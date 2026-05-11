Reorganization plan (non-destructive copy)
===========================================

Goal
----
Create a clear, maintainable layout for the typesetting sources and build
artifacts while keeping the original folder intact until you're ready to adopt
the new structure.

Proposed layout in this copy
---------------------------
- `src/tex/` — LaTeX entry files and local adjusts (wrappers provided).
- `src/packages/` — per-chapter `.tex` packages (copy here if you want a local
  working set).
- `scripts/` — build and helper scripts; includes `copy_finished_manuscript.py`.
- `templates/` — templates and styles to keep separate from outputs.
- `outputs/` — compiled PDFs and exported assets for this reorg.
- `original_copy/` — full copy of the original `finished-manuscript/` (created
  by the script).

Next steps (safe)
-----------------
1. Run `scripts/copy_finished_manuscript.py` to create `original_copy/`.
2. Inspect `original_copy/` and, if it builds cleanly, move selected files into
   `src/tex/`, `templates/`, or `scripts/` in this reorg copy.
3. Update relative paths in local copies (images, inputs) and test a LaTeX
   compile from `src/tex/`.

If you want me to complete the full physical move (replace originals), say
"promote" and I will present a precise move plan and update the build scripts
before making any changes.
