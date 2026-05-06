"""
Functional tests for GEESP-Angola API and LCOE Calculator.
These tests actually exercise real endpoints and analysis engines.
"""

import pytest
from _path_setup import ensure_backend_paths
ensure_backend_paths()

from fastapi.testclient import TestClient

try:
    from api.api import app
    client = TestClient(app)
    API_AVAILABLE = True
except Exception:
    API_AVAILABLE = False
    client = None

try:
    from scripts.lcoe_calculator import LCOECalculator
    LCOE_AVAILABLE = True
except Exception:
    LCOE_AVAILABLE = False


# ============================================================================
# API Endpoint Tests
# ============================================================================

@pytest.mark.skipif(not API_AVAILABLE, reason="API not importable")
class TestAPIEndpoints:
    """Test real API endpoints."""

    def test_health(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "uptime_seconds" in data

    def test_root(self):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "GEESP-Angola API"

    def test_create_scenario(self):
        resp = client.post("/scenarios", json={
            "name": "Test Scenario",
            "description": "Unit test scenario",
            "location": "Huíla, Angola",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Test Scenario"
        assert data["id"].startswith("scenario-")
        return data["id"]

    def test_get_scenario(self):
        # Create first
        create_resp = client.post("/scenarios", json={
            "name": "Get Test",
            "description": "test",
            "location": "Angola",
        })
        sid = create_resp.json()["id"]
        # Retrieve
        resp = client.get(f"/scenarios/{sid}")
        assert resp.status_code == 200
        assert resp.json()["id"] == sid

    def test_get_scenario_not_found(self):
        resp = client.get("/scenarios/nonexistent-id")
        assert resp.status_code == 404

    def test_list_scenarios(self):
        resp = client.get("/scenarios")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_update_scenario(self):
        create_resp = client.post("/scenarios", json={
            "name": "Before Update",
            "description": "original",
            "location": "Angola",
        })
        sid = create_resp.json()["id"]
        resp = client.put(f"/scenarios/{sid}", json={
            "name": "After Update",
        })
        assert resp.status_code == 200
        assert resp.json()["name"] == "After Update"

    def test_delete_scenario(self):
        create_resp = client.post("/scenarios", json={
            "name": "To Delete",
            "description": "will be deleted",
            "location": "Angola",
        })
        sid = create_resp.json()["id"]
        resp = client.delete(f"/scenarios/{sid}")
        assert resp.status_code == 204
        # Verify gone
        resp2 = client.get(f"/scenarios/{sid}")
        assert resp2.status_code == 404

    def test_analyze_lcoe(self):
        # Create scenario first
        create_resp = client.post("/scenarios", json={
            "name": "LCOE Test",
            "description": "test lcoe",
            "location": "Cacula",
        })
        sid = create_resp.json()["id"]
        resp = client.post("/analyze", json={
            "scenario_id": sid,
            "analysis_type": "lcoe",
            "parameters": {
                "capacity_mw": 1.0,
                "annual_irradiance": 2000.0,
            },
        })
        assert resp.status_code == 202
        data = resp.json()
        assert data["status"] == "completed"
        assert data["analysis_type"] == "lcoe"
        assert "results" in data

    def test_analyze_scenario_not_found(self):
        resp = client.post("/analyze", json={
            "scenario_id": "does-not-exist",
            "analysis_type": "lcoe",
        })
        assert resp.status_code == 404

    def test_get_results(self):
        # Create scenario + run analysis
        create_resp = client.post("/scenarios", json={
            "name": "Results Test",
            "description": "test",
            "location": "Angola",
        })
        sid = create_resp.json()["id"]
        analyze_resp = client.post("/analyze", json={
            "scenario_id": sid,
            "analysis_type": "lcoe",
        })
        aid = analyze_resp.json()["id"]
        resp = client.get(f"/results/{aid}")
        assert resp.status_code == 200


# ============================================================================
# LCOE Calculator Unit Tests
# ============================================================================

@pytest.mark.skipif(not LCOE_AVAILABLE, reason="LCOE Calculator not importable")
class TestLCOECalculatorUnit:
    """Test LCOE calculator engine directly."""

    def test_compare_technologies_basic(self):
        calc = LCOECalculator(location="Test")
        df = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2000)
        assert not df.empty
        assert "lcoe_usd_per_kwh" in df.columns
        assert "lcoe_usd_per_mwh" in df.columns
        assert all(df["lcoe_usd_per_kwh"] > 0)

    def test_compare_technologies_high_irradiance(self):
        calc = LCOECalculator(location="Angola")
        df = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2500)
        # Higher irradiance should produce lower LCOE
        df_low = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=1500)
        # On average, high irradiance = lower cost
        assert df["lcoe_usd_per_kwh"].mean() < df_low["lcoe_usd_per_kwh"].mean()

    def test_compare_technologies_different_capacities(self):
        calc = LCOECalculator(location="Test")
        df1 = calc.compare_technologies(capacity_mw=0.5, annual_irradiance=2000)
        df10 = calc.compare_technologies(capacity_mw=10.0, annual_irradiance=2000)
        assert not df1.empty
        assert not df10.empty

    def test_irr_returns_none_on_failure(self):
        calc = LCOECalculator(location="Test")
        # All-zero cash flows won't converge
        result = calc._calculate_irr([0.0, 0.0, 0.0])
        assert result is None

    def test_financial_analysis(self):
        calc = LCOECalculator(location="Test")
        result = calc.financial_analysis(
            initial_investment=5_000_000,
            annual_revenue=800_000,
            annual_opex=100_000,
            discount_rate=8,
            lifetime=25,
        )
        assert "npv_usd" in result
        assert "irr_percent" in result
        assert "payback_years" in result
