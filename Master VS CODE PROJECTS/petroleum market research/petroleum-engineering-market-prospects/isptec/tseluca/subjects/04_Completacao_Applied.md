# Completação de Poços — Applied to Angola Subsea Wells
## From Gravel Pack Equations to Block 17 Horizontal Trees

---

## Overview

Completação de Poços is one of the most directly applied ISPTEC subjects. The completion engineer's work determines how efficiently a well produces for the next 20–30 years. A poorly designed completion — wrong sand control method, undersized tubing, incorrect DHSV — cannot easily be fixed once the well is producing subsea at 1,500m water depth.

In Angola, completions engineering is dominated by the challenges of:
- Unconsolidated turbidite sands (sand control is mandatory in almost every well)
- Subsea horizontal trees (no surface access — everything must be done through the tubing)
- 1,000–2,500m water depth (no easy intervention)
- Long well lives (completions must last 20+ years)

This guide connects your ISPTEC Completação subject to the real engineering decisions that Halliburton, Baker Hughes, Weatherford, and operator completion teams make on Angola wells.

---

## Sand Control: The Dominant Angola Completion Decision

### Why Sand Control Is Non-Negotiable in Angola

Angola's turbidite reservoir sands are poorly consolidated. The sand grains are barely cemented together. Under the drawdown pressure of production, these grains are mobilised into the wellbore and carried to surface with the produced fluid.

**Consequences of sand production:**
- Erosion of FPSO process equipment (chokes, valves, separators)
- Erosion of tubing and wellhead components (potential well integrity failure)
- Plugging of completion screens
- Formation collapse around the wellbore (loss of permeability, reduced production)
- Loss of well integrity over time

**ANPG requirement:** Operators must have a sand management plan for each well. If sand production occurs, ANPG requires reporting and a remediation plan.

**Angola operator policy:** All TotalEnergies, Azule, and Eni Angola production wells are completed with sand control. This is a blanket policy, not a well-by-well decision.

---

### Sand Control Methods and Angola Suitability

#### 1. Openhole Gravel Pack (OHGP) — Most Common in Angola Deepwater

**Method:** A gravel pack screen is set in the open hole reservoir section. Gravel is pumped as a slurry down the tubing-casing annulus, out a crossover tool, and packed around the screen in the open hole. The gravel fills the annular space and supports the formation, while the screen prevents gravel from entering the tubing.

**Gravel sizing rule (Saucier criterion):**
$$d_{50,gravel} = 5 \times d_{50,formation}$$

Where d₅₀ is the median grain diameter by weight. For a typical Angola turbidite with d₅₀ = 0.15mm (fine-medium sand):
$$d_{50,gravel} = 5 \times 0.15 = 0.75 \text{ mm}$$

This falls in the 20/40 mesh gravel size range (0.42–0.84mm). Most Angola gravel packs use 20/40 or 16/30 mesh.

**Screen sizing:** The screen slot must retain the gravel but not plug with formation fines:
$$\text{Slot width} \approx d_{10,gravel}$$
For 20/40 mesh: slot width ≈ 0.2mm (200 micron premium wire-wrap screen)

**Why OHGP works in Angola turbidites:**
- Horizontal wells with 800–1,200m reservoir sections → open hole completion gives access to the entire reservoir section
- The turbidite sand quality (well-sorted, uniform grain size) makes gravel sizing predictable
- OHGP gives maximum inflow area and minimum skin (no perforation damage)

**Limitations:**
- Cannot be selectively placed in a specific zone (the entire open hole interval is completed)
- If the formation contains multiple zones with different pressure or fluid contacts, OHGP cannot isolate them
- Higher risk in very deviated wells with long reservoir sections (gravel packing efficiency decreases at >75° deviation in some conditions)

---

#### 2. Cased Hole Gravel Pack (CHGP)

**Method:** The production casing is run into the reservoir and cemented. Perforations are shot through the casing and cement into the reservoir. Gravel is then packed around a screen in the perforated interval.

**When CHGP is used in Angola:**
- Multi-zone wells requiring selective isolation between zones
- Wells where zonal isolation is important for water management
- Workovers where the original OHGP has failed and a second completion is needed

**Disadvantage vs OHGP:** Perforation damage skin. The perforations reduce effective permeability near the wellbore. In a high-perm Angola turbidite (100–500 mD), this skin can reduce production 10–20%.

---

#### 3. Standalone Screen (SAS)

**Method:** A wire-wrap screen or premium mesh screen is simply set in the open hole without gravel packing. The formation grains bridge naturally on the screen.

**Angola suitability:** Limited. SAS works only in well-sorted sands where fine-grained material is minimal. Angola turbidite thin-beds contain fine-grained material that will plug a SAS over time.

**Where SAS is used in Angola:** Short, high-quality sand intervals in well-characterised reservoirs with limited fine content. This is a minority of Angola completions.

---

#### 4. FracPack

**Method:** A hydraulic fracture is created simultaneously with the gravel pack. High-viscosity fluid is pumped at fracturing rates, breaking down the formation and creating a short, wide fracture. As the fracture closes on the gravel, a short, highly conductive path is created from the reservoir to the wellbore.

**Angola applicability:** FracPack is used in the moderate-permeability range (1–50 mD), where bypass of near-wellbore damage via the fracture improves productivity significantly. Angola's main turbidite reservoirs (>100 mD) typically do not benefit from FracPack — the skin from perforation damage is small relative to the overall productivity.

FracPack is more relevant to Angola's tighter gas sands or sub-commercial discoveries in lower-quality reservoirs.

---

## Tubing Design and Selection

**What ISPTEC taught:** Tubing sizes, material grades, burst and collapse, premium connections.

### Tubing Sizing

The tubing must carry the target liquid rate without excessive pressure loss. But a larger tubing means less annular area for gas lift.

**Flow velocity limits:**
- Minimum velocity: > 1.5 m/s to transport liquids and avoid phase separation stratification
- Maximum velocity (erosion limit): < erosion velocity, calculated by:
  $$V_{erosion} = \frac{C}{\sqrt{\rho_m}}$$
  Where C = 100 (empirical constant for clean service), ρ_m = mixture density (kg/m³)

**Angola typical tubing selection:**

| Production Rate | Typical Tubing OD | Notes |
|----------------|------------------|-------|
| < 5,000 bbl/day | 3½" (88.9mm) | Low-rate or late-life wells |
| 5,000–12,000 bbl/day | 4½" (114.3mm) | Most Angola development wells |
| 12,000–25,000 bbl/day | 5½" (139.7mm) | High-rate producers |
| > 25,000 bbl/day | 7" (177.8mm) | Very high-rate wells on large FPSOs |

### Material Selection

Angola's deepwater environment is corrosive: CO₂ in the produced gas causes carbonate scale and carbonic acid attack on carbon steel tubing.

**Key ISPTEC subject connection: Ciências dos Materiais e Corrosão**

| Condition | Material Grade | Notes |
|-----------|---------------|-------|
| Sweet service (no H₂S, low CO₂) | L-80 or J-55 carbon steel | Lowest cost, adequate for some Angola wells |
| Moderate CO₂ | 13Cr stainless steel | Most common in Angola — good CO₂ resistance |
| High CO₂ + Cl⁻ | Super 13Cr (S13Cr) | Enhanced chromium, better pitting resistance |
| High CO₂ + H₂S present | Duplex stainless steel (DSS 22Cr or 25Cr) | Resists both CO₂ and H₂S |
| Very high H₂S (HP/HT) | High alloy (Inconel) | Extreme cost, only for very aggressive conditions |

**How to determine which grade is needed:**
1. Obtain produced fluid chemistry from PVT lab (CO₂ partial pressure, H₂S concentration, Cl⁻ concentration)
2. Plot on ISO 15156 (NACE MR0175) corrosion resistance chart
3. Select the lowest-cost material grade that falls in the acceptable zone

Most Angola Block 17/32 wells: 13Cr or S13Cr tubing (moderate CO₂, low to zero H₂S).

---

### Premium Threaded Connections

**The Angola subsea requirement:** All connections in a subsea well must have premium threaded and coupled (T&C) connections. These are machined to tighter tolerances than API connections, with metal-to-metal seals that provide both structural integrity and fluid-tight sealing.

**Why API connections are not acceptable subsea:**
- API connections rely on thread compound (dope) for sealing → not reliable for long-term subsea pressure containment
- Metal-to-metal seal premium connections (VAM TOP, TenarisHydril Wedge, Atlas Bradford CS2) are designed for 20+ year service

**Connection selection criteria:**
- Internal pressure rating (must exceed burst design case)
- External pressure rating (must exceed collapse design case)
- Tension capacity (must handle string weight)
- Compression capacity (needed for deviated wells)
- Bending capacity (for high-doglegs)

---

## The Downhole Safety Valve (DHSV)

**What ISPTEC taught:** DHSV function and placement.

**Industry detail for Angola subsea wells:**

Every Angola deepwater production well has a DHSV installed in the upper section of the completion tubing, typically 30–100m below the wellhead (i.e., just below the seabed for subsea wells).

**DHSV installation depth selection:**
- Must be below the wellhead/tree (for subsea wells: below the mudline)
- Must be accessible by wireline (for retrieval if the DHSV fails)
- Should be in a section of the tubing with no significant profile or restriction

**DHSV control line:**
A ¼" or ⅜" OD stainless steel hydraulic control line runs from the DHSV up to the subsea tree, through the umbilical to the FPSO. Hydraulic pressure (150–200 bar) from the FPSO keeps the valve open. Loss of control line pressure causes the valve to close (fail-safe closed).

**DHSV test procedure (as you will execute on your first offshore job):**
1. Inform FPSO control room: about to test DHSV on Well XX
2. Close the well choke (reduce production to near-zero)
3. Close the master valve above the DHSV test point
4. Bleed hydraulic pressure from the control line → DHSV closes
5. Open well choke → monitor tubing head pressure
6. If THP remains stable (no pressure build) → DHSV is holding → test passed
7. If THP builds → DHSV has a leak → test failed → require intervention
8. Re-open control line pressure → DHSV opens → restore production
9. Document result in well integrity management system

---

## Perforating Design

**What ISPTEC taught:** Perforation tunnel geometry, penetration depth, shot density.

**Industry workflow:**

**Step 1: Select shot density**
Standard perforation design for Angola horizontal wells:
- SPF (shots per foot): 12–18 SPF for open hole liner perforations (less common in Angola)
- For cased hole: 12–18 SPF, 60° phasing (balanced entry)
- For FracPack: 6 SPF, 0° phasing (all in one plane for fracture initiation)

**Step 2: Balance or underbalance?**
- **Overbalanced perforation:** Wellbore pressure > formation pore pressure → mud invades perforation tunnel. Simple but results in damaged perforations with higher skin.
- **Underbalanced perforation:** Wellbore pressure < formation pore pressure → formation fluid flows into wellbore at moment of perforation → cleans the tunnel. Reduces skin to near zero but requires well control procedures to manage the inflow.

In Angola, underbalanced perforation using tubing-conveyed perforating (TCP) guns on a wire is standard for cased hole completions. This directly uses your Engenharia de Poços knowledge (pore pressure, formation pressure, differential pressure management).

**Step 3: Interval selection**
Use log data (from Avaliação de Formações):
- Perforate intervals where: φ > cutoff AND Sw < cutoff AND GR indicates clean sand
- Avoid perforating: water zones (high Sw), shale interbeds (low porosity), intervals with high GOR that would cause early gas breakthrough

---

## Angola Subsea Tree Interface

**The unique Angola challenge:** All Angola deepwater production wells are completed as subsea wells with horizontal trees (also called horizontal xmas trees or HXT). This is different from a conventional land or platform well where the tree sits on top of the casing.

**Horizontal tree (HXT) key features:**
- The master valve and wing valve are in horizontal positions on the tree body (not vertical)
- The tubing hanger lands inside the tree body, sealing the production annulus
- The tree sits on the subsea wellhead, which sits on the seabed
- All valve actuation is hydraulic, from the FPSO via the umbilical
- The DHSV in the completion tubing is the deepest valve in the system

**What this means for completions design:**
1. All completion operations (gravel pack, tubing installation, DHSV installation) are done through the drilling BOP/riser before the subsea tree is installed
2. Once the tree is installed, the only access to the well is through the tubing bore (slickline, e-line, or coiled tubing)
3. This means the completion design must be right the first time — major changes require a rig-assisted workover at $300,000+/day

---

## Completion Fluid Selection

**What ISPTEC taught:** Completion fluid requirements (non-damaging, density-matched, shale-compatible).

**Angola deepwater completion fluid practice:**

| Density Required | Fluid Type | Application |
|----------------|------------|-------------|
| 8.4 ppg | Seawater/KCl brine | Shallow, low-pressure reservoirs |
| 9.0–10.0 ppg | KCl/NaCl brine | Most Angola development wells at TD |
| 10.0–11.5 ppg | CaCl₂/NaCl blend | Moderately pressured reservoirs |
| 11.5–13.8 ppg | CaBr₂/NaCl blend | High-pressure Angola reservoirs |
| > 13.8 ppg | ZnBr₂/CaBr₂ blend | HP/HT wells |

**Reservoir damage control:** Completion fluids contact the formation during gravel packing. Any incompatibility causes permeability damage and reduced production. Required compatibility tests:
- Soak test: core samples soaked in completion fluid → measure permeability change (< 5% acceptable)
- Fluid-fluid compatibility: mix completion fluid with formation water → check for precipitation
- HPHT stability: fluid must maintain density and clarity at reservoir conditions (150°C, 700 bar)

---

## Interview Questions for Completions Engineering Roles

1. What are the four main sand control methods? For an Angola turbidite well, which would you recommend and why?
2. How do you size gravel for an OHGP in a formation with d₅₀ = 0.12mm?
3. What is the two-barrier principle and how does it apply to a completion design?
4. Why is 13Cr tubing preferred over carbon steel in Angola wells?
5. What is a DHSV and how do you test it on a subsea well?
6. Explain the difference between overbalanced and underbalanced perforation. When would you choose each?
7. What is a horizontal Christmas tree and how does it differ from a conventional vertical tree?
8. What causes a DHSV to fail open? What is the consequence?
9. An OHGP has been in service for 3 years and the production rate has declined significantly — PI is down 40%. What is your diagnostic process?
10. What properties must a completion fluid have for use in an Angola deepwater reservoir?

---

## Practical Next Steps

**To build real completions engineering capability before graduation:**

1. **Read Baker Hughes "Completion Design Manual" (Industry document)** — available through university engineering library or SPE digital library access. Covers gravel packing design in practical detail.

2. **Study API 11D1** — "Packers and bridge plugs" standard. Understand the packer classification (permanent, retrievable, inflatable) and testing requirements.

3. **Download NORSOK D-010** (well integrity) — Section 7 covers completion barrier requirements. This is what Angola operators' completions engineers work to.

4. **Connect to SPE completion groups** — SPE has several completion-focused technical sections. As a student member, you can access webinars and papers on Angola completions from TotalEnergies and Eni authors.

5. **Your Projecto I/II topic:** A completion design for a fictitious Angola well (define the formation, choose sand control, design gravel pack, select tubing, size DHSV, specify perforation interval) is an outstanding final project that demonstrates directly applicable knowledge.

---

*Continue to [05_Termodinamica_Gas_Applied.md](05_Termodinamica_Gas_Applied.md) for Termodinâmica Aplicada and Engenharia de Gás Natural applied to Angola flow assurance and gas processing.*  
*Where to learn: [Learning Resources](../../../docs/learning-resources.md)*
