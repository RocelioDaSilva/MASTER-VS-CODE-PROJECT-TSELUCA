"""
GEESP-Angola: Input Validation Module
Comprehensive validation functions for all inputs and parameters
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Angola geographic bounds (approximate)
ANGOLA_BOUNDS = {
    "lat_min": -18.0,
    "lat_max": -4.38,
    "lon_min": 11.67,
    "lon_max": 24.82
}


# ============================================================================
# SPATIAL DATA VALIDATION
# ============================================================================

def validate_solar_irradiance(data: np.ndarray, name: str = "solar_irradiance") -> bool:
    """
    Validate solar irradiance data (kWh/m²/day)
    
    Args:
        data: Raster array with solar irradiance values
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Valid Range: 0-10 kWh/m²/day (global bounds)
    Angola typical: 5-7 kWh/m²/day
    """
    if data is None or len(data) == 0:
        raise ValueError(f"❌ {name}: Data is None or empty")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid (finite) data found")
    
    data_clean = data[valid_mask]
    min_val = np.min(data_clean)
    max_val = np.max(data_clean)
    
    if min_val < 0:
        logger.warning(f"⚠️ {name}: Negative values found (min={min_val:.2f}). Expected ≥0")
    
    if max_val > 10:
        logger.warning(f"⚠️ {name}: Values exceed 10 kWh/m²/day (max={max_val:.2f}). May be unrealistic")
    
    logger.info(f"✓ {name}: Valid range [{min_val:.2f}, {max_val:.2f}]")
    return True


def validate_population(data: np.ndarray, name: str = "population_density") -> bool:
    """
    Validate population density data (people/km²)
    
    Args:
        data: Raster array with population values
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Valid Range: 0-10,000 people/km²
    Context: Angola average ~24 people/km², some cities >10k
    """
    if data is None or len(data) == 0:
        raise ValueError(f"❌ {name}: Data is None or empty")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid data found")
    
    data_clean = data[valid_mask]
    min_val = np.min(data_clean)
    max_val = np.max(data_clean)
    
    if min_val < 0:
        logger.warning(f"⚠️ {name}: Negative values found (min={min_val:.2f})")
    
    if max_val > 50000:
        logger.warning(f"⚠️ {name}: Extremely high density (max={max_val:.0f} people/km²)")
    
    logger.info(f"✓ {name}: Valid range [{min_val:.2f}, {max_val:.2f}]")
    return True


def validate_ndvi(data: np.ndarray, name: str = "ndvi") -> bool:
    """
    Validate Normalized Difference Vegetation Index (NDVI)
    
    Args:
        data: Raster array with NDVI values
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Valid Range: -1 to +1
    Interpretation:
        < -0.1: Water
        -0.1 to 0.1: Barren/Rock
        0.1 to 0.3: Grass/Shrub
        > 0.3: Forest/Dense vegetation
    """
    if data is None or len(data) == 0:
        raise ValueError(f"❌ {name}: Data is None or empty")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid data found")
    
    data_clean = data[valid_mask]
    min_val = np.min(data_clean)
    max_val = np.max(data_clean)
    
    if min_val < -1.0:
        logger.warning(f"⚠️ {name}: Values below -1.0 (min={min_val:.2f}). Expected ∈ [-1, 1]")
    
    if max_val > 1.0:
        logger.warning(f"⚠️ {name}: Values above 1.0 (max={max_val:.2f}). Expected ∈ [-1, 1]")
    
    logger.info(f"✓ {name}: Valid range [{min_val:.2f}, {max_val:.2f}]")
    return True


def validate_distance(data: np.ndarray, name: str = "distance_to_grid") -> bool:
    """
    Validate distance to electrical grid (km)
    
    Args:
        data: Raster array with distance values
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Valid Range: 0-500 km
    Context: Angola's typical service area is <200 km
    """
    if data is None or len(data) == 0:
        raise ValueError(f"❌ {name}: Data is None or empty")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid data found")
    
    data_clean = data[valid_mask]
    min_val = np.min(data_clean)
    max_val = np.max(data_clean)
    
    if min_val < 0:
        logger.warning(f"⚠️ {name}: Negative distances (min={min_val:.2f})")
    
    if max_val > 500:
        logger.warning(f"⚠️ {name}: Very far distances (max={max_val:.2f} km). Expected <500 km")
    
    logger.info(f"✓ {name}: Valid range [{min_val:.2f}, {max_val:.2f}] km")
    return True


def validate_slope(data: np.ndarray, name: str = "slope") -> bool:
    """
    Validate terrain slope (degrees)
    
    Args:
        data: Raster array with slope values
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Valid Range: 0-90 degrees
    Practical: >30° becomes difficult for solar installation
    """
    if data is None or len(data) == 0:
        raise ValueError(f"❌ {name}: Data is None or empty")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid data found")
    
    data_clean = data[valid_mask]
    min_val = np.min(data_clean)
    max_val = np.max(data_clean)
    
    if min_val < 0:
        logger.warning(f"⚠️ {name}: Negative slopes (min={min_val:.2f}°)")
    
    if max_val > 90:
        logger.warning(f"⚠️ {name}: Slopes exceed 90° (max={max_val:.2f}°). Expected ≤90°")
    
    if max_val > 30:
        logger.info(f"ℹ️ {name}: Steep slopes found (max={max_val:.2f}°). May be unsuitable for solar")
    
    logger.info(f"✓ {name}: Valid range [{min_val:.2f}, {max_val:.2f}]°")
    return True


# ============================================================================
# WEIGHT VALIDATION
# ============================================================================

def validate_weights(weights: Dict[str, float], tolerance: float = 0.01) -> bool:
    """
    Validate MCDA criterion weights
    
    Args:
        weights: Dictionary of criterion names to weights
        tolerance: Allowed deviation from 1.0 (default 0.01 = ±1%)
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Rules:
        - All weights ∈ [0, 1]
        - Sum ≈ 1.0 (±tolerance)
    """
    if not weights:
        raise ValueError("❌ Weights dictionary is empty")
    
    if not isinstance(weights, dict):
        raise ValueError(f"❌ Weights must be dict, got {type(weights)}")
    
    # Check individual weights
    for criterion, weight in weights.items():
        if not isinstance(weight, (int, float)):
            raise ValueError(f"❌ Weight for '{criterion}' must be numeric, got {type(weight)}")
        
        if weight < 0 or weight > 1:
            raise ValueError(f"❌ Weight for '{criterion}' ({weight}) outside [0, 1]")
    
    # Check sum
    weight_sum = sum(weights.values())
    deviation = abs(weight_sum - 1.0)
    
    if deviation > tolerance:
        raise ValueError(
            f"❌ Weights sum to {weight_sum:.3f}, expected ≈1.0 (tolerance={tolerance})"
        )
    
    if deviation > 0.001:
        logger.warning(f"⚠️ Weights sum to {weight_sum:.3f} (deviation={deviation:.4f})")
    
    logger.info(f"✓ Weights valid: {len(weights)} criteria, sum={weight_sum:.3f}")
    return True


def validate_weight_vector(weights: np.ndarray, tolerance: float = 0.01) -> bool:
    """
    Validate weight vector (array form)
    
    Args:
        weights: 1D numpy array of weights
        tolerance: Allowed deviation from 1.0
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(weights, np.ndarray):
        raise ValueError(f"❌ Weights must be numpy array, got {type(weights)}")
    
    if weights.ndim != 1:
        raise ValueError(f"❌ Weights must be 1D, got shape {weights.shape}")
    
    if np.any(weights < 0) or np.any(weights > 1):
        raise ValueError(f"❌ Some weights outside [0, 1]: [{weights.min()}, {weights.max()}]")
    
    weight_sum = float(weights.sum())
    deviation = abs(weight_sum - 1.0)
    
    if deviation > tolerance:
        raise ValueError(f"❌ Weights sum to {weight_sum:.3f}, expected ≈1.0")
    
    logger.info(f"✓ Weight vector valid: {len(weights)} weights, sum={weight_sum:.3f}")
    return True


# ============================================================================
# PARAMETER VALIDATION
# ============================================================================

def validate_capacity_mw(capacity: float, min_val: float = 0.1, max_val: float = 500) -> bool:
    """
    Validate solar capacity in MW
    
    Args:
        capacity: Capacity in megawatts
        min_val: Minimum allowed (default 0.1 MW)
        max_val: Maximum allowed (default 500 MW)
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(capacity, (int, float)):
        raise ValueError(f"❌ Capacity must be numeric, got {type(capacity)}")
    
    if capacity < min_val or capacity > max_val:
        raise ValueError(f"❌ Capacity {capacity} MW outside [{min_val}, {max_val}] MW")
    
    logger.info(f"✓ Capacity valid: {capacity} MW")
    return True


def validate_irradiance_kwh(irradiance: float, min_val: float = 500, max_val: float = 3500) -> bool:
    """
    Validate annual solar irradiance (kWh/m²/year)
    
    Args:
        irradiance: Annual irradiance value
        min_val: Minimum (default 500 kWh/m²/year)
        max_val: Maximum (default 3500 kWh/m²/year)
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(irradiance, (int, float)):
        raise ValueError(f"❌ Irradiance must be numeric, got {type(irradiance)}")
    
    if irradiance < min_val or irradiance > max_val:
        raise ValueError(
            f"❌ Irradiance {irradiance} kWh/m²/year outside [{min_val}, {max_val}]"
        )
    
    logger.info(f"✓ Irradiance valid: {irradiance} kWh/m²/year")
    return True


def validate_discount_rate(rate: float, min_val: float = -100, max_val: float = 100) -> bool:
    """
    Validate LCOE discount rate (%)
    
    Args:
        rate: Discount rate as percentage
        min_val: Minimum (default -100%)
        max_val: Maximum (default 100%)
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Typical range: 5-12% for solar projects in EMs
    """
    if not isinstance(rate, (int, float)):
        raise ValueError(f"❌ Discount rate must be numeric, got {type(rate)}")
    
    if rate < min_val or rate > max_val:
        raise ValueError(f"❌ Discount rate {rate}% outside [{min_val}, {max_val}]%")
    
    if rate < 0:
        logger.warning(f"⚠️ Negative discount rate {rate}% is unusual")
    
    if rate > 25:
        logger.warning(f"⚠️ High discount rate {rate}% may be unrealistic")
    
    logger.info(f"✓ Discount rate valid: {rate}%")
    return True


def validate_project_lifetime(years: int, min_val: int = 5, max_val: int = 50) -> bool:
    """
    Validate project lifetime (years)
    
    Args:
        years: Project lifetime
        min_val: Minimum (default 5 years)
        max_val: Maximum (default 50 years)
    
    Returns:
        True if valid, raises ValueError otherwise
    
    Typical: 20-25 years for solar PV
    """
    if not isinstance(years, int):
        raise ValueError(f"❌ Lifetime must be integer, got {type(years)}")
    
    if years < min_val or years > max_val:
        raise ValueError(f"❌ Lifetime {years} years outside [{min_val}, {max_val}]")
    
    logger.info(f"✓ Project lifetime valid: {years} years")
    return True


# ============================================================================
# SHAPE & DIMENSION VALIDATION
# ============================================================================

def validate_raster_shape(
    data: np.ndarray,
    expected_shape: Tuple[int, int],
    name: str = "raster"
) -> bool:
    """
    Validate raster dimensions
    
    Args:
        data: Raster array
        expected_shape: Expected (height, width)
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(data, np.ndarray):
        raise ValueError(f"❌ {name}: Not a numpy array, got {type(data)}")
    
    if data.ndim != 2:
        raise ValueError(f"❌ {name}: Must be 2D, got {data.ndim}D with shape {data.shape}")
    
    if data.shape != expected_shape:
        raise ValueError(
            f"❌ {name}: Shape {data.shape} doesn't match expected {expected_shape}"
        )
    
    logger.info(f"✓ {name}: Shape {data.shape} valid")
    return True


def validate_is_probability_array(
    data: np.ndarray,
    name: str = "probability_array"
) -> bool:
    """
    Validate array contains probability values [0, 1]
    
    Args:
        data: Array to validate
        name: Name for logging
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(data, np.ndarray):
        raise ValueError(f"❌ {name}: Not a numpy array")
    
    valid_mask = np.isfinite(data)
    if not valid_mask.any():
        raise ValueError(f"❌ {name}: No valid values")
    
    data_clean = data[valid_mask]
    
    if data_clean.min() < 0 or data_clean.max() > 1:
        raise ValueError(
            f"❌ {name}: Values outside [0, 1]: [{data_clean.min():.3f}, {data_clean.max():.3f}]"
        )
    
    logger.info(f"✓ {name}: All values in [0, 1]")
    return True


# ============================================================================
# BATCH VALIDATION
# ============================================================================

def validate_all_inputs(
    solar: np.ndarray,
    population: np.ndarray,
    distance: np.ndarray,
    slope: np.ndarray,
    ndvi: np.ndarray,
    weights: Dict[str, float],
    capacity_mw: float,
    irradiance: float,
    discount_rate: float,
    expected_shape: Tuple[int, int] = (280, 300)
) -> bool:
    """
    Comprehensive validation of all inputs
    
    Args:
        solar: Solar irradiance raster
        population: Population density raster
        distance: Distance to grid raster
        slope: Slope raster
        ndvi: NDVI raster
        weights: MCDA weights dictionary
        capacity_mw: Capacity in MW
        irradiance: Annual irradiance in kWh/m²/year
        discount_rate: LCOE discount rate %
        expected_shape: Expected raster shape
    
    Returns:
        True if all valid, raises ValueError with details otherwise
    
    Example:
        >>> validate_all_inputs(solar, pop, dist, slope, ndvi, 
        ...                     weights, 1.0, 2226, 8.0)
    """
    errors = []
    
    # Validate rasters
    try:
        validate_raster_shape(solar, expected_shape, "solar")
        validate_solar_irradiance(solar)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_raster_shape(population, expected_shape, "population")
        validate_population(population)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_raster_shape(distance, expected_shape, "distance")
        validate_distance(distance)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_raster_shape(slope, expected_shape, "slope")
        validate_slope(slope)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_raster_shape(ndvi, expected_shape, "ndvi")
        validate_ndvi(ndvi)
    except ValueError as e:
        errors.append(str(e))
    
    # Validate parameters
    try:
        validate_weights(weights)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_capacity_mw(capacity_mw)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_irradiance_kwh(irradiance)
    except ValueError as e:
        errors.append(str(e))
    
    try:
        validate_discount_rate(discount_rate)
    except ValueError as e:
        errors.append(str(e))
    
    if errors:
        error_str = "\n".join(errors)
        raise ValueError(f"❌ Validation failed with {len(errors)} error(s):\n{error_str}")
    
    logger.info(f"✓ All inputs validated successfully ({9} items checked)")
    return True


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    print("✅ Validators module loaded successfully")
    
    # Test with dummy data
    test_solar = np.random.uniform(5.0, 7.0, (280, 300))
    validate_solar_irradiance(test_solar)
    
    test_weights = {"solar": 0.25, "population": 0.25, "distance": 0.20, 
                    "slope": 0.15, "ndvi": 0.15}
    validate_weights(test_weights)
    
    print("✓ All example validations passed!")
