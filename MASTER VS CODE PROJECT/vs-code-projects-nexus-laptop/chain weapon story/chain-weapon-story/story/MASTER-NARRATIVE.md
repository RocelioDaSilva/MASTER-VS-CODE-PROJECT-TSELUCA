---
title: "TBD"
status: Draft
updated: 2026-04-15
pov:
age:
chapter_number:
---

# MASTER NARRATIVE — Thornwood Chronicle (Draft Integration)

This document is a working master index and integration skeleton for assembling the Thornwood Chronicle into a single, chapter-ordered narrative. It references existing scene files in `story/` and includes short placement notes and excerpts where appropriate. Use this to produce a single concatenated manuscript or to guide copy/paste integration.

---

## Table of Contents (Recommended Chapter Order)

### Act I — Origins & Teaching
- Chapter 1: Aldric's Teaching Years — [ALDRIC-MENTOR-SCENES.md](ALDRIC-MENTOR-SCENES.md)
- Chapter 2: Aldric's Execution (flashback) — [ALDRIC-EXECUTION-SCENE.md](ALDRIC-EXECUTION-SCENE.md)
- Chapter 3: Ryo's Vision (introduction) — [RYO-VISION-CHASM-PROSE.md](RYO-VISION-CHASM-PROSE.md)
- Chapter 4: Early Collisions (Aisen & others) — [CHARACTER-COLLISION-SCENES.md](CHARACTER-COLLISION-SCENES.md)

### Act II — Exposure & War
- Chapter 5: Aisen's War Service / Conscription — [AISEN-WAR-SERVICE.md](AISEN-WAR-SERVICE.md)
- Chapter 6: Ryo & Kairos meetings / training — [RYO-AISEN-CAMPFIRE-SCENE.md](RYO-AISEN-CAMPFIRE-SCENE.md) and [RYO-ADDITIONAL-SCENES.md](RYO-ADDITIONAL-SCENES.md)
- Chapter 7: Corvin Bargain (past) — [CORVIN-BARGAIN-SCENE.md](CORVIN-BARGAIN-SCENE.md)
- Chapter 8: Caspian Heart-loss sequence — [CASPIAN-HEART-LOSS-SCENE.md](CASPIAN-HEART-LOSS-SCENE.md)
- Chapter 9: Kairos loop montage — [KAIROS-LOOP-MONTAGE.md](KAIROS-LOOP-MONTAGE.md)

### Act III — Thornwood Hollow & Aftermath
- Chapter 10: Pre-siege preparation — [AISEN-PREPARATION-WEEKS.md](AISEN-PREPARATION-WEEKS.md)
- Chapter 11: Tactical movement & siege (narrative) — [THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md](THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md)
- Chapter 12: Final Stand (Aisen's scene) — [AISEN-FINAL-STAND-THORNWOOD.md](AISEN-FINAL-STAND-THORNWOOD.md)
- Chapter 13: Soldier perspectives (breakdown) — [SOLDIER-PERSPECTIVES-BREAKDOWN.md](SOLDIER-PERSPECTIVES-BREAKDOWN.md)
- Chapter 14: Refugee escape & settlement — [REFUGEE-PERSPECTIVES-ESCAPE.md](REFUGEE-PERSPECTIVES-ESCAPE.md)

### Epilogue & Echoes
- Chapter 15: Ryo unified being (fusion aftermath) — [RYO-UNIFIED-BEING.md](RYO-UNIFIED-BEING.md)
- Chapter 16: Orin wanderer / confession continued — [ORIN-WANDERER.md](ORIN-WANDERER.md) and [ORIN-DRUNK-CONFESSION.md](ORIN-DRUNK-CONFESSION.md)
- Chapter 17: Corvin final arc — [CORVIN-HOLLOW-KNIGHT-FINAL.md](CORVIN-HOLLOW-KNIGHT-FINAL.md)
- Chapter 18: Caspian aftermath — [CASPIAN-HEART-LOSS-AFTERMATH.md](CASPIAN-HEART-LOSS-AFTERMATH.md)
- Chapter 19: Memorials & remembrance — [THORNWOOD-MEMORIALS-AND-VIGILS.md](THORNWOOD-MEMORIALS-AND-VIGILS.md)
- Chapter 20: Tactical appendix & analysis — [THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md](THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md)

---

## Integration notes
- The files above are the canonical scene files in `story/`. Use the order above to assemble chapters.
- Scenes are written primarily in third-person multi-POV. When compiling, preserve original POV blocks and keep section breaks where a file naturally divides scenes.
- To avoid duplication, do not copy the same scene twice. Use the master index as the single source-of-truth.

## Quick integration (PowerShell example)
If you want to produce a single concatenated Markdown file in this workspace, run this PowerShell snippet from the repository root (adjust order as needed):

```powershell
$files = @(
  'story/ALDRIC-MENTOR-SCENES.md',
  'story/ALDRIC-EXECUTION-SCENE.md',
  'story/RYO-VISION-CHASM-PROSE.md',
  'story/CHARACTER-COLLISION-SCENES.md',
  'story/AISEN-WAR-SERVICE.md',
  'story/RYO-AISEN-CAMPFIRE-SCENE.md',
  'story/CORVIN-BARGAIN-SCENE.md',
  'story/CASPIAN-HEART-LOSS-SCENE.md',
  'story/KAIROS-LOOP-MONTAGE.md',
  'story/AISEN-PREPARATION-WEEKS.md',
  'story/THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md',
  'story/AISEN-FINAL-STAND-THORNWOOD.md',
  'story/SOLDIER-PERSPECTIVES-BREAKDOWN.md',
  'story/REFUGEE-PERSPECTIVES-ESCAPE.md',
  'story/RYO-UNIFIED-BEING.md',
  'story/ORIN-DRUNK-CONFESSION.md',
  'story/ORIN-WANDERER.md',
  'story/CORVIN-HOLLOW-KNIGHT-FINAL.md',
  'story/CASPIAN-HEART-LOSS-AFTERMATH.md',
  'story/THORNWOOD-MEMORIALS-AND-VIGILS.md',
  'story/THORNWOOD-HOLLOW-TACTICAL-CHOREOGRAPHY.md'
)
Get-Content $files | Set-Content story/MASTER-NARRATIVE-FULL.md
```

Notes:
- This does a raw concatenation. You may want to insert chapter breaks or frontmatter between files.
- For a clean manuscript, run a lightweight pass to normalize headings and remove duplicate frontmatter.

---

## Editorial suggestions
- Run one stylistic pass to unify tense and POV transitions between adjacent files.
- Add chapter headings explicitly between concatenated files (e.g., `## Chapter X - Title`) when building the single manuscript to aid readability.
- Create a `manuscript/` folder and place the concatenated output there: `manuscript/Thornwood-Chronicle.md` for long-term versioning.

---

**END: MASTER NARRATIVE (integration skeleton)**
