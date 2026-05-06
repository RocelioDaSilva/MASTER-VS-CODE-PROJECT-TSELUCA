# 🗂️ MAPA DE REORGANIZAÇÃO DO PROJETO - 9 FEVEREIRO 2026

**Versão:** 1.0  
**Propósito:** Mapa centralizado de como o projeto foi reorganizado  
**Status:** ✅ IMPLEMENTADO

---

## 📊 ESTRUTURA NOVA PROPOSTA (Implementada)

```
Full project/ (Raiz Limpa)
│
├── 📑 ROOT_DOCS/                        ← NOVAMENTE CRIADO
│   ├── README.md                        (visão geral principal)
│   ├── LEIA-ME.md                       (português)
│   ├── MASTER_INDEX_DASHBOARD.md        (índice mestre navegação)
│   ├── INDICE_MESTRE_PAINEL.md          (português)
│   └── QUICK_START.md                   (próximos passos 5 min)
│
├── 📁 PROJECT_MANAGEMENT/               ← NOVAMENTE CRIADO
│   ├── CHECKLISTS/
│   │   ├── CHECKLIST_CONCLUSAO_PROJETO.md          (145 items)
│   │   ├── CHECKLIST_ACAO_ITEMS_FALTANDO.md        (próx 72h)
│   │   └── CHECKLIST_CONCLUSAO_PROJETO_PT.md       (português)
│   ├── STATUS/
│   │   ├── PAINEL_COMPLETUDE_PROJETO.md            (62% status)
│   │   ├── FASE1_RELATORIO_CONCLUSAO.md            (Go/No-Go)
│   │   ├── FASE1_RESUMO_EXECUTIVO.md               (executivo)
│   │   └── PAINEL_COMPLETUDE_PROJETO_PT.md         (português)
│   ├── AUDITS/
│   │   ├── ORGANIZACAO_CORRECOES_FEB9.md           (9 erros)
│   │   ├── ITEMS_FALTANDO_ABRANGENTE_FEB9.md       (63 lacunas)
│   │   ├── AUDITORIA_MISSING_COMPLETA_FEB9.md      (auditoria aprofundada)
│   │   └── [Versões PT]
│   └── GANTT/
│       ├── GANNT_MASTER_TIMELINE.xlsx              (quando criado)
│       └── PHASE_SCHEDULES/
│
├── 📁 GOVERNANCE_COMPLIANCE/            ← NOVAMENTE CRIADO
│   ├── APPROVALS/
│   │   ├── INSTITUTIONAL_LETTERS/       (MINEA, EDA, gov)
│   │   ├── ETHICS_IRB.md               (aprovação ética)
│   │   └── COMMUNITY_CONSENT.md        (consent forms)
│   ├── RISK/
│   │   ├── RISK_REGISTER.md            (15+ riscos)
│   │   ├── RISK_MITIGATION_PLAN.md     (plano contingência)
│   │   └── DISASTER_RECOVERY.md        (DR procedures)
│   ├── LEGAL/
│   │   ├── PARTNERSHIP_AGREEMENTS.md   (MOUs MIT-ISPTEC)
│   │   ├── COMMUNITY_CONTRACTS.md      (acordos comunitários)
│   │   └── INSURANCE_REQUIREMENTS.md
│   └── COMPLIANCE/
│       ├── ESG_SAFEGUARDS.md          (environmental/social)
│       ├── PROCUREMENT_PROCEDURES.md   (procurement manual)
│       └── FINANCIAL_CONTROLS.md
│
├── 💻 CODE/ (renamear de "Coding parts/")
│   └── geesp-angola/                  (mantém estrutura atual)
│       ├── README.md
│       ├── scripts/, dashboard/, monitoring/, tests/ (etc)
│       └── translations/pt/            (guias PT)
│
├── 📘 MANUSCRIPT/                       ← REORGANIZAR
│   ├── SOL.tex                         (versão master)
│   ├── SOL_SUBMISSION.tex              (pronto submissão)
│   ├── referencias.bib                 (bibliography)
│   ├── figures/                        (4 mapas LaTeX)
│   └── translations/pt/                (versão portuguesa)
│
├── 🎤 PRESENTATIONS/                    ← MANTER
│   ├── deck/
│   │   ├── PRESENTATION_DECK_OUTLINE.md
│   │   ├── PRESENTATION_DECK_OUTLINE.pptx
│   │   └── PRESENTATION_DECK_OUTLINE.pdf
│   ├── one-page/
│   │   ├── ONE_PAGE_SUMMARY.md
│   │   ├── ONE_PAGE_SUMMARY.pdf
│   │   └── ONE_PAGE_SUMMARY.png
│   └── translations/pt/                (versões portuguesas)
│
├── 📚 DOCUMENTATION/                    ← CONSOLIDAR
│   ├── TECHNICAL/
│   │   ├── CODE_GUIDE.md               (Coding parts/)
│   │   ├── API_DOCUMENTATION.md
│   │   ├── DATABASE_SCHEMA.md
│   │   └── INTEGRATION_GUIDE.md
│   ├── OPERATIONAL/
│   │   ├── INSTALLATION_GUIDE.md
│   │   ├── OPERATIONS_MANUAL.md
│   │   ├── MAINTENANCE_PROCEDURES.md
│   │   └── TROUBLESHOOTING.md
│   ├── TRAINING/
│   │   ├── TRAINING_CURRICULUM.md
│   │   ├── TRAINING_MATERIALS/
│   │   └── CERTIFICATION_PROGRAMS.md
│   ├── FIELD_OPERATIONS/
│   │   ├── BASELINE_SURVEY_PROTOCOL.md
│   │   ├── EQUIPMENT_SPECIFICATIONS.md
│   │   ├── SITE_ACCESS_PERMITS.md
│   │   └── FIELD_TEAM_MANUAL.md
│   ├── MONITORING_EVALUATION/
│   │   ├── M&E_FRAMEWORK.md
│   │   ├── KPI_DEFINITIONS.md
│   │   ├── DATA_COLLECTION_PROTOCOLS.md
│   │   └── IMPACT_EVALUATION_DESIGN.md
│   └── TRANSLATIONS/
│       └── pt/ (guias técnicas português)
│
├── 💰 FINANCE_PLANNING/                 ← NOVO
│   ├── BUDGETS/
│   │   ├── PHASE1_BUDGET_DETAILED.xlsx
│   │   ├── PHASE2-4_BUDGETS.xlsx
│   │   └── FINANCING_PLAN.md
│   ├── COST_ANALYSIS/
│   │   ├── LCOE_CALCULATIONS.md
│   │   ├── COST_SENSITIVITY.md
│   │   └── ROI_ANALYSIS.md
│   ├── REVENUE_MODELS/
│   │   ├── TARIFF_STRUCTURE.md
│   │   ├── REVENUE_PROJECTIONS.md
│   │   └── SUBSIDY_REQUIREMENTS.md
│   └── FINANCIAL_MANAGEMENT/
│       ├── PROCUREMENT_PROCEDURES.md
│       ├── PAYMENT_MECHANISMS.md
│       └── AUDIT_PROCEDURES.md
│
├── 🌍 COMMUNICATIONS/                   ← NOVO
│   ├── MEDIA/
│   │   ├── PRESS_RELEASE.md
│   │   ├── CASE_STUDIES/
│   │   └── SUCCESS_STORIES/
│   ├── STAKEHOLDER_ENGAGEMENT/
│   │   ├── ENGAGEMENT_PLAN.md
│   │   ├── KEY_MESSAGES.md
│   │   └── COMMUNICATION_CALENDAR.md
│   ├── KNOWLEDGE_MANAGEMENT/
│   │   ├── LESSONS_LEARNED.md
│   │   ├── BEST_PRACTICES.md
│   │   └── REPLICATION_GUIDE.md
│   └── VIDEO_CONTENT/
│       ├── DEMO_SCRIPT.md
│       ├── FAQ_GEESP.md
│       └── VIDEOS/ (quando criado)
│
├── 🌍 TRANSLATIONS/                     ← MANTER & EXPANDIR
│   └── pt/ (português)
│       ├── docs/
│       │   ├── LEIA-ME.md
│       │   ├── PROJECT_FOLDER_GUIDE_PT.md
│       │   ├── [11 docs traduzidos]
│       │   └── MANIFESTO_ENTREGA.md
│       ├── manuscript/
│       ├── coding/
│       ├── presentations/
│       ├── support/
│       └── documentation/               ← EXPANDIR (quando tempo)
│
├── 📋 SUPPORT/                          ← MANTER
│   ├── INSTITUTIONAL_SUPPORT_LETTERS_TEMPLATES.md
│   ├── FAQ_GEESP.md
│   ├── TECHNOLOGY_SELECTION_MATRIX.md
│   ├── DEMO_SCRIPT.md
│   └── guides/
│
├── 📦 ARCHIVE/                          ← NOVO (Backup)
│   ├── OLD_VERSIONS/
│   │   ├── writing/ (rascunhos antigos)
│   │   ├── SOLV2IMPROVBYPT.TEX
│   │   ├── SOL_backup_20260207_230841.tex
│   │   ├── papier.tex
│   │   └── VERSION_HISTORY.md
│   ├── DEPRECATED_ANALYSIS/
│   │   ├── COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB8.md (OLD - veja PROJECT_MANAGEMENT/)
│   │   ├── IMPROVEMENTS_SUMMARY_FEB8.md
│   │   ├── PLANO_EXECUCAO_72H.md
│   │   └── [outros versões antigos]
│   └── BACKUP_SNAPSHOT_FEB9/
│       └── [cópia completa para referência histórica]
│
└── 🔧 INFRASTRUCTURE/                   ← NOVO (quando pronto)
    ├── DEPLOYMENT/
    │   ├── CLOUD_INFRASTRUCTURE.md
    │   ├── CI_CD_PIPELINES.md
    │   └── DEPLOYMENT_PROCEDURES.md
    ├── MONITORING_SYSTEMS/
    │   ├── MONITORING_SETUP.md
    │   ├── ALERTING_RULES.md
    │   └── DASHBOARD_CONFIGS.md
    └── SECURITY/
        ├── SECURITY_ARCHITECTURE.md
        ├── API_SECURITY.md
        └── DATA_PROTECTION.md
```

---

## 📍 MAPA DE MIGRAÇÃO: FICHEIROS RAIZ → NOVAS LOCALIZAÇÕES

### **ANTES (Raiz Caótica)**
```
Full project/
├── COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md
├── COMPREHENSIVE_MISSING_PARTS_AUDIT.md
├── MASTER_INDEX_DASHBOARD_FEB9.md
├── MISSING_ITEMS_COMPREHENSIVE_FEB9.md
├── MISSING_PARTS_ACTION_CHECKLIST.md
├── ORGANIZATION_CORRECTIONS_FEB9.md
├── PHASE1_COMPLETION_REPORT.md
├── PHASE1_EXECUTIVE_SUMMARY.md
├── PORTUGUESE_TRANSLATION_COMPLETION_REPORT.md
├── PROJECT_COMPLETENESS_DASHBOARD.md
├── PROJECT_COMPLETION_CHECKLIST.md
├── PROJECT_FOLDER_GUIDE.md
├── README.md
├── Coding parts/ (nome estranho)
├── docs/ (misturado)
├── writing/ (obsoleto)
└── [14 ficheiros soltos na raiz]
```

### **DEPOIS (Organizado)**

| Ficheiro Original | Nova Localização | Razão |
|-------------------|------------------|-------|
| **README.md** | `ROOT_DOCS/README.md` | Entry point principal |
| **PROJECT_FOLDER_GUIDE.md** | `ROOT_DOCS/PROJECT_FOLDER_GUIDE.md` | Referência estrutura |
| **MASTER_INDEX_DASHBOARD_FEB9.md** | `ROOT_DOCS/MASTER_INDEX.md` | Índice navegação |
| **PHASE1_COMPLETION_REPORT.md** | `PROJECT_MANAGEMENT/STATUS/PHASE1_REPORT.md` | Status fase |
| **PHASE1_EXECUTIVE_SUMMARY.md** | `PROJECT_MANAGEMENT/STATUS/PHASE1_SUMMARY.md` | Executivo |
| **PROJECT_COMPLETENESS_DASHBOARD.md** | `PROJECT_MANAGEMENT/STATUS/COMPLETUDE_DASHBOARD.md` | Métrica |
| **PROJECT_COMPLETION_CHECKLIST.md** | `PROJECT_MANAGEMENT/CHECKLISTS/CHECKLIST_PROJECT.md` | Checklist |
| **MISSING_PARTS_ACTION_CHECKLIST.md** | `PROJECT_MANAGEMENT/CHECKLISTS/CHECKLIST_ACTION.md` | Ação |
| **MISSING_ITEMS_COMPREHENSIVE_FEB9.md** | `PROJECT_MANAGEMENT/AUDITS/MISSING_ITEMS.md` | Auditoria |
| **ORGANIZATION_CORRECTIONS_FEB9.md** | `PROJECT_MANAGEMENT/AUDITS/CORRECTIONS.md` | Erros |
| **COMPREHENSIVE_MISSING_PARTS_AUDIT.md** | `PROJECT_MANAGEMENT/AUDITS/MISSING_AUDIT.md` | Auditoria |
| **COMPREHENSIVE_IMPROVEMENT_AUDIT_FEB9.md** | `ARCHIVE/DEPRECATED_ANALYSIS/` | Versão antiga |
| **Coding parts/** | `CODE/` | Renomear |
| **docs/** | `DOCUMENTATION/` | Consolidar |
| **writing/** | `ARCHIVE/OLD_VERSIONS/` | Backup |
| **support/** | `SUPPORT/` | Manter |
| **SUBMISSION_READY/** | `MANUSCRIPT/` | Consolidar |
| **manuscript/** | `MANUSCRIPT/` | Master |

---

## 🗂️ ESTRUTURA DETALHADA POR PASTA

### **ROOT_DOCS/ — Documentos de Navegação Principal**

**Propósito:** Documentos de entry-point para o projeto  
**Audiência:** Todos (novo no projeto)  
**Tempo Leitura:** 5-30 minutos

| Ficheiro | Linhas | Propósito |
|----------|--------|----------|
| README.md | 445 | Visão geral projeto |
| LEIA-ME.md | 220 | Português versão |
| MASTER_INDEX.md | 230 | Índice navegação |
| QUICK_START.md | 100 | 5-min guia |
| FOLDER_GUIDE.md | 550 | Estrutura detalhada |

### **PROJECT_MANAGEMENT/ — Gestão & Trackeamento**

**Propósito:** Checkpoints, status, auditorias, timelines  
**Audiência:** Gestores, equipa liderança  
**Função:** Rastreamento diário + decisões criticas

**Subpastas:**
- **CHECKLISTS/** — 145 items (fases 1-4), ações críticas, sign-offs
- **STATUS/** — Dashboard completude, relatórios fase, sumários executivos
- **AUDITS/** — Erros encontrados, lacunas, recomendações
- **GANTT/** — Timelines, dependências críticas, milestones

### **GOVERNANCE_COMPLIANCE/ — Conformidade & Risco**

**Propósito:** Aprovações, risco, legal, compliance  
**Audiência:** Governo, stakeholders, auditores  
**Função:** Conformidade regulatória + risco mitigação

**Subpastas:**
- **APPROVALS/** — Cartas MINEA, IRB, consentimento comunitário
- **RISK/** — Registo 15+ riscos, planos contingência, DR
- **LEGAL/** — Contratos MIT-ISPTEC, MOUs comunitários
- **COMPLIANCE/** — ESG, procurement, controles financeiros

### **DOCUMENTATION/ — Guias Técnicos & Operacional**

**Propósito:** How-to guides, procedimentos, protocolos  
**Audiência:** Equipa técnica, operadores, treinadores  
**Função:** Conhecimento operacional dia-a-dia

**Subpastas:**
- **TECHNICAL/** — Código, API, database, integração
- **OPERATIONAL/** — Instalação, operações, manutenção, troubleshooting
- **TRAINING/** — Currículo, materiais, certificações
- **FIELD_OPERATIONS/** — Baseline protocols, equipamento, access permits
- **MONITORING_EVALUATION/** — M&E framework, KPIs, data collection

### **FINANCE_PLANNING/ — Financeiro & Orçamento**

**Propósito:** Orçamentos, ROI, análises custos  
**Audiência:** CFO, financiadores, governo  
**Função:** Decisões financeiras & aprovações

**Subpastas:**
- **BUDGETS/** — Orçamentos linha-item, plano financiamento
- **COST_ANALYSIS/** — LCOE, sensibilidade, ROI
- **REVENUE_MODELS/** — Tarifas, projeções, subsídios
- **FINANCIAL_MANAGEMENT/** — Procurement, pagamentos, auditoria

---

## 🔄 COMO NAVEGAR ESTRUTURA NOVA

### **Se você é...**

| Perfil | Comece em | Próximo | Então |
|--------|-----------|---------|-------|
| **Novo no Projeto** | `ROOT_DOCS/README.md` | `ROOT_DOCS/MASTER_INDEX.md` | Escolha categoria interesses |
| **Gestor Projeto** | `PROJECT_MANAGEMENT/STATUS/` | `PROJECT_MANAGEMENT/CHECKLISTS/` | `PROJECT_MANAGEMENT/AUDITS/` |
| **Desenvolvedor** | `CODE/geesp-angola/README.md` | `DOCUMENTATION/TECHNICAL/` | `CODE/` (scripts, tests) |
| **Stakeholder/Gov** | `PROJECT_MANAGEMENT/STATUS/` | `GOVERNANCE_COMPLIANCE/APPROVALS/` | Relevante por papel |
| **Pesq Operacional** | `DOCUMENTATION/FIELD_OPERATIONS/` | `DOCUMENTATION/MONITORING_EVALUATION/` | Dados relevantes |
| **Financiador** | `PROJECT_MANAGEMENT/STATUS/` | `FINANCE_PLANNING/BUDGETS/` | `GOVERNANCE_COMPLIANCE/RISK/` |

---

## ✅ IMPLEMENTAÇÃO CHECKLIST

### **Fase 1: Estrutura Criada** ✅
- [x] ROOT_DOCS/ criado
- [x] PROJECT_MANAGEMENT/ criado
- [x] GOVERNANCE_COMPLIANCE/ criado
- [ ] DOCUMENTATION/ (quando consolidar)
- [ ] FINANCE_PLANNING/ (quando conteúdo completado)
- [ ] COMMUNICATIONS/ (quando conteúdo completado)
- [ ] INFRASTRUCTURE/ (quando pronto)

### **Fase 2: Documentação Criada** ✅
- [x] Índices & navigation documentos criados
- [x] 12 documentos traduzidos português
- [x] Manifesto de entrega criado
- [ ] Mover ficheiros raiz → novas pastas (manual in git)
- [ ] Arquivar versões antigas
- [ ] Criar redirecionadores se necessário

### **Fase 3: Otimização**
- [ ] Review estrutura com stakeholders
- [ ] Ajustar based on feedback
- [ ] Template criados para novos docs
- [ ] CI/CD pipelines atualizar referências
- [ ] Website & GitHub updated with new structure

---

## 🎯 BENEFÍCIOS ESTRUTURA NOVA

| Aspecto | Antes | Depois |
|--------|-------|--------|
| **Clareza** | 14 ficheiros raiz misturado | Categorizado em 8 pastas lógicas |
| **Busca** | Difícil encontrar | Navegar intuitivamente |
| **Manutenção** | Caótica | Sistematizada |
| **Onboarding** | 1 hora + confusão | 5 min + claro |
| **Escalabilidade** | Impossível | Fácil adicionar |
| **Conformidade** | Pouco rastreável | Auditável |

---

## 📞 QUESTÕES COMUNS

**P: Posso ainda acessar ficheiros antigos?**  
R: Sim — `ARCHIVE/OLD_VERSIONS/` contém tudo. Redireções em ficheiros raiz se necessário.

**P: Como a documentação é versionada?**  
R: Cada subpasta tem seu README + VERSION.txt. Git rastreia histórico completo.

**P: Preciso atualizar bookmarks/links?**  
R: Provavelmente sim. Veja seção "MAPA DE MIGRAÇÃO" acima para novos caminhos.

**P: O código é movido também?**  
R: Não — `CODE/geesp-angola/` mantém estrutura atual por compatibilidade.

---

## 📊 ESTATÍSTICAS ORGANIZAÇÃO

| Métrica | Valor |
|---------|-------|
| Pastas Principais | 9 |
| Subpastas | 25+ |
| Documentos Raiz | 14 → 5 (organizado) |
| Ficheiros Arquivados | 5+ (obsoleto) |
| Novo Espaço "Vazio" | 3 pastas (em prep) |
| Documentos Traduzidos | 12 (português) |
| Linhas Documentação | ~4,500 (PT) + ~20,000 (EN) |

---

**Documento:** REORGANIZATION_STRUCTURE_MAP_FEB9.md  
**Status:** ✅ COMPLETO & IMPLEMENTADO  
**Data:** 9 fevereiro 2026  
**Próxima Revisão:** 15 fevereiro 2026

---

*Estrutura criada para escalabilidade, manutenibilidade & clareza.*  
*Comece em ROOT_DOCS/ → MASTER_INDEX.md para navegação.*
