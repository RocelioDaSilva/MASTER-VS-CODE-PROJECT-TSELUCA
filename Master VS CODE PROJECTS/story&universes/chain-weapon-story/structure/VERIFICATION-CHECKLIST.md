# VERIFICATION CHECKLIST — Scene & Continuity QA

Purpose
-------
Run a quick, repeatable audit on scene files and micro‑scenes to ensure adherence to the project's writing rules (anchors, POV, metadata, limit‑breaking tags, and follow‑ups).

How to run
----------
1. Open the target scene file.
2. Run each check below and mark `PASS` or `FLAG`.
3. Record a short `AuditNote:` for each flagged item.
4. Save the audit results in the `audits/` folder as `<SceneID>-audit.md`.

Checklist
---------
- Frontmatter present: `Title`, `SceneID`, `POV`, `Anchors`, `Tags`, `LimitBreak` (if true then `Severity` required), `Chronology`.
- Anchor opener: Scene begins with a clear interaction anchor within the first two paragraphs (dialogue, physical contact, or decisive action naming characters).
- POV match: The `POV` value corresponds to the anchor character and internal beats are only from that POV.
- LimitBreak tagging: If the body includes limit‑breaking language (words: `weave`, `rending`, `limit-break`, `push beyond`, `overload`, `blood bargain`, `soul-anchor`), then `LimitBreak: true` and `Severity` are present.
- Cost anchor line: If `LimitBreak: true`, a single-line sensory/functional signal must appear (e.g., "His left hand stopped answering him.").
- Metadata completeness: `Tags` includes at least one micro‑scene tag (`downtime`, `reveal`, `skill-test`, `motif`, `tension`, `limit-break-followup`).
- Three‑appearance tracking: For every named supporting character in scene, confirm entry exists in the Character Interaction spreadsheet and increment their appearance counter.
- Cross‑links valid: Any referenced files (characters, previous scenes) exist at the given relative path.
- Follow‑up scheduled: If `LimitBreak: true`, confirm at least one micro‑scene or later scene is tagged to show impact.
- Anchor visibility: No head‑hopping within scene — other characters' internal thoughts are not presented.

Audit Template (paste at top of audit file)
-----------------------------------------
Scene: <SceneID>
File: <path>
POV: <character>
CheckedBy: <name/date>

- Frontmatter: PASS/FLAG — AuditNote:
- Anchor opener: PASS/FLAG — AuditNote:
- POV match: PASS/FLAG — AuditNote:
- LimitBreak tagging: PASS/FLAG — AuditNote:
- Cost anchor line: PASS/FLAG — AuditNote:
- Metadata completeness: PASS/FLAG — AuditNote:
- Three‑appearance tracking: PASS/FLAG — AuditNote:
- Cross‑links valid: PASS/FLAG — AuditNote:
- Follow‑up scheduled: PASS/FLAG — AuditNote:
- Anchor visibility: PASS/FLAG — AuditNote:

Minimal follow-up actions (examples)
-----------------------------------
- Add frontmatter block with required fields.
- Insert a one‑line anchor opener within the first paragraph.
- Tag LimitBreak: true and set Severity where appropriate.
- Create a micro‑scene file to hold the follow‑up and tag it `limit-break-followup`.

Automation notes
----------------
- I can run an automated pass to detect missing frontmatter, presence of key limit‑break keywords, and whether referenced files exist. If you want, I can perform that automated pass across the repo and output a CSV of flags.

Next step
---------
- Use this checklist to audit two sample scenes. Save audits under `audits/` and report back for fixes.
