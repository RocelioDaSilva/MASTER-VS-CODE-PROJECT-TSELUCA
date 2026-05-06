"""UI-facing validators that wrap `scripts.validators` into testable helpers.

These adapters make it easier for pages to call validation logic without
duplicating error handling and to simplify unit testing.
"""
from typing import Dict
import numpy as np

from scripts import validators


def validate_weights_for_ui(weights: Dict[str, float]) -> bool:
    """Validate weights and convert errors to ValueError for UI consumption."""
    return validators.validate_weights(weights)


def validate_raster_shape_for_ui(data: np.ndarray, expected_shape: tuple) -> bool:
    """Wrap `validate_raster_shape` for UI tests."""
    return validators.validate_raster_shape(data, expected_shape)
