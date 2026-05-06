#!/usr/bin/env python3
import os
import json
import time
import shutil


def norm_rel(path, repo_root):
    if not path:
        return path
    if os.path.isabs(path):
        try:
            rel = os.path.relpath(path, repo_root)
        except Exception:
            rel = path
    else:
        rel = path
    return rel.replace('\\', '/')


def load_json(p):
    if not os.path.exists(p):
        return {}
    with open(p, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def main():
    script_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    move_map_path = os.path.join(script_dir, 'move_map.json')
    archive_move_map_path = os.path.join(script_dir, 'archive_move_map.json')

    if not os.path.exists(move_map_path):
        print('No move_map.json found; aborting.')
        return

    move_map = load_json(move_map_path)
    archive_move_map = load_json(archive_move_map_path)

    # normalize archive map keys
    archive_norm = {}
    for k, v in archive_move_map.items():
        k_norm = k.replace('\\', '/').lstrip('./')
        archive_norm[k_norm] = v.replace('\\', '/')

    merged = {}
    skipped = []
    removed_venv = []

    for src, dst in move_map.items():
        src_rel = norm_rel(src, repo_root)
        dst_rel = norm_rel(dst, repo_root)

        # skip venv-related entries
        if any(part == '.venv' for part in src_rel.split('/')) or any(part == '.venv' for part in dst_rel.split('/')):
            removed_venv.append((src_rel, dst_rel))
            continue

        # prefer archive_by_hash mapping if present
        final_dst = None
        if dst_rel in archive_norm:
            final_dst = archive_norm[dst_rel]
        else:
            # check destination existence
            abs_dst = dst if os.path.isabs(dst) else os.path.join(repo_root, dst_rel)
            if os.path.exists(abs_dst):
                final_dst = dst_rel
            else:
                skipped.append((src_rel, dst_rel))
                continue

        # store normalized relative mapping
        merged[src_rel] = final_dst

    # backup original
    ts = time.strftime('%Y%m%d%H%M%S')
    backup_path = move_map_path + '.bak-' + ts
    shutil.copy2(move_map_path, backup_path)

    # write merged map to both move_map.json and move_map_merged.json
    with open(os.path.join(script_dir, 'move_map_merged.json'), 'w', encoding='utf-8') as fh:
        json.dump(merged, fh, indent=2)

    with open(move_map_path, 'w', encoding='utf-8') as fh:
        json.dump(merged, fh, indent=2)

    print(json.dumps({
        'original_count': len(move_map),
        'merged_count': len(merged),
        'skipped_count': len(skipped),
        'removed_venv_count': len(removed_venv),
        'backup': os.path.relpath(backup_path, repo_root).replace('\\','/')
    }, indent=2))


if __name__ == '__main__':
    main()
