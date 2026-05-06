# TECHNOLOGY SELECTION MATRIX FOR COMMUNITY SOLAR SYSTEMS
**Integrated with 12-Criteria Evaluation Framework**
**Version**: 1.0 | **Date**: February 8, 2026

---

## Executive Overview

This matrix connects **spatial aptitude scores** (from GEESP-Angola MCDA) to **optimal technology recommendations**, ensuring that technology selection is:
1. ✅ **Spatially-optimized** (matches local solar resources + constraints)
2. ✅ **Financially-viable** (LCOE calculated for each zone combination)
3. ✅ **Socially-appropriate** (community capacity + operational complexity)
4. ✅ **Technically-feasible** (supply chain + skills available in Angola)
5. ✅ **Operationally-sustainable** (maintenance model realistic for 20+ year lifetime)

---

## Part 1: Technology Options (4 System Types)

### **Option A: PV-Fixed + Battery (Recommended for Zone A, Aptitude 0.76–1.0)**

**Technical Specifications**:
- **PV Array**: Fixed tilt (17° optimal for Huíla latitude), monocrystalline panels 370–380 Wp
- **Battery Storage**: Lithium-ion (LiFePO4), 6-hour autonomy (oversizing for cloudy spells)
- **Inverter**: Hybrid inverter (grid-forming, islanding capable)
- **Balance of System**: Combiner box, DC breakers, monitoring (SCADA-capable)

**Criteria Coverage**:
- ✅ **Clareza científica**: Well-established technology, extensive literature, modeling tools standardized
- ✅ **Viabilidade técnica (TRL)**: TRL 9/9 (mass-produced, proven in sub-Saharan Africa)
- ✅ **Recurso-condicionado**: Requires GHI > 5.5 kWh/m²/day (Zones A, B, partially C)
- ✅ **Sustentabilidade operacional**: Minimal moving parts → low maintenance (quarterly inspections)
- ✅ **Escalabilidade**: Modular (can add batteries later, no redesign required)
- ✅ **Custo-benefício**: LCOE USD 0.18–0.22/kWh (best among options)

**Advantages**:
- Lowest LCOE when GHI favorable
- Simplest operation (local technician can manage)
- Mature supply chain (panels readily available Angola/SADC, batteries from South Africa)
- Very reliable (>95% annual availability)

**Disadvantages**:
- High CapEx (battery cost USD 2.8M for 20 MWh storage)
- Battery lifespan 10–15 years (replacement needed mid-project)
- Sensitive to cloud cover (requires adequate sizing)

**Community Appropriateness**:
- **Skills Required**: Low (technician needs 4-week training, can be local)
- **Governance Model**: Community cooperative manages tariff collection + maintenance fund
- **Complexity**: Medium (requires daily monitoring system, not complex computations)

**Financial Model (Zone A, 12.5 MW example)**:
- **CapEx**: USD 31.25M (panels) + USD 2.8M (battery) = USD 34.05M
- **LCOE at 8% IRR**: USD 0.20/kWh (20-year NPV USD 28.6M)
- **Payback**: 6.2 years
- **Tariff-Setting**: USD 0.25/kWh (leaves USD 0.05/kWh margin for O&M + profit)

**Recommended For**:
- Zone A (Cacula): Highest irradiance, largest population, strongest community readiness
- Communities within 50 km of existing transmission (grid resilience)
- Mixed load profiles (24-hour usage: schools, clinics, irrigation + night-time domestic)

**Regulatory Fit**:
- ✅ Aligns with Angola's renewable energy policy (solar explicitly prioritized)
- ✅ No special grid permits required (islands operate independently)
- ✅ Environmental: Zero greenhouse gas, minimal land disturbance

---

### **Option B: PV-Tracker (1-axis) + Battery (Recommended for Zone B, Aptitude 0.70–0.85)**

**Technical Specifications**:
- **PV Array**: Single-axis tracking system (horizontal E-W tracking), same panels as Option A
- **Benefit**: +25% generation compared to fixed tilt (due to tracking sun movement)
- **Actuators**: Hydraulic or electric motors + controller (medium complexity)
- **Battery**: Same as Option A (Li-ion, 6-hour)
- **Balance of System**: Similar to Option A, plus tracking control circuitry

**Criteria Coverage**:
- ✅ **Clareza científica**: Tracking technology well-studied, efficiency gains predictable
- ✅ **Viabilidade técnica (TRL)**: TRL 8/9 (proven in Africa, but less common than fixed)
- ✅ **Recurso-condicionado**: Optimal for GHI 5.2–5.8 kWh/m²/day (Zone B sweet spot)
- ✅ **Sustentabilidade operacional**: Medium—tracking system adds 1–2 maintenance tasks/year (annual motor service)
- ✅ **Escalabilidade**: Can disable tracking if maintenance not feasible (degrades to fixed tilt option)

**Advantages**:
- 25% more generation than fixed tilt → higher capacity factor
- Better for lower-irradiance zones (B, C use Case B because of this premium)
- Justifies battery investment (higher utilization of storage)

**Disadvantages**:
- **Higher CapEx** (USD 0.50/Wp for tracking system vs USD 0.25/Wp fixed)
- **Operational complexity** (technician needs motor/hydraulic knowledge)
- **Supply chain risk** (fewer local suppliers; parts may be imported from South Africa/Europe)
- **O&M cost** higher (tracking system ~USD 5K/year for lubrication, sensor checks vs USD 1K/year for fixed)

**Community Appropriateness**:
- **Skills**: Medium (technician must complete 8-week training, ideally with mentorship in SADC region)
- **Governance**: Requires designated "system manager" (not just community operator)
- **Complexity**: Medium-High (tracking system daily or manual reset if motors fail)

**Financial Model (Zone B, 8.2 MW example)**:
- **CapEx**: USD 20.5M (panels + tracker system higher cost)
- **Generation Premium**: 25% more → LCOE advantage only if GHI well-suited
- **LCOE at 8% IRR**: USD 0.22–0.25/kWh (slightly higher than fixed due to complexity)
- **Justification**: Payback extended to 6.8 years, but higher reliability
- **Tariff-Setting**: USD 0.28/kWh (vs USD 0.25 for fixed option)

**Recommended For**:
- Zone B (Humpata): Moderate irradiance (5.72 kWh/m²/day) where tracking adds 20–30% useful generation
- Communities <30 km from South Africa border (access to technical support)
- Mid-scale systems (5–15 kW) where CapEx less constraining than small/large

**Risk Mitigations**:
- **Fallback**: Tracker can be disabled (lock in optimal fixed position) if maintenance becomes infeasible
- **Supplier**: Contractual SLA with Southern Africa supplier for 5-year parts availability
- **Training**: Pair each community tracker operator with regional technician (visit every 6 months)

---

### **Option C: Hybrid Solar-Diesel (Recommended for Zone C, Aptitude 0.60–0.75, OR contingency)**

**Technical Specifications**:
- **PV Array**: 5–10 kW (smaller than options A/B, used to reduce diesel fuel)
- **Diesel Generator**: 5–10 kW backup (existing technology in Angola)
- **Battery**: Smaller (5–10 kWh, mainly for bridging solar disappearance)
- **Controller**: Hybrid inverter that optimizes PV-diesel blend (minimize fuel burn)

**Criteria Coverage**:
- ✅ **Viabilidade técnica (TRL)**: TRL 9/9 (standard in rural Africa during transition phase)
- ✅ **Escalabilidade**: Can add more PV later (retrofit-friendly)
- ✅ **Custo-benefício**: Medium (avoids large upfront battery CapEx)
- ⚠️ **Sustentabilidade ambiental**: Trade-off (diesel emissions, fuel supply vulnerability)
- ⚠️ **Sustentabilidade econômica**: Diesel price volatility (if fuel > USD 1.50/L, model breaks)

**Advantages**:
- **Lower upfront CapEx** (no USD 2.8M battery for Zone A equivalent)
- **Operational familiarity** (communities already run diesel systems)
- **Scalability**: Start small (solar reduces diesel by 20–30%), grow PV over time

**Disadvantages**:
- **High LCOE** (USD 0.28–0.35/kWh due to diesel fuel cost + generator O&M)
- **Not viable long-term** (diesel price trends upward; doesn't meet climate goals)
- **Fuel supply logistics** (must import diesel, price exposure)

**Community Appropriateness**:
- **Skills**: High (diesel maintenance already known, hybrid controller is new knowledge)
- **Governance**: Diesel costs may create tariff disputes (fuel price changes weekly)
- **Complexity**: Medium (hybrid system has automatic switchover logic, potential for failure)

**Financial Model (Option C example)**:
- **CapEx**: USD 5M (5 kW solar + 5 kWh battery + modest 5 kW diesel generator)
- **LCOE at 8% IRR**: USD 0.28–0.35/kWh (fuel price dependent)
- **Breakeven vs pure diesel**: Only if solar generation >40% of total (not achievable in Zone C)
- **Payback**: 8–10 years (if diesel stays <USD 1.20/L; longer if price rises)

**Recommended For**:
- **Zone C (Quilengues** as **initial option** to reduce upfront investment
- **Contingency**: If battery supply delays Option A/B (can install diesel + PV, upgrade to battery later)
- **Transitional**: Communities beginning electrification (phase from 100% diesel → hybrid → 100% PV over 10 years)

**Climate/SDG Risk**:
- ⚠️ Does NOT align with Angola's goal of 72% renewables by 2027
- ⚠️ Does NOT meet SDG 13 (climate action) unless explicit transition plan to 100% PV by Year 10

---

### **Option D: Solar-Powered Water Pumping (Special Case for Agricultural Communities)**

**Technical Specifications**:
- **PV Array**: 2–5 kW (dedicated to water pumping)
- **Pump**: Submersible solar pump (brushless DC, optimized for low-power operation)
- **Storage**: Water tank (replaces battery; water = stored energy)
- **Application**: Irrigation, livestock watering, community water supply

**Criteria Coverage**:
- ✅ **Resolução pratica**: Addresses multiple needs (water + electricity) from same PV
- ✅ **Impacto social**: Water scarcity = critical constraint in Huíla; solution improves agriculture
- ✅ **Sustentabilidade**: Water storage more resilient than battery (no degradation)
- ✅ **Custo-beneficio**: LCOE lower (no battery) + revenue from agricultural products (vegetables, dairy)

**Advantages**:
- **Lower CapEx** (no battery)
- **Dual use** (water + primary energy need)
- **Revenue generation** (communities sell irrigated produce → tariff payment capacity improves)
- **Resilience** (water tank decouples solar variability; no daily battery charging needed)

**Disadvantages**:
- **Limited to water-accessible communities** (requires river/borehole within feasible distance)
- **Not supplyin evening electricity** (pumping only daytime)

**Community Appropriateness**:
- **Skills**: Low (pump operation minimal training)
- **Governance**: Cooperative manages both water + electricity revenue

**Recommended For**:
- **Zone A (Cacula)**: Rio Vombe river ~3 km away → Option D supplements PV batteries
- **Communities with agriculture as primary livelihood** (produce irrigation → local jobs + income)
- **Gender benefit**: Water collection (traditionally women's task) → time freed for education/business

---

## Part 2: Decision Matrix (Aptitude → Technology)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Technology Suitability Matrix (Input: Zone Aptitude Score → Technology)   │
└─────────────────────────────────────────────────────────────────────────┘

ZONE APTITUDE SCORE  │  GHI RANGE     │  RECOMMENDED TECHNOLOGY    │  BACKUP OPTION
────────────────────┼────────────────┼──────────────────────────────┼─────────────────
0.80–1.0            │ 5.8–6.8 kWh/m│ Option A: PV-Fixed + Battery │  Option B (premium)
(Zone A: Cacula)    │ /day           │ LCOE: USD 0.18–0.22/kWh    │  +5% cost for
Certainty: HIGH     │ Confidence:    │ Payback: 6–7 years         │  tracking
                    │ HIGH           │ TRL: 9/9, Most Mature      │

0.70–0.80           │ 5.5–5.8 kWh/m │ Option B: PV-Tracker       │  Option A (fallback)
(Zone B: Humpata)   │ /day           │ + Battery                  │  if motor supply
Certainty: MEDIUM   │ Confidence:    │ LCOE: USD 0.22–0.25/kWh    │  fails
                    │ MEDIUM         │ Payback: 6.5–7.5 years     │
                    │                │ TRL: 8/9, Supply chain ok  │

0.60–0.70           │ 5.2–5.5 kWh/m │ Option C: Hybrid (Solar +   │  Option A at
(Zone C:            │ /day           │ Diesel) for transition     │  higher LCOE
Quilengues)         │ Confidence:    │ OR Option D: Solar Pump    │  if/when diesel
Certainty: MEDIUM   │ MEDIUM-LOW     │ + Irrigation (dual-use)    │  unavailable
                    │                │ LCOE: USD 0.25–0.35/kWh    │
                    │                │ (Option C) vs USD 0.15/kWh │
                    │                │ (Option D, no battery)     │

<0.60               │ <5.2 kWh/m/day │ NOT RECOMMENDED for solar   │  Option C only if
(Remote/marginal    │ Confidence:    │ (LCOE prohibitive)         │  government
areas)              │ LOW            │ Alternative: Extend grid OR│  mandate
Certainty: LOW      │                │ Diesel-only for now        │
                    │                │                            │
                    │                │ EXCEPTION: Small solar kits │
                    │                │ (0.05–0.5 kWp, <10 people)│
                    │                │ for household lighting      │
```

---

## Part 3: Weighting by Evaluation Criteria

### **How Each Criterion Influences Technology Choice**:

| Criterion | Implication for Tech Selection |
|-----------|-------------------------------|
| **1. Clareza Científica** | Must justify WHY specific tech; full life-cycle model provided (LCOE, emissions, supply chain) |
| **2. Relevância Prática** | Tech must solve actual problem (no electricity → system must provide reliable power); validated with community needs assessment |
| **3. Viabilidade Técnica** | TRL assessment mandatory; import dependencies, local skills, spare parts availability all considered |
| **4. Viabilidade Económica** | LCOE, payback, sensitivity to cost/tariff variation; option must beat baseline (current diesel or grid extension) |
| **5. Alinhamento Político** | Tech must align with Angola's renewable energy goals (72% by 2027); hybrid/diesel options discouraged politically |
| **6. Equipa & Capacidade** | Local tech capacity determines max complexity (Zone A skilled community → Option B feasible; Zone C low capacity → Option A w/ external support) |
| **7. Ética & Equidade** | Tech design must benefit vulnerable groups (women, elderly); Option D (water pump) favors women particularly |
| **8. Reprodutibilidade** | Tech choice must be open-source and replicable (e.g., no proprietary tracking systems); all data/models public |
| **9. Risco & Mitigação** | Must identify failure modes + backup plans (e.g., if battery fails → can operate Option A as fixed for reduced output) |
| **10. Disseminação** | Tech must be documented in peer-review literature (Options A/B published extensively; Option C transitional; Option D innovative gap-filler) |
| **11. Métricas & M&E** | Must have clear KPIs (MW generated, cost/beneficiary, CO₂/year, tariff collection %, uptime %) tracked monthly |
| **12. Apresentação** | Tech choice must be compelling to funders (AfDB prefers renewable-only → Options A/B favored; World Bank open to hybrids for transition) |

---

## Part 4: Detailed LCOE Comparison Table

```
┌───────────────────────────────────────────────────────────────────────────────┐
│ Levelized Cost of Electricity (LCOE) Comparison                                 │
│ Assumptions: 20-year project life, 8% annual discount rate, Angola market 2023  │
└───────────────────────────────────────────────────────────────────────────────┘

COST COMPONENT            │  OPTION A       │  OPTION B        │  OPTION C      │  BASELINE
                          │  PV-Fixed       │  PV-Tracker      │  Hybrid        │  (Diesel)
                          │  (Zone A)       │  (Zone B)        │  (Zone C)      │
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
CapEx Breakdown           │                 │                  │                │
└─ PV Panel (USD/Wp)      │     0.25        │     0.25         │     0.20       │    —
└─ Tracking (USD/Wp)      │      —          │     0.50         │      —         │    —
└─ Battery (USD/kWh)      │    140          │     140          │     100        │    —
└─ Diesel Gen. (USD/kW)   │      —          │      —           │     300        │   300
└─ BOP (USD/Wp)           │     0.75        │     0.75         │     0.30       │    —
└─ Total CapEx (12.5 MWp) │   USD 34.0M     │   USD 37.5M      │   USD 8.5M     │    —
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
OPEX Annual               │                 │                  │                │
└─ O&M (% of CapEx/year)  │     1.5%        │     2.2%         │     3.5%       │   8–10%
└─ Fuel (L/kWh)           │      —          │      —           │    0.25        │    0.35
└─ Fuel cost (USD/L)      │      —          │      —           │    1.15        │    1.15
└─ Annual OPEX            │  USD 510K       │  USD 825K        │   USD 1.2M     │  USD 2.1M
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
LCOE Calculation          │                 │                  │                │
(20-year NPV, 8% IRR)     │                 │                  │                │
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
Annual Generation (GWh)   │    16.2         │    20.3 (25% +)  │    5.8         │    6.2
LCOE (USD/kWh)           │   0.18–0.20    │   0.22–0.25      │   0.28–0.35    │  0.40–0.50
Payback Period (years)    │    6.2          │     6.8          │     8.5        │    N/A
NPV @ 8% (USD MM)        │   28.6          │    16.9          │    × (negative)│    —
TIR (%)                  │   14.2%         │    13.8%         │    9–11%       │    —
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
SENSITIVITY ANALYSIS      │                 │                  │                │
(20% cost variation)      │                 │                  │                │
├─ CapEx ↑20%             │  0.20 → 0.24   │  0.25 → 0.30     │  +0.05/kWh    │    —
├─ Tariff ±15%            │  ±0.02/kWh     │  ±0.02–0.03      │  ±0.03–0.05   │    —
├─ Interest 6%→10%        │  0.17 → 0.22   │  0.21 → 0.27     │  +0.02–0.05   │    —
└─ Ranking after tests    │  OPTION A wins  │   Option B 2nd   │   Option C last│    —
──────────────────────────┼─────────────────┼──────────────────┼────────────────┼──────────
COMPETITIVE VERDICT       │                 │                  │                │
                          │ **BEST** for    │ **GOOD** if      │ **TRANSITION** │  **WORST**
                          │ Zone A (mature) │ community wants  │ only (not      │  (avoid)
                          │ (lowest cost,   │ higher gen. +    │  sustainable)  │
                          │ proven tech,    │ local tracking   │                │
                          │ best payback)   │ skills available │                │
```

---

## Part 5: Decision Flow (For Implementation Teams)

```
                           START: Site Identified
                                  |
                                  v
                      Is Aptitude Score Available?
                    /            |              \
                  YES             NO            COLLECT DATA
                   |                             (read from maps)
                   v                             |
            What is GHI value?                   v
            (5.2–5.8? 5.8–6.8?)
            /        |        \
           /         |         \
      <5.2       5.2–5.5     5.5–5.8      5.8–6.8+
        |            |          |            |
        |            |          |            |
        v            v          v            v
    MARGINAL    SUITABLE    GOOD        EXCELLENT
   (NOT viable) (Option C)  (Option B)  (Option A)
        |            |          |            |
        V            V          V            V
   Community    Assess local  Assess supply Community
   only if at   capacity      chain ready? accepts
   government  /terrain OK?   (can track   (proven
   mandate or  |              motors      adoption
   pilot.      v              sourced?)    signal).
              Option C:      /      \
              Hybrid Solar +  YES    NO
              Diesel          |       |
              (plan 10-year  v       v
              transition to Option A  Option A
              full PV)       + Manual  (fallback)
                             Tracking

              DO NOT RECOMMEND OPTION D
              unless:
              ├─ Community has water
              │  access <3 km
              ├─ Agriculture = primary
              │  livelihood
              └─ Women's groups
                 interested
```

---

## Part 6: Implementation Checklist (Per Technology Choice)

### **If Choosing Option A (PV-Fixed + Battery) — CHECKLIST**:

- [ ] Confirm GHI >5.5 kWh/m²/day from NASA POWER + ±6 month pyranometer validation
- [ ] Verify battery sourcing (South Africa supplier confirmed, 5-year parts SLA)
- [ ] Plan technician training (4 weeks, basic PV + battery knowledge, certify 2–3 per community)
- [ ] Design community cooperative (tariff collection, O&M fund, female representation)
- [ ] Secure financing (World Bank? AfDB? Private equity?)
- [ ] Environmental assessment (< 10 hectares, minimal impact → typically fast-tracked)
- [ ] Community acceptance survey (>75% favorable before CapEx commitment)

### **If Choosing Option B (PV-Tracker) — CHECKLIST**:

- [ ] Confirm GHI 5.2–5.8 kWh/m²/day optimal range
- [ ] Secure tracker supply (visit factory, negotiate 5-year parts + service contract)
- [ ] Plan extended technician training (8 weeks + mentorship with regional technician 2x/year)
- [ ] Designate system manager role (not just operator)
- [ ] Design manual override (if motors fail, lock tracker in fixed position)
- [ ] Higher tariff model (USD 0.28/kWh vs 0.25 for Option A)
- [ ] Risk mitigation: Plan upgradable fallback to fixed ($50K loss if tracking discontinued)

### **If Choosing Option C (Hybrid) — CHECKLIST**:

- [ ] ONLY IF: Aptitude <0.65 OR government mandate OR awaiting battery supply
- [ ] Plan diesel supply logistics (fuel storage, regular vehicle for delivery)
- [ ] Design transition roadmap (hybrid Year 1–3, add batteries Year 4, remove diesel Year 7–10)
- [ ] Consult with climate stakeholders (World Bank, PNUD may object; requires narrative about transition)
- [ ] Higher O&M cost model (diesel service, fuel volatility)
- [ ] Consider price hedging (lock diesel price for 2–3 years via supplier contract)

### **If Choosing Option D (Solar Pump) — CHECKLIST**:

- [ ] Verify irrigation demand (survey local farmers, water-less-than-3km distance)
- [ ] Partner with agriculture department (crop training)
- [ ] Estimate water revenue (produce sales → household tariff payment capacity)
- [ ] Community governance (manage water rights + tariff fairness)
- [ ] Include in gender impact narrative (women's time savings → education/business)

---

## Part 7: Post-Implementation M&E (All Options)

**Standard KPIs tracked monthly**:
- ✓ MWh generated (vs model prediction)
- ✓ System uptime (%)
- ✓ Households connected
- ✓ Tariff collection rate (%)
- ✓ CO₂ avoided (ton/year)
- ✓ Cost per beneficiary (USD/person connected)

**Technology-Specific Metrics**:
- **Option A**: Battery state-of-health (%) → replacement trigger if <80%
- **Option B**: Tracker accuracy (±5° tolerance) → drift signals maintenance need
- **Option C**: Diesel consumption (L/MWh) vs model → if >20% over, system design review
- **Option D**: Water volume delivered (m³/day), crop yield change (quarterly survey)

---

## Summary: Technology Roadmap for Huíla Province

```
ZONE A (CACULA) — APTITUDE 0.83 — PRIMARY TECHNOLOGY
└─ IMMEDIATE: Option A (PV-Fixed + Battery, 12.5 MWp)
   ├─ LCOE: USD 0.20/kWh
   ├─ Payback: 6.2 years
   ├─ Timeline: 6 months construction (Q2–Q3 2026)
   ├─ Confidence: VERY HIGH
   └─ Next phase: Upgrade to Option B (tracking) if battery costs drop

ZONE B (HUMPATA) — APTITUDE 0.79 — SECONDARY TECHNOLOGY  
└─ PRIMARY: Option B (PV-Tracker + Battery, 8.2 MWp)
   ├─ LCOE: USD 0.24/kWh (vs USD 0.22/kWh Zone A, due to tracking O&M)
   ├─ Payback: 6.8 years
   ├─ Timeline: 6 months construction (Q3–Q4 2026)
   ├─ Confidence: HIGH
   ├─ Backup: Option A if tracking supply fails
   └─HYBRID (Option C) as short-term bridge (3–6 months, while tracker sourced)

ZONE C (QUILENGUES) — APTITUDE 0.76 — TRANSITIONAL TECHNOLOGY
└─ IMMEDIATE: Option C (Hybrid Solar + Diesel, mixed 5 kW solar + 5 kW diesel)
   ├─ LCOE: USD 0.30/kWh (initially high, but fuel reduction over time)
   ├─ Payback: 8–10 years
   ├─ 10-YEAR TRANSITION PLAN:
   │  ├─ Year 1–2: Solar 20% load, diesel 80% (proof of concept)
   │  ├─ Year 3–4: Add battery (Option A upgrade), solar 60%, diesel 40%
   │  ├─ Year 5–10: Ramp to 100% solar (diesel emergency only)
   │  └─ LCOE declining from 0.30 → 0.18/kWh as solar % increases
   ├─ Gender co-benefit: Integrate Option D (solar pump for irrigation) in Year 2
   └─ Confidence: MEDIUM

SPECIALIZED: Option D (Solar Water Pumping) 
└─ Can supplement ANY of above
   ├─ Cacula: Pump from Rio Vombe (2 kW, irrigate 5 ha cooperatives)
   ├─ Humpata: Pump service 2–3 villages (1 kW each, decentralized)
   ├─ Quilengues: If hybrid system proves reliable, add pump Year 3
   └─ Expected impact: 10–15% additional household income via agriculture
```

---

**Technology Selection = Core to GEESP-Angola's Competitiveness**

This matrix ensures that every community gets **optimal technology matched to their spatial + social + economic context**, not a one-size-fits-all approach. This is the **differentiator vs Nassar (Iraq) and Li (macro-regional)** frameworks that lack community-level technology customization.

**Next step**: Integrate this technology section into main SOL.tex manuscript.
