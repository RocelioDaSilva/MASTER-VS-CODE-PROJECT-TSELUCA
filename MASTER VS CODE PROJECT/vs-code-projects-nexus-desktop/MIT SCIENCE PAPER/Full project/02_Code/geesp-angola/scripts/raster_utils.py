"""
Consolidated raster utilities to eliminate duplication.

Provides shared functions for normalization, validation, and manipulation.
Reduces code duplication across mcda_analysis, dashboard, and map generation modules.
"""

from typing import Dict, Optional, Tuple
import numpy as np
import logging

logger = logging.getLogger(__name__)


def normalize_raster_minmax(
    data: np.ndarray,
    minimum: float = 0.0,
    maximum: float = 1.0,
    name: str = "raster"
) -> np.ndarray:
    """
    Normalize raster using min-max scaling to [minimum, maximum].

    Handles NaN and inf values gracefully by preserving them in output.

    Args:
        data: Input numpy array (any shape)
        minimum: Target minimum value (default 0.0)
        maximum: Target maximum value (default 1.0)
        name: Name for logging

    Returns:
        Normalized array with scaling applied; NaN/inf preserved

    Raises:
        ValueError: If all values are NaN/inf
    """
    valid_mask = np.isfinite(data)

    if not valid_mask.any():
        logger.warning(f"⚠ {name}: No finite values found, returning zeros")
        return np.zeros_like(data, dtype=np.float32)

    arr_min = np.nanmin(data[valid_mask])
    arr_max = np.nanmax(data[valid_mask])

    if arr_max == arr_min:
        normalized = np.ones_like(data) * 0.5
    else:
        normalized = (data - arr_min) / (arr_max - arr_min)

    # Scale to [minimum, maximum]
    normalized = normalized * (maximum - minimum) + minimum

    # Preserve NaN/inf in output
    normalized[~valid_mask] = np.nan

    logger.info(f"✓ {name}: Normalized to [{minimum}, {maximum}]")
    return normalized.astype(np.float32)


def normalize_rasters_dict(
    rasters_dict: Dict[str, np.ndarray],
    minimum: float = 0.0,
    maximum: float = 1.0
) -> Dict[str, np.ndarray]:
    """
    Normalize all rasters in a dictionary.

    Args:
        rasters_dict: {name: raster_array}
        minimum: Target minimum
        maximum: Target maximum

    Returns:
        {name: normalized_raster}
    """
    normalized = {}
    for name, data in rasters_dict.items():
        try:
            normalized[name] = normalize_raster_minmax(data, minimum, maximum, name)
        except Exception as e:
            logger.error(f"✗ Failed to normalize {name}: {e}")
            normalized[name] = np.nan_to_num(data)
    return normalized
