"""
📑 ÍNDICE DE MÓDULOS - PetroChamp v2.0

Referência rápida para todos os módulos, classes e funções principais.
"""

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 1: CONFIG/SETTINGS.PY
# ═══════════════════════════════════════════════════════════════════════════

MODULE_1 = {
    "name": "petrochamp_v2.config.settings",
    "purpose": "Configuração centralizada do sistema",
    "key_classes": {
        "AppConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração master com todos os settings",
            "atributos": [
                "max_cache_size",
                "performance: PerformanceConfig",
                "visualization: VisualizationConfig",
                "analysis: AnalysisConfig",
                "persistence: PersistenceConfig",
                "api: APIConfig",
            ],
            "métodos_principais": [
                "from_file(path) -> AppConfig",
                "save(path) -> None",
                "validate() -> bool",
            ],
        },
        "PerformanceConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração de cache e performance",
            "atributos": [
                "cache_ttl_seconds: int",
                "max_cache_size: int",
                "n_workers: int",
            ],
        },
        "VisualizationConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração de visualização",
            "atributos": [
                "style: str",
                "dpi: int",
                "figure_size: tuple",
            ],
        },
        "AnalysisConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração de análise",
            "atributos": [
                "oat_steps: int",
                "mc_iterations: int",
                "optimization_methods: list",
            ],
        },
        "PersistenceConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração de persistência",
            "atributos": [
                "base_dir: str",
                "projects_dir: str",
                "auto_backup: bool",
                "backup_interval_hours: int",
            ],
        },
        "APIConfig": {
            "tipo": "dataclass",
            "descrição": "Configuração de API",
            "atributos": [
                "host: str",
                "port: int",
                "debug: bool",
                "api_version: str",
            ],
        },
    },
    "constantes_globais": {
        "DEVELOPMENT_CONFIG": "Configuração para desenvolvimento",
        "PRODUCTION_CONFIG": "Configuração para produção",
        "LIGHTWEIGHT_CONFIG": "Configuração minimalista",
    },
    "funções_globais": [
        "get_config() -> AppConfig",
        "load_config(path: str) -> None",
        "set_config(config: AppConfig) -> None",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 2: CORE/MODELS.PY
# ═══════════════════════════════════════════════════════════════════════════

MODULE_2 = {
    "name": "petrochamp_v2.core.models",
    "purpose": "Modelos de dados com serialização",
    "key_classes": {
        "ReservoirData": {
            "tipo": "dataclass",
            "descrição": "Parâmetros do reservatório",
            "atributos": [
                "api_gravity: float",
                "viscosity: float",
                "depth: float",
                "porosity: float",
                "permeability: float",
                "temperature: float",
                "saturation_oil: float",
                "saturation_water: float",
                "net_to_gross: float",
                "formation: str",
                "created_at: datetime",
            ],
            "métodos": [
                "to_dict() -> dict",
                "from_dict(d: dict) -> ReservoirData",
                "to_json() -> str",
                "from_json(s: str) -> ReservoirData",
            ],
        },
        "EORProject": {
            "tipo": "dataclass",
            "descrição": "Projeto EOR principal",
            "atributos": [
                "id: str",
                "name: str",
                "location: str",
                "reservoir_data: ReservoirData",
                "screening_result: Optional[ScreeningResult]",
                "created_at: datetime",
                "updated_at: datetime",
            ],
            "métodos": [
                "to_dict() -> dict",
                "from_dict(d: dict) -> EORProject",
                "save_to_file(path: str) -> None",
                "load_from_file(path: str) -> EORProject",
            ],
        },
        "ScreeningResult": {
            "tipo": "dataclass",
            "descrição": "Resultado de triagem",
            "atributos": [
                "method_name: str",
                "suitability_score: float",
                "screening_criteria: dict",
                "timestamp: datetime",
                "calculation_time: float",
            ],
        },
        "EconomicAnalysis": {
            "tipo": "dataclass",
            "descrição": "Análise econômica",
            "atributos": [
                "npv: float",
                "irr: float",
                "payback_period: float",
                "capex: float",
                "opex: float",
                "revenue: float",
            ],
        },
        "SensitivityAnalysisResult": {
            "tipo": "dataclass",
            "descrição": "Resultado de análise de sensibilidade",
            "atributos": [
                "parameter_name: str",
                "base_value: float",
                "sensitivity_values: dict",
                "tornado_data: dict",
            ],
        },
    },
    "enums": {
        "ReservoirType": ["SANDSTONE", "LIMESTONE", "SHALE", "FRACTURED_ROCK"],
        "EORMethodType": ["THERMAL", "CHEMICAL", "GAS_INJECTION", "MISCIBLE"],
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 3: CORE/PLUGINS.PY
# ═══════════════════════════════════════════════════════════════════════════

MODULE_3 = {
    "name": "petrochamp_v2.core.plugins",
    "purpose": "Sistema de plugins para métodos EOR",
    "key_classes": {
        "EORMethodPlugin": {
            "tipo": "ABC",
            "descrição": "Classe abstrata para plugins EOR",
            "métodos_abstratos": [
                "get_metadata() -> EORMethodMetadata",
                "get_screening_criteria() -> dict",
                "calculate_suitability(reservoir_data: dict) -> float",
                "get_justification(score: float, reservoir_data: dict) -> str",
                "get_critical_parameters(reservoir_data: dict) -> list",
                "estimate_recovery_factor(reservoir_data: dict, params: dict) -> float",
                "get_economic_parameters() -> dict",
                "get_implementation_roadmap() -> dict",
            ],
        },
        "EORMethodMetadata": {
            "tipo": "dataclass",
            "descrição": "Metadados de um método EOR",
            "atributos": [
                "name: str",
                "type: EORMethodType",
                "description: str",
                "developed_year: int",
                "maturity_level: str",
                "applicable_api_range: tuple",
                "applicable_viscosity_range: tuple",
                "typical_recovery_increase: float",
                "typical_capex_per_well: float",
                "typical_opex_annual: float",
            ],
        },
        "PluginManager": {
            "tipo": "class",
            "descrição": "Gerenciador de plugins",
            "métodos_principais": [
                "register_plugin(plugin: EORMethodPlugin) -> None",
                "get_plugin(method_name: str) -> EORMethodPlugin",
                "get_available_methods() -> list",
                "calculate_all_suitability_scores(reservoir_data: dict) -> dict",
                "get_top_methods(reservoir_data: dict, n: int) -> list",
            ],
        },
        "SteamInjectionPlugin": {
            "tipo": "EORMethodPlugin",
            "descrição": "Implementação de Injeção de Vapor",
            "nota": "Exemplo completo - seguir este padrão para novos plugins",
        },
        "CO2MisciblePlugin": {
            "tipo": "EORMethodPlugin",
            "descrição": "Implementação de Injeção de CO2 Miscível",
            "nota": "Exemplo completo - seguir este padrão para novos plugins",
        },
    },
    "extensibilidade": [
        "Combustão In Situ",
        "Injeção de Polímeros",
        "Injeção de Surfactantes",
        "Injeção Alcalina",
        "Gás Não-Miscível",
        "Nitrogênio",
        "Aquecimento Eletromagnético",
        "Injeção de Solventes",
        "Drenagem por Gravidade",
        "Oxidação In Situ",
        "Vibração Acústica",
        "Injeção de Microemulsões",
        "Métodos Híbridos",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 4: CORE/ANALYSIS.PY
# ═══════════════════════════════════════════════════════════════════════════

MODULE_4 = {
    "name": "petrochamp_v2.core.analysis",
    "purpose": "Análise avançada multivariável",
    "key_classes": {
        "SensitivityMetric": {
            "tipo": "dataclass",
            "descrição": "Métrica de sensibilidade",
            "atributos": [
                "parameter_name: str",
                "base_value: float",
                "sensitivity_coefficient: float",
                "elasticity: float",
            ],
        },
        "SensitivityAnalyzer": {
            "tipo": "class",
            "descrição": "Análise de sensibilidade",
            "métodos": [
                "analyze_one_at_a_time(base_case, parameter_ranges, objective_function, steps)",
                "tornado_analysis(base_case, parameter_ranges, objective_function)",
                "monte_carlo_simulation(base_case, parameter_distributions, objective_function, n_iterations)",
            ],
            "retorno": "DataFrame com resultados + matplotlib Figure",
        },
        "HybridEOROptimizer": {
            "tipo": "class",
            "descrição": "Otimização de combinações EOR",
            "métodos": [
                "find_optimal_combination(reservoir_data, economic_params, constraints)",
            ],
            "features": [
                "Geração de combinações",
                "Validação de constraints",
                "Cálculo de sinergias",
                "Ranking de combinações",
            ],
        },
        "IntelligentRecommender": {
            "tipo": "class",
            "descrição": "Recomendador baseado em IA",
            "métodos": [
                "recommend(current_reservoir, similarity_threshold, top_n)",
            ],
            "features": [
                "Busca de casos similares",
                "Cálculo de similaridade",
                "Taxa de sucesso histórica",
                "Justificativa customizada",
            ],
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULO 5: DATA/PERSISTENCE.PY
# ═══════════════════════════════════════════════════════════════════════════

MODULE_5 = {
    "name": "petrochamp_v2.data.persistence",
    "purpose": "Gerenciamento de cache e projetos",
    "key_classes": {
        "ResultsCache": {
            "tipo": "class",
            "descrição": "Cache inteligente com LRU e TTL",
            "parâmetros": [
                "max_size: int (default 1000)",
                "ttl_seconds: int (default 300)",
            ],
            "métodos": [
                "put(key: str, value: Any) -> None",
                "get(key: str) -> Optional[Any]",
                "clear() -> None",
                "get_statistics() -> dict",
            ],
            "features": [
                "LRU eviction",
                "Time-to-live (TTL)",
                "Hit/Miss statistics",
                "Sincronização automática",
            ],
        },
        "ProjectManager": {
            "tipo": "class",
            "descrição": "Gerenciador de projetos",
            "métodos": [
                "create_project(name, location, reservoir_data) -> EORProject",
                "open_project(project_id) -> EORProject",
                "save_project(project, auto_backup=False) -> None",
                "delete_project(project_id) -> None",
                "list_projects() -> list",
                "get_statistics() -> dict",
                "export_project(project_id, path, format='json') -> None",
                "import_project(path) -> EORProject",
                "restore_from_backup(project_id, timestamp) -> EORProject",
            ],
            "features": [
                "CRUD completo",
                "Backup automático",
                "Restore automático",
                "Export (JSON, PKL)",
                "Import seguro",
                "Índice de projetos",
            ],
        },
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# MAPA DE DEPENDÊNCIAS
# ═══════════════════════════════════════════════════════════════════════════

DEPENDENCY_MAP = {
    "config/settings.py": {
        "importa": ["json", "dataclasses", "logging"],
        "é importado por": ["Todos os outros módulos"],
        "dependências externas": ["json", "os"],
    },
    "core/models.py": {
        "importa": ["config", "dataclasses", "datetime"],
        "é importado por": ["plugins", "persistence", "analysis"],
        "dependências externas": ["dataclasses", "json"],
    },
    "core/plugins.py": {
        "importa": ["models", "abc", "enum"],
        "é importado por": ["analysis", "persistence"],
        "dependências externas": ["abc", "numpy", "scipy"],
    },
    "core/analysis.py": {
        "importa": ["models", "plugins", "numpy", "scipy", "pandas"],
        "é importado por": ["persistence"],
        "dependências externas": ["numpy", "scipy", "pandas", "matplotlib"],
    },
    "data/persistence.py": {
        "importa": ["models", "json", "pickle", "logging"],
        "é importado por": ["__init__"],
        "dependências externas": ["json", "pickle", "os", "shutil"],
    },
}

# ═══════════════════════════════════════════════════════════════════════════
# CLASSES PRINCIPAIS POR FUNCIONALIDADE
# ═══════════════════════════════════════════════════════════════════════════

CLASSES_BY_FUNCTIONALITY = {
    "Dados & Modelos": [
        "ReservoirData - Parâmetros do reservatório",
        "EORProject - Projeto completo",
        "ScreeningResult - Resultado de triagem",
        "EconomicAnalysis - Análise econômica",
    ],
    
    "Configuração": [
        "AppConfig - Configuração master",
        "PerformanceConfig - Performance settings",
        "VisualizationConfig - Visualization settings",
        "AnalysisConfig - Analysis settings",
    ],
    
    "Plugins": [
        "EORMethodPlugin - Interface abstrata",
        "PluginManager - Gerenciador de plugins",
        "SteamInjectionPlugin - Implementação exemplo",
        "CO2MisciblePlugin - Implementação exemplo",
    ],
    
    "Análise": [
        "SensitivityAnalyzer - Análise de sensibilidade",
        "HybridEOROptimizer - Otimização de combinações",
        "IntelligentRecommender - Recomendador IA",
    ],
    
    "Persistência": [
        "ResultsCache - Cache LRU+TTL",
        "ProjectManager - Gerenciamento de projetos",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS RECOMENDADOS
# ═══════════════════════════════════════════════════════════════════════════

RECOMMENDED_IMPORTS = {
    "Uso Básico": [
        "from petrochamp_v2 import PluginManager, ProjectManager, ReservoirData",
    ],
    
    "Análise Completa": [
        "from petrochamp_v2 import PluginManager, SensitivityAnalyzer, HybridEOROptimizer, IntelligentRecommender",
    ],
    
    "Gerenciamento": [
        "from petrochamp_v2 import ProjectManager, ResultsCache, EORProject",
    ],
    
    "Configuração": [
        "from petrochamp_v2 import AppConfig, DEVELOPMENT_CONFIG, PRODUCTION_CONFIG",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# EXEMPLOS RÁPIDOS
# ═══════════════════════════════════════════════════════════════════════════

QUICK_EXAMPLES = {
    "1. Criar Projeto": """
from petrochamp_v2 import ProjectManager, ReservoirData

mgr = ProjectManager()
reservoir = ReservoirData(api_gravity=25, viscosity=500, depth=1200)
project = mgr.create_project("Projeto X", "Campo Y", reservoir)
mgr.save_project(project)
    """,
    
    "2. Triagem Rápida": """
from petrochamp_v2 import PluginManager, ReservoirData

pm = PluginManager()
data = {'api_gravity': 25, 'viscosity': 500, 'depth': 1200}
scores = pm.calculate_all_suitability_scores(data)
top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    """,
    
    "3. Sensibilidade": """
from petrochamp_v2 import SensitivityAnalyzer

analyzer = SensitivityAnalyzer()
results = analyzer.monte_carlo_simulation(
    base_case={...},
    parameter_distributions={...},
    objective_function=npv_function,
    n_iterations=1000
)
print(f"P50: ${results['p50']:.0f}M")
    """,
    
    "4. Recomendações": """
from petrochamp_v2 import IntelligentRecommender

recommender = IntelligentRecommender(plugin_mgr, project_mgr)
recs = recommender.recommend(reservoir_dict, similarity_threshold=0.7)
for rec in recs[:3]:
    print(f"{rec['method']}: {rec['confidence']*100:.0f}%")
    """,
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO PARA EXIBIR ÍNDICE
# ═══════════════════════════════════════════════════════════════════════════

def print_module_index():
    """Exibe índice de módulos."""
    
    print("\n" + "="*80)
    print("📑 ÍNDICE DE MÓDULOS - PetroChamp v2.0")
    print("="*80)
    
    print("\n📦 MÓDULO 1: CONFIG/SETTINGS.PY")
    print(f"Propósito: {MODULE_1['purpose']}")
    print("Classes principais:")
    for cls_name in MODULE_1['key_classes'].keys():
        print(f"  • {cls_name}")
    
    print("\n📦 MÓDULO 2: CORE/MODELS.PY")
    print(f"Propósito: {MODULE_2['purpose']}")
    print("Classes principais:")
    for cls_name in MODULE_2['key_classes'].keys():
        print(f"  • {cls_name}")
    
    print("\n📦 MÓDULO 3: CORE/PLUGINS.PY")
    print(f"Propósito: {MODULE_3['purpose']}")
    print("Classes principais:")
    for cls_name in MODULE_3['key_classes'].keys():
        print(f"  • {cls_name}")
    
    print("\n📦 MÓDULO 4: CORE/ANALYSIS.PY")
    print(f"Propósito: {MODULE_4['purpose']}")
    print("Classes principais:")
    for cls_name in MODULE_4['key_classes'].keys():
        print(f"  • {cls_name}")
    
    print("\n📦 MÓDULO 5: DATA/PERSISTENCE.PY")
    print(f"Propósito: {MODULE_5['purpose']}")
    print("Classes principais:")
    for cls_name in MODULE_5['key_classes'].keys():
        print(f"  • {cls_name}")
    
    print("\n🔗 DEPENDÊNCIAS:")
    for module, deps in DEPENDENCY_MAP.items():
        print(f"\n{module}")
        print(f"  Importa: {', '.join(deps['importa'][:3])}...")
        print(f"  Importado por: {deps['é importado por'][0]}")
    
    print("\n📚 CLASSES POR FUNCIONALIDADE:")
    for func, classes in CLASSES_BY_FUNCTIONALITY.items():
        print(f"\n{func}:")
        for cls in classes:
            print(f"  • {cls}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    print_module_index()
