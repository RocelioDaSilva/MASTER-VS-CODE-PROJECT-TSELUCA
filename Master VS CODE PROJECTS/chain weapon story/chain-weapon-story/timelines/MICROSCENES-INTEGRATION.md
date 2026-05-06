# Micro-scenes Integration Notes

Generated: 2026-04-05

Summary:
- Collects candidate micro-scenes found in the manuscript and proposes a lightweight, non-destructive integration plan.

Found candidates (scan highlights):
- [story/Chapter-05-Elaras-Ambush-and-Care.md](story/Chapter-05-Elaras-Ambush-and-Care.md) — contains a present narration plus flashback material (Aisen 10 present; flashback Aisen 7–8). Candidate for extracting flashback anchor.
- [story/Chapter-50-Final-Micro-Scene-Recurrence.md](story/Chapter-50-Final-Micro-Scene-Recurrence.md) — chapter composed of short vignettes; treat as a hub or extract to micro-scenes/
- story/scene-final-stand-expanded.md — standalone vignette snippet found in `story/` (micro‑vignette language).
- Additional candidates: chapters flagged as `Ambiguous` or with multiple timeframes in `timelines/AGES-CHECK.csv` (e.g., Ch05, Ch19, Ch33).

Proposed integration approach (non-destructive):
1. Add front-matter tagging to candidate chapters: `MicroScenes: true` and `MicroSceneAnchors: [id1,id2]`.
2. Prefer anchor-and-reference (keep text inline) by adding brief anchor markers and a short comment block identifying the micro-scene, e.g. `<!-- MicroScene: flashback-a01 -->`.
3. Optional extraction: move repeatable micro-vignettes to `micro-scenes/<id>.md` and include via a short include pattern or a two-line reference to avoid duplication.
4. Update `timelines/CONTINUITY-TIMELINE.md` to list micro-scene anchors and canonical ages for their timeframe.
5. Author review: confirm which flashbacks should be extracted vs left inline.

Suggested anchors (examples):
- `flashback-a01` — Ch05: Aisen childhood ambush (Aisen 7–8)
- `vignette-50-1..N` — Ch50: series of short vignettes to be enumerated
- `final-stand-micro` — scene-final-stand-expanded.md snippet

Action items for the next pass:
- If you approve, I can (a) tag chapters with anchor markers, (b) optionally extract to `micro-scenes/`, and (c) update the continuity timeline with references.

Notes:
- This integration is deliberately conservative so it doesn't rewrite or remove any existing manuscript text without author sign-off.

Extracted micro-scenes (this pass):
- `micro-scenes/scene-001.md` — Marta: economic worry (extracted from Chapter-01)
- `micro-scenes/scene-002.md` — Aldric: moral erosion (extracted from Chapter-03)
