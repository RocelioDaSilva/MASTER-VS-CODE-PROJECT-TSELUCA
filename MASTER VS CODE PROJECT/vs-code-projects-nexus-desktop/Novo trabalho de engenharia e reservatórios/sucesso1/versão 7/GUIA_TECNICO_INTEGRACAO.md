# 🔧 GUIA TÉCNICO - INTEGRAÇÃO DE NOVOS MÉTODOS EOR E RED FLAGS

**Versão:** 7.0.0 (FASE 1)  
**Data:** 22 de Janeiro de 2026  
**Nível:** Desenvolvedor/Integrador

---

## 📑 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Novos Métodos EOR](#novos-métodos-eor)
3. [Sistema de Red Flags](#sistema-de-red-flags)
4. [Exemplos de Código](#exemplos-de-código)
5. [Referências Técnicas](#referências-técnicas)

---

## 🎯 Visão Geral

v7.0 expande PetroChamp com:
- **20 métodos EOR** (antes: 15)
- **Sistema automático de validação técnica** (Red Flags)
- **Critérios específicos para campos angolanos**
- **Justificações contextualizadas**

### Compatibilidade
- ✅ 100% compatível com v6.0
- ✅ Interface gráfica sem mudanças
- ✅ Banco de dados não afetado
- ✅ Retrocompatível

---

## 🆕 Novos Métodos EOR

### 1. Injeção Cíclica de Vapor (CSS)

**Classe:** `EORScreeningEngine.criteria["Injeção Cíclica de Vapor (CSS)"]`

**Critérios:**
```python
{
    "API": {"min": None, "max": 25, "peso": 0.3},
    "Viscosidade": {"min": 50, "max": 10000, "peso": 0.35},
    "Profundidade": {"min": 150, "max": 2000, "peso": 0.15},
    "Espessura": {"min": 5, "max": None, "peso": 0.1},
    "Saturação de Óleo": {"min": 35, "max": None, "peso": 0.1}
}
```

**Aplicabilidade:** Campos maduros, onshore, óleo pesado  
**Recuperação adicional:** 5-20% OOIP  
**CAPEX:** US$ 3-8 milhões  
**OPEX:** US$ 2-4/bbl  

**Red Flags:**
- ❌ API > 22° (anti-econômico)
- ❌ Viscosidade < 100 cP (não justifica)
- ❌ Profundidade > 2000m (perdas térmicas)
- ❌ Espessura < 5m (eficiência baixa)

---

### 2. Injeção de Gás com Alternância de Água (WAG)

**Classe:** `EORScreeningEngine.criteria["Injeção de Gás com Alternância de Água (WAG)"]`

**Critérios:**
```python
{
    "API": {"min": 20, "max": None, "peso": 0.25},
    "Viscosidade": {"min": None, "max": 50, "peso": 0.2},
    "Pressão": {"min": 1000, "max": None, "peso": 0.2},
    "Profundidade": {"min": 800, "max": 3500, "peso": 0.15},
    "Permeabilidade": {"min": 50, "max": 2000, "peso": 0.2}
}
```

**Aplicabilidade:** Campos offshore, API leve a médio  
**Recuperação adicional:** 15-25% OOIP  
**Vantagem:** Reduz gas fingering em 40-60%  
**Ideal para:** Angola (Blocos 15, 17, 18)

**Red Flags:**
- ❌ API < 20° (não se miscibiliza bem)
- ❌ Viscosidade > 50 cP (mobilidade reduzida)
- ❌ Profundidade > 3500m (operações complexas)
- ❌ Pressão < 1000 psi (miscibilidade comprometida)

---

### 3. Injeção de Baixa Salinidade (LoSal)

**Classe:** `EORScreeningEngine.criteria["Injeção de Baixa Salinidade (LoSal)"]`

**Critérios:**
```python
{
    "Viscosidade": {"min": None, "max": 200, "peso": 0.2},
    "Salinidade": {"min": 30000, "max": None, "peso": 0.3},
    "Temperatura": {"min": None, "max": 100, "peso": 0.15},
    "Permeabilidade": {"min": 10, "max": 2000, "peso": 0.2},
    "TAN": {"min": 0.2, "max": None, "peso": 0.15}
}
```

**Aplicabilidade:** Retrofit em campos existentes, alta salinidade  
**Recuperação adicional:** 5-15% OOIP  
**CAPEX:** Mínimo (retrofit)  
**OPEX:** Tratamento de água

**Mecanismo:** Alteração de molhabilidade por redução de salinidade  
**Compatibilidade:** Campos com água de formação salina

**Red Flags:**
- ❌ Salinidade < 30.000 ppm (benefício limitado)
- ❌ TAN < 0.2 mg KOH/g (reação insuficiente)
- ❌ Temperatura > 100°C (adsorção afetada)
- ❌ Permeabilidade < 10 mD (distribuição comprometida)

---

### 4. Nanotecnologia aplicada ao EOR

**Classe:** `EORScreeningEngine.criteria["Nanotecnologia aplicada ao EOR"]`

**Critérios:**
```python
{
    "API": {"min": 10, "max": 40, "peso": 0.2},
    "Viscosidade": {"min": None, "max": 500, "peso": 0.2},
    "Salinidade": {"min": None, "max": 200000, "peso": 0.2},
    "Temperatura": {"min": 20, "max": 120, "peso": 0.2},
    "Permeabilidade": {"min": 1, "max": 5000, "peso": 0.2}
}
```

**Aplicabilidade:** Ampla compatibilidade, tecnologia emergente  
**Recuperação adicional:** 8-20% OOIP  
**Custo:** US$ 1-3/bbl  
**Mecanismo:** Aumento de mobilidade, redução de IFT

**Tipos de Nanopartículas:**
- Sílica (SiO₂)
- Óxido de ferro (Fe₃O₄)
- Compósitos polímero-nano
- Nanopartículas ativadas

**Red Flags:**
- ❌ Salinidade > 200.000 ppm (agregação)
- ❌ Temperatura > 120°C (degradação)
- ❌ API < 10° (óleo muito pesado)
- ❌ API > 40° (óleo muito leve)

---

### 5. EOR Térmico para Águas Profundas

**Classe:** `EORScreeningEngine.criteria["EOR Térmico para Águas Profundas"]`

**Critérios:**
```python
{
    "API": {"min": None, "max": 24, "peso": 0.3},
    "Viscosidade": {"min": 80, "max": 5000, "peso": 0.3},
    "Profundidade": {"min": 1000, "max": 3500, "peso": 0.2},
    "Temperatura": {"min": None, "max": 130, "peso": 0.1},
    "Pressão": {"min": 500, "max": None, "peso": 0.1}
}
```

**Aplicabilidade:** Campos offshore profundos, óleo pesado  
**Profundidade de água:** 500-3500m  
**Recuperação adicional:** 10-20% OOIP  
**Custo CAPEX:** US$ 50-150 milhões  

**Desafios:**
- Perdas térmicas em água fria
- Isolamento térmico de tubulação
- Trocadores de calor submarinos
- Monitoramento subsuperficial

**Red Flags:**
- ❌ Profundidade > 3500m (perdas > 50%)
- ❌ API > 24° (custo ineficiente)
- ❌ Temperatura > 130°C (instabilidade)
- ❌ Pressão < 500 psi (problemas estruturais)

---

## ⚠️ Sistema de Red Flags

### Visão Geral

Classe `TechnicalRedFlags` implementa validação automática de inviabilidades técnicas.

### Uso Básico

```python
from v7 import TechnicalRedFlags, EORScreeningEngine

# Dados do reservatório
campo = {
    'API': 18,
    'Viscosidade': 350,
    'Profundidade': 1200,
    'Temperatura': 65,
    # ... outros parâmetros
}

# Verificar para um método específico
red_flags = TechnicalRedFlags.check_reservoir_inviability(
    campo, 
    "Injeção de Vapor"
)

if red_flags:
    print(f"❌ {len(red_flags)} inviabilidades detectadas")
    for flag in red_flags:
        print(f"  • {flag['mensagem']}")
```

### Estrutura de Red Flag

```python
{
    "método": str,              # Nome do método EOR
    "parâmetro": str,          # Nome do parâmetro (API, Viscosidade, etc)
    "valor": float,            # Valor atual do parâmetro
    "limite": float,           # Limite técnico
    "tipo": str,               # "máximo excedido" ou "mínimo não atingido"
    "mensagem": str,           # Descrição textual do problema
    "severidade": str          # "CRÍTICA" (todas são críticas por padrão)
}
```

### Métodos Principais

#### 1. `check_reservoir_inviability()`

Detecta inviabilidades para um método específico.

```python
red_flags = TechnicalRedFlags.check_reservoir_inviability(
    reservoir_data=campo,
    method="Injeção de Polímeros"
)
# Retorna: List[Dict] com flags detectadas
```

#### 2. `check_all_methods_inviability()`

Executa verificação para todos os métodos.

```python
from v7 import EORScreeningEngine

screening = EORScreeningEngine()
all_flags = TechnicalRedFlags.check_all_methods_inviability(
    reservoir_data=campo,
    all_methods=screening.methods
)
# Retorna: Dict[str, List[Dict]] {método: [flags]}
```

#### 3. `get_inviability_report()`

Gera relatório textual formatado.

```python
report = TechnicalRedFlags.get_inviability_report(
    reservoir_data=campo,
    all_methods=screening.methods
)
print(report)
```

### Exemplo de Saída

```
⚠️ RELATÓRIO DE INVIABILIDADES TÉCNICAS (RED FLAGS)
================================================================================

❌ Injeção de Vapor
────────────────────────────────────────────────────────────────────────────
  • API > 22° torna injeção de vapor anti-econômica
    Parâmetro: API
    Valor: 25.50 | Limite: 22.00
    Severidade: CRÍTICA

  • Profundidade > 3500m inviável para vapor por perdas térmicas
    Parâmetro: Profundidade
    Valor: 4200.00 | Limite: 3500.00
    Severidade: CRÍTICA

================================================================================
RESUMO: 2 método(s) com inviabilidade técnica detectada
MÉTODOS VIÁVEIS: 18/20
```

---

## 💻 Exemplos de Código

### Exemplo 1: Análise Simples de Campo

```python
from v7 import EORScreeningEngine, TechnicalRedFlags

# Dados do campo
campo_angola = {
    'API': 18.5,
    'Viscosidade': 850,
    'Profundidade': 1200,
    'Salinidade': 85000,
    'Temperatura': 65,
    # ... outros parâmetros
}

# Triagem técnica
screening = EORScreeningEngine()
scores = screening.score_reservoir(campo_angola)

# Validação técnica
inviabilities = TechnicalRedFlags.check_all_methods_inviability(
    campo_angola,
    screening.methods
)

# Filtrar métodos viáveis
viable_methods = {
    method: score for method, score in scores.items()
    if method not in inviabilities
}

# Top 3 viáveis
top_3 = sorted(
    viable_methods.items(),
    key=lambda x: x[1]['score'],
    reverse=True
)[:3]

print("Top 3 Métodos Recomendados:")
for i, (method, data) in enumerate(top_3, 1):
    print(f"{i}. {method}: {data['score']:.1f}%")
```

### Exemplo 2: Integração com Interface Gráfica

```python
def run_screening_with_validation(self):
    """Método para integração com GUI de PetroChamp"""
    
    # Colher dados da interface
    reservoir_data = self._collect_reservoir_data()
    
    # Validação básica
    valid, errors = DataValidator.validate_reservoir_data(reservoir_data)
    if not valid:
        messagebox.showerror("Erro de Dados", f"Erros: {errors}")
        return
    
    # Triagem técnica
    screening = EORScreeningEngine()
    scores = screening.score_reservoir(reservoir_data)
    
    # Red flags automáticas
    inviabilities = TechnicalRedFlags.check_all_methods_inviability(
        reservoir_data,
        screening.methods
    )
    
    # Gerar relatório
    if inviabilities:
        report = TechnicalRedFlags.get_inviability_report(
            reservoir_data,
            screening.methods
        )
        messagebox.showwarning(
            "Validação Técnica",
            report
        )
    
    # Atualizar display
    self._update_results_table(scores, inviabilities)
```

### Exemplo 3: Relatório Executivo

```python
def generate_executive_report(campo: Dict):
    """Gera relatório executivo com análise técnica"""
    
    from v7 import EORScreeningEngine, TechnicalRedFlags
    
    screening = EORScreeningEngine()
    scores = screening.score_reservoir(campo)
    
    report = f"""
    ╔════════════════════════════════════════════════════════════╗
    ║         RELATÓRIO DE AVALIAÇÃO EOR - FASE 1               ║
    ╚════════════════════════════════════════════════════════════╝
    
    CAMPO: {campo.get('nome', 'Sem identificação')}
    
    PARÂMETROS PRINCIPAIS:
    • API Gravity: {campo.get('API', 'N/A')}°
    • Viscosidade: {campo.get('Viscosidade', 'N/A')} cP
    • Profundidade: {campo.get('Profundidade', 'N/A')} m
    • Temperatura: {campo.get('Temperatura', 'N/A')}°C
    
    MELHORES OPÇÕES EOR:
    """
    
    top_3 = sorted(
        scores.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )[:3]
    
    for i, (method, data) in enumerate(top_3, 1):
        report += f"\n    {i}. {method}"
        report += f"\n       Score: {data['score']:.1f}%"
        report += f"\n       Status: {data['status']}"
    
    # Red flags
    inviabilities = TechnicalRedFlags.check_all_methods_inviability(
        campo,
        screening.methods
    )
    
    if inviabilities:
        report += f"\n\n    LIMITAÇÕES TÉCNICAS: {len(inviabilities)} métodos com restrições"
    
    return report
```

---

## 📋 Referências Técnicas

### Tabela de Limites Críticos

| Parâmetro | CSS | WAG | LoSal | Nanotech | Deepwater |
|-----------|-----|-----|-------|----------|-----------|
| **API máx** | 22° | ∞ | ∞ | 40° | 24° |
| **Viscosidade máx** | ∞ | 50 cP | 200 cP | 500 cP | 5000 cP |
| **Profundidade máx** | 2000m | 3500m | ∞ | ∞ | 3500m |
| **Temperatura máx** | ∞ | ∞ | 100°C | 120°C | 130°C |
| **Salinidade máx** | ∞ | ∞ | ∞ | 200k ppm | ∞ |

### Fórmulas de Viabilidade

**CSS Viável se:**
```
API ≤ 22° AND Viscosidade ≥ 100 cP AND Profundidade ≤ 2000m AND Espessura ≥ 6m
```

**WAG Viável se:**
```
API ≥ 20° AND Viscosidade ≤ 50 cP AND 800m ≤ Profundidade ≤ 3500m AND Pressão ≥ 1000 psi
```

**LoSal Viável se:**
```
Salinidade ≥ 30000 ppm AND TAN ≥ 0.2 AND Temperatura ≤ 100°C
```

### Estimativas de Recuperação

| Método | Baixa | Média | Alta |
|--------|-------|-------|------|
| CSS | 5% OOIP | 12% OOIP | 20% OOIP |
| WAG | 15% OOIP | 20% OOIP | 25% OOIP |
| LoSal | 5% OOIP | 10% OOIP | 15% OOIP |
| Nanotech | 8% OOIP | 14% OOIP | 20% OOIP |
| Deepwater | 10% OOIP | 15% OOIP | 20% OOIP |

---

## ✅ Checklist de Integração

- [ ] v7.py importado corretamente
- [ ] TechnicalRedFlags acessível
- [ ] EORScreeningEngine instanciado
- [ ] Red flags executados antes de exibir resultados
- [ ] Mensagens de erro/aviso capturam inviabilidades
- [ ] Relatórios incluem seção de validação técnica
- [ ] GUI atualizada para exibir red flags

---

## 📞 Suporte

**Dúvidas técnicas:**
- Consultar docstrings em v7.py
- Executar exemplo_red_flags.py
- Revisar FASE1_IMPLEMENTACOES.md

**Problemas:**
- Verificar v7.py compila: `python -m py_compile v7.py`
- Validar dados com DataValidator
- Consultar logs de erro

---

**Versão:** 7.0.0-FASE1  
**Atualizado:** 22 de Janeiro de 2026  
**Status:** ✅ Produção
