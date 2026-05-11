# Skill 11 â€” Subsea Systems

> **Applies to:** Subsea Engineer, [ROV](../glossary.md) Pilot/Technician, Inspection Engineer, Production Engineer
> **Offshore relevance:** Angola's deepwater production (Blocks 15, 17, 32) is entirely subsea-based â€” the wells, trees, manifolds, and flowlines are on the seabed; nothing is visible from the surface

---

## What Is This Skill?

Subsea systems engineering covers the design, installation, operation, and integrity management of all equipment placed on the seabed or below the water surface. In Angola's ultra-deepwater context (500â€“2,200m depth), this includes: subsea wellheads, christmas trees, production manifolds, flowlines, flexible risers, umbilicals, and the mooring systems of FPSOs. Subsea engineers and [ROV](../glossary.md) technicians are the people who monitor, maintain, and intervene on this equipment â€” entirely remotely.

---

## Why It Matters Offshore

Angola produces primarily from subsea tieback systems. On Block 17 alone:
- 34+ production wells
- Hundreds of kilometres of flowlines and umbilicals
- Multiple subsea manifolds (Dalia, CLOV, Girassol, Pazflor) connecting wells to [TotalEnergies](../../data/company-directory/totalenergies.md) FPSOs
- All intervention requires [ROV](../glossary.md) work or costly well intervention vessels

Subsea equipment failure is extremely expensive â€” a stuck subsea valve or leaking umbilical can cost millions per day in lost production and repair costs. Subsea engineers are among the highest-paid offshore professionals.

---

## Key Concepts to Master

### 1. Subsea Wellhead System

The wellhead sits on the seabed and provides structural support and pressure sealing for all the strings inside the well.

```
   Sea Surface
       |
   Riser (marine conductor)
       |
   Subsea Wellhead Housing (stuck in seabed)
       |
   Casing hanger (22" conductor â†’ 18 5/8" â†’ 13 3/8" â†’ 9 5/8" â†’ 7")
       |
   Tubing hanger (production tubing)
       |
   Subsea Christmas Tree (mounted on top of wellhead)
```

**Key components:**
- **High-pressure wellhead housing (HPWH):** Structural hub for all casing strings
- **Casing hangers + seals:** Each casing string lands and seals in the wellhead
- **Tubing hanger:** Suspends the production tubing and seals the annuli

---

### 2. Subsea Christmas Tree (XT)

The Christmas tree is the assembly of valves, gauges, and connections mounted on the wellhead to control production/injection and provide well access for intervention.

#### 2.1 Horizontal XT vs. Vertical XT

| Feature | Horizontal XT (HXT) | Vertical XT (VXT) |
|---|---|---|
| **Tree configuration** | Tubing hanger inside tree body | Tubing hanger in wellhead |
| **Well access** | Side access â€” requires specialized tool | Direct vertical access â€” wireline friendly |
| **Weight** | Lighter | Heavier |
| **Angola preference** | [SLB](../../data/company-directory/slb.md) OneSubsea HXT common on Angola deepwater | Both used |
| **Installation** | Drill string or dedicated crane | Drill string or crane |

#### 2.2 Key Valves on the XT

```
 Well bore (production)
        |
 SCSSV (Surface Controlled Subsurface Safety Valve) â€” downhole in tubing
        |
 Subsea christmas tree:
   - PMV (Production Master Valve) â€” first valve above wellhead
   - PWV (Production Wing Valve) â€” diverts to flowline
   - Swab valve (vertical access for intervention)
   - Annulus master valve / annulus wing valve
        |
 Flowline connection hub / jumper
```

**All valves are hydraulically actuated** â€” hydraulic pressure from the umbilical opens/closes them. The default fail-safe state is Closed (fail-safe-closed = FSC).

---

### 3. Umbilicals

The umbilical is the "nervous system" of the subsea field â€” a bundle of tubes, hoses, and cables running from the [FPSO](../glossary.md) surface (or UTA â€” Umbilical Termination Assembly on seabed) to each XT and manifold.

**Contents of a typical Angola deepwater umbilical:**
- **Hydraulic lines:** High-pressure (HP) and low-pressure (LP) lines to actuate wellhead valves
- **Chemical injection lines:** For scale inhibitor, MEG, asphaltene dispersant, methanol injection
- **Electrical cables:** Power supply for subsea electronics (sensors, communication systems)
- **Fiber optic cables:** Real-time data transmission (production monitoring, temperatures, pressures)

**Dynamic umbilicals:** Section from seabed (static) to [FPSO](../glossary.md) (dynamic) â€” flexes with [FPSO](../glossary.md) motion
**Static umbilicals:** Seabed sections between manifolds and trees

---

### 4. Subsea Manifolds

A manifold is a subsea gathering station â€” it receives production from several wells and combines flows into one or two production flowlines leading to the FPSO.

```
 Well 1 â”€â”€â†’ |
 Well 2 â”€â”€â†’ | MANIFOLD | â”€â”€â†’ Flowline to FPSO
 Well 3 â”€â”€â†’ |
 Well 4 â”€â”€â†’ |
```

**Key manifold components:**
- **Production header:** Collects all well flows
- **Isolation valves:** Allow individual wells or export lines to be isolated
- **Pressure transmitters / temperature sensors:** Monitor production parameters
- **Pigging loop:** Allows pigs to be launched from the FPSO, pass through the manifold, and return (for wax removal / [flow assurance](10-flow-assurance.md))

**Angola examples:**
- **Girassol manifolds ([TotalEnergies](../../data/company-directory/totalenergies.md) Block 17):** Early Angola deepwater manifolds, 1,200m water depth
- **Kaombo manifolds ([TotalEnergies](../../data/company-directory/totalenergies.md) Block 32):** Multiple cluster manifolds at 1,300â€“2,000m, tied back to Kaombo Norte and Kaombo Sul FPSOs

---

### 5. Flowlines and Risers

#### 5.1 Flowlines
Flowlines connect the XT to the manifold, and the manifold to the riser base (on the seabed).

**Types:**
| Type | Application | Angola use |
|---|---|---|
| **Rigid steel flowline (pipe-in-pipe)** | Long inter-field tiebacks with insulation | Block 32 long tiebacks |
| **Flexible flowline** | Short jumpers, dynamic applications | Jumpers between XT and manifold |
| **Carbon steel + polyurethane insulation** | Cost-effective for warm fluid | Shorter tiebacks |

#### 5.2 Risers
Risers are the pipe sections that connect the seabed flowline to the FPSO topside.

| Riser type | Description | Angola use |
|---|---|---|
| **Flexible riser (catenary)** | Flexible pipe â€” curves from seabed to FPSO; accommodates FPSO motion | Most Angola FPSOs |
| **Steel Catenary Riser (SCR)** | Steel pipe in a free-hanging catenary curve | Some [TotalEnergies](../../data/company-directory/totalenergies.md) FPSOs |
| **Top-tensioned riser (TTR)** | Vertical rigid riser, tensioned from surface | TLPs/Spars â€” not common in Angola |

**Riser configurations on a typical Angola FPSO:**
- Production risers (oil): 10â€“20 flowlines entering from the subsea wells
- Water injection risers: Injecting seawater or treated produced water back into reservoir
- Gas lift risers: Injecting gas down to ESPs or gas lift mandrels

---

### 6. PLEM / PLET

- **PLEM (Pipeline End Manifold):** A subsea manifold at the end of a pipeline â€” typically where the production pipeline ends before the riser attachment
- **PLET (Pipeline End Termination):** A structural frame at the end of a pipeline with connection hub for jumpers or risers

Both are lowered by crane or deployment vessel to the seabed.

---

### 7. FPSO Mooring Systems

Angola FPSOs must stay on station while connected to multiple subsea risers and umbilicals, in water depths of 1,000â€“2,000m, in current and swell environments.

**Two main mooring types:**

| Type | Description | Angola FPSOs |
|---|---|---|
| **Internal Turret (weathervaning)** | FPSO can rotate around the turret â€” risers connected inside rotating turret; hull always weathervanes to minimize loads | Girassol, Rosa, Dalia, Kaombo |
| **Spread mooring (fixed)** | FPSO fixed by chains in 4â€“8 directions; cannot rotate | Suitable for benign current environments |

**Turret mooring detail:** The turret has a swivel stack that allows the FPSO to rotate 360Â° while the turret and risers remain stationary relative to the seabed. This is mechanically complex â€” the swivel stack is a high-maintenance item in Angola.

**Mooring lines:** Steel chain + wire rope + polyester rope segments anchored to suction piles or drag anchors on the seabed.

---

### 8. ROV (Remotely Operated Vehicle)

ROVs are unmanned underwater robots used by offshore operations teams and well intervention vessels to inspect, maintain, and operate subsea equipment.

#### 8.1 ROV Classes

| Class | Weight / Power | Application |
|---|---|---|
| **Work Class [ROV](../glossary.md) (WROV)** | 500â€“4000 kg; 50â€“200 HP | All subsea intervention: valve operations, connection, repair, inspection |
| **Inspection Class [ROV](../glossary.md) (IROV / Flying Eye)** | 50â€“200 kg | Inspection and video only â€” no manipulation |
| **Trenching [ROV](../glossary.md)** | Large, heavy | Pipeline route preparation and burial |

**WROV components:**
- **Manipulator arms:** 5 or 7-function arms for valve turn, connector engagement, torque tool operations
- **Thrusters:** Vectored, horizontal + vertical for positioning
- **Cameras / lights:** Multiple cameras, sonar
- **Tool skids:** Custom tooling for specific subsea tasks (hot stab panels, torque tools, cutting tools)
- **LARS (Launch and Recovery System):** Deck crane + tether management system on the vessel

#### 8.2 What ROVs Do in Angola

- Open/close subsea valves (production tree isolation for maintenance, MEG injection manifold valves)
- Connect/disconnect flying leads (hydraulic, chemical, electrical jumpers between components)
- Inspect flowline integrity (video survey, cathodic protection checks)
- Monitor marine growth fouling and clean subsea structures
- Support well intervention tool deployment
- Inspect riser and umbilical hang-off points on FPSO
- Perform leak testing after maintenance

---

### 9. Subsea Control System

**From FPSO to seabed, the control signal path:**
1. Master Control Station (MCS) on FPSO â†’ operator commands
2. Transmission via Hydraulic Power Unit (HPU) and electrical/optical signal over umbilical
3. Subsea Distribution Unit (SDU) / Subsea Control Module (SCM) on each manifold/XT
4. SCM interprets command â†’ opens/closes hydraulic valve via solenoid â†’ valve actuates

**SCSSV (Surface Controlled Subsurface Safety Valve):**
- Positioned inside the production tubing, ~100m below the XT
- Normally held open by hydraulic pressure from the surface
- Loss of hydraulic pressure (e.g., umbilical failure or ESD) â†’ spring force closes valve
- The last safety barrier between the reservoir and the environment in an emergency

---

## Study Roadmap

### Beginner (0â€“2 months)
- [ ] Learn the subsea hardware stack: wellhead â†’ XT â†’ jumper â†’ manifold â†’ flowline â†’ riser
- [ ] Understand valve types on the christmas tree: PMV, PWV, swab valve, SCSSV
- [ ] Know what an umbilical contains and what it does
- [ ] Understand why ROVs are necessary (depth prevents divers in Angola)

### Intermediate (2â€“5 months)
- [ ] Study flexible pipe and rigid pipe construction (API 17B, API 17J standards)
- [ ] Learn SCM/SCU control system architecture
- [ ] Study mooring system design for FPSOs â€” catenary equations
- [ ] Review specific Angola field architectures: Girassol, Dalia, Kaombo

### Advanced (5â€“12 months)
- [ ] Study [ROV](../glossary.md) operations procedure manuals (freely available from [ROV](../glossary.md) companies)
- [ ] Learn subsea integrity management: inspection intervals, cathodic protection, corrosion under insulation
- [ ] Study ISO 13628 (subsea systems standard) â€” overview at minimum
- [ ] Understand [FPSO](../glossary.md) life extension challenges â€” aging umbilicals and risers in Angola

---

## Resources

| Resource | Notes | Cost |
|---|---|---|
| **Yong Bai "Subsea Engineering Handbook"** | Comprehensive reference | Paid |
| **API 17A: Specification for Subsea Christmas Trees** | Standard | Paid (limited free preview) |
| **[TechnipFMC](../../data/company-directory/technipfmc.md) / SLB OneSubsea technical brochures** | Product specs and case studies | Free via company websites |
| **SPE "Subsea Production Systems" papers** | Real Angola case studies | SPE membership (student = ~$15/yr) |
| **DOF Subsea / [Oceaneering](../../data/company-directory/oceaneering.md) ROV operator videos** | Free on YouTube | Free |
| **[Subsea 7](../../data/company-directory/subsea7.md) / Saipem Angola project case studies** | Company websites | Free |

---

## Practice Questions

1. Describe the pressure barrier function of the SCSSV. What happens if the hydraulic supply to the SCSSV is lost?
2. What is the difference between a horizontal and vertical Christmas tree? Why might Angola prefer horizontal XTs?
3. An umbilical chemical injection line becomes blocked. Describe the consequences for hydrate prevention in a deepwater Angola tieback.
4. What is severe riser slugging? At what conditions does it occur and how does it affect the [FPSO](../glossary.md)?
5. Describe what a Work Class [ROV](../glossary.md) would do during a routine Angola manifold inspection.

---

## Related Skills

- [10 â€” Flow Assurance](10-flow-assurance.md) (flowlines and umbilicals are the [flow assurance](10-flow-assurance.md) infrastructure)
- [08 â€” FPSO Process Operations](08-fpso-process-operations.md) (risers connect subsea to [FPSO](../glossary.md))
- [13 â€” Cementing & Completions](13-cementing-and-completions.md) (XT sits on top of completion tubing hanger)
- [15 â€” Well Integrity](15-well-integrity.md) (subsea barrier elements â€” XT valves and SCSSV)

---

## Where to Learn This Skill

| Resource | Type | Cost | Link |
|----------|------|------|------|
| **PetroWiki â€” Subsea Engineering** | Free reference | Free | [petrowiki.spe.org/Subsea_engineering](https://petrowiki.spe.org/Subsea_engineering) |
| **YouTube â€” Subsea production system** | Free animations | Free | Search "subsea production system animation" on YouTube |
| **Subsea Engineering Handbook** (Bai & Bai) | Textbook | ~$120 | [Elsevier](https://www.elsevier.com) |
| **Subsea Pipeline Engineering** (Palmer & King) | Textbook | ~$100 | PennWell |
| **IMCA** | Professional org â€” subsea standards | Membership | [imca-int.com](https://www.imca-int.com) |
| **TechnipFMC / Subsea 7 / Saipem grad programs** | Company training (deepest) | Employer-funded | [technipfmc.com/careers](https://www.technipfmc.com/careers) Â· [subsea7.com/careers](https://www.subsea7.com/careers) |

â†’ Full directory: [Learning Resources](../learning-resources.md)

