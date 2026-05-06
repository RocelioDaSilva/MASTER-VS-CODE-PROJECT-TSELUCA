"""
Test Suite: LCOE Calculator
=============================
Tests the LCOECalculator from scripts/lcoe_calculator.py with the real API.
"""

import pytest

try:
    from scripts.lcoe_calculator import LCOECalculator, SolarParameters
    LCOE_AVAILABLE = True
except ImportError:
    LCOE_AVAILABLE = False

pytestmark = pytest.mark.skipif(not LCOE_AVAILABLE, reason="LCOECalculator not importable")


class TestSolarParameters:
    """Verify SolarParameters dataclass."""

    def test_defaults(self):
        p = SolarParameters()
        assert p.capacity_mw == 1.0
        assert p.project_lifetime == 25
        assert p.system_efficiency == 0.18

    def test_from_dict(self):
        p = SolarParameters.from_dict({"capacity_mw": 5.0, "unknown_key": 99})
        assert p.capacity_mw == 5.0
        # Unknown key should be silently ignored
        assert not hasattr(p, "unknown_key")


class TestLCOECalculator:
    """Test the core LCOE calculation engine."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = LCOECalculator(location="Angola")

    def test_basic_calculation(self):
        result = self.calc.calculate_lcoe(
            capacity_mw=1.0,
            annual_irradiance=2000.0,
            system_efficiency=0.18,
            discount_rate=8.0,
            project_lifetime=25,
        )
        assert result is not None
        assert isinstance(result, dict)
        assert "lcoe_usd_per_mwh" in result or "lcoe_usd_per_kwh" in result

    def test_higher_irradiance_lowers_lcoe(self):
        low = self.calc.calculate_lcoe(annual_irradiance=1000.0)
        high = self.calc.calculate_lcoe(annual_irradiance=3000.0)
        # More sun -> cheaper energy
        lcoe_key = "lcoe_usd_per_mwh" if "lcoe_usd_per_mwh" in low else "lcoe_usd_per_kwh"
        assert high[lcoe_key] < low[lcoe_key]

    def test_zero_capacity_raises(self):
        with pytest.raises((ValueError, Exception)):
            self.calc.calculate_lcoe(capacity_mw=0)

    def test_negative_irradiance_raises(self):
        with pytest.raises((ValueError, Exception)):
            self.calc.calculate_lcoe(annual_irradiance=-100)

    def test_params_object(self):
        p = SolarParameters(capacity_mw=2.0, annual_irradiance=2500.0)
        result = self.calc.calculate_lcoe(params=p)
        assert result is not None


class TestCompareTechnologies:
    """Test compare_technologies (multi-tech LCOE comparison)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = LCOECalculator(location="Angola")

    def test_returns_dataframe(self):
        import pandas as pd
        df = self.calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2000.0)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_has_lcoe_column(self):
        df = self.calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2000.0)
        assert "lcoe_usd_per_kwh" in df.columns or "lcoe_usd_per_mwh" in df.columns


class TestFinancialAnalysis:
    """Test financial_analysis method."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = LCOECalculator(location="Angola")

    def test_returns_dict(self):
        result = self.calc.financial_analysis(
            capacity_mw=1.0,
            annual_irradiance=2000.0,
        )
        assert isinstance(result, dict)

