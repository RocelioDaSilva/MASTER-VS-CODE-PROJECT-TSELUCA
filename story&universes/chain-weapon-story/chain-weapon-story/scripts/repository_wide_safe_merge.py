#!/usr/bin/env python3
"""Repository-wide non-destructive merge generator.

This script does NOT modify source files. It scans for duplicate basenames,
then writes merged artifacts that preserve full contents of every source.

Usage:
  python scripts/repository_wide_safe_merge.py
  python scripts/repository_wide_safe_merge.py --root . --out outputs/repo-merge-2026-04-18
"""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import os
from collections import defaultdict
from pathlib import Path


DEFAULT_EXTENSIONS = {".md", ".txt"}
IGNORE_DIR_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".smart-env",
}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_candidate_files(root: Path, exts: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in IGNORE_DIR_NAMES and not d.startswith(".")
        ]

        dir_path = Path(dirpath)
        if "outputs" in dir_path.parts and any("repo-merge" in p for p in dir_path.parts):
            continue

        for name in filenames:
            path = dir_path / name
            if path.suffix.lower() in exts:
                yield path


def sanitize_name(name: str) -> str:
    safe = []
    for c in name:
        if c.isalnum() or c in {"-", "_", "."}:
            safe.append(c)
        else:
            safe.append("_")
    return "".join(safe)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--out",
        default=f"outputs/repo-merge-{datetime.date.today().isoformat()}",
        help="Output directory for merged artifacts",
    )
    parser.add_argument(
        "--extensions",
        default=".md,.txt",
        help="Comma-separated extension list, e.g. .md,.txt",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_dir = Path(args.out).resolve()
    merged_dir = out_dir / "merged"
    merged_dir.mkdir(parents=True, exist_ok=True)

    exts = {e.strip().lower() for e in args.extensions.split(",") if e.strip()}
    if not exts:
        exts = DEFAULT_EXTENSIONS

    groups: dict[str, list[Path]] = defaultdict(list)
    for path in iter_candidate_files(root, exts):
        groups[path.name.lower()].append(path)

    duplicate_groups = {
        basename: sorted(paths)
        for basename, paths in groups.items()
        if len(paths) > 1
    }

    csv_path = out_dir / "duplicate-groups.csv"
    out_dir.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["basename", "count", "paths"])
        for basename in sorted(duplicate_groups.keys()):
            paths = duplicate_groups[basename]
            rel_paths = [str(p.relative_to(root)).replace("\\", "/") for p in paths]
            writer.writerow([basename, len(paths), "|".join(rel_paths)])

    manifest_path = out_dir / "MERGE-MANIFEST.md"
    with manifest_path.open("w", encoding="utf-8") as mf:
        mf.write("# Repository-Wide Safe Merge Manifest\n\n")
        mf.write("- Mode: non-destructive\n")
        mf.write("- Source files modified: 0\n")
        mf.write(f"- Duplicate groups found: {len(duplicate_groups)}\n")
        mf.write(f"- Extensions scanned: {', '.join(sorted(exts))}\n")
        mf.write(f"- Generated: {datetime.datetime.now().isoformat(timespec='seconds')}\n\n")
        mf.write("## Groups\n\n")

        if not duplicate_groups:
            mf.write("No duplicate basename groups were found for selected extensions.\n")
        else:
            mf.write("| # | Basename | Files | Merged Artifact |\n")
            mf.write("|---|----------|-------|-----------------|\n")

        for idx, basename in enumerate(sorted(duplicate_groups.keys()), start=1):
            paths = duplicate_groups[basename]
            artifact_name = f"{idx:03d}-{sanitize_name(basename)}.merged.md"
            artifact_path = merged_dir / artifact_name

            with artifact_path.open("w", encoding="utf-8") as out:
                out.write(f"# Merged Artifact: {basename}\n\n")
                out.write("This file preserves all source content exactly.\n\n")
                out.write("## Sources\n\n")
                for p in paths:
                    rel = str(p.relative_to(root)).replace("\\", "/")
                    out.write(f"- {rel} (sha256: {file_hash(p)})\n")

                out.write("\n---\n\n")

                for p in paths:
                    rel = str(p.relative_to(root)).replace("\\", "/")
                    out.write(f"## Source: {rel}\n\n")
                    text = p.read_text(encoding="utf-8", errors="replace")
                    out.write(text)
                    if not text.endswith("\n"):
                        out.write("\n")
                    out.write("\n---\n\n")

            mf.write(
                f"| {idx} | {basename} | {len(paths)} | merged/{artifact_name} |\n"
            )

    print(f"Root scanned: {root}")
    print(f"Output directory: {out_dir}")
    print(f"Duplicate groups: {len(duplicate_groups)}")
    print(f"Manifest: {manifest_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
