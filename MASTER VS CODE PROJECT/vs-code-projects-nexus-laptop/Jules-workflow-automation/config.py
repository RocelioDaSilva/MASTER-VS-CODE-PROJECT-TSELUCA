# config.py
import os

# --- Jules API Configuration ---
# Set these as environment variables before running: $env:JULES_API_KEY=...
JULES_API_KEY = os.environ.get("JULES_API_KEY")
if not JULES_API_KEY:
    raise ValueError("JULES_API_KEY environment variable is not set.")
API_BASE_URL = "https://jules.googleapis.com/v1alpha"

# --- GitHub Configuration ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")
GITHUB_OWNER = "RocelioDaSilva"
GITHUB_REPO = "THE-petrolumen"
JULES_SOURCE_FULL_NAME = f"sources/github/{GITHUB_OWNER}/{GITHUB_REPO}"
BASE_BRANCH = "main"

# --- Pipeline Tasks (7 sessions covering your brainstorm) ---
SEQUENTIAL_TASKS = [
    
    # 1. DevOps Foundation
    {
        "title": "1 - DevOps Foundation",
        "prompt": """
Set up the following for the PetroLúmen repository:
1. GitHub Actions workflow (.github/workflows/ci.yml) that runs linting (Black, Flake8) and tests for backend (pytest) and frontend (npm test).
2. Ensure pre-commit hooks are correctly configured: Python (Black, Flake8) and frontend (husky/lint-staged). Fix any hook failures.
3. Pin all Python dependencies in requirements.txt (exact versions) and npm packages in package.json (use exact versions).
4. Create a .github/dependabot.yml for automated dependency updates.
5. Run a security audit (pip-audit / npm audit) and fix any critical vulnerabilities. Create DEPENDENCY_AUDIT_REPORT.md with findings.
"""
    },
    
    # 2. Testing & Coverage Boost
    {
        "title": "2 - Testing & Coverage Boost",
        "prompt": """
Improve testing coverage for both backend and frontend:
1. Add missing unit tests in backend/tests/ to reach at least 80% coverage (focus on critical paths in gaia_genesis). Use pytest --cov.
2. Add frontend unit tests (Jest) for key utility functions and components.
3. Add a script in package.json and a Makefile or just-docs command to generate and view coverage reports.
4. Fix any failing tests.
"""
    },
    
    # 3. Documentation Drive
    {
        "title": "3 - Documentation Drive",
        "prompt": """
1. Create a docs/ directory at the root with an architecture overview (ARCHITECTURE.md) describing the system, data flow, and technology stack.
2. Update backend/README.md: add clear API versioning strategy, setup instructions, and link to architecture docs.
3. Add JSDoc comments to the most important frontend components (e.g., Button, Card, and any custom hooks). Add a short "Component Documentation" section in petrolumen/README.md.
4. Create a DEVELOPER_ONBOARDING.md at the root with step-by-step local setup, common commands, and development workflow.
"""
    },
    
    # 4. Security Hardening
    {
        "title": "4 - Security Hardening",
        "prompt": """
1. Strongly emphasize changing the SECRET_KEY in backend/README.md (make it a warning at the top).
2. Create or enhance SECURITY.md with best practices: API key management, data handling, dependency scanning, and reporting process.
3. Run a basic static analysis security tool (e.g., bandit for Python) and fix any high-severity findings.
4. Ensure no hardcoded secrets are left in the codebase (scan quickly). Add a pre-commit check for secrets if possible.
"""
    },
    
    # 5. Code Quality & Cleanup
    {
        "title": "5 - Code Quality & Cleanup",
        "prompt": """
1. Review the directory 'possible feature calculation/THE-petrolumen-cafa105c2124580e244b9abca798a163d4588449/'. Decide if it should be integrated or removed. If removed, delete it and update any references.
2. Identify and remove obvious code duplication (backend and frontend). Refactor duplicated logic into shared utilities.
3. Create a .github/CODEOWNERS file listing default owners (you can use a generic placeholder for now).
4. Ensure Black and Flake8 pass cleanly on all Python files; fix any warnings.
"""
    },
    
    # 6. Developer Experience & i18n
    {
        "title": "6 - Developer Experience & i18n",
        "prompt": """
1. Add a basic internationalization plan file (I18N_L10N_PLAN.md) outlining strategy, tools, and milestones.
2. Create a feature toggles placeholder: a simple config file (feature_flags.json) with a comment explaining its purpose, and a small utility to read it (both frontend and backend if needed).
3. Optimize build times: check Next.js and Python build scripts, add caching where easy. Document any improvements in the developer onboarding guide.
4. Ensure pre-built documentation generation commands are documented (e.g., 'make html' for Sphinx, Storybook for frontend) – but actual generation can be left as setup steps.
"""
    },
    
    # 7. Error Handling & Polish
    {
        "title": "7 - Error Handling & Polish",
        "prompt": """
1. Implement consistent error handling across backend API endpoints and frontend API calls. Use user-friendly error messages and proper HTTP status codes.
2. Introduce structured logging (JSON format) in the backend where feasible; keep existing print/logging if changes are too large.
3. Add basic accessibility (a11y) improvements to frontend: alt texts, ARIA labels, and keyboard navigation where missing.
4. Review any remaining items from the original brainstorm that are quick wins and safe to implement (e.g., pinning remaining dependencies, minor performance tweaks). Apply them.
"""
    }
]

# Optional final analysis (8th session). Remove or keep as you like.
FINAL_ANALYSIS_TASK = {
    "title": "Final Repo Review",
    "prompt": "Review all changes made in the previous sessions. Check for consistency, regressions, and any remaining gaps from the original brainstorm. Implement any final improvements you deem critical."
}

# API Headers
HEADERS = {
    "X-Goog-Api-Key": JULES_API_KEY,
    "Content-Type": "application/json"
}