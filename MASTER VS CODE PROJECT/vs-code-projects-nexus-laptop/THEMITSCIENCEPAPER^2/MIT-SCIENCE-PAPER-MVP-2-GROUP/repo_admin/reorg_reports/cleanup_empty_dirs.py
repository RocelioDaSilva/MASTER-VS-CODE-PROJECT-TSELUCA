import os
import json
import argparse


def find_root(default=None):
    if default:
        return os.path.abspath(default)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    p = argparse.ArgumentParser(description='Remove empty dirs under repository root (safe).')
    p.add_argument('--root', help='Repository root', default=None)
    p.add_argument('--exclude', nargs='*', default=['.git', '.venv', 'node_modules', 'repo_admin'])
    p.add_argument('--report', help='JSON report path', default=os.path.join(os.path.dirname(__file__), 'cleanup_summary.json'))
    args = p.parse_args()

    repo_root = find_root(args.root)
    excluded = [os.path.normpath(os.path.join(repo_root, e)) for e in args.exclude]

    removed = []
    errors = []

    for dirpath, dirnames, filenames in os.walk(repo_root, topdown=False):
        norm = os.path.normpath(dirpath)
        # skip excluded paths
        if any(norm == ex or norm.startswith(ex + os.sep) for ex in excluded):
            continue
        # don't remove repo root itself
        if norm == os.path.normpath(repo_root):
            continue
        try:
            entries = os.listdir(dirpath)
            if not entries:
                os.rmdir(dirpath)
                removed.append(dirpath)
        except Exception as e:
            errors.append({'dir': dirpath, 'error': str(e)})

    report = {
        'root': repo_root,
        'excluded': args.exclude,
        'removed_count': len(removed),
        'removed': removed,
        'errors': errors,
    }

    with open(args.report, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
