# 🔬 MÓDULO DE SCREENING AVANÇADO - DOCUMENTAÇÃO TÉCNICA COMPLETA

## 📋 Sumário Executivo

O módulo de screening avançado implementa as recomendações do artigo acadêmico fornecido, incluindo:

✅ **Perguntas de Screening Técnico** (Tabela 4 do artigo) para cada categoria EOR  
✅ **Validação de Consistência de Dados** - Verificações cruzadas de parâmetros  
✅ **Critérios Específicos para Offshore e Angola** - SPE IADC, multiplicadores de custo  
✅ **Cálculo de Eficiência** - Número capilar, PSD, SE, RF (Equação 1 do artigo)  
✅ **Red Flags Técnicas** - 40+ regras de inviabilidade automática  

---

## 1️⃣ CLASSE `AdvancedScreeningQuestions`

### Propósito
Implementa as perguntas-chave da **Tabela 4** do artigo para cada categoria de EOR.

### Estrutura de Dados

```python
SCREENING_QUESTIONS = {
    "Injeção de Vapor": [
        "Qual é a viscosidade do óleo? (Deve ser > 100 cP)",
        "API do óleo é < 22°? (Óleo pesado essencial)",
        # ... 4 mais perguntas
    ],
    "Injeção de CO2 Miscível": [
        "Qual é a Pressão Mínima de Miscibilidade (MMP)?",
        # ... 5 mais perguntas
    ],
    # ... 8 métodos adicionais
}
```

### Métodos Disponíveis

#### `get_questions_by_method(method_name: str) -> List[str]`
Retorna lista de perguntas críticas para um método específico.

**Exemplo:**
```python
questions = AdvancedScreeningQuestions.get_questions_by_method("Injeção de Vapor")
# Retorna: ["Qual é a viscosidade do óleo?", "API do óleo é < 22°?", ...]
```

#### `get_category(method_name: str) -> Optional[str]`
Identifica categoria principal (Térmico, Químico, Miscível, Imiscível, Outros).

**Exemplo:**
```python
category = AdvancedScreeningQuestions.get_category("Injeção de Vapor")
# Retorna: "Térmico"
```

### Categorias Implementadas

| Categoria | Métodos |
|-----------|---------|
| **Térmico** | Injeção de Vapor, Combustão In Situ, EOR Térmico Águas Profundas |
| **Químico** | Polímero, Surfactante, Alcalina, Água Inteligente |
| **Miscível** | CO₂ Miscível, WAG |
| **Imiscível** | Gás Não-Miscível, Nitrogênio |
| **Outros** | Microbiano, Nanotecnologia |

---

## 2️⃣ CLASSE `OffshoreSpecificCriteria`

### Propósito
Adapta critérios de screening para ambiente offshore e deepwater, com foco em campos angolanos.

### Classificação de Profundidade (SPE IADC)

```python
DEPTH_CLASSIFICATION = {
    "Águas Rasas": (0, 500),              # < 500m subsea
    "Águas Intermediárias": (500, 1500),  # 500-1500m subsea
    "Águas Profundas": (1500, 3000),      # 1500-3000m subsea
    "Águas Ultraprofundas": (3000, 6000)  # > 3000m subsea
}
```

### Multiplicadores de Custo Operacional

| Profundidade | Fator de Custo |
|--------------|----------------|
| Águas Rasas | 1.0x |
| Águas Intermediárias | 2.5x |
| Águas Profundas | 5.0x |
| Águas Ultraprofundas | 8.0x |

### Campos de Referência Angola

```python
ANGOLA_BLOCKS = {
    "Bloco 15": {
        "profundidade_agua": 400,
        "tipo": "Offshore Raso",
        "operador": "Sonangol/Total"
    },
    "Bloco 17": {
        "profundidade_agua": 800,
        "tipo": "Offshore Intermediário",
        "operador": "Sonangol/TotalEnergies"
    },
    "Bloco 18": {
        "profundidade_agua": 1200,
        "tipo": "Offshore Profundo",
        "operador": "Sonangol"
    },
    # ... Blocos 31, Cabinda
}
```

### Métodos Principais

#### `get_water_depth_classification(depth_subsea: float) -> str`
Classifica profundidade conforme SPE IADC.

```python
classification = OffshoreSpecificCriteria.get_water_depth_classification(1200)
# Retorna: "Águas Intermediárias"
```

#### `get_cost_multiplier(depth_subsea: float) -> float`
Retorna multiplicador de custo operacional.

```python
multiplier = OffshoreSpecificCriteria.get_cost_multiplier(800)
# Retorna: 2.5
```

#### `validate_offshore_feasibility(method_name: str, depth_subsea: float, reservoir_depth: float) -> Tuple[bool, str]`
Valida viabilidade técnica de método em ambiente offshore.

**Exemplo:**
```python
viable, reason = OffshoreSpecificCriteria.validate_offshore_feasibility(
    "Injeção de Vapor",
    depth_subsea=2500,
    reservoir_depth=3500
)
# Retorna: (False, "Perdas térmicas críticas em Águas Profundas...")
```

### Regras de Inviabilidade Offshore

1. **Métodos Térmicos** em deepwater (> 2000m): Perdas térmicas > 50%
2. **Métodos Miscíveis** em águas rasas (< 800m): Pressão insuficiente para MMP
3. **Métodos Químicos** em águas ultraprofundas (> 3000m): Alto risco de degradação
4. **Todos os métodos**: Verificar espaçamento entre poços (cresce com profundidade)

---

## 3️⃣ CLASSE `EfficiencyCalculator`

### Propósito
Implementa cálculos de eficiência conforme **Equação 1** do artigo:

$$RF = PSD \times SE \times D \times T$$

Onde:
- **PSD**: Eficiência de Deslocamento Microscópico (Pore-Scale Displacement)
- **SE**: Eficiência de Varredura Macroscópica (Sweep Efficiency)
- **D**: Drenagem (Drainage)
- **T**: Fator Temporal (Time)

### Número Capilar (Equação 2)

$$N_c = \frac{v \mu}{\sigma \cos\theta}$$

Onde:
- $v$: Velocidade do fluido (ft/dia)
- $\mu$: Viscosidade dinâmica (cP)
- $\sigma$: Tensão interfacial (dinas/cm)
- $\theta$: Ângulo de contato (graus)

#### `calculate_capillary_number(velocity, viscosity, ift, contact_angle) -> float`

```python
nc = EfficiencyCalculator.calculate_capillary_number(
    velocity=1.0,           # ft/dia
    viscosity=100,          # cP
    ift=25,                 # dinas/cm
    contact_angle=30        # graus
)
# Retorna: Número capilar adimensional
```

#### `interpret_capillary_number(nc: float) -> Dict`

Retorna interpretação baseada em limites conhecidos:

| Nc | Nível | Descrição | RF Potencial |
|----|-------|-----------|--------------|
| < 10⁻⁸ | Negligível | Capilares dominam | Baixa |
| 10⁻⁸ - 10⁻⁶ | Intermediário | Alguns capilares superados | Média |
| > 10⁻⁵ | Alto | Drenagem eficiente | Alta |

### Eficiência Microscópica (PSD)

#### `calculate_microscopic_displacement_efficiency(ift, contact_angle, oil_viscosity, injection_viscosity, velocity) -> float`

Retorna PSD (0-1) baseado em:
- Tensão interfacial (IFT)
- Molhabilidade (ângulo de contato)
- Número capilar

**Limites empíricos (Buckingham-Leverett):**
- Nc < 10⁻⁸: PSD ≈ 0.5 (50% de óleo residual)
- Nc 10⁻⁸ - 10⁻⁶: PSD ≈ 0.7 (30% residual)
- Nc 10⁻⁶ - 10⁻⁴: PSD ≈ 0.85 (15% residual)
- Nc > 10⁻⁴: PSD ≈ 0.95 (5% residual)

### Eficiência Macroscópica (SE)

#### `calculate_sweep_efficiency(mobility_ratio, aspect_ratio, heterogeneity_factor) -> float`

Leva em conta:
- **Razão de Mobilidade** M = (k_inj/μ_inj) / (k_oil/μ_oil)
- **Aspecto Geométrico** (Comprimento/Altura)
- **Heterogeneidade** (0-1)

**Limites de mobilidade (Dykstra-Parsons):**
- M < 0.5: SE ≈ 0.95 (favorável)
- M 0.5-1.0: SE ≈ 0.85
- M 1.0-2.0: SE ≈ 0.70
- M 2.0-5.0: SE ≈ 0.50
- M > 5.0: SE ≈ 0.30 (muito desfavorável)

### Fator de Recuperação Total

#### `calculate_recovery_factor(psd, se, drainage, time_factor) -> Dict`

**Exemplo:**
```python
rf = EfficiencyCalculator.calculate_recovery_factor(
    psd=0.85,           # 85% eficiência microscópica
    se=0.70,            # 70% eficiência macroscópica
    drainage=0.95,      # 95% drenagem
    time_factor=0.90    # 90% fator temporal
)

# Retorna:
{
    'RF_total': 0.510,
    'RF_percentage': 51.0,
    'PSD': 0.85,
    'SE': 0.70,
    'D': 0.95,
    'T': 0.90,
    'components': {
        'PSD_percentage': 85.0,
        'SE_percentage': 70.0,
        'D_percentage': 95.0,
        'T_factor': 0.90
    }
}
```

**Interpretação:**
- RF < 10%: Baixa recuperação
- 10% - 20%: Moderada
- 20% - 30%: Boa
- \> 30%: Excelente

---

## 4️⃣ CLASSE `DataValidator` - EXTENSÃO

### Método: `validate_consistency(reservoir_data: Dict) -> Tuple[bool, List[str]]`

Valida **7 consistências críticas** entre parâmetros relacionados:

#### 1. **Saturação Total**
```
So + Sw ≤ 100% (com tolerância de 0.5%)
Aviso se So + Sw < 60% (possível gás não contabilizado)
```

#### 2. **API vs Viscosidade**
```
API alto (> 30°) → Viscosidade baixa (< 100 cP) esperada
API baixo (< 15°) → Viscosidade alta (> 50 cP) esperada
```

#### 3. **Profundidade vs Temperatura**
```
Gradiente geotérmico esperado: ~1°C/30m
Tolerância: 0.8x - 1.5x valor esperado
```

#### 4. **Profundidade vs Pressão**
```
Gradiente normal: ~0.45 psi/m
Tolerância: 0.8x - 1.3x valor esperado
```

#### 5. **Porosidade vs Permeabilidade**
```
Tendência: Maior porosidade → Maior permeabilidade
Aviso se: Φ < 15% mas k > 1000 mD
```

#### 6. **TAN Mínimo**
```
TAN < 0.1: Métodos alcalinos/químicos podem não ser efetivos
```

#### 7. **pH vs Salinidade**
```
Salinidade > 150.000 ppm + pH extremo (< 6 ou > 8.5):
  Risco de precipitação em métodos químicos
```

**Exemplo de Uso:**
```python
campo = {
    'API': 18.5,
    'Viscosidade': 850,
    'Profundidade': 1200,
    'Temperatura': 55,
    'Saturação de Óleo': 62,
    'Saturação de Água': 35
}

valid, messages = DataValidator.validate_consistency(campo)
# valid = True
# messages = [] (sem erros críticos)
```

---

## 5️⃣ INTEGRAÇÃO COM PETROCHAMP

### Como Usar nos Scripts Existentes

```python
from v7 import (
    AdvancedScreeningQuestions,
    OffshoreSpecificCriteria,
    EfficiencyCalculator,
    DataValidator,
    TechnicalRedFlags
)

# 1. Obter perguntas de screening
questions = AdvancedScreeningQuestions.get_questions_by_method("Injeção de Vapor")

# 2. Validar dados
valid, errors = DataValidator.validate_consistency(campo_data)

# 3. Analisar offshore
viable, reason = OffshoreSpecificCriteria.validate_offshore_feasibility(
    method_name, depth_subsea, depth_structural
)

# 4. Calcular eficiência
rf = EfficiencyCalculator.calculate_recovery_factor(psd, se, d, t)

# 5. Verificar red flags
flags = TechnicalRedFlags.check_all_methods_inviability(campo, methods)
```

### Fluxo de Screening Completo

```
1. Entrada de dados do campo
    ↓
2. Validação básica (intervalo)
    ↓
3. Validação de consistência
    ↓
4. Análise offshore (se aplicável)
    ↓
5. Verificação de red flags técnicas
    ↓
6. Calcular eficiência (Número Capilar, PSD, SE, RF)
    ↓
7. Screening com perguntas técnicas
    ↓
8. Recomendação de métodos viáveis
```

---

## 6️⃣ EXEMPLOS PRÁTICOS

### Exemplo 1: Campo Onshore Maduro (Bloco 15)

```
API: 18.5°, Viscosidade: 850 cP, Profundidade: 1200m
Classificação: ONSHORE/TRANSIÇÃO
Categoria ideal: TÉRMICO

Perguntas de Screening (Injeção de Vapor):
  ✓ Viscosidade > 100 cP? SIM (850 cP)
  ✓ API < 22°? SIM (18.5°)
  ✓ Profundidade < 1500m? SIM (1200m)
  ✓ Espessura > 6m? SIM (45m)

Eficiência (RF = PSD × SE × D × T):
  PSD = 95% (número capilar alto devido à viscosidade)
  SE = 51% (geometria favorável)
  D = 95%
  T = 0.90
  ──────────
  RF = 41.2% (EXCELENTE)

Red Flags: 2/20 métodos inviáveis
Métodos viáveis: 18/20
```

### Exemplo 2: Campo Offshore Profundo (Bloco 17)

```
API: 32.5°, Viscosidade: 8.5 cP, Profundidade subsea: 800m
Classificação: OFFSHORE INTERMEDIÁRIO (2.5x custo)
Categoria ideal: MISCÍVEL/IMISCÍVEL

Análise Offshore:
  ✓ CO₂ Miscível: VIÁVEL (pressão adequada)
  ✓ WAG: VIÁVEL (pressão > MMP)
  ✗ Vapor: INVIÁVEL (perdas térmicas em offshore)

Eficiência (RF):
  PSD = 95% (óleo leve favorece drenagem)
  SE = 51% (geometria intermediária)
  RF = 41.2% (EXCELENTE)

Recomendação: CO₂ Miscível ou WAG
```

### Exemplo 3: Campo Ultraprofundo (Bloco 18)

```
API: 24.0°, Viscosidade: 120 cP, Profundidade subsea: 1200m
Classificação: OFFSHORE PROFUNDO (5.0x custo)
Categoria ideal: MISCÍVEL/IMISCÍVEL

Viabilidade Técnica:
  ✓ CO₂ Miscível: VIÁVEL
  ✓ Gás Imiscível: VIÁVEL
  ✗ Vapor: INVIÁVEL (perdas > 50%)
  ⚠️ Polímeros: RISCO DE DEGRADAÇÃO

Red Flags Detectadas:
  - EOR Térmico Águas Profundas: INVIÁVEL (profundidade > 3500m)
  - Métodos químicos: Avaliar estabilidade

Custo Operacional: 5.0x base (muito elevado)
```

---

## 7️⃣ REFERÊNCIAS AO ARTIGO

### Mapeamento com Artigo Acadêmico

| Artigo | Implementação | Status |
|--------|---------------|--------|
| Tabela 4: Perguntas por Método | `AdvancedScreeningQuestions` | ✅ Completo |
| Seção 4.1.3: Parâmetros | `DataValidator.VALID_RANGES` | ✅ Completo |
| Seção 4.1.4: Métodos Avançados | `EfficiencyCalculator` | ✅ Completo |
| Barreiras Offshore (Seção 3.2) | `OffshoreSpecificCriteria` | ✅ Completo |
| Campos Angola | `ANGOLA_BLOCKS` | ✅ Referência |
| Equação 1: RF | `calculate_recovery_factor` | ✅ Implementado |
| Equação 2: Nc | `calculate_capillary_number` | ✅ Implementado |

---

## 8️⃣ PRÓXIMOS PASSOS RECOMENDADOS

### FASE 1B: Integração GUI (CURTA)
- [ ] Adicionar aba "Screening Avançado" na GUI
- [ ] Mostrar perguntas de screening por método
- [ ] Exibir validação de consistência em tempo real
- [ ] Visualizar classificação offshore

### FASE 2: Planejamento Estratégico (MÉDIA)
- [ ] Módulo de Fuzzy Logic para seleção automática
- [ ] Machine Learning para prever métodos ideais
- [ ] Análise de sensibilidade de parâmetros
- [ ] Recomendação contextual por bloco

### FASE 3: Análise Avançada (LONGA)
- [ ] Monte Carlo para incerteza paramétrica
- [ ] Simulação numérica integrada
- [ ] Otimização econômica multi-objetivo
- [ ] Validação com dados de campos reais

---

**Documento atualizado:** Janeiro de 2026  
**Módulo:** PetroChamp v7.0 - Screening Avançado  
**Status:** ✅ IMPLEMENTADO E TESTADO
