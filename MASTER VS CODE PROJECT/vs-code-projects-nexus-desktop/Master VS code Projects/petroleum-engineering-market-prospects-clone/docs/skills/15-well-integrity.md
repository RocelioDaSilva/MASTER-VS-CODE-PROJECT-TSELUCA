# Skill 15 â€” Well Integrity

> **Applies to:** Well Integrity Engineer, Drilling Engineer, Completions Engineer, Production Engineer, [FPSO](../glossary.md) Operations, Intervention Engineer
> **Offshore relevance:** Well integrity is the cornerstone of offshore safety â€” a well integrity failure can cause a blowout, oil spill, or toxic gas release. In Angola, ANPG regulates well integrity and operators self-manage with their own barrier standards

---

## What Is This Skill?

Well integrity is the application of technical, operational, and organizational solutions to reduce the risk of uncontrolled release of formation fluids throughout the life cycle of a well â€” from drilling through completion, production, suspension, and abandonment. It is governed by the concept of **barriers**: if barrier 1 fails, barrier 2 must hold; if both fail simultaneously, the result is a blowout. Well integrity engineers prevent that from happening.

---

## Why It Matters Offshore

Angola has hundreds of active deepwater production and injection wells connected to FPSOs. A well integrity incident:
- Creates a direct path for reservoir fluid (oil, gas, [H2S](../glossary.md)) to surface or the environment
- Can cause fire, explosion, oil spill, or toxic gas cloud on the [FPSO](../glossary.md)
- Is extremely difficult and expensive to remediate remotely at 1,000â€“2,000m water depth
- Is subject to ANPG regulatory reporting requirements and can result in permit suspension

High-profile examples globally (Macondo 2010, Montara 2009) were well integrity failures â€” they killed people and devastated companies.

---

## Key Concepts to Master

### 1. Well Barrier Concept

A **well barrier** is a system of components that prevents uncontrolled flow of formation fluids to the environment.

#### Two Independent Barriers

International standards (NORSOK D-010, API RP 100) require **two independent barriers** to be maintained at all times in a live well. The barriers must be independent â€” failure of one must not cause the other to fail.

```
BARRIER ENVELOPE CONCEPT:

    SURFACE / ATMOSPHERE
         â†‘â†‘ (BLOCK THIS)
    â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•  â† BARRIER 2 (Secondary barrier envelope)
         â†‘â†‘
    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  â† BARRIER 1 (Primary barrier envelope)
         â†‘â†‘ (formation fluid pressure trying to migrate)
    â–ˆâ–ˆ RESERVOIR â–ˆâ–ˆ
```

#### NORSOK D-010 â€” Primary Barrier Examples (Production Well)

| Component | What it is | Why it's a barrier |
|---|---|---|
| **Production packer** | Seals annulus at bottom of tubing | Blocks annular flow path |
| **Tubing** | Production tubing string | Contains wellbore pressure |
| **SCSSV (downhole safety valve)** | Hydraulically controlled valve ~100m BML | Closes off tubing flow on ESD |
| **Tubing hanger seal** | Seals tubing at XT | Prevents tubing-to-annulus crossflow |

#### Secondary Barrier Examples

| Component | What it is |
|---|---|
| **Production casing** | 9 5/8" or 7" steel casing behind tubing |
| **Cement behind casing** | Zonal isolation preventing migration outside casing |
| **XT master valves (PMV, AMV)** | Surface valves on the tree |
| **Wellhead housing seals** | Metal seals between casing strings |

---

### 2. Well Barrier Element Classification

| Classification | Meaning |
|---|---|
| **Primary Well Barrier Element (WBE)** | Directly prevents flow toward surface |
| **Secondary Well Barrier Element (WBE)** | Provides backup if primary fails |
| **Supporting/Functional Element** | Supports system function but is not itself the barrier (e.g., hydraulic line to SCSSV) |

**Barrier status categories:**
- **Green:** Full function, no issue
- **Yellow:** Degraded â€” one barrier in reduced status; enhance monitoring, plan remediation
- **Red:** Failed barrier â€” immediate action required; consider well suspension
- **Two-yellow rule:** A well cannot have two concurrent degraded barriers â€” must be shut in

---

### 3. MAASB and MAASP

#### MAASP (Maximum Allowable Annular Surface Pressure)

**Definition:** The maximum pressure that can be accepted on a casing annulus before the risk of formation fracture or casing failure becomes unacceptable.

**Calculated as:**

$$\text{MAASP} = \left(\text{LOT pressure} - \text{hydrostatic pressure at LOT depth}\right) + \text{hydrostatic at surface}$$

Simplified: **MAASP = (fracture pressure at weakest formation âˆ’ pore pressure of fluid in annulus) Ã— TVD conversion**

**In practice:** Each annulus (A, B, C) on an Angola production well has a rated MAASP. If annular pressure exceeds MAASP, the well must be investigated and remediated.

#### MAASP (Maximum Allowable Annulus Shut-in Pressure) â€” same acronym

Also used for: Maximum pressure allowed on an annulus before taking action (bleed-off, investigation, well shut-in).

---

### 4. Sustained Casing Pressure (SCP)

**What it is:** Pressure in a casing annulus that returns after being bled off â€” indicating a continuous source of gas or fluid leaking into that annulus.

**Causes:**
1. **Cement failure:** Channeling behind casing allows gas migration from reservoir to annulus
2. **Casing shoe failure:** High pressure zone communicating through cement below casing shoe
3. **Tubing / packer leak:** Wellbore fluid leaking from tubing into A-annulus
4. **Control line / chemical injection line leak:** Small-bore leak into annulus

**Detection:** Monitor annulus pressures on the [FPSO](../glossary.md) data historian â†’ anomalous pressure build-up â†’ trend analysis

**Classification:**
| Class | SCP behavior | Action |
|---|---|---|
| **Bleed-down only** | Bled to zero, does not rebuild | Monitor â€” may be trapped thermal pressure |
| **SCP Type 1** | Bled, rebuilds slowly; stabilizes below MAASP | Active SCP â€” investigate, plan well intervention |
| **SCP Type 2** | Bled, rebuilds to MAASP or above | Urgent investigation; suspend well from production |

**Remediation:**
- **Squeeze cementing:** Pump cement into annulus to fill channels
- **Casing patching:** Run an expandable patch over the leak point
- **Well completion change:** If packer or tubing is leaking, requires well intervention

---

### 5. Well Integrity Management on an FPSO

On an Angola [FPSO](../glossary.md), the well integrity engineer/team:

**Daily tasks:**
- Monitor wellhead and Christmas tree pressures (A-annulus, B-annulus, C-annulus, tubing, surface casing)
- Review [FPSO](../glossary.md) SCADA historian for pressure trends and anomalies
- Assess any valves showing anomalous signatures (leak-off, hydraulic consumption)

**Scheduled tests:**
| Test | Frequency | What it checks |
|---|---|---|
| **SCSSV function test** | 6 monthly (or as per regulator) | SCSSV closes and holds shut-in pressure |
| **XT valve leak test** | Annual | Each tree valve tested for leak-off |
| **Annulus pressure monitoring** | Continuous | SCP detection |
| **Packer leak test** | As required / on intervention | Annulus pressure test across packer |

**SCSSV function test procedure:**
1. Reduce hydraulic pressure on SCSSV control line below minimum closing pressure (~50 bar)
2. SCSSV closes â€” tubing pressure should hold (no bleed-off)
3. Check that pressure below SCSSV is isolated from above
4. Reopen by re-pressuring control line
5. Monitor for recovery of production

---

### 6. Well Barrier Schematic (WBS)

Every well in Angola must have a current **Well Barrier Schematic** â€” a drawing of the well showing all barrier elements with their status.

**WBS contents:**
- Well sketch with all strings, packers, cement tops, valves
- Each barrier element identified with status (Green/Yellow/Red)
- Pressure ratings and test dates
- SCP status on each annulus
- Date of last Well Integrity Assessment (WIA)
- MAASP for each annulus

**Angola requirement:** Under ANPG Presidential Decree 43/19, all production wells in Angola must have current WBS, annual well integrity assessments, and any anomaly reported within 24 hours.

---

### 7. Well Suspension and Abandonment

#### Well Suspension (P&A-S)

Temporary suspension when a well is not actively producing but may be returned to service:
- Close all tree valves
- Install subsea cap or tree guard (as required)
- Set a plug in the tubing above the packer as additional barrier
- Monitor â€” regular pressure surveys may be required

#### Permanent Abandonment (P&A)

When a well is permanently decommissioned:
1. Remove production tubing
2. Set a permanent cement plug in the casing above the reservoir
3. Test plug integrity
4. Set secondary plug at shallower depth (above any hydrocarbon-bearing formations)
5. Remove well from FPSO manifold
6. Subsea: remove XT, set seabed mudline plug
7. Document all barrier elements placed

**P50 P&A cost for Angola deepwater well:** $10â€“30M, depending on intervention vessel day rate and complexity.

---

### 8. Integrity-Related Standards and References

| Standard | Description |
|---|---|
| **NORSOK D-010** | Norwegian industry standard for well integrity in drilling and well operations â€” internationally adopted |
| **API RP 100 â€” Well Integrity** | American Petroleum Institute recommended practice |
| **ISO 16530-1** | International standard for well integrity during lifetime of a well |
| **IOGP Report 485 â€” [Well Control](01-well-control.md)** | Well control/integrity guidance |
| **ANPG Angola Regulation** | Presidential Decree 43/19 â€” Angola specific |

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Understand the two-barrier concept â€” draw a well barrier schematic for a simple production well
- [ ] Know what SCP is and why it's important
- [ ] Learn the difference between primary and secondary barriers in a production well
- [ ] Understand what MAASP means and why exceeding it is dangerous

### Intermediate (2â€“5 months)
- [ ] Study NORSOK D-010 overview â€” get the free Norwegian standard
- [ ] Practice calculating MAASP for a given well scenario
- [ ] Study common well integrity failures: what causes them, how they were detected, how they were fixed
- [ ] Learn SCSSV function test procedure â€” understand the pressure signature

### Advanced (5â€“12 months)
- [ ] Study well integrity management system (WIMS) design
- [ ] Learn risk-based well integrity assessment methodology
- [ ] Study SPE well integrity papers from Angola and the North Sea
- [ ] Study P&A requirements and cost drivers for deepwater Angola wells

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **NORSOK D-010 Standard** | Free Norwegian standard; downloadable | Free â€” standard.no |
| **API RP 100 Well Integrity** | API recommended practice | Paid |
| **ISO 16530-1** | International standard | Paid |
| **SPE papers "well integrity Angola"** | Real case studies | SPE membership |
| **[IWCF](../glossary.md) Well Integrity module** | IWCF training program | Via IWCF certified training centers |
| **Petroleum Safety Authority Norway (PSA) â€” SCP guidelines** | Clear regulatory guidance | Free â€” ptil.no |

---

## Practice Questions

1. Draw a simple well barrier schematic for a deepwater Angola production well. Label each primary and secondary barrier element.
2. You observe that the A-annulus pressure on an Angola production well is building from 0 bar to 80 bar within 48 hours after bleed-off. The MAASP for that annulus is 150 bar. What classification is this SCP and what is the recommended action?
3. What is the "two independent barriers" rule? Why must the barriers be independent?
4. The SCSSV on a well fails to close during its 6-monthly function test. Describe the consequences for well barrier status and what actions should be taken.
5. Why is sustained casing pressure on the B-annulus (behind production casing) considered more serious than SCP on the A-annulus?

---

## Related Skills

- [01 â€” Well Control](01-well-control.md) ([well control](01-well-control.md) is the active response to barrier failure)
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (completions ARE the barrier elements)
- [11 â€” Subsea Systems](11-subsea-systems.md) (XT valves and SCSSV are subsea barrier elements)
- [12 â€” Offshore HSE & Safety](12-offshore-hse-safety.md) (well integrity failures are the most serious [offshore HSE](12-offshore-hse-safety.md) events)
- [14 â€” Reservoir Engineering Basics](14-reservoir-engineering.md) (reservoir pressure is the driving force behind integrity threats)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Well Integrity** | Free reference | Free | [petrowiki.spe.org/Well_integrity](https://petrowiki.spe.org/Well_integrity) |
| **NORSOK D-010** | Standard (free download) | Free | [standard.no](https://www.standard.no) |
| **IWCF Level 2** | Certification (covers barrier philosophy) | $600â€“1,500 | [iwcf.org](https://iwcf.org) Â· PETROTEC Luanda |
| **Well Integrity for Workovers and Recompletions** (Skinner) | Textbook | ~$80 | Gulf Professional |

â†’ Full directory: [Learning Resources](../learning-resources.md) Â· Angola certs: [Certifications Angola](../../isptec/tseluca/support/Certifications_Angola.md)

