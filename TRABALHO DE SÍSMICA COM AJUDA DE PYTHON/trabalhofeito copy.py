# -*- coding: utf-8 -*-
"""
Script: NMO + Dix + Excel-formulas + Gráficos + Relatório PDF
- Lê o Excel de entrada, insere fórmulas no Excel (folha "Calculos"),
    gera gráficos (PNGs) e compila um PDF com os gráficos + tabela de resultados.

Comportamento de entradas/saídas
- O ficheiro de entrada Excel é procurado por nome em `INPUT_PATH` dentro da
    mesma pasta deste script.
- Por predefinição os ficheiros de saída (XLSX, PDF, PNGs) são colocados numa
    subpasta chamada `output_nmo` dentro da pasta onde este script está. Para
    alterar a pasta de saída, mude `OUTPUT_DIR` abaixo para um caminho absoluto
    ou para outra subpasta (ex: "results" ou BASE_DIR / "meus_outputs").
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from xlsxwriter.utility import xl_rowcol_to_cell
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# -----------------------------
# CONFIGURAÇÃO - editar conforme necessário
# -----------------------------
# Entrada (nome do ficheiro Excel esperado na mesma pasta que este script)
INPUT_PATH = "Exercício de Análise de Velocidade e Correção NMO (Rocélio Da Silva-20220001)(deepseek) (4).xlsx"
# Saída: por defeito gravamos os outputs na subpasta 'output_nmo' da pasta do
# script. Para usar outra pasta, colocar um caminho (absoluto ou relativo).
OUTPUT_DIR = "output_nmo"
OUTPUT_BASENAME = "NMO_Analise"   # base name for outputs
SHEET_TO_READ = 0
# -----------------------------

# garantir paths relativos à pasta do script (esta pasta)
BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / INPUT_PATH
if not input_file.exists():
    raise FileNotFoundError(f"Ficheiro de entrada não encontrado: {input_file.resolve()}")

# decidir pasta de saída: se OUTPUT_DIR for None usamos a pasta do script
if OUTPUT_DIR is None:
    OUTPUT_DIR = BASE_DIR
else:
    OUTPUT_DIR = Path(OUTPUT_DIR)
    # se foi fornecido um caminho relativo, torná-lo relativo à pasta do script
    if not OUTPUT_DIR.is_absolute():
        OUTPUT_DIR = BASE_DIR / OUTPUT_DIR

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_excel = Path(OUTPUT_DIR) / f"{input_file.stem}_{OUTPUT_BASENAME}.xlsx"
output_pdf = Path(OUTPUT_DIR) / f"{input_file.stem}_{OUTPUT_BASENAME}.pdf"

# -----------------------------
# Ler dados e localizar colunas
# -----------------------------
df = pd.read_excel(input_file, sheet_name=SHEET_TO_READ)
df.columns = [str(c).strip() for c in df.columns]

expected_names = {
    "offset": ["distância (m)", "distancia (m)", "distância", "distancia", "offset", "distance (m)"],
    "r1": ["reflexão 1 (ms)", "reflexao 1 (ms)", "reflexão 1", "reflexao 1", "ref1"],
    "r2": ["reflexão 2 (ms)", "reflexao 2 (ms)", "reflexão 2", "reflexao 2", "ref2"],
    "r3": ["reflexão 3 (ms)", "reflexao 3 (ms)", "reflexão 3", "reflexao 3", "ref3"],
    "r4": ["reflexão 4 (ms)", "reflexao 4 (ms)", "reflexão 4", "reflexao 4", "ref4"],
    "r5": ["reflexão 5 (ms)", "reflexao 5 (ms)", "reflexão 5", "reflexao 5", "ref5"],
}

def find_column(possible_names, columns):
    for nm in possible_names:
        for c in columns:
            if c.lower() == nm.lower():
                return c
    # substring fallback
    for nm in possible_names:
        key = nm.split()[0].lower()
        for c in columns:
            if key in c.lower():
                return c
    return None

cols = df.columns.tolist()
col_offset_name = find_column(expected_names["offset"], cols)
col_r1_name = find_column(expected_names["r1"], cols)
col_r2_name = find_column(expected_names["r2"], cols)
col_r3_name = find_column(expected_names["r3"], cols)
col_r4_name = find_column(expected_names["r4"], cols)
col_r5_name = find_column(expected_names["r5"], cols)

if any(c is None for c in [col_offset_name, col_r1_name, col_r2_name, col_r3_name, col_r4_name, col_r5_name]):
    raise ValueError("Não foi possível localizar todas as colunas necessárias. "
                     f"Encontrados: offset={col_offset_name}, r1={col_r1_name}, r2={col_r2_name}, r3={col_r3_name}, r4={col_r4_name}, r5={col_r5_name}")

df_work = df[[col_offset_name, col_r1_name, col_r2_name, col_r3_name, col_r4_name, col_r5_name]].copy()
df_work.columns = ["offset_m", "t_r1_ms", "t_r2_ms", "t_r3_ms", "t_r4_ms", "t_r5_ms"]
df_work = df_work.dropna(subset=["offset_m"]).reset_index(drop=True)
nrows = len(df_work)

# -----------------------------
# Preparar posições no Excel
# -----------------------------
data_start_row = 1  # pandas wrote header in row 0; data begins at Excel row 2 (0-based index 1)
data_end_row = data_start_row + nrows - 1

# original columns indexes (0-based)
col_offset = 0
col_r1 = 1
col_r2 = 2
col_r3 = 3
col_r4 = 4
col_r5 = 5
last_orig_col = col_r5

# auxiliares
col_x2 = last_orig_col + 1
col_t1sq = last_orig_col + 2
col_t2sq = last_orig_col + 3
col_t3sq = last_orig_col + 4
col_t4sq = last_orig_col + 5
col_t5sq = last_orig_col + 6

col_t1_nmo = col_t5sq + 1
col_t2_nmo = col_t1_nmo + 1
col_t3_nmo = col_t1_nmo + 2
col_t4_nmo = col_t1_nmo + 3
col_t5_nmo = col_t1_nmo + 4

summary_col0 = col_t5_nmo + 2
summary_header_row = data_end_row + 2

# summary rows
row_t0_s = summary_header_row + 1
row_t0_ms = summary_header_row + 2
row_vnmo = summary_header_row + 3
row_vint = summary_header_row + 4
row_depth = summary_header_row + 5
row_thick = summary_header_row + 6

# -----------------------------
# Escrever Excel com fórmulas (xlsxwriter)
# -----------------------------
with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Dados_originais", index=False)
    df_work.to_excel(writer, sheet_name="Calculos", index=False, startrow=0, startcol=0)
    workbook = writer.book
    ws = writer.sheets["Calculos"]

    # cabeçalhos auxiliares
    ws.write(0, col_x2, "x^2 (m^2)")
    ws.write(0, col_t1sq, "t1^2 (s^2)")
    ws.write(0, col_t2sq, "t2^2 (s^2)")
    ws.write(0, col_t3sq, "t3^2 (s^2)")
    ws.write(0, col_t4sq, "t4^2 (s^2)")
    ws.write(0, col_t5sq, "t5^2 (s^2)")

    # inserir fórmulas x^2 e t^2 (t em segundos => (t_ms/1000)^2)
    for i in range(nrows):
        row = data_start_row + i
        offset_cell = xl_rowcol_to_cell(row, col_offset)
        t1_cell = xl_rowcol_to_cell(row, col_r1)
        t2_cell = xl_rowcol_to_cell(row, col_r2)
        t3_cell = xl_rowcol_to_cell(row, col_r3)
        t4_cell = xl_rowcol_to_cell(row, col_r4)
        t5_cell = xl_rowcol_to_cell(row, col_r5)

        ws.write_formula(row, col_x2, f"={offset_cell}^2")
        ws.write_formula(row, col_t1sq, f"=({t1_cell}/1000)^2")
        ws.write_formula(row, col_t2sq, f"=({t2_cell}/1000)^2")
        ws.write_formula(row, col_t3sq, f"=({t3_cell}/1000)^2")
        ws.write_formula(row, col_t4sq, f"=({t4_cell}/1000)^2")
        ws.write_formula(row, col_t5sq, f"=({t5_cell}/1000)^2")

    # summary headers (Ref 1..5)
    for i_ref in range(1, 6):
        ws.write(summary_header_row, summary_col0 + i_ref, f"Ref {i_ref}")

    # helper ranges
    def rng(col_idx):
        return f"{xl_rowcol_to_cell(data_start_row, col_idx)}:{xl_rowcol_to_cell(data_end_row, col_idx)}"

    rng_x2 = rng(col_x2)
    rng_tsq_list = [rng(col_t1sq), rng(col_t2sq), rng(col_t3sq), rng(col_t4sq), rng(col_t5sq)]

    # inserir fórmulas t0 (s), t0 (ms), Vnmo (m/s)
    ws.write(row_t0_s, summary_col0, "t0 (s)")
    ws.write(row_t0_ms, summary_col0, "t0 (ms)")
    ws.write(row_vnmo, summary_col0, "Vnmo (m/s)")
    ws.write(row_vint, summary_col0, "Vint (m/s) [Dix]")
    ws.write(row_depth, summary_col0, "Depth (m)")
    ws.write(row_thick, summary_col0, "Thickness (m)")

    for idx, t_range in enumerate(rng_tsq_list, start=1):
        col_summary = summary_col0 + idx
        # t0_s = SQRT(INTERCEPT(t^2_range, x^2_range))
        ws.write_formula(row_t0_s, col_summary, f"=IFERROR(SQRT(INTERCEPT({t_range}, {rng_x2})), NA())")
        # t0_ms = t0_s * 1000
        t0s_cell = xl_rowcol_to_cell(row_t0_s, col_summary)
        ws.write_formula(row_t0_ms, col_summary, f"=IF(ISNA({t0s_cell}),NA(),{t0s_cell}*1000)")
        # v_nmo = SQRT(1/SLOPE(t^2_range, x^2_range))
        ws.write_formula(row_vnmo, col_summary, f"=IFERROR(SQRT(1/SLOPE({t_range}, {rng_x2})), NA())")

    # Vint via Dix: Vint1 = Vnmo1, Vint_i formula para i>=2
    ws.write_formula(row_vint, summary_col0 + 1, xl_rowcol_to_cell(row_vnmo, summary_col0 + 1))  # Vint1 = Vnmo1
    for i in range(2, 6):
        col_i = summary_col0 + i
        vnmo_i = xl_rowcol_to_cell(row_vnmo, col_i)
        vnmo_prev = xl_rowcol_to_cell(row_vnmo, col_i - 1)
        t0_i = xl_rowcol_to_cell(row_t0_s, col_i)
        t0_prev = xl_rowcol_to_cell(row_t0_s, col_i - 1)
        dix_formula = (f"=IFERROR(SQRT((( {vnmo_i}^2 * {t0_i}) - ({vnmo_prev}^2 * {t0_prev})) / "
                       f"({t0_i} - {t0_prev})), NA())")
        ws.write_formula(row_vint, col_i, dix_formula)

    # profundidades e espessuras
    # depth1 = v_int1 * (t0_1 / 2)
    v_int1 = xl_rowcol_to_cell(row_vint, summary_col0 + 1)
    t0_1 = xl_rowcol_to_cell(row_t0_s, summary_col0 + 1)
    ws.write_formula(row_depth, summary_col0 + 1, f"=IF(OR(ISNA({v_int1}),ISNA({t0_1})),NA(),{v_int1}*({t0_1}/2))")
    ws.write_formula(row_thick, summary_col0 + 1, xl_rowcol_to_cell(row_depth, summary_col0 + 1))  # thickness1 = depth1

    for i in range(2, 6):
        col_i = summary_col0 + i
        v_int_i = xl_rowcol_to_cell(row_vint, col_i)
        t0_i = xl_rowcol_to_cell(row_t0_s, col_i)
        t0_prev = xl_rowcol_to_cell(row_t0_s, col_i - 1)
        prev_depth = xl_rowcol_to_cell(row_depth, col_i - 1)
        # thickness
        thickness_formula = (f"=IF(OR(ISNA({v_int_i}),ISNA({t0_i}),ISNA({t0_prev})),NA(),"
                             f"{v_int_i}*(({t0_i} - {t0_prev})/2))")
        ws.write_formula(row_thick, col_i, thickness_formula)
        # depth = prev_depth + thickness_col
        ws.write_formula(row_depth, col_i, f"=IF(ISNA({xl_rowcol_to_cell(row_thick,col_i)}),NA(),{prev_depth} + {xl_rowcol_to_cell(row_thick,col_i)})")

    # tempos NMO-corrigidos (em ms) por receptor: t_corr_ms = IF( (t_ms/1000)^2 - x^2/v^2 <=0, 0, sqrt(...)*1000 )
    for i in range(nrows):
        row = data_start_row + i
        t1_cell = xl_rowcol_to_cell(row, col_r1)
        t2_cell = xl_rowcol_to_cell(row, col_r2)
        t3_cell = xl_rowcol_to_cell(row, col_r3)
        t4_cell = xl_rowcol_to_cell(row, col_r4)
        t5_cell = xl_rowcol_to_cell(row, col_r5)
        x_cell = xl_rowcol_to_cell(row, col_offset)

        v1_abs = xl_rowcol_to_cell(row_vnmo, summary_col0 + 1, row_abs=True, col_abs=True)
        v2_abs = xl_rowcol_to_cell(row_vnmo, summary_col0 + 2, row_abs=True, col_abs=True)
        v3_abs = xl_rowcol_to_cell(row_vnmo, summary_col0 + 3, row_abs=True, col_abs=True)
        v4_abs = xl_rowcol_to_cell(row_vnmo, summary_col0 + 4, row_abs=True, col_abs=True)
        v5_abs = xl_rowcol_to_cell(row_vnmo, summary_col0 + 5, row_abs=True, col_abs=True)

        f1 = f"=IF( ({t1_cell}/1000)^2 - ({x_cell}^2)/({v1_abs}^2) <= 0, 0, SQRT( ({t1_cell}/1000)^2 - ({x_cell}^2)/({v1_abs}^2) )*1000 )"
        f2 = f"=IF( ({t2_cell}/1000)^2 - ({x_cell}^2)/({v2_abs}^2) <= 0, 0, SQRT( ({t2_cell}/1000)^2 - ({x_cell}^2)/({v2_abs}^2) )*1000 )"
        f3 = f"=IF( ({t3_cell}/1000)^2 - ({x_cell}^2)/({v3_abs}^2) <= 0, 0, SQRT( ({t3_cell}/1000)^2 - ({x_cell}^2)/({v3_abs}^2) )*1000 )"
        f4 = f"=IF( ({t4_cell}/1000)^2 - ({x_cell}^2)/({v4_abs}^2) <= 0, 0, SQRT( ({t4_cell}/1000)^2 - ({x_cell}^2)/({v4_abs}^2) )*1000 )"
        f5 = f"=IF( ({t5_cell}/1000)^2 - ({x_cell}^2)/({v5_abs}^2) <= 0, 0, SQRT( ({t5_cell}/1000)^2 - ({x_cell}^2)/({v5_abs}^2) )*1000 )"

        ws.write_formula(row, col_t1_nmo, f1)
        ws.write_formula(row, col_t2_nmo, f2)
        ws.write_formula(row, col_t3_nmo, f3)
        ws.write_formula(row, col_t4_nmo, f4)
        ws.write_formula(row, col_t5_nmo, f5)

    # ajustar col widths
    for c in range(0, col_t5_nmo + 6):
        ws.set_column(c, c, 14)

    # Criar figures numéricas para PNGs (calculados com pandas) 
    # - isto gera as imagens que vamos inserir no PDF
    dfnum = df_work.copy()
    for i in range(1,6):
        dfnum[f"t{i}_s"] = dfnum[f"t_r{i}_ms"] / 1000.0
        dfnum[f"t{i}_s2"] = dfnum[f"t{i}_s"] ** 2
    dfnum["x2"] = dfnum["offset_m"] ** 2

    slopes = []; intercepts = []; t0s_ms = []; vnmos = []
    for i in range(1,6):
        x = dfnum["x2"].values
        y = dfnum[f"t{i}_s2"].values
        mask = (~np.isnan(x)) & (~np.isnan(y))
        if mask.sum() < 3:
            slopes.append(np.nan); intercepts.append(np.nan); t0s_ms.append(np.nan); vnmos.append(np.nan)
            continue
        slope, intercept = np.polyfit(x[mask], y[mask], 1)
        slopes.append(slope); intercepts.append(intercept)
        t0s_ms.append(np.sqrt(intercept)*1000.0 if intercept >= 0 else np.nan)
        vnmos.append(np.sqrt(1.0/slope) if slope > 0 else np.nan)

    # calcular Vint numeric e depths numeric para tabela do PDF
    v_int_nums = [np.nan]*5
    for i in range(5):
        if i == 0:
            v_int_nums[i] = vnmos[i]
        else:
            if not np.isnan(vnmos[i]) and not np.isnan(vnmos[i-1]) and not np.isnan(t0s_ms[i]) and not np.isnan(t0s_ms[i-1]):
                t_i = t0s_ms[i]/1000.0
                t_prev = t0s_ms[i-1]/1000.0
                if (t_i - t_prev) > 0:
                    val = ((vnmos[i]**2 * t_i) - (vnmos[i-1]**2 * t_prev)) / (t_i - t_prev)
                    v_int_nums[i] = np.sqrt(val) if val > 0 else np.nan
    depths = []
    thicknesses = []
    acc = 0.0
    t_prev = 0.0
    for i in range(5):
        if np.isnan(v_int_nums[i]) or np.isnan(t0s_ms[i]):
            thicknesses.append(np.nan)
            depths.append(np.nan)
            continue
        t_i = t0s_ms[i]/1000.0
        thick = v_int_nums[i] * ((t_i - t_prev)/2.0)
        acc += thick
        thicknesses.append(thick)
        depths.append(acc)
        t_prev = t_i

    # gerar PNGs (t^2 vs x^2 para cada reflexao, Vnmo vs t0, depths, thicknesses)
    png_files = []
    for i in range(1,6):
        x = dfnum["x2"].values
        y = dfnum[f"t{i}_s2"].values
        mask = (~np.isnan(x)) & (~np.isnan(y))
        if mask.sum() < 3:
            continue
        plt.figure(figsize=(6,4))
        plt.scatter(x[mask], y[mask], s=20)
        if not np.isnan(slopes[i-1]) and not np.isnan(intercepts[i-1]):
            xs = np.linspace(x[mask].min(), x[mask].max(), 200)
            plt.plot(xs, slopes[i-1]*xs + intercepts[i-1], label=f"y={slopes[i-1]:.3e}x + {intercepts[i-1]:.3e}")
        plt.xlabel("x^2 (m^2)")
        plt.ylabel("t^2 (s^2)")
        plt.title(f"t^2 vs x^2 - Reflexão {i}")
        plt.grid(True, ls=":")
        plt.legend()
        p = Path(OUTPUT_DIR) / f"t2_vs_x2_ref{i}.png"
        plt.tight_layout()
        plt.savefig(p, dpi=200)
        plt.close()
        png_files.append(p)

    # Vnmo vs t0
    valid = [i for i in range(5) if not np.isnan(vnmos[i]) and not np.isnan(t0s_ms[i])]
    if len(valid) >= 2:
        plt.figure(figsize=(6,4))
        plt.plot([t0s_ms[i] for i in valid], [vnmos[i] for i in valid], marker='o', linestyle='-')
        plt.xlabel("t0 (ms)")
        plt.ylabel("Vnmo (m/s)")
        plt.title("Vnmo vs t0")
        plt.grid(True, ls=":")
        p = Path(OUTPUT_DIR) / "Vnmo_vs_t0.png"
        plt.tight_layout()
        plt.savefig(p, dpi=200)
        plt.close()
        png_files.append(p)

    # depths plot
    if any(not np.isnan(d) for d in depths):
        plt.figure(figsize=(6,4))
        labels = [str(i+1) for i in range(5)]
        vals = [d if not np.isnan(d) else 0 for d in depths]
        plt.bar(labels, vals)
        plt.xlabel("Reflector")
        plt.ylabel("Profundidade (m)")
        plt.title("Profundidade por Reflector")
        plt.grid(axis='y', ls=":")
        p = Path(OUTPUT_DIR) / "depths_per_reflector.png"
        plt.tight_layout()
        plt.savefig(p, dpi=200)
        plt.close()
        png_files.append(p)

    # thicknesses plot
    if any(not np.isnan(t) for t in thicknesses):
        plt.figure(figsize=(6,4))
        labels = [str(i+1) for i in range(5)]
        vals = [t if not np.isnan(t) else 0 for t in thicknesses]
        plt.bar(labels, vals)
        plt.xlabel("Camada")
        plt.ylabel("Espessura (m)")
        plt.title("Espessura por Camada")
        plt.grid(axis='y', ls=":")
        p = Path(OUTPUT_DIR) / "thickness_per_layer.png"
        plt.tight_layout()
        plt.savefig(p, dpi=200)
        plt.close()
        png_files.append(p)

    # inserir imagens na folha Graficos (opcional) e salvar workbook
    ws_g = workbook.add_worksheet("Graficos")
    r = 1
    c = 1
    for p in png_files:
        ws_g.insert_image(r, c, str(p.resolve()), {'x_scale': 0.9, 'y_scale': 0.9})
        r += 20

# Excel salvo no exit do with
print("Excel criado:", output_excel.resolve())

# -----------------------------
# Criar PDF: compilar PNGs + tabela de resultados
# -----------------------------
# Preparar tabela de resultados (DataFrame)
res_df = pd.DataFrame({
    "Reflector": [1,2,3,4,5],
    "t0_ms": t0s_ms,
    "Vnmo_m_s": vnmos,
    "Vint_m_s": v_int_nums,
    "Thickness_m": thicknesses,
    "Depth_m": depths
})
res_df_display = res_df.copy()
res_df_display = res_df_display.set_index("Reflector")
res_df_display = res_df_display.round({
    "t0_ms": 3, "Vnmo_m_s": 2, "Vint_m_s": 2, "Thickness_m": 2, "Depth_m": 2
})

# criar PDF com PdfPages
with PdfPages(output_pdf) as pdf:
    # capa simples
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 portrait in inches
    fig.suptitle(f"Relatório NMO - {input_file.stem}", fontsize=16)
    fig.text(0.1, 0.8, f"Arquivo de entrada: {input_file.name}")
    fig.text(0.1, 0.78, f"Criado por script automatizado")
    fig.text(0.1, 0.76, f"Observações: tempos originais em ms; fórmulas inseridas no Excel na folha 'Calculos'")
    pdf.savefig(fig)
    plt.close(fig)

    # inserir cada PNG como página
    for p in png_files:
        img = plt.imread(p)
        fig = plt.figure(figsize=(8.27, 11.69))
        plt.imshow(img)
        plt.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    # tabela de resultados (renderizar como figura)
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.axis('off')
    table = ax.table(cellText=res_df_display.reset_index().values,
                     colLabels=res_df_display.reset_index().columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.2)
    ax.set_title("Tabela de resultados (t0, Vnmo, Vint, Espessuras, Profundidades)")
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

print("PDF gerado:", output_pdf.resolve())
print("PNGs em:", Path(OUTPUT_DIR).resolve())