#!/usr/bin/env python3
"""
Find duplicate basenames in the repository and write a CSV report.

Usage:
  python scripts/find_duplicate_basename.py --root . --out tools/reports/duplicate_basenames.csv
"""
import os
import csv
import argparse
from collections import defaultdict


def iter_files(root):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(dirpath, f)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.', help='Root directory to scan')
    p.add_argument('--out', default='tools/reports/duplicate_basenames.csv')
    args = p.parse_args()

    d = defaultdict(list)
    for path in iter_files(args.root):
        base = os.path.basename(path)
        d[base].append(path)

    duplicates = {b: paths for b, paths in d.items() if len(paths) > 1}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['basename', 'paths_count', 'paths'])
        for base in sorted(duplicates.keys()):
            paths = duplicates[base]
            w.writerow([base, len(paths), '|'.join(paths)])

    print(f'Wrote {len(duplicates)} duplicate basenames to {args.out}')


if __name__ == '__main__':
    main()
