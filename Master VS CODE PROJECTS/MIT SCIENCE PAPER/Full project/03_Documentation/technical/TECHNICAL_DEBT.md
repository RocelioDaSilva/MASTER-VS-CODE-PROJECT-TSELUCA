# Technical Debt & TODO Inventory

Generated: 2026-02-10

Summary
- Repository scan found ~200 markers (TODO/TBD/DRAFT/FIXME/INCOMPLETE) across code and documentation.
- This file captures high-level categories, top-priority items, and suggested next steps to convert markers into tracked tickets.

Top-priority technical debt (action first)
- Audit & close false-positives: files that declare "DRAFT/TBD" but have implemented code (e.g., dashboard, MCDA, LCOE).
  - Example: `Full project/translations/pt/docs/CHECKLIST_CONCLUSAO_PROJETO.md` — updated to reflect implemented dashboard.
- Create a single CSV export of all marker occurrences for triage.

High-level categories
- Documentation (SOP, QA Plan, Protocols): many items require human authoring and review.
- Deploy/Infra: DB production, VPN/security, field connectivity remain infra tasks.
- Code consistency: a few scripts had hard-coded values (fixed: `scripts/generate_maps_simple.py`).
- Tests & CI: add unit tests for MCDA and LCOE modules and simple CI checks for linting.

Suggested immediate actions (automatable)
1. Export full marker list to CSV for triage.
   - PowerShell (from workspace root):
     ```powershell
     Select-String -Path 'Full project\**\*.*' -Pattern 'TODO|TBD|DRAFT|FIXME|INCOMPLETE' -SimpleMatch |
       Select-Object Path,LineNumber,Line |
       Export-Csv -Path docs/technical_debt_matches.csv -NoTypeInformation -Encoding UTF8
     ```
2. Triage CSV into three priority bins: High (blocking/go-no-go), Medium (nice-to-have before pilot), Low (future improvements).
3. For High/Medium items, create tracked issues (GitHub) with owner and estimate.

Short-term roadmap (next 3 actions I can do now)
- Produce the full CSV export of marker occurrences and commit it to `docs/technical_debt_matches.csv`.
- Auto-generate a prioritized file-by-file TODO list (High/Medium/Low) from the CSV.
- Update any docs that are clearly outdated where code proves the feature exists (minor edits).

If you want, I will now run the repository search and generate `docs/technical_debt_matches.csv` and a prioritized TODO file.
