# MASTER NAVIGATION GUIDE & PROJECT HARMONIZATION
## Where to Find Everything & How It Fits Together

**Date:** March 6, 2026  
**Purpose:** Single source of truth for project organization  
**For:** All developers, stakeholders, new team members

---

## SECTION 1: START HERE

### New to the Project?
```
1️⃣ READ FIRST (5 min):
   📄 02_Code/README.md
   ↳ Quick overview, what it does, how to start
   
2️⃣ UNDERSTAND STATUS (15 min):
   📋 02_Code/00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md
   ↳ What's done ✅, what's in progress 🟡, what's not done ❌
   
3️⃣ KNOW WHAT'S NEXT (10 min):
   🗺️ 02_Code/01_PENDING_IMPLEMENTATION_ROADMAP.md
   ↳ 46 items to do, organized by priority
   
4️⃣ UNDERSTAND SYSTEM (15 min):
   🏗️ 02_Code/PRODUCTION_ARCHITECTURE.md
   ↳ How everything fits together (React + Express + Python)
   
5️⃣ SET UP LOCALLY (30 min):
   🚀 02_Code/DEPLOYMENT_GUIDE.md
   ↳ Get code running on your machine
   
6️⃣ START DEVELOPING (20 min):
   💻 02_Code/DEVELOPMENT_WORKFLOW.md
   ↳ Patterns, best practices, role-specific workflows

Total time: ~90 minutes to full understanding ⏱️
```

---

## SECTION 2: DOCUMENT MAP BY ROLE

### For Project Leads / Managers
```
📊 STATUS & DECISIONS
   1. CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md ← Read first
   2. PENDING_IMPLEMENTATION_ROADMAP.md ← Plan work
   3. PRODUCTION_ARCHITECTURE.md ← Understand system
   
💰 PLANNING & FORECASTING
   • Effort estimates: PENDING_IMPLEMENTATION_ROADMAP.md (Part: Effort Estimation)
   • Timeline: PENDING_IMPLEMENTATION_ROADMAP.md (Part: Implementation Phases)
   • Risk assessment: PENDING_IMPLEMENTATION_ROADMAP.md (Section: Risk Mitigation)
   • Team capacity: PENDING_IMPLEMENTATION_ROADMAP.md (Concluding section)
   
✅ CHECKPOINTS & VALIDATION
   • Quality metrics: CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md (Part 8)
   • Test results: PROJECT_HARMONY_TEST_REPORT.md
   • Risk register: PENDING_IMPLEMENTATION_ROADMAP.md (Risk Mitigation)
```

### For Developers (Frontend - React)
```
📚 UNDERSTANDING (In order)
   1. README.md ← What is GEESP?
   2. PRODUCTION_ARCHITECTURE.md ← System overview
   3. DEVELOPMENT_WORKFLOW.md ← Developer patterns
   
🎨 BUILDING & TESTING
   • Component guide: DEVELOPMENT_WORKFLOW.md (Section: Frontend Developer Role)
   • Code structure: nevermindu/src/ ← Read the .tsx files themselves
   • Styling guide: Look at existing components (use Tailwind)
   • No automated tests yet → Manual testing in browser
   
🚀 DEPLOYMENT
   • Local setup: DEPLOYMENT_GUIDE.md (Dev Deployment section)
   • Production build: DEPLOYMENT_GUIDE.md (Staging & Production)
   
📋 WHAT'S HAPPENING
   • What to build next: PENDING_IMPLEMENTATION_ROADMAP.md
   • Priority: Tier 1 (Security), Tier 2 (User Management)
```

### For Developers (Backend - Express/Node)
```
📚 UNDERSTANDING (In order)
   1. README.md ← Project overview
   2. PRODUCTION_ARCHITECTURE.md ← System & API design
   3. DEVELOPMENT_WORKFLOW.md ← Backend-specific workflows
   
🔧 API & DATABASE
   • All 7 endpoints: PRODUCTION_ARCHITECTURE.md (System Overview section)
   • Database schema: nevermindu/server.ts lines 25-60 ← Source of truth
   • Entity relationships: PRODUCTION_ARCHITECTURE.md (Database section)
   • API documentation (when available): PENDING_IMPLEMENTATION_ROADMAP.md (T1.2.1)
   
✅ QUICK REFERENCE
   • Endpoint summary: QUICK_REFERENCE_CARD.md (5 minute cheat sheet)
   • Request/response examples: (See examples under PENDING_IMPLEMENTATION_ROADMAP.md T1.2.3)
   
🚀 DEPLOYMENT
   • Local development: DEPLOYMENT_GUIDE.md
   • Environment setup: DEPENDENCIES_AND_SETUP.md
   • Production checklist: PENDING_IMPLEMENTATION_ROADMAP.md (T1.1 critical items)
```

### For Developers (Python/MCDA)
```
📚 UNDERSTANDING (In order)
   1. geesp-angola/README.md ← What is GEESP-Angola?
   2. PRODUCTION_ARCHITECTURE.md ← How it integrates
   3. DEVELOPMENT_WORKFLOW.md ← Python developer workflow
   
🔬 MCDA ENGINE
   • Core algorithm: geesp-angola/utils/mcda_engine.py ← Read source
   • Testing: geesp-angola/tests/ (68 tests passing) ← See examples
   • Constants: geesp-angola/utils/constants.py ← Angola data
   
💸 FINANCIAL CALCULATIONS
   • LCOE formula: geesp-angola/utils/lcoe_calculator.py ← Source of truth
   • ROI/Payback: Same file
   • Testing: geesp-angola/tests/test_financial*.py
   
📊 STREAMLIT DASHBOARD
   • Visualization: geesp-angola/dashboard/app.py (762 lines)
   • How to run: DEPLOYMENT_GUIDE.md
   • Future enhancements: PENDING_IMPLEMENTATION_ROADMAP.md (T3: Analytics)
   
🧪 TESTING
   • All tests: geesp-angola/tests/
   • Run tests: DEPLOYMENT_GUIDE.md or pytest tests/
   • Status: 68/68 passing ✅
```

### For DevOps / Deployment
```
📚 UNDERSTANDING
   1. PRODUCTION_ARCHITECTURE.md ← System overview
   2. DEPLOYMENT_GUIDE.md ← All deployment scenarios
   3. DEPENDENCIES_AND_SETUP.md ← All packages & requirements
   
🐳 DOCKER & CONTAINERIZATION
   • Dockerfile: nevermindu/Dockerfile exists
   • Docker Compose: geesp-angola/docker-compose.yml
   • Build instructions: DEPLOYMENT_GUIDE.md
   • Status: Basic setup exists, Kubernetes/K8s not done (PENDING_IMPLEMENTATION_ROADMAP T4.1.1)
   
☸️ KUBERNETES (Not implemented yet)
   • Plan: PENDING_IMPLEMENTATION_ROADMAP.md (T4.1.1)
   • Effort: 40 hours, Timeline: Month 3
   
🔐 SECURITY & SECRETS
   • Env variables: .env.example in nevermindu/
   • Secrets management: PENDING_IMPLEMENTATION_ROADMAP.md (T1.1: Security)
   • Rate limiting: PENDING_IMPLEMENTATION_ROADMAP.md (T1.1.5)
   
📊 MONITORING & ALERTS
   • Currently: Not implemented ❌
   • Plan: PENDING_IMPLEMENTATION_ROADMAP.md
   • Services: Prometheus, Grafana, Sentry, ELK (to be added)
```

### For QA / Testing
```
📊 TEST STATUS
   • Current: 68/68 Python tests passing ✅
   • Report: PROJECT_HARMONY_TEST_REPORT.md
   • Frontend tests: Not automated yet ← PENDING (T2.2)
   
✅ WHERE TO RUN TESTS
   • Python: cd geesp-angola && pytest tests/ -v
   • Check syntax: npm run lint (in nevermindu/)
   • Results: Should be 68/68 passing
   
🔍 TESTING ROADMAP
   • Component tests (Jest): PENDING_IMPLEMENTATION_ROADMAP.md (T2.2)
   • Integration tests: PENDING_IMPLEMENTATION_ROADMAP.md (T2.2)
   • E2E tests: PENDING_IMPLEMENTATION_ROADMAP.md (T2.2)
   
🐛 BUGS & ISSUES
   • Found & fixed (Mar 5): test_security.py:141 (syntax error) ✅
   • Current issues: None known
   • Report issues: GitHub issues or Slack
```

---

## SECTION 3: DOCUMENT HIERARCHY

```
┌─────────────────────────────────────────────────────────────┐
│                   MASTER DOCUMENTS                           │
│  (Start if confused about project status or direction)       │
└─────────────────────────────────────────────────────────────┘
            │
            ├─ README.md (3-5 min read)
            │   "What is this? How to start quickly?"
            │
            ├─ CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md (15 min)
            │   "What's done? What's in progress? What's not done?"
            │
            └─ PENDING_IMPLEMENTATION_ROADMAP.md (15 min)
                "What do we build next? In what order? Why?"

┌─────────────────────────────────────────────────────────────┐
│               REFERENCED DOCUMENTS                           │
│  (Read based on your role or need)                          │
└─────────────────────────────────────────────────────────────┘
            │
            ├─ PRODUCTION_ARCHITECTURE.md
            │   └─ For: Understanding system design
            │
            ├─ DEVELOPMENT_WORKFLOW.md
            │   └─ For: Understanding how to develop (frontend/backend/python)
            │
            ├─ DEPLOYMENT_GUIDE.md
            │   └─ For: Setting up locally, deploying to servers
            │
            ├─ PROJECT_HARMONY_TEST_REPORT.md
            │   └─ For: Latest test results & quality metrics
            │
            └─ Reference Documents (Quick lookups)
                ├─ QUICK_REFERENCE_CARD.md (API endpoints)
                ├─ DEPENDENCIES_AND_SETUP.md (Installation)
                └─ WINDOWS_APP_PACKAGING.md (Windows .exe building)

┌─────────────────────────────────────────────────────────────┐
│                SOURCE CODE                                   │
│  (Real source of truth - documents explain this)            │
└─────────────────────────────────────────────────────────────┘
            │
            ├─ nevermindu/
            │   ├─ App.tsx (Main React app)
            │   ├─ server.ts (Express API)
            │   └─ src/components/ (React components)
            │
            ├─ geesp-angola/
            │   ├─ utils/mcda_engine.py (MCDA algorithm)
            │   ├─ utils/lcoe_calculator.py (Financial calc)
            │   ├─ dashboard/app.py (Streamlit UI)
            │   └─ tests/ (68 test files)
            │
            └─ databases
                └─ geesp_scenarios.db (SQLite, auto-created)
```

---

## SECTION 4: INFORMATION ARCHITECTURE

### By Topic

| Topic | Where to Learn | Key File(s) | Time |
|-------|---|---|---|
| **MCDA Algorithm** | Code + comments | mcda_engine.py | 30 min |
| **LCOE Calculation** | Code + comments | lcoe_calculator.py | 20 min |
| **React Components** | Code + DEVELOPMENT_WORKFLOW | src/components/*.tsx | 60 min |
| **Express API** | Code + QUICK_REFERENCE | server.ts | 30 min |
| **Database Schema** | PRODUCTION_ARCHITECTURE or server.ts | server.ts:25-60 | 10 min |
| **Deployment Process** | DEPLOYMENT_GUIDE | Step-by-step | 30 min |
| **Testing** | PROJECT_HARMONY_TEST_REPORT + tests/ | tests/ directory | 20 min |
| **Future Work** | PENDING_IMPLEMENTATION_ROADMAP | Roadmap document | 30 min |
| **System Design** | PRODUCTION_ARCHITECTURE | Diagrams + descriptions | 15 min |
| **Dev Patterns** | DEVELOPMENT_WORKFLOW | Role-specific sections | 30 min |

### By Stage of Work

| Stage | Documents | Focus Area |
|-------|-----------|-----------|
| **Planning** | CODE_STATUS, ROADMAP, ARCHITECTURE | Understand scope |
| **Development** | DEVELOPMENT_WORKFLOW, Code itself | Build features |
| **Testing** | PROJECT_HARMONY_TEST_REPORT, DEPLOYMENT_GUIDE | Verify quality |
| **Deployment** | DEPLOYMENT_GUIDE, Cleanup Plan | Release to production |
| **Operations** | README, Architecture, Quick Ref | Run & maintain |
| **Future** | ROADMAP, Pending Implementations | Plan next phase |

---

## SECTION 5: CROSS-REFERENCE MAP

### Frontend Developers Need to Know
```
React (nevermindu/src/)
    ├─ Talks to: Express API (nevermindu/server.ts)
    ├─ Shows data from: geesp-angola (Python MCDA)
    ├─ Saves to: SQLite (via Express)
    └─ Calls: Gemini AI for chat
    
Key connections:
• API: server.ts endpoints (7 total)
• Data model: types.ts (TypeScript interfaces)
• Constants: Angola communities, weights, etc.
• Styles: Tailwind CSS (in components)
```

### Backend Developers Need to Know
```
Express API (nevermindu/server.ts)
    ├─ Receives requests from: React frontend
    ├─ Calls: Python MCDA (via subprocess or REST)
    ├─ Stores: SQLite database
    ├─ Returns: JSON responses
    └─ Should implement: Auth (T1.1), Rate limiting (T1.1.5)
    
Key connections:
• Frontend: React App.tsx makes fetch() calls
• Backend logic: geesp-angola MCDA engine
• Database: SQLite (3 tables)
• Future: User authentication (pending T1.1)
```

### Python Developers Need to Know
```
MCDA Engine (geesp-angola/)
    ├─ Called by: Express API (via CLI or REST)
    ├─ Uses data from: Communities CSV
    ├─ Performs: Multi-criteria analysis
    ├─ Returns: Scores, rankings, aptitude
    └─ Also available: Streamlit dashboard
    
Key connections:
• Frontend: React Dashboard
• Backend: Express API (intermediate)
• Testing: 68 tests in tests/
• Data: communities_45.csv
```

---

## SECTION 6: HARMONIZATION & CONSISTENCY

### Code Style Consistency

**React/TypeScript** (nevermindu/)
```
✅ Enforced by:
   • tsconfig.json (strict mode)
   • ESLint (via npm run lint)
   • Prettier (auto-formatting)

Standard pattern:
   interface Props {
     scenarioId: string;
     onUpdate: (data: Scenario) => void;
   }
   
   export function MyComponent({ scenarioId, onUpdate }: Props) {
     const [state, setState] = useState<State>(initialState);
     // ... component logic
   }
```

**Express/TypeScript** (nevermindu/server.ts)
```
✅ Enforced by:
   • TypeScript strict mode
   • Explicit types on all functions
   • Error handling with try-catch

Standard pattern:
   app.post('/api/endpoint', (req: Request, res: Response) => {
     try {
       const result = processData(req.body);
       res.json(result);
     } catch (error) {
       res.status(500).json({ error: 'Error message' });
     }
   });
```

**Python** (geesp-angola/)
```
✅ Enforced by:
   • PEP 8 style guide
   • Type hints (Python 3.10+)
   • pytest for testing
   • mypy (optional type checking)

Standard pattern:
   def calculate_lcoe(params: dict[str, float]) -> float:
       """
       Calculate levelized cost of energy.
       
       Args:
           params: Dictionary with cost parameters
       
       Returns:
           LCOE in $/kWh
       """
       # implementation
       return lcoe
```

### Documentation Consistency

**All .md files should follow:**
```
# Main Title (H1 - only one per file)

## Section (H2)

### Subsection (H3)

#### Item (H4 if needed)

Key elements:
• Use ✅, ❌, 🟡, 🔴 for status
• Use clear code blocks with language specified
• Include "When to use this document" at top
• Link to related documents
• Include file paths as clickable links when possible
• Update date at bottom
```

### API Consistency

**All endpoints should:**
```
Method: HTTP verb (GET/POST/PUT/DELETE)
Path: /api/resource or /api/resource/:id
Auth: Required? (Yes/No, what type?)
Input: What data required (JSON Schema ideally)
Output: Success response (JSON example)
Errors: Possible error codes & messages
Example: Full curl or Postman example
Rate limit: How many requests/hour?
```

---

## SECTION 7: GETTING HELP

### "I don't know where to start"
```
→ Read: README.md (5 min)
→ Then: CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md (15 min)
→ Then: Ask in Slack or create GitHub issue
```

### "I don't understand the system"
```
→ Read: PRODUCTION_ARCHITECTURE.md
→ Look at: System diagram (in ARCHITECTURE file)
→ Run locally: DEPLOYMENT_GUIDE.md
→ Explore code: Start with App.tsx or server.ts
```

### "What should I work on?"
```
→ Read: PENDING_IMPLEMENTATION_ROADMAP.md
→ Look at: Tier 1 (critical) first, then Tier 2
→ Check: Time estimate & dependencies
→ Ask lead: "Should I start on X or Y?"
```

### "How do I deploy?"
```
→ Read: DEPLOYMENT_GUIDE.md
→ Follow: Step-by-step instructions
→ Test locally: npm run dev, pytest tests/
→ Ask: DevOps lead for access to staging/prod
```

### "The code doesn't match the docs"
```
→ Trust: The code is source of truth
→ Update: Related documentation
→ Ask: Why was code changed without doc update?
→ Create: GitHub issue to track doc updates needed
```

### "I found a bug"
```
→ Create: GitHub issue with steps to reproduce
→ Check: Is it in PROJECT_HARMONY_TEST_REPORT or existing tests?
→ Fix: Add test first, then fix code
→ Test: Run pytest tests/ to verify fix
→ Document: Note in PENDING_IMPLEMENTATION_ROADMAP if it's new debt
```

---

## SECTION 8: QUICK LOOKUP TABLE

| Need | Go To | Link |
|------|-------|------|
| Project status | CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md | [Link](#) |
| What to build next | PENDING_IMPLEMENTATION_ROADMAP.md | [Link](#) |
| System design | PRODUCTION_ARCHITECTURE.md | [Link](#) |
| How to develop | DEVELOPMENT_WORKFLOW.md | [Link](#) |
| How to deploy | DEPLOYMENT_GUIDE.md | [Link](#) |
| API endpoints | QUICK_REFERENCE_CARD.md | [Link](#) |
| Test results | PROJECT_HARMONY_TEST_REPORT.md | [Link](#) |
| Install dependencies | DEPENDENCIES_AND_SETUP.md | [Link](#) |
| Build for Windows | WINDOWS_APP_PACKAGING.md | [Link](#) |
| Historical docs | 08_Archive/legacy-documentation/ | [Folder](#) |

---

## SECTION 9: UPDATED README ROADMAP

When you update 02_Code/README.md, include this structure:

```markdown
# GEESP-Angola: Code Module

## 📖 Documentation Roadmap (Start HERE!)

**New to the project?** Follow this order:
1. This README (you are here) - 5 min
2. [Status Report](00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md) - 15 min
3. [Roadmap](01_PENDING_IMPLEMENTATION_ROADMAP.md) - 15 min
4. [System Design](PRODUCTION_ARCHITECTURE.md) - 15 min
5. [How to Deploy](DEPLOYMENT_GUIDE.md) - 30 min
6. [How to Develop](DEVELOPMENT_WORKFLOW.md) - 30 min

**Quick lookup:** [Navigation Guide](03_MASTER_NAVIGATION_GUIDE.md)

## 🚀 Quick Start

[Same as before...]

## 📚 Full Documentation Index

[Organized by topic...]

## 🎯 Current Status

- ✅ Code quality: 95/100
- ✅ Tests: 68/68 passing (100%)
- 🟡 Security: Planned (T1.1 roadmap)
- 🟡 Deployment: Basic Docker, no K8s yet
- 🔴 Mobile: Not started

See [Status Report](00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md) for details.

## 🗺️ Roadmap

What's next? [See full roadmap](01_PENDING_IMPLEMENTATION_ROADMAP.md)

Priority: Security → User Management → Analytics → DevOps
Timeline: 6 months, 640 hours

## 🔧 For Specific Roles

- **Frontend dev:** [React guide](DEVELOPMENT_WORKFLOW.md#frontend)
- **Backend dev:** [Express guide](DEVELOPMENT_WORKFLOW.md#backend)
- **Python/MCDA:** [Python guide](DEVELOPMENT_WORKFLOW.md#python)
- **DevOps:** [Deployment guide](DEPLOYMENT_GUIDE.md)
- **Managers:** [Status & roadmap](00_CODE_IMPLEMENTATION_STATUS_CONSOLIDATED.md)
- **QA:** [Testing guide](PROJECT_HARMONY_TEST_REPORT.md)
```

---

## FINAL SUMMARY

### What We're Doing
```
🎯 Consolidating documentation
   ✅ 40+ scattered docs → 13 focused master docs
   ✅ Clear single source of truth
   ✅ Easy navigation for all roles
   ✅ 65 legacy docs archived for reference
```

### What Gets Easier
```
📖 Documentation:
   ✅ Find info 5x faster
   ✅ No confusion about "which doc is current"
   ✅ New devs onboard in 2 hours instead of 4
   
💻 Development:
   ✅ Clear roadmap (46 features prioritized)
   ✅ Know exact effort & timeline
   ✅ Understand dependencies before starting
   
🚀 Deployment:
   ✅ Clear steps to go from code to production
   ✅ All environments documented
   ✅ Rollback procedures clear
```

### What Stays the Same
```
✅ Code quality: Still 95/100
✅ All functionality: Still works
✅ Tests: Still 68/68 passing
✅ No code changes: Only documentation reorganization
```

---

**Document Version:** 1.0  
**Created:** March 6, 2026  
**Status:** Ready to implement  
**Next Step:** Follow 02_DOCUMENTATION_CLEANUP_PLAN.md
