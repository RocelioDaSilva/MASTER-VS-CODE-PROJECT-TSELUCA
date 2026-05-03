"""Compatibility shim exposing performance helpers under `scripts.performance`.

Re-exports selected functions from `utils.performance` used by archived tests.
"""
from utils.performance import normalize_array, vectorized_weighted_sum, benchmark_function

__all__ = ["normalize_array", "vectorized_weighted_sum", "benchmark_function"]
