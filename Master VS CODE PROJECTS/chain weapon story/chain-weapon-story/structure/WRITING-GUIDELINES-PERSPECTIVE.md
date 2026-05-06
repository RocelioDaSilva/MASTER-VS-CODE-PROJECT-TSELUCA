# WRITING GUIDELINES — Perspective & Scene Rules

Purpose
-------
Provide concise, enforceable rules for writing scenes using the interaction‑triggered POV method, micro‑scenes, and limit‑breaking constraints. These guidelines keep head‑hopping, cheap fixes, and inconsistent costs out of drafts.

Core Principle — Interaction‑Triggered POV Anchors
-------------------------------------------------
- Every scene must be anchored to an interaction (dialogue, physical contact, or a deliberate action) that defines the POV focal point for that scene.
- The POV focal character's internal access is allowed; other characters are shown only externally. No head‑hopping inside a scene.
- To shift POV, create a clear scene break and open the new scene with the new anchor's interaction.

Handshake Pattern (author checklist)
----------------------------------
1. Anchor line: open the scene with a short sensory/action line that ties the POV to the interaction (e.g., "When Caspian spoke, Aisen flinched before his arm moved.").
2. Sensory stamp: within the first two paragraphs, include one strong sensory detail tied to the anchor.
3. Internal beat: one internal sentence that reveals POV thought or priority; keep it focused and short.

Three‑Appearance Recurrence Rule
--------------------------------
- Every named non-background character should appear at least three meaningful times across the work: Intro (seed), Complication (stakes/choice), Callback/Payoff (consequence or resolution).
- Use micro‑scenes and tag them to guarantee the three appearances without forcing long expository passages.

Micro‑Scenes: Use & Tags
------------------------
- Purpose: small, repeatable moments (downtime, reveal, motif, skill test, consequence) used to build familiarity and distribute information.
- Recommended tags: `downtime`, `reveal`, `skill-test`, `motif`, `tension`, `limit-break-followup`.
- Placement: aim for at least one micro‑scene per major character per act; micro‑scenes should feel like natural beats (snackable, 150–800 words depending on need).

Limit‑Breaking Scene Constraints
--------------------------------
- Reference: [structure/LIMIT-BREAKING-BACKLASH.md](structure/LIMIT-BREAKING-BACKLASH.md).
- Mandatory for any scene where a character exceeds safe limits:
  - Include a single-line cost anchor in-scene (sensory or functional: e.g., "His left hand stopped answering him.").
  - Add metadata: `LimitBreak: true` and `Severity: Minor|Moderate|Severe|Catastrophic`.
  - Show immediate consequence in the same scene and schedule at least one follow‑up micro‑scene showing narrative impact.
  - Do not allow instant full recovery; any restoration must be expensive and narratively justified.

POV Shift Rules
---------------
- POV shifts are only allowed at scene boundaries and must start with the handshake pattern.
- If an interaction involves multiple potential POV anchors, choose the character whose subjective experience yields the clearest dramatic stakes for the scene.

Metadata / Frontmatter Requirements
----------------------------------
Every scene file must include a minimal frontmatter block with these fields (YAML or simple key/value header):

```yaml
Title: <short title>
SceneID: <unique id>
POV: <character name>
Anchors: <comma-separated character names>
Tags: <comma-separated tags>
LimitBreak: true|false
Severity: Minor|Moderate|Severe|Catastrophic  # required if LimitBreak: true
Chronology: <timeline reference or age>
```

Formatting Examples
-------------------
- Good anchor opener: "When Caspian barked the order, Aisen's arm moved before his mind agreed." — sensory + agency.
- Cost anchor: "He felt the fingers of his right hand go cold and stupid." — single-line signal that must be paid forward.

Verification & QA
-----------------
- Use the `Verification Checklist` (planned file: [structure/VERIFICATION-CHECKLIST.md](structure/VERIFICATION-CHECKLIST.md)) to audit scenes for: anchor presence, metadata completeness, three-appearance tracking, and proper limit‑break tagging.
- For limit‑breaking scenes, run a mandatory follow‑up audit to ensure consequences are visible in subsequent scenes.

Author Notes
------------
- Keep the rules light but enforced: they exist to make stakes real and consequences matter.
- I can scan scenes and auto-flag missing anchors/metadata if you want an automated pass.

Next steps
----------
- Create `structure/VERIFICATION-CHECKLIST.md` and run it on two sample scenes from `story/` or `characters/` to validate these rules.
