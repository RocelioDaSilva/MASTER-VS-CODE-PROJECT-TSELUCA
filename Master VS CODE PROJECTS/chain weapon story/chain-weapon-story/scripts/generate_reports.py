#!/usr/bin/env python3
"""
Generate CSV reports: missing_frontmatter.csv and duplicate_basenames.csv

Scans the following directories (if present): story/, manuscript/, finished-manuscript/
Outputs to tools/reports/ by default.
"""
import os
import re
import csv
import argparse

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
TARGETS = ['story', 'manuscript', 'finished-manuscript']


def iter_md_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith('.md'):
                yield os.path.join(dirpath, f)


def has_front_matter(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            sample = fh.read(4096)
    except Exception as e:
        return False, f'read error: {e}'
    if FM_RE.match(sample):
        return True, None
    return False, 'missing front-matter'


def scan_missing_frontmatter(target_dirs):
    results = []
    for d in target_dirs:
        if not os.path.isdir(d):
            continue
        for md in iter_md_files(d):
            ok, reason = has_front_matter(md)
            if not ok:
                results.append((md, reason))
    return results


def find_duplicate_basenames(root):
    from collections import defaultdict
    d = defaultdict(list)
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            d[f].append(os.path.join(dirpath, f))
    duplicates = [(b, paths) for b, paths in d.items() if len(paths) > 1]
    return duplicates


def write_missing_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['path', 'reason'])
        for p, reason in rows:
            w.writerow([p, reason])


def write_duplicates_csv(path, duplicates):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['basename', 'count', 'paths'])
        for b, paths in sorted(duplicates, key=lambda x: x[0]):
            w.writerow([b, len(paths), '|'.join(paths)])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out-dir', default='tools/reports', help='Output folder for CSVs')
    p.add_argument('--root', default='.', help='Repository root to scan for duplicates')
    args = p.parse_args()

    targets = [d for d in TARGETS if os.path.isdir(d)]
    missing = scan_missing_frontmatter(targets)
    duplicates = find_duplicate_basenames(args.root)

    out_missing = os.path.join(args.out_dir, 'missing_frontmatter.csv')
    out_dups = os.path.join(args.out_dir, 'duplicate_basenames.csv')
    write_missing_csv(out_missing, missing)
    write_duplicates_csv(out_dups, duplicates)

    print(f'Wrote missing front-matter: {len(missing)} rows to {out_missing}')
    print(f'Wrote duplicates: {len(duplicates)} basenames to {out_dups}')


if __name__ == '__main__':
    main()
