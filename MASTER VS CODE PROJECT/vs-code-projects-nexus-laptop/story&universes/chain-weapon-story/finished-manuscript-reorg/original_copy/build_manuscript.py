#!/usr/bin/env python3
"""
Generate integrated book manuscript with per-chapter landscape/character configuration.

Reads:
  - chapter-config.json: mapping of chapters to characters, landscapes, locations
  - cwbook_minimal_package/chapterXX.tex: chapter content files

Outputs:
  - manuscript-final.tex: complete book with headers, footers, glyphs, stripes

Usage:
  python3 build_manuscript.py
"""

import json
import os
from pathlib import Path
import re

# Paths
CONFIG_FILE = "chapter-config.json"
CHAPTERS_DIR = "cwbook_minimal_package"
TEMPLATE_FILE = "manuscript-integrated.tex"
OUTPUT_FILE = "manuscript-final.tex"
AUXILIARY_EXTENSIONS = (".aux", ".log", ".toc", ".out", ".lof", ".lot")
LEGACY_CHAPTER_WRAPPER_PATTERNS = (
    re.compile(r"^\s*\\chapter\{.*?\}\s*$", re.MULTILINE),
    re.compile(r"^\s*\\renewcommand\{\\CurrentChapterNum\}\{.*?\}\s*$", re.MULTILINE),
    re.compile(r"^\s*\\POV\{.*?\}\{.*?\}\s*$", re.MULTILINE),
)

def load_config(filename):
    """Load chapter configuration from JSON."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_chapter_content(chapter_num):
    """Load chapter content from chapterXX.tex file."""
    chapter_file = Path(CHAPTERS_DIR) / f"chapter{chapter_num:02d}.tex"
    if chapter_file.exists():
        with open(chapter_file, 'r', encoding='utf-8') as f:
            return sanitize_chapter_content(f.read())
    return None

def sanitize_chapter_content(content):
    """Strip legacy per-chapter wrapper commands that conflict with the master template."""
    sanitized = content

    for pattern in LEGACY_CHAPTER_WRAPPER_PATTERNS:
        sanitized = pattern.sub("", sanitized)

    return sanitized.strip()

def clear_stale_build_artifacts(output_filename):
    """Remove auxiliary files that can break a fresh compile after template changes."""
    removed_files = []
    output_path = Path(output_filename)

    for suffix in AUXILIARY_EXTENSIONS:
        artifact_path = output_path.with_suffix(suffix)
        if artifact_path.exists():
            artifact_path.unlink()
            removed_files.append(artifact_path.name)

    return removed_files

def generate_chapter_block(chapter_info):
    """Generate LaTeX block for a single chapter."""
    num = chapter_info['num']
    label = chapter_info['label']
    title = chapter_info['title']
    character = chapter_info['character']
    landscape = chapter_info['landscape']
    location = chapter_info['location']
    
    # Load chapter content
    content = load_chapter_content(num)
    if not content:
        # Placeholder if file doesn't exist
        content = f"% [Content for {title} not found]"
    
    block = f"""% ═══════════════════════════════════════════════════════════════════════════
% CHAPTER {label}  —  {character} POV, {landscape}
% ═══════════════════════════════════════════════════════════════════════════

\\renewcommand{{\\CurrentChapterNum}}{{{num}}}
\\renewcommand{{\\CurrentChapterLabel}}{{{label}}}
\\renewcommand{{\\ActiveCharacter}}{{{character}}}
\\renewcommand{{\\ActiveLandscape}}{{{landscape}}}
\\renewcommand{{\\SceneLocation}}{{{location}}}
\\renewcommand{{\\POVGlyphName}}{{{character}}}
\\renewcommand{{\\POVColor}}{{Col{character}}}

\\BookChapter{{\\CurrentChapterLabel}}{{{title}}}

{content}

\\newpage
"""
    return block

def generate_manuscript(config):
    """Generate complete manuscript."""
    # Read the template (preamble up to \begin{document})
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Split at \begin{document}
    preamble_end = template.find("\\begin{document}")
    if preamble_end == -1:
        print("ERROR: Could not find \\begin{document} in template")
        return
    
    preamble = template[:preamble_end + len("\\begin{document}")]
    
    # Generate all chapter blocks
    chapters_content = ""
    for chapter_info in config['chapters']:
        chapters_content += generate_chapter_block(chapter_info)
        print(f"✓ Generated chapter {chapter_info['num']:02d}: {chapter_info['title']}")
    
    # Footer
    footer = """
\\end{document}
"""
    
    # Assemble final manuscript
    final = preamble + "\n\n" + chapters_content + footer
    
    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final)

    removed_files = clear_stale_build_artifacts(OUTPUT_FILE)
    
    print(f"\n✓ Manuscript generated: {OUTPUT_FILE}")
    print(f"  Total chapters: {len(config['chapters'])}")
    print(f"  Compile with: xelatex {OUTPUT_FILE} (run twice)")
    if removed_files:
        print(f"  Cleared stale build artifacts: {', '.join(removed_files)}")

if __name__ == "__main__":
    print("Building integrated manuscript...")
    config = load_config(CONFIG_FILE)
    generate_manuscript(config)
    print("\nDone!")
