#!/usr/bin/env python3
"""
UNIFIED PIPELINE ORCHESTRATOR — Single entry point for all data and docs processing

This is the DEFINITIVE entry point for the entire repository workflow.
DO NOT run individual scripts directly — use this orchestrator instead.

Usage:
    python run_pipeline.py data         # rebuild company hierarchy from raw ANPG data
    python run_pipeline.py docs         # rebuild documentation (merge, fix links, cross-link)
    python run_pipeline.py all          # run both pipelines in order (default)
    python run_pipeline.py --help
    python run_pipeline.py --dry-run    # preview steps without executing

Data Pipeline (7 steps):
  1. Extract KPIs for LaTeX generation
  2. Reorganize cross-references
  3. Generate hierarchy directory structure
  4. Rename files to include company names
  5. Fill company profiles with BI reports & curated data
  6. Add peer backlinks between companies
  7. Export to CSV and Excel formats

Docs Pipeline (3 steps):
  1. Merge overlapping documentation files
  2. Fix and validate SUMMARY.md
  3. Cross-link the entire repository

Default: run both pipelines ('all')
"""

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pipeline")

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
DATA_PROC = ROOT / "data" / "processed"          # data-only dir (no scripts)

# ══════════════════════════════════════════════════════════════════════════════
# DATA PROCESSING PIPELINE — Hierarchy Generation & Company Profile Filling
# ══════════════════════════════════════════════════════════════════════════════
# fmt: off
DATA_PIPELINE = [
    ("Step 1: Extract KPIs for LaTeX",
     [sys.executable, str(SCRIPTS / "preprocess-anpg-data.py")]),
    
    ("Step 2: Reorganise cross-references",
     [sys.executable, str(SCRIPTS / "reorganize_crossref.py")]),
    
    ("Step 3: Generate hierarchy directory structure",
     [sys.executable, str(SCRIPTS / "generate_hierarchy.py")]),
    
    ("Step 4: Rename files to include company names",
     [sys.executable, str(SCRIPTS / "rename_files_with_company_names.py")]),
    
    ("Step 5: Fill company profiles with BI reports & curated data (MERGED SCRIPT)",
     [sys.executable, str(SCRIPTS / "fill_company_info.py"), "--mode", "full"]),
    
    ("Step 6: Add peer backlinks between companies in same niche",
     [sys.executable, str(SCRIPTS / "add_backlinks.py")]),
    
    ("Step 7: Export processed hierarchy to CSV & Excel",
     [sys.executable, str(SCRIPTS / "export_hierarchy_to_csv_excel.py")]),
]

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION PIPELINE — Consolidation, Cross-linking & Verification
# ══════════════════════════════════════════════════════════════════════════════
DOCS_PIPELINE = [
    ("Step 1: Merge overlapping documentation files",
     [sys.executable, str(SCRIPTS / "merge_docs.py")]),
    
    ("Step 2: Fix and validate SUMMARY.md structure",
     [sys.executable, str(SCRIPTS / "fix_summary.py")]),
    
    ("Step 3: Cross-link entire repository (Obsidian compatible)",
     [sys.executable, str(SCRIPTS / "crosslink_repo.py")]),
]
# fmt: on


def run_steps(steps: list, label: str, dry_run: bool = False) -> bool:
    """Execute a pipeline of numbered steps with timing and logging.

    Returns True if all steps succeeded, False on first failure.
    """
    log.info("=" * 72)
    log.info("  ▶ %s", label)
    log.info("=" * 72)

    if dry_run:
        for name, cmd in steps:
            log.info("[DRY RUN] %s", name)
            log.info("    → %s", " ".join(cmd))
        return True

    t0 = time.perf_counter()
    for i, (name, cmd) in enumerate(steps, 1):
        log.info("%s", name)
        log.info("  Command: %s", " ".join(cmd))

        # Validate script exists before running
        script_path = Path(cmd[1]) if len(cmd) > 1 else None
        if script_path and not script_path.exists():
            log.error("  ✗ Script not found: %s", script_path)
            return False

        result = subprocess.run(cmd, cwd=str(ROOT))
        if result.returncode != 0:
            log.error("!" * 72)
            log.error("  ✗ FAILED at %s", name)
            log.error("  Exit code: %d", result.returncode)
            log.error("!" * 72)
            return False

    elapsed = time.perf_counter() - t0
    log.info("✓ %s complete (%.1fs).\n", label, elapsed)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="UNIFIED PIPELINE ORCHESTRATOR — Run all data & docs processing\n"
                    "(This is the ONLY entry point for the repository workflow)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python run_pipeline.py all        # Run everything (default)\n"
               "  python run_pipeline.py data       # Only data pipeline\n"
               "  python run_pipeline.py docs       # Only docs pipeline\n"
               "  python run_pipeline.py --dry-run  # Preview steps\n",
    )
    parser.add_argument(
        "target",
        nargs="?",
        choices=["data", "docs", "all"],
        default="all",
        help="Pipeline to run: data, docs, or all (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show steps without executing",
    )
    args = parser.parse_args()

    targets = {
        "data": [(DATA_PIPELINE, "📊 DATA PIPELINE (Company Hierarchy Processing)")],
        "docs": [(DOCS_PIPELINE, "📚 DOCS PIPELINE (Documentation Consolidation)")],
        "all":  [(DATA_PIPELINE, "📊 DATA PIPELINE (Company Hierarchy Processing)"),
                 (DOCS_PIPELINE, "📚 DOCS PIPELINE (Documentation Consolidation)")],
    }

    log.info("=" * 72)
    log.info("  UNIFIED PIPELINE ORCHESTRATOR")
    log.info("  Repository Root: %s", ROOT)
    log.info("=" * 72)
    
    for steps, label in targets[args.target]:
        if not run_steps(steps, label, dry_run=args.dry_run):
            sys.exit(1)
    
    log.info("=" * 72)
    log.info("  ✓ ALL PIPELINES COMPLETE")
    log.info("=" * 72)


if __name__ == "__main__":
    main()
