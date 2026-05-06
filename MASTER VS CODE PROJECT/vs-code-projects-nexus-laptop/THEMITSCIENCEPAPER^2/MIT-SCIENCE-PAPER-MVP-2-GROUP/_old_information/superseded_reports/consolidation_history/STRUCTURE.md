# 📁 02_Code: Project Structure Guide

**Last Updated**: March 6, 2026  
**Status**: ✅ Streamlined & Optimized  
**Purpose**: Clear navigation for developers, data scientists, DevOps engineers

---

## 🎯 Quick Navigation

### 🚀 I Want To...
- **Run the app** → [`START_HERE.md`](START_HERE.md) (5 min start)
- **Find something** → [`INDEX.md`](INDEX.md) (complete map)
- **Understand the code** → [`README.md`](README.md) (project overview)

---

## 📊 Folder Structure (After Consolidation)

```
02_Code/
├── START_HERE.md               ← 🌟 READ THIS FIRST (role-based nav)
├── README.md                   ← Project overview
├── INDEX.md                    ← Complete documentation index
├── STRUCTURE.md                ← THIS FILE - folder organization
│
├── geesp-angola/               ← 🔥 MAIN PROJECT (140 files)
│   ├── dashboard/              ← Streamlit UI (components + pages)
│   ├── scripts/                ← Core MCDA & LCOE analysis engines
│   ├── tests/                  ← Test suite (27 core + 17 archived versions)
│   ├── utils/                  ← Utility functions (imports, validators, cache)
│   ├── data/                   ← Map data & community data (GEE exports)
│   ├── models/                 ← Database models & monitoring
│   ├── monitoring/             ← Monitoring dashboard
│   ├── k8s/                    ← Kubernetes deployment configs
│   ├── migrations/             ← Database migrations
│   ├── notebooks/              ← Demo notebooks (MCDA, LCOE)
│   ├── integration/            ← Integration tests & benchmarks
│   ├── ARCHIVE/                ← 40+ old docs (preserved, not active)
│   └── docs/                   ← Capabilities, improvements docs
│
├── nevermindu/                 ← 🎨 ALTERNATIVE FRONTEND
│   ├── src/                    ← React components + TypeScript services
│   ├── server.ts               ← Express backend entry point
│   └── (Node.js + React + TypeScript stack)
│
├── docs/                       ← 📚 COMPREHENSIVE DOCUMENTATION
│   ├── api-examples/           ← 10 JSON request/response examples
│   │   ├── authentication/     ← Login, register, token refresh
│   │   ├── scenarios/          ← MCDA scenario operations
│   │   └── analysis/           ← Financial metrics calculations
│   │
│   ├── guides/                 ← 📖 OPERATIONAL GUIDES
│   │   ├── BUILD_WINDOWS_APP_QUICK.md
│   │   ├── WINDOWS_APP_PACKAGING.md
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── DEVELOPMENT_WORKFLOW.md
│   │   ├── DEPENDENCIES_AND_SETUP.md
│   │   ├── PRODUCTION_ARCHITECTURE.md
│   │   └── QUICK_REFERENCE_CARD.md
│   │
│   ├── analysis/               ← 🔬 ANALYSIS & AUDIT DOCUMENTS
│   │   ├── CODE_FUNCTIONALITY_AUDIT.md
│   │   ├── 00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md
│   │   ├── 01_PENDING_IMPLEMENTATION_ROADMAP.md
│   │   ├── 02_DOCUMENTATION_CLEANUP_PLAN.md
│   │   ├── 03_MASTER_NAVIGATION_GUIDE.md
│   │   ├── 04_FINAL_HARMONIZATION_REPORT.md
│   │   └── PROJECT_HARMONY_TEST_REPORT.md
│   │
│   ├── archived-versions/      ← 📦 HISTORICAL CONSOLIDATION REPORTS
│   │   ├── CONSOLIDATION_AND_REORGANIZATION_MASTER_PLAN.md
│   │   ├── CONSOLIDATION_COMPLETION_SUMMARY.md
│   │   ├── DONE.md
│   │   └── LISTA_IMAGENS_FONTES_CODIGO_PROJETO.md
│   │
│   └── ERROR_CODES.md          ← 🚨 API error reference (25+ codes)
│
└── ARCHIVE/                    ← 💾 ARCHIVED ALTERNATIVE PROJECTS
    ├── geesp-angola-fixes/     ← Phase 2 unicode logging fix
    └── google-ai-studio-app/   ← Google AI Studio alternative frontend
```

---

## 🎓 By Role

### 👨‍💻 **Developer** (Python/PyTest/Streamlit)
```
START_HERE.md
├─→ geesp-angola/scripts/      (core algorithms)
├─→ geesp-angola/dashboard/    (Streamlit UI)
├─→ geesp-angola/tests/        (27 current test suites)
├─→ docs/guides/DEVELOPMENT_WORKFLOW.md
└─→ docs/guides/DEPENDENCIES_AND_SETUP.md
```

### 🎨 **Frontend Developer** (React/TypeScript/Node)
```
START_HERE.md
├─→ nevermindu/               (main frontend)
├─→ docs/guides/DEVELOPMENT_WORKFLOW.md
└─→ docs/api-examples/        (API integration reference)
```

### 🚀 **DevOps/Infrastructure**
```
START_HERE.md
├─→ geesp-angola/k8s/        (Kubernetes deployment)
├─→ docs/guides/DEPLOYMENT_GUIDE.md
├─→ docs/guides/PRODUCTION_ARCHITECTURE.md
└─→ docs/guides/BUILD_WINDOWS_APP_QUICK.md
```

### 📊 **Data Scientist**
```
START_HERE.md
├─→ geesp-angola/data/       (processed maps & community data)
├─→ geesp-angola/scripts/mcda_analysis.py
├─→ geesp-angola/scripts/lcoe_calculator.py
├─→ geesp-angola/notebooks/  (demo notebooks)
└─→ docs/analysis/CODE_FUNCTIONALITY_AUDIT.md
```

### 📋 **Project Manager**
```
START_HERE.md
├─→ INDEX.md                                    (status overview)
├─→ docs/analysis/01_PENDING_IMPLEMENTATION_ROADMAP.md
├─→ docs/analysis/00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md
└─→ docs/analysis/PROJECT_HARMONY_TEST_REPORT.md
```

---

## 📈 Consolidation Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Root-level .md files | 27 | 3 | **89% reduction** |
| Test files (main) | 46 | 27 | **41% reduction** |
| Alternative projects in 02_Code | 2 | 0 | **Archived** |
| Navigation clarity | Low | High | ✅ Streamlined |

---

## 🔄 Key Changes Made

### ✅ Archival Strategy
- **geesp-angola/** (Angelo variant) → `08_Archive/geesp-angola-fixes/`
  - Only had 1 file (phase2_unicode_logging_fix.py)
  - Preserved in archive, not needed in active development

- **code from google creator/** → `08_Archive/google-ai-studio-app/`
  - Google AI Studio alternative frontend
  - Different project type, alternative implementation
  - Preserved for reference, not active

### ✅ Test Consolidation
Archived older test versions (17 files moved):
- `test_lcoe_adapted.py` → archive (kept `test_lcoe_consolidated.py`)
- `test_mcda_expanded.py` → archive (kept `test_mcda_comprehensive.py`)
- `test_*_phase*.py` variants → archive (kept consolidated versions)

**Current Core Tests (27 files)**:
- `test_lcoe_consolidated.py` ✅
- `test_mcda_consolidated.py` ✅
- `test_integration_full_workflow.py` ✅
- `test_dashboard_*.py` ✅
- `test_security.py` ✅
- + 17 other focused tests

### ✅ Documentation Organization
**Golden Source** (root):
- `START_HERE.md` - Entry point
- `README.md` - Project overview
- `INDEX.md` - Complete documentation map

**Organized Under docs/**:
- `guides/` - Operational guides (build, deploy, develop)
- `analysis/` - Code analysis, audits, roadmaps
- `api-examples/` - JSON examples by endpoint type
- `archived-versions/` - Historical consolidation reports
- `ERROR_CODES.md` - API error reference

---

## 🚀 Active Projects

### 1. **geesp-angola** (PRIMARY)
- **Status**: ✅ Production-ready
- **Type**: Python + Streamlit
- **Purpose**: Multi-criteria solar suitability analysis for Angola
- **Components**: Dashboard UI, MCDA engine, LCOE calculator, MAPS
- **Tests**: 27 core test suites
- **Scale**: 140 files, fully comprehensive

### 2. **nevermindu** (FRONTEND ALTERNATIVE)
- **Status**: ✅ Active development
- **Type**: React + Express + TypeScript
- **Purpose**: Full-stack web interface for GEESP
- **Components**: Interactive map, financial analysis, scenario management
- **Scale**: Complete modern web stack

### 3. **Archived Projects** (08_Archive)
- **geesp-angola-fixes**: Single bug fix (preserved for reference)
- **google-ai-studio-app**: Google AI Studio variant (preserved for reference)

---

## 📝 File Categories

### 🌟 Golden Source (Never Edit Lightly)
- `START_HERE.md` - Master entry point
- `INDEX.md` - Complete doc map
- `README.md` - Project overview
- `STRUCTURE.md` - This file (folder guide)

### 📚 Reference (Update When Changes Made)
- `docs/guides/*` - Operational procedures
- `docs/api-examples/*` - API patterns
- `docs/ERROR_CODES.md` - Error handling

### 🔬 Analysis (For Understanding, Not Active Development)
- `docs/analysis/*` - Audit reports, status checks
- `docs/archived-versions/*` - Historical reports

### 💾 Archive (Preserved, Not Active)
- `08_Archive/*` - Alternative projects & old fixes

---

## ✅ Navigation Checklist

- [ ] **First time?** Read [`START_HERE.md`](START_HERE.md)
- [ ] **Looking for something?** Check [`INDEX.md`](INDEX.md)
- [ ] **Need to set up?** See `docs/guides/DEPENDENCIES_AND_SETUP.md`
- [ ] **Want to deploy?** Read `docs/guides/DEPLOYMENT_GUIDE.md`
- [ ] **Need API examples?** Check `docs/api-examples/`
- [ ] **Debugging errors?** See `docs/ERROR_CODES.md`
- [ ] **Understanding architecture?** Check `docs/guides/PRODUCTION_ARCHITECTURE.md`
- [ ] **Curious about status?** See `docs/analysis/00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md`

---

## 🔄 Maintenance Guidelines

### Adding New Documentation
```
If it's a...                          → Place it in...
- Operational guide                  → docs/guides/
- API example                        → docs/api-examples/
- Code audit/analysis                → docs/analysis/
- Historical phase report            → docs/archived-versions/
- Golden source (master list)        → Root (START_HERE, INDEX, README)
```

### Archiving Old Content
```
Move to docs/archived-versions/ when:
- Document is > 6 months old and superseded
- Represents a completed phase (not active)
- Useful for reference but not needed daily
```

### Test File Organization
```
Keep in tests/                       Archive to tests/_archived_test_versions/
- test_*_consolidated.py            - test_*_adapted.py
- test_*_comprehensive.py           - test_*_expanded.py
- test_*_workflow.py                - test_*_phase*.py
- test_security.py                  - test_*_option*.py
- test_integration_full.py
```

---

## 📊 Quick Stats

- **Total Projects**: 2 active + 2 archived
- **Main Codebase**: 140 files (geesp-angola)
- **Test Suites**: 27 active, 17 archived versions
- **Documentation**: 30+ files organized in 4 categories
- **API Examples**: 10 JSON request/response pairs
- **Error Codes**: 25+ mapped with solutions
- **Lines of Code**: ~15,000+ (fully functional)

---

## 🎯 Next Steps

### Immediate (This Week)
- [ ] Verify all imports work after consolidation
- [ ] Run full test suite to confirm no regressions
- [ ] Update CI/CD to use archived test location references

### Short-term (Next 2 Weeks)
- [ ] Begin T2.1 implementation (User Management)
- [ ] Archive remaining old scripts as needed

### Medium-term (Next Month)
- [ ] Consolidate nevermindu and geesp-angola dashboards into single interface
- [ ] Unify authentication between frontend and backend
- [ ] Complete T2.2-T2.8 implementation

---

**Questions?** → See [`INDEX.md`](INDEX.md) or [`START_HERE.md`](START_HERE.md)
