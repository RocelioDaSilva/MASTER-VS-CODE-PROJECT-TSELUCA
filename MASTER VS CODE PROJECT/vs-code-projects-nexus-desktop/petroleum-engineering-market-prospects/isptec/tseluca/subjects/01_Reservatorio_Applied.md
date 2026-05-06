# Engenharia de Reservatórios — Applied to Real Angola Work
## From ISPTEC Equations to Industry Practice

---

## Overview

Engenharia de Reservatórios I and II are the most directly applicable subjects in your entire ISPTEC curriculum. Every single major concept taught in these two courses — plus Simulação e Modelagem and Gerenciamento e Monitoração de Reservatórios — is used by reservoir engineers in Angola every working day.

This guide takes each major topic from your ISPTEC curriculum and shows you exactly how it is used, which software implements it, and what a real Angola reservoir engineer does with it.

---

## ER I: Porosity, Permeability, and Saturation in Real Work

### What ISPTEC Taught You
Definitions of effective porosity, absolute permeability (Darcy's Law), relative permeability, capillary pressure, and water saturation.

### How Industry Uses It
These are not abstract properties — they are the inputs to every reserve estimate and production forecast ever made.

**A petrophysicist's workflow for an Angola well:**
1. Import well log data (LAS file) into Petrel or Interactive Petrophysics
2. Calculate porosity from density log:
   $$\phi = \frac{\rho_{ma} - \rho_b}{\rho_{ma} - \rho_f} = \frac{2.65 - \rho_b}{2.65 - 1.0}$$
   (where ρ_ma = 2.65 g/cc for quartz sandstone, ρ_f = 1.0 g/cc for fresh water)
3. Calculate Sw from Archie:
   $$S_w = \left(\frac{aR_w}{\phi^m R_t}\right)^{1/n}$$
   Angola turbidite parameters: a=1.0, m=1.85–1.95, n=2.0, Rw=0.02–0.05 ohm.m
4. Define net pay: select intervals where φ > 12% AND Sw < 50%
5. Sum net pay across all intervals → Net pay per well → Input to STOIIP calculation

**The petrophysicist's uncertainty:** The Archie parameters (m, n) are calibrated against core measurements. If no core data exists for a new well, default values carry uncertainty that directly affects Sw — and therefore reserves. This uncertainty propagates into the FDP economics.

---

## ER I: Darcy's Law and Well Productivity

### What ISPTEC Taught You
Darcy's Law in radial flow, the Productivity Index (PI), and the concept of skin.

$$Q = \frac{kh(P_r - P_{wf})}{141.2 \mu B \left[\ln\left(\frac{r_e}{r_w}\right) - 0.75 + S\right]}$$

### How Industry Uses It
**Every well performance analysis starts here.** The production engineer uses Darcy's Law (embedded in the IPR equation) to:

1. **Predict well deliverability before drilling:** "Given our reservoir model predicts k = 300 mD, h = 25m, what flow rate do we expect at a flowing pressure of 3,000 psi?"

2. **Diagnose well underperformance:** "Well A15 is producing 30% less than Darcy's Law predicts for its reservoir pressure. This implies a positive skin. What is the skin?"
   $$S = \left[\frac{141.2 Q \mu B}{kh(P_r - P_{wf})} - \ln\left(\frac{r_e}{r_w}\right) + 0.75\right]$$
   Skin > 0 → damage (scale, mud invasion, perforation damage) → stimulation candidate
   Skin < 0 → stimulation already present (acid job, fracture) → exceeding natural deliverability

3. **Justify a stimulation job:** "If we perform an acid wash to remove near-wellbore scale and reduce skin from +10 to 0, how much incremental production do we gain? Is the $2M acid job cost justified?"

**Software:** Prosper (Petroleum Experts) has a direct Darcy's Law inflow calculator. You define k, h, μ, B, re, rw, skin → get the IPR curve. This is the first thing you build in Prosper for any Angola well analysis.

---

## ER I: STOIIP and Recoverable Reserves — The Industry Workflow

### What ISPTEC Taught You
The volumetric equation:
$$N = \frac{7758 \times A \times h \times \phi \times (1 - S_{wi})}{B_{oi}}$$

### How Industry Uses It
**This calculation is done in Petrel, not by hand.** The static model in Petrel sums across millions of grid cells:

$$N = \sum_{i=1}^{N_{cells}} V_i \times NTG_i \times \phi_i \times (1 - S_{wi}) \times \frac{1}{B_{oi}} \times 6.29$$

But the equation itself is still the foundation. You need to know it to verify your Petrel results make sense.

**Reserves classification (SPE-PRMS):**
- **1P Proved (P90):** Only reservoir volume you are 90% confident exists
- **2P Proved + Probable (P50):** Best estimate volume
- **3P Proved + Probable + Possible (P10):** Optimistic volume

For an Angola deepwater field before first production:
- P10/P90 ratio for STOIIP: often 3:1 to 5:1 (huge uncertainty before history matching)
- P10/P90 ratio for recoverable reserves: similar or larger (additional recovery factor uncertainty)

**Angola reserves audit:** Every year, TotalEnergies, Azule, Eni, and Sonangol must report their reserves to ANPG and (for listed companies) to the SEC or other regulators. An independent reservoir engineer (from firms like Gaffney Cline, DeGolyer & MacNaughton, Ryder Scott) audits the reserves. They use exactly the ER I volumetric method combined with ER II material balance and production history.

---

## ER I: Drive Mechanisms and Material Balance

### What ISPTEC Taught You
The Havlena-Odeh formulation of the material balance equation (MBE):
$$F = N(E_o + mE_g + E_f) + W_e B_w$$

Where:
- F = underground withdrawal (production converted to reservoir conditions)
- Eo = expansion of oil and solution gas
- Eg = expansion of gas cap gas
- Ef = expansion due to compaction and connate water
- We = water influx from aquifer

### How Industry Uses It
**The MBE is one of the first tools a reservoir engineer applies when a new Angola field starts producing.** It requires no geological model — only production data and pressure measurements.

**Angola-specific workflow:**
1. Collect monthly production data (oil, water, gas) from FPSO
2. Collect quarterly reservoir pressure measurements (downhole gauges or pressure buildup tests)
3. Plot F vs Eo: if the points lie on a straight line through the origin → solution gas drive only, slope = N (OOIP)
4. If points curve upward → aquifer support exists. Re-plot with aquifer term: line up with correct Aquifer model
5. OOIP from MBE vs OOIP from volumetric method: compare → validates or questions the geological model

**Why this matters in Angola:** Angola turbidite reservoirs often have strong aquifer support. The MBE tells the reservoir engineer:
- How strong is the aquifer? (Aquifer productivity index)
- How quickly is the pressure maintaining? (Is natural water influx enough or do we need water injection?)
- When will water breakthrough occur? (The front is advancing — when does it reach the producers?)

**Software:** Material balance is done in MBAL (Petroleum Experts), which has graphical Havlena-Odeh plots, aquifer models, and production matching built in.

---

## ER II: Pressure Transient Analysis — Reading the Reservoir

### What ISPTEC Taught You
The radial diffusivity equation and its solutions (line source solution, superposition), Horner plot construction and interpretation, calculation of kh and skin from buildup tests.

$$\frac{\partial^2 P}{\partial r^2} + \frac{1}{r}\frac{\partial P}{\partial r} = \frac{\phi \mu c_t}{k}\frac{\partial P}{\partial t}$$

### How Industry Uses It
**Pressure transient analysis (PTA) is performed on every new production well in Angola before sustained production begins.** This is called a "drill stem test" (DST) if done during drilling, or a "well test" if done after completion.

**A well test workflow in Angola:**
1. Produce the well at a stabilised rate for 12–72 hours (the "drawdown" period)
2. Shut the well in at the tree and record the pressure buildup for 12–72 hours
3. Download the pressure data from the downhole gauges (high-resolution, 0.001 psi precision)
4. Import into PTA software: Kappa Saphir or SLB Ecrin
5. Build the Horner plot: $P_{ws}$ vs $\log\left[\frac{t_p + \Delta t}{\Delta t}\right]$
6. Fit the middle time region (MTR): slope = $m = \frac{162.6 q \mu B}{kh}$ → solve for kh
7. Calculate skin: $S = 1.151\left[\frac{P_{1hr} - P_{wf(t_p)}}{m} - \log\left(\frac{k}{\phi \mu c_t r_w^2}\right) + 3.23\right]$
8. Identify late-time behaviour: boundary effects (closed reservoir, sealing fault, constant pressure boundary = aquifer)

**What PTA gives you that no simulation model can:**
- The actual reservoir permeability in the drainage area around the well (simulation uses assumed permeability from the static model)
- The skin factor (damage or stimulation condition at this specific well)
- Evidence of faults or boundaries near the well
- Reservoir connectivity (do pressure responses communicate between wells?)

**Software in Angola operations:** Kappa Saphir is the most widely used PTA software. SLB Ecrin is also common. Both require an understanding of ER II concepts to interpret correctly.

---

## Simulação e Modelagem: Eclipse in Practice

### What ISPTEC Taught You
Reservoir simulation concepts: discretisation of the diffusivity equation, finite difference approximation, IMPES vs fully implicit schemes, black oil model, relative permeability, capillary pressure in simulation, history matching concepts.

### How Industry Uses It
**An Eclipse or CMG model of an Angola block is the single most important technical document the subsurface team maintains.**

**The Eclipse DATA file structure:**
```
-- Eclipse DATA file structure (keywords)
RUNSPEC      -- Dimensions, phases, grid type
GRID         -- Grid geometry, permeability, porosity (from static model)
PROPS        -- PVT tables, relative permeability, capillary pressure
REGIONS      -- Saturation and PVT region assignments
SOLUTION     -- Initial conditions (pressure, saturations, fluid contacts)
SCHEDULE     -- Well data, production history, completion schedule, time steps
```

**A junior reservoir engineer's first Eclipse task:** Update the production history in the SCHEDULE section with the last 3 months of FPSO production data, re-run the simulation, compare simulated vs actual production. This is called the "history match update" and is done quarterly.

**History matching in practice:**
The history match is never perfect. When the simulation under-predicts water cut in Well A15:
- Is the well's perforations too close to the OWC? → Review completion data
- Is the relative permeability curve too "water-wet"? → Adjust kro/krw curves
- Is there a higher-permeability streak connecting the injector to this producer? → Review geological model
- Is the injector's BHP too high, causing the front to move faster than expected? → Check injection data

This detective work is what makes reservoir engineering intellectually demanding and valuable.

**Production forecasting:** Once history-matched, the model is run forward 20 years under several scenarios:
- Base case: current well count, no new wells
- Development case: 4 new infill wells + water injection increase
- EOR case: WAG injection commencing in Year 10

Each scenario generates a production profile (oil, water, gas by month) that feeds the economics model.

---

## Gerenciamento e Monitoração: Field Management in Practice

### What ISPTEC Taught You
Reservoir management principles: production optimisation, pressure maintenance, surveillance program design, well performance monitoring, secondary recovery.

### How Industry Uses It

**The reservoir management plan (RMP)** is a living document that governs how an Angola block is operated. It contains:
- Production strategy (target rates, wells to produce, injection strategy)
- Pressure maintenance plan (when and how much to inject)
- Surveillance plan (what measurements to take, at what frequency)
- Performance indicators (what KPIs will trigger a review or intervention?)
- Update schedule (annual full-field review)

**Annual field review:** Every Angola operator conducts an annual subsurface review of each block. The reservoir engineering team presents:
- Production performance vs FDP forecast (are we ahead or behind?)
- Reserve update (has the P50 EUR changed?)
- Surveillance data interpretation (what have the 4D seismic and PTA results told us?)
- Recommendations for the next year (new infill wells, injection adjustments, stimulation candidates)

This review is presented to ANPG as part of the operator's annual reporting obligation.

---

## The Software Stack for Reservoir Engineers

| Software | What ISPTEC Subject It Connects To | How to Access |
|---------|-----------------------------------|---------------|
| Eclipse (SLB) / CMG | Simulação e Modelagem | CMG Student Version (free — register on CMG website) |
| Petrel (SLB) | Geoestatística + Avaliação Formações | Petrel Student Version (free via Schlumberger Academic) |
| MBAL (Petroleum Experts) | ER I (MBE) | 30-day free trial; university license available |
| Prosper (Petroleum Experts) | ER I (IPR), Elevação | 30-day free trial |
| Kappa Saphir | ER II (PTA) | Kappa Academic Program (free for students) |
| OFM (SLB) | Gerenciamento Reservatórios | SLB academic access |
| Python | Computação Científica I & II | Free; see discipline/05_Digital_PE.md |

**Priority order for a future reservoir engineer:** Get the CMG student version first (direct connection to your Simulação subject). Then Kappa Saphir (connects directly to ER II PTA). Then MBAL and Prosper together.

---

## Exercises That Bridge ISPTEC and Industry

### Exercise 1: Build a Full STOIIP and Reserves Estimate
Angola discovery data:
- Reservoir area: 12 km² (from seismic interpretation)
- Gross thickness: 45m
- Net-to-gross: 0.65
- Porosity: 0.24
- Initial water saturation: 0.30
- Bo: 1.35 rb/stb
- Recovery factor estimates: P90 = 25%, P50 = 35%, P10 = 48%

Calculate: STOIIP, P90/P50/P10 recoverable reserves.

### Exercise 2: Diagnose a Skin from Well Test Data
Well test data for an Angola deepwater well:
- Production rate: 8,000 stb/day
- Reservoir pressure: 7,250 psi
- Flowing BHP at shut-in: 6,400 psi
- Horner plot slope: m = 210 psi/cycle
- P(1hr) = 6,850 psi
- k = 180 mD (from m), h = 22m, φ = 0.23, μ = 0.8 cp, ct = 12×10⁻⁶ psi⁻¹, rw = 0.35ft, B = 1.38

Calculate skin. Is this well damaged or stimulated? What would you recommend?

### Exercise 3: Material Balance for Drive Mechanism
An Angola producer has produced the following:
| Year | Np (MMstb) | Gp (Bscf) | Wp (MMbbl) | Pres (psi) |
|------|-----------|-----------|-----------|------------|
| 0 | 0 | 0 | 0 | 8,200 |
| 1 | 8.5 | 6.8 | 0.2 | 7,800 |
| 2 | 18.2 | 14.6 | 1.1 | 7,350 |
| 3 | 28.7 | 23.0 | 4.8 | 6,900 |

Initial Rsi = 800 scf/stb, Boi = 1.42, μo = 0.85 cp, Bo at each pressure available from PVT table.

Plot F vs Eo and determine: what is the drive mechanism? Is aquifer support present? Estimate OOIP.

### Exercise 4: Eclipse Model Update
Given a simplified 5-spot Eclipse model (1 injector, 4 producers, 100×100×3 grid), update the SCHEDULE section to:
- Add 6 months of additional production history
- Add a new infill producer well W5 with 15 perforations
- Run a 10-year forecast

(This exercise requires CMG student version or access to Eclipse — start with the tutorial models that come with each software package.)

---

*Continue to [02_Pocos_Fluidos_Applied.md](02_Pocos_Fluidos_Applied.md) for the Engenharia de Poços and Fluidos de Perfuração applied guide.*  
*Where to learn: [Learning Resources](../../../docs/learning-resources.md)*
