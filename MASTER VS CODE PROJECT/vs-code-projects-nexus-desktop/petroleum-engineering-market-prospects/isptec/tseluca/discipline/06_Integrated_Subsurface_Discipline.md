# The Integrated Subsurface Discipline
## How Reservoir Engineers, Geologists, and Petrophysicists Work as One Team

---

## What "Integrated Subsurface" Means

In the oil and gas industry, the subsurface team is responsible for understanding what is underground — the geometry of the reservoir, the quality of the rock, the properties of the fluid, and how much can be recovered.

No single discipline can do this alone:
- **Geologists** see the structure and depositional history, but cannot calculate flow rates
- **Petrophysicists** read the logs and define rock quality, but cannot predict depletion
- **Reservoir engineers** build dynamic models and forecast production, but need the rock and fluid description from geology and petrophysics

The **integrated subsurface workflow** is the process of combining all three disciplines to go from seismic data and well logs to a reservoir model that can be used to plan wells and develop fields.

Angola's deepwater turbidite reservoirs are among the most complex in the world. Understanding how the integrated subsurface works is essential for any engineer aspiring to work for TotalEnergies, Azule, Eni, or Sonangol in the subsurface.

---

## The Integrated Subsurface Workflow

### Step 1: Seismic Interpretation (Geophysics Lead)

**Input:** 3D seismic volume (raw data from marine seismic survey)
**Output:** Structural model (top reservoir surface, fault interpretation, salt geometry)

The geophysicist interprets the seismic data to map:
- The top and base of reservoir horizons
- Faults and their displacement
- Salt bodies (critical for Block 32 sub-salt targets)
- Fluid contacts (DHI — Direct Hydrocarbon Indicators: flat spots, amplitude anomalies)

**Angola-specific context:**
Angola's deepwater blocks contain salt diapirs (large salt bodies) that complicate seismic imaging. Sub-salt imaging requires advanced techniques: Full Waveform Inversion (FWI), reverse time migration (RTM). These are cutting-edge geophysics methods that TotalEnergies and Eni apply to Block 32 and Block 15/06 data.

---

### Step 2: Petrophysical Interpretation (Petrophysicist Lead)

**Input:** Well log data (GR, resistivity, density, neutron, sonic) from exploration and appraisal wells
**Output:** Petrophysical model (porosity, permeability, water saturation, net-to-gross) for each well

The petrophysicist uses the ISPTEC subject "Avaliação de Formações" (Formation Evaluation) to:
1. Identify reservoir intervals (low GR = clean sand = potential reservoir)
2. Calculate porosity (from density log: $\phi = \frac{\rho_{ma} - \rho_b}{\rho_{ma} - \rho_f}$)
3. Calculate water saturation (Archie's equation: $S_w = \sqrt{\frac{aR_w}{\phi^m R_t}}$)
4. Calculate net pay (intervals where φ > 12% and Sw < 50% — typical Angola cutoffs)
5. Estimate permeability from correlations (core calibrated)

**The petrophysicist's critical decision:** What are the correct cutoffs for net pay? Being too generous gives you a larger reservoir model — which looks good in early meetings but produces less than expected. Being too conservative undervalues the discovery. Calibrating cutoffs against core data and production performance is the key skill.

**Angola turbidite petrophysics:**
Angola's turbidite reservoirs are typically:
- Porosity: 20–30% (excellent, well-sorted deep marine sands)
- Permeability: 100–2,000 mD in main sand bodies; 0.1–10 mD in thin laminated sands
- Net-to-gross ratio: 30–80% (highly variable — this uncertainty is a major FDP risk)
- Water saturation: 15–40% in main sands

The contrast between good quality clean sands and intervening mudstone/shale baffles is one of the defining features of Angola turbidite reservoirs. This heterogeneity drives reservoir behaviour — and is something the static model must capture.

---

### Step 3: Static Geological Modelling (Geologist + Petrophysicist Lead)

**Input:** Seismic interpretation + petrophysical interpretation + depositional model
**Output:** 3D grid populated with reservoir properties (porosity, permeability, net-to-gross, fluid contacts)

**What a static model is:**
A 3D numerical grid — imagine the reservoir divided into millions of small blocks (grid cells). Each cell has values for:
- Porosity
- Permeability (in x, y, and z directions — typically different in each)
- Net-to-gross (fraction of the cell that is reservoir-quality rock)
- Water saturation (initial conditions)
- Oil, water, or gas type

**Software:** Petrel (SLB) is the dominant static modelling software for Angola deepwater. IRAP RMS (Halliburton) is also used.

**Key modelling challenges for Angola turbidites:**

1. **Facies modelling:** Turbidite systems have complex geometry — channels, lobes, amalgamated sands, thin-bedded sequences. The geologist must build a depositional model (where are the channels? how wide? how connected?) and encode this into the static model using geostatistical methods.

   - Sequential Gaussian Simulation (SGS): used for continuous properties like porosity
   - Sequential Indicator Simulation (SIS): used for discrete properties like facies
   - Object-based modelling: used for channel bodies where geometry is known from analogue data

2. **Connectivity:** Are the sand bodies in different parts of the field connected? This is the most important uncertainty in many Angola fields. If disconnected, pressure support from water injectors won't reach all producers.

3. **Thin beds:** Angola turbidites often have thin-bedded intervals that are below seismic resolution (1m beds in a 25Hz seismic survey are invisible). These thin beds contribute to reserves but are missed in the static model unless corrected for using Thomas-Stieber method.

**STOIIP Calculation from the static model:**

$$N = \frac{7758 \times A \times h \times \phi_{net} \times (1 - S_{wi})}{B_{oi}}$$

But the static model does this automatically by summing across all cells:

$$N = \sum_{cells} \frac{V_{cell} \times NTG \times \phi \times (1 - S_w)}{B_{oi}} \times 6.29 \text{ (m}^3\text{ to bbl)}$$

Where $V_{cell}$ is the cell volume (m³).

---

### Step 4: Fluid Characterisation (Reservoir Engineer + Petrophysicist)

**Input:** Fluid samples from exploration or appraisal wells (PVT samples)
**Output:** PVT equation of state (EOS) model characterising oil and gas properties at all P and T conditions

**What PVT stands for:** Pressure, Volume, Temperature. PVT tests measure how the oil-gas system behaves as pressure and temperature change from reservoir conditions to surface conditions.

**Key PVT parameters for Angola crudes:**
- **Bubble point pressure (Pb):** The pressure below which gas starts to come out of solution. If reservoir pressure drops below Pb, a free gas phase forms in the reservoir — dramatically affecting flow behaviour.
- **Oil formation volume factor (Bo):** The ratio of oil volume at reservoir conditions to oil volume at surface conditions. Angola deepwater crudes: Bo typically 1.2–1.6 (20–60% volume shrinkage from reservoir to surface).
- **Gas-oil ratio (Rs):** Dissolved gas per barrel of oil at reservoir conditions. Angola crudes: Rs typically 400–1,200 scf/bbl.
- **Oil viscosity (μo):** Angola deepwater crudes: typically 0.3–1.5 cp at reservoir conditions (light, mobile oil — good for production).

**EOS model:** The PVT data is tuned to an equation of state (Peng-Robinson or Soave-Redlich-Kwong) using PVTsim or Multiflash software. The EOS model is then used in the dynamic reservoir simulator to calculate fluid behaviour during depletion.

---

### Step 5: Dynamic Reservoir Modelling (Reservoir Engineer Lead)

**Input:** Static model + PVT model + production history
**Output:** Dynamic simulation model that can forecast production under different development scenarios

**The dynamic model extends the static model by adding:**
- Relative permeability curves (how oil, water, and gas compete for pore space)
- Aquifer model (influx of water from connected aquifer into the reservoir)
- Well models (perforations, skin, completion type)
- Pressure-dependent properties (how porosity and permeability change with depletion)
- Production history for history matching

**Software:** Eclipse (SLB) — the dominant Angola deepwater simulator. CMG (Computer Modelling Group) used by some operators. Both use reservoir simulator input files with structured keyword-based format.

**History matching:** Before you can trust the model to forecast the future, it must reproduce the past. History matching is the process of adjusting model parameters (permeability, NTG, aquifer strength, relative permeability) until the simulated production matches the observed production history.

This is simultaneously the most time-consuming and most important step in reservoir engineering. A poorly history-matched model gives unreliable forecasts. A well history-matched model is a powerful decision-making tool.

---

### Step 6: Production Forecasting (Reservoir Engineer)

**Input:** History-matched dynamic model
**Output:** Production profiles for each development scenario (P10, P50, P90)

The reservoir engineer runs the model forward in time with:
- A defined well count and schedule (from the drilling team)
- Defined operating conditions (reservoir management strategy)
- Three cases: optimistic (P10), base (P50), conservative (P90) — reflecting uncertainty in reservoir parameters

**Key reservoir management decisions the forecast informs:**
- When should water injection start?
- Should we drill horizontal wells or vertical/deviated wells? (higher recovery for horizontal but higher cost)
- What is the optimal production rate to maximise recovery without coning water?
- When will water cut reach the facility limit?
- Should we install a third FPSO separator or will existing capacity last?

---

## The Subsurface Team Structure in an Angola Operator

Understanding who does what helps you know where you fit.

```
SUBSURFACE MANAGER
│
├── GEOPHYSICS TEAM
│   ├── Seismic Interpreter (Lead)
│   ├── Geophysical Analyst
│   └── Specialist: Rock physics / FWI / 4D seismic
│
├── GEOLOGY TEAM
│   ├── Development Geologist (Lead)
│   ├── Static Modeller (Petrel specialist)
│   └── Specialist: Sedimentology / Stratigraphy
│
├── PETROPHYSICS TEAM
│   ├── Petrophysicist (Lead)
│   └── Petrophysical Analyst
│
└── RESERVOIR ENGINEERING TEAM
    ├── Lead Reservoir Engineer (dynamic modelling lead)
    ├── Senior Reservoir Engineer (reserves, material balance)
    ├── Reservoir Engineer (production forecasting, history match)
    └── Junior Reservoir Engineer (data management, model updates)
```

**Where ISPTEC graduates enter:**
- Junior Reservoir Engineer (with ER I & II + Simulação + Avaliação de Formações)
- Petrophysical Analyst (with Avaliação de Formações + Geologia + strong log reading)
- Static Modelling Analyst (with Geologia + Geoestatística + Petrel training)

---

## 4D Seismic: Seeing the Reservoir Change Over Time

4D seismic (time-lapse seismic) is one of the most powerful tools in Angola deepwater reservoir management — and it is something you will encounter early in your career at TotalEnergies or Eni Angola.

**Concept:** A seismic survey is acquired over the same area at two (or more) different times (e.g., before production started and 5 years later). The difference between the surveys reveals how the reservoir has changed:
- Water flooding front: swept areas show different acoustic response than oil-saturated areas
- Pressure depletion: areas of pressure depletion show a seismic response change (stress changes rock velocity)
- Bypass oil: areas that should have been swept but show oil-saturated response may contain bypassed oil — drilling opportunity

**Angola 4D examples:**
- TotalEnergies has acquired multiple 4D surveys over Block 17 (Girassol, Dalia, Pazflor fields)
- The 4D data has directly guided infill well placement — identifying bypassed oil pockets that could not be seen in the original 3D seismic
- Estimated recovery improvement from 4D-guided infill drilling: hundreds of millions of barrels across Block 17

**Why you should care:** Understanding 4D seismic makes you a better reservoir engineer. Being able to interpret a 4D response and connect it to a reservoir simulation gives you a skill that senior engineers value highly.

---

## The Uncertainty Problem: P10, P50, P90

The most important concept the subsurface team communicates to management is **uncertainty**.

Everything underground is uncertain:
- The reservoir area (only constrained by well penetrations and seismic resolution)
- The net-to-gross ratio (varies between wells)
- The recovery factor (depends on drive mechanism, heterogeneity, injection performance)
- The connectivity (can only be tested by drilling more wells)

**How uncertainty is handled:**

1. **Multiple realisations:** The static model is built 50–100 times with different random seeds (different geologically-plausible reservoir geometries). The spread of STOIIP values across these realisations represents the geological uncertainty.

2. **Multiple scenario cases:** Beyond geological uncertainty, there are scenario uncertainties (What if the aquifer is stronger than expected? What if we drill 2 more wells?). These are represented as discrete scenarios.

3. **P10/P50/P90 classification:**
   - P90 (conservative): There is a 90% probability of at least this much recovery
   - P50 (base case): There is a 50% probability of at least this much recovery
   - P10 (optimistic): There is only a 10% probability of at least this much recovery

The FDP economic model is run for all three cases. Management needs to know: even in the P90 (pessimistic) case, is the project economic?

---

## Your ISPTEC Subjects and the Integrated Subsurface

| ISPTEC Subject | Integrated Subsurface Role |
|---------------|---------------------------|
| Avaliação de Formações | Core input to petrophysical interpretation; porosity, Sw, net pay calculation |
| Geologia Geral | Foundation for understanding depositional environments and facies |
| Geoestatística | Essential for stochastic modelling (SGS, SIS) in Petrel |
| Engenharia Reservatórios I | Fluid flow fundamentals; IPR, skin, drive mechanisms |
| Engenharia Reservatórios II | Advanced: pressure transient, simulation, MBE under complex drive |
| Simulação e Modelagem | Eclipse/CMG workflow directly from this subject |
| Gerenciamento Monitoração Res. | Production monitoring, 4D integration, field management strategy |
| Geoquímica Orgânica | Source rock analysis, generation potential, migration — exploration phase |
| Introdução Análise de Bacias | Basin architecture context for exploration leads |
| Modelagem Bacias Sedimentares | How the basin formed — context for reservoir distribution |
| Métodos Sísmicos (Optativa I) | Direct connection to geophysical interpretation step |

**The standout combination:** Graduates who have strong Avaliação de Formações + Geoestatística + Simulação AND know Petrel are extremely rare and extremely sought after. If you can do all three, you can work on the most challenging Angola deepwater subsurface teams from early in your career.

---

## Interview Questions for Subsurface Roles

### Petrophysics
1. Walk me through how you calculate porosity from a density log.
2. What is the Archie equation and what are its limitations in shaly sands?
3. What is net pay and what cutoffs would you apply to an Angola turbidite?
4. What is a neutron-density crossplot and what does it tell you?

### Static Modelling / Geology
1. What is Sequential Gaussian Simulation and when would you use it vs object-based modelling?
2. What is net-to-gross and why is it one of the largest uncertainties in an Angola reservoir model?
3. What is a Thomas-Stieber correction and when is it applied?
4. How does a 3D seismic survey help define the reservoir model?

### Dynamic Modelling / Reservoir Engineering
1. What is history matching and why is it necessary before forecasting?
2. What is relative permeability and how does it affect displacement efficiency?
3. What is a material balance equation and what can it tell you without a simulation model?
4. Explain P10/P50/P90 reserves classification. How is it used in an FDP?

### Integrated
1. Walk me through the full workflow from seismic to production forecast.
2. What is 4D seismic and how has it been used in Angola?
3. If the simulation history match for a Block 17 well shows we are under-predicting water cut — what are the three most likely causes?
4. What is the difference between STOIIP and recoverable reserves? What determines the recovery factor?

---

*You have completed the Discipline section. Return to [00_PE_Discipline_Map.md](00_PE_Discipline_Map.md) for the complete map, or proceed to the [subjects/](../subjects/) section to connect your ISPTEC curriculum directly to these disciplines.*  
*Full learning directory: [Learning Resources](../../../docs/learning-resources.md)*
