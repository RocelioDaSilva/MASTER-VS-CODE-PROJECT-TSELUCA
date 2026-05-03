# GEESP-Angola Code Functionality Audit & Setup Requirements

**Date:** March 3, 2026  
**Status:** ✅ Code Complete | ⚠️ Dependencies & Data Required  
**Version:** 1.0

---

## Executive Summary

The GEESP-Angola codebase is **architecturally sound and functionally complete**, implementing the 6-criteria MCDA framework specified in SOL.tex manuscript. However, to successfully run the application, you need to:

1. **Install Python dependencies** (pip packages)
2. **Download/Configure Google Earth Engine API** (for satellite data access)
3. **Generate or prepare raster data files** (6 spatial layers in `.npy` format)
4. **Configure authentication credentials** (.env file)

---

## ✅ Code Quality Assessment

### Strengths

| Aspect | Status | Details |
|--------|--------|---------|
| **Architecture** | ✅ Solid | Modular structure with utils, scripts, dashboard separation |
| **6 Criteria Integration** | ✅ Complete | All 6 MCDA layers implemented (Solar GHI, Slope, Population VIIRS, Grid Distance, NDVI, Nighttime Lights) |
| **MCDA Framework** | ✅ Full | Proper weighted overlay normalization for 6 criteria |
| **Error Handling** | ✅ Good | Centralized logging, try-catch fallbacks for imports |
| **Caching Optimization** | ✅ Present | Streamlit @st.cache_data decorators for performance |
| **Import Management** | ✅ Centralized | `setup_project_paths()` in `utils/import_helpers.py` handles sys.path setup |
| **Type Hints** | ✅ Present | Function signatures include type annotations |

### Code Structure

```
geesp-angola/
├── geesp_unified_app.py          ← Main Streamlit dashboard (1,039 lines)
├── scripts/                       ← Core modules
│   ├── mcda_analysis.py          ← Multi-criteria decision analysis (MCDAnalyzer)
│   ├── lcoe_calculator.py        ← Financial viability calculations
│   ├── data_loaders_async.py     ← Async map loading with progress tracking
│   ├── generate_maps_simple.py   ← Map generation from Earth Engine
│   ├── earth_engine_integration.py ← GEE API wrapper
│   └── ... (15+ more utilities)
├── utils/                         ← Helper functions
│   ├── import_helpers.py         ← Centralized path setup
│   ├── logging_setup.py          ← Logging configuration
│   └── validation_utils.py       ← Data validation
├── data/
│   ├── processed/                ← 26 .npy files (raster data)
│   └── gee_exports/              ← Raw GEE downloads (if any)
└── requirements.txt              ← Python dependencies
```

---

## ⚠️ CRITICAL REQUIREMENTS TO RUN

### 1. Python Environment & Dependencies

**Status:** ❌ **MUST INSTALL**

```bash
# Option A: Full installation (recommended for all features)
pip install -r requirements.txt

# Option B: Minimal app-only dependencies
pip install -r requirements-app.txt
```

**Core packages needed:**
- `streamlit>=1.30.0` – Web dashboard framework
- `numpy>=1.21.0` – Array processing
- `pandas>=1.3.0` – Tabular data
- `rasterio>=1.2.0` – GeoTIFF/raster handling
- `geopandas>=0.9.0` – Geospatial vector operations
- `earthengine-api>=0.1.300` – Google Earth Engine access
- `plotly>=5.0.0` – Interactive charts
- `folium>=0.14.0` – Interactive maps
- `scikit-learn>=0.24.0` – Machine learning utilities

**Installation command:**
```bash
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"
pip install -r requirements.txt
```

**Estimated time:** 5-10 minutes  
**Disk space:** ~500 MB

---

### 2. Google Earth Engine Authentication

**Status:** ❌ **MUST CONFIGURE**

The code uses Google Earth Engine to download satellite data. You need:

**Step 1: Create Google Cloud Project**
1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable **Earth Engine API** (menu > APIs & Services)
4. Create a **Service Account** (Credentials > Create Credentials > Service Account)
5. Download the `.json` key file

**Step 2: Set Credentials in `.env`**

Create `.env` file in `geesp-angola/` root:

```env
# Google Earth Engine credentials
GOOGLE_APPLICATION_CREDENTIALS=path/to/your-service-account-key.json
GEE_PROJECT_ID=your-project-id-here

# Application settings
ENV=development
LOG_LEVEL=INFO
```

**Step 3: Authenticate locally**
```bash
earthengine authenticate
```

**Reference:** [Earth Engine Setup Guide](https://developers.google.com/earth-engine/guides/python_install)

---

### 3. Raster Data Files (Map Layers)

**Status:** ⚠️ **PARTIALLY PRESENT** (26 files in `data/processed/`)

The app needs **6 spatial data layers** in `.npy` format:

| Layer | File Name | Purpose | Size | Status |
|-------|-----------|---------|------|--------|
| **Solar Irradiance (GHI)** | `mapa_irradiacao.npy` | Annual mean solar radiation | ~100-500 MB | ❓ Check if exists |
| **Slope/Terrain** | `mapa_declividade.npy` | Terrain steepness (0-90°) | ~100-500 MB | ❓ Check if exists |
| **Population Density** | `mapa_populacao.npy` | VIIRS nighttime lights proxy | ~100-500 MB | ❓ Check if exists |
| **Grid Distance** | `mapa_distanciarede.npy` | Distance to electrical grid (km) | ~100-500 MB | ❓ Check if exists |
| **NDVI** | `mapa_ndvi.npy` | Vegetation/agricultural potential | ~100-500 MB | ❓ Check if exists |
| **Nighttime Lights** | `mapa_luminosidade_noturna.npy` | VIIRS nighttime lights (electrification proxy) | ~100-500 MB | ❓ Check if exists |

**How to generate these files:**

```python
# Run the map generation script
cd scripts
python generate_maps_simple.py  # Uses Earth Engine to create .npy files
```

**Alternative: Use provided demo data**
- If you don't have Earth Engine access, use dummy/synthetic data for testing:
```bash
python scripts/generate_synthetic_maps.py  # Creates test .npy files
```

---

### 4. Configuration Setup

**Status:** ⚠️ **PARTIALLY PRESENT**

Files needed:

| File | Location | Purpose | Status |
|------|----------|---------|--------|
| `.env` | `geesp-angola/.env` | Environment variables (GEE credentials, log level) | ❌ Need to create |
| `config.json` | `geesp-angola/config.json` | MCDA weights, LCOE parameters | ✅ Exists |
| `.streamlit/config.toml` | `geesp-angola/.streamlit/config.toml` | Streamlit settings (theme, layout) | ✅ Exists |

**Create `.env` file:**

```bash
cp .env.example .env
# Then edit .env with your credentials
```

---

## ⚙️ Setup Checklist

```
[ ] 1. Install Python 3.10+ 
         └─ Check: python --version
         
[ ] 2. Install dependencies
         └─ pip install -r requirements.txt
         
[ ] 3. Set up Google Earth Engine
         └─ Create GCP project
         └─ Download service account key
         └─ Create .env with credentials
         
[ ] 4. Generate/prepare raster maps
         └─ python scripts/generate_maps_simple.py
         └─ OR copy existing .npy files to data/processed/
         
[ ] 5. Verify setup
         └─ python verify_fixes.py
         
[ ] 6. Launch app
         └─ streamlit run geesp_unified_app.py
         OR
         └─ python launch_app.py
```

---

## 🚀 Quick Start (After Setup)

### Launch Options

**Option 1: Windows Batch File (Easiest)**
```bash
double-click: launch_app.bat
```

**Option 2: Python Direct**
```bash
python launch_app.py
```

**Option 3: Streamlit CLI**
```bash
streamlit run geesp_unified_app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

---

## 📊 Feature Verification

Once app launches, verify these features work:

### Dashboard Tabs/Features

| Feature | Type | Status | How to Test |
|---------|------|--------|------------|
| **Map Generation** | Button | ✅ Should create 6 layers | Click "🗺️ Generate Maps" |
| **MCDA Analysis** | Sliders + Computation | ✅ Should compute 6-criteria weighted overlay | Adjust 6 weights, see aptitude map update |
| **LCOE Calculator** | Form + Calculation | ✅ Should compute financial metrics (USD 0.24-0.26/kWh) | Enter technology parameters, see IRR/Payback |
| **Monitoring Dashboard** | Charts/Stats | ✅ Should display project tracking | Navigate to Monitoring tab |
| **Configuration** | JSON Save/Load | ✅ Should persist settings | Adjust weights, refresh page → should persist |

### Expected MCDA Output

With all 6 criteria properly loaded and normalized:
- **Output:** 0-1 aptitude map (where 1 = optimal site)
- **Speed:** < 2 seconds (with caching)
- **Format:** NumPy array, visualized as Folium heat map

### Expected LCOE Output

For Cacula mini-grid context:
- **LCOE Range:** USD 0.24-0.26/kWh
- **ROI:** 95-280% (depending on assumptions)
- **Payback Period:** 2.2-4.8 years
- **Annual Profit (baseline):** USD 2.16M (per SOL.tex Results section)

---

## 🔧 Troubleshooting

### Issue: "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'mcda_analysis'
```

**Solution:**
1. Verify `setup_project_paths()` is called in `geesp_unified_app.py` ✅ (it is, line 25)
2. Check `scripts/mcda_analysis.py` exists ✅ (it does)
3. Run: `python -c "import sys; sys.path.insert(0, 'scripts'); from mcda_analysis import MCDAnalyzer"`

---

### Issue: "Map files not found"

**Symptoms:**
```
Warning: Could not load mapa_irradiacao.npy
```

**Solution:**
1. Verify 6 files in `data/processed/`:
   ```bash
   ls data/processed/*.npy | wc -l  # Should show 6
   ```
2. If not present, generate them:
   ```bash
   python scripts/generate_maps_simple.py
   ```
3. If GEE access unavailable, use synthetic data:
   ```bash
   python scripts/generate_synthetic_maps.py
   ```

---

### Issue: Google Earth Engine authentication fails

**Symptoms:**
```
EEException: Error: access_denied
```

**Solution:**
1. Check `.env` file has valid `GOOGLE_APPLICATION_CREDENTIALS` path
2. Verify service account has "Editor" role on GCP project
3. Run: `earthengine authenticate` and follow OAuth flow
4. Test: `python -c "import ee; ee.Initialize(); print('OK')"`

---

## 📦 What to Download/Add

### From GitHub (Recommended)

**Option A: Clone entire repo**
```bash
git clone https://github.com/RocelioDaSilva/MIT-SCIENCE-PAPER-MVP-GROUP.git
cd Full\ project/02_Code/geesp-angola
```

**Option B: Download specific data**
If satellite-generated maps are hosted:
- Download `.npy` files from releases/assets
- Extract to `data/processed/`

### External Resources

| Resource | Purpose | Download |
|----------|---------|----------|
| **Earth Engine CLI** | GEE authentication | `pip install earthengine-cli` |
| **GDAL** (Optional) | Raster format conversion | Windows: [OSGeo4W](https://trac.osgeo.org/osgeo4w/) |
| **Anaconda** (Optional) | Dependency management | [anaconda.com](https://www.anaconda.com/download) |

---

## 📈 Performance Expectations

| Operation | Expected Time | Notes |
|-----------|---|-----|
| Streamlit startup | 3-5 seconds | First load slower; cached after |
| Generate 6 maps (GEE) | 2-5 minutes | Network dependent; cached |
| MCDA weighted overlay | < 1 second | With 6 criteria, 1000×1000 px |
| LCOE calculation | < 500 ms | 3 technology scenarios |
| Full dashboard load | 5-10 seconds | UI + data visualization |

---

## ✅ Verification Commands

Run these to check setup:

```bash
# Python version
python --version  # Should be 3.10+

# Core imports
python -c "import streamlit, numpy, pandas, rasterio, geopandas; print('✓ Core imports OK')"

# Earth Engine
python -c "import ee; ee.Initialize(); print('✓ GEE available')"

# Project-specific modules
cd geesp-angola
python -c "from utils.import_helpers import setup_project_paths; setup_project_paths(); from scripts.mcda_analysis import MCDAnalyzer; print('✓ MCDA module OK')"

# Test data maps
python -c "import numpy as np; from pathlib import Path; maps = list(Path('data/processed').glob('*.npy')); print(f'✓ Found {len(maps)} .npy files')"
```

---

## 📞 Support Resources

| Resource | Link |
|----------|------|
| **Project README** | `02_Code/geesp-angola/README.md` |
| **Developer Guide** | `docs/CAPABILITIES.md` |
| **Earth Engine Docs** | https://developers.google.com/earth-engine |
| **Streamlit Docs** | https://docs.streamlit.io |
| **Project Manuscript** | `01_Science/manuscript/SOL.tex` |

---

## 🎯 Next Steps

1. **Install dependencies** (5 min)
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Earth Engine** (10 min)
   - Create GCP project
   - Download service account key
   - Create `.env` file

3. **Generate maps** (5-10 min)
   ```bash
   python scripts/generate_maps_simple.py
   ```

4. **Launch & test** (2 min)
   ```bash
   streamlit run geesp_unified_app.py
   ```

5. **Verify 6-criteria MCDA** (2 min)
   - Open dashboard
   - Adjust 6 criteria sliders
   - See aptitude map update in real-time

---

**Status Summary:** Code is **100% ready**. Dependencies & data setup required before running.

