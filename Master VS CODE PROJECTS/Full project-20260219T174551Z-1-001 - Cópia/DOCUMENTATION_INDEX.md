# DOCUMENTATION INDEX — Complete File Map

**Last updated:** April 18, 2026

This file maps every important document in the repository to help you find what you need.

---

## Quick Navigation

| I need to... | Go to |
|-------------|-------|
| **Run the app** | `code_unified/app_codebase/START_HERE.md` |
| **Set up development** | `code_unified/app_codebase/DEVELOPER_QUICK_START.md` |
| **Edit the manuscript** | `manuscript_unified/science_manuscript/manuscript/SOL.tex` |
| **Find where files live** | `repo_admin/reports/CANONICAL_SOURCES.md` |
| **Check repo health** | `repo_admin/reports/REPOSITORY_HEALTH_STATUS.md` |
| **See old/archived content** | `_old_information/README.md` |

---

## Repository Structure

```
REPOSITORY ROOT
├── code_unified/                    ← ALL APPLICATION CODE
│   ├── app_codebase/
│   │   ├── geesp-angola/           ← Main app (FastAPI + Streamlit + React)
│   │   │   ├── backend/            ← Python backend (API, models, analysis)
│   │   │   ├── frontend/           ← TypeScript/React dashboard
│   │   │   ├── notebooks/          ← Jupyter analysis notebooks
│   │   │   ├── monitoring/         ← Prometheus/Grafana configs
│   │   │   ├── k8s/                ← Kubernetes manifests
│   │   │   ├── docs/               ← App-specific docs
│   │   │   └── tests/              ← Test suite
│   │   ├── docs/                   ← API examples, guides, error codes
│   │   └── ARCHIVE/                ← Frozen development phase reports
│   └── operations_devops/          ← Infrastructure-as-Code
│       ├── ansible/                ← Ansible playbooks
│       ├── kubernetes/             ← K8s deployment configs
│       ├── infrastructure/         ← Terraform/cloud setup
│       ├── monitoring/             ← Monitoring stack configs
│       └── scripts/                ← DevOps utility scripts
│
├── manuscript_unified/              ← ALL MANUSCRIPT CONTENT
│   ├── science_manuscript/
│   │   └── manuscript/
│   │       ├── SOL.tex             ← THE canonical manuscript
│   │       ├── referencias.bib     ← Bibliography (99 citations)
│   │       ├── figures/            ← Figure images
│   │       └── figs/               ← Additional figures
│   ├── submission_package/         ← Pre-built submission copy
│   └── reports/                    ← Manuscript improvement reports
│
├── repo_admin/                      ← REPOSITORY GOVERNANCE
│   ├── reports/                    ← Status reports & analysis
│   ├── scripts/                    ← Maintenance utilities
│   └── maps/                       ← Migration reference maps
│
├── _old_information/                ← ARCHIVED CONTENT (read-only)
│   ├── legacy_mit_science_paper/   ← Old project tree (docs, governance, etc.)
│   ├── manuscript_variants/        ← Non-canonical SOL.tex versions
│   ├── superseded_reports/         ← Old phase/consolidation/audit reports
│   └── google_ai_studio_app/      ← Archived prototype app
│
├── MIT-SCIENCE-PAPER/               ← DEPRECATED (scheduled for removal)
│   └── Full project/              ← Original project structure (legacy)
│
├── REPOSITORY_ORGANIZATION.md      ← How the repo is organized
└── DOCUMENTATION_INDEX.md          ← THIS FILE
```

---

## Documents by Category

### Getting Started (for new developers)
| Document | Location | Purpose |
|----------|----------|---------|
| START_HERE.md | `code_unified/app_codebase/` | First thing to read for the codebase |
| DEVELOPER_QUICK_START.md | `code_unified/app_codebase/` | Setup instructions |
| DEVELOPER_SETUP_GUIDE.md | `code_unified/app_codebase/geesp-angola/` | Detailed app setup |
| QUICK_REFERENCE.md | `code_unified/app_codebase/` | Common commands & shortcuts |

### Application Documentation (GEESP-Angola)
| Document | Location | Purpose |
|----------|----------|---------|
| README.md | `code_unified/app_codebase/geesp-angola/` | App overview & architecture |
| API_DOCUMENTATION.md | `code_unified/app_codebase/geesp-angola/` | REST API reference |
| ARCHITECTURE_GUIDE.md | `code_unified/app_codebase/geesp-angola/` | System architecture |
| CONTRIBUTING.md | `code_unified/app_codebase/geesp-angola/` | Contribution guidelines |
| CHANGELOG.md | `code_unified/app_codebase/geesp-angola/` | Version history |
| PROJECT_STATUS_DASHBOARD.md | `code_unified/app_codebase/geesp-angola/` | Current project status |

### Master Documentation (comprehensive guides)
| Document | Location | Purpose |
|----------|----------|---------|
| 01_MASTER_GETTING_STARTED.md | `code_unified/app_codebase/geesp-angola/` | Complete getting started guide |
| 02_MASTER_ARCHITECTURE.md | `code_unified/app_codebase/geesp-angola/` | Full architecture reference |
| 03_MASTER_IMPLEMENTATION.md | `code_unified/app_codebase/geesp-angola/` | Implementation details |
| 04_MASTER_PRODUCTION.md | `code_unified/app_codebase/geesp-angola/` | Production deployment guide |
| 05_MASTER_TESTING_QA.md | `code_unified/app_codebase/geesp-angola/` | Testing & QA procedures |
| 06_MASTER_DEVELOPMENT.md | `code_unified/app_codebase/geesp-angola/` | Development workflow |
| 07_MASTER_DASHBOARD.md | `code_unified/app_codebase/geesp-angola/` | Dashboard usage guide |
| 08_MASTER_ADVANCED.md | `code_unified/app_codebase/geesp-angola/` | Advanced features & config |

### Manuscript & Research
| Document | Location | Purpose |
|----------|----------|---------|
| SOL.tex | `manuscript_unified/science_manuscript/manuscript/` | The paper (LaTeX) |
| referencias.bib | `manuscript_unified/science_manuscript/manuscript/` | Bibliography |
| Various reports | `manuscript_unified/reports/` | Manuscript improvement analysis |

### Repository Governance
| Document | Location | Purpose |
|----------|----------|---------|
| CANONICAL_SOURCES.md | `repo_admin/reports/` | Where every canonical file lives |
| REPOSITORY_HEALTH_STATUS.md | `repo_admin/reports/` | Repo quality metrics |
| CONSOLIDATION_COMPLETION_SUMMARY.md | `repo_admin/reports/` | Phase 7 consolidation record |
| FOLDER_RENAME_MAP.md | `repo_admin/maps/` | Old → new path mappings |
