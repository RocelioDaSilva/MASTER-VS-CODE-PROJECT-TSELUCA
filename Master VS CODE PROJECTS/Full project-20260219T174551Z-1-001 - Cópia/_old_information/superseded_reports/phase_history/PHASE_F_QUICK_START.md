# PHASE F: QUICK START GUIDE
## Backend Integration & E2E Testing (Week-by-Week)

**Status:** Ready for Immediate Execution  
**Timeline:** 5-7 days (compressed, with focused testing)  
**Goal:** Achieve 80%+ test coverage and production readiness  
**Starting:** March 9-13, 2026

---

## 🚀 GETTING STARTED: DAY 1

### Prerequisites Check
```bash
# 1. Navigate to backend directory
cd c:\Users\rocel\...\geesp-angola\backend

# 2. Activate Python environment (if using venv)
# Windows:
venv\Scripts\activate

# 3. Install/verify pytest and dependencies
pip install pytest pytest-cov pytest-asyncio

# 4. Check Python version
python --version  # Should be 3.11+
```

### View Current Test Status
```bash
# Run existing tests to establish baseline
pytest tests/ -v --cov=. --cov-report=term-missing

# Expected result: ~42-50% coverage, some tests may be marked skip
```

### Phase F File Structure
```
geesp-angola/
├── backend/
│   ├── tests/
│   │   ├── test_api_endpoints.py          ← DAY 1-2 (Create & Implement)
│   │   ├── test_lcoe_calculator.py        ← DAY 3-4 (Create & Implement)
│   │   ├── test_mcda_algorithm.py         ← DAY 4-5 (Create & Implement)
│   │   ├── test_e2e_workflows.py          ← DAY 5-6 (Create & Implement)
│   │   ├── test_database_operations.py    ← DAY 7 (Create & Implement)
│   │   └── test_gee_integration.py        ← WEEK 2
│   ├── api/
│   │   └── api.py                         ← May need database wiring
│   ├── models/
│   │   └── (*.py)                         ← Database ORM models
│   ├── scripts/
│   │   ├── lcoe_calculator.py            ← Algorithm to test
│   │   ├── mcda_analysis.py              ← Algorithm to test
│   │   └── gee_integration.py            ← Integration to test
│   └── database/
│       ├── session.py                     ← Database setup
│       └── init_db.py                     ← Database initialization
```

---

## 📋 DAY-BY-DAY EXECUTION PLAN

### DAY 1-2: API Endpoint Tests (24 tests)

**File:** `backend/tests/test_api_endpoints.py`  
**Status:** Template created ✅

**Step 1: Review Template**
```bash
# Open and read the template
code backend/tests/test_api_endpoints.py

# Template includes:
# - 24 test functions (all marked with pytest.skip)
# - 8 classes for different endpoint groups
# - Documentation for each test
# - Pytest fixtures for auth and sample data
```

**Step 2: Implement Tests (Choose Approach)**

*Option A: Sequential Implementation (Recommended for first 3 tests)*
```bash
# 1. Start with simplest endpoint: Health Check
pytest.skip() → Remove this line
# Implement: GET /api/health
# Run: pytest tests/test_api_endpoints.py::TestHealthEndpoint::test_health_check -v
# Verify: ✅ Pass

# 2. Next: Get Communities (no auth needed)
# Implement test_get_communities
# Run: pytest tests/test_api_endpoints.py::TestCommunitiesEndpoint::test_get_communities -v
# Verify: ✅ Pass

# 3. Next: Login endpoint (required for other tests)
# Implement test_login_valid_credentials
# First create test user in database
# Run: All auth-dependent tests
# Verify: ✅ Pass
```

*Option B: Complete Implementation (If confident)*
```bash
# Edit test_api_endpoints.py
# 1. Replace all pytest.skip() with actual implementations
# 2. Configure test credentials in fixtures
# 3. Run full test suite
# 4. Fix failures one by one
```

**Step 3: Setup Test Configuration**

Create `backend/tests/conftest.py`:
```python
import pytest
from fastapi.testclient import TestClient
from backend.api.api import app
from backend.database.session import SessionLocal
from backend.models.user import User

@pytest.fixture(scope="session")
def test_db():
    """Setup test database"""
    # Create test database tables
    # Seed test data
    yield
    # Cleanup

@pytest.fixture
def client(test_db):
    """Test client for API"""
    return TestClient(app)

@pytest.fixture
def test_user(test_db):
    """Create test user"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_123"
    )
    # Save to test database
    return user

@pytest.fixture
def auth_token(client, test_user):
    """Get auth token for test user"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Authorization headers"""
    return {"Authorization": f"Bearer {auth_token}"}
```

**Step 4: Implementation Checklist**

For each endpoint group:
- [ ] Authentication endpoints (3 tests)
- [ ] Analysis endpoints (3 tests)
- [ ] Scenario endpoints (4 tests)
- [ ] Communities endpoint (3 tests)
- [ ] LCOE endpoint (3 tests)
- [ ] Health endpoint (2 tests)
- [ ] Error handling (3 tests)

**Expected by End of Day 2:**
```
✅ 24/24 API tests created
✅ 20/24 tests passing (some may need DB integration)
✅ documentation in place
✅ CI/CD recipe established
```

**Run Commands:**
```bash
# Full test suite
pytest backend/tests/test_api_endpoints.py -v

# Specific class
pytest backend/tests/test_api_endpoints.py::TestAuthenticationEndpoints -v

# Single test
pytest backend/tests/test_api_endpoints.py::TestAuthenticationEndpoints::test_login_valid_credentials -v

# With coverage
pytest backend/tests/test_api_endpoints.py -v --cov=backend.api --cov-report=html
```

---

### DAY 3-4: LCOE Calculator Tests (12 tests)

**File:** `backend/tests/test_lcoe_calculator.py`  
**Status:** Template created ✅

**Step 1: Review LCOE Implementation**
```bash
# Check existing LCOE calculator
code backend/scripts/lcoe_calculator.py

# Verify it has:
# - calculate_lcoe() method
# - Takes: capacity_wp, efficiency, lifetime, annual_om_cost, capital_cost, irradiance
# - Returns: float (cost per kWh)
```

**Step 2: Implement Tests**

Most tests are independent (no database needed):

```python
# Remove pytest.skip() and implement:

# Test 1: Basic calculation
def test_lcoe_basic_calculation(self):
    result = self.calc.calculate_lcoe(
        capacity_wp=400,
        efficiency=0.20,
        lifetime=25,
        annual_om_cost=500,
        capital_cost=15000,
        irradiance=5.5
    )
    assert isinstance(result, float)
    assert result > 0

# Test 2: Different technologies
def test_lcoe_monocrystalline_vs_polycrystalline(self):
    mono = self.calc.calculate_lcoe(
        capacity_wp=400, efficiency=0.22, lifetime=25,
        annual_om_cost=500, capital_cost=16000, irradiance=5.5
    )
    poly = self.calc.calculate_lcoe(
        capacity_wp=400, efficiency=0.18, lifetime=25,
        annual_om_cost=500, capital_cost=14000, irradiance=5.5
    )
    assert mono > 0 and poly > 0

# Test 3: Irradiance sensitivity
def test_lcoe_irradiance_affects_result(self):
    low_irr = self.calc.calculate_lcoe(
        capacity_wp=400, efficiency=0.20, lifetime=25,
        annual_om_cost=500, capital_cost=15000, irradiance=3.0
    )
    high_irr = self.calc.calculate_lcoe(
        capacity_wp=400, efficiency=0.20, lifetime=25,
        annual_om_cost=500, capital_cost=15000, irradiance=7.0
    )
    assert low_irr > high_irr  # Higher irradiance = lower cost
```

**Step 3: Identify Requirements**

Check `backend/scripts/lcoe_calculator.py`:
- [ ] Algorithm exists
- [ ] Correct parameter names
- [ ] Returns numerical value
- [ ] Handles edge cases (zero cost, negative inputs)

If algorithm missing:
```bash
# Create basic implementation
cat > backend/scripts/lcoe_calculator.py << 'EOF'
class LCOECalculator:
    def calculate_lcoe(self, capacity_wp, efficiency, lifetime,
                      annual_om_cost, capital_cost, irradiance):
        """
        Calculate LCOE: Cost per kWh of solar energy
        
        Formula simplified:
        LCOE = (Capital Cost + (O&M Cost * Years)) / (Annual kWh * Years)
        """
        if capital_cost < 0 or capacity_wp <= 0 or lifetime <= 0:
            raise ValueError("Invalid input parameters")
        
        # Annual energy output: kWh/year
        annual_kwh = capacity_wp * efficiency * irradiance * 365 / 1000
        
        # Total cost over lifetime
        total_cost = capital_cost + (annual_om_cost * lifetime)
        
        # LCOE: $/kWh
        lcoe = total_cost / (annual_kwh * lifetime) if annual_kwh > 0 else 0
        
        return lcoe
EOF
```

**Step 4: Implementation Checklist**

- [ ] LCOE algorithm exists and testable
- [ ] All 12 unit tests created
- [ ] 10/12 tests passing
- [ ] Sensitivity analysis working
- [ ] Edge cases handled
- [ ] Batch calculator tested

**Expected by End of Day 4:**
```
✅ 12/12 LCOE tests created
✅ 10/12 tests passing
✅ Algorithm validated
✅ Sensitivity analysis documented
```

**Run Commands:**
```bash
pytest backend/tests/test_lcoe_calculator.py -v
pytest backend/tests/test_lcoe_calculator.py::TestLCOECalculator::test_lcoe_basic_calculation -v
pytest backend/tests/test_lcoe_calculator.py -v --tb=short
```

---

### DAY 4-5: MCDA Algorithm Tests

**File:** Already has tests, verify in `backend/tests/test_mcda_algorithm.py`

**Step 1: Check Existing MCDA Tests**
```bash
# Review what's already there
code backend/tests/test_mcda_algorithm.py

# Expected to find tests for:
# - Ranking communities
# - Weight validation
# - AHP calculations
```

**Step 2: Fill Gaps in MCDA Testing**

Common gaps to address:
- [ ] Weight normalization verification
- [ ] AHP consistency tests
- [ ] All 8 Angola communities tested
- [ ] Edge cases (all weight on 1 criterion)

**Step 3: Run Full MCDA Test Suite**
```bash
pytest backend/tests/test_mcda_algorithm.py -v
```

---

### DAY 5-6: End-to-End Workflow Tests

**File:** Template in `backend/tests/test_e2e_workflows.py`

**Key Workflows to Test:**

1. **New User Registration → Login → Analysis**
   ```python
   # Step 1: Register
   # Step 2: Login
   # Step 3: Submit analysis
   # Step 4: Get results
   # Verify data matches
   ```

2. **Create Scenario → Update → Delete**
   ```python
   # CRUD workflow
   # Verify persistence
   # Verify proper deletion
   ```

3. **Analysis → LCOE Calculation**
   ```python
   # Run analysis
   # Get top-ranked community
   # Calculate LCOE
   # Compare results
   ```

**Implementation Steps:**

1. Remove `pytest.skip()` from test functions
2. Ensure test user exists in database
3. Use auth fixtures from Day 2
4. Run sequentially to catch dependencies

**Expected by End of Day 6:**
```
✅ 8/8 E2E workflows created
✅ 6/8 workflows pass (1-2 may need DB fixes)
✅ Complete user journeys validated
```

---

### DAY 7: Database Integration & Validation

**Critical Tasks:**

1. **Verify Database Models**
   ```bash
   # Check all models exist
   code backend/models/
   
   # Required:
   # - User
   # - Scenario
   # - AnalysisResult
   # - Community
   # - MapData
   ```

2. **Wire API to Database**
   ```bash
   # Update API endpoints to use database
   # Before: In-memory storage
   # After: SQLAlchemy ORM operations
   
   code backend/api/api.py
   ```

3. **Run Database Integration Tests**
   ```bash
   # Create test_database_operations.py
   # Test: Create, Read, Update, Delete operations
   # Test: Data persistence
   # Test: Relationships between models
   ```

4. **Final Coverage Report**
   ```bash
   pytest tests/ -v --cov=backend --cov-report=html
   # Target: 65%+ coverage achieved
   ```

---

## 📊 WEEK 1 EXIT CRITERIA

### Test Count
- [ ] 54 new tests created
- [ ] 48+ tests passing (89% pass rate)
- [ ] 0 critical failures

### Test Coverage
- [ ] API endpoints: 100% (8/8 endpoints)
- [ ] LCOE calculator: 100% (algorithm)
- [ ] MCDA algorithm: 95%+ (logic)
- [ ] E2E workflows: 75% (setup-dependent)
- [ ] Database: 60%+ (basic CRUD)
- **Overall: 65%+ coverage**

### Quality Metrics
- [ ] No circular imports
- [ ] No unhandled exceptions
- [ ] All error codes verified
- [ ] Response schemas valid
- [ ] Database integrity confirmed

### Documentation
- [ ] Test results documented
- [ ] Coverage reports generated
- [ ] Known failures/skips documented
- [ ] Phase F completion summary created

---

## 🔧 USEFUL COMMANDS

### Development & Debugging
```bash
# Run tests with print statements
pytest tests/ -v -s

# Run single file
pytest backend/tests/test_api_endpoints.py -v

# Run specific test
pytest backend/tests/test_api_endpoints.py::TestAuthenticationEndpoints::test_login_valid_credentials -v

# Run with markers
pytest -m "auth" -v  # Only auth tests

# Run and stop on first failure
pytest -x -v

# Run with coverage
pytest --cov=backend --cov-report=html -v
```

### Database Debugging
```bash
# Reset test database
python -c "from backend.database.session import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"

# Seed test data
python backend/scripts/seed_database.py

# Check database contents
sqlite3 backend/test.db ".tables"
sqlite3 backend/test.db "SELECT * FROM users LIMIT 5;"
```

### API Testing
```bash
# Start API server
python -m uvicorn backend.api.api:app --reload --port 8000

# Test endpoint manually
curl -X GET http://localhost:8000/api/health
curl -X POST http://localhost:8000/api/analyze -H "Content-Type: application/json" -d '{"weights": {...}}'
```

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue 1: "Module not found" errors
**Solution:**
```bash
# Ensure backend is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"

# Or in conftest.py:
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```

### Issue 2: Database connection errors
**Solution:**
```bash
# Use SQLite for testing (in-memory)
DATABASE_URL = "sqlite:///:memory:"

# Or separate test database
DATABASE_URL = "sqlite:///test.db"

# Initialize database
python -c "from backend.database.session import Base, engine; Base.metadata.create_all(engine)"
```

### Issue 3: Auth token expiration
**Solution:**
```python
# In conftest.py, use test tokens with long expiration
def auth_token(client, test_user):
    """Get test token with 24-hour expiration"""
    from datetime import datetime, timedelta
    
    # Create token that expires far in future
    response = client.post("/api/auth/login", ...)
    # Verify token in response
    return response.json()["access_token"]
```

### Issue 4: Tests timeout
**Solution:**
```bash
# Increase timeout for slow operations
pytest --timeout=30 -v

# Or configure in pytest.ini:
# [pytest]
# timeout = 30
```

---

## 📈 SUCCESS METRICS

By end of Week 1, verify:

```
✅ Tests created: 54/54 (100%)
✅ Tests passing: 48/54 (89%)
✅ Coverage: 65%+
✅ API endpoints: 8/8 functional
✅ Algorithms: Validated
✅ Workflows: E2E working
✅ Database: Integrated
✅ Documentation: Complete
```

---

## 🚀 NEXT STEPS (WEEK 2)

Once Week 1 complete:

1. **GEE Integration Tests** (8 tests)
2. **Map Generation Tests** (6 tests)
3. **Dashboard Integration** (5 tests)
4. **Load Testing** (3 tests)
5. **Performance Optimization**
6. **Final Production Readiness Assessment**

---

**Estimated Time: 5-7 focused days**  
**Expected Outcome: 80%+ test coverage + production readiness**

Status: 🟡 **Ready to Start - Phase F Execution Begin**
