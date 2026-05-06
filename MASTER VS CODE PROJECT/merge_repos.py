"""
Merge vs-code-projects-nexus-desktop and vs-code-projects-nexus-laptop
into MASTER-VS-CODE-PROJECT-TSELUCA.
Rules:
  - Copy all desktop files first
  - For each laptop file:
      * Not in dest -> copy it
      * Same path, same hash -> skip (duplicate)
      * Same path, different hash -> copy with _LAPTOP suffix
Excludes: .git/, node_modules/, __pycache__, *.pyc (regeneratable artifacts)
"""

import os
import shutil
import hashlib
import sys

BASE     = r"C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT"
DESKTOP  = os.path.join(BASE, "vs-code-projects-nexus-desktop")
LAPTOP   = os.path.join(BASE, "vs-code-projects-nexus-laptop")
DEST     = os.path.join(BASE, "MASTER-VS-CODE-PROJECT-TSELUCA")

# Folders/files to skip during copy
SKIP_DIRS  = {".git", "node_modules", "__pycache__", ".mypy_cache",
              ".pytest_cache", ".smart-env", "venv", ".venv", "env"}
SKIP_EXTS  = {".pyc", ".pyd", ".pyo"}
SKIP_FILES = {"desktop.ini", "Thumbs.db"}

def should_skip_dir(dirname):
    return dirname in SKIP_DIRS

def should_skip_file(filename):
    if filename in SKIP_FILES:
        return True
    _, ext = os.path.splitext(filename)
    return ext.lower() in SKIP_EXTS

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

def walk_repo(repo_root):
    """Yield (abs_path, relative_path) for all non-excluded files."""
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune excluded dirs in-place
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for fname in filenames:
            if should_skip_file(fname):
                continue
            abs_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(abs_path, repo_root)
            yield abs_path, rel_path

# ── Step 1: Copy all desktop files ──────────────────────────────────────────
print("[1/2] Copying desktop files...")
desktop_count = 0
for src, rel in walk_repo(DESKTOP):
    dst = os.path.join(DEST, rel)
    safe_copy(src, dst)
    desktop_count += 1
    if desktop_count % 1000 == 0:
        print(f"  Desktop: {desktop_count} files copied...", flush=True)

print(f"  Desktop done: {desktop_count} files")

# ── Step 2: Merge laptop files ───────────────────────────────────────────────
print("\n[2/2] Merging laptop files...")
copied = 0
skipped = 0
conflicts = 0
total = 0

for src, rel in walk_repo(LAPTOP):
    total += 1
    if total % 5000 == 0:
        print(f"  Laptop: {total} processed | new:{copied} skip:{skipped} conflict:{conflicts}", flush=True)

    dst = os.path.join(DEST, rel)

    if not os.path.exists(dst):
        safe_copy(src, dst)
        copied += 1
    else:
        # Same path exists – compare content
        dst_size = os.path.getsize(dst)
        src_size = os.path.getsize(src)
        if dst_size == src_size and md5(dst) == md5(src):
            skipped += 1  # Completely identical – keep one copy
        else:
            # Different content – keep both
            base, ext = os.path.splitext(dst)
            conflict_dst = f"{base}_LAPTOP{ext}"
            n = 1
            while os.path.exists(conflict_dst):
                conflict_dst = f"{base}_LAPTOP_{n}{ext}"
                n += 1
            safe_copy(src, conflict_dst)
            conflicts += 1

print(f"\n{'='*50}")
print(f"MERGE COMPLETE")
print(f"{'='*50}")
print(f"Desktop files copied      : {desktop_count}")
print(f"Laptop files processed    : {total}")
print(f"  New (unique) files added: {copied}")
print(f"  Identical duplicates    : {skipped} (kept 1 copy)")
print(f"  Conflicts (kept both)   : {conflicts}")
print(f"\nDestination: {DEST}")
print(f"\nNote: node_modules/, __pycache__, .pyc files were excluded")
print(f"(run 'npm install' / 'pip install' inside each project to restore them)")
