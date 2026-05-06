# SCIENTIFIC ARTICLE STANDARDS GUIDE - SOL.TEX REORGANIZATION

**Date**: March 5, 2026  
**Purpose**: Align SOL.tex with international scientific writing standards

---

## STANDARD SCIENTIFIC ARTICLE STRUCTURE (IMRAD + FRONT/BACK)

### ✅ CORRECT SEQUENCE

```
FRONT MATTER:
├── Title (concise, descriptive, <15 words)
├── Authors & Affiliations
├── Date
├── ABSTRACT (150-300 words)
│   ├─ Background/Context (1-2 sentences)
│   ├─ Objective/Purpose (1-2 sentences)  
│   ├─ Methods (2-3 sentences)
│   ├─ Results/Findings (2-3 sentences)
│   └─ Conclusion/Implications (1-2 sentences)
└── Keywords (5-8 words, separated by semicolons)

MAIN CONTENT (IMRAD):
├── 1. INTRODUCTION (8-15% of paper)
│   ├─ Background/Context
│   ├─ Literature Review (what's known)
│   ├─ Gap in Knowledge (what's missing)
│   ├─ Problem Statement
│   ├─ Research Questions
│   └─ Objectives/Hypotheses
│
├── 2. METHODS/METHODOLOGY (10-20% of paper)
│   ├─ Study Design
│   ├─ Theoretical Framework
│   ├─ Data Sources
│   ├─ Analytical Approach
│   ├─ Tools & Techniques
│   ├─ Validation Methods
│   └─ Research Ethics (if applicable)
│
├── 3. RESULTS (15-25% of paper)
│   ├─ Quantitative Findings
│   ├─ Case Study Results
│   ├─ Validation Results
│   ├─ Sensitivity Analysis
│   ├─ Comparative Analysis
│   └─ Key Metrics & Evidence
│
├── 4. DISCUSSION (20-30% of paper)
│   ├─ Interpretation of Results
│   ├─ Comparison with Literature
│   ├─ Implications (theoretical & practical)
│   ├─ Limitations & Caveats
│   ├─ Recommendations
│   └─ Generalizability
│
└── 5. CONCLUSION (3-5% of paper)
    ├─ Summary of Key Findings
    ├─ Contribution to Knowledge
    ├─ Practical Applications
    ├─ Future Research Directions
    └─ Final Statement

BACK MATTER:
├── Acknowledgments
├── Funding Statement (if applicable)
├── Conflict of Interests (if applicable)
├── References
├── Appendices (optional)
└── Supplementary Materials (optional)
```

---

## SOL.TEX CURRENT STRUCTURE ANALYSIS

### Current Sections (Line Order):
1. ✅ Title
2. ✅ Authors & Affiliations
3. ✅ Date (via \today)
4. ✅ Abstract + Keywords
5. ✅ **Introduction** (with 3 subsections)
6. ❌ **GEESP-Angola: Framework section** (Should be in METHODS or INTRODUCTION)
7. ❌ **Types of Technologies section** (Should be in INTRODUCTION/METHODS)
8. ✅ **Methodology** (Correct position)
9. ✅ **Results** (Correct position)
10. ✅ **Discussion** (Correct position)
11. ❌ **Comparative Historical Patterns section** (Should merge into DISCUSSION)
12. ❌ **Logistics, Costs section** (Should merge into DISCUSSION or be separate IMPLEMENTATION PLANNING)

---

## ISSUES IDENTIFIED

### 🔴 Issue #1: Sections Out of Logical Order
**Current**: Introduction → Framework → Technologies → Methods → Results → Discussion  
**Should be**: Introduction → Methods (with Framework) → Results → Discussion  

**Fix**: Move "GEESP-Angola Framework" section into Methods, not as standalone section

---

### 🔴 Issue #2: Theory/Background in Middle of Paper
**Current**: "Types of Technologies" section (with physics, comparisons, international examples)  
**Should be**: This belongs in INTRODUCTION as literature review + theoretical foundation  

**Fix**: Integrate into Introduction → Subsection on "Technology Foundations & International Context"

---

### 🔴 Issue #3: Technology Selection Logic in Methodology
**Current**: Detailed technology recommendations scattered across multiple sections  
**Should be**: Technology selection criteria should be in METHODS (as part of decision framework)

**Fix**: Move "Aprofundamento e Recomendações por Tipo de Tecnologia" into Methods as decision matrix

---

### 🔴 Issue #4: Comparative Analysis Placed After Discussion
**Current**: "Padrões e Práticas Históricas" section placed AFTER Discussion  
**Should be**: Comparative evidence belongs in INTRODUCTION or early DISCUSSION  

**Fix**: Move comparative analysis into DISCUSSION → subsection on "Comparative Validation"

---

### 🔴 Issue #5: Implementation/Logistics Section Dangling
**Current**: "Logística, Custos e Parcerias" at end of paper  
**Should be**: Either in DISCUSSION (implications) → IMPLEMENTATION CONSIDERATIONS, or as dedicated section if too long

**Fix**: Rename to "Implementation & Deployment Framework" and move to Discussion or after Conclusion as "IMPLEMENTATION PLANNING"

---

## REORGANIZATION PLAN FOR SOL.TEX

### ✅ Proposed New Structure:

```
FRONT MATTER:
├── Title ✓ (keep as is)
├── Authors & Affiliations ✓ (keep as is)
├── Date ✓ (keep as is)
├── Abstract ✓ (keep as is - EXCELLENT current abstract)
└── Keywords ✓ (keep as is)

MAIN CONTENT:
├── 1. INTRODUCTION (EXPANDED - include background + theory)
│   ├─ Contexto Global e Desafios em Angola ✓
│   ├─ Lacunas de Pesquisa & Solução Proposta ✓ (currently subsection 3)
│   ├─ Fundamentos Teóricos: MCDA-GIS [FROM current "GEESP-Angola" section]
│   ├─ Revisão Crítica da Literatura [INTEGRATE "Types of Technologies"]
│   │   ├─ Tecnologias Solares: Fundamentos Físicos
│   │   ├─ Experiências Internacionais
│   │   ├─ Trade-offs Tecnológicos
│   │   └─ Lacunas no Contexto Angolano
│   └─ Objetivos e Estrutura do Artigo ✓
│
├── 2. METHODOLOGY (EXPANDED - framework + implementation)
│   ├─ Enquadramento Conceptual e Teórico ✓ (CURRENT METHODOLOGY SUBSECTION 1)
│   ├─ GEESP-Angola Framework Detalhado [FROM current standalone section]
│   │   ├─ Teoria do MCDA-GIS
│   │   ├─ Critérios de Decisão (técnicos, socioeconômicos, ambientais)
│   │   ├─ Weighting Methods (AHP)
│   │   ├─ Validation Protocols [FROM "Protocolos de Validação"]
│   │   └─ Risk Mitigation Strategies [FROM current subsection]
│   ├─ Processo de Implementação: Etapas Detalhadas ✓
│   ├─ Tecnologias Solares Recomendadas [FROM technologies section]
│   │   ├─ Off-Grid Systems
│   │   ├─ Mini-grids Híbridas
│   │   ├─ Rastreadores
│   │   ├─ Bombeamento Solar
│   │   ├─ Aquecimento Solar
│   │   └─ Armazenamento de Energia (Li-ion, Sodium-ion, Térmico)
│   ├─ Critérios Ambientais Críticos
│   │   ├─ Degradação por Pó em Semi-Árido
│   │   ├─ Impacto de Temperatura Extrema
│   │   └─ Resiliência Climática
│   └─ Seleção de Tecnologia: Matriz de Decisão
│
├── 3. RESULTS
│   ├─ Aplicação a Província da Huíla: Três Zonas Prioritárias ✓
│   ├─ Análise de Sensibilidade: Robustez do Ranking ✓
│   ├─ Quantificação Econômica do Business Case (Cacula) ✓
│   ├─ Comparação com Metodologias Alternativas ✓
│   └─ Validação Retrospectiva em 5 Contextos Africanos ✓
│
├── 4. DISCUSSION (WITH COMPARATIVE ANALYSIS INTEGRATED)
│   ├─ Interpretação dos Resultados ✓
│   ├─ Validação com Literatura: Padrões Comparativos
│   │   └─ [INTEGRATE: "Padrões e Práticas Históricas em 87 Mini-Redes Africanas"]
│   ├─ Análise de Trade-offs e Generalização ✓
│   ├─ Comparação com Estudos Anteriores ✓
│   ├─ Implicações Científicas, Políticas e Práticas
│   │   ├─ Implicações Políticas ✓
│   │   ├─ Angola Energy Policy Context ✓
│   │   ├─ Climate Resilience & Adaptation ✓
│   │   ├─ Community Engagement Framework ✓
│   │   └─ Business Model Assessment ✓
│   ├─ Implementação & Financiamento [FROM "Logistics" section]
│   │   ├─ Supply Chain Logistics
│   │   ├─ Life-Cycle Costing
│   │   ├─ Financing Mechanisms
│   │   └─ Partnership Models
│   └─ Limitações ✓
│
├── 5. CONCLUSION
│   ├─ Resumo dos Principais Achados
│   ├─ Contribuição Científica da Pesquisa
│   ├─ Recomendações para Implementação
│   ├─ Perspectivas para Pesquisa Futura
│   └─ Implicação Final para Contexto Angolano
│
└── BACK MATTER:
    ├─ Acknowledgments (if not already present)
    ├─ Funding Statement (if applicable)
    ├─ References ✓
    └─ Appendices (if any)
```

---

## SPECIFIC REORGANIZATION ACTIONS

### ACTION 1: Expand Introduction to Include Theory
**Move these subsections INTO Introduction:**
- Current "Experiências Internacionais em Sistemas Solares Comunitários"
- Current "Tipos de Tecnologias Solares: Fundamentos Teóricos"
  - Fundamentos Físicos da Conversão Fotovoltaica
  - Aprofundamento e Recomendações por Tipo de Tecnologia
  - Estudos Comparativos Internacionais
  - Tables and figures on technology comparisons

**Result**: Introduction becomes comprehensive literature + theory foundation (currently ~4 pages, should be ~6-8 pages for a technical article)

---

### ACTION 2: Consolidate Methods Section
**Keep in Methods:**
- Enquadramento Conceptual (current subsection)
- Processo de Implementação (current subsection)

**Add to Methods:**
- GEESP-Angola Framework section (currently standalone)
- Protocolos de Validação section (currently in Technologies)
- Estratégias de Mitigação (currently scattered)
- Technology Selection Matrix (currently in Technologies)
- Environmental Criteria (soiling, temperature) currently in Technologies

**Result**: Complete, self-contained methodology section

---

### ACTION 3: Reorganize Discussion
**Keep in Discussion:** Current Discussion sections 1-6 (Interpretação... Limitações)

**Integrate INTO Discussion:**
- "Padrões e Práticas Históricas em Projetos Solares Comunitários"
  → Rename to "Section 6.6: Validation Against 87 African Mini-Grid Case Studies"
  → Place immediately after "Comparação com Estudos Anteriores"

**Add after Implicações Políticas:**
- "Logística, Custos e Parcerias"
  → Rename to "Section 6.7: Implementation Framework & Partnership Models"
  → Include supply chain, LCC analysis, financing mechanisms

---

### ACTION 4: Add Conclusion Section
**Currently MISSING:** Dedicated conclusion section

**Create NEW section after Discussion:**
```latex
\section{Conclusão}
\subsection{Síntese dos Achados Principais}
[1-2 paragraphs summarizing key results]

\subsection{Contribuição para o Conhecimento Científico}
[1-2 paragraphs on what this adds to literature]

\subsection{Recomendações para Implementação em Angola}
[Bullet points on policy/practice recommendations]

\subsection{Direções para Pesquisa Futura}
[Priority areas for follow-up research]

\subsection{Declaração Final}
[1 paragraph on overall significance]
```

---

## BENEFITS OF REORGANIZATION

✅ **Logical Flow**: Readers understand context before methods, methods before results  
✅ **IMRAD Compliance**: Meets international journal standards  
✅ **Clarity**: Each section has clear purpose and boundaries  
✅ **Completeness**: No dangling sections or orphaned content  
✅ **Professionalism**: Allows submission to peer-reviewed journals  
✅ **Navigation**: Readers (and reviewers) know where to find information  

---

## SCIENTIFIC WRITING STANDARDS APPLIED

### Standards Source References:

1. **IMRAD Structure** (Standard since 1972)
   - International format for scientific articles
   - Used by 90%+ of peer-reviewed journals

2. **Elsevier Guidelines**
   - Logical section ordering
   - Clear introduction → methods → results → discussion flow
   - Separate conclusions from discussion

3. **APA & MLA Standards**
   - Keywords placement
   - Abstract positioning
   - Reference formatting

4. **Nature & Science Journal Standards**
   - Concise introduction (context + gap + objective)
   - Complete methodology (reproducibility)
   - Results separate from interpretation
   - Discussion for comparative analysis
   - Conclusion for synthesis

---

## NEXT STEPS

1. ✅ **Document Structure Review** (this document)
2. ⏳ **Execute Reorganization** (text rearrangement)
3. ⏳ **Create New Conclusion Section**
4. ⏳ **Update Cross-references** (labels, citations)
5. ⏳ **Verify LaTeX Compilation**
6. ⏳ **Final Review & Polish**

---

**Status**: Ready for implementation  
**Estimated Changes**: 40-50 lines of LaTeX reorganization  
**Time to Complete**: ~30 minutes manual adjustment  

