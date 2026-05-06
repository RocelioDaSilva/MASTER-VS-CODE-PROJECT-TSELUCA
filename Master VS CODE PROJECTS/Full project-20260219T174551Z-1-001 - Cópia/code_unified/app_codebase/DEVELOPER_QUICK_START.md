# 🚀 DEVELOPER QUICK START - GEESP-Angola

**For Consolidated Backend (Post-Phases 1-3)**  
**Updated:** March 8, 2026

---

## ⚡ 5-Minute Setup

### 1. Clone & Setup Environment
```bash
cd geesp-angola
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# OR
source venv/bin/activate      # Linux/Mac
```

### 2. Install Dependencies
```bash
# Development environment (recommended)
pip install -r requirements-dev.txt

# Verify installation
python -c "import streamlit; print('✓ Ready')"
```

### 3. Run Tests
```bash
pytest  # Should see ✓ tests passing
```

### 4. Start Dashboard
```bash
streamlit run backend/dashboard/app.py
```
👉 Open http://localhost:8501

---

## 📁 New Structure (Post-Consolidation)

**Key Changes:**
- `backend/utils/` - NO MORE nested utils/utils/ ❌
- `backend/scripts/` - NO MORE nested scripts/scripts/ ❌
- `backend/maps/` - NEW consolidated module ✨
- `backend/geospatial/` - NEW consolidated module ✨
- `backend/tests/conftest.py` - ONE unified fixture file ✨

### Quick File Navigation

```
backend/
  utils/                    ← All utilities (flat!)
    config_manager.py
    constants.py
    logging_config.py
    → etc.
  
  scripts/                  ← All scripts (flat!)
    mcda_analysis.py        ← Main MCDA solver
    lcoe_calculator.py      ← LCOE calculations
    validation_pipeline.py
    → etc.
  
  maps/                     ← Map operations
    generate.py             ← Map generation
    pdf_export.py           ← PDF exports
  
  geospatial/              ← GEE operations
    earth_engine.py         ← Earth Engine client
  
  dashboard/               ← Streamlit app
    app.py                  ← Main entry point
  
  tests/
    conftest.py            ← All fixtures here!
    unit/                   ← Unit tests
    integration/            ← Integration tests
    e2e/                    ← E2E tests
```

---

## 📦 Common Installation Scenarios

### Production Deploy
```bash
pip install -r requirements.txt
```
✓ Streamlit, data science, mapping tools  
✗ No dev/testing tools

### Development
```bash
pip install -r requirements-dev.txt
```
✓ Everything including pytest, linters, formatters  
✓ Recommended for local development

### Minimal App
```bash
pip install -r requirements-app.txt
```
✓ Bare minimum for Streamlit app  
✗ No advanced geospatial tools

### Reproducible Build
```bash
pip install -r requirements-lock.txt
```
✓ Exact pinned versions  
✓ Used in Docker for consistency

---

## 🔌 Common Imports (Updated for Flat Structure)

```python
# ✓ Utilities (from backend/utils/)
from utils.constants import MCDAConstants, LCOEConstants
from utils.logging_config import setup_logging

# ✓ Scripts (from backend/scripts/)
from mcda_analysis import MCDAnalyzer
from lcoe_calculator import LCOECalculator
from validation_pipeline import run_validation_pipeline

# ✓ New modules (fully qualified)
from backend.maps.generate import generate_map
from backend.geospatial.earth_engine import EarthEngineClient

# ✗ OLD (no longer needed)
# from backend.utils.utils.constants import ...  ❌ DON'T USE
# from backend.scripts.scripts.mcda_analysis import ...  ❌ DON'T USE
```

---

## 🧪 Testing Quick Reference

```bash
# Run all tests
pytest

# Run specific test level
pytest backend/tests/unit/          # Fast ✓
pytest backend/tests/integration/   # Medium
pytest backend/tests/e2e/           # Slow

# With coverage
pytest --cov=backend

# Debug mode
pytest -vv --pdb
```

**Test files have access to unified fixtures:**
```python
def test_example(sample_array_2d, mock_config, temp_dir):
    # All fixtures from root conftest.py available!
    pass
```

---

## 🐳 Docker Quick Start

```bash
# Development (Streamlit)
docker-compose up -d
# → http://localhost:8501

# Production (API + Database)
docker-compose -f docker-compose-production.yml up -d
# → http://localhost:8000

# With monitoring (Prometheus + Grafana)
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
# → Grafana: http://localhost:3000 (admin/admin)
```

---

## 🛠️ Code Quality

```bash
# Format code
black backend/

# Check linting
flake8 backend/
pylint backend/

# Type checking
mypy backend/

# All at once
black backend/ && flake8 backend/ && mypy backend/
```

---

## 🐛 Troubleshooting

### Import Error: "ModuleNotFoundError: No module named 'utils'"
**Fix:** Ensure `sys.path.insert(0, str(backend_root))` in entry point

### Test Discovery Issues
**Fix:** Run from project root: `pytest backend/tests/`

### Docker Port Conflict
**Fix:** `docker-compose down` then `docker-compose up -d`

### Permission Denied (Linux/Mac)
**Fix:** `chmod +x backend/scripts/*.sh`

---

## 📚 Documentation

- **Full Guide:** [CONSOLIDATION_GUIDE.md](CONSOLIDATION_GUIDE.md)
- **Architecture:** [PHASE3_CONSOLIDATION_REPORT.md](PHASE3_CONSOLIDATION_REPORT.md)
- **Import Details:** [PHASE2B_3_COMPLETION_REPORT.md](PHASE2B_3_COMPLETION_REPORT.md)

---

## ✨ Key Files to Know

| File | Purpose |
|------|---------|
| `backend/dashboard/app.py` | Streamlit entry point |
| `backend/utils/__init__.py` | Utility module exports |
| `backend/scripts/mcda_analysis.py` | MCDA solver |
| `backend/tests/conftest.py` | ALL test fixtures |
| `requirements-dev.txt` | Dev dependencies |
| `docker-compose.yml` | Dev environment |

---

## ✅ First 10 Minutes Checklist

- [ ] Activated virtual environment
- [ ] Installed dependencies (`pip install -r requirements-dev.txt`)
- [ ] Ran tests (`pytest`)
- [ ] Started dashboard (`streamlit run ...`)
- [ ] Accessed http://localhost:8501
- [ ] Made a code change and verified hot-reload
- [ ] Read CONSOLIDATION_GUIDE.md for full reference

---

**Ready to code!** 🎉

