#!/usr/bin/env python3
"""
Repo-wide file auditor
Generates:
 - audits/file_audit.csv
 - audits/file_audit.json
 - audits/DETAILED-FILE-BY-FILE-AUDIT.md

Run from repository root.
"""
import os
import re
import json
import csv
from collections import defaultdict

root = os.path.abspath(os.getcwd())
out_dir = os.path.join(root, 'audits')
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file_rows = []
by_basename = defaultdict(list)
by_category = defaultdict(int)
char_name_map = defaultdict(list)

# helper funcs
name_normalize = lambda s: re.sub(r"[^a-z0-9]+", '-', s.lower()).strip('-')

for dirpath, dirnames, filenames in os.walk(root):
    # skip the .git folder if present
    if '.git' in dirpath.split(os.sep):
        continue
    for fname in filenames:
        # skip the audit outputs we will create to avoid recursion
        if dirpath.startswith(out_dir):
            continue
        full = os.path.join(dirpath, fname)
        rel = os.path.relpath(full, root).replace('\\', '/')
        try:
            stat = os.stat(full)
            size = stat.st_size
        except Exception:
            size = 0
        text = ''
        try:
            with open(full, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
        except Exception:
            # binary or unreadable; record minimal info
            text = ''
        lines = text.splitlines()
        line_count = len(lines)
        word_count = len(text.split())

        # detect front-matter
        has_front = False
        fm = {}
        if len(lines) >= 1 and lines[0].strip() == '---':
            has_front = True
            end_idx = None
            for i in range(1, min(len(lines), 400)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break
            if end_idx is not None:
                meta_lines = lines[1:end_idx]
                for ml in meta_lines:
                    m = re.match(r'^([^:\n]+):\s*(.*)$', ml)
                    if m:
                        key = m.group(1).strip()
                        val = m.group(2).strip()
                        fm[key] = val

        # category detection by path
        p = rel.lower()
        if p.startswith('.obsidian') or '/.obsidian/' in p:
            cat = 'obsidian'
        elif p.startswith('.smart-env') or '/.smart-env/' in p:
            cat = 'smart-env'
        elif p.startswith('characters/') or '/characters/' in p:
            cat = 'characters'
        elif p.startswith('story/') or p.startswith('chapters/') or '/story/' in p or '/chapters/' in p:
            cat = 'story'
        elif p.startswith('world/') or '/world/' in p:
            cat = 'world'
        elif p.startswith('arcs/') or '/arcs/' in p:
            cat = 'arcs'
        elif p.startswith('audits/') or '/audits/' in p:
            cat = 'audits'
        elif p.startswith('writingtutorials/') or '/writingtutorials/' in p:
            cat = 'writingtutorials'
        elif p.startswith('assets/') or '/assets/' in p:
            cat = 'assets'
        else:
            cat = 'other'
        by_category[cat] += 1

        base = os.path.basename(fname).lower()
        by_basename[base].append(rel)

        # character name heuristics
        if cat == 'characters':
            # use filename without extension tokens
            base_noext = os.path.splitext(base)[0]
            # split on non-alpha
            tokens = re.split(r'[^a-z]+', base_noext)
            if tokens:
                primary = tokens[0]
                char_name_map[primary].append(rel)

        file_rows.append({
            'path': rel,
            'size': size,
            'lines': line_count,
            'words': word_count,
            'has_frontmatter': has_front,
            'frontmatter_keys': list(fm.keys()),
            'frontmatter': fm,
            'category': cat,
        })

# duplicates by basename
duplicates = {k:v for k,v in by_basename.items() if len(v) > 1}
# character name collisions
char_conflicts = {name:paths for name,paths in char_name_map.items() if len({os.path.basename(p).lower() for p in paths})>1 and len(paths)>1}

# timeline age checks (if NORMALIZED-AGES.csv exists)
age_map = {}
ages_csv = os.path.join(root, 'timelines', 'NORMALIZED-AGES.csv')
if os.path.exists(ages_csv):
    try:
        with open(ages_csv, 'r', encoding='utf-8', errors='replace') as f:
            rdr = csv.reader(f)
            for row in rdr:
                if not row: continue
                # expected format: chapter_index, file, age, ...
                if len(row) >= 3:
                    filefield = row[1].strip()
                    agefield = row[2].strip()
                    age_map[filefield] = agefield
    except Exception:
        pass

# compare front-matter ages
age_mismatches = []
for r in file_rows:
    if r['category'] == 'story' and r['has_frontmatter']:
        fm = r['frontmatter']
        if 'Age' in fm:
            # try to match with normalized ages by filename
            fname = os.path.basename(r['path'])
            norm = age_map.get(r['path']) or age_map.get(r['path'].replace('./','')) or age_map.get(r['path'].replace('story/',''))
            if norm and norm.lower() != fm['Age'].lower():
                age_mismatches.append({'path': r['path'], 'front_age': fm['Age'], 'normalized': norm})

# write CSV
csv_path = os.path.join(out_dir, 'file_audit.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as cf:
    w = csv.writer(cf)
    header = ['path','category','size','lines','words','has_frontmatter','frontmatter_keys']
    w.writerow(header)
    for r in file_rows:
        w.writerow([r['path'], r['category'], r['size'], r['lines'], r['words'], r['has_frontmatter'], ';'.join(r['frontmatter_keys'])])

# write JSON
json_path = os.path.join(out_dir, 'file_audit.json')
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump({'summary':{
        'total_files': len(file_rows),
        'by_category': dict(by_category),
        'duplicates_count': len(duplicates),
        'char_conflicts_count': len(char_conflicts),
    }, 'files': file_rows, 'duplicates': duplicates, 'char_conflicts': char_conflicts, 'age_mismatches': age_mismatches}, jf, indent=2)

# write human readable markdown summary
md_path = os.path.join(out_dir, 'DETAILED-FILE-BY-FILE-AUDIT.md')
with open(md_path, 'w', encoding='utf-8') as mf:
    mf.write('# Detailed File-by-File Audit\n\n')
    mf.write(f'- Repository root: `{root}`\n')
    mf.write(f'- Total files scanned: {len(file_rows)}\n\n')
    mf.write('## Summary by category\n\n')
    for cat, cnt in sorted(by_category.items(), key=lambda x:-x[1]):
        mf.write(f'- **{cat}**: {cnt} files\n')
    mf.write('\n')

    mf.write('## High-priority findings\n\n')
    if duplicates:
        mf.write(f'- **Filename duplicates**: {len(duplicates)} basenames found in multiple locations. Examples:\n')
        for k, v in list(duplicates.items())[:20]:
            mf.write(f'  - `{k}` -> {len(v)} files\n')
            for p in v[:6]:
                mf.write(f'    - {p}\n')
    else:
        mf.write('- No filename duplicates detected.\n')
    mf.write('\n')

    if char_conflicts:
        mf.write(f'- **Character name collisions**: {len(char_conflicts)} names with multiple profile files. Examples:\n')
        for name, paths in list(char_conflicts.items())[:30]:
            mf.write(f'  - `{name}` -> {len(paths)} files\n')
            for p in paths[:6]:
                mf.write(f'    - {p}\n')
    else:
        mf.write('- No character name collisions detected by heuristic.\n')
    mf.write('\n')

    if age_mismatches:
        mf.write(f'- **Timeline age mismatches**: {len(age_mismatches)} files where front-matter `Age` differs from `timelines/NORMALIZED-AGES.csv`. Examples:\n')
        for am in age_mismatches[:20]:
            mf.write(f'  - {am["path"]}: front `{am["front_age"]}` vs normalized `{am["normalized"]}`\n')
    else:
        mf.write('- No story front-matter age mismatches detected (where data available).\n')
    mf.write('\n')

    mf.write('## Files missing front-matter (story files)\n\n')
    missing_fm = [r['path'] for r in file_rows if r['category']=='story' and not r['has_frontmatter']]
    mf.write(f'- {len(missing_fm)} story files without YAML front-matter. Example list (first 50):\n')
    for p in missing_fm[:50]:
        mf.write(f'  - {p}\n')
    mf.write('\n')

    mf.write('## Per-file sample (first 200 characters)\n\n')
    for r in file_rows[:200]:
        preview = ''
        try:
            with open(os.path.join(root, r['path']), 'r', encoding='utf-8', errors='replace') as f:
                preview = f.read(200).replace('\n','\\n')
        except Exception:
            preview = ''
        mf.write(f'- {r["path"]} — {r["category"]} — {r["lines"]} lines — fm:{r["has_frontmatter"]} — preview: `{preview}`\n')

print('AUDIT_COMPLETE')
print('Outputs:')
print(' -', csv_path)
print(' -', json_path)
print(' -', md_path)
