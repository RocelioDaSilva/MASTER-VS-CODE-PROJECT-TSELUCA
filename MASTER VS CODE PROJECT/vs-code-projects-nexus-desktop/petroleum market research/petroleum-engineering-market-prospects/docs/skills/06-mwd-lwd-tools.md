# Skill 06 â€” MWD/LWD Tools & Operations

> **Applies to:** [MWD](../glossary.md)/LWD Field Engineer (primary role), Drilling Engineer, Directional Driller, Wellsite Geologist
> **Companies in Angola:** [SLB](../../data/company-directory/slb.md) (Drilling & Measurements), [Halliburton](../../data/company-directory/halliburton.md) (Sperry Drilling), [Baker Hughes](../../data/company-directory/bakerhughes.md) (Reservoir Characterization group)

---

## What Is This Skill?

[MWD](../glossary.md) (Measurement While Drilling) and [LWD](../glossary.md) (Logging While Drilling) are downhole tool systems integrated into the [BHA](../glossary.md) (Bottom Hole Assembly) that measure directional, mechanical, and formation data in real time as the well is being drilled. The data is transmitted to surface through the mud pulse telemetry system (or EM/wired pipe alternatives). 

An [MWD](../glossary.md)/LWD Field Engineer is responsible for the surface data acquisition system, the downhole tools, tool maintenance, and real-time interpretation of the incoming data. This is a **heavily offshore** role â€” you live on the rig for your entire 28-day rotation.

---

## Why It Matters Offshore

- In Angola's ultra-deep water (Block 17, 32, 31), lowering a wireline tool after drilling can take hours and risks getting the wireline stuck in a deteriorating borehole. Real-time [LWD](../glossary.md) data is often the only timely [formation evaluation](04-formation-evaluation.md) available.
- Geosteering horizontal wells in thin sands (10â€“30m) requires continuous [LWD](../glossary.md) data to keep the well in the pay zone.
- [MWD](../glossary.md) directional data enables real-time anti-collision monitoring on busy subsea templates.
- The entire well cost optimization â€” knowing when to stop drilling, when to change target â€” depends on the quality of real-time [MWD](../glossary.md)/LWD data.

---

## Key Concepts to Master

### 1. MWD vs. LWD: What's the Difference?

| Term | What it measures | Application |
|---|---|---|
| **[MWD](../glossary.md) (Measurement While Drilling)** | Directional data (inclination, azimuth), downhole WOB, torque, vibration, temperature, pressure | Navigation and drilling optimization |
| **[LWD](../glossary.md) (Logging While Drilling)** | Formation properties (GR, resistivity, density, neutron porosity, sonic) | [Formation evaluation](04-formation-evaluation.md) and geosteering |

In practice, the tools are often combined into a single [BHA](../glossary.md) with both MWD and LWD sensors. Commonly referred to together as **MWD/LWD**.

---

### 2. MWD Sensors and What They Measure

| Sensor | Measurement | Use |
|---|---|---|
| **Magnetometers** (3-axis) | Magnetic field direction â†’ azimuth | Directional surveys |
| **Accelerometers** (3-axis) | Gravitational field â†’ inclination | Directional surveys |
| **Gamma Ray (GR)** | Formation radioactivity | Lithology ID at the bit â€” boundary detection |
| **Annular Pressure While Drilling (APWD)** | Downhole annular pressure | Real-time ECD monitoring â€” critical for [well control](01-well-control.md) |
| **Downhole WOB (DWOB)** | Actual weight at bit | Drilling optimization (rig surface WOB often inaccurate) |
| **Downhole Torque (DTOR)** | Actual bit torque | Detect bit balling, motor stall |
| **RPM** | Drill string rotation speed | Vibration management |
| **Vibration sensors** | Lateral, axial, torsional vibration | Warn about bit bounce, [BHA](../glossary.md) whirl |
| **Temperature tool** | Bottomhole temperature | Fluid design, log interpretation correction |

---

### 3. LWD Sensors and Tool Systems

#### Gamma Ray (GR) LWD
- Located in the [MWD](../glossary.md) sub or LWD string
- ~1â€“2m from bit face â†’ immediate formation identification as you drill
- Critical for geosteering â€” detects the sand/shale boundary in real time

#### Resistivity LWD
| Tool | Company | Description |
|---|---|---|
| **ARC (Array Resistivity Compensated)** | [SLB](../../data/company-directory/slb.md) | Multiple depths of investigation â€” shallow to deep |
| **EcoScope** | [SLB](../../data/company-directory/slb.md) | Integrated multi-measurement collar |
| **ALD/ADN** | [SLB](../../data/company-directory/slb.md) | Azimuthal [LWD](../glossary.md) for geostoering with images |
| **AXT** | [Halliburton](../../data/company-directory/halliburton.md) | Array resistivity with deep azimuthal |
| **OnTrak** | [Baker Hughes](../../data/company-directory/bakerhughes.md) | MWD + GR + basic resistivity |

Deep resistivity reads farther into the formation â€” detects hydrocarbon contacts ahead of the bit ("look-ahead" capability with some tools).

#### Neutron-Density LWD
- **ADN (Azimuthal Density Neutron)** â€” SLB: measures density and neutron porosity, can produce 360Â° borehole images for formation dip
- Essential for porosity estimation and gas detection while drilling
- Slightly less accurate than wireline (borehole rugosity effects, tool standoff)

#### Sonic LWD
- **SonicScope** (SLB), **Bi-Modal Acoustic** ([Baker Hughes](../../data/company-directory/bakerhughes.md)), **Acoustic Logging While Drilling** ([Halliburton](../../data/company-directory/halliburton.md))
- Measures compressional and shear wave velocities
- Used for: formation mechanical properties (geomechanics), pore pressure prediction, seismic tie

#### Formation Pressure While Drilling (FPWD)
- **StethoScope** (SLB), **Geo-Tap** ([Halliburton](../../data/company-directory/halliburton.md)), **TesTrak** ([Baker Hughes](../../data/company-directory/bakerhughes.md))
- Takes pressure measurements in permeable zones while drilling (like a mini-MDT)
- Critical for real-time pore pressure detection â†’ direct input to [well control](01-well-control.md)

---

### 4. Mud Pulse Telemetry â€” How Data Gets to Surface

Downhole MWD tools encode data as **pressure pulses** in the mud column:

```
Downhole tool generates data
  â†’ Tool creates pressure variations in drilling fluid (mud pulses)
  â†’ Signal travels up through mud at speed of sound in fluid
  â†’ Surface sensor detects pressure variations
  â†’ Decoding software reconstructs measurements
  â†’ Data displayed on surface acquisition system (SLB IDEAL, Halliburton QMAX)
```

**Data rate:** Typically 3â€“12 bits/second (very low bandwidth!)
- This is why only the most critical real-time data is transmitted continuously
- Full datasets stored in downhole memory and downloaded when tools are pulled to surface

**Transmission limitations:**
- Water depth and mud compressibility degrade signal in ultra-deep water
- In Angola ultra-deep water (2,000m), signal can be noisy â€” sophisticated decoders needed
- **Electromagnetic (EM) telemetry** is an alternative â€” transmits signal through the earth rather than mud â€” used in lost circulation situations where mud pulse doesn't work
- **Wired Drill Pipe (WDP):** High-speed data (57,600 bps) via inductive coupler in each joint â€” very high bandwidth but expensive â€” used in some premium Angola deep-water applications

---

### 5. Surface Acquisition System

The [MWD](../glossary.md)/LWD field engineer manages the surface data acquisition system:

**SLB:** IDEAL (Integrated Drilling Environment for Automated Logging) / WellWatcher
**Halliburton:** QMAX software
**Baker Hughes:** FirstView

Responsibilities:
- Set up sensors and configure data channels before spudding
- Monitor data quality in real-time during drilling
- Alert drilling engineer / operator representative of anomalies
- Download memory data when tools return to surface
- Transmit [LWD](../glossary.md) log to operator base office (via WITSML standard protocol)

---

### 6. Tool Failure and Troubleshooting

A significant part of the MWD/LWD field engineer's job is diagnosing and troubleshooting tool issues in real time:

| Problem | Likely cause | Action |
|---|---|---|
| No signal at surface | Mud pulse lost (lost circulation, foam in mud) | Check shakers for lost circ; check defoamer |
| Erratic GR | Tool shock/vibration | Reduce RPM or WOB; check vibration |
| Negative porosity values | Gas effect not corrected; tool standoff | Apply gas-effect correction scheme |
| High vibration alarms | Bit bounce or [BHA](../glossary.md) whirl | Reduce WOB, change RPM |
| Tool fails to survey | Magnetic interference (casing, fish) | Use gyro survey instead |

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Learn the difference between [MWD](../glossary.md) and LWD sensors
- [ ] Understand mud pulse telemetry: how data gets to surface
- [ ] Know the main tool strings for [SLB](../../data/company-directory/slb.md), [Halliburton](../../data/company-directory/halliburton.md), and [Baker Hughes](../../data/company-directory/bakerhughes.md)
- [ ] Read a standard [LWD](../glossary.md) real-time data display (WDP, GR, resistivity, density)

### Intermediate (2â€“5 months)
- [ ] Understand all [MWD](../glossary.md) sensors and their measurements (APWD, vibration, WOB, torque)
- [ ] Learn how formation pressure while drilling (FPWD) works and what it tells you
- [ ] Study a real-time [LWD](../glossary.md) display from a geosteering job and interpret the formation changes
- [ ] Understand surface acquisition setup and WITSML data transmission

### Advanced (5â€“12 months)
- [ ] IADC Wellbore Positioning Technical Section (WPTS) â€” survey calculations and uncertainty
- [ ] Study [SLB](../../data/company-directory/slb.md) ADN/ARC full tool specifications (publicly available)
- [ ] Learn advanced telemetry: EM telemetry, Wired Drill Pipe operation
- [ ] Practice tool failure diagnostics on historical rig data sets

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **[SLB](../../data/company-directory/slb.md) Oilfield Review articles on MWD/LWD** | Excellent technical depth, free | Free â€” slb.com |
| **[Halliburton](../../data/company-directory/halliburton.md) Technical Papers on Sperry tools** | Practical tool descriptions | Free via Halliburton website |
| **SPE 49018 "[LWD](../glossary.md) data acquisition and quality control"** | Classic paper | Free with SPE membership |
| **Petrowiki â€” [MWD](../glossary.md)/LWD page** | Good overview | Free |
| **[Baker Hughes](../../data/company-directory/bakerhughes.md) BHG Navigator product page** | Tool specifications | Free |

---

## Practice Questions

1. What is the difference between [MWD](../glossary.md) and LWD in terms of what they measure?
2. Explain how mud pulse telemetry transmits data to surface. What are its limitations in ultra-deep water?
3. You are [MWD](../glossary.md) engineer on a deepwater rig in Angola. You lose your mud pulse signal. List three possible causes.
4. An [LWD](../glossary.md) run shows high GR (90 API) followed by low GR (20 API) followed by high resistivity. What formation sequence does this suggest?
5. Why is real-time APWD (Annular Pressure While Drilling) critical for [well control](01-well-control.md) in Angola deepwater?

---

## Related Skills

- [04 â€” Formation Evaluation](04-formation-evaluation.md) (what [LWD](../glossary.md) data means)
- [05 â€” Directional Drilling](05-directional-drilling.md) ([MWD](../glossary.md) provides the directional surveys)
- [02 â€” Drilling Fundamentals](02-drilling-fundamentals.md) ([BHA](../glossary.md) design, integration of tools)
- [01 â€” Well Control](01-well-control.md) (APWD is a real-time kick detection tool)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” MWD** | Free reference | Free | [petrowiki.spe.org/Measurement_while_drilling_(MWD)](https://petrowiki.spe.org/Measurement_while_drilling_(MWD)) |
| **PetroWiki â€” LWD** | Free reference | Free | [petrowiki.spe.org/Logging_while_drilling_(LWD)](https://petrowiki.spe.org/Logging_while_drilling_(LWD)) |
| **SLB Learning â€” Downhole Tools** | Free student modules | Free | [learn.slb.com](https://learn.slb.com) |
| **SLB / Halliburton / Baker Hughes FET programs** | Company training (best depth) | Employer-funded | [careers.slb.com](https://careers.slb.com) Â· [jobs.halliburton.com](https://jobs.halliburton.com) Â· [careers.bakerhughes.com](https://careers.bakerhughes.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

