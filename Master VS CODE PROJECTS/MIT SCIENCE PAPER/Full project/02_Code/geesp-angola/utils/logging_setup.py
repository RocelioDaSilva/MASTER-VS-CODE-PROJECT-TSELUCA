"""
Shared logging setup utility for GEESP-Angola
Eliminates duplication across unified app, dashboard, monitoring, and API modules
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


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
    
    # Try to load config for defaults (prefer project root on path so utils/scripts both work)
    try:
        _root = Path(__file__).parent.parent
        _root_s = str(_root)
        if _root_s not in sys.path:
            sys.path.insert(0, _root_s)
        from scripts.config_loader import load_config
        config = load_config()
        log_config = config.get_logging_config()
        if log_level is None:
            log_level = log_config.get("level", "INFO")
        if log_file is None:
            log_file = log_config.get("file", "logs/geesp.log")
        max_bytes = log_config.get("max_bytes", max_bytes)
        backup_count = log_config.get("backup_count", backup_count)
        log_format = log_config.get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    except Exception:
        # Fallback to defaults if config unavailable
        if log_level is None:
            log_level = "INFO"
        if log_file is None:
            log_file = "logs/geesp.log"
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
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
    
    logger.info(f"[OK] Logging initialized for {logger_name}")
    return logger
