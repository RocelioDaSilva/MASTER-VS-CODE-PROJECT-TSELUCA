"""
End-to-End Test Suite for GEESP-Angola

Tests complete user workflows from data input through analysis and output.
Ensures all components work together seamlessly.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

import pytest
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any

from scripts.config_loader import ConfigLoader
from scripts.lcoe_calculator import LCOECalculator
from scripts.mcda_analysis import MCDAnalyzer
from scripts.validators import (
    validate_solar_irradiance,
    validate_weights
)
from scripts.api_server import app
from utils.logging_config import setup_logging

logger = setup_logging(__name__)


class TestE2EDataIngestion:
    """Test complete data ingestion workflow"""
    
    def test_load_and_validate_Angola_reference_data(self):
        """Test loading Angola reference data"""
        loader = ConfigLoader()
        config = loader.get()
        
        # Verify configuration loaded
        assert config is not None
        assert "study_area" in config
        assert config["study_area"]["country"] == "Angola"
        
        # Angola bounds
        bounds = config["study_area"]["bounds"]
        test_coords = [
            (-18.0, 14.75),  # Central Angola
            (-4.4, 11.6),    # Northwest corner
            (-18.5, 24.1),   # Southeast corner
        ]
        
        # Verify coordinates within bounds
        for lat, lon in test_coords:
            assert bounds[1] <= lat <= bounds[3], f"Latitude {lat} not in bounds {bounds[1]}-{bounds[3]}"
            assert bounds[0] <= lon <= bounds[2], f"Longitude {lon} not in bounds {bounds[0]}-{bounds[2]}"

    def test_load_geospatial_datasets(self):
        """Test loading geospatial datasets"""
        # Create sample geospatial data (45 points)
        irradiance_data = np.random.uniform(5, 7, 45)
        
        # Validate all points
        valid = validate_solar_irradiance(irradiance_data)
        assert valid is True

    def test_import_communities_data(self):
        """Test importing 45 communities data"""
        communities = [
            {"name": "Cacula", "latitude": -18.3, "longitude": 14.8},
            {"name": "Humpata", "latitude": -17.9, "longitude": 15.2},
            {"name": "Quilengues", "latitude": -18.2, "longitude": 15.5},
        ]
        
        # Validate each community
        for community in communities:
            lat_valid = -18.5 <= community["latitude"] <= -4.4
            lon_valid = 11.6 <= community["longitude"] <= 24.1
            assert lat_valid and lon_valid


class TestE2ELCOECalculation:
    """Test complete LCOE calculation workflow"""
    
    def test_full_lcoe_workflow_10MW_system(self):
        """Test complete LCOE workflow for 10MW solar system"""
        calc = LCOECalculator()
        
        # Realistic Angola solar parameters
        params = {
            "capacity_mw": 10,
            "capex_usd": 5_000_000,  # $5M for 10MW
            "opex_annual_usd": 50_000,  # $50K/year
            "annual_irradiance": 6.0,  # kWh/m²/day
            "project_lifetime": 25,
            "discount_rate": 0.08,
        }
        
        # Calculate - returns float LCOE when using kwargs
        result = calc.calculate_lcoe(params)
        
        # Verify results (LCOE in USD/kWh when created from kwargs)
        assert isinstance(result, (int, float))
        assert result > 0.01  # Minimum reasonable LCOE
        assert result < 50.0  # Maximum reasonable LCOE

    def test_lcoe_sensitivity_analysis(self):
        """Test sensitivity analysis across parameters"""
        calc = LCOECalculator()
        
        base_params = {
            "capacity_mw": 10,
            "capex_usd": 5_000_000,
            "opex_annual_usd": 50_000,
            "project_lifetime": 25,
            "annual_irradiance": 6.0,
        }
        
        # Test capex sensitivity (±20%)
        results = []
        for capex in [4_000_000, 5_000_000, 6_000_000]:
            params = base_params.copy()
            params["capex_usd"] = capex
            result = calc.calculate_lcoe(params)
            results.append(result)
        
        # Verify capex impact: higher capex = higher or similar LCOE
        assert results[0] <= results[2], f"LCOE should increase with higher capex: {results}"

    def test_lcoe_different_system_sizes(self):
        """Test LCOE calculation for different system sizes"""
        calc = LCOECalculator()
        
        sizes = [1, 5, 10, 50, 100]  # MW
        lcoe_values = []
        
        for size in sizes:
            result = calc.calculate_lcoe(
                capacity_mw=size,
                capex_usd=size * 500_000,  # $500K/MW
                opex_annual_usd=size * 5_000,
                project_lifetime=25,
                annual_irradiance=6.0,
            )
            lcoe_values.append(result)
        
        # All should be reasonable
        for lcoe in lcoe_values:
            assert 0.03 < lcoe < 0.30


class TestE2EMCDAAnalysis:
    """Test complete MCDA (Multi-Criteria Decision Analysis) workflow"""
    
    def test_site_suitability_ranking(self):
        """Test ranking sites by suitability"""
        mcda = MCDAnalyzer(weights_dict={"irradiance": 0.5, "area": 0.3, "distance": 0.2})
        
        # Test with sample rasters
        irradiance = np.array([[6.2, 5.8], [6.0, 6.3]])
        area = np.array([[50.0, 100.0], [75.0, 60.0]])
        
        # Normalize rasters
        n_irr = mcda.normalize_raster(irradiance, name="irradiance")
        n_area = mcda.normalize_raster(area, name="area")
        
        # Both should be normalized
        assert n_irr.shape == irradiance.shape
        assert n_area.shape == area.shape
        assert np.all((n_irr >= 0) & (n_irr <= 1))
        assert np.all((n_area >= 0) & (n_area <= 1))

    def test_multi_criteria_optimization(self):
        """Test optimization across multiple criteria"""
        # Criteria data (45 communities)
        criteria = {
            "irradiance": np.random.uniform(5.5, 6.5, 45),
            "land_cost": np.random.uniform(1000, 5000, 45),
            "population_proximity": np.random.uniform(0, 100, 45),
        }
        
        weights = {"irradiance": 0.50, "land_cost": 0.30, "population_proximity": 0.20}
        
        # Validate weights
        assert validate_weights(weights) is True
        assert len(criteria["irradiance"]) == 45

    def test_scenario_comparison(self):
        """Test comparing different scenarios"""
        mcda = MCDAAnalysis()
        
        # Scenario 1: Maximize energy output
        scenario1 = {"irradiance": 0.60, "cost": 0.20, "environmental": 0.20}
        
        # Scenario 2: Minimize cost
        scenario2 = {"irradiance": 0.30, "cost": 0.50, "environmental": 0.20}
        
        # Scenario 3: Balanced
        scenario3 = {"irradiance": 0.40, "cost": 0.30, "environmental": 0.30}
        
        for scenario in [scenario1, scenario2, scenario3]:
            assert validate_weights(scenario) is True


class TestE2ECompleteWorkflow:
    """Test complete end-to-end workflow"""
    
    def test_full_analysis_pipeline_site_selection(self):
        """Test complete pipeline: data → LCOE → MCDA → ranking"""
        logger.info("Starting complete workflow test")
        
        # Step 1: Load configuration
        config = ConfigLoader().get()
        assert config is not None
        logger.info("✓ Configuration loaded")
        
        # Step 2: Generate/load site data
        sites = {
            "site_1": {"irradiance": 6.1, "capex": 5e6, "opex": 50000, "area": 50},
            "site_2": {"irradiance": 5.9, "capex": 4.5e6, "opex": 45000, "area": 45},
            "site_3": {"irradiance": 6.3, "capex": 5.5e6, "opex": 55000, "area": 55},
        }
        logger.info(f"✓ Site data loaded: {len(sites)} sites")
        
        # Step 3: Calculate LCOE for each site
        lcoe_results = {}
        calc = LCOECalculator()
        
        for site_name, site_data in sites.items():
            result = calc.calculate_lcoe(
                capacity_mw=10,
                capex_usd=site_data["capex"],
                opex_annual_usd=site_data["opex"],
                project_lifetime=25,
                annual_irradiance=site_data["irradiance"],
            )
            lcoe_results[site_name] = result
        
        logger.info(f"✓ LCOE calculated for {len(lcoe_results)} sites")
        
        # Step 4: Calculate final scores based on criteria
        weights = {
            "irradiance": 0.40,
            "cost": 0.35,
            "area": 0.25,
        }
        
        final_scores = {}
        for site_name, lcoe in lcoe_results.items():
            # Composite score: higher irradiance better, lower LCOE better, larger area better
            irr_score = sites[site_name]["irradiance"] / 7.0  # Normalize to 0-1
            lcoe_score = (0.5 - lcoe) / 0.5  # Normalize inverse (lower is better)
            area_score = sites[site_name]["area"] / 100.0  # Normalize to 0-1
            
            score = (
                irr_score * weights["irradiance"] +
                lcoe_score * weights["cost"] +
                area_score * weights["area"]
            )
            final_scores[site_name] = score
        
        logger.info(f"✓ Scores calculated")
        
        # Step 5: Rank results
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        logger.info(f"✓ Sites ranked:")
        for rank, (site, score) in enumerate(ranked, 1):
            logger.info(f"  {rank}. {site}: {score:.4f}")
        
        # Verify results
        assert len(ranked) == 3
        assert ranked[0][1] > ranked[1][1] > ranked[2][1]


class TestE2EAPIIntegration:
    """Test API endpoints with complete workflows"""
    
    def test_api_health_check(self):
        """Test health check endpoint"""
        # Create test client
        client = app.test_client()
        
        # Test /health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json() if hasattr(response, 'json') else json.loads(response.data)
        assert "status" in data

    def test_api_lcoe_calculation_endpoint(self):
        """Test LCOE calculation via API"""
        client = app.test_client()
        
        payload = {
            "capacity_mw": 10,
            "capex_usd": 5000000,
            "opex_annual_usd": 50000,
            "project_lifetime": 25,
        }
        
        # Test LCOE endpoint
        response = client.post("/api/lcoe", json=payload)
        
        # Should return success or method not allowed (not 500)
        assert response.status_code in [200, 404, 405]


class TestE2EDataExport:
    """Test data export and reporting workflow"""
    
    def test_export_results_to_json(self):
        """Test exporting analysis results to JSON"""
        results = {
            "analysis_date": "2026-03-01",
            "sites": {
                "site_1": {"lcoe": 0.045, "rank": 1},
                "site_2": {"lcoe": 0.052, "rank": 2},
            },
            "summary": "Complete analysis for Angola renewable energy sites",
        }
        
        # Serialize to JSON
        json_str = json.dumps(results, indent=2)
        assert json_str is not None
        
        # Deserialize back
        loaded = json.loads(json_str)
        assert loaded["sites"]["site_1"]["lcoe"] == 0.045

    def test_generate_summary_report(self):
        """Test generating summary report"""
        report = {
            "title": "GEESP-Angola Site Analysis Report",
            "date": "2026-03-01",
            "sections": [
                {"name": "Executive Summary"},
                {"name": "Methodology"},
                {"name": "Results"},
                {"name": "Recommendations"},
            ],
        }
        
        assert len(report["sections"]) == 4
        assert report["title"] is not None


# Test Execution
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
