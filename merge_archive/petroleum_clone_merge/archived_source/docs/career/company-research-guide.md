# Company Research Guide

**Two-Tier Company Database Structure**

This repository maintains two complementary company databases to serve different research needs:

---

## Tier 1: Hand-Curated Major Companies (21 profiles)

**Location:** `data/company-directory/`

**Purpose:** In-depth, manually researched profiles of the largest and most strategically important employers in Angola's oil & gas sector.

**Coverage:** International operators, Tier-1 multinational service companies, and key Angolan state entities.

**Profiles Include:**
- Official websites and Angola-specific career pages
- Verified contact information (HR email, phone, address)
- LinkedIn presence
- Typical entry-level roles and career progression
- [Service specializations](service-specializations.md) and tech focus
- Application procedures and hiring timelines

**Companies Covered:**
- **Operators:** [TotalEnergies](../../data/company-directory/totalenergies.md), Chevron, ExxonMobil, Azule Energy, Eni, Sonangol
- **Tier-1 Service:** [SLB](../../data/company-directory/slb.md), [Halliburton](../../data/company-directory/halliburton.md), [Baker Hughes](../../data/company-directory/bakerhughes.md), TechnipFMC, Subsea7, SBM Offshore, Yinson, Oceaneering, Saipem, Weatherford
- **Tier-1 Local:** [PAENAL](../../data/company-directory/paenal.md), [SONAMET](../../data/company-directory/sonamet.md), [Petromar](../../data/company-directory/petromar.md)
- **Analysis:** Producer-Service Tree (who works for whom?)

**When to Use Tier 1:**
- Research top employers before applying
- Understand salary expectations and career paths
- Find verified contact details for cold outreach
- Build "padrinho" (mentor) networking strategy
- Compare company cultures and growth opportunities

**Files:**
- `data/company-directory/totalenergies.md`
- `data/company-directory/slb.md` ([SLB](../../data/company-directory/slb.md))
- `data/company-directory/halliburton.md`
- `data/company-directory/bakerhughes.md`
- `data/company-directory/[chevron](../../data/company-directory/chevron.md).md`
- `data/company-directory/[exxonmobil](../../data/company-directory/exxonmobil.md).md`
- ... (20 total under `data/company-directory/`)

---

## Tier 2: Full Hierarchy Canonical Profiles (3,005 unique NIFs)

**Location:** `data/processed/company_hierarchy/_Profiles/`

**Purpose:** Comprehensive database of ALL companies registered with ANPG (Agência Nacional da Petróleo, Gás e Biocombustíveis).

**Coverage:** SCA (Sociedade Comercial Angolana), LDA, SA, and international subsidiaries across all 20 [ANPG service categories](../angola/anpg-company-service-categories.md).

**Profiles Include:**
- Company name and NIF (unique identifier)
- ANPG status: "Preferência" or "Exclusividade"
- Service categories and niches they're registered for (often 10–100+ per company)
- Quick-reference search links (Google, LinkedIn, ANPG registry)
- Template for adding verified company info

**Structure:**
- One canonical profile per unique NIF
- Organized by service category / niche in folder tree for context
- Stub files in each niche folder with wiki-link to canonical (Obsidian compatibility)

**When to Use Tier 2:**
- Find ALL companies in a specific niche (e.g., "Perfuração / Limpeza de Formação")
- Understand market concentration (how many suppliers per niche)
- Cold-prospect smaller service providers
- Map the full supply chain for a service category
- Export data to CSV/Excel for analysis
- Identify "Preferência" vs. "Exclusividade" suppliers

**Statistical Summary:**
- Total companies: 3,005 unique NIFs
- Service categories: 20 (drilling, completions, subsea, operations, etc.)
- Niches: 800+ subspecialties
- Local supplier ratio: ~70% Angolan-registered
- Major international players: embedded in full hierarchy + Tier 1 profiles

**Files Location:**
- Canonical profiles: `data/processed/company_hierarchy/_Profiles/CompanyName_NIF.md` (3,005 files)
- Stub references: Throughout `data/processed/company_hierarchy/[1-20].**/` folders

---

## How to Use Both Tiers Together

### Scenario 1: "I want to work at a Tier-1 international service company"
1. Start in **Tier 1:** Browse `data/company-directory/` for SLB, Halliburton, [Baker Hughes](../../data/company-directory/bakerhughes.md) profiles
2. Research verified contact info and application procedures
3. Optional: Use **Tier 2** to see what niches they specialize in (cross-check with `_Profiles/`)

### Scenario 2: "I want to find local drilling service providers in Angola"
1. Navigate **Tier 2:** `data/processed/company_hierarchy/17. Serviços e Bens de Perfuração.../`
2. Browse all 50+ local drilling companies (SCA/LDA)
3. Find ANPG status and service niches each offers
4. If a company looks promising, check **Tier 1** to see if they have a full profile

### Scenario 3: "I'm analyzing the Angola offshore supply chain"
1. Use **Tier 2** export function: `python export_hierarchy_to_csv_excel.py`
2. Generates `company_hierarchy.csv` (3,005 rows × 13 columns) and XLSX for analysis
3. Filter by service category, ANPG status, company type (SCA/LDA/SA)
4. Cross-reference **Tier 1** profiles for international majors to understand buyer power

---

## CSV/Excel Export (Tier 2 Data)

`data/processed/company_hierarchy.csv` contains:
- Company name, NIF, type (SCA/LDA/SA), status (Preferência/Exclusividade)
- Service category (1–20), niche, sub-niche, company description
- Pre-built research URLs (Google, LinkedIn, ANPG)

**Regenerate from markdown:**
```bash
python scripts/export_hierarchy_to_csv_excel.py
```

This creates:
- `company_hierarchy.csv` (13.3 MB, 3,015 rows)
- `company_hierarchy.xlsx` (2 MB, for Excel analysis)

---

## Data Quality & Maintenance

**Tier 1** (Hand-curated):
- Last updated: April 2026
- Sources: Official company websites, LinkedIn, direct outreach (emails, phone)
- Completeness: ~95% for major international companies
- Maintenance: Manual; updated when new verified info is discovered

**Tier 2** (Automated hierarchy):
- Base data: ANPG-provided full services listing (April 2026)
- Status: Automatically populated from `company_hierarchy.csv` lookup
- Completeness: 100% of registered companies; sparse detail (most are templates awaiting data)
- Maintenance: Regenerated when new companies register with ANPG

---

## Next Steps

- **Research a company:** Start in Tier 1, cross-check in Tier 2
- **Learn a service niche:** Explore Tier 2 folder structure + Tier 1 profiles of leaders
- **Export for analysis:** Run `export_hierarchy_to_csv_excel.py` for full dataset
- **Add your research:** Edit canonical profiles in `_Profiles/` to enrich the database
- **Use in career planning:** Cross-reference [career-climbing-strategy.md](career-climbing-strategy.md) with company tiers

---

**📌 Bookmarks:**
- Tier 1 directory: [data/company-directory/](../../data/company-directory)
- Tier 2 canonical profiles: [data/processed/company_hierarchy/_Profiles/](../../data/processed/company_hierarchy/_Profiles)
- Full hierarchy export: `python data/processed/export_hierarchy_to_csv_excel.py`
- Verify company data: See [anpg-registration-verification.md](../angola/anpg-registration-verification.md)
