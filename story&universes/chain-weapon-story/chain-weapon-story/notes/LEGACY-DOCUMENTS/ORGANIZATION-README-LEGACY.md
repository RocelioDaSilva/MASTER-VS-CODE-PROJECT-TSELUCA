Repository layout

- `story/` — per-scene Markdown files (one file per scene).
- `structure/` — canonical design documents and method specs (POV method, timelines, micro-scene banks, limit-break rules).
- `audits/` — verification outputs and scan reports.
- `memories/` — session and repo memory files.

Scene file conventions

- Filename: `scene-XXX.md` (zero-padded scene number matching `SceneID`).
- Required frontmatter (YAML block or simple key/value header):

  - `Title`: short title
  - `SceneID`: scene-### (matches filename)
  - `POV`: focal character for the scene
  - `Anchors`: comma-separated character names present in the anchor interaction
  - `Tags`: comma-separated tags (e.g., downtime, recurrence, Tavern)
  - `LimitBreak`: true|false
  - `Severity`: Minor|Moderate|Severe|Catastrophic (required if `LimitBreak: true`)
  - `Chronology`: timeline reference (e.g., "Age 8-10")

Frontmatter example

---
Title: The Empty Coin Jar
SceneID: scene-001
POV: Marta
Anchors: Marta
Tags: downtime, recurrence, Tavern, Economic Decline
LimitBreak: false
Severity: None
Chronology: Age 8-10
---

Workflow notes

- After creating or editing scene files, run the `structure/VERIFICATION-CHECKLIST.md` audit and save audits to `audits/`.
- Naming and SceneID consistency matters for automated scans and the Character Interaction spreadsheet.
- If you want full scene drafts instead of stubs, indicate that and I'll generate them in batches.

Next steps

- I created an initial batch of scene stubs (Scenes 1–10) under `story/` next. I'll continue in batches until all micro-scenes are converted, then run a metadata scan if you want.