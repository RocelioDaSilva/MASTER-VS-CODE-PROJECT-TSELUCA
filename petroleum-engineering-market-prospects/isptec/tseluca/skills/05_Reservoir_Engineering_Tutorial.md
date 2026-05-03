# Skill Tutorial 05 — Reservoir Engineering

> **Applies to:** Reservoir engineers (CORE), production engineers (HIGH), drilling engineers (MEDIUM)
> **ISPTEC connection:** Engenharia de Reservatórios I & II, Avaliação de Formações, Produção de Hidrocarbonetos
> **Goal:** Master the quantitative tools of reservoir engineering — from rock/fluid properties through material balance, decline curve analysis, pressure transient analysis, and simulation — at the level expected of a reservoir engineer trainee.

---

## Part 1: Reservoir Rock Properties

### Porosity

**Definition:** The fraction of the total rock volume that is pore space (not solid mineral).

$$\phi = \frac{V_{pore}}{V_{bulk}} = \frac{V_{bulk} - V_{grain}}{V_{bulk}}$$

**Angola turbidite reservoirs:** Typical porosity 20–32%. These are very good reservoirs. Conventional carbonate reservoirs in the Middle East: 10–20%. By comparison, Angola's reservoir quality is excellent.

**Types:**
- **Total porosity:** All void space including isolated pores
- **Effective porosity:** Connected pore space only (what matters for flow)

### Permeability

**Definition:** A rock's ability to transmit fluid. Quantified by Darcy's Law.

**Darcy's Law (single-phase, horizontal, incompressible flow):**

$$q = \frac{k A \Delta P}{\mu L}$$

Where:
- $q$ = flow rate (cm³/s in Darcy units; m³/s in SI)
- $k$ = permeability (Darcy or millidarcy; mD is most common in oilfield)
- $A$ = cross-sectional area (cm²)
- $\Delta P$ = pressure difference (atm in Darcy; Pa in SI)
- $\mu$ = fluid viscosity (cP)
- $L$ = flow length (cm)

**Permeability ranges:**

| Permeability | Rock Type | Angola Implication |
|---|---|---|
| > 500 mD | Excellent sand | Block 17 Girassol sands |
| 100–500 mD | Good sand | Typical Angola turbidite |
| 10–100 mD | Moderate | Tighter sands |
| 1–10 mD | Tight | Requires special attention |
| < 1 mD | Tight sand | Not common in Angola deepwater |

**Horizontal permeability (kh)** is typically higher than **vertical permeability (kv)** in laminated sands. The kv/kh ratio (anisotropy) matters for gravity drainage and water/gas coning.

### Fluid Saturations

The pore space contains some combination of oil, gas, and water:

$$S_o + S_g + S_w = 1.0$$

**Irreducible water saturation (Swi or Swirr):** The minimum water saturation — water that is bound to rock surfaces and cannot be produced. Even "clean" oil sands contain Swi typically = 10–25% in Angola.

**Residual oil saturation (Sor):** Oil that remains trapped in pores after water flooding. Limits oil recovery to (1 − Swi − Sor) / (1 − Swi) of the oil initially in place.

---

## Part 2: Reservoir Fluid Properties (PVT)

Reservoir fluids behave very differently underground than at surface. PVT (Pressure-Volume-Temperature) properties describe these differences.

### Oil Formation Volume Factor (Bo)

**Definition:** Volume of reservoir oil required to produce 1 stock tank barrel of oil at surface conditions.

$$B_o = \frac{V_{oil,reservoir}}{V_{oil,surface}} \quad \text{[RB/STB]}$$

Typical Angola deepwater oil: $B_o$ = 1.2–1.6 RB/STB. This means 1 barrel at surface came from 1.2–1.6 barrels underground. The difference is due to gas coming out of solution and oil shrinking as pressure and temperature drop.

**Why Bo matters:**
- Converts surface production (what you measure in bbl/day on the FPSO) to reservoir volumes (what you need for reserves calculations)
- Reservoir oil in place = Stock tank oil in place × Bo

### Solution Gas-Oil Ratio (Rs)

**Definition:** Volume of gas dissolved in oil at reservoir conditions, measured in scf/STB.

Below the **bubble point pressure (Pb)**: gas is dissolved in oil. Above Pb, free gas exists.

As reservoir pressure drops below Pb: dissolved gas comes out of solution (solution gas drive). This is the primary production mechanism in many Angola blocks before pressure support is installed.

### Key PVT Relationships

$$\text{OOIP (STB)} = \frac{7758 \times A \times h \times \phi \times (1 - S_w)}{B_{oi}}$$

Where:
- 7758 = conversion factor (bbl/acre-ft)
- $A$ = area (acres)
- $h$ = pay thickness (ft)
- $\phi$ = porosity (fraction)
- $S_w$ = water saturation (fraction)
- $B_{oi}$ = initial formation volume factor (RB/STB)

---

## Part 3: Drive Mechanisms

How does the oil actually flow to the well? The answer determines how many wells to drill, what the production profile looks like, and the ultimate recovery factor.

| Mechanism | What Drives Production | Recovery Factor | Angola Relevance |
|---|---|---|---|
| **Solution gas drive** | Gas coming out of solution as pressure drops. Expands and drives oil. | 5–25% | Common early in field life |
| **Gas cap drive** | Free gas cap expands as oil is produced, pushing oil toward wells. | 20–40% | Some Angola fields have gas caps |
| **Water drive (aquifer)** | Natural aquifer supports reservoir pressure as oil is produced. | 35–60% | Strong in some Angola deepwater blocks |
| **Water injection** | Injected water maintains pressure and sweeps oil toward producing wells. | 35–55% | Standard IOR method in Angola (Block 15, 17, 32) |
| **Gas injection / WAG** | Injected gas (WAG = Water Alternating Gas) improves sweep. | 40–65% | Used or tested in several Angola fields |
| **Gravity drainage** | Oil drains down under gravity. Long-term mechanism. | High in right conditions | Relevant for tall reservoirs |

---

## Part 4: Material Balance Equation (MBE)

The Material Balance Equation is the fundamental reservoir energy equation. It states that the total production from the reservoir equals the total expansion of reservoir fluids plus any natural influx.

**Simplified Havlena-Odeh form:**

$$F = N(E_o + m \cdot E_g + E_{fw}) + W_e B_w$$

Where:
- $F$ = total underground withdrawal (RB) = $N_p B_o + W_p B_w + G_p B_g$
- $N$ = original oil in place (STB)
- $E_o$ = oil expansion term = $B_o - B_{oi}$
- $m$ = initial gas cap size ratio
- $E_g$ = gas cap expansion term
- $E_{fw}$ = connate water and formation compressibility expansion
- $W_e$ = cumulative water influx (RB)
- $B_w$ = water FVF

**Practical use:** Plot $F/E_o$ vs. $W_e B_w / E_o$ (Havlena-Odeh plot). If it's a straight line with intercept at N — the model is consistent. If it curves — there's an aquifer influx or other mechanism not accounted for.

---

## Part 5: Decline Curve Analysis (Arps Method)

When a well has been producing for a while, you can fit its production history to an Arps decline curve to predict future production and estimate recoverable reserves.

**Three types of decline:**

**Exponential decline (b = 0):** Constant fractional decline rate. Most conservative.
$$q(t) = q_i \times e^{-D_i t}$$

**Harmonic decline (b = 1):**
$$q(t) = \frac{q_i}{1 + D_i t}$$

**Hyperbolic decline (0 < b < 1):** Most common in practice.
$$q(t) = \frac{q_i}{(1 + b D_i t)^{1/b}}$$

Where:
- $q_i$ = initial production rate
- $D_i$ = initial decline rate (fraction/time period)
- $b$ = hyperbolic exponent (0–1; higher b = slower decline)

**Recoverable reserves by decline curve:**
$$EUR = \int_0^{t_{aban}} q(t) \, dt + N_p^{existing}$$

Where EUR = Estimated Ultimate Recovery and $t_{aban}$ = abandonment time (when rate reaches economic limit).

**In practice:** You plot production rate on semi-log paper vs time. If it falls on a straight line, it's exponential decline. You extrapolate to the economic limit rate to get EUR.

---

## Part 6: Pressure Transient Analysis (Well Testing)

When a well is produced at a constant rate and then shut in, the pressure behavior during buildup contains information about the reservoir.

### The Semi-Log Straight Line (Horner Plot)

For a buildup test, plot $P_{ws}$ (shut-in wellhead or downhole pressure) vs. $\log\left(\frac{t_p + \Delta t}{\Delta t}\right)$ on semi-log paper.

The straight-line portion of this plot gives:

$$k h = \frac{162.6 \, q B \mu}{m}$$

Where $m$ is the slope of the straight line (psi/log cycle) and $kh$ = permeability × net pay thickness.

**Skin factor (S):** A dimensionless number describing near-wellbore flow improvement or damage:
- $S > 0$: **Positive skin** = formation damage. Mud invasion, scale, clay swelling, fines migration. Reduces well productivity.
- $S = 0$: Clean well, undamaged
- $S < 0$: **Negative skin** = improved wellbore. Hydraulic fracture or acid stimulation has increased effective flow area.

**For Angola:** Most Angola deepwater wells have low or negative skin because the unconsolidated sands are highly permeable and typically undamaged. Positive skin is a warning sign of scale, asphaltene deposition, or near-wellbore condensate banking.

---

## Part 7: Reservoir Simulation Workflow

Reservoir simulation is how you combine all the above knowledge to build a predictive model of reservoir behavior.

### Step 1: Static Model (Geological Model)

The static model (built in Petrel) captures the 3D geometry and properties of the reservoir:
- Grid construction: 3D corner-point grid or structured Cartesian grid
- Seismic interpretation defines structural top and base
- Well log data (GR, porosity, Sw) are propagated through the grid using geostatistics (kriging, sequential Gaussian simulation)
- Result: 3D grid with porosity, permeability, and water saturation at every cell
- STOIIP: Sum of all cells: $STOIIP = \sum_{cells} \frac{V_{cell} \times \phi \times (1-S_w)}{B_{oi}}$

### Step 2: Initialization

Load the static model into the simulator (Eclipse, CMG IMEX, Intersect). Define:
- Initial pressure at datum depth
- Fluid contacts (OWC, GOC depth)
- Aquifer properties (if natural water drive)
- PVT tables (from laboratory fluid characterization)
- Relative permeability curves (from core flooding experiments)

**Initialization check:** The simulator must reproduce STOIIP from the static model. If the simulated STOIIP differs by > 3% from the static model, the grid or fluid contacts need to be revisited.

### Step 3: History Matching

History matching is the process of adjusting model parameters until the model reproduces the historical production and pressure data.

**What you match:**
- Field oil production rate (usually constrained as the "known" input)
- Field water production and water cut vs time
- Field gas production and GOR vs time
- Individual well bottomhole pressures from pressure gauges
- Shut-in pressure recovery from well tests

**What you adjust:**
- Permeability distribution (locally or by multiplier)
- Fault transmissibility (faults can be barriers or partially communicating)
- Relative permeability endpoints (Sor, Swcrit, krw, kro)
- Aquifer strength (Carter-Tracy aquifer model parameters)
- Horizontal-to-vertical permeability ratio (kv/kh)

**Automatic history matching:** Iterative algorithms (Ensemble Kalman Filter, Randomized Maximum Likelihood) perturb model parameters and minimize the mismatch. Available in Petrel INTERSECT, CMG CMOST, SLB Reservoir Characterization Studio.

**Manual history matching** (still very common, especially for experienced engineers):
1. Plot simulated vs observed GOR, water cut, BHP for each well
2. Identify which well is mismatching and what it tells you (too early water breakthrough → too high permeability on water channel? Too slow → low kh?)
3. Adjust locally and re-run
4. Iterate to global match

**The history match is never perfect.** The goal is "fit for purpose" — good enough to make reliable production forecasts. Typically targeting R² > 0.95 on field rates.

### Step 4: Prediction/Forecast

Once history-matched, run the model forward in time with assumed future operations:
- Infill wells (new wells)
- Water injection rates and locations
- Gas injection or WAG
- Surface constraints (FPSO plateau rate)

**P10/P50/P90 spread:**
Because the history match is non-unique (many models can match the history), run multiple history-matched realizations:
- **P90 (conservative):** Low EUR — optimistic enough that 90% of outcomes are above this
- **P50 (base):** Mid case — best engineering estimate
- **P10 (optimistic):** High EUR — only 10% of outcomes are above this

The range P10–P90 represents the reservoir uncertainty. For Angola deepwater fields, this uncertainty can be hundreds of millions of barrels of oil equivalent.

---

## Part 8: Reservoir Management in Angola

A field does not manage itself. After first oil, reservoir engineers continuously monitor and adjust to maximize recovery.

**Annual Field Review (AFR):** Required by ANPG for each producing block. The operator reviews:
- Production performance vs forecast
- Water injection performance
- Any identified opportunities (infill wells, workovers, ESP replacement)
- Updated reserves estimate

**Key reservoir management decisions:**

**Water injection timing:**
Most Angola deepwater fields inject water for pressure maintenance. The timing of water injection startup affects recovery. Too early → may bypass oil. Too late → reservoir depletes, productivity drops. Model studies guide this decision.

**Infill drilling:**
As the field matures, areas between existing wells may be poorly swept. 4D seismic (time-lapse seismic) identifies these areas. New wells (infill wells) are drilled to access bypassed oil. TotalEnergies has drilled multiple infill wells on Block 17 (Dalia, Pazflor) guided by 4D seismic — recovering hundreds of millions of additional barrels.

**EOR (Enhanced Oil Recovery):**
Angola's high-permeability turbidites are good candidates for WAG (Water Alternating Gas) injection. Injecting slugs of gas alternating with water improves displacement efficiency over water-only injection. Several Angola operators have tested WAG, and it is being evaluated for major deployments.

---

## Part 9: Pressure Transient Analysis — Angola Field Application

A well has been producing at 3,800 STB/day for 72 hours. The pump is shut in and a buildup test begins. Downhole gauges record pressure every minute.

**Build-up data:**

| Δt (hr) | P_ws (psi) | Horner time ratio [(tp+Δt)/Δt] |
|---------|-----------|-------------------------------|
| 0.1 | 3,820 | 721 |
| 0.5 | 4,050 | 145 |
| 1.0 | 4,210 | 73 |
| 2.0 | 4,380 | 37 |
| 5.0 | 4,620 | 15.4 |
| 10.0 | 4,780 | 8.2 |
| 24.0 | 4,940 | 4.0 |

Plot on semi-log paper (P_ws on Y axis vs log[(tp+Δt)/Δt] on X axis). The slope of the straight line = m.

$$kh = \frac{162.6 \, q B \mu}{m}$$

Angola deepwater typical inputs:
- q = 3,800 STB/day
- B = 1.38 RB/STB
- μ = 0.65 cP
- m = read from slope = approximately 380 psi/log cycle from the data above

$$kh = \frac{162.6 \times 3800 \times 1.38 \times 0.65}{380} = \frac{554,380}{380} = 1,459 \text{ mD·ft}$$

If net pay h = 45 ft (from logs): k = 32 mD (reasonable for a moderate Angola turbidite)

---

## Exercises — Reservoir Engineering

**Exercise 1: STOIIP Calculation**
A Block 17 reservoir compartment has:
- Area: 4.2 km² (= 1,038 acres)
- Average net pay: 18m (= 59 ft)
- Average porosity: 0.26
- Average Sw: 0.18
- Boi: 1.41 RB/STB

Calculate STOIIP in stock tank barrels and in million barrels. (Use 7758 conversion factor for acre-ft)

**Exercise 2: Production Decline**
A well starts production at 6,200 STB/day and shows exponential decline at Di = 0.18/year. Calculate:
1. Production rate after 2 years
2. Cumulative production after 2 years
3. Time to reach an economic limit of 500 STB/day

**Exercise 3: Material Balance**
An Angola block has produced 120 MMstb of oil and 95 MMscf/stb of gas (GOR tracking). Average reservoir pressure has dropped from 7,200 psi to 5,800 psi. The reservoir is a strong water drive system. PVT data: Bo = 1.35 RB/STB, Bg = 0.0065 RB/scf. There is no gas cap.

Using the simplified MBE $N_p B_o = N(B_o - B_{oi}) + W_e B_w$, estimate the cumulative water influx $W_e$ if N = 800 MMstb.

**Exercise 4: Well Test Permeability**
A buildup test in a Block 32 well shows a Horner slope of m = 425 psi/log cycle. Well production = 4,200 STB/day, B = 1.45 RB/STB, μ = 0.72 cP, net pay = 38 ft.
1. Calculate kh and k
2. From the test, the extrapolated P* = 6,800 psi. Reservoir pressure from static gradient = 6,780 psi. Are these consistent? What does a small discrepancy indicate?
3. Skin S = -0.5 from the test. Is the well damaged or stimulated? What does this mean physically?

---

## Interview Questions — Reservoir Engineering

1. An Angola Block 17 field has been producing for 12 years. The water cut has risen from 5% to 55%. What reservoir engineering analysis would you perform to understand the reason and propose remediation?
2. Explain the Havlena-Odeh method. What is it used for and what does a non-linear Havlena-Odeh plot indicate?
3. What is a P50 production forecast and how does it differ from P10 and P90? Why does the range matter to ANPG and the operator?
4. You are history matching a Block 32 field model. The simulated water cut at Well-7 is too early by 18 months. What parameters would you adjust and why?
5. What is 4D seismic and how has it been used to improve recovery in Angola?
6. What is the difference between Original Oil in Place (OOIP) and Reserves? What determines the Recovery Factor?
7. A Block 15 well shows a rapid GOR increase from 600 to 1,400 scf/STB. What are the possible causes and how would you investigate?
8. Explain relative permeability and how it affects water flooding efficiency.

---

*Next: [06_Drilling_Fluids_Tutorial.md](06_Drilling_Fluids_Tutorial.md) | See also: [08_Formation_Evaluation_Tutorial.md](08_Formation_Evaluation_Tutorial.md)*

Built by the geologist/geophysicist:
- Structural model: shape of the reservoir (from seismic)
- Stratigraphic model: layering and connectivity (from well logs)
- Petrophysical model: porosity, permeability, saturation distribution (from core + logs)

**Software:** Petrel (SLB), RMS (Roxar/Emerson)

### Step 2: Dynamic Model (Simulation Model)

The static model is upscaled and input into the reservoir simulator:
- Fluid PVT data (from lab reports)
- Relative permeability curves (from core analysis)
- Aquifer model
- Well locations, completions, production constraints

**Software:** Eclipse (SLB — industry standard), CMG (Computer Modelling Group — free student version available), IX (Intersect — SLB next-gen simulator)

### Step 3: History Match

The model is run from the start of production to the present. The simulated production is compared to actual production data. Parameters are adjusted until the model reproduces actual history within acceptable tolerances (typically ±5% cumulative production).

**History matching parameters adjusted:**
- Permeability distribution (most sensitive)
- Fault transmissibility
- Aquifer size and strength
- Relative permeability end-points

### Step 4: Forecast / Development Optimization

With a history-matched model, you can forecast future production under different development scenarios:
- How many infill wells are needed?
- What is the optimal water injection rate?
- Should we drill a horizontal or deviated well?
- What is the incremental recovery from a WAG injection scheme?

---

## Part 8: Reserves Classification (SPE-PRMS)

Reserves = the volumes of hydrocarbons anticipated to be commercially recovered from known accumulations from a given date.

**1P (Proved Reserves):** Reasonable certainty (≥90% probability) of commercial production. What banks lend money against.

**2P (Proved + Probable):** Best estimate (≥50% probability). Used for most economic analysis.

**3P (Proved + Probable + Possible):** Low certainty (≥10% probability). Exploration upside.

**Contingent Resources:** Technically recoverable but not yet commercially viable (awaiting development decision, infrastructure, or price).

Angola operators report reserves annually to ANPG using the SPE-PRMS framework.

---

## Part 9: Angola Turbidite Reservoir Context

Angola's deepwater reservoirs are turbidite sands — sediments deposited by underwater avalanche (turbidity current) flows from the continental shelf edge into the deep ocean. Key characteristics:

**Positive aspects:**
- High porosity: 22–32%
- High permeability: 100–2,000 mD in clean sands
- Low viscosity oil: 0.3–3 cP at reservoir conditions
- Combined: extremely productive wells. Peak rates of 20,000–50,000 bbl/day per well.

**Challenges:**
- **Heterogeneity:** Turbidite sands are internally complex — interbedded sands and shales, channelized geometry. Water floods poorly in some directions.
- **Unconsolidated:** High risk of sand production. Requires sand control completions.
- **Pressure support:** Naturally strong aquifer drive in some fields. Water cut rise can be rapid.
- **Reserves estimation uncertainty:** Complex geometry makes OOIP estimation uncertain. 2P/1P ratio often high early in field life.

**Typical Angola deepwater recovery factors:**
- Primary depletion alone: 15–25%
- With water injection: 35–50%
- With WAG: 40–55%
- Long-term with optimization: 55–65% in best fields

---

## Part 10: Practice Exercises

**Exercise 1:** A turbidite reservoir has the following parameters: Area = 12 km², thickness = 35m, porosity = 27%, Swi = 22%, Boi = 1.45 RB/STB. Calculate OOIP in STB.

**Exercise 2:** A well produces with initial rate 10,000 bbl/day and exponential decline rate Di = 0.08 per year. Calculate:
1. Production rate after 2 years
2. Cumulative production in 2 years
3. Time to reach abandonment rate of 500 bbl/day

**Exercise 3:** A build-up test gives a Horner semi-log straight line with slope m = 125 psi/log cycle. Well produced at q = 8,000 bbl/day, Bo = 1.35 RB/STB, μ = 0.8 cP. Net pay = 40m. Calculate permeability and kh.

**Exercise 4:** Draw the full reservoir simulation workflow from static model to forecast. Identify the main inputs and outputs at each step. Identify where a reservoir engineer spends most of their time.

---

## Part 11: Study Resources

| Resource | Format | Cost | Notes |
|---|---|---|---|
| CMG GEM/IMEX/STARS | Simulation software | Free student version (CMG.ca) | Install this — run your first model |
| "Fundamentals of Reservoir Engineering" — Craft, Hawkins, Terry | Textbook | Library | Classic material balance reference |
| "Well Testing" — Lee, Rollins, Spivey | Textbook | SPE | Complete PTA reference |
| "Principles of Applied Reservoir Simulation" — Fanchi | Textbook | Library | Good simulation theory book |
| Petex MBAL (Material Balance) | Software | Free student via Petex | Material balance tool |
| SPE OnePetro: search "Angola turbidite" | Papers | SPE student membership | Real Angola reservoir studies |
| IHS Markit (now S&P Global) production data | Online | School access may apply | Angola production history data |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/04_Reservoir_Path.md](../paths/04_Reservoir_Path.md)*  
*Where to learn: [learn.slb.com](https://learn.slb.com) (Petrel/Eclipse free) | [PROSPER student](https://www.petex.com/academic/) | [Learning Resources](../../../docs/learning-resources.md)*
