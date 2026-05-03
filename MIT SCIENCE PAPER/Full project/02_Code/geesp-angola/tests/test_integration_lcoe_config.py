import numpy as np
from scripts.lcoe_calculator import LCOECalculator, SolarParameters
from scripts.config_loader import get_lcoe_parameters


def test_lcoe_with_config_parameters():
    params_dict = get_lcoe_parameters()

    # Build SolarParameters with reasonable defaults
    params = SolarParameters(
        capacity_mw=float(params_dict.get("capacity_mw", 1.0)),
        capex_dict={
            "pv_module": 200,
            "inverter": 80,
            "bop": 100,
            "battery": 450,
            "installation": 150,
        },
        opex_fixed=14000.0,
        opex_variable=3.0,
        annual_irradiance=6.0,
        system_efficiency=0.18,
        degradation_rate=0.005,
        discount_rate=float(params_dict.get("discount_rate", 8.0)),
        project_lifetime=int(params_dict.get("project_lifetime", 25)),
        warranty_years=10,
        location="Test"
    )

    calc = LCOECalculator(location="Test")
    results = calc.calculate_lcoe(params)

    assert "lcoe_usd_per_mwh" in results
    assert results["lcoe_usd_per_mwh"] > 0
