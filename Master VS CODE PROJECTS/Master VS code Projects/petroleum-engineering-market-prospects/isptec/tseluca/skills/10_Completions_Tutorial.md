# Skill Tutorial 10 — Completions Engineering

> **Applies to:** Completions engineers (CORE), drilling engineers (HIGH), production engineers (HIGH)
> **ISPTEC connection:** Engenharia de Poços, Fluidos de Perfuração e Completação, Sistemas de Produção Superfície
> **Goal:** Understand the complete completion design process — from sand control selection through tubing and packer design, DHSV, perforating, wireline operations, and coiled tubing — in the Angola deepwater turbidite context.

---

## Part 1: What Completions Engineers Do

After the reservoir section is drilled and evaluated (by the drilling and reservoir teams), the completions team takes over to:
1. Design and install the production completion (tubing, packer, safety valve, sand control)
2. Execute perforating operations to connect the wellbore to the reservoir
3. Conduct the initial well test and clean-up flow
4. Throughout the well's life: perform intervention operations (wireline, coiled tubing, workover) to maintain or restore productivity

The completion is what turns a drilled hole into a producing well. It is the last step before the well is handed to production operations.

---

## Part 2: The Completion Design Workflow

```
1. WELL DATA REVIEW
   Reservoir engineer: formation pressure, temperature, fluid properties, PI estimate
   Drilling engineer: wellbore geometry, casing program, cement evaluation log
   Geologist: formation characterization — sand quality, clay content

2. SAND CONTROL SELECTION ← Most critical decision for Angola turbidites
   Unconsolidated sand? → Yes (almost all Angola deepwater) → Sand control required
   
3. COMPLETION TYPE SELECTION
   Open-hole gravel pack (OHGP)? Or cased-hole gravel pack? Or fracpack?
   
4. TUBING STRING DESIGN
   Size, material, thread, packer placement

5. DOWNHOLE SAFETY VALVE (DHSV) DESIGN
   Type, setting depth, control line design

6. PERFORATING DESIGN (for cased-hole completions)
   Charge type, shot density, phasing, interval selection

7. COMPLETION FLUID SELECTION
   Clear brine density, filtration specification

8. WELL TEST AND CLEAN-UP PLAN
   Flow periods, pressures, sampling

9. HANDOVER TO PRODUCTION
```

---

## Part 3: Sand Control — The Most Important Angola Topic

Angola's turbidite sands are **unconsolidated** — the sand grains are not cemented together. Under the pressure drawdown of production, grains can mobilize and flow into the wellbore along with the oil.

**Consequences of sand production:**
- **Erosion** of surface equipment (chokes, valves, separators)
- **Sand accumulation** in the wellbore and subsea equipment (plugging)
- **Casing collapse** from formation compaction (subsidence)
- Handling and disposal of produced sand on the FPSO

**Sand control methods:**

### 3.1 Standalone Screen (SAS)

A simple wire-wrapped or sintered metal screen installed in the open-hole (no casing across the reservoir). The screen's slot size is designed to be smaller than the formation sand grain size.

**When to use:** Well-consolidated sand with high uniformity — rare in Angola deepwater.

**Angola suitability:** LOW. Fine-grained turbidites tend to plug standalone screens rapidly.

### 3.2 Open-Hole Gravel Pack (OHGP)

The dominant completion method in Angola's deepwater turbidite reservoirs.

**How it works:**
1. Drill the reservoir section (8½" or 6" hole, open hole — no casing)
2. Run a specialized screen assembly (premium screen with a base pipe)
3. Pump a slurry of sized gravel (carefully sized sand) through the tubing-screen annulus and across the formation face
4. The gravel pack fills the annulus between the screen and the borehole wall
5. Gravel is sized to be retained by the screen and to hold back formation sand grains

**OHGP advantages:**
- Maximum inflow area (open hole exposes full formation face)
- High productivity (low skin)
- Excellent sand control for unconsolidated Angola sands
- No perforation required (no casing damage)

**Gravel size selection:**
The gravel must be sized relative to the formation sand:
$$d_{50,gravel} = 5 \times d_{50,formation}$$

Where $d_{50}$ is the median grain diameter from a sieve analysis of the formation sample. Typical Angola turbidite: $d_{50}$ = 150–350 microns → Gravel: 750–1,750 microns (20/40 or 16/30 US mesh).

### 3.3 Cased-Hole Gravel Pack (CHGP)

Casing is run across the reservoir, cemented, and perforated. Gravel is then pumped through the perforations (frac-pack mode or classic CHGP).

**When used in Angola:** When OHGP is not possible (hole stability problems, multi-zone completions requiring zone isolation).

### 3.4 FracPack

A combination of hydraulic fracturing and gravel packing. The gravel slurry is pumped at high rate to fracture the formation — the fracture bypasses near-wellbore damage and greatly increases productivity. The fracture is then packed with gravel.

**When used:** Wells with high skin or formations where near-wellbore damage limits productivity. Very common in Gulf of Mexico. Less common in Angola due to high natural permeability.

---

## Part 4: Production Tubing Design

### Tubing Size Selection

Tubing ID must be large enough to allow maximum production without excessive friction losses, but not so large that artificial lift (gas lift) is inefficient or that wellbore interventions are difficult.

**Common Angola deepwater tubing sizes:**

| Tubing OD | ID | Typical Application |
|---|---|---|
| **5½"** | 4.67"–4.87" | High-rate FPSO wells (>5,000 bbl/day target) |
| **5"** | 4.28"–4.50" | Medium-rate wells, most Angola completions |
| **4½"** | 3.74"–3.96" | Lower rate wells, limited tubing space in casing |

### Tubing Material and Grade

- **L80, N80:** Standard carbon steel for normal service
- **13Cr (13% Chromium stainless):** For CO₂ service — common in Angola where CO₂ content is moderate (0.5–5%). Resists CO₂ corrosion.
- **S13Cr, Super 13Cr:** Enhanced corrosion resistance for higher CO₂ or mild H2S
- **DSS (Duplex Stainless Steel), CRA (Corrosion Resistant Alloy):** For highly corrosive environments (H2S)

### Premium Connections

Deep, high-pressure, high-temperature Angola wells require premium threaded connections (not API round threads):
- **VAM TOP, VAM ACE** (Vallourec)
- **Tenaris Blue, Tenaris Dopeless**
- **TSH Blue, Semilas** (various manufacturers)

Premium connections have gas-tight metal-to-metal seals, are rated for higher load combinations, and meet the API 5CT/ISO 11960 specs.

---

## Part 5: Packer Design

A packer is a seal element run on the tubing string to isolate the annulus between the tubing and the casing.

**Primary functions:**
1. Prevent wellbore fluid from bypassing the tubing (annular flow = production losses)
2. Isolate the production zone from the casing annulus (pressure integrity, corrosion protection)
3. Enable annulus gas lift (packer seals above the gas lift valve — gas goes DOWN the annulus and enters the tubing through the GLV)

### Packer Types

**Permanent packer (set by hydraulic pressure or rotation):**
- Cannot be unset without milling (requires workover)
- Highest pressure/temperature ratings
- Used in Angola deepwater completions as the primary production packer

**Retrievable packer (set and retrieved by mechanical or hydraulic actuation):**
- Can be unset and retrieved with the tubing
- Used for testing, temporary completions, or when re-completion is anticipated

**Single vs dual completion:**
- **Single string:** One tubing and one packer. Produces one zone.
- **Dual completion:** Two tubing strings and two packers to independently produce two zones.

---

## Part 6: Downhole Safety Valve (DHSV / SCSSV)

The DHSV (Downhole Safety Valve) is a critical well barrier. It is a valve installed in the tubing string approximately 50–100m below the seabed (mudline).

**Failsafe principle:** The DHSV is held OPEN by hydraulic pressure from a control line that runs from the FPSO down through the umbilical and wellhead to the valve. If hydraulic pressure is lost (control line rupture, hydraulic system failure, deliberate closure), a spring inside the valve causes it to close automatically.

**Why it matters:** If an FPSO fire, riser rupture, or emergency occurs, the DHSV can be closed to isolate the wellbore independent of the subsea tree. It is the last barrier before the reservoir.

**Control line:** ¼" stainless steel or HDPE control line strapped to the outside of the tubing string, running from the DHSV up through the wellhead and into the FPSO hydraulic control panel. Failure of this line = DHSV closes (failsafe).

---

## Part 7: Perforating Design (For Cased-Hole Completions)

In a cased-hole completion, you must create holes (perforations) through the casing, cement, and into the reservoir formation. This is done by gun-fired shaped charges.

### Perforating Parameters

**Shot Density:** Number of perforations per foot (spf). Typical: 4–8 spf for oil wells. Higher density = more flow area = lower skin.

**Phase Angle:** Angular spacing between shots around the tubing circumference. Common: 0°, 90°, 60°, 45°. 60° phasing gives good coverage and structural casing integrity.

**Charge Size:** Larger charges = longer penetration into the formation. Critical in tight formations but less important in high-permeability Angola sands.

**Perforation tunnel length:** The length of the perforation hole into the formation. For Angola gravel-packed wells: penetration depth less critical because the gravel pack is the inflow conduit, not the perforation itself.

### Overbalanced vs Underbalanced Perforating

**Overbalanced:** Wellbore pressure > formation pressure when perforating. Formation fluid is not drawn into the wellbore. Perforations are packed with crushed rock and debris.
- Requires acidizing or flow clean-up to clear the perforation tunnels

**Underbalanced:** Wellbore pressure < formation pressure when perforating. Formation fluid immediately flows into the perforations, carrying debris away.
- Cleaner perforations, less skin
- Requires well control measures (the well flows immediately on perforation)
- Preferred method for Angola sands when practical

---

## Part 8: Completion Fluids (Recap from Drilling Fluids Tutorial)

During completion operations:
- **Drilling OBM is displaced** from the wellbore with a seawater spacer and then a clean completion brine
- **Completion brine selection** (from [06_Drilling_Fluids_Tutorial.md](06_Drilling_Fluids_Tutorial.md)):
  - Must be filtered to < 2 micron (NTU < 5) to avoid formation damage
  - Must be formulated to balance formation pressure (density = kill weight)
  - Must not precipitate minerals with formation water

**Common brines used in Angola:**

| Brine | Density | Application |
|-------|---------|-------------|
| Seawater | 8.4 ppg | Shallow, low-pressure wells only |
| Potassium Chloride (KCl) | 8.4–9.7 ppg | Protection against clay swelling in completion interval |
| Sodium Chloride (NaCl) | 8.4–10.0 ppg | Standard clear brine, economical |
| Calcium Chloride (CaCl₂) | 8.4–11.6 ppg | Denser applications, widely used in Angola completions |
| Calcium Bromide (CaBr₂) | 10.0–15.1 ppg | Very high density wells, expensive |
| Zinc Bromide (ZnBr₂) | up to 19.2 ppg | Extreme HP wells; environmental concerns |

---

## Part 9: Wireline Operations

After the completion is installed and the well is producing, wireline is the primary tool for downhole intervention without a workover rig.

### Types of Wireline

**Slickline (single-wire mechanical wireline):**
- A solid single strand of steel wire (1/16" to 3/16" OD)
- Conveys tools downhole by gravity and wire manipulation
- No electrical signals — purely mechanical
- Used for: gauge retrieval/setting, running and pulling gas lift valves, setting bridge plugs, shifting sliding sleeves, measuring depth (XN key)

**Braided line / Electric line (wireline with conductors):**
- Multi-strand or armored wire with electrical conductors inside
- Can power and communicate with downhole tools
- Used for: logging (pulsed neutron logging, casing corrosion logs), downhole cameras, perforating guns (electrically fired)

**Coiled Tubing (CT):**
- Continuous flexible steel or composite tubing (1" to 2⅜" OD) coiled on a large drum
- Can pump fluids down the CT string while running (cleanouts, acid treatments)
- Much greater reach than slickline (can pump against flow, can push where wireline cannot reach)
- Expensive: CT unit = $30,000–$80,000/day

### Slickline Tool String

A typical slickline run:
```
Wire head (top)
  │
Stem (weight bars — provides weight so tools go down, even in flowing wells)
  │
Gauge setter / pulling tool / standing valve (depending on task)
  │
Bottom tool (e.g., GR survey collar locator, mechanical pulling tool)
```

**Common slickline tasks in Angola deepwater:**
- **Gas lift valve changeout:** Pull the old valve from the mandrel, run the new valve with the new opening pressure setting. No rig needed. Cost: 1–2 days of LWI vessel + slickline.
- **Downhole pressure gauge retrieval:** Pull the permanent gauge for calibration/replacement.
- **DHSV function check:** Close and test the DHSV by slickline actuation and pressure testing.
- **Bridge plug setting:** Isolate lower perforations for selective zone testing.

---

## Part 10: Coiled Tubing Operations

### CT Applications on Angola Wells

**Matrix acid stimulation:**
CT is run to the target depth. Acid (typically 15% HCl for carbonate damage, or Mud Acid HCl+HF for sandstone damage) is pumped down the CT string and out through the bottom hole assembly. The acid dissolves damage near the wellbore.

**Scale removal:**
Calcium carbonate scale in the tubing or perforations can be dissolved with HCl. Scale inhibitor is then squeezed through the perforations for future protection.

**Sand cleanout:**
Produced sand accumulates at the bottom of the wellbore over time. CT with a jetting assembly washes the sand out of the well and carries it to surface. This is common on Angola Block 0 (Cabinda) wells where sand production is a known problem.

**Perforating with TCP via CT:**
Tubing-Conveyed Perforating on CT allows perforating in a live well (underbalanced) through a very long interval in one run.

**CT nitrogen lift:**
In a well with very low reservoir pressure (dead well), CT is used to inject nitrogen gas into the tubing to "kick off" the well — reduce the hydrostatic column enough that formation fluid starts flowing.

### CT Limits

- **Maximum CT reach:** Friction increases with CT length and horizontal angle. In Angola deepwater horizontal wells (2+ km horizontal), CT cannot always reach total depth. Alternative: production logging, wireline tractor.
- **CT fatigue:** Each time CT bends through the gooseneck (surface) and is straightened by the injector head, it accumulates fatigue. CT strings have a maximum bending cycle count before they must be replaced.

---

## Part 11: Well Integrity Monitoring for the Completions Engineer

After completing a well and handing to production, the completions team remains responsible for well barrier integrity through the well's life.

**Key monitoring points (see also discipline/02_Well_Integrity_Management.md):**

**DHSV function testing:**
ANPG requires the DHSV to be function tested annually (minimum). Test procedure:
1. Remove well from production (route other wells to the FPSO)
2. Close the DHSV (hydraulic pressure removed from control line)
3. Bleed down tubing above DHSV to zero pressure
4. Apply test pressure below DHSV (from wellbore pressure below valve)
5. Hold for 15 minutes: zero pressure bleed-up in tubing = DHSV holding = PASS
6. Open DHSV, restore production

**Annulus pressure monitoring:**
The A-annulus (between tubing and production casing) should be near zero psi. Any sustained annulus pressure (SAP) > 200 psi indicates:
- Tubing leak (production fluids leaking into annulus)
- Packer leak
- Crossflow between formations

**Production casing integrity:**
Casing corrosion log (caliper or EM caliper tool) run every 3–5 years in Angola. Reports to ANPG include casing integrity status for every well.

---

## Part 12: The Completions Engineer in Angola's Career Landscape

### What Sets Completions Engineers Apart

Completions engineers have a unique position in the Angola job market because they bridge:
- **Drilling** (wellbore construction, casing, cementing)
- **Reservoir** (understanding what the completion must achieve for the field)
- **Production** (the completion design determines long-term productivity and AL requirements)
- **Subsea** (interface with the subsea tree and control system)

Angola's deepwater sand control completions (OHGP, multi-zone completions) are among the most complex in the world. Engineers with this specific experience are highly sought by Baker Hughes, SLB, Halliburton, TechnipFMC, and the operators (TotalEnergies, Azule, Eni).

### Entry Roles for ISPTEC Graduates in Completions

**Baker Hughes Completions Field Engineer Trainee:**
- 12-month onshore training program
- Then field deployment on Angola wells
- Typical first role: OHGP screen installation, well clean-up operations, coiled tubing

**SLB Completions Specialist:**
- Focus on one technology (e.g., sand control screens, gas lift valves)
- Become the deepwater Angola expert for that technology
- Career progression to global specialist

**TechnipFMC Subsea Completions:**
- Interface between subsea trees and completions
- Wellhead design and installation coordination
- Running tool operations

---

## Exercises — Completions Engineering

**Exercise 1: Saucier Gravel Sizing**
A formation sand sample from a Block 32 well shows:
- d₅₀ (median grain diameter) = 0.18 mm
- d₁₀ (fine end) = 0.09 mm

1. Calculate the required gravel d₅₀ using the Saucier criterion
2. Identify the appropriate US mesh size gravel pack
3. Calculate the target screen slot width (approximately equal to gravel d₁₀)

**Exercise 2: Tubing Size Selection**
A Block 17 horizontal well is expected to produce 8,500 STB/day of oil with 20% water cut. Flow rate at reservoir conditions (using total liquid) = 11,000 bbl/day of liquid. Tubing OD options: 5" (ID = 4.408"), 5½" (ID = 4.670"), 7" (ID = 6.184").

Minimum annular velocity for gas lift = 1.5 m/s upward velocity.
Cross-sectional area of 5" ID = π/4 × (0.1120m)² = 0.00985 m²
Flow rate = 11,000 bbl/day = 0.0202 m³/s

1. Calculate flow velocity in each tubing size
2. Which tubing sizes achieve minimum lift velocity?
3. What other factors would influence your final selection?

**Exercise 3: DHSV Test**
A DHSV test yields the following:
- DHSV closed at 09:00. Tubing pressure above DHSV = 0 psi (bled to zero at 09:10)
- Monitor tubing pressure for 15 minutes: pressure = 0 psi at 09:25 → **PASS or FAIL?**
- In a second well: Tubing pressure bled to 0 psi at 09:10. At 09:25: pressure = 45 psi → **PASS or FAIL?**
- For the second well: what does the result indicate and what is your next action?

**Exercise 4: Completion Material Selection**
A Block 32 deepwater completion well has the following fluid characteristics from PVT analysis:
- CO₂: 4.2 mol%
- H₂S: 15 ppm
- Chlorides: 82,000 mg/L
- Temperature: 145°C
- Pressure: 8,200 psi

Using the ISO 15156 / NACE MR0175 chart and general corrosion engineering principles:
1. Is standard L-80 carbon steel adequate? Why or why not?
2. Is 13Cr adequate (maximum H₂S for 13Cr = 10 psi partial pressure H₂S)?
3. What grade would you recommend?
(Calculate H₂S partial pressure: P_H2S = 15 ppm × 1e-6 × 8,200 psi)

---

## Interview Questions — Completions Engineering

1. Why is Open-Hole Gravel Pack (OHGP) the dominant completion method in Angola's deepwater turbidite reservoirs? What are its limitations?
2. What is the Saucier criterion and how does it guide gravel size selection?
3. Explain the two-barrier philosophy for well integrity. What are the primary and secondary barriers in a completed Angola deepwater well?
4. What is a DHSV and what happens if the control line is cut?
5. A gas lift valve needs to be changed in an Angola subsea well. The well is in production in 1,800m water depth. Describe the operation, the equipment needed, and the estimated cost/time.
6. What is the difference between overbalanced and underbalanced perforating? When would you choose each?
7. A completions engineer recommends 13Cr tubing for a Block 32 well. A drilling engineer (cost-focused) asks why you cannot use cheaper L-80. How do you justify 13Cr?
8. What is the purpose of premium threaded connections (VAM TOP, TenarisHydril) versus standard API round threads? When are they required?

---

*You have completed all 10 Skill Tutorials. Return to [00_INDEX.md](../00_INDEX.md) for the master navigation guide, or explore [paths/](../paths/) for career-specific tracks.*

**Typical Angola deepwater completion brine:** CaCl₂ (1.40 SG) or CaBr₂ (1.60–1.82 SG) depending on reservoir pressure.

---

## Part 9: Well Intervention — Wireline and Coiled Tubing

After a well is completed and on production, interventions are needed over its life to:
- Retrieve and replace downhole safety valves
- Replace gas lift valves (as well performance changes)
- Remove scale or paraffin deposits
- Test downhole pressure and temperature
- Perforate new zones

### Slickline (Mechanical Wireline)

A single strand of solid steel wire. Used to run simple tools:
- **Gauge cutter:** Runs down to confirm wellbore is clear to full ID
- **Flow coupling / landing nipple plug:** Install and retrieve plugs to isolate the tubing
- **Gas lift valve pull/reinstall:** The most common slickline job in Angola
- **Jars and knocking tools:** Mechanical force tools to unseat stuck tools
- **Downhole pressure/temperature gauges:** Permanently installed; data retrieved by slickline

**Can carry mechanical tools only** — no electrical power.

### Electric Line (E-Line / Wireline Logging)

Multi-conductor cable. Carries electrical power to downhole tools:
- **Production logging tools:** Measure downhole flow rate, temperature, pressure, phase holdup (liquid vs gas vs water distribution)
- **Perforating guns:** Fire electrically-actuated shaped charges
- **Formation evaluation:** Downhole sampling tools (MDT, RFT)
- **Cased-hole logging:** CBL (Cement Bond Log), PLT (Production Logging Tool)

### Coiled Tubing (CT)

Continuous flexible tubing (1.5"–3.5" OD) wound on a large reel. Deployed into the wellbore through a BOP stack on the wellhead. Has both mechanical and hydraulic capability.

**CT interventions in Angola:**
- **Scale removal:** Pump acid (HCl for carbonate scale, HF for silicate scale) through CT into the wellbore
- **Wax removal:** Pump hot oil or solvent through CT to melt paraffin
- **Sand cleanout:** CT + nitrogen or water to circulate sand out of the wellbore
- **Jetting / stimulation:** Acid jetting through a coil-to-nozzle configuration
- **Nitrogen kick-off:** Inject N₂ down CT to unload liquid and restart a dead well

**CT advantages over wireline:** Continuous real-time pumping capability. Can provide fluid to any downhole operation.

**CT limitations:** Limited weight on bit capability. Complex surface equipment. Expensive.

---

## Part 10: Angola Deepwater — Dual Barrier and Subsea Completion

Angola's deepwater subsea wells require a **dual barrier** design — two independent, tested, failsafe-closed barriers between the wellbore and the surface at all times.

**Barrier philosophy for Angola deepwater:**
- **Barrier 1:** DHSV (Downhole Safety Valve) — failsafe closed, hydraulically actuated
- **Barrier 2:** Subsea tree PMV and PWV (Production Master Valve and Production Wing Valve) — both failsafe closed

At no point during normal operations or any workover should both barriers be simultaneously open and untested.

**Tubing hanger and subsea tree interface:**
In a horizontal tree design (standard for Angola), the tubing hanger is installed in the wellhead bore. The tree is then installed over it. The tubing hanger has annulus access ports that connect to the tree's annulus circuit — allowing monitoring of casing annulus pressure.

**Well integrity testing:**
- DHSV: tested for closure and pressure integrity every 3–6 months (via hydraulic test from FPSO)
- Subsea tree valves: function-tested and pressure-tested on a defined schedule per the well integrity management plan

---

## Part 11: Technical Interview Questions

1. Why is sand control necessary in Angola turbidite completions? What are the consequences of sand production?
2. Compare OHGP vs CHGP. Under what conditions would you choose one over the other?
3. Explain how a gas lift valve works and why gas lift is preferred over ESP in many Angola wells.
4. What is the failsafe principle of a DHSV? How is it controlled from the FPSO?
5. What is a premium tubing connection and why is it required in deepwater completions?
6. What is the purpose of the packer in a deepwater completion?
7. Describe the dual barrier philosophy for Angola deepwater wells. Name the two barriers.
8. What is gravel sizing and how do you select the correct gravel size for a formation?
9. What is the difference between slickline and electric line? Give two jobs for each.
10. Why is completion fluid filtered to < 2 micron? What happens if unfiltered brine is used?
11. What is underbalanced perforating and what are its advantages?
12. What corrosion-resistant material would you specify for tubing in a well with 3% CO₂?
13. Describe a typical coiled tubing scale removal job on an Angola FPSO well.
14. What is a tubing hanger? Where does it sit in a horizontal subsea tree design?
15. What tests do you perform on a DHSV during commissioning of a new well?

---

## Part 12: Study Resources

| Resource | Format | Notes |
|---|---|---|
| "Well Completion Design" — Economides, Watters, Dunn-Norman | Textbook | The standard completions textbook |
| "Petroleum Engineering Handbook Vol. II" (Drilling Engineering) | SPE Textbook | Completions chapters |
| Halliburton Completions Technical Manual | Free on halliburton.com | Industry's most practical completions reference |
| Baker Hughes Completions Catalog | Free online | Real Angola-applicable equipment descriptions |
| SLB OneSubsea completion equipment brochures | Free online | Subsea tree and tubing hanger systems |
| "The Technology of Artificial Lift Methods" — Brown | Textbook | Gas lift in depth |
| SPE OnePetro: "Angola gravel pack" OR "Angola OHGP" | Papers | Case studies from Block 17/32 completions |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/06_Completions_Path.md](../paths/06_Completions_Path.md)*  
*Where to learn: [PetroWiki](https://petrowiki.spe.org/Well_completions) | [IWCF L2](https://iwcf.org) | [Learning Resources](../../../docs/learning-resources.md)*
