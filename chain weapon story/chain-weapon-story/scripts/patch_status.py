#!/usr/bin/env python3
"""Inject 'status: Draft' into front-matter of .md files that are missing it."""
import os
import re

FM_RE = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.S)
ROOTS = ['story', 'manuscript']


def patch(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception:
        return False
    m = FM_RE.match(text)
    if not m:
        return False
    fm = m.group(2)
    if re.search(r'^status\s*:', fm, re.I | re.M):
        return False  # already present
    new_fm = fm + "\nstatus: Draft"
    new_text = m.group(1) + new_fm + m.group(3) + text[m.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return True


patched = 0
for root in ROOTS:
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.md'):
                if patch(os.path.join(dirpath, fn)):
                    patched += 1
print(f"Patched {patched} files")
