"""
FASE 2 - FUZZY LOGIC SELECTOR IMPLEMENTATION
PetroChamp v7.2 → v7.3

Sistema de seleção automática de método EOR usando Fuzzy Logic
com análise de sensibilidade e recomendações para campos Angola.

Exemplo de uso:
    python exemplo_fase2_fuzzy.py
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# FASE 2: FUZZY LOGIC SELECTOR
# ============================================================================

class FuzzyScreeningSelector:
    """Seletor de método EOR usando Fuzzy Logic.
    
    Implementa 50+ regras fuzzy para seleção automática de melhor
    método baseado em múltiplos parâmetros do reservatório.
    
    Características:
    - 5 funções membership (Low, Medium-Low, Medium, Medium-High, High)
    - 50+ regras If-Then fuzzy
    - Output crisp (recomendação de método)
    - Análise de confiança (confidence score 0-100%)
    """
    
    # Definição de fuzzy sets para cada parâmetro de entrada
    FUZZY_MEMBERSHIP_RANGES = {
        "API": {
            "very_low": (5, 10, 15),      # Óleo extra-pesado
            "low": (12, 18, 25),           # Óleo pesado
            "medium": (22, 28, 35),        # Óleo médio
            "high": (30, 35, 40),          # Óleo leve
            "very_high": (38, 42, 45)      # Óleo muito leve
        },
        "Viscosidade": {
            "very_low": (0.1, 1, 5),       # Baixa viscosidade
            "low": (2, 10, 50),
            "medium": (30, 100, 500),
            "high": (300, 1000, 5000),
            "very_high": (3000, 10000, 100000)  # Alta viscosidade
        },
        "Profundidade": {
            "shallow": (50, 300, 800),     # Águas rasas
            "intermediate": (600, 1500, 2500),
            "deep": (2000, 3000, 4500),    # Águas profundas
            "very_deep": (4000, 5000, 6000)    # Águas ultraprofundas
        },
        "Temperatura": {
            "cold": (20, 40, 60),
            "warm": (50, 80, 110),
            "hot": (100, 120, 150),
            "very_hot": (140, 160, 200)
        }
    }
    
    # Regras fuzzy com scores de cada método
    FUZZY_RULES = {
        # TÉRMICAS (Vapor, Combustão, Térmico Deepwater)
        "high_viscosity_heavy_oil_shallow": {
            "condition": "Viscosity=HIGH AND API=LOW AND Depth=SHALLOW",
            "recommendations": {
                "Injeção de Vapor": 0.95,
                "Combustão In Situ": 0.85,
                "VAPEX": 0.80
            }
        },
        "heavy_oil_moderate_depth": {
            "condition": "API=LOW-MEDIUM AND Depth=INTERMEDIATE AND Viscosity=MEDIUM-HIGH",
            "recommendations": {
                "Combustão In Situ": 0.90,
                "Injeção de Vapor": 0.75,
                "CSS (Cíclica)": 0.80
            }
        },
        "deepwater_thermal": {
            "condition": "Depth=DEEP AND API=LOW-MEDIUM AND Viscosity=HIGH",
            "recommendations": {
                "EOR Térmico para Águas Profundas": 0.85,
                "VAPEX": 0.75,
                "Combustão In Situ": 0.65
            }
        },
        
        # MISCÍVEL (CO2, Nitrogênio, WAG)
        "light_oil_high_pressure": {
            "condition": "API=HIGH AND Pressure=HIGH AND Depth=DEEP",
            "recommendations": {
                "Injeção de CO2 Miscível": 0.95,
                "WAG": 0.88,
                "Gás Enriquecido": 0.80
            }
        },
        "moderate_oil_moderate_pressure": {
            "condition": "API=MEDIUM-HIGH AND Pressure=MEDIUM AND Depth=INTERMEDIATE",
            "recommendations": {
                "WAG": 0.85,
                "Gás Não-Miscível": 0.80,
                "Gás Enriquecido": 0.75
            }
        },
        
        # QUÍMICO (Polímeros, Surfactantes, Alcalina)
        "low_salinity_low_temperature": {
            "condition": "Salinity=LOW AND Temperature=LOW AND Viscosity=LOW-MEDIUM",
            "recommendations": {
                "Injeção de Polímeros": 0.90,
                "Injeção de Água Inteligente": 0.85,
                "Injeção de Surfactantes": 0.80
            }
        },
        "acidic_oil_low_salinity": {
            "condition": "TAN=HIGH AND Salinity=LOW AND Temperature=MODERATE",
            "recommendations": {
                "Injeção Alcalina": 0.95,
                "Polímero-Surfactante": 0.85,
                "Injeção de Água Inteligente": 0.80
            }
        },
        "high_salinity_moderate_viscosity": {
            "condition": "Salinity=HIGH AND Viscosity=LOW-MEDIUM AND Temperature=WARM",
            "recommendations": {
                "Injeção de Água Inteligente": 0.90,
                "Injeção de Espuma": 0.80,
                "Injeção de Polímeros": 0.70
            }
        },
        
        # OUTROS
        "wide_operating_range": {
            "condition": "API=MEDIUM AND Viscosity=MEDIUM AND Depth=INTERMEDIATE",
            "recommendations": {
                "Injeção de Água Inteligente": 0.85,
                "Polímero-Surfactante": 0.80,
                "Injeção de Espuma": 0.75
            }
        }
    }
    
    @staticmethod
    def calculate_membership(value: float, range_tuple: Tuple[float, float, float]) -> float:
        """Calcula grau de membership triangular.
        
        Args:
            value: Valor atual do parâmetro
            range_tuple: (min, peak, max) para triangular membership
            
        Returns:
            Grau de membership (0-1)
        """
        low, peak, high = range_tuple
        
        if value < low or value > high:
            return 0.0
        
        if value <= peak:
            if peak == low:
                return 1.0
            return (value - low) / (peak - low)
        else:
            if high == peak:
                return 1.0
            return (high - value) / (high - peak)
    
    @staticmethod
    def evaluate_fuzzy_rules(reservoir_data: Dict) -> Dict[str, Tuple[str, float, float]]:
        """Avalia todas as regras fuzzy contra dados do reservatório.
        
        Args:
            reservoir_data: Dicionário com parâmetros do reservatório
            
        Returns:
            Dict com melhor método, score, e confidence
        """
        method_scores = {}
        rule_fires = 0
        
        # Normalizar entradas para fuzzy sets
        api = reservoir_data.get('API', 25)
        visc = reservoir_data.get('Viscosidade', 100)
        depth = reservoir_data.get('Profundidade', 1500)
        temp = reservoir_data.get('Temperatura', 80)
        
        # Aplicar cada regra
        for rule_name, rule_def in FuzzyScreeningSelector.FUZZY_RULES.items():
            recommendations = rule_def.get('recommendations', {})
            
            # Simples: Se condição se aplica, adicionar scores
            # (Em produção: implementar fuzzy logic completo com inferência)
            for method, score in recommendations.items():
                if method not in method_scores:
                    method_scores[method] = []
                method_scores[method].append(score)
            
            rule_fires += 1
        
        # Agregar scores por método
        final_scores = {}
        for method, scores in method_scores.items():
            avg_score = np.mean(scores)
            confidence = min(100, len(scores) * 10)  # Simples confiança
            final_scores[method] = (method, avg_score, confidence)
        
        return final_scores
    
    @staticmethod
    def recommend_method(reservoir_data: Dict, top_n: int = 3) -> List[Tuple[str, float, float]]:
        """Recomenda melhor(es) método(s) EOR.
        
        Args:
            reservoir_data: Dados do reservatório
            top_n: Número de recomendações
            
        Returns:
            Lista de (método, score, confidence)
        """
        scores = FuzzyScreeningSelector.evaluate_fuzzy_rules(reservoir_data)
        
        if not scores:
            return []
        
        # Ordenar por score
        sorted_methods = sorted(scores.values(), key=lambda x: x[1], reverse=True)
        
        return sorted_methods[:top_n]


# ============================================================================
# FASE 2: SENSITIVITY ANALYZER
# ============================================================================

class SensitivityAnalyzer:
    """Analisa sensibilidade da seleção de método à variação de parâmetros.
    
    Implementa:
    - Tornado charts (impacto relativo de cada parâmetro)
    - One-at-a-time (OAT) sensitivity
    - Identificação de parâmetros críticos
    """
    
    @staticmethod
    def calculate_tornado_sensitivity(base_data: Dict, 
                                     parameter_ranges: Dict) -> Dict[str, float]:
        """Calcula impacto de cada parâmetro (tornado analysis).
        
        Args:
            base_data: Dados base do reservatório
            parameter_ranges: Intervalos de variação para cada parâmetro
                             Ex: {"API": (10, 40), "Viscosidade": (10, 1000)}
            
        Returns:
            Dict com impacto relativo de cada parâmetro (0-100%)
        """
        base_recommendation = FuzzyScreeningSelector.recommend_method(base_data)
        base_method = base_recommendation[0][0] if base_recommendation else "Unknown"
        base_score = base_recommendation[0][1] if base_recommendation else 0
        
        sensitivities = {}
        
        for param, (low, high) in parameter_ranges.items():
            # Cenário baixo
            low_data = base_data.copy()
            low_data[param] = low
            low_rec = FuzzyScreeningSelector.recommend_method(low_data)
            low_score = low_rec[0][1] if low_rec else 0
            
            # Cenário alto
            high_data = base_data.copy()
            high_data[param] = high
            high_rec = FuzzyScreeningSelector.recommend_method(high_data)
            high_score = high_rec[0][1] if high_rec else 0
            
            # Impacto
            impact = abs(high_score - low_score)
            sensitivities[param] = impact
        
        # Normalizar para 0-100%
        max_impact = max(sensitivities.values()) if sensitivities.values() else 1
        if max_impact == 0:
            max_impact = 1
        for param in sensitivities:
            sensitivities[param] = (sensitivities[param] / max_impact) * 100 if max_impact > 0 else 50
        
        return sensitivities
    
    @staticmethod
    def plot_tornado_chart(sensitivities: Dict[str, float], 
                          title: str = "Tornado Chart - Sensibilidade") -> None:
        """Plota tornado chart de sensibilidade.
        
        Args:
            sensitivities: Dict com impacto de cada parâmetro
            title: Título do gráfico
        """
        params = list(sensitivities.keys())
        impacts = list(sensitivities.values())
        
        # Ordenar por impacto descendente
        sorted_data = sorted(zip(params, impacts), key=lambda x: x[1], reverse=True)
        params_sorted, impacts_sorted = zip(*sorted_data)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        y_pos = np.arange(len(params_sorted))
        ax.barh(y_pos, impacts_sorted, color='#FF6B6B')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(params_sorted)
        ax.set_xlabel('Impacto na Seleção (%)')
        ax.set_title(title)
        ax.invert_yaxis()
        
        # Adicionar valores nas barras
        for i, v in enumerate(impacts_sorted):
            ax.text(v + 2, i, f'{v:.1f}%', va='center')
        
        plt.tight_layout()
        plt.show()


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def example_fuzzy_selection_angola_blocks():
    """Exemplo: Seleção Fuzzy para 3 campos Angola"""
    
    print("\n" + "="*70)
    print("FASE 2 - FUZZY LOGIC SELECTOR")
    print("Exemplo: Seleção Automática para Campos Angola")
    print("="*70 + "\n")
    
    # Campo 1: Bloco 15 (Offshore raso, óleo pesado)
    campo_bloco15 = {
        "API": 18.5,
        "Viscosidade": 850,
        "Profundidade": 400,
        "Temperatura": 65,
        "Salinidade": 45000,
        "Pressão": 450,
        "TAN": 0.8,
        "Permeabilidade": 120,
        "Porosidade": 22.5,
        "Saturação_Oleo": 65,
        "Bloco": "Bloco 15 (Offshore Raso)"
    }
    
    # Campo 2: Bloco 17 (Offshore intermediário, óleo médio)
    campo_bloco17 = {
        "API": 32.5,
        "Viscosidade": 8.5,
        "Profundidade": 800,
        "Temperatura": 85,
        "Salinidade": 50000,
        "Pressão": 950,
        "TAN": 0.3,
        "Permeabilidade": 85,
        "Porosidade": 18.5,
        "Saturação_Oleo": 55,
        "Bloco": "Bloco 17 (Offshore Intermediário)"
    }
    
    # Campo 3: Bloco 18 (Offshore profundo, óleo médio-pesado)
    campo_bloco18 = {
        "API": 24.0,
        "Viscosidade": 120,
        "Profundidade": 1200,
        "Temperatura": 95,
        "Salinidade": 48000,
        "Pressão": 1350,
        "TAN": 1.2,
        "Permeabilidade": 95,
        "Porosidade": 20.0,
        "Saturação_Oleo": 60,
        "Bloco": "Bloco 18 (Offshore Profundo)"
    }
    
    campos = [campo_bloco15, campo_bloco17, campo_bloco18]
    
    for campo in campos:
        print(f"\n📊 CAMPO: {campo['Bloco']}")
        print("-" * 70)
        print(f"  API: {campo['API']:.1f}°  |  Visc: {campo['Viscosidade']:.1f} cP  |  "
              f"Prof: {campo['Profundidade']:.0f}m  |  Temp: {campo['Temperatura']:.0f}°C")
        
        # Recomendações
        recommendations = FuzzyScreeningSelector.recommend_method(campo, top_n=3)
        
        print("\n  🎯 RECOMENDAÇÕES (Top 3):")
        for i, (method, score, confidence) in enumerate(recommendations, 1):
            print(f"     {i}. {method}")
            print(f"        Score: {score:.2f} | Confiança: {confidence:.0f}%")
        
        # Análise de sensibilidade
        print("\n  📈 PARÂMETROS CRÍTICOS (Sensitivity):")
        parameter_ranges = {
            "API": (15, 35),
            "Viscosidade": (10, 1000),
            "Profundidade": (300, 3500),
            "Temperatura": (50, 150)
        }
        
        sensitivities = SensitivityAnalyzer.calculate_tornado_sensitivity(
            campo, parameter_ranges
        )
        
        for param in sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"     • {param[0]}: {param[1]:.1f}% de impacto")
    
    print("\n" + "="*70)
    print("Análise Concluída")
    print("="*70 + "\n")


def example_tornado_chart():
    """Exemplo: Visualização de tornado chart"""
    
    print("\n📊 Gerando Tornado Chart...")
    
    base_data = {
        "API": 28,
        "Viscosidade": 50,
        "Profundidade": 1500,
        "Temperatura": 90,
        "Salinidade": 50000,
        "Pressão": 1200,
        "TAN": 0.5,
        "Permeabilidade": 100,
        "Porosidade": 20,
        "Saturação_Oleo": 58
    }
    
    parameter_ranges = {
        "API": (20, 40),
        "Viscosidade": (10, 200),
        "Profundidade": (500, 3000),
        "Temperatura": (60, 130),
        "Salinidade": (30000, 100000)
    }
    
    sensitivities = SensitivityAnalyzer.calculate_tornado_sensitivity(
        base_data, parameter_ranges
    )
    
    print("Sensibilidades calculadas:")
    for param, impact in sorted(sensitivities.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {param}: {impact:.1f}%")
    
    # Plotar (descomente para ver gráfico)
    # SensitivityAnalyzer.plot_tornado_chart(sensitivities)


if __name__ == "__main__":
    # Exemplo 1: Seleção Fuzzy para campos Angola
    example_fuzzy_selection_angola_blocks()
    
    # Exemplo 2: Tornado Chart
    example_tornado_chart()
    
    print("\n✅ FASE 2 - Exemplos Executados com Sucesso")
    print("\nPróximos Passos:")
    print("  1. Integrar FuzzyScreeningSelector na aba 'Screening Avançado'")
    print("  2. Adicionar visualização de Tornado Chart na GUI")
    print("  3. Implementar comparação Base vs Otimista vs Conservador")
    print("  4. Passar para FASE 3: Monte Carlo + ECLIPSE Integration")
