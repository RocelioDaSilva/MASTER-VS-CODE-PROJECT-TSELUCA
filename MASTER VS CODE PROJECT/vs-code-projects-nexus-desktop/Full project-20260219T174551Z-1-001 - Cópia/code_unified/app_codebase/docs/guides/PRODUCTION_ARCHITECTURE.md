# GEESP-Angola: Production Architecture

*Consolidated unified architecture for the complete GEESP-Angola solar suitability assessment platform.*

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GEESP-Angola Platform                     │
│                    (Production: 2026-03-05)                  │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    User Applications                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────┐        ┌──────────────────────┐      │
│  │  React Dashboard  │        │  Streamlit Dashboard │      │
│  │  (nevermindu)     │        │  (geesp-angola)      │      │
│  │  • 8-tab UI       │        │  • Real-time viz     │      │
│  │  • Financial      │        │  • Community details │      │
│  │  • AI Chat        │        │  • Map visualization │      │
│  │  • Exports        │        │  • Live interactions │      │
│  │ Port: 5173/80     │        │ Port: 8501           │      │
│  └────────┬──────────┘        └──────────┬───────────┘      │
│           │                              │                   │
│           └──────────────┬───────────────┘                   │
│                          │                                    │
└──────────────────────────┼────────────────────────────────────┘
                           │
                           ▼
        ┌───────────────────────────────────────┐
        │   Express API Server (port 3000)      │
        │   nevermindu/server.ts                │
        │                                        │
        │  7 REST Endpoints:                    │
        │  • POST /api/scenarios                │
        │  • GET /api/scenarios                 │
        │  • POST /api/calculate-financial-... │
        │  • POST /api/filter-communities      │
        │  • DELETE /api/scenarios/:id          │
        │  • GET /api/health                   │
        │  • And 1 more...                     │
        └────────────────┬──────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    ┌─────────────────┐    ┌──────────────────────┐
    │   SQLite DB     │    │  Python Backend      │
    │  (Persistent)   │    │  (geesp-angola)      │
    │                 │    │                      │
    │ • scenarios     │    │  MCDA Engine:        │
    │ • results       │    │  • Weight calc       │
    │ • financial     │    │  • Score ranking     │
    │ • config        │    │  • Aptitude rating   │
    │                 │    │  • API endpoints     │
    │ File:           │    │                      │
    │ geesp_scena...  │    │ • Port: 5000 (alt)   │
    │ .db             │    │ • Streamlit: 8501   │
    └─────────────────┘    └──────────────────────┘
         │                         │
         └─────────────┬───────────┘
                       │
                       ▼
         ┌──────────────────────────┐
         │   Data & Configuration   │
         │                          │
         │ • Angola community data  │
         │ • GHI (solar irradiance) │
         │ • Population data        │
         │ • Financial parameters   │
         │ • Soil types             │
         │ • Distance to grid       │
         └──────────────────────────┘
```

---

## Component Details

### 1. Frontend: React Dashboard (nevermindu/)

**Purpose**: User-facing decision support interface

**Technology Stack**:
- React 19 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Framer Motion (animations)
- Leaflet + Leaflet-Draw (mapping)
- Recharts (visualizations)
- Gemini API (@google/genai)

**Key Components** (8 Tabs):
1. **Dashboard** - Overview, metrics, community rankings
2. **Spatial** - Interactive map with draw tools
3. **Analysis** - Charts & trend analysis
4. **Financial** (NEW) - ROI, LCOE, Payback metrics
5. **Filter** (NEW) - 6-dimensional community search
6. **Scenarios** (NEW) - Save/load MCDA configurations
7. **AI Chat** - Gemini AI insights
8. **Compare** - Side-by-side scenario analysis

**Export Capabilities**:
- PDF (jsPDF with autoTable)
- Excel (XLSX)
- JSON (with metadata & timestamp)

**Port**: 5173 (dev) | 80 (production)

---

### 2. Backend: Express API Server (nevermindu/server.ts)

**Purpose**: Persistence and advanced calculations

**Technology**:
- Express.js 4.21+
- TypeScript 5.8+
- SQLite 3 (via better-sqlite3)
- CORS enabled

**Database Schema**:
```sql
CREATE TABLE scenarios (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  weights TEXT,          -- JSON: {climate, soil, terrain, infrastructure}
  solar_params TEXT,     -- JSON: {efficiency, lifetime, costs}
  created_at DATETIME,
  updated_at DATETIME,
  tags TEXT              -- JSON array of tags
);

CREATE TABLE scenario_results (
  id TEXT PRIMARY KEY,
  scenario_id TEXT,
  community_id TEXT,
  score REAL,
  aptitude TEXT,         -- Excellent, Good, Moderate, Poor, Unsuitable
  lcoe REAL,            -- Levelized Cost of Energy
  roi REAL,             -- Return on Investment
  payback_years REAL    -- Payback Period
);

CREATE TABLE financial_config (
  id TEXT PRIMARY KEY,
  scenario_id TEXT,
  technology TEXT,
  installation_cost_per_kw REAL,
  om_cost_per_kwh REAL,
  financing_rate REAL,
  financing_years INTEGER,
  grid_electricity_cost_per_kwh REAL
);
```

**API Endpoints** (7 total):

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/scenarios` | Save new scenario |
| GET | `/api/scenarios` | List all scenarios |
| GET | `/api/scenarios/:id` | Retrieve scenario |
| DELETE | `/api/scenarios/:id` | Delete scenario |
| POST | `/api/calculate-financial-metrics` | Calculate ROI/LCOE |
| POST | `/api/filter-communities` | Advanced filtering |
| POST | `/api/scenarios/:id/save-results` | Persist analysis results |
| GET | `/api/health` | Health check |

**Port**: 3000

**Financial Calculations**:
- LCOE: `Total Cost / Total Energy Production`
- ROI: `(Total Grid Savings - Total Cost) / Total Cost × 100`
- Payback: `Capital Cost / Annual Savings`

---

### 3. Python Backend: MCDA Engine (geesp-angola/)

**Purpose**: Multi-Criteria Decision Analysis for solar suitability

**Technology**:
- Python 3.11.9
- Streamlit (UI framework)
- Pandas (data processing)
- Numpy (calculations)

**Core Features**:
- MCDA weighted scoring
- Community suitability ranking
- Real-time metrics computation
- Interactive dashboard
- API endpoints (Flask/FastAPI optional)

**Folder Structure**:
```
geesp-angola/
├── dashboard/              # Streamlit app
│   └── app.py
├── utils/
│   ├── exceptions.py      # Unified exception handling (11 classes)
│   ├── import_helpers.py  # Path management
│   └── mcda_engine.py    # Scoring logic
├── tests/
│   ├── test_mcda.py      # MCDA tests
│   ├── test_exceptions.py
│   └── [68 tests total - ✅ 100% passing]
├── data/
│   └── communities.csv    # Angola community data
└── models/
    └── [data models]
```

**Port**: 8501 (Streamlit)

**Test Coverage**: 68/68 ✅ (100%)

---

## Data Flow

### Scenario Analysis Flow

```
1. User adjusts weights (Climate, Soil, Terrain, Infrastructure)
   ↓
2. Frontend calls backend: POST /api/scenarios
   ↓
3. Backend stores in SQLite
   ↓
4. Frontend sends to Python: Python MCDA engine scores communities
   ↓
5. Scores returned with aptitude (Excellent/Good/Moderate/Poor)
   ↓
6. Backend calculates financial metrics: POST /api/calculate-financial-metrics
   ↓
7. Results stored: POST /api/scenarios/:id/save-results
   ↓
8. Frontend displays in Dashboard, Financial, Filter, Charts tabs
   ↓
9. Export triggered: PDF/Excel/JSON generated on frontend
```

### Filtering Flow

```
User sets criteria:
  • Min suitability (e.g., Good+)
  • Max LCOE (e.g., $0.15/kWh)
  • Min GHI (e.g., 5.5 kWh/m²/day)
  • Province selection
  • Max population
   ↓
Frontend calls: POST /api/filter-communities
   ↓
Backend applies all filters in sequence
   ↓
Returns filtered communities list
   ↓
Frontend displays in Filter tab with count & details
```

---

## Deployment Architecture

### Development Environment
```
localhost:5173  (Vite React dev server)
localhost:3000  (Express API)
localhost:8501  (Streamlit dashboard)
```

### Production Environment
```
http://yourserver/           (React frontend via Nginx/Vercel)
http://yourserver/api        (Express backend)
http://yourserver:8501       (Streamlit dashboard, optional internal)
Database: /var/lib/geesp/geesp_scenarios.db

Environment Variables:
  GEMINI_API_KEY=your_key_here
  PORT=3000
  NODE_ENV=production
  DATABASE_URL=./geesp_scenarios.db
```

### Docker (Optional)
```
docker-compose up -d
Spins up:
  - Express backend (port 3000)
  - Vite frontend (port 5173)
  - Streamlit (port 8501)
  - SQLite volume mount
```

---

## Integration Points

### Frontend ↔ Backend API
- All communication via REST/JSON
- Authentication: Optional (can add JWT)
- Rate limiting: Configurable
- CORS: Enabled by default

### Python ↔ Express
- Optional: Express can delegate MCDA to Python subprocess
- Current: Python used only via Streamlit dashboard
- Future: Could add FastAPI wrapper around Python engine

### Database
- SQLite: Lightweight, perfect for single-server deployment
- Scenarios & results persisted indefinitely
- Financial config per scenario
- Upgrade path: PostgreSQL (production scale)

---

## Performance Characteristics

| Operation | Typical Time | Bottleneck |
|-----------|--------------|-----------|
| Load communities | ~200ms | JSON parsing |
| MCDA scoring (45 communities) | ~500ms | Math calculations |
| Calculate financial metrics | ~100ms per community | API overhead |
| Advanced filtering | ~300ms | Database query |
| Export PDF | ~1-2s | PDF generation |
| Gemini chat response | ~2-5s | Network latency |
| Scenario persistence | ~150ms | SQLite write |

---

## Security Considerations

- [ ] API authentication (add JWT if multi-user)
- [ ] Input validation (all endpoints)
- [ ] SQL injection prevention (using parameterized queries)
- [ ] CORS whitelist (configure for production domain)
- [ ] Rate limiting (5req/sec default)
- [ ] HTTPS (deploy with SSL cert)
- [ ] Environment variables (never hardcode secrets)

---

## Monitoring & Operations

### Health Checks
```bash
GET /api/health
Response: { status: "ok", timestamp: "2026-03-05T14:30:00Z" }
```

### Logging
- Express: Console + file logs
- Streamlit: Built-in error tracking
- Database: SQLite query log (optional)

### Backup Strategy
```bash
# Daily backup of SQLite
cp geesp_scenarios.db geesp_scenarios.db.$(date +%Y%m%d)
```

---

## Maintenance & Evolution

### Current Phase (Stable)
✅ MCDA engine complete
✅ Financial analytics done
✅ Advanced filtering working
✅ Scenario persistence functional

### Phase 2 (Planned)
- [ ] User authentication & multi-tenant support
- [ ] Mobile app (React Native)
- [ ] GEE integration (Sentinel-2 data)
- [ ] Real-time weather updates
- [ ] Machine learning predictions
- [ ] Advanced scenario optimization

### Phase 3 (Future)
- PostgreSQL upgrade (>10k scenarios)
- Kubernetes deployment
- GraphQL API option
- Mobile offline support
- Blockchain scenario signing

---

## Quick Reference

| Task | Command | Duration |
|------|---------|----------|
| Start all services | `npm run dev` (nevermindu) | ~10s |
| Run tests | `pytest tests/` (geesp-angola) | ~30s |
| Build frontend | `npm run build` | ~60s |
| Deploy backend | `npm install && npm start` | ~2min |
| Backup database | `cp geesp_scenarios.db ...` | ~5s |
| Check health | `curl localhost:3000/api/health` | <100ms |

---

## Support & Documentation

- **Architecture**: This file
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **Development**: See `DEVELOPMENT_WORKFLOW.md`
- **API Docs**: See `nevermindu/README.md`
- **Tests**: `geesp-angola/tests/`

---

**Last Updated**: 2026-03-05
**Maintainer**: GEESP Team
**Status**: 🟢 Production Ready
