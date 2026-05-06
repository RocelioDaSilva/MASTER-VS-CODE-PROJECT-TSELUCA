# GEESP-Angola Dashboard: Component Quick Reference

**Status**: Current State Analysis (Feb 12, 2026)
**Purpose**: Quick lookup for all dashboard components

---

## Components by Type

### 📊 INPUT COMPONENTS

| Component | Current Location | Input Type | State Storage | Notes |
|-----------|------------------|-----------|---|---|
| **Weight Sliders** | Page 3 (MCDA) | 5× Streamlit slider | Session state | Auto-normalizes to 100% |
| **File Uploader** | Page 2 (Data) | GeoTIFF file | Session buffer | Single file only; no validation |
| **Zone Selector** | Page 3 (MCDA) | Dropdown (4 options) | Session state | Hardcoded zones |
| **Technology Select** | Page 5 (LCOE) | Dropdown (3 options) | Session state | PV Fixed / PV Tracker / Hybrid |
| **Numeric Inputs** | Page 5 (LCOE) | 4× Number input | Session state | Capacity, irradiance, rate, lifetime |
| **Layer Toggles** | Page 3 (MCDA) | Multiselect (5 layers) | Session state | Irrad / Demand / Access / Infra / LC |
| **AHP Matrix Editor** | Page 3 (MCDA) | Checkbox + Table | Read-only | Example only; not user-configurable |

### 🗺️ MAPPING COMPONENTS

| Component | Library | Status | Capability | Issue |
|-----------|---------|--------|-----------|-------|
| **Base Map** | Folium | ✅ Working | OpenStreetMap | No layer control |
| **Community Markers** | Folium | ✅ Working | Lat/Lon pins (45 communities) | Hardcoded coordinates |
| **Zone Boundaries** | Folium | ❌ Missing | Should show 3 priority zones | Needed for Phase 1 |
| **Aptitude Overlay** | Matplotlib + Folium | ✅ Working | Colored raster visualization | PNG only (low DPI) |
| **Live GPS Tracker** | Mapbox GL | ❌ Missing | Real-time field team tracking | Needed for monitoring page |

### 📈 VISUALIZATION COMPONENTS

| Component | Library | Used On | Output | Notes |
|-----------|---------|---------|--------|-------|
| **KPI Cards** | Streamlit metric | Page 1 | 4 cards | Hardcoded values |
| **Weight Bar Chart** | Plotly | Page 3 | Bar chart | Auto-generated from sliders |
| **Distribution Box Plot** | Plotly | Page 2 | Box plot | Per-layer statistics |
| **LCOE Bar Comparison** | Plotly express | Page 5 | Bar chart | 3 technology comparison |
| **Sensitivity Line Plot** | Plotly express | Page 3 | Line chart | Perturbation analysis |
| **Zone Summary Table** | Pandas/Streamlit | Page 4 | DataFrame | Hardcoded data |
| **Tech Recommendations Table** | Pandas/Streamlit | Page 4 | DataFrame | Hardcoded data |
| **Statistics Table** | Pandas/Streamlit | Page 2 | DataFrame | Min/max/mean/std |

### 🎯 ANALYSIS COMPONENTS

| Component | Function | Input | Output | Cached |
|-----------|----------|-------|--------|--------|
| **Weighted Overlay** | MCDA engine | 5 rasters + weights | Aptitude map (.npy) | ❌ No |
| **Normalization** | Min-max scaling | Any raster | [0,1] normalized | ❌ No |
| **Sensitivity Analysis** | Perturbation | Weights ± range % | Mean vs. delta plot | ❌ No |
| **LCOE Calculator** | Financial model | Tech + capacity + irr | LCOE comparison table | ❌ No |
| **Technology Recommender** | LCOE + irradiance | Mean irradiance | Best tech suggestion | ❌ No |

### 💾 DATA MANAGEMENT COMPONENTS

| Component | Type | Location | Format | Status |
|-----------|------|----------|--------|--------|
| **Config Loader** | Utils | `utils/config.py` | JSON | ✅ Working |
| **Raster Loader** | Utils | `utils/data_io.py` | .npy / .tif | ✅ Working |
| **Raster Saver** | Utils | `utils/data_io.py` | .npy / .tif | ⚠️ Partial (GeoTIFF optional) |
| **DataFrame Export** | Utils | (Ad-hoc) | CSV | ✅ Working |
| **GeoTIFF Export** | Utils | Page 3 | .tif | ⚠️ Fails if rasterio missing |

### ❌ MISSING COMPONENTS

| Component | Purpose | Status | Phase |
|-----------|---------|--------|-------|
| **PDF Report Generator** | Export formatted results | ❌ Missing | Phase 2 |
| **Database Persistence** | Store analysis results | ❌ Missing | Phase 3 |
| **Redis Cache** | Speed up repeated queries | ❌ Missing | Phase 3 |
| **GPS Tracker** | Real-time field location | ❌ Missing | Phase 2 (monitoring page) |
| **Offline-Capable Form** | Mobile field checklist | ❌ Missing | Phase 2 (monitoring page) |
| **Alert System** | Notify on conflicts | ❌ Missing | Phase 2 (monitoring page) |
| **Monte Carlo Analysis** | Uncertainty quantification | ❌ Missing | Phase 3 |
| **Tornado Chart** | LCOE sensitivity | ❌ Missing | Phase 2 |

---

## Current Component Inventory by Page

### PAGE 1: 🏠 Home (150 lines)

**User-Facing Components**:
- Title + description text
- 4× KPI metric cards (Criteria, Zones, Population, LCOE)
- Objectives list (4 items)
- Methodology summary (4-step diagram)
- Interactive Folium map
  - 3× Zone markers (orange, priority)
  - 45× Community circles (blue, non-priority)
  - Navigation labels

**Behind-the-Scenes**:
- `st.metric()` for KPI cards
- `folium.Map()` + `folium.Marker()` for mapping
- Hardcoded coordinates + labels

**Issues**:
- ⚠️ No real-time data refresh (static on load)
- ⚠️ KPI values hardcoded (should read from config/database)

---

### PAGE 2: 📊 Data Exploration (80 lines)

**User-Facing Components**:
- GeoTIFF file uploader
- Criteria multiselect (5 layers)
- Statistics table (min, max, mean, stdev, count)
- Box plot distribution chart
- Data type & shape display

**Behind-the-Scenes**:
- `st.file_uploader()` for file input
- `np.nanpercentile()` for statistics
- `plotly.graph_objects.Box()` for visualization
- `utils.load_raster()` for data I/O

**Outputs**:
- Layer stats displayed in UI
- No persistence (ephemeral)

**Issues**:
- ⚠️ No projection metadata display
- ⚠️ Single file only (no batch upload)
- ⚠️ No raster bounds validation
- ⚠️ No CRS/transform info shown

---

### PAGE 3: 🎯 MCDA Analysis (250 lines)

**User-Facing Components**:
- 5× Weight sliders (Irrad, Demand, Access, Infra, LC)
- Weight normalization display (percentage sum)
- Weight distribution bar chart
- Zone selector (4 options: All, A, B, C)
- Layer visibility toggles (5 layer checkboxes)
- Sensitivity configuration:
  - Criterion selector
  - Variation range slider (0-50%)
  - Step size slider (1-20%)
- AHP Matrix display (checkbox to show)
- Execute MCDA button
- Execute Sensitivity button
- Results display:
  - Aptitude map (PNG overlay)
  - Statistics metrics (pixels, min/max/mean)
  - Download buttons (.npy, .png)
  - Technology recommendation text
- Sensitivity plot (line chart)

**Behind-the-Scenes**:
- `st.slider()` × 5 for weights
- `st.multiselect()` for layer toggles
- Session state for ephemeral storage
- `np.nanmin/max()` for normalization
- Weighted sum: `Σ(w_i * raster_i)`
- `matplotlib.pyplot` for PNG generation
- `plotly.express.line()` for sensitivity plot
- `LCOECalculator.compare_technologies()` for tech recommendation

**Outputs**:
- `.npy` file: `mapa_aptidao_integrada.npy`
- `.tif` file: `mapa_aptidao_integrada.tif` (optional, may fail)
- PNG for in-browser display
- Sensitivity DataFrame + plot

**Issues**:
- ⚠️ GeoTIFF output fails silently if rasterio unavailable
- ⚠️ No bounds validation before overlay
- ⚠️ Sensitivity results not cached (slow re-computation)
- ⏳ AHP matrix is read-only example
- ⏳ No visualization of weight uncertainty

---

### PAGE 4: 📈 Results (80 lines)

**User-Facing Components**:
- Zone comparison table (3 zones × 6 columns)
- Technology recommendations table (3 zones × 3 columns)
- Sensitivity robustness plot (line chart)
- Export buttons (suggested but broken)

**Behind-the-Scenes**:
- Hardcoded zone data (no computation)
- Hardcoded tech recommendations (no computation)
- Plotly line chart for sensitivity

**Outputs**:
- Visual display only (no file persistence)

**Issues**:
- 🔴 **CRITICAL**: All data hardcoded (should read from MCDA)
- ⚠️ Export buttons don't work (no implementation)
- ⚠️ Robustness = "Robust" placeholder (should compute variance)
- ⏳ No confidence intervals displayed
- ⏳ No zone filtering/sorting UI

---

### PAGE 5: 💰 LCOE Calculator (120 lines)

**User-Facing Components**:

*Left Column (Inputs)*:
- Capacity slider (0.1-100 MW, default 1.0)
- Irradiance input (1000-3000 kWh/m²/a, default 2226)
- Discount rate slider (1-15%, default 8%)
- Lifetime slider (10-40 yrs, default 25)
- Technology dropdown (3 options)
- Calculate button

*Right Column (Results)*:
- LCOE comparison bar chart (Plotly)
- Detailed comparison table (5 columns)
- Export buttons (suggested but broken)
- Help section (collapsible)

**Behind-the-Scenes**:
- `scripts/lcoe_calculator.py` (390 lines) for computations
- `LCOECalculator` class with methods:
  - `calculate_pv_fixed()` → LCOE for fixed PV + batteries
  - `calculate_pv_tracker()` → LCOE for tracking PV
  - `calculate_hybrid()` → LCOE for solar + diesel hybrid
  - `compare_technologies()` → DataFrame comparison
- Financial model includes:
  - CAPEX per technology
  - Degradation (0.5%/yr)
  - Battery replacement (Yr 10-12)
  - O&M costs (1%/yr CAPEX)
  - Diesel fuel escalation (3%/yr)
  - Discount rate application

**Outputs**:
- LCOE comparison table
- Technology ranking by cost

**Issues**:
- ⚠️ Export buttons not implemented
- ⏳ No sensitivity analysis (interest/inflation variation)
- ⏳ Diesel fuel price curve not user-configurable
- ⏳ No Monte Carlo uncertainty
- ⏳ No tornado chart for parameter sensitivity

---

## Key Stats

| Metric | Value |
|--------|-------|
| **Total Lines of Code** (current app) | 752 |
| **Number of Pages** | 5 |
| **Number of Streamlit Widgets** | 40+ |
| **Libraries Used** | Streamlit, Plotly, Folium, Matplotlib, NumPy, Pandas |
| **Data Format Support** | .npy, .tif, .csv, JSON |
| **Test Coverage** | 0% (dashboard); 88 tests in other modules |
| **Components Reused** | 0 (monolithic design) |
| **Hardcoded Values** | 20+ (zone data, coordinates, LCOE parameters) |
| **Broken Features** | Export buttons, GeoTIFF output, robustness metric |

---

## Page Navigation Flow

```
                          🏠 HOME
                            │
                ┌───────────┼───────────┐
                │           │           │
            Start   Explore Data  Configure MCDA
                │           │           │
                ├─────→  📊 DATA ────→  🎯 MCDA ────┐
                │                                    │
                └────────────────────→  📈 RESULTS ──┤
                                            │        │
                                            └─→ 💰 LCOE
                                            
    [Future] 🔍 MONITORING (field data during Phase 1)
```

---

## Session State Variables

| Variable | Type | Set By | Used By | Persists |
|----------|------|--------|---------|----------|
| `page` (sidebar.radio) | str | nav | all pages | Session only |
| `weights` (sliders) | dict | sliding | MCDA, Results | Session only |
| `current_analysis` | dict | MCDA analyze | Results | Session only |
| `uploaded_file` | file buffer | Data uploader | Data page | Session only |
| `selected_zone` | str | Zone selector | MCDA | Session only |
| `selected_tech` | str | Tech dropdown | LCOE | Session only |
| `lcoe_results` | DataFrame | LCOE calc | LCOE, Results | Session only |

**Problem**: ❌ No persistence across session refreshes or browser closes

---

## Data Files Generated

| File | Location | Format | Size (Typical) | Persistence |
|------|----------|--------|----------------|-------------|
| `mapa_aptidao_integrada.npy` | `data/processed/` | NumPy binary | 2-5 MB | Persistent |
| `mapa_aptidao_integrada.tif` | `data/processed/` | GeoTIFF | 5-10 MB | Persistent (if saved) |
| `mapa_aptidao_integrada.png` | In-memory | PNG | 50-100 KB | Session only |
| Reference layers (5×) | `data/processed/` | .npy | 2-5 MB each | Pre-created |

---

## Recommended Improvements (Priority Order)

### 🔴 CRITICAL (Phase 2 - Now!)

1. **Add database persistence** (results should survive page refresh)
   - Impact: High (lost analysis on refresh)
   - Effort: 8 hrs
   
2. **Fix export buttons** (CSV, GeoTIFF, PDF)
   - Impact: Medium (users can't download results)
   - Effort: 4 hrs

3. **Add monitoring page** (GPS + baseline checklist for field teams)
   - Impact: High (Phase 1 requirement)
   - Effort: 6 hrs

### 🟡 IMPORTANT (Phase 2)

4. **Modularize pages** (< 100 lines each)
   - Impact: Medium (maintainability)
   - Effort: 10 hrs

5. **Create reusable components** (MetricsCard, MapViewer, etc.)
   - Impact: Medium (reduces duplication)
   - Effort: 6 hrs

6. **Add input validation UI** (bounds checking, file validation)
   - Impact: Low (mostly works)
   - Effort: 4 hrs

### 🟢 NICE-TO-HAVE (Phase 3)

7. **Cache with Redis** (speed up repeated queries)
   - Impact: Medium (performance)
   - Effort: 4 hrs

8. **Add sensitivity tornado chart** (LCOE parameter uncertainty)
   - Impact: Low (visualization)
   - Effort: 3 hrs

9. **Add Monte Carlo analysis** (LCOE confidence intervals)
   - Impact: Low (advanced feature)
   - Effort: 5 hrs

---

## Testing Checklist

**Current State**: 12/12 tests passing (in other modules, 0% dashboard coverage)

**Needed**:
- [ ] Page render tests (each page loads without error)
- [ ] Component tests (metrics, sliders, tables)
- [ ] Integration tests (MCDA → Results flow)
- [ ] Export functionality tests
- [ ] Input validation tests
- [ ] Performance benchmarks

**Target**: 70% code coverage from 0%

---

**Document Version**: 1.0 | **Last Updated**: 2026-02-12
