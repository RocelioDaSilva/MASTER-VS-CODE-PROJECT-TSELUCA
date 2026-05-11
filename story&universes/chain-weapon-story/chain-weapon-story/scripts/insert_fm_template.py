#!/usr/bin/env python3
"""
Interactive front-matter template inserter (dry-run by default).

Usage:
  python scripts/insert_fm_template.py --path <dir_or_file> [--apply]

--apply will modify files; without it the script prints candidates.
"""
import os
import re
import sys
import argparse
import datetime
import shutil

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def has_front_matter(text: str) -> bool:
    return FM_RE.match(text) is not None


def iter_md_files(root: str):
    if os.path.isfile(root):
        if root.lower().endswith('.md'):
            yield root
        return
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith('.md'):
                yield os.path.join(dirpath, f)


TEMPLATE = """---
title: "TBD"
status: Draft
updated: {date}
pov:
age:
chapter_number:
---

"""


def insert_template(path: str, dry_run: bool = True, backup: bool = True):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return False, f"read error: {e}"
    if has_front_matter(text):
        return False, 'already has front-matter'
    today = datetime.date.today().isoformat()
    new = TEMPLATE.format(date=today) + text
    if dry_run:
        return True, 'would insert template'
    if backup:
        bak = path + '.fm.bak'
        shutil.copyfile(path, bak)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
    except Exception as e:
        return False, f'write error: {e}'
    return True, 'inserted template (backup created)'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='File or directory to scan')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: dry-run)')
    parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    args = parser.parse_args()

    modified = []
    candidates = []
    for p in iter_md_files(args.path):
        ok, msg = insert_template(p, dry_run=not args.apply, backup=not args.no_backup)
        if ok:
            if args.apply:
                modified.append((p, msg))
            else:
                candidates.append((p, msg))

    if args.apply:
        if modified:
            print('Templates inserted into:')
            for p, msg in modified:
                print(p + ': ' + msg)
        else:
            print('No files needed templates.')
    else:
        if candidates:
            print('Files that would receive templates:')
            for p, msg in candidates:
                print(p + ': ' + msg)
        else:
            print('No candidate files found (all have front-matter).')


if __name__ == '__main__':
    main()
