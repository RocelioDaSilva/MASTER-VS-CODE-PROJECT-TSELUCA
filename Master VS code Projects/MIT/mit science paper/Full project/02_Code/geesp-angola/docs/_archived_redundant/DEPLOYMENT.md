# 📦 GEESP-Angola: Deployment Guide

Complete instructions to deploy GEESP-Angola to GitHub and run locally.

## 1. Local Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool

### Quick Start

```bash
# Clone repo (or skip if you cloned already)
git clone https://github.com/YOUR-USERNAME/geesp-angola.git
cd geesp-angola

# Create and activate venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows PowerShell

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install optional packages (recommended)
pip install fastapi uvicorn streamlit > /dev/null 2>&1

# Run tests
python -m pytest -q

# Launch dashboard
streamlit run dashboard/app.py
```

Dashboard will be available at: **http://localhost:8501**

## 2. Running Tests Locally

```bash
# All tests
python -m pytest -q

# Specific test file
python -m pytest tests/test_mcda.py -v

# With coverage
python -m pytest --cov=scripts tests/
```

## 3. API Server (FastAPI)

```bash
# Start API server
python -m uvicorn scripts.api:app --host 0.0.0.0 --port 8000

# Test endpoint
curl -X POST http://localhost:8000/mcda \
  -H "Content-Type: application/json" \
  -d '{"weights":{"mapa_irradiacao":0.25,"mapa_populacao":0.25,"mapa_distanciarede":0.2,"mapa_declividade":0.15,"mapa_ndvi":0.15}}'
```

Swagger docs: http://localhost:8000/docs

## 4. GitHub Setup (First Time)

### A. Create Remote Repository

```bash
# Option 1: Using GitHub CLI (if installed)
gh auth login  # Authenticate if needed
gh repo create geesp-angola --public --source=. --remote=origin --push

# Option 2: Manual (create repo on GitHub.com first)
# 1. Go to https://github.com/new
# 2. Name: geesp-angola
# 3. Description: "GEESP-Angola: Geospatial Energy for Equity and Solar Planning"
# 4. Public, Add README/license (optional—we have these)
# 5. Create repository
# 6. Copy the HTTPS URL
```

### B. Initialize Local Git & Push

```bash
cd geesp-angola

# Initialize git (if not already done)
git init

# Configure user (if first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# First commit
git commit -m "Initial commit: GEESP-Angola project structure, modules, tests, dashboard"

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/geesp-angola.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### C. Verify Push

```bash
git log --oneline
git remote -v
# Should show "origin" pointing to your GitHub repo
```

## 5. GitHub Settings (After First Push)

1. **Enable GitHub Actions** (for CI/CD):
   - Go to repo Settings → Actions → General
   - Allow all actions and workflows

2. **Enable GitHub Pages** (optional, for docs):
   - Go to Settings → Pages
   - Source: Deploy from a branch → main → /root

3. **Branch Protection** (optional, for safety):
   - Settings → Branches → Add rule
   - Pattern: main
   - Require status checks to pass

## 6. Continuous Integration (CI)

GitHub Actions workflow is already set up at `.github/workflows/ci.yml`.

**What it does:**
- Runs on every push and pull request
- Runs Python 3.11 with pytest
- Checks code quality

**View CI status:**
- Go to repo → Actions tab
- See build status on main branch

## 7. Collaboration & Contributions

```bash
# Create a feature branch
git checkout -b feature/add-gee-scripts

# Make changes, commit, and push
git add .
git commit -m "Add GEE extraction scripts"
git push origin feature/add-gee-scripts

# Open Pull Request on GitHub and request review
```

## 8. Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["streamlit", "run", "dashboard/app.py"]
```

Build and run:

```bash
docker build -t geesp-angola .
docker run -p 8501:8501 -p 8000:8000 geesp-angola
```

## 9. Project Structure Checklist

- ✅ `scripts/` - Core modules (MCDA, LCOE, GEE, utils)
- ✅ `dashboard/` - Streamlit web app
- ✅ `data/processed/` - Generated maps (.npy, .pdf, .png) + communities_45.csv
- ✅ `notebooks/` - Demo Jupyter notebook
- ✅ `tests/` - Unit tests
- ✅ `.github/workflows/` - CI/CD pipeline
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Git ignore rules
- ✅ `README.md` - Project overview
- ✅ `INSTALL.md` - Installation guide
- ✅ `pyproject.toml` - Build configuration
- ✅ `.pre-commit-config.yaml` - Code quality hooks

## 10. Troubleshooting

### git: Command not found
→ Install Git from https://git-scm.com

### ModuleNotFoundError: No module named 'streamlit'
```bash
pip install streamlit
```

### Port 8501 already in use
```bash
streamlit run dashboard/app.py --server.port 8502
```

### Tests fail with import errors
```bash
# Add current dir to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%           # Windows
python -m pytest -q
```

## 11. Recommended Next Steps

1. **Authenticate with Google Earth Engine** (for GEE extraction)
   ```bash
   python -m pip install earthengine-api
   ee_jupyter.authenticate()  # or similar in your script
   ```

2. **Run full GEE pipeline** (once GEE is available):
   ```bash
   python scripts/gee_extraction.py
   ```

3. **Set up pre-commit hooks** (for code quality):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Monitor GitHub Actions** after pushes

5. **Invite collaborators** on GitHub to work together

## 12. Support & Issues

- **Documentation**: See `README.md`, `INSTALL.md`, `docs/` folder
- **Issues**: Create issue on GitHub → Issues tab
- **Discussions**: Use GitHub Discussions for questions

---

**Happy coding! 🚀**
