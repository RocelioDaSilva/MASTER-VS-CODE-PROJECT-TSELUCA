# 🚀 PetroChamp Advanced v2.0 - Arquitetura Modular

## 📋 Visão Geral

PetroChamp Advanced é uma plataforma de última geração para triagem e otimização de métodos Enhanced Oil Recovery (EOR). Apresenta arquitetura modular, sistema de plugins extensível, análise avançada e persistência robusta.

### ✨ Características Principais

- ✅ **Arquitetura Modular** - Separação de responsabilidades
- ✅ **Sistema de Plugins** - Adicione novos métodos EOR facilmente
- ✅ **Cache Inteligente** - Otimização de performance
- ✅ **Gerenciamento de Projetos** - Persistência com backup
- ✅ **Análise Avançada** - Sensibilidade, otimização, recomendações
- ✅ **Configuração Centralizada** - Ambiente-específico
- ✅ **Relatórios** - Múltiplos formatos

---

## 📁 Estrutura de Diretórios

```
petrochamp_v2/
├── config/
│   └── settings.py                 # Configuração centralizada
├── core/
│   ├── models.py                   # Modelos de dados (EORProject, etc)
│   ├── plugins.py                  # Sistema de plugins EOR
│   ├── analysis.py                 # Análise avançada
│   └── engine.py                   # Motor de triagem (a implementar)
├── ui/
│   ├── main_window.py              # Janela principal (a implementar)
│   └── widgets/                    # Componentes customizados (a implementar)
├── visualization/
│   └── charts.py                   # Gráficos e dashboards (a implementar)
├── data/
│   ├── persistence.py              # Gerenciamento de projetos
│   └── connectors.py               # Conectores de BD (a implementar)
└── main.py                         # Ponto de entrada (a implementar)
```

---

## 🔧 Módulos Principais

### 1. **config/settings.py**

Configuração centralizada com suporte a múltiplos ambientes.

```python
# Uso básico
from config.settings import get_config, load_config

config = get_config()
print(config.performance['max_cache_size'])

# Carregar de arquivo
config = load_config('config.json')

# Uso de presets
from config.settings import PRODUCTION_CONFIG, DEVELOPMENT_CONFIG
```

**Configurações Disponíveis:**
- `PerformanceConfig` - Cache, workers, intervals
- `VisualizationConfig` - Temas, qualidade de gráficos
- `AnalysisConfig` - Iterações, confiança, thresholds
- `PersistenceConfig` - Auto-save, backups
- `APIConfig` - Integração com serviços externos

---

### 2. **core/models.py**

Modelos de dados com persistência em JSON.

```python
from core.models import EORProject, ReservoirData, ScreeningResult

# Criar projeto
project = EORProject(name="Reservatório X")

# Adicionar dados
project.reservoir_data = ReservoirData(
    api_gravity=25,
    viscosity=500,
    depth=1000,
    # ...
)

# Salvar
project.save_to_file("projetos/projeto1.json")

# Carregar
project = EORProject.load_from_file("projetos/projeto1.json")
```

**Tipos de Dados:**
- `ReservoirData` - Parâmetros do reservatório
- `ScreeningResult` - Resultado de triagem
- `EconomicAnalysis` - Análise econômica
- `SensitivityAnalysisResult` - Resultado de sensibilidade
- `EORProject` - Projeto completo

---

### 3. **core/plugins.py**

Sistema de plugins extensível para métodos EOR.

```python
from core.plugins import PluginManager

# Inicializar
pm = PluginManager()

# Listar métodos disponíveis
methods = pm.get_available_methods()
print(methods)  # ['Injeção de Vapor', 'Injeção de CO2 Miscível', ...]

# Obter plugin
plugin = pm.get_plugin('Injeção de Vapor')

# Calcular suitability
reservoir = {'api_gravity': 20, 'viscosity': 500, ...}
score = plugin.calculate_suitability(reservoir)

# Top métodos para reservatório
top_3 = pm.get_top_methods(reservoir, n=3)
```

**Criar Novo Plugin:**

```python
from core.plugins import EORMethodPlugin, EORMethodMetadata

class MeuMethodoPlugin(EORMethodPlugin):
    def get_metadata(self):
        return EORMethodMetadata(
            name="Meu Método",
            # ...
        )
    
    def get_screening_criteria(self):
        return {...}
    
    def calculate_suitability(self, reservoir_data):
        # Implementar lógica
        return score
    
    # ... implementar outros métodos

# Registrar
pm.register_plugin(MeuMethodoPlugin())
```

---

### 4. **data/persistence.py**

Gerenciamento robusto de projetos com cache.

```python
from data.persistence import ProjectManager, ResultsCache

# Gerenciador de projetos
pm = ProjectManager(storage_path="./projects")

# Criar projeto
project = pm.create_project("Novo Projeto")

# Listar projetos
projects = pm.list_projects()

# Salvar
pm.save_project(project, auto_backup=True)

# Carregar
project = pm.open_project(project.id)

# Estatísticas
stats = pm.get_statistics()
print(f"Projetos totais: {stats.total_projects}")
print(f"Score médio: {stats.avg_best_score:.1f}%")

# Cache de resultados
cache = ResultsCache(max_size=1000, ttl_seconds=3600)

def expensive_calculation(data):
    # Lógica complexa
    return result

# Usar cache
result = cache.get('minha_chave', expensive_calculation, data)

# Estatísticas do cache
stats = cache.get_statistics()
print(f"Taxa de acerto: {stats['hit_rate']:.1f}%")
```

---

### 5. **core/analysis.py**

Análise avançada multivariada.

```python
from core.analysis import SensitivityAnalyzer, HybridEOROptimizer, IntelligentRecommender

# Análise de Sensibilidade
analyzer = SensitivityAnalyzer()

# One-At-a-Time
results_oat = analyzer.analyze_one_at_a_time(
    base_case={'api_gravity': 25, 'viscosity': 500},
    parameter_ranges={
        'api_gravity': (10, 40),
        'viscosity': (100, 5000)
    },
    objective_function=my_npv_function,
    steps=20
)

# Tornado
df_tornado, fig_tornado = analyzer.tornado_analysis(
    base_case={...},
    variations={'api_gravity': (15, 35), 'viscosity': (200, 2000)},
    objective_function=my_npv_function
)

# Monte Carlo
mc_results = analyzer.monte_carlo_simulation(
    base_case={...},
    parameter_distributions={
        'oil_price': {'type': 'normal', 'mean': 75, 'std': 10},
        'capex': {'type': 'lognormal', 'mean': 10, 'std': 2}
    },
    objective_function=my_npv_function,
    n_iterations=1000
)

print(f"NPV P10: ${mc_results['p10']:.0f}M")
print(f"NPV P90: ${mc_results['p90']:.0f}M")

# Otimização Híbrida
optimizer = HybridEOROptimizer(plugin_manager)

optimal = optimizer.find_optimal_combination(
    reservoir_data=project.reservoir_data.to_dict(),
    economic_params={'num_wells': 10, 'budget': 100e6},
    constraints={'min_suitability': 0.6}
)

print(f"Melhor combinação: {optimal['best_combination']}")
print(f"Score: {optimal['best_score']:.1f}")

# Recomendações Inteligentes
recommender = IntelligentRecommender(plugin_manager, project_manager)

recommendations = recommender.recommend(
    current_reservoir=project.reservoir_data.to_dict(),
    similarity_threshold=0.7
)

for rec in recommendations:
    print(f"{rec['method']}: {rec['confidence']*100:.0f}% confiança")
    print(f"  Razão: {rec['recommendation_reason']}")
```

---

## 🚀 Guia de Início Rápido

### Instalação

```bash
cd petrochamp_v2
pip install -r requirements.txt
```

**Dependências (requirements.txt):**
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
openpyxl>=3.6.0
```

### Exemplo Básico

```python
#!/usr/bin/env python3
"""
Exemplo de uso da plataforma PetroChamp Advanced
"""

from config.settings import get_config, DEVELOPMENT_CONFIG
from core.models import EORProject, ReservoirData
from core.plugins import PluginManager
from data.persistence import ProjectManager, ResultsCache
from core.analysis import SensitivityAnalyzer, HybridEOROptimizer, IntelligentRecommender

# 1. Configurar
config = DEVELOPMENT_CONFIG
print(f"Modo debug: {config.debug_mode}")
print(f"Passos de sensibilidade: {config.analysis['sensitivity_steps']}")

# 2. Criar projeto
project_mgr = ProjectManager("./projects")
project = project_mgr.create_project("Projeto Piloto")

# 3. Adicionar dados do reservatório
project.reservoir_data = ReservoirData(
    api_gravity=20,
    viscosity=500,
    depth=1200,
    thickness=25,
    permeability=100,
    porosity=22,
    temperature=65,
    pressure=250,
    salinity=50000,
    oil_saturation=60,
    field_name="Campo Exemplo"
)

# 4. Realizar triagem
plugin_mgr = PluginManager()
scores = plugin_mgr.calculate_all_suitability_scores(
    project.reservoir_data.to_dict()
)

print("\n=== Resultados de Triagem ===")
for method, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{method}: {score:.1f}%")

# 5. Análise de Sensibilidade
analyzer = SensitivityAnalyzer()
def dummy_npv(data):
    # Função objetivo simplificada
    return data.get('api_gravity', 25) * 1e6

oat_results = analyzer.analyze_one_at_a_time(
    base_case=project.reservoir_data.to_dict(),
    parameter_ranges={'api_gravity': (10, 40)},
    objective_function=dummy_npv,
    steps=5
)

print("\n=== Sensibilidade ===")
print(oat_results)

# 6. Recomendações Inteligentes
recommender = IntelligentRecommender(plugin_mgr, project_mgr)
recs = recommender.recommend(project.reservoir_data.to_dict())

print("\n=== Recomendações ===")
for rec in recs[:3]:
    print(f"{rec['method']}: {rec['confidence']*100:.0f}% confiança")

# 7. Salvar projeto
project_mgr.save_project(project)
print("\nProjeto salvo!")

# 8. Estatísticas
stats = project_mgr.get_statistics()
print(f"\nProjetos no histórico: {stats.total_projects}")
```

**Executar:**
```bash
python example_basic.py
```

---

## 📊 Casos de Uso

### Caso 1: Triagem Rápida

```python
# Análise rápida sem persistência
plugin_mgr = PluginManager()
top_methods = plugin_mgr.get_top_methods(
    {'api_gravity': 25, 'viscosity': 500},
    n=3
)
for method, score in top_methods:
    print(f"{method}: {score:.1f}%")
```

### Caso 2: Análise Completa

```python
# Análise detalhada com todos os componentes
project_mgr = ProjectManager()
plugin_mgr = PluginManager()
analyzer = SensitivityAnalyzer()
optimizer = HybridEOROptimizer(plugin_mgr)
recommender = IntelligentRecommender(plugin_mgr, project_mgr)

# ... executar análises
```

### Caso 3: Integração em Sistema Existente

```python
# Usar apenas o PluginManager em código existente
plugin_mgr = PluginManager()
plugin_mgr.register_plugin(SeuMethodoCustomizado())

# Adicionar um novo método EOR sem modificar código existente
```

---

## 🔌 Estendendo com Plugins

Cada método EOR é um plugin que implementa `EORMethodPlugin`:

```python
class SeuMethodoPlugin(EORMethodPlugin):
    def get_metadata(self):
        """Informações sobre o método"""
        
    def get_screening_criteria(self):
        """Critérios de aplicabilidade"""
        
    def calculate_suitability(self, reservoir_data):
        """Lógica de pontuação"""
        
    def get_justification(self, score, reservoir_data):
        """Explicação textual"""
        
    def get_critical_parameters(self, reservoir_data):
        """Parâmetros-chave"""
        
    def estimate_recovery_factor(self, reservoir_data, operational_params):
        """Estimativa de recuperação"""
        
    def get_economic_parameters(self):
        """Parâmetros econômicos"""
        
    def get_implementation_roadmap(self):
        """Plano de implementação"""
```

---

## 💾 Persistência e Backup

**Salvamento Automático:**
```python
project_mgr = ProjectManager()
project = project_mgr.create_project("Projeto X")

# Auto-save a cada 5 minutos
project_mgr.save_project(project, auto_backup=True)
```

**Restauração de Backup:**
```python
project = project_mgr.restore_from_backup(
    project_id="...",
    backup_timestamp="20240120_143022"
)
```

---

## 🎯 Próximas Fases

- [ ] Implementar `engine.py` - Motor de cálculo econômico
- [ ] Implementar `ui/main_window.py` - Interface gráfica
- [ ] Implementar `visualization/charts.py` - Gráficos avançados
- [ ] Implementar `data/connectors.py` - Integração com BD
- [ ] Criar API REST com Flask
- [ ] Adicionar mais plugins EOR
- [ ] Implementar dashboard em tempo real

---

## 📝 Documentação Adicional

- Ver `config/settings.py` para todas as opções de configuração
- Ver `core/plugins.py` para exemplos de plugins
- Ver `data/persistence.py` para gerenciamento de projetos
- Ver `core/analysis.py` para análise avançada

---

**Versão:** 2.0  
**Última atualização:** Janeiro 20, 2026  
**Status:** 🟢 Arquitetura Core Completa
