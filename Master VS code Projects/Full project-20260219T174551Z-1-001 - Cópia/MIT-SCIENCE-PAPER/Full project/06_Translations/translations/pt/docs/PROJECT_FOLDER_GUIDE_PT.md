# 📖 GUIA COMPLETO PASTAS DO PROJETO & ÍNDICE
**Data:** Fevereiro 9, 2026  
**Propósito:** Explicação completa da estrutura de pastas + conteúdo de cada ficheiro  
**Âmbito:** 100% do projeto GEESP-Angola

---

## 🗺️ MAPA VISUAL DA ESTRUTURA

```
Full project/ (Raiz)
│
├── 📘 MANUSCRIPT/               ← Documento científico
├── 💻 Coding parts/             ← Todo o código
├── 🎤 presentations/            ← Apresentações
├── 📚 docs/                     ← Documentação
├── 📋 support/                  ← Suporte/templates
├── 🌍 translations/             ← Traduções português
├── 📄 SUBMISSION_READY/         ← Versão pronta para entrega
├── 📝 writing/                  ← Rascunhos/backup
├── 🔧 scripts/                  ← Scripts diversos
└── 📑 FICHEIROS RAIZ            ← Master docs + README
```

---

## 📄 FICHEIROS NO NÍVEL RAIZ (Raiz do Projeto)

### **Navegação e Índice**
```
Full project/
├── README.md                                    [VISÃO GERAL DO PROJETO]
├── MASTER_INDEX_DASHBOARD_FEB9.md              [ÍNDICE MESTRE - COMECE AQUI]
├── ORGANIZATION_CORRECTIONS_FEB9.md            [ERROS + ESTRUTURA PROPOSTA]
├── MISSING_ITEMS_COMPREHENSIVE_FEB9.md        [63 LACUNAS DO PROJETO]
└── PORTUGUESE_TRANSLATION_COMPLETION_REPORT.md [STATUS TRADUÇÕES PT]
```

**O que contém:**
- `README.md` — Visão geral do projeto, 445 linhas, guia rápido para começar
- `MASTER_INDEX_DASHBOARD_FEB9.md` — Índice navegação + dashboard de status
- `ORGANIZATION_CORRECTIONS_FEB9.md` — Erros encontrados + organização proposta
- `MISSING_ITEMS_COMPREHENSIVE_FEB9.md` — 63 items faltando (TIER 1/2/3)
- `PORTUGUESE_TRANSLATION_COMPLETION_REPORT.md` — Status de 7 ficheiros PT traduzidos

**→ LEIA PRIMEIRO:** `MASTER_INDEX_DASHBOARD_FEB9.md` para visão geral

---

### **Auditoria e Qualidade**
```
├── COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md     [AUDITORIA 9-DIMENSÕES]
├── COMPREHENSIVE_MISSING_PARTS_AUDIT.md        [AUDITORIA APROFUNDADA DE LACUNAS]
├── MISSING_PARTS_ACTION_CHECKLIST.md          [ITENS DE AÇÃO RÁPIDA]
├── PROJECT_COMPLETENESS_DASHBOARD.md          [STATUS DE CONCLUSÃO 62%]
├── PROJECT_COMPLETION_CHECKLIST.md            [CHECKLIST FASES 1-4]
├── PHASE1_COMPLETION_REPORT.md                [STATUS FASE 1]
└── PHASE1_EXECUTIVE_SUMMARY.md                [SUMÁRIO EXECUTIVO FASE 1]
```

**O que contém:**
- Auditorias de 9 dimensões (rigor científico, formato, metodologia, etc.)
- Checklists de ação prioritários
- Status de conclusão por fase (1-4)
- Sumários executivos

**→ LEIA SE:** Precisa de uma auditoria técnica ou auditoria de conformidade

---

## 📘 PASTA MANUSCRIPT/ (Manuscrito)

### **Estrutura**
```
Full project/manuscript/
├── SOL.tex                      [MANUSCRITO PRINCIPAL - 2.000 LINHAS]
├── SOL_SUBMISSION.tex           [VERSÃO PRONTA PARA SUBMISSÃO]
├── referencias.bib              [BIBLIOGRAFIA COMPLETA - 15 REFS]
├── referencias_submission.bib   [BIBLIOGRAFIA PARA SUBMISSÃO]
└── figures/                     [TODAS AS FIGURAS LATEX]
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
2. **Resumos** — Português + Inglês
3. **Destaques de Pesquisa** — 4 contribuições principais
4. **Introdução** — Crise energética em Angola + contexto
5. **Revisão de Literatura** — 15 referências
6. **Metodologia** — Framework GEESP-Angola, AHP, Sobreposição Ponderada
7. **Resultados** — 3 zonas (Cacula 0.83, Humpata 0.79, Quilengues 0.76)
8. **Discussão** — Implicações, validação, limitações
9. **Conclusões** — 4 achados principais
10. **Apêndices A-D** — ACV, dados comunitários, matrizes AHP, protocolo validação

**Ficheiros Relacionados:**
- `referencias.bib` — 15 referências científicas
- `figures/` — 4 mapas principais (LaTeX tikz)

**Erros Conhecidos:**
- ⚠️ Aptidão Cacula: 0.71 vs 0.83 (inconsistência — usar 0.83)
- ⚠️ Data: "Fevereiro 9, 2025" deve ser 2026

**Status:** ✅ Pronto para submissão (1-2 correções pendentes)

---

#### **SOL_SUBMISSION.tex**
**O que é:** Cópia limpa para submissão de revista (sem comentários/rascunhos)  
**Diferença vs. SOL.tex:** Remove notas TODO, limpa formatação, valida referências  
**Status:** ✅ Pronto para usar

---

#### **referencias.bib**
**O que é:** Ficheiro BibTeX com 15 referências científicas  
**Formato:** Padrão BibTeX (usado por Overleaf, LaTeX CLI)  
**Conteúdo:**
- 3 artigos em AMCM/SIG (Saaty, Malczewski)
- 4 artigos sobre energia solar em África/Angola
- 5 artigos sobre mini-redes + tecnologia solar
- 3 artigos sobre dados satélite (GEE, VIIRS, Sentinel-2)

**Uso:** `\cite{chave}` em SOL.tex puxa referências deste ficheiro

---

#### **figures/** (Pasta)
**O que contém:** 4 mapas principais em TikZ
- `mapa_aptidao_integrada.tex` — Mapa de aptidão integrada (Cacula, Humpata, Quilengues)
- `mapa_distanciarede.tex` — Distância à rede elétrica
- `mapa_irradiacao.tex` — Irradiação solar (GHI)
- `mapa_populacao.tex` — Densidade populacional (VIIRS)

**Tipo:** Ficheiros LaTeX TikZ (gráficos vetoriais)  
**Uso:** Incluídos em SOL.tex com `\input{figures/mapa_*.tex}`

---

## 💻 PASTA CODING PARTS/ (Código)

### **Estrutura**
```
Full project/Coding parts/
├── startofthecode               [?? - Ficheiro desconhecido]
└── geesp-angola/                [REPOSITÓRIO CÓDIGO PRINCIPAL]
    ├── README.md                [Visão geral do framework]
    ├── requirements.txt         [Dependências Python]
    ├── pyproject.toml           [Setup pytest, linting]
    ├── config.json              [Configurações]
    ├── Dockerfile               [Imagem Docker]
    │
    ├── 📁 scripts/              [SCRIPTS PYTHON]
    │   ├── gee_extraction.py    [Extração de dados da Google Earth Engine]
    │   ├── mcda_analysis.py     [Análise multicritério AHP + Sobreposição Ponderada]
    │   ├── data_processing.py   [Normalização de dados]
    │   ├── lcoe_calculator.py   [Cálculo de LCOE]
    │   ├── utils.py             [Funções auxiliares]
    │   └── __init__.py
    │
    ├── 📁 dashboard/            [APP STREAMLIT - INTERFACE WEB]
    │   ├── app.py               [Aplicação principal (4 abas)]
    │   ├── pages/               [Páginas/widgets]
    │   │   ├── 1_exploracao.py  [Aba 1: Exploração de dados]
    │   │   ├── 2_mcda.py        [Aba 2: Interface AMCM]
    │   │   ├── 3_resultados.py  [Aba 3: Mapas de resultados]
    │   │   └── 4_lcoe.py        [Aba 4: Calculadora LCOE]
    │   ├── assets/              [Imagens, CSS]
    │   └── streamlit_config.toml [Configuração da IU]
    │
    ├── 📁 notebooks/            [JUPYTER NOTEBOOKS]
    │   ├── 01_extracao_gee.ipynb      [Notebook: Extração GEE]
    │   ├── 02_processamento_dados.ipynb [Processamento + normalização]
    │   ├── 03_ahp_ponderacao.ipynb     [Demo de ponderação AHP]
    │   └── 04_validacao_resultados.ipynb [Validação de resultados]
    │
    ├── 📁 data/                 [DADOS DE INPUT + OUTPUT]
    │   ├── raw/                 [Dados brutos (GEE, shapefile)]
    │   ├── processed/           [Dados processados]
    │   └── example/             [Dados de demonstração para testes]
    │
    ├── 📁 monitoring/           [APP DE MONITORAMENTO]
    │   ├── monitoring_app.py    [App de monitoramento 24x7]
    │   └── __init__.py
    │
    ├── 📁 tests/                [TESTES UNITÁRIOS]
    │   ├── test_gee_extraction.py
    │   ├── test_mcda_analysis.py
    │   ├── test_lcoe_calculator.py
    │   └── [11 ficheiros de teste adicionais - todos passando 12/12]
    │
    ├── 📁 docs/                 [DOCUMENTAÇÃO DO CÓDIGO]
    │   ├── INSTALL.md
    │   ├── USAGE.md
    │   ├── API.md
    │   └── METODOLOGIA.md
    │
    ├── 📁 .github/              [GITHUB ACTIONS]
    │   └── workflows/           [Pipelines CI/CD]
    │       ├── tests.yml        [Testes automatizados]
    │       └── deploy.yml       [Automatização de implementação]
    │
    ├── .gitignore               [Ficheiros a ignorar git]
    ├── .pre-commit-config.yaml  [Hooks pré-commit]
    ├── LICENSE                  [Licença MIT]
    ├── .mypy_cache/             [Cache de verificação de tipo]
    ├── .pytest_cache/           [Cache de teste]
    ├── __pycache__/             [Cache Python]
    │
    ├── 📄 DOCUMENTAÇÃO MARKDOWN:
    ├── CODE_GUIDE.md            [Explicação do código]
    ├── CHANGELOG.md             [Histórico de mudanças]
    ├── CONTRIBUTING.md          [Diretrizes de contribuição]
    ├── DEPLOYMENT.md            [Instruções de implementação]
    ├── MONITORING.md            [Instruções de monitoramento]
    ├── MONITORING_IMPLEMENTATION.md
    ├── INTEGRATION_GUIDE.md      [Integração com sistemas]
    ├── GITHUB_SETUP.md          [Setup do GitHub Actions]
    ├── GITHUB_DEPLOY.md         [Implementação via GitHub]
    ├── INSTALL.md               [Instalação passo-a-passo]
    ├── QUICKSTART.md            [Introdução 5-30 min]
    ├── README.docker.md         [Setup Docker]
    ├── QUICK_REFERENCE.md       [Cheat sheet de funções]
    ├── PROJECT_STATUS.md        [Status atual]
    ├── PROJECT_SUMMARY.md       [Sumário do projeto]
    ├── AUDIT_REPORT.md          [Auditoria de código]
    │
    ├── 🔧 SHELL SCRIPTS:
    ├── run_dashboard.bat        [Lançar dashboard (Windows)]
    ├── run_dashboard.sh         [Lançar dashboard (Linux/Mac)]
    ├── run_monitoring.bat       [Lançar monitoramento (Windows)]
    └── run_monitoring.sh        [Lançar monitoramento (Linux/Mac)]
```

### **Conteúdo Detalhado**

#### **README.md** (geesp-angola)
**O que é:** Visão geral do framework Python  
**Conteúdo:**
- Descrição de 6 módulos principais (GEE, AMCM, Dashboard, LCOE, Monitoramento, Utils)
- Arquitetura do projeto
- Casos de uso (3 personas)
- Fluxo de trabalho
- Requisitos do sistema

**Uso:** Primeira leitura para novos developadores

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

**Uso:** `pip install -r requirements.txt` para configurar ambiente

---

#### **scripts/** (Pasta Python)
**Ficheiros principais:**

- **gee_extraction.py** — Extrai dados da Google Earth Engine
  - Input: Geometria (shapefile/bounds)
  - Output: 6 rasters (GHI, slope, population, distance, NDVI, nightlights)
  - Engine: GEE Python API
  
- **mcda_analysis.py** — Framework AMCM
  - Input: 6 rasters normalizados
  - Ponderação AHP (método Saaty)
  - Sobreposição Ponderada
  - Output: Mapa de aptidão + classificação de zona
  
- **data_processing.py** — Normalização
  - Escala Min-Max
  - Tratamento de critérios de custo vs. benefício
  - Controle de qualidade
  
- **lcoe_calculator.py** — Economia de LCOE
  - Taxa de desconto, vida útil, O&M
  - Output: USD/kWh por zona
  
- **utils.py** — Funções auxiliares
  - I/O de ficheiros
  - Plotting
  - Validação de dados

---

## 🎤 PASTA PRESENTATIONS/ (Apresentações)

### **Estrutura**
```
Full project/presentations/
├── deck/                        [BARALHO DE APRESENTAÇÃO - 7 SLIDES]
│   ├── PRESENTATION_DECK_OUTLINE.md              [Script + notas do orador]
│   ├── PRESENTATION_DECK_OUTLINE.md.bak          [Backup]
│   ├── PRESENTATION_DECK_OUTLINE.pptx            [PowerPoint editável]
│   └── PRESENTATION_DECK_OUTLINE.pdf             [PDF imprimível]
│
└── one-page/                    [RESUMO DE UMA PÁGINA - EXECUTIVO]
    ├── ONE_PAGE_SUMMARY.md                       [Markdown 496 palavras]
    ├── ONE_PAGE_SUMMARY.pdf                      [PDF imprimível]
    ├── ONE_PAGE_SUMMARY.png                      [Imagem de alta resolução]
    └── ONE_PAGE_SUMMARY.html                     [?? Pode existir]
```

### **Conteúdo Detalhado**

#### **PRESENTATION_DECK_OUTLINE.md**
**O que é:** Apresentação de 7 slides (6 minutos) com scripts de orador completos  
**Tamanho:** ~2.000 linhas de markdown  
**Slides:**
1. **Título + Gancho** (30s) — Mapa Angola claro/escuro, pergunta gancho
2. **Problema** (60s) — 3 desafios + 4 fatores "por quê agora"
3. **Solução** (90s) — Framework AMCM de 4 passos
4. **Resultados** (60s) — 3 zonas prioritárias, financeiro
5. **Diferenciação** (60s) — vs. precedentes, alinhamento ODS
6. **Timeline + Parcerias** (90s) — Roadmap 2026-2027

**Cada slide inclui:**
- Sugestão visual
- Bullets principais
- **Script do orador** (palavra por palavra)
- Timing (segundos)

**Formato:** Pronto para adaptar para PowerPoint

---

#### **ONE_PAGE_SUMMARY.md**
**O que é:** Sumário executivo de 496 palavras (formato de resumo de conferência)  
**Conteúdo:**
- Problema (2 linhas)
- Solução (3 linhas)
- Metodologia (3 linhas)
- Resultados (4 linhas)
- Originalidade (2 linhas)
- Implicações (2 linhas)
- Tabela com 12 critérios de competitividade (com scores)
- Requisitos de financiamento (USD 50.5M / 4 fases)
- Timeline (6 meses)

**Uso:** Submissão de revistas, financiadores, submissões de conferências

---

## 📚 PASTA DOCS/ (Documentação)

### **Estrutura**
```
Full project/docs/
├── INDEX.md                     [ÍNDICE DE DOCUMENTAÇÃO]
│
├── 📁 audit/                    [RELATÓRIOS DE AUDITORIA]
│   └── [Verificações de qualidade, rastreamento de problemas]
│
├── 📁 phases/                   [RELATÓRIOS DE CONCLUSÃO DE FASES 1-4]
│   ├── PHASE1_COMPLETION_*.md
│   ├── PHASE2_COMPLETION_*.md
│   ├── PHASE3_COMPLETION_*.md
│   └── PHASE4_COMPLETION_*.md
│
├── 📁 analysis/                 [ANÁLISE DO PROJETO]
│   ├── PROJECT_ANALYSIS_REPORT.md
│   └── ANALISE_INTEGRADA_PROPOSTA_VS_REALIDADE.md
│
├── 📁 resources/                [MATERIAIS DE RECURSO]
│   ├── capacity/                [RELATÓRIOS DE CAPACIDADE]
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
│   └── references/              [DOCUMENTOS DE REFERÊNCIA]
│       ├── INDICE_DOCUMENTOS_CRIADOS.md
│       ├── MAPA_EVIDENCIAS_CODIGO.md
│       ├── MASTER_SUMMARY_FINAL.md
│       └── PAPER_COMPLETION_REPORT.md
│
└── 📁 archive/                  [DOCUMENTOS ANTIGOS/OBSOLETOS]
    ├── GEESP-COMPLETION-SUMMARY.md
    ├── IMPROVEMENTS_SUMMARY_FEB8.md
    ├── PLANO_EXECUCAO_72H.md
    ├── README-COMPLETION.md
    └── REPRODUCIBILITY.md
```

### **Conteúdo**

**INDEX.md** — Índice mestre de documentação  
**audit/** — Relatórios de qualidade (análise de código, trilhos de auditoria)  
**phases/** — Status de conclusão das fases 1-4 + sumários executivos  
**analysis/** — Análise do projeto + relatórios de alinhamento  
**resources/capacity/** — Avaliações de capacidade + recomendações  
**resources/checklists/** — Checklists de implementação  
**resources/references/** — Materiais de referência + mapeamento de evidências  
**archive/** — Documentos obsoletos/antigos

---

## 📋 PASTA SUPPORT/ (Suporte)

### **Estrutura**
```
Full project/support/
├── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md  [5 MODELOS DE CARTA]
├── DEMO_SCRIPT.md                              [PONTOS-CHAVE DE DEMONSTRAÇÃO]
├── FAQ_GEESP.md                                [PERGUNTAS FREQUENTES]
├── TECHNOLOGY_SELECTION_MATRIX_PHASE4.md       [TABELA DE SELEÇÃO DE TECNOLOGIA]
│
└── 📁 guides/                                  [GUIAS OPERACIONAIS]
    └── [Vários guias operacionais, se existirem]
```

### **Conteúdo Detalhado**

#### **INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md**
**O que é:** 5 modelos de cartas (customizáveis)  
**Modelos:**
1. Ministério MINEA (alinhamento de estratégia)
2. Banco Multilateral (viabilidade + ROI)
3. ONG/PNUD (validação comunitária)
4. Governo Local (aceitação de sítios)
5. Operador EDA (integração de rede)

**Cada modelo:**
- [ ] Cabeçalho institucional
- [ ] Corpo (3 parágrafos)
- [ ] Placeholders `[INSIRA...]`
- [ ] Linha de assinatura

**Uso:** 
1. Copie o modelo
2. Substitua placeholders
3. Imprima em papel timbrado
4. Assine + colecte

---

#### **DEMO_SCRIPT.md**
**O que é:** Pontos de discussão para demonstração ao vivo  
**Duração:** ~10 minutos  
**Conteúdo:**
- Introdução 2 min (problema + solução)
- Walkthrough do dashboard 5 min (4 abas)
- Interpretação de resultados 2 min
- Prep de P&R 1 min

---

#### **FAQ_GEESP.md**
**O que é:** Perguntas frequentes + respostas  
**P&R típico:**
- "Como funciona a ponderação AHP?"
- "Quão confiáveis são os dados satélite?"
- "Quanto custa implementar um sistema?"
- "Qual é o LCOE final?"

---

## 🌍 PASTA TRANSLATIONS/ (Traduções)

### **Estrutura**
```
Full project/translations/
└── 📁 pt/                              [TRADUÇÕES PARA PORTUGUÊS - COMPLETO]
    ├── README_TRANSLATIONS.md          [Guia navegação PT]
    ├── DELIVERY_MANIFEST.md            [Manifesto de qualidade de entrega]
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
    │   └── PRESENTATION_DECK_OUTLINE_PT.md [script de 7 slides]
    │
    └── 📁 support/                     [SUPORTE PT]
        └── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md [5 modelos]
```

### **Conteúdo**

**Tradução Portuguesa Completa** — Todos os 7 ficheiros principais  
**Status:** ✅ QA verificado (0 erros de sintaxe)  
**Cobertura:** ~8.500 linhas traduzidas  

**Ficheiros:**
1. `manuscript/SOL.tex` — Manuscrito 2.000+ linhas português
2. `coding/README.md` — Visão geral técnica do framework
3. `coding/INSTALL.md` — Instalação passo-a-passo
4. `coding/QUICKSTART.md` — Início rápido 5-30 min
5. `presentations/ONE_PAGE_SUMMARY_PT.md` — Executivo 496 palavras
6. `presentations/PRESENTATION_DECK_OUTLINE_PT.md` — Script de 7 slides + notas do orador
7. `support/INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md` — 5 modelos de cartas

---

## 📄 PASTA SUBMISSION_READY/ (Pronto para Submissão)

### **Estrutura**
```
Full project/SUBMISSION_READY/
├── README.txt                   [Informações do ficheiro]
├── SOL.tex                      [Manuscrito pronto submissão]
├── SOL.aux                      [Auxiliar LaTeX (compilação)]
├── SOL.bbl                      [Bibliografia compilada]
├── SOL.blg                      [Log de bibliografia]
├── SOL.toc                      [Tabela de conteúdos]
└── 📁 figuras/                  [TODAS AS FIGURAS]
    └── [4 ficheiros de figura]
```

**O que é:** Versão pronta para submissão (pode arquivar depois)  
**Status:** Backup — conteúdo duplicado em `manuscript/`

---

## 📝 PASTA WRITING/ (Escrita)

### **Estrutura**
```
Full project/writing/
├── papier.tex                   [RASCUNHO DO MANUSCRITO]
├── SOL.tex                      [CÓPIA DO MANUSCRITO]
├── SOL_backup_20260207_230841.tex [BACKUP COM TIMESTAMP]
├── SOL.bbl                      [BIBLIOGRAFIA COMPILADA]
├── SOLV2IMPROVBYPT.TEX          [VERSÃO ANTERIOR]
├── referencias.bib              [CÓPIA DE REFERÊNCIAS]
│
└── 📁 figuras/                  [FIGURAS PASTE/RASCUNHO]
    ├── mapa_aptidao_integrada.tex
    ├── mapa_distanciarede.tex
    ├── mapa_irradiacao.tex
    ├── mapa_populacao.tex
    └── [subdiretório de escrita/]
```

**O que é:** Pasta de rascunhos + backups (pode arquivar)  
**Status:** Obsoleto — use `manuscript/` em vez disso

---

## 🔧 PASTA SCRIPTS/ (Scripts)

### **Estrutura**
```
Full project/scripts/
└── create_one_page_visual.py    [SCRIPT PARA CRIAR VISUAL DE UMA PÁGINA]
```

**O que é:** Script Python para gerar imagem de resumo de uma página  
**Entrada:** Dados de markdown (texto + tabelas)  
**Saída:** Imagem PNG/PDF de alta resolução

---

## 📁 PASTA .GITHUB/ (.GitHub)

### **Estrutura**
```
Full project/.github/
└── ISSUE_TEMPLATE/              [Modelos de issue do GitHub]
    ├── bug_report.md
    ├── feature_request.md
    └── [outros modelos]
```

**O que é:** Automatização do GitHub  
**Uso:** Modelos para reportar bugs, solicitações de features

---

## 🔍 TABELA DE REFERÊNCIA RÁPIDA

| Pasta | Propósito | Ficheiro Importante | Ler Primeiro |
|-------|----------|-------|-------|
| **manuscript/** | Documento científico | SOL.tex (2.000 linhas) | Seções 1-3 do SOL.tex |
| **Coding parts/geesp-angola/** | Código + framework | README.md, scripts/ | README.md |
| **presentations/** | Apresentações | PRESENTATION_DECK_OUTLINE.md | Versão .md |
| **docs/** | Documentação | INDEX.md, reports/ | INDEX.md |
| **support/** | Templates/FAQ | INSTITUTIONAL_SUPPORT_LETTERS.md | Conforme necessidade |
| **translations/pt/** | Português completo | README_TRANSLATIONS.md | Versão .md |
| **SUBMISSION_READY/** | Backup submissão | SOL.tex | [Arquivo — use manuscript/] |
| **writing/** | Rascunhos/backup | SOL.tex | [Arquivo — use manuscript/] |
| **.github/** | Automatização GitHub | ISSUE_TEMPLATE/ | [Conforme necessidade] |

---

## 🎯 NAVEGAÇÃO POR OBJETIVO

### **Se quer o MANUSCRITO:**
```
→ Full project/manuscript/SOL.tex
  - Versão principal (use isto)
  - 2.000 linhas LaTeX português
  - Abra em Overleaf ou editor LaTeX
```

### **Se quer o CÓDIGO:**
```
→ Full project/Coding parts/geesp-angola/
  - README.md: visão geral
  - scripts/: código Python
  - dashboard/: app web Streamlit
  - tests/: 12 testes (passando)
```

### **Se quer APRESENTAR:**
```
→ Full project/presentations/
  - deck/PRESENTATION_DECK_OUTLINE.md: script de 7 slides
  - one-page/ONE_PAGE_SUMMARY.md: 1-pager executivo
  - Ficheiros .pptx e .pdf editáveis
```

### **Se quer DOCUMENTAÇÃO:**
```
→ Full project/docs/
  - INDEX.md: índice mestre
  - reports/: conclusão de fases
  - resources/: checklists + capacidade
```

### **Se quer PORTUGUÊS:**
```
→ Full project/translations/pt/
  - README_TRANSLATIONS.md: guia PT
  - manuscript/, coding/, presentations/: tudo traduzido
  - 7 ficheiros, ~8.500 linhas
```

### **Se quer TEMPLATES/CARTAS:**
```
→ Full project/support/
  - INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md
  - 5 modelos personalizáveis
  - FAQ_GEESP.md: perguntas frequentes
```

---

## 📊 ESTIMATIVAS DE TAMANHO DOS FICHEIROS

| Ficheiro | Linhas | Tamanho MB | Tipo |
|----------|--------|---------|------|
| manuscript/SOL.tex | 2.000+ | 1.5 | LaTeX |
| Coding parts/geesp-angola/ | 1.500+ | 2.0 | Python |
| presentations/deck/ | 2.000 | 0.5 | Markdown |
| docs/ | 3.000+ | 1.0 | Markdown |
| translations/pt/ | 8.500+ | 3.0 | Mixed |
| Projeto total | ~18.000 | ~8 | Mixed |

---

## ✅ GUIA DE LEITURA RECOMENDADA

### **15 Minutos**
1. Este ficheiro (PROJECT_FOLDER_GUIDE.md)
2. README.md (root)
3. MASTER_INDEX_DASHBOARD_FEB9.md

### **1 Hora**
- Acima + manuscript/SOL.tex (seções de introdução)
- Acima + presentations/PRESENTATION_DECK_OUTLINE.md

### **4 Horas (Onboarding Completo)**
- Tudo acima +
- Coding parts/geesp-angola/README.md
- translations/pt/README_TRANSLATIONS.md
- docs/INDEX.md

### **1 Dia (Aprofundamento)**
- Tudo acima +
- Explore árvore Coding parts/
- Leia alguns scripts Python
- Revise tests/

---

## 🏗️ ESTRUTURA PROPOSTA (Para o Futuro)

Para melhor organização (recomendação):

```
Full project/ (reorganizado)
├── MANUSCRIPT/           (mesclar: manuscript/ + SUBMISSION_READY/)
├── CODE/                 (renomear: Coding parts/geesp-angola/)
├── PRESENTATIONS/        (manter: presentations/)
├── DOCUMENTATION/        (renomear: docs/ + support/)
├── TRANSLATIONS/         (manter: translations/)
├── ROOT_DOCS/           (README.md + metadocs de INDEX)
└── ARCHIVE/             (writing/, ficheiros antigos)
```

---

## 📞 AJUDA RÁPIDA

**Tenho dúvida sobre...?**

| Pergunta | Resposta | Ficheiro |
|----------|----------|----------|
| Qual é a estrutura do projeto? | Este ficheiro | PROJECT_FOLDER_GUIDE_PT.md |
| Como submeter manuscrito? | Instruções + template | manuscript/SOL_SUBMISSION.tex |
| Como executar código? | Passo-a-passo | Coding parts/geesp-angola/INSTALL.md |
| Como usar dashboard? | Demo + screenshots | Coding parts/geesp-angola/QUICKSTART.md |
| Tenho dúvida FAQ? | Respostas | support/FAQ_GEESP.md |
| Quero português? | Pasta completa | translations/pt/ |
| O que falta no projeto? | 63 items listados | MISSING_ITEMS_COMPREHENSIVE_FEB9.md |
| Quais erros corrigir? | 9 erros encontrados | ORGANIZATION_CORRECTIONS_FEB9.md |

---

**Estado do Documento:** ✅ Completo  
**Versão:** 1.0 (Português)  
**Criado:** Fevereiro 9, 2026  
**Próxima revisão:** 1º de marzo, 2026

---

*Guia criado por Rocélio Silva | MIT Global Classroom Energy Initiative*
