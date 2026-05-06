---
title: Worldbuilding Index — Chain Weapon Story
date: 2026-04-07
status: Master Hub
---

# Worldbuilding Index

**Purpose**: Central reference hub for all world materials, magic systems, geography, cultures, ecology, and political structures.

**See also:** 
- [CROSS-REFERENCE-HUB.md](../CROSS-REFERENCE-HUB.md#-location--regional-mapping) — Cross-linked location & regional mapping
- [SYSTEMS-TO-DOCUMENTATION-INDEX.md](../SYSTEMS-TO-DOCUMENTATION-INDEX.md#magic-systems) — Magic systems cross-referenced to scenes
- [reference/worldbuilding/README.md](../reference/worldbuilding/README.md) — Reference worldbuilding hub

---

## Quick Navigation

- **New to the world?** Start with [Cosmology & Origins](#cosmology--origins)
- **Need magic system rules?** Go to [Magic System](#magic-system)
- **Looking for political info?** See [Nations & Politics](#nations--politics)
- **Want ecology/bestiary?** Check [Ecology & Creatures](#ecology--creatures)
- **Researching a culture?** Head to [Cultures & Traditions](#cultures--traditions)

---

## I. Cosmology & Origins

### Core Concepts
- **Source**: `AI/reference/DEEPSEEK-BATCH-1.md` (foundational)
- **Topics covered**:
  - Weave vs. Flux (physics + magic overlay)
  - Aelfar civilization and the Sundering (~2000 years ago)
  - Veil mechanism and Flux Tears
  - Post-Sundering timeline (Age of Rebirth → Age of Discovery → Modern era)

### Key Files
| File | Purpose | Status |
|------|---------|--------|
| `AI/reference/DEEPSEEK-BATCH-1.md` | Cosmology, Aelfar origins, Flux system | ✓ Complete |
| `worldbuilding/COSMOLOGY.md` | Weave/Flux physics (172 lines) | ✓ Exists |
| `worldbuilding/` | *Root folder* — All world materials | ✓ Exists |

### Canonical Facts
- **The Weave**: Physical law (gravity, light, time, matter). Deterministic.
- **The Flux**: Magical energy overlay. Can be thin (scarce magic) or thick (abundant magic).
- **The Veil**: Semi-permeable barrier between Flux source and reality. Damaged by Sundering; healing slowly.
- **Flux Tears**: Persistent rifts where Veil is absent. High-magic zones. Mutate creatures.
- **Aelfar**: Ancient advanced civilization. Attempted ritual to thin Veil. Catastrophic backfire (Sundering).

---

## II. Magic System

### Overview
- **Hardcoded Rules**: Conservation (mana → effect), Resistance, Fatigue, Consequence, No Resurrection
- **Softcoded Rules**: Channeling crystals efficient, working with existing forces cheaper, ritual magic improvable
- **Cultural Variation**: Each nation has distinct magical tradition

### Core Files
| File | Purpose | Status |
|------|---------|--------|
| `AI/reference/DEEPSEEK-BATCH-3.md` | Magic costs, Hard/Soft magic, opening craft | ✓ Complete |
| `AI/reference/DEEPSEEK-BATCH-5.md` | Six Flux Laws, power archetypes | ✓ Complete |
| `AI/reference/DEEPSEEK-BATCH-8.md` | Chain-weapon mechanics, limit-breaking, power system digest | ✓ Complete |
| `magic-system/THE-FLUX-AND-THE-WEAVE-DETAILED-MECHANICS.md` | Flux/Weave physics & six laws (282 lines) | ✓ Exists |
| `magic-system/FOUR-LAWS-NARRATIVE-VERIFICATION.md` | Laws narrative verification (267 lines) | ✓ Exists |
| `magic-system/MAGIC-SYSTEM-REFERENCE.md` | Hard magic rules & conservation (136 lines) | ✓ Exists |
| `magic-system/RULE-BREAKERS-EXPLOITATION-GUIDE.md` | Limit-breaking, costs, forbidden techniques (485 lines) | ✓ Exists |
| `magic-system/CHARACTER-POWER-ARCHETYPES.md` | Mage types, schools, traditions (494 lines) | ✓ Exists |
| `magic-system/RESONANCE-PRINCIPLE.md` | Crystal grades, resonance mechanics (350 lines) | ✓ Exists |

### The Six Flux Domains
> **Note**: These 6 Domains describe *what magic can manipulate*. They are governed by the 4 Meta-Laws (Conservation, Entropy Exchange, Symmetry Breach, Information) which describe the *costs and constraints* of all magic use. See `magic-system/FOUR-LAWS-NARRATIVE-VERIFICATION.md` for the Meta-Laws.

1. **Gravity**: Control mass, acceleration, momentum, weight
2. **Energy**: Heat, light, electricity, force projection
3. **Information**: Sound, data, knowledge, communication
4. **Causality**: Time manipulation, sequence, probability, consequence
5. **Entropy**: Decay, randomness, disorder, aging
6. **Momentum**: movement, velocity, inertia, trajectory

Each law has:
- Practitioners (different schools per culture)
- Hard limits (what it can't do)
- Costs (personalized to the magic user)
- Cultural taboos (varies by nation)

---

## III. Nations & Politics

### The Six Major Nations
1. **Valdimere** (Heartland): Centralized imperial military culture. Rigid hierarchy. → `world/nations/valdimere/`
2. **Shukei** (Island Fortress): Samurai codes, spirit-binding, martial honor. → `world/nations/shukei/`
3. **Celestial Kingdom**: Scholar-gentry, libraries, laboratories, meritocratic veneer. → `world/nations/celestial-kingdom/`
4. **Therryn-Umara** (Sahelian): Merchant-princes, griot networks, trade diplomacy. → `world/nations/therryn-umara/` (also `therryn/`, `umara/`)
5. **Andean Alliance**: Communal ayllu leaders, shamans, rope-engineering. → `world/nations/andean-alliance/`
6. **Mercantile Federation**: Patrician oligarchy, mercantile power, contracts. → `world/nations/mercantile-federation/`

### Academy Structure
- **Founding**: Post-Void-Covenant-War; neutral research space
- **Halls**: One Hall per nation (+ Common Stave as counter-culture)
- **Politics**: Each Hall competes for prestige, influence, recruitment
- **Neutral Status**: Academy is supposed to be above national politics (contested)

### Core Files
| File | Purpose | Version |
|------|---------|---------|
| `AI/reference/DEEPSEEK-BATCH-2.md` | Geography, political history, six nations, Guild systems | ✓ Complete |
| *Nations & Politics* | Content consolidated in this index (Section III above) and culture folklore files | ✓ Inline |
| *Geography* | Content consolidated in this index (Section V below) and DEEPSEEK sources | ✓ Inline |
| *Timeline* | Content consolidated in COSMOLOGY.md and DEEPSEEK-BATCH-1/2 | ✓ Distributed |

---

## IV. Cultures & Traditions

### Regional Magical Traditions
Each culture has distinct approach to magic:

| Culture | Focus | Method | Value |
|---------|-------|--------|-------|
| **Valdimere** (Heartland) | Military enforcement, infrastructure | Formalized, militarized | Stability & expansion |
| **Shukei** (Island Fortress) | Personal power, spirit-binding | Individual cultivation | Martial honor |
| **Celestial Kingdom** | Theory, understanding, research | Scholarly, experimental | Knowledge |
| **Therryn-Umara** (Sahelian) | Storytelling, oral magic, griots | Living repositories | Trade & information |
| **Andean Alliance** | Land-connected, shamanism | Plant/animal lore, rituals | Community harmony |
| **Mercantile Federation** | Pragmatic artifacts, trade | Mercantile, productive | Commerce & efficiency |

### Culture-Specific Files
Located in: `worldbuilding/CULTURE/`

| Folder | Content | Status |
|--------|---------|--------|
| `Valdimere/` | [worldbuilding/CULTURE/HEARTLAND-FOLKLORE.md](worldbuilding/CULTURE/HEARTLAND-FOLKLORE.md) — Military tradition, politics, aesthetics | ✓ Draft |
| `Shukei/` | [worldbuilding/CULTURE/ISLAND-FORTRESS-FOLKLORE.md](worldbuilding/CULTURE/ISLAND-FORTRESS-FOLKLORE.md) — Samurai codes, spirit-binding, honor | ✓ Draft |
| `Celestial/` | [worldbuilding/CULTURE/CELESTIAL-FOLKLORE.md](worldbuilding/CULTURE/CELESTIAL-FOLKLORE.md) — Scholar system, meritocracy, research | ✓ Draft |
| `Therryn-Umara/` | [worldbuilding/CULTURE/SAHELIAN-FOLKLORE.md](worldbuilding/CULTURE/SAHELIAN-FOLKLORE.md) — Griot networks, merchant houses, diplomacy | ✓ Draft |
| `Andean/` | [worldbuilding/CULTURE/ANDEAN-FOLKLORE.md](worldbuilding/CULTURE/ANDEAN-FOLKLORE.md) — Ayllu system, shamanism, land stewardship | ✓ Draft |
| `Federation/` | [worldbuilding/CULTURE/FEDERATION-FOLKLORE.md](worldbuilding/CULTURE/FEDERATION-FOLKLORE.md) — Guild contracts, mercantile law, logistics | ✓ Draft |

### Cultural Sources
- `AI/reference/DEEPSEEK-BATCH-2.md` (overview of noble castes and hall systems)
- `AI/reference/DEEPSEEK-BATCH-7.md` (supporting cast and cultural examples)
- `AI/reference/DEEPSEEK-BATCH-8.md` (cultural variation in magic practice)

---

## V. Geography

### Major Geographic Features
- **The Spine of the World**: Mountain backbone rich in resonance crystals. Divides east/west. Home to Andean cultures.
- **The Silverrun River System**: Trade artery; Aldric's Crossing at strategic ford.
- **The Shattered Coast**: Sundering scars; thin Veil; Aelfar ruins; Flux anomalies.
- **Heartland Plains**: Central, stable Veil, seat of imperial power.
- **Sahelian Savannah**: Merchant routes, griot networks, trade hubs.
- **Federation Coast**: Mercantile ports, guild centers, maritime culture.
- **Celestial Territories**: Libraries, academies, scholarly institutions.

### Source Materials
- `AI/reference/DEEPSEEK-BATCH-2.md` (geography overview and timeline)
- `AI/reference/DEEPSEEK-BATCH-8.md` (geography and era digests)

---

## VI. Ecology & Creatures

### Bestiary
- **Master File**: `AI/reference/BEASTS.md`
- **Status**: Complete (20 creatures catalogued)
- **Entries Include**: Etymology, physical description, behavioral profile, Flux abilities, combat notes, lore, art prompts

### Creature Categories
1. **Resonance Thrush** — Small songbird; sound/vibration magic
2. **Entropy Maw** — Large quadruped; decay/entropy magic
3. **Photon Spinner** — Arachnid; light-weaving
4–20. [See full bestiary in `AI/reference/BEASTS.md`]

### Ecological Crisis
- **Problem**: Industrialized magic usage strains local Flux
- **Effect**: Ecosystem degradation, wildlife die-off, creature mutation
- **Consequence**: Refugee crises, ecological instability, political pressure
- **Status**: Slow-moving but accelerating crisis (long-term plot driver)

### Ecology-Specific Files
Located in: `worldbuilding/ECOLOGY/`

| File | Purpose | Status |
|------|---------|--------|
| `CREATURE-BESTIARY.md` | [worldbuilding/ECOLOGY/BEAST-CATALOG.md](worldbuilding/ECOLOGY/BEAST-CATALOG.md) — Cross-cultural catalog | ✓ Draft |
| `FLUX-ANOMALIES.md` | [worldbuilding/ECOLOGY/FLUX-ANOMALIES.md](worldbuilding/ECOLOGY/FLUX-ANOMALIES.md) — Types, locations, hazards | ✓ Draft |
| *Environmental Crisis* | Content in this index (Ecological Crisis section above) and ecology/ files | ✓ Inline |
| *Fourth-Party System* | Content in `magic-system/CREATURE-BESTIARY-FRAMEWORK.md` (759 lines) and ecology/ | ✓ Distributed |

### Sources
- `AI/reference/BEASTS.md` (full bestiary, 20 entries)
- `AI/reference/DEEPSEEK-COMPENDIUM-FULL.md` (ecological crisis section)
- `ecology/` (existing creature and ecosystem files)

---

## VII. Technology & Artifacts

### Chain Weapon System
- **Anatomy**: Memory-metal links, resonance crystals (every 3rd link), segmentation rings, control ring, terminal blades
- **Four States**: Tighten (rigid staff), Loosen (flexible whip), Connect (extended form), Disconnect (projectile use)
- **Evolution**: Configurations vary from whip to staff to sword to net to bridge
- **External Matrix**: Imbued links with specific spells (attraction, tracking, returning, decoy tags)

### Technology Files
- `AI/reference/DEEPSEEK-BATCH-8.md` (chain weapon technical digest)
- `AI/reference/DEEPSEEK-TALKS-SYNTHESIS.md` (chain-spear anatomy and states)
- `technology/` (existing artifact and weapon files)

### Resonance Crystals
- Natural Flux batteries; found in high-Veil-damage areas
- Grades: common, refined, perfect, corrupted
- Uses: artifact charging, ritual focus, magical amplification, energy storage
- Properties: degrade over time; corrupted crystals are unpredictable

---

## VIII. Cross-References & Integration

### Character Integration
- **Source**: `characters/CHARACTER-MASTER-INDEX.md`
- **Tiers**: PRIMARY (Aisen, Caspian, etc.), SECONDARY (Harald, Tarovin, etc.), ENSEMBLE (special powers)
- **Relationships**: See `characters/RELATIONSHIP-MAPS/`
- **Arcs & Deaths**: See `characters/ARCS-AND-DEATHS/`

### Story Integration
- **Chapters**: See `story/CHAPTER-BY-CHAPTER/` (all 52 chapters)
- **Scenes by Arc**: See `story/SCENES-BY-ARC/`
  - ACT-I-CHILDHOOD
  - ACT-II-ACADEMY
  - ACT-III-WAR-AND-FINAL-STAND
- **Character Moments**: See `story/CHARACTER-MOMENTS/`

### Analysis & Synthesis
- **Compendium Full**: `AI/reference/DEEPSEEK-COMPENDIUM-FULL.md` (comprehensive overview)
- **Talks Synthesis**: `AI/reference/DEEPSEEK-TALKS-SYNTHESIS.md` (weapon system and protagonist bio)
- **Index**: `AI/reference/DEEPSEEK-COMPENDIUM-INDEX.md` (batch cross-references)

---

## IX. How to Use This Index

### For Writers
1. **Starting Out**: Read `AI/reference/DEEPSEEK-BATCH-1.md` (cosmology) and `DEEPSEEK-BATCH-2.md` (politics)
2. **Magic Questions**: Check `AI/reference/DEEPSEEK-BATCH-3.md` and `MAGIC-SYSTEM/` folder
3. **Character Context**: See `characters/RELATIONSHIP-MAPS/`
4. **Scene Research**: Check `story/SCENES-BY-ARC/` for similar scenes

### For Worldbuilding Expansion
1. Create topic-specific `.md` files in relevant subfolders (e.g., `worldbuilding/CULTURE/Heartland/`)
2. Link back to this index for navigation
3. Keep cross-references updated as you add content

### For Consistency Checking
1. Reference `AI/reference/DEEPSEEK-BATCH-*.md` files for established facts
2. Verify cultural details against nation profiles before writing
3. Check creature behaviors against bestiary before encounter scenes
4. Confirm magic system costs before writing magic-use scenes

---

## X. To-Do: Files to Create

### High Priority
- [ ] `worldbuilding/COSMOLOGY.md` — Expand cosmology section with diagrams
- [ ] `worldbuilding/MAGIC-SYSTEM/HARD-MAGIC-RULES.md` — Codify magic rules
- [ ] `worldbuilding/NATIONS-AND-POLITICS.md` — Nation profiles
- [ ] `worldbuilding/GEOGRAPHY.md` — Detailed geography with maps

### Medium Priority
- [ ] `worldbuilding/CULTURE/*/` folders with detailed culture files
- [ ] `worldbuilding/ECOLOGY/ENVIRONMENTAL-CRISIS.md`
- [ ] `worldbuilding/TIMELINE.md`
- [ ] `story/INDEX.md` — Master list of all story scenes

### Lower Priority
- [ ] Individual culture subfiles
- [ ] Detailed artifact catalogs
- [ ] Extended lore articles
- [ ] Maps and visual references

---

## XI. Last Updated

**Date**: April 7, 2026  
**By**: Automated folder expansion  
**Next Review**: After Phase 4 (file moves complete)

---

## Navigation

**Back to**: [Project Root](../../README.md)  
**Peer Indexes**: [Story Index](../story/INDEX.md) | [Character Index](../characters/CHARACTER-MASTER-INDEX.md)
