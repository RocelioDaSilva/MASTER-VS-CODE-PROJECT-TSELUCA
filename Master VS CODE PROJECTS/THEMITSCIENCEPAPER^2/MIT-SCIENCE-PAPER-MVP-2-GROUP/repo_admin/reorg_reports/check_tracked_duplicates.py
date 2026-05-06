#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib
import json


def compute_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    script_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    p = subprocess.run(['git', 'ls-files'], cwd=repo_root, capture_output=True, text=True)
    if p.returncode != 0:
        print('git ls-files failed:', p.stderr)
        sys.exit(1)

    files = [f.strip() for f in p.stdout.splitlines() if f.strip()]
    exclude_prefixes = ('.venv', 'node_modules', '.git', 'repo_admin/reorg_archives')

    tracked = []
    for f in files:
        if any(f.startswith(ex) for ex in exclude_prefixes):
            continue
        absf = os.path.join(repo_root, f)
        if os.path.isfile(absf):
            tracked.append((f, absf))

    mapping = {}
    for rel, absf in tracked:
        try:
            h = compute_hash(absf)
        except Exception as e:
            print('hash error', rel, e)
            continue
        mapping.setdefault(h, []).append(rel)

    duplicates = {h: paths for h, paths in mapping.items() if len(paths) > 1}
    report = {
        'scanned_tracked_count': len(tracked),
        'duplicate_groups_count': len(duplicates),
        'duplicate_files_count': sum(len(v) for v in duplicates.values()),
        'duplicates': duplicates,
    }

    out_path = os.path.join(script_dir, 'tracked_duplicates_report.json')
    with open(out_path, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps({'status': 'ok', 'scanned': len(tracked), 'groups': len(duplicates), 'files': sum(len(v) for v in duplicates.values())}, indent=2))


if __name__ == '__main__':
    main()
