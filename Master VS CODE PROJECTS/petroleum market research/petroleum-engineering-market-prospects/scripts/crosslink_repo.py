"""
crosslink_repo.py
=================
Scans all .md files in the repository and inserts Obsidian-style
inline markdown links whenever a known entity (company, doc file, key term,
career path, skill module) is mentioned in plain text but NOT already linked.

Rules
-----
- Recursively processes .md files in docs/, data/company-directory/,
  isptec/guide/, isptec/curriculum/, isptec/tseluca/, and root .md files.
- Does NOT touch the 80K auto-generated files in data/processed/company_hierarchy/.
- A mention is linked only if it appears as plain text (not already inside []()
  or a heading # title of its own file).
- Each entity is linked at most once per section (## heading block) to avoid
  over-linking.
- Links use workspace-relative paths for Obsidian / GitHub rendering.
"""

import os
import re
import sys

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Directories to process (will recurse into subdirectories)
SCAN_DIRS = [
    os.path.join(REPO_ROOT, "docs"),
    os.path.join(REPO_ROOT, "data", "company-directory"),
    os.path.join(REPO_ROOT, "isptec", "guide"),
    os.path.join(REPO_ROOT, "isptec", "curriculum"),
    os.path.join(REPO_ROOT, "isptec", "tseluca"),
]
# Also process root-level .md files
SCAN_ROOT_MD = True

# Directories to NEVER touch
SKIP_DIRS = {
    "company_hierarchy",
    "company_hierarchy_originals",
    "backups",
    ".git",
    ".obsidian",
    "build",
    "_markdown_anpg-local-content-full-data",
    "node_modules",
    "__pycache__",
}

# ══════════════════════════════════════════════════════════════════════════════
# ENTITY REGISTRY
# Keys   = canonical display name (what appears in links)
# Values = relative path from repo root (the link target)
# ══════════════════════════════════════════════════════════════════════════════

# ── Company profiles (data/company-directory/*.md) ───────────────────────────
COMPANY_ENTITIES = {
    # Canonical name → (relative target path, list of aliases to match)
    "Baker Hughes":       ("data/company-directory/bakerhughes.md",
                           ["Baker Hughes", "BakerHughes", "Baker Petrolite"]),
    "Halliburton":        ("data/company-directory/halliburton.md",
                           ["Halliburton"]),
    "Oceaneering":        ("data/company-directory/oceaneering.md",
                           ["Oceaneering"]),
    "Saipem":             ("data/company-directory/saipem.md",
                           ["Saipem"]),
    "SBM Offshore":       ("data/company-directory/sbmoffshore.md",
                           ["SBM Offshore", "SBM"]),
    "SLB":                ("data/company-directory/slb.md",
                           ["SLB", "Schlumberger"]),
    "Sonangol":           ("data/company-directory/sonangol.md",
                           ["Sonangol", "SONILS", "SONADRILL", "Sonadrill"]),
    "Subsea 7":           ("data/company-directory/subsea7.md",
                           ["Subsea 7", "Subsea7"]),
    "TechnipFMC":         ("data/company-directory/technipfmc.md",
                           ["TechnipFMC", "Technip"]),
    "TotalEnergies":      ("data/company-directory/totalenergies.md",
                           ["TotalEnergies", "Total Energies"]),
    "Yinson":             ("data/company-directory/yinson.md",
                           ["Yinson"]),
    "Chevron":            ("data/company-directory/chevron.md",
                           ["Chevron", "CABGOC"]),
    "ExxonMobil":         ("data/company-directory/exxonmobil.md",
                           ["ExxonMobil", "Esso Exploration Angola"]),
    "Azule Energy":       ("data/company-directory/azule-energy.md",
                           ["Azule Energy", "Azule"]),
    "Eni":                ("data/company-directory/eni.md",
                           ["Eni Angola", "Eni "]),
    "Weatherford":        ("data/company-directory/weatherford.md",
                           ["Weatherford"]),
    "PAENAL":             ("data/company-directory/paenal.md",
                           ["PAENAL"]),
    "SONAMET":            ("data/company-directory/sonamet.md",
                           ["SONAMET", "Sonamet"]),
    "Petromar":           ("data/company-directory/petromar.md",
                           ["Petromar"]),
}

# ── Other well-known companies mentioned but without profile files ───────────
# We still link these to their first mention in the ecosystem doc
ECOSYSTEM_ENTITIES = {
    "McDermott":          ("docs/angola/angolan-offshore-companies.md",
                           ["McDermott"]),
    "MODEC":              ("docs/angola/angolan-offshore-companies.md",
                           ["MODEC"]),
    "Afentra":            ("docs/angola/angolan-offshore-companies.md",
                           ["Afentra"]),
    "NOV":                ("docs/angola/angolan-offshore-companies.md",
                           ["NOV ", "National Oilwell Varco"]),
    "Bourbon":            ("docs/angola/angolan-offshore-companies.md",
                           ["Bourbon"]),
}

# ── Doc files cross-references ───────────────────────────────────────────────
DOC_ENTITIES = {
    "glossary":                  ("docs/glossary.md",
                                  ["glossary"]),
    "career-climbing-strategy":  ("docs/career/career-climbing-strategy.md",
                                  ["career-climbing-strategy", "career climbing strategy"]),
    "application-guide":         ("docs/career/application-guide.md",
                                  ["application-guide", "application guide"]),
    "offshore-reality-check":    ("docs/career/offshore-reality-check.md",
                                  ["offshore-reality-check", "offshore reality check"]),
    "service-specializations":   ("docs/career/service-specializations.md",
                                  ["service-specializations", "service specializations",
                                   "services-by-niche", "services by niche"]),
    "producer-service-tree":     ("data/company-directory/producer-service-tree.md",
                                  ["producer-service-tree", "producer service tree"]),
    "angolan-offshore-companies": ("docs/angola/angolan-offshore-companies.md",
                                   ["angolan-offshore-companies", "angolan offshore companies"]),
    "anpg-company-service-categories": ("docs/angola/anpg-company-service-categories.md",
                                        ["anpg-company-service-categories",
                                         "ANPG service categories"]),
    "anpg-registration-verification":  ("docs/angola/anpg-registration-verification.md",
                                        ["anpg-registration-verification",
                                         "ANPG registration verification"]),
    "company-research-guide":    ("docs/career/company-research-guide.md",
                                  ["company-research-guide", "company research guide"]),
    "career-niches":             ("docs/career/career-niches.md",
                                  ["career-niches", "career niches"]),
}

# ── Career path guides ───────────────────────────────────────────────────────
CAREER_PATH_ENTITIES = {
    "career-paths-index":        ("docs/career-paths/00-career-paths-index.md",
                                  ["career-paths-index", "career paths index"]),
    "drilling-engineer-path":    ("docs/career-paths/01-drilling-engineer.md",
                                  ["drilling engineer career path",
                                   "drilling engineer path"]),
    "production-engineer-path":  ("docs/career-paths/02-production-engineer.md",
                                  ["production engineer career path",
                                   "production engineer path"]),
    "reservoir-engineer-path":   ("docs/career-paths/03-reservoir-engineer.md",
                                  ["reservoir engineer career path",
                                   "reservoir engineer path"]),
    "subsea-engineer-path":      ("docs/career-paths/04-subsea-engineer.md",
                                  ["subsea engineer career path",
                                   "subsea engineer path"]),
    "hse-safety-engineer-path":  ("docs/career-paths/05-hse-safety-engineer.md",
                                  ["HSE safety engineer career path",
                                   "HSE engineer path", "hse-safety-engineer"]),
    "completions-engineer-path": ("docs/career-paths/06-completions-engineer.md",
                                  ["completions engineer career path",
                                   "completions engineer path"]),
}

# ── Career deep-dive files ───────────────────────────────────────────────────
CAREER_ENTITIES = {
    "career-drilling":       ("docs/career-deep-dives/career_drilling_engineer.md",
                              ["career_drilling_engineer"]),
    "career-production":     ("docs/career-deep-dives/career_production_engineer.md",
                              ["career_production_engineer"]),
    "career-reservoir":      ("docs/career-deep-dives/career_reservoir_engineer.md",
                              ["career_reservoir_engineer"]),
    "career-subsea":         ("docs/career-deep-dives/career_subsea_engineer.md",
                              ["career_subsea_engineer"]),
    "career-completions":    ("docs/career-deep-dives/career_completions_engineer.md",
                              ["career_completions_engineer"]),
    "career-hse":            ("docs/career-deep-dives/career_hse_engineer.md",
                              ["career_hse_engineer"]),
    "career-learning-maps":  ("docs/career-deep-dives/career-learning-maps.md",
                              ["career-learning-maps", "career learning maps"]),
}

# ── Skills modules ───────────────────────────────────────────────────────────
SKILLS_ENTITIES = {
    "skills-index":             ("docs/skills/00-skills-index.md",
                                 ["skills-index", "skills index"]),
    "well-control":             ("docs/skills/01-well-control.md",
                                 ["well control", "well-control"]),
    "drilling-fundamentals":    ("docs/skills/02-drilling-fundamentals.md",
                                 ["drilling fundamentals", "drilling-fundamentals"]),
    "drilling-fluids":          ("docs/skills/03-drilling-fluids.md",
                                 ["drilling fluids", "drilling-fluids"]),
    "formation-evaluation":     ("docs/skills/04-formation-evaluation.md",
                                 ["formation evaluation", "formation-evaluation"]),
    "directional-drilling":     ("docs/skills/05-directional-drilling.md",
                                 ["directional drilling", "directional-drilling"]),
    "mwd-lwd-tools":            ("docs/skills/06-mwd-lwd-tools.md",
                                 ["MWD/LWD tools", "mwd-lwd-tools"]),
    "mudlogging":               ("docs/skills/07-mudlogging.md",
                                 ["mudlogging", "mud logging"]),
    "fpso-process-operations":  ("docs/skills/08-fpso-process-operations.md",
                                 ["FPSO process operations",
                                  "fpso-process-operations"]),
    "artificial-lift":          ("docs/skills/09-artificial-lift.md",
                                 ["artificial lift", "artificial-lift"]),
    "flow-assurance":           ("docs/skills/10-flow-assurance.md",
                                 ["flow assurance", "flow-assurance"]),
    "subsea-systems":           ("docs/skills/11-subsea-systems.md",
                                 ["subsea systems", "subsea-systems"]),
    "offshore-hse-safety":      ("docs/skills/12-offshore-hse-safety.md",
                                 ["offshore HSE safety", "offshore-hse-safety",
                                  "offshore HSE"]),
    "cementing-and-completions": ("docs/skills/13-cementing-and-completions.md",
                                  ["cementing and completions",
                                   "cementing-and-completions"]),
    "reservoir-engineering-skill": ("docs/skills/14-reservoir-engineering.md",
                                    ["reservoir engineering skill",
                                     "reservoir-engineering"]),
    "well-integrity":           ("docs/skills/15-well-integrity.md",
                                 ["well integrity", "well-integrity"]),
}

# ── ISPTEC Curriculum ─────────────────────────────────────────────────────────
ISPTEC_ENTITIES = {
    "curriculum-map":    ("isptec/curriculum/00_START_HERE_Curriculum_Map.md",
                          ["Curriculum Map", "START HERE Curriculum Map"]),
    "upstream-guide":    ("isptec/curriculum/02_Sector_Guides/01_UPSTREAM_Exploration_Production.md",
                          ["Upstream Exploration Production",
                           "upstream guide"]),
    "midstream-guide":   ("isptec/curriculum/02_Sector_Guides/02_MIDSTREAM_Transport_Storage.md",
                          ["Midstream Transport Storage",
                           "midstream guide"]),
    "downstream-guide":  ("isptec/curriculum/02_Sector_Guides/03_DOWNSTREAM_Refining_Marketing.md",
                          ["Downstream Refining Marketing",
                           "downstream guide"]),
}

# ── ISPTEC Offshore Guide files ───────────────────────────────────────────────
GUIDE_ENTITIES = {
    "guide-start":        ("isptec/guide/00_START_HERE.md",
                           ["Offshore Guide Start", "Guide Overview"]),
    "guide-market":       ("isptec/guide/01_Angola_Offshore_Market.md",
                           ["Angola Offshore Market"]),
    "guide-degree":       ("isptec/guide/02_Your_Degree_and_the_Market.md",
                           ["Degree and the Market"]),
    "guide-tracks":       ("isptec/guide/03_Six_Career_Tracks.md",
                           ["Six Career Tracks"]),
    "guide-companies":    ("isptec/guide/04_Companies_That_Hire.md",
                           ["Companies That Hire"]),
    "guide-certs":        ("isptec/guide/05_Certifications_Roadmap.md",
                           ["Certifications Roadmap"]),
    "guide-reality":      ("isptec/guide/06_Offshore_Reality.md",
                           ["Offshore Reality"]),
    "guide-plan":         ("isptec/guide/07_Five_Year_Action_Plan.md",
                           ["Five Year Action Plan", "Five-Year Action Plan"]),
    "guide-playbook":     ("isptec/guide/08_Application_Playbook.md",
                           ["Application Playbook"]),
}

# ── Key terms linked to glossary ─────────────────────────────────────────────
GLOSSARY_TERMS = {
    "BOSIET":   ("docs/glossary.md", ["BOSIET"]),
    "HUET":     ("docs/glossary.md", ["HUET"]),
    "IWCF":     ("docs/glossary.md", ["IWCF"]),
    "FPSO":     ("docs/glossary.md", ["FPSO"]),
    "SURF":     ("docs/glossary.md", ["SURF"]),
    "MWD":      ("docs/glossary.md", ["MWD"]),
    "LWD":      ("docs/glossary.md", ["LWD"]),
    "ROV":      ("docs/glossary.md", ["ROV"]),
    "BHA":      ("docs/glossary.md", ["BHA"]),
    "NDT":      ("docs/glossary.md", ["NDT"]),
    "EPC":      ("docs/glossary.md", ["EPC"]),
    "FEED":     ("docs/glossary.md", ["FEED"]),
    "IMR":      ("docs/glossary.md", ["IMR"]),
    "H2S":      ("docs/glossary.md", ["H2S"]),
}

# Merge all entities
ALL_ENTITIES = {}
for d in (COMPANY_ENTITIES, ECOSYSTEM_ENTITIES, DOC_ENTITIES, GLOSSARY_TERMS,
          CAREER_PATH_ENTITIES, CAREER_ENTITIES, SKILLS_ENTITIES, ISPTEC_ENTITIES,
          GUIDE_ENTITIES):
    ALL_ENTITIES.update(d)


def collect_files():
    """Collect all .md files to process, recursing into subdirectories."""
    files = []
    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue
        for root, dirs, fnames in os.walk(scan_dir):
            # Prune skip dirs
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in fnames:
                if fname.lower().endswith(".md"):
                    files.append(os.path.join(root, fname))
    if SCAN_ROOT_MD:
        for fname in os.listdir(REPO_ROOT):
            fp = os.path.join(REPO_ROOT, fname)
            if os.path.isfile(fp) and fname.lower().endswith(".md"):
                files.append(fp)
    return sorted(set(files))


def rel_path(from_file, to_target_repo_rel):
    """Compute a relative path from from_file's directory to the target."""
    from_dir = os.path.dirname(from_file)
    to_abs = os.path.join(REPO_ROOT, to_target_repo_rel)
    rel = os.path.relpath(to_abs, from_dir).replace("\\", "/")
    return rel


def is_inside_link(text, start, end):
    """Check if position start..end is already inside a markdown link [...](...) or heading."""
    # Check if inside [...]
    # Walk backwards from start looking for unmatched [
    depth = 0
    for i in range(start - 1, max(start - 300, -1), -1):
        if text[i] == ']':
            depth += 1
        elif text[i] == '[':
            if depth > 0:
                depth -= 1
            else:
                return True  # inside a link text
    # Check if inside (...)  after ]
    for i in range(start - 1, max(start - 300, -1), -1):
        if text[i] == '(':
            # Check if preceded by ]
            j = i - 1
            while j >= 0 and text[j] == ' ':
                j -= 1
            if j >= 0 and text[j] == ']':
                return True  # inside a link URL
            break
        elif text[i] in '\n\r':
            break
    return False


def is_in_heading(text, pos):
    """Check if position is in a markdown heading line."""
    line_start = text.rfind('\n', 0, pos) + 1
    line_text = text[line_start:pos]
    return line_text.lstrip().startswith('#')


def _build_fenced_code_ranges(text):
    """Find all (start, end) byte ranges of fenced code blocks (``` ... ```)."""
    ranges = []
    for m in re.finditer(r'^(`{3,}|~{3,})', text, re.MULTILINE):
        if not ranges or ranges[-1][1] is not None:
            ranges.append([m.start(), None])  # opening fence
        else:
            ranges[-1][1] = m.end()  # closing fence
    # If an unclosed fence remains, extend to end of text
    if ranges and ranges[-1][1] is None:
        ranges[-1][1] = len(text)
    return [(s, e) for s, e in ranges]


def is_in_fenced_code_block(pos, fenced_ranges):
    """Check if position falls inside any fenced code block."""
    for start, end in fenced_ranges:
        if start <= pos <= end:
            return True
        if start > pos:
            break
    return False


# Box-drawing characters used in directory trees
_TREE_CHARS = set('├└│─┌┐┘┤┬┴┼╔╗╚╝║═╠╣╦╩╬')


def is_in_tree_or_table_line(text, pos):
    """Check if position is on a line containing box-drawing characters (tree diagrams)."""
    line_start = text.rfind('\n', 0, pos) + 1
    line_end = text.find('\n', pos)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    return any(ch in _TREE_CHARS for ch in line)


def is_in_code_or_url(text, pos):
    """Check if position is inside backticks or a URL."""
    # Check backticks
    before = text[max(0, pos - 200):pos]
    backtick_count = before.count('`')
    if backtick_count % 2 == 1:
        return True  # inside inline code
    # Check if inside a URL (http...)
    line_start = text.rfind('\n', 0, pos) + 1
    line_end = text.find('\n', pos)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    col = pos - line_start
    # If 'http' appears before our position on the same segment, likely in URL
    url_match = re.search(r'https?://\S+', line)
    if url_match and url_match.start() <= col <= url_match.end():
        return True
    return False


def is_own_file(fpath, entity_target_repo_rel):
    """Check if this file IS the target file (don't self-link)."""
    file_repo_rel = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
    return file_repo_rel == entity_target_repo_rel


def process_file(fpath):
    """Process a single .md file: insert links for entity mentions."""
    # Detect encoding: try UTF-8 first, then Windows-1252, then latin-1
    file_encoding = "utf-8"
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            file_encoding = "cp1252"
            with open(fpath, "r", encoding="cp1252") as f:
                content = f.read()
        except UnicodeDecodeError:
            file_encoding = "latin-1"
            with open(fpath, "r", encoding="latin-1") as f:
                content = f.read()

    original = content
    linked_in_file = set()  # track which entities already linked

    # Pre-compute fenced code block ranges
    fenced_ranges = _build_fenced_code_ranges(content)

    # Process entities sorted by alias length descending (longer matches first)
    entity_items = []
    for canonical, (target, aliases) in ALL_ENTITIES.items():
        for alias in aliases:
            entity_items.append((alias, canonical, target))
    entity_items.sort(key=lambda x: -len(x[0]))

    for alias, canonical, target_repo_rel in entity_items:
        if is_own_file(fpath, target_repo_rel):
            continue

        # Build regex: match alias as a whole word, not inside []()
        # Use word boundaries but be careful with special chars
        escaped = re.escape(alias)
        # For aliases ending with space (like "Eni " or "NOV "), trim for the pattern
        if alias.endswith(" "):
            escaped_trimmed = re.escape(alias.rstrip())
            pattern = r'(?<!\[)' + escaped_trimmed + r'(?!\w)(?![^\[]*\])'
        else:
            pattern = r'(?<!\[)\b' + escaped + r'\b(?![^\[]*\])(?!\()'

        # Glossary acronyms must match case-sensitively
        is_acronym = canonical in GLOSSARY_TERMS
        re_flags = 0 if is_acronym else re.IGNORECASE

        linked_in_section = set()
        new_content = []
        current_section = 0
        last_end = 0

        for m in re.finditer(pattern, content, re_flags):
            start, end = m.start(), m.end()
            matched_text = m.group()

            # Skip if inside fenced code block or tree diagram line
            if is_in_fenced_code_block(start, fenced_ranges):
                continue
            if is_in_tree_or_table_line(content, start):
                continue
            # Skip if already linked, in heading, code, or URL
            if is_inside_link(content, start, end):
                continue
            if is_in_heading(content, start):
                continue
            if is_in_code_or_url(content, start):
                continue

            # Determine section number
            section_start = content.rfind('\n## ', 0, start)
            section_id = section_start if section_start >= 0 else 0

            # Only link once per section per entity
            key = (canonical, section_id)
            if key in linked_in_section:
                continue
            linked_in_section.add(key)

            # Build the link
            rel = rel_path(fpath, target_repo_rel)
            # URL-encode spaces in the path
            rel_encoded = rel.replace(" ", "%20")
            link = f"[{matched_text}]({rel_encoded})"

            new_content.append(content[last_end:start])
            new_content.append(link)
            last_end = end

        if new_content:
            new_content.append(content[last_end:])
            content = "".join(new_content)

    if content != original:
        with open(fpath, "w", encoding=file_encoding) as f:
            f.write(content)
        return True
    return False


def main():
    print(f"Repository root: {REPO_ROOT}")
    print(f"Entity registry: {len(ALL_ENTITIES)} entities with {sum(len(v[1]) for v in ALL_ENTITIES.values())} aliases\n")

    files = collect_files()
    print(f"Files to process: {len(files)}\n")

    modified = 0
    for fpath in files:
        fname = os.path.relpath(fpath, REPO_ROOT)
        result = process_file(fpath)
        if result:
            print(f"  [ok] {fname}")
            modified += 1
        else:
            print(f"    {fname} (no changes)")

    print(f"\nDone. Modified {modified}/{len(files)} files.")


if __name__ == "__main__":
    main()
