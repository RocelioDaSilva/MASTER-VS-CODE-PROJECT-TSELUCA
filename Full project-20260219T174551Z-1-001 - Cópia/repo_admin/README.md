# repo_admin — Repository Governance & Utilities

Administrative tools and reports for managing this repository.

## Folder Contents

| Folder | What It Is |
|--------|-----------|
| `reports/` | Canonical status reports: health, consolidation summaries, analysis |
| `scripts/` | Python utilities for repo maintenance (audit, citation fixes, LaTeX fixes) |
| `maps/` | Folder rename maps and migration references |

## Key Documents

| Document | Purpose |
|----------|---------|
| [reports/CANONICAL_SOURCES.md](reports/CANONICAL_SOURCES.md) | **Where everything lives** — the single reference for file locations |
| [reports/REPOSITORY_HEALTH_STATUS.md](reports/REPOSITORY_HEALTH_STATUS.md) | Current repository quality metrics |
| [reports/CONSOLIDATION_COMPLETION_SUMMARY.md](reports/CONSOLIDATION_COMPLETION_SUMMARY.md) | Phase 7 consolidation status |
| [maps/FOLDER_RENAME_MAP.md](maps/FOLDER_RENAME_MAP.md) | Old path → new path migration table |

## Scripts

| Script | What It Does |
|--------|-------------|
| `scripts/repo_audit.py` | Scans repository for issues |
| `scripts/fix_citations.py` | Fixes citation formatting in LaTeX |
| `scripts/fix_latex_issues.py` | General LaTeX error corrections |
| `scripts/update_docs_consolidation.py` | Automates documentation updates |
| `scripts/update_health_status_phase7.py` | Updates health status report |

## Related

- **Code:** [../code_unified/](../code_unified/README.md)
- **Manuscript:** [../manuscript_unified/](../manuscript_unified/README.md)
- **Archive:** [../_old_information/](../_old_information/README.md)

For team guidance on finding files, start with [reports/CANONICAL_SOURCES.md](reports/CANONICAL_SOURCES.md).
