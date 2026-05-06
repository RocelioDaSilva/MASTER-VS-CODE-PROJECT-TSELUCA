# Development Workflow

Guidelines for developers working on GEESP-Angola platform.

---

## Project Structure (Quick Mental Model)

```
nevermindu/                    ← Frontend + Express backend (what users see/interact with)
└── src/                          React components, UI logic
└── server.ts                      API endpoints, database layer

geesp-angola/                  ← Python MCDA engine (business logic)
└── dashboard/                    Streamlit UI (alternative to React)
└── utils/                        Shared utilities, MCDA engine
└── tests/                        All tests (68/68 passing)

DOCUMENTATION FILES (this folder)
└── PRODUCTION_ARCHITECTURE.md    ← System overview
└── DEPLOYMENT_GUIDE.md           ← How to deploy
└── DEVELOPMENT_WORKFLOW.md       ← This file
```

---

## Getting Started

### 1. Initial Setup
```bash
# Clone and navigate
git clone <repo>
cd Full\ project/02_Code

# Install both backends
cd nevermindu && npm install && cd ..
cd geesp-angola && pip install -r requirements.txt && cd ..
```

### 2. Verify Everything Works
```bash
# Terminal 1: React + API
cd nevermindu && npm run dev

# Terminal 2: Python tests
cd geesp-angola && python -m pytest tests/ -v

# Browser: http://localhost:5173
```

### 3. Create Feature Branch
```bash
git checkout -b feature/my-feature-name
```

---

## Development Workflows by Role

### Frontend Developer (React/TypeScript)

**Typical Task**: Add new analytics chart to Dashboard

```bash
cd nevermindu/src/components

# Create: AdvancedChart.tsx
# Import in: App.tsx
# Add to tab: financial or analysis

npm run lint  # Check TypeScript errors
npm run dev   # Hot reload in browser
```

**File Locations**:
- Components: `src/components/*.tsx`
- Images: `src/assets/`
- Styles: In component (Tailwind)
- Types: `src/types.ts`
- API calls: `src/api/` (create if needed)

**Key Technologies**:
- React 19 hooks (useState, useEffect, useContext)
- Tailwind CSS (utility classes)
- Framer Motion (animations)
- Recharts (charts) or Leaflet (maps)

**Testing**:
```bash
# No automated tests yet (add in future)
# Manual testing in browser
```

---

### Backend Developer (Express/TypeScript)

**Typical Task**: Add new API endpoint for report generation

```bash
# Edit: server.ts

app.post('/api/generate-report', async (req: Request, res: Response) => {
  try {
    const { scenario_id, format } = req.body;
    // Implementation here
    res.json({ report_url: "..." });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

# Then in frontend, call:
fetch('/api/generate-report', {
  method: 'POST',
  body: JSON.stringify({ scenario_id, format })
})
```

**Database Tasks**:
```bash
# Add column to scenarios table
# Modify: server.ts database initialization

db.exec(`
  ALTER TABLE scenarios ADD COLUMN custom_field TEXT;
`);
```

**Key Files**:
- API: `server.ts` (430 lines, all endpoints here)
- Types: `src/types.ts` (shared with frontend)
- Database: SQLite (geesp_scenarios.db)

**Testing**:
```bash
# Manual API testing
curl -X POST http://localhost:3000/api/health

# Or use Postman/Insomnia
# Or use: npm install -g rest-client
```

---

### Python Developer (MCDA / Analytics)

**Typical Task**: Improve MCDA scoring algorithm

```bash
cd geesp-angola

# File: utils/mcda_engine.py (if doesn't exist, create it)
# Or modify: dashboard/app.py

# Improve scoring:
def calculate_mcda_score(
  community: Community, 
  weights: MCDAWeights
) -> float:
  # Your new logic here
  return score

# Run tests
python -m pytest tests/test_mcda.py -v
```

**Key Files**:
- MCDA Logic: `utils/mcda_engine.py`
- Dashboard: `dashboard/app.py`
- Data: `data/communities.csv`
- Tests: `tests/test_mcda.py`

**Data Structure** (from constants):
```python
class Community:
  id: str
  name: str
  province: str
  ghi: float          # Solar irradiance
  slope: float        # Terrain slope
  distToGrid: float   # Distance to grid (km)
  population: int

class MCDAWeights:
  climate: float      # Sum must = 1.0
  soil: float
  terrain: float
  infrastructure: float
```

**Testing MCDA**:
```bash
python -m pytest tests/test_mcda.py::test_score_calculation -v

# Or manual test
python
>>> from utils.mcda_engine import calculate_score
>>> result = calculate_score(community, weights)
>>> print(result)
```

---

### Full-Stack Developer (Both)

**Typical Task**: Add new filtering criterion

```bash
# Backend (Express): Add filter logic in server.ts
app.post('/api/filter-communities', (req, res) => {
  // Add new criterion check here
});

# Frontend: Update AdvancedFilter.tsx
// Add new input field
// Add to FilterCriteria interface
// Pass to backend

npm run dev      # Start everything
npm run lint    # Check TypeScript
```

---

## Code Style & Standards

### TypeScript
```typescript
// Use interfaces, not types
interface UserData {
  id: string;
  name: string;
}

// Use const, avoid var
const value = 42;

// Arrow functions preferred
const calculate = (x: number): number => x * 2;

// Add prop types
const MyComponent: React.FC<{label: string}> = ({label}) => (
  <div>{label}</div>
);
```

### Python
```python
# Follow PEP 8
def calculate_mcda_score(community: Community, weights: MCDAWeights) -> float:
    """Docstring required."""
    return score

# Type hints required
def filter_communities(communities: List[Community], min_ghi: float) -> List[Community]:
    pass

# Use logging, not print
import logging
logger = logging.getLogger(__name__)
logger.info("Processing community: %s", community.name)
```

### CSS (Tailwind)
```tsx
// Use Tailwind classes, avoid custom CSS
<div className="p-4 bg-emerald-600 hover:bg-emerald-700 rounded-lg">
  Content
</div>

// For complex animations, use Framer Motion
<motion.div
  animate={{ scale: 1.1 }}
  transition={{ duration: 0.3 }}
>
  Animated content
</motion.div>
```

---

## Testing Guidelines

### Unit Tests (Python)

```python
# tests/test_mcda.py

import pytest
from utils.mcda_engine import calculate_score
from types import Community, MCDAWeights

def test_score_calculation():
    """Test MCDA score calculation."""
    community = Community(
        id="test",
        name="Test Community",
        ghi=5.5,
        slope=5,
        distToGrid=20,
        population=1000
    )
    weights = MCDAWeights(climate=0.4, soil=0.3, terrain=0.2, infrastructure=0.1)
    
    score = calculate_score(community, weights)
    
    assert 0 <= score <= 100
    assert isinstance(score, float)

# Run: pytest tests/test_mcda.py -v
```

### Integration Tests

```bash
# Test API endpoint
curl -X POST http://localhost:3000/api/calculate-financial-metrics \
  -H "Content-Type: application/json" \
  -d '{
    "ghi": 5.5,
    "solar_params": {
      "efficiency": 0.18,
      "lifetime": 25,
      "capitalCost": 15000,
      "omCost": 200
    }
  }'

# Expected response:
# {"lcoe": 0.095, "roi": 125.5, "payback_years": 12.3, ...}
```

### E2E Tests (Manual)

1. Save scenario
2. Load scenario
3. Apply filters
4. Export PDF
5. Compare scenarios
6. Chat with Gemini

---

## Common Tasks

### Add a New Community

```python
# Edit: geesp-angola/data/communities.csv
# Or in code: geesp-angola/constants.py if using Python dict

ANGOLA_COMMUNITIES = [
    {
        "id": "new_001",
        "name": "New Community",
        "province": "Luanda",
        "ghi": 5.8,
        "soilType": "Sandy",
        "slope": 3,
        "distToGrid": 15,
        "population": 2500
    },
    # ...existing communities...
]
```

### Add a New Weight for MCDA

```typescript
// Frontend: types.ts
interface MCDAWeights {
  climate: number;
  soil: number;
  terrain: number;
  infrastructure: number;
  newFactor: number;  // ← NEW
}

// Backend: server.ts calculateFinancialMetrics()
const newFactorScore = (community.newValue / maxValue) * weights.newFactor;
```

### Deploy a Hotfix

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug
# Make fix
git commit -m "fix: critical issue"
git push origin hotfix/critical-bug
# Create pull request, merge to main
# Deploy using steps in DEPLOYMENT_GUIDE.md
```

---

## Debugging Tips

### Frontend (React)
```javascript
// Browser console
console.log("State:", weights);  // Check state values
debugger;                         // Breakpoints
// Or use React DevTools extension
```

### Backend (Express)
```typescript
// server.ts
console.log("Received:", req.body);
console.error("Error:", error.stack);

// Or use debugger
node --inspect server.ts
// Then visit chrome://inspect
```

### Python
```python
# Use debugger
import pdb; pdb.set_trace()

# Or logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use IDE debugger (VS Code, PyCharm)
```

---

## Performance Profiling

### Frontend
```bash
# React Profiler
# In React DevTools → Profiler tab
# Record interaction → See render times
```

### Backend
```bash
# Simple timing
const start = Date.now();
// ... operation ...
console.log(`Time: ${Date.now() - start}ms`);

# Or use benchmarking tools
npm install -g autocannon
autocannon http://localhost:3000/api/health
```

### Python
```python
import time

start = time.time()
# ... operation ...
elapsed = time.time() - start
print(f"Time: {elapsed:.3f}s")
```

---

## Dependency Management

### Add to Frontend
```bash
cd nevermindu
npm install package-name
# Or dev dependency:
npm install --save-dev package-name

git add package.json package-lock.json
git commit -m "feat: add package-name"
```

### Add to Python
```bash
cd geesp-angola
pip install package-name
pip freeze > requirements.txt

git add requirements.txt
git commit -m "feat: add package-name"
```

---

## Pull Request Process

1. **Create branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   ```bash
   # Edit files
   npm run lint      # TypeScript check
   npm run test      # If tests exist
   git add .
   git commit -m "feat: brief description"
   ```

3. **Push & create PR**
   ```bash
   git push origin feature/my-feature
   # On GitHub: Create Pull Request
   ```

4. **Code review checklist**
   - [ ] Tests pass
   - [ ] No TypeScript errors
   - [ ] Code follows style guide
   - [ ] Documentation updated
   - [ ] At least 1 approval

5. **Merge**
   ```bash
   # After approval
   git merge --squash feature/my-feature
   git push origin main
   ```

---

## Troubleshooting Development Issues

### Port already in use
```bash
# Kill process using port 3000
lsof -ti:3000 | xargs kill -9
```

### Node modules issue
```bash
rm -rf node_modules package-lock.json
npm install
```

### TypeScript errors
```bash
npm run lint  # See full errors
# Or restart editor (VS Code)
```

### Tests failing
```bash
pytest tests/ -v --tb=short  # Verbose output
pytest tests/test_mcda.py::test_name -v  # Single test
```

---

## Getting Help

1. **Check documentation**
   - PRODUCTION_ARCHITECTURE.md
   - Component comments in code
   - Inline docstrings

2. **Search existing issues**
   - GitHub Issues
   - StackOverflow (tag: geesp-angola or reactjs, python)

3. **Ask team**
   - Slack #development channel
   - Email: dev-team@example.com

4. **Debug locally**
   - Enable verbose logging
   - Use debugger (pdb, Chrome DevTools)
   - Check git history (git log --oneline)

---

## Quick Command Reference

```bash
# Frontend development
cd nevermindu && npm run dev          # Start both server + client
npm run lint                           # Check TypeScript
npm run build                          # Production build

# Backend development
npm run server                         # Just Express server
npm run client                         # Just Vite

# Python development
cd geesp-angola
python -m pytest tests/ -v             # Run all tests
streamlit run dashboard/app.py         # Run dashboard
python -c "import utils; print(ok)"    # Quick test

# Git workflows
git status                             # Check changes
git diff                               # See differences
git log --oneline                      # Commit history
git stash                              # Temporary save
git cherry-pick <commit>               # Apply specific commit
```

---

## Next Steps

1. **Fork the repository** (if contributing)
2. **Set up locally** using "Getting Started" section
3. **Pick an issue** or feature to work on
4. **Create a branch** with clear name
5. **Follow PR process** above
6. **Deploy to staging** for testing
7. **Get code review** from team
8. **Merge to main** with squash commit
9. **Deploy to production** using DEPLOYMENT_GUIDE.md

---

**Happy coding! 🚀**

For questions, see PRODUCTION_ARCHITECTURE.md or contact the dev team.

Last Updated: 2026-03-05
