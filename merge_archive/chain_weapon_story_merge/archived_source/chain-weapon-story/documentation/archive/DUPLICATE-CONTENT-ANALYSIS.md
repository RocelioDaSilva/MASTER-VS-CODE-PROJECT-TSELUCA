# Duplicate & Overlapping Content Analysis
**Chain Weapon Story Repository**  
**Date:** April 8, 2026  
**Scope:** Root-level reference files vs. reference/ subdirectory consolidations

---

## EXECUTIVE SUMMARY

The repository has three layers of documentation that significantly overlap:
1. **story-overview.md** (root) — narrative overview with all core systems
2. **World-Bible.md** (reference/worldbuilding/) — comprehensive reference bible  
3. **Master consolidation files** (magic-system/, society/, techniques/) — specialized reference docs

**Current state:** 40-60% content duplication across these tiers. The three master files (CHAIN-SPEAR-MASTER, ACADEMY-POLITICS-MASTER, COMBAT-CHOREOGRAPHY-MASTER) also contain their original source files, creating cascading redundancy.

**Consolidation opportunity:** Establish clear hierarchy with single source of truth for each topic, cross-references only.

---

## TIER 1: ROOT-LEVEL DOCUMENTATION

### story-overview.md
**Purpose:** Narrative overview with protagonist, weapon, magic, arcs, and antagonists  
**Size:** ~500 lines  
**Authority:** High for narrative/thematic intent  

**Contains:**
- ✓ Protagonist (Aisen) — full profile, skills, traits, no-plot-armor philosophy
- ✓ Weapon System (Chain Spear) — states, telekinesis synergy, armor
- ✓ Magic System (Telekinesis) — techniques, physics principles, costs summary
- ✓ Story Arcs (4 phases) — childhood through death
- ✓ Antagonists — Caspian Vane, Seraphine Moroz, Corvin Ashford, Lucius Varro, The Covenant (organizational)
- ✓ Supporting Characters (12) — Harald, Tarovin, Elara, Kaelen, Rin, Amara, Lysandra, Scholar Network
- ✓ World Building (7 cultures) — Heartland, Island Fortress, Celestial, Sahelian, Andean, Federation, Common
- ✓ Ecological Crisis — overview and Flux Tearing concept
- ✓ Fourth Party — brief intro as "beast-kin, elemental enclaves, remnant constructs"
- ✓ Narrative Themes — no plot armor, randomness, consequences, death not end, deck of cards philosophy

**Not Contains:**
- ✗ Master Academy governance structure/factions (Conservators, Practical Arms, Innovators)
- ✗ Specific exam mechanics (Resonance Calibration Trial)
- ✗ Detailed Fourth Party encounters (Forlorn Engineers, Tusk Clans, etc.)
- ✗ Year-by-year timeline (only narrative phases)
- ✗ Combat choreography sequences with MU costs
- ✗ Detailed nation political structures

---

## TIER 2: REFERENCE WORLDBUILDING LAYER

### World-Bible.md (reference/worldbuilding/)
**Purpose:** Comprehensive consolidated reference  
**Size:** ~1,200 lines  
**Authority:** High for worldbuilding consistency  

**Contains:**
- ✓ **Introduction & Contents** — navigational structure
- ✓ **I. World Overview** — Cosmology (Weave, Flux, Veil), Magic + Physics, Geography (Spine, Silverrun, Coast)
- ✓ **II. Historical Timeline** — Aelfar Age → Sundering → Void Covenant War → Contemporary (Age of Strife)
- ✓ **III. Major Powers & Cultural Specializations** — 6 cultures (Heartland, Island, Celestial, Sahelian, Andean, Federation) with combat/magic/tech specs
- ✓ **IV. The Academy** — neutral institution, halls as cultural proxies, mission tensions
- ✓ **V. Protagonist Profile** — Aisen origin, tavern family, mentors, arc summary, traits
- ✓ **VI. Weapons & Systems** — Hunting tools, Spear techniques, Telekinesis, Chain Spear basics, Combos & tactics
- ✓ **VII. Fourth Party & Ecological Crisis** — overuse of magic → degrade → wild fauna → political exploitation
- ✓ **VIII. Encounters** — 6 cultural teachers shaping protagonist (Heartland engineer → siege thinking, Island ronin → maai discipline, etc.)
- ✓ **IX. Practical Notes** — Compendium workflow and preservation strategy
- ✓ **X. Appendix** — Physics concepts quick reference and credits

**Total Content Overlap with story-overview.md:** ~60%
- Cosmology/Magic/Physics: Identical framework
- World timeline: Identical events, different detail level
- Cultural descriptions: Identical, slightly expanded
- Protagonist section: Identical but World-Bible is shorter
- Weapon/Magic systems: Both present, slightly different emphasis
- Fourth Party/Ecological: Both covered, World-Bible less detailed
- Narrative themes: NOT in World-Bible (pure reference)

**Unique to World-Bible:**
- Historical domino effects (Aelfar Age → Sundering progression)
- Academy mission tensions (military vs. ecological research)
- Encounters-that-shaped-protagonist framework (8 cultural lessons)
- Practical notes on compendium workflow

---

### YEAR-BY-YEAR-TIMELINE.md (reference/worldbuilding/)
**Purpose:** Compact age-based Aisen timeline with skill milestones  
**Size:** ~100 lines  
**Authority:** High for narrative pacing  

**Contains:**
- ✓ Ages 0–30 detailed events (birth → final border stand)
- ✓ Skill & power growth phases (childhood → adulthood → sacrifice)
- ✓ Key story beats anchored to ages (Frostfang Incident at 18, Final Border-Stand at 30)

**OVERLAP CONCERN:**
- World-Bible mentions Aisen's phases but NOT specific age-to-event mapping
- story-overview.md mentions 4 phases (Childhood, Academy Years, Adult Career, Death & Aftermath) NOT ages
- **UNIQUE VALUE:** YEAR-BY-YEAR-TIMELINE provides timeline precision that neither root file has
- **Recommendation:** KEEP as supplemental to story-overview.md for author/editor reference

---

### FOURTH-PARTY-DOSSIERS-ECOLOGY.md (reference/worldbuilding/)
**Purpose:** Quick-reference encounter dossiers for non-institutional actors  
**Size:** ~150 lines  

**Contains:**
- ✓ **6 Fourth Party entities:** Forlorn Engineers, Tusk Clans, Graybar Marauders, Frosthorn Herds & Predators, Mire-Glass Colonies, Glassshore Wreckers
- Each entry: overview, behavior/ecology, resources/threats, narrative hooks, encounter rating

**OVERLAP CONCERN:**
- World-Bible says Fourth Party = "beast-kin, elemental enclaves, remnant constructs — not monolithic evil, often victims"
- story-overview.md says same (brief mention)
- **UNIQUE VALUE:** Encounter-level detail with scavenger guilds, resource conflicts, and narrative hooks
- **Gap:** World-Bible and story-overview don't distinguish between actual beast-kin civilization vs. human scavenger groups
- **Recommendation:** KEEP but clarify taxonomy (Fourth Party civilization vs. scavenger encounters)

---

## TIER 3: SPECIALIZED REFERENCE LAYER

### reference/magic-system/CHAIN-SPEAR-MASTER.md (Consolidated)
**Purpose:** Complete chain spear technical + narrative guide  
**Source Files:** CHAIN-SPEAR-COMPENDIUM.md, CHAIN-SPEAR-DEEPENING.md, CHAIN-SPEAR-SPECS.md  
**Size:** ~1,500 lines  

**Contains:**
- ✓ **PART A: World Context** — Cosmology, Magic-Physics, Geography, Timeline, Grand Alliance, Academy, Fourth Party, Ecological Crisis
- ✓ **PART B: Protagonist & Formative Systems** — Origin/Family, Upbringing, Formative Events, Hunting/Spear/Telekinesis tools
- ✓ **PART C: Chain Design & Mechanics** — Construction, Physical baseline, Memory-metal properties, States, Terminal blades, Costs/LIP, Modular tactics
- ✓ **PART D: Telekinesis Integration** — Core techniques, Mana cost tiers, Error modes, Synergy with chain
- ✓ **PART E: Combat Applications** — Offensive patterns, Defensive constructs, Mobility/Escape, Crowd control, Environmental tactics
- ✓ **PART F: Tables & Reference** — Link specifications, MU cost table, state transition chart, technique index

**OVERLAP WITH story-overview.md:** ~70%
- World context section = substantial duplication of story-overview.md's world section
- Protagonist section = duplication of story-overview.md protagonist profile
- Chain design = slight expansion on story-overview.md section 2
- Telekinesis = duplication of story-overview.md magic system
- Combat applications = NEW content not fully in story-overview.md

**OVERLAP WITH World-Bible.md:** ~65%
- Cosmology/timeline/Fourth Party = ~95% duplication
- Protagonist section = duplication
- Geographic/cultural context = duplication

**CASCADING REDUNDANCY:**
- CHAIN-SPEAR-MASTER contains its source files (CHAIN-SPEAR-COMPENDIUM/DEEPENING/SPECS) = **internal triplication**
- Never deleted source files after consolidation

**Unique Value:**
- Numeric MU cost tables and link specifications
- Detailed state transition mechanics
- Combat application patterns with environmental tactics

**Recommendation:** See consolidation strategy below

---

### reference/society/ACADEMY-POLITICS-MASTER.md (Consolidated)
**Purpose:** Institutional analysis and scene scaffolding  
**Source Files:** ACADEMY-POLITICS.md, ACADEMY-POLITICS-DEEPENED.md  
**Size:** ~800 lines  

**Contains:**
- ✓ **I. Overview** — Council, Provost & Guards, Research Divisions, Student Houses
- ✓ **II. Governance & Structure** — Council of Masters, Provost, Research Divisions, Student Houses/Guilds
- ✓ **III. Primary Factions** — Conservators, Practical Arms, Innovators, Patron Houses (with goals/power bases)
- ✓ **IV. The Exam** — Resonance Calibration Trial (setup, failure modes)
- ✓ **V. Exam Sabotage** — Mechanism, forensics, planting evidence
- ✓ **VI. Conclave Hearing Outline** — 3-act structure for resolution scene

**OVERLAP WITH story-overview.md:**
- Academy brief mention ("disciples of politically complex") — story-overview.md has NO faction details
- **Minor overlap:** ~15%

**OVERLAP WITH World-Bible.md:**
- "IV. The Academy" section mentions "four halls by culture, mission tensions"
- ACADEMY-POLITICS-MASTER expands this to 4 governance structures + 4 detailed factions
- **Moderate overlap:** ~30%

**UNIQUE VALUE:**
- Faction mechanics (Conservators vs. Practical Arms vs. Innovators goals)
- Specific scene scaffolding (Exam Sabotage, Conclave Hearing outlined)
- Evidence forensics and narrative structure

**CASCADING REDUNDANCY:**
- Contains source files (ACADEMY-POLITICS.md, ACADEMY-POLITICS-DEEPENED.md)

**Recommendation:** Unique enough to KEEP, but establish cross-reference from story-overview.md

---

### reference/techniques/COMBAT-CHOREOGRAPHY-MASTER.md (Consolidated)
**Purpose:** Tactical sequences with MU costs and narrative beats  
**Source Files:** COMBAT-CHOREOGRAPHY.md, COMBAT-CHOREOGRAPHY-EXTRA.md  
**Size:** ~1,200 lines  

**Contains:**
- ✓ **Assumptions & Notation** — 120 MU baseline, MU cost definitions
- ✓ **6 Sequences** — Alley Ambush, Open Field Duel, Sustained Defense, Urban Suppression, Cavalry Disruptor, Rescue/Extraction
- Each sequence: Context, Tactical Beats, Cost Summary, Fatigue, Link Integrity, Author Cues, Failure Modes

**OVERLAP WITH story-overview.md:**
- Phase 3: Chain/Telekinesis combos mentioned but NOT choreographed
- Chain states, techniques mentioned but NOT costed
- **Minimal direct overlap:** ~10% (same systems, different detail)

**OVERLAP WITH CHAIN-SPEAR-MASTER:**
- Both contain combat applications
- COMBAT-CHOREOGRAPHY-MASTER focuses on MU costs and narrative beats
- CHAIN-SPEAR-MASTER focuses on tactical patterns and mechanics
- **Moderate overlap:** ~25% (same combat, different lens)

**UNIQUE VALUE:**
- Scene-by-scene choreography with MU costs
- Author cues (sensory detail prompts)
- Failure modes for dramatic timing

**CASCADING REDUNDANCY:**
- Contains source files (COMBAT-CHOREOGRAPHY.md, COMBAT-CHOREOGRAPHY-EXTRA.md)

**Recommendation:** Unique enough to KEEP, but establish cross-reference from story-overview.md

---

## OTHER REFERENCE FILES

### reference/magic-system/
**Files present:**
- CHAIN-SPEAR-COMPENDIUM.md (source, now in MASTER)
- CHAIN-SPEAR-DEEPENING.md (source, now in MASTER)
- CHAIN-SPEAR-SPECS.md (source, now in MASTER)
- CHAIN-SPEAR-MASTER.md (consolidated)
- POWER-SYSTEMS-COMPREHENSIVE.md (unchecked)
- TELEKINESIS-NUMERIC.md (likely detailed costs)
- README.md

**Recommendation:** Delete source files (COMPENDIUM/DEEPENING/SPECS) after confirming MASTER is complete

---

### reference/society/
**Files present:**
- ACADEMY-POLITICS.md (source, now in MASTER)
- ACADEMY-POLITICS-DEEPENED.md (source, now in MASTER)
- ACADEMY-POLITICS-MASTER.md (consolidated)
- NPC-DOSSIERS.md (likely expanded character details)
- README.md

**Recommendation:** Delete source files after confirming MASTER is complete; check if NPC-DOSSIERS duplicates story-overview.md characters

---

### reference/techniques/
**Files present:**
- COMBAT-CHOREOGRAPHY.md (source, now in MASTER)
- COMBAT-CHOREOGRAPHY-EXTRA.md (source, now in MASTER)
- COMBAT-CHOREOGRAPHY-MASTER.md (consolidated)
- QUICK-REFERENCE-SHEETS.md (likely useful quick-lookup)
- README.md

**Recommendation:** Delete source files after confirming MASTER is complete; keep QUICK-REFERENCE-SHEETS

---

## CONSOLIDATION STRATEGY & RECOMMENDATIONS

### PRIORITY 1: Eliminate Internal Cascading Redundancy
**Problem:** Master files contain their own source files (COMPENDIUM/DEEPENING in CHAIN-SPEAR-MASTER, etc.)  
**Solution:**
1. Verify CHAIN-SPEAR-MASTER contains all content from COMPENDIUM/DEEPENING/SPECS
2. Verify ACADEMY-POLITICS-MASTER contains all content from source files
3. Verify COMBAT-CHOREOGRAPHY-MASTER contains all content from source files
4. Delete source files once verified
5. **Impact:** Remove ~40% filespace redundancy

---

### PRIORITY 2: Establish Authority Hierarchy
**Problem:** story-overview.md, World-Bible.md, and Master files all cover same ground  
**Solution:**

| **Topic** | **Primary Source** | **Supporting References** | **Authority** |
|---|---|---|---|
| Protagonist Profile | story-overview.md | World-Bible.md (summary) | Narrative intent |
| World Cosmology/Magic | World-Bible.md | story-overview.md (summary) | Worldbuilding consistency |
| Chain Spear System | CHAIN-SPEAR-MASTER.md | story-overview.md (narrative), COMBAT-CHOREOGRAPHY (application) | Technical reference |
| Academy Politics | ACADEMY-POLITICS-MASTER.md | story-overview.md (narrative context) | Institutional structure |
| Combat Choreography | COMBAT-CHOREOGRAPHY-MASTER.md | story-overview.md (narrative), CHAIN-SPEAR-MASTER (mechanics) | Scene choreography |
| Fourth Party Encounters | FOURTH-PARTY-DOSSIERS-ECOLOGY.md | World-Bible.md (context) | Encounter design |
| Timeline/Ages | YEAR-BY-YEAR-TIMELINE.md | story-overview.md (narrative phases) | Pacing reference |

**Benefits:**
- Single source of truth per topic
- Other files become cross-reference only
- Reduces maintenance burden
- Clear authority for edits

---

### PRIORITY 3: Rationalize Root-Level Files

**Current state:**
- story-overview.md = ~80% narrative overview + 20% detailed system reference
- World-Bible.md = ~50% worldbuilding reference + 50% narrative content (duplicate)

**Option A (Recommended): Two-Tier Root Level**
```
Root Level:
├── STORY-OVERVIEW.md (narrative-first, keep pure narrative)
└── REFERENCE-BIBLE.md (worldbuilding-first, pure reference)

Reference/ subdirectory:
├── worldbuilding/ (place World-Bible here, retire duplicate)
├── magic-system/
├── society/
└── techniques/
```

**Option B (Simpler): Single Root Reference**
- Keep story-overview.md as narrative entry point
- Delete World-Bible.md (everything is in CHAIN-SPEAR-MASTER, ACADEMY-POLITICS-MASTER, worldbuilding/ subdirectory)
- Cross-reference from story-overview.md to specialized references

---

### PRIORITY 4: Specific Consolidation Actions

#### A. **Delete from reference/magic-system/:**
- CHAIN-SPEAR-COMPENDIUM.md (content in CHAIN-SPEAR-MASTER)
- CHAIN-SPEAR-DEEPENING.md (content in CHAIN-SPEAR-MASTER)
- CHAIN-SPEAR-SPECS.md (content in CHAIN-SPEAR-MASTER)

#### B. **Delete from reference/society/:**
- ACADEMY-POLITICS.md (content in ACADEMY-POLITICS-MASTER)
- ACADEMY-POLITICS-DEEPENED.md (content in ACADEMY-POLITICS-MASTER)

#### C. **Delete from reference/techniques/:**
- COMBAT-CHOREOGRAPHY.md (content in COMBAT-CHOREOGRAPHY-MASTER)
- COMBAT-CHOREOGRAPHY-EXTRA.md (content in COMBAT-CHOREOGRAPHY-MASTER)

#### D. **Audit & Possibly Delete:**
- reference/worldbuilding/World-Bible.md (content scattered across story-overview.md + master files + subdirectories)
  - **Decision:** Retire if Option B chosen; keep if Option A chosen
- reference/society/NPC-DOSSIERS.md (likely duplicates story-overview.md characters)
  - **Recommendation:** Audit for new content; if same, delete

---

## DETAILED OVERLAP MATRIX

| **File** | **story-overview.md** | **World-Bible.md** | **CHAIN-SPEAR-MASTER** | **ACADEMY-POLITICS-MASTER** | **COMBAT-CHOREOGRAPHY-MASTER** | **YEAR-BY-YEAR-TIMELINE** | **FOURTH-PARTY-DOSSIERS** |
|---|---|---|---|---|---|---|---|
| **story-overview.md** | — | 60% | 70% | 15% | 10% | 0% | 5% |
| **World-Bible.md** | 60% | — | 65% | 30% | 5% | 0% | 40% |
| **CHAIN-SPEAR-MASTER** | 70% | 65% | — | 0% | 25% | 0% | 0% |
| **ACADEMY-POLITICS-MASTER** | 15% | 30% | 0% | — | 0% | 0% | 0% |
| **COMBAT-CHOREOGRAPHY-MASTER** | 10% | 5% | 25% | 0% | — | 0% | 0% |
| **YEAR-BY-YEAR-TIMELINE** | 0% | 0% | 0% | 0% | 0% | — | 0% |
| **FOURTH-PARTY-DOSSIERS** | 5% | 40% | 0% | 0% | 0% | 0% | — |

**Key:** % overlap = estimated proportion of file A's content that duplicates file B

---

## SPACE ANALYSIS

| **Category** | **Files** | **Est. Lines** | **Est. Redundancy** | **Action** |
|---|---|---|---|---|
| Source → Consolidated | COMPENDIUM/DEEPENING/SPECS + CHAIN-SPEAR-MASTER | 4,000 | Internal 3x | Delete source files |
| | ACADEMY-POLITICS + MASTER | 1,500 | Internal 2x | Delete source files |
| | COMBAT-CHOREOGRAPHY + MASTER | 2,000 | Internal 2x | Delete source files |
| Root-level overlap | story-overview.md + World-Bible.md | 1,700 | Cross-tier 60% | Retire World-Bible OR restructure |
| World-Bible + Subdirs | World-Bible.md + YEAR-BY-YEAR + FOURTH-PARTY | 1,400 | Cross-tier 40% | Consolidate to subdirs |
| **Estimated Redundancy** | | ~10,600 | ~45% | **Remove ~4,770 lines** |

---

## RECOMMENDATIONS SUMMARY

### **Immediate Actions (Week 1)**
1. **Delete** CHAIN-SPEAR-COMPENDIUM.md, CHAIN-SPEAR-DEEPENING.md, CHAIN-SPEAR-SPECS.md
2. **Delete** ACADEMY-POLITICS.md, ACADEMY-POLITICS-DEEPENED.md
3. **Delete** COMBAT-CHOREOGRAPHY.md, COMBAT-CHOREOGRAPHY-EXTRA.md
4. **Verify** no external cross-references point to deleted files

### **Medium-Term Actions (Week 2–3)**
5. **Audit** reference/society/NPC-DOSSIERS.md for unique content vs. story-overview.md
   - If duplicate → delete
   - If expanded → cross-reference from story-overview.md
6. **Clarify** FOURTH-PARTY-DOSSIERS boundary:
   - Distinguish "Fourth Party civilization (beast-kin)" vs. "Human scavenger encounters"
   - Add taxonomy to World-Bible.md or create FOURTH-PARTY-TAXONOMY.md
7. **Update** story-overview.md with cross-references:
   - Link to CHAIN-SPEAR-MASTER for technical details
   - Link to ACADEMY-POLITICS-MASTER for faction mechanics
   - Link to COMBAT-CHOREOGRAPHY-MASTER for scene choreography

### **Long-Term Actions (Week 3–4)**
8. **Decide** on root structure (Option A vs. Option B)
   - Option A: Restructure to STORY-OVERVIEW + REFERENCE-BIBLE at root, consolidate World-Bible → reference/worldbuilding/
   - Option B: Keep story-overview.md, delete World-Bible.md, have all references point to specialists

### **Ongoing Maintenance**
9. **Establish protocol:** Any edit to cosmology/magic/characters → update PRIMARY SOURCE, then cascade to supporting references
10. **Regular audit:** Monthly check for new redundancy as content evolves

---

## FILES AWAITING AUDIT

These files were not fully analyzed; recommend secondary review:
- reference/magic-system/POWER-SYSTEMS-COMPREHENSIVE.md (may duplicate CHAIN-SPEAR-MASTER)
- reference/magic-system/TELEKINESIS-NUMERIC.md (may be absorbed into CHAIN-SPEAR-MASTER)
- reference/society/NPC-DOSSIERS.md (likely duplicates story-overview.md character section)
- reference/techniques/QUICK-REFERENCE-SHEETS.md (likely useful companion; keep)

---

## CONCLUSION

The repository contains **40–60% duplicated content** across three documentation tiers due to:
1. **Intentional consolidation without cleanup** (source files retained after master creation)
2. **Overlapping scopes** (story-overview.md and World-Bible.md both try to be complete references)
3. **Lack of authority hierarchy** (unclear which file is "canonical" for any given topic)

**Recommended savings:** ~4,770 lines removed through deduplication.  
**Implementation effort:** 2–3 hours to execute + ongoing maintenance.  
**Benefit:** Clearer maintenance, reduced merge conflicts, faster edits.

