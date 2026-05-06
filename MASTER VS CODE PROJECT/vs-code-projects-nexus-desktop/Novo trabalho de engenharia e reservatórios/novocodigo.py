#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script PetroChamp EOR:

Este script integra funcionalidades de cálculo de OOIP, simulação de produção com declínio exponencial,
avaliação de viabilidade técnica de métodos EOR (Enhanced Oil Recovery), cálculo de fluxo de caixa,
NPV, IRR e payback, exibição de gráficos e exportação de resultados para Excel e PDF.

Instruções de Uso:
 - Preencha os campos da interface gráfica com os parâmetros do reservatório, do fluido e econômicos.
 - Ou carregue um arquivo CSV com valores das variáveis de entrada (colunas: Area, Espessura, Porosidade, Swi, Bo, 
   Pressao, API, Qi, Decline, AnosSim, Preco, OPEX, CAPEX, Royalties, Desconto).
 - Clique em 'Executar' para gerar os cálculos.
 - O script exibirá os resultados e gráficos de produção e fluxo de caixa.
 - Resultados serão exportados para 'resultados.xlsx' (Excel) e 'relatorio.pdf'.

Bibliotecas necessárias: pandas, numpy, matplotlib, tkinter, numpy_financial.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import numpy_financial as nf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Função para calcular OOIP
def calcular_ooip(area, espessura, porosidade, swi, bo):
    # OOIP (Original Oil in Place) em barris
    # Formula empírica: OOIP = 7758 * Area(acres) * H(ft) * porosidade * (1 - Swi) / Bo
    OOIP = 7758.0 * area * espessura * porosidade * (1 - swi) / bo
    return OOIP

# Função para avaliar viabilidade técnica de métodos EOR
def avaliar_eor(pressao, api, viscosidade=0, salinidade=0):
    """
    Avalia quais métodos EOR são aplicáveis com base em critérios simplificados:
    - Injeção CO2: pressão suficientemente alta e óleo leve (API >= 35).
    - Injeção HC (gás hidrocarboneto): API >= 35.
    - WAG: aplicável se injeção gasosa possível (não miscível) e corte de água moderado.
    - Injeção N2: se pressão muito alta (>= 2500 psi).
    - Polímeros: se API < 30.
    - Surfactante/ASP: se 25 <= API < 35.
    - Combustão in-situ (ISC): se API < 20.
    - Vapor: se API < 20 (óleo muito pesado).
    """
    viabilities = {}
    # Critério para injeção de CO2 (miscível)
    if pressao >= 1500 and api >= 35:
        viabilities['CO2'] = True
    else:
        viabilities['CO2'] = False
    # Critério para injeção de hidrocarbonetos (gás miscível)
    if pressao >= 1500 and api >= 35:
        viabilities['HC'] = True
    else:
        viabilities['HC'] = False
    # Critério para injeção WAG (se gas injetável e corte de água > 0.2)
    # Simplificação: considera não aplicável se gas injection é miscível
    if viabilities['CO2'] or viabilities['HC']:
        viabilities['WAG'] = False
    else:
        viabilities['WAG'] = False
    # Critério para injeção de N2 (pressão muito alta)
    if pressao >= 2500:
        viabilities['N2'] = True
    else:
        viabilities['N2'] = False
    # Critério para polímeros
    if api < 30:
        viabilities['Polimeros'] = True
    else:
        viabilities['Polimeros'] = False
    # Critério para surfactante/ASP
    if 25 <= api < 35:
        viabilities['ASP_Surfactante'] = True
    else:
        viabilities['ASP_Surfactante'] = False
    # Critério para combustão in-situ (ISC)
    if api < 20:
        viabilities['ISC'] = True
    else:
        viabilities['ISC'] = False
    # Critério para injeção de vapor (vapor superaquecido)
    if api < 20:
        viabilities['Vapor'] = True
    else:
        viabilities['Vapor'] = False
    return viabilities

# Função para seleção do método EOR mais adequado (com base em regras simplificadas)
def selecionar_melhor_eor(viabilities):
    # Prioridade: CO2, HC, Polímeros, ASP/Surf, N2, WAG, ISC, Vapor
    if viabilities.get('CO2'):
        return "Injeção de CO2"
    if viabilities.get('HC'):
        return "Injeção de Hidrocarbonetos"
    if viabilities.get('Polimeros'):
        return "Injeção de Polímeros"
    if viabilities.get('ASP_Surfactante'):
        return "Injeção de Surfactantes/Alcalino"
    if viabilities.get('N2'):
        return "Injeção de N2"
    if viabilities.get('WAG'):
        return "WAG (Water Alternating Gas)"
    if viabilities.get('ISC'):
        return "Combustão In-Situ"
    if viabilities.get('Vapor'):
        return "Injeção de Vapor"
    return "Nenhum método aplicável"

# Função para simulação de produção com declínio exponencial
def simular_producao(Qi, D, anos):
    # Qi: vazão inicial (bbl/ano)
    # D: taxa de declínio exponencial (/ano)
    # retorna lista de produção anual (bbl)
    tempos = np.arange(1, anos+1)
    Q = Qi * np.exp(-D * (tempos - 1))
    return Q

# Função para cálculo de fluxo de caixa, NPV, IRR, Payback
def calcular_financas(Q, preco, opex, capex, royalties, taxa_desc):
    n = len(Q)
    cashflow = np.zeros(n+1)
    # Período 0: investimento inicial (CAPEX negativo)
    cashflow[0] = -capex
    # Fluxo de caixa de produção anual
    for t in range(1, n+1):
        receita = Q[t-1] * preco * (1 - royalties)
        cashflow[t] = receita - opex
    # Calcular DCF (fluxo descontado) e NPV acumulado
    dcf = np.zeros(n+1)
    npv_acum = np.zeros(n+1)
    for t in range(0, n+1):
        dcf[t] = cashflow[t] / ((1 + taxa_desc) ** t)
        npv_acum[t] = dcf[:t+1].sum()
    # NPV total (valor presente líquido)
    npv_total = npv_acum[-1]
    # IRR (Taxa Interna de Retorno)
    try:
        irr = nf.irr(cashflow)
    except:
        irr = None
    # Payback (tempo para recuperar o CAPEX)
    cumul = np.cumsum(cashflow)
    payback = None
    for t in range(1, len(cumul)):
        if cumul[t] >= 0 and cumul[t-1] < 0:
            # Interpolação linear entre t-1 e t para payback
            frac = -cumul[t-1] / (cumul[t] - cumul[t-1])
            payback = (t-1) + frac
            break
    return cashflow, dcf, npv_acum, npv_total, irr, payback

# Função para exportar resultados para Excel e PDF
def exportar_resultados(params, OOIP, viabilities, best_eor, production, cumul, cashflow, dcf, npv_acum, npv_total, irr, payback):
    # Exportar para Excel
    df_out = pd.DataFrame({
        'Período': list(range(0, len(cashflow))),
        'Fluxo de Caixa (USD)': cashflow,
        'DCF (USD)': dcf,
        'NPV Acumulado (USD)': npv_acum
    })
    df_out.to_excel('resultados.xlsx', index=False)
    # Criar relatório PDF
    with PdfPages('relatorio.pdf') as pdf:
        # Página de resultados textuais
        fig = plt.figure(figsize=(8.27, 11.69))  # A4 vertical
        fig.clf()
        text = []
        text.append("Resumo de Resultados")
        text.append("-------------------")
        text.append(f"OOIP Estimado: {OOIP:,.0f} bbl")
        text.append("Viabilidade EOR:")
        for method, ok in viabilities.items():
            status = "Aplicável" if ok else "Não aplicável"
            text.append(f" - {method}: {status}")
        text.append(f"Método EOR Selecionado: {best_eor}")
        text.append(f"NPV Total: {npv_total:,.2f} USD")
        text.append(f"IRR: {irr*100:.2f}%" if irr is not None else "IRR: N/A")
        if payback is not None:
            text.append(f"Payback: {payback:.2f} anos")
        else:
            text.append("Payback: N/A")
        # Exibir texto no PDF
        plt.text(0.05, 0.95, "\n".join(text), fontsize=10, va='top')
        plt.axis('off')
        pdf.savefig(fig)
        plt.close(fig)
        # Página de gráficos
        fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.27, 11.69))
        anos = np.arange(0, len(cashflow))
        # Gráfico 1: Fluxo de Caixa e DCF
        ax1.plot(anos, cashflow, marker='o', label='Fluxo de Caixa (USD)')
        ax1.plot(anos, dcf, marker='s', label='DCF (USD)')
        ax1.set_xlabel('Período')
        ax1.set_title('Fluxo de Caixa e DCF ao longo do tempo')
        ax1.legend()
        # Gráfico 2: NPV acumulado
        ax2.plot(anos, npv_acum, marker='o', color='green')
        ax2.set_xlabel('Período')
        ax2.set_title('NPV Acumulado (USD)')
        ax2.axhline(0, color='gray', linewidth=0.7, linestyle='--')
        pdf.savefig(fig2)
        plt.close(fig2)

# Função executada ao clicar em 'Executar'
def executar():
    try:
        # Ler parâmetros do formulário
        area = float(entry_area.get())
        espessura = float(entry_espessura.get())
        porosidade = float(entry_por.get()) / 100.0
        swi = float(entry_swi.get()) / 100.0
        bo = float(entry_bo.get())
        pressao = float(entry_pressao.get())
        api = float(entry_api.get())
        Qi = float(entry_Qi.get())
        D = float(entry_decline.get())
        anos = int(entry_anos.get())
        preco = float(entry_preco.get())
        opex = float(entry_opex.get())
        capex = float(entry_capex.get())
        royalties = float(entry_roy.get()) / 100.0
        taxa_desc = float(entry_taxa.get()) / 100.0
        # Calcular OOIP
        OOIP = calcular_ooip(area, espessura, porosidade, swi, bo)
        # Avaliar EOR
        viab = avaliar_eor(pressao, api)
        melhor = selecionar_melhor_eor(viab)
        # Simular produção
        producao = simular_producao(Qi, D, anos)
        cumul = np.cumsum(producao)
        # Calcular finanças
        cashflow, dcf, npv_acum, npv_total, irr, payback = calcular_financas(
            producao, preco, opex, capex, royalties, taxa_desc)
        # Exportar resultados
        exportar_resultados(
            {}, OOIP, viab, melhor, producao, cumul,
            cashflow, dcf, npv_acum, npv_total, irr, payback)
        # Exibir mensagem de conclusão
        messagebox.showinfo("Conclusão", 
            "Cálculos concluídos. Resultados exportados para 'resultados.xlsx' e 'relatorio.pdf'.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para carregar CSV de entrada
def carregar_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)
        # Atribuir valores às entradas se colunas existirem
        if 'Area' in df.columns:
            entry_area.delete(0, tk.END); entry_area.insert(0, df.at[0, 'Area'])
        if 'Espessura' in df.columns:
            entry_espessura.delete(0, tk.END); entry_espessura.insert(0, df.at[0, 'Espessura'])
        if 'Porosidade' in df.columns:
            entry_por.delete(0, tk.END); entry_por.insert(0, df.at[0, 'Porosidade'])
        if 'Swi' in df.columns:
            entry_swi.delete(0, tk.END); entry_swi.insert(0, df.at[0, 'Swi'])
        if 'Bo' in df.columns:
            entry_bo.delete(0, tk.END); entry_bo.insert(0, df.at[0, 'Bo'])
        if 'Pressao' in df.columns:
            entry_pressao.delete(0, tk.END); entry_pressao.insert(0, df.at[0, 'Pressao'])
        if 'API' in df.columns:
            entry_api.delete(0, tk.END); entry_api.insert(0, df.at[0, 'API'])
        if 'Qi' in df.columns:
            entry_Qi.delete(0, tk.END); entry_Qi.insert(0, df.at[0, 'Qi'])
        if 'Decline' in df.columns:
            entry_decline.delete(0, tk.END); entry_decline.insert(0, df.at[0, 'Decline'])
        if 'AnosSim' in df.columns:
            entry_anos.delete(0, tk.END); entry_anos.insert(0, df.at[0, 'AnosSim'])
        if 'Preco' in df.columns:
            entry_preco.delete(0, tk.END); entry_preco.insert(0, df.at[0, 'Preco'])
        if 'OPEX' in df.columns:
            entry_opex.delete(0, tk.END); entry_opex.insert(0, df.at[0, 'OPEX'])
        if 'CAPEX' in df.columns:
            entry_capex.delete(0, tk.END); entry_capex.insert(0, df.at[0, 'CAPEX'])
        if 'Royalties' in df.columns:
            entry_roy.delete(0, tk.END); entry_roy.insert(0, df.at[0, 'Royalties'])
        if 'Desconto' in df.columns:
            entry_taxa.delete(0, tk.END); entry_taxa.insert(0, df.at[0, 'Desconto'])
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar CSV: {e}")

# Configurar interface gráfica com Tkinter
root = tk.Tk()
root.title("Ferramenta PetroChamp EOR")
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Parâmetros do reservatório
tk.Label(frame, text="Área (acres):").grid(row=0, column=0, sticky="e")
entry_area = tk.Entry(frame); entry_area.grid(row=0, column=1)
tk.Label(frame, text="Espessura (pés):").grid(row=1, column=0, sticky="e")
entry_espessura = tk.Entry(frame); entry_espessura.grid(row=1, column=1)
tk.Label(frame, text="Porosidade (%):").grid(row=2, column=0, sticky="e")
entry_por = tk.Entry(frame); entry_por.grid(row=2, column=1)
tk.Label(frame, text="Swi (%):").grid(row=3, column=0, sticky="e")
entry_swi = tk.Entry(frame); entry_swi.grid(row=3, column=1)
tk.Label(frame, text="Boi (RB/STB):").grid(row=4, column=0, sticky="e")
entry_bo = tk.Entry(frame); entry_bo.grid(row=4, column=1)

# Parâmetros do fluido/reservatório
tk.Label(frame, text="Pressão (psi):").grid(row=0, column=2, sticky="e")
entry_pressao = tk.Entry(frame); entry_pressao.grid(row=0, column=3)
tk.Label(frame, text="API do óleo:").grid(row=1, column=2, sticky="e")
entry_api = tk.Entry(frame); entry_api.grid(row=1, column=3)

# Parâmetros de produção
tk.Label(frame, text="Produção inicial Qi (bbl/ano):").grid(row=5, column=0, sticky="e")
entry_Qi = tk.Entry(frame); entry_Qi.grid(row=5, column=1)
tk.Label(frame, text="Declínio (anual):").grid(row=6, column=0, sticky="e")
entry_decline = tk.Entry(frame); entry_decline.grid(row=6, column=1)
tk.Label(frame, text="Tempo de simulação (anos):").grid(row=7, column=0, sticky="e")
entry_anos = tk.Entry(frame); entry_anos.grid(row=7, column=1)

# Parâmetros econômicos
tk.Label(frame, text="Preço do óleo (USD/bbl):").grid(row=5, column=2, sticky="e")
entry_preco = tk.Entry(frame); entry_preco.grid(row=5, column=3)
tk.Label(frame, text="OPEX (USD/ano):").grid(row=6, column=2, sticky="e")
entry_opex = tk.Entry(frame); entry_opex.grid(row=6, column=3)
tk.Label(frame, text="CAPEX (USD):").grid(row=7, column=2, sticky="e")
entry_capex = tk.Entry(frame); entry_capex.grid(row=7, column=3)
tk.Label(frame, text="Royalties (%):").grid(row=8, column=2, sticky="e")
entry_roy = tk.Entry(frame); entry_roy.grid(row=8, column=3)
tk.Label(frame, text="Taxa de desconto (%):").grid(row=9, column=2, sticky="e")
entry_taxa = tk.Entry(frame); entry_taxa.grid(row=9, column=3)

# Botões
btn_load = tk.Button(frame, text="Carregar CSV", command=carregar_csv)
btn_load.grid(row=10, column=0, pady=10)
btn_run = tk.Button(frame, text="Executar", command=executar)
btn_run.grid(row=10, column=1, pady=10)

root.mainloop()
