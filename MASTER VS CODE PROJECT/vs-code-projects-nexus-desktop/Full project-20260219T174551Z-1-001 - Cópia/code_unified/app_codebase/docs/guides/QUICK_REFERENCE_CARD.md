# GEESP-Angola Quick Reference Card

## 🚀 FASTEST SETUP (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate test maps  
python generate_synthetic_maps_quick.py

# 3. Launch dashboard
streamlit run geesp_unified_app.py
```

**→ Opens at:** http://localhost:8501

---

## 📦 All Packages (Paste into terminal)

```bash
pip install numpy>=1.21.0 pandas>=1.3.0 scipy>=1.7.0 scikit-learn>=0.24.0 rasterio>=1.2.0 geopandas>=0.9.0 shapely>=1.7.0 pyproj>=3.1.0 rioxarray>=0.11.0 earthengine-api>=0.1.300 streamlit>=1.30.0 folium>=0.14.0 streamlit-folium>=0.16.0 matplotlib>=3.4.0 plotly>=5.0.0 seaborn>=0.11.0 openpyxl>=3.7.0 python-docx>=0.8.10 reportlab>=3.6.0 requests>=2.26.0 python-dotenv>=0.19.0 pyyaml>=5.4.0 tqdm>=4.62.0 Pillow>=9.0.0 fastapi>=0.95.0 uvicorn>=0.22.0 jupyter>=1.0.0 ipython>=7.25.0 black>=21.7b0 flake8>=3.9.0 pytest>=6.2.0
```

---

## 🔑 Earth Engine Setup (10 Minutes)

1. **Create GCP Project:** https://console.cloud.google.com/
   - New Project → Name: `GEESP-Angola` → Create

2. **Enable API:**
   - Search: `Earth Engine API` → Enable

3. **Create Service Account:**
   - APIs & Services → Credentials → Create Service Account
   - Name: `geesp-app` → Add role: Editor → Create Key (JSON) → Download

4. **Save Credentials:**
   ```
   geesp-angola/geesp-credentials.json
   ```

5. **Set Environment Variable:**
   ```powershell
   # Windows PowerShell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\geesp-credentials.json"
   ```

6. **Test:**
   ```bash
   python -c "import ee; ee.Initialize(); print('✅')"
   ```

---

## 🗺️ Generate Test Maps (5 Seconds)

```bash
python generate_synthetic_maps_quick.py
```

**Creates 6 files (~6 MB total):**
- ✅ `mapa_irradiacao.npy` (Solar)
- ✅ `mapa_declividade.npy` (Slope)
- ✅ `mapa_populacao.npy` (Population)
- ✅ `mapa_distanciarede.npy` (Grid Distance)
- ✅ `mapa_ndvi.npy` (Vegetation)
- ✅ `mapa_luminosidade_noturna.npy` (Nightlights)

---

## 🔧 Interactive Setup Menu

```bash
python SETUP_WIZARD.py
```

**Menu options:**
1. Print all dependencies
2. Install all packages
3. Setup Earth Engine
4. Generate synthetic maps
5. Complete setup (all above)
6. Verify installation
7. Exit

---

## 🧪 Verification Commands

```bash
# Check Python
python --version  # Must be 3.10+

# Check packages installed
python -c "import streamlit, numpy, geopandas; print('✓')"

# Verify data directory
ls data/processed/  # Should show 6 .npy files

# Check Earth Engine
python -c "import ee; ee.Initialize(); print('✅ GEE Ready')"

# Test Streamlit
streamlit run geesp_unified_app.py
```

---

## 📊 Expected Output: Dashboard

```
Dashboard Features:
├─ 🗺️  Interactive Maps (6 layers)
├─ 🎯 MCDA Analysis (6-criteria weighting)
├─ 💰 LCOE Calculator (USD/kWh)
├─ 📊 Monitoring (project tracking)
└─ ⚙️  Configuration
```

**6 Criteria (MCDA):**
- ☀️ Solar Irradiance (25% weight default)
- 👥 Population Density (25%)
- 🔌 Grid Distance (20%)
- ⛰️ Slope (15%)
- 🌱 NDVI (15%)
- 🌙 Nighttime Lights (10%)

---

## ⚡ Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `pip install [module]` |
| GDAL errors | `pip install --upgrade rasterio` |
| No map files | `python generate_synthetic_maps_quick.py` |
| Earth Engine fails | Check credentials + `earthengine authenticate` |
| Port 8501 in use | `streamlit run --server.port 8502 geesp_unified_app.py` |

---

## 📂 Project Structure

```
geesp-angola/
├── geesp_unified_app.py         ← Main dashboard
├── scripts/
│   ├── mcda_analysis.py        ← 6-criteria weighting
│   ├── lcoe_calculator.py       ← Financial math
│   ├── earth_engine_integration.py
│   ├── data_loaders_async.py
│   └── ... (35 modules total)
├── utils/
│   ├── import_helpers.py
│   ├── logging_config.py
│   └── ... (12 modules)
├── data/
│   └── processed/               ← 6 .npy map files
├── requirements.txt             ← All 48 packages
├── SETUP_WIZARD.py             ← Interactive setup
└── generate_synthetic_maps_quick.py
```

---

## 💾 Configuration (.env)

Create `geesp-angola/.env`:

```ini
ENV=development
GOOGLE_APPLICATION_CREDENTIALS=./geesp-credentials.json

# Default MCDA weights (sum = 1.0)
DEFAULT_WEIGHT_SOLAR=0.25
DEFAULT_WEIGHT_POPULATION=0.25
DEFAULT_WEIGHT_DISTANCE=0.20
DEFAULT_WEIGHT_SLOPE=0.15
DEFAULT_WEIGHT_NDVI=0.15
DEFAULT_WEIGHT_NIGHTLIGHTS=0.10
```

---

## 🎯 Quick Test Workflow

```bash
# 1. Setup (one-time)
python SETUP_WIZARD.py

# 2. Generate test data (one-time)
python generate_synthetic_maps_quick.py

# 3. Launch dashboard
streamlit run geesp_unified_app.py

# 4. Open browser → http://localhost:8501

# 5. Test features:
#    - Drag weight sliders (6 criteria)
#    - See map update in real-time
#    - View LCOE results (USD/kWh)
#    - Download results
```

---

## 🌍 Once Authenticated with Real Data

After Earth Engine setup, generate real satellite maps:

1. Edit `geesp_unified_app.py` → Change `USE_SYNTHETIC_DATA=False`
2. Set study area boundaries (Angola coordinates)
3. Dashboard auto-downloads satellite imagery:
   - NASA POWER (solar)
   - Sentinel-2 (NDVI)
   - SRTM (slope)
   - WorldPop (population)
   - VIIRS (nightlights)

---

## 📖 Documentation References

- **Full setup guide:** `DEPENDENCIES_AND_SETUP.md`
- **Code audit:** `CODE_FUNCTIONALITY_AUDIT.md`
- **Scientific manuscript:** `01_Science/manuscript/SOL.tex`
- **Framework:** 6-criteria MCDA for community solar in Angola

---

## ✅ Success Checklist

After setup, verify:

```
☐ Python 3.10+ installed
☐ All 48 packages installed (or 14 app-only)
☐ 6 map files in data/processed/ (~6 MB)
☐ .env configuration created
☐ (Optional) Earth Engine credentials configured
☐ Dashboard launches without errors
☐ Can move weight sliders
☐ LCOE calculator produces output
```

---

## 🚀 You're Ready!

```bash
streamlit run geesp_unified_app.py
```

**Performance expectations:**
- Dashboard load: <2 seconds
- Map update (slider move): <1 second  
- LCOE calculation: <500ms
- Download report: <2 seconds

---

**GEESP-Angola: Multi-Criteria Decision Analysis for Community Solar Sites**  
*6 criteria • 500×500 pixel maps • Real-time weighting • Financial analysis*

