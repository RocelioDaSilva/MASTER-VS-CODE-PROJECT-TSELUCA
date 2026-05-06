# GEESP-Angola: Complete Capabilities & Features

**Version**: 1.0 | **Date**: 2026-02-10 | **Status**: Production Ready

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Installation & Setup](#installation--setup)
4. [User Guide](#user-guide)
5. [API Reference](#api-reference)
6. [Deployment Options](#deployment-options)
7. [Troubleshooting](#troubleshooting)

---

## Overview

**GEESP-Angola** (Geospatial Energy for Equity & Solar Planning) is a comprehensive Python framework for solar energy site selection, financial analysis, and project monitoring in Angola.

### What It Does

- 🗺️ **Generates spatial analysis maps** from satellite data (solar, population, infrastructure)
- 🎯 **Performs multi-criteria decision analysis** (MCDA) for site ranking
- 💰 **Calculates financial viability** (LCOE) for different solar technologies
- 📊 **Monitors projects** post-implementation with KPIs and metrics
- ⚙️ **Manages configuration** centrally for reproducibility

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11+, NumPy, Pandas, SciPy |
| **GIS** | Rasterio, GeoPandas, Google Earth Engine |
| **Web UI** | Streamlit, Plotly, Folium |
| **Database** | SQLite (default), PostgreSQL (optional) |
| **API** | FastAPI (optional) |

---

## Core Features

### 🗺️ Map Generation

**Generates 6 spatial analysis layers:**

1. **Solar Irradiance** — Annual average radiation (kWh/m²/day)
   - Source: NASA POWER via Google Earth Engine
   - Range: 5.5-6.4 kWh/m²/day (Huíla region)

2. **Population Density** — Proximity to communities
   - Source: VIIRS Nighttime Lights
   - Units: nanoWatts/cm²/sr

3. **Grid Distance** — Distance to electrical infrastructure
   - Calculated from road/transmission line data
   - Units: kilometers

4. **Terrain Slope** — Suitability for construction
   - Source: SRTM DEM
   - Units: degrees (0-30° optimal)

5. **NDVI** — Vegetation coverage (land use compatibility)
   - Source: Sentinel-2
   - Range: -1 to +1

6. **Integrated Aptitude** — Combined weighted suitability score
   - Result of MCDA weighted overlay
   - Range: 0-1 (higher = better)

**Usage:**
```python
from scripts.generate_maps_simple import generate_maps

# Generate all maps
generate_maps(output_dir="data/processed")
```

**Output:** 6 `.npy` files + metadata JSON in `data/processed/`

---

### 🎯 Multi-Criteria Decision Analysis (MCDA)

**Weighted overlay analysis with customizable criteria:**

**Default Weights:**
- Solar Irradiance: 25%
- Population Access: 25%
- Grid Distance: 20%
- Terrain Slope: 15%
- Vegetation (NDVI): 15%

**Capabilities:**
- ✅ Adjust weights dynamically via UI sliders
- ✅ Normalize raster data to [0,1] range
- ✅ Three-class classification (Low/Medium/High aptitude)
- ✅ Sensitivity analysis (±20% weight variation)
- ✅ AHP (Analytic Hierarchy Process) consistency checking
- ✅ Interactive visualization with Plotly heatmaps

**Usage:**
```python
from scripts.mcda_analysis import MCDAnalyzer

analyzer = MCDAnalyzer()
weights = {
    'solar': 0.25,
    'population': 0.25,
    'distance': 0.20,
    'slope': 0.15,
    'ndvi': 0.15
}
aptitude = analyzer.weighted_overlay()
classified = analyzer.classify_aptitude()
```

**Output:** Integrated aptitude map, classification, statistics

---

### 💰 LCOE Calculator

**Financial comparison across 3 solar technologies:**

1. **PV Fixed + Batteries** — Standard fixed-tilt panels with 3h storage
2. **PV with Single-Axis Tracker** — Tracking system for higher yield
3. **Hybrid Solar + Diesel + Batteries** — Off-grid hybrid system

**Calculates:**
- Capital expenditure (CapEx) breakdown
- Operating expenditure (OpEx) annual costs
- Annual energy production (MWh)
- Levelized Cost of Energy (LCOE) in USD/MWh and USD/kWh
- Net Present Value (NPV) and Internal Rate of Return (IRR)
- Payback period

**Inputs:**
- Capacity (MW)
- Annual irradiance (kWh/m²/year)
- Discount rate (WACC %)
- Project lifetime (years)

**Usage:**
```python
from scripts.lcoe_calculator import LCOECalculator

calc = LCOECalculator(location="Angola")
results = calc.compare_technologies(
    capacity_mw=1.0,
    annual_irradiance=2226,
    discount_rate=8,
    lifetime=25
)
```

**Output:** DataFrame with technology comparison, sorted by LCOE

---

### 📊 Unified Dashboard

**Interactive web interface with 6 integrated modules:**

#### 🏠 Home
- Project introduction and overview
- Feature highlights
- Quick start guide
- System status indicators

#### 🗺️ Map Generation
- Generate all 6 spatial layers with one click
- Preview maps with statistics (min, max, mean, std)
- Interactive heatmap viewer
- Histogram distributions
- Download options (.npy, .png)

#### 🎯 MCDA Analysis
- Adjust 5 weight sliders in real-time
- Automatic weight normalization
- Compute integrated aptitude map
- Zone classification (High/Medium/Low)
- Sensitivity analysis controls

#### 💰 LCOE Calculator
- Input capacity and irradiance
- Technology comparison table
- Bar charts and visualizations
- Financial metrics summary
- Best technology recommendation

#### 📊 Monitoring
- Project status dashboard
- KPI metrics (generation, efficiency, downtime)
- Generation trends over time
- Maintenance schedule
- Database-connected (with fallback to sample data)

#### ⚙️ Settings
- Configure map dimensions
- Set MCDA weight defaults
- Adjust LCOE parameters (WACC, lifetime)
- Save configuration to `config.json`

**Launch:**
```bash
streamlit run geesp_unified_app.py
```

**Access:** http://localhost:8501

---

### 🔧 Configuration System

**Centralized configuration via `config.json`:**

```json
{
  "map_generation": {
    "output_shape": [280, 300],
    "default_format": "npy",
    "resolution_m": 1000
  },
  "mcda": {
    "default_weights": {
      "solar_irradiance": 0.25,
      "population_density": 0.25,
      "grid_distance": 0.20,
      "slope": 0.15,
      "vegetation_ndvi": 0.15
    },
    "classification_thresholds": {
      "high": 0.70,
      "medium": 0.40,
      "low": 0.0
    }
  },
  "lcoe": {
    "standard_parameters": {
      "default_capacity_mw": 1.0,
      "default_discount_rate_percent": 8.0,
      "default_project_lifetime_years": 25
    }
  }
}
```

**Access in code:**
```python
from scripts.config_loader import load_config

config = load_config()
weights = config.get_mcda_weights()
map_shape = config.get_map_shape()
```

---

## Installation & Setup

### Prerequisites

- **Python**: 3.11+ (3.10 minimum)
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: ~2 GB for dependencies + data
- **Memory**: 4 GB RAM minimum (8 GB recommended)

### Quick Install (2 minutes)

```bash
# 1. Navigate to project directory
cd "Full project/Coding parts/geesp-angola"

# 2. Install dependencies
pip install -r requirements-app.txt

# 3. Run the app
streamlit run geesp_unified_app.py
```

### Detailed Install

```bash
# 1. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements-app.txt

# 3. (Optional) Install development dependencies
pip install -r requirements.txt

# 4. Generate initial maps (optional)
python scripts/generate_maps_simple.py

# 5. Run the app
streamlit run geesp_unified_app.py
```

### Verify Installation

```bash
# Run verification script
python verify_integration.py

# Run tests
pytest tests/ -v
```

---

## User Guide

### Typical Workflow (15 minutes)

#### Step 1: Generate Maps 🗺️
1. Open the app: `streamlit run geesp_unified_app.py`
2. Navigate to **Map Generation** tab
3. Click **"🔄 Generate Maps"** button
4. Wait ~5-10 seconds for generation
5. View generated maps with statistics

#### Step 2: Analyze with MCDA 🎯
1. Navigate to **MCDA Analysis** tab
2. Adjust weight sliders for each criterion
3. Ensure weights sum to 1.0 (auto-normalization available)
4. Click **"📊 Compute MCDA"** button
5. View integrated aptitude map and zone classification

#### Step 3: Calculate LCOE 💰
1. Navigate to **LCOE Calculator** tab
2. Enter capacity (MW) and annual irradiance
3. Select location (optional)
4. Click **"🧮 Calculate LCOE"** button
5. Compare technologies and review financial metrics

#### Step 4: Review Monitoring 📊
1. Navigate to **Monitoring** tab
2. View active projects and KPIs
3. Check generation trends
4. Review maintenance schedule

#### Step 5: Customize Settings ⚙️
1. Navigate to **Settings** tab
2. Adjust map resolution, MCDA defaults, LCOE parameters
3. Click **"💾 Save Settings"** to persist changes

### Advanced Usage

#### Command-Line Map Generation
```bash
python scripts/generate_maps_simple.py
```

#### Python API Usage
```python
from scripts.mcda_analysis import MCDAnalyzer
from scripts.lcoe_calculator import LCOECalculator

# MCDA
analyzer = MCDAnalyzer(weights={'solar': 0.30, 'population': 0.25, ...})
aptitude = analyzer.weighted_overlay()

# LCOE
calc = LCOECalculator(location="Angola")
results = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2226)
```

#### Batch Processing
```python
from scripts.batch_mcda_api import get_batch_processor

processor = get_batch_processor()
job_id = processor.submit_job(inputs)
status = processor.get_job_status(job_id)
```

---

## API Reference

### REST API (Optional - FastAPI)

**Base URL:** `http://localhost:8000`

**Endpoints:**
- `GET /health` — Health check
- `POST /mcda/compute` — Compute MCDA analysis
- `POST /mcda/batch/jobs` — Submit batch MCDA job
- `GET /mcda/batch/jobs/{job_id}` — Get job status
- `GET /lcoe/compare` — Compare technologies

**Documentation:** http://localhost:8000/docs (Swagger UI)

**Start API:**
```bash
uvicorn scripts.api:app --host 0.0.0.0 --port 8000
```

---

## Deployment Options

### Option 1: Local Development
```bash
streamlit run geesp_unified_app.py
```
**Access:** http://localhost:8501

### Option 2: Docker
```bash
docker build -f Dockerfile.app -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```

### Option 3: Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect repository at streamlit.io/cloud
3. Deploy automatically
4. Share public URL

### Option 4: Desktop Executable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico geesp_unified_app.py
```
**Result:** Single `.exe` file that launches the app

### Option 5: Kubernetes
```bash
kubectl apply -f k8s/geesp-deployment.yaml
```

---

## Troubleshooting

### Common Issues

#### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements-app.txt
# Or reinstall:
pip install --upgrade -r requirements-app.txt
```

#### Issue: Maps not generating
**Solution:**
- Check `data/processed/` directory exists
- Ensure write permissions
- Run: `python scripts/generate_maps_simple.py` manually

#### Issue: Port 8501 already in use
**Solution:**
```bash
# Use different port
streamlit run geesp_unified_app.py --server.port 8502
```

#### Issue: Database connection errors
**Solution:**
- App falls back to sample data automatically
- To use database: Run migrations first
- Check `data/sqlite/` directory exists

#### Issue: Google Earth Engine not working
**Solution:**
- GEE requires authentication: `earthengine authenticate`
- App works without GEE (uses local map generation)

### Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: Check `verify_integration.py` output
- **Logs**: Check `logs/geesp.log` for errors

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.10 | 3.11+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 2 GB | 5 GB |
| **CPU** | 2 cores | 4+ cores |

---

## License

MIT License - See [LICENSE](LICENSE) file

---

## Authors & Contact

- **Rocélio Da Silva** (ISPTEC) - Lead Developer
- **Alexandre Dos Santos** (ISPTEC) - Backend & GEE Integration
- **Delfina Mpanka** (ISPTEC) - Data & Validation

**Contact:** geesp-angola@isptec.ao  
**GitHub:** github.com/ISPTEC-Energy/geesp-angola

---

*Developed for MIT Climate Portal - Boston 2026*
