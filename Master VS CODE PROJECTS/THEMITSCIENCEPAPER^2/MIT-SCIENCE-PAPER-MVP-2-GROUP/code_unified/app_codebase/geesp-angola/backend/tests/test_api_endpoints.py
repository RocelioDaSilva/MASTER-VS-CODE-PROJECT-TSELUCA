"""
Test Suite: API Endpoint Validation
====================================
Tests the REST API endpoints for proper request handling, validation, and responses.

Covers:
- Scenario CRUD endpoints
- Direct analysis endpoint (/api/analyze)
- Results and Maps retrieval
- Health check
"""

import pytest
from fastapi.testclient import TestClient

try:
    from api.api import app
    client = TestClient(app)
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False
    client = None

pytestmark = pytest.mark.skipif(not API_AVAILABLE, reason="API module not importable")


# ============================================================================
# HEALTH CHECK
# ============================================================================


class TestHealthEndpoint:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime_seconds" in data

    def test_root_returns_api_info(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["name"] == "GEESP-Angola API"


# ============================================================================
# SCENARIO CRUD
# ============================================================================


class TestScenarioCRUD:
    def _create(self, name="Test Scenario"):
        return client.post("/scenarios", json={"name": name, "description": "test"})

    def test_create_scenario(self):
        resp = self._create()
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Test Scenario"
        assert data["status"] == "active"
        assert "id" in data

    def test_create_scenario_missing_name(self):
        resp = client.post("/scenarios", json={"description": "no name"})
        assert resp.status_code == 422

    def test_list_scenarios(self):
        self._create("List-Test")
        resp = client.get("/scenarios")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_scenario(self):
        sid = self._create("Get-Test").json()["id"]
        resp = client.get(f"/scenarios/{sid}")
        assert resp.status_code == 200
        assert resp.json()["id"] == sid

    def test_get_nonexistent(self):
        resp = client.get("/scenarios/does-not-exist")
        assert resp.status_code == 404

    def test_update_scenario(self):
        sid = self._create("Update-Test").json()["id"]
        resp = client.put(f"/scenarios/{sid}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    def test_delete_scenario(self):
        sid = self._create("Delete-Test").json()["id"]
        resp = client.delete(f"/scenarios/{sid}")
        assert resp.status_code == 204
        # Confirm gone
        resp2 = client.get(f"/scenarios/{sid}")
        assert resp2.status_code == 404


# ============================================================================
# DIRECT ANALYSIS (/api/analyze — frontend-compatible)
# ============================================================================


class TestDirectAnalysis:
    PAYLOAD = {
        "communities": [
            {"id": "c1", "name": "Test Community", "province": "Luanda",
             "lat": -8.838, "lng": 13.234, "ghi": 5.6, "soilType": "Sandy",
             "slope": 2.0, "distToGrid": 5.0, "population": 10000},
        ],
        "weights": {"climate": 0.35, "soil": 0.15, "terrain": 0.25, "infrastructure": 0.25},
        "params": {"wattage": 400, "efficiency": 0.21, "lifetime": 25, "omCost": 500, "capitalCost": 25000},
    }

    def test_analyze_returns_results(self):
        resp = client.post("/api/analyze", json=self.PAYLOAD)
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data
        assert len(data["results"]) == 1
        r = data["results"][0]
        assert r["communityId"] == "c1"
        assert 0 <= r["score"] <= 100
        assert r["aptitude"] in ("Unsuitable", "Poor", "Moderate", "Good", "Excellent")
        assert r["lcoe"] > 0

    def test_analyze_empty_communities(self):
        payload = {**self.PAYLOAD, "communities": []}
        resp = client.post("/api/analyze", json=payload)
        assert resp.status_code == 200
        assert resp.json()["results"] == []

    def test_analyze_invalid_weights(self):
        payload = {**self.PAYLOAD, "weights": {"climate": 2.0}}
        resp = client.post("/api/analyze", json=payload)
        # Pydantic should reject climate > 1
        assert resp.status_code == 422


# ============================================================================
# SCENARIO-BASED ANALYSIS (/analyze)
# ============================================================================


class TestScenarioAnalysis:
    def test_analyze_requires_existing_scenario(self):
        resp = client.post("/analyze", json={
            "scenario_id": "nonexistent", "analysis_type": "lcoe",
        })
        assert resp.status_code == 404

    def test_analyze_lcoe(self):
        sid = client.post("/scenarios", json={"name": "LCOE-Test"}).json()["id"]
        resp = client.post("/analyze", json={
            "scenario_id": sid, "analysis_type": "lcoe",
            "parameters": {"capacity_mw": 1.0, "annual_irradiance": 2000.0},
        })
        assert resp.status_code == 202
        data = resp.json()
        assert data["status"] == "completed"
        assert data["analysis_type"] == "lcoe"

    def test_get_results(self):
        sid = client.post("/scenarios", json={"name": "Res-Test"}).json()["id"]
        aid = client.post("/analyze", json={
            "scenario_id": sid, "analysis_type": "mcda",
        }).json()["id"]
        resp = client.get(f"/results/{aid}")
        assert resp.status_code == 200

    def test_get_maps(self):
        sid = client.post("/scenarios", json={"name": "Map-Test"}).json()["id"]
        aid = client.post("/analyze", json={
            "scenario_id": sid, "analysis_type": "lcoe",
        }).json()["id"]
        resp = client.get(f"/maps/{aid}")
        assert resp.status_code == 200
        assert "map_url" in resp.json()


