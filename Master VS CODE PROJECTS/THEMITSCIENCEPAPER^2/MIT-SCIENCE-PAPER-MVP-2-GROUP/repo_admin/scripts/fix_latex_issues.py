#!/usr/bin/env python3
"""
Script para corrigir problemas estruturais do arquivo SOL_melhorado.tex
"""
import re
import os
from pathlib import Path

# Resolve repo-relative tex and bib paths for portability
ROOT = Path(__file__).resolve().parent
candidates_tex = [
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "SOL_melhorado.tex",
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "SOL.tex",
]
tex_file_path = next((p for p in candidates_tex if p.exists()), candidates_tex[0])

candidates_bib = [
    ROOT / "MIT-SCIENCE-PAPER" / "Full project" / "01_Science" / "manuscript" / "referencias.bib",
]
bib_file_path = next((p for p in candidates_bib if p.exists()), candidates_bib[0])

tex_file = str(tex_file_path)
bib_file = str(bib_file_path)

print(f"[PATHS] tex_file={tex_file}")
print(f"[PATHS] bib_file={bib_file}")

# ============================================================================
# 1. LER ARQUIVO TEX
# ============================================================================
print("[1] Lendo arquivo TEX...")
with open(tex_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar índice de \documentclass
doc_class_idx = content.find(r'\documentclass')
if doc_class_idx == -1:
    print("ERRO: \\documentclass não encontrado!")
    exit(1)

# Extrair seção pré-documentclass (contém \bibliography errada)
pre_doc = content[:doc_class_idx]
post_doc = content[doc_class_idx:]

# Remover \bibliography e \bibliographystyle do início
pre_doc_clean = re.sub(r'\\bibliography\{.*?\}', '', pre_doc)
pre_doc_clean = re.sub(r'\\bibliographystyle\{.*?\}', '', pre_doc_clean)
pre_doc_clean = re.sub(r'%.*?\n', '\n', pre_doc_clean)  # Remover comentários
pre_doc_clean = re.sub(r'\n\s*\n\s*\n', '\n\n', pre_doc_clean)  # Limpar linhas em branco

# Reconstruir conteúdo
content_fixed = pre_doc_clean + post_doc

# Adicionar \bibliography no final (antes de \end{document})
content_fixed = content_fixed.replace(
    r'\end{document}',
    r'''\
\bibliographystyle{plainnat}
\bibliography{referencias}

\end{document}'''
)

print("  ✓ Movido \\bibliography e \\bibliographystyle para o final")

# ============================================================================
# 2. ADICIONAR RÓTULOS FALTANTES
# ============================================================================
print("\n[2] Adicionando rótulos de equações faltantes...")

# Lista de equações que precisam de rótulos
missing_labels = {
    r'X\_{\text{norm}} = \frac{X - X\_{\min}}{X\_{\max} - X\_{\min}}': r'\label{eq:normalization}',
    r'S(\vec{x}) = \sum\_{i=1}^{n} w\_i \cdot \text{Norm}': r'\label{eq:overlay}',
    r'\\text{CR} = \\frac{\\text{CI}}{\\text{RI}}': r'\label{eq:cr}',
}

# Verificar se os rótulos já existem
existing_labels = set(re.findall(r'\\label\{(.*?)\}', content_fixed))
print(f"  Rótulos já existentes: {len(existing_labels)}")

# ============================================================================
# 3. ADICIONAR RÓTULOS PARA TABELAS/FIGURAS FALTANTES
# ============================================================================
print("\n[3] Adicionando rótulos para tabelas/figuras referenciadas mas não definidas...\n")

missing_refs = [
    'app:ahp_matrix',
    'tab:aptitude_classes', 
    'eq:lcoe',
    'tab:ahp_weights',
    'tab:cacula_impact',
    'fig:mapas_individual',
    'fig:mapa_integrado',
    'tab:lca_summary',
    'tab:lca_assumptions',
    'tab:lca_numeric',
    'tab:mitigation_costs',
    'tab:sensitivity',
    'tab:communities',
    'tab:45_communities',
]

# Verificar quais já existem
for ref in missing_refs:
    if f'\\label{{{ref}}}' in content_fixed:
        print(f"  ✓ {ref} - já definido")
    else:
        print(f"  ✗ {ref} - FALTANDO")

# ============================================================================
# 4. CRIAR ENTRADAS PLACEHOLDER NO .BIB
# ============================================================================
print("\n[4] Analisando arquivo .bib...")

if os.path.exists(bib_file):
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_content = f.read()
    
    # Extrair citações existentes
    existing_citations = set(re.findall(r'@\w+\{(\w+),', bib_content))
    print(f"  Entradas .bib existentes: {len(existing_citations)}")
    
    # Citações referenciadas no TEX
    tex_citations = set(re.findall(r'\\cite[pt]?\{(\w+)\}', content_fixed))
    print(f"  Citações referenciadas: {len(tex_citations)}")
    
    # Diferença (faltando)
    missing_cites = tex_citations - existing_citations
    if missing_cites:
        print(f"\n  Citações faltando ({len(missing_cites)}):")
        for cite in sorted(missing_cites)[:10]:
            print(f"    - {cite}")
        if len(missing_cites) > 10:
            print(f"    ... e {len(missing_cites)-10} mais")
else:
    print(f"  AVISO: Arquivo .bib não encontrado em {bib_file}")

# ============================================================================
# 5. SALVAR ARQUIVO CORRIGIDO
# ============================================================================
print("\n[5] Salvando arquivo corrigido...")
output_file = tex_file.replace('.tex', '_FIXED_STRUCTURE.tex')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print(f"  ✓ Salvo em: {output_file}")

# ============================================================================
# 6. RESUMO
# ============================================================================
print("\n" + "="*70)
print("RESUMO DE AÇÕES:")
print("="*70)
print(f"1. ✓ Movido \\bibliography para final do documento")
print(f"2. ⚠  {len(missing_refs)} rótulos ausentes (alguns podem ser placeholders)")
print(f"3. ⚠  Citações indefinidas precisam ser adicionadas ao .bib")
print(f"\nPróximas ações (manual):")
print(f"- Revisar tab:aptitude_classes, tab:ahp_weights (devem estar no texto)")
print(f"- Adicionar eq:lcoe onde for necessário")
print(f"- Consultar referencias.bib e adicionar citações faltantes")
print(f"- Compilar com: pdflatex SOL_melhorado.tex && bibtex SOL_melhorado && pdflatex ...")
print("="*70)
