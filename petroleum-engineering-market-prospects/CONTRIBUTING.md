# Contributing to Petroleum Engineering Market Prospects

Thank you for your interest in contributing! This repository is a comprehensive resource for petroleum engineering career planning with a focus on Angola's offshore industry.

---

## Repository Structure

```
├── data/                  # Company data & ANPG local content database
│   ├── raw/               # Original ANPG data (do not edit)
│   ├── processed/         # Generated hierarchy, CSV, scripts
│   └── company-directory/ # Curated company profiles (20+)
├── docs/                  # Career guides, glossary, strategy docs
│   ├── angola/            # Angola market & ANPG regulatory docs
│   ├── career/            # Career planning & application guides
│   ├── career-paths/      # Step-by-step career path guides (6 disciplines)
│   ├── career-deep-dives/           # Comprehensive career deep-dives (26 Q&A each)
│   ├── skills/            # Technical skill modules (15 modules)
│   └── learning-resources.md  # Central hub: courses, books, certifications, free software
├── isptec/                # ISPTEC student resources
│   ├── guide/             # Offshore career playbook (8 files)
│   ├── curriculum/        # ISPTEC subject files + sector guides
│   └── tseluca/           # Career accelerator: paths, skills, discipline, subjects
│       ├── paths/         # 6 career-path roadmaps
│       ├── skills/        # 13 skill tutorials with worked examples
│       ├── discipline/    # 6 discipline deep-dives
│       ├── subjects/      # 6 applied subject files
│       └── support/       # Certifications, employability intel, company targeting
├── scripts/               # ALL data processing & documentation scripts
├── automation/            # News monitoring, alerts & config
├── tex/                   # LaTeX source for PDF report
└── run_pipeline.py        # Unified pipeline orchestrator
```

## How to Run the Pipeline

```bash
# Install dependencies
pip install -r requirements.txt

# Run everything (data + docs pipelines)
python run_pipeline.py all

# Run only the data pipeline (hierarchy generation, company fills)
python run_pipeline.py data

# Run only the docs pipeline (merge, fix links, cross-link)
python run_pipeline.py docs

# Preview without executing
python run_pipeline.py --dry-run
```

## Contribution Guidelines

### Adding a New Company Profile

1. Create a new `.md` file in `data/company-directory/` using the company name (lowercase, no spaces): e.g., `newcompany.md`
2. Use the existing profiles (e.g., `slb.md`, `totalenergies.md`) as templates
3. Include: headquarters, Angola operations, typical roles, application links, local content status
4. Add the company to the entity registry in `scripts/crosslink_repo.py` so it gets auto-linked

### Adding a New Skill Module

1. Create a numbered file in `docs/skills/`: e.g., `17-new-skill.md`
2. Follow the format of existing modules (learning objectives, resources, Angola context)
3. Update `docs/skills/00-skills-index.md` with the new entry

### Adding a New Career Path

1. Create a new guide in `docs/career-paths/`: e.g., `07-new-path.md`
2. Follow the 4-phase structure (Year 0–1, 1–3, 3–5, 5–10+)
3. Include: books, certifications, software, salary expectations, Angola context
4. Update `docs/career-paths/00-career-paths-index.md`

### Adding or Editing Tseluca Content

The `isptec/tseluca/` folder is the career accelerator for ISPTEC students. When adding new files:

1. Follow the existing naming convention (`XX_Name.md`) and file structure
2. **Always link to [Learning Resources](docs/learning-resources.md) in the file footer** — this is the central hub for courses, books, and providers
3. Add skill-specific resource links (e.g., IWCF, PetroWiki, NEBOSH) where relevant
4. Update `isptec/tseluca/00_INDEX.md` if creating a new top-level section
5. Run `python run_pipeline.py docs` to regenerate cross-links

### Updating Learning Resources

The file `docs/learning-resources.md` is the central directory of all training resources. When updating:

1. Add new platforms, courses, or providers to the appropriate section
2. Verify all URLs are current (online platforms change frequently)
3. For Angola-based providers, include location, approximate cost, and certification body
4. Keep the skill-specific sections in sync with `docs/skills/` module numbers

### Editing Documentation

- Keep Obsidian-compatible markdown (no HTML unless essential)
- Use relative links between files
- Run `python run_pipeline.py docs` after edits to update cross-links
- Avoid editing files in `data/processed/company_hierarchy/` — these are auto-generated

### Code Style

- Python 3.10+ with type hints where practical
- Use `pathlib.Path` for file paths
- All scripts should be runnable standalone and via `run_pipeline.py`
- Use Windows extended path prefix (`\\?\`) when handling the 80K+ hierarchy files

## Angola-Specific Contribution Guidelines

This repository is **Angola-focused first**. All content should prioritize Angola's offshore petroleum sector with global context as secondary comparison.

### When Adding or Editing Content

- **Lead with Angola context** — mention Angola blocks, FPSOs, operators, and local companies before global comparisons
- **Use the Tier system** — reference Tier 3 (local companies like [SONILS](data/company-directory/sonangol.md), [Sonamet](data/company-directory/sonamet.md), PAENAL), Tier 2 (service companies like [SLB](data/company-directory/slb.md), [Halliburton](data/company-directory/halliburton.md)), and Tier 1 (operators like [TotalEnergies](data/company-directory/totalenergies.md), Chevron, Azule Energy)
- **Include ANPG context** — reference local content law (Lei do Conteúdo Local, Law 14/23), ANPG registration requirements, and workforce nationalization targets where relevant
- **Salary data** — always include Angola salary ranges in the Tier 3/2/1 format; global comparisons are welcome but secondary
- **Rotation patterns** — Angola standard is 28/28 (28 days on, 28 days off). Mention when different.
- **Deepwater focus** — Angola's production is >90% deepwater [FPSO](docs/glossary.md)-based. Content should reflect this reality.

### Updating Company Profiles

- Update when new ANPG registration data is published (check [ANPG portal](https://www.angolapetroleo.gov.ao/))
- Update career portal links annually (these change frequently)
- Note when companies win or lose Angola contracts (adds timeliness)

### Updating the News Monitoring System

- Add new RSS feeds to `automation/alert_feeds.txt` when new Angola oil & gas news sources become available
- Add local Angolan job boards to the monitoring when they launch RSS feeds
- Check `automation/fetch_alerts.py` for any needed feed format changes

## Reporting Issues

Open a GitHub issue with:
- What you expected vs. what happened
- Which file(s) are affected
- Steps to reproduce (if applicable)

## License

By contributing, you agree that your contributions will be licensed under the same terms as this project.
