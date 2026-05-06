"""
GEESP-Angola Utilities Package
==============================

Production-ready utilities for the GEESP-Angola project, providing:
- Centralized logging configuration
- Custom exception hierarchy
- Configuration management
- Data validation framework
- Data processing utilities
- Import helpers
- Consolidated constants

Usage:
    from utils.logging import setup_logging
    from utils.constants import MCDAConstants
    from utils.exceptions_config import ValidationError
    
    logger = setup_logging(__name__)
    
    if value < MCDAConstants.APTITUDE_UNSUITABLE_THRESHOLD:
        raise ValidationError(field="aptitude", expected="numeric", received=type(value).__name__)

For comprehensive integration guide, see: UTILITIES_INTEGRATION_GUIDE.md
For project status, see: UTILITIES_PHASE2_COMPLETION_SUMMARY.md
"""

__version__ = "1.0.0"
__author__ = "GEESP-Angola Development Team"

# Import all public utilities
try:
    from .logging import (
        setup_logging, get_logger,
        LoggingManager
    )
except ImportError:
    pass

try:
    from .exceptions import (
        GEESPError, GeespAnglolaException, ValidationError, DataError,
        ConfigurationError, GeoProcessingError, MCDAError,
        AHPError, LCOECalculationError, APIError, TimeoutError,
        ErrorSeverity, handle_exceptions, retry_on_exception
    )
except ImportError:
    pass

# Phase 5C: New Consolidated Modules (Code Merging)
try:
    from .data_processing import (
        ensure_numpy_array, validate_array_shape, get_valid_data_mask,
        get_statistics, standardize_array, clip_array, process_raster_batch,
        merge_rasters, memoize_operation, clear_operation_cache,
        save_raster, load_raster
    )
except ImportError:
    pass

try:
    from ..core.config import (
        ConfigManager, AppConfig, ProcessingConstants,
        get_config_value, set_config_value, get_data_dir,
        get_output_dir, get_cache_dir
    )
except ImportError:
    pass

try:
    from .validation import (
        validate_type, validate_range, validate_string, validate_not_empty,
        validate_inputs, safe_call, retry_with_backoff,
        handle_errors, suppress_errors, Result, operation_result,
        get_error_summary
    )
except ImportError:
    pass

try:
    from .constants import (
        MCDAConstants, GeoConstants, SolarConstants,
        PopulationConstants, InfrastructureConstants,
        LCOEConstants, EnvironmentalConstants, DataPathConstants,
        TechnicalConstants, UIConstants, MessageConstants
    )
except ImportError:
    pass

try:
    from .helpers import (
        setup_project_paths, safe_import, conditional_import,
        load_module_from_path, import_or_mock,
        ensure_numpy_array, validate_array_shape, normalize_array
    )
except ImportError:
    pass

try:
    from .config_utilities import (
        ConfigManager, ConfigSpec, EnvironmentConfig, create_config_manager
    )
except ImportError:
    pass

try:
    from .validation_utils import (
        Validator, RangeValidator, ChoiceValidator, RegexValidator,
        TypeValidator, CoordinateValidator, BoundingBoxValidator,
        MCDAWeightValidator, AHPRatioValidator, DataSourceValidator,
        ValidationSchema, validate_multiple, clean_numeric,
        clean_percentage, ensure_list,
        GEESP_ANGOLA_BBOX, GHI_VALIDATOR, LATITUDE_VALIDATOR,
        LONGITUDE_VALIDATOR, APTITUDE_SCORE_VALIDATOR, AHP_CR_VALIDATOR,
        PANEL_EFFICIENCY_VALIDATOR
    )
except ImportError:
    pass

try:
    from .data_processing import (
        DataCleaner, DataTransformer, SpatialTransformer,
        TemporalTransformer, aggregate_data, pivot_data
    )
except ImportError:
    pass


def initialize_project():
    """
    Initialize project with all utilities configured
    
    Sets up:
    - Project paths
    - Logging
    - Configuration
    
    Call this once at application startup
    """
    setup_project_paths()
    logger = setup_logging("geesp-angola")
    logger.info("✅ GEESP-Angola utilities initialized")
    return logger
