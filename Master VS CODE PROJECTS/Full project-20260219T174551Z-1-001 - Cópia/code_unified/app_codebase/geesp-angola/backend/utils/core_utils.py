"""Compatibility shim for legacy `utils.core_utils` module.

Exports `get_data_statistics` from the consolidated `utils.helpers`.
"""
from .helpers import get_data_statistics, normalize_array

__all__ = ["get_data_statistics", "normalize_array"]
