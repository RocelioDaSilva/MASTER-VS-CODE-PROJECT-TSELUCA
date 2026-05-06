---
title: Repository & Documentation Improvements
date: April 9, 2026
purpose: Enhance organization, searchability, and usability
status: Implementation Guide
---

# Repository & Documentation Improvements

## IMPROVEMENT 1: Enhanced Scene Quick-Reference Index

**Purpose:** Enable rapid location of specific scene types, character moments, and thematic content

**Create:** `/story/SCENE-QUICK-INDEX.md`

### Index Categories
- **Emotional Breakthrough Scenes** — Character growth moments (chapters 1, 15, 28, 46, 49)
- **Combat Showcase Scenes** — Best chain spear examples, telekinesis displays
- **Conspiracy Revelation Scenes** — Information dumps, plot twists
- **Character Relationship Moments** — One-on-ones, group dynamics
- **System Explanation Scenes** — Where magic, Heresy, limit breaks first appear
- **Sensory Strongholds** — Prose highlights for beta reader attention
- **Dialogue Showcases** — Speech pattern examples by character

**Benefits:**
- Faster scene location during revision
- Clear section for beta readers: "Read this for character chemistry"
- Easy identification of scenes needing polish

---

## IMPROVEMENT 2: Character Development Tracker

**Purpose:** Verify each character's arc is complete and consistent

**Create:** `/characters/CHARACTER-ARC-COMPLETION-STATUS.md`

```markdown
# Character Arc Completion Status

## Aisen Korv
- **Arc Type:** Transformation (observer → agent → sacrifice)
- **Establishment:** Chapter 1 (tavern scene, vulnerability)
- **Development:** Chapters 6-46 (network building, philosophy)
- **Crisis:** Chapter 45 (HQ assault, final choice)
- **Resolution:** Chapter 46 (death as completed choice)
- **Legacy:** Chapters 48-52 (impact shown through others)
- **Status:** ✅ Complete

## [Other characters...]
```

**Each character should show:**
- ✅ Clear establishment of starting belief/limitation
- ✅ At least 3 scenes of active development
- ✅ One major crisis forcing change
- ✅ Visible resolution (even if ambiguous)

---

## IMPROVEMENT 3: Plot Hole Prevention Document

**Purpose:** Pre-emptively identify and document any narrative gaps

**Create:** `/documentation/KNOWN-QUESTIONS-AND-ANSWERS.md`

**Format:**
```markdown
## Questions Readers Will Ask

### Q: Why doesn't Aisen use telekinesis to solve problem X?
**A:** [Narrative answer + chapter reference]
**Foreshadowing:** Chapter Y established this limitation
**Thematic Purpose:** Reinforces "ordinary people with limits" theme

### Q: What happened to character A after Chapter X?
**A:** [Character continues in Chapter Z, storyline resolves at...]
**Reader May Miss:** This is intentional time jump to show passage
```

**Action Items:**
- [ ] Anticipate 15-20 likely reader questions
- [ ] Write clear answers with chapter references
- [ ] Identify any questions without good answers (plot holes)
- [ ] Use this during beta reader response phase

---

## IMPROVEMENT 4: Sensory Consistency Map

**Purpose:** Ensure sensory details feel authentic to world and POV

**Create:** `/style/SENSORY-ANCHORS-BY-CHARACTER.md`

**Structure:**
```markdown
## Aisen's Sensory Priorities
- **Dominant Sense:** Touch (chain grip, muscle memory)
- **Secondary:** Sound (alertness to danger)
- **Tertiary:** Visual (tactical awareness)
- **Weak:** Smell (doesn't register unless threat-relevant)
- **Example Passages:** [List 3 scenes showing this pattern]

## Caspian's Sensory World
- **Dominant Sense:** Proprioceptive (body as tool)
- **Secondary:** Visual (aesthetics, beauty)
- ...
```

**Verification Process:**
- [ ] Read 2 Aisen scenes → verify sensory pattern
- [ ] Read 2 Caspian scenes → verify distinct pattern
- [ ] Confirm each POV feels consistent

---

## IMPROVEMENT 5: Dialogue Voice Guide

**Purpose:** Make character dialogue instantly recognizable

**Create:** `/characters/DIALOGUE-VOICE-PATTERNS.md`

**Per Character:**
```markdown
## Aisen
- **Sentence structure:** Short to medium, direct
- **Vocabulary:** Practical, concrete (not flowery)
- **Speech habits:** Rarely asks questions; states observations
- **Emotional tells:** Hesitates before admitting feelings
- **Signature phrases:** "That's..." [incomplete thoughts showing discomfort]
- **Example lines:** [Provide 5 authentic dialogue examples]

## Caspian
- **Sentence structure:** Often elegant, sometimes fragmented
- **Vocabulary:** Precise, aesthetic, occasionally poetic
- **Speech habits:** Makes declarations, not requests
- ...
```

**Verification:** Can reader recognize speaker by dialogue alone?

---

## IMPROVEMENT 6: Pacing Heat Map

**Purpose:** Visualize tension distribution across all 52 chapters

**Create:** `/structure/MANUSCRIPT-PACING-HEAT-MAP.md`

```markdown
# Pacing Heat Map

## Act I (Chapters 1-12)
| Ch | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|
|Int| 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟠 | 🟠 | 🟠 | 🟠 | 🟡 | 🟠 |

🟢 = Low intensity (recovery/setup)
🟡 = Medium intensity (development/conflict)
🟠 = High intensity (climax/revelation)
🔴 = Extreme intensity (major crisis)

## Analysis
- No more than 3 consecutive 🔴 chapters
- Minimum 1 🟢 per 5 chapters for reader recovery
- [Pattern assessment]
```

---

## IMPROVEMENT 7: Magic System Reference Quick Card

**Purpose:** One-page system summary for consistency checking

**Create:** `/reference/magic-system/ONE-PAGE-REFERENCE.md`

```markdown
# Magic System Quick Reference

## Core Rules (Non-Negotiable)
1. Every use requires precise intention or it fails
2. Major power expenditure = temporary or permanent cost
3. No power can do everything (each has clear limit)
4. Extended use causes mental fatigue (not just mana)

## Aisen's Chain Spear
- **Techniques:** 50+ (see CHAIN-SPEAR-MASTER.md)
- **Cost:** Physical exhaustion, practice/maintenance requirement
- **Limit:** Speed/complexity bound by muscle memory
- **Signature:** Precision over power

## Caspian's Erasure
- **Cost:** Each erased memory costs emotional resonance
- **Limit:** Can only erase memories, not prevent new ones
- **Unique:** Uses willing victim's own consciousness

## [Other systems...]
```

---

## IMPROVEMENT 8: Timeline Verification Sheet

**Purpose:** Catch any chronological inconsistencies

**Create:** `/timelines/COMPREHENSIVE-CONSISTENCY-CHECK.md`

**Track:**
```markdown
| Character | Age at Start | Current Age | Chapters | Key Events |
|-----------|--------------|-------------|----------|-----------|
| Aisen | 12 | 24-25 | 1-52 | Birth? | Tavern → Academy → War |
| Caspian | ~20 | ~32 | 6+? | Meet Aisen? | Romance arc shape |
| [Others] | | | | |

## Seasonal/Temporal Markers
- Chapter 1-12: [Season?] Age 12-14
- Chapter 13-38: [Years?] Age 14-24
- Chapter 39+: [Rapid?] Age 24-25

## Validity Checks
- [ ] No character ages impossibly fast/slow
- [ ] Time jumps clearly marked in text
- [ ] Weather/seasons feel consistent
```

---

## IMPROVEMENT 9: "Show Don't Tell" Audit Sample

**Purpose:** Identify opportunity to strengthen prose through demonstration

**Create:** `/style/PROSE-STRENGTH-AUDIT.md`

**Example Format:**
```markdown
## Scene 1: Tavern Opening
**Current (tells):** "Aisen felt nervous about the stranger"
**Strengthened (shows):** "Aisen's grip tightened on his cup. A drop of water slipped down his thumb."

**Current:** "He was talented but humble"
**Strengthened:** [Show through action/dialogue/consequence]
```

**Process:**
- [ ] Identify 20-30 "tell" moments across manuscript
- [ ] Write stronger "show" alternatives
- [ ] Prioritize by emotional importance

---

## IMPROVEMENT 10: Reader Expectation vs. Delivery Matrix

**Purpose:** Ensure story delivers on promises made in early chapters

**Create:** `/documentation/NARRATIVE-PROMISES.md`

```markdown
# Narrative Promises & Delivery

## Promise Made
**Chapter 1:** Aisen is ordinary; the world has prodigies
**When Delivered:** Shown consistently through Acts I-II
**Payoff:** Act III shows ordinary person's consequential choice
**Verification:** ✅ Delivered

## Promise Made
**Chapter 3:** Chain spear is versatile tool, not random weapon
**When Delivered:** Chapters throughout show applications
**Payoff:** Combat system feels earned and consistent
**Verification:** ✅ Delivered

## Promise Made (Check These)
**Chapter X:** [Setup]
**When Delivered?** [Or is this unfulfilled?]
**Status:** ⚠️ Needs attention
```

---

## IMPROVEMENT 11: Documentation README Update

**Purpose:** Help future readers navigate all resources

**Update:** `/documentation/README.md`

Add sections:
```markdown
## Quick Reference by Task

### "I'm writing a scene and need to..."
- **...check if this power was already established** →  SYSTEMS-TO-DOCUMENTATION-INDEX
- **...verify when a character first appeared** → CHARACTER-APPEARANCE-INDEX
- **...know what happened to character X** → CHARACTER-MASTER-INDEX
- **...find chapters in a specific arc** → ARC-TO-SCENES-INDEX
- **...understand the world timeline** → timelines/COMPREHENSIVE-CONSISTENCY-CHECK

### "I'm revising and need to..."
- **...verify pacing feels good** → REVISION-STRATEGY-APRIL-2026 → Phase 1
- **...ensure magic system consistency** → REVISION-STRATEGY-APRIL-2026 → Phase 2
- **...check dialogue sounds natural** → /style/DIALOGUE-VOICE-PATTERNS.md
- **...find sensory inconsistencies** → /style/SENSORY-ANCHORS-BY-CHARACTER.md

### "I'm giving this to beta readers and they'll ask..."
- **...why character didn't use power X** → KNOWN-QUESTIONS-AND-ANSWERS
- **...did you mean for this to be confusing** → KNOWN-QUESTIONS-AND-ANSWERS
- **...what's your magic system** → /reference/magic-system/ONE-PAGE-REFERENCE.md
```

---

## IMPROVEMENT 12: Version Control & Change Tracking

**Purpose:** Document what changed and why between drafts

**Create:** `/documentation/REVISION-LOG-APRIL-2026.md`

```markdown
# Revision Log — April 2026

## Session: Strategic Improvements Phase

### Changes Made
| Date | Component | Change | Reason | Files |
|------|-----------|--------|--------|-------|
| 4/9 | Pacing | Created heat map | Verify Act I-III balance | MANUSCRIPT-PACING-HEAT-MAP.md |
| 4/9 | Characters | Added arc tracker | Ensure completeness | CHARACTER-ARC-COMPLETION-STATUS.md |

### Analysis
- [Findings from this session]
- [Gaps identified]
- [Next priorities]
```

---

## Quick Implementation Checklist

### Week 1: Documentation Foundation
- [ ] Create REVISION-STRATEGY-APRIL-2026.md
- [ ] Create KNOWN-QUESTIONS-AND-ANSWERS.md
- [ ] Create CHARACTER-ARC-COMPLETION-STATUS.md
- [ ] Create SENSORY-ANCHORS-BY-CHARACTER.md

### Week 2: Manuscript Audits
- [ ] Complete Pacing Heat Map (read all 52 chapters, rate by intensity)
- [ ] Complete Dialogue Voice Patterns (3 lines per character minimum)
- [ ] Complete Timeline Verification
- [ ] Identify & document 15-20 potential plot holes

### Week 3: Resource Documentation
- [ ] Create Scene Quick-Reference Index
- [ ] Create Narrative Promises Matrix
- [ ] Update Documentation README
- [ ] Create One-Page Magic Reference

### Week 4: Integration & Application
- [ ] Use heat map to identify 10-15 chapters for prose polish
- [ ] Apply dialogue improvements
- [ ] Verify character consistency
- [ ] Prepare for beta reader feedback

---

## Files to Create/Update Summary

**New Files:**
1. REVISION-STRATEGY-APRIL-2026.md (created) ← Start here
2. /story/SCENE-QUICK-INDEX.md
3. /characters/CHARACTER-ARC-COMPLETION-STATUS.md
4. /characters/DIALOGUE-VOICE-PATTERNS.md
5. /documentation/KNOWN-QUESTIONS-AND-ANSWERS.md
6. /style/SENSORY-ANCHORS-BY-CHARACTER.md
7. /style/PROSE-STRENGTH-AUDIT.md
8. /structure/MANUSCRIPT-PACING-HEAT-MAP.md
9. /reference/magic-system/ONE-PAGE-REFERENCE.md
10. /timelines/COMPREHENSIVE-CONSISTENCY-CHECK.md
11. /documentation/NARRATIVE-PROMISES.md
12. /documentation/REVISION-LOG-APRIL-2026.md

**Files to Update:**
- /documentation/README.md (add quick reference by task)

---

## Success Criteria for Each Improvement

✅ **Scene Quick-Reference:** Reader can locate any scene type in <5 seconds  
✅ **Character Arc Tracker:** Each of 9 POV characters shows clear growth  
✅ **Plot Hole Document:** No reader question goes unanswered  
✅ **Sensory Map:** Each character feels sensorily distinct  
✅ **Dialogue Guide:** Each speaker recognizable by voice alone  
✅ **Pacing Heat Map:** No more than 2 consecutive high-intensity chapters  
✅ **Magic Reference:** Consistency verified across all systems  
✅ **Timeline Check:** Zero chronological contradictions  
✅ **Narrative Promises:** Every major setup is paid off  
✅ **Documentation README:** New reader knows exactly where to look  

---

## Repository Health Indicators (Current State)

| Metric | Status | Target |
|--------|--------|--------|
| Cross-references | ✅ Excellent (4 hubs created) | Maintain |
| Organization | ✅ Good (20+ folders) | Add 2-3 new audit docs |
| Consistency tracking | ⚠️ Partial (seen in audits/) | Complete all 12 improvements |
| Reader navigation | ✅ Good (README updated) | Enhance with quick-ref |
| Revision readiness | 🟡 Medium (audit work done) | Complete Phase 1-2 |

