"""Compatibility raster utilities used by archived tests.

Provides a simple `normalize` function that accepts either a single
NumPy array or a mapping of arrays and returns normalized results.
"""
from typing import Dict, Any
import numpy as np


def _normalize_array(arr: np.ndarray) -> np.ndarray:
    if arr is None:
        raise ValueError("Array is None")
    a = np.asarray(arr, dtype=float)
    mask = np.isfinite(a)
    if not mask.any():
        return np.full_like(a, np.nan, dtype=float)
    valid = a[mask]
    vmin = valid.min()
    vmax = valid.max()
    if vmin == vmax:
        return np.full_like(a, 0.5, dtype=float)
    out = np.full_like(a, np.nan, dtype=float)
    out[mask] = (a[mask] - vmin) / (vmax - vmin)
    return out


def normalize(data: Any):
    """Normalize a single array or a dict of arrays to range [0,1].

    Args:
        data: np.ndarray or mapping of name->np.ndarray

    Returns:
        Normalized array or dict of normalized arrays
    """
    if isinstance(data, dict):
        return {k: _normalize_array(v) for k, v in data.items()}
    else:
        return _normalize_array(data)


__all__ = ["normalize"]
