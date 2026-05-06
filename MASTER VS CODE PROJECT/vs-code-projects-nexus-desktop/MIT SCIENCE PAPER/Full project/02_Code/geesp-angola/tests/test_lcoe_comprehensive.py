"""
Comprehensive unit tests for LCOE Calculator module
Tests: capacity validation, cost calculations, technology comparison, edge cases
"""

import pytest
import numpy as np
import pandas as pd
from scripts.lcoe_calculator import LCOECalculator, SolarParameters


class TestSolarParametersDataclass:
    """Test SolarParameters dataclass validation"""

    def test_solar_parameters_creation(self):
        """Test creating valid SolarParameters instance"""
        params = SolarParameters(
            capacity_mw=0.5,
            capex_dict={"pv": 200, "inverter": 80},
            opex_fixed=2.0,
            opex_variable=5.0,
            annual_irradiance=2000,
            system_efficiency=0.85,
            degradation_rate=0.5,
            discount_rate=10.0,
            project_lifetime=25,
            warranty_years=10
        )
        assert params.capacity_mw == 0.5
        assert params.system_efficiency == 0.85
        assert params.project_lifetime == 25

    def test_solar_parameters_defaults(self):
        """Test location defaults to Angola"""
        params = SolarParameters(
            capacity_mw=0.5,
            capex_dict={},
            opex_fixed=2.0,
            opex_variable=5.0,
            annual_irradiance=2000,
            system_efficiency=0.85,
            degradation_rate=0.5,
            discount_rate=10.0,
            project_lifetime=25,
            warranty_years=10
        )
        assert params.location == "Angola"


class TestLCOECalculatorInit:
    """Test LCOECalculator initialization"""

    def test_calculator_init_with_location(self):
        """Test creating calculator with location"""
        calc = LCOECalculator(location="Luanda")
        assert calc.location == "Luanda"

    def test_calculator_init_default(self):
        """Test default location is Angola"""
        calc = LCOECalculator()
        assert calc.location == "Angola"

    def test_technology_costs_available(self):
        """Test that technology cost database is loaded"""
        calc = LCOECalculator()
        assert len(calc.TECHNOLOGY_COSTS) >= 2
        assert "PV_Fixed" in calc.TECHNOLOGY_COSTS
        assert "Hybrid_Solar_Diesel" in calc.TECHNOLOGY_COSTS


class TestLCOECalculations:
    """Test core LCOE calculation methods"""

    @pytest.fixture
    def calc(self):
        """Fixture: initialize calculator"""
        return LCOECalculator(location="Test_Site")

    def test_calculate_lcoe_basic(self, calc):
        """Test LCOE calculation with basic parameters"""
        lcoe = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=2000,
            discount_rate=10.0,
            project_lifetime=25
        )
        assert isinstance(lcoe, (int, float))
        assert lcoe > 0
        assert lcoe < 500  # Sanity check: LCOE should be reasonable for solar

    def test_calculate_lcoe_high_irradiance(self, calc):
        """Test that higher irradiance reduces LCOE"""
        lcoe_low = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=1500,
            discount_rate=10.0,
            project_lifetime=25
        )
        lcoe_high = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=2500,
            discount_rate=10.0,
            project_lifetime=25
        )
        assert lcoe_high < lcoe_low, "Higher irradiance should reduce LCOE"

    def test_calculate_lcoe_zero_capacity_raises(self, calc):
        """Test that zero capacity raises error"""
        with pytest.raises((ValueError, ZeroDivisionError)):
            calc.calculate_lcoe(
                capacity_mw=0.0,
                capex_usd=440_000,
                opex_annual_usd=5_000,
                annual_irradiance=2000,
                discount_rate=10.0,
                project_lifetime=25
            )

    def test_calculate_lcoe_negative_irradiance_raises(self, calc):
        """Test that negative irradiance raises error"""
        with pytest.raises(ValueError):
            calc.calculate_lcoe(
                capacity_mw=0.5,
                capex_usd=440_000,
                opex_annual_usd=5_000,
                annual_irradiance=-1000,
                discount_rate=10.0,
                project_lifetime=25
            )


class TestTechnologyComparison:
    """Test compare_technologies method"""

    @pytest.fixture
    def calc(self):
        return LCOECalculator(location="Test")

    def test_compare_technologies_runs(self, calc):
        """Test that technology comparison runs without error"""
        df = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        assert not df.empty
        assert "lcoe_usd_per_mwh" in df.columns

    def test_compare_technologies_returns_dataframe(self, calc):
        """Test that result is a pandas DataFrame"""
        df = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        assert isinstance(df, pd.DataFrame)

    def test_compare_technologies_has_required_columns(self, calc):
        """Test that result has all required columns"""
        df = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2100)
        required_cols = ["technology", "lcoe_usd_per_mwh"]
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"

    def test_compare_technologies_all_lcoe_positive(self, calc):
        """Test that all LCOE values are positive"""
        df = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        assert (df["lcoe_usd_per_mwh"] > 0).all(), "All LCOE values must be positive"

    def test_compare_technologies_with_different_irradiance(self, calc):
        """Test comparison across different irradiance levels"""
        for irr in [1500, 2000, 2500, 3000]:
            df = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=irr)
            assert not df.empty
            assert len(df) >= 2, "Should compare at least 2 technologies"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    @pytest.fixture
    def calc(self):
        return LCOECalculator()

    def test_very_small_capacity(self, calc):
        """Test LCOE calculation with very small capacity (1 kW)"""
        lcoe = calc.calculate_lcoe(
            capacity_mw=0.001,
            capex_usd=1_000,
            opex_annual_usd=50,
            annual_irradiance=2000,
            discount_rate=10.0,
            project_lifetime=25
        )
        assert lcoe > 0

    def test_very_large_capacity(self, calc):
        """Test LCOE calculation with large capacity (100 MW)"""
        lcoe = calc.calculate_lcoe(
            capacity_mw=100.0,
            capex_usd=440_000_000,
            opex_annual_usd=5_000_000,
            annual_irradiance=2000,
            discount_rate=10.0,
            project_lifetime=25
        )
        assert lcoe > 0
        assert lcoe < 200, "Large-scale solar should have lower LCOE"

    def test_zero_discount_rate(self, calc):
        """Test LCOE with zero discount rate (should work)"""
        lcoe = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=2000,
            discount_rate=0.0,
            project_lifetime=25
        )
        assert lcoe > 0

    def test_short_project_lifetime(self, calc):
        """Test LCOE with short project lifetime (5 years)"""
        lcoe_short = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=2000,
            discount_rate=10.0,
            project_lifetime=5
        )
        lcoe_long = calc.calculate_lcoe(
            capacity_mw=0.5,
            capex_usd=440_000,
            opex_annual_usd=5_000,
            annual_irradiance=2000,
            discount_rate=10.0,
            project_lifetime=25
        )
        assert lcoe_short > lcoe_long, "Shorter lifetime should increase LCOE"


class TestIntegration:
    """Integration tests combining multiple features"""

    def test_full_comparison_workflow(self):
        """Test complete workflow: init → compare → verify"""
        calc = LCOECalculator(location="Huíla_Angola")
        
        # Run comparison
        df = calc.compare_technologies(capacity_mw=0.3, annual_irradiance=2100)
        
        # Verify structure
        assert not df.empty
        assert "lcoe_usd_per_mwh" in df.columns
        assert len(df) >= 2
        
        # Find cheapest option
        cheapest_idx = df["lcoe_usd_per_mwh"].idxmin()
        cheapest_tech = df.loc[cheapest_idx, "technology"]
        cheapest_lcoe = df.loc[cheapest_idx, "lcoe_usd_per_mwh"]
        
        assert cheapest_tech in df["technology"].values
        assert cheapest_lcoe > 0
        assert cheapest_lcoe < 300

    def test_comparison_consistency(self):
        """Test that repeated calls give consistent results"""
        calc = LCOECalculator()
        df1 = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        df2 = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        
        # Results should be identical (deterministic)
        pd.testing.assert_frame_equal(df1, df2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
