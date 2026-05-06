import re
from pathlib import Path

# Read the original file
with open("SOL.tex", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.split('\n')

# Find line numbers of major sections
major_sections = {}
for i, line in enumerate(lines):
    if '\\section{Introdução}' in line and 'Introdução' not in major_sections:
        major_sections['Introdução'] = i
    elif '\\section{GEESP-Angola' in line and 'GEESP' not in major_sections:
        major_sections['GEESP'] = i
    elif '\\section{Tipos de Tecnologias' in line:
        major_sections['Tipos'] = i
    elif '\\section{Metodologia}' in line and 'Metodologia' not in major_sections:
        major_sections['Metodologia'] = i
    elif '\\section{Resultados}' in line and 'Resultados' not in major_sections:
        major_sections['Resultados'] = i
    elif '\\section{Discussão}' in line and 'Discussão' not in major_sections:
        major_sections['Discussão'] = i
    elif '\\section{Padrões' in line:
        major_sections['Padrões'] = i
    elif '\\section{Logística' in line:
        major_sections['Logística'] = i
    elif '\\section{Conclusão}' in line and 'Conclusão' not in major_sections:
        major_sections['Conclusão'] = i

print("Major sections found at lines:")
for section in ['Introdução', 'GEESP', 'Tipos', 'Metodologia', 'Resultados', 'Discussão', 'Padrões', 'Logística', 'Conclusão']:
    if section in major_sections:
        print(f"  {section}: line {major_sections[section] + 1}")

print("\nTotal lines:", len(lines))
print("\n=== REORGANIZATION STRATEGY ===")
print("1. Keep Introduction but enhance with theory")
print("2. Move GEESP Framework into Methods section")
print("3. Move Types of Technologies into Introduction")
print("4. Integrate Comparative Patterns into Discussion")
print("5. Integrate Logistics/Costs into Discussion")
print("6. Consolidate Conclusion sections")
