#!/usr/bin/env python3
"""
rebuild_chapters.py — Regenerate all chapter .tex files from current manuscript markdown.

Reads:
  - chapter-config-105.json: chapter metadata (source_file, num, character, landscape, location)
  - manuscript/Chapters/*.md: current chapter markdown files
  - manuscript/Chapters/archives/*.md: fallback for archived chapters

Outputs:
  - cwbook_minimal_package/chapter001.tex through chapter105.tex

Usage:
  python rebuild_chapters.py
"""

import json
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "chapter-config-105.json"
CHAPTERS_DIR = REPO_ROOT / "manuscript" / "Chapters"
ARCHIVES_DIR = CHAPTERS_DIR / "archives"
OUTPUT_DIR = SCRIPT_DIR / "cwbook_minimal_package"

# LaTeX special characters that need escaping
LATEX_ESCAPES = [
    ('\\', r'\textbackslash{}'),
    ('&', r'\&'),
    ('%', r'\%'),
    ('$', r'\$'),
    ('#', r'\#'),
    ('_', r'\_'),
    ('{', r'\{'),
    ('}', r'\}'),
    ('~', r'\textasciitilde{}'),
    ('^', r'\textasciicircum{}'),
]


def load_config():
    """Load chapter configuration."""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_source_file(source_name):
    """Find the markdown source file, checking main dir then archives."""
    main_path = CHAPTERS_DIR / f"{source_name}.md"
    if main_path.exists():
        return main_path
    archive_path = ARCHIVES_DIR / f"{source_name}.md"
    if archive_path.exists():
        return archive_path
    # Also check for -SUPERSEDED suffix in archives
    for suffix in ['-SUPERSEDED', '-Expanded']:
        alt_path = ARCHIVES_DIR / f"{source_name}{suffix}.md"
        if alt_path.exists():
            return alt_path
    return None


def strip_frontmatter(text):
    """Remove YAML frontmatter from markdown."""
    text = text.strip()
    if text.startswith('---'):
        parts = text.split('\n---\n', 1)
        if len(parts) == 2:
            return parts[1].lstrip()
        # Try splitting on just '---' on its own line
        lines = text.splitlines()
        if len(lines) > 1:
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break
            if end_idx is not None:
                return '\n'.join(lines[end_idx + 1:]).lstrip()
    return text


def strip_banners_and_notes(text):
    """Remove blockquote banners and chapter notes sections."""
    # Strip leading blockquote lines (warning banners)
    lines = text.splitlines()
    i = 0
    while i < len(lines) and (lines[i].startswith('>') or lines[i].strip() == ''):
        i += 1
    text = '\n'.join(lines[i:]).lstrip()

    # Strip trailing chapter notes
    text = re.sub(r'\n---\n+## CHAPTER NOTES[\s\S]*$', '', text)
    text = re.sub(r'\n---\n+## Chapter Notes[\s\S]*$', '', text, flags=re.IGNORECASE)

    return text.strip()


def escape_latex(text):
    """Escape LaTeX special characters in running text."""
    # Don't escape backslashes that are already LaTeX commands
    # Process carefully to avoid double-escaping
    result = text

    # First, protect existing LaTeX-like commands by replacing them temporarily
    # We'll handle & % $ # _ ~ ^ which are the common markdown chars that need escaping
    result = result.replace('&', r'\&')
    result = result.replace('%', r'\%')
    result = result.replace('$', r'\$')
    result = result.replace('#', r'\#')
    # Don't escape underscores inside words (common in markdown filenames etc.)
    # But do escape bare ones
    result = result.replace('_', r'\_')

    return result


def md_to_latex(text):
    """Convert markdown text to LaTeX."""
    # Remove any remaining YAML dividers
    text = re.sub(r'(?m)^---\s*$', '', text)

    # Remove "END CHAPTER XX" markers
    text = re.sub(r'(?m)^[-—*\s]*END\s+CHAPTER\s+\d+\S*\s*[-—*]*\s*$', '', text, flags=re.IGNORECASE)

    # Convert markdown headings
    # ### subheading → \medskip\noindent\textbf{...}
    text = re.sub(r'(?m)^#{3,}\s+(.+)$', r'\\medskip\\noindent\\textbf{\1}\\medskip', text)
    # ## scene break heading → \SceneBreak + bold
    text = re.sub(r'(?m)^#{2}\s+(.+)$', r'\\SceneBreak\n\\noindent\\textbf{\1}\\medskip', text)
    # # chapter heading → remove (handled by BookChapter command)
    text = re.sub(r'(?m)^#{1}\s+.*$', '', text)

    # Scene break markers (*** or --- or ___ on their own line)
    text = re.sub(r'(?m)^\s*[*_-]{3,}\s*$', r'\\SceneBreak', text)

    # Bold **text** → \textbf{text}
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text, flags=re.DOTALL)

    # Italic *text* → \emph{text} (but not ** which is bold)
    text = re.sub(r'(?<!\*)\*(?!\*)([^\*\n]+?)\*(?!\*)', r'\\emph{\1}', text)

    # Links [text](url) → just text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Images ![alt](url) → remove
    text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text)

    # Escape LaTeX special characters (after markdown processing)
    # Only escape & and % which are common in prose
    # Don't escape _ since we already handled it in markdown conversion
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')

    # Em dashes: --- → —
    text = text.replace('---', '---')  # LaTeX handles --- as em dash natively

    # En dashes: -- (already handled by LaTeX)

    # Smart quotes: LaTeX handles these with fontspec

    # Clean up multiple blank lines → double newline (paragraph break)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def process_chapter(chapter_info):
    """Convert a single chapter from markdown to LaTeX."""
    source_name = chapter_info['source_file']
    num = chapter_info['num']
    character = chapter_info.get('character', 'Aisen')
    landscape = chapter_info.get('landscape', 'Mountains')
    location = chapter_info.get('location', '')

    # Find source file
    source_path = find_source_file(source_name)
    if source_path is None:
        print(f"  [{num:3d}/105] WARNING: source not found: {source_name}")
        return f"% Source not found: {source_name}\n\n[Chapter content missing]\n"

    # Read markdown
    with open(source_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Clean up
    text = strip_frontmatter(raw_text)
    text = strip_banners_and_notes(text)

    # Convert to LaTeX
    tex_content = md_to_latex(text)

    # Add header comment
    header = (
        f"% Auto-generated from {source_name}.md\n"
        f"% POV: {chapter_info.get('pov_name', character)} | "
        f"Landscape: {landscape} | Location: {location}\n\n"
    )

    print(f"  [{num:3d}/105] {source_name} ✓")
    return header + tex_content + "\n"


def main():
    print("🔨 Rebuilding chapter .tex files from current manuscript markdown...")
    print()

    config = load_config()
    chapters = config['chapters']

    print(f"📖 Processing {len(chapters)} chapters...")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for chapter_info in chapters:
        num = chapter_info['num']
        tex_content = process_chapter(chapter_info)

        # Write output file (3-digit numbering)
        output_path = OUTPUT_DIR / f"chapter{num:03d}.tex"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)

    print()
    print(f"✅ Generated {len(chapters)} chapter .tex files in {OUTPUT_DIR.name}/")
    print()
    print("Next steps:")
    print(f"  cd finished-manuscript")
    print(f"  xelatex manuscript-integrated-105.tex")
    print(f"  xelatex manuscript-integrated-105.tex   (second pass for TOC/refs)")


if __name__ == '__main__':
    main()
