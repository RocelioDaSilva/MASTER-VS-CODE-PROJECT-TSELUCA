# Skill Tutorial 04 — Subsea Systems

> **Applies to:** Subsea engineers (CORE), production engineers (HIGH), completions engineers (HIGH), all others (awareness)
> **ISPTEC connection:** Sistemas Marítimos de Produção, Engenharia de Poços, Mecânica dos Fluidos
> **Goal:** Understand the entire subsea production system: trees, manifolds, umbilicals, flowlines, risers, ROV operations, and flow assurance. Able to discuss Angola deepwater infrastructure in a technical interview.

---

## Part 1: Angola's Subsea Scale — Context First

Angola's deepwater production relies entirely on subsea infrastructure. There are no fixed platforms — the water is too deep (500–2,500m). Everything happens on the seabed.

**Angola's subsea inventory (approximate):**

| Block | Operator | Water Depth | Subsea Wells | FPSOs |
|---|---|---|---|---|
| Block 15 | Azule Energy (ex-Esso) | 800–1,800m | 50+ | Kizomba A, B, C |
| Block 17 | TotalEnergies | 800–2,000m | 70+ | Girassol, Dalia, Pazflor, CLOV |
| Block 32 | TotalEnergies | 1,400–1,700m | 30+ | Kaombo Norte, Kaombo Sul |
| Block 31 | BP/Azule | 1,800–2,400m | 20+ | PSVM |
| Block 0 | Chevron | 50–150m | Shallow — less subsea | Various platforms |

Every one of these wells has a subsea tree, connected to a manifold, connected by flowlines and risers to an FPSO, with umbilicals supplying control signals and chemicals.

---

## Part 2: The Subsea Tree (X-mas Tree)

The subsea tree is the valve assembly installed on top of the wellhead at the seabed. It controls flow from the well and provides the barriers required by well integrity regulations.

### Horizontal vs Vertical Tree

**Vertical Subsea Tree (VST) — Legacy design:**
```
Well Bore
    │
Wellhead
    │
Casing Hanger + Tubing Hanger (inside the tree)
    │
Master Valve (manual/hydraulic) — primary production valve
    │
Wing Valve — connects to flowline
    │
Swab Valve — for wireline access
    │
Production Choke
    │
Crossover Valve (to annulus access)
```
- Production casing is suspended inside the tree body
- To access the wellbore with wireline, you must pull the tree (expensive, time-consuming)

**Horizontal Subsea Tree (HST) — Current standard:**
- The tree body is a horizontal assembly flanged to the side of the wellhead
- The tubing hanger sits in the wellhead bore above the casing hangers
- Wireline access is straight down through the tree bore — much easier
- Preferred for Angola deepwater wells where well interventions are planned

### Key Tree Components and Functions

| Component | Function |
|---|---|
| **Production Master Valve (PMV)** | Main on/off for production flow. Failsafe closed (springs shut if hydraulic pressure lost). |
| **Production Wing Valve (PWV)** | On/off valve between tree and flowline. Failsafe closed. |
| **Annulus Master Valve (AMV)** | Provides access to the casing annulus. Allows annulus pressure monitoring. |
| **Production Choke** | Controls flow rate from the well. Sized to manage production and maintain wellhead pressure. |
| **Subsurface Safety Valve (SCSSV)** | Located in the tubing string ~50–100m below seabed. Failsafe closed. Second barrier below the tree. |
| **Chemical Injection Valve** | Point where scale/corrosion/hydrate inhibitor is injected into the wellstream |
| **Hydraulic Actuators** | Open/close valves by hydraulic pressure from the umbilical |
| **Tree Cap / Intervention Riser** | Provides ROV and wireline access port |

---

## Part 3: Subsea Manifolds

A manifold is a piping distribution hub on the seabed. Instead of running a separate flowline from every well to the FPSO, you connect all nearby wells to a manifold and run 2–4 flowlines (production headers) to the FPSO.

**Benefits:**
- Fewer risers to the FPSO (reduces cost and riser loads)
- Commingled production from multiple wells
- Ability to route individual wells to test separator on FPSO
- Gas lift distribution from the FPSO to multiple wells

**Manifold structure:**
- **Production headers:** Typically 2 (dual-production design) so you can segregate well groups or use one for pigging
- **Test header:** Allows any single well to be routed to the FPSO test separator for individual well rate measurement
- **Gas lift header:** Distributes compressed gas lift from the FPSO to individual wells
- **Chemical injection header:** Distributes chemicals from FPSO

**PLEM / PLET:**
Pipeline End Manifolds (PLEMs) and Pipeline End Terminations (PLETs) are the connecting structures at the ends of flowlines/pipelines where they connect to the manifold or to the FPSO riser base.

---

## Part 4: Umbilicals

An umbilical is a bundle that runs from the FPSO to the seabed manifold/trees. It carries everything needed to control and supply the subsea system:

### Umbilical Layers (inside to outside, for a typical Angola umbilical)

```
[Center filler/core]
  ├── Hydraulic tubes (HP service: 250–350 bar, ½" to ¾" OD)
  │     Used for: valve actuation (open/close tree valves)
  ├── Hydraulic tubes (LP service: 100–200 bar)
  │     Used for: secondary actuator functions
  ├── Chemical injection tubes (¼" to ½" OD)
  │     Used for: MEG, scale inhibitor, corrosion inhibitor, asphaltene inhibitor lines
  ├── Electrical cables (power)
  │     Used for: instrument power (sensors, SCM electronics)
  ├── Electrical cables (signal)
  │     Used for: sensor data transmission to FPSO (older systems)
  ├── Fiber optic cables
  │     Used for: high-bandwidth data transmission (modern systems), distributed temperature sensing (DTS)
  └── [Outer armoring — steel wire braiding for strength and protection]
```

**Subsea Control Module (SCM):** Each subsea tree has an SCM mounted directly on the tree. The SCM receives hydraulic pressure and electrical/fiber signals from the umbilical and translates them into valve actuations. From the FPSO control room, an operator clicking "close PMV Well-14" sends a hydraulic command down the umbilical to the Well-14 SCM, which closes the valve.

**Umbilical termination assembly (UTA):** The subsea end of the umbilical, connected to the manifold. Distributes individual tubes to each tree via a "flying lead" (short jumper umbilical from manifold UTA to tree).

---

## Part 5: Flexible Pipes and Risers

### Flexible Pipe Construction

Flexible pipe (flowlines and risers) used in Angola's FPSOs is an unbonded flexible pipe — multiple layers that slide relative to each other, allowing the pipe to flex:

**Layer by layer (outside to inside):**

```
1. External plastic sheath (HDPE/PA) — corrosion/mechanical protection
2. Outer wire armor (helical high-tensile steel wires) — tension resistance
3. Anti-wear layer (PA/HDPE tape) — reduces friction between armor layers
4. Inner wire armor (helical steel wires) — tension and compression resistance
5. Intermediate plastic sheath — pressure isolation
6. Pressure armor (interlocked steel profile) — resists radial pressure load (collapse/burst)
7. Internal plastic liner (PVDF/HDPE/PA) — fluid-tight barrier against internal fluid
8. Carcass (interlocked steel profile) — collapse resistance in inner bore; prevents liner collapse
```

**Key advantage:** Can absorb large motions from FPSO heave, surge, and sway without fatigue failure. Essential for risers on floating FPSOs.

**Length:** Individual flexible pipe lengths = 3–5 km each. An Angola FPSO may have 20–40 flexible risers and flowlines.

### Riser Configurations

A **riser** is the pipe that connects the seabed to the FPSO. It must handle the FPSO's motions while maintaining flow.

**Lazy Wave Riser (most common in Angola):**
```
FPSO
  │ (risers hang off FPSO turret/riser balcony)
  │ \
  │  \ (catenary section)
  │   \
  │    [buoyancy section — foam modules clamped to pipe]
  │   /
  │  / (lazy wave — the "S" curve)
  │ /
  seabed TDZ (Touch Down Zone)
  │
  horizontal flowline to manifold
```
The buoyancy modules create an "S" or wave shape in the riser. This decouples FPSO motion from the pipe at the seabed touch-down zone, reducing fatigue loads. Critical in Angola's deepwater.

**Steel Catenary Riser (SCR):** Simple catenary shape. Used when water is deep enough that the horizontal length provides natural decoupling. Less expensive than lazy wave but higher fatigue loads near the touchdown zone.

**Free Hanging (vertical):** Only for relatively still floaters; not common in Angola due to FPSO motions.

---

## Part 6: Flow Assurance — Keeping the Flow Flowing

Flow assurance is the engineering discipline that ensures hydrocarbons flow continuously from reservoir to surface without plugging, blocking, or losing pressure. The threats in Angola deepwater:

### Hydrates

**What they are:** Ice-like crystals (clathrates) formed when gas molecules are trapped inside a lattice of water molecules. Form at low temperatures and high pressures — exactly the conditions in Angola's deepwater flowlines.

**Hydrate curve (equilibrium curve):** A line on a P-T diagram separating "hydrate region" (left/below) from "no-hydrate region." Angola deepwater flowlines spend a lot of time in the hydrate region during shutdown and cool-down.

**Prevention methods:**
1. **MEG injection:** Monoethylene glycol — depresses the hydrate formation temperature. Injected continuously at the wellhead.
2. **MeOH injection:** Methanol — emergency hydrate inhibitor, faster-acting but more expensive at continuous injection
3. **Insulation:** Pipe-in-pipe (PIP) flowlines with insulation layer maintain fluid temperature above the hydrate curve during production
4. **Depressurization:** During planned shutdowns, blow down the flowlines to reduce pressure below hydrate stability
5. **Heating:** Some critical flowlines have electrical heat tracing

**Hydrate remediation:** If a hydrate plug forms: locate it, depressurize from both sides, inject MeOH to dissolve the plug. Can take days or weeks. Severe plugs can rupture the pipe.

### Scale

**What it is:** Inorganic mineral deposits (calcium carbonate, barium sulfate, strontium sulfate) that precipitate when formation water chemistry changes under pressure/temperature conditions in the production system.

**Prevention:** Scale inhibitor injection at the wellhead (continuous) or squeeze treatment (pumped down the tubing, absorbed into rock, slowly released into the production stream).

### Wax (Paraffin)

**What it is:** Heavy alkane molecules (C18–C60) that are dissolved in oil at reservoir temperature. As oil cools in the flowline, wax crystallizes and deposits on the pipe wall.

**Wax Appearance Temperature (WAT):** Temperature at which wax first crystallizes. Angola crude WAT typically 20–40°C — well within seabed flowline temperatures.

**Prevention:** Wax inhibitor injection. Regular pigging (see below). Pour point depressant chemicals.

### Asphaltenes

**What they are:** High molecular weight aromatic compounds that can precipitate from crude oil when pressure drops (especially near or in the wellbore) or when mixing with incompatible fluids.

**Prevention:** Asphaltene inhibitor injection at the wellhead. Very difficult to remediate once deposited.

---

## Part 7: ROV Operations in Angola Deepwater

**What is an ROV?**
A Remotely Operated Vehicle (ROV) is an underwater robot deployed from the surface vessel (FPSO, drillship, or DSV — Dive Support Vessel) to perform tasks at the seabed. In 1,500m water depth — beyond any human diver — ROVs are the only way to interact physically with subsea equipment.

**ROV types used in Angola:**

| Type | Description | Use |
|------|-------------|-----|
| **Work-class ROV (heavy)** | 3,000–4,000m rated. High power (100–200 HP). Multiple manipulator arms. | Valve operations, tree connections, jumper installation, inspection |
| **Observation ROV** | Small, lower-power. Visual inspection only. | Pre-installation surveys, visual inspection of structure/coatings |
| **Electric-work ROV** | Compact but capable. Some valve operation capability. | Smaller tasks, umbilical connections |

**What ROVs do on Angola FPSOs:**
1. **Routine inspection:** Inspect tree, manifold, riser bases, flexible pipe, corrosion coatings. Cathodic protection potential readings. CCTV recording.
2. **Valve intervention:** Open or close a valve that the control system cannot operate (SCM failure, control line rupture). Using hydraulic torque tools on the ROV manipulator arm.
3. **Flying lead connections:** Connect the short umbilical jumpers between the manifold UTA and the tree (during installation and replacement).
4. **Flowline connection:** Stab and lock flowline end connections (PLETs) using ROV-deployed tooling.
5. **Debris removal:** Clear debris from subsea equipment (fishing lines, dropped tools, biological growth).
6. **Well intervention support:** Monitor PLEM/PLET connections during wireline or coiled tubing work. Support workover riser running operations.

### ROV Operations on Your FPSO Rotation

As a production or completions engineer, you will:
- Brief the ROV supervisor on the task (valve number, target position, P&ID reference)
- Monitor the ROV feed in the control room (ROV cameras stream live video to the FPSO control room)
- Sign off on the ROV task completion report
- Notify ANPG if an emergency subsea intervention was performed

---

## Part 8: Subsea Control and Communication

### Multiplexed Electrohydraulic (MUX) Control System

The current standard in Angola deepwater. How it works:

```
FPSO CONTROL ROOM
  ├── Master Control Station (MCS) — computer workstation for subsea control
  ├── Hydraulic Power Unit (HPU) — pressurizes hydraulic fluid to 250-350 bar
  └── Electrical Power Supply Unit (EPSU) — powers instruments
         │ (umbilical carries: hydraulic, electrical, fiber optic)
         ▼
UMBILICAL TERMINATION ASSEMBLY (UTA) at manifold
         │ (flying leads to each tree)
         ▼
SUBSEA CONTROL MODULE (SCM) on each tree
  ├── Receives hydraulic pressure (actuates valves)
  ├── Receives electrical/fiber commands (logic processing)
  ├── Transmits sensor data upward (pressure gauges, temperature sensors, position sensors)
  └── Local battery backup (for safety functions if comms lost)
```

**What the MCS operator can do from the FPSO control room:**
- Open/close individual well valves (PMV, PWV, AMV, choke)
- Monitor downhole pressure and temperature gauges (downhole permanent sensors)
- Monitor tree pressures and temperatures
- Initiate ESD actions (close all wells in a defined sequence)

**All-Electric Subsea (future):** Next generation eliminates hydraulic umbilical tubes. All actuators are electric. Angola's Block 48 and future deep pre-salt developments are candidates. TotalEnergies and Aker BP are developing this technology. Fewer hydraulic failures, faster response, reduced umbilical weight and cost.

---

## Part 9: Pigging and Pipeline Inspection

### Pigging in the Subsea Context

Angola's subsea flowlines (typically 10"–16" OD, 10–30 km long) must be pigged regularly. The subsea system includes:

- **Subsea pig launcher (at the PLEM/manifold):** In some configurations, pigs are launched from a launching station at the manifold — driven by injection fluid (sea water or oil).
- **FPSO pig receiver:** The pig arrives at the FPSO pig receiver on the riser base.

**Wax pigging program for Block 17 example:**
- Wax buildup rate: ~1–3 mm/month at seabed temperatures
- Pigging frequency: Monthly to quarterly depending on wax severity
- Pigging monitoring: Pig tracking beacons clamped to the pig, acoustic sensors detect pig passage at PLEM, manifold, and riser TDZ.

### In-Line Inspection (ILI)

For monitoring pipeline wall integrity (corrosion, erosion, mechanical damage):

**MFL (Magnetic Flux Leakage) pig:** A strong magnet magnetizes the pipeline wall. Wall loss (corrosion) creates a flux leakage that sensors detect and locate.

**UT (Ultrasonic Testing) pig:** Ultrasonic sensors measure wall thickness directly. Higher resolution than MFL.

**Output:** A detailed report showing every area of wall loss > 10% wall thickness, dimensioned and located. The integrity engineer uses this to:
- Update the corrosion rate model
- Calculate safe operating pressure
- Schedule repairs or replacements

**ANPG requirement:** Angola operators must maintain Pipeline Integrity Management Plans (PIMPs) and submit inspection data to ANPG.

---

## Part 10: Subsea Intervention and Workover

### Why Subsea Workover?

Over time, subsea wells need intervention:
- **Scale or wax plugging the completion**
- **Sand accumulation in the wellbore**
- **Changing the gas lift valve depth** (as reservoir pressure declines, the optimum injection depth changes)
- **Replacing a failed DHSV**
- **Acidizing for damage removal**
- **Full well re-completion** (replace sand screen, change tubing)

### Light Well Intervention (LWI)

For smaller operations (chemical treatments, slickline/coiled tubing, gauge retrieval):

- **Subsea LWI vessel:** A surface vessel with a wire or coil deployed through a seabed lubricator that is flanged onto the tree cap.
- **Cost:** $50,000–$150,000/day for an LWI vessel — expensive but much cheaper than a full workover rig.
- **Limitation:** Cannot pull the tubing string or perform major completions changes.

### Full Workover (Drilling Rig)

For major well operations (tubing pull, re-completion, sidetracks):
- **Workover riser deployed from the drillship:** The drillship sets up over the well, runs a large-diameter workover riser to the tree, and the well can be worked just like during drilling.
- **Cost:** $200,000–$500,000/day for a drillship — Angola's deep wells demand this for major interventions.
- **Decision trigger:** When LWI cannot achieve the objective and the expected production increase justifies the rig cost.

---

## Exercises — Subsea Systems

**Exercise 1: Manifold Configuration**
An Angola development has 12 producing wells arranged around two 6-slot manifolds. Each manifold has a dual-production header (two production flowlines to the FPSO) and one test header. Draw a schematic showing how the wells connect to manifolds, manifolds to the FPSO.

**Exercise 2: Hydrate Risk Assessment**
A Block 17 flowline operates at 180 bar and 8°C at the seabed. The hydrate formation temperature for this fluid at 180 bar is 24°C. Is this flowline inside or outside the hydrate stability zone? If the flowline temperature drops to 5°C after a 6-hour production shutdown, what happens and what must the production team do?

**Exercise 3: Umbilical Capacity**
A new Angola development will have 10 wells connected to a central manifold 18 km from the FPSO. Each tree requires:
- 2 HP hydraulic tubes (for PMV and PWV)
- 1 LP hydraulic tube (for choke and secondary functions)
- 4 chemical injection lines (MEG, scale inhibitor, corrosion inhibitor, asphaltene inhibitor)
- 2 signal cables
- 1 fiber optic cable

The wells share the manifold-to-FPSO umbilical. The individual trees need dedicated flying leads. How many tube/cable counts are needed in the manifold-to-FPSO umbilical? (Assume some functions are shared on the manifold.)

**Exercise 4: ROV Task Sequence**
A well's PMV (Production Master Valve) has failed hydraulically open (control system reads "open" but physical position is uncertain). An ROV must verify and manually close the PMV override. List the steps the ROV supervisor and production engineer would follow. What safety considerations apply?

---

## Interview Questions — Subsea Systems

1. What is the difference between a vertical subsea tree and a horizontal subsea tree? Why are horizontal trees preferred for Angola deepwater completions?
2. What are the four main flow assurance threats in Angola deepwater and how is each managed?
3. How does a Subsea Control Module (SCM) work and what happens if it fails?
4. What is a lazy-wave riser and why is it superior to a simple catenary riser for Angola FPSOs?
5. An Angola flowline has been shut in for 12 hours due to FPSO maintenance. Outline the restart procedure and the main risk during restart.
6. What is the role of MEG (monoethylene glycol) in Angola deepwater operations? How is it recovered and recycled?
7. Explain the difference between a PLEM and a manifold. When would you use one versus the other?
8. A well's SCM has failed and the production wing valve is stuck closed. The well is offline. What are your options for intervening?

---

*Next: [05_Reservoir_Engineering_Tutorial.md](05_Reservoir_Engineering_Tutorial.md) | See also: [10_Completions_Tutorial.md](10_Completions_Tutorial.md)*

---

## Part 7: Pipeline Pigging

**Pigging** = running a device ("pig") through the pipeline/flowline for inspection, cleaning, or measurement.

**Types of pigs:**
- **Gauge pig:** Checks ID of the pipeline — confirms no restrictions or deformations
- **Cleaning pig:** Foam or wire brush pig removes wax, scale, and debris deposits
- **Smart pig (ILI — In-Line Inspection):** Equipped with sensors (magnetic flux leakage, ultrasound) to detect corrosion, metal loss, dents, cracks in the pipe wall

**Pipeline Integrity Management:** All Angola deepwater flowlines and export pipelines are subject to regular smart pigging programs to ensure they remain fit for service.

---

## Part 8: ROV Operations

**ROV (Remotely Operated Vehicle):** Unmanned underwater vehicle tethered to the surface vessel, controlled by pilots in the control van. Angola deepwater subsea work is done almost entirely by ROVs.

**Work classes:**

| Class | Capability | Depth Rating |
|---|---|---|
| **Observation ROV** | Camera, lights only — no manipulation | Up to 1,000m |
| **Work-Class ROV (WROV)** | 7-function manipulators, tool skids, up to 200+ HP | Up to 4,000m |
| **Drill Support ROV** | Attached to drillship, real-time BOP support and inspection | To drillship's rated depth |

**Typical ROV tasks in Angola:**
- Valve actuations on subsea trees (when SCM fails)
- Flying lead (umbilical jumper) connection and disconnection
- Subsea structure inspection (visual, torque tool)
- Pipeline tie-in operations with connection tools
- PLET/PLEM installation assistance
- BOP inspection during drilling operations
- Lost equipment recovery

**Tooling skids:** A WROV can change its tool configuration rapidly. Torque tool, hot stab (hydraulic connection), electrical/optical connector, cutting tool, and cleaning brushes are all available.

---

## Part 9: Subsea Installation Methods

Understanding how subsea infrastructure is installed helps you understand why certain design decisions are made.

| Method | Used For | Angola Examples |
|---|---|---|
| **J-Lay** | Deepwater rigid pipelines, SCRs. Pipe is assembled vertically and paid out at near-vertical angle. Lowest tension needed. | Deep rigid flowlines |
| **S-Lay** | Shallow to mid-depth rigid pipelines. Pipe is assembled horizontally, then curves in S-shape over the stinger. | Block 0 shallow lines |
| **Reel-Lay** | Small to medium flexible or rigid pipes prefabricated and spooled on a large reel, then unreeled at the seabed. Fast installation. | Umbilicals, flexible flowlines, small rigid lines |
| **MODU or Crane Vessel** | Lifting and placing manifolds, PLEMs, trees, pipeline end structures | All subsea structures |

**PAENAL and Sonamet** (based in Angola) fabricate subsea structures for installation by vessel campaigns.

---

## Part 10: Interview Questions and Study Resources

### Common Interview Questions

1. What is the difference between a vertical and horizontal subsea tree? When would you use each?
2. Explain the function of each layer in an unbonded flexible pipe.
3. What is a lazy wave riser? Why is it preferred in Angola deepwater?
4. Describe the hydrate formation mechanism and the four methods to prevent it.
5. What is MEG regeneration and why is it economically important on an FPSO?
6. A well's flow suddenly stops. The ROV observes ice-like material near the tree valve. What is your diagnosis and procedure?
7. What is an umbilical and what types of conduits does it contain?
8. Explain cathodic protection on subsea pipelines. Why is it necessary?
9. What is the purpose of pigging a subsea flowline?
10. What is a flying lead? When is it replaced?

### Study Resources

| Resource | Format | Notes |
|---|---|---|
| "Subsea Engineering Handbook" — Yong Bai | Textbook | Comprehensive subsea design reference |
| "Flow Assurance in Subsea Pipelines" — SPE workshop notes | PDF | Deepwater flow assurance specifics |
| TechnipFMC / OneSubsea engineering brochures | Free online | Technical descriptions of real systems used in Angola |
| Oceaneering ROV operations videos | YouTube | Real deepwater ROV work |
| IFPEN (Institut Français du Pétrole) online courses | Online/free | Flexible pipe and riser courses |
| SPE student papers on Angola Block 17/32 | OnePetro | Case studies of real Angola subsea infrastructure |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [paths/03_Subsea_Path.md](../paths/03_Subsea_Path.md)*  
*Where to learn: [PetroWiki](https://petrowiki.spe.org/Subsea_engineering) | [IMCA](https://www.imca-int.com) | [Learning Resources](../../../docs/learning-resources.md)*
