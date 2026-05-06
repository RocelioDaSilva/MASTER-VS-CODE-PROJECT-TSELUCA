# Production Technology
## Artificial Lift, Flow Assurance, and Production Optimisation

---

## Production Technology as a Discipline

Production technology sits between the reservoir and the export point. Its job is to maximise the rate and efficiency at which oil and gas move from the reservoir into the pipeline or tanker.

It is NOT a single role — it is a cluster of related disciplines:

| Sub-discipline | Core Question | ISPTEC Subject |
|----------------|---------------|----------------|
| Well Performance | Is this well producing at its potential? | Engenharia Reservatórios I, Elevação |
| Artificial Lift | How do we lift fluid that won't flow naturally? | Elevação de Petróleo |
| Flow Assurance | Will the fluid actually reach the FPSO? | Escoamento de Petróleo, Termodinâmica |
| Production Chemistry | What chemical threats exist in the flow path? | Química Orgânica, Ciências Materiais |
| Production Optimisation | How do we get the most from the whole system? | ER I & II, Elevação, Escoamento |
| Integrated Modelling | How does the whole system behave together? | All of the above combined |

---

## Section 1: Well Performance Engineering

### The Well Performance Concept

A well's production rate is determined by two things working together:
1. **Inflow Performance (IPR):** How much fluid the reservoir can deliver to the wellbore
2. **Outflow Performance (VLP/TPR):** How much fluid the tubing can lift from the wellbore to surface

The well produces at the intersection of these two curves — the operating point.

```
          Wellbore Flowing Pressure (Pwf)
High ┤
     │                                      
     │    IPR curve                         
     │   (reservoir inflow)                 
     │  ╲                                   
     │   ╲                                  
     │    ╲             ◄── Operating point (intersection)
     │     ╲       VLP/TPR (tubing)        
     │      ╲     ╱                        
     │       ╲   ╱                         
     │        ╲ ╱                          
Low  └─────────────────────────────────────
                     Flow Rate (Q)    High
```

**IPR equation (Vogel, for two-phase flow):**

$$\frac{q}{q_{max}} = 1 - 0.2\left(\frac{P_{wf}}{P_r}\right) - 0.8\left(\frac{P_{wf}}{P_r}\right)^2$$

Where:
- $q$ = current flow rate
- $q_{max}$ = maximum flow rate (at $P_{wf}$ = 0)
- $P_{wf}$ = flowing bottomhole pressure
- $P_r$ = current reservoir pressure

**Skin factor ($S$):** A dimensionless measure of damage or improvement near the wellbore. Positive skin = damage (reduced production). Negative skin = stimulation (improved production).

$$P_{wf} = P_r - \frac{141.2\, q \mu B}{kh}\left[\ln\left(\frac{r_e}{r_w}\right) - 0.75 + S\right]$$

A skin of +10 means the well behaves as if it has a 10× smaller wellbore radius. A skin of -3 (from a successful fracture) means the well behaves as if it has a much larger effective wellbore. This is the production engineer's target: reduce skin to maximise the IPR curve.

### Well Performance Monitoring

Production engineers monitor well performance continuously by comparing actual production against the expected IPR:

**Normalised Productivity Index (PI):**
$$PI = \frac{q}{(P_r - P_{wf})} \text{ [bbl/day/psi]}$$

If PI is declining faster than reservoir pressure decline would explain: the well has a problem (scale, asphaltene deposition, equipment failure).

**Angola production engineer's workflow:**
1. Download SCADA data daily (production rates, tubing head pressure, casing head pressure)
2. Calculate daily PI for each well
3. Flag wells with declining PI > 15% month-on-month
4. Investigate cause: send a wireline gauge run? Perform an acoustic fluid level survey? Increase gas lift rate?
5. Recommend intervention if warranted

---

## Section 2: Artificial Lift

### When Natural Flow Is Not Enough

A well flows naturally when reservoir pressure is sufficient to lift fluid from the reservoir to surface against the opposing pressure in the tubing. This natural flow is free — no energy input needed.

But reservoirs deplete. As reservoir pressure drops, the well reaches the point where it can no longer lift fluid naturally. At this point, artificial lift is required.

**Definition:** Artificial lift is any method of adding energy to the wellbore fluid to enable or enhance production.

### Artificial Lift Methods

#### 1. Gas Lift (Dominant in Angola)

**Principle:** Inject gas (from the FPSO gas compression system) down the casing-tubing annulus. The gas enters the tubing through gas lift valves, mixes with the produced fluid, reduces the density of the fluid column, and enables the fluid to lift to surface.

**Why gas lift dominates in Angola:**
- Angola FPSOs have large volumes of associated gas that must be managed (injected back into reservoir or flared — ANPG restricts flaring)
- Gas lift uses this available gas as a resource
- Subsea gas lift is feasible with existing umbilical infrastructure
- Gas lift is robust, reliable, and tolerates sand and debris
- Easy to adjust from surface (change injection rate via choke)

**Gas lift system components:**
- Gas lift compressor (on FPSO) → compresses gas to injection pressure
- Gas injection flowline (from FPSO) → delivers gas to the subsea manifold
- Umbilical/control line → delivers gas to the wellhead
- Gas lift mandrels → installed in the tubing string during completion
- Gas lift valves → installed in mandrels, open/close based on pressure differential
- Operating valve → the deepest valve, where gas actually enters the tubing

**Gas lift design:**
1. Determine the maximum injection depth (limited by injection pressure available at surface)
2. Design unloading valves to permit the well to be brought onto gas lift from dead state
3. Determine optimal injection rate → balance between more injection gas (lower fluid density = higher production) and too much gas (gas locks the well)

**GLR (Gas Liquid Ratio) optimisation:**
For a given well, there is an optimal gas injection rate. Below this rate: underinjecting, leaving production on the table. Above this rate: overinjecting, wasting gas and potentially causing unstable flow.

$$GLR_{optimal} \approx \frac{P_{injection}^{0.7} \times 100}{Depth_{injection}}$$ (approximate; actual optimisation done in Prosper/NodalSys)

**Angola gas lift allocation problem:** With 20+ wells on gas lift from a single FPSO, and a total gas availability of, say, 10 MMscf/day, how do you allocate gas across the wells to maximise total field production? This is a classic optimisation problem. The answer: allocate gas such that the marginal gain per Mscf is equal across all wells. This is solved using integrated production models (GAP software).

---

#### 2. Electric Submersible Pump (ESP)

**Principle:** A downhole electric motor drives a multistage centrifugal pump, pushing fluid from the wellbore to surface.

**When ESPs are used in Angola:**
- High liquid rate wells where gas lift reaches its limit (GLR > 5,000 scf/bbl)
- High water cut wells (late field life)
- Wells with insufficient gas supply for gas lift
- Horizontal wells with complex trajectories (gas lift valves difficult to install)

**ESP system components:**
- Motor (bottom): receives 3-phase power from surface via cable
- Motor protector/seal section: prevents wellbore fluid from entering the motor
- Pump stages: multiple impeller-diffuser stages, each adding ~10–20 psi head
- Intake section: where wellbore fluid enters the pump
- Motor lead extension: cable connection from flat cable to motor
- Power cable: runs from surface control panel to motor (strapped to tubing OD)
- Variable Speed Drive (VSD) at surface: controls motor frequency and speed

**ESP monitoring parameters:**
- Motor temperature (high temperature → overload or scaling)
- Vibration (high vibration → worn bearings, pump damage)
- Current (amperage): high current → overload; low current → pump off (pump above fluid level)
- Tubing head pressure: monitor for changes
- Flow rate: verify against IPR

**ESP failure modes in Angola:**
- Gas lock (especially if gas lift AND ESP both used)
- Scale deposition on pump stages (carbonate scale common in Angola turbidites)
- Sand ingestion (if completion sand control is inadequate)
- High temperature failure (deep, hot wells)
- Cable failure (lightning, corrosion, mechanical damage)

**ESP run life:** Typically 2–5 years in Angola conditions. An ESP replacement is a major workover operation — requires the rig to pull and replace the completion string.

---

#### 3. Other Artificial Lift Methods (Less Common in Angola)

| Method | Principle | Angola Applicability |
|--------|-----------|----------------------|
| Jet Pump | Venturi effect lifts fluid | Used in some wells; limited in deepwater |
| Plunger Lift | Gas slug drives a plunger to surface | Mainly in shallow gas wells; not deepwater |
| Progressive Cavity Pump (PCP) | Rotating helical rotor lifts viscous fluid | Not common in Angola light oil |
| Hydraulic Piston Pump | High-pressure fluid drives downhole piston | Rare in Angola |

---

### Artificial Lift Selection Framework

The correct artificial lift method depends on:

| Factor | Favours Gas Lift | Favours ESP |
|--------|-----------------|-------------|
| Available gas | Large volumes available | No/limited gas available |
| Production rate | Medium-high rates | Very high rates |
| GOR | Low-medium GOR | High GOR requires special design |
| Well deviation | Deviated wells work well | Best in near-vertical wells |
| Sand production | Good tolerance | Sensitive to sand |
| Field life | Long life, easy to adjust | Medium life, replacement needed |
| Water depth | Works excellently in deepwater | Works in deepwater (special cable design) |
| FPSO infrastructure | Gas injection system already present | Requires power supply and VSD |

---

## Section 3: Flow Assurance

### What Is Flow Assurance?

Flow assurance is the engineering discipline that ensures hydrocarbon fluids flow reliably from the reservoir to the export point, without blockage, corrosion, or instability.

The name comes from the goal: ensure the flow. This means understanding and managing everything that can go wrong in the flow path.

**Flow assurance threatens in Angola deepwater:**
- Water depth: 1,000–2,500m → very low seabed temperatures (3–5°C)
- Long tiebacks: 20–50km from wellhead to FPSO → long time for fluid to cool
- High-pressure systems: reservoir pressure 5,000–12,000 psi
- Complex fluid chemistry: high wax content, asphaltene-prone crudes, high CO₂ in some areas

The combination of high pressure and low temperature creates perfect conditions for hydrate formation.

---

### The Four Major Flow Assurance Threats

#### 1. Gas Hydrates

**What they are:** Crystalline ice-like solids formed when gas molecules (methane, ethane, propane) are encaged in a water ice lattice. They form at high pressure and low temperature.

**Formation conditions (approximate for Angola deepwater):**
- Temperature: < 20°C at pipeline pressures > 100 bar
- In Angola deepwater flowlines: this condition exists during steady-state production (seabed at 4°C, pipeline pressure 150–300 bar)
- Even worse during shutdown (no flow, fluid cools to seabed temperature)

**Angola-specific context:** All Angola deepwater flowlines operate inside the hydrate formation envelope during normal operation. Hydrate management is therefore not optional — it is a continuous engineering activity.

**Hydrate management methods:**

| Method | How It Works | Angola Use |
|--------|-------------|-----------|
| Chemical inhibition (MeOH) | Methanol shifts the hydrate curve to lower T and P | Used for shutdown treatment |
| Chemical inhibition (MEG) | Monoethylene glycol shifts hydrate curve | Continuous injection on major Angola tiebacks |
| Thermal insulation | Keeps fluid warm (above hydrate temperature) | Pipe-in-pipe insulation on all Angola deepwater flowlines |
| Electrical heating | Active heating of flowline (PIP with electrical trace) | Used on some Angola long tiebacks |
| Depressurisation | Reduces pressure below hydrate stability pressure | Emergency treatment if hydrate plug suspected |

**MEG injection system on Angola FPSOs:** MEG is injected at the wellhead (via umbilical), flows with the produced fluid back to the FPSO, is recovered in the MEG regeneration unit, and re-injected. This closed-loop system is present on every major Angola FPSO.

---

#### 2. Wax (Paraffin) Deposition

**What it is:** Paraffinic crude oils contain long-chain hydrocarbons (waxes) that are soluble at reservoir temperature but precipitate as the oil cools below the Wax Appearance Temperature (WAT).

**Angola context:** Angola deepwater crudes are typically medium to high API gravity (25–38° API) with moderate wax content. The WAT for Angola crudes is typically 25–45°C. Since flowline temperatures can fall to 10–20°C in long tiebacks, wax deposition is a real concern.

**Consequences:** Wax deposits on flowline walls, progressively reducing the flow area and increasing back-pressure. If not managed, total blockage can occur.

**Wax management methods:**
- **Pigging:** Mechanical pigs (foam pigs, disc pigs, gel pigs) are launched from the FPSO, travel down the flowline, and scrape wax off the walls. Angola FPSOs are designed with pigging loops so both production and injection flowlines can be pigged. Pigging frequency: typically monthly to quarterly.
- **Chemical inhibitors:** Wax crystal modifiers injected downhole prevent wax crystals from aggregating and depositing.
- **Thermal management:** Maintaining flowline temperature above WAT (insulation, heating).

---

#### 3. Scale Deposition

**What it is:** Inorganic mineral deposits (calcium carbonate, barium sulphate, calcium sulphate, strontium sulphate) that precipitate in the wellbore, tubing, or flowlines when incompatible waters mix or when pressure and temperature change.

**Barium sulphate (BaSO₄) — the most problematic:**
- Forms when formation water (containing barium ions, Ba²⁺) mixes with injection seawater (containing sulphate ions, SO₄²⁻)
- Extremely difficult to remove chemically — practically insoluble
- Prevention through sulphate removal from injection water (nanofiltration on FPSO)
- Barium sulphate scale in an ESP pump can destroy it within months

**Calcium carbonate (CaCO₃):**
- Precipitates as CO₂ degasses from produced water during pressure drop
- Common in Angola due to high CO₂ content in some Block 17/32 reservoir gases
- Treatable with scale inhibitor chemical injection and acid squeeze treatments

**Scale management program:**
- Water chemistry monitoring (monthly sampling from each well)
- Scale prediction software (Multiflash, ScaleSoftPitzer, OLI ScaleChem)
- Scale inhibitor injection via umbilical (subsea wells) or downhole chemical injection system
- Annual acid squeeze treatment if scale detected in wellbore

---

#### 4. Asphaltene Deposition

**What it is:** Asphaltenes are the heaviest, most polar fraction of crude oil. They can precipitate as solid particles when pressure drops below the Asphaltene Onset Pressure (AOP) or when temperature changes.

**Where deposition occurs:**
- Near-wellbore (as drawdown reduces pressure below AOP)
- Tubing strings (most common blockage point)
- Topsides processing equipment

**Angola context:** Most Angola deepwater crudes are asphaltene-stable, but some fields (notably some Block 17 crudes) have moderate asphaltene content. Due diligence on asphaltene stability is always part of a flow assurance study.

**Asphaltene management:**
- Asphaltene inhibitor injection (downhole, via umbilical)
- Pigging (mechanical removal from tubing, though less effective than for wax)
- Solvent squeezes (xylene or aromatic solvent injection to dissolve asphaltene plug)

---

### Integrated Pressure and Temperature Profiles

Flow assurance engineers generate Pressure-Temperature (PT) profiles along the entire flow path (wellbore → flowline → riser → FPSO) and overlay:
- Hydrate formation curve
- Wax appearance temperature curve
- Asphaltene onset pressure curve

The goal: keep the PT profile outside all three hazard regions at all times (steady state AND transient conditions like shutdown and restart).

Software: OLGA (Schlumberger — the dominant flow assurance tool), LedaFlow (KM), PipeSim, Multiflash.

---

## Section 4: Production Optimisation

### What Production Optimisation Means

Production optimisation is the continuous process of maximising production from the field within technical and contractual constraints.

**Constraints that limit production:**
- FPSO liquid handling capacity (separator throughput)
- FPSO gas compression capacity
- FPSO water injection capacity
- Export line capacity (pipeline or tanker schedule)
- Well rate limits (sand control, velocity, DHSV rating)
- ANPG production licence caps

**Variables that can be changed:**
- Well choke settings (open/close individual wells)
- Gas lift injection rate per well
- ESP speed (via VSD)
- Separator operating pressure (affects GOR and flash)
- Water injection rate per injector
- Manifold routing (which wells go to which separator)

### Integrated Production Modelling (IPM)

The most powerful production optimisation tool is the Integrated Production Model: a software model that links the reservoir model → well models (IPR + tubing) → manifold → flowlines → FPSO in one connected simulation.

**Software:** Petroleum Experts GAP (connected to Prosper well models), SLB Avocet, TotalEnergies' own in-house systems.

**What it enables:**
- Gas lift allocation optimisation: given 10 MMscf/day available, how to split it across 20 wells to maximise total production?
- Choke optimisation: which wells to choke back to avoid sand production without losing too much production?
- Production forecasting: what will the field produce next month under different operating scenarios?

**Angola example:** On FPSO Dalia (Block 17, TotalEnergies), a dedicated production optimisation team runs the integrated model weekly. They adjust gas lift allocation and well choke positions based on current reservoir conditions. The model has been shown to recover 2,000–5,000 bbl/day of production that would otherwise be lost through suboptimal gas allocation — worth $55–140M/year at $75/bbl.

---

## The Production Engineer's Software Stack

| Software | Function | Provider |
|----------|---------|---------|
| Prosper | Well performance modelling (IPR, VLP, gas lift design, ESP design) | Petroleum Experts |
| GAP | Field-level integrated production model | Petroleum Experts |
| OLGA | Flow assurance (transient multiphase flow) | SLB |
| Multiflash / PVTsim | PVT modelling (fluid properties, hydrate curves) | KBC / Calsep |
| Pipesim | Steady-state pipeline flow | SLB |
| ScaleSoftPitzer / OLI | Scale prediction | Various |
| Python / Pandas | Data analysis, production surveillance | Open source |
| PI Processbook (OSIsoft) | SCADA data historian access | OSIsoft |

Start with Prosper (Petroleum Experts offers a 30-day free trial). It directly connects to your ISPTEC subjects: Elevação de Petróleo (gas lift module), Escoamento de Petróleo (tubing VLP), and Engenharia de Reservatórios (IPR module).

---

## Interview Questions for Production Technology Roles

1. What is the difference between IPR and VLP? How does the operating point change when reservoir pressure declines?
2. Why does gas lift dominate as the artificial lift method in Angola deepwater?
3. What is GLR optimisation and how would you approach gas allocation across 15 gas lift wells?
4. Explain why hydrates form in Angola deepwater flowlines and what the three main mitigation strategies are.
5. What is MEG and how is it used in a closed-loop system on an FPSO?
6. A well's PI has declined 25% in 2 months. Walk me through your diagnostic process.
7. What is barium sulphate scale, why is it particularly difficult to manage, and how do operators prevent it?
8. What is skin factor and how does it appear in the well's IPR?
9. Explain the difference between steady-state and transient flow assurance analysis.
10. What is an Integrated Production Model and why is it valuable?

---

*Next: [05_Digital_PE_Data_Science.md](05_Digital_PE_Data_Science.md) — data science, machine learning, and the digital transformation of petroleum engineering.*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
