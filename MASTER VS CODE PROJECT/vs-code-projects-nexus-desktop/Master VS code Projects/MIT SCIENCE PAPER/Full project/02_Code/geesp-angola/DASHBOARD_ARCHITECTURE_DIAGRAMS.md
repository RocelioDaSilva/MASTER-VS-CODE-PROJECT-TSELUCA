# GEESP-Angola Dashboard Architecture Diagrams

## 1. Current Architecture (5-Page Monolithic)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GEESP-Angola Dashboard                       │
│                   (Single Streamlit app.py)                     │
│                        752 Lines Total                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│              │              │              │              │              │
│ 🏠 Home      │ 📊 Data      │ 🎯 MCDA      │ 📈 Results   │ 💰 LCOE      │
│ (150 lines)  │ Exploration  │ Analysis     │ (80 lines)   │ Calculator   │
│              │ (80 lines)   │ (250 lines)  │              │ (120 lines)  │
│              │              │              │              │              │
│ - Title      │ - Upload     │ - Sliders    │ - Zone table │ - Inputs     │
│ - KPI cards  │   GeoTIFF    │ - Normalize  │ - Tech recs  │ - Results    │
│ - Map (fold) │ - Stats tbl  │ - AHP matrix │ - Sens plot  │ - Comparison │
│              │ - Box plots  │ - Overlay    │ - Export     │ - Export     │
│              │              │ - Sens run   │   (broken)   │   (broken)   │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                              ↓↓↓
                        MONOLITHIC ISSUES
                    - 750+ lines in single file
                    - Duplicated plotting code
                    - No component reuse
                    - Hard to test pages independently
                    - Mixed concerns (UI + logic)
                    - Session state scattered
```

---

## 2. Current Data Flow

```
USER INPUTS                 COMPUTATION                 OUTPUTS
   │                              │                         │
   ├─ Weight sliders          ├─ Load .npy                ├─ PNG overlay
   ├─ Zone selector           │  from disk                ├─ Statistics
   ├─ Layer toggles           │                           ├─ Text summary
   ├─ File upload             ├─ Normalize to             ├─ Download
   ├─ LCOE parameters         │  [0, 1]                   │  buttons
   │                          │                           │
   └─ Click buttons           ├─ Weighted sum:            └─ (Broken
      (compute)               │  Σ(w_i * r_i)               export)
                              │
                              ├─ Generate viz
                              │
                              ├─ Compute stats
                              │
                              └─ Save .npy/.tif
```

---

## 3. Proposed Architecture (6-Page Modular)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GEESP-Angola Dashboard                       │
│                      (Modular Streamlit)                        │
│                     6 Pages + Components                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PAGES/                    (6 separate files)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ home.py (75L)         🏠 Dashboard Overview                ││
│  │ ├─ MetricsCard        (KPI display)                        ││
│  │ ├─ MapViewer          (Folium map + zones)                 ││
│  │ └─ Navigation hints                                         ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ data_layers.py (80L)  📊 Raster Upload & Analysis          ││
│  │ ├─ FileUploader       (GeoTIFF input)                       ││
│  │ ├─ MetadataDisplay    (CRS, resolution, bounds)             ││
│  │ ├─ StatisticsTable    (min/max/mean/std)                    ││
│  │ └─ DistributionPlot   (Plotly box plot)                     ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ mcda_config.py (120L) 🎯 MCDA Weight Configuration         ││
│  │ ├─ WeightSliders      (5 criteria, auto-normalize)          ││
│  │ ├─ AHPMatrixEditor    (Saaty scale, interactive)            ││
│  │ ├─ SensitivityControl (range ± %, step)                     ││
│  │ ├─ ExecuteMCDA        (compute overlay)                      ││
│  │ └─ SensitivityPlots   (perturbation analysis)               ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ results_viewer.py (90L) 📈 MCDA Results                    ││
│  │ ├─ ZoneTable          (Cacula/Humpata/Quilengues)          ││
│  │ ├─ AptitudeMap        (Folium overlay)                      ││
│  │ ├─ TechRecommender    (PV/Tracker/Hybrid)                   ││
│  │ ├─ SensitivitySummary (robustness assessment)              ││
│  │ └─ ExportButtons      (CSV, GeoTIFF, PDF)                   ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ lcoe_analysis.py (100L) 💰 Financial Analysis              ││
│  │ ├─ ParameterInputs    (capacity, irradiance, rate)          ││
│  │ ├─ TechnologySelector (3 options)                           ││
│  │ ├─ LCOEComparison     (bar chart)                           ││
│  │ ├─ DetailedTable      (CAPEX, O&M, generation)              ││
│  │ ├─ SensitivityAnalysis (tornado chart)                      ││
│  │ └─ ExportButtons      (CSV, Excel, JSON)                    ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ monitoring.py (110L)  🔍 Field Monitoring [NEW]            ││
│  │ ├─ ProjectSelector    (phase 1 site selection)              ││
│  │ ├─ GPSTracker         (real-time field location)            ││
│  │ ├─ BaselineChecklist  (GPS, photos, interviews)             ││
│  │ ├─ LiveMetrics        (collected data)                      ││
│  │ ├─ AlertNotifications (status updates)                      ││
│  │ └─ SiteValidation     (field adjustment)                    ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  COMPONENTS/              (Reusable Widget Library)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ├─ metrics_card.py        → MetricsCard([data])                │
│  ├─ map_viewer.py          → MapViewer(path).render()           │
│  ├─ weight_sliders.py      → WeightSliders(criteria).get()      │
│  ├─ sensitivity_analyzer.py → SensitivityAnalyzer(w, r).run()   │
│  ├─ zone_table.py          → ZoneTable(zones).render()          │
│  ├─ technology_recommender.py → TechRecommender().suggest()     │
│  └─ gps_tracker.py         → GPSTracker(proj).map()             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  UTILS/                   (Shared Utilities)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ├─ session_state.py       → SessionState.load/save()           │
│  ├─ page_router.py         → router.render_page()               │
│  ├─ error_handlers.py      → ErrorHandler.show()                │
│  ├─ validators_ui.py       → validate_raster(file)              │
│  └─ cache_manager.py       → CacheManager.get/set()             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Dependency Graph

```
                        app.py (main)
                          │
          ┌───────────────┼───────────────┐
          │               │               │
      page_router   session_state    error_handlers
          │
    ┌─────┼─────┬─────┬────────┬───────────┐
    │     │     │     │        │           │
  home  data  mcda results  lcoe      monitoring
    │     │     │     │        │           │
    └─────┴─────┴─────┴────────┴───────────┘
          │
          └──────────┬──────────────────────┐
                     │                      │
               components/            (shared libs)
                     │                      │
        ┌────────────┼────────────┐         │
        │            │            │         │
    metrics_card  map_viewer  weight_     cache_
                              sliders    manager
        │            │            │         │
        └────────────┴────────────┴─────────┘
                     │
           data/ → analysis/ → results/
           config/                export/
```

---

## 5. Data Flow: Current vs. Proposed

### **CURRENT - Session State Based**

```
┌─ User Input ──────────────┐
│                           │
│  Weight sliders      ↓    │
│  File uploads        ↓    │
│  Zone selector       ↓    │
│  Parameters          ↓    │
│                           │
│  st.session_state   ┌─────────────┐
│  (ephemeral)        │ RAM Memory  │ ← Lost on page refresh!
└─────────────────┬──┐└────────────┐┘
                  │  │             │
            ┌─────↓──↓─────┐       │
            │  Computation │       │
            │ (numpy ops)  │←──────┘
            └─────┬────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    ┌───↓────┐         ┌───↓────┐
    │Display │         │ Save to │
    │on page │         │  Disk   │
    └────────┘         │(.npy)   │
                       └─────────┘
```

### **PROPOSED - Database-Backed**

```
┌──── User Input ────────────────┐
│                                │
└────────────┬───────────────────┘
             │
        ┌────↓──────┐
        │ Validation│  ← validators_ui.py
        └────┬──────┘
             │
        ┌────↓────────────────┐
        │ config.json          │ ← version control
        │ (Parameter Store)    │
        └────┬────────────────┘
             │
        ┌────↓──────────────────────┐
        │ Redis Cache               │ ← (7 day TTL)
        │ (computed overlays)       │
        └────┬─────────────────────┐│
             │                     │ └─→ [CACHE HIT] ← Fast!
        ┌────↓──────────────────────┐
        │ PostgreSQL Database        │ ← Persistence
        ├────────────────────────────┤
        │ ├─ analysis_results       │
        │ ├─ project_sites          │
        │ ├─ field_baseline         │
        │ └─ audit_log              │
        └────┬──────────────────────┘
             │
        ┌────↓──────────────────┐
        │ FastAPI (Optional)     │
        │ REST Endpoints         │
        └────┬──────────────────┘
             │
        ┌────┴────┬─────────┬─────────┐
        │          │         │         │
    ┌───↓───┐  ┌──↓──┐  ┌──↓──┐  ┌──↓──┐
    │Web    │  │Mobile│ │PDF  │ │ API │
    │Streamlit│ │PWA  │ │Report│ │Call │
    └───────┘  └─────┘  └─────┘  └────┘
```

---

## 6. Component Reuse Matrix

```
                COMPONENT         | Home | Data | MCDA | Results | LCOE | Monitor
────────────────────────────────────────────────────────────────────────────────
 metrics_card.py                  │  ✓   │      │      │    ✓    │      │
 map_viewer.py                    │  ✓   │  ✓   │  ✓   │    ✓    │      │   ✓
 weight_sliders.py                │      │      │  ✓   │         │      │
 sensitivity_analyzer.py          │      │      │  ✓   │    ✓    │  ✓   │
 zone_table.py                    │      │      │      │    ✓    │      │   ✓
 technology_recommender.py        │      │      │      │    ✓    │  ✓   │
 gps_tracker.py                   │      │      │      │         │      │   ✓
────────────────────────────────────────────────────────────────────────────────
 REUSE COUNT                       │  3   │  2   │  3   │    5    │  2   │   2
 REDUNDANCY REDUCED BY             │ 30%  │      │      │    30%  │      │
```

---

## 7. Performance Impact: Before → After

```
CURRENT (Monolithic)          PROPOSED (Modular)
├─ App Load: ~5 sec          ├─ App Load: ~3 sec (-40%)
├─ MCDA Compute: ~8 sec      ├─ MCDA Compute: [~3-8 sec]
│  (no cache)                │  ├─ 1st run: ~8 sec
├─ Map Render: ~2 sec        │  ├─ Cached: <1 sec! ✓
├─ Export: fails             │  └─ [savings from Redis]
└─ Total: ~20 sec            ├─ Map Render: ~1 sec (-50%)
                             ├─ Export: functional ✓
                             └─ Total: ~10 sec (-50%)
```

---

## 8. Integration Timeline

```
CURRENT                    PHASE 2 (2-3 wks)           PHASE 3 (2-3 wks)       PRODUCTION
┌──────────────┐          ┌──────────────────┐         ┌───────────────┐        ┌────────────┐
│ 5-page app   │  ────→   │ 6-page modules   │  ────→  │ Optimized     │ ────→  │ Full      │
│ 752 lines    │          │ + components     │         │ + cached      │        │ stack     │
│ Monolithic   │          │ 6 × <100 lines   │         │ + monitored   │        │ deployed  │
│ 0% coverage  │          │ 70% test coverage│         │ <3 sec load   │        │ Phase 1   │
└──────────────┘          └──────────────────┘         └───────────────┘        │ ready     │
   Feb 12-13              Feb 13 → Mar 5               Mar 6 → Apr 2            │ Apr 2     │
                                                                                 └────────────┘
```

---

## 9. Phase 1 Field Integration

```
DASHBOARD (Streamlit)           FIELD TEAMS (Phase 1)
┌──────────────────────┐    ┌────────────────────────────┐
│                      │    │                            │
│ 6-page dashboard     │◄──►│ Mobile-friendly pages      │
│                      │    │ ├─ GPS check-in           │
│ • Monitoring page    │    │ ├─ Photo upload (offline) │
│ • Real-time tracking │    │ ├─ Interview form         │
│ • Alert system       │    │ ├─ Measurements          │
│ • Site validation    │    │ └─ Baseline submit       │
│                      │    │                            │
└──────────────────────┘    └────────────────────────────┘
       │                               │
       ├─ Sync Field Data             │
       ├─ Update Site Rankings        │
       ├─ Generate Live Reports       │
       └─ Alert on Conflicts          │
       
FEEDBACK LOOP:
Phase 1 field insights → Dashboard model update → Improved Phase 2-3 prioritization
```

---

## 10. Database Schema (Proposed)

```sql
┌─────────────────────────────────────────────────────────────┐
│                PostgreSQL Schema                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  analysis_results                                           │
│  ├─ id (UUID)                                              │
│  ├─ timestamp (datetime)                                   │
│  ├─ weights (JSON) → {irradiacao: 0.25, ...}             │
│  ├─ aptitude_map_path (string)                             │
│  ├─ zone_rankings (JSON)                                   │
│  └─ sensitivity_params (JSON)                              │
│                                                             │
│  project_sites  [NEW]                                       │
│  ├─ id (UUID)                                              │
│  ├─ zone_name (A/B/C)                                      │
│  ├─ gps_lat, gps_lon (float)                               │
│  ├─ status (planning/baseline/validated/active)            │
│  ├─ predicted_aptitude (0-1)                               │
│  ├─ field_validated (bool)                                 │
│  └─ baseline_data (JSONB)                                  │
│                                                             │
│  field_visits  [NEW]                                        │
│  ├─ id (UUID)                                              │
│  ├─ project_id (FK)                                        │
│  ├─ team_id (string)                                       │
│  ├─ timestamp (datetime)                                   │
│  ├─ gps_track (JSON array of points)                       │
│  ├─ photos (array of URLs)                                 │
│  ├─ checklist_status (JSON)                                │
│  └─ notes (text)                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

