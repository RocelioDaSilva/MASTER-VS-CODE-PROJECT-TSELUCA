# COSMOLOGY — Veil, Flux, and the Weave

## Purpose

This document defines the cosmological model used across the project: the physical and metaphysical substrate (Flux), the boundary layer that modulates access to it (the Veil), the shaping patterns (the Weave), and a pragmatic MU economy for authors to keep scenes consistent and scalable.

Use this as the canonical reference for how magic interacts with geology, artifacts, creatures, and society.

## Core concepts

- Flux — an energetic substrate that permeates the world. Local concentrations of Flux enable manipulation; low or disrupted Flux reduces or corrupts effects.
- Veil — a property of space that resists direct access to Flux. Lower Veil means easier access to raw Flux; higher Veil dampens effects and raises cost. Treat the Veil as a scalar modifier (the "Veil Index", default $V=1$ for ordinary regions).
- Weave — structured patterns of intent and resonance (rituals, gestures, inscriptions, or artifact protocols) that channel Flux toward a purpose. The Weave converts potential Flux into predictable outcomes.
- Mana Units (MU) — an abstract, additive unit measuring the energetic work performed. All costs in other system docs (telekinesis, chain-spear mechanics, artifacts) are expressed in MU.
- Tiers — qualitative buckets for scale and narrative impact (see below).

## Tier mapping (narrative scale)

- Tier 0 — Ambient phenomena, passive resonance, ecosystem-level flux effects (MU ≈ 0–1).
- Tier 1 — Small, local manipulations: single-object telekinesis, short-range illusions (MU ≈ 1–10).
- Tier 2 — Significant feats: battlefield effects, medium-area rituals, moderate artifacts (MU ≈ 10–100).
- Tier 3 — Major events: large-area weaves, permanent landscape changes, powerful artifacts (MU ≈ 100–1000).
- Tier 4 — Catastrophic / mythic: vein-scale flux storms, rupturing the Veil, planetary-scale consequences (MU > 1000).

These ranges are guidelines for authors — pick values consistent with the scene's stakes.

## Practical MU estimation (author's quick formula)

Use a simple multiplicative estimation for scene planning:

$$\text{MU} = B \times M_f \times D_f \times V_f \times C_f$$

where:

- $B$ = base work factor (depends on action type; e.g., moving mass, shaping matter, altering fields). Pick a small integer baseline (1 for simple manipulation, 5 for structural change).
- $M_f$ = mass factor (rough proxy: $M_f = \max(1, \tfrac{mass_{kg}}{10})$ for physical moves).
- $D_f$ = distance/scale factor (1 for close, 1.5–3 for longer ranges, higher for area effects).
- $V_f$ = Veil modifier (default $V_f=1$; increase >1 for thicker Veil, decrease <1 for thin Veil or resonant nodes).
- $C_f$ = complexity multiplier (1 = blunt force; 1.5–3 = precise, delicate, or layered effects).

Example: lift a 50 kg crate 3 m across a normal field with a basic weave: $B=1$, $M_f=5$, $D_f=1$, $V_f=1$, $C_f=1$ → MU ≈ 5.

Keep the estimate rough — it's a planning tool, not a hard physics engine.

## Veil & regional scaling

- Different regions have different Veil Index values. Use $V<1$ to denote thin-veil regions (flux-rich coasts, standing stones, fault lines), $V\approx1$ as ordinary, and $V>1$ for thick-veil zones (sacred wards, imperial wards, sealed ruins).
- Geological features (resonant seams, crystal beds, fault lines) act as Flux sources or conduits. See [worldbuilding/ECOLOGY/FLUX-ANOMALIES.md](worldbuilding/ECOLOGY/FLUX-ANOMALIES.md) and [worldbuilding/ECOLOGY/BEAST-CATALOG.md](worldbuilding/ECOLOGY/BEAST-CATALOG.md) for examples.

## Sources, sinks, and routing

- Sources: tectonic stress, resonance crystal deposits, deep ritual lattices, artifact networks, ancient weaves left by civilization-scale rituals.
- Sinks: heavy Veil reinforcement (man-made or natural), anti-resonant lattices, active draining artifacts.
- Flux flows along strata and can concentrate at intersection nodes (use these as natural chokepoints for story beats and monsters).

## Artifacts and resonance crystals

- Resonance crystals act as local amplifiers, stabilizers, or batteries for Flux. See [worldbuilding/MAGIC-SYSTEM/RESONANCE-CRYSTALS.md](worldbuilding/MAGIC-SYSTEM/RESONANCE-CRYSTALS.md) for mechanics and artifact networks.
- Artifacts can be passive (modify $V_f$ locally), active (produce MU via stored resonance), or catalytic (lower $C_f$ for a given operation). Chain‑spear artifacts and their protocols are documented in [CHAIN-SPEAR-SPECS.md](CHAIN-SPEAR-SPECS.md).

## Ecology & beasts

- Flux anomalies seed unusual ecologies; creatures that develop in flux‑rich nodes often display emergent abilities tied to local Tier. When designing beasts, align their power level with the Tier of the anomaly that spawned or sustains them (see [worldbuilding/ECOLOGY/BEAST-CATALOG.md](worldbuilding/ECOLOGY/BEAST-CATALOG.md)).

## Limits, recovery, and consequences

- MU is conserved per use and must be expended or drained; recovery is a narrative choice but should be consistent (e.g., rest recovers a small percentage; ritual recharge requires time and a node).
- Overdraw / backlash: forcing MU beyond safe thresholds causes flux bleed, corruption, or Veil rupture; use these as stakes.
- Side effects can be physical (fatigue, mutation), environmental (local flora die-back), or metaphysical (permanent thinning of the Veil at a site).

## Narrative rules-of-thumb

- Always state the local Veil Index for major setpieces so readers and authors share constraints.
- Favor local causes: avoid inventing ad-hoc energy sources unless anchored by an artifact, ritual, or node.
- Keep one canonical rule for each culture's relationship to Flux (see [worldbuilding/MAGIC-SYSTEM/CULTURAL-POWER-SYSTEMS.md](worldbuilding/MAGIC-SYSTEM/CULTURAL-POWER-SYSTEMS.md)).

## History & myth (brief)

- Provide a short canonical sequence: origin of the Weave (ancient seeding), first Veil‑thinning events (Flux Storms), age of artifacts and Great Wards, modern equilibrium. Use myth fragments to explain cosmological puzzles in local folklore.

## Cross-references & next work

- See the magic-system hub: [worldbuilding/MAGIC-SYSTEM/INDEX.md](worldbuilding/MAGIC-SYSTEM/INDEX.md)
- Telekinesis numeric references: [TELEKINESIS-NUMERIC.md](TELEKINESIS-NUMERIC.md)
- Chain-spear design: [CHAIN-SPEAR-SPECS.md](CHAIN-SPEAR-SPECS.md)
- Ecology and anomalies: [worldbuilding/ECOLOGY/BEAST-CATALOG.md](worldbuilding/ECOLOGY/BEAST-CATALOG.md) and [worldbuilding/ECOLOGY/FLUX-ANOMALIES.md](worldbuilding/ECOLOGY/FLUX-ANOMALIES.md)

Next steps: add diagrams (Veil/Flux cross-section), map flux hotspots, and extract canonical excerpts from DEEPSEEK batches to cite as in‑world research notes.

## Worked MU examples & sample calculations

Use the quick formula from above to produce scene estimates. The examples below walk through realistic author choices.

1) Simple lift — crate (50 kg, 3 m, basic weave)

- Choose: $B=1$, $M_f=\max(1,50/10)=5$, $D_f=1$, $V_f=1$, $C_f=1$
- Calculation: $\mathrm{MU}=1\times5\times1\times1\times1=5$ (Tier 1)

2) Stable levitation of a person (70 kg) across a crowded chamber

- Choose: $B=1$ (manipulation), $M_f=7$, $D_f=1.2$ (room-scale), $V_f=1$, $C_f=1.5$ (precision to avoid harm)
- Calculation: $\mathrm{MU}\approx1\times7\times1.2\times1\times1.5\approx12.6$ (Tier 2 — sustained control)

3) Small structural collapse — focused weave to snap support (estimated mass affected: 500 kg)

- Choose: $B=5$ (shaping/structural work), $M_f=50$, $D_f=1.5$ (localized area), $V_f=1.2$ (slightly thick Veil), $C_f=2$ (targeted precision)
- Calculation: $\mathrm{MU}=5\times50\times1.5\times1.2\times2=900$ (Tier 3)

4) Ritual recharge at a resonant node (restores ~200 MU over 8 hours)

- A node with $V_f=0.6$ and auxiliary crystals providing a catalytic $C_f=0.8$ can support slow recharging rituals. Exact numbers depend on node yield documented in [worldbuilding/ECOLOGY/FLUX-ANOMALIES.md](worldbuilding/ECOLOGY/FLUX-ANOMALIES.md).

### Sample author table (quick reference)

| Action | Typical MU | Suggested Tier |
|---|---:|---:|
| Lift 50 kg (single object) | 3–8 MU | Tier 1 |
| Hold/levitate person (precise) | 8–20 MU | Tier 2 |
| Local area weave (minor collapse) | 100–500 MU | Tier 3 |
| Permanent landscape alteration | 500–5000 MU | Tier 3–4 |

Numbers in the table are approximate ranges to help scene pacing and should be adjusted for $V_f$, mass, and complexity.

## Author checklist for computing MU

1. Define the intent and scope (single object, person, area, permanent change).
2. Estimate mass or equivalent difficulty (convert to $M_f$).
3. Pick base factor $B$ for the work type.
4. Choose distance/scale factor $D_f$.
5. Set the local Veil modifier $V_f$ (include site notes: nodes, wards, crystals).
6. Choose complexity multiplier $C_f$ for precision, layering, or timing.
7. Compute MU and compare to Tier guidance.
8. Decide recovery and backlash rules before committing (see below).

## Backlash and thresholds

- Soft overdraw (up to ~25% over planned MU): localized fatigue, shaky weave, minor environmental flicker.
- Moderate overdraw (~25–100% over): flux bleed, short-lived corruption of nearby flora/fauna, temporary Veil thinning.
- Severe overdraw (>100% over): Veil rupture, persistent corruption, node collapse, possible artifact destabilization.

Authors should pick consistent thresholds for cultures or character specialties (for example, adepts from the Island Fortress accept higher moderate overdraw risk due to local node training).

## Veil/Flux cross-section (diagram)

```mermaid
graph TD
	subgraph Surface
		A[Thin Veil node\n(V &lt; 1) — high Flux] --> FN((Flux Node))
		B[Ordinary ground\n(V ≈ 1) — ambient Flux] --> FA((Ambient Flux))
		C[Thick Veil zone\n(V &gt; 1) — low Flux] --> FL((Drained Flux))
	end
	FN --> Deep[Deep Strata/conduits]
	FA --> Deep
	FL --> Deep
	FN --- Artifact[Resonance crystal / Lattice]
	Artifact ---|amplifies| FA
```

This simple flowchart shows how nodes, ambient flux, and thick-veil zones relate to deeper conduits and artifacts.

## Practical scene guidance

- Always declare the local $V_f$ when introducing flux-dependent effects.
- Tie extraordinary power uses to explicit sources (artifacts, crystal beds, ritual scaffolds).
- Use backlash rules to raise stakes and limit free-use of high MU feats.

---
Next actions I can take: (A) render the diagram as an embedded image and add labeled cross-sections, (B) pull supporting citations from DEEPSEEK batches and embed them as in-world research notes, or (C) expand the MU table into a full reference appendix. Which would you like next?

Draft: status = DRAFT.
---
Draft: status = DRAFT. Questions or priorities: would you like diagrams next, or expanded numeric tables and sample scenes that compute MU step-by-step?
