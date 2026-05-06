---
name: Chapter / Story PR Template
about: Use for any new or expanded chapter, B-chapter, or scene draft
title: "WRITE: Ch [number] [title] — [POV] — Draft"
labels: ["draft", "chapter"]
---

## Summary
<!-- One sentence: what this chapter does narratively. -->

## Chapter metadata
| Field | Value |
|-------|-------|
| Chapter number | |
| POV character | |
| Act | |
| Type | NEW / EXPAND / EXISTING-REVISION |
| Target word count | |
| Actual word count | |

## Arc beats addressed
<!-- List which arc beats (A–E) this chapter advances, and how. -->
- Arc [letter]: [beat name] — [1 sentence]

## Character beats
<!-- Which character's arc does this chapter advance? At which beat? -->
- [Character]: [beat] — [scene reference]

## Handoff
<!-- Where does the camera come FROM and where does it GO? What physical object or detail carries continuity? -->
- **Receives from**: [previous chapter / POV]
- **Returns to**: [next chapter / POV]
- **Handoff object/detail**: [specific item or observation]

## Worldbuilding references
<!-- List any worldbuilding files consulted or cited in this chapter. -->
- [ ] `worldbuilding/` file: [path] — [how used]

## MU accounting (if combat/magic present)
<!-- If the chapter contains magic use or combat, fill this in. -->
| Character | MU reserve | MU expended | Notes |
|-----------|-----------|-------------|-------|
| | | | |

## Review checklist
### Draft quality
- [ ] Draft is ≥ 3,000 words (or target justified)
- [ ] YAML front-matter present with all required fields
- [ ] No info-dump exposition (integrate through action/dialogue)
- [ ] At least one sensory anchor per scene
- [ ] Unique POV detail present (only this character could narrate this)

### Character
- [ ] POV character's Lie or Flaw is present (even if only implied)
- [ ] At least one vulnerability moment
- [ ] Mannerism appears at least once
- [ ] Handoff is explicit and consistent with next chapter

### Political / worldbuilding
- [ ] At least one political arc thread advanced or referenced
- [ ] Any worldbuilding references are accurate to source files
- [ ] No new worldbuilding introduced without corresponding file update

### Technical
- [ ] CI/front-matter check passes
- [ ] Build script runs without error
- [ ] No tracked secrets, real names, or external PII
 - [ ] Formatting check (Black) passes
 - [ ] Linting (Flake8) passes
 - [ ] Tests pass (pytest)

### Review
- [ ] Continuity reviewer assigned and approved
- [ ] Editorial reviewer assigned and approved

## Notes
<!-- Any open questions, deferred items, or flags for future chapters. -->
