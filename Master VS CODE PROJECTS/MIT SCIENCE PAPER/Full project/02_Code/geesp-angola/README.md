# GEESP-Angola: Geospatial Energy for Equity & Solar Planning

**Version**: 1.0 | **Status**: ✅ Production Ready | **Date**: 2026-02-10

---

## 🚀 Quick Start (One-Click Launch)

### Windows
Double-click: **`launch_app.bat`**

### Linux/macOS
```bash
chmod +x launch_app.sh
./launch_app.sh
```

### Cross-Platform (Python)
```bash
python launch_app.py
```

**The app will automatically:**
- Check Python installation
- Install dependencies if needed
- Create necessary directories
- Launch the web application
- Open in your browser at http://localhost:8501

---

## 📋 What Is GEESP-Angola?

A comprehensive Python framework for **solar energy site selection, financial analysis, and project monitoring** in Angola.

### Core Capabilities

- 🗺️ **Map Generation** — Create 6 spatial analysis layers from satellite data
- 🎯 **MCDA Analysis** — Multi-criteria decision analysis for site ranking
- 💰 **LCOE Calculator** — Financial viability analysis for 3 solar technologies
- 📊 **Monitoring Dashboard** — Track projects post-implementation
- ⚙️ **Configuration Management** — Centralized settings

---

## 📖 Documentation

All documentation is consolidated in the `docs/` directory:

- **[CAPABILITIES.md](docs/CAPABILITIES.md)** — Complete feature list, installation, user guide, API reference
- **[IMPROVEMENTS.md](docs/IMPROVEMENTS.md)** — Roadmap, planned improvements, quality metrics

**Quick Links:**
- Installation: See [CAPABILITIES.md](docs/CAPABILITIES.md#installation--setup)
- User Guide: See [CAPABILITIES.md](docs/CAPABILITIES.md#user-guide)
- Improvements: See [IMPROVEMENTS.md](docs/IMPROVEMENTS.md)

---

## 🏗️ Project Structure

```
geesp-angola/
├── geesp_unified_app.py      # Main application (launch this)
├── launch_app.bat            # Windows launcher
├── launch_app.sh             # Linux/macOS launcher
├── launch_app.py             # Cross-platform launcher
│
├── docs/                     # Consolidated documentation
│   ├── CAPABILITIES.md       # Features, installation, user guide
│   └── IMPROVEMENTS.md       # Roadmap, improvements, metrics
│
├── scripts/                  # Core modules
│   ├── generate_maps_simple.py   # Map generation
│   ├── mcda_analysis.py          # MCDA engine
│   ├── lcoe_calculator.py        # Financial analysis
│   ├── config_loader.py          # Configuration
│   └── ...
│
├── utils/                    # Shared utilities
│   ├── logging_setup.py     # Centralized logging
│   ├── error_handlers.py     # Error handling
│   └── ...
│
├── dashboard/                # Dashboard components
├── monitoring/               # Monitoring app
├── models/                   # Database models
├── tests/                    # Test suite
│
├── data/                     # Data directory
│   └── processed/            # Generated maps (.npy files)
│
├── requirements-app.txt      # Application dependencies
└── config.json              # Configuration (auto-generated)
```

---

## ⚡ Installation

### Option 1: One-Click Launch (Recommended)
Use the launcher scripts above - they handle everything automatically.

### Option 2: Manual Installation

```bash
# 1. Install dependencies (use app-only file; full dev: requirements.txt)
pip install -r requirements-app.txt

# 2. Run the app
streamlit run geesp_unified_app.py
```

**Requirements files:** `requirements-app.txt` = run the app. `requirements.txt` = full stack (GEE, geospatial, optional DB).

### Option 3: Docker

```bash
docker build -f Dockerfile.app -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```

---

## 🎯 Typical Workflow

1. **Launch App** → Double-click `launch_app.bat` (Windows) or `./launch_app.sh` (Linux/Mac)
2. **Generate Maps** → Go to Map Generation tab, click "Generate Maps"
3. **Run MCDA** → Adjust weights, compute integrated aptitude
4. **Calculate LCOE** → Compare technologies, review costs
5. **Monitor Projects** → Track performance and KPIs

**Total Time:** 15-30 minutes for complete analysis

---

## 📊 Features Overview

### Map Generation
- Solar irradiance, population density, grid distance
- Terrain slope, NDVI (vegetation), integrated aptitude
- Output: 6 `.npy` files + metadata JSON

### MCDA Analysis
- Adjustable weight sliders (5 criteria)
- Real-time weight validation
- Three-class classification (High/Medium/Low)
- Sensitivity analysis

### LCOE Calculator
- Compare 3 technologies (PV Fixed, Tracker, Hybrid)
- Financial metrics (NPV, IRR, Payback)
- Technology recommendations

### Monitoring
- Project status dashboard
- KPI tracking (generation, efficiency)
- Database-connected (with fallback)

---

## 🔧 Configuration

Configuration is managed via `config.json` (auto-generated on first run).

**Key Settings:**
- Map dimensions: `map_generation.output_shape`
- MCDA weights: `mcda.default_weights`
- LCOE parameters: `lcoe.standard_parameters`

**Access in code:**
```python
from scripts.config_loader import load_config
config = load_config()
weights = config.get_mcda_weights()
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run verification script
python verify_integration.py

# Run smoke tests
python scripts/smoke_test.py
```

**Test Status:** 88 tests, 100% pass rate, 62% coverage

---

## 🐛 Troubleshooting

### App won't start
- Check Python version: `python --version` (need 3.10+)
- Install dependencies: `pip install -r requirements-app.txt`
- Check port 8501 is available

### Maps not generating
- Ensure `data/processed/` directory exists
- Check write permissions
- Run manually: `python scripts/generate_maps_simple.py`

### Import errors
- Verify all dependencies installed
- Check Python path includes project directory
- Run: `python verify_integration.py`

**More help:** See [CAPABILITIES.md](docs/CAPABILITIES.md#troubleshooting)

---

## 📈 Current Status

**✅ Production Ready (MVP)**
- All core features working
- Critical bugs fixed
- Code consolidated and streamlined
- Documentation consolidated

**🔄 In Progress**
- Database initialization
- API authentication
- Test coverage expansion

**⏳ Planned**
- Advanced visualizations
- Real-time monitoring
- Cloud deployment

**See:** [IMPROVEMENTS.md](docs/IMPROVEMENTS.md) for detailed roadmap

---

## 📝 Requirements

- **Python**: 3.10+ (3.11 recommended)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk**: 2 GB for dependencies + data
- **OS**: Windows, macOS, or Linux

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👥 Authors

- **Rocélio Da Silva** (ISPTEC) - Lead Developer
- **Alexandre Dos Santos** (ISPTEC) - Backend & GEE Integration  
- **Delfina Mpanka** (ISPTEC) - Data & Validation

**Contact:** geesp-angola@isptec.ao  
**GitHub:** github.com/ISPTEC-Energy/geesp-angola

---

## 🎓 Acknowledgments

Developed for **MIT Climate Portal - Boston 2026**

---

**Last Updated:** 2026-02-10  
**Version:** 1.0  
**Status:** ✅ Production Ready
