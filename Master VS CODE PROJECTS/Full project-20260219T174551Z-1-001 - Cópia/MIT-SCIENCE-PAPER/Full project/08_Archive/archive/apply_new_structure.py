#!/usr/bin/env python3
"""
Apply new folder structure: divide project into greater, specified folders.
Run from: Full project/
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
LOG = []

def log(msg):
    LOG.append(msg)
    print(msg)

def move_dir(src, dest):
    """Move directory src to dest (dest is path under ROOT)."""
    s, d = ROOT / src, ROOT / dest
    if not s.exists():
        log(f"SKIP (not found): {src}")
        return False
    if d.exists():
        log(f"SKIP (exists): {dest}")
        return False
    try:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(s), str(d))
        log(f"MOVED: {src} -> {dest}")
        return True
    except Exception as e:
        log(f"ERROR: {src} -> {dest}: {e}")
        return False

def main():
    log("=" * 60)
    log("Applying new folder structure (greater + specified folders)")
    log("=" * 60)

    # 1. Create 01_Science: manuscript + presentations
    log("\n--- 01_Science ---")
    move_dir("manuscript", "01_Science/manuscript")
    move_dir("presentations", "01_Science/presentations")

    # 2. Create 02_Code: move Coding parts/geesp-angola to 02_Code/geesp-angola
    log("\n--- 02_Code ---")
    move_dir("Coding parts/geesp-angola", "02_Code/geesp-angola")
    # Remove empty "Coding parts" if present
    cp = ROOT / "Coding parts"
    if cp.exists() and not any(cp.iterdir()):
        cp.rmdir()
        log("REMOVED empty: Coding parts/")

    # 3. Create 03_Documentation: ROOT_DOCS, docs, PROJECT_MANAGEMENT, support
    log("\n--- 03_Documentation ---")
    move_dir("ROOT_DOCS", "03_Documentation/navigation")
    move_dir("docs", "03_Documentation/technical")
    move_dir("PROJECT_MANAGEMENT", "03_Documentation/project_management")
    move_dir("support", "03_Documentation/support")

    # 4. Create 04_Operations: scripts, infrastructure, k8s, ansible, monitoring
    log("\n--- 04_Operations ---")
    move_dir("scripts", "04_Operations/scripts")
    move_dir("infrastructure", "04_Operations/infrastructure")
    move_dir("k8s", "04_Operations/kubernetes")
    move_dir("ansible", "04_Operations/ansible")
    move_dir("monitoring", "04_Operations/monitoring")

    # 5. Create 05_Governance: GOVERNANCE_COMPLIANCE, submissions, funding, planning
    log("\n--- 05_Governance ---")
    move_dir("GOVERNANCE_COMPLIANCE", "05_Governance/compliance")
    move_dir("submissions", "05_Governance/submissions")
    move_dir("funding", "05_Governance/funding")
    move_dir("planning", "05_Governance/planning")

    # 6. Create 06_Translations: translations -> 06_Translations
    log("\n--- 06_Translations ---")
    move_dir("translations", "06_Translations/translations")

    # 7. Create 07_Data
    log("\n--- 07_Data ---")
    move_dir("data", "07_Data/data")

    # 8. Create 08_Archive
    log("\n--- 08_Archive ---")
    move_dir("ARCHIVE", "08_Archive/archive")

    log("\n" + "=" * 60)
    log("Done. Summary:")
    log(f"  Moves: {len([x for x in LOG if x.startswith('MOVED')])}")
    (ROOT / "STRUCTURE_CHANGE_LOG.txt").write_text("\n".join(LOG), encoding="utf-8")
    log(f"  Log: STRUCTURE_CHANGE_LOG.txt")

if __name__ == "__main__":
    main()
