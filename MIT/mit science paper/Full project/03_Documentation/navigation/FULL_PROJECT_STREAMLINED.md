# GEESP-Angola – Streamlined Project Map

**Goal**: Reduce clutter and make it obvious where to look for what, **without touching your thesis or any `SOL.tex` files**.

---

## 🔝 The Only Folders You Really Need Day-to-Day

When you open `Full project/`, focus on these:

- **`03_Documentation/navigation/`** – Navigation & status (formerly ROOT_DOCS)
  - `README.md`: human-friendly “start here”
  - `MASTER_INDEX.md`: master index of everything
  - `PROJECT_FOLDER_GUIDE.md`: detailed explanation of all folders

- **`02_Code/geesp-angola/`** – **All code + app**
  - `geesp_unified_app.py`: main Streamlit app
  - `launch_app.bat` / `launch_app.sh` / `launch_app.py`: one-click launchers
  - `docs/CAPABILITIES.md`: all capabilities + user guide
  - `docs/IMPROVEMENTS.md`: roadmap & improvements

- **`01_Science/manuscript/`** – **Canonical thesis/paper**
  - `SOL.tex`: main manuscript (do not touch here as requested)
  - `SOL_SUBMISSION.tex`, `referencias.bib`, `figures/…`

- **`01_Science/presentations/`**
  - Slide deck and one-page summary for talks

- **`03_Documentation/technical/`**
  - Technical and project documentation (reports, resources, archive)

- **`06_Translations/translations/pt/`**
  - Portuguese versions of key documents (manuscript, coding guides, presentations, support)

- **`03_Documentation/project_management/`**
  - Status dashboards, audits, and checklists that are still active

Everything else (04_Operations, 05_Governance, 07_Data, 08_Archive) is **ops, governance, data, or archive** — use when needed.

---

## 📂 Folders You Can Treat as Archive / Backup

These exist mainly for history and safety. You can usually ignore them in daily work:

- **`08_Archive/archive/`**
  - Old manuscripts, logs, and historical backups (already separated).
  - SUBMISSION_READY, writing, and other backups live here when present.

- **`04_Operations/`** (scripts, infrastructure, kubernetes, ansible, monitoring)
  - DevOps / automation / infra helpers. Use when you’re doing deployment work, otherwise safe to ignore.

- **`.github/`, `.vscode/`**
  - Tooling and automation configs (CI, editor). Don’t affect your main flow.

All these remain intact; this file just marks them as **“archive / advanced”** so you don’t feel overwhelmed.

---

## 🖱️ How to Open the App From the Root

From `Full project/` you now have a **single icon/script**:

- **Windows**: double-click `run_geesp_app.bat`
  - This:
    - jumps into `02_Code/geesp-angola`
    - calls `launch_app.bat`
    - starts the unified Streamlit app

From the command line:

```bash
cd "Full project"
run_geesp_app.bat
```

Linux/macOS users can still run from inside `Coding parts/geesp-angola/` using `launch_app.sh`.

---

## 🧭 Mental Model (Super Simple)

Think of the project as **three big buckets**:

- **Science** → `01_Science/manuscript/` + `06_Translations/translations/pt/manuscript/`
- **Software** → `02_Code/geesp-angola/` (+ its own `docs/`)
- **Project framing** (audits, planning, governance, checklists) → `03_Documentation/` (navigation, technical, project_management, support)

Everything else is **ops (04), governance (05), data (07), or archive (08)**.

---

## ✅ What I Actually Changed to Streamline

- **Did not touch**:
  - Any `SOL.tex` file (in `manuscript/`, `translations/pt/manuscript/`, `SUBMISSION_READY/`, or `writing/`)
  - Any thesis LaTeX or figures
- **Added**:
  - `run_geesp_app.bat` at the root so you can open the app with one click from `Full project/`
  - This guide: `FULL_PROJECT_STREAMLINED.md` to clearly separate **active** vs **archive** areas
- **Reused existing organization**:
  - Kept `ROOT_DOCS/` as the top-level navigation hub
  - Left all management / audit files intact, just re-framed them as “project management” rather than things you must read every time

The result is a **thin, clear “spine”** through the project:

- Start at `03_Documentation/navigation/README.md` or root `README.md`
- For code/app: go to `02_Code/geesp-angola/`
- For thesis: go to `01_Science/manuscript/`
- For Portuguese: go to `06_Translations/translations/pt/`
- For everything else: only when needed.

