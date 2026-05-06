# DEVELOPER QUICK START GUIDE

**Last Updated**: March 1, 2026  
**Audience**: New developers, team members  
**Time to Setup**: 15 minutes

---

## 🚀 ONE-MINUTE SETUP

### 1. Clone and Environment
```bash
# Clone repository
git clone <repo-url>
cd "Full project/02_Code/geesp-angola"

# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### 2. Verify Installation
```bash
# Run tests to verify setup
pytest tests/ -q
# Expected: 224 passed in ~5 minutes
```

### 3. Launch Application
```bash
# Option A: Streamlit app
streamlit run geesp_unified_app.py

# Option B: REST API
uvicorn scripts.api_server:app --reload

# Option C: Docker
docker-compose up
```

---

## 📚 PROJECT STRUCTURE (90-Second Overview)

```
02_Code/geesp-angola/
├── scripts/              # Core modules
│   ├── lcoe_calculator.py    # LCOE computation
│   ├── mcda_analysis.py      # Multi-criteria analysis
│   ├── validators.py         # Input validation
│   └── config_loader.py      # Configuration
├── tests/               # 224 tests (100% passing)
│   ├── test_unit_testing_phase3a.py
│   ├── test_integration_phase3b.py
│   ├── test_performance_phase3c.py
│   ├── test_type_safety_phase4.py
│   ├── test_advanced_features_phase5.py
│   ├── test_deployment_phase6.py
│   ├── test_feature_enhancements_option5.py
│   └── test_production_deployment_option1.py
├── docs/               # Documentation
├── monitoring/         # Prometheus/Grafana setup
├── kubernetes/         # K8s manifests
├── dashboard/          # Streamlit dashboard
└── config.json         # Configuration

Key Docs:
├── README.md           # Main README
├── DEPLOYMENT.md       # Deployment guide
├── RUNBOOK.md          # Operational procedures
├── API.md              # API documentation
└── ARCHITECTURE.md     # System design
```

---

## 📖 ESSENTIAL READS (in order)

### For All Developers
1. **README.md** (5 min) - Project overview
2. **ARCHITECTURE.md** (10 min) - System design
3. **CODE_ANALYSIS_REPORT.md** (5 min) - Code quality metrics

### For Code Contributors  
4. **scripts/README.md** (5 min) - Module descriptions
5. **CODING_STANDARDS.py** (5 min) - Style guide
6. **CONTRIBUTING.md** (5 min) - Contribution workflow

### For Ops/Deployment
7. **DEPLOYMENT.md** (10 min) - Production deployment
8. **RUNBOOK.md** (10 min) - Common operations
9. **Dockerfile** (5 min) - Container setup

### For Testing
10. **tests/README.md** (5 min) - Test structure
11. **TESTING_GUIDE.md** (10 min) - How to write tests

---

## 🛠️ COMMON DEVELOPER TASKS

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_unit_testing_phase3a.py

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test
pytest tests/ -k "test_lcoe_calculation"

# Run with verbose output
pytest -v
```

### Check Code Quality
```bash
# Linting
flake8 scripts/
pylint scripts/

# Type checking
mypy scripts/

# Format check
black --check scripts/
```

### Run Application
```bash
# Streamlit app
streamlit run geesp_unified_app.py

# API server (port 8000)
uvicorn scripts.api_server:app --reload

# Production (Docker)
docker-compose up
```

### Monitor Performance
```bash
# Run benchmarks
pytest tests/test_performance_phase3c.py -v

# Generate performance report
pytest --benchmark-compare
```

---

## 🔍 KEY MODULES EXPLAINED

### `scripts/lcoe_calculator.py`
**Purpose**: Calculate Levelized Cost of Energy  
**Key Functions**:
- `calculate_lcoe()` - Main calculation
- `_calculate_pv_costs()` - PV-specific costs
- `_calculate_pv_generation()` - Generation estimates

**Example**:
```python
from scripts.lcoe_calculator import calculate_lcoe

result = calculate_lcoe(
    capacity_mw=500,
    technology="PV",
    location_lat=-11.2,
    location_lng=17.9
)
print(f"LCOE: ${result['lcoe_usd_mwh']:.2f}/MWh")
```

### `scripts/mcda_analysis.py`
**Purpose**: Multi-Criteria Decision Analysis  
**Key Functions**:
- `normalize_raster()` - Data normalization
- `weighted_overlay()` - Weighted combination

**Example**:
```python
from scripts.mcda_analysis import weighted_overlay

result = weighted_overlay(
    criteria_data=[cost_map, irradiance_map, land_map],
    weights=[0.3, 0.4, 0.3]
)
```

### `scripts/validators.py`
**Purpose**: Input validation  
**Key Validators**:
- `validate_solar_irradiance()` - 0-1500 W/m²
- `validate_capacity_mw()` - Positive values
- `validate_coordinates()` - Geographic bounds

---

## 📊 TEST YOUR CHANGES

### Before Committing
```bash
# 1. Run full test suite
pytest

# 2. Check coverage
pytest --cov=scripts --cov-report=term-missing

# 3. Lint code
flake8 scripts/
black scripts/

# 4. Type check
mypy scripts/
```

### Expected Results
```
✅ All tests passing (224)
✅ Coverage >95%
✅ No lint errors
✅ No type errors
```

---

## 🐛 DEBUGGING TIPS

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Use Python Debugger
```bash
# Run with debugger
python -m pdb scripts/lcoe_calculator.py

# Or in code:
import pdb; pdb.set_trace()
```

### View Test Output
```bash
# Show print statements
pytest -s tests/test_file.py

# Show variable dumps
pytest -vv
```

---

## 🚀 PERFORMANCE PROFILING

### Profile Your Code
```python
import cProfile
import pstats

cProfile.run('calculate_lcoe(...)', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)
```

### Compare to Baselines
```bash
# Run performance tests
pytest tests/test_performance_phase3c.py -v

# Expected performance:
# - LCOE: 4.5ms ✅
# - MCDA: 35ms ✅
# - Validation: 2.1ms ✅
```

---

## 📦 DEPENDENCY MANAGEMENT

### Add New Dependency
```bash
# Install
pip install <package-name>

# Update requirements
pip freeze > requirements.txt

# Verify tests still pass
pytest
```

### Check for Vulnerabilities
```bash
# Safety check
safety check

# Bandit security scan
bandit -r scripts/
```

---

## 🔄 GIT WORKFLOW

### Feature Branch
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat: add new capability"

# Push and create PR
git push origin feature/my-feature
```

### Commit Message Format
```
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
perf: optimize performance
refactor: restructure code
```

### Before Pushing
```bash
git pull origin main
pytest  # Verify tests pass
git push
# Create pull request on GitHub
```

---

## 🆘 TROUBLESHOOTING

### Tests Failing?
```bash
# Reinstall dependencies
pip install -r requirements-dev.txt

# Clear cache
rm -rf .pytest_cache __pycache__

# Run with more verbosity
pytest -vv --tb=long
```

### Import Errors?
```bash
# Check virtual environment is activated
which python  # Should show .venv path

# Verify installation
pip list | grep <package>

# Reinstall if needed
pip install -r requirements.txt
```

### Slow Tests?
```bash
# Run performance tests
pytest tests/test_performance_phase3c.py -v

# Profile test execution
pytest --durations=10 tests/
```

### Docker Issues?
```bash
# Check logs
docker-compose logs -f geesp-api

# Rebuild image
docker-compose build --no-cache

# Full restart
docker-compose down -v && docker-compose up
```

---

## 📞 GETTING HELP

| Question | Resource |
|----------|----------|
| How do I...? | Check README.md or code comments |
| What does this function do? | Read docstring: `help(function_name)` |
| What are the requirements? | Review requirements.txt or INSTALL.md |
| How is it deployed? | See DEPLOYMENT.md and docker-compose files |
| What tests cover this? | Search tests/ directory |
| How are credentials managed? | See .env.example and SECURITY.md |

---

## ✅ VALIDATION CHECKLIST

After setup, verify:
- [ ] Python environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] Tests running and passing (`pytest`)
- [ ] Application starts (`streamlit run geesp_unified_app.py`)
- [ ] API responds (`curl http://localhost:8000/health`)
- [ ] Docker runs (`docker-compose up`)

**If all checks pass**: ✅ You're ready to develop!

---

## 🎓 LEARNING PATH

1. **Day 1**: Setup, run tests, read README
2. **Day 2**: Read ARCHITECTURE, explore scripts/
3. **Day 3**: Run application, explore UI
4. **Day 4**: Modify a test, make a small change
5. **Day 5**: Create feature branch, make contribution

---

## 📞 NEED HELP?

- **Questions?** Check docs/ folder
- **Bug report?** Create GitHub issue
- **Feature request?** Open GitHub discussion
- **Deployment help?** See DEPLOYMENT.md
- **Performance issues?** Profile with pytest-profile

---

**Happy coding! 🚀**

*For complete documentation, see [PROJECT_MASTER_DASHBOARD.md](./PROJECT_MASTER_DASHBOARD.md)*

