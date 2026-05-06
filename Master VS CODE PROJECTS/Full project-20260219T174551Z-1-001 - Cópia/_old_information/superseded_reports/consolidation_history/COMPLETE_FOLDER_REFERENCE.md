# 02_Code Folder Structure - Complete Reference Guide

**Generated**: March 6, 2026  
**Location**: `Full project\02_Code`

---

## 📊 Overview

The `02_Code` directory contains:
- **4 main folders** at root level
- **geesp-angola**: Main Python/Streamlit application (primary focus)
- **docs**: Documentation and guides
- **ARCHIVE**: Legacy code and implementations
- **nevermindu**: Node.js/npm project
- **.pytest_cache**: Testing cache

---

## 🗂️ COMPLETE FOLDER STRUCTURE

### 📁 **geesp-angola/** (MAIN APPLICATION)
```
geesp-angola/                          # Main Python/Streamlit project
│
├── 📄 Configuration Files
│   ├── .bandit                        # Security configuration
│   ├── .dockerignore                  # Docker ignore rules
│   ├── .editorconfig                  # Editor configuration
│   ├── .env.example                   # Environment variables template
│   ├── .gitignore                     # Git ignore rules
│   ├── .pre-commit-config.yaml        # Pre-commit hooks
│   ├── config.json                    # Application config
│   ├── docker-compose*.yml            # Docker compose files (4 files)
│   ├── Dockerfile*                    # Docker images (3 files)
│   ├── GEESP-Angola.spec              # PyInstaller spec
│   ├── Makefile                       # Build automation
│   ├── pyproject.toml                 # Python project config
│   ├── requirements*.txt              # Python dependencies
│   └── tox.ini                        # Testing configuration
│
├── 📄 Documentation Files (12 Master Guides)
│   ├── 01_MASTER_GETTING_STARTED.md
│   ├── 02_MASTER_ARCHITECTURE.md
│   ├── 03_MASTER_IMPLEMENTATION.md
│   ├── 04_MASTER_PRODUCTION.md
│   ├── 05_MASTER_TESTING_QA.md
│   ├── 06_MASTER_DEVELOPMENT.md
│   ├── 07_MASTER_DASHBOARD.md
│   ├── 08_MASTER_ADVANCED.md
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   └── MARKDOWN_CONSOLIDATION_SUMMARY.md
│
├── 📄 Phase 5B Consolidation Reports
│   ├── PHASE_5B_COMPLETE_CONSOLIDATION_REPORT.md
│   ├── TEST_SUITE_FINAL_STATUS.md
│   └── phase3a_*.json                 # Test results
│
├── 📄 Build & Launch Scripts
│   ├── build_windows_app.py           # Windows PyInstaller build
│   ├── launch_app.sh                  # Linux launch script
│   ├── run_all_tests.bat              # Windows batch test runner
│   ├── run_tests.py                   # Python test runner
│   └── test_consolidation.py          # Consolidation tests
│
├── 📄 Metadata Files
│   ├── LICENSE                        # Project license
│   ├── CODEOWNERS                     # Code ownership
│   └── version (implicit)
│
├── 📁 .github/
│   └── workflows/                     # GitHub Actions CI/CD pipelines
│
├── 📁 .vscode/
│   └── [VS Code settings & launch configs]
│
├── 📁 .streamlit/
│   └── [Streamlit configuration files]
│
├── 📁 scripts/ (11 CORE PYTHON MODULES - CONSOLIDATED)
│   ├── __init__.py
│   ├── base.py                        # Base classes
│   ├── config_loader.py               # Configuration loading
│   ├── core_utils.py                  # Core utilities
│   ├── data_loaders_async.py          # Async data loading
│   ├── lcoe_calculator.py             # LCOE calculation
│   ├── map_utils.py                   # Map generation (refactored)
│   ├── mcda_analysis.py               # MCDA analysis
│   ├── performance.py                 # Performance monitoring
│   ├── raster_utils.py                # Raster operations (unified normalize)
│   ├── validation_pipeline.py         # Data validation
│   └── (build/, migration/ subdirs)
│
├── 📁 utils/ (CONSOLIDATED UTILITIES)
│   ├── __init__.py
│   ├── logging_config.py              # Unified logging (created)
│   ├── exceptions.py                  # Custom exceptions
│   └── (other utility modules)
│
├── 📁 tests/ (6 ACTIVE CORE TESTS - CONSOLIDATED)
│   ├── __init__.py
│   ├── conftest.py                    # PyTest configuration
│   ├── run_gee_tests.py               # GEE test runner
│   ├── test_communities.py            # Community data tests
│   ├── test_dashboard_components.py   # Dashboard components
│   ├── test_dashboard_pages.py        # Dashboard pages
│   ├── test_dashboard_state.py        # Dashboard state
│   ├── test_database_models.py        # Database models
│   ├── test_maps_pdf.py               # PDF map generation
│   ├── test_mcda.py                   # MCDA analysis
│   ├── test_performance_profiling.py  # Performance profiling
│   └── (11 archived tests in useless/)
│
├── 📁 dashboard/ (STREAMLIT APPLICATION)
│   ├── __init__.py
│   ├── components/                    # Dashboard UI components
│   ├── pages/                         # Streamlit pages
│   ├── styles/                        # CSS/styling
│   └── utils/                         # Dashboard utilities
│
├── 📁 code/ (LEGACY CODE ORGANIZATION)
│   ├── gee_exports/                   # Google Earth Engine exports
│   ├── processed/                     # Processed data files
│   └── versions/                      # Code versions
│
├── 📁 models/ (DATA MODELS)
│   ├── api/                           # API data models
│   ├── build/                         # Build artifacts
│   ├── gee/                           # GEE service models
│   ├── maps/                          # Map generation models
│   ├── migration/                     # Database migrations
│   └── __pycache__/
│
├── 📁 data/ (DATASETS)
│   ├── (processing scripts)
│   └── (data files organized by type)
│
├── 📁 integration/ (INTEGRATION TESTS)
│   ├── performance/
│   ├── unit/
│   └── __pycache__/
│
├── 📁 useless/ (CONSOLIDATED ARCHIVES)
│   ├── documentation/
│   │   ├── archived_redundant/        # 47 archived docs
│   │   ├── old_stuff/                 # Legacy docs
│   │   └── (52 total archived markdown files)
│   │
│   └── archived_tests_phase5/         # 11 archived test files
│       ├── test_e2e_workflows.py
│       ├── test_edge_cases_comprehensive.py
│       ├── test_gee_extraction.py
│       ├── test_integration_full_workflow.py
│       ├── test_lcoe.py
│       ├── test_load_performance.py
│       ├── test_maps.py
│       ├── test_security.py
│       ├── test_utils.py
│       ├── test_validators.py
│       └── test_database_models.py
│
├── 📁 logs/ (APPLICATION LOGS - EMPTY AFTER CONSOLIDATION)
│   └── (59 log files deleted in Phase 5A)
│
├── 📁 monitoring/ (MONITORING CONFIGURATION)
│   ├── (metrics & health checks)
│   └── (alert configurations)
│
├── 📁 migrations/ (DATABASE MIGRATIONS)
│   ├── (Alembic/sqlalchemy migrations)
│   └── (schema versions)
│
├── 📁 notebooks/ (JUPYTER ANALYSIS)
│   ├── (analysis notebooks)
│   └── (exploration & prototyping)
│
├── 📁 k8s/ (KUBERNETES CONFIGURATION)
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   └── helm/
│
├── 📁 ARCHIVE/ (OLDER CODE VERSIONS)
│   ├── _archive/                      # Archived application variants
│   │   ├── api/
│   │   ├── benchmarking/
│   │   ├── build_and_verification/
│   │   ├── config/
│   │   ├── entry_points/
│   │   ├── logging/
│   │   ├── map_generation/
│   │   ├── orphaned/
│   │   ├── phase_history/
│   │   ├── test_infrastructure/
│   │   ├── test_variants/
│   │   ├── utilities/
│   │   └── validation/
│   └── (legacy implementations)
│
├── 📁 build/ (BUILD ARTIFACTS)
│   ├── PyInstaller output
│   ├── Compiled binaries
│   └── Build logs
│
├── 📁 dist/ (DISTRIBUTION FILES)
│   ├── Packaged applications
│   └── Release builds
│
├── 📁 venv/ (PYTHON VIRTUAL ENVIRONMENT)
│   ├── Scripts/
│   │   ├── activate.ps1
│   │   └── python.exe
│   └── Lib/
│       └── site-packages/
│
├── 📁 .mypy_cache/ (TYPE CHECKING CACHE)
│   └── (mypy type checking cache)
│
├── 📁 .pytest_cache/ (TESTING CACHE)
│   └── v/ (.pytest metadata)
│
└── 📁 __pycache__/ (COMPILED PYTHON FILES)
    └── (*.pyc files)
```

---

### 📁 **docs/** (DOCUMENTATION)
```
docs/
├── analysis/                          # Data analysis documentation
├── api-examples/                      # API usage examples
├── guides/                            # User guides
│   ├── analysis/
│   ├── authentication/
│   └── scenarios/
├── archived-versions/                 # Old documentation versions
└── ERROR_CODES.md                     # Error documentation
```

---

### 📁 **ARCHIVE/** (LEGACY CODE)
```
ARCHIVE/
├── legacy-fixes/                      # Legacy bug fixes
├── manual-implementation/             # Manual implementations
└── README.md
```

---

### 📁 **nevermindu/** (NODE.JS PROJECT)
```
nevermindu/
├── node_modules/                      # npm dependencies
├── src/                               # Source code
│   ├── .bin/
│   ├── @babel/, @esbuild/...         # npm packages
│   └── ...
├── package.json
├── package-lock.json
└── .env.example
```

---

### 📁 **.pytest_cache/** (TEST CACHE)
```
.pytest_cache/
├── v/
│   └── cache/                         # pytest cache files
├── .gitignore
├── CACHEDIR.TAG
└── README.md
```

---

## 📊 CONSOLIDATION STATUS (Phase 5B)

| Category | Before | After | Reduction | Status |
|----------|--------|-------|-----------|--------|
| **Markdown Files** | 138 | 12 | 91% | ✅ Consolidated |
| **Test Files** | 58 | 6 | 90% | ✅ Consolidated |
| **Archived Tests** | - | 11 | - | ✅ Safe archive |
| **Log Files** | 59 | 0 | 100% | ✅ Deleted |
| **Python Scripts** | 30 | 11 | 63% | ✅ Consolidated |
| **Total Files** | 445 | ~280 | **37-39%** | ✅ COMPLETE |

---

## 🔍 KEY FILES BY CATEGORY

### Configuration
- `config.json` - Main app configuration
- `.env.example` - Environment template
- `pyproject.toml` - Python project metadata
- `docker-compose.yml` - Docker orchestration
- `tox.ini` - Test automation

### Source Code (scripts/)
- `raster_utils.py` - Unified normalization (cached)
- `map_utils.py` - Map generation (refactored)
- `lcoe_calculator.py` - Solar economics
- `mcda_analysis.py` - Multi-criteria analysis
- `config_loader.py` - Configuration management
- `core_utils.py` - Shared utilities
- `validation_pipeline.py` - Data validation

### Testing (tests/)
- `test_mcda.py` - MCDA analysis ✅
- `test_maps_pdf.py` - PDF generation ✅
- `test_dashboard_*.py` - Dashboard (3 files) ✅
- `test_communities.py` - Community data ✅
- `conftest.py` - Pytest configuration ✅

### Documentation (12 Master Guides)
1. Getting Started Guide
2. Architecture Overview
3. Implementation Details
4. Production Deployment
5. Testing & QA
6. Development Guide
7. Dashboard Reference
8. Advanced Topics
9. README
10. Changelog
11. Contributing Guidelines
12. Consolidation Summary

---

## 🚀 Quick Navigation

| Purpose | Path | Files |
|---------|------|-------|
| **Run App** | `geesp-angola/` | `launch_app.sh` |
| **Run Tests** | `geesp-angola/tests/` | `run_tests.py` |
| **View Logs** | `geesp-angola/logs/` | _(cleared in Phase 5A)_ |
| **Read Guides** | `geesp-angola/` | `0*_MASTER_*.md` |
| **Modify Config** | `geesp-angola/` | `config.json` |
| **Kubernetes** | `geesp-angola/k8s/` | `*.yaml` |
| **Database** | `geesp-angola/migrations/` | `*.py` |
| **Docker** | `geesp-angola/` | `docker-compose*.yml` |
| **Dashboard** | `geesp-angola/dashboard/` | `components/`, `pages/` |

---

## 📋 Test Execution

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_mcda.py -v

# Run with coverage
python -m pytest tests/ --cov=scripts

# Expected: 6 passed, 1 skipped (~4 seconds)
```

---

## 📦 File Counts by Directory

| Directory | Files | Type |
|-----------|-------|------|
| `scripts/` | 11 | Python modules (core) |
| `tests/` | 6 | Python tests (active) |
| `dashboard/` | 10+ | Streamlit components |
| `models/` | 12+ | Data models |
| `docs files root/` | 12 | Markdown (master guides) |
| `utils/` | 5+ | Utility modules |
| `ARCHIVE/` | 47+ | Legacy code |
| `useless/` | 63 | Consolidated files |

**Total Active**: ~280 files  
**Total Archived**: 63 files  
**Total Project**: 343 files  

---

## ✅ Phase 5B Consolidation Summary

**Completed Consolidations**:
- ✅ Code refactoring (map_utils unified)
- ✅ Test suite reduction (58 → 6 active)
- ✅ Documentation consolidation (138 → 12 master guides)
- ✅ Log file deletion (59 files)
- ✅ Script consolidation (30 → 11 core)
- ✅ All tests passing (6/6)

**Verification**: All remaining tests ✅ PASSING  
**Status**: READY FOR DEPLOYMENT 🚀

---

**Last Updated**: March 6, 2026  
**Created by**: Phase 5B Consolidation  
**Location**: `02_Code/geesp-angola/`
