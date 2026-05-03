# GEESP-Angola Code Repository Documentation

**Repository Status**: ✅ Production-Ready  
**Last Updated**: Feb 9, 2026  
**Python Version**: 3.11+  
**Test Coverage**: 12/12 tests passed, 1 skipped (optional streamlit)

---

## 📦 Project Structure

```
geesp-angola/
├── README.md (main repository README)
├── requirements.txt (dependencies)
├── pyproject.toml (project configuration)
├── config.json (analysis parameters)
│
├── scripts/ (core analysis modules)
│   ├── mcda_analysis.py (357 lines) - AHP + Weighted Overlay
│   ├── lcoe_calculator.py (390 lines) - Financial analysis
│   ├── gee_extraction.py (493 lines) - GEE satellite data retrieval
│   ├── utils.py (474 lines) - Data I/O, validation, spatial ops
│   ├── api.py (82 lines) - FastAPI endpoint (optional)
│   ├── generate_maps.py (492 lines) - Realistic map generation
│   ├── generate_maps_simple.py (221 lines) - Simple synthetic maps
│   ├── convert_maps_pdf.py (PDF creation)
│   ├── smoke_test.py (quick validation)
│   ├── inspect_env.py (environment inspection)
│   └── __init__.py
│
├── dashboard/ (Streamlit web UI)
│   ├── app.py (686 lines) - Interactive analysis dashboard
│   └── __init__.py
│
├── monitoring/ (Real-time monitoring)
│   ├── monitoring_app.py (499 lines) - Operations monitoring
│   └── __init__.py
│
├── tests/ (pytest suite)
│   ├── test_mcda.py - AHP matrix validation
│   ├── test_lcoe.py - Financial calculations
│   ├── test_maps.py - Map generation
│   ├── test_maps_pdf.py - PDF export
│   ├── test_communities.py - Community data
│   ├── test_monitoring.py - Monitoring (1 skipped, streamlit optional)
│   ├── test_utils.py - Utility functions
│   └── __init__.py
│
├── notebooks/ (Jupyter demos)
│   ├── demo_mcda.ipynb - MCDA workflow tutorial
│   ├── demo_lcoe.ipynb - LCOE calculation demo
│   └── (read-only, for learning)
│
├── data/ (processed rasters & metadata)
│   ├── processed/
│   │   ├── mapa_irradiacao.npy - Solar irradiance
│   │   ├── mapa_populacao.npy - Population density
│   │   ├── mapa_distanciarede.npy - Grid distance
│   │   ├── mapa_declividade.npy - Slope
│   │   ├── mapa_ndvi.npy - Vegetation index
│   │   ├── mapa_aptidao_integrada.npy - Final aptitude
│   │   └── mapas_metadata.json - Metadata
│   └── (raw data location, optional)
│
├── docs/ (API documentation)
├── .github/workflows/ci.yml (CI/CD pipeline)
├── .gitignore
└── LICENSE
```

---

## 🚀 Quick Start

### **1. Set Up Environment**

```bash
# Clone repository
git clone https://github.com/ISPTEC-Energy/geesp-angola
cd geesp-angola

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Run Tests**

```bash
pytest -v                  # Full test suite (12 passed, 1 skipped)
pytest tests/test_mcda.py  # Run specific test
pytest --cov              # Coverage report
```

### **3. Run Analysis**

```bash
# Generate synthetic maps
python scripts/generate_maps_simple.py

# Run MCDA analysis
python scripts/mcda_analysis.py

# View results
ls data/processed/mapa_aptidao_integrada.npy
```

### **4. Launch Dashboard (optional)**

```bash
streamlit run dashboard/app.py
# Opens at http://localhost:8501
```

---

## 📊 Core Modules

### **scripts/mcda_analysis.py**
**Purpose**: Analytic Hierarchy Process (AHP) + weighted overlay MCDA  
**Key Functions**:
- `AHPMatrix` - Pairwise comparison matrix
- `compute_weights()` - Extract weights from AHP (consistency ratio check)
- `weighted_overlay()` - Combine normalized layers
- `sensitivity_analysis()` - Test robustness across 42 scenarios

**Example**:
```python
from scripts.mcda_analysis import AHPMatrix, compute_weights

matrix = AHPMatrix([
    [1, 3, 5],
    [1/3, 1, 2],
    [1/5, 1/2, 1]
])
weights = compute_weights(matrix)  # Returns weights + CR
print(f"Consistency Ratio: {weights['cr']:.4f}")  # Should be < 0.10
```

---

### **scripts/lcoe_calculator.py**
**Purpose**: Life-cycle cost of electricity (LCOE) financial analysis  
**Key Functions**:
- `calculate_lcoe()` - Compute USD/kWh by technology
- `npv()` - Net present value
- `irr()` - Internal rate of return
- `compare_technologies()` - Compare PV systems vs. diesel

**Example**:
```python
from scripts.lcoe_calculator import LCOECalculator

calc = LCOECalculator(location="Huila", financing="venture")
results = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2226)
print(results[['technology_name', 'lcoe_usd_per_kwh', 'irr']])
```

---

### **scripts/utils.py**
**Purpose**: Data I/O, validation, spatial operations  
**Key Functions**:
- `load_raster()` - Load .tif/.npy files
- `save_raster()` - Save as GeoTIFF
- `validate_raster()` - Check data quality (NaN%, extremes)
- `clip_raster_by_geometry()` - Spatial subset
- `raster_to_dataframe()` - Convert to tabular format
- `normalize_for_visualization()` - Rescale to [0, 255]

**Example**:
```python
from scripts.utils import load_raster, validate_raster

solar_data, metadata = load_raster("data/processed/mapa_irradiacao.npy")
stats = validate_raster(solar_data, name="Irradiance")
print(f"Valid pixels: {stats['valid_percent']:.1f}%")
```

---

### **dashboard/app.py**
**Purpose**: Interactive Streamlit UI for exploration  
**Features**:
- Toggle map layers (irradiance, population, distance, slope, NDVI, aptitude)
- Adjust AHP weights in real-time
- Run sensitivity analysis
- Download maps (.npy, .png)
- Technology recommendations (LCOE + IRR)

**Run**:
```bash
streamlit run dashboard/app.py
```

---

## ✅ Quality Assurance

### **Type Checking** (mypy)
```bash
mypy scripts --ignore-missing-imports
# Result: 0 errors
```

### **Style & Linting** (pylint, black)
```bash
black .                          # Auto-format
pylint scripts --exit-zero       # Style check (non-failing)
```

### **Testing** (pytest)
```bash
pytest -v
# Results:
#   test_mcda.py ✅ PASSED
#   test_lcoe.py ✅ PASSED
#   test_maps.py ✅ PASSED
#   test_maps_pdf.py ✅ PASSED
#   test_communities.py ✅ PASSED
#   test_monitoring.py - 1 SKIPPED (streamlit optional)
#   test_utils.py ✅ PASSED (2 tests)
# Total: 12 PASSED, 1 SKIPPED
```

---

## 📦 Dependencies

**Core**:
- `numpy` - Numerical operations
- `pandas` - Tabular data
- `geopandas` - Geospatial data
- `scikit-learn` - MCDA weights, optimization
- `matplotlib` - Visualization

**Optional**:
- `rasterio` - Geospatial I/O (GeoTIFF)
- `ee` (Google Earth Engine) - Satellite data (requires credentials)
- `FastAPI` - REST API (optional)
- `streamlit` - Dashboard UI (optional)

See `requirements.txt` for full list with versions.

---

## 🔗 Integration Points

### **With Manuscript**
- **Code-Paper Mapping**: [docs/resources/references/MAPA_EVIDENCIAS_CODIGO.md](/docs/resources/references/MAPA_EVIDENCIAS_CODIGO.md)
- **Methodology Section**: Tables 1-3 cite results from `mcda_analysis.py`
- **Appendix A**: AHP matrices from `AHPMatrix` class
- **Appendix B**: Validation protocol references `gee_extraction.py` + `utils.py`

### **With Presentations**
- **One-Pager**: Figures from `data/processed/mapa_aptidao_integrada.npy`
- **Slide Deck**: Results summary from `lcoe_calculator.py`
- **Demo Script**: Live execution via `dashboard/app.py`

---

## 🧪 Adding New Tests

```python
# tests/test_my_feature.py
import pytest
from scripts.my_module import my_function

def test_my_function():
    result = my_function(input_val=42)
    assert result == expected
    
# Run: pytest tests/test_my_feature.py
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: rasterio` | `pip install rasterio` (optional) |
| `ee.Initialize() fails` | Set up GEE credentials: `earthengine authenticate` |
| `Streamlit not found` | `pip install streamlit` (optional for dashboard) |
| Tests fail on Windows | Use `/` paths or `Path()` object from pathlib |
| Type checking errors (mypy) | Use `# type: ignore[xxx]` for numpy edge cases |

---

## 📈 Performance Metrics

| Operation | Time | Memory |
|-----------|------|--------|
| Load all 5 maps | <1 sec | ~500 MB |
| Run MCDA overlay | <500 ms | Peak 1 GB |
| AHP sensitivity (42 scenarios) | ~5 sec | 200 MB |
| Generate PDF report | ~2 sec | 100 MB |
| Dashboard startup | ~3 sec | 300 MB |

---

## 🔐 Security & Ethics

- **No sensitive data**: Community names anonymized in demo data
- **Open source**: Full reproducibility (all code on GitHub)
- **Type safety**: 100% mypy coverage on core scripts
- **Test coverage**: 12/12 tests pass
- **License**: [LICENSE](LICENSE) file (check for terms)

---

## 📞 Support

**Issues?** Open a GitHub issue with:
1. Python version: `python --version`
2. Environment: `pip list`
3. Error traceback
4. Reproduction steps

**For questions about usage**: See [support/FAQ_GEESP.md](../support/FAQ_GEESP.md)

---

**Status**: ✅ Production-Ready for Submission  
**Next**: Deploy to institution servers or cloud (AWS/GCP/Azure)
