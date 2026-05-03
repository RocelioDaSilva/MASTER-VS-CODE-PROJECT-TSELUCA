"""
GEESP-Angola: Unified Error Handling and Validation Module
Consolidates exception handling, input validation, and error recovery patterns
"""

from typing import Any, Callable, Optional, Tuple, Union, TypeVar, Dict
from functools import wraps
from dataclasses import dataclass
import inspect
from contextlib import contextmanager

from utils.logging import setup_logging
from utils.exceptions import (
    ValidationError, 
    DataError, 
    ConfigurationError,
    retry_on_exception
)

logger = setup_logging(__name__)

T = TypeVar('T')


# ============================================================================
# INPUT VALIDATION
# ============================================================================


def validate_type(value: Any, expected_type: Union[type, Tuple[type, ...]], param_name: str = "value") -> Any:
    """
    Validate input is correct type.
    
    Args:
        value: Value to validate
        expected_type: Expected type(s)
        param_name: Parameter name for error messages
        
    Returns:
        The value if valid
        
    Raises:
        ValidationError: If type is incorrect
        
    Example:
        >>> validate_type([1, 2, 3], (list, tuple), "items")
        [1, 2, 3]
    """
    if not isinstance(value, expected_type):
        type_names = (
            ", ".join(t.__name__ for t in expected_type)
            if isinstance(expected_type, tuple)
            else expected_type.__name__
        )
        raise ValidationError(
            f"Parameter '{param_name}' must be {type_names}, got {type(value).__name__}"
        )
    return value


def validate_range(
    value: float,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    param_name: str = "value"
) -> float:
    """
    Validate numeric value is within range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        param_name: Parameter name for error messages
        
    Returns:
        The value if valid
        
    Raises:
        ValidationError: If out of range
        
    Example:
        >>> validate_range(5, min_val=0, max_val=10, param_name="score")
        5
    """
    validate_type(value, (int, float), param_name)
    
    if min_val is not None and value < min_val:
        raise ValidationError(
            f"Parameter '{param_name}' must be >= {min_val}, got {value}"
        )
    
    if max_val is not None and value > max_val:
        raise ValidationError(
            f"Parameter '{param_name}' must be <= {max_val}, got {value}"
        )
    
    return value


def validate_string(
    value: str,
    allowed_values: Optional[Tuple[str, ...]] = None,
    min_length: int = 0,
    param_name: str = "value"
) -> str:
    """
    Validate string parameter.
    
    Args:
        value: String to validate
        allowed_values: If provided, value must be in this tuple
        min_length: Minimum string length
        param_name: Parameter name for error messages
        
    Returns:
        The value if valid
        
    Raises:
        ValidationError: If validation fails
        
    Example:
        >>> validate_string("high", allowed_values=("low", "medium", "high"))
        "high"
    """
    validate_type(value, str, param_name)
    
    if len(value) < min_length:
        raise ValidationError(
            f"Parameter '{param_name}' length must be >= {min_length}"
        )
    
    if allowed_values is not None and value not in allowed_values:
        raise ValidationError(
            f"Parameter '{param_name}' must be one of {allowed_values}, got '{value}'"
        )
    
    return value


def validate_not_empty(value: Any, param_name: str = "value") -> Any:
    """
    Validate value is not empty.
    
    Args:
        value: Value to validate
        param_name: Parameter name for error messages
        
    Returns:
        The value if valid
        
    Raises:
        ValidationError: If empty
        
    Example:
        >>> validate_not_empty([1, 2, 3], "items")
        [1, 2, 3]
    """
    if not value:
        raise ValidationError(f"Parameter '{param_name}' cannot be empty")
    return value


# ============================================================================
# FUNCTION INPUT VALIDATION DECORATOR
# ============================================================================


def validate_inputs(**validators) -> Callable:
    """
    Decorator to validate function inputs automatically.
    
    Args:
        **validators: Mapping of parameter name to validation function
        
    Returns:
        Decorated function
        
    Example:
        @validate_inputs(
            score=lambda x: validate_range(x, 0, 100),
            name=lambda x: validate_not_empty(x, "name")
        )
        def process(score: int, name: str) -> str:
            return f"{name}: {score}"
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each parameter
            for param_name, validator_func in validators.items():
                if param_name in bound_args.arguments:
                    try:
                        validated_value = validator_func(bound_args.arguments[param_name])
                        bound_args.arguments[param_name] = validated_value
                    except ValidationError as e:
                        logger.error(f"Validation failed for '{param_name}' in {func.__name__}: {str(e)}")
                        raise
            
            return func(*bound_args.args, **bound_args.kwargs)
        
        return wrapper
    
    return decorator


# ============================================================================
# EXCEPTION HANDLING DECORATORS
# ============================================================================


def safe_call(
    default_return: Any = None,
    log_errors: bool = True,
    reraise: bool = False
) -> Callable:
    """
    Decorator for safe function execution with error handling.
    
    Args:
        default_return: Return value if exception occurs
        log_errors: If True, log exceptions
        reraise: If True, re-raise exceptions after logging
        
    Returns:
        Decorated function
        
    Example:
        @safe_call(default_return=0, log_errors=True)
        def risky_operation():
            return 1 / 0  # Will return 0 instead of raising
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                if reraise:
                    raise
                return default_return
        
        return wrapper
    
    return decorator


def retry_with_backoff(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[type, ...] = (Exception,)
) -> Callable:
    """
    Decorator for automatic retry with exponential backoff.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries (seconds)
        backoff_factor: Multiplier for delay on each retry
        exceptions: Tuple of exception types to catch
        
    Returns:
        Decorated function
        
    Example:
        @retry_with_backoff(max_attempts=3, delay=1.0)
        def unstable_operation():
            return fetch_from_api()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    attempt_num = attempt + 1
                    
                    if attempt_num < max_attempts:
                        logger.warning(
                            f"Attempt {attempt_num}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        import time
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}"
                        )
            
            raise last_exception or Exception("Retry failed with no exception tracked")
        
        return wrapper
    
    return decorator


# ============================================================================
# CONTEXT MANAGERS
# ============================================================================


@contextmanager
def handle_errors(operation_name: str = "operation"):
    """
    Context manager for error handling.
    
    Args:
        operation_name: Name of operation for logging
        
    Example:
        with handle_errors("data_loading"):
            data = load_data()
    """
    try:
        yield
    except ValidationError as e:
        logger.error(f"Validation error during {operation_name}: {str(e)}")
        raise
    except DataError as e:
        logger.error(f"Data error during {operation_name}: {str(e)}")
        raise
    except ConfigurationError as e:
        logger.error(f"Configuration error during {operation_name}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during {operation_name}: {str(e)}", exc_info=True)
        raise


@contextmanager
def suppress_errors(exception: type = Exception):
    """
    Context manager to suppress specific exceptions.
    
    Args:
        exception: Exception type to suppress
        
    Example:
        with suppress_errors(FileNotFoundError):
            os.remove('maybe_nonexistent_file.txt')
    """
    try:
        yield
    except exception as e:
        logger.debug(f"Suppressed exception: {type(e).__name__}: {str(e)}")


# ============================================================================
# RESULT WRAPPING
# ============================================================================


@dataclass
class Result:
    """
    Represents result of operation with success status and optional error.
    
    Example:
        result = Result(success=True, data=[1, 2, 3])
        if result.success:
            print(result.data)
    """
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    
    def is_success(self) -> bool:
        """Check if operation succeeded."""
        return self.success
    
    def is_error(self) -> bool:
        """Check if operation failed."""
        return not self.success
    
    def get_or_raise(self) -> Any:
        """Get data or raise error if failed."""
        if self.is_error():
            raise DataError(self.error or "Operation failed")
        return self.data
    
    def get_or_default(self, default: Any) -> Any:
        """Get data or return default if failed."""
        return self.data if self.is_success() else default


from dataclasses import dataclass


def operation_result(func: Callable) -> Callable:
    """
    Decorator to wrap function result in Result object.
    
    Args:
        func: Function to wrap
        
    Returns:
        Decorated function returning Result
        
    Example:
        @operation_result
        def safe_divide(a, b):
            return a / b
        
        result = safe_divide(10, 2)
        if result.is_success():
            print(result.data)  # 5.0
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Result:
        try:
            data = func(*args, **kwargs)
            return Result(success=True, data=data)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return Result(success=False, error=str(e))
    
    return wrapper


# ============================================================================
# ERROR REPORTING
# ============================================================================


def get_error_summary(exception: Exception) -> Dict[str, Any]:
    """
    Get comprehensive error summary.
    
    Args:
        exception: Exception to summarize
        
    Returns:
        Dictionary with error details
        
    Example:
        try:
            operation()
        except Exception as e:
            summary = get_error_summary(e)
            logger.error(f"Error: {summary['message']}")
    """
    import traceback
    
    return {
        'type': type(exception).__name__,
        'message': str(exception),
        'traceback': traceback.format_exc(),
        'module': exception.__class__.__module__,
    }


from typing import Dict
