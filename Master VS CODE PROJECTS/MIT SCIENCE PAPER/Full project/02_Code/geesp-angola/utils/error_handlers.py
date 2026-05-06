from typing import Callable, TypeVar, Optional, Any, Dict
import functools
import logging
import inspect
import time

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================

class GEESPError(Exception):
    """Base exception for all GEESP-Angola errors"""
    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.context = context or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API responses"""
        return {
            "error": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context
        }


class ValidationError(GEESPError):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        self.field = field
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)


class DataError(GEESPError):
    """Raised when data loading or processing fails"""
    def __init__(self, message: str, source: Optional[str] = None, **kwargs):
        self.source = source
        super().__init__(message, error_code="DATA_ERROR", **kwargs)


class ConfigurationError(GEESPError):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        self.config_key = config_key
        super().__init__(message, error_code="CONFIG_ERROR", **kwargs)


class GEEIntegrationError(GEESPError):
    """Raised when Google Earth Engine operations fail"""
    def __init__(self, message: str, gee_error: Optional[str] = None, **kwargs):
        self.gee_error = gee_error
        super().__init__(message, error_code="GEE_ERROR", **kwargs)


class APIError(GEESPError):
    """Raised when API operations fail"""
    def __init__(self, message: str, status_code: int = 500, **kwargs):
        self.status_code = status_code
        super().__init__(message, error_code=f"API_ERROR_{status_code}", **kwargs)


class DatabaseError(GEESPError):
    """Raised when database operations fail"""
    def __init__(self, message: str, operation: Optional[str] = None, **kwargs):
        self.operation = operation
        super().__init__(message, error_code="DATABASE_ERROR", **kwargs)


class TimeoutError(GEESPError):
    """Raised when operations timeout"""
    def __init__(self, message: str, timeout_seconds: Optional[float] = None, **kwargs):
        self.timeout_seconds = timeout_seconds
        super().__init__(message, error_code="TIMEOUT_ERROR", **kwargs)


def handle_exceptions(default: Optional[Any] = None, swallow: bool = True):
    """Decorator to catch exceptions, log them and optionally return a default.

    Args:
        default: Value to return if an exception occurs (None by default).
        swallow: If True, exceptions are not re-raised.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                if swallow:
                    return default
                raise

        return wrapper  # type: ignore

    return decorator


def retry_on_exception(retries: int = 3, delay_seconds: float = 1.0, backoff: float = 2.0):
    """Retry decorator with exponential backoff for idempotent operations.

    Args:
        retries: Number of retries before failing
        delay_seconds: Initial sleep between attempts
        backoff: Multiplier for exponential backoff (e.g., 2.0 = exponential growth)
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    is_last_attempt = attempt == retries
                    wait_time = delay_seconds * (backoff ** (attempt - 1))
                    
                    if is_last_attempt:
                        logger.error(
                            f"All {retries} attempts failed for {func.__name__}",
                            extra={"exception": str(e), "attempt": attempt}
                        )
                    else:
                        logger.warning(
                            f"Attempt {attempt}/{retries} failed for {func.__name__}: {e}. "
                            f"Retrying in {wait_time:.1f}s",
                            extra={"exception": str(e), "attempt": attempt, "wait_time": wait_time}
                        )
                        time.sleep(wait_time)
            
            raise last_exc

        return wrapper  # type: ignore

    return decorator


# ============================================================================
# INPUT VALIDATION DECORATOR
# ============================================================================

def validate_inputs(**type_checks: Dict[str, Callable[[Any], bool]]):
    """
    Decorator to validate function inputs against type checks.
    
    Args:
        **type_checks: Mapping of parameter names to validation functions.
                      Each validation function should return True if valid,
                      raise ValidationError or return False if invalid.
    
    Example:
        @validate_inputs(
            data=lambda x: isinstance(x, np.ndarray),
            threshold=lambda x: 0 <= x <= 1
        )
        def my_function(data, threshold=0.5):
            ...
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each parameter
            for param_name, validator in type_checks.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    try:
                        is_valid = validator(value)
                        if is_valid is False:
                            raise ValidationError(
                                f"Parameter '{param_name}' failed validation in {func.__name__}"
                            )
                    except ValidationError:
                        raise
                    except Exception as e:
                        raise ValidationError(
                            f"Validator error for '{param_name}' in {func.__name__}: {e}"
                        )
            
            # Call original function
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    
    return decorator


# ============================================================================
# ERROR FORMATTING & RESPONSE UTILITIES
# ============================================================================

def format_api_error(error: Exception, status_code: int = 500) -> Dict[str, Any]:
    """Format exception as API-friendly JSON response
    
    Args:
        error: The exception to format
        status_code: HTTP status code (default 500)
    
    Returns:
        Dictionary with error details suitable for JSON response
    """
    if isinstance(error, GEESPError):
        response = error.to_dict()
        response["status_code"] = status_code
    else:
        response = {
            "error": error.__class__.__name__,
            "error_code": "INTERNAL_ERROR",
            "message": str(error),
            "status_code": status_code,
            "context": {}
        }
    
    logger.error(f"API Error {status_code}: {response['message']}")
    return response


def catch_and_format_error(func: F, default_status: int = 500) -> F:
    """Decorator to catch exceptions and format as API responses
    
    Args:
        default_status: Default HTTP status code for exceptions
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GEESPError as e:
            status = e.status_code if isinstance(e, APIError) else default_status
            return format_api_error(e, status)
        except Exception as e:
            return format_api_error(e, default_status)
    
    return wrapper  # type: ignore


# ============================================================================
# ERROR CONTEXT MANAGEMENT
# ============================================================================

class ErrorContext:
    """Context manager for preserving error context across function calls
    
    Example:
        with ErrorContext("data_loading", {"filename": "data.tif"}):
            load_data()  # If this fails, context will be included in error
    """
    
    _stack = []
    
    def __init__(self, operation: str, context: Optional[Dict] = None):
        self.operation = operation
        self.context = context or {}
    
    def __enter__(self):
        ErrorContext._stack.append((self.operation, self.context))
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        ErrorContext._stack.pop()
        
        if exc_type is not None and issubclass(exc_type, GEESPError):
            # Add operation context to error
            if not exc_val.context.get("operation"):
                exc_val.context["operation"] = self.operation
            if self.context:
                exc_val.context["operation_context"] = self.context
            logger.debug(f"Error context for {self.operation}: {exc_val.context}")
        
        return False  # Don't suppress exceptions
    
    @classmethod
    def get_stack(cls) -> list:
        """Get current error context stack"""
        return cls._stack.copy()
