"""
PETROCHAMP - PLATAFORMA COMPLETA EOR COM JUSTIFICAÇÕES E ANÁLISE DE SUITABILITY
=====================================================================================

Sistema integrado para triagem técnica e análise econômica de projetos de recuperação
secundária/terciária de petróleo com 15 métodos EOR diferentes.

Uso:
    python v6.py

Requisitos:
    - tkinter, pandas, numpy, matplotlib, seaborn
    - numpy_financial (opcional - para cálculo de IRR)

Funcionalidades principais:
    • Triagem de 15 métodos EOR com critérios baseados em literatura
    • Sistema de justificações automáticas para cada método
    • Gráficos de suitability (adequabilidade) multidimensionais
    • Análise econômica completa (NPV, IRR, Payback)
    • Dashboard visual com cores de semáforo
    • Importação/exportação de dados (CSV, Excel, JSON)
    • Relatórios detalhados com análise de parâmetros
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Dict, List, Tuple, Optional, Any
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
import logging
from datetime import datetime
import json
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DE LOGGING E CONSTANTES
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes de configuração
SUITABILITY_THRESHOLDS = {
    'alta': 80,      # Score >= 80%
    'media': 60,     # Score 60-79%
    'baixa': 0       # Score < 60%
}

COLOR_SCHEME = {
    'alta': '#27ae60',   # Verde
    'media': '#f39c12',  # Laranja
    'baixa': '#e74c3c',  # Vermelho
    'neutro': '#bdc3c7'  # Cinza
}

WINDOW_CONFIG = {
    'title': 'PetroChamp - Plataforma de Triagem EOR com Justificações e Suitability',
    'geometry': '1400x900',
    'minsize': (1200, 700)
}

# Tentar importar numpy_financial para cálculo de IRR
try:
    import numpy_financial as npf
    HAS_NUMPY_FINANCIAL = True
except ImportError:
    HAS_NUMPY_FINANCIAL = False
    logger.warning("numpy_financial não está instalado. Usando cálculo manual de IRR.")

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# MÓDULO DE GRÁFICOS DE SUITABILITY (ADEQUABILIDADE)
# ============================================================================

class SuitabilityVisualizer:
    """Gerador de gráficos de suitability para métodos EOR.
    
    Responsável pela criação de visualizações e análises gráficas
    de adequabilidade dos métodos EOR aos parâmetros do reservatório.
    """
    
    def __init__(self):
        """Inicializa visualizador com paleta de cores padrão."""
        self.colors = COLOR_SCHEME
        self.thresholds = SUITABILITY_THRESHOLDS
        
    def _validate_method_scores(self, method_scores: Dict[str, Dict]) -> bool:
        """Valida estrutura de dados de scores de métodos.
        
        Args:
            method_scores: Dicionário com scores dos métodos
            
        Returns:
            True se válido, False caso contrário
        """
        if not method_scores:
            logger.warning("method_scores vazio")
            return False
            
        required_keys = {'score', 'color'}
        for method, data in method_scores.items():
            if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
                logger.error(f"Dados inválidos para método {method}")
                return False
                
        return True
    
    def create_spider_chart(self, method_scores: Dict[str, Dict], 
                          title: str = "Suitability EOR") -> plt.Figure:
        """Cria gráfico radar/spider para visualização de suitability.
        
        Args:
            method_scores: Dict com scores de cada método
            title: Título do gráfico
            
        Returns:
            Figure do matplotlib
            
        Raises:
            ValueError: Se dados inválidos
        """
        if not self._validate_method_scores(method_scores):
            raise ValueError("Dados de método inválidos")
        
        try:
            # Preparar dados
            methods = list(method_scores.keys())
            scores = [method_scores[m]['score'] for m in methods]
            colors = [method_scores[m]['color'] for m in methods]
            
            # Mapear cores para valores hex
            color_map = {'green': self.colors['alta'], 
                        'orange': self.colors['media'], 
                        'red': self.colors['baixa']}
            bar_colors = [color_map.get(c, '#3498db') for c in colors]
            
            # Criar figura
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Gráfico 1: Barras horizontais
            y_pos = np.arange(len(methods))
            bars = ax1.barh(y_pos, scores, color=bar_colors, edgecolor='black', linewidth=1.5)
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(methods, fontsize=9)
            ax1.set_xlabel('Pontuação de Suitability (%)', fontweight='bold')
            ax1.set_title('Pontuação por Método', fontweight='bold')
            ax1.set_xlim([0, 100])
            ax1.grid(axis='x', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar, score in zip(bars, scores):
                width = bar.get_width()
                ax1.text(width + 1, bar.get_y() + bar.get_height()/2,
                        f'{score:.1f}%', ha='left', va='center', fontsize=8, fontweight='bold')
            
            # Adicionar linhas de referência com significado
            ax1.axvline(x=self.thresholds['alta'], color=self.colors['alta'], 
                       linestyle='--', alpha=0.5, linewidth=2, label='Alta (≥80%)')
            ax1.axvline(x=self.thresholds['media'], color=self.colors['media'], 
                       linestyle='--', alpha=0.5, linewidth=2, label='Média (60-79%)')
            ax1.legend(loc='lower right', fontsize=9)
            
            # Gráfico 2: Radar para top 3 métodos
            top_methods = sorted(method_scores.items(), 
                               key=lambda x: x[1]['score'], reverse=True)[:3]
            
            if len(top_methods) >= 3:
                categories = ['Técnico', 'Econômico', 'Operacional', 'Ambiental', 'Risco']
                values_list = []
                
                for method, data in top_methods:
                    score = data['score']
                    # Distribuir score nas categorias de forma ponderada
                    vals = self._distribute_score(score)
                    values_list.append(vals)
                
                # Configurar ângulos para radar
                N = len(categories)
                angles = [n / float(N) * 2 * np.pi for n in range(N)]
                angles += angles[:1]
                
                # Plotar radar
                ax2 = plt.subplot(122, polar=True)
                for i, (method, data) in enumerate(top_methods):
                    val = values_list[i] + [values_list[i][0]]
                    label = method[:12] + '...' if len(method) > 12 else method
                    ax2.plot(angles, val, linewidth=2, linestyle='solid', label=label, marker='o')
                    ax2.fill(angles, val, alpha=0.1)
                
                # Configurar radar
                ax2.set_theta_offset(np.pi / 2)
                ax2.set_theta_direction(-1)
                ax2.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=8)
                ax2.set_ylim(0, 100)
                ax2.set_yticks([20, 40, 60, 80, 100])
                ax2.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7)
                ax2.set_title('Top 3 Métodos - Análise Multidimensional', fontweight='bold', pad=20)
                ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=8)
                ax2.grid(True)
            
            plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            
            logger.info(f"Spider chart criado com sucesso para {len(methods)} métodos")
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar spider chart: {str(e)}")
            raise
    
    def _distribute_score(self, score: float) -> List[float]:
        """Distribui score normalizado em 5 dimensões.
        
        Args:
            score: Score normalizado (0-100)
            
        Returns:
            Lista com 5 valores distribuídos
        """
        if score >= 80:
            return [score*0.9, score*1.1, score*0.95, score*0.85, score*0.8]
        elif score >= 60:
            return [score*0.8, score*0.9, score*0.7, score*0.6, score*0.5]
        else:
            return [score*0.7, score*0.6, score*0.5, score*0.4, score*0.3]
    
    def create_suitability_matrix(self, reservoir_data: Dict, 
                                 criteria_scores: Dict) -> plt.Figure:
        """Cria matriz de heatmap para suitability de parâmetros.
        
        Args:
            reservoir_data: Dados do reservatório
            criteria_scores: Scores por critério e método
            
        Returns:
            Figure do matplotlib
        """
        try:
            # Criar figura
            fig, ax = plt.subplots(figsize=(13, 8))
            
            # Preparar dados
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
                        score = criteria_scores[method][param]
                        matrix[i, j] = 1 if score > 0 else (-1 if score < 0 else 0)
            
            # Criar heatmap com cores discretas
            cmap = plt.cm.RdYlGn
            im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=-1, vmax=1, interpolation='nearest')
            
            # Configurar eixos
            ax.set_xticks(np.arange(len(methods)))
            ax.set_yticks(np.arange(len(parameters)))
            
            method_labels = [m[:12] + '...' if len(m) > 12 else m for m in methods]
            ax.set_xticklabels(method_labels, rotation=45, ha='right', fontsize=9)
            ax.set_yticklabels(parameters, fontsize=9)
            
            # Adicionar símbolos nas células
            for i in range(len(parameters)):
                for j in range(len(methods)):
                    value = matrix[i, j]
                    text = "✓" if value > 0 else "✗" if value < 0 else "-"
                    color = "white" if abs(value) > 0.5 else "black"
                    ax.text(j, i, text, ha="center", va="center", 
                           color=color, fontweight='bold', fontsize=11)
            
            ax.set_title("Matriz de Adequabilidade - Parâmetros vs Métodos", 
                        fontweight='bold', pad=20, fontsize=12)
            
            cbar = plt.colorbar(im, ax=ax, ticks=[-1, 0, 1])
            cbar.set_label('Adequabilidade: ✗=Baixa, -=Não avaliado, ✓=Alta', fontsize=9)
            
            plt.tight_layout()
            logger.info(f"Matriz de suitability criada com {len(parameters)} parâmetros")
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar matriz de suitability: {str(e)}")
            raise
    
    def create_comparison_chart(self, method_scores: Dict[str, Dict]) -> plt.Figure:
        """Cria gráfico comparativo completo com 4 visualizações.
        
        Args:
            method_scores: Dict com scores dos métodos
            
        Returns:
            Figure com 4 subplots
        """
        if not self._validate_method_scores(method_scores):
            raise ValueError("Dados de método inválidos")
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Análise Comparativa de Suitability', 
                        fontsize=16, fontweight='bold', y=0.995)
            
            # 1. Gráfico de barras coloridas por status
            methods = list(method_scores.keys())
            scores = [method_scores[m]['score'] for m in methods]
            colors = [self._get_status_color(score) for score in scores]
            
            axes[0, 0].barh(methods, scores, color=colors, edgecolor='black', linewidth=1.2)
            axes[0, 0].set_xlabel('Pontuação (%)', fontweight='bold')
            axes[0, 0].set_title('Suitability por Método', fontweight='bold')
            axes[0, 0].set_xlim(0, 100)
            axes[0, 0].grid(axis='x', alpha=0.3)
            
            # 2. Distribuição por categoria
            categories = self._count_categories(method_scores)
            
            pie_colors = [self.colors['alta'], self.colors['media'], self.colors['baixa']]
            wedges, texts, autotexts = axes[0, 1].pie(categories.values(), 
                                                        labels=categories.keys(), 
                                                        autopct='%1.1f%%',
                                                        colors=pie_colors,
                                                        startangle=90)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            axes[0, 1].set_title('Distribuição por Categoria', fontweight='bold')
            
            # 3. Evolução acumulada
            sorted_scores = sorted(scores, reverse=True)
            cumulative = np.cumsum(sorted_scores) / np.sum(sorted_scores) * 100 if sorted_scores else []
            
            if cumulative.size > 0:
                axes[1, 0].plot(range(1, len(sorted_scores) + 1), cumulative, 
                               marker='o', linewidth=2.5, markersize=6, color=self.colors['media'])
                axes[1, 0].fill_between(range(1, len(sorted_scores) + 1), 
                                       cumulative, alpha=0.2, color=self.colors['media'])
                axes[1, 0].set_xlabel('Número de Métodos (ordenados)', fontweight='bold')
                axes[1, 0].set_ylabel('Suitabilidade Acumulada (%)', fontweight='bold')
                axes[1, 0].set_title('Curva de Suitability Acumulada', fontweight='bold')
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].set_ylim([0, 105])
            
            # 4. Heatmap de scores
            heatmap_data = np.array(scores).reshape(1, -1)
            im = axes[1, 1].imshow(heatmap_data, aspect='auto', cmap='RdYlGn', 
                                  vmin=0, vmax=100, interpolation='nearest')
            
            method_labels_short = [m[:8]+'...' if len(m) > 8 else m for m in methods]
            axes[1, 1].set_xticks(range(len(methods)))
            axes[1, 1].set_xticklabels(method_labels_short, rotation=90, fontsize=8)
            axes[1, 1].set_yticks([])
            axes[1, 1].set_title('Mapa de Calor - Suitability', fontweight='bold')
            
            # Adicionar valores no heatmap
            for i in range(len(methods)):
                axes[1, 1].text(i, 0, f'{scores[i]:.0f}%', ha='center', va='center', 
                              color='black' if scores[i] < 50 else 'white', 
                              fontweight='bold', fontsize=9)
            
            cbar = plt.colorbar(im, ax=axes[1, 1])
            cbar.set_label('Score (%)', fontweight='bold')
            
            plt.tight_layout()
            logger.info("Gráfico comparativo criado com sucesso")
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico comparativo: {str(e)}")
            raise
    
    def _get_status_color(self, score: float) -> str:
        """Retorna cor baseada no score.
        
        Args:
            score: Score normalizado (0-100)
            
        Returns:
            Código hex de cor
        """
        if score >= self.thresholds['alta']:
            return self.colors['alta']
        elif score >= self.thresholds['media']:
            return self.colors['media']
        else:
            return self.colors['baixa']
    
    def _count_categories(self, method_scores: Dict[str, Dict]) -> Dict[str, int]:
        """Conta métodos por categoria de suitability.
        
        Args:
            method_scores: Dict com scores dos métodos
            
        Returns:
            Dict com contagem por categoria
        """
        categories = {'Alta': 0, 'Média': 0, 'Baixa': 0}
        for data in method_scores.values():
            score = data['score']
            if score >= self.thresholds['alta']:
                categories['Alta'] += 1
            elif score >= self.thresholds['media']:
                categories['Média'] += 1
            else:
                categories['Baixa'] += 1
        return categories
    
    def create_spider_chart_advanced(self, method_scores: Dict[str, Dict], 
                                    title: str = "Suitability EOR") -> Optional[plt.Figure]:
        """Cria gráfico spider avançado com análise multidimensional.
        
        Args:
            method_scores: Dict com scores de cada método
            title: Título do gráfico
            
        Returns:
            Figure do matplotlib ou None se implementação futura
        """
        try:
            # Implementação futura para análise multidimensional avançada
            logger.warning("Função create_spider_chart_advanced ainda não implementada")
            return None
        except Exception as e:
            logger.error(f"Erro ao criar spider chart: {str(e)}")
            return None
    
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
        criteria = self.screening_engine.criteria.get(method_name, {})
        
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
            },
            # ====== NOVOS MÉTODOS EOR - FASE 1 EXPANSÃO ======
            "Injeção Cíclica de Vapor (CSS)": {
                "API": {"min": None, "max": 25, "peso": 0.3},
                "Viscosidade": {"min": 50, "max": 10000, "peso": 0.35},
                "Profundidade": {"min": 150, "max": 2000, "peso": 0.15},
                "Espessura": {"min": 5, "max": None, "peso": 0.1},
                "Saturação de Óleo": {"min": 35, "max": None, "peso": 0.1}
            },
            "Injeção de Gás com Alternância de Água (WAG)": {
                "API": {"min": 20, "max": None, "peso": 0.25},
                "Viscosidade": {"min": None, "max": 50, "peso": 0.2},
                "Pressão": {"min": 1000, "max": None, "peso": 0.2},
                "Profundidade": {"min": 800, "max": 3500, "peso": 0.15},
                "Permeabilidade": {"min": 50, "max": 2000, "peso": 0.2}
            },
            "Injeção de Baixa Salinidade (LoSal)": {
                "Viscosidade": {"min": None, "max": 200, "peso": 0.2},
                "Salinidade": {"min": 30000, "max": None, "peso": 0.3},
                "Temperatura": {"min": None, "max": 100, "peso": 0.15},
                "Permeabilidade": {"min": 10, "max": 2000, "peso": 0.2},
                "TAN": {"min": 0.2, "max": None, "peso": 0.15}
            },
            "Nanotecnologia aplicada ao EOR": {
                "API": {"min": 10, "max": 40, "peso": 0.2},
                "Viscosidade": {"min": None, "max": 500, "peso": 0.2},
                "Salinidade": {"min": None, "max": 200000, "peso": 0.2},
                "Temperatura": {"min": 20, "max": 120, "peso": 0.2},
                "Permeabilidade": {"min": 1, "max": 5000, "peso": 0.2}
            },
            "EOR Térmico para Águas Profundas": {
                "API": {"min": None, "max": 24, "peso": 0.3},
                "Viscosidade": {"min": 80, "max": 5000, "peso": 0.3},
                "Profundidade": {"min": 1000, "max": 3500, "peso": 0.2},
                "Temperatura": {"min": None, "max": 130, "peso": 0.1},
                "Pressão": {"min": 500, "max": None, "peso": 0.1}
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
            },
            # ====== JUSTIFICAÇÕES DOS NOVOS MÉTODOS - FASE 1 ======
            "Injeção Cíclica de Vapor (CSS)": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para injeção cíclica de vapor! O reservatório tem características ideais: "
                    "óleo pesado (API < 25°) com viscosidade alta (50-10.000 cP) que responde bem ao aquecimento cíclico, profundidade adequada (150-2000m) "
                    "para contenção de vapor, e espessura suficiente (>5m) para ciclos eficientes. A saturação de óleo (>35%) garante volume para recuperação. "
                    "CSS é mais econômico que injeção contínua de vapor (30-40% menor CAPEX). Ideal para campos maduros em declínio."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para CSS com restrições. A viscosidade do óleo é adequada, mas a profundidade ou espessura "
                    "podem reduzir a eficiência dos ciclos. A saturação de óleo pode ser marginal. Recomenda-se análise de produção acumulada por ciclo "
                    "e estudo de aquecimento não uniforme."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para CSS. O óleo pode ser muito leve (API > 25°) para responder adequadamente ao aquecimento, "
                    "a profundidade pode ser excessiva (>2000m causando perdas de calor), ou a espessura é insuficiente (<5m para ciclos econômicos). "
                    "Recuperação por ciclo pode ser <2% do OOIP."
                )
            },
            "Injeção de Gás com Alternância de Água (WAG)": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Perfeito para WAG! O reservatório tem características excelentes: óleo leve (API > 20°) com baixa viscosidade (<50 cP) "
                    "que se mobiliza bem com gás, pressão adequada (>1000 psi) para miscibilidade parcial, e profundidade ideal (800-3500m) para operações offshore. "
                    "Permeabilidade (50-2000 mD) permite fluxo alternado eficiente. WAG reduz fingering de gás em 40-60% vs injeção contínua. "
                    "Recuperação adicional pode alcançar 15-25% do OOIP."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para WAG. A viscosidade e pressão podem estar nos limites, exigindo otimização de proporção gás/água. "
                    "A permeabilidade pode limitar a injeção alternada se muito baixa (<50) ou muito alta (>2000). Estudo de simulação necessário "
                    "para otimizar frequência de alternância e volume de gás."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para WAG. O óleo pode ser muito pesado (API < 20°) ou viscoso (>50 cP), "
                    "a pressão pode ser insuficiente (<1000 psi), ou a permeabilidade inadequada. Profundidade > 3500m torna operações complexas. "
                    "Risco alto de separação de fases e produção de água."
                )
            },
            "Injeção de Baixa Salinidade (LoSal)": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para LoSal! O reservatório tem condições ideais: água formação com alta salinidade (>30.000 ppm) "
                    "que pode ser reduzida por injeção de água fresca, óleo com TAN moderado (>0.2 mg KOH/g) para alteração de molhabilidade, "
                    "temperatura moderada (<100°C) para estabilidade da superfície, e permeabilidade adequada (10-2000 mD). LoSal aumenta recuperação em 5-15% "
                    "com CAPEX mínimo (apenas tratamento de água). Aplicável em campos existentes com poço de injeção."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para LoSal. A salinidade pode estar no limite inferior, ou o TAN pode ser marginal. "
                    "A temperatura pode afetar a adsorção de surfactante natural. Estudo de compatibilidade de água necessário para evitar inchamento de argila. "
                    "Testes de laboratório com fluidos reais recomendados."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não adequado para LoSal. A salinidade é baixa (<30.000 ppm), limitando benefício da redução. "
                    "O TAN é muito baixo (<0.2) para alteração significativa. A viscosidade pode ser muito alta (>200 cP) ou temperatura muito alta (>100°C). "
                    "Risco de inchamento de argila pode ser proibitivo. Custo vs benefício desfavorável."
                )
            },
            "Nanotecnologia aplicada ao EOR": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para nanotecnologia EOR! O reservatório tem ampla compatibilidade: óleo leve a médio (API 10-40°), "
                    "viscosidade variável (até 500 cP) permitindo uso de nanopartículas, salinidade qualquer (nanotecnologia tolerante a sal), "
                    "temperatura moderada (20-120°C), e permeabilidade adequada (1-5000 mD). Nanopartículas aumentam mobilidade do óleo em 10-30%, "
                    "reduzem tensão interfacial e aumentam eficiência de varrimento. Custo de implementação: US$ 1-3/bbl. "
                    "Tecnologia versátil aplicável a múltiplos cenários."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para nanotecnologia. Alguns parâmetros podem limitar eficiência (viscosidade muito alta, "
                    "salinidade extrema, temperatura limite). Recomenda-se estudo de compatibilidade de nanopartículas com fluidos do reservatório. "
                    "Avaliação de agregação e estabilidade em condições de fundo de poço necessária."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Restrições para nanotecnologia. Limitações severas em salinidade excessiva (>200.000 ppm) causando agregação, "
                    "temperatura muito alta (>120°C) causando degradação, ou óleo com propriedades químicas incompatíveis. Permeabilidade extrema "
                    "(<1 mD causar entupimento, >5000 mD perder nanopartículas). Custo-benefício desfavorável em cenários limitados."
                )
            },
            "EOR Térmico para Águas Profundas": {
                "alta": (
                    "🟢 ALTA SUITABILITY - Excelente para EOR térmico em águas profundas! O reservatório tem características adequadas: "
                    "óleo pesado (API < 24°) com viscosidade significativa (80-5000 cP) que responde bem ao aquecimento, profundidade (1000-3500m) "
                    "ideal para campos offshore profundos de Angola, temperatura de fundo moderada (<130°C), e pressão necessária (>500 psi) para operações submarinas. "
                    "Sistemas de injeção de vapor isolados termicamente permitem eficiência em água profunda. Recuperação adicional: 10-20% do OOIP. "
                    "Aplicável em campos como Bloco 15, 17, 18 de Angola."
                ),
                "media": (
                    "🟡 SUITABILITY MÉDIA - Potencial para EOR térmico deepwater. A viscosidade ou profundidade podem estar nos limites. "
                    "O desafio principal é a eficiência térmica em água profunda fria (risco de perda de calor >40%). "
                    "Recomenda-se simulação térmica com modelos dinâmicos e análise de viabilidade econômica considerando custo de infraestrutura submarinha."
                ),
                "baixa": (
                    "🔴 BAIXA SUITABILITY - Não recomendado para EOR térmico deepwater. O óleo pode ser muito leve (API > 24°) para justificar custo térmico, "
                    "a profundidade > 3500m torna infraestrutura proibitivamente cara, ou temperatura de fundo > 130°C causa instabilidade. "
                    "Perdas de calor podem exceder 50%, tornando o método economicamente inviável. Custo CAPEX pode exceder US$ 100M/poço."
                )
            }
        }

    
    def score_reservoir(self, reservoir_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Calcula pontuação para cada método EOR com justificações detalhadas.
        
        Args:
            reservoir_data: Dicionário com parâmetros do reservatório
            
        Returns:
            Dict com scores e análises para cada método
            
        Raises:
            ValueError: Se dados do reservatório inválidos
        """
        if not reservoir_data or not isinstance(reservoir_data, dict):
            raise ValueError("Dados de reservatório inválidos ou vazio")
        
        scores = {}
        
        for method, criteria in self.criteria.items():
            try:
                score = self._calculate_method_score(method, criteria, reservoir_data)
                scores[method] = score
                logger.info(f"Score calculado para {method}: {score['score']:.1f}%")
            except Exception as e:
                logger.error(f"Erro ao calcular score para {method}: {str(e)}")
                # Usar score padrão em caso de erro
                scores[method] = {
                    'score': 0,
                    'status': 'ERRO',
                    'color': 'gray',
                    'justificativa': f'Erro ao processar método: {str(e)}',
                    'pontos_positivos': [],
                    'pontos_negativos': [str(e)],
                    'criteria_scores': {}
                }
        
        return scores
    
    def _calculate_method_score(self, method: str, criteria: Dict, 
                               reservoir_data: Dict) -> Dict[str, Any]:
        """Calcula score detalhado para um método específico.
        
        Args:
            method: Nome do método EOR
            criteria: Critérios específicos do método
            reservoir_data: Dados do reservatório
            
        Returns:
            Dict com análise completa do método
        """
        score = 0.0
        max_score = 0.0
        pontos_positivos = []
        pontos_negativos = []
        criteria_scores = {}
        
        for param, limits in criteria.items():
            weight = limits.get("peso", 0)
            max_score += weight * 100
            
            if param not in reservoir_data or reservoir_data[param] is None:
                pontos_negativos.append(f"Parâmetro '{param}' não disponível")
                criteria_scores[param] = 0
                continue
            
            value = float(reservoir_data[param])
            
            # Avaliar se o valor está dentro dos limites
            if limits.get("min") is not None and value < limits["min"]:
                pontos_negativos.append(
                    f"{param}: {value:.2f} abaixo do mínimo ({limits['min']})"
                )
                criteria_scores[param] = 0
            elif limits.get("max") is not None and value > limits["max"]:
                pontos_negativos.append(
                    f"{param}: {value:.2f} acima do máximo ({limits['max']})"
                )
                criteria_scores[param] = 0
            else:
                score += weight * 100
                pontos_positivos.append(
                    f"{param} ({value:.2f}) dentro dos limites ✓"
                )
                criteria_scores[param] = weight * 100
        
        # Normalizar score
        normalized_score = (score / max_score * 100) if max_score > 0 else 0
        normalized_score = min(100, max(0, normalized_score))  # Limitar entre 0-100
        
        # Determinar status baseado em thresholds
        if normalized_score >= SUITABILITY_THRESHOLDS['alta']:
            status = "RECOMENDADO"
            color = "green"
            justificativa = self.justifications.get(method, {}).get("alta", "")
        elif normalized_score >= SUITABILITY_THRESHOLDS['media']:
            status = "POTENCIAL"
            color = "orange"
            justificativa = self.justifications.get(method, {}).get("media", "")
        else:
            status = "NÃO RECOMENDADO"
            color = "red"
            justificativa = self.justifications.get(method, {}).get("baixa", "")
        
        return {
            "score": normalized_score,
            "status": status,
            "color": color,
            "justificativa": justificativa,
            "pontos_positivos": pontos_positivos[:5],  # Limitar a 5
            "pontos_negativos": pontos_negativos[:5],  # Limitar a 5
            "criteria_scores": criteria_scores,
            "max_score": max_score
        }
    
    def get_recommendations(self, reservoir_data: Dict[str, Any], 
                           top_n: int = 3) -> List[Tuple[str, Dict]]:
        """Retorna os top_n métodos recomendados.
        
        Args:
            reservoir_data: Dados do reservatório
            top_n: Número de recomendações (padrão: 3)
            
        Returns:
            Lista com top_n métodos e seus scores
        """
        scores = self.score_reservoir(reservoir_data)
        sorted_methods = sorted(scores.items(), 
                               key=lambda x: x[1]["score"], reverse=True)
        return sorted_methods[:min(top_n, len(sorted_methods))]
    
    def generate_justification_report(self, reservoir_data: Dict[str, Any], 
                                     scores: Optional[Dict] = None) -> str:
        """Gera relatório completo de justificações.
        
        Args:
            reservoir_data: Dados do reservatório
            scores: Scores pré-calculados (opcional)
            
        Returns:
            String com relatório formatado
        """
        if scores is None:
            scores = self.score_reservoir(reservoir_data)
        
        report = []
        report.append("=" * 100)
        report.append("RELATÓRIO DE JUSTIFICAÇÕES E SUITABILITY - PETROCHAMP")
        report.append("=" * 100)
        report.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append(f"Versão: 6.0 - Análise Avançada")
        report.append("")
        
        # Resumo dos dados do reservatório
        report.append("\nDADOS DO RESERVATÓRIO:")
        report.append("-" * 50)
        for param, value in list(reservoir_data.items())[:5]:
            if value is not None:
                report.append(f"  {param}: {value}")
        if len(reservoir_data) > 5:
            report.append(f"  ... ({len(reservoir_data) - 5} parâmetros adicionais)")
        
        # Ordenar por pontuação
        sorted_methods = sorted(scores.items(), 
                               key=lambda x: x[1]["score"], reverse=True)
        
        report.append("\n" + "=" * 100)
        report.append("ANÁLISE DETALHADA POR MÉTODO")
        report.append("=" * 100)
        
        for idx, (method, data) in enumerate(sorted_methods, 1):
            report.append(f"\n[{idx}] {method.upper()}")
            report.append("-" * 80)
            report.append(f"Pontuação de Suitability: {data['score']:.1f}%")
            report.append(f"Status: {data['status']}")
            
            # Ícone de semáforo
            if data['score'] >= SUITABILITY_THRESHOLDS['alta']:
                report.append("🟢 SUITABILITY ALTA - Fortemente recomendado")
            elif data['score'] >= SUITABILITY_THRESHOLDS['media']:
                report.append("🟡 SUITABILITY MÉDIA - Potencial com ressalvas")
            else:
                report.append("🔴 SUITABILITY BAIXA - Não recomendado")
            
            report.append("\nJustificativa:")
            report.append(data['justificativa'])
            
            # Análise de suitability
            report.append("\nAnálise de Suitability:")
            report.append(f"  • Score Técnico: {data['score']:.1f}%")
            total_criteria = len(data.get('criteria_scores', {}))
            met_criteria = sum(1 for v in data.get('criteria_scores', {}).values() if v > 0)
            report.append(f"  • Critérios atendidos: {met_criteria}/{total_criteria}")
            
            if data['pontos_positivos']:
                report.append("\n  PONTOS FORTES:")
                for ponto in data['pontos_positivos']:
                    report.append(f"    ✓ {ponto}")
            
            if data['pontos_negativos']:
                report.append("\n  PONTOS A MELHORAR:")
                for ponto in data['pontos_negativos']:
                    report.append(f"    ✗ {ponto}")
            
            # Recomendações específicas
            report.append("\n  RECOMENDAÇÃO:")
            if data['score'] >= SUITABILITY_THRESHOLDS['alta']:
                report.append("    → Proceder com estudo detalhado de viabilidade")
                report.append("    → Considerar piloto ou implementação direta")
                report.append("    → Alto potencial de retorno econômico")
            elif data['score'] >= SUITABILITY_THRESHOLDS['media']:
                report.append("    → Realizar estudos adicionais de laboratório")
                report.append("    → Considerar modificações no método")
                report.append("    → Avaliar risco técnico e econômico")
            else:
                report.append("    → Não recomendado para implementação atual")
                report.append("    → Considerar métodos alternativos")
                report.append("    → Reavaliar se novos dados estiverem disponíveis")
        
        # Conclusões finais
        report.append(f"\n{'=' * 100}")
        report.append("CONCLUSÕES E RECOMENDAÇÕES FINAIS")
        report.append("=" * 100)
        
        best_method, best_data = sorted_methods[0] if sorted_methods else (None, {})
        
        if best_data and best_data.get('score', 0) >= SUITABILITY_THRESHOLDS['alta']:
            report.append("\n🟢 Reservatório com ALTA SUITABILITY para EOR")
            report.append(f"   Melhor método: {best_method} ({best_data['score']:.1f}%)")
            if len(sorted_methods) > 1:
                second_method, second_data = sorted_methods[1]
                if second_data.get('score', 0) >= SUITABILITY_THRESHOLDS['alta']:
                    report.append(f"   Método alternativo: {second_method} ({second_data['score']:.1f}%)")
        elif best_data and best_data.get('score', 0) >= SUITABILITY_THRESHOLDS['media']:
            report.append("\n🟡 Reservatório com SUITABILITY MÉDIA para EOR")
            report.append(f"   Melhor candidato: {best_method} ({best_data['score']:.1f}%)")
            report.append("   Recomenda-se estudo detalhado de viabilidade técnica e econômica")
        else:
            report.append("\n🔴 Reservatório com BAIXA SUITABILITY para EOR")
            if best_method:
                report.append(f"   Melhor método (ainda assim não ideal): {best_method} ({best_data.get('score', 0):.1f}%)")
            report.append("   Recomenda-se manter com recuperação primária/secundária")
            report.append("   Ou reavalie com dados mais completos do reservatório")
        
        # Estatísticas finais
        alta = sum(1 for _, d in sorted_methods if d['score'] >= SUITABILITY_THRESHOLDS['alta'])
        media = sum(1 for _, d in sorted_methods 
                   if SUITABILITY_THRESHOLDS['media'] <= d['score'] < SUITABILITY_THRESHOLDS['alta'])
        baixa = sum(1 for _, d in sorted_methods if d['score'] < SUITABILITY_THRESHOLDS['media'])
        
        report.append("\nESTATÍSTICAS DE SUITABILITY:")
        report.append(f"  • Métodos com alta suitability (≥{SUITABILITY_THRESHOLDS['alta']}%): {alta}/15")
        report.append(f"  • Métodos com suitability média ({SUITABILITY_THRESHOLDS['media']}-{SUITABILITY_THRESHOLDS['alta']-1}%): {media}/15")
        report.append(f"  • Métodos com baixa suitability (<{SUITABILITY_THRESHOLDS['media']}%): {baixa}/15")
        
        report.append("\n" + "=" * 100)
        
        return "\n".join(report)

# ============================================================================
# MÓDULO DE ANÁLISE ECONÔMICA MELHORADO
# ============================================================================

class EconomicAnalyzer:
    """Analisador econômico completo para projetos EOR.
    
    Responsável por cálculos financeiros incluindo NPV, IRR, Payback
    e análise de viabilidade econômica dos projetos.
    """
    
    DEFAULT_PARAMS = {
        "oil_price": 60.0,          # USD/bbl
        "capex_multiplier": 5000,   # Multiplicador de CAPEX
        "opex_percentage": 30,      # Percentual da receita
        "discount_rate": 10,        # Taxa de desconto (%)
        "tax_rate": 25,             # Alíquota de imposto (%)
        "project_life": 15,         # Vida do projeto (anos)
        "construction_time": 2,     # Tempo de construção (anos)
        "decline_rate": 15          # Taxa de declínio (%/ano)
    }
    
    def __init__(self):
        """Inicializa analisador econômico com parâmetros padrão."""
        self.default_params = self.DEFAULT_PARAMS.copy()
        logger.info("EconomicAnalyzer inicializado")
    
    def calculate_cash_flow(self, production_profile: List[float], 
                           economic_params: Dict[str, float]) -> Dict[str, Any]:
        """Calcula fluxo de caixa completo do projeto.
        
        Args:
            production_profile: Lista de produção anual (bbl/dia)
            economic_params: Parâmetros econômicos customizados
            
        Returns:
            Dict com fluxo de caixa, receita, OPEX e CAPEX
            
        Raises:
            ValueError: Se dados inválidos
        """
        try:
            if not production_profile or len(production_profile) == 0:
                raise ValueError("Perfil de produção vazio")
            
            params = {**self.default_params, **economic_params}
            
            # Validar parâmetros críticos
            if params["oil_price"] <= 0:
                raise ValueError("Preço do óleo deve ser positivo")
            if params["construction_time"] <= 0:
                raise ValueError("Tempo de construção deve ser positivo")
            
            # Converter produção para array numpy
            production = np.array([float(p) for p in production_profile])
            annual_production = production * 365  # Converter bbl/dia para bbl/ano
            
            # Calcular receita
            revenue = annual_production * params["oil_price"]
            
            # Calcular CAPEX
            total_capex = params.get("capex", production[0] * params["capex_multiplier"])
            capex_per_year = total_capex / max(params["construction_time"], 1)
            
            # Calcular OPEX
            opex = revenue * (params["opex_percentage"] / 100)
            operational_cf = revenue - opex
            
            # Construir fluxo de caixa completo
            construction_years = int(params["construction_time"])
            total_years = len(production) + construction_years
            cash_flow = np.zeros(total_years)
            
            # Fase de construção (CAPEX negativo)
            for i in range(construction_years):
                cash_flow[i] = -capex_per_year
            
            # Fase operacional
            for i in range(len(production)):
                cash_flow[i + construction_years] = operational_cf[i]
            
            # Aplicar impostos
            taxable_income = cash_flow.copy()
            taxable_income[taxable_income > 0] *= (1 - params["tax_rate"] / 100)
            
            logger.info(f"Fluxo de caixa calculado: {total_years} anos")
            
            return {
                "cash_flow": cash_flow.tolist(),
                "revenue": revenue.tolist(),
                "opex": opex.tolist(),
                "capex": float(total_capex),
                "years": total_years,
                "taxable_income": taxable_income.tolist()
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular fluxo de caixa: {str(e)}")
            raise
    
    def calculate_npv(self, cash_flow: List[float], discount_rate: float) -> float:
        """Calcula Valor Presente Líquido (NPV).
        
        Args:
            cash_flow: Lista de fluxos de caixa anuais
            discount_rate: Taxa de desconto (%)
            
        Returns:
            NPV em USD
        """
        try:
            cf_array = np.array([float(cf) for cf in cash_flow])
            periods = np.arange(len(cf_array), dtype=float)
            discount_factor = (1 + discount_rate / 100) ** periods
            npv = np.sum(cf_array / discount_factor)
            
            logger.info(f"NPV calculado: ${npv:,.2f}")
            return float(npv)
            
        except Exception as e:
            logger.error(f"Erro ao calcular NPV: {str(e)}")
            raise
    
    def calculate_irr(self, cash_flow: List[float], precision: float = 0.0001) -> float:
        """Calcula Taxa Interna de Retorno (IRR).
        
        Args:
            cash_flow: Lista de fluxos de caixa anuais
            precision: Precisão desejada para cálculo
            
        Returns:
            IRR em percentual (%)
        """
        try:
            if HAS_NUMPY_FINANCIAL:
                irr_value = npf.irr(cash_flow)
                if irr_value is not None and not np.isnan(irr_value):
                    return float(irr_value * 100)
                else:
                    logger.warning("IRR retornou valor inválido, usando método manual")
                    return self._calculate_irr_manual(cash_flow, precision)
            else:
                return self._calculate_irr_manual(cash_flow, precision)
                
        except Exception as e:
            logger.error(f"Erro ao calcular IRR: {str(e)}")
            return 0.0
    
    def _calculate_irr_manual(self, cash_flow: List[float], 
                             precision: float = 0.0001) -> float:
        """Calcula IRR usando método de bisseção.
        
        Args:
            cash_flow: Lista de fluxos de caixa
            precision: Tolerância de convergência
            
        Returns:
            IRR em percentual (%)
        """
        def npv_func(rate: float) -> float:
            """Calcula NPV para uma taxa específica."""
            periods = np.arange(len(cash_flow), dtype=float)
            return np.sum(np.array(cash_flow) / ((1 + rate) ** periods))
        
        # Usar bisseção para encontrar a taxa
        low, high = -0.99, 2.0
        max_iterations = 1000
        
        try:
            for iteration in range(max_iterations):
                mid = (low + high) / 2
                val = npv_func(mid)
                
                if abs(val) < precision:
                    logger.info(f"IRR encontrado em {iteration} iterações: {mid*100:.2f}%")
                    return mid * 100
                
                # Ajustar intervalo
                if npv_func(low) * val < 0:
                    high = mid
                else:
                    low = mid
            
            logger.warning(f"IRR não convergiu após {max_iterations} iterações")
            return mid * 100
            
        except Exception as e:
            logger.error(f"Erro no cálculo manual de IRR: {str(e)}")
            return 0.0
    
    def calculate_payback(self, cash_flow: List[float]) -> Optional[float]:
        """Calcula período de payback (em anos).
        
        Args:
            cash_flow: Lista de fluxos de caixa anuais
            
        Returns:
            Período de payback em anos, ou None se não alcançado
        """
        try:
            cumulative = np.cumsum(cash_flow)
            
            # Encontrar quando cumulative viira positivo
            for i, val in enumerate(cumulative):
                if val >= 0:
                    if i == 0:
                        return 0.0
                    
                    # Interpolação linear para maior precisão
                    prev_val = cumulative[i - 1]
                    year_fraction = abs(prev_val) / abs(val - prev_val) if (val - prev_val) != 0 else 0
                    payback = i - 1 + year_fraction
                    
                    logger.info(f"Payback calculado: {payback:.2f} anos")
                    return float(payback)
            
            logger.warning("Payback não alcançado durante período do projeto")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao calcular payback: {str(e)}")
            return None
    
    def generate_production_profile(self, initial_rate: float, 
                                   decline_rate: float, 
                                   years: int) -> List[float]:
        """Gera perfil de produção com declínio exponencial.
        
        Args:
            initial_rate: Taxa inicial de produção (bbl/dia)
            decline_rate: Taxa de declínio anual (%)
            years: Número de anos
            
        Returns:
            Lista com produção anual
            
        Raises:
            ValueError: Se parâmetros inválidos
        """
        try:
            if initial_rate <= 0:
                raise ValueError("Taxa inicial deve ser positiva")
            if not (0 <= decline_rate < 100):
                raise ValueError("Taxa de declínio deve estar entre 0 e 100%")
            if years <= 0:
                raise ValueError("Número de anos deve ser positivo")
            
            profile = []
            years = int(years)
            decline_factor = (100 - decline_rate) / 100
            
            for year in range(years):
                production = initial_rate * (decline_factor ** year)
                profile.append(max(0, production))  # Não permitir negativo
            
            logger.info(f"Perfil de produção gerado: {years} anos, declínio de {decline_rate}%/ano")
            return profile
            
        except Exception as e:
            logger.error(f"Erro ao gerar perfil de produção: {str(e)}")
            raise
    
    def validate_economic_params(self, params: Dict[str, float]) -> bool:
        """Valida parâmetros econômicos.
        
        Args:
            params: Dicionário de parâmetros
            
        Returns:
            True se válidos, False caso contrário
        """
        critical_params = {
            'oil_price': (0, float('inf')),
            'discount_rate': (-100, 100),
            'tax_rate': (0, 100),
            'project_life': (1, 100),
            'decline_rate': (0, 100)
        }
        
        for param, (min_val, max_val) in critical_params.items():
            if param not in params:
                logger.warning(f"Parâmetro {param} não encontrado")
                continue
            
            val = params[param]
            if not (min_val <= val <= max_val):
                logger.error(f"Parâmetro {param} fora do intervalo [{min_val}, {max_val}]: {val}")
                return False
        
        return True
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


# ============================================================================
# MÓDULO DE UTILIDADES E CACHE
# ============================================================================

class CacheManager:
    """Gerenciador de cache para operações computacionalmente caras.
    
    Armazena resultados de cálculos para evitar recomputações
    desnecessárias quando dados não mudam.
    """
    
    def __init__(self, max_size: int = 100):
        """Inicializa cache com tamanho máximo.
        
        Args:
            max_size: Número máximo de entradas em cache
        """
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        logger.info(f"CacheManager inicializado com capacidade de {max_size} entradas")
    
    def _generate_key(self, obj: Any) -> str:
        """Gera chave hash para um objeto.
        
        Args:
            obj: Objeto para cachear
            
        Returns:
            String com hash do objeto
        """
        try:
            return str(hash(str(obj)))
        except:
            return str(id(obj))
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache.
        
        Args:
            key: Chave do cache
            
        Returns:
            Valor ou None se não encontrado
        """
        return self.cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        """Armazena valor no cache.
        
        Args:
            key: Chave do cache
            value: Valor a armazenar
        """
        if len(self.cache) >= self.max_size:
            # Remover entrada mais antiga
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = value
    
    def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
        logger.info("Cache limpo")


class DataValidator:
    """Validador de dados de entrada para a plataforma.
    
    Garante que os dados fornecidos estejam dentro de intervalos
    razoáveis e consistentes para análise.
    """
    
    # Intervalos razoáveis para parâmetros do reservatório
    VALID_RANGES = {
        'API': (5, 45),
        'Viscosidade': (0.1, 100000),
        'Profundidade': (50, 5000),
        'Permeabilidade': (0.001, 10000),
        'Porosidade': (0, 100),
        'Saturação de Óleo': (0, 100),
        'Saturação de Água': (0, 100),
        'Temperatura': (-50, 250),
        'Pressão': (0, 10000),
        'Salinidade': (0, 500000),
        'Espessura': (0.1, 500),
        'TAN': (0, 10),
        'pH': (0, 14),
        'Dip': (0, 90)
    }
    
    @staticmethod
    def validate_parameter(param_name: str, value: float) -> Tuple[bool, str]:
        """Valida um parâmetro individual.
        
        Args:
            param_name: Nome do parâmetro
            value: Valor a validar
            
        Returns:
            Tupla (válido, mensagem)
        """
        if param_name not in DataValidator.VALID_RANGES:
            return True, "Parâmetro não configurado para validação"
        
        min_val, max_val = DataValidator.VALID_RANGES[param_name]
        
        if value < min_val or value > max_val:
            msg = f"{param_name}: {value} fora do intervalo [{min_val}, {max_val}]"
            logger.warning(msg)
            return False, msg
        
        return True, "Ok"
    
    @staticmethod
    def validate_reservoir_data(reservoir_data: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Valida conjunto completo de dados do reservatório.
        
        Args:
            reservoir_data: Dicionário com parâmetros
            
        Returns:
            Tupla (válido, lista de erros)
        """
        errors = []
        
        for param, value in reservoir_data.items():
            if value is None:
                continue
            
            try:
                value_float = float(value)
                valid, msg = DataValidator.validate_parameter(param, value_float)
                if not valid:
                    errors.append(msg)
            except ValueError:
                errors.append(f"{param}: valor não é numérico")
        
        if errors:
            logger.warning(f"Erros de validação: {errors}")
            return False, errors
        
        return True, []
    
    @staticmethod
    def validate_consistency(reservoir_data: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Valida consistência entre parâmetros relacionados (NOVO).
        
        Implementa validações baseadas na física e geologia:
        - Saturação de óleo + água não pode > 100%
        - Porosidade não pode ser negativa
        - API e viscosidade devem ser consistentes
        - Profundidade e temperatura devem ser consistentes
        """
        errors = []
        warnings = []
        
        # Verificação 1: Saturação total
        if "Saturação de Óleo" in reservoir_data and "Saturação de Água" in reservoir_data:
            so = reservoir_data["Saturação de Óleo"]
            sw = reservoir_data["Saturação de Água"]
            if so + sw > 100.5:  # Tolerância de 0.5%
                errors.append(
                    f"Saturação total inválida: So={so}% + Sw={sw}% = {so+sw}% (máximo 100%)"
                )
            if so + sw < 60:
                warnings.append(
                    f"Saturação total baixa ({so+sw}%). Possível volume de gás não contabilizado?"
                )
        
        # Verificação 2: Consistência API-Viscosidade
        if "API" in reservoir_data and "Viscosidade" in reservoir_data:
            api = reservoir_data["API"]
            visc = reservoir_data["Viscosidade"]
            
            # API alto = óleo leve = viscosidade baixa
            if api > 30 and visc > 100:
                warnings.append(
                    f"API alto ({api}°) mas viscosidade alta ({visc} cP). "
                    f"Verificar dados - pode estar inconsistente"
                )
            
            # API baixo = óleo pesado = viscosidade alta
            if api < 15 and visc < 50:
                warnings.append(
                    f"API baixo ({api}°) mas viscosidade baixa ({visc} cP). "
                    f"Verificar dados - pode estar inconsistente"
                )
        
        # Verificação 3: Profundidade vs Temperatura
        if "Profundidade" in reservoir_data and "Temperatura" in reservoir_data:
            depth = reservoir_data["Profundidade"]
            temp = reservoir_data["Temperatura"]
            
            # Gradiente geotérmico esperado: ~1°C/30m
            expected_temp = 15 + (depth / 30)
            
            if temp < expected_temp * 0.8 or temp > expected_temp * 1.5:
                warnings.append(
                    f"Temperatura {temp}°C inconsistente com profundidade {depth}m. "
                    f"Esperado ~{expected_temp:.0f}°C (gradiente 1°C/30m)"
                )
        
        # Verificação 4: Pressão vs Profundidade
        if "Profundidade" in reservoir_data and "Pressão" in reservoir_data:
            depth = reservoir_data["Profundidade"]
            pressure = reservoir_data["Pressão"]
            
            # Gradiente de pressão esperado: ~0.45 psi/m
            expected_pressure = depth * 0.45
            
            if pressure < expected_pressure * 0.8 or pressure > expected_pressure * 1.3:
                warnings.append(
                    f"Pressão {pressure} psi inconsistente com profundidade {depth}m. "
                    f"Esperado ~{expected_pressure:.0f} psi (gradiente normal)"
                )
        
        # Verificação 5: Porosidade e Permeabilidade
        if "Porosidade" in reservoir_data and "Permeabilidade" in reservoir_data:
            porosity = reservoir_data["Porosidade"]
            perm = reservoir_data["Permeabilidade"]
            
            # Tendência geral: maior porosidade → maior permeabilidade
            if porosity < 15 and perm > 1000:
                warnings.append(
                    f"Porosidade baixa ({porosity}%) mas permeabilidade alta ({perm} mD). "
                    f"Verificar consistência"
                )
        
        # Verificação 6: TAN mínimo
        if "TAN" in reservoir_data:
            tan = reservoir_data["TAN"]
            if tan < 0.1:
                warnings.append(
                    f"TAN muito baixo ({tan}). Métodos alcalinos/químicos podem não ser efetivos"
                )
        
        # Verificação 7: pH e Salinidade
        if "pH" in reservoir_data and "Salinidade" in reservoir_data:
            ph = reservoir_data["pH"]
            salinity = reservoir_data["Salinidade"]
            
            if salinity > 150000 and (ph < 6 or ph > 8.5):
                warnings.append(
                    f"Salinidade extrema ({salinity} ppm) com pH extremo ({ph}). "
                    f"Risco de precipitação em métodos químicos"
                )
        
        return len(errors) == 0, errors + warnings


# ============================================================================
# MÓDULO DE SCREENING AVANÇADO COM PERGUNTAS TÉCNICAS
# ============================================================================

class AdvancedScreeningQuestions:
    """Sistema de perguntas de screening técnico baseado na literatura.
    
    Implementa as perguntas-chave da Tabela 4 do artigo acadêmico
    para cada categoria de EOR, permitindo análise detalhada antes
    da seleção de método.
    """
    
    SCREENING_QUESTIONS = {
        "Injeção de Vapor": [
            "Qual é a viscosidade do óleo? (Deve ser > 100 cP)",
            "API do óleo é < 22°? (Óleo pesado essencial)",
            "Profundidade < 1500m? (Perdas térmicas críticas)",
            "Qual é a espessura da camada? (Deve ser > 6m)",
            "Há heterogeneidade significativa?",
            "Permeabilidade vertical é adequada para segregação térmica?"
        ],
        "Combustão In Situ": [
            "Qual é a composição do óleo (API, SARA)?",
            "Permeabilidade > 50 mD?",
            "Temperatura = Espontaneidade para ignição a campo?",
            "Qual é o mecanismo esperado (rica/pobre)?",
            "Há acesso adequado a oxigênio ao longo do intervalo?",
            "Pressão de poros permite pressão de ar necessária?"
        ],
        "Injeção de CO2 Miscível": [
            "Qual é a Pressão Mínima de Miscibilidade (MMP)?",
            "Pressão do reservatório > MMP?",
            "API > 27° para atingir miscibilidade?",
            "Temperatura < 120°C?",
            "Fonte de CO₂ economicamente viável está disponível?",
            "Há possibilidade de alternância CO₂-água (WAG)?"
        ],
        "Injeção de Gás Imiscível": [
            "Qual é a saturação residual de óleo após waterflooding?",
            "Qual é o residual esperado para gás imiscível?",
            "Como será drenada a estrutura? (falhas, camadas finas)",
            "Há suficiente segregação gravitacional (mergulho > 10°)?",
            "Qual é a composição do gás disponível?",
            "Mobilidade do gás vs óleo residual?"
        ],
        "Polímero": [
            "Qual é a concentração de polímero necessária para controle de mobilidade?",
            "Qual parte do polímero será adsorvida nas argilas?",
            "Salinidade < 20.000 ppm para estabilidade do polímero?",
            "Temperatura < 90°C?",
            "pH entre 5-8 para evitar hidrólise?",
            "Permeabilidade suficiente para injeção sem plugging?"
        ],
        "Surfactante": [
            "Qual é o design do slug para atingir IFT ultrabaixa?",
            "Qual é a salinidade da água do reservatório?",
            "Como isso impactará a atividade do slug?",
            "Como será controlada a mobilidade do banco químico?",
            "Que recuperação de óleo residual é esperada?",
            "Há compatibilidade com argilas da rocha (adsorção)?"
        ],
        "Alcalina": [
            "TAN do óleo > 0.5 mg KOH/g para reação de sabão?",
            "Salinidade < 5.000 ppm?",
            "pH esperado do efluente < 9.5?",
            "Qual é a reação esperada com argilas?",
            "Há risco de precipitação de carbonato (escala)?",
            "Permeabilidade adequada para injeção contínua?"
        ],
        "Injeção de Água Inteligente": [
            "Qual é a composição iônica ideal?",
            "Como vai alterar a molhabilidade?",
            "Qual é o esperado incremento de recuperação?",
            "Há compatibilidade com sistemas presentes?",
            "Salinidade e composição são controladas?",
            "Há monitoramento de pressão em tempo real disponível?"
        ],
        "Térmico em Águas Profundas": [
            "Profundidade subsea < 3500m para viabilidade térmica?",
            "API < 24° (óleo pesado essencial)?",
            "Qual é a perdas térmica esperada no poço e formação?",
            "Há infraestrutura submarinha para suportar aquecimento?",
            "Temperatura pode ser mantida em faixa operacional?",
            "Custo de aquecimento profundo vs benefício de recuperação?"
        ],
        "Microbiano": [
            "Podem ser identificados micróbios apropriados?",
            "Qual é a temperatura e pH do reservatório?",
            "Há nutrientes suficientes para crescimento?",
            "Como os micróbios serão distribuídos uniformemente?",
            "Qual é o tempo esperado para colonização?",
            "Há risco de plugging por biofilme?"
        ]
    }
    
    METHODS_CATEGORIES = {
        "Térmico": ["Injeção de Vapor", "Combustão In Situ", "EOR Térmico para Águas Profundas"],
        "Químico": ["Injeção de Polímeros", "Injeção de Surfactantes", "Injeção Alcalina", 
                    "Injeção de Água Inteligente"],
        "Miscível": ["Injeção de CO2 Miscível", "Injeção de Gás com Alternância de Água (WAG)"],
        "Imiscível": ["Injeção de Gás Não-Miscível", "Injeção de Nitrogênio"],
        "Outros": ["Injeção Microbiana", "Nanotecnologia aplicada ao EOR"]
    }
    
    @staticmethod
    def get_questions_by_method(method_name: str) -> List[str]:
        """Retorna lista de perguntas screening para um método específico."""
        return AdvancedScreeningQuestions.SCREENING_QUESTIONS.get(method_name, [])
    
    @staticmethod
    def get_category(method_name: str) -> Optional[str]:
        """Identifica categoria principal de um método."""
        for category, methods in AdvancedScreeningQuestions.METHODS_CATEGORIES.items():
            if method_name in methods:
                return category
        return None


class OffshoreSpecificCriteria:
    """Critérios específicos para campos offshore e deepwater (Angola).
    
    Implementa validações e adaptações de critérios para ambiente offshore,
    considerando:
    - Profundidade subsea vs profundidade estrutural
    - Custos operacionais aumentados
    - Limitações de infraestrutura
    - Considerações logísticas
    """
    
    # Classificação por profundidade (SPE IADC)
    DEPTH_CLASSIFICATION = {
        "Águas Rasas": (0, 500),          # < 500m subsea
        "Águas Intermediárias": (500, 1500),  # 500-1500m subsea
        "Águas Profundas": (1500, 3000),     # 1500-3000m subsea
        "Águas Ultraprofundas": (3000, 6000) # > 3000m subsea
    }
    
    # Fatores de multiplicação de custo por profundidade
    COST_MULTIPLIERS = {
        "Águas Rasas": 1.0,
        "Águas Intermediárias": 2.5,
        "Águas Profundas": 5.0,
        "Águas Ultraprofundas": 8.0
    }
    
    # Critérios adaptados para offshore
    OFFSHORE_CRITERIA = {
        "Espaçamento Poços": {
            "Onshore": (200, 500),      # metros
            "Offshore Raso": (500, 1000),
            "Offshore Profundo": (1000, 3000)
        },
        "Capex Injeção": {
            "Onshore": (5000, 15000),   # US$/dia
            "Offshore Raso": (25000, 75000),
            "Offshore Profundo": (100000, 500000)
        },
        "Infra Redimensionamento": {
            "Onshore": "Baixa",
            "Offshore Raso": "Média",
            "Offshore Profundo": "Alta"
        }
    }
    
    # Campos de referência Angola (Blocos)
    ANGOLA_BLOCKS = {
        "Bloco 15": {
            "profundidade_agua": 400,   # m subsea
            "tipo": "Offshore Raso",
            "status": "Ativo",
            "operador": "Sonangol/Total"
        },
        "Bloco 17": {
            "profundidade_agua": 800,
            "tipo": "Offshore Intermediário",
            "status": "Ativo",
            "operador": "Sonangol/TotalEnergies"
        },
        "Bloco 18": {
            "profundidade_agua": 1200,
            "tipo": "Offshore Profundo",
            "status": "Ativo",
            "operador": "Sonangol"
        },
        "Bloco 31": {
            "profundidade_agua": 300,
            "tipo": "Offshore Raso",
            "status": "Maduro",
            "operador": "Sonangol"
        },
        "Cabinda": {
            "profundidade_agua": 100,
            "tipo": "Onshore/Transição",
            "status": "Maduro",
            "operador": "Sonangol/ChevronTexaco"
        }
    }
    
    @staticmethod
    def get_water_depth_classification(depth_subsea: float) -> str:
        """Classifica profundidade em categoria SPE IADC."""
        for category, (min_d, max_d) in OffshoreSpecificCriteria.DEPTH_CLASSIFICATION.items():
            if min_d <= depth_subsea < max_d:
                return category
        return "Águas Ultraprofundas"
    
    @staticmethod
    def get_cost_multiplier(depth_subsea: float) -> float:
        """Retorna multiplicador de custo para profundidade."""
        category = OffshoreSpecificCriteria.get_water_depth_classification(depth_subsea)
        return OffshoreSpecificCriteria.COST_MULTIPLIERS.get(category, 8.0)
    
    @staticmethod
    def validate_offshore_feasibility(method_name: str, 
                                     depth_subsea: float,
                                     reservoir_depth: float) -> Tuple[bool, str]:
        """Valida viabilidade técnica de método em ambiente offshore.
        
        Args:
            method_name: Nome do método EOR
            depth_subsea: Profundidade de lâmina d'água (m)
            reservoir_depth: Profundidade da estrutura (m)
            
        Returns:
            Tupla (viável, justificativa)
        """
        category = OffshoreSpecificCriteria.get_water_depth_classification(depth_subsea)
        
        # Métodos térmicos difíceis em deepwater
        if method_name in ["Injeção de Vapor", "Combustão In Situ"] and depth_subsea > 2000:
            return False, f"Perdas térmicas críticas em {category}. Profundidade subsea {depth_subsea}m > 2000m"
        
        # Métodos miscíveis requerem pressão suficiente
        if "CO2 Miscível" in method_name and depth_subsea < 800:
            return False, "Pressão insuficiente em águas rasas para alcançar MMP de CO₂"
        
        # Métodos químicos com deposição de sais em profundidade
        if any(x in method_name for x in ["Polímero", "Surfactante"]) and depth_subsea > 3000:
            return False, f"Risco alto de degradação em {category}. Recomenda-se avaliação piloto"
        
        return True, f"Viável tecnicamente em {category} (profundidade subsea: {depth_subsea}m)"


class EfficiencyCalculator:
    """Calculadora de eficiência de deslocamento microscópico e macroscópico.
    
    Implementa cálculos baseados no artigo:
    - Número capilar (Nc)
    - Eficiência de deslocamento (PSD)
    - Eficiência de varredura (SE)
    - Fator de recuperação (RF)
    """
    
    @staticmethod
    def calculate_capillary_number(velocity: float, viscosity: float, 
                                   ift: float, contact_angle: float = 0) -> float:
        """Calcula número capilar (Equação 2 do artigo).
        
        Nc = (v * μ) / (σ * cos(θ))
        
        Args:
            velocity: Velocidade do fluido (ft/dia ou m/dia)
            viscosity: Viscosidade dinâmica (cP)
            ift: Tensão interfacial óleo-água (dinas/cm ou N/m)
            contact_angle: Ângulo de contato (graus)
            
        Returns:
            Número capilar adimensional
        """
        cos_theta = np.cos(np.radians(contact_angle))
        
        # Conversão de unidades para consistência
        # Se usar dinas/cm, resultado é adimensional direto
        if cos_theta == 0:
            cos_theta = 1.0
        
        nc = (velocity * viscosity) / (ift * abs(cos_theta))
        return nc
    
    @staticmethod
    def interpret_capillary_number(nc: float) -> Dict[str, Any]:
        """Interpreta significado do número capilar.
        
        Baseado em limites conhecidos:
        - Nc < 10^-8: Negligível (capilares dominam)
        - 10^-8 < Nc < 10^-6: Trapeamento (alguns capilares superados)
        - Nc > 10^-5: Drenagem completa possível
        """
        if nc < 1e-8:
            level = "Negligível"
            description = "Forças capilares dominam. Óleo residual alto."
            recovery_potential = "Baixa"
        elif nc < 1e-6:
            level = "Intermediário"
            description = "Alguns capilares superados. Redução de residual."
            recovery_potential = "Média"
        else:
            level = "Alto"
            description = "Capilares superados. Drenagem eficiente."
            recovery_potential = "Alta"
        
        return {
            "capillary_number": nc,
            "level": level,
            "description": description,
            "recovery_potential": recovery_potential,
            "log_nc": np.log10(nc) if nc > 0 else -np.inf
        }
    
    @staticmethod
    def calculate_microscopic_displacement_efficiency(ift: float, 
                                                     contact_angle: float,
                                                     oil_viscosity: float,
                                                     injection_viscosity: float,
                                                     velocity: float) -> float:
        """Estima eficiência de deslocamento microscópico (PSD).
        
        Considera tensão interfacial, molhabilidade e número capilar.
        
        Returns:
            PSD (0-1)
        """
        nc = EfficiencyCalculator.calculate_capillary_number(
            velocity, oil_viscosity, ift, contact_angle
        )
        
        # Fórmula empírica baseada em Buckingham-Leverett
        # PSD aumenta com Nc
        if nc < 1e-8:
            psd = 0.5  # ~50% residual fica
        elif nc < 1e-6:
            psd = 0.7  # ~30% residual fica
        elif nc < 1e-4:
            psd = 0.85  # ~15% residual fica
        else:
            psd = 0.95  # ~5% residual fica
        
        return psd
    
    @staticmethod
    def calculate_sweep_efficiency(mobility_ratio: float, 
                                  aspect_ratio: float = 1.0,
                                  heterogeneity_factor: float = 1.0) -> float:
        """Estima eficiência de varredura macroscópica (SE).
        
        Args:
            mobility_ratio: M = (k_inj/μ_inj) / (k_oil/μ_oil)
            aspect_ratio: Razão comprimento/altura da camada
            heterogeneity_factor: Fator de heterogeneidade (0-1)
            
        Returns:
            SE (0-1)
        """
        # Fórmula de Dykstra-Parsons para mobilidade
        if mobility_ratio < 0.5:
            mobility_efficiency = 0.95
        elif mobility_ratio < 1.0:
            mobility_efficiency = 0.85
        elif mobility_ratio < 2.0:
            mobility_efficiency = 0.7
        elif mobility_ratio < 5.0:
            mobility_efficiency = 0.5
        else:
            mobility_efficiency = 0.3  # Razão de mobilidade desfavorável
        
        # Fator de geometria
        geometry_factor = 1.0 / (1.0 + 0.1 * np.sqrt(aspect_ratio))
        
        # Fator de heterogeneidade
        he_factor = heterogeneity_factor
        
        se = mobility_efficiency * geometry_factor * he_factor
        
        return min(se, 1.0)
    
    @staticmethod
    def calculate_recovery_factor(psd: float, se: float, 
                                 drainage: float = 0.95,
                                 time_factor: float = 1.0) -> Dict[str, Any]:
        """Calcula fator de recuperação (Equação 1 do artigo).
        
        RF = PSD × SE × D × T
        
        Returns:
            Dict com componentes e RF total
        """
        rf = psd * se * drainage * time_factor
        
        return {
            "RF_total": rf,
            "PSD": psd,  # Deslocamento microscópico
            "SE": se,    # Varredura macroscópica
            "D": drainage,  # Drenagem
            "T": time_factor,  # Tempo
            "RF_percentage": rf * 100,
            "components": {
                "PSD_percentage": psd * 100,
                "SE_percentage": se * 100,
                "D_percentage": drainage * 100,
                "T_factor": time_factor
            }
        }


# ============================================================================
# MÓDULO DE VALIDAÇÃO TÉCNICA AVANÇADA - SISTEMA DE RED FLAGS
# ============================================================================

class TechnicalRedFlags:
    """Sistema de validação técnica avançada com "red flags" automáticas.
    
    Implementa regras de inviabilidade técnica baseadas na literatura e
    experiência de campos angolanos. Detecta automaticamente combinações
    de parâmetros que tornam métodos tecnicamente inviáveis.
    """
    
    # Regras de inviabilidade por método
    INVIABILITY_RULES = {
        "Injeção de Vapor": [
            {"profundidade_max": 3500, "flag": "Profundidade > 3500m inviável para vapor por perdas térmicas"},
            {"api_min": 22.1, "flag": "API > 22° torna injeção de vapor anti-econômica"},
            {"viscosidade_min": 99, "flag": "Viscosidade < 100 cP não justifica custos de vapor"},
            {"espessura_min": 5.9, "flag": "Espessura < 6m reduz eficiência de varrimento para <40%"},
        ],
        "Combustão In Situ": [
            {"api_min": 25.1, "flag": "API > 25° causa combustão muito rápida (instável)"},
            {"api_max": 9.9, "flag": "API < 10° pode causar extração de óleo insuficiente"},
            {"permeabilidade_min": 49, "flag": "Permeabilidade < 50 mD insuficiente para fluxo de ar"},
            {"viscosidade_max": 50000, "flag": "Viscosidade > 50.000 cP pode bloquear fluxo de oxigênio"},
        ],
        "Injeção de CO2 Miscível": [
            {"profundidade_min": 799, "flag": "Profundidade < 800m insuficiente para MMP adequado"},
            {"pressao_min": 1199, "flag": "Pressão < 1200 psi (≈ 8.3 MPa) abaixo de MMP mínimo"},
            {"api_max": 26.9, "flag": "API < 27° pode não alcançar miscibilidade com CO2"},
            {"temperatura_max": 120.1, "flag": "Temperatura > 120°C aumenta MMP significativamente"},
        ],
        "Injeção de Polímeros": [
            {"salinidade_max": 20000.1, "flag": "Salinidade > 20.000 ppm causa degradação rápida de polímero"},
            {"temperatura_max": 90.1, "flag": "Temperatura > 90°C reduz vida útil de HPAM para <6 meses"},
            {"ph_min": 4.9, "flag": "pH < 5 causa hidrólise acelerada de polímero"},
            {"ph_max": 8.1, "flag": "pH > 8 causa precipitação de cátions (Ca, Mg)"},
            {"permeabilidade_min": 9, "flag": "Permeabilidade < 10 mD risco de plugging permanente"},
        ],
        "Injeção de Surfactantes": [
            {"salinidade_max": 10000.1, "flag": "Salinidade > 10.000 ppm causa salting-out do surfactante"},
            {"temperatura_max": 80.1, "flag": "Temperatura > 80°C reduz eficiência IFT em 50-70%"},
            {"saturacao_oleo_residual_min": 24.9, "flag": "Saturação residual < 25% não justifica custos (>US$5/bbl)"},
        ],
        "Injeção Alcalina": [
            {"tan_min": 0.49, "flag": "TAN < 0.5 mg KOH/g reação de sabão insuficiente"},
            {"salinidade_max": 5000.1, "flag": "Salinidade > 5.000 ppm consome alcali rapidamente"},
            {"ph_max": 9.1, "flag": "pH > 9.5 causa precipitação de carbonato (escala)"},
        ],
        "Injeção de Gás Não-Miscível": [
            {"dip_min": 9.9, "flag": "Mergulho < 10° insuficiente para segregação gravitacional"},
            {"viscosidade_max": 100.1, "flag": "Viscosidade > 100 cP reduz mobilidade de gás em 80%"},
        ],
        "Injeção de Nitrogênio": [
            {"profundidade_min": 1999, "flag": "Profundidade < 2000m: N2 não mantém fase gasosa"},
            {"pressao_min": 1499, "flag": "Pressão < 1500 psi: N2 pode condensar parcialmente"},
        ],
        "Nanotecnologia aplicada ao EOR": [
            {"salinidade_max": 200000.1, "flag": "Salinidade > 200.000 ppm causa agregação de nanopartículas"},
            {"temperatura_max": 120.1, "flag": "Temperatura > 120°C degrada a maioria das nanopartículas"},
        ],
        "EOR Térmico para Águas Profundas": [
            {"profundidade_min": 3500.1, "flag": "Profundidade > 3500m: perdas térmicas > 50%, inviável"},
            {"api_min": 24.1, "flag": "API > 24°: custo térmica supera benefício de recuperação"},
            {"temperatura_max": 130.1, "flag": "Temperatura > 130°C reduz estabilidade em 40%"},
        ],
    }
    
    @staticmethod
    def check_reservoir_inviability(reservoir_data: Dict[str, Any], method: str) -> List[Dict]:
        """Detecta inviabilidades técnicas para um método específico.
        
        Args:
            reservoir_data: Dados do reservatório
            method: Nome do método EOR
            
        Returns:
            Lista de red flags detectadas
        """
        red_flags = []
        
        if method not in TechnicalRedFlags.INVIABILITY_RULES:
            return red_flags
        
        rules = TechnicalRedFlags.INVIABILITY_RULES[method]
        
        for rule in rules:
            for param_rule, value_limit in rule.items():
                if param_rule == "flag":
                    continue
                
                # Extrair nome do parâmetro e tipo de comparação
                if "_max" in param_rule:
                    param_name = param_rule.replace("_max", "")
                    param_value = reservoir_data.get(param_name)
                    if param_value is not None and param_value > value_limit:
                        red_flags.append({
                            "método": method,
                            "parâmetro": param_name,
                            "valor": param_value,
                            "limite": value_limit,
                            "tipo": "máximo excedido",
                            "mensagem": rule.get("flag", "Limite técnico excedido"),
                            "severidade": "CRÍTICA"
                        })
                
                elif "_min" in param_rule:
                    param_name = param_rule.replace("_min", "")
                    param_value = reservoir_data.get(param_name)
                    if param_value is not None and param_value < value_limit:
                        red_flags.append({
                            "método": method,
                            "parâmetro": param_name,
                            "valor": param_value,
                            "limite": value_limit,
                            "tipo": "mínimo não atingido",
                            "mensagem": rule.get("flag", "Limite técnico não atingido"),
                            "severidade": "CRÍTICA"
                        })
        
        return red_flags
    
    @staticmethod
    def check_all_methods_inviability(reservoir_data: Dict[str, Any], 
                                     all_methods: List[str]) -> Dict[str, List[Dict]]:
        """Executa verificação de inviabilidade para todos os métodos.
        
        Args:
            reservoir_data: Dados do reservatório
            all_methods: Lista de todos os métodos disponíveis
            
        Returns:
            Dicionário {método: [red_flags]}
        """
        all_flags = {}
        
        for method in all_methods:
            flags = TechnicalRedFlags.check_reservoir_inviability(
                reservoir_data, method
            )
            if flags:
                all_flags[method] = flags
        
        return all_flags
    
    @staticmethod
    def get_inviability_report(reservoir_data: Dict[str, Any], 
                              all_methods: List[str]) -> str:
        """Gera relatório textual de inviabilidades técnicas.
        
        Args:
            reservoir_data: Dados do reservatório
            all_methods: Lista de todos os métodos
            
        Returns:
            String com relatório formatado
        """
        all_flags = TechnicalRedFlags.check_all_methods_inviability(
            reservoir_data, all_methods
        )
        
        if not all_flags:
            return "✅ VALIDAÇÃO TÉCNICA: Nenhuma inviabilidade detectada"
        
        report = "⚠️ RELATÓRIO DE INVIABILIDADES TÉCNICAS (RED FLAGS)\n"
        report += "=" * 80 + "\n\n"
        
        for method, flags in all_flags.items():
            report += f"❌ {method}\n"
            report += "-" * 80 + "\n"
            for flag in flags:
                report += (
                    f"  • {flag['mensagem']}\n"
                    f"    Parâmetro: {flag['parâmetro']}\n"
                    f"    Valor: {flag['valor']:.2f} | Limite: {flag['limite']:.2f}\n"
                    f"    Severidade: {flag['severidade']}\n\n"
                )
        
        report += "\n" + "=" * 80 + "\n"
        report += f"RESUMO: {len(all_flags)} método(s) com inviabilidade técnica detectada\n"
        report += f"MÉTODOS VIÁVEIS: {len([m for m in all_methods if m not in all_flags])}/{len(all_methods)}\n"
        
        return report


# ============================================================================
# PLATAFORMA PRINCIPAL - PETROCHAMP
# ============================================================================
class PetroChampPlatform:
    """Plataforma principal PetroChamp com análise avançada de EOR.
    
    Interface gráfica completa para triagem técnica e análise econômica
    de projetos de recuperação terciária de petróleo usando 15 métodos EOR
    diferentes com análise de suitability e justificações automáticas.
    """
    
    def __init__(self):
        """Inicializa plataforma PetroChamp com todos os componentes."""
        try:
            # Configurar janela principal
            self.root = tk.Tk()
            self.root.title(WINDOW_CONFIG['title'])
            self.root.geometry(WINDOW_CONFIG['geometry'])
            self.root.minsize(*WINDOW_CONFIG['minsize'])
            
            # Inicializar componentes principais
            logger.info("Inicializando componentes principais...")
            self.screening_engine = EORScreeningEngine()
            self.economic_analyzer = EconomicAnalyzer()
            self.suitability_viz = SuitabilityVisualizer()
            
            # Inicializar utilidades
            self.cache_manager = CacheManager(max_size=100)
            self.data_validator = DataValidator()
            
            # Estado da aplicação
            self.current_project: Optional[str] = None
            self.reservoir_data: List[Dict[str, float]] = []
            self.screening_results: Optional[Dict] = None
            self.economic_results: Optional[Dict] = None
            self.justification_report: Optional[str] = None
            
            # Configurar tema e estilo visual
            self._setup_styling()
            
            # Construir interface
            logger.info("Construindo interface gráfica...")
            self._create_menu()
            self._create_main_interface()
            
            logger.info("PetroChamp inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar PetroChampPlatform: {str(e)}")
            raise
        
    def _setup_styling(self):
        """Configura estilos visuais e tema da aplicação."""
        try:
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            # Paleta de cores
            self.colors = {
                'primary': '#2c3e50',
                'secondary': '#3498db',
                'success': '#27ae60',
                'warning': '#f39c12',
                'danger': '#e74c3c',
                'light': '#ecf0f1',
                'dark': '#2c3e50'
            }
            
            # Aplicar cor de fundo
            self.root.configure(bg=self.colors['light'])
            
            logger.debug("Estilo visual configurado")
            
        except Exception as e:
            logger.error(f"Erro ao configurar estilo: {str(e)}")
        
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
        self._create_advanced_screening_tab()  # FASE 1B: Novo módulo de screening avançado
        self._create_fuzzy_selector_tab()  # FASE 2: Fuzzy Logic Selector
        self._create_monte_carlo_tab()  # FASE 3: Monte Carlo Analyzer
        
        self.status_bar = tk.Label(self.root, text="Pronto | PetroChamp v7.4 COMPLETO (Fases 1B + 2 + 3)", 
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
        
        # Aba de gráficos (EXPANDIDA)
        chart_tab = ttk.Frame(results_notebook)
        results_notebook.add(chart_tab, text="Gráficos")
        
        # Frame de controle de gráficos
        self.chart_control_frame = ttk.LabelFrame(chart_tab, text="Controles de Gráficos", padding=10)
        self.chart_control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(self.chart_control_frame, text="Tipo de Gráfico:").pack(side=tk.LEFT, padx=5)
        
        self.chart_type_var = tk.StringVar(value="barras")
        self.chart_type_combo = ttk.Combobox(
            self.chart_control_frame,
            textvariable=self.chart_type_var,
            values=["Barras", "Pizza", "Linha", "Área", "Radar", "Box Plot", "Dispersão", "Dashboard Completo"],
            state="readonly",
            width=25
        )
        self.chart_type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.chart_control_frame, text="Gerar Gráfico",
                  command=self.generate_custom_chart).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.chart_control_frame, text="Exportar Gráfico",
                  command=self.export_chart_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.chart_control_frame, text="Limpar",
                  command=self.clear_chart_results).pack(side=tk.LEFT, padx=5)
        
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
        """Cria aba específica para gráficos de suitability com estrutura reorganizada"""
        self.suitability_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.suitability_tab, text="Suitability")
        
        # Notebook principal para sub-abas
        self.suitability_notebook = ttk.Notebook(self.suitability_tab)
        self.suitability_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== SUB-ABA: MATRIZ =====
        self.matrix_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.matrix_frame, text="Matriz")
        
        # Controles para Matriz
        matrix_control_frame = ttk.LabelFrame(self.matrix_frame, text="Configuração da Matriz", padding=10)
        matrix_control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(matrix_control_frame, text="Métodos a avaliar:").pack(side=tk.LEFT, padx=5)
        
        # Botões de seleção rápida
        ttk.Button(matrix_control_frame, text="Todos", 
                  command=self._select_all_matrix_methods, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(matrix_control_frame, text="Nenhum", 
                  command=self._clear_matrix_methods, width=10).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(matrix_control_frame, text="Gerar Matriz",
                  command=self.show_suitability_matrix, width=15).pack(side=tk.LEFT, padx=10)
        
        # Frame para checkboxes de métodos
        methods_frame = ttk.LabelFrame(self.matrix_frame, text="Selecione Métodos", padding=10)
        methods_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Scrollable frame para métodos
        canvas = tk.Canvas(methods_frame, height=100, bg='white')
        scrollbar = ttk.Scrollbar(methods_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.matrix_method_vars = {}
        if hasattr(self, 'screening_engine'):
            for method in self.screening_engine.methods:
                var = tk.BooleanVar(value=True)
                self.matrix_method_vars[method] = var
                ttk.Checkbutton(scrollable_frame, text=method, variable=var).pack(anchor='w', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para matriz
        self.matrix_display_frame = ttk.Frame(self.matrix_frame)
        self.matrix_display_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # ===== SUB-ABA: VISÃO GERAL =====
        self.main_suitability_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.main_suitability_frame, text="Visão Geral")
        
        overview_control_frame = ttk.LabelFrame(self.main_suitability_frame, text="Gráficos de Visão Geral", padding=10)
        overview_control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(overview_control_frame, text="Gerar Gráficos",
                  command=self.generate_suitability_charts, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(overview_control_frame, text="Spider Chart",
                  command=self.show_spider_chart, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(overview_control_frame, text="Dashboard",
                  command=self.show_suitability_dashboard, width=15).pack(side=tk.LEFT, padx=5)
        
        # ===== SUB-ABA: GRÁFICOS INDIVIDUAIS =====
        self.individual_charts_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.individual_charts_frame, text="Gráficos Individuais")
        
        individual_control_frame = ttk.LabelFrame(self.individual_charts_frame, text="Configuração de Gráficos Individuais", padding=10)
        individual_control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(individual_control_frame, text="Método:").pack(side=tk.LEFT, padx=5)
        
        self.method_select_var = tk.StringVar()
        self.method_combo = ttk.Combobox(
            individual_control_frame,
            textvariable=self.method_select_var,
            state="readonly",
            width=30
        )
        self.method_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(individual_control_frame, text="Tipo:").pack(side=tk.LEFT, padx=5)
        
        self.individual_chart_type = tk.StringVar(value="Radar")
        ttk.Combobox(
            individual_control_frame,
            textvariable=self.individual_chart_type,
            values=["Radar", "Barras", "Linha", "Gauge", "Scorecard"],
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(individual_control_frame, text="Gerar",
                  command=self.show_individual_chart, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(individual_control_frame, text="Exportar",
                  command=self.export_individual_chart, width=15).pack(side=tk.LEFT, padx=5)
        
        # Frame para exibição
        self.individual_display_frame = ttk.Frame(self.individual_charts_frame)
        self.individual_display_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # ===== SUB-ABA: COMPARATIVO =====
        self.comparison_frame = ttk.Frame(self.suitability_notebook)
        self.suitability_notebook.add(self.comparison_frame, text="Comparativo")
        
        comparison_control_frame = ttk.LabelFrame(self.comparison_frame, text="Configuração de Comparativo", padding=10)
        comparison_control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(comparison_control_frame, text="Tipo de Gráfico:").pack(side=tk.LEFT, padx=5)
        
        self.comparison_chart_type = tk.StringVar(value="Radar")
        ttk.Combobox(
            comparison_control_frame,
            textvariable=self.comparison_chart_type,
            values=["Radar", "Barras", "Box Plot", "Dispersão", "Dashboard"],
            state="readonly",
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(comparison_control_frame, text="Todos os Métodos",
                  command=self._generate_comparison_all, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(comparison_control_frame, text="Métodos Selecionados",
                  command=self._generate_comparison_selected, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(comparison_control_frame, text="Exportar",
                  command=self._export_comparison_chart, width=15).pack(side=tk.LEFT, padx=5)
        
        # Frame para seleção de métodos
        comparison_methods_frame = ttk.LabelFrame(self.comparison_frame, text="Selecione Métodos para Comparação", padding=10)
        comparison_methods_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Scrollable frame
        canvas2 = tk.Canvas(comparison_methods_frame, height=80, bg='white')
        scrollbar2 = ttk.Scrollbar(comparison_methods_frame, orient="vertical", command=canvas2.yview)
        scrollable_frame2 = ttk.Frame(canvas2)
        
        scrollable_frame2.bind(
            "<Configure>",
            lambda e: canvas2.configure(scrollregion=canvas2.bbox("all"))
        )
        
        canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
        canvas2.configure(yscrollcommand=scrollbar2.set)
        
        self.comparison_method_vars = {}
        if hasattr(self, 'screening_engine'):
            for method in self.screening_engine.methods:
                var = tk.BooleanVar(value=True)
                self.comparison_method_vars[method] = var
                ttk.Checkbutton(scrollable_frame2, text=method, variable=var).pack(anchor='w', padx=5)
        
        canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
        # Frame para exibição
        self.comparison_display_frame = ttk.Frame(self.comparison_frame)
        self.comparison_display_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
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
    
    def _select_all_matrix_methods(self):
        """Seleciona todos os métodos na matriz"""
        for var in self.matrix_method_vars.values():
            var.set(True)
    
    def _clear_matrix_methods(self):
        """Limpa seleção de métodos na matriz"""
        for var in self.matrix_method_vars.values():
            var.set(False)
    
    def _generate_comparison_all(self):
        """Gera comparativo com todos os métodos"""
        self._comparison_selected_methods = list(self.screening_results.keys())
        self.show_comparison_chart()
    
    def _generate_comparison_selected(self):
        """Gera comparativo apenas com métodos selecionados"""
        self._comparison_selected_methods = [method for method, var in self.comparison_method_vars.items() if var.get()]
        if not self._comparison_selected_methods:
            messagebox.showwarning("Aviso", "Selecione pelo menos um método")
            return
        self.show_comparison_chart()
    
    def _export_comparison_chart(self):
        """Exporta gráfico comparativo"""
        messagebox.showinfo("Info", "Funcionalidade de exportação será implementada")
    
    def show_suitability_matrix(self):
        """Mostra matriz de suitability com bordas azuis + aba dinâmica de características"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            # Limpar frame anterior
            for widget in self.matrix_display_frame.winfo_children():
                widget.destroy()
            
            # Obter apenas métodos selecionados
            selected_methods = [method for method, var in self.matrix_method_vars.items() if var.get()]
            if not selected_methods:
                messagebox.showwarning("Aviso", "Selecione pelo menos um método")
                return
            
            methods = selected_methods
            
            # ===== CRIAR FRAME COM COMBOBOX E MATRIZ =====
            top_frame = ttk.Frame(self.matrix_frame)
            top_frame.pack(fill='x', padx=5, pady=5)
            
            ttk.Label(top_frame, text="Selecione Método:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
            
            # Combobox para seleção de método
            method_var = tk.StringVar(value=methods[0])
            method_combo = ttk.Combobox(top_frame, textvariable=method_var, values=methods, 
                                       state='readonly', width=40, font=('Arial', 10))
            method_combo.pack(side='left', fill='x', expand=True, padx=5)
            
            # ===== CRIAR FIGURA COM MATRIZ =====
            fig = plt.figure(figsize=(14, 8))
            gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.4)
            ax_matrix = fig.add_subplot(gs[0])
            ax_chars = fig.add_subplot(gs[1])
            
            param_names = ['API', 'Viscosidade', 'Profundidade', 'Permeabilidade', 
                          'Temperatura', 'Salinidade', 'Saturação de Óleo', 'Pressão',
                          'Porosidade', 'Saturação de Água', 'Espessura', 'TAN', 'pH', 'Dip']
            
            # Preparar matriz de dados
            matrix_data = []
            for param in param_names:
                row = []
                for method in methods:
                    criteria_scores = self.screening_results[method].get('criteria_scores', {})
                    if isinstance(criteria_scores, dict):
                        score = criteria_scores.get(param, 0)
                    else:
                        score = 0
                    row.append(max(0, min(100, score)))
                matrix_data.append(row)
            
            matrix_data = np.array(matrix_data)
            
            # Criar heatmap
            im = ax_matrix.imshow(matrix_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
            
            # Configurar eixos
            ax_matrix.set_xticks(np.arange(len(methods)))
            ax_matrix.set_yticks(np.arange(len(param_names)))
            ax_matrix.set_xticklabels([m[:12]+'...' if len(m) > 12 else m for m in methods], 
                                     rotation=45, ha='right', fontsize=9)
            ax_matrix.set_yticklabels(param_names, fontsize=9)
            
            ax_matrix.set_title('Matriz de Suitability - Parâmetros vs Métodos', 
                               fontweight='bold', fontsize=13, pad=15)
            
            # Adicionar valores na matriz
            for i in range(len(param_names)):
                for j in range(len(methods)):
                    text = ax_matrix.text(j, i, f'{matrix_data[i, j]:.0f}',
                                         ha="center", va="center", color="black",
                                         fontweight='bold', fontsize=7)
            
            # ===== BORDAS AZUIS NOS PARÂMETROS CRÍTICOS =====
            for j, method in enumerate(methods):
                criteria = self.screening_engine.criteria.get(method, {})
                for i, param in enumerate(param_names):
                    if param in criteria:
                        rect = plt.Rectangle((j-0.5, i-0.5), 1, 1, 
                                           fill=False, edgecolor='#1f618d', 
                                           linewidth=1.5, linestyle='-')
                        ax_matrix.add_patch(rect)
            
            # Colorbar
            cbar = plt.colorbar(im, ax=ax_matrix, orientation='vertical', pad=0.02)
            cbar.set_label('Score (%)', fontweight='bold')
            
            # ===== ABA DE CARACTERÍSTICAS DINÂMICA =====
            ax_chars.axis('off')
            
            def update_characteristics(*args):
                """Atualiza características quando método é selecionado"""
                ax_chars.clear()
                ax_chars.axis('off')
                
                selected_method = method_var.get()
                method_data = self.screening_results.get(selected_method, {})
                criteria = self.screening_engine.criteria.get(selected_method, {})
                
                # Montar texto da caixa
                box_lines = []
                box_lines.append(f"★ MÉTODO RECOMENDADO: {selected_method.upper()}")
                box_lines.append(f"Score: {method_data.get('score', 0):.1f}%  |  Status: {method_data.get('status', 'N/A').upper()}")
                box_lines.append("─" * 100)
                box_lines.append("Critérios Principais:")
                box_lines.append("")
                
                for param, limits in list(criteria.items())[:6]:
                    min_val = limits.get('min', 'N/A')
                    max_val = limits.get('max', 'N/A')
                    peso = limits.get('peso', 0) * 100
                    
                    range_str = ""
                    if min_val is not None and max_val is not None:
                        range_str = f"{min_val} - {max_val}"
                    elif min_val is not None:
                        range_str = f"≥ {min_val}"
                    elif max_val is not None:
                        range_str = f"≤ {max_val}"
                    else:
                        range_str = "Sem limite"
                    
                    box_lines.append(f"  • {param:<20} | Intervalo: {range_str:<20} | Peso: {peso:.0f}%")
                
                box_text = "\n".join(box_lines)
                
                # Adicionar caixa com fundo azul
                bbox_props = dict(boxstyle='round,pad=1.0', facecolor='#d6eaf8', 
                                edgecolor='#1f618d', linewidth=2.5, alpha=0.95)
                ax_chars.text(0.5, 0.5, box_text, ha='center', va='center', fontsize=9,
                            transform=ax_chars.transAxes, family='monospace',
                            bbox=bbox_props, fontweight='bold')
                
                fig.canvas.draw_idle()
            
            # Vincular evento de mudança no combobox
            method_combo.bind('<<ComboboxSelected>>', update_characteristics)
            
            # Inicializar com primeiro método
            update_characteristics()
            
            plt.suptitle('Análise de Adequabilidade - Matriz com Características Dinâmicas', 
                        fontsize=14, fontweight='bold', y=0.98)
            
            # Embed figura
            canvas = FigureCanvasTkAgg(fig, self.matrix_display_frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.matrix_display_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar matriz de suitability: {str(e)}")
    
    def show_comparison_chart(self):
        """Mostra gráfico comparativo com métodos e tipo selecionados"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            # Limpar frames anteriores
            for widget in self.comparison_display_frame.winfo_children():
                widget.destroy()
            
            # Obter métodos selecionados
            if hasattr(self, '_comparison_selected_methods') and self._comparison_selected_methods:
                methods = self._comparison_selected_methods
            else:
                methods = [m for m, var in self.comparison_method_vars.items() if var.get()] if self.comparison_method_vars else list(self.screening_results.keys())
            
            if not methods:
                messagebox.showwarning("Aviso", "Selecione pelo menos um método")
                return
            
            chart_type = self.comparison_chart_type.get().lower()
            
            # Criar figura baseada no tipo de gráfico
            if chart_type == "radar":
                fig = self._create_comparison_radar(methods)
            elif chart_type == "barras":
                fig = self._create_comparison_bars(methods)
            elif chart_type == "box plot":
                fig = self._create_comparison_boxplot(methods)
            elif chart_type == "dispersão":
                fig = self._create_comparison_scatter(methods)
            elif chart_type == "dashboard":
                fig = self._create_comparison_dashboard(methods)
            else:
                fig = self._create_comparison_radar(methods)
            
            # Embed
            canvas = FigureCanvasTkAgg(fig, self.comparison_display_frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.comparison_display_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar gráfico comparativo: {str(e)}")
    
    def _create_comparison_radar(self, methods):
        """Cria gráfico radar comparativo"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='polar')
        
        categories = ['API', 'Viscosidade', 'Profundidade', 'Temperatura', 'Salinidade']
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        for method in methods[:5]:  # Máximo 5 métodos para clareza
            values = [self.screening_results[method].get('criteria_scores', {}).get(cat, 0) for cat in categories]
            values += values[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=method)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.set_title('Comparativo - Gráfico Radar', fontweight='bold', pad=20)
        ax.grid(True)
        
        return fig
    
    def _create_comparison_bars(self, methods):
        """Cria gráfico de barras comparativo"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        scores = [self.screening_results[m]['score'] for m in methods]
        colors = [self.screening_results[m]['color'] for m in methods]
        
        bars = ax.barh(methods, scores, color=colors, edgecolor='black', linewidth=1.5)
        
        # Adicionar valores nas barras
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 2, i, f'{score:.1f}%', va='center', fontweight='bold')
        
        ax.set_xlabel('Score (%)', fontweight='bold')
        ax.set_title('Comparativo - Gráfico de Barras', fontweight='bold')
        ax.set_xlim(0, 105)
        ax.grid(True, alpha=0.3, axis='x')
        
        return fig
    
    def _create_comparison_boxplot(self, methods):
        """Cria gráfico box plot comparativo"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scores_by_status = {'Alta (≥80%)': [], 'Média (60-79%)': [], 'Baixa (<60%)': []}
        for method in methods:
            score = self.screening_results[method]['score']
            if score >= 80:
                scores_by_status['Alta (≥80%)'].append(score)
            elif score >= 60:
                scores_by_status['Média (60-79%)'].append(score)
            else:
                scores_by_status['Baixa (<60%)'].append(score)
        
        data_for_box = [scores_by_status['Alta (≥80%)'] if scores_by_status['Alta (≥80%)'] else [0],
                       scores_by_status['Média (60-79%)'] if scores_by_status['Média (60-79%)'] else [0],
                       scores_by_status['Baixa (<60%)'] if scores_by_status['Baixa (<60%)'] else [0]]
        
        bp = ax.boxplot(data_for_box, labels=['Alta', 'Média', 'Baixa'], patch_artist=True, notch=True)
        for patch, color in zip(bp['boxes'], ['#27ae60', '#f39c12', '#e74c3c']):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('Score (%)', fontweight='bold')
        ax.set_title('Comparativo - Box Plot', fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
        
        return fig
    
    def _create_comparison_scatter(self, methods):
        """Cria gráfico scatter comparativo"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        scores = [self.screening_results[m]['score'] for m in methods]
        colors = [self.screening_results[m]['color'] for m in methods]
        indices = range(len(methods))
        
        ax.scatter(indices, scores, s=400, c=colors, alpha=0.6, edgecolor='black', linewidth=2)
        
        for i, (idx, score, method) in enumerate(zip(indices, scores, methods)):
            ax.annotate(f'{score:.0f}%', xy=(idx, score), xytext=(5, 5), 
                       textcoords='offset points', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Métodos', fontweight='bold')
        ax.set_ylabel('Score (%)', fontweight='bold')
        ax.set_title('Comparativo - Dispersão', fontweight='bold')
        ax.set_ylim(0, 105)
        ax.set_xlim(-1, len(methods))
        ax.set_xticks(indices)
        ax.set_xticklabels([m[:8]+'...' if len(m) > 8 else m for m in methods], rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _create_comparison_dashboard(self, methods):
        """Cria dashboard comparativo com KPIs"""
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axis('off')
        
        scores = [self.screening_results[m]['score'] for m in methods]
        
        alta_count = sum(1 for s in scores if s >= 80)
        media_count = sum(1 for s in scores if 60 <= s < 80)
        baixa_count = sum(1 for s in scores if s < 60)
        media_score = np.mean(scores)
        
        kpi_text = "DASHBOARD COMPARATIVO\n\n"
        kpi_text += f"Métodos Analisados: {len(methods)}\n\n"
        kpi_text += f"Alta Suitability (≥80%): {alta_count}\n"
        kpi_text += f"Média Suitability (60-79%): {media_count}\n"
        kpi_text += f"Baixa Suitability (<60%): {baixa_count}\n\n"
        kpi_text += f"Score Médio: {media_score:.1f}%\n"
        kpi_text += f"Score Máximo: {max(scores):.1f}%\n"
        kpi_text += f"Score Mínimo: {min(scores):.1f}%"
        
        ax.text(0.5, 0.5, kpi_text, ha='center', va='center',
               transform=ax.transAxes, fontsize=12, family='monospace',
               bbox=dict(boxstyle='round,pad=1.5', facecolor='#ecf0f1', 
                       edgecolor='#34495e', linewidth=2.5),
               fontweight='bold')
        
        fig.suptitle('Comparativo - Dashboard KPIs', fontsize=14, fontweight='bold')
        
        return fig
    
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
    
    def generate_custom_chart(self) -> None:
        """Gera gráfico personalizado com base na seleção do usuário"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro para gerar gráficos")
            return
        
        try:
            chart_type = self.chart_type_var.get().lower()
            methods = list(self.screening_results.keys())
            scores = [self.screening_results[m]['score'] for m in methods]
            colors = [self.screening_results[m]['color'] for m in methods]
            
            if chart_type == "barras":
                fig = self._create_results_bars(methods, scores, colors)
            elif chart_type == "pizza":
                fig = self._create_results_pie(methods, scores)
            elif chart_type == "linha":
                fig = self._create_results_line(methods, scores)
            elif chart_type == "área":
                fig = self._create_results_area(methods, scores, colors)
            elif chart_type == "radar":
                fig = self._create_results_radar(methods, scores)
            elif chart_type == "box plot":
                fig = self._create_results_boxplot(methods, scores, colors)
            elif chart_type == "dispersão":
                fig = self._create_results_scatter(methods, scores, colors)
            elif chart_type == "dashboard completo":
                fig = self._create_results_dashboard(methods, scores, colors)
            else:
                messagebox.showwarning("Aviso", "Tipo de gráfico não reconhecido")
                return
            
            self._embed_results_chart(fig)
            messagebox.showinfo("Sucesso", f"Gráfico de {chart_type} gerado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar gráfico: {str(e)}")
    
    def _create_results_bars(self, methods, scores, colors):
        """Cria gráfico de barras horizontal"""
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(methods, scores, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Suitability Score (%)', fontweight='bold', fontsize=12)
        ax.set_title('Análise de Suitability - Gráfico de Barras', fontweight='bold', fontsize=14)
        ax.set_xlim(0, 100)
        ax.axvline(x=80, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Alta (≥80%)')
        ax.axvline(x=60, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Média (60-79%)')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3, axis='x')
        
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{score:.1f}%', 
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def _create_results_pie(self, methods, scores):
        """Cria gráfico de pizza com distribuição de suitability"""
        fig, ax = plt.subplots(figsize=(10, 8))
        categories = {'Alta (≥80%)': 0, 'Média (60-79%)': 0, 'Baixa (<60%)': 0}
        
        for score in scores:
            if score >= 80:
                categories['Alta (≥80%)'] += 1
            elif score >= 60:
                categories['Média (60-79%)'] += 1
            else:
                categories['Baixa (<60%)'] += 1
        
        colors_pie = ['#27ae60', '#f39c12', '#e74c3c']
        wedges, texts, autotexts = ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
                        colors=colors_pie, startangle=90, textprops={'fontweight': 'bold', 'fontsize': 11})
        ax.set_title('Distribuição de Métodos por Suitability', fontweight='bold', fontsize=14)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
        
        plt.tight_layout()
        return fig
    
    def _create_results_line(self, methods, scores):
        """Cria gráfico de linha com tendência"""
        fig, ax = plt.subplots(figsize=(12, 6))
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        sorted_methods = [methods[i] for i in sorted_indices]
        sorted_scores = [scores[i] for i in sorted_indices]
        
        ax.plot(range(len(sorted_scores)), sorted_scores, 'o-', linewidth=2.5, markersize=10, 
               color='#3498db', markerfacecolor='#2980b9', markeredgewidth=2)
        ax.fill_between(range(len(sorted_scores)), sorted_scores, alpha=0.2, color='#3498db')
        
        ax.set_xlabel('Métodos (Ordenados por Score)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Suitability Score (%)', fontweight='bold', fontsize=12)
        ax.set_title('Tendência de Suitability dos Métodos EOR', fontweight='bold', fontsize=14)
        ax.set_xticks(range(len(sorted_methods)))
        ax.set_xticklabels([m[:10]+'...' if len(m) > 10 else m for m in sorted_methods], 
                           rotation=45, ha='right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
        
        plt.tight_layout()
        return fig
    
    def _create_results_area(self, methods, scores, colors):
        """Cria gráfico de área"""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(range(len(methods)), scores, color=colors, edgecolor='black', alpha=0.8, linewidth=1.5)
        
        ax.set_xlabel('Métodos EOR', fontweight='bold', fontsize=12)
        ax.set_ylabel('Suitability Score (%)', fontweight='bold', fontsize=12)
        ax.set_title('Área de Suitability - Todos os Métodos', fontweight='bold', fontsize=14)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels([m[:10]+'...' if len(m) > 10 else m for m in methods], 
                           rotation=45, ha='right', fontsize=9)
        ax.set_ylim(0, 105)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def _create_results_radar(self, methods, scores):
        """Cria gráfico radar"""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Limitar a 8 métodos para legibilidade
        display_methods = methods[:8] if len(methods) > 8 else methods
        display_scores = scores[:8] if len(scores) > 8 else scores
        
        angles = np.linspace(0, 2 * np.pi, len(display_methods), endpoint=False).tolist()
        display_scores_plot = display_scores + [display_scores[0]]
        angles += angles[:1]
        
        ax.plot(angles, display_scores_plot, 'o-', linewidth=2, color='#2980b9')
        ax.fill(angles, display_scores_plot, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([m[:8]+'...' if len(m) > 8 else m for m in display_methods], fontsize=9)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_title('Análise Radar de Métodos EOR', fontweight='bold', fontsize=14, pad=20)
        ax.grid(True)
        
        plt.tight_layout()
        return fig
    
    def _create_results_boxplot(self, methods, scores, colors):
        """Cria box plot por categoria"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        alta = [s for s in scores if s >= 80]
        media = [s for s in scores if 60 <= s < 80]
        baixa = [s for s in scores if s < 60]
        
        data_to_plot = [alta, media, baixa]
        labels = ['Alta (≥80%)', 'Média (60-79%)', 'Baixa (<60%)']
        colors_box = ['#27ae60', '#f39c12', '#e74c3c']
        
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True, widths=0.6)
        
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('Suitability Score (%)', fontweight='bold', fontsize=12)
        ax.set_title('Box Plot de Suitability por Categoria', fontweight='bold', fontsize=14)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 105)
        
        plt.tight_layout()
        return fig
    
    def _create_results_scatter(self, methods, scores, colors):
        """Cria gráfico de dispersão"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_positions = np.arange(len(methods))
        ax.scatter(x_positions, scores, c=colors, s=300, alpha=0.7, edgecolors='black', linewidth=2)
        
        for i, (pos, score) in enumerate(zip(x_positions, scores)):
            ax.annotate(f'{score:.1f}%', (pos, score), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Métodos EOR', fontweight='bold', fontsize=12)
        ax.set_ylabel('Suitability Score (%)', fontweight='bold', fontsize=12)
        ax.set_title('Dispersão de Métodos - Suitability Scores', fontweight='bold', fontsize=14)
        ax.set_xticks(x_positions)
        ax.set_xticklabels([m[:10]+'...' if len(m) > 10 else m for m in methods], 
                           rotation=45, ha='right', fontsize=9)
        ax.set_ylim(0, 105)
        ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, linewidth=1)
        ax.axhline(y=60, color='orange', linestyle='--', alpha=0.5, linewidth=1)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def _create_results_dashboard(self, methods, scores, colors):
        """Cria dashboard com KPIs e gráficos combinados"""
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)
        
        # KPIs no topo
        ax_kpi = fig.add_subplot(gs[0, :])
        ax_kpi.axis('off')
        
        total = len(methods)
        alta_count = len([s for s in scores if s >= 80])
        media_count = len([s for s in scores if 60 <= s < 80])
        baixa_count = len([s for s in scores if s < 60])
        mean_score = np.mean(scores)
        max_score = np.max(scores)
        min_score = np.min(scores)
        
        kpi_text = f"""
        RESUMO DE SUITABILITY - EOR SCREENING
        ════════════════════════════════════════════════════════════════
        Total de Métodos: {total} │ Média: {mean_score:.1f}% │ Máx: {max_score:.1f}% │ Mín: {min_score:.1f}%
        Suitabilidade Alta (≥80%): {alta_count} │ Média (60-79%): {media_count} │ Baixa (<60%): {baixa_count}
        ════════════════════════════════════════════════════════════════
        """
        
        ax_kpi.text(0.5, 0.5, kpi_text, transform=ax_kpi.transAxes, fontfamily='monospace',
                   fontsize=10, verticalalignment='center', horizontalalignment='center',
                   bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8, pad=1))
        
        # Gráfico de barras
        ax1 = fig.add_subplot(gs[1, 0])
        bars = ax1.barh(methods[:10], scores[:10], color=colors[:10], edgecolor='black')
        ax1.set_xlabel('Score (%)', fontsize=10, fontweight='bold')
        ax1.set_title('Top 10 Métodos', fontsize=11, fontweight='bold')
        ax1.set_xlim(0, 100)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Gráfico de pizza
        ax2 = fig.add_subplot(gs[1, 1])
        colors_pie = ['#27ae60', '#f39c12', '#e74c3c']
        ax2.pie([alta_count, media_count, baixa_count], labels=['Alta', 'Média', 'Baixa'],
               colors=colors_pie, autopct='%1.1f%%', startangle=90, textprops={'fontweight': 'bold'})
        ax2.set_title('Distribuição por Categoria', fontsize=11, fontweight='bold')
        
        # Histograma de distribuição
        ax3 = fig.add_subplot(gs[2, 0])
        ax3.hist(scores, bins=10, color='#3498db', edgecolor='black', alpha=0.7)
        ax3.set_xlabel('Score (%)', fontweight='bold')
        ax3.set_ylabel('Frequência', fontweight='bold')
        ax3.set_title('Distribuição de Scores', fontsize=11, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Linha de tendência
        ax4 = fig.add_subplot(gs[2, 1])
        sorted_scores = sorted(scores, reverse=True)
        ax4.plot(range(len(sorted_scores)), sorted_scores, 'o-', linewidth=2, color='#2980b9', markersize=6)
        ax4.fill_between(range(len(sorted_scores)), sorted_scores, alpha=0.2, color='#3498db')
        ax4.set_xlabel('Posição', fontweight='bold')
        ax4.set_ylabel('Score (%)', fontweight='bold')
        ax4.set_title('Tendência de Scores (Ordenado)', fontsize=11, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, 105)
        
        return fig
    
    def _embed_results_chart(self, fig) -> None:
        """Empacotar gráfico no frame de resultados"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        # Armazenar referência à figura para export
        self.current_results_figure = fig
        
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.chart_container)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def export_chart_results(self) -> None:
        """Exporta gráfico dos resultados"""
        try:
            if not hasattr(self, 'current_results_figure'):
                messagebox.showwarning("Aviso", "Nenhum gráfico para exportar")
                return
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")]
            )
            
            if filepath:
                self.current_results_figure.savefig(filepath, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {str(e)}")
    
    def clear_chart_results(self) -> None:
        """Limpa gráfico dos resultados"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.update_status("Gráfico limpo")
    
    def show_individual_chart(self) -> None:
        """Gera gráfico individual de método selecionado"""
        if not self.method_select_var.get():
            messagebox.showwarning("Aviso", "Selecione um método")
            return
        
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
        
        try:
            method = self.method_select_var.get()
            method_data = self.screening_results.get(method, {})
            chart_type = self.individual_chart_type.get().lower()
            
            # Limpar frame anterior
            for widget in self.individual_display_frame.winfo_children():
                widget.destroy()
            
            # Criar figura baseada no tipo selecionado
            if chart_type == "radar":
                fig = self._create_individual_chart_radar(method, method_data)
            elif chart_type == "barras":
                fig = self._create_individual_chart_bars(method, method_data)
            elif chart_type == "linha":
                fig = self._create_individual_chart_line(method, method_data)
            elif chart_type == "gauge":
                fig = self._create_individual_chart_gauge(method, method_data)
            elif chart_type == "scorecard":
                fig = self._create_individual_chart_scorecard(method, method_data)
            else:
                fig = self._create_individual_chart_radar(method, method_data)
            
            # Embed
            canvas = FigureCanvasTkAgg(fig, self.individual_display_frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.individual_display_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar gráfico: {str(e)}")
    
    def _create_individual_chart_radar(self, method: str, data: Dict) -> plt.Figure:
        """Cria gráfico radar individual"""
        criteria = self.screening_engine.criteria.get(method, {})
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        # Preparar dados
        categories = list(criteria.keys())
        N = len(categories)
        
        if N < 3:
            categories = ['Critério 1', 'Critério 2', 'Critério 3']
            N = 3
        
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Valores
        values = []
        for param in categories:
            val = data.get('criteria_scores', {}).get(param, 0) if isinstance(data.get('criteria_scores', {}), dict) else 0
            values.append(max(0, min(100, val)))
        values += values[:1]
        
        # Plotar
        ax.plot(angles, values, 'o-', linewidth=2, color='#3498db', markersize=8)
        ax.fill(angles, values, alpha=0.25, color='#3498db')
        
        # Configurar
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=8)
        ax.grid(True)
        
        # Título com score
        title = f'{method}\nScore: {data.get("score", 0):.1f}%'
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)
        
        return fig
    
    def _create_individual_chart_bars(self, method: str, data: Dict) -> plt.Figure:
        """Cria gráfico de barras para um método individual"""
        criteria = self.screening_engine.criteria.get(method, {})
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        categories = list(criteria.keys())
        values = []
        for param in categories:
            val = data.get('criteria_scores', {}).get(param, 0) if isinstance(data.get('criteria_scores', {}), dict) else 0
            values.append(max(0, min(100, val)))
        
        # Cores baseadas em score
        colors = ['#27ae60' if v >= 80 else '#f39c12' if v >= 60 else '#e74c3c' for v in values]
        
        bars = ax.bar(range(len(categories)), values, color=colors, edgecolor='black', alpha=0.7)
        
        ax.set_xlabel('Critérios', fontweight='bold')
        ax.set_ylabel('Score (%)', fontweight='bold')
        ax.set_title(f'{method} - Análise por Critério\nScore Total: {data.get("score", 0):.1f}%', 
                    fontweight='bold', fontsize=12)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.set_ylim(0, 100)
        ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='Alta (80%)')
        ax.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Média (60%)')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Adicionar valores nas barras
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def _create_individual_chart_line(self, method: str, data: Dict) -> plt.Figure:
        """Cria gráfico de linha para um método individual"""
        criteria = self.screening_engine.criteria.get(method, {})
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        categories = list(criteria.keys())
        values = []
        for param in categories:
            val = data.get('criteria_scores', {}).get(param, 0) if isinstance(data.get('criteria_scores', {}), dict) else 0
            values.append(max(0, min(100, val)))
        
        ax.plot(range(len(categories)), values, 'o-', linewidth=2.5, markersize=10, 
               color='#2980b9', markerfacecolor='#3498db', markeredgewidth=2)
        ax.fill_between(range(len(categories)), values, alpha=0.2, color='#3498db')
        
        ax.set_xlabel('Critérios', fontweight='bold')
        ax.set_ylabel('Score (%)', fontweight='bold')
        ax.set_title(f'{method} - Análise por Critério (Linha)\nScore Total: {data.get("score", 0):.1f}%', 
                    fontweight='bold', fontsize=12)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.set_ylim(0, 100)
        ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='Alta (80%)')
        ax.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Média (60%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Adicionar valores nos pontos
        for x, y in enumerate(values):
            ax.text(x, y + 3, f'{y:.0f}%', ha='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        return fig
    
    def _create_individual_chart_gauge(self, method: str, data: Dict) -> plt.Figure:
        """Cria gráfico gauge (velocímetro) para um método"""
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        score = data.get('score', 0)
        
        # Configurar gauge
        theta = np.linspace(np.pi, 0, 100)
        
        # Cores de fundo (segmentos)
        colors_segment = ['#e74c3c'] * 30 + ['#f39c12'] * 30 + ['#27ae60'] * 40
        for i in range(len(theta) - 1):
            ax.fill_between([theta[i], theta[i+1]], 0, 1, color=colors_segment[i], alpha=0.3)
        
        # Agulha
        needle_angle = np.pi - (score / 100 * np.pi)
        ax.arrow(needle_angle, 0, 0, 0.8, head_width=0.1, head_length=0.1, fc='black', ec='black', linewidth=3)
        
        # Configuração
        ax.set_ylim(0, 1)
        ax.set_theta_offset(np.pi)
        ax.set_theta_direction(-1)
        ax.set_xticks([np.pi, 2*np.pi/3, np.pi/3, 0])
        ax.set_xticklabels(['0%', '33%', '67%', '100%'], fontsize=12, fontweight='bold')
        ax.set_yticks([])
        
        fig.suptitle(f'{method}\nScore: {score:.1f}%', fontsize=14, fontweight='bold', y=0.98)
        
        return fig
    
    def _create_individual_chart_scorecard(self, method: str, data: Dict) -> plt.Figure:
        """Cria scorecard visual para um método"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        score = data.get('score', 0)
        status = data.get('status', 'DESCONHECIDO')
        color = data.get('color', '#bdc3c7')
        
        # Título do método
        ax.text(0.5, 0.95, method, ha='center', va='top', fontsize=16, fontweight='bold',
               transform=ax.transAxes)
        
        # Score principal (grande)
        ax.text(0.5, 0.80, f'{score:.1f}%', ha='center', va='center', fontsize=48, fontweight='bold',
               transform=ax.transAxes, color=color)
        
        # Status
        ax.text(0.5, 0.68, status, ha='center', va='top', fontsize=14, fontweight='bold',
               transform=ax.transAxes, color=color, 
               bbox=dict(boxstyle='round,pad=0.8', facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))
        
        # Pontos positivos
        ax.text(0.05, 0.55, 'Pontos Fortes:', fontsize=11, fontweight='bold', transform=ax.transAxes)
        pontos_pos = data.get('pontos_positivos', [])[:3]
        for i, ponto in enumerate(pontos_pos):
            ax.text(0.08, 0.50 - i*0.08, f'✓ {ponto}', fontsize=10, transform=ax.transAxes,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#d5f4e6', alpha=0.7))
        
        # Pontos negativos
        ax.text(0.55, 0.55, 'Pontos Fracos:', fontsize=11, fontweight='bold', transform=ax.transAxes)
        pontos_neg = data.get('pontos_negativos', [])[:3]
        for i, ponto in enumerate(pontos_neg):
            ax.text(0.58, 0.50 - i*0.08, f'✗ {ponto}', fontsize=10, transform=ax.transAxes,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='#fadbd8', alpha=0.7))
        
        return fig
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        categories = list(criteria.keys())
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        values = []
        for param in categories:
            if param in data.get('criteria_scores', {}):
                values.append(min(100, data['criteria_scores'][param]))
            else:
                values.append(0)
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2.5, color=data.get('color', '#3498db'),
               markersize=8, markerfacecolor='white', markeredgewidth=2)
        ax.fill(angles, values, alpha=0.25, color=data.get('color', '#3498db'))
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_title(f'{method}\nSuitability: {data["score"]:.1f}% ({data["status"]})', 
                    fontsize=13, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.6)
        
        return fig
    
    def export_individual_chart(self) -> None:
        """Exporta gráfico individual"""
        if not self.method_select_var.get():
            messagebox.showwarning("Aviso", "Selecione um método")
            return
        
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("PDF", "*.pdf")]
            )
            if filepath:
                messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {str(e)}")
    
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
            
            # Atualizar combobox de seleção de métodos
            self.method_combo['values'] = list(scores.keys())
            
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
    
    # ============================================================================
    # FASE 1B: SCREENING AVANÇADO COM 4 SUBABAS
    # ============================================================================
    
    def _create_advanced_screening_tab(self):
        """Cria aba principal de Screening Avançado com 4 subabas"""
        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Screening Avançado")
        
        # Sub-notebook para 4 categorias
        self.screening_notebook = ttk.Notebook(self.advanced_tab)
        self.screening_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Subaba 1: Perguntas Técnicas
        self._create_screening_questions_tab()
        
        # Subaba 2: Validação de Dados
        self._create_screening_validation_tab()
        
        # Subaba 3: Offshore & Angola
        self._create_screening_offshore_tab()
        
        # Subaba 4: Eficiência (Nc + RF)
        self._create_screening_efficiency_tab()
    
    def _create_screening_questions_tab(self):
        """Subaba 1: Perguntas técnicas de screening por método"""
        questions_tab = ttk.Frame(self.screening_notebook)
        self.screening_notebook.add(questions_tab, text="Perguntas Técnicas")
        
        # Frame superior: Seleção de método
        top_frame = ttk.LabelFrame(questions_tab, text="1. Selecione o Método EOR", padding=10)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(top_frame, text="Método:").pack(side=tk.LEFT, padx=5)
        
        self.screening_method_var = tk.StringVar()
        methods_list = list(AdvancedScreeningQuestions.METHODS_CATEGORIES.get("Térmico", []) +
                           AdvancedScreeningQuestions.METHODS_CATEGORIES.get("Químico", []) +
                           AdvancedScreeningQuestions.METHODS_CATEGORIES.get("Miscível", []) +
                           AdvancedScreeningQuestions.METHODS_CATEGORIES.get("Imiscível", []) +
                           AdvancedScreeningQuestions.METHODS_CATEGORIES.get("Outros", []))
        
        method_combo = ttk.Combobox(top_frame, textvariable=self.screening_method_var,
                                    values=methods_list, state='readonly', width=30)
        method_combo.pack(side=tk.LEFT, padx=5)
        method_combo.bind('<<ComboboxSelected>>', self._on_screening_method_selected)
        
        # Frame central: Perguntas
        questions_frame = ttk.LabelFrame(questions_tab, text="2. Responda as Perguntas", padding=10)
        questions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas com scrollbar para perguntas
        canvas = tk.Canvas(questions_frame, bg='white')
        scrollbar = ttk.Scrollbar(questions_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        self.screening_questions_frame = ttk.Frame(canvas, padding=10)
        self.screening_questions_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.screening_questions_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.screening_answers = {}  # Armazena respostas
        
        # Frame inferior: Resultado
        result_frame = ttk.LabelFrame(questions_tab, text="Resultado da Análise", padding=10)
        result_frame.pack(fill='x', padx=10, pady=10)
        
        self.screening_result_text = tk.Text(result_frame, height=8, width=80, wrap=tk.WORD)
        self.screening_result_text.pack(fill='both', expand=True)
        
        ttk.Button(result_frame, text="Analisar Respostas",
                  command=self._analyze_screening_questions).pack(pady=10)
    
    def _on_screening_method_selected(self, event=None):
        """Carrega perguntas quando método é selecionado"""
        method = self.screening_method_var.get()
        if not method:
            return
        
        # Limpa perguntas anteriores
        for widget in self.screening_questions_frame.winfo_children():
            widget.destroy()
        
        # Obtem perguntas do método
        questions = AdvancedScreeningQuestions.get_questions_by_method(method)
        self.screening_answers.clear()
        
        if not questions:
            ttk.Label(self.screening_questions_frame,
                     text=f"Nenhuma pergunta disponível para {method}").pack()
            return
        
        # Cria widgets para cada pergunta
        for i, question in enumerate(questions, 1):
            frame = ttk.Frame(self.screening_questions_frame)
            frame.pack(fill='x', pady=10)
            
            ttk.Label(frame, text=f"{i}. {question}", wraplength=600,
                     justify=tk.LEFT).pack(anchor='w')
            
            var = tk.StringVar(value="Não respondido")
            self.screening_answers[i] = var
            
            options_frame = ttk.Frame(frame)
            options_frame.pack(fill='x', padx=20, pady=5)
            
            ttk.Radiobutton(options_frame, text="Sim", variable=var,
                          value="Sim").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(options_frame, text="Não", variable=var,
                          value="Não").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(options_frame, text="Parcialmente", variable=var,
                          value="Parcialmente").pack(side=tk.LEFT, padx=5)
    
    def _analyze_screening_questions(self):
        """Analisa respostas das perguntas de screening"""
        method = self.screening_method_var.get()
        
        if not method:
            messagebox.showwarning("Aviso", "Selecione um método primeiro")
            return
        
        # Contar respostas
        sim_count = sum(1 for var in self.screening_answers.values() if var.get() == "Sim")
        total_count = len(self.screening_answers)
        score = (sim_count / total_count * 100) if total_count > 0 else 0
        
        # Gerar resultado
        result = f"ANÁLISE DE SCREENING - {method}\n"
        result += "=" * 70 + "\n\n"
        result += f"Respostas Positivas: {sim_count}/{total_count}\n"
        result += f"Score de Viabilidade: {score:.1f}%\n\n"
        
        if score >= 80:
            result += "STATUS: ✅ MÉTODO VIÁVEL\n"
            result += "Este método apresenta excelente potencial para o reservatório.\n"
        elif score >= 60:
            result += "STATUS: ⚠️ MÉTODO PARCIALMENTE VIÁVEL\n"
            result += "Recomenda-se análise adicional de parâmetros críticos.\n"
        else:
            result += "STATUS: ❌ MÉTODO NÃO VIÁVEL\n"
            result += "Este método apresenta limitações significativas.\n"
        
        self.screening_result_text.delete('1.0', tk.END)
        self.screening_result_text.insert('1.0', result)
    
    def _create_screening_validation_tab(self):
        """Subaba 2: Validação de consistência de dados em tempo real"""
        validation_tab = ttk.Frame(self.screening_notebook)
        self.screening_notebook.add(validation_tab, text="Validação de Dados")
        
        # Frame superior: Instrução
        instr_frame = ttk.Frame(validation_tab)
        instr_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(instr_frame, text="Validação Automática de 7 Critérios de Consistência",
                 font=('Arial', 11, 'bold')).pack(anchor='w')
        
        # Frame central: 7 validadores
        validators_frame = ttk.LabelFrame(validation_tab, text="Critérios de Validação", padding=15)
        validators_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas para scrolling
        canvas = tk.Canvas(validators_frame, bg='white')
        scrollbar = ttk.Scrollbar(validators_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        self.validation_results_frame = ttk.Frame(canvas)
        self.validation_results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.validation_results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Frame inferior: Botão de validação
        button_frame = ttk.Frame(validation_tab)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Validar Dados Atuais",
                  command=self._run_data_validation).pack()
        
        # Label para resumo
        self.validation_summary = tk.StringVar(value="Clique em 'Validar Dados Atuais' para análise")
        ttk.Label(button_frame, textvariable=self.validation_summary,
                 foreground='blue').pack(pady=10)
    
    def _run_data_validation(self):
        """Executa validação de dados consistência"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Carregue dados de reservatório primeiro")
            return
        
        # Executar validação
        valid, messages = DataValidator.validate_consistency(self.reservoir_data)
        
        # Limpar frame anterior
        for widget in self.validation_results_frame.winfo_children():
            widget.destroy()
        
        # Mostrar resultados
        validations = [
            ("Saturação Total", f"So + Sw = {self.reservoir_data.get('Saturação de Óleo', 0) + self.reservoir_data.get('Saturação de Água', 0):.1f}%"),
            ("API vs Viscosidade", f"API={self.reservoir_data.get('API', 0):.1f}°, Visc={self.reservoir_data.get('Viscosidade', 0):.1f} cP"),
            ("Profundidade vs Temperatura", f"Prof={self.reservoir_data.get('Profundidade', 0):.0f}m, Temp={self.reservoir_data.get('Temperatura', 0):.1f}°C"),
            ("Profundidade vs Pressão", f"Prof={self.reservoir_data.get('Profundidade', 0):.0f}m, Press={self.reservoir_data.get('Pressão', 0):.0f} psi"),
            ("Porosidade vs Permeabilidade", f"Poro={self.reservoir_data.get('Porosidade', 0):.1f}%, Perm={self.reservoir_data.get('Permeabilidade', 0):.2f} mD"),
            ("TAN Mínimo", f"TAN={self.reservoir_data.get('TAN', 0):.2f} mg KOH/g"),
            ("pH vs Salinidade", f"pH={self.reservoir_data.get('pH', 7):.1f}, Salinidade={self.reservoir_data.get('Salinidade', 0):.0f} ppm")
        ]
        
        for title, detail in validations:
            frame = ttk.Frame(self.validation_results_frame)
            frame.pack(fill='x', pady=5, padx=5)
            
            # Determinar cor (verde=ok, amarelo=aviso, vermelho=erro)
            if any(title in msg for msg in messages):
                bg_color = '#ffcccc'  # Vermelho
                status = "❌ ERRO"
            else:
                bg_color = '#ccffcc'  # Verde
                status = "✅ OK"
            
            label = tk.Label(frame, text=f"{status} - {title}: {detail}",
                           bg=bg_color, fg='black', justify=tk.LEFT,
                           wraplength=600)
            label.pack(fill='x', padx=5, pady=2)
        
        # Atualizar resumo
        errors = len(messages)
        summary = f"Validação Concluída: {7 - errors}/7 critérios OK" if errors == 0 else f"⚠️ {errors} critério(s) com problema"
        self.validation_summary.set(summary)
    
    def _create_screening_offshore_tab(self):
        """Subaba 3: Critérios offshore e campos Angola"""
        offshore_tab = ttk.Frame(self.screening_notebook)
        self.screening_notebook.add(offshore_tab, text="Offshore & Angola")
        
        # Frame esquerdo: Seleção de bloco
        left_frame = ttk.LabelFrame(offshore_tab, text="Campos Angola (SPE IADC)", padding=10)
        left_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=(10, 5), pady=10)
        
        ttk.Label(left_frame, text="Selecione um Bloco:").pack()
        
        self.offshore_block_var = tk.StringVar()
        blocks = list(OffshoreSpecificCriteria.ANGOLA_BLOCKS.keys())
        
        block_combo = ttk.Combobox(left_frame, textvariable=self.offshore_block_var,
                                   values=blocks, state='readonly', width=20)
        block_combo.pack(pady=5)
        block_combo.bind('<<ComboboxSelected>>', self._on_offshore_block_selected)
        
        # Text widget para mostrar detalhes do bloco
        self.offshore_details_text = tk.Text(left_frame, height=15, width=40, wrap=tk.WORD)
        self.offshore_details_text.pack(fill='both', expand=True, pady=10)
        
        # Frame direito: Análise de viabilidade
        right_frame = ttk.LabelFrame(offshore_tab, text="Viabilidade por Profundidade", padding=10)
        right_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 10), pady=10)
        
        # Canvas para métodos viáveis/inviáveis
        canvas = tk.Canvas(right_frame, bg='white')
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        self.offshore_viability_frame = ttk.Frame(canvas)
        self.offshore_viability_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.offshore_viability_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
    
    def _on_offshore_block_selected(self, event=None):
        """Mostra detalhes do bloco selecionado"""
        block = self.offshore_block_var.get()
        if not block:
            return
        
        # Obter detalhes do bloco
        block_data = OffshoreSpecificCriteria.ANGOLA_BLOCKS.get(block, {})
        depth = block_data.get('profundidade_agua', 0)
        
        # Mostrar detalhes
        self.offshore_details_text.delete('1.0', tk.END)
        details = f"BLOCO {block}\n"
        details += "=" * 35 + "\n\n"
        details += f"Profundidade subsea: {depth}m\n"
        details += f"Tipo: {block_data.get('tipo', 'N/A')}\n"
        details += f"Status: {block_data.get('status', 'N/A')}\n"
        details += f"Operador: {block_data.get('operador', 'N/A')}\n\n"
        
        # Classificação SPE IADC
        classification = OffshoreSpecificCriteria.get_water_depth_classification(depth)
        cost_mult = OffshoreSpecificCriteria.get_cost_multiplier(depth)
        details += f"Classificação: {classification}\n"
        details += f"Multiplicador Custo: {cost_mult}x\n"
        
        self.offshore_details_text.insert('1.0', details)
        
        # Atualizar viabilidade por método
        self._update_offshore_viability(block, depth)
    
    def _update_offshore_viability(self, block, depth):
        """Atualiza lista de viabilidade de métodos"""
        # Limpar frame
        for widget in self.offshore_viability_frame.winfo_children():
            widget.destroy()
        
        # Verificar viabilidade para cada método
        methods = list(self.eor_engine.methods)[:10]  # Mostrar primeiros 10
        
        for method in methods:
            viable, reason = OffshoreSpecificCriteria.validate_offshore_feasibility(
                method, depth, 0  # profundidade subsea = depth
            )
            
            frame = ttk.Frame(self.offshore_viability_frame)
            frame.pack(fill='x', pady=3, padx=5)
            
            status = "✅" if viable else "❌"
            color = '#ccffcc' if viable else '#ffcccc'
            
            label = tk.Label(frame, text=f"{status} {method}",
                           bg=color, fg='black', justify=tk.LEFT,
                           wraplength=250)
            label.pack(fill='x')
    
    def _create_screening_efficiency_tab(self):
        """Subaba 4: Cálculo de eficiência (Nc + RF)"""
        efficiency_tab = ttk.Frame(self.screening_notebook)
        self.screening_notebook.add(efficiency_tab, text="Eficiência (Nc + RF)")
        
        # Frame superior: Entrada de parâmetros
        input_frame = ttk.LabelFrame(efficiency_tab, text="Parâmetros de Eficiência", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Entrada de dados com sliders
        self.efficiency_params = {}
        
        params_config = [
            ("Número Capilar (Nc) - Calcular", "velocidade", 0.001, 0.1, 0.01),
            ("  Viscosidade (cP)", "viscosidade", 0.1, 1000, 10),
            ("  IFT (dine/cm)", "ift", 0.01, 100, 30),
            ("  Ângulo de Contato (°)", "contact_angle", 0, 180, 30),
            ("EficiênciaMicroscópica (PSD)", "psd", 0.0, 1.0, 0.8),
            ("Eficiência Varredura (SE)", "se", 0.0, 1.0, 0.7),
            ("Fator Drenagem (D)", "drainage", 0.5, 1.0, 0.95),
            ("Fator Tempo (T)", "time_factor", 0.0, 1.0, 0.9),
        ]
        
        for title, param, min_val, max_val, default in params_config:
            row = ttk.Frame(input_frame)
            row.pack(fill='x', pady=5)
            
            ttk.Label(row, text=title, width=30).pack(side=tk.LEFT)
            
            var = tk.DoubleVar(value=default)
            self.efficiency_params[param] = var
            
            scale = ttk.Scale(row, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                            variable=var, command=self._update_efficiency_calc)
            scale.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
            
            value_label = tk.Label(row, text=f"{default:.3f}", width=8)
            value_label.pack(side=tk.LEFT)
            
            var.trace('w', lambda *args, vl=value_label, v=var: 
                     vl.config(text=f"{v.get():.3f}"))
        
        # Frame resultado: Gráficos e cálculos
        result_frame = ttk.LabelFrame(efficiency_tab, text="Resultados de Eficiência", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas para gráfico
        self.efficiency_canvas_frame = ttk.Frame(result_frame)
        self.efficiency_canvas_frame.pack(fill='both', expand=True)
        
        # Text widget para resultados numéricos
        self.efficiency_results_text = tk.Text(result_frame, height=8, width=80, wrap=tk.WORD)
        self.efficiency_results_text.pack(fill='x', pady=10)
        
        # Botão para calcular
        ttk.Button(result_frame, text="Calcular Eficiência Completa",
                  command=self._calculate_full_efficiency).pack(pady=10)
    
    def _update_efficiency_calc(self, *args):
        """Atualiza cálculos de eficiência em tempo real"""
        try:
            # Calcular Número Capilar
            vel = self.efficiency_params.get('velocidade', tk.DoubleVar(value=0.01)).get()
            visc = self.efficiency_params.get('viscosidade', tk.DoubleVar(value=10)).get()
            ift = self.efficiency_params.get('ift', tk.DoubleVar(value=30)).get()
            angle = self.efficiency_params.get('contact_angle', tk.DoubleVar(value=30)).get()
            
            if ift > 0:
                nc = EfficiencyCalculator.calculate_capillary_number(vel, visc, ift, angle)
                nc_interp = EfficiencyCalculator.interpret_capillary_number(nc)
            
        except Exception as e:
            logger.error(f"Erro em cálculo de eficiência: {e}")
    
    def _calculate_full_efficiency(self):
        """Calcula eficiência completa com componentes"""
        try:
            # Obter parâmetros
            psd = self.efficiency_params.get('psd', tk.DoubleVar(value=0.8)).get()
            se = self.efficiency_params.get('se', tk.DoubleVar(value=0.7)).get()
            drainage = self.efficiency_params.get('drainage', tk.DoubleVar(value=0.95)).get()
            time_factor = self.efficiency_params.get('time_factor', tk.DoubleVar(value=0.9)).get()
            
            # Calcular RF
            rf_result = EfficiencyCalculator.calculate_recovery_factor(psd, se, drainage, time_factor)
            
            # Mostrar resultados
            result_text = f"ANÁLISE DE EFICIÊNCIA DE RECUPERAÇÃO\n"
            result_text += "=" * 70 + "\n\n"
            result_text += f"Fator de Recuperação Total: {rf_result['RF_percentage']:.2f}%\n"
            result_text += f"Fator de Recuperação Decimal: {rf_result['RF_total']:.4f}\n\n"
            result_text += "COMPONENTES:\n"
            result_text += f"  • PSD (Eficiência Microscópica): {rf_result['components']['PSD']:.4f}\n"
            result_text += f"  • SE (Eficiência Varredura): {rf_result['components']['SE']:.4f}\n"
            result_text += f"  • D (Fator Drenagem): {rf_result['components']['D']:.4f}\n"
            result_text += f"  • T (Fator Tempo): {rf_result['components']['T']:.4f}\n"
            
            self.efficiency_results_text.delete('1.0', tk.END)
            self.efficiency_results_text.insert('1.0', result_text)
            
            # Criar gráfico stacked bar
            self._draw_efficiency_chart(rf_result)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular eficiência: {str(e)}")
    
    def _draw_efficiency_chart(self, rf_result):
        """Desenha gráfico de componentes de eficiência"""
        try:
            # Limpar canvas anterior
            for widget in self.efficiency_canvas_frame.winfo_children():
                widget.destroy()
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(10, 5))
            
            components = rf_result['components']
            values = list(components.values())
            labels = list(components.keys())
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
            
            # Stacked bar
            ax.bar(['Fator de Recuperação'], [values[0]], label=labels[0], color=colors[0])
            bottom = values[0]
            for i in range(1, len(values)):
                ax.bar(['Fator de Recuperação'], [values[i]], bottom=bottom,
                      label=labels[i], color=colors[i])
                bottom += values[i]
            
            ax.set_ylabel('Fator (adimensional)')
            ax.set_title('Decomposição do Fator de Recuperação')
            ax.legend(loc='upper right')
            ax.set_ylim(0, 1.0)
            
            # Adicionar valores
            y_pos = 0
            for i, (val, label) in enumerate(zip(values, labels)):
                ax.text(0, y_pos + val/2, f'{label}\n{val:.3f}', 
                       ha='center', va='center', fontweight='bold')
                y_pos += val
            
            plt.tight_layout()
            
            # Embutir na interface
            canvas = FigureCanvasTkAgg(fig, master=self.efficiency_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            logger.error(f"Erro ao desenhar gráfico de eficiência: {e}")
    
    # ============================================================================
    # FASE 2: FUZZY LOGIC SELECTOR
    # ============================================================================
    
    def _create_fuzzy_selector_tab(self):
        """Cria aba FASE 2: Fuzzy Logic Selector com recomendações automáticas"""
        
        # Frame principal
        fuzzy_tab = ttk.Frame(self.notebook)
        self.notebook.add(fuzzy_tab, text="🧠 Fuzzy Selector (FASE 2)")
        
        # Painel de controle
        control_frame = ttk.LabelFrame(fuzzy_tab, text="Seleção de Campo", padding=15)
        control_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(control_frame, text="Campo Angola:").grid(row=0, column=0, sticky='w')
        
        # Dropdown com campos Angola
        campos_options = ["Bloco 15 (Raso)", "Bloco 17 (Intermediário)", "Bloco 18 (Profundo)", 
                         "Bloco 31 (Raso)", "Cabinda (Onshore)"]
        self.fuzzy_campo_var = tk.StringVar(value=campos_options[0])
        campo_combo = ttk.Combobox(control_frame, textvariable=self.fuzzy_campo_var, 
                                   values=campos_options, state='readonly', width=40)
        campo_combo.grid(row=0, column=1, sticky='ew', padx=10)
        
        # Botões
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Executar Fuzzy Selector", 
                  command=self._run_fuzzy_selector).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Exportar Resultado", 
                  command=self._export_fuzzy_result).pack(side='left', padx=5)
        
        # Resultado
        result_frame = ttk.LabelFrame(fuzzy_tab, text="Resultados - Top 5 Métodos", padding=10)
        result_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Text widget para resultados
        self.fuzzy_result_text = scrolledtext.ScrolledText(result_frame, height=20, width=80)
        self.fuzzy_result_text.pack(fill='both', expand=True)
        
        self.fuzzy_result_text.insert('1.0', 
            "Selecione um campo e clique em 'Executar Fuzzy Selector'\n"
            "para ver as 5 melhores recomendações de método EOR\n"
            "baseado em Fuzzy Logic...\n")
    
    def _run_fuzzy_selector(self):
        """Executa seleção automática com Fuzzy Logic"""
        try:
            from exemplo_fase2_fuzzy import FuzzyScreeningSelector
        except ImportError:
            messagebox.showerror("Erro", "Arquivo exemplo_fase2_fuzzy.py não encontrado")
            return
        
        # Dados dos campos Angola
        campos = {
            "Bloco 15": {"API": 18.5, "Viscosidade": 850, "Profundidade": 1200, "Temperatura": 65, 
                        "Pressão": 1500, "Salinidade": 35000, "Permeabilidade": 200, "Porosidade": 28,
                        "Saturação_Oleo": 65, "TAN": 0.8, "pH": 6.5, "Dip": 8},
            "Bloco 17": {"API": 32.5, "Viscosidade": 8.5, "Profundidade": 2200, "Temperatura": 85,
                        "Pressão": 3200, "Salinidade": 42000, "Permeabilidade": 450, "Porosidade": 30,
                        "Saturação_Oleo": 58, "TAN": 0.3, "pH": 7.2, "Dip": 12},
            "Bloco 18": {"API": 28.0, "Viscosidade": 25, "Profundidade": 3100, "Temperatura": 95,
                        "Pressão": 4500, "Salinidade": 50000, "Permeabilidade": 300, "Porosidade": 26,
                        "Saturação_Oleo": 52, "TAN": 0.6, "pH": 7.8, "Dip": 15},
            "Bloco 31": {"API": 22.0, "Viscosidade": 250, "Profundidade": 900, "Temperatura": 55,
                        "Pressão": 1200, "Salinidade": 32000, "Permeabilidade": 150, "Porosidade": 25,
                        "Saturação_Oleo": 70, "TAN": 0.5, "pH": 6.8, "Dip": 7},
            "Cabinda": {"API": 38.0, "Viscosidade": 3.5, "Profundidade": 500, "Temperatura": 45,
                       "Pressão": 800, "Salinidade": 28000, "Permeabilidade": 800, "Porosidade": 32,
                       "Saturação_Oleo": 45, "TAN": 0.2, "pH": 7.0, "Dip": 5}
        }
        
        bloco_selecionado = self.fuzzy_campo_var.get().split(" ")[1]
        
        if bloco_selecionado not in campos:
            messagebox.showerror("Erro", "Campo não encontrado")
            return
        
        reservoir_data = campos[bloco_selecionado]
        
        try:
            fuzzy = FuzzyScreeningSelector()
            recommendations = fuzzy.recommend_method(reservoir_data, top_n=5)
            
            # Limpar e exibir resultados
            self.fuzzy_result_text.delete('1.0', 'end')
            
            output = f"{'='*76}\n"
            output += f"FUZZY LOGIC SELECTOR - {self.fuzzy_campo_var.get()}\n"
            output += f"{'='*76}\n\n"
            
            output += f"Parâmetros do Reservatório:\n"
            output += f"  API: {reservoir_data['API']}° | Viscosidade: {reservoir_data['Viscosidade']} cP\n"
            output += f"  Profundidade: {reservoir_data['Profundidade']}m | Temperatura: {reservoir_data['Temperatura']}°C\n"
            output += f"  Pressão: {reservoir_data['Pressão']} psi | Salinidade: {reservoir_data['Salinidade']} ppm\n\n"
            
            output += f"{'🎯 TOP 5 MÉTODOS RECOMENDADOS'}\n"
            output += f"{'-'*76}\n\n"
            
            for idx, (method, score, confidence) in enumerate(recommendations, 1):
                output += f"{idx}. {method}\n"
                output += f"   Score: {score:.2f} | Confiança: {confidence:.1f}%\n\n"
            
            output += f"{'-'*76}\n"
            output += f"✅ Análise concluída com sucesso\n"
            
            self.fuzzy_result_text.insert('1.0', output)
            self.update_status("Fuzzy Logic Selector executado com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar Fuzzy Logic: {e}")
    
    def _export_fuzzy_result(self):
        """Exporta resultado do Fuzzy Selector"""
        content = self.fuzzy_result_text.get('1.0', 'end')
        if "FUZZY LOGIC SELECTOR" not in content:
            messagebox.showwarning("Aviso", "Execute o Fuzzy Selector primeiro")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Sucesso", f"Resultado salvo em:\n{file_path}")
    
    # ============================================================================
    # FASE 3: MONTE CARLO ANALYZER
    # ============================================================================
    
    def _create_monte_carlo_tab(self):
        """Cria aba FASE 3: Monte Carlo Analyzer com análise de incertezas"""
        
        # Frame principal
        mc_tab = ttk.Frame(self.notebook)
        self.notebook.add(mc_tab, text="📊 Monte Carlo (FASE 3)")
        
        # Painel de controle
        control_frame = ttk.LabelFrame(mc_tab, text="Configuração da Simulação", padding=15)
        control_frame.pack(fill='x', padx=15, pady=15)
        
        # Campo
        ttk.Label(control_frame, text="Campo Angola:").grid(row=0, column=0, sticky='w')
        campos_options = ["Bloco 15 (Raso)", "Bloco 17 (Intermediário)", "Bloco 18 (Profundo)", 
                         "Bloco 31 (Raso)", "Cabinda (Onshore)"]
        self.mc_campo_var = tk.StringVar(value=campos_options[1])
        campo_combo = ttk.Combobox(control_frame, textvariable=self.mc_campo_var, 
                                   values=campos_options, state='readonly', width=40)
        campo_combo.grid(row=0, column=1, sticky='ew', padx=10)
        
        # Número de iterações
        ttk.Label(control_frame, text="Iterações Monte Carlo:").grid(row=1, column=0, sticky='w')
        self.mc_iter_var = tk.StringVar(value="10000")
        iter_combo = ttk.Combobox(control_frame, textvariable=self.mc_iter_var,
                                  values=["5000", "10000", "25000", "50000"], state='readonly', width=20)
        iter_combo.grid(row=1, column=1, sticky='w', padx=10)
        
        # Método
        ttk.Label(control_frame, text="Método EOR:").grid(row=2, column=0, sticky='w')
        self.mc_method_var = tk.StringVar(value="Injeção de CO2 Miscível")
        method_combo = ttk.Combobox(control_frame, textvariable=self.mc_method_var,
                                    values=["Injeção de CO2 Miscível", "Injeção de Polímeros", 
                                           "Injeção de Água Inteligente", "WAG"], 
                                    state='readonly', width=38)
        method_combo.grid(row=2, column=1, sticky='ew', padx=10)
        
        # Botões
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Executar Monte Carlo", 
                  command=self._run_monte_carlo).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Exportar Relatório", 
                  command=self._export_mc_result).pack(side='left', padx=5)
        
        # Resultado
        result_frame = ttk.LabelFrame(mc_tab, text="Resultados P10/P50/P90", padding=10)
        result_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Text widget para resultados
        self.mc_result_text = scrolledtext.ScrolledText(result_frame, height=20, width=80)
        self.mc_result_text.pack(fill='both', expand=True)
        
        self.mc_result_text.insert('1.0', 
            "Configure a simulação e clique em 'Executar Monte Carlo'\n"
            "para ver análise de incertezas com P10/P50/P90\n"
            "para RF, NPV, IRR e CAPEX...\n")
    
    def _run_monte_carlo(self):
        """Executa simulação de Monte Carlo"""
        try:
            from exemplo_fase3_monte_carlo import MonteCarloAnalyzer
        except ImportError:
            messagebox.showerror("Erro", "Arquivo ejemplo_fase3_monte_carlo.py não encontrado")
            return
        
        # Dados dos campos
        campos = {
            "Bloco 15": {"API": 18.5, "Viscosidade": 850, "Profundidade": 1200, "Temperatura": 65, 
                        "Pressão": 1500, "Salinidade": 35000, "Permeabilidade": 200, "Porosidade": 28,
                        "Saturação_Oleo": 65, "TAN": 0.8, "pH": 6.5, "Dip": 8},
            "Bloco 17": {"API": 32.5, "Viscosidade": 8.5, "Profundidade": 2200, "Temperatura": 85,
                        "Pressão": 3200, "Salinidade": 42000, "Permeabilidade": 450, "Porosidade": 30,
                        "Saturação_Oleo": 58, "TAN": 0.3, "pH": 7.2, "Dip": 12},
            "Bloco 18": {"API": 28.0, "Viscosidade": 25, "Profundidade": 3100, "Temperatura": 95,
                        "Pressão": 4500, "Salinidade": 50000, "Permeabilidade": 300, "Porosidade": 26,
                        "Saturação_Oleo": 52, "TAN": 0.6, "pH": 7.8, "Dip": 15},
            "Bloco 31": {"API": 22.0, "Viscosidade": 250, "Profundidade": 900, "Temperatura": 55,
                        "Pressão": 1200, "Salinidade": 32000, "Permeabilidade": 150, "Porosidade": 25,
                        "Saturação_Oleo": 70, "TAN": 0.5, "pH": 6.8, "Dip": 7},
            "Cabinda": {"API": 38.0, "Viscosidade": 3.5, "Profundidade": 500, "Temperatura": 45,
                       "Pressão": 800, "Salinidade": 28000, "Permeabilidade": 800, "Porosidade": 32,
                       "Saturação_Oleo": 45, "TAN": 0.2, "pH": 7.0, "Dip": 5}
        }
        
        bloco_selecionado = self.mc_campo_var.get().split(" ")[1]
        n_iterations = int(self.mc_iter_var.get())
        method = self.mc_method_var.get()
        
        if bloco_selecionado not in campos:
            messagebox.showerror("Erro", "Campo não encontrado")
            return
        
        reservoir_data = campos[bloco_selecionado]
        
        try:
            self.update_status(f"Executando Monte Carlo com {n_iterations} iterações...")
            self.root.update()
            
            mc = MonteCarloAnalyzer(n_iterations=n_iterations)
            mc_results = mc.run_monte_carlo_simulation(reservoir_data, method)
            
            # Limpar e exibir resultados
            self.mc_result_text.delete('1.0', 'end')
            
            output = f"{'='*76}\n"
            output += f"MONTE CARLO ANALYZER - {self.mc_campo_var.get()}\n"
            output += f"{'='*76}\n\n"
            
            output += f"Configuração:\n"
            output += f"  Método: {method}\n"
            output += f"  Iterações: {n_iterations:,}\n"
            output += f"  Parâmetros: API={reservoir_data['API']}°, Visc={reservoir_data['Viscosidade']} cP\n\n"
            
            output += f"{'─'*76}\n"
            output += f"FATOR DE RECUPERAÇÃO (RF)\n"
            output += f"{'─'*76}\n"
            output += f"  P10 (Pessimista): {mc_results.get('RF', {}).get('P10', 0):.2f}%\n"
            output += f"  P50 (Realista):   {mc_results.get('RF', {}).get('P50', 0):.2f}%\n"
            output += f"  P90 (Otimista):   {mc_results.get('RF', {}).get('P90', 0):.2f}%\n\n"
            
            output += f"NPV (US$ MILHÕES)\n"
            output += f"{'─'*76}\n"
            output += f"  P10: US$ {mc_results.get('NPV', {}).get('P10', 0):.0f}M\n"
            output += f"  P50: US$ {mc_results.get('NPV', {}).get('P50', 0):.0f}M\n"
            output += f"  P90: US$ {mc_results.get('NPV', {}).get('P90', 0):.0f}M\n\n"
            
            output += f"IRR (%)\n"
            output += f"{'─'*76}\n"
            output += f"  P10: {mc_results.get('IRR', {}).get('P10', 0):.2f}%\n"
            output += f"  P50: {mc_results.get('IRR', {}).get('P50', 0):.2f}%\n"
            output += f"  P90: {mc_results.get('IRR', {}).get('P90', 0):.2f}%\n\n"
            
            output += f"CAPEX (US$ MILHÕES)\n"
            output += f"{'─'*76}\n"
            output += f"  P10: US$ {mc_results.get('CAPEX', {}).get('P10', 0):.0f}M\n"
            output += f"  P50: US$ {mc_results.get('CAPEX', {}).get('P50', 0):.0f}M\n"
            output += f"  P90: US$ {mc_results.get('CAPEX', {}).get('P90', 0):.0f}M\n\n"
            
            output += f"{'='*76}\n"
            output += f"✅ Simulação concluída com sucesso\n"
            
            self.mc_result_text.insert('1.0', output)
            self.update_status("Monte Carlo executado com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar Monte Carlo: {e}")
            logger.error(f"MC Error: {e}")
    
    def _export_mc_result(self):
        """Exporta resultado do Monte Carlo"""
        content = self.mc_result_text.get('1.0', 'end')
        if "MONTE CARLO ANALYZER" not in content:
            messagebox.showwarning("Aviso", "Execute Monte Carlo primeiro")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Sucesso", f"Resultado salvo em:\n{file_path}")
    
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