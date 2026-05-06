# Skill 09 â€” Artificial Lift Systems

> **Applies to:** Production Engineer, [FPSO](../glossary.md) Production Operator, Completions Engineer, Field Engineer ([Weatherford](../../data/company-directory/weatherford.md), SLB, [Baker Hughes](../../data/company-directory/bakerhughes.md))
> **Offshore relevance:** Most Angola deepwater wells require artificial lift within 3â€“7 years of first production as reservoir pressure declines

---

## What Is This Skill?

Artificial lift refers to any method used to increase the flow of fluids from a well when the natural reservoir energy (pressure) is insufficient to lift fluids to surface on its own. In Angola's deepwater environment, the most common systems are Electric Submersible Pumps (ESP) and gas lift â€” both are critical to sustaining production on FPSOs long-term.

---

## Why It Matters Offshore

Angola's deepwater reservoirs (Blocks 15, 17, 32) initially flow naturally at high rates â€” reservoir pressure is high and wells produce without artificial assistance. However, as production continues and reservoir pressure drops, wells need help. **Without artificial lift, production declines rapidly and becomes uneconomical.** FPSOs are designed from day one to accommodate artificial lift:
- ESP strings are installed in completion designs
- Gas lift mandrels are built into production tubing
- FPSOs have dedicated gas lift compressors

A Production Engineer in Angola who doesn't understand artificial lift cannot manage their well portfolio.

---

## Key Concepts to Master

### 1. Why Wells Need Artificial Lift

**Natural flow condition:** Well flows if the wellhead pressure (from reservoir) exceeds all pressure losses in the system:

$$P_{reservoir} > P_{wellbore\_friction} + P_{hydrostatic} + P_{wellhead}$$

As reservoir pressure drops or water cut increases (water is heavier than oil â†’ greater hydrostatic load), the well stops flowing or produces below economic rates.

---

### 2. Electric Submersible Pump (ESP)

**What it is:** A multi-stage centrifugal pump + motor assembly deployed inside the production tubing, suspended on an electric power cable.

```
Surface transformer (on FPSO)
  â†’ Power cable (inside tubing string)
  â†’ Downhole motor (rotates on electricity)
  â†’ Seal/protector (isolates motor from wellbore fluids)
  â†’ Intake section (screens fluid entering pump)
  â†’ Pump stages (50â€“500+ stages, each adds head/pressure)
  â†’ Fluid flows up tubing to [FPSO](../glossary.md)
```

**How ESP works:**
- Each pump stage adds hydraulic head (energy) to the fluid
- Multi-stage impellers create high differential pressure
- Pump is sized to the well: flow rate (BPD) vs. head requirement (psi or meters)

**Key ESP parameters:**

| Parameter | Definition | Purpose |
|---|---|---|
| **Frequency (Hz)** | Motor operating frequency (50 or 60 Hz standard; VSD allows variable) | Controls pump speed â†’ controls flow rate |
| **Flow rate (BPD)** | Volume pumped per day | Must match well productivity to avoid surge or dead-heading |
| **Head (psi or meters)** | Pressure increase provided per stage Ã— stages | Must overcome gravity + friction to surface |
| **Motor HP/kW** | Power required | Cable and transformer must be sized correctly |
| **Motor temperature** | Critical limit â€” overheating kills motor windings | VSD protection; adequate flow for cooling |
| **VSD (Variable Speed Drive)** | Surface device that varies frequency â†’ varies speed | Most modern ESPs are variable speed |

**ESP performance curve:**
- Pump curve shows head vs. flow rate at fixed speed
- System curve shows head required by the well system vs. flow
- **Operating point:** Where pump curve intersects system curve

**ESP failure modes (most common causes of downtime):**
- **Motor winding failure** (overheating, water ingress)
- **Scale buildup** on pump stages (calcium carbonate, barium sulfate)
- **Gas locking** â€” gas enters pump, pump cannot create head on vapor
- **Abrasion** from sand production
- **Shaft failure** from vibration or misalignment

**Angola ESP context:** Angola deepwater ESPs operate at depths of 1,000â€“2,500m TVD, high temperatures (up to 150Â°C), high pressures, and often in wells producing with high water cut. This is among the most demanding ESP application in the world.

**Main ESP suppliers:** [SLB](../../data/company-directory/slb.md) (Centrilift, now [SLB](../../data/company-directory/slb.md) ESP), [Baker Hughes](../../data/company-directory/bakerhughes.md), Weatherford, Borets, OneSubsea ([SLB](../../data/company-directory/slb.md))

---

### 3. Gas Lift

**What it is:** Injecting compressed gas into the tubing-annulus side of the completion, which enters the production tubing through gas lift valves, mixes with the produced fluid, and reduces the average fluid density in the tubing â€” making it easier for reservoir pressure to lift fluid to surface.

```
Gas lift compressor (on FPSO)
  â†’ Injection line â†’ Down the annulus (between tubing and casing)
  â†’ Gas lift mandrels (at specific depths in tubing string)
  â†’ Gas lift valves (open when annulus pressure > pressure differential)
  â†’ Gas bubbles into production tubing
  â†’ Fluid density drops â†’ lighter column â†’ well flows
```

**Why gas lift is preferred in some Angola wells:**
- No downhole moving parts â†’ very reliable, low OPEX
- Can handle high sand production (no ESP impellers to erode)
- Easy to adjust injection rate from surface ([FPSO](../glossary.md) gas lift compressor)
- Recoverable if tubing fails â€” gas lift completion is simpler to pull and replace

**Gas lift design considerations:**
- **Depth of injection:** Deeper injection = more benefit (more column lightened)
- **Injection gas rate:** Optimum injection rate â€” too much gas causes turbulence and pressure losses
- **Gas lift valve design:** Dummy valves, unloading valves, operating valve
- **Mandrel spacing:** Calculated to allow staged unloading

**Continuous vs. Intermittent gas lift:**
- **Continuous:** Constant gas injection â€” most Angola deepwater wells use continuous
- **Intermittent:** Cycles on/off â€” used for low-productivity wells

---

### 4. Other Artificial Lift Methods (Less Common Offshore Angola)

| Method | Principle | When used |
|---|---|---|
| **Hydraulic Jet Pump (HJP)** | High-pressure surface fluid injected downhole, creates venturi suction | Some Angola wells with no electrical power available |
| **Progressing Cavity Pump (PCP)** | Positive displacement rotary pump â€” handles viscous oil and sand | Shallow wells, not deepwater |
| **Plunger Lift** | Cylindrical plunger cycles through tubing to unload liquids | Low-rate / high GOR gas wells |
| **Beam Pump (Sucker Rod)** | Surface beam lifts sucker rod string connected to downhole pump | Onshore only |

---

### 5. IPR and VLP â€” The Production Engineering Framework

**Inflow Performance Relationship (IPR):** How much the reservoir can deliver as a function of bottomhole flowing pressure.

$$q = J (P_R - P_{wf})$$

Where:
- q = flow rate
- J = productivity index (PI) [bbl/day/psi]
- P_R = reservoir pressure
- P_wf = bottomhole flowing pressure

For two-phase flow (Vogel correlation):
$$\frac{q}{q_{max}} = 1 - 0.2 \frac{P_{wf}}{P_R} - 0.8 \left(\frac{P_{wf}}{P_R}\right)^2$$

**Vertical Lift Performance (VLP):** How much pressure is needed at bottomhole to lift the fluid to the [FPSO](../glossary.md) at the required wellhead pressure.

**System analysis:** IPR and VLP intersect at the operating point. Artificial lift shifts the VLP curve down (reduces required BHP), finding a new, higher-flow intersection.

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Understand why wells need artificial lift (natural energy depletion)
- [ ] Learn the ESP completion: motor, seal, intake, pump stages, power cable
- [ ] Learn gas lift: how gas enters tubing, why it lightens the fluid column
- [ ] Read IPR and VLP curves: identify the operating point

### Intermediate (2â€“5 months)
- [ ] Calculate ESP head requirement for a specific well scenario
- [ ] Understand VSD operation and how to adjust ESP frequency to optimize production
- [ ] Study gas lift design: mandrel spacing, valve selection, injection depth
- [ ] Use PROSPER (PETEX) software for nodal analysis â€” free trial available

### Advanced (5â€“12 months)
- [ ] Design an artificial lift selection for a new Angola deepwater well
- [ ] Study ESP failure analysis: read motor current vs. time curves to diagnose failure modes
- [ ] Learn real-time ESP monitoring parameters: motor current, motor temperature, pump inlet pressure
- [ ] Study artificial lift optimization in decline scenarios (field production decline management)

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **PETEX PROSPER software** | Industry production modelling tool | Free trial / paid |
| **[Weatherford](../../data/company-directory/weatherford.md) Artificial Lift Handbook** | Comprehensive AL reference | Available from Weatherford contacts |
| **[Baker Hughes](../../data/company-directory/bakerhughes.md) ESP Design Course** | Online/training center | Paid |
| **SPE papers "Artificial Lift Angola"** | Real case studies | Free with SPE student membership |
| **Petrowiki â€” Artificial Lift** | Good overview of all methods | Free |

---

## Practice Questions

1. A well has PI = 2 bbl/day/psi, reservoir pressure = 3,500 psi. If BHP drops to 1,200 psi with gas lift, what is the flow rate?
2. What is gas locking in an ESP, and how do you prevent it?
3. Why is gas lift preferred over ESP in some Angola deepwater wells with high sand production?
4. An ESP is running at 60 Hz. Production is below target. What actions can you take?
5. Draw a simple nodal analysis diagram showing IPR, VLP, and how an ESP shifts the VLP curve.

---

## Related Skills

- [08 â€” FPSO Process Operations](08-fpso-process-operations.md) (gas lift compressors are on the [FPSO](../glossary.md))
- [10 â€” Flow Assurance](10-flow-assurance.md) (artificial lift must overcome [flow assurance](10-flow-assurance.md) issues too)
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (gas lift mandrels and ESP completions are part of well design)
- [14 â€” Reservoir Engineering Basics](14-reservoir-engineering.md) (IPR comes from reservoir properties)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Artificial Lift** | Free reference | Free | [petrowiki.spe.org/Artificial_lift](https://petrowiki.spe.org/Artificial_lift) |
| **SLB Learning â€” ESP modules** | Free student | Free | [learn.slb.com](https://learn.slb.com) |
| **PROSPER** | Nodal analysis software (student) | Free student license | [petex.com/academic](https://www.petex.com/academic/) |
| **Production Optimization Using Nodal Analysis** (Beggs) | Textbook | ~$80 | SPE / technical libraries |
| **PetroSkills â€” Artificial Lift** | Paid course | $1,000â€“3,000 | [petroskills.com](https://www.petroskills.com) |
| **Udemy â€” ESP Design** | Paid course | $10â€“30 | [udemy.com](https://www.udemy.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

