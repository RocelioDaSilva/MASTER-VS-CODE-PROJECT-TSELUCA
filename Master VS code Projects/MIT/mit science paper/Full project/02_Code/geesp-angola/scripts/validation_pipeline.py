from typing import Dict, Any, Tuple, Optional
import numpy as np
import logging
from . import validators

logger = logging.getLogger(__name__)


def run_validation_pipeline(
    rasters: Dict[str, np.ndarray],
    weights: Dict[str, float],
    capacity_mw: float,
    annual_irradiance: float,
    discount_rate: float,
    expected_shape: Tuple[int, int] = (280, 300),
) -> Dict[str, Any]:
    """Run a validation pipeline using `scripts.validators` helpers.

    Args:
        rasters: Dict with keys 'solar','population','distance','slope','ndvi'
        weights: MCDA weights dict (should sum to 1)
        capacity_mw: Project capacity in MW
        annual_irradiance: Annual irradiance in kWh/m2/year
        discount_rate: Discount rate (%) for LCOE
        expected_shape: Expected raster shape

    Returns:
        Dict containing 'ok':bool and 'errors': list[str]

    Raises:
        ValueError if critical validation fails
    """
    errors = []

    # Extract rasters
    solar = rasters.get("solar")
    population = rasters.get("population")
    distance = rasters.get("distance")
    slope = rasters.get("slope")
    ndvi = rasters.get("ndvi")

    try:
        validators.validate_all_inputs(
            solar,
            population,
            distance,
            slope,
            ndvi,
            weights,
            capacity_mw,
            annual_irradiance,
            discount_rate,
            expected_shape=expected_shape,
        )
        logger.info("All inputs validated successfully by validation_pipeline")
        return {"ok": True, "errors": []}
    except Exception as e:
        logger.warning(f"Validation pipeline reported errors: {e}")
        return {"ok": False, "errors": [str(e)]}


def quick_validate_shapes(rasters: Dict[str, np.ndarray], expected_shape: Tuple[int, int]) -> bool:
    """Fast shape-only check for rasters; raises ValueError on mismatch."""
    for name, arr in rasters.items():
        if arr is None:
            raise ValueError(f"Raster '{name}' is None")
        if not isinstance(arr, np.ndarray):
            raise ValueError(f"Raster '{name}' is not numpy array (got {type(arr)})")
        if arr.shape != expected_shape:
            raise ValueError(f"Raster '{name}' shape {arr.shape} != expected {expected_shape}")
    return True
