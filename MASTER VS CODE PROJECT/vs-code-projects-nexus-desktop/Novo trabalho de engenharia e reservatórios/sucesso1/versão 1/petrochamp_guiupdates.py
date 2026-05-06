"""
ATUALIZAÇÃO DO PETROCHAMP - PLATAFORMA COMPLETA EOR
===================================================

Este código substitui a versão anterior (PetroChampGUI) pela nova plataforma completa (PetroChampPlatform).

Para usar:
1. Salve este código como petrochamp_guiupdates.py (substituindo o anterior)
2. Execute: python petrochamp_guiupdates.py

MELHORIAS DA NOVA VERSÃO:
• Interface profissional com dashboard e múltiplas abas
• Sistema de triagem com 7 métodos EOR e critérios detalhados
• Análise econômica completa (NPV, IRR, Payback)
• Gerenciamento de projetos (salvar/abrir)
• Visualização avançada de dados
• Exportação para Excel e outros formatos
• Sistema de ajuda e documentação
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import os
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# MÓDULO DE TRIAGEM EOR AVANÇADA
# ============================================================================
class EORScreeningEngine:
    """Motor de triagem EOR com múltiplos critérios"""
    
    def __init__(self):
        self.criteria = self._load_criteria()
        self.methods = list(self.criteria.keys())
        
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
            }
        }
    
    def score_reservoir(self, reservoir_data):
        """Calcula pontuação para cada método EOR"""
        scores = {}
        recommendations = {}
        
        for method, criteria in self.criteria.items():
            score = 0
            max_score = 0
            justificativas = []
            
            for param, limits in criteria.items():
                max_score += limits["peso"] * 100
                
                # Verificar se parâmetro existe nos dados
                if param in reservoir_data and reservoir_data[param] is not None:
                    value = reservoir_data[param]
                    
                    # Aplicar limites
                    if limits["min"] is not None and value < limits["min"]:
                        justificativas.append(f"{param} ({value}) abaixo do mínimo ({limits['min']})")
                    elif limits["max"] is not None and value > limits["max"]:
                        justificativas.append(f"{param} ({value}) acima do máximo ({limits['max']})")
                    else:
                        # Dentro dos limites - pontuação máxima
                        score += limits["peso"] * 100
                        justificativas.append(f"{param} ({value}) dentro dos limites aceitáveis")
                else:
                    justificativas.append(f"Parâmetro {param} não disponível")
            
            # Normalizar pontuação
            normalized_score = (score / max_score * 100) if max_score > 0 else 0
            
            # Classificação
            if normalized_score >= 80:
                status = "RECOMENDADO"
                color = "green"
            elif normalized_score >= 60:
                status = "POTENCIAL"
                color = "orange"
            else:
                status = "NÃO RECOMENDADO"
                color = "red"
            
            scores[method] = {
                "score": normalized_score,
                "status": status,
                "color": color,
                "justificativas": justificativas
            }
        
        return scores
    
    def get_recommendations(self, reservoir_data, top_n=3):
        """Retorna os top_n métodos recomendados"""
        scores = self.score_reservoir(reservoir_data)
        sorted_methods = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
        return sorted_methods[:top_n]

# ============================================================================
# MÓDULO DE ANÁLISE ECONÔMICA
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
        
        years = len(production) + params["construction_time"]
        cash_flow = np.zeros(years)
        
        for i in range(params["construction_time"]):
            cash_flow[i] = -capex_per_year
        
        for i in range(len(production)):
            cash_flow[i + params["construction_time"]] = operational_cf[i]
        
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
        periods = np.arange(len(cash_flow))
        return np.sum(cash_flow / ((1 + discount_rate / 100) ** periods))
    
    def calculate_irr(self, cash_flow):
        """Calcula Taxa Interna de Retorno"""
        try:
            import numpy_financial as nf
            return nf.irr(cash_flow) * 100
        except:
            def npv_func(rate):
                periods = np.arange(len(cash_flow))
                return np.sum(cash_flow / ((1 + rate) ** periods))
            
            low, high = -0.99, 1.0
            for _ in range(1000):
                mid = (low + high) / 2
                val = npv_func(mid)
                if abs(val) < 1e-6:
                    return mid * 100
                if npv_func(low) * val < 0:
                    high = mid
                else:
                    low = mid
            return mid * 100
    
    def calculate_payback(self, cash_flow):
        """Calcula período de payback"""
        cumulative = np.cumsum(cash_flow)
        for i, val in enumerate(cumulative):
            if val >= 0:
                if i == 0:
                    return 0
                prev_val = cumulative[i-1]
                year_fraction = abs(prev_val) / (val - prev_val) if (val - prev_val) != 0 else 0
                return i - 1 + year_fraction
        return None
    
    def generate_production_profile(self, initial_rate, decline_rate, years):
        """Gera perfil de produção com declínio"""
        profile = []
        for year in range(years):
            production = initial_rate * ((100 - decline_rate) / 100) ** year
            profile.append(production)
        return profile

# ============================================================================
# PLATAFORMA PRINCIPAL - PETROCHAMP PLATFORM (VERSÃO CORRIGIDA)
# ============================================================================
class PetroChampPlatform:
    """Plataforma principal PetroChamp - VERSÃO CORRIGIDA"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Configuração inicial
        self.root.title("PetroChamp - Plataforma de Triagem EOR")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Inicializar módulos
        self.screening_engine = EORScreeningEngine()
        self.economic_analyzer = EconomicAnalyzer()
        
        # Estado da aplicação
        self.current_project = None
        self.reservoir_data = None
        self.screening_results = None
        self.economic_results = None
        
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
        """Cria barra de menu CORRIGIDA - removidas referências a métodos inexistentes"""
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
        menubar.add_cascade(label="Análise", menu=analysis_menu)
        
        # Menu Visualização (corrigido)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Gráfico de Pontuação", command=self.show_score_chart)
        view_menu.add_command(label="Visualizar Gráficos Econômicos", command=self.plot_economic_charts)
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
        
        self.status_bar = tk.Label(self.root, text="Pronto | PetroChamp Plataforma EOR", 
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
        
        tk.Label(title_frame, text="Versão completa com 7 métodos EOR e análise econômica integrada", 
                font=('Arial', 12), fg=self.colors['dark']).pack()
        
        cards_frame = ttk.Frame(self.dashboard_tab)
        cards_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.card1 = self._create_card(cards_frame, "📊 Dados do Reservatório", 
                                      "Carregue dados para análise", 0, 0)
        self.card2 = self._create_card(cards_frame, "🔍 Triagem EOR", 
                                      "Execute análise técnica", 0, 1)
        self.card3 = self._create_card(cards_frame, "💰 Análise Econômica", 
                                      "Avalie viabilidade financeira", 1, 0)
        self.card4 = self._create_card(cards_frame, "📈 Resultados", 
                                      "Visualize e exporte resultados", 1, 1)
        
        actions_frame = ttk.LabelFrame(self.dashboard_tab, text="Ações Rápidas", padding=20)
        actions_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Button(actions_frame, text="Importar Dados CSV", 
                  command=self.import_csv, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Executar Análise Completa", 
                  command=self.run_complete_analysis, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Gerar Relatório Excel", 
                  command=self.export_excel, width=20).pack(side=tk.LEFT, padx=5)
        
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
            ("Salinidade", "ppm"), ("Espessura", "m"), ("TAN", "mg KOH/g")
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
        ttk.Button(control_frame, text="Selecionar Todos", 
                  command=self.select_all_methods, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Limpar Seleção", 
                  command=self.clear_selection, width=20).pack(side=tk.LEFT, padx=5)
        
        methods_frame = ttk.LabelFrame(self.screening_tab, text="Métodos EOR Disponíveis", padding=15)
        methods_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.method_vars = {}
        methods = self.screening_engine.methods
        
        for i, method in enumerate(methods):
            var = tk.BooleanVar(value=True)
            self.method_vars[method] = var
            
            cb = ttk.Checkbutton(methods_frame, text=method, variable=var)
            cb.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=5)
        
        for i in range(3):
            methods_frame.grid_columnconfigure(i, weight=1)
            
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
        """Cria aba de resultados"""
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Resultados")
        
        results_notebook = ttk.Notebook(self.results_tab)
        results_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        table_tab = ttk.Frame(results_notebook)
        results_notebook.add(table_tab, text="Tabela")
        
        self.results_tree = ttk.Treeview(table_tab, columns=("Método", "Pontuação", "Status", "Recomendação"))
        self.results_tree.heading("Método", text="Método")
        self.results_tree.heading("Pontuação", text="Pontuação")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.heading("Recomendação", text="Recomendação")
        
        self.results_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        chart_tab = ttk.Frame(results_notebook)
        results_notebook.add(chart_tab, text="Gráficos")
        
        self.chart_frame = ttk.Frame(chart_tab)
        self.chart_frame.pack(fill='both', expand=True)
        
        export_frame = ttk.Frame(self.results_tab)
        export_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(export_frame, text="Exportar para Excel", 
                  command=self.export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Copiar Resultados", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
    # ============================================================================
    # MÉTODOS DE AÇÃO
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
                "TAN": 1.2
            },
            {
                "ID": 2,
                "API": 32.0,
                "Viscosidade": 8,
                "Profundidade": 2500,
                "Permeabilidade": 180,
                "Porosidade": 18,
                "Saturação de Óleo": 45,
                "Saturação de Água": 55,
                "Temperatura": 95,
                "Pressão": 3200,
                "Salinidade": 85000,
                "Espessura": 8,
                "TAN": 0.3
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
                    reservoir[param] = float(value) if param != "TAN" else float(value)
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
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos")
            
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
        """Executa triagem EOR"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado de reservatório disponível")
            return
            
        self.update_status("Executando triagem EOR...")
        
        try:
            reservoir = self.reservoir_data[0]
            scores = self.screening_engine.score_reservoir(reservoir)
            
            self.screening_results = scores
            self._update_results_table(scores)
            
            self.update_status("Triagem concluída")
            messagebox.showinfo("Sucesso", "Triagem EOR executada com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na triagem: {str(e)}")
            self.update_status("Erro na triagem")
            
    def _update_results_table(self, scores):
        """Atualiza tabela de resultados"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        for method, data in scores.items():
            score = data["score"]
            status = data["status"]
            
            tag = "green" if status == "RECOMENDADO" else "orange" if status == "POTENCIAL" else "red"
            
            self.results_tree.insert("", tk.END, values=(
                method, 
                f"{score:.1f}%", 
                status,
                "✓" if score >= 80 else "⚠" if score >= 60 else "✗"
            ), tags=(tag,))
            
        self.results_tree.tag_configure("green", foreground="green")
        self.results_tree.tag_configure("orange", foreground="orange")
        self.results_tree.tag_configure("red", foreground="red")
        
    def run_economic_analysis(self):
        """Executa análise econômica"""
        try:
            self.update_status("Calculando análise econômica...")
            
            economic_params = {}
            for param, entry in self.econ_entries.items():
                value = entry.get()
                if value:
                    economic_params[param.lower().replace(" ", "_")] = float(value)
            
            initial_rate = float(self.prod_entry.get())
            production_profile = self.economic_analyzer.generate_production_profile(
                initial_rate, 
                economic_params.get("taxa_de_declínio", 15),
                economic_params.get("vida_do_projeto", 15)
            )
            
            cashflow_data = self.economic_analyzer.calculate_cash_flow(
                production_profile, economic_params
            )
            
            npv = self.economic_analyzer.calculate_npv(
                cashflow_data["cash_flow"], 
                economic_params.get("taxa_de_desconto", 10)
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
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na análise: {str(e)}")
            
    def _display_economic_results(self, npv, irr, payback, cashflow_data):
        """Exibe resultados econômicos"""
        self.results_text.delete(1.0, tk.END)
        
        text = "=== RESULTADOS DA ANÁLISE ECONÔMICA ===\n\n"
        text += f"Valor Presente Líquido (NPV): ${npv:,.2f}\n"
        text += f"Taxa Interna de Retorno (IRR): {irr:.2f}%\n"
        text += f"Payback Período: {payback:.2f} anos\n\n"
        
        text += f"Investimento Total (CAPEX): ${cashflow_data['capex']:,.2f}\n\n"
        
        text += "Fluxo de Caixa por Ano:\n"
        text += "Ano | Fluxo de Caixa ($)\n"
        text += "-" * 30 + "\n"
        
        for year, cf in enumerate(cashflow_data["cash_flow"]):
            text += f"{year:3d} | ${cf:12,.2f}\n"
            
        self.results_text.insert(1.0, text)
        
    def plot_economic_charts(self):
        """Plota gráficos econômicos - MÉTODO CORRIGIDO"""
        if not hasattr(self, 'economic_results') or not self.economic_results:
            messagebox.showwarning("Aviso", "Execute a análise econômica primeiro")
            return
            
        # Limpar frame anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Criar figura com múltiplos gráficos
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        
        # Dados para gráficos
        cf = self.economic_results["cashflow"]["cash_flow"]
        revenue = self.economic_results["cashflow"]["revenue"]
        opex = self.economic_results["cashflow"]["opex"]
        
        years = list(range(len(cf)))
        
        # Gráfico 1: Fluxo de caixa acumulado
        axes[0, 0].plot(years, np.cumsum(cf), 'b-', linewidth=2, marker='o')
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 0].set_title("Fluxo de Caixa Acumulado")
        axes[0, 0].set_xlabel("Ano")
        axes[0, 0].set_ylabel("USD")
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Receita vs OPEX
        x = list(range(1, len(revenue) + 1))
        axes[0, 1].bar(x, revenue, alpha=0.6, label='Receita')
        axes[0, 1].bar(x, opex, alpha=0.6, label='OPEX')
        axes[0, 1].set_title("Receita vs OPEX")
        axes[0, 1].set_xlabel("Ano")
        axes[0, 1].set_ylabel("USD")
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Pontuação dos métodos EOR (se disponível)
        if hasattr(self, 'screening_results') and self.screening_results:
            methods = list(self.screening_results.keys())
            scores = [self.screening_results[m]["score"] for m in methods]
            colors = [self.screening_results[m]["color"] for m in methods]
            
            axes[1, 0].barh(methods, scores, color=colors)
            axes[1, 0].set_title("Pontuação dos Métodos EOR")
            axes[1, 0].set_xlabel("Pontuação (%)")
            axes[1, 0].set_xlim(0, 100)
            
            # Adicionar valores nas barras
            for i, (method, score) in enumerate(zip(methods, scores)):
                axes[1, 0].text(score + 1, i, f'{score:.1f}%', va='center')
        else:
            axes[1, 0].text(0.5, 0.5, "Execute a triagem EOR\npara ver resultados", 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title("Pontuação dos Métodos EOR")
            
        # Gráfico 4: Sensibilidade do NPV
        discount_rates = np.linspace(5, 20, 10)
        npv_values = [self.economic_analyzer.calculate_npv(cf, dr) for dr in discount_rates]
        
        axes[1, 1].plot(discount_rates, npv_values, 'g-', linewidth=2, marker='s')
        axes[1, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 1].set_title("Sensibilidade do NPV")
        axes[1, 1].set_xlabel("Taxa de Desconto (%)")
        axes[1, 1].set_ylabel("NPV (USD)")
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Embed no Tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def show_score_chart(self):
        """Mostra gráfico de pontuação dos métodos EOR"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro")
            return
            
        # Criar nova janela para o gráfico
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Gráfico de Pontuação - Métodos EOR")
        chart_window.geometry("800x600")
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        methods = list(self.screening_results.keys())
        scores = [self.screening_results[m]["score"] for m in methods]
        colors = [self.screening_results[m]["color"] for m in methods]
        
        bars = ax.barh(methods, scores, color=colors)
        ax.set_xlabel('Pontuação (%)')
        ax.set_title('Triagem EOR - Pontuação dos Métodos')
        ax.set_xlim(0, 100)
        
        # Adicionar valores nas barras
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                   f'{score:.1f}%', ha='left', va='center')
        
        # Adicionar legenda de cores
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', label='RECOMENDADO (≥80%)'),
            Patch(facecolor='orange', label='POTENCIAL (60-79%)'),
            Patch(facecolor='red', label='NÃO RECOMENDADO (<60%)')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        
        # Embed no Tkinter
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(canvas, chart_window)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def run_complete_analysis(self):
        """Executa análise completa (triagem + econômica)"""
        if not self.reservoir_data:
            messagebox.showwarning("Aviso", "Nenhum dado de reservatório disponível")
            return
            
        self.update_status("Iniciando análise completa...")
        
        # Executar triagem
        self.run_screening()
        
        # Executar análise econômica
        self.run_economic_analysis()
        
        # Navegar para aba de resultados
        self.notebook.select(self.results_tab)
        
        messagebox.showinfo("Análise Completa", "Análise técnica e econômica concluída!")
        self.update_status("Análise completa concluída")
        
    def export_excel(self):
        """Exporta resultados para Excel"""
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
                    "Status": scores["status"]
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
                        "IRR": [f"{self.economic_results['irr']:.2f}%"],
                        "Payback": [f"{self.economic_results['payback']:.2f} anos"]
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
        self.reservoir_data = None
        self.screening_results = None
        self.economic_results = None
        
        # Limpar interfaces
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        self.results_text.delete(1.0, tk.END)
        
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
                "timestamp": datetime.now().isoformat(),
                "version": "PetroChamp 2.0"
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
                
            self.reservoir_data = project_data.get("reservoir_data")
            self.screening_results = project_data.get("screening_results")
            self.economic_results = project_data.get("economic_results")
            
            # Atualizar interfaces
            self._update_data_tree()
            
            if self.screening_results:
                self._update_results_table(self.screening_results)
                
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
        PETROCHAMP - PLATAFORMA DE TRIAGEM EOR
        
        FUNCIONALIDADES PRINCIPAIS:
        1. IMPORTAR DADOS:
           • CSV: Arquivos com dados de reservatórios
           • Excel: Planilhas com múltiplas abas
           • Manual: Inserção direta de parâmetros
        
        2. TRIAGEM EOR:
           • Avaliação de 7 métodos de recuperação avançada
           • Critérios técnicos baseados em literatura
           • Pontuação automática e classificação
           • Justificativas detalhadas
        
        3. ANÁLISE ECONÔMICA:
           • Cálculo de NPV, IRR e Payback
           • Projeção de fluxo de caixa
           • Parâmetros ajustáveis (preço, taxas, custos)
           • Gráficos interativos
        
        4. RESULTADOS:
           • Tabela comparativa de métodos
           • Gráficos de pontuação e econômicos
           • Exportação para Excel
           • Cópia para clipboard
        
        5. GERENCIAMENTO:
           • Salvar projetos em JSON
           • Abrir projetos salvos
           • Limpar dados
           • Executar análise completa
        
        MÉTODOS EOR DISPONÍVEIS:
        1. Injeção de Vapor
        2. Combustão In Situ
        3. Injeção de CO2 Miscível
        4. Injeção de Polímeros
        5. Injeção de Surfactantes
        6. Injeção Alcalina
        7. Injeção de Gás Não-Miscível
        
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
        
        INSTRUÇÕES DE USO:
        1. Importe dados ou insira manualmente
        2. Execute a triagem EOR
        3. Configure parâmetros econômicos
        4. Calcule análise econômica
        5. Visualize resultados e exporte
        
        DICAS:
        • Use o exemplo para testar a plataforma
        • Exporte resultados para análise detalhada
        • Salve projetos para trabalho futuro
        """
        
        # Criar janela de documentação
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Documentação - PetroChamp")
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
        PetroChamp - Plataforma de Triagem EOR
        Versão 2.0
        
        Desenvolvido para auxiliar engenheiros de reservatórios
        na seleção de métodos de Recuperação Avançada de Petróleo.
        
        Características:
        • Interface profissional com múltiplas abas
        • 7 métodos EOR com critérios técnicos
        • Análise econômica completa (NPV, IRR, Payback)
        • Sistema de gerenciamento de projetos
        • Exportação para Excel e JSON
        
        Data: {datetime.now().strftime('%d/%m/%Y')}
        © 2024 PetroChamp Team
        
        Dependências:
        • Python 3.8+
        • Pandas, NumPy, Matplotlib
        • Seaborn, Openpyxl
        
        Para suporte ou relatar problemas:
        • Verifique a documentação
        • Verifique as dependências instaladas
        """
        
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre o PetroChamp")
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
            self.reservoir_data = None
            self.screening_results = None
            self.economic_results = None
            
            # Limpar interfaces
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
                
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
                
            self.results_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Sucesso", "Todos os dados foram removidos")
            self.update_status("Todos os dados removidos")
            
    def copy_to_clipboard(self):
        """Copia resultados da triagem para clipboard"""
        if not hasattr(self, 'screening_results') or not self.screening_results:
            messagebox.showwarning("Aviso", "Nenhum resultado para copiar")
            return
            
        text = "RESULTADOS DA TRIAGEM EOR - PETROCHAMP\n"
        text += "=" * 50 + "\n\n"
        
        for method, data in self.screening_results.items():
            text += f"Método: {method}\n"
            text += f"Pontuação: {data['score']:.1f}%\n"
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
        print("INICIANDO PETROCHAMP - PLATAFORMA DE TRIAGEM EOR")
        print("Versão: 2.0 (Corrigida)")
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
            with open('petrochamp_error.log', 'w') as f:
                f.write(error_msg)
            print("\nLog de erro salvo em: petrochamp_error.log")
        except:
            pass

if __name__ == "__main__":
    main()