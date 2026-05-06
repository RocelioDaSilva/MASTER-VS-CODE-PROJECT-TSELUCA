# 📖 ARCHITECTURE GUIDE: Backend/Frontend Separation
## Unified GEESP-Angola Project Structure
### Phase 5 Complete: March 7, 2026

---

## 🎯 Design Overview

The GEESP-Angola project now follows a **modern full-stack architecture** with clear separation between:
- **Backend** (Python) - Analysis engines, APIs, data processing
- **Frontend** (React/TypeScript) - User interface, services, middleware

### Why This Architecture?

| Benefit | Impact |
|---------|--------|
| **Independent Development** | Teams can work on backend/frontend simultaneously |
| **Parallel Deployment** | Deploy frontend to CDN, backend to servers independently |
| **Technology Flexibility** | Use best tools for each stack (Python for analysis, React for UI) |
| **Scalability** | Frontend can scale horizontally, backend can scale vertically |
| **Maintainability** | Clear boundaries, single responsibility per module |
| **Team Organization** | Frontend team, backend team, DevOps team all clear |

---

## 🔧 BACKEND ARCHITECTURE

### Overview
```
Backend (Python 20,407 lines)
├── FastAPI REST API       [8 endpoints + async job queue]
├── Analysis Engines       [MCDA, LCOE, GEE integration]
├── Database Models        [SQLAlchemy ORM]
├── Utilities              [Centralized core_utils]
├── Streamlit Dashboard    [Monitoring & visualization]
└── Test Suite             [19,520 lines organized]
```

### API Layer (`backend/api/`)

**Technology**: FastAPI (async-capable)

**Endpoints**:
```python
# Health & Status
GET  /health                    # Service health check

# Layer Management
GET  /layers                    # Available spatial layers
GET  /layers/{layer_id}        # Layer details

# MCDA Analysis
POST /mcda                      # Compute MCDA ranking (sync)
GET  /mcda/inputs              # MCDA input schema

# Async Job Queue (for long-running analyses)
POST /mcda/jobs                 # Submit MCDA job to queue
GET  /mcda/jobs/{job_id}        # Query job status/results
GET  /mcda/jobs                 # List all jobs
GET  /mcda/stats                # Queue statistics

# Batch Operations (through job queue)
POST /batch/process             # Batch processing
```

**Key Classes**:
- `MCDAJobData` - Job representation
- `MCDABatchProcessor` - Async processor
- `BatchJobConstants` - Status codes & constants

### Analysis Scripts (`backend/scripts/`)

| Module | Purpose | Key Functions |
|--------|---------|----------------|
| `mcda_analysis.py` | MCDA ranking | `MCDAnalyzer.compute()` |
| `lcoe_calculator.py` | Financial analysis | `LCOECalculator.calculate()` |
| `gee_integration.py` | Google Earth Engine | `GEEConnector.get_layer()` |
| `generate_maps_simple.py` | Map generation | `generate_spatial_layers()` |
| `map_utilities.py` | Map processing | `postprocess_map()` |

### Utils Layer (`backend/utils/`)

**Centralized Utilities** (Core functions in one place):
- `core_utils.py` - Shared functions (format_number, data validation, etc.)
- `validation.py` - Input validation schemas
- `logging_setup.py` - Unified logging configuration
- `config.py` - Configuration management
- `error_handlers.py` - Exception handling

### Database Models (`backend/models/`)

```python
# models/scenario.py
class Scenario(Base):
    id: int
    name: str
    location: str
    created_at: datetime

# models/results.py
class AnalysisResults(Base):
    id: int
    scenario_id: int
    mcda_score: float
    lcoe_value: float
    metadata: dict
```

### Test Organization (`backend/tests/`)

```
tests/
├── unit/                    # Isolated component tests
│   ├── test_mcda.py        # MCDA algorithm
│   └── conftest.py         # Unit fixtures
│
├── integration/            # Multi-component tests
│   ├── test_database_models.py
│   ├── test_performance_profiling.py
│   └── conftest.py         # Integration fixtures
│
├── e2e/                    # End-to-end workflows
│   └── conftest.py         # E2E fixtures
│
├── performance/            # Performance benchmarks
│   ├── test_performance.py
│   └── conftest.py         # Performance fixtures
│
└── conftest.py             # Shared fixtures
```

**Run Tests**:
```bash
pytest                          # All tests
pytest -m unit                  # Unit tests only
pytest -m integration           # Integration tests
pytest backend/tests/unit/      # Specific folder
```

### Dashboard Application (`backend/dashboard/`)

```
dashboard/
├── app.py                  # Main Streamlit app
├── pages/
│   ├── home.py            # Home page
│   ├── analysis.py        # Analysis interface
│   ├── results.py         # Results visualization
│   └── ...
└── utils/                 # Dashboard utilities
```

**Run Dashboard**:
```bash
streamlit run backend/dashboard/app.py
```

---

## 🎨 FRONTEND ARCHITECTURE

### Overview
```
Frontend (React/TypeScript 8,500+ lines)
├── React Components       [66 components]
├── API Services           [Gemini AI, Auth, API calls]
├── TypeScript Types       [Type safety]
├── Authentication         [Middleware]
└── Vite Build System      [Fast development]
```

### Component Structure (`frontend/src/components/`)

| Component | Purpose |
|-----------|---------|
| `AdvancedFilter.tsx` | Data filtering UI |
| `Charts/` | Data visualization components |
| `Chat/` | Chatbot interface (Gemini AI) |
| `Map/` | Interactive map components |
| `Sidebar.tsx` | Navigation sidebar |
| ... | Other UI components |

### Services Layer (`frontend/src/services/`)

| Service | Purpose | Key Functions |
|---------|---------|----------------|
| `geminiService.ts` | Gemini AI integration | `sendMessage()`, `getResponse()` |
| `authService.ts` | Authentication | `login()`, `logout()`, `register()` |
| `apiService.ts` | Backend API calls | `fetchData()`, `submitAnalysis()` |

### Middleware (`frontend/src/middleware/`)

```typescript
// authMiddleware.ts
export const authMiddleware = (req, res, next) => {
  const token = getToken();
  if (!token) redirect('/auth');
  next();
}
```

### Build Configuration

**Vite Config** (`frontend/vite.config.ts`):
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

**TypeScript Config** (`frontend/tsconfig.json`):
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "jsx": "react-jsx",
    "strict": true
  }
}
```

**Run Frontend**:
```bash
cd frontend
npm install
npm run dev        # Development server
npm run build      # Production build
```

---

## 🔗 INTEGRATION POINTS

### Backend to Frontend Communication

```
Frontend                          Backend
├── HTTP Requests                ├── FastAPI
│   ├── GET /health             │   ├── Health check
│   ├── POST /mcda              │   ├── Compute MCDA
│   ├── GET /layers             │   ├── Get layers
│   └── POST /mcda/jobs         │   └── Queue job
│
└── WebSocket (for real-time)   └── Job status updates
    ├── /ws/jobs/{id}            ├── Status streaming
    └── /ws/chat                 └── Chat streaming
```

### API Communication Pattern

**Frontend makes request**:
```typescript
const response = await fetch('/api/mcda', {
  method: 'POST',
  body: JSON.stringify(params)
});
```

**Backend processes**:
```python
@app.post('/mcda')
async def compute_mcda(data: MCDARequest):
    results = MCDAnalyzer.compute(data)
    return {'status': 'success', 'results': results}
```

### Async Job Pattern (for long-running tasks)

**Frontend**:
```typescript
// Submit job
const response = await fetch('/api/mcda/jobs', {
  method: 'POST',
  body: JSON.stringify(largeDataset)
});
const jobId = response.job_id;

// Poll status
const status = await fetch(`/api/mcda/jobs/${jobId}`);
```

**Backend**:
```python
@app.post('/mcda/jobs')
async def submit_mcda_job(data: MCDAJobData):
    job_id = queue.add(data)
    background_tasks.add_task(process_mcda_job, job_id)
    return {'job_id': job_id}

@app.get('/mcda/jobs/{job_id}')
async def get_job_status(job_id: str):
    return queue.get_status(job_id)
```

---

## 📦 DEPLOYMENT ARCHITECTURE

### Docker Setup

**Backend Image** (`Dockerfile`):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0"]
```

**Frontend Image** (`Dockerfile.frontend`):
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package*.json .
RUN npm install
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
  
  frontend:
    build:
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

**Start Development Stack**:
```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Kubernetes Deployment

**Structure** (`k8s/`):
```
k8s/
├── backend-deployment.yml
├── backend-service.yml
├── frontend-deployment.yml
├── frontend-service.yml
├── database-statefulset.yml
├── ingress.yml
└── configmap.yml
```

**Deploy to Kubernetes**:
```bash
kubectl apply -f k8s/
```

---

## 🔄 DEVELOPMENT WORKFLOW

### Local Development

**Terminal 1 - Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate    # ..\venv\Scripts\activate on Windows
pip install -r ../requirements.txt
python -m uvicorn api.api:app --reload
# Backend running at http://localhost:8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm install
npm run dev
# Frontend running at http://localhost:5173
```

**Terminal 3 - Dashboard** (optional):
```bash
cd backend
streamlit run dashboard/app.py
# Dashboard running at http://localhost:8501
```

### Import Patterns

**Within Backend**:
```python
# Using relative imports within backend/
from scripts.mcda_analysis import MCDAnalyzer
from utils.validation import validate_input
from models.scenario import Scenario

# Or using absolute imports from root
from backend.scripts.mcda_analysis import MCDAnalyzer
from backend.utils.validation import validate_input
```

**Frontend**:
```typescript
// Using ES6 imports
import { AdvancedFilter } from '@/components/AdvancedFilter';
import { apiService } from '@/services/apiService';
import type { AnalysisResult } from '@/types';
```

---

## 📊 TYPE SAFETY

### Backend (Python Type Hints)

```python
from pydantic import BaseModel
from datetime import datetime

class MCDARequest(BaseModel):
    criteria: Dict[str, float]
    weights: Dict[str, float]
    alternatives: List[str]

class MCDAResponse(BaseModel):
    rankings: Dict[str, float]
    timestamp: datetime
    status: str
```

### Frontend (TypeScript)

```typescript
// types/index.ts
export interface AnalysisRequest {
  criteria: Record<string, number>;
  weights: Record<string, number>;
  alternatives: string[];
}

export interface AnalysisResponse {
  rankings: Record<string, number>;
  timestamp: Date;
  status: 'success' | 'fail';
}
```

---

## 🛡️ Security Architecture

### Authentication Flow

```
User Login
    ↓
Frontend: POST /auth/login with credentials
    ↓
Backend: Verify credentials, create JWT token
    ↓
Frontend: Store token locally
    ↓
Subsequent Requests: Include token in header
    Authorization: Bearer <token>
    ↓
Backend: Verify token, process request
```

### CORS Configuration

```python
# backend/api/api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables

Create `.env` files:

```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@localhost/dbname
API_KEY=your_api_key
GEE_CREDENTIALS=/path/to/gee_credentials.json

# frontend/.env
VITE_API_URL=http://localhost:8000
VITE_GEMINI_API_KEY=your_gemini_key
```

---

## 📈 Performance Optimization

### Backend

- **Database Indexing**: Key queries indexed
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Long tasks queued asynchronously
- **Lazy Loading**: Load data on-demand

### Frontend

- **Code Splitting**: React lazy loading
- **Bundle Optimization**: Tree-shaking, minification
- **Image Optimization**: WebP, responsive images
- **Service Workers**: Offline capability

---

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Run tests
        run: pytest

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Build
        run: cd frontend && npm run build
```

---

## 📞 Support & Resources

- **Backend API Docs**: http://localhost:8000/docs
- **Frontend Dev Server**: http://localhost:5173
- **Dashboard**: http://localhost:8501
- **Kubernetes Docs**: See k8s/ directory
- **Docker Docs**: See Dockerfile & docker-compose files

---

**Architecture Guide Complete** ✅  
Maintains single source of truth while enabling independent team development.

