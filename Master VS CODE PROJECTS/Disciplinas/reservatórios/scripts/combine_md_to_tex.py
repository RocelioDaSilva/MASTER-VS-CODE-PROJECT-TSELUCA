#!/usr/bin/env python3
r"""
Combine Markdown files into a single LaTeX file with basic Markdown->LaTeX conversions.
This is a pragmatic converter (headings, code fences, inline code, bold/italic, lists).
It preserves LaTeX math ($...$, $$...$$) and LaTeX blocks.

Run:
    python scripts\combine_md_to_tex.py

Output:
    c:\Users\PCGAME\Desktop\reservatórios\Estudar\matéria\revisão para a prova\compendio_revisao_prova.tex
"""
from pathlib import Path
import re

# Auto-discover input Markdown files in a sensible order:
# - cap 1..5 transcriptions (if present)
# - exercises folder files
# - revisão para a prova files in preferred order
BASE_DIR = Path(r"c:\Users\PCGAME\Desktop\reservatórios")
INPUT_DIR = BASE_DIR / "Estudar" / "matéria"
REV_DIR = INPUT_DIR / "revisão para a prova"

INPUT_FILES = []
# chapters
for i in range(1, 6):
    p = INPUT_DIR / f"cap {i}" / f"cap{i}_transcription.md"
    if p.exists():
        INPUT_FILES.append(str(p))

# exercises (any markdown files inside exercícios/)
ex_dir = INPUT_DIR / "exercícios"
if ex_dir.exists():
    for p in sorted(ex_dir.glob("*.md")):
        INPUT_FILES.append(str(p))

# revisão files in chosen order
rev_order = [
    "resumo_capitulos.md",
    "resumo_capitulos_ultra_detalhado.md",
    "compressibilidade_Z_cheatsheet.md",
    "exercicios_resolvidos.md",
    "exame_gabarito.md",
]
for name in rev_order:
    p = REV_DIR / name
    if p.exists():
        INPUT_FILES.append(str(p))

# fallback to the revisão files if nothing else found
if not INPUT_FILES:
    INPUT_FILES = [
        str(REV_DIR / "resumo_capitulos.md"),
        str(REV_DIR / "resumo_capitulos_ultra_detalhado.md"),
        str(REV_DIR / "compressibilidade_Z_cheatsheet.md"),
        str(REV_DIR / "exercicios_resolvidos.md"),
        str(REV_DIR / "exame_gabarito.md"),
    ]

print('Using INPUT_FILES:')
for f in INPUT_FILES:
    print(' -', f)

OUTPUT_TEX = Path(r"c:\Users\PCGAME\Desktop\reservatórios\Estudar\matéria\revisão para a prova\compendio_revisao_prova.tex")

PREAMBLE = r'''\documentclass[11pt,a4paper]{article}
% XeLaTeX-friendly preamble: use fontspec for Unicode fonts
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}
\usepackage[brazil]{babel}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{longtable}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage{microtype}
    itle{Revisão para a prova — Engenharia de Reservatórios I}
\author{Compilado}
\date{Gerado em 2026-04-22}
\begin{document}
\maketitle
    ableofcontents
\clearpage
'''

POSTAMBLE = '\\end{document}\\n'


def sanitize_heading(text: str) -> str:
    # minimal sanitize for heading text (avoid unbalanced braces)
    return text.replace('{', '\\{').replace('}', '\\}').strip()


def is_math_line(line: str) -> bool:
    # crude detection: lines that start or end with $$ or contain inline $...$
    if line.strip().startswith('$$') or line.strip().endswith('$$'):
        return True
    if '$' in line:
        # consider it math-containing; to be safe we avoid altering
        return True
    return False


def convert_lines(lines):
    out_lines = []
    in_code = False
    in_itemize = False
    in_enumerate = False
    # when True we skip lines inside reference/bibliography sections
    skip_section = False
    SKIP_REF_KEYWORDS = ['referen', 'bibliog', 'bibliogr', 'bibliografia', 'references', 'bibliography', 'referência', 'referencias']
    BIB_CMDS = ['\\bibliography', '\\bibliographystyle', '\\printbibliography', '\\addbibresource']

    def close_lists():
        nonlocal in_itemize, in_enumerate
        r = []
        if in_itemize:
            r.append('\end{itemize}\n')
            in_itemize = False
        if in_enumerate:
            r.append('\end{enumerate}\n')
            in_enumerate = False
        return r

    for raw in lines:
        line = raw.rstrip('\n')
        # remove non-printable control characters (e.g. backspace) that break LaTeX
        line = re.sub(r'[\x00-\x08\x0b-\x1f]', '', line)
        # skip LaTeX bibliography commands if present
        if any(cmd in line for cmd in BIB_CMDS):
            continue
        # if currently skipping a references section, ignore until next heading
        if skip_section:
            if line.lstrip().startswith('#'):
                title_candidate = line.lstrip('#').strip().lower()
                if not any(k in title_candidate for k in SKIP_REF_KEYWORDS):
                    skip_section = False
                    # fall through to process this heading
                else:
                    continue
            else:
                continue
        # handle fenced code blocks
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                out_lines.extend(close_lists())
                out_lines.append('\\begin{verbatim}\n')
            else:
                in_code = False
                out_lines.append('\\end{verbatim}\n')
            continue

        if in_code:
            out_lines.append(line + '\n')
            continue

        # headings (allow leading whitespace before the '#')
        s = line.lstrip()
        if s.startswith('# '):
            out_lines.extend(close_lists())
            title_raw = s[2:].strip()
            if any(k in title_raw.lower() for k in SKIP_REF_KEYWORDS):
                skip_section = True
                continue
            title = sanitize_heading(title_raw)
            out_lines.append(f'\\section{{{title}}}\n')
            continue
        if s.startswith('## '):
            out_lines.extend(close_lists())
            title_raw = s[3:].strip()
            if any(k in title_raw.lower() for k in SKIP_REF_KEYWORDS):
                skip_section = True
                continue
            title = sanitize_heading(title_raw)
            out_lines.append(f'\\subsection{{{title}}}\n')
            continue
        if s.startswith('### '):
            out_lines.extend(close_lists())
            title_raw = s[4:].strip()
            if any(k in title_raw.lower() for k in SKIP_REF_KEYWORDS):
                skip_section = True
                continue
            title = sanitize_heading(title_raw)
            out_lines.append(f'\\subsubsection{{{title}}}\n')
            continue

        # lists: unordered
        m_item = re.match(r'^\s*[-\*]\s+(.*)', line)
        if m_item:
            if not in_itemize:
                out_lines.append('\\begin{itemize}\n')
                in_itemize = True
            content = m_item.group(1)
            out_lines.append('\\item ' + content + '\n')
            continue

        # enumerated lists: numeric (1) or lettered (A)
        m_enum_num = re.match(r'^\s*(\d+)[\)\.]\s+(.*)', line)
        m_enum_letter = re.match(r'^\s*([A-Za-z])[\)\.]\s+(.*)', line)
        if m_enum_num:
            if not in_enumerate:
                out_lines.append('\\begin{enumerate}\n')
                in_enumerate = True
            content = m_enum_num.group(2)
            out_lines.append('\\item ' + content + '\n')
            continue
        if m_enum_letter:
            if not in_enumerate:
                # use alphabetical labels for lettered options (requires enumitem)
                out_lines.append('\\begin{enumerate}[label=\\Alph*)]\n')
                in_enumerate = True
            content = m_enum_letter.group(2)
            out_lines.append('\\item ' + content + '\\n')
            continue

        # blank line -> paragraph separation
        if line.strip() == '':
            out_lines.extend(close_lists())
            out_lines.append('\n')
            continue

        # Inline formatting: bold, italic, inline code
        # We apply conversions even if line contains $; avoid touching explicit LaTeX commands (backslash)
        if '\\' in line:
            out_lines.append(line + '\n')
            continue

        # bold **text** (use lambda to preserve groups safely)
        line = re.sub(r'\*\*(.+?)\*\*', lambda m: '\\textbf{' + m.group(1) + '}', line)
        # italic *text* (avoid matching bold)
        line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', lambda m: '\\emph{' + m.group(1) + '}', line)
        # inline code `code`
        line = re.sub(r'`(.+?)`', lambda m: '\\texttt{' + m.group(1) + '}', line)

        # minimal escape for %, &, # when no backslashes present
        line = line.replace('%', '\\%').replace('&', '\\&').replace('#', '\\#')

        out_lines.append(line + '\n')

    out_lines.extend(close_lists())
    return out_lines


def main():
    parts = []
    for f in INPUT_FILES:
        p = Path(f)
        if not p.exists():
            print(f'Warning: file not found: {f}')
            continue
        text = p.read_text(encoding='utf-8')
        # extract first heading for a section title if present
        first_line = ''
        for ln in text.splitlines():
            if ln.strip():
                first_line = ln.strip()
                break
        parts.append('\n% ---- file: ' + p.name + '\n')
        # convert and append
        lines = text.splitlines(True)
        conv = convert_lines(lines)
        parts.extend(conv)

    # write output
    OUTPUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_TEX.open('w', encoding='utf-8') as fh:
        fh.write(PREAMBLE)
        for item in parts:
            fh.write(item)
        fh.write(POSTAMBLE)

    print('Wrote', OUTPUT_TEX)


if __name__ == '__main__':
    main()
