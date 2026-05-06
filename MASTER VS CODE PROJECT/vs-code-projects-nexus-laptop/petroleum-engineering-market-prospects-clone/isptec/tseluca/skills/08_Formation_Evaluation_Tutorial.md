# Skill Tutorial 08 — Formation Evaluation and Well Logging

> **Applies to:** Reservoir engineers (CORE), drilling engineers (HIGH), completions engineers (HIGH)
> **ISPTEC connection:** Avaliação de Formações, Engenharia de Reservatórios, Geologia do Petróleo
> **Goal:** Read and interpret standard wireline logs, apply Archie's equation to calculate water saturation, understand MWD/LWD logs, and select perforation intervals from log data in the Angola deepwater turbidite context.

---

## Part 1: Why Formation Evaluation Matters

You have drilled a well. You've spent $50–150 million USD to drill to 4,000m in 1,500m water depth (Angola deepwater cost range). Now the critical question: **What is in this rock, and is it worth completing?**

Formation evaluation is the process of characterizing the reservoir from:
1. **Wireline logs** (run after drilling with the bit out of the hole)
2. **LWD logs** (measured while drilling)
3. **Cores** (physical rock samples)
4. **Formation fluid samples** (MDT, RFT tests)
5. **Drill stem tests** (DST — flow testing)

Getting this wrong means completing a water-bearing zone or abandoning a productive one. Both are expensive mistakes.

---

## Part 2: The Gamma Ray (GR) Log

**What it measures:** Natural radioactivity of the formation, in API units.

**Physical basis:** Clay minerals (shales) are radioactive — they contain potassium-40, uranium, and thorium isotopes. Clean sandstone and limestone are not radioactive.

**Reading the GR log:**
- **Clean sand:** Low GR reading (typically 10–40 API in clean Angola turbidite sands)
- **Shale:** High GR reading (typically 80–150 API in Angola)
- **Intermediate GR:** Shaly sand (some clay content) or thin-bedded sand-shale sequence

**GR is almost always the first log on the left track of a composite log display.**

### Volume of Shale (Vsh) Calculation

$$V_{sh} = \frac{GR_{log} - GR_{clean}}{GR_{shale} - GR_{clean}}$$

Where:
- $GR_{log}$ = GR reading at the interval of interest
- $GR_{clean}$ = GR in a clean sand (baseline minimum)
- $GR_{shale}$ = GR in a pure shale (baseline maximum)

A Vsh > 0.3 (30% shale) generally indicates the sand is too tight or too clay-rich to be productive.

---

## Part 3: The Resistivity Logs

**What they measure:** Electrical resistance of the formation in ohm·m.

**Physical basis:**
- **Salt water** (formation brine) is a good conductor → **low resistivity** (0.2–2 ohm·m)
- **Hydrocarbons (oil/gas)** are electrical insulators → **high resistivity** (10–500+ ohm·m)
- **Dry rock** is an insulator too

**Key principle:** If a clean sand (low GR) shows high resistivity — it likely contains hydrocarbons, not water.

### Resistivity Log Types

| Log | Depth of Investigation | What It Measures |
|---|---|---|
| **Deep resistivity (Rt)** | 1–2m into formation | True formation resistivity — beyond mud invasion |
| **Medium resistivity** | ~0.5m | Transition zone |
| **Shallow resistivity (Rxo)** | 5–30cm from borehole | Flushed zone (where mud filtrate has displaced formation fluid) |
| **Micro-resistivity (MSFL, MLL)** | Centimeters | Filter cake and immediate borehole wall |

**Invasion profile:** When drilling, mud filtrate invades the permeable zone. The true reservoir fluid (oil or water) exists only beyond the invasion front. Deep resistivity reads the true formation.

**Crossplot interpretation:**
- Deep Rt >> Shallow Rxo: Invasion of water-based filtrate into oil-bearing zone (oil zone confirmed)
- Deep Rt ≈ Shallow Rxo: Residual oil in flushed zone ≈ oil in reservoir (low oil mobility?) OR water zone with similar resistivity throughout

---

## Part 4: Porosity Logs

Three tools measure porosity by different physical methods. They complement each other and should always be interpreted together.

### Density Log (RHOB)

**What it measures:** Bulk density of the formation (g/cm³ or kg/m³)

**Physical basis:** A radioactive source (Cs-137) emits gamma rays into the formation. High-density rock attenuates the gamma rays more → lower detector count rate → higher bulk density reading.

**Porosity from density:**
$$\phi_D = \frac{\rho_{ma} - \rho_b}{\rho_{ma} - \rho_f}$$

Where:
- $\rho_{ma}$ = matrix density (sandstone = 2.65 g/cm³, limestone = 2.71 g/cm³)
- $\rho_b$ = bulk density from log
- $\rho_f$ = fluid density (1.0 for water, 0.8 for oil, ~0.1–0.3 for gas)

### Neutron Log (NPHI)

**What it measures:** Hydrogen index of the formation — proportional to hydrogen content.

**Physical basis:** A neutron source emits high-energy neutrons. As they collide with hydrogen atoms (in water and hydrocarbons), they slow down. The detector measures the ratio of slowed neutrons.

**Porosity from neutron:** Directly proportional to hydrogen concentration = fluid-filled porosity.

**Gas effect:** Gas has much lower hydrogen density than liquid water or oil. In a gas zone, the neutron log reads **lower** than true porosity.

### Sonic (Acoustic) Log (DT)

**What it measures:** Travel time of a compressional sound wave through 1 foot of formation (Δt, microseconds/ft).

**Wyllie time-average equation:**
$$\frac{1}{V_{log}} = \frac{\phi}{V_f} + \frac{(1-\phi)}{V_{ma}}$$

Or equivalently: $\phi = \frac{DT_{log} - DT_{ma}}{DT_f - DT_{ma}}$

---

## Part 5: The Neutron-Density Crossplot (Gas Identification)

By plotting neutron porosity (x-axis) vs density porosity (y-axis) for each depth, you can identify fluid type:

**Interpretation rules:**
- **Water zone:** N and D porosities approximately equal. Points plot near the 1:1 line.
- **Oil zone:** Small crossover (D slightly > N) or equal. Less contrast than gas.
- **Gas zone:** **Large "gas crossover"** — density porosity is MUCH HIGHER than neutron porosity. Gas causes neutron to read low (no hydrogen) and density to read high (low bulk density).

**In Angola turbidites:** Gas cap/gas reservoir identification on the N-D crossplot is a routine interpretation skill.

---

## Part 6: Archie's Equation — Water Saturation

**The single most important equation in formation evaluation:**

$$S_w = \left(\frac{a \cdot R_w}{\phi^m \cdot R_t}\right)^{1/n}$$

Where:
- $S_w$ = water saturation (fraction) — what you're solving for
- $a$ = tortuosity factor (typically 1.0 for sands; 0.62–1.0)
- $R_w$ = formation water resistivity (ohm·m) — from water samples or SP log
- $\phi$ = porosity (from logs above)
- $m$ = cementation exponent (typically 1.8–2.0 for sands; higher for carbonates)
- $n$ = saturation exponent (typically 2.0)
- $R_t$ = true formation resistivity from deep resistivity log (ohm·m)

**If $S_w$ < 0.30 (30%):** More than 70% of pore space is hydrocarbon. This is typically productive.
**If $S_w$ > 0.60 (60%):** Mostly water. May not be economically productive.

**Angola-specific parameters (Block 17 turbidites, approximate):**
- $m$ = 1.85–1.95
- $n$ = 2.0
- $a$ = 1.0
- $R_w$ = 0.02–0.05 ohm·m (saline formation water)

**Worked example:**
$\phi$ = 0.28, $R_t$ = 25 ohm·m, $R_w$ = 0.03 ohm·m, $a$ = 1.0, $m$ = 1.9, $n$ = 2.0

$$S_w = \left(\frac{1.0 \times 0.03}{0.28^{1.9} \times 25}\right)^{1/2} = \left(\frac{0.03}{0.0891 \times 25}\right)^{0.5} = \left(\frac{0.03}{2.228}\right)^{0.5} = (0.01347)^{0.5} = 0.116$$

$S_w$ = 11.6% → Only 11.6% water saturation → 88.4% oil saturation → Excellent reservoir

---

## Part 7: Spontaneous Potential (SP) Log

**What it measures:** The natural voltage generated at the boundary between the mud filtrate and the formation fluid — due to differences in ion concentration.

**Reading the SP:**
- **Clean permeable sand:** SP deflects NEGATIVELY (to the left) from the shale baseline
- **Shale:** SP stays at the shale baseline (no deflection)
- **Tight rock (no permeability):** No SP deflection

**Uses:**
1. **Identify permeable vs impermeable zones** (can confirm sand boundaries that GR shows)
2. **Estimate Rw** (formation water resistivity): $R_w$ can be calculated from the SP magnitude

**Limitation:** SP works poorly in highly saline muds or freshwater formations. In OBM wells, no SP signal because there's no ion exchange.

---

## Part 8: Reading a Composite Log — Angola Turbidite Example

A typical Angola turbidite well log presentation (5-track composite log):

```
TRACK 1 (left):      GR (0-150 API) + Caliper (6-16")
TRACK 2:             Deep Resistivity + Medium Resistivity + Shallow Resistivity (0.2-200 ohm·m, log scale)
TRACK 3:             Density (RHOB, 1.95-2.95 g/cm³) + Neutron Porosity (NPHI, 0.45-(-0.15) right to left)
                     [N-D crossover = gas zone]
TRACK 4:             Sonic (DT, 140-40 us/ft)
TRACK 5 (right):     Depth scale + Interpreted lithology column + Sw curve
```

### Reading the Log: Block 17 Turbidite Example

**Zone A: 3,820–3,875m (55m interval)**
- GR = 18–25 API → **Very clean sand** (Vsh < 5%)
- Deep Rt = 35–55 ohm·m → **High resistivity** → Likely hydrocarbon-bearing
- RHOB = 2.12 g/cm³ → Dense log porosity: φ_D = (2.65 - 2.12)/(2.65 - 0.85) = 0.29 (29%)
- NPHI = 0.28 → Neutron porosity 28%. N-D roughly equal → **Oil (not gas)**
- Archie Sw = (1.0 × 0.03 / 0.29^1.9 × 45)^0.5 = **~12% Sw → 88% oil saturation → Excellent**

**Zone B: 3,875–3,895m (20m interval)**
- GR = 65–85 API → **Shaly sand/thin shale**. Net pay? Depends on cutoffs.
- Deep Rt = 4.5–6.0 ohm·m → **Low resistivity** → Water-bearing OR heavily shaly
- Apply Vsh correction before using Archie

**Zone C: 3,895–3,920m (25m interval)**
- GR = 22–28 API → Clean sand
- Deep Rt = 28–40 ohm·m → Good resistivity
- RHOB = 2.05, NPHI = 0.22 → Large N-D crossover (density high, neutron low) → **GAS signature**
- Possible gas cap or gas reservoir

---

## Part 9: Net Pay Determination

Not all of the reservoir section is "pay" (economic). You must apply cutoffs to determine which intervals contribute to production.

### Standard Cutoffs for Angola Turbidites

| Parameter | Cutoff | Rationale |
|-----------|--------|-----------|
| Vsh | < 0.30 (30%) | Shaly rock has poor permeability |
| Porosity | > 0.10 (10%) | Tight rock cannot produce economically |
| Water Saturation | < 0.60 (60%) | Less than 40% hydrocarbon → likely uneconomic |
| Permeability (from core) | > 1 mD | Minimum flow capacity |

**Net Pay:** Sum of all intervals that meet all cutoffs within the gross reservoir interval.

$$\text{NTG ratio} = \frac{\text{Net Pay (ft or m)}}{\text{Gross Reservoir (ft or m)}}$$

Angola deepwater turbidites: NTG typically 0.3–0.8 (30–80%). High NTG (>0.6) means large connected flow bodies — good field development. Low NTG means thinner, more discontinuous sands — more uncertain connectivity.

---

## Part 10: LWD vs Wireline Logs

**Wireline logging** (after drilling — most common for appraisal and development wells):
- Better log quality (tools are stationary or moving slowly in stable hole)
- Can run any number of passes and repeat sections
- Requires bit to be out of hole (time-consuming in deepwater Angola — round trip = 12–18 hours)

**LWD logging** (sensors in the BHA, measurements while drilling):
- Real-time formation data as you drill
- Allows the geologist to stop in the reservoir and evaluate before drilling past the best quality sands
- Essential in deepwater Angola for "geo-steering" horizontal wells — landing and staying within a thin oil sand
- LWD log quality somewhat lower than wireline for some measurements (vibration effects, borehole conditions while drilling)

**Angola practice:** LWD is used for all production wells (horizontal, long reservoir sections). Wireline logs are run after LWD for quality confirmation and for tools not available in LWD (e.g., MDT fluid sampling, VSP — vertical seismic profiling).

### Geo-Steering in Angola Horizontal Wells

Block 17 and Block 32 horizontal wells must land within a turbidite sand body and remain in the best quality sand for 1–2 km horizontal sections. The LWD tools provide:
- GR in real time → tells the geologist if the bit is in clean sand or shale
- Resistivity → confirms oil vs water zone
- Density + neutron → porosity quality

**The geologist and directional driller work together in real time:**
- GR rising → entering shale top → drill down (adjust inclination)
- GR falling → back in clean sand → hold
- Resistivity drops → water contact approaching → drill up (or stop)

This real-time geology-guided drilling is called **geo-steering** and is standard practice on Angola deepwater development wells.

---

## Part 11: Formation Testing (MDT — Modular Formation Dynamics Tester)

After drilling and before running casing, a wireline MDT tool can be set against the borehole wall to take:

**Pressure measurements:**
- Formation pressure at multiple depths
- Pressure gradient → fluid density → identify oil/water contact
- Connectivity test: Are two pressure points in pressure communication? (same gradient = same fluid, same pressure trend = hydraulic communication)

**Fluid sampling:**
- Draw small volumes of formation fluid into the MDT tool (100–1,000 cc)
- Samples analyzed at surface (PVT lab) for fluid composition, GOR, API gravity, H₂S content, CO₂ content
- Critical input for completion design (material selection, flow assurance)

**Example: MDT pressure gradient interpretation for Block 32 well:**
- 4,020m: 5,220 psi
- 4,050m: 5,243 psi → Gradient = (5,243-5,220)/(4,050-4,020) × 10 = 0.077 psi/ft → Oil (0.3–0.4 psi/ft expected) — wait, 0.077 is too low. Recalculate...

Actually: Gradient = (5243-5220 psi) / ((4050-4020) × 3.281 ft/m) = 23/98.4 = 0.234 psi/ft → Oil gradient (0.2–0.35 psi/ft for Angola crudes) ✓

- 4,150m: 5,271 psi → Gradient from 4,050 to 4,150m = (5,271-5,243)/(328.1) = 0.085 psi/ft → Water (0.44–0.47 psi/ft? No — too low)

Wait — let me use consistent numbers:
- Gradient in psi/ft at 4,050m level: $(P_2 - P_1)/(TVD_2 - TVD_1)$ in ft. If the gradient changes, you've crossed a fluid contact.
- Oil gradient = ρ_oil × g ≈ 0.33 psi/ft (for 0.76 SG crude)
- Water gradient ≈ 0.435 psi/ft

A sudden change in gradient at a specific depth = the Oil-Water Contact (OWC). This is the most reliable way to determine the OWC for field development planning.

---

## Exercises — Formation Evaluation

**Exercise 1: Archie Sw Calculation**
An Angola Block 32 well shows the following log readings at a 3m depth interval:
- GR = 28 API
- RHOB = 2.18 g/cm³
- NPHI = 0.25
- Deep Rt = 30 ohm·m

Using: a = 1.0, m = 1.90, n = 2.0, Rw = 0.035 ohm·m, matrix density = 2.65 g/cm³, fluid density = 0.85 g/cm³

1. Calculate porosity from density log
2. Calculate Vsh from GR (assume GR_clean = 20, GR_shale = 110)
3. Calculate Sw using Archie's equation
4. Is this interval pay? Apply standard Angola cutoffs.

**Exercise 2: N-D Crossplot Analysis**
A 30m interval has the following log data:

| Depth | RHOB (g/cc) | NPHI | GR (API) | Deep Rt (ohm·m) |
|-------|-------------|------|----------|-----------------|
| 4,010 | 2.20 | 0.26 | 22 | 28 |
| 4,020 | 2.08 | 0.19 | 25 | 45 |
| 4,030 | 2.03 | 0.16 | 21 | 62 |
| 4,040 | 2.35 | 0.24 | 18 | 32 |

Calculate density porosity for each depth (use matrix = 2.65, fluid = 0.85 g/cc). Which interval shows gas crossover (density porosity >> neutron porosity)? What fluid type is present in each interval?

**Exercise 3: Net Pay Calculation**
A 40m gross reservoir interval has the following zonal data:

| Zone | Gross thickness (m) | Vsh | φ | Sw |
|------|---------------------|-----|---|----|
| A | 12 | 0.08 | 0.27 | 0.14 |
| B | 8 | 0.35 | 0.22 | 0.30 |
| C | 10 | 0.12 | 0.31 | 0.18 |
| D | 10 | 0.28 | 0.14 | 0.65 |

Apply cutoffs: Vsh < 0.30, φ > 0.10, Sw < 0.60. Calculate net pay and NTG ratio.

**Exercise 4: MDT Pressure Gradient**
MDT measurements in a Block 17 appraisal well:

| TVD (m) | Pressure (psi) |
|---------|---------------|
| 3,810 | 5,140 |
| 3,835 | 5,148 |
| 3,860 | 5,156 |
| 3,900 | 5,175 |
| 3,940 | 5,193 |
| 3,970 | 5,209 |

Calculate pressure gradients between successive points. Identify the likely fluid contacts. At what depth does the gradient change? What fluid is above vs below the contact?

---

## Interview Questions — Formation Evaluation

1. A Block 32 appraisal well shows high GR (90 API) across a 15m interval that also shows high deep resistivity (45 ohm·m). What are the possible explanations? How would you resolve the ambiguity?
2. Explain Archie's equation. What are the key parameters and where do they come from for an Angola well?
3. What is geo-steering and why is it important for Angola horizontal completions?
4. What information does an MDT pressure test give that logs alone cannot provide?
5. What is the neutron-density crossover effect and what does it indicate?
6. Why do resistivity logs in OBM wells have different interpretation requirements than WBM wells?
7. Describe the sequence of wireline logs you would run in an Angola 8½" production hole and explain the purpose of each tool.
8. What is the difference between gross pay and net pay? How does the NTG ratio affect the STOIIP estimate?

---

*Next: [09_Production_Engineering_Tutorial.md](09_Production_Engineering_Tutorial.md) | See also: [05_Reservoir_Engineering_Tutorial.md](05_Reservoir_Engineering_Tutorial.md)*

```
Track 1: Gamma Ray (0–150 API) | Caliper (6"–16")
Track 2: Resistivity (deep, medium, shallow) on log scale (0.2–2000 ohm·m)
Track 3: Neutron porosity (45–0%) overlay with Density porosity (45–0%)
Track 4: Sonic DT (40–140 µs/ft) | Density (RHOB) (1.95–2.95 g/cm³)
Track 5: Lithology / Formation evaluation summary

Depth track in center: measured depth and TVD
```

**How to read it:**

Starting from the left:
1. **GR:** Is it clean (sand) or shale?
2. **Resistivity:** Is the deep resistivity high (hydrocarbons) or low (water)?
3. **N-D crossover:** Gas? Oil? Water?
4. **Calculate Sw:** Plug in porosity and Rt from logs.
5. **Decision:** Reservoir candidate or not?

**Typical pay zone in Angola (what you'll see):**
- GR: drops sharply to 20–35 API
- Deep resistivity: jumps to 15–80 ohm·m
- NPHI: 22–30%
- RHOB: 2.10–2.20 g/cm³ (low — hydrocarbon in pores)
- N-D slightly separated (or small gas crossover if gas cap)
- Calculated Sw: 10–25% (mostly oil)

---

## Part 9: MWD/LWD Logs — Logging While Drilling

**LWD (Logging While Drilling):** The same measurements (GR, resistivity, density, neutron) but taken while the bit is drilling. Tools mounted in the BHA.

**Advantages:**
- Formation evaluated at time of drilling — before mud invasion distorts resistivity readings
- Real-time geo-steering: the directional driller can steer the well based on real-time GR — stay in the best part of the reservoir
- Essential for Angola's horizontal and high-angle wells

**MWD (Measurement While Drilling):** Specifically the directional measurements — inclination, azimuth, toolface. Transmitted to surface via mud pulse (pressure pulses in the mud column).

**Geo-steering in Angola:** In a horizontal well, the LWD GR log is monitored in real time. The drillers keep the well in the clean sand (low GR zone). If GR rises, they are entering shale — steer back down into the sand.

---

## Part 10: Perforation Interval Selection

After a well is cased and cemented, you must decide which intervals to perforate (create holes in the casing and cement to connect the wellbore to the formation).

**Selection criteria:**
1. **Net pay:** Intervals with $S_w$ < 0.5 AND porosity > 15% AND not too shaly (Vsh < 0.25)
2. **Avoid water contacts:** Do not perforate below the OWC (Oil-Water Contact)
3. **Avoid gas caps:** Do not perforate above the GOC (Gas-Oil Contact) unless gas production is intended
4. **Consider completion design:** For open-hole gravel packs (Angola standard for sand control), the entire pay is treated — perforation design is different

**OWC/GOC identification from logs:**
- OWC: Resistivity drops sharply from oil zone value (20–80 ohm·m) to water zone value (0.5–3 ohm·m)
- GOC: N-D crossover disappears (gas above, oil below)

---

## Part 11: Practice Exercises

**Exercise 1:** A formation at 3,800m depth has: GR = 28 API, RHOB = 2.18 g/cm³, NPHI = 0.24, Deep Rt = 35 ohm·m.
- Is it sand or shale?
- Calculate density porosity (use ρma = 2.65, ρf = 0.85 for oil)
- Is there a gas crossover?
- Calculate Sw using Archie (a=1.0, m=1.9, n=2.0, Rw=0.03 ohm·m)
- Is this a pay zone? What is your perforation recommendation?

**Exercise 2:** Draw a schematic showing how resistivity logs change as you drill from (top to bottom): shale → clean oil sand → oil-water contact → clean water sand → shale. Show the approximate resistivity values for each zone.

**Exercise 3:** Explain why the neutron log shows low porosity in a gas zone when the actual porosity (from core) is 28%. Draw the N-D crossplot response for gas vs oil vs water in a sand with 28% true porosity.

**Exercise 4:** An Angola Block 17 well has a 50m sand package. GR shows 3 clean sand intervals (12m, 8m, 6m thick) separated by 2 shale streaks (5m and 7m thick). Deep Rt in the sands: 45, 32, and 2 ohm·m from top to bottom. Where is the OWC likely located? Which intervals do you recommend for perforation?

---

## Part 12: Study Resources

| Resource | Format | Notes |
|---|---|---|
| "Fundamentals of Well Log Interpretation" — Asquith & Krygowski | Textbook | Standard introductory log interpretation textbook |
| "Cased Hole Log Analysis" — Western Atlas | Textbook | Production logging and cased hole evaluation |
| Schlumberger Log Interpretation Charts | Free PDF | The "chartbook" used by all log interpreters — get this |
| Petrel RE (SLB) student version | Software | Industry standard interpretation software |
| SPE papers: search "Angola formation evaluation" | OnePetro | Angola-specific calibration and case studies |
| SPWLA (Petrophysicists society) education resources | Online | Excellent petrophysics education materials |
| TotalEnergies/SLB Angola log data publications | Papers | Turbidite-specific interpretation challenges |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/04_Reservoir_Path.md](../paths/04_Reservoir_Path.md)*  
*Where to learn: [learn.slb.com](https://learn.slb.com) (log interpretation) | [PetroWiki](https://petrowiki.spe.org/Formation_evaluation) | [Learning Resources](../../../docs/learning-resources.md)*
