# Termodinâmica Aplicada + Engenharia de Gás Natural — Applied
## Phase Behaviour, Hydrates, and Angola's Gas Challenge

---

## Overview

Termodinâmica Aplicada and Engenharia de Gás Natural are among the most underestimated subjects in the ISPTEC curriculum. Students often see them as theoretical. In Angola, they are directly applied in two critical contexts:

1. **Flow assurance:** Hydrate prediction and management (Termodinâmica)
2. **Gas monetisation:** Angola's $10 billion ALNG (Angola LNG) plant, gas re-injection, and associated gas management (Engenharia de Gás Natural)

Angola has one of the largest reserves of associated gas in Africa. The question of what to do with this gas — flare it (illegal), re-inject it (common), use it for gas lift (existing practice), liquefy it (ALNG), or pipe it to a power plant — is one of the most consequential strategic decisions in Angola's energy sector. It is a question that petroleum engineers help answer.

---

## Part 1: Termodinâmica Aplicada — Phase Behaviour in Petroleum Engineering

### The Pressure-Temperature (PT) Phase Diagram

**What ISPTEC taught:** Phase equilibrium, vapour-liquid equilibrium (VLE), equations of state (van der Waals, Peng-Robinson, SRK).

**Why this matters for every petroleum engineer:**

The oil and gas produced from an Angola reservoir changes phase continuously as it flows from the reservoir (high P, high T) through the wellbore, flowline, and FPSO process (dropping P and T). The phase behaviour determines:
- How much gas comes out of solution (GOR)
- How dense the fluid is at each point (affects pressure drop calculations)
- Whether hydrates will form (P-T inside the hydrate stability zone)
- Whether asphaltenes or wax will precipitate
- How the FPSO separators perform

**The Peng-Robinson Equation of State (PR EOS):**

$$P = \frac{RT}{V - b} - \frac{a(T)}{V(V+b) + b(V-b)}$$

Where:
$$a(T) = 0.45724 \frac{R^2 T_c^2}{P_c} \left[1 + m\left(1 - \sqrt{T/T_c}\right)\right]^2$$
$$b = 0.07780 \frac{RT_c}{P_c}$$
$$m = 0.37464 + 1.54226\omega - 0.26992\omega^2$$

And Tc, Pc are the critical temperature and pressure of each component, ω is the acentric factor.

**How this is applied in Angola:**

The flow assurance engineer does not solve the PR EOS by hand. Instead, software like PVTsim (Calsep) or Multiflash (KBC) uses the PR EOS to model the fluid behaviour. The engineer provides:
- Fluid composition (mole fractions of each component from the PVT sample)
- Reservoir pressure and temperature

The software provides:
- Bubble point pressure at reservoir temperature
- Gas-oil ratio at separator conditions
- Oil and gas densities at any P and T
- Phase envelope (dew point curve, bubble point curve, cricondentherm)
- Hydrate formation curve (temperature vs pressure for hydrate stability)

**Your job as a reservoir or production engineer:** Understand what these outputs mean and how to use them. Understand why a lighter oil (lower molecular weight hydrocarbons) has a higher GOR and lower viscosity. Understand why CO₂ in the produced gas shifts the bubble point and creates a different phase envelope.

---

### Hydrate Thermodynamics: Where Your Termodinâmica Subject Is Critical

**The van der Waals-Platteeuw (vdW-P) statistical thermodynamics model** underlies hydrate prediction. You do not need to implement it — PVTsim and Multiflash implement it. But understanding the physics is what makes you credible in a flow assurance discussion.

**Physical explanation:**
Hydrates form when:
1. Light gas molecules (CH₄, C₂H₆, CO₃, H₂S) are present
2. Free water is present
3. Pressure is high enough AND temperature is low enough that the free energy of the hydrate structure is lower than that of free gas + liquid water

The equilibrium condition (thermodynamic stability) is:
$$\Delta \mu_{water}^{hydrate} = \Delta \mu_{water}^{ice/liquid}$$

This equality defines the hydrate stability boundary — the PT curve separating hydrate-stable conditions (above/left of the curve) from hydrate-unstable conditions (below/right).

**For a typical Angola deepwater gas composition (C₁ dominated, ~20 mol% C₂, 5 mol% CO₂):**
- Hydrate formation temperature at 200 bar: approximately 23–26°C
- Angola seabed temperature: 3–5°C
- Steady-state flowline temperature at 25 km from wellhead: 15–20°C

**Conclusion:** The flowline is inside the hydrate stability zone at steady-state operating conditions. Hydrates will form unless inhibited. This is the fundamental flow assurance challenge in Angola.

**The thermodynamic effect of methanol (MeOH):**
Methanol disrupts the water activity (raises the chemical potential of water in the liquid phase), shifting the hydrate curve to lower temperatures. The Hammerschmidt equation gives a first approximation:

$$\Delta T_{hydrate} = \frac{2335 W}{M(100 - W)}$$

Where ΔT = depression of hydrate formation temperature (°C), W = weight percent of methanol in water phase, M = molecular weight of methanol (32 g/mol).

**Example:** To achieve a 10°C suppression:
$$10 = \frac{2335 W}{32(100 - W)}$$
$$320(100 - W) = 2335W$$
$$32000 = 2335W + 320W = 2655W$$
$$W = 12.1\text{ wt\%}$$

Need ~12 wt% methanol in the water phase to achieve 10°C hydrate suppression. For a Angola well producing 2,000 bbl/day of water, this means:
$$V_{MeOH} = 2000 \times 0.121 \times 0.35 \approx 85 \text{ bbl/day of methanol}$$

This is a significant operational cost and logistical challenge — methanol must be stored on the FPSO, injected via umbilical, and recovered or disposed.

---

### PVT Testing: Your Termodinâmica Subject in a Lab

When an Angola exploration well is drilled, reservoir fluid samples are taken (surface recombination samples or downhole PVT samples using MDT/RFT tools). These samples are sent to a PVT laboratory for analysis.

**Standard PVT tests (directly connected to your Termodinâmica Aplicada subject):**

| Test | What It Measures | Termodinâmica Concept |
|------|-----------------|----------------------|
| Constant Composition Expansion (CCE) | Bubble point pressure, compressibility | Phase equilibrium, compressibility |
| Differential Liberation (DL) | Bo, Bg, Rs, gas gravity vs pressure | VLE, component partitioning |
| Separator tests | Optimum separator conditions | Flash separation, VLE |
| Viscosity measurement | Oil and gas viscosity vs P, T | Transport properties |
| Compositional analysis | Mole fractions of C₁ through C₇+ | Component thermodynamics |
| SARA analysis | Saturates/Aromatics/Resins/Asphaltenes | Asphaltene stability |
| WAT measurement | Wax Appearance Temperature | Phase transition thermodynamics |

**The PVT report** is a fundamental input to the reservoir simulation (your Simulação subject uses PVT data) and to the flow assurance model (OLGA uses PVT data for two-phase pipeline simulation).

---

## Part 2: Engenharia de Gás Natural Applied to Angola

### Angola's Associated Gas Situation

**The numbers:**
- Angola produces approximately 600,000–700,000 boe/day of oil
- For every barrel of oil, 600–1,500 scf of associated gas is produced (GOR)
- Total associated gas: ~600 MMscf/day in 2024
- Angola's domestic gas demand: ~100 MMscf/day (power generation, industry)
- ALNG plant capacity: ~1,100 MMscf/day feed gas (equivalent to ~10 MTPA LNG)

**The gas disposition challenge:**
Angola's deepwater oil production generates a large volume of associated gas that cannot be safely flared (ANPG has a zero routine flaring target by 2030, per Angola's NDC commitments). This gas must be:
- **Re-injected** into the reservoir (most common) — this also maintains reservoir pressure
- **Used as fuel** on the FPSO (partial use)
- **Supplied to ALNG** (Angola LNG plant at Soyo — receives gas from Blocks 0, 17, 18, 31, 32)
- **Supplied to domestic power plants** (limited pipeline infrastructure currently)
- **Used for gas lift** (immediate re-use in production)

---

### Gas Re-injection: Your Engenharia de Gás Natural Subject Applied

**Why re-inject gas?**
1. Maintain reservoir pressure (gas injection provides pressure support, similar to water injection)
2. Compliance with zero-flaring regulations
3. Gas banking (storing gas until monetisation is possible)
4. Enhanced recovery (miscible gas injection at pressures above MMP — Minimum Miscibility Pressure)

**Gas compression (FPSO gas compression system):**

Your Engenharia de Gás Natural subject covers gas compression. Here is the application:

Gas arrives at the HP separator at 60–80 bar. Re-injection into the reservoir requires 250–400 bar injection pressure (above reservoir pore pressure). This pressure boosting is done in multiple compression stages (typically 3–4 stages with intercooling).

**Polytropic compression work:**
$$W = \frac{n}{n-1} \frac{P_1 V_1}{\eta_p} \left[\left(\frac{P_2}{P_1}\right)^{(n-1)/n} - 1\right]$$

Where:
- n = polytropic exponent (1.25–1.35 for Angola gas composition)
- P₁ = suction pressure
- P₂ = discharge pressure
- V₁ = suction volume flow rate
- η_p = polytropic efficiency (0.75–0.82 for modern centrifugal compressors)

**Interstage cooling:** After each compression stage, the gas is cooled back to ~40°C before entering the next stage. This:
- Reduces the work required in the next stage (lower suction temperature)
- Condenses out liquid hydrocarbons and water that would damage the next stage compressor

**Compressor types on Angola FPSOs:**
- Centrifugal compressors: high flow rates (>50 MMscf/day), lower pressure ratios per stage (1.5:1–4:1)
- Reciprocating compressors: lower flow rates, higher pressure ratios — used for final injection stage or test separators

---

### Angola LNG (ALNG): What It Is and How It Connects to Your Degree

**Background:**
Angola LNG (ALNG) is a joint venture between Sonangol, Chevron, BP, Eni, and TotalEnergies. The plant at Soyo (northern Angola) receives associated gas from offshore blocks via subsea pipelines, processes it, and exports it as LNG to world markets.

**Capacity:** ~10 MTPA LNG (equivalent to ~1,100 MMscf/day of feed gas)
**Train:** Single LNG train (vs Qatar's multiple-train mega-projects)
**Startup:** 2013 (first LNG cargo); intermittent operation due to technical and commercial issues; operating more consistently from 2016 onward

**The gas processing sequence (from your Engenharia de Gás Natural subject):**

```
OFFSHORE GAS (from Blocks 0, 17, 18, 31, 32)
         │
         ▼
SUBSEA PIPELINES TO SOYO
         │
         ▼
SLUG CATCHER (removes condensate and water from pipeline slugs)
         │
         ▼
ACID GAS REMOVAL (AGR)
│  Remove CO₂ and H₂S using amine absorption
│  Solvent: MDEA (methyldiethanolamine) or DEA
│  Regeneration column: strips CO₂/H₂S from solvent using heat
│  Angola gas: relatively low CO₂ (1–5 mol% typically) but must remove to < 50 ppm for LNG
         │
         ▼
DEHYDRATION (Gas glycol dehydration)
│  Remove water vapour from the gas
│  Solvent: TEG (triethylene glycol)
│  TEG absorbs water → regenerated by heating to ~200°C → dry gas
│  Must achieve: water dew point < -50°C for LNG production
         │
         ▼
HEAVY HYDROCARBON REMOVAL (Turboexpander or refrigerated NGL extraction)
│  Remove C₃+ hydrocarbons (propane, butanes, pentanes)
│  These would freeze out in the LNG main cryogenic heat exchanger
│  NGL product (C₃+): sold separately as LPG or NGLs
         │
         ▼
LNG MAIN CRYOGENIC HEAT EXCHANGER
│  Cool gas from ~-40°C to -162°C at near-atmospheric pressure
│  Gas liquefies: LNG density ≈ 450 kg/m³ (600× denser than gas at standard conditions)
│  Refrigerant system: APCI C3/MR process (propane pre-cool + mixed refrigerant)
         │
         ▼
LNG STORAGE TANKS (double-wall vacuum-insulated tanks, 165,000 m³ each)
         │
         ▼
LNG LOADING (into LNG carriers at the jetty)
         │
         ▼
EXPORT TO: Europe, North America, Asia
```

**The thermodynamics content in this process:**
- Acid gas removal: chemical absorption equilibrium (related to your Físico-Química subject)
- Dehydration: VLE of water-TEG system (Termodinâmica Aplicada)
- NGL extraction: phase separation with turboexpander (isentropic expansion — Termodinâmica)
- Liquefaction: refrigeration cycle (Termodinâmica refrigeration cycles)
- LNG vapour pressure and boil-off: Clausius-Clapeyron equation (Termodinâmica)

---

### Gas Lift: Using Associated Gas Within the FPSO System

Your Engenharia de Gás Natural subject covers gas flow equations. Here is the FPSO gas lift application:

The FPSO compresses recovered gas from the separators and re-routes it for gas lift injection down the wells. This is a closed-loop system:
1. Wells produce oil + gas
2. Gas separates at HP separator (~70 bar)
3. Gas compressor boosts pressure to 180–220 bar
4. Gas injected back down through umbilicals to wellheads
5. Gas lift valves introduce gas into tubing
6. Gas lifts fluid to surface → cycle repeats

**Gas lift gas specification:**
The gas used for gas lift must be:
- Free of liquids (would slug the gas lift valves)
- Free of solids (would erode or plug valves)
- Dehydrated to the specified water dew point (to prevent hydrate formation in the umbilical at low seabed temperature)
- Within the injection pressure rating of the gas lift valves

---

### Domestic Gas for Angola Power

A strategic opportunity your Engenharia de Gás Natural subject connects to:

Angola has chronic electricity shortfalls. Luanda and other major cities experience regular power outages. The government's solution includes gas-fired power plants — but this requires:
1. A gas supply from offshore fields
2. A gas processing facility onshore (remove liquids, dehydrate, possibly remove CO₂)
3. A pipeline network to power plants

**The Sonagas** (Angola state gas company) and **Sonangol** are developing this domestic gas infrastructure. Engineers who combine offshore production knowledge with gas processing/transport knowledge are highly valuable for this growing sector.

---

## Exercises Connecting Termodinâmica and Gás Natural to Angola Work

### Exercise 1: Hydrate Formation Temperature
An Angola flowline contains gas with the following composition: 88% CH₄, 7% C₂H₆, 3% C₃H₈, 1.5% CO₂, 0.5% N₂. The operating pressure at the midpoint of the flowline is 180 bar.

1. Using the Sloan hydrate prediction chart (look up in Sloan's "Clathrate Hydrates of Natural Gases"), estimate the hydrate formation temperature at 180 bar.
2. If the seabed temperature is 5°C, is this flowline inside or outside the hydrate stability zone?
3. How much methanol (wt% in water phase) is required to suppress hydrate formation by 8°C?

### Exercise 2: Bubble Point and GOR
A Block 17 crude has the following PVT data at reservoir temperature of 95°C:
- Bubble point pressure: 4,200 psi
- Reservoir pressure: 7,500 psi (well above bubble point)
- Rs at bubble point: 780 scf/stb
- Bo at bubble point: 1.42 rb/stb

Current reservoir pressure has declined to 5,800 psi (still above bubble point):
1. Is the reservoir currently producing with free gas in the reservoir? Why?
2. What happens to oil mobility as pressure approaches and drops below the bubble point?
3. Why is maintaining reservoir pressure above the bubble point a reservoir management priority?

### Exercise 3: ALNG Compression Requirement
Natural gas from an offshore block arrives at the Soyo ALNG plant at 80 bar and 30°C. The LNG liquefaction process requires the gas to be supplied at 60 bar (slightly reduced after acid gas removal) and then liquefied. However, the ALNG plant needs to deliver 700 MMscf/day.

The gas transport pipeline from offshore has a 150 psi pressure drop over 200km. The offshore block's separator pressure is 65 bar. Is additional compression needed onshore? Calculate whether a booster compressor is required and estimate the required power.

(Assume γ = 1.3, Z = 0.88, R = 8.314 J/mol·K, MW = 18 g/mol for the gas mixture)

### Exercise 4: Gas Re-injection Compression Stages
A Block 32 FPSO produces 250 MMscf/day of associated gas that must be re-injected at 320 bar. The gas enters the compression system at 8 bar after the LP separator. Design a 3-stage compression system:
1. Calculate the equal-ratio compression stage ratio: $(P_{out}/P_{in})^{1/3}$
2. Calculate the discharge pressure of each stage
3. Estimate the total compression power (polytropic, η = 0.78, γ = 1.28, T_in = 40°C per stage)
4. What is the importance of interstage cooling, and at what temperature should the gas be cooled between stages?

---

## Career Paths Connected to This Subject Cluster

| Career | Primary Connection | Angola Employer |
|--------|--------------------|-----------------|
| Flow Assurance Engineer | Termodinâmica + Escoamento + Sistemas Marítimos | TechnipFMC, Subsea 7, operators |
| Gas Processing Engineer | Engenharia de Gás Natural + Termodinâmica | ALNG, Sonangol, Total |
| Reservoir Engineer (gas fields) | Termodinâmica (PVT) + ER I & II | Eni Angola (Block 15/06 gas), Sonangol |
| LNG Engineer | Engenharia de Gás Natural + Termodinâmica | ALNG Joint Venture (Sonangol/Chevron/BP/Total/Eni) |
| Process Engineer (FPSO) | Termodinâmica + Sistemas de Produção | SBM Offshore, Yinson, FPSO operators |
| Domestic Gas Engineer | Engenharia de Gás Natural | Sonagas, Sonangol, power sector |

**The Angola LNG path is particularly interesting for ISPTEC graduates:** ALNG needs engineers who understand both offshore gas production (to coordinate with the offshore operators delivering gas) AND gas processing (to manage the Soyo plant). This dual knowledge set is rare and highly valued. As an Angolan national with the ISPTEC curriculum, you are exceptionally positioned for this role.

---

*You have completed the Subjects section. Return to [00_Subject_Industry_Map.md](00_Subject_Industry_Map.md) for the complete curriculum map, or explore the [discipline/](../discipline/) section for the full petroleum engineering discipline deep-dives.*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
