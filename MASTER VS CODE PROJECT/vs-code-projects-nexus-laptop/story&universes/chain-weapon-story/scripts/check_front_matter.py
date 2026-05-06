#!/usr/bin/env python3
"""
Check Markdown front-matter presence and required keys.

Usage:
  python scripts/check_front_matter.py --path <file_or_dir> [--strict] [--extra-keys pov age]

Returns exit code 0 when all checked files pass; 2 when failures present.
"""
import os
import re
import sys
import argparse
from typing import Optional

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def parse_front_matter(text: str) -> Optional[set]:
    m = FM_RE.match(text)
    if not m:
        return None
    fm_text = m.group(1)
    keys = set()
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k = line.split(':', 1)[0].strip().lower()
            keys.add(k)
    return keys


def check_file(path: str, strict: bool = False, extra_required=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return False, f"read error: {e}"
    keys = parse_front_matter(text)
    if keys is None:
        return False, "missing front-matter"
    # Base requirements: title (or name) + status
    required = {'title', 'status'}
    # 'updated' and any extras only required in strict mode
    strict_extra = {'updated'}
    if strict:
        required = required | strict_extra
        if extra_required:
            required = required | set([k.lower() for k in extra_required])
    # Accept 'name' as an alias for 'title' (character profile format)
    if 'name' in keys:
        keys = keys | {'title'}
    missing = required - keys
    if missing:
        return False, "missing keys: " + ",".join(sorted(missing))
    return True, None


def iter_md_files(root: str):
    if os.path.isfile(root):
        if root.lower().endswith('.md'):
            yield root
        return
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith('.md'):
                yield os.path.join(dirpath, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='File or directory to check')
    parser.add_argument('--strict', action='store_true', help='Require extra keys (pov, age, chapter_number)')
    parser.add_argument('--extra-keys', nargs='*', help='Additional required keys (space-separated)')
    args = parser.parse_args()

    extra = args.extra_keys or []
    failures = []
    for p in iter_md_files(args.path):
        ok, msg = check_file(p, strict=args.strict, extra_required=extra)
        if not ok:
            failures.append((p, msg))

    if failures:
        print('Files failing front-matter checks:')
        for p, msg in failures:
            print(p + ': ' + msg)
        sys.exit(2)

    print('All checked files passed front-matter requirements.')
    sys.exit(0)


if __name__ == '__main__':
    main()
