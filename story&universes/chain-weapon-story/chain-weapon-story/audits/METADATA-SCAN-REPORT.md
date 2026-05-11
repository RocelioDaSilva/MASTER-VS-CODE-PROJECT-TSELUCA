# METADATA SCAN REPORT — Scene Frontmatter Audit

Date: 2026-03-30

Purpose
-------
Automated pass across repository Markdown files to detect presence of required scene frontmatter (Title, SceneID, POV, Anchors, Tags, LimitBreak, Severity, Chronology) as defined in `structure/WRITING-GUIDELINES-PERSPECTIVE.md` and `structure/VERIFICATION-CHECKLIST.md`.

Method
------
- Scanned all `*.md` files in repository root and subfolders.
- For each file, inspected the top ~200 lines for occurrences of the frontmatter keys.
- Marked files that contain scene-like content (micro-scenes, timeline, story chapters) as `Scene Candidate` and noted remediation suggestions.

Summary Results
---------------

| File | Scene Candidate? | Keys Found | Missing Keys | Notes |
|---|---:|---|---|---|
| timelines/timeline.md | No | none | All | Mermaid timeline; not a scene file. Keep as meta doc. |
| timelines/chain-diagram.md | No | none | All | Weapon-mechanics diagram; not a scene file. |
| theme/prejudice-as-narrative.md | No | none | All | Thematic doc; not a scene file. |
| README.md | No | none | All | Project README; not a scene file. |
| structure/WRITING-GUIDELINES-PERSPECTIVE.md | No (guidelines) | example frontmatter (code block) | All (not applied) | Contains a code example showing required frontmatter but does not include frontmatter itself. |
| structure/VERIFICATION-CHECKLIST.md | No (tooling) | none | All | Checklist doc; not an individual scene file. |
| structure/SIDE-CHARACTER-MOMENTS.md | Yes (micro-scene bank) | inline tags (`[downtime]`, `[recurrence]`, `[location:]`, `[character:]`) | Frontmatter keys (Title, SceneID, POV, Anchors, Tags, LimitBreak, Chronology) | Contains many micro‑scenes and recurrence notes; should be split into standalone scene files or augmented with standardized frontmatter per micro‑scene. Also: Scene 22 (Naia) describes a clear limit‑break but lacks `LimitBreak: true` and `Severity`. |
| structure/PRE-ACADEMY-TIMELINE.md | Yes (seed timeline) | none | All | Timeline/meta doc with many seed encounters; convert high-value seed encounters into scene files with frontmatter. |
| structure/LIMIT-BREAKING-BACKLASH.md | No | none | All | Specification doc; not a scene file (but used to inform `LimitBreak` metadata). |
| structure/GOWR-PERSPECTIVE-METHOD.md | No | none | All | Method doc; not a scene file. |
| structure/CHARACTER-INTERACTION-SPREADSHEET.md | No | none | All | Spreadsheet template; not a scene file. |
| structure/CHARACTER-INTERACTION-MATRIX.md | No | none | All | Matrix doc; not a scene file. |
| story-overview.md | No | none | All | Master overview; not a scene file. |
| magic-system/telekinesis-core.md | No | none | All | System doc; not a scene file. |
| audits/SIDE-CHARACTER-MOMENTS-audit.md | No | none | All | Audit file (meta). |
| audits/PRE-ACADEMY-TIMELINE-audit.md | No | none | All | Audit file (meta). |
| characters/main/aisen.md | No | none | All | Character profile; not a scene file. |
| characters/mentors/guard-mentor.md | No | none | All | Mentor profile; not a scene file. |
| characters/mentors/cleric-mentor.md | No | none | All | Mentor profile; not a scene file. |

Findings — High Level
---------------------
- No repository Markdown file currently contains the required scene frontmatter block at the top — either because files are meta documents (guides, templates, analysis) or because scene content is stored in consolidated banks (`SIDE-CHARACTER-MOMENTS.md`, `PRE-ACADEMY-TIMELINE.md`) rather than as standalone scene files.
- `structure/SIDE-CHARACTER-MOMENTS.md` is the highest-priority target for conversion: it contains ~51 micro‑scenes, several of which imply limit‑breaking (e.g., Naia) but are not tagged with `LimitBreak: true` and `Severity` in a standardized frontmatter form.
- `structure/PRE-ACADEMY-TIMELINE.md` contains many seed encounters that should be converted into individual scene files to comply with the checklist and support automated auditing.

Recommended Next Steps
----------------------
1. Option A (recommended): Auto‑generate scene stubs for high‑value micro‑scenes and seed encounters.
   - Convert top N micro‑scenes (default N=10) into `story/` files named `<Chapter##_Scene##>_<slug>.md` with required frontmatter and the existing content moved into the body. Add `LimitBreak` metadata where implied.
2. Option B: Run an automated pass that lists only candidate files and creates a CSV of missing keys for human review (no file writes). Good if you want to review before changes.
3. Option C: I can produce suggested frontmatter blocks for specified files in this chat for manual insertion.

Proposed immediate action (I can run now)
---------------------------------------
- Create scene stubs for the following seed/micro-scenes (first-pass N=8):
  - `structure/SIDE-CHARACTER-MOMENTS.md` — Scene 22 (Naia, healer limit‑break) → `story/naia_healer_limitbreak.md`
  - `structure/SIDE-CHARACTER-MOMENTS.md` — Scene 17 (Refugee Camp) → `story/refugee_camp_firstwave.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Tavern Opening Scene (Age 5) → `story/tavern_opening_aisen.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Caspian first encounter (Age 5) → `story/caspian_first_encounter.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Harald arrival (Age 6) → `story/harald_arrives.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Tarovin candle demo (Age 6) → `story/tarovin_candle_demo.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Elara ambush (Age 7) → `story/elara_ambush.md`
  - `structure/PRE-ACADEMY-TIMELINE.md` — Kaelen flower grove (Age 11) → `story/kaelen_flower_grove.md`

- For each stub, I will: create a file under `story/` with the required frontmatter fields, paste the existing micro/seed content as the body, and tag `LimitBreak: true` when the body implies a breaking event.

Would you like me to (A) auto‑generate the suggested scene stubs now, (B) produce a CSV of all Markdown files and missing keys for you to review, or (C) create draft frontmatter blocks here for manual insertion? Reply with A, B, or C (or give an alternate instruction).
