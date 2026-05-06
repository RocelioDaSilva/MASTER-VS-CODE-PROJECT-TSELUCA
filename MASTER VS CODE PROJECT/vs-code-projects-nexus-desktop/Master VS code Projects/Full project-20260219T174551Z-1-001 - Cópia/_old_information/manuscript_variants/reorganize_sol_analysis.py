#!/usr/bin/env python3
"""
SOL.tex Reorganization Script
Reorganizes manuscript from current structure to IMRAD standards while preserving all content
"""

import re
import os
from pathlib import Path
from datetime import datetime

# File paths
input_file = "SOL.tex"
output_file = "SOL_REORGANIZED.tex"
backup_file = f"SOL_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex"

print("=" * 80)
print("SOL.TEX REORGANIZATION SCRIPT - IMRAD HARMONIZATION")
print("=" * 80)

# Read the original file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')
total_lines = len(lines)

# Find section locations
sections = {}
for i, line in enumerate(lines):
    if '\\section{Introdução}' in line and 'Introdução' not in sections:
        sections['Introdução'] = i
        print(f"\n✓ Found: Introdução at line {i+1}")
    elif '\\section{GEESP-Angola' in line and 'GEESP' not in sections:
        sections['GEESP'] = i
        print(f"✓ Found: GEESP-Angola Framework at line {i+1}")
    elif '\\section{Tipos de Tecnologias' in line:
        sections['Tipos'] = i
        print(f"✓ Found: Tipos de Tecnologias at line {i+1}")
    elif '\\section{Metodologia}' in line and 'Metodologia' not in sections:
        sections['Metodologia'] = i
        print(f"✓ Found: Metodologia at line {i+1}")
    elif '\\section{Resultados}' in line and 'Resultados' not in sections:
        sections['Resultados'] = i
        print(f"✓ Found: Resultados at line {i+1}")
    elif '\\section{Discussão}' in line and 'Discussão' not in sections:
        sections['Discussão'] = i
        print(f"✓ Found: Discussão at line {i+1}")
    elif '\\section{Padrões' in line:
        sections['Padrões'] = i
        print(f"✓ Found: Padrões e Práticas Históricas at line {i+1}")
    elif '\\section{Logística' in line:
        sections['Logística'] = i
        print(f"✓ Found: Logística, Custos e Parcerias at line {i+1}")
    elif '\\section{Conclusão}' in line or '\\section{Conclusões}' in line:
        if 'Conclusão' not in sections:
            sections['Conclusão'] = i
            print(f"✓ Found: Conclusão/Conclusões at line {i+1}")

print(f"\nTotal file lines: {total_lines}")
print("\n" + "=" * 80)
print("REORGANIZATION PLAN:")
print("=" * 80)

print("\nCurrent Order:")
for section in ['Introdução', 'GEESP', 'Tipos', 'Metodologia', 'Resultados', 'Discussão', 'Padrões', 'Logística', 'Conclusão']:
    if section in sections:
        print(f"  • {section:20s} at line {sections[section] + 1:5d}")

print("\nTarget Order (IMRAD Standard):")
print("""
  1. Introdução (keep + enhance with theory from Tipos)
  2. Tipos de Tecnologias → Move into Introduction as literature/theory subsection
  3. Metodologia (keep + integrate GEESP framework as subsections)
  4. GEESP-Angola → Move into Methodology
  5. Resultados (keep as is)
  6. Discussão (keep + integrate Padrões + Logística)
  7. Padrões e Práticas → Move into Discussion
  8. Logística, Custos → Move into Discussion  
  9. Conclusão (consolidate duplicates, keep strong one)
""")

print("\n" + "=" * 80)
print("STATUS: Analysis complete. Ready for reorganization implementation.")
print("=" * 80)
print("\nNext step: Execute strategic section replacements to achieve IMRAD structure")
print("while preserving all content and cross-reference integrity.")

# Write analysis summary
with open("reorganization_analysis.txt", "w", encoding="utf-8") as f:
    f.write("SOL.TEX REORGANIZATION ANALYSIS\n")
    f.write("=" * 80 + "\n")
    f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
    f.write(f"Total file lines: {total_lines}\n\n")
    f.write("Sections Found:\n")
    for section in sorted(sections.items(), key=lambda x: x[1]):
        f.write(f"  {section[0]:20s} at line {section[1] + 1:5d}\n")

print("\nAnalysis saved to: reorganization_analysis.txt")
