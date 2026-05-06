"""
add_backlinks.py
================
Add peer backlinks between company Markdown files in `company_hierarchy/`.

For each company file (CompanyName_NIF.md) it will add or update a
"## 🔗 Backlinks" section containing up to N peers from the same niche
(directory). Links are relative and URL-quoted per-segment.

Usage: python add_backlinks.py
"""

import os
import re
from urllib.parse import quote

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "data", "processed")
BASE_DIR = os.path.normpath(BASE_DIR)
HIER_ROOT = os.path.join(BASE_DIR, "company_hierarchy")
BACKLINKS_PER_FILE = 10

FNAME_RE = re.compile(r"^(.+?)_([^_]+)\.md$", re.UNICODE)
SECTION_TITLE = "## 🔗 Backlinks"


def build_dir_index(root):
    """Return mapping dirpath -> sorted list of entries {fname,name,nif,fpath}.
    """
    index = {}
    for dirpath, _dirs, files in os.walk(root):
        md_files = [f for f in files if f.lower().endswith('.md')]
        if not md_files:
            continue
        entries = []
        for fname in md_files:
            m = FNAME_RE.match(fname)
            if m:
                name = m.group(1)
                nif = m.group(2)
            else:
                name = fname[:-3]
                nif = ''
            entries.append({
                'fname': fname,
                'name': name,
                'nif': nif,
                'fpath': os.path.join(dirpath, fname)
            })
        entries.sort(key=lambda x: x['name'].lower())
        index[dirpath] = entries
    return index


def make_rel_link(from_path, to_path):
    rel = os.path.relpath(to_path, os.path.dirname(from_path)).replace('\\', '/')
    # quote each path segment but keep '/'
    parts = rel.split('/')
    parts_q = [quote(p) for p in parts]
    return '/'.join(parts_q)


def build_section(peers, current_path):
    if not peers:
        return ''
    lines = []
    lines.append('\n---\n\n' + SECTION_TITLE + '\n')
    lines.append('\n- **Peer companies in this niche:**\n')
    for peer in peers:
        rel = make_rel_link(current_path, peer['fpath'])
        # Use display name as the link text
        lines.append(f'- [{peer["name"]}]({rel})')
    lines.append('\n')
    return '\n'.join(lines)


def insert_backlinks_into_content(content, section):
    # place before the final note '> **Nota:**' if present
    note_marker = '\n> **Nota:**'
    if note_marker in content:
        idx = content.rfind(note_marker)
        return content[:idx] + section + content[idx:]

    # remove existing backlinks block if present
    if SECTION_TITLE in content:
        pattern = re.compile(r'\n---\n\n' + re.escape(SECTION_TITLE) + r'[\s\S]*?(?=\n---\n\n|\Z)', re.MULTILINE)
        content = pattern.sub('', content)

    # append at end
    if not content.endswith('\n'):
        content += '\n'
    return content + section


def main():
    print("Building directory index…")
    index = build_dir_index(HIER_ROOT)
    total = 0
    updated = 0

    for dirpath, entries in index.items():
        for ent in entries:
            total += 1
            peers = [e for e in entries if e['fpath'] != ent['fpath']]
            peers = peers[:BACKLINKS_PER_FILE]
            section = build_section(peers, ent['fpath'])

            try:
                with open(ent['fpath'], 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except Exception as exc:
                print(f"Could not read {ent['fpath']}: {exc}")
                continue

            new_content = insert_backlinks_into_content(content, section)
            if new_content != content:
                try:
                    with open(ent['fpath'], 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    updated += 1
                except Exception as exc:
                    print(f"Could not write {ent['fpath']}: {exc}")

            if updated and updated % 5000 == 0:
                print(f"  ... {updated} files updated")

    print('\nDone.')
    print(f'  Total files processed: {total}')
    print(f'  Files updated: {updated}')


if __name__ == '__main__':
    main()
