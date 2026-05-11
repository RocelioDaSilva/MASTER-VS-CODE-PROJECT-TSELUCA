# Skill 04 â€” Formation Evaluation & Log Interpretation

> **Applies to:** Petrophysicist, [MWD](../glossary.md)/LWD Field Engineer, Mudlogger, Wellsite Geologist, Reservoir Engineer
> **Companies in Angola:** [SLB](../../data/company-directory/slb.md) (Wireline & Testing), [Halliburton](../../data/company-directory/halliburton.md) (Sperry/Wireline), [Baker Hughes](../../data/company-directory/bakerhughes.md) (Reservoir Characterization)

---

## What Is This Skill?

Formation evaluation is the process of measuring and interpreting rock and fluid properties in the subsurface â€” while drilling ([LWD](../glossary.md) logs) or after drilling (wireline logs). The goal is to determine: Is there oil or gas here? How much? How easily can it flow? Petrophysicists and log analysts are the people who answer these questions from sensor data.

This skill is central to the [MWD](../glossary.md)/LWD field engineer role (you run the tools that acquire the data) and the petrophysicist role (you interpret the data). Mudloggers also use basic log interpretation to identify reservoir zones in real time.

---

## Why It Matters Offshore

Every well drilled on Blocks 15, 17, or 32 in Angola generates thousands of feet of log data. This data determines:
- Whether to set production casing and complete the well (finding oil)
- Where to perforate (which intervals to produce from)
- How to design the completion (sand control, tubing size)
- The reserves estimate (how much oil the company booked)

A mistake in log interpretation can mean perforating the wrong zone, producing water instead of oil, or abandoning a productive zone. The financial consequences are enormous.

---

## Key Concepts to Master

### 1. Types of Well Logs

#### 1.1 Gamma Ray (GR) Log
**Measures:** Natural radioactivity of formations
**Tool:** Scintillation detector (Na-I crystal)
**Units:** API (American Petroleum Institute units)

| GR reading | Rock type |
|---|---|
| Low (0â€“30 API) | Clean reservoir (sandstone, carbonate) â€” low radioactivity |
| Medium (30â€“75 API) | Slightly shaly sand |
| High (75â€“150+ API) | Shale â€” high radioactivity from potassium, uranium, thorium |

**Primary use:** Identify sand vs. shale. Pick reservoir tops and bases. Calculate shale volume (Vsh).

$$V_{sh} = \frac{GR_{log} - GR_{clean}}{GR_{shale} - GR_{clean}}$$

---

#### 1.2 Resistivity Log
**Measures:** Electrical resistance of the formation
**Why it matters:** Oil and gas are non-conductive (high resistivity). Salty formation water is conductive (low resistivity).

| Resistivity | What it means |
|---|---|
| High (>50 Î©Â·m) | Likely hydrocarbon-bearing (non-conductive fluid) |
| Low (1â€“10 Î©Â·m) | Likely water-bearing or shale |

**Tool types:**
- **Deep resistivity** â€” reads far from wellbore (true formation)
- **Shallow resistivity** â€” reads near wellbore (invaded zone â€” mud filtrate has displaced formation fluid)
- **Micro-resistivity (MSFL)** â€” reads the flushed zone

**Use LLD (deep) for Rt (true resistivity), used in Archie's equation below.**

---

#### 1.3 Neutron Porosity Log
**Measures:** Hydrogen index of formation â†’ proxy for porosity
- High neutron reading = high hydrogen content = high porosity (or high fluid content)
- **Caution:** Gas reduces neutron reading (gas has low hydrogen density) â†’ "gas effect"
- **Units:** Porosity units (p.u.) on a limestone scale

---

#### 1.4 Density Log
**Measures:** Formation bulk density (Ïb, g/cc)
**Derives porosity:**

$$\phi_D = \frac{\rho_{matrix} - \rho_b}{\rho_{matrix} - \rho_{fluid}}$$

Typical matrix densities:
- Sandstone: 2.65 g/cc
- Limestone: 2.71 g/cc
- Dolomite: 2.87 g/cc

**Neutron-Density crossplot:** The key gas identification technique:
- Water zone / Oil zone: Neutron â‰ˆ Density porosity (curves track together)
- **Gas zone: Density porosity > Neutron porosity â€” the "gas crossover"** â€” one of the most important log signatures

---

#### 1.5 Sonic / Acoustic Log
**Measures:** Travel time of sound through formation (Î”t, microseconds/ft)
**Uses:**
- Porosity calculation (independent of fluid type if corrected)
- Compressive strength estimates (geomechanics)
- Seismic tie (synthetic seismogram) â€” converts log to seismic

---

#### 1.6 Photoelectric Effect (Pe) Log
**Measures:** Lithology factor independent of fluid
- Pe = 1.8: Sandstone
- Pe = 3.1: Limestone
- Pe = 3.5: Dolomite
- Pe = 2.7: Anhydrite

Used for lithology identification alongside GR and resistivity.

---

#### 1.7 NMR (Nuclear Magnetic Resonance) Log
**Advanced tool:** Directly measures pore size distribution, effective porosity (excluding clay-bound water), permeability estimate.
Used for complex reservoirs (carbonates, shaly sands) common in some Angola fields.

---

### 2. The Archie Equation â€” Foundation of Petrophysics

$$S_w = \left(\frac{a \cdot R_w}{\phi^m \cdot R_t}\right)^{1/n}$$

Where:
- Sw = water saturation (what fraction of pore space contains water) â†’ 1 - Sw = Hydrocarbon Saturation
- a = tortuosity factor (~1.0)
- Rw = formation water resistivity
- Ï† = porosity
- m = cementation exponent (~2.0 for clean sands)
- Rt = true formation resistivity (from deep resistivity log)
- n = saturation exponent (~2.0)

> **The core calculation:** From this equation, you determine whether a zone has oil/gas (low Sw) or water (high Sw â‰ˆ 1.0). Cut-off is typically Sw < 0.5â€“0.6 for a productive zone.

---

### 3. Quick Look Log Analysis Workflow

```
STEP 1: Identify lithology using GR
  â†’ Low GR = potential reservoir (sand/carbonate)
  â†’ High GR = shale (skip or calculate Vsh)

STEP 2: Estimate porosity using Density or Neutron-Density crossplot
  â†’ Apply lithology-appropriate matrix density

STEP 3: Check for gas (neutron-density crossover)

STEP 4: Read deep resistivity (Rt) in low-GR zones
  â†’ High Rt in porous zone â†’ likely hydrocarbon

STEP 5: Calculate Sw using Archie (need Rw from water samples or SP log)
  â†’ Sw < 50% â†’ likely oil/gas zone â€” mark for completion

STEP 6: Calculate net pay (sum of reservoir thickness with Sw < cutoff)
```

---

### 4. LWD vs. Wireline: Key Differences

| Aspect | LWD (Logging While Drilling) | Wireline |
|---|---|---|
| Timing | Real-time while drilling | After drilling (pulled out, tools run in) |
| Data quality | Good; slight borehole effect | Excellent â€” stable, uncombined wellbore |
| Application | Geosteering, early formation evaluation | Definitive log for reservoir analysis |
| Deepwater preference | [LWD](../glossary.md) essential (borehole conditions change with time) | Wireline run after [LWD](../glossary.md) confirms target |
| Tools | Integrated in [BHA](../glossary.md) ([MWD](../glossary.md)+LWD) | Separate tools on wireline cable |

---

### 5. Key Curves on a Log Display

Standard log display (track layout):

```
TRACK 1        TRACK 2                  TRACK 3
Depth (m)      GR / SP / Caliper        Neutron-Density (crossplot)
               Resistivity curves       
               (LLS, LLD, MSFL)         Sonic (DT)
```

**Caliper log:** Measures borehole diameter. Washout (borehole > bit size) can indicate soft shales or poor wellbore quality. Important for correcting log readings.

---

### 6. Angola-Specific Reservoir Context

Angola's deepwater reservoirs are predominantly:
- **Pre-salt carbonates** (new frontier blocks) â€” complex pore structures, require NMR and special Archie parameters
- **Post-salt turbidite sandstones** (Blocks 15, 17, 32) â€” cleaner, more straightforward Archie analysis
- **High porosity** (20â€“30%) turbidite sands are common in Angola
- **Good oil saturations** (Sw 20â€“40%) in productive zones â€” easy to identify on logs

---

## Study Roadmap

### Beginner (0â€“3 months)
- [ ] Draw a standard log display with GR, resistivity, and neutron-density tracks
- [ ] Identify sand vs. shale on a GR track
- [ ] Recognize gas crossover on neutron-density logs
- [ ] Understand what Archie's equation is trying to solve (Sw)

### Intermediate (3â€“6 months)
- [ ] Run complete quick-look analysis on practice log sets (available free online)
- [ ] Learn to use Interactive Petrophysics (IP) or Techlog (both have free trials)
- [ ] Calculate Sw, porosity, and net pay for practice wells
- [ ] Understand how [LWD](../glossary.md) data is used for real-time geosteering decisions

### Advanced (6â€“12 months)
- [ ] Study complex reservoir analysis: shaly sands (Waxman-Smits model), carbonates
- [ ] Core calibration: calibrating log-derived porosity against core plug measurements
- [ ] Understand borehole corrections for each tool (invasion, rugosity, mud type effects)
- [ ] Practice interpreting a full wireline log suite for an Angola-like reservoir

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **[Schlumberger](../../data/company-directory/slb.md) Log Interpretation Charts** | Industry standard quick-reference | Free â€” download from SLB.com |
| **Asquith & Gibson, "Basic Well Log Analysis"** | Classic textbook | Paid (AAPG) |
| **Petrowiki (SPE)** | Wikipedia-quality technical reference | Free |
| **IP Software (Interactive Petrophysics)** | Industry standard, free trial | Free trial via [Halliburton](../../data/company-directory/halliburton.md) |
| **Kansas Geological Survey well log database** | Practice log sets | Free â€” kgs.ku.edu |
| **Core Laboratories public resources** | Formation evaluation reference | Free |

---

## Practice Questions

1. A zone shows GR = 25 API, deep resistivity = 180 Î©Â·m, bulk density = 2.18 g/cc, neutron porosity = 0.28. What can you conclude about this zone?
2. Calculate Sw if Rt = 85 Î©Â·m, Ï† = 0.24, Rw = 0.05 Î©Â·m, a = 1, m = 2, n = 2.
3. What does "neutron-density crossover" mean and what causes it?
4. Why does a deepwater operator prefer [LWD](../glossary.md) data to wireline in the first hours after drilling a zone?
5. You see a high-resistivity zone from 2,450â€“2,480m with GR = 30 API but density porosity = 8%. Is this likely a hydrocarbon zone? Why or why not?

---

## Related Skills

- [05 â€” Directional Drilling](05-directional-drilling.md) ([LWD](../glossary.md) data used for geosteering)
- [06 â€” MWD/LWD Tools](06-mwd-lwd-tools.md) (the tools that acquire these logs)
- [07 â€” Mudlogging & Cuttings Analysis](07-mudlogging.md) (first-line formation evaluation)
- [14 â€” Reservoir Engineering Basics](14-reservoir-engineering.md) (log data feeds into reserves estimation)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Formation Evaluation** | Free reference | Free | [petrowiki.spe.org/Formation_evaluation](https://petrowiki.spe.org/Formation_evaluation) |
| **SLB Learning â€” Log Interpretation** | Free student | Free | [learn.slb.com](https://learn.slb.com) |
| **SLB Log Interpretation Chartbooks** | Free download | Free | [slb.com](https://www.slb.com) (search "chartbook") |
| **Petrel RE** | Software (student) | Free | [learn.slb.com](https://learn.slb.com) |
| **Well Logging for Earth Scientists** (Ellis) | Textbook | ~$100 | Springer |
| **The Geological Interpretation of Well Logs** (Rider) | Textbook | ~$80 | Technical libraries |
| **PetroSkills â€” Log Analysis** | Paid course | $1,000â€“3,000 | [petroskills.com](https://www.petroskills.com) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

