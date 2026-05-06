# Technical Debt — Prioritized TODO

Generated: 2026-02-10

Purpose: short, actionable list to close blockers for Phase 1 Go/No-Go and prepare for Phase 2.

## High Priority (Blockers — fix before 15 Feb)
- IRB / Ethical approval: update approvals tracking and attach IRB submission files.
  - Location: Full project/translations/pt/docs/CHECKLIST_CONCLUSAO_PROJETO.md (1.3)
  - Owner: Rocélio — Estimate: 3d (follow-up + submission)
- MINEA institutional letter (government approval): ensure signed copy and update `submissions/MINEA_Support_Letter_FEB2026.md`.
  - Owner: Rocélio / Government liaison — Estimate: 2d
- Field technicians hiring (positions open): finalize recruitment and onboarding plans.
  - Location: translations/pt/docs/CHECKLIST_CONCLUSAO_PROJETO.md (1.16)
  - Owner: HR / Rocélio — Estimate: 5d
- VPN / Security for field access: infrastructure task to secure remote sites.
  - Location: ROOT_DOCS/ (see `CONSOLIDACAO_FINAL_MELHORIAS_FEB11_2026.md`) and infra notes.
  - Owner: Infra — Estimate: 4d
- Equipment procurement (piranometer, GPS, tablets): raise RFQ and confirm lead times.
  - Location: PROJECT_MANAGEMENT/STATUS/*
  - Owner: Logistics — Estimate: 7d
- Baseline Survey Protocol finalization (detailed days): complete `GANNT_MASTER_FEB2026.md` entry and `Baseline Survey Protocol` doc.
  - Owner: Field Eng — Estimate: 3d
- Database production / schema: finalize PostgreSQL schema and provisioning script.
  - Location: PROJECT_MANAGEMENT/CHECKLISTS and ROOT_DOCS references
  - Owner: DevOps/DBA — Estimate: 2-3d
- Manuscript final edits (SOL_SUBMISSION.tex & SOL.tex): resolved remaining reviewer comments and prepare submission.
  - Owner: Rocélio — Estimate: 2d

## Medium Priority (Resolve during Phase 2 prep)
- Update `EXECUTION_TRACKER_REALTIME_FEB9-12.md` (replace [TBD] notes with concrete actions). Owner: PM — 1d
- Audit: complete sensitivity narrative referenced in `AUDITS/COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md` (sensitivity table + narrative). Owner: Statistician — 2d
- Convert code TODO comments into GitHub issues or fix small items (`translations/pt/docs/ORGANIZACAO_CORRECOES_FEB9.md` lists many). Owner: Dev — 1-2d
- Docker image tests and AWS account setup (MISSING_ITEMS_COMPREHENSIVE_FEB9.md). Owner: DevOps — 2d
- Update `IMPLEMENTATION_SUMMARY_FEB11_2026.md` entries marked `⚠️ DRAFT` (local authority letters, website TBD). Owner: PM — 1d

## Low Priority (Nice-to-have / future)
- Polish translations & presentation TBD lines (presentations/*, translations/pt/README_TRANSLATIONS.md). Owner: Comms — 2d
- Add unit tests for `scripts/mcda_analysis.py` and `scripts/lcoe_calculator.py` and add basic CI linting. Owner: Dev — 3d
- Improve logging and error handling in scripts (examples flagged in `ORGANIZACAO_CORRECOES_FEB9.md`). Owner: Dev — 2d

## Suggested Next Steps (automatable)
1. Commit full `docs/technical_debt_matches.csv` (export of all grep matches) for triage (done partial; append remaining matches).
2. Create GitHub Issues for all High and Medium items with owner and estimate.
3. Triage Low items into a backlog milestone for Phase 2.

If you want, I will now append the remaining grep matches to `docs/technical_debt_matches.csv` (complete export) and create GitHub Issue templates for the High-priority items in `.github/ISSUE_TEMPLATE/`.
