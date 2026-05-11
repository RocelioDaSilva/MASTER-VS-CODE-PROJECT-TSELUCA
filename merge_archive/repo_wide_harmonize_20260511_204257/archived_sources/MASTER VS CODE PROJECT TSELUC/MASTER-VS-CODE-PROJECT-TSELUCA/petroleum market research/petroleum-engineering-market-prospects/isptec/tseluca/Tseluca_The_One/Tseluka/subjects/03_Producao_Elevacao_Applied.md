# Elevação de Petróleo + Escoamento + Sistemas de Produção — Applied
## From IPR/VLP Equations to FPSO Operations in Angola

---

## Overview

Three ISPTEC subjects form the core of production engineering:
1. **Elevação de Petróleo** — how fluid rises from the reservoir through the well to surface
2. **Escoamento de Petróleo** — how fluid flows through pipelines and flowlines
3. **Sistemas de Produção Superfície** — how fluid is processed on the FPSO or platform

In industry, these are not separate activities. The production engineer manages the entire system from reservoir to export — and all three subjects apply every day.

The key software that connects all three: **Prosper** (well), **GAP** (field), **OLGA** (flow assurance/pipeline) — all from petroleum industry vendors. This guide shows you which ISPTEC concept maps to which software module.

---

## Part 1: Elevação de Petróleo Applied

### Nodal Analysis: The Foundation of Well Performance Work

**What ISPTEC taught:** IPR (Inflow Performance Relationship), VLP (Vertical Lift Performance), the concept of a nodal analysis operating point.

**The production engineer's daily question:** Is this well producing at its potential?

To answer this, the production engineer runs nodal analysis in Prosper:

**Prosper workflow for a gas lift well on Block 17:**

1. Input reservoir data: Pr = 6,800 psi, k = 250 mD, h = 18m, S = +3 (damaged), API = 32°, GOR = 650 scf/stb

2. Build IPR curve using Vogel equation:
   $$\frac{q}{q_{max}} = 1 - 0.2\left(\frac{P_{wf}}{P_r}\right) - 0.8\left(\frac{P_{wf}}{P_r}\right)^2$$

3. Input tubing data: 3.5" tubing OD, 5,100m length, 68° deviation, fluid properties (oil gravity, GOR, water cut)

4. Input gas lift data: 5 MMscf/day injection at 3,000m depth, 100 bar injection pressure

5. Prosper calculates the VLP/TPR (Tubing Performance Relationship) — using a multiphase flow correlation (Hagedorn-Brown or Beggs-Brill) to compute pressure drop from perforations to wellhead

6. Operating point = intersection of IPR and VLP curves

7. **Compare actual rate to model prediction.** If actual < predicted → skin is higher than estimated → stimulation candidate or downhole equipment problem.

**The two levers the production engineer controls:**
- **Wellhead choke:** Opening the choke lowers the wellhead pressure → lowers Pwf → moves up the IPR curve (more inflow). But a too-low Pwf can cause sand production, gas coning, or water coning.
- **Gas lift rate:** More gas lift lowers the tubing fluid density → lowers Pwf at same WHP. But too much gas lift causes overinjection — the GLR becomes too high for good lift (gas competes with liquid).

---

### Gas Lift Design Deep Dive

**What ISPTEC taught:** Gas lift principle, valve types (bellows-operated, injection pressure operated), unloading sequence.

**Industry workflow — designing a gas lift completion for Angola:**

**Step 1: Determine maximum injection depth**
The gas is injected from the FPSO at a fixed pressure (the compressor discharge pressure). After flowing down the casing annulus (losing pressure to friction and static head), the pressure available at depth determines the maximum injection depth.

Available injection pressure at depth d:
$$P_{inj,d} = P_{inj,surface} + \rho_{gas} \times g \times d - \Delta P_{friction,annulus}$$

For Angola deepwater wells with 2,800–3,500m well depth to perforations (below mudline), injection depths of 2,000–2,800m are typically achievable with 180–200 bar surface injection pressure.

**Step 2: Size the operating valve**
The gas lift operating valve must pass the required injection rate at the available differential pressure. Valve size is selected from a performance curve (flow coefficient vs differential pressure × ΔP).

**Step 3: Design unloading valves**
During well startup, the tubing is full of dead mud/kill fluid. The well must be unloaded progressively using a series of valves from top to bottom:
- Upper valve opens first → gas enters, lightens the fluid above → column above flows → upper valve closes (pressure drops)
- Next valve opens → process repeats down to the operating valve

Angola deepwater well unloading design consideration: The static head of 1,800m of seawater above the seabed tree adds ~2,600 psi of back-pressure on the casing annulus. This must be accounted for in the unloading valve design — the valves must be calibrated accordingly.

---

### ESP Design for Angola High Water Cut Wells

**What ISPTEC taught:** ESP operating principle, pump performance curves, motor sizing.

**Industry workflow — selecting an ESP for a Block 18 well:**

Given well conditions:
- Required liquid rate: 18,000 stb/day (85% water cut — late field life)
- Required total dynamic head (TDH): 2,800 psi (to lift fluid from reservoir to surface)
- Bottom hole temperature: 138°C
- Fluid specific gravity: 1.05 (water-dominated)

**Step 1: Calculate flow rate in pump condition (res. bbls/day)**
$$Q_{pump} = \frac{Q_{surface} \times B_w}{(1 - \text{free gas fraction at pump intake})}$$
≈ 19,000 bbl/day in this case

**Step 2: Select pump series**
Each ESP manufacturer (Schlumberger REDA, Baker Hughes Centrilift, Weatherford) offers pump series for different flow rates:
- 562-series pump (5.62" OD): 8,000–20,000 bbl/day range ← select this
- 400-series pump: 1,000–8,000 bbl/day range
- 675-series pump: 15,000–50,000 bbl/day range

**Step 3: Determine number of pump stages**
Each stage delivers a certain head (in feet of fluid):
- 562-series at 19,000 bbl/day: ~25 ft/stage
- TDH in feet: 2,800 psi × 2.31 / SG = 6,160 ft
- Number of stages: 6,160 / 25 = 246 stages

**Step 4: Motor sizing**
Motor HP = (Number of stages × HP/stage at design rate) + 10% safety factor

**Step 5: Temperature derating**
At 138°C, the motor is operating at the upper limit for standard motors. A high-temperature motor grade must be specified. This requires knowing material properties — from your Ciências dos Materiais subject.

**Software:** Prosper ESP module (Petroleum Experts) does this calculation automatically once you input the well parameters and select the pump model from the database.

---

## Part 2: Escoamento de Petróleo Applied

### Multiphase Flow in Pipelines

**What ISPTEC taught:** Two-phase flow regimes (stratified, slug, annular, bubbly, dispersed), pressure drop correlations (Lockhart-Martinelli, Beggs-Brill, Hagedorn-Brown), holdup.

**Why this matters in Angola deepwater:** The flowlines connecting subsea wells to the FPSO carry a mixture of oil, water, and gas at high pressure. The flow regime and pressure drop in these 10–50km flowlines directly affects:
- The wellhead flowing pressure (the downstream backpressure on the well)
- Slugging behaviour (large slugs of liquid arriving at the FPSO in irregular pulses — major operational problem)
- Hydrate risk (slug flow causes local cold spots)

**Slug flow in Angola deepwater flowlines:** This is one of the most significant operational challenges in Angola. When gas and liquid flow together at certain rates and geometry conditions, the flow organises into alternating slugs of liquid and pockets of gas. Each liquid slug arriving at the FPSO separator causes:
- Sudden increase in separator liquid level
- Pressure fluctuation in the separator
- Risk of high-level trip on the separator (production shutdown)

**Slug management strategies:**
1. **Topside slug catchers:** Large vessels upstream of the separator designed to absorb slug arrival
2. **Riser base gas injection:** Inject gas at the riser base to homogenise the flow and prevent slug formation
3. **Production rate optimisation:** Operate wells at rates that avoid slugging flow regimes
4. **Anti-slug control valves:** Choke the riser to maintain stable flow

**OLGA simulation:** The transient multiphase flow simulator (OLGA by SLB) is the standard tool for flow assurance analysis. It uses numerical solutions of the conservation equations for each phase and provides:
- Steady-state pressure and temperature profiles
- Transient slug flow prediction
- Ramp-up simulation (how does the flowline behave when production starts?)
- Shutdown and restart analysis (hydrate risk during shut-in)

---

### Multiphase Flow: Pressure Drop Calculation (Beggs-Brill Method)

**What ISPTEC taught:** The principle. **What industry requires:** Applying it in software, understanding when correlations are inaccurate.

**A simplified pipeline pressure drop calculation:**

For horizontal flow of a gas-liquid mixture:
$$\frac{dP}{dL} = \frac{dP}{dL}_{friction} + \frac{dP}{dL}_{elevation}$$

$$\frac{dP}{dL}_{friction} = \frac{f \rho_m v_m^2}{2g_c d}$$

Where:
- f = Moody friction factor (depends on Reynolds number and pipe roughness)
- ρ_m = mixture density (weighted average of oil and gas densities by holdup)
- v_m = mixture velocity
- d = pipe diameter

**Holdup (H_L):** The fraction of pipe cross-section occupied by liquid. H_L is not simply the input liquid volume fraction — it depends on the flow regime. This is what makes multiphase flow difficult: you need an empirical correlation or simulation to get holdup, and holdup affects both density and pressure drop.

**Angola-specific pipeline parameter:**
- Typical Angola deepwater flowline: 10" diameter, 15–30 km long, with ~1,800m of riser (the nearly vertical section from seabed to FPSO)
- The riser dominates the pressure drop — gravitational head of 1,800m of fluid at typical oil/gas/water mixture densities is the largest pressure component

---

## Part 3: Sistemas de Produção Superfície Applied

### FPSO Process Flow: From Wellstream to Export

**What ISPTEC taught:** Separator principles (two-phase and three-phase), gas compression, water treatment, crude stabilisation.

**The Angola FPSO production process in sequence:**

```
FPSO DALIA (Block 17 — TotalEnergies) — SIMPLIFIED PROCESS

SUBSEA INLET
│
│  Wellstream: ~240,000 bbl/day liquid + 300 MMscf/day gas
│  at 150–200 bar, 70–90°C arriving at FPSO
│
▼
HIGH PRESSURE SEPARATOR (2 trains)
│  Operating at 60–80 bar
│  Oil + dissolved gas → next separator
│  Free gas → HP compression
│  Produced water → water treatment
│
▼
MEDIUM PRESSURE SEPARATOR
│  Operating at 12–20 bar
│  Further gas liberation from oil
│  Gas → MP compression
│
▼
LOW PRESSURE SEPARATOR / DEGASSING DRUM
│  Operating at 2–5 bar
│  Final gas stripping from oil
│  Oil → electrostatic treater
│
▼
ELECTROSTATIC TREATER
│  Breaks oil-water emulsion using electric field
│  Target: BS&W < 0.5% (basic sediment and water)
│
▼
CRUDE COOLER / METERING
│  Oil cooled to export temperature (~45°C)
│  Metered for fiscal measurement (custody transfer)
│
▼
STORAGE TANKS (3–5 tanks, each 300,000–500,000 bbl)
│
▼
OFFLOADING SYSTEM
│  Tandem offloading to shuttle tanker (every 5–7 days)
│  Transfer rate: 40,000–60,000 bbl/hr
│
▼
SHUTTLE TANKER → EUROPE/CHINA/USA
```

**Three-phase separator design (from Sistemas de Produção Superfície):**

The separator must:
1. Allow gas to disengage from liquid (vertical velocity < terminal velocity of oil droplets in gas)
2. Allow oil-water separation (retention time sufficient for gravity separation)
3. Control levels (gas-liquid interface and oil-water interface) via level controllers

**Separator sizing:**
- Liquid residence time required: typically 2–5 minutes for Angola crude to achieve adequate dewatering
- Volume = Flow rate × Residence time
- For 240,000 bbl/day = 10,000 bbl/hr ≈ 167 bbl/min

Separator liquid volume = 167 bbl/min × 3 min = 500 bbl per separator
= two parallel trains × 250 bbl each

**In industry:** The detailed separator design is done by process/facilities engineers using HYSYS (Aspen Tech) or PRO/II (AVEVA) process simulation software. But as a production engineer, you must understand the process to:
- Diagnose separation problems (poor dewatering → high BS&W export)
- Optimise separator pressures (affects GOR, oil shrinkage, gas compression)
- Manage FPSO capacity constraints (if throughput exceeds design, what gives first?)

---

### FPSO Process Safety: From Sistemas de Produção to Real Operations

**What ISPTEC taught:** Safety valves, pressure vessels, flaring.

**What ANPG requires on all Angola FPSOs:**
1. **High-High pressure shutdown (PAHH):** Every vessel has automatic shutdown valves that close when pressure exceeds safe limits (ANPG requires proof testing every 2 years)
2. **Emergency Shutdown System (ESD):** Three tiers — ESD-1 (well shutdown), ESD-2 (process shutdown), ESD-3 (FPSO total shutdown including power)
3. **Flare system:** Must handle maximum relief flow from all pressure safety valves simultaneously — ANPG requires a flare system design basis review
4. **Produced water treatment:** Must achieve < 40 ppm oil in water before discharge to sea (ANPG and MARPOL requirement)

**Produced water treatment system:**
Angola FPSOs must process ~100,000–300,000 bbl/day of produced water by late field life (as water cut increases). The treatment train:
1. Skim tank / hydrocyclone: Remove free oil (>150 μm droplets)
2. Induced gas flotation (IGF): Remove dispersed oil (10–150 μm droplets) by micro-bubbles
3. Guard filter/walnut shell filter: Polishing to < 40 ppm
4. Deoiling membrane (some FPSOs): Final polishing to < 15 ppm

**Why produced water treatment is critical for Angola engineers:** Angola's production is increasingly water-dominant as fields mature. Managing produced water efficiently and in compliance with environmental regulations is a growing technical challenge. This is an opportunity for engineers with strong Sistemas de Produção + Engenharia Ambiental backgrounds.

---

## The Integrated Production System: Everything Connected

Here is how your three ISPTEC subjects connect to each other and to real-world Angola operations:

```
RESERVOIR
│  P_r = 6,800 psi (declining over field life)
│  Permeability, skin — set by reservoir and completion quality
│
▼
WELL (Elevação de Petróleo)
│  IPR/VLP intersection → Q well = 8,000 bbl/day
│  Gas lift: 4 MMscf/day at 2,800m injection depth
│  DHSV status: open (tested last month)
│  Tubing head pressure: 280 bar
│
▼
SUBSEA FLOWLINE (Escoamento de Petróleo)
│  Multiphase flow, 25km flowline + 1,800m riser
│  Pressure drop: 75 bar (flowline + riser)
│  Temperature: drops from 85°C (wellhead) to 45°C (FPSO)
│  MEG injection at wellhead: 50 m³/day (hydrate prevention)
│
▼
FPSO INLET (Sistemas de Produção)
│  Fluid arrives at ~205 bar, 45°C
│  Total FPSO throughput: 20 wells × 8,000 bbl/day avg = 160,000 bbl/day
│
▼
THREE-PHASE SEPARATOR → TREATER → METERING → STORAGE → OFFLOAD
```

**The production engineer sits in the middle of this entire system.** Any anomaly anywhere — declining well rate, slugging flowline, separator upset, ESP trip — lands on the production engineer's desk.

---

## Software Connecting Your ISPTEC Subjects

| ISPTEC Subject | Concept | Software Module | Free Access? |
|----------------|---------|----------------|-------------|
| Elevação de Petróleo | Gas lift design | Prosper (Gas lift) | 30-day trial |
| Elevação de Petróleo | ESP design | Prosper (ESP) | 30-day trial |
| Elevação de Petróleo | IPR/VLP | Prosper (VLP/IPR) | 30-day trial |
| Escoamento de Petróleo | Pipeline hydraulics | Pipesim (SLB) | Academic license |
| Escoamento de Petróleo | Transient flow/slugging | OLGA (SLB) | Academic contact SLB |
| Sistemas Produção | FPSO process simulation | HYSYS (Aspen Tech) | Student version via AspenTech |
| Sistemas Produção | PVT / phase behaviour | PVTsim (Calsep) | Academic license |

**Start with Prosper.** It is the most direct connection between Elevação de Petróleo and real production engineering work. The 30-day trial is sufficient to build a complete gas lift well model and run a nodal analysis.

---

## Exercises

### Exercise 1: Nodal Analysis
A Block 17 well has:
- Pr = 6,400 psi, k = 280 mD, h = 22m, S = +5, μ = 0.82 cp, Bo = 1.40, rw = 0.35ft, re = 2,000ft
- Tubing: 3.5" ID, 5,000m length, deviation 65°
- Gas lift: 3 MMscf/day at 2,600m depth
- WHP = 280 bar

1. Plot the IPR using Vogel equation (at least 6 points)
2. Given the gas lift, estimate the VLP curve at the operating GLR
3. Estimate the operating flow rate

### Exercise 2: Gas Lift Optimisation
Four wells share 10 MMscf/day total gas availability. Well performance data:

| Well | Q at 0 MMscf/d | Q at 2 MMscf/d | Q at 4 MMscf/d | Q at 6 MMscf/d |
|------|----------------|----------------|----------------|----------------|
| A | 2,000 | 5,500 | 7,200 | 7,800 |
| B | 500 | 3,000 | 5,500 | 7,000 |
| C | 4,000 | 6,000 | 7,000 | 7,100 |
| D | 1,000 | 4,000 | 6,500 | 7,800 |

Allocate 10 MMscf/day to maximise total field production. (Hint: equalise marginal gain per MMscf/d across all wells.)

### Exercise 3: FPSO Separator Capacity
An FPSO HP separator receives 180,000 bbl/day of liquid. Required residence time: 3 minutes. The separator is horizontal, 4m diameter, 25m long. The liquid level fills 50% of the separator cross-section.

1. Calculate separator liquid volume (bbl)
2. Is the separator large enough?
3. If water cut increases from 30% to 70% while total liquid rate remains constant, does this affect separator performance? Explain.

---

*Continue to [04_Completacao_Applied.md](04_Completacao_Applied.md) for Completação de Poços applied guide.*  
*Where to learn: [Learning Resources](../../../docs/learning-resources.md)*
