"""
Modelos de dados para PetroChamp Advanced
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ReservoirType(Enum):
    """Tipos de reservatório"""
    ONSHORE = "onshore"
    OFFSHORE_SHALLOW = "offshore_shallow"
    OFFSHORE_DEEP = "offshore_deep"
    UNCONVENTIONAL = "unconventional"
    CARBONATE = "carbonate"
    SANDSTONE = "sandstone"


class EORMethodType(Enum):
    """Tipos de métodos EOR"""
    THERMAL = "thermal"
    CHEMICAL = "chemical"
    MISCIBLE = "miscible"
    IMMISCIBLE = "immiscible"
    HYBRID = "hybrid"


@dataclass
class ReservoirData:
    """Dados do reservatório"""
    api_gravity: float  # °API
    viscosity: float  # cP
    depth: float  # m
    thickness: float  # m
    permeability: float  # mD
    porosity: float  # %
    temperature: float  # °C
    pressure: float  # bar
    salinity: float  # ppm
    oil_saturation: float  # %
    water_saturation: float = 0.0
    
    # Parâmetros adicionais
    reservoir_type: ReservoirType = ReservoirType.SANDSTONE
    location: str = ""
    field_name: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['reservoir_type'] = self.reservoir_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReservoirData':
        """Cria a partir de dicionário"""
        if isinstance(data.get('reservoir_type'), str):
            data['reservoir_type'] = ReservoirType(data['reservoir_type'])
        return cls(**data)


@dataclass
class ScreeningResult:
    """Resultado de triagem para um método EOR"""
    method_name: str
    suitability_score: float  # 0-100
    rank: int
    status: str  # "ALTA", "MEDIA", "BAIXA"
    confidence: float  # 0-1
    
    # Detalhes
    justified_criteria: Dict[str, float] = field(default_factory=dict)
    critical_parameters: List[str] = field(default_factory=list)
    limiting_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Metadados
    calculated_at: datetime = field(default_factory=datetime.now)
    computation_time_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['calculated_at'] = self.calculated_at.isoformat()
        return data


@dataclass
class EconomicAnalysis:
    """Análise econômica"""
    method: str
    
    # Custos
    capex: float  # $ milhões
    opex_annual: float  # $ milhões/ano
    drilling_wells: int
    production_rate_bbl_day: float
    
    # Finanças
    oil_price: float = 75.0  # $/bbl
    discount_rate: float = 0.1  # 10%
    project_life: int = 20  # anos
    
    # Resultados
    npv: float = 0.0  # $ milhões
    irr: float = 0.0  # %
    payback_period: float = 0.0  # anos
    recovery_factor: float = 0.0  # %
    cumulative_production: float = 0.0  # MMbbl
    
    # Riscos
    risk_adjusted_npv: float = 0.0
    probability_of_success: float = 0.7
    
    calculated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['calculated_at'] = self.calculated_at.isoformat()
        return data


@dataclass
class SensitivityAnalysisResult:
    """Resultado de análise de sensibilidade"""
    method: str
    base_case_npv: float
    
    parameters_sensitivity: Dict[str, float] = field(default_factory=dict)
    tornado_chart_data: Dict[str, tuple] = field(default_factory=dict)
    
    # Monte Carlo
    monte_carlo_mean: float = 0.0
    monte_carlo_std: float = 0.0
    monte_carlo_p10: float = 0.0
    monte_carlo_p90: float = 0.0
    
    calculated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['calculated_at'] = self.calculated_at.isoformat()
        return data


@dataclass
class EORProject:
    """Projeto EOR completo com persistência"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Novo Projeto"
    description: str = ""
    
    # Dados
    reservoir_data: ReservoirData = field(default_factory=lambda: ReservoirData(
        api_gravity=30, viscosity=50, depth=1500, thickness=20,
        permeability=100, porosity=20, temperature=60, pressure=200, salinity=50000
    ))
    
    # Resultados
    screening_results: List[ScreeningResult] = field(default_factory=list)
    economic_analyses: List[EconomicAnalysis] = field(default_factory=list)
    sensitivity_results: List[SensitivityAnalysisResult] = field(default_factory=list)
    
    # Metadados
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    author: str = "User"
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    
    # Status
    is_locked: bool = False
    backup_available: bool = False
    
    def to_dict(self, include_results: bool = True) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'reservoir_data': self.reservoir_data.to_dict(),
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'author': self.author,
            'tags': self.tags,
            'notes': self.notes,
            'is_locked': self.is_locked,
        }
        
        if include_results:
            data['screening_results'] = [r.to_dict() for r in self.screening_results]
            data['economic_analyses'] = [e.to_dict() for e in self.economic_analyses]
            data['sensitivity_results'] = [s.to_dict() for s in self.sensitivity_results]
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EORProject':
        """Cria a partir de dicionário"""
        # Processar tipos especiais
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('modified_at'), str):
            data['modified_at'] = datetime.fromisoformat(data['modified_at'])
        
        # Processar dados do reservatório
        if 'reservoir_data' in data and isinstance(data['reservoir_data'], dict):
            data['reservoir_data'] = ReservoirData.from_dict(data['reservoir_data'])
        
        # Processar resultados
        if 'screening_results' in data and isinstance(data['screening_results'], list):
            # Filtrar apenas os campos da dataclass
            screening_only = {
                k: v for k, v in data.items() 
                if k in ['id', 'name', 'description', 'reservoir_data', 'version', 
                        'created_at', 'modified_at', 'author', 'tags', 'notes', 'is_locked']
            }
            data = screening_only
        
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def save_to_file(self, filepath: str) -> bool:
        """Salva projeto em arquivo JSON"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, default=str)
            
            self.backup_available = True
            logger.info(f"Projeto salvo: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar projeto: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, filepath: str) -> Optional['EORProject']:
        """Carrega projeto de arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            project = cls.from_dict(data)
            logger.info(f"Projeto carregado: {filepath}")
            return project
        except Exception as e:
            logger.error(f"Erro ao carregar projeto: {e}")
            return None
    
    def get_best_method(self) -> Optional[ScreeningResult]:
        """Retorna método com melhor score"""
        if not self.screening_results:
            return None
        return max(self.screening_results, key=lambda r: r.suitability_score)
    
    def get_method_ranking(self) -> List[ScreeningResult]:
        """Retorna métodos ordenados por score"""
        return sorted(self.screening_results, 
                     key=lambda r: r.suitability_score, 
                     reverse=True)
    
    def get_top_n_methods(self, n: int = 3) -> List[ScreeningResult]:
        """Retorna top N métodos"""
        return self.get_method_ranking()[:n]


@dataclass
class ProjectStatistics:
    """Estatísticas de um projeto"""
    total_projects: int = 0
    projects_with_results: int = 0
    avg_best_score: float = 0.0
    most_recommended_method: str = ""
    avg_npv: float = 0.0
    avg_irr: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)
