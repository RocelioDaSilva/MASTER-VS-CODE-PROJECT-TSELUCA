import os
import json


def main():
    script_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    archive_move_map_path = os.path.join(script_dir, 'archive_move_map.json')
    archive_reorg_summary_path = os.path.join(script_dir, 'archive_reorg_summary.json')
    report_path = os.path.join(script_dir, 'verify_archive_summary.json')

    move_map = {}
    if os.path.exists(archive_move_map_path):
        with open(archive_move_map_path, 'r', encoding='utf-8') as fh:
            move_map = json.load(fh)
    elif os.path.exists(archive_reorg_summary_path):
        with open(archive_reorg_summary_path, 'r', encoding='utf-8') as fh:
            summary = json.load(fh)
            move_map = summary.get('moved', {})
    else:
        print('No archive_move_map.json or archive_reorg_summary.json found.')
        return

    missing_dests = []
    present_sources = []

    for src, dst in move_map.items():
        abs_src = src if os.path.isabs(src) else os.path.join(repo_root, src)
        abs_dst = dst if os.path.isabs(dst) else os.path.join(repo_root, dst)
        if not os.path.exists(abs_dst):
            missing_dests.append(abs_dst)
        if os.path.exists(abs_src):
            present_sources.append(abs_src)

    updated_files = []
    if os.path.exists(archive_reorg_summary_path):
        with open(archive_reorg_summary_path, 'r', encoding='utf-8') as fh:
            summary = json.load(fh)
            updated_files = summary.get('updated_files', [])

    missing_updated_files = []
    for uf in updated_files:
        p = os.path.join(repo_root, uf)
        if not os.path.exists(p):
            missing_updated_files.append(uf)

    report = {
        'move_map_count': len(move_map),
        'missing_destinations_count': len(missing_dests),
        'missing_destinations_sample': missing_dests[:100],
        'present_sources_count': len(present_sources),
        'present_sources_sample': present_sources[:100],
        'updated_files_count': len(updated_files),
        'missing_updated_files': missing_updated_files,
    }

    with open(report_path, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
