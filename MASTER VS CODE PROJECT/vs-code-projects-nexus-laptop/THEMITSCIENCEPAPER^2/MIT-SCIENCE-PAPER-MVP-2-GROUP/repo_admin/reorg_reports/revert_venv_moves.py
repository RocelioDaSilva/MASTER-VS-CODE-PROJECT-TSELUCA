#!/usr/bin/env python3
import json
import os
import shutil
import time
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOVE_MAP = HERE / "move_map.json"
if not MOVE_MAP.exists():
    print("move_map.json not found at", MOVE_MAP)
    sys.exit(1)

with MOVE_MAP.open("r", encoding="utf-8") as f:
    move_map = json.load(f)

reverted = {}
skipped = {}

for old_raw, new_raw in move_map.items():
    old = Path(old_raw)
    new = Path(new_raw)

    # Only target entries that are inside a .venv folder
    if ".venv" not in [p for p in old.parts]:
        continue

    if not new.exists():
        skipped[str(old)] = "archived missing"
        continue

    try:
        old_parent = old.parent
        old_parent.mkdir(parents=True, exist_ok=True)

        if old.exists():
            # preserve whatever is currently at the original location
            conflict_backup = old.with_name(old.name + ".reorg_conflict." + time.strftime("%Y%m%d%H%M%S"))
            shutil.move(str(old), str(conflict_backup))
            skipped[str(old)] = f"original existed; moved to {conflict_backup}"

        shutil.move(str(new), str(old))
        reverted[str(old)] = str(new)
    except Exception as e:
        skipped[str(old)] = f"move failed: {e}"

SUMMARY = {
    "reverted_count": len(reverted),
    "reverted": reverted,
    "skipped_count": len(skipped),
    "skipped": skipped,
}

summary_path = HERE / "revert_summary.json"
with summary_path.open("w", encoding="utf-8") as f:
    json.dump(SUMMARY, f, indent=2)

print(f"Reverted {len(reverted)} files. Summary written to {summary_path}")
if skipped:
    print(f"Skipped {len(skipped)} entries. See {summary_path} for details.")
