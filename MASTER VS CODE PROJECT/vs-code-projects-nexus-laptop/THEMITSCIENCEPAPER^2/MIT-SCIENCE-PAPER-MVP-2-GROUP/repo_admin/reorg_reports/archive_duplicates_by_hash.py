import os
import json
import shutil
import argparse
import subprocess
import time


def find_root(default=None):
    if default:
        return os.path.abspath(default)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def is_archived(rel):
    return rel.replace('\\', '/').startswith('repo_admin/reorg_archives')


def run_git_ls(repo_root):
    try:
        p = subprocess.run(['git', 'ls-files', '-z'], cwd=repo_root, capture_output=True, check=True)
        raw = p.stdout.decode('utf-8', errors='ignore')
        return [t for t in raw.split('\0') if t]
    except Exception:
        return []


def ensure_parent(path):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)


def safe_move(src, dst):
    ensure_parent(dst)
    if os.path.exists(dst):
        base, ext = os.path.splitext(dst)
        dst = f"{base}-dup-{int(time.time())}{ext}"
    shutil.move(src, dst)
    return dst


def main():
    p = argparse.ArgumentParser(description='Archive duplicate files by content hash and update references')
    p.add_argument('--root', default=None)
    p.add_argument('--duplicates_tracked', default=os.path.join(os.path.dirname(__file__), 'duplicates_tracked.json'))
    p.add_argument('--duplicates_all', default=os.path.join(os.path.dirname(__file__), 'duplicates_content.json'))
    p.add_argument('--out_map', default=os.path.join(os.path.dirname(__file__), 'archive_move_map.json'))
    p.add_argument('--out_summary', default=os.path.join(os.path.dirname(__file__), 'archive_reorg_summary.json'))
    p.add_argument('--exclude', nargs='*', default=['.git', '.venv', 'node_modules', 'repo_admin/reorg_archives'])
    p.add_argument('--text_exts', nargs='*', default=['.md', '.tex', '.txt', '.py', '.js', '.json', '.html', '.htm', '.yml', '.yaml', '.rst', '.csv', '.bib'])
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--commit', action='store_true')
    args = p.parse_args()

    repo_root = find_root(args.root)

    tracked_data = load_json(args.duplicates_tracked)
    all_data = load_json(args.duplicates_all)

    duplicates_tracked = tracked_data.get('duplicates_tracked', {}) if isinstance(tracked_data, dict) else {}
    duplicates_all = all_data.get('duplicates_all', {}) if isinstance(all_data, dict) else {}

    # merge keys
    all_hashes = set(duplicates_tracked.keys()) | set(duplicates_all.keys())

    # get git-tracked list
    tracked_list = set(run_git_ls(repo_root))

    move_map = {}
    moved = {}
    skipped = []
    updated_files = []

    for h in all_hashes:
        # gather unique relative paths
        paths = set()
        paths.update(duplicates_all.get(h, []))
        paths.update(duplicates_tracked.get(h, []))
        paths = sorted(paths)
        if len(paths) <= 1:
            continue

        # choose canonical: prefer non-archived, then tracked, then shortest path
        def score(rel):
            rel_norm = rel.replace('\\', '/')
            not_arch = 1 if not is_archived(rel_norm) else 0
            tracked_flag = 1 if rel in tracked_list else 0
            return (not_arch, tracked_flag, -len(rel_norm))

        canonical = max(paths, key=score)

        for rel in paths:
            if rel == canonical:
                continue
            src = os.path.join(repo_root, rel)
            if not os.path.exists(src):
                skipped.append({'src': rel, 'reason': 'missing'})
                continue

            # destination under duplicates_by_hash/<hash>/<original_rel>
            dst_rel = os.path.join('repo_admin', 'reorg_archives', 'duplicates_by_hash', h, rel)
            dst = os.path.join(repo_root, dst_rel)

            try:
                if args.dry_run:
                    moved_rel = dst_rel.replace('\\', '/')
                    moved[rel] = moved_rel
                else:
                    ensure_parent(dst)
                    final_dst = safe_move(src, dst)
                    moved_rel = os.path.relpath(final_dst, repo_root).replace('\\', '/')
                    moved[rel] = moved_rel
                    move_map[rel] = moved_rel
            except Exception as e:
                skipped.append({'src': rel, 'error': str(e)})

    # update textual references
    text_exts = set(e.lower() for e in args.text_exts)
    # build replace map: old->new for exact matches (forward slash)
    repl_map = {k.replace('\\','/'): v.replace('\\','/') for k,v in moved.items()}

    for dirpath, dirnames, filenames in os.walk(repo_root):
        norm_dir = os.path.normpath(dirpath)
        if any(norm_dir == os.path.normpath(os.path.join(repo_root, ex)) or norm_dir.startswith(os.path.normpath(os.path.join(repo_root, ex)) + os.sep) for ex in args.exclude):
            continue
        for fn in filenames:
            _, ext = os.path.splitext(fn)
            if ext.lower() not in text_exts:
                continue
            full = os.path.join(dirpath, fn)
            rel_full = os.path.relpath(full, repo_root).replace('\\','/')
            if rel_full in moved:  # file itself moved; skip
                continue
            try:
                with open(full, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
            except Exception:
                continue
            new_content = content
            for old, new in repl_map.items():
                if old in new_content:
                    new_content = new_content.replace(old, new)
                # also replace backslash variants
                old_bs = old.replace('/', '\\')
                new_bs = new.replace('/', '\\')
                if old_bs in new_content:
                    new_content = new_content.replace(old_bs, new_bs)

            if new_content != content:
                if not args.dry_run:
                    try:
                        with open(full, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        updated_files.append(rel_full)
                    except Exception as e:
                        skipped.append({'file': rel_full, 'error': str(e)})
                else:
                    updated_files.append(rel_full)

    summary = {
        'repo_root': repo_root,
        'duplicate_hashes_processed': len(all_hashes),
        'moved_count': len(moved),
        'moved': moved,
        'skipped': skipped,
        'updated_files_count': len(updated_files),
        'updated_files': updated_files,
    }

    # write outputs
    with open(args.out_map, 'w', encoding='utf-8') as fh:
        json.dump(move_map, fh, indent=2)
    with open(args.out_summary, 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)

    print('Summary:')
    print(json.dumps(summary, indent=2))

    # commit & push if requested and not dry-run
    if args.commit and not args.dry_run:
        try:
            subprocess.run(['git', 'add', '-A'], cwd=repo_root, check=True)
            subprocess.run(['git', 'commit', '-m', 'chore(reorg): archive duplicate files by hash and update references (automated)'], cwd=repo_root, check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_root, check=True)
            print('Committed and pushed changes to origin/main')
        except subprocess.CalledProcessError as e:
            print('Git commit/push failed:', str(e))

if __name__ == '__main__':
    main()
