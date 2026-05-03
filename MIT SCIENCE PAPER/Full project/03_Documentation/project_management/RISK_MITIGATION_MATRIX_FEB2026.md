# 🚨 MATRIZ DE RISCO & MITIGAÇÃO - GEESP-ANGOLA
**Projeto:** GEESP-Angola Fase 1 (Piloto)  
**Data Criação:** 11 de fevereiro de 2026  
**Propósito:** Identificação e gestão proativa de riscos  
**Escopo:** Fase 1 (Fev-Jul 2026) + Antecipação Fase 2-3  
**Revisão:** Mensal (próxima: 18 fevereiro)

---

## 📊 SUMÁRIO EXECUTIVO

| Categoria | # Riscos | Críticos | Altos | Médios | Baixos |
|-----------|----------|----------|-------|--------|--------|
| **Técnico** | 8 | 1 | 2 | 3 | 2 |
| **Financeiro** | 6 | 1 | 2 | 2 | 1 |
| **Operacional** | 5 | 1 | 1 | 2 | 1 |
| **Social** | 4 | 0 | 1 | 2 | 1 |
| **Ambiental** | 3 | 0 | 1 | 1 | 1 |
| **Governança** | 4 | 1 | 1 | 1 | 1 |
| | **30** | **4** | **8** | **11** | **7** |

**RISCO GERAL:** 🔴 MODERADO-ALTO  
**Recomendação:** Planos de contingência prioritários para 4 riscos críticos

---

## 🔴 RISCOS CRÍTICOS (4 ITEMS)

### **R1: Atraso na Aprovação do Comitê de Ética (IRB-MIT)**

| Aspecto | Detalhe |
|---------|---------|
| **ID** | R-TECH-001 |
| **Probabilidade** | 40% (Moderada) |
| **Impacto** | 🔴 CRÍTICO (bloqueia trabalho de campo) |
| **Risco geral** | 40% × 100 = **40 (CRÍTICO)** |
| **Propriet

ário** | Rocélio Silva (Lead), MIT IRB (Governança) |
| **Controlo** | Proativa |

**Descrição:**
- IRB pode recusar aprovação por preocupações com protocolo de consentimento
- Atrasos administrativos podem adiar decisão 2-4 semanas
- BLOQUEIO: Não podemos começar trabalho de campo sem aprovação

**Impacto se não Mitigado:**
- Atraso trabalho de campo: 2+ semanas
- Risco perda momentum político (cartas MINEA expiram)
- Risco perda compromisso comunitário (morosidade)
- Impacto Financeiro: USD 15K+ em custos incrementais

**Acções de Mitigação (Proativa):**
1. **Submissão antecipada (14 fev):** 1 semana antes do início do campo esperado
2. **Protocolo de qualidade muito alta:** Revisar com especialista ética MIT ANTES de submeter
3. **Contacto direto com IRB:** Comunicação semanal com staff; pedir "expedited track" (5 dias vs 30)
4. **Documentação completa:** Todas cartas comunitárias + consentimento em português + tradução certificada
5. **Documento de alinhamento:** "How our protocol meets MIT IRB §46 Common Rule requirements"

**Plano Contingência (Reativa):**
- **Cenário A (Aprovação com modific

ações, 10 dias):**
  - Implementar mudanças no protocolo (est. 2-3 dias)
  - Resubmeter + aprovação final (5-7 dias)
  - Risco de atraso total: ~2 semanas
  - **Esforço:** 15 h adicional

- **Cenário B (Rejeição, recomeçar 0):**
  - Refazer protocolo inteiro (40 h)
  - Reconsulta comunitária (3 dias)
  - Resubmissão + aprovação (10 dias)
  - **Esforço:** 60 h total
  - **Impacto:** Atraso 3-4 semanas

**Responsável de Resposta:** Rocélio Silva  
**Escalonamento:** MIT Advisor (se não aprovado dia 27 fev)

---

### **R2: Equipamento Crítico Não Chega a Tempo**

| Aspecto | Detalhe |
|---------|---------|
| **ID** | R-OPS-002 |
| **Probabilidade** | 35% (Moderada-Alta) |
| **Impacto** | 🔴 CRÍTICO (delai baseline 2+ semanas) |
| **Risco geral** | 35% × 95 = **33 (CRÍTICO)** |
| **Proprietário** | Eng. Campo Senior (Procurement) |
| **Controlo** | Proativa + Reativa |

**Descrição:**
- Fornecedor internacional (Europa/Ásia): leadtime 3-4 semanas
- Alfândega angolana: clearance pode levar 1-2 semanas
- Transportes internacionais podem atrasar 1-3 semanas

**Equipamento Crítico:**
1. Piranometer (medidor radiação solar) - USD 6K - 12-16 dias
2. GPS diferencial cm-precision - USD 4K - 14 dias
3. Baterias teste (5 units) - USD 3K - 10 dias
4. Câmeras multiespectrais (backup Sentinel-2) - USD 2K - 8 dias

**Impacto se Não Mitigado:**
- Impossível coletar dados radiação solar (kernel da baseline)
- Risco perda confiança comunitária ("disseram que vêm, não vêm")
- Custo overrun: USD 20K+ em custo de armazenamento + taxa de alfândega

**Acções de Mitigação (Proativa):**
1. **PO imediata (12 fev):** Não esperar aprovação ética; colocar ordem mesmo que tentativa
2. **Express shipping (4 dias):** Pagar premium USD 2K para DHL Express vs standard 10 dias
3. **Duplicação de fornecedores:** Encomendar piranometer para 2 fornecedores (Europa + Ásia)
4. **Pre-clearance alfândega:** Contatar Alfândega Luanda ANTES da chegada; prepare paperwork
5. **Armazém temporário:** Pré-agendar storage container se alfândega delay > 5 dias
6. **Rastreamento GPS:** Pacotes com rastreamento em tempo real; alertas automáticas de atraso

**Plano Contingência (Reativa):**
- **Cenário A (Atraso <5 dias):**
  - Adiar trabalho campo para 22 mai (vs 18 mai)
  - Custo: USD 5K (prorrogação alojamento equipa)
  - Impacto: Aceitável, mantém timeline geral

- **Cenário B (Atraso 1-2 semanas):**
  - Equipamento rental local: Procurar piranometer equivalente em Luanda
  - Contato: INEA (Instituto Energia Angola) tem 2 equipamentos emprestáveis
  - Impacto: Mesmo equipamento, sem risco

- **Cenário C (Perda total na alfândega - muito raro):**
  - Ativar insurance claim
  - Re-encomendar via fornecedor prioritário (DHL)
  - Atraso estimado: 3 semanas
  - Impacto: Risco grave, escalona a MIT Advisor

**Responsável de Resposta:** Eng. Campo Senior  
**Escalonamento:** Rocélio Silva (se atraso >10 dias),  MIT Advisor (se atraso >2 semanas)

---

### **R3: Financiamento Bancário Não Aprovado**

| Aspecto | Detalhe |
|---------|---------|
| **ID** | R-FIN-001 |
| **Probabilidade** | 30% (Moderada) |
| **Impacto** | 🔴 CRÍTICO (bloqueia Fase 2 escalabilidade) |
| **Risco geral** | 30% × 90 = **27 (CRÍTICO)** |
| **Proprietário** | MIT Administration (Finance) |
| **Controlo** | Proativa |

**Descrição:**
- Proposta inicial para USD 50M (Fase 1-4) pode ser recusada por bancos
- Falta de track record em Angola: "first-mover" risk
- Mercados financeiros instáveis: taxa de aprovação 30-40% para energia renovável em África

**Impacto se Não Mitigado:**
- Atraso implementação Fase 2 (escalabilidade 10+ mini-grids)
- Equipa desmobiliza, perda de momentum
- Risco perda compromisso comunitário (espera 6+ meses)
- Custo oportunidade: USD 2M/ano em eletrificação não realizada

**Acções de Mitigação (Proativa):**
1. **Plano de financiamento escalonado:**
   - Fase 1 (USD 12M, 2026): foco em 3 zonas piloto — **BAIXO RISCO**
   - Fase 2+ (USD 38M, 2027+): condicional a Fase 1 SUCCESS — **RISCO mitigado por track record**

2. **Diversificação de fontes:**
   - Bancos: African Development Bank (AfDB), BNI (Banco Nacional Investimento Angola)
   - Multilaterais: World Bank, Green Climate Fund (GCF), DFID
   - Doadores privados: Gates Foundation Energy, Shell Foundation, Breakthrough Energy
   - Governo: MINEA (budget nacional), PPP

3. **Business case sólido:**
   - ROI 12-15% (para bancos)
   - Impacto social 95K pessoas
   - Co-financiamento comunitário 15% (reduz risco de default)
   - Risco rating: BB+ (investment grade para renewable energy)

4. **Demonstration effect:**
   - Successo Fase 1 (12 meses) → leverage para Fase 2
   - Métricas públicas: LCOE real, uptime 24x7, satisfação comunitária

5. **Contacto précoce:**
   - Mar 2026: Apresentações a 5+ instituições financeiras
   - Jun 2026: Decisões de aprovação esperadas
   - Jul 2026: Assinatura de contratos

**Plano Contingência (Reativa):**
- **Cenário A (Aprovação parcial, USD 8M vs 12M):**
  - Reduzir Fase 1 para 2 zonas piloto (Cacula + Humpata)
  - Terceira zona (Quilengues) entra em Fase 1B (6 meses depois)
  - Impacto: Slippage 6 meses, mas viável

- **Cenário B (Rejeição total):**
  - Ativar financiamento alternativo: Phased approach com doadores bilaterais
  - MIT internal funding (grant) para Fase 1 prototipo: USD 2-3M possível via MIT D-Lab
  - Impacto: Atraso 12 meses possível, risco alto

**Responsável de Resposta:** MIT Administration  
**Escalonamento:** Rocélio Silva (se tendência negativa em set 2026), MIT President (se rejeição)

---

### **R4: Rejeição ou Grandes Revisões da Revista Científica**

| Aspecto | Detalhe |
|---------|---------|
| **ID** | R-ACAD-001 |
| **Probabilidade** | 25% (Baixa-Moderada) |
| **Impacto** | 🔴 CRÍTICO (credibilidade do projeto) |
| **Risco geral** | 25% × 80 = **20 (CRÍTICO-ALTO)** |
| **Proprietário** | Rocélio Silva (Lead Author) |
| **Controlo** | Proativa |

**Descrição:**
- Reviewers podem criticar: viés de dados, falta de validação de campo, metodologia MCDA discutida
- Rejeição: "Not novel sufficient," "Marginal contribution," "Needs major revisions"
- Ciclos iterate: mediana 6-12 meses para Accept (vs nosso alvo 2-3 meses rápido)

**Impacto se Não Mitigado:**
- Perda credibilidade académica: "projeto não publicado"
- Dificultará aprovação financeira (bancos querem peer-reviewed)
- Atraso certificação MINEA como framwork válido
- Custo: tempo + energy em revisões

**Acções de Mitigação (Proativa):**
1. **Qualidade editorial máxima ANTES de submeter:**
   - Pre-review informal com 2-3 co-reviewers externos (academia)
   - Verify: novel

ty, rigor, relevância journal
   - Rastreamento de "desk reject" risk (<5% chance bom MS)

2. **Seleção de revista estratégica:**
   - 1ª opção: *Energy Policy* (high impact, aplicada) — 40% acceptance
   - 2ª fallback: *Applied Energy* (peer-reviewed, rápido) — 50% acceptance
   - 3ª fallback: *Environmental Modelling & Software* (metodológico) — 60% acceptance

3. **Cover letter strategy:**
   - Highlight novelty: "First MCDA-GIS framework with community-validated field protocol for Angola"
   - Highlight urgency: "Time-sensitive; government piloting framework now"
   - Highlight impact: "95K+ beneficiaries pending rapid publication"

4. **Reviewer strategy:**
   - Suggest 4+ reviewers (evita adversário)
   - Request fast-track: "Early-stage field data; recommend rapid review for policy relevance"

**Plano Contingência (Reativa):**
- **Cenário A (Rejeição desk review):**
  - Resubmeter próxima journal em 2 semanas (2ª opção)
  - Rápide-se implementa Fase 1 enquanto aguarda (não bloqueia)

- **Cenário B (Major revisions, 6 meses retouro):**
  - Implementar Fase 1 COMOU SEM publicação
  - Publicação torna-se "bonus" em Jun-Jul (depois Fase 1 completa)
  - Menor risco de atraso total; projeto não bloqueado

**Responsável de Resposta:** Rocélio Silva + Co-autores  
**Escalonamento:** MIT Advisor (se rejeição repetida >2x)

---

## 🟠 RISCOS ALTOS (8 ITEMS)

### **R5: Recusa Comunitária de Consentimento ou Resistência Social**
- **Prob:** 25% | **Impact:** Alto 75 | **Score:** 19
- **Mitig 1:** Reuniões comunitárias antecipadas (15 fev) com apresentações culturalmente sensíveis
- **Mitig 2:** Líderes comunitários envolvidos como co-designers (não imposição top-down)
- **Mitig 3:** Benefícios claramente comunicados: luz, água, saúde, educação
- **Contingency:** Zona alternativa se rejeição (Quilengues vs Malanje)

### **R6: Slippage no Cronograma de Trabalho de Campo**
- **Prob:** 40% | **Impact:** Médio 60 | **Score:** 24
- **Mitig 1:** Cronograma buffer: +1 semana pré-construído para cada fase
- **Mitig 2:** Equipa redundante: 2 técnicos sênior (vs 1 único ponto falha)
- **Mitig 3:** Plano wetherr contingency: "rain plan" para medições solares (reposição automática)
- **Contingency:** Estender baseline até julho se necessário (afeta mas não bloqueia)

### **R7: Falha/Mau Funcionamento de Equipamento em Campo**
- **Prob:** 20% | **Impact:** Alto 75 | **Score:** 15
- **Mitig 1:** Pre-testagem rigorosa de todos equipamento (2 semanas antes campo)
- **Mitig 2:** Documentação de calibração: piranometer testado vs reference standard
- **Mitig 3:** Backup equipment: 2ª piranometer + 2ª GPS em standby
- **Mitig 4:** Fieldtech training: falha tipografi protocolo de troubleshooting
- **Contingency:** Empréstimo equipamento de INEA (contingency nacional)

### **R8: Custos de Implementação Excedem Orçamento (Fase 1 USD 12M)**
- **Prob:** 35% | **Impact:** Médio 65 | **Score:** 23
- **Mitig 1:** Estimativas detalhadas com 20% contingency pré-construído
- **Mitig 2:** Procura competitiva (3+ fornecedores) para reduzir custos
- **Mitig 3:** Co-financiamento comunitário (USD 1.8M via community contribution = 15%)
- **Contingency:** Fase comunitária extensão (fase piloto menor)

### **R9: Perda Conhecimento / Key Staff Turnover**
- **Prob:** 15% | **Impact:** Alto 75 | **Score:** 11
- **Mitig 1:** Documentação extensiva: GitHub + Notion wiki para knowledge base
- **Mitig 2:** Redundância de staff: 2ª pessoa treinada em cada papel
- **Mitig 3:** Retenção financial: bonus pós-implementação + permanência contratual
- **Contingency:** Ativar contractor backup (Eng. freelance identificada desde já)

### **R10: Dados de Baseline Qualidade Inferior / Viés Sampling**
- **Prob:** 20% | **Impact:** Médio 70 | **Score:** 14
- **Mitig 1:** Protocolo de QA rigoroso: 10% replicação medições (check duplicate)
- **Mitig 2:** Validação comunitária: apresentar resultados preliminares para feedback
- **Mitig 3:** Métodos triangulation: combinar múltiplas fontes (satellite + ground + surveys)
- **Contingency:** Extensão recolha dados (4 semanas adicional) vs relance

### **R11: Capacidade Técnica Local Insuficiente**
- **Prob:** 25% | **Impact:** Médio 70 | **Score:** 18
- **Mitig 1:** Plano de Capacitação (60h estruturado) antes de trabalho campo
- **Mitig 2:** Mentoring periódico: MIT instructor visita site 2x mês
- **Mitig 3:** Recursos didáticos: manuais em português + vídeos de treino
- **Contingency:** Contractor especialista de São Paulo/Nairobi para suporte intensivo

---

## 🟡 RISCOS MÉDIOS (11 ITEMS)

### **R12-R14: Riscos Técnicos de Dados (Qualidade Satélite, Cobertura, Resolução)**
- **Prob:** cada ~20% | **Combined Score:** 12-14 cada
- **Mitigação:** Uso de múltiplas fontes (Sentinel-2 10m + NASA POWER 1º + VIIRS 750m)
- **Note:** Bem controlada via Weighted Overlay design (cada camada tem redundância)

### **R15-R17: Riscos Operacionais (Logística, Segurança Campo, Comunicações)**
- **Prob:** cada ~20-30% | **Combined Score:** 8-15
- **Mitigação:** Planeamento logístico antecipado, comunicação satélite, vehicle insurance

### **R18-R19: Riscos de Comunicação / Gestão Stakeholder** 
- **Prob:** ~25% | **Score:** 12-14
- **Mitigação:** Atualizações mensais, reuniões stakeholder trimestrais, newsletters

### **R20-R22: Riscos Ambientais (Clima Extremo, Sazonalidade)**
- **Prob:** ~15-20% | **Combined Score:** 8-12
- **Mitigação:** Schedule field work em estação seca (mai-ago); plano contingency chuva

---

## 🟢 RISCOS BAIXOS (7 ITEMS)

### **R23-R30: Riscos Baixos**
- Questões político

a internacional, conflito armado regional (Angola estável)
- Pandemia/saúde pública (COVID back under control, vacinação >70%)
- Rejeição tecnologia comunitária (aceitação solar é alta em Angola)
- **Estratégia:** Monitoramento passivo; sem plano contingency específico

---

## 📊 MATRIZ DE RISCO (Probabilidade vs Impacto)

```
IMPACTO
Alto    │
  90    │  ●R1 ●R3        ●R7        ●R5
  80    │         ●R2              ●R8
  70    │  ●R6              ●R9  ●R10        ●R11
  60    │
  50    │
        └─────────────────────────────────────
          Baixa      Moderada      Alta      Crítica
          PROBABILIDADE
          
Cor: Vermelho (Crit)  | Laranja (Alto) | Amarelo (Med) | Verde (Baixo)
```

**Topright Quadrant (Critical - Immediate Action):** R1, R2, R3, R4
**Upper-middle (High - Monitoring):** R5-R11
**Lower (Medium/Low - Routine):** R12-R30

---

## 🔄 PLANO DE MONITORAMENTO & REVISÃO

| Frequência | Atividade | Responsável | Data Próxima |
|-----------|-----------|-------------|--|
| **Semanal** | Rastreio riscos críticos (R1-R4) | Rocélio | Seg 12 fev |
| **Bi-Semanal** | Atualização GANNT vs matriz risco | Rocélio | Seg 18 fev |
| **Mensal** | Revisão matriz completa + comit

ê | Rocélio + Advisor | 18 fev, 18 mar |
| **Trimestral** | Strategic review + ajustamentos | MIT + ISPTEC | 18 mai |

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [x] Matriz de Risco criada e documentada (11 feb)
- [ ] Reviewed com MIT Advisor (target: 12 fev)
- [ ] Planos de contingência validados com team (target: 15 fev)
- [ ] Escalation triggers comunicados a stakeholders (target: 13 fev)
- [ ] Tool de rastreamento estabelecida (Notion ou Excel) (target: 14 fev)
- [ ] Reunião kick-off risk management (target: 18 fev)

---

**Criado por:** Rocélio Silva, Coordenador GEESP-Angola  
**Revisado por:** Pendente MIT Advisor  
**Data de Criação:** 11 de fevereiro de 2026  
**Próxima Revisão:** 18 de fevereiro de 2026  
**Arquivo:** `project_management/RISK_MITIGATION_MATRIX_FEB2026.md`

---

_"Antecipação é a melhor gestão de risco. Esperamos o pior, planeamos o melhor."_
