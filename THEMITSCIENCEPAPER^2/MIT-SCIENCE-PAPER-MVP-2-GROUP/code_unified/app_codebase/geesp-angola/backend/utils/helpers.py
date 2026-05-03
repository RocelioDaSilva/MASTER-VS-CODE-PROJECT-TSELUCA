"""
GEESP-Angola: Unified Utilities and Helpers Module

Consolidates utility functions from core_utils.py and import_helpers.py:
- Array manipulation and validation
- File and path operations  
- Import handling and module loading
- String formatting utilities

This unified module provides a single source of truth for common utilities
used across GEESP-Angola backend modules.
"""

import sys
import importlib
import importlib.util
import logging
from pathlib import Path
from typing import Union, Tuple, Dict, Optional, Any
from types import ModuleType as Module
from numpy.typing import NDArray

import numpy as np

# Import exceptions and constants
try:
    from .constants import TechnicalConstants
    from .exceptions import ValidationError, retry_on_exception
except ImportError:
    # Fallback for testing/standalone usage
    TechnicalConstants = None
    ValidationError = ValueError
    retry_on_exception = None

logger = logging.getLogger(__name__)


# ============================================================================
# IMPORT UTILITIES (from import_helpers.py)
# ============================================================================


def setup_project_paths() -> None:
    """
    Add project root and submodules to sys.path
    Should be called once at application startup
    """
    project_root = Path(__file__).parent.parent
    paths_to_add = [
        str(project_root),
        str(project_root / "scripts"),
        str(project_root / "utils"),
        str(project_root / "dashboard"),
        str(project_root / "models"),
        str(project_root / "integration"),
    ]

    for path_str in paths_to_add:
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
            logger.debug(f"Added to sys.path: {path_str}")


def safe_import(module_name: str, package: Optional[str] = None, fallback: bool = True) -> Optional[Module]:
    """
    Safely import a module with fallback support

    Args:
        module_name: Name of module to import
        package: Package context for relative imports
        fallback: If True, logs warning instead of raising on ImportError

    Returns:
        Imported module or None if import fails and fallback=True

    Example:
        >>> config_loader = safe_import("config_loader")
        >>> if config_loader:
        ...     config = config_loader.load_config()
    """
    try:
        if package:
            return importlib.import_module(f".{module_name}", package=package)
        else:
            return importlib.import_module(module_name)
    except ImportError as e:
        if fallback:
            logger.warning(f"Failed to import {module_name}: {e}")
            return None
        else:
            logger.error(f"Failed to import {module_name}: {e}")
            raise


def conditional_import(
    module_name: str,
    optional: bool = False,
    description: str = ""
) -> Optional[Module]:
    """
    Import with better error handling for optional dependencies

    Args:
        module_name: Module to import
        optional: If True, treat ImportError as non-fatal
        description: Description of what module is used for

    Returns:
        Module or None

    Example:
        >>> ee = conditional_import("ee", optional=True, description="Google Earth Engine")
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        msg = f"Could not import {module_name}"
        if description:
            msg += f" ({description})"

        if optional:
            logger.warning(f"Could not import {module_name} ({description}). Some features may be unavailable: {e}")
            return None
        else:
            logger.error(f"Could not import {module_name}: {e}")
            raise


def load_module_from_path(file_path: str, module_name: Optional[str] = None) -> Module:
    """
    Load a Python module from an arbitrary file path

    Args:
        file_path: Path to Python file
        module_name: Name to use for module (default: filename without .py)

    Returns:
        Loaded module

    Example:
        >>> custom_module = load_module_from_path("/path/to/custom.py", "custom")
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Module file not found: {file_path}")

    if module_name is None:
        module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    logger.debug(f"Loaded module {module_name} from {file_path}")
    return module


def import_or_mock(
    module_name: str,
    mock_attributes: Optional[dict] = None
) -> Module:
    """
    Import a module or return mock with specified attributes (useful for testing)

    Args:
        module_name: Module to import
        mock_attributes: Attributes to add to mock object if import fails

    Returns:
        Module or mock object

    Example:
        >>> ee = import_or_mock("ee", mock_attributes={"Initialize": lambda: None})
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        logger.warning(f"Importing mock for {module_name}")

        # Create a simple mock
        class MockModule:
            pass

        mock = MockModule()
        if mock_attributes:
            for key, value in mock_attributes.items():
                setattr(mock, key, value)

        return mock


# ============================================================================
# ARRAY UTILITIES (from core_utils.py)
# ============================================================================


def ensure_numpy_array(data: Any) -> NDArray:
    """
    Ensure input is a numpy array.

    Args:
        data: Input data (list, array, etc.)

    Returns:
        Numpy array

    Raises:
        ValidationError: If conversion fails
    """
    try:
        if not isinstance(data, np.ndarray):
            data = np.asarray(data)
        return data
    except Exception as e:
        raise ValidationError(f"Failed to convert to numpy array: {str(e)}")


def validate_array_shape(
    data: NDArray, expected_shape: Optional[Tuple[int, ...]] = None
) -> bool:
    """
    Validate array shape.

    Args:
        data: Array to validate
        expected_shape: Expected shape tuple

    Returns:
        True if valid

    Raises:
        ValidationError: If shape is invalid
    """
    if data.ndim == 0 or data.size == 0:
        raise ValidationError("Array is empty or scalar")

    if expected_shape is not None and data.shape != expected_shape:
        raise ValidationError(
            f"Shape mismatch: expected {expected_shape}, got {data.shape}"
        )

    return True


def get_valid_data_mask(data: NDArray) -> NDArray:
    """
    Get mask of valid (finite) data points.

    Args:
        data: Array with potential NaN/Inf values

    Returns:
        Boolean mask of valid values
    """
    return np.isfinite(data)


def get_data_statistics(data: NDArray) -> Dict[str, float]:
    """
    Calculate data statistics for finite values only.

    Args:
        data: Input array

    Returns:
        Dictionary with statistics

    Raises:
        ValidationError: If no valid data found
    """
    valid_mask = get_valid_data_mask(data)
    if not valid_mask.any():
        raise ValidationError("No valid (finite) data found in array")

    valid_data = data[valid_mask]

    return {
        "count": int(valid_mask.sum()),
        "min": float(np.min(valid_data)),
        "max": float(np.max(valid_data)),
        "mean": float(np.mean(valid_data)),
        "median": float(np.median(valid_data)),
        "std": float(np.std(valid_data)),
        "missing_percentage": float((~valid_mask).sum() / data.size * 100),
    }


def normalize_array(
    data: NDArray, min_val: float = None, max_val: float = None
) -> NDArray:
    """
    Normalize array to specified range using min-max scaling.

    Args:
        data: Input array
        min_val: Target minimum (default from TechnicalConstants)
        max_val: Target maximum (default from TechnicalConstants)

    Returns:
        Normalized array

    Raises:
        ValidationError: If normalization fails
    """
    if min_val is None:
        min_val = getattr(TechnicalConstants, 'NORMALIZATION_MIN_DEFAULT', 0.0) if TechnicalConstants else 0.0
    if max_val is None:
        max_val = getattr(TechnicalConstants, 'NORMALIZATION_MAX_DEFAULT', 1.0) if TechnicalConstants else 1.0
        
    if data is None:
        raise ValidationError("data cannot be None")

    valid_mask = get_valid_data_mask(data)
    if not valid_mask.any():
        raise ValidationError("No valid data to normalize")

    valid_data = data[valid_mask]
    data_min = np.min(valid_data)
    data_max = np.max(valid_data)

    if data_min == data_max:
        # All values are the same, fill with midpoint
        normalized = np.full_like(data, (min_val + max_val) / 2, dtype=float)
    else:
        # Min-max normalization formula
        normalized = np.full_like(data, np.nan, dtype=float)
        normalized[valid_mask] = (
            min_val + (valid_data - data_min) / (data_max - data_min) * (max_val - min_val)
        )

    return normalized


def clip_array(data: NDArray, min_val: float, max_val: float) -> NDArray:
    """
    Clip array values to specified range.

    Args:
        data: Input array
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Clipped array
    """
    return np.clip(data, min_val, max_val)


def apply_threshold(data: NDArray, threshold: float) -> NDArray:
    """
    Apply threshold to array (values >= threshold = 1, else 0).

    Args:
        data: Input array
        threshold: Threshold value

    Returns:
        Binary array (1 where >= threshold, 0 elsewhere)
    """
    return (data >= threshold).astype(float)


# ============================================================================
# FILE & PATH UTILITIES (from core_utils.py)
# ============================================================================


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, creating if necessary.

    Args:
        path: Directory path

    Returns:
        Path object

    Raises:
        ValidationError: If directory cannot be created
    """
    try:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise ValidationError(f"Cannot create directory {path}: {str(e)}")


def file_exists(path: Union[str, Path]) -> bool:
    """Check if file exists"""
    return Path(path).exists()


def get_file_size_mb(path: Union[str, Path]) -> float:
    """Get file size in MB"""
    return Path(path).stat().st_size / (1024 * 1024)


def safe_load_npy(filepath: Union[str, Path]) -> Optional[NDArray]:
    """
    Safely load numpy array from .npy file.

    Args:
        filepath: Path to .npy file

    Returns:
        Loaded array or None if fails

    Raises:
        ValidationError: If file cannot be loaded
    """
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return np.load(filepath)
    except Exception as e:
        raise ValidationError(f"Failed to load {filepath}: {str(e)}")


def safe_save_npy(
    data: NDArray, filepath: Union[str, Path], overwrite: bool = True
) -> Path:
    """
    Safely save numpy array to .npy file.

    Args:
        data: Array to save
        filepath: Destination path
        overwrite: Whether to overwrite existing file

    Returns:
        Path to saved file

    Raises:
        ValidationError: If save fails
    """
    try:
        filepath = Path(filepath)
        if filepath.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {filepath}")

        filepath.parent.mkdir(parents=True, exist_ok=True)
        np.save(filepath, data)
        logger.info(f"Saved array to {filepath} ({data.nbytes / 1024 / 1024:.1f} MB)")
        return filepath
    except Exception as e:
        raise ValidationError(f"Failed to save {filepath}: {str(e)}")


# ============================================================================
# FORMAT & STRING UTILITIES (from core_utils.py)
# ============================================================================


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    return f"{value:.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format as percentage"""
    return f"{value * 100:.{decimals}f}%"


def format_bytes(bytes_count: int) -> str:
    """Format bytes as human-readable string"""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} TB"


# Auto-setup paths on module import
setup_project_paths()
