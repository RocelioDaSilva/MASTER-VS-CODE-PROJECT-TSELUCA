"""Canonical source: analysis/base.py. Re-exported here for backward compatibility."""
from analysis.base import AnalysisResult, Component, Validator, AnalysisEngine, RasterProcessor  # noqa: F401

__all__ = ["AnalysisResult", "Component", "Validator", "AnalysisEngine", "RasterProcessor"]

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

from utils.logging import get_logger
from utils.exceptions import ValidationError

logger = get_logger(__name__)


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class AnalysisResult:
    """Base class for analysis results"""

    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        status = "✓ Success" if self.success else "✗ Failed"
        if self.error:
            return f"{status}: {self.error}"
        return status


# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================


class Component(ABC):
    """Base class for GEESP-Angola analysis components"""

    def __init__(self, component_name: str) -> None:
        """
        Initialize component.

        Args:
            component_name: Name of component for logging
        """
        self.component_name = component_name
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def log_info(self, message: str) -> None:
        """Log info message with component prefix"""
        self.logger.info(f"[{self.component_name}] {message}")

    def log_warning(self, message: str) -> None:
        """Log warning with component prefix"""
        self.logger.warning(f"[{self.component_name}] {message}")

    def log_error(self, message: str) -> None:
        """Log error with component prefix"""
        self.logger.error(f"[{self.component_name}] {message}")

    @abstractmethod
    def validate(self) -> bool:
        """Validate component state. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def execute(self) -> AnalysisResult:
        """Execute component analysis. Must be implemented by subclasses."""
        pass


class Validator(ABC):
    """Base class for validation handlers"""

    def __init__(self) -> None:
        """Initialize validator"""
        self.logger = get_logger(self.__class__.__name__)
        self.errors: list = []
        self.warnings: list = []

    def validate(self, data: Any, **kwargs: Any) -> bool:
        """
        Validate data. Returns True if valid, False otherwise.

        Args:
            data: Data to validate
            **kwargs: Additional validation parameters

        Returns:
            True if validation passes, False otherwise
        """
        try:
            self._validate_impl(data, **kwargs)
            if self.errors:
                return False
            return True
        except Exception as e:
            self.log_error(f"Validation failed: {str(e)}")
            return False

    @abstractmethod
    def _validate_impl(self, data: Any, **kwargs: Any) -> None:
        """
        Implement validation logic. Subclasses should populate
        self.errors and self.warnings lists.

        Args:
            data: Data to validate
            **kwargs: Additional validation parameters
        """
        pass

    def add_error(self, message: str) -> None:
        """Add validation error"""
        self.errors.append(message)
        self.log_error(f"✗ {message}")

    def add_warning(self, message: str) -> None:
        """Add validation warning"""
        self.warnings.append(message)
        self.logger.warning(f"⚠️ {message}")

    def clear(self) -> None:
        """Clear errors and warnings"""
        self.errors.clear()
        self.warnings.clear()

    def log_error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


class AnalysisEngine(ABC):
    """Base class for analysis engines (MCDA, LCOE, etc.)"""

    def __init__(self, engine_name: str) -> None:
        """
        Initialize analysis engine.

        Args:
            engine_name: Name of engine
        """
        self.engine_name = engine_name
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._validated = False

    def validate_inputs(self, **inputs: Any) -> bool:
        """
        Validate all inputs before analysis. Must be overridden by subclasses.

        Args:
            **inputs: Input parameters to validate

        Returns:
            True if inputs are valid, False otherwise
        """
        try:
            self._validate_inputs_impl(**inputs)
            self._validated = True
            self.logger.info(f"[{self.engine_name}] Inputs validated successfully")
            return True
        except ValidationError as e:
            self.logger.error(f"[{self.engine_name}] Validation failed: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"[{self.engine_name}] Unexpected error during validation: {str(e)}")
            return False

    @abstractmethod
    def _validate_inputs_impl(self, **inputs: Any) -> None:
        """
        Implement input validation. Raise ValidationError if validation fails.

        Args:
            **inputs: Input parameters to validate

        Raises:
            ValidationError: If validation fails
        """
        pass

    def run(self, **parameters: Any) -> AnalysisResult:
        """
        Run analysis with given parameters.

        Args:
            **parameters: Analysis parameters

        Returns:
            AnalysisResult with analysis output
        """
        if not self._validated:
            self.logger.warning(f"[{self.engine_name}] Running without validation")

        try:
            result = self._run_impl(**parameters)
            self.logger.info(f"[{self.engine_name}] Analysis completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"[{self.engine_name}] Analysis failed: {str(e)}")
            return AnalysisResult(success=False, data=None, error=str(e))

    @abstractmethod
    def _run_impl(self, **parameters: Any) -> AnalysisResult:
        """
        Implement analysis logic.

        Args:
            **parameters: Analysis parameters

        Returns:
            AnalysisResult object
        """
        pass


class RasterProcessor(ABC):
    """Base class for raster data processing components"""

    def __init__(self, processor_name: str) -> None:
        """
        Initialize raster processor.

        Args:
            processor_name: Name of processor
        """
        self.processor_name = processor_name
        self.logger = get_logger(self.__class__.__name__)

    def process(self, data: Any, **kwargs: Any) -> Any:
        """
        Process raster data.

        Args:
            data: Raster data to process
            **kwargs: Processing parameters

        Returns:
            Processed raster data
        """
        try:
            self.logger.info(f"[{self.processor_name}] Processing raster data...")
            result = self._process_impl(data, **kwargs)
            self.logger.info(f"[{self.processor_name}] Processing completed")
            return result
        except Exception as e:
            self.logger.error(f"[{self.processor_name}] Processing failed: {str(e)}")
            raise

    @abstractmethod
    def _process_impl(self, data: Any, **kwargs: Any) -> Any:
        """
        Implement raster processing logic.

        Args:
            data: Raster data
            **kwargs: Processing parameters

        Returns:
            Processed data
        """
        pass
