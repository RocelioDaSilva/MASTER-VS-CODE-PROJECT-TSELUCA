# GEESP-Angola – Project Structure (Greater + Specified Folders)

**Last updated**: 2026-02-10  
**Layout**: Numbered top-level folders for clear separation.

---

## Root level

```
Full project/
├── README.md                    # Main entry (this structure)
├── run_geesp_app.bat           # One-click app launcher
├── PROJECT_STRUCTURE_FINAL.md  # This file
│
├── 01_Science/                  # Thesis + presentations
├── 02_Code/                     # Application code
├── 03_Documentation/            # All documentation
├── 04_Operations/               # DevOps & infrastructure
├── 05_Governance/               # Compliance, submissions, funding
├── 06_Translations/             # Translations
├── 07_Data/                     # Data files
├── 08_Archive/                  # Archives & backups
│
├── .github/                     # GitHub automation
└── .vscode/                     # Editor config
```

---

## 01_Science

Thesis/manuscript and presentation materials.

```
01_Science/
├── manuscript/                  # Canonical thesis/paper
│   ├── SOL.tex                  # Main manuscript (do not modify)
│   ├── SOL_SUBMISSION.tex
│   ├── referencias.bib
│   └── figures/
└── presentations/
    ├── deck/                    # Slide deck (e.g. 7 slides)
    └── one-page/               # One-page summary
```

---

## 02_Code

All application code and the main GEESP-Angola app.

```
02_Code/
└── geesp-angola/                # Main application
    ├── geesp_unified_app.py     # Streamlit app entry
    ├── launch_app.bat / .sh / .py
    ├── README.md
    ├── docs/
    │   ├── CAPABILITIES.md
    │   └── IMPROVEMENTS.md
    ├── scripts/                 # Core Python modules
    ├── utils/
    ├── dashboard/
    ├── monitoring/
    ├── models/
    ├── tests/
    └── data/
```

---

## 03_Documentation

Navigation, technical docs, project management, and support.

```
03_Documentation/
├── navigation/                  # Former ROOT_DOCS
│   ├── README.md
│   ├── MASTER_INDEX.md
│   ├── PROJECT_FOLDER_GUIDE.md
│   └── FULL_PROJECT_STREAMLINED.md
├── technical/                   # Former docs/
│   ├── reports/                 # Audits, phases, analysis
│   ├── resources/               # Checklists, capacity, references
│   └── archive/
├── project_management/          # Former PROJECT_MANAGEMENT
│   ├── STATUS/
│   ├── CHECKLISTS/
│   ├── AUDITS/
│   └── [Gantt, risk matrix, etc.]
└── support/                     # Former support/
    ├── FAQ_GEESP.md
    ├── DEMO_SCRIPT.md
    ├── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md
    └── [other support files]
```

---

## 04_Operations

Scripts, infrastructure, Kubernetes, Ansible, and monitoring.

```
04_Operations/
├── scripts/                     # DB, cron, utilities
├── infrastructure/              # Terraform, CloudFormation
├── kubernetes/                  # Former k8s/
├── ansible/
└── monitoring/                  # Prometheus, Grafana, alerts
```

---

## 05_Governance

Compliance, submissions, funding, and planning.

```
05_Governance/
├── compliance/                  # Former GOVERNANCE_COMPLIANCE
├── submissions/
├── funding/
└── planning/
```

---

## 06_Translations

All translation assets (e.g. Portuguese).

```
06_Translations/
└── translations/
    └── pt/
        ├── manuscript/
        ├── coding/
        ├── docs/
        ├── presentations/
        └── support/
```

---

## 07_Data

Project data files.

```
07_Data/
└── data/
```

---

## 08_Archive

Archives and backups.

```
08_Archive/
└── archive/
    ├── ARCHIVE_INDEX.md
    ├── REORGANIZATION_COMPLETE.md
    └── [other archived content]
```

---

## Quick navigation

| Goal | Path |
|------|------|
| Run app | `run_geesp_app.bat` or `02_Code/geesp-angola/launch_app.bat` |
| Thesis | `01_Science/manuscript/SOL.tex` |
| Presentations | `01_Science/presentations/` |
| Code & app | `02_Code/geesp-angola/` |
| Start / index | `03_Documentation/navigation/README.md` |
| Technical docs | `03_Documentation/technical/` |
| Project status | `03_Documentation/project_management/` |
| Support / FAQ | `03_Documentation/support/` |
| Ops / DevOps | `04_Operations/` |
| Governance | `05_Governance/` |
| Portuguese | `06_Translations/translations/pt/` |
| Archives | `08_Archive/archive/ARCHIVE_INDEX.md` |

---

**Reorganization script & log**: `08_Archive/archive/apply_new_structure.py`, `08_Archive/archive/STRUCTURE_CHANGE_LOG.txt`

*Structure applied: 2026-02-10*
