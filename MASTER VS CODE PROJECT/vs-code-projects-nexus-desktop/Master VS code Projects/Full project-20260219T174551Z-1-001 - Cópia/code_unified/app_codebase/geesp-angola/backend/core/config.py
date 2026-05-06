"""
GEESP-Angola: Unified Configuration Access Module
Consolidated from config_manager.py to backend/core/config.py

Consolidates configuration loading and access patterns across the application.
"""

from typing import Dict, Any, Optional, Union, List
from pathlib import Path
from dataclasses import dataclass, asdict
import json
import os
import logging
import threading

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================


@dataclass
class AppConfig:
    """
    Unified application configuration.
    Consolidates settings from config.json and environment variables.
    """
    # Application
    app_name: str = "GEESP-Angola"
    app_version: str = "2.0"
    environment: str = "development"
    
    # Database
    database_url: str = "sqlite:///geesp.db"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 4
    api_debug: bool = False
    
    # Google Earth Engine
    gee_project: str = os.environ.get("GEESP_GEE_PROJECT", "")  # Must be set via env
    gee_export_bucket: Optional[str] = None
    gee_cache_dir: str = "./data/gee_cache"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = "logs/geesp.log"
    
    # Data Processing
    data_cache_enabled: bool = True
    data_cache_dir: str = "./data/cache"
    normalization_min: float = 0.0
    normalization_max: float = 1.0
    
    # Paths
    data_dir: str = "./data"
    output_dir: str = "./output"
    config_dir: str = "./config"
    
    # Performance
    batch_size: int = 100
    max_workers: int = 4
    enable_profiling: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        """Create config from dictionary."""
        # Filter to only accepted fields
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)


# ============================================================================
# CONFIGURATION EXCEPTIONS
# ============================================================================


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass


# ============================================================================
# CONFIGURATION MANAGER (SINGLETON)
# ============================================================================


class ConfigManager:
    """
    Singleton configuration manager.
    Provides unified access to application configuration.
    
    Loads configuration from:
    1. config.json (file)
    2. Environment variables (overrides file)
    3. Default values (fallback)
    
    Example:
        >>> config = ConfigManager.get_instance()
        >>> database_url = config.get('database_url')
        >>> config.set('api_port', 9000)
    """
    
    _instance: Optional["ConfigManager"] = None
    _config: Dict[str, Any] = {}
    _lock = threading.Lock()
    
    def __new__(cls) -> "ConfigManager":
        """Ensure singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager."""
        if self._initialized:
            return
        
        self._app_config = AppConfig()
        self._custom_config: Dict[str, Any] = {}
        self._initialized = True
        
        self._load_configuration()
        logger.info(f"Configuration loaded: {self._app_config.environment} environment")
    
    @classmethod
    def get_instance(cls) -> "ConfigManager":
        """Get singleton instance."""
        return cls()
    
    def _load_configuration(self) -> None:
        """Load configuration from all sources."""
        # 1. Load from config.json
        self._load_from_file()
        
        # 2. Override with environment variables
        self._load_from_environment()
        
        # 3. Warn about missing recommended env vars
        self._warn_missing_env_vars()
    
    def _warn_missing_env_vars(self) -> None:
        """Warn at startup if important env vars are not set."""
        if not self._app_config.gee_project:
            logger.warning(
                "GEESP_GEE_PROJECT is not set — Google Earth Engine features will be unavailable. "
                "Set this environment variable to your GEE project ID."
            )
        if not os.getenv("DATABASE_URL") and not os.getenv("GEESP_DATABASE_URL"):
            logger.warning(
                "DATABASE_URL / GEESP_DATABASE_URL is not set — "
                "database features will use defaults which may not work in production."
            )
    
    def _load_from_file(self, filepath: str = "config.json") -> None:
        """Load configuration from JSON file."""
        try:
            config_path = Path(filepath)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                self._app_config = AppConfig.from_dict(file_config)
                logger.info(f"Configuration loaded from {filepath}")
            else:
                logger.warning(f"Configuration file not found: {filepath}, using defaults")
        except Exception as e:
            logger.error(f"Failed to load configuration from file: {str(e)}")
            raise ConfigurationError(f"Config load failed: {str(e)}")
    
    def _load_from_environment(self) -> None:
        """Override configuration with environment variables."""
        env_mapping = {
            'GEESP_ENVIRONMENT': 'environment',
            'GEESP_DATABASE_URL': 'database_url',
            'GEESP_API_HOST': 'api_host',
            'GEESP_API_PORT': 'api_port',
            'GEESP_GEE_PROJECT': 'gee_project',
            'GEESP_LOG_LEVEL': 'log_level',
            'GEESP_LOG_FILE': 'log_file',
            'GEESP_DATA_DIR': 'data_dir',
            'GEESP_OUTPUT_DIR': 'output_dir',
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    if config_key == 'api_port':
                        value = int(value)
                        if not (1 <= value <= 65535):
                            raise ValueError(f"Port must be 1-65535, got {value}")
                    elif config_key == 'data_cache_enabled':
                        value = value.lower() == 'true'
                    setattr(self._app_config, config_key, value)
                    logger.debug(f"Configuration overridden from env: {env_var}")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to parse {env_var}: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config = ConfigManager.get_instance()
            >>> port = config.get('api_port', 8000)
        """
        # Check AppConfig attributes first
        if hasattr(self._app_config, key):
            return getattr(self._app_config, key)
        
        # Check custom config
        if key in self._custom_config:
            return self._custom_config[key]
        
        return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value at runtime.
        
        Args:
            key: Configuration key
            value: Configuration value
            
        Example:
            >>> config = ConfigManager.get()
            >>> config.set('api_port', 9000)
        """
        if hasattr(self._app_config, key):
            setattr(self._app_config, key, value)
            logger.debug(f"Configuration updated: {key} = {value}")
        else:
            self._custom_config[key] = value
            logger.debug(f"Custom configuration set: {key} = {value}")
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration as dictionary.
        
        Returns:
            Dictionary of all configuration
            
        Example:
            >>> config = ConfigManager.get()
            >>> all_config = config.get_all()
        """
        result = self._app_config.to_dict()
        result.update(self._custom_config)
        return result
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration from dictionary.
        
        Args:
            config_dict: Dictionary of configuration values
            
        Example:
            >>> config = ConfigManager.get()
            >>> config.update_from_dict({'api_port': 9000, 'log_level': 'DEBUG'})
        """
        for key, value in config_dict.items():
            self.set(key, value)
        logger.info(f"Configuration updated with {len(config_dict)} values")
    
    def validate(self) -> bool:
        """
        Validate configuration consistency.
        
        Returns:
            True if valid
            
        Raises:
            ConfigurationError: If validation fails
        """
        # Validate required fields
        required = ['app_name', 'environment', 'database_url']
        
        for field in required:
            if not self.get(field):
                raise ConfigurationError(f"Required field missing: {field}")
        
        # Validate port range
        port = self.get('api_port', 8000)
        if not (0 < port < 65536):
            raise ConfigurationError(f"Invalid port: {port}")
        
        # Validate batch size
        batch_size = self.get('batch_size', 100)
        if batch_size <= 0:
            raise ConfigurationError(f"Invalid batch_size: {batch_size}")
        
        logger.info("Configuration validation passed")
        return True
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._app_config = AppConfig()
        self._custom_config.clear()
        logger.info("Configuration reset to defaults")


# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Shorthand for getting configuration values.
    
    Args:
        key: Configuration key
        default: Default value
        
    Returns:
        Configuration value
        
    Example:
        >>> api_port = get_config_value('api_port', 8000)
    """
    return ConfigManager.get_instance().get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """
    Shorthand for setting configuration values.
    
    Args:
        key: Configuration key
        value: Configuration value
        
    Example:
        >>> set_config_value('api_port', 9000)
    """
    ConfigManager.get_instance().set(key, value)


def get_data_dir() -> Path:
    """Get data directory path."""
    data_dir = get_config_value('data_dir', './data')
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_dir() -> Path:
    """Get output directory path."""
    output_dir = get_config_value('output_dir', './output')
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_cache_dir() -> Path:
    """Get cache directory path."""
    cache_dir = get_config_value('data_cache_dir', './data/cache')
    path = Path(cache_dir)
    if get_config_value('data_cache_enabled', True):
        path.mkdir(parents=True, exist_ok=True)
    return path


# ============================================================================
# CONSOLIDATED CONSTANTS (from TechnicalConstants)
# ============================================================================


class ProcessingConstants:
    """Unified processing constants consolidation."""
    
    # Normalization defaults
    NORMALIZE_MIN = 0.0
    NORMALIZE_MAX = 1.0
    
    # Data thresholds
    EMPTY_ARRAY_THRESHOLD = 0
    CONSTANT_ARRAY_TOLERANCE = 1e-6
    
    # Performance
    ARRAY_PROCESSING_CHUNK_SIZE = 1000000  # Elements
    MAX_CACHE_SIZE = 1000
    
    # Solar radiation
    SOLAR_RADIATION_MIN = 0.0
    SOLAR_RADIATION_MAX = 3000.0  # W/m2
    
    # Population
    POPULATION_DENSITY_MIN = 0.0
    POPULATION_DENSITY_MAX = 100000.0  # people/km2
    
    # Elevation
    ELEVATION_MIN = -500.0  # Meters below sea level
    ELEVATION_MAX = 9000.0  # Mt. Everest


# Initialize configuration on module import
_config_manager = ConfigManager.get_instance()
logger.debug("Configuration module initialized")
