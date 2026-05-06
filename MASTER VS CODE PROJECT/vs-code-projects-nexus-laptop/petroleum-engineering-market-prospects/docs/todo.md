# Things to do (prioritized)

## Completed

<details>
<summary>16 items completed (click to expand)</summary>

- [x] Improve `README.md` and add `SUMMARY.md` (orientation and reading plan).
- [x] Create `services-by-niche.md` — 1-page cheat-sheet mapping ANPG categories to target job titles and offshore exposure.
- [x] Create `[application-guide](career/application-guide.md).md` — required certifications ([BOSIET](glossary.md)/HUET, IWCF), CV tips, and how to apply for internships/graduate programs.
- [x] Add `companies-by-niche.md` — list of operators, Tier-1 service companies, and local Tier-3 providers per niche.
- [x] Add subniche content — detailed subfunctions and common entry-level tasks per niche. Covered in `offshore niches & subniches which of them lead to where.md` and `service-specializations.md`.
- [x] Build `company-directory/` with one-page profiles: head office, Angolan operations, typical roles, application links. (20 profiles created.)
- [x] Add `[glossary](glossary.md).md` for acronyms and common field terms (BHA, ROP, ECD, [FPSO](glossary.md), SURF, MWD/LWD).
- [x] Fill 80,924 company hierarchy `.md` files with structured BI reports, backlinks, and one-click research URLs.
- [x] Enrich 2,502 files for 45 major companies with verified real data (websites, emails, phones, addresses, LinkedIn).
- [x] Repository-wide cross-reference linking — every company and key term mention auto-linked to its profile or [glossary](glossary.md) entry.
- [x] Consolidate overlapping docs — merged 10 files into 4 master documents.
- [x] Merged `anpg company service categories.md` content into `glossary.md` § [ANPG Service Categories](angola/anpg-company-service-categories.md) (April 2026).
- [x] **Renamed files for clarity** — cleaner, shorter, URL-friendly filenames across `docs/` and `docs/skills/` (April 2026).
- [x] **Created 6 career path step-by-step guides** in `docs/career-paths/`: Drilling, Production, Reservoir, Subsea, HSE, Completions — each with phased milestones, books, certs, software, Angola context (April 2026).
- [x] **Created [career paths index](career-paths/00-career-paths-index.md)** with comparison tables, quick-pick guide, certification matrix, salary comparisons (April 2026).
- [x] **Updated README.md and SUMMARY.md** with career paths section, fixed all internal cross-references for renamed files (April 2026).
- [x] **Expanded `.gitignore`** — added LaTeX extras, editor/IDE, generated hierarchy dirs, news output, .env, venv (April 2026).
- [x] **Updated `requirements.txt`** — added feedparser, requests, python-dateutil for automation scripts (April 2026).
- [x] **Improved `run_pipeline.py`** — added logging module, elapsed timing, script existence validation (April 2026).
- [x] **Created `CONTRIBUTING.md`** — repo structure, pipeline usage, contribution guidelines (April 2026).
- [x] **Fixed `scan_repo.py`** — replaced bare `except` with `except OSError` (April 2026).
- [x] **Created 6 comprehensive career deep-dive files** in `docs/career-deep-dives/`: Drilling, Production, Reservoir, Subsea, HSE, Completions — each answering 26 detailed questions (salaries, interview Qs, books, software, companies, certifications ROI, day-1 action plans) (April 2026).
- [x] **Created news monitoring system** — `NEWS_MONITORING_SETUP.md`, `automation/fetch_alerts.py` (RSS fetcher with deduplication), `automation/run_daily.bat`, `alert_feeds.txt`, `.github/workflows/fetch_news.yml` (daily GitHub Actions) (April 2026).
- [x] **Angola-focused career deep-dives** — Added "Angola Market Context" sections to all 6 career deep-dive files (`docs/career-deep-dives/`) covering: Angola-specific employers by tier, block/[FPSO](glossary.md) mapping, Angola salary tables (Tier 3/2/1), local challenges, ANPG local content requirements (April 2026).
- [x] **Reweighted `[career-niches](career/career-niches.md).md`** — Angola Tier 3/2/1 salary table now leads (was USA-first), added Angola demand context to job growth outlook, expanded Angola-specific details for Completions, Reservoir Simulation, and Energy Transition niches (April 2026).
- [x] **Angola-ized `CONTRIBUTING.md`** — Added Angola-specific contribution guidelines: Tier system usage, ANPG context requirements, salary data format, deepwater focus, company profile update cadence (April 2026).
- [x] **Fixed broken skill file references** — `career_hse_engineer.md` → `12-offshore-hse-safety.md`, `career_subsea_engineer.md` → `11-subsea-systems.md` (April 2026).

</details>

## Future work

### P1 — High impact, directly helps job seekers
- [x] ~~Add company profiles for Chevron/CABGOC, ExxonMobil, Azule Energy, Eni, Weatherford, PAENAL, SONAMET, [Petromar](../data/company-directory/petromar.md)~~ — **Done.** All 8 profiles now exist in `data/company-directory/`.
- [ ] Add salary benchmarking data table (by role, tier, and year) with sources. *(Partially covered — each `docs/career-deep-dives/` deep-dive now includes Angola Tier 3/2/1 salary tables.)*

### P2 — Nice to have, improves repository quality
- [ ] Add Angolan university petroleum engineering program comparison (ISPTEC, UAN, UKB).
- [ ] Automate careers-page crawling for top 20 companies (Angola-specific openings).
- [ ] Add career paths for remaining niches: Petrophysicist, Geoscientist, LNG Engineer, Data Scientist, Project Manager, Local Content Consultant.
- [ ] Add interactive skills self-assessment checklist (track which skills you've studied).
- [ ] Add interview question banks per career path (drilling, production, reservoir, subsea). *(Partially covered — each `docs/career-deep-dives/` deep-dive includes 15 interview questions.)*
