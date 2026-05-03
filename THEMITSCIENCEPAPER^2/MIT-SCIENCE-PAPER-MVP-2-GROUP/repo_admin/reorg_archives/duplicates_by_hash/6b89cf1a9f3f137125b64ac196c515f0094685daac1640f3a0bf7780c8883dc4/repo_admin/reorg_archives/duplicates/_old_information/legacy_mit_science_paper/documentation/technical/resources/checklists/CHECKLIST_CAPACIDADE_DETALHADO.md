# CAPACIDADE DO GEESP-ANGOLA: CHECKLIST DETALHADO

## ✅ FASE 1: AQUISIÇÃO E PROCESSAMENTO DE DADOS

### Camada 1: Necessidade (Demanda)

| Requisito Metodológico | Implementado? | Verificação | Localização Código |
|---|---|---|---|
| VIIRS Nighttime Lights para mapear ausência de rede | ✅ | `extract_nighttime_lights()` coleta `NOAA/VIIRS/DNB/MONTHLY_V1/VCMCOG` | `gee_extraction.py:115-137` |
| Dados de população (INE/Censo) | ✅ | 45 comunidades com `population_est` de 200-15,000 hab | `communities_45.csv` |
| Priorização por população x luz noturna | ✅ | Dashboard mostra comunidades coloridas (3 zonas prioritárias) | `dashboard/app.py:478-510` |
| **Subtotal Camada 1** | **✅ 100%** | - | - |

---

### Camada 2: Potencial Físico Solar

| Requisito | Implementado? | Status | Código |
|---|---|---|---|
| NASA POWER (irradiância solar) | ✅ | Extrai `ALLSKY_KT`, `ALLSKY_SFC_SW_DWN` | `gee_extraction.py:45-72` |
| SRTM 30m (elevação, declividade) | ✅ | Calcula `slope` e `aspect` via `ee.Terrain` | `gee_extraction.py:138-160` |
| Sentinel-2 (uso solo, NDVI, EVI) | ✅ | NDVI = `(B8-B4)/(B8+B4)` normalizado | `gee_extraction.py:76-110` |
| ESA WorldCover (classificação de landcover) | ✅ | Coleta `ESA/WorldCover/v200` com 11 classes | `gee_extraction.py:170-190` |
| Exportação para GeoTIFF | ✅ | Método `export_to_geotiff()` com gdrive integração | `gee_extraction.py:200-230` |
| **Subtotal Camada 2** | **✅ 100%** | - | - |

---

### Camada 3: Viabilidade Socioeconómica ⚠️ PARCIAL

#### O que EXISTE:

| Requisito | Status | Evidência |
|---|---|---|
| Proximidade à rede elétrica | ✅ | `mapa_distanciarede.npy` no dataset processado |
| NDVI como proxy de potencial agrícola | ✅ | `mapa_ndvi.npy` armazenado + usado em MCDA |
| Pontos de interesse (escolas, saúde) | ❌ | Não coletados do GEE |

#### O que FALTA:

| Requisito Metodológico | Implementado? | O que falta? | Esforço para adicionar |
|---|---|---|---|
| **Índice de Vulnerabilidade** (pobreza + acesso água + saúde) | ❌ | Classe `VulnerabilityCalculator` | 2-3 dias |
| Dados de pobreza (proxy: baixa VIIRS) | ⚠️ | Lógica existe (1 - viirs_lights) mas não isolada | 1 dia |
| Acesso a água potável | ❌ | Requer shapefile de rios/borehole. Não coletado | 3 dias (coleta) + 1 dia (processamento) |
| Distância a serviços de saúde | ❌ | Requer POI shapefile. Não coletado | 2 dias (dados) + 1 dia (GEE) |
| **Potencial Agrícola Explícito** | ⚠️ | NDVI existe, mas não há método `agricultural_suitability()` | 2 dias |
| Proximidade a infraestruturas críticas | ❌ | `extract_critical_infrastructure()` não existe | 3 dias |
| **Subtotal Camada 3** | **⚠️ 50%** | - | **~2 semanas** |

---

## ✅ FASE 2: MODELO MULTICRITÉRIO (AHP)

### Componente 2a: AHP (Analytic Hierarchy Process)

| Funcionalidade | Implementado? | Detalhes | Código |
|---|---|---|---|
| Matriz de comparação pareada | ✅ | Cria matriz NxN com relações Saaty | `mcda_analysis.py:35-60` |
| Escala de Saaty (1, 3, 5, 7, 9) | ✅ | Implementada completa com reciprocais | `mcda_analysis.py:20-28` |
| Método do autovetor | ✅ | Normaliza colunas, média das linhas | `mcda_analysis.py:75-88` |
| Cálculo de Consistency Ratio (CR) | ✅ | CR = CI/RI com validação CR<0.1 | `mcda_analysis.py:93-118` |
| **Subtotal AHP** | **✅ 100%** | - | - |

---

### Componente 2b: Weighted Overlay e Análise Sensibilidade

| Funcionalidade | Implementado? | Detalhes | 
|---|---|---|
| Normalização Min-Max | ✅ | Escala [0,1] com tratamento de NaN |
| Soma ponderada de critérios | ✅ | `Σ(weight_i × raster_i)` |
| Classificação em 3 classes | ✅ | Alta (>0.70), Média (0.40-0.70), Baixa (<0.40) |
| Análise sensibilidade ±20% | ✅ | Varia pesos + recalcula overlay |
| **Subtotal Weighted Overlay** | **✅ 100%** | - |

---

### Componente 2c: Customização por Perfil ⚠️ NÃO IMPLEMENTADO

| Requisito Metodológico | Implementado? | Gap |
|---|---|---|
| **Perfil "Agro-Comunitário"** | ❌ | Não há classe `CommunityProfile` |
| — Pesos: Solar 25%, NDVI 30%, Rio 20%, Vulnerab. 25% | ❌ | Usar pesos genéricos (25,25,20,15,15) |
| — Filtro: NDVI > 0.4, Proximidade Rio < 5km | ❌ | Não há lógica de filtro por perfil |
| **Perfil "Vila Social"** | ❌ | Não há implementação |
| — Pesos: Demanda 30%, Infraestrutura 30%, Solar 25%, Terreno 15% | ❌ | Mesmos 5 critérios genéricos |
| — Filtro: População > 500, Escolas + Saúde > 2 | ❌ | Sem lógica de restrições |
| **Ranking dinâmico por prioridade** | ⚠️ | Ordena por aptidão, não por vulnerabilidade+viabilidade |
| **Subtotal Customização** | **⚠️ 10%** | **Esforço: 1 semana** |

---

## ⚠️ FASE 3: OUTPUT E RECOMENDAÇÕES

### Componente 3a: Dashboard Interativo

| Página/Funcionalidade | Implementado? | Detalhes |
|---|---|---|
| 🏠 Início | ✅ | Informações do projeto, autores, links |
| 📊 Exploração de Dados | ✅ | Carrega GeoTIFF, mostra distribuição |
| 🎯 Análise MCDA | ✅ | Sliders para pesos, cria overlay, sensibilidade |
| 📈 Resultados | ✅ | Mostra 3 zonas prioritárias com gráficos |
| 💰 Calculadora LCOE | ✅ | Entrada de parâmetros, compara 3 tecnologias |
| 🗺️ Mapa Folio | ✅ | Localiza 45 comunidades, marca 3 prioridades |
| **Mapa de Aptidão Sobreposto** | ⚠️ | Pode ser adicionado (raster layer de aptidão) |
| **Subtotal Dashboard** | **✅ 95%** | - |

---

### Componente 3b: Recomendações Tecnológicas

| Recomendação | Implementada? | Detalhes |
|---|---|---|
| **Por Zona** | ✅ | Cacula→PV Fixo, Humpata→Rastreador, Quilengues→Híbrido |
| **LCOE por Tecnologia** | ✅ | 0.18-0.22 USD/kWh (Fixo), 0.22-0.28 (Rastreador), 0.25-0.35 (Híbrido) |
| **Dimensionamento Específico** | ❌ | Não diz "10kW para escola de 200 alunos" |
| **Benefícios Esperados** | ⚠️ | Genéricos ("acesso 24h"), não quantificados ("3 horas estudo noturno extra") |
| **Topologia de Sistema** | ❌ | Não descreve "mini-rede de 50kW com 150 casas" |
| **Estimativa CAPEX/Payback** | ⚠️ | LCOE fornece custo/kWh, não investimento total em USD |
| **Subtotal Recomendações** | **⚠️ 50%** | **Esforço: 1 semana** |

---

### Componente 3c: Modelo de Benefícios Esperados ❌ NÃO IMPLEMENTADO

| Benefício Esperado | Implementado? | Como medir |
|---|---|---|
| **Agro-Comunitário** | - | - |
| — "300% aumento produção horta" | ❌ | Irrigação contínua vs. sazonal |
| — "Receita +USD 150-500/família/ano" | ❌ | Preço local vegetal × produção extra |
| — "N postos de trabalho" | ❌ | Bombeamento + venda agrícola |
| **Vila Social** | - | - |
| — "Horas estudo noturno +3-4h/dia" | ❌ | Survey com estudantes pré/pós |
| — "Perda de vacinas <2%" | ❌ | Refrigeração 24/7 vs. falhas atuais |
| — "Melhoria notas +5-10%" | ❌ | Histórico acadêmico pré/pós |
| **Subtotal Benefícios Quantificados** | **❌ 0%** | **Esforço: 2-3 dias** |

---

## ⚠️ FASE 4: RESULTADOS E VALIDAÇÃO EM CAMPO

### Componente 4a: Simulação e Mapeamento (Já Implementado)

| Elemento | Status | Evidência |
|---|---|---|
| 3 Zonas identificadas (Cacula-Humpata, Quilengues, Nhamatanda-Sul) | ✅ | Apresentadas no dashboard |
| 45 comunidades listadas | ✅ | CSV com coordenadas, população, zona |
| Mapa temático de aptidão | ✅ | Dashboard mostra mapa folium com markers |
| Ranking por prioridade | ⚠️ | Ordena por aptidão, não por vulnerabilidade |

---

### Componente 4b: Plano de Validação em Campo ⚠️ PARCIAL

#### O que EXISTE:

| Componente | Status | Detalhes |
|---|---|---|
| Exemplo de monitoramento pós-impl. | ✅ | 5 projetos pilotos em `monitoring/monitoring_app.py` |
| Geração diária (kWh) | ✅ | Rastreado por projeto |
| Saúde do sistema (%) | ✅ | Métrica '95% saúde' para Cacula |
| Status de manutenção | ✅ | Agenda com priorização |
| ROI em operação | ✅ | "+12% retorno" para Cacula |

---

#### O que FALTA:

| Elemento | Implementado? | O que falta | Esforço |
|---|---|---|---|
| **Protocolo Técnico de Campo** | ❌ | Piranômetro, logger de inversor, testes de eficiência | 3 dias |
| **Métricas Socioeconômicas Pré** | ❌ | Baseline: produção/mês, renda/família, horas estudo | 3 dias |
| **Métricas Socioeconômicas Pós** | ❌ | Medições 3-6 meses após: comparar vs. baseline | 5 dias |
| **Formulários de Survey** | ❌ | ODK forms para coleta estruturada em campo | 2 dias |
| **Análise de Impacto** | ❌ | Relatório comparando previsto vs. realizado | 3 dias |
| **Dashboard de Rastreamento Validação** | ❌ | Streamlit page para progresso de validação | 2 dias |
| **Subtotal Validação** | **⚠️ 25%** | - | **~3 semanas** |

---

## 📊 RESUMO EXECUTIVO

```
┌─────────────────────────────────────────────────────────────┐
│         CAPACIDADE DO GEESP-ANGOLA POR FASE                 │
├─────────────────────────────────────────────────────────────┤
│ FASE 1: Extração Dados              ██████████ 95%  ✅      │
│ FASE 2: MCDA/AHP                    ████████░░ 85%  ⚠️      │
│ FASE 3: Recomendações               ████░░░░░░ 50%  ⚠️      │
│ FASE 4: Validação Campo             ██░░░░░░░░ 25%  ❌      │
├─────────────────────────────────────────────────────────────┤
│ CAPACIDADE GERAL                    ██████░░░░ 64%          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 GAPS CRÍTICOS PARA METODOLOGIA PROPOSTA

### 1️⃣ Perfis de Comunidade (IMPACTO: ALTO)

**Falta**: Pesos e lógica específicos para "Agro-Comunitário" vs. "Vila Social"

**Impacto**: Sem isto, não consegue diferenciar qual tecnologia é melhor para que tipo de comunidade

**Esforço para fixar**: 1 semana

**Prioridade**: 🔴 CRÍTICA para implementação metodológica

---

### 2️⃣ Recomendações Personalizadas por Comunidade (IMPACTO: ALTO)

**Falta**: "Mini-rede de 10kW para escola + 5 sistemas de bombeamento para horta de 2 hectares"

**Impacto**: Sem isto, recomendações são genéricas por zona, não por comunidade específica

**Esforço para fixar**: 1 semana (Classe `RecommendationEngine`)

**Prioridade**: 🔴 CRÍTICA para demonstração ao MIT

---

### 3️⃣ Protocolo de Validação em Campo (IMPACTO: MÉDIO)

**Falta**: Definição de métricas técnicas (irrad. vs. medida) e socioeconômicas (produção, renda, estudo)

**Impacto**: Sem isto, caso piloto não tem framework de análise estruturada

**Esforço para fixar**: 2-3 semanas (protocolo + surveys + análise)

**Prioridade**: 🟠 ALTA para implementação operacional, não crítica para proposta MIT

---

### 4️⃣ Camadas de Dados Socioeconômicas (IMPACTO: MÉDIO)

**Falta**: Índice de Vulnerabilidade, Proximidade a Rios, POIs de Saúde/Escolas

**Impacto**: Camada de "Viabilidade Socioeconómica" fica dependente de dados externos

**Esforço para fixar**: 1-2 semanas (coleta + integração GEE)

**Prioridade**: 🟠 ALTA para operacionalização, pode usar dados de exemplo para proposta

---

## ⏱️ CRONOGRAMA PARA 100% DE CAPACIDADE

```
Semana 1: Perfis de Comunidade + Recomendações Personalizadas
          └─ (Crítico para apresentação MIT)

Semana 2: Camadas de Dados Socioeconômicas
          └─ (Amplia capacidade analítica)

Semana 3: Protocolo de Validação Básico
          └─ (Pronto para caso piloto)

Semana 4: Refinamentos + Documentação
          └─ (Pronto para operação)
```

**Total**: 4 semanas = 1 mês para 100% de capacidade metodológica

---

## 💼 RECOMENDAÇÃO FINAL

> **O projeto GEESP-Angola É totalmente viável para implementar a metodologia proposta. Não há impedimentos técnicos, apenas pequenas extensões código.**

**Para Apresentação ao MIT (Curto Prazo):**
- Focar em Perfis + Recomendações Personalizadas (Semana 1)
- Demonstrar diferenciação entre Agro vs. Vila Social
- Mostrar recomendações específicas para Cacula, Humpata, Quilengues

**Para Implementação Operacional (Médio Prazo):**
- Integrar camadas socioeconômicas (Semana 2)
- Estabelecer protocolo de validação (Semana 3)
- Executar caso piloto com coleta de dados 6 meses

**Resultado**: Framework GEESP-Angola 100% operacional e validado

---

**Documento preparado**: Auditoria Completa de Capacidade  
**Data**: 8 de Fevereiro, 2026  
**Status**: RECOMENDAÇÃO POSITIVA PARA DESENVOLVIMENTO
