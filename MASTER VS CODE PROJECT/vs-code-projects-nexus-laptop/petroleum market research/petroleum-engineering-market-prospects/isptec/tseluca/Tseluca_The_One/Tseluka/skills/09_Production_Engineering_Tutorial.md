# Skill Tutorial 09 — Production Engineering

> **Applies to:** Production engineers (CORE), reservoir engineers (HIGH), subsea engineers (MEDIUM)
> **ISPTEC connection:** Engenharia de Produção de Hidrocarbonetos, Sistemas de Produção Superfície, Mecânica dos Fluidos
> **Goal:** Master IPR, VLP, nodal analysis, artificial lift, and production optimization at the level of a production engineer trainee.

---

## Part 1: The Production System

A producing well is a connected system. Every component from the reservoir to the export tanker interacts. Production engineering is the art of optimizing the entire system.

```
RESERVOIR
  │ (fluid flows through rock — inflow)
  │
WELLBORE / TUBING
  │ (fluid rises up the tubing — lift)
  │
WELLHEAD / CHOKE
  │ (pressure managed — surface control)
  │
FLOWLINE / RISER
  │ (transport to FPSO)
  │
FPSO PROCESS
  │ (separation, treatment)
  │
EXPORT
```

The production rate of the well is determined by **where the system is most restricted**. Your job as a production engineer: find and remove restrictions.

---

## Part 2: Inflow Performance Relationship (IPR)

The IPR describes how much oil the reservoir can deliver to the wellbore at a given flowing bottomhole pressure (FBHP).

### Darcy IPR (Single-phase liquid, no gas in reservoir)

For a simple undersaturated oil reservoir above bubble point:

$$q = \frac{k h}{141.2 B \mu} \cdot \frac{(P_r - P_{wf})}{\ln(r_e/r_w) - 0.75 + S}$$

Or in practical form using the Productivity Index (PI):

$$q = PI \times (P_r - P_{wf})$$

$$PI = \frac{q}{P_r - P_{wf}} \quad \text{[STB/day/psi]}$$

Where:
- $q$ = production rate (STB/day)
- $P_r$ = average reservoir pressure (psi)
- $P_{wf}$ = flowing wellhead pressure (converted to bottomhole)
- $S$ = skin factor

**Linear IPR line:** On a q vs $P_{wf}$ plot, a straight line from (0, $P_r$) to ($q_{max}$, 0).

### Vogel IPR (Two-phase below bubble point)

When reservoir pressure is below the bubble point, gas comes out of solution and the IPR becomes curved (gas reduces permeability to oil via relative permeability effects):

$$\frac{q}{q_{max}} = 1 - 0.2\left(\frac{P_{wf}}{P_r}\right) - 0.8\left(\frac{P_{wf}}{P_r}\right)^2$$

Where $q_{max} = \frac{q_0}{1 - 0.2(P_{wf}/P_r) - 0.8(P_{wf}/P_r)^2}$

**Angola deepwater wells:** Most are drilled and completed with reservoir pressure above or near bubble point initially. As depletion occurs over years, Vogel corrections become necessary.

---

## Part 3: Vertical Lift Performance (VLP) — The Tubing Performance Curve

The VLP (also called Tubing Performance Curve or Outflow curve) describes the pressure required at the bottomhole to lift fluid to surface at a given flow rate.

**What controls VLP shape:**
- **Tubing size:** Larger tubing = lower friction loss at the same rate = lower required FBHP = easier lift
- **Water cut:** Higher water cut = heavier fluid = more hydrostatic head to lift = higher required FBHP
- **GOR:** Gas helps lift fluid (reduces hydrostatic head) but at very high rates, gas causes friction losses
- **Surface backpressure:** From the separator, choke, and flowline

**The VLP curve is U-shaped on a q vs FBHP plot:**
- At very low rates: VLP is high (friction low but high hydrostatic due to slow, heavy mixture)
- At moderate rates: VLP is minimum (optimum lifting conditions)
- At high rates: VLP increases (friction losses dominate)

**Gradient curves:** Pre-calculated tables and charts showing pressure gradients for different flow rates, GLRs, and tubing sizes. Found in "Brown's Gas Lift Manual" and built into software (Prosper, Pipesim).

---

## Part 4: Nodal Analysis

Nodal analysis is the core technique for well performance analysis and optimization. The concept: choose a "node" in the system (usually bottomhole or wellhead), calculate the pressure at that node from two directions (inflow and outflow), and find where they balance.

### Bottomhole as Node

**IPR (Inflow):** For a given $q$, reservoir delivers $P_{wf}$ = $P_r$ - $q/PI$. Plot: $q$ on x-axis, $P_{wf}$ on y-axis, **downward sloping line**.

**VLP (Outflow):** For a given $q$, the tubing requires a minimum $P_{wf}$ to lift fluid to surface. Plot: $q$ on x-axis, $P_{wf}$ on y-axis, **U-shaped curve**.

**Operating point:** Where IPR and VLP curves intersect. This is the natural flow rate of the well.

```
P_wf
 │  IPR (inflow) \
 │                \         ← Operating Point
 │                 ×
 │                / ← VLP (outflow — U shape minimum here)
 │               /
 └─────────────────── q
```

### Effect of Choke on Operating Point

The surface choke adds backpressure to the system. Increasing choke restriction:
- Raises the VLP curve (more pressure needed at bottomhole to overcome the backpressure)
- Moves the operating point LEFT (lower rate) and HIGHER on P_wf axis

**Why choke?** Rate control, well testing isolation, prevent slugging, manage drawdown to prevent sand production, prevent flowing below bubble point.

---

## Part 5: Skin Factor

Skin ($S$) is a dimensionless parameter in the well-flow equations that accounts for near-wellbore effects:

$$\Delta P_{skin} = \frac{141.2 q B \mu}{k h} \times S$$

**Positive skin (formation damage):**
- Mud invasion, filter cake in perforated zones
- Fines migration plugging pore throats
- Scale deposits (calcium carbonate, barium sulfate)
- Paraffin or asphaltene deposition
- Poor perforation design

**Negative skin (stimulation):**
- Hydraulic fracture
- Matrix acid stimulation (HCl acid dissolves carbonate damage, HF for sandstone)
- Good perforation design (high density, phasing)

**Equivalent wellbore radius:**
$$r_{wa} = r_w \cdot e^{-S}$$

Negative skin = larger effective wellbore. A well with S = -5 behaves as if it has a wellbore radius 148× larger than the physical bit size.

---

## Part 6: Gas Lift

Gas lift is the most common artificial lift method in Angola deepwater. Gas (from the FPSO compressors) is injected through the casing annulus, down to a gas lift valve in the tubing, and into the tubing to aerate the oil column.

**Why gas lift works:**
By injecting gas into the tubing, you reduce the average density of the fluid column. A lighter fluid column requires less bottomhole pressure to reach the surface → the IPR/VLP operating point moves to a higher production rate.

### Gas Lift System Components

- **Gas lift compressors on FPSO:** Compress the separated gas back to 100–350 bar (depending on the well)
- **Gas injection riser:** Carries high-pressure gas from FPSO down to the seabed
- **Gas injection manifold:** Distributes gas to multiple wells
- **Gas injection umbilical/line:** Carries gas down the casing annulus to the downhole valve
- **Gas Lift Valve (GLV):** Installed in the tubing at the designed injection depth. Allows gas to enter the tubing from the annulus at a specific injection pressure.
- **Mandrels:** Housings welded onto the tubing string that hold the GLVs. Multiple mandrels installed at different depths = flexibility to change injection depth by wireline operations.

### GLR Optimization

**Optimum GLR (Gas-Liquid Ratio):** There is an optimum amount of gas to inject per barrel of liquid. Too little = well underperforming. Too much = overinjection causing extra friction and actually reducing rate. The optimum is found from VLP gradient curves and confirmed by well testing.

**FPSO gas allocation:** The total available gas lift gas on the FPSO is limited. The production engineer allocates it among all producing wells to maximize total FPSO oil production. This is a classic optimization problem solved with Prosper/GAP software.

---

## Part 7: Electrical Submersible Pumps (ESP)

An ESP is a centrifugal pump system run into the tubing on the end of the production tubing string. It is driven by an electric motor at downhole.

**Components (bottom to top in well):**
1. Motor (electric, 3-phase) — typically 100–2,000+ HP
2. Motor protector — seals motor from wellbore fluid, handles shaft thrust
3. Intake — fluid entry into pump
4. Multi-stage centrifugal pump (20–500+ stages) — each stage adds head pressure
5. Cable — power supply from surface to motor (3-conductor power cable alongside tubing)
6. Variable Speed Drive (VSD) at surface — controls motor speed (frequency) = controls flow rate

**When to use ESP over gas lift:**
- High water cut wells (gas lift inefficient for mostly water)
- Deep wells with low reservoir pressure
- High GOR can damage ESP impellers (gas lock problem)

**ESP monitoring parameters:**
- Motor current (amperage) — increases with load, trips on overcurrent
- Motor temperature — high temp = pump running dry or mechanical problem
- Pump intake pressure — confirms drawdown performance
- Vibration — impeller wear or gas lock indicator

---

## Part 8: Production Decline Analysis

See [05_Reservoir_Engineering_Tutorial.md](05_Reservoir_Engineering_Tutorial.md) Part 5 for Arps decline equations.

**Practical decline curve analysis workflow:**

1. **Gather production data:** Monthly production rates (STB/month or bbl/day) from FPSO allocation
2. **Plot rate vs time** on semi-log paper (rate on log scale)
3. **Identify straight-line section** (exponential decline)
4. **Calculate decline rate Di:** Slope of the straight line = -Di
5. **Extrapolate to economic limit rate** (cost of production per barrel = oil price at abandonment)
6. **Calculate EUR** (Estimated Ultimate Recovery): Area under the rate-time curve

**Multi-well analysis for an FPSO:** Each well is analyzed individually. Total FPSO forecast = sum of all individual well forecasts. New wells and workovers are added to the base decline forecast.

---

## Part 9: Production Allocation

On an FPSO, the total export meter measures one combined oil production number. But there are 20–60 individual wells. How do you know how much each well produced?

**Well Test Allocation:** Each well is periodically tested through the test separator (see FPSO tutorial). The test gives:
- Individual well oil rate ($q_{oil,test}$)
- Water cut
- GOR

**Allocation factor calculation:**
$$AF_i = \frac{q_{oil,i}^{test}}{\sum_{j=1}^{n} q_{oil,j}^{test}}$$

**Daily allocation:**
$$q_{oil,i}^{allocated} = AF_i \times Q_{FPSO}^{total}$$

This allocated production is what gets reported to ANPG for royalty and cost oil calculations. The accuracy of well tests directly affects revenue attribution.

**Complication — well status changes:** Wells are shut in for maintenance, brought on for workovers, gas lift rate changes. Each status change requires an updated allocation model. In practice, the production technologist updates the allocation model daily.

---

## Part 10: Production Surveillance and Well Performance Monitoring

### Key Performance Indicators per Well

The production engineer monitors each well daily against these metrics:

| Metric | Calculated How | Trend to Watch |
|--------|---------------|----------------|
| **PI (Productivity Index)** | $PI = q / (P_{res} - P_{wf})$ | Declining PI → damage or depletion |
| **Water cut** | $WC = q_{water} / (q_{oil} + q_{water})$ | Rising WC → water breakthrough |
| **GOR** | $GOR = q_{gas} / q_{oil}$ | Rising GOR → gas cone or reservoir depletion |
| **Wellhead pressure (WHP)** | Topside sensor | Declining WHP → reservoir declining or restriction upstream |
| **Gas lift injection rate** | Topside meter | Increasing GL to maintain same rate → well declining |

### Decline Curve Surveillance

Plot each well's oil rate vs time on semi-log scale. Fit the exponential decline line. Monitor:
- Is the well following the decline trend? (Expected)
- Is the well declining FASTER than the trend? (Problem — investigate)
- Has a step-change occurred? (Workover, ESP change, gas lift optimization — document it)

**Monthly well performance review:** The production engineer prepares a one-page "well card" for each well showing rate history, water cut, GOR, WHP, and GL rate trends. Deviations from trend trigger investigation.

---

## Part 11: Gas Lift Optimization — Angola FPSO Level

With 20–50 gas lift wells on one FPSO and a fixed amount of gas available from the compressors, allocating gas optimally among wells maximizes FPSO production.

### Problem Statement

**Given:**
- Total GL gas available: $G_{total}$ MMscf/day
- For each well $i$: a performance curve $q_{oil,i}(G_{inj,i})$ (incremental oil vs gas injected)

**Objective:** Maximize $\sum_{i=1}^{n} q_{oil,i}$ subject to $\sum_{i=1}^{n} G_{inj,i} = G_{total}$

**Optimal condition:** The incremental oil per MMscf of gas injection is equal across all wells:

$$\frac{dq_i}{dG_i} = \frac{dq_j}{dG_j} \quad \forall \, i, j$$

This is solved using Prosper+GAP (SLB) or PIPESIM (Schlumberger) in practice.

**Angola example (Block 17 Dalia FPSO):**
- 36 gas lift wells on one FPSO
- Total GL gas available: 180 MMscf/day
- Optimal allocation generates 8,000–12,000 bbl/day more than naive equal distribution
- Annual revenue impact: ~$220M/year at $50/bbl (40 years × 8,000 bbl/day × 365 × $50 = $5.8 billion over field life)

---

## Part 12: ESP Management and Monitoring

### Monitoring an ESP Well Remotely

An ESP well on an Angola FPSO streams data continuously via PI historian:

**Parameters monitored:**
- **Motor current (amps):** Steady current = good operation. Trending up = pump working harder (increasing head or increasing fluid viscosity). Trip point (max current) = overload protection.
- **Motor temperature:** High temp = running dry (low fluid inflow), or mechanical friction. Trip on high temperature.
- **Pump intake pressure (PIP):** Low PIP = the reservoir is not supplying enough fluid (drawdown limited). High PIP = ESP undersized or partially blocked.
- **Discharge pressure:** Pump discharge — confirms pump is developing the correct head.
- **Vibration (accelerometer):** High vibration = bearing wear, imbalance, gas locking, sand ingestion.
- **Cable insulation resistance:** Measured offline during shutdowns. Declining insulation resistance = cable jacket damage, moisture ingress.

### Gas Locking

The ESP's centrifugal stages require liquid to function. If free gas ingestion is too high, the impellers lose their prime and the pump becomes inefficient ("gas locked"). Symptoms:
- Current drops suddenly
- Motor temperature rises (pump running fast but no fluid being moved)
- Production drops

**Solutions:**
- Choke back the well to reduce drawdown (reduces gas breakout near wellbore)
- Install a gas separator (advanced gas handler) above the pump intake
- Change to a higher-GOR tolerant pump design

---

## Part 13: Production Optimization Workflow

### The Daily Optimization Loop

```
Morning meeting: Production engineer reviews 24-hour data
        │
        ├── Any wells offline? → Root cause, restore as priority
        ├── FPSO below plateau target? → Identify and remove bottlenecks
        ├── Any well performance deviations? → Investigate and schedule action
        └── Gas allocation optimized? → Update Prosper/GAP model if changes
                │
Afternoon: Update daily production report (submitted to ANPG by 18:00)
                │
Weekly: Well performance review meeting with operations team
                │
Monthly: Detailed production analysis submitted to ANPG (block production report)
```

### Integrated Production Modelling (IPM)

For complex Angola fields, a full integrated model is built:
- **Reservoir model** (Eclipse/CMG) provides deliverability profiles
- **Well model** (Prosper) models each well (IPR + VLP + artificial lift)
- **Network model** (GAP) connects wells → manifolds → flowlines → risers → FPSO
- **Process model** (HYSYS or OLGA) models topside processing constraints

The integrated model can simulate "what if" scenarios: What happens to total FPSO production if Well-A is shut for 2 weeks? What is the optimal gas lift gas distribution for Q3?

**Software combination most common in Angola:** Prosper + GAP (SLB/Petroleum Experts), connected to Eclipse reservoir. SLB refers to this as "Integrated Asset Model (IAM)."

---

## Exercises — Production Engineering

**Exercise 1: Nodal Analysis — Operating Point**
A Block 17 gas lift well has:
- Reservoir pressure: 4,100 psi
- PI = 6.5 STB/day/psi
- VLP curve minimum FBHP at q = 4,000 STB/day = 2,800 psi
- VLP (simplified): FBHP = 1,500 + 0.325 × q (psi, where q is in STB/day)

1. Find the operating rate using the IPR equation: $q = PI \times (P_r - P_{wf})$ and the VLP equation simultaneously
2. What is the operating FBHP?
3. If you increase gas lift injection to reduce the VLP constant from 1,500 to 1,200 psi, what is the new operating rate?

**Exercise 2: ESP Design (Simplified)**
A completion requires an ESP to lift 8,000 bbl/day against a total dynamic head of 3,500 ft. A pump stage produces 18 ft of head at 8,000 bbl/day flow rate in the operating range.
1. How many stages are required?
2. If the motor efficiency is 92% and pump efficiency is 74%, calculate the hydraulic power required: $P_{hydraulic} = \frac{q \times \rho \times g \times TDH}{\eta_{pump} \times \eta_{motor}}$ (convert 8,000 bbl/day to m³/s first; TDH in meters)

**Exercise 3: Gas Lift Optimization**
Two wells on an FPSO both receive gas lift injection. Total available gas = 8 MMscf/day.

| Gas Injection (MMscf/day) | Well A oil rate (STB/day) | Well B oil rate (STB/day) |
|--------------------------|--------------------------|--------------------------|
| 1 | 1,800 | 2,200 |
| 2 | 2,600 | 3,000 |
| 3 | 3,200 | 3,600 |
| 4 | 3,650 | 4,050 |
| 5 | 3,950 | 4,400 |
| 6 | 4,100 | 4,650 |

Currently Well A gets 4 MMscf/day and Well B gets 4 MMscf/day = 7,700 STB/day total.

Find the optimal allocation (must sum to 8 MMscf/day) by comparing incremental oil per MMscf injected for each well.

**Exercise 4: Decline Curve**
A Block 15 well produced 5,500 STB/day at start-up. After 18 months, it produces 3,900 STB/day (exponential decline observed).
1. Calculate the annual decline rate Di
2. Predict the rate at Year 3 and Year 5
3. If the economic limit is 500 STB/day, when does the well reach abandonment?
4. Calculate EUR (integrate exponential decline from t=0 to t_abandon)

---

## Interview Questions — Production Engineering

1. An Angola gas lift well has been producing at 4,200 STB/day for 8 months. This month's test shows 3,100 STB/day with the same reservoir pressure and GL injection rate. What is your diagnostic process?
2. Explain nodal analysis. Draw the IPR and VLP curves and mark the operating point.
3. What is the skin factor and what are the most common causes of positive skin in Angola deepwater wells?
4. Why is gas lift the dominant artificial lift method in Angola deepwater rather than ESP?
5. An FPSO processes 180,000 bbl/day from 40 wells. You need to allocate production to each well without testing them all simultaneously. Describe your allocation methodology.
6. What is Integrated Production Modelling (IPM) and what software is used for it in Angola?
7. A well shows sudden GOR increase from 800 to 2,400 scf/STB. The reservoir pressure has not changed. What are the possible causes?
8. How does water cut affect gas lift performance? What happens to the VLP curve as water cut increases?

---

*Next: [10_Completions_Tutorial.md](10_Completions_Tutorial.md) | See also: [03_FPSO_Operations_Tutorial.md](03_FPSO_Operations_Tutorial.md)*

**Production allocation methods:**

1. **Test separator allocation:** Route each well to the FPSO's dedicated test separator periodically. Measure individual rates. Use these test rates as allocation factors until the next test.

2. **Virtual metering / multiphase flow metering:** Mathematical models or subsea multiphase meters estimate each well's rate using wellhead pressure, temperature, and choke position.

3. **Subsea multiphase meter:** Installed on some Angola wells on the subsea tree. Measures rate of each phase (oil, water, gas) in real time at the seabed. Most accurate but expensive.

**Why allocation matters:**
- Reservoir management decisions depend on knowing individual well performance
- Production sharing agreements require accurate allocation for commercial purposes
- ANPG reporting requires field-level production data

---

## Part 10: Flow Assurance at the Production Level

**Hydrate prevention (production side):**
- Continuous MEG injection at the wellhead via umbilical
- MEG recovered at the FPSO and regenerated (MEG regeneration unit)

**Wax management in tubing:**
- Chemical injection (wax inhibitor) at wellhead
- Periodic hot-oiling (pumping hot oil down the tubing to melt wax deposits)
- Wax scrapers on wireline (pigging is not done in production tubing)

**Asphaltene management:**
- Asphaltene inhibitor injection at wellhead
- If asphaltene deposits form in tubing: coiled tubing mechanical scraping or chemical solvent treatments

**Scale management:**
- Scale inhibitor injection (continuous or periodic squeeze)
- Periodic wellbore cleanout by acid treatment (downhole scale removal)

---

## Part 11: Prosper (Petroleum Experts IPM) Workflow

Prosper is the industry-standard production engineering software. Learn this tool — it appears in nearly every production engineer job interview.

**Basic Prosper workflow:**

```
1. Create a new well model

2. Input PVT data:
   - Fluid type (oil/gas)
   - Reservoir temperature, pressure
   - Oil gravity (API), GOR, water cut
   - PVT correlation (Vasquez-Beggs, Standing, etc.)

3. Input reservoir data:
   - Reservoir pressure
   - PI or k, h, skin, drainage radius

4. Input completion data:
   - Tubing size and depth
   - Perforated intervals

5. Run IPR calculation → generates IPR curve

6. Input VLP (vertical lift) data:
   - Correlations or gradient curves
   - Tubing size, inclination

7. Solve for operating point → model predicts q

8. Validate against actual well test data

9. Sensitivity analysis:
   - Effect of declining reservoir pressure on rate
   - Effect of increasing water cut on rate
   - Optimize gas lift injection rate
   - Evaluate infill well candidates
```

**Free student version:** Available from Petroleum Experts (petex.com/products/ipm/student/). Install it and run through their tutorials.

---

## Part 12: Practice Exercises

**Exercise 1:** A well has reservoir pressure 350 bar and PI = 15 STB/day/bar. Calculate the production rate at flowing bottomhole pressures of: 320, 300, 250, 200, 150, 100, 50 bar. Plot the IPR curve.

**Exercise 2:** Using your IPR from Exercise 1, add a VLP (use simplified gradient: $P_{wf}$ = WHP + 0.4 × q + 3,200 ft × 0.35 psi/ft, for a 5" tubing well, WHP = 300 psi). Where is the operating point?

**Exercise 3:** A well has a skin factor of +8. The reservoir k = 500 mD, h = 35m, q = 5,000 STB/day, B = 1.4 RB/STB, μ = 0.9 cP. Calculate the pressure drop due to skin. What would the additional production be if skin were reduced to 0 by acid stimulation?

**Exercise 4:** An FPSO has 6 gas lift wells sharing 10 MMscfd of available gas lift. Well data and optimum gas injection rates from gradient curves: Well A needs 2 MMscfd (gives 8,000 bbl/day), Well B 1.5 (7,200), Well C 1.8 (6,500), Well D 2.2 (9,000), Well E 1.0 (4,000), Well F 2.5 (10,500). Total demand = 11 MMscfd > available 10. How do you allocate gas to maximize total production? Which well do you cut back, and by how much?

---

## Part 13: Study Resources

| Resource | Format | Notes |
|---|---|---|
| Prosper / IPM Suite (Petex) | Free student software | **Most important — install and use before interview** |
| "Production Optimization Using Nodal Analysis" — Brown | Textbook | The classic reference for this entire tutorial |
| "Natural Flow Performance" — Beggs | Textbook | IPR, VLP, flow correlations |
| "Gas Lift Theory and Practice" — Brown | Textbook | Complete gas lift reference |
| Petex training tutorials (YouTube) | Video | Prosper worked examples |
| SPE papers: search "Angola gas lift optimization" | OnePetro | Real Angola cases |
| Rigzone production engineering section | Online | Free introductory content |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/02_Production_FPSO_Path.md](../paths/02_Production_FPSO_Path.md)*  
*Where to learn: [PROSPER student license](https://www.petex.com/academic/) | [PetroWiki](https://petrowiki.spe.org/Artificial_lift) | [Learning Resources](../../../docs/learning-resources.md)*
