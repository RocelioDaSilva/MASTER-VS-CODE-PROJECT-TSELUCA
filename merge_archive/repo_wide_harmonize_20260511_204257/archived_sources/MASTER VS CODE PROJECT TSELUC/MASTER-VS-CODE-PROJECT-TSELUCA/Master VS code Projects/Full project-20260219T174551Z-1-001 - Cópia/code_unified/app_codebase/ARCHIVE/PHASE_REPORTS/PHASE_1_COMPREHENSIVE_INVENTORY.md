# PHASE 1: COMPREHENSIVE FILE INVENTORY & FUNCTIONAL CLASSIFICATION
**Codebase Consolidation Project for GEESP-Angola**  
**Date**: March 6, 2026  
**Focus**: 02_Code folder only (NOT 01_Science)

---

## EXECUTIVE SUMMARY

### Baseline Metrics
- **Total Files**: 445 (excluding caches, venv, build artifacts)
- **Total Directories**: 57
- **Total Size**: 60.06 MB
- **Primary Language**: Python (162 files)
- **File Types**: 25 different extensions

### Current State Assessment
The codebase exhibits significant bloat and redundancy:

**🔴 CRITICAL BLOAT** (Remove immediately):
- 66 Reports/Log files - **Generated data, not source code**
- 59 .log files - Should be .gitignored
- Multiple backup files (.bak)

**🔴 EXCESSIVE DOCUMENTATION** (Consolidate 80-90%):
- 143 markdown files - Far exceeds healthy project needs
- Many duplicate guides, tutorials, README files scattered across directories
- Multiple master guides covering same topics

**🟡 CODE FRAGMENTATION** (Reorganize):
- 74 Python core files scattered across multiple directories
- 58 test files with many archaeological artifacts in archive
- 30 build/deployment scripts in fragmented locations
- Multiple utility files with overlapping functionality

**🟠 Configuration Spread**:
- 17 configuration files across multiple formats and locations
- Potential for consolidation using environment variables

---

## DETAILED FILE INVENTORY

### Category 1: DOCUMENTATION (143 files) - 🔴 PRIORITY 1

**Current State**: Far too many files  
**Target**: **20-30 consolidated files** (80% reduction)  
**Status**: EXCESSIVE

#### Key Documentation Files (First 20):
```
01_MASTER_GETTING_STARTED.md       # Master guide 1
02_MASTER_ARCHITECTURE.md          # Master guide 2
03_MASTER_IMPLEMENTATION.md        # Master guide 3
04_MASTER_PRODUCTION.md            # Master guide 4
05_MASTER_TESTING_QA.md            # Master guide 5
06_MASTER_DEVELOPMENT.md           # Master guide 6
07_MASTER_DASHBOARD.md             # Master guide 7
08_MASTER_ADVANCED.md              # Master guide 8
API_RESPONSE_CACHING_GUIDE.md
AUDIT_REPORT.md
BUILD_WINDOWS_APP_QUICK.md
...and 131 more
```

#### Analysis:
- **8 "MASTER" guides** - These appear to be from previous consolidation attempt
- **137 additional .md files** - Scattered across directories and archive
- **Redundancy Hypothesis**: Multiple versions of same guides (e.g., MASTER_ARCHITECTURE.md vs architecture docs in subdirectories)
- **Likelihood of Consolidation**: **85-90%** These can be merged into 3-5 comprehensive guides at root level

#### Sub-Categories:
- **API Documentation**: Multiple API guide files
- **Installation/Setup**: Setup guides repeated multiple times
- **Architecture Guides**: Multiple architecture explanation files
- **Development Guides**: Setup, contribution, development guides repeated
- **Archived Documentation**: Many old versions in various locations

**PHASE 2 ACTION**: Need to compare all .md files for content overlap

---

### Category 2: PYTHON CORE CODE (74 files) - 🟡 PRIORITY 2

**Current State**: Scattered across multiple locations  
**Target**: **Single organized location with 40-50 files**  
**Status**: FRAGMENTED

#### Key Files:
```
CODING_STANDARDS.py                # Code style reference (archive?)
DEVELOPER_GUIDE.py                 # Development guide (archive or docs?)
INFRASTRUCTURE_SUMMARY.py          # Architecture reference
MODULE_ARCHITECTURE.py             # Architecture reference
SETUP_WIZARD.py                    # Setup utility
... 69 more
```

#### Issues Identified:
1. **Multiple copies in different locations** (core/ vs scripts/ vs code/_archive/)
2. **Utility files scattered** (core_utils.py, map_utils.py, raster_utils.py, performance.py)
3. **Model files in multiple places** (models/ and individual files)
4. **Some files appear to be reference/documentation** disguised as Python (CODING_STANDARDS.py, DEVELOPER_GUIDE.py)

**PHASE 2 ACTION**: Classify each file by purpose (core vs utility vs archive vs docs-as-code)

---

### Category 3: REPORTS & LOGS (66 files) - 🔴 PRIORITY 1

**Current State**: In repository  
**Target**: **NONE - delete all** (100% reduction)  
**Status**: SHOULD NOT BE IN REPO

#### Files:
```
logs/config_loader.log              # Generated logs
logs/config_loader_errors.log       
logs/data_loaders_async.log
... 56 more log files

data/processed/mapa_aptidao_integrada.pdf   # Generated reports
data/processed/mapa_aptidao_integrada.npy   # Generated data
... various map outputs
```

#### Recommendation:
All `.log` files and generated report files should be:
1. **Added to `.gitignore`** immediately
2. **Moved to useless/ folder** for archival
3. **Never committed to repo** again

These are **generated outputs** of the application, not source code.

**PHASE 5 ACTION**: Move all 66 files to useless/

---

### Category 4: PYTHON TESTS (58 files) - 🟡 PRIORITY 2

**Current State**: Scattered across main and archive directories  
**Target**: **Single tests/ directory with 15-20 files**  
**Status**: DUPLICATED & FRAGMENTED

#### Key Test Files:
```
run_tests.py                        # Main test runner
test_*.py (multiple)                # Unit tests scattered
...in code/_archive/:
  code\_archive\test_infrastructure\final_test_run.py
  code\_archive\test_infrastructure\test_app.py
  code\_archive\phase_history\phase3a_test_runner.py
  ... many old test runners
```

#### Issues:
1. **Old test runners** in archive (phase3a_test_runner.py, etc.) - likely obsolete
2. **Multiple test infrastructure files** with similar names
3. **Test files not organized** in single /tests directory
4. **Possible duplicate test coverage**

**PHASE 2 ACTION**: Identify which tests are current vs archived duplicates

---

### Category 5: PYTHON SCRIPTS (30 files) - 🟡 PRIORITY 3

**Current State**: Scattered across scripts/ and archive/  
**Target**: **Single scripts/ directory with 10-12 organized files**  
**Status**: PARTIALLY ORGANIZED

#### Key Scripts:
```
build_windows_app.py
scripts/api/api.py
scripts/api/api_server.py
... in archive:
  code\_archive\build_and_verification\verify_*.py (multiple)
  code\_archive\build_and_verification\launch_*.bat (multiple)
```

#### Issues:
1. **Verification scripts** scattered across multiple files
2. **Multiple launch/build scripts** with similar purposes
3. **Archive has old versions** that may be duplicates

**PHASE 2 ACTION**: Consolidate verification scripts into single verification suite

---

### Category 6: CONFIGURATION (17 files) - 🟠 PRIORITY 4

**Current State**: Multiple formats and locations  
**Target**: **Consolidated config system, 8-10 files**  
**Status**: MANAGEABLE but can improve

#### Files:
```
.github/workflows/ci.yml            # CI/CD config
.github/workflows/production-pipeline.yml
.pre-commit-config.yaml             # Pre-commit hooks
.streamlit/config.toml              # Streamlit config
.vscode/settings.json               # VS Code settings
config.json                         # App config
docker-compose*.yml (multiple)      # Docker configs
Dockerfile (multiple)               # Container configs
```

#### Opportunities:
1. **Environment variable system** - Move secrets/env-specific settings to .env file
2. **Consolidate docker-compose files** - Use profiles or separate services
3. **Centralize app configuration** - Single config.json with environments

**PHASE 2 ACTION**: Review for consolidation using environment variables

---

### Category 7: BUILD/DEPLOYMENT (16 files) - 🟡 PRIORITY 3

**Current State**: Scattered across root, archives, and subdirectories  
**Target**: **Single build/ directory with 5-8 files**  
**Status**: FRAGMENTED

#### Files:
```
BUILD.bat                           # Windows build script
Dockerfile
Dockerfile.app / Dockerfile.root    # Multiple container configs
... in archive:
  build_and_verification/launch_api_server.bat
  build_and_verification/launch_app.bat
  build_and_verification/run_dashboard.bat/.sh
```

#### Issues:
1. **Multiple .bat files** for similar tasks
2. **Duplicate Dockerfiles** in different locations
3. **Shell scripts scattered**

**PHASE 2 ACTION**: Consolidate build system into single Makefile or build.py

---

### Category 8: ASSETS & DATA (19 files) - 🟠 PRIORITY 4

**Current State**: Generated outputs in data/ directory  
**Target**: **Keep structure, archive unused outputs**  
**Status**: MANAGEABLE

#### Files:
```
data/processed/mapa_*.npy          # Generated numpy arrays
data/processed/mapa_*.png          # Generated images
data/processed/mapa_*.tif          # Generated GIS rasters
...and metadata JSON files
```

#### Note:
These are **generated outputs**, but keeping them for demonstration is reasonable if space allows. Can be .gitignored if regenerable.

---

### Category 9: OTHER (22 files) - 🟠 PRIORITY 5

**Current State**: Mixed files at root  
**Target**: **Organize into appropriate directories, 12-15 files**  
**Status**: NEEDS ORGANIZATION

#### Files:
```
.bandit                             # Linting config
.editorconfig                       # Editor config
.env.example                        # Example env file
.gitignore                          # Git ignore
CODEOWNERS                          # GitHub ownership
LICENSE                             # License file
Makefile                            # Build automation
README.md                           # Documentation
requirements.txt                   # Dependencies
setup.py                            # Package setup
... more config files
```

#### Note:
Most of these should remain at root. Some can be consolidated.

---

## CONSOLIDATION OPPORTUNITY ANALYSIS

### Quick Wins (Implement First)

| Action | Files Affected | Reduction | Effort | Impact |
|--------|----------------|-----------|--------|--------|
| **Delete logs/ folder** | 59 files | -59 | 5 min | HIGH |
| **Delete obsolete reports** | 6+ PDF files | -6 | 5 min | MEDIUM |
| **Add logs/ to .gitignore** | - | - | 1 min | HIGH |
| **Archive old test runners** | 15+ files | -15 | 10 min | MEDIUM |
| **Archive old build scripts** | 8+ files | -8 | 10 min | MEDIUM |

### Medium-Difficulty (Phase 2-3)

| Action | Files Affected | Reduction | Effort | Impact |
|--------|----------------|-----------|--------|--------|
| **Consolidate documentation** | 143 → 25 | -118 | 2-3 hrs | CRITICAL |
| **Merge duplicate utilities** | 5+ files | -2 | 1 hr | HIGH |
| **Unify build system** | 16 → 5 | -11 | 1 hr | MEDIUM |
| **Consolidate config files** | 17 → 10 | -7 | 1 hr | MEDIUM |

### Projected Results

**Before**: 445 files  
**After Aggressive Consolidation**: ~250 files  
**Reduction**: **44%**

**Realistic Conservative Estimate**: ~290 files  
**Reduction**: **35%**

---

## CRITICAL FINDINGS

### Finding 1: Documentation Explosion
The 143 markdown files represent **previous consolidation attempts** that created MORE files instead of fewer. 8 "MASTER" guides suggest someone tried to consolidate but left all old files in place.

**Recommendation**: Delete all old documentation files and keep only the 8 MASTER guides (or consolidate those further into 3-5).

### Finding 2: Generated Data in Repository
66 log and report files should never have been committed. This suggests:
- No `.gitignore` was used during development
- Generated data was manually committed
- Repository has unnecessary bloat

**Recommendation**: Add to `.gitignore` immediately, delete from repo.

### Finding 3: Code Archive Structure
The `code/_archive/` folder contains significant amounts of old code:
- Entry points (4 old versions)
- Test runners (multiple old versions)
- Build scripts (multiple old versions)
- Orphaned code

**Recommendation**: Review and keep only 1 entry point, archive rest properly.

### Finding 4: Scattered Utilities
Multiple utility files in different locations:
- scripts/core_utils.py
- scripts/map_utils.py
- scripts/raster_utils.py
- scripts/performance.py

**Recommendation**: Phase 2 must analyze these for consolidation or clear separation of concerns.

### Finding 5: Missing Organization
No clear src/ → models/ → services/ → utils/ structure. Files are scattered at root and in many locations.

**Recommendation**: Phase 6 will design new structure: `src/core/`, `src/services/`, `src/utils/`, `src/api/`, etc.

---

## RECOMMENDATIONS FOR PHASE 2

1. ✅ **Analyze documentation files** for content duplication
2. ✅ **Identify duplicate Python utility functions** across files
3. ✅ **Map test file purposes** - current vs obsolete
4. ✅ **Audit configuration files** for consolidation opportunities
5. ✅ **List all archive files** asreason for archival

---

## PHASE 1 SUMMARY

- **Files Analyzed**: 445
- **Categories Identified**: 9
- **Consolidation Opportunities**: 7 major groups
- **Quick Win Deletions**: ~130 files (logs, old tests, old scripts, old reports)
- **Consolidation Targets**: Documentation (143→25), Core Code (74→50), Scripts (30→12)
- **Estimated Final Count**: 250-290 files (44-35% reduction)

**Status**: ✅ **PHASE 1 COMPLETE** - Ready for Phase 2
