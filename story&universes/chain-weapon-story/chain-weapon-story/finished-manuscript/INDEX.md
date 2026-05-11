Finished Manuscript — Quick Index
================================

Open these first:

- [manuscript.tex](manuscript.tex) — Primary LaTeX entry (root of typeset).
- [manuscript-integrated-105.tex](manuscript-integrated-105.tex) — Integrated
  compiled .tex used for the current build.
- [cwbook_minimal_package/](cwbook_minimal_package/) — Per-chapter `.tex` files
  that build into the book package.
- [final_product/](final_product/) — Final PDFs and exported artifacts (if
  present).
- [build_manuscript.py](build_manuscript.py) and
  [build_manuscript_v3.py](build_manuscript_v3.py) — Build helpers (Python).
- [convert_md_to_tex.py](convert_md_to_tex.py) — Markdown → LaTeX conversion.
- [archive_removed_by_copilot_2026-04-07/](archive_removed_by_copilot_2026-04-07/) —
  Templates and older variants (safe to inspect for styling choices).

Where the editable manuscript source lives
-----------------------------------------
The canonical chapter markdown sources are under the repository `manuscript/`
folder (not inside `finished-manuscript/`). Edit Markdown there and re-run the
build script to regenerate integrated files.

Safe next actions
-----------------
- If you want me to create a reorganized *copy* of this folder (safe, leaves
  originals intact), say "copy" and I will create `finished-manuscript-reorg/`
  with the cleaned layout.
- If you want files moved instead, say "move" and I will present the exact
  list of files I will move before changing anything.
