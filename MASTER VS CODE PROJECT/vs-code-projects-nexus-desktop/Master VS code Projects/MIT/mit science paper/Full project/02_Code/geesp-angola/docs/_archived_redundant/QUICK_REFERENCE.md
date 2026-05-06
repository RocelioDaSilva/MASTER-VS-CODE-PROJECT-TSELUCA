# 🗂️ GEESP-Angola Quick Reference Card

**Consolidated Documentation** | **Effective 2026-02-09** | **Keep this handy!**

---

## ⭐ THE TWO MASTER DOCS (Go Here First!)

### 1. **[SOFTWARE_CAPABILITIES.md](SOFTWARE_CAPABILITIES.md)** — Features & How-To
- 📦 Installation & setup (5 minutes)
- 🎯 All 6 dashboard modules
- 🔧 Deployment options (Docker, Cloud, Local)
- 📖 Complete API reference
- ❓ Troubleshooting

👉 **Read when**: Getting started, deploying, learning features

### 2. **[IMPROVEMENTS_ROADMAP.md](IMPROVEMENTS_ROADMAP.md)** — Roadmap & Progress
- 📈 Quality metrics & scoring
- 🎯 Phase 1-3 breakdown (70 hours total)
- ✅ Current status (80% complete)
- 📋 Action matrix by file
- 🚀 Strategic recommendations

👉 **Read when**: Planning, understanding progress, tracking metrics

---

## 🚀 Quick Start (Choose One)

### Option A: Interactive Dashboard (Recommended)
```bash
cd geesp-angola
streamlit run geesp-unified-app.py
# Opens: http://localhost:8501
```

### Option B: Docker
```bash
docker-compose up -d
# Opens: http://localhost:8501
```

### Option C: With Python Venv
```bash
python -m venv env
source env/bin/activate  # or: env\Scripts\activate
pip install -r requirements-unified.txt
streamlit run geesp-unified-app.py
```

---

## 📋 Navigation Guide

| I want to... | Read this |
|--------------|-----------|
| **Install & run** | [SOFTWARE_CAPABILITIES.md](SOFTWARE_CAPABILITIES.md) |
| **See what features exist** | [SOFTWARE_CAPABILITIES.md](SOFTWARE_CAPABILITIES.md) |
| **Deploy to cloud** | [SOFTWARE_CAPABILITIES.md](SOFTWARE_CAPABILITIES.md) |
| **Understand the roadmap** | [IMPROVEMENTS_ROADMAP.md](IMPROVEMENTS_ROADMAP.md) |
| **Check Phase 1 progress** | [PHASE1_IMPLEMENTATION_STATUS.md](PHASE1_IMPLEMENTATION_STATUS.md) |
| **Verify everything works** | `python verify_phase1.py` |
| **Find any document** | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |

---

## 🏃 QuickStart: 5 Minutes to Running| Component | Status | Start Command | Port | Users |
|-----------|--------|---------------|------|-------|
| **Dashboard Web** | ✅ 686 LOC | `streamlit run dashboard/app.py` | 8501 | Decision-makers, Planners |
| **API REST** | ✅ 67 LOC | `uvicorn scripts.api:app` | 8000 | Developers, GIS analysts |
| **GEE Scripts** | ✅ 293 LOC | `python scripts/gee_extraction.py` | N/A | Data scientists |
| **Notebooks** | ✅ 2 files | `jupyter notebook notebooks/` | 8888 | Analysts, Trainers |
| **LCOE Calculator** | ✅ 378 LOC | Embedded in Dashboard | - | Finance teams |
| **Monitoring System** | ✅ 499 LOC | `streamlit run monitoring/monitoring_app.py` | 8502 | Operations |
| **Test Suite** | ✅ 7/7 passing | `pytest tests/ -v` | N/A | QA, CI/CD |

---

## 🗂️ Key Files & Locations

```
geesp-angola/
├── dashboard/
│   └── app.py                    ← Main interactive dashboard (5 pages)
├── scripts/
│   ├── api.py                    ← REST API (FastAPI)
│   ├── gee_extraction.py         ← Satellite data extraction
│   ├── mcda_analysis.py          ← MCDA weighted overlay
│   ├── lcoe_calculator.py        ← Financial analysis
│   └── utils.py                  ← Utility functions
├── monitoring/
│   └── monitoring_app.py         ← Post-implementation tracking
├── notebooks/
│   ├── demo_mcda.ipynb          ← MCDA pipeline demo
│   └── demo_lcoe.ipynb          ← LCOE analysis demo
├── tests/
│   ├── test_mcda.py
│   ├── test_lcoe.py
│   ├── test_monitoring.py
│   └── 4 other test files
├── data/processed/
│   ├── mapa_irradiacao.npy      ← Solar irradiance
│   ├── mapa_populacao.npy       ← Population/nightlights
│   ├── mapa_distanciarede.npy   ← Distance to transmission
│   ├── mapa_declividade.npy     ← Terrain slope
│   ├── mapa_ndvi.npy            ← Vegetation index
│   ├── mapa_aptidao_integrada.npy ← MCDA result
│   ├── communities_45.csv       ← 45 priority locations
│   └── mapas_metadata.json      ← Map statistics
├── requirements.txt              ← Python dependencies
├── INTEGRATION_GUIDE.md          ← Complete 11-section guide
└── README.md                     ← Project overview
```

---

## 📊 Dashboard Pages Guide

### Page 1: 🏠 INÍCIO (Home)
- **Purpose**: Overview and project statistics
- **Content**: 
  - 45 communities interactive map
  - 3 priority zones highlighted (Cacula, Humpata, Quilengues)
  - Key metrics: ~48k population, LCOE 0.18-0.22 USD/kWh
- **Time**: 2-3 minutes

### Page 2: 📊 EXPLORAÇÃO DE DADOS (Data Explorer)
- **Purpose**: Understand data distribution
- **Content**:
  - Upload GeoTIFF rasters (optional)
  - View criterion statistics
  - Distribution histograms
- **Time**: 5-10 minutes

### Page 3: 🎯 ANÁLISE MCDA (Analysis Engine - Most Important!)
- **Purpose**: Main decision-making tool
- **Key Features**:
  - **Weight Sliders**: Adjust each criterion 0-100%
  - **Zone Filter**: Focus on specific zone
  - **Layer Toggles**: Show/hide raster components
  - **Run Analysis**: Computes weighted overlay
  - **Sensitivity Study**: ±20% perturbation
  - **Technology Recommendation**: Automatic
  - **Downloads**: Export maps as .npy or .png
- **Time**: 10-15 minutes

### Page 4: 📈 RESULTADOS (Results Summary)
- **Purpose**: Compare zones and validate recommendations
- **Content**:
  - Side-by-side zone comparison table
  - Technology recommendations (PV Fixed, PV Tracker, Hybrid)
  - Sensitivity robustness charts
- **Time**: 5-10 minutes

### Page 5: 💰 CALCULADORA LCOE (Financial Tool)
- **Purpose**: Detailed financial analysis
- **Inputs**:
  - Capacity (MW): 0.1 - 100
  - Irradiance (kWh/m²/year): 1000 - 3000
  - Discount rate (%): 1 - 15
  - Lifetime (years): 10 - 40
  - Technology type (3 options)
- **Output**:
  - LCOE comparison bar chart
  - Detailed cost breakdown
- **Time**: 5-10 minutes

---

## 🔌 API Endpoints Reference

### 1. Health Check
```bash
GET /health
# Response: {"status": "ok"}
```

### 2. MCDA Computation
```bash
POST /mcda
# Body:
{
  "weights": {
    "mapa_irradiacao": 0.25,
    "mapa_populacao": 0.25,
    "mapa_distanciarede": 0.20,
    "mapa_declividade": 0.15,
    "mapa_ndvi": 0.15
  }
}

# Response:
{
  "summary": {
    "min": 0.123,
    "max": 0.987,
    "mean": 0.567
  },
  "saved_path": "data/processed/api_mapa_aptidao.npy"
}
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v
# Expected: 7 passed in ~2.3 seconds

# Quick smoke test
python scripts/smoke_test.py
# Expected: IMPORT_OK list with modules, ERRORS empty

# Individual tests
pytest tests/test_mcda.py -v      # MCDA module
pytest tests/test_lcoe.py -v      # LCOE calculator
pytest tests/test_monitoring.py -v # Monitoring
```

---

## 📦 Core Dependencies

| Package | Version | Used For |
|---------|---------|----------|
| streamlit | 1.30+ | Dashboards |
| fastapi | 0.95+ | API backend |
| numpy | 1.21+ | Raster processing |
| pandas | 1.3+ | Data tables |
| plotly | 5.0+ | Interactive charts |
| rasterio | 1.2+ | GeoTIFF I/O |
| geopandas | 0.9+ | Vector data |
| earthengine-api | 0.1.300+ | Satellite data |
| matplotlib | 3.4+ | Visualization |

---

## 💡 Common Tasks

### Task 1: Update Map Data (Quarterly)
```python
from scripts.gee_extraction import GEEExtractor
import ee

ee.Authenticate()
extractor = GEEExtractor()
aoi = ee.Geometry.Rectangle([-17, -18.5], [15.5, 14])

# Extract latest solar radiation
solar_img = extractor.extract_solar_radiation(
    aoi, '2024-02-01', '2025-02-01'
)
extractor.download_as_geotiff(solar_img, aoi, 'data/processed', 'mapa_irradiacao.tif')

# Reload dashboard → auto-detects new data
```

### Task 2: Add New Community
```bash
# Edit: data/processed/communities_45.csv
# Add row:
# Lobito,-12.35,13.58,Benguela,8900
# Save and reload Dashboard
```

### Task 3: Modify Technology Parameters
```bash
# Edit: scripts/lcoe_calculator.py
# Find: TECHNOLOGY_COSTS dictionary
# Update cost parameters
# Restart Dashboard
```

### Task 4: Generate New Maps (Different Resolution)
```python
from scripts.generate_maps import MapGenerator

gen = MapGenerator()
gen.generate_all(resolution=256)  # Lower resolution = faster

# Save to data/processed/ → Dashboard auto-loads
```

---

## 🚨 Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Port 8501 already in use` | Another app on same port | Kill: `lsof -i :8501 \| kill` or use `--server.port 9999` |
| `ModuleNotFoundError` | Missing dependencies | `pip install -r requirements.txt` |
| `No maps found in data/processed` | Missing .npy files | Download or regenerate maps |
| `GEE auth failed` | No credentials | `earthengine authenticate` |
| `Array dimension mismatch` | Corrupted data | Re-download or regenerate |

---

## 📚 Learning Resources

1. **Getting Started**: Read [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) (11 sections, comprehensive)
2. **Quick Start**: Run `streamlit run dashboard/app.py`
3. **Learn by Example**: Open `notebooks/demo_mcda.ipynb` and `demo_lcoe.ipynb`
4. **API Docs**: Visit `http://localhost:8000/docs` (Swagger UI)
5. **Code Comments**: Check docstrings in each Python module

---

## 🔗 Links

- **GitHub Repo**: https://github.com/ISPTEC-Energy/geesp-angola
- **Dashboard**: http://localhost:8501 (when running)
- **Monitoring**: http://localhost:8502 (when running)
- **API Docs**: http://localhost:8000/docs (when running)
- **Integration Guide**: [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
- **Project Status**: [PROJECT_STATUS.md](./PROJECT_STATUS.md)

---

## ✅ Verification Checklist

After installation, run these to verify everything works:

- [ ] Dashboard loads: `streamlit run dashboard/app.py` → http://localhost:8501
- [ ] All 5 pages accessible without errors
- [ ] Monitoring dashboard loads: `streamlit run monitoring/monitoring_app.py`
- [ ] API starts: `uvicorn scripts.api:app` → http://localhost:8000/docs
- [ ] Tests pass: `pytest tests/ -v` → 7/7 passing
- [ ] Notebooks runnable: `jupyter notebook notebooks/demo_mcda.ipynb`

---

## 🎯 Next Steps

1. **Read** [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for complete documentation
2. **Deploy** one component (start with Dashboard)
3. **Test** with sample data (all included)
4. **Customize** with local data via GEE scripts
5. **Integrate** with existing systems via API

---

**Last Updated**: February 8, 2026 | **Status**: 🟢 Production Ready | All 6 Components Complete
