"""Shared logging configuration for operations scripts."""

from pathlib import Path
import logging
import sys
from typing import Optional


def get_script_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """Return a consistently configured logger for ops scripts.

    If ``log_file`` is provided, logs are emitted to both file and stdout.
    Without a log file, logs go to stdout only.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
