#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reorganize_crossref.py

Purpose:
  Parse 'anpg-local-content-full-data.md' (Section 7: company-activity cross-reference)
  and produce 'fullinfobetteroorganized.md' with hierarchy:

    Serviço (Categoria)
      Nicho (Actividade)
        Tipo (SCA / SCDA / SE / Other)
          - NIF — Company Name — (Regime)

Usage:
  python reorganize_crossref.py

Notes:
  - The script is defensive about header names (looks for NIF, Nome/Company Name, Tipo/Type).
  - It preserves the original category / activity order as they appear in the .md file.
  - Output is UTF-8 markdown; large (tens of thousands of lines).

"""

from pathlib import Path
import re
import sys
from datetime import datetime

INPUT = Path('anpg-local-content-full-data.md')
OUTPUT = Path('fullinfobetteroorganized.md')

if not INPUT.exists():
    print(f"ERROR: input file {INPUT} not found. Run this from the repository root.")
    sys.exit(1)

text = INPUT.read_text(encoding='utf-8')
lines = text.splitlines()
N = len(lines)

# Find start of cross-reference section (Section 7)
start_idx = None
for i, L in enumerate(lines):
    up = L.upper()
    if re.match(r'^##\s*7\.', L) or 'COMPANY-ACTIVITY CROSS-REFERENCE' in up or 'REFERÊNCIA CRUZADA' in up or 'REFERENCIA CRUZADA' in up:
        start_idx = i + 1
        break

if start_idx is None:
    print('WARNING: Could not find explicit Section 7 marker; falling back to first occurrence of "FULL COMPANY-ACTIVITY"')
    for i, L in enumerate(lines):
        if 'FULL COMPANY-ACTIVITY' in L.upper():
            start_idx = i + 1
            break

if start_idx is None:
    print('ERROR: Could not locate the cross-reference section in the markdown. Aborting.')
    sys.exit(1)

structure = {}  # {category: {activity: {type: [ {nif,name,regime}, ... ] } } }

i = start_idx
current_category = None
current_activity = None

# Helper to detect a markdown table separator (| --- | ---: | )
def is_table_sep(line):
    if not line.strip().startswith('|'):
        return False
    cells = [c.strip() for c in line.strip().split('|')[1:-1]]
    if not cells:
        return False
    for c in cells:
        # allow patterns like ---- or :---:
        if not re.fullmatch(r'[-:\s]+', c):
            return False
    return True

# Helper to find column index given expected header tokens
def find_col_index(header_cells, tokens):
    for j, h in enumerate(header_cells):
        low = h.lower()
        for t in tokens:
            if t in low:
                return j
    return None

while i < N:
    L = lines[i]
    if L.startswith('### '):
        current_category = L[4:].strip()
        structure.setdefault(current_category, {})
        i += 1
        continue
    if L.startswith('#### '):
        # activity
        activity_line = L[5:].strip()
        # remove trailing parentheses like "(273 companies)" or "(273 empresas)"
        activity_name = re.sub(r'\s*\([^)]*\)\s*$', '', activity_line)
        structure[current_category].setdefault(activity_name, {})
        i += 1
        # advance to table header (line that starts with | and contains at least one header token)
        while i < N and not lines[i].lstrip().startswith('|'):
            i += 1
        if i >= N:
            break
        header_line = lines[i].strip()
        header_cells = []
        if header_line.startswith('|'):
            header_cells = [c.strip() for c in header_line.split('|')[1:-1]]
        # find useful columns
        idx_nif = find_col_index(header_cells, ['nif','n.º','numero','num'])
        idx_name = find_col_index(header_cells, ['company','nome','empresa','name'])
        idx_type = find_col_index(header_cells, ['type','tipo','sociedade'])
        idx_regime = find_col_index(header_cells, ['regime'])
        # skip header separator if present
        i += 1
        if i < N and is_table_sep(lines[i]):
            i += 1
        # read table rows
        while i < N and lines[i].strip().startswith('|'):
            row = lines[i].strip()
            cells = [c.strip() for c in row.split('|')[1:-1]]
            # skip weird rows
            if not cells or all(re.fullmatch(r'[-:\s]+', c) for c in cells):
                i += 1
                continue
            # try to safely extract columns
            nif = cells[idx_nif] if (idx_nif is not None and idx_nif < len(cells)) else ''
            name = cells[idx_name] if (idx_name is not None and idx_name < len(cells)) else ''
            typ = cells[idx_type] if (idx_type is not None and idx_type < len(cells)) else ''
            regime = cells[idx_regime] if (idx_regime is not None and idx_regime < len(cells)) else ''
            typ = typ.strip() or 'Unknown'
            # normalize type small variants
            if typ in ['—','-','None','none','None ']:
                typ = 'Unknown'
            # append
            structure[current_category][activity_name].setdefault(typ, []).append({
                'nif': nif,
                'name': name,
                'regime': regime,
            })
            i += 1
        continue
    i += 1

# Summaries
num_categories = len(structure)
num_activities = sum(len(v) for v in structure.values())
num_companies = sum(sum(len(lst) for lst in act.values()) for act in structure.values())

# Write output markdown
with OUTPUT.open('w', encoding='utf-8') as out:
    out.write('# Reorganização: Serviço → Nicho → Tipo → Empresas\n\n')
    out.write(f'_Gerado: {datetime.utcnow().isoformat()}Z_\n\n')
    out.write('## Sumário\n\n')
    out.write(f'- Categorias: {num_categories}\n')
    out.write(f'- Actividades (nichos): {num_activities}\n')
    out.write(f'- Entradas empresa–actividade: {num_companies}\n\n')

    # iterate preserving original order (dict preserves insertion order)
    for cat, activities in structure.items():
        out.write(f'## {cat}\n\n')
        for act, types in activities.items():
            total_in_act = sum(len(v) for v in types.values())
            out.write(f'### {act} ({total_in_act} empresas)\n\n')
            # prefer ordering for types
            pref = ['SCA', 'SCDA', 'SE']
            def type_key(t):
                if t in pref:
                    return (0, pref.index(t))
                return (1, t)
            for typ in sorted(types.keys(), key=type_key):
                comps = types[typ]
                out.write(f'#### Tipo: {typ} ({len(comps)} empresas)\n\n')
                for c in comps:
                    nif = c['nif'] or '—'
                    name = c['name'] or '—'
                    regime = c['regime'].strip()
                    if regime:
                        out.write(f'- {nif} — {name} — {regime}\n')
                    else:
                        out.write(f'- {nif} — {name}\n')
                out.write('\n')
            out.write('\n')
        out.write('\n')

print(f"Wrote {OUTPUT} — {num_categories} categories, {num_activities} activities, {num_companies} entries.")
