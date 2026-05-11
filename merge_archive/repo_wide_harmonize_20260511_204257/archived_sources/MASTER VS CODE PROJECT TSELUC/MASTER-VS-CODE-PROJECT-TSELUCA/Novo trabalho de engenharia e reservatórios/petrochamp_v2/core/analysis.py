"""
Módulo de análise avançada: sensibilidade, otimização e recomendações
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


@dataclass
class SensitivityMetric:
    """Métrica de sensibilidade de um parâmetro"""
    parameter: str
    baseline_value: float
    sensitivity_index: float
    impact_on_npv: float
    impact_classification: str  # "Low", "Medium", "High", "Critical"


class SensitivityAnalyzer:
    """Análise avançada de sensibilidade multivariada"""
    
    def __init__(self):
        self.results = {}
        self.methods = ['oat', 'tornado', 'monte_carlo', 'sobol']
    
    def analyze_one_at_a_time(self, 
                             base_case: Dict[str, float],
                             parameter_ranges: Dict[str, Tuple[float, float]],
                             objective_function: Callable,
                             steps: int = 10) -> pd.DataFrame:
        """
        Análise One-At-a-Time (OAT)
        
        Varia um parâmetro por vez mantendo outros constantes
        """
        results = []
        
        for param_name, (min_val, max_val) in parameter_ranges.items():
            if param_name not in base_case:
                continue
            
            # Variação linear do parâmetro
            values = np.linspace(min_val, max_val, steps)
            outputs = []
            
            for value in values:
                test_case = base_case.copy()
                test_case[param_name] = value
                
                try:
                    output = objective_function(test_case)
                    outputs.append(output)
                except Exception as e:
                    logger.warning(f"Erro ao avaliar {param_name}={value}: {e}")
                    outputs.append(np.nan)
            
            # Calcular sensibilidade
            outputs = np.array(outputs)
            valid_outputs = outputs[~np.isnan(outputs)]
            
            if len(valid_outputs) > 0:
                sensitivity = (np.nanmax(outputs) - np.nanmin(outputs)) / np.nanmean(outputs) if np.nanmean(outputs) != 0 else 0
                
                results.append({
                    'parameter': param_name,
                    'min_output': np.nanmin(outputs),
                    'max_output': np.nanmax(outputs),
                    'baseline_output': objective_function(base_case),
                    'sensitivity': sensitivity,
                    'range': max_val - min_val
                })
        
        df = pd.DataFrame(results)
        df = df.sort_values('sensitivity', ascending=False)
        
        return df
    
    def tornado_analysis(self,
                        base_case: Dict[str, float],
                        variations: Dict[str, Tuple[float, float]],
                        objective_function: Callable) -> Tuple[pd.DataFrame, plt.Figure]:
        """
        Análise Tornado - mostra impacto de cada parâmetro
        """
        results = []
        base_output = objective_function(base_case)
        
        for param, (low, high) in variations.items():
            # Caso baixo
            low_case = base_case.copy()
            low_case[param] = low
            low_output = objective_function(low_case)
            
            # Caso alto
            high_case = base_case.copy()
            high_case[param] = high
            high_output = objective_function(high_case)
            
            # Impacto (tornado mostra em relação ao base case)
            low_impact = low_output - base_output
            high_impact = high_output - base_output
            
            results.append({
                'parameter': param,
                'low_impact': low_impact,
                'high_impact': high_impact,
                'total_range': high_impact - low_impact
            })
        
        df = pd.DataFrame(results)
        df = df.sort_values('total_range', ascending=True)
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        y_pos = np.arange(len(df))
        ax.barh(y_pos, df['low_impact'], left=0, label='Impacto Baixo', color='#e74c3c')
        ax.barh(y_pos, df['high_impact'], left=0, label='Impacto Alto', color='#27ae60')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df['parameter'])
        ax.set_xlabel('Impacto no NPV ($)')
        ax.set_title('Análise Tornado - Sensibilidade dos Parâmetros')
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        return df, fig
    
    def monte_carlo_simulation(self,
                              base_case: Dict[str, float],
                              parameter_distributions: Dict[str, Dict[str, float]],
                              objective_function: Callable,
                              n_iterations: int = 1000) -> Dict[str, Any]:
        """
        Simulação de Monte Carlo para análise de risco
        
        parameter_distributions formato:
        {
            'param_name': {'type': 'normal', 'mean': 100, 'std': 10},
            'param_name': {'type': 'uniform', 'min': 50, 'max': 150}
        }
        """
        results = []
        
        for i in range(n_iterations):
            sample_case = base_case.copy()
            
            # Gerar amostras
            for param, dist_params in parameter_distributions.items():
                dist_type = dist_params.get('type', 'normal')
                
                if dist_type == 'normal':
                    value = np.random.normal(
                        dist_params['mean'],
                        dist_params['std']
                    )
                elif dist_type == 'uniform':
                    value = np.random.uniform(
                        dist_params['min'],
                        dist_params['max']
                    )
                elif dist_type == 'lognormal':
                    value = np.random.lognormal(
                        dist_params['mean'],
                        dist_params['std']
                    )
                else:
                    value = base_case.get(param, 0)
                
                sample_case[param] = value
            
            # Avaliar
            try:
                output = objective_function(sample_case)
                results.append(output)
            except Exception as e:
                logger.warning(f"Erro em iteração {i}: {e}")
        
        results = np.array(results)
        
        # Calcular estatísticas
        return {
            'mean': np.mean(results),
            'std': np.std(results),
            'p10': np.percentile(results, 10),
            'p50': np.percentile(results, 50),
            'p90': np.percentile(results, 90),
            'min': np.min(results),
            'max': np.max(results),
            'results': results
        }


class HybridEOROptimizer:
    """Otimização de combinações de métodos EOR híbridos"""
    
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.optimization_results = {}
    
    def find_optimal_combination(self,
                                reservoir_data: Dict[str, float],
                                economic_params: Dict[str, float],
                                constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Encontra combinação ótima de métodos EOR
        """
        if constraints is None:
            constraints = {}
        
        available_methods = self.plugin_manager.get_available_methods()
        
        # Gerar combinações (até 3 métodos)
        combinations = self._generate_combinations(available_methods, max_methods=3)
        
        best_combo = None
        best_score = -float('inf')
        all_combos = []
        
        for combo in combinations:
            # Verificar restrições
            if not self._check_constraints(combo, constraints):
                continue
            
            # Avaliar combinação
            score = self._evaluate_combination(combo, reservoir_data, economic_params)
            
            all_combos.append({
                'combination': combo,
                'score': score,
                'estimated_recovery': self._estimate_recovery(combo, reservoir_data),
                'required_investment': self._calculate_investment(combo, economic_params),
                'synergy_factor': self._calculate_synergy(combo)
            })
            
            if score > best_score:
                best_score = score
                best_combo = combo
        
        return {
            'best_combination': best_combo,
            'best_score': best_score,
            'all_combinations': sorted(all_combos, key=lambda x: x['score'], reverse=True)[:10]
        }
    
    def _generate_combinations(self, methods: List[str], max_methods: int = 3) -> List[List[str]]:
        """Gera todas as combinações viáveis de métodos"""
        from itertools import combinations
        all_combos = []
        
        for r in range(1, min(max_methods + 1, len(methods) + 1)):
            for combo in combinations(methods, r):
                all_combos.append(list(combo))
        
        return all_combos
    
    def _check_constraints(self, combination: List[str], constraints: Dict) -> bool:
        """Verifica se combinação atende restrições"""
        # Implementar lógica de restrições
        return True
    
    def _evaluate_combination(self, combination: List[str],
                             reservoir_data: Dict,
                             economic_params: Dict) -> float:
        """Avalia score de uma combinação"""
        score = 0.0
        
        for method in combination:
            plugin = self.plugin_manager.get_plugin(method)
            if plugin:
                score += plugin.calculate_suitability(reservoir_data) / len(combination)
        
        return score
    
    def _estimate_recovery(self, combination: List[str], reservoir_data: Dict) -> float:
        """Estima recuperação total da combinação"""
        total_recovery = 0.0
        
        for method in combination:
            plugin = self.plugin_manager.get_plugin(method)
            if plugin:
                recovery = plugin.estimate_recovery_factor(reservoir_data, {})
                total_recovery += recovery * 0.5  # Sinergia reduzida
        
        return min(total_recovery, 1.0)
    
    def _calculate_investment(self, combination: List[str], economic_params: Dict) -> float:
        """Calcula investimento total"""
        total_investment = 0.0
        
        for method in combination:
            plugin = self.plugin_manager.get_plugin(method)
            if plugin:
                params = plugin.get_economic_parameters()
                total_investment += params.get('capex_per_well', 0) * economic_params.get('num_wells', 10)
        
        return total_investment
    
    def _calculate_synergy(self, combination: List[str]) -> float:
        """Calcula fator de sinergia entre métodos"""
        if len(combination) == 1:
            return 1.0
        
        # Matriz de sinergia (exemplo)
        synergy_matrix = {
            ('Injeção de Vapor', 'Injeção de Polímeros'): 1.15,
            ('Injeção de CO2 Miscível', 'Injeção de Polímeros'): 1.10,
            # Adicionar mais combinações
        }
        
        # Buscar sinergia na matriz
        sorted_combo = tuple(sorted(combination))
        return synergy_matrix.get(sorted_combo, 1.0)


class IntelligentRecommender:
    """Sistema de recomendações baseado em histórico e similitude"""
    
    def __init__(self, plugin_manager, project_manager):
        self.plugin_manager = plugin_manager
        self.project_manager = project_manager
    
    def recommend(self, current_reservoir: Dict[str, float], 
                 similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Recomenda métodos baseado em casos históricos similares
        """
        recommendations = []
        
        # Obter casos históricos
        historical_cases = self._get_historical_cases()
        
        # Encontrar casos similares
        similar_cases = self._find_similar_cases(
            current_reservoir,
            historical_cases,
            similarity_threshold
        )
        
        # Analisar métodos bem-sucedidos em casos similares
        method_success_rates = {}
        
        for case in similar_cases:
            for result in case.get('screening_results', []):
                method = result['method_name']
                score = result['suitability_score']
                
                if method not in method_success_rates:
                    method_success_rates[method] = []
                
                method_success_rates[method].append(score)
        
        # Gerar recomendações
        for method, scores in method_success_rates.items():
            avg_score = np.mean(scores)
            success_rate = sum(1 for s in scores if s >= 70) / len(scores)
            
            if success_rate >= 0.6:  # Mínimo 60% de sucesso
                plugin = self.plugin_manager.get_plugin(method)
                if plugin:
                    current_score = plugin.calculate_suitability(current_reservoir)
                    
                    recommendations.append({
                        'method': method,
                        'current_suitability': current_score,
                        'historical_avg_score': avg_score,
                        'success_rate': success_rate,
                        'confidence': min(success_rate, current_score / 100),
                        'similar_cases_count': len(similar_cases),
                        'recommendation_reason': self._generate_reason(
                            method, success_rate, similar_cases
                        )
                    })
        
        return sorted(recommendations, 
                     key=lambda x: x['confidence'], 
                     reverse=True)
    
    def _get_historical_cases(self) -> List[Dict]:
        """Obtém casos históricos do project manager"""
        cases = []
        
        for project in self.project_manager.projects.values():
            if project.screening_results:
                cases.append({
                    'reservoir_data': project.reservoir_data.to_dict(),
                    'screening_results': [r.to_dict() for r in project.screening_results]
                })
        
        return cases
    
    def _find_similar_cases(self, target: Dict[str, float],
                           cases: List[Dict],
                           threshold: float) -> List[Dict]:
        """Encontra casos similares por características principais"""
        similar = []
        
        for case in cases:
            similarity = self._calculate_similarity(
                target,
                case['reservoir_data']
            )
            
            if similarity >= threshold:
                similar.append(case)
        
        return similar
    
    def _calculate_similarity(self, target: Dict, case: Dict) -> float:
        """Calcula similaridade entre dois reservatórios"""
        # Características principais
        features = ['api_gravity', 'viscosity', 'depth', 'temperature']
        
        similarities = []
        
        for feature in features:
            target_val = target.get(feature, 0)
            case_val = case.get(feature, 0)
            
            if target_val == 0 or case_val == 0:
                similarities.append(0.5)  # Valor neutra
            else:
                ratio = min(target_val, case_val) / max(target_val, case_val)
                similarities.append(ratio)
        
        return np.mean(similarities)
    
    def _generate_reason(self, method: str, success_rate: float, 
                        similar_cases: List[Dict]) -> str:
        """Gera explicação da recomendação"""
        return (
            f"Método {method} foi bem-sucedido em {len(similar_cases)} casos similares "
            f"com taxa de sucesso de {success_rate*100:.0f}%. "
            f"Suitability média em casos similares: {np.mean([c['screening_results'][0]['suitability_score'] for c in similar_cases if c['screening_results']]):.1f}%"
        )
