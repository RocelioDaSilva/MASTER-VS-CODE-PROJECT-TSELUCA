#!/usr/bin/env python3
"""Fix LaTeX command issues in SOL.tex"""

import re
import os

filepath = r"Full project\01_Science\manuscript\SOL.tex"

# Read the file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file size: {len(content)} bytes")

# Count issues before
before_literal_newlines = content.count(r'\n')
print(f"Found {before_literal_newlines} instances of literal \\n newlines")

# MOST IMPORTANT: Fix literal \n escape sequences to actual newlines
content = content.replace(r'\n', '\n')

# Fix double backslashes for LaTeX commands
replacements = [
    ('\\\\begin{', '\\begin{'),
    ('\\\\end{', '\\end{'),
    ('\\\\subsection{', '\\subsection{'),
    ('\\\\subsubsection{', '\\subsubsection{'),
    ('\\\\section{', '\\section{'),
    ('\\\\item ', '\\item '),
    ('\\\\hline', '\\hline'),
    ('\\\\textwidth', '\\textwidth'),
    ('\\\\multicolumn', '\\multicolumn'),
    ('\\\\small', '\\small'),
    ('\\\\itshape', '\\itshape'),
    ('\\\\bfseries', '\\bfseries'),
    ('\\\\tikzstyle', '\\tikzstyle'),
    ('\\\\node', '\\node'),
    ('\\\\draw', '\\draw'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Fix \extbf and \extit (missing 't')
content = content.replace('\\extbf{', '\\textbf{')
content = content.replace('\\extit{', '\\textit{')

# Fix escaped percent signs (double backslash before %)
content = re.sub(r'\\\\%', r'\\%', content)

# Count issues after
after_literal_newlines = content.count(r'\n')
print(f"\nAfter fixes:")
print(f"Remaining literal \\n: {after_literal_newlines}")

# Backup original
backup_path = filepath + '.backup_before_newline_fix'
if not os.path.exists(backup_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(backup_path, 'w', encoding='utf-8') as backup:
        backup.write(original)
    print(f"Backup created: {backup_path}")

# Write the fixed file
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed file written: {filepath}")
print(f"New file size: {len(content)} bytes")
print("Done!")
