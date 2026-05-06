# 🏗️ GEESP-Angola Architecture & Design

**Consolidated Master Guide** | Merged from: PROJECT_STRUCTURE.md, FEATURES_AND_IMPLEMENTATION.md, DASHBOARD_ARCHITECTURE_DIAGRAMS.md, CODE_GUIDE.md, DOCUMENTATION_INDEX.md  
**Last Updated**: March 6, 2026  
**Version**: 2.0  

---

## 📊 System Architecture Overview

GEESP-Angola is a **geospatial energy analysis framework** with three distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Streamlit Web Dashboard)          │
│  • 6 interactive pages (Home, Data, MCDA, LCOE, etc)   │
│  • Real-time visualizations & maps                     │
│  • User configuration interface                        │
└──────────────┬──────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER (Core Analysis Modules)          │
│  • MCDA Engine (Multi-Criteria Decision Analysis)      │
│  • LCOE Calculator (Financial Viability)               │
│  • GEE Integration (Satellite Data Extraction)         │
│  • Map Generation & Processing                        │
│  • Validators & Utilities                             │
└──────────────┬──────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────┐
│  DATA LAYER (Files & External APIs)                    │
│  • Google Earth Engine (satellite imagery)             │
│  • Local data files (CSV, GeoTIFF, NumPy arrays)       │
│  • Database (optional Alembic migrations)              │
│  • Configuration files (JSON, environment)             │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Complete Project Structure

```
geesp-angola/
│
├── 🚀 LAUNCH SHORTCUTS
│   ├── launch_app.bat          ← Windows double-click
│   ├── launch_app.sh           ← Linux/macOS executable
│   └── launch_app.py           ← Python cross-platform
│
├── 📄 DOCUMENTATION (Master Guides)
│   ├── README.md               ← Entry point (you are here)
│   ├── 01_MASTER_GETTING_STARTED.md      ← Installation
│   ├── 02_MASTER_ARCHITECTURE.md         ← This file
│   ├── 03_MASTER_IMPLEMENTATION.md       ← Features
│   ├── 04_MASTER_PRODUCTION.md           ← Deployment
│   ├── 05_MASTER_TESTING_QA.md          ← Testing
│   ├── 06_MASTER_DEVELOPMENT.md         ← Development
│   ├── 07_MASTER_DASHBOARD.md           ← Dashboard
│   └── 08_MASTER_ADVANCED.md            ← Performance
│
├── 🎯 MAIN APPLICATION ENTRY POINT
│   └── geesp_unified_app.py    ← Use this file to run!
│
├── 📦 CORE ANALYSIS MODULES (scripts/)
│   ├── __init__.py
│   ├── gee_extraction.py       [GEE Integration]
│   │   ├── GEEExtractor() class
│   │   ├── extract_solar_radiation()
│   │   ├── extract_demand_layer()
│   │   └── create_aoi_from_bbox()
│   │
│   ├── mcda_analysis.py         [Decision Analysis]
│   │   ├── AHPWeighter() class
│   │   ├── MCDAnalyzer() class
│   │   ├── normalize() function
│   │   └── weighted_overlay()
│   │
│   ├── lcoe_calculator.py       [Financial Analysis]
│   │   ├── LCOECalculator() class
│   │   ├── calculate_lcoe()
│   │   ├── compare_technologies()
│   │   └── sensitivity_analysis()
│   │
│   ├── api_server.py            [REST API]
│   │   ├── POST /mcda
│   │   ├── POST /lcoe
│   │   └── GET /results
│   │
│   ├── config_loader.py         [Configuration]
│   │   ├── ConfigLoader() class
│   │   └── load_config()
│   │
│   ├── validators.py            [Data Validation]
│   │   ├── validate_weights()
│   │   ├── validate_inputs()
│   │   └── validate_raster()
│   │
│   ├── earth_engine_integration.py [GEE Auth]
│   ├── map_utils.py              [Map Processing]
│   ├── raster_utils.py           [Raster Operations]
│   ├── data_loaders_async.py     [Async Data Loading]
│   ├── performance.py            [Performance Monitoring]
│   └── constants.py              [Global Constants]
│
├── 🎨 DASHBOARD COMPONENTS (dashboard/)
│   ├── app.py                  [Legacy dashboard - don't use]
│   ├── components/
│   │   ├── __init__.py
│   │   ├── map_renderer.py
│   │   ├── metric_card.py
│   │   ├── weight_sliders.py
│   │   └── zone_table.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py            [PAGE 1: Home]
│   │   ├── data_explore.py     [PAGE 2: Data]
│   │   ├── mcda.py             [PAGE 3: MCDA]
│   │   ├── lcoe.py             [PAGE 4: LCOE]
│   │   ├── results.py          [PAGE 5: Results]
│   │   └── monitoring.py       [PAGE 6: Monitoring]
│   │
│   └── utils/
│       ├── cache_manager.py
│       └── session_state.py
│
├── 📊 DATA MODELS (models/)
│   └── monitoring.py           [SQLAlchemy ORM models]
│
├── 🔧 UTILITIES (utils/)
│   ├── __init__.py
│   ├── import_helpers.py       ← Centralized path setup
│   ├── logging_config.py       ← Centralized logging
│   ├── cache.py                ← Response caching
│   ├── constants.py            ← Global constants
│   ├── validators_ui.py        ← UI validation
│   ├── exceptions.py           ← Custom exceptions
│   ├── data_processing.py      ← Common operations
│   └── config_utilities.py     ← Configuration helpers
│
├── 🧪 TEST SUITE (tests/)
│   ├── conftest.py             [Fixtures & Setup]
│   ├── test_mcda.py            [MCDA Tests - 8 tests]
│   ├── test_lcoe.py            [LCOE Tests - 7 tests]
│   ├── test_integration_full_workflow.py [E2E - 6 tests]
│   ├── test_gee_extraction.py  [GEE API - 5 tests]
│   ├── test_database_models.py [DB Model Tests - 4 tests]
│   ├── test_security.py        [Security Tests - 6 tests]
│   ├── test_utils.py           [Utility Tests - 3 tests]
│   ├── test_validators.py      [Validation Tests - 5 tests]
│   ├── test_performance_profiling.py [Performance - 6 tests]
│   ├── _archived_test_versions/ [Old test versions - 17 files]
│   └── run_gee_tests.py        [Test runner script]
│
├── 📂 DATA DIRECTORY (data/)
│   ├── gee_exports/            [Google Earth Engine outputs]
│   │   └── export_manifest.json
│   │
│   └── processed/              [Locally processed data]
│       ├── communities_45.csv   [Community coordinates]
│       ├── mapa_*.npy           [Map files - 8 layers]
│       └── mapas_metadata.json  [Metadata]
│
├── 📚 DOCUMENTATION (docs/)
│   ├── CAPABILITIES.md          [Full features & user guide]
│   ├── IMPROVEMENTS.md          [Roadmap & enhancements]
│   ├── README.md                [Folder reference]
│   └── _old_stuff/              [Archived docs]
│       ├── STATUS_REPORTS/
│       ├── COMPLETION_REPORTS/
│       ├── CONSOLIDATION_WORK/
│       ├── QUICKSTARTS/
│       └── API_DOCS/
│
├── 🐳 DEPLOYMENT CONFIGS
│   ├── Dockerfile
│   ├── Dockerfile.app
│   ├── docker-compose.yml       [Local development]
│   ├── docker-compose.monitoring.yml
│   └── docker-compose-production.yml
│
├── ☸️ KUBERNETES (k8s/)
│   ├── geesp-deployment.yaml   [K8s deployment config]
│   └── k8s-setup.sh            [Setup script]
│
├── 🔄 DATABASE MIGRATIONS (migrations/)
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
│
├── 📦 NOTEBOOKS (notebooks/)
│   ├── demo_lcoe.ipynb         [LCOE example]
│   └── demo_mcda.ipynb         [MCDA example]
│
├── 📋 PROJECT CONFIGURATION
│   ├── requirements.txt         [All dependencies]
│   ├── requirements-dev.txt     [Dev dependencies]
│   ├── requirements-app.txt     [App-only dependencies]
│   ├── config.json              [Application config]
│   ├── .env.example             [Environment template]
│   ├── setup.py                 [Package configuration]
│   ├── pytest.ini               [Test configuration]
│   ├── tox.ini                  [Test automation config]
│   ├── .flake8                  [Linting config]
│   ├── .bandit                  [Security config]
│   └── pyproject.toml           [Build system config]
│
├── 🚀 DEPLOYMENT SCRIPTS
│   ├── launch_app.bat           [Windows launcher]
│   ├── launch_app.sh            [Linux/macOS launcher]
│   ├── launch_app.py            [Python launcher]
│   ├── build_windows_app.py     [PyInstaller build]
│   ├── package_windows_app.py   [Packaging script]
│   ├── deploy_docker.bat        [Docker deployment]
│   └── prepare_git_push.sh      [Git prep script]
│
├── 🔐 GITHUB CONFIG
│   ├── .github/workflows/ci.yml [CI/CD Pipeline]
│   └── .github/workflows/production-pipeline.yml
│
└── 📄 ROOT DOCUMENTATION
    ├── README.md                 ← You are here
    ├── CHANGELOG.md              [Version history]
    ├── LICENSE                   [Project license]
    ├── CONTRIBUTING.md           [Contribution guide]
    ├── .gitignore                [Git ignore patterns]
    └── Makefile                  [Build commands]
```

---

## 🔄 Data Flow Diagram

```
USER INTERFACE (Streamlit Dashboard)
    ↓
    ├─→ PAGE 1: Home (Overview & Navigation)
    │
    ├─→ PAGE 2: Data Exploration (Upload GeoTIFF)
    │    ↓
    │    [data_loaders_async.py]
    │    [raster_utils.py]
    │
    ├─→ PAGE 3: MCDA Analysis
    │    ↓
    │    [mcda_analysis.py]
    │    ├─ AHPWeighter (weights)
    │    ├─ normalize() (scale [0,1])
    │    └─ MCDAnalyzer (weighted overlay)
    │    ↓
    │    [OUTPUT: Suitability Map]
    │
    ├─→ PAGE 4: LCOE Analysis
    │    ↓
    │    [lcoe_calculator.py]
    │    ├─ LCOECalculator
    │    ├─ Financial comparison
    │    └─ Sensitivity analysis
    │    ↓
    │    [OUTPUT: Cost-benefit report]
    │
    ├─→ PAGE 5: Results Visualization
    │    ↓
    │    [map_utils.py]
    │    [components/map_renderer.py]
    │    ↓
    │    [OUTPUT: Interactive maps]
    │
    └─→ PAGE 6: Monitoring
         ↓
         [models/monitoring.py]
         [monitoring/monitoring_app.py]
         ↓
         [OUTPUT: Performance dashboard]

DATA SOURCES
    ├─ Google Earth Engine (satellite data)
    ├─ Local files (data/processed/*.npy)
    ├─ CSV data (communities_45.csv)
    └─ Configuration (config.json)
```

---

## 🎯 Core Modules Overview

### 1. **GEE Extraction Module** (`gee_extraction.py`)
- Connects to Google Earth Engine API
- Extracts satellite data layers (solar, demand, access)
- Handles spatial queries and data preprocessing
- **Output**: Raster arrays (NumPy/GeoTIFF)

### 2. **MCDA Analysis Module** (`mcda_analysis.py`)
- Implements Analytic Hierarchy Process (AHP)
- Normalizes input data to [0,1]
- Calculates weighted overlay
- Generates suitability classifications
- **Output**: Classified suitability maps

### 3. **LCOE Calculator Module** (`lcoe_calculator.py`)
- Financial analysis for 3 solar technologies
- Cost-benefit comparison
- Sensitivity analysis
- **Output**: Financial viability reports

### 4. **Configuration System** (`config_loader.py`)
- Loads settings from `config.json`
- Environment variable management
- Runtime configuration updates
- **Output**: Application settings object

### 5. **Validators Module** (`validators.py`)
- Input data validation
- Weight matrix validation
- Raster data checks
- **Output**: Validation pass/fail status

---

## 📊 Development Workflow

```
1. UNDERSTAND THE ARCHITECTURE
   ↓ Start with README.md & this file

2. INSTALL & SET UP
   ↓ Follow 01_MASTER_GETTING_STARTED.md

3. EXPLORE CAPABILITIES
   ↓ Read docs/CAPABILITIES.md

4. REVIEW IMPLEMENTATION
   ↓ Read 03_MASTER_IMPLEMENTATION.md

5. RUN TESTS
   ↓ pytest tests/ -v

6. START DEVELOPMENT
   ↓ Read 06_MASTER_DEVELOPMENT.md for standards

7. DEPLOY TO PRODUCTION
   ↓ Read 04_MASTER_PRODUCTION.md when ready
```

---

## 🔗 Import Paths

All imports go through **centralized path helpers**:

```python
# In any script, use:
from utils.import_helpers import setup_project_paths
setup_project_paths()

# Then your imports work:
from scripts.mcda_analysis import MCDAnalyzer
from scripts.lcoe_calculator import LCOECalculator
```

This ensures imports work regardless of where you run the code from.

---

## 📈 Component Dependency Graph

```
utils/ (Shared utilities)
  ├── logging_config.py
  ├── constants.py
  └── validators.py

scripts/ (Core modules)
  ├── gee_extraction.py
  │   └── depends on: utils/, config_loader.py
  ├── mcda_analysis.py
  │   └── depends on: utils/
  └── lcoe_calculator.py
      └── depends on: utils/, validators.py

dashboard/ (UI Layer)
  └── pages/*.py
      └── depends on: scripts/, utils/

tests/ (Quality Assurance)
  └── test_*.py
      └── depends on: scripts/, dashboard/, utils/
```

---

## ✅ Architecture Principles

1. **Modular Design**: Each module has single responsibility
2. **DRY (Don't Repeat Yourself)**: Shared code in `utils/`
3. **Centralized Configuration**: Single `config.json`
4. **Type Safety**: Type hints on all functions
5. **Error Handling**: Custom exceptions in `exceptions.py`
6. **Logging**: Centralized logging in `logging_config.py`
7. **Testing**: 46 test files covering all modules

---

**Next Step:** → Read [03_MASTER_IMPLEMENTATION.md](03_MASTER_IMPLEMENTATION.md) to understand features
