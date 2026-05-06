#!/usr/bin/env python3
import re
from pathlib import Path

# File path (repo-relative)
HERE = Path(__file__).resolve().parent
candidates = [
    HERE / 'SOL.tex',
    HERE / 'SOL_melhorado.tex',
]
fpath = next((p for p in candidates if p.exists()), candidates[0])
print(f'[PATHS] file={fpath}')

# Read file
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Count before
tab_extbf = len(re.findall(r'\s+extbf\{', content))
quot_ents = len(re.findall(r'&quot;', content))
dbl_backslash = len(re.findall(r'\\\\\s', content))

print(f'Before fixes:')
print(f'  Tab+extbf patterns: {tab_extbf}')
print(f'  HTML &quot; entities: {quot_ents}')
print(f'  Double backslashes: {dbl_backslash}')

# Fix 1: Replace whitespace+extbf with \textbf
content = re.sub(r'\s+extbf\{', r'\\textbf{', content)

# Fix 2: Replace &quot; with straight quote
content = re.sub(r'&quot;', r'"', content)

# Write back
with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(fpath, 'r', encoding='utf-8') as f:
    content_after = f.read()

tab_extbf_after = len(re.findall(r'\s+extbf\{', content_after))
quot_ents_after = len(re.findall(r'&quot;', content_after))

print(f'\nAfter fixes:')
print(f'  Tab+extbf patterns: {tab_extbf_after}')
print(f'  HTML &quot; entities: {quot_ents_after}')
print(f'\nFile saved successfully!')
