"""
Integration test: full MCDA → LCOE → result pipeline (M2).

Runs without real GEE data by generating synthetic rasters.
Marked with pytest.mark.integration so it can be skipped in fast CI runs.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

# Ensure backend root is on sys.path
_BACKEND = Path(__file__).parent.parent.parent
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

pytestmark = pytest.mark.integration

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

RNG = np.random.default_rng(42)
SHAPE = (64, 64)


def _synthetic_raster(low: float = 0.0, high: float = 1.0) -> np.ndarray:
    """Return a random float32 raster in [low, high]."""
    return (RNG.random(SHAPE, dtype=np.float32) * (high - low) + low)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def synthetic_maps():
    """Provide a dict of synthetic raster arrays matching MCDA input spec."""
    return {
        "solar":      _synthetic_raster(4.5, 6.5),   # kWh/m²/day
        "population": _synthetic_raster(0.0, 1.0),
        "distance":   _synthetic_raster(0.0, 50.0),  # km
        "slope":      _synthetic_raster(0.0, 30.0),  # degrees
        "ndvi":       _synthetic_raster(0.0, 1.0),
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestMCDALCOEPipeline:
    """End-to-end: synthetic rasters → aptitude map → LCOE calculation."""

    def test_compute_aptitude_shape(self, synthetic_maps):
        """Aptitude output must have the same shape as the input rasters."""
        from geospatial.operations import compute_aptitude

        apt = compute_aptitude(**synthetic_maps)
        assert apt.shape == SHAPE, f"Expected {SHAPE}, got {apt.shape}"

    def test_compute_aptitude_range(self, synthetic_maps):
        """All aptitude values must lie in [0, 1] after normalisation."""
        from geospatial.operations import compute_aptitude
        from utils.constants import MCDAConstants

        apt = compute_aptitude(**synthetic_maps)
        assert float(np.nanmin(apt)) >= MCDAConstants.APTITUDE_LOW - 1e-6
        assert float(np.nanmax(apt)) <= MCDAConstants.APTITUDE_HIGH + 1e-6

    def test_compute_aptitude_deterministic(self, synthetic_maps):
        """compute_aptitude must be deterministic for identical inputs."""
        from geospatial.operations import compute_aptitude
        from geospatial.raster import clear_normalization_cache

        clear_normalization_cache()
        apt1 = compute_aptitude(**synthetic_maps)
        clear_normalization_cache()
        apt2 = compute_aptitude(**synthetic_maps)
        np.testing.assert_array_equal(apt1, apt2)

    def test_lcoe_returns_dict(self):
        """calculate_lcoe must always return a dict (H11 regression guard)."""
        from scripts.lcoe_calculator import LCOECalculator, SolarParameters

        calc = LCOECalculator()

        # SolarParameters path
        params = SolarParameters(
            capacity_mw=1.0,
            annual_irradiance=1800.0,
            system_efficiency=0.18,
        )
        result_obj = calc.calculate_lcoe(params)
        assert isinstance(result_obj, dict), "Expected dict from SolarParameters path"
        assert "lcoe_usd_per_mwh" in result_obj

        # kwargs path (was returning float — H11)
        result_kw = calc.calculate_lcoe(
            capacity_mw=1.0,
            annual_irradiance=1800.0,
            system_efficiency=0.18,
        )
        assert isinstance(result_kw, dict), "Expected dict from kwargs path (H11 regression)"
        assert "lcoe_usd_per_mwh" in result_kw

    def test_lcoe_value_positive(self):
        """LCOE must be a positive finite number for valid inputs."""
        from scripts.lcoe_calculator import LCOECalculator, SolarParameters

        calc = LCOECalculator()
        params = SolarParameters(capacity_mw=5.0, annual_irradiance=2000.0, system_efficiency=0.20)
        result = calc.calculate_lcoe(params)
        lcoe = result["lcoe_usd_per_mwh"]
        assert np.isfinite(lcoe), "LCOE must be finite"
        assert lcoe > 0, "LCOE must be positive"

    def test_pipeline_aptitude_to_lcoe(self, synthetic_maps):
        """High-aptitude pixels should correlate with better (lower) LCOE proxies."""
        from geospatial.operations import compute_aptitude
        from geospatial.raster import clear_normalization_cache
        from scripts.lcoe_calculator import LCOECalculator, SolarParameters

        clear_normalization_cache()
        apt = compute_aptitude(**synthetic_maps)

        # Pick representative high/low aptitude pixels
        flat_apt = apt.ravel()
        high_irr_idx = int(np.argmax(synthetic_maps["solar"].ravel()))
        low_irr_idx  = int(np.argmin(synthetic_maps["solar"].ravel()))

        calc = LCOECalculator()

        def lcoe_for_irr(irr_kwh_m2_day: float) -> float:
            p = SolarParameters(
                capacity_mw=1.0,
                annual_irradiance=float(irr_kwh_m2_day * 365),
                system_efficiency=0.18,
            )
            return calc.calculate_lcoe(p)["lcoe_usd_per_mwh"]

        high_irr = float(synthetic_maps["solar"].ravel()[high_irr_idx])
        low_irr  = float(synthetic_maps["solar"].ravel()[low_irr_idx])

        lcoe_high = lcoe_for_irr(high_irr)
        lcoe_low  = lcoe_for_irr(low_irr)

        # Higher irradiance → more generation → lower LCOE
        assert lcoe_high < lcoe_low, (
            f"Higher irradiance ({high_irr:.2f}) should yield lower LCOE "
            f"({lcoe_high:.2f} < {lcoe_low:.2f})"
        )
