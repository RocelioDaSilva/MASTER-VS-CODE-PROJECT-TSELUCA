# Repo-wide Audit: Characters, Arcs, and Worldbuilding

Snapshot: pre-audit commit `68df401` created (message: "pre-audit: snapshot").

Scope & method
- Scanned canonical indexes: [characters/CHARACTER-INDEX.md](characters/CHARACTER-INDEX.md), [characters/CHARACTER-BIBLE.md](characters/CHARACTER-BIBLE.md)
- Scanned arcs: `Arcs/` and `Arcs/Character-Arcs/`
- Scanned story chapters: `story/`, `Chapters/`
- Scanned world docs: `world/`, `magic-system/`, `timelines/`
- Used automated searches for name variants, front-matter/timeline flags, and duplicate files.

Summary findings (high priority)

1) Canonical name inconsistencies (high)
- `Rin` appears under multiple canonical names and files:
  - [characters/allies/rin-celestara.md](characters/allies/rin-celestara.md)
  - [characters/allies/RIN-SHIRAKAWA.md](characters/allies/RIN-SHIRAKAWA.md)
  - `CHARACTER-BIBLE.md` lists `Rin Shirakawa` ([characters/CHARACTER-BIBLE.md](characters/CHARACTER-BIBLE.md)).
  Action: pick one canonical surname and merge duplicates (recommend: `Rin Shirakawa` appears more in notes; confirm before change).

- `Kaelen` appears as `Kaelen Blackwood` and `Kaelen Thornwood`:
  - [characters/allies/kaelen-blackwood.md](characters/allies/kaelen-blackwood.md)
  - [characters/allies/KAELEN-THORNWOOD.md](characters/allies/KAELEN-THORNWOOD.md)
  Action: canonicalize to one surname (notes and world/refs predominantly use `Thornwood`).

- `Aisen` surname mismatch:
  - Index uses `Aisen Korv` ([characters/CHARACTER-INDEX.md](characters/CHARACTER-INDEX.md)) and file exists at [characters/main/aisen-korv.md](characters/main/aisen-korv.md)
  - `CHARACTER-BIBLE.md` describes Aisen as no-surname in some passages.
  Action: choose canonical form (suggest keep `Aisen Korv` because file exists and many chapters reference `Aisen Korv`).

2) Duplicate / conflicting character files (medium)
- Multiple profile files with overlapping content (e.g., `rin-celestara.md` vs `RIN-SHIRAKAWA.md`, `kaelen-blackwood.md` vs `KAELEN-THORNWOOD.md`).
- These duplicates increase risk of divergence and inconsistent updates.
  Action: consolidate duplicates into single canonical files and add redirect notes or symlink-style references.

3) Timeline / age mismatches (medium)
- `CHARACTER-BIBLE.md` sometimes lists Aisen final year as age 23; timelines file [timelines/NORMALIZED-AGES.csv](timelines/NORMALIZED-AGES.csv) and the chapter front-matter normalize Aisen to age 24 at Chapter-44.
  Example files:
  - [characters/CHARACTER-BIBLE.md](characters/CHARACTER-BIBLE.md)
  - [timelines/NORMALIZED-AGES.csv](timelines/NORMALIZED-AGES.csv)
  Action: decide canonical age mapping (I recommend normalizing to ages in `timelines/NORMALIZED-AGES.csv` then updating character docs to match).

4) Chapter front-matter / metadata flags (low→medium)
- Some chapters have missing or indeterminate front-matter values (e.g., `POV`, `Age`). Example: [story/Chapter-43-Varros-Fragmented-Truth.md](story/Chapter-43-Varros-Fragmented-Truth.md) has `Age: Indeterminate` and was flagged in timelines.
- Audits recommend adding `POV`, `Age`, and `ChapterID` front-matter consistently to all story files.
  Action: populate front-matter for flagged chapter files (can be automated for obvious cases; ambiguous cases flagged for author review).

5) Worldbuilding coverage (observations)
- Core world docs exist in `world/` and include definitions for Thornwood Hollow and Covenant mechanics (e.g., [world/HERESY-OF-INFORMATION-SYSTEM.md](world/HERESY-OF-INFORMATION-SYSTEM.md)).
- Recommendation: create a small canonical `world/INDEX.md` (already exists) and add explicit entries for any frequently referenced micro-locations (Thornwood Hollow, Academy campuses) to reduce scattered definitions.

6) Voice & attribute divergence (style/inconsistency)
- A few characters have slightly differing physical/voice attributes across files (e.g., Kaelen surname + motif wording differences). These are stylistic but important to unify before edits.
  Action: after canonicalizing names, run a substitution pass to align physical traits and voice notes across character files.

Automated checks performed (examples)
- Name-variant grep for `Rin`, `Kaelen`, `Aisen`, `Caspian` across repo
- Scanned `Arcs/Character-Arcs/` for per-character NOTES files
- Checked `timelines/` CSVs for `Indeterminate` or `Variable` age flags

Quick actionable prioritised list
1. Confirm canonical names for conflicting characters: `Rin`, `Kaelen`, `Aisen` (I can apply merges if you approve).  
2. Consolidate duplicate character files into canonical filenames and update inbound references.  
3. Normalize ages using `timelines/NORMALIZED-AGES.csv`, update character docs to match.  
4. Add missing front-matter to chapters flagged in [audits/PRE-ACADEMY-TIMELINE-audit.md](audits/PRE-ACADEMY-TIMELINE-audit.md) and `timelines/AGES-CHECK.csv`.  
5. Commit changes and run a second pass audit to verify no new inconsistencies.

Files created by this audit
- [audits/REPO-WIDE-CHARACTER-ARC-WORLDBUILDING-AUDIT.md](audits/REPO-WIDE-CHARACTER-ARC-WORLDBUILDING-AUDIT.md) (this file)

Next steps I can take (choose one):
- I can canonicalize names and merge duplicate files automatically (I will commit the changes and provide a follow-up audit).  
- I can prepare a detailed list of exact file edits needed for you to review before committing.  
- Or, if you prefer, I can only add metadata fixes to chapter front-matter and commit those changes first.

If you want me to proceed with automated fixes, tell me which of the canonical choices you prefer (e.g., `Rin Shirakawa` vs `Rin Celestara`, `Kaelen Thornwood` vs `Kaelen Blackwood`, `Aisen Korv` vs `Aisen (no surname)`).


----
Audit generated: 2026-04-05
