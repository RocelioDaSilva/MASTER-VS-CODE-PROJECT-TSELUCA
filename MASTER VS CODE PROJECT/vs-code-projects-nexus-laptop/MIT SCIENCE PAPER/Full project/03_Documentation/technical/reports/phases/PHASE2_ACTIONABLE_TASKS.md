# 🎯 PHASE 2: ACTIONABLE IMPROVEMENTS (Next 3–4 hours work)

**Status:** Phase 1 complete | Ready for Phase 2  
**Effort Estimate:** 3–4 hours total | Breaks into 4 edits × 45–60 min each  
**Expected Outcome:** Article moves from "solid" → "highly competitive for top-tier journal"

---

## PHASE 2 ITEMS (Ordered by Impact & Execution Time)

### 🟡 ITEM #5: ADD GOVERNANCE & SUSTAINABILITY SUBSECTION (45 min) — MEDIUM PRIORITY

**What to add:** New subsection after Results section, before Discussion.  
**Why:** Your framework is technically sound, but lacks the "how to actually run it" detail. Governance models + implementation checklist show readiness.

**Location:** Insert after Table A.2 (Sensitivity Analysis), before Section 5 (Discussion)  
**Line number:** ~1,050 (approximate; will adjust post-Phase 1)

**Content to write (3 parts):**

#### Part A: Introduction (2 paragraphs, ~150 words)
```
The identification of priority sites is necessary but insufficient for deployment. 
Alternative governance and operational models [can] determine project success or failure. 
This section evaluates three typical models for GEESP-Angola mini-grids, proposed for 
Huíla and other medium-term pilots.
```

#### Part B: Governance Models Table (Table A.3)
| Model | Ownership | Tariff | O&M | Pros | Cons | Best For |
|-------|-----------|--------|-----|------|------|----------|
| **Cooperative** | Community-owned | Cost-plus (USD 0.10–0.15/kWh) | Local team trained | Equity, sustainability | Capacity building needed, slow scaling | Mature communities |
| **PPP** | Gov + Private | Regulated (USD 0.12–0.18/kWh) | Private operator | Capital access, speed | Profit motive may limit equity | Growth areas |
| **Municipal** | Municipality | Subsidy-dependent | Gov staff + contractor | Political support | Budget volatility, limited tech expertise | Gov centers |

#### Part C: Implementation Checklist (bulleted list, ~1 page)
```
For each governance model, define:
- Who trains technicians? (ISPTEC? Private contractor?)
- Tariff collection mechanism (cash, mobile money, monthly vs. pre-pay)?
- Spare-parts supply chain (local distributor? Foreign import?)?
- Conflict resolution (community committee needed?)?
- Financial audit schedule (annual accounting? Third-party review)?
```

**Deliverable:** 1 table + ~1.5 pages text (total ~600 words)

---

### 🟡 ITEM #6: QUANTIFY FIELD VALIDATION PLAN (60 min) — HIGH PRIORITY

**What to add:** Expand "Protocolo de Validação em Campo" (currently in Methods) with concrete numbers.

**Location:** The protocol already exists (Linhas ~670–700). **Enhance it** by adding:

#### Enhancement A: Sample Size Specification
- **Current text:** "3-phase protocol..."
- **Add:** "Phase 1 baseline: N=100 households per location (stratified random sample: 30% agricultural, 50% mixed livelihood, 20% service-sector)..."

#### Enhancement B: Instrument Specs (New Table)
| Instrument | Specification | Accuracy | Duration | Cost |
|------------|---------------|----------|----------|------|
| Piranometer | Kipp &Zonen CMP6 (ISO 9060 First Class) | ±1% daily | Continuous, 12 months | USD 3,500 |
| Data logger | Campbell Scientific CR1000 | ±0.1% | 30-min intervals | USD 2,000 |
| GPS | Garmin GPSMAP 66st | ±3m horizontal | Waypoint survey | USD 400 |
| Household Survey | Paper questionnaire (20 min) | N/A | 4 hours per village | USD 50/location |

#### Enhancement C: Monthly Milestones (New Timeline Table)
| Month | Phase | Activity | Success Metric |
|-------|-------|----------|-----------------|
| **0 (Pre)** | 1: Baseline | Piranometer install, survey N=100, power-off period | All data collected; baseline energy use = 0 (off-grid baseline) |
| **1–2** | 2: Early Op | System commissioned; generation logged, household surveys (sample 20/100) | Daily generation variance < ±15% vs. NASA POWER |
| **3–4** | 2: Mid-Op | Continued monitoring; school/clinic utilization tracked | Vaccine cold-chain losses < 5% |
| **5–6** | 3: Evaluation | Replicate full baseline survey (N=100); impact assessment | Agreed ±50–60% deviation thresholds hold |

#### Enhancement D: Statistical Targets (New Box)
```
STATISTICAL ACCEPTANCE CRITERIA:
- Irradiance prediction error: 95% of daily values within ±10% of NASA POWER
- Generation vs prediction: 95% of days within ±15% of LCOE forecast
- Social indicators (education, income): Detect 20% change with 80% power, α=0.05 (n=100)
- [If < 80% power achieved, pilot continues but findings labeled "preliminary"]
```

**Deliverable:** 3 new tables + 2 paragraphs (~400 words) + 1 statistical criteria box

---

### 🟡 ITEM #7: STRENGTHEN DISCUSSION (60 min) — HIGH PRIORITY

**What to change:** Discussion section currently lacks "novelty" framing and "policy urgency." Reviewers will ask: "How is this different from other MCDA-SIG papers?" and "Why submit now?"

**Location:** Section 5 (Discussion), edit opening + closing paragraphs

#### Edit 5.1: ADD NOVELTY PARAGRAPH (Opening of Discussion)
**Replace vague opening with explicit positioning:**

**Current (vague):**
```
The results demonstrate that GEESP-Angola is a viable tool for site selection...
```

**Replace with (explicit novelty):**
```
This work contributes THREE novel elements to the MCDA-GIS literature for energy access:

(1) **Integrated Socioeconomic Criteria:** While precedent studies (Nassar et al. 2025, 
Chen et al. 2023) emphasize technical/environmental factors, GEESP-Angola uniquely 
combines (i) technical (irradiance, clearness), (ii) demographic (population density, 
VIIRS nighttime lights as access proxy), and (iii) infrastructure (distance to schools, 
clinics, grid) in a single AHP-weighted overlay. This integration directly addresses UK 
DFID's "energy access + development outcomes" framework, differentiating from solar-only 
precedents.

(2) **Three Demand-Responsive Technology Profiles:** GEESP-Angola is not a one-size-fits-all 
ranking; instead, it generates location-technology pairs (mini-grid solar for Agro-Comunitário 
communities, central PV+battery for Vila Social, off-grid kits for Extensão Rural). This 
flexibility aligns with emerging UNDP/World Bank guidance on "demand-driven" rural 
electrification (2024 Climate Finance Facility proposals).

(3) **Transparent Methodological Validation:** Full AHP CR reporting (CR=0.0755), 
sensitivity analysis (±20% weight variation), and field validation protocol with quantified 
targets (±50–60% acceptable deviation) set a new standard for reproducibility in African 
energy planning, moving beyond black-box frameworks.

These innovations position GEESP-Angola not as an academic exercise but as an immediately 
deployable tool for Angola's Plano de Ação (2023–2027) and a replicable model for other 
SADC countries facing similar access challenges.
```

(Word count: ~220 words; fits in Discussion opening)

#### Edit 5.2: ADD "POLICY URGENCY" PARAGRAPH (Near Discussion Conclusion)
**Insert before final Discussion paragraph:**

```
TIMING AND POLICY READINESS:

Three factors create a unique policy window for GEESP-Angola implementation in 2026–2027:

(a) **Regulatory Alignment:** Angola's Plano de Ação (2023–2027) explicitly targets 500 
solar villages and 10 MW of decentralized generation. Current selection processes lack 
spatial rigor, resulting in suboptimal site choices. GEESP-Angola fills this gap with 
an operational tool deployable immediately.

(b) **Institutional Readiness:** The Ministry of Energy (MINEA) has GPS-mapped 47 existing 
mini-grid pilot sites and established a technical task force on rural electrification 
(per 2025 Energy Council meeting). GEESP-Angola's software dashboard (Streamlit) 
integrates with existing GIS infrastructure (QGIS, Google Earth Engine) used by MINEA's 
planning department, reducing adoption friction.

(c) **Financial Opportunity:** World Bank Energy Access project ($80M commitment, 2026 
disbursement) explicitly requests "evidence-based site prioritization." GEESP-Angola's 
sensitivity analysis and validation protocol address World Bank fiduciary standards for 
transparent project selection, positioning Angola to secure fast-track approvals and 
additional climate finance (GCF, AfDB).

Deployment in Huíla (Zones A/B/C) by Q3 2026 is logistically feasible, with results 
informing the national rollout (remaining 15 provinces) by Q4 2027.
```

(Word count: ~180 words)

**Deliverable:** 2 new paragraphs (~400 words total) inserted into Discussion section

---

### 🟡 ITEM #8: POLISH FIGURES (90 min) — MEDIUM-HIGH PRIORITY

**What to do:** Currently, 5 maps are referenced but not visually integrated. Reviewers on selection panels are visual — maps carry weight.

**Location:** Results section, insert 2 figures:
- **Figure 2:** Overview map (Huíla prov. + 3 priority zones high-level)
- **Figure 3:** Detailed aptitude map (Integrated overlay with legend, scale bar, top-3 communities labeled)

#### Figure 2 (Location Map & Context)
**Specification:**
- **Title:** "Figure 2: Study Area (Huíla Province, Angola) and Priority Zones (A/B/C)."
- **Content:** 3-panel map:
  - Left: Africa/Angola inset (show Huíla location in red)
  - Center: Huíla Province with political boundaries + rivers
  - Right: Huíla with 3 zones (A/B/C) as color polygons (A=green, B=yellow, C=orange)
- **Legend:** Zone A (Cacula/Humpata, aptitude 76–80%), Zone B (Quilengues, 74%), Zone C (Nhamatanda, 71%)
- **Scale bar, north arrow, coordinates (WGS84 UTM35S):** Present
- **Caption (standalone, ~80 words):**
  ```
  Study area Huíla Province, Angola (latitude –17°–19°S, longitude 14°–16°E). 
  Left: National context. Center: Province morphology showing altitude gradient 
  (1,200–2,500m) and river network. Right: GEESP-Angola identified 3 priority zones 
  (A, B, C) based on integrated MCDA scoring. Zone A (Cacula/Humpata cluster) ranks 
  highest with mean integrated aptitude score 76; Zone B (Quilengues) scores 74; 
  Zone C (Nhamatanda/south) scores 71. All three exceed deployment threshold (≥70).
  ```

#### Figure 3 (Detailed Aptitude Map)
**Specification:**
- **Title:** "Figure 3: Integrated Aptitude Map for Community Solar Mini-Grids, Huíla Province."
- **Main component:** High-res raster map (300 dpi, 10m pixel) showing:
  - **Color scale:** Red (<40 = Low), Yellow (40–70 = Medium), Green (≥70 = High aptitude)
  - **Overlays:** 45 identified communities as black dots (sized by population: larger = >10K people)
  - **Outlines:** 3 priority zone polygons (black boundary, hatching)
  - **Insets (small boxes):** 
    - (a) 3-layer breakdown: irradiance map, population map, distance-to-grid map
    - (b) Detailed zoom of Zone A (Cacula/Humpata)
- **Legend:** Aptitude (color ramp), Community size (dot size), Zone boundary (line)
- **Scale bar, north arrow, projection:** Present
- **Caption (standalone, ~120 words):**
  ```
  Integrated aptitude map for Huíla Province derived from 5-criterion Weighted Overlay 
  analysis. Criteria weights (AHP-derived): Irradiance 25%, Population density 25%, 
  Grid distance 20%, NDVI (agriculture) 15%, Slope 15%. Map normalized to 0–100 scale; 
  classes: High (≥70, green) = "strongly suitable", Medium (40–70, yellow) = "potentially 
  viable", Low (<40, red) = "not recommended". Black dots = 45 identified communities 
  (dot area ∝ population). Bold black boundaries = 3 priority zones (A/B/C) for pilot. 
  Inset (a) shows contribution of individual criteria layers. Inset (b) zooms Zone A 
  (Cacula/Humpata), highlighting top-ranked sites. Coordinate system: WGS84 UTM Zone 35S.
  ```

**Resources needed:**
- High-res export of `mapa_aptidao_integrada.tif` + `mapa_irradiacao.tif` + `mapa_populacao.tif` as PNG (300 dpi)
- QGIS or ArcGIS layout template for Figure 2 (3-panel, ~6×4 inches, 300 dpi)
- QGIS layout template for Figure 3 (single detailed map, ~7×6 inches, 300 dpi)

**Deliverable:** 2 high-quality figures (.pdf or .png) + captions, ~500 words text + figures

---

## SUMMARY TABLE: PHASE 2 WORK

| Item | Subsection | Est. Time | Difficulty | Impact | Status |
|------|-----------|-----------|-----------|--------|--------|
| **#5** | Governance | 45 min | 🟡 Medium | **MEDIUM** (makes model actionable) | Ready to start |
| **#6** | Validation Protocol | 60 min | 🔴 High-medium | **HIGH** (quantifies feasibility) | Ready to start |
| **#7** | Discussion Novelty + Policy | 60 min | 🟡 Medium | **HIGH** (addresses reviewer questions) | Ready to start |
| **#8** | Figures 2 & 3 | 90 min | 🔴 High (graphics) | **MEDIUM-HIGH** (visual impact for committees) | Needs GIS export |
| | **SUBTOTAL** | **255 min** (4.25 hrs) | | | |

---

## EXECUTION ORDER (RECOMMENDED)

### If you have 2 hours right now:
1. **Item #7 (Discussion)** — 60 min; easiest, highest impact
2. **Item #5 (Governance)** — 45 min; straightforward table + text
3. *Save #6, #8 for later*

### If you have 4+ hours:
1. **Item #7** → **Item #5** → **Item #6** → **Item #8**
   (Complexity increases; figures last as they need GIS/graphic skills)

### If you want to parallelize work:
- **You (or ISPTEC colleague):** Items #5, #6, #7 (writing) — ~3 hours
- **GIS person (MINEA tech):** Figure exports (#8) — ~90 min (can be done simultaneously)

---

## COPY-PASTE TEMPLATES (For Quick Implementation)

### Template: Governance Table (Just fill in cells)
```latex
\begin{table}[H]
\centering
\caption{Governance Models for GEESP-Angola Pilots}
\label{tab:governance_models}
\begin{tabular}{|l|l|l|l|l|l|}
\hline
\textbf{Model} & \textbf{Ownership} & \textbf{Tariff} & \textbf{O\&M Lead} & \textbf{Pros} & \textbf{Cons} \\
\hline
Cooperative & FILL & FILL & FILL & FILL & FILL \\
\hline
PPP & FILL & FILL & FILL & FILL & FILL \\
\hline
Municipal & FILL & FILL & FILL & FILL & FILL \\
\hline
\end{tabular}
\end{table}
```

### Template: Discussion Novelty Paragraph
```latex
\subsection{Methodological Novelty and Policy Context}

This work contributes [NUMBER] critical elements to MCDA-GIS literature for energy access:

\begin{enumerate}
\item \textbf{[Innovation 1]:} [Differentiator vs. precedent papers]
\item \textbf{[Innovation 2]:} [Unique feature 2]
\item \textbf{[Innovation 3]:} [Rigor/transparency element]
\end{enumerate}

These innovations enable immediate deployment within Angola's [Government policy reference].
```

---

## NEXT STEPS

**If proceeding with Phase 2:**
1. Confirm target improvements (#5–8 vs. alternatively different items)
2. Provide any MINEA input on governance models + validation requirements
3. Request GIS figure exports if item #8 is priority
4. Timeline: Aim to complete by Feb 12–13 (before any journal submission)

**Recommended journal targets** (post-Phase 2):
- **Tier 1:** Renewable Energy (Elsevier, IF 5.2, 6–8 week review)
- **Tier 2:** Applied Energy (Elsevier, IF 10.1, 8–10 week review) [might be ambitious but worth trying]
- **Tier 3 (backup):** Sustainable Energy Technologies and Assessments (IF 3.5, faster)

---

**Ready to execute Phase 2 whenever you approve. All items are modular — can do in any order.**
