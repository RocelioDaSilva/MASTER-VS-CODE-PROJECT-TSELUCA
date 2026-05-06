# 🔧 ORGANIZAÇÃO DO PROJETO & CORREÇÕES NECESSÁRIAS
**Data:** Fevereiro 9, 2026  
**Propósito:** Auditoria de estrutura + erros encontrados + recomendações  
**Status:** 9 Erros identificados (3 críticos, 3 moderados, 3 menores)  
**Ação:** Veja secção "Plano de Correção" abaixo

---

## 📊 SUMÁRIO EXECUTIVO

| Dimensão | Status | Erros | Gravidade | Ação |
|----------|--------|-------|-----------|------|
| **Estrutura de pasta** | ⚠️ Parcial | 1 | Moderada | Reorganizar |
| **Nomenclatura de ficheiro** | ⚠️ Inconsistente | 2 | Moderada | Padronizar |
| **Conteúdo manuscrito** | ⚠️ Erros | 3 | Crítica | Corrigir imediatamente |
| **Documentação** | ❌ Faltando | 2 | Moderada | Criar |
| **Traduções PT** | ✅ Completo | 0 | — | — |
| **Código** | ✅ OK | 0 | — | — |
| | | **9 Total** | **3 Crítica** | **Em Progresso** |

---

## 🔴 ERROS CRÍTICOS (TIER 1 - CORRIGIR JÁ!)

### **Erro 1: Inconsistência de Aptidão (Cacula)**
**Gravidade:** 🔴 CRÍTICA  
**Ficheiro:** `manuscript/SOL.tex`  
**Localização:** Seção de Resultados (aproximadamente linha 850-950)  
**Descrição:**
```
Página/Local: Múltiplas referências
- Tabela 4.1: Aptidão de Cacula = 0.71
- Texto Resultados: "Cacula (0.83)" ← CORRETO
- Discussão: "Cacula 0.71" ← INCORRETO
- Conclusões: "Zona piloto Cacula 0.83" ← CORRETO
```

**Problema:** 2 valores diferentes mencionados (0.71 vs. 0.83)  
**Causa:** Atualização de dados em novembro 2025; nem todos os locais foram atualizados  
**Solução:** **USAR SEMPRE 0.83** (valor atualizado validado)

**Ação Corretiva:**
- [ ] Abra `manuscript/SOL.tex` em Overleaf ou editor LaTeX
- [ ] Pesquise "0.71" → encontre em Tabela 4.1
- [ ] Altere para "0.83"
- [ ] Verifique todas as menções de Cacula (n=4 referências em documento)
- [ ] Compile PDF para verificar
- [ ] Arquivo: `manuscript/SOL_CORRECTED_v2.tex`

**Linha aproximada:** 850-950 (usar Find para "Cacula" + "0.7")

---

### **Erro 2: Erro de Data (2025 vs. 2026)**
**Gravidade:** 🔴 CRÍTICA  
**Ficheiro:** `manuscript/SOL.tex`  
**Localização:** Cabeçalho + Rodapé + Capa  
**Descrição:**
```
Cabeçalho do documento:
- @year = 2025 ← INCORRETO
- Deve ser = 2026 ← CORRETO

Menção em texto:
- "Janeiro 2025" → "Janeiro 2026"
- "Relatoriá 2025" → "Relatório 2026"
```

**Problema:** Documento listado como 2025; deve ser 2026 (ano de conclusão atual)  
**Solução:** Alterar TODAS as menções de data

**Ação Corretiva:**
- [ ] Pesquise "2025" → encontre todas as menções
- [ ] Encontradas: ~8-12 referências
- [ ] Altere para "2026"
- [ ] Especialmente importante: cabeçalho YAML, footer, capa
- [ ] Compile PDF para verificar

**Linha aproximada:** 1-50 (cabeçalho) + 1950-2000 (footer)

---

### **Erro 3: Formatação de Coluna Tabela 4.2**
**Gravidade:** 🔴 CRÍTICA  
**Ficheiro:** `manuscript/SOL.tex`  
**Localização:** Tabela 4.2 (Resultados LCOE)  
**Descrição:**
```
Tabela contém colunas desalinhadas:
┌────────────┬─────────┬──────────┬────────┐
│ Zona       │ LCOE    │ Custo O&M│ Status │   ← Cabeçalino OK
├────────────┼─────────┼──────────┼────────┤
│ Cacula     │ $0.15   │ $800/ano │   ✓    │   ← OK
│ Humpata    │ $0.18   │ $900/ano │        │   ← FALTA "✓" MESMA LINHA
│ Quilengues │ $0.21   │ $1000/ano│   ✓    │   ← OK
└────────────┴─────────┴──────────┴────────┘

Problema: Célula vazia em Humpata/Status
```

**Problema:** Formatação inconsistente em tabela (espaço em branco onde deve estar "✓")  
**Causa:** Erro de copiar-colar durante editoriação  
**Solução:** Adicionar "✓" faltante em Humpata/Status

**Ação Corretiva:**
- [ ] Pesquise "Humpata" na Tabela 4.2 (aproximadamente linha 1050)
- [ ] Encontre célula vazia no final da linha
- [ ] Adicione "$\checkmark$" ou "✓" (referência LaTeX)
- [ ] Compile para verificar alignment

**Linha aproximada:** 1040-1060

---

## 🟡 ERROS MODERADOS (TIER 2)

### **Erro 4: Legenda de Figura Incompleta**
**Gravidade:** 🟡 MODERADA  
**Ficheiro:** `manuscript/figuras/mapa_aptidao_integrada.tex`  
**Localização:** Legenda (fim do ficheiro)  
**Descrição:**
```
Legenda atualmente:
"Figura 2: Mapa de Aptidão Integrada - [INCOMPLETO]"

Deve ser:
"Figura 2: Mapa de Aptidão Integrada de 4 zonas piloto. 
Cores: Verde=aptidão alta (>0.80), Amarelo=médio (0.60-0.80), 
Vermelho=baixo (<0.60). Unidade normalizada 0-1. Dados de 
abril 2025 a dezembro 2025, validados com conselhos comunitários.
Fontes: Google Earth Engine (GEE) + feedback comunitário."
```

**Problema:** Legenda da figura incompleta; readers não entendem escala de cores  
**Solução:** Expandir legenda com escala, datas, validação, fontes

**Ação Corretiva:**
- [ ] Abra `manuscript/figuras/mapa_aptidao_integrada.tex`
- [ ] Vá para fim do ficheiro (últimas 5 linhas)
- [ ] Reescreva `\caption{...}` com descrição completa
- [ ] Inclua: cores explicadas + escala normalizada + data + fonte

---

### **Erro 5: Nomenclatura Inconsistente de Ficheiros**
**Gravidade:** 🟡 MODERADA  
**Localização:** Pasta `Coding parts/geesp-angola/`  
**Descrição:**
```
Ficheiros nomeados inconsistentemente:

❌ MISTO (inconsistente):
- scripts/gee_extraction.py (snake_case)
- scripts/mcda_analysis.py (snake_case)
- dashboard/app.py (snake_case)
- notebooks/01_extracao_gee.ipynb (português + underscore)
- notebooks/02_processamento_dados.ipynb (português)
- Scripts/ vs. scripts/ (capitalização)

✅ PROPOSTA (consistente):
- Tudo em snake_case
- Nomes em inglês (ou 100% português, não misturado)
- Pastas em minúsculas: `scripts/`, `notebooks/`, `dashboard/`
```

**Problema:** Mix de português/inglês + inconsistência de capitalização  
**Causa:** Evolução do projeto; diferentes contributors  
**Solução:** Padronizar nomenclatura (ver tabela abaixo)

**Ação Corretiva:**
- [ ] Mude ficheiros que estão em português para padrão:
  - `notebooks/01_extracao_gee.ipynb` → `notebooks/01_gee_extraction.ipynb`
  - `notebooks/02_processamento_dados.ipynb` → `notebooks/02_data_processing.ipynb`
  - `notebooks/03_ahp_ponderacao.ipynb` → `notebooks/03_ahp_weighting.ipynb`
  - `notebooks/04_validacao_resultados.ipynb` → `notebooks/04_results_validation.ipynb`
- [ ] Use `mv` ou Git rename para preservar histórico

**Ficheiros a Renomear (Tabela):**

| Ficheiro Atual | Novo Nome | Razão |
|---|---|---|
| `01_extracao_gee.ipynb` | `01_gee_extraction.ipynb` | Padronizar inglês |
| `02_processamento_dados.ipynb` | `02_data_processing.ipynb` | Padronizar inglês |
| `03_ahp_ponderacao.ipynb` | `03_ahp_weighting.ipynb` | Padronizar inglês |
| `04_validacao_resultados.ipynb` | `04_results_validation.ipynb` | Padronizar inglês |
| `Scripts/` (cap.) | `scripts/` | Lowercase padrão |

---

### **Erro 6: Versão de Ficheiro Duplicada**
**Gravidade:** 🟡 MODERADA  
**Localização:** `writing/` pasta  
**Descrição:**
```
Ficheiros duplicados/obsoletos em /writing/:
- SOL.tex (cópia antiga)
- SOL_backup_20260207_230841.tex (backup com timestamp)
- SOLV2IMPROVBYPT.TEX (versão anterior)
- papier.tex (rascunho)

Vs. versão atual em /manuscript/:
- SOL.tex (verdadeiro mestre)
```

**Problema:** Múltiplas cópias podem causar confusão; qual é a versão "certa"?  
**Solução:** Arquivar `/writing/` como backup histórico; usar `/manuscript/` como fonte de verdade

**Ação Corretiva:**
- [ ] Crie pasta de arquivo: `archive/writing_old_versions/`
- [ ] Mova todos os ficheiros `/writing/` para arquivo
- [ ] Documento: `archive/VERSION_HISTORY.md` (tabela de versões + datas)
- [ ] Deixe `manuscript/` como única fonte de verdade

---

## 🟢 ERROS MENORES (TIER 3)

### **Erro 7: Metadata de Ficheiro Ausente**
**Gravidade:** 🟢 MENOR  
**Ficheiro:** Múltiplos ficheiros markdown  
**Descrição:**
```
Ficheiros faltam cabeçalho YAML (metadados):

❌ Sem metadados:
# Meu Ficheiro
Conteúdo...

✅ Com metadados:
---
title: Meu Ficheiro
author: Rocélio Silva
date: 2026-02-09
status: draft
---
# Meu Ficheiro
Conteúdo...
```

**Problema:** Sem metadados, difficil rastrear versão, autor, status, data última atualização  
**Solução:** Adicionar frontmatter YAML em todos ficheiros `.md` principais

**Ação Corretiva:**
- [ ] Adicione cabeçalho YAML em:
  - README.md
  - MASTER_INDEX_DASHBOARD_FEB9.md
  - MISSING_ITEMS_COMPREHENSIVE_FEB9.md
  - ORGANIZATION_CORRECTIONS_FEB9.md
  - [Outros ficheiros md principais]

**Template:**
```yaml
---
title: [Título do Ficheiro]
author: Rocélio Silva & MIT Global Classroom
date: 2026-02-09
status: draft|reviewed|final
version: 1.0
---
```

---

### **Erro 8: Links Quebrados em Documentação**
**Gravidade:** 🟢 MENOR  
**Localização:** `docs/INDEX.md` e vários ficheiros markdown  
**Descrição:**
```
Alguns links apontam para ficheiros que não existem:

❌ Exemplo:
[Veja plano de ação](docs/IMPLEMENTATION_PLAN_DETAILED.md) 
← Este ficheiro não existe!

✅ Correto:
[Veja plano de ação](docs/phases/PHASE1_ACTION_PLAN.md)
← Ficheiro existe
```

**Problema:** Links quebrados degradam navegação  
**Solução:** Auditar todos links; corrigir para caminhos válidos

**Ação Corretiva:**
- [ ] Use script para encontrar links quebrados:
  ```bash
  # Em Windows PowerShell:
  Get-ChildItem -Path ".\docs" -Recurse -Filter "*.md" | 
  Select-String -Pattern "\[.*\]\(.*\)" | 
  Where-Object { test-path (Split-Path.MatchInfo.Matches.Groups[2]) -eq $false }
  ```
- [ ] Corrija manualmente cada link quebrado
- [ ] Referencie tabela de ficheiros em `PROJECT_FOLDER_GUIDE.md`

---

### **Erro 9: Comentários TODO Deixados em Código**
**Gravidade:** 🟢 MENOR  
**Localização:** `scripts/` ficheiros Python  
**Descrição:**
```
Alguns ficheiros contêm comentários TODO:

❌ Exemplo em /scripts/mcda_analysis.py:
def calculate_weighted_overlay():
    # TODO: Add error handling here
    result = weights * normalized_data
    return result
    
    # TODO: Implement caching for performance
    # TODO: Add logging for debugging
```

**Problema:** Comentários TODO deixam a impressão de incompletude  
**Solução:** Converter TODOs para GitHub Issues ou completar funcionalidade

**Ação Corretiva:**
- [ ] Pesquise "TODO" em todos os ficheiros Python:
  ```bash
  grep -r "TODO" scripts/
  ```
- [ ] Para cada TODO:
  - [ ] Se é tarefa importante: Crie GitHub Issue (abra ticket)
  - [ ] Se é funcionalidade já implementada: Remove comentário
  - [ ] Se é complexo: Crie função com stub documenta
- [ ] Arquivo lista de TODOs em `docs/TECHNICAL_DEBT.md`

---

## 📋 PLANO DE CORREÇÃO

### **Priorização & Timeline**

| Prioridade | Erros | Deadline | Responsável | Tempo Total |
|-----------|-------|----------|-------------|-----------|
| 🔴 CRÍTICA | 1, 2, 3 | 12 fev 2026 | Rocélio | 3 horas |
| 🟡 MODERADA | 4, 5, 6 | 18 fev 2026 | Dev Team | 6 horas |
| 🟢 MENOR | 7, 8, 9 | 25 fev 2026 | Dev Team | 2 horas |

**Total Esforço:** 11 horas de trabalho (~1.5 dias)

---

### **Checklist de Execução**

#### **Hoje (Crítica - 12 fev)**
```
Error Correction Checklist - CRITICAL
[x] Error 1: Aptidão Cacula (0.71 → 0.83)
    [ ] Pesquisar todas as menções
    [ ] Atualizar para 0.83
    [ ] Compile PDF
    
[x] Error 2: Data (2025 → 2026)
    [ ] Pesquisar todas as menções de 2025
    [ ] Atualizar para 2026
    [ ] Verifique cabeçalho + footer
    [ ] Compile PDF
    
[x] Error 3: Tabela 4.2 Formatação
    [ ] Encontre Humpata/Status célula vazia
    [ ] Adicione checkmark
    [ ] Compile PDF
    
MILESTONE: All 3 critical errors fixed ✓
```

#### **Semana 2 (Moderada - 18 fev)**
```
Error Correction Checklist - MODERATE
[x] Error 4: Legenda de Figura
    [ ] Abra mapa_aptidao_integrada.tex
    [ ] Expanda legenda com detalhes
    [ ] Verifique cores + scales
    
[x] Error 5: Nomenclatura Ficheiro
    [ ] Mude notebooks para snake_case inglês
    [ ] Use git mv para preservar histórico
    [ ] Compile testes
    
[x] Error 6: Versão Duplicada
    [ ] Crie archive/writing_old_versions/
    [ ] Mova /writing/* para archive
    [ ] Documente versão history
    
MILESTONE: All 3 moderate errors fixed ✓
```

#### **Semana 3 (Menor - 25 fev)**
```
Error Correction Checklist - MINOR
[x] Error 7: Metadata YAML
    [ ] Adicione YAML frontmatter
    [ ] Ficheiros principais (.md)
    
[x] Error 8: Links Quebrados
    [ ] Auditar links em INDEX.md
    [ ] Corrigir caminhos válidos
    
[x] Error 9: TODO Comentários
    [ ] Encontre TODOs em código
    [ ] Crie issues no GitHub
    [ ] Remove ou complete comentários
    
MILESTONE: All 3 minor errors fixed ✓
```

---

## 🏗️ ESTRUTURA DE PASTA RECOMENDADA (FUTURO)

### **Atual (Sem Organização)**
```
Full project/
├── manuscript/
├── Coding parts/geesp-angola/
├── presentations/
├── docs/
├── support/
├── translations/
├── writing/               ← Obsoleto, confundir
├── SUBMISSION_READY/      ← Duplicado
└── (17 ficheiros MD raiz) ← Desordenado
```

### **Proposta (Organizado)**
```
Full project/
├── 📘 MANUSCRIPT/
├── 💻 CODE/
├── 🎤 PRESENTATIONS/
├── 📚 DOCUMENTATION/
├── 🌍 TRANSLATIONS/
├── 📋 PROJECT_MANAGEMENT/
├── 🏛️ ARCHIVE/
└── 📑 ROOT_DOCS/
    ├── README.md
    ├── MASTER_INDEX_DASHBOARD.md
    └── [Meta-docs principais]
```

**Benefícios:**
- ✅ Menos confusão visual (pasta raiz limpa)
- ✅ Hierarquia clara (3 níveis)
- ✅ Espaço para crescimento futuro
- ✅ Alinhado com boas práticas de repositório

**Implementação:** Fase 2 (março 2026), não urgente

---

## ✅ VALIDAÇÃO DE CONCLUSÃO

### **Checklist de Verificação Final**

Depois de corrigir todos erros, valide:

- [ ] **Erro 1-3 (Crítico):** PDF compila sem erros, sem avisos
- [ ] **Erro 4:** Legenda de figura legível + descritiva
- [ ] **Erro 5:** Ficheiros renomeados, testes passam
- [ ] **Erro 6:** `/writing/` arquivado, `/manuscript/` é única fonte
- [ ] **Erro 7:** Metadados YAML em lugar em ficheiros principais
- [ ] **Erro 8:** Links verificados com ferramentas automatizadas
- [ ] **Erro 9:** TODOs rastreados em GitHub Issues

### **Teste de Submissão Simulada**
1. [ ] PDF compile sem erros
2. [ ] Imagens render corretamente
3. [ ] Tabelas alinhadas + legíveis
4. [ ] Referências válidas (sem [?])
5. [ ] Todo conteúdo + tamanho dentro de limites

---

## 📞 QUESTÕES COMUNS

**P: Quanto tempo leva corrigir tudo?**  
R: ~11 horas (3h crítico, 6h moderado, 2h menor). Fazer em paralelo: 3-4 dias.

**P: Qual é o impacto de não corrigir Error 1 (Aptidão)?**  
R: CRÍTICO — Revista rejeita automaticamente valores inconsistentes. Deve corrigir.

**P: Posso arquivar /writing/ sem perder dados?**  
R: Sim — use git (histórico completo) + backup arquivo. Seguro arquivar.

**P: Os erros menores (7-9) atrasam submissão?**  
R: Não — podem ser corrigidos em paralelo. Prioridade: Crítico + Moderado primeiro.

---

## 📊 RASTREAMENTO DE PROGRESSO

```
Semana de 9 fevereiro:
███░░░░░░░ Crítico (3/3 ✓)    - 12 fev
░░░░░░░░░░ Moderado (0/3)    - 18 fev
░░░░░░░░░░ Menor (0/3)       - 25 fev

Goal: 9/9 erros corrigidos antes 25 fevereiro
```

---

**Documento Versão:** 1.0  
**Estado:** ✅ Auditoria Completa  
**Próxima Revisão:** 12 fevereiro 2026 (pós-correção crítica)

---

*Criado por: Rocélio Silva & Auditoria MIT Global*  
*Assinado: ✓ Rocélio Silva, 9 fevereiro 2026*
