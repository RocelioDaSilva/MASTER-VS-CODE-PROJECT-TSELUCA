#!/usr/bin/env python3
"""
convert_md_to_tex.py
Simple converter: turn Markdown chapter files into LaTeX chapter files for cwbook_minimal_package.
Run from the workspace root (finished-manuscript).
"""
import os
import re

WORKSPACE = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(WORKSPACE, 'manuscriptbaseforchapters')
OUTPUT_DIR = os.path.join(WORKSPACE, 'cwbook_minimal_package')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map POV names to glyph macros defined in cwbook_minimal.cls
GLYPH_MAP = {
    'Aisen': '\\glyphAisen',
    'Caspian': '\\glyphCaspian',
    'Corvin': '\\glyphCorvin',
    'Ryo': '\\glyphRyo',
    'Kael': '\\glyphKael',
    'Kairos': '\\glyphKairos',
    'Orin': '\\glyphOrin',
    'Amara': '\\glyphAmara',
    'Renard': '\\glyphRenard',
}

MD_FILES = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.md')])

def sanitize_title(t: str) -> str:
    pairs = [('\\','\\textbackslash{}'),('&','\\&'),('%','\\%'),('$','\\$'),('#','\\#'),('_','\\_'),('{','\\{'),('}','\\}'),('~','\\textasciitilde{}'),('^','\\textasciicircum{}')]
    for a,b in pairs:
        t = t.replace(a,b)
    return t


def md_to_latex(s: str) -> str:
    # remove any YAML-like divider lines used elsewhere
    s = re.sub(r'(?m)^---\s*$', '', s)
    # markdown headings: # Title -> remove (chapter already set), ## -> \scenebreak + bold, ### -> bold
    s = re.sub(r'(?m)^#{1}\s+CHAPTER\s+\d+.*$', '', s)  # remove "# CHAPTER XX: ..." lines
    s = re.sub(r'(?m)^#{3,}\s+(.+)$', r'\\medskip\\noindent\\textbf{\1}\\medskip', s)
    s = re.sub(r'(?m)^#{2}\s+(.+)$', r'\\scenebreak\n\\noindent\\textbf{\1}\\medskip', s)
    s = re.sub(r'(?m)^#{1}\s+(.+)$', r'\\bigskip\\noindent{\\Large\\bfseries \1}\\bigskip', s)
    # bold **text** -> \textbf{text}
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s, flags=re.DOTALL)
    # italic *text* -> \emph{text}
    s = re.sub(r'(?<!\\)\*(?!\\)([^\*\n]+?)\*(?!\\)', r'\\emph{\1}', s)
    # links [text](url) -> text
    s = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', s)
    # images ![alt](url) -> remove
    s = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', s)
    # escape percent, underscores, and hash signs
    s = s.replace('%', '\\%').replace('_', '\\_').replace('#', '\\#')
    return s

for md in MD_FILES:
    mdpath = os.path.join(INPUT_DIR, md)
    with open(mdpath, 'r', encoding='utf-8') as fh:
        text = fh.read()

    # parse frontmatter
    title = None
    pov = None
    chapter_id = None

    lines = text.splitlines()
    if len(lines) == 0:
        continue

    # if file starts with YAML frontmatter
    if lines[0].strip() == '---':
        # find closing '---'
        try:
            end_idx = lines.index('---', 1)
        except ValueError:
            end_idx = None
        if end_idx is not None:
            meta_lines = lines[1:end_idx]
            content_lines = lines[end_idx+1:]
            for L in meta_lines:
                if ':' in L:
                    k,v = L.split(':',1)
                    k = k.strip()
                    v = v.strip().strip('"')
                    if k.lower() == 'title':
                        title = v
                    elif k.lower() == 'pov':
                        pov = v
                    elif k.lower() == 'chapterid':
                        chapter_id = v
        else:
            # no closing marker; treat whole file as content
            content_lines = lines
    else:
        content_lines = lines

    # if there is a trailing '---' separating notes, cut at first such occurrence
    try:
        trailing = content_lines.index('---')
        content_body_lines = content_lines[:trailing]
    except ValueError:
        content_body_lines = content_lines

    content_body = '\n'.join(content_body_lines).strip()

    # fallback title from filename
    if not title:
        # remove leading 'Chapter-XX-' if present
        m = re.match(r'Chapter-(\d+)-(.*)\\.md', md, flags=re.IGNORECASE)
        if m:
            title = m.group(2).replace('-', ' ')
        else:
            title = os.path.splitext(md)[0].replace('-', ' ')

    if not pov:
        pov = ''

    # determine glyph macro
    glyph_macro = ''
    for key in GLYPH_MAP.keys():
        if key.lower() in pov.lower():
            glyph_macro = GLYPH_MAP[key]
            break
    # if not found, leave glyph empty

    # sanitize
    title_tex = sanitize_title(title)
    body_tex = md_to_latex(content_body)

    # determine chapter index
    idx = None
    m2 = re.search(r'Chapter-(\d+)', md, flags=re.IGNORECASE)
    if m2:
        idx = int(m2.group(1))
    else:
        # fallback sequential
        idx = MD_FILES.index(md) + 1

    outname = f'chapter{idx:02d}.tex'
    outpath = os.path.join(OUTPUT_DIR, outname)

    tex = []
    tex.append('% Auto-generated from ' + md)
    tex.append('% Source: ' + mdpath)
    tex.append('')
    tex.append('\\chapter{' + title_tex + '}')
    # emit the current chapter number so the class can render the stripe
    tex.append('\\renewcommand{\\CurrentChapterNum}{' + str(idx) + '}')
    if glyph_macro:
        tex.append('\\POV{' + glyph_macro + '}{' + pov + '}')
    else:
        tex.append('\\POV{}{'+ pov + '}')
    tex.append('')
    tex.append(body_tex)
    tex_content = '\n'.join(tex)

    with open(outpath, 'w', encoding='utf-8') as ofh:
        ofh.write(tex_content)
    print('Wrote', outpath)

# create a master manuscript.tex that inputs all chapters in order
master_path = os.path.join(OUTPUT_DIR, 'manuscript.tex')
with open(master_path, 'w', encoding='utf-8') as mfh:
    mfh.write('\\documentclass{cwbook_minimal}\n')
    # set the total chapter count in the master file so the stripe scales
    mfh.write('\\renewcommand{\\TotalChapters}{' + str(len(MD_FILES)) + '}\n')
    mfh.write('\\begin{document}\n')
    for md in MD_FILES:
        m2 = re.search(r'Chapter-(\d+)', md, flags=re.IGNORECASE)
        if m2:
            idx = int(m2.group(1))
        else:
            idx = MD_FILES.index(md) + 1
        mfh.write(f'\\input{{chapter{idx:02d}.tex}}\n')
    mfh.write('\\end{document}\n')

print('Master manuscript.tex written to', master_path)
