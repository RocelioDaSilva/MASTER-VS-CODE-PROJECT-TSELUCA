# Skill Tutorial 03 — FPSO Process Operations

> **Applies to:** Production engineers (CORE), HSE engineers (CORE), all tracks (awareness of the system they work on)
> **ISPTEC connection:** Sistemas de Produção Superfície, Sistemas Marítimos de Produção, Fenômenos de Transporte
> **Goal:** Understand every unit operation on an FPSO, the process flow from wellhead to export, key equipment, process safety concepts, and how to troubleshoot production problems.

---

## Part 1: The FPSO — Your Working Environment

An FPSO (Floating Production, Storage and Offloading unit) is simultaneously:
- An oil refinery (minus cracking/upgrading) — it processes raw wellstream into export crude
- A storage tank farm — it holds 1–2 million barrels of processed crude
- A production platform — it receives and manages production from 20–80 subsea wells
- A living facility — it houses 100–250 personnel

Angola's FPSOs are among the world's largest. The Kaombo Norte and Sul FPSOs (Block 32, TotalEnergies) can each process 115,000 bbl/day of crude. The Girassol FPSO (Block 17) processes up to 220,000 bbl/day.

---

## Part 2: The Complete Process Flow — From Well to Tanker

Understanding the complete process flow is the single most important thing a production engineer must know. Every optimization decision, every troubleshooting analysis starts with "where in the process flow is the problem?"

### Wellstream Composition

Raw wellstream coming from a subsea well is a mixture of:
- **Crude oil** (your product)
- **Associated gas** (methane, ethane, propane, heavier hydrocarbons)
- **Produced water** (formation water — saltwater)
- **Sand/solids** (in unconsolidated reservoirs — common in Angola)
- **CO2, H2S** (acid gases — present in some Angola reservoirs)
- **Heavy components** (wax, asphaltenes — can deposit in tubing and flowlines)

The FPSO's job is to separate and treat all of these.

### Complete Process Flow Diagram (text representation)

```
[Subsea Wells] ──flexible risers──► [FPSO Inlet]
                                         │
                               [SLUG CATCHER / INLET MANIFOLD]
                                  Remove slugs (large liquid/gas bursts)
                                         │
                               [HIGH PRESSURE (HP) SEPARATOR]
                                  Pressure: 30–60 bar
                                  Separates into: Gas / Oil / Water
                                    │         │         │
                               [HP GAS]  [HP OIL]  [HP WATER]
                                  │         │         │
                            [HP Compr]  [LP Sep]  [Prod Water Tx]
                                  │         │
                               [LP GAS]  [LP OIL]
                                  │         │
                            [LP Compr]  [Wash Vessel / Electrostatic Treater]
                                  │             Remove residual water from oil
                                  │                     │
                            [Fuel Gas System]     [CRUDE OIL STORAGE TANKS]
                            [Gas Lift Compressors]     (1–2 million bbl capacity)
                                                        │
                                               [EXPORT PUMPS]
                                                        │
                                               [EXPORT METERING]
                                        Fiscal measurement — every barrel accounted for
                                                        │
                                              [CRUDE OIL TANKER]
                                       (offloads every 3–7 days via CALM buoy)
```

---

## Part 3: Key Unit Operations — Deep Dive

### 3.1 Three-Phase Separator

The workhorse of FPSO process operations. Separates oil, gas, and water by exploiting:
1. **Density difference:** Water (SG ~1.03) sinks below oil (SG 0.8–0.9). Gas rises above oil.
2. **Retention time:** The fluid sits in the separator long enough for separation to occur (typically 3–10 minutes for crude oil/water separation)
3. **Velocity reduction:** Large vessel diameter slows the flow, allowing gravity separation

**Separator internals:**
- **Inlet device:** Breaks slug flow into dispersed droplets
- **Mist eliminator (demister):** Wire mesh or vane pack at the gas outlet — removes liquid droplets from the gas stream
- **Weir plate:** Controls the oil-water interface level
- **Vortex breaker:** Prevents gas carry-under at the liquid outlets

**Three-phase separator control:**
- **Gas pressure control:** Back-pressure control valve (BPCV) on the gas outlet. Maintains operating pressure.
- **Oil level control:** Level control valve on the oil outlet. Maintains the oil-water interface at the weir.
- **Water level control:** Level control valve on the water outlet. Maintains water level.

**What can go wrong:**
- **Oil carry-under with water:** If interface level is too high, oil overflows into water section. Produces oily water that's hard to treat.
- **Water carry-over with oil:** If interface level is too low, water dumps over the weir into the oil section. Increases BS&W.
- **High inlet temperature:** Reduces viscosity difference, makes separation easier (good). Also increases vapor pressure, can cause flashing.

### 3.2 Electrostatic Treater (Electrostatic Dehydrator)

After the separators, crude oil still contains 1–5% water as fine droplets suspended in oil (emulsion). The electrostatic treater breaks this emulsion by applying a high-voltage electric field (10,000–30,000 volts AC or DC) across the vessel.

**How it works:**
1. The electric field polarizes water droplets
2. Polarized droplets are attracted to each other and coalesce into larger droplets
3. Larger droplets settle faster (Stokes' Law: settling velocity ∝ droplet diameter²)
4. Water phase separates from oil and drains

**Target:** Produce export crude with **BS&W < 0.5%** (Basic Sediment and Water — the quality spec for oil tankers and contracts)

**Chemical injection here:** Demulsifier (emulsion breaker) is injected upstream to assist the electric field.

### 3.3 Gas Compression

Produced gas must be managed safely and economically. Uses on an FPSO:

1. **Fuel gas:** Runs the gas turbines that generate all electrical power on the FPSO. 80–150 MW power demand on a large FPSO.
2. **Gas lift:** Injected back down the production risers to lift oil (see production engineering tutorial)
3. **Gas injection:** Some Angola FPSOs inject gas back into the reservoir for pressure support (reinjection = higher recovery factor)
4. **Gas export:** Some blocks have gas export pipelines. Angola's LNG project (Angola LNG, Soyo) takes associated gas.
5. **Flaring (last resort):** Should be minimized per ANPG regulations

**Compression stages:** Gas is typically compressed in 2–3 stages (HP → LP → instrument air), with intercoolers between stages to manage temperature.

### 3.4 Produced Water Treatment

Every Angola FPSO produces large volumes of water along with oil (typical water cut on a mature FPSO: 30–70%). This water cannot be dumped overboard without treatment — regulatory limit is <30 mg/L oil in water per ANPG/OSPAR regulations.

**Treatment sequence:**
1. **Hydrocyclones:** Centrifugal separation — removes oil droplets > 20 microns
2. **Degasser:** Removes dissolved gas from produced water (gas carry-under from separators)
3. **Flotation cell:** Gas bubbles carry remaining oil droplets to the surface for skimming
4. **Polishing filters (some FPSOs):** Final removal of trace oil

**Monitoring:** Online oil-in-water analyzers in the overboard discharge. Alarms if oil-in-water exceeds threshold.

**Water injection (some FPSOs):** Instead of discharging treated water, it's injected back into the reservoir for pressure maintenance. Requires produced water injection (PWI) system with high-pressure pumps and injection risers.

### 3.5 Chemical Injection System

Angola's crude oil and reservoir conditions require multiple chemical injection programs on each FPSO:

| Chemical | Purpose | Where Injected |
|---|---|---|
| **Corrosion Inhibitor** | Protects carbon steel flowlines and risers | At subsea wellheads or manifolds |
| **Scale Inhibitor** | Prevents calcium carbonate/barium sulfate scale | At subsea wellheads |
| **Hydrate Inhibitor (MEG or MeOH)** | Prevents gas hydrate plug formation | Risers and flowlines (deepwater) |
| **Wax Inhibitor** | Prevents paraffin wax deposition | Flowlines at wellhead |
| **Asphaltene Inhibitor** | Prevents asphaltene precipitation | Wellheads and tubing |
| **Demulsifier** | Breaks oil-water emulsions | Inlet manifold / separator inlet |
| **Biocide** | Kills sulfate-reducing bacteria (corrosion, H2S generation) | Water injection system |
| **Anti-foam** | Prevents foaming in separators | Separator vessels |

---

## Part 4: Process Safety Fundamentals

### Major Accident Hazards on an FPSO

**Fire and Explosion:**
- Hydrocarbon releases igniting in confined modules
- FPSO process modules are ventilated but flammable gas can accumulate
- Hot work (welding) near hydrocarbon systems is a major ignition risk

**Hydrocarbon Release:**
- Flange or valve leaks
- Vessel overpressure causing relief valve discharge
- Pipeline rupture from corrosion or mechanical damage

**Loss of Mooring:**
- FPSO breaks free from moorings in bad weather → potential well disconnect and oil spill

**Fire on the Flare Stack:**
- Flare tip failure or backfire can cause structural issues

### Safety Critical Systems

**Emergency Shutdown System (ESD):**
The ESD system automatically shuts down the production process in a defined sequence if dangerous conditions are detected:
- Gas/fire detection → ESD activation
- ESD-1: Wellhead shutdown (closes SCSSV in wells)
- ESD-2: FPSO process shutdown (closes all process isolation valves)
- ESD-3: Utility shutdown
- **Total Release (TR):** All hazardous systems shut, ventilation on maximum, prepare for evacuation

**Fire and Gas (F&G) Detection:**
- Flame detectors (UV/IR) in process areas
- Heat detectors in accommodation and enclosed areas
- Gas detectors (catalytic bead or IR beam) in process modules

**Deluge Systems:**
Water deluge (sprinkler equivalent) for process module fire suppression and FPSO cooling during fire events.

---

## Part 5: FPSO Performance Metrics

As a production engineer, these are the numbers you live by:

| KPI | Definition | Typical Target | Angola Context |
|-----|-----------|---------------|---------------|
| **Production Efficiency (PE)** | Actual production / Maximum potential production | > 90% | Lost production from shutdowns, wells offline |
| **FPSO Uptime** | Hours in full production / total hours | > 95% | Planned maintenance windows, weather downtime |
| **BS&W (Basic Sediment and Water)** | % water + solids in export crude | < 0.5% | Electrostatic treater performance |
| **Export GOR** | Gas exported (scf) / oil exported (bbl) | Contractual limit | Determines gas monetisation revenue |
| **Water Cut (WC)** | % water in total liquid production | Monitor vs forecast | Rising WC indicates water breakthrough |
| **Oil Rate (bbl/day)** | Net oil exported per day | Plateau target | Compare to production forecast |
| **Gas Utilisation** | % of produced gas used productively (lift, fuel, export) vs flared | > 98% | ANPG zero-flaring target |

---

## Part 6: Well Testing on an FPSO

### Why Well Test?

The FPSO export meter measures one combined crude oil production number from all wells. To know how much each individual well contributes, wells are tested one at a time through the **test separator**.

**Test separator:** A dedicated three-phase separator on the FPSO (typically smaller than the main separators). Each well can be routed to the test separator by opening a valve on the subsea test header manifold.

**What you measure during a well test:**
- **Gross rate** (liquid + gas = total wellstream)
- **Oil rate** (from test separator oil metering)
- **Water rate** (from test separator water measurement)
- **GOR** (gas rate / oil rate)
- **Water cut** (water rate / liquid rate)

**Test duration:** Typically 8–24 hours per well for a stable flow test. Start of test: let well stabilize after routing to test separator (clear slug from flowline, reach steady state). End of test: when rates are stable for >2 hours.

### Allocation Factor Method

After each well test, the individual well rates are used to calculate **allocation factors** — what fraction of the FPSO total production to assign to each well:

$$AF_{well-i} = \frac{q_{oil,i}^{test}}{q_{oil,total}^{FPSO}}$$

Between tests, FPSO production is allocated to each well using:
$$q_{well-i,allocated} = AF_{well-i} \times q_{oil,total}^{FPSO,daily}$$

**Angola ANPG requirement:** Each well must be tested regularly (typically quarterly to monthly for flowing wells). ANPG uses these test data for production reporting and royalty calculation. The Field Allocation Procedure (FAP) is an agreed document between ANPG and the operator.

---

## Part 7: Production Troubleshooting on the FPSO

The production engineer's role includes diagnosing why production is below target. The following workflow applies:

### Step 1: Is the Problem Reservoir, Wells, or Topside?

```
FPSO oil rate < target
        │
        ├── ALL wells below rate? → Topside bottleneck or reservoir pressure depletion
        │
        ├── SINGLE well below rate? → Well problem (scale, hydrate, tubing leak, choke)
        │
        └── Rising water cut on specific well? → Water breakthrough from injector or aquifer
```

### Step 2: Well-Level Diagnosis

**Declining well rate with no pressure change:**
- Test well PI: $PI = q_{test} / (P_{res} - P_{wf,test})$
- If PI has dropped → near-wellbore damage (scale, asphaltene, fines)
- Action: Acid squeeze or solvent treatment

**Declining well rate WITH pressure decline:**
- Reservoir depletion. Pressure support from water injection may be insufficient.
- Action: Check water injection performance. Recommend infill well or pressure maintenance review.

**High and rising wellhead pressure:**
- Possible flowline restriction (wax plug, hydrate partial plug)
- Action: Increase chemical injection, check flowline temperature, pipeline pigging

**Low separator pressure despite high wellhead pressure:**
- High pressure drop in flowline/riser. Possible partial blockage or severe slugging.
- Action: Flow assurance team diagnosis. Consider pigging, cleaning pig.

**Excessive gas-oil ratio:**
- Reservoir pressure falling below bubble point? (Free gas in reservoir)
- Gas coning from gas cap?
- Action: Monitor reservoir pressure, review well completion (perforate above GOC?)

### Step 3: Process-Level Diagnosis

**High BS&W in export crude:**
- Electrostatic treater malfunctioning (low voltage, electrode fouling)
- Demulsifier underinjected or wrong formulation
- Action: Increase demulsifier, verify treater voltage, contact chemical vendor for product optimization

**High oil-in-water discharge:**
- Hydrocyclone wear or wrong design
- Flotation cell underperforming
- Action: Check hydrocyclone apex, test flotation gas rate, increase biocide if bacteria suspected

---

## Part 8: Pigging Operations

A pig is a device inserted into a pipeline that travels through it, propelled by the flowing fluid.

**Types of pigs used on Angola FPSOs:**

| Pig Type | Purpose |
|----------|---------|
| **Foam pig (cleaning pig)** | Wax and deposit removal in flowlines |
| **Intelligent pig (ILI — In-Line Inspection)** | Detects corrosion, wall loss, dents, cracks in pipeline |
| **Gauge pig (caliper pig)** | Measures internal diameter — detects deformations |
| **Pressure test pig (bi-di pig)** | Seals line for pressure testing |

**Pigging sequence for a wax-laden Angola flowline:**
1. Pre-pig: Check pig launcher and receiver on FPSO and seabed PLEM. Confirm pig trap is clear.
2. Open pig launcher, insert foam pig, close and pressurize.
3. Open bypass valve — pig launches with the flow
4. Monitor pig tracking (acoustic sensors along the flowline give "pig squeals" at known positions)
5. Pig arrives at receiver on FPSO — pig catcher traps the pig
6. Inspect pig for wax deposits (how much came off = measure of wax buildup)
7. Record volumes of fluid received ahead of the pig

**Why regular pigging matters in Angola:** Seabed temperature (3–5°C) is near or below the WAT of many Angola crudes. Without regular pigging, wax builds up on pipe walls → reduces effective diameter → increases pressure drop → reduces production rate → eventually plugs the line.

---

## Exercises — FPSO Operations

**Exercise 1: BS&W Calculation**
An electrostatic treater receives 15,000 bbl/day of crude with inlet BS&W = 3.5%. The target export BS&W = 0.3%. The treater achieves 91% water removal efficiency. Is the target met?

**Exercise 2: Production Allocation**
An FPSO has 8 producing wells. During the last well test round:
- Well A: 3,200 bbl/day oil
- Well B: 4,100 bbl/day oil
- Well C: 2,800 bbl/day oil
- Wells D–H: 2,000 bbl/day each

The FPSO total export meter reads 25,000 bbl/day for the current month. Calculate the allocation factor for Well B and its allocated monthly production.

**Exercise 3: Well PI Decline**
A well on Block 17 was tested 6 months ago: oil rate = 4,500 bbl/day, reservoir pressure = 4,100 psi, flowing bottomhole pressure = 3,200 psi. Today's test: oil rate = 3,200 bbl/day, reservoir pressure = 4,050 psi, FBHP = 3,180 psi.
1. Calculate PI for each test period
2. Calculate the % decline in PI
3. What are the possible causes? What diagnostic tests would you run?

**Exercise 4: Gas Utilisation**
An FPSO produces 280,000 bbl/day of oil with an average GOR of 950 scf/bbl. Total gas produced = ? MMscf/day. Fuel gas consumption = 50 MMscf/day. Gas lift injection = 180 MMscf/day. Flared gas = 22 MMscf/day. Calculate gas utilisation efficiency. Is this compliant with ANPG zero-flaring target?

---

## Interview Questions — FPSO Operations

1. An Angola FPSO's oil rate has dropped 8% over 3 months. You have 24 well tests from last quarter and this quarter. What is your diagnostic process?
2. What is BS&W, why does it matter for oil export, and what process equipment controls it on an FPSO?
3. Explain the difference between the test separator and the main production separators. How does well allocation work?
4. What is the significance of the oil-in-water discharge limit of 30 mg/L in Angola and what treatment steps achieve it?
5. An FPSO is routinely flaring 30 MMscf/day of gas. What are the operational, economic, and regulatory implications?
6. What is a three-phase separator and what three variables do its level controllers manage?
7. Why is demulsifier chemical injection critical to achieving export BS&W < 0.5%?
8. Describe a lazy-wave riser and explain why it is preferred over a simple catenary riser for Angola FPSOs.

---

*Next: [04_Subsea_Systems_Tutorial.md](04_Subsea_Systems_Tutorial.md) | See also: [09_Production_Engineering_Tutorial.md](09_Production_Engineering_Tutorial.md)*

| Metric | Definition | Formula |
|---|---|---|
| **Production Efficiency (PE)** | Actual production vs maximum possible | PE = Actual / (Capacity × Time Available) |
| **BS&W** | Basic Sediment and Water content in export oil | % water + sediment by volume |
| **Water Cut** | Fraction of total liquid production that is water | WC = Qw / (Qw + Qo) |
| **GOR** | Gas-oil ratio | GOR = Qg (scf/day) / Qo (bbl/day) |
| **Total Fluid Rate** | Total liquid production | TFR = Qo + Qw |
| **Uptime** | % of time FPSO is in full production (not shut down) | Uptime = Available hours / Total hours |
| **NPT** | Non-Productive Time (planned maintenance + unplanned downtime) | NPT = Total time - Productive time |
| **Deferred Production** | Oil not produced due to a problem | (Lost rate × hours) |

---

## Part 6: Production Problem Solving Framework

When production drops unexpectedly on an FPSO, this is the diagnostic sequence:

**Step 1: Is it the well or the process?**
- Check individual well production rates (allocations via test separator or virtual metering)
- If all wells decline together → likely FPSO process problem or upstream (riser/manifold) issue
- If one well declines → likely wellbore issue

**Step 2: Process-side diagnosis**
- Check separator levels: is the oil-water interface at the right level?
- Check gas pressure: are the compressors running correctly? Any trips?
- Check export pump operation
- Check all critical control loops: are any in manual mode, bypassed, or in alarm?

**Step 3: Wellbore-side diagnosis**
- Compare flowing wellhead pressure (FWHP) to historical trend
- Check gas injection rates for gas lift wells
- Check ESP motor parameters for ESP wells
- Look at any recent maintenance or intervention on the affected well

**Step 4: Reservoir-side interpretation**
- Is the decline rate consistent with reservoir depletion? (expected long-term)
- Or is it a sharp, unexplained decline? (equipment or wellbore problem)
- Work with the reservoir engineer to confirm

---

## Part 7: Practice Exercises

**Exercise 1:** Draw from memory the complete FPSO process flow from subsea wells to oil export. Label every major piece of equipment. State the purpose of each.

**Exercise 2:** A separator has a feed of 15,000 bbl/day total liquid with 60% water cut and 500 scf/bbl GOR. Calculate:
1. Oil rate (bbl/day)
2. Water rate (bbl/day)
3. Gas rate (MMscfd)

**Exercise 3:** FPSO production drops by 3,000 bbl/day. All 8 producing wells show similar decline. The separator pressure has increased by 5 bar. Where do you look first? What is your diagnosis?

**Exercise 4:** Export crude BS&W is reading 2.8% — well above the 0.5% contract spec. Walk through the process changes you would make to reduce BS&W.

---

## Part 8: Where to Study Further

| Resource | Format | Notes |
|---|---|---|
| Petex IPM Suite (Prosper, GAP, MBAL) | Free student software | Most important production engineering tool |
| "Surface Production Operations" — Arnold & Stewart | Textbook | The definitive surface facility reference |
| FPSO operator technical manuals | Internal (from your company) | Best learning material once employed |
| TotalEnergies/SBM Offshore public reports | PDF | Describes FPSO designs and performance |
| SPE papers on Angola FPSO production optimization | Free via SPE membership | Search "Angola FPSO production" on OnePetro |
| Rigzone FPSO education section | Online | Free introductory explanations |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [docs/skills/08-fpso-process-operations.md](../../../docs/skills/08-fpso-process-operations.md)*  
*Where to learn: [PetroWiki](https://petrowiki.spe.org/Surface_facilities) | [HYSYS student](https://www.aspentech.com/en/university-program) | [Learning Resources](../../../docs/learning-resources.md)*
