# Skill 08 â€” FPSO Process Operations

> **Applies to:** Production Operator / Process Operator ([FPSO](../glossary.md)), Production Engineer (offshore), Operations Engineer, Process Engineer
> **Companies in Angola:** [SBM Offshore](../../data/company-directory/sbmoffshore.md), Yinson Production, BW Offshore, MODEC â€” FPSO operators; also [TotalEnergies](../../data/company-directory/totalenergies.md), Eni, Azule Energy operations teams
> **Schedule:** 28/28 rotation; 12-hour shifts on the [FPSO](../glossary.md) production deck or control room

---

## What Is This Skill?

An [FPSO](../glossary.md) (Floating Production, Storage and Offloading) vessel is essentially a floating oil processing plant. It receives crude oil and gas from subsea wells, separates the oil from gas and water, treats each stream to export quality, stores the oil, and offloads it to shuttle tankers. A Production/Process Operator on an [FPSO](../glossary.md) is responsible for operating and maintaining the process equipment that makes this happen â€” every hour of every day.

This is one of the most direct entry-level offshore roles for petroleum engineering graduates with a strong background in surface production systems and fluid mechanics.

---

## Why It Matters Offshore in Angola

Angola's flagship FPSOs (Kaombo Norte, Kaombo Sul, CLOV, Dalia, Pazflor, Girassol, Kizomba A/B, N'Goma) are massive processing plants â€” each processing 100,000â€“250,000+ barrels of oil per day. These are multi-billion dollar assets. Production Operators who understand the engineering behind the equipment are far more effective than those who just follow procedures blindly â€” and they advance much faster.

**Kaombo Norte [FPSO](../glossary.md) ([TotalEnergies](../../data/company-directory/totalenergies.md), Block 32):** 115,000 bopd capacity, 5 production wells, water depth 1,700â€“2,100m.

---

## Key Concepts to Master

### 1. FPSO Layout and Process Flow (Overview)

```
SUBSEA WELLS
     â”‚
     â”œâ”€ Production manifolds (subsea)
     â”‚
RISERS (flexible pipes from seafloor to FPSO)
     â”‚
     â–¼
PRODUCTION MANIFOLD (on FPSO â€” directs flow to process trains)
     â”‚
     â–¼
SEPARATION TRAINS  â†â”€â”€ [Most critical process on the FPSO]
     â”‚
     â”œâ”€â”€â”€ OIL TREATMENT TRAIN â”€â”€â†’ Oil storage tanks â†’ Offloading pumps â†’ Shuttle tanker
     â”‚
     â”œâ”€â”€â”€ GAS TREATMENT TRAIN â”€â”€â†’ Gas compression â†’ Gas injection (reservoir pressure support)
     â”‚                                             â†’ Gas export pipeline (if applicable)
     â”‚                                             â†’ Fuel gas (power generation)
     â”‚
     â””â”€â”€â”€ PRODUCED WATER TREATMENT â”€â”€â†’ Clean water overboard / re-injection
```

---

### 2. Separation â€” The Core Process

**Three-phase separation** removes oil, gas, and water from the incoming wellstream.

#### First Stage Separator
- Incoming wellstream enters at high pressure (typically 20â€“60 bar depending on reservoir pressure)
- **Gas flashes off** (released from solution due to pressure drop) â€” rises to top
- **Oil** accumulates in the middle
- **Water** (produced formation water) sinks to bottom

**Principle:** API gravity difference between oil (lighter) and water (heavier), plus degassing from pressure reduction

#### Second Stage Separator / Intermediate Pressure (IP) Separator
- Takes liquid from first separator at lower pressure
- removes more dissolved gas
- Further separates oil from water

#### Third Stage Separator / Low Pressure (LP) Separator
- Final degassing stage â€” oil exits with minimal gas
- "Stock tank oil" condition â€” ready for storage

#### Heater Treaters / Electrostatic Coalescers
- Heat the oil-water emulsion to break it
- Electrostatic field coalesces small water droplets â†’ easier separation
- **BS&W (Basic Sediment & Water):** Target < 0.5% water in export oil (contractual requirement)
- If BS&W exceeds spec, the oil **cannot be exported** â€” major production deferment alert

---

### 3. Key Process Systems on an FPSO

#### 3.1 Gas Compression Train
- Compresses gas from separator vapor to injection pressure or export pressure
- **Compression stages:** Multiple stages with interstage cooling (compressed gas heats up)
- **Gas injection:** Reinjecting produced gas into reservoir maintains reservoir pressure â†’ increases oil recovery
- In Angola, nearly all associated gas is either reinjected or compressed to fuel â€” gas flaring is being phased out

#### 3.2 Produced Water Treatment
Produced water is salty formation water produced alongside oil. It contains dissolved hydrocarbons and cannot be discharged without treatment.

**Treatment sequence:**
```
Produced water â†’ Skim tanks â†’ Hydrocyclone (deoiling) â†’ Flotation unit (IGF/CGF) â†’ Overboard
```

**Target:** Oil-in-water < 30 mg/L (OSPAR standard for offshore discharge in West Africa)

**Re-injection (alternative):** Most Angola FPSOs reinject water into the reservoir (waterflood) â€” maintains pressure and avoids overboard discharge entirely.

#### 3.3 Chemical Injection Systems
Multiple chemical injection skids dose chemicals into the process for:
- **Scale inhibitor** â€” prevents calcium carbonate/barium sulfate scale in pipes
- **Corrosion inhibitor** â€” protects steel pipework
- **Demulsifier** â€” helps break oil-water emulsions in separators
- **Biocide** â€” prevents bacterial growth in produced water
- **Hydrate inhibitor (MEG/methanol)** â€” prevents hydrate formation in subsea flowlines

#### 3.4 Oil Storage and Export
- Crude oil stored in cargo tanks (hull of [FPSO](../glossary.md) below the topsides)
- Offloaded to shuttle tankers approximately every 1â€“3 weeks
- **Tandem offloading:** Shuttle tanker moors 50â€“100m behind [FPSO](../glossary.md) connected by floating hose
- **Export metering:** Custody transfer meters measure volume and quality (API gravity, BS&W, temperature) for commercial purposes â€” must be highly accurate

#### 3.5 Power Generation
- [FPSO](../glossary.md) uses its own fuel gas (from process) to power gas turbine generators
- Typical FPSO power: 30â€“80 MW
- **Waste Heat Recovery Unit (WHRU)** uses turbine exhaust to heat process fluids

---

### 4. Key Process Parameters to Monitor

| Parameter | Why it matters | Action if abnormal |
|---|---|---|
| **Separator pressure** | Controls separation efficiency and backpressure on wells | Adjust control valve (PCV) |
| **Separator level (oil, water)** | If too low, gas blows through oil or water outlets | Level control valves |
| **GB&W / BS&W** | Export oil quality spec | Adjust demulsifier dose, heater temp, or separator retention time |
| **Gas flare rate** | Regulatory and environmental complinace | Investigate process upsets causing unplanned flaring |
| **Produced water oil-in-water** | Environmental compliance (< 30 mg/L) | Adjust treatment chemicals or flow |
| **Compressor suction/discharge pressure** | Efficiency and mechanical integrity | Adjust speed, check valves, alert maintenance |
| **Chemical injection rates** | Scale, corrosion, hydrate prevention | Check pumps, verify dosing |

---

### 5. Alarm Response and Operator Responsibilities

A Production Operator on a 12-hour shift is responsible for:

1. **Rounds:** Physical walk-through of process deck every 2â€“4 hours â€” check pressures, temperatures, leaks, abnormal sounds
2. **Alarm management:** Respond to DCS (Distributed Control System) alarms â€” investigate and resolve or escalate
3. **Sampling:** Collect process samples (oil BS&W, produced water oil-in-water, gas analysis) and send to lab
4. **Chemical injection checks:** Verify correct dosing rates for all chemical skids
5. **Logbook:** Maintain detailed shift log of all events, readings, and actions
6. **PTW (Permit to Work):** Issue, verify, and close out PTW for any maintenance on live equipment
7. **Flaring:** Minimize flaring; report any unplanned flaring to OIM

---

### 6. FPSO Process Safety: Critical Concepts

**Safety instrumented systems (SIS):**
- Every piece of equipment has a **shutdown (ESD) logic**: on high pressure â†’ PSV (pressure safety valve) opens; on high-high pressure â†’ automatic shutdown
- **Emergency Shut Down (ESD) levels:**
  - ESD Level 1: Individual equipment shutdown
  - ESD Level 2: Process train shutdown  
  - ESD Level 3: Full production shutdown
  - ESD Level 4: Emergency shutdown + deluge (fire water)

**Process Hazard Analysis (HAZOP):** Every process modification must go through HAZOP review before implementation.

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Draw the complete [FPSO](../glossary.md) process flow from wellhead to storage
- [ ] Understand three-phase separation: what happens in each stage
- [ ] Learn gas compression: why multiple stages, interstage cooling
- [ ] Know what BS&W is and why it has a hard limit for export

### Intermediate (2â€“6 months)
- [ ] Study HYSYS (Aspentech) or PROII for process simulation basics â€” both have free trials or university licenses
- [ ] Learn P&ID notation: read a process and instrumentation diagram
- [ ] Understand produced water treatment to OSPAR standards and Angola regulatory requirements
- [ ] Study chemical injection systems and why each chemical is needed

### Advanced (6â€“12 months)
- [ ] Study real [FPSO](../glossary.md) operation manuals ([SBM Offshore](../../data/company-directory/sbmoffshore.md) and [TotalEnergies](../../data/company-directory/totalenergies.md) publish technical documents publicly)
- [ ] Learn compressor performance curves: head vs. flow, surge lines, anti-surge control
- [ ] Study offshore process safety: ALARP, SIL ratings, HAZOP methodology
- [ ] Learn DCS systems: SCADA basics, Honeywell or Yokogawa control systems

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **Bai & Bai, "Subsea Production Systems"** | Process and subsea engineering | Paid |
| **ASPENTECH HYSYS (free edu license via AspenTech EDU)** | Process simulation software | Free via university |
| **[SBM Offshore](../../data/company-directory/sbmoffshore.md) public technical reports** | FPSO engineering insights | Free â€” sbmoffshore.com |
| **[TotalEnergies](../../data/company-directory/totalenergies.md) FPSO Block 17 technical publications** | Angola-specific | Free via TotalEnergies technical library |
| **Petrowiki â€” Production Facilities** | Comprehensive reference | Free |
| **GPSA Engineering Data Book** | Gas processing standard reference | Industry standard â€” available from GPSA |
| **YouTube: "[FPSO](../glossary.md) explained"** | Visual overview of an FPSO | Free |

---

## Practice Questions

1. Describe the sequence of fluid processing from the subsea wellhead to crude oil storage on an [FPSO](../glossary.md).
2. What is BS&W? Why does it have a hard contractual limit, and what causes it to exceed spec?
3. Angola regulations require oil-in-water < 30 mg/L before overboard discharge. Name three treatment steps that achieve this.
4. Why is gas reinjected in Angola rather than flared or exported?
5. A separator level control valve is stuck fully open. What happens to the downstream process?
6. You smell hydrocarbon gas on the process deck during your rounds. What are your first three actions?

---

## Related Skills

- [09 â€” Artificial Lift Systems](09-artificial-lift.md) (how oil gets to the [FPSO](../glossary.md) from the wells)
- [10 â€” Flow Assurance](10-flow-assurance.md) (what happens in the subsea flowlines before the [FPSO](../glossary.md))
- [11 â€” Subsea Systems](11-subsea-systems.md) (subsea infrastructure that delivers flow to the [FPSO](../glossary.md))
- [12 â€” Offshore HSE & Safety](12-offshore-hse-safety.md) (PTW, HAZOP, emergency response)
- [15 â€” Well Integrity](15-well-integrity.md) (wellhead pressure monitoring for FPSO operators)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Surface Facilities** | Free reference | Free | [petrowiki.spe.org/Surface_facilities](https://petrowiki.spe.org/Surface_facilities) |
| **Aspen HYSYS** | Process simulation (student) | Free student license | [aspentech.com/university](https://www.aspentech.com/en/university-program) |
| **Udemy â€” Oil and Gas Processing** | Paid course | $10â€“30 | [udemy.com](https://www.udemy.com) |
| **PetroSkills â€” Surface Facilities** | Paid course | $1,000â€“3,000 | [petroskills.com](https://www.petroskills.com) |
| **Petroleum Production Engineering** (Guo et al.) | Textbook | ~$90 | [Elsevier](https://www.elsevier.com) |
| **YouTube â€” FPSO process overview** | Free video | Free | Search "FPSO process overview" on YouTube |

â†’ Full directory: [Learning Resources](../learning-resources.md)

