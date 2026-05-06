"""
Sistema de plugins para métodos EOR
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class EORMethodType(Enum):
    """Tipos de métodos EOR"""
    STEAM_INJECTION = "steam_injection"
    IN_SITU_COMBUSTION = "in_situ_combustion"
    CO2_MISCIBLE = "co2_miscible"
    POLYMERIC_FLOODING = "polymeric_flooding"
    SURFACTANT_FLOODING = "surfactant_flooding"
    ALKALINE_FLOODING = "alkaline_flooding"
    IMMISCIBLE_GAS = "immiscible_gas"
    NITROGEN_INJECTION = "nitrogen_injection"
    ENRICHED_GAS = "enriched_gas"
    POLYMER_SURFACTANT = "polymer_surfactant"
    VAPEX = "vapex"
    SMART_WATERFLOODING = "smart_waterflooding"
    FOAM_INJECTION = "foam_injection"
    ELECTRIC_HEATING = "electric_heating"
    MICROBIAL_INJECTION = "microbial_injection"


@dataclass
class EORMethodMetadata:
    """Metadados de método EOR"""
    name: str
    type: EORMethodType
    description: str
    developed_year: int
    maturity_level: str  # "Experimental", "Emerging", "Proven"
    applicable_api_range: tuple  # (min, max)
    applicable_viscosity_range: tuple  # (min, max) cP
    typical_recovery_increase: float  # %
    typical_capex_per_well: float  # $ milhões
    typical_opex_annual: float  # $ milhões/ano


class EORMethodPlugin(ABC):
    """Interface abstrata para plugins de métodos EOR"""
    
    @abstractmethod
    def get_metadata(self) -> EORMethodMetadata:
        """Retorna metadados do método"""
        pass
    
    @abstractmethod
    def get_screening_criteria(self) -> Dict[str, Dict[str, Any]]:
        """Retorna critérios de triagem
        
        Formato:
        {
            'API': {'min': None, 'max': 22, 'weight': 0.3},
            'Viscosity': {'min': 100, 'max': None, 'weight': 0.3},
            ...
        }
        """
        pass
    
    @abstractmethod
    def calculate_suitability(self, reservoir_data: Dict[str, float]) -> float:
        """Calcula score de suitability (0-100)"""
        pass
    
    @abstractmethod
    def get_justification(self, score: float, reservoir_data: Dict) -> str:
        """Gera justificativa textual baseada no score"""
        pass
    
    @abstractmethod
    def get_critical_parameters(self, reservoir_data: Dict) -> List[str]:
        """Retorna parâmetros críticos para este método"""
        pass
    
    @abstractmethod
    def estimate_recovery_factor(self, reservoir_data: Dict, 
                                 operational_params: Dict) -> float:
        """Estima fator de recuperação (0-1)"""
        pass
    
    @abstractmethod
    def get_economic_parameters(self) -> Dict[str, float]:
        """Retorna parâmetros econômicos padrão"""
        pass
    
    @abstractmethod
    def get_implementation_roadmap(self) -> Dict[str, Any]:
        """Retorna plano de implementação"""
        pass


# ============================================================================
# PLUGINS IMPLEMENTADOS
# ============================================================================

class SteamInjectionPlugin(EORMethodPlugin):
    """Plugin para Injeção de Vapor"""
    
    def get_metadata(self) -> EORMethodMetadata:
        return EORMethodMetadata(
            name="Injeção de Vapor",
            type=EORMethodType.STEAM_INJECTION,
            description="Redução de viscosidade através de injeção de vapor saturado ou superaquecido",
            developed_year=1960,
            maturity_level="Proven",
            applicable_api_range=(0, 22),
            applicable_viscosity_range=(100, 50000),
            typical_recovery_increase=0.30,
            typical_capex_per_well=2.5,
            typical_opex_annual=0.5
        )
    
    def get_screening_criteria(self) -> Dict[str, Dict[str, Any]]:
        return {
            "API": {"min": None, "max": 22, "weight": 0.30},
            "Viscosity": {"min": 100, "max": None, "weight": 0.30},
            "Depth": {"min": 150, "max": 1500, "weight": 0.15},
            "Thickness": {"min": 6, "max": None, "weight": 0.10},
            "Oil_Saturation": {"min": 40, "max": None, "weight": 0.15}
        }
    
    def calculate_suitability(self, reservoir_data: Dict[str, float]) -> float:
        """Calcula suitability para steam injection"""
        score = 0.0
        criteria = self.get_screening_criteria()
        
        # API - crítico
        api = reservoir_data.get('api_gravity', 25)
        if api and api <= 22:
            api_score = (22 - api) / 22 * 100  # Mais pesado = melhor
            score += min(api_score, 100) * criteria['API']['weight']
        
        # Viscosidade - crítico
        visc = reservoir_data.get('viscosity', 100)
        if visc and visc >= 100:
            visc_score = min((visc / 5000) * 100, 100)  # Mais viscoso = melhor (até limite)
            score += visc_score * criteria['Viscosity']['weight']
        
        # Profundidade
        depth = reservoir_data.get('depth', 1000)
        if depth and 150 <= depth <= 1500:
            depth_score = 100 - abs((depth - 750) / 750) * 50  # Ótimo em torno de 750m
            score += depth_score * criteria['Depth']['weight']
        
        # Espessura
        thickness = reservoir_data.get('thickness', 15)
        if thickness and thickness >= 6:
            thickness_score = min((thickness / 30) * 100, 100)
            score += thickness_score * criteria['Thickness']['weight']
        
        # Saturação de óleo
        oil_sat = reservoir_data.get('oil_saturation', 50)
        if oil_sat and oil_sat >= 40:
            oil_sat_score = (oil_sat / 100) * 100
            score += oil_sat_score * criteria['Oil_Saturation']['weight']
        
        return min(score, 100)
    
    def get_justification(self, score: float, reservoir_data: Dict) -> str:
        """Gera justificativa baseada no score"""
        if score >= 80:
            return (
                "🟢 ALTA SUITABILITY - Seu reservatório é IDEAL para injeção de vapor. "
                f"Óleo muito pesado (API {reservoir_data.get('api_gravity', 25):.1f}°), alta viscosidade "
                f"({reservoir_data.get('viscosity', 500):.0f} cP), e características geológicas excelentes. "
                "Viscosidade reduzirá 100-1000x com aumento de temperatura. Recuperação esperada: 20-40%."
            )
        elif score >= 60:
            return (
                "🟡 SUITABILITY MÉDIA - O método tem potencial, mas com limitações. "
                "Profundidade ou espessura podem reduzir eficiência. Recomenda-se análise detalhada "
                "de balanço energético. Recuperação esperada: 10-20%."
            )
        else:
            return (
                "🔴 BAIXA SUITABILITY - Não recomendado. Óleo muito leve, profundidade inadequada, "
                "ou perdas de calor muito altas (>30%). Custo pode exceder US$15/bbl."
            )
    
    def get_critical_parameters(self, reservoir_data: Dict) -> List[str]:
        """Parâmetros críticos"""
        return ["API", "Viscosity", "Depth", "Temperature"]
    
    def estimate_recovery_factor(self, reservoir_data: Dict, 
                                operational_params: Dict) -> float:
        """Estima fator de recuperação"""
        base_recovery = 0.15  # 15% base
        
        # Ajustar por API
        api = reservoir_data.get('api_gravity', 25)
        if api < 12:
            base_recovery += 0.20
        elif api < 18:
            base_recovery += 0.15
        elif api < 22:
            base_recovery += 0.10
        
        # Ajustar por viscosidade
        visc = reservoir_data.get('viscosity', 100)
        if visc > 1000:
            base_recovery += 0.10
        elif visc > 500:
            base_recovery += 0.08
        
        return min(base_recovery, 0.50)  # Máximo 50%
    
    def get_economic_parameters(self) -> Dict[str, float]:
        return {
            'capex_per_well': 2.5e6,  # $ 2.5M
            'opex_annual': 0.5e6,  # $ 0.5M/ano
            'production_rate_bbl_day': 200,
            'steam_cost_per_bbl': 15.0,
            'well_spacing': 10  # acres
        }
    
    def get_implementation_roadmap(self) -> Dict[str, Any]:
        return {
            'phase_1': {
                'name': 'Piloto',
                'duration_months': 12,
                'wells': 2,
                'investment': 5e6
            },
            'phase_2': {
                'name': 'Expansão',
                'duration_months': 24,
                'wells': 10,
                'investment': 25e6
            },
            'phase_3': {
                'name': 'Produção Plena',
                'duration_months': 60,
                'wells': 30,
                'investment': 75e6
            }
        }


class CO2MisciblePlugin(EORMethodPlugin):
    """Plugin para Injeção de CO2 Miscível"""
    
    def get_metadata(self) -> EORMethodMetadata:
        return EORMethodMetadata(
            name="Injeção de CO2 Miscível",
            type=EORMethodType.CO2_MISCIBLE,
            description="Deslocamento miscível de óleo usando CO2 sob alta pressão",
            developed_year=1975,
            maturity_level="Proven",
            applicable_api_range=(27, 60),
            applicable_viscosity_range=(0.1, 12),
            typical_recovery_increase=0.20,
            typical_capex_per_well=3.0,
            typical_opex_annual=1.0
        )
    
    def get_screening_criteria(self) -> Dict[str, Dict[str, Any]]:
        return {
            "API": {"min": 27, "max": None, "weight": 0.25},
            "Viscosity": {"min": None, "max": 12, "weight": 0.20},
            "Pressure": {"min": 1200, "max": None, "weight": 0.20},
            "Depth": {"min": 800, "max": None, "weight": 0.15},
            "Temperature": {"min": None, "max": 120, "weight": 0.10},
            "Salinity": {"min": None, "max": 100000, "weight": 0.10}
        }
    
    def calculate_suitability(self, reservoir_data: Dict[str, float]) -> float:
        """Calcula suitability para CO2 miscível"""
        score = 0.0
        criteria = self.get_screening_criteria()
        
        # API
        api = reservoir_data.get('api_gravity', 30)
        if api and api >= 27:
            api_score = ((api - 27) / 33) * 100  # Maior é melhor
            score += min(api_score, 100) * criteria['API']['weight']
        
        # Viscosidade
        visc = reservoir_data.get('viscosity', 1.0)
        if visc and visc <= 12:
            visc_score = (1 - (visc / 12)) * 100  # Menor é melhor
            score += visc_score * criteria['Viscosity']['weight']
        
        # Pressão
        pressure = reservoir_data.get('pressure', 1500)
        if pressure and pressure >= 1200:
            pressure_score = min(((pressure - 1200) / 1800) * 100, 100)
            score += pressure_score * criteria['Pressure']['weight']
        
        # Profundidade
        depth = reservoir_data.get('depth', 1000)
        if depth and depth >= 800:
            depth_score = min(((depth - 800) / 1200) * 100, 100)
            score += depth_score * criteria['Depth']['weight']
        
        return min(score, 100)
    
    def get_justification(self, score: float, reservoir_data: Dict) -> str:
        if score >= 80:
            return (
                "🟢 ALTA SUITABILITY - Excelente para CO2 miscível. "
                f"Óleo leve (API {reservoir_data.get('api_gravity', 30):.1f}°), baixa viscosidade, "
                "pressão e profundidade adequadas. Recuperação esperada: 15-25%."
            )
        elif score >= 60:
            return (
                "🟡 SUITABILITY MÉDIA - Possível aplicação com otimizações. "
                "Alguns parâmetros fora da faixa ideal. Análise econômica necessária."
            )
        else:
            return (
                "🔴 BAIXA SUITABILITY - Não adequado. Óleo muito pesado ou viscoso, "
                "ou pressão insuficiente para miscibilidade."
            )
    
    def get_critical_parameters(self, reservoir_data: Dict) -> List[str]:
        return ["API", "Viscosity", "Pressure", "Depth"]
    
    def estimate_recovery_factor(self, reservoir_data: Dict, 
                                operational_params: Dict) -> float:
        base_recovery = 0.10  # 10% base
        
        api = reservoir_data.get('api_gravity', 30)
        if api > 35:
            base_recovery += 0.12
        elif api > 27:
            base_recovery += 0.08
        
        pressure = reservoir_data.get('pressure', 1500)
        if pressure > 1800:
            base_recovery += 0.05
        
        return min(base_recovery, 0.35)
    
    def get_economic_parameters(self) -> Dict[str, float]:
        return {
            'capex_per_well': 3.0e6,
            'opex_annual': 1.0e6,
            'production_rate_bbl_day': 300,
            'co2_cost_per_ton': 30.0,
            'injection_rate_tons_day': 50
        }
    
    def get_implementation_roadmap(self) -> Dict[str, Any]:
        return {
            'phase_1': {
                'name': 'Piloto',
                'duration_months': 18,
                'wells': 3,
                'investment': 10e6
            },
            'phase_2': {
                'name': 'Produção',
                'duration_months': 36,
                'wells': 15,
                'investment': 50e6
            }
        }


class PluginManager:
    """Gerenciador de plugins de métodos EOR"""
    
    def __init__(self):
        self.plugins: Dict[str, EORMethodPlugin] = {}
        self.load_builtin_plugins()
        logger.info(f"PluginManager inicializado com {len(self.plugins)} plugins")
    
    def load_builtin_plugins(self) -> None:
        """Carrega plugins embutidos"""
        builtin_plugins = [
            SteamInjectionPlugin(),
            CO2MisciblePlugin(),
            # Adicionar mais plugins conforme necessário
        ]
        
        for plugin in builtin_plugins:
            self.register_plugin(plugin)
    
    def register_plugin(self, plugin: EORMethodPlugin, override: bool = False) -> bool:
        """Registra novo plugin"""
        metadata = plugin.get_metadata()
        name = metadata.name
        
        if name in self.plugins and not override:
            logger.warning(f"Plugin '{name}' já existe. Use override=True para substituir")
            return False
        
        self.plugins[name] = plugin
        logger.info(f"Plugin registrado: {name}")
        return True
    
    def get_plugin(self, method_name: str) -> Optional[EORMethodPlugin]:
        """Obtém plugin de um método"""
        return self.plugins.get(method_name)
    
    def get_available_methods(self) -> List[str]:
        """Lista métodos disponíveis"""
        return sorted(list(self.plugins.keys()))
    
    def get_methods_by_type(self, method_type: EORMethodType) -> List[str]:
        """Lista métodos de um tipo específico"""
        return [
            name for name, plugin in self.plugins.items()
            if plugin.get_metadata().type == method_type
        ]
    
    def calculate_all_suitability_scores(self, reservoir_data: Dict[str, float]) -> Dict[str, float]:
        """Calcula suitability para todos os métodos"""
        scores = {}
        
        for method_name, plugin in self.plugins.items():
            try:
                score = plugin.calculate_suitability(reservoir_data)
                scores[method_name] = score
            except Exception as e:
                logger.error(f"Erro ao calcular suitability para {method_name}: {e}")
                scores[method_name] = 0.0
        
        return scores
    
    def get_top_methods(self, reservoir_data: Dict[str, float], 
                       n: int = 3) -> List[tuple[str, float]]:
        """Retorna top N métodos para um reservatório"""
        scores = self.calculate_all_suitability_scores(reservoir_data)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:n]
