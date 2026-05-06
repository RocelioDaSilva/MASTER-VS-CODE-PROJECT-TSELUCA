"""Compatibility validators shim for archived tests.

This module implements a small set of validation helpers that archived
tests expect under `scripts.validators`. Functions are intentionally
minimal but strict enough to catch obvious misuse in tests.
"""
from typing import Iterable, Sequence
import numpy as np


def _to_array(x):
    if isinstance(x, np.ndarray):
        return x
    try:
        return np.asarray(x)
    except Exception:
        raise ValueError("numpy")


def validate_solar_irradiance(arr) -> bool:
    if arr is None:
        raise ValueError("None")
    a = _to_array(arr)
    if a.size == 0:
        raise ValueError("empty")
    if np.isnan(a).all():
        raise ValueError("valid")
    return True


def validate_population(arr) -> bool:
    if arr is None:
        raise ValueError("None")
    a = _to_array(arr)
    if a.size == 0:
        raise ValueError("empty")
    if np.isnan(a).all():
        raise ValueError("valid")
    if (a < 0).any():
        raise ValueError("negative")
    return True


def validate_weights(w: Sequence[float]) -> bool:
    if not hasattr(w, "items") and not isinstance(w, dict):
        try:
            _ = list(w)
        except Exception:
            raise ValueError("numeric")

    if isinstance(w, dict):
        if len(w) == 0:
            raise ValueError("empty")
        vals_list = list(w.values())
        # Reject string types even if they look numeric
        if any(isinstance(x, str) for x in vals_list):
            raise ValueError("numeric")
        try:
            vals = np.asarray(vals_list, dtype=float)
        except Exception:
            raise ValueError("numeric")
    else:
        try:
            # If it's an iterable of strings, reject
            if any(isinstance(x, str) for x in w):
                raise ValueError("numeric")
        except Exception:
            pass
        try:
            vals = np.asarray(w, dtype=float)
        except Exception:
            raise ValueError("numeric")

    if vals.ndim != 1:
        raise ValueError("1D")
    if (vals < 0).any() or (vals > 1).any():
        raise ValueError("outside")
    s = float(vals.sum())
    if not np.isclose(s, 1.0, atol=1e-6):
        raise ValueError("sum to")
    return True


def validate_weight_vector(vec) -> bool:
    if not isinstance(vec, np.ndarray):
        raise ValueError("numpy")
    if vec.ndim != 1:
        raise ValueError("1D")
    if (vec < 0).any() or (vec > 1).any():
        raise ValueError("outside")
    s = float(vec.sum())
    if not np.isclose(s, 1.0, atol=1e-6):
        raise ValueError("sum to")
    return True


def validate_raster_shape(arr, expected_shape: Iterable[int]) -> bool:
    if not isinstance(arr, np.ndarray):
        raise ValueError("numpy")
    a = arr
    if a.ndim != 2:
        raise ValueError("2D")
    if tuple(a.shape) != tuple(int(x) for x in expected_shape):
        raise ValueError(f"Raster shape {a.shape} doesn't match expected {tuple(expected_shape)}")
    return True


def validate_is_probability_array(arr) -> bool:
    a = _to_array(arr)
    if (a < 0).any() or (a > 1).any():
        raise ValueError("outside")
    return True


def validate_ndvi(arr) -> bool:
    a = _to_array(arr)
    if a.size == 0:
        raise ValueError("empty")
    if (a < -1).any():
        raise ValueError("below -1")
    if (a > 1).any():
        raise ValueError("above 1")
    return True


def validate_distance(arr) -> bool:
    a = _to_array(arr)
    if a.size == 0:
        raise ValueError("empty")
    if (a < 0).any():
        raise ValueError("negative")
    return True


def validate_slope(arr) -> bool:
    a = _to_array(arr)
    if a.size == 0:
        raise ValueError("empty")
    if a.ndim != 2:
        raise ValueError("2D")
    if (a < 0).any() or (a > 90).any():
        raise ValueError("outside")
    return True


def validate_capacity_mw(val) -> bool:
    # Reject string values that look numeric to enforce proper types
    if isinstance(val, str):
        raise ValueError("numeric")
    try:
        v = float(val)
    except Exception:
        raise ValueError("numeric")
    if not (0.1 <= v <= 500.0):
        raise ValueError("outside")
    return True


def validate_irradiance_kwh(val) -> bool:
    try:
        v = float(val)
    except Exception:
        raise ValueError("numeric")
    if not (200.0 <= v <= 3500.0):
        raise ValueError("outside")
    return True


def validate_discount_rate(val) -> bool:
    try:
        v = float(val)
    except Exception:
        raise ValueError("numeric")
    if not (0.0 <= v <= 100.0):
        raise ValueError("outside")
    return True


def validate_project_lifetime(val) -> bool:
    if not isinstance(val, int):
        raise ValueError("integer")
    if not (5 <= val <= 50):
        raise ValueError("outside")
    return True


def validate_all_inputs(
    solar, population, distance, slope, ndvi,
    weights, capacity_mw, irradiance_kwh, discount_rate
):
    try:
        validate_solar_irradiance(solar)
        validate_population(population)
        validate_distance(distance)
        validate_slope(slope)
        validate_ndvi(ndvi)
        validate_weights(weights)
        validate_capacity_mw(capacity_mw)
        validate_irradiance_kwh(irradiance_kwh)
        validate_discount_rate(discount_rate)
    except Exception as e:
        raise ValueError(f"Validation failed: {e}")
    return True


__all__ = [
    "validate_solar_irradiance",
    "validate_population",
    "validate_weights",
    "validate_weight_vector",
    "validate_raster_shape",
    "validate_is_probability_array",
    "validate_ndvi",
    "validate_distance",
    "validate_slope",
    "validate_capacity_mw",
    "validate_irradiance_kwh",
    "validate_discount_rate",
    "validate_project_lifetime",
    "validate_all_inputs",
]
