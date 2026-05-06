"""
Projeto de Engenharia de Reservatórios I
Cálculo do factor de compressibilidade do gás natural (Z)

Métodos:
- Gás ideal
- Hall-Yarborough (Newton-Raphson)
- Dranchuk & Abou-Kassem (iteração na densidade reduzida)
- Correcções: Wichert-Aziz, Carr-Kobayashi-Burrows
- Propriedades pseudo-críticas: Standing (seco/húmido) e Sutton (húmido)

Unidades:
- Pressão: psia
- Temperatura: °F (convertida para °R internamente)
- Frações molares: decimais (ex.: 5% = 0.05)

Autor: Fusão dos códigos original e melhorado
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font
import math
import csv

# Tentar importar matplotlib para gráficos
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ============================================================================
# Módulo de cálculo (versão corrigida, baseada no primeiro código)
# ============================================================================

def f_to_r(temp_f: float) -> float:
    """Converte °F para °R."""
    return temp_f + 459.67


# --- Propriedades pseudo-críticas -------------------------------------------------
def pseudo_critical_standing_dry(gamma_g: float):
    """Standing (1977) para gás seco."""
    ppc = 677.0 + 15.0 * gamma_g - 37.5 * gamma_g ** 2
    tpc = 168.0 + 325.0 * gamma_g - 12.5 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_standing_wet(gamma_g: float):
    """Standing (1977) para gás húmido / condensado."""
    ppc = 706.0 - 51.7 * gamma_g - 11.1 * gamma_g ** 2
    tpc = 187.0 + 330.0 * gamma_g - 71.5 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_sutton_wet(gamma_g: float):
    """Sutton para gás húmido / condensado."""
    ppc = 169.2 + 349.5 * gamma_g - 74.0 * gamma_g ** 2
    tpc = 756.8 - 131.07 * gamma_g - 3.6 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_properties(gamma_g: float, method: str = "standing_dry"):
    method = method.lower().strip()
    if method == "standing_dry":
        return pseudo_critical_standing_dry(gamma_g)
    if method == "standing_wet":
        return pseudo_critical_standing_wet(gamma_g)
    if method == "sutton_wet":
        return pseudo_critical_sutton_wet(gamma_g)
    raise ValueError("Método pseudo-crítico inválido.")


# --- Correcções de contaminantes -------------------------------------------------
def wichert_aziz(tpc: float, ppc: float, y_co2: float, y_h2s: float):
    """Correcção Wichert‑Aziz (com y_CO2^4 no termo D)."""
    s = y_co2 + y_h2s
    if s <= 0:
        return tpc, ppc
    d = math.sqrt(max(y_h2s, 0.0)) - (y_co2 ** 4)
    eps = 120.0 * (s ** 0.9 - s ** 1.6) + 15.0 * d
    tpc_corr = tpc - eps
    denom = tpc + y_h2s * (1.0 - y_h2s) * eps
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Denominador nulo na correcção Wichert-Aziz.")
    ppc_corr = (ppc * tpc_corr) / denom
    return tpc_corr, ppc_corr


def carr_kobayashi_burrows(tpc: float, ppc: float, y_co2: float, y_h2s: float, y_n2: float):
    """Correcção Carr‑Kobayashi‑Burrows simplificada."""
    tpc_corr = tpc - 80.0 * y_co2 + 130.0 * y_h2s - 250.0 * y_n2
    ppc_corr = ppc + 440.0 * y_co2 + 600.0 * y_h2s - 170.0 * y_n2
    if tpc_corr <= 0 or ppc_corr <= 0:
        raise ValueError("Correcção Carr-Kobayashi-Burrows produziu propriedades inválidas.")
    return tpc_corr, ppc_corr


def corrected_pseudocriticals(gamma_g: float, y_co2: float, y_h2s: float, y_n2: float,
                              correction: str, pseudo_method: str):
    """Obtém Tpc e Ppc corrigidos conforme escolha do utilizador."""
    tpc, ppc = pseudo_critical_properties(gamma_g, pseudo_method)
    correction = correction.lower().strip()
    if correction == "none":
        return tpc, ppc
    if correction == "wichert_aziz":
        return wichert_aziz(tpc, ppc, y_co2, y_h2s)
    if correction == "carr_kobayashi_burrows":
        return carr_kobayashi_burrows(tpc, ppc, y_co2, y_h2s, y_n2)
    raise ValueError("Correcção inválida.")


# --- Métodos de cálculo do factor Z ------------------------------------------------
def z_ideal() -> float:
    return 1.0


def hall_yarborough_z(ppr: float, tpr: float, tol: float = 1e-5, max_iter: int = 100):
    """Hall‑Yarborough via Newton‑Raphson. Retorna (Z, info)."""
    if tpr <= 0:
        raise ValueError("Tpr deve ser positivo.")
    t = 1.0 / tpr
    y = 0.001
    for it in range(1, max_iter + 1):
        a = -0.06125 * ppr * t * math.exp(-1.2 * (1.0 - t) ** 2)
        b = y * (1.0 + y + y ** 2 - y ** 3) / (1.0 - y) ** 3
        c = -((4.58 * t - 9.76) * t + 14.76) * t * y ** 2
        d = ((42.4 * t - 242.2) * t + 90.7) * t * y ** (2.18 + 2.82 * t)
        f = a + b + c + d

        db = (y ** 4 - 4.0 * y ** 3 + 4.0 * y ** 2 + 4.0 * y + 1.0) / (1.0 - y) ** 4
        dc = -2.0 * ((4.58 * t - 9.76) * t + 14.76) * t * y
        dd = (2.18 + 2.82 * t) * ((42.4 * t - 242.2) * t + 90.7) * t * y ** (1.18 + 2.82 * t)
        df = db + dc + dd

        if abs(df) < 1e-14:
            raise ZeroDivisionError("Derivada quase nula.")
        y_new = y - f / df
        if abs(y_new - y) < tol:
            y = y_new
            break
        y = y_new
    z = 0.06125 * ppr * t * math.exp(-1.2 * (1.0 - t) ** 2) / y
    return z, {"iterations": it, "y": y}


DAK_COEFFS = {
    "A1": 0.3265, "A2": -1.0700, "A3": -0.5339, "A4": 0.01569, "A5": -0.05165,
    "A6": 0.5475, "A7": -0.7361, "A8": 0.1844, "A9": 0.1056, "A10": 0.6134, "A11": 0.7210,
}


def dak_z_from_rhor(rhor: float, tpr: float) -> float:
    """Z de DAK a partir da densidade reduzida."""
    c = DAK_COEFFS
    a1 = c["A1"] + c["A2"] / tpr + c["A3"] / tpr ** 3 + c["A4"] / tpr ** 4 + c["A5"] / tpr ** 5
    a2 = c["A6"] + c["A7"] / tpr + c["A8"] / tpr ** 2
    a3 = c["A9"] * (c["A7"] / tpr + c["A8"] / tpr ** 2)
    a4 = c["A10"] / tpr ** 3
    a5 = c["A11"]
    return (1.0 + a1 * rhor + a2 * rhor ** 2 - a3 * rhor ** 5 +
            a4 * (1.0 + a5 * rhor ** 2) * rhor ** 2 * math.exp(-a5 * rhor ** 2))


def dranchuk_abou_kassem_z(ppr: float, tpr: float, tol: float = 1e-8, max_iter: int = 200):
    """DAK por iteração na densidade reduzida."""
    if tpr <= 0:
        raise ValueError("Tpr deve ser positivo.")
    rhor = max(1e-8, 0.27 * ppr / tpr)
    for it in range(1, max_iter + 1):
        z = dak_z_from_rhor(rhor, tpr)
        rhor_new = 0.5 * rhor + 0.5 * (0.27 * ppr / (z * tpr))
        if abs(rhor_new - rhor) < tol:
            rhor = rhor_new
            break
        rhor = rhor_new
    z = dak_z_from_rhor(rhor, tpr)
    return z, {"iterations": it, "rho_r": rhor}


# ============================================================================
# Viscosidade do gás natural
# ============================================================================

def lee_gonzalez_eakin_viscosity(T_R: float, P: float, Z: float, gamma_g: float) -> float:
    """Lee-González-Eakin (1966) gas viscosity correlation.

    Parameters: T_R [°R], P [psia], Z [-], gamma_g (air = 1)
    Returns: μg [cp]
    """
    M = 28.97 * gamma_g
    rho_lb_ft3 = P * M / (Z * 10.73 * T_R)
    rho_gcc = rho_lb_ft3 / 62.4
    K = (9.4 + 0.02 * M) * T_R ** 1.5 / (209.0 + 19.0 * M + T_R)
    X = 3.5 + 986.0 / T_R + 0.01 * M
    Y = 2.4 - 0.2 * X
    return K * math.exp(X * rho_gcc ** Y) * 1.0e-4  # cp


def lucas_viscosity(T_R: float, Tpc: float, Ppc: float,
                   gamma_g: float, P: float) -> float:
    """Lucas (1981) gas viscosity correlation with high-pressure correction.

    Parameters: T_R [°R], Tpc [°R], Ppc [psia], gamma_g (air=1), P [psia]
    Returns: μg [cp]
    """
    M = 28.97 * gamma_g
    Tr = T_R / Tpc
    Pr = P / Ppc
    if Tr <= 0:
        raise ValueError("Tpr deve ser positivo.")

    # Parâmetro redutor de viscosidade ξ (unidades de campo)
    xi = Tpc ** (1.0 / 6.0) / (M ** 0.5 * Ppc ** (2.0 / 3.0))

    # Viscosidade à pressão atmosférica [cp]
    mu_1 = (
        0.807 * Tr ** 0.618
        - 0.357 * math.exp(-0.449 * Tr)
        + 0.340 * math.exp(-4.058 * Tr)
        + 0.018
    ) / xi * 1.0e-4

    # Correcção de alta pressão – coeficientes de Lucas (1981)
    a1 = 1.245e-3; a2 = 5.1726;  a3 = 0.3286
    a4 = 1.6553;  a5 = 1.2723;  a6 = 0.4489
    a7 = 3.0578;  a8 = 37.7332; a9 = 1.7368; a10 = 2.2310

    A = a1 * math.exp(a2 * (1.0 - Tr ** (-a3)))
    B = A * (a4 * Tr - a5)
    C = a6 * math.exp(a7 * (1.0 - Tr ** (-a8))) / Tr
    D = a9 + a10 / Tr

    Pr_pow = Pr ** 1.3088
    inner = 1.0 + C * Pr ** D
    denom = B * Pr_pow + (1.0 / inner if abs(inner) > 1e-15 else 0.0)
    if abs(denom) < 1e-14:
        return mu_1
    return mu_1 * (1.0 + A * Pr_pow / denom)  # cp


# ============================================================================
# Factor Volume de Formação e Factor de Expansão do Gás
# ============================================================================

def gas_formation_volume_factor(Z: float, T_R: float, P: float,
                                unit: str = "bbl_scf") -> float:
    """Factor Volume de Formação do Gás (Bg).

    Condições standard: Psc = 14.7 psia, Tsc = 519.67 °R (60 °F).
    Unidades disponíveis: 'bbl_scf', 'ft3_scf', 'm3_m3'
    """
    Bg_ft3 = 0.028269 * Z * T_R / P  # res ft³ / scf
    if unit == "bbl_scf":
        return Bg_ft3 / 5.61458       # res bbl / scf
    elif unit == "m3_m3":
        return Bg_ft3                 # res m³/sm³ ≈ res ft³/scf numericament
    else:
        return Bg_ft3                 # ft3_scf


def gas_expansion_factor(Z: float, T_R: float, P: float,
                         unit: str = "scf_bbl") -> float:
    """Factor de Expansão do Gás (Eg = 1 / Bg).

    Unidades disponíveis: 'scf_bbl', 'scf_ft3', 'm3_m3'
    """
    if unit == "scf_bbl":
        Bg = gas_formation_volume_factor(Z, T_R, P, "bbl_scf")
    elif unit == "m3_m3":
        Bg = gas_formation_volume_factor(Z, T_R, P, "m3_m3")
    else:
        Bg = gas_formation_volume_factor(Z, T_R, P, "ft3_scf")
    return 1.0 / Bg if abs(Bg) > 1e-15 else float("inf")


# ============================================================================
# Interface gráfica (baseada no segundo código, com ajustes)
# ============================================================================

class GasZApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Factor de Compressibilidade de Gas (Z factor) – Engenharia de Reservatórios I | ISPTEC")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        self.setup_style()

        # Variáveis de entrada
        self.var_p = tk.DoubleVar()
        self.var_t = tk.DoubleVar()
        self.var_gamma = tk.DoubleVar()
        self.var_n2 = tk.DoubleVar()
        self.var_co2 = tk.DoubleVar()
        self.var_h2s = tk.DoubleVar()
        self.var_use_direct = tk.BooleanVar(value=False)
        self.var_tpc_direct = tk.DoubleVar()
        self.var_ppc_direct = tk.DoubleVar()
        self.var_pseudo_method = tk.StringVar(value="standing_dry")
        self.var_correction = tk.StringVar(value="wichert_aziz")

        # Variáveis da malha
        self.var_calc_mode = tk.StringVar(value="single")
        self.var_p_start = tk.DoubleVar()
        self.var_p_end = tk.DoubleVar()
        self.var_p_points = tk.IntVar(value=10)

        # Armazenar resultados
        self.last_results = None

        # Variáveis de Phase 2 – Propriedades do Gás
        self.var_z_method   = tk.StringVar(value="hall_yarborough")
        self.var_visc_method = tk.StringVar(value="lee_gonzalez_eakin")
        self.var_bg_unit    = tk.StringVar(value="bbl_scf")
        self.var_eg_unit    = tk.StringVar(value="scf_bbl")

        # Criar notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Abas
        self.tab_input = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_input, text="📊 Entrada de Dados")
        self.create_input_tab()

        self.tab_results = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_results, text="📈 Resultados")
        self.create_results_tab()

        if MATPLOTLIB_AVAILABLE:
            self.tab_plot = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_plot, text="📉 Gráfico Comparativo")
            self.create_plot_tab()
        else:
            self.tab_plot = None

        self.tab_tutorial = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tutorial, text="📘 Tutorial / Exemplo")
        self.create_tutorial_tab()

        self.tab_props = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_props, text="⚗️ Propriedades do Gás")
        self.create_props_tab()

        # Barra de status
        self.status = ttk.Label(root, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Atualizar sidebar quando valores mudam
        self.var_t.trace_add('write', lambda *a: self.update_sidebar())
        self.var_gamma.trace_add('write', lambda *a: self.update_sidebar())
        self.var_n2.trace_add('write', lambda *a: self.update_sidebar())
        self.var_co2.trace_add('write', lambda *a: self.update_sidebar())
        self.var_h2s.trace_add('write', lambda *a: self.update_sidebar())
        self.var_pseudo_method.trace_add('write', lambda *a: self.update_sidebar())
        self.var_correction.trace_add('write', lambda *a: self.update_sidebar())
        self.var_use_direct.trace_add('write', lambda *a: self.toggle_direct())
        self.var_tpc_direct.trace_add('write', lambda *a: self.update_sidebar())
        self.var_ppc_direct.trace_add('write', lambda *a: self.update_sidebar())
        self.var_calc_mode.trace_add('write', lambda *a: self.update_mode_visibility())
        self.var_p_start.trace_add('write', lambda *a: self.update_sidebar())
        self.var_p_end.trace_add('write', lambda *a: self.update_sidebar())
        self.var_p_points.trace_add('write', lambda *a: self.update_sidebar())

        self.update_mode_visibility()
        self.toggle_direct()
        self.update_sidebar()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = "#f0f0f0"
        accent_color = "#2c7da0"
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#1f5e7a")])
        style.configure("Accent.TButton", foreground="white", background=accent_color)
        style.configure("TEntry", fieldbackground="white", font=("Segoe UI", 10))
        style.configure("TLabelframe", background=bg_color, font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color)
        style.configure("TNotebook", background=bg_color)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", accent_color)], foreground=[("selected", "white")])

    def create_input_tab(self):
        main_panel = ttk.Frame(self.tab_input)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = ttk.Frame(main_panel)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right = ttk.Frame(main_panel)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        ttk.Label(left, text="Parâmetros do Reservatório", font=title_font).pack(anchor=tk.W, pady=(0, 10))
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Campos
        f = ttk.Frame(left)
        f.pack(fill=tk.X, pady=5)
        ttk.Label(f, text="Temperatura (°F):", width=25, anchor=tk.W).pack(side=tk.LEFT)
        ttk.Entry(f, textvariable=self.var_t, width=15).pack(side=tk.RIGHT)

        f = ttk.Frame(left)
        f.pack(fill=tk.X, pady=5)
        ttk.Label(f, text="Densidade relativa (ar=1):", width=25, anchor=tk.W).pack(side=tk.LEFT)
        ttk.Entry(f, textvariable=self.var_gamma, width=15).pack(side=tk.RIGHT)

        # Contaminantes
        ttk.Label(left, text="Contaminantes (frações molares):", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        cont = ttk.Frame(left)
        cont.pack(fill=tk.X)
        ttk.Label(cont, text="N₂:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(cont, textvariable=self.var_n2, width=10).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(cont, text="CO₂:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(cont, textvariable=self.var_co2, width=10).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(cont, text="H₂S:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(cont, textvariable=self.var_h2s, width=10).pack(side=tk.LEFT)

        # Opções de método pseudo-crítico e correcção
        frame_opts = ttk.LabelFrame(left, text="Modelos de Propriedades Críticas", padding=5)
        frame_opts.pack(fill=tk.X, pady=10)

        ttk.Label(frame_opts, text="Correlação:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        pseudo_combo = ttk.Combobox(frame_opts, textvariable=self.var_pseudo_method,
                                    values=["standing_dry", "standing_wet", "sutton_wet"],
                                    state="readonly", width=20)
        pseudo_combo.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(frame_opts, text="Correcção:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        corr_combo = ttk.Combobox(frame_opts, textvariable=self.var_correction,
                                  values=["none", "wichert_aziz", "carr_kobayashi_burrows"],
                                  state="readonly", width=20)
        corr_combo.grid(row=1, column=1, padx=5, pady=2)

        # Opção Tpc/Ppc diretas
        ttk.Checkbutton(left, text="Usar Tpc e Ppc diretamente", variable=self.var_use_direct,
                        command=self.toggle_direct).pack(anchor=tk.W, pady=10)
        self.direct_frame = ttk.Frame(left)
        self.direct_frame.pack(anchor=tk.W, pady=5)
        ttk.Label(self.direct_frame, text="Tpc (°R):").pack(side=tk.LEFT)
        self.entry_tpc = ttk.Entry(self.direct_frame, textvariable=self.var_tpc_direct, width=10)
        self.entry_tpc.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.direct_frame, text="Ppc (psia):").pack(side=tk.LEFT)
        self.entry_ppc = ttk.Entry(self.direct_frame, textvariable=self.var_ppc_direct, width=10)
        self.entry_ppc.pack(side=tk.LEFT, padx=5)

        # Modo de cálculo
        mode_frame = ttk.LabelFrame(left, text="Modo de Cálculo", padding=5)
        mode_frame.pack(fill=tk.X, pady=10)
        ttk.Radiobutton(mode_frame, text="Único", variable=self.var_calc_mode, value="single").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Malha de pressão", variable=self.var_calc_mode, value="mesh").pack(anchor=tk.W)

        self.single_frame = ttk.Frame(mode_frame)
        self.single_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.single_frame, text="Pressão (psia):").pack(side=tk.LEFT)
        ttk.Entry(self.single_frame, textvariable=self.var_p, width=15).pack(side=tk.RIGHT)

        self.mesh_frame = ttk.Frame(mode_frame)
        ttk.Label(self.mesh_frame, text="P inicial (psia):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.mesh_frame, textvariable=self.var_p_start, width=12).grid(row=0, column=1, padx=5)
        ttk.Label(self.mesh_frame, text="P final (psia):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.mesh_frame, textvariable=self.var_p_end, width=12).grid(row=1, column=1, padx=5)
        ttk.Label(self.mesh_frame, text="Nº de pontos:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.mesh_frame, textvariable=self.var_p_points, width=12).grid(row=2, column=1, padx=5)

        # Botão calcular
        ttk.Button(left, text="Calcular Fator Z", command=self.calcular, style="Accent.TButton").pack(pady=20)

        # Área do passo a passo (direita)
        ttk.Label(right, text="Passo a Passo do Cálculo", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        ttk.Separator(right, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        self.step_text = tk.Text(right, height=25, font=("Courier New", 10), wrap=tk.WORD, bg="#fafafa", relief=tk.FLAT)
        self.step_text.pack(fill=tk.BOTH, expand=True, pady=5)
        scroll = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self.step_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_text.configure(yscrollcommand=scroll.set)
        self.step_text.config(state=tk.DISABLED)

    def toggle_direct(self):
        if self.var_use_direct.get():
            self.entry_tpc.config(state='normal')
            self.entry_ppc.config(state='normal')
        else:
            self.entry_tpc.config(state='disabled')
            self.entry_ppc.config(state='disabled')
        self.update_sidebar()

    def update_mode_visibility(self):
        if self.var_calc_mode.get() == "single":
            self.single_frame.pack(fill=tk.X, pady=5)
            self.mesh_frame.pack_forget()
        else:
            self.single_frame.pack_forget()
            self.mesh_frame.pack(fill=tk.X, pady=5)

    def update_sidebar(self):
        if not hasattr(self, 'step_text'):
            return
        try:
            T = self.var_t.get()
            gamma = self.var_gamma.get()
            y_N2 = self.var_n2.get()
            y_CO2 = self.var_co2.get()
            y_H2S = self.var_h2s.get()
        except:
            return

        if self.var_use_direct.get():
            Tpc = self.var_tpc_direct.get()
            Ppc = self.var_ppc_direct.get()
            Tpc_prime, Ppc_prime = Tpc, Ppc  # sem correcções se directo
            corr_applied = " (diretas)"
        else:
            # Calcular Tpc e Ppc base com método escolhido
            try:
                Tpc, Ppc = pseudo_critical_properties(gamma, self.var_pseudo_method.get())
            except:
                Tpc, Ppc = 0, 0
            # Aplicar correcção escolhida
            try:
                Tpc_prime, Ppc_prime = corrected_pseudocriticals(
                    gamma, y_CO2, y_H2S, y_N2,
                    self.var_correction.get(), self.var_pseudo_method.get()
                )
            except:
                Tpc_prime, Ppc_prime = Tpc, Ppc
            corr_applied = f" (correcção: {self.var_correction.get()})"

        # Pressão de referência para o passo a passo
        if self.var_calc_mode.get() == "single":
            P = self.var_p.get()
        else:
            P = self.var_p_start.get()

        if Ppc_prime != 0:
            Ppr = P / Ppc_prime
        else:
            Ppr = 0
        T_R_sb = f_to_r(T)  # convert °F → °R for the sidebar display
        if Tpc_prime != 0:
            Tpr = T_R_sb / Tpc_prime
        else:
            Tpr = 0

        lines = []
        lines.append("=" * 60)
        lines.append("1. PROPRIEDADES PSEUDO-CRÍTICAS")
        lines.append(f"   Método: {self.var_pseudo_method.get()}")
        if not self.var_use_direct.get():
            lines.append(f"   Tpc base = {Tpc:.2f} °R")
            lines.append(f"   Ppc base = {Ppc:.2f} psia")
            lines.append(f"   Aplicando correcção {corr_applied}")
        lines.append(f"   Tpc' = {Tpc_prime:.2f} °R")
        lines.append(f"   Ppc' = {Ppc_prime:.2f} psia")
        lines.append("")
        lines.append("=" * 60)
        lines.append("2. PARÂMETROS REDUZIDOS")
        lines.append(f"   Ppr = {P:.2f} / {Ppc_prime:.2f} = {Ppr:.4f}")
        lines.append(f"   Tpr = ({T:.2f}°F → {T_R_sb:.2f}°R) / {Tpc_prime:.2f} = {Tpr:.4f}")
        lines.append("")
        lines.append("=" * 60)
        lines.append("3. FATOR Z - HALL-YARBOROUGH")
        if self.last_results and self.var_calc_mode.get() == "single" and 'Z_HY' in self.last_results:
            lines.append(f"   Z_HY = {self.last_results['Z_HY']:.6f}")
        else:
            lines.append("   Z_HY = ? (Clique em 'Calcular')")
        lines.append("")
        lines.append("=" * 60)
        lines.append("4. FATOR Z - DRANCHUK & ABOU-KASSEM")
        if self.last_results and self.var_calc_mode.get() == "single" and 'Z_DAK' in self.last_results:
            lines.append(f"   Z_DAK = {self.last_results['Z_DAK']:.6f}")
        else:
            lines.append("   Z_DAK = ? (Clique em 'Calcular')")

        self.step_text.config(state=tk.NORMAL)
        self.step_text.delete(1.0, tk.END)
        self.step_text.insert(tk.END, "\n".join(lines))
        self.step_text.config(state=tk.DISABLED)

    def create_results_tab(self):
        self.results_frame = ttk.Frame(self.tab_results)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = ttk.Label(self.results_frame, text="Resultados do Cálculo", font=("Segoe UI", 14, "bold"))
        title.pack(pady=10)

        self.results_notebook = ttk.Notebook(self.results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_single = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.tab_single, text="Resumo")

        self.tab_mesh = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.tab_mesh, text="Tabela (Malha)")

        self.tree_single = ttk.Treeview(self.tab_single, columns=("Método", "Fator Z"), show="headings", height=8)
        self.tree_single.heading("Método", text="Método")
        self.tree_single.heading("Fator Z", text="Fator Z")
        self.tree_single.column("Método", width=200, anchor=tk.CENTER)
        self.tree_single.column("Fator Z", width=150, anchor=tk.CENTER)
        self.tree_single.pack(pady=10, padx=10, fill=tk.X)

        self.details_text = tk.Text(self.tab_single, height=15, font=("Courier New", 10), wrap=tk.WORD, state=tk.DISABLED)
        scroll = ttk.Scrollbar(self.tab_single, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scroll.set)
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.mesh_tree = ttk.Treeview(self.tab_mesh, columns=("Pressão (psia)", "Z_HY", "Z_DAK"), show="headings", height=20)
        self.mesh_tree.heading("Pressão (psia)", text="Pressão (psia)")
        self.mesh_tree.heading("Z_HY", text="Hall-Yarborough")
        self.mesh_tree.heading("Z_DAK", text="Dranchuk & Abou-Kassem")
        self.mesh_tree.column("Pressão (psia)", width=120, anchor=tk.CENTER)
        self.mesh_tree.column("Z_HY", width=150, anchor=tk.CENTER)
        self.mesh_tree.column("Z_DAK", width=180, anchor=tk.CENTER)
        self.mesh_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.results_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Copiar Resultados", command=self.copy_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar CSV (Malha)", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.clear_results).pack(side=tk.LEFT, padx=5)

    def create_plot_tab(self):
        self.plot_frame = ttk.Frame(self.tab_plot)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.plot_label = ttk.Label(self.plot_frame, text="Clique em 'Calcular' para gerar o gráfico.")
        self.plot_label.pack(pady=50)

    def create_tutorial_tab(self):
        canvas = tk.Canvas(self.tab_tutorial, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_tutorial, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        main = scrollable_frame
        main.columnconfigure(0, weight=1)
        title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        ttk.Label(main, text="Como Utilizar a Ferramenta", font=title_font).grid(row=0, column=0, pady=10, sticky="w")

        instr = """
        Esta ferramenta calcula o fator Z do gás natural usando três abordagens:
        • Gás Ideal (Z = 1)
        • Hall-Yarborough (Newton-Raphson)
        • Dranchuk & Abou-Kassem (iteração na densidade reduzida)

        Modos de cálculo:
        - Único: insira uma pressão específica e obtenha Z para ela.
        - Malha de pressão: defina um intervalo e número de pontos; o programa calcula Z para cada pressão e exibe tabela e gráfico.

        Passo a passo:
        1. Preencha os parâmetros do reservatório (temperatura em °F, densidade relativa, contaminantes).
        2. Escolha a correlação para propriedades pseudo-críticas (Standing seco, Standing húmido, Sutton húmido).
        3. Selecione a correcção desejada (Wichert-Aziz, Carr-Kobayashi-Burrows ou nenhuma).
        4. Escolha o modo de cálculo e preencha os valores de pressão.
        5. Opcionalmente, marque "Usar Tpc e Ppc diretamente" e informe os valores.
        6. Clique em "Calcular Fator Z".
        7. Os resultados aparecem na aba "Resultados" (tabela e detalhes).
        8. Se houver gráfico, a aba "Gráfico Comparativo" mostrará a variação de Z com a pressão.

        Dicas:
        • Unidades: pressão em psia, temperatura em °F (convertida internamente para °R).
        • Frações molares devem estar entre 0 e 1.
        • A correcção de Wichert-Aziz é aplicada apenas quando H₂S > 0.
        """
        txt = tk.Text(main, height=12, font=("Segoe UI", 10), wrap=tk.WORD, bg="#fafafa", relief=tk.FLAT)
        txt.insert(tk.END, instr)
        txt.config(state=tk.DISABLED)
        txt.grid(row=1, column=0, sticky="ew", pady=5, padx=10)

        ttk.Separator(main, orient=tk.HORIZONTAL).grid(row=2, column=0, sticky="ew", pady=10)
        ttk.Label(main, text="Exemplo Prático", font=("Segoe UI", 12, "bold")).grid(row=3, column=0, sticky="w", pady=10, padx=10)
        ex = """
        Gás com:
        • Temperatura: 160 °F
        • Densidade relativa: 0.70
        • Contaminantes: N₂ = 0%, CO₂ = 5%, H₂S = 10%
        • Método pseudo-crítico: standing_dry
        • Correcção: wichert_aziz
        • Modo: Malha de pressão de 1000 a 5000 psia, 10 pontos.
        Clique em "Carregar Exemplo" e depois em "Calcular".
        """
        ex_widget = tk.Text(main, height=8, font=("Segoe UI", 10), wrap=tk.WORD, bg="#fafafa", relief=tk.FLAT)
        ex_widget.insert(tk.END, ex)
        ex_widget.config(state=tk.DISABLED)
        ex_widget.grid(row=4, column=0, sticky="ew", pady=5, padx=10)

        ttk.Button(main, text="Carregar Exemplo", command=self.load_example).grid(row=5, column=0, pady=15, padx=10, sticky="w")
        ttk.Label(main, text="").grid(row=6, column=0, pady=10)

    # ------------------------------------------------------------------
    # Aba – Propriedades do Gás (Phase 2)
    # ------------------------------------------------------------------

    def create_props_tab(self):
        """Create the Phase-2 tab: viscosity, Bg, Eg."""
        outer = ttk.Frame(self.tab_props)
        outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        ttk.Label(outer, text="Propriedades do Gás Natural", font=title_font).pack(
            anchor=tk.W, pady=(0, 5)
        )
        ttk.Label(
            outer,
            text=("Calcule primeiro o Factor Z na aba 'Entrada de Dados', "
                  "depois configure as opções abaixo e clique em Calcular."),
            wraplength=800,
        ).pack(anchor=tk.W, pady=(0, 5))
        ttk.Separator(outer, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # ---- Options frame ----
        opts = ttk.LabelFrame(outer, text="Configurações de Cálculo", padding=8)
        opts.pack(fill=tk.X, pady=(0, 8))
        opts.columnconfigure(1, weight=1)

        ttk.Label(opts, text="Factor Z – método:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=3)
        ttk.Combobox(
            opts, textvariable=self.var_z_method,
            values=["hall_yarborough", "dranchuk_abou_kassem"],
            state="readonly", width=28
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Label(opts, text="Viscosidade – correlação:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=3)
        ttk.Combobox(
            opts, textvariable=self.var_visc_method,
            values=["lee_gonzalez_eakin", "lucas"],
            state="readonly", width=28
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Label(opts, text="Bg – unidades:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=3)
        ttk.Combobox(
            opts, textvariable=self.var_bg_unit,
            values=["bbl_scf", "ft3_scf", "m3_m3"],
            state="readonly", width=28
        ).grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Label(opts, text="Eg – unidades:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=3)
        ttk.Combobox(
            opts, textvariable=self.var_eg_unit,
            values=["scf_bbl", "scf_ft3", "m3_m3"],
            state="readonly", width=28
        ).grid(row=3, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Button(
            opts, text="Calcular Propriedades",
            command=self.calcular_props, style="Accent.TButton"
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # ---- Results tree ----
        tree_frame = ttk.Frame(outer)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("Pressão (psia)", "Z", "μg (cp)", "Bg", "Eg")
        self.props_tree = ttk.Treeview(
            tree_frame, columns=cols, show="headings", height=18
        )
        col_widths = {"Pressão (psia)": 120, "Z": 110,
                      "μg (cp)": 120, "Bg": 160, "Eg": 160}
        for col in cols:
            self.props_tree.heading(col, text=col)
            self.props_tree.column(col, width=col_widths[col], anchor=tk.CENTER)

        scrollbar_p = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.props_tree.yview
        )
        self.props_tree.configure(yscrollcommand=scrollbar_p.set)
        self.props_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_p.pack(side=tk.RIGHT, fill=tk.Y)

        # Export button
        ttk.Button(
            outer, text="Exportar CSV", command=self.export_props_csv
        ).pack(anchor=tk.W, pady=5)

    def calcular_props(self):
        """Compute viscosity, Bg and Eg using current last_results."""
        if self.last_results is None:
            messagebox.showinfo(
                "Aviso",
                "Calcule primeiro o Factor Z na aba 'Entrada de Dados'."
            )
            return

        try:
            # Reuse the exact T_R, gamma and pseudo-criticals from last calculation
            T_R     = self.last_results["T_R"]
            gamma_g = self.last_results["gamma"]
            Tpc     = self.last_results["Tpc_prime"]
            Ppc     = self.last_results["Ppc_prime"]

            z_meth   = self.var_z_method.get()
            visc_meth = self.var_visc_method.get()
            bg_unit  = self.var_bg_unit.get()
            eg_unit  = self.var_eg_unit.get()

            # Human-readable unit labels for column headers
            bg_labels = {"bbl_scf": "bbl/scf",
                         "ft3_scf": "ft³/scf",
                         "m3_m3":   "m³/m³"}
            eg_labels = {"scf_bbl": "scf/bbl",
                         "scf_ft3": "scf/ft³",
                         "m3_m3":   "sm³/m³"}
            self.props_tree.heading("Bg", text=f"Bg ({bg_labels[bg_unit]})")
            self.props_tree.heading("Eg", text=f"Eg ({eg_labels[eg_unit]})")

            for item in self.props_tree.get_children():
                self.props_tree.delete(item)

            def _compute_row(P, Z):
                if visc_meth == "lee_gonzalez_eakin":
                    mu_g = lee_gonzalez_eakin_viscosity(T_R, P, Z, gamma_g)
                else:
                    mu_g = lucas_viscosity(T_R, Tpc, Ppc, gamma_g, P)
                Bg = gas_formation_volume_factor(Z, T_R, P, bg_unit)
                Eg = gas_expansion_factor(Z, T_R, P, eg_unit)
                return mu_g, Bg, Eg

            if self.last_results["mode"] == "single":
                P = self.last_results["P"]
                Z = (self.last_results["Z_HY"]
                     if z_meth == "hall_yarborough"
                     else self.last_results["Z_DAK"])
                mu_g, Bg, Eg = _compute_row(P, Z)
                self.props_tree.insert(
                    "", tk.END,
                    values=(f"{P:.2f}", f"{Z:.6f}",
                            f"{mu_g:.6f}", f"{Bg:.4e}", f"{Eg:.4f}")
                )
            else:  # mesh
                pressures = self.last_results["pressures"]
                Z_list = (
                    self.last_results["Z_HY"]
                    if z_meth == "hall_yarborough"
                    else self.last_results["Z_DAK"]
                )
                for P, Z in zip(pressures, Z_list):
                    mu_g, Bg, Eg = _compute_row(P, Z)
                    self.props_tree.insert(
                        "", tk.END,
                        values=(f"{P:.2f}", f"{Z:.6f}",
                                f"{mu_g:.6f}", f"{Bg:.4e}", f"{Eg:.4f}")
                    )

            self.status.config(
                text=(
                    f"Propriedades calculadas "
                    f"(Z: {z_meth.replace('_',' ')}, "
                    f"μg: {visc_meth.replace('_',' ')})."
                )
            )
        except Exception as exc:
            messagebox.showerror("Erro", f"Erro ao calcular propriedades:\n{exc}")
            self.status.config(text="Erro no cálculo das propriedades.")

    def export_props_csv(self):
        """Export Phase-2 results to CSV."""
        children = self.props_tree.get_children()
        if not children:
            messagebox.showinfo("Exportar", "Nenhum resultado de propriedades disponível.")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not filename:
            return
        try:
            import csv as _csv
            headers = [self.props_tree.heading(c)["text"]
                       for c in ("Pressão (psia)", "Z", "μg (cp)", "Bg", "Eg")]
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = _csv.writer(f)
                writer.writerow(headers)
                for child in children:
                    writer.writerow(self.props_tree.item(child)["values"])
            self.status.config(text=f"Propriedades exportadas: {filename}")
        except Exception as exc:
            messagebox.showerror("Erro", f"Não foi possível salvar:\n{exc}")

    # ------------------------------------------------------------------

    def load_example(self):
        self.var_t.set(160.0)
        self.var_gamma.set(0.70)
        self.var_n2.set(0.0)
        self.var_co2.set(0.05)
        self.var_h2s.set(0.10)
        self.var_use_direct.set(False)
        self.var_pseudo_method.set("standing_dry")
        self.var_correction.set("wichert_aziz")
        self.var_calc_mode.set("mesh")
        self.var_p_start.set(1000.0)
        self.var_p_end.set(5000.0)
        self.var_p_points.set(10)
        self.update_mode_visibility()
        self.toggle_direct()
        self.status.config(text="Exemplo carregado. Clique em Calcular.")
        self.notebook.select(self.tab_input)
        self.update_sidebar()

    def validate_inputs(self):
        T = self.var_t.get()
        gamma = self.var_gamma.get()
        y_N2 = self.var_n2.get()
        y_CO2 = self.var_co2.get()
        y_H2S = self.var_h2s.get()

        if T <= 0:
            raise ValueError("Temperatura deve ser positiva (°F).")
        if gamma <= 0:
            raise ValueError("Densidade relativa deve ser positiva.")
        for y in (y_N2, y_CO2, y_H2S):
            if not (0 <= y <= 1):
                raise ValueError("Frações molares devem estar entre 0 e 1.")
        if y_N2 + y_CO2 + y_H2S > 1:
            raise ValueError("Soma das frações molares não pode exceder 1.")

        if self.var_use_direct.get():
            Tpc = self.var_tpc_direct.get()
            Ppc = self.var_ppc_direct.get()
            if Tpc <= 0 or Ppc <= 0:
                raise ValueError("Tpc e Ppc devem ser positivos.")

        if self.var_calc_mode.get() == "single":
            P = self.var_p.get()
            if P <= 0:
                raise ValueError("Pressão deve ser positiva.")
        else:
            P_start = self.var_p_start.get()
            P_end = self.var_p_end.get()
            n_points = self.var_p_points.get()
            if P_start <= 0 or P_end <= 0:
                raise ValueError("Pressões inicial e final devem ser positivas.")
            if P_start >= P_end:
                raise ValueError("Pressão inicial deve ser menor que a final.")
            if n_points < 2:
                raise ValueError("Número de pontos deve ser pelo menos 2.")

    def calcular(self):
        self.status.config(text="Calculando...")
        self.root.update()

        try:
            self.validate_inputs()
            T_F = self.var_t.get()
            T_R = f_to_r(T_F)
            gamma = self.var_gamma.get()
            y_N2 = self.var_n2.get()
            y_CO2 = self.var_co2.get()
            y_H2S = self.var_h2s.get()
            pseudo_method = self.var_pseudo_method.get()
            correction = self.var_correction.get()

            if self.var_use_direct.get():
                Tpc_prime = self.var_tpc_direct.get()
                Ppc_prime = self.var_ppc_direct.get()
            else:
                Tpc_prime, Ppc_prime = corrected_pseudocriticals(
                    gamma, y_CO2, y_H2S, y_N2, correction, pseudo_method
                )

            Tpr = T_R / Tpc_prime

            if self.var_calc_mode.get() == "single":
                P = self.var_p.get()
                Ppr = P / Ppc_prime

                Z_HY, info_hy = hall_yarborough_z(Ppr, Tpr)
                Z_DAK, info_dak = dranchuk_abou_kassem_z(Ppr, Tpr)

                self.last_results = {
                    'mode': 'single',
                    'P': P, 'T_F': T_F, 'T_R': T_R,
                    'gamma': gamma,
                    'y_N2': y_N2, 'y_CO2': y_CO2, 'y_H2S': y_H2S,
                    'pseudo_method': pseudo_method,
                    'correction': correction,
                    'Tpc_prime': Tpc_prime, 'Ppc_prime': Ppc_prime,
                    'Ppr': Ppr, 'Tpr': Tpr,
                    'Z_HY': Z_HY, 'Z_DAK': Z_DAK,
                    'HY_iterations': info_hy['iterations'],
                    'DAK_iterations': info_dak['iterations']
                }

                # Atualizar árvore de resumo
                for item in self.tree_single.get_children():
                    self.tree_single.delete(item)
                self.tree_single.insert("", tk.END, values=("Gás Ideal", "1.000000"))
                self.tree_single.insert("", tk.END, values=("Hall-Yarborough", f"{Z_HY:.6f}"))
                self.tree_single.insert("", tk.END, values=("Dranchuk & Abou-Kassem", f"{Z_DAK:.6f}"))

                details = [
                    "=" * 60, "DADOS DE ENTRADA", "=" * 60,
                    f"Pressão (psia).............. {P:.4f}",
                    f"Temperatura (°F)............ {T_F:.4f}",
                    f"Temperatura (°R)............ {T_R:.4f}",
                    f"Densidade relativa.......... {gamma:.4f}",
                    f"Fração molar N₂............. {y_N2:.4f}",
                    f"Fração molar CO₂............ {y_CO2:.4f}",
                    f"Fração molar H₂S............ {y_H2S:.4f}",
                    "",
                    "PROPRIEDADES PSEUDO-CRÍTICAS",
                    f"Correlação.................. {pseudo_method}",
                    f"Correcção................... {correction}",
                    f"Tpc'........................ {Tpc_prime:.2f} °R",
                    f"Ppc'........................ {Ppc_prime:.2f} psia",
                    f"Pressão reduzida, Ppr....... {Ppr:.4f}",
                    f"Temperatura reduzida, Tpr... {Tpr:.4f}",
                    "",
                    "FATOR DE COMPRESSIBILIDADE Z",
                    "-" * 40,
                    f"Gás Ideal................... 1.000000",
                    f"Hall-Yarborough............. {Z_HY:.6f}",
                    f"Dranchuk & Abou-Kassem..... {Z_DAK:.6f}",
                    "",
                    "ITERAÇÕES",
                    f"Hall-Yarborough............. {info_hy['iterations']} iterações",
                    f"Dranchuk & Abou-Kassem..... {info_dak['iterations']} iterações",
                ]
                self.details_text.config(state=tk.NORMAL)
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, "\n".join(details))
                self.details_text.config(state=tk.DISABLED)

                self.results_notebook.select(self.tab_single)
                # Limpar tabela de malha
                for item in self.mesh_tree.get_children():
                    self.mesh_tree.delete(item)

                if MATPLOTLIB_AVAILABLE:
                    self.update_plot_single()

            else:  # modo malha
                P_start = self.var_p_start.get()
                P_end = self.var_p_end.get()
                n_points = self.var_p_points.get()
                pressures = [P_start + i * (P_end - P_start) / (n_points - 1) for i in range(n_points)]
                Z_HY_list = []
                Z_DAK_list = []

                # Barra de progresso
                progress = ttk.Progressbar(self.results_frame, mode='determinate', maximum=n_points)
                progress.pack(pady=5, fill=tk.X)
                progress_label = ttk.Label(self.results_frame, text="Calculando...")
                progress_label.pack()

                for i, P in enumerate(pressures):
                    Ppr = P / Ppc_prime
                    z_hy, _ = hall_yarborough_z(Ppr, Tpr)
                    z_dak, _ = dranchuk_abou_kassem_z(Ppr, Tpr)
                    Z_HY_list.append(z_hy)
                    Z_DAK_list.append(z_dak)
                    progress['value'] = i + 1
                    self.root.update()

                progress.destroy()
                progress_label.destroy()

                self.last_results = {
                    'mode': 'mesh',
                    'pressures': pressures,
                    'Z_HY': Z_HY_list,
                    'Z_DAK': Z_DAK_list,
                    'T_F': T_F, 'T_R': T_R, 'gamma': gamma,
                    'y_N2': y_N2, 'y_CO2': y_CO2, 'y_H2S': y_H2S,
                    'pseudo_method': pseudo_method,
                    'correction': correction,
                    'Tpc_prime': Tpc_prime, 'Ppc_prime': Ppc_prime,
                    'Tpr': Tpr
                }

                # Preencher tabela de malha
                for item in self.mesh_tree.get_children():
                    self.mesh_tree.delete(item)
                for i, P in enumerate(pressures):
                    self.mesh_tree.insert("", tk.END, values=(f"{P:.2f}", f"{Z_HY_list[i]:.6f}", f"{Z_DAK_list[i]:.6f}"))

                self.results_notebook.select(self.tab_mesh)
                # Limpar resumo single
                for item in self.tree_single.get_children():
                    self.tree_single.delete(item)
                self.details_text.config(state=tk.NORMAL)
                self.details_text.delete(1.0, tk.END)
                self.details_text.config(state=tk.DISABLED)

                if MATPLOTLIB_AVAILABLE:
                    self.update_plot_mesh()

            self.update_sidebar()
            self.status.config(text="Cálculo concluído.")

        except ValueError as e:
            messagebox.showerror("Erro de entrada", str(e))
            self.status.config(text="Erro nos dados de entrada.")
        except Exception as e:
            messagebox.showerror("Erro de cálculo", f"Ocorreu um erro inesperado:\n{str(e)}")
            self.status.config(text="Erro no cálculo.")

    def update_plot_single(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        Tpr = self.last_results['Tpr']
        Ppr_vals = [i * 0.1 for i in range(5, 51)]
        Z_HY_curve = [hall_yarborough_z(ppr, Tpr)[0] for ppr in Ppr_vals]
        Z_DAK_curve = [dranchuk_abou_kassem_z(ppr, Tpr)[0] for ppr in Ppr_vals]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(Ppr_vals, Z_HY_curve, '-', label='Hall-Yarborough (curva)', color='#2c7da0')
        ax.plot(Ppr_vals, Z_DAK_curve, '-', label='Dranchuk & Abou-Kassem (curva)', color='#e63946')
        Ppr = self.last_results['Ppr']
        Z_HY = self.last_results['Z_HY']
        Z_DAK = self.last_results['Z_DAK']
        ax.plot(Ppr, Z_HY, 'ro', markersize=8, label=f'Ponto HY (Ppr={Ppr:.2f})')
        ax.plot(Ppr, Z_DAK, 'go', markersize=8, label=f'Ponto DAK (Ppr={Ppr:.2f})')
        ax.set_xlabel('Pressão Reduzida (Ppr)')
        ax.set_ylabel('Fator Z')
        ax.set_title(f'Comparação dos Fatores Z (Tpr = {Tpr:.3f})')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_plot_mesh(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        pressures = self.last_results['pressures']
        Z_HY = self.last_results['Z_HY']
        Z_DAK = self.last_results['Z_DAK']

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(pressures, Z_HY, 'o-', label='Hall-Yarborough', color='#2c7da0')
        ax.plot(pressures, Z_DAK, 's-', label='Dranchuk & Abou-Kassem', color='#e63946')
        ax.set_xlabel('Pressão (psia)')
        ax.set_ylabel('Fator Z')
        ax.set_title(f'Comparação dos Fatores Z (Tpr = {self.last_results["Tpr"]:.3f})')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def copy_results(self):
        if self.last_results is None:
            self.status.config(text="Nenhum resultado para copiar.")
            return
        if self.last_results['mode'] == 'single':
            text = self.details_text.get(1.0, tk.END).strip()
        else:
            lines = ["Pressão (psia)\tZ_HY\tZ_DAK"]
            for child in self.mesh_tree.get_children():
                values = self.mesh_tree.item(child)['values']
                lines.append(f"{values[0]}\t{values[1]}\t{values[2]}")
            text = "\n".join(lines)
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status.config(text="Resultados copiados.")
        else:
            self.status.config(text="Nada para copiar.")

    def export_to_csv(self):
        if self.last_results is None or self.last_results['mode'] != 'mesh':
            messagebox.showinfo("Exportar", "Nenhuma malha calculada.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            return
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Pressão (psia)", "Z_HY", "Z_DAK"])
                for p, zhy, zdak in zip(self.last_results['pressures'], self.last_results['Z_HY'], self.last_results['Z_DAK']):
                    writer.writerow([p, zhy, zdak])
            self.status.config(text=f"Resultados exportados para {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{str(e)}")

    def clear_results(self):
        for item in self.tree_single.get_children():
            self.tree_single.delete(item)
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state=tk.DISABLED)
        for item in self.mesh_tree.get_children():
            self.mesh_tree.delete(item)
        self.last_results = None
        if MATPLOTLIB_AVAILABLE:
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.plot_frame, text="Clique em 'Calcular' para gerar o gráfico.").pack(pady=50)
        self.status.config(text="Resultados limpos.")
        self.update_sidebar()


if __name__ == "__main__":
    # Prefer the refactored GUI in `src.main` when available; fall back to the
    # legacy GUI defined below if an import or execution error occurs.
    try:
        import sys, os
        HERE = os.path.dirname(os.path.abspath(__file__))
        ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
        from src.main import main as run_main
        run_main()
    except Exception:
        # If the refactored GUI can't be imported/run, fall back to legacy GUI.
        import sys, traceback
        print("Failed to run refactored GUI; falling back to legacy implementation.", file=sys.stderr)
        traceback.print_exc()
        root = tk.Tk()
        app = GasZApp(root)
        root.mainloop()