import os, json, shutil, datetime, re

ROOT = r"c:\Users\PCGAME\Desktop\Master VS CODE PROJECTS\THEMITSCIENCEPAPER^2\MIT-SCIENCE-PAPER-MVP-2-GROUP"
DUP_JSON = os.path.join(ROOT, 'repo_admin', 'reorg_reports', 'duplicates.json')
OUT_DIR = os.path.join(ROOT, 'repo_admin', 'reorg_archives', 'duplicates')

import os
import json
import shutil
import datetime
import argparse
from pathlib import Path

ROOT = r"c:\Users\PCGAME\Desktop\Master VS CODE PROJECTS\THEMITSCIENCEPAPER^2\MIT-SCIENCE-PAPER-MVP-2-GROUP"
DUP_JSON = os.path.join(ROOT, 'repo_admin', 'reorg_reports', 'duplicates.json')
OUT_DIR = os.path.join(ROOT, 'repo_admin', 'reorg_archives', 'duplicates')

LEGACY_KEYWORDS = [
    '_old_information',
    'legacy',
    '08_Archive',
    'archive_snapshots',
    'archive',
    'ARCHIVE',
    'ARCHIVED',
    'deprecated',
    'backups',
    'OLD_VERSIONS'
]

PRIORITY = [
    'manuscript_unified',
    'code_unified',
    'MIT-SCIENCE-PAPER\\Full project',
    'manuscript_unified\\science_manuscript'
]

TEXT_EXTS = {'.md', '.tex', '.py', '.json', '.yml', '.yaml', '.txt', '.html', '.htm', '.ts', '.tsx', '.js', '.rst'}


def parse_args():
    p = argparse.ArgumentParser(description='Archive legacy duplicate files and update references')
    p.add_argument('--dry-run', action='store_true', help='Do not move files; write a dry-run summary instead')
    p.add_argument('--exclude', '-e', nargs='*', default=['.venv', 'node_modules', '.git', 'repo_admin', 'reorg_archives'], help='Directory names or path fragments to exclude')
    p.add_argument('--dup-json', default=DUP_JSON, help='Path to duplicates.json')
    p.add_argument('--out-dir', default=OUT_DIR, help='Archive output directory')
    return p.parse_args()


def matches_exclude(path_str, excludes):
    if not path_str:
        return False
    p = Path(path_str)
    parts = [part.lower() for part in p.parts]
    lower = str(p).lower()
    for ex in excludes:
        ex_l = ex.strip().lower()
        if not ex_l:
            continue
        if ex_l in parts:
            return True
        if ex_l in lower:
            return True
    return False


def is_legacy(path):
    low = path.lower()
    return any(k.lower() in low for k in LEGACY_KEYWORDS)


def main():
    args = parse_args()
    DUP = args.dup_json
    OUT = args.out_dir
    excludes = args.exclude or []

    if not os.path.exists(DUP):
        print('duplicates.json not found at', DUP)
        return

    with open(DUP, 'r', encoding='utf-8') as fh:
        dup_map = json.load(fh)

    move_map = {}
    proposed_move_map = {}
    updated_files = set()
    would_update_files = set()

    # Only create OUT when actually applying changes
    if not args.dry_run:
        os.makedirs(OUT, exist_ok=True)

    for name, paths in dup_map.items():
        paths = [os.path.normpath(p) for p in paths]
        # filter out excluded paths
        paths = [p for p in paths if not matches_exclude(p, excludes)]
        if len(paths) < 2:
            continue

        # Partition
        legacy = [p for p in paths if is_legacy(p)]
        active = [p for p in paths if p not in legacy]

        # If there are legacy copies and at least one active canonical, move legacy ones
        if legacy and active:
            # choose canonical among active by priority
            canonical = None
            for p in active:
                for pr in PRIORITY:
                    if pr.lower() in p.lower():
                        canonical = p
                        break
                if canonical:
                    break
            if not canonical:
                canonical = sorted(active, key=lambda x: len(x))[0]

            for p in legacy:
                # skip anything excluded (double-check)
                if matches_exclude(p, excludes):
                    continue
                rel = os.path.relpath(p, ROOT)
                dest = os.path.normpath(os.path.join(OUT, rel))
                dest_dir = os.path.dirname(dest)
                if args.dry_run:
                    proposed_move_map[p] = dest
                    print(f"Would move: {p} -> {dest}")
                else:
                    os.makedirs(dest_dir, exist_ok=True)
                    if os.path.exists(dest):
                        ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
                        dest = dest + f'.archived.{ts}'
                    try:
                        shutil.move(p, dest)
                        move_map[p] = dest
                        print(f"Moved: {p} -> {dest}")
                    except Exception as e:
                        print(f"Failed to move {p}: {e}")

    # Determine which mapping to use for replacements
    mapping = proposed_move_map if args.dry_run else move_map

    if mapping:
        replacements = []
        for old, new in mapping.items():
            old_rel = os.path.relpath(old, ROOT).replace('\\', '/')
            new_rel = os.path.relpath(new, ROOT).replace('\\', '/')
            replacements.append((old_rel, new_rel))

        # Walk repository and either simulate or apply text replacements
        for dirpath, dirs, files in os.walk(ROOT):
            # prune excluded dirs from traversal
            dirs[:] = [d for d in dirs if not matches_exclude(os.path.join(dirpath, d), excludes)]
            if matches_exclude(dirpath, excludes):
                continue
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in TEXT_EXTS:
                    continue
                fp = os.path.join(dirpath, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        txt = fh.read()
                except Exception:
                    continue
                new_txt = txt
                for old_rel, new_rel in replacements:
                    new_txt = new_txt.replace(old_rel, new_rel)
                    new_txt = new_txt.replace(old_rel.replace('/', '\\'), new_rel)
                if new_txt != txt:
                    if args.dry_run:
                        would_update_files.add(os.path.relpath(fp, ROOT))
                    else:
                        with open(fp, 'w', encoding='utf-8') as fh:
                            fh.write(new_txt)
                        updated_files.add(os.path.relpath(fp, ROOT))

        # Write appropriate summary
        reports_dir = os.path.join(ROOT, 'repo_admin', 'reorg_reports')
        os.makedirs(reports_dir, exist_ok=True)
        if args.dry_run:
            dry_out = os.path.join(reports_dir, 'dry_run_summary.json')
            summary = {
                'proposed_move_count': len(proposed_move_map),
                'proposed_moves': proposed_move_map,
                'would_update_files': sorted(list(would_update_files)),
                'replacements': replacements
            }
            with open(dry_out, 'w', encoding='utf-8') as fh:
                json.dump(summary, fh, indent=2)
            print('\nDry-run summary written to', dry_out)
        else:
            MAP_OUT = os.path.join(reports_dir, 'move_map.json')
            with open(MAP_OUT, 'w', encoding='utf-8') as fh:
                json.dump(move_map, fh, indent=2)

            summary_out = os.path.join(reports_dir, 'reorg_summary.json')
            summary = {'moved_count': len(move_map), 'moved': move_map, 'updated_files': sorted(list(updated_files))}
            with open(summary_out, 'w', encoding='utf-8') as fh:
                json.dump(summary, fh, indent=2)
            print('\nReorganization summary written to', summary_out)
    else:
        print('No legacy duplicates required moving under current policy (after applying exclusions).')

    print('Done.')


if __name__ == '__main__':
    main()
