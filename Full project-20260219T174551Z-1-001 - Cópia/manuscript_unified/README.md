# manuscript_unified — Scientific Paper & Bibliography

This is the **single source of truth** for the GEESP-Angola scientific manuscript.

## Canonical Files

| File | What It Is |
|------|-----------|
| `science_manuscript/manuscript/SOL.tex` | **THE manuscript** — edit this file |
| `science_manuscript/manuscript/referencias.bib` | Bibliography (99 citations) |
| `science_manuscript/manuscript/figures/` | Figure image files |
| `science_manuscript/manuscript/figs/` | Additional figure files |
| `submission_package/` | Pre-built submission copy (SOL.tex + referencias.bib + figuras/) |

## How To Work

1. **Edit:** `science_manuscript/manuscript/SOL.tex`
2. **Compile:** Run LaTeX from the `manuscript/` directory
3. **References:** Update `referencias.bib` for new citations
4. **Submit:** Regenerate `submission_package/` from canonical sources before submission

## Related

| What | Where |
|------|-------|
| Reports on the manuscript | [../manuscript_unified/reports/](reports/) |
| Application code | [../code_unified/](../code_unified/README.md) |
| Admin/governance | [../repo_admin/](../repo_admin/README.md) |
| Old manuscript variants | [../_old_information/manuscript_variants/](../_old_information/manuscript_variants/README.md) |
