# Skill Tutorial 06 — Drilling Fluids

> **Applies to:** Drilling engineers (CORE), completions engineers (HIGH), HSE engineers (MEDIUM for environmental aspects)
> **ISPTEC connection:** Fluidos de Perfuração e Completação, Engenharia de Poços
> **Goal:** Understand drilling fluid types, composition, rheological properties, solids control, environmental regulations, and troubleshooting. Be able to read a daily mud report and discuss mud selection with a drilling fluids engineer.

---

## Part 1: The Seven Functions of Drilling Mud

Drilling fluid does more than just "lubricate the bit." Every function is critical:

1. **Control formation pressure:** Hydrostatic pressure of the mud column keeps formation fluids out of the wellbore (primary well control barrier)
2. **Transport cuttings to surface:** Cuttings created by the bit must be carried up the annulus by the mud and removed at surface
3. **Suspend cuttings and weighting material:** When circulation stops (during a connection), cuttings and barite must not settle to the bottom (this would cause stuck pipe and the well to lose pressure)
4. **Cool and lubricate the bit and drill string:** High temperatures at the bit (friction, formation temperature) are managed by the circulating fluid
5. **Provide information:** Mud returns carry cuttings that tell you about the formation being drilled; mud logging analyzes gas in the returns
6. **Protect the formation:** Minimize invasion of mud filtrate into productive zones; prevent clay swelling
7. **Support the borehole wall:** Mud pressure and filter cake formation provide physical support to the borehole wall

---

## Part 2: Drilling Fluid Types

### Water-Based Mud (WBM)

**Base:** Fresh water, seawater, or salt water

**Composition:**
- Base fluid (water)
- **Bentonite clay:** Provides viscosity and filter cake
- **Barite (BaSO₄):** Heavy mineral used to increase mud weight (density up to 2.68 SG)
- **Chemical additives:** Polymers (viscosifiers, fluid loss reducers), inhibitors, pH control chemicals

**Types of WBM:**
- **Freshwater gel (bentonite/water):** Simple, cheap, used in surface hole sections
- **KCl-polymer mud:** Potassium chloride inhibits clay swelling. Used in shale sections.
- **Seawater-based:** Used in deepwater where freshwater is expensive to transport
- **High-performance WBM (HPWBM):** Modern WBMs with excellent inhibition — approaching OBM performance at lower environmental impact

**Advantages of WBM:**
- Cheaper than OBM
- Easier to manage
- Environmentally preferred — discharge to sea may be allowed (with proper treatment)
- No contamination of hydrocarbon zone analysis

**Disadvantages:**
- Poor performance in highly reactive clays (clay swelling, wellbore instability)
- Higher torque/drag than OBM
- Limited thermal stability at very high temperatures

### Oil-Based Mud (OBM) and Synthetic-Based Mud (SBM)

**Base:** Diesel oil (OBM), mineral oil, or synthetic fluids (SBM) — also called invert emulsion mud

**Composition:**
- Base oil (continuous phase)
- Water (internal/dispersed phase — typically 20–30% by volume)
- **Emulsifiers:** Keep oil-water emulsion stable
- **Organophilic clay / polymers:** Provide viscosity in the oil phase
- **Lime (CaO):** Controls pH and provides alkalinity
- **Barite:** Weight material
- **Oil/water ratio (O/W ratio):** Expressed as 80/20, 75/25, etc. — higher oil = better inhibition

**Key advantages of OBM/SBM:**
- **Excellent borehole stability:** Oil inhibits clay swelling and shale hydration
- **Lubricity:** Much lower torque and drag than WBM — critical in long deviated wells
- **High temperature stability:** Can drill at 200°C+
- **Gas hydrate inhibition:** In deepwater drilling, OBM reduces hydrate risk

**Disadvantages:**
- More expensive (especially SBM)
- **Environmental regulations:** OBM cuttings cannot be discharged to sea. Must be collected and transported to shore for treatment/disposal.
- Gas shows are harder to detect in OBM (gas solubility in oil is higher)
- Formation evaluation: OBM filtrate invades the formation, affecting resistivity log interpretation

**Angola drilling context:** Angola's deepwater wells (Blocks 17, 32, 31) predominantly use SBM for the reservoir and intermediate sections. WBM is used for the shallower conductor and surface sections.

---

## Part 3: Rheological Models and Why They Matter

Rheology = the study of how fluids flow under stress. For drilling mud, rheology determines:
- Can the mud carry cuttings in the annulus? (annular velocity + rheology)
- Will cuttings settle when circulation stops? (gel strength)
- What pump pressure is needed? (friction losses = function of rheology)

### Key Rheological Parameters

**Mud Weight (MW):** Density in kg/L or ppg. The most fundamental parameter. Controls hydrostatic pressure.

**Plastic Viscosity (PV):** Resistance to flow at high shear rates (like in the drill string). Measured in cP. High PV = thick mud = high pump pressure. PV is largely controlled by solids content.

**Yield Point (YP):** The additional stress needed to initiate flow (like breaking static friction). Measured in lb/100ft² or Pa. High YP = good cuttings carrying capacity.

**Gel Strengths (10-sec and 10-min):** The static gel strength that builds when mud is not circulating. Essential for suspending cuttings during connections. If gel strength is too high, restarting circulation requires very high pressure (risk of fracturing formation).

**HTHP Filtration:** Fluid loss through the mud filter cake under high temperature (121°C+) and high pressure (500 psi differential). Low HTHP filtration = thin filter cake = formation protection.

**Low Gravity Solids (LGS):** Clay and drilled solids with density < 3.0 SG. These increase PV and YP but add no density value. Must be controlled by solids control equipment.

### The Bingham Plastic Model

The most commonly used model for field calculations:

$$\tau = PV \cdot \dot{\gamma} + YP$$

Where $\tau$ = shear stress (lb/100ft²) and $\dot{\gamma}$ = shear rate (1/s).

This is a simplified model valid for moderate-viscosity muds.

### The Power Law Model

For better accuracy in annular hydraulics:

$$\tau = K \cdot \dot{\gamma}^n$$

Where $K$ = consistency index and $n$ = flow behavior index (n < 1 for shear-thinning fluids like drilling mud — they thin when pumped fast, good for hydraulics).

### The Herschel-Bulkley Model

Combines yield point with power law:

$$\tau = \tau_y + K \cdot \dot{\gamma}^n$$

Most accurate model for modern mud systems, especially in software calculations.

---

## Part 4: Solids Control — The Key to Economic Drilling

Drilled cuttings must be removed from the mud immediately. Every particle of low-gravity solid (LGS) that remains in the mud:
- Increases plastic viscosity (higher pump pressures, more energy)
- Increases mud weight (potential overbalance, risk of fracturing weak formations)
- Reduces penetration rate (bits cannot drill efficiently in viscous mud)
- Increases equipment wear

**Solids control equipment sequence (mud flows through these in order):**

```
ANNULUS RETURNS
     │
  SHALE SHAKERS ← Primary solids removal. Vibrating screens separate cuttings > 74 microns
     │
  DEGASSER ← Removes gas entrained in the mud (from a kick or gas-cut mud)
     │
  DESANDER ← Hydrocyclones. Removes sand-size particles 40–74 microns
     │
  DESILTER ← Hydrocyclones (smaller). Removes silt-size particles 15–40 microns
     │
  CENTRIFUGE ← Removes colloidal particles and barite recovery
     │
  ACTIVE MUD PITS ← Treated mud recycled to pumps
```

**Shale shaker screen selection:** API screen mesh size. Finer mesh = more solids removed, but slower throughput. For Angola deepwater (mostly SBM): 200–325 mesh screens typically used.

---

## Part 5: Mud Weight Adjustment

### Adding Barite to Increase Mud Weight

If you need to increase mud weight (e.g., approaching a high-pressure zone), you add barite (BaSO₄, SG = 4.20).

**Amount of barite to add per 100 bbl of mud:**

$$\text{Barite to add (sacks)} = \frac{1490 (MW_f - MW_i)}{35 - MW_f}$$

Where $MW_f$ = final mud weight (ppg) and $MW_i$ = initial mud weight (ppg), 1 sack = 100 lb.

**Example:** Current MW = 12.5 ppg. Need to increase to 13.0 ppg.

$$\text{Barite} = \frac{1490(13.0 - 12.5)}{35 - 13.0} = \frac{745}{22} = 33.9 \text{ sacks per 100 bbl}$$

---

## Part 6: Lost Circulation — The Other Major Problem

**What it is:** The reverse of a kick. Mud flows INTO the formation (into fractures, vugs, or highly permeable zones) instead of being returned to surface. You "lose" mud.

**Signs:**
- Return flow rate drops below pump rate (partial loss)
- Return flow ceases entirely (total loss)
- Pit volume decreases
- Pump pressure may drop (less resistance in annulus)

**Types:**

| Type | Cause | Severity |
|------|-------|----------|
| Seepage loss | High permeability formation (>1,000 mD) | Mild — <10 bbl/hr. Continue with reduced mud weight or LCM treatment. |
| Partial loss | Fractured or vuggy formation | Moderate — 10–100 bbl/hr. LCM treatment required. |
| Severe loss | Natural fractures opened by ECD | High — 100–500 bbl/hr. Stop drilling. Spot LCM pill. |
| Total loss | Complete fracture or cavern | Critical — no returns. Drill blind? Spot cement. Major NPT event. |

**LCM (Lost Circulation Material) Pills:**

A concentrated slug of LCM is mixed and pumped down to the loss zone. LCM types:

| LCM Type | Material | Best For |
|----------|----------|---------|
| Fibrous | Cane fiber, walnut hull | Seepage loss |
| Flake | Cellophane, mica | Fracture bridging |
| Granular | Calcium carbonate, ground nut shells | Vuggy formation |
| High-filter-loss pill | Graphite + calcium carbonate blend | Fracture plugging |
| Cement | Neat cement or micro-cement | Severe/total loss (permanent seal) |

**Dual Gradient Drilling:** In some Angola deepwater wells, the riser is filled with seawater instead of mud (seawater-based returns). This reduces the hydrostatic head at the seabed, preventing fractures while still allowing heavier mud below the seabed. Experimental but under evaluation for future deep pre-salt wells.

---

## Part 7: Environmental Regulations in Angola

### Decreto Executivo n.º 97/19 — Environmental Management in the Petroleum Sector

Angola's primary environmental regulation for the oil and gas industry. Key requirements for drilling:

**Cuttings disposal:**
- OBM/SBM cuttings: **Cannot be discharged to sea**. Must be:
  - Collected in cuttings skips on the drillship
  - Transported to shore
  - Treated at an ANPG-licensed treatment facility (thermal desorption or bioremediation)
  - Annual disposal volumes must be reported to ANPG

**Drilling fluid discharge:**
- WBM discharges to sea may be permitted if oil contamination < 1% by weight
- OBM/SBM base fluid: strict limits (no free oil visible on sea surface)

**Mud pit monitoring:**
- Regular sampling and analysis of active mud system
- Documentation of all additives used
- Mass balance of cuttings volume vs formation volume drilled

**Chemical inventory:** All chemicals used must be on the approved ANPG list. Environmentally harmful chemicals (e.g., mercury-containing biocides, certain heavy metals) are prohibited.

**Drill water (cuttings washing water):** Must be treated before discharge. Oil content < 15 mg/L.

---

## Part 8: Reading a Daily Mud Report (DMR)

On any drilling rig, the mud engineer produces a Daily Mud Report every morning. As a drilling engineer, you need to read and understand it.

**Key parameters on a standard DMR:**

```
DATE: 15 April 2026
WELL: Block 32 Well A-7
DEPTH: 4,185m MD / 3,920m TVD
HOLE SECTION: 8½" Production Hole
FLUID TYPE: SBM (Synthetic Based Mud)
O/W RATIO: 80/20 (oil/water)

DENSITY (MUD WEIGHT): 1.62 kg/L   TARGET: 1.60-1.65 kg/L ✓
FUNNEL VISCOSITY: 55 sec/qt        TARGET: 45-65 sec/qt ✓

RHEOLOGY (FANN 35 READINGS):
  600 RPM: 102    300 RPM: 65
  Plastic Viscosity (PV): 37 cP   TARGET: <45 cP ✓
  Yield Point (YP): 28 lb/100ft²  TARGET: 20-30 lb/100ft² ✓
  Gel 10-sec: 8 lb/100ft²
  Gel 10-min: 14 lb/100ft²

HTHP FILTRATION (150°C, 500 psi): 4.2 mL/30min   TARGET: <6.0 mL ✓
ELECTRICAL STABILITY: 580 V   TARGET: >400 V (SBM emulsion quality) ✓
MBT (METHYLENE BLUE TEST): 4.0 lb/bbl   (monitors LGS and reactive solids)
CHLORIDES: 85,000 mg/L   (monitors water phase — consistent with formulation)

LOW GRAVITY SOLIDS (LGS): 6.2%   TARGET: <7% ✓
HIGH GRAVITY SOLIDS (HGS / BARITE): 22.1%

DAILY BARITE ADDED: 48 sacks   TOTAL VOLUME: 1,250 bbl active pit
```

**What raises flags:**
- MBT rising → contamination with reactive clays from formation
- LGS rising → centrifuge not working effectively, solids building up
- Electrical stability dropping → SBM emulsion breaking down (water washing)
- PV rising → excess solids, viscosity too high for good hydraulics
- HTHP filtration high → filter cake thick, formation damage risk

---

## Part 9: HPHT Drilling — Angola's Deepest Wells

Angola's pre-salt reservoirs (discovered in some Block 32 prospects, and in deeper pre-salt plays under evaluation) can be HPHT (High Pressure, High Temperature): reservoir pressure > 690 bar (10,000 psi) and temperature > 150°C.

**Challenges for drilling fluids:**

- **Thermal stability:** Standard OBM emulsifiers degrade above 180°C. Specially formulated HPHT mud systems required.
- **Pressure-density relationship:** Mud density increases with pressure (compressibility) and decreases with temperature. In HPHT wells, the variation in mud density with depth is significant — must model density profile carefully.
- **HTHP filtration:** Standard WBM filter cakes are not stable at HPHT. Use synthetic polymers (AMPS copolymers, sulfonated asphalt) for filtration control.
- **High ECD management:** HPHT wells typically have very tight PP/FG windows. MPD is often essential.

---

## Exercises — Drilling Fluids

**Exercise 1: Cuttings Transport**
A 12¼" hole is drilled at 60 RPM with 5" drill pipe. Pump flow rate = 1,200 L/min. Annular capacity between 12¼" hole and 5" pipe = 0.0489 bbl/m.

Calculate:
1. Annular velocity in m/min
2. If cuttings have settling velocity of 4 m/min in the mud, will cuttings be transported to surface? (Transport efficiency > 1.0 = adequate)

**Exercise 2: Mud Weight Increase**
You are drilling at 3,500m TVD with 11.2 ppg mud. A kick warning is noted — you increase mud weight to 11.8 ppg as a precaution. Active mud volume = 600 bbl.

Calculate:
1. Barite sacks required (use: $\text{Barite (sks/100bbl)} = \frac{1490(MW_f - MW_i)}{35 - MW_f}$)
2. Volume increase due to barite addition (barite volume = mass / density; barite SG = 4.20)

**Exercise 3: Hydrostatic Pressure**
An SBM system has density 1.62 kg/L at surface conditions. Due to HPHT effects, the density at 4,000m TVD is 1.68 kg/L (compressibility effect). Calculate:
1. HP at 4,000m TVD using surface density
2. HP at 4,000m TVD using downhole density
3. The difference in psi — why does this matter for HPHT well control?

**Exercise 4: Environmental Compliance**
A 12¼" hole section is drilled from 2,800m to 3,500m in SBM (700m section). Bit size = 12.25" (0.311m diameter). Estimated cuttings volume = π/4 × D² × length × porosity of formation = 40m³ of rock cuttings. Each cuttings skip holds 2 m³. How many cuttings skips must be rigged up and transported to shore for this section?

---

## Interview Questions — Drilling Fluids

1. Why is SBM preferred over WBM for Angola deepwater intermediate and production sections?
2. You are reviewing the morning mud report. PV has increased from 28 cP to 41 cP overnight. What are the possible causes and what action do you recommend?
3. What is electrical stability in OBM/SBM and what does a low reading tell you?
4. A Block 17 well is experiencing partial lost circulation (25 bbl/hr) while drilling a 12¼" section. What LCM pill would you design and how would you spot it?
5. Explain the impact of ANPG's cuttings disposal regulations on rig operations and cost.
6. What is the difference between Plastic Viscosity (PV) and Yield Point (YP)? Which parameter most affects cuttings carrying capacity?
7. A well is being drilled with 1.55 kg/L mud at 3,200m TVD. The formation water salinity is 120,000 mg/L chlorides. What is the expected mud contamination risk and how would you detect it on the DMR?
8. What is the O/W ratio in an OBM/SBM system and how does it affect mud performance?

---

*Next: [07_HSE_Offshore_Tutorial.md](07_HSE_Offshore_Tutorial.md) | See also: [02_Drilling_Fundamentals_Tutorial.md](02_Drilling_Fundamentals_Tutorial.md)*

### Dilution to Reduce Mud Weight

If mud weight is too high, dilute with base fluid (water for WBM, base oil for OBM). This also reduces LGS concentration.

---

## Part 6: Lost Circulation

**Lost circulation** = drilling fluid flows into the formation instead of returning to surface. The mud column height drops. Hydrostatic pressure decreases. Risk of a kick.

**Types:**
- **Seepage losses:** < 10 bbl/hr. Usually manageable with LCM pills.
- **Partial losses:** 10–100 bbl/hr. Significant. Requires LCM treatment.
- **Total losses:** No returns. Catastrophic. May require cement squeezes.

**Lost Circulation Materials (LCMs):**
- **Bridging materials:** Nut shells, calcium carbonate, graphite platelets — bridge across fractures
- **Fibrous materials:** Cellulosic fibers — strengthen the bridge
- **Flaky materials:** Graphite, cellophane — seal small voids
- **Cement squeezes:** For total losses — cement pumped into the loss zone and allowed to set

**Prevention:** In Angola's narrow-pressure-window wells, precise ECD management is critical. Too high ECD = lost circulation. Too low = kick.

---

## Part 7: Completion Fluids

When drilling into the reservoir section and during the completion phase (running tubing, perforating), special fluids are used:

**Requirements:**
- Must not damage the formation (no solids, filtered to < 2 micron)
- Must provide the required overbalance to prevent flow
- Must be compatible with formation fluids (no scale precipitation)

**Completion fluid types (clear brines):**

| Fluid | Max Density (SG) | Notes |
|---|---|---|
| NaCl (sodium chloride) | 1.20 | Cheapest. Used for low-pressure reservoirs. |
| KCl (potassium chloride) | 1.16 | Clay-inhibiting. Common. |
| CaCl₂ (calcium chloride) | 1.40 | Medium-density completions. |
| CaBr₂ (calcium bromide) | 1.82 | High-pressure reservoir completions. Expensive. |
| ZnBr₂ blends | 2.30+ | Ultra-high-pressure. Zinc is toxic — special handling. |

**Note:** OBM is NOT used as a completion fluid. The oil phase would create an oil-wet filter cake in the reservoir pores that is very difficult to clean up and would damage productivity. Always switch to clean brine completion fluid before perforating.

---

## Part 8: ANPG Environmental Regulations for Drilling Fluids

Angola's deepwater drilling occurs in an environmentally sensitive marine environment. ANPG (and international standards like OSPAR) regulate:

- **Cuttings discharge:** WBM cuttings may be discharged to sea (within concentration limits). SBM cuttings MUST be collected and returned to shore. Each Angola deepwater rig has cuttings handling and storage equipment.
- **Mud discharge:** Small volumes of WBM slurry may be discharged after treatment. OBM/SBM cannot be discharged.
- **Fluid loss to formation:** Excessive fluid loss to reservoir = formation damage = reduced production. Good mud design protects reservoir productivity.
- **Biodegradability:** SBM must use synthetic base fluids with tested biodegradability. Diesel OBM is banned in Angola deepwater.

---

## Part 9: Practice Exercises

**Exercise 1:** Mud weight is 1.45 kg/L. You need to increase it to 1.55 kg/L. You have 200 bbl of mud in the active system. How many 100-lb sacks of barite do you need? (Convert to ppg first: 1.45 kg/L × 8.33 = 12.08 ppg)

**Exercise 2:** A driller reports that ROP has decreased significantly and pump pressure is rising. The Plastic Viscosity has increased from 18 cP to 34 cP over 24 hours. Diagnose the problem and describe the treatment.

**Exercise 3:** Draw the complete solids control equipment train for a deepwater SBM system. For each piece of equipment, state: what it removes, how it works, and the approximate cut point in microns.

**Exercise 4:** You are designing the completion fluid for an Angola deepwater reservoir at 4,200m TVD with pore pressure = 720 bar. What minimum density completion fluid do you need? (Calculate in both ppg and SG.) What fluid type would you choose?

---

## Part 10: Study Resources

| Resource | Format | Notes |
|---|---|---|
| "Drilling Fluids Technology" — Azar & Samuel | Textbook | Comprehensive drilling fluids reference |
| API RP 13B-1 / 13B-2 | Standard | Field testing procedures for WBM and OBM |
| M-I SWACO (SLB) Drilling Fluids Engineering Manual | PDF | Industry's most used mud engineering reference |
| Halliburton Drilling Fluids Manual | PDF | Available on request from Halliburton Angola |
| "Fundamentals of Drilling Engineering" — SPE Textbook | Textbook | Chapter on fluid hydraulics |
| PetroWiki (SPE) — Drilling Fluids section | Online/Free | Excellent technical summary of all mud topics |
| LinkedIn Learning: "Introduction to Drilling" | Video | Visual explanation of mud systems |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/01_Drilling_Path.md](../paths/01_Drilling_Path.md)*  
*Where to learn: [PetroWiki](https://petrowiki.spe.org/Drilling_fluids) | [Drillingformulas.com](https://drillingformulas.com) | [Learning Resources](../../../docs/learning-resources.md)*
