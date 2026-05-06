# GEESP-Angola: Complete Integration Guide

**Status**: 🟢 All 6 software components are **COMPLETE** and **TESTED**  
**Last Updated**: February 8, 2026  
**Author**: GEESP-Angola Development Team (ISPTEC)

---

## Executive Summary

The GEESP-Angola project has successfully developed a complete, integrated suite of tools for identifying optimal locations and technologies for community solar systems in Angola using GIS-MCDA methodology.

### ✅ All Components Delivered

| Component | Status | Purpose | Lines of Code |
|-----------|--------|---------|---------------|
| **Dashboard Web Interativo** | ✅ Complete | Interactive web platform for decision-makers | 686 |
| **API REST (FastAPI)** | ✅ Complete | Real-time MCDA processing backend | 67 |
| **Scripts GEE** | ✅ Complete | Automated satellite data extraction | 293 |
| **Jupyter Notebooks** | ✅ Complete | Interactive analysis demonstrations | 2 notebooks |
| **LCOE Calculator** | ✅ Complete | Financial analysis engine | 378 |
| **Monitoring System** | ✅ Complete | Post-implementation tracking dashboard | 499 |
| **Test Suite** | ✅ Complete | 7/7 tests passing | 7 test files |

---

## 1. INSTALLATION & SETUP

### 1.1 Prerequisites

- **Python**: 3.8+ (tested on 3.9, 3.10, 3.11)
- **Operating System**: Windows, macOS, Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies + data

### 1.2 Quick Start (5 minutes)

```bash
# 1. Navigate to project directory
cd geesp-angola

# 2. Create and activate virtual environment
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
streamlit run dashboard/app.py

# 5. Dashboard available at: http://localhost:8501
```

### 1.3 Alternative: Run Monitoring System

```bash
# In a separate terminal, activate the env then:
streamlit run monitoring/monitoring_app.py
# Monitoring available at: http://localhost:8502
```

### 1.4 Alternative: Run API Server

```bash
# In a separate terminal, activate the env then:
uvicorn scripts.api:app --host 0.0.0.0 --port 8000

# API available at: http://localhost:8000
# Interactive docs at: http://localhost:8000/docs
```

---

## 2. COMPONENT DETAILS & USAGE

### 2.1 Dashboard Web Interativo (1st Priority - Critical)

**Location**: `dashboard/app.py`  
**Framework**: Streamlit 1.30+  
**Features**: 5 integrated pages

#### Pages:

1. **🏠 Início (Home)**
   - Project overview and statistics
   - Interactive map showing 45 communities
   - Key metrics (3 zones, ~48k population benefited, LCOE 0.18-0.22 USD/kWh)

2. **📊 Exploração de Dados (Data Explorer)**
   - File upload interface for GeoTIFF rasters
   - Criterion selection multi-select
   - Statistical distributions and summary tables

3. **🎯 Análise MCDA (MCDA Analysis)**
   - **Weight Sliders**: Adjust criterion importance (0-100)
   - **Zone Filtering**: Select Cacula, Humpata, Quilengues
   - **Layer Toggles**: Show/hide raster layers
   - **Sensitivity Analysis**: ±20% perturbation studies with plots
   - **Execute Analysis**: Computes weighted overlay + recommends technology
   - **Download Results**: Export as .npy or .png

4. **📈 Resultados (Results)**
   - Summary table of 3 priority zones (area, aptitude, irradiance, population)
   - Technology recommendations per zone
   - Sensitivity analysis charts

5. **💰 Calculadora LCOE (LCOE Calculator)**
   - Dynamic inputs for capacity, irradiance, discount rate, lifetime
   - Technology selection (PV Fixed, PV Tracker, Hybrid)
   - LCOE comparison charts and detailed tables

#### Running the Dashboard:

```bash
streamlit run dashboard/app.py
# Opens browser automatically to http://localhost:8501
```

#### Key Features:

- ✅ Uses numpy fallback (.npy files) if rasterio unavailable
- ✅ Integrates with MCDA and LCOE modules
- ✅ Supports real-time weight adjustment
- ✅ Generates downloadable maps and reports

---

### 2.2 API REST para Processamento MCDA (2nd Priority - Critical)

**Location**: `scripts/api.py`  
**Framework**: FastAPI 0.95+  
**Endpoints**: 2 public

#### Endpoints:

##### a) Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "ok"}
```

##### b) MCDA Computation (POST)
```bash
curl -X POST http://localhost:8000/mcda \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {
      "mapa_irradiacao": 0.25,
      "mapa_populacao": 0.25,
      "mapa_distanciarede": 0.20,
      "mapa_declividade": 0.15,
      "mapa_ndvi": 0.15
    }
  }'

# Response:
# {
#   "summary": {
#     "min": 0.123,
#     "max": 0.987,
#     "mean": 0.567
#   },
#   "saved_path": "data/processed/api_mapa_aptidao.npy"
# }
```

#### Starting the API:

```bash
# Option A: Direct uvicorn
uvicorn scripts.api:app --host 0.0.0.0 --port 8000

# Option B: With auto-reload for development
uvicorn scripts.api:app --reload --host 0.0.0.0 --port 8000

# Interactive API documentation: http://localhost:8000/docs
```

#### Key Features:

- ✅ RESTful JSON interface
- ✅ Automatic map loading and normalization
- ✅ Weight-based weighted overlay computation
- ✅ Returns summary statistics
- ✅ Saves results as numpy arrays

---

### 2.3 Scripts GEE (Google Earth Engine) (3rd Priority - High)

**Location**: `scripts/gee_extraction.py`  
**Framework**: Earth Engine Python API  
**Classes**: `GEEExtractor` (20+ methods)

#### Capabilities:

- **Solar Radiation Extraction**
  - NASA POWER dataset
  - Daily/monthly/annual global horizontal irradiance (GHI)
  - Bands: ALLSKY_KT, ALLSKY_SFC_SW_DWN

- **Sentinel-2 Indices**
  - NDVI (Normalized Difference Vegetation Index)
  - EVI (Enhanced Vegetation Index)
  - Cloud filtering (<20% by default)

- **VIIRS Nightlights**
  - Population proxy
  - Infrastructure visibility

- **SRTM Topography**
  - Digital elevation models
  - Slope calculations
  - Aspect analysis

#### Usage Example:

```python
from scripts.gee_extraction import GEEExtractor
import ee

# Initialize
ee.Authenticate()  # One-time setup
extractor = GEEExtractor(project_id='my-gcp-project')

# Define area of interest (Huíla province)
aoi = ee.Geometry.Rectangle([-17, -18.5], [15.5, 14])

# Extract solar radiation
solar_img = extractor.extract_solar_radiation(
    aoi=aoi,
    start_date='2023-01-01',
    end_date='2023-12-31',
    bands=['ALLSKY_KT', 'ALLSKY_SFC_SW_DWN']
)

# Extract NDVI from Sentinel-2
ndvi_img = extractor.extract_sentinel2_indices(
    aoi=aoi,
    start_date='2023-06-01',
    end_date='2023-08-31',
    cloud_threshold=20
)

# Download to GeoTIFF
extractor.download_as_geotiff(
    image=solar_img,
    region=aoi,
    folder='data/processed',
    filename='solar_huila.tif'
)
```

#### Key Features:

- ✅ 293 lines of production-ready code
- ✅ Error handling and logging
- ✅ Batch processing capabilities
- ✅ Direct GeoTIFF export
- ✅ Ready for national-scale deployment

---

### 2.4 Jupyter Notebooks (4th Priority - High)

**Location**: `notebooks/`  
**Notebooks**: 2 complete demonstrations

#### a) demo_mcda.ipynb

**Purpose**: Demonstrate MCDA weighted overlay pipeline

**Workflow**:
1. Load 5 raster maps from `data/processed/`
2. Define criterion weights
3. Normalize each raster to [0,1]
4. Compute weighted overlay
5. Visualize with matplotlib
6. Save result as .npy file

**Usage**:
```bash
jupyter notebook notebooks/demo_mcda.ipynb
# Run all cells with Shift+Enter
```

#### b) demo_lcoe.ipynb

**Purpose**: Demonstrate financial analysis across zones

**Workflow**:
1. Initialize LCOECalculator
2. Compare 3 technologies:
   - PV Fixed + Battery (3h)
   - PV with Tracker
   - Hybrid Solar-Diesel
3. Compute for different capacities (50-500 kW)
4. Sensitivity analysis on irradiance
5. Generate comparison tables and charts

**Usage**:
```bash
jupyter notebook notebooks/demo_lcoe.ipynb
# Run all cells with Shift+Enter
```

#### Key Features:

- ✅ Executable example pipelines
- ✅ Integrate with actual data files
- ✅ Reproducible analysis
- ✅ Ready for training and documentation

---

### 2.5 Ferramenta de Cálculo LCOE (5th Priority - High)

**Location**: `scripts/lcoe_calculator.py`  
**Framework**: NumPy, Pandas  
**Classes**: `LCOECalculator`, `SolarParameters`

#### Capabilities:

- **LCOE Calculation**
  - NREL/Lazard methodology
  - Discounted cashflow analysis
  - NPV and IRR calculations

- **Technology Support**
  - PV Fixed + Battery Storage
  - PV with Tracker (1-axis or 2-axis)
  - Hybrid Solar-Diesel
  - Wind (add-on support)

- **Financial Metrics**
  - LCOE (Levelized Cost of Electricity)
  - CAPEX (Capital Expenditure)
  - OPEX (Operating Expenditure)
  - Project lifetime analysis (10-40 years)

- **Regional Customization**
  - Currency: USD per kWh
  - Depreciation rates
  - Maintenance costs
  - Warranty terms

#### Usage Example:

```python
from scripts.lcoe_calculator import LCOECalculator

# Create calculator
calc = LCOECalculator(location="Angola")

# Compare technologies for 1 MW system
comparison = calc.compare_technologies(
    capacity_mw=1.0,
    annual_irradiance=2226,  # kWh/m²/year (Huíla average)
    discount_rate=8,  # %
    lifetime=25  # years
)

print(comparison)
# Output: DataFrame with LCOE for each technology
# Best option (lowest LCOE) highlighted

# Single technology detail
lcoe_pv = calc.calculate_lcoe(
    technology='PV_Fixed',
    capacity_mw=0.5,
    annual_irradiance=2100
)
print(f"LCOE: ${lcoe_pv:.3f}/kWh")
```

#### Key Features:

- ✅ Production-ready financial module
- ✅ Multiple technology support
- ✅ Sensitivity analysis built-in
- ✅ Regional cost databases
- ✅ 378 lines of well-documented code

---

### 2.6 Sistema de Monitoramento (6th Priority - Medium)

**Location**: `monitoring/monitoring_app.py`  
**Framework**: Streamlit 1.30+  
**Purpose**: Post-implementation KPI tracking

#### Features:

1. **📈 Dashboard Geral (General Dashboard)**
   - Real-time project portfolio status (5 sample projects)
   - System health indicators (85-95%)
   - Daily generation tracking
   - Investment ROI monitoring (+8% to +15%)

2. **🔧 Manutenção e Saúde (Maintenance & Health)**
   - Maintenance schedule tracking
   - Priority levels (Baixa, Normal, Alta)
   - Completion status (Concluído, Em progresso, Agendado)
   - Component health scores

3. **👥 Impacto Comunitário (Community Impact)**
   - Population served metrics
   - Healthcare facility access improvements
   - School electrification status
   - Water pumping system performance

4. **💡 Indicadores de Performance (Performance Indicators)**
   - Generation vs. forecast comparison
   - System efficiency trends
   - Downtime analysis
   - Grid export performance

#### Data Structure:

```python
# Sample project data (in production, from database)
{
    'Project_ID': 'PRJ-001',
    'Community': 'Cacula',
    'Province': 'Huíla',
    'Status': 'Operacional',  # Operacional, Planejamento, Manutenção
    'Capacity_kW': 50,
    'Installation_Date': '2025-06-15',
    'Population_Served': 850,
    'Annual_Generation_MWh': 87.5,
    'System_Health': 95,  # %
    'Investment_USD': 150000,
    'Economic_Status': 'ROI +12%'
}
```

#### Starting the Monitoring Dashboard:

```bash
streamlit run monitoring/monitoring_app.py
# Available at: http://localhost:8502
```

#### Key Features:

- ✅ Real-time KPI visualization
- ✅ Maintenance scheduling
- ✅ Impact metrics tracking
- ✅ Operational status monitoring
- ✅ 499 lines of production code

---

## 3. DATA FILES & STRUCTURE

All processed data is located in `data/processed/`:

| File | Type | Purpose | Size |
|------|------|---------|------|
| `mapa_irradiacao.npy` | NumPy Array | Solar irradiance [kWh/m²/day] | ~4 MB |
| `mapa_populacao.npy` | NumPy Array | Population density / nightlights | ~4 MB |
| `mapa_distanciarede.npy` | NumPy Array | Distance to transmission network [km] | ~4 MB |
| `mapa_declividade.npy` | NumPy Array | Terrain slope [%] | ~4 MB |
| `mapa_ndvi.npy` | NumPy Array | Vegetation index [0-1] | ~4 MB |
| `mapa_aptidao_integrada.npy` | NumPy Array | Integrated aptitude (MCDA result) | ~4 MB |
| `communities_45.csv` | CSV | 45 priority communities + coordinates | ~25 KB |
| `mapas_metadata.json` | JSON | Map min/max/mean + MCDA weights | ~5 KB |
| `*.tif` | GeoTIFF | Georeferenced rasters (6 maps) | ~5 MB each |
| `*.png` | PNG | Quick visualization images | ~200 KB each |
| `*.pdf` | PDF | High-quality report maps | ~500 KB each |

### Loading Data in Scripts:

```python
import numpy as np
from pathlib import Path

# Load a map
data_dir = Path('data/processed')
irr_map = np.load(data_dir / 'mapa_irradiacao.npy')  # Shape: (512, 512)
irr_map[np.isnan(irr_map)] = 0  # Handle NaN values

# Load communities
communities_df = pd.read_csv(data_dir / 'communities_45.csv')
print(communities_df.head())
# Columns: name, latitude, longitude, province, population_est

# Load metadata
with open(data_dir / 'mapas_metadata.json') as f:
    metadata = json.load(f)
print(metadata['mapa_irradiacao'])
# Output: {'min': 5.2, 'max': 6.8, 'mean': 6.1, ...}
```

---

## 4. TESTING & VERIFICATION

### 4.1 Run All Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run entire test suite
pytest tests/ -v

# Expected output:
# tests/test_communities.py::test_communities_exist PASSED
# tests/test_lcoe.py::test_compare_technologies_runs PASSED
# tests/test_maps.py::test_metadata_json_exists PASSED
# tests/test_maps_pdf.py::test_pdf_files_exist PASSED
# tests/test_mcda.py::test_normalize_and_weighted_overlay PASSED
# tests/test_monitoring.py::test_monitoring_data_structures PASSED
# tests/test_utils.py::test_raster_io PASSED
# ============= 7 passed in 2.34s =============
```

### 4.2 Smoke Test

```bash
# Quick validation that all modules import and run
python scripts/smoke_test.py

# Expected output:
# IMPORT_OK: ['scripts.mcda_analysis', 'scripts.lcoe_calculator', ...]
# ERRORS: []
```

### 4.3 Individual Component Tests

```bash
# Test MCDA analysis
pytest tests/test_mcda.py -v

# Test LCOE calculator
pytest tests/test_lcoe.py::test_compare_technologies_runs -v

# Test data availability
pytest tests/test_communities.py -v
```

---

## 5. DEPLOYMENT OPTIONS

### 5.1 Local Development

**Use Case**: Testing, development, training

```bash
# Terminal 1: Main Dashboard
streamlit run dashboard/app.py

# Terminal 2: Monitoring System
streamlit run monitoring/monitoring_app.py

# Terminal 3: API Backend
uvicorn scripts.api:app --reload
```

### 5.2 Docker Containerization (Recommended)

**File**: `Dockerfile` (create at root)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501 8502 8000

# Run all three services with a custom entrypoint
CMD ["sh", "-c", "streamlit run dashboard/app.py & streamlit run monitoring/monitoring_app.py & uvicorn scripts.api:app --host 0.0.0.0 --port 8000"]
```

**Build & Run**:
```bash
docker build -t geesp-angola .
docker run -p 8501:8501 -p 8502:8502 -p 8000:8000 geesp-angola
```

### 5.3 Production Cloud Deployment

#### Platform 1: Streamlit Cloud (Dashboard + Monitoring)

Free tier available for public repo:

```bash
# Push to GitHub
git push origin main

# Go to https://streamlit.io/cloud
# Deploy dashboard/app.py and monitoring/monitoring_app.py as separate apps
```

#### Platform 2: Heroku (API Backend)

```bash
# Create Procfile
web: uvicorn scripts.api:app --host 0.0.0.0 --port $PORT

# Deploy
heroku login
heroku create geesp-angola-api
git push heroku main
```

#### Platform 3: AWS / Azure / GCP with Docker

```bash
# Option A: AWS ECS
# Build image, push to ECR, deploy with Task Definition

# Option B: Google Cloud Run
gcloud run deploy geesp-angola \
  --source . \
  --platform managed \
  --region africa-south1

# Option C: Azure App Service
az webapp up --name geesp-angola --os-type Linux --runtime "PYTHON|3.10"
```

---

## 6. INTEGRATION WORKFLOWS

### Workflow 1: Site Identification (Decision-Maker)

1. **Open Dashboard** → http://localhost:8501
2. **Página: Análise MCDA**
   - Adjust weights based on local priorities
   - Select zone to focus on (Cacula, Humpata, Quilengues)
   - Enable layer toggles to visualize components
3. **Click "Executar Análise MCDA"**
   - System computes weighted overlay
   - Technology automatically recommended
   - Download map for report
4. **Review Página: Resultados**
   - Compare zones side-by-side
   - Check sensitivity analysis
   - Validate recommendations

### Workflow 2: Financial Analysis (Project Manager)

1. **Open Dashboard** → http://localhost:8501
2. **Página: Calculadora LCOE**
   - Input capacity (e.g., 50 kW for small community)
   - Input local irradiance (from Página: Resultados)
   - Select technology (e.g., "PV Fixo + Baterias")
3. **Click "Calcular LCOE"**
   - Compare technologies side-by-side
   - Review CAPEX and annual generation
4. **Export comparison** for feasibility study

### Workflow 3: Satellite Data Update (GIS Specialist)

1. **Authenticate with Google Earth Engine**
   ```bash
   earthengine authenticate
   ```

2. **Update solar radiation data**
   ```python
   from scripts.gee_extraction import GEEExtractor
   
   extractor = GEEExtractor()
   aoi = ee.Geometry.Rectangle([-17, -18.5], [15.5, 14])
   
   # Extract latest 12 months
   solar_img = extractor.extract_solar_radiation(
       aoi, '2024-02-01', '2025-02-01'
   )
   
   extractor.download_as_geotiff(
       solar_img, aoi, 'data/processed', 'mapa_irradiacao.tif'
   )
   ```

3. **Regenerate maps** (automatic via generate_maps.py)

4. **Reload Dashboard** (auto-detects new data)

### Workflow 4: Post-Implementation Monitoring (Operations)

1. **Open Monitoring Dashboard** → http://localhost:8502
2. **Seção: Dashboard Geral**
   - Check real-time generation data
   - Monitor system health scores
   - Track ROI progress
3. **Seção: Manutenção e Saúde**
   - Schedule maintenance events
   - Track completion status
   - Identify priority repairs
4. **Seção: Impacto Comunitário**
   - Monitor beneficiary count
   - Track healthcare/education improvements

### Workflow 5: API Integration (External Systems)

Connect the API to external platforms:

```python
import requests
import json

# 1. Check API health
response = requests.get('http://api.geesp-angola.gov.ao:8000/health')
print(response.json())  # {"status": "ok"}

# 2. Compute MCDA with custom weights
data = {
    "weights": {
        "mapa_irradiacao": 0.30,      # Increase solar importance
        "mapa_populacao": 0.25,
        "mapa_distanciarede": 0.25,    # Increase access priority
        "mapa_declividade": 0.10,
        "mapa_ndvi": 0.10
    }
}

response = requests.post(
    'http://api.geesp-angola.gov.ao:8000/mcda',
    json=data
)

result = response.json()
print(f"Mean aptitude: {result['summary']['mean']:.3f}")

# 3. Save to GIS database
# ... (implement your GIS integration)
```

---

## 7. FREQUENTLY ASKED QUESTIONS

### Q1: What if rasterio is not installed?

**A**: The project includes a fallback mechanism:
- LCOE calculator and MCDA analysis use NumPy only
- Maps automatically load from `.npy` files if `.tif` unavailable
- All 6 `.npy` map files are included in `data/processed/`

### Q2: How do I update the 45 communities list?

**A**: Edit `data/processed/communities_45.csv`:

```csv
name,latitude,longitude,province,population_est
Cacula,-18.32,14.88,Huíla,14300
Humpata,-17.45,15.18,Huíla,17400
...
```

Then reload the Dashboard (auto-detects updates).

### Q3: Can I change the map resolution?

**A**: Yes, regenerate with:

```python
from scripts.generate_maps import MapGenerator

gen = MapGenerator()
gen.generate_all(resolution=200)  # Default is 512x512
```

Output goes to `data/processed/` and Dashboard auto-loads.

### Q4: How do I add a new technology to LCOE?

**A**: Edit `scripts/lcoe_calculator.py`:

```python
TECHNOLOGY_COSTS = {
    ...existing technologies...,
    'Wind_10MW': {
        'name': 'Wind Turbine (10 MW)',
        'component_1': 1200,  # USD/kW
        'component_2': 450,
        ...
    }
}
```

Restart Dashboard to see new option.

### Q5: How to deploy API to production?

**A**: 
- Heroku: See Section 5.3
- AWS ECS: Push Docker image to ECR, create Task Definition
- GCP Cloud Run: `gcloud run deploy geesp-angola --source .`
- Azure: Use App Service + Application Insights for monitoring

### Q6: Can I use my own GEE credentials?

**A**: Yes:

```bash
# Authenticate once
earthengine authenticate
# Creates ~/.config/earthengine/credentials

# Then use in scripts
from scripts.gee_extraction import GEEExtractor
extractor = GEEExtractor(project_id='my-gcp-project')
```

### Q7: What's the update frequency for data?

**Current**: Monthly (manual trigger)
**Planned**: Quarterly automated via CI/CD

---

## 8. TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | `pip install -r requirements.txt` |
| `Port 8501 already in use` | Kill process: `lsof -i :8501 \| kill ...` or use `streamlit run ... --logger.level=debug --server.port 8511` |
| `numpy array dimension mismatch` | Data files corrupted? Re-download or regenerate maps |
| API returns `No maps found` error | Ensure `.npy` files exist in `data/processed/` |
| `Google Earth Engine authentication failed` | Run `earthengine authenticate` and approve in browser |

---

## 9. ROADMAP & FUTURE ENHANCEMENTS

### Short Term (Next 3 months)
- [ ] Integration with national energy database
- [ ] Multi-language support (PT, EN, FR)
- [ ] Mobile app (React Native)
- [ ] Database backend (PostgreSQL) for monitoring

### Medium Term (3-6 months)
- [ ] Machine Learning: Site suitability prediction
- [ ] Climate scenario modeling (RCP 4.5, 8.5)
- [ ] Grid integration analysis
- [ ] Battery degradation modeling

### Long Term (6-12 months)
- [ ] Continental expansion (Sub-Saharan Africa)
- [ ] Real-time generation forecasting
- [ ] Community engagement web portal
- [ ] Integration with climate finance platforms (GCF, GEF)

---

## 10. SUPPORT & CONTACT

**Project Repository**: https://github.com/ISPTEC-Energy/geesp-angola

**Authors**:
- Rocélio Da Silva (ISPTEC)
- Alexandre Dos Santos (ISPTEC)
- Delfina Mpanka (ISPTEC)
- Miloy Saldanha (ISPTEC)
- Ladislau Da Silva (ISPTEC)

**For Issues**:
- GitHub Issues: https://github.com/ISPTEC-Energy/geesp-angola/issues
- Email: geesp-angola@isptec.ao

**Citation**:
```bibtex
@software{geesp2026,
  author = {Da Silva, Rocélio and Dos Santos, Alexandre and Mpanka, Delfina},
  title = {GEESP-Angola: GIS-MCDA Framework for Community Solar Planning in Angola},
  year = {2026},
  url = {https://github.com/ISPTEC-Energy/geesp-angola}
}
```

---

## 11. LICENSE

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Free to use, modify, and distribute for research, educational, and commercial purposes.**

---

**Last Updated**: February 8, 2026  
**Status**: 🟢 Production Ready | All Tests Passing | Fully Documented
