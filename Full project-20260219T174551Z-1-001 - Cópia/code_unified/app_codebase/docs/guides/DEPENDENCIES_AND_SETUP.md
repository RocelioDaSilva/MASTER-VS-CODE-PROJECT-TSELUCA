# GEESP-Angola: Complete Dependencies & Setup Guide

**Date:** March 3, 2026  
**Version:** 1.0  
**Python Required:** 3.10+

---

## 📋 Part 1: All Dependencies (48 Packages)

### INSTALLATION OPTIONS

**Option A: Full Installation (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: App-Only (Minimal)**
```bash
pip install -r requirements-app.txt
```

**Option C: Interactive Setup Wizard**
```bash
python SETUP_WIZARD.py
```

---

## 📦 Complete Dependency List (Organized by Category)

### 1. **Core Data Processing** (4 packages)
Essential for numerical operations and data manipulation
```
numpy>=1.21.0           # Numerical array operations
pandas>=1.3.0           # Tabular data processing
scipy>=1.7.0            # Scientific computing
scikit-learn>=0.24.0    # Machine learning utilities
```

### 2. **Geospatial & Remote Sensing** (5 packages)
For working with maps and satellite data
```
rasterio>=1.2.0         # Read/write GeoTIFF rasters
geopandas>=0.9.0        # Geographic dataframes
shapely>=1.7.0          # Geometric operations
pyproj>=3.1.0           # Coordinate transformations
rioxarray>=0.11.0       # Raster I/O with xarray
```

### 3. **Google Earth Engine** (1 package)
Access to satellite data and Earth Engine API
```
earthengine-api>=0.1.300  # GEE Python client
```

### 4. **Visualization & Dashboard** (6 packages)
Create interactive web interface and charts
```
streamlit>=1.30.0         # Web dashboard framework
folium>=0.14.0           # Interactive maps
streamlit-folium>=0.16.0  # Streamlit + Folium integration
matplotlib>=3.4.0        # Static plotting
plotly>=5.0.0            # Interactive charts
seaborn>=0.11.0          # Statistical visualization
```

### 5. **Tabular Data & Reports** (3 packages)
Generate reports and export data
```
openpyxl>=3.7.0         # Excel file handling
python-docx>=0.8.10     # Word document generation
reportlab>=3.6.0        # PDF creation
```

### 6. **Utilities & Configuration** (5 packages)
General helper functions
```
requests>=2.26.0        # HTTP client
python-dotenv>=0.19.0   # Load .env files
pyyaml>=5.4.0           # YAML parsing
tqdm>=4.62.0            # Progress bars
Pillow>=9.0.0           # Image processing
```

### 7. **API & Web Server** (2 packages)
REST API backend (optional)
```
fastapi>=0.95.0         # Modern web framework
uvicorn>=0.22.0         # ASGI server
```

### 8. **Development & Testing** (5 packages)
For code quality and testing
```
jupyter>=1.0.0          # Jupyter notebooks
ipython>=7.25.0         # Interactive Python shell
black>=21.7b0           # Code formatter
flake8>=3.9.0           # Linter
pytest>=6.2.0           # Testing framework
```

---

## 🚀 Part 2: Installation Steps

### Step 1: Verify Python Version

**Windows (PowerShell):**
```powershell
python --version  # Should show Python 3.10 or higher
```

**Linux/macOS:**
```bash
python3 --version
```

**Expected output:** `Python 3.10.x` or higher

If not installed, download from: https://www.python.org/downloads/

---

### Step 2: Install Dependencies

**Option A: Using SETUP_WIZARD.py (Recommended)**

```bash
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"

python SETUP_WIZARD.py
# Select option 2 or 5 to install dependencies
```

**Option B: Direct pip Installation**

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install full dependencies
pip install -r requirements.txt

# OR install app-only (smaller)
pip install -r requirements-app.txt
```

**Expected output:**
```
Successfully installed numpy-1.24.3 pandas-2.0.2 ... (and 46 more)
```

**Time required:** 5-15 minutes (depending on internet speed)

---

### Step 3: Verify Installation

```bash
# Test core imports
python -c "import streamlit; import numpy; import geopandas; print('✓ All core packages installed')"
```

If successful, output will be: `✓ All core packages installed`

---

## 🔑 Part 3: Google Earth Engine Authentication

### Why Earth Engine?
The code uses Earth Engine to download satellite data for:
- Solar irradiance (NASA POWER)
- Population density (WorldPop/VIIRS)
- Vegetation index (Sentinel-2/MODIS)
- Nighttime lights (VIIRS)

### Complete Setup Process

#### A. Create Google Cloud Project

1. Open: https://console.cloud.google.com/
2. Click **Select Project** (top-left)
3. Click **New Project**
4. Name: `GEESP-Angola`
5. Click **Create** (wait 1-2 minutes)

#### B. Enable Earth Engine API

1. In GCP Console, search for: `Earth Engine API`
2. Click **Enable**
3. Wait for activation (1-2 minutes)

#### C. Create Service Account

1. Go to: **APIs & Services > Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in:
   - Service account name: `geesp-app`
   - Service account ID: (auto-filled)
4. Click **Create and Continue**
5. Grant role: Select **Editor**
6. Click **Continue**
7. Click **Create Key**
8. Select **JSON** format
9. Click **Create** (downloads `xxxxx.json`)

#### D. Save Credentials Locally

1. Move downloaded JSON file to project folder:
   ```
   geesp-angola/geesp-credentials.json
   ```

2. Verify file exists:
   ```powershell
   Test-Path "geesp-angola\geesp-credentials.json"
   # Should output: True
   ```

#### E. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola\geesp-credentials.json"

# Verify
$env:GOOGLE_APPLICATION_CREDENTIALS
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\geesp-credentials.json
```

**Linux/macOS:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/geesp-credentials.json"
```

#### F. Test Authentication

```bash
python -c "import ee; ee.Initialize(); print('✅ Earth Engine authenticated!')"
```

If successful: `✅ Earth Engine authenticated!`

---

## 🗺️ Part 4: Generate Synthetic Test Maps

### Option A: Quick Generation (Fastest)

```bash
cd geesp-angola
python generate_synthetic_maps_quick.py
```

**Output:**
```
================================================================================
GEESP-ANGOLA: SYNTHETIC TEST MAP GENERATOR
================================================================================

☀️  Solar Irradiance (GHI)
  File: mapa_irradiacao.npy
  Range: 3.5 - 5.5 kWh/m²/day
  Size: 500×500 pixels (1.0 MB)
  Data stats: min=3.50, max=5.50, mean=4.50

👥 Population Density (VIIRS)
  File: mapa_populacao.npy
  ...

✅ Successfully generated 6 synthetic maps in: data/processed
```

### Option B: Using SETUP_WIZARD

```bash
python SETUP_WIZARD.py
# Select option 4 or 5
```

### What Gets Generated?

| Map | File Name | Description | Range | Size |
|-----|-----------|-------------|-------|------|
| ☀️ Solar | `mapa_irradiacao.npy` | Solar GHI | 3.5-5.5 kWh/m²/day | 1.0 MB |
| ⛰️ Slope | `mapa_declividade.npy` | Terrain | 0-45° | 1.0 MB |
| 👥 Population | `mapa_populacao.npy` | Density | 10-500 people/km² | 1.0 MB |
| 🔌 Grid | `mapa_distanciarede.npy` | Distance | 5-50 km | 1.0 MB |
| 🌱 NDVI | `mapa_ndvi.npy` | Vegetation | 0-1 index | 1.0 MB |
| 🌙 Nightlights | `mapa_luminosidade_noturna.npy` | Electrification | 0-100 radiance | 1.0 MB |

**Total size:** ~6 MB for all test maps

---

## 📝 Part 5: Create Configuration File

Create `geesp-angola/.env`:

```bash
# Windows PowerShell
@"
# GEESP-Angola Configuration
ENV=development
LOG_LEVEL=INFO

# Google Earth Engine
GOOGLE_APPLICATION_CREDENTIALS=./geesp-credentials.json
GEE_PROJECT_ID=your-project-id

# Data paths
DATA_DIR=./data/processed
GEE_EXPORTS_DIR=./data/gee_exports

# Default MCDA Weights (6 criteria)
DEFAULT_WEIGHT_SOLAR=0.25
DEFAULT_WEIGHT_POPULATION=0.25
DEFAULT_WEIGHT_DISTANCE=0.20
DEFAULT_WEIGHT_SLOPE=0.15
DEFAULT_WEIGHT_NDVI=0.15
DEFAULT_WEIGHT_NIGHTLIGHTS=0.10
"@ > .env
```

---

## ✅ Part 6: Verification Checklist

Run this to verify everything is set up:

```bash
python SETUP_WIZARD.py
# Select option 6
```

**Verification includes:**
- ✅ Python version (3.10+)
- ✅ Core packages (streamlit, numpy, pandas, rasterio, geopandas, plotly)
- ✅ Data directory with 6 .npy files
- ✅ .env configuration file

---

## 🎯 Quick Start (After Setup)

```bash
# Navigate to project
cd "c:\Users\rocel\OneDrive\Desktop\Full project-20260219T174551Z-1-001 - Cópia\MIT-SCIENCE-PAPER\Full project\02_Code\geesp-angola"

# Launch dashboard
streamlit run geesp_unified_app.py

# Opens automatically in browser at: http://localhost:8501
```

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit>=1.30.0
```

---

### Issue: "GDAL library not found" (on Windows)

**Solution:** Install OSGeo4W
1. Download: https://trac.osgeo.org/osgeo4w/
2. Run installer
3. Select GDAL when prompted

Or use pre-built wheels:
```bash
pip install --upgrade rasterio
```

---

### Issue: "Earth Engine authentication failed"

**Solution:**
1. Verify credentials file exists: `geesp-credentials.json`
2. Check environment variable is set
3. Reinitialize: `earthengine authenticate`
4. Follow OAuth prompt in browser

---

### Issue: "No map files found"

**Solution:**
```bash
python generate_synthetic_maps_quick.py
```

---

## 📊 Installation Summary

| Component | Status | Command |
|-----------|--------|---------|
| **Dependencies** | ✅ | `pip install -r requirements.txt` |
| **Earth Engine** | ✅ | Download credentials + set env var |
| **Synthetic Maps** | ✅ | `python generate_synthetic_maps_quick.py` |
| **Config** | ✅ | Create `.env` file |
| **Launch** | ✅ | `streamlit run geesp_unified_app.py` |

---

## 🚀 Next Step

After completing setup, run:

```bash
streamlit run geesp_unified_app.py
```

**Expected browser output:**
```
Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

Dashboard features:
- 🗺️ Map generation (6 layers)
- 🎯 MCDA analysis (weighted overlay)
- 💰 LCOE calculator (financial analysis)
- 📊 Monitoring dashboard (project tracking)
- ⚙️ Configuration management

---

## 📞 Support

| Issue | Resource |
|-------|----------|
| **Streamlit docs** | https://docs.streamlit.io |
| **Earth Engine docs** | https://developers.google.com/earth-engine |
| **GDAL installation** | https://gdal.org/download.html |
| **Project manuscript** | `01_Science/manuscript/SOL.tex` |

---

**Setup Complete! Ready to analyze solar sites for Angola. 🌍⚡**

