"""
GEESP-Angola: Unified Validation Pipeline
Provides consistent validation framework for all data validation operations
"""

from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional, Tuple
from enum import Enum
from typing import Dict, Any, Tuple

import numpy as np

from utils.logging import setup_logging
from utils.constants import ConfigLoaderConstants
from utils.exceptions import ValidationError
from . import validators

logger = setup_logging(__name__)


class ValidationType(str, Enum):
    """Types of validation checks"""
    CRITICAL = "critical"  # Must pass or raise exception
    WARNING = "warning"    # Log warning but continue
    INFO = "info"          # Log for information only


@dataclass
class ValidationCheck:
    """Single validation check definition"""
    name: str
    validator_func: Callable[[Any], bool]
    check_type: ValidationType = ValidationType.CRITICAL
    error_message: Optional[str] = None
    
    def execute(self, data: Any) -> Tuple[bool, Optional[str]]:
        """
        Execute validation check.
        
        Args:
            data: Data to validate
            
        Returns:
            Tuple of (passed, error_message)
        """
        try:
            result = self.validator_func(data)
            if result:
                return True, None
            else:
                return False, self.error_message or f"{self.name} validation failed"
        except Exception as e:
            return False, str(e)


@dataclass
class ValidationResult:
    """Result of validation pipeline execution"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0
    
    def add_error(self, message: str) -> None:
        """Add an error message"""
        self.errors.append(message)
        self.checks_failed += 1
    
    def add_warning(self, message: str) -> None:
        """Add a warning message"""
        self.warnings.append(message)
    
    def mark_passed(self) -> None:
        """Mark a check as passed"""
        self.checks_passed += 1
    
    def finalize(self) -> None:
        """Finalize result - set valid flag based on errors"""
        self.valid = len(self.errors) == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "total_checks": self.checks_passed + self.checks_failed,
        }
    
    def __str__(self) -> str:
        """String representation"""
        if self.valid:
            return f"✓ Validation passed ({self.checks_passed} checks)"
        else:
            return f"✗ Validation failed ({self.checks_failed} errors, {len(self.warnings)} warnings)"


class ValidationPipeline:
    """
    Unified validation pipeline for data validation.
    
    Allows composing multiple validation checks with consistent error handling.
    """
    
    def __init__(self, name: str = "ValidationPipeline"):
        """Initialize validation pipeline."""
        self.name = name
        self.checks: List[ValidationCheck] = []
        self.logger = logger
    
    def add_check(self, check: ValidationCheck) -> "ValidationPipeline":
        """Add validation check to pipeline."""
        self.checks.append(check)
        self.logger.debug(f"[{self.name}] Added check: {check.name}")
        return self
    
    def add_checks(self, checks: List[ValidationCheck]) -> "ValidationPipeline":
        """Add multiple validation checks."""
        for check in checks:
            self.add_check(check)
        return self
    
    def validate(self, data: Any, stop_on_error: bool = False) -> ValidationResult:
        """Execute all validation checks."""
        result = ValidationResult()
        
        self.logger.info(f"[{self.name}] Starting validation with {len(self.checks)} checks")
        
        for check in self.checks:
            passed, error_msg = check.execute(data)
            
            if passed:
                result.mark_passed()
                self.logger.debug(f"  ✓ {check.name}")
            else:
                if check.check_type == ValidationType.CRITICAL:
                    result.add_error(error_msg or f"{check.name} failed")
                    self.logger.error(f"  ✗ {check.name}: {error_msg}")
                    if stop_on_error:
                        break
                elif check.check_type == ValidationType.WARNING:
                    result.add_warning(error_msg or f"{check.name} warning")
                    self.logger.warning(f"  ⚠️  {check.name}: {error_msg}")
                elif check.check_type == ValidationType.INFO:
                    self.logger.info(f"  ℹ️  {check.name}: {error_msg}")
        
        result.finalize()
        self.logger.info(f"[{self.name}] Validation result: {result}")
        
        return result
    
    def validate_and_raise(self, data: Any, stop_on_error: bool = True) -> ValidationResult:
        """Execute validation and raise exception if any critical errors."""
        result = self.validate(data, stop_on_error=stop_on_error)
        
        if not result.valid:
            error_summary = "\n".join([f"  - {e}" for e in result.errors])
            raise ValidationError(
                f"Validation failed in {self.name}:\n{error_summary}"
            )
        
        return result
    
    def clear(self) -> None:
        """Clear all validation checks"""
        self.checks.clear()
        self.logger.debug(f"[{self.name}] Cleared all checks")


# ============================================================================
# LEGACY FUNCTION - MAINTAINED FOR BACKWARD COMPATIBILITY
# ============================================================================

def run_validation_pipeline(
    rasters: Dict[str, np.ndarray],
    weights: Dict[str, float],
    capacity_mw: float,
    annual_irradiance: float,
    discount_rate: float,
    expected_shape: Tuple[int, int] = None,
) -> Dict[str, Any]:
    """Run a validation pipeline using `scripts.validators` helpers.

    Args:
        rasters: Dict with keys 'solar','population','distance','slope','ndvi'
        weights: MCDA weights dict (should sum to 1)
        capacity_mw: Project capacity in MW
        annual_irradiance: Annual irradiance in kWh/m2/year
        discount_rate: Discount rate (%) for LCOE
        expected_shape: Expected raster shape (default from ConfigLoaderConstants)

    Returns:
        Dict containing 'ok':bool and 'errors': list[str]

    Raises:
        ValueError if critical validation fails
    """
    if expected_shape is None:
        expected_shape = ConfigLoaderConstants.MAP_OUTPUT_SHAPE_DEFAULT
    
    errors = []

    # Extract rasters
    solar = rasters.get("solar")
    population = rasters.get("population")
    distance = rasters.get("distance")
    slope = rasters.get("slope")
    ndvi = rasters.get("ndvi")

    try:
        validators.validate_all_inputs(
            solar,
            population,
            distance,
            slope,
            ndvi,
            weights,
            capacity_mw,
            annual_irradiance,
            discount_rate,
            expected_shape=expected_shape,
        )
        logger.info("All inputs validated successfully by validation_pipeline")
        return {"ok": True, "errors": []}
    except Exception as e:
        logger.warning(f"Validation pipeline reported errors: {e}")
        return {"ok": False, "errors": [str(e)]}


def quick_validate_shapes(rasters: Dict[str, np.ndarray], expected_shape: Tuple[int, int] = None) -> bool:
    """Fast shape-only check for rasters; raises ValueError on mismatch."""
    if expected_shape is None:
        expected_shape = ConfigLoaderConstants.MAP_OUTPUT_SHAPE_DEFAULT
    
    for name, arr in rasters.items():
        if arr is None:
            raise ValueError(f"Raster '{name}' is None")
        if not isinstance(arr, np.ndarray):
            raise ValueError(f"Raster '{name}' is not numpy array (got {type(arr)})")
        if arr.shape != expected_shape:
            raise ValueError(f"Raster '{name}' shape {arr.shape} != expected {expected_shape}")
    return True
