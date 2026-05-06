"""Compatibility shim `scripts.utils` re-exporting a couple of utils used in tests.

Provides `save_raster`, `load_raster`, and `validate_raster` used by
archived tests that import `from scripts import utils`.
"""
from typing import Tuple, Optional
from pathlib import Path
import numpy as np
from utils.helpers import safe_save_npy, safe_load_npy, get_data_statistics


def save_raster(arr: np.ndarray, path: str) -> Path:
    p = Path(path)
    try:
        return safe_save_npy(arr, p)
    except Exception:
        # Fallback: plain numpy save
        p.parent.mkdir(parents=True, exist_ok=True)
        np.save(p, arr)
        return p


def load_raster(path: str) -> Tuple[np.ndarray, Optional[dict]]:
    p = Path(path)
    arr = safe_load_npy(p)
    # Old behaviour returned (array, metadata) where metadata might be None
    return arr, None


def validate_raster(arr: np.ndarray, name: str = "raster") -> dict:
    stats = get_data_statistics(arr)
    return {
        "total_pixels": int(arr.size),
        "valid_pixels": int(stats["count"]),
        "min": float(stats["min"]),
        "max": float(stats["max"]),
    }


__all__ = ["save_raster", "load_raster", "validate_raster"]
