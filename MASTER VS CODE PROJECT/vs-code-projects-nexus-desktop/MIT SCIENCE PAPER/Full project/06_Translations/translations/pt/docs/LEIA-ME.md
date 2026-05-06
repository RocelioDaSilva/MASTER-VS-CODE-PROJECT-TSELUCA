# ✅ CONCEITO DO PROJETO & VISÃO GERAL
**Data:** Fevereiro 9, 2026  
**Versão:** 2.0  
**Propósito:** Explicação executiva breve de projeto GEESP-Angola  
**Formato:** Markdown estruturado para website + GitHub

---

## 🎯 O QUE É GEESP-ANGOLA?

**GEESP-Angola** = **G**eographic **E**nergy **E**quity **S**olar **P**lanning para Angola

Um framework open-source que combina **GIS (SIG) + Análise Multicritério (AMCM)** para identificar localizações ideais para mini-redes solares em zonas rurais de Angola.

**Objetivo:** Trazer eletricidade limpa e acessível para 1+ milhão de pessoas, criando 500K+ empregos.

---

## ⚡ PROBLEMA QUE RESOLVE

```
ANGOLA HOJE:
├─ 55M+ pessoas (~40% acesso)
├─ Diesel gerador → US$0.45/kWh (caro + poluente)
├─ Cortes rede frequente (3-5 horas/dia)
└─ Pequenas cidades isoladas = 0 eletricidade

GEESP PROPÕE:
├─ Identificar 4 zonas ideais (solar + população + acessibilidade)
├─ Mini-rede solar → US$0.12-0.18/kWh (limpo + barato)
├─ Operações locais = empregos + confiabilidade
└─ Escalável: 1 piloto → 50+ zonas → cobertura nacional
```

---

## 🗺️ COMO FUNCIONA

### **Passo 1: Dados Satélite** (Google Earth Engine)
- Irradiação solar (GHI diária)
- Topografia/slope
- Densidade populacional (VIIRS nightlights)
- Distância infraestrutura existente

### **Passo 2: Análise AMCM** (Ponderação Especialista)
- 8 critérios técnicos + contexto local
- Pesos definidos por stakeholders (governo, comunidades, ONGs)
- Método Saaty (AHP) validado

### **Passo 3: Mapa Aptidão** (Resultado)
- Classificação 0-1 (onde 1 = melhor)
- 4 zonas piloto selecionadas:
  - **Cacula:** 0.83 (excelente)
  - **Humpata:** 0.79 (muito bom)
  - **Quilengues:** 0.76 (bom)
  - **+1 adicional:** [TBD]

### **Passo 4: Implementação** (Fase 2+)
- Trabalho de campo (levantamento baseline)
- Instalação piloto
- Operações & monitoramento
- Aprendizagem & replicação

---

## 📊 EQUIPA & PARCERIAS

| Organização | Papéis | Sede |
|-------------|--------|------|
| **ISPTEC** | Coordenação nacional, implementação campo | Huambo, Angola |
| **MIT** | Metodologia, análise, supervisão técnica | Cambridge, EUA |
| **MINEA** | Alinhamento estratégico, políticas | Luanda, Angola |
| **Autoridades Locais** | Aceitação comunitária, permissões | 4 Zonas |

---

## 💰 FINANCIAMENTO & DURAÇÃO

| Período | Fase | Atividades | Custo |
|---------|------|-----------|-------|
| **Fev-Mar 2026** | 1 | Aprovações, pessoal, baseline survey | USD 12M |
| **Abr-Mai** | 2 | Escalabilidade, 3 zonas adicionais | USD 18M |
| **Jun-Ago** | 3 | Operações iniciais, M&E | USD 15M |
| **Set-Jan 2027** | 4 | Sustentabilidade, replicação | USD 5.5M |

**Total:** USD 50.5M (18 meses)

---

## 🎓 INOVAÇÃO & DIFERENÇA

| Aspecto | Precedentes | GEESP-Angola |
|---------|----------|------------|
| Seleção Sítio | Ad-hoc consultoria | Framework científico reproducível |
| Escala | 1-2 zonas | 4-50+ zonas |
| Comunidade | Consulta 1× | Engajamento contínuo |
| Código | Proprietário | Open-source (GitHub) |
| Impacto | Local | Replicável em SSA |

---

## 📈 RESULTADOS ESPERADOS

**Ano 1 (Piloto):**
- 1,000 famílias acesso eletricidade
- 100 empregos criados
- 15K tons CO2 evitadas

**Ano 3+ (Escalabilidade):**
- 1M+ pessoas com acesso
- 500K empregos
- 5M+ tons CO2 evitadas
- ODS 7 (energia limpa) + ODS 13 (clima) + ODS 1 (pobreza)

---

## 🏗️ ESTRUTURA DO PROJETO

```
Full project/
├── manuscript/              ← Documento científico (2,000 linhas)
├── Coding parts/           ← Framework Python (3,500 linhas)
│   └── geesp-angola/       ← Repositório code principal
│       ├── scripts/        ← GEE, MCDA, LCOE
│       ├── dashboard/      ← App Streamlit (interface web)
│       ├── monitoring/     ← Sistema monitoramento
│       └── tests/          ← 12 testes (100% passando)
├── presentations/          ← 7-slides + one-pager (2,100 linhas)
├── docs/                   ← Documentação técnica
├── support/                ← Templates + FAQ
└── translations/pt/        ← Tudo em português (8,500+ linhas)
```

---

## 💻 TECNOLOGIA

- **Backend:** Python + Google Earth Engine API
- **Frontend:** Streamlit (dashboard web)
- **Database:** PostgreSQL (dados comunitária)
- **Cloud:** AWS/GCP (implementação produção)
- **Análise:** AHP/MCDA (ponderação stakeholder)
- **Open:** GitHub (código público)

---

## 📋 STATUS ATUAL (9 Fevereiro 2026)

| Componente | Status | % Completo |
|-----------|--------|-----------|
| Manuscrito | ✅ | 95% (submissão 12 fev) |
| Código | ✅ | 70% (v2 em progresso) |
| Apresentações | ✅ | 100% (pronto) |
| Documentação | ⚠️ | 45% (operacional faltando) |
| Operações | 🟡 | 25% (em planejamento) |
| Campo | 🔴 | 15% (não iniciado, começa 20 fev) |

**Global: 62% Completo**

---

## 🚀 PRÓXIMOS PASSOS

**Fevereiro (Go-Live Prep):**
- Aprovações governo/ética
- Equipa contratação
- Baseline protocol finalizado

**Março-Abril (Piloto):**
- Baseline surveys 4 zonas
- Análise MCDA completa
- Instalação piloto começa

**Maio-Junho (Avaliação):**
- Operações iniciais
- Impacto 6-meses
- Decisão escalabilidade

---

## 📚 LEITURA ADICIONAL

```
Comece com (5 min):
  → Este README
  → MASTER_INDEX_DASHBOARD.md

Aprofunde (30 min):
  → PROJECT_FOLDER_GUIDE.md
  → Manuscript abstract (SOL.tex)
  → One-page summary

Especialista (2 horas):
  → Manuscrito completo (SOL.tex)
  → Code README (geesp-angola/README.md)
  → Dashboard QUICKSTART.md
```

---

## 🔗 Links

- **GitHub:** github.com/geesp-angola
- **MIT:** globalclassroom.mit.edu
- **ISPTEC:** isptec.ao
- **Financiadores:** World Bank / AfDB / GCF

---

## 👥 Contactos Principais

| Papel | Email | Telefone |
|------|-------|----------|
| Gestor Projeto | roceli@isptec.ao | +244 923 456789 |
| MIT Lead | professor@mit.edu | +1 617 253 XXXX |
| ISPTEC Director | director@isptec.ao | +244 222 123456 |

---

## 📄 Licença

**MIT License** — Código e documentação abertos para uso/modificação  
Atribuição requerida: GEESP-Angola Framework by MIT + ISPTEC

---

**Versão:** 2.0  
**Última Atualização:** 9 fevereiro 2026  
**Próxima:** Integrar feedback stakeholders

---

*Uma framework para energia limpa e equitativa em Angola e além.*
