# Phase F Testing Strategy - GEESP-Angola Backend
**Date:** March 9, 2026  
**Purpose:** Comprehensive testing plan for Phase F validation  
**Duration:** 5-7 days estimated

---

## Quick Reference Summary

| Feature | Module | Status | Test Type | Priority |
|---------|--------|--------|-----------|----------|
| Scenario CRUD | api/ | ✅ Code | API + Integration | 🔴 HIGH |
| MCDA Analysis | scripts/analysis/ | ✅ Code | Unit + Integration | 🔴 HIGH |
| LCOE Calculation | scripts/analysis/ | ✅ Code | Unit + Integration | 🔴 HIGH |
| GEE Data Extract | geospatial/ | ✅ Code | Integration | 🔴 HIGH |
| Map Generation | maps/ | ✅ Code | Unit + Integration | 🟡 MEDIUM |
| Dashboard UI | dashboard/ | ✅ Code | E2E + Performance | 🟡 MEDIUM |
| Database ORM | models/ | ✅ Code | Integration | 🔴 HIGH |
| PDF Export | maps/exporters.py | ✅ Code | Unit + Integration | 🟡 MEDIUM |

---

## Module Testing Requirements

### 1. API Module Testing

**File to Create:** `tests/api/test_endpoints.py`

```python
# Test all 8 endpoints
test_create_scenario()           # POST /scenarios
test_get_scenario()              # GET /scenarios/{id}
test_update_scenario()           # PUT /scenarios/{id}
test_delete_scenario()           # DELETE /scenarios/{id}
test_analyze()                   # POST /analyze
test_get_results()               # GET /results/{id}
test_get_maps()                  # GET /maps/{id}
test_health()                    # GET /health

# Test error cases
test_create_scenario_invalid_data()
test_get_scenario_not_found()
test_analyze_missing_scenario()
```

**Expected Inputs/Outputs:**
```
POST /scenarios
Input: {
  "name": "Test Scenario",
  "description": "Test",
  "location": "Luanda",
  "mcda_weights": {...}
}
Output: {
  "id": "uuid",
  "name": "Test Scenario",
  "status": "created",
  "created_at": "2026-03-09T..."
}

POST /analyze
Input: {
  "scenario_id": "uuid",
  "analysis_type": "MCDA",
  "parameters": {...}
}
Output: {
  "analysis_id": "uuid",
  "status": "completed",
  "results": {...}
}
```

**Test Checklist:**
- [ ] Status codes correct (201, 200, 400, 404, 500)
- [ ] Response schemas valid
- [ ] Error messages clear
- [ ] CORS headers present
- [ ] Request validation working
- [ ] Content-Type handling correct

---

### 2. Analysis Modules Testing

**File to Create:** `tests/unit/test_lcoe.py`

```python
# LCOE Calculator Tests
test_calculate_lcoe_pv()         # PV technology
test_calculate_lcoe_tracker()    # Tracker technology
test_calculate_lcoe_hybrid()     # Hybrid technology
test_calculate_npv()              # NPV computation
test_calculate_irr()              # IRR computation
test_bulk_calculation()           # Batch LCOE

# Test parameter validation
test_lcoe_invalid_capacity()
test_lcoe_invalid_irradiance()
test_lcoe_invalid_discount_rate()
test_lcoe_invalid_lifetime()

# Test caching
test_lcoe_caching()              # Same params = cached result
```

**Expected Results:**
```
Test Case: calculate_lcoe_pv(capacity=10MW, irradiance=5.5, discount_rate=8%)
Expected: {
  "lcoe": 0.075,                 # $/kWh
  "capex": 15000000,             # $
  "opex_annual": 180000,         # $
  "npv": 8500000,                # $
  "irr": 12.5,                   # %
  "payback_period": 7.2          # years
}
```

**Test Checklist:**
- [ ] LCOE values within expected range (0.03-0.15 $/kWh)
- [ ] NPV calculations correct
- [ ] Technology costs realistic
- [ ] Parameter validation working
- [ ] Error handling for invalid inputs
- [ ] Performance acceptable (<1s)

---

**File to Create:** `tests/unit/test_mcda.py` (Expand existing)

```python
# MCDA Tests
test_ahp_weighting()             # Weight generation
test_consistency_ratio()           # CR calculation
test_consistency_check()           # CR < 0.1 validation
test_weighted_overlay()            # Layer weighting
test_aptitude_map()                # Suitability map generation
test_zone_ranking()                # Zone ranking

# Edge cases
test_mcda_zero_weights()
test_mcda_extreme_values()
test_mcda_missing_criteria()
```

**Expected Results:**
```
Test Case: ahp_weighting(comparison_matrix)
Expected: {
  "weights": [0.215, 0.185, 0.142, ...],  # 13 weights
  "consistency_ratio": 0.087,              # < 0.1 acceptable
  "max_eigenvalue": 13.95
}

Test Case: weighted_overlay(layers, weights)
Expected: {
  "aptitude": array(shape=(n, m)),        # 0-1000 scale
  "min": 0,
  "max": 985,
  "mean": 450,
  "std": 180
}
```

**Test Checklist:**
- [ ] Weights sum to 1.0
- [ ] Consistency ratio checked (< 0.1)
- [ ] Aptitude in 0-1000 range
- [ ] Output shapes correct
- [ ] NaN handling working
- [ ] Edge cases handled gracefully

---

### 3. Geospatial Module Testing

**File to Create:** `tests/unit/test_gee.py`

```python
# GEE Authentication Tests
test_gee_authenticate()          # Google auth
test_gee_credentials_valid()     # Credential check

# Data Extraction Tests
test_extract_sentinel_2()        # Sentinel data
test_extract_landsat_8()         # Landsat data
test_compute_ndvi()              # NDVI calculation

# Export Tests
test_export_geotiff()            # GeoTIFF export
test_export_batch()              # Batch export
test_batch_status()              # Status polling

# Cloud masking
test_cloud_mask_qa()             # QA-based masking
test_cloud_confidence()          # Confidence threshold
```

**Expected Behavior:**
```
Test Case: extract_sentinel_2(roi, date_range)
Expected:
1. Authenticate with Google
2. Load Sentinel-2 collection
3. Filter by ROI and dates
4. Mask clouds and shadows
5. Compute indices (NDVI, etc.)
6. Return GeoTIFF file

Test Case: export_geotiff(array, filepath, crs)
Expected:
- File created at filepath
- GeoTIFF format valid
- CRS metadata correct
- Data values preserved
```

**Test Checklist:**
- [ ] Authentication flow working
- [ ] GEE API calls succeed
- [ ] Data download completes
- [ ] Exports valid GeoTIFF
- [ ] CRS metadata preserved
- [ ] Cloud masking effective
- [ ] Batch processing parallel

---

### 4. Maps Module Testing

**File to Create:** `tests/unit/test_maps.py` (Expand existing)

```python
# Map Generation Tests
test_generate_suitability_map()  # MCDA output
test_generate_lcoe_map()         # LCOE output
test_generate_infrastructure()   # Infrastructure layer
test_color_ramp()                # Color mapping
test_legend_generation()         # Legend creation

# Export Tests (expand test_maps_pdf.py)
test_export_png()                # PNG export
test_export_geotiff()            # GeoTIFF export
test_export_pdf()                # PDF export
test_pdf_styling()               # PDF appearance

# Annotations
test_compass_rose()              # Direction indicator
test_scale_bar()                 # Scale annotation
test_coordinate_grid()           # Grid overlay
test_metadata_footer()           # Title/metadata
```

**Expected Outputs:**
```
Test Case: generate_suitability_map(aptitude_array)
Expected:
1. PNG image (256-color indexed)
2. Color ramp applied (Viridis)
3. Legend bar on side
4. Metadata footer
5. Valid file at output path
6. File size > 50KB

Test Case: export_pdf(map_image)
Expected:
1. PDF file created
2. A4 page size
3. Margins: 10mm
4. Image properly positioned
5. Metadata embedded
6. Valid PDF (can open with PDF reader)
```

**Test Checklist:**
- [ ] PNG files created
- [ ] Color ramps correct
- [ ] Legends readable
- [ ] PDFs valid
- [ ] Metadata embedded
- [ ] Performance acceptable
- [ ] File sizes reasonable

---

### 5. Database Module Testing

**File to Create:** `tests/integration/test_database_operations.py` (Expand existing)

```python
# Connection Tests
test_database_connection()       # DB connectivity
test_session_creation()          # Session management

# Scenario Model Tests
test_scenario_create()           # Insert scenario
test_scenario_read()             # Query scenario
test_scenario_update()           # Update scenario
test_scenario_delete()           # Delete scenario

# Analysis Result Tests
test_analysis_result_insert()    # Insert analysis
test_analysis_result_query()     # Query results
test_batch_insert()              # Bulk insert

# Relationships
test_scenario_analysis_relationship()  # FK integrity
test_cascade_delete()            # Cascade on delete

# Data Integrity
test_unique_constraints()        # Unique IDs
test_foreign_key_constraints()   # FK validation
test_required_fields()           # Non-null fields
```

**Expected Behavior:**
```
Test Case: scenario_create_read()
1. Insert: Scenario(name="Test", location="Luanda")
2. Commit to database
3. Query: session.query(Scenario).filter_by(name="Test")
4. Assert: Retrieved scenario matches inserted
5. Assert: UUID generated automatically

Test Case: cascade_delete()
1. Create scenario with analysis_results
2. Delete scenario
3. Assert: All related analysis_results deleted
4. Assert: No orphaned records
```

**Test Checklist:**
- [ ] All CRUD operations work
- [ ] Data persists across sessions
- [ ] Relationships maintained
- [ ] Constraints enforced
- [ ] No N+1 queries
- [ ] Transaction rollback works
- [ ] Concurrent access safe

---

### 6. Dashboard Module Testing

**File to Create:** `tests/e2e/test_dashboard.py`

```python
# Page Navigation
test_sidebar_navigation()        # Sidebar working
test_page_load()                 # All pages load
test_page_transitions()          # Page switching

# Component Tests
test_metrics_card()              # Card rendering
test_map_viewer()                # Map interactive
test_weight_sliders()            # Sliders functional
test_zone_table()                # Table display

# Scenario Workflow
test_create_scenario_workflow()  # Full creation
test_run_analysis_workflow()     # Analysis execution
test_view_results()              # Results display
test_download_export()           # Export functionality

# Performance
test_large_dataset()             # Handle 45 communities
test_map_responsiveness()        # Map interaction speed
test_slider_performance()        # Slider smoothness
```

**Expected Behavior:**
```
Test Case: create_scenario_workflow()
1. Load dashboard
2. Go to "Create Scenario" page
3. Fill form: name, location, description
4. Click "Create"
5. Assert: Scenario created (in DB)
6. Assert: Success message displayed
7. Assert: Redirected to scenario view

Test Case: run_analysis_workflow()
1. Open existing scenario
2. Adjust MCDA weights (13 sliders)
3. Click "Run MCDA Analysis"
4. Assert: Spinner shows progress
5. Assert: Results load (< 10s)
6. Assert: Aptitude map displayed
7. Assert: Statistics shown
```

**Test Checklist:**
- [ ] All pages load without errors
- [ ] Navigation works smoothly
- [ ] Form validation working
- [ ] Analysis results display
- [ ] Maps render correctly
- [ ] Export functionality works
- [ ] Loading times acceptable
- [ ] No console errors

---

### 7. Integration Tests (Full Workflows)

**File to Create:** `tests/integration/test_full_workflows.py`

```python
# Complete Workflows
test_workflow_mcda_only()        # MCDA start-to-finish
test_workflow_lcoe_only()        # LCOE start-to-finish
test_workflow_combined()         # MCDA + LCOE analysis
test_workflow_with_export()      # Full pipeline + export

# API to Database Flow
test_api_scenario_persistence()  # API creates, DB stores
test_api_analysis_execution()    # API triggers analysis
test_api_results_retrieval()     # API returns results

# Multi-user Scenarios
test_concurrent_analysis()       # Parallel analyses
test_scenario_isolation()        # No data leakage
```

**Test Flow Example:**
```
test_workflow_combined():
1. POST /scenarios → Create scenario
2. Wait for scenario creation
3. POST /analyze (MCDA) → Run MCDA
4. Wait for completion < 15s
5. GET /results/[id] → Retrieve MCDA results
6. POST /analyze (LCOE) → Run LCOE
7. GET /results/[id] → Retrieve LCOE results
8. GET /maps/[id] → Retrieve generated maps
9. Assert: All steps completed successfully
10. Assert: Results match expectations
11. Assert: Database records created
```

**Test Checklist:**
- [ ] Full workflows execute
- [ ] No data loss
- [ ] Timing expectations met
- [ ] Results consistent
- [ ] Concurrent execution safe
- [ ] Error recovery working
- [ ] Database state correct

---

## Test Execution Timeline

### Day 1: Setup & Unit Tests
```
Morning (2-3 hours):
- Set up pytest framework
- Configure test fixtures (conftest.py)
- Install testing dependencies

Afternoon (3-4 hours):
- Create test_lcoe.py (LCOE unit tests)
- Create test_mcda.py (MCDA unit tests)
- Run: pytest tests/unit/ --cov
```

### Day 2: Geospatial & Maps Tests
```
Morning (2-3 hours):
- Create test_gee.py (GEE integration tests)
- Address GEE authentication mocking

Afternoon (3-4 hours):
- Expand test_maps_pdf.py (PDF export tests)
- Create test_maps.py (Image generation tests)
- Run full unit test suite
```

### Day 3: API & Integration Tests
```
Morning (2-3 hours):
- Create test_endpoints.py (API endpoint tests)
- Test all 8 HTTP endpoints
- Test error handling

Afternoon (3-4 hours):
- Expand test_database_models.py
- Create test_database_operations.py
- Test CRUD flows
```

### Day 4-5: E2E & Performance Tests
```
Day 4:
- Create test_dashboard.py (E2E tests)
- Create test_full_workflows.py (Integration tests)
- Run full test suite with coverage report

Day 5:
- Create test_performance_profiling.py (Benchmarks)
- Performance optimization
- Documentation & reporting
```

---

## Test Execution Commands

```bash
# Run all tests
pytest tests/ -v --cov=backend

# Run specific test category
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v
pytest tests/api/ -v
pytest tests/performance/ -v

# Run with coverage report
pytest tests/ --cov=backend --cov-report=html

# Run single test file
pytest tests/unit/test_lcoe.py -v

# Run single test function
pytest tests/unit/test_lcoe.py::test_calculate_lcoe_pv -v

# Run with performance profiling
pytest tests/performance/ -v --durations=10

# Run with markers
pytest -m "not slow" tests/  # Skip slow tests
pytest -m "integration" tests/  # Run only integration tests
```

---

## Success Criteria

### Unit Tests (✅ Pass all or 95%+)
- [ ] test_lcoe.py: 10/10 passing
- [ ] test_mcda.py: 8/8 passing
- [ ] test_gee.py: 6/6 passing
- [ ] test_maps.py: 8/8 passing
- [ ] test_validation.py: 6/6 passing

### Integration Tests (✅ Pass all or 95%+)
- [ ] test_database_operations.py: 10/10 passing
- [ ] test_api_scenarios.py: 8/8 passing
- [ ] test_analysis_flow.py: 6/6 passing
- [ ] test_export_flow.py: 5/5 passing

### E2E Tests (✅ Pass all or 90%+)
- [ ] test_dashboard.py: 7/7 passing
- [ ] test_full_workflows.py: 6/6 passing

### Performance Tests (✅ All meet targets)
- [ ] LCOE calc: < 1s per scenario
- [ ] MCDA analysis: < 15s
- [ ] Map generation: < 10s
- [ ] PDF export: < 5s
- [ ] API response: < 500ms (P95)

### Code Coverage (✅ 80%+ coverage)
- [ ] api/: 90%+
- [ ] scripts/: 85%+
- [ ] utils/: 90%+
- [ ] models/: 85%+
- [ ] dashboard/: 75% (Streamlit harder to test)
- [ ] **Overall: 80%+**

### Integration Validation (✅ All green)
- [ ] API ↔ Database: ✅
- [ ] API ↔ Analysis: ✅
- [ ] Analysis ↔ Maps: ✅
- [ ] Maps ↔ Export: ✅
- [ ] Dashboard ↔ Backend: ✅

---

## Known Limitations & Workarounds

### GEE Testing
**Issue:** May require valid Google credentials  
**Workaround:** Mock GEE API responses in tests
```python
@patch('geospatial.earth_engine_integration.ee')
def test_extract_sentinel_2(mock_ee):
    mock_ee.Image.return_value = MockGEEImage()
    # ...
```

### Dashboard Testing
**Issue:** Streamlit difficult to test programmatically  
**Workaround:** Test components separately, use manual E2E
```python
# Test components independently
def test_metrics_card():
    card = MetricsCard([{"label": "LCOE", "value": "$0.08"}])
    # Assert rendered correctly (visual inspection)
```

### External Services
**Issue:** Maps/GEE require external API calls  
**Workaround:** Use VCR cassettes to record/playback responses
```python
@vcr.use_cassette('fixtures/gee_extract.yaml')
def test_extract_sentinel_2():
    # First run records actual GEE response
    # Subsequent runs use recorded response
    data = extractor.extract_sentinel_2()
```

---

## Reporting & Documentation

### Test Report Template
```markdown
# Phase F Testing Report
Date: 2026-03-XX
Tester: [Name]

## Summary
- Total Tests: XXX
- Passed: XXX (XX%)
- Failed: X
- Skipped: X
- Coverage: XX%

## Results by Category
- Unit Tests: XX/XX passed ✅
- Integration Tests: XX/XX passed ✅
- E2E Tests: XX/XX passed ⚠️
- Performance Tests: All ✅

## Critical Issues Found
1. [Issue]: [Impact] → [Resolution]

## Known Issues
1. [Minor]: [Impact] → [Workaround]

## Coverage Report
[Link to HTML coverage report]

## Recommendations
1. [Action item]
2. [Action item]

## Sign-off
Date: 2026-03-XX
Status: ✅ READY FOR PRODUCTION / 🔴 BLOCKED
```

---

## Final Validation Checklist

Before marking Phase F complete:

- [ ] All critical bugs fixed
- [ ] Test suite > 80% coverage
- [ ] Performance targets met
- [ ] API fully documented (docstrings)
- [ ] Database schema verified
- [ ] GEE integration tested
- [ ] Map export working
- [ ] Dashboard responsive
- [ ] Error handling comprehensive
- [ ] Logging working
- [ ] Configuration management tested
- [ ] Deployment runbook created
- [ ] Performance baseline established
- [ ] Security review (basic)
- [ ] Documentation complete

---

## Contact & Escalation

**Testing Lead:** [Name]  
**Backend Owner:** [Name]  
**Escalation:** If critical issue found, notify immediately

---

**Document Generated:** March 9, 2026  
**Version:** 1.0  
**Status:** Ready for Phase F Execution
