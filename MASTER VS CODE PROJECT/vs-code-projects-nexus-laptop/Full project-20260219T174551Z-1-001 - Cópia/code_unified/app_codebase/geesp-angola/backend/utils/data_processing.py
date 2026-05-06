"""
GEESP-Angola: Unified Data Processing Module
Consolidates all array, raster, and data transformation operations into single source of truth
"""

from typing import Union, Tuple, Dict, Optional, Any, Callable
from functools import wraps
from pathlib import Path
import threading
import numpy as np
from numpy.typing import NDArray
import warnings

from utils.logging import setup_logging
from utils.exceptions import ValidationError

logger = setup_logging(__name__)

# Global cache for expensive operations
_PROCESSING_CACHE: Dict[str, Any] = {}
_CACHE_MAX_SIZE = 1000
_CACHE_LOCK = threading.Lock()


# ============================================================================
# CACHING UTILITIES
# ============================================================================


def memoize_operation(func: Callable) -> Callable:
    """
    Memoize expensive data processing operations.
    
    Decorator that caches function results based on arguments.
    Automatically clears cache when it exceeds MAX_SIZE.
    
    Args:
        func: Function to memoize
        
    Returns:
        Wrapped function with caching
        
    Example:
        @memoize_operation
        def expensive_calculation(data):
            return process(data)
    """
    cache: Dict[str, Any] = {}
    lock = threading.Lock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from function name and arguments
        # Use id() for unhashable types (e.g., numpy arrays)
        try:
            key = f"{func.__name__}_{hash((args, tuple(sorted(kwargs.items()))))}"
        except TypeError:
            hashable_args = tuple(id(a) if not isinstance(a, (int, float, str, bool, tuple)) else a for a in args)
            hashable_kwargs = tuple((k, id(v) if not isinstance(v, (int, float, str, bool, tuple)) else v) for k, v in sorted(kwargs.items()))
            key = f"{func.__name__}_{hash((hashable_args, hashable_kwargs))}"
        
        with lock:
            if key in cache:
                logger.debug(f"Cache hit for {func.__name__}")
                return cache[key]
        
        # Compute result outside lock to avoid holding it during expensive ops
        result = func(*args, **kwargs)
        
        with lock:
            # Manage cache size
            if len(cache) >= _CACHE_MAX_SIZE:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
                logger.debug(f"Cache evicted oldest entry for {func.__name__}")
            
            cache[key] = result
        
        return result
    
    return wrapper


def clear_operation_cache() -> None:
    """Clear all operation caches."""
    global _PROCESSING_CACHE
    with _CACHE_LOCK:
        _PROCESSING_CACHE.clear()
    logger.info("All processing caches cleared")


# ============================================================================
# ARRAY VALIDATION & CONVERSION
# ============================================================================


def ensure_numpy_array(data: Any) -> NDArray:
    """
    Ensure input is a numpy array with proper dtype.
    
    Args:
        data: Input data (list, array, tuple, scalar, etc.)
        
    Returns:
        Numpy array
        
    Raises:
        ValidationError: If conversion fails
        
    Example:
        >>> arr = ensure_numpy_array([1, 2, 3])
        >>> arr.dtype
        dtype('int64')
    """
    try:
        if isinstance(data, np.ndarray):
            return data
        
        data = np.asarray(data, dtype=float)
        
        if data.ndim == 0:
            logger.warning("Input is scalar, returning as 0-dimensional array")
        
        return data
    except (TypeError, ValueError) as e:
        msg = f"Failed to convert to numpy array: {str(e)}"
        logger.error(msg)
        raise ValidationError(msg)


def validate_array_shape(
    data: NDArray, 
    expected_shape: Optional[Tuple[int, ...]] = None,
    allow_empty: bool = False
) -> bool:
    """
    Validate array shape and dimensions.
    
    Args:
        data: Array to validate
        expected_shape: Expected shape tuple (e.g., (100, 100))
        allow_empty: If False, reject empty arrays
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If validation fails
        
    Example:
        >>> arr = np.zeros((10, 10))
        >>> validate_array_shape(arr, expected_shape=(10, 10))
        True
    """
    if not isinstance(data, np.ndarray):
        raise ValidationError(f"Expected numpy array, got {type(data)}")
    
    if data.size == 0 and not allow_empty:
        raise ValidationError("Array is empty")
    
    if data.ndim == 0:
        raise ValidationError("Array is scalar (0-dimensional)")
    
    if expected_shape is not None and data.shape != expected_shape:
        raise ValidationError(
            f"Shape mismatch: expected {expected_shape}, got {data.shape}"
        )
    
    return True


def get_valid_data_mask(data: NDArray) -> NDArray:
    """
    Get boolean mask of valid (finite) data points.
    
    Args:
        data: Input array with potential NaN/Inf values
        
    Returns:
        Boolean array where True = valid, False = invalid
        
    Example:
        >>> data = np.array([1.0, np.nan, 3.0, np.inf])
        >>> mask = get_valid_data_mask(data)
        >>> mask
        array([ True, False,  True, False])
    """
    try:
        return np.isfinite(data)
    except Exception as e:
        logger.error(f"Failed to create valid data mask: {str(e)}")
        return np.ones_like(data, dtype=bool)


def get_statistics(
    data: NDArray, 
    include_nan: bool = False
) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for array.
    
    Args:
        data: Input array
        include_nan: If True, include NaN count in stats
        
    Returns:
        Dictionary with min, max, mean, median, std
        
    Example:
        >>> data = np.array([1, 2, 3, 4, 5])
        >>> stats = get_statistics(data)
        >>> stats['mean']
        3.0
    """
    valid_mask = get_valid_data_mask(data)
    valid_data = data[valid_mask]
    
    if len(valid_data) == 0:
        logger.warning("No valid data found for statistics")
        return {
            'min': np.nan,
            'max': np.nan,
            'mean': np.nan,
            'median': np.nan,
            'std': np.nan,
            'count': 0,
            'valid_count': 0
        }
    
    stats = {
        'min': float(np.nanmin(valid_data)),
        'max': float(np.nanmax(valid_data)),
        'mean': float(np.nanmean(valid_data)),
        'median': float(np.nanmedian(valid_data)),
        'std': float(np.nanstd(valid_data)),
        'count': data.size,
        'valid_count': np.sum(valid_mask)
    }
    
    if include_nan:
        invalid_count = data.size - stats['valid_count']
        stats['invalid_count'] = invalid_count
        stats['invalid_percent'] = 100.0 * invalid_count / data.size
    
    return stats


# ============================================================================
# ARRAY TRANSFORMATIONS
# ============================================================================


@memoize_operation
def standardize_array(
    data: NDArray,
    epsilon: float = 1e-10
) -> NDArray:
    """
    Standardize array to mean=0, std=1 (z-score normalization).
    
    Args:
        data: Input array
        epsilon: Small value to prevent division by zero
        
    Returns:
        Standardized array
        
    Example:
        >>> data = np.array([10, 20, 30])
        >>> std = standardize_array(data)
        >>> std.mean()  # Approximately 0
    """
    try:
        mean = np.nanmean(data)
        std = np.nanstd(data)
        
        if std < epsilon:
            logger.warning("Array has very small standard deviation, returning zeros")
            return np.zeros_like(data)
        
        return (data - mean) / (std + epsilon)
    except Exception as e:
        logger.error(f"Standardization failed: {str(e)}")
        return data


@memoize_operation
def clip_array(
    data: NDArray,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None
) -> NDArray:
    """
    Clip array values to specified range, preserving NaN/Inf.
    
    Args:
        data: Input array
        min_val: Minimum value (None = no minimum)
        max_val: Maximum value (None = no maximum)
        
    Returns:
        Clipped array with NaN/Inf preserved
        
    Example:
        >>> data = np.array([-5, 0, 5, 10])
        >>> clipped = clip_array(data, min_val=0, max_val=5)
        >>> clipped
        array([0, 0, 5, 5])
    """
    valid_mask = get_valid_data_mask(data)
    result = data.copy()
    
    if min_val is not None:
        result[valid_mask] = np.maximum(result[valid_mask], min_val)
    
    if max_val is not None:
        result[valid_mask] = np.minimum(result[valid_mask], max_val)
    
    return result


# ============================================================================
# BATCH OPERATIONS
# ============================================================================


def process_raster_batch(
    rasters: Dict[str, NDArray],
    processor: Callable[[NDArray], NDArray],
    skip_invalid: bool = True
) -> Dict[str, NDArray]:
    """
    Apply processor function to batch of rasters.
    
    Args:
        rasters: Dictionary mapping names to raster arrays
        processor: Function to apply to each raster
        skip_invalid: If True, skip rasters with errors
        
    Returns:
        Dictionary with processed rasters
        
    Example:
        >>> rasters = {'solar': arr1, 'wind': arr2}
        >>> normalized = process_raster_batch(
        ...     rasters, 
        ...     processor=lambda x: (x - x.min()) / (x.max() - x.min())
        ... )
    """
    results = {}
    errors = {}
    
    for name, raster in rasters.items():
        try:
            results[name] = processor(raster)
        except Exception as e:
            msg = f"Error processing raster '{name}': {str(e)}"
            if skip_invalid:
                logger.warning(msg)
                errors[name] = str(e)
            else:
                logger.error(msg)
                raise ValidationError(msg)
    
    if errors:
        logger.info(f"Skipped {len(errors)} rasters with errors")
    
    return results


def merge_rasters(
    rasters: Dict[str, NDArray],
    merge_method: str = "stack"
) -> NDArray:
    """
    Merge multiple rasters into single array.
    
    Args:
        rasters: Dictionary mapping names to raster arrays
        merge_method: 'stack' (3D), 'mean' (average), 'max' (maximum)
        
    Returns:
        Merged raster array
        
    Example:
        >>> rasters = {'layer1': arr1, 'layer2': arr2}
        >>> merged = merge_rasters(rasters, merge_method='mean')
    """
    if not rasters:
        raise ValidationError("No rasters provided")
    
    try:
        arrays = [arr for arr in rasters.values()]
        
        if merge_method == "stack":
            return np.stack(arrays, axis=0)
        elif merge_method == "mean":
            return np.nanmean(arrays, axis=0)
        elif merge_method == "max":
            return np.nanmax(arrays, axis=0)
        else:
            raise ValidationError(f"Unknown merge method: {merge_method}")
    except Exception as e:
        msg = f"Failed to merge rasters: {str(e)}"
        logger.error(msg)
        raise ValidationError(msg)


# ============================================================================
# REPORT GENERATION
# ============================================================================


def generate_processing_report(
    operation: str,
    input_shape: Tuple[int, ...],
    output_shape: Tuple[int, ...],
    processing_time: float,
    success: bool = True,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate processing operation report.
    
    Args:
        operation: Name of operation performed
        input_shape: Shape of input data
        output_shape: Shape of output data
        processing_time: Time taken in seconds
        success: Whether operation succeeded
        notes: Optional notes/warnings
        
    Returns:
        Report dictionary
        
    Example:
        >>> report = generate_processing_report(
        ...     operation="normalize",
        ...     input_shape=(100, 100),
        ...     output_shape=(100, 100),
        ...     processing_time=0.123
        ... )
    """
    return {
        'operation': operation,
        'input_shape': input_shape,
        'output_shape': output_shape,
        'processing_time': processing_time,
        'success': success,
        'notes': notes,
        'timestamp': np.datetime64('now')
    }


# ============================================================================
# LEGACY COMPATIBILITY WRAPPERS
# ============================================================================


def save_raster(array: NDArray, filepath: Union[str, Path]) -> None:
    """
    Save raster to file (legacy compatibility).
    
    **Deprecated:** Use rasterio or terrain-specific libraries.
    Currently saves as .npy binary format.
    
    Args:
        array: Raster array
        filepath: Output file path
    """
    filepath = Path(filepath)
    try:
        np.save(filepath, array)
        logger.info(f"Raster saved to {filepath}")
    except Exception as e:
        msg = f"Failed to save raster: {str(e)}"
        logger.error(msg)
        raise ValidationError(msg)


def load_raster(filepath: Union[str, Path]) -> Tuple[NDArray, Optional[Dict]]:
    """
    Load raster from file (legacy compatibility).
    
    **Deprecated:** Use rasterio or terrain-specific libraries.
    Currently loads .npy binary format.
    
    Args:
        filepath: Input file path
        
    Returns:
        Tuple of (array, metadata) - metadata is None for .npy files
    """
    filepath = Path(filepath)
    try:
        array = np.load(filepath)
        logger.info(f"Raster loaded from {filepath}")
        return array, None
    except Exception as e:
        msg = f"Failed to load raster: {str(e)}"
        logger.error(msg)
        raise ValidationError(msg)
