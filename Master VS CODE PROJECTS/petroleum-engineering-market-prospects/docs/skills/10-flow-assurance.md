# Skill 10 â€” Flow Assurance

> **Applies to:** Flow Assurance Engineer, Facilities Engineer, Process Engineer, Subsea Engineer
> **Offshore relevance:** Critical for Angola's ultra-deepwater subsea tiebacks â€” the subsea flowlines from well to [FPSO](../glossary.md) are where most flow assurance problems occur

---

## What Is This Skill?

Flow assurance is the engineering discipline concerned with ensuring that hydrocarbons flow reliably from the reservoir, through well tubing, subsea flowlines, risers, and up to the [FPSO](../glossary.md) â€” without obstruction, blockage, or uncontrolled pressure. The name comes from the challenge: in deepwater environments, conditions are favorable for the formation of solid deposits and flow irregularities that can block or damage the system entirely.

---

## Why It Matters Offshore

Angola's ultra-deepwater environment (1,000â€“2,000m water depth) presents extreme challenges:
- **Seabed temperatures** of 4Â°C (near freezing)
- **High pressures** (150â€“350 bar at the seafloor)
- Long subsea tiebacks â€” some flowlines on Block 32 are 25â€“35km long
- These conditions of **low temperature + high pressure** are exactly the conditions that form **gas hydrates** â€” ice-like plugs that can completely block a flowline within hours

A single hydrate plug in Angola can cost $5â€“50M to remediate and cause months of production loss. Flow assurance engineers prevent this.

---

## Key Concepts to Master

### 1. The Four Main Flow Assurance Threats

#### 1.1 Gas Hydrates

**What they are:** Crystalline solids (clathrates) formed when water molecules form a cage structure around small hydrocarbon molecules (methane, ethane, propane) under high pressure and low temperature.

**Formation conditions:** Follow a hydrate stability curve (phase envelope):
- High pressure + Low temperature = Hydrate formation zone
- Angola seabed (150â€“350 bar, 4Â°C) is INSIDE the hydrate stability zone

**Prevention methods:**

| Method | How it works | Application |
|---|---|---|
| **MEG injection (Monoethylene Glycol)** | Depresses the hydrate formation temperature (thermodynamic inhibitor) | Most common in Angola deepwater â€” injected at subsea wellhead |
| **Methanol injection** | Same as MEG but lighter, more volatile | Emergency/well testing |
| **Electrical heat tracing (EHT)** | Electric cables on flowline maintain temperature above hydrate point | Expensive; used for critical short sections |
| **Pipe-in-pipe insulation** | Thick insulation on flowline slows heat loss during shutdown | Most Angola tiebacks use PiP or DEH |
| **Direct Electric Heating (DEH)** | Alternating current through flowline itself generates heat | Used on some [TotalEnergies](../../data/company-directory/totalenergies.md) Angola tiebacks |

**MEG regeneration:** On the [FPSO](../glossary.md), lean MEG is injected downhole; rich MEG (diluted with produced water) returns and is regenerated in the MEG regeneration plant on the [FPSO](../glossary.md) â†’ recycled. This is a major FPSO process system.

---

#### 1.2 Wax (Paraffin)

**What it is:** Heavier paraffin hydrocarbons (C17+) that are dissolved in warm crude oil crystallize and deposit on pipe walls as the oil cools below the **Wax Appearance Temperature (WAT)**, also called Cloud Point.

**Angola crude characteristic:** Most Angola crude oils have high pour points (some above 35Â°C). If cooled, the crude solidifies and cannot be pumped.

**Prevention methods:**
- **Pour Point Depressant (PPD) / Wax Crystal Modifier:** Chemical injected at wellhead that modifies wax crystal structure, keeping oil pumpable to lower temperatures
- **Pigging:** Physical scraper (pig) pushed through flowline to mechanically clean wax deposits
- **Insulation:** Keep crude warm during transit
- **Regular pigging programs:** Angola FPSOs run pigging operations weekly to monthly

---

#### 1.3 Asphaltenes

**What they are:** Heavy, polar, condensed aromatic compounds naturally dissolved in crude oil. They precipitate as solids when:
- Pressure drops near the wellbore (around bubble point pressure)
- Crude mixes with incompatible fluids
- Temperature changes

**Consequences:** Asphaltene deposition in perforations, tubing, valves, and flowlines â€” extremely difficult to remove (unlike scale, which dissolves in acid).

**Prevention:**
- **Asphaltene dispersants:** Chemical injection to keep asphaltenes in suspension
- **ESP operating conditions:** Avoid operating below bubble point pressure in ESP intake
- **Solvent treatment:** Xylene squeeze (with significant SSHE precautions) to dissolve deposits

---

#### 1.4 Scale

**What it is:** Inorganic mineral deposits formed when ions in produced water combine:
- **Calcium Carbonate (CaCOâ‚ƒ):** Most common; forms when COâ‚‚ evolves as pressure drops
- **Barium Sulfate (BaSOâ‚„):** Very hard scale, insoluble in acid â€” forms when incompatible waters mix
- **Strontium Sulfate (SrSOâ‚„):** Similar to BaSOâ‚„

**Consequences:** Blocks perforations, tubing, wellhead valves, ESPs, manifolds

**Prevention:**
- **Scale inhibitor injection:** Standard practice â€” injected at wellhead injection points
- **Squeeze treatments:** Pump scale inhibitor into formation for slow release
- **Waterflood compatibility:** Design injected water to be compatible with formation water (avoid mixing BaSOâ‚„-forming ions)

---

### 2. Slugging

**What it is:** Alternating flow of gas and liquid in two-phase pipeline flow. Under certain conditions (low flow rate, inclined pipe, riser), the gas and liquid separate and create large "slugs" of liquid followed by large gas surges.

**Types:**
- **Hydrodynamic slugging:** Occurs in horizontal/slightly inclined pipes at certain flow velocities
- **Riser slugging (severe slugging / terrain slugging):** Liquid accumulates at the base of the riser (seabed low point) then periodically surges â†’ gas kicks â†’ alternating pressure on [FPSO](../glossary.md) separators

**Consequences:**
- Overflows separator â€” trips process, causes flaring, production loss
- Pressure surges damage equipment
- Gas blows through separator affecting downstream processes

**Mitigation:**
- **Slug catchers:** Large buffer vessels on FPSO to absorb slugs
- **Riser base gas injection:** Inject gas at riser base to keep flow continuous
- **Flow rate optimization:** Keep above critical velocity
- **Topside slug control:** Use inlet chokes to dampen incoming slugs

---

### 3. Thermal Hydraulic Modeling

Flow assurance engineers use specialized software to model the thermohydraulics of subsea tiebacks:

| Software | Developer | What it does |
|---|---|---|
| **OLGA** | [SLB](../../data/company-directory/slb.md) | Industry standard transient multiphase flow simulator |
| **LedaFlow** | Kongsberg/TOTAL | Transient multiphase â€” used by [TotalEnergies](../../data/company-directory/totalenergies.md) |
| **PIPESIM** | [SLB](../../data/company-directory/slb.md) | Steady-state multiphase analysis |
| **HYSYS** | Aspentech | Process simulation including pipeline sections |

A flow assurance study for an Angola tieback involves:
1. Defining fluid PVT properties (from reservoir samples)
2. Building the flowline/riser geometry
3. Simulating: normal flow, cool-down, shutdown, restart
4. Identifying risk zones: where are hydrates most likely to form?
5. Designing chemical injection rates and insulation specifications

---

### 4. Shutdown and Restart Procedures â€” Critical Operations

**Planned shutdown:** Standard procedure â€” depressurize and displace flowlines with MEG or dead oil before the flowline cools â†’ no hydrate risk.

**Emergency shutdown (ESD):** Well/flowline shuts in suddenly without depressurization. The fluid pressure is maintained but temperature drops toward seabed temperature (4Â°C). If inside hydrate stability zone â†’ hydrates forming within hours.

**Angola restart procedures:** After any shutdown, the operator follows strict restart protocols:
- Slow pressure ramp-up
- MEG injection confirmed before opening wells
- Temperature monitoring at flowline outlets
- Choke management to prevent large slugs entering FPSO

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Understand the four main flow assurance risks: hydrates, wax, scale, asphaltenes
- [ ] Learn the hydrate phase envelope: pressure/temperature conditions for hydrate formation
- [ ] Understand why Angola deepwater tiebacks are particularly vulnerable (cold, deep, long distances)
- [ ] Know the basic chemical prevention methods for each threat

### Intermediate (2â€“5 months)
- [ ] Study PVT (Pressure-Volume-Temperature) fluid analysis â€” how crude oil properties are characterized
- [ ] Learn PIPESIM (steady-state) â€” free trial available from [SLB](../../data/company-directory/slb.md)
- [ ] Study slug flow: when does it occur, and how does it affect the [FPSO](../glossary.md)?
- [ ] Read [TotalEnergies](../../data/company-directory/totalenergies.md) technical papers on Angola tieback management

### Advanced (5â€“12 months)
- [ ] Master OLGA (get student license or attend training course)
- [ ] Study complete flow assurance design workflow for a new deepwater tieback
- [ ] Learn MEG regeneration system on the [FPSO](../glossary.md)
- [ ] Study Angola LNG associated gas flow assurance challenges

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **Guo, Song, Chacko, Cassidy â€” "Offshore Pipelines"** | Flow assurance chapter | Paid |
| **PIPESIM Student Edition ([SLB](../../data/company-directory/slb.md))** | Free | Via SLB.com |
| **SPE papers "flow assurance deepwater Angola"** | Real case studies | Free with SPE membership |
| **Bai & Bai "Subsea Engineering Handbook"** | Flow assurance chapter | Paid |
| **IFE OLGA user manual** | Technical reference | Via SINTEF/[SLB](../../data/company-directory/slb.md) |

---

## Practice Questions

1. Explain why a 2,000m deep subsea flowline in Angola is in the hydrate stability zone at normal operating conditions.
2. What is the difference between MEG and methanol as hydrate inhibitors? Why is MEG preferred for long-term Angola operations?
3. A flowline experiences severe riser slugging. Describe what the [FPSO](../glossary.md) operator sees and why it is dangerous.
4. What is WAT (Wax Appearance Temperature) and why does it matter for Angola crude with a high pour point?
5. You detect BaSOâ‚„ scale in the production tubing of an Angola well. Why is this harder to treat than CaCOâ‚ƒ scale?

---

## Related Skills

- [08 â€” FPSO Process Operations](08-fpso-process-operations.md) (slugs affect [FPSO](../glossary.md) separators; MEG regen is an FPSO system)
- [09 â€” Artificial Lift](09-artificial-lift.md) (scale and asphaltenes affect ESP performance)
- [11 â€” Subsea Systems](11-subsea-systems.md) (flowlines and risers are subsea infrastructure)
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (scale and hydrate inhibitor injection points are in the completion)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Flow Assurance** | Free reference | Free | [petrowiki.spe.org/Flow_assurance](https://petrowiki.spe.org/Flow_assurance) |
| **SPE papers on hydrate management** | Free with SPE student membership | ~$25/yr | [onepetro.org](https://onepetro.org) |
| **Flow Assurance for Production Operations** (Forrest) | Textbook | ~$100 | [Amazon](https://www.amazon.com) |
| **PetroSkills â€” Flow Assurance** | Paid course | $1,000â€“5,000 | [petroskills.com](https://www.petroskills.com) |
| **NExT â€” Flow Assurance short course** | Paid course | $1,000â€“5,000 | [next-training.net](https://www.next-training.net) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

