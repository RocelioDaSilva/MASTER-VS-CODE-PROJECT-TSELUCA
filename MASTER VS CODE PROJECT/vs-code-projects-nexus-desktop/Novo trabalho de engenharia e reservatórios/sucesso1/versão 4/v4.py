"""
ATUALIZAÇÃO DO PETROCHAMP - PLATAFORMA COMPLETA EOR COM JUSTIFICAÇÕES E GRÁFICOS DE SUITABILITY
===============================================================================================

Este código substitui a versão anterior pela nova plataforma completa com sistema de justificações
e gráficos de suitability para cada método EOR.

Para usar:
1. Salve este código como petrochamp_completo_suitability.py
2. Execute: python petrochamp_completo_suitability.py

NOVAS CARACTERÍSTICAS:
• Gráficos de suitability (adequabilidade) para cada método EOR
• Visualização radar/spider chart para comparação de métodos
• Dashboard de suitability com cores de semáforo
• Análise detalhada de parâmetros-chave por método
• Exportação de gráficos de suitability em alta resolução
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import seaborn as sns
import os
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Tentar importar numpy_financial para cálculo de IRR
try:
    import numpy_financial as npf
    HAS_NUMPY_FINANCIAL = True
except ImportError:
    HAS_NUMPY_FINANCIAL = False
    print("Aviso: numpy_financial não está instalado. Usando método alternativo para cálculo de IRR.")

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# MÓDULO DE GRÁFICOS DE SUITABILITY (ADEQUABILIDADE)
# ============================================================================
class SuitabilityVisualizer:
    """Gerador de gráficos de suitability para métodos EOR"""
    
    def __init__(self):
        self.colors = {
            'alta': '#27ae60',  # Verde
            'media': '#f39c12', # Laranja
            'baixa': '#e74c3c', # Vermelho
            'neutro': '#bdc3c7' # Cinza
        }
        
    def create_spider_chart(self, method_scores, title="Suitability EOR"):
        """Cria gráfico radar/spider para visualização de suitability"""
        
        # Preparar dados
        methods = list(method_scores.keys())
        scores = [method_scores[m]['score'] for m in methods]
        colors = [method_scores[m]['color'] for m in methods]
        
        # Mapear cores para valores hex
        color_map = {'green': '#27ae60', 'orange': '#f39c12', 'red': '#e74c3c'}
        bar_colors = [color_map.get(c, '#3498db') for c in colors]
        
        # Criar figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Gráfico 1: Barras horizontais
        y_pos = np.arange(len(methods))
        bars = ax1.barh(y_pos, scores, color=bar_colors, edgecolor='black')
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(methods)
        ax1.set_xlabel('Pontuação de Suitability (%)')
        ax1.set_title('Pontuação por Método')
        ax1.set_xlim([0, 100])
        
        # Adicionar valores nas barras
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax1.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{score:.1f}%', ha='left', va='center')
        
        # Adicionar linhas de referência
        ax1.axvline(x=80, color='green', linestyle='--', alpha=0.5, label='Alta (>80%)')
        ax1.axvline(x=60, color='orange', linestyle='--', alpha=0.5, label='Média (60-80%)')
        ax1.axvline(x=0, color='red', linestyle='--', alpha=0.5, label='Baixa (<60%)')
        ax1.legend()
        
        # Gráfico 2: Radar para top 3 métodos
        top_methods = sorted(method_scores.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        
        if len(top_methods) >= 3:
            # Criar dados para radar
            categories = ['Técnico', 'Econômico', 'Operacional', 'Ambiental', 'Risco']
            
            # Valores simulados para cada dimensão
            values = []
            for method, data in top_methods:
                score = data['score']
                # Distribuir pontuação nas categorias (simulado)
                if score >= 80:
                    vals = [score*0.9, score*1.1, score*0.95, score*0.85, score*0.8]
                elif score >= 60:
                    vals = [score*0.8, score*0.9, score*0.7, score*0.6, score*0.5]
                else:
                    vals = [score*0.7, score*0.6, score*0.5, score*0.4, score*0.3]
                values.append([min(v, 100) for v in vals])
            
            # Configurar ângulos
            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]
            
            # Plotar radar
            ax2 = plt.subplot(122, polar=True)
            for i, (method, data) in enumerate(top_methods):
                val = values[i]
                val += val[:1]
                ax2.plot(angles, val, linewidth=2, linestyle='solid', 
                        label=method[:15] + '...' if len(method) > 15 else method)
                ax2.fill(angles, val, alpha=0.1)
            
            # Configurar radar
            ax2.set_theta_offset(np.pi / 2)
            ax2.set_theta_direction(-1)
            ax2.set_thetagrids(np.degrees(angles[:-1]), categories)
            ax2.set_ylim(0, 100)
            ax2.set_title('Análise Multidimensional - Top 3 Métodos')
            ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def create_suitability_matrix(self, reservoir_data, criteria_scores):
        """Cria matriz de suitability para todos os parâmetros"""
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Preparar dados para heatmap
        methods = list(criteria_scores.keys())
        parameters = set()
        for method_scores in criteria_scores.values():
            parameters.update(method_scores.keys())
        
        parameters = sorted(list(parameters))
        
        # Criar matriz
        matrix = np.zeros((len(parameters), len(methods)))
        
        for j, method in enumerate(methods):
            for i, param in enumerate(parameters):
                if param in criteria_scores[method]:
                    # Score baseado na adequação do parâmetro
                    if criteria_scores[method][param] > 0:
                        matrix[i, j] = 1  # Adequado
                    else:
                        matrix[i, j] = -1  # Não adequado
                else:
                    matrix[i, j] = 0  # Não avaliado
        
        # Criar heatmap
        cmap = plt.cm.RdYlGn
        im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=-1, vmax=1)
        
        # Configurar eixos
        ax.set_xticks(np.arange(len(methods)))
        ax.set_yticks(np.arange(len(parameters)))
        ax.set_xticklabels([m[:15] + '...' if len(m) > 15 else m for m in methods], 
                          rotation=45, ha='right')
        ax.set_yticklabels(parameters)
        
        # Adicionar valores na matriz
        for i in range(len(parameters)):
            for j in range(len(methods)):
                value = matrix[i, j]
                text = "✓" if value > 0 else "✗" if value < 0 else "-"
                color = "white" if abs(value) > 0.5 else "black"
                ax.text(j, i, text, ha="center", va="center", color=color, 
                       fontweight='bold' if text != "-" else 'normal')
        
        ax.set_title("Matriz de Adequabilidade - Parâmetros vs Métodos", 
                    fontweight='bold', pad=20)
        plt.colorbar(im, ax=ax, ticks=[-1, 0, 1], 
                    label='Adequabilidade: ✗=Baixa, -=Não avaliado, ✓=Alta')
        
        plt.tight_layout()
        
        return fig
    
    def create_parameter_radar(self, method_name, method_data, reservoir_data):
        """Cria radar chart específico para um método"""
        
        # Obter critérios específicos do método
        from eor_screening import EORScreeningEngine
        engine = EORScreeningEngine()
        criteria = engine.criteria.get(method_name, {})
        
        if not criteria:
            return None
        
        # Preparar dados
        categories = list(criteria.keys())
        N = len(categories)
        
        if N < 3:
            # Se poucas categorias, usar gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 6))
            
            scores = []
            for param in categories:
                if param in method_data.get('criteria_scores', {}):
                    scores.append(method_data['criteria_scores'][param])
                else:
                    scores.append(0)
            
            bars = ax.barh(categories, scores, color=self.colors['media'])
            ax.set_xlim(0, 100)
            ax.set_xlabel('Adequabilidade (%)')
            ax.set_title(f'Análise de Parâmetros - {method_name}')
            
            # Adicionar valores
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                       f'{score:.0f}%', va='center')
            
            return fig
        
        # Radar chart para 3+ categorias
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Valores
        values = []
        for param in categories:
            if param in method_data.get('criteria_scores', {}):
                values.append(method_data['criteria_scores'][param])
            else:
                values.append(0)
        values += values[:1]
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        # Plotar
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.25)
        
        # Configurar
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        
        # Adicionar linhas de referência
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
        
        ax.set_title(f'Suitability por Parâmetro\n{method_name}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Adicionar score total
        ax.text(0.5, -0.1, f'Score Total: {method_data["score"]:.1f}%', 
               transform=ax.transAxes, ha='center', fontsize=12, 
               bbox=dict(boxstyle='round', facecolor=self.colors['media'], alpha=0.3))
        
        return fig
    
    def create_comparison_chart(self, method_scores):
        """Cria gráfico comparativo de suitability"""
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Análise Comparativa de Suitability', fontsize=16, fontweight='bold')
        
        # 1. Gráfico de barras coloridas por status
        methods = list(method_scores.keys())
        scores = [method_scores[m]['score'] for m in methods]
        colors = []
        for m in methods:
            if method_scores[m]['score'] >= 80:
                colors.append(self.colors['alta'])
            elif method_scores[m]['score'] >= 60:
                colors.append(self.colors['media'])
            else:
                colors.append(self.colors['baixa'])
        
        axes[0, 0].barh(methods, scores, color=colors, edgecolor='black')
        axes[0, 0].set_xlabel('Pontuação (%)')
        axes[0, 0].set_title('Suitability por Método')
        axes[0, 0].set_xlim(0, 100)
        
        # 2. Distribuição por categoria
        categories = {'Alta': 0, 'Média': 0, 'Baixa': 0}
        for data in method_scores.values():
            if data['score'] >= 80:
                categories['Alta'] += 1
            elif data['score'] >= 60:
                categories['Média'] += 1
            else:
                categories['Baixa'] += 1
        
        axes[0, 1].pie(categories.values(), labels=categories.keys(), 
                      autopct='%1.1f%%', colors=[self.colors['alta'], 
                                                self.colors['media'], 
                                                self.colors['baixa']])
        axes[0, 1].set_title('Distribuição por Categoria')
        
        # 3. Evolução acumulada
        sorted_scores = sorted(scores, reverse=True)
        cumulative = np.cumsum(sorted_scores) / np.sum(sorted_scores) * 100
        
        axes[1, 0].plot(range(1, len(sorted_scores) + 1), cumulative, 
                       marker='o', linewidth=2)
        axes[1, 0].set_xlabel('Número de Métodos (ordenados)')
        axes[1, 0].set_ylabel('Suitabilidade Acumulada (%)')
        axes[1, 0].set_title('Curva de Suitability Acumulada')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Heatmap de scores
        heatmap_data = np.array(scores).reshape(1, -1)
        im = axes[1, 1].imshow(heatmap_data, aspect='auto', cmap='RdYlGn', 
                              vmin=0, vmax=100)
        axes[1, 1].set_xticks(range(len(methods)))
        axes[1, 1].set_xticklabels([m[:10]+'...' if len(m) > 10 else m 
                                   for m in methods], rotation=90)
        axes[1, 1].set_yticks([])
        axes[1, 1].set_title('Mapa de Calor - Suitability')
        
        # Adicionar valores no heatmap
        for i in range(len(methods)):
            axes[1, 1].text(i, 0, f'{scores[i]:.0f}%', ha='center', va='center', 
                          color='black' if scores[i] < 50 else 'white', fontweight='bold')
        
        plt.colorbar(im, ax=axes[1, 1])
        plt.tight_layout()
        
        return fig

# ============================================================================
# MÓDULO DE TRIAGEM EOR AVANÇADA COM JUSTIFICAÇÕES COMPLETAS
# ============================================================================
class EORScreeningEngine:
    """Motor de triagem EOR com justificações em texto"""
    
    def __init__(self):
        self.criteria = self._load_criteria()
        self.methods = list(self.criteria.keys())
        self.justifications = self._load_justifications()
        self.suitability_viz = SuitabilityVisualizer()
        
    def _load_criteria(self):
        """Carrega critérios de triagem baseados em literatura"""
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
    
    def _load_justifications(self):
        """Carrega justificações em texto para cada método EOR"""
        return {
            "Injeção de Vapor": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Este método é altamente recomendado porque seu reservatório tem características ideais para injeção de vapor: "
                    "óleo pesado (API < 22°) com alta viscosidade (>100 cP) que responde bem ao calor. A profundidade adequada (150-1500m) permite contenção eficiente do vapor, "
                    "e a espessura da formação (>6m) maximiza a recuperação térmica. A saturação de óleo (>40%) garante volume suficiente para recuperação econômica. "
                    "A viscosidade reduz em até 1000x com aumento de temperatura, facilitando a produção."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - O método tem potencial mas apresenta algumas limitações. Seu reservatório tem boa viscosidade para tratamento térmico, "
                    "mas a profundidade/espessura podem reduzir a eficiência. A saturação de óleo é adequada, mas o custo energético deve ser analisado. "
                    "Recomenda-se estudo de viabilidade térmica detalhado para avaliar balanço energético e custos operacionais."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Este método não é recomendado porque seu reservatório não atende aos critérios básicos. "
                    "O óleo pode ser muito leve (API > 22°) para justificar o custo térmico, ou a profundidade/espessura podem causar perdas excessivas de calor (>30%). "
                    "A saturação de óleo pode ser insuficiente (<40%) para recuperação econômica. Custo de vapor pode exceder US$ 15/bbl."
                )
            },
            "Combustão In Situ": {
                "alta": (
                    "🟢 ALTA SUITABILITY - A combustão in situ é recomendada devido às características ideais do seu reservatório: "
                    "óleo com viscosidade adequada (50-10,000 cP) para sustentar a combustão, boa permeabilidade (>50 mD) para fluxo de ar, "
                    "e profundidade suficiente (>300m) para manutenção da pressão necessária. A espessura (>3m) permite propagação eficiente da frente de combustão. "
                    "Recuperação adicional pode atingir 15-25% do óleo original no lugar."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - O método apresenta potencial mas requer cuidados. A viscosidade do óleo permite combustão, "
                    "mas a permeabilidade/espessura podem limitar a propagação da frente de combustão. "
                    "Recomenda-se estudo detalhado de viabilidade incluindo testes de ignição e análise de composição de gases."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado devido a características inadequadas. O óleo pode ser muito leve (API > 25°) ou muito viscoso (>10,000 cP), "
                    "a permeabilidade pode ser insuficiente (<50 mD) para fluxo de ar, ou a profundidade pode ser excessiva. "
                    "O controle da combustão seria difícil nas condições atuais. Risco de não ignição ou combustão incompleta."
                )
            },
            "Injeção de CO2 Miscível": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente candidato para CO2 miscível! Seu reservatório tem óleo leve (API > 27°) que se mistura bem com CO2, "
                    "pressão (>1200 psi) e profundidade (>800m) adequadas para alcançar miscibilidade, e temperatura (<120°C) dentro dos limites operacionais. "
                    "A salinidade (<100,000 ppm) também é compatível com a injeção de CO2. MMP (Minimum Miscibility Pressure) provavelmente alcançável. "
                    "Recuperação adicional estimada em 10-20% do óleo original."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial moderado para CO2 miscível. O óleo tem características aceitáveis, "
                    "mas a pressão ou temperatura podem estar nos limites. A salinidade pode exigir tratamentos adicionais. "
                    "Recomenda-se estudo de viabilidade com análise de sourcing de CO2, cálculo preciso do MMP e avaliação de corrosividade."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para CO2 miscível. O óleo pode ser muito pesado (API < 27°) para miscibilidade, "
                    "a pressão do reservatório é insuficiente (<1200 psi), ou a profundidade não garante as condições necessárias. "
                    "A temperatura (>120°C) ou salinidade alta (>100,000 ppm) podem causar problemas operacionais. MMP provavelmente não alcançável."
                )
            },
            "Injeção de Polímeros": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Ideal para injeção de polímeros! A viscosidade do óleo (<150 cP) e a salinidade da água (<20,000 ppm) estão dentro dos limites ideais, "
                    "a temperatura (<90°C) permite estabilidade do polímero, e a permeabilidade (10-5000 mD) é adequada para injeção sem plugging. "
                    "Saturação de água <50% favorece aumento da eficiência de varrimento. Polímeros HPAM podem aumentar a viscosidade da água em 10-50x."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para injeção de polímeros com algumas restrições. A salinidade ou temperatura podem estar nos limites superiores, "
                    "exigindo polímeros específicos (como copolímeros ou polímeros termorresistentes). A saturação de água pode reduzir a eficiência. "
                    "Estudo de compatibilidade necessário com testes de adsorção e degradação."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para polímeros. A salinidade muito alta (>20,000 ppm) degrada os polímeros rapidamente, "
                    "a temperatura excessiva (>90°C) causa degradação térmica, ou a permeabilidade é inadequada para injeção (plugging risk). "
                    "O pH pode estar fora da faixa de estabilidade (ideal 5-8). Custo do polímero pode exceder US$ 2-5/bbl."
                )
            },
            "Injeção de Surfactantes": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Perfeito para surfactantes! O reservatório tem baixa viscosidade do óleo (<30 cP), salinidade compatível (<10,000 ppm), "
                    "temperatura adequada (<80°C) para estabilidade química, e saturação residual de óleo (>25%) que justifica o custo dos surfactantes. "
                    "Permeabilidade >20 mD permite boa propagação. Tensão interfacial pode ser reduzida de 30 para 0.001 mN/m."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial moderado para surfactantes. Alguns parâmetros estão nos limites (salinidade, temperatura), "
                    "exigindo formulações específicas (surfactantes aniónicos-catiónicos mistos). A saturação de óleo residual pode limitar a recuperação adicional. "
                    "Estudo econômico necessário devido ao custo dos surfactantes (US$ 3-10/bbl)."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para surfactantes. A viscosidade do óleo pode ser muito alta (>30 cP), "
                    "a salinidade excessiva (>10,000 ppm) causa precipitação, ou a temperatura (>80°C) degrada os surfactantes rapidamente. "
                    "A saturação de óleo residual é muito baixa (<25%) para justificar o custo. Adsorção em rocha pode exceder 1 mg/g."
                )
            },
            "Injeção Alcalina": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente candidato para injeção alcalina! O óleo tem TAN adequado (>0.5 mg KOH/g) para reação e formação de sabões, "
                    "viscosidade dentro dos limites (<200 cP), salinidade compatível (<5,000 ppm), e permeabilidade suficiente (>20 mD) para fluxo da solução. "
                    "pH pode ser ajustado para 11-12 para otimizar a reação. Custo do agente alcalino é baixo (US$ 0.5-2/bbl)."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para injeção alcalina com ressalvas. O TAN está no limite mínimo (0.5 mg KOH/g), "
                    "a salinidade pode exigir ajustes na concentração, ou o pH precisa ser controlado para evitar precipitação. "
                    "Estudo de compatibilidade com a água formação necessário para evitar escalagem."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para injeção alcalina. O TAN é muito baixo (<0.5 mg KOH/g) para reação eficiente, "
                    "a salinidade muito alta (>5,000 ppm) consome rapidamente o agente alcalino, ou a permeabilidade é insuficiente (<20 mD). "
                    "A viscosidade do óleo (>200 cP) pode limitar a mobilização. Precipitação de carbonatos é risco significativo."
                )
            },
            "Injeção de Gás Não-Miscível": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Recomendado para injeção de gás não-miscível. O óleo tem API adequado (10-35°), viscosidade aceitável (<100 cP), "
                    "profundidade (>600m) e pressão (>800 psi) suficientes para manutenção do gás em fase desejada, e mergulho (>10°) que favorece a segregação gravitacional. "
                    "Gás natural ou gás de exaustão podem ser utilizados. Fator de recuperação adicional: 5-15%."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial moderado para injeção de gás. O óleo tem características razoáveis, "
                    "mas a profundidade ou pressão podem estar nos limites inferiores. O mergulho da formação pode limitar a eficiência do varrimento. "
                    "Recomenda-se estudo de simulação para avaliar sweep efficiency e risco de breakthrough prematuro."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para injeção de gás não-miscível. O óleo pode ter viscosidade muito alta (>100 cP), "
                    "a pressão do reservatório é insuficiente (<800 psi), ou falta mergulho (<10°) para segregação eficiente. "
                    "O risco de breakthrough prematuro do gás é alto (>50% em 2 anos). Baixa eficiência de varrimento vertical."
                )
            },
            "Injeção de Nitrogênio": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente candidato para injeção de nitrogênio! O reservatório tem óleo leve (API > 30°), "
                    "profundidade (>2000m) e pressão (>1500 psi) adequadas para manutenção do nitrogênio em fase gasosa, "
                    "e mergulho (>15°) que favorece a segregação gravitacional. A baixa viscosidade do óleo (<10 cP) permite mobilização eficiente. "
                    "Nitrogênio pode ser gerado in situ ou importado. Aplicável em reservatórios de alta pressão."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial moderado para injeção de nitrogênio. O óleo tem características aceitáveis, "
                    "mas a profundidade ou pressão podem estar nos limites. A temperatura pode afetar a eficiência (>150°C causa compressibilidade reduzida). "
                    "Recomenda-se estudo de viabilidade com análise de sourcing de N2 e compressão."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para injeção de nitrogênio. O óleo pode ser muito viscoso (>10 cP), "
                    "a profundidade é insuficiente (<2000m) para manter o nitrogênio em fase gasosa, "
                    "ou falta mergulho (<15°) para segregação gravitacional eficiente. Custo de compressão pode ser proibitivo."
                )
            },
            "Injeção de Gás Enriquecido": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Perfeito para injeção de gás enriquecido! O reservatório tem óleo com API ideal (>25°), "
                    "viscosidade baixa (<15 cP), pressão dentro da faixa de miscibilidade (1000-3000 psi), e temperatura compatível (<110°C). "
                    "A profundidade é adequada (>1000m) para alcançar condições de miscibilidade. Enriquecimento com C2-C6 melhora miscibilidade. "
                    "MMP reduzido em 20-40% comparado com CO2 puro."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para injeção de gás enriquecido. Alguns parâmetros estão nos limites, "
                    "exigindo ajustes na composição do gás (ótimização de enriquecimento). A pressão ou temperatura podem requerer monitoramento. "
                    "Estudo de composição do gás necessário para determinar MMP e custo de enriquecimento."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para injeção de gás enriquecido. O óleo pode ser muito pesado (API < 25°), "
                    "a pressão é insuficiente (<1000 psi) para miscibilidade, ou a temperatura está fora dos limites operacionais (>110°C). "
                    "O custo do gás enriquecido pode não ser justificado (US$ 2-5/Mscf). MMP muito alto para condições do reservatório."
                )
            },
            "Polímero-Surfactante": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Ideal para combinação polímero-surfactante! O reservatório tem viscosidade moderada (<100 cP), "
                    "salinidade compatível (<15,000 ppm), temperatura adequada (<85°C) e permeabilidade ideal (30-2000 mD) para os dois agentes. "
                    "A saturação residual de óleo (>30%) justifica o uso combinado. Sinergia reduz tensão interfacial e aumenta viscosidade simultaneamente. "
                    "Recuperação adicional pode alcançar 20-30% do óleo residual."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para combinação polímero-surfactante. A salinidade ou temperatura podem estar nos limites, "
                    "exigindo formulações específicas (surfactantes tolerantes a sal). A permeabilidade pode limitar a injeção simultânea. "
                    "Estudo de compatibilidade necessário para evitar separação de fase ou degradação."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para combinação polímero-surfactante. A salinidade muito alta (>15,000 ppm) degrada ambos agentes, "
                    "a temperatura excessiva (>85°C) causa instabilidade, ou a permeabilidade é inadequada (<30 mD plugging, >2000 mD channeling). "
                    "O custo da combinação pode não ser justificado (US$ 5-15/bbl). Interações químicas complexas."
                )
            },
            "VAPEX (Vapor Extraction)": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para VAPEX! O reservatório tem óleo pesado (API < 20°) e viscoso (1000-10,000 cP) ideal para extração por solventes, "
                    "profundidade adequada (>500m), boa permeabilidade (>100 mD) para fluxo do solvente, e espessura suficiente (>10m) para recuperação econômica. "
                    "Solventes como propano/butano reduzem viscosidade em 100-1000x. Aplicável em reservatórios onde steam injection não é viável."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para VAPEX. O óleo tem viscosidade adequada, mas a profundidade ou permeabilidade "
                    "podem limitar a eficiência. A espessura pode ser marginal (5-10m) para recuperação econômica. "
                    "Estudo de viabilidade necessário para seleção de solvente e análise de custo de solvente perdido."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para VAPEX. O óleo pode não ser suficientemente viscoso (<1000 cP), "
                    "a profundidade é excessiva (perdas de solvente), ou a permeabilidade é muito baixa (<100 mD) para fluxo adequado do solvente. "
                    "A espessura pode ser insuficiente (<5m). Custo de solvente pode exceder US$ 20/bbl."
                )
            },
            "Injeção de Água Inteligente": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Perfeito para água inteligente! O reservatório tem salinidade dentro da faixa ideal (5,000-50,000 ppm), "
                    "óleo com TAN adequado (>0.3 mg KOH/g) para alteração de molhabilidade, temperatura compatível (<120°C) e boa permeabilidade (>50 mD). "
                    "A viscosidade do óleo (<100 cP) permite mobilização eficiente. Modificação de íons (Ca2+, Mg2+, SO42-) altera molhabilidade de oleofílica para intermediária."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para água inteligente. A salinidade ou TAN podem estar nos limites, "
                    "exigindo ajustes na composição da água (otimização de íons). A temperatura pode afetar a eficiência (>120°C). "
                    "Estudo de composição necessário para determinar diluição/tratamento da água."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para água inteligente. A salinidade está fora da faixa efetiva (<5,000 ou >50,000 ppm), "
                    "o TAN é muito baixo (<0.3 mg KOH/g), ou a temperatura compromete a alteração de molhabilidade. "
                    "A permeabilidade pode ser insuficiente (<50 mD) para observação de efeitos. Tempo de resposta muito longo (>5 anos)."
                )
            },
            "Injeção de Espuma": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Ideal para injeção de espuma! O reservatório tem características perfeitas: "
                    "viscosidade moderada do óleo (<50 cP), salinidade compatível (<50,000 ppm), temperatura ideal (<90°C) para estabilidade da espuma, "
                    "permeabilidade adequada (100-3000 mD) e saturação de óleo dentro da faixa ótima (30-70%). "
                    "Espuma reduz mobilidade do gás em 10-100x, melhorando sweep efficiency. Aplicável para controle de conformance."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para injeção de espuma. Alguns parâmetros estão nos limites (salinidade, temperatura), "
                    "exigindo formulações específicas de surfactante (espumas estáveis). A saturação de óleo pode afetar a estabilidade da espuma. "
                    "Estudos de laboratório necessários para otimizar formulação e concentração."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para injeção de espuma. A salinidade muito alta (>50,000 ppm) destrói a espuma rapidamente, "
                    "a temperatura excessiva (>90°C) reduz a estabilidade, ou a permeabilidade é inadequada (<100 mD formação, >3000 mD colapso). "
                    "A saturação de óleo está fora da faixa ideal (<30% ou >70%). Custo do surfactante espumante é alto."
                )
            },
            "Aquecimento Elétrico": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para aquecimento elétrico! O reservatório tem óleo pesado (API < 18°) e viscoso (500-5000 cP) que responde bem ao aquecimento, "
                    "profundidade ideal (100-800m) para eficiência energética, boa permeabilidade (>50 mD) e espessura adequada (5-30m) para recuperação térmica. "
                    "Aquecimento por resistência ou RF pode aumentar temperatura em 50-200°C. Aplicável onde injeção de vapor não é possível."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para aquecimento elétrico. A viscosidade é adequada, mas a profundidade ou espessura "
                    "podem reduzir a eficiência energética (perdas para camadas adjacentes). A permeabilidade pode limitar a distribuição do calor. "
                    "Estudo de viabilidade elétrica necessário (consumo kW/h, custo de energia)."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para aquecimento elétrico. O óleo pode ser muito leve (API > 18°) para justificar o custo energético, "
                    "a profundidade é excessiva (>800m causando altas perdas), ou a espessura é inadequada (<5m recuperação econômica, >30m aquecimento não uniforme). "
                    "Custo energético pode exceder US$ 20/bbl."
                )
            },
            "Injeção Microbiana": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Perfeito para recuperação microbiana! O reservatório tem condições ideais para atividade microbiana: "
                    "temperatura dentro da faixa de sobrevivência (20-80°C), salinidade compatível (<100,000 ppm), permeabilidade adequada (>50 mD) para nutrientes "
                    "e pH dentro dos limites (5-9) para crescimento microbiano. Microrganismos producem surfactantes, polímeros, gases e ácidos in situ. "
                    "Custo baixo (US$ 0.5-2/bbl) e ambientalmente amigável."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para recuperação microbiana. A temperatura ou salinidade podem estar nos limites, "
                    "exigindo seleção de microrganismos específicos (extremófilos). O pH pode requerer ajustes. "
                    "Estudo de compatibilidade microbiana necessário para determinar nutrientes e tempo de incubação."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para recuperação microbiana. A temperatura é muito alta (>80°C) para sobrevivência microbiana, "
                    "a salinidade excessiva (>100,000 ppm) inibe o crescimento, ou o pH está fora da faixa de sobrevivência (<5 ou >9). "
                    "A permeabilidade pode limitar a distribuição de nutrientes (<50 mD). Tempo de resposta muito longo (>2 anos)."
                )
            }
        }
    
    def score_reservoir(self, reservoir_data):
        """Calcula pontuação para cada método EOR com justificações"""
        scores = {}
        
        for method, criteria in self.criteria.items():
            score = 0
            max_score = 0
            pontos_positivos = []
            pontos_negativos = []
            criteria_scores = {}  # Armazenar scores por critério para gráficos
            
            for param, limits in criteria.items():
                max_score += limits["peso"] * 100
                
                if param in reservoir_data and reservoir_data[param] is not None:
                    value = reservoir_data[param]
                    
                    if limits["min"] is not None and value < limits["min"]:
                        pontos_negativos.append(f"{param} ({value}) abaixo do mínimo ({limits['min']})")
                        criteria_scores[param] = 0
                    elif limits["max"] is not None and value > limits["max"]:
                        pontos_negativos.append(f"{param} ({value}) acima do máximo ({limits['max']})")
                        criteria_scores[param] = 0
                    else:
                        score += limits["peso"] * 100
                        pontos_positivos.append(f"{param} ({value}) dentro dos limites")
                        criteria_scores[param] = limits["peso"] * 100
                else:
                    pontos_negativos.append(f"Parâmetro {param} não disponível")
                    criteria_scores[param] = 0
            
            normalized_score = (score / max_score * 100) if max_score > 0 else 0
            
            if normalized_score >= 80:
                status = "RECOMENDADO"
                color = "green"
                justificativa = self.justifications[method]["alta"]
            elif normalized_score >= 60:
                status = "POTENCIAL"
                color = "orange"
                justificativa = self.justifications[method]["media"]
            else:
                status = "NÃO RECOMENDADO"
                color = "red"
                justificativa = self.justifications[method]["baixa"]
            
            scores[method] = {
                "score": normalized_score,
                "status": status,
                "color": color,
                "justificativa": justificativa,
                "pontos_positivos": pontos_positivos,
                "pontos_negativos": pontos_negativos,
                "criteria_scores": criteria_scores  # Para gráficos de suitability
            }
        
        return scores
    
    def get_recommendations(self, reservoir_data, top_n=3):
        """Retorna os top_n métodos recomendados"""
        scores = self.score_reservoir(reservoir_data)
        sorted_methods = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        return sorted_methods[:top_n]
    
    def generate_justification_report(self, reservoir_data, scores=None):
        """Gera relatório completo de justificações"""
        if scores is None:
            scores = self.score_reservoir(reservoir_data)
        
        report = []
        report.append("=" * 100)
        report.append("RELATÓRIO DE JUSTIFICAÇÕES E SUITABILITY - PETROCHAMP")
        report.append("=" * 100)
        report.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append("")
        
        # Ordenar por pontuação
        sorted_methods = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        
        for method, data in sorted_methods:
            report.append(f"\n{'-'*80}")
            report.append(f"MÉTODO: {method}")
            report.append(f"{'-'*80}")
            report.append(f"PONTUAÇÃO DE SUITABILITY: {data['score']:.1f}%")
            report.append(f"STATUS: {data['status']}")
            
            # Adicionar ícone de semáforo
            if data['score'] >= 80:
                report.append("🟢 SUITABILITY ALTA - Fortemente recomendado")
            elif data['score'] >= 60:
                report.append("🟡 SUITABILITY MÉDIA - Potencial com ressalvas")
            else:
                report.append("🔴 SUITABILITY BAIXA - Não recomendado")
            
            report.append("")
            report.append("JUSTIFICATIVA DETALHADA:")
            report.append(data['justificativa'])
            report.append("")
            
            # Resumo de suitability
            report.append("ANÁLISE DE SUITABILITY:")
            report.append(f"  • Score Técnico: {data['score']:.1f}%")
            report.append(f"  • Critérios atendidos: {len(data['pontos_positivos'])}/{len(data['criteria_scores'])}")
            
            if data['pontos_positivos']:
                report.append("\n  PONTOS FORTES:")
                for ponto in data['pontos_positivos'][:5]:  # Limitar a 5 principais
                    report.append(f"    ✓ {ponto}")
            
            if data['pontos_negativos']:
                report.append("\n  PONTOS A MELHORAR:")
                for ponto in data['pontos_negativos'][:5]:  # Limitar a 5 principais
                    report.append(f"    ✗ {ponto}")
            
            # Recomendação específica
            report.append("\n  RECOMENDAÇÃO ESPECÍFICA:")
            if data['score'] >= 80:
                report.append("    → Proceder com estudo detalhado de viabilidade")
                report.append("    → Considerar piloto ou implementação direta")
                report.append("    → Alto potencial de retorno econômico")
            elif data['score'] >= 60:
                report.append("    → Realizar estudos adicionais de laboratório")
                report.append("    → Considerar modificações no método")
                report.append("    → Avaliar risco técnico e econômico")
            else:
                report.append("    → Não recomendado para implementação")
                report.append("    → Considerar métodos alternativos")
                report.append("    → Reavaliar se novos dados estiverem disponíveis")
            
            report.append("")
        
        # Recomendação final com análise de suitability
        report.append(f"\n{'='*100}")
        report.append("ANÁLISE FINAL DE SUITABILITY:")
        
        best_method, best_data = sorted_methods[0]
        second_method, second_data = sorted_methods[1] if len(sorted_methods) > 1 else (None, None)
        third_method, third_data = sorted_methods[2] if len(sorted_methods) > 2 else (None, None)
        
        if best_data['score'] >= 80:
            report.append("🟢 CONCLUSÃO: Reservatório com ALTA SUITABILITY para EOR")
            report.append(f"   Método recomendado: {best_method} ({best_data['score']:.1f}%)")
            if second_method and second_data['score'] >= 80:
                report.append(f"   Método alternativo: {second_method} ({second_data['score']:.1f}%)")
        elif best_data['score'] >= 60:
            report.append("🟡 CONCLUSÃO: Reservatório com SUITABILITY MÉDIA para EOR")
            report.append(f"   Método com maior potencial: {best_method} ({best_data['score']:.1f}%)")
            report.append("   Recomenda-se estudo detalhado de viabilidade técnica e econômica")
        else:
            report.append("🔴 CONCLUSÃO: Reservatório com BAIXA SUITABILITY para EOR")
            report.append(f"   Melhor método: {best_method} ({best_data['score']:.1f}%)")
            report.append("   Considere técnicas de recuperação primária/secundária")
            report.append("   Ou reavalie com dados mais completos do reservatório")
        
        # Estatísticas
        alta = sum(1 for _, d in sorted_methods if d['score'] >= 80)
        media = sum(1 for _, d in sorted_methods if d['score'] >= 60 and d['score'] < 80)
        baixa = sum(1 for _, d in sorted_methods if d['score'] < 60)
        
        report.append(f"\nESTATÍSTICAS DE SUITABILITY:")
        report.append(f"  • Métodos com alta suitability (≥80%): {alta}/15")
        report.append(f"  • Métodos com suitability média (60-79%): {media}/15")
        report.append(f"  • Métodos com baixa suitability (<60%): {baixa}/15")
        
        return "\n".join(report)

# ============================================================================
# MÓDULO DE ANÁLISE ECONÔMICA (mantido igual)
# ============================================================================
class EconomicAnalyzer:
    """Analisador econômico para projetos EOR"""
    
    def __init__(self):
        self.default_params = {
            "oil_price": 60.0,
            "capex_multiplier": 5000,
            "opex_percentage": 30,
            "discount_rate": 10,
            "tax_rate": 25,
            "project_life": 15,
            "construction_time": 2,
            "decline_rate": 15
        }
    
    def calculate_cash_flow(self, production_profile, economic_params):
        """Calcula fluxo de caixa completo"""
        params = {**self.default_params, **economic_params}
        
        production = np.array(production_profile)
        revenue = production * params["oil_price"]
        
        total_capex = params.get("capex", production[0] * params["capex_multiplier"])
        capex_per_year = total_capex / params["construction_time"]
        
        opex = revenue * (params["opex_percentage"] / 100)
        operational_cf = revenue - opex
        
        years = len(production) + int(params["construction_time"])
        cash_flow = np.zeros(years)
        
        for i in range(int(params["construction_time"])):
            cash_flow[i] = -capex_per_year
        
        for i in range(len(production)):
            cash_flow[i + int(params["construction_time"])] = operational_cf[i]
        
        taxable_income = cash_flow.copy()
        taxable_income[taxable_income > 0] *= (1 - params["tax_rate"] / 100)
        
        return {
            "cash_flow": cash_flow.tolist(),
            "revenue": revenue.tolist(),
            "opex": opex.tolist(),
            "capex": total_capex,
            "years": years
        }
    
    def calculate_npv(self, cash_flow, discount_rate):
        """Calcula Valor Presente Líquido"""
        periods = np.arange(len(cash_flow), dtype=float)
        return np.sum(cash_flow / ((1 + discount_rate / 100) ** periods))
    
    def calculate_irr(self, cash_flow):
        """Calcula Taxa Interna de Retorno"""
        try:
            if HAS_NUMPY_FINANCIAL:
                irr_value = npf.irr(cash_flow)
                if irr_value is not None:
                    return irr_value * 100
                else:
                    return 0.0
            else:
                return self._calculate_irr_manual(cash_flow)
        except:
            return self._calculate_irr_manual(cash_flow)
    
    def _calculate_irr_manual(self, cash_flow):
        """Método manual para cálculo de IRR (bisseção)"""
        def npv_func(rate):
            periods = np.arange(len(cash_flow), dtype=float)
            return np.sum(cash_flow / ((1 + rate) ** periods))
        
        low, high = -0.99, 1.0
        max_iterations = 1000
        tolerance = 1e-6
        
        for _ in range(max_iterations):
            mid = (low + high) / 2
            val = npv_func(mid)
            
            if abs(val) < tolerance:
                return mid * 100
            
            if npv_func(low) * val < 0:
                high = mid
            else:
                low = mid
        
        return mid * 100
    
    def calculate_payback(self, cash_flow):
        """Calcula período de payback"""
        try:
            cumulative = np.cumsum(cash_flow)
            for i, val in enumerate(cumulative):
                if val >= 0:
                    if i == 0:
                        return 0.0
                    prev_val = cumulative[i-1]
                    year_fraction = abs(prev_val) / (val - prev_val) if (val - prev_val) != 0 else 0
                    return i - 1 + year_fraction
            return None
        except Exception as e:
            print(f"Erro no cálculo do payback: {e}")
            return None
    
    def generate_production_profile(self, initial_rate, decline_rate, years):
        """Gera perfil de produção com declínio"""
        profile = []
        years = int(years)
        for year in range(years):
            production = initial_rate * ((100 - decline_rate) / 100) ** year
            profile.append(production)
        return profile

# ============================================================================
# PLATAFORMA PRINCIPAL - PETROCHAMP PLATFORM COM JUSTIFICAÇÕES E SUITABILITY
# ============================================================================
class PetroChampPlatform:
    """Plataforma principal PetroChamp com sistema de justificações e suitability"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Configuração inicial
        self.root.title("PetroChamp - Plataforma de Triagem EOR com Justificações e Suitability")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Inicializar módulos
        self.screening_engine = EORScreeningEngine()
        self.economic_analyzer = EconomicAnalyzer()
        self.suitability_viz = SuitabilityVisualizer()
        
        # Estado da aplicação
        self.current_project = None
        self.reservoir_data = []
        self.screening_results = None
        self.economic_results = None
        self.justification_report = None
        
        # Configurar ícone e tema
        self._setup_styling()
        
        # Criar interface
        self._create_menu()
        self._create_main_interface()
        
    def _setup_styling(self):
        """Configura estilos e temas"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
        
        self.root.configure(bg=self.colors['light'])
        
    def _create_menu(self):
        """Cria barra de menu"""
        menubar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Novo Projeto", command=self.new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir Projeto", command=self.open_project, accelerator="Ctrl+O")
        file_menu.add_command(label="Salvar Projeto", command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Importar Dados", command=self.import_data)
        file_menu.add_command(label="Exportar Relatório", command=self.export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Análise
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Executar Triagem", command=self.run_screening)
        analysis_menu.add_command(label="Análise Econômica", command=self.run_economic_analysis)
        analysis_menu.add_command(label="Gerar Justificações", command=self.generate_justifications)
        analysis_menu.add_command(label="Gerar Gráficos Suitability", command=self.generate_suitability_charts)
        menubar.add_cascade(label="Análise", menu=analysis_menu)
        
        # Menu Visualização
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Gráfico de Pontuação", command=self.show_score_chart)
        view_menu.add_command(label="Visualizar Gráficos Econômicos", command=self.plot_economic_charts)
        view_menu.add_command(label="Dashboard Suitability", command=self.show_suitability_dashboard)
        menubar.add_cascade(label="Visualização", menu=view_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentação", command=self.show_documentation)
        help_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Atalhos de teclado
        self.root.bind('<Control-n>', lambda e: self.new_project())
        self.root.bind('<Control-o>', lambda e: self.open_project())
        self.root.bind('<Control-s>', lambda e: self.save_project())
        
    def _create_main_interface(self):
        """Cria interface principal com abas"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self._create_dashboard_tab()
        self._create_data_tab()
        self._create_screening_tab()
        self._create_economic_tab()
        self._create_results_tab()
        self._create_suitability_tab()  # Nova aba para gráficos de suitability
        
        self.status_bar = tk.Label(self.root, text="Pronto | PetroChamp Plataforma EOR com Suitability", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def _create_dashboard_tab(self):
        """Cria aba de dashboard"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        title_frame = ttk.Frame(self.dashboard_tab)
        title_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(title_frame, text="PetroChamp - Plataforma de Triagem EOR", 
                font=('Arial', 24, 'bold'), fg=self.colors['primary']).pack()
        
        tk.Label(title_frame, text="Versão completa com análise de suitability, 15 métodos EOR e sistema de justificações", 
                font=('Arial', 12), fg=self.colors['dark']).pack()
        
        cards_frame = ttk.Frame(self.dashboard_tab)
        cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.card1 = self._create_card(cards_frame, "📊 Dados do Reservatório", 
                                      "Carregue dados para análise", 0, 0)
        self.card2 = self._create_card(cards_frame, "🔍 Triagem EOR", 
                                      "Execute análise técnica", 0, 1)
        self.card3 = self._create_card(cards_frame, "📈 Suitability", 
                                      "Avalie adequabilidade", 1, 0)
        self.card4 = self._create_card(cards_frame, "💰 Análise Econômica", 
                                      "Avalie viabilidade financeira", 1, 1)
        
        actions_frame = ttk.LabelFrame(self.dashboard_tab, text="Ações Rápidas", padding=20)
        actions_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Button(actions_frame, text="Importar Dados CSV", 
                  command=self.import_csv, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Executar Análise Completa", 
                  command=self.run_complete_analysis, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Gerar Dashboard Suitability", 
                  command=self.generate_suitability_charts, width=25).pack(side=tk.LEFT, padx=5)
        
    def _create_card(self, parent, title, description, row, col):
        """Cria um card de dashboard"""
        card = ttk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        tk.Label(card, text=title, font=('Arial', 14, 'bold'), 
                fg=self.colors['primary']).pack(padx=20, pady=(20, 5))
        
        tk.Label(card, text=description, font=('Arial', 10), 
                fg=self.colors['dark']).pack(padx=20, pady=(0, 20))
        
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        return card
        
    def _create_data_tab(self):
        """Cria aba para entrada de dados"""
        self.data_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.data_tab, text="Dados")
        
        left_panel = ttk.LabelFrame(self.data_tab, text="Importação de Dados", padding=15)
        left_panel.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 5), pady=10)
        
        ttk.Button(left_panel, text="Importar CSV", 
                  command=self.import_csv, width=20).pack(pady=5)
        ttk.Button(left_panel, text="Importar Excel", 
                  command=self.import_excel, width=20).pack(pady=5)
        ttk.Button(left_panel, text="Carregar Exemplo", 
                  command=self.load_example, width=20).pack(pady=5)
        
        tk.Label(left_panel, text="Ou insira manualmente:", 
                font=('Arial', 10, 'bold')).pack(pady=(20, 10))
        
        form_frame = ttk.Frame(left_panel)
        form_frame.pack(fill='x', pady=10)
        
        self.manual_entries = {}
        parameters = [
            ("API", "°API"), ("Viscosidade", "cP"), ("Profundidade", "m"),
            ("Permeabilidade", "mD"), ("Porosidade", "%"), ("Saturação de Óleo", "%"),
            ("Saturação de Água", "%"), ("Temperatura", "°C"), ("Pressão", "psi"),
            ("Salinidade", "ppm"), ("Espessura", "m"), ("TAN", "mg KOH/g"),
            ("Dip", "graus")
        ]
        
        for i, (param, unit) in enumerate(parameters):
            row = ttk.Frame(form_frame)
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text=f"{param}:", width=20, anchor='w').pack(side=tk.LEFT)
            entry = ttk.Entry(row, width=15)
            entry.pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=unit).pack(side=tk.LEFT)
            
            self.manual_entries[param] = entry
        
        ttk.Button(left_panel, text="Adicionar Reservatório", 
                  command=self.add_manual_reservoir).pack(pady=20)
        
        right_panel = ttk.LabelFrame(self.data_tab, text="Visualização de Dados", padding=15)
        right_panel.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0), pady=10)
        
        columns = ("ID", "API", "Viscosidade", "Profundidade", "Permeabilidade", "Status")
        self.data_tree = ttk.Treeview(right_panel, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        self.data_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        btn_frame = ttk.Frame(right_panel)
        btn_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(btn_frame, text="Visualizar Detalhes", 
                  command=self.view_reservoir_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover Selecionado", 
                  command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Todos", 
                  command=self.clear_all_data).pack(side=tk.LEFT, padx=5)
        
    def _create_screening_tab(self):
        """Cria aba de triagem EOR"""
        self.screening_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.screening_tab, text="Triagem")
        
        control_frame = ttk.LabelFrame(self.screening_tab, text="Controles", padding=15)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Executar Triagem", 
                  command=self.run_screening, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Gerar Suitability", 
                  command=self.generate_suitability_charts, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Selecionar Todos", 
                  command=self.select_all_methods, width=20).pack(side=tk.LEFT, padx=5)
        
        # Criar um frame com scrollbar para mostrar todos os 15 métodos
        container = ttk.Frame(self.screening_tab)
        container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Criar um canvas e uma scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar os métodos ao scrollable_frame
        self.method_vars = {}
        methods = self.screening_engine.methods
        
        # Organizar métodos em 3 colunas para melhor visualização
        num_cols = 3
        for i, method in enumerate(methods):
            row = i // num_cols
            col = i % num_cols
            
            var = tk.BooleanVar(value=True)
            self.method_vars[method] = var
            
            cb = ttk.Checkbutton(scrollable_frame, text=method, variable=var)
            cb.grid(row=row, column=col, sticky='w', padx=10, pady=5, ipadx=5, ipady=5)
        
        # Configurar pesos das colunas
        for i in range(num_cols):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
            
    def _create_economic_tab(self):
        """Cria aba de análise econômica"""
        self.economic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.economic_tab, text="Análise Econômica")
        
        params_frame = ttk.LabelFrame(self.economic_tab, text="Parâmetros Econômicos", padding=15)
        params_frame.pack(fill='x', padx=10, pady=10)
        
        self.econ_entries = {}
        econ_params = [
            ("Preço do Óleo", "$/bbl", 60),
            ("Taxa de Desconto", "%", 10),
            ("Impostos", "%", 25),
            ("Vida do Projeto", "anos", 15),
            ("Taxa de Declínio", "%/ano", 15),
            ("Custo CAPEX", "$", 5000000),
            ("OPEX (% receita)", "%", 30)
        ]
        
        for i, (param, unit, default) in enumerate(econ_params):
            row = i // 3
            col = (i % 3) * 2
            
            tk.Label(params_frame, text=f"{param}:").grid(row=row, column=col, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(params_frame, width=12)
            entry.insert(0, str(default))
            entry.grid(row=row, column=col+1, sticky='w', padx=5, pady=5)
            tk.Label(params_frame, text=unit).grid(row=row, column=col+2, sticky='w', padx=(0, 20), pady=5)
            
            self.econ_entries[param] = entry
        
        prod_frame = ttk.LabelFrame(self.economic_tab, text="Perfil de Produção", padding=15)
        prod_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(prod_frame, text="Taxa de Produção Inicial (bbl/dia):").pack(side=tk.LEFT, padx=5)
        self.prod_entry = ttk.Entry(prod_frame, width=15)
        self.prod_entry.insert(0, "1000")
        self.prod_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(prod_frame, text="Calcular Análise", 
                  command=self.run_economic_analysis).pack(side=tk.LEFT, padx=20)
        ttk.Button(prod_frame, text="Plotar Gráfico", 
                  command=self.plot_economic_charts).pack(side=tk.LEFT, padx=5)
        
        results_frame = ttk.LabelFrame(self.economic_tab, text="Resultados Econômicos", padding=15)
        results_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.pack(fill='both', expand=True)
        
    def _create_results_tab(self):
        """Cria aba de resultados com seção de justificações"""
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Resultados")
        
        results_notebook = ttk.Notebook(self.results_tab)
        results_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de tabela resumida
        table_tab = ttk.Frame(results_notebook)
        results_notebook.add(table_tab, text="Tabela")
        
        self.results_tree = ttk.Treeview(table_tab, columns=("Método", "Pontuação", "Status", "Suitability"))
        self.results_tree.heading("Método", text="Método")
        self.results_tree.heading("Pontuação", text="Pontuação")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.heading("Suitability", text="Suitability")
        
        self.results_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de gráficos
        chart_tab = ttk.Frame(results_notebook)
        results_notebook.add(chart_tab, text="Gráficos")
        
        # Criar um frame para conter o canvas e a toolbar
        self.chart_container = ttk.Frame(chart_tab)
        self.chart_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de justificações
        justification_tab = ttk.Frame(results_notebook)
        results_notebook.add(justification_tab, text="Justificações")
        
        # Widget de texto para justificações
        self.justification_text = scrolledtext.ScrolledText(
            justification_tab, 
            width=100, 
            height=30,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.justification_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botões para justificações
        justify_frame = ttk.Frame(justification_tab)
        justify_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(justify_frame, text="Gerar Justificações",
                  command=self.generate_justifications).pack(side=tk.LEFT, padx=5)
        ttk.Button(justify_frame, text="Copiar Justificações",
                  command=self.copy_justifications).pack(side=tk.LEFT, padx=5)
        ttk.Button(justify_frame, text="Salvar Relatório",
                  command=self.save_justification_report).pack(side=tk.LEFT, padx=5)
        
        export_frame = ttk.Frame(self.results_tab)
        export_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(export_frame, text="Exportar para Excel", 
                  command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Copiar Resultados", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
    def _create_suitability_tab(self):
        """Cria aba específica para gráficos de suitability"""
        self.suitability_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.suitability_tab, text="Suitability")
        
        # Frame de controle
        control_frame = ttk.LabelFrame(self.suitability_tab, text="Controles de Suitability", padding=15)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(control_frame, text="Gerar Gráficos Suitability",
                  command=self.generate_suitability_charts, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Spider Chart",
                  command=self.show_spider_chart, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Matriz Suitability",
                  command=self.show_suitability_matrix, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Comparativo",
                  command=self.show_comparison_chart, width=20).pack(side=tk.LEFT, padx=5)
        
        # Notebook para diferentes visualizações de suitability
        self.suitability_notebook = ttk.Notebook(self.suitability_tab)
        self.suitability_notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Frame para gráfico principal
        self.main_suitability_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.main_suitability_frame, text="Visão Geral")
        
        # Frame para gráficos individuais
        self.individual_charts_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.individual_charts_frame, text="Gráficos Individuais")
        
        # Frame para matriz
        self.matrix_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.matrix_frame, text="Matriz")
        
        # Frame para comparativo
        self.comparison_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.comparison_frame, text="Comparativo")
        
    # ============================================================================
    # MÉTODOS DE SUITABILITY (NOVOS)
    # ============================================================================
    
    def generate_suitability_charts(self):
        """Gera todos os gráficos de suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro para gerar gráficos de suitability")
            return
        
        try:
            self.update_status("Gerando gráficos de suitability...")
            
            # Gerar spider chart principal
            self.show_spider_chart()
            
            # Gerar matriz de suitability
            self.show_suitability_matrix()
            
            # Gerar gráfico comparativo
            self.show_comparison_chart()
            
            # Navegar para aba de suitability
            self.notebook.select(self.suitability_tab)
            
            messagebox.showinfo("Sucesso", 
                              "Gráficos de suitability gerados com sucesso!\n\n"
                              "Consulte a aba 'Suitability' para análise visual detalhada.")
            self.update_status("Gráficos de suitability gerados")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar gráficos de suitability: {str(e)}")
            self.update_status("Erro ao gerar gráficos")
    
    def show_spider_chart(self):
        """Mostra gráfico spider/radar de suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            # Limpar frame anterior
            for widget in self.main_suitability_frame.winfo_children():
                widget.destroy()
            
            # Criar spider chart
            fig = self.suitability_viz.create_spider_chart(
                self.screening_results, 
                title="Análise de Suitability - Métodos EOR"
            )
            
            # Embed no Tkinter
            canvas = FigureCanvasTkAgg(fig, self.main_suitability_frame)
            canvas.draw()
            
            # Toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.main_suitability_frame)
            toolbar.update()
            
            # Empacotar
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar spider chart: {str(e)}")
    
    def show_suitability_matrix(self):
        """Mostra matriz de suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            # Limpar frame anterior
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            
            # Coletar dados para matriz
            criteria_scores = {}
            for method, data in self.screening_results.items():
                criteria_scores[method] = data.get('criteria_scores', {})
            
            # Criar matriz
            if self.reservoir_data:
                reservoir = self.reservoir_data[0]
                fig = self.suitability_viz.create_suitability_matrix(reservoir, criteria_scores)
                
                # Embed no Tkinter
                canvas = FigureCanvasTkAgg(fig, self.matrix_frame)
                canvas.draw()
                
                # Toolbar
                toolbar = NavigationToolbar2Tk(canvas, self.matrix_frame)
                toolbar.update()
                
                # Empacotar
                canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar matriz de suitability: {str(e)}")
    
    def show_comparison_chart(self):
        """Mostra gráfico comparativo de suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            # Limpar frame anterior
            for widget in self.comparison_frame.winfo_children():
                widget.destroy()
            
            # Criar gráfico comparativo
            fig = self.suitability_viz.create_comparison_chart(self.screening_results)
            
            # Embed no Tkinter
            canvas = FigureCanvasTkAgg(fig, self.comparison_frame)
            canvas.draw()
            
            # Toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.comparison_frame)
            toolbar.update()
            
            # Empacotar
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar gráfico comparativo: {str(e)}")
    
    def show_suitability_dashboard(self):
        """Mostra dashboard completo de suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        # Criar nova janela para dashboard
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard de Suitability - PetroChamp")
        dashboard_window.geometry("1200x800")
        
        # Criar notebook para diferentes visualizações
        dashboard_notebook = ttk.Notebook(dashboard_window)
        dashboard_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame 1: Visão geral
        overview_frame = ttk.Frame(dashboard_notebook)
        dashboard_notebook.add(overview_frame, text="Visão Geral")
        
        # Criar figura com múltiplos gráficos
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Dashboard de Suitability - Análise Completa', fontsize=16, fontweight='bold')
        
        # 1. Gráfico de barras
        methods = list(self.screening_results.keys())
        scores = [self.screening_results[m]['score'] for m in methods]
        colors = []
        for m in methods:
            if self.screening_results[m]['score'] >= 80:
                colors.append('#27ae60')
            elif self.screening_results[m]['score'] >= 60:
                colors.append('#f39c12')
            else:
                colors.append('#e74c3c')
        
        axes[0, 0].barh(methods, scores, color=colors, edgecolor='black')
        axes[0, 0].set_xlabel('Pontuação de Suitability (%)')
        axes[0, 0].set_title('Ranking de Suitability')
        axes[0, 0].set_xlim(0, 100)
        
        # 2. Distribuição por categoria
        categories = {'Alta': 0, 'Média': 0, 'Baixa': 0}
        for data in self.screening_results.values():
            if data['score'] >= 80:
                categories['Alta'] += 1
            elif data['score'] >= 60:
                categories['Média'] += 1
            else:
                categories['Baixa'] += 1
        
        axes[0, 1].pie(categories.values(), labels=categories.keys(), 
                      autopct='%1.1f%%', colors=['#27ae60', '#f39c12', '#e74c3c'])
        axes[0, 1].set_title('Distribuição por Categoria')
        
        # 3. Top 5 métodos
        top_methods = sorted(self.screening_results.items(), 
                           key=lambda x: x[1]['score'], reverse=True)[:5]
        top_names = [m[0] for m in top_methods]
        top_scores = [m[1]['score'] for m in top_methods]
        
        bars = axes[1, 0].bar(range(5), top_scores, color=['#27ae60', '#27ae60', 
                                                          '#f39c12', '#f39c12', '#f39c12'])
        axes[1, 0].set_xticks(range(5))
        axes[1, 0].set_xticklabels([n[:15] + '...' if len(n) > 15 else n for n in top_names], 
                                  rotation=45, ha='right')
        axes[1, 0].set_ylabel('Pontuação (%)')
        axes[1, 0].set_title('Top 5 Métodos')
        axes[1, 0].set_ylim(0, 100)
        
        # Adicionar valores nas barras
        for bar, score in zip(bars, top_scores):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{score:.1f}%', ha='center', va='bottom')
        
        # 4. Heatmap de adequabilidade
        heatmap_data = []
        param_names = ['API', 'Viscosidade', 'Profundidade', 'Permeabilidade', 'Temperatura']
        
        for param in param_names:
            row = []
            for method in methods:
                if param in self.screening_results[method].get('criteria_scores', {}):
                    score = self.screening_results[method]['criteria_scores'][param]
                    row.append(score)
                else:
                    row.append(0)
            heatmap_data.append(row)
        
        im = axes[1, 1].imshow(heatmap_data, aspect='auto', cmap='RdYlGn', 
                              vmin=0, vmax=100)
        axes[1, 1].set_yticks(range(len(param_names)))
        axes[1, 1].set_yticklabels(param_names)
        axes[1, 1].set_xticks(range(len(methods)))
        axes[1, 1].set_xticklabels([m[:10]+'...' if len(m) > 10 else m 
                                   for m in methods], rotation=90)
        axes[1, 1].set_title('Adequabilidade por Parâmetro')
        
        plt.colorbar(im, ax=axes[1, 1])
        plt.tight_layout()
        
        # Embed no Tkinter
        canvas = FigureCanvasTkAgg(fig, overview_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Frame 2: Análise detalhada
        detail_frame = ttk.Frame(dashboard_notebook)
        dashboard_notebook.add(detail_frame, text="Análise Detalhada")
        
        # Criar treeview para análise detalhada
        columns = ("Método", "Suitability", "Status", "Pontos Fortes", "Pontos Fracos")
        detail_tree = ttk.Treeview(detail_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            detail_tree.heading(col, text=col)
            detail_tree.column(col, width=150)
        
        # Preencher com dados
        for method, data in self.screening_results.items():
            pontos_fortes = len(data['pontos_positivos'])
            pontos_fracos = len(data['pontos_negativos'])
            
            # Determinar cor da linha
            tag = 'green' if data['score'] >= 80 else 'orange' if data['score'] >= 60 else 'red'
            
            detail_tree.insert("", tk.END, values=(
                method,
                f"{data['score']:.1f}%",
                data['status'],
                str(pontos_fortes),
                str(pontos_fracos)
            ), tags=(tag,))
        
        detail_tree.tag_configure('green', background='#d5f4e6')
        detail_tree.tag_configure('orange', background='#fdebd0')
        detail_tree.tag_configure('red', background='#fadbd8')
        
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=detail_tree.yview)
        detail_tree.configure(yscrollcommand=scrollbar.set)
        
        detail_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Botão para exportar dashboard
        export_btn = ttk.Button(dashboard_window, text="Exportar Dashboard", 
                               command=lambda: self.export_suitability_dashboard(fig))
        export_btn.pack(pady=10)
    
    def export_suitability_dashboard(self, fig):
        """Exporta dashboard de suitability como imagem"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), 
                      ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Sucesso", f"Dashboard exportado para:\n{filepath}")
            self.update_status(f"Dashboard exportado: {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar dashboard: {str(e)}")
    
    # ============================================================================
    # MÉTODOS EXISTENTES (mantidos do código anterior)
    # ============================================================================
    
    def update_status(self, message):
        """Atualiza barra de status"""
        self.status_bar.config(text=f"{message} | {datetime.now().strftime('%H:%M:%S')}")
        self.root.update_idletasks()
        
    def import_csv(self):
        """Importa dados de arquivo CSV"""
        filepath = filedialog.askopenfilename(
            title="Importar CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            self.update_status("Importando CSV...")
            df = pd.read_csv(filepath)
            self.reservoir_data = df.to_dict('records')
            
            self._update_data_tree()
            
            messagebox.showinfo("Sucesso", f"Importados {len(df)} reservatórios com sucesso!")
            self.update_status("CSV importado com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar CSV: {str(e)}")
            self.update_status("Erro na importação")
            
    def import_excel(self):
        """Importa dados de arquivo Excel"""
        filepath = filedialog.askopenfilename(
            title="Importar Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            self.update_status("Importando Excel...")
            df = pd.read_excel(filepath)
            self.reservoir_data = df.to_dict('records')
            
            self._update_data_tree()
            
            messagebox.showinfo("Sucesso", f"Importados {len(df)} reservatórios com sucesso!")
            self.update_status("Excel importado com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar Excel: {str(e)}")
            self.update_status("Erro na importação")
            
    def load_example(self):
        """Carrega dados de exemplo"""
        example_data = [
            {
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
        ]
        
        self.reservoir_data = example_data
        self._update_data_tree()
        messagebox.showinfo("Exemplo", "Dados de exemplo carregados com sucesso!")
        self.update_status("Exemplo carregado")
        
    def add_manual_reservoir(self):
        """Adiciona reservatório manualmente"""
        try:
            reservoir = {}
            for param, entry in self.manual_entries.items():
                value = entry.get()
                if value:
                    reservoir[param] = float(value)
                else:
                    reservoir[param] = None
            
            reservoir["ID"] = len(self.reservoir_data) + 1 if self.reservoir_data else 1
            
            if not self.reservoir_data:
                self.reservoir_data = []
                
            self.reservoir_data.append(reservoir)
            self._update_data_tree()
            
            for entry in self.manual_entries.values():
                entry.delete(0, tk.END)
                
            messagebox.showinfo("Sucesso", "Reservatório adicionado com sucesso!")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Por favor, insira valores numéricos válidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar reservatório: {str(e)}")
            
    def _update_data_tree(self):
        """Atualiza treeview com dados atuais"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        if not self.reservoir_data:
            return
            
        for reservoir in self.reservoir_data:
            values = (
                reservoir.get("ID", ""),
                reservoir.get("API", ""),
                reservoir.get("Viscosidade", ""),
                reservoir.get("Profundidade", ""),
                reservoir.get("Permeabilidade", ""),
                "Importado" if reservoir.get("ID") else "Manual"
            )
            self.data_tree.insert("", tk.END, values=values)
            
    def run_screening(self):
        """Executa triagem EOR e gera justificações automaticamente"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado de reservatório disponível")
            return
            
        self.update_status("Executando triagem EOR...")
        
        try:
            # Usar o primeiro reservatório para análise
            reservoir = self.reservoir_data[0]
            scores = self.screening_engine.score_reservoir(reservoir)
            
            self.screening_results = scores
            self._update_results_table(scores)
            
            self.update_status("Triagem concluída com justificações geradas")
            messagebox.showinfo("Sucesso", 
                              "Triagem EOR executada com sucesso!\n\n"
                              "As justificações detalhadas e análise de suitability foram geradas.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na triagem: {str(e)}")
            self.update_status("Erro na triagem")
    
    def _update_results_table(self, scores):
        """Atualiza tabela de resultados com cores e justificações"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        for method, data in scores.items():
            score = data["score"]
            status = data["status"]
            
            # Determinar ícone de suitability
            if score >= 80:
                suitability_icon = "🟢 ALTA"
                tag = "green"
            elif score >= 60:
                suitability_icon = "🟡 MÉDIA"
                tag = "orange"
            else:
                suitability_icon = "🔴 BAIXA"
                tag = "red"
            
            self.results_tree.insert("", tk.END, values=(
                method, 
                f"{score:.1f}%", 
                status,
                suitability_icon
            ), tags=(tag,))
            
        self.results_tree.tag_configure("green", foreground="green", font=('Arial', 10, 'bold'))
        self.results_tree.tag_configure("orange", foreground="orange", font=('Arial', 10))
        self.results_tree.tag_configure("red", foreground="red", font=('Arial', 10))
    
    def generate_justifications(self):
        """Gera justificações detalhadas para os métodos EOR"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado de reservatório disponível")
            return
        
        try:
            # Usar o primeiro reservatório
            reservoir = self.reservoir_data[0]
            
            # Gerar relatório de justificações
            self.justification_report = self.screening_engine.generate_justification_report(
                reservoir, self.screening_results
            )
            
            # Exibir no widget de texto
            self.justification_text.delete(1.0, tk.END)
            self.justification_text.insert(1.0, self.justification_report)
            
            # Navegar para a aba de justificações
            self.notebook.select(self.results_tab)
            tab_control = self.results_tab.winfo_children()[0]
            tab_control.select(2)  # Selecionar a aba de justificações
            
            messagebox.showinfo("Justificações Geradas", 
                              "Relatório de justificações e suitability gerado com sucesso!\n\n"
                              "Veja a aba 'Justificações' para análise detalhada.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar justificações: {str(e)}")
    
    def copy_justifications(self):
        """Copia justificações para a área de transferência"""
        if not self.justification_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Aviso", "Gere as justificações primeiro")
            return
        
        text_to_copy = self.justification_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text_to_copy)
        self.root.update()
        
        messagebox.showinfo("Copiado", "Justificações copiadas para a área de transferência!")
    
    def save_justification_report(self):
        """Salva relatório de justificações em arquivo de texto"""
        if not self.justification_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Aviso", "Gere as justificações primeiro")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.justification_text.get(1.0, tk.END))
            
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{filepath}")
            self.update_status(f"Relatório salvo: {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")
    
    def run_economic_analysis(self):
        """Executa análise econômica"""
        try:
            self.update_status("Calculando análise econômica...")
            
            economic_params = {}
            for param, entry in self.econ_entries.items():
                value = entry.get()
                if value:
                    # Converter chave para formato correto
                    key = param.lower().replace(" ", "_").replace("ó", "o").replace("ç", "c")
                    economic_params[key] = float(value)
            
            initial_rate = float(self.prod_entry.get())
            
            # Mapear nomes dos parâmetros para os nomes esperados pelo EconomicAnalyzer
            param_mapping = {
                "taxa_de_declínio": "decline_rate",
                "vida_do_projeto": "project_life",
                "taxa_de_desconto": "discount_rate"
            }
            
            # Criar dicionário com nomes corretos
            mapped_params = {}
            for key, value in economic_params.items():
                if key in param_mapping:
                    mapped_params[param_mapping[key]] = value
                else:
                    # Para outros parâmetros, tentar manter nomes padrão
                    mapped_params[key] = value
            
            # Adicionar parâmetros padrão se não estiverem presentes
            default_params = self.economic_analyzer.default_params
            for key, default_value in default_params.items():
                if key not in mapped_params:
                    mapped_params[key] = default_value
            
            production_profile = self.economic_analyzer.generate_production_profile(
                initial_rate, 
                mapped_params.get("decline_rate", 15),
                mapped_params.get("project_life", 15)
            )
            
            cashflow_data = self.economic_analyzer.calculate_cash_flow(
                production_profile, mapped_params
            )
            
            npv = self.economic_analyzer.calculate_npv(
                cashflow_data["cash_flow"], 
                mapped_params.get("discount_rate", 10)
            )
            
            irr = self.economic_analyzer.calculate_irr(cashflow_data["cash_flow"])
            payback = self.economic_analyzer.calculate_payback(cashflow_data["cash_flow"])
            
            self.economic_results = {
                "npv": npv,
                "irr": irr,
                "payback": payback,
                "cashflow": cashflow_data
            }
            
            self._display_economic_results(npv, irr, payback, cashflow_data)
            
            self.update_status("Análise econômica concluída")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
            self.update_status("Erro na análise econômica")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na análise: {str(e)}")
            self.update_status("Erro na análise econômica")
            
    def _display_economic_results(self, npv, irr, payback, cashflow_data):
        """Exibe resultados econômicos"""
        self.results_text.delete(1.0, tk.END)
        
        text = "=== RESULTADOS DA ANÁLISE ECONÔMICA ===\n\n"
        
        # Função segura para formatação
        def safe_format(value, format_str):
            if value is None:
                return "N/A"
            try:
                return format(value, format_str)
            except:
                return str(value)
        
        text += f"Valor Presente Líquido (NPV): ${safe_format(npv, ',.2f')}\n"
        text += f"Taxa Interna de Retorno (IRR): {safe_format(irr, '.2f')}%\n"
        text += f"Payback Período: {safe_format(payback, '.2f')} anos\n\n"
        
        text += f"Investimento Total (CAPEX): ${safe_format(cashflow_data.get('capex', 0), ',.2f')}\n\n"
        
        text += "Fluxo de Caixa por Ano:\n"
        text += "Ano | Fluxo de Caixa ($)\n"
        text += "-" * 30 + "\n"
        
        cash_flow = cashflow_data.get("cash_flow", [])
        for year, cf in enumerate(cash_flow):
            cf_str = safe_format(cf, "12,.2f")
            text += f"{year:3d} | ${cf_str}\n"
            
        self.results_text.insert(1.0, text)
        
    def plot_economic_charts(self):
        """Plota gráficos econômicos"""
        if not hasattr(self, 'economic_results') or not self.economic_results:
            messagebox.showwarning("Aviso", "Execute a análise econômica primeiro")
            return
        
        # Limpar frame anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()
            
        try:
            # Criar figura com múltiplos gráficos
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('Análise Econômica Completa', fontsize=16, fontweight='bold')
            
            # Dados para gráficos
            cf = np.array(self.economic_results["cashflow"]["cash_flow"])
            revenue = np.array(self.economic_results["cashflow"]["revenue"])
            opex = np.array(self.economic_results["cashflow"]["opex"])
            
            years = list(range(len(cf)))
            
            # Gráfico 1: Fluxo de caixa acumulado
            axes[0, 0].plot(years, np.cumsum(cf), 'b-', linewidth=2, marker='o')
            axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
            axes[0, 0].set_title("Fluxo de Caixa Acumulado", fontweight='bold')
            axes[0, 0].set_xlabel("Ano")
            axes[0, 0].set_ylabel("USD")
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].fill_between(years, np.cumsum(cf), alpha=0.3)
            
            # Gráfico 2: Receita vs OPEX
            if len(revenue) > 0:
                x = list(range(1, len(revenue) + 1))
                axes[0, 1].bar(x, revenue, alpha=0.6, label='Receita', color='green')
                axes[0, 1].bar(x, opex, alpha=0.6, label='OPEX', color='red')
                axes[0, 1].set_title("Receita vs OPEX", fontweight='bold')
                axes[0, 1].set_xlabel("Ano")
                axes[0, 1].set_ylabel("USD")
                axes[0, 1].legend()
                axes[0, 1].grid(True, alpha=0.3)
            
            # Gráfico 3: Pontuação dos métodos EOR (se disponível)
            if hasattr(self, 'screening_results') and self.screening_results:
                methods = list(self.screening_results.keys())
                scores = [self.screening_results[m]["score"] for m in methods]
                colors = [self.screening_results[m]["color"] for m in methods]
                
                bars = axes[1, 0].barh(methods, scores, color=colors)
                axes[1, 0].set_title("Suitability dos Métodos EOR", fontweight='bold')
                axes[1, 0].set_xlabel("Pontuação (%)")
                axes[1, 0].set_xlim(0, 100)
                
                # Adicionar valores nas barras
                for i, (bar, score) in enumerate(zip(bars, scores)):
                    width = bar.get_width()
                    axes[1, 0].text(width + 1, bar.get_y() + bar.get_height()/2,
                                   f'{score:.1f}%', va='center', fontweight='bold')
                    
                # Adicionar linhas de referência
                axes[1, 0].axvline(x=80, color='green', linestyle='--', alpha=0.5, label='Alta (≥80%)')
                axes[1, 0].axvline(x=60, color='orange', linestyle='--', alpha=0.5, label='Média (≥60%)')
                axes[1, 0].legend()
            else:
                axes[1, 0].text(0.5, 0.5, "Execute a triagem EOR\npara ver suitability", 
                               ha='center', va='center', transform=axes[1, 0].transAxes)
                axes[1, 0].set_title("Suitability dos Métodos EOR", fontweight='bold')
                
            # Gráfico 4: Sensibilidade do NPV
            discount_rates = np.linspace(5, 20, 10)
            npv_values = [self.economic_analyzer.calculate_npv(cf, dr) for dr in discount_rates]
            
            axes[1, 1].plot(discount_rates, npv_values, 'g-', linewidth=2, marker='s')
            axes[1, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
            axes[1, 1].set_title("Sensibilidade do NPV", fontweight='bold')
            axes[1, 1].set_xlabel("Taxa de Desconto (%)")
            axes[1, 1].set_ylabel("NPV (USD)")
            axes[1, 1].grid(True, alpha=0.3)
            
            # Destacar NPV atual
            current_dr = 10  # Taxa de desconto padrão
            if current_dr in discount_rates:
                idx = list(discount_rates).index(current_dr)
                axes[1, 1].plot(current_dr, npv_values[idx], 'ro', markersize=10)
                axes[1, 1].annotate(f'NPV: ${npv_values[idx]:,.0f}', 
                                   xy=(current_dr, npv_values[idx]),
                                   xytext=(current_dr+1, npv_values[idx]),
                                   arrowprops=dict(arrowstyle='->'))
            
            plt.tight_layout()
            
            # Embed no Tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart_container)
            canvas.draw()
            
            # Toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.chart_container)
            toolbar.update()
            
            # Empacotar
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar gráficos: {str(e)}")
        
    def show_score_chart(self):
        """Mostra gráfico de pontuação dos métodos EOR"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
            
        try:
            # Criar nova janela para o gráfico
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Gráfico de Suitability - Métodos EOR")
            chart_window.geometry("1000x700")
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(12, 8))
            
            methods = list(self.screening_results.keys())
            scores = [self.screening_results[m]["score"] for m in methods]
            colors = []
            for m in methods:
                if self.screening_results[m]["score"] >= 80:
                    colors.append('#27ae60')
                elif self.screening_results[m]["score"] >= 60:
                    colors.append('#f39c12')
                else:
                    colors.append('#e74c3c')
            
            bars = ax.barh(methods, scores, color=colors, edgecolor='black', height=0.7)
            ax.set_xlabel('Pontuação de Suitability (%)', fontweight='bold')
            ax.set_title('Análise de Suitability - Métodos EOR', fontsize=16, fontweight='bold')
            ax.set_xlim(0, 100)
            
            # Adicionar valores nas barras
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                       f'{score:.1f}%', ha='left', va='center', fontweight='bold')
            
            # Adicionar linhas de referência
            ax.axvline(x=80, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Alta Suitability (≥80%)')
            ax.axvline(x=60, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Média Suitability (60-79%)')
            ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Baixa Suitability (<60%)')
            
            # Adicionar legenda de cores
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#27ae60', label='ALTA SUITABILITY (≥80%)'),
                Patch(facecolor='#f39c12', label='MÉDIA SUITABILITY (60-79%)'),
                Patch(facecolor='#e74c3c', label='BAIXA SUITABILITY (<60%)')
            ]
            ax.legend(handles=legend_elements, loc='lower right')
            
            plt.tight_layout()
            
            # Embed no Tkinter
            canvas = FigureCanvasTkAgg(fig, chart_window)
            canvas.draw()
            
            # Toolbar
            toolbar = NavigationToolbar2Tk(canvas, chart_window)
            toolbar.update()
            
            # Empacotar
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar gráfico: {str(e)}")
    
    def run_complete_analysis(self):
        """Executa análise completa (triagem + econômica + justificações + suitability)"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado de reservatório disponível")
            return
            
        self.update_status("Iniciando análise completa...")
        
        # Executar triagem
        self.run_screening()
        
        # Executar análise econômica
        self.run_economic_analysis()
        
        # Gerar justificações
        self.generate_justifications()
        
        # Gerar gráficos de suitability
        self.generate_suitability_charts()
        
        # Navegar para aba de suitability
        self.notebook.select(self.suitability_tab)
        
        messagebox.showinfo("Análise Completa", 
                          "Análise técnica, econômica, justificações e suitability concluídas!\n\n"
                          "Consulte a aba 'Suitability' para análise visual detalhada.")
        self.update_status("Análise completa concluída")
    
    def export_excel(self):
        """Exporta resultados para Excel incluindo justificações e suitability"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            # Criar DataFrame com resultados da triagem
            triagem_data = []
            for method, scores in self.screening_results.items():
                triagem_data.append({
                    "Método": method,
                    "Pontuação": scores["score"],
                    "Status": scores["status"],
                    "Suitability": "Alta" if scores["score"] >= 80 else "Média" if scores["score"] >= 60 else "Baixa",
                    "Justificativa": scores["justificativa"],
                    "Pontos Positivos": "; ".join(scores["pontos_positivos"]),
                    "Pontos Negativos": "; ".join(scores["pontos_negativos"])
                })
                
            triagem_df = pd.DataFrame(triagem_data)
            
            # Criar writer Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Aba de triagem
                triagem_df.to_excel(writer, sheet_name='Triagem_EOR', index=False)
                
                # Aba de análise econômica (se disponível)
                if hasattr(self, 'economic_results') and self.economic_results:
                    econ_data = {
                        "NPV": [self.economic_results["npv"]],
                        "IRR": [f"{self.economic_results['irr']:.2f}%" if self.economic_results['irr'] is not None else "N/A"],
                        "Payback": [f"{self.economic_results['payback']:.2f} anos" if self.economic_results['payback'] is not None else "N/A"]
                    }
                    econ_df = pd.DataFrame(econ_data)
                    econ_df.to_excel(writer, sheet_name='Análise_Econômica', index=False)
                    
                    # Aba de fluxo de caixa
                    cf_data = {
                        "Ano": list(range(len(self.economic_results["cashflow"]["cash_flow"]))),
                        "Fluxo_de_Caixa": self.economic_results["cashflow"]["cash_flow"]
                    }
                    cf_df = pd.DataFrame(cf_data)
                    cf_df.to_excel(writer, sheet_name='Fluxo_de_Caixa', index=False)
                    
                # Aba de dados do reservatório (se disponível)
                if self.reservoir_data:
                    reservoir_df = pd.DataFrame(self.reservoir_data)
                    reservoir_df.to_excel(writer, sheet_name='Dados_Reservatório', index=False)
                
                # Aba de justificações completas (se disponível)
                if hasattr(self, 'justification_report') and self.justification_report:
                    # Converter relatório para DataFrame
                    lines = self.justification_report.split('\n')
                    justify_data = {"Relatório de Justificações e Suitability": lines}
                    justify_df = pd.DataFrame(justify_data)
                    justify_df.to_excel(writer, sheet_name='Justificações', index=False)
                
                # Aba de suitability por critério
                suitability_data = []
                for method, data in self.screening_results.items():
                    row = {"Método": method}
                    for param, score in data.get('criteria_scores', {}).items():
                        row[param] = score
                    suitability_data.append(row)
                
                if suitability_data:
                    suitability_df = pd.DataFrame(suitability_data)
                    suitability_df.to_excel(writer, sheet_name='Suitability_Detalhada', index=False)
                
            messagebox.showinfo("Sucesso", f"Resultados exportados para:\n{filepath}")
            self.update_status(f"Exportado para {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {str(e)}")
            self.update_status("Erro na exportação")
    
    def new_project(self):
        """Cria novo projeto"""
        if self.reservoir_data:
            response = messagebox.askyesno(
                "Novo Projeto", 
                "Deseja salvar o projeto atual antes de criar um novo?"
            )
            if response:
                self.save_project()
                
        # Limpar dados
        self.reservoir_data = []
        self.screening_results = None
        self.economic_results = None
        self.justification_report = None
        
        # Limpar interfaces
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        self.results_text.delete(1.0, tk.END)
        self.justification_text.delete(1.0, tk.END)
        
        # Limpar gráficos
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        # Limpar gráficos de suitability
        for frame in [self.main_suitability_frame, self.matrix_frame, 
                     self.comparison_frame, self.individual_charts_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        
        messagebox.showinfo("Novo Projeto", "Novo projeto criado com sucesso!")
        self.update_status("Novo projeto criado")
    
    def save_project(self):
        """Salva projeto atual em arquivo JSON"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            project_data = {
                "reservoir_data": self.reservoir_data,
                "screening_results": self.screening_results,
                "economic_results": self.economic_results,
                "justification_report": self.justification_report,
                "timestamp": datetime.now().isoformat(),
                "version": "PetroChamp 4.0 com Suitability"
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, default=str)
                
            messagebox.showinfo("Sucesso", f"Projeto salvo em:\n{filepath}")
            self.update_status(f"Projeto salvo: {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")
    
    def open_project(self):
        """Abre projeto salvo em arquivo JSON"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            self.reservoir_data = project_data.get("reservoir_data", [])
            self.screening_results = project_data.get("screening_results")
            self.economic_results = project_data.get("economic_results")
            self.justification_report = project_data.get("justification_report")
            
            # Atualizar interfaces
            self._update_data_tree()
            
            if self.screening_results:
                self._update_results_table(self.screening_results)
            
            if self.justification_report:
                self.justification_text.delete(1.0, tk.END)
                self.justification_text.insert(1.0, self.justification_report)
            
            # Atualizar resultados econômicos
            if self.economic_results:
                self._display_economic_results(
                    self.economic_results["npv"],
                    self.economic_results["irr"],
                    self.economic_results["payback"],
                    self.economic_results["cashflow"]
                )
                
            messagebox.showinfo("Sucesso", f"Projeto carregado de:\n{filepath}")
            self.update_status(f"Projeto aberto: {os.path.basename(filepath)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar: {str(e)}")
    
    def import_data(self):
        """Importa dados - navega para aba de dados"""
        self.notebook.select(self.data_tab)
        self.update_status("Aguardando importação de dados")
    
    def export_report(self):
        """Exporta relatório (chama export_excel)"""
        self.export_excel()
    
    def show_documentation(self):
        """Mostra documentação do sistema"""
        docs = """
        PETROCHAMP - PLATAFORMA DE TRIAGEM EOR COM SUITABILITY
        
        FUNCIONALIDADES PRINCIPAIS:
        1. IMPORTAR DADOS:
           • CSV: Arquivos com dados de reservatórios
           • Excel: Planilhas com múltiplas abas
           • Manual: Inserção direta de parâmetros
        
        2. TRIAGEM EOR:
           • Avaliação de 15 métodos de recuperação avançada
           • Critérios técnicos baseados em literatura
           • Pontuação automática e classificação
           • Análise de suitability detalhada
        
        3. GRÁFICOS DE SUITABILITY:
           • Spider charts para visualização multidimensional
           • Matriz de adequabilidade parâmetros vs métodos
           • Gráficos comparativos
           • Dashboard completo de suitability
        
        4. ANÁLISE ECONÔMICA:
           • Cálculo de NPV, IRR e Payback
           • Projeção de fluxo de caixa
           • Parâmetros ajustáveis (preço, taxas, custos)
           • Gráficos interativos
        
        5. JUSTIFICAÇÕES DETALHADAS:
           • Explicações completas em texto para cada método
           • Pontos fortes e pontos a melhorar
           • Recomendações específicas baseadas em suitability
           • Relatórios completos com análise técnica
        
        MÉTODOS EOR DISPONÍVEIS (15):
        1. Injeção de Vapor
        2. Combustão In Situ
        3. Injeção de CO2 Miscível
        4. Injeção de Polímeros
        5. Injeção de Surfactantes
        6. Injeção Alcalina
        7. Injeção de Gás Não-Miscível
        8. Injeção de Nitrogênio
        9. Injeção de Gás Enriquecido
        10. Polímero-Surfactante
        11. VAPEX (Vapor Extraction)
        12. Injeção de Água Inteligente
        13. Injeção de Espuma
        14. Aquecimento Elétrico
        15. Injeção Microbiana
        
        SISTEMA DE SUITABILITY:
        Para cada método EOR, o sistema calcula:
        • Pontuação de suitability (0-100%)
        • Categoria: Alta (≥80%), Média (60-79%), Baixa (<60%)
        • Análise por parâmetro técnico
        • Visualização em gráficos spider/radar
        • Matriz de adequabilidade
        
        PARÂMETROS TÉCNICOS ANALISADOS:
        • API (°API) - Grau API do óleo
        • Viscosidade (cP) - Viscosidade do óleo
        • Profundidade (m) - Profundidade do reservatório
        • Permeabilidade (mD) - Permeabilidade da rocha
        • Porosidade (%) - Porosidade do reservatório
        • Saturações (%) - Saturação de óleo e água
        • Temperatura (°C) - Temperatura do reservatório
        • Pressão (psi) - Pressão do reservatório
        • Salinidade (ppm) - Salinidade da água
        • Espessura (m) - Espessura da formação
        • TAN (mg KOH/g) - Número de acidez total
        • Dip (graus) - Ângulo de mergulho da formação
        
        INSTRUÇÕES DE USO:
        1. Importe dados ou insira manualmente
        2. Execute a triagem EOR
        3. Configure parâmetros econômicos
        4. Calcule análise econômica
        5. Gere gráficos de suitability
        6. Analise justificações detalhadas
        7. Exporte resultados para análise
        
        DICAS:
        • Use o exemplo para testar todas as funcionalidades
        • Consulte os gráficos de suitability para análise visual
        • Exporte dashboard para apresentações
        • Salve projetos para trabalho futuro
        • Use as justificações para entender recomendações técnicas
        """
        
        # Criar janela de documentação
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentação - PetroChamp com Suitability")
        doc_window.geometry("700x600")
        
        # Adicionar texto rolável
        doc_text = scrolledtext.ScrolledText(doc_window, width=85, height=35)
        doc_text.pack(padx=10, pady=10)
        doc_text.insert(1.0, docs)
        doc_text.config(state='disabled')
        
        # Botão de fechar
        ttk.Button(doc_window, text="Fechar", command=doc_window.destroy).pack(pady=10)
    
    def show_about(self):
        """Mostra informações sobre o software"""
        about_text = f"""
        PetroChamp - Plataforma de Triagem EOR com Suitability
        Versão 4.0
        
        Desenvolvido para auxiliar engenheiros de reservatórios
        na seleção de métodos de Recuperação Avançada de Petróleo.
        
        NOVAS CARACTERÍSTICAS:
        • Sistema completo de análise de suitability
        • Gráficos spider/radar para visualização multidimensional
        • Dashboard de suitability com semáforo de adequabilidade
        • Matriz de adequabilidade parâmetros vs métodos
        • Justificações detalhadas com análise técnica
        
        Características principais:
        • Interface profissional com múltiplas abas
        • 15 métodos EOR com critérios técnicos detalhados
        • Análise econômica completa (NPV, IRR, Payback)
        • Sistema de gerenciamento de projetos
        • Exportação para Excel com análise de suitability
        
        Sistema de Suitability:
        • Pontuação 0-100% para cada método
        • Categorias: Alta (🟢), Média (🟡), Baixa (🔴)
        • Análise por parâmetro técnico
        • Visualização gráfica avançada
        
        Data: {datetime.now().strftime('%d/%m/%Y')}
        © 2024 PetroChamp Team
        
        Dependências:
        • Python 3.8+
        • Pandas, NumPy, Matplotlib
        • Seaborn, Openpyxl
        
        Para suporte ou relatar problemas:
        • Verifique a documentação completa
        • Certifique-se de ter todas as dependências instaladas
        """
        
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre o PetroChamp com Suitability")
        about_window.geometry("500x400")
        
        # Adicionar texto
        text_widget = scrolledtext.ScrolledText(about_window, width=60, height=20)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(1.0, about_text)
        text_widget.config(state='disabled')
        
        # Botão de fechar
        ttk.Button(about_window, text="Fechar", command=about_window.destroy).pack(pady=10)
    
    def select_all_methods(self):
        """Seleciona todos os métodos EOR na triagem"""
        for var in self.method_vars.values():
            var.set(True)
        self.update_status("Todos os métodos selecionados")
    
    def clear_selection(self):
        """Limpa seleção de métodos na triagem"""
        for var in self.method_vars.values():
            var.set(False)
        self.update_status("Seleção limpa")
    
    def view_reservoir_details(self):
        """Visualiza detalhes do reservatório selecionado"""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um reservatório na tabela")
            return
            
        item = self.data_tree.item(selection[0])
        reservoir_id = item['values'][0]
        
        # Encontrar reservatório
        reservoir = None
        for r in self.reservoir_data:
            if r.get("ID") == reservoir_id:
                reservoir = r
                break
                
        if not reservoir:
            messagebox.showerror("Erro", "Reservatório não encontrado")
            return
            
        # Mostrar detalhes
        details = f"=== DETALHES DO RESERVATÓRIO {reservoir_id} ===\n\n"
        for key, value in reservoir.items():
            if value is not None:
                details += f"{key}: {value}\n"
            else:
                details += f"{key}: Não informado\n"
        
        # Criar janela de detalhes
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Reservatório {reservoir_id}")
        detail_window.geometry("500x400")
        
        text_widget = scrolledtext.ScrolledText(detail_window, width=60, height=20)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(1.0, details)
        text_widget.config(state='disabled')
        
        # Botão de fechar
        ttk.Button(detail_window, text="Fechar", command=detail_window.destroy).pack(pady=10)
    
    def remove_selected(self):
        """Remove reservatório selecionado"""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um reservatório para remover")
            return
            
        item = self.data_tree.item(selection[0])
        reservoir_id = item['values'][0]
        
        # Confirmar remoção
        response = messagebox.askyesno("Confirmar", f"Remover reservatório {reservoir_id}?")
        if not response:
            return
            
        # Remover do dados
        self.reservoir_data = [r for r in self.reservoir_data if r.get("ID") != reservoir_id]
        
        # Atualizar treeview
        self._update_data_tree()
        
        messagebox.showinfo("Sucesso", f"Reservatório {reservoir_id} removido com sucesso")
        self.update_status(f"Reservatório {reservoir_id} removido")
    
    def clear_all_data(self):
        """Limpa todos os dados do projeto"""
        if not self.reservoir_data:
            messagebox.showinfo("Informação", "Não há dados para limpar")
            return
            
        response = messagebox.askyesno(
            "Confirmar", 
            "Deseja remover TODOS os dados do projeto?\nEsta ação não pode ser desfeita."
        )
        
        if response:
            self.reservoir_data = []
            self.screening_results = None
            self.economic_results = None
            self.justification_report = None
            
            # Limpar interfaces
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
                
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
                
            self.results_text.delete(1.0, tk.END)
            self.justification_text.delete(1.0, tk.END)
            
            # Limpar gráficos
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            
            # Limpar gráficos de suitability
            for frame in [self.main_suitability_frame, self.matrix_frame, 
                         self.comparison_frame, self.individual_charts_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()
            
            messagebox.showinfo("Sucesso", "Todos os dados foram removidos")
            self.update_status("Todos os dados removidos")
    
    def copy_to_clipboard(self):
        """Copia resultados da triagem para clipboard"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Nenhum resultado para copiar")
            return
            
        text = "RESULTADOS DA TRIAGEM EOR - PETROCHAMP COM SUITABILITY\n"
        text += "=" * 60 + "\n\n"
        
        for method, data in self.screening_results.items():
            text += f"Método: {method}\n"
            text += f"Suitability: {data['score']:.1f}% "
            if data['score'] >= 80:
                text += "🟢 ALTA\n"
            elif data['score'] >= 60:
                text += "🟡 MÉDIA\n"
            else:
                text += "🔴 BAIXA\n"
            text += f"Status: {data['status']}\n"
            text += "-" * 30 + "\n"
            
        # Adicionar data/hora
        text += f"\nGerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        
        messagebox.showinfo("Sucesso", "Resultados copiados para o clipboard")
        self.update_status("Resultados copiados para clipboard")
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

# ============================================================================
# EXECUÇÃO PRINCIPAL - COM VERIFICAÇÃO DE ERROS
# ============================================================================
def main():
    """Função principal de execução"""
    try:
        # Verificar dependências
        required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'openpyxl']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            error_msg = "Faltam as seguintes dependências:\n\n"
            for package in missing_packages:
                error_msg += f"• {package}\n"
            error_msg += "\nInstale com: pip install " + " ".join(missing_packages)
            messagebox.showerror("Erro de Dependência", error_msg)
            return
        
        print("=" * 60)
        print("INICIANDO PETROCHAMP - PLATAFORMA DE TRIAGEM EOR COM SUITABILITY")
        print("Versão: 4.0 (Com Gráficos de Suitability)")
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Iniciar aplicação
        app = PetroChampPlatform()
        app.run()
        
    except Exception as e:
        # Mostrar erro detalhado
        import traceback
        error_details = traceback.format_exc()
        
        error_msg = f"ERRO AO INICIAR A APLICAÇÃO:\n\n"
        error_msg += f"Tipo de erro: {type(e).__name__}\n"
        error_msg += f"Mensagem: {str(e)}\n\n"
        error_msg += "Detalhes técnicos:\n"
        error_msg += error_details
        
        # Tentar mostrar em messagebox
        try:
            messagebox.showerror("Erro Fatal", error_msg[:1000] + "\n\n...")
        except:
            print("ERRO CRÍTICO:")
            print(error_msg)
        
        # Salvar log de erro
        try:
            with open('petrochamp_suitability_error.log', 'w') as f:
                f.write(error_msg)
            print("\nLog de erro salvo em: petrochamp_suitability_error.log")
        except:
            pass

if __name__ == "__main__":
    main()