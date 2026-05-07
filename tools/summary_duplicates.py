"""
Quick summary scanner: prints counts and a few example duplicate groups.
"""
from __future__ import annotations
import os
import hashlib
from collections import defaultdict

root = r"c:\Users\rocel\OneDrive\Desktop\MASTER VS CODE PROJECT TSELUCA"


def iter_files(root: str):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(dirpath, f)


def sha256_file(path: str, chunk_size: int = 1024 * 1024) -> str | None:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(chunk_size), b""):
                h.update(chunk)
    except Exception:
        return None
    return h.hexdigest()


names = defaultdict(list)
sizes = defaultdict(list)
count = 0

for p in iter_files(root):
    count += 1
    names[os.path.basename(p)].append(p)
    try:
        sizes[os.path.getsize(p)].append(p)
    except Exception:
        pass

print(f"Scanned files: {count}")

dup_names = {n: ps for n, ps in names.items() if len(ps) > 1}
print(f"Duplicate filename groups: {len(dup_names)}")
if dup_names:
    for name, ps in list(dup_names.items())[:20]:
        print(f"{name} -> {len(ps)}")
        for q in ps[:5]:
            print("   ", q)

# Find duplicate contents by first grouping by size to avoid hashing unique-size files
dup_content = {}
for size, ps in sizes.items():
    if len(ps) <= 1:
        continue
    hashes = defaultdict(list)
    for p in ps:
        h = sha256_file(p)
        if h:
            hashes[h].append(p)
    for h, pl in hashes.items():
        if len(pl) > 1:
            dup_content[h] = pl

print(f"Duplicate content groups: {len(dup_content)}")
if dup_content:
    for h, pl in list(dup_content.items())[:20]:
        print(f"hash {h} count {len(pl)}")
        for q in pl[:5]:
            print("   ", q)

if not dup_names and not dup_content:
    print("No duplicates found.")
