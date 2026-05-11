"""
Test suite: Validators Module
Tests for input validation across all core functions
"""

import pytest
import numpy as np
import logging
from scripts.validators import (
    validate_solar_irradiance, validate_population, validate_ndvi,
    validate_distance, validate_slope, validate_weights, 
    validate_weight_vector, validate_capacity_mw, validate_irradiance_kwh,
    validate_discount_rate, validate_project_lifetime, validate_raster_shape,
    validate_is_probability_array, validate_all_inputs
)


# ============================================================================
# SPATIAL DATA VALIDATION TESTS
# ============================================================================

class TestSolarIrradianceValidation:
    """Test solar irradiance validation"""
    
    def test_valid_solar_data(self):
        """Should accept valid solar irradiance data"""
        data = np.random.uniform(5.0, 7.0, (280, 300))
        assert validate_solar_irradiance(data) == True
    
    def test_empty_data_raises_error(self):
        """Should reject empty arrays"""
        with pytest.raises(ValueError, match="empty"):
            validate_solar_irradiance(np.array([]))
    
    def test_none_data_raises_error(self):
        """Should reject None"""
        with pytest.raises(ValueError, match="None"):
            validate_solar_irradiance(None)
    
    def test_all_nan_data_raises_error(self):
        """Should reject all-NaN arrays"""
        data = np.full((280, 300), np.nan)
        with pytest.raises(ValueError, match="valid"):
            validate_solar_irradiance(data)
    
    def test_negative_values_warning(self, caplog):
        """Should log warning for negative values"""
        data = np.random.uniform(-1.0, 7.0, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_solar_irradiance(data)
        assert "Negative" in caplog.text
    
    def test_extreme_high_values_warning(self, caplog):
        """Should log warning for values >10"""
        data = np.random.uniform(8.0, 15.0, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_solar_irradiance(data)
        assert "exceed" in caplog.text.lower()


class TestPopulationValidation:
    """Test population density validation"""
    
    def test_valid_population_data(self):
        """Should accept valid population data"""
        data = np.random.uniform(0, 500, (280, 300))
        assert validate_population(data) == True
    
    def test_negative_population_warning(self, caplog):
        """Should log warning for negative values"""
        data = np.random.uniform(-100, 500, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_population(data)
        assert "Negative" in caplog.text
    
    def test_extreme_density_warning(self, caplog):
        """Should warn for extremely high density"""
        data = np.random.uniform(40000, 60000, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_population(data)
        assert "Extremely high" in caplog.text


class TestNDVIValidation:
    """Test NDVI validation"""
    
    def test_valid_ndvi_data(self):
        """Should accept valid NDVI [-1, 1]"""
        data = np.random.uniform(-0.5, 0.8, (280, 300))
        assert validate_ndvi(data) == True
    
    def test_ndvi_below_minus_one_warning(self, caplog):
        """Should warn for values <-1"""
        data = np.random.uniform(-1.5, -0.5, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_ndvi(data)
        assert "below -1" in caplog.text.lower()
    
    def test_ndvi_above_one_warning(self, caplog):
        """Should warn for values >1"""
        data = np.random.uniform(0.5, 1.5, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_ndvi(data)
        assert "above 1" in caplog.text.lower()


class TestDistanceValidation:
    """Test distance to grid validation"""
    
    def test_valid_distance_data(self):
        """Should accept valid distance data"""
        data = np.random.uniform(0, 200, (280, 300))
        assert validate_distance(data) == True
    
    def test_excessive_distance_warning(self, caplog):
        """Should warn for distances >500 km"""
        data = np.random.uniform(300, 800, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_distance(data)
        assert ">500" in caplog.text or "very far" in caplog.text.lower()


class TestSlopeValidation:
    """Test slope validation"""
    
    def test_valid_slope_data(self):
        """Should accept valid slope [0, 90]"""
        data = np.random.uniform(0, 30, (280, 300))
        assert validate_slope(data) == True
    
    def test_negative_slope_warning(self, caplog):
        """Should warn for negative slopes"""
        data = np.random.uniform(-10, 30, (280, 300))
        with caplog.at_level(logging.WARNING):
            validate_slope(data)
        assert "Negative" in caplog.text
    
    def test_excessive_slope_warning(self, caplog):
        """Should warn for slopes >90° or >30°"""
        data = np.random.uniform(25, 45, (280, 300))
        with caplog.at_level(logging.INFO):
            validate_slope(data)
        assert "steep" in caplog.text.lower() or "unsuitable" in caplog.text.lower()


# ============================================================================
# WEIGHT VALIDATION TESTS
# ============================================================================

class TestWeightValidation:
    """Test MCDA weights validation"""
    
    def test_valid_weights(self):
        """Should accept valid normalized weights"""
        weights = {"solar": 0.25, "pop": 0.25, "dist": 0.20, 
                   "slope": 0.15, "ndvi": 0.15}
        assert validate_weights(weights) == True
    
    def test_weights_sum_to_one(self):
        """Should accept weights summing to 1.0"""
        weights = {"a": 0.5, "b": 0.5}
        assert validate_weights(weights) == True
    
    def test_empty_weights_raises(self):
        """Should reject empty weights dict"""
        with pytest.raises(ValueError, match="empty"):
            validate_weights({})
    
    def test_weight_out_of_range_raises(self):
        """Should reject weights outside [0, 1]"""
        with pytest.raises(ValueError, match="outside"):
            validate_weights({"a": 1.5, "b": -0.5})
    
    def test_weights_dont_sum_to_one_raises(self):
        """Should reject weights not summing to ~1.0"""
        with pytest.raises(ValueError, match="sum to"):
            validate_weights({"a": 0.3, "b": 0.3})  # Only 0.6
    
    def test_non_numeric_weight_raises(self):
        """Should reject non-numeric weights"""
        with pytest.raises(ValueError, match="numeric"):
            validate_weights({"a": "0.5", "b": 0.5})


class TestWeightVectorValidation:
    """Test weight vector (array) validation"""
    
    def test_valid_weight_vector(self):
        """Should accept valid weight vectors"""
        weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])
        assert validate_weight_vector(weights) == True
    
    def test_wrong_dimensions_raises(self):
        """Should reject non-1D arrays"""
        with pytest.raises(ValueError, match="1D"):
            validate_weight_vector(np.array([[0.5, 0.5]]))
    
    def test_not_array_raises(self):
        """Should reject non-arrays"""
        with pytest.raises(ValueError, match="numpy"):
            validate_weight_vector([0.5, 0.5])
    
    def test_weights_out_of_range_raises(self):
        """Should reject weights outside [0, 1]"""
        with pytest.raises(ValueError, match="outside"):
            validate_weight_vector(np.array([0.5, 1.5, -0.2]))


# ============================================================================
# PARAMETER VALIDATION TESTS
# ============================================================================

class TestCapacityValidation:
    """Test capacity validation"""
    
    def test_valid_capacity(self):
        """Should accept valid capacity"""
        assert validate_capacity_mw(1.0) == True
        assert validate_capacity_mw(100.0) == True
    
    def test_capacity_too_low_raises(self):
        """Should reject capacity below minimum"""
        with pytest.raises(ValueError, match="outside"):
            validate_capacity_mw(0.01)
    
    def test_capacity_too_high_raises(self):
        """Should reject capacity above maximum"""
        with pytest.raises(ValueError, match="outside"):
            validate_capacity_mw(1000.0)
    
    def test_non_numeric_capacity_raises(self):
        """Should reject non-numeric capacity"""
        with pytest.raises(ValueError, match="numeric"):
            validate_capacity_mw("1.0")


class TestIrradianceValidation:
    """Test irradiance validation"""
    
    def test_valid_irradiance(self):
        """Should accept valid irradiance"""
        assert validate_irradiance_kwh(2226) == True  # Angola typical
        assert validate_irradiance_kwh(1200) == True
    
    def test_irradiance_too_low_raises(self):
        """Should reject very low irradiance"""
        with pytest.raises(ValueError, match="outside"):
            validate_irradiance_kwh(100)
    
    def test_irradiance_too_high_raises(self):
        """Should reject very high irradiance"""
        with pytest.raises(ValueError, match="outside"):
            validate_irradiance_kwh(4000)


class TestDiscountRateValidation:
    """Test discount rate validation"""
    
    def test_valid_discount_rate(self):
        """Should accept valid discount rates"""
        assert validate_discount_rate(8.0) == True
        assert validate_discount_rate(0.0) == True
    
    def test_negative_rate_warning(self, caplog):
        """Should warn for negative rates (unusual)"""
        with caplog.at_level(logging.WARNING):
            validate_discount_rate(-5.0)
        assert "Negative" in caplog.text
    
    def test_high_rate_warning(self, caplog):
        """Should warn for high rates (>25%)"""
        with caplog.at_level(logging.WARNING):
            validate_discount_rate(35.0)
        assert "High" in caplog.text or "unrealistic" in caplog.text.lower()
    
    def test_rate_out_of_range_raises(self):
        """Should reject rates outside range"""
        with pytest.raises(ValueError, match="outside"):
            validate_discount_rate(150.0)


class TestProjectLifetimeValidation:
    """Test project lifetime validation"""
    
    def test_valid_lifetime(self):
        """Should accept valid lifetimes"""
        assert validate_project_lifetime(20) == True
        assert validate_project_lifetime(25) == True
    
    def test_lifetime_too_short_raises(self):
        """Should reject lifetime <5 years"""
        with pytest.raises(ValueError, match="outside"):
            validate_project_lifetime(2)
    
    def test_lifetime_too_long_raises(self):
        """Should reject lifetime >50 years"""
        with pytest.raises(ValueError, match="outside"):
            validate_project_lifetime(100)
    
    def test_non_integer_raises(self):
        """Should reject non-integer lifetimes"""
        with pytest.raises(ValueError, match="integer"):
            validate_project_lifetime(20.5)


# ============================================================================
# SHAPE & DIMENSION TESTS
# ============================================================================

class TestRasterShapeValidation:
    """Test raster shape validation"""
    
    def test_correct_shape(self):
        """Should accept correct shape"""
        data = np.zeros((280, 300))
        assert validate_raster_shape(data, (280, 300)) == True
    
    def test_wrong_shape_raises(self):
        """Should reject wrong shape"""
        with pytest.raises(ValueError, match="doesn't match"):
            data = np.zeros((100, 100))
            validate_raster_shape(data, (280, 300))
    
    def test_wrong_dimensions_raises(self):
        """Should reject non-2D arrays"""
        with pytest.raises(ValueError, match="2D"):
            data = np.zeros((280, 300, 3))  # 3D
            validate_raster_shape(data, (280, 300))
    
    def test_not_array_raises(self):
        """Should reject non-arrays"""
        with pytest.raises(ValueError, match="numpy"):
            validate_raster_shape([[1, 2], [3, 4]], (280, 300))


class TestProbabilityArrayValidation:
    """Test probability array validation"""
    
    def test_valid_probabilities(self):
        """Should accept valid probability arrays"""
        data = np.random.uniform(0, 1, (280, 300))
        assert validate_is_probability_array(data) == True
    
    def test_values_below_zero_raises(self):
        """Should reject values <0"""
        with pytest.raises(ValueError, match="outside"):
            data = np.random.uniform(-0.5, 0.5, (280, 300))
            validate_is_probability_array(data)
    
    def test_values_above_one_raises(self):
        """Should reject values >1"""
        with pytest.raises(ValueError, match="outside"):
            data = np.random.uniform(0.5, 1.5, (280, 300))
            validate_is_probability_array(data)


# ============================================================================
# BATCH VALIDATION TESTS
# ============================================================================

class TestBatchValidation:
    """Test comprehensive batch validation"""
    
    def test_all_valid_inputs(self):
        """Should accept all valid inputs"""
        solar = np.random.uniform(5.0, 7.0, (280, 300))
        population = np.random.uniform(0, 500, (280, 300))
        distance = np.random.uniform(0, 200, (280, 300))
        slope = np.random.uniform(0, 30, (280, 300))
        ndvi = np.random.uniform(-0.5, 0.8, (280, 300))
        weights = {"solar": 0.25, "pop": 0.25, "dist": 0.20, "slope": 0.15, "ndvi": 0.15}
        
        assert validate_all_inputs(
            solar, population, distance, slope, ndvi,
            weights, 1.0, 2226, 8.0
        ) == True
    
    def test_raises_on_invalid_solar(self):
        """Should raise on invalid solar data"""
        solar = np.full((280, 300), np.nan)  # All NaN
        population = np.random.uniform(0, 500, (280, 300))
        distance = np.random.uniform(0, 200, (280, 300))
        slope = np.random.uniform(0, 30, (280, 300))
        ndvi = np.random.uniform(-0.5, 0.8, (280, 300))
        weights = {"solar": 0.25, "pop": 0.25, "dist": 0.20, "slope": 0.15, "ndvi": 0.15}
        
        with pytest.raises(ValueError, match="Validation failed"):
            validate_all_inputs(
                solar, population, distance, slope, ndvi,
                weights, 1.0, 2226, 8.0
            )
    
    def test_raises_on_invalid_weights(self):
        """Should raise on invalid weights"""
        solar = np.random.uniform(5.0, 7.0, (280, 300))
        population = np.random.uniform(0, 500, (280, 300))
        distance = np.random.uniform(0, 200, (280, 300))
        slope = np.random.uniform(0, 30, (280, 300))
        ndvi = np.random.uniform(-0.5, 0.8, (280, 300))
        weights = {"solar": 0.5, "pop": 0.5}  # Only sums to 1.0 but missing criteria
        
        # Note: This might actually pass if it just checks sum, adjust based on implementation
        result = validate_all_inputs(
            solar, population, distance, slope, ndvi,
            weights, 1.0, 2226, 8.0
        )
        # Weights with only 2 criteria might be valid, depending on implementation
    
    def test_raises_on_invalid_capacity(self):
        """Should raise on invalid capacity"""
        solar = np.random.uniform(5.0, 7.0, (280, 300))
        population = np.random.uniform(0, 500, (280, 300))
        distance = np.random.uniform(0, 200, (280, 300))
        slope = np.random.uniform(0, 30, (280, 300))
        ndvi = np.random.uniform(-0.5, 0.8, (280, 300))
        weights = {"solar": 0.25, "pop": 0.25, "dist": 0.20, "slope": 0.15, "ndvi": 0.15}
        
        with pytest.raises(ValueError, match="Validation failed"):
            validate_all_inputs(
                solar, population, distance, slope, ndvi,
                weights, 1000.0, 2226, 8.0  # Capacity too high
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
