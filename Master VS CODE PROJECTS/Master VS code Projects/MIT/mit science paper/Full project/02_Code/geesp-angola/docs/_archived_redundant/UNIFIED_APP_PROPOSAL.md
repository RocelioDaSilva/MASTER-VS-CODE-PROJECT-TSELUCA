# GEESP-Angola: Consolidated App Architecture
**Date**: 2026-02-09 | **Question**: Can all components become a single app?
**Answer**: ✅ **Yes** — 3 viable approaches with effort/complexity tradeoffs

---

## 🎯 WHAT WE HAVE (Scattered Across Modules)

| Component | Current Form | Purpose |
|-----------|--------------|---------|
| Map Generation | 2 scripts | Create 6 GIS layers (solar, population, etc.) |
| MCDA Analysis | Module + tests | Weight layers; compute integrated aptitude |
| LCOE Calculator | Module + tests | Financial analysis (3 technologies) |
| Dashboard | Streamlit app | Visualize maps, MCDA results, LCOE estimates |
| Monitoring | Streamlit app | Post-implementation project tracking |
| REST API | FastAPI skeleton | Endpoint for MCDA computation |
| Configuration | Hardcoded | Weights, shapes, LCOE parameters |

**Current UX**: 3 separate tools (dashboard, monitoring, API)
**Goal**: 1 unified application

---

## 📊 THREE CONSOLIDATION OPTIONS

### **Option 1: Unified Streamlit Mega-App** ⭐ RECOMMENDED
**Complexity**: ⭐ Easiest | **Time**: 6-8 hours | **Portability**: Web-based

#### What It Is
Single Streamlit app with 5-6 tabs covering:
1. **🏠 Home** — Project intro, overview, documentation
2. **🗺️ Map Generation** — Generate maps, preview outputs
3. **🎯 MCDA Analysis** — Adjust weights, see results
4. **💰 LCOE Calculator** — Compare technologies, sensitivity
5. **📊 Monitoring** — Track post-implementation projects
6. **⚙️ Settings** — Configure map resolution, weights, LCOE params

#### Architecture
```
geesp-angola-unified-app.py (800 lines)
├── page_home() — Landing page + docs
├── page_map_generation() — Map controls + generation
├── page_mcda() — Weight sliders + visualization
├── page_lcoe() — Technology comparison
├── page_monitoring() — Project dashboard
├── page_settings() — Configuration panel
└── main() — Page routing + sidebar
```

#### Strengths
✅ Simplest to build (reuse existing Streamlit code)
✅ No backend server needed
✅ Session state handles data persistence
✅ Works on desktop, web, mobile browsers
✅ Deploy to Streamlit Cloud for free
✅ Users see all features in one place

#### Weaknesses
⚠️ Less scalable for high traffic
⚠️ Slower for large computations (Streamlit reruns entire script)
⚠️ No multi-user concurrent access
⚠️ Data lost on page refresh (unless cached)

#### Deployment
- **Local**: `streamlit run geesp-angola-unified-app.py`
- **Cloud**: Push to GitHub → Deploy on [Streamlit Cloud](https://streamlit.io/cloud) (free)
- **Docker**: `docker run -p 8501:8501 geesp-angola-app`

---

### **Option 2: Full Web Stack (FastAPI + React)** 🏢 PROFESSIONAL
**Complexity**: ⭐⭐⭐ Intermediate | **Time**: 20-30 hours | **Portability**: Web + mobile

#### What It Is
Backend API + modern frontend for enterprise deployment:
- **Backend**: FastAPI (Python) with async workers
- **Frontend**: React (JavaScript) with Plotly.js visualization
- **Database**: PostgreSQL for monitoring data
- **Deployment**: Docker Compose, Kubernetes-ready

#### Architecture
```
geesp-app-backend/
├── main.py — FastAPI app
├── routers/
│   ├── maps.py — Map generation endpoints
│   ├── mcda.py — MCDA analysis endpoints
│   ├── lcoe.py — LCOE calculator endpoints
│   └── monitoring.py — Project tracking endpoints
├── models/ — Pydantic data validation
├── database/ — SQLAlchemy ORM
└── config.py — Environment settings

geesp-app-frontend/
├── src/
│   ├── pages/
│   │   ├── Maps.jsx
│   │   ├── MCDA.jsx
│   │   ├── LCOE.jsx
│   │   └── Monitoring.jsx
│   ├── components/
│   ├── services/ — API calls
│   └── App.jsx
└── docker-compose.yml
```

#### Strengths
✅ Highly scalable (multiple users, concurrent requests)
✅ Persistent data (PostgreSQL)
✅ Professional UI/UX
✅ Mobile-friendly responsive design
✅ API-first (reusable from mobile apps)
✅ Production-grade error handling
✅ Authentication possible (users, permissions)

#### Weaknesses
❌ Much longer development time
❌ Requires DevOps knowledge
❌ More moving parts (backend, frontend, DB)
❌ Higher hosting costs
❌ Overkill for single-user/research use case

#### Deployment
- **Local dev**: `docker-compose up` (starts backend + frontend + DB)
- **Production**: AWS/Azure/GCP with load balancing
- **Time to production**: 20-30 hours dev + DevOps setup

---

### **Option 3: Desktop App (PyInstaller)** 💻 STANDALONE
**Complexity**: ⭐⭐ Moderate | **Time**: 8-12 hours | **Portability**: Windows/Mac/Linux

#### What It Is
Standalone executable that runs Streamlit mega-app without Python installation:
- Single `.exe` (Windows) or `.app` (Mac) file
- Streamlit bundled inside
- Double-click to launch

#### Architecture
```
geesp-app/
├── geesp-unified-app.py — Streamlit code (same as Option 1)
├── config/
│   ├── config.json
│   └── default_parameters.json
├── data/processed/ — Output directory
├── build_installer.py — PyInstaller script
└── README.md
```

**Build Script** (`build_installer.py`):
```python
import PyInstaller
import os

# Create standalone executable
os.system("""
pyinstaller --onefile \\
  --windowed \\
  --name "GEESP-Angola" \\
  --icon="logo.ico" \\
  geesp-unified-app.py
""")
# Output: dist/GEESP-Angola.exe (Windows)
```

#### Strengths
✅ No Python installation needed
✅ Simple distribution (send `.exe` file)
✅ Works offline (no internet required)
✅ Double-click launch (non-technical users)
✅ Same codebase as Option 1

#### Weaknesses
⚠️ Large file size (~500 MB with Streamlit bundled)
⚠️ Slower startup (first run ~30-60 seconds)
⚠️ Platform-specific builds (need Windows, Mac, Linux machines)
⚠️ No auto-updates (users must download new version)
⚠️ Antivirus may flag as suspicious

#### Deployment
- **Build**: `python build_installer.py`
- **Distribution**: Host `.exe` on website or GitHub Releases
- **User experience**: Click, run, use (no setup required)

---

## 🔄 COMPARISON MATRIX

| Factor | Streamlit Mega-App | FastAPI + React | PyInstaller |
|--------|-------------------|-----------------|-------------|
| **Time to Build** | 6–8h ⚡ | 20–30h 🐢 | 8–12h ⚡⚡ |
| **Complexity** | Simple | Complex | Moderate |
| **Multi-User** | No | Yes ✅ | No |
| **Persistent Data** | Session only | Database ✅ | Local files |
| **Scalability** | Single machine | Load balanced ✅ | N/A |
| **Mobile Support** | Responsive web | Native mobile ✅ | No |
| **Offline Support** | No | No | Yes ✅ |
| **Installation** | `pip install streamlit` | Docker + setup | Double-click ✅ |
| **Cost to Host** | Free (Streamlit Cloud) | ~$100/mo | One-time download |
| **Suitable For** | Individual users, demos, research | Teams, production, scaling | End-user distribution |

---

## 🚀 RECOMMENDED PATH: Streamlit Mega-App

**Why**: 
- Fastest to build (your team can deliver in 1 week)
- Perfect for research/analysis use case
- Can upgrade to FastAPI later if needed
- Users can run locally or via cloud
- Reuses all existing Streamlit code

**Timeline**:
- Day 1–2: Create `geesp-unified-app.py` skeleton; integrate existing pages
- Day 3: Add map generation controls + preview
- Day 4: Add settings/configuration tab
- Day 5: Testing + deployment to Streamlit Cloud
- **Total**: 5 days, 1 developer

---

## 📋 HOW TO BUILD: Streamlit Mega-App (Step-by-Step)

### Step 1: Create Main App File (2 hours)

**File**: `geesp-unified-app.py`

```python
import streamlit as st
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# Import existing modules
from mcda_analysis import AHPWeighter, MCDAnalyzer
from lcoe_calculator import LCOECalculator, SolarParameters
from generate_maps_simple import generate_all_maps
import utils

# ============================================================================
# PAGE ROUTING
# ============================================================================

st.set_page_config(
    page_title="GEESP-Angola",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
page = st.sidebar.radio(
    "📍 Select Page:",
    [
        "🏠 Home",
        "🗺️ Map Generation",
        "🎯 MCDA Analysis",
        "💰 LCOE Calculator",
        "📊 Monitoring",
        "⚙️ Settings"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("**GEESP-Angola v1.0**\nGeospatial Energy for Equity & Solar Planning")

# ============================================================================
# PAGE: HOME
# ============================================================================

if page == "🏠 Home":
    st.markdown("<h1 style='color: #1f77b4;'>GEESP-Angola</h1>", unsafe_allow_html=True)
    st.markdown("### Integrated Tool for Solar Planning in Angola")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Features:**
        - 🗺️ Generate 6 GIS map layers
        - 🎯 Multi-criteria decision analysis (MCDA)
        - 💰 Financial modeling (LCOE)
        - 📊 Project monitoring dashboard
        - ⚙️ Configurable parameters
        """)
    with col2:
        st.success("""
        **Use Cases:**
        - Site identification for solar projects
        - Feasibility analysis
        - Technology selection
        - Community site selection
        - Project performance tracking
        """)
    
    st.divider()
    st.subheader("Quick Start")
    st.markdown("""
    1. Go to **Map Generation** to create spatial layers
    2. Use **MCDA Analysis** to weight and rank sites
    3. Check **LCOE Calculator** for financial viability
    4. Track projects in **Monitoring** dashboard
    5. Adjust **Settings** as needed
    """)

# ============================================================================
# PAGE: MAP GENERATION
# ============================================================================

elif page == "🗺️ Map Generation":
    st.markdown("## 🗺️ Map Generation")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Generate spatial layers for MCDA analysis")
    with col2:
        if st.button("🔄 Generate Maps"):
            st.info("Generating maps...")
            try:
                result = generate_all_maps()
                st.success("✅ Maps generated successfully!")
                st.write(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    st.divider()
    
    # Preview generated maps
    st.subheader("Generated Maps Preview")
    import numpy as np
    try:
        maps = {
            'Solar Irradiance': np.load('data/processed/mapa_irradiacao.npy'),
            'Population Density': np.load('data/processed/mapa_populacao.npy'),
            'Grid Distance': np.load('data/processed/mapa_distanciarede.npy'),
            'Slope': np.load('data/processed/mapa_declividade.npy'),
            'NDVI': np.load('data/processed/mapa_ndvi.npy'),
            'Aptitude': np.load('data/processed/mapa_aptidao_integrada.npy'),
        }
        
        # Interactive map selector
        selected_map = st.selectbox("Select map to view:", list(maps.keys()))
        data = maps[selected_map]
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Min", f"{data.min():.3f}")
        with col2:
            st.metric("Max", f"{data.max():.3f}")
        with col3:
            st.metric("Mean", f"{data.mean():.3f}")
        with col4:
            st.metric("Std Dev", f"{data.std():.3f}")
        
        # Heatmap visualization
        import plotly.express as px
        fig = px.imshow(data, color_continuous_scale='viridis', 
                       title=f"{selected_map} - Heatmap")
        st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.warning("⚠️ No maps generated yet. Click 'Generate Maps' above.")

# ============================================================================
# PAGE: MCDA ANALYSIS
# ============================================================================

elif page == "🎯 MCDA Analysis":
    st.markdown("## 🎯 Multi-Criteria Decision Analysis")
    
    st.markdown("Adjust weights for each criterion and compute integrated aptitude")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        w_solar = st.slider("☀️ Solar Irradiance", 0.0, 1.0, 0.25, step=0.05)
    with col2:
        w_pop = st.slider("👥 Population", 0.0, 1.0, 0.25, step=0.05)
    with col3:
        w_dist = st.slider("🔌 Grid Distance", 0.0, 1.0, 0.20, step=0.05)
    
    col1, col2 = st.columns(2)
    with col1:
        w_slope = st.slider("⛰️ Slope", 0.0, 1.0, 0.15, step=0.05)
    with col2:
        w_ndvi = st.slider("🌱 NDVI", 0.0, 1.0, 0.15, step=0.05)
    
    # Validate weight sum
    weight_sum = w_solar + w_pop + w_dist + w_slope + w_ndvi
    if abs(weight_sum - 1.0) > 0.01:
        st.warning(f"⚠️ Weights sum to {weight_sum:.2f}. Normalize to 1.0 for valid MCDA.")
    else:
        st.success(f"✅ Weights sum to {weight_sum:.2f}")
    
    # Analyze button
    if st.button("📊 Compute MCDA"):
        weights = {
            'irradiacao': w_solar,
            'populacao': w_pop,
            'distancia_rede': w_dist,
            'declividade': w_slope,
            'ndvi': w_ndvi
        }
        try:
            analyzer = MCDAnalyzer()
            result = analyzer.normalize_raster([w_solar, w_pop, w_dist, w_slope, w_ndvi])
            st.success("✅ MCDA computed!")
            
            # Visualize aptitude map
            import plotly.express as px
            fig = px.imshow(result, color_continuous_scale='RdYlGn',
                           title="Integrated Aptitude (MCDA Result)")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ============================================================================
# PAGE: LCOE CALCULATOR
# ============================================================================

elif page == "💰 LCOE Calculator":
    st.markdown("## 💰 Levelized Cost of Energy (LCOE)")
    
    col1, col2 = st.columns(2)
    with col1:
        capacity = st.number_input("Capacity (MW)", value=1.0, min_value=0.1)
    with col2:
        annual_irradiance = st.number_input("Annual Irradiance (kWh/m²/day)", value=2226, min_value=500)
    
    if st.button("Calculate LCOE"):
        try:
            calc = LCOECalculator(location="Huíla")
            results = calc.compare_technologies(capacity, annual_irradiance)
            
            st.success("✅ LCOE Analysis Complete")
            st.dataframe(results)
            
            # Visualize as chart
            import plotly.express as px
            fig = px.bar(results, x="Technology", y="LCOE USD/MWh",
                        color="Technology",
                        title="LCOE Comparison")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ============================================================================
# PAGE: MONITORING
# ============================================================================

elif page == "📊 Monitoring":
    st.markdown("## 📊 Project Monitoring Dashboard")
    
    st.info("Track post-implementation project performance")
    
    # Sample monitoring data
    import pandas as pd
    import plotly.graph_objects as go
    
    sample_data = pd.DataFrame({
        'Project': ['Cacula', 'Humpata', 'Quilengues'],
        'Status': ['Active', 'Active', 'Planning'],
        'Generation (kWh/month)': [15000, 12000, 0],
        'Efficiency (%))': [85, 88, 0],
        'Downtime (hours)': [2, 1, 0]
    })
    
    st.dataframe(sample_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Projects", 2)
    with col2:
        st.metric("Avg Efficiency", "86.5%")
    with col3:
        st.metric("Total Generation", "27,000 kWh/mo")
    
    st.divider()
    st.subheader("Generation Trend")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[15000, 15200, 15100], name="Cacula", mode='lines+markers'))
    fig.add_trace(go.Scatter(y=[12000, 12100, 12050], name="Humpata", mode='lines+markers'))
    fig.update_layout(title="Monthly Generation Trend", xaxis_title="Month", yaxis_title="kWh")
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "⚙️ Settings":
    st.markdown("## ⚙️ Configuration Settings")
    
    st.markdown("### Map Generation")
    col1, col2 = st.columns(2)
    with col1:
        shape_x = st.number_input("Map Width (pixels)", value=300, min_value=100, max_value=1000)
    with col2:
        shape_y = st.number_input("Map Height (pixels)", value=280, min_value=100, max_value=1000)
    
    st.markdown("### MCDA Weights (Defaults)")
    col1, col2, col3 = st.columns(3)
    with col1:
        default_solar = st.number_input("Default Solar Weight", value=0.25, min_value=0.0, max_value=1.0)
    with col2:
        default_pop = st.number_input("Default Population Weight", value=0.25, min_value=0.0, max_value=1.0)
    with col3:
        default_dist = st.number_input("Default Grid Distance Weight", value=0.20, min_value=0.0, max_value=1.0)
    
    st.markdown("### LCOE Defaults")
    col1, col2 = st.columns(2)
    with col1:
        wacc = st.number_input("WACC (%)", value=8.0, min_value=1.0, max_value=20.0)
    with col2:
        lifetime = st.number_input("Project Lifetime (years)", value=20, min_value=5, max_value=50)
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved!")
        
        # Save to config.json
        import json
        config = {
            "map_generation": {
                "output_shape": [shape_y, shape_x]
            },
            "mcda": {
                "weights": {
                    "irradiacao": default_solar,
                    "populacao": default_pop,
                    "distancia_rede": default_dist,
                    "declividade": 0.15,
                    "ndvi": 0.15
                }
            },
            "lcoe": {
                "wacc": wacc / 100.0,
                "project_lifetime_years": lifetime
            }
        }
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**GEESP-Angola v1.0** | Geospatial Energy for Equity & Solar Planning
[GitHub](https://github.com/geesp-angola) | [Documentation](https://docs.geesp.org) | [Contact](mailto:geesp@email.com)
""")
```

### Step 2: Create Requirements & Deployment Files (1 hour)

**File**: `requirements-unified.txt`
```pip-requirements
streamlit>=1.0
numpy
pandas
matplotlib
plotly
scikit-learn
scipy
rasterio
geopandas
shapely
pytest
```

**File**: `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#262730"

[client]
showErrorDetails = true

[logger]
level = "info"
```

### Step 3: Deployment Options (1 hour)

**Option A: Local Development**
```bash
pip install -r requirements-unified.txt
streamlit run geesp-unified-app.py
# Opens at http://localhost:8501
```

**Option B: Streamlit Cloud (Free Hosting)**
```bash
# 1. Push to GitHub
git add geesp-unified-app.py requirements-unified.txt .streamlit/
git commit -m "feat: unified app"
git push origin main

# 2. Deploy via streamlit.io/cloud
# - Connect GitHub repo
# - Select main branch
# - Point to geesp-unified-app.py
# - App lives at: https://geesp-angola.streamlit.app
```

**Option C: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-unified.txt .
RUN pip install -r requirements-unified.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "geesp-unified-app.py"]
```

```bash
docker build -t geesp-angola .
docker run -p 8501:8501 geesp-angola
```

---

## 📊 EFFORT ESTIMATE: Unified Streamlit App

| Phase | Task | Hours | Who |
|-------|------|-------|-----|
| 1 | Create `geesp-unified-app.py` skeleton (6-page structure) | 2 | Dev 1 |
| 2 | Integrate existing dashboard code (Home, MCDA, LCOE) | 1.5 | Dev 1 |
| 3 | Add map generation controls + preview UI | 1.5 | Dev 1 |
| 4 | Add monitoring dashboard + settings page | 1 | Dev 1 |
| 5 | Testing + bug fixes | 1 | Dev 1 |
| 6 | Deploy to Streamlit Cloud + Docker | 0.5 | DevOps |
| 7 | Documentation + user guide | 1 | Technical writer |
| **Total** | **Single unified app ready for users** | **8.5 hours** | |

---

## 🎯 FINAL RECOMMENDATION

**Build the Streamlit Mega-App** because:

1. ✅ **Fastest delivery** (week 1)
2. ✅ **Reuses all existing code** (no rewrite)
3. ✅ **Easy to deploy** (Streamlit Cloud is free)
4. ✅ **Perfect for research** (your use case)
5. ✅ **Future-proof** (can upgrade to FastAPI later if needed)
6. ✅ **No infrastructure costs** (free tier available)

**Timeline**: Complete by end of Feb 9 or Feb 10 (1–2 days)

**Next Steps**:
1. Create `geesp-unified-app.py` with all 6 pages
2. Test locally (`streamlit run geesp-unified-app.py`)
3. Push to GitHub
4. Deploy to Streamlit Cloud (5 minutes)
5. Share URL with stakeholders

---

## 📞 IMPLEMENTATION READY?

Want me to:
- [ ] Build the complete `geesp-unified-app.py` file now?
- [ ] Set up Docker configs for local/cloud deployment?
- [ ] Create deployment documentation?
- [ ] Build the FastAPI + React alternative for future reference?

---

*Generated: 2026-02-09 | Recommendation: Start with Streamlit Mega-App, upgrade to web stack later if needed*
