# _old_information — Archived & Historical Content

**Purpose:** This folder preserves all legacy, superseded, and historical content from the repository reorganization. Nothing here is actively maintained — it exists purely as a reference archive.

**Created:** April 18, 2026 (Repository-wide cleanup & consolidation)

---

## What's Inside

| Folder | Contains | Why It's Here |
|--------|----------|---------------|
| `legacy_mit_science_paper/` | Full copy of the old MIT-SCIENCE-PAPER project tree (docs, governance, translations, data, coding parts) | The original project structure before consolidation into `code_unified/` and `manuscript_unified/` |
| `manuscript_variants/` | All non-canonical versions of SOL.tex (backups, experiments, old drafts, one-time scripts) | Only `manuscript_unified/science_manuscript/manuscript/SOL.tex` is canonical |
| `superseded_reports/` | Phase completion reports, consolidation reports, audit reports that are no longer current | Replaced by the 8 MASTER docs in `code_unified/app_codebase/geesp-angola/` |
| `google_ai_studio_app/` | Archived Google AI Studio prototype app (React/TypeScript) | Standalone prototype, not part of main GEESP-Angola codebase |

---

## Do NOT Edit Files Here

These files are **frozen references**. If you need information from them, copy the relevant parts to the active locations:

- **Active code:** `code_unified/app_codebase/geesp-angola/`
- **Active manuscript:** `manuscript_unified/science_manuscript/manuscript/SOL.tex`
- **Active reports:** `repo_admin/reports/`

---

## Folder Details

### `legacy_mit_science_paper/`
The original project used a numbered folder structure (`02_Code/`, `03_Documentation/`, etc.) under `MIT-SCIENCE-PAPER/Full project/`. All useful content was migrated:
- Code → `code_unified/app_codebase/geesp-angola/`
- Manuscript → `manuscript_unified/science_manuscript/`
- Operations → `code_unified/operations_devops/`

What remains here is the **documentation, governance, translations, and data** that were part of the old structure.

### `manuscript_variants/`
- `backups/` — Timestamped backup copies of SOL.tex
- `experimental/` — Modified versions (melhorado, SOLEX, submission)
- `old_manuscripts/` — The very first manuscript drafts (papier.tex, early SOL versions)
- `reference_docs/` — Academic source lists, enhancement guides used during writing

### `superseded_reports/`
- `phase_history/` — Phase B through F completion reports from code development
- `consolidation_history/` — Reports from the code consolidation process
- `audit_history/` — JSON audits and file inventories

### `google_ai_studio_app/`
A standalone React + TypeScript prototype for solar energy planning visualization. Built with Vite, uses Google AI Studio API. Not integrated with the main GEESP-Angola system.
