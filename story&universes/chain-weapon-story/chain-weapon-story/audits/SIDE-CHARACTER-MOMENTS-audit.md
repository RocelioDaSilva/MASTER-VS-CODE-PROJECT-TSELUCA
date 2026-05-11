Scene: SIDE-CHARACTER-MOMENTS (Micro‑Scene Bank)
File: structure/SIDE-CHARACTER-MOMENTS.md
POV: Mixed (banked micro-scenes; per‑scene POV varies)
CheckedBy: GitHub Copilot — 2026-03-30

- Frontmatter: FLAG — AuditNote: This file is a consolidated micro‑scene bank with per‑scene headings and inline tags, not individual scene files with YAML frontmatter. Consider splitting high‑value micro‑scenes into individual scene files under `story/` or adding standardized frontmatter blocks for each micro‑scene.
- Anchor opener: PARTIAL — AuditNote: Many micro‑scenes contain clear context and an event (e.g., "Marta counts coins") but do not consistently use the required anchor opener style within the first two paragraphs. Add a short anchor sentence for each scene when converting.
- POV match: FLAG — AuditNote: Scenes include `character:` tags but lack explicit `POV:` frontmatter; map `character` → `POV` when converting.
- LimitBreak tagging: FLAG — AuditNote: Scene 22 ("The Healer's Dilemma" / Naia) describes a clear limit‑break (burned out mana reserves and permanent damage) but lacks `LimitBreak: true` and `Severity` metadata. Several other scenes imply overuse of power without formal tags.
- Cost anchor line: FLAG for Naia (Scene 22) — AuditNote: Add a one‑line sensory/functional cost anchor (e.g., "Her hands trembled and the warmth never fully returned.").
- Metadata completeness: PARTIAL — AuditNote: Tagging is rich and useful (`[downtime]`, `[recurrence]`, `[location:]`, etc.) but not standardized to the project's required frontmatter fields.
- Three‑appearance tracking: PARTIAL — AuditNote: Recurrence tags are present; sync these occurrences into `structure/CHARACTER-INTERACTION-SPREADSHEET.md` for automated counting.
- Cross‑links valid: PASS — AuditNote: Internal references and "See also" links resolve to existing structure files.
- Follow‑up scheduled: PASS — AuditNote: Many micro‑scenes include "Later recurrence" notes (good follow‑up strategy). Ensure `limit-break-followup` is used on scenes where cost must be shown later.
- Anchor visibility (head‑hopping): PARTIAL — AuditNote: Micro‑scenes are short and generally manage POV well in summary; ensure full scene files preserve single‑POV rule.

Examples of concrete fixes
- For Scene 22 (Naia): add frontmatter `LimitBreak: true` and `Severity: Severe`; add a one‑line cost anchor in the scene body; create a follow‑up micro‑scene file `story/naia_healer_aftermath.md` tagged `limit-break-followup`.
- For frequently recurring characters (Marta, Thorne, Aldric), create per‑character summary entries in `structure/CHARACTER-INTERACTION-SPREADSHEET.md` and seed their appearance counts.

Recommended next actions
- Split 6–10 high‑value micro‑scenes (including Naia, The Initiation Chamber, The Refugee Camp) into standalone scene files with frontmatter and anchor openers.
- Run an automated pass to flag all scenes in the repo missing required frontmatter and limit‑break tags.
