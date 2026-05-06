"""
🔗 Integração V5 → PetroChamp v2.0

Este módulo integra as funcionalidades do v5.py com a nova arquitetura modular.
Permite usar o código legado com os novos componentes.
"""

import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SuitabilityLevel(Enum):
    """Enum para classificação de adequabilidade"""
    ALTA = (80, 100, '#27ae60', '🟢')      # Verde
    MEDIA = (60, 79, '#f39c12', '🟡')       # Laranja
    BAIXA = (0, 59, '#e74c3c', '🔴')        # Vermelho


@dataclass
class ColorScheme:
    """Esquema de cores centralizado"""
    alta: str = '#27ae60'
    media: str = '#f39c12'
    baixa: str = '#e74c3c'
    neutro: str = '#bdc3c7'
    bg_primary: str = '#2c3e50'
    bg_secondary: str = '#34495e'
    text_primary: str = '#ffffff'


class VisualizationConfig:
    """Configuração de visualização"""
    FIGURE_SIZE_DEFAULT = (14, 6)
    FIGURE_SIZE_RADAR = (8, 8)
    FIGURE_SIZE_COMPARISON = (12, 10)
    FIGURE_DPI = 100
    DEFAULT_STYLE = 'seaborn-v0_8-darkgrid'
    
    RADAR_CATEGORIES = ['Técnico', 'Econômico', 'Operacional', 'Ambiental', 'Risco']
    HEATMAP_VMIN = 0
    HEATMAP_VMAX = 100


class ScreeningConfig:
    """Configuração de triagem"""
    THRESHOLD_ALTA = 80
    THRESHOLD_MEDIA = 60
    DECIMAL_PLACES = 1


def get_suitability_level(score: float) -> SuitabilityLevel:
    """Obtém nível de adequabilidade de um score."""
    for level in SuitabilityLevel:
        if level.value[0] <= score <= level.value[1]:
            return level
    return SuitabilityLevel.BAIXA


class SuitabilityVisualizer:
    """Visualizador de scores de adequabilidade."""
    
    def __init__(self, config: Optional[ColorScheme] = None):
        """Inicializa visualizador com esquema de cores opcional."""
        self.colors = config or ColorScheme()
        self.viz_config = VisualizationConfig()
        self._setup_matplotlib()
    
    def _setup_matplotlib(self) -> None:
        """Configura estilo matplotlib."""
        try:
            plt.style.use(self.viz_config.DEFAULT_STYLE)
        except Exception as e:
            logger.warning(f"Não foi possível aplicar estilo matplotlib: {e}")
    
    def _get_score_color(self, score: float) -> str:
        """Obtém cor para um score específico."""
        level = get_suitability_level(score)
        return level.value[2]
    
    def create_suitability_chart(self, method_scores: Dict[str, float], 
                                title: str = "Análise de Adequabilidade EOR") -> plt.Figure:
        """
        Cria gráfico de adequabilidade para métodos EOR.
        
        Args:
            method_scores: Dict com {método: score}
            title: Título do gráfico
        
        Returns:
            matplotlib Figure
        """
        methods = list(method_scores.keys())
        scores = list(method_scores.values())
        colors = [self._get_score_color(s) for s in scores]
        
        fig, ax = plt.subplots(figsize=self.viz_config.FIGURE_SIZE_DEFAULT)
        
        # Criar barras
        y_pos = np.arange(len(methods))
        bars = ax.barh(y_pos, scores, color=colors, edgecolor='black', linewidth=2)
        
        # Configurar eixos
        ax.set_yticks(y_pos)
        ax.set_yticklabels(methods)
        ax.set_xlabel('Pontuação de Adequabilidade (%)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlim([0, 100])
        
        # Adicionar valores nas barras
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 1, bar.get_y() + bar.get_height()/2,
                   f'{score:.1f}%', ha='left', va='center', fontweight='bold')
        
        # Adicionar linhas de referência
        ax.axvline(x=ScreeningConfig.THRESHOLD_ALTA, color='green', linestyle='--', 
                  alpha=0.5, linewidth=2, label='Alta (>80%)')
        ax.axvline(x=ScreeningConfig.THRESHOLD_MEDIA, color='orange', linestyle='--', 
                  alpha=0.5, linewidth=2, label='Média (60-80%)')
        ax.legend(loc='lower right', fontsize=10)
        
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        return fig
    
    def create_comparison_chart(self, comparison_data: Dict[str, Dict[str, float]],
                               title: str = "Comparação de Métodos EOR") -> plt.Figure:
        """
        Cria gráfico de comparação entre múltiplos critérios.
        
        Args:
            comparison_data: Dict com {método: {critério: score}}
            title: Título do gráfico
        
        Returns:
            matplotlib Figure
        """
        fig, axes = plt.subplots(2, 2, figsize=self.viz_config.FIGURE_SIZE_COMPARISON)
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        methods = list(comparison_data.keys())
        criteria = list(comparison_data[methods[0]].keys()) if methods else []
        
        # Subplot 1: Scores técnicos
        ax = axes[0, 0]
        technical_scores = [comparison_data[m].get('technical', 0) for m in methods]
        colors = [self._get_score_color(s) for s in technical_scores]
        ax.bar(range(len(methods)), technical_scores, color=colors)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels(methods, rotation=45, ha='right')
        ax.set_ylabel('Score (%)')
        ax.set_title('Critério Técnico')
        ax.set_ylim([0, 100])
        
        # Subplot 2: Scores econômicos
        ax = axes[0, 1]
        economic_scores = [comparison_data[m].get('economic', 0) for m in methods]
        colors = [self._get_score_color(s) for s in economic_scores]
        ax.bar(range(len(methods)), economic_scores, color=colors)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels(methods, rotation=45, ha='right')
        ax.set_ylabel('Score (%)')
        ax.set_title('Critério Econômico')
        ax.set_ylim([0, 100])
        
        # Subplot 3: Scores operacionais
        ax = axes[1, 0]
        operational_scores = [comparison_data[m].get('operational', 0) for m in methods]
        colors = [self._get_score_color(s) for s in operational_scores]
        ax.bar(range(len(methods)), operational_scores, color=colors)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels(methods, rotation=45, ha='right')
        ax.set_ylabel('Score (%)')
        ax.set_title('Critério Operacional')
        ax.set_ylim([0, 100])
        
        # Subplot 4: Scores ambientais
        ax = axes[1, 1]
        environmental_scores = [comparison_data[m].get('environmental', 0) for m in methods]
        colors = [self._get_score_color(s) for s in environmental_scores]
        ax.bar(range(len(methods)), environmental_scores, color=colors)
        ax.set_xticks(range(len(methods)))
        ax.set_xticklabels(methods, rotation=45, ha='right')
        ax.set_ylabel('Score (%)')
        ax.set_title('Critério Ambiental')
        ax.set_ylim([0, 100])
        
        plt.tight_layout()
        return fig
    
    def create_radar_chart(self, method_name: str, 
                          scores: Dict[str, float]) -> plt.Figure:
        """
        Cria gráfico radar (spider) para um método.
        
        Args:
            method_name: Nome do método EOR
            scores: Dict com {categoria: score}
        
        Returns:
            matplotlib Figure
        """
        categories = self.viz_config.RADAR_CATEGORIES
        values = [scores.get(cat, 0) for cat in categories]
        values += values[:1]  # Fechar o polígono
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=self.viz_config.FIGURE_SIZE_RADAR, 
                              subplot_kw=dict(projection='polar'))
        
        color = self._get_score_color(np.mean(values[:-1]))
        ax.plot(angles, values, 'o-', linewidth=2, color=color, label=method_name)
        ax.fill(angles, values, alpha=0.25, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=10)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], size=8)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        ax.set_title(f'{method_name} - Análise Multidimensional', 
                    size=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig


class V5ToV2Adapter:
    """
    Adaptador que integra funcionalidades do v5.py com petrochamp_v2.
    Permite usar componentes legados com nova arquitetura.
    """
    
    def __init__(self):
        """Inicializa o adaptador."""
        self.visualizer = SuitabilityVisualizer()
        logger.info("Adaptador V5→V2 inicializado")
    
    def convert_scores_format(self, method_scores: Dict[str, float]) -> Dict[str, Dict]:
        """
        Converte scores para formato com metadata.
        
        Args:
            method_scores: {método: score}
        
        Returns:
            {método: {score: float, level: SuitabilityLevel, color: str}}
        """
        result = {}
        for method, score in method_scores.items():
            level = get_suitability_level(score)
            result[method] = {
                'score': score,
                'level': level,
                'color': level.value[2],
                'label': level.name,
                'emoji': level.value[3]
            }
        return result
    
    def generate_summary_report(self, method_scores: Dict[str, float]) -> str:
        """
        Gera relatório de sumário em texto.
        
        Args:
            method_scores: {método: score}
        
        Returns:
            Texto formatado
        """
        converted = self.convert_scores_format(method_scores)
        
        lines = [
            "=" * 80,
            "RELATÓRIO DE TRIAGEM EOR - PetroChamp v2.0",
            "=" * 80,
            ""
        ]
        
        # Ordenar por score
        sorted_methods = sorted(converted.items(), key=lambda x: x[1]['score'], reverse=True)
        
        lines.append("RANKING DE MÉTODOS:")
        lines.append("-" * 80)
        
        for i, (method, data) in enumerate(sorted_methods, 1):
            lines.append(f"{i}. {method}")
            lines.append(f"   Score: {data['score']:.1f}%")
            lines.append(f"   Nível: {data['emoji']} {data['label']}")
            lines.append("")
        
        lines.append("-" * 80)
        lines.append("RECOMENDAÇÃO:")
        
        if sorted_methods:
            top_method = sorted_methods[0]
            lines.append(f"Método recomendado: {top_method[0]}")
            lines.append(f"Score de adequabilidade: {top_method[1]['score']:.1f}%")
            lines.append(f"Classificação: {top_method[1]['emoji']} {top_method[1]['label']}")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def export_to_dataframe(self, method_scores: Dict[str, float]) -> pd.DataFrame:
        """
        Exporta scores como DataFrame.
        
        Args:
            method_scores: {método: score}
        
        Returns:
            pandas DataFrame
        """
        converted = self.convert_scores_format(method_scores)
        
        data = []
        for method, scores in converted.items():
            data.append({
                'Método EOR': method,
                'Score (%)': scores['score'],
                'Nível': scores['label'],
                'Emoji': scores['emoji'],
                'Cor': scores['color']
            })
        
        return pd.DataFrame(data).sort_values('Score (%)', ascending=False)


class PetroChampV5GUI:
    """Interface gráfica compatível com v5.py usando petrochamp_v2."""
    
    def __init__(self, root: Optional[tk.Tk] = None):
        """
        Inicializa a interface gráfica.
        
        Args:
            root: Janela Tkinter principal (criará uma nova se não fornecida)
        """
        self.root = root or tk.Tk()
        self.root.title("PetroChamp v5.0 / v2.0")
        self.root.geometry("1200x800")
        
        self.adapter = V5ToV2Adapter()
        self.visualizer = SuitabilityVisualizer()
        
        self._setup_ui()
        logger.info("Interface gráfica inicializada")
    
    def _setup_ui(self):
        """Configura elementos da interface."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles
        control_frame = ttk.LabelFrame(main_frame, text="Entrada de Dados")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botões
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Carregar Dados", 
                  command=self.load_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Gerar Gráfico", 
                  command=self.generate_chart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exportar Relatório", 
                  command=self.export_report).pack(side=tk.LEFT, padx=5)
        
        # Frame de exibição
        display_frame = ttk.LabelFrame(main_frame, text="Visualização")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas_frame = ttk.Frame(display_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        logger.info("Interface gráfica configurada")
    
    def load_data(self):
        """Carrega dados de arquivo."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.json'):
                import json
                with open(file_path, 'r') as f:
                    self.data = json.load(f)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                self.data = df.to_dict(orient='records')[0]
            
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def generate_chart(self):
        """Gera gráfico de adequabilidade."""
        try:
            # Dados de exemplo
            method_scores = {
                'Injeção de Vapor': 82.5,
                'CO2 Miscível': 76.3,
                'Gás Não-Miscível': 68.1,
                'Polímeros': 71.4,
                'Combustão In Situ': 65.2
            }
            
            # Gerar gráfico
            fig = self.visualizer.create_suitability_chart(method_scores)
            
            # Exibir em canvas
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            messagebox.showinfo("Sucesso", "Gráfico gerado com sucesso!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")
    
    def export_report(self):
        """Exporta relatório."""
        try:
            method_scores = {
                'Injeção de Vapor': 82.5,
                'CO2 Miscível': 76.3,
                'Gás Não-Miscível': 68.1,
                'Polímeros': 71.4,
            }
            
            report = self.adapter.generate_summary_report(method_scores)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Sucesso", f"Relatório exportado: {file_path}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def run(self):
        """Executa a interface gráfica."""
        self.root.mainloop()


def launch_gui():
    """Lança a interface gráfica."""
    gui = PetroChampV5GUI()
    gui.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    launch_gui()
