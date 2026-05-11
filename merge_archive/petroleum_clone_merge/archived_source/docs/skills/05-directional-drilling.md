# Skill 05 â€” Directional Drilling

> **Applies to:** [MWD](../glossary.md)/LWD Field Engineer, Directional Driller (DD), Drilling Engineer, Field Engineer Trainee
> **Companies:** [SLB](../../data/company-directory/slb.md) (PowerDrive), [Halliburton](../../data/company-directory/halliburton.md) (Sperry Drilling), [Baker Hughes](../../data/company-directory/bakerhughes.md) (AutoTrak), [National Oilwell Varco](../angola/angolan-offshore-companies.md) ([NOV](../angola/angolan-offshore-companies.md)), Gyrodata

---

## What Is This Skill?

Directional drilling is the controlled steering of a wellbore along a planned trajectory â€” deviating from vertical to reach a target zone that cannot be accessed directly. Nearly every modern offshore well in deepwater Angola is directional. FPSOs position over the seabed and drill multiple wells from a single wellhead cluster (subsea template), each reaching a different part of the reservoir at various angles. Without directional drilling, deepwater development would be economically impossible.

---

## Why It Matters Offshore

- Angola's subsea templates (e.g., the Block 17 [FPSO](../glossary.md) cluster layouts) have 4â€“12 slots, each with wells drilled to different targets hundreds of meters apart.
- **Extended Reach Drilling (ERD):** Some wells drill horizontally for 5,000â€“10,000m to contact maximum reservoir volume from a single location.
- **Horizontal wells:** In Angola's turbidite reservoirs, horizontal wells dramatically increase productivity â€” a 1,000m horizontal section contacts far more reservoir rock than a vertical well.
- A **Directional Driller (DD)** is one of the most senior, well-paid people on a rig â€” they steer the wellbore in real time, making decisions that determine whether the well hits its $50â€“100M+ target.

---

## Key Concepts to Master

### 1. Well Trajectory Types

```
VERTICAL WELL        DEVIATED WELL         HORIZONTAL WELL
     |                    |                      |
     |                    |  (inclination starts)  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
     |                    |  /                    
     |                    | /  
    â•â•â•                   /                      â•â•â•â•â•â•â•â•â•â•â•
   Target              Target                   Target (long horizontal)
```

| Well type | Inclination at TD | Use case |
|---|---|---|
| **Vertical** | 0Â° | Simple exploration wells, injection |
| **Deviated** | 15Â°â€“70Â° | Reach off-centre targets, multiple well slots |
| **Horizontal** | 80Â°â€“95Â° | Maximum reservoir contact, turbidite sands |
| **S-shape** | Variable | Kick off, reach target, land horizontal |
| **Extended Reach (ERD)** | 80Â°â€“95Â° for 3,000â€“10,000m | Long horizontal sections in high-productively reservoirs |

---

### 2. Fundamental Directional Parameters

| Parameter | Symbol | Definition | Units |
|---|---|---|---|
| **Inclination (Hole Angle)** | Inc | Deviation from vertical (0Â° = vertical; 90Â° = horizontal) | Degrees |
| **Azimuth** | Az | Compass direction of the wellbore (0Â° = North, 90Â° = East) | Degrees |
| **Total Vertical Depth** | TVD | True vertical distance from surface to point | m or ft |
| **Measured Depth** | MD | Actual length along the wellbore (always â‰¥ TVD) | m or ft |
| **Departure / Horizontal Displacement** | HD | Horizontal distance from the well slot to the point in the well | m or ft |
| **True North Displacement** | NS | North/South horizontal component | m or ft |
| **East/West Displacement** | EW | East/West horizontal component | m or ft |
| **Closure** | â€” | Straight-line distance from slot to bottom hole | m or ft |

---

### 3. Dogleg Severity (DLS)

**Dogleg** = a change in well direction. Dogleg Severity measures how sharply the well changes direction per unit length:

$$DLS \text{ (Â°/30m)} = \frac{\sqrt{(\Delta Inc)^2 + (\Delta Az \cdot \sin Inc)^2}}{Î”MD} \times 30$$

Simplified in degrees per 100 ft or degrees per 30m.

**Why it matters:**
- Excessive DLS creates drill string fatigue â†’ failures offshore
- High DLS increases torque and drag â†’ stuck pipe risk
- Maximum DLS limits depend on casing/pipe grades and bit walk characteristics
- Angola deepwater wells typically designed to < 3Â°/30m DLS in curved sections

---

### 4. Directional Tools â€” How Steering Works

#### Build Up / Drop Off / Turn

**Motor + Bent Housing (Steerable Motor):**
- Downhole motor (PDM â€” positive displacement motor) powered by drilling fluid flow
- Bent housing creates a fixed offset angle (1Â°â€“3Â°)
- **Sliding mode:** No drill string rotation â†’ motor and bent sub steer the bit in the bent direction â†’ builds inclination or turns (slow ROP)
- **Rotating mode:** Full rotation â†’ tools neutralize each other â†’ drills straight (normal mode)
- Manual method: DD alternates sliding/rotating to control trajectory

**Rotary Steerable System (RSS):**
- **Push-the-bit type** ([SLB](../../data/company-directory/slb.md) PowerDrive, [Halliburton](../../data/company-directory/halliburton.md) GeoPilot): Pads push against borehole wall to steer
- **Point-the-bit type** ([Baker Hughes](../../data/company-directory/bakerhughes.md) AutoTrak Curve): Internal mechanism deflects bit shaft
- RSS allows continuous rotation while steering â†’ faster ROP, smoother wellbore, less torque
- **RSS is standard for Angola deepwater wells** â€” deepwater horizontal wells cannot use conventional motors efficiently at 2,000m+ water depth + 5,000m+ TVD

---

### 5. Survey Methods â€” How We Know Where We Are

| Method | How it works |
|---|---|
| **Magnetic [MWD](../glossary.md) survey** | Magnetometers + accelerometers inside BHA report inclination and azimuth in real time via mud pulse |
| **Gyro survey** | Mechanical or fiber-optic gyroscope â€” not affected by magnetic interference (used near casing or in magnetic formations) |
| **Continuous inclination (CI)** | [MWD](../glossary.md) surveys every ~30 seconds during drilling |
| **Single-shot / multi-shot** | Older method â€” dropped tool reads inclination and azimuth at a single point |

**[MWD](../glossary.md) surveys:** Taken every 30m (100 ft) during drilling. These are the primary directional data points used to calculate the actual well path vs. the planned trajectory.

**Survey frequency in Angola:** Due to close-proximity wells on subsea templates, **anti-collision analysis** is critical. Each well must be surveyed frequently to ensure it doesn't collide with adjacent existing wells.

---

### 6. Well Path Calculation Methods

**Minimum Curvature Method** (industry standard):

$$TVD = \frac{\Delta MD}{2} (cos I_1 + cos I_2) \cdot RF$$

$$NS = \frac{\Delta MD}{2} (sin I_1 cos A_1 + sin I_2 cos A_2) \cdot RF$$

$$EW = \frac{\Delta MD}{2} (sin I_1 sin A_1 + sin I_2 sin A_2) \cdot RF$$

Where RF (Ratio Factor):
$$RF = \frac{2}{\Delta MD} \cdot \frac{tan(DL/2)}{DL}$$

> Don't worry about memorizing this formula â€” directional software (WellPlan, COMPASS, Landmark) calculates it automatically. But understand *what* it's doing: interpolating a smooth arc between two survey stations.

---

### 7. Geosteering

**Geosteering:** Using real-time [LWD](../glossary.md) [formation evaluation](04-formation-evaluation.md) data to guide the wellbore through a specific geological layer (the reservoir).

- As the well drills horizontally through a turbidite sand, the [LWD](../glossary.md) GR and resistivity logs tell you if you're still in the oil sand or drifting into shale above or below
- The DD adjusts the inclination in real-time to stay in the "sweet spot"
- In Angola, geosteering horizontal wells through thin turbidite sands (sometimes only 10â€“15m thick) requires millimeter-level precision at 1,000m water depth

**Geosteering workflow:**
```
LWD GR/Density/Resistivity (real-time) 
  â†’ Petrophysicist interprets: still in sand? shale above? 
  â†’ Structural geologist updates dip model
  â†’ DD adjusts trajectory â†’ stays in reservoir
```

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Draw the basic well trajectory types (vertical, deviated, horizontal, S-shape)
- [ ] Understand inclination, azimuth, TVD, MD, and departure
- [ ] Learn what DLS means and why it matters
- [ ] Understand the difference between sliding (motor) and rotating (RSS/straight) modes

### Intermediate (2â€“5 months)
- [ ] Calculate TVD, NS, EW from survey data using minimum curvature
- [ ] Use a software tool: COMPASS or free version of WellPlan
- [ ] Understand anti-collision analysis principles (build a 2-well scenario)
- [ ] Study how the RSS tools work mechanically for [SLB](../../data/company-directory/slb.md) PowerDrive Orbit and [Baker Hughes](../../data/company-directory/bakerhughes.md) AutoTrak

### Advanced (5â€“12 months)
- [ ] Learn extended reach well planning: torque and drag modeling
- [ ] Study geosteering case studies (SPE papers on Angola horizontal wells)
- [ ] Understand [LWD](../glossary.md)-based geosteering: real-time interpretation of GR, deep resistivity ahead of bit
- [ ] Learn about well placement software ([SLB](../../data/company-directory/slb.md) BoreTrack / Techlog)

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **Bourgoyne et al., Ch. 8** | Directional [drilling fundamentals](02-drilling-fundamentals.md) | Paid |
| **[Baker Hughes](../../data/company-directory/bakerhughes.md) Directional Drilling Reference Manual** | Clear, practical | Widely available from field contacts |
| **Drillingformulas.com â€” Directional section** | All DD calculations explained | Free |
| **SPE papers on Angola horizontal wells** | Real-world context | Free with SPE student membership |
| **COMPASS software trial** | Industry standard DD planning tool | Contact [Halliburton](../../data/company-directory/halliburton.md) |
| **YouTube: "Directional Drilling Explained"** | Visual intro | Free |

---

## Practice Questions

1. A well has Incâ‚ = 0Â°, Azâ‚ = 0Â°, and Incâ‚‚ = 35Â°, Azâ‚‚ = 120Â° over a measured depth interval of 300m. What type of trajectory is this?
2. Explain the difference between TVD and Measured Depth, and why it matters for pressure calculations.
3. What is the advantage of RSS over a steerable motor for deepwater Angola horizontal wells?
4. A wellbore has DLS = 8Â°/30m. Is this acceptable for an Angola deepwater well? What risk does it create?
5. During geosteering a horizontal well, the [LWD](../glossary.md) GR suddenly increases from 25 to 90 API. What does this mean? What instruction do you give the DD?

---

## Related Skills

- [02 â€” Drilling Fundamentals](02-drilling-fundamentals.md) (the drilling system you're steering)
- [04 â€” Formation Evaluation](04-formation-evaluation.md) ([LWD](../glossary.md) data used for geosteering)
- [06 â€” MWD/LWD Tools](06-mwd-lwd-tools.md) (tools that provide real-time directional and [LWD](../glossary.md) data)
- [01 â€” Well Control](01-well-control.md) (directional wells have unique [well control](01-well-control.md) challenges)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Directional Drilling** | Free reference | Free | [petrowiki.spe.org/Directional_drilling](https://petrowiki.spe.org/Directional_drilling) |
| **Drillingformulas.com â€” Directional** | Free tutorials | Free | [drillingformulas.com](https://drillingformulas.com) |
| **Applied Drilling Engineering** (Bourgoyne) | Textbook | ~$80 | [SPE Bookstore](https://store.spe.org) |
| **Directional Drilling** (Inglis) | Textbook | ~$70 | Technical libraries |
| **SLB PowerDrive / Halliburton GeoPilot** | Company trainee programs | Employer-funded | [careers.slb.com](https://careers.slb.com) Â· [jobs.halliburton.com](https://jobs.halliburton.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

