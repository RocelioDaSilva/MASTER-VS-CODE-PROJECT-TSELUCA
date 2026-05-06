# SCIENCE PAPER WEAKNESSES - CONSOLIDATED AUDIT REPORT
**Date:** April 17, 2026  
**Scope:** SOL.tex manuscript (GEESP-Angola Framework)  
**Status:** Complete review of all identified weaknesses across repository analysis files

---

## EXECUTIVE SUMMARY

The GEESP-Angola manuscript possesses strong motivation and contextual framing but contains **4 critical publication-blocking weaknesses** and **13 high-to-medium impact quality issues**. Below is the consolidated inventory from deep analysis files (ANALISE_FRAQUEZAS_COMPLETA.md, ANALISE_CRITICA_ARGUMENTACAO_ARTIGO.md, RELATORIO_DISCREPANCIA_CODIGO_MANUSCRITO.md, and others).

---

## 🔴 TIER 1: CRITICAL WEAKNESSES (Publication-Blocking)

### 1. Field Validation Protocol Promised But Never Executed
**Severity:** CRITICAL | **Blocks Publication:** YES | **Fix Time:** 3-6 months

**Problem:**
- Manuscript explicitly promises 6-month Phase 1-3 field validation with piranometer measurements in Cacula/Humpata/Quilengues
- Results section completely absent of any field-collected data
- Section 4 (Resultados) reports only modeled/predicted aptitudes, no observed data

**Evidence:**
- Line ~155: "Fase 1-3 com medições de piranómetro, validação participativa..."
- Line ~16: "CAVEAT: Zonas prioritárias PREDITAS... requerem validação rigorosa"
- Results tables (Tab 13-14): LCOE, ROI, sensitivities are all computational, not field-observed

**Impact:**
- Validation is theoretical, not empirical
- Reader expects "project implemented and validated" but receives "prototype model with uncertain validation"
- Confidence claims unsupported by primary data

**Required Fix:**
- Execute minimum 1-2 site pilots in Huíla region
- Report field-collected results (irradiance measurements, community acceptance, actual LCOE, tariff viability)
- Rewrite abstract/highlights to clarify: "framework applied to case study with planned field validation" vs. "mapeamos 45 comunidades"

**Timeline:**
- Months 1-3: Field equipment setup, baseline surveys
- Months 3-6: Active site monitoring, data collection
- Month 6: Analysis, reporting

---

### 2. Causality Not Rigorously Established; Confidence Claims Unfounded
**Severity:** CRITICAL | **Blocks Publication:** YES | **Fix Time:** 2-3 hours (documentation) + 3-6 months (empirical test)

**Problem:**
- Headline claim: "GEESP-Angola identifies viable zones with 89% confidence"
- Reality: Validation is retrospective ex-post on 5 cherry-picked cases (n=5), not prospective random assignment
- No control group; no baseline comparison methodology

**Evidence:**
- "validação retrospectiva em 5 casos (n=5), não prospectiva random-assign" 
- Selection criterion not documented — how many cases evaluated? If intentional selection, statistical bias introduced
- "34/41 (83%)" accuracy claim lacks methodology for this 41-case sample

**Impact:**
- Overestimates methodological rigor
- Claims causality without causal design (RCT, instrumental variable, matched pairs, etc.)
- Confidence interval actual uncertainty unknown

**Required Fix:**
1. **Immediate (this week):** Explicitly document limitations
   - Rewrite abstract: "retrospective validation on n=5 case studies with selection bias acknowledged"
   - Remove "89% confidence" unless followed by: "(±margin of error TBD by prospective test)"
   - Add methods section: "Limitations of Retrospective Validation"

2. **Medium-term (months 1-3):** Plan prospective test
   - Design: Random selection of ≥10 candidate sites from GEESP prediction map
   - Test: Compare GEESP-predicted aptitude vs. actual performance (irradiance, community acceptance, cost)
   - Report: confidence intervals with proper uncertainty quantification

**Key Rewrite:**
```
BEFORE: "GEESP-Angola identifies viable zones with 89% confidence"
AFTER: "GEESP-Angola retrospectively identified 5 previously successful sites 
with 89% aptitude match (n=5, selection bias acknowledged). Prospective 
validation on ≥10 randomly selected sites planned for 2026-2027 to test 
predictive accuracy and establish proper confidence intervals."
```

---

### 3. Cost-Benefit Analysis Missing; Payback Period Never Quantified
**Severity:** CRITICAL | **Blocks Publication:** YES | **Fix Time:** 3-4 hours

**Problem:**
- Benefits claimed: "40-50% risk reduction", "USD 50-250k economic savings per site"
- Implementation costs NOT quantified
- Payback period unknown → viability cannot be assessed

**Evidence:**
- Manuscript claims reduced failure (34% → 10% success improvement)
- Never calculates: USD required for GIS expertise, equipment, software, training per province
- No ROI analysis connecting implementation cost to benefits accrued

**Implementation Cost (Quantified Below):**
- GIS equipment (laptop, GPS, software QGIS): USD 2-5k
- GIS specialist salary (3-6 months @ USD 2-3k/month): USD 6-18k
- Training local staff (workshops, materials): USD 3-5k
- **Total per province:** ~USD 15-30k
- **Angola 18 provinces:** ~USD 270-540k national deployment

**Payback Analysis:**
- Benefit per site: "reduced failure 34% → 10%, saves USD 50-250k capex"
- Conservative: USD 50k × 24% improvement = USD 12k per site
- Breakeven: USD 15-30k ÷ USD 12k/site = **1.25-2.5 sites must succeed for payback**
- **Question never answered:** Is viability dependent on success in only 2 sites? Or 10 sites?

**Impact:**
- Cannot determine if GEESP investment is justified
- Appears like "expensive solution seeking problem"
- Decision-makers cannot compare: "Do we spend USD 30k on GEESP vs. USD 0 on simple methods?"

**Required Fix:**
1. Add subsection "Implementation Cost-Benefit Analysis":
```tex
\subsection{Cost-Benefit Analysis: GEESP-Angola Implementation}

Implementation costs per province:
\begin{itemize}
  \item GIS equipment and software: USD 2–5k (one-time)
  \item GIS specialist (3–6 months): USD 6–18k
  \item Staff training: USD 3–5k
  \item \textbf{Total: USD 15–30k per province}
\end{itemize}

Benefit per site (conservative estimate):
\begin{itemize}
  \item Risk reduction 34\% → 10\% implies 24\% lower failure rate
  \item Failure cost (scrapped equipment, community loss of confidence): 
        USD 50–250k per site
  \item Expected benefit: USD 12–60k per site
\end{itemize}

Payback period:
\begin{itemize}
  \item Conservative scenario: 2–5 sites must succeed for GEESP cost recovery
  \item Implementation timeline: 3–6 months setup, then immediate application
  \item Risk: If fewer than 2 sites succeed, GEESP implementation cost not recovered
\end{itemize}
```

2. Add risk table:
| Scenario | Success Rate | Sites Needed for Payback | Timeline | Recommendation |
|----------|--|--|--|--|
| Optimistic | 80% | 2 sites | 6 months | Deploy immediately |
| Conservative | 60% | 3 sites | 9 months | Deploy with caution |
| Pessimistic | 40% | 5 sites | 15 months | Pilot 1-2 sites first |

---

### 4. Code-Manuscript Discrepancy: Missing VIIRS Criterion
**Severity:** CRITICAL | **Blocks Publication:** YES | **Fix Time:** 4-6 hours (code) + 1 hour (documentation)

**Problem:**
- Manuscript specifies **6 raster criteria** for MCDA weighted overlay
- Python code (`geesp_unified_app.py`) implements only **5 criteria**
- **Missing:** Nighttime lights (VIIRS) criterion

**Detailed Inventory:**

| # | Criterion | Manuscript | Code | Status |
|---|-----------|-----------|------|--------|
| 1 | Solar irradiance (GHI) | ✅ Line 64 | ✅ w_solar | ✓ OK |
| 2 | Slope/Topography | ✅ Line 64 | ✅ w_slope | ✓ OK |
| 3 | Population density (VIIRS) | ✅ Line 64 | ✅ w_pop | ✓ OK |
| 4 | Distance to grid | ✅ Line 64 | ✅ w_dist | ✓ OK |
| 5 | NDVI (vegetation/agriculture) | ✅ Line 64 | ✅ w_ndvi | ✓ OK |
| 6 | Nighttime lights (VIIRS) | ✅ Line 64, 136, 152 | ❌ MISSING | ✗ CRITICAL |

**Evidence from Manuscript:**
- Line 64: "Integramos 6 camadas raster (irradiação solar GHI, declividade, densidade populacional VIIRS, distância à rede, NDVI, luminosidade noturna)"
- Line 152: "VIIRS com ±30% incerteza"
- Line 136: "Integração de nighttime lights (VIIRS), WorldPop, NDVI..."
- Line ~200: "Luzes Noturnas (VIIRS/DMSP): Mapas de luminosidade servem como proxy de eletrificação e demanda energética. R²≈0.88 correlação com consumo elétrico"

**Evidence from Code:**
```python
# geesp_unified_app.py lines 123-162
def cached_mcda_analysis(
    w_solar: float,      # ✅ Present
    w_pop: float,        # ✅ Present
    w_dist: float,       # ✅ Present
    w_slope: float,      # ✅ Present
    w_ndvi: float        # ✅ Present
    # ❌ MISSING: w_nightlights
):
```

**Impact:**
- Code does NOT implement methodology as published
- Research is irreproducible — third parties cannot replicate GEESP-Angola
- Violates scientific integrity standards

**Semantic Purpose of Nighttime Lights:**
Nighttime lights (VIIRS) serve as **proxy for unmet electricity demand**:
- Different from population density: identifies areas with people but NO current electricity
- Indicator of "electrification gap" = target market for GEESP
- Example: High population + low lights = high unmet demand = high success potential

**Required Code Changes:**

1. **Add VIIRS data loading** (in `cached_mcda_analysis` function):
```python
# BEFORE: 5 criteria
# AFTER: 6 criteria including nighttime lights

nightlights = cached_load_map("viirs_nighttime_lights_2023.npy")  # NEW
nightlights_norm = analyzer.normalize_raster(nightlights, name="nightlights")

aptitude = (
    w_solar * solar_norm +
    w_pop * pop_norm +
    w_dist * dist_norm +
    w_slope * slope_norm +
    w_ndvi * ndvi_norm +
    w_nightlights * nightlights_norm  # NEW
)
```

2. **Add UI slider** (in Streamlit dashboard):
```python
w_nightlights = st.slider(
    "💡 Luminosidade Noturna (peso):",
    min_value=0.0,
    max_value=1.0,
    value=0.10,
    step=0.05,
    help="Proxy de falta de eletrificação. Aumentar para priorizar zonas escuras."
)
```

3. **Normalize weights** (new, CRITICAL):
```python
# After collecting all 6 weights, normalize to sum=1.0
total_weight = w_solar + w_pop + w_dist + w_slope + w_ndvi + w_nightlights
w_solar_norm = w_solar / total_weight
w_pop_norm = w_pop / total_weight
w_dist_norm = w_dist / total_weight
w_slope_norm = w_slope / total_weight
w_ndvi_norm = w_ndvi / total_weight
w_nightlights_norm = w_nightlights / total_weight
```

4. **Suggested default weights** (per manuscript context):
```
Standard Profile (Angola general):
  w_solar = 0.25
  w_pop = 0.20
  w_dist = 0.20
  w_slope = 0.10
  w_ndvi = 0.15
  w_nightlights = 0.10
  Total = 1.00
```

**Timeline:**
- Code changes: 2-3 hours
- Testing (check map loads, weights normalize, outputs sensible): 1-2 hours
- Documentation update: 1 hour
- Total: 4-6 hours

---

## 🟠 TIER 2: HIGH-IMPACT WEAKNESSES (Quality Reduction, May Block Tier-1 Venues)

### 5. Ambiguous Value Proposition vs. Existing Methods
**Severity:** HIGH | **Blocks Publication:** Maybe (depends on venue) | **Fix Time:** 2-3 hours

**Problem:**
- What makes GEESP-Angola methodologically novel?
- Comparison with alternatives (Doorga 2022 Kenya, Nassar 2025 Iraq, Thiam 2020 Tanzania) lacks specificity
- Appears to be context application rather than methodological innovation

**Evidence:**
- Both Doorga 2022 and GEESP-Angola use: AHP, GIS, weighted overlay, same 5-6 criteria
- Only difference claimed: "First MCDA-GIS framework specific to Angola" (geography, not method)
- Table 14 compares "Patronage 2005-2013 Mozambique" vs "Consultative 2010-2020 Tanzania" vs "GEESP 2018-2023 Kenya" — not comparable contexts

**Impact:**
- Difficult to justify publication in methods-focused journals
- Restricts to regional/applied venues (lower impact)

**Required Fix:**
1. **Create detailed comparison table:** GEESP-Angola vs. Doorga vs. Nassar
```
| Feature | GEESP-Angola | Doorga 2022 | Nassar 2025 | Innovation? |
|---------|---|---|---|---|
| AHP-based weighting | Yes | Yes | Yes | No (standard) |
| GIS weighted overlay | Yes | Yes | Yes | No (standard) |
| Criteria count | 6 | 5-6 | 4-5 | Minor variation |
| Participatory validation | Planned | Implemented | Implemented | GEESP lags |
| Specific to context | Angola | Kenya/Uganda | Iraq | All context-specific |
| **True innovation:** | ??? | ??? | ??? | ??? |
```

2. **Clarify what IS novel:**
- Is it the specific criterion combination (6 vs. 5)?
- Is it the application to Angola's specific geography + institutions?
- Is it the engagement methodology (women's groups, local cooperatives)?
- Is it the cost-sharing model with PNUD + municipal government?
- **Be explicit, not vague**

---

### 6. Results Section Anemic vs. Discussion Hypertrophied
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 6-8 hours

**Problem:**
- Results section: ~60 lines (3% of document)
  - Only 3 zones aptitude scores (0.83, 0.79, 0.76)
  - Few data tables
  - Placeholder figures marked "absent"
- Discussion section: ~400+ lines (20%+)
  - 10+ subsections (interpretations, trade-offs, policy, climate, gender, business model)
  - Too much theoretical speculation vs. data-driven analysis
- **Standard journal practice:** Results ≈ Discussion (1:1 ratio)

**Evidence:**
- Results (Section 4): ~60 lines of sparse data
- Discussion (Section 6): 6.1-6.10 subsections covering 350+ lines

**Impact:**
- Reader gets impression of weak empirical contribution
- Structure suggests analysis thin on actual findings
- Violates academic writing norms

**Required Fix:**
1. **Expand Results** (add 100+ lines):
   - More detailed zone descriptions (not just aptitudes)
   - Expanded tables for each zone (population, current electricity access, infrastructure, land use)
   - LCOE breakdowns per zone
   - Sensitivity analyses with visual charts
   - Preliminary validation data (if available)

2. **Consolidate Discussion** (reduce from 10 to 4-5 subsections):
   - 6.1-6.2: **Interpretation of Results** (current and methodological implications)
   - 6.3-6.4: **Comparison with Literature** (Doorga, Nassar, precedents)
   - 6.5-6.6: **Implementation & Policy Implications** (Angola-specific context)
   - 6.7-6.8: **Limitations & Future Work**
   - Remove fragmented subsections (gender, climate as separate → integrate into 6.6 "implementation")

3. **Reorganize numbering:**
   - Current: 6.3.1, 6.3.2, 6.3.3 (sub-subsections appearing ad-hoc)
   - Correct to: 6.8, 6.9, 6.10 (clear main subsections)

---

### 7. Discussion Fragmented Into 10+ Disconnected Subsections
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 4-6 hours

**Problem:**
- Subsections 6.1-6.10+ do not form coherent narrative
- Jumps between interpretations (6.1) → trade-offs (6.2) → comparisons (6.3) → policy (6.4) → climate (6.5) → gender (6.6) → business model (6.7) → then back to interpretations (6.3.1-6.3.3)
- Numbering broken: 6.3.1, 6.3.2, 6.3.3 appears as sub-subsections when logically should be 6.8, 6.9, 6.10

**Evidence:**
- Structure appears ad-hoc; suggests late additions without reorganization

**Required Fix:**
1. **Regroup into 4-5 coherent meta-topics:**
   ```
   6.1 Interpretation of Aptitude Model & Results
   6.2 Comparison with Existing Methodologies (Doorga, Nassar, Thiam)
   6.3 Implementation Pathways & Institutional Requirements
       6.3.1 Multi-criteria Business Model
       6.3.2 Sustainability Determinants (gender, climate, governance)
       6.3.3 Policy Alignment with Angola Energy Goals
   6.4 Limitations & Future Research Needs
   ```

2. **Fix numbering:** Promote sub-subsections (6.3.1-6.3.3) to main sections or keep as 6.3.1-6.3.3 only if they're genuinely sub-topics

3. **Ensure narrative flow:** Each transition should have bridging sentence

---

### 8. Theory-Methodology Gap: Sen/Nussbaum Invoked But Not Operationalized
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 3-4 hours

**Problem:**
- Section 2.1 eloquently discusses Amartya Sen's "capability approach" and Martha Nussbaum's 10 central capabilities
- Quotes: "Uma mulher em Cacula com acesso a luz elétrica ganha capacidade de estudar à noite (educação), bombear água para irrigação (renda agrícola), conservar medicamentos (saúde), e participar em processos decisórios comunitários (voz política)."
- **But then:** MCDA weighted overlay uses only technical criteria (solar, slope, population, distance, NDVI, lights)
  - No explicit raster layer for "educational capacity"
  - No raster for "voice/political agency"
  - No raster for "health infrastructure"
- Theory is "adorned but not actionable" — humanitarian language detached from technical pragmatism

**Impact:**
- Readers question: "How does GEESP actually maximize capabilities described by Sen?"
- Appears theory is window-dressing, not central to logic

**Required Fix:**
1. **Add Theory-Operationalization Appendix:**
```
TABLE: Mapping Sen-Nussbaum Capabilities to GEESP-Angola Indicators

| Capability | Definition | GEESP Operationalization | Data Source |
|---|---|---|---|
| Education | Learning ability | Proxy: Schools within 5km buffer (binary Y/N) | OpenStreetMap POI |
| Health | Physical/mental wellbeing | Proxy: Clinics within 5km + NDVI (vegetation) | OSM POI + Sentinel-2 |
| Economic freedom | Livelihood opportunity | Proxy: Distance to market/transport + NDVI (agriculture) | OSM roads + Sentinel |
| Political voice | Participation in decisions | Proxy: Cooperative presence (soft indicator, Phase 1) | Baseline survey |
| Climate resilience | Adaptation to environment | Proxy: NDVI + water access | Sentinel-2 |
| Life | Survival & health | Proxy: Combination of health + water access | OSM + Sentinel |
```

2. **Revise narrative:** "While Sen argues energy expands freedom, our framework operationalizes this by identifying zones where complementary infrastructure (schools, clinics) already exists, maximizing multiplier effects. In Humpata (Zone B), proximity to 3 schools and 1 clinic means electrification immediately enables educational benefits; areas lacking these services would require co-investment."

---

### 9. Comparisons Not Contemporaneous
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 2-3 hours

**Problem:**
- Table 14 compares three methodologies from different contexts and time periods:
  - Patronage (Mozambique 2005-2013, n=12)
  - Consultative (Tanzania 2010-2020, n=12)
  - GEESP-Angola (Kenya 2018-2023, n=5)
- Superiority attributed to method, but confounded by temporal evolution + context

**Evidence:**
- Mozambique's patronage approach is historical (2005-2013)
- Tanzania's consultative model is different country (2010-2020)
- Kenya's GEESP application is most recent (2018-2023)
- **Conclusion:** Can't isolate whether GEESP superiority comes from method or just "progress over time + favorable context"

**Impact:**
- Causal inference weak
- Appears GEESP benefits from "recent evolution" not inherent methodological superiority

**Required Fix:**
1. **Reframe comparison:** "Temporal Evolution of Selection Methodologies" (explicitly acknowledge time/context confounding)
2. **Add caveat:** "While GEESP-Angola shows better outcomes, we cannot attribute this solely to method given different implementation contexts and decades. Prospective comparison (GEESP vs. alternatives applied simultaneously in same context) recommended for future research."
3. **Alternatively:** Conduct controlled comparison in Angola:
   - Apply GEESP-Angola methodology to select sites
   - Apply simpler alternative (expert opinion, aggregated data) to select different sites
   - Compare outcomes prospectively (2-3 years)

---

### 10. AHP Weights Determined by Expert Panel but Not Empirically Validated
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 2-3 hours

**Problem:**
- Methodology: 5 expert panelists determined AHP weights in workshop
- Consistency ratio (CR) = 0.0755 (acceptable, <0.10 per Saaty standard)
- **But:** No documentation of expert divergence; no empirical test of weights' importance

**Evidence:**
- Sensitivity analysis shows zones "maintain ranking" at ±20% weight variation
- But this is ordinal (ranking preserved), not cardinal (impact on outcomes quantified)
- Never tested: Are these weights the "correct" weights? Or just "one acceptable set"?

**Impact:**
- Readers question: How do we know these weights are right?
- Answer should be: Empirical validation in field pilots (but not done)

**Required Fix:**
1. **Document expert panel:**
   - List experts' names/affiliations
   - Report divergence: Did all 5 agree on weights? Or significant disagreement?
   - Provide panel discussion notes/transcript showing rationale

2. **Expand sensitivity analysis:**
   - Instead of just "ranking maintained," show cardinal impact:
   ```
   | Weight Scenario | Zone A Aptitude | Zone B Aptitude | Zone C Aptitude | LCOE Δ |
   |---|---|---|---|---|
   | Base | 0.83 | 0.79 | 0.76 | USD 0.24 |
   | -20% solar weight | 0.78 | 0.75 | 0.71 | USD 0.26 |
   | +20% pop weight | 0.85 | 0.81 | 0.79 | USD 0.23 |
   | +20% nightlights weight | 0.84 | 0.80 | 0.78 | USD 0.23 |
   ```

3. **Propose empirical validation:**
   - "In Phase 1 field validation, we will record which criterion (solar, population, distance, slope, NDVI, lights) best predicts actual site success/failure"
   - "Post-pilot, AHP weights can be recalibrated based on observed importance"

---

### 11. No Discussion of GEESP Implementation Disadvantages
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 2-3 hours

**Problem:**
- Manuscript assumes GEESP superior in all dimensions
- Never discusses costs, expertise requirements, implementation timeline, or when simpler methods might be preferable

**Risks Not Discussed:**
- GIS expertise requirement (non-trivial in rural Angola; requires 1-2 trained technicians per province)
- Computational infrastructure (laptops, software licenses, internet connectivity)
- Implementation timeline: 6-12 months before 1st kWh (vs. faster ad-hoc selection)
- Trade-off: GEESP complexity vs. simple selection (expert opinion, "follow electrification natural growth")
- Political risk: Transparent, top-down algorithm may threaten local power structures
- Organizational risk: MINEA/EDA may lack capacity to maintain GEESP system long-term

**Impact:**
- Appears "advocacy for GEESP" vs. "balanced risk assessment"
- Decision-makers cannot make informed choice: "Is GEESP appropriate for our context?"

**Required Fix:**
1. **Add subsection "Limitations & Appropriate Use Cases":**
```tex
\subsection{Limitations & Contextual Applicability}

While GEESP-Angola offers advantages in objectivity and reproducibility, it is not 
universally appropriate for all contexts. Disadvantages include:

\begin{enumerate}
\item \textbf{Expertise Requirements:} GEESP requires trained GIS specialists, 
      MCDA knowledge, and technical capacity. Small municipalities may lack these skills, 
      requiring external technical support (cost: USD 6–18k per province).
      
\item \textbf{Implementation Timeline:} Data acquisition (satellite imagery, field surveys) 
      + AHP process + community validation = 6–12 months before implementation begins. 
      Simpler methods (expert opinion, follow existing electrification patterns) can 
      be deployed within 4–8 weeks.
      
\item \textbf{Infrastructure Dependency:} GEESP requires reliable internet, GIS software 
      (QGIS, ArcGIS), and computational hardware. Maintenance may be challenging in 
      remote areas with limited technical support.
      
\item \textbf{Political Risk:} Algorithmic site selection, while objective, may encounter 
      resistance from local authorities accustomed to patronage-based allocation. 
      Transparent methodology can threaten existing power structures.
      
\item \textbf{Data Availability:} Accuracy depends on quality of input data (satellite 
      imagery, population census, grid maps). In Angola, some regions lack current 
      geospatial data, introducing uncertainty.
\end{enumerate}

Recommended use cases for GEESP-Angola:
\begin{itemize}
\item Provinces with 5+ planned mini-grid sites (sufficient scale to justify setup cost)
\item Institutional partners with GIS capacity or training resources
\item Donor-funded projects with 18–24 month timelines
\end{itemize}

Contexts where simpler methods may be preferable:
\begin{itemize}
\item Small municipalities with <5 planned sites
\item Rapid deployment scenarios (emergency electrification)
\item Communities with strong traditional decision-making preferences (requiring deeper 
      participatory methods than GEESP alone)
\end{itemize}
```

---

### 12. Non-Empirical Testing of GEESP Components
**Severity:** HIGH | **Blocks Publication:** Maybe | **Fix Time:** 1-2 hours (documentation)

**Problem:**
- Genre of intervention untested: "Babayomi's 4 factors (PDA, training, governance, maintenance) incorporated into GEESP"
- But: No empirical evidence that simultaneous implementation of these 4 factors in Angola context yields claimed 73% sustainability

**Evidence:**
- Manuscript states GEESP incorporates factors, but does not test them
- Claim: "modelos comunitários (cooperativa/associação) atingem 72% sustentabilidade" but source is Babayomi 2023, not GEESP pilot

**Impact:**
- Unclear whether GEESP success depends on Babayomi's 4 factors, or on site selection itself, or on both
- Cannot decompose which ingredient matters most

**Required Fix:**
1. **Add research question:** "Do Babayomi's 4 factors explain variance in GEESP site success?"
2. **Design test:** In Phase 1 pilots, measure all 4 factors + site outcomes → regress to quantify contribution

---

## 🟡 TIER 3: MEDIUM-IMPACT WEAKNESSES (Clarity & Professionalism)

### 13. Inconsistent Terminology
**Severity:** MEDIUM | **Fix Time:** 1 hour

| Inconsistency | Standardize To |
|---|---|
| "mini-grid" vs "mini-rede" | **mini-rede** (Portuguese) |
| GEESP-Angola vs Geesp-Angola vs geesp | **GEESP-Angola** (consistent capitalization) |
| "energia solar comunitária" vs "sistemas solares comunitários" | Choose one |

---

### 14. Language Mix (Portuguese + English)
**Severity:** MEDIUM | **Fix Time:** 2-3 hours

**Problem:** 75% Portuguese, 25% English (especially in Sections 6.5+)

**Examples:**
- "While GEESP-Angola foi projetado..." (English + Portuguese mix)
- "Climate Resilience" (English section headers)
- "Climate Vulnerability Index" (English in Portuguese context)

**Fix:** Convert all to Portuguese OR all to English; choose one language for submission

---

### 15. Excessive Textual Density
**Severity:** MEDIUM | **Fix Time:** 2-3 hours

**Example:**
> "Para a Huíla, isto traduz-se em benefício direto para 95.000 pessoas: ~12.000 crianças com acesso nocturno a educação, ~850 gestantes com acesso a serviços de parto seguro (projeção conservadora: redução 15-20% mortalidade maternal), e ~8.000 agricultores com capacidade de irrigação mecanizada gerando renda adicional USD 180.000 agregado em 5 anos."

**Fix:** Break into 2-3 sentences; maximum 2 data points per sentence

---

### 16. National Cases Not Feeding Into MCDA Methodology
**Severity:** MEDIUM | **Fix Time:** 2 hours

**Problem:** Cozinhas Solares case shows (94% uptime, USD 0.35/kWh tariff, 40% subsidy dependence) but these numbers don't reappear in AHP weights calibration

**Fix:** Append table showing which Cozinhas Solares metrics were incorporated into GEESP weights

---

### 17. Results → Recommendations Bridge Missing
**Severity:** MEDIUM | **Fix Time:** 2-3 hours

**Problem:** Results show aptitude scores (0.83, 0.79, 0.76) but don't explain why Zone A → PV+Battery, Zone C → Hybrid

**Fix:** Add subsection interpreting results with explicit logic for technology choice

---

## 📊 SUMMARY: Prioritized Action Plan

| Priority | Weakness | Time | Blocking? |
|----------|----------|------|-----------|
| **P0** | Code: Add VIIRS criterion | 4-6 hrs | YES |
| **P0** | Cost-benefit analysis | 3-4 hrs | YES |
| **P1** | Field validation (plan + execute) | 3-6 mo | YES |
| **P1** | Causality documentation | 2-3 hrs | YES |
| **P2** | Results/Discussion restructure | 6-8 hrs | MAYBE |
| **P2** | Discussion consolidation | 4-6 hrs | MAYBE |
| **P2** | Theory-operationalization appendix | 3-4 hrs | MAYBE |
| **P3** | Terminology, language, density | 4-6 hrs | NO |
| **P3** | Disadvantages section | 2-3 hrs | NO |
| **P3** | Comparison contemporaneity | 2-3 hrs | NO |

**Estimated Total Effort:**
- Code + documentation fixes: 7-10 hours (this week)
- Manuscript structural improvements: 15-20 hours (this week/next)
- Field validation execution: 3-6 months (ongoing)

---

## 🎯 NEXT STEPS

1. **This week (URGENT):**
   - [ ] Add VIIRS criterion to Python code
   - [ ] Add cost-benefit section to manuscript
   - [ ] Document causality limitations

2. **Next 2-3 weeks (HIGH PRIORITY):**
   - [ ] Restructure Results/Discussion sections
   - [ ] Consolidate Discussion subsections
   - [ ] Add theory-operationalization table

3. **Ongoing (3-6 months):**
   - [ ] Execute Phase 1 field pilots
   - [ ] Collect empirical validation data
   - [ ] Rewrite results with actual field data

---

**Report Compiled:** 17 April 2026  
**Status:** Ready for implementation  
**Next Review:** After field validation (Month 6)
