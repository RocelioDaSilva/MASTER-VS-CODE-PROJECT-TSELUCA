# Engenharia de Poços + Fluidos de Perfuração — Applied to Angola Deepwater
## From Casing Design Equations to Block 32 Wells

---

## Why These Two Subjects Form One Professional Package

You cannot design a well without knowing the mud system, and you cannot design the mud system without knowing the casing programme. Engenharia de Poços and Fluidos de Perfuração e Completação are taught separately at ISPTEC but are executed together in industry by the same drilling engineering team.

A drilling engineer at TotalEnergies Angola, working on a Block 32 development well, uses both subjects simultaneously every day.

---

## Part 1: Engenharia de Poços Applied

### Pore Pressure and Fracture Gradient: The Foundation of Everything

Before designing a single casing string, the drilling engineer must understand the pressure environment the well will be drilled through. This is the pore pressure / fracture gradient (PP/FG) window.

**Pore pressure (PP):** The pressure of the fluid inside the pore space of the formation. In normally pressured formations, PP = 0.435 psi/ft (hydrostatic gradient of seawater). Overpressured formations have PP > 0.435 psi/ft — meaning a greater mud weight is needed to control the well.

**Fracture gradient (FG):** The pressure at which the formation rock fractures, allowing drilling fluid to be lost. Defines the maximum safe mud weight.

**The mud weight window:**
$$PP < \rho_{mud} \times 0.052 \times TVD < FG$$

If the window is narrow (< 0.5 ppg wide), drilling becomes extremely difficult — the mud weight that prevents a kick may simultaneously cause lost circulation. This is a critical Angola deepwater challenge.

**Angola Block 32 context:** The sub-salt interval (reaching the target reservoir below a thick salt layer) has particularly challenging pressure gradients:
- Above salt: normally pressured (8.5–9.0 ppg mud weight)
- Top of overpressure (often just below salt): sudden increase to 13–15 ppg
- Maximum overpressure at reservoir: up to 17–18 ppg
- Fracture gradient at same depth: 18–19 ppg

Window = 1–2 ppg. Requires precise control of mud weight and ECD (Equivalent Circulating Density).

**How PP/FG is used:**
1. Obtained from offset well data (pore pressure measurements from MDT/RFT tests, LOT data, events database)
2. Modelled using geomechanics software (Landmark Drillworks, Baker Hughes JewelSuite)
3. Used to place casing shoes: each casing shoe must be deep enough to allow drilling the next section without exceeding PP/FG constraints

---

### Casing Programme Design: Angola Deepwater Example

Your ISPTEC subject covers burst, collapse, and tension calculations. Here is how a real casing programme is built for an Angola deepwater development well.

**Example well: Block 32 development producer**
- Water depth: 1,800m
- TD: 5,400m TVD (reservoir top at 5,100m)
- Max pore pressure: 17.2 ppg at TD
- Fracture gradient at shoe of each interval: see design below

```
ANGOLA DEEPWATER CASING SCHEME

Sea surface
│
│  1,800m water
│
Seabed ─────────────────────────────
│
│  36" Conductor
│  Driven to ~80m below seabed (jet driven in soft Angola seabed)
│
│  26" Surface hole / 20" Surface casing to ~600m BML
│  Set at ~600m below mudline (below shallow hazard zone)
│  Cemented back to mudline
│  Purpose: Establish well integrity, protect shallow formations,
│           provide BOP anchoring point
│
│  17.5" Intermediate hole / 13⅜" Intermediate casing to ~2,800m
│  Set before entering the overpressure zone
│  Provides pressure integrity for deeper drilling with heavier mud
│
│  12.25" Hole / 9⅝" Production casing to ~5,100m
│  Drilled with OBM (18 ppg mud weight through overpressured section)
│  Set at reservoir top
│  This is the well's primary hydraulic seal
│
│  8.5" Hole / 7" Production liner from 5,000m to 5,400m TD
│  Drilled through the reservoir with balanced/slightly overbalanced OBM
│  Sand control completion (gravel pack) installed in liner
│
│ ████████████████████████████████ RESERVOIR (5,100m–5,400m TD)
```

**Casing design calculations (as taught in Engenharia de Poços):**

*Burst pressure (internal pressure that could cause the casing to burst outward):*
$$P_{burst} = P_{pore} \times SF_{burst}$$
SF = 1.10 (10% safety factor, per Shell/NORSOK standards)

*Collapse pressure (external pressure that could cause the casing to collapse inward):*
$$P_{collapse} = \rho_{mud} \times 0.052 \times TVD \times SF_{collapse}$$
SF = 1.00–1.10 (depends on fluid level inside casing during cementing)

*Tension (axial load from weight of casing string):*
$$T_{hook} = \sum W_{casing} + \text{buoyed weight in mud}$$
Must not exceed 80% of pipe body yield strength.

**Grade selection for a 9⅝" production casing string, 5,100m depth in Angola:**
- Required burst resistance: (8,900 psi pore pressure) × 1.1 = 9,790 psi
- Required collapse resistance: (17.2 ppg × 0.052 × 5,100 × 3.281) = needs full calculation in metric
- Grade P-110, 47 ppf: burst rating 9,970 psi ✓, collapse rating 8,800 psi — check against collapse requirement

This calculation is done in well planning software (Landmark WellPlan, SLB Well Engineering Toolbox) but you must understand the method to verify software output and identify errors.

---

### Wellbore Stability and Geomechanics

**Mecânica das Rochas** (taught in Year 4) directly connects here. Borehole stability analysis determines the safe mud weight window considering not just pore pressure but also the mechanical strength of the rock.

**Two failure modes:**
1. **Shear failure (wellbore collapse):** If mud weight is too low relative to formation strength, the wellbore walls shear inward. Signs: increased mud weight in returns, stuck pipe, tight spots on wiper trips.
2. **Tensile failure (lost circulation):** If mud weight too high, hydraulic fracturing opens tensile fractures. Signs: drop in return flow rate, increase in pit level, lost mud.

**Minimum mud weight for stability (Mogi-Coulomb criterion):**
$$MW_{min} = \frac{(3\sigma_H - \sigma_h) - 2P_p + q_{UCS}}{(1 + 2.31)} \times \frac{1}{0.052 \times TVD}$$

Where σH = maximum horizontal stress, σh = minimum horizontal stress, UCS = unconfined compressive strength of the rock (measured from cores — your Mecânica das Rochas lab).

In practice, the geomechanics engineer provides a stability mud weight window to the drilling engineer, who designs the mud programme to stay within this window.

---

### Directional Drilling and Survey Calculations

Your ISPTEC subject covers inclination, azimuth, and the minimum curvature method for survey calculation. Here is the industry workflow.

**A development well on Block 32** is typically a complex well with:
- Vertical section from seabed through the salt
- Build section: inclination increases from 0° to 60–75° over 300–500m (using a mud motor or RSS)
- Tangent section at 60–70° inclination, approaching the reservoir target
- Reservoir section: horizontal or near-horizontal across the pay zone

**Minimum curvature survey calculation** (as you learned in ISPTEC):
$$\Delta N = \frac{\Delta MD}{2}\left(\cos I_1 \cos A_1 + \cos I_2 \cos A_2\right) \times RF$$

Where:
$$RF = \frac{2}{\Delta MD}\tan\left(\frac{\beta}{2}\right)$$
And β is the total angle change between survey stations.

This calculation is done by MWD/surveying software in real-time at the rig site, and by the directional driller and drilling engineer. You need to understand it to:
- Verify the well is on trajectory
- Calculate the well-to-well distance (for collision avoidance — critical when 15 wells are drilled from a single FPSO)
- Determine the true vertical depth (TVD) for converting measured depth (MD) to TVD

**Anti-collision:** A critical safety discipline in multi-well subsea developments. Every new well drilled must be modelled against all existing wellbores to ensure the drill string does not collide with a nearby production well. This uses 3D trajectory calculations at the heart of your directional drilling module.

---

### Hydraulics Programme

**What ISPTEC taught:** Equivalent circulating density (ECD), annular pressure loss calculations, surge and swab pressures.

**How industry uses it:** The hydraulics programme is a mandatory deliverable before spudding any Angola well. It specifies:

1. Bit pressure loss: $\Delta P_{bit} = \frac{\rho V^2}{1120 C_d^2}$ (nozzle pressure loss)
2. Annular pressure loss: Bingham plastic model or power law model for OBM
3. ECD: $ECD = MW_{static} + \frac{\Delta P_{annular}}{0.052 \times TVD}$

**Critical ECD management in Angola:**
The narrow mud weight window (1–2 ppg in some sections) means that the ECD (mud weight during circulation) must be carefully controlled:
- If ECD > FG: lost circulation during drilling
- If static MW < PP: kick when pumps are off (e.g., during connections)

This is why **managed pressure drilling (MPD)** is used on some Angola sub-salt wells — a technology that controls the surface backpressure to maintain constant bottomhole pressure regardless of whether the pumps are running.

---

## Part 2: Fluidos de Perfuração Applied

### The Mud Programme: A Well-by-Well Document

For every Angola well, a mud programme document is prepared before spudding. This is not optional — ANPG requires it. The document specifies:
- Mud type for each hole section
- Target mud weight for each section
- Rheological properties (PV, YP, gels)
- Fluid loss control requirements
- Chemical treatment plan
- Environmental disposal requirements (OBM cutting handling per ANPG Decreto 97/19)

**Typical Angola deepwater mud programme:**

| Section | Hole Size | Mud Type | MW (ppg) | Rationale |
|---------|-----------|---------|---------|-----------|
| Conductor/Surface | 26" | Seawater/gel sweep | 8.6 | Shallow, unconsolidated, no pressure concerns |
| Intermediate | 17.5" | KCl/polymer WBM | 9.0–10.5 | Cost-effective, compatible with formations |
| Deeper intermediate | 12.25" | SBM (IO) | 13.0–15.5 | Enter overpressure zone; WBM inadequate |
| Production liner | 8.5" | SBM (IO) | 16.0–17.5 | Deep overpressure; reservoir section |

**Why OBM/SBM is used in Angola deepwater:**
- Salt sections drill poorly in WBM (salt dissolves into WBM, causing washout and instability)
- Overpressured shales absorb water from WBM, swelling and closing the wellbore
- OBM/SBM provides excellent hole stability in challenging formations
- Angola's regulatory framework allows OBM cuttings to be brought to shore for disposal (not discharged subsea)

---

### Rheology in Practice: Bingham Plastic Model

**ISPTEC taught:** Bingham plastic model, power law model, Herschel-Bulkley.

**Industry use:** The Bingham plastic model is the most widely used because it uses only two parameters: Plastic Viscosity (PV) and Yield Point (YP), which are measured directly with a Fann 35 viscometer on the rig.

$$\tau = YP + PV \times \dot{\gamma}$$

**Annular velocity requirement (OBM, Angola deepwater):**

Minimum annular velocity to lift cuttings: 
$$V_{min} = \frac{0.85 \times D_h \times MW}{d_{bit} \times MW_{cutting}}$$

Typical: 120–180 ft/min annular velocity for Angola deepwater wells with heavy OBM and large hole sections.

**Gel strengths:** The initial gel strength (read at 10 seconds) and final gel strength (read at 10 minutes) on the Fann viscometer tell you:
- Is the mud progressive gelling? (Bad — progressive gels cause swabbing on trips)
- Are the gels flat? (Good — shear thinning with flat gels means easy pump restart)
- Typical Angola SBM target: 10-sec gel = 5–15 lb/100ft², 10-min gel = 8–20 lb/100ft²

---

### Solids Control: The Circuit on Every Angola Drillship

**ISPTEC taught:** Shale shaker, desander, desilter, decanting centrifuge functions and cut points.

**Industry context:** On an Angola drillship (e.g., Seadrill West Saturn or Ocean BlackLion operating on Block 32), the solids control system processes 500–1,500 gallons per minute of returning mud continuously. Poor solids control degrades the expensive OBM and increases waste volume.

**Full solids control train for Angola OBM:**

```
Drill bit → Cuttings in mud → Annulus → Seabed riser → 
DRILLSHIP
│
├── Shale shakers (primary) — 4–6 units
│   Remove cuttings > 74 μm (200 mesh screens)
│   OBM-coated cuttings → cuttings dryer → skip for shore disposal
│
├── Mud cleaner (fine shaker + hydrocyclone)
│   Removes ultra-fine solids > 25 μm
│
├── Decanting centrifuges — 2–3 units (barite recovery mode)
│   Recover expensive barite from fine solids
│   Low gravity solids: discard
│   Barite (high SG): return to active mud
│
└── Active mud system
    Properly treated OBM back to pumps
```

**MBT (Methylene Blue Test):** The key test for drill solids contamination in OBM. High MBT means reactive clay solids are building up — degrading rheology and increasing mud cost. Regular MBT testing is part of the daily mud report.

**Barite addition calculation:**
$$V_{add} = \frac{V_{sys}(\rho_2 - \rho_1)}{(SG_{bar} \times 8.34 - \rho_2)}$$

Where ρ₁ = initial mud density, ρ₂ = target density, SG_barite = 4.2. This calculation is done by the mud engineer every time a density increase is needed.

---

### Lost Circulation Materials (LCM) and Events

**Angola deepwater LCM scenarios:**

| Formation | LCM Type | Material | Rate |
|-----------|---------|---------|------|
| Salt section | Preventative squeeze | Fine-medium carbonates | Continuous 10–20 ppb in mud |
| Weak carbonate stringers | Severe lost circ. | Mica flakes + nut shells + graphite | LCM pill, 30–50 ppb |
| Natural fractures sub-salt | Total losses | Fibre + granular blend | Whole mud pills |
| Aquifer stringers | Controlled losses | Cement squeeze | Sidetrack may be required |

**ANPG environmental note:** LCMs used in water-based mud sections must be non-toxic and biodegradable per ANPG environmental regulations (Decreto 97/19 on offshore waste management).

---

## The Well Programme Document

Every Angola development well is executed against a **Well Programme** — typically a 200–400 page engineering document that contains:

```
WELL PROGRAMME CONTENTS

1. Well objectives and targets
2. Trajectory design and anti-collision analysis
3. Geology and pore pressure prediction
4. Casing programme (sizes, grades, depths, cementing)
5. Mud programme (fluid type, density, rheology targets by section)
6. Hydraulics programme (pump rates, ECD, bit nozzle design)
7. BHA programme (drill collars, stabilisers, MWD/LWD, RSS)
8. Bit programme (bit type and size for each section)
9. Cementing programme (slurry design, volume, WOC time)
10. Completion design (perforations, sand control, DHSV)
11. HSE — major hazard register for this specific well
12. Cost estimate (AFE — Authority for Expenditure)
13. Schedule (days vs depth curve)
14. Contingency plans (for kick, lost circulation, stuck pipe)
```

**Your goal:** Understand each section of the well programme. By Year 3 of your career as a drilling engineer at SLB or Halliburton, you should be able to draft sections of this document independently.

---

## ANPG Regulatory Requirements for Drilling in Angola

Every well drilled in Angola requires ANPG approval. Key regulatory requirements that directly affect the drilling and fluids programme:

1. **Well design approval:** The well programme must be submitted to ANPG before spudding. Any changes during drilling require notification.
2. **Mud system reporting:** Daily drilling reports must include mud weight, rheology, and fluid losses. These are submitted to ANPG.
3. **Cuttings disposal:** OBM cuttings cannot be discharged to sea. They must be collected and transported to shore for approved disposal. Cuttings dryers and cuttings boxes are mandatory on all Angola drillships.
4. **Well control procedures:** ANPG requires a documented well control programme, tested crew (IWCF/OPITO certified), and functioning BOP system before drilling.
5. **Blowout reporting:** Any well control incident must be immediately reported to ANPG.

---

## Exercises Bridging ISPTEC to Angola Wells

### Exercise 1: Casing Shoe Depth Selection
An Angola well has the following PP/FG profile:
- 0–600m BML: PP = 8.6 ppg, FG = 14.0 ppg
- 600–2,800m: PP = 8.6–10.5 ppg (normal to slight overpressure), FG = 13.5 ppg
- 2,800–4,200m: PP = 10.5–15.0 ppg (significant overpressure), FG = 15.5 ppg
- 4,200–5,400m: PP = 15.0–17.2 ppg (reservoir section), FG = 18.0 ppg

Design a 4-string casing programme (conductor, surface, intermediate, production) with shoe depths, and specify the required mud weight for each section.

### Exercise 2: ECD Calculation
A 12.25" hole section is being drilled with OBM at 10.5 ppg static mud weight. Annular pressure loss = 280 psi at 1,000 gpm pump rate. TVD = 2,400m. 

Calculate: ECD. Is this safe given FG = 12.8 ppg at this depth?

### Exercise 3: Barite Addition
An Angola OBM system has 900 bbl total volume at 14.5 ppg. A kick swabbing event caused the crew to add seawater, diluting the mud to 14.0 ppg. How many sacks of barite (50 lb/sack, SG 4.2) must be added to return to 14.5 ppg?

### Exercise 4: Minimum Curvature Survey
From a BHA survey at 2,200m MD (Inclination 45°, Azimuth 210°) to 2,310m MD (Inclination 52°, Azimuth 215°):
1. Calculate the total angle change β
2. Calculate ΔN, ΔE, ΔTVDusing minimum curvature
3. What is the Dogleg Severity (degrees/30m)?

---

*Continue to [03_Producao_Elevacao_Applied.md](03_Producao_Elevacao_Applied.md) for Elevação de Petróleo, Escoamento, and Sistemas de Produção Superfície applied guide.*  
*Where to learn: [Learning Resources](../../../docs/learning-resources.md)*
