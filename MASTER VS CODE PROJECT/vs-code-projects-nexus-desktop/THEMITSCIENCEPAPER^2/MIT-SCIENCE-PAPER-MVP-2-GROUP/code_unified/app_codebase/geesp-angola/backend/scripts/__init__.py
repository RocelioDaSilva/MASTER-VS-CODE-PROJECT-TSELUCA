"""
GEESP-Angola Scripts Package
Central hub for all analysis modules with unified infrastructure

**Phase 7 Consolidation (Code Streamlining)**:
- Unified normalization in raster_utils.normalize() (was: normalize_array, batch_normalize_arrays, normalize_raster_minmax)
- Unified weighted overlay in performance.compute_weighted_overlay() (was duplicated in tests)
- Consolidated caching strategy (global cache in raster_utils, managed via unified normalize function)
- Instance cache removed from MCDAnalyzer (use global cache via cache_key parameter)

Backward Compatibility:
- All old functions maintained as wrappers for existing code
- New code should use unified interfaces: normalize(), compute_weighted_overlay()
- Deprecation warnings show recommended alternatives
"""

# ============================================================================
# CORE INFRASTRUCTURE - Always available
# ============================================================================

from utils.logging import get_logger, setup_logging, LoggingManager
from utils.exceptions import (
    GEESPError,
    ValidationError,
    ConfigurationError,
    DataError,
    GeoProcessingError,
    MCDAError,
    LCOECalculationError,
    GEEIntegrationError,
    TimeoutError,
    handle_exceptions,
)
from .base import Component, Validator, AnalysisEngine, RasterProcessor, AnalysisResult
from utils.helpers import (
    ensure_numpy_array,
    validate_array_shape,
    normalize_array,
    get_data_statistics,
    ensure_directory,
    safe_load_npy,
    safe_save_npy,
    file_exists,
)

# ============================================================================
# ANALYSIS MODULES - Conditionally loaded
# ============================================================================

from importlib import import_module
import logging

logger = get_logger(__name__)

__version__ = "1.0.0"
__author__ = "GEESP Team"

# Define all available modules
_analysis_modules = [
    "config_loader",
    "performance",
    "validators",
    "raster_utils",
    "map_utils",
    "gee_extraction",
    "mcda_analysis",
    "lcoe_calculator",
    "generate_maps_simple",
    "generate_maps",
    "api",
]

# Lazily import analysis modules (non-critical if unavailable)
for _module_name in _analysis_modules:
    try:
        globals()[_module_name] = import_module(f".{_module_name}", package=__name__)
    except Exception as e:
        # Do not set the name to None - leave it unset so importlib can
        # import the submodule directly later or tests can import it
        logger.debug(f"Optional module scripts.{_module_name} unavailable at init: {e}")

# ============================================================================
# PACKAGE EXPORTS
# ============================================================================

__all__ = [
    # Core infrastructure
    "get_logger",
    "setup_logging",
    "LoggingManager",
    "GeespException",
    "ValidationError",
    "ConfigurationError",
    "DataError",
    "RasterError",
    "MCDAError",
    "LCOEError",
    "GEEError",
    "TimeoutError",
    "handle_exceptions",
    "validate_arguments",
    "error_context",
    "Component",
    "Validator",
    "AnalysisEngine",
    "RasterProcessor",
    "AnalysisResult",
    # Constants
    "ANGOLA_BOUNDS",
    "HUILA_BOUNDS",
    "CRS_UTM33S",
    "CRS_WGS84",
    "SAATY_SCALE",
    "LCOE_MIN",
    "LCOE_MAX",
    "TECHNOLOGIES",
    "COMMUNITIES",
    # Utilities
    "ensure_numpy_array",
    "validate_array_shape",
    "normalize_array",
    "get_data_statistics",
    "ensure_directory",
    "safe_load_npy",
    "safe_save_npy",
    "file_exists",
    "weighted_sum",
    # Analysis modules
    "config_loader",
    "performance",
    "validators",
    "raster_utils",
    "map_utils",
    "gee_extraction",
    "mcda_analysis",
    "lcoe_calculator",
    "generate_maps_simple",
    "generate_maps",
    "api",
]


# Backwards compatibility helpers: expose a few common symbols to builtins
try:
    import builtins as _builtins
    # LCOE helpers
    if "lcoe_calculator" in globals() and globals()["lcoe_calculator"] is not None:
        _builtins.SolarParameters = getattr(globals()["lcoe_calculator"], "SolarParameters", None)
        _builtins.LCOECalculator = getattr(globals()["lcoe_calculator"], "LCOECalculator", None)
    # MCDA aliases
    if "mcda_analysis" in globals() and globals()["mcda_analysis"] is not None:
        _builtins.MCDAAnalysis = getattr(globals()["mcda_analysis"], "MCDAAnalysis", None)
        _builtins.MCDAnalyzer = getattr(globals()["mcda_analysis"], "MCDAnalyzer", None)
except Exception:
    pass

