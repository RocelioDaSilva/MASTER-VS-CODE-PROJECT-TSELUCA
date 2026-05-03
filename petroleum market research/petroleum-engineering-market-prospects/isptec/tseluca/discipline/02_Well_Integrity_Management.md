# Well Integrity Management
## The Discipline That Keeps Wells Safe for Their Entire Life

---

## What Is Well Integrity?

Well integrity is the application of technical, operational, and organisational solutions to reduce the risk of uncontrolled release of formation fluids throughout the life cycle of a well.

In simple terms: a well must contain its pressure at all times. If it fails to do so, you have a blowout — the most catastrophic event in the industry.

Well integrity is not the same as well control. Well control is what you do when a kick occurs (emergency response). Well integrity is the ongoing engineering that prevents the well from getting into that situation in the first place.

**The governing standard:** NORSOK D-010 "Well Integrity in Drilling and Well Operations" — the most widely used well integrity standard internationally. Used by TotalEnergies, Eni, and Azule in Angola.

---

## The Barrier Concept

The entire well integrity discipline is built on one concept: **two independent pressure barriers must exist at all times** between the reservoir and the environment.

```
SURFACE / ATMOSPHERE
      │
──────┼───────  ← Barrier 1 (e.g., DHSV + tubing/wellhead/Christmas tree)
      │
 PRODUCTION
    ZONE
      │
──────┼───────  ← Barrier 2 (e.g., casing + cement + formation)
      │
RESERVOIR PRESSURE
```

If Barrier 1 fails (e.g., DHSV leaks), you still have Barrier 2. If Barrier 2 also fails, you have a blowout.

**The two-barrier philosophy:** Every well must have two independent barriers. Any time a well has only one barrier, it is in a "barrier lost" situation — work must stop on the well and it must be either restored to two barriers or shut in.

This philosophy governs every decision a well integrity engineer makes.

---

## Barrier Elements

Barriers are made up of individual elements. A barrier envelope is a combination of elements that together form one complete barrier.

### Primary Barrier Elements (typical producing well)
- Downhole Safety Valve (DHSV): closes the tubing in case of emergency
- Production tubing: the conduit from reservoir to surface
- Tubing hanger and seal assembly: seals the top of the tubing in the wellhead
- Christmas tree: the valve assembly on top of the wellhead
- Tree cap and plugs: redundant seals in the tree body

### Secondary Barrier Elements (typical producing well)
- Cemented production casing: the casing that isolates the producing zone
- Casing hanger and seal assembly: seals the casing in the wellhead
- Cement behind the production casing: isolates the annulus from the reservoir
- Formation itself: the rock provides the outermost containment

**Key insight:** If the cement behind the casing has a channel (a common failure), the secondary barrier may already be compromised — even if the well appears to be producing normally. This is why well integrity surveillance (measuring annulus pressures) is critical.

---

## Annulus Pressure Monitoring

For a producing well, the wellbore has multiple annuli (annular spaces between concentric tubulars):

```
TUBING ← Production conduit
  │
A-annulus: between tubing and production casing
  │
B-annulus: between production casing and intermediate casing
  │
C-annulus: between intermediate casing and surface casing
  │
D-annulus: between surface casing and conductor
```

Each annulus should be at a known pressure (often atmospheric or with a small positive pressure from gas migration).

**Sustained Casing Pressure (SCP):** When an annulus builds pressure that returns after bleeding, it indicates a continuous source of fluid (gas or liquid) leaking from somewhere. SCP is a well integrity failure that must be investigated and managed.

**Angola context:** SCP is common in mature fields. Many of Angola's Cabinda (Block 0) wells, some drilled in the 1970s and 1980s, have SCP that has been managed for decades. The Well Integrity Engineer's job is to classify the risk (is it acceptable with monitoring? Does it need intervention?) and maintain a management plan.

---

## Well Integrity Failure Categories

Not all integrity failures are equal. The API 100-2 standard and NORSOK D-010 classify failures by type and severity:

### By Location
| Location | Failure Type | Implication |
|----------|-------------|-------------|
| Tubing | Hole, split, corrosion | Bypasses primary barrier — critical |
| DHSV | Fails open, fails to seal | Primary barrier lost — critical |
| Cement | Channelling, debonding | Secondary barrier compromised |
| Casing | Corrosion, collapse, parted | Major structural failure |
| Wellhead/tree | Seal failure, valve leak | Surface containment breach |
| Completion packers | Packer bypass | Annular isolation lost |

### By Severity
- **Category 1 (Red):** Well shut in immediately — loss of containment risk is imminent
- **Category 2 (Amber):** Well continues producing with enhanced monitoring and repair scheduled within defined timeframe
- **Category 3 (Green):** Minor anomaly, documented and monitored

Most operators use a Well Integrity Status (WIS) system — a database of every well's barrier status, updated by the Well Integrity Engineer after each surveillance event.

---

## The Well Integrity Engineer's Daily Work

This role exists in every operating company. In Angola, TotalEnergies, Azule, Eni, Chevron, and Sonangol all have Well Integrity teams.

**Daily responsibilities:**
1. Review annulus pressure readings from all producing wells
2. Classify any new SCP observations
3. Update the Well Integrity Status database
4. Coordinate DHSV testing schedule (DHSVs must be tested periodically — typically every 6 months)
5. Plan leak-off tests and pressure integrity tests for new wells
6. Review DHSV pull requests (when a DHSV fails, it must be pulled and replaced by wireline)
7. Write Well Integrity Reports for management and ANPG

**Less frequent responsibilities:**
- Lead well integrity assessments for acquisition/divestiture (due diligence)
- Design workovers for wells with integrity failures
- Write P&A programs for late-life wells
- Conduct root cause analysis for integrity failures
- Input to new well design (barrier philosophy for the new well's life)

---

## DHSV: The Most Important Barrier Element

The Downhole Safety Valve (DHSV) is the deepest valve in the well. It is installed in the upper completion tubing, typically 30–150m below the mudline (for subsea wells) or below surface in platform wells.

**Why it matters:** If a surface emergency occurs (fire, collision with FPSO), the DHSV closes automatically — isolating the well below the seabed. Without it, the well would flow uncontrolled to the surface fire.

### DHSV Design
- **Type:** Flapper type (most common) or ball type
- **Control line:** A hydraulic control line runs from the DHSV up through the tubing-annulus to the tree. Pressure in this line keeps the valve open. If pressure is lost, the valve closes automatically (fail-safe closed).
- **Test:** DHSV must be tested periodically. The standard test: close the DHSV, bleed the tubing above it, confirm no flow. If pressure builds above the closed DHSV, it has a leak — failed test.

### DHSV Failure Modes
| Failure Mode | Cause | Consequence |
|-------------|-------|-------------|
| Fails to close | Flapper stuck open (scale, asphaltene) | Loss of subsurface barrier |
| Fails to open | Control line blocked or broken | Well shut in (not a safety failure, but an operational problem) |
| Leak through closed valve | Worn flapper seal, debris on seat | Primary barrier degraded |
| Control line leak | Corrosion, fatigue at connection | DHSV may fail to open when needed |

**Angola deepwater note:** In subsea wells, the control line runs up through the umbilical all the way to the FPSO. A leak or break in this 2km+ control line will prevent the DHSV from opening. Control line integrity is a specific surveillance item on all Angola subsea wells.

---

## Cement as a Barrier

Cement behind the production casing is the secondary barrier. It is placed there during well construction and must maintain its integrity for the entire field life (20–30 years).

**Why cement fails:**
- Poor cement placement (channels in the cement column during primary cementing)
- Thermal cycling (from injecting cold seawater or from steam injection)
- Pressure cycling (production and shut-in cycles flex the casing)
- CO₂ degradation (CO₂-containing gases dissolve cement over time — carbonate formation)
- Mechanical damage during perforation

**Detecting cement problems:**
- Cement bond log (CBL/USIT) — acoustic log run after cementing, during construction
- Annulus pressure buildup — the first indication of a cement channel in service
- Temperature surveys — temperature anomalies can indicate fluid migration behind casing

**Angola-specific issue:** Many old wells in Cabinda were cemented with older technology. Cement quality varies. This is why the Block 0 P&A program (as Cabinda fields approach end of life) requires careful cement evaluation before each P&A operation.

---

## Well Life Cycle Integrity Events

Well integrity management happens at every stage of the well's life:

### During Construction (Drilling)
- Leak-off test (LOT) / formation integrity test (FIT) at each casing shoe — confirms the casing shoe cement and shoe track can hold pressure
- Primary cementing: bond logs run to verify cement quality
- Casing pressure tests: each casing string is pressure-tested before proceeding
- Wellhead and tree factory acceptance testing

### During Completion
- Packer setting and testing: the completion packer must hold against reservoir pressure
- DHSV installation and function test
- Tubing pressure test
- Annulus pressure testing

### During Production (Operating Life)
- Periodic DHSV function tests (every 6 months typically)
- Annulus pressure monitoring (daily — automatic from SCADA)
- Wellhead leak checks (visual and sensor-based)
- Well integrity status updates after each well intervention

### During Intervention (Workover/Wireline/Coiled Tubing)
- Well kill or well conditioning prior to any intervention
- Barrier documentation for each phase of the operation
- Barrier restoration after intervention

### During P&A (End of Life)
- Establish permanent barriers: cement plugs across the production zone, across all hydrocarbon-bearing intervals, and at the wellhead
- Remove all surface equipment
- Verify barrier integrity before final abandonment

---

## P&A (Plug and Abandonment) Engineering

P&A is the well integrity discipline's final act. Every well that has ever been drilled must eventually be abandoned — permanently.

**Why P&A is technically demanding:**
- You are working in a well that may be 30–50 years old
- Cement may be degraded
- Casing may be corroded
- You cannot see into the formation
- You must ensure the barriers you install will last for 1,000+ years (the regulatory requirement)

### P&A Requirements (NORSOK D-010 Compliant)
1. **Formation zone isolation:** A minimum 30m cement plug across each hydrocarbon-bearing zone
2. **Cross-flow isolation:** Prevent inter-zone communication (isolate each formation interval)
3. **Wellhead barrier:** Permanent barrier at or near the mudline (for subsea wells)
4. **Surface plug:** Cement plug near surface for onshore/platform wells

### Angola P&A Context
Angola's Cabinda (Block 0) fields are approaching end of life. Chevron is the operator. The P&A program for these fields will be one of the largest engineering undertakings in Angola in the 2030s. This represents a significant career opportunity for Angolan petroleum engineers with well integrity skills.

**Typical Angola deepwater P&A cost:** $15–40 million per well. For a field with 50 wells, that is $750 million to $2 billion in P&A liability. Operators take this seriously.

---

## NORSOK D-010: What You Need to Know

NORSOK D-010 is the Norwegian standard for well integrity, but it has become the international reference standard for deepwater operations. All major Angola operators use it.

**Key requirements relevant to well integrity engineers:**

| Requirement | What it Means |
|------------|---------------|
| Two independent barriers at all times | Never allow single-barrier situation without risk acceptance |
| Well integrity status classification | Every well must be classified Red/Amber/Green |
| DHSV test frequency | Minimum every 6 months for all producing wells |
| Annulus pressure monitoring | Continuous monitoring and recorded pressure limits |
| Written procedures for barrier reduction | Any planned barrier reduction needs documented risk assessment |
| Periodic well integrity reports | Formal reporting to management on population status |

---

## Interview Questions for Well Integrity Roles

1. What is the two-barrier principle and why is it fundamental to well integrity?
2. Define Sustained Casing Pressure. What are the common causes?
3. How do you test a DHSV? What does a failed test tell you?
4. What is an Annulus Management Procedure and when is it required?
5. Describe the P&A process for a subsea Angola deepwater well.
6. What is the difference between well integrity and well control?
7. Name three ways cement integrity can fail over the life of a well.
8. An A-annulus has been slowly building pressure for 6 months. How do you classify this well and what is your action plan?
9. What is a leak-off test and what is it measuring?
10. What ANPG regulatory requirements govern well integrity in Angola?

---

## Study Resources

- **NORSOK D-010** (free download from Standard Norge website) — read Sections 5 (general requirements) and 9 (well integrity testing)
- **API RP 90** — Annular Casing Pressure Management
- **SPE 112083** — "Well Integrity Issues in Angola Deepwater Fields" (check SPE OnePetro)
- **Oil & Gas UK:** "Well Integrity Guidelines" (publicly available)
- **Software:** Landmark's WellPlan has well integrity modules; Halliburton's BaraLogix tracks barrier status

---

*Next: [03_Petroleum_Economics.md](03_Petroleum_Economics.md) — the financial framework that determines which projects get built.*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
