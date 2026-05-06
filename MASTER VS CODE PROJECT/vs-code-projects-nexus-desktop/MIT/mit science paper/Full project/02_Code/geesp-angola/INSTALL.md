# Installation Guide - GEESP Angola

## Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Virtual environment** (recommended)

## Step 1: Clone the Repository

```bash
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola
```

## Step 2: Create Virtual Environment

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Install Google Earth Engine API (Optional)

If you plan to extract data from Google Earth Engine:

```bash
pip install earthengine-api
earthengine authenticate
```

This will open a browser for authentication with your Google account.

## Step 5: Verify Installation

Test the installation:

```bash
python -c "import geopandas, streamlit, rasterio; print('All dependencies installed successfully!')"
python verify_integration.py
python -m pytest tests/ -q
```

## Step 6: Run the Application

To launch the unified Streamlit app (recommended):

```bash
python launch_app.py
# or
streamlit run geesp_unified_app.py
```

The app will open at `http://localhost:8501`. For dashboard-only: `streamlit run dashboard/app.py`

## Step 7: Generate Map Data (Optional)

Generate demonstration maps:

```bash
python scripts/generate_maps_simple.py
```

Output will be saved to `data/processed/`.

## Troubleshooting

### Module Import Errors
If you encounter import errors:
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check Python version: `python --version`

### Rasterio Installation Issues (Windows)
If rasterio fails to install:
1. Use conda instead: `conda install -c conda-forge rasterio`
2. Or install from wheels: `pip install --only-binary :all: rasterio`

### Google Earth Engine Authentication
If earthengine authentication fails:
1. Visit https://earthengine.google.com/ and sign up
2. Re-run `earthengine authenticate`
3. Check that you have access to GEE datasets

### OneDrive/CloudSync Issues
If files on OneDrive cause synchronization problems:
1. Move the project folder outside OneDrive
2. Or configure OneDrive to not sync the `venv/` and `data/processed/` folders

## Development Setup

If you plan to contribute to the project:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 jupyter

# Install pre-commit hooks (if added)
pre-commit install

# Run tests
pytest

# Format code
black scripts/ dashboard/
```

## Docker Setup (Optional)

If you have Docker installed:

```bash
docker build -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for common workflows
- Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for project overview
- Review [README.md](README.md) for detailed documentation
- Explore `scripts/` directory for available modules
- Open Jupyter notebooks in `notebooks/` for interactive analysis

## Support

For issues or questions:
1. Check the [README.md](README.md) FAQ section
2. Review existing GitHub issues
3. Create a new GitHub issue with detailed information
4. Contact the development team

---

**Última atualização**: Fevereiro, 2026
