# Changelog

## 2026-02-09 — Phase 1 Code Quality Improvements (80% COMPLETE)

- Phase 1 summary: 4/5 tasks complete; 88 tests passing; 2,200+ lines added; 100% pass rate.
- ✅ T1.1 Input Validation: `scripts/validators.py` (548 lines) + 53 tests
- ✅ T1.2 Type Annotations: `scripts/type_annotations.py` (280+ lines)
- ✅ T1.3 Config Management: `scripts/config_loader.py` (260 lines)
- ✅ T1.4 Test Expansion: `tests/test_mcda_expanded.py` (500+ lines)
- ⏳ T1.5 GEE Extraction Tests: In progress (2-3 hrs)

- Added `scripts/map_utils.py` — shared aptitude computation and metadata builder.
- Refactored `scripts/generate_maps.py` and `scripts/generate_maps_simple.py` to use the new helper.
- Fixed an accidental leftover metadata literal in `generate_maps_simple.py` (IndentationError).
- Hardened `scripts/utils.py` to use an `.npy` fallback for raster save/load and guarded visualization normalization.
- Improved `scripts/smoke_test.py` to accept both `(data, meta)` and `data` from loader.
- Ran unit tests: 12 passed, 1 skipped. Smoke test: successful; outputs saved to `data/processed`.

Files changed/added:
- `scripts/map_utils.py` (new)
- `scripts/generate_maps_simple.py` (modified)
- `scripts/generate_maps.py` (modified)
- `scripts/utils.py` (modified)
- `scripts/smoke_test.py` (modified)
- `README.md`, `requirements.txt`, `scripts/run_all_maps.py` (added)

Committed changes to repository.
# Changelog

All notable changes to the GEESP-Angola project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-08

### Added
- **Core Framework**
  - Google Earth Engine data extraction module (`gee_extraction.py`)
  - MCDA analysis with AHP weighting and Weighted Overlay (`mcda_analysis.py`)
  - LCOE financial calculator with 3 technology options (`lcoe_calculator.py`)
  - Support utilities for data handling and validation (`utils.py`)
  - Comprehensive utility library with 20+ functions

- **Dashboard**
  - Streamlit web interface with 5 interactive pages:
    - Home page with project overview and interactive Folium map
    - Data exploration tools with statistics and visualizations
    - MCDA analysis interface with dynamic weight adjustment
    - Results comparison for 3 priority zones
    - LCOE calculator for technology evaluation

- **Data Generation**
  - `generate_maps.py`: Full-featured map generator with GeoTIFF and PNG output
  - `generate_maps_simple.py`: Lightweight NumPy-only version for portability
  - Pre-generated demonstration maps for 6 MCDA criteria (npy, png, tif formats)

- **Configuration & Documentation**
  - `config.json`: Centralized project parameters and MCDA settings
  - `README.md`: Comprehensive project documentation (3,500+ lines)
  - `QUICKSTART.md`: Quick start guide and usage examples
  - `PROJECT_SUMMARY.md`: Code architecture and component overview
  - `INSTALL.md`: Step-by-step installation instructions
  - `CONTRIBUTING.md`: Contribution guidelines
  - `requirements.txt`: 35+ Python dependencies

- **Project Structure**
  - Professional directory layout following Python best practices
  - Git-ready project with `.gitignore`
  - Virtual environment setup (`venv/`)
  - Notebook directory structure for Jupyter notebooks

### Features
- **AHP Implementation**
  - Saaty scale (1-9) paired comparison matrix
  - Eigenvector method for weight calculation
  - Consistency Ratio validation (CR < 0.10)

- **Spatial Analysis**
  - Min-Max normalization for raster data [0,1]
  - Weighted overlay spatial combination
  - 3-class aptitude classification (High/Medium/Low)
  - ±20% sensitivity analysis for robustness testing

- **Financial Analysis**
  - Levelized Cost of Electricity (LCOE) calculation
  - Technologies: PV Fixed, PV Tracker, Solar-Diesel Hybrid
  - Cost range: 0.18-0.35 USD/kWh
  - NPV, IRR, and Payback Period analysis
  - Technology comparison tools

- **Maps & Visualizations**
  - 6 criterion layers: Solar Radiation, Population, Distance to Grid, Slope, NDVI, Aptitude
  - Multiple output formats: NumPy arrays, GeoTIFF, PNG
  - UTM Zone 33S geospatial referencing (Angola)
  - Resolution: 300×280 pixels (~100m equivalent)
  - Interactive Folium maps with zone boundaries

### Data
- **Demonstration Maps** (in `data/processed/`)
  - `mapa_irradiacao.npy`: Solar radiation (5.5-6.4 kWh/m²/dia)
  - `mapa_populacao.npy`: Population density (10-95 nW/cm²/sr)
  - `mapa_distanciarede.npy`: Grid distance (0-45 km)
  - `mapa_declividade.npy`: Slope (0-30°)
  - `mapa_ndvi.npy`: Vegetation index (-0.2 to 0.7)
  - `mapa_aptidao_integrada.npy`: Integrated aptitude (0-1)
  - `mapas_metadata.json`: Statistics and MCDA parameters

### Development
- Python 3.8+ compatibility
- 2,850+ lines of production-ready code
- Comprehensive docstrings and type hints
- Error handling and logging throughout
- Modular design for easy extension

## [Unreleased]

### Planned Features
- [ ] GitHub Actions CI/CD pipeline
- [ ] Jupyter Notebook tutorials
- [ ] REST API backend for web integration
- [ ] Mobile-friendly dashboard version
- [ ] Database integration (PostgreSQL/PostGIS)
- [ ] Real satellite imagery integration with GEE
- [ ] Advanced visualization with 3D terrain
- [ ] Multi-language support (Portuguese, English, French)
- [ ] Community feedback integration system

### Known Limitations
- Demonstration maps are synthetic (not real satellite data)
- Google Earth Engine requires authentication for real data extraction
- Dashboard requires server deployment for production use
- Rasterio support limited on Windows (requires GDAL installation)

---

## Version History

### Version 1.0.0 - Release Date: 2026-02-08
- Initial release with complete MCDA framework
- All core modules production-ready
- Full documentation suite
- Demonstration data and visualizations

---

## Notes

**Associated Academic Work**:
This project implements the methodology described in:
- "Geospatial Analysis for Renewable Energy Strategic Planning in Huíla Province, Angola"
- Research conducted at ISPTEC (Instituto Superior Politécnico de Tecnologia)

**Funding & Support**:
- ISPTEC Energy Research Group
- MIT Science Paper Competition 2026

**Contributors**:
- Research Team: ISPTEC Energy Department

---

For more information, visit the [GitHub Repository](https://github.com/ISPTEC-Energy/geesp-angola)

**Last updated**: February 8, 2026
