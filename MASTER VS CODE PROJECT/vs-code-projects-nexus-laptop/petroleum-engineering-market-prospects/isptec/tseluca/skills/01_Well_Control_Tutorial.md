# Skill Tutorial 01 — Well Control

> **Applies to:** Every offshore track. Well control is the most safety-critical skill in the petroleum industry. Understanding it is required before any offshore trip near a wellhead, regardless of your specialization.
> **ISPTEC connection:** Engenharia de Poços, Fluidos de Perfuração e Completação, Engenharia de Segurança
> **Certification target:** IWCF Level 1 (awareness) before graduation; IWCF Level 2 (operational) within 12 months of first job

---

## Part 1: What Is Well Control and Why Does It Exist?

A well is a tube connecting the surface to a pressurized underground formation. Inside that formation, oil and gas are held in pore spaces at pressures that can exceed 10,000 psi (690 bar) at the depths Angola's deepwater wells reach.

If that pressure is not controlled — if formation fluid enters the wellbore and is allowed to migrate to surface — the result is a **blowout**: uncontrolled release of hydrocarbons, potentially explosive and fatal.

Well control is the set of principles, procedures, equipment, and training used to prevent this from happening.

**Why Angola specifically:**
Angola's deepwater wells (Blocks 15, 17, 31, 32) penetrate reservoir sands at 2,000–5,000m total vertical depth in 500–2,500m water depth. Reservoir pressures of 5,000–10,000+ psi are common. A well control failure in these conditions is catastrophic. The Macondo/Deepwater Horizon disaster (2010) was exactly this — and it killed 11 people and discharged 4.9 million barrels of crude oil. That event rewrote well control regulations globally.

---

## Part 2: The Pressure Balance Concept

### Hydrostatic Pressure: Your Primary Tool

The mud column in the wellbore exerts pressure on the formation. As long as this **hydrostatic pressure (HP)** is greater than or equal to the **formation pore pressure (PP)**, the well is "in control."

$$\text{HP (psi)} = 0.052 \times \text{Mud Weight (ppg)} \times \text{TVD (ft)}$$

$$\text{HP (bar)} = 0.0981 \times \rho \text{ (kg/L)} \times \text{TVD (m)}$$

**Example:**  
Well depth: 4,000m TVD  
Mud weight: 1.50 kg/L (12.5 ppg)

$$\text{HP} = 0.0981 \times 1.50 \times 4000 = 588.6 \text{ bar}$$

If the reservoir at 4,000m has pore pressure = 560 bar: you have ~29 bar overbalance. The well is controlled.

### The Pressure Window

Every formation has two critical pressure limits:

| Pressure | Definition | Danger Zone |
|---|---|---|
| **Pore Pressure (PP)** | Pressure in rock pore spaces — the fluid you're trying to exclude | HP < PP → Kick (formation fluid enters wellbore) |
| **Fracture Gradient (FG)** | Pressure at which the formation rock fractures open | HP > FG → Lost circulation (mud lost into formation) |

Your drilling fluid density must keep the **Equivalent Circulating Density (ECD)** inside this window at all times:

$$PP < ECD < FG$$

In Angola's deepwater narrow-margin wells, this window may be only 0.3–0.5 ppg wide. Extremely precise mud weight management is required.

### ECD: What It Is and Why It Matters

**ECD** is the effective mud density when the pump is circulating. The act of pumping creates additional pressure (friction) in the annulus, increasing the effective density seen by the formation:

$$\text{ECD (ppg)} = \text{Static Mud Weight (ppg)} + \frac{\text{Annular Pressure Loss (psi)}}{0.052 \times \text{TVD (ft)}}$$

When you pull the pipe out of the hole (tripping), you remove the ECD component — the effective density drops. This is when kicks most commonly occur.

---

## Part 3: Kick Detection — Recognizing the Warning Signs

A **kick** is an influx of formation fluid into the wellbore. It must be caught early. Once a kick becomes large (a "blowout" risk), the consequences multiply rapidly. Your job: detect it in minutes, not hours.

### Primary Kick Indicators

**Pit Gain (most reliable):**
Mud is a closed system. If the total volume of mud in the active pit increases without you adding anything — formation fluid has entered the wellbore.

> **Rule:** Any pit gain > 2 barrels while drilling must be investigated immediately. > 5 barrels = shut in the well.

**Flow After Pump Stops:**
Stop the pump. Monitor the return line (bell nipple). If mud continues to flow after the pump stops — the formation pressure is pushing mud out. The well is flowing.

**Pump Pressure Decrease:**
Gas entering the wellbore is less dense than mud. As gas rises up the annulus, it lightens the mud column. This reduces hydrostatic head. If pump pressure drops unexpectedly (with no change in pump speed or string position), gas cutting is possible.

**Increase in Flow Rate:**
If you pump at a constant stroke rate but return flow is higher than expected, something is adding volume — formation fluid influx.

**Drilling Break:**
Sudden increase in Rate of Penetration (ROP). When the bit drills into an overpressured formation, the differential pressure assists penetration — the bit drills faster. A drilling break > 2–3× normal rate is a warning sign.

**Chloride Increase:**
If the mud shows increasing chloride content (from saline water), salt water is entering the wellbore from a saline formation or water zone.

---

## Part 4: The Blowout Preventer (BOP)

The BOP is the mechanical barrier that seals the wellbore when you need to shut the well in. On deepwater Angola wells, it is a **subsea BOP stack** sitting on the seabed directly above the wellhead.

### BOP Components and Functions

| Component | Function | Location |
|---|---|---|
| **Annular Preventer** | Flexible rubber element that seals around any OD (pipe, tubing, open hole) | Top of BOP stack |
| **Variable Bore Rams (VBR)** | Close and seal around a range of pipe sizes | Upper rams |
| **Pipe Rams** | Fixed size — seals around a specific pipe OD | Middle rams |
| **Blind/Shear Rams** | Cuts the drill pipe and seals the wellbore completely | Lower rams (emergency) |
| **Wellhead Connector** | Connects BOP to the wellhead on the seabed | Base of BOP |

**Deepwater-specific addition: Lower Marine Riser Package (LMRP)**
In a deepwater well, a drilling riser (large pipe) connects the surface (drillship) to the subsea BOP. The LMRP sits between the riser and the BOP. In an emergency disconnect, the LMRP disconnects, the BOP's blind/shear rams cut and seal the drill pipe, and the rig can move off location without losing well control.

### BOP Testing

BOPs must be pressure tested regularly (typically every 14–21 days per API/ANPG requirements). Tests include:
- **Low-pressure test:** ~200–300 psi for 5 minutes
- **High-pressure test:** Full working pressure for 5 minutes
- **Function test:** Each ram operated open/close

---

## Part 5: The Shut-In Procedure

You have detected a kick. You have > 2 barrels of pit gain. What do you do?

**Step 1: Stop drilling immediately.** Pick up off-bottom.

**Step 2: Notify the rig floor.** "We have a kick. Shut in the well."

**Step 3: Shut in — Soft Shut-In (most common) OR Hard Shut-In.**

*Soft shut-in sequence:*
1. Stop the pump
2. Open the Hydraulic Kill Manifold (HKM)
3. Close the annular preventer (or upper pipe rams)
4. Close the HKM
5. Read SIDPP (Shut-In Drill Pipe Pressure) and SICP (Shut-In Casing Pressure)

**Step 4: Record pressures and pit gain.** These numbers determine your kill procedure.

**Shut-In Drill Pipe Pressure (SIDPP):** Pressure you read on the drill pipe side with the pump off and well shut in. This is the pressure the formation is pushing at — it tells you how much your current mud weight is underbalanced.

**Kill Mud Weight:**
$$\text{Kill Mud Weight (ppg)} = \text{Current MW (ppg)} + \frac{\text{SIDPP (psi)}}{0.052 \times \text{TVD (ft)}}$$

---

## Part 6: Well Kill Methods

### Method 1: Driller's Method (Two Circulation Approach)

**When to use:** You detected the kick and shut in quickly. You want to remove the kick from the wellbore immediately without waiting to mix kill mud.

**Circulation 1 — Circulate the influx out:**

1. Circulate at the pre-recorded slow pump rate (SPR) — the pump rate used at the time of the kick
2. Hold the **casing pressure constant** using the choke (open or close choke to maintain SICP)
3. The influx (gas/oil/water) travels up the annulus and reaches the choke
4. As gas rises, it expands — casing pressure will tend to increase → open choke slightly to maintain constant casing pressure
5. Influx exits through the choke manifold → mud/gas separator (poor boy degasser) → flare

**After Circulation 1:** The wellbore contains original mud (too light — that's why we got the kick). Well is stable but not killed.

**Circulation 2 — Kill with weighted mud:**

While Circulation 1 is ongoing, kill mud is mixed in the pits to the kill mud weight calculated earlier. After the influx is out and the well is stable:

1. Start pumping kill mud down the drill pipe
2. Maintain drill pipe pressure at a specific "kill pressure" schedule (drill pipe pressure decreases as kill mud fills the drill string — because the heavier kill mud is displacing lighter original mud)
3. When kill mud reaches the bit: maintain constant drill pipe pressure (casing backpressure should drop)
4. Continue circulating kill mud up the annulus. When kill mud appears at the choke → well is killed.
5. Shut down pumps. Both drill pipe and casing pressure should be zero → well is statically killed.

---

### Method 2: Wait and Weight Method (Engineer's Method — One Circulation)

**When to use:** You prefer a single circulation. You can afford to wait 30–90 minutes while kill mud is mixed and verified before starting.

**Advantage:** One circulation instead of two. Kill mud displaces the influx in a single pass.

**Kill pressure schedule (what you maintain on drill pipe pressure):**

At start of circulation (kill mud at surface):
$$SIDPP_{kill} = SIDPP + 0.052 \times (MW_{kill} - MW_{current}) \times TVD$$

As kill mud fills the drill string, the drill pipe pressure decreases linearly from this initial value down to the final circulating pressure (FCP) when kill mud exits the bit.

**The kill sheet:** A table you fill out before starting circulation:
- Initial circulating pressure (ICP) = Slow Circulating Rate pressure + SIDPP
- Final circulating pressure (FCP) = Slow Circulating Rate pressure with kill mud
- Stroke counter at each 25% or 50% increment of the kill mud fill
- Expected drill pipe pressure at each stroke increment

**Angola deepwater note:** Deepwater wells have a long riser (1,500–2,500m) filled with seawater, then the BOP, then the drill string below. The riser contents complicate the kill sheet because riser fluid is different from mud. Always check whether the riser margin has been accounted for.

---

### Part 6 Continued: Deepwater Well Control — Special Considerations

**Riser margin:**
In a deepwater well, if the riser disconnects (emergency disconnect), the seawater in the riser replaces the heavier mud in the top section. The hydrostatic head at the wellhead drops. If the mud weight was barely above pore pressure, this could cause the well to flow. The riser margin is the extra mud weight above the minimum needed to compensate for this scenario:

$$\text{Riser Margin (ppg)} = \frac{(MW_{mud} - \rho_{seawater}) \times \text{Riser Length}}{TVD_{well}}$$

This is why deepwater mud weights are often higher than the pore pressure alone would dictate.

**Kick tolerance:**
In deepwater narrow-margin formations (Block 32 sub-salt), there is very little room between pore pressure and fracture gradient. "Kick tolerance" is the maximum pit gain you can take and still safely shut in and kill the well without fracturing the weakest open hole:

$$\text{KT (bbl)} = \frac{(FG - MW) \times 0.052 \times TVD_{weak shoe}}{C_a} \times K$$

Where $C_a$ = annular capacity (bbl/ft) and $K$ = conversion factor. Low kick tolerance means you shut in earlier and faster.

**Managed Pressure Drilling (MPD):**
In wells where the pore pressure/fracture gradient window is very narrow (< 0.3 ppg), conventional drilling cannot maintain the ECD within the window for the entire hole section. MPD adds surface backpressure (using a rotating control device — RCD — on the riser) to fine-tune the effective wellbore pressure without changing mud weight. Used on Block 32 sub-salt wells in Angola.

---

## Part 7: Stripping Operations

When a kick is detected while tripping (pipe is moving), you must get the drill string back to bottom to circulate out the influx. Stripping = moving the drill string through the closed BOP.

**Stripping procedure:**
1. Close annular preventer around the drill string
2. Monitor casing pressure — as pipe is run into the hole, the string displaces fluid, increasing casing pressure. Bleed pressure to maintain safe level.
3. Run the string to bottom (or to a safe depth to circulate)
4. Circulate out the kick using standard well kill procedure

**Volumetric method (if you cannot strip — well control from surface only):**
Used when you cannot run pipe (bit off bottom, complex situation). You control the wellbore by allowing gas to migrate upward while bleeding small volumes of mud from the choke to maintain constant casing pressure. This "lubricate and bleed" technique requires careful monitoring.

---

## Part 8: IWCF Certification — What You Need to Know

The **IWCF (International Well Control Forum)** certification is the internationally recognized well control qualification. Every engineer who goes offshore on a drilling or workover operation needs it.

**IWCF Level 1 (Foundation — Well Control):**
- Awareness level. The exam covers: pressure concepts, kick detection, BOP equipment, shut-in procedures.
- Entry-level. Get this before your first offshore trip.
- Format: Multiple choice exam.

**IWCF Level 2 (Supervisory — Well Control):**
- Operational level. Required to supervise drilling operations.
- Covers everything in Level 1 plus: kill methods, abnormal pressures, well control complications, kick calculation worksheets.
- Format: Multiple choice + practical simulation/oral exam.

**IWCF Surface Stack (Drilling) vs Subsea Stack:**
Angola deepwater wells use subsea BOPs. The Subsea Stack certificate adds knowledge of:
- Subsea BOP configuration (stack layout, LMRP, riser)
- Emergency disconnect procedure
- Riser margin calculations
- Kill and choke line considerations (friction adds back-pressure in deepwater)

---

## Exercises — Angola Well Control Scenarios

**Exercise 1: Pressure Balance Calculation**
A well is drilling at 3,800m TVD with 1.45 kg/L mud. Formation pore pressure = 530 bar. Is the well overbalanced or underbalanced? By how much? Calculate the minimum mud weight required for balance.

**Exercise 2: Kill Mud Weight**
You detect a kick. Pump is stopped. SIDPP = 42 bar. SICP = 58 bar. Current mud weight = 1.50 kg/L. Well depth = 4,200m TVD. Calculate:
1. The kill mud weight required
2. The initial circulating pressure (ICP) for the Wait and Weight method if the slow pump rate pressure was 120 bar
3. The final circulating pressure (FCP)

**Exercise 3: Kick Volume and Type**
You shut in after detecting a kick. Pit gain = 15 barrels. SIDPP = 28 bar. SICP = 45 bar. The difference between SIDPP and SICP is the "hydrostatic head of the influx column." Annular capacity = 0.05 bbl/ft.
1. Calculate the length of the influx column in the annulus
2. The gradient of the influx = (SICP - SIDPP) / influx length in psi/ft. Identify if it's gas, oil, or salt water:
   - Gas: 0.07–0.12 psi/ft
   - Oil: 0.30–0.40 psi/ft
   - Salt water: 0.44–0.48 psi/ft

**Exercise 4: ECD Calculation**
Mud weight = 1.52 kg/L. Annular pressure loss = 45 bar. Well TVD = 4,000m. Calculate ECD. The fracture gradient at the last casing shoe (3,500m TVD) is 1.78 kg/L. Is there a fracture risk?

---

## Interview Questions — Well Control

1. A drillship in Angola Block 32 takes a 15 bbl kick at 4,200m TVD. SIDPP = 35 bar. Current mud weight = 1.55 kg/L. What is your kill mud weight, and which kill method would you recommend and why?
2. Explain the difference between a Hard Shut-In and a Soft Shut-In. Which is currently preferred on most rigs and why?
3. What is the riser margin and why does it affect mud weight selection on Angola deepwater wells?
4. A well is drilled with an ECD of 1.62 kg/L but static mud weight of 1.55 kg/L. The fracture gradient at the next casing shoe is 1.65 kg/L. What is your risk and what options do you have?
5. What is Managed Pressure Drilling and when would you use it in Angola?
6. If you hear "We have a drilling break — rate went from 5 m/hr to 18 m/hr" from the driller, what do you do immediately?
7. What does SIDPP = 0 and SICP > 0 tell you about the kick?
8. Explain the volumetric well control method. When is it used?

---

*Next: [02_Drilling_Fundamentals_Tutorial.md](02_Drilling_Fundamentals_Tutorial.md) | Return to [00_INDEX.md](../00_INDEX.md)*

Most commonly used when you need to act immediately without waiting to mix heavy kill mud.

**Circulation 1:** Circulate the kick out of the wellbore using current mud weight (the lighter mud). The BOP is closed; you pump down the drill string and out through the choke line.

**Circulation 2:** After the kick is out, circulate the kill mud weight down to kill the well.

**Advantage:** Starts immediately. No waiting for heavy mud.  
**Disadvantage:** The formation is underbalanced during Circulation 1. Higher surface pressures.

### Method 2: Wait and Weight Method (Engineer's Method)

**Single circulation:** Immediately mix kill mud. Calculate the exact weight required. When kill mud is ready, begin ONE circulation pumping kill mud down the drill pipe while managing the choke.

**The choke schedule:** During the kill, you hold SIDPP constant by adjusting the choke. As kill mud replaces regular mud in the drill string, you track the calculated drill pipe pressure. When heavy mud reaches the bit, you begin managing casing pressure.

**Advantage:** Single circulation. Lower surface pressures.  
**Disadvantage:** Takes time to mix heavy mud before you can start.

---

## Part 7: H2S — The Silent Killer

Hydrogen sulfide (H2S) is a toxic gas that can be present in some Angola well streams. It is:
- Colorless
- Has a rotten egg smell at low concentrations (but paralyzes your sense of smell at high concentrations — you stop smelling it before it kills you)
- Heavier than air (accumulates in low points)
- Flammable
- Fatal at 300 ppm exposure (instantaneous at 1,000 ppm)

**H2S safety on a drillship or FPSO:**
- Personal H2S detectors worn by all personnel (alarm at 10 ppm)
- Fixed H2S point detectors in high-risk areas
- Self-Contained Breathing Apparatus (SCBA) staged at strategic locations
- Wind direction awareness (muster upwind of H2S source)
- **H2S Contingency Plan:** Pre-designated safe muster areas based on wind direction

**Your H2S awareness certification** covers all of the above. This cert is mandatory before any offshore trip where H2S is possible.

---

## Part 8: Deepwater-Specific Well Control Challenges

Angola is deepwater. Deepwater well control has unique complications beyond what you study in standard IWCF Level 1:

**Riser Margin:**
The drilling riser is filled with seawater or kill-weight mud. In a normal deepwater well, the BOP is closed on the seabed, and there is ~1,500m of seawater in the riser above the BOP. This seawater is lighter than the kill mud needed in the wellbore — creating a pressure asymmetry that requires careful calculation.

**Bullheading:**
Pumping down the annulus to force the kick back into the formation. Used when you can't circulate out safely. Requires high pump pressure.

**LMRP Disconnect:**
In an emergency on a deepwater drillship, the rig may disconnect from the well while the BOP holds the well shut in. The kill and choke lines are sealed. The rig moves off location. This is a last resort for weather events, dynamic positioning failures, or fire on the rig.

**Sub-surface Gas Behavior:**
Gas that enters the wellbore at 2,000m seabed depth is highly compressed. As it migrates up the wellbore (if not controlled), it expands. A small kick at the seabed becomes a massive gas expansion problem at surface if not handled correctly.

---

## Part 9: Self-Assessment Exercises

Work through these before your IWCF Level 1 exam or before any well control interview:

**Exercise 1:** A well is drilled to 3,500m TVD with 1.45 kg/L mud. SIDPP after a kick is detected is 85 bar. Calculate:
1. Current hydrostatic pressure
2. Kill mud weight required
3. New hydrostatic pressure with kill mud

**Exercise 2:** ECD calculation. A well has static mud weight of 1.52 kg/L. The annular pressure loss while circulating is 120 psi (8.3 bar) at 3,200m TVD. Calculate the ECD in kg/L. Is this ECD inside a pressure window of PP = 1.55 kg/L and FG = 1.78 kg/L?

**Exercise 3:** Draw from memory the main components of a subsea BOP stack from wellhead connector to LMRP. Label each component and state its function.

**Exercise 4:** You are on a drillship. The driller calls you and says: "We just had a 5-barrel pit gain. I've stopped the pump." What are your next 5 actions in order?

---

## Part 10: Where to Study Further

| Resource | Format | Cost | What You Get |
|---|---|---|---|
| IWCF Study Guide (official) | PDF/Online | Free on iwcf.org | The actual exam syllabus and study materials |
| Landmark WellPlan tutorials | YouTube | Free | Visual understanding of hydraulics calculations |
| SPE paper: "Well Control Incidents Review" | PDF | Free on SPE | Real case studies from Angola and similar environments |
| "Applied Drilling Engineering" (Bourgoyne et al.) | Textbook | Library/purchase | The industry's classic drilling fundamentals textbook |
| Drilling Engineering Association (DEA) videos | YouTube | Free | Professional-grade explanations of BOP components |
| "Fundamentals of Drilling Engineering" (SPE Textbook Vol. 12) | PDF/Textbook | SPE student membership ($25/yr) | Current comprehensive drilling reference |

---

*Back to: [03_Skills_Universe.md](../03_Skills_Universe.md) | See also: [docs/skills/01-well-control.md](../../../docs/skills/01-well-control.md)*  
*Where to learn: [IWCF](https://iwcf.org) (PETROTEC Luanda) | [Drillingformulas.com](https://drillingformulas.com) | [Learning Resources](../../../docs/learning-resources.md)*
