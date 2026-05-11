# CONTRIBUTING – Standards & Workflow

This document establishes standards for creating, organizing, and editing files in the Chain Weapon Story project.

---

## File Organization

### Story Files (Primary)

**Location**: `/story/`  
**Format**: `Chapter-XX-Title.md` and `scene-XXX-title.md`

Example:
```
story/Chapter-01-The-Tavern-Opens.md
story/Chapter-02-First-Hunt.md
story/scene-001-tavern-morning.md
story/scene-002-robbers-arrive.md
```

### Character Files

**Master Index**: `characters/CHARACTER-MASTER-INDEX.md`  
**Tier Structure**:
- `characters/TIER-PRIMARY/` – Core protagonists and antagonists
- `characters/TIER-SECONDARY/` – Mentors, major allies, important supporting
- `characters/TIER-ENSEMBLE/` – Special ability holders, minor recurring roles

**Format**: One file per character (no duplicates)  
**Example**: `characters/TIER-PRIMARY/AISEN-profile.md`

### World & System Files

**Location**: `/world/`, `/magic-system/`, `/culture/`, `/ecology/`, `/conflict/`  
**Format**: `TOPIC-GUIDE.md` or `TOPIC-REFERENCE.md`

**Example**:
```
world/HERESY-OF-INFORMATION-SYSTEM.md
magic-system/CHAIN-WEAPON-REFERENCE.md
culture/HEARTLAND-GUIDE.md
ecology/FLUX-SYSTEM-GUIDE.md
```

### Documentation Files

**Change Logs & Reports**: `notes/REPORTS/PROJECT-REPORT-DATE.md`  
**Brainstorming & Experiments**: `notes/BRAINSTORM-TOPIC.md`  
**Legacy Content**: `notes/LEGACY-DOCUMENTS/filename.md`

---

## Required Frontmatter

All story chapters and major system documents must include YAML frontmatter:

```yaml
---
Title: Chapter Title or Document Title
Type: Chapter | Scene | Guide | Reference | Report
Author: Your Name (optional)
Created: YYYY-MM-DD
LastUpdated: YYYY-MM-DD
ChapterID: Chapter-XX or scene-XXX (chapters/scenes only)
POV: Primary Character Name (chapters only)
Act: I | II | III (chapters only)
Chronology: Story timeline reference, e.g., "Aisen age 7, Year 2" (chapters only)
SceneCount: Number of scenes in chapter (chapters only)
WordTarget: 3000-5000 (chapters only)
Status: Not Started | Outline | Draft | Revision | Final
Tags: Comma-separated relevant topics (heresy, combat, magic, mentorship, politics, etc.)
---
```

### Frontmatter Definitions

| Field | Values | Required For |
|-------|--------|--------------|
| **Title** | Any | All story files |
| **Type** | Chapter / Scene / Guide / Reference / Report | All files |
| **POV** | Character name | Chapters only |
| **Act** | I / II / III | Chapters only |
| **Status** | Not Started (0%) \| Outline (10%) \| Draft (90%) \| Revision (100%) \| Final (100%) | All story files |
| **SceneCount** | Numeric | Chapters only |
| **WordTarget** | Numeric range or target | Chapters only |
| **Tags** | Comma-separated list | Story files & guides |

---

## Naming Conventions

### Chapters
```
Chapter-01-The-Tavern-Opens.md
Chapter-02-First-Hunt.md
Chapter-52-Final-Decision.md
```

**Pattern**: `Chapter-[NUMBER]-[Title-In-Title-Case].md`  
**Number**: Always 2 digits (01-52)  
**Title**: Descriptive, hyphen-separated, reflects chapter theme

### Scenes
```
scene-001-tavern-morning.md
scene-042-academy-arrival.md
scene-143-final-battle-begins.md
```

**Pattern**: `scene-[NUMBER]-[title-in-title-case].md`  
**Number**: Always 3 digits (001-999)  
**Title**: Brief, reflects scene focus

### Characters
```
AISEN-profile.md
CASPIAN-VANE-THE-ERASURE.md
HENRIK-GREYSON-mentor.md
SERAPHINE-MOROZ-antagonist.md
```

**Pattern**: `CHARACTER-NAME-descriptor.md` (optional descriptor for clarity)  
**Name**: Full character name in CAPITALS  
**Location**: In appropriate tier folder

### Guides & References
```
HERESY-OF-INFORMATION-SYSTEM.md
CHAIN-WEAPON-REFERENCE.md
HEARTLAND-CULTURE-GUIDE.md
MAGICS-SYSTEM-PHYSICS-PRINCIPLES.md
```

**Pattern**: `TOPIC-TYPE.md`  
**Type**: -GUIDE, -REFERENCE, -SYSTEM, -FRAMEWORK, -DOCUMENT  
**Case**: Title case with hyphens

### Reports & Archives
```
CHAPTER-STATUS-TRACKER.md
PROJECT-COMPLETION-REPORT-2026-04-05.md
CHARACTER-MASTER-INDEX.md
AUDIT-APRIL-2026.md
```

**Pattern**: `TYPE-DATE.md` or `TYPE.md`  
**Date format**: YYYY-MM-DD (if included)

---

## Before Saving/Committing

Checklist for any story chapter added or updated:

- [ ] **Frontmatter complete** – All required fields filled
- [ ] **File location correct** – In `/story/` folder, proper numbering
- [ ] **Naming follows convention** – Chapter-XX or scene-XXX format
- [ ] **Word count realistic** – Matches target range or documented in frontmatter
- [ ] **Character references valid** – All characters mentioned have profiles or are properly introduced
- [ ] **Timeline consistent** – Aisen's age and story chronology match CHAPTER-STATUS-TRACKER
- [ ] **Status updated** – Chapter marked as Draft/Revision/Final (not "Not Started")
- [ ] **Cross-links added** – References to other chapters or character profiles (if applicable)
- [ ] **No duplicates** – Not overwriting existing chapter without intent
- [ ] **Consistency check** – Prose matches story tone; plot aligns with established canon

For character or system files:
- [ ] **Unique** – Not a duplicate of existing profile/guide
- [ ] **Placed in correct folder** – Characters in tier folders, systems in world/magic/etc.
- [ ] **Linked in index** – Added to CHARACTER-MASTER-INDEX or appropriate hub
- [ ] **Cross-referenced** – Links to related files/characters
- [ ] **Front matter complete** – Even system docs should have Type, Status, LastUpdated

---

## Updating CHAPTER-STATUS-TRACKER

When completing a chapter:

1. Open `structure/CHAPTER-STATUS-TRACKER.md`
2. Find your chapter row
3. Update fields:
   - **% Complete**: Increase based on actual progress
   - **Status**: Change to Draft (90%) or Revision/Final (100%)
   - **Notes**: Add brief update (e.g., "First draft complete: 4,200 words")
   - **LastUpdated**: Today's date

Example:
```markdown
| 1 | The Tavern Opens | Aisen | I | 3 | 3,200 | Draft | 90% | 2026-04-05 |
```

---

## Referencing Other Files

Use relative markdown links to other project files:

```markdown
See [Caspian's profile](../characters/TIER-PRIMARY/CASPIAN-VANE-THE-ERASURE.md)
For telekinesis rules, see [magic-system guide](../magic-system/CHAIN-WEAPON-REFERENCE.md)
Check [story overview](../story-overview.md) for character timeline
```

**Pattern**: `[Display Text](relative/path/to/file.md)`

---

## Git Commit Messages

When committing chapter or character changes, use clear commit messages:

```
Write Chapter-01 (First Draft) - Tavern scene complete, 3200 words
Update Caspian profile - Added erasure arc details
Add CHARACTER-MASTER-INDEX - Organized 50+ characters by tier
```

**Format**: `[Action] Filename - Brief description (word count if applicable)`

---

## Contact & Questions

If unclear about:
- **Where a file should go** → Check character tier structure or system folder organization
- **How to name something** → Follow the naming convention patterns above
- **What frontmatter to use** → Copy the template from an existing similar file
- **Chapter numbering/progress** → Check CHAPTER-STATUS-TRACKER.md

---

---

## Developer Tools & Local Checks

To help contributors keep the repository consistent, we provide lightweight developer checks.

- Install development tools:

```
python -m pip install -r requirements-dev.txt
```

- Run front-matter validation (manuscript and story folders are recommended):

```
python scripts/check_front_matter.py --path manuscript
python scripts/check_front_matter.py --path story
```

- Run code formatter check (Black) and lint (Flake8):

```
black --check .
flake8 --max-line-length=88
```

These checks are run on CI for pull requests. If your PR fails the formatting checks, run `black .` locally, re-run `flake8` to review any remaining issues, and then commit the formatted code.

Last Updated: 2026-04-05
