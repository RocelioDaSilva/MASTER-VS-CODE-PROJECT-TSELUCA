# Skills Universe — The Complete Map of Every Skill, Every Path

> This file does one thing: maps every technical skill you will ever need for an offshore career to the paths that need it, the priority level for each path, and the order in which to learn them.
>
> Use this as your study planning document. Before you start studying a skill, check this map to confirm it's in your priority zone.

---

## How to Read This Map

**Priority levels:**
- **CORE** — You must know this to get the job. Interviewers will test it. It is a prerequisite for offshore work in your track.
- **HIGH** — You need this within 12 months of starting your first job. You should be studying it now.
- **MEDIUM** — You'll learn this on the job. Having exposure is valuable but not required to get hired.
- **LOW** — Specialist knowledge. Relevant to senior roles or specific sub-specializations.

---

## Master Skills Matrix

| Skill | Tutorial | Drilling | Production | Subsea | Reservoir | HSE | Completions |
|---|---|---|---|---|---|---|---|
| **Well Control** | [skills/01](skills/01_Well_Control_Tutorial.md) | CORE | HIGH | HIGH | MEDIUM | HIGH | CORE |
| **Drilling Fundamentals** | [skills/02](skills/02_Drilling_Fundamentals_Tutorial.md) | CORE | LOW | LOW | LOW | MEDIUM | HIGH |
| **FPSO Process Operations** | [skills/03](skills/03_FPSO_Operations_Tutorial.md) | LOW | CORE | MEDIUM | MEDIUM | CORE | LOW |
| **Subsea Systems & SURF** | [skills/04](skills/04_Subsea_Systems_Tutorial.md) | MEDIUM | MEDIUM | CORE | LOW | MEDIUM | MEDIUM |
| **Reservoir Engineering** | [skills/05](skills/05_Reservoir_Engineering_Tutorial.md) | MEDIUM | HIGH | LOW | CORE | LOW | MEDIUM |
| **Drilling Fluids (Mud Eng.)** | [skills/06](skills/06_Drilling_Fluids_Tutorial.md) | CORE | LOW | LOW | LOW | LOW | HIGH |
| **Offshore HSE Systems** | [skills/07](skills/07_HSE_Offshore_Tutorial.md) | CORE | CORE | CORE | MEDIUM | CORE | CORE |
| **Formation Evaluation** | [skills/08](skills/08_Formation_Evaluation_Tutorial.md) | HIGH | MEDIUM | LOW | CORE | LOW | HIGH |
| **Production Engineering** | [skills/09](skills/09_Production_Engineering_Tutorial.md) | LOW | CORE | LOW | HIGH | LOW | MEDIUM |
| **Completions & Intervention** | [skills/10](skills/10_Completions_Tutorial.md) | HIGH | MEDIUM | LOW | MEDIUM | LOW | CORE |

---

## Path-Specific Study Order

### Drilling Engineering — Your Study Sequence

Study these in order. Each builds on the previous.

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Offshore HSE Systems | You will not pass a safety induction without this. Study first. |
| 2 | Well Control | The single most safety-critical skill. IWCF Level 1 test requires this. |
| 3 | Drilling Fundamentals | Understand the system before you optimize it |
| 4 | Drilling Fluids | You will likely be a mud engineer trainee or directional drilling FE — both need this |
| 5 | Formation Evaluation | Needed to interpret MWD/LWD data in real time |
| 6 | Completions | Needed for casing design, cementing, and advanced drilling |

**Before your first offshore trip:** Skills 1, 2, 3 at CORE level
**Before your 6-month review:** Skills 4, 5 at HIGH level
**Before Year 3 on the job:** All skills in the drilling column

---

### Production / FPSO — Your Study Sequence

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Offshore HSE Systems | Offshore safety induction, process safety fundamentals |
| 2 | FPSO Process Operations | Core of your job — understand every unit operation on an FPSO |
| 3 | Production Engineering | Optimize individual wells and the overall production system |
| 4 | Reservoir Engineering | Understand what's underground to manage what's at surface |
| 5 | Well Control | You operate near wellheads and flowlines. Know the basics. |
| 6 | Subsea Systems | Understand what feeds your FPSO from below |

---

### Subsea Engineering — Your Study Sequence

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Offshore HSE Systems | Diving and ROV operations carry unique hazards |
| 2 | Subsea Systems & SURF | Core technical domain — learn this deeply |
| 3 | Well Control | Subsea trees and BOPs — you must understand well barriers |
| 4 | FPSO Process Operations | Understand the topside system your subsea infrastructure connects to |
| 5 | Reservoir Engineering | Understand flow assurance and production chemistry |

---

### Reservoir Engineering — Your Study Sequence

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Reservoir Engineering | Your entire job. Start here and go deep. |
| 2 | Formation Evaluation | Reservoir characterization depends on well log interpretation |
| 3 | Production Engineering | Production decline, nodal analysis, pressure management |
| 4 | Offshore HSE Systems | Required for any offshore visits |
| 5 | Well Control | For well testing and DST operations offshore |

---

### HSE Engineering — Your Study Sequence

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Offshore HSE Systems | This is your entire job domain. Master it. |
| 2 | FPSO Process Operations | You cannot identify process hazards without understanding the process |
| 3 | Well Control | BOPs, well barriers, blowout prevention are major HSE risks you must understand |
| 4 | Drilling Fundamentals | HSE on a drillship requires operational understanding |
| 5 | Subsea Systems | Hazards in diving, ROV, and subsea intervention operations |

---

### Completions Engineering — Your Study Sequence

| Priority | Skill | Why This Order |
|---|---|---|
| 1 | Well Control | You work with open holes and live wells. This is non-negotiable. |
| 2 | Offshore HSE Systems | Completions work involves high-pressure, high-risk activities |
| 3 | Completions & Intervention | Core technical domain |
| 4 | Drilling Fluids | Completion fluids (brines, acid) are a sub-specialty of mud engineering |
| 5 | Drilling Fundamentals | Understand the well you're completing |
| 6 | Formation Evaluation | To design perforations and select completion intervals |

---

## Universal Skills (Every Path Needs These)

These skills appear across all tracks. They are not "soft skills" — they are technical capabilities that every offshore engineer must have regardless of specialization.

### 1. Reading P&IDs (Process and Instrumentation Diagrams)

**What it is:** The standard engineering drawing language for piping, equipment, and control systems on an offshore installation. Every piece of equipment, every valve, every instrument, every pipe on the FPSO or rig has a P&ID representation.

**Why it matters:** You cannot troubleshoot a process problem, plan a workover, or perform a JSA without reading the P&ID. It is the map of the installation.

**How to learn it:**
- Download ISA standard P&ID symbol library (free online)
- Practice reading the FPSO P&ID in your company's technical documentation
- ISPTEC subject connection: Desenho Técnico covers the drawing conventions

### 2. Pressure-Temperature Relationships

**What it is:** Understanding how pressure and temperature change with depth in a wellbore and in a process system. This underpins well control, flow assurance, FPSO operations, and completions.

**Key equations you must know:**

Hydrostatic pressure:
$$P_{hyd} \text{ (psi)} = 0.052 \times \rho \text{ (ppg)} \times h \text{ (ft)}$$

$$P_{hyd} \text{ (bar)} = 0.0981 \times \rho \text{ (kg/L)} \times h \text{ (m)}$$

Geothermal gradient (typical Angola deepwater):
$$T(°C) = T_{seabed} + 0.025 \times \text{depth below seabed (m)}$$

Hydrate formation condition: at any combination of P and T below the hydrate equilibrium curve, natural gas + water = solid plugs.

### 3. Unit Conversions (Oilfield vs SI)

The offshore industry uses **oilfield units** (psi, ppg, bbl, ft, °F) alongside SI. You must be fluent in both and able to convert instantly.

| Quantity | Oilfield Unit | SI Unit | Conversion |
|---|---|---|---|
| Pressure | psi | bar | 1 bar = 14.504 psi |
| Mud weight | ppg (lb/gal) | kg/L (SG) | 1 ppg = 0.1198 kg/L |
| Flow rate | bbl/day | m³/day | 1 bbl = 0.159 m³ |
| Length | ft | m | 1 ft = 0.3048 m |
| Temperature | °F | °C | °C = (°F - 32) / 1.8 |
| Volume | bbl | m³ | 1 bbl = 0.158987 m³ |

### 4. Report Writing (Daily Drilling Reports / Shift Reports)

Every offshore discipline writes reports. The offshore industry runs on documentation. A drilling engineer writes DDRs (Daily Drilling Reports). A production engineer writes Daily Production Reports. An HSE officer writes incident reports and shift safety reports.

**The format:** Time-based account. Every 15 minutes of rig/installation time is accounted for, coded (drilling, tripping, waiting on weather, non-productive time). Losses are quantified.

**How to improve:** Read example DDRs (available on industry forums). Practice writing clear, concise technical narratives. Technical English is critical — most reports are written in English regardless of crew nationality.

### 5. Technical English

All offshore technical documentation, software interfaces, training materials, standards (API, ISO, NORSOK), and most inter-company communications are in English. Your ISPTEC English courses are a foundation. To reach technical offshore English proficiency:

- Read: Rigzone news (English), SPE technical papers, API standards preambles
- Write: Practice writing DDR-style summaries of what you did in lab exercises
- Study vocabulary: Know the difference between "casing", "liner", "tubing", "riser", "conductor"

### 6. Basic Data Analysis (Excel / Python)

Production engineers, reservoir engineers, and drilling engineers all use spreadsheets and increasingly Python to analyze data. You don't need to be a programmer. You do need to:
- Build engineering calculation spreadsheets in Excel
- Create production trend plots
- Basic statistical analysis: decline curves, correlation coefficients
- In Python: pandas for data reading, matplotlib for plotting, scipy for fitting

**ISPTEC connection:** Computação Científica I & II + Estatística Básica + Cálculo Numérico

---

## Skills Gap Assessment Tool

Rate yourself on each skill from 1–5:
- 1 = No knowledge
- 2 = Basic awareness (heard the terms)
- 3 = Conceptual understanding (can explain the concepts)
- 4 = Working knowledge (can solve problems, apply equations)
- 5 = Interview-ready (can explain to an interviewer, give examples from ISPTEC labs or projects)

A **CORE** skill needs to be at level 4–5 before your first job interview. A **HIGH** skill needs to reach level 3–4 within 6 months of starting work.

---

## Where to Learn Each Skill

Every skill tutorial in [skills/](skills/) covers what to learn. For *where* and *how*:

- **Central directory of courses, books, platforms, and providers:** [Learning Resources](../../docs/learning-resources.md)
- **Free online:** [learn.slb.com](https://learn.slb.com) (Petrel, Eclipse) · [PetroWiki](https://petrowiki.spe.org) · [Drillingformulas.com](https://drillingformulas.com) · [OnePetro](https://onepetro.org)
- **Angola in-person:** PETROTEC Luanda (BOSIET, IWCF) · Clínica Multiperfil (Offshore Medical) · ISPTEC SPE Chapter
- **Certifications with costs & providers:** [Certifications Angola](support/Certifications_Angola.md)
- **Free student software:** [Petrel/Eclipse](https://learn.slb.com) · [PROSPER/MBAL/GAP](https://www.petex.com/academic/) · [HYSYS](https://www.aspentech.com/en/university-program) · [AutoCAD](https://www.autodesk.com/education/edu-software)
- **Professional orgs:** [SPE](https://www.spe.org) ($25/yr student) · [IWCF](https://iwcf.org) · [NEBOSH](https://www.nebosh.org.uk) · [IMCA](https://www.imca-int.com)

---

*Previous: [02_Six_Paths_Decoded.md](02_Six_Paths_Decoded.md) | Next: [04_Year3_Launchpad.md](04_Year3_Launchpad.md)*
