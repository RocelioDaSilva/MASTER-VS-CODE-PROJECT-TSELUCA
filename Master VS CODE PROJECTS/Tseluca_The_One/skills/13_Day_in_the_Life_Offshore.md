# A Day in the Life — Offshore Angola
## Hour-by-Hour Reality Guide for Every Major Role

> This is what your day actually looks like. Not theory. Not a textbook. The real schedule, the real forms, the real tools, the real conversations. Read this so that when you arrive, nothing is a surprise.

---

## The FIFO Framework

**FIFO = Fly In, Fly Out.** You work a rotation (e.g., 28 days on, 28 days off) and fly to the facility by helicopter or vessel. During your 28 days on, you work every single day. You live on the installation. When your rotation ends, you fly back to Luanda and have 28 days completely off.

**Schedule types you'll encounter in Angola:**
- 28/28 (28 on / 28 off): Most service company field engineers on Angola drillships
- 21/21: Production operators on many Angola FPSOs (TotalEnergies, Azule)
- 14/14: Some short-rotation specialist roles (BOSIET mandated max 14 days without refresher on some platforms)
- 28/28 vs 21/21: 28/28 gives higher per-day rate but less home time; 21/21 is better for family life

**Shift patterns:**
- Most facilities operate 12-hour shifts (06:00–18:00 and 18:00–06:00)
- Night shift is "B shift"; day shift is "A shift"
- New arrivals often start on night shift

---

# Role 1: Drilling Engineer (Field) — Drillship, Block 32

**Rotation:** 28 days on the Valaris DS-12 (or similar). Water depth 1,850m. Drilling an 8½" production well for TotalEnergies.

---

## 05:30 — Wake Up

Your cabin (called an "accommodation unit") has:
- Single bed (good mattress — offshore companies know you need sleep to function safely)
- Small desk, TV, telephone
- Ensuite bathroom (on modern drillships)
- Air conditioning (important — Angola offshore is hot and humid)

You wake up 30 minutes before the shift handover. The ship's intercom announces: "Day shift personnel, please prepare for morning handover." (Yes, it's in English on international drillships — even in Angola.)

**Before leaving your cabin:**
- Hard hat, safety glasses, steel-toed boots (always — even walking to the mess)
- Coveralls (company-branded PPE — SLB green, Halliburton red, etc.)
- Pen and notebook (you write things down constantly)
- Your radio (company radio, channel assigned to your group)

---

## 06:00 — Morning Handover at the Driller's Console

You walk to the driller's console (also called the "dog house") on the drill floor. It smells of pipe dope, hydraulic oil, and coffee. Night shift is still running.

The night shift Drilling Engineer (a Brazilian named Carlos, 8 years at SLB) is at the whiteboard:

> "Morning. So here's the situation. We're at 4,020m MD, 3,998m TVD. Drilling the 6" horizontal section. We've been in the reservoir since 3,820m — full 200m of clean sand (GR consistently 15–22 API, Rt 25–40 Ω·m). ROP has been good: 11–14 m/hr overnight.
>
> One issue: at 3,990m there was a short 4m shale break — GR jumped to 65 API, Rt dropped to 5 Ω·m. The DD kicked the bit down 0.3° and we're back in clean sand at 3,994m. Staying in the pay zone.
>
> Mud weight 1.38 SG, ECD 1.42 SG. Pore pressure prognosis at this depth: 1.35 SG. We have +0.03 SG overbalance which is a bit low for my liking in this section — recommend watching the trend closely. If ROP spikes without explanation, be ready to shut in.
>
> BHA has been in hole 7 days. PDC bit has 84 hours on it — getting near time to POOH (pull out of hole) and inspect. Based on current drill-out rate, we'll reach TD ~4,120m in 2 days, then run wireline and pull BHA.
>
> Nothing unusual on surface equipment. TQI (torque), drag, and pump pressures all nominal. The MWD engineer (Fatima, SLB LWD) is in the cabin — LWD logs are excellent quality.
>
> No HSE events on my shift. One stop work: the roughneck wanted to shortcut the floor prep before the connection — I had him do it properly. Documented in shift log. Go well."

You sign the handover log. Carlos signs it. He goes to breakfast and then bed.

---

## 06:15 — Review the Night Data

You sit at the drilling engineer's workstation. You pull up:

**1. The real-time drilling dashboard (EDR — Electronic Drilling Recorder):**
```
CURRENT DRILLING PARAMETERS
────────────────────────────────────────────────────
Bit Depth:       4,020m MD
WOB:             18 klbs
RPM:             175 rpm (rotary + RSS)
ROP:             12.4 m/hr
Torque:          28 kft·lb  (normal for 6" hole at this depth)
Pump Rate:       220 gpm
Pump Pressure:   3,850 psi
ECD (from PWD):  1.42 SG
Pit Volume:      185 m³  (stable — no gain/loss)
```

**2. The LWD real-time log:** Download the overnight LAS file from the SLB Wellsite Geologist server. Open in your PDF viewer. Review the last 150m of reservoir. Clean sand throughout except the 4m shale break Carlos mentioned. Oil indicators all strong.

**3. The drilling fluid report:** The mud engineer's midnight sample:
```
Mud type: OBM (SLB Versadril)
Density: 1.38 SG ✓
FV: 45 sec/qt ✓
PV: 16 cP ✓
YP: 8 lb/100ft² ✓
HPHT filtrate: 2.2 mL (limit: <4.0) ✓
O/W ratio: 80/20 ✓
Chlorides: 31,000 mg/L (tracking formation water salinity)
Status: All good
```

---

## 07:00 — Morning Safety Meeting (Stand-Up)

Every day, at 07:00, the senior personnel meet in the conference room:
- Company Man (the TotalEnergies representative, most senior person on the rig)
- Drilling Contractor toolpusher (Valaris)
- HSE Officer
- Department heads: Mud, Cement, Directional, LWD/MWD, Maintenance

The Company Man runs the meeting (~15 minutes):
1. **Yesterday's operations summary** (brief)
2. **Today's plan** — what we're drilling, any BHA change, any casing run
3. **Safety moment** (always first) — one HSE topic, rotated among team members. Today: "Dropped object prevention on the drill floor during connection." Five minutes of focused safety discussion.
4. **Any concerns?** Open floor.
5. **Permit to Work:** Any new work activities starting today that require a PTW? Yes — the maintenance team wants to change a pump impeller on the mud pump #2. "Make sure you have the isolation and energy lock-out before any work begins. Maintenance — confirm with HSE Officer."

You leave the morning meeting with today's drilling plan locked in your head:
- Continue drilling to 4,080m (60m today at ~11 m/hr = ~5.5 hours of drilling)
- At 4,080m: pump sweep (40 bbl high-viscosity pill to clean cuttings)
- After sweep: drill ahead to 4,120m (TD)
- At TD: circulate bottoms up (3 bottoms-up circulations), pull BHA, run cement plug

---

## 08:00 — Active Drilling: Your Monitoring Routine

You are drilling. The driller is in the console. You are in the engineering office 30m away, watching the same real-time data on your workstation and available on radio.

**Every 30 minutes, you check:**
1. **Pit volume trend** — is it increasing (kick) or decreasing (lost returns)?
2. **ECD** — is it trending toward the fracture gradient? (Current: 1.42, limit: 1.52 SG)
3. **ROP** — sudden spike = could be formation change or kick
4. **Torque** — trending up = bit wear or formation hardening; sudden spike = possible packoff
5. **Pump pressure** — sudden drop = washout in drill string or BHA; sudden rise = plugged bit nozzle

**The driller calls you at 09:15:**
"We had a brief torque spike — jumped from 28 to 38 kft·lb for about 2 minutes, then came back down to 29. ROP was steady throughout. Pit volume stable."

You think: Torque spike with stable pit, stable ROP, stable pump pressure. Likely cause: momentary packoff (cuttings compacted in the annulus, then cleared). **Not a well control issue. Monitor.**

Your action: Reduce drilling parameters slightly (WOB from 18 → 16 klbs) for 15 minutes to be cautious. Log the event: "09:15 — 2-min torque spike 38 kft·lb. Likely packoff. Cleared. Reduced WOB 16 klbs. Monitoring."

---

## 10:30 — IADC Daily Drilling Report: Filling the Previous Day's Report

Every morning, the drilling engineer completes the previous day's IADC DDR. See Simulation 5 in [11_Practical_Workflow_Simulations.md](11_Practical_Workflow_Simulations.md) for the full format. This report is submitted to:
1. TotalEnergies (Company Man reviews and approves)
2. Drilling contractor (Valaris retains for their records)
3. SLB (your company retains for contract records)
4. ANPG (submitted as part of the well operations log — monthly compendium)

**Time to write:** 30–45 minutes. Be accurate. The DDR is a legal record.

---

## 12:00 — Lunch

The galley (mess hall) is open from 11:30 to 13:00 for the day shift. On a modern drillship:
- Full hot meals, salad bar, dessert
- 24-hour coffee and tea station
- Special dietary options

You have 30–45 minutes. You eat with the roughnecks, the MWD engineer, whoever is on break. A lot of the real knowledge transfer happens over lunch. "How did that Block 17 well handle the narrow window in the 12¼" section last month?" — real conversations that teach you more than any manual.

---

## 13:00 — Reach TD: The Sequence of Events

**13:42:** Bit touches 4,120m — **Total Depth reached.** The directional driller announces on the radio: "TD, TD, TD — 4,120m MD, 4,097m TVD, Inc 87.2°, Azm 287°." You respond: "Confirmed. Begin bottoms-up circulation."

The sequence from TD to pulling the BHA:

**1. Bottoms-up circulation (14:00–16:30):**
The mud pump pumps fresh mud down the drill string. It sweeps all cuttings that are sitting in the annulus up to surface. One "bottoms-up" = the time for mud to travel from bit to surface (function of annular volume and flow rate). With 4,120m of 6" hole in an 8½" annulus:
- Annular volume ≈ 47 m³
- Flow rate: 8 bbl/min
- Bottoms-up time: 47 m³ / (8 × 0.159 m³/min) = 37 minutes per circulation
- You circulate 3 times = ~1.9 hours

**2. Survey (16:30):** Final directional survey. This locks in the well trajectory endpoint for the permanent record.

**3. Wiper trip (16:30–18:00):** Pull the drill string back up to the 9⅝" shoe (2,800m), then run back to TD. This "wipes" the wellbore — cleaning cuttings off the walls and checking for tight spots (stuck pipe indicators). If the pipe catches anywhere, you know there's a problem.

**18:00 — End of shift.** You hand over to the night shift engineer. The BHA POOH (pull-out-of-hole) will run overnight.

---

## 18:00 — Evening Handover

You give the incoming engineer:

> "We reached TD at 4,120m at 13:42. Circulated 3 bottoms-up, no shows (no hydrocarbons seen at surface — oil-based mud so no direct hydrocarbon show visible, but we confirmed by LWD). Wiper trip in progress — currently at 3,600m pulling back. No tight spots encountered yet. Survey confirmed. POOH all the way overnight, surface expected ~03:00. Bit and BHA inspection on deck by morning meeting. Cement plug scheduled for tomorrow afternoon pending inspection results.
>
> ECD was 1.42 SG throughout the day. No well control events. Mud weight stable at 1.38 SG.
>
> Watch for tight spots between 3,820m and 4,120m (reservoir section) — we had one minor packoff at 09:15 but it cleared. If the string catches on POOH, set down weight, pick up slowly. Call me if it doesn't free up easily."

Sign the handover log. Walk to the mess for dinner. Then: gym (many drillships have a gym), call family, read, sleep.

**Repeat for 28 days.**

---

# Role 2: Production Operator — FPSO One Santos (Block 17, Yinson)

**Rotation:** 21/21. The One Santos FPSO processes ~85,000 STB/day from Block 17 wells.  
**Note:** The production operator role is distinct from the production engineer. The operator monitors and operates the plant; the engineer designs and optimizes. Many ISPTEC graduates start as operators before moving to engineer roles.

---

## 05:50 — Pre-Shift Check

You arrive at the control room 10 minutes before your shift starts. This is professional culture: showing up on time for handover means showing up 10 minutes early.

The control room has:
- 8 large ICSS (Integrated Control and Safety System) monitors showing process values
- One operator station per process system (inlet, separation, compression, export, water treatment)
- A large overview screen showing FPSO-wide status

---

## 06:00 — Shift Handover (Control Room)

The night shift lead operator walks through the FPSO status board:

> "Current production: 83,400 STB/day. All 20 producing wells online. No shutdowns overnight.
>
> Separator Train B had a brief pressure fluctuation at 03:15 — PCV (pressure control valve) hunting. Maintenance adjusted the tuning — it's stable now. Watch PCV-201B this morning.
>
> Gas compression: both compressors running. Compressor 2 outlet temperature is trending up — 145°C vs design 140°C. Not yet at alarm, but it's a flag. Notified maintenance. They'll look at it at 09:00.
>
> Export pump 1 running, pump 2 on standby. Crude export started at 04:30 for an SPM loading — tanker is alongside. Expected loading complete at 10:00. Export rate 55,000 BPH.
>
> Water injection: 40,000 STB/day injection into Block 17 wells. All WI pumps running normal.
>
> Produced water: 18,500 m³/day, oil in water = 22 ppm (limit 29 ppm per MARPOL). All good.
>
> Nothing unusual. Have a safe shift."

You and the outgoing operator both sign the handover logbook. Physical signature, ink, in the logbook. Every shift.

---

## 06:30 — First Field Round

The most important habit of a good process operator: **you leave the control room and walk the plant.** Control room screens tell you what instruments read. A field round tells you what you can see, hear, smell, and feel.

**First-round checklist (from memory, confirmed against printed checklist):**

**Separation Deck:**
- [ ] Train A separator: Check level gauge (should read 45–55%). Check flanges for leaks (look for liquid drips, wet marks). Listen — does the separator sound normal (steady flow noise) or different (banging, surging)?
- [ ] Train B separator: Same checks. Look at PCV-201B — is it hunting (cycling rapidly) or steady?
- [ ] Meter skid: Check that the export meter is spinning (confirms crude is flowing to export pump)

**Compression Deck:**
- [ ] Compressor 1: Vibration levels on the indicator panel. Listen for any unusual noise. Check oil level sight glass.
- [ ] Compressor 2: Check the outlet temperature gauge. It reads 147°C now. You write it in your log: "06:35 — Comp 2 outlet temp 147°C, slightly above design 140°C. Reported to maintenance, monitoring."

**Chemical injection:**
- [ ] Corrosion inhibitor: Tank level (must be >30% to maintain continuous injection). Level: 48%. Good.
- [ ] Scale inhibitor: Level 65%. Good.
- [ ] Demulsifier: Level 52%. Good.

**Fire and Gas Panel Check:**
- All F&G detectors on deck showing green (no detection). If any detector shows fault: report immediately to HSE supervisor.

**Duration of field round:** 45–60 minutes. You cover 2km of walkway in this time.

---

## 07:30 — Control Room Monitoring

Back in the control room. You monitor the ICSS screens. Your specific responsibility: **Gas Compression and Export System.**

Key parameters you watch:
```
Compressor 1:
  Suction pressure: 4.8 bar (design: 4.5–5.5 bar) ✓
  Discharge pressure: 35.2 bar ✓
  Speed: 6,200 RPM ✓
  Vibration: 2.8 mm/s (alarm at 7.5) ✓
  Seal gas flow: 120 Nm³/hr ✓
  Outlet temperature: 139°C ✓

Compressor 2:
  Suction pressure: 4.9 bar ✓
  Discharge pressure: 35.1 bar ✓
  Speed: 6,195 RPM ✓
  Vibration: 3.1 mm/s ✓
  Outlet temperature: 147°C ← TRENDING HIGH
  Seal gas flow: 118 Nm³/hr ✓
```

At 08:15, Comp 2 outlet temperature reaches 151°C. **Alarm set at 150°C.** ICSS alarm activates.

You follow the alarm response procedure:

1. **Acknowledge the alarm** in the ICSS (stops the audible alarm, keeps the visual flag).
2. **Assess:** Is this a process upset or an instrument fault? Temperature has been rising steadily for 2 hours — this is real, not a sensor fault.
3. **Notify:** Call the maintenance lead on the radio: "Comp 2 outlet temp alarm at 151°C. I'm watching it. Can you check the intercooler cooling water flow?"
4. **Take action:** Slightly reduce Comp 2 load by 5% (trim the speed) to reduce heat generation. Monitor.
5. **Document:** "08:15 — Comp 2 outlet temp alarm 151°C. Reduced speed 5%. Maintenance notified (intercooler check). Monitoring."

Maintenance checks: intercooler has low cooling water flow — one fouled strainer. They clean it at 10:00. Temperature drops back to 141°C. Crisis avoided. You log the resolution: "10:25 — Comp 2 temp 141°C post intercooler strainer cleaning. Resumed normal operation."

---

## 09:00 — Morning Meeting (Production Operations)

Every day, the operations supervisor, production engineer, HSE engineer, and department leads meet:
- **Production status:** 83,400 STB/day vs 85,000 target. 1,600 bbl/day gap. Why?
- **Root cause:** Well G-09 was tested yesterday — allocation factor revision shows it's producing less than previous estimate. This reduces the FPSO total slightly.
- **Action:** Schedule a detailed test on G-09 this week to confirm the new performance.
- **Export:** Tanker loading on schedule, complete by 10:00. Next tanker in 5 days. Ensure we have enough storage volume (~4 days of production in tanks) to accommodate.
- **Safety:** Yesterday's safety observation cards (SOCs): 12 submitted, 2 required follow-up (a damaged handrail on deck 4, and a leak from a drain valve). Both assigned to maintenance with due dates.

---

## 10:00 — Crude Export Completion + Paperwork

The cargo tanker finishes loading at 10:05. Cargo: 450,000 barrels of Dalia crude (API 23.7°, BS&W 0.28%).

You complete the **Cargo Measurement Certificate:**
```
Vessel: MT ANGOLA TRADER
Bill of Lading No.: BL-2024-047
Loading Port: One Santos FPSO, Block 17
Date of Loading: [Today], 04:30–10:05

Opening Gauge (FPSO tank): 1,235,840 barrels
Closing Gauge (FPSO tank): 785,840 barrels
Gross Quantity Transferred: 450,000 barrels

Quality:
  API Gravity: 23.7° @ 60°F
  BS&W: 0.28% (max 0.5%) PASS
  Reid Vapor Pressure: 12.4 psi (max 14 psi) PASS
  Sediment: 0.01% (max 0.1%) PASS

Certified by: [Your name], Production Operator, One Santos FPSO
```

This document goes to:
1. TotalEnergies/Yinson commercial department
2. The tanker captain (they get a certified copy)
3. ANPG (for royalty and cost oil calculation)

---

## 12:00–18:00 — Second Field Round, Monitoring, Permit to Work

**14:00 — Second field round:** Same route as morning. Document any changes.

**15:30 — Permit to Work (PTW) activity:** The maintenance team needs to replace a pump seal on the produced water lift pump. This requires:
- Isolation of the pump (electrical, mechanical)
- LOTO (Lock-Out, Tag-Out) — physical locks on energy sources
- You (operations) must sign the PTW as "Area Authority" — you confirm the area is safe for the work and the equipment is properly isolated
- Gas test (check for hydrocarbon gas at the worksite) — HSE Officer tests: 0% LEL. PASS.
- Signature: you sign the PTW permit.
- Work begins.

**17:45 — Shift handover preparation:** Write your shift summary. By 18:00 you hand over to the incoming operator. Same format as the morning handover you received.

---

# Role 3: HSE Engineer — FPSO Dalia (TotalEnergies)

## Typical Day Structure

The HSE Engineer on an FPSO is not primarily administrative — they are active on the deck daily.

**06:00–07:00:** Shift handover + review overnight HSE log. Any incidents? Any near misses? Review safety observation cards submitted on night shift.

**07:00–07:30:** Morning safety meeting (see drilling role above — same structure).

**08:00–09:00:** PTW review. As the HSE engineer, you review all active permits for the day. For complex work (hot work, confined space entry, lifting operations, working at height), you must personally inspect the worksite and verify controls are in place before signing.

**09:00–11:00:** Field observation rounds. You walk the decks specifically looking for:
- Uncontrolled ignition sources (grinding without permits, smoking in unauthorized areas)
- Physical hazards (damaged scaffolding, unsecured equipment, slippery surfaces)
- Personnel behavior (PPE compliance, phone use in restricted areas)
- Life safety equipment (lifebuoys, fire extinguishers — in place and accessible?)
- Environmental: are chemical drums properly labeled and bunded?

**11:00–12:00:** Safety observation card (SOC) review and follow-up. You track every card to closure. Today there are 15 open cards. 8 are "closed." 7 need action.

**13:00–15:00:** HAZOP review session (if a modification is being studied — see Simulation 4).

**15:00–16:30:** Incident investigation. There was a minor hand injury yesterday (a technician cut his hand on a sharp edge during maintenance). You conduct the ICAM investigation:
- Sequence of events (what happened, step by step)
- Contributing factors: was the sharp edge guarded? Was a risk assessment done? Was PPE being worn (gloves)?
- Root cause: Sharp edge not identified in pre-task risk assessment (JSA not thorough).
- Corrective action: Revise the JSA template to include "inspect for sharp edges" as a specific check. Brief the maintenance team.

**16:00–17:30:** Compile the daily HSE statistics:
```
Day 47 of rotation (Block 17 Dalia FPSO)
LTI (Lost Time Injuries) YTD: 0
RWC (Restricted Work Cases) YTD: 0
MTC (Medical Treatment Cases) YTD: 1 (hand laceration, today)
FAC (First Aid Cases) YTD: 3
Near Miss reports: 14
Hazard observations (SOCs): 267

Hours worked this week: 3,840 person-hours (320 people × 12 hrs/day × 1 day)
TRIR this week: (1 MTC / 3,840) × 200,000 = 52.1 (tracking — above our 30-day rolling average target of 35)
```

**18:00:** Handover. Document the MTC, the corrective actions, and the status of all open PTWs.

---

# The Non-Negotiable Daily Habits of Offshore Professionals

Regardless of your role, these habits separate the professionals who advance from those who don't:

**1. Never skip the handover.** If you miss even one handover detail and something goes wrong, it's on you. Always be early, always be thorough.

**2. Write everything down.** The offshore industry runs on documentation. If it's not written, it didn't happen.

**3. Do your field rounds, every time.** The screen is good. Being on the deck is better. You catch things with your eyes and ears and nose that no instrument reports.

**4. Speak up when something is wrong.** Stop Work Authority (SWA) means every single person — trainee included — has the right and RESPONSIBILITY to stop any unsafe work. Use it. You will not be penalized. You will be respected.

**5. Sleep when you're off shift.** Fatigue is the silent killer offshore. When you're tired: 28% slower reaction time, 28% more likely to make errors. Your shift is 12 hours. Use the other 12 to sleep (8 hours) and decompress (4 hours).

**6. Maintain your certifications.** BOSIET is 4 years. IWCF is 2 years. Medical certificate is 2 years. Yellow fever vaccination is 10 years. Let any of these expire and you cannot board. Know your expiry dates.

---

*Related: [11_Practical_Workflow_Simulations.md](11_Practical_Workflow_Simulations.md) | [01_FIFO_Life_Decoded.md](../01_FIFO_Life_Decoded.md) | [07_HSE_Offshore_Tutorial.md](07_HSE_Offshore_Tutorial.md)*  
*Certifications for going offshore: [Certifications Angola](../support/Certifications_Angola.md) | [Learning Resources](../../../docs/learning-resources.md)*
