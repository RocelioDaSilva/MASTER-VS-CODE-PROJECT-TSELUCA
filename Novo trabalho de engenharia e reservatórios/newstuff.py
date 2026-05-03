# ==========================================================
# SISTEMA DE SELEÇÃO DE RESERVATÓRIOS PARA EOR (CUSTOMTKINTER)
# Autor: ChatGPT
# Descrição:
# Aplicação completa para triagem técnica e econômica de
# métodos de Enhanced Oil Recovery (EOR) usando critérios
# consagrados na literatura (Taber et al., Al-Adasani & Bai).
# Interface moderna com CustomTkinter.
# ==========================================================

# -------------------- DEPENDÊNCIAS -------------------------
# pip install customtkinter pandas numpy matplotlib numpy-financial openpyxl

import customtkinter as ctk
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox

# -------------------- CONFIGURAÇÃO UI ----------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -------------------- FUNÇÕES TÉCNICAS ---------------------

def calcular_ooip(area, h, poro, swi, bo):
    return 7758 * area * h * poro * (1 - swi) / bo


def triagem_eor(api, visc, depth, temp, poro, perm):
    metodos = {}

    metodos['CO2 Miscível'] = api >= 30 and depth > 2500
    metodos['Gás HC'] = api >= 35 and depth > 3000
    metodos['Polímeros'] = api < 30 and visc < 150
    metodos['Surfactante/ASP'] = 25 <= api <= 35 and perm > 100
    metodos['Vapor'] = api < 20 and depth < 3000
    metodos['Combustão In-Situ'] = api < 15

    return metodos


def melhor_metodo(metodos):
    for m, ok in metodos.items():
        if ok:
            return m
    return "Nenhum método tecnicamente viável"


def simular_producao(qi, decline, anos):
    t = np.arange(anos)
    return qi * np.exp(-decline * t)


def avaliar_economia(prod, preco, opex, capex, taxa):
    fluxo = [-capex]
    for q in prod:
        fluxo.append(q * preco - opex)

    npv = npf.npv(taxa, fluxo)
    irr = npf.irr(fluxo)

    acumulado = np.cumsum(fluxo)
    payback = next((i for i, v in enumerate(acumulado) if v > 0), None)

    return fluxo, npv, irr, payback

# -------------------- APLICAÇÃO -----------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EOR Selector – Engenharia de Reservatórios")
        self.geometry("1200x720")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_input = self.tabs.add("Dados do Reservatório")
        self.tab_eor = self.tabs.add("Triagem EOR")
        self.tab_eco = self.tabs.add("Análise Econômica")
        self.tab_plot = self.tabs.add("Gráficos")

        self.create_inputs()
        self.create_eor()
        self.create_eco()
        self.create_plot()

    # -------------------- ABA 1 -----------------------------
    def create_inputs(self):
        self.entries = {}
        campos = [
            ("Área (acres)", 1000),
            ("Espessura (ft)", 50),
            ("Porosidade (%)", 20),
            ("Swi (%)", 25),
            ("Bo", 1.2),
            ("API", 32),
            ("Viscosidade (cP)", 10),
            ("Profundidade (ft)", 6000),
            ("Temperatura (°C)", 80),
            ("Permeabilidade (mD)", 300)
        ]

        for i, (label, default) in enumerate(campos):
            ctk.CTkLabel(self.tab_input, text=label).grid(row=i, column=0, pady=5, padx=10, sticky="w")
            e = ctk.CTkEntry(self.tab_input)
            e.insert(0, default)
            e.grid(row=i, column=1, pady=5)
            self.entries[label] = e

        ctk.CTkButton(self.tab_input, text="Calcular OOIP", command=self.calc_ooip).grid(row=11, column=0, pady=20)
        self.ooip_label = ctk.CTkLabel(self.tab_input, text="OOIP: -")
        self.ooip_label.grid(row=11, column=1)

    def calc_ooip(self):
        v = lambda k: float(self.entries[k].get())
        ooip = calcular_ooip(v("Área (acres)"), v("Espessura (ft)"), v("Porosidade (%)")/100,
                             v("Swi (%)")/100, v("Bo"))
        self.ooip_label.configure(text=f"OOIP ≈ {ooip:,.0f} STB")

    # -------------------- ABA 2 -----------------------------
    def create_eor(self):
        self.result_eor = ctk.CTkTextbox(self.tab_eor, width=600, height=400)
        self.result_eor.pack(pady=20)

        ctk.CTkButton(self.tab_eor, text="Executar Triagem EOR", command=self.run_eor).pack()

    def run_eor(self):
        v = lambda k: float(self.entries[k].get())
        met = triagem_eor(v("API"), v("Viscosidade (cP)"), v("Profundidade (ft)"),
                          v("Temperatura (°C)"), v("Porosidade (%)")/100, v("Permeabilidade (mD)"))
        texto = "RESULTADOS DA TRIAGEM EOR\n\n"
        for m, ok in met.items():
            texto += f"{m}: {'APLICÁVEL' if ok else 'NÃO APLICÁVEL'}\n"
        texto += f"\nMétodo Recomendado: {melhor_metodo(met)}"
        self.result_eor.delete("1.0", "end")
        self.result_eor.insert("end", texto)

    # -------------------- ABA 3 -----------------------------
    def create_eco(self):
        self.qi = ctk.CTkEntry(self.tab_eco)
        self.qi.insert(0, 5000)
        self.qi.pack(pady=5)
        self.decline = ctk.CTkEntry(self.tab_eco)
        self.decline.insert(0, 0.12)
        self.decline.pack(pady=5)
        self.anos = ctk.CTkEntry(self.tab_eco)
        self.anos.insert(0, 10)
        self.anos.pack(pady=5)
        self.preco = ctk.CTkEntry(self.tab_eco)
        self.preco.insert(0, 70)
        self.preco.pack(pady=5)
        self.opex = ctk.CTkEntry(self.tab_eco)
        self.opex.insert(0, 200000)
        self.opex.pack(pady=5)
        self.capex = ctk.CTkEntry(self.tab_eco)
        self.capex.insert(0, 5000000)
        self.capex.pack(pady=5)
        self.taxa = ctk.CTkEntry(self.tab_eco)
        self.taxa.insert(0, 0.1)
        self.taxa.pack(pady=5)

        ctk.CTkButton(self.tab_eco, text="Calcular Economia", command=self.calc_eco).pack(pady=10)
        self.eco_label = ctk.CTkLabel(self.tab_eco, text="")
        self.eco_label.pack()

    def calc_eco(self):
        prod = simular_producao(float(self.qi.get()), float(self.decline.get()), int(self.anos.get()))
        fluxo, npv, irr, payback = avaliar_economia(prod, float(self.preco.get()),
                                                    float(self.opex.get()), float(self.capex.get()),
                                                    float(self.taxa.get()))
        self.eco_label.configure(text=f"NPV = {npv:,.2f} USD | IRR = {irr:.2%} | Payback = {payback} anos")
        self.prod = prod
        self.fluxo = fluxo

    # -------------------- ABA 4 -----------------------------
    def create_plot(self):
        ctk.CTkButton(self.tab_plot, text="Mostrar Gráficos", command=self.plotar).pack(pady=20)

    def plotar(self):
        plt.figure(figsize=(10,4))
        plt.subplot(1,2,1)
        plt.plot(self.prod)
        plt.title("Produção")
        plt.subplot(1,2,2)
        plt.plot(np.cumsum(self.fluxo))
        plt.title("Fluxo de Caixa Acumulado")
        plt.show()


# -------------------- EXECUÇÃO ------------------------------
if __name__ == '__main__':
    app = App()
    app.mainloop()
