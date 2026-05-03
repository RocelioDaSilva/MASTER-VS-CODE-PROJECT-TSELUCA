# 📖 COMPLETE PROJECT FOLDER GUIDE & INDEX
**Data:** Fevereiro 9, 2026  
**Propósito:** Explicação completa estrutura pastas + conteúdo cada ficheiro  
**Scope:** 100% projeto GEESP-Angola

---

## 🗺️ MAPA VISUAL ESTRUTURA

```
Full project/ (Raiz)
│
├── 📘 MANUSCRIPT/               ← Documento científico
├── 💻 Coding parts/             ← Tudo código
├── 🎤 presentations/            ← Apresentações
├── 📚 docs/                     ← Documentação
├── 📋 support/                  ← Suporte/templates
├── 🌍 translations/             ← Traduções português
├── 📄 SUBMISSION_READY/         ← Versão pronta entrega
├── 📝 writing/                  ← Rascunhos/backup
├── 🔧 scripts/                  ← Misc scripts
└── 📑 ROOT FILES                ← Master docs + README
```

---

## 📄 ROOT LEVEL FILES (Raiz do Projeto)

### **Navigation & Index**
```
Full project/
├── README.md                                    [PROJECT OVERVIEW]
├── MASTER_INDEX_DASHBOARD_FEB9.md              [INDEX MASTER - START HERE]
├── ORGANIZATION_CORRECTIONS_FEB9.md            [ERROS + ESTRUTURA PROPOSTA]
├── MISSING_ITEMS_COMPREHENSIVE_FEB9.md        [63 GAPS PROJETO]
└── PORTUGUESE_TRANSLATION_COMPLETION_REPORT.md [STATUS TRADUÇÕES PT]
```

**O que contém:**
- `README.md` — Overview geral projeto, 445 linhas, guia rápido começar
- `MASTER_INDEX_DASHBOARD_FEB9.md` — Índice navegação + status dashboard
- `ORGANIZATION_CORRECTIONS_FEB9.md` — Erros encontrados + organização proposta
- `MISSING_ITEMS_COMPREHENSIVE_FEB9.md` — 63 items faltando (TIER 1/2/3)
- `PORTUGUESE_TRANSLATION_COMPLETION_REPORT.md` — Status 7 ficheiros PT traduzidos

**→ LEIA PRIMEIRO:** `MASTER_INDEX_DASHBOARD_FEB9.md` para overview

---

### **Audit & Quality**
```
├── COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md     [9-DIMENSION AUDIT]
├── COMPREHENSIVE_MISSING_PARTS_AUDIT.md        [MISSING PARTS DEEP DIVE]
├── MISSING_PARTS_ACTION_CHECKLIST.md          [QUICK ACTION ITEMS]
├── PROJECT_COMPLETENESS_DASHBOARD.md          [COMPLETION STATUS 62%]
├── PROJECT_COMPLETION_CHECKLIST.md            [PHASE 1-4 CHECKLIST]
├── PHASE1_COMPLETION_REPORT.md                [PHASE 1 STATUS]
└── PHASE1_EXECUTIVE_SUMMARY.md                [PHASE 1 SUMMARY]
```

**O que contém:**
- Audits de 9 dimensões (rigor científico, formato, metodologia, etc.)
- Checklists ação prioritários
- Status completion por fase (1-4)
- Executive summaries

**→ LEIA SE:** Precisa audit técnico ou audit de compliance

---

## 📘 MANUSCRIPT/ FOLDER

### **Estrutura**
```
Full project/manuscript/
├── SOL.tex                      [MANUSCRITO PRINCIPAL - 2.000 LINHAS]
├── SOL_SUBMISSION.tex           [VERSÃO SUBMISSION-READY]
├── referencias.bib              [BIBLIOGRAFIA COMPLETA - 15 REFS]
├── referencias_submission.bib   [BIBLIOGRAPHY PARA SUBMISSÃO]
└── figures/                     [TODAS FIGURAS LATEX]
    ├── mapa_aptidao_integrada.tex
    ├── mapa_distanciarede.tex
    ├── mapa_irradiacao.tex
    ├── mapa_populacao.tex
    └── [outras figuras]
```

### **Conteúdo Detalhado**

#### **SOL.tex** (Manuscrito Principal)
**O que é:** Documento científico completo em LaTeX português (62 páginas)  
**Tamanho:** ~2.000 linhas de código LaTeX  
**Secções:**
1. **Título & Autores** — 6 co-autores ISPTEC + MIT
2. **Abstractos** — Português + English
3. **Research Highlights** — 4 key contributions
4. **Introdução** — Crise energética Angola + contexto
5. **Revisão Literatura** — 15 referencias
6. **Metodologia** — Framework GEESP-Angola, AHP, Weighted Overlay
7. **Resultados** — 3 zonas (Cacula 0.83, Humpata 0.79, Quilengues 0.76)
8. **Discussão** — Implicações, validação, limitações
9. **Conclusões** — 4 achados principais
10. **Apêndices A-D** — LCA, dados comunitários, matrizes AHP, protocolo validação

**Ficheiros Relacionados:**
- `referencias.bib` — 15 referências científicas
- `figures/` — 4 mapas principais (LaTeX tikz)

**Erros Conhecidos:**
- ⚠️ Aptidão Cacula: 0.71 vs 0.83 (inconsistência — usar 0.83)
- ⚠️ Data: "February 9, 2025" deve ser 2026

**Status:** ✅ Pronto submissão (1-2 fixes pendentes)

---

#### **SOL_SUBMISSION.tex**
**O que é:** Cópia clean para submissão revista (sem comentários/rascunhos)  
**Diferença vs. SOL.tex:** Remove TODO notes, limpa formatting, valida references  
**Status:** ✅ Pronto usar

---

#### **referencias.bib**
**O que é:** Ficheiro BibTeX com 15 referências científicas  
**Formato:** BibTeX padrão (usado por Overleaf, LaTeX CLI)  
**Conteúdo:**
- 3 artigos MCDA/GIS (Saaty, Malczewski)
- 4 artigos energia solar África/Angola
- 5 artigos sobre mini-grids + technologia solar
- 3 artigos dados satélite (GEE, VIIRS, Sentinel-2)

**Uso:** `\cite{key}` em SOL.tex puxa referências deste ficheiro

---

#### **figures/** (Pasta)
**O que contém:** 4 mapas principais em TikZ
- `mapa_aptidao_integrada.tex` — Mapa aptidão integrada (Cacula, Humpata, Quilengues)
- `mapa_distanciarede.tex` — Distância à rede elétrica
- `mapa_irradiacao.tex` — Irradiação solar (GHI)
- `mapa_populacao.tex` — Densidade populacional (VIIRS)

**Tipo:** Ficheiros LaTeX TikZ (gráficos vetoriais)  
**Uso:** Incluídos em SOL.tex com `\input{figures/mapa_*.tex}`

---

## 💻 CODING PARTS/ FOLDER

### **Estrutura**
```
Full project/Coding parts/
├── startofthecode               [?? - Unknown file]
└── geesp-angola/                [REPOSITÓRIO CÓDIGO PRINCIPAL]
    ├── README.md                [Overview framework]
    ├── requirements.txt         [Dependências Python]
    ├── pyproject.toml           [Setup pytest, linting]
    ├── config.json              [Configurações]
    ├── Dockerfile               [Image Docker]
    ├── docker-compose.yml       [?? - May not exist]
    │
    ├── 📁 scripts/              [PYTHON SCRIPTS]
    │   ├── gee_extraction.py    [Extração dados Google Earth Engine]
    │   ├── mcda_analysis.py     [Análise multicritério AHP + Weighted Overlay]
    │   ├── data_processing.py   [Normalização dados]
    │   ├── lcoe_calculator.py   [Cálculo LCOE]
    │   ├── utils.py             [Funções auxiliares]
    │   └── __init__.py
    │
    ├── 📁 dashboard/            [STREAMLIT APP - INTERFACE WEB]
    │   ├── app.py               [Aplicação principal (4 abas)]
    │   ├── pages/               [Páginas/widgets]
    │   │   ├── 1_exploracao.py  [Tab 1: Exploração dados]
    │   │   ├── 2_mcda.py        [Tab 2: MCDA interface]
    │   │   ├── 3_resultados.py  [Tab 3: Mapas resultados]
    │   │   └── 4_lcoe.py        [Tab 4: Calculadora LCOE]
    │   ├── assets/              [Imagens, CSS]
    │   └── streamlit_config.toml [Configuração UI]
    │
    ├── 📁 notebooks/            [JUPYTER NOTEBOOKS]
    │   ├── 01_extracao_gee.ipynb      [Notebook: Extração GEE]
    │   ├── 02_processamento_dados.ipynb [Processamento + normalização]
    │   ├── 03_ahp_ponderacao.ipynb     [AHP ponderação demo]
    │   └── 04_validacao_resultados.ipynb [Validação resultados]
    │
    ├── 📁 data/                 [DADOS INPUT + OUTPUT]
    │   ├── raw/                 [Dados brutos (GEE, shapefile)]
    │   ├── processed/           [Dados processados]
    │   └── example/             [Dados demo para tests]
    │
    ├── 📁 monitoring/           [MONITORING APP]
    │   ├── monitoring_app.py    [App monitoramento 24x7]
    │   └── __init__.py
    │
    ├── 📁 tests/                [UNIT TESTS]
    │   ├── test_gee_extraction.py
    │   ├── test_mcda_analysis.py
    │   ├── test_lcoe_calculator.py
    │   └── [11 more test files - all passing 12/12]
    │
    ├── 📁 docs/                 [DOCUMENTAÇÃO CODE]
    │   ├── INSTALL.md
    │   ├── USAGE.md
    │   ├── API.md
    │   └── METODOLOGIA.md
    │
    ├── 📁 .github/              [GITHUB ACTIONS]
    │   └── workflows/           [CI/CD pipelines]
    │       ├── tests.yml        [Automated tests]
    │       └── deploy.yml       [Deployment automation]
    │
    ├── .gitignore               [Ficheiros ignorar git]
    ├── .pre-commit-config.yaml  [Pre-commit hooks]
    ├── LICENSE                  [MIT License]
    ├── .mypy_cache/             [Type checking cache]
    ├── .pytest_cache/           [Test cache]
    ├── __pycache__/             [Python cache]
    │
    ├── 📄 DOCUMENTATION MARKDOWN:
    ├── CODE_GUIDE.md            [Explicação código]
    ├── CHANGELOG.md             [Histórico mudanças]
    ├── CONTRIBUTING.md          [Guidelines contribuições]
    ├── DEPLOYMENT.md            [Instruções deployment]
    ├── MONITORING.md            [Instruções monitoring]
    ├── MONITORING_IMPLEMENTATION.md
    ├── INTEGRATION_GUIDE.md      [Integração com sistemas]
    ├── GITHUB_SETUP.md          [Setup GitHub Actions]
    ├── GITHUB_DEPLOY.md         [Deploy via GitHub]
    ├── INSTALL.md               [Instalação passo-a-passo]
    ├── QUICKSTART.md            [5-30 min getting started]
    ├── README.docker.md         [Docker setup]
    ├── QUICK_REFERENCE.md       [Cheat sheet funções]
    ├── PROJECT_STATUS.md        [Status atual]
    ├── PROJECT_SUMMARY.md       [Resumo projeto]
    ├── AUDIT_REPORT.md          [Audit código]
    │
    ├── 🔧 SHELL SCRIPTS:
    ├── run_dashboard.bat        [Launch dashboard (Windows)]
    ├── run_dashboard.sh         [Launch dashboard (Linux/Mac)]
    ├── run_monitoring.bat       [Launch monitoring (Windows)]
    └── run_monitoring.sh        [Launch monitoring (Linux/Mac)]
```

### **Conteúdo Detalhado**

#### **README.md** (geesp-angola)
**O que é:** Overview framework Python  
**Conteúdo:**
- Descrição 6 módulos principais (GEE, MCDA, Dashboard, LCOE, Monitoring, Utils)
- Arquitetura projeto
- Uso casos (3 personas)
- Fluxo trabalho
- Requisitos sistema

**Uso:** Primeira leitura para novos developers

---

#### **requirements.txt**
**O que é:** Dependências Python (pip)  
**Conteúdo típico:**
```
numpy>=1.20
pandas>=1.3
geopandas>=0.10
rasterio>=1.2
shapely>=1.7
earthengine-api>=0.1.300
streamlit>=1.0
plotly>=5.0
sqlalchemy>=1.4
psycopg2>=2.9
pytest>=6.2
```

**Uso:** `pip install -r requirements.txt` para setup ambiente

---

#### **scripts/** (Pasta Python)
**Ficheiros principais:**

- **gee_extraction.py** — Extrac dados Google Earth Engine
  - Input: Geometria (shapefile/bounds)
  - Output: 6 rasters (GHI, slope, population, distance, NDVI, nightlights)
  - Engine: GEE Python API
  
- **mcda_analysis.py** — MCDA framework
  - Input: 6 rasters normalizados
  - AHP ponderação (Saaty method)
  - Weighted Overlay
  - Output: Aptitude map + zone classification
  
- **data_processing.py** — Normalização
  - Min-max scaling
  - Cost vs. benefit criteria handling
  - Quality control
  
- **lcoe_calculator.py** — LCOE economics
  - Discount rate, lifetime, O&M
  - Output: USD/kWh por zona
  
- **utils.py** — Helper functions
  - File I/O
  - Plotting
  - Data validation

---

#### **dashboard/** (Streamlit App)
**O que é:** Interface web interativa  
**Tecnologia:** Streamlit (Python framework)  
**Componentes:**
- **app.py** — App principal, login, navigation
- **pages/1_exploracao.py** — Tab exploração: dados brutos, filters
- **pages/2_mcda.py** — Tab MCDA: sliders pesos AHP, live updates
- **pages/3_resultados.py** — Tab resultados: mapas, tabelas, exports
- **pages/4_lcoe.py** — Tab calculadora: inputs zona, tecnologia → LCOE

**Acesso:** `streamlit run app.py` (localhost:8501)

---

#### **notebooks/** (Jupyter)
**O que contém:** 4 notebooks análise + tutorial

- **01_extracao_gee.ipynb** — Demo extração GEE
- **02_processamento_dados.ipynb** — Data cleaning + normalização
- **03_ahp_ponderacao.ipynb** — AHP ponderação (interativo)
- **04_validacao_resultados.ipynb** — Sensitivity analysis, validation

**Uso:** Research, demos, teaching

---

#### **tests/** (Unit Tests)
**O que é:** 12 ficheiros pytest  
**Status:** ✅ 12/12 passing  
**Cobertura:** 
- gee_extraction: 3 testes
- mcda_analysis: 4 testes
- lcoe_calculator: 3 testes
- validation: 2 testes

**Execução:** `pytest` (runs all)

---

#### **SUBMISSION_READY/** (Subpasta - Backup)
```
Coding parts/SUBMISSION_READY/
├── SOL.tex                 [Cópia manuscrito]
├── referencias.bib         [Cópia bibliografia]
└── figuras/                [Cópia figuras]
```

**O que é:** Versão backup pronta submissão  
**Status:** Duplicado de `manuscript/` (pode arquivar)

---

## 🎤 PRESENTATIONS/ FOLDER

### **Estrutura**
```
Full project/presentations/
├── deck/                        [PRESENTATION DECK - 7 SLIDES]
│   ├── PRESENTATION_DECK_OUTLINE.md              [Script + speaker notes]
│   ├── PRESENTATION_DECK_OUTLINE.md.bak          [Backup]
│   ├── PRESENTATION_DECK_OUTLINE.pptx            [PowerPoint editável]
│   └── PRESENTATION_DECK_OUTLINE.pdf             [PDF printável]
│
└── one-page/                    [ONE-PAGE SUMMARY - EXECUTIVE]
    ├── ONE_PAGE_SUMMARY.md                       [Markdown 496 palavras]
    ├── ONE_PAGE_SUMMARY.pdf                      [PDF printável]
    ├── ONE_PAGE_SUMMARY.png                      [Imagem high-res]
    └── ONE_PAGE_SUMMARY.html                     [?? May exist]
```

### **Conteúdo Detalhado**

#### **PRESENTATION_DECK_OUTLINE.md**
**O que é:** 7-slide presentation (6 minutos) com scripts orador completos  
**Tamanho:** ~2.000 linhas markdown  
**Slides:**
1. **Título + Hook** (30s) — Angola dark/bright map, question gancho
2. **Problema** (60s) — 3 challenges + 4 "why now" factors
3. **Solução** (90s) — 4-step MCDA framework
4. **Resultados** (60s) — 3 priority zones, financeiro
5. **Diferenciação** (60s) — vs. precedentes, ODS alignment
6. **Timeline + Partnerships** (90s) — 2026-2027 roadmap

**Cada slide inclui:**
- Sugestão visual
- Bullets principais
- **Script orador** (palavra por palavra)
- Timing (segundos)

**Formato:** Pronto adaptar para PowerPoint

---

#### **ONE_PAGE_SUMMARY.md**
**O que é:** Executive summary 496 palavras (conference abstract format)  
**Conteúdo:**
- Problema (2 linhas)
- Solução (3 linhas)
- Metodologia (3 linhas)
- Resultados (4 linhas)
- Originalidade (2 linhas)
- Implicações (2 linhas)
- Tabela 12-critérios competitividade (com scores)
- Requisitos financiamento (USD 50.5M / 4 fases)
- Timeline (6 meses)

**Uso:** Submissão revistas, financiadores, conference submissions

---

## 📚 DOCS/ FOLDER

### **Estrutura**
```
Full project/docs/
├── INDEX.md                     [ÍNDICE DOCUMENTAÇÃO]
│
├── 📁 audit/                    [AUDIT REPORTS]
│   └── [Quality checks, issue tracking]
│
├── 📁 phases/                   [PHASE COMPLETION REPORTS 1-4]
│   ├── PHASE1_COMPLETION_*.md
│   ├── PHASE2_COMPLETION_*.md
│   ├── PHASE3_COMPLETION_*.md
│   └── PHASE4_COMPLETION_*.md
│
├── 📁 analysis/                 [PROJECT ANALYSIS]
│   ├── PROJECT_ANALYSIS_REPORT.md
│   └── ANALISE_INTEGRADA_PROPOSTA_VS_REALIDADE.md
│
├── 📁 resources/                [RESOURCE MATERIALS]
│   ├── capacity/                [CAPACITY REPORTS]
│   │   ├── RELATORIO_CAPACIDADE_METODOLOGIA.md
│   │   ├── RESPOSTA_FINAL_CAPACIDADE.md
│   │   ├── MIT_SUMMARY_CAPABILITY.md
│   │   └── RECOMENDACOES_OPERACIONAIS_LATEX.md
│   │
│   ├── checklists/              [CHECKLISTS]
│   │   ├── CHECKLIST_SUBMISSAO_FINAL.md
│   │   ├── CHECKLIST_CAPACIDADE_DETALHADO.md
│   │   └── RISK_SCREENING_CHECKLIST.md
│   │
│   └── references/              [REFERENCE DOCS]
│       ├── INDICE_DOCUMENTOS_CRIADOS.md
│       ├── MAPA_EVIDENCIAS_CODIGO.md
│       ├── MASTER_SUMMARY_FINAL.md
│       └── PAPER_COMPLETION_REPORT.md
│
└── 📁 archive/                  [OLD/SUPERSEDED DOCS]
    ├── GEESP-COMPLETION-SUMMARY.md
    ├── IMPROVEMENTS_SUMMARY_FEB8.md
    ├── PLANO_EXECUCAO_72H.md
    ├── README-COMPLETION.md
    └── REPRODUCIBILITY.md
```

### **Conteúdo**

**INDEX.md** — Master index docs  
**audit/** — Quality reports (code review, audit trails)  
**phases/** — Phase 1-4 completion status + executive summaries  
**analysis/** — Project analysis + alignment reports  
**resources/capacity/** — Capability assessments + recommendations  
**resources/checklists/** — Implementation checklists  
**resources/references/** — Reference materials + evidence mapping  
**archive/** — Superseded/old documents

---

## 📋 SUPPORT/ FOLDER

### **Estrutura**
```
Full project/support/
├── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md  [5 LETTER TEMPLATES]
├── DEMO_SCRIPT.md                              [DEMO TALKING POINTS]
├── FAQ_GEESP.md                                [FREQUENTLY ASKED QUESTIONS]
├── TECHNOLOGY_SELECTION_MATRIX_PHASE4.md       [TECH SELECTION TABLE]
│
└── 📁 guides/                                  [OPERATIONAL GUIDES]
    └── [Various operational guides if exist]
```

### **Conteúdo Detalhado**

#### **INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md**
**O que é:** 5 modelos cartas (customizáveis)  
**Modelos:**
1. Ministério MINEA (alinhamento estratégia)
2. Banco Multilateral (viabilidade + ROI)
3. ONG/PNUD (validação comunitária)
4. Governo Local (aceitação sítios)
5. Operador EDA (integração rede)

**Cada modelo:**
- [ ] Cabeçalho institucional
- [ ] Corpo (3 parágrafos)
- [ ] Placeholders `[INSIRA...]`
- [ ] Assinatura linha

**Uso:** 
1. Copy modelo
2. Replace placeholders
3. Imprima papel timbrado
4. Assine + colecte

---

#### **DEMO_SCRIPT.md**
**O que é:** Talking points para apresentação live demo  
**Duração:** ~10 minutos  
**Conteúdo:**
- Intro 2 min (problema + solução)
- Dashboard walkthrough 5 min (4 tabs)
- Results interpretation 2 min
- Q&A prep 1 min

---

#### **FAQ_GEESP.md**
**O que é:** Perguntas frequentes + respostas  
**Q&A típico:**
- "Como funciona AHP ponderação?"
- "Quão confiáveis são dados satélite?"
- "Quanto custa implementar um sistema?"
- "Qual é o LCOE final?"

---

## 🌍 TRANSLATIONS/ FOLDER

### **Estrutura**
```
Full project/translations/
└── 📁 pt/                              [PORTUGUESE TRANSLATIONS - COMPLETO]
    ├── README_TRANSLATIONS.md          [Guia navegação PT]
    ├── DELIVERY_MANIFEST.md            [Manifesto qualidade entrega]
    │
    ├── 📁 manuscript/                  [MANUSCRITO PT]
    │   └── SOL.tex                     [2.000 linhas português]
    │
    ├── 📁 coding/                      [GUIAS TÉCNICOS PT]
    │   ├── README.md                   [280 linhas]
    │   ├── INSTALL.md                  [160 linhas]
    │   └── QUICKSTART.md               [260 linhas]
    │
    ├── 📁 presentations/               [APRESENTAÇÕES PT]
    │   ├── ONE_PAGE_SUMMARY_PT.md      [496 palavras summary]
    │   └── PRESENTATION_DECK_OUTLINE_PT.md [7-slide script]
    │
    └── 📁 support/                     [SUPORTE PT]
        └── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md [5 templates]
```

### **Conteúdo**

**Completo Portuguese Translation** — Todas 7 ficheiros principais  
**Status:** ✅ QA verified (0 erros sintaxe)  
**Cobertura:** ~8.500 linhas traduzidas  

**Ficheiros:**
1. `manuscript/SOL.tex` — Manuscrito 2.000+ linhas português
2. `coding/README.md` — Framework overview técnico
3. `coding/INSTALL.md` — Passo-a-passo instalação
4. `coding/QUICKSTART.md` — 5-30 min quick start
5. `presentations/ONE_PAGE_SUMMARY_PT.md` — Executivo 496 palavras
6. `presentations/PRESENTATION_DECK_OUTLINE_PT.md` — 7-slide script + speaker notes
7. `support/INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md` — 5 letter templates

---

## 📄 SUBMISSION_READY/ FOLDER

### **Estrutura**
```
Full project/SUBMISSION_READY/
├── README.txt                   [Info ficheiro]
├── SOL.tex                      [Manuscrito pronto submissão]
├── SOL.aux                      [LaTeX auxiliary (compilação)]
├── SOL.bbl                      [Bibliography compiled]
├── SOL.blg                      [Bibliography log]
├── SOL.toc                      [Table of contents]
└── 📁 figuras/                  [TODAS FIGURAS]
    └── [4 figure files]
```

**O que é:** Versão submission-ready (pode arquivar este posterior)  
**Status:** Backup — conteúdo duplicado em `manuscript/`

---

## 📝 WRITING/ FOLDER

### **Estrutura**
```
Full project/writing/
├── papier.tex                   [RASCUNHO MANUSCRITO]
├── SOL.tex                      [CÓPIA MANUSCRITO]
├── SOL_backup_20260207_230841.tex [BACKUP COM TIMESTAMP]
├── SOL.bbl                      [BIBLIOGRAPHY COMPILED]
├── SOLV2IMPROVBYPT.TEX          [VERSÃO EARLIER]
├── referencias.bib              [CÓPIA REFERENCES]
│
└── 📁 figuras/                  [FIGURES PASTE/DRAFT]
    ├── mapa_aptidao_integrada.tex
    ├── mapa_distanciarede.tex
    ├── mapa_irradiacao.tex
    ├── mapa_populacao.tex
    └── [writing/ subdirectory]
```

**O que é:** Pasta rascunhos + backups (pode arquivar)  
**Status:** Superseded — usar `manuscript/` em vez disto

---

## 🔧 SCRIPTS/ FOLDER

### **Estrutura**
```
Full project/scripts/
└── create_one_page_visual.py    [SCRIPT CRIAR ONE-PAGE VISUAL]
```

**O que é:** Python script gerar imagem one-page summary  
**Entrada:** Markdown data (texto + tabelas)  
**Saída:** PNG/PDF image high-res

---

## 📁 .GITHUB/ FOLDER

### **Estrutura**
```
Full project/.github/
└── ISSUE_TEMPLATE/              [GitHub issue templates]
    ├── bug_report.md
    ├── feature_request.md
    └── [outros templates]
```

**O que é:** GitHub automation  
**Uso:** Templates para reportar bugs, feature requests

---

## 🔍 QUICK REFERENCE TABLE

| Pasta | Propósito | Ficheiro Importante | Leia Primeiro |
|-------|----------|-------|-------|
| **manuscript/** | Documento científico | SOL.tex (2.000 linhas) | SOL.tex sections 1-3 |
| **Coding parts/geesp-angola/** | Código + framework | README.md, scripts/ | README.md |
| **presentations/** | Apresentações | PRESENTATION_DECK_OUTLINE.md | .md version |
| **docs/** | Documentação | INDEX.md, reports/ | INDEX.md |
| **support/** | Templates/FAQ | INSTITUTIONAL_SUPPORT_LETTERS.md | Conforme necessidade |
| **translations/pt/** | Português completo | README_TRANSLATIONS.md | .md version |
| **SUBMISSION_READY/** | Backup submissão | SOL.tex | [Archive — use manuscript/] |
| **writing/** | Rascunhos/backup | SOL.tex | [Archive — use manuscript/] |
| **.github/** | GitHub automation | ISSUE_TEMPLATE/ | [conforme need] |

---

## 🎯 NAVEGAÇÃO POR PROPÓSITO

### **Se quer MANUSCRITO:**
```
→ Full project/manuscript/SOL.tex
  - Versão principal (use isto)
  - 2.000 linhas LaTeX português
  - Abra em Overleaf ou editor LaTeX
```

### **Se quer CÓDIGO:**
```
→ Full project/Coding parts/geesp-angola/
  - README.md: overview + como correr app unificada
  - geesp_unified_app.py: app principal Streamlit
  - launch_app.bat / launch_app.sh / launch_app.py: launchers
  - scripts/: código Python
  - dashboard/: app web Streamlit (versão legacy)
  - tests/: testes pytest
```

### **Se quer APRESENTAR:**
```
→ Full project/presentations/
  - deck/PRESENTATION_DECK_OUTLINE.md: 7-slide script
  - one-page/ONE_PAGE_SUMMARY.md: executive 1-pager
  - .pptx e .pdf files editáveis
```

### **Se quer DOCUMENTAÇÃO:**
```
→ Full project/docs/
  - INDEX.md: master index
  - reports/: phase completion
  - resources/: checklists + capacidade
```

### **Se quer PORTUGUÊS:**
```
→ Full project/translations/pt/
  - README_TRANSLATIONS.md: guia PT
  - manuscript/, coding/, presentations/: tudo traducido
  - 7 ficheiros, ~8.500 linhas
```

### **Se quer TEMPLATES/CARTAS:**
```
→ Full project/support/
  - INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md
  - 5 modelos customizáveis
  - FAQ_GEESP.md: perguntas frequentes
```

### **Se quer ARQUIVOS / BACKUPS:**
```
→ Full project/ARCHIVE/
→ Full project/writing/
→ Full project/SUBMISSION_READY/
→ Full project/docs/archive/

Resumo detalhado:
  - ARCHIVE/ARCHIVE_INDEX.md
```

---

## 📊 FICHEIRO SIZE ESTIMATES

| Ficheiro | Lines | Size MB | Type |
|----------|-------|---------|------|
| manuscript/SOL.tex | 2.000+ | 1.5 | LaTeX |
| Coding parts/geesp-angola/ | 1.500+ | 2.0 | Python |
| presentations/deck/ | 2.000 | 0.5 | Markdown |
| docs/ | 3.000+ | 1.0 | Markdown |
| translations/pt/ | 8.500+ | 3.0 | Mixed |
| Total project | ~18.000 | ~8 | Mixed |

---

## ✅ GUIA LEITURA RECOMENDADA

### **15 Minutos**
1. Este ficheiro (PROJECT_FOLDER_GUIDE.md)
2. README.md (root)
3. MASTER_INDEX_DASHBOARD_FEB9.md

### **1 Hora**
- Acima + manuscript/SOL.tex (intro sections)
- Acima + presentations/PRESENTATION_DECK_OUTLINE.md

### **4 Horas (Onboarding**
- Tudo acima +
- Coding parts/geesp-angola/README.md
- translations/pt/README_TRANSLATIONS.md
- docs/INDEX.md

### **1 Dia (Deep Dive)**
- Tudo acima +
- Explore Coding parts/ tree
- Ler alguns scripts Python
- Review tests/

---

## 🏗️ ESTRUTURA PROPOSTA (Future)

Para melhor organização (recomendação):

```
Full project/ (reorganized)
├── MANUSCRIPT/           (merge: manuscript/ + SUBMISSION_READY/)
├── CODE/                 (rename: Coding parts/geesp-angola/)
├── PRESENTATIONS/        (keep: presentations/)
├── DOCUMENTATION/        (rename: docs/ + support/)
├── TRANSLATIONS/         (keep: translations/)
├── ROOT_DOCS/           (README.md + INDEX metadocs)
└── ARCHIVE/             (writing/, old files)
```

---

## 📞 QUICK HELP

**Tenho dúvida sobre...?**

| Pergunta | Resposta | Ficheiro |
|----------|----------|----------|
| Qual é estrutura projeto? | Este ficheiro | PROJECT_FOLDER_GUIDE.md |
| Como submeter manuscrito? | Instruções + template | manuscript/SOL_SUBMISSION.tex |
| Como executar código? | Passo-a-passo | Coding parts/geesp-angola/INSTALL.md |
| Como usar dashboard? | Demo + screenshots | Coding parts/geesp-angola/QUICKSTART.md |
| Tenho dúvida FAQ? | Respostas | support/FAQ_GEESP.md |
| Quero português? | Pasta completa | translations/pt/ |
| O que falta projeto? | 63 items listado | MISSING_ITEMS_COMPREHENSIVE_FEB9.md |
| Quais erros corrigir? | 9 erros encontrado | ORGANIZATION_CORRECTIONS_FEB9.md |

---

**Documento Status:** ✅ Completo  
**Versão:** 1.0  
**Criado:** Fevereiro 9, 2026  
**Próxima revisão:** March 1, 2026

---

*Guia criado por Rocélio Silva | MIT Global Classroom Energy Initiative*
