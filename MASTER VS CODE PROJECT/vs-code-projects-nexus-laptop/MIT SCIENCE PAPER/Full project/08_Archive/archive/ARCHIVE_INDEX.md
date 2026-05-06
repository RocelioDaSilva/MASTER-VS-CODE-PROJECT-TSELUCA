# GEESP-Angola – Archive Index (Read-Only Area)

**Purpose**: Central map of all **archive / backup / old** material in `Full project/`, so your active work stays clean and you always know where “old stuff” lives.

**Important**: This is an index only. Your science files and thesis (`SOL.tex` in all locations) remain **unchanged**.

---

## 🔝 Summary – Where Archives Live

- **`08_Archive/archive/`** (this folder) – Central archive snapshots and old versions
- `SUBMISSION_READY/` – Old submission bundle (if present; duplicate of `01_Science/manuscript/`)
- `writing/` – Draft / backup LaTeX and figures (if present)
- `03_Documentation/technical/archive/` – Old docs replaced by newer versions
- Older / backup variants **inside** other folders (e.g. `*.bak`, `*_OLD`, etc.)

Use this file as your **single reference** when you need to find or clean up older material.

---

## 📁 1. ARCHIVE/ (Central Archive)

Path: `Full project/08_Archive/archive/` (this folder)

Main subfolders:

- `BACKUP_SNAPSHOTS/`
  - PDF/TeX/log snapshots of earlier manuscript and output
  - Good for forensic history; not needed for daily work

- `OLD_VERSIONS/`
  - Older manuscript builds, logs and PDFs
  - Includes:
    - `papier.tex`, `papier.pdf`
    - `SOL_backup_*.tex` and related logs
    - Old figure TeX files and compiled PDFs

**Rule of thumb**:
- Treat everything under `ARCHIVE/` as **read-only history**.
- The **canonical thesis** is under `01_Science/manuscript/`, not here.

---

## 📁 2. SUBMISSION_READY/ (Legacy Submission Bundle)

Path: `Full project/08_Archive/archive/SUBMISSION_READY/` (if present)  *(if present in your tree)*

Content (typical):

- `SOL.tex`, `.aux`, `.bbl`, `.blg`, `.toc`
- `figuras/` – figure files for one particular submission snapshot

This folder is essentially a **frozen copy** of one submission state.  
Your **live / canonical** manuscript is:

- `manuscript/SOL.tex`
- `manuscript/SOL_SUBMISSION.tex`

Recommendation:
- Keep `SUBMISSION_READY/` as a **backup reference only**.
- When editing, always work from `manuscript/`, never from `SUBMISSION_READY/`.

---

## 📁 3. writing/ (Drafts & Scratch)

Path: `Full project/08_Archive/archive/writing/` (if present)

What typically lives here:

- Early manuscript experiments:
  - `papier.tex`, `SOLV2IMPROVBYPT.TEX`, etc.
- Backup LaTeX:
  - `SOL_backup_*.tex`
- Duplicate `referencias.bib`
- A `figuras/` subfolder with draft figures and temporary LaTeX

Interpretation:

- This is your **scratchpad + backup** for writing.
- The real, current narrative is in `01_Science/manuscript/`.

Recommendation:

- Mark this mentally as **archive**.
- Only open when you intentionally want to dig into old drafts.

---

## 📁 4. docs/archive/ (Old Documentation)

Path: `Full project/03_Documentation/technical/archive/`

Examples you may find there:

- `GEESP-COMPLETION-SUMMARY.md`
- `IMPROVEMENTS_SUMMARY_FEB8.md`
- `PLANO_EXECUCAO_72H.md`
- `README-COMPLETION.md`
- `REPRODUCIBILITY.md`

These were superseded by newer, more organized documents (e.g. in `ROOT_DOCS/`, `PROJECT_MANAGEMENT/`, and `Coding parts/geesp-angola/docs/`).

Use them only for:

- Historical reference
- Checking how a plan evolved

Not for:

- Current execution or decisions (use the newer docs instead).

---

## 📁 5. Other Archived / Old Files by Pattern

Across the tree you will see files that are clearly “old” by name. Common patterns:

- `*_OLD.*`, `*_backup_*`, `*.bak`
- Suffixes with dates (e.g. `_FEB8`, `_FEB9`, `_FEB11_2026`)

Examples:

- `PRESENTATION_DECK_OUTLINE.md.bak` in `presentations/`
- Older improvement summaries in `docs/archive/`
- Backup PDFs/logs in `ARCHIVE/OLD_VERSIONS/`

**Treatment**:

- Keep them for history.
- Don’t edit them; instead, edit the latest canonical version in its main folder.

---

## 🧭 How This Fits Your Day-to-Day Workflow

For **active work**, you only really need:

- Thesis / Paper: `01_Science/manuscript/`
- Code + App: `02_Code/geesp-angola/`
- High-level navigation & status: `03_Documentation/navigation/`
- Presentations: `01_Science/presentations/`
- Portuguese material: `06_Translations/translations/pt/`

Everything described in this `ARCHIVE_INDEX.md` can be considered **“cold storage”**:

- Safe to ignore most of the time
- Available if you ever need to go back and see what something looked like

---

## ✅ Guarantee About Your Thesis Files

As part of this archive organization:

- No `SOL.tex` file was moved, edited, or deleted:
  - `01_Science/manuscript/SOL.tex`
  - `06_Translations/translations/pt/manuscript/SOL.tex`
  - Any `SOL.tex` copies under `08_Archive/archive/` (SUBMISSION_READY, writing, etc.)
- All archive organization has been done **by index and documentation**, not by changing your LaTeX content.

If you ever decide later to physically move or delete archive material, this file gives you a clear map of **what is safe to touch** and what should remain untouched.

