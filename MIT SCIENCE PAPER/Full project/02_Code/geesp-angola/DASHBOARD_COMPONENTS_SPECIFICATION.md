# GEESP-Angola Dashboard: Components Specification

**Version**: 1.0 | **Date**: 2026-02-12 | **Status**: Current State Analysis & Roadmap

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture (5 Pages)](#current-architecture-5-pages)
3. [Component Inventory](#component-inventory)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Proposed 6-Page Modular Structure](#proposed-6-page-modular-structure)
6. [Testing & Performance](#testing--performance)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

The GEESP-Angola dashboard is a **Streamlit-based geospatial analysis platform** for identifying optimal sites for solar mini-grids in Huíla Province, Angola. The application integrates satellite data analysis, multi-criteria decision analysis (MCDA), financial modeling (LCOE), and operational monitoring into an interactive web interface.

**Current State**: 5-page Streamlit application (752 lines of monolithic code)
**Test Status**: 12/12 tests passing (88 total tests across all modules)
**Target State**: 6-page modular architecture with <100 lines per page
**Timeline**: Phase 2 (2-3 weeks post-Phase 1 completion)

---

## Current Architecture (5 Pages)

### **PAGE 1: 🏠 Home (Overview & Navigation)**

**Purpose**: Project introduction, key metrics, geographic context

**Current Components**:
```
├── Title & description
├── Project objectives
├── Methodology steps summary (4 phases)
├── KPI cards (4 metrics)
│   ├── Criteria count (5)
│   ├── Priority zones (3)
│   ├── Population beneficiary (~48k)
│   └── LCOE estimate range (USD 0.18-0.22/kWh)
├── Interactive map (Folium)
│   ├── Base layer (OpenStreetMap)
│   ├── Markers for 3 priority zones (Cacula, Humpata, Quilengues)
│   └── Community grid (45 communities total)
└── Navigation guide
```

**Implementation Details**:
- **Framework**: Streamlit + Folium
- **Data Source**: `data/communities_45.csv` (hardcoded coordinates)
- **Map Type**: Leaflet-based (via Folium wrapper)
- **Marker Style**: Orange for priority zones (aptitude > 0.75), Blue for others
- **Metrics Engine**: `utils.load_config()` for hardcoded values

**Current Code**: ~150 lines (lines 1-150 in app.py)

**Issues Identified**:
- ⚠️ KPI values hardcoded (should read from analysis results)
- ⚠️ Community coordinates duplicated (should use config)
- ⏳ No real-time data refresh (static on load)

---

### **PAGE 2: 📊 Data Exploration**

**Purpose**: Inspect satellite data layers before analysis

**Current Components**:
```
├── GeoTIFF file uploader
│   └── Accepts .tif, .tiff files from user's machine
├── Data layer selector
│   ├── Irradiação Solar (GHI from NASA POWER)
│   ├── Demanda (VIIRS nighttime lights)
│   ├── Acesso (distance to grid)
│   ├── Infraestrutura (slope/DEM)
│   └── Uso do Solo (NDVI)
├── Layer statistics table
│   ├── Min, Max, Mean, StdDev
│   ├── Null count
│   └── Pixel count
├── Distribution visualization
│   ├── Box plots (Plotly)
│   ├── Histograms (on demand)
│   └── Q-Q plots (for normality check)
└── Download export button
```

**Implementation Details**:
- **Framework**: Streamlit + Plotly + NumPy
- **Data Format**: `.npy` (NumPy arrays) + `.tif` (GeoTIFF) with metadata
- **Statistics**: Computed via `numpy.nanpercentile()` (handles NaN values)
- **Visualization**: `plotly.graph_objects.Box()` for distribution
- **File I/O**: `utils.load_raster()` reads GeoTIFF or NPY fallback

**Current Code**: ~80 lines (lines 150-230 in app.py)

**Data Sources**:
- Pre-processed layers in `data/processed/`:
  - `mapa_irradiacao.npy` (5-year average GHI)
  - `mapa_populacao.npy` (VIIRS-derived population density proxy)
  - `mapa_distanciarede.npy` (Euclidean distance to grid infrastructure)
  - `mapa_declividade.npy` (slope % from SRTM DEM)
  - `mapa_ndvi.npy` (vegetation index from Sentinel-2)

**Issues Identified**:
- ⚠️ No projection information display (should show CRS, bounds)
- ⚠️ File upload limited to single file (should support batch)
- ⏳ No data validation (should check raster bounds match)

---

### **PAGE 3: 🎯 MCDA Analysis (Weight Configuration & Sensitivity)**

**Purpose**: Configure criteria weights and examine sensitivity

**Current Components**:
```
├── Weight Configuration
│   ├── 5 sliders (one per criterion)
│   │   ├── Irradiação Solar (default 25%)
│   │   ├── Demanda/VIIRS (default 25%)
│   │   ├── Acesso Grid (default 20%)
│   │   ├── Infraestrutura/Slope (default 15%)
│   │   └── Uso Solo/NDVI (default 15%)
│   ├── Auto-normalization display (sum to 100%)
│   └── Weight distribution bar chart (Plotly)
│
├── Zone & Layer Filter
│   ├── Zone selector (Todas, A-Cacula, B-Humpata, C-Quilengues)
│   ├── Layer visibility toggles (multiselect)
│   └── Layer preview (on demand)
│
├── Sensitivity Analysis Configuration
│   ├── Criterion selector (dropdown)
│   ├── Variation range ±% (0-50%)
│   └── Step size (1-20%)
│
├── AHP Matrix Display
│   ├── Checkbox: "Show pairwise comparison matrix"
│   ├── Example matrix (Saaty scale demonstration)
│   └── Read-only (for education only)
│
├── Execute MCDA Button
│   └── Triggers weighted overlay computation
│
└── Execute Sensitivity Button
    └── Runs perturbation analysis on selected criterion
```

**Implementation Details**:
- **Framework**: Streamlit + Plotly + NumPy
- **Weight Engine**: Manual slider setup → session state storage
- **Normalization**: `weights / sum(weights)` with live display
- **Overlay Computation**: `sum(w_i * raster_i)` weighted sum
- **Normalization Pre-Processing**: Each raster scaled to [0,1] via min-max: `(a - min) / (max - min)`
- **Sensitivity Method**: Perturbation ±range% in steps; recompute overlay for each; plot mean vs. delta

**Current Code**: ~250 lines (lines 230-480 in app.py)

**Computation Outputs**:
- **Aptitude Map**: `data/processed/mapa_aptidao_integrada.npy` (combined raster)
- **Visualization**: In-memory PNG (Matplotlib-rendered overlay map)
- **Statistics**: Min, Max, Mean pixel values
- **Technology Recommendation**: Uses mean irradiance to suggest technology via `LCOECalculator.compare_technologies()`
- **Sensitivity Plot**: Line chart showing mean aptitude vs. weight perturbation

**Issues Identified**:
- ⚠️ GeoTIFF output fails silently if rasterio not installed
- ⚠️ No bounds checking (rasters must align before overlay)
- ⏳ AHP matrix is static example (not user-configurable)
- ⏳ Sensitivity results should be cached (expensive re-computation)

---

### **PAGE 4: 📈 Results (Zone Comparison & Technology Recommendations)**

**Purpose**: Present MCDA outputs and technology recommendations

**Current Components**:
```
├── Priority Zones Summary Table
│   ├── Zone ID (A-Cacula, B-Humpata, C-Quilengues)
│   ├── Area (km²): [850, 620, 720]
│   ├── Mean Aptitude: [0.83, 0.79, 0.76]
│   ├── Irradiance (kWh/m²/day): [6.1, 6.3, 5.9]
│   ├── Population: [45k, 52k, 38k]
│   └── Priority Level: [🔴 Critical, 🟠 High, 🟡 Medium]
│
├── Technology Comparison by Zone
│   ├── Zone A: PV Fixed + Batteries (LCOE USD 0.18-0.22)
│   ├── Zone B: PV with Tracker (LCOE USD 0.22-0.28)
│   └── Zone C: Hybrid Solar+Diesel (LCOE USD 0.25-0.35)
│
├── Sensitivity Analysis Visualization
│   ├── Weight perturbation range: -20% to +20%
│   ├── Robustness assessment: All variations labeled "Robust"
│   └── Line plot (Plotly): Aptitude Mean vs. Variation %
│
└── Export Buttons (on demand)
    ├── Download zone rankings (CSV)
    ├── Download aptitude map (GeoTIFF)
    └── Download report (PDF)
```

**Implementation Details**:
- **Framework**: Streamlit + Plotly + Pandas
- **Data Source**: Hardcoded zone statistics (should read from analysis)
- **Technology Recommendation**: Based on mean irradiance in each zone
- **Visualization**: `plotly.express.line()` for sensitivity curves
- **Robustness Assessment**: All scenarios marked "Robust" (placeholder)

**Current Code**: ~80 lines (lines 480-560 in app.py)

**Issues Identified**:
- ⚠️ All data hardcoded (should read from MCDA computation)
- ⚠️ No export functionality implemented (buttons present but no action)
- ⏳ Robustness assessment is placeholder (should compute variance)
- ⏳ No confidence intervals on zone rankings

---

### **PAGE 5: 💰 LCOE Calculator (Financial Analysis)**

**Purpose**: Estimate costs and compare energy technologies

**Current Components**:
```
├── Input Parameters (Left Column)
│   ├── Capacity (MW): [0.1 - 100.0, default 1.0]
│   ├── Annual Irradiance (kWh/m²/ano): [1000 - 3000, default 2226]
│   ├── Discount Rate (%): [1 - 15, default 8%]
│   ├── Project Lifetime (years): [10 - 40, default 25]
│   └── Technology: [PV Fixed + Batteries, PV with Tracker, Hybrid Solar+Diesel]
│
├── Results Display (Right Column)
│   ├── LCOE Comparison Bar Chart (Plotly)
│   │   ├── Technology on X-axis
│   │   ├── LCOE (USD/kWh) on Y-axis
│   │   └── Color scale: Green (low) → Red (high)
│   │
│   ├── Detailed Comparison Table
│   │   ├── Technology name
│   │   ├── CAPEX (USD/kW)
│   │   ├── Annual Generation (MWh)
│   │   ├── LCOE (USD/MWh)
│   │   └── LCOE (USD/kWh)
│   │
│   └── Download Export Buttons
│       ├── Export as CSV
│       └── Export as JSON
└── Help Section (Collapsible)
    ├── LCOE formula explanation
    ├── Parameter descriptions
    └── Assumptions documentation
```

**Implementation Details**:
- **Framework**: Streamlit + Plotly + Pandas
- **Calculator Engine**: `scripts/lcoe_calculator.py` (390 lines)
- **Technologies**:
  - **PV Fixed + Batteries**: Includes battery replacement at year 10-12
  - **PV with Tracker**: Higher CAPEX but improved output
  - **Hybrid Solar+Diesel**: Includes diesel backup, fuel cost escalation
- **Financial Model**:
  - **LCOE Formula**: (CAPEX + PV(O&M) - PV(Salvage)) / PV(Generation)
  - **Discount Rate**: 8% default (user configurable 1-15%)
  - **Life**: 25 years default (user configurable 10-40 years)
  - **Degradation**: PV system ~0.5%/year
  - **Battery Replacement**: Year 10-12 at ~$7,000/system

**Current Code**: ~120 lines (lines 560-680 in app.py)

**Calculations Include**:
- Solar generation: `capacity * efficiency * irradiance * system_losses`
- CAPEX: Technology-specific (panel, inverter, BOP costs)
- Diesel fuel escalation: 3%/year baseline fuel cost increase
- Operation & Maintenance: 1% CAPEX/year
- Terminal salvage value: 20% of original CAPEX at year 25

**Issues Identified**:
- ⚠️ Export buttons not functional (buttons present but no data flow)
- ⏳ No sensitivity analysis on key parameters (interest rate, inflation)
- ⏳ Diesel fuel price curve not user-configurable
- ⏳ No Monte Carlo uncertainty quantification

---

## Component Inventory

### **Data Input Components**

| Component | Location | Type | Status | Issue |
|-----------|----------|------|--------|-------|
| File uploader (GeoTIFF) | Data Exploration | Streamlit widget | ✅ Working | Single file only |
| Slider group (5 weights) | MCDA Analysis | Streamlit widgets | ✅ Working | No persistence |
| Zone selector | MCDA Analysis | Dropdown | ✅ Working | Hardcoded zones |
| Technology selector | LCOE Calculator | Dropdown | ✅ Working | Limited options |
| Numeric inputs | LCOE Calculator | Number inputs | ✅ Working | No bounds validation UI |

### **Mapping Components**

| Component | Library | Status | Issue |
|-----------|---------|--------|-------|
| Base map (OpenStreetMap) | Folium | ✅ Working | No layer control |
| Community markers | Folium | ✅ Working | Hardcoded coordinates |
| Aptitude overlay | Matplotlib | ✅ Working | Low resolution PNG only |
| Zone boundaries | (Missing) | ❌ Not implemented | Needed for Phase 1 |

### **Analysis Components**

| Component | Module | Status | Output | Issue |
|-----------|--------|--------|--------|-------|
| Weighted overlay | MCDA engine | ✅ Working | `.npy` + PNG | No bounds validation |
| Sensitivity analysis | MCDA engine | ✅ Working | Line plot | No caching |
| LCOE comparison | LCOE calculator | ✅ Working | Bar chart + table | Export not functional |
| Technology recommendation | LCOE calculator | ✅ Working | Text recommendation | Based on mean irradiance only |

### **Results Components**

| Component | Type | Status | Data Source | Issue |
|-----------|------|--------|-------------|-------|
| Zone summary table | DataFrame display | ✅ Working | Hardcoded | Should read from analysis |
| Technology recommendations | Text + table | ✅ Working | Hardcoded | Should read from MCDA |
| Sensitivity plot | Line chart | ✅ Working | Computed on demand | Should be cached |
| Statistics summary | Metric cards | ✅ Working | Computed | No confidence intervals |

### **Monitoring/Operations Components**

| Component | Feature | Status | Issue |
|-----------|---------|--------|-------|
| Project list | Database query | ✅ Working (separate app) | Not integrated into main dashboard |
| Generation tracking | Time series | ✅ Working (separate app) | Separate Streamlit instance |
| Maintenance log | CRUD operations | ✅ Working (separate app) | Not real-time |
| KPI dashboard | Computed metrics | ✅ Working (separate app) | No alerts/notifications |

---

## Data Flow Architecture

### **Current Data Flow (Session-Based)**

```
User Input
    ↓
Session State (Streamlit)
    ├─→ Weight sliders → Normalized to [0,1]
    ├─→ Files uploaded → Loaded from disk
    └─→ Parameters entered → Stored in session
    ↓
Computation
    ├─→ Load rasters from data/processed/
    ├─→ Normalize each to [0,1]
    ├─→ Compute weighted overlay: Σ(w_i * raster_i)
    ├─→ Generate visualization (PNG)
    └─→ Compute statistics (min, max, mean)
    ↓
Output
    ├─→ Display on page (interactive)
    ├─→ Save to data/processed/ (.npy, .tif)
    └─→ Offer download buttons
```

### **Proposed Data Flow (Database-Backed)**

```
User Input
    ↓
Configuration Store (JSON)
    ├─→ Save analysis parameters
    ├─→ Version control
    └─→ Enable reproducibility
    ↓
Database (PostgreSQL)
    ├─→ Store analysis results
    ├─→ Index zones by aptitude
    ├─→ Track project sites (Phase 1)
    └─→ Archive historical analyses
    ↓
Cache Layer (Redis)
    ├─→ Store computed overlays
    ├─→ Cache sensitivity analysis
    └─→ TTL: 7 days
    ↓
API Endpoint (FastAPI)
    ├─→ Serve analysis results
    ├─→ Support field team mobile access
    └─→ Real-time project status
    ↓
Output
    ├─→ Web dashboard (Streamlit)
    ├─→ Mobile app (PWA)
    └─→ PDF reports (automated)
```

---

## Proposed 6-Page Modular Structure

### **Architecture Diagram**

```
dashboard/
├── __init__.py
├── app.py                              # Main entry point (100 lines)
├── pages/
│   ├── __init__.py
│   ├── home.py                         # 🏠 Home (75 lines)
│   ├── data_layers.py                 # 📊 Data Exploration (80 lines)
│   ├── mcda_config.py                 # 🎯 MCDA Configuration (120 lines)
│   ├── results_viewer.py              # 📈 Results Viewer (90 lines)
│   ├── lcoe_analysis.py               # 💰 LCOE Analysis (100 lines)
│   └── monitoring.py                  # 🔍 Field Monitoring (110 lines) [NEW]
│
├── components/
│   ├── __init__.py
│   ├── metrics_card.py                # KPI display cards
│   ├── map_viewer.py                  # Folium + Plotly map rendering
│   ├── weight_sliders.py              # Weight configuration UI
│   ├── sensitivity_analyzer.py        # Sensitivity computation & plots
│   ├── zone_table.py                  # Zone comparison tables
│   ├── technology_recommender.py      # LCOE + tech selection UI
│   └── gps_tracker.py                 # GPS tracking for field teams [NEW]
│
├── utils/
│   ├── __init__.py
│   ├── session_state.py               # Streamlit session management
│   ├── page_router.py                 # Multi-page routing logic
│   ├── error_handlers.py              # Error handling UI
│   ├── validators_ui.py               # Input validation for UI
│   └── cache_manager.py               # Caching strategy
│
├── styles/
│   ├── __init__.py
│   ├── custom.css                     # Custom Streamlit styling
│   └── colors.py                      # Color scheme definitions
│
└── config/
    ├── defaults.json                  # Default parameters
    └── zones.geojson                  # 3 priority zones (GeoJSON)
```

### **PAGE 1 (REFACTORED): 🏠 Dashboard**

**New Location**: `pages/home.py` (target: <75 lines)

**Components**:
```python
# pages/home.py
import streamlit as st
from components.metrics_card import MetricsCard
from components.map_viewer import MapViewer

def render():
    st.title("🏠 GEESP-Angola Dashboard")
    
    # KPI cards (reusable component)
    MetricsCard([
        {"label": "Critérios", "value": "5"},
        {"label": "Zonas", "value": "3"},
        {"label": "População", "value": "~135k"},
        {"label": "LCOE", "value": "USD 0.18-0.35/kWh"}
    ])
    
    # Map viewer (reusable component)
    st.subheader("📍 Zonas Prioritárias")
    map_obj = MapViewer(
        zones_file="config/zones.geojson",
        style="openstreetmap"
    )
    st.plotly_chart(map_obj.render())
```

**Benefits**:
- ✅ Decoupled from page routing logic
- ✅ Reusable `MetricsCard` component (used on other pages)
- ✅ Map rendering abstracted to `MapViewer` class
- ✅ Easy to test in isolation

---

### **PAGE 2 (REFACTORED): 📊 Data Layers**

**New Location**: `pages/data_layers.py` (target: <80 lines)

**Key Changes**:
- Move file upload to persistent session state
- Add bounds validation
- Display projection info
- Add batch upload support

```python
# pages/data_layers.py
import streamlit as st
import pandas as pd
from components.map_viewer import MapViewer
from utils.validators_ui import validate_raster

def render():
    st.title("📊 Camadas de Dados")
    
    uploaded_file = st.file_uploader("Carregar GeoTIFF", type=["tif", "tiff"])
    
    if uploaded_file:
        # Validate raster
        raster, meta = validate_raster(uploaded_file)
        
        # Display metadata
        st.info(f"✓ Projeção: {meta['crs']}")
        st.info(f"✓ Resolução: {meta['resolution']} m")
        
        # Statistics
        df_stats = pd.DataFrame({
            "Min": [raster.min()],
            "Max": [raster.max()],
            "Mean": [raster.mean()],
            "StdDev": [raster.std()]
        })
        st.dataframe(df_stats)
        
        # Visualization
        fig = plot_distribution(raster)
        st.plotly_chart(fig)
```

---

### **PAGE 3 (REFACTORED): 🎯 MCDA Configuration**

**New Location**: `pages/mcda_config.py` (target: <120 lines)

**Key Changes**:
- Extract weight sliders to reusable component
- Add AHP matrix editor (interactive)
- Add optimization button (auto-generate weights from AHP)
- Persist weights to config.json

```python
# pages/mcda_config.py
from components.weight_sliders import WeightSliders
from components.sensitivity_analyzer import SensitivityAnalyzer

def render():
    st.title("🎯 Configuração MCDA")
    
    # Weight configuration (reusable component)
    weights = WeightSliders(
        criteria=["Irradiação", "Demanda", "Acesso", "Infra", "Uso Solo"],
        defaults=[0.25, 0.25, 0.20, 0.15, 0.15]
    )
    
    # AHP matrix (interactive)
    if st.checkbox("Editar matriz AHP"):
        st.subheader("Matriz de Comparação Pareada (Saaty)")
        matrix = render_ahp_matrix_editor()
        
        if st.button("Calcular pesos via AHP"):
            weights = compute_ahp_weights(matrix)
    
    # Sensitivity analysis
    SensitivityAnalyzer(
        weights=weights,
        rasters_dir="data/processed/"
    ).render()
```

---

### **PAGE 4 (REFACTORED): 📈 Results Viewer**

**New Location**: `pages/results_viewer.py` (target: <90 lines)

**Key Changes**:
- Read results from database instead of hardcoding
- Add zone ranking table (sortable, filterable)
- Add export buttons (functional)
- Add confidence interval visualization

```python
# pages/results_viewer.py
from components.zone_table import ZoneTable
from components.map_viewer import MapViewer

def render():
    st.title("📈 Visualizador de Resultados")
    
    # Load latest analysis
    analysis = st.session_state.get("current_analysis")
    
    if analysis:
        # Zone table (reusable component)
        ZoneTable(analysis["zones"]).render()
        
        # Aptitude map
        map_viewer = MapViewer(
            overlay_path=analysis["aptitude_map"],
            cmap="viridis"
        )
        st.plotly_chart(map_viewer.render())
        
        # Export
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📥 Baixar CSV",
                data=analysis["zones"].to_csv(),
                file_name="zonas.csv"
            )
```

---

### **PAGE 5 (REFACTORED): 💰 LCOE Analysis**

**New Location**: `pages/lcoe_analysis.py` (target: <100 lines)

**Key Changes**:
- Extract parameter inputs to reusable component
- Make export buttons functional
- Add Monte Carlo uncertainty quantification
- Add sensitivity tornado chart

```python
# pages/lcoe_analysis.py
from components.technology_recommender import TechRecommender

def render():
    st.title("💰 Análise de LCOE")
    
    # Input parameters (simplified via component)
    params = TechRecommender().get_parameters()
    
    if st.button("Calcular"):
        results = compute_lcoe(params)
        
        # Display results
        fig_bar = plot_lcoe_comparison(results)
        st.plotly_chart(fig_bar)
        
        # Sensitivity (new)
        fig_tornado = plot_sensitivity_tornado(results)
        st.plotly_chart(fig_tornado)
        
        # Export (functional)
        st.download_button(
            "📥 Baixar Excel",
            data=export_to_excel(results),
            file_name="lcoe_analysis.xlsx"
        )
```

---

### **PAGE 6 (NEW): 🔍 Field Monitoring**

**New Location**: `pages/monitoring.py` (target: <110 lines)

**Purpose**: Real-time Phase 1 field validation dashboard

**Components**:
```python
# pages/monitoring.py
from components.gps_tracker import GPSTracker
from models.monitoring import ProjectRepository

def render():
    st.title("🔍 Monitoramento de Campo")
    
    # Project selection
    projects = ProjectRepository().get_all()
    selected = st.selectbox("Selecionar projeto", projects)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # GPS tracking map
        GPSTracker(selected).render_map()
        
        # Team checklist
        st.subheader("✅ Checklist de Baseline")
        st.checkbox("GPS validação")
        st.checkbox("Foto terreno")
        st.checkbox("Entrevista comunitária")
        st.checkbox("Medição solar/DEM")
    
    with col2:
        # Real-time data
        st.subheader("📊 Dados em Tempo Real")
        render_live_metrics(selected)
        
        # Alert notifications
        st.info("✓ Equipa B status: Humpata (12:34)")
```

---

## Testing & Performance

### **Component-Level Tests** (Proposed)

```python
# tests/test_components.py
import pytest
from dashboard.components.metrics_card import MetricsCard
from dashboard.components.weight_sliders import WeightSliders

def test_metrics_card_render():
    """Test metrics card component rendering"""
    card = MetricsCard([{"label": "Test", "value": "123"}])
    assert card.render() is not None

def test_weight_sliders_normalization():
    """Test that weights sum to 1.0"""
    sliders = WeightSliders(
        criteria=["A", "B", "C"],
        defaults=[0.3, 0.3, 0.4]
    )
    assert sum(sliders.get_weights().values()) == 1.0

def test_invalid_raster_validation():
    """Test that invalid rasters are rejected"""
    with pytest.raises(ValueError):
        validate_raster("invalid.txt")
```

### **Page-Level Tests** (Proposed)

```python
# tests/test_pages.py
from streamlit.testing.v1 import AppTest

def test_home_page_load():
    """Test home page loads without errors"""
    at = AppTest.from_file("dashboard/pages/home.py")
    at.run()
    assert not at.exception

def test_mcda_analysis_produces_overlay():
    """Test MCDA analysis produces valid output"""
    at = AppTest.from_file("dashboard/pages/mcda_config.py")
    at.run()
    # Assert output files created
    assert Path("data/processed/mapa_aptidao_integrada.npy").exists()
```

### **Performance Benchmarks** (Current vs. Target)

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **Dashboard Load Time** | ~5 sec | <3 sec | -40% |
| **MCDA Computation** | ~8 sec | <5 sec | -37% |
| **Sensitivity Analysis** | ~12 sec | <8 sec (cached) | -33% |
| **Map Rendering** | ~2 sec | <1 sec | -50% |
| **Total Session Startup** | ~15 sec | <10 sec | -33% |

**Optimization Strategies**:
1. **Caching**: Redis (7-day TTL on overlays)
2. **Lazy Loading**: Tiles for maps
3. **Vectorization**: NumPy operations
4. **Pre-computation**: Pre-generate common scenarios

---

## Implementation Roadmap

### **Phase 2: Important Improvements (30 Hours)**

**Task 1: Test Coverage Expansion (12 hours)**
- [ ] Component-level tests (5 hrs)
- [ ] Page-level tests (5 hrs)
- [ ] Integration tests (2 hrs)
- **Target Coverage**: 20% → 70%

**Task 2: Modular Dashboard Refactoring (10 hours)**
- [ ] Create `components/` directory (1 hr)
- [ ] Create `pages/` directory (1 hr)
- [ ] Refactor 5 pages into separate files (5 hrs)
- [ ] Create `page_router.py` for navigation (2 hrs)
- [ ] Create `session_state.py` for state management (1 hr)
- **Target Structure**: Monolithic → 6 modular pages (<100 lines each)

**Task 3: Code Deduplication (8 hours)**
- [ ] Extract common plotting functions (2 hrs)
- [ ] Centralize error handling (2 hrs)
- [ ] Consolidate data loading (2 hrs)
- [ ] Extract configuration access (2 hrs)
- **Target Duplication**: 15% → <5%

### **Phase 3: Nice-to-Have Improvements (20 Hours)**

**Task 1: Performance Optimization (8 hours)**
- [ ] Implement Redis caching (3 hrs)
- [ ] Optimize map rendering (2 hrs)
- [ ] Vectorize MCDA computation (2 hrs)
- [ ] Implement lazy loading (1 hr)
- **Target Load Time**: ~5 sec → <3 sec

**Task 2: Database Integration (8 hours)**
- [ ] Design PostgreSQL schema (2 hrs)
- [ ] Implement SQLAlchemy ORM (3 hrs)
- [ ] Create result persistence (2 hrs)
- [ ] Implement query interface (1 hr)

**Task 3: Monitoring Integration (4 hours)**
- [ ] Integrate GPS tracking component (2 hrs)
- [ ] Add real-time notifications (1.5 hrs)
- [ ] Create baseline checklist UI (0.5 hrs)

### **Success Criteria**

- ✅ Dashboard loads in <3 seconds
- ✅ 70% code test coverage achieved
- ✅ Each page <100 lines of code
- ✅ <5% code duplication
- ✅ All export buttons functional
- ✅ Database persistence working
- ✅ Real-time monitoring available

### **Timeline**

| Phase | Duration | Hours | Start | End |
|-------|----------|-------|-------|-----|
| Current Phase 1 | 1 week | 8/20 | Feb 9 | Feb 12 |
| Phase 2 (Refactoring) | 2-3 weeks | 30 | Feb 13 | Mar 5 |
| Phase 3 (Optimization) | 2-3 weeks | 20 | Mar 6 | Apr 2 |
| **Total** | **6-8 weeks** | **70** | **Feb 9** | **Apr 2** |

---

## Integration with Phase 1 Field Validation

### **Field Team Requirements**

The 6th dashboard page (`monitoring.py`) will support Phase 1 fieldwork with:

1. **GPS Validation**
   - Real-time field team location tracking (Mapbox GL)
   - Automatic comparison to predicted aptitude zones
   - Alert if team outside priority zone buffer

2. **Baseline Data Collection**
   - Interactive checklist (GPS photo, interview, measurements)
   - Offline-capable mobile form (PWA)
   - Automatic sync when connectivity returns

3. **Site Adjustment**
   - Ability to mark invalid sites (security concerns, accessibility)
   - Automatic re-prioritization based on field feedback
   - Real-time zone rank updates

4. **Impact Tracking**
   - Population verified (camera + GPS)
   - Technical constraints documented (photos)
   - Community interest collected (survey data)

---

## Continuation Priority

**For Boston Presentation (Feb 15)**:
- [ ] Dashboard component architecture diagram (this document ✓)
- [ ] Mockups of monitoring page (in progress)
- [ ] Integration roadmap with Phase 1 timeline

**For MINEA Stakeholder Briefing (Feb 16-17)**:
- [ ] Operational requirements from Phase 1 (ask MINEA team)
- [ ] Real-time monitoring capabilities demo
- [ ] Field team training module

**For Production Deployment (Mar 5)**:
- [ ] Modularization complete (Phase 2)
- [ ] 70% test coverage achieved
- [ ] Performance targets met
- [ ] Database integrated

---

## Questions for Stakeholder Alignment

1. **Data Persistence**: Should results persist in database or stay ephemeral?
2. **Mobile Access**: Does Phase 1 team need full dashboard on phone or just checklist?
3. **Export Formats**: PDF reports required? Or CSV sufficient?
4. **Real-Time Updates**: Should dashboard auto-refresh field data or require manual refresh?
5. **Offline Capability**: Should monitoring app work offline with sync on reconnect?

---

**Document Version**: 1.0
**Last Updated**: 2026-02-12
**Author**: AI Assistant (GitHub Copilot)
**Status**: Final Specification Ready for Review
