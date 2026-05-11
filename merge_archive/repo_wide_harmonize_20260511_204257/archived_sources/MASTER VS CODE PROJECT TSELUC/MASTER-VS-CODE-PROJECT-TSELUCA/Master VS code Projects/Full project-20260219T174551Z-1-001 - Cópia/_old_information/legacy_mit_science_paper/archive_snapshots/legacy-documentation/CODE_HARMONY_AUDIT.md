# GEESP-Angola Code Harmony Audit Report

## EXECUTIVE SUMMARY

**Status**: ⚠️ SIGNIFICANT DISHARMONY DETECTED  
**Severity**: HIGH  
**Impact**: Code maintainability, developer experience, testing reliability

---

## CRITICAL FINDINGS

### 1. ❌ DUPLICATE EXCEPTION HIERARCHIES (CRITICAL)

**Problem**: Two competing exception systems defined in parallel:

#### Location 1: `utils/error_handlers.py`
```python
class ErrorSeverity(str, Enum): ...
class GEESPError(Exception): ...
class ValidationError(GEESPError): ...
class DataError(GEESPError): ...
class ConfigurationError(GEESPError): ...
class GEEIntegrationError(GEESPError): ...
class APIError(GEESPError): ...
class DatabaseError(GEESPError): ...
class TimeoutError(GEESPError): ...
```

#### Location 2: `utils/exceptions_config.py`
```python
class ErrorSeverity(Enum): ...  # ⚠️ DUPLICATE!
class GeespAnglolaException(Exception): ...  # Different naming!
class ValidationError(GeespAnglolaException): ...  # ⚠️ DUPLICATE!
class DataError(GeespAnglolaException): ...  # ⚠️ DUPLICATE!
class ConfigurationError(GeespAnglolaException): ...  # ⚠️ DUPLICATE!
class GeoProcessingError(GeespAnglolaException): ...
class MCDAError(GeespAnglolaException): ...
class AHPError(GeespAnglolaException): ...
class LCOECalculationError(GeespAnglolaException): ...
class APIError(GeespAnglolaException): ...  # ⚠️ DUPLICATE!
class TimeoutError(GeespAnglolaException): ...  # ⚠️ DUPLICATE!
class DataValidationError(ValidationError): ...
```

**Issues**:
- ✗ 7 exception classes defined TWICE with identical names
- ✗ Different base class names: `GEESPError` vs `GeespAnglolaException`
- ✗ Different ErrorSeverity implementations (str,Enum vs plain Enum)
- ✗ Different initialization patterns (**kwargs vs **context)
- ✗ Tests import from BOTH modules inconsistently
- ✗ Violates DRY principle (Don't Repeat Yourself)

**Impact**: 
- Confusion about which to use
- Harder to maintain - fixes in one place don't apply to the other
- Tests fail if wrong import used
- Runtime issues if code mixes imports

---

### 2. ❌ INCONSISTENT IMPORT PATTERNS

**Current State**:
```python
# Some files use this:
from utils.error_handlers import handle_exceptions, ValidationError, GEESPError

# Other files use this:
from utils.exceptions_config import ValidationError, retry_on_exception, GeespAnglolaException

# Some files use BOTH:
from utils.error_handlers import handle_exceptions
from utils.exceptions_config import retry_on_exception
```

**Files with Mixed Imports** (15+ files):
- `tests/test_error_handling_adapted.py`
- `scripts/lcoe_calculator.py`
- `scripts/earth_engine_integration.py`
- `scripts/core_utils.py`
- `scripts/batch_mcda_api.py`
- And 10+ others

**Standard Should Be**: Single, consistent import source

---

### 3. ❌ MISSING UNIFIED INTERFACE

**Expected Pattern** (from STANDARDS_AND_CONVENTIONS.md):
```python
# Should have ONE unified import source
from utils.exceptions import (
    ValidationError,
    DataError,
    ConfigurationError,
    GEESPError,
    ErrorSeverity,
    handle_exceptions,
    retry_on_exception,
)
```

**Actual Pattern**:
```python
# Scattered, inconsistent across files
from utils.error_handlers import ...
from utils.exceptions_config import ...
# Sometimes both, sometimes one, sometimes wrong one
```

---

### 4. ❌ INCONSISTENT DECORATOR LOCATIONS

**Location 1**: `utils/error_handlers.py`
```python
def handle_exceptions(...): ...
def validate_inputs(...): ...
```

**Location 2**: `utils/exceptions_config.py`
```python
def retry_on_exception(...): ...
```

**Problem**: Decorators scattered across modules instead of centralized

---

### 5. ⚠️ PARAMETER PATTERN INCONSISTENCY

**error_handlers.py** (Using **kwargs):
```python
def __init__(self, message: str, field: Optional[str] = None, **kwargs):
    self.field = field
    super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)
```

**exceptions_config.py** (Using **context):
```python
def __init__(self, message: str, field: Optional[str] = None, **context: Any):
    context["field"] = field
    super().__init__(
        message=message,
        error_code="VALIDATION_ERROR",
        severity=ErrorSeverity.ERROR,
        **context
    )
```

**Impact**: Different semantics, harder to reason about

---

### 6. ⚠️ MISSING SPECIALIZED ERROR TYPES

**In exceptions_config.py** (Not in error_handlers.py):
- GeoProcessingError
- MCDAError
- AHPError
- LCOECalculationError

**Potential Issue**: If someone imports from error_handlers, they can't catch these specialized errors

---

### 7. ⚠️ UNEQUAL IMPLEMENTATIONS

**error_handlers.py** has:
- ErrorSeverity (str, Enum) ✓ JSON-serializable
- to_dict() method ✓

**exceptions_config.py** has:
- format_message() with context formatting ✓
- More detailed context tracking ✓
- But ErrorSeverity without str - NOT JSON-serializable ✗

---

## RECOMMENDED CONSOLIDATION STRATEGY

### Phase 1: Create Single Source of Truth

**Create**: `utils/exceptions.py` (replace both files)

```python
"""
GEESP-Angola: Unified Exception & Error Handling System
Single source of truth for all exceptions, decorators, and error handling.
"""

from typing import Any, Optional, Dict, Callable
from enum import Enum
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CORE DEFINITIONS
# ============================================================================

class ErrorSeverity(str, Enum):
    """Error severity levels - string serializable for JSON/API"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class GEESPError(Exception):
    """Unified base exception for all GEESP-Angola errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.context = context or {}
        
        # Store kwargs as attributes for field-specific errors
        for key, value in kwargs.items():
            self.context[key] = value
            setattr(self, key, value)
        
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Format exception with context"""
        msg = f"[{self.error_code}] {self.message}"
        if self.context:
            ctx = " | ".join(f"{k}={v}" for k, v in self.context.items())
            msg += f" | {ctx}"
        return msg
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for API responses"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "severity": self.severity.value,  # String value from enum
            "context": self.context,
        }


# ============================================================================
# VALIDATION & DATA ERRORS
# ============================================================================

class ValidationError(GEESPError):
    """Raised when validation fails"""
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        **context
    ):
        if field:
            context["field"] = field
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class DataError(GEESPError):
    """Raised when data loading/processing fails"""
    def __init__(self, message: str, source: Optional[str] = None, **context):
        if source:
            context["source"] = source
        super().__init__(
            message,
            error_code="DATA_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class DataValidationError(ValidationError):
    """Raised when data validation fails with field info"""
    def __init__(self, message: str, field: Optional[str] = None, **context):
        super().__init__(message, field=field, **context)


# ============================================================================
# CONFIGURATION & PROCESSING ERRORS
# ============================================================================

class ConfigurationError(GEESPError):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, config_key: Optional[str] = None, **context):
        if config_key:
            context["config_key"] = config_key
        super().__init__(
            message,
            error_code="CONFIGURATION_ERROR",
            severity=ErrorSeverity.CRITICAL,
            context=context
        )


class GeoProcessingError(GEESPError):
    """Raised when geospatial processing fails"""
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        layer_name: Optional[str] = None,
        **context
    ):
        if operation:
            context["operation"] = operation
        if layer_name:
            context["layer_name"] = layer_name
        super().__init__(
            message,
            error_code="GEO_PROCESSING_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class MCDAError(GEESPError):
    """Raised when MCDA analysis fails"""
    def __init__(
        self,
        message: str,
        analysis_step: Optional[str] = None,
        **context
    ):
        if analysis_step:
            context["analysis_step"] = analysis_step
        super().__init__(
            message,
            error_code="MCDA_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class AHPError(GEESPError):
    """Raised when AHP analysis fails"""
    def __init__(self, message: str, consistency_ratio: Optional[float] = None, **context):
        if consistency_ratio:
            context["consistency_ratio"] = consistency_ratio
        super().__init__(
            message,
            error_code="AHP_ERROR",
            severity=ErrorSeverity.WARNING,
            context=context
        )


class LCOECalculationError(GEESPError):
    """Raised when LCOE calculation fails"""
    def __init__(
        self,
        message: str,
        parameter: Optional[str] = None,
        zone: Optional[str] = None,
        **context
    ):
        if parameter:
            context["parameter"] = parameter
        if zone:
            context["zone"] = zone
        super().__init__(
            message,
            error_code="LCOE_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


# ============================================================================
# INTEGRATION ERRORS
# ============================================================================

class GEEIntegrationError(GEESPError):
    """Raised when Google Earth Engine operations fail"""
    def __init__(self, message: str, gee_error: Optional[str] = None, **context):
        if gee_error:
            context["gee_error"] = gee_error
        super().__init__(
            message,
            error_code="GEE_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class APIError(GEESPError):
    """Raised when API operations fail"""
    def __init__(self, message: str, status_code: int = 500, **context):
        context["status_code"] = status_code
        super().__init__(
            message,
            error_code=f"API_ERROR_{status_code}",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class DatabaseError(GEESPError):
    """Raised when database operations fail"""
    def __init__(self, message: str, operation: Optional[str] = None, **context):
        if operation:
            context["operation"] = operation
        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            severity=ErrorSeverity.ERROR,
            context=context
        )


class TimeoutError(GEESPError):
    """Raised when operations timeout"""
    def __init__(
        self,
        message: str,
        timeout_seconds: Optional[float] = None,
        operation: Optional[str] = None,
        **context
    ):
        if timeout_seconds:
            context["timeout_seconds"] = timeout_seconds
        if operation:
            context["operation"] = operation
        super().__init__(
            message,
            error_code="TIMEOUT_ERROR",
            severity=ErrorSeverity.WARNING,
            context=context
        )


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

GeespAnglolaException = GEESPError  # Old naming
GEESPBaseException = GEESPError      # Old naming


# ============================================================================
# DECORATORS
# ============================================================================

def handle_exceptions(
    func_or_default: Any = None,
    swallow: bool = True,
    default: Any = None
) -> Callable:
    """Decorator to catch exceptions gracefully"""
    if callable(func_or_default) and not isinstance(func_or_default, type):
        # Direct decoration: @handle_exceptions
        func = func_or_default
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                return None
        
        return wrapper
    
    # Parameterized: @handle_exceptions(default=X, swallow=True)
    actual_default = func_or_default if func_or_default is not None else default
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                if swallow:
                    return actual_default
                raise
        return wrapper
    
    return decorator


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_multiplier: float = 1.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed: {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_multiplier
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed: {e}"
                        )
            
            raise last_exception
        
        return wrapper
    
    return decorator


def validate_inputs(**type_checks: Dict[str, Callable[[Any], bool]]) -> Callable:
    """Decorator to validate function inputs"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for param_name, validator in type_checks.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    try:
                        is_valid = validator(value)
                        if is_valid is False:
                            raise ValidationError(
                                f"Parameter '{param_name}' failed validation"
                            )
                    except ValidationError:
                        raise
                    except Exception as e:
                        raise ValidationError(
                            f"Validation error for '{param_name}': {e}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ============================================================================
# EXPORT ALL
# ============================================================================

__all__ = [
    # Severity and base
    "ErrorSeverity",
    "GEESPError",
    "GeespAnglolaException",  # Backward compatibility
    "GEESPBaseException",      # Backward compatibility
    
    # Exceptions
    "ValidationError",
    "DataError",
    "DataValidationError",
    "ConfigurationError",
    "GeoProcessingError",
    "MCDAError",
    "AHPError",
    "LCOECalculationError",
    "GEEIntegrationError",
    "APIError",
    "DatabaseError",
    "TimeoutError",
    
    # Decorators
    "handle_exceptions",
    "retry_on_exception",
    "validate_inputs",
]
```

### Phase 2: Update All Imports

**Replace in ALL files**:
```python
# OLD (delete these)
from utils.error_handlers import ...
from utils.exceptions_config import ...

# NEW (use this everywhere)
from utils.exceptions import (
    GEESPError,
    ValidationError,
    DataError,
    ConfigurationError,
    ErrorSeverity,
    handle_exceptions,
    retry_on_exception,
)
```

### Phase 3: Delete Old Files

```bash
rm utils/error_handlers.py
rm utils/exceptions_config.py
```

### Phase 4: Update __init__.py Files

**utils/__init__.py** should export all exceptions:
```python
from utils.exceptions import (
    ErrorSeverity,
    GEESPError,
    ValidationError,
    # ... all others
)

__all__ = [
    "ErrorSeverity",
    "GEESPError",
    "ValidationError",
    # ... all others
]
```

---

## ADDITIONAL HARMONY ISSUES FOUND

### 8. ⚠️ Missing Type Annotation Consistency

**Issue**: Some files missing proper type hints
- `scripts/lcoe_calculator.py` - Mix of typed and untyped parameters
- `scripts/mcda_analysis.py` - Incomplete type coverage

**Solution**: Run `mypy` in strict mode

### 9. ⚠️ Docstring Inconsistency

**Issue**: Docstrings vary in format:
- Some use Google-style
- Some use NumPy-style
- Some minimal or missing

**Solution**: Standardize on Google-style (established in STANDARDS_AND_CONVENTIONS.md)

### 10. ⚠️ Logging Pattern Inconsistency

**Issue**: Different logging setup patterns
- Some files: `logger = logging.getLogger(__name__)`
- Some files through: `setup_logging(__name__)`

**Solution**: Use `setup_logging(__name__)` consistently

---

## IMPLEMENTATION PLAN

| Phase | Task | Effort | Files | Priority |
|-------|------|--------|-------|----------|
| 1 | Create unified `exceptions.py` | 2 hours | 1 new file | CRITICAL |
| 2 | Update imports across codebase | 3 hours | 40+ files | CRITICAL |
| 3 | Delete old exception files | 30 min | 2 files | CRITICAL |
| 4 | Update utils/__init__.py | 1 hour | 1 file | HIGH |
| 5 | Run comprehensive tests | 1 hour | tests/ | HIGH |
| 6 | Fix type annotations | 4 hours | 15+ files | MEDIUM |
| 7 | Standardize docstrings | 3 hours | 20+ files | MEDIUM |
| 8 | Standardize logging | 2 hours | 30+ files | MEDIUM |

**Total Estimated Effort**: 16-17 hours for complete harmony

---

## VERIFICATION CHECKLIST

After consolidation:
- [ ] All imports use `from utils.exceptions import ...`
- [ ] No imports from `error_handlers` or `exceptions_config`
- [ ] All tests pass with new unified exceptions
- [ ] `mypy --strict` passes for all files
- [ ] All docstrings use consistent Google-style format
- [ ] All files use `setup_logging(__name__)`
- [ ] No duplicate exception definitions
- [ ] Review for additional consistency issues

---

## EXPECTED BENEFITS

✅ **Single Source of Truth**: One exception hierarchy  
✅ **Predictable Imports**: Everyone knows where to import from  
✅ **Easier Maintenance**: Changes in one place  
✅ **Better Testing**: Consistent exception handling  
✅ **Cleaner Code**: Less boilerplate, clearer intent  
✅ **Developer Experience**: Clear standards to follow  
✅ **Better Documentation**: Centralized definitions  

---

**Report Generated**: 2026-03-05  
**Status**: READY FOR IMPLEMENTATION  
**Next Step**: Review and approve consolidation strategy
