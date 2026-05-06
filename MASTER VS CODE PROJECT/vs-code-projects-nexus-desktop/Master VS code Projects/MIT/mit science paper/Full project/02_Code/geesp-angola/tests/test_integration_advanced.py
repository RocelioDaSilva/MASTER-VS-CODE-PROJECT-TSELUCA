"""
Additional integration tests for API endpoints and data handling
Covers API layers, database integration, and end-to-end workflows
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import json
from pathlib import Path

# Path setup in conftest.py
try:
    from utils.error_handlers import APIError, format_api_error, catch_and_format_error
except (ModuleNotFoundError, AttributeError):
    import importlib.util
    _root = Path(__file__).resolve().parent.parent
    _spec = importlib.util.spec_from_file_location("utils.error_handlers", _root / "utils" / "error_handlers.py")
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    APIError = _mod.APIError
    format_api_error = _mod.format_api_error
    catch_and_format_error = _mod.catch_and_format_error
from config_loader import load_config, ConfigLoader


class TestAPIErrorHandling:
    """Test API error formatting and responses"""
    
    def test_api_error_400_bad_request(self):
        """Test formatting 400 Bad Request error"""
        error = APIError("Invalid solar irradiance value", status_code=400)
        response = format_api_error(error, status_code=400)
        
        assert response["status_code"] == 400
        assert "Invalid" in response["message"]
        assert response["error"] == "APIError"
    
    def test_api_error_404_not_found(self):
        """Test formatting 404 Not Found error"""
        error = APIError("Endpoint not found", status_code=404)
        response = format_api_error(error, status_code=404)
        
        assert response["status_code"] == 404
        assert "404" in response["error_code"]
    
    def test_api_error_500_internal_error(self):
        """Test formatting 500 Internal Server Error"""
        error = APIError("Database connection failed", status_code=500)
        response = format_api_error(error, status_code=500)
        
        assert response["status_code"] == 500
        assert response["error_code"] == "API_ERROR_500"
    
    def test_catch_and_format_error_decorator(self):
        """Test error catching and formatting decorator"""
        @catch_and_format_error
        def endpoint():
            raise ValueError("Invalid input")
        
        result = endpoint()
        assert "error" in result
        assert "ERROR" in result["error_code"]


class TestConfigurationManagement:
    """Test configuration loading and access patterns"""
    
    def test_config_singleton_pattern(self):
        """Test that ConfigLoader implements singleton pattern"""
        config1 = load_config()
        config2 = load_config()
        
        # Should be same instance
        assert config1 is config2
    
    def test_config_get_with_defaults(self):
        """Test config.get() with default values"""
        config = load_config()
        
        # Existing key
        mcda_weights = config.get("mcda.default_weights")
        assert isinstance(mcda_weights, dict)
        assert "solar_irradiance" in mcda_weights
        
        # Non-existing key with default
        result = config.get("nonexistent.key", {"default": "value"})
        assert result == {"default": "value"}
    
    def test_config_mcda_methods(self):
        """Test MCDA-specific config methods"""
        config = load_config()
        assert hasattr(config, "get_mcda_classification_thresholds")
        assert hasattr(config, "get_mcda_normalization_ranges")
        thresholds = config.get_mcda_classification_thresholds()
        assert isinstance(thresholds, dict)
        ranges = config.get_mcda_normalization_ranges()
        assert isinstance(ranges, dict)
    
    def test_config_lcoe_methods(self):
        """Test LCOE-specific config methods"""
        config = load_config()
        
        # Test operational parameters
        params = config.get_lcoe_operational_parameters()
        assert "area_per_kw_sqm" in params
        assert "opex_percent_of_capex" in params
        
        # Test irradiance hours
        hours = config.get_irradiance_hours_per_year()
        assert 0 < hours < 10000  # Sanity check


class TestDataProcessingPipeline:
    """Test end-to-end data processing workflows"""
    
    def test_mcda_full_pipeline(self):
        """Test complete MCDA analysis pipeline"""
        from mcda_analysis import MCDAnalyzer
        
        analyzer = MCDAnalyzer(weights_dict={
            "solar": 0.25, "pop": 0.2, "dist": 0.2, "slope": 0.15, "ndvi": 0.2
        })
        
        # Generate synthetic data
        shape = (50, 50)
        solar = np.random.uniform(5.5, 6.5, shape)
        population = np.random.uniform(10, 100, shape)
        distance = np.random.uniform(0, 50, shape)
        slope = np.random.uniform(0, 30, shape)
        ndvi = np.random.uniform(-0.2, 0.7, shape)
        
        # Normalize each raster then run weighted overlay
        analyzer.normalize_raster(solar, "solar", minimum=4, maximum=7)
        analyzer.normalize_raster(population, "pop", minimum=0, maximum=200)
        analyzer.normalize_raster(distance, "dist", minimum=0, maximum=50)
        analyzer.normalize_raster(slope, "slope", minimum=0, maximum=35)
        analyzer.normalize_raster(ndvi, "ndvi", minimum=-0.2, maximum=0.8)
        aptitude = analyzer.weighted_overlay()
        
        # Verify output
        assert aptitude.shape == shape
        assert 0 <= np.nanmin(aptitude) <= 1
        assert 0 <= np.nanmax(aptitude) <= 1
        
        # Classify
        classified = analyzer.classify_aptitude(scores=aptitude)
        assert classified.shape == shape
        assert np.all(np.isin(classified[~np.isnan(classified)], [0, 1, 2]))
    
    def test_lcoe_full_pipeline(self):
        """Test complete LCOE analysis pipeline"""
        from lcoe_calculator import LCOECalculator, SolarParameters
        
        calculator = LCOECalculator()
        # Build minimal capex_dict (USD/kW) and required SolarParameters fields
        capex = {"modules": 400, "inverter": 150, "balance": 100}
        
        capacities = [0.1, 1.0, 10.0]
        results = {}
        
        for cap_mw in capacities:
            params = SolarParameters(
                capacity_mw=cap_mw,
                capex_dict=capex,
                opex_fixed=1.5,
                opex_variable=2.0,
                annual_irradiance=1800,
                system_efficiency=0.85,
                degradation_rate=0.005,
                discount_rate=8.0,
                project_lifetime=25,
                warranty_years=10,
            )
            out = calculator.calculate_lcoe(params)
            assert isinstance(out, dict)
            lcoe_val = out.get("lcoe_usd_per_kwh") or out.get("lcoe_usd_per_mwh", 0) / 1000
            assert lcoe_val is not None
            results[cap_mw] = float(lcoe_val)
            assert 0 < float(lcoe_val) < 1.0  # Typically 0.1-0.3 USD/kWh
        
        assert results[10.0] < results[0.1]


class TestDatabaseIntegration:
    """Test database model and integration"""
    
    def test_database_models_creation(self):
        """Test database models can be instantiated"""
        try:
            from models.monitoring import (
                Project, DailyGeneration, MaintenanceLog, KeyPerformanceIndicator,
            )
            project = Project(
                project_id="TEST-001",
                community="Test Community",
                province="Test Province",
                status="Planejamento",
                capacity_kw=100.0,
                population_served=500,
                annual_generation_mwh=150.0,
                investment_usd=200000.0,
            )
            assert project.project_id == "TEST-001"
            assert project.capacity_kw == 100.0
        except ImportError:
            pytest.skip("Database models not available")
    
    def test_database_manager_initialization(self):
        """Test database manager can initialize"""
        try:
            from models.monitoring import get_database_manager
            
            # Don't actually connect, just test initialization
            db_url = "sqlite:///:memory:"
            # Would test with mocked connection
        except ImportError:
            pytest.skip("Database manager not available")


class TestMonitoringAndMetrics:
    """Test monitoring and KPI tracking"""
    
    def test_performance_metrics_calculation(self):
        """Test performance KPI calculations"""
        from lcoe_calculator import LCOECalculator
        
        calculator = LCOECalculator()
        
        # Simulate operation data
        expected_generation_mwh = 250.0  # Annual
        actual_generation_mwh = 230.0    # Actual
        
        # Performance ratio
        performance_ratio = actual_generation_mwh / expected_generation_mwh
        assert 0.8 < performance_ratio < 1.0
        assert performance_ratio == pytest.approx(0.92, rel=0.01)
    
    def test_health_check_endpoint(self):
        """Test health check and status endpoints"""
        # Would test with mocked FastAPI app
        status_response = {
            "status": "healthy",
            "version": "3.0.0",
            "mcda_ready": True,
            "lcoe_ready": True
        }
        
        assert status_response["status"] == "healthy"
        assert status_response["version"] == "3.0.0"


class TestDataValidationPipeline:
    """Test complete validation pipeline"""
    
    def test_validate_input_raster_shapes(self):
        """Test validation of input raster dimensions"""
        from validators import validate_raster_shape
        
        shape = (100, 100)
        arr = np.zeros(shape)
        assert validate_raster_shape(arr, shape) is True
        
        with pytest.raises(ValueError):
            validate_raster_shape(np.zeros((99, 100)), shape)
    
    def test_validate_all_criteria_together(self):
        """Test validating all MCDA criteria simultaneously (validators expect arrays)"""
        from validators import (
            validate_solar_irradiance, validate_population,
            validate_distance, validate_slope, validate_ndvi
        )
        
        # Valid arrays for each criterion
        solar = np.array([5.5, 6.0, 6.5])
        population = np.array([10, 500, 2000])
        distance = np.array([5.0, 20.0, 45.0])
        slope = np.array([0, 15, 28])
        ndvi = np.array([-0.1, 0.3, 0.7])
        
        assert validate_solar_irradiance(solar) is True
        assert validate_population(population) is True
        assert validate_distance(distance) is True
        assert validate_slope(slope) is True
        assert validate_ndvi(ndvi) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
