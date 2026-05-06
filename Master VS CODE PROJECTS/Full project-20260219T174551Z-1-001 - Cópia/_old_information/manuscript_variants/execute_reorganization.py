#!/usr/bin/env python3
"""
Comprehensive SOL.tex reorganization script
Extracts sections and reorganizes to IMRAD standard while preserving all content
"""

import re
from pathlib import Path
from datetime import datetime

# Configuration
INPUT_FILE = "SOL.tex"
OUTPUT_FILE = "SOL_HARMONIZED.tex"
BACKUP_FILE = f"SOL_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex"

print("=" * 90)
print(" SOL.TEX HARMONIZATION SCRIPT - REORGANIZATION TO IMRAD + CONSOLIDATION")
print("=" * 90)

# Read original file
print("\n[1/5] Reading original file...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.split('\n')

total_lines = len(lines)
print(f"[OK] Loaded {total_lines} lines")

# Create backup
print("\n[2/5] Creating backup...")
with open(BACKUP_FILE, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[OK] Backup created: {BACKUP_FILE}")

# Section line ranges (from analysis: 89, 107, 166, 489, 652, 776, 1068, 1169, 2743)
sections = {
    'preamble': (0, 88),                    # Lines 1-88: preamble, title, abstract
    'intro': (88, 106),                     # Line 89-106: Introduction  
    'geesp': (106, 165),                    # Line 107-165: GEESP Framework section
    'tipos': (165, 488),                    # Line 166-488: Types of Technologies
    'methodology': (488, 651),              # Line 489-651: Methodology
    'results': (651, 775),                  # Line 652-775: Results
    'discussion': (775, 1067),              # Line 776-1067: Discussion
    'patterns':(1067, 1168),                # Line 1068-1168: Patterns/Comparative
    'logistics': (1168, 2742),              # Line 1169-2742: Logistics/Costs
    'conclusion': (2742, total_lines)       # Line 2743+: Conclusions and rest
}

print("\n[3/5] Extracting sections...")

extracted = {}
for name, (start, end) in sections.items():
    extracted[name] = lines[start:end]
    line_count = len(extracted[name])
    print(f"  [OK] {name:15s}: {line_count:4d} lines (lines {start+1}-{end})")

# Reconstruct with new order: Preamble → Intro (+ Types) → Methods (+ GEESP) → Results → Discussion (+ Patterns + Logistics) → Conclusion
print("\n[4/5] Reorganizing to IMRAD + consolidation...")

new_order = [
    ('preamble', 'PREAMBLE'),
    ('intro', 'INTRODUCTION'),
    ('tipos', '  → Added: Types of Technologies (into Introduction)'),
    ('methodology', 'METHODOLOGY'),
    ('geesp', '  → Added: GEESP Framework (into Methods)'),
    ('results', 'RESULTS'),
    ('discussion', 'DISCUSSION'),
    ('patterns', '  → Added: Comparative Patterns (into Discussion)'),
    ('logistics', '  → Added: Logistics/Costs (into Discussion)'),
    ('conclusion', 'CONCLUSION')
]

print("\nNew structure:")
for section, label in new_order:
    print(f"  [OK] {label}")

# Build reorganized content
print("\n[5/5] Writing reorganized file...")

reorganized_lines = []

# 1. Preamble (unchanged)
reorganized_lines.extend(extracted['preamble'])

# 2. Introduction (unchanged, but add note about integration)
reorganized_lines.append("\n% ==========================================")
reorganized_lines.append("% PART 1: INTRODUCTION (includes technology/theory overview)")
reorganized_lines.append("% ==========================================\n")
reorganized_lines.extend(extracted['intro'])

# 3. Types of Technologies → Integrated as enhanced literature section in Introduction
reorganized_lines.append("\n% --- Technology Foundations & International Context (from original Tipos section) ---\n")
reorganized_lines.extend(extracted['tipos'])

# 4. Methodology (unchanged)
reorganized_lines.append("\n% ==========================================")
reorganized_lines.append("% PART 2: METHODOLOGY (includes GEESP framework)")
reorganized_lines.append("% ==========================================\n")
reorganized_lines.extend(extracted['methodology'])

# 5. GEESP Framework → Integrated into Methodology
reorganized_lines.append("\n% --- GEESP-Angola Framework Details (from original section) ---\n")
reorganized_lines.extend(extracted['geesp'])

# 6. Results (unchanged)
reorganized_lines.append("\n% ==========================================")
reorganized_lines.append("% PART 3: RESULTS")
reorganized_lines.append("% ==========================================\n")
reorganized_lines.extend(extracted['results'])

# 7. Discussion (unchanged, but will have additions)
reorganized_lines.append("\n% ==========================================")
reorganized_lines.append("% PART 4: DISCUSSION (includes validation & implementation insights)")
reorganized_lines.append("% ==========================================\n")
reorganized_lines.extend(extracted['discussion'])

# 8. Comparative Patterns → Integrated into Discussion
reorganized_lines.append("\n% --- Comparative Analysis: Patterns & Validation (from original section) ---\n")
reorganized_lines.extend(extracted['patterns'])

# 9. Logistics/Costs → Integrated into Discussion
reorganized_lines.append("\n% --- Implementation Framework: Logistics, Costs & Partnerships (from original section) ---\n")
reorganized_lines.extend(extracted['logistics'])

# 10. Conclusion (all remaining)
reorganized_lines.append("\n% ==========================================")
reorganized_lines.append("% PART 5: CONCLUSION & RECOMMENDATIONS")
reorganized_lines.append("% ==========================================\n")
reorganized_lines.extend(extracted['conclusion'])

# Write reorganized file
reorganized_content = '\n'.join(reorganized_lines)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(reorganized_content)

new_line_count = len(reorganized_lines)
print(f"[OK] Written {OUTPUT_FILE} ({new_line_count} lines)")

print("\n" + "=" * 90)
print(" REORGANIZATION COMPLETE")
print("=" * 90)

print(f"""
Summary:
  - Original file: {total_lines} lines
  - New file: {new_line_count} lines
  - Backup: {BACKUP_FILE}
  - Reorganized: {OUTPUT_FILE}

Structure Changes:
  [OK] Intro now includes technology/theory overview
  [OK] Methodology now includes GEESP framework details  
  [OK] Discussion now includes comparative analysis + implementation insights
  [OK] All content preserved - only reorganized for IMRAD compliance

Next Steps:
  1. Review {OUTPUT_FILE} for structure
  2. Test LaTeX compilation
  3. Verify cross-references
  4. Update project harmony score
""")

# Create summary
with open("REORGANIZATION_SUMMARY.txt", "w", encoding="utf-8") as f:
    f.write("SOL.TEX REORGANIZATION SUMMARY\n")
    f.write("=" * 80 + "\n")
    f.write(f"Date: {datetime.now().isoformat()}\n\n")
    f.write("Original Structure:\n")
    f.write("  1. Introducao\n")
    f.write("  2. GEESP-Angola Framework\n")
    f.write("  3. Tipos de Tecnologias\n")
    f.write("  4. Metodologia\n")
    f.write("  5. Resultados\n")
    f.write("  6. Discussao\n")
    f.write("  7. Padroes e Praticas\n")
    f.write("  8. Logistica, Custos e Parcerias\n")
    f.write("  9. Conclusao\n\n")
    f.write("New IMRAD Structure:\n")
    f.write("  1. INTRODUCTION (+ Technology/Theory)\n")
    f.write("  2. METHODOLOGY (+ GEESP Framework)\n")
    f.write("  3. RESULTS\n")
    f.write("  4. DISCUSSION (+ Comparative Analysis + Implementation)\n")
    f.write("  5. CONCLUSION\n\n")
    f.write("Content Preservation:\n")
    f.write("  - All original content maintained\n")
    f.write("  - Reorganized for logical flow\n")
    f.write("  - Meets international scientific standards (IMRAD)\n")

print("Summary saved to: REORGANIZATION_SUMMARY.txt")
