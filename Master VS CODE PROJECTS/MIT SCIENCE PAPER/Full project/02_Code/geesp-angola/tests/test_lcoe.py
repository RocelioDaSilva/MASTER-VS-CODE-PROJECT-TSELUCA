from scripts.lcoe_calculator import LCOECalculator


def test_compare_technologies_runs():
    calc = LCOECalculator(location="Test")
    df = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
    assert not df.empty
    assert "lcoe_usd_per_mwh" in df.columns
