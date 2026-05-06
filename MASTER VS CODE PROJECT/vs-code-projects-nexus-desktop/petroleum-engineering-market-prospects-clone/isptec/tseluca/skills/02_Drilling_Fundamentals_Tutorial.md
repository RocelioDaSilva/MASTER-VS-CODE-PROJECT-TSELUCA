# Skill Tutorial 02 — Drilling Fundamentals

> **Applies to:** Drilling engineers (CORE), Completions engineers (HIGH), all tracks (awareness)
> **ISPTEC connection:** Engenharia de Poços, Mecânica das Rochas, Geometria e Trajetória de Poços
> **Goal:** Understand the complete well construction process, rig components, drill string, BHA, casing design, and cementing well enough to discuss them in a technical interview and understand what you see on your first rig trip.

---

## Part 1: The Well Construction Sequence

Drilling a well is a structured process. Every well drilled in Angola deepwater goes through the same sequence. Know this cold.

```
1. SPUD                   → Rig positioned. Conductor hole pre-drilled (36" or 30" hole)
2. CONDUCTOR CASING       → 30" or 24" casing set 100–200m BML (below mudline)
3. SURFACE HOLE           → Drill to ~1,500m. 17½" or 20" hole
4. SURFACE CASING         → 13⅜" casing set. Cement to surface.
5. INTERMEDIATE HOLE      → Drill to ~3,000m. 12¼" hole. Through pressure transitions.
6. INTERMEDIATE CASING    → 9⅝" casing set. Cement to above shoe.
7. PRODUCTION HOLE        → Drill to TD (total depth). 8½" or 6" hole. Into reservoir.
8. PRODUCTION CASING/LINER → 7" liner or 9⅝" casing set across reservoir.
9. CEMENTING              → Primary cement job seals annulus.
10. LOGGING               → Run wireline logs or LWD for formation evaluation.
11. COMPLETION            → Install production tubing, packer, DHSV (completions team).
12. HANDOVER TO PRODUCTION → Well on production.
```

Each step is a hole section. Each hole section uses a smaller bit than the previous one (telescoping design) to allow casing to pass through the previous casing.

---

## Part 2: The Drilling Rig — Components You Must Know

### Rig Types in Angola

| Rig Type | Used For | Angola Examples |
|---|---|---|
| **Drillship** | Ultra-deepwater (>500m) | Valaris DS-7/9 on Block 17/32 |
| **Semi-submersible** | Mid-deepwater (300–1,500m) | Less common in Angola recently |
| **Jackup** | Shallow water (<150m) | Block 0 (Cabinda offshore) |
| **Land rig** | Onshore | Cabinda onshore (minor) |

### Key Rig Systems

**Hoisting System:** Lifts and lowers the drill string. Components:
- **Derrick:** The tall steel structure. Height = maximum drill string length + clearance (~50m for deepwater rigs)
- **Crown Block:** Fixed pulley system at top of derrick
- **Traveling Block:** Movable pulley below crown block. Drill string hangs from this.
- **Hook:** What the top drive/swivel hangs from
- **Drawworks:** The winch that controls the drilling line

**Rotating System:** Turns the drill bit. Modern rigs use:
- **Top Drive:** Motorized unit that hangs from the traveling block and rotates the drill string. Replaces the older rotary table + kelly system.
- **Rotary Table (legacy):** Rotates the kelly bushing and thus the drill string via a square kelly bar

**Circulating System:** Pumps drilling mud down the drill string and back up the annulus:
- **Mud Pumps:** High-pressure piston pumps (triplex pumps). Typically 2–3 on a drillship. 2,000+ HP each.
- **Stand Pipe:** Rigid high-pressure pipe on the derrick that connects mud pumps to the hose
- **Rotary Hose (Kelly Hose):** Flexible high-pressure hose from stand pipe to top drive
- **Drill String:** The tubular conduit for mud down to the bit
- **Mud Pits:** Large tanks holding the active drilling fluid (800–2,000+ barrel capacity on deepwater rigs)
- **Shale Shakers:** Vibrating screens on the return flowline. Remove drill cuttings from the mud.
- **Desander, Desilter, Centrifuge:** Further solids control equipment

**Blow Out Preventer (BOP):** See [01_Well_Control_Tutorial.md](01_Well_Control_Tutorial.md)

---

## Part 3: The Drill String

The drill string is the tubular assembly that connects the surface (top drive on the rig floor) to the drill bit on the bottom. It serves three purposes:
1. **Transmit rotation** from top drive to bit
2. **Transmit mud pressure** (pump fluid down to the bit, returns up the annulus)
3. **Transmit weight on bit (WOB)** (through the heavy bottom hole assembly)

### Drill String Components (top to bottom)

**Drill Pipe (DP):**
- The bulk of the string. Typically 27–30 ft (9m) joints.
- Sizes: 5", 5½", 5⅞" OD (most common in Angola deepwater)
- Made of high-strength steel (Grade E, S135, V150 for high-strength applications)
- Has male (pin) and female (box) threaded connections called **tool joints**
- Stands: 3 joints connected = one "stand" (~90 ft / 27m) stored in the derrick racking board

**Heavy Weight Drill Pipe (HWDP):**
- Thicker-walled than regular DP
- Transition between drill pipe and drill collars
- Provides stiffness and additional weight
- Used to control dogleg severity in directional wells

**Drill Collars (DC):**
- Massive thick-walled steel pipe (up to 9" OD, 2.5"–3" ID)
- Very heavy. Provide the weight on bit.
- Placed at the bottom of the string, just above the bit
- In deviated wells: fewer drill collars used; WOB provided by other means

**Stabilizers:**
- Blades on the OD that contact the borehole wall
- Control wellbore trajectory (keep the bit on course or build/drop angle)

---

## Part 4: The Bottom Hole Assembly (BHA)

The BHA is the bottom section of the drill string. It contains the bit and all the tools required for the specific drilling objective. A typical deepwater directional BHA:

```
Drill Bit
  └── PDC Bit (Polycrystalline Diamond Compact) — 8½" for reservoir section
Rotary Steerable System (RSS) or Downhole Motor
  └── Controls trajectory while rotating
MWD Tool (Measurement While Drilling)
  └── Measures: inclination, azimuth, tool face, downhole WOB and torque
LWD Tools (Logging While Drilling)
  └── Measures: gamma ray, resistivity, porosity, density — formation evaluation while drilling
HWDP (Heavy Weight Drill Pipe)
  └── Transition, provides stiffness
Drill Collars
  └── Weight source
```

### Bit Types

**PDC Bit (Polycrystalline Diamond Compact):**
- Dominant in Angola deepwater reservoir sections (soft to medium rock)
- Fixed cutters — no moving parts
- Very high ROP in soft formations
- Sensitive to formation hardness changes and vibration

**Tricone (Roller Cone) Bit:**
- Three cones with steel/tungsten carbide teeth
- Used in harder formations or where PDC bits underperform
- Less common in deepwater but still used for surface hole

---

## Part 5: Directional Drilling

Almost no well drilled in Angola is vertical. The wells are directional — they start vertical, build an angle, and land in the reservoir at a specific location sometimes 2–4 km from the wellhead.

**Why directional drilling:**
- Reach multiple reservoir targets from a single wellhead
- Maximize reservoir contact (horizontal wells)
- Avoid surface obstructions (in shallow water: platforms)
- Optimize subsea infrastructure (wells cluster around a manifold)

### Well Profile Components

```
Vertical Section: Drilling straight down to the kick-off point (KOP)
  │
KOP (Kick-Off Point): Where directional drilling begins
  │
Build Section: Angle increases from 0° to target inclination (e.g., 0° → 45°)
  │            Build rate: degrees per 100 ft drilled (typically 2–5°/100ft)
  │
Tangent Section: Drilling at a constant angle and azimuth toward the reservoir
  │
Drop Section (sometimes): Reducing angle for horizontal entry or wellbore completion
  │
Landing Point → Enter the reservoir at target inclination and azimuth
```

**Inclination:** The angle from vertical (0° = vertical, 90° = horizontal)

**Azimuth:** The compass direction of the wellbore (0° = North, 90° = East, 180° = South, 270° = West)

**Dogleg Severity (DLS):** Rate of change of inclination AND azimuth per 30m or 100ft. Expressed in °/30m. High DLS causes torque, drag, and fatigue problems.

### Tools for Directional Control

**Rotary Steerable System (RSS):**
- The modern preferred method
- Continuously steers the bit while rotating the entire drill string
- More consistent trajectory control than motors
- Better for long horizontal sections

**Downhole Motor (PDM — Positive Displacement Motor):**
- Uses drilling fluid to power a downhole motor that turns the bit while the drill string is stationary (sliding)
- Less efficient but simpler and cheaper
- Used in combination with RSS or alone for shorter directional sections

---

## Part 6: Casing Design Principles

Casing is the permanent steel pipe cemented in the wellbore to:
1. Prevent wellbore collapse
2. Isolate different pressure zones
3. Allow BOP installation at each casing shoe
4. Enable progressive deepening of the well (telescoping design)

### Casing Grades and Connections

Casing is specified by:
- **OD:** 30", 20", 13⅜", 9⅝", 7", 5½", 4½" (from largest to smallest)
- **Weight:** lb/ft (heavier = thicker wall)
- **Grade:** H40, K55, N80, L80, P110, Q125 (higher number = higher yield strength)
- **Connection:** Buttress, Premium Connection (VAM, Tenaris, etc.)

### Design Criteria

A casing must be checked against three load cases:
1. **Collapse:** External pressure trying to crush the casing (when drilling below, you have fluid outside and less inside) — *most critical when you drain the casing accidentally*
2. **Burst:** Internal pressure trying to burst the casing outward (during a kick, well testing, cementing) — *most critical during a well control event*
3. **Axial (tension):** The weight of the casing hanging in the hole — *most critical at the top of the casing string*

**Design factors:** Safety margin applied on each criterion. Typically 1.1–1.25× the calculated maximum load.

---

## Part 7: Primary Cementing

After a casing string is run to depth, it is cemented into place. Cementing achieves:
1. **Zonal isolation:** Prevents fluid communication between formations in the annulus
2. **Casing support:** Bonds the casing to the formation, preventing movement
3. **Corrosion protection:** Protects the outer surface of the casing from formation fluids
4. **Well control barrier:** Cement + casing = the secondary barrier behind the wellbore fluid

### Cementing Process

```
1. Run casing to target depth
2. Circulate bottom to top (clean the hole, condition mud)
3. Run cementing head on top of casing
4. Pump spacer fluid (to separate mud from cement) — typically 20–50 bbl
5. Release BOTTOM PLUG (a rubber wiper plug that sweeps mud ahead of cement)
6. Pump cement slurry behind the plug (calculated volume to fill annulus to target depth)
7. Release TOP PLUG (sweeps cement behind it, displaces with mud)
8. Pump displacement fluid (mud) behind top plug
9. Top plug lands on bottom plug at float collar (bump) → pressure spike confirms plug bump
10. STOP pumping. Float valve holds cement in annulus. Wait for cement to set (8–24 hours).
```

### Cement Slurry Design

**Density:** Typical cement slurry = 1.8–2.0 kg/L. Must be:
- Heavy enough to control formation pressure in the annulus during cementing
- Light enough not to fracture weak formations above the shoe

**Thickening time:** How long before the cement becomes unworkable. Must be > pumping time + safety margin (usually 30–60 minutes extra).

**Compressive strength:** Target > 500 psi (35 bar) before drilling the plug and next hole section.

**Additives used in Angola deepwater:**
- **Accelerators** (CaCl₂): In cold deepwater water where temperatures slow setting
- **Retarders**: In HPHT wells where high temperatures accelerate setting too fast
- **Lightweight additives** (silica, foam cement): Reduce slurry density to prevent fracturing weak formations
- **Anti-gas migration additives**: Prevent gas migration through the cement during setting (critical for Angola wells with high GOR)

### Angola Deepwater Cementing Challenges

**Temperature:** Seabed temperature at 1,500m depth = 3–5°C. Cement hydration is very slow at cold temperatures. Accelerators required.

**Shallow water flow:** In some Angola deepwater wells, over-pressured water-bearing sands above the reservoir can flow into the cemented annulus and contaminate the cement while it's setting. Requires careful design.

**Long cement columns:** Cementing 9⅝" across 1,500m of annulus means large cement volumes and long pumping times. Each additional hour of pumping time requires more retarder to keep the slurry fluid.

---

## Part 8: Torque, Drag, and Wellbore Mechanics

In a directional well, friction between the drill string and the borehole wall creates:
- **Torque:** Rotational resistance that the top drive must overcome
- **Drag:** Axial friction that increases apparent weight when running in hole and reduces it when pulling out

**Why this matters:**
- Excessive torque → twisted-off drill string (catastrophic)
- Excessive drag → inability to reach target depth (stuck pipe)
- In Angola's long high-angle wells (2,000m+ horizontal sections): T&D management is critical to well success

### T&D Calculations

**For a straight inclined section:**

Axial friction load:
$$F_{friction} = \mu \times W_{string} \times \cos(\theta)$$

Normal force (force of string against borehole wall):
$$N = W_{string} \times \sin(\theta)$$

Torque from friction:
$$T_{friction} = \mu \times N \times r_{pipe}$$

Where μ = coefficient of friction (OBM: 0.15–0.25; WBM: 0.25–0.35), θ = inclination angle, $W_{string}$ = buoyed weight of drill string.

**T&D software:** Landmark WellPlan, SLB Wellbore Advisor, Halliburton WellFlo. These compute the full 3D T&D profile along the well trajectory. Run T&D models before every Angola well to confirm the drill string design is adequate.

---

## Part 9: Stuck Pipe — The Most Expensive Drilling Problem

Stuck pipe costs the global drilling industry hundreds of millions of dollars per year. It is the most common cause of drilling NPT (non-productive time).

### Differential Sticking

**Mechanism:** The drill string is pressed against the borehole wall by the pressure difference between the mud column (overbalanced relative to the formation). As the string sits stationary against the permeable borehole wall, the filter cake grows and embeds the pipe.

**Signs:** Pipe is stuck while stationary. Weight indicator reads full string weight. Rotation possible initially (before cake hardens). Zero drag on pickup.

**Solution:** Reduce differential pressure (reduce pump pressure or bleed off mud weight), apply spotting fluid (diesel-OBM mixture or commercial spotting fluid that dissolves filter cake), jarring.

### Mechanical Sticking

**Mechanisms:**
- **Key-seating:** A channel worn into the borehole wall by drill string contact in a dogleg. Pipe runs through easily while rotating but catches on the key seat when pulling out.
- **Pack-off:** Cuttings accumulate in the annulus if transport is inadequate → cuttings bed → pipe gets buried
- **Wellbore collapse:** Unstable formation caves in around the drill string

**Signs of pack-off:** High torque and drag building before the pipe stops moving. Pump pressure increases (annulus packing off).

**Solution for key-seating:** Ream through with a reamer. Reduce dogleg severity in future wells. Use a near-bit reamer.

**Prevention:** Good hole cleaning (flow rate, pipe rotation, sweeps), low dogleg severity, appropriate mud weight for wellbore stability.

---

## Part 10: Cementing Quality Evaluation

After cementing, before drilling the next section, you need to verify the cement job quality.

**Cement Bond Log (CBL/VDL):**
A sonic log run in the cased hole. The acoustic energy travels through the casing and into the cement/formation. Good bond = energy is attenuated by the cement = low signal amplitude at the receiver. Poor bond = energy travels through the free pipe = high amplitude.

**Radial bond evaluation:** Newer tools (Isolation Scanner, Flexus Bond Tool) give a circumferential image of cement quality — essential for Angola well integrity requirements.

**What you're looking for:**
- Cement top location (confirm cement reached the target depth)
- Micro-annuli (hairline gaps at casing-cement interface)
- Channeling (vertical paths through the cement column where cement was contaminated or channeled by gas)

**ANPG requirement:** Operators must submit cementing evaluation logs to ANPG for each primary cement job. If cement quality is inadequate → squeeze cementing repair job must be performed before continuing.

---

## Exercises — Angola Drilling Scenarios

**Exercise 1: Kill Mud ECD**
You are drilling a 12¼" hole at 3,000m TVD with 1.52 kg/L mud. Annular pressure loss = 38 bar. The fracture gradient at the 13⅜" shoe at 2,500m is 1.72 kg/L. Calculate:
1. The ECD at the shoe
2. Is the ECD within the fracture gradient? What is your safety margin?

**Exercise 2: Casing Burst Design**
A 9⅝" casing is set at 4,500m TVD. During a well control event, the maximum internal pressure at the top of the casing = 280 bar. The minimum burst resistance of P-110 53.5 lb/ft casing = 620 bar (single-wall burst pressure). Design factor = 1.10. Is this casing acceptable for burst?

**Exercise 3: Directional Calculation**
A well has a kick-off point (KOP) at 1,500m TVD and builds angle at 3°/30m. Starting vertical. At what depth will the well reach 45° inclination? At that depth, what is the horizontal displacement from the KOP?

(Use: $\Delta_{TVD} = \frac{(\theta_2 - \theta_1)°}{3°/30m} \times 30m \times \cos(\bar{\theta})$, where $\bar{\theta}$ = average inclination)

**Exercise 4: Barite Addition During Cement Job**
Your pre-cement mud weight = 1.55 kg/L. After the cement job, you need to bump back to 1.65 kg/L due to a deeper overpressured zone. You have 400 barrels of active mud. Using the formula from the Drilling Fluids Tutorial, calculate how many sacks of barite to add.

---

## Interview Questions — Drilling Fundamentals

1. A drillship in Angola Block 17 is drilling the 8½" production hole at 4,200m TVD. The MWD operator reports a 30% increase in torque over the past hour. What are the possible causes and what do you do?
2. Explain the telescoping casing design concept. Why can't you run all casing at the same size?
3. What is the difference between a PDC bit and a roller cone (tri-cone) bit? When would you choose each?
4. Why is OBM dominant in Angola's deepwater wells rather than WBM?
5. An intermediate casing (9⅝") failed a cement bond log — large channels observed from 2,200m to 2,500m. What are your options?
6. What is the function of stabilizers in the BHA? How does their placement affect wellbore trajectory?
7. A Block 32 well targeting a reservoir 2.5 km horizontally from the wellhead requires a horizontal well. Describe the well profile and key challenges.
8. What is differential sticking, and what do you do to free a differentially stuck pipe?

---

*Next: [03_FPSO_Operations_Tutorial.md](03_FPSO_Operations_Tutorial.md) | See also: [01_Well_Control_Tutorial.md](01_Well_Control_Tutorial.md)*
## Part 7: Primary Cementing

After running casing in the hole, cement is pumped down the inside of the casing, through the float equipment at the bottom, and back up the annulus between the casing OD and the borehole wall. The goals:

1. **Zonal isolation:** Prevent formation fluids from moving from one zone to another via the annulus
2. **Casing support:** Bond the casing to the formation
3. **Corrosion protection:** Protect the casing from corrosive formation fluids

**Cement job sequence:**
1. Condition mud (circulate to ensure clean wellbore)
2. Pump lead cement (usually lightweight/foamed cement to avoid fracturing the formation)
3. Pump tail cement (higher strength, normal density)
4. Pump top plug — displaces cement with drilling fluid and separates plug from cement
5. Bump the plug on the float collar — confirms required displacement
6. Check for backflow — float valve holds cement in place

**Common cement problems:**
- **Channeling:** Cement doesn't fully displace mud in irregular boreholes — leaves mud channels providing zonal communication
- **Gas migration:** Gas migrates through unset cement before it gels — dangerous
- **Free water:** Excess water at the top of the cement column — reduced bond at top of casing

---

## Part 8: Drilling Parameters and Their Meaning

On a real-time drilling screen, you will see these parameters continuously:

| Parameter | Symbol | What It Tells You |
|---|---|---|
| Rate of Penetration | ROP | How fast the bit is drilling (m/hr). Drilling break = sudden ROP increase |
| Weight on Bit | WOB | Force applied to the bit (tonnes or klbf). Too little = slow. Too much = vibration damage |
| Rotary Speed | RPM | Bit rotation speed. Combined with WOB for optimization |
| Torque | TQ | Resistance to rotation. High torque = tight spots, pack-off risk |
| Stand Pipe Pressure | SPP | Pump pressure. Changes with mud weight, flow rate, restrictions |
| Flow Rate | Q | Pump output in bbl/min. Affects hydraulic horsepower at bit |
| Equivalent Circulating Density | ECD | Effective mud density while circulating (see well control tutorial) |
| Hook Load | HKLB | Total weight on hook. Tells you drillstring weight in different conditions |
| Pit Volume Total | PVT | Total mud volume in active system. Changes = influx or loss |
| Differential Pressure | Diff P | Pressure differential across motor or bit. Used to optimize motor performance |

---

## Part 9: Practice Exercises

**Exercise 1:** Draw the telescoping casing design for an Angola deepwater well with 4 casing strings. Label each size, typical depth, and the purpose of each string.

**Exercise 2:** A well is being drilled at 3,200m TVD. Mud weight is 1.52 kg/L. Pump rate = 600 L/min. Annular velocity in a 12¼" hole with 5" DP is 0.65 m/s. Calculate:
- Hydrostatic pressure at 3,200m
- Flow rate in bbl/min
- Will this annular velocity effectively carry cuttings? (Need >0.6 m/s for adequate hole cleaning)

**Exercise 3:** From memory, draw a simplified BHA for a deepwater directional well at 2,000m TVD, 45° inclination. Label the components from bit to top.

**Exercise 4:** A kick is detected at 3,500m TVD. Current mud weight = 1.48 kg/L. SIDPP = 65 bar. Calculate the kill mud weight in kg/L.

---

## Part 10: Where to Study Further

| Resource | Format | Notes |
|---|---|---|
| "Applied Drilling Engineering" — Bourgoyne et al. (SPE) | Textbook | Classic reference, available through SPE student access |
| "Drilling Engineering" — Neal Adams | Textbook | More practical focus |
| DrillingForGas YouTube channel | Video | Clear visual explanations of rig components |
| Landmark (Halliburton) WellPlan tutorial videos | Video | Hydraulics and torque/drag in practice |
| SPE Student Chapter paper presentations | Free PDFs | Real Angola well case studies |
| IADC Drilling Manual | Reference | Industry standard operational reference |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [docs/skills/02-drilling-fundamentals.md](../../../docs/skills/02-drilling-fundamentals.md)*  
*Where to learn: [PetroWiki](https://petrowiki.spe.org/Drilling) | [Drillingformulas.com](https://drillingformulas.com) | [Learning Resources](../../../docs/learning-resources.md)*
