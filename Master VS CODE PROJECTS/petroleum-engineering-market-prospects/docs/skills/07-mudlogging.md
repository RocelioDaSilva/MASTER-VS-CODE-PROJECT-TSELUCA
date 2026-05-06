# Skill 07 â€” Mudlogging & Cuttings Analysis

> **Applies to:** Mudlogger, Wellsite Geologist, Mudlogging Field Engineer
> **Entry level:** One of the most accessible offshore roles â€” can go offshore within 3â€“6 months of graduation. 28-day rotations on drillships and semis.
> **Companies:** Geoservices ([SLB](../../data/company-directory/slb.md)), Wellware, Integrated Exploration Systems (IES), Datalog ([Baker Hughes](../../data/company-directory/bakerhughes.md)), Geo-Log

---

## What Is This Skill?

Mudlogging is the continuous monitoring of drilling operations and formation data at the wellsite. The mudlogger is the first person to physically handle rock from a new formation â€” analyzing drill cuttings brought to surface by the drilling mud. They also monitor gas shows (hydrocarbons detected in the mud), drilling parameters, and wellbore behaviour in real time.

Mudloggers live on the rig in a self-contained instrumentation cabin (the mud logging unit / geological unit) and work 12-hour shifts throughout drilling operations. They are the eyes and ears of the geologist and reservoir engineer back in the office.

---

## Why It Matters Offshore

- On a $100M+ Angola deepwater well, every meter costs thousands of dollars. The mudlogger's real-time lithology calls and gas detection help the operator make critical decisions: set casing here, continue drilling, the reservoir has been reached.
- **Gas detection is a primary [well control](01-well-control.md) early-warning system.** Rising background gas or a sudden gas peak can signal an approaching influx â€” the mudlogger alerts the driller.
- In Angola's Block 17 and Block 32 wells, the turbidite sand reservoirs are often identified first by the mudlogger noting a change in lithology (from grey shale to buff-coloured clean sand) before the [MWD](../glossary.md) GR even confirms it.
- For a fresh graduate, mudlogging is the fastest path to offshore experience with the lowest barrier to entry. You need a geology background, not years of engineering experience.

---

## Key Concepts to Master

### 1. The Mud Logging Unit

A self-contained cabin (or module) on the rig containing:
- Gas detector sensors (flow line, trip tank)
- Computer workstations with real-time data acquisition
- Cuttings sample station (microscope, UV lamp, acids, reference sets)
- Connections to rig sensors (shakers, pit volume, pump strokes, hookload)

The mudlogger receives data from:
- Cuttings at the shale shakers
- Gas detectors in the mud return line
- Rig sensors (hookload, WOB, RPM, pump pressure, pit volume)
- Mud properties from the mud engineer

---

### 2. Lag Time Calculation

**Lag** is the time it takes for drill cuttings to travel from the bit (at depth) to the shale shaker (at surface). Because of this delay, cuttings you see at surface right now were actually cut at a shallower depth.

$$Lag \text{ (pump strokes)} = \frac{Annular Volume}{Pump Output}$$

$$Lag \text{ (minutes)} = \frac{Lag \text{ (strokes)}}{Pump Strokes Per Minute}$$

**Annular volume** = volume of space between drill string and hole/casing wall

$$AV \text{ (bbl)} = \frac{(D_h^2 - D_p^2) \times L}{1029.4}$$

Where Dh = hole diameter (in), Dp = pipe OD (in), L = depth interval (ft)

**Why it matters:** When you are at 3,000m depth and pumping at 400 spm with 5 bbl/stroke pump output and 250 bbl annular volume:
$$Lag = 250 / (400 Ã— 0.005) = 125 minutes$$

Cuttings arriving at surface now were cut over 2 hours ago. Your sample log must be depth-corrected for this lag.

---

### 3. Cuttings Analysis: Lithology Identification

Cuttings are collected at the shale shaker and washed. The mudlogger then examines them:

**Tools used:**
- **Hand lens / 10Ã— loupe** â€” gross identification
- **Binocular microscope** â€” detailed examination
- **UV lamp (ultraviolet light)** â€” fluorescence for oil detection
- **Acid (dilute HCl)** â€” carbonate identification (fizzes)
- **Streak plate** â€” mineral hardness

**Common lithologies and their cuttings characteristics:**

| Rock type | Color | Texture | UV fluorescence | Acid reaction |
|---|---|---|---|---|
| **Shale** | Grey, brown, black | Platy, micro-crystalline, slippery | None | None |
| **Sandstone (clean)** | White, buff, yellow | Granular, gritty, quartz grains visible | None (unless oil shows) | None |
| **Limestone** | White, grey, cream | Waxy, conchoidal fracture | None | Strong fizz |
| **Dolomite** | White, cream, pinkish | Rhombic crystals, powdery | None | Weak fizz (only when powdered) |
| **Anhydrite** | White, pinkish | Hard, crystalline | None | None |
| **Salt (Halite)** | Colourless/white | Cubic crystals, dissolves in water | None | None |

**For Angola turbidite reservoirs:**
- Shales: Grey, dark, soft, smear on glass
- Turbidite Sand: Light grey/buff, angular to sub-angular quartz, clean

---

### 4. Gas Detection

#### Gas Types Detected

| Gas | Significance |
|---|---|
| **Background gas (C1)** | Methane â€” always present at low levels from organic-rich shales |
| **Gas shows (C1 spike)** | Significant methane increase â€” possible gas sand encountered |
| **Wet gas (C2, C3, C4, C5)** | Heavier hydrocarbons â€” indicates oil-associated gas or wet gas reservoir |
| **Gas ratio (C1/C2+)** | Distinguishes gas condensate from oil reservoirs |
| **COâ‚‚** | Can be corrosive, safety hazard, non-hydrocarbon source |
| **Hâ‚‚S** | Highly toxic (immediately dangerous to life at >300 ppm) â€” safety alarm |

#### Gas Chromatograph

The gas detector feeds into a **gas chromatograph** that separates individual gas components (C1â€“C5+, COâ‚‚, Hâ‚‚S):
- **Total gas (TG):** Sum of all hydrocarbons detected
- **C1 (methane):** Dominant in dry gas wells
- **C2 (ethane), C3 (propane), iC4, nC4:** Heavier fractions â†’ oil reservoir signatures
- **Wetness ratio:** (C2+C3+C4+C5) / Total gas â€” increases in oil reservoirs

**Gas ratios used to characterize reservoir fluid:**

| Ratio | Indication |
|---|---|
| C1/C2+ > 50 | Dry gas |
| Wetness 5â€“20% | Gas condensate |
| Wetness 20â€“50% | Oil reservoir with gas cap |
| Wetness > 50% + C4/C5 present | Oil reservoir |

---

### 5. Oil Shows

When cuttings contain visible oil, the mudlogger records a "show":

| Show type | Description |
|---|---|
| **Oil stained** | Cuttings show brown/orange oil staining visible under white light |
| **Fluorescence (UV)** | Cuttings glow yellow/blue/orange under UV light â€” oil present |
| **Cut fluorescence** | Crush the cutting and add solvent â€” oil bleeds out and forms a halo (cut) |
| **Free oil** | Oil visible as droplets on cuttings or in drilling fluid |

**Oil show classification:**
- Trace â†’ Fair â†’ Good â†’ Very Good â†’ Excellent

---

### 6. The Mud Log (Composite Log)

The mudlogger compiles all data into a real-time **composite mud log** containing, in depth columns:

1. Lithological column (cuttings description)
2. Rate of Penetration (ROP) â€” formation hardness proxy  
3. Total gas (continuous curve)
4. Gas components (C1â€“C5)
5. Pit volume + pump pressure
6. Mud weight in/out
7. Any shows (oil, gas, water)
8. Drilling parameter annotations (drill breaks, connection gas, etc.)

This log is transmitted digitally to the operator's office in real time (via WITSML or CSV).

---

### 7. Connection Gas and Trip Gas

**Connection gas:** Every time a new joint of pipe is added (connection), the pump stops briefly. During this stop, gas from the formation diffuses into the near-wellbore mud. When pumping resumes, this shows as a gas peak at surface. Normal â€” but elevated connection gas suggests formation pressure close to mud weight.

**Trip gas:** Gas accumulated during a pipe trip. If substantially higher than connection gas â†’ potential kick situation.

**Monitoring these gas peaks is a primary safety task of the mudlogger.**

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Learn to identify 8 common lithologies from cuttings descriptions and photos
- [ ] Memorize lag time calculations â€” do 10 practical problems
- [ ] Understand gas chromatograph output: C1â€“C5, background gas, gas shows
- [ ] Study the standard mud log format â€” be able to read and annotate one

### Intermediate (2â€“5 months)
- [ ] Learn UV fluorescence classification (trace to excellent)
- [ ] Study gas ratios: how to distinguish oil wells from gas wells from cuttings gas
- [ ] Complete a field geology or core description course (AAPG short course)
- [ ] Practice reading composite mud logs from published well reports (search NLOG, USGS public well data)

### Advanced (5â€“12 months)
- [ ] Learn to identify Angola-specific lithologies (turbidite sequences, pre-salt carbonates)
- [ ] Study integration of [LWD](../glossary.md) GR with cuttings lithology for lithostratigraphic correlation
- [ ] Understand sequence stratigraphy basics (correlating Angola turbidite sandstones between wells)
- [ ] Get experience on a simulated wellsite or physical rock core workshop

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **AAPG Core Workshop notes** | Cuttings and core description best practices | Free via AAPG DL |
| **Geoservices Mudlogging Training Manual** | Industry standard | Available from [SLB](../../data/company-directory/slb.md) contacts |
| **Norwegian Petroleum Directorate well data** | Real mud logs from Norwegian wells â€” excellent practice | Free at factpages.npd.no |
| **NLOG (Netherlands well data)** | Free mud log and cutting data for practice | Free â€” nlog.nl |
| **Petrowiki â€” Mud Logging** | Comprehensive overview | Free |
| **YouTube: "Mudlogging for beginners"** | Visual introduction | Free |

---

## Practice Questions

1. A well is at 2,500m MD. Hole size is 12Â¼" (0.31m), DP OD is 5" (0.127m), pump output is 35 L/stroke, pump rate is 90 spm. Calculate the lag time in minutes.
2. You receive cuttings that are grey, platy, slightly waxy, and show no UV fluorescence. What is the likely lithology?
3. Gas detector shows a total gas jump from 250 units background to 3,200 units. C1 = 85%, C2 = 8%, C3 = 4%, C4 = 2%, C5 = 1%. Classify the likely formation fluid and action you take.
4. What is connection gas and what does elevated connection gas indicate?
5. Cuttings under UV lamp show a yellow-orange fluorescence with a spreading cut. What does this indicate? What is the show classification?

---

## Related Skills

- [04 â€” Formation Evaluation](04-formation-evaluation.md) (cuttings data integrates with logs)
- [03 â€” Drilling Fluids](03-drilling-fluids.md) (cuttings come out with the mud)
- [01 â€” Well Control](01-well-control.md) (gas detection = first-line [well control](01-well-control.md) warning)
- [02 â€” Drilling Fundamentals](02-drilling-fundamentals.md) (rig operations context)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Mudlogging** | Free reference | Free | [petrowiki.spe.org/Mudlogging](https://petrowiki.spe.org/Mudlogging) |
| **YouTube â€” Mudlogging tutorials** | Free video | Free | Search "mudlogging cuttings analysis" on YouTube |
| **Well Logging for Earth Scientists** (Ellis) | Textbook | ~$100 | Springer |
| **Geoservices (SLB) mudlogger training** | Company entry-level program | Employer-funded | [careers.slb.com](https://careers.slb.com) |
| **Baker Hughes Datalog training** | Company entry-level program | Employer-funded | [careers.bakerhughes.com](https://careers.bakerhughes.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

