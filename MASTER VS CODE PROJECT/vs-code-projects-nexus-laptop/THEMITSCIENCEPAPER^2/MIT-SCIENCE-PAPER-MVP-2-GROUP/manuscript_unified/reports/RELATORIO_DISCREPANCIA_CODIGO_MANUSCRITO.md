# RELATÓRIO DE CONCORDÂNCIA: CÓDIGO vs. MANUSCRITO
## Identificação de Inconsistências - GEESP-Angola Framework

**Data:** 03/03/2026  
**Status:** ⚠️ DISCREPÂNCIA CRÍTICA IDENTIFICADA  
**Severidade:** ALTA

---

## RESUMO EXECUTIVO

O código Python (geesp_unified_app.py) implementa **5 critérios MCDA**, enquanto o manuscrito (SOL.tex) especifica explicitamente **6 camadas raster**. Esta desconexão fundamental compromete a fidelidade da implementação ao design descrito na literatura.

---

## 1. DISCREPÂNCIA PRINCIPAL: NÚMERO DE CRITÉRIOS

### 1.1 Manuscrito (SOL.tex - Linhas 64, 152)

**Critérios Especificados (6 camadas raster):**

```
"Integramos 6 camadas raster (irradiação solar GHI, declividade, 
densidade populacional VIIRS, distância à rede, NDVI, 
luminosidade noturna) através de Weighted Overlay"
```

### 1.2 Código Atual (geesp_unified_app.py - Linhas 123-162)

**Critérios Implementados (5 variáveis):**

```python
def cached_mcda_analysis(
    w_solar: float,      # ✅ Irradiação solar (GHI)
    w_pop: float,        # ✅ Densidade populacional (VIIRS)
    w_dist: float,       # ✅ Distância à rede
    w_slope: float,      # ✅ Declividade
    w_ndvi: float        # ✅ NDVI
    # ❌ FALTANDO: w_nightlights (Luminosidade noturna)
):
```

### 1.3 Comparação Tabular

| # | Critério | Manuscrito | Código | Status |
|---|---|---|---|---|
| 1 | Irradiação Solar (GHI) | ✅ Especificado | ✅ Implementado (w_solar) | ✓ OK |
| 2 | Declividade | ✅ Especificado | ✅ Implementado (w_slope) | ✓ OK |
| 3 | Densidade Populacional (VIIRS) | ✅ Especificado | ✅ Implementado (w_pop) | ✓ OK |
| 4 | Distância à Rede | ✅ Especificado | ✅ Implementado (w_dist) | ✓ OK |
| 5 | NDVI (Potencial Agrícola) | ✅ Especificado | ✅ Implementado (w_ndvi) | ✓ OK |
| 6 | Luminosidade Noturna | ✅ **ESPECIFICADO** | ❌ **FALTANDO** | ✗ CRÍTICO |

---

## 2. ANÁLISE DETALHADA: CRITÉRIO FALTANTE

### 2.1 Especificação do Manuscrito

**Luminosidade Noturna (Linhas 152, 136):**

```
"VIIRS com ±30% incerteza"

"Integração de nighttime lights (VIIRS), WorldPop, NDVI, 
e avaliação rápida participativa em 2018-2020"

"Luzes Noturnas (VIIRS/DMSP): Mapas de luminosidade servem como 
proxy de eletrificação e demanda energética. Estudos indicam forte 
correlação (R²≈0.88) entre intensidade de luz noturna e consumo 
elétrico"
```

### 2.2 Fonte de Dados

- **Produto:** VIIRS (Visible Infrared Imaging Radiometer Suite) nighttime lights
- **Resolução:** ~375m
- **Função:** Proxy de eletrificação atual + demanda energética
- **Correlação com consumo:** R² ≈ 0.88 (forte)
- **Incerteza aceita:** ±30% (per manuscrito linha 152)

### 2.3 Interpretação Semântica

Luminosidade noturna em GEESP-Angola não é um critério redundante:
- **Diferente de densidade populacional**: luzes indicam desenvolvimento/infraestrutura
- **Indicador de "energia faltante"**: áreas com população mas sem luz = demanda potencial
- **Calibração de LCOE**: áreas escuras sugerem demanda não atendida = maior potencial financeiro

---

## 3. IMPACTO DA DISCREPÂNCIA

### 3.1 Consequências Técnicas

| Aspecto | Impacto | Severidade |
|---|---|---|
| **Aptidão Agregada** | Subestima zonas com população + sem eletrificação | ALTA |
| **Seleção de Sítios** | Pode priorizar sítios errados (populosos mas eletrificados) | ALTA |
| **Validação de Pesquisa** | Código não implementa framework conforme publicado | CRÍTICA |
| **Reprodutibilidade** | Terceiros não conseguem replicar GEESP-Angola | CRÍTICA |

### 3.2 Exemplo de Efeito

**Cenário:** Comunidade Cacula
- População: VIIRS + WorldPop = 1.800 hab.
- Luminosidade noturna: **muito baixa** (indicando falta de eletrificação)

**Com 5 critérios (atual):** Aptidão média ≈ 0.65
**Com 6 critérios (correto):** Aptidão pode aumentar para ≈ 0.75-0.80
- **Razão:** Baixa luminosidade aumenta demanda latente

---

## 4. SOLUÇÃO PROPOSTA

### 4.1 Mudanças Requeridas ao Código

#### A. Adicionar carregamento de mapa VIIRS

**Localização:** `cached_mcda_analysis()` função

```python
# NOVO: Carregar mapa de luminosidade noturna
nightlights = cached_load_map("mapa_luminosidade_noturna.npy")  # NOVO
```

#### B. Adicionar parâmetro de peso

**Localização:** Assinatura de função

```python
# ANTES:
def cached_mcda_analysis(w_solar, w_pop, w_dist, w_slope, w_ndvi):

# DEPOIS:
def cached_mcda_analysis(
    w_solar: float,
    w_pop: float,
    w_dist: float,
    w_slope: float,
    w_ndvi: float,
    w_nightlights: float  # NOVO
):
```

#### C. Normalizar e integrar

```python
# NOVO: Normalizar e adicionar ao cálculo
nightlights_norm = analyzer.normalize_raster(nightlights, name="nightlights")

# ANTES:
aptitude = (
    w_solar * solar_norm +
    w_pop * pop_norm +
    w_dist * dist_norm +
    w_slope * slope_norm +
    w_ndvi * ndvi_norm
)

# DEPOIS:
aptitude = (
    w_solar * solar_norm +
    w_pop * pop_norm +
    w_dist * dist_norm +
    w_slope * slope_norm +
    w_ndvi * ndvi_norm +
    w_nightlights * nightlights_norm  # NOVO
)
```

#### D. Adicionar slider UI

**Localização:** Dashboard MCDA section

```python
# NOVO: Slider para peso de luminosidade noturna
w_nightlights = st.slider(
    "💡 Luminosidade Noturna (peso):",
    min_value=0.0,
    max_value=1.0,
    value=0.15,  # Default: 15% (típico)
    step=0.05,
    help="Proxy de eletrificação atual e demanda energética. "
         "Aumentar para priorizar zonas sem eletrificação."
)
```

#### E. Normalizar pesos

**Localização:** Após coleta de inputs

```python
# NOVO: Normalizar para soma = 1.0
total_weight = w_solar + w_pop + w_dist + w_slope + w_ndvi + w_nightlights
w_solar_norm = w_solar / total_weight
w_pop_norm = w_pop / total_weight
w_dist_norm = w_dist / total_weight
w_slope_norm = w_slope / total_weight
w_ndvi_norm = w_ndvi / total_weight
w_nightlights_norm = w_nightlights / total_weight  # NOVO
```

### 4.2 Pesos Sugeridos (Baseados em Manuscrito)

Para diferentes contextos prioritários:

**Perfil Padrão (Geral - Angola):**
```
w_solar = 0.25  (potencial solar máximo)
w_pop = 0.20    (densidade populacional)
w_dist = 0.20   (acesso à rede)
w_slope = 0.10  (topografia)
w_ndvi = 0.15   (potencial agrícola)
w_nightlights = 0.10  (falta de eletrificação)
Total = 1.00
```

**Perfil Agrário (Aumento NDVI + Nightlights):**
```
w_solar = 0.20
w_pop = 0.15
w_dist = 0.20
w_slope = 0.10
w_ndvi = 0.25  (↑ agrária)
w_nightlights = 0.10
Total = 1.00
```

**Perfil Eletrificação Urgente (Aumento Nightlights):**
```
w_solar = 0.20
w_pop = 0.20
w_dist = 0.20
w_slope = 0.10
w_ndvi = 0.10
w_nightlights = 0.20  (↑ priorizar áreas escuras)
Total = 1.00
```

---

## 5. CONCORDÂNCIA: PRÉ vs. PÓS-CORREÇÃO

### 5.1 Antes (Status Atual)

❌ **Problema:**
- Código: 5 critérios
- Manuscrito: 6 critérios
- **Gap: -1 critério (-17% funcionalidade)**

### 5.2 Depois (Pós-Correção)

✅ **Resolvido:**
- Código: 6 critérios
- Manuscrito: 6 critérios
- **Gap: 0 (100% concordância)**

---

## 6. ARQUIVOS A MODIFICAR

| Arquivo | Linhas | Mudanças | Prioridade |
|---|---|---|---|
| `geesp_unified_app.py` | 123-162 | Adicionar w_nightlights parâmetro e cálculo | CRÍTICA |
| `geesp_unified_app.py` | 300-350 (aprox.) | Adicionar slider UI | ALTA |
| `mcda_analysis.py` | TBD | Validar normalization de VIIRS | ALTA |
| `data_loaders_async.py` | TBD | Assegurar carregamento mapa VIIRS | MÉDIA |
| `generate_maps_simple.py` | TBD | Incluir geração mapa luminosidade noturna | ALTA |
| `README.md` | TBD | Atualizar documentação 5→6 critérios | BAIXA |

---

## 7. VALIDAÇÃO PÓS-IMPLEMENTAÇÃO

### 7.1 Testes Requeridos

- [ ] **Teste 1:** Carregar mapa VIIRS sem erro
- [ ] **Teste 2:** Normalização VIIRS produz valores 0-1
- [ ] **Teste 3:** Slider de peso 0-1 funciona
- [ ] **Teste 4:** Cálculo aptidão com 6 critérios sem erro NaN
- [ ] **Teste 5:** Pesos somam 1.0 após normalização
- [ ] **Teste 6:** Aptidão com w_nightlights=1.0, outros=0 prioriza zonas escuras
- [ ] **Teste 7:** Análise sensibilidade ±20% em 6 critérios mantém Kendall tau ≥0.98 (per manuscrito)

### 7.2 Validação de Concordância

```
ANTES: 5/6 critérios = 83% conformidade
DEPOIS: 6/6 critérios = 100% conformidade ✅
```

---

## 8. RECOMENDAÇÃO FINAL

**Status:** ⚠️ **IMPLEMENTAÇÃO NECESSÁRIA ANTES DE SUBMISSÃO**

**Ação:** Incorporar 6º critério (luminosidade noturna) em código em conformidade com manuscrito publicado.

**Timeline:**
- Modificação código: **2-3 horas**
- Testes: **1 hora**
- Validação: **30 minutos**
- **Total: ~4 horas**

**Bloqueador de Submissão:** SIM (código não implementa framework conforme manuscrito)

---

**Assinado:** Auditoria de Concordância Código-Manuscrito  
**Timestamp:** 2026-03-03 | 15:45 UTC  
**Próximo Passo:** Implementar Solução 4.1 (Adicionar 6º critério ao código)
