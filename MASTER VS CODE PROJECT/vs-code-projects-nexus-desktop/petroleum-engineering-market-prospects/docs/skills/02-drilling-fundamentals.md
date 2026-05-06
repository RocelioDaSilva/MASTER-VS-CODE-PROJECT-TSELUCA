# Skill 02 â€” Drilling Fundamentals

> **Applies to:** Field Engineer Trainee, Drilling Engineer, [MWD](../glossary.md)/LWD Engineer, Wellsite Geologist, Completions Engineer
> **Why offshore:** Every offshore drilling job â€” from a jackup on Block 0 to a drillship at 2,000m on Block 32 â€” runs on these same fundamentals. If you don't know the rig, you can't work on it.

---

## What Is This Skill?

Drilling fundamentals covers the mechanical and operational knowledge of how a well is drilled: the rig components, the drill string, the bottomhole assembly, drilling parameters, casing design, and well construction sequence. It is the common language of everyone on a drilling rig â€” regardless of whether they work for the operator, a drilling contractor, or a service company.

---

## Why It Matters Offshore

In Angola's deep-water environment, drilling a single well on Block 17 or Block 32 costs **$80â€“$150 million**. Every person on the rig â€” from the tool pusher to the field engineer â€” is working against a tight cost and schedule target. You need to understand what is happening in the hole at all times, why each decision is made, and how your job connects to the overall well program.

---

## Key Concepts to Master

### 1. Offshore Drilling Rig Types

| Rig Type | How it works | Water depth | Angola use |
|---|---|---|---|
| **Jackup** | Three legs extend to the seabed, lifts hull above water | <150m | Block 0 (Cabinda shelf) |
| **Semi-submersible (Semi)** | Pontoons submerged, buoyancy-stabilized, moored or DP | 300â€“3,000m | All deepwater Angola blocks |
| **Drillship** | Ship-shaped, Dynamic Positioning (DP), highly mobile | 300â€“3,600m | Exploration wells on new blocks |
| **Tender Assisted** | Tender barge supports a fixed platform | Shallow | Not common in Angola deepwater |

**Angola's deepwater rigs:** The ultra-deepwater drillships and semis operating in Angola (e.g., Valaris, Transocean, Stena Drilling vessels) are among the most capable drilling assets in the world.

---

### 2. Rig Components (Top to Bottom)

```
DERRICK
  â””â”€ Crown Block (fixed pulley at top)
  â””â”€ Travelling Block (moves up/down with hook)
  â””â”€ Hook + Swivel (connects to drill string)
  â””â”€ Top Drive (rotates drill string) â€” modern rigs
  
DRILL FLOOR (Rig Floor)
  â””â”€ Rotary Table (older rigs, before top drives)
  â””â”€ Kelly Bushing
  â””â”€ Mouse Hole / Rat Hole (temporary pipe storage)
  â””â”€ Iron Roughneck (automated pipe makeup)

SUBSTRUCTURE
  â””â”€ BOP Stack (below drill floor on subsea wells â†’ on seabed)
  â””â”€ Riser (connects seafloor BOP to rig â€” for deepwater)

MUD SYSTEM
  â””â”€ Mud Pits (trip tanks, suction tanks, reserve)
  â””â”€ Mud Pumps (circulate drilling fluid)
  â””â”€ Shale Shakers (remove cuttings from returning mud)
  â””â”€ Desanders, Desilters, Mud Cleaner
  â””â”€ Centrifuge

POWER SYSTEM
  â””â”€ Diesel generators (most rigs) or dual-fuel systems
```

---

### 3. The Drill String

The drill string transmits rotation and weight to the bit, and circulates drilling fluid.

**From top to bottom:**

| Component | Function |
|---|---|
| **Kelly / Top Drive** | Connects rig rotation to drill string |
| **Drill Pipe (DP)** | Long hollow tubes (~9.5m / 31ft each), carry fluid and rotation down |
| **Heavy Weight Drill Pipe (HWDP)** | Thicker walls, transition between DP and collars |
| **Drill Collars (DC)** | Heavy, thick-walled pipe; provides weight on bit (WOB) |
| **Stabilizers** | Blades that centralize [BHA](../glossary.md) against borehole wall â€” control well path |
| **Drill Bit** | Cuts the formation |

**Key metric: Weight on Bit (WOB)** â€” force applied to the bit to make it cut. Measured in 1,000 lbs (klbs) or kN. Too little = slow drilling. Too much = bit damage, vibration, deviation.

---

### 4. The Drill Bit

| Bit Type | Best for | Identifier |
|---|---|---|
| **Tricone / Roller Cone (PDC)** | Soft to medium formations | Three rotating cones with teeth |
| **PDC (Polycrystalline Diamond Compact)** | Hard formations, faster ROP, common deepwater | Fixed cutters, no moving parts |
| **Diamond / Impregnated** | Very hard abrasive rock | Special applications |

PDC bits dominate modern Angola deepwater drilling â€” they drill faster and last longer.

---

### 5. Key Drilling Parameters

| Parameter | Symbol | What it controls | Typical range |
|---|---|---|---|
| **Weight on Bit** | WOB | Rate of penetration (ROP) | 5â€“30 klbs |
| **Rotary Speed** | RPM | How fast bit rotates | 60â€“200 RPM |
| **Flow Rate** | GPM or L/min | Cuttings lifting, cooling bit | 500â€“1,200 GPM |
| **Rate of Penetration** | ROP | How fast you drill (ft/hr, m/hr) | 20â€“200+ m/hr depending on formation |
| **Torque** | ft-lbs | Friction resistance on drill string | Varies with depth/formation |
| **Standpipe Pressure** | SPP (psi) | System pressure indication | 1,500â€“5,000 psi |
| **ECD** | ppg equivalent | Total pressure exerted on formation | Must stay between PP and FP |

---

### 6. Casing Design and Well Architecture

Wells are not just an open hole from surface to reservoir. They are constructed in concentric steel tubes:

```
SURFACE (seabed for deepwater)
  â”‚
  â”œâ”€ Conductor Pipe (30"-36") â€” structural, supports wellhead
  â”‚
  â”œâ”€ Surface Casing (18Â¾"-20") â€” isolates shallow formations, supports BOP
  â”‚
  â”œâ”€ Intermediate Casing (13â…œ"-16") â€” bridges troublesome zones (shale, overpressure)
  â”‚
  â”œâ”€ Production Casing / Liner (9â…"-10Â¾") â€” isolates reservoir
  â”‚
  â””â”€ Liner / Tieback (7"-7â…") â€” optional, deep sections
         â”‚
         â””â”€ RESERVOIR (Open Hole or Perforated Casing)
```

**Why multiple strings?** Each casing string is cemented in place to isolate different pressure regimes. Without this, high-pressure formations deeper in the well cannot be managed while drilling shallower formations.

**Conductor pipe for deepwater:** Jetted or driven into the seabed mud before drilling begins. The BOP stack then latches onto the subsea wellhead at seafloor level.

---

### 7. The Drilling Circulation System

Drilling fluid (mud) is pumped down the drill string, exits through the bit, and returns to surface via the **annulus** (space between drill string and borehole wall), carrying cuttings with it.

```
Mud pits â†’ Mud pumps â†’ Standpipe â†’ Swivel/Top Drive 
  â†’ DOWN through Drill String â†’ Out through bit jets
  â†’ UP through Annulus (carrying cuttings)
  â†’ Through Riser (deepwater) â†’ BOP/Wellhead â†’ Mud Return Line
  â†’ Over Shale Shaker â†’ Cleaned mud back to pits
```

**Annular velocity (AV)** must be high enough to carry cuttings to surface:
$$AV \text{ (ft/min)} = \frac{0.408 \times Q}{D_h^2 - D_p^2}$$

Where Q = flow rate (GPM), Dh = hole diameter (inches), Dp = pipe OD (inches)

---

### 8. Well Construction Sequence (Deepwater Angola, typical)

1. **Jet/drill and set conductor** (36" Ã— 30") â€” from seafloor to ~150m
2. **Drill and set surface casing** (20" Ã— 18Â¾") â€” to ~600â€“800m, install subsea wellhead + BOP
3. **Drill and set intermediate casing** (16" Ã— 13â…œ") â€” through overpressured formations
4. **Drill and set production casing** (13â…œ" Ã— 9â…") â€” through reservoir
5. **Run production liner + perforate** â€” complete the well for production
6. **Test well** â€” flow test to confirm productivity
7. **Suspend or complete** â€” install wellhead for [FPSO](../glossary.md) tieback or temporarily abandon

---

### 9. Drilling Operations Vocabulary (Must Know)

| Term | Meaning |
|---|---|
| **Tripping** | Pulling drill string out of or running it back into the hole |
| **Make a connection** | Adding a new joint of drill pipe every ~30 feet |
| **Spud / Spudding in** | Beginning drilling a new well |
| **TD** | Total Depth â€” the final depth of the well |
| **POOH / RIH** | Pull Out Of Hole / Run In Hole |
| **Wiper trip** | Short trip to condition the hole before a long trip |
| **Reaming** | Passing the [BHA](../glossary.md) up and down to clean the hole |
| **Drilling break** | Sudden increase in ROP â€” often indicates formation change or kick |
| **Tight hole** | Drill string experiences abnormally high drag going in or coming out |
| **Stuck pipe** | Drill string cannot move up or down â€” can be differential sticking or mechanical |
| **Fishing** | Recovering a downhole tool or broken pipe from the wellbore |
| **Sidetrack** | Drilling a new hole branch from an existing wellbore |

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Learn all rig component names and draw a rig from memory
- [ ] Understand the difference between jackup, semi, and drillship â€” when each is used
- [ ] Know the drill string from top drive to bit
- [ ] Learn the 5 main drilling parameters and what each controls
- [ ] Walk through a complete well construction sequence (conductor â†’ production casing)

### Intermediate (2â€“5 months)
- [ ] Calculate ECD, AV, hydrostatic pressure in drilling scenarios
- [ ] Understand casing design: why each string is needed, what it isolates
- [ ] Learn the full circulation system â€” where fluid goes and why
- [ ] Study a real deepwater Angola wellbore schematic ([TotalEnergies](../../data/company-directory/totalenergies.md)/Block 17 public presentations)
- [ ] Learn rig floor operations: trip, connection, reaming, making up pipe

### Advanced (5â€“12 months)
- [ ] Understand drillstring dynamics: vibration modes (lateral, axial, torsional), their effects on WOB/ROP, mitigation
- [ ] Study wellbore stability: breakout, washout, differential sticking mechanisms
- [ ] Learn advanced [BHA](../glossary.md) design for directional wells
- [ ] Study deepwater-specific challenges: shallow hazards, gas hydrates at seafloor, riser management

---

## Resources

| Resource | Type | Cost |
|---|---|---|
| **Bourgoyne et al., "Applied Drilling Engineering"** (SPE textbook Vol. 2) | Reference book | Available via SPE or library |
| **IADC Drilling Manual** | Industry reference | iadc.org (paid) |
| **Drillingformulas.com** | Tutorials + calculations | Free |
| **Petrowiki (SPE)** | Wiki-style reference | Free â€” petrowiki.spe.org |
| **YouTube: Drilling Engineering by HH** | Video series | Free |
| **Wellbore Design PDF â€” [TotalEnergies](../../data/company-directory/totalenergies.md) publications** | Applied examples | Free via public TotalEnergies technical library |

---

## Practice Questions

1. Name all components of the drill string from top to bottom.
2. A 12Â¼" hole is being drilled with 5" drill pipe. Flow rate is 750 GPM. Calculate annular velocity.
3. Why do deepwater wells have more casing strings than onshore wells?
4. What is ECD and why does it matter in a narrow pressure window?
5. What is the difference between ROP and WOB, and how do they relate?
6. Explain what happens physically during a "drilling break" and what action you take.

---

## Related Skills

- [01 â€” Well Control](01-well-control.md) (the safety layer applied to everything you drill)
- [03 â€” Drilling Fluids](03-drilling-fluids.md) (the fluid that makes drilling possible)
- [05 â€” Directional Drilling](05-directional-drilling.md) (how to control well path)
- [06 â€” MWD/LWD Tools](06-mwd-lwd-tools.md) (sensors that measure what's happening downhole)
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (what happens after drilling)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Drilling** | Free reference | Free | [petrowiki.spe.org/Drilling](https://petrowiki.spe.org/Drilling) |
| **Drillingformulas.com** | Free tutorials | Free | [drillingformulas.com](https://drillingformulas.com) |
| **Applied Drilling Engineering** (Bourgoyne) | Textbook | ~$80 | [SPE Bookstore](https://store.spe.org) |
| **Fundamentals of Drilling Engineering** (Mitchell & Miska) | Textbook | ~$90 | [SPE Bookstore](https://store.spe.org) |
| **PetroSkills â€” Drilling Practices** | Paid course | $500â€“3,000 | [petroskills.com](https://www.petroskills.com) |
| **Udemy â€” Drilling Engineering** | Paid course | $10â€“30 | [udemy.com](https://www.udemy.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

