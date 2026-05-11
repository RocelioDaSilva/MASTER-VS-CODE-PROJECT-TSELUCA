# 🚀 GUIA DE INÍCIO RÁPIDO - PetroChamp v2.0

## Estrutura Implementada

A nova plataforma foi completamente refatorada em **arquitetura modular** no diretório:

```
📁 petrochamp_v2/
```

---

## 📦 Instalação

```bash
# 1. Navegar para o diretório
cd petrochamp_v2

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar instalação
python -c "import petrochamp_v2; print('✓ Pronto!')"
```

---

## ⚡ Uso Básico (5 Linhas)

```python
from petrochamp_v2 import PluginManager, ProjectManager, ReservoirData

pm = PluginManager()
project_mgr = ProjectManager()
project = project_mgr.create_project("Meu Projeto")
project.reservoir_data = ReservoirData(api_gravity=25, viscosity=500, depth=1200)
top_methods = pm.get_top_methods(project.reservoir_data.to_dict(), n=3)

for method, score in top_methods:
    print(f"{method}: {score:.1f}%")
```

---

## 📚 Exemplos Completos

Execute o exemplo abrangente:

```bash
python example_complete.py
```

Demonstra:
1. ✅ Configuração centralizada
2. ✅ Gerenciamento de projetos
3. ✅ Sistema de plugins
4. ✅ Triagem de métodos
5. ✅ Análise econômica
6. ✅ Sensibilidade
7. ✅ Cache
8. ✅ Recomendações inteligentes
9. ✅ Exportação/importação

---

## 🎯 Principais Recursos

### 1. Triagem Rápida
```python
from petrochamp_v2 import PluginManager

pm = PluginManager()
scores = pm.calculate_all_suitability_scores({
    'api_gravity': 20,
    'viscosity': 500,
    'depth': 1200
})

for method, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{method}: {score:.1f}%")
```

### 2. Gerenciamento de Projetos
```python
from petrochamp_v2 import ProjectManager

mgr = ProjectManager("./projetos")
project = mgr.create_project("Projeto X")
mgr.save_project(project, auto_backup=True)

projects = mgr.list_projects()
stats = mgr.get_statistics()
```

### 3. Análise de Sensibilidade
```python
from petrochamp_v2 import SensitivityAnalyzer

analyzer = SensitivityAnalyzer()

# One-At-a-Time
oat = analyzer.analyze_one_at_a_time(
    base_case={'api': 25, 'visc': 500},
    parameter_ranges={'api': (10, 40), 'visc': (100, 2000)},
    objective_function=npv_function,
    steps=10
)

# Monte Carlo
mc = analyzer.monte_carlo_simulation(
    base_case={...},
    parameter_distributions={...},
    objective_function=npv_function,
    n_iterations=1000
)

print(f"P10: ${mc['p10']:.0f}M")
print(f"P90: ${mc['p90']:.0f}M")
```

### 4. Otimização Híbrida
```python
from petrochamp_v2 import HybridEOROptimizer

optimizer = HybridEOROptimizer(plugin_manager)
optimal = optimizer.find_optimal_combination(
    reservoir_data=data,
    economic_params={'num_wells': 10},
    constraints={}
)

print(f"Melhor: {optimal['best_combination']}")
print(f"Score: {optimal['best_score']:.1f}")
```

### 5. Recomendações Inteligentes
```python
from petrochamp_v2 import IntelligentRecommender

recommender = IntelligentRecommender(plugin_mgr, project_mgr)
recs = recommender.recommend(
    current_reservoir=reservoir_dict,
    similarity_threshold=0.7
)

for rec in recs[:3]:
    print(f"{rec['method']}: {rec['confidence']*100:.0f}% confiança")
```

---

## 📁 Estrutura de Arquivos

```
petrochamp_v2/
├── __init__.py                 # Imports principais
├── README.md                   # Documentação detalhada
├── IMPLEMENTATION_GUIDE.md     # Guia de implementação
├── EXECUTIVE_SUMMARY.md        # Resumo executivo
├── requirements.txt            # Dependências
├── example_complete.py         # Exemplo abrangente
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuração centralizada (1000+ linhas)
│
├── core/
│   ├── __init__.py
│   ├── models.py              # Modelos de dados (800+ linhas)
│   ├── plugins.py             # Sistema de plugins (900+ linhas)
│   └── analysis.py            # Análise avançada (1200+ linhas)
│
├── data/
│   ├── __init__.py
│   └── persistence.py         # Gerenciamento de projetos (1000+ linhas)
│
├── ui/
│   └── __init__.py            # (Interface futura)
│
└── visualization/
    └── __init__.py            # (Gráficos futuros)
```

---

## 💾 Salvando e Carregando Projetos

```python
from petrochamp_v2 import ProjectManager

mgr = ProjectManager()

# Criar e salvar
project = mgr.create_project("Novo Projeto")
mgr.save_project(project)

# Carregar
project = mgr.open_project(project.id)

# Listar
projects = mgr.list_projects()

# Exportar
mgr.export_project(project.id, "projeto.json", include_results=True)

# Importar
imported = mgr.import_project("projeto.json")

# Backup/Restore
restored = mgr.restore_from_backup(project.id, "20240120_143022")
```

---

## 🔌 Criando Novo Plugin

```python
from petrochamp_v2 import EORMethodPlugin, EORMethodMetadata

class MeuMethodoPlugin(EORMethodPlugin):
    def get_metadata(self):
        return EORMethodMetadata(
            name="Meu Método",
            type=EORMethodType.THERMAL,
            description="...",
            developed_year=2024,
            maturity_level="Emerging",
            applicable_api_range=(20, 35),
            applicable_viscosity_range=(100, 1000),
            typical_recovery_increase=0.25,
            typical_capex_per_well=2.0,
            typical_opex_annual=0.5
        )
    
    def get_screening_criteria(self):
        return {
            'API': {'min': 20, 'max': 35, 'weight': 0.3},
            'Viscosity': {'min': 100, 'max': 1000, 'weight': 0.3},
            # ...
        }
    
    def calculate_suitability(self, reservoir_data):
        # Sua lógica aqui
        return score  # 0-100
    
    def get_justification(self, score, reservoir_data):
        return f"Justificativa customizada"
    
    def get_critical_parameters(self, reservoir_data):
        return ['API', 'Viscosity', 'Depth']
    
    def estimate_recovery_factor(self, reservoir_data, operational_params):
        return 0.25  # 25%
    
    def get_economic_parameters(self):
        return {
            'capex_per_well': 2.0e6,
            'opex_annual': 0.5e6,
            # ...
        }
    
    def get_implementation_roadmap(self):
        return {
            'phase_1': {'name': 'Piloto', 'duration_months': 12},
            # ...
        }

# Registrar
from petrochamp_v2 import PluginManager

pm = PluginManager()
pm.register_plugin(MeuMethodoPlugin())
```

---

## 🎓 Casos de Uso Avançados

### Triagem com Histórico
```python
recommender = IntelligentRecommender(plugin_mgr, project_mgr)
recs = recommender.recommend(reservoir_data)
# Retorna métodos com taxa de sucesso em casos similares
```

### Análise Completa
```python
# Obter todos os métodos
methods = pm.get_available_methods()

# Para cada método, calcular:
# 1. Suitability
# 2. Recuperação estimada
# 3. Análise econômica
# 4. Sensibilidade
# 5. Combinações híbridas

for method in methods:
    plugin = pm.get_plugin(method)
    score = plugin.calculate_suitability(reservoir_data)
    recovery = plugin.estimate_recovery_factor(reservoir_data, {})
    econ = plugin.get_economic_parameters()
```

### Monitorar Performance
```python
cache = ResultsCache()
stats = cache.get_statistics()
print(f"Taxa de acerto: {stats['hit_rate']:.1f}%")
print(f"Cache size: {stats['size']}/{stats['max_size']}")
```

---

## 📊 Configurações Predefinidas

```python
from petrochamp_v2 import DEVELOPMENT_CONFIG, PRODUCTION_CONFIG, LIGHTWEIGHT_CONFIG

# Desenvolvimento (debug ativado, menos iterações)
config = DEVELOPMENT_CONFIG

# Produção (otimizado, mais iterações)
config = PRODUCTION_CONFIG

# Lightweight (mínimo de recursos)
config = LIGHTWEIGHT_CONFIG
```

---

## 🔒 Backup e Segurança

```python
# Auto-backup automático
mgr.save_project(project, auto_backup=True)

# Listar backups
backups = Path("./projects/backups").glob("*.json")

# Restaurar
restored = mgr.restore_from_backup(project_id, timestamp)

# Exportar para segurança
mgr.export_project(project_id, "backup.pkl")
```

---

## 🐛 Debugging

```python
# Ativar debug mode
config = DEVELOPMENT_CONFIG  # debug_mode=True

# Logs em arquivo
# Verificar: petrochamp.log

# Importância
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

---

## 📈 Próximas Fases

### Fase 1: Interface Gráfica
- `ui/main_window.py` - Janela principal
- Gerenciamento de projetos
- Entrada de dados
- Visualização de resultados

### Fase 2: API REST
- Flask endpoints
- Autenticação JWT
- Rate limiting
- Documentação OpenAPI

### Fase 3: Banco de Dados
- SQLAlchemy models
- Persistência em BD
- Queries otimizadas

### Fase 4: Dashboard Web
- React/Vue frontend
- Gráficos interativos
- Exportação de relatórios

---

## 🆘 Suporte

**Documentação:**
- `README.md` - Visão geral
- `IMPLEMENTATION_GUIDE.md` - Detalhadoguia de integração
- `EXECUTIVE_SUMMARY.md` - Resumo excelado
- `example_complete.py` - Exemplos práticos

**Logs:**
- Verificar `petrochamp.log` para erros
- Ativar debug mode se necessário

**Plugins:**
- Seguir padrão de `SteamInjectionPlugin`
- Registrar em `PluginManager`

---

## ✅ Checklist Rápido

- [ ] Instalar dependências (`pip install -r requirements.txt`)
- [ ] Executar exemplo (`python example_complete.py`)
- [ ] Explorar módulos (`import petrochamp_v2`)
- [ ] Criar primeiro projeto
- [ ] Executar triagem
- [ ] Análise de sensibilidade
- [ ] Recomendações inteligentes
- [ ] Exportar resultados

---

## 🎉 Conclusão

Você agora tem uma **plataforma profissional e modular** para triagem e otimização de métodos EOR com:

✅ **Arquitetura sólida** - Modular, extensível, desacoplada  
✅ **Código de alta qualidade** - 100% type hints, logging completo  
✅ **Funcionalidades avançadas** - Análise, otimização, recomendações  
✅ **Fácil de usar** - API intuitiva, exemplos práticos  
✅ **Bem documentada** - README, exemplos, docstrings  

---

**Próximo passo:** Implementar interface gráfica em `ui/main_window.py`

*Happy coding! 🚀*
