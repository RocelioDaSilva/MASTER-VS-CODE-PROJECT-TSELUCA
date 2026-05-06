# 🚀 Getting Started with GEESP-Angola

**Consolidated Master Guide** | Merged from: GETTING_STARTED.md, INSTALL.md, QUICKSTART.md, QUICK_REFERENCE.md  
**Last Updated**: March 6, 2026  
**Status**: Production Ready  

---

## ⚡ Quick Start (5 Minutes)

### Windows (One-Click)
```bash
# Method 1: Double-click
launch_app.bat

# Method 2: PowerShell
.\launch_app.bat
```

### Linux/macOS (One-Click)
```bash
# Make executable
chmod +x launch_app.sh

# Run
./launch_app.sh
```

### Python (Cross-Platform)
```bash
python launch_app.py
```

**The app will automatically:**
- Check Python installation
- Install dependencies if needed
- Create necessary directories
- Launch Streamlit at http://localhost:8501

---

## 📦 Complete Installation Guide

### System Requirements
- **Python**: 3.8+ (3.10+ recommended)
- **OS**: Windows, macOS, Linux
- **Disk**: ~500MB for dependencies
- **RAM**: 2GB minimum (4GB recommended)
- **Internet**: For Google Earth Engine authentication

### Step 1: Clone Repository
```bash
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate.ps1
# Or with batch file:
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip and Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Optional - Google Earth Engine Authentication
If you need to extract satellite data:

```bash
# Install EE API
pip install earthengine-api

# Authenticate (opens browser)
earthengine authenticate
```

### Step 5: Verify Installation
```bash
# Test critical imports
python -c "import streamlit, geopandas, rasterio; print('✅ All dependencies installed!')"

# Run integration tests
python verify_integration.py

# Run pytest suite
pytest tests/ -q --tb=short
```

### Step 6: Launch Application

**Method A: Dashboard (Recommended)**
```bash
streamlit run geesp_unified_app.py
```

**Method B: Python Scripts**
```python
from scripts.gee_extraction import GEEExtractor
from scripts.mcda_analysis import MCDAnalyzer
from scripts.lcoe_calculator import LCOECalculator

# Example workflow
extractor = GEEExtractor()
mcda = MCDAnalyzer()
lcoe = LCOECalculator()
```

**Method C: Jupyter Notebooks**
```bash
jupyter notebook notebooks/
```

---

## 🎯 One-Time Setup

### Configuration (Optional)
If you need custom settings:

```bash
# Edit configuration
cp config.json.example config.json
# Then customize in your editor
```

### Environment Variables
```bash
# Create .env file
echo "GEE_PROJECT_ID=your-project-id" > .env
echo "GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json" >> .env
```

---

## 🗂️ Project Structure Overview

```
geesp-angola/
├── 🚀 launch_app.bat/sh/py    ← Run this to start!
├── 📄 README.md               ← Full documentation
├── 📄 geesp_unified_app.py    ← Main application
│
├── scripts/                   ← Core analysis modules
│   ├── gee_extraction.py      ← Map data extraction
│   ├── mcda_analysis.py       ← Multi-criteria analysis
│   └── lcoe_calculator.py     ← Financial analysis
│
├── dashboard/                 ← UI components
│   └── app.py                 ← Dashboard (legacy)
│
├── tests/                     ← 29 test files (46 total)
│   ├── test_mcda.py
│   ├── test_lcoe.py
│   └── test_integration_full_workflow.py
│
├── data/                      ← Data directory
│   └── communities_45.csv     ← Community data
│
└── docs/                      ← Documentation
    └── CAPABILITIES.md        ← Full feature guide
```

---

## 🆘 Troubleshooting

### "Python not found"
```bash
# On Windows, use py launcher
py -3.10 -m venv venv

# Or specify full path
C:\Python310\python.exe -m venv venv
```

### "Permission denied" (Linux/macOS)
```bash
chmod +x launch_app.sh
chmod +x venv/bin/activate
```

### "Module not found"
```bash
# Ensure venv is activated, then reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### "StreamlitAPIException"
```bash
# Clear cache and restart
rm -rf ~/.streamlit/
streamlit run geesp_unified_app.py --logger.level=debug
```

### "Google Earth Engine authentication failed"
```bash
# Re-authenticate
earthengine authenticate --auth_mode=notebook

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

---

## 📚 Next Steps

1. **First Run**: Double-click `launch_app.bat` (Windows) or run `./launch_app.sh` (Mac/Linux)
2. **Dashboard Tour**: Explore all 6 pages of the interface
3. **Run Sample Analysis**: Use example data in dashboard
4. **Read Documentation**: See `docs/CAPABILITIES.md` for detailed features
5. **Check Tests**: Review `tests/` for usage examples

---

## 🔗 Quick Reference Commands

```bash
# Activate environment (do this first!)
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate.ps1         # Windows

# Start app
streamlit run geesp_unified_app.py

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_mcda.py -v

# Code quality check
flake8 scripts/ --max-line-length=100

# Format code
black scripts/ dashboard/

# Generate coverage report
pytest --cov=scripts --cov-report=html

# Deactivate environment
deactivate
```

---

## 📞 Getting Help

- **Documentation**: See [README.md](README.md) and `docs/`
- **Issues**: Report via GitHub Issues
- **Examples**: Check `notebooks/` for Jupyter examples
- **Tests**: Review `tests/` for code usage patterns

---

**What's Next?** → Read [CAPABILITIES.md](docs/CAPABILITIES.md) for complete feature guide or jump to [MASTER_ARCHITECTURE.md](01_MASTER_ARCHITECTURE.md) to understand the codebase structure.
