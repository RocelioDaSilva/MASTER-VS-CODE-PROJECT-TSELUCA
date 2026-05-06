# PHASE 2: TEST COVERAGE & MODULAR REFACTORING
## 30-Hour Sprint for Code Quality Enhancement

**Status:** Ready to Start  
**Budget:** 30 hours  
**Quality Target:** 7.0/10 → 9.5/10  
**Timeline:** Week 1-2 of Phase 2  

---

## 📋 Executive Summary

Phase 2 focuses on expanding test coverage and refactoring monolithic code into maintainable, modular components. This phase addresses the quality gap between Phase 1's (7.0/10) and target (9.5/10) by:

1. **Test Expansion (12 hours)** — From 30% to 70% coverage
2. **Dashboard Refactoring (10 hours)** — From 430-line monolith to 6 pages  
3. **Code Quality (8 hours)** — Remove duplication, complete type hints

---

## 🎯 Task Breakdown

### **T2.1: Test Coverage Expansion** (12 hours)

**Objective:** Increase test coverage from 30% to 70% and add 40+ new integration tests

#### T2.1.1: Integration Test Suite (5 hours)
- **Description:** Create end-to-end tests covering module interactions
- **Deliverables:**
  - `tests/test_integration_mcda_validators.py` — Test MCDA pipeline with validator chain
  - `tests/test_integration_lcoe_config.py` — Test LCOE calculator with config system
  - `tests/test_integration_full_workflow.py` — Complete solar assessment workflow
  - Minimum 15 new tests

**Acceptance Criteria:**
- ✅ Each integration test traces a real user workflow
- ✅ Tests verify data flow between modules
- ✅ All tests pass with mocked Earth Engine data
- ✅ Coverage report shows module-level coverage

**Test Examples:**
```python
# Test: Load config → Generate random rasters → Validate → Run MCDA → Classify
def test_full_workflow_assessment():
    config = load_config()
    shapes = config.get_map_shape()
    
    # Generate test data
    solar_data = np.random.uniform(5, 7, shapes)
    pop_data = np.random.uniform(0, 500, shapes)
    
    # Validate
    assert validate_solar_irradiance(solar_data)
    assert validate_population(pop_data)
    
    # Analyze
    analyzer = MCDAnalyzer()
    result = analyzer.weighted_overlay([solar_data, pop_data], ...)
    
    # Classify
    classes = analyzer.classify_aptitude(result)
    assert classes.shape == shapes
```

#### T2.1.2: Edge Case & Error Handling Tests (4 hours)
- **Description:** Comprehensive edge case coverage
- **Deliverables:**
  - `tests/test_edge_cases_comprehensive.py` — 15+ edge case tests
  - Coverage for: NaN handling, extreme values, boundary conditions
  
**Test Categories:**
- Memory/performance limits (large rasters 2000×2000)
- Invalid configuration values
- Missing or corrupted input files
- Concurrent request handling

**Acceptance Criteria:**
- ✅ All error paths tested
- ✅ Each validator has 5+ edge case tests
- ✅ Performance tests included (execution time ≤ 5s for 1000×1000 raster)

#### T2.1.3: Dashboard Component Tests (3 hours)
- **Description:** Unit tests for Streamlit components
- **Deliverables:**
  - `tests/test_dashboard_components.py` — Component isolation tests
  - `tests/test_dashboard_state.py` — State management tests
  - Test sidebar, maps, metrics, downloads

**Test Examples:**
```python
def test_sidebar_parameter_validation():
    # Verify sidebar rejects invalid weight sum
    weights = {"solar": 0.5, "population": 0.6}  # Sum > 1
    assert sidebar_validate_weights(weights) == False

def test_map_rendering_with_nan():
    # Verify map renders with NaN values
    raster_with_nan = np.array([[1, 2, np.nan], [4, np.nan, 6]])
    assert render_map(raster_with_nan) is not None
```

---

### **T2.2: Dashboard Refactoring** (10 hours)

**Objective:** Transform `geesp-unified-app.py` (430 lines) into modular Streamlit pages

#### Current Structure (430 lines, monolithic):
```
geesp-unified-app.py
├── Imports & config (50 lines)
├── Sidebar setup (80 lines)
├── Map generation & caching (100 lines)
├── MCDA analysis UI (80 lines)
├── Result classification (40 lines)
└── Download & export (80 lines)
```

#### Target Structure (6 pages, ~70 lines each):
```
pages/
├── 1_🏠_Overview.py (70 lines)
│   └── Project summary, key metrics, navigation
├── 2_📊_Data_Upload.py (70 lines)
│   └── Upload rasters, validate, preview
├── 3_🎯_MCDA_Analysis.py (80 lines)
│   └── Weight configuration, sensitivity analysis
├── 4_📈_Results.py (75 lines)
│   └── Classification, statistics, aptitude maps
├── 5_💾_Export.py (70 lines)
│   └── Download formats, batch export
├── 6_⚙️_Settings.py (60 lines)
│   └── Configuration, advanced options, logs
└── utils/
    ├── components.py (100 lines) — Reusable Streamlit widgets
    ├── cache.py (80 lines) — Caching layer for rasters
    └── validators_ui.py (60 lines) — UI validation helpers
```

#### T2.2.1: Page Architecture Setup (2 hours)
- **Deliverables:**
  - Directory structure: `pages/`, `utils/`
  - `shared.py` — Shared state, config, caching
  - `__init__.py` for imports
  
**File Structure:**
```
geesp-angola/
├── geesp_app.py (main entry point, ~50 lines)
├── pages/
│   ├── __init__.py
│   ├── 1_🏠_Overview.py
│   ├── 2_📊_Data_Upload.py
│   ├── 3_🎯_MCDA_Analysis.py
│   ├── 4_📈_Results.py
│   ├── 5_💾_Export.py
│   └── 6_⚙️_Settings.py
├── utils/
│   ├── __init__.py
│   ├── components.py
│   ├── cache.py
│   └── validators_ui.py
└── dashboard/ (old structure)
    └── geesp-unified-app.py (archive)
```

#### T2.2.2: Reusable Component Library (3 hours)
- **Deliverables:**
  - `utils/components.py` — Reusable widgets
  
**Components to Create:**
```python
# Rendering
- render_raster_with_colormap(data, title, cmap='viridis')
- render_side_by_side_maps(raster1, raster2)
- render_classification_legend()

# Input
- weight_slider_group(config, keys=['solar', 'population', ...])
- file_uploader_with_validation(format='tif|npy')
- config_selector(config_type='mcda|lcoe|map')

# Display
- metric_card(label, value, delta=None, icon='📊')
- statistics_panel(raster_data)
- result_summary_table(results)

# State management
- session_state_init() — Initialize persistent state
- get_session_config() — Get current configuration
- cache_raster(key, data) — Memoize raster in session
```

**Example:**
```python
# weight_slider_group usage
weights = weight_slider_group(
    config,
    keys=['solar_irradiance', 'population_density', 'grid_distance'],
    default_config=config.get_mcda_weights()
)
# Returns: {"solar_irradiance": 0.25, "population_density": 0.30, ...}
```

#### T2.2.3: Individual Page Migration (5 hours)
- **Deliverables:**
  - All 6 pages migrated and tested
  
**Per-Page Effort:**
| Page | Lines | Time | Components | Tests |
|------|-------|------|-----------|--------|
| Overview | 70 | 45 min | Dashboard, navbar | 2 |
| Data Upload | 70 | 1h | File uploader, validator | 4 |
| MCDA Analysis | 80 | 1h 15m | Weight sliders, sensitivity | 5 |
| Results | 75 | 1h | Maps, statistics, legend | 5 |
| Export | 70 | 45 min | Download buttons, formats | 3 |
| Settings | 60 | 30 min | Config editor, logs viewer | 2 |

---

### **T2.3: Code Quality & Completeness** (8 hours)

#### T2.3.1: Type Hint Completion (3 hours)
- **Objective:** Increase type hint coverage from 35% to 95%

**Priority Files (in order):**
1. `scripts/mcda_analysis.py` (417 lines) — 20% → 100%
2. `scripts/lcoe_calculator.py` (459 lines) — 15% → 100%
3. `scripts/generate_maps_simple.py` (183 lines) — 30% → 100%
4. `dashboard/geesp-unified-app.py` (430 lines) — 5% → 95%

**Type Hints to Add:**
```python
# Before
def weighted_overlay(self, rasters, weights):
    # implementation
    
# After
def weighted_overlay(
    self, 
    rasters: List[np.ndarray], 
    weights: Dict[str, float],
    normalization: str = "minmax"
) -> np.ndarray:
    # implementation
```

**Tools:**
- Use Pylance for inline hints
- Use `pyright --outputjson` to find missing hints
- Coverage target: 95% of public methods + parameters

#### T2.3.2: Code Duplication Elimination (3 hours)
- **Objective:** Reduce code duplication below 5%

**Common Duplication Patterns to Fix:**
1. **Raster normalization** (appears in 3 files)
   - Extract to `utils/raster_utils.py`
   
2. **Configuration access** (repeated .get() chains)
   - Already in config_loader, verify usage

3. **Error handling** (try/except patterns)
   - Create `utils/error_handlers.py` decorators

4. **Validation chains** (repeated validator calls)
   - Create `scripts/validation_pipeline.py`

**Duplication Detection Method:**
```bash
radon cc scripts/ -a  # Cyclomatic complexity
pylint --duplicate-code-check  # Code duplication
```

#### T2.3.3: Documentation & Docstring Completion (2 hours)
- **Objective:** 100% docstring coverage for public API

**Docstring Format (Google style):**
```python
def weighted_overlay(self, rasters: List, weights: Dict) -> np.ndarray:
    """
    Perform weighted overlay MCDA analysis on multiple rasters.
    
    Combines raster layers using provided weights, normalizing each
    layer before combining. Supports multiple normalization methods.
    
    Args:
        rasters: List of 2D numpy arrays, all same shape (H, W)
        weights: Dict mapping layer names to weights (0-1), must sum ≤ 1.1
        
    Returns:
        2D numpy array of same shape as inputs, values [0, 1]
        
    Raises:
        ValueError: If raster shapes don't match or weights invalid
        TypeError: If inputs not numpy arrays or dict
        
    Examples:
        >>> solar = np.random.uniform(5, 7, (280, 300))
        >>> pop = np.random.uniform(0, 500, (280, 300))
        >>> result = analyzer.weighted_overlay(
        ...     [solar, pop],
        ...     {"solar": 0.6, "population": 0.4}
        ... )
        >>> result.shape
        (280, 300)
    """
```

---

## 📊 Effort & Resource Allocation

### Hours Distribution:
```
T2.1: Test Coverage Expansion       12 hours
    ├── Integration tests           5h
    ├── Edge case tests             4h
    └── Dashboard tests             3h

T2.2: Dashboard Refactoring        10 hours
    ├── Architecture setup          2h
    ├── Reusable components         3h
    └── Page migration              5h

T2.3: Code Quality & Polish         8 hours
    ├── Type hints                  3h
    ├── Duplication removal         3h
    └── Documentation               2h
                                   ─────
TOTAL:                            30 hours
```

### Quality Metrics:
| Metric | Phase 1 | Target P2 | Success Criteria |
|--------|---------|----------|------------------|
| Test Coverage | 30% | 70% | pytest coverage > 70% |
| Lines of Longest File | 430 | 80 | Max page < 80 LOC |
| Type Hint Coverage | 35% | 95% | pyright OK on public API |
| Code Duplication | ~10% | <5% | radon < 5 duplicate lines % |
| Docstring Coverage | 40% | 100% | pydocstyle 0 errors |
| Cyclomatic Complexity | 8 | < 5 | radon cc -a shows all < 5 |

---

## ✅ Acceptance Criteria

### For Phase 2 Completion:

**Test Coverage:**
- [ ] 40+ new tests written
- [ ] Coverage: 70%+ overall, 75%+ for scripts/
- [ ] All MCDA/LCOE integration tests pass
- [ ] Dashboard pages individually testable

**Code Organization:**
- [ ] All 6 pages created and functional
- [ ] Each page < 85 lines (excluding docstrings)
- [ ] Shared utils library in place with 3+ reusable components
- [ ] Old monolith archived, not deleted

**Code Quality:**
- [ ] Type hints: 95%+ coverage (pyright --outputjson reports < 5 "unknown")
- [ ] Docstrings: 100% of public functions
- [ ] Duplication: < 5% (radon report)
- [ ] Cyclomatic complexity: all functions < 5
- [ ] No CI/CD failures (all tests pass)

**Performance:**
- [ ] Page load time < 3s (Streamlit startup)
- [ ] MCDA analysis on 1000×1000 raster < 5s
- [ ] Cache layer working (session state persists)

**Documentation:**
- [ ] PHASE2_COMPLETION_SUMMARY.md written
- [ ] Updated README.md with new architecture
- [ ] Pages documented in SOFTWARE_CAPABILITIES.md

---

## 🛠️ Implementation Strategy

### Week 1 (15 hours):
- Monday: T2.1.1-T2.1.3 (all tests written & passing) — 12h
- Tuesday: T2.2.1-T2.2.2 (pages & components setup) — 3h

### Week 2 (15 hours):
- Wednesday: T2.2.3 (page migration complete) — 5h
- Thursday: T2.3.1-T2.3.3 (quality polish) — 8h
- Friday: Testing & documentation — 2h

### Parallelizable Tasks:
- Individual page creation can be done in parallel (assign pages to different developers)
- Test writing can proceed in parallel with page refactoring

---

## 📦 Deliverables Checklist

- [ ] `tests/test_integration_mcda_validators.py`
- [ ] `tests/test_integration_lcoe_config.py`
- [ ] `tests/test_integration_full_workflow.py`
- [ ] `tests/test_edge_cases_comprehensive.py`
- [ ] `tests/test_dashboard_components.py`
- [ ] `tests/test_dashboard_state.py`
- [ ] `pages/1_🏠_Overview.py`
- [ ] `pages/2_📊_Data_Upload.py`
- [ ] `pages/3_🎯_MCDA_Analysis.py`
- [ ] `pages/4_📈_Results.py`
- [ ] `pages/5_💾_Export.py`
- [ ] `pages/6_⚙️_Settings.py`
- [ ] `utils/components.py` (100+ lines, 10+ components)
- [ ] `utils/cache.py` (caching layer)
- [ ] `utils/validators_ui.py` (form validation)
- [ ] Type hints added to all scripts (95%+)
- [ ] Docstrings added (100% of public API)
- [ ] PHASE2_COMPLETION_SUMMARY.md
- [ ] Updated README.md
- [ ] All 40+ new tests passing (100 → 140+ total tests)

---

## 🎯 Success Metrics

**Before Phase 2:**
- Tests: 100/105 passing (95%)
- Code quality: 7.0/10
- Type hints: 35% coverage
- Coverage: 30%
- Longest file: 430 lines

**After Phase 2:**
- Tests: 140+/145 (96%+)
- Code quality: 9.5/10 ✅
- Type hints: 95% coverage ✅
- Coverage: 70% ✅
- Longest file: 80 lines ✅

---

## 📝 Notes

- Keep Phase 1 deliverables (validators, config) unchanged
- Maintain backward compatibility with existing API
- All original tests must continue to pass
- GEE integration tests remain mocked until credentials available
- Optional: Add GitHub Actions CI/CD for automated testing

---

**Status:** Ready to implement  
**Created:** 2026-02-09  
**Last Updated:** 2026-02-09  
**Owner:** Development Team
