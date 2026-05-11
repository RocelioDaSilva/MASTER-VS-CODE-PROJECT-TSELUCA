"""
PetroChamp-like GUI em Python
Funcionalidades:
- Ler CSV de reservatórios ou entrada manual
- Triagem técnica para seleção de EOR (térmico, químico, miscível, imiscível, MEOR)
- Cálculo simples de viabilidade económica (fluxo de caixa, NPV, IRR, payback)
- Gráficos e exportação de resultados

Dependências: pandas, numpy, matplotlib
Instalação:
    pip install pandas numpy matplotlib
Executar:
    python petrochamp_gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ---------------------------
# Regras de triagem EOR
# ---------------------------
def recomenda_eor_row(row):
    """
    Recebe uma linha (Series) com:
    Profundidade (m), Viscosidade (cP), API, Salinidade (ppm),
    Litologia (string), Permeabilidade (mD), Temperatura (°C), Saturacao (%)
    Retorna (metodo, justificativas(list))
    """
    profundidade = try_float(row.get("Profundidade"))
    viscosidade = try_float(row.get("Viscosidade"))
    api = try_float(row.get("API"))
    salinidade = try_float(row.get("Salinidade"))
    litologia = str(row.get("Litologia","")).lower()
    permeab = try_float(row.get("Permeabilidade"))
    temp = try_float(row.get("Temperatura"))
    saturacao = try_float(row.get("Saturacao"))

    justificativas = []

    # Térmico: óleo pesado, alta viscosidade, reservatórios rasos
    if viscosidade is not None and api is not None:
        if viscosidade > 100 and api < 20 and (profundidade is None or profundidade <= 900):
            justificativas.append(f"Óleo pesado (API {api}) e viscosidade alta ({viscosidade} cP) => favorece processo térmico.")
            return "Térmico (vapor / combustão in-situ)", justificativas

    # Químico (polímero/surfactante): viscosidade moderada, permeabilidade razoável, limitação salinidade/temperatura
    if (viscosidade is None or viscosidade < 10000) and (permeab is not None and permeab > 10) and (salinidade is None or salinidade < 20000) and (temp is None or temp < 95):
        justificativas.append(f"Condições condizentes com polímero/surfactante: permeab {permeab} mD, salinidade {salinidade} ppm, temp {temp}°C.")
        if "carbonat" in litologia:
            justificativas.append("Atenção: litologia carbonática aumenta adsorção de polímeros.")
        return "Químico (polímeros / surfactantes)", justificativas

    # Gás miscível (CO2 / HC): óleo leve (API alto), profundidade/pressão alta favorece miscibilidade
    if api is not None and api >= 25:
        justificativas.append(f"Óleo leve (API {api}) => adequado para gás miscível (CO2/HC) quando pressão permitir.")
        return "Gás miscível (CO2 / HC)", justificativas

    # Gás imiscível (N2 / flue gas) - alternativa para API médio
    if api is not None and 10 <= api < 25:
        justificativas.append(f"API médio ({api}) => gás imiscível como N₂ ou flue gas pode ajudar suporte de pressão.")
        return "Gás imiscível (N₂ / flue gas)", justificativas

    # MEOR / Outros
    justificativas.append("Condições não cobertas por regras anteriores — considerar MEOR / estudos adicionais.")
    return "Biológico (MEOR) ou outros", justificativas

def try_float(x):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return None
        return float(x)
    except Exception:
        return None

# ---------------------------
# Funções económicas simples
# ---------------------------
def calcular_fluxo_caixa(producao_bopd, price_usd_per_bbl, opex_usd_per_bbl, capex=0.0, anos=None):
    """
    producao_bopd: array anual ou por mês? vamos assumir anual production (bbl/year)
    price_usd_per_bbl: preço por barril
    opex_usd_per_bbl: custo operacional por barril
    capex: gasto inicial (negativo)
    Retorna: fluxo_caixa array (período 0..N), NPV, IRR, payback_years (float or None)
    """
    prod = np.array(producao_bopd, dtype=float)
    revenue = prod * price_usd_per_bbl
    opex = prod * opex_usd_per_bbl
    cash_flow_operational = revenue - opex
    # Criar fluxo com capex no tempo 0
    cf = np.concatenate(([-abs(capex)], cash_flow_operational))
    return cf

def npv(cashflows, discount_rate):
    # discount_rate em decimal (0.1 = 10%)
    periods = np.arange(len(cashflows))
    return np.sum(cashflows / ((1 + discount_rate) ** periods))

def irr(cashflows, guess=0.1):
    # numpy.irr deprecated but we can use npf from numpy_financial if installed.
    # fallback: binary search
    try:
        import numpy_financial as nf
        return nf.irr(cashflows)
    except Exception:
        # simple bracket search
        def f(r):
            return npv(cashflows, r)
        low, high = -0.9999, 1.0
        for _ in range(100):
            mid = (low + high) / 2
            val = f(mid)
            if abs(val) < 1e-6:
                return mid
            # choose side by sign
            if f(low) * val < 0:
                high = mid
            else:
                low = mid
        return mid

def payback_year(cashflows):
    cum = np.cumsum(cashflows)
    for i, v in enumerate(cum):
        if v >= 0:
            # linear interpolation within period
            prev = cum[i-1] if i>0 else 0.0
            if cashflows[i] == 0:
                return i
            frac = (0 - prev) / (cum[i] - prev) if (cum[i] - prev)!=0 else 0
            return i -1 + frac
    return None

# ---------------------------
# GUI (tkinter)
# ---------------------------
class PetroChampGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PetroChamp (reimplementação) - Triagem EOR e Viabilidade")
        self.geometry("1000x700")
        self.create_widgets()
        self.df = None
        self.results = None

    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        self.tab_data = ttk.Frame(tabControl)
        self.tab_screen = ttk.Frame(tabControl)
        self.tab_econ = ttk.Frame(tabControl)
        tabControl.add(self.tab_data, text='Dados')
        tabControl.add(self.tab_screen, text='Triagem EOR')
        tabControl.add(self.tab_econ, text='Viabilidade Económica')
        tabControl.pack(expand=1, fill="both")

        # TAB Dados
        frm = ttk.Frame(self.tab_data, padding=10)
        frm.pack(fill='both', expand=True)
        btn_load = ttk.Button(frm, text="Carregar CSV", command=self.load_csv)
        btn_load.grid(row=0, column=0, sticky='w')
        btn_sample = ttk.Button(frm, text="Carregar Exemplo", command=self.load_example)
        btn_sample.grid(row=0, column=1, sticky='w')

        lbl = ttk.Label(frm, text="Ou insira manualmente os valores para um reservatório:")
        lbl.grid(row=1, column=0, columnspan=4, pady=(10,0), sticky='w')

        labels = ["Profundidade (m)","Viscosidade (cP)","API","Salinidade (ppm)",
                  "Litologia","Permeabilidade (mD)","Temperatura (°C)","Saturação (%)"]
        self.entries = {}
        for i, lab in enumerate(labels):
            ttk.Label(frm, text=lab).grid(row=2 + i//4, column=(i%4)*2, sticky='e', padx=2, pady=2)
            ent = ttk.Entry(frm, width=18)
            ent.grid(row=2 + i//4, column=(i%4)*2+1, sticky='w', padx=2, pady=2)
            self.entries[lab] = ent

        btn_add = ttk.Button(frm, text="Adicionar linha manual", command=self.add_manual_row)
        btn_add.grid(row=5, column=0, pady=10, sticky='w')
        btn_show = ttk.Button(frm, text="Mostrar tabela (DataFrame)", command=self.show_dataframe)
        btn_show.grid(row=5, column=1, pady=10, sticky='w')

        # TAB Triagem
        frm2 = ttk.Frame(self.tab_screen, padding=10)
        frm2.pack(fill='both', expand=True)
        btn_run_screen = ttk.Button(frm2, text="Executar triagem EOR", command=self.run_screening)
        btn_run_screen.grid(row=0, column=0, sticky='w')
        btn_export = ttk.Button(frm2, text="Exportar resultados CSV", command=self.export_results)
        btn_export.grid(row=0, column=1, sticky='w')
        self.tree = ttk.Treeview(frm2, columns=("Metodo","Justificativa"), show='headings', height=20)
        self.tree.heading("Metodo", text="Método recomendado")
        self.tree.heading("Justificativa", text="Justificativa (resumo)")
        self.tree.column("Metodo", width=200)
        self.tree.column("Justificativa", width=700)
        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # TAB Económica
        frm3 = ttk.Frame(self.tab_econ, padding=10)
        frm3.pack(fill='both', expand=True)
        # Parâmetros económicos
        labels_e = ["Capex (USD)", "Preço ($/bbl)", "Opex ($/bbl)", "Discount rate (%)", "Período (anos)"]
        self.econ_entries = {}
        for i, lab in enumerate(labels_e):
            ttk.Label(frm3, text=lab).grid(row=i, column=0, sticky='e', padx=2, pady=2)
            ent = ttk.Entry(frm3, width=20)
            ent.grid(row=i, column=1, sticky='w', padx=2, pady=2)
            self.econ_entries[lab] = ent
        ttk.Label(frm3, text="Produção anual estimada (bbl/ano) - lista separada por vírgulas ou 'usar triagem'").grid(row=6, column=0, columnspan=2, sticky='w', pady=(10,0))
        self.prod_text = tk.Text(frm3, height=4, width=60)
        self.prod_text.grid(row=7, column=0, columnspan=3, pady=4, padx=4)
        btn_calc = ttk.Button(frm3, text="Calcular Viabilidade (NPV/IRR/Payback)", command=self.run_econ)
        btn_calc.grid(row=8, column=0, pady=10, sticky='w')
        btn_plot = ttk.Button(frm3, text="Plotar Fluxo Caixa", command=self.plot_cashflow)
        btn_plot.grid(row=8, column=1, pady=10, sticky='w')

        self.result_text = tk.Text(frm3, height=12, width=100)
        self.result_text.grid(row=9, column=0, columnspan=3, pady=6)

    # ---------- callbacks ----------
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:
            return
        try:
            df = pd.read_csv(path)
            # Verificar se tem colunas necessárias (tenta normalizar nomes)
            expected = ["Profundidade","Viscosidade","API","Salinidade","Litologia","Permeabilidade","Temperatura","Saturacao","Saturação"]
            # Tentar mapear colunas com insensibilidade a acentos e case
            df_cols_map = {c:normalize_col(c) for c in df.columns}
            new_cols = {}
            for want in ["Profundidade","Viscosidade","API","Salinidade","Litologia","Permeabilidade","Temperatura","Saturacao"]:
                found = None
                for c,norm in df_cols_map.items():
                    if normalize_col(want) == norm:
                        found = c; break
                if found:
                    new_cols[found] = want
            df = df.rename(columns=new_cols)
            self.df = df
            messagebox.showinfo("OK", f"CSV carregado com {len(df)} linhas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar CSV: {e}")

    def load_example(self):
        # Carregar um DataFrame de exemplo
        data = {
            "Profundidade":[800,1200],
            "Viscosidade":[500,10],
            "API":[15,32],
            "Salinidade":[30000,5000],
            "Litologia":["arenito","arenito"],
            "Permeabilidade":[200,150],
            "Temperatura":[60,90],
            "Saturacao":[60,45]
        }
        self.df = pd.DataFrame(data)
        messagebox.showinfo("OK", "Exemplo carregado (2 linhas).")

    def add_manual_row(self):
        # ler entradas
        field_map = {
            "Profundidade (m)":"Profundidade",
            "Viscosidade (cP)":"Viscosidade",
            "API":"API",
            "Salinidade (ppm)":"Salinidade",
            "Litologia":"Litologia",
            "Permeabilidade (mD)":"Permeabilidade",
            "Temperatura (°C)":"Temperatura",
            "Saturação (%)":"Saturacao"
        }
        row = {}
        for label, key in field_map.items():
            val = self.entries[label].get()
            if val == "":
                row[key] = np.nan
            else:
                # manter litologia como string
                if key == "Litologia":
                    row[key] = val
                else:
                    try:
                        row[key] = float(val)
                    except:
                        row[key] = np.nan
        dfrow = pd.DataFrame([row])
        if self.df is None:
            self.df = dfrow
        else:
            self.df = pd.concat([self.df, dfrow], ignore_index=True)
        messagebox.showinfo("OK", "Linha adicionada manualmente.")

    def show_dataframe(self):
        if self.df is None:
            messagebox.showinfo("Info", "Nenhum dado carregado.")
            return
        # Mostrar num popup como texto
        top = tk.Toplevel(self)
        text = tk.Text(top, width=120, height=30)
        text.pack()
        text.insert("end", self.df.to_string(index=False))
        text.config(state='disabled')

    def run_screening(self):
        if self.df is None:
            messagebox.showwarning("Aviso", "Carregue ou adicione dados primeiro.")
            return
        self.results = []
        for idx, row in self.df.iterrows():
            metodo, justificativas = recomenda_eor_row(row)
            just = "; ".join(justificativas)
            self.results.append({
                "Index": idx,
                "Metodo": metodo,
                "Justificativa": just
            })
        res_df = pd.DataFrame(self.results)
        # popular treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, r in res_df.iterrows():
            self.tree.insert("", "end", values=(r["Metodo"], r["Justificativa"]))
        messagebox.showinfo("OK", f"Triagem concluída para {len(res_df)} reservatórios.")

    def export_results(self):
        if not self.results:
            messagebox.showwarning("Aviso", "Execute a triagem primeiro.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        pd.DataFrame(self.results).to_csv(path, index=False)
        messagebox.showinfo("OK", f"Resultados exportados para {path}")

    def run_econ(self):
        # obter parâmetros económicos
        try:
            capex = float(self.econ_entries["Capex (USD)"].get() or 0.0)
            price = float(self.econ_entries["Preço ($/bbl)"].get() or 0.0)
            opex = float(self.econ_entries["Opex ($/bbl)"].get() or 0.0)
            dr = float(self.econ_entries["Discount rate (%)"].get() or 10.0) / 100.0
        except Exception as e:
            messagebox.showerror("Erro", f"Parâmetros económicos inválidos: {e}")
            return
        prod_text = self.prod_text.get("1.0", "end").strip()
        if not prod_text:
            messagebox.showwarning("Aviso", "Insira perfil de produção (bbl/ano) ou escreva 'usar triagem'.")
            return

        # interpretar produção
        if prod_text.lower().strip() == "usar triagem":
            # estimar produção: pega o primeiro reservatório e gera perfil simples
            if self.df is None:
                messagebox.showerror("Erro", "Nenhum reservatório disponível para estimativa.")
                return
            # suposição simples: produção inicial proporcional à saturação e permeabilidade
            row = self.df.iloc[0]
            sat = try_float(row.get("Saturacao")) or 50
            perm = try_float(row.get("Permeabilidade")) or 100
            # produzir: prod0 (bbl/ano) = sat% * perm * fator arbitrário
            prod0 = sat/100.0 * perm * 1000.0  # escala arbitrária – ajuste conforme caso real
            anos = int(self.econ_entries["Período (anos)"].get() or 10)
            # gerar declínio linear por simplicidade
            prod_profile = [max(prod0*(1 - 0.05*year), 0) for year in range(1, anos+1)]
        else:
            # ler lista de números separados por vírgula
            try:
                vals = [float(x.strip()) for x in prod_text.split(",") if x.strip()!=""]
                prod_profile = vals
            except Exception as e:
                messagebox.showerror("Erro", f"Perfil de produção inválido: {e}")
                return

        cf = calcular_fluxo_caixa(prod_profile, price, opex, capex)
        npv_val = npv(cf, dr)
        irr_val = irr(cf)
        payback = payback_year(cf)

        # salvar resultados e apresentar
        self.econ_result = {
            "npv": npv_val,
            "irr": irr_val,
            "payback": payback,
            "cashflows": cf,
            "production": prod_profile
        }
        txt = f"NPV (discount {dr*100:.2f}%): ${npv_val:,.2f}\n"
        txt += f"IRR: {irr_val:.4f}\n"
        txt += f"Payback (anos): {payback}\n"
        txt += "\nFluxo de caixa por período (t=0 capex negativo):\n"
        for i, v in enumerate(cf):
            txt += f"t={i}: ${v:,.2f}\n"
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", txt)

        messagebox.showinfo("OK", "Cálculo económico concluído.")

    def plot_cashflow(self):
        if not hasattr(self, "econ_result"):
            messagebox.showwarning("Aviso", "Execute o cálculo económico primeiro.")
            return
        cf = self.econ_result["cashflows"]
        prod = self.econ_result["production"]
        years = np.arange(len(cf))
        fig, ax = plt.subplots(2,1, figsize=(8,6), sharex=True)
        ax[0].bar(years, cf)
        ax[0].set_title("Fluxo de Caixa (USD)")
        ax[0].set_ylabel("USD")
        ax[1].plot(np.arange(1, len(prod)+1), prod, marker='o')
        ax[1].set_title("Produção anual (bbl/ano)")
        ax[1].set_xlabel("Ano")
        ax[1].set_ylabel("bbl/ano")
        plt.tight_layout()
        plt.show()

# ---------------------------
# Helpers
# ---------------------------
def normalize_col(s):
    return ''.join(ch for ch in s.lower() if ch.isalnum())

# ---------------------------
# Main
# ---------------------------
def main():
    app = PetroChampGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
