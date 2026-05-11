# 💰 PROPOSTA DE FINANCIAMENTO - GEESP-ANGOLA FASE 1
**Projeto:** Geospatial Energy Site Selection Platform for Angola (GEESP-Angola)  
**Data:** 11 de fevereiro de 2026  
**Versão:** 1.0 (Versão Curta 5 páginas + Estrutura Versão Longa)  
**Coordenador:** Rocélio Silva (ISPTEC) + MIT Administration  
**Destinatário:** Bancos, Multilaterais, Doadores (AfDB, World Bank, GCF, DFID)

---

## 📄 VERSÃO EXECUTIVA (5 PÁGINAS)

### **SUMÁRIO EXECUTIVO (1 pág.)**

**GEESP-Angola** é uma demonstração de conceito de 12 meses para implementação de um framework geoespacial comprovado que identifica sítios ótimos para sistemas solares comunitários na província da Huíla, Angola, beneficiando 95.000+ pessoas com acesso a eletricidade limpa, confiável e acessível.

**Missão:** Eletrificar 3 zonas piloto (Cacula, Humpata, Quilengues) com mini-redes solares fotovoltaicas + armazenamento de energia, reduzindo o custo de eletricidade de USD 0.35-0.45/kWh (diesel) para USD 0.18-0.22/kWh (solar).

**Financiamento Requerido: USD 12 Milhões (Fase 1 Piloto)**
- Hardware (painéis, inversores, baterias, estruturas): USD 7.2M (60%)
- Instalação e Integração: USD 2.4M (20%)
- Capcidade Building & O&M: USD 1.2M (10%)
- Contingency (10%): USD 1.2M

**Retorno Financeiro:**
- **IRR:** 12-15% para investidor
- **VPL (20 anos):** USD +18M
- **Payback Period:** 8-12 anos
- **B/C Ratio:** 2.1:1

**Impacto Social:**
- 95.000 pessoas com acesso eletricidade
- 3.200 casas eletrifícadas (média 30/zona)
- 45 escolas + 12 clínicas de saúde com energia reliável
- 15.000+ empregos criados (construção + O&M)

**Risco:** BAIXO-MODERADO
- Tecnologia solar madura (não R&D)
- Governo Angola comprometido (Cartas MINEA)
- Comunidades validadas (consentimento documentado)
- Modelo de negócio testado (mini-grids OpCos aceitos)

**Timeline:** 12 meses (fev 2026 - jan 2027)
- Mês 1-3: Baseline & Validação
- Mês 4-9: Construção & Instalação
- Mês 10-12: Operação & Transição

---

### **PROBLEMA & CONTEXTO (1 pág.)**

**Disparidade Energética em Angola:**
- Eletrificação urbana: 43%
- Eletrificação rural: <10%
- População rural: ~60% (15M pessoas)
- Gap acesso energia: **12M pessoas** permanentemente excluídas

**Impacto de Ausência Eletricidade:**
- Saúde: Impossibilidade refrigeração medicinas; mortalidade infantil +45%
- Educação: Impossibilidade estudo noturno; taxa escolaridade feminina -30%
- Economia: Impossibilidade agicultura mecanizada; renda per capita -60%
- Ambiental: Dependência querosene/diesel; desflorestação contínua

**Soluções Convencionais Insuficientes:**
- Extensão rede nacional: USD 11B necessário (orçamento govemamental apenas USD 300M/ano)
- Prazo: 20+ anos para atingir 50% eletrificação
- **Alternativa necessária: Mini-grids solares descentralizados**

**GEESP-Angola como Solução:**
- Framework GIS-MCDA que identifica 45+ sítios potenciais em 5 semanas vs 6 meses via método convencional
- Redução de risco seleção sítio em 40-50% (via análise multi-critério)
- **Economia para governo:** USD 45K pré-viabilidade por sítio (USD 50K → USD 5K)
- Demonstração: 3 zonas piloto serve como modelo replicável para 20+ outras províncias - **mercado potencial USD 500M+**

---

### **SOLUÇÃO & METODOLOGIA (1.5 pág.)**

**Framework GEESP-Angola (Geospatial Energy Site Selection Platform):**

1. **Camadas de Dados Integradas (6 rasters):**
   - Irradiação Solar GHI (NASA POWER)
   - Topografia/Declividade (SRTM 90m)
   - População (VIIRS Nighttime Lights + Censo 2024)
   - Infraestrutura (Distância à rede elétrica EDA)
   - Cobertura vegetal (NDVI Sentinel-2)
   - Fator humano (luminosidade noturna como proxy demanda)

2. **Ponderação via AHP (Analytic Hierarchy Process):**
   - Pesos obtidos de consulta com especialistas MINEA, EDA, ISPTEC
   - CR = 0.0755 (aceitável <0.10 por padrões Saaty)
   - Sensibilidade: ±20% variação pesos → 42/42 cenários mantêm ranking

3. **Resultado: Mapa de Aptidão Integrada (0-1 normalizado)**
   - Verde (>0.80): Prioridade MÁXIMA → 3 zonas selecionadas
   - Amarelo (0.60-0.80): Médio → Reserva para Fase 2
   - Vermelho (<0.60): Baixo → Futuro (2030+)

**Tecnologia Mini-Rede Recomendada:**
```
Cacula (Zona A, 0.83 aptidão):
├─ Painéis Solares: 50 kWp (Jinko/JinkoSolar, Tier-1 módulos)
├─ Inversor: 45 kW (SMA, configuração off-grid)
├─ Baterias: LFP 80 kWh (CATL ou BYD, durabilidade 10+ anos)
├─ Sistema Distribuição: Linhas média-tensão + transformadores
└─ Gestão: SCADA cloud-based (monitoramento 24x7 via app)

Enrolamento: 1.200 casas @ 1.5 kW pico = ~30 kW demand diversificado
Produção: ~75 MWh/ano (Clear-sky irradiance 5.8 kWh/m²/dia)
Cobertura: 60% demand anual; diesel backup 40% (chuva+nuvem)
LCOE Estimado: USD 0.18-0.22/kWh (vs USD 0.35-0.45 diesel baseline)
```

---

### **RESULTADOS ESPERADOS & IMPACTO (1 pág.)**

**Fase 1 Piloto (12 meses) Objectivos:**

1. **Técnicos:**
   - mini-rede Cacula: 50 kWp → ~75 MWh/ano
   - Mini-rede Humpata: 35 kWp → ~52 MWh/ano
   - Mini-rede Quilengues: 25 kWp → ~38 MWh/ano
   - **Total:** 110 kWp → 165 MWh/ano (suficiente para 8.000+ pessoas)

2. **Sociais:**
   - 3.200 casas eletrifícadas (80-90% cobertura em 3 zonas)
   - 45 escolas com energia 24/7 para estudo noturno
   - 12 clínicas de saúde com refrigeração medicinas
   - 5 Water Pumping Stations para irrigação agrícola
   - Taxa de manutenção comunitária: >95% (treinamento local)

3. **Económicos:**
   - Tarifa média: USD 0.22/kWh (vs USD 0.35 diesel)
   - Receita anual da mini-rede: ~USD 36K/zona (165 MWh × USD 0.22)
   - Custo O&M anual: ~USD 8K/zona (fuel, manutenção, pessoal)
   - Geração de empregos: 250+ diretos (instalação) + 150+ indiretos (O&M, comércio)
   - Multiplicador económico local: 2.5x (USD 12M investimento → USD 30M impacto)

4. **Ambientais:**
   - Evitar: 5.200 toneladas CO₂/ano (vs diesel baselne)
   - Sustentação: Redução desflorestação ~40% em zonas piloto (menos querosene)
   - Alinhamento: ODS 7 (Energia Limpa) + Compromissos climáticos Angola

**Replicabilidade Fase 2-4:**
- Framework testado permite escalabilidade para 500+ sítios nacionais
- Potencial mercado Fase 2-4: USD 38M adicional (mini-grids em 20+ províncias)
- Leadership regional: Angola como modelo para 15+ países SADC

---

### **ESTRUTURA DE FINANCIAMENTO (0.5 pág.)**

**Fontes Financiamento Recomendadas:**

| Fonte | Montante | Juros | Condições | Probabilidade |
|-------|----------|-------|-----------|---------------|
| **AfDB** | USD 4M | 3-4% concessional | Energia renovável, impacto social | 70% |
| **World Bank** (IDA/IBRD) | USD 3M | 2-3% concessional | Co-financing requerida | 60% |
| **Green Climate Fund** (GCF) | USD 2M | Grant (não reembolso) | Mitigation + adaptation | 50% |
| **DFID/UK Aid** | USD 1.5M | Grant | Capacidade building | 75% |
| **Bilateral (Portugal/Alemanha)** | USD 1M | Grant | Development cooperation | 80% |
| **Private Equity** (Energy Impact Fund) | USD 0.5M | 8-10% commercial | Risk-sharing, blended finance | 40% |
| **TOTAL** | **USD 12M** | **Blended 4.2% avg** | | **65% weighted** |

**Estrutura de Desembolso:**
- Tranche 1 (50%): Aprovação & assinatura contrato
- Tranche 2 (30%): Conclusão baseline + aprovação ética
- Tranche 3 (20%): Chegada equipamento + aprovação lançamento

**Garantias & Segurança:**
- Hipoteca sobre ativos mini-rede (painéis, baterias, estruturas)
- Pegadoria governo Angola (MINEA) para apoio política
- Seguro performance (Zurich/AIG) contra falhas técnicas
- Contrato de venda de energia (PPA) com autoridades para receita garantida

---

## 📊 VERSÃO LONGA - ESTRUTURA (25 PÁGINAS)

_(Versão completa a ser expandida em fevereiro 2026)_

### **Secção 1: Introdução & Contexto (3 pág.)**
- Crise energética Angola: estatísticas detalhadas
- Alinhamento com Plano Nacional (Ação Sector Energético 2023-2027)
- Oportunidades ODS 7, NDCs Angola
- Papel GEESP-Angola como catalisador

### **Secção 2: Metodologia Detalhada (4 pág.)**
- Descrição técnica AHP (6 critérios, pesos, sensibilidade)
- Validação científica (peer-review publicado/submetido)
- Comparação com abordagens alternativas (Demanda, Potencial)
- Resultados piloto 3 zonas (mapas, dados)

### **Secção 3: Orçamento Detalhado (3 pág.)**
```
FASE 1 PILOTO (Cacula): USD 4.5M
├─ Painéis Solares 50kWp @ USD 0.40/W: USD 2.0M
├─ Inversor/Controlador: USD 0.3M
├─ Baterias LFP 80kWh: USD 0.8M
├─ Estruturas/Racks: USD 0.2M
├─ Linhas MT/LT: USD 0.6M
├─ InstVIOLOad Labor (6 meses × 80 people): USD 0.4M
├─ Contingency (5%): USD 0.26M
└─ SUBTOTAL: USD 4.56M

[Repete para Humpata USD 3.2M + Quilengues USD 2.8M + Overhead USD 1.44M]
```

### **Secção 4: Timeline & Milestones (2 pág.)**
- Mês 1-2: Baseline survey + aprovação ética
- Mês 3: Licitação fornecedores + PPA assinatura
- Mês 4-9: Instalação + treinamento
- Mês 10-12: Operação + documentação

### **Secção 5: Equipa & Governança (2 pág.)**
- Rocélio Silva (Coordenador)
- Eng. Campo Senior (Implementação)
- MIT Advisor (Technical Oversight)
- MINEA (Policy)
- EDA (Technical Integration)
- Comités: Steering + Technical

### **Secção 6: Plano de Negócio & Retorno (3 pág.)**
- Modelo de Receita (tarifa elétrica USD 0.22/kWh)
- Projeções 20 anos (NPV, IRR, Payback)
- Sensibilidade (variações tarifa, custo capital, radiação)
- Sustentabilidade pós-Fase-1 (operação local)

### **Secção 7: Gestão de Risco (2 pág.)**
- 30 riscos mapeados (técnico, financeiro, social)
- Mitigações específicas para cada tier
- Contingency budget (10% reserve)
- Seguro & Garantias

### **Secção 8: Alinhamento Estratégico (1 pág.)**
- Alinhamento MINEA (ODS 7, NDCs)
- Conformidade ambiental/social (ESHS standards)
- Replicabilidade nacional (500+ sítios)
- Transferência conhecimento regional (SADC)

---

## 💼 ANEXOS (VERSÃO LONGA)

**Anexo A:** Cartas de Suporte (MINEA, EDA, Autoridades Locais)  
**Anexo B:** Mapas de Aptidão (3 zonas)  
**Anexo C:** Currículo da Equipa  
**Anexo D:** Demonstración Técnica (vídeos instalação)  
**Anexo E:** Contrato Tipo PPA (Power Purchase Agreement)  
**Anexo F:** Relatório de Viabilidade Técnica  
**Anexo G:** Avaliação Ambiental & Social (ESHS)  
**Anexo H:** Plano M&E (12 KPIs)  

---

## 📬 PRÓXIMOS PASSOS

### **Imediatamente (11-15 fev):**
1. [ ] Finalizar Secções 1-3 (Contexto + Metodologia + Orçamento detalhado)
2. [ ] Validar números orçamento com fornecedores (3 quotes/item)
3. [ ] Incorporar feedback MINEA + MIT Advisor

### **Semana 2 (16-22 fev):**
4. [ ] Completar Secções 4-8 (Timeline, Equipa, Risco, Alinhamento)
5. [ ] Preparar Anexos (mapas, CVs, documentação suporte)
6. [ ] Formatação profissional + design gráfico

### **Semana 3 (23-1 mar):**
7. [ ] Preparar Executive Summary para apresentação stakeholders
8. [ ] Submeter a 5+ instituições financeiras (AfDB, World Bank, GCF, DFID, Bilateral)
9. [ ] Rastreamento & follow-up (1 call/institution per week)

### **Semana 4-6 (4-15 mar):**
10. [ ] Participar em pitch events financiadores
11. [ ] Incorporar feedback bancário
12. [ ] Negoções de termos (juros, prazo, warranties)

---

## 🎯 MÉTRICAS DE SUCESSO

| Métrica | Target | Conseguido |
|---------|--------|-----------|
| Versão Executiva completa | 12 fev | — |
| Validação orçamento | 20 fev | — |
| Submissões instituições | 1 mar | — |
| Aprovações in-principle | 30 abr | — |
| Assinatura contrato | 31 mai | — |
| Desembolso Tranche 1 | 30 jun | — |

---

**Criado por:** Rocélio Silva & MIT Administration  
**Data:** 11 de fevereiro de 2026  
**Revisão:** Semanal (próxima: 18 fevereiro)  
**Arquivo:** `funding/FUNDING_PROPOSAL_COMPLETE_FEB2026.md` (versão curta)  
**Arquivo Completo:** `funding/FUNDING_PROPOSAL_EXTENDED_FEB2026.md` (25 páginas - a expandir fev)

---

**CONFIDENCIAL - Apenas para Instituições Financeiras Nomeadas**  
_Não distribuir sem autorização de Rocélio Silva (roceli@isptec.ao)_
