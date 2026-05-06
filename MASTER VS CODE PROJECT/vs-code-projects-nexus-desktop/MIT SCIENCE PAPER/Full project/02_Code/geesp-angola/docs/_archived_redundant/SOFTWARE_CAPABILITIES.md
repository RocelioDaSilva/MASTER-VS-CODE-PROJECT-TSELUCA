# GEESP-Angola: Software Capabilities & User Guide

**Version**: 1.0 | **Date**: 2026-02-09 | **Status**: Production Ready

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features & Capabilities](#features--capabilities)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Module Reference](#module-reference)
6. [Deployment Options](#deployment-options)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)

---

## Overview

**GEESP-Angola** (Geospatial Energy for Equity & Solar Planning) is a comprehensive Python framework for solar energy site selection, financial analysis, and project monitoring in Angola.

### Core Components

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **Map Generation** | Extract GIS layers (solar, population, accessibility) | Google Earth Engine, Rasterio |
| **MCDA Analysis** | Multi-criteria decision analysis for site ranking | NumPy, Pandas, SciPy |
| **LCOE Calculator** | Financial viability analysis (3 technologies) | Python 3.11 |
| **Streamlit Dashboard** | Interactive visualization | Streamlit, Plotly |
| **Monitoring Dashboard** | Post-implementation performance tracking | Streamlit |
| **Configuration System** | Centralized settings management | JSON, Pydantic |

---

## Features & Capabilities

### 🗺️ Map Generation

Generate 6 spatial analysis layers:

1. **Solar Irradiance** — Annual average radiation (kWh/m²/day)
2. **Population Density** — Proximity to communities
3. **Grid Distance** — Distance to electrical infrastructure
4. **Terrain Slope** — Suitability for construction
5. **NDVI** — Vegetation coverage (land use)
6. **Integrated Aptitude** — Combined weighted suitability score

**Usage:**
```python
from scripts.gee_extraction import GEEExtractor

extractor = GEEExtractor()
aoi = extractor.create_aoi_from_bbox([14.0, -18.5, 15.5, -17.0])
solar = extractor.extract_solar_radiation(aoi, '2022-01-01', '2023-12-31')
```

**Data Source:** Google Earth Engine (requires authentication)

---

### 🎯 Multi-Criteria Decision Analysis (MCDA)

Weighted overlay analysis with customizable criteria:

**Default Weights:**
- Solar Irradiance: 30%
- Population Access: 25%
- Grid Distance: 20%
- Terrain Slope: 15%
- Vegetation (NDVI): 10%

**Capabilities:**
- Adjust weights dynamically
- Normalize raster data ([0,1])
- Three-class classification (Low/Medium/High aptitude)
- Sensitivity analysis
- Visualization with Plotly heatmaps

**Usage:**
```python
from scripts.mcda_analysis import MCDAnalyzer

analyzer = MCDAnalyzer()
weights = {'solar': 0.30, 'population': 0.25, ...}
aptitude = analyzer.combine_layers(weights)
```

---

### 💰 LCOE Calculator

Financial comparison across 3 solar technologies:

1. **Monocrystalline Silicon** — Highest efficiency, highest cost
2. **Polycrystalline Silicon** — Balanced efficiency/cost
3. **Cadmium Telluride (CdTe)** — Lowest cost, emerging tech

**Calculates:**
- Capital expenditure (CapEx)
- Operating expenditure (OpEx)
- Annual energy production
- Levelized Cost of Energy (LCOE) in USD/MWh

**Inputs:**
- Capacity (MW)
- Annual irradiance
- Discount rate (WACC)
- Project lifetime (years)

**Usage:**
```python
from scripts.lcoe_calculator import LCOECalculator

calc = LCOECalculator(location="Huíla")
results = calc.compare_technologies(capacity=1.0, irradiance=2226)
```

---

### 📊 Streamlit Unified Dashboard

Interactive web interface with 6 integrated tabs:

#### 🏠 Home
- Project introduction
- Feature overview
- Quick start guide
- System status

#### 🗺️ Map Generation
- Generate spatial layers
- Preview maps with statistics
- Interactive heatmap viewer
- Download options

#### 🎯 MCDA Analysis
- Adjust 5 weight sliders
- Real-time weight validation
- Integrated aptitude visualization
- Zone classification

#### 💰 LCOE Calculator
- Input capacity and location
- Technology comparison
- Cost breakdown
- Sensitivity analysis

#### 📊 Monitoring
- Project status dashboard
- KPI metrics
- Generation trends
- Efficiency tracking

#### ⚙️ Settings
- Configure map dimensions
- Set MCDA weight defaults
- Adjust LCOE parameters
- Save to config.json

---

### 🔧 Configuration System

**Centralized configuration** via `config.json`:

```json
{
  "map_generation": {
    "output_shape": [280, 300],
    "crs": "EPSG:32733"
  },
  "mcda": {
    "weights": {
      "solar_irradiance": 0.30,
      "population": 0.25,
      "grid_distance": 0.20,
      "slope": 0.15,
      "ndvi": 0.10
    }
  },
  "lcoe": {
    "wacc": 0.08,
    "project_lifetime_years": 20
  }
}
```

**Access in code:**
```python
from scripts.config_loader import ConfigLoader

config = ConfigLoader()
weights = config.get_mcda_weights()
```

---

### ✅ Input Validation

13 production validators ensure data quality:

- `validate_solar_irradiance()` — 0-300 kWh/m²/day
- `validate_population_density()` — 0-100,000 people/km²
- `validate_ndvi()` — -1 to +1 range
- `validate_weights()` — Sum to 1.0, all [0,1]
- `validate_capacity()` — 0.1 to 500 MW
- `validate_discount_rate()` — 1% to 20%
- And 7 more for specific parameters

**Usage:**
```python
from scripts.validators import validate_capacity, validate_weights

validate_capacity(1.5)  # ✓ Pass
validate_weights([0.3, 0.25, 0.2, 0.15, 0.1])  # ✓ Pass
```

---

### 📈 Type Annotations

Full type hint framework:

```python
from scripts.type_annotations import RasterArray, WeightsDict

def process_layer(data: RasterArray, weights: WeightsDict) -> RasterArray:
    ...
```

**Supports:**
- Type checking with Mypy
- IDE autocompletion
- Runtime validation with Pydantic
- Clear function signatures

---

## Installation

### Prerequisites
- Python 3.11+
- pip package manager
- 2 GB free disk space

### Step 1: Clone Repository

```bash
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements-unified.txt
```

### Step 4: Google Earth Engine Setup

```bash
earthengine authenticate
# Follow browser prompts to authorize
```

### Step 5: Configure Application

Edit `config.json`:
```json
{
  "study_area": {
    "bounds": [14.0, -18.5, 15.5, -17.0],
    "crs": "EPSG:32733"
  }
}
```

---

## Quick Start

### Run Locally (Easiest)

```bash
streamlit run geesp-unified-app.py
```

Opens at **http://localhost:8501**

### Run with Docker

```bash
docker-compose up -d
```

App available at **http://localhost:8501**

### Access Cloud Version

Deploy to Streamlit Cloud:
```bash
git push origin main
# Auto-deploys to https://geesp-angola.streamlit.app
```

---

## Module Reference

### scripts/gee_extraction.py

**Class: GEEExtractor**

```python
class GEEExtractor:
    def create_aoi_from_bbox(bounds: List[float]) -> ee.Geometry
    def extract_solar_radiation(aoi: ee.Geometry, date_start: str, date_end: str) -> np.ndarray
    def extract_population_density(aoi: ee.Geometry) -> np.ndarray
    def extract_vegetation(aoi: ee.Geometry) -> np.ndarray
    def export_to_geotiff(data: np.ndarray, filename: str) -> None
```

---

### scripts/mcda_analysis.py

**Class: MCDAnalyzer**

```python
class MCDAnalyzer:
    def normalize_raster(data: np.ndarray) -> np.ndarray
    def combine_layers(weights: Dict[str, float]) -> np.ndarray
    def classify_aptitude(data: np.ndarray, thresholds: List[float]) -> np.ndarray
    def sensitivity_analysis(base_weights: Dict, param_ranges: Dict) -> Dict
```

---

### scripts/lcoe_calculator.py

**Class: LCOECalculator**

```python
class LCOECalculator:
    def __init__(location: str, wacc: float = 0.08, lifetime: int = 20)
    def compare_technologies(capacity: float, irradiance: float) -> pd.DataFrame
    def calculate_capex(capacity: float, tech: str) -> float
    def calculate_opex(capacity: float, annual_yield: float, tech: str) -> float
    def calculate_lcoe(annual_yield: float, capex: float, opex: float) -> float
```

---

### scripts/validators.py

**Validation Functions:**

```python
def validate_capacity(value: float) -> float
def validate_solar_irradiance(value: float) -> float
def validate_population_density(value: float) -> float
def validate_weights(weights: List[float]) -> bool
def validate_discount_rate(value: float) -> float
def validate_raster_shape(shape: Tuple[int, int]) -> bool
# ... 7 more validators
```

---

### scripts/config_loader.py

**Configuration Management:**

```python
config = ConfigLoader()

# Get configurations
weights = config.get_mcda_weights()
shape = config.get_map_shape()
wacc = config.get_lcoe_wacc()

# Set configurations
config.set_mcda_weights({'solar': 0.35, ...})
config.save()
```

---

## Deployment Options

### Option 1: Local Development

```bash
pip install -r requirements-unified.txt
streamlit run geesp-unified-app.py
```

**Pros:** Fast, offline, free  
**Cons:** Single user, no persistence

---

### Option 2: Streamlit Cloud (Recommended) ⭐

```bash
# Push to GitHub
git add .
git commit -m "Deploy"
git push origin main

# Deploy at https://streamlit.io/cloud
```

**Pros:** Free, auto-deploy, web access  
**Cons:** Slower startup, limited compute

---

### Option 3: Docker

```bash
# Build image
docker build -t geesp-angola .

# Run container
docker run -p 8501:8501 geesp-angola

# Or use docker-compose
docker-compose up -d
```

**Pros:** Reproducible, portable  
**Cons:** More setup, docker knowledge needed

---

### Option 4: Cloud Platforms

**AWS, Azure, GCP:**
- Use provided Docker image
- Set environment variables for GEE credentials
- Configure auto-scaling

See [APP_DEPLOYMENT_GUIDE.md](APP_DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## API Documentation

### REST API (FastAPI - Future)

Planned for Phase 2+

**Endpoints:**
- `POST /api/mcda/analyze` — Run MCDA analysis
- `POST /api/lcoe/calculate` — Calculate LCOE
- `GET /api/maps/{map_type}` — Retrieve generated maps
- `GET /api/monitoring/projects` — List monitored projects

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install --upgrade streamlit
```

### Maps not loading

Maps need to be generated first:
1. Click "🔄 Generate" on Maps tab
2. Wait for completion
3. Refresh page

### Google Earth Engine authentication fails

```bash
earthengine authenticate
# Follow browser prompts
# Authorize access to GEE
```

### Port 8501 already in use

```bash
streamlit run geesp-unified-app.py --server.port 8502
```

### Performance slow

Enable caching in Settings tab:
```bash
# Streamlit automatically caches @st.cache_data functions
```

---

## Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** changes (`git commit -am 'Add feature'`)
4. **Push** to branch (`git push origin feature/your-feature`)
5. **Create** a Pull Request

### Code Standards

- Python 3.11+
- Type hints required
- Docstrings for all functions
- Tests for new features
- Follow PEP 8

### Testing

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=scripts
```

---

## Additional Resources

- **[README.md](README.md)** — Project overview
- **[QUICKSTART.md](QUICKSTART.md)** — 5-minute setup
- **[CODE_GUIDE.md](CODE_GUIDE.md)** — Code structure
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** — GitHub configuration
- **[LICENSE](LICENSE)** — Licensing information

---

## Support & Contact

📧 **Email**: geesp@isptec.ao  
🐙 **GitHub**: https://github.com/ISPTEC-Energy/geesp-angola  
📚 **Docs**: https://geesp-angola.readthedocs.io  
🐛 **Issues**: https://github.com/ISPTEC-Energy/geesp-angola/issues

---

**Last Updated**: 2026-02-09 | **Version**: 1.0 | **Status**: ✅ Production Ready
