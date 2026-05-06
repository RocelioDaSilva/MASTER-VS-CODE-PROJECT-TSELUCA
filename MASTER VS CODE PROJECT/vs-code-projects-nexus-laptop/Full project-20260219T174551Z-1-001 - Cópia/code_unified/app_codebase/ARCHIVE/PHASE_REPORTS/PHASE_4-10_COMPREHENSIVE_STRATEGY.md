# CONSOLIDATED CONSOLIDATION STRATEGY & EXECUTION PLAN
**Complete Analysis for GEESP-Angola Codebase Consolidation**  
**Phases 4-10: Design, Implementation, Reporting**  
**Date**: March 6, 2026

---

## EXECUTIVE SUMMARY

**Current State**: 445 meaningful files, 60 MB, 57 directories  
**Analysis Complete**: Phases 1-3 finished with comprehensive redundancy analysis  
**Consolidation Target**: 250-280 files (40-45% reduction)

**Quick Wins** (143 files, 25 minutes): Can execute immediately with zero risk
- Delete all log files (59 files)
- Delete archive tests (26 files)
- Delete backup files (7 files)
- Archive old documentation (47 files)
- Consolidate duplicate reports (4 files)

---

## PHASE 4: UNIFIED IMPLEMENTATION DESIGNS

### 4A: Utility Function Consolidation

**Target**: Normalize all array/raster operations to single unified interface

#### 1. Unified Normalization Function (PRIMARY)

**Location**: `scripts/raster_utils.py::normalize()`  
**Status**: ✅ Already well-designed

**Function Signature**:
```python
def normalize(
    data: Union[np.ndarray, Dict[str, np.ndarray]],
    minimum: float = None,
    maximum: float = None,
    name: str = "raster",
    handle_constant: bool = True,
    cache_key: Optional[str] = None,
    use_cache: bool = True,
    preserve_nan: bool = True
) -> Union[np.ndarray, Dict[str, np.ndarray]]:
```

**Features**:
- ✅ Single array or batch dictionary
- ✅ Global caching with performance optimization
- ✅ NaN preservation for rasters
- ✅ Constant array handling
- ✅ Well-documented with benchmarks

**Impact**: All normalization across codebase should use this function

---

#### 2. Unified Array Validation (PRIMARY)

**Location**: `scripts/core_utils.py`  
**Status**: ✅ Already well-designed

**Functions**:
- `validate_array_shape(data, expected_shape)` - Shape validation
- `get_valid_data_mask(data)` - NaN/inf detection
- `ensure_numpy_array(data)` - Type conversion
- `get_data_statistics(data)` - Compute statistics

**Impact**: All validation across codebase should use these functions

---

#### 3. Refactored Map Aptitude Calculation

**Location**: `scripts/map_utils.py::compute_aptitude()`  
**Current Status**: Uses inline normalization
**Proposed Status**: Use unified raster_utils.normalize()

**Refactored Implementation**:
```python
from scripts.raster_utils import normalize
from scripts.core_utils import get_data_statistics

def compute_aptitude(
    solar: np.ndarray,
    population: np.ndarray,
    distance: np.ndarray,
    slope: np.ndarray,
    ndvi: np.ndarray,
    weights: Dict[str, float] = None,
) -> np.ndarray:
    """Compute weighted aptitude map using unified normalization."""
    
    # Use unified normalization with caching
    norm_batch = normalize(
        {
            'solar': solar,
            'population': population,
            'distance': distance,
            'slope': slope,
            'ndvi': ndvi
        },
        cache_key='aptitude_components'
    )
    
    solar_norm = norm_batch['solar']
    population_norm = norm_batch['population']
    distance_norm = 1 - norm_batch['distance']  # Inverse (farther is worse)
    slope_norm = 1 - norm_batch['slope']        # Inverse (steeper is worse)
    ndvi_norm = norm_batch['ndvi']
    
    # Apply weights
    w = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)
    
    aptitude = (
        w["irradiacao"] * solar_norm
        + w["populacao"] * population_norm
        + w["distancia_rede"] * distance_norm
        + w["declividade"] * slope_norm
        + w["ndvi"] * ndvi_norm
    )
    
    result = np.clip(aptitude, MCDAConstants.APTITUDE_LOW, MCDAConstants.APTITUDE_HIGH).astype(np.float32)
    return result
```

**Benefits**:
- ✅ Uses unified normalization (caching, validation)
- ✅ Cleaner, more maintainable
- ✅ Consistent across all MCDA operations
- ✅ Proper error handling

---

### 4B: Documentation Consolidation

**Target**: 138 markdown files → 8-10 master guides

**Unified Documentation Structure**:
```
geesp-angola/
├── 01_GETTING_STARTED.md        (Getting Started + Quick Setup)
├── 02_ARCHITECTURE.md           (System Design + Dashboard Architecture)
├── 03_DEVELOPMENT.md            (Development + Testing guides)
├── 04_OPERATIONS.md             (Production + Advanced Deployment)
├── CONTRIBUTING.md              (Keep - standard contribution guide)
├── CHANGELOG.md                 (Keep - version history)
├── LICENSE.md                   (Keep - license)
└── README.md                    (Keep - project overview)
```

**Process**:
1. Keep 8 MASTER guides (already consolidated)
2. DELETE 78 root-level markdown files (consolidation reports, duplicates, etc.)
3. ARCHIVE 47 old documentation files from code/_archive/
4. CONSOLIDATE 51 documentation subdirectory files into above structure

**Files to Delete**:
```
DELETE (Consolidation reports):
  CONSOLIDATION_COMPLETE_SUMMARY.md
  CONSOLIDATION_SUMMARY.md
  CONSOLIDATION_PLAN.md
  CONSOLIDATION_INDEX.md
  CODE_CONSOLIDATION_EXECUTION.md
  CODE_CONSOLIDATION_PLAN.md
  CODE_CONSOLIDATION_STATUS.md
  ...and 71 more duplicate/completion reports
```

---

### 4C: Test Suite Consolidation

**Target**: 58 test files → 18-20 active test files

**New Test Structure**:
```
tests/
├── conftest.py                  (Shared fixtures)
├── test_app.py                  (Main application tests)
├── test_api.py                  (API endpoints)
├── test_core_utils.py           (Utilities)
├── test_data_loaders.py         (Data loading)
├── test_mcda_analysis.py        (MCDA analysis)
├── test_lcoe_calculator.py      (LCOE calculations)
├── test_map_generation.py       (Map creation)
├── test_validation.py           (Validation pipeline)
├── test_performance.py          (Performance benchmarks)
├── test_error_handling.py       (Error scenarios)
├── test_integration.py          (End-to-end integration)
└── test_edge_cases.py           (Edge case scenarios)
```

**Process**:
1. DELETE all 26 archive tests (obsolete phase-specific tests)
2. CONSOLIDATE 32 active tests into 13-15 logical test modules
3. Remove duplicate test coverage
4. Ensure all critical paths tested

---

### 4D: Script Consolidation

**Target**: 6 map/data scripts → 3-4 focused scripts

**Recommended Structure**:
```
scripts/maps/
├── generate_maps.py             (Main map generator)
├── convert_maps_pdf.py          (PDF generation - consolidated)
├── run_all_maps.py              (Orchestrator)
└── (DELETE generate_maps_simple.py if truly redundant)

scripts/data/
├── data_loaders_async.py        (Data loading)
├── earth_engine_integration.py  (GEE integration)
└── gee_extraction.py            (GEE extraction utilities)
```

**Process**:
1. INSPECT code to verify generate_maps_simple.py vs generate_maps.py
2. CONSOLIDATE PDF generation (enhanced_maps_to_pdf.py + convert_maps_pdf.py → 1 function)
3. VERIFY run_all_maps.py provides orchestration value
4. DELETE redundant implementations

---

## PHASE 5: QUICK WINS EXECUTION PLAN

**These can be executed today with ZERO risk of breaking anything:**

### 5A: Delete Log Files (59 files)
```
Action: Delete all *.log files in logs/ directory
Files: logs/*.log (59 total)
Time: 5 minutes
Risk: NONE - These are generated application outputs, not source code
Verification: Add logs/ to .gitignore to prevent future commits
Reduction: -59 files
```

### 5B: Delete Old Test Runners (26 files)
```
Action: Delete all tests in archives
Files:
  - code/_archive/orphaned/*
  - code/_archive/phase_history/*
  - code/_archive/test_infrastructure/*
  - tests/_archived_test_versions/*
Time: 10 minutes
Risk: LOW - Active tests remain in /tests/ directory
Reduction: -26 files
```

### 5C: Delete Backup Files (7 files)
```
Action: Delete all *.bak files
Files: various *.bak files throughout project
Time: 2 minutes
Risk: NONE - Backup files have no purpose in repo
Reduction: -7 files
```

### 5D: Archive Old Archive Code (30 files)
```
Action: Move code/_archive/ folder to useless/code_archive
Files: All 30 files in code/_archive/
Time: 5 minutes
Risk: LOW - Keeping for historical reference but move out of active tree
Reduction: -30 files (logically, keeps in useless/)
```

### 5E: Delete Duplicate Consolidation Reports (4 files)
```
Action: Keep CONSOLIDATION_INDEX.md, delete others
Files:
  - CONSOLIDATION_COMPLETE_SUMMARY.md
  - CONSOLIDATION_SUMMARY.md
  - CONSOLIDATION_PLAN.md
  - (Keep 1 master reference)
Time: 5 minutes
Risk: LOW - Consolidation work already done, documented
Reduction: -4 files
```

### 5F: Archive Duplicate Documentation (70+ files)
```
Action: Move to useless/documentation/

Groups to archive:
  - Completion/Final reports (5 files)
  - Code audit duplicates (1 file - keep CODE_AUDIT_FULL_ANALYSIS.md)
  - Dashboard duplicates (4+ files - keep in MASTER_DASHBOARD.md)
  - Root-level duplicate guides (50+ files)
  - Archive documentation (47 files)

Time: 20-30 minutes (careful review needed)
Risk: MEDIUM - Need to verify no unique content lost
Reduction: -70+ files
```

**Total Quick Wins**: **~130-150 files** in **30-40 minutes**  
**Result**: 445 → 310-320 files (**30-35% immediate reduction**)

---

## PHASE 6: RECOMMENDED NEW PROJECT STRUCTURE

**Current**: Files scattered across multiple locations  
**Proposed**: Organized by domain and concern

```
geesp-angola/
│
├── README.md                        # Single comprehensive README
├── LICENSE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
├── setup.py
├── pyproject.toml
│
├── docs/                            # ESSENTIAL DOCUMENTATION ONLY
│   ├── 01_GETTING_STARTED.md       # Installation + quick start
│   ├── 02_ARCHITECTURE.md          # System design
│   ├── 03_DEVELOPMENT.md           # Dev guide + testing
│   ├── 04_OPERATIONS.md            # Production ops
│   └── api/                        # API reference if needed
│
├── src/                             # SOURCE CODE (MAIN REORGANIZATION)
│   ├── __init__.py
│   ├── main.py                     # Entry point
│   │
│   ├── core/                       # Core algorithm modules
│   │   ├── __init__.py
│   │   ├── mcda_analysis.py        # MCDA/AHP analysis
│   │   ├── lcoe_calculator.py      # LCOE calculations
│   │   └── aptitude_engine.py      # Map aptitude synthesis
│   │
│   ├── services/                   # Business logic layer
│   │   ├── __init__.py
│   │   ├── data_service.py         # Data loading/processing
│   │   ├── map_service.py          # Map generation
│   │   ├── api_service.py          # API handling
│   │   └── validation_service.py   # Validation pipeline
│   │
│   ├── utils/                      # UNIFIED UTILITIES (CONSOLIDATED)
│   │   ├── __init__.py
│   │   ├── core_utils.py           # Array/data utilities
│   │   ├── raster_utils.py         # Raster operations + unified normalization
│   │   ├── validation.py           # All validation functions
│   │   ├── constants.py            # Constants + configurations
│   │   ├── exceptions.py           # Custom exceptions
│   │   ├── logging.py              # Logging configuration
│   │   └── cache.py                # Caching utilities
│   │
│   ├── api/                        # API layer
│   │   ├── __init__.py
│   │   ├── router.py               # CONSOLIDATED API routes
│   │   ├── models.py               # API request/response models
│   │   └── middleware.py           # API middleware
│   │
│   ├── ui/                         # Streamlit UI components
│   │   ├── __init__.py
│   │   ├── app.py                  # Main Streamlit app
│   │   ├── pages/                  # Streamlit pages
│   │   ├── components/             # UI components
│   │   └── styles/                 # CSS/styling
│   │
│   ├── models/                     # Data models/entities
│   │   ├── __init__.py
│   │   ├── raster.py               # Raster data models
│   │   ├── analysis.py             # Analysis models
│   │   └── config.py               # Configuration models
│   │
│   └── config/                     # Configuration management
│       ├── __init__.py
│       ├── settings.py             # Settings loader
│       ├── env.py                  # Environment management
│       └── dev.py, prod.py         # Environment-specific configs
│
├── tests/                          # CONSOLIDATED TEST SUITE
│   ├── conftest.py
│   ├── test_core_modules.py        # Core algorithm tests
│   ├── test_services.py            # Service layer tests
│   ├── test_utils.py               # Utility tests
│   ├── test_api.py                 # API tests
│   ├── test_ui.py                  # UI tests
│   ├── test_integration.py         # Integration tests
│   ├── test_performance.py         # Performance tests
│   └── fixtures/                   # Test fixtures/mocks
│
├── scripts/                        # CONSOLIDATED SCRIPTS
│   ├── __init__.py
│   ├── build.py                    # Build automation
│   ├── deploy.py                   # Deployment automation
│   │
│   ├── data/                       # Data processing scripts
│   │   ├── __init__.py
│   │   ├── extract_gee_data.py    # GEE extraction
│   │   └── load_datasets.py        # Dataset loading
│   │
│   ├── maps/                       # Map generation scripts
│   │   ├── __init__.py
│   │   ├── generate.py             # Main map generator
│   │   ├── export_pdf.py           # PDF export
│   │   └── run_all.py              # Orchestrator
│   │
│   └── verify/                     # Verification scripts
│       ├── __init__.py
│       ├── check_setup.py
│       └── test_integration.py
│
├── config/                         # CONSOLIDATED CONFIG FILES
│   ├── app.json                    # Main config
│   ├── settings.toml               # Streamlit settings  
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.prod
│   │   └── docker-compose.yml
│   │
│   ├── ci/
│   │   ├── ci.yml
│   │   └── production-pipeline.yml
│   │
│   └── .env.example                # Example environment variables
│
├── data/                           # SAMPLE DATA & OUTPUTS
│   ├── raw/                        # Raw input data
│   ├── processed/                  # Processed outputs
│   └── exports/                    # Exported maps
│
├── useless/                        # ARCHIVED/OBSOLETE CODE
│   ├── documentation/              # Old documentation
│   ├── code_archive/               # Old code versions
│   ├── test_archive/               # Obsolete tests
│   ├── logs/                       # Generated log files
│   └── MANIFEST.md                 # What's here and why
│
└── .gitignore                      # Updated to include logs/
```

---

## PHASE 7: CONSOLIDATION MANIFEST

### Files to DELETE (143 files)

**Group 1: Log Files (59 files)**
- Location: logs/*.log
- Reason: Generated application outputs, not source code
- Risk: NONE (regenerable)
- Action: DELETE + Add logs/ to .gitignore

**Group 2: Archive Tests (26 files)**
- Location: code/_archive/*/test*.py, tests/_archived_test_versions/*
- Reason: Phase-specific obsolete tests
- Risk: LOW (active tests remain)
- Action: DELETE

**Group 3: Backup Files (7 files)**
- Location: Various *.bak files
- Reason: No purpose in version control
- Risk: NONE
- Action: DELETE

**Group 4: Consolidation Reports (4 files)**
- Files: CONSOLIDATION_SUMMARY.md, CONSOLIDATION_COMPLETE_SUMMARY.md, CONSOLIDATION_PLAN.md, CONSOLIDATION_INDEX.md (keep 1)
- Reason: Duplicates of same information
- Risk: LOW
- Action: DELETE (keep INDEX as reference)

**Group 5: Duplicate Documentation (47 files)**
- Location: code/_archive/ (old documentation)
- Reason: Superseded by MASTER guides
- Risk: MEDIUM (verify uniqueness)
- Action: ARCHIVE to useless/documentation/

---

### Files to CONSOLIDATE (100-120 files)

**Group 1: Utilities (5 → 3 files)**
- Consolidate: performance.py deprecated functions into raster_utils, map_utils
- Keep: core_utils, raster_utils, map_utils (refactored)
- Delete: scripts/utils.py (if exists)
- Refactor map_utils.compute_aptitude() to use raster_utils.normalize()

**Group 2: Documentation (78 root level → keep 8)**
- Keep: 8 MASTER guides (excellent quality)
- Archive: Duplicate guides, report duplicates, completion certificates
- Consolidate: Unique content from deleted files into MASTER guides

**Group 3: Tests (32 active → 15-18)**
- Consolidate: Similar test files (test_mcda1.py + test_mcda2.py → test_mcda.py)
- Keep: Essential test coverage
- Delete: Redundant/duplicate test cases
- Organize: Logical grouping by domain (core, services, utils, api, ui, integration)

**Group 4: Scripts (15 → 8-10)**
- Consolidate: Map generation (remove simple version if redundant)
- Consolidate: PDF generation (one unified function)
- Keep: Orchestrators (run_all_maps.py)
- Organize: scripts/maps/, scripts/data/, scripts/verify/

**Group 5: Configuration (17 → 10)**
- Consolidate: Environment-specific configs using .env pattern
- Merge: docker-compose variants using profiles
- Merge: Dockerfile variants using build args
- Result: Fewer base files, configuration via environment variables

---

### Files to MOVE to useless/ (77 files)

**Group 1: Archive Code (30 files)**
- Location: code/_archive/ (all files)
- Where: useless/code_archive/
- Reason: Old versions of code, obsolete implementations, historical

**Group 2: Old Documentation (47 files)**
- Location: code/_archive/ (all .md files), duplicates at root
- Where: useless/documentation/
- Reason: Superseded by MASTER guides, obsolete information

---

### Files to KEEP (250-280 files)

**Core Application Code** (~80 files)
- Main entry point (app.py, main.py)
- Core algorithms (mcda_analysis.py, lcoe_calculator.py)
- Services (data_loaders, map_generators, API handlers)
- UI components (Streamlit pages, components)

**Essential Utilities** (~30 files)
- core_utils.py, raster_utils.py, map_utils.py
- validation.py, constants.py, exceptions.py
- logging.py, cache utilities

**Active API & Services** (~20 files)
- API router, models, middleware
- Data services
- Map services
- Validation

**Tests** (~18-20 files)
- Logical test modules
- Fixtures and mocks
- Configuration

**Scripts** (~10-12 files)
- Build, deploy, verification
- Data extraction
- Map generation and orchestration

**Configuration** (~10-12 files)
- APP config (app.json, settings.toml)
- Docker configs (1 Dockerfile + 1 docker-compose with profiles)
- CI/CD config
- Environment files

**Documentation** (~8-10 files)
- 8 MASTER guides
- README, LICENSE, CONTRIBUTING, CHANGELOG

**Other** (~50-60 files)
- IDE configs (.vscode, .editorconfig)
- Development tools (.pre-commit-config, .bandit)
- Static data and fixtures
- License, makefile, etc.

---

## PHASE 8: IMPACT ANALYSIS & RISK ASSESSMENT

### Benefits of Consolidation

| Benefit | Impact | Confidence |
|---------|--------|------------|
| **Reduced Repository Size** | 60 MB → 35-40 MB | HIGH |
| **Easier Navigation** | Find code faster, clearer structure | HIGH |
| **Reduced Maintenance** | Less duplicate code to maintain | MEDIUM |
| **Improved Consistency** | Single implementations of patterns | MEDIUM |
| **Easier Onboarding** | New devs understand structure faster | HIGH |
| **Better Testing** | Consolidated test suite easier to manage | MEDIUM |
| **Faster Builds** | Fewer files to process | LOW |

### Risks & Mitigations

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| **Deleted code is needed later** | LOW | Keep useless/ folder for 1+ release; Version control history remains |
| **Consolidation breaks imports** | MEDIUM | Update all imports systematically, test thoroughly |
| **Duplicate code diverges** | MEDIUM | Each consolidation includes test that exercises all original code paths |
| **Console breaks on merge** | LOW | Test after every consolidation milestone |
| **Lost functionality in docs** | MEDIUM | Cross-check MASTER guides contain all unique information |

### Rollback Strategy

If critical issues found:
1. Useless/ folder contains all deleted files (can be restored)
2. Git history contains all original files
3. No build artifacts affected
4. Test suite can verify correctness

---

## PHASE 9: EXECUTION TIMELINE

### Phase 5A: Quick Wins (30 minutes) - ZERO RISK
- Delete log files (5 min)
- Delete archive tests (10 min)
- Delete backup files (2 min)
- Delete consolidation reports (5 min)
- Archive old code (8 min)
- Result: -110 files

### Phase 5B: Medium Consolidations (2-3 hours) - MEDIUM EFFORT
- Refactor map_utils (consolidate with raster_utils) - 30 min
- Consolidate tests into 15 files - 45 min
- Consolidate documentation (archive old, keep MASTER) - 45 min
- Consolidate scripts - 30 min
- Consolidate configuration - 30 min
- Result: -80-100 files

### Phase 6: Structure Reorganization (1-2 hours) - CAREFUL
- Create src/ directory structure - 15 min
- Move/reorganize source files - 30 min
- Update all imports - 30 min
- Move config to config/ - 15 min
- Move scripts to scripts/subdirs - 15 min
- Result: 0 file change (just organization)

### Phase 8-10: Verification & Testing (1-2 hours) - CRITICAL
- Run full test suite - 15 min
- Run syntax checker on all Python files - 5 min
- Verify imports work - 10 min
- Test application startup - 10 min
- Verify documentation renders - 5 min
- Generate final metrics - 10 min

**Total Time Estimate: 5-7 hours spread over multiple days**

---

## PHASE 10: FINAL DELIVERABLES

### Report 1: Consolidation Summary
- Before/after file count
- Consolidation actions taken
- Impact metrics
- Rollback information

### Report 2: New Structure Documentation
- Project tree diagram
- Module descriptions
- Import patterns
- Development guidelines

### Report 3: Prevention Recommendations
- Pre-commit hooks to prevent log commits
- Periodic code review process
- Documentation standards
- Configuration management approach

---

## RECOMMENDATIONS SUMMARY

✅ **Implement Quick Wins (Phase 5A)**
- Zero risk, significant impact
- 30 minutes of work
- Removes 110+ files

✅ **Consolidate High-Impact Groups**
- Utilities (normalization)
- Tests (reduce from 58 → 18)
- Documentation (reduce from 138 → 8)

🔄 **Consider Structure Reorganization**
- More organized codebase
- Easier to scale
- Better for team development

---

**Status**: ✅ **Phases 4-10 Strategy Complete**  
**Next Step**: User Review & Approval for Execution

