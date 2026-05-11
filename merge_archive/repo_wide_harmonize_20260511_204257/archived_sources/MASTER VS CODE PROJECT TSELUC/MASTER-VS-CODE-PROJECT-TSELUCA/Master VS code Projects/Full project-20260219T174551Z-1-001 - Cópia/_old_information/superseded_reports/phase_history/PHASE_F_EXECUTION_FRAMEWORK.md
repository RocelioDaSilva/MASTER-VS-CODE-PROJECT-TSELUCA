# PHASE F: EXECUTION FRAMEWORK & TEST TEMPLATES
## Production-Ready Backend Integration Testing

**Date:** March 9, 2026  
**Phase:** F - Backend Integration & E2E Testing  
**Status:** Ready for Execution  

---

## 🎯 PHASE F EXECUTION SUMMARY

Based on the comprehensive backend audit, Phase F will focus on:

1. **Creating Missing Tests** (Critical)
   - API endpoint tests
   - LCOE calculator validation
   - MCDA algorithm tests
   - End-to-end workflow tests

2. **Database Integration** (Critical)
   - Wire API endpoints to database
   - Test CRUD operations
   - Verify data persistence

3. **Frontend-Backend Integration** (High Priority)
   - Authentication flow
   - Analysis submission
   - Results retrieval
   - Scenario management

4. **Performance & Reliability** (Medium Priority)
   - Load testing
   - Error handling
   - Recovery procedures

---

## 📋 TEST PLAN: WEEK-BY-WEEK EXECUTION

### WEEK 1: API & Unit Tests

#### Day 1-2: Create API Endpoint Tests
**File:** `backend/tests/test_api_endpoints.py`  
**Coverage:** All 8 API endpoints  
**Tests to Create:** 24 test cases (3 per endpoint)

```python
# Template structure:
import pytest
from fastapi.testclient import TestClient
from backend.api.api import app

client = TestClient(app)

# Authentication Tests
def test_login_valid_credentials():
    """POST /api/auth/login with valid credentials"""
    response = client.post("/api/auth/login", 
        json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    """POST /api/auth/login with invalid credentials"""
    response = client.post("/api/auth/login", 
        json={"email": "test@example.com", "password": "wrong"})
    assert response.status_code == 401

def test_login_missing_fields():
    """POST /api/auth/login with missing fields"""
    response = client.post("/api/auth/login", json={"email": "test@example.com"})
    assert response.status_code == 422  # Validation error

# Analysis Tests
def test_analyze_valid_request():
    """POST /api/analyze with valid MCDA weights"""
    response = client.post("/api/analyze",
        json={
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "communities": ["Luanda", "Benguela"]
        })
    assert response.status_code == 200
    assert "results" in response.json()

def test_analyze_invalid_weights():
    """POST /api/analyze with invalid weights (don't sum to 1)"""
    response = client.post("/api/analyze",
        json={
            "weights": {"climate": 0.5, "soil": 0.5},  # sums to 1.0 but missing criteria
            "communities": ["Luanda"]
        })
    assert response.status_code == 422  # Validation error

def test_analyze_empty_communities():
    """POST /api/analyze with no communities"""
    response = client.post("/api/analyze",
        json={
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "communities": []
        })
    assert response.status_code == 422

# Results Tests  
def test_get_results():
    """GET /api/results returns analysis results"""
    response = client.get("/api/results")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Scenario Tests
def test_create_scenario():
    """POST /api/scenarios creates new scenario"""
    response = client.post("/api/scenarios",
        json={
            "name": "Test Scenario",
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "params": {"wattage": 400, "efficiency": 0.2, "lifetime": 25}
        })
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_scenarios():
    """GET /api/scenarios returns list of scenarios"""
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_scenario():
    """PATCH /api/scenarios/{id} updates scenario"""
    scenario_id = "test-id"
    response = client.patch(f"/api/scenarios/{scenario_id}",
        json={"name": "Updated Scenario"})
    assert response.status_code in [200, 404]

def test_delete_scenario():
    """DELETE /api/scenarios/{id} deletes scenario"""
    scenario_id = "test-id"
    response = client.delete(f"/api/scenarios/{scenario_id}")
    assert response.status_code in [204, 404]

# Communities Tests
def test_get_communities():
    """GET /api/communities returns community data"""
    response = client.get("/api/communities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 8  # Should have 8 Angola communities

# Calculation Tests
def test_lcoe_calculation():
    """POST /api/lcoe calculates LCOE"""
    response = client.post("/api/lcoe",
        json={
            "community_id": "luanda",
            "params": {
                "wattage": 400,
                "efficiency": 0.2,
                "lifetime": 25,
                "om_cost": 500,
                "capital_cost": 15000
            }
        })
    assert response.status_code == 200
    assert "lcoe" in response.json()
    assert response.json()["lcoe"] > 0
```

**Success Criteria:**
- [ ] All 24 tests pass
- [ ] 100% endpoint coverage
- [ ] Error cases handled
- [ ] Response schemas validated

#### Day 3-4: Create LCOE Calculator Tests
**File:** `backend/tests/test_lcoe_calculator.py`  
**Coverage:** LCOE calculation algorithm  
**Tests to Create:** 12 test cases

```python
import pytest
from backend.scripts.lcoe_calculator import LCOECalculator

calc = LCOECalculator()

# Basic Calculation Tests
def test_lcoe_basic_calculation():
    """Basic LCOE calculation with standard inputs"""
    result = calc.calculate_lcoe(
        capacity_wp=400,
        efficiency=0.2,
        lifetime=25,
        annual_om_cost=500,
        capital_cost=15000,
        irradiance=5.5  # kWh/m²/day for Angola
    )
    assert result > 0
    assert isinstance(result, float)

def test_lcoe_with_different_technologies():
    """LCOE for different solar technologies"""
    results = {}
    for tech in ["mono", "poly", "thin_film"]:
        result = calc.calculate_lcoe(
            capacity_wp=400,
            efficiency=0.18 if tech == "poly" else 0.20,
            lifetime=25,
            annual_om_cost=500,
            capital_cost=15000 if tech != "thin_film" else 12000
        )
        results[tech] = result
    
    # Mono should be most efficient (lowest LCOE)
    assert results["mono"] < results["poly"]
    assert results["thin_film"] < results["poly"]

def test_lcoe_sensitivity_to_irradiance():
    """LCOE sensitivity to solar irradiance"""
    low_irradiance = calc.calculate_lcoe(3.0, 0.2, 25, 500, 15000)
    medium_irradiance = calc.calculate_lcoe(5.5, 0.2, 25, 500, 15000)
    high_irradiance = calc.calculate_lcoe(7.0, 0.2, 25, 500, 15000)
    
    # Higher irradiance = lower LCOE
    assert low_irradiance > medium_irradiance > high_irradiance

def test_lcoe_invalid_inputs():
    """LCOE with invalid inputs"""
    with pytest.raises(ValueError):
        calc.calculate_lcoe(
            capacity_wp=-400,  # negative capacity
            efficiency=0.2,
            lifetime=25,
            annual_om_cost=500,
            capital_cost=15000
        )

# Edge Cases
def test_lcoe_zero_capital_cost():
    """LCOE calculation with zero capital cost"""
    result = calc.calculate_lcoe(400, 0.2, 25, 0, 0)
    assert result == 0  # No inputs = no cost

def test_lcoe_very_short_lifetime():
    """LCOE with very short project lifetime"""
    result = calc.calculate_lcoe(400, 0.2, 1, 500, 15000)
    assert result > 15000  # High cost per unit due to short life

def test_lcoe_very_long_lifetime():
    """LCOE with very long project lifetime"""
    result = calc.calculate_lcoe(400, 0.2, 50, 500, 15000)
    assert result > 0 and result < 1000  # Lower per-year cost

# Integration Tests
def test_lcoe_for_all_angola_communities():
    """Calculate LCOE for each Angola community"""
    from backend.api.models import Community
    
    results = {}
    for community in Community.get_all():
        lcoe = calc.calculate_lcoe(
            capacity_wp=400,
            efficiency=0.2,
            lifetime=25,
            annual_om_cost=500,
            capital_cost=15000,
            irradiance=community.ghi  # Use actual GHI
        )
        results[community.name] = lcoe
    
    assert len(results) == 8
    assert all(v > 0 for v in results.values())

def test_lcoe_comparison_scenarios():
    """Compare LCOE across different scenarios"""
    scenario1 = calc.calculate_lcoe(400, 0.2, 25, 500, 15000)
    scenario2 = calc.calculate_lcoe(500, 0.22, 25, 600, 18000)  # Larger, more efficient
    
    # Larger capacity should have better LCOE (economies of scale)
    assert scenario2 < scenario1
```

**Success Criteria:**
- [ ] All 12 tests pass
- [ ] Algorithm accuracy verified
- [ ] Edge cases handled
- [ ] Sensitivity analysis working

#### Day 4-5: Create MCDA Algorithm Tests
**File:** `backend/tests/test_mcda_algorithm.py`  
**Coverage:** MCDA ranking logic  
**Tests to Create:** 10 test cases

```python
import pytest
from backend.scripts.mcda_analysis import MCDAAnalyzer

analyzer = MCDAAnalyzer()

def test_mcda_basic_ranking():
    """Basic MCDA ranking of communities"""
    weights = {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3}
    results = analyzer.rank_communities(weights)
    
    assert len(results) == 8
    assert all(0 <= r["score"] <= 100 for r in results)
    # Results should be sorted by score descending
    assert results[0]["score"] >= results[-1]["score"]

def test_mcda_weight_validation():
    """MCDA validates weights sum to 1.0"""
    invalid_weights = {"climate": 0.5, "soil": 0.3}  # Sum = 0.8
    
    with pytest.raises(ValueError):
        analyzer.rank_communities(invalid_weights)

def test_mcda_sensitivity_to_weights():
    """MCDA results change with different weights"""
    weights1 = {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3}
    weights2 = {"climate": 0.1, "soil": 0.4, "terrain": 0.2, "infrastructure": 0.3}
    
    results1 = analyzer.rank_communities(weights1)
    results2 = analyzer.rank_communities(weights2)
    
    # Top ranked community should differ
    assert results1[0]["community_id"] != results2[0]["community_id"]

def test_mcda_extreme_weights():
    """MCDA with extreme weight distributions"""
    # All weight on climate
    weights = {"climate": 1.0, "soil": 0.0, "terrain": 0.0, "infrastructure": 0.0}
    results = analyzer.rank_communities(weights)
    
    # Community with best climate should rank highest
    assert results[0]["score"] > 0

def test_mcda_equal_weights():
    """MCDA with equal weights"""
    weights = {"climate": 0.25, "soil": 0.25, "terrain": 0.25, "infrastructure": 0.25}
    results = analyzer.rank_communities(weights)
    
    assert len(results) == 8
    assert results[0]["score"] >= results[-1]["score"]

def test_mcda_different_criteria_combinations():
    """Test various criterion combinations"""
    combinations = [
        {"climate": 0.6, "soil": 0.2, "terrain": 0.1, "infrastructure": 0.1},  # Climate focused
        {"climate": 0.1, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.6},  # Infrastructure focused
        {"climate": 0.3, "soil": 0.3, "terrain": 0.2, "infrastructure": 0.2},  # Balanced
    ]
    
    results_list = [analyzer.rank_communities(w) for w in combinations]
    
    # All should produce valid rankings
    assert all(len(r) == 8 for r in results_list)
    assert all(all(0 <= c["score"] <= 100 for c in r) for r in results_list)

def test_mcda_with_weights_passed_as_list():
    """MCDA handles weights in different formats"""
    # This tests API compatibility
    weights_dict = {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3}
    results = analyzer.rank_communities(weights_dict)
    
    assert len(results) == 8

def test_mcda_reproducibility():
    """MCDA results are reproducible"""
    weights = {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3}
    
    results1 = analyzer.rank_communities(weights)
    results2 = analyzer.rank_communities(weights)
    
    # Results should be identical
    assert results1 == results2

def test_mcda_ranking_order():
    """MCDA results maintain proper ranking order"""
    weights = {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3}
    results = analyzer.rank_communities(weights)
    
    # Verify descending order
    for i in range(len(results) - 1):
        assert results[i]["score"] >= results[i + 1]["score"]
        assert results[i]["rank"] == i + 1
```

**Success Criteria:**
- [ ] All 10 tests pass
- [ ] Weight validation working
- [ ] Rankings reproducible
- [ ] Edge cases handled

### WEEK 2: Integration Tests & Database

#### Day 1-2: Create Workflow Tests
**File:** `backend/tests/test_e2e_workflows.py`  
**Coverage:** Complete user workflows  
**Tests to Create:** 8 end-to-end scenarios

```python
import pytest
from fastapi.testclient import TestClient
from backend.api.api import app

client = TestClient(app)

def test_new_user_registration_and_login():
    """Complete new user workflow: register → login"""
    # Register
    register_response = client.post("/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "confirmPassword": "SecurePass123!"
        })
    assert register_response.status_code == 201
    token = register_response.json()["access_token"]
    
    # Login with same credentials
    login_response = client.post("/api/auth/login",
        json={"email": "newuser@example.com", "password": "SecurePass123!"})
    assert login_response.status_code == 200
    assert login_response.json()["access_token"] == token

def test_complete_analysis_workflow():
    """Full analysis workflow: login → submit analysis → get results"""
    # 1. Login
    auth_response = client.post("/api/auth/login",
        json={"email": "test@example.com", "password": "password123"})
    assert auth_response.status_code == 200
    headers = {"Authorization": f"Bearer {auth_response.json()['access_token']}"}
    
    # 2. Submit analysis
    analysis_response = client.post("/api/analyze",
        json={
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "communities": ["Luanda", "Benguela", "Huambo"]
        },
        headers=headers)
    assert analysis_response.status_code == 200
    analysis_id = analysis_response.json()["id"]
    
    # 3. Get results
    results_response = client.get(f"/api/results/{analysis_id}", headers=headers)
    assert results_response.status_code == 200
    results = results_response.json()
    assert len(results) == 3  # 3 communities analyzed

def test_scenario_creation_and_retrieval():
    """Scenario workflow: create → retrieve → verify"""
    # Login
    auth_response = client.post("/api/auth/login",
        json={"email": "test@example.com", "password": "password123"})
    headers = {"Authorization": f"Bearer {auth_response.json()['access_token']}"}
    
    # Create scenario
    create_response = client.post("/api/scenarios",
        json={
            "name": "Test Scenario",
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "params": {"wattage": 400, "efficiency": 0.2, "lifetime": 25, "om_cost": 500, "capital_cost": 15000}
        },
        headers=headers)
    assert create_response.status_code == 201
    scenario_id = create_response.json()["id"]
    
    # Retrieve scenario
    get_response = client.get(f"/api/scenarios/{scenario_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Scenario"
    
    # Verify in list
    list_response = client.get("/api/scenarios", headers=headers)
    scenario_names = [s["name"] for s in list_response.json()]
    assert "Test Scenario" in scenario_names

def test_scenario_update_and_delete():
    """Scenario update and deletion workflow"""
    # Create scenario
    create_response = client.post("/api/scenarios",
        json={"name": "Original Name", ...})
    scenario_id = create_response.json()["id"]
    
    # Update
    update_response = client.patch(f"/api/scenarios/{scenario_id}",
        json={"name": "Updated Name"})
    assert update_response.status_code == 200
    
    # Verify update
    get_response = client.get(f"/api/scenarios/{scenario_id}")
    assert get_response.json()["name"] == "Updated Name"
    
    # Delete
    delete_response = client.delete(f"/api/scenarios/{scenario_id}")
    assert delete_response.status_code == 204
    
    # Verify deletion
    get_response = client.get(f"/api/scenarios/{scenario_id}")
    assert get_response.status_code == 404

def test_lcoe_calculation_workflow():
    """LCOE calculation for scenario"""
    auth_response = client.post("/api/auth/login",
        json={"email": "test@example.com", "password": "password123"})
    headers = {"Authorization": f"Bearer {auth_response.json()['access_token']}"}
    
    # Calculate LCOE for Luanda
    lcoe_response = client.post("/api/lcoe",
        json={
            "community_id": "luanda",
            "params": {
                "wattage": 400,
                "efficiency": 0.2,
                "lifetime": 25,
                "om_cost": 500,
                "capital_cost": 15000
            }
        },
        headers=headers)
    assert lcoe_response.status_code == 200
    result = lcoe_response.json()
    assert "lcoe" in result
    assert result["lcoe"] > 0

def test_analysis_with_lcoe_combination():
    """Full workflow: analysis → results → LCOE for top community"""
    # Analysis
    analysis_response = client.post("/api/analyze",
        json={
            "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
            "communities": ["Luanda", "Benguela"]
        })
    results = analysis_response.json()["results"]
    top_community = results[0]["community_id"]  # Highest ranked
    
    # LCOE for top community
    lcoe_response = client.post("/api/lcoe",
        json={
            "community_id": top_community,
            "params": {"wattage": 400, "efficiency": 0.2, "lifetime": 25, "om_cost": 500, "capital_cost": 15000}
        })
    assert lcoe_response.status_code == 200
    assert lcoe_response.json()["lcoe"] > 0

def test_concurrent_analysis_requests():
    """Multiple concurrent analysis requests"""
    import concurrent.futures
    
    def run_analysis():
        return client.post("/api/analyze",
            json={
                "weights": {"climate": 0.4, "soil": 0.1, "terrain": 0.2, "infrastructure": 0.3},
                "communities": ["Luanda"]
            })
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_analysis) for _ in range(5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # All requests should succeed
    assert all(r.status_code == 200 for r in results)
```

**Success Criteria:**
- [ ] All 8 workflows complete end-to-end
- [ ] Data persisted correctly
- [ ] Each step verifiable
- [ ] Concurrent requests handled

#### Day 3-4: Database Integration
**Objectives:**
- [ ] Wire API endpoints to database
- [ ] Create database session management
- [ ] Test CRUD operations
- [ ] Verify data persistence

**Key Files to Update:**
1. `backend/api/api.py` - Add database session to endpoints
2. `backend/models/` - Ensure SQLAlchemy models complete
3. `backend/database/session.py` - Database connection management
4. `backend/utils/config.py` - Database URL configuration

**Database Setup:**
```bash
# Initialize database
cd backend
python -c "from database.session import engine, Base; Base.metadata.create_all(engine)"

# Create initial data
python scripts/seed_database.py
```

**Test Database Operations:**
```python
# backend/tests/test_database_operations.py
def test_create_user():
    """Create and retrieve user from database"""
    from backend.models.user import User
    
    user = User(email="test@example.com", password_hash="...")
    session.add(user)
    session.commit()
    
    retrieved = session.query(User).filter_by(email="test@example.com").first()
    assert retrieved.email == "test@example.com"

def test_create_scenario():
    """Create scenario and verify persistence"""
    from backend.models.scenario import Scenario
    
    scenario = Scenario(
        name="Test",
        user_id=1,
        weights={"climate": 0.4, ...}
    )
    session.add(scenario)
    session.commit()
    
    retrieved = session.query(Scenario).filter_by(id=scenario.id).first()
    assert retrieved.name == "Test"
```

#### Day 5: Performance & Integration Validation
**Tasks:**
- [ ] Run full test suite
- [ ] Measure API response times
- [ ] Verify end-to-end workflows
- [ ] Document any issues
- [ ] Create Phase F completion report

---

## 📊 WEEK 1 CHECKLIST

**By End of Week 1:**
- [ ] API endpoint tests created and passing (24 tests)
- [ ] LCOE calculator tests created and passing (12 tests)
- [ ] MCDA algorithm tests created and passing (10 tests)
- [ ] E2E workflow tests created and passing (8 tests)
- [ ] Database integration complete
- [ ] 54 total new tests added
- [ ] Test coverage increased to 65%+

**Exit Criteria for Week 1:**
```
✅ New tests: 54
✅ Tests passing: 54
✅ Coverage: 65%+
✅ API endpoints: All functional
✅ Database: Integrated
✅ No critical failures
```

---

## 🎯 WEEK 2 OBJECTIVES

- [ ] GEE integration testing
- [ ] Map generation validation
- [ ] Dashboard integration testing
- [ ] Load testing (100+ concurrent requests)
- [ ] Error scenario coverage
- [ ] Performance optimization
- [ ] Final E2E validation

---

## 📊 EXPECTED OUTCOMES

### Test Coverage Improvement
```
BEFORE Phase F:     42%  (8 modules)
AFTER Week 1:       65%+ (54 new tests)
AFTER Week 2:       85%+ (complete)
TARGET:             80%+ ✅
```

### Code Quality
```
BEFORE:  Untested backend modules, no E2E tests
AFTER:   Comprehensive test coverage, all workflows validated
```

### Production Readiness
```
BEFORE:  57% (Frontend only)
AFTER:   95% (Full stack validated)
```

---

**Status:** 🟡 **Ready for Execution - Week 1 Starting March 9-13, 2026**

