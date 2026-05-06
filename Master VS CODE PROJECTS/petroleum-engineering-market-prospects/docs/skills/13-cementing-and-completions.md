# Skill 13 â€” Cementing & Completions

> **Applies to:** Completions Engineer, Drilling Engineer, Well Intervention Engineer, Wireline Engineer
> **Offshore relevance:** Completing a deepwater Angola well costs $40â€“80M â€” the cementing and completion design determines whether that well produces effectively for 15â€“25 years

---

## What Is This Skill?

Cementing is the process of placing cement between the casing and the formation wall to provide zonal isolation, prevent fluid migration between formations, and structurally support the casing. Well completions refers to everything done after the reservoir is drilled to bring the well into production: perforating the reservoir, installing production tubing, safety valves, and downhole equipment. Together, cementing and completions define the "finished" well that will be handed to the production team.

---

## Why It Matters Offshore

In Angola's deepwater turbidite reservoirs:
- Wells cost $40â€“80M to drill and complete â€” every decision has massive financial consequence
- Deepwater wells have multiple challenges: narrow pore-pressure/fracture-gradient windows, high temperature/pressure (HPHT), unstable formations, and reactive shales
- Completions in angular turbidite sands often require **sand control** (gravel packs or screens) to prevent sand production that destroys ESP pumps and surface equipment
- A poor cement job = sustained annular pressure, which is both a safety risk and a regulatory compliance issue in Angola under ANPG standards

---

## Key Concepts to Master

### 1. Primary Cementing

Primary cementing is placing cement behind casing as it is run into the well. This is the most critical cementing operation.

#### Why Cement?
- **Zonal isolation:** Prevent flow between formations (e.g., saltwater zone communicating with oil zone)
- **Structural support:** Bond casing to formation â€” resists axial and lateral loads
- **Wellbore integrity:** Seal annulus to prevent pressure from migrating to surface
- **Corrosion protection:** Cement protects steel casing from formation brines

#### Cement Placement Sequence

```
1. Casing run to target depth
2. Plug landing collar is landed with a bottom wiper plug
3. Cement slurry mixed and pumped down the casing
4. Wiper plug separates cement from drilling fluid
5. Top wiper plug is released, follows cement down
6. Cement exits through float shoe at casing bottom
7. Cement flows UP the annulus (between casing and formation)
8. Top wiper plug lands on plug landing collar â†’ bump pressure â†’ cement placement complete
9. Wait on Cement (WOC): cement sets, develops compressive strength
```

**Float equipment:**
- **Float shoe:** One-way valve at bottom of casing â€” allows cement to flow out but prevents backflow when pumping stops
- **Float collar:** Secondary check valve above float shoe
- **Centralizers:** Keep casing centered in borehole to ensure uniform cement fill

---

### 2. Cement Slurry Design

**Base components:**
- **Portland cement (API Class G or H):** Standard offshore cement
- **Freshwater or seawater mix fluid**
- **Additives** to modify properties

#### Key Cement Properties

| Property | Measurement | Offshore target range |
|---|---|---|
| **Density** | lbs/gal or ppg | 14.0â€“18.0 ppg (varies by design) |
| **Thickening time** | Hours until 70 BC (Bearden Consistency) | >1.5Ã— placement time (safety factor) |
| **Compressive strength** | psi at 24 hr | >500 psi before running next casing |
| **Free water** | % separated fluid | <2% â€” free water causes channels |
| **Fluid loss** | mL/30 min | <50 mL/30 min for reservoir sections |

#### Common Cement Additives

| Additive | Purpose | Example |
|---|---|---|
| **Accelerators** | Speed up setting time | Calcium chloride, NaCl (small amounts) |
| **Retarders** | Slow setting (more time for placement) | AMPS-based polymer; used in HPHT Angola wells |
| **Lightweight extenders** | Reduce slurry density (prevents fracturing) | Perlite, sodium silicate, foam cement |
| **Heavyweight additives** | Increase density | Barite, hematite, ilmenite |
| **Fluid loss control** | Prevent cement filtrate entering formation | AMPS polymers, HPMC |
| **Anti-channeling / spacers** | Ensure good mud removal before cement | Turbulent-flow spacer |

---

### 3. Cement Evaluation Logging

After WOC, a cement bond log (CBL) is run on wireline to evaluate cement quality before proceeding.

#### Cement Bond Log (CBL) / Variable Density Log (VDL)

| Log | What it measures | Good cement signature |
|---|---|---|
| **CBL (amplitude)** | Attenuation of acoustic signal between casing and tool â€” bonded cement = signal attenuated | Low amplitude (near zero) = good bond |
| **VDL (variable density)** | Shows formation arrivals + casing arrivals as variable intensity | Formation arrivals visible = cement bonded to formation |
| **USIT / Flexus (ultrasonic)** | Acoustic impedance of annular fill | High impedance = solid fill |

**[SLB](../../data/company-directory/slb.md) CemNET / [Halliburton](../../data/company-directory/halliburton.md) SonicScope / BHI SoundTrak** are the main CBL/USIT tools used in Angola. The decision to squeeze-cement a poor section requires a CBL log showing a channel.

---

### 4. Well Completion Design

After drilling into the reservoir, the completion converts the well from a "hole in the ground" to a producing well.

#### 4.1 Completion Types

| Type | Description | When used in Angola |
|---|---|---|
| **Open hole completion** | No perforations â€” well produces through open reservoir section | Competent carbonate or consolidated sandstone (rare in Angola) |
| **Cased and perforated** | Casing cemented through reservoir; perforations made by guns | Most Angola completions |
| **Slotted liner** | Liner with pre-cut slots; run open hole but no cement behind | Some cases |
| **Pre-packed screens** | Screens with gravel pre-packed; run in open hole | Sand control in unconsolidated sands |

---

### 5. Perforating

After the casing is cemented into the reservoir, perforations are shot through the casing and cement to create flow channels into the formation.

#### Perforating Systems

| System | How deployed | Angola use |
|---|---|---|
| **TCP (Tubing Conveyed Perforating)** | Perforating guns run on production tubing; fired at end of completion | Most common offshore â€” large guns, multiple zones |
| **Wireline guns** | Guns run on electrical wireline | Smaller diameter; used for well interventions |

#### Key Perforating Parameters

| Parameter | Effect |
|---|---|
| **Shot density** (shots per foot, SPF) | More shots = more flow area; typical 4â€“12 SPF |
| **Phasing** | Angle between shots (0Â°, 60Â°, 90Â°, 120Â°, 180Â°) |
| **Penetration depth** | How deep into formation the shaped charge perforates |
| **Perforation diameter** | Affects flow area |

**Underbalanced perforating:** When bottomhole pressure is below reservoir pressure at the time of perforating, formation fluids immediately flow into the wellbore and clean the perforation tunnel. Preferred method for Angola turbidite sandstones.

---

### 6. Sand Control

Angola turbidite sandstones are often **unconsolidated** â€” the sand grains are not cemented together and will flow into the well with the oil, eventually destroying the ESP and blocking the wellbore.

#### Sand Control Methods

| Method | How it works | Angola application |
|---|---|---|
| **Gravel Pack (GP)** | Gravel (engineered grain size) packed in annulus between screen and formation; blocks sand while allowing fluid | Most common for shallow, moderate-rate Angola producers |
| **Frac Pack (FP)** | Hydraulic fracturing + gravel packing simultaneously; creates high-permeability fracture filled with gravel | High-rate Angola wells; combines well stimulation with sand control |
| **Standalone Screen (SAS)** | Screen only â€” no gravel; relies on formation bridging | Lower risk tolerance â€” some Angola wells |
| **Inflow Control Devices (ICD)** | Devices on screen that equalize inflow along horizontal well â€” not sand control alone | Often combined with screens |

**Gravel pack sizing:** Gravel size selected to bridge formation sand (Saucier's rule: D50 gravel = 5â€“6 Ã— D50 formation sand).

---

### 7. Completion String Equipment

A typical Angola deepwater completion string (bottom to top):

```
[Bottom]
  Packer (production packer â€” set below perforations)
  â†‘
  Gravel pack / frac pack screen assembly
  â†‘
  Production liner (perforated or slotted)
  â†‘
  Tubing (3.5" or 4.5" production tubing)
  â†‘
  SCSSV (Surface Controlled Subsurface Safety Valve) ~100m BML
  â†‘
  Upper completion tubing
  â†‘
  Tubing hanger (in subsea XT)
[Top]
```

**Key equipment:**

| Item | Function |
|---|---|
| **Production packer** | Seals annulus between tubing and casing; directs all flow through tubing |
| **SCSSV** | Fail-safe-closed wireline-retrievable valve; shuts well on loss of hydraulic control |
| **Tubing hanger** | Lands and seals tubing in XT; provides both production and annulus conduits |
| **Nipple profiles** | Machined landing profiles in tubing for wireline plugs and flow control equipment |
| **Blast joint** | Thick-walled tubing opposite perforations â€” resists sand-erosion from inflowing fluid |

---

### 8. Completion Fluids

During completion operations, the wellbore is filled with a **clean, solids-free** fluid (completion fluid) to prevent formation damage.

| Fluid | Description | Angola use |
|---|---|---|
| **Calcium Bromide / CaBrâ‚‚** | Clear, solids-free; density to 14.2 ppg; compatible with most formations | Common Angola deepwater completion fluid |
| **Zinc Bromide (ZnBrâ‚‚)** | Very high density (up to 19.2 ppg); used for HPHT wells | HPHT Angola completions |
| **CaClâ‚‚ (brine)** | Lower density, lower cost; compatibility limited | Shallower wells |

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Understand the purpose of cementing: why we need zonal isolation
- [ ] Learn the primary cementing sequence end-to-end
- [ ] Know the 4 completion types: open hole, cased/perforated, gravel pack, frac pack
- [ ] Understand what the SCSSV does and how it is controlled

### Intermediate (2â€“5 months)
- [ ] Study gravel pack design â€” Saucier's rule, gravel size selection
- [ ] Learn CBL/VDL interpretation â€” what a good vs. bad cement bond looks like
- [ ] Study [SLB](../../data/company-directory/slb.md) and [Halliburton](../../data/company-directory/halliburton.md) completion product catalogs for Angola wells
- [ ] Read SPE papers on frac-pack completions in Angola turbidites

### Advanced (5â€“12 months)
- [ ] Study HPHT cementing challenges: density windows, thickening time management
- [ ] Learn production logging to evaluate completion performance
- [ ] Study multilateral well completions (TAML levels 1â€“4)
- [ ] Learn completion design software: WellPlan ([Halliburton](../../data/company-directory/halliburton.md)) or Landmark

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **API Spec 10A: Specification for Cements** | API cement standard | Paid |
| **[SLB](../../data/company-directory/slb.md) Cementing Manual ([Schlumberger](../../data/company-directory/slb.md))** | Comprehensive cementing guide | Request via SLB.com |
| **[Halliburton](../../data/company-directory/halliburton.md) Red Book (Cementing)** | [Halliburton](../../data/company-directory/halliburton.md)'s cementing reference | Industry standard; request via HAL |
| **SPE papers "gravel pack Angola"** | Real case studies | SPE membership |
| **[TotalEnergies](../../data/company-directory/totalenergies.md) completions papers (Girassol, Dalia)** | Angola-specific | SPE OnePetro |
| **"Well Completion Design" â€” Jonathan Bellarby (Elsevier)** | Textbook | Paid |

---

## Practice Questions

1. Why is centralizing the casing critical for achieving a good primary cement job?
2. What is a "channeling" defect in a cement job? How is it identified? How is it remediated?
3. You are completing a well in an unconsolidated turbidite formation at 2,000m water depth in Angola. What sand control method would you recommend and why?
4. What is the purpose of the SCSSV in a deepwater Angola completion? At what depth is it typically set?
5. The CBL log shows a 15m interval of poor cement bond behind 9 5/8" production casing, directly above the reservoir. What is the recommended action and why?

---

## Related Skills

- [01 â€” Well Control](01-well-control.md) (packer and SCSSV are completion barriers; [well control](01-well-control.md) events during completion)
- [11 â€” Subsea Systems](11-subsea-systems.md) (subsea XT sits on top of the completion tubing hanger)
- [09 â€” Artificial Lift](09-artificial-lift.md) (ESP is the upper completion in Angola deepwater producers)
- [15 â€” Well Integrity](15-well-integrity.md) (completion is part of the barrier envelope)
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (this file)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Well Completions** | Free reference | Free | [petrowiki.spe.org/Well_completions](https://petrowiki.spe.org/Well_completions) |
| **PetroWiki â€” Cementing** | Free reference | Free | [petrowiki.spe.org/Cementing](https://petrowiki.spe.org/Cementing) |
| **Well Completion Design** (Bellarby) | Textbook | ~$100 | [Elsevier](https://www.elsevier.com) |
| **Oilwell Cement and Cementing** (Nelson & Guillot) | Textbook | ~$80 | [SPE Bookstore](https://store.spe.org) |
| **Halliburton / Baker Hughes / SLB trainee programs** | Company training | Employer-funded | [jobs.halliburton.com](https://jobs.halliburton.com) Â· [careers.bakerhughes.com](https://careers.bakerhughes.com) Â· [careers.slb.com](https://careers.slb.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

