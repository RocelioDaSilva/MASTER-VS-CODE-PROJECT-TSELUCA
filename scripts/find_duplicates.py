#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
import json
import argparse
from collections import defaultdict


def sha256_file(path, chunk_size=1024*1024):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(root='.', ignore_dirs=None, min_size=1):
    if ignore_dirs is None:
        ignore_dirs = {'.git', 'node_modules', '.venv', 'venv', 'env', '__pycache__', '.idea', '.vscode'}
    size_map = defaultdict(list)
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                if not os.path.isfile(fpath):
                    continue
                st = os.stat(fpath)
            except Exception:
                continue
            sz = st.st_size
            total_files += 1
            if sz < min_size:
                continue
            size_map[sz].append(fpath)
    hash_map = defaultdict(list)
    for sz, files in size_map.items():
        if len(files) < 2:
            continue
        for f in files:
            try:
                h = sha256_file(f)
            except Exception:
                continue
            hash_map[(h, sz)].append(f)
    dup_groups = []
    reclaimable = 0
    for (h, sz), files in hash_map.items():
        if len(files) > 1:
            dup_groups.append({'hash': h, 'size': sz, 'files': files})
            reclaimable += (len(files) - 1) * sz
    return {
        'scanned_files': total_files,
        'duplicate_groups_count': len(dup_groups),
        'reclaimable_bytes': reclaimable,
        'groups': dup_groups,
    }


def human_size(n):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return f"{n:.2f} {unit}"
        n /= 1024.0
    return f"{n:.2f} PB"


def main():
    p = argparse.ArgumentParser(description='Find duplicate files by content')
    p.add_argument('--root', default='.', help='Root folder to scan')
    p.add_argument('--min-size', type=int, default=1, help='Minimum size in bytes to consider')
    p.add_argument('--ignore', nargs='*', default=None, help='Directory names to ignore (space separated)')
    p.add_argument('--json-out', default='duplicates_report.json', help='JSON report path')
    p.add_argument('--txt-out', default='duplicates_report.txt', help='Text report path')
    args = p.parse_args()
    ignore_dirs = set(args.ignore) if args.ignore else None
    res = find_duplicates(root=args.root, ignore_dirs=ignore_dirs, min_size=args.min_size)
    with open(args.json_out, 'w', encoding='utf-8') as jf:
        json.dump(res, jf, indent=2)
    with open(args.txt_out, 'w', encoding='utf-8') as tf:
        tf.write(f"Scanned files: {res['scanned_files']}\n")
        tf.write(f"Duplicate groups: {res['duplicate_groups_count']}\n")
        tf.write(f"Potential reclaimable space: {res['reclaimable_bytes']} bytes ({human_size(res['reclaimable_bytes'])})\n\n")
        for i, g in enumerate(res['groups'], start=1):
            tf.write(f"Group {i}: hash={g['hash']} size={g['size']} bytes ({human_size(g['size'])})\n")
            for f in g['files']:
                tf.write(f"  - {f}\n")
            tf.write("\n")
    print(f"Scanned {res['scanned_files']} files. Found {res['duplicate_groups_count']} duplicate groups.")
    print(f"Report written to {args.json_out} and {args.txt_out}")


if __name__ == '__main__':
    main()
