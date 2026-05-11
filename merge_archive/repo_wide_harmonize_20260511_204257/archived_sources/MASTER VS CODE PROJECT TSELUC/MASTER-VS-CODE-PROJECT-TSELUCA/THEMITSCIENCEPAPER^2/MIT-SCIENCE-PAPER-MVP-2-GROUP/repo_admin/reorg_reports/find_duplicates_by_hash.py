import os
import hashlib
import json
import argparse
import subprocess


def find_root(default=None):
    if default:
        return os.path.abspath(default)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def compute_hash(path, chunk_size=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description='Find duplicate files by content hash')
    p.add_argument('--root', help='Repository root', default=None)
    p.add_argument('--exclude', nargs='*', default=['.git', '.venv', 'node_modules', 'repo_admin/reorg_archives'])
    p.add_argument('--out_all', default=os.path.join(os.path.dirname(__file__), 'duplicates_content.json'))
    p.add_argument('--out_tracked', default=os.path.join(os.path.dirname(__file__), 'duplicates_tracked.json'))
    args = p.parse_args()

    repo_root = find_root(args.root)
    excluded = [os.path.normpath(os.path.join(repo_root, e)) for e in args.exclude]

    hash_map = {}  # hash -> list of absolute paths
    size_map = {}

    print('Scanning files under', repo_root)

    for dirpath, dirnames, filenames in os.walk(repo_root):
        norm_dir = os.path.normpath(dirpath)
        if any(norm_dir == ex or norm_dir.startswith(ex + os.sep) for ex in excluded):
            continue
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                if os.path.islink(full) or not os.path.isfile(full):
                    continue
                # compute size
                size = os.path.getsize(full)
                h = compute_hash(full)
                size_map.setdefault(h, size)
                hash_map.setdefault(h, []).append(os.path.relpath(full, repo_root).replace('\\','/'))
            except Exception as e:
                # skip unreadable files
                continue

    duplicates_all = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    # Now check git-tracked files
    try:
        p = subprocess.run(['git', 'ls-files', '-z'], cwd=repo_root, capture_output=True, check=True)
        tracked_raw = p.stdout
        tracked = [t for t in tracked_raw.decode('utf-8', errors='ignore').split('\0') if t]
    except Exception:
        tracked = []

    tracked_hash_map = {}
    for rel in tracked:
        abs_path = os.path.join(repo_root, rel)
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            continue
        # reuse computed hash if present
        rel_norm = rel.replace('\\','/')
        found = None
        for h, paths in hash_map.items():
            if rel_norm in paths:
                found = h
                break
        if not found:
            try:
                found = compute_hash(abs_path)
            except Exception:
                continue
        tracked_hash_map.setdefault(found, []).append(rel_norm)

    duplicates_tracked = {h: paths for h, paths in tracked_hash_map.items() if len(paths) > 1}

    summary = {
        'repo_root': repo_root,
        'excluded': args.exclude,
        'scanned_files_count': sum(len(v) for v in hash_map.values()),
        'duplicate_groups_all': len(duplicates_all),
        'duplicate_groups_tracked': len(duplicates_tracked),
    }

    with open(args.out_all, 'w', encoding='utf-8') as fh:
        json.dump({'summary': summary, 'duplicates_all': duplicates_all}, fh, indent=2)

    with open(args.out_tracked, 'w', encoding='utf-8') as fh:
        json.dump({'summary': summary, 'duplicates_tracked': duplicates_tracked}, fh, indent=2)

    print('Wrote', args.out_all)
    print('Wrote', args.out_tracked)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
