# Deep Repository-Wide Analysis

Date: 2026-04-17
Scope: MIT-SCIENCE-PAPER monorepo (manuscript, code, docs, operations, archive)

## Executive Summary

The repository is functional and heavily documented, but quality risk is concentrated in three areas:

1. Manuscript source-of-truth sprawl (many `SOL*.tex` variants).
2. Generated LaTeX build artifacts committed in working folders.
3. Historical path leakage and stale planning markers in technical documentation.

A citation-integrity check was run on the canonical manuscript and the active submission manuscript. One concrete citation-key mismatch was found and fixed.

## What Was Validated in This Deep Pass

- Citation integrity check (`.tex` cites vs `.bib` keys):
  - `MIT-SCIENCE-PAPER/Full project/Coding parts/SUBMISSION_READY/SOL.tex`
  - `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex`
- LaTeX artifact census across `MIT-SCIENCE-PAPER/**`.
- Marker/debt hotspot scan (`TODO/TBD/FIXME/DRAFT/PLACEHOLDER`) with manual filtering for false positives.
- Absolute-path residue scan (Windows user/OneDrive patterns).
- Manuscript variant enumeration (`SOL*.tex` spread).

## Implemented During This Pass

### 1) Fixed real citation-key mismatch in canonical manuscript

File changed:
- `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex`

Change:
- `\citep{Governo_Angola_2022}` -> `\citep{governo_angola_2022}`
- `\bibitem{Governo_Angola_2022}` -> `\bibitem{governo_angola_2022}`

Post-fix verification:
- Canonical manuscript cite-key audit now reports:
  - cites: 99
  - bib keys: 114
  - missing keys: 0
  - unused keys: 15

## Deep Findings (Prioritized)

### P1 - Source-of-truth ambiguity (high impact)

Observed:
- 14 `SOL*.tex` files distributed across manuscript, submission, translations, and archive trees.

Risk:
- Edits diverge, review comments land in the wrong file, and compilation outcomes are inconsistent.

Action:
- Declare one canonical manuscript source.
- Mark all non-canonical variants as archive/derived.
- Add a short `CANONICAL_SOURCES.md` at repo root with:
  - canonical `.tex`
  - canonical `.bib`
  - canonical figure source directory

### P1 - Build artifact noise still present (high impact, easy cleanup)

Observed:
- 72 LaTeX build artifacts currently present (counts from live scan):
  - `.log`: 30
  - `.aux`: 17
  - `.bbl`: 5
  - `.toc`: 5
  - `.out`: 4
  - `.fdb_latexmk`: 4
  - `.fls`: 3
  - `.blg`: 2
  - `.synctex.gz`: 2

Risk:
- Large noisy diffs, merge friction, accidental regression masking.

Action:
- Remove tracked artifacts in active (non-archive) trees.
- Keep archive snapshots only under `08_Archive` if historically required.

### P2 - Documentation debt markers are mostly historical/meta (medium)

Observed:
- Many `TODO/TBD/DRAFT` hits are in debt inventories and archive reports, not active runtime code.
- A few live planning docs still contain unresolved placeholders (for example in phase protocol/planning docs).

Risk:
- Execution status appears less complete than implementation reality.

Action:
- Separate "historical debt records" from "active open tasks".
- Keep one active tracker and freeze old tracker snapshots.

### P2 - Path leakage persists in inventory CSV metadata (medium)

Observed:
- Historical absolute paths (`C:\Users\...\OneDrive\...`) remain in inventory/debt CSV content.

Risk:
- Portability confusion and environment-specific references in docs.

Action:
- Keep immutable historical CSVs in archive.
- For active inventories, regenerate using repo-relative paths.

## Recommended Execution Order

1. Canonicalization pass (manuscript source-of-truth declaration).
2. Artifact cleanup pass (remove tracked LaTeX build files from active trees).
3. Active-tracker cleanup pass (resolve or close true open `TODO/TBD` items).
4. Inventory normalization pass (repo-relative path refresh for active catalogs).

## Success Criteria for Next Iteration

- Exactly one canonical manuscript path documented.
- Zero tracked LaTeX build artifacts outside `08_Archive`.
- Active tracker has no stale `TBD` entries without owner/date.
- Active inventory files contain only repo-relative paths.

## Notes

This analysis focuses on repository hygiene, reproducibility, and submission reliability, not on rewriting scientific claims. The implemented citation fix removes one real compile/citation integrity failure in the canonical manuscript workflow.
