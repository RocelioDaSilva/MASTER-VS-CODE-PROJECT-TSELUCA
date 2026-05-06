"""Compatibility logging configuration used by archived tests.

Provides a minimal `setup_logging` function returning a configured
logger so tests can call `setup_logging(__name__)` safely.
"""
import logging


def setup_logging(name: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


__all__ = ["setup_logging"]
