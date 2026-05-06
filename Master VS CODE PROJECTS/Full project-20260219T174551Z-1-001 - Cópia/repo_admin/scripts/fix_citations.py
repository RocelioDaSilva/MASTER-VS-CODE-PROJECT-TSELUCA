#!/usr/bin/env python3
"""
Completar arquivo .bib com citações faltantes
"""
import re
from pathlib import Path

# Resolve repository-relative paths for the manuscript and bib files.
# This makes the script portable rather than relying on user-specific absolute paths.
ROOT = Path(__file__).resolve().parent

candidates_tex = [
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "SOL_melhorado.tex",
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "SOL.tex",
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "Coding parts" / "SUBMISSION_READY" / "SOL.tex",
]
tex_path = next((p for p in candidates_tex if p.exists()), candidates_tex[0])

candidates_bib = [
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "referencias.bib",
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "Coding parts" / "SUBMISSION_READY" / "referencias.bib",
]
bib_path = next((p for p in candidates_bib if p.exists()), candidates_bib[0])

tex_file = str(tex_path)
bib_file = str(bib_path)

print(f"[PATHS] tex_file={tex_file}")
print(f"[PATHS] bib_file={bib_file}")

# ============================================================================
# 1. EXTRAIR TODAS AS CITAÇÕES DO TEX
# ============================================================================
print("[1] Extraindo citações do arquivo TEX...")
with open(tex_file, 'r', encoding='utf-8') as f:
    tex_content = f.read()

# Encontrar todas as citações
citations = set(re.findall(r'\\cit[ep]\{([^}]+)\}', tex_content))
print(f"  Total de citações encontradas: {len(citations)}")

# ============================================================================
# 2. CARGA O .BIB ATUAL
# ============================================================================
print("\n[2] Carregando arquivo .bib atual...")
with open(bib_file, 'r', encoding='utf-8') as f:
    bib_content = f.read()

# Extrair citações existentes
existing = set(re.findall(r'@\w+\{(\w+),', bib_content))
print(f"  Entradas existentes: {len(existing)}")

# ============================================================================
# 3. IDENTIFICAR FALTANDO
# ============================================================================
missing = sorted(citations - existing)
print(f"\n[3] Citações faltando: {len(missing)}")
for i, cite in enumerate(missing, 1):
    print(f"    {i:2d}. {cite}")

# ============================================================================
# 4. CRIAR TEMPLATE PARA ENTRADAS FALTANDO
# ============================================================================
print("\n[4] Gerando template de entradas para .bib...")

template_entries = []
for cite in missing:
    # Tentar extrair autor e ano do nome
    match = re.match(r'(\w+?)(\d{4})', cite)
    if match:
        author = match.group(1)
        year = match.group(2)
    else:
        author = cite[:10]
        year = '2024'
    
    entry = f"""
@article{{{cite},
  author = {{{author}, Author}},
  year = {{{{ {year}}}}},
  title = {{{{Generation and selection methods for solar energy in Angola}}}},
  journal = {{{{Journal of Renewable Energy}}}},
  note = {{{{PLACEHOLDER - adicionar informações completas}}}}
}}
"""
    template_entries.append(entry)

# ============================================================================
# 5. APPEND AO .BIB (com comentário)
# ============================================================================
print("\n[5] Atualizando arquivo .bib...")

with open(bib_file, 'a', encoding='utf-8') as f:
    f.write("\n\n% ============================================================\n")
    f.write("% ENTRADAS ADICIONADAS AUTOMATICAMENTE - REVISAR E COMPLETAR\n")
    f.write("% ============================================================\n")
    for entry in template_entries:
        f.write(entry)

print(f"  ✓ {len(template_entries)} entradas de template adicionadas ao final do .bib")
print(f"  Observação: As entradas são placeholders - revisar e preencher com dados reais")

# ============================================================================
# 6. VERIFICAÇÃO FINAL
# ============================================================================
print("\n[6] Verificação final...")
with open(bib_file, 'r', encoding='utf-8') as f:
    new_bib = f.read()

new_existing = set(re.findall(r'@\w+\{(\w+),', new_bib))
resolved = citations & new_existing
unresolved = citations - new_existing

print(f"  Citações resolvidas: {len(resolved)}/{len(citations)}")
if unresolved and len(unresolved) < 10:
    print(f"  Ainda faltando ({len(unresolved)}):")
    for cite in unresolved:
        print(f"    - {cite}")
elif unresolved:
    print(f"  Ainda faltando: {len(unresolved)} citações")

print("\n" + "="*70)
print("CONCLUÍDO")
print("="*70)
print("Próximas ações:")
print("1. Revisar as entradas PLACEHOLDER no final de referencias.bib")
print("2. Preencher author, title, journal com informações corretas")
print("3. Compilar: pdflatex && bibtex && pdflatex (2x)")
print("="*70)
