---
title: Lost & Missing Information Tracker
created: 2026-04-12
purpose: Track information gaps, unresolved references, and orphaned content across the repository
status: Active
---

# Lost & Missing Information Tracker

Central log of unresolved information gaps, broken references, and orphaned content discovered during repository audits.

---

## Duplicate / Conflicting Character Files

| Character | Canonical File | Duplicates to Reconcile | Status |
|-----------|---------------|------------------------|--------|
| **Aisen** | `characters/TIER-PRIMARY/AISEN-profile.md` + `characters/main/aisen-korv.md` | `characters/AISEN-EXPANDED.md` (exact dup of TIER-PRIMARY), `profiles/AISEN-RESTRUCTURED.md`, `duplicates_for_review/characters/AISEN-EXPANDED.md`, `duplicates_for_review/characters/main/aisen-korv.md`, `duplicates_for_review/characters/duplicates-archive/main/AISEN.md`, `duplicates_for_review/characters/duplicates-archive/main/AISEN-CHARACTER-ENHANCEMENT.md` | Needs merge |
| **Kaelen** | `characters/TIER-SECONDARY/KAELEN-BLACKWOOD-profile.md` | `characters/KAELEN-PROFILE-EXPANDED.md`, `duplicates_for_review/characters/allies/kaelen-blackwood.md`, `duplicates_for_review/characters/allies/KAELEN-THORNWOOD.md` | Needs merge |
| **Caspian** | `characters/TIER-PRIMARY/CASPIAN-VANE-profile.md` | `duplicates_for_review/characters/antagonists/CASPIAN-VANE.md`, `duplicates_for_review/characters/CASPIAN-INTEGRATION-GUIDE.md`, `duplicates_for_review/characters/CASPIAN-VANE-THE-ERASURE.md` | Needs merge |
| **Corvin** | `characters/TIER-PRIMARY/CORVIN-ASHFORD-profile.md` | `duplicates_for_review/characters/antagonists/CORVIN-ASHFORD.md`, `duplicates_for_review/characters/antagonists/SER-CORVIN-ASHFORD.md`, `duplicates_for_review/characters/CORVIN-THE-HOLLOW-KNIGHT.md`, `duplicates_for_review/characters/CORVIN-INTEGRATION-GUIDE.md` | Needs merge |

## Conflicting Chapter Versions

| Chapter # | Versions Found | Resolution |
|-----------|---------------|------------|
| **04** | `04-First-Magic-Lesson.md`, `04-Frostfang-Incident.md`, `04-Frostfang-Incident-Expanded.md` | Frostfang variants merged into single canonical `04-Frostfang-Incident.md`; both are valid chapter 4 content alongside `04-First-Magic-Lesson` |
| **05** | `05-Exam-Sabotage.md`, `05-Observation-Game.md` | Build script references Exam-Sabotage; Observation-Game exists but was excluded |
| **30** | `30-Archive-Infiltration.md`, `30-Final-Border-Stand.md`, `30-Final-Border-Stand-Expanded.md` | Border Stand variants merged into `30-Final-Border-Stand.md`; Archive-Infiltration is separate chapter |
| **41-44** | `41-44-War-Operations-Strategic-Escalations.md` + individual `42`, `43`, `44` files | Combined file overlaps individual chapters |

## Missing Metadata (flagged by audits/METADATA-SCAN-REPORT)

Files in `Chapters/` lacking YAML frontmatter:
- `04-Frostfang-Incident.md` — needs frontmatter added
- `04-Frostfang-Incident-Expanded.md` — archived after merge
- `05-Exam-Sabotage.md` — needs frontmatter added
- `30-Final-Border-Stand.md` — needs frontmatter added
- `30-Final-Border-Stand-Expanded.md` — archived after merge
- `Childhood-01-Tavern-At-Night.md` — needs frontmatter added
- `Childhood-02-Beast-Attack.md` — needs frontmatter added
- `Childhood-03-Harald-Gift.md` — needs frontmatter added
- `Childhood-04-Night-Before-Academy.md` — needs frontmatter added
- `Training-Drills-Master-States.md` — reference doc, not a chapter
- `Meta-Copilot-Archive.md` — meta/easter-egg, not a chapter

## Empty / Stub Directories

| Directory | Contents | Action |
|-----------|----------|--------|
| `consistency/` | Only `README.md` | Populate or merge into another folder |
| `culture/` | Only `synthesis-framework.md` | Populate or merge into `worldbuilding/CULTURE/` |

## Naming Issues

| Path | Issue | Suggested Fix |
|------|-------|--------------|
| `full information w/` | Trailing space + special char in folder name | Rename to `full-information` |
| `lost info` | No extension, space in filename | This file (now populated) |
| `reconstruction of the past/` | Spaces in folder name | Rename to `reconstruction-of-the-past` |

## Build Script Issues (BUILD-MANUSCRIPT-FOR-REVIEW.py)

- Array has 54 entries, header/footer claim "52 chapters"
- `05-Observation-Game.md` exists but excluded from build
- `41-44-War-Operations-Strategic-Escalations.md` overlaps individual `42`, `43`, `44` entries
- Two `30-` numbered chapters treated as sequential

---

*Last updated: April 12, 2026*