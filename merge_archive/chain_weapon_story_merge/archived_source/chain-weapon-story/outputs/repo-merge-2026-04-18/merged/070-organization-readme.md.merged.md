# Merged Artifact: organization-readme.md

This file preserves all source content exactly.

## Sources

- finished-manuscript/ORGANIZATION-README.md (sha256: 11df69fbaecef324f6876ace851117b7967746fe3e393256c7ec5b949fc4fa7e)
- finished-manuscript-reorg/original_copy/ORGANIZATION-README.md (sha256: 11df69fbaecef324f6876ace851117b7967746fe3e393256c7ec5b949fc4fa7e)

---

## Source: finished-manuscript/ORGANIZATION-README.md

Finished Manuscript — Organization Notes
=====================================

Purpose
-------
This file provides a small, non-destructive re-organization layer for the
`finished-manuscript/` folder. It does *not* move or delete your existing files
unless you explicitly approve physical reorganization. Instead it creates a
clear index and recommended next steps so you can read, edit, and rebuild with
minimal friction.

Quick navigation (what to open first)
-----------------------------------
- Combined review manuscript (readable): `../manuscript-review.md` (repo root)
- Source TeX entry: `manuscript.tex` and `manuscript-integrated-105.tex` in this
  folder.
- Per-chapter TeX (packaged): `cwbook_minimal_package/` (many `chapterNNN.tex` files).
- Scripts that build and manipulate files: `build_manuscript.py`,
  `build_manuscript_v3.py`, `rebuild_chapters.py` in this folder.
- Templates & archived templates: `archive_removed_by_copilot_2026-04-07/` and
  `stylish_book_template.tex` inside that archive.

What I added here
-----------------
- `ORGANIZATION-README.md` — this file.
- `INDEX.md` — a short, clickable list of the most important files and where to
  edit them. (See next file.)

How to rebuild the combined manuscript (local)
--------------------------------------------
From the repository root (where `BUILD-MANUSCRIPT-FOR-REVIEW.py` sits):

PowerShell
```
python BUILD-MANUSCRIPT-FOR-REVIEW.py
```

This regenerates `manuscript-review.md` and `manuscript-review.txt` in the
repo root.

To generate the LaTeX/PDF in `finished-manuscript/` (requires MiKTeX/XeLaTeX):

PowerShell
```
cd finished-manuscript
xelatex manuscript-integrated-105.tex
xelatex manuscript-integrated-105.tex
```

Notes & recommendations before moving files
-------------------------------------------
- Physical moves can break relative path references in build scripts (LaTeX
  inputs, image paths, python scripts). I will not move or delete anything
  without your explicit approval.
- Two safe options:
  1. Create an *index & organizational README* (this is what I have done).
  2. Create a *non-destructive reorganized copy* (duplicate key files into a
     clearer folder structure) so you can work there and confirm builds, then
     optionally swap or remove originals.
- If you want me to perform a full physical reorganization (move files into
  `src/`, `scripts/`, `docs/`, `templates/`, `archive/`), tell me which option
  you prefer (move vs copy) and I will implement it and update scripts.

Next steps you can ask me to perform now
----------------------------------------
1. Produce a per-chapter editing checklist for Act I (which chapters need
   rewrites, hooks fixed, show/tell conversion).
2. Create a reorganized copy of the folder structure (non-destructive).
3. Execute an approved physical reorganization (move files and update scripts).

If you'd like immediate reorganization, say whether you want files MOVED or
COPIED (safe). If you need me to continue, I will prepare the move/copy plan
and update the todo list accordingly.

— End of organization notes

---

## Source: finished-manuscript-reorg/original_copy/ORGANIZATION-README.md

Finished Manuscript — Organization Notes
=====================================

Purpose
-------
This file provides a small, non-destructive re-organization layer for the
`finished-manuscript/` folder. It does *not* move or delete your existing files
unless you explicitly approve physical reorganization. Instead it creates a
clear index and recommended next steps so you can read, edit, and rebuild with
minimal friction.

Quick navigation (what to open first)
-----------------------------------
- Combined review manuscript (readable): `../manuscript-review.md` (repo root)
- Source TeX entry: `manuscript.tex` and `manuscript-integrated-105.tex` in this
  folder.
- Per-chapter TeX (packaged): `cwbook_minimal_package/` (many `chapterNNN.tex` files).
- Scripts that build and manipulate files: `build_manuscript.py`,
  `build_manuscript_v3.py`, `rebuild_chapters.py` in this folder.
- Templates & archived templates: `archive_removed_by_copilot_2026-04-07/` and
  `stylish_book_template.tex` inside that archive.

What I added here
-----------------
- `ORGANIZATION-README.md` — this file.
- `INDEX.md` — a short, clickable list of the most important files and where to
  edit them. (See next file.)

How to rebuild the combined manuscript (local)
--------------------------------------------
From the repository root (where `BUILD-MANUSCRIPT-FOR-REVIEW.py` sits):

PowerShell
```
python BUILD-MANUSCRIPT-FOR-REVIEW.py
```

This regenerates `manuscript-review.md` and `manuscript-review.txt` in the
repo root.

To generate the LaTeX/PDF in `finished-manuscript/` (requires MiKTeX/XeLaTeX):

PowerShell
```
cd finished-manuscript
xelatex manuscript-integrated-105.tex
xelatex manuscript-integrated-105.tex
```

Notes & recommendations before moving files
-------------------------------------------
- Physical moves can break relative path references in build scripts (LaTeX
  inputs, image paths, python scripts). I will not move or delete anything
  without your explicit approval.
- Two safe options:
  1. Create an *index & organizational README* (this is what I have done).
  2. Create a *non-destructive reorganized copy* (duplicate key files into a
     clearer folder structure) so you can work there and confirm builds, then
     optionally swap or remove originals.
- If you want me to perform a full physical reorganization (move files into
  `src/`, `scripts/`, `docs/`, `templates/`, `archive/`), tell me which option
  you prefer (move vs copy) and I will implement it and update scripts.

Next steps you can ask me to perform now
----------------------------------------
1. Produce a per-chapter editing checklist for Act I (which chapters need
   rewrites, hooks fixed, show/tell conversion).
2. Create a reorganized copy of the folder structure (non-destructive).
3. Execute an approved physical reorganization (move files and update scripts).

If you'd like immediate reorganization, say whether you want files MOVED or
COPIED (safe). If you need me to continue, I will prepare the move/copy plan
and update the todo list accordingly.

— End of organization notes

---

