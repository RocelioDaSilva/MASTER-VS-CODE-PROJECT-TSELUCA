"""Fix SUMMARY.md - apply all pending edits directly to disk."""
import pathlib
import sys

_warnings = 0

def safe_replace(content, old, new, label=""):
    """Replace old with new in content, warning if old is not found."""
    global _warnings
    if old not in content:
        print(f"  ⚠ SKIP (pattern not found): {label or old[:60]!r}")
        _warnings += 1
        return content
    return content.replace(old, new)

p = pathlib.Path('docs/SUMMARY.md')
content = p.read_text(encoding='utf-8')
original = content

# Fix 1: Phase 2 - remove duplicate item 5, change "2 files" to "1 file"
content = safe_replace(content, 
    '**Phase 2: Find Your Role (45 min, 2 files)**\n\n4. [service-specializations.md](service-specializations.md)',
    '**Phase 2: Find Your Role (45 min, 1 file)**\n\n4. [service-specializations.md](service-specializations.md)'
)
content = safe_replace(content, 
    '5. [anpg-company-service-categories.md](anpg-company-service-categories.md) \u2014 Ranked ANPG categories with analytical commentary on which actually lead to offshore rotations.\n\n',
    '\n'
)

# Fix 2: Renumber Phase 3 items (6->5, 7->6, 8->7)
content = safe_replace(content, 
    '6. [company-directory/](company-directory/)',
    '5. [company-directory/](../data/company-directory/)'
)
content = safe_replace(content, 
    '7. [company-directory/producer-service-tree.md](company-directory/producer-service-tree.md)',
    '6. [company-directory/producer-service-tree.md](../data/company-directory/producer-service-tree.md)'
)
content = safe_replace(content, 
    '8. [companies-angolan-offshore-ecosystem.md]',
    '7. [companies-angolan-offshore-ecosystem.md]'
)

# Fix 3: Renumber Phase 4 (9->8)
content = safe_replace(content, 
    '9. [career-climbing-strategy.md]',
    '8. [career-climbing-strategy.md]'
)

# Fix 4: Renumber Phase 5 (10->9, 11->10)
content = safe_replace(content, 
    '10. [application-guide.md]',
    '9. [application-guide.md]'
)
content = safe_replace(content, 
    '11. [glossary.md]',
    '10. [glossary.md]'
)

# Fix 5: Renumber Phase 6 (12->11)
content = safe_replace(content, 
    '12. [offshore-reality-check.md]',
    '11. [offshore-reality-check.md]'
)

# Fix 6: Quick Navigation - fix company-directory link
content = safe_replace(content, 
    '\u2192 Start with: [company-directory/](company-directory/) and',
    '\u2192 Start with: [company-directory/](../data/company-directory/) and'
)

# Fix 7: File Descriptions table - remove deleted file rows
deleted_rows = [
    '| [services-by-niche.md](services-by-niche.md) | Reference | Job seekers | 1-page cheat-sheet: ANPG \u2192 job titles \u2192 employers |\n',
    '| [companies-by-niche.md](companies-by-niche.md) | Directory | Job seekers | Employers by sector and specialization |\n',
    '| [company-connection-climbing.md](company-connection-climbing.md) | Strategy | Career planners | Alternative climbing tactics (reference) |\n',
    '| [offshore-work-lifestyle.md](offshore-work-lifestyle.md) | Reality | Lifestyle researchers | Raw field expectations (reference) |\n',
    '| [local content niches to check per category.md](local content niches to check per category.md) | Reference | Niche analysts | Local content service niches (reference) |\n',
    '| [Roles per service.md](Roles per service.md) | Job guide | Role researchers | Entry titles by service category (reference) |\n',
    '| [Services per petroleum niche](Services per petroleum niche) | Practical guide | Job searchers | Practical ANPG-to-service mapping (reference) |\n',
]
for row in deleted_rows:
    content = safe_replace(content, row, '')

# Fix table: update descriptions and links for remaining rows
content = safe_replace(content, 
    '| [anpg-company-service-categories.md](anpg-company-service-categories.md) |',
    '| [anpg-company-service-categories.md](anpg-company-service-categories.md) |'
)
content = safe_replace(content, 
    '| Career guide | Role searchers | Detailed ANPG-to-role mapping with salary ranges and timelines |',
    '| Career guide | Role searchers | Master niche guide: ANPG-to-role mapping with salary ranges and timelines |'
)
content = safe_replace(content, 
    '| [company-directory/](company-directory/) | Profiles',
    '| [company-directory/](../data/company-directory/) | Profiles'
)
content = safe_replace(content, 
    '| [company-directory/producer-service-tree.md](company-directory/producer-service-tree.md) |',
    '| [producer-service-tree.md](../data/company-directory/producer-service-tree.md) |'
)
content = safe_replace(content, 
    '| [companies-angolan-offshore-ecosystem.md](companies-angolan-offshore-ecosystem.md) | Deep analysis | Researchers | Comprehensive Tier 1\u20135 contractor structure (reference) |',
    '| [companies-angolan-offshore-ecosystem.md](companies-angolan-offshore-ecosystem.md) | Deep analysis | Researchers | Comprehensive Tier 1\u20135 contractor structure with quick-apply links |'
)

# Fix 8: Directory tree - replace entire block
old_tree = """```
repository-root/
\u251c\u2500\u2500 README.md (START HERE)
\u251c\u2500\u2500 SUMMARY.md (this file)
\u251c\u2500\u2500 glossary.md (bookmark this)
\u251c\u2500\u2500 application-guide.md (prepare to apply)
\u251c\u2500\u2500 career-climbing-strategy.md (plan your path)
\u251c\u2500\u2500 [offshore-reality-check](offshore-reality-check.md).md (reality check)
\u251c\u2500\u2500 [service-specializations](service-specializations.md).md (find your role)
\u251c\u2500\u2500 [services-by-niche](services-by-niche.md).md (quick reference)
\u251c\u2500\u2500 [companies-by-niche](companies-by-niche.md).md (find employers)
\u251c\u2500\u2500 [company-directory](company-directory.md)/ (employer profiles)
\u2502   \u251c\u2500\u2500 [producer-service-tree](../data/company-directory/producer-service-tree.md).md (who works for whom)
\u2502   \u251c\u2500\u2500 [totalenergies](../data/company-directory/totalenergies.md).md
\u2502   \u251c\u2500\u2500 [chevron](companies-angolan-offshore-ecosystem.md).md
\u2502   \u251c\u2500\u2500 [slb](../data/company-directory/slb.md).md
\u2502   \u251c\u2500\u2500 [halliburton](../data/company-directory/halliburton.md).md
\u2502   \u251c\u2500\u2500 ... (other companies)
\u2502
\u2514\u2500\u2500 [Reference files for deep research]
    \u251c\u2500\u2500 anpg-company-service-categories.md
    \u251c\u2500\u2500 companies-angolan-offshore-ecosystem.md
    \u251c\u2500\u2500 company-connection-climbing.md
    \u2514\u2500\u2500 ... (other reference files)
```"""

new_tree = """```
repository-root/
\u251c\u2500\u2500 README.md                          \u2190 START HERE
\u251c\u2500\u2500 docs/
\u2502   \u251c\u2500\u2500 SUMMARY.md                     \u2190 this file (reading guide)
\u2502   \u251c\u2500\u2500 glossary.md                    \u2190 bookmark this
\u2502   \u251c\u2500\u2500 anpg-company-service-categories.md
\u2502   \u251c\u2500\u2500 service-specializations.md     \u2190 master niche guide
\u2502   \u251c\u2500\u2500 companies-angolan-offshore-ecosystem.md
\u2502   \u251c\u2500\u2500 career-climbing-strategy.md    \u2190 central career plan
\u2502   \u251c\u2500\u2500 application-guide.md           \u2190 certifications, CV, how to apply
\u2502   \u251c\u2500\u2500 offshore-reality-check.md      \u2190 reality check
\u2502   \u251c\u2500\u2500 anpg-verify.md                 \u2190 ANPG data verification
\u2502   \u2514\u2500\u2500 todo-s.md                      \u2190 task tracking
\u251c\u2500\u2500 data/
\u2502   \u251c\u2500\u2500 company-directory/             \u2190 12 company profiles
\u2502   \u2502   \u251c\u2500\u2500 producer-service-tree.md   \u2190 operator \u2192 service provider mapping
\u2502   \u2502   \u251c\u2500\u2500 totalenergies.md, slb.md, halliburton.md, ...
\u2502   \u2502   \u2514\u2500\u2500 bakerhughes, oceaneering, saipem, sbmoffshore, sonangol, subsea7, technipfmc, yinson
\u2502   \u251c\u2500\u2500 processed/                     \u2190 80,924 company .md files by ANPG category
\u2502   \u2514\u2500\u2500 raw/                           \u2190 original ANPG data
\u251c\u2500\u2500 scripts/                           \u2190 Python automation scripts
\u2514\u2500\u2500 tex/                               \u2190 LaTeX source files
```"""

content = safe_replace(content, old_tree, new_tree)

# Fix 9: Getting Started - fix company-directory links
content = safe_replace(content, 
    '3. Find matching companies in [company-directory/](company-directory/) (20 min)',
    '3. Find matching companies in [company-directory/](../data/company-directory/) (20 min)'
)
content = safe_replace(content, 
    '7. Deep dive into [company-directory/](company-directory/) profiles',
    '7. Deep dive into [company-directory/](../data/company-directory/) profiles'
)

# Write back
p.write_text(content, encoding='utf-8')
new_lines = content.count('\n')
print(f'Done. {len(original)} -> {len(content)} chars, {new_lines} lines')
if _warnings:
    print(f'⚠ {_warnings} replacement(s) skipped — patterns not found (already applied or content changed)')
print('Still has services-by-niche:', 'services-by-niche' in content)
print('Still has companies-by-niche:', 'companies-by-niche' in content)
print('Still has company-connection-climbing:', 'company-connection-climbing' in content)
print('Has ../data/company-directory/:', '../data/company-directory/' in content)
if _warnings:
    sys.exit(1)
