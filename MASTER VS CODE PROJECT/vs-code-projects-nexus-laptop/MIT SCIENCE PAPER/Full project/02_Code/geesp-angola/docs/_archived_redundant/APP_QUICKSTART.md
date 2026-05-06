# 🚀 GEESP-Angola Unified App - Quick Start

**All-in-one application for solar site selection, financial analysis, and project monitoring**

---

## ⚡ 2-Minute Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements-unified.txt
```

### 2️⃣ Run the App
```bash
streamlit run geesp-unified-app.py
```

### 3️⃣ Open Browser
The app will automatically open at **http://localhost:8501**

---

## 📖 What's Inside?

The unified app has **6 integrated modules**:

| Module | Purpose | What You Can Do |
|--------|---------|-----------------|
| 🏠 **Home** | Overview & intro | Learn about the project |
| 🗺️ **Map Generation** | Create spatial layers | Generate & preview 6 GIS maps |
| 🎯 **MCDA Analysis** | Weighted site ranking | Adjust weights, compute suitability |
| 💰 **LCOE Calculator** | Financial analysis | Compare technologies, costs |
| 📊 **Monitoring** | Project tracking | Monitor post-implementation sites |
| ⚙️ **Settings** | Configuration | Customize all parameters |

---

## 🎯 Typical Workflow (15 min)

### Step 1: Generate Maps 🗺️
- Go to **Map Generation** tab
- Click **"🔄 Generate"** button
- View 6 spatial layers (solar, population, grid distance, slope, NDVI, aptitude)

### Step 2: Analyze with MCDA 🎯
- Go to **MCDA Analysis** tab
- Adjust **weight sliders** for each criterion
- Click **"📊 Compute"** button
- See integrated aptitude map + statistics


### Step 3: Calculate LCOE 💰
- Go to **LCOE Calculator**
- Enter capacity (MW) + irradiance (kWh/m²/year)
- Click **"Calculate LCOE"**
- Compare PV, Wind, Hybrid technologies

### Step 4: Review Monitoring 📊
- Go to **Monitoring**
- View sample project data
- Check KPIs (generation, efficiency, downtime)

### Step 5: Customize Settings ⚙️
- Go to **Settings**
- Adjust map resolution, MCDA defaults, LCOE parameters
- Click **"Save Settings"**

---

## 🖥️ System Requirements

- **Python**: 3.8+ (3.11 recommended)
- **RAM**: 2+ GB
- **Disk**: 500 MB
- **Browser**: Chrome, Firefox, Safari, Edge

---

## 📦 Deployment Options

### 🏠 Local
```bash
streamlit run geesp_unified_app.py
```
**Best for**: Development, testing, local analysis

### ☁️ Streamlit Cloud (Free!)
```bash
# Push to GitHub, then deploy at streamlit.io/cloud
# Your app: https://your-username-geesp-angola.streamlit.app
```
**Best for**: Sharing with others, no infrastructure needed

### 🐳 Docker
```bash
docker build -f Dockerfile.app -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```
**Best for**: Production, reproducibility, complex environments

### 💻 Desktop App (Windows/Mac)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed geesp_unified_app.py
# Executable: dist/GEESP-Angola.exe
```
**Best for**: End-user distribution, no Python installation required

*See [APP_DEPLOYMENT_GUIDE.md](APP_DEPLOYMENT_GUIDE.md) for detailed instructions*

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements-app.txt --upgrade
```

### Maps not loading
```bash
# Generate maps first
python scripts/generate_maps_simple.py
```

### Port 8501 already in use
```bash
streamlit run geesp_unified_app.py --server.port=8502
```

### Streamlit crashes
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements-app.txt --force-reinstall
```

---

## 📊 Data & Configuration

### Where is my data stored?
```
geesp-angola/
├── data/
│   └── processed/       ← Generated maps (.npy files)
├── logs/                ← Application logs
└── config.json          ← Settings (generated on first save)
```

### How do I customize parameters?
1. Go to **Settings** tab
2. Adjust sliders/inputs
3. Click **"Save Settings"**
4. Settings are saved to `config.json`

### Can I use custom data?
Yes! Replace files in `data/processed/`:
- `mapa_irradiacao.npy` — Solar irradiance
- `mapa_populacao.npy` — Population density
- `mapa_distanciarede.npy` — Grid distance
- `mapa_declividade.npy` — Terrain slope
- `mapa_ndvi.npy` — Vegetation index

---

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| App startup | 2–5 sec | First run slower |
| Map generation | 2–5 sec | Creates 6 layers |
| MCDA computation | <100 ms | Very fast |
| LCOE calculation | <500 ms | Technology comparison |
| Page load | <1 sec | With caching |

**Tip**: Use **Settings** to reduce map size for faster processing

---

## 🔐 Security

### Local Use
- No authentication needed
- Data stored locally in `data/` folder
- No external API calls

### Sharing Online
- Consider adding password via Streamlit secrets
- Don't share sensitive location data
- Use HTTPS (automatic on Streamlit Cloud)

---

## 📞 Support & Feedback

### Documentation
- [ANALYSIS_CODING_STATUS.md](ANALYSIS_CODING_STATUS.md) — Technical deep dive
- [UNIFIED_APP_PROPOSAL.md](UNIFIED_APP_PROPOSAL.md) — Architecture rationale
- [APP_DEPLOYMENT_GUIDE.md](APP_DEPLOYMENT_GUIDE.md) — Full deployment guide
- [README.md](README.md) — Project overview

### Get Help
- 🐙 [GitHub Issues](https://github.com/geesp-angola/geesp-angola/issues)
- 📧 Email: geesp@email.com
- 💬 Discussions: [GitHub Discussions](https://github.com/geesp-angola/geesp-angola/discussions)

---

## 🎓 Example Use Cases

### Use Case 1: Site Selection (30 min)
1. Generate maps
2. Adjust MCDA weights based on priorities
3. Identify top aptitude zones
4. Calculate LCOE for best sites

### Use Case 2: Feasibility Study (1 hour)
1. Import custom solar/population data
2. Run multiple MCDA scenarios
3. Compare LCOE across technologies
4. Export results for report

### Use Case 3: Community Planning (1 week)
1. Generate baseline maps
2. Run stakeholder workshops (adjust weights)
3. Create multiple scenarios (best/worst case)
4. Monitor implementation progress

---

## 🚀 Next Steps

1. **Run the app**: `streamlit run geesp_unified_app.py`
2. **Explore modules**: Click through each tab
3. **Generate maps**: Start with Map Generation → MCDA → LCOE
4. **Customize settings**: Adjust parameters for your region
5. **Share results**: Export/screenshot maps for reports

---

## 📋 Features Checklist

- ✅ Single unified app (no multiple tools)
- ✅ 6 integrated modules
- ✅ Interactive visualizations
- ✅ Configuration management
- ✅ Local data storage
- ✅ Responsive design (works on mobile)
- ✅ Docker support
- ✅ Free cloud deployment option

---

## 📝 Changelog

### v1.0 (2026-02-09)
- ✨ Initial unified app release
- 🗺️ Map generation module
- 🎯 MCDA analysis with weight sliders
- 💰 LCOE calculator with technology comparison
- 📊 Project monitoring dashboard
- ⚙️ Configuration management
- 🐳 Docker containerization
- 📚 Comprehensive documentation

---

**Ready to start?** 🚀

```bash
streamlit run geesp_unified_app.py
```

Open **http://localhost:8501** and explore!

---

*GEESP-Angola v1.0 | Geospatial Energy for Equity & Solar Planning*
