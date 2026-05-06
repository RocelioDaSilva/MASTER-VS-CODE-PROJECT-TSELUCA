import os
import shutil
from pathlib import Path

repo_root = Path(r"C:\Users\PCGAME\Desktop\story&universes\chain-weapon-story")
chapters_dir = repo_root / "manuscript" / "Chapters"
doc_archive = repo_root / "documentation" / "archive"
chars_dir = repo_root / "manuscript" / "characters"
tier2 = chars_dir / "TIER-SECONDARY"

doc_archive.mkdir(parents=True, exist_ok=True)
tier2.mkdir(parents=True, exist_ok=True)

# 1. Move conflicting chapters
moves = [
    (chapters_dir / "04-Frostfang-Incident.md", doc_archive / "04-Frostfang-Incident.md"),
    (chapters_dir / "04-Frostfang-Incident-Expanded.md", doc_archive / "04-Frostfang-Incident-Expanded.md"),
    (chapters_dir / "05-Exam-Sabotage.md", doc_archive / "05-Exam-Sabotage.md"),
    (chapters_dir / "30-Final-Border-Stand.md", doc_archive / "30-Final-Border-Stand.md"),
    (chapters_dir / "30-Final-Border-Stand-Expanded.md", doc_archive / "30-Final-Border-Stand-Expanded.md"),
    (repo_root / "documentation" / "41-44-War-Operations-Strategic-Escalations.md", doc_archive / "41-44-War-Operations-Strategic-Escalations.md"),
    (repo_root / "manuscript" / "characters" / "KAELEN-THORNWOOD.md", doc_archive / "KAELEN-THORNWOOD.md"),
]
for src, dst in moves:
    if src.exists():
        shutil.move(src, dst)

# 2. Delete .fm.bak files
for p in repo_root.rglob("*.fm.bak"):
    try:
        p.unlink()
    except:
        pass

# 3. Create/update stubs
(tier2 / "SOREN-profile.md").write_text("# Soren\nArchivist at the Covenant Academy.")
(tier2 / "MASTER-THOLEN-profile.md").write_text("# Master Tholen\nAcademy Librarian.")
(tier2 / "PIETER-VAN-DER-BERG-profile.md").write_text("# Pieter van der Berg\nExpanded profile.")
(tier2 / "TUPAC-profile.md").write_text("# Tupac\nExpanded profile.")

print("Cleanup done.")
