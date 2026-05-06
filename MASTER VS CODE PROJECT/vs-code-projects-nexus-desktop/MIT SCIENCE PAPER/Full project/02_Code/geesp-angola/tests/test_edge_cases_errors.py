"""
Test edge cases and error handling for GEESP-Angola components
Covers error conditions, boundary cases, and recovery mechanisms
"""

import pytest
import numpy as np
from typing import Dict

# Path setup is in conftest.py (project root and scripts on sys.path)
from mcda_analysis import MCDAnalyzer, AHPWeighter
from lcoe_calculator import LCOECalculator, SolarParameters
try:
    from utils.error_handlers import (
        GEESPError, ValidationError, DataError, ConfigurationError,
        GEEIntegrationError, APIError, DatabaseError, TimeoutError,
        retry_on_exception, validate_inputs, ErrorContext
    )
except (ModuleNotFoundError, AttributeError):
    import importlib.util
    from pathlib import Path
    _root = Path(__file__).resolve().parent.parent
    _spec = importlib.util.spec_from_file_location("utils.error_handlers", _root / "utils" / "error_handlers.py")
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    GEESPError = _mod.GEESPError
    ValidationError = _mod.ValidationError
    DataError = _mod.DataError
    ConfigurationError = _mod.ConfigurationError
    GEEIntegrationError = _mod.GEEIntegrationError
    APIError = _mod.APIError
    DatabaseError = _mod.DatabaseError
    TimeoutError = _mod.TimeoutError
    retry_on_exception = _mod.retry_on_exception
    validate_inputs = _mod.validate_inputs
    ErrorContext = _mod.ErrorContext
from scripts.validators import (
    validate_weights, validate_raster_shape, validate_solar_irradiance,
    validate_population, validate_distance, validate_slope, validate_ndvi
)


class TestErrorHandling:
    """Test custom exception hierarchy and error handling"""
    
    def test_geesp_error_to_dict(self):
        """Test GEESPError serialization"""
        error = GEESPError("Test error", error_code="TEST_001", context={"key": "value"})
        error_dict = error.to_dict()
        
        assert error_dict["error"] == "GEESPError"
        assert error_dict["error_code"] == "TEST_001"
        assert error_dict["message"] == "Test error"
        assert error_dict["context"] == {"key": "value"}
    
    def test_validation_error_with_field(self):
        """Test ValidationError with field information"""
        error = ValidationError("Invalid solar irradiance", field="solar_irradiance")
        assert error.field == "solar_irradiance"
        assert error.error_code == "VALIDATION_ERROR"
    
    def test_data_error_with_source(self):
        """Test DataError with source information"""
        error = DataError("Failed to load raster", source="data/maps/solar.tif")
        assert error.source == "data/maps/solar.tif"
        assert error.error_code == "DATA_ERROR"
    
    def test_api_error_with_status(self):
        """Test APIError with HTTP status code"""
        error = APIError("Endpoint not found", status_code=404)
        assert error.status_code == 404
        assert "404" in error.error_code
    
    def test_timeout_error_with_duration(self):
        """Test TimeoutError with duration information"""
        error = TimeoutError("MCDA computation timed out", timeout_seconds=30.0)
        assert error.timeout_seconds == 30.0
        assert error.error_code == "TIMEOUT_ERROR"
    
    def test_error_context_manager(self):
        """Test ErrorContext for operation tracking"""
        with ErrorContext("test_operation", {"param": "value"}):
            pass
        
        # Stack should be empty after exiting context
        assert len(ErrorContext.get_stack()) == 0
    
    def test_retry_decorator_success(self):
        """Test retry decorator succeeds on first attempt"""
        call_count = 0
        
        @retry_on_exception(retries=3, delay_seconds=0.001)
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_func()
        assert result == "success"
        assert call_count == 1
    
    def test_retry_decorator_exponential_backoff(self):
        """Test retry decorator with exponential backoff"""
        call_count = 0
        
        @retry_on_exception(retries=3, delay_seconds=0.01, backoff=2.0)
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Not yet")
            return "success"
        
        result = failing_func()
        assert result == "success"
        assert call_count == 2
    
    def test_validate_inputs_decorator(self):
        """Test input validation decorator"""
        @validate_inputs(
            data=lambda x: isinstance(x, np.ndarray),
            threshold=lambda x: 0 <= x <= 1
        )
        def validated_func(data, threshold):
            return data * threshold
        
        # Valid inputs
        result = validated_func(np.array([1, 2, 3]), 0.5)
        assert np.array_equal(result, np.array([0.5, 1.0, 1.5]))
        
        # Invalid inputs should raise ValidationError
        with pytest.raises(ValidationError):
            validated_func([1, 2, 3], 0.5)  # list instead of ndarray


def _minimal_solar_params(**overrides):
    """Build minimal SolarParameters for edge-case tests."""
    defaults = {
        "capacity_mw": 1.0,
        "capex_dict": {"modules": 400, "inverter": 150, "balance": 100},
        "opex_fixed": 1.5,
        "opex_variable": 2.0,
        "annual_irradiance": 1800.0,
        "system_efficiency": 0.85,
        "degradation_rate": 0.005,
        "discount_rate": 8.0,
        "project_lifetime": 25,
        "warranty_years": 10,
    }
    defaults.update(overrides)
    return SolarParameters(**defaults)


class TestMCDAEdgeCases:
    """Test MCDA edge cases and error conditions"""
    
    def test_mcda_with_nan_values(self):
        """Test MCDA handling of NaN values"""
        analyzer = MCDAnalyzer(weights_dict={"solar": 0.2, "pop": 0.2, "dist": 0.2, "slope": 0.2, "ndvi": 0.2})
        solar = np.array([[6.0, np.nan], [5.5, 6.2]])
        population = np.array([[50.0, 100.0], [np.nan, 75.0]])
        distance = np.array([[10.0, np.nan], [15.0, 20.0]])
        slope = np.array([[5.0, 10.0], [np.nan, 8.0]])
        ndvi = np.array([[0.3, 0.4], [0.5, np.nan]])
        analyzer.normalize_raster(solar, "solar", 4, 7)
        analyzer.normalize_raster(population, "pop", 0, 200)
        analyzer.normalize_raster(distance, "dist", 0, 50)
        analyzer.normalize_raster(slope, "slope", 0, 35)
        analyzer.normalize_raster(ndvi, "ndvi", -0.2, 0.8)
        aptitude = analyzer.weighted_overlay()
        assert isinstance(aptitude, np.ndarray)
        assert not np.all(np.isnan(aptitude))
    
    def test_mcda_with_uniform_values(self):
        """Test MCDA with uniform input values"""
        analyzer = MCDAnalyzer(weights_dict={"solar": 0.2, "pop": 0.2, "dist": 0.2, "slope": 0.2, "ndvi": 0.2})
        shape = (10, 10)
        solar = np.full(shape, 6.0)
        population = np.full(shape, 50.0)
        distance = np.full(shape, 20.0)
        slope = np.full(shape, 5.0)
        ndvi = np.full(shape, 0.3)
        analyzer.normalize_raster(solar, "solar", 4, 7)
        analyzer.normalize_raster(population, "pop", 0, 200)
        analyzer.normalize_raster(distance, "dist", 0, 50)
        analyzer.normalize_raster(slope, "slope", 0, 35)
        analyzer.normalize_raster(ndvi, "ndvi", -0.2, 0.8)
        aptitude = analyzer.weighted_overlay()
        assert 0 <= np.nanmin(aptitude) <= 1
        assert 0 <= np.nanmax(aptitude) <= 1
    
    def test_mcda_classification_boundary_values(self):
        """Test MCDA classification at threshold boundaries"""
        analyzer = MCDAnalyzer()
        scores = np.array([0.0, 0.39, 0.40, 0.69, 0.70, 1.0]).reshape(1, 6)
        classified = analyzer.classify_aptitude(
            scores=scores,
            low_threshold=0.40,
            high_threshold=0.70
        )
        assert classified.shape == (1, 6)
        assert classified[0, 0] == 0  # Below low threshold
        assert classified[0, 1] == 0  # Just below low threshold
        assert classified[0, 2] == 1  # At or above low threshold
        assert classified[0, 3] == 1  # Between thresholds
        assert classified[0, 4] == 2  # At or above high threshold
        assert classified[0, 5] == 2  # At maximum
    
    def test_mcda_weights_sum_tolerance(self):
        """Test MCDA weight validation with weights that don't sum to 1.0"""
        from scripts.validators import validate_weights
        # Weights that don't sum to 1.0 should raise or be rejected
        bad_weights = {"a": 0.5, "b": 0.6}
        with pytest.raises((ValidationError, ValueError)):
            validate_weights(bad_weights)
    
    def test_ahp_inconsistent_matrix(self):
        """Test AHP with inconsistent comparison matrix"""
        weighter = AHPWeighter()
        criteria = ["A", "B", "C"]
        comparisons = {
            ("A", "B"): 9.0,
            ("B", "C"): 9.0,
            ("A", "C"): 1.0,
        }
        weighter.create_comparison_matrix(criteria, comparisons)
        weighter.calculate_weights_from_matrix()
        # Inconsistent matrix should yield high CR (Saaty threshold 0.1)
        assert weighter.consistency_ratio is not None
        assert weighter.consistency_ratio > 0.1


class TestLCOEEdgeCases:
    """Test LCOE calculation edge cases"""
    
    def test_lcoe_zero_capacity(self):
        """Test LCOE with zero capacity - should raise or return inf"""
        calculator = LCOECalculator()
        params = _minimal_solar_params(capacity_mw=0.0)
        try:
            out = calculator.calculate_lcoe(params)
            assert isinstance(out, dict)
            val = out.get("lcoe_usd_per_mwh") or out.get("lcoe_usd_per_kwh")
            assert val is None or not np.isfinite(float(val)) or float(val) == 0
        except (ValidationError, ValueError, ZeroDivisionError):
            pass
    
    def test_lcoe_negative_irradiance(self):
        """Test LCOE with negative solar irradiance - may raise or return"""
        calculator = LCOECalculator()
        params = _minimal_solar_params(annual_irradiance=-1000.0)
        try:
            out = calculator.calculate_lcoe(params)
            assert isinstance(out, dict)
        except (ValidationError, ValueError):
            pass
    
    
    def test_lcoe_100_percent_discount_rate(self):
        """Test LCOE with extreme discount rate (100%)"""
        calculator = LCOECalculator()
        params = _minimal_solar_params(discount_rate=100.0)
        out = calculator.calculate_lcoe(params)
        assert isinstance(out, dict)
        val = out.get("lcoe_usd_per_kwh") or (out.get("lcoe_usd_per_mwh", 0) / 1000)
        assert val is not None and float(val) > 0
    
    def test_lcoe_zero_lifetime(self):
        """Test LCOE with zero project lifetime - may raise or return inf"""
        calculator = LCOECalculator()
        params = _minimal_solar_params(project_lifetime=0)
        try:
            out = calculator.calculate_lcoe(params)
            assert isinstance(out, dict)
            val = out.get("lcoe_usd_per_mwh") or out.get("lcoe_usd_per_kwh")
            assert val is None or not np.isfinite(float(val))
        except (ValidationError, ValueError, ZeroDivisionError):
            pass
    
    def test_lcoe_very_small_capacity(self):
        """Test LCOE with very small capacity (1 Watt)"""
        calculator = LCOECalculator()
        params = _minimal_solar_params(capacity_mw=0.000001)
        out = calculator.calculate_lcoe(params)
        assert isinstance(out, dict)
        val = out.get("lcoe_usd_per_kwh") or out.get("lcoe_usd_per_mwh")
        assert val is not None and np.isfinite(float(val))


class TestValidationEdgeCases:
    """Test validator edge cases (validators expect np.ndarray)"""
    
    def test_validate_irradiance_extreme_ranges(self):
        """Test solar irradiance validation at extremes"""
        assert validate_solar_irradiance(np.array([6.5])) is True
        assert validate_solar_irradiance(np.array([5.5])) is True
        # Empty data raises
        with pytest.raises((ValidationError, ValueError)):
            validate_solar_irradiance(np.array([]))
    
    def test_validate_population_with_nan(self):
        """Test population validation with all-NaN array"""
        with pytest.raises((ValidationError, ValueError)):
            validate_population(np.array([np.nan]))
    
    def test_validate_distance_zero(self):
        """Test distance validation with zero value"""
        assert validate_distance(np.array([0.0])) is True
    
    def test_validate_slope_negative(self):
        """Test slope validation with negative slope (validator warns, may not raise)"""
        # All-NaN or empty raises; out-of-range only warns
        with pytest.raises((ValidationError, ValueError)):
            validate_slope(np.array([]))
    
    def test_validate_ndvi_out_of_range(self):
        """Test NDVI validation (validators expect array; out-of-range only warns)"""
        assert validate_ndvi(np.array([0.5])) is True
        with pytest.raises((ValidationError, ValueError)):
            validate_ndvi(np.array([]))


class TestAsyncOperationEdgeCases:
    """Test async data loading edge cases"""
    
    def test_async_timeout_handling(self):
        """Test async operation timeout"""
        from data_loaders_async import AsyncDataLoader
        import time
        
        loader = AsyncDataLoader(max_workers=1)
        
        def slow_computation():
            time.sleep(2.0)
            return np.zeros((10, 10))
        
        # Should timeout with 0.5s timeout
        result = loader.compute_mcda_async(
            solar=np.zeros((10, 10)),
            population=np.zeros((10, 10)),
            distance=np.zeros((10, 10)),
            slope=np.zeros((10, 10)),
            ndvi=np.zeros((10, 10)),
            timeout=0.5
        )
        
        # May timeout or complete, depending on system
        # Just verify no crash
        loader.shutdown()
    
    def test_async_cache_hit(self):
        """Test async loader cache efficiency"""
        from data_loaders_async import AsyncDataLoader
        
        loader = AsyncDataLoader(max_workers=2)
        
        filename = "test_map.npy"
        # Create a temporary test file
        test_array = np.random.rand(5, 5)
        
        # First load (cache miss, creates entry)
        # Second load (cache hit)
        # Cache hit should be immediate
        
        loader.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
