"""
GEESP-Angola: Unified Logging Module
Renamed from logging_config.py to logging.py

Shared logging setup utility - eliminates duplication across unified app,
dashboard, monitoring, and API modules.
"""

import logging
import sys
import os
import io
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

# Ensure UTF-8 encoding for console output on Windows
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')


def setup_logging(
    logger_name: str = "geesp",
    log_file: Optional[str] = None,
    log_level: Optional[str] = None,
    max_bytes: int = 10485760,  # 10 MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure structured logging for any GEESP-Angola module.
    
    Args:
        logger_name: Name for the logger (e.g., "geesp_dashboard", "geesp_api")
        log_file: Path to log file (defaults to logs/geesp.log)
        log_level: Logging level (defaults to INFO, or from config if available)
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup log files to keep
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    
    # Return existing logger if already configured
    if logger.handlers:
        return logger
    
    # Default values
    if log_level is None:
        log_level = "INFO"
    if log_file is None:
        log_file = "logs/geesp.log"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Validate log level (M6: reject unknown levels early)
    _valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    _level_upper = log_level.upper()
    if _level_upper not in _valid_levels:
        import warnings
        warnings.warn(
            f"Unknown log level {log_level!r}; falling back to INFO. "
            f"Valid choices: {', '.join(sorted(_valid_levels))}",
            stacklevel=2,
        )
        _level_upper = "INFO"
    log_level = _level_upper
    
    # Try to load config for defaults (prefer project root on path so utils/scripts both work)
    try:
        _root = Path(__file__).parent.parent
        _root_s = str(_root)
        if _root_s not in sys.path:
            sys.path.insert(0, _root_s)
        from core.config import ConfigManager, get_config_value
        config = ConfigManager.get_instance()
        log_level_cfg = config.get('log_level')
        log_file_cfg = config.get('log_file')
        if log_level_cfg is not None:
            log_level = log_level_cfg
        if log_file_cfg is not None:
            log_file = log_file_cfg
    except Exception:
        # Fallback to defaults (already set above)
        pass
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Console handler with UTF-8 encoding (handles Windows cp1252 issue)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # On Windows, wrap stdout to handle UTF-8 properly
    if sys.platform == 'win32':
        try:
            # Replace stdout/stderr with UTF-8 wrapped versions
            if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer,
                    encoding='utf-8',
                    line_buffering=True
                )
            if not isinstance(sys.stderr, io.TextIOWrapper) or sys.stderr.encoding.lower() != 'utf-8':
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer,
                    encoding='utf-8',
                    line_buffering=True
                )
        except (AttributeError, TypeError):
            pass  # Already properly wrapped or immutable
    
    # File handler with rotation and UTF-8 encoding
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    logger.info(f"Logging initialized for {logger_name}")
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.
    Simple wrapper around logging.getLogger() for consistency.
    
    Args:
        name: Logger name (typically __name__ from calling module)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggingManager:
    """
    Manager class for centralized logging configuration.
    Provides convenient interface for setting up and managing loggers.
    """
    
    _instance = None
    _configured = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def configure(self, logger_name: str = "geesp", **kwargs) -> logging.Logger:
        """
        Configure the logging system.
        
        Args:
            logger_name: Name for the root logger
            **kwargs: Additional arguments passed to setup_logging()
        
        Returns:
            Configured logger instance
        """
        if not LoggingManager._configured:
            self._logger = setup_logging(logger_name, **kwargs)
            LoggingManager._configured = True
        return self._logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger with the given name."""
        return get_logger(name)
