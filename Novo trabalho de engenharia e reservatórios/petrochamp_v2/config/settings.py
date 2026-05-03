"""
Configuração centralizada da aplicação PetroChamp Advanced
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceConfig:
    """Configurações de performance"""
    max_cache_size: int = 1000
    max_workers: int = 4
    update_interval_ms: int = 1000
    enable_caching: bool = True
    parallel_processing: bool = True
    cache_ttl_seconds: int = 3600


@dataclass
class VisualizationConfig:
    """Configurações de visualização"""
    default_theme: str = "dark"
    chart_quality: str = "high"  # low, medium, high
    animation_enabled: bool = True
    dpi: int = 100
    figure_size_default: tuple = (14, 6)
    figure_size_radar: tuple = (8, 8)
    figure_size_comparison: tuple = (12, 10)
    default_palette: str = "husl"


@dataclass
class AnalysisConfig:
    """Configurações de análise"""
    sensitivity_steps: int = 20
    monte_carlo_iterations: int = 1000
    risk_confidence_level: float = 0.95
    tornado_chart_enabled: bool = True
    parallel_sensitivity: bool = True
    min_similarity_threshold: float = 0.7
    max_recommendations: int = 5


@dataclass
class PersistenceConfig:
    """Configurações de persistência"""
    auto_save_interval_seconds: int = 300
    max_history_items: int = 100
    storage_path: str = "./projects"
    backup_enabled: bool = True
    backup_frequency: str = "daily"  # daily, weekly, monthly
    enable_version_control: bool = True


@dataclass
class APIConfig:
    """Configurações de APIs externas"""
    enable_external_apis: bool = False
    timeout_seconds: int = 30
    retry_attempts: int = 3
    cache_external_data: bool = True
    
    # Chaves de API (carregadas de variáveis de ambiente)
    oil_price_api_key: Optional[str] = None
    co2_supply_api_key: Optional[str] = None
    equipment_cost_api_key: Optional[str] = None


@dataclass
class AppConfig:
    """Configuração central da aplicação PetroChamp Advanced"""
    
    # Versão da aplicação
    version: str = "2.0.0"
    app_name: str = "PetroChamp Advanced"
    
    # Configurações específicas (usar field com default_factory)
    performance: Optional[PerformanceConfig] = None
    visualization: Optional[VisualizationConfig] = None
    analysis: Optional[AnalysisConfig] = None
    persistence: Optional[PersistenceConfig] = None
    api: Optional[APIConfig] = None
    
    # Configurações gerais
    debug_mode: bool = False
    log_level: str = "INFO"
    enable_tooltips: bool = True
    enable_dark_mode: bool = True
    
    def __post_init__(self):
        """Validar e processar configurações"""
        # Inicializar configs se não fornecidas
        if self.performance is None:
            self.performance = PerformanceConfig()
        if self.visualization is None:
            self.visualization = VisualizationConfig()
        if self.analysis is None:
            self.analysis = AnalysisConfig()
        if self.persistence is None:
            self.persistence = PersistenceConfig()
        if self.api is None:
            self.api = APIConfig()
        
        # Criar diretório de storage se não existir
        Path(self.persistence.storage_path).mkdir(parents=True, exist_ok=True)
        # Converter dicts para dataclass instances se necessário
        if isinstance(self.performance, dict):
            self.performance = PerformanceConfig(**self.performance)
        if isinstance(self.visualization, dict):
            self.visualization = VisualizationConfig(**self.visualization)
        if isinstance(self.analysis, dict):
            self.analysis = AnalysisConfig(**self.analysis)
        if isinstance(self.persistence, dict):
            self.persistence = PersistenceConfig(**self.persistence)
        if isinstance(self.api, dict):
            self.api = APIConfig(**self.api)
    
    @classmethod
    def from_file(cls, filepath: str) -> 'AppConfig':
        """Carrega configuração de arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Configuração carregada de: {filepath}")
            return cls(**data)
        except FileNotFoundError:
            logger.warning(f"Arquivo de config não encontrado: {filepath}. Usando padrão.")
            return cls()
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}. Usando padrão.")
            return cls()
    
    def save(self, filepath: str) -> bool:
        """Salva configuração em arquivo JSON"""
        try:
            # Converter dataclasses para dict
            config_dict = {
                'version': self.version,
                'app_name': self.app_name,
                'performance': asdict(self.performance) if isinstance(self.performance, PerformanceConfig) else self.performance,
                'visualization': asdict(self.visualization) if isinstance(self.visualization, VisualizationConfig) else self.visualization,
                'analysis': asdict(self.analysis) if isinstance(self.analysis, AnalysisConfig) else self.analysis,
                'persistence': asdict(self.persistence) if isinstance(self.persistence, PersistenceConfig) else self.persistence,
                'api': asdict(self.api) if isinstance(self.api, APIConfig) else self.api,
                'debug_mode': self.debug_mode,
                'log_level': self.log_level,
                'enable_tooltips': self.enable_tooltips,
                'enable_dark_mode': self.enable_dark_mode,
            }
            
            # Criar diretório se não existir
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Configuração salva em: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def validate(self) -> tuple[bool, list[str]]:
        """Valida configurações e retorna (is_valid, errors)"""
        errors = []
        
        # Validar performance
        if self.performance['max_workers'] < 1:
            errors.append("max_workers deve ser >= 1")
        
        if self.performance['max_cache_size'] < 10:
            errors.append("max_cache_size deve ser >= 10")
        
        # Validar análise
        if self.analysis['sensitivity_steps'] < 5:
            errors.append("sensitivity_steps deve ser >= 5")
        
        if not (0 < self.analysis['risk_confidence_level'] < 1):
            errors.append("risk_confidence_level deve estar entre 0 e 1")
        
        # Validar persistência
        try:
            Path(self.persistence['storage_path']).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Erro ao acessar storage_path: {e}")
        
        return len(errors) == 0, errors


# Instância global de configuração
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Retorna instância global de configuração"""
    global _config
    if _config is None:
        _config = AppConfig()
    return _config


def load_config(filepath: str) -> AppConfig:
    """Carrega e define configuração global"""
    global _config
    _config = AppConfig.from_file(filepath)
    
    # Validar
    is_valid, errors = _config.validate()
    if not is_valid:
        logger.warning(f"Erros de configuração: {errors}")
    
    return _config


def set_config(config: AppConfig) -> None:
    """Define configuração global"""
    global _config
    _config = config


# Configurações predefinidas por ambiente
DEVELOPMENT_CONFIG = AppConfig(
    debug_mode=True,
    log_level="DEBUG",
    analysis=AnalysisConfig(sensitivity_steps=10),  # Menos iterações para desenvolvimento
)

PRODUCTION_CONFIG = AppConfig(
    debug_mode=False,
    log_level="INFO",
    analysis=AnalysisConfig(sensitivity_steps=20),
    performance=PerformanceConfig(max_workers=8),
)

LIGHTWEIGHT_CONFIG = AppConfig(
    performance=PerformanceConfig(
        max_cache_size=100,
        max_workers=2,
        enable_caching=False
    ),
    analysis=AnalysisConfig(
        sensitivity_steps=5,
        monte_carlo_iterations=100
    ),
)
