import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox

# Configurar aparência
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class EORSelectionApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Seleção de Reservatórios para EOR")
        self.root.geometry("1200x700")
        
        # Parâmetros padrão
        self.default_params = {
            "api": 30.0,
            "porosity": 20.0,
            "permeability": 100.0,
            "viscosity": 10.0,
            "water_saturation": 30.0,
            "pressure": 2000.0,
            "temperature": 80.0,
            "depth": 2000.0,
            "oil_price": 60.0,
            "discount_rate": 10.0,
            "capital_cost": 5000000.0,
            "operating_cost": 1000000.0
        }
        
        # Critérios de EOR
        self.eor_criteria = {
            "Gas Injection": {"min_api": 30, "max_viscosity": 10, "min_porosity": 12},
            "Thermal": {"max_api": 25, "min_viscosity": 50, "max_depth": 5000},
            "Chemical": {"min_porosity": 15, "max_permeability": 5000, "min_api": 20},
            "Polymer": {"min_porosity": 15, "max_salinity": 100000, "max_temp": 90},
            "CO2 Miscible": {"min_api": 27, "max_viscosity": 12, "min_pressure": 1200},
            "Steam Injection": {"max_api": 25, "min_viscosity": 100, "max_depth": 4500}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Criar frames principais
        self.left_frame = ctk.CTkFrame(self.root, width=400)
        self.left_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)
        
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Configurar grid no left_frame
        self.left_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            self.left_frame, 
            text="Seleção de Reservatórios EOR",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="w")
        
        # Parâmetros do reservatório
        params_label = ctk.CTkLabel(
            self.left_frame,
            text="Parâmetros do Reservatório",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        params_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        # Widgets de entrada
        self.entries = {}
        row = 2
        
        parameters = [
            ("Gravidade API (°):", "api", 10, 50),
            ("Porosidade (%):", "porosity", 5, 35),
            ("Permeabilidade (mD):", "permeability", 1, 10000),
            ("Viscosidade (cP):", "viscosity", 1, 10000),
            ("Saturação de Água (%):", "water_saturation", 10, 80),
            ("Pressão (psi):", "pressure", 500, 10000),
            ("Temperatura (°C):", "temperature", 30, 200),
            ("Profundidade (m):", "depth", 500, 5000),
            ("Preço do Óleo ($/bbl):", "oil_price", 20, 150),
            ("Taxa de Desconto (%):", "discount_rate", 1, 20),
            ("Custo Capital ($):", "capital_cost", 100000, 10000000),
            ("Custo Operacional ($/ano):", "operating_cost", 100000, 5000000)
        ]
        
        for label_text, key, min_val, max_val in parameters:
            # Label
            label = ctk.CTkLabel(self.left_frame, text=label_text)
            label.grid(row=row, column=0, padx=(10, 5), pady=5, sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(self.left_frame, width=150)
            entry.insert(0, str(self.default_params[key]))
            entry.grid(row=row, column=1, padx=(0, 10), pady=5, sticky="w")
            self.entries[key] = entry
            
            # Slider
            slider = ctk.CTkSlider(
                self.left_frame, 
                from_=min_val, 
                to=max_val,
                command=lambda val, e=entry: self.on_slider_change(val, e)
            )
            slider.set(self.default_params[key])
            slider.grid(row=row, column=2, padx=(0, 10), pady=5, sticky="ew")
            self.entries[f"{key}_slider"] = slider
            
            row += 1
        
        # Botões de controle
        button_frame = ctk.CTkFrame(self.left_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20, sticky="ew")
        
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        calc_button = ctk.CTkButton(
            button_frame,
            text="Avaliar Reservatório",
            command=self.evaluate_reservoir,
            height=40
        )
        calc_button.grid(row=0, column=0, padx=5, pady=5)
        
        import_button = ctk.CTkButton(
            button_frame,
            text="Importar CSV",
            command=self.import_csv,
            height=40
        )
        import_button.grid(row=0, column=1, padx=5, pady=5)
        
        export_button = ctk.CTkButton(
            button_frame,
            text="Exportar Resultados",
            command=self.export_results,
            height=40
        )
        export_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Tema
        theme_label = ctk.CTkLabel(self.left_frame, text="Tema:")
        theme_label.grid(row=row+1, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
        
        theme_var = ctk.StringVar(value="System")
        theme_menu = ctk.CTkOptionMenu(
            self.left_frame,
            values=["System", "Dark", "Light"],
            command=self.change_theme,
            variable=theme_var
        )
        theme_menu.grid(row=row+1, column=1, padx=(0, 10), pady=(10, 5), sticky="w")
        
        # Área de resultados no right_frame
        self.setup_results_area()
        
    def setup_results_area(self):
        # Notebook para múltiplas abas
        self.tabview = ctk.CTkTabview(self.right_frame)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba de Recomendações
        self.recommendations_tab = self.tabview.add("Recomendações")
        self.results_text = ctk.CTkTextbox(self.recommendations_tab)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba de Gráficos
        self.graphs_tab = self.tabview.add("Gráficos")
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self.graphs_tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba Econômica
        self.economic_tab = self.tabview.add("Análise Econômica")
        self.economic_text = ctk.CTkTextbox(self.economic_tab)
        self.economic_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Progress bars para pontuação
        self.score_frame = ctk.CTkFrame(self.right_frame)
        self.score_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bars = {}
        methods = list(self.eor_criteria.keys())
        for i, method in enumerate(methods):
            label = ctk.CTkLabel(self.score_frame, text=method, width=150)
            label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            progressbar = ctk.CTkProgressBar(self.score_frame, width=300)
            progressbar.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
            progressbar.set(0)
            self.progress_bars[method] = progressbar
            
            score_label = ctk.CTkLabel(self.score_frame, text="0%", width=50)
            score_label.grid(row=i, column=2, padx=5, pady=2, sticky="w")
            self.progress_bars[f"{method}_label"] = score_label
        
        self.score_frame.grid_columnconfigure(1, weight=1)
    
    def on_slider_change(self, value, entry):
        entry.delete(0, tk.END)
        entry.insert(0, f"{value:.2f}")
    
    def evaluate_reservoir(self):
        try:
            # Coletar dados
            params = {}
            for key in self.default_params.keys():
                try:
                    value = self.entries[key].get()
                    if not value:
                        messagebox.showerror("Erro", f"Por favor, insira um valor para {key}")
                        return
                    params[key] = float(value)
                except ValueError:
                    messagebox.showerror("Erro", f"Valor inválido para {key}. Por favor, insira um número válido.")
                    return
            
            # Avaliar métodos EOR
            recommendations = self.assess_eor_methods(params)
            
            # Calcular NPV
            npv, cash_flows = self.calculate_npv(params)
            
            # Exibir resultados
            self.display_results(params, recommendations, npv, cash_flows)
            
            # Atualizar gráficos
            self.update_graphs(recommendations, npv, cash_flows)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na avaliação: {str(e)}")
    
    def assess_eor_methods(self, params):
        scores = {}
        recommendations = {}
        
        for method, criteria in self.eor_criteria.items():
            score = 0
            max_score = len(criteria) * 20
            
            if "min_api" in criteria and params["api"] >= criteria["min_api"]:
                score += 20
            if "max_api" in criteria and params["api"] <= criteria["max_api"]:
                score += 20
            if "min_porosity" in criteria and params["porosity"] >= criteria["min_porosity"]:
                score += 20
            if "max_viscosity" in criteria and params["viscosity"] <= criteria["max_viscosity"]:
                score += 20
            if "min_viscosity" in criteria and params["viscosity"] >= criteria["min_viscosity"]:
                score += 20
            if "max_depth" in criteria and params["depth"] <= criteria["max_depth"]:
                score += 20
            if "min_pressure" in criteria and params["pressure"] >= criteria["min_pressure"]:
                score += 20
            if "max_temp" in criteria and params["temperature"] <= criteria["max_temp"]:
                score += 20
            
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            scores[method] = percentage
            
            if percentage >= 60:
                recommendations[method] = "RECOMENDADO"
            elif percentage >= 40:
                recommendations[method] = "POTENCIAL"
            else:
                recommendations[method] = "NÃO RECOMENDADO"
        
        return {"scores": scores, "recommendations": recommendations}
    
    def calculate_npv(self, params, years=10):
        # Cálculo simplificado do NPV
        initial_investment = params["capital_cost"]
        annual_production = 1000000  # bbl/ano (valor exemplo)
        annual_revenue = annual_production * params["oil_price"]
        annual_cost = params["operating_cost"]
        annual_cash_flow = annual_revenue - annual_cost
        
        cash_flows = []
        npv = -initial_investment
        
        discount_rate_decimal = params["discount_rate"] / 100
        
        for year in range(1, years + 1):
            discounted_cf = annual_cash_flow / ((1 + discount_rate_decimal) ** year)
            cash_flows.append(discounted_cf)
            npv += discounted_cf
        
        return npv, cash_flows
    
    def display_results(self, params, recommendations, npv, cash_flows):
        # Limpar texto anterior
        self.results_text.delete("1.0", tk.END)
        self.economic_text.delete("1.0", tk.END)
        
        # Exibir parâmetros
        result_text = "=== PARÂMETROS DO RESERVATÓRIO ===\n\n"
        for key, value in params.items():
            formatted_key = key.replace('_', ' ').title()
            if key in ['capital_cost', 'operating_cost']:
                result_text += f"{formatted_key}: ${value:,.2f}\n"
            elif key in ['oil_price']:
                result_text += f"{formatted_key}: ${value:.2f}\n"
            elif key in ['api', 'porosity', 'water_saturation', 'discount_rate']:
                result_text += f"{formatted_key}: {value:.2f}%\n"
            else:
                result_text += f"{formatted_key}: {value:.2f}\n"
        
        result_text += "\n=== RECOMENDAÇÕES EOR ===\n\n"
        
        scores = recommendations["scores"]
        recs = recommendations["recommendations"]
        
        for method in scores.keys():
            percentage = scores[method]
            status = recs[method]
            
            result_text += f"{method}:\n"
            result_text += f"  Pontuação: {percentage:.1f}% - {status}\n"
            
            # Atualizar progress bars
            self.progress_bars[method].set(percentage / 100)
            self.progress_bars[f"{method}_label"].configure(text=f"{percentage:.1f}%")
            
            # Adicionar justificativa baseada nos critérios
            if status == "RECOMENDADO":
                result_text += "  ✓ Atende aos principais critérios\n"
            elif status == "POTENCIAL":
                result_text += "  ⚠ Requer análise mais detalhada\n"
            else:
                result_text += "  ✗ Não atende aos critérios mínimos\n"
            
            result_text += "\n"
        
        self.results_text.insert("1.0", result_text)
        
        # Exibir análise econômica
        economic_text = "=== ANÁLISE ECONÔMICA ===\n\n"
        economic_text += f"Valor Presente Líquido (NPV): ${npv:,.2f}\n"
        economic_text += f"Investimento Inicial: ${params['capital_cost']:,.2f}\n"
        economic_text += f"Taxa de Desconto: {params['discount_rate']}%\n\n"
        
        economic_text += "Fluxo de Caixa Descontado (10 anos):\n"
        for year, cf in enumerate(cash_flows, 1):
            economic_text += f"  Ano {year}: ${cf:,.2f}\n"
        
        roi_percentage = (npv / params['capital_cost'] * 100) if params['capital_cost'] != 0 else 0
        economic_text += f"\nRetorno sobre Investimento (ROI): {roi_percentage:.1f}%\n"
        
        if npv > 0:
            economic_text += "\n✓ PROJETO ECONOMICAMENTE VIÁVEL\n"
        else:
            economic_text += "\n✗ PROJETO NÃO VIÁVEL ECONOMICAMENTE\n"
        
        self.economic_text.insert("1.0", economic_text)
    
    def update_graphs(self, recommendations, npv, cash_flows):
        # Limpar gráfico anterior
        self.ax.clear()
        
        # Gráfico 1: Pontuação dos métodos EOR
        methods = list(recommendations["scores"].keys())
        scores = list(recommendations["scores"].values())
        
        colors = []
        for method in methods:
            if recommendations["recommendations"][method] == "RECOMENDADO":
                colors.append('green')
            elif recommendations["recommendations"][method] == "POTENCIAL":
                colors.append('orange')
            else:
                colors.append('red')
        
        bars = self.ax.barh(methods, scores, color=colors)
        self.ax.set_xlabel('Pontuação (%)')
        self.ax.set_title('Avaliação de Métodos EOR')
        self.ax.set_xlim(0, 100)
        
        # Adicionar valores nas barras
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            self.ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                        f'{score:.1f}%', ha='left', va='center')
        
        # Adicionar grade
        self.ax.grid(axis='x', alpha=0.3)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Importar arquivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = pd.read_csv(file_path)
                if not df.empty:
                    # Assumindo que o CSV tem colunas com nomes específicos
                    for col in df.columns:
                        col_lower = col.lower().replace(' ', '_')
                        if col_lower in self.entries:
                            value = str(df[col].iloc[0])
                            self.entries[col_lower].delete(0, tk.END)
                            self.entries[col_lower].insert(0, value)
                    
                    messagebox.showinfo("Sucesso", "Dados importados com sucesso!")
                    # Avaliar automaticamente após importação
                    self.evaluate_reservoir()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar CSV: {str(e)}")
    
    def export_results(self):
        file_path = filedialog.asksaveasfilename(
            title="Exportar resultados",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Coletar dados atuais
                params = {}
                for key in self.default_params.keys():
                    try:
                        params[key] = float(self.entries[key].get())
                    except:
                        params[key] = 0.0
                
                # Avaliar métodos EOR
                recommendations = self.assess_eor_methods(params)
                
                # Calcular NPV
                npv, cash_flows = self.calculate_npv(params)
                
                # Preparar conteúdo
                content = "=== RELATÓRIO DE SELEÇÃO EOR ===\n\n"
                content += "Parâmetros do Reservatório:\n"
                for key, value in params.items():
                    content += f"  {key.replace('_', ' ').title()}: {value:.2f}\n"
                
                content += "\nRecomendações EOR:\n"
                scores = recommendations["scores"]
                recs = recommendations["recommendations"]
                for method in scores.keys():
                    content += f"  {method}: {scores[method]:.1f}% - {recs[method]}\n"
                
                content += f"\nAnálise Econômica:\n"
                content += f"  NPV: ${npv:,.2f}\n"
                roi_percentage = (npv/params['capital_cost']*100) if params['capital_cost'] != 0 else 0
                content += f"  ROI: {roi_percentage:.1f}%\n"
                
                # Salvar arquivo
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("Sucesso", f"Resultados exportados para:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EORSelectionApp()
    app.run()