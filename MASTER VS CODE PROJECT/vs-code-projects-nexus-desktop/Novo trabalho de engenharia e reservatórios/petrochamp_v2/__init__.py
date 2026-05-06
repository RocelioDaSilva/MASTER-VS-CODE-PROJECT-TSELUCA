"""
PetroChamp Advanced v2.0 - Plataforma Modular para Triagem e Otimização EOR

Pacotes principais:
  - config: Configuração centralizada
  - core: Lógica principal (modelos, plugins, análise)
  - data: Persistência e gerenciamento de dados
  - ui: Interface de usuário (a implementar)
  - visualization: Gráficos e dashboards (a implementar)
"""

__version__ = "2.0.0"
__author__ = "PetroChamp Team"
__license__ = "MIT"

# Imports simplificados para fácil acesso
from .config.settings import (
    AppConfig,
    get_config,
    load_config,
    DEVELOPMENT_CONFIG,
    PRODUCTION_CONFIG,
    LIGHTWEIGHT_CONFIG
)

from .core.models import (
    EORProject,
    ReservoirData,
    ScreeningResult,
    EconomicAnalysis,
    SensitivityAnalysisResult,
    ProjectStatistics
)

from .core.plugins import (
    PluginManager,
    EORMethodPlugin,
    EORMethodMetadata,
    EORMethodType,
    SteamInjectionPlugin,
    CO2MisciblePlugin
)

from .data.persistence import (
    ProjectManager,
    ResultsCache
)

from .core.analysis import (
    SensitivityAnalyzer,
    HybridEOROptimizer,
    IntelligentRecommender,
    SensitivityMetric
)

from .core.dashboard import (
    RealtimeDashboard,
    DashboardMetrics,
    DashboardAlert
)

from .core.reporting import (
    AdvancedReportGenerator,
    ReportMetadata
)

__all__ = [
    # Configuration
    'AppConfig',
    'get_config',
    'load_config',
    'DEVELOPMENT_CONFIG',
    'PRODUCTION_CONFIG',
    'LIGHTWEIGHT_CONFIG',
    
    # Models
    'EORProject',
    'ReservoirData',
    'ScreeningResult',
    'EconomicAnalysis',
    'SensitivityAnalysisResult',
    'ProjectStatistics',
    
    # Plugins
    'PluginManager',
    'EORMethodPlugin',
    'EORMethodMetadata',
    'EORMethodType',
    'SteamInjectionPlugin',
    'CO2MisciblePlugin',
    
    # Persistence
    'ProjectManager',
    'ResultsCache',
    
    # Analysis
    'SensitivityAnalyzer',
    'HybridEOROptimizer',
    'IntelligentRecommender',
    'SensitivityMetric',
    
    # Dashboard
    'RealtimeDashboard',
    'DashboardMetrics',
    'DashboardAlert',
    
    # Reporting
    'AdvancedReportGenerator',
    'ReportMetadata',
]
