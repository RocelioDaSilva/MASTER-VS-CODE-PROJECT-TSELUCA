# Repository Organization

**Last updated:** April 18, 2026

---

## Top-Level Structure

| Folder | Purpose | Status |
|--------|---------|--------|
| `code_unified/` | All application code (GEESP-Angola app + DevOps infrastructure) | **ACTIVE** — edit here |
| `manuscript_unified/` | Scientific paper (SOL.tex), bibliography, figures, submission package | **ACTIVE** — edit here |
| `repo_admin/` | Repository governance: reports, scripts, migration maps | **ACTIVE** — admin use |
| `_old_information/` | Archived legacy content, old manuscript variants, superseded reports | **READ-ONLY** — reference only |
| `MIT-SCIENCE-PAPER/` | Original project tree (deprecated) | **DEPRECATED** — will be removed |

## Rules

1. **Only edit files in `code_unified/` and `manuscript_unified/`** — these are the canonical sources
2. **Never edit files in `_old_information/`** — they are frozen archives
3. **The `MIT-SCIENCE-PAPER/` folder is deprecated** — everything useful has been moved out

## What Happened (Consolidation History)

- **Phase 7 (April 2026):** Code and manuscript unified from the scattered MIT-SCIENCE-PAPER tree into `code_unified/` and `manuscript_unified/`
- **Phase 8 (April 2026):** Repository-wide cleanup — duplicates merged, naming standardized, `_old_information/` archive created
- All old phase reports, audit reports, and manuscript variants preserved in `_old_information/`

## See Also

- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) — Complete map of every document in the repo
- [repo_admin/reports/CANONICAL_SOURCES.md](repo_admin/reports/CANONICAL_SOURCES.md) — Where canonical files live
