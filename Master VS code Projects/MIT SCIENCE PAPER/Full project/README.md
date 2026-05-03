# GEESP-Angola – Root Project Overview

This is the **root entry point** for the entire project.  
All content is organized into **numbered top-level folders** for clear navigation.

---

## Folder layout (greater → specified)

| Folder | Purpose |
|--------|--------|
| **01_Science** | Thesis/manuscript and presentations |
| **02_Code** | Application code (GEESP-Angola app) |
| **03_Documentation** | Navigation, technical docs, project management, support |
| **04_Operations** | Scripts, infrastructure, Kubernetes, Ansible, monitoring |
| **05_Governance** | Compliance, submissions, funding, planning |
| **06_Translations** | Portuguese (and other) translations |
| **07_Data** | Data files |
| **08_Archive** | Archives and backups |

---

## Start here

- **Documentation index**: `03_Documentation/DOCS_INDEX.md` — one-page links to navigation, code docs, technical, support
- **Full structure**: `PROJECT_STRUCTURE_FINAL.md` | **Archive**: `08_Archive/archive/ARCHIVE_INDEX.md`

---

## Run the application

**Windows (one click):** double-click `run_geesp_app.bat`

**Or from the code folder:**
```bash
cd "02_Code/geesp-angola"
launch_app.bat           # Windows
./launch_app.sh          # Linux/macOS
python launch_app.py     # Cross-platform
```

Main app entry point: `02_Code/geesp-angola/geesp_unified_app.py`

---

## Main areas at a glance

- **Thesis / manuscript**: `01_Science/manuscript/`
- **Presentations**: `01_Science/presentations/`
- **Code & app**: `02_Code/geesp-angola/`
- **All documentation**: `03_Documentation/` (navigation, technical, project_management, support)
- **DevOps / ops**: `04_Operations/` (scripts, infrastructure, kubernetes, ansible, monitoring)
- **Governance**: `05_Governance/` (compliance, submissions, funding, planning)
- **Translations**: `06_Translations/translations/`
- **Data**: `07_Data/data/`
- **Archives**: `08_Archive/archive/`

For more detail, see `03_Documentation/navigation/MASTER_INDEX.md` and `PROJECT_STRUCTURE_FINAL.md`.
