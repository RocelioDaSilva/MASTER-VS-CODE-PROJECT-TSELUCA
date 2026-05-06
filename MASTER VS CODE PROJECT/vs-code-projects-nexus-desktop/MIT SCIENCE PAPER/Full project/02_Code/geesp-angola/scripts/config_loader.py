"""
Configuration Loader for GEESP-Angola
Provides centralized configuration management with environment variable overrides
"""

import json
import os
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage GEESP-Angola configuration"""
    
    _instance = None
    _config: Optional[Dict[str, Any]] = None
    
    def __new__(cls):
        """Singleton pattern - ensure only one config instance"""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize config loader (singleton)"""
        if self._config is None:
            self._config = self._load_config()
    
    @staticmethod
    def _load_config() -> Dict[str, Any]:
        """Load configuration from config.json or environment variables"""
        
        # 1. Try to load from environment variable first
        config_path_env = os.getenv("GEESP_CONFIG")
        if config_path_env and os.path.exists(config_path_env):
            logger.info(f"Loading config from environment variable: {config_path_env}")
            return ConfigLoader._read_json(config_path_env)
        
        # 2. Look for config.json in project root
        config_paths = [
            Path(__file__).parent.parent / "config.json",  # ../config.json
            Path.cwd() / "config.json",                    # ./config.json
            Path.home() / ".geesp" / "config.json",       # ~/.geesp/config.json
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                logger.info(f"Loading config from: {config_path}")
                return ConfigLoader._read_json(str(config_path))
        
        # 3. If no config found, return default minimal config
        logger.warning("No config.json found, using defaults")
        return ConfigLoader._get_default_config()
    
    @staticmethod
    def _read_json(filepath: str) -> Dict[str, Any]:
        """Read JSON file with error handling"""
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            logger.info(f"Config loaded successfully from {filepath}")
            return config
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return ConfigLoader._get_default_config()
        except Exception as e:
            logger.error(f"Error reading config file: {e}")
            return ConfigLoader._get_default_config()
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "project_name": "GEESP-Angola",
            "version": "3.0.0",
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/geesp.log",
                "max_bytes": 10485760,  # 10 MB
                "backup_count": 5
            },
            "map_generation": {
                "output_shape": [280, 300],
                "default_format": "npy",
                "resolution_m": 1000,
                "nodata_value": -9999,
                "dtype": "float32"
            },
            "mcda": {
                "default_weights": {
                    "solar_irradiance": 0.25,
                    "population_density": 0.25,
                    "grid_distance": 0.20,
                    "slope": 0.15,
                    "vegetation_ndvi": 0.15
                },
                "weights_sum_tolerance": 0.01,
                "consistency_ratio_threshold": 0.1,
                "min_weight": 0.05,
                "max_weight": 0.50,
                "classification_thresholds": {
                    "high": 0.70,
                    "medium": 0.40,
                    "low": 0.0
                },
                "normalization_ranges": {
                    "solar_irradiance": [5.5, 6.4],
                    "population_density": [10, 95],
                    "grid_distance": [0, 45],
                    "slope": [0, 30],
                    "vegetation_ndvi": [-0.2, 0.7]
                }
            },
            "lcoe": {
                "standard_parameters": {
                    "default_capacity_mw": 1.0,
                    "default_discount_rate_percent": 8.0,
                    "default_project_lifetime_years": 25,
                    "default_warranty_years": 10,
                    "default_degradation_rate_percent": 0.5
                },
                "technology_costs": {
                    "pv_module_usd_per_kw": 200,
                    "inverter_usd_per_kw": 80,
                    "battery_usd_per_kwh": 150,
                    "installation_labor_percent": 15
                },
                "operational_parameters": {
                    "area_per_kw_sqm": 7.5,
                    "opex_percent_of_capex": 2.0,
                    "decommissioning_percent_of_capex": 0.5,
                    "capacity_factor_percent": 20.0
                },
                "irradiance_hours_per_year": 1825
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "cors_origins": ["*"],
                "rate_limit_requests": 100,
                "rate_limit_seconds": 60
            },
            "dashboard": {
                "page_title": "GEESP-Angola",
                "page_icon": "☀️",
                "layout": "wide",
                "sidebar_state": "expanded",
                "theme": "light"
            },
            "monitoring": {
                "cache_ttl_seconds": 300,
                "refresh_interval_seconds": 60,
                "max_datapoints": 1000
            },
            "gee": {
                "timeout_seconds": 300,
                "max_retries": 3,
                "batch_size": 10,
                "export_resolution_m": 1000
            },
            "data_storage": {
                "backend": "local",  # local, s3, gcs
                "data_dir": "data",
                "output_dir": "output",
                "logs_dir": "logs",
                "cache_dir": ".cache"
            },
            "validation": {
                "strict_mode": True,
                "warn_on_invalid": True,
                "max_array_size_mb": 500
            },
            "performance": {
                "enable_caching": True,
                "cache_max_size_mb": 1000,
                "num_workers": 4,
                "batch_processing": True
            },
            "solar_data_ranges": {
                "irradiance": {
                    "expected_range": [4.5, 7.5],
                    "absolute_min": 0,
                    "absolute_max": 10
                },
                "population_density": {
                    "expected_range": [50, 5000],
                    "absolute_min": 0,
                    "absolute_max": 50000
                },
                "grid_distance": {
                    "expected_range": [0, 50],
                    "unit": "km",
                    "absolute_max": 500
                },
                "slope": {
                    "expected_range": [0, 30],
                    "unit": "degrees",
                    "absolute_max": 90
                },
                "ndvi": {
                    "expected_range": [-0.2, 0.7],
                    "absolute_min": -1.0,
                    "absolute_max": 1.0
                }
            },
            "paths": {
                "data_dir": "data",
                "output_dir": "output",
                "logs_dir": "logs"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is not None:
                logger.warning(f"Config key '{key}' not found, using default: {default}")
            return default
    
    def get_map_shape(self) -> Tuple[int, int]:
        """Get map output shape (height, width)"""
        shape = self.get("map_generation.output_shape", [280, 300])
        return tuple(shape) if isinstance(shape, list) else (280, 300)
    
    def get_mcda_weights(self) -> Dict[str, float]:
        """Get default MCDA weights"""
        return self.get("mcda.default_weights", {
            "solar_irradiance": 0.25,
            "population_density": 0.25,
            "grid_distance": 0.20,
            "slope": 0.15,
            "vegetation_ndvi": 0.15
        })
    
    def get_lcoe_capacity_mw(self) -> float:
        """Get default LCOE capacity"""
        return self.get("lcoe.standard_parameters.default_capacity_mw", 1.0)
    
    def get_lcoe_discount_rate(self) -> float:
        """Get default LCOE discount rate (as percentage)"""
        return self.get("lcoe.standard_parameters.default_discount_rate_percent", 8.0)
    
    def get_lcoe_lifetime_years(self) -> int:
        """Get default LCOE project lifetime"""
        return self.get("lcoe.standard_parameters.default_project_lifetime_years", 25)
    
    def get_solar_irradiance_range(self) -> Tuple[float, float]:
        """Get solar irradiance expected range"""
        ranges = self.get("solar_data_ranges.irradiance.expected_range", [4.5, 7.5])
        return tuple(ranges) if isinstance(ranges, list) else (4.5, 7.5)
    
    def get_population_density_range(self) -> Tuple[float, float]:
        """Get population density expected range"""
        ranges = self.get("solar_data_ranges.population_density.expected_range", [50, 5000])
        return tuple(ranges) if isinstance(ranges, list) else (50, 5000)
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.get("logging", {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/geesp.log"
        })
    
    def get_logging_level(self) -> str:
        """Get logging level"""
        return self.get("logging.level", "INFO")
    
    def get_logging_file(self) -> str:
        """Get logging file path"""
        return self.get("logging.file", "logs/geesp.log")
    
    # ============================================================================
    # MCDA CONFIGURATION GETTERS
    # ============================================================================
    
    def get_mcda_classification_thresholds(self) -> Dict[str, float]:
        """Get MCDA classification thresholds (high, medium, low)"""
        return self.get("mcda.classification_thresholds", {
            "high": 0.70,
            "medium": 0.40,
            "low": 0.0
        })
    
    def get_mcda_normalization_ranges(self) -> Dict[str, list]:
        """Get normalization ranges for MCDA criteria"""
        return self.get("mcda.normalization_ranges", {
            "solar_irradiance": [5.5, 6.4],
            "population_density": [10, 95],
            "grid_distance": [0, 45],
            "slope": [0, 30],
            "vegetation_ndvi": [-0.2, 0.7]
        })
    
    # ============================================================================
    # LCOE CONFIGURATION GETTERS
    # ============================================================================
    
    def get_lcoe_operational_parameters(self) -> Dict[str, float]:
        """Get LCOE operational parameters"""
        return self.get("lcoe.operational_parameters", {
            "area_per_kw_sqm": 7.5,
            "opex_percent_of_capex": 2.0,
            "decommissioning_percent_of_capex": 0.5,
            "capacity_factor_percent": 20.0
        })
    
    def get_irradiance_hours_per_year(self) -> float:
        """Get annual irradiance hours"""
        return self.get("lcoe.irradiance_hours_per_year", 1825)

    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self.get("api", {})
    
    def get_api_host(self) -> str:
        """Get API host"""
        return self.get("api.host", "0.0.0.0")
    
    def get_api_port(self) -> int:
        """Get API port"""
        return self.get("api.port", 8000)
    
    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration"""
        return self.get("dashboard", {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        return self.get("monitoring", {})
    
    def get_gee_config(self) -> Dict[str, Any]:
        """Get Google Earth Engine configuration"""
        return self.get("gee", {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance configuration"""
        return self.get("performance", {})
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get entire configuration dictionary"""
        return self._config.copy() if self._config else {}
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get configuration section"""
        return self.get(section, {})
    
    def reload(self) -> None:
        """Reload configuration from disk"""
        self._config = self._load_config()
        logger.info("Configuration reloaded")
    
    def save_section(self, section: str, data: Dict[str, Any]) -> bool:
        """Save configuration section to disk (if config path available)"""
        try:
            config_path = os.getenv("GEESP_CONFIG")
            if not config_path:
                project_root = Path(__file__).parent.parent
                config_path = project_root / "config.json"
            
            # Update in-memory config
            keys = section.split('.')
            current = self._config
            for k in keys[:-1]:
                current = current[k]
            current[keys[-1]] = data
            
            # Write to file
            with open(config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Config section '{section}' saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False


# Global config instance
_config = None


def load_config() -> ConfigLoader:
    """Get global config instance (lazy loading)"""
    global _config
    if _config is None:
        _config = ConfigLoader()
    return _config


def get_config_value(key: str, default: Any = None) -> Any:
    """Convenience function to get config value"""
    return load_config().get(key, default)


def get_map_shape() -> Tuple[int, int]:
    """Get map output shape from config"""
    return load_config().get_map_shape()


def get_mcda_weights() -> Dict[str, float]:
    """Get MCDA weights from config"""
    return load_config().get_mcda_weights()


def get_lcoe_parameters() -> Dict[str, float]:
    """Get LCOE standard parameters from config"""
    config = load_config()
    return {
        "capacity_mw": config.get_lcoe_capacity_mw(),
        "discount_rate": config.get_lcoe_discount_rate(),
        "project_lifetime": config.get_lcoe_lifetime_years()
    }


# Type hints for configuration
class ConfigSection(dict):
    """Type-safe configuration section"""
    pass


# Initialize logging for config module
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == "__main__":
    # Test configuration loading
    config = load_config()
    
    print("Configuration loaded successfully")
    print(f"  Project: {config.get('project_name')}")
    print(f"  Map shape: {config.get_map_shape()}")
    print(f"  MCDA weights: {config.get_mcda_weights()}")
    print(f"  LCOE capacity: {config.get_lcoe_capacity_mw()} MW")
    print(f"  LCOE discount rate: {config.get_lcoe_discount_rate()}%")
    print(f"  LCOE lifetime: {config.get_lcoe_lifetime_years()} years")
    
    # Test convenience functions
    print("\nConvenience functions:")
    print(f"  get_map_shape(): {get_map_shape()}")
    print(f"  get_mcda_weights(): {get_mcda_weights()}")
    print(f"  get_lcoe_parameters(): {get_lcoe_parameters()}")
