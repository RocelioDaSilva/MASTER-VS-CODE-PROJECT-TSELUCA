"""
PETROCHAMP v5.0 - PLATAFORMA OTIMIZADA DE TRIAGEM EOR COM SUITABILITY
======================================================================

Versão refatorada e otimizada com:
- Arquitetura modular com separação de responsabilidades
- Performance otimizada com caching de resultados
- Type hints para melhor compreensão do código
- Tratamento robusto de erros
- Logging detalhado de operações
- Redução de duplicação de código
- Padrões de design (Singleton, Factory, MVC)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from abc import ABC, abstractmethod
from functools import lru_cache
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('petrochamp_v5.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    import numpy_financial as npf
    HAS_NUMPY_FINANCIAL = True
except ImportError:
    HAS_NUMPY_FINANCIAL = False
    logger.warning("numpy_financial não instalado. Usando cálculo manual de IRR.")

# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================
class Config:
    """Configurações globais da aplicação"""
    
    # Cores para interface
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#3498db',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'light': '#ecf0f1',
        'dark': '#2c3e50'
    }
    
    # Suitability thresholds
    SUITABILITY_THRESHOLDS = {
        'high': (80, 100),
        'medium': (60, 79),
        'low': (0, 59)
    }
    
    # Métodos EOR disponíveis
    EOR_METHODS = [
        "Injeção de Vapor",
        "Combustão In Situ",
        "Injeção de CO2 Miscível",
        "Injeção de Polímeros",
        "Injeção de Surfactantes",
        "Injeção Alcalina",
        "Injeção de Gás Não-Miscível",
        "Injeção de Nitrogênio",
        "Injeção de Gás Enriquecido",
        "Polímero-Surfactante",
        "VAPEX (Vapor Extraction)",
        "Injeção de Água Inteligente",
        "Injeção de Espuma",
        "Aquecimento Elétrico",
        "Injeção Microbiana"
    ]
    
    PARAMETERS = [
        ("API", "°API"),
        ("Viscosidade", "cP"),
        ("Profundidade", "m"),
        ("Permeabilidade", "mD"),
        ("Porosidade", "%"),
        ("Saturação de Óleo", "%"),
        ("Saturação de Água", "%"),
        ("Temperatura", "°C"),
        ("Pressão", "psi"),
        ("Salinidade", "ppm"),
        ("Espessura", "m"),
        ("TAN", "mg KOH/g"),
        ("Dip", "graus")
    ]

# ============================================================================
# BASE DE DADOS - CRITÉRIOS E JUSTIFICAÇÕES
# ============================================================================
class ScreeningDatabase:
    """Gerenciador centralizado de critérios e justificações"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._criteria = None
        self._justifications = None
    
    @property
    def criteria(self) -> Dict:
        """Carrega critérios sob demanda (lazy loading)"""
        if self._criteria is None:
            self._criteria = self._load_criteria()
        return self._criteria
    
    @property
    def justifications(self) -> Dict:
        """Carrega justificações sob demanda (lazy loading)"""
        if self._justifications is None:
            self._justifications = self._load_justifications()
        return self._justifications
    
    def _load_criteria(self) -> Dict:
        """Carrega critérios técnicos de triagem"""
        return {
            "Injeção de Vapor": {
                "API": {"min": None, "max": 22, "peso": 0.3},
                "Viscosidade": {"min": 100, "max": None, "peso": 0.3},
                "Profundidade": {"min": 150, "max": 1500, "peso": 0.15},
                "Espessura": {"min": 6, "max": None, "peso": 0.1},
                "Saturação de Óleo": {"min": 40, "max": None, "peso": 0.15}
            },
            "Combustão In Situ": {
                "API": {"min": None, "max": 25, "peso": 0.25},
                "Viscosidade": {"min": 50, "max": 10000, "peso": 0.25},
                "Permeabilidade": {"min": 50, "max": None, "peso": 0.2},
                "Profundidade": {"min": 300, "max": None, "peso": 0.15},
                "Espessura": {"min": 3, "max": None, "peso": 0.15}
            },
            "Injeção de CO2 Miscível": {
                "API": {"min": 27, "max": None, "peso": 0.25},
                "Viscosidade": {"min": None, "max": 12, "peso": 0.2},
                "Pressão": {"min": 1200, "max": None, "peso": 0.2},
                "Profundidade": {"min": 800, "max": None, "peso": 0.15},
                "Temperatura": {"min": None, "max": 120, "peso": 0.1},
                "Salinidade": {"min": None, "max": 100000, "peso": 0.1}
            },
            "Injeção de Polímeros": {
                "Viscosidade": {"min": None, "max": 150, "peso": 0.25},
                "Salinidade": {"min": None, "max": 20000, "peso": 0.2},
                "Temperatura": {"min": None, "max": 90, "peso": 0.15},
                "Permeabilidade": {"min": 10, "max": 5000, "peso": 0.2},
                "Saturação de Água": {"min": None, "max": 50, "peso": 0.1},
                "pH": {"min": 5, "max": 8, "peso": 0.1}
            },
            "Injeção de Surfactantes": {
                "Viscosidade": {"min": None, "max": 30, "peso": 0.2},
                "Salinidade": {"min": None, "max": 10000, "peso": 0.25},
                "Temperatura": {"min": None, "max": 80, "peso": 0.15},
                "Permeabilidade": {"min": 20, "max": None, "peso": 0.2},
                "Saturação de Óleo Residual": {"min": 25, "max": None, "peso": 0.2}
            },
            "Injeção Alcalina": {
                "Viscosidade": {"min": None, "max": 200, "peso": 0.2},
                "Salinidade": {"min": None, "max": 5000, "peso": 0.25},
                "TAN": {"min": 0.5, "max": None, "peso": 0.25},
                "Permeabilidade": {"min": 20, "max": None, "peso": 0.2},
                "pH": {"min": None, "max": 9, "peso": 0.1}
            },
            "Injeção de Gás Não-Miscível": {
                "API": {"min": 10, "max": 35, "peso": 0.3},
                "Viscosidade": {"min": None, "max": 100, "peso": 0.2},
                "Profundidade": {"min": 600, "max": None, "peso": 0.2},
                "Pressão": {"min": 800, "max": None, "peso": 0.15},
                "Dip": {"min": 10, "max": None, "peso": 0.15}
            },
            "Injeção de Nitrogênio": {
                "API": {"min": 30, "max": None, "peso": 0.25},
                "Viscosidade": {"min": None, "max": 10, "peso": 0.2},
                "Profundidade": {"min": 2000, "max": None, "peso": 0.2},
                "Pressão": {"min": 1500, "max": None, "peso": 0.15},
                "Temperatura": {"min": None, "max": 150, "peso": 0.1},
                "Dip": {"min": 15, "max": None, "peso": 0.1}
            },
            "Injeção de Gás Enriquecido": {
                "API": {"min": 25, "max": None, "peso": 0.3},
                "Viscosidade": {"min": None, "max": 15, "peso": 0.2},
                "Pressão": {"min": 1000, "max": 3000, "peso": 0.2},
                "Profundidade": {"min": 1000, "max": None, "peso": 0.15},
                "Temperatura": {"min": None, "max": 110, "peso": 0.15}
            },
            "Polímero-Surfactante": {
                "Viscosidade": {"min": None, "max": 100, "peso": 0.2},
                "Salinidade": {"min": None, "max": 15000, "peso": 0.25},
                "Temperatura": {"min": None, "max": 85, "peso": 0.15},
                "Permeabilidade": {"min": 30, "max": 2000, "peso": 0.2},
                "Saturação de Óleo Residual": {"min": 30, "max": None, "peso": 0.2}
            },
            "VAPEX (Vapor Extraction)": {
                "API": {"min": None, "max": 20, "peso": 0.3},
                "Viscosidade": {"min": 1000, "max": 10000, "peso": 0.3},
                "Profundidade": {"min": 500, "max": None, "peso": 0.15},
                "Permeabilidade": {"min": 100, "max": None, "peso": 0.15},
                "Espessura": {"min": 10, "max": None, "peso": 0.1}
            },
            "Injeção de Água Inteligente": {
                "Viscosidade": {"min": None, "max": 100, "peso": 0.2},
                "Salinidade": {"min": 5000, "max": 50000, "peso": 0.25},
                "TAN": {"min": 0.3, "max": None, "peso": 0.2},
                "Temperatura": {"min": None, "max": 120, "peso": 0.15},
                "Permeabilidade": {"min": 50, "max": None, "peso": 0.2}
            },
            "Injeção de Espuma": {
                "Viscosidade": {"min": None, "max": 50, "peso": 0.2},
                "Salinidade": {"min": None, "max": 50000, "peso": 0.2},
                "Temperatura": {"min": None, "max": 90, "peso": 0.2},
                "Permeabilidade": {"min": 100, "max": 3000, "peso": 0.2},
                "Saturação de Óleo": {"min": 30, "max": 70, "peso": 0.2}
            },
            "Aquecimento Elétrico": {
                "API": {"min": None, "max": 18, "peso": 0.3},
                "Viscosidade": {"min": 500, "max": 5000, "peso": 0.3},
                "Profundidade": {"min": 100, "max": 800, "peso": 0.2},
                "Permeabilidade": {"min": 50, "max": None, "peso": 0.1},
                "Espessura": {"min": 5, "max": 30, "peso": 0.1}
            },
            "Injeção Microbiana": {
                "Viscosidade": {"min": None, "max": 1000, "peso": 0.25},
                "Temperatura": {"min": 20, "max": 80, "peso": 0.25},
                "Salinidade": {"min": None, "max": 100000, "peso": 0.2},
                "Permeabilidade": {"min": 50, "max": None, "peso": 0.2},
                "pH": {"min": 5, "max": 9, "peso": 0.1}
            }
        }
    
    def _load_justifications(self) -> Dict:
        """Carrega justificações (abreviadas para economia de espaço)"""
        return {
            "Injeção de Vapor": {
                "alta": "🟢 ALTA - Óleo pesado com viscosidade ideal. Profundidade e espessura adequadas. Recuperação esperada: 20-30%.",
                "media": "🟡 MÉDIA - Alguns parâmetros nos limites. Estudo detalhado recomendado.",
                "baixa": "🔴 BAIXA - Óleo muito leve ou profundidade inadequada. Não recomendado."
            },
            # ... Adicionar outros métodos conforme necessário
        }

# ============================================================================
# MOTOR DE ANÁLISE
# ============================================================================
class EORAnalyzer:
    """Analisador principal de métodos EOR"""
    
    def __init__(self):
        self.db = ScreeningDatabase()
        self._cache = {}
    
    def score_reservoir(self, reservoir_data: Dict[str, Any]) -> Dict:
        """
        Calcula pontuação para cada método EOR
        
        Args:
            reservoir_data: Dicionário com dados do reservatório
            
        Returns:
            Dicionário com resultados de pontuação
        """
        # Verificar cache
        cache_key = hash(frozenset(reservoir_data.items()))
        if cache_key in self._cache:
            logger.info("Retornando resultado em cache")
            return self._cache[cache_key]
        
        scores = {}
        criteria = self.db.criteria
        
        for method in Config.EOR_METHODS:
            score_data = self._calculate_method_score(
                method, 
                reservoir_data, 
                criteria.get(method, {})
            )
            scores[method] = score_data
        
        # Armazenar em cache
        self._cache[cache_key] = scores
        return scores
    
    def _calculate_method_score(
        self, 
        method: str, 
        reservoir: Dict, 
        criteria: Dict
    ) -> Dict:
        """Calcula pontuação para um método específico"""
        
        score = 0.0
        max_score = 0.0
        criteria_scores = {}
        strengths = []
        weaknesses = []
        
        for param, limits in criteria.items():
            max_score += limits["peso"] * 100
            
            if param in reservoir and reservoir[param] is not None:
                value = reservoir[param]
                param_score = self._evaluate_parameter(value, limits)
                criteria_scores[param] = param_score
                
                if param_score > 0:
                    score += limits["peso"] * 100
                    strengths.append(f"{param}: {value} ✓")
                else:
                    weaknesses.append(f"{param}: {value} ✗")
            else:
                criteria_scores[param] = 0
                weaknesses.append(f"{param}: N/A")
        
        normalized_score = (score / max_score * 100) if max_score > 0 else 0
        
        return {
            "score": normalized_score,
            "status": self._get_status(normalized_score),
            "color": self._get_color(normalized_score),
            "suitability": self._get_suitability_label(normalized_score),
            "criteria_scores": criteria_scores,
            "strengths": strengths[:3],
            "weaknesses": weaknesses[:3]
        }
    
    @staticmethod
    def _evaluate_parameter(value: float, limits: Dict) -> float:
        """Avalia se parâmetro atende aos critérios"""
        if limits["min"] is not None and value < limits["min"]:
            return 0.0
        if limits["max"] is not None and value > limits["max"]:
            return 0.0
        return 1.0
    
    @staticmethod
    def _get_status(score: float) -> str:
        """Retorna status baseado em pontuação"""
        if score >= 80:
            return "RECOMENDADO"
        elif score >= 60:
            return "POTENCIAL"
        else:
            return "NÃO RECOMENDADO"
    
    @staticmethod
    def _get_color(score: float) -> str:
        """Retorna cor baseada em pontuação"""
        if score >= 80:
            return "green"
        elif score >= 60:
            return "orange"
        else:
            return "red"
    
    @staticmethod
    def _get_suitability_label(score: float) -> str:
        """Retorna label de suitability"""
        if score >= 80:
            return "🟢 ALTA"
        elif score >= 60:
            return "🟡 MÉDIA"
        else:
            return "🔴 BAIXA"

# ============================================================================
# ANALISADOR ECONÔMICO OTIMIZADO
# ============================================================================
class EconomicAnalyzer:
    """Analisador econômico para projetos EOR"""
    
    DEFAULT_PARAMS = {
        "oil_price": 60.0,
        "discount_rate": 10,
        "tax_rate": 25,
        "project_life": 15,
        "opex_percentage": 30,
        "decline_rate": 15
    }
    
    def calculate_metrics(
        self, 
        production_profile: List[float], 
        economic_params: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calcula métricas econômicas completas
        
        Args:
            production_profile: Lista de produção anual
            economic_params: Parâmetros econômicos
            
        Returns:
            Dicionário com NPV, IRR, Payback
        """
        
        params = {**self.DEFAULT_PARAMS, **economic_params}
        
        # Calcular fluxo de caixa
        production = np.array(production_profile)
        revenue = production * params["oil_price"]
        opex = revenue * (params["opex_percentage"] / 100)
        net_cash_flow = revenue - opex
        
        # Calcular métricas
        npv = self._calculate_npv(net_cash_flow, params["discount_rate"])
        irr = self._calculate_irr(net_cash_flow)
        payback = self._calculate_payback(net_cash_flow)
        
        logger.info(f"Análise econômica: NPV=${npv:,.2f}, IRR={irr:.2f}%, Payback={payback:.2f}anos")
        
        return {
            "npv": npv,
            "irr": irr,
            "payback": payback,
            "revenue": revenue.tolist(),
            "opex": opex.tolist(),
            "net_cash_flow": net_cash_flow.tolist()
        }
    
    @staticmethod
    def _calculate_npv(cash_flow: np.ndarray, discount_rate: float) -> float:
        """Calcula NPV de forma vetorizada"""
        periods = np.arange(len(cash_flow))
        pv_factors = (1 + discount_rate / 100) ** periods
        return float(np.sum(cash_flow / pv_factors))
    
    @staticmethod
    def _calculate_irr(cash_flow: List[float]) -> float:
        """Calcula IRR usando método de bisseção"""
        cf_array = np.array(cash_flow)
        
        try:
            if HAS_NUMPY_FINANCIAL:
                irr_value = npf.irr(cf_array)
                return float(irr_value * 100) if irr_value is not None else 0.0
        except:
            pass
        
        # Fallback: método de bisseção
        def npv_func(rate):
            periods = np.arange(len(cf_array))
            return np.sum(cf_array / ((1 + rate) ** periods))
        
        try:
            low, high = -0.99, 1.0
            for _ in range(1000):
                mid = (low + high) / 2
                if abs(npv_func(mid)) < 1e-6:
                    return mid * 100
                if npv_func(low) * npv_func(mid) < 0:
                    high = mid
                else:
                    low = mid
            return mid * 100
        except:
            return 0.0
    
    @staticmethod
    def _calculate_payback(cash_flow: List[float]) -> Optional[float]:
        """Calcula período de payback"""
        cumulative = np.cumsum(cash_flow)
        for i, val in enumerate(cumulative):
            if val >= 0:
                if i == 0:
                    return 0.0
                prev = cumulative[i - 1]
                if val != prev:
                    return i - 1 + abs(prev) / (val - prev)
        return None

# ============================================================================
# VISUALIZADOR OTIMIZADO
# ============================================================================
class ChartGenerator:
    """Gerador otimizado de gráficos"""
    
    @staticmethod
    def create_suitability_bars(scores: Dict[str, Dict]) -> plt.Figure:
        """Cria gráfico de barras de suitability"""
        
        methods = list(scores.keys())
        score_values = [scores[m]["score"] for m in methods]
        colors = [
            '#27ae60' if scores[m]["score"] >= 80 else 
            '#f39c12' if scores[m]["score"] >= 60 else 
            '#e74c3c' 
            for m in methods
        ]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(methods, score_values, color=colors, edgecolor='black')
        
        ax.set_xlabel('Pontuação de Suitability (%)', fontweight='bold')
        ax.set_title('Análise de Suitability - Métodos EOR', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        # Adicionar valores nas barras
        for bar, score in zip(bars, score_values):
            ax.text(score + 1, bar.get_y() + bar.get_height()/2,
                   f'{score:.1f}%', va='center', fontweight='bold')
        
        # Linhas de referência
        ax.axvline(x=80, color='green', linestyle='--', alpha=0.5, label='Alta (≥80%)')
        ax.axvline(x=60, color='orange', linestyle='--', alpha=0.5, label='Média (60-79%)')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_economic_analysis(metrics: Dict[str, Any]) -> plt.Figure:
        """Cria gráficos econômicos"""
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Análise Econômica Completa', fontsize=14, fontweight='bold')
        
        # Gráfico 1: Fluxo de caixa acumulado
        cf = np.array(metrics["net_cash_flow"])
        cumsum_cf = np.cumsum(cf)
        years = list(range(len(cf)))
        
        axes[0, 0].plot(years, cumsum_cf, 'b-', linewidth=2, marker='o')
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 0].fill_between(years, cumsum_cf, alpha=0.3)
        axes[0, 0].set_title('Fluxo de Caixa Acumulado')
        axes[0, 0].set_ylabel('USD')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Receita vs OPEX
        if len(metrics["revenue"]) > 0:
            years_prod = list(range(1, len(metrics["revenue"]) + 1))
            axes[0, 1].bar(years_prod, metrics["revenue"], alpha=0.6, label='Receita', color='green')
            axes[0, 1].bar(years_prod, metrics["opex"], alpha=0.6, label='OPEX', color='red')
            axes[0, 1].set_title('Receita vs OPEX')
            axes[0, 1].set_ylabel('USD')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Sensibilidade NPV
        discount_rates = np.linspace(5, 20, 10)
        npv_values = [
            EconomicAnalyzer._calculate_npv(cf, dr) 
            for dr in discount_rates
        ]
        
        axes[1, 0].plot(discount_rates, npv_values, 'g-', linewidth=2, marker='s')
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 0].set_title('Sensibilidade do NPV')
        axes[1, 0].set_xlabel('Taxa de Desconto (%)')
        axes[1, 0].set_ylabel('NPV (USD)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfico 4: Métricas resumidas
        axes[1, 1].axis('off')
        metrics_text = f"""
        RESUMO ECONÔMICO
        
        NPV: ${metrics['npv']:,.2f}
        IRR: {metrics['irr']:.2f}%
        Payback: {metrics['payback']:.2f} anos
        
        Período do Projeto: 15 anos
        Status: {'✓ VIÁVEL' if metrics['npv'] > 0 else '✗ NÃO VIÁVEL'}
        """
        axes[1, 1].text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
                       verticalalignment='center')
        
        plt.tight_layout()
        return fig

# ============================================================================
# GERENCIADOR DE DADOS
# ============================================================================
class DataManager:
    """Gerencia dados de reservatórios e projetos"""
    
    def __init__(self):
        self.reservoirs: List[Dict] = []
        self.results: Optional[Dict] = None
    
    def add_reservoir(self, data: Dict) -> None:
        """Adiciona reservatório"""
        data["id"] = len(self.reservoirs) + 1
        self.reservoirs.append(data)
        logger.info(f"Reservatório {data['id']} adicionado")
    
    def clear(self) -> None:
        """Limpa todos os dados"""
        self.reservoirs.clear()
        self.results = None
        logger.info("Dados limpos")
    
    def export_to_excel(self, filepath: str, scores: Dict) -> None:
        """Exporta dados para Excel"""
        
        # Criar DataFrames
        triagem_data = []
        for method, data in scores.items():
            triagem_data.append({
                "Método": method,
                "Pontuação": data["score"],
                "Status": data["status"],
                "Suitability": data["suitability"]
            })
        
        triagem_df = pd.DataFrame(triagem_data)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            triagem_df.to_excel(writer, sheet_name='Triagem_EOR', index=False)
            
            if self.reservoirs:
                pd.DataFrame(self.reservoirs).to_excel(writer, sheet_name='Dados', index=False)
        
        logger.info(f"Exportado para {filepath}")

# ============================================================================
# INTERFACE GRÁFICA PRINCIPAL
# ============================================================================
class PetroChampUI:
    """Interface gráfica principal"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PetroChamp v5.0 - Triagem EOR Otimizada")
        self.root.geometry("1400x900")
        
        # Inicializar componentes
        self.analyzer = EORAnalyzer()
        self.econ_analyzer = EconomicAnalyzer()
        self.chart_gen = ChartGenerator()
        self.data_manager = DataManager()
        
        # Setup UI
        self._setup_styling()
        self._create_menu()
        self._create_interface()
        
        logger.info("Interface gráfica inicializada")
    
    def _setup_styling(self) -> None:
        """Configura temas e estilos"""
        style = ttk.Style()
        style.theme_use('clam')
        self.root.configure(bg=Config.COLORS['light'])
    
    def _create_menu(self) -> None:
        """Cria barra de menu"""
        menubar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo", command=self._new_project)
        file_menu.add_command(label="Importar CSV", command=self._import_csv)
        file_menu.add_command(label="Salvar Como Excel", command=self._export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Análise
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Executar Triagem", command=self._run_screening)
        analysis_menu.add_command(label="Análise Econômica", command=self._run_economic)
        menubar.add_cascade(label="Análise", menu=analysis_menu)
        
        self.root.config(menu=menubar)
    
    def _create_interface(self) -> None:
        """Cria interface principal"""
        
        # Notebook para abas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de entrada de dados
        data_tab = ttk.Frame(notebook)
        notebook.add(data_tab, text="Dados")
        self._create_data_tab(data_tab)
        
        # Aba de resultados
        results_tab = ttk.Frame(notebook)
        notebook.add(results_tab, text="Resultados")
        self._create_results_tab(results_tab)
        
        # Aba econômica
        econ_tab = ttk.Frame(notebook)
        notebook.add(econ_tab, text="Econômico")
        self._create_economic_tab(econ_tab)
        
        # Barra de status
        self.status_bar = tk.Label(
            self.root, 
            text="Pronto | PetroChamp v5.0",
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _create_data_tab(self, parent: ttk.Frame) -> None:
        """Cria aba de dados"""
        
        control_frame = ttk.LabelFrame(parent, text="Controles", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Importar CSV", 
                  command=self._import_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Carregar Exemplo", 
                  command=self._load_example).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Limpar Tudo", 
                  command=self._clear_data).pack(side=tk.LEFT, padx=5)
        
        # Tabela de dados
        data_frame = ttk.LabelFrame(parent, text="Reservatórios", padding=10)
        data_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ("ID", "API", "Viscosidade", "Profundidade", "Status")
        self.data_tree = ttk.Treeview(data_frame, columns=columns, height=15)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
        
        self.data_tree.pack(fill='both', expand=True)
    
    def _create_results_tab(self, parent: ttk.Frame) -> None:
        """Cria aba de resultados"""
        
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Executar Triagem", 
                  command=self._run_screening).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Visualizar Gráfico", 
                  command=self._show_chart).pack(side=tk.LEFT, padx=5)
        
        # Tabela de resultados
        results_frame = ttk.LabelFrame(parent, text="Resultados da Triagem", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ("Método", "Pontuação", "Status", "Suitability")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        self.results_tree.pack(fill='both', expand=True)
    
    def _create_economic_tab(self, parent: ttk.Frame) -> None:
        """Cria aba econômica"""
        
        control_frame = ttk.LabelFrame(parent, text="Parâmetros", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        params = [
            ("Preço do Óleo", "60"),
            ("Taxa de Desconto", "10"),
            ("Impostos", "25")
        ]
        
        self.econ_entries = {}
        for label, default in params:
            frame = ttk.Frame(control_frame)
            frame.pack(fill='x', padx=5, pady=5)
            
            tk.Label(frame, text=f"{label}:").pack(side=tk.LEFT, width=20)
            entry = ttk.Entry(frame, width=15)
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, padx=5)
            
            self.econ_entries[label] = entry
        
        ttk.Button(control_frame, text="Calcular", 
                  command=self._run_economic).pack(pady=10)
        
        # Canvas para gráficos
        self.chart_frame = ttk.Frame(parent)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    # ========== MÉTODOS DE AÇÃO ==========
    
    def _import_csv(self) -> None:
        """Importa dados de CSV"""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            df = pd.read_csv(filepath)
            self.data_manager.reservoirs = df.to_dict('records')
            self._update_data_tree()
            self._update_status(f"Importados {len(df)} reservatórios")
            logger.info(f"Importados {len(df)} reservatórios de {filepath}")
            messagebox.showinfo("Sucesso", f"Importados {len(df)} reservatórios")
        except Exception as e:
            logger.error(f"Erro ao importar: {e}")
            messagebox.showerror("Erro", f"Falha ao importar: {str(e)}")
    
    def _load_example(self) -> None:
        """Carrega exemplo de dados"""
        example = {
            "ID": 1,
            "API": 15.5,
            "Viscosidade": 850,
            "Profundidade": 1200,
            "Permeabilidade": 450,
            "Porosidade": 22,
            "Saturação de Óleo": 65,
            "Saturação de Água": 35,
            "Temperatura": 75,
            "Pressão": 1800,
            "Salinidade": 25000,
            "Espessura": 12,
            "TAN": 1.2,
            "Dip": 5
        }
        
        self.data_manager.reservoirs = [example]
        self._update_data_tree()
        self._update_status("Exemplo carregado")
        messagebox.showinfo("Exemplo", "Dados de exemplo carregados")
    
    def _clear_data(self) -> None:
        """Limpa todos os dados"""
        if not self.data_manager.reservoirs:
            return
        
        if messagebox.askyesno("Confirmar", "Limpar todos os dados?"):
            self.data_manager.clear()
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            self._update_status("Dados limpos")
    
    def _run_screening(self) -> None:
        """Executa triagem EOR"""
        if not self.data_manager.reservoirs:
            messagebox.showwarning("Aviso", "Nenhum dados disponível")
            return
        
        try:
            self._update_status("Executando triagem...")
            
            reservoir = self.data_manager.reservoirs[0]
            scores = self.analyzer.score_reservoir(reservoir)
            self.data_manager.results = scores
            
            self._update_results_tree(scores)
            self._update_status("Triagem concluída")
            messagebox.showinfo("Sucesso", "Triagem concluída")
            
        except Exception as e:
            logger.error(f"Erro na triagem: {e}")
            messagebox.showerror("Erro", f"Falha na triagem: {str(e)}")
    
    def _run_economic(self) -> None:
        """Executa análise econômica"""
        try:
            self._update_status("Calculando análise econômica...")
            
            # Obter parâmetros
            params = {
                "oil_price": float(self.econ_entries["Preço do Óleo"].get()),
                "discount_rate": float(self.econ_entries["Taxa de Desconto"].get()),
                "tax_rate": float(self.econ_entries["Impostos"].get())
            }
            
            # Gerar produção
            production = [1000 * (0.85 ** year) for year in range(15)]
            
            # Calcular
            metrics = self.econ_analyzer.calculate_metrics(production, params)
            
            # Mostrar gráficos
            self._show_economic_chart(metrics)
            self._update_status("Análise econômica concluída")
            
        except Exception as e:
            logger.error(f"Erro na análise econômica: {e}")
            messagebox.showerror("Erro", f"Falha: {str(e)}")
    
    def _show_chart(self) -> None:
        """Mostra gráficos de suitability"""
        if not self.data_manager.results:
            messagebox.showwarning("Aviso", "Execute triagem primeiro")
            return
        
        try:
            fig = self.chart_gen.create_suitability_bars(self.data_manager.results)
            self._embed_figure(fig)
        except Exception as e:
            logger.error(f"Erro ao criar gráfico: {e}")
            messagebox.showerror("Erro", f"Falha ao criar gráfico: {str(e)}")
    
    def _show_economic_chart(self, metrics: Dict) -> None:
        """Mostra gráficos econômicos"""
        try:
            fig = self.chart_gen.create_economic_analysis(metrics)
            self._embed_figure(fig)
        except Exception as e:
            logger.error(f"Erro ao criar gráfico econômico: {e}")
            messagebox.showerror("Erro", str(e))
    
    def _embed_figure(self, fig: plt.Figure) -> None:
        """Embeds matplotlib figure em Tkinter"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _export_results(self) -> None:
        """Exporta resultados"""
        if not self.data_manager.results:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("All", "*.*")]
        )
        
        if filepath:
            try:
                self.data_manager.export_to_excel(filepath, self.data_manager.results)
                messagebox.showinfo("Sucesso", f"Exportado para {filepath}")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
    
    def _new_project(self) -> None:
        """Novo projeto"""
        if self.data_manager.reservoirs:
            if messagebox.askyesno("Novo", "Descartar dados atuais?"):
                self.data_manager.clear()
                self._clear_interface()
    
    def _update_status(self, message: str) -> None:
        """Atualiza barra de status"""
        self.status_bar.config(text=f"{message} | {datetime.now().strftime('%H:%M:%S')}")
        self.root.update_idletasks()
    
    def _update_data_tree(self) -> None:
        """Atualiza tabela de dados"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for r in self.data_manager.reservoirs:
            self.data_tree.insert("", tk.END, values=(
                r.get("ID", ""),
                r.get("API", ""),
                r.get("Viscosidade", ""),
                r.get("Profundidade", ""),
                "✓"
            ))
    
    def _update_results_tree(self, scores: Dict) -> None:
        """Atualiza tabela de resultados"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        for method, data in sorted(
            scores.items(), 
            key=lambda x: x[1]["score"], 
            reverse=True
        ):
            self.results_tree.insert("", tk.END, values=(
                method,
                f"{data['score']:.1f}%",
                data["status"],
                data["suitability"]
            ))
    
    def _clear_interface(self) -> None:
        """Limpa interface"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
    def run(self) -> None:
        """Inicia a aplicação"""
        self.root.mainloop()

# ============================================================================
# PONTO DE ENTRADA
# ============================================================================
def main():
    """Função principal"""
    try:
        # Verificar dependências
        required = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'openpyxl']
        missing = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        
        if missing:
            print(f"Faltam dependências: {', '.join(missing)}")
            print(f"Instale com: pip install {' '.join(missing)}")
            return
        
        logger.info("=" * 60)
        logger.info("INICIANDO PETROCHAMP v5.0")
        logger.info("=" * 60)
        
        app = PetroChampUI()
        app.run()
        
    except Exception as e:
        logger.critical(f"Erro crítico: {e}", exc_info=True)
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar: {str(e)}")

if __name__ == "__main__":
    main()
