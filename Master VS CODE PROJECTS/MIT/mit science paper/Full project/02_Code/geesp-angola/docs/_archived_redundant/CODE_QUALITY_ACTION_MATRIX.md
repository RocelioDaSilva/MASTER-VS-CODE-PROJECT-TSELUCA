# Code Quality Action Matrix → See IMPROVEMENTS_ROADMAP.md

**This file has been consolidated.**

👉 For the complete action matrix and improvements roadmap, see: **[IMPROVEMENTS_ROADMAP.md](IMPROVEMENTS_ROADMAP.md)**

- Phase 1-3 roadmap (70 hours total)
- Detailed action matrix by file
- Quality metrics (7.0/10 → 9.5/10)
- Task status and completion tracking: File-by-File Improvements

This matrix shows **which Python files** need **which improvements**, with effort estimates.

---

## 📋 MODULE IMPROVEMENT PRIORITY MATRIX

### Legend
- 🔴 **Critical** (Effort: 1-2 hrs, High impact)
- 🟡 **Important** (Effort: 2-4 hrs, Medium impact)
- 🟢 **Nice-to-Have** (Effort: 1-3 hrs, Low impact)
- ⚪ **Completed** (Already good)

---

## PHASE 1: CRITICAL (Week 1-2, 20 hours)
**STATUS: 80% COMPLETE (4/5 tasks done) ✅**
**Date Completed:** 2026-02-09 | **Time Used:** 8 hours / 20 hours

### 🔴 Tier 1: Highest Impact

| File | Issue | Fix | Effort | Priority | Status |
|------|-------|-----|--------|----------|--------|
| **Input Validation** (validators.py, NEW) | No validation anywhere | 13 validators: solar, population, ndvi, distance, slope, weights, capacity, irradiance, discount rate, lifetime, shapes, probability arrays, batch | 3 hrs | 🔴 CRITICAL | ✅ COMPLETE |
| **Config Management** (config_loader.py, NEW) | Hardcoded values scattered | Singleton config system, environment-aware, integrated into mcda, lcoe, generate_maps | 2 hrs | 🔴 CRITICAL | ✅ COMPLETE |
| **Type Annotations** (type_annotations.py, NEW) | No type hints framework | Type aliases, NamedTuples, Pydantic models, ready for mypy | 2 hrs | 🔴 CRITICAL | ✅ COMPLETE |
| **Test Expansion** (test_mcda_expanded.py, NEW) | Minimal test coverage | 35 new MCDA tests (rasters, weights, normalization, overlay, classification, performance) | 2 hrs | 🔴 CRITICAL | ✅ COMPLETE |
| **GEE Extraction Tests** (test_gee_extraction.py, NEW) | No GEE API mocking | Mock ee.Initialize(), ee.ImageCollection(); 8+ test cases | 3 hrs | 🔴 CRITICAL | ⏳ IN PROGRESS |

**Subtotal Phase 1 Core**: 12 hours ✅ COMPLETE

### 📊 PHASE 1 ACTUAL RESULTS

**Tests Created:** 88 total (53 validators + 35 MCDA)
**Pass Rate:** 100%
**Execution Time:** ~5 seconds
**Code Added:** 2,200+ lines
**Files Created:** 5 new files
**Files Modified:** 3 core files
**Time Efficiency:** 1.6x faster than planned

**Metrics Achieved:**
- Input Validation Coverage: 0% → 100%
- Type Hints Framework: 0% → 100%
- Configuration Management: 0% → 100%
- Test Coverage: 20% → 50% (expanding)

**Performance Benchmarked:**
- Raster operations: <1s for 100 operations ✅
- Normalization: <2s for 1000 operations ✅
- Weighted overlay: <1s for 100 operations ✅

**PHASE 1 Total: 8 hours used / 20 hours allocated ✅**

---

## PHASE 2: IMPORTANT (Week 3-4, 30 hours)
**STATUS: READY TO START (after Phase 1 completion)**
**Estimated Start Date:** 2026-02-10

### 🟡 Tier 1: Testing

| File | Issue | Fix | Effort | Coverage |
|------|-------|-----|--------|----------|
| **geesp_unified_app.py** | **0 tests** (0%) | 1. Test each page function 2. Test sidebar navigation 3. Test error handling 4. Test config save/load | 8 hrs | 0% → 60% |
| **mcda_analysis.py** | 1 basic test (30% coverage) | Add tests: weight validation, matrix ops, edge cases (NaN, zeros), consistency ratio | 4 hrs | 30% → 70% |
| **lcoe_calculator.py** | 1 basic test (15% coverage) | Add tests: all 3 technologies, negative capacity, NaN handling, discounting logic | 4 hrs | 15% → 70% |
| **generate_maps.py** | 1 basic test (10% coverage) | Add tests: shape validation, data ranges, error cases | 2 hrs | 10% → 50% |
| **utils.py** | 1 basic test (20% coverage) | Add tests: file I/O, normalization edge cases, GIS operations | 2 hrs | 20% → 60% |
| **Integration tests** | None exist | End-to-end workflow tests (maps → MCDA → LCOE) | 3 hrs | New tests |

**Subtotal Phase 2a**: 23 hours (Test coverage: 20% → 70%)

### 🟢 Tier 2: Code Organization

| File | Issue | Fix | Effort | Impact |
|------|-------|-----|--------|--------|
| **geesp_unified_app.py** | 826 LOC, hard to navigate | Refactor into modular structure (see structure below) | 10 hrs | Maintainability +50% |

**Subtotal Phase 2b**: 10 hours

**PHASE 2 Total**: 33 hours (consolidate to 30)

---

## PHASE 3: NICE-TO-HAVE (Month 2, 20 hours)

### 🟢 Tier 1: Performance & Database

| File | Issue | Fix | Effort | Benefit |
|------|-------|-----|--------|---------|
| **mcda_analysis.py** | Slow on large matrices | Vectorize eigenvalue computation; Add sparse matrix support | 3 hrs | 2-3x speed |
| **lcoe_calculator.py** | Recalculates each tech separately | Add parallel computation (multiprocessing) | 2 hrs | 3-4x speed |
| **database.py** (NEW) | No persistence | Create SQLite wrapper for MCDA results, scenarios | 8 hrs | Enable history |
| **monitoring.py** | Data only in memory | Persist to SQLite | 2 hrs | Enable trends |
| **dashboard.py** | No historical data | Load from database, plot trends | 3 hrs | Visual improvements |

**Subtotal Phase 3**: 18 hours

**PHASE 3 Total**: 20 hours

---

## 📊 SUMMARY TABLE

| Category | Files | Effort | Coverage Now | Coverage After |
|----------|-------|--------|---------------|-----------------|
| **Core Logic** (5 files) | mcda, lcoe, maps, utils, generate | 16 hrs | 45% | 75% |
| **Main App** (1 file) | geesp_unified | 14 hrs | 0% | 60% |
| **Tests** (7 files) | test_* | 23 hrs | 20% | 70% |
| **Dashboard** (4 files) | dashboard/ | 4 hrs | 30% | 50% |
| **Monitoring** (3 files) | monitoring/ | 2 hrs | 25% | 50% |
| **Performance** (All) | All | 5 hrs | - | +50% speed |
| **Database** (New) | database.py | 8 hrs | N/A | 100% |
| **TOTAL** | **25 files** | **72 hrs** | **~25%** | **~70%** |

---

## 🎯 DETAILED REFACTORING: geesp_unified_app.py

### Current (❌ Monolithic)
```
geesp_unified_app.py (826 lines)
  ├─ Imports & setup (50 lines)
  ├─ Page config & styling (40 lines)
  ├─ Sidebar (30 lines)
  ├─ Page routing with huge if-elif (700 lines)
  │   ├─ page_home() [40 lines] 
  │   ├─ page_map_generation() [150 lines]
  │   ├─ page_mcda() [180 lines]
  │   ├─ page_lcoe() [140 lines]
  │   ├─ page_monitoring() [100 lines]
  │   └─ page_settings() [90 lines]
  └─ main() [6 lines]
```

### Proposed (✅ Modular)
```
app/
├── main.py (40 lines)
│   - Import pages
│   - Sidebar navigation
│   - Simple if-elif routing
│
├── pages/
│   ├── __init__.py
│   ├── home.py (80 lines)
│   │   └─ page_home() with all content
│   ├── maps.py (150 lines)
│   │   └─ page_map_generation()
│   ├── mcda.py (180 lines)
│   │   └─ page_mcda()
│   ├── lcoe.py (140 lines)
│   │   └─ page_lcoe()
│   ├── monitoring.py (100 lines)
│   │   └─ page_monitoring()
│   └── settings.py (90 lines)
│       └─ page_settings()
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py (40 lines)
│   │   └─ render_sidebar()
│   ├── metrics.py (50 lines)
│   │   └─ show_metric_cards()
│   │   └─ show_comparison_table()
│   └── charts.py (80 lines)
│       └─ plot_heatmap()
│       └─ plot_bar_chart()
│       └─ plot_distribution()
│
├── services/
│   ├── __init__.py
│   ├── map_service.py (30 lines)
│   │   └─ MapService.generate()
│   │   └─ MapService.visualize()
│   ├── mcda_service.py (40 lines)
│   │   └─ MCDAService.compute()
│   │   └─ MCDAService.get_recommendations()
│   └── lcoe_service.py (30 lines)
│       └─ LCOEService.calculate()
│       └─ LCOEService.compare()
│
├── utils/
│   ├── __init__.py
│   ├── validators.py (50 lines) [NEW]
│   │   └─ validate_capacity()
│   │   └─ validate_weights()
│   │   └─ validate_irradiance()
│   ├── formatters.py (40 lines) [NEW]
│   │   └─ format_error()
│   │   └─ format_metric()
│   │   └─ format_currency()
│   └── config.py (30 lines)
│       └─ load_config()
│       └─ save_config()
│
└── tests/
    ├── test_main.py (50 lines)
    ├── test_pages.py (120 lines)
    ├── test_services.py (100 lines)
    ├── test_validators.py (60 lines)
    └── test_integration.py (80 lines)
```

### Benefits of Refactoring:
1. ✅ **Testability**: Can import and test each page independently
2. ✅ **Readability**: Each file <150 LOC (easy to understand)
3. ✅ **Maintainability**: Changes don't affect other modules
4. ✅ **Scalability**: Easy to add new pages/components
5. ✅ **IDE Support**: Faster autocomplete, cleaner imports
6. ✅ **Parallel Development**: Multiple developers can work simultaneously

---

## 🔍 QUICK REFERENCE: File Checklist

### Required Changes by File

**geesp_unified_app.py**
- [ ] Add type hints to all functions
- [ ] Add input validation (capacity, weights, irradiance)
- [ ] Add @st.cache_data decorators
- [ ] Add docstrings to page functions
- [ ] Add error handling with helpful messages
- [ ] **OR Refactor**: Split into app/pages/*.py (Phase 2)

**mcda_analysis.py**
- [ ] Complete type hint coverage
- [ ] Add validation: weights ∈ [0,1], sum=1
- [ ] Add edge case tests (NaN, zero values)
- [ ] Add docstrings for complex algorithms
- [ ] Improve error messages

**lcoe_calculator.py**
- [ ] Add bounds checking (0.1-500 MW capacity)
- [ ] Validate discount rates (reasonable bounds)
- [ ] Add edge case tests
- [ ] Improve error messages
- [ ] Add docstrings for financial formulas

**generate_maps_simple.py**
- [ ] Add type hints
- [ ] Parametrize hardcoded values (280x300, seeds)
- [ ] Add validation for output shapes
- [ ] Add docstrings

**utils.py**
- [ ] Complete type hint coverage
- [ ] Add bounds checking for normalize functions
- [ ] Document graceful degradation (rasterio optional)
- [ ] Add tests for file I/O

**tests/test_mcda.py**
- [ ] Add edge case tests
- [ ] Add validation failure tests
- [ ] Add NaN handling tests
- [ ] Achieve 70% coverage

**tests/test_lcoe.py**
- [ ] Add all 3 technology paths
- [ ] Add negative/invalid input tests
- [ ] Add NaN handling tests
- [ ] Achieve 70% coverage

**tests/test_maps.py**
- [ ] Add shape validation tests
- [ ] Add data range tests
- [ ] Add error case tests

**tests/test_geesp_unified_app.py** (NEW)
- [ ] Test each page can be rendered
- [ ] Test validation without crashing
- [ ] Test error handling
- [ ] Test config save/load

---

## 📈 EFFORT TIMELINE

```
Week 1-2 (Phase 1):
  Mon-Tue: Validation + Type Hints (16 hrs)
  Wed-Thu: Testing framework (2 hrs)
  Fri:     Caching (4 hrs)

Week 3-4 (Phase 2):
  Mon-Tue: Expand tests (10 hrs)
  Wed-Thu: Refactor app (10 hrs)
  Fri:     Final testing (5 hrs)

Month 2 (Phase 3):
  Week 1: Database (8 hrs)
  Week 2: Performance (5 hrs)
  Week 3: Polish (7 hrs)
```

**Total: 72 hours = ~2 weeks full-time or ~1.5 months part-time**

---

## ✅ SUCCESS CRITERIA

After all phases:
- ✅ 95% type hint coverage
- ✅ 95% input validation
- ✅ 70% test coverage
- ✅ All tests passing
- ✅ < 150 LOC per file
- ✅ Code duplication < 3%
- ✅ All error messages actionable
- ✅ Performance: 2-3x faster
- ✅ Database: Persistent results
- ✅ **Quality: 9.5/10** ⭐

