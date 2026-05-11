import os
import json


def main():
    script_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    move_map_path = os.path.join(script_dir, 'move_map.json')
    reorg_summary_path = os.path.join(script_dir, 'reorg_summary.json')
    report_path = os.path.join(script_dir, 'verify_summary.json')

    if not os.path.exists(move_map_path):
        print('move_map.json not found at', move_map_path)
        return

    with open(move_map_path, 'r', encoding='utf-8') as fh:
        move_map = json.load(fh)

    missing_dests = []
    present_sources = []

    for src, dst in move_map.items():
        if not os.path.exists(dst):
            missing_dests.append(dst)
        if os.path.exists(src):
            present_sources.append(src)

    updated_files = []
    if os.path.exists(reorg_summary_path):
        with open(reorg_summary_path, 'r', encoding='utf-8') as fh:
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
