# GEESP-Angola: Project Structure Guide

**Last Updated**: 2026-02-10

---

## 📁 Directory Structure

```
geesp-angola/
│
├── 📄 README.md                    # Main entry point (start here!)
├── 📄 launch_app.bat              # Windows launcher (double-click to run)
├── 📄 launch_app.sh                # Linux/macOS launcher
├── 📄 launch_app.py                # Cross-platform Python launcher
│
├── 📁 docs/                        # Consolidated documentation
│   ├── CAPABILITIES.md             # Features, installation, user guide
│   └── IMPROVEMENTS.md             # Roadmap, improvements, metrics
│
├── 📁 scripts/                     # Core modules
│   ├── generate_maps_simple.py     # Map generation (main)
│   ├── mcda_analysis.py            # MCDA engine
│   ├── lcoe_calculator.py          # Financial analysis
│   ├── config_loader.py            # Configuration management
│   ├── earth_engine_integration.py # GEE integration
│   └── ...
│
├── 📁 utils/                       # Shared utilities
│   ├── logging_setup.py            # Centralized logging
│   ├── error_handlers.py           # Error handling
│   └── ...
│
├── 📁 dashboard/                   # Dashboard components
│   ├── app.py                      # Dashboard app (legacy)
│   └── utils/                      # Dashboard utilities
│
├── 📁 monitoring/                  # Monitoring app
│   └── monitoring_app.py           # Post-implementation monitoring
│
├── 📁 models/                      # Database models
│   └── monitoring.py               # SQLAlchemy models
│
├── 📁 tests/                       # Test suite
│   ├── test_mcda.py                # MCDA tests
│   ├── test_lcoe.py                # LCOE tests
│   └── ...
│
├── 📁 data/                        # Data directory
│   └── processed/                  # Generated maps (.npy files)
│
├── 📁 k8s/                         # Kubernetes manifests
│   └── geesp-deployment.yaml       # K8s deployment config
│
├── 📄 geesp_unified_app.py         # ⭐ MAIN APPLICATION (use this!)
├── 📄 requirements-app.txt          # Application dependencies
├── 📄 config.json                  # Configuration (auto-generated)
└── 📄 Dockerfile.app               # Docker configuration
```

---

## 🎯 Key Files

### Main Application
- **`geesp_unified_app.py`** — Unified Streamlit app (main entry point)
  - Use this file to run the application
  - Contains all 6 modules: Home, Maps, MCDA, LCOE, Monitoring, Settings

### Launchers
- **`launch_app.bat`** — Windows one-click launcher
- **`launch_app.sh`** — Linux/macOS one-click launcher  
- **`launch_app.py`** — Cross-platform Python launcher

### Documentation
- **`README.md`** — Main documentation (start here)
- **`docs/CAPABILITIES.md`** — Complete feature list and user guide
- **`docs/IMPROVEMENTS.md`** — Roadmap and planned improvements

### Core Modules
- **`scripts/generate_maps_simple.py`** — Map generation
- **`scripts/mcda_analysis.py`** — Multi-criteria decision analysis
- **`scripts/lcoe_calculator.py`** — Financial analysis
- **`scripts/config_loader.py`** — Configuration management

### Utilities
- **`utils/logging_setup.py`** — Centralized logging
- **`utils/error_handlers.py`** — Error handling decorators

---

## 🚀 How to Run

### Option 1: One-Click Launch (Easiest)
- **Windows**: Double-click `launch_app.bat`
- **Linux/Mac**: Run `./launch_app.sh`

### Option 2: Command Line
```bash
streamlit run geesp_unified_app.py
```

### Option 3: Python Launcher
```bash
python launch_app.py
```

---

## 📦 Dependencies

Install dependencies:
```bash
pip install -r requirements-app.txt
```

---

## 🔧 Configuration

Configuration is stored in `config.json` (auto-generated on first run).

**Key settings:**
- Map dimensions: `map_generation.output_shape`
- MCDA weights: `mcda.default_weights`
- LCOE parameters: `lcoe.standard_parameters`

---

## 📊 Data Files

**Generated Maps** (in `data/processed/`):
- `mapa_irradiacao.npy` — Solar irradiance
- `mapa_populacao.npy` — Population density
- `mapa_distancia_rede.npy` — Grid distance
- `mapa_declive.npy` — Terrain slope
- `mapa_ndvi.npy` — Vegetation index
- `mapa_aptidao_integrada.npy` — Integrated aptitude

**Generate maps:**
```bash
python scripts/generate_maps_simple.py
```

---

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Verify integration:
```bash
python verify_integration.py
```

---

## 📝 Notes

- **Main app**: Always use `geesp_unified_app.py` (with underscore)
- **Legacy app**: `geesp-unified-app.py` (with hyphen) is deprecated
- **Documentation**: All consolidated in `docs/` directory
- **Backups**: Redundant docs archived in `docs/_archived_redundant/`

---

*For detailed information, see README.md and docs/CAPABILITIES.md*
