# EXEMPLOS DE USO - PetroChamp v6.1

## 📚 Exemplos Práticos de Código

### 1. **Importar e Analisar Reservatório**

```python
# Importar módulos
from v6 import EORScreeningEngine, SuitabilityVisualizer

# Criar engine
engine = EORScreeningEngine()

# Dados do reservatório
reservoir = {
    'API': 28,                    # Óleo leve-médio
    'Viscosidade': 45,           # cP
    'Profundidade': 1200,        # metros
    'Permeabilidade': 200,       # mD
    'Porosidade': 18,            # %
    'Saturação de Óleo': 65,     # %
    'Saturação de Água': 35,     # %
    'Temperatura': 75,           # °C
    'Pressão': 1500,             # psi
    'Salinidade': 45000,         # ppm
    'Espessura': 25,             # metros
    'TAN': 0.8,                  # mg KOH/g
    'pH': 7.2,
    'Dip': 12                    # graus
}

# Calcular scores
scores = engine.score_reservoir(reservoir)

# Obter top 3 recomendações
recommendations = engine.get_recommendations(reservoir, top_n=3)

for method, data in recommendations:
    print(f"{method}: {data['score']:.1f}% - {data['status']}")
```

**Saída Esperada:**
```
Injeção de CO2 Miscível: 87.5% - RECOMENDADO
Injeção de Nitrogênio: 75.3% - POTENCIAL
Injeção de Gás Enriquecido: 72.1% - POTENCIAL
```

---

### 2. **Validar Dados de Entrada**

```python
from v6 import DataValidator

# Validador
validator = DataValidator()

# Dados questionáveis
data_to_check = {
    'API': 5,               # OK (intervalo válido)
    'Viscosidade': 500000,  # ERRO (acima do limite)
    'Temperatura': 300      # ERRO (acima do limite)
}

# Validar
valid, errors = validator.validate_reservoir_data(data_to_check)

if not valid:
    for error in errors:
        print(f"❌ {error}")
else:
    print("✅ Todos os dados são válidos")
```

**Saída Esperada:**
```
❌ Viscosidade: 500000.0 fora do intervalo [0.1, 100000]
❌ Temperatura: 300 fora do intervalo [-50, 250]
```

---

### 3. **Análise Econômica Completa**

```python
from v6 import EconomicAnalyzer

# Criar analisador
analyzer = EconomicAnalyzer()

# Parâmetros econômicos
econ_params = {
    'oil_price': 75,         # US$/bbl
    'discount_rate': 12,     # %
    'tax_rate': 25,          # %
    'project_life': 15,      # anos
    'decline_rate': 10       # %/ano
}

# Validar parâmetros
if not analyzer.validate_economic_params(econ_params):
    print("Parâmetros econômicos inválidos")
else:
    # Gerar perfil de produção
    initial_rate = 5000  # bbl/dia
    production = analyzer.generate_production_profile(
        initial_rate, 
        econ_params['decline_rate'], 
        econ_params['project_life']
    )
    
    # Calcular fluxo de caixa
    cf_data = analyzer.calculate_cash_flow(production, econ_params)
    
    # Calcular métricas
    npv = analyzer.calculate_npv(
        cf_data['cash_flow'], 
        econ_params['discount_rate']
    )
    irr = analyzer.calculate_irr(cf_data['cash_flow'])
    payback = analyzer.calculate_payback(cf_data['cash_flow'])
    
    print(f"NPV: ${npv:,.0f}")
    print(f"IRR: {irr:.2f}%")
    print(f"Payback: {payback:.1f} anos")
```

**Saída Esperada:**
```
NPV: $45,234,567
IRR: 18.50%
Payback: 4.2 anos
```

---

### 4. **Usar Cache para Operações Repetidas**

```python
from v6 import CacheManager
import time

# Criar cache
cache = CacheManager(max_size=50)

def expensive_calculation(x):
    """Cálculo custoso (simula demora)"""
    time.sleep(1)
    return x ** 2

# Primeira chamada (não em cache)
key = "expensive_100"
result = cache.get(key)

if result is None:
    result = expensive_calculation(100)
    cache.set(key, result)
    print(f"Calculado: {result} (1.0 segundo)")
else:
    print(f"Do cache: {result} (<0.001 segundo)")

# Segunda chamada (do cache)
result = cache.get(key)
if result is not None:
    print(f"Do cache: {result} (<0.001 segundo)")
```

---

### 5. **Gerar Gráfico de Suitability**

```python
from v6 import SuitabilityVisualizer, EORScreeningEngine
import matplotlib.pyplot as plt

# Engine e visualizador
engine = EORScreeningEngine()
viz = SuitabilityVisualizer()

# Dados
reservoir = {
    'API': 32,
    'Viscosidade': 8,
    'Profundidade': 2200,
    'Temperatura': 85,
    'Permeabilidade': 150,
    # ... outros parâmetros
}

# Calcular scores
scores = engine.score_reservoir(reservoir)

# Criar gráfico spider
fig = viz.create_spider_chart(scores)
plt.show()

# Criar matriz de suitability
fig2 = viz.create_suitability_matrix(reservoir, 
    {m: data['criteria_scores'] for m, data in scores.items()})
plt.show()

# Criar comparativo
fig3 = viz.create_comparison_chart(scores)
plt.show()
```

---

### 6. **Gerar Relatório Completo**

```python
from v6 import EORScreeningEngine

engine = EORScreeningEngine()

# Dados
reservoir = {
    'API': 28,
    'Viscosidade': 45,
    'Profundidade': 1200,
    # ... outros parâmetros
}

# Gerar relatório
report = engine.generate_justification_report(reservoir)

# Salvar em arquivo
with open('analise_suitability.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("Relatório salvo em: analise_suitability.txt")

# Ou visualizar no console
print(report)
```

---

### 7. **Workflow Completo Automático**

```python
from v6 import (
    EORScreeningEngine, 
    EconomicAnalyzer, 
    SuitabilityVisualizer,
    DataValidator
)
import matplotlib.pyplot as plt

def analyze_reservoir(reservoir_data, econ_params):
    """
    Análise completa de um reservatório
    Retorna: scores, económicos, gráficos
    """
    
    # 1. Validar dados
    print("1️⃣  Validando dados...")
    validator = DataValidator()
    valid, errors = validator.validate_reservoir_data(reservoir_data)
    if not valid:
        print(f"❌ Erros de validação: {errors}")
        return None
    print("✅ Dados válidos")
    
    # 2. Triagem EOR
    print("\n2️⃣  Executando triagem EOR...")
    engine = EORScreeningEngine()
    scores = engine.score_reservoir(reservoir_data)
    recommendations = engine.get_recommendations(reservoir_data, top_n=3)
    print("✅ Triagem concluída")
    
    # 3. Análise de Suitability
    print("\n3️⃣  Analisando suitability...")
    viz = SuitabilityVisualizer()
    fig1 = viz.create_spider_chart(scores)
    fig2 = viz.create_comparison_chart(scores)
    print("✅ Gráficos de suitability gerados")
    
    # 4. Análise Econômica
    print("\n4️⃣  Executando análise econômica...")
    analyzer = EconomicAnalyzer()
    
    initial_rate = econ_params.get('production_rate', 2000)
    decline = econ_params.get('decline_rate', 10)
    years = econ_params.get('project_life', 15)
    
    production = analyzer.generate_production_profile(
        initial_rate, decline, years
    )
    
    cf_data = analyzer.calculate_cash_flow(production, econ_params)
    npv = analyzer.calculate_npv(
        cf_data['cash_flow'], 
        econ_params['discount_rate']
    )
    irr = analyzer.calculate_irr(cf_data['cash_flow'])
    payback = analyzer.calculate_payback(cf_data['cash_flow'])
    
    print("✅ Análise econômica concluída")
    
    # 5. Gerar relatório
    print("\n5️⃣  Gerando relatório...")
    report = engine.generate_justification_report(reservoir_data, scores)
    print("✅ Relatório gerado")
    
    # 6. Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DA ANÁLISE")
    print("="*60)
    
    print("\n🏆 Top 3 Métodos Recomendados:")
    for i, (method, data) in enumerate(recommendations, 1):
        print(f"{i}. {method}: {data['score']:.1f}% ({data['status']})")
    
    print(f"\n💰 Resultados Econômicos:")
    print(f"   NPV: ${npv:,.0f}")
    print(f"   IRR: {irr:.2f}%")
    if payback:
        print(f"   Payback: {payback:.1f} anos")
    else:
        print(f"   Payback: Não alcançado")
    
    return {
        'scores': scores,
        'recommendations': recommendations,
        'economic': {
            'NPV': npv,
            'IRR': irr,
            'Payback': payback,
            'CashFlow': cf_data['cash_flow']
        },
        'report': report,
        'figures': [fig1, fig2]
    }


# Usar a função
if __name__ == "__main__":
    # Dados de exemplo
    reservoir = {
        'API': 28,
        'Viscosidade': 45,
        'Profundidade': 1200,
        'Permeabilidade': 200,
        'Porosidade': 18,
        'Saturação de Óleo': 65,
        'Saturação de Água': 35,
        'Temperatura': 75,
        'Pressão': 1500,
        'Salinidade': 45000,
        'Espessura': 25,
        'TAN': 0.8,
        'pH': 7.2,
        'Dip': 12
    }
    
    economics = {
        'oil_price': 75,
        'discount_rate': 12,
        'tax_rate': 25,
        'project_life': 15,
        'decline_rate': 10,
        'production_rate': 3000
    }
    
    # Executar análise
    results = analyze_reservoir(reservoir, economics)
    
    # Exibir gráficos
    if results:
        plt.show()
```

---

## 🎯 Exemplos Específicos por Método

### **Cenário 1: Óleo Pesado - Vapor**

```python
heavy_oil = {
    'API': 15,              # Óleo muito pesado
    'Viscosidade': 2000,    # Muito viscoso
    'Profundidade': 800,    # Profundidade ideal
    'Temperatura': 40,      # Ambiente
    'Saturação de Óleo': 70
}

engine = EORScreeningEngine()
scores = engine.score_reservoir(heavy_oil)

print(f"Injeção de Vapor: {scores['Injeção de Vapor']['score']:.1f}%")
# Esperado: ~90% (Ideal para vapor)
```

### **Cenário 2: Óleo Leve - CO2**

```python
light_oil = {
    'API': 35,              # Óleo leve
    'Viscosidade': 3,       # Pouco viscoso
    'Profundidade': 2000,   # Profundo
    'Pressão': 2500,        # Alta pressão
    'Temperature': 90
}

engine = EORScreeningEngine()
scores = engine.score_reservoir(light_oil)

print(f"CO2 Miscível: {scores['Injeção de CO2 Miscível']['score']:.1f}%")
# Esperado: ~85% (Ideal para CO2)
```

---

## 📚 Referências de Documentação

- Ver **GUIA_DE_USO.md** para interface gráfica
- Ver **MELHORIAS_IMPLEMENTADAS.md** para detalhes técnicos
- Ver **SUMÁRIO_DE_MELHORIAS.md** para overview

---

**Exemplos criados com v6.1 - Sistema melhorado de PetroChamp**
