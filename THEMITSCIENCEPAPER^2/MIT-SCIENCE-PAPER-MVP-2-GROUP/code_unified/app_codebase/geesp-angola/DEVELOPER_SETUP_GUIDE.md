# 👨‍💻 DEVELOPER SETUP GUIDE
## Getting Started with GEESP-Angola (Backend + Frontend)
### Phase 6: Comprehensive Developer Documentation

---

## 🚀 QUICK START (5 minutes)

### Prerequisites
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- Git
- Database (PostgreSQL recommended, SQLite for dev)

### One-Time Setup

```bash
# Clone repository
git clone <your-repo-url>
cd geesp-angola

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate        # ..\venv\Scripts\activate on Windows
pip install -r ../requirements.txt

# Frontend setup
cd ../frontend
npm install

# Return to root
cd ..
```

---

## 🖥️ RUNNING LOCALLY

### Option 1: Full Stack (Everyone)

**Terminal 1 - Backend API**:
```bash
cd backend
source venv/bin/activate
export PYTHONPATH=/path/to/geesp-angola/backend:$PYTHONPATH
python -m uvicorn api.api:app --reload --port 8000
# ✅ Backend running at http://localhost:8000
# 📚 API docs at http://localhost:8000/docs
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
# ✅ Frontend running at http://localhost:5173
```

**Terminal 3 - Dashboard** (optional):
```bash
cd backend
source venv/bin/activate
streamlit run dashboard/app.py
# ✅ Dashboard at http://localhost:8501
```

### Option 2: Backend Only (Python Developers)

```bash
cd backend
source venv/bin/activate
python -m uvicorn api.api:app --reload
```

### Option 3: Frontend Only (React Developers)

```bash
cd frontend
npm run dev
# API calls will proxy to http://localhost:8000
```

---

## 📁 FOLDER STRUCTURE FOR DEVELOPERS

### If You're Working on Backend:

```
backend/
├── api/                         # ← Add REST endpoints here
│   └── api.py                  # ← Modify this for new endpoints
├── scripts/                     # ← Add analysis engines here
│   ├── mcda_analysis.py        # ← MCDA engine (modify for new analysis)
│   ├── lcoe_calculator.py      # ← Financial analysis
│   └── gee_integration.py      # ← Geospatial integration
├── utils/                       # ← Add utilities here
│   ├── core_utils.py           # ← Core functions (centralized)
│   └── validation.py           # ← Input validation
├── models/                      # ← Add database models here
│   ├── scenario.py             # ← Scenario model
│   └── results.py              # ← Results model
├── dashboard/                   # ← Modify dashboard pages
│   ├── app.py                  # ← Main dashboard
│   └── pages/                  # ← Dashboard pages
├── tests/                       # ← Add tests here
│   ├── unit/                   # ← Unit tests
│   ├── integration/            # ← Integration tests
│   └── conftest.py             # ← Shared fixtures
└── data/
    └── processed/              # ← Generated map data (.npy files)
```

### If You're Working on Frontend:

```
frontend/
├── src/
│   ├── components/             # ← Add React components here
│   │   ├── AdvancedFilter.tsx  # ← Example component
│   │   └── ... other components
│   ├── services/               # ← Add API services here
│   │   ├── apiService.ts       # ← API calls
│   │   └── geminiService.ts    # ← AI integration
│   ├── middleware/             # ← Auth & middleware
│   ├── routes/                 # ← Route definitions
│   ├── types/                  # ← TypeScript interfaces
│   ├── utils/                  # ← Frontend utilities
│   ├── App.tsx                 # ← Main component
│   └── main.tsx                # ← Entry point
├── package.json                # ← Dependencies
├── tsconfig.json               # ← TypeScript config
├── vite.config.ts              # ← Build config
└── index.html                  # ← HTML entry
```

---

## 💡 COMMON DEVELOPMENT TASKS

### Adding a New Backend Endpoint

**1. Create the handler in `backend/api/api.py`**:
```python
@app.post('/api/myfeature')
async def my_feature(request: MyFeatureRequest):
    """New feature endpoint"""
    result = process_data(request)
    return {'status': 'success', 'data': result}
```

**2. Define the request/response model**:
```python
from pydantic import BaseModel

class MyFeatureRequest(BaseModel):
    input_data: str
    threshold: float = 0.5

class MyFeatureResponse(BaseModel):
    result: str
    confidence: float
```

**3. Test it**:
```bash
cd backend
pytest tests/unit/test_myfeature.py -v
```

### Adding a New React Component

**1. Create component in `frontend/src/components/MyComponent.tsx`**:
```typescript
import React from 'react';

export const MyComponent: React.FC<Props> = ({ title }) => {
  return <div>{title}</div>;
};
```

**2. Use it in your page**:
```typescript
import { MyComponent } from '@/components/MyComponent';

export default function MyPage() {
  return <MyComponent title="Hello" />;
}
```

**3. Test with npm**:
```bash
cd frontend
npm run dev
```

### Running Tests

**Unit Tests**:
```bash
cd backend
pytest tests/unit/ -v
```

**Integration Tests**:
```bash
cd backend
pytest tests/integration/ -v
```

**All Tests**:
```bash
cd backend
pytest -v
```

**With Coverage**:
```bash
cd backend
pytest --cov=. tests/
```

---

## 🔧 CONFIGURATION

### Backend Configuration

**Environment Variables** (`.env`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/geesp_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Google Earth Engine
GEE_CREDENTIALS=/path/to/gee_credentials.json

# Logging
LOG_LEVEL=DEBUG
```

### Frontend Configuration

**Environment Variables** (`.env`):
```bash
# Backend API
VITE_API_URL=http://localhost:8000

# Gemini AI
VITE_GEMINI_API_KEY=your_api_key

# Other services
VITE_APP_NAME=GEESP-Angola
```

---

## 🗄️ DATABASE SETUP

### Using SQLite (Development)

No setup needed - SQLite auto-creates `app.db`

### Using PostgreSQL (Recommended)

**1. Install PostgreSQL**:
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows: Download installer
https://www.postgresql.org/download/windows/
```

**2. Create database**:
```bash
psql -U postgres
CREATE DATABASE geesp_db;
\q
```

**3. Update `.env`**:
```bash
DATABASE_URL=postgresql://postgres:password@localhost/geesp_db
```

**4. Run migrations**:
```bash
cd backend
alembic upgrade head
```

---

## 📝 CODING STANDARDS

### Python (Backend)

**Follow PEP 8**:
```python
# ✅ Good
def calculate_mcda_score(criteria: Dict[str, float], weights: Dict[str, float]) -> float:
    """Calculate MCDA score.
    
    Args:
        criteria: Criteria values
        weights: Criteria weights
        
    Returns:
        Calculated score
    """
    total = sum(criteria[k] * weights[k] for k in criteria)
    return total


# ❌ Bad
def calculateMCDAScore(criteria,weights):
    total=sum(criteria[k]*weights[k]for k in criteria)
    return total
```

**Type Hints**:
```python
# ✅ Good
def process_data(data: Dict[str, Any]) -> List[float]:
    pass

# ❌ Bad
def process_data(data):
    pass
```

**Imports**:
```python
# ✅ Good - organized, alphabetical
from typing import Dict, List
from pydantic import BaseModel
from backend.utils.validation import validate_input
from backend.scripts.mcda_analysis import MCDAnalyzer

# ❌ Bad - disorganized, wildcard
from backend.utils import *
from backend.scripts import *
```

### TypeScript (Frontend)

**Strict Mode**:
```typescript
// ✅ Good
interface Props {
  title: string;
  count: number;
}

export const MyComponent: React.FC<Props> = ({ title, count }) => {
  return <div>{title}: {count}</div>;
};

// ❌ Bad
export const MyComponent = ({ title, count }: any) => {
  return <div>{title}: {count}</div>;
};
```

---

## 🧪 TESTING WORKFLOW

### Backend Testing

**Create test file** (`tests/unit/test_myfeature.py`):
```python
import pytest
from backend.scripts.mcda_analysis import MCDAnalyzer

@pytest.fixture
def analyzer():
    return MCDAnalyzer()

def test_mcda_computation(analyzer):
    result = analyzer.compute({'score': 0.5})
    assert result > 0

def test_mcda_with_invalid_input(analyzer):
    with pytest.raises(ValueError):
        analyzer.compute(None)
```

**Run tests**:
```bash
pytest tests/unit/test_myfeature.py -v
```

### Frontend Testing

**Create test file** (`src/__tests__/components.test.tsx`):
```typescript
import { render, screen } from '@testing-library/react';
import { MyComponent } from '../components/MyComponent';

test('renders component', () => {
  render(<MyComponent title="Test" />);
  expect(screen.getByText('Test')).toBeInTheDocument();
});
```

---

## 🐛 DEBUGGING

### Backend Debugging

**Using print debugging**:
```python
print(f"Value: {value}")  # Simple debug
```

**Using logging**:
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing: {data}")
logger.error(f"Error: {error}")
```

**Using VS Code Debugger**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["api.api:app", "--reload"],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

**Browser DevTools**:
- Open Chrome DevTools (F12)
- Console tab for errors
- Network tab for API calls
- React DevTools extension

**React Error Boundaries**:
```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({error, resetErrorBoundary}) {
  return (
    <div>
      <h1>Error occurred!</h1>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

export default function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MyComponent />
    </ErrorBoundary>
  )
}
```

---

## 🔄 GIT WORKFLOW

### Branch Naming

```bash
feature/add-new-analysis
bugfix/fix-mcda-calculation
docs/update-readme
refactor/consolidate-utils
```

### Commit Convention

```bash
git commit -m "feat: add MCDA endpoint"
git commit -m "fix: resolve scoring bug"
git commit -m "docs: update API docs"
git commit -m "refactor: consolidate utilities"
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added
- [ ] Tests pass locally

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
```

---

## 📦 DEPENDENCIES MANAGEMENT

### Python

**Installing dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt   # Development tools
```

**Adding new dependency**:
```bash
pip install new_package
pip freeze > requirements.txt
```

**Checking for updates**:
```bash
pip list --outdated
```

### Node (Frontend)

**Installing dependencies**:
```bash
npm install
npm install --save package-name      # Production
npm install --save-dev package-name  # Development
```

**Lock dependencies**:
```bash
npm ci  # Uses package-lock.json
```

---

## 🚀 DEPLOYMENT CHECKLIST

Before deploying to production:

- [ ] All tests pass locally (`pytest`)
- [ ] No console errors in frontend
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Code reviewed by peer
- [ ] No hardcoded passwords/secrets
- [ ] API documentation updated
- [ ] Version bump in `package.json`/`setup.py`

---

## 📞 GETTING HELP

### Common Issues

**"Module not found" error**:
```bash
export PYTHONPATH=/path/to/geesp-angola/backend:$PYTHONPATH
python -m uvicorn api.api:app --reload
```

**Frontend build errors**:
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Database connection errors**:
```bash
# Check DATABASE_URL in .env
# Verify PostgreSQL is running
# Try SQLite: DATABASE_URL=sqlite:///app.db
```

### Documentation

- [Backend API Docs](ARCHITECTURE_GUIDE.md#backend-architecture)
- [Frontend Setup](ARCHITECTURE_GUIDE.md#frontend-architecture)
- [Architecture Guide](ARCHITECTURE_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)

### Support

- Issue Tracker: GitHub Issues
- Discussions: GitHub Discussions
- Email: your-email@example.com

---

## 🎯 NEXT STEPS

1. **Clone the repo** and run the setup
2. **Choose your stack** (backend or frontend)
3. **Follow the coding standards**
4. **Write tests** for your changes
5. **Create a pull request**

**Welcome to the team!** 🎉

