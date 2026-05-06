#!/usr/bin/env python3
"""
Build complete manuscript for friends' review.
Combines all chapters in order into a single formatted document.
Outputs as:
  1. manuscript-review.txt (plain text, easy to share)
  2. manuscript-review.md (markdown, formatted)
"""

import os
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent
CHAPTERS_DIR = REPO_ROOT / "manuscript" / "Chapters"

# Chapter order — canonical sequence
# Note: Some chapter numbers share a slot (e.g. 04 has two sub-chapters,
# 30 has two entries). The combined 41-44 file is used instead of individual
# 42/43/44 files to avoid duplication.
CHAPTERS = [
    "01-Tavern-Opening",
    "02-Training-Years-Begin",
    "03-City-Beneath",
    "04-First-Magic-Lesson",
    "04-Frostfang-Incident",
    "05-Exam-Sabotage",
    "05-Observation-Game",
    "06-First-Contact",
    "07-Network-Test",
    "08-Covenant-Scholar",
    "09-Final-Warning",
    "10-Last-Ordinary-Day",
    "11-Academy-Initiation",
    "12-First-Operations",
    "13-The-Archive-Access",
    "14-The-Competitor-Networks",
    "14B-The-Provincial-Cost",
    "15-The-Heresy-Archive",
    "15B-The-Patient-Grower",
    "16-The-Database-Infiltration",
    "17-Examination-Crisis",
    "17B-The-Load-Bearing-Wall",
    "18-The-Military-Assignment",
    "19-Military-Training-Initiate",
    "19B-Institutional-Gravity",
    "20-The-Threshold",
    "20B-The-Two-Masks",
    "21-Academy-Arrival",
    "21B-The-Pattern-in-the-Noise",
    "22-Covenant-Marking",
    "22B-The-Public-Hearing",
    "23-Heresy-and-Power",
    "24-Chain-Spear-Mastery",
    "25-Amara-Positioning",
    "26-Network-Expands",
    "26B-Village-Aftermath",
    "27-Academy-Conflict",
    "28-Network-Consolidation",
    "29-The-Final-Planning",
    "29B-The-Blockade",
    "30-Archive-Infiltration",
    "30-Final-Border-Stand",
    "31-Deployment-Begins",
    "31B-Force-Geometry",
    "32-Evidence-Distribution",
    "33-The-Investigation-Deepens",
    "33B-The-Ultimatum-Letter",
    "34-The-Extraction",
    "34B-The-Ghost-Agent",
    "35-Military-Campaign-Escalation",
    "36-Conscription",
    "37-Covenant-Confrontation",
    "38-Deliberation",
    "38B-The-Weight-of-Command",
    "39-Regional-Conflict",
    "39B-Architecture-of-Absence",
    "40-Contact-Point",
    "41-Transition-Decision",
    "42-Institutional-Replacement",
    "43-Network-Reorganization",
    "44-Convergence",
    # ACT III: WAR, SACRIFICE & RECONSTRUCTION (Ch 45-85)
    "45-HQ-Assault",
    "45B-The-Language-of-Roots",
    # "46-Aisen-Death",  # SUPERSEDED — canonical death is Ch 70
    "47-The-Merchants-War",
    "47B-First-Contact",
    # "48-Immediate-Aftermath",  # OLD DRAFT — orphaned post-death arc, replaced by Ch 71-85
    "48B-The-Crowns-Gambit",
    # "49-New-Governance",  # OLD DRAFT — orphaned, replaced by Ch 76-80
    # "50-Without-Center",  # OLD DRAFT — orphaned, replaced by Ch 71-85
    # "51-Reconstruction",  # OLD DRAFT — orphaned, replaced by Ch 78
    # "52-Final-Epilogue",  # OLD DRAFT — orphaned, replaced by Ch 82-85
    "53-Varros-Gambit",
    "54-The-Sanctuary-Falls",
    "55-The-Network-Bleeds",
    "55B-Kaels-Collapse",
    "56-The-Covenant-Schism",
    "56B-The-Blueprint-of-Destruction",
    "57-Caspians-Choice",
    "58-The-Provincial-Atrocity",
    "58B-The-Document-That-Burns",
    "59-The-Alliance-Negotiation",
    "60-Corvins-Bridge",
    "61-The-Crown-Falls",
    "62-The-Spy-Exposed",
    "63-Three-Funerals",
    "64-Aisens-Realization",
    "64B-The-Princess-Burns",
    "65-Pre-Assault-Planning",
    "65B-The-Last-Geometry",
    "66-The-Burning-Forest",
    "67-The-HQ-Approach",
    "68-The-Assault-First-Wave",
    "68B-The-Building-Speaks",
    "69-Seraphine-Confrontation",
    "70-Aisens-Final-Stand",
    "71-The-Silence-After",
    "72-The-Record",
    "73-The-Last-Report",
    "74-The-Network-Holds",
    "75-Breaking-Point",
    "76-The-Moderate-Peace",
    "77-The-Serath-Doctrine",
    "78-Reconstruction",
    "79-The-Garden",
    "80-New-Governance-Year-One",
    "81-Caspians-Freedom",
    "82-Five-Years-Later",
    "83-Kaels-Pocket",
    "84-The-History",
    "85-Final-Coda-The-Ordinary-Foundation",
]

def load_chapter(chapter_name):
    """Load chapter from Chapters/ folder."""
    chapter_path = CHAPTERS_DIR / f"{chapter_name}.md"
    if chapter_path.exists():
        with open(chapter_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        return clean_chapter_text(raw_text)
    else:
        return f"[ERROR: Chapter file not found: {chapter_name}.md]\n\n"


def clean_chapter_text(raw_text):
    """Strip chapter frontmatter and author-note sections from manuscript output."""
    cleaned = raw_text.strip()

    if cleaned.startswith("---"):
        parts = cleaned.split("\n---\n", 1)
        if len(parts) == 2:
            cleaned = parts[1].lstrip()

    # Strip any leading blockquote warning banners (lines starting with "> ⚠" or "> **⚠")
    lines = cleaned.splitlines()
    i = 0
    while i < len(lines) and (lines[i].startswith(">") or lines[i].strip() == ""):
        i += 1
    cleaned = "\n".join(lines[i:]).lstrip()

    cleaned = re.sub(r"\n---\n+## CHAPTER NOTES[\s\S]*$", "", cleaned)
    return cleaned.strip()

def build_manuscript():
    """Build complete manuscript from all chapters."""
    
    print("🔨 Building manuscript for review...")
    print(f"📖 Processing {len(CHAPTERS)} chapters...")
    
    # Header
    header = f"""# Chain Weapon Story — Complete Manuscript
## For Friend Review

**Built:** {datetime.now().strftime('%B %d, %Y at %H:%M')}  
**Status:** {len(CHAPTERS)} Chapters, Revised Draft (April 2026)  
**Word Count:** ~300,000 words  
**Revision:** 85-chapter expansion — full kaleidoscopic POV system applied

---

## Before You Read

This manuscript represents the complete first draft of a dark fantasy about an ordinary protagonist using a chain spear and strategic telekinesis to survive in a world filled with prodigies and conspiracies. 

**Key themes:**
- No plot armor or destiny—only learning and luck
- Ordinary people matter more than legends
- Consequences are permanent and real
- The world continues after the protagonist's death

---

## MANUSCRIPT BEGINS

"""
    
    # Content
    content = header
    
    for i, chapter_name in enumerate(CHAPTERS, 1):
        print(f"  [{i:2d}/{len(CHAPTERS)}] Loading {chapter_name}...", end=" ")
        chapter_content = load_chapter(chapter_name)
        
        # Add chapter number if not already in file
        if not chapter_content.strip().startswith("#"):
            content += f"\n## Chapter {i}\n\n"
        
        content += chapter_content + "\n\n---\n\n"
        print("✓")
    
    # Footer
    footer = f"""---

## Manuscript Complete

**Total Chapters:** {len(CHAPTERS)}  
**Status:** First Draft Complete (April 8, 2026)  
**Built for Review:** {datetime.now().strftime('%B %d, %Y')}

All feedback, corrections, and suggestions welcome.

---

*Thank you for reading.*
"""
    
    content += footer
    
    # Write markdown version
    output_md = Path("manuscript-review.md")
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✓ Wrote {output_md} ({len(content):,} characters)")
    
    # Write plain text version (strip markdown)
    text_content = content.replace("# ", "").replace("## ", "").replace("**", "").replace("_", "")
    output_txt = Path("manuscript-review.txt")
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text_content)
    print(f"✓ Wrote {output_txt} ({len(text_content):,} characters)")
    
    print("\n✅ Manuscript built successfully!")
    print(f"\nTo share with friends:")
    print(f"  - markdown version: manuscript-review.md")
    print(f"  - plain text version: manuscript-review.txt")
    print(f"\nFile sizes:")
    print(f"  - {output_md.name}: {output_md.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"  - {output_txt.name}: {output_txt.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    build_manuscript()
