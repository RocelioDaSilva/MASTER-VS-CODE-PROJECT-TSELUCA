# Skill Tutorial 07 — HSE for Offshore Environments

> **Applies to:** HSE engineers (CORE), every offshore worker (foundational knowledge)
> **ISPTEC connection:** Engenharia de Segurança, Gestão Ambiental, Engenharia Legal
> **Goal:** Understand the complete HSE management system for an offshore installation — from legal framework and risk management through PTW, HAZOP, emergency response, incident investigation, and KPI measurement.

---

## Part 1: The Legal and Standards Framework

You cannot work in offshore HSE without knowing which standards govern your work. Angola has its own regulatory body and also adopts international standards.

### Angola — ANPG (Agência Nacional de Petróleo, Gás e Biocombustíveis)

ANPG issues regulations under:
- **Decreto Presidencial n.º 39/16:** Main petroleum industry safety regulation
- **Decreto Executivo n.º 97/19:** Environmental Management in the petroleum sector
- **Decreto Executivo n.º 151/12:** Occupational health and safety in industry
- Operators must submit **Plano de Gestão de Segurança (PGS)** — Safety Management System
- **Environmental Impact Assessment (EIA)** required for all new development projects

### International Standards Referenced in Angola

| Standard | Organization | Topic |
|---|---|---|
| **API RP 75** | American Petroleum Institute | Safety and Environmental Management System (SEMS) for offshore |
| **NORSOK S-001** | Norwegian Petroleum Directorate | Technical Safety design standard — used by TotalEnergies, Equinor projects |
| **ISO 14001** | ISO | Environmental Management System |
| **ISO 45001** | ISO | Occupational Health and Safety Management System |
| **MODU Code** | IMO | Safety code for mobile offshore drilling units (drillships, semi-subs) |
| **SOLAS** | IMO | Safety of life at sea — applies to FPSOs as ships |
| **OSPAR Convention** | International | Protection of marine environment in the North-East Atlantic (referenced for discharge standards) |

---

## Part 2: Risk Management Framework

### The Hierarchy of Controls (in order of effectiveness)

1. **Elimination:** Remove the hazard entirely (best option)
2. **Substitution:** Replace with a less hazardous alternative
3. **Engineering controls:** Physical barriers, isolation, ventilation
4. **Administrative controls:** Procedures, training, permits, signs
5. **PPE:** Personal Protective Equipment (last resort, least effective)

### Risk Matrix

Risk = Likelihood × Severity

| | Severity 1 (Minor) | Severity 2 (Moderate) | Severity 3 (Major) | Severity 4 (Severe) | Severity 5 (Catastrophic) |
|---|---|---|---|---|---|
| **Likelihood 5 (Almost certain)** | Medium | High | High | Critical | Critical |
| **Likelihood 4 (Likely)** | Low | Medium | High | High | Critical |
| **Likelihood 3 (Possible)** | Low | Medium | Medium | High | High |
| **Likelihood 2 (Unlikely)** | Low | Low | Medium | Medium | High |
| **Likelihood 1 (Rare)** | Low | Low | Low | Medium | Medium |

**ALARP Principle (As Low As Reasonably Practicable):** Risks in the "High" zone must be reduced. Risks in the "Critical" zone must not proceed. Risks that are "Low" are tolerable. Everything in between must be ALARP — reduced as much as is reasonably practicable without disproportionate cost.

### Hazard Identification (HAZID)

A structured group exercise reviewing a project or operation to identify hazards systematically. Typically done at the concept stage, detailed design stage, and pre-commissioning stage. Outputs a hazard register with assigned risk levels and recommended controls.

---

## Part 3: Permit to Work (PTW) System

The PTW system is the administrative backbone of offshore safety. No hazardous non-routine work happens without a permit. The PTW ensures:
- All hazards are identified before work starts
- Correct isolations are in place
- The right people are involved
- Permit issuer knows what's happening on the installation at all times

### Permit Categories

| Permit Type | Used For | Key Requirements |
|---|---|---|
| **Cold Work Permit** | Non-sparking, non-ignition work in hydrocarbon-free areas | Verification of hazardous area classification |
| **Hot Work Permit** | Welding, grinding, cutting — ignition sources | Gas test, fire watch, 15m radius clearance of hydrocarbons, fire extinguisher |
| **Confined Space Entry** | Entry into tanks, vessels, pipes, voids | Atmospheric testing (O₂%, gas), stand-by man, rescue equipment, communication |
| **Electrical Permit** | Work on electrical systems, isolation of electrical equipment | LOTO (Lockout-Tagout) completed, arc flash assessment |
| **Radiography Permit** | Radiographic inspection using ionizing radiation | Exclusion zone, radiation monitor, dosimetry |
| **Excavation Permit** | Ground disturbance onshore, structural penetration offshore | Drawing check for buried cables/pipes |

### The Permit Workflow

```
1. JOB PLANNING
   Task leader plans the job. Identifies required isolations, PPE, tools.

2. ISOLATION REQUEST
   Operator performs physical isolations (valve closures, LOTO, blind flanges).
   Verifies isolated state (gas test, pressure check, zero energy).

3. PERMIT ISSUE
   Permit Issuer (Area Authority — typically senior platform engineer) reviews 
   the job plan, verifies isolations, checks no SIMOPS conflicts.
   Signs and issues the permit.

4. PERMIT ACCEPTANCE
   Task Performing Authority (crew supervisor) accepts the permit, briefs his 
   team on hazards and controls.

5. WORK EXECUTION
   Work performed within permit conditions. If conditions change → STOP, return 
   to permit issuer.

6. PERMIT HANDBACK / RETURN
   Work complete. Area cleaned up. System ready for reinstatement.
   Task Performing Authority hands permit back.

7. REINSTATEMENT
   Operator removes isolations and reinstates system.
   Permit closed.
```

### SIMOPS (Simultaneous Operations)

When multiple high-risk operations are happening concurrently on the same installation (e.g., wellwork + process maintenance + crane operations), the hazards of interference are managed by:
- **SIMOPS matrix:** A grid showing which activities can happen simultaneously and which cannot
- **Zone control:** Defining work exclusion zones around each activity
- **Daily operations meeting:** All parties brief simultaneously planned activities

---

## Part 4: Job Safety Analysis (JSA)

A JSA (also called Job Hazard Analysis — JHA) is a step-by-step hazard analysis of a specific job. Every task on an offshore installation should have a JSA before execution.

### How to Write a JSA

**Step 1: Break the job into sequential steps**
Each step should be a discrete action. For "Replace a flange gasket on a 6" process line":
1. Obtain permit and isolate line
2. Bleed down pressure and confirm zero pressure
3. Remove flange bolts
4. Remove old gasket, clean flange faces
5. Install new gasket, torque bolts to spec
6. Reinstate pressure and check for leaks
7. Return permit

**Step 2: Identify hazards for each step**
For each step, ask: what could go wrong? What are the energy sources? What could hurt someone?

**Step 3: Describe the controls for each hazard**
Controls must follow the hierarchy (engineering → administrative → PPE).

**JSA Table format:**

| Step | Potential Hazard | Risk Level (before controls) | Control Measure | Risk Level (after controls) | Responsible |
|---|---|---|---|---|---|
| 2. Bleed pressure | Residual pressure — line not fully depressurized | High | Verify on pressure gauge; open vent valve until stable; confirm with permit issuer | Low | Task leader |
| 4. Remove gasket | Contaminated surface — hot crude exposure | Medium | Chemical resistant gloves; face shield; have EWS ready | Low | All workers |

---

## Part 5: HAZOP Methodology

A HAZOP (Hazard and Operability Study) is a formalized, structured review of a process design to identify all scenarios where the process could deviate from its design intent — and what the consequences would be.

### HAZOP Guide Words

Applied to every design parameter (flow, temperature, pressure, composition) at every node:

| Guide Word | Meaning | Example deviation |
|---|---|---|
| **NO / NONE** | Complete absence of the parameter | No flow in a production header |
| **MORE** | Quantitative increase | High pressure in a separator |
| **LESS** | Quantitative decrease | Low flow through a pump |
| **AS WELL AS** | Qualitative increase — extra component | Produced water contaminated with gas carry-under |
| **PART OF** | Qualitative decrease — composition change | Incorrect fluid in a line |
| **REVERSE** | Opposite direction | Reverse flow through a check valve |
| **OTHER THAN** | Substitution — wrong fluid | Wrong chemical injected |

### HAZOP Session

A team of 5–8 people reviews P&IDs (Piping and Instrumentation Diagrams) node by node. For each node:
1. Apply each guide word to each parameter
2. Identify causes of the deviation
3. Identify consequences
4. Review existing safeguards (instruments, alarms, relief valves)
5. Determine residual risk (after safeguards)
6. Assign actions if risk is unacceptable

**Output:** HAZOP action register. Each action has an owner, target completion date, and is tracked to closure.

---

## Part 6: Fire and Gas Systems

### Fire Triangle and Fire Types

**Fire triangle:** Fuel + Oxygen + Ignition Source → Fire
Remove any one leg → fire cannot start or is extinguished.

**Offshore fire types:**

| Type | Medium | Extinguish with |
|---|---|---|
| **Class A** | Solid combustibles (wood, plastic) | Water, CO₂, foam |
| **Class B** | Flammable liquids (crude oil, diesel) | Foam, dry powder, CO₂ |
| **Class C** | Electrical fires | CO₂, dry powder (NOT water — electrocution risk) |
| **Class D** | Metal fires | Dry powder (specialized) |

### FPSO Fire Suppression Systems

- **Deluge system:** Water spray covering entire process modules. Activates on F&G detection or manually. Cools equipment, suppresses vapor clouds, limits fire spread.
- **High-expansion foam:** For enclosed areas (pump rooms, compressor areas). Fills the space with foam to exclude oxygen.
- **CO₂ fixed system:** For enclosed equipment rooms (electrical switchrooms). Displaces oxygen. Personnel must evacuate before activation.
- **Portable fire extinguishers:** Staged throughout the installation. CO₂ and dry powder types.
- **Fireman's outfit:** Full thermal protection suit + SCBA for the designated emergency response team members.

### Gas Detection

- **Catalytic bead detector:** Measures % of Lower Explosive Limit (LEL). Alarms at 10% LEL, trips at 20–25% LEL. Range: 0–100% LEL.
- **Infrared beam detector:** Line-of-sight gas detection across process areas. Good for large open spaces.
- **H2S point detector:** Electrochemical sensor measuring ppm H2S.
- **Flame detectors:** UV (ultraviolet) detectors respond in milliseconds to open flame. IR (infrared) for hydrocarbon fires.

---

## Part 7: Emergency Response

### Muster and Evacuation Hierarchy

**Muster → Rescue → Evacuation (in that order)**

1. **Muster:** All personnel go to muster stations (weather deck, typically). Head count taken. Await further instructions.
2. **Rescue:** If source of emergency is identified and controllable — emergency response team activates.
3. **Evacuation:** If the situation cannot be controlled — full evacuation of the installation.

### Evacuation Methods

| Method | Conditions | How |
|---|---|---|
| **TEMPSC (Totally Enclosed Motor Propelled Survival Craft) — Lifeboat** | Primary evacuation. Safe weather conditions. | Released from gravity davit. Self-propelled. Fireproof for 8 minutes in oil fire. |
| **Life raft** | Secondary. Lifeboat unavailable. | Hydrostatic release or manual inflation. |
| **Rescue boat (MOB boat)** | Man overboard recovery. | Davit-launched small craft. |
| **Helicopter** | Emergency medical evacuation. Casualty transfer. | Can also be primary evacuation if pre-arranged. |

**Helicopter emergency breathing system (HEBS):** A small compressed air bottle worn in the helicopter. If the helicopter ditches in the sea, you have ~90 seconds of air to escape from an inverted, submerged helicopter. This is what HUET training teaches you.

### Emergency Signals

- **PA announcement:** "Mayday" or specific emergency codes announced on the PA system
- **General Alarm:** Constant siren = muster required
- **Abandon Platform:** Continuous alternating fast/slow siren = evacuate immediately

---

## Part 8: Incident Investigation

When something goes wrong offshore — an injury, a near miss, a hydrocarbon release — the investigation process is mandatory, systematic, and reported to ANPG.

### Incident Classification

| Severity Level | Definition | Examples |
|---------------|------------|---------|
| **Fatality** | Death resulting from the incident | Person falls overboard and drowns |
| **LTI (Lost Time Injury)** | Injury requiring > 24 hours away from work | Fractured hand from dropped object |
| **Restricted Work Case (RWC)** | Injury limiting duties but person still works | Sprained back — light duties only |
| **Medical Treatment Case (MTC)** | Requires medical treatment beyond first aid | Lacerations needing stitches |
| **First Aid Case (FAC)** | Minor first aid treatment | Small cut, minor bruise |
| **Near Miss / Dangerous Occurrence** | Event with serious potential even if no injury | Dropped object that missed person |
| **HSE Critical (process safety)** | Unintended hydrocarbon release, fire, explosion | Gas leak from flange joint (H1 event) |

### Investigation Methods

**ICAM (Incident Cause Analysis Method):**
Used by TotalEnergies and many Angola operators. ICAM traces the incident back through:
1. **Absent or failed defences** (what barriers should have stopped this?)
2. **Individual and team actions** (what did people do or fail to do?)
3. **Task/environmental conditions** (what made the task difficult?)
4. **Organisational factors** (underlying management system failures)

**Bow-tie Analysis:**
Visually maps the causal chain:
```
[Top Event (Hazard Released)]
  ←THREATS→ [TOP EVENT: Gas release] ←CONSEQUENCES→
                    │
              Preventive                   Mitigating
              controls                    controls
           (left side of                 (right side of
            the bow-tie)                  the bow-tie)
```

**5 Whys Analysis:**
For simpler incidents: ask "why?" 5 times to get to root cause. Starting from the event, each answer is followed by another "why" until you reach a systemic cause.

### ANPG Reporting Requirements

Angola operators must report to ANPG:
- All fatalities: Within 24 hours (immediate notification)
- LTI and serious injuries: Within 24 hours
- Significant hydrocarbon releases: Within 24 hours
- Near misses (high potential): Within 72 hours
- All incidents: Full investigation report within 30 days

ANPG may send inspectors to investigate serious incidents independently.

---

## Part 9: HSE KPIs and Performance Measurement

### Lagging Indicators (Things that already happened)

| KPI | Definition | Formula |
|-----|-----------|---------|
| **TRIR (Total Recordable Incident Rate)** | Recordable injuries per 200,000 work hours | $(LTI + RWC + MTC) \times 200,000 / \text{total hrs}$ |
| **LTIR (Lost Time Injury Rate)** | LTIs per 200,000 work hours | $LTI \times 200,000 / \text{total hrs}$ |
| **Fatality Rate** | Deaths per 100 million work hours | Rare but catastrophic benchmark |
| **Hydrocarbon Release Rate** | Unintentional HC releases per year | Tracked by severity category |

**Angola benchmark (industry target):** TRIR < 0.5 for IOC operators in Angola offshore. TotalEnergies Angola and Azule Energy publish annual sustainability reports with these numbers.

### Leading Indicators (Prevention-focused)

Leading indicators predict future incidents by measuring the safety of current activities:

| Leading KPI | What It Measures |
|------------|-----------------|
| **PTW compliance rate** | % of work done with valid permits |
| **Safety observation cards (SOC)** | Number of hazard observations submitted by crew |
| **Safety walkabouts completed** | % of planned management safety tours done |
| **Critical Lifesaving Rules compliance** | Violations of absolute rules (working at heights without harness, bypassing F&G systems) |
| **Near miss reporting rate** | Near misses reported per 200,000 hours — higher is GOOD (means people are reporting) |
| **Overdue corrective actions** | % of HAZOP, incident, and audit actions closed on time |

**Why leading indicators matter:** They allow you to intervene BEFORE the incident happens. A team that reports no near misses for 6 months is either very safe OR not reporting — the latter is dangerous.

---

## Part 10: Life-Saving Rules and Process Safety Essentials

### Life-Saving Rules (Angola Industry Standard)

Most Angola operators enforce a set of non-negotiable Life-Saving Rules (LSRs) — violations result in immediate dismissal and removal from the installation:

1. **Work with a valid Permit to Work:** No task without a valid permit for hazardous work
2. **Conduct gas tests before and during hot work:** Gas free confirmed before welding/grinding
3. **Verify isolation before work begins:** LOTO completed and verified before any maintenance
4. **Obtain authorized entry before entering a confined space:** Atmospheric test, standby man confirmed
5. **Wear your seatbelt:** In all vehicles/helicopters
6. **No alcohol or drugs:** Zero tolerance
7. **Work within the scope of the PTW:** Don't deviate from the permit scope without stopping and revising
8. **Never bypass a safety critical device:** No bypassing F&G detectors, ESD systems, relief valves
9. **Follow prescribed Journey Management when traveling by land:** Angola onshore security procedures
10. **Protect yourself from drops:** Never stand under a suspended load; all objects secured at height

### Process Safety: Major Accident Prevention

Beyond personal safety, offshore HSE engineers are responsible for preventing Major Accident Events (MAEs) — events that could kill multiple people simultaneously:

**The Bow-tie model for process safety:**
- **Prevention barriers** (left side): Relief valves set correctly, flanges torqued to spec, integrity inspection schedules met, ESDV function tested, PTW complied with.
- **Mitigation barriers** (right side): F&G detection operational, ESD system tested, deluge tested, TEMPSC available and maintained, crew trained in emergency response.

**Barrier health:** Angola operators use barrier health dashboards (digital tool) tracking the status of every critical safety barrier. A "degraded" barrier must be replaced by a compensatory measure and repaired immediately.

---

## Part 11: BOSIET and IWCF — Your Pre-Offshore Certifications

Before going offshore in Angola, you need:

### BOSIET (Basic Offshore Safety Induction and Emergency Training)

**Provider:** OPITO-approved training centers (ERT in Luanda, Falck Safety Services)
**Duration:** 3 days
**Cost:** $800–1,500 USD in Luanda
**Validity:** 4 years (then renewal FOET — Further Offshore Emergency Training)

**What you train:**
- Day 1: Fire fighting (live fire exercise), first aid, manual handling
- Day 2: Sea survival (jump into pool in survival suit, board life raft), HUET
- Day 3: Helicopter underwater escape training (HUET): Submerged inverted helicopter mockup — you escape in <30 seconds using HEBS kit

**Angola requirement:** BOSIET is mandatory for all offshore personnel per ANPG and all operator regulations. Without it, you cannot board a helicopter.

### IWCF (International Well Control Forum)

Required for anyone involved in drilling, completions, or workover operations. See [01_Well_Control_Tutorial.md](01_Well_Control_Tutorial.md) for exam content detail.

### Angola Medical Certificate

All offshore workers need an ANPG-compliant medical certificate confirming fitness for offshore work. Includes:
- Annual medical examination
- Vision and hearing tests
- Cardiovascular screening
- Respiratory function test

---

## Exercises — HSE Offshore

**Exercise 1: Risk Assessment**
A maintenance team on a Block 15 FPSO needs to replace a corroded flange on a 4" gas line within the HP separator module. The line is in service and cannot be fully depressurized (it serves gas lift). Identify:
1. At least 4 hazards associated with this task
2. The risk level (likelihood × severity) for each hazard before controls
3. A control measure for each hazard
4. What type of permit is required?

**Exercise 2: TRIR Calculation**
An Angola FPSO crew works 28/28 rotation. There are 200 crew on rotation at any time.
- In 2025: 3 Medical Treatment Cases, 1 Lost Time Injury, 0 fatalities
- Total man-hours worked in 2025 = 200 crew × 12 hours/day × 365 days = 876,000 hours

Calculate TRIR for 2025. Is this above or below the industry target of 0.5?

**Exercise 3: HAZOP Scenario**
A HAZOP study is reviewing the FPSO HP separator. The guide word "MORE" is applied to the parameter "Temperature" at the separator inlet.

1. What deviation does this generate?
2. What are the possible causes?
3. What are the consequences?
4. What existing safeguards would prevent/mitigate this?
5. What additional actions (if any) would you recommend?

**Exercise 4: Emergency Response Decision**
You are the Offshore Installation Manager (OIM) on a Block 32 FPSO. At 02:30, the gas detection system alarm sounds in the HP separator module. The PA system announces: "Gas detected, HP separator module, Level 1 alarm." Wind is 25 knots from the south. 180 people are aboard. What are your immediate actions and decision tree?

---

## Interview Questions — HSE Offshore

1. What is the ALARP principle and how do you demonstrate a risk is ALARP?
2. Walk me through the Permit to Work process for a confined space entry on an FPSO.
3. What is a HAZOP and at what stage(s) of a project is it performed?
4. What are the three things required to start a fire (fire triangle)? How does the FPSO fire suppression system address each?
5. What is the difference between a leading and lagging HSE indicator? Give an example of each relevant to Angola offshore.
6. What certifications must you have before your first Angola offshore trip, and what does each cover?
7. You witness a colleague bypassing a safety-critical valve interlock to speed up a process restart. What do you do?
8. What is the ESD system on an FPSO? Describe ESD-1, ESD-2, and Total Release.

---

*Next: [08_Formation_Evaluation_Tutorial.md](08_Formation_Evaluation_Tutorial.md) | Return to [00_INDEX.md](../00_INDEX.md)*
## Part 8: Incident Investigation (ICAM Method)

After any incident (or near-miss), a structured investigation determines the root causes.

**ICAM (Incident Cause Analysis Method):**

### Causal Chain

```
INCIDENT / CONSEQUENCE
        │
INDIVIDUAL / TEAM ACTIONS (What the person did or failed to do)
        │
TASK / ENVIRONMENTAL CONDITIONS (Why the action occurred — situational factors)
        │
ORGANIZATIONAL FACTORS (What systemic factors allowed this situation to exist)
        │
ABSENT / FAILED DEFENSES (What safeguards failed or were missing)
```

**Goal:** Identify organizational factors (systemic problems) — not to blame individuals. Most incidents trace to system failures, not individual negligence.

**Corrective actions:** Address each causal factor. Must be SMART (Specific, Measurable, Achievable, Relevant, Time-bound). Tracked in the action tracking system.

### Five Whys (Simple version for minor incidents)

Start with the consequence. Ask "why did this happen?" five times. Each answer becomes the next "why."

**Example:**
- Incident: Worker injured — slip on wet deck
- Why 1: Deck was wet with oil → Why 2: Small oil leak from flange → Why 3: Flange gasket had deteriorated → Why 4: Last inspection was 18 months ago → Why 5: Inspection schedule was not being followed
- **Root cause:** Inspection scheduling system failure (administrative/organizational)

---

## Part 9: Safety KPIs

These are the numbers HSE managers and operators track to measure safety performance:

| KPI | Definition | Formula | Industry Benchmark |
|---|---|---|---|
| **LTI** | Lost Time Injury | Any injury causing ≥1 shift of lost time | Count per year per installation |
| **LTIF** | Lost Time Injury Frequency | LTIs per million hours worked | Target < 0.5 |
| **TRIR** | Total Recordable Incident Rate | All recordable incidents per 200,000 man-hours | Target < 1.0 |
| **TRIF** | Total Recordable Injury Frequency | All recordable injuries per million hours | Target < 2.0 |
| **NMF** | Near-Miss Frequency | Near-miss reports per million hours | High is GOOD — means reporting culture is healthy |
| **PTW compliance** | % of work activities covered by valid permits | Audited/total jobs | Target > 98% |
| **Observation cards** | Safety observations raised per person per period | Count | Lagging/leading indicator |

**Lagging indicators** (LTI, TRIR): Measure past performance. Only go up when someone is hurt.
**Leading indicators** (near-miss frequency, observation card rate, audit scores): Measure the health of the safety system before incidents occur. Much more valuable for prediction.

---

## Part 10: NEBOSH IGC Study Reference

NEBOSH IGC (International General Certificate) is your primary HSE qualification for the offshore sector. It has two units:

**Unit IG1: Management of Health and Safety**
- Hazard identification, risk assessment, ALARP
- Health and safety law principles
- Incident investigation and causation theory
- Emergency planning and fire safety principles

**Unit IG2: Risk Assessment (Practical)**
- Conduct a workplace risk assessment on a real workplace
- Submit written report to NEBOSH examiner
- Must identify hazards, assess risks, propose controls

**Preparation:** 120 hours of study is recommended. Online courses available from:
- NEBOSH accredited providers: Red Oak Training, Astutis, Zoe Talent Solutions, British Safety Council
- Cost: approximately $400–1,200 USD depending on provider
- Pass rate: approximately 70%
- Validity: Does not expire (refresher recommended every 3–5 years)

---

## Part 11: Practice Exercises

**Exercise 1:** Write a full JSA for the following task: "Open and inspect a subsea pig receiver on a deepwater FPSO after a pig return from the export pipeline." The pig receiver contains residual pressure and the pig may carry crude oil contamination.

**Exercise 2:** Conduct a partial HAZOP on the following node: "Flow from a high-pressure (HP) separator to a low-pressure (LP) separator via a pressure control valve (PCV)." Apply the guide words NO, MORE, and LESS to the flow parameter. For each deviation, state: cause, consequence, safeguard, and recommended action.

**Exercise 3:** An LTI occurs on an FPSO — a rigger falls 2m from a platform ladder and breaks his wrist. Apply the ICAM method causal chain. What organizational factors might you expect to find?

**Exercise 4:** Your FPSO has the following statistics for this year (August year-to-date): 8 months, average 250 workers on board. 1 LTI (3 days lost), 4 recordable incidents (treated by medic, no lost time), 25 near-miss reports. Calculate LTIF and TRIR.

---

## Part 12: Study Resources

| Resource | Format | Notes |
|---|---|---|
| NEBOSH IGC study materials | PDF/Online | Your primary certification study |
| API RP 75 (free download) | PDF | SEMS for offshore — read once |
| "Introduction to Safety Management" — Stranks | Textbook | Good general safety management theory |
| SPE HSE papers: search "Angola FPSO HSE" | OnePetro | Real case studies |
| IOGP Life-Saving Rules | Free PDF | 9 rules that prevent the most fatal incidents — memorize them |
| OPITO BOSIET / HUET training materials | Training course | Your first offshore safety qualification |
| UK HSE website — Process Safety resources | Online/Free | Best free process safety reference globally |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/05_HSE_Path.md](../paths/05_HSE_Path.md)*  
*Where to learn: [NEBOSH online](https://www.nebosh.org.uk) | [OSHA free training](https://www.osha.gov/training) | BOSIET at PETROTEC Luanda | [Learning Resources](../../../docs/learning-resources.md)*
