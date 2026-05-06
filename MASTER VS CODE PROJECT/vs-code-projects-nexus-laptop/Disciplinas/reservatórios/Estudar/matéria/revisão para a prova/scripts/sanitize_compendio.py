#!/usr/bin/env python3
import re
from pathlib import Path


def protect_blocks(text, pattern):
    global _PLACEHOLDER_COUNTER
    try:
        _PLACEHOLDER_COUNTER
    except NameError:
        _PLACEHOLDER_COUNTER = 0
    placeholders = {}
    def repl(m):
        global _PLACEHOLDER_COUNTER
        key = f"@@PH{_PLACEHOLDER_COUNTER}@@"
        _PLACEHOLDER_COUNTER += 1
        placeholders[key] = m.group(0)
        return key
    new_text = pattern.sub(repl, text)
    return new_text, placeholders


def restore_blocks(text, placeholders):
    for k, v in placeholders.items():
        text = text.replace(k, v)
    return text


root = Path(__file__).parent
src = root / 'compendio_prova_topicos.tex'
if not src.exists():
    src = Path(r'c:/Users/PCGAME/Desktop/reservatórios/Estudar/matéria/revisão para a prova/compendio_prova_topicos.tex')
out = root / 'compendio_prova_topicos_auto_sanitized.tex'
backup = root / 'compendio_prova_topicos.tex.bak'

text = src.read_text(encoding='utf-8')
if not backup.exists():
    backup.write_text(text, encoding='utf-8')

# Protect Verbatim-like and code fence blocks and \VerbatimInput lines
verbatim_pattern = re.compile(r"\\begin\{Verbatim\}.*?\\end\{Verbatim\}", re.S)
verbatim_lower_pattern = re.compile(r"\\begin\{verbatim\}.*?\\end\{verbatim\}", re.S)
verbatiminput_pattern = re.compile(r"\\VerbatimInput\{.*?\}")
lstlisting_pattern = re.compile(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", re.S)
minted_pattern = re.compile(r"\\begin\{minted\}.*?\\end\{minted\}", re.S)
code_fence_pattern = re.compile(r"```.*?```", re.S)

text, verb_blocks = protect_blocks(text, verbatim_pattern)
text, verb_lower_blocks = protect_blocks(text, verbatim_lower_pattern)
text, lst_blocks = protect_blocks(text, lstlisting_pattern)
text, minted_blocks = protect_blocks(text, minted_pattern)
text, code_fence_blocks = protect_blocks(text, code_fence_pattern)
text, verbinput_blocks = protect_blocks(text, verbatiminput_pattern)

# Protect math environments to avoid inserting $ inside them
math_patterns = [re.compile(r"\\\(.*?\\\)", re.S),
                 re.compile(r"\\\[.*?\\\]", re.S),
                 re.compile(r"\$\$.*?\$\$", re.S),
                 re.compile(r"\$.*?\$", re.S)]
math_placeholders = {}
for pat in math_patterns:
    text, new_ph = protect_blocks(text, pat)
    math_placeholders.update(new_ph)

# Protect simple \text{...} blocks to avoid injecting $ or changing units inside them
textcmd_pattern = re.compile(r"\\text\{.*?\}", re.S)
text, textcmd_blocks = protect_blocks(text, textcmd_pattern)

# Protect existing \texttt{...} blocks to avoid interpreting inline $ or # inside them
texttt_pattern = re.compile(r"\\texttt\{.*?\}", re.S)
text, texttt_blocks = protect_blocks(text, texttt_pattern)

# Now safe to perform textual replacements on non-verbatim, non-math text
# 1) Markdown bold/italic
text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\emph{\1}", text)

# 2) Remove Markdown horizontal rules
text = re.sub(r"^---\s*$", "", text, flags=re.M)

# 2b) Convert Markdown headings (#, ##, ###) to LaTeX sections
text = re.sub(r"(?m)^\s*###\s+(.*)", r"\\subsubsection{\1}", text)
text = re.sub(r"(?m)^\s*##\s+(.*)", r"\\subsection{\1}", text)
text = re.sub(r"(?m)^\s*#\s+(.*)", r"\\section{\1}", text)

# 3) Convert inline backticks to \texttt{...} (safer than math-mode conversion)
def backtick_to_texttt(m):
    inner = m.group(1)
    # Escape only braces and percent inside \texttt, avoid doubling backslashes
    inner = inner.replace('{', '\\{').replace('}', '\\}').replace('%','\\%')
    # Avoid introducing math or macro tokens inside \texttt
    inner = inner.replace('$', '\\$').replace('#', '\\#').replace('_', '\\_')
    inner = inner.replace('\\', '\\textbackslash{}')
    return f"\\texttt{{{inner}}}"

# NOTE: inline backtick -> \texttt conversion is disabled to avoid corrupting TeX
# quoting and math fragments inside the LaTeX master file. If you need inline
# code formatting for Markdown sources, run a separate pass on the original
# Markdown files instead.

# Strip single-backtick inline code spans (safe fallback): remove surrounding backticks
# but avoid TeX-style double quotes (``...'') — preserves inner content as-is.
text = re.sub(r"(?<!`)`([^`]+)`(?!`)", r"\1", text)

# 4) Convert underscore identifiers like A_eff -> $A_{eff}$ outside math (we've protected math)
def underscore_to_math(m):
    base = m.group(1)
    sub = m.group(2)
    return f"${base}_{{{sub}}}$"

# Only convert identifiers with underscore that are NOT LaTeX commands (not preceded by backslash)
text = re.sub(r"(?<!\\)\b([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9_]+)\b", underscore_to_math, text)

# 5) Convert m^3 and Sm^3 and numeric powers to math-mode using \mathrm
text = re.sub(r"\bSm\^3\b", r"$\\mathrm{Sm}^3$", text)
text = re.sub(r"\bm\^3\b", r"$\\mathrm{m}^3$", text)
text = re.sub(r"\b(10)\^(\d+)\b", lambda m: f"${m.group(1)}^{{{m.group(2)}}}$", text)

# 6) Small cleanup: remove stray Markdown list markers like '- ' at line starts when they appear inside paragraphs
text = re.sub(r"(?m)^[ ]{0,3}-[ ]+", "- ", text)

# Restore protected blocks in reverse order
# Escape any remaining '#' characters in unprotected content (safe fallback)
text = text.replace('#', r'\\#')

def _restore_texttt_safely(text, blocks):
    for k, v in blocks.items():
        m = re.match(r"\\texttt\{(.*)\}", v, re.S)
        if m:
            inner = m.group(1)
            safe_inner = (inner.replace('\\', '\\textbackslash{}')
                               .replace('{', '\\{').replace('}', '\\}')
                               .replace('$', '\\$').replace('#', '\\#')
                               .replace('_', '\\_'))
            repl = f"\\texttt{{{safe_inner}}}"
        else:
            repl = v.replace('$', '\\$').replace('#', '\\#').replace('_','\\_')
        text = text.replace(k, repl)
    return text

text = restore_blocks(text, textcmd_blocks)
text = restore_blocks(text, math_placeholders)
text = _restore_texttt_safely(text, texttt_blocks)
text = restore_blocks(text, verbinput_blocks)

# Convert any protected code-fence placeholders into Verbatim environments
def _restore_code_fences_as_verbatim(text, code_blocks):
    for k, v in code_blocks.items():
        m = re.match(r"```(?:[^\n]*)\n(.*?)\n```", v, re.S)
        if m:
            inner = m.group(1)
        else:
            inner = v.strip('`')
        repl = "\\begin{Verbatim}\n" + inner + "\n\\end{Verbatim}"
        text = text.replace(k, repl)
    return text

text = _restore_code_fences_as_verbatim(text, code_fence_blocks)
text = restore_blocks(text, minted_blocks)
text = restore_blocks(text, lst_blocks)
text = restore_blocks(text, verb_lower_blocks)
text = restore_blocks(text, verb_blocks)

out.write_text(text, encoding='utf-8')
print(f"Wrote sanitized file: {out}\nBackup saved as: {backup}")
