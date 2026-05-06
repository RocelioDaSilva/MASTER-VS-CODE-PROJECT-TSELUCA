#!/usr/bin/env python3
"""Update REPOSITORY_HEALTH_STATUS.md for Phase 7 consolidation"""

import re
from pathlib import Path

# Get paths
script_dir = Path(__file__).resolve().parent
repo_root = script_dir.parent.parent
filepath = repo_root / "repo_admin" / "reports" / "REPOSITORY_HEALTH_STATUS.md"

# Read file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update date
content = content.replace(
    '**Date:** April 17, 2026',
    '**Date:** April 18, 2026 (Updated post-Phase 7 Consolidation)'
)

# Update status
content = content.replace(
    '**Status:** ✅ CRITICAL ISSUES ADDRESSED',
    '**Status:** ✅ CRITICAL ISSUES RESOLVED (Phase 7 Consolidation Complete)'
)

# Update canonical manuscript path
content = content.replace(
    'Declared canonical manuscript: `Full project/01_Science/manuscript/SOL.tex`',
    'Declared canonical manuscript: `manuscript_unified/science_manuscript/SOL.tex` (Phase 7 Consolidation)'
)

# Update canonical bibliography path
content = content.replace(
    'Declared canonical bibliography: `Full project/01_Science/manuscript/referencias.bib`',
    'Declared canonical bibliography: `manuscript_unified/science_manuscript/referencias.bib` (Phase 7 Consolidation)'
)

# Add Phase 7 cleanup note for artifacts
content = content.replace(
    '**Verification Performed:**',
    '**Phase 7 Cleanup:** All 72 artifacts removed and cleaned in Phase 7 consolidation (commit 1b2809c)\n\n**Verification Performed:**'
)

# Update final report line
content = content.replace(
    '**Status:** Report Complete\n**Date:** April 17, 2026',
    '**Status:** Report Complete - Phase 7 Consolidation\n**Date:** April 18, 2026'
)

# Update team instruction for single source
content = content.replace(
    'Team knows: only edit `01_Science/manuscript/SOL.tex`',
    'Team knows: only edit `manuscript_unified/science_manuscript/SOL.tex`'
)

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ REPOSITORY_HEALTH_STATUS.md updated for Phase 7 consolidation')
