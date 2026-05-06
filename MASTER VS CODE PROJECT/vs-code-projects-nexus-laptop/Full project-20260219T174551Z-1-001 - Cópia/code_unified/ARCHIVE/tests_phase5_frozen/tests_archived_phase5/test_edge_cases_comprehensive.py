"""Edge-case tests for validators and MCDA-related utilities."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

import numpy as np
import pytest

from scripts import validators


def test_validate_weights_accepts_good_weights() -> None:
    good = {"solar": 0.25, "population": 0.25, "distance": 0.2, "slope": 0.15, "ndvi": 0.15}
    assert validators.validate_weights(good)


def test_validate_weights_rejects_bad_sum() -> None:
    bad = {"a": 0.5, "b": 0.5, "c": 0.5}
    with pytest.raises(ValueError):
        validators.validate_weights(bad)


def test_validate_raster_shape_raises_for_wrong_shape() -> None:
    arr = np.zeros((10, 10))
    with pytest.raises(ValueError):
        validators.validate_raster_shape(arr, expected_shape=(5, 5))


def test_validate_probability_array_rejects_out_of_range() -> None:
    arr = np.array([[0.0, 1.0], [1.2, -0.1]])
    with pytest.raises(ValueError):
        validators.validate_is_probability_array(arr)
import numpy as np
import math
import pytest

from scripts import mcda_analysis, lcoe_calculator, validators


def test_validators_empty_and_all_nan():
    # empty array should raise
    with pytest.raises(ValueError):
        validators.validate_solar_irradiance(np.array([]))

    # all-NaN should raise
    arr = np.full((10, 10), np.nan)
    with pytest.raises(ValueError):
        validators.validate_population(arr)


def test_validate_weight_vector_invalid_shape_and_values():
    with pytest.raises(ValueError):
        validators.validate_weight_vector([0.5, 0.5])  # not numpy array

    import numpy as _np
    with pytest.raises(ValueError):
        validators.validate_weight_vector(_np.array([[0.5, 0.5]]))  # not 1D

    with pytest.raises(ValueError):
        validators.validate_weight_vector(_np.array([0.6, 0.6]))  # sums >1


def test_mcda_weighted_overlay_no_rasters_raises():
    analyzer = mcda_analysis.MCDAnalyzer()
    # no normalized rasters -> should raise
    with pytest.raises(ValueError):
        analyzer.weighted_overlay()

    # classify without aptitude_map
    with pytest.raises(ValueError):
        analyzer.classify_aptitude()


def test_lcoe_zero_generation_returns_inf():
    # Build SolarParameters with zero efficiency to force zero generation
    params = lcoe_calculator.SolarParameters(
        capacity_mw=1.0,
        capex_dict={"pv_module": 200, "inverter": 80},
        opex_fixed=100.0,
        opex_variable=1.0,
        annual_irradiance=6.0,
        system_efficiency=0.0,  # zero -> zero generation
        degradation_rate=0.0,
        discount_rate=8.0,
        project_lifetime=25,
        warranty_years=10,
        location="Test",
    )

    calc = lcoe_calculator.LCOECalculator(location="Test")
    res = calc.calculate_lcoe(params)
    assert "lcoe_usd_per_mwh" in res
    assert math.isinf(res["lcoe_usd_per_mwh"]) or res["lcoe_usd_per_mwh"] == float("inf")
