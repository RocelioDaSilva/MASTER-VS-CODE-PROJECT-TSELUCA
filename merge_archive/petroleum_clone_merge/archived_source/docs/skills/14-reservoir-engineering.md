# Skill 14 â€” Reservoir Engineering Basics

> **Applies to:** Reservoir Engineer, Production Engineer, Simulation Engineer, Field Development Engineer
> **Offshore relevance:** Understanding reservoir behaviour is the foundation of all production decisions â€” Angola FPSOs are optimized based on reservoir engineer outputs

---

## What Is This Skill?

Reservoir engineering is the application of scientific principles and engineering judgement to efficiently produce oil and gas from underground reservoirs while maximizing ultimate recovery. It sits at the intersection of geology, fluid mechanics, thermodynamics, and economics. A reservoir engineer in Angola answers: "How much oil is there? How fast can we produce it? How do we maximize what we recover?" These answers drive billion-dollar decisions.

---

## Why It Matters Offshore

Angola's major turbidite reservoirs (Block 15 Kizomba, Block 17 Girassol/Dalia/PAZFLOR, Block 32 Kaombo) are complex, stratified sandstone systems with:
- High initial reservoir pressure (400â€“600 bar at 5,000â€“7,000m depth)
- Undersaturated oil (above bubble point) at initial conditions
- Strong aquifer support or gas cap
- Decline rates that must be managed to optimize [FPSO](../glossary.md) plateau rates

Without reservoir engineering input, the [FPSO](../glossary.md) would either be underloaded (leaving money on the table) or overproduced (causing rapid decline and early water breakthrough).

---

## Key Concepts to Master

### 1. Reservoir Rock Properties

#### Porosity (Ï†)

**Definition:** The fraction of total rock volume occupied by pore space.

$$\phi = \frac{V_{pore}}{V_{bulk}} = \frac{V_{bulk} - V_{grain}}{V_{bulk}}$$

**Typical values:**
| Reservoir type | Porosity |
|---|---|
| Excellent sandstone | 25â€“35% |
| Good sandstone | 20â€“25% |
| Poor sandstone | 10â€“20% |
| Angola turbidite sandstones | 20â€“30% (excellent) |
| Carbonate (Angola pre-salt) | 5â€“30% (variable) |

**Effective porosity:** Only connected pores contribute to flow (excludes isolated pores and clay-bound water).

---

#### Permeability (k)

**Definition:** The ability of a rock to transmit fluid. Measured in millidarcies (mD) or Darcies (D).

**Darcy's Law** (1D linear flow):

$$Q = \frac{k \cdot A \cdot \Delta P}{\mu \cdot L}$$

Where:
- $Q$ = flow rate (cmÂ³/s or bbl/day)
- $k$ = absolute permeability (Darcies)
- $A$ = cross-sectional area (cmÂ² or ftÂ²)
- $\Delta P$ = pressure drop (atm or psi)
- $\mu$ = fluid viscosity (cP)
- $L$ = length (cm or ft)

**Typical values:**
| Permeability | Rock quality |
|---|---|
| >1,000 mD | Excellent |
| 100â€“1,000 mD | Good |
| 10â€“100 mD | Moderate |
| 1â€“10 mD | Low |
| <1 mD | Tight (unconventional) |

Angola turbidite reservoirs: often 100â€“2,000 mD â€” high permeability, good flow rates.

---

#### Fluid Saturations

- **Sw (water saturation):** Fraction of pore space occupied by water â€” critical for distinguishing water from oil zones
- **So (oil saturation):** Fraction of pore space with oil
- **Sg (gas saturation):** Fraction of pore space with gas
- **Sw + So + Sg = 1** (always sums to 1)

**Irreducible water saturation (Swirr):** Minimum water saturation that cannot be produced even with great drawdown (held in pore throats by capillary forces). Oil is mobile above Swirr.

**Residual oil saturation (Sor):** Oil left in reservoir after a waterflood â€” cannot be displaced by water injection below this value.

---

### 2. Fluid Properties â€” PVT Analysis

**PVT (Pressure-Volume-Temperature) analysis** characterizes reservoir fluid behaviour. Samples are collected at reservoir conditions and analysed in a laboratory.

#### Key PVT Parameters

| Parameter | Symbol | Definition |
|---|---|---|
| **Solution Gas-Oil Ratio** | Rsi | Volume of gas dissolved per barrel of stock tank oil at initial conditions (scf/STB) |
| **Formation Volume Factor (oil)** | Bo | Volume of reservoir oil / volume of stock tank oil (reservoir bbl / STB) |
| **Bubble Point Pressure** | Pb | Pressure at which first gas bubble comes out of solution |
| **Oil viscosity** | Î¼o | Resistance to flow (cP) â€” increases as pressure drops below bubble point |
| **Gas compressibility factor** | Z | Deviation factor for real gas behaviour |

**Bo significance:** If Bo = 1.35, then 1 barrel of reservoir oil = 1.35 reservoir barrels. When it reaches surface and gas comes out of solution, oil shrinks to 1 STB (stock tank barrel).

**Angola fluid characteristics:**
- Block 17 crudes: API 29â€“36Â°, GOR 100â€“400 scf/STB, Pb 150â€“250 bar
- High Bo (1.3â€“1.5) due to dissolved gas
- Undersaturated above bubble point at reservoir conditions

---

### 3. Reservoir Pressure and Drive Mechanisms

**Reservoir energy** (what pushes oil to the well) comes from:

| Drive mechanism | How it works | Efficiency |
|---|---|---|
| **Solution gas drive** | Gas comes out of solution as pressure drops; expands to displace oil | 5â€“30% recovery |
| **Gas cap drive** | Free gas cap at top expands as reservoir pressure falls | 20â€“40% |
| **Water drive (natural aquifer)** | Aquifer water influx replaces produced oil | 35â€“60% |
| **Compaction drive** | Formation compaction as pore pressure declines | Minor â€” only important in chalk or weak sediments |
| **Gravity drainage** | Oil drains downward by gravity | Works in steeply dipping reservoirs |

**Angola Kaombo Block 32:** Strong bottom water drive + solution gas. Water injection to supplement aquifer drive.

---

### 4. Material Balance Equation

The material balance equation (MBE) is sometimes called "the tank model" â€” it treats the reservoir as a single tank and equates production to reservoir expansion.

**Simplified form (undersaturated oil, no gas cap, aquifer support):**

$$N_p \cdot B_o = N \cdot B_{oi} \cdot c_{eff} \cdot \Delta P + W_e - W_p \cdot B_w$$

Where:
- $N_p$ = cumulative oil production (STB)
- $B_o, B_{oi}$ = oil volume factor (current, initial)
- $N$ = STOIIP (Stock Tank Oil Initially In Place)
- $c_{eff}$ = effective compressibility
- $W_e$ = aquifer water influx
- $W_p$ = cumulative water production

**Havlena-Odeh method:** Rearranges MBE into a linear form to solve for STOIIP and aquifer size simultaneously from production history.

---

### 5. Decline Curve Analysis (DCA)

**Purpose:** Extrapolate future production from past production trends to forecast reserves.

**Arps' decline equations:**

| Decline type | Rate equation | Cumulative production | b value |
|---|---|---|---|
| **Exponential** | $q = q_i \cdot e^{-D_i t}$ | $Q = \frac{q_i - q}{D_i}$ | b = 0 |
| **Hyperbolic** | $q = q_i(1 + b D_i t)^{-1/b}$ | Complex | 0 < b < 1 |
| **Harmonic** | $q = \frac{q_i}{1 + D_i t}$ | $Q = \frac{q_i}{D_i} \ln\left(\frac{q_i}{q}\right)$ | b = 1 |

Where:
- $q$ = production rate (bbl/day)
- $q_i$ = initial rate at start of decline
- $D_i$ = initial decline rate (1/time)
- $t$ = time

**Exponential decline** is the most common for a depletion-drive reservoir in late life.

**Log-linear plot:** Plotting log(rate) vs. time â€” exponential decline appears as a straight line. Deviation from straight line = hyperbolic or harmonic.

---

### 6. Reserves Classification

**SPE PRMS (Petroleum Resources Management System)** is the international standard for classifying reserves.

| Category | Definition | Probability |
|---|---|---|
| **Proved (1P)** | Reasonable certainty of recovery under existing conditions | â‰¥90% (P90) |
| **Proved + Probable (2P)** | Best estimate (central estimate) | â‰¥50% (P50) |
| **Proved + Probable + Possible (3P)** | Upside estimate | â‰¥10% (P10) |
| **Contingent Resources** | Discovered but not yet commercial | Variable |
| **Prospective Resources** | Not yet discovered (exploration) | Variable |

**Reserves are different from STOIIP:**
- STOIIP = total oil in the reservoir
- Reserves = recoverable portion of STOIIP (after applying recovery factor)

**Recovery factor (RF):** `Reserves = STOIIP Ã— RF`. RF for Angola deepwater ranging 25â€“45% depending on drive mechanism and waterflooding.

---

### 7. Pressure Transient Analysis (PTA) â€” Introduction

**Purpose:** Analyse the pressure changes in a well following a rate change (buildup test or drawdown test) to measure reservoir and near-wellbore properties.

#### Buildup Test (BU)
1. Well flows at constant rate â†’ pressure decreases
2. Well is shut in (rate = 0) â†’ pressure **builds back up** toward reservoir pressure
3. Plot of pressure rise during buildup allows calculation of:
   - **Permeability (k):** From slope of semi-log straight line
   - **Skin (S):** Measure of wellbore damage or stimulation (positive S = damage; negative S = stimulated, e.g., frac)
   - **Static reservoir pressure (Pi)**

**Horner plot:** Classic analysis â€” plot pressure vs. $\log\left(\frac{t_p + \Delta t}{\Delta t}\right)$ where $t_p$ = producing time and $\Delta t$ = shut-in time.

**Skin factor S:**
- S = 0: No damage, no stimulation
- S > 0: Formation damage (scale, clay, fines migration) â€” well performing below potential
- S < 0: Stimulated well (fracture, acid job) â€” producing above theoretical Darcy flow

---

### 8. Decline and Field Management â€” Angola Context

**[FPSO](../glossary.md) plateau production:** Angola FPSOs are designed to maintain a target production rate (the plateau) for as long as possible, then decline. Reservoir engineer's job is to maximize plateau duration.

**Strategies:**
- **Infill drilling:** New wells to arrest decline â€” standard in Angola
- **Water injection / EOR:** Replace produced reservoir energy
- **Production optimization:** Well allocation optimization â€” give more production to wells with best GOR, lowest watercut
- **Gas injection:** Reinjection of produced gas to maintain reservoir pressure and recover gas-cap benefits
- **Side-track:** Drill new wellbore from existing platform if well performance deteriorates

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Memorize Darcy's Law â€” understand what each term means physically
- [ ] Understand porosity vs. permeability â€” can a rock have high porosity but low permeability?
- [ ] Learn the 5 reservoir drive mechanisms â€” rank them by recovery factor
- [ ] Understand Arps' exponential decline â€” practice calculating future rate and ultimate recovery

### Intermediate (2â€“5 months)
- [ ] Study PVT concepts: bubble point, Bo, Rsi â€” practice reading a PVT report
- [ ] Work through material balance equation for simple cases (no aquifer, no gas cap)
- [ ] Practice Horner buildupttest analysis on example data sets (SPE textbooks have examples)
- [ ] Learn Python/Excel for decline curve analysis â€” build your own DCA spreadsheet

### Advanced (5â€“12 months)
- [ ] Study reservoir simulation basics: grid geometries, fluid models, history matching
- [ ] Learn CMG GEM or Eclipse (common in Angola IOCs) â€” student licenses available
- [ ] Study SPE papers on Angola block field development plans
- [ ] Learn how reserves are audited (SPE-PRMS standard in detail)

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **Craft, Hawkins "Applied Petroleum Reservoir Engineering"** | Classic textbook | Paid |
| **Tarek Ahmed "Reservoir Engineering Handbook"** | Comprehensive reference | Paid |
| **[SLB](../../data/company-directory/slb.md) [Schlumberger](../../data/company-directory/slb.md) Oilfield Glossary** | Clear definitions | Free â€” glossary.oilfield.slb.com |
| **SPE "Reservoir Engineering" module** | SPE online courses | SPE membership |
| **Python for Petroleum Engineering (pyPetro)** | Decline curves in Python | Free on GitHub |
| **CMG Software (student license)** | Reservoir simulation | Free student version |
| **SPE PRMS 2018 (free PDF)** | Reserves classification standard | Free â€” spe.org |

---

## Practice Questions

1. An Angola well has an initial rate of 8,000 bbl/day and exponential decline at $D_i = 0.03$/month. What is the rate after 24 months?
2. What is the physical meaning of a negative skin factor? What operations can produce a negative skin?
3. A reservoir has STOIIP = 500 MMbbl and a water-drive recovery factor of 35%. What are the 2P reserves?
4. Explain the difference between solution gas drive and water drive. Which provides higher oil recovery, and why?
5. You note that a well's production plot (log rate vs. time) has suddenly become steeper. Suggest three possible causes.

---

## Related Skills

- [04 â€” Formation Evaluation & Log Interpretation](04-formation-evaluation.md) (logs determine porosity, Sw, pay thickness)
- [09 â€” Artificial Lift](09-artificial-lift.md) (IPR curves come from reservoir engineering)
- [10 â€” Flow Assurance](10-flow-assurance.md) (reservoir fluid PVT drives [flow assurance](10-flow-assurance.md) design)
- [15 â€” Well Integrity](15-well-integrity.md) (reservoir pressure changes affect barrier envelopes)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Reservoir Engineering** | Free reference | Free | [petrowiki.spe.org/Reservoir_engineering](https://petrowiki.spe.org/Reservoir_engineering) |
| **Petrel RE + Eclipse** | Software (free student) | Free | [learn.slb.com](https://learn.slb.com) |
| **MBAL** | Material balance software (student) | Free student license | [petex.com/academic](https://www.petex.com/academic/) |
| **Reservoir Engineering Handbook** (Ahmed) | Textbook | ~$100 | [Elsevier](https://www.elsevier.com) |
| **Fundamental of Reservoir Engineering** (Dake) | Textbook | ~$80 | SPE / Elsevier |
| **PetroSkills â€” Reservoir Engineering** | Paid course | $1,000â€“5,000 | [petroskills.com](https://www.petroskills.com) |
| **NExT â€” Reservoir Simulation** | Paid course | $1,000â€“5,000 | [next-training.net](https://www.next-training.net) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

