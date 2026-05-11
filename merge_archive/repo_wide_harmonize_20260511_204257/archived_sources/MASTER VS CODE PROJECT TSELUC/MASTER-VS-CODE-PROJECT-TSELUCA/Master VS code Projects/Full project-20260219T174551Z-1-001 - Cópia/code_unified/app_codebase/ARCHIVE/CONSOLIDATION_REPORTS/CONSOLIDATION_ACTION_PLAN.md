# 02_Code Consolidation Action Plan
## Based on Comprehensive Code Audit - March 7, 2026

---

## ✅ COMPLETED PHASES

### PHASE 1: Archive Cleanup ✓ COMPLETE
- **Status**: DONE
- **Deleted**: `code/_archive/` directory (39 files, 6,084 lines)
- **Files Deleted**: 
  - `orphaned/database_integration.py` (663 lines)
  - `validation/validators.py` (601 lines)
  - `utilities/utils_from_scripts.py` (536 lines)
  - `orphaned/k8s_metrics.py` (463 lines)
  - `orphaned/cog_generator.py` (456 lines)
  - `utilities/config_utilities.py` (334 lines)
  - `entry_points/` directory (400 lines)
  - `test_infrastructure/` directory (600 lines)
  - `phase_history/` directory (800 lines)
  - Plus 20+ other obsolete files
- **Impact**: Eliminated 17.5% of codebase (dead code)
- **Risk**: LOW (all code was already archived)

---

## 🔄 IN-PROGRESS PHASES

### PHASE 2: Utility Consolidation (Starting)
**Goal**: Consolidate scattered utility modules into central `utils/` location

**Current Scattered Utilities:**
- `geesp-angola/scripts/core_utils.py` (399 lines)
- `geesp-angola/dashboard/utils/helpers.py` (247 lines)
- `geesp-angola/dashboard/utils/validators_ui.py` (88 lines)
- `geesp-angola/dashboard/utils/cache_manager.py` (173 lines)
- `geesp-angola/dashboard/utils/session_state.py` (156 lines)
- `geesp-angola/dashboard/utils/page_router.py` (142 lines)

**Canonical Utils Location** (already exists):
- `geesp-angola/utils/constants.py` (882 lines) ✓
- `geesp-angola/utils/validation.py` (465 lines) ✓
- `geesp-angola/utils/data_processing.py` (489 lines) ✓
- `geesp-angola/utils/config_manager.py` (389 lines) ✓
- `geesp-angola/utils/logging_config.py` (247 lines) ✓
- `geesp-angola/utils/import_helpers.py` (156 lines) ✓
- `geesp-angola/utils/exceptions.py` (118 lines) ✓

**Consolidation Actions:**
1. ✓ Move non-UI functions from `scripts/core_utils.py` → `utils/core_utils.py` (NEW)
2. ✓ Move non-Streamlit helpers from `dashboard/utils/helpers.py` → `utils/helpers.py` (NEW)
3. ✓ Keep UI-specific: `dashboard/utils/cache_manager.py`, `session_state.py`, `page_router.py`
4. ✓ Consolidate validators: Move validator utilities to `utils/validators.py` (NEW)
5. ✓ Update all imports to use central location
6. ✓ Remove duplicate/empty dashboard utils

**Expected Recovery**: 200-300 lines (deduplication)
**Effort**: 4-5 hours
**Status**: QUEUED

---

### PHASE 3: Test Organization (Starting)
**Goal**: Organize scattered tests into unit/integration/e2e structure

**Current Test Files** (14 files scattered across):
- `tests/test_database_models.py`
- `tests/test_mcda_analysis.py`
- `tests/test_consolidation.py`
- And 11 others with inconsistent naming/organization

**Proposed Structure:**
```
tests/
├── unit/                          # Unit tests for individual modules
│   ├── test_constants.py
│   ├── test_validation.py
│   ├── test_data_processing.py
│   ├── test_config_manager.py
│   └── test_exceptions.py
├── integration/                   # Integration tests for subsystems
│   ├── test_api_endpoints.py
│   ├── test_dashboard_pages.py
│   ├── test_gee_integration.py
│   ├── test_mcda_analysis.py
│   ├── test_lcoe_calculator.py
│   └── test_database_integration.py
├── e2e/                          # End-to-end workflow tests
│   ├── test_full_analysis_workflow.py
│   ├── test_scenario_generation.py
│   └── test_map_generation.py
└── conftest.py                   # Shared fixtures and configuration
```

**Actions:**
1. ✓ Create directory structure: `tests/{unit|integration|e2e}/`
2. ✓ Move existing tests to appropriate directories
3. ✓ Create consolidated `tests/conftest.py` with shared fixtures
4. ✓ Remove duplicate test utilities from individual files
5. ✓ Update pytest configuration

**Expected Organization**: 
- Clear separation of concerns
- Easier to locate and maintain tests
- Shared fixtures in one place

**Effort**: 3-4 hours
**Status**: QUEUED

---

### PHASE 4: API Consolidation (Starting)
**Goal**: Consolidate API modules into single FastAPI application

**Current API Structure:**
- `geesp-angola/scripts/api/api.py` (510 lines) - Main API
- `geesp-angola/scripts/api/batch_mcda_api.py` (488 lines) - Batch processing
- `nevermindu/server.ts` (536 lines) - Express.js backend (keep separate)

**Audit Finding**: "Can be consolidated by merging batch processing as routes in main API"

**Consolidation Plan:**
1. ✓ Review `batch_mcda_api.py` - extract batch job processing logic
2. ✓ Add batch endpoints as FastAPI routes in `api.py`
3. ✓ Convert batch job models to Pydantic models
4. ✓ Consolidate dependencies and imports
5. ✓ Delete `batch_mcda_api.py` after consolidation

**Code Integration Points:**
- BatchJobConstants → Move to utils/constants.py
- BatchJobStatus dataclass → Convert to Pydantic BaseModel
- Async job processing → Add to main API router
- Job storage/tracking → Consolidate in API state

**Expected Recovery**: 100-150 lines (consolidated)
**Effort**: 2-3 hours
**Status**: QUEUED

---

## 📋 PLANNED PHASES (Future)

### PHASE 5: Folder Structure Reorganization (8-12 hours)
**Goal**: Restructure folder layout for clarity and scalability

**Proposed New Structure:**
```
02_Code/
├── backend/                       # Python backend services
│   ├── core/                      # Core analysis engines
│   │   ├── mcda_analysis.py
│   │   ├── lcoe_calculator.py
│   │   └── performance.py
│   ├── gee/                       # Google Earth Engine integration
│   │   ├── earth_engine_integration.py
│   │   ├── data_loaders_async.py
│   │   ├── raster_utils.py
│   │   └── map_utils.py
│   ├── api/                       # REST API (FastAPI)
│   │   ├── api.py (consolidated)
│   │   ├── routes/
│   │   └── models/
│   ├── dashboard/                 # Streamlit dashboard
│   │   ├── app.py
│   │   ├── pages/
│   │   ├── components/
│   │   └── utils/
│   ├── models/                    # Data models (SQLAlchemy/ORM)
│   │   └── monitoring.py
│   └── utils/                     # Shared utilities (CONSOLIDATED)
│       ├── constants.py
│       ├── config_manager.py
│       ├── validation.py
│       ├── data_processing.py
│       ├── logging_config.py
│       ├── exceptions.py
│       ├── core_utils.py (NEW - moved from scripts/)
│       ├── helpers.py (NEW - moved from dashboard/)
│       └── __init__.py
├── frontend/                      # React/TypeScript frontend
│   └── nevermindu/
│       ├── src/
│       ├── package.json
│       └── ...
├── tests/                         # Organized test suite
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── conftest.py
├── docs/                          # Documentation (consolidated)
│   ├── guides/
│   ├── api/
│   └── architecture/
├── config/                        # Configuration files
│   ├── docker-compose.yml
│   ├── kubernetes/
│   └── ...
└── ...
```

**Benefits:**
- Clear backend/frontend separation ✓
- All utilities in one consolidated location ✓
- Tests organized by scope ✓
- Configuration centralized ✓
- Easier onboarding for new developers ✓
- Improved discoverability ✓

**Status**: PLANNING

---

### PHASE 6: Documentation Updates (2-3 hours)
**Goal**: Update documentation to reflect consolidations

**Actions:**
1. Update import statements in README
2. Update architecture documentation
3. Update contribution guidelines
4. Create migration guide for developers
5. Update API documentation (Swagger)

**Status**: PLANNING

---

## 📊 CONSOLIDATION IMPACT SUMMARY

### Code Metrics
| Metric | Before | After | Recovery |
|--------|--------|-------|----------|
| Total Files | 159 | ~145-150 | 9-14 |
| Total Lines | 34,825 | 28,600+ | 6,200+ |
| Archive/Dead | 39 files (6,084 lines) | 0 | 6,084 ✓ |
| Utilities Scattered | 16 files | 1 location | Unified ✓ |
| Tests Organized | Scattered (14) | Structured | Organized ✓ |
| Duplicate Code | 25-30% utilities | <10% | Reduced ✓ |

### File Changes
- **Files Deleted**: 40-50 (archive + duplicates)
- **Files Modified**: 20-30 (import updates)
- **Files Created**: 3-5 (new consolidated modules)
- **Files Moved**: 10-15 (reorganization)

### Time Investment
| Phase | Effort | Status |
|-------|--------|--------|
| Phase 1: Archive Cleanup | 2-3 hrs | ✓ COMPLETE |
| Phase 2: Utility Consolidation | 4-5 hrs | 🔄 READY |
| Phase 3: Test Organization | 3-4 hrs | 🔄 READY |
| Phase 4: API Consolidation | 2-3 hrs | 🔄 READY |
| Phase 5: Folder Restructuring | 8-12 hrs | 📋 PLANNED |
| Phase 6: Documentation | 2-3 hrs | 📋 PLANNED |
| **TOTAL** | **21-30 hrs** | **75% IN QUEUE** |

---

## 🎯 NEXT IMMEDIATE ACTIONS

### For Next Session:
1. **Execute PHASE 2**: Utility consolidation (4-5 hours)
   - Move `scripts/core_utils.py` non-UI functions to `utils/`
   - Move `dashboard/utils/helpers.py` non-UI functions to `utils/`
   - Create consolidated utilities module
   - Update all imports

2. **Execute PHASE 3**: Test organization (3-4 hours)
   - Create test directory structure
   - Move tests to appropriate folders
   - Create consolidated conftest.py
   - Verify test discovery

3. **Execute PHASE 4**: API consolidation (2-3 hours)
   - Merge batch_mcda_api.py into api.py
   - Consolidate constants and models
   - Delete batch_mcda_api.py
   - Test API endpoints

---

## 🔒 SAFETY & ROLLBACK

**Completed Actions:**
- ✓ Archive cleanup already verified (no imports found)
- ✓ No dependencies on deleted files

**Rollback Plan for Future Phases:**
1. All changes committed to git
2. Branches created before major restructuring
3. Tests run before and after each phase
4. Imports verified before file deletion

---

## 📈 SUCCESS CRITERIA

✓ **PHASE 1**: 6,084 lines of dead code removed
- Verified no imports from archive
- Reduced codebase complexity

🔄 **PHASE 2**: Utilities consolidated into single location
- Single import path for all utilities
- Reduced scattered helper functions
- Improved code discoverability

🔄 **PHASE 3**: Tests organized by scope
- Clear unit/integration/e2e separation
- Unified test fixtures
- Easier test maintenance

🔄 **PHASE 4**: API consolidated
- Single FastAPI application
- Batch processing as standard routes
- Reduced API module complexity

📋 **PHASE 5**: Folder structure reflects architecture
- Backend/frontend clearly separated
- All utilities in one place
- Easy for new developers to understand

📋 **PHASE 6**: Documentation reflects changes
- Updated all references
- Migration guide for developers
- API docs current

---

## 📞 AUDIT SUMMARY STATISTICS

**Total Code Analyzed**: 159 files | 34,825 lines | 7 languages

**Systems Identified**: 10 distinct systems
- ✅ Frontend (React/TypeScript): 23 files, 10,156 lines
- ✅ Backend (Python): 54 files, 13,606 lines
- ✅ Dashboard (Streamlit): 13 files, 1,486 lines
- ✅ API (FastAPI): 3 files, 1,148 lines
- ✅ GEE Integration: 13 files, 4,071 lines
- ✅ Analysis Engines: 4 files, 1,450 lines
- ✅ Maps/Visualization: 3 files, 1,141 lines
- ⚠️ Tests: 14 files, 1,258 lines (needs organization)
- ✅ Core Utilities: 9 files, 3,246 lines (needs consolidation)
- ❌ Archive: 39 files, 6,084 lines (DELETED ✓)

**Consolidation Opportunities**: 6,200+ lines
**Estimated Time to Complete All**: 21-30 hours
**Current Progress**: Phase 1 of 6 (17%)

---

**Created**: March 7, 2026  
**Last Updated**: March 7, 2026  
**Prepared By**: Comprehensive Code Audit System  
**Status**: Action Plan Ready for Execution  

