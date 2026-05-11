# Skill 12 â€” Offshore HSE & Safety Management

> **Applies to:** ALL offshore roles â€” HSE Officer, Drilling Engineer, Production Operator, Subsea Engineer, Field Engineer
> **Offshore relevance:** HSE competency is a prerequisite for ANY offshore employment. You cannot board a rig or [FPSO](../glossary.md) without baseline HSE certifications, and HSE attitudes are checked at every interview

---

## What Is This Skill?

Health, Safety, and Environment (HSE) is the management of risk to people, assets, and the environment in industrial operations. Offshore, where a fire, blowout, or structural failure can kill dozens of people with no possibility of rapid external help, HSE is not optional or bureaucratic â€” it is the primary system that keeps people alive. For an Angolan offshore career, understanding HSE is both a regulatory requirement (you must have [BOSIET](../glossary.md) before going offshore) and a core competency evaluated at every technical interview.

---

## Why It Matters Offshore

- **Regulatory:** ANPG (Angola's regulator) and operators require all offshore workers to hold valid survival certificates (STCW/[BOSIET](../glossary.md)) before going offshore
- **Employment:** Every OFS company ([SLB](../../data/company-directory/slb.md), [Baker Hughes](../../data/company-directory/bakerhughes.md), Halliburton, [TotalEnergies](../../data/company-directory/totalenergies.md)) has mandatory HSE induction training and expects candidates to speak the language of risk management
- **Angola specifics:** Angola's offshore operations are governed by Presidential Decree 43/19 and follow IMCA and IOGP standards; international operators apply their own global HSE standards on top

---

## Key Concepts to Master

### 1. Risk Assessment

Risk is the combination of **likelihood** (probability an event occurs) and **consequence** (severity if it does). The fundamental tool is the **Risk Matrix**.

#### Risk Matrix (5Ã—5)

```
             CONSEQUENCE â†’
              1-Negligible  2-Minor  3-Moderate  4-Major  5-Catastrophic
L  5-VeryLikely    M          H        VH          VH          E
I  4-Likely        L          M         H          VH          VH
K  3-Possible      L          M         M           H          VH
E  2-Unlikely      VL         L         M           M           H
L  1-Rare          VL         VL        L           M           H
â†“
```
**L=Low, M=Medium, H=High, VH=Very High, E=Extreme**

**ALARP (As Low As Reasonably Practicable):**
The principle that risk must be reduced until the cost of further reduction is grossly disproportionate to the benefit. HSE law in Angola (and UK/Norwegian standards applied by operators) requires all High and VH risks to be reduced to ALARP.

---

### 2. Permit to Work (PTW) System

The Permit to Work is the formal written system that controls hazardous work offshore. **Before ANY non-routine work begins, a permit must be issued.**

#### PTW Hierarchy (Angola FPSO / Rig)

| Permit type | When used |
|---|---|
| **Hot Work Permit** | Any work that generates sparks/heat near flammable areas (welding, grinding, cutting) |
| **Cold Work Permit** | Non-ignition work on electrical or mechanical systems |
| **Confined Space Entry Permit** | Entry into tanks, vessels, enclosed spaces |
| **Electrical Isolation Permit** | Isolation of electrical equipment before maintenance |
| **Excavation and Penetration Permit** | Used onshore or on the deck |

#### PTW Process Flow

```
1. REQUESTOR raises permit describing task, hazards, controls
2. AREA AUTHORITY reviews and adds conditions
3. PTWAAU isolations confirmed (LOTO applied)
4. GAS TEST carried out by trained gas tester
5. PERMIT ISSUED with validity time window
6. WORK STARTS â€” permit displayed at worksite
7. WORK COMPLETE â€” area cleaned, normal state restored
8. PERMIT CLOSED by area authority + requestor sign-off
```

**Simultaneous Operations (SIMOPS):** When multiple work activities could create combined hazards (e.g., hot work while crane lifts â€” crane drops object, causes spark in flammable atmosphere), the SIMOPS matrix is used.

---

### 3. LOTO â€” Lock Out Tag Out

The process of isolating and securing energy sources before maintenance work begins.

**Energy types to isolate:**
- **Electrical:** De-energize and lock electrical panel
- **Pressure (hydraulic/pneumatic):** Close and lock valves, bleed down residual pressure
- **Stored energy:** Bleed accumulators, check for spring-loaded components
- **Gravity:** Block raised equipment against falling

**LOTO steps:**
1. Identify all energy sources
2. Notify affected personnel
3. Shut down equipment in controlled manner
4. Apply isolation devices (locks + tags)
5. Verify zero energy state (try to start, test pressure)
6. Perform work
7. Remove LOTO in reverse order
8. Restore to normal and confirm with operations

---

### 4. HAZOP (Hazard and Operability Study)

**What it is:** A structured, systematic study of process design to identify hazards and operability problems. Used in design stage of FPSOs and [subsea systems](11-subsea-systems.md).

**Method:**
- A multidisciplinary team reviews the P&ID (Piping and Instrumentation Diagram) section by section
- Apply guide words (No/More/Less/As well as/Part of/Reverse/Other than) to process parameters (Flow, Pressure, Temperature, Level, Composition)
- For each deviation: identify causes, consequences, safeguards, recommended actions

**Example:**
- Node: Inlet separator
- Parameter: Pressure
- Guide word: MORE
- Deviation: HIGH PRESSURE in separator
- Causes: Downstream blockage, gas carry-under, PSV failure
- Consequences: Rupture, vessel failure, fire
- Safeguards: PSV (pressure safety valve), HIPPS (High Integrity Pressure Protection System), high-pressure alarm + shutdown
- Action: Verify PSV set point and maintenance interval

---

### 5. Barrier Model â€” Bow-Tie Analysis

**The bow-tie model** visualizes the relationship between hazards, causes, consequences, and barriers:

```
                    [PREVENTIVE BARRIERS]              [RECOVERY BARRIERS]
                          |                                   |
Cause 1 â†’               |                                   |           â†’ Consequence 1
Cause 2 â†’ â†’ â†’ â†’ â†’ â†’ [HAZARDOUS EVENT] â†’ â†’ â†’ â†’ â†’ â†’ â†’ â†’ â†’ |           â†’ Consequence 2
Cause 3 â†’         (e.g. loss of containment)              |           â†’ Consequence 3
```

Each barrier is a control measure that prevents escalation. If barriers fail (the "swiss cheese" model â€” holes align), an incident occurs.

**Critical barriers offshore:**
- Well barriers (BOP, casing, wellhead)
- Process safety barriers (PSVs, HIPPS, ESD system)
- Active fire and gas detection
- Passive fire protection (PFP coating on structural steel)
- Personnel protective equipment (PPE)
- Emergency response procedures

---

### 6. Emergency Response Procedures

#### ESD (Emergency Shutdown) System Levels

| Level | Trigger | Action |
|---|---|---|
| **ESD 0 (Process Shutdown)** | Process exceedance (high pressure, etc.) | Shuts down process equipment only |
| **ESD 1 (Partial Platform SD)** | Fire/gas in one zone | Isolates affected module; closes SDVs in that zone |
| **ESD 2 (Full Platform SD)** | Major fire/gas/blowout | Shuts down ALL production + compression; deploys DEP |
| **ESD 3 ([FPSO](../glossary.md) Abandon)** | Catastrophic emergency | Full mustering and lifeboat deployment |

#### Muster and Abandon Ship

1. **General alarm sounds** (7 short + 1 long): All personnel stop work, don life jacket and survival suit, proceed to assigned muster station
2. **Roll call at muster station:** OIM/Muster Coordinator checks all personnel accounted for
3. **Instructions issued:** PA system â€” may be "stand by" (wait), "proceed to survival craft," or "abandon ship"
4. **Lifeboat deployment:** Enclosed lifeboats (totally enclosed motor propelled survival craft â€” TEMPSC) â€” minimum complement capacity for all plus 25% extra

#### H2S Emergency Response

[H2S](../glossary.md) (hydrogen sulfide) is a colorless, highly toxic gas:
- **TLV (Threshold Limit Value):** 1 ppm (smell detectable â€” "rotten eggs")
- **ACGIH STEL:** 5 ppm (15 min)
- **IDLH (Immediately Dangerous to Life/Health):** 100 ppm
- **Lethal concentration (rapid):** >500 ppm â€” instant knockdown without warning

**Response procedure:**
1. Sound [H2S](../glossary.md) alarm
2. Move upwind to muster station
3. Don SCBA (Self-Contained Breathing Apparatus) before entering affected zone
4. Account for personnel in [H2S](../glossary.md) zone
5. Medical response for casualties (rescue breathing â€” trained responder only)

---

### 7. BOSIET & Offshore Survival Certifications

These are mandatory certifications before your first offshore trip. They are obtained from OPITO-accredited training centers.

| Certification | Full Name | What it covers | Validity |
|---|---|---|---|
| **[BOSIET](../glossary.md)** | Basic Offshore Safety Induction & Emergency Training | Firefighting, evacuation, HUET, survival at sea, first aid (EHRB) | 4 years |
| **[HUET](../glossary.md)** | Helicopter Underwater Escape Training | Helicopter ditching, underwater egress, breathing systems (REBS/EBS) | Included in [BOSIET](../glossary.md) |
| **MIST** | Minimum Industry Safety Training (UK North Sea) | 12-module online + basic manual handling, dropped objects, etc. | Annual online refresh |
| **H2S Awareness** | H2S: Properties, detection, escape | H2S hazards, detection equipment, escape procedures | 2 years |
| **STCW Basic Safety** | Standards of Training, Certification and Watchkeeping (maritime) | Firefighting, first aid, personal survival, PSSR | 5 years |

**Angola note:** OPITO-approved centers in Angola include CEFOPETRO (Luanda) and the [SLB](../../data/company-directory/slb.md)/[TotalEnergies](../../data/company-directory/totalenergies.md) training centers. BOSIET obtained internationally is generally accepted.

---

### 8. Incident Investigation and Root Cause Analysis

**Incident categories:**
- **Near Miss / Unsafe Act / Unsafe Condition:** No injury â€” must be reported and investigated
- **First Aid Case (FAC):** Treatment below medical level
- **Medical Treatment Case (MTC):** Physician treatment required
- **Restricted Work Case (RWC):** Worker on restricted duties
- **Lost Time Injury (LTI):** Worker loses one or more shifts
- **Fatality**

**LTIR (Lost Time Injury Rate):** Standard metric
$$\text{LTIR} = \frac{\text{LTIs} \times 1,000,000}{\text{Man-hours worked}}$$

**Root Cause Analysis methods:** 
- **5 Whys:** Ask "Why?" repeatedly to trace from symptom to root cause
- **Fishbone (Ishikawa) diagram:** Categorize causes into: Man, Machine, Method, Material, Environment, Measurement
- **TapRootÂ®:** Systematic method used by many Angola operators

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Memorize the Risk Matrix and ALARP concept
- [ ] Understand the PTW system â€” why it exists and how a permit flows
- [ ] Know all [BOSIET](../glossary.md)/HUET content at conceptual level before attending the course
- [ ] Learn the ESD system levels and what each triggers
- [ ] Study [H2S](../glossary.md): properties, IDLH, response procedure

### Intermediate (2â€“5 months)
- [ ] Book and complete your [BOSIET](../glossary.md) course at an OPITO center
- [ ] Study IOGP (International Association of Oil and Gas Producers) Life-Saving Rules â€” 9 rules every operator enforces offshore
- [ ] Learn the bow-tie model â€” draw one for a well blowout event
- [ ] Study basic HAZOP: practice applying guide words to simple P&ID nodes
- [ ] Study LOLER / PSSR regulations (lifting operations, pressure systems) â€” referenced in Angola operations

### Advanced (5â€“12 months)
- [ ] Study NEBOSH International General Certificate (IGC) â€” recognized qualification for HSE Officer roles
- [ ] Read IOGP 459 "Life-Saving Rules" and all IOGP safety bulletins
- [ ] Complete IOGP / OPITO "Process Safety Fundamentals" course
- [ ] Study SEMS (Safety and Environmental Management System) â€” used by Angola IOCs
- [ ] Learn Behavior-Based Safety (BBS) principles â€” Dupont STOP program and similar

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **IOGP Life-Saving Rules** | 9 golden rules; free PDF | Free â€” iogp.org |
| **NEBOSH IGC Study Guide** | Full HSE qualification | ~$1,000â€“2,000 (exam + course) |
| **[BOSIET](../glossary.md) Course (OPITO)** | MANDATORY before going offshore | ~$500â€“1,500 depending on location |
| **IOGP Report 434: UFO (Unsafe Acts / Conditions)** | Root cause data | Free |
| **[TotalEnergies](../../data/company-directory/totalenergies.md) Angola HSE Charter** | Company specific standards | Free via TotalEnergies.com |
| **OPITO Standards (opito.com)** | All offshore training standards | Free summaries |

---

## Practice Questions

1. Using the 5Ã—5 risk matrix, rate the risk of "working at height without a harness" and explain your rating.
2. Describe the PTW process for a hot work job on the [FPSO](../glossary.md) production deck.
3. A gas cloud is detected in the accommodation module. Describe the first four actions you take.
4. What is ALARP and how would you apply it to the risk of dropped objects from a crane?
5. You discover a colleague skipped a LOTO lock on a pressure vessel. What do you do?

---

## Related Skills

- [08 â€” FPSO Process Operations](08-fpso-process-operations.md) (PTW governs all maintenance on process equipment)
- [01 â€” Well Control](01-well-control.md) (well kicks are the biggest [FPSO](../glossary.md)/rig safety event)
- [15 â€” Well Integrity](15-well-integrity.md) (integrity failures are HSE incidents)
- [11 â€” Subsea Systems](11-subsea-systems.md) ([ROV](../glossary.md) operations, diving, SIMOPS with subsea work)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **NEBOSH IGC** | Certification (online from Angola) | $350â€“600 | [Astutis](https://www.astutis.com) Â· [Red Oak](https://www.redoaktraining.com) Â· [nebosh.org.uk](https://www.nebosh.org.uk) |
| **IOSH Managing Safely** | Certification (online) | Â£250â€“400 | [iosh.com](https://iosh.com) |
| **BOSIET/HUET** | Certification (Angola) | $800â€“1,400 | PETROTEC Luanda (OPITO-accredited) |
| **OSHA Training** | Free online modules | Free | [osha.gov/training](https://www.osha.gov/training) |
| **IOGP Life-Saving Rules** | Free safety resources | Free | [iogp.org/safety](https://www.iogp.org/safety/) |
| **PetroWiki â€” HSE** | Free reference | Free | [petrowiki.spe.org/HSE](https://petrowiki.spe.org/Health,_safety,_and_environment_(HSE)) |
| **Lees' Loss Prevention** (Mannan, 3 vols) | Textbook (HSE bible) | ~$200 | [Elsevier](https://www.elsevier.com) |
| **Introduction to Health and Safety at Work** (Hughes & Ferrett) | NEBOSH companion | ~$40 | [Amazon](https://www.amazon.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md) Â· Angola certs: [Certifications Angola](../../isptec/tseluca/support/Certifications_Angola.md)

