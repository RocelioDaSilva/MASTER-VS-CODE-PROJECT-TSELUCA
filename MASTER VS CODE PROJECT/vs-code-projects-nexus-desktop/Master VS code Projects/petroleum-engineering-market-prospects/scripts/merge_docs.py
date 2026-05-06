"""
merge_docs.py
=============
Performs 4 document merge operations to consolidate overlapping content:

Merge A: company-connection-climbing.md → career-climbing-strategy.md
  - Appends: Certifications Checklist, Networking Playbook, Pitfalls, One-page Summary
  - (Parts 1-2 of source are redundant with target)

Merge B: company-directory.md + companies-by-niche.md → companies-angolan-offshore-ecosystem.md
  - Appends: "Careers & quick apply notes" section from company-directory.md
  - companies-by-niche.md content is entirely subsumed

Merge C: offshore-work-lifestyle.md → offshore-reality-check.md + career-climbing-strategy.md
  - To offshore-reality-check.md: FPSO table, Active Drilling Rigs table, Company Desirability table
  - To career-climbing-strategy.md: 5-Year Progression, Knowledge Checklist, Capabilities Matrix, How to Set Yourself Apart

Merge D: 6 small niche files → service-specializations.md
  - Adds Quick Reference cheat sheet from services-by-niche.md at top
  - All 6 source files are subsets already covered

After running, deleted source files must be removed via git rm.
"""

import os
import re

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(REPO, "docs")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def append(path, extra):
    content = read(path)
    content = content.rstrip("\n") + "\n\n" + extra.lstrip("\n")
    write(path, content)


# ── Merge A: company-connection-climbing → career-climbing-strategy ──────────
def merge_a():
    source = read(os.path.join(DOCS, "company-connection-climbing.md"))

    # Extract Parts 3-6 (unique content)
    # Part 3 starts with "### 🛠️ Part 3:"
    m = re.search(r"(### 🛠️ Part 3:.*)", source, re.DOTALL)
    if not m:
        # Try without emoji
        m = re.search(r"(###.*Part 3:.*The Master Skills.*)", source, re.DOTALL)
    if not m:
        print("  ⚠ Could not find Part 3 in company-connection-climbing.md")
        return False

    unique = m.group(1).strip()

    # Prepend a merge header
    merged_section = """
---

## Appendix: Certifications, Networking & Pitfalls

> *Merged from company-connection-climbing.md — complementary tactics for the career climbing strategy above.*

""" + unique

    target = os.path.join(DOCS, "career-climbing-strategy.md")
    append(target, merged_section)
    print("  ✓ Merge A: Appended Certs/Networking/Pitfalls to career-climbing-strategy.md")
    return True


# ── Merge B: company-directory + companies-by-niche → ecosystem doc ──────────
def merge_b():
    source_cd = read(os.path.join(DOCS, "company-directory.md"))

    # Extract "Careers & quick apply notes" section
    m = re.search(r"(Careers & quick apply notes.*)", source_cd, re.DOTALL)
    if not m:
        print("  ⚠ Could not find 'Careers & quick apply notes' in company-directory.md")
        return False

    careers_section = m.group(1).strip()

    merged_section = """

---

## Appendix: Quick-Apply Career Links

> *Merged from company-directory.md — direct links and search keywords for each major employer.*

""" + careers_section

    target = os.path.join(DOCS, "companies-angolan-offshore-ecosystem.md")
    append(target, merged_section)
    print("  ✓ Merge B: Appended Careers & quick apply notes to ecosystem doc")
    return True


# ── Merge C: offshore-work-lifestyle → offshore-reality-check + career-climbing ─
def merge_c():
    source = read(os.path.join(DOCS, "offshore-work-lifestyle.md"))

    # === Part C1: Extract FPSO/Rig/Desirability tables → offshore-reality-check ===
    # These tables start after "### 0. Pre-Research" and end before "### Part 1:"
    m_tables = re.search(
        r"(\*\*a\) Major FPSOs & Work Environments.*?)(?=---\s*\n\s*### Part 1:|\n### Part 1:)",
        source, re.DOTALL
    )
    if not m_tables:
        # Try broader match
        m_tables = re.search(
            r"(\*\*a\) Major FPSOs.*?\*\*c\) Company Desirability.*?\n\n)",
            source, re.DOTALL
        )
    if not m_tables:
        print("  ⚠ Could not extract FPSO/Rig tables from offshore-work-lifestyle.md")
    else:
        tables = m_tables.group(1).strip()
        tables_section = """

---

## Appendix: Angola Offshore Assets & Company Rankings (2026)

> *Merged from offshore-work-lifestyle.md — reference tables for the Angolan deepwater battlefield.*

""" + tables

        target_orc = os.path.join(DOCS, "offshore-reality-check.md")
        append(target_orc, tables_section)
        print("  ✓ Merge C1: Appended FPSO/Rig/Desirability tables to offshore-reality-check.md")

    # === Part C2: Extract technical prep content → career-climbing-strategy ===
    # Starts at "### Part 1: The 5-Year Progression Timeline"
    m_career = re.search(r"(### Part 1: The 5-Year Progression Timeline.*)", source, re.DOTALL)
    if not m_career:
        # Try "Part 1:" without specific title
        m_career = re.search(r"(\*   \*\*Year 1:.*)", source, re.DOTALL)
    if not m_career:
        print("  ⚠ Could not extract career-dev content from offshore-work-lifestyle.md")
    else:
        career_content = m_career.group(1).strip()
        career_section = """

---

## Appendix: Drilling Engineer Progression & Technical Readiness

> *Merged from offshore-work-lifestyle.md — year-by-year technical milestones, knowledge checklists, and how to stand out.*

""" + career_content

        target_ccs = os.path.join(DOCS, "career-climbing-strategy.md")
        append(target_ccs, career_section)
        print("  ✓ Merge C2: Appended technical progression/checklist to career-climbing-strategy.md")

    return True


# ── Merge D: 6 small niche files → service-specializations ──────────────────
def merge_d():
    source_sbn = read(os.path.join(DOCS, "services-by-niche.md"))

    # Add the cheat sheet as a "Quick Reference" section at the top of service-specializations
    target_path = os.path.join(DOCS, "service-specializations.md")
    target = read(target_path)

    # Find the first heading line after the title
    # The file starts with "Service specializations — ANPG categories..."
    # Insert after the intro paragraph, before the first ## section
    quick_ref = """
---

## Quick Reference Cheat Sheet

> *Merged from services-by-niche.md — one-page lookup of ANPG categories to roles, employers, and prep actions.*

""" + source_sbn.strip() + "\n"

    # Insert before the first "## 1." section
    m = re.search(r"\n(---\s*\n\s*## 1\.)", target)
    if m:
        insert_pos = m.start()
        new_target = target[:insert_pos] + "\n" + quick_ref + "\n" + target[insert_pos:]
        write(target_path, new_target)
        print("  ✓ Merge D: Inserted Quick Reference cheat sheet into service-specializations.md")
    else:
        print("  ⚠ Could not find insertion point in service-specializations.md")
        return False

    return True


def main():
    print("=== Document Merge Operations ===\n")

    print("[A] Career strategy merge...")
    merge_a()

    print("[B] Company directory merge...")
    merge_b()

    print("[C] Offshore lifestyle merge...")
    merge_c()

    print("[D] Service/niche merge...")
    merge_d()

    print("\n=== Files to delete (via git rm) ===")
    to_delete = [
        "docs/company-connection-climbing.md",
        "docs/company-directory.md",
        "docs/companies-by-niche.md",
        "docs/offshore-work-lifestyle.md",
        "docs/services-by-niche.md",
        "docs/Roles per service.md",
        "docs/local content niches to check per category.md",
        "docs/offshore niches & subniches which of them lead to where.md",
        "docs/Services per petroleum niche.md",
        "docs/offshore services and subcategories.md",
    ]
    for f in to_delete:
        print(f"  - {f}")

    print("\nDone. Run: git rm <files> to remove source files.")


if __name__ == "__main__":
    main()
