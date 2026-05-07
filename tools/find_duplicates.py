"""
Scan workspace for duplicate filenames and identical files by SHA256 hash.
Saves results to `duplicate_filenames.txt` and `duplicate_contents.txt` in the tools folder.
Usage: run from project root or pass --path <root_path>
"""
from __future__ import annotations
import argparse
import hashlib
import os
from collections import defaultdict


def iter_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(dirpath, f)


def sha256_file(path: str, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(chunk_size), b""):
                h.update(chunk)
    except Exception:
        return ""
    return h.hexdigest()


def find_duplicate_filenames(root: str):
    names = defaultdict(list)
    for path in iter_files(root):
        names[os.path.basename(path)].append(path)
    return {name: paths for name, paths in names.items() if len(paths) > 1}


def find_duplicate_contents(root: str):
    hashes = defaultdict(list)
    for path in iter_files(root):
        h = sha256_file(path)
        if not h:
            continue
        hashes[h].append(path)
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", default=".", help="Root path to scan")
    args = parser.parse_args()
    root = os.path.abspath(args.path)

    print(f"Scanning {root} ...")
    dup_names = find_duplicate_filenames(root)
    dup_content = find_duplicate_contents(root)

    tools_dir = os.path.join(root, "tools")
    os.makedirs(tools_dir, exist_ok=True)

    fnames = os.path.join(tools_dir, "duplicate_filenames.txt")
    fcont = os.path.join(tools_dir, "duplicate_contents.txt")

    with open(fnames, "w", encoding="utf-8") as fh:
        if not dup_names:
            fh.write("No duplicate filenames found.\n")
        else:
            for name, paths in sorted(dup_names.items()):
                fh.write(f"{name}\n")
                for p in paths:
                    fh.write(f"    {p}\n")
                fh.write("\n")

    with open(fcont, "w", encoding="utf-8") as fh:
        if not dup_content:
            fh.write("No duplicate file contents found.\n")
        else:
            for h, paths in sorted(dup_content.items()):
                fh.write(f"hash: {h}\n")
                for p in paths:
                    fh.write(f"    {p}\n")
                fh.write("\n")

    print("Finished. Results written to:")
    print(f"  {fnames}")
    print(f"  {fcont}")


if __name__ == "__main__":
    main()
