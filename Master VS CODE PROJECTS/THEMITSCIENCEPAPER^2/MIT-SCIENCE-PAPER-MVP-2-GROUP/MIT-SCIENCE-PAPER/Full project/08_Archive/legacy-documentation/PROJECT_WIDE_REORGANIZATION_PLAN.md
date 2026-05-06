# Project-Wide Reorganization Plan

## Current State Analysis

### Active Components
```
✅ PRODUCTION
├── geesp-angola/ (Python Backend)
│   ├── Complete MCDA implementation
│   ├── Dashboard (Streamlit)
│   ├── Utils & consolidated exceptions
│   ├── Tests (68/68 passing)
│   └── API & data processing
│
└── nevermindu/ (Full-Stack Frontend)
    ├── React 19 + TypeScript
    ├── Express backend (server.ts)
    ├── SQLite persistence
    ├── 8-tab UI (Dashboard, Spatial, Analysis, Financial, Filter, Scenarios, Chat, Compare)
    ├── Gemini AI integration
    ├── PDF/Excel/JSON exports
    └── Advanced analytics (ROI, LCOE, Payback)
```

### Legacy/Deprecated Components
```
❌ SUPERSEDED
├── code from google creator/ (Manual React - SUPERSEDED by nevermindu)
├── geesp-angelo/ (Minimal fix - 1 file only)
└── Multiple .md files (Consolidation reports from previous phases)
```

## Recommended Consolidation

### Phase 1: Archive Legacy Code
- **geesp-angelo/** → Move to `08_Archive/legacy-fixes/`
- **code from google creator/** → Move to `08_Archive/manual-implementation/`
- Rationale: These were intermediate steps; nevermindu supersedes both

### Phase 2: Consolidate Python Tests
- Ensure geesp-angola/ maintains 100% test coverage
- Copy any missing tests from legacy folders

### Phase 3: Documentation Consolidation
- Create single `PRODUCTION_ARCHITECTURE.md` (replaces 20+ consolidation reports)
- Create `DEPLOYMENT_GUIDE.md` (unified process)
- Create `DEVELOPMENT_WORKFLOW.md` (for future work)

### Phase 4: Final Structure
```
02_Code/
├── PRODUCTION_ARCHITECTURE.md    ← NEW: Single source of truth
├── DEPLOYMENT_GUIDE.md           ← NEW: How to deploy
├── DEVELOPMENT_WORKFLOW.md       ← NEW: How to develop
├── geesp-angola/                 ← PRIMARY: Python backend
│   ├── dashboard/
│   ├── utils/
│   ├── tests/
│   └── [app files]
│
├── nevermindu/                   ← PRIMARY: Full-stack frontend
│   ├── server.ts
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── [app files]
│   └── [config files]
│
└── 08_Archive/                   ← LEGACY: Superseded code
    ├── legacy-fixes/
    ├── manual-implementation/
    └── README.md
```

## Integration Points

1. **Frontend → Backend**: nevermindu/server.ts calls geesp-angola APIs
2. **Database**: SQLite in nevermindu/ (Streamlit uses in-memory MCDA)
3. **Deployment**: Both run on same host, different ports
   - Backend: Port 3000 (Express)
   - Frontend: Port 5173 (Vite dev) or 80 (production)
   - Dashboard: localhost:8501 (Streamlit)

## Actions Required

- [ ] Move geesp-angelo/ to archive
- [ ] Move code from google creator/ to archive
- [ ] Create PRODUCTION_ARCHITECTURE.md
- [ ] Create DEPLOYMENT_GUIDE.md
- [ ] Update 02_Code/README.md
- [ ] Verify all 68 tests still pass
- [ ] Document API contracts between frontend/backend
