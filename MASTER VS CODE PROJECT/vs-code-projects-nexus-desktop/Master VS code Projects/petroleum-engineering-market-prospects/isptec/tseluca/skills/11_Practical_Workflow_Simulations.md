# Practical Workflow Simulations — Angola Offshore
## The "You Are There" Guide: What You Actually Do From Day 1

> This file puts you in the role. Read these simulations like a script. When the shift starts, this is what happens. This is what you fill in. This is what you say on the radio. This is what the handover note looks like. Study this until it feels normal.

---

## How to Use This File

Each simulation has:
- **Context:** What the scenario is
- **Your role:** Who you are
- **Step-by-step:** What you actually do (not theory — specific actions)
- **Documents you fill in:** Real form layouts
- **Decision points:** What you check and what you decide
- **What could go wrong:** Red flags to catch

Do not skip any simulation. They build on each other.

---

# Simulation 1: Your First Day on a Drillship (Block 32, TotalEnergies)

**Context:** You are a Field Engineer Trainee at SLB. You have completed your 8-week onshore training. Today is Day 1 of your first offshore rotation. You will fly from Luanda to the Valaris DS-12 drillship operating in Block 32, 250 km offshore. Water depth: 1,850m.

**Your role:** SLB MWD/LWD Field Engineer Trainee. You shadow the Senior MWD Engineer, Eng. Paulo, for your first 2 weeks before taking your own shifts.

---

### 06:00 — Helicopter Briefing at Luanda Airport (4 de Fevereiro)

You arrive at the helicopter terminal. You must show:
- [ ] BOSIET certificate (original, valid — yours expires in 4 years)
- [ ] IWCF or Well Control certificate (or evidence of current enrollment)
- [ ] Medical certificate (offshore medical, valid 2 years)
- [ ] Yellow fever vaccination card
- [ ] Your company ID badge
- [ ] SLB offshore assignment letter

The check-in clerk weighs your personal baggage. Limit: **15 kg personal + 5 kg hand luggage.** Overweight = left behind. You packed smart: 2 weeks of clothes (you wash on the rig), one technical book (this one is good), your laptop, personal meds.

**The safety briefing:**
Before boarding the AS365 Dauphin helicopter (10 seats), the helideck officer gives a 3-minute briefing:
- "Life jackets under your seat. Put on if commanded."
- "Emergency exit: slide door to your left. Pull red handle."
- "If we ditch: wait for rotors to stop, equalize pressure, exit."

You already practiced this in HUET (Helicopter Underwater Escape Training) during BOSIET. You feel calm.

**Flight time:** ~1.5 hours offshore. You can see the FPSO Dalia in the distance as you cross Block 17 airspace.

---

### 08:00 — Arrival on the Drillship

The helicopter lands on the helideck. The helideck officer signals: wait until rotors slow. You step off single-file, hard hat on, visor down.

A SLB hand meets you at the helideck entry: "Welcome aboard. I'm Miguel, SLB Coord. Paulo will meet you in the MWD cabin. First: safety induction."

**Mandatory safety induction (1.5 hours):**
- Muster station location (yours: muster station B, deck 4)
- Emergency signals (7 short + 1 long = general alarm = abandon ship)
- Fire/gas alarm procedures
- Lifeboat assignment (your lifeboat: portside, boat #3)
- H₂S procedures (below 10 ppm = caution, above 10 ppm = evacuate)
- PTW (Permit to Work) system overview
- Hospital/clinic location

After induction: sign the **Offshore Safety Induction Register.** Keep a copy.

---

### 10:00 — MWD Cabin: Your Work Home

The MWD cabin is on the third deck, port side. It looks like this:

```
┌─────────────────────────────────────────────────────┐
│  Monitor 1: Real-time drilling parameters (WITSML) │
│  Monitor 2: MWD tool status + gamma ray track      │
│  Monitor 3: Directional survey plots               │
│  Monitor 4: Depth track + formation evaluation     │
│                                                    │
│  [Desk] Drill ahead / EM pulse decoder             │
│  [Filing cabinet] Previous well data, procedures  │
│  [Whiteboard] Current well status, depths, casing  │
└─────────────────────────────────────────────────────┘
```

Eng. Paulo shows you the current situation:

"We're at 3,420m MD in an 8½" hole section. We're drilling the reservoir approach. In about 50m we expect to enter the Malembo Formation turbidite sands — that's why LWD is critical right now. The GR should drop from 90 API to below 30 API when we enter sand. Our job is to tell the directional driller and the company man what we're seeing in real time."

**What the MWD system does:**
The MWD tool is part of the BHA (bottom hole assembly), ~60m above the drill bit. It measures:
- **Inclination and azimuth** (directional survey — is the well going where it should?)
- **Gamma Ray** (GR) — tells us the lithology in real time
- **Resistivity** (shallow, medium, deep) — tells us if we're in oil or water
- **Annular pressure** (PWD) — tells us if ECD is within safe limits

The tool sends this data uphole by **mud pulse telemetry**: pressure pulses coded as binary data travel up the mud column at ~1,000 m/s. The surface computer decodes these pulses into the numbers you see on your screen.

---

### 14:00 — Shift Handover (Critical Skill)

Eng. Paulo calls you to observe a shift handover. This happens every 12 hours. The outgoing MWD engineer (Eng. Chen, who worked the night shift) hands over to Eng. Paulo (day shift). You watch and take notes.

**Shift Handover Script:**

> "Current depth: 3,418m MD / 3,401m TVD. Still drilling 8½" hole. BHA run #4 in hole since yesterday 06:00. ROP averaging 12 m/hr. Bit is PDC 8½" SLB M22K.
>
> Survey status: Last survey at 3,400m — inclination 43.2°, azimuth 287°. On target, trending slightly below the planned well trajectory by 4m TVD. Plan says we should be above. I told the DD (directional driller) — he's building angle 0.5°/30m to correct. Watch for the next survey at 3,430m.
>
> Tool status: GR, P+R (density + resistivity), and PWD all reading good. Battery 78% — we have 8 more days of battery life. No issues.
>
> Mud weight: 1.42 SG, ECD showing 1.47 SG at bit. Formation pore pressure predicted 1.39 SG — we have 0.08 SG overbalance. Safe window. Keep an eye if ECD trends up toward 1.52 SG (fracture gradient limit at this depth).
>
> Flag: Company man wants a call if GR drops below 40 API — that's our sand entry signal. Call him immediately, do not wait.
>
> Nothing unusual. Handover complete."

Eng. Paulo signs the handover logbook. Both engineers sign. **This handover log is a legal document.**

**Key lesson:** A good handover is **depth + status + trend + flag + action.** Never say "everything is fine" without backing it up with numbers.

---

### 16:00 — Sand Entry! Real-Time Decision Making

You are watching Monitor 2. GR has been steady at 85–92 API (shale). Suddenly at 3,468m:

```
GR: 89 → 87 → 71 → 52 → 34 → 22 API   ← Sand entry!
Deep Rt: 2.1 → 2.3 → 4.5 → 12 → 28 Ω·m  ← Resistivity rising → OIL!
RHOB: 2.52 → 2.38 → 2.21 g/cc  ← Density decreasing → porosity improving
NPHI: 0.28 → 0.26 → 0.25 → 0.22  ← Neutron tracking density → no gas
```

**What you do:**

1. **Pick up the intercom.** "Company man, MWD — we've hit sand at 3,468m MD. GR is 22 API, resistivity at 28 ohm·m and rising. Density porosity ~28%. Looks like clean oil sand. I'm flagging it now."

2. **Log the sand top in the Well Event Log** (paper log in the cabin):
   ```
   3,468m MD | 3,449m TVD | Sand entry confirmed | GR 22 API | Rt 28 Ω·m | 16:12 hrs
   ```

3. **Update the depth track on Monitor 4.** Mark the lithology boundary.

4. **Send a LAS file update** (log ASCII standard format) to the company man's cabin within 15 minutes. This is the official digital record of your observations.

5. **Notify your SLB coordinator** with a text on the rig internal system: "B32-GD1: sand at 3468m. GR 22 API, Rt 28, φ 28%. Oil-bearing indicators present. See LAS update."

The company man calls back: "Good work. Drill ahead but slow ROP to 8 m/hr — we want good log quality through this interval. Take a wiper trip at 3,500m before we get too deep in the sand."

You relay this to the DD: "Company man says slow ROP to 8 m/hr, plan a wiper trip at 3,500m."

---

# Simulation 2: Production Operator Morning Shift on FPSO Dalia (Block 17, TotalEnergies)

**Context:** You are a Production Technologist Trainee at TotalEnergies, assigned to the FPSO Dalia, Block 17. The FPSO processes ~120,000 STB/day oil from 24 producing wells. You are on your second rotation, so you know the layout. Your supervisor is Sr. Production Technologist Eng. Fatima.

---

### 06:00 — Shift Handover (Same principle, different data)

The night shift technologist (Eng. Sebastiao) hands over to you and Eng. Fatima:

> "Current production: 118,200 STB/day oil. FPSO throughput target is 120,000. We're 1,800 bbl/day short.
>
> Well status: 24 wells online, 0 wells shut in. However, Well G-17 is showing declining WHP. WHP this morning is 210 bar, down from 225 bar last week. The well is 3 months old, so this is premature decline — we need to watch it.
>
> Gas lift: All 22 GL wells operating. Total GL gas injection: 185 MMscfd. GL compressor 2 had a minor trip at 03:00 but auto-restarted. No action needed.
>
> Separators: Train A operating at 95% throughput. Train B at 92%. Train C at 82% (one separator under scheduled maintenance, back online 08:00 today).
>
> Water treatment: BWWT making spec — BS&W export = 0.28% (limit 0.5%). Produced water overboard flow = 18,200 m³/day, meeting MARPOL specification (<30 ppm oil).
>
> Nothing unusual. Watch G-17."

You sign the handover log. Shift starts.

---

### 07:00 — The Daily Production Sheet

You open the FPSO production management system (MERAK or TotalEnergies PI). Your first task: **build the daily production report** that must be submitted to:
1. The Asset team (onshore Luanda) by 09:00
2. ANPG by 18:00

Here is what the daily production sheet looks like:

```
DALIA FPSO — DAILY PRODUCTION REPORT
Date: [Today] | Report #: 847

PRODUCTION SUMMARY
─────────────────────────────────────────────────────
Gross Liquids Processed:           148,200 STB/day
Oil to Storage / Export:           118,200 STB/day
Water Produced:                     29,400 STB/day
Water Cut:                           19.8%
Gas Produced (associated):          95 MMscfd
Gas Utilized (compression + GL):    88 MMscfd
Gas Flared:                          7 MMscfd  ← FLAG: above 5 MMscfd limit
Gas Utilization Efficiency:          92.6%

INJECTION
─────────────────────────────────────────────────────
Water Injection FPSO A: 45,000 STB/day
Gas Lift Injection: 185 MMscfd

WELL STATUS
─────────────────────────────────────────────────────
Producing Wells: 24/24
Shut-in Wells: 0
New Wells on Production: None
Wells Under Maintenance: None

EQUIPMENT STATUS
─────────────────────────────────────────────────────
Train A: OPERATING (95% utilization)
Train B: OPERATING (92% utilization)
Train C: OPERATING (82% utilization, separator back online 08:15)
GL Compressor 1: RUNNING
GL Compressor 2: RUNNING (auto-restart at 03:00, monitoring)
Export Pump 1: RUNNING
Export Pump 2: STANDBY

EXPORT QUALITY
─────────────────────────────────────────────────────
BS&W: 0.28% (spec: <0.5%) PASS
Reid Vapor Pressure: 12 psi (spec: <14 psi) PASS
API gravity: 23.8° (consistent with Dalia blend)

ALERTS AND FLAGS
─────────────────────────────────────────────────────
1. FLARING: 7 MMscfd — above 5 MMscfd target. Root cause: compressor trip 03:00. 
   Action: Monitor GL Compressor 2, engineering reviewing.
2. Well G-17 WHP declining (210 bar, trend -15 bar/week). 
   Action: Production engineer notified. PI test scheduled tomorrow.
```

---

### 09:00 — Well Performance Review: Diagnosing G-17

Eng. Fatima pulls up Well G-17 in the production history system. She shows you how to diagnose:

**Step 1: Plot the trend**
```
Month 1: WHP 245 bar, q = 6,200 STB/day, GL inj = 5.0 MMscfd
Month 2: WHP 232 bar, q = 5,950 STB/day, GL inj = 5.0 MMscfd
Month 3: WHP 210 bar, q = 5,600 STB/day, GL inj = 5.0 MMscfd
```
Rate declining AND WHP declining with constant GL injection. What does this mean?

**Step 2: Diagnostic logic**

| Observation | Possible Cause |
|------------|---------------|
| WHP declining, Rate declining, GL inj constant | Reservoir pressure decline OR well damage (skin) |
| WHP declining, Rate constant | Tubing restriction (scale?) |
| WHP constant, Rate declining | Separator back-pressure increasing |
| WHP rising, Rate declining | Well loading up (GL insufficient) |

For G-17: WHP falling AND rate falling → **reservoir pressure declining OR skin increasing.**

**Step 3: Check if other wells in the same area are declining**
Pull up neighboring wells G-15, G-16, G-18. Check their WHP trend over the same period.

If G-15 and G-16 are also declining → **reservoir pressure depletion** (expected, natural)
If only G-17 is declining → **well-specific issue** (possible damage/scale/sand)

In our case: G-15 and G-16 also show slight WHP decline (5 bar over 3 months). G-17 is declining faster (15 bar over 3 months).

**Conclusion:** Primarily reservoir decline, but G-17 has an additional well-specific issue. Action: Schedule a **well test** (route G-17 through test separator) and a **downhole pressure gauge readout** to confirm reservoir pressure.

Eng. Fatima: "Good diagnosis. Write it up in the well surveillance log and send the request for a downhole gauge readout to the completions team."

---

### 10:30 — Gas Lift Optimization (Daily Task)

The GL compressor capacity this morning is **185 MMscfd** available. You need to distribute this across 22 gas lift wells to maximize total oil production.

**Current allocation:** Equal distribution = 185/22 = 8.4 MMscfd/well (naive approach)

**Better approach:** Use each well's **Gas Lift Performance Curve** (rate vs GL injection rate) in the Prosper/GAP model.

You open GAP (General Allocation Program). The model shows:

```
Well     GL Injection  Oil Rate    Incremental Oil/MMscf
G-01     8.0 MMscfd   5,200 bbl     —
G-02     8.0 MMscfd   4,800 bbl     —
G-17     8.0 MMscfd   5,600 bbl   [Note: declining recently]
...
G-22     8.0 MMscfd   6,100 bbl     —

Increase G-03 injection from 8 to 10: +420 bbl → 210 bbl/MMscf
Increase G-07 injection from 8 to 10: +280 bbl → 140 bbl/MMscf
Increase G-15 injection from 8 to 10: +190 bbl → 95 bbl/MMscf

Decrease G-12 from 8 to 6 (well approaching economic limit of GL efficiency):
Loss: -180 bbl → gives you 2 MMscfd to redistribute
```

**Optimal allocation action:** Reduce G-12 to 6 MMscfd, redistribute 2 MMscfd to G-03. Net gain: +420 - 180 = **+240 STB/day**.

You make the recommendation, Eng. Fatima approves, the control room technician adjusts the GL injection control valves via the ICSS (Integrated Control and Safety System). You document the change in the production log.

---

# Simulation 3: Well Control Incident Response (Kick Detection to Kill)

**Context:** You are an operator's drilling engineer on a drillship in Block 17. It is 02:15 (night shift). You are the Company Man on duty. The driller calls you.

---

### 02:15 — The Driller's Call

**[Intercom]** "Company man — we've got a pit gain. Pit volume was 320 m³ at 02:00, now reading 333 m³. ROP just jumped from 15 m/hr to 32 m/hr. I think we have a kick. Should I shut in?"

**Your mental checklist (next 30 seconds):**

1. **Confirm the indicators.** Pit gain = 13 m³. ROP increase. Any other signs? Check monitor quickly:
   - Pump pressure: stable or decreasing? (decrease = formation fluid lighter than mud entering)
   - Torque: any changes? No.
   - ECD: reading consistent with expected? Yes, 1.44 SG.

2. **Size the kick: 13 m³ = 82 barrels.** This is a medium-sized kick. Not a catastrophic blowout yet. Time is on your side if you act now.

3. **Identify likely kick source.** Current depth: 3,650m. Pore pressure prediction at this depth: 1.38 SG. Current mud weight: 1.42 SG. We should have overbalance. Check: was there a mud weight change recently? Check the mud report — yes, the mud weight was being diluted from 1.43 to 1.42 SG in the past 2 hours because of a high ECD concern. Temporarily under-balanced when diluting. This is the likely cause.

**Your response (out loud):**

"Yes, shut in. Execute the soft shut-in procedure. Now."

---

### 02:17 — Soft Shut-In Procedure

The driller executes:
1. Picks up kelly/top drive — lifts bit off bottom
2. Opens HCR (Hydraulic Choke Return) — diverts returns from bell nipple to choke manifold
3. Slowly closes the pipe rams on the BOP stack

While this is happening, you:
1. **Alert the OIM** (Offshore Installation Manager): "OIM, Company Man. We've shut in on a kick. Pit gain 13 m³. Implementing well control procedures."
2. **Alert SLB/Halliburton Well Control specialist** on duty — "Get to the driller's console now."
3. **Start the clock.** SIDPP stabilization time: 5 minutes minimum before reading.

---

### 02:25 — SIDPP and SICP Readings

After 5 minutes of shut-in:
- **SIDPP (Shut-In Drill Pipe Pressure):** 32 bar (3.2 MPa)
- **SICP (Shut-In Casing Pressure):** 45 bar (4.5 MPa)

**Kill mud weight calculation:**

$$\text{Kill Mud Weight} = \text{Current MW} + \frac{\text{SIDPP}}{0.0098 \times \text{TVD}}$$

$$= 1.42 + \frac{32}{0.0098 \times 3,628} = 1.42 + \frac{32}{35.55} = 1.42 + 0.09 = 1.51 \text{ SG}$$

**ICP (Initial Circulating Pressure):**

$$\text{ICP} = \text{SIDPP} + \text{SCR pressure} = 32 + 45 = 77 \text{ bar}$$
(SCR = slow circulating rate pressure, measured at 30 strokes/min = 45 bar, from your pre-kick baseline)

**FCP (Final Circulating Pressure):**

$$\text{FCP} = \text{SCR pressure} \times \frac{\text{Kill MW}}{\text{Current MW}} = 45 \times \frac{1.51}{1.42} = 47.9 \text{ bar}$$

You write these on the whiteboard at the driller's console.

---

### 02:30 — Decision: Driller's Method or Wait and Weight

You speak with the company man, Well Control specialist, and OIM:

**Driller's Method:** Circulate the kick out at current mud weight, then circulate kill mud. Two circulations. Faster. Good if kick is large (risk of differential sticking if you wait too long).

**Wait and Weight:** Weight up mud to kill weight first, then circulate in one pass. Slower. Less exposure of annulus to low-mud-weight conditions.

Given the kick is 13 m³ (medium), mud weighting is fast (barite is available), you choose **Wait and Weight.**

---

### 02:32 — Weighting Up the Mud

Instruct the mud engineer: "Add barite to bring mud weight from 1.42 to 1.55 SG as soon as possible." (You add 0.04 SG excess for kill weight = 1.51 + 0.04 = 1.55 SG)

Mud engineer calculation:
$$\text{Barite to add} = \frac{4.2 \times (1.55 - 1.42)}{4.2 - 1.55} \times \text{Volume of active system}$$

Active mud volume = 320 m³. Result: ~66 metric tons of barite. You have 80 tons on board. Good.

Estimated weighting time: 45 minutes.

---

### 03:15 — Kill Circulation Begins

Kill mud weight achieved: 1.55 SG. Start pumping at SCR = 30 strokes/min.

**Kill sheet (what you follow minute by minute):**

| Strokes Pumped | Pressure at Surface (target) | Notes |
|---------------|-------------------------------|-------|
| 0 (start) | 77 bar (ICP) | Kill mud at surface |
| 500 | 74 bar | Kill mud entering drillstring |
| 1,000 | 71 bar | Kill mud at ~50% depth |
| 1,500 | 66 bar | Kill mud approaching bit |
| 2,100 (bit depth) | 47.9 bar (FCP) | Kill mud at bit — maintain this pressure |
| 3,200 (through riser) | 47.9 bar | Monitoring casing pressure |
| 4,100 (full circulation) | 47.9 bar (FCP) | Kill mud has swept full annulus |

Choke operator adjusts back-pressure continuously to maintain the target drillpipe pressure on the kill sheet.

At 05:30: First indication of kill success — SICP drops to zero. Drill pipe pressure = FCP only. No more formation fluid influx. The well is killed.

**You log the incident:** Start time 02:15, shut-in 02:17, kill commenced 03:15, well killed 05:30. Total kick volume circulated: 14.2 m³ (measured). Kick fluid: gas (confirmed by light SICP vs heavy SIDPP). Root cause: mud weight reduction during dilution at permeable zone. Corrective action: Resume drilling with 1.55 SG mud, pore pressure model revision required.

**Report to ANPG:** Kick incidents > 5 m³ must be reported to ANPG within 24 hours. OIM signs the incident report.

---

# Simulation 4: HAZOP Study — Separator Inlet (FPSO Process Safety)

**Context:** You are an HSE Engineer at TotalEnergies in Luanda. A process modification is being reviewed: increasing the separator inlet pressure from 60 bar to 75 bar. You are part of the HAZOP team.

**Team:** Process Engineer (team leader), HSE Engineer (you), Instrument Engineer, Operations Representative, SLB Production Services Engineer.

---

### Node: Separator 1st Stage Inlet Line

**Design intention:** Transfer produced fluids from wellhead at 75 bar to the 1st stage separator at 60 bar.

**HAZOP Guide Word: MORE FLOW**

| Column | Entry |
|--------|-------|
| Deviation | More flow than design (75 bar → separator instead of 60 bar) |
| Cause 1 | Control valve CV-101 fails open |
| Cause 2 | Manual isolation valve left open during maintenance |
| Consequence | Separator overpressure. PSV (pressure safety valve) lifts. If PSV undersized: separator rupture. |
| Safeguard | PSV-101 set at 65 bar. High-pressure shutdown HH-101 at 70 bar → closes ESD valve. |
| Is safeguard adequate? | **CHECK:** Is PSV-101 sized for the new 75 bar inlet scenario? → **ACTION: Re-rate PSV-101 for new scenario** |
| Recommendation | RE-07: Perform PSV sizing calculation for 75 bar inlet. Assign: Process Engineer. Due: 2 weeks. |

**HAZOP Guide Word: NO FLOW**

| Column | Entry |
|--------|-------|
| Deviation | No flow |
| Cause 1 | Control valve CV-101 fails closed |
| Cause 2 | Hydrate formation blocking inlet line (possible if cold seabed flow) |
| Consequence | Well backed up, wellhead overpressure, DHSV trips |
| Safeguard | Low-flow alarm LAL-101 alerts control room. Operator intervention. |
| Is safeguard adequate? | Yes, but add: **ACTION: Add hydrate thermodynamic check for new operating conditions.** |
| Recommendation | RE-08: Confirm no hydrate formation at 75 bar, T = ambient. Assign: Flow Assurance Engineer. |

You record every action in the HAZOP Action Register. The study produces 23 recommendations total. You track closure of each with the responsible engineers. No modifications are implemented until all safety-critical actions are closed.

---

# Simulation 5: Writing an IADC Daily Drilling Report

**Context:** You are a field engineer on a drillship. The driller has just completed Day 12 of a well. You must write the IADC Daily Drilling Report (DDR). This goes to the operator, the drilling contractor, and ANPG.

---

### IADC DDR Template (Simplified)

```
═══════════════════════════════════════════════════════════
IADC DAILY DRILLING REPORT — CONFIDENTIAL
═══════════════════════════════════════════════════════════
Well Name: GD-1                    Block: 32           Date: [Today]
Rig Name: Valaris DS-12            Water Depth: 1,847m  Day #: 12
Operator: TotalEnergies            AFE No: B32-GD1-001

DEPTH STATUS
───────────────────────────────────────────────────────────
Depth at Start of Day: 3,380m MD / 3,363m TVD
Depth at End of Day:   3,502m MD / 3,484m TVD
Drilled Today:          122m
Total Depth:            3,502m MD

BIT INFORMATION
───────────────────────────────────────────────────────────
Bit: SLB PDC 8½" M22K series         Bit #4
On bottom: 3,380m                    Off bottom: —
Hours on bit: 48 total (14 today)    ROP: 8.7 m/hr avg (today)
WOB: 12–16 klbs                      RPM: 120–140

MUD PROPERTIES
───────────────────────────────────────────────────────────
Mud type: SLB Versadril (OBM)        Density: 1.42 SG
FV: 52 sec/qt                        PV: 18 cP
YP: 9 lb/100ft²                      HPHT filtrate: 2.8 mL
Oil/Water ratio: 80/20               Chlorides: 28,000 mg/L

DAILY ACTIVITIES (chronological log)
───────────────────────────────────────────────────────────
00:00–06:00  Drilled 3,380m to 3,430m @ avg 10 m/hr. Pulled back 
              to 3,340m for survey. Survey at 3,430m: Inc 43.5°, 
              Azm 287.2°. On target +0.2° inc from plan. Drilled ahead.

06:00–08:30  Drilled 3,430m to 3,465m. ROP slowing to 7 m/hr — 
              possible formation change.

08:30        SAND ENTRY at 3,468m. GR dropped from 85 API to 22 API.
              Resistivity 28 ohm·m (deep). High oil saturation indicators.
              Company man notified. ROP reduced to 8 m/hr for log quality.

08:30–12:00  Drilled 3,468m to 3,488m in sand. GR stable 18–25 API.
              Excellent reservoir quality.

12:00–14:00  Wiper trip from 3,488m to 3,380m (2,108m pulled back).
              No tight spots. Back on bottom 14:30.

14:30–18:00  Drilled ahead 3,488m to 3,502m. GR rising slightly 
              (25 → 38 API) — possible sand/shale interbed.

18:00–24:00  Continued drilling. Surveying in progress at 24:00.

NPT (Non-Productive Time): 0 hours today
Flat time: 2 hrs (wiper trip)

SAFETY
───────────────────────────────────────────────────────────
Stop Work Authority exercised: No
Near misses: No
Incidents: No
Safety observation cards submitted: 7

UPCOMING OPERATIONS
───────────────────────────────────────────────────────────
Tomorrow: Continue drilling to TD at ~3,550m (as per prognosis).
Expected: Run wireline LWD confirmation logs before casing decision.
If GR remains in sand: drill to 3,570m for a full reservoir penetration.

Company Man signature: ____________  Date: ____________
═══════════════════════════════════════════════════════════
```

---

# Simulation 6: Preparing for a Job Interview at SLB Angola

**Context:** You have a phone screen with SLB Angola's recruiting team in 3 days. Then a technical interview with a Senior Field Engineer. This simulation prepares you for both.

---

### Phone Screen (20 minutes)

The recruiter's questions are not deeply technical. They assess:
1. Communication clarity in English
2. Motivation (why SLB, why Angola, why offshore)
3. Baseline awareness of the role

**Practice answers:**

Q: "Why do you want to work as a field engineer at SLB?"
> "I'm completing my petroleum engineering degree at ISPTEC and I want to start my career with the best technical training available. SLB is the largest oilfield services company in Angola — working on Block 17 and Block 32 wells means working on the most technically complex deepwater completions in Africa. I specifically want the MWD/LWD track because I enjoy the real-time technical decision-making aspect — you're reading the geology as you drill, and your decisions directly affect the well outcome. I also know SLB has the best graduate training program in the industry, and that foundation will serve my entire career."

Q: "What do you know about Angola's oil sector?"
> "Angola is sub-Saharan Africa's second-largest oil producer at about 1.16 million barrels per day. The main deepwater operators are TotalEnergies on Block 17 and 32, Azule Energy on Block 15 and 18, Eni on Block 3 and 15/06, and Chevron on Block 0. Production has been declining due to mature fields, but there's a new investment wave — Agogo, Kaminho, and Begonia are all sanctioned or close to it. Angola left OPEC in 2024 to attract more upstream investment. There's also a massive refinery expansion underway with SonaRef and Soyo. SLB has major service contracts on all these blocks, so it's an excellent time to join."

---

### Technical Interview (45 minutes)

The senior field engineer will ask you to solve real problems. Prepare these categories:

**Category 1: Pressure calculations**

Q: "A well at 3,200m TVD has a mud weight of 1.38 SG. What is the hydrostatic pressure at the bottom of the hole?"

$$P_{hyd} = \rho \times g \times h = 1,380 \times 9.81 \times 3,200 = 43.3 \text{ MPa} = 433 \text{ bar}$$

Or using field units: $P_{hyd} = 0.052 \times MW_{ppg} \times TVD_{ft} = 0.052 \times 11.5 \times 10,499 = 6,282 \text{ psi}$

Practice converting between SG, ppg, psi/ft, and bar until these are automatic.

**Category 2: Well control**

Q: "You are drilling at 3,500m with MW 1.40 SG. You see a pit gain of 2 m³ and the well starts flowing. What do you do and what do you check first?"

Answer framework:
1. Pick up off bottom (lift bit 3–5m)
2. Shut in the well (soft shut-in: open choke, close annular, monitor)
3. Read SIDPP and SICP after 5 minutes
4. Calculate kill mud weight
5. Notify company man/OIM
6. Implement well control procedure (Driller's or Wait & Weight)

**Category 3: Interpretation**

Q: "Your GR log shows 90 API in one zone and 15 API in another. Your resistivity shows 45 ohm·m in the 15 API zone. What does this tell you?"

Answer: GR 90 API = shale or clay-rich zone. GR 15 API = clean sand (very low clay). Resistivity 45 ohm·m in clean sand = hydrocarbon-bearing (water-wet sand would show 0.5–3 ohm·m). This is a prospective oil or gas interval. Calculate porosity from density log if available, then apply Archie's equation to get Sw.

---

*Related: [01_Well_Control_Tutorial.md](01_Well_Control_Tutorial.md) | [07_HSE_Offshore_Tutorial.md](07_HSE_Offshore_Tutorial.md) | [Angola_Employability_Market_Intelligence.md](../support/Angola_Employability_Market_Intelligence.md)*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
