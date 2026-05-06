Finished Manuscript — Reorganized Copy (non-destructive)
=========================================================

This folder is a safe, non-destructive reorganized copy of `finished-manuscript/`.
It contains wrappers and a small script that duplicates the original folder into
`original_copy/` inside this directory so you can experiment without touching the
original files.

Layout
------
- `src/tex/` — LaTeX wrapper files that point at the originals in
  `finished-manuscript/`.
- `scripts/` — helper scripts (notably `copy_finished_manuscript.py`).
- `docs/` — reorganization plan and notes.
- `templates/` — (place to collect templates if you want a cleaned copy).
- `outputs/` — put rebuilt PDFs and exported artifacts here.
- `original_copy/` — created by the copy script; this will contain the full
  duplicated contents of `finished-manuscript/` when you run the script.

Quick usage
-----------
Open a terminal and run:

PowerShell
```
cd finished-manuscript-reorg\scripts
python copy_finished_manuscript.py
```

This will create `finished-manuscript-reorg/original_copy/` containing the full
copy of the original `finished-manuscript/` folder. Add `--force` to overwrite an
existing copy.

If you want me to perform the physical copy now, say "yes"; otherwise run the
script yourself.
