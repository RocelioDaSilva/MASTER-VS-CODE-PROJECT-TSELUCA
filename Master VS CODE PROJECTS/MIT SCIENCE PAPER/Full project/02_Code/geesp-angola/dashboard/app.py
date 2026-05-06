"""
GEESP-Angola: Dashboard Interativo
Interface Streamlit para visualização e análise de dados MCDA-SIG
"""

import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import io
import logging
from logging.handlers import RotatingFileHandler

# ============================================================================
# LOGGING SETUP
# ============================================================================

# Use shared logging utility
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
try:
    from logging_setup import setup_logging
    logger = setup_logging("geesp_dashboard", log_file="logs/geesp_dashboard.log")
except ImportError:
    # Fallback if utils not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("geesp_dashboard")

# Adiciona scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from mcda_analysis import AHPWeighter, MCDAnalyzer
from lcoe_calculator import LCOECalculator, SolarParameters
import utils

# Load communities
communities_path = (
    Path(__file__).parent.parent / "data" / "processed" / "communities_45.csv"
)
communities_df = (
    pd.read_csv(communities_path) if communities_path.exists() else pd.DataFrame()
)

# ============================================================================
# CONFIG & SETUP
# ============================================================================

st.set_page_config(
    page_title="GEESP-Angola Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Tema customizado
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ============================================================================
# SIDEBAR: NAVEGAÇÃO
# ============================================================================

st.sidebar.markdown("# 🗺️ GEESP-Angola")
st.sidebar.markdown("### Geospatial Energy for Equity and Solar Planning")
st.sidebar.divider()

page = st.sidebar.radio(
    "Selecione uma página:",
    [
        "🏠 Início",
        "📊 Exploração de Dados",
        "🎯 Análise MCDA",
        "📈 Resultados",
        "💰 Calculadora LCOE",
    ],
)

logger.info(f"User navigated to page: {page}")

st.sidebar.divider()
st.sidebar.markdown("### ℹ️ Sobre")
st.sidebar.info("""
    Dashboard para identificação otimizada de locais para sistemas solares
    comunitários em Angola.
    
    **Dados**: NASA POWER, Sentinel-2, VIIRS, SRTM
    
    **Métodos**: AHP, Weighted Overlay, Análise de Sensibilidade
    """)


# ============================================================================
# PÁGINA 1: INÍCIO
# ============================================================================

if page == "🏠 Início":
    logger.info("Loading home page")
    st.markdown("<h1 class='header-title'>GEESP-Angola</h1>", unsafe_allow_html=True)
    st.markdown("### Identificação de Locais Ótimos para Sistemas Solares Comunitários")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ## 🎯 Objetivo
        
        Desenvolver um framework integrado de análise multicritério (MCDA) baseado em SIG
        para identificar locais prioritários e recomendar tecnologias apropriadas para
        sistemas solares comunitários em Angola.
        """)

        st.markdown("""
        ## 📊 Dados Integrados
        
        - **Solar**: NASA POWER (radiação global)
        - **Ambiental**: Sentinel-2 (vegetação), SRTM (topografia)
        - **Demanda**: VIIRS (luzes noturnas), dados censitários
        - **Infraestrutura**: Distância à rede, estradas
        """)

    with col2:
        st.markdown("""
        ## 🔬 Metodologia
        
        1. **Pré-processamento**: Normalização de critérios [0,1]
        2. **AHP**: Ponderação via comparações pareadas
        3. **Weighted Overlay**: Combinação de camadas
        4. **Classificação**: 3 classes de aptidão
        5. **Sensibilidade**: Validação de robustez
        """)

        st.markdown("""
        ## 🌍 Estudo de Caso
        
        **Província da Huíla, Angola**
        - Área: ~34,000 km²
        - População: ~270,000 hab
        - 3 zonas prioritárias identificadas
        """)

    st.divider()

    # Estatísticas do projeto
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Critérios Integrados", "5", "+2 secundários")
    with col2:
        st.metric("Zonas Prioritárias", "3", "Alta aptidão")
    with col3:
        st.metric("População Beneficiada", "~48k", "Zona A+B+C")
    with col4:
        st.metric("LCOE Estimado", "0.18-0.22", "USD/kWh")

    st.divider()

    st.markdown("### 🗺️ Mapa de Localização")

    # Community selector
    if not communities_df.empty:
        comm_names = ["Visão Geral"] + communities_df["name"].tolist()
        selected_comm = st.selectbox("Selecionar Comunidade:", comm_names, index=0)

        if selected_comm != "Visão Geral":
            comm_row = communities_df[communities_df["name"] == selected_comm].iloc[0]
            map_lat = float(comm_row["latitude"])
            map_lon = float(comm_row["longitude"])
            pop = int(comm_row["population_est"])
            st.info(
                f"📍 {selected_comm} | Pop. {pop:,} | [{map_lat:.3f}, {map_lon:.3f}]"
            )
        else:
            map_lat, map_lon = -18.0, 14.75
    else:
        map_lat, map_lon = -18.0, 14.75

    # Cria mapa base
    m = folium.Map(
        location=[map_lat, map_lon],
        zoom_start=8 if selected_comm == "Visão Geral" else 12,
        tiles="OpenStreetMap",
    )

    # Add markers for communities
    if not communities_df.empty:
        # Top 3 zones (Cacula, Humpata, Quilengues) are priority
        priority_names = ["Cacula", "Humpata", "Quilengues"]

        for idx, row in communities_df.iterrows():
            name = row["name"]
            coords = [float(row["latitude"]), float(row["longitude"])]
            pop = int(row["population_est"])

            if name in priority_names:
                color = "orange"
                icon = "info-sign"
            else:
                color = "blue"
                icon = "circle"

            folium.Marker(
                location=coords,
                popup=f"{name}<br>Pop: {pop:,}",
                tooltip=name,
                icon=folium.Icon(color=color, icon=icon),
            ).add_to(m)
    else:
        # Fallback: hard-coded 3 zones
        zonas = {
            "Cacula (Zona A)": [-18.32, 14.88],
            "Humpata (Zona B)": [-17.45, 15.18],
            "Quilengues (Zona C)": [-17.80, 14.55],
        }

        for zona, coords in zonas.items():
            folium.Marker(
                location=coords,
                popup=zona,
                icon=folium.Icon(color="orange", icon="info-sign"),
            ).add_to(m)

    st_folium(m, width=700, height=400)


# ============================================================================
# PÁGINA 2: EXPLORAÇÃO DE DADOS
# ============================================================================

elif page == "📊 Exploração de Dados":
    logger.info("Loading data exploration page")
    st.markdown("# 📊 Exploração de Dados")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        Carregue arquivos raster (GeoTIFF) para análise exploratória.
        """)

        uploaded_files = st.file_uploader(
            "Selecione arquivos GeoTIFF:",
            type=["tif", "tiff"],
            accept_multiple_files=True,
        )

    with col2:
        st.markdown("### 📋 Critérios Disponíveis")
        criteria = st.multiselect(
            "Critérios:",
            [
                "Irradiação Solar",
                "Demanda (Luzes Noturnas)",
                "Acesso (Distância Rede)",
                "Infraestrutura",
            ],
            default=["Irradiação Solar", "Demanda (Luzes Noturnas)"],
        )

    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} arquivo(s) carregado(s)")

        # Simula dados de exemplo se nenhum arquivo
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Estatísticas")

            # Dados simulados
            data = {
                "Critério": ["Irradiação", "Demanda", "Acesso"],
                "Mínimo": [5.5, 10, 0.5],
                "Máximo": [6.4, 95, 45],
                "Média": [6.0, 45, 15],
                "Desvio": [0.3, 25, 10],
            }

            st.dataframe(pd.DataFrame(data), use_container_width=True)

        with col2:
            st.markdown("### Distribuição")

            # Gráfico de distribuição
            fig = go.Figure()
            fig.add_trace(go.Box(y=[5.5, 5.8, 6.0, 6.2, 6.4], name="Irradiação"))
            fig.add_trace(go.Box(y=[10, 30, 45, 60, 95], name="Demanda"))
            st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PÁGINA 3: ANÁLISE MCDA
# ============================================================================

elif page == "🎯 Análise MCDA":
    logger.info("Loading MCDA analysis page")
    st.markdown("# 🎯 Análise Multicritério (MCDA)")

    # Sidebar: Configurar pesos
    st.sidebar.markdown("## ⚙️ Configurar Pesos")

    # Default weights
    default_weights = {
        "Irradiação Solar": 25,
        "Demanda (Luzes Noturnas)": 25,
        "Acesso (Distância Rede)": 20,
        "Infraestrutura": 15,
        "Uso do Solo": 15,
    }

    weights = {}
    for criterion, default in default_weights.items():
        weights[criterion] = st.sidebar.slider(
            f"{criterion}",
            0,
            100,
            default,
            help="Ajuste o peso relativo deste critério",
        )

    # Normaliza pesos para soma = 100%
    total = sum(weights.values())
    weights_normalized = {k: v / total * 100 for k, v in weights.items()}

    # Exibe pesos normalizados
    st.markdown("### 📊 Pesos Dos Critérios (Normalizados)")

    weights_df = pd.DataFrame(
        {
            "Critério": list(weights_normalized.keys()),
            "Peso (%)": list(weights_normalized.values()),
        }
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.bar(
            weights_df,
            x="Critério",
            y="Peso (%)",
            color="Peso (%)",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(weights_df, use_container_width=True)

    # Zone filter and layer toggles
    st.markdown("### 🔎 Filtros & Camadas")
    zone = st.selectbox(
        "Selecionar Zona (para visualização)",
        ["Todas", "Cacula (Zona A)", "Humpata (Zona B)", "Quilengues (Zona C)"],
    )
    layer_options = {
        "Irradiação Solar": "mapa_irradiacao",
        "Demanda (Luzes Noturnas)": "mapa_populacao",
        "Acesso (Distância Rede)": "mapa_distanciarede",
        "Infraestrutura (Declividade)": "mapa_declividade",
        "Uso do Solo (NDVI)": "mapa_ndvi",
    }
    selected_layers = st.multiselect(
        "Mostrar camadas (pré-visualização)",
        list(layer_options.keys()),
        default=list(layer_options.keys())[:2],
    )

    # Sensitivity analysis controls
    st.markdown("### 🔬 Análise de Sensibilidade (por critério)")
    sens_crit = st.selectbox(
        "Critério para Sensibilidade", list(layer_options.keys()), index=0
    )
    sens_range = st.slider("Variação ±%", 0, 50, 20, step=5)
    sens_steps = st.slider("Passo (%)", 1, 20, 5)

    st.divider()

    # Matriz AHP
    st.markdown("### 🔀 Matriz de Comparação AHP (Saaty)")

    if st.checkbox("Mostrar matriz de comparação pareada"):
        criteria_list = list(weights.keys())

        # Cria matriz de exemplo
        matrix_data = np.eye(len(criteria_list))
        matrix_data[0, 1] = 3
        matrix_data[1, 0] = 1 / 3

        st.dataframe(
            pd.DataFrame(matrix_data, index=criteria_list, columns=criteria_list),
            use_container_width=True,
        )

    st.divider()

    # Executar análise
    if st.button("▶️ Executar Análise MCDA", use_container_width=True):
        st.info("Analisando... ⏳")

        with st.spinner("Processando dados..."):
            # Load available maps from data/processed using utils (supports .npy fallback)
            data_dir = Path(__file__).parent.parent / "data" / "processed"
            map_keys = {
                "Irradiação Solar": "mapa_irradiacao",
                "Demanda (Luzes Noturnas)": "mapa_populacao",
                "Acesso (Distância Rede)": "mapa_distanciarede",
                "Infraestrutura": "mapa_declividade",
                "Uso do Solo": "mapa_ndvi",
            }

            loaded = {}
            for crit, fname in map_keys.items():
                p = data_dir / f"{fname}.npy"
                try:
                    arr, meta = utils.load_raster(str(p))
                    loaded[crit] = np.array(arr, dtype=float)
                except Exception:
                    # skip missing maps
                    continue

            if not loaded:
                st.error("Nenhum mapa disponível em data/processed para executar MCDA.")
            else:
                # Normalize each raster to [0,1]
                normed = {}
                for k, a in loaded.items():
                    valid = np.isfinite(a)
                    if valid.any():
                        amin = float(np.nanmin(a))
                        amax = float(np.nanmax(a))
                        norm = (a - amin) / (amax - amin + 1e-9)
                        normed[k] = np.nan_to_num(norm)
                    else:
                        normed[k] = np.zeros_like(a)

                # Convert sidebar weights to fractions summing to 1
                frac_weights = {k: (weights[k] / total) for k in weights.keys()}

                # Compute weighted overlay
                overlay = None
                for crit, arr in normed.items():
                    w = frac_weights.get(crit, 0.0)
                    if overlay is None:
                        overlay = w * arr
                    else:
                        overlay = overlay + w * arr

                # Ensure overlay is an ndarray (not None) for downstream ops
                import numpy as _np

                overlay = _np.asarray(overlay)
                overlay = np.nan_to_num(overlay)

                # Save overlay numpy and attempt GeoTIFF via utils.save_raster
                out_npy = data_dir / "mapa_aptidao_integrada.npy"
                np.save(out_npy, overlay)
                try:
                    utils.save_raster(
                        overlay, str(data_dir / "mapa_aptidao_integrada.tif")
                    )
                    logger.info("✓ GeoTIFF salvo com sucesso")
                except Exception as e:
                    # Log instead of silently passing so failures are visible
                    logger.warning(
                        f"Não foi possível salvar GeoTIFF (rasterio ausente ou erro): {e}"
                    )

                # Create PNG visualization in-memory
                fig, ax = plt.subplots(figsize=(6, 4))
                im = ax.imshow(overlay, cmap="viridis")
                ax.set_title("Mapa de Aptidão Integrada (MCDA)")
                fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight")
                plt.close(fig)
                buf.seek(0)

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.success("✓ Análise concluída com sucesso!")
                    st.metric("Pixels válidos", f"{np.isfinite(overlay).sum()}")
                    st.image(buf.getvalue(), use_column_width=True)

                    # Download buttons
                    st.download_button(
                        label="📥 Baixar overlay (.npy)",
                        data=open(out_npy, "rb").read(),
                        file_name="mapa_aptidao_integrada.npy",
                        mime="application/octet-stream",
                    )
                    st.download_button(
                        label="📥 Baixar overlay (.png)",
                        data=buf.getvalue(),
                        file_name="mapa_aptidao_integrada.png",
                        mime="image/png",
                    )

                with col2:
                    # Summary statistics
                    st.markdown("### Estatísticas")
                    st.write(
                        {
                            "min": float(np.min(overlay)),
                            "max": float(np.max(overlay)),
                            "mean": float(np.mean(overlay)),
                        }
                    )

                    # Recommend technology using LCOECalculator (area mean irradiance -> annual)
                    try:
                        irr_map = loaded.get("Irradiação Solar")
                        if irr_map is not None:
                            mean_daily = float(np.nanmean(irr_map))
                            annual_irr = mean_daily * 365.0
                        else:
                            annual_irr = 2226

                        calc = LCOECalculator(location="Huíla")
                        comp = calc.compare_technologies(
                            capacity_mw=1.0, annual_irradiance=annual_irr
                        )
                        # pick lowest LCOE
                        best = comp.sort_values("lcoe_usd_per_kwh").iloc[0]
                        st.markdown("### 🔧 Recomendação Tecnológica")
                        st.markdown(
                            f"**{best['technology_name']}** — LCOE ≈ {best['lcoe_usd_per_kwh']:.3f} USD/kWh"
                        )
                    except Exception as e:
                        st.warning(
                            f"Não foi possível calcular recomendação tecnológica: {e}"
                        )

        # Sensitivity analysis execution (runs after overlay created)
        if st.button("▶️ Executar Sensibilidade para critério selecionado"):
            # build range of perturbations
            deltas = list(range(-sens_range, sens_range + 1, sens_steps))
            results = []
            base_weights = {k: weights[k] / total for k in weights.keys()}
            for d in deltas:
                # adjust selected criterion by d% and renormalize
                adj = base_weights.copy()
                key_name = sens_crit
                adj[key_name] = max(0.0, adj.get(key_name, 0.0) * (1 + d / 100.0))
                s = sum(adj.values())
                if s == 0:
                    normed_w = {k: 0.0 for k in adj.keys()}
                else:
                    normed_w = {k: v / s for k, v in adj.items()}

                # compute overlay mean using normed_w and available normed maps
                o = None
                for crit_name, arr in normed.items():
                    w = normed_w.get(crit_name, 0.0)
                    if o is None:
                        o = w * arr
                    else:
                        o = o + w * arr
                mean_val = float(np.nanmean(o)) if o is not None else 0.0
                results.append({"delta": d, "mean": mean_val})

            df = pd.DataFrame(results)
            fig2 = px.line(df, x="delta", y="mean", title=f"Sensibilidade: {sens_crit}")
            st.plotly_chart(fig2, use_container_width=True)


# ============================================================================
# PÁGINA 4: RESULTADOS
# ============================================================================

elif page == "📈 Resultados":
    logger.info("Loading results page")
    st.markdown("# 📈 Resultados MCDA-SIG")

    # Sumário das 3 zonas
    st.markdown("## 🎯 Zonas Prioritárias Identificadas")

    zones_data = {
        "Zona": ["A - Cacula", "B - Humpata", "C - Quilengues"],
        "Área (km²)": [850, 620, 720],
        "Aptidão Média": [0.83, 0.79, 0.76],
        "Irradiação (kWh/m²/dia)": [6.1, 6.3, 5.9],
        "População": ["45k", "52k", "38k"],
        "Prioridade": ["🔴 Crítica", "🟠 Alta", "🟡 Média"],
    }

    zones_df = pd.DataFrame(zones_data)
    st.dataframe(zones_df, use_container_width=True, hide_index=True)

    st.divider()

    # Comparação tecnológica
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💡 Recomendações Tecnológicas por Zona")

        tech_recs = {
            "Zona": ["A - Cacula", "B - Humpata", "C - Quilengues"],
            "Tecnologia Recomendada": [
                "PV Fixo + Baterias",
                "PV com Rastreador",
                "Híbrido Solar+Diesel",
            ],
            "LCOE (USD/kWh)": ["0.18-0.22", "0.22-0.28", "0.25-0.35"],
        }

        st.dataframe(pd.DataFrame(tech_recs), use_container_width=True)

    with col2:
        st.markdown("### 📊 Análise de Sensibilidade")

        # Simula variação de pesos
        sensitivity_data = {
            "Variação": ["-20%", "-10%", "0%", "+10%", "+20%"],
            "Aptidão Média Zona A": [0.81, 0.82, 0.83, 0.84, 0.85],
            "Robustez": ["Robusta"] * 5,
        }

        fig = px.line(
            pd.DataFrame(sensitivity_data),
            x="Variação",
            y="Aptidão Média Zona A",
            title="Sensibilidade: Variação de Peso ±20%",
        )
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PÁGINA 5: CALCULADORA LCOE
# ============================================================================

elif page == "💰 Calculadora LCOE":
    logger.info("Loading LCOE calculator page")
    st.markdown("# 💰 Calculadora de LCOE")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ Parâmetros")

        # Inputs
        capacity = st.number_input(
            "Capacidade (MW):", min_value=0.1, max_value=100.0, value=1.0, step=0.1
        )

        irradiance = st.number_input(
            "Irradiância Anual (kWh/m²/ano):",
            min_value=1000,
            max_value=3000,
            value=2226,
            step=50,
        )

        discount_rate = st.slider(
            "Taxa de Desconto (%):", min_value=1, max_value=15, value=8
        )

        lifetime = st.slider("Vida Útil (anos):", min_value=10, max_value=40, value=25)

        technology = st.selectbox(
            "Tecnologia:",
            ["PV Fixo + Baterias", "PV com Rastreador", "Híbrido Solar+Diesel"],
        )

    with col2:
        # Executar cálculo
        if st.button("Calcular LCOE", use_container_width=True, type="primary"):
            calculator = LCOECalculator(location="Angola")

            comparison = calculator.compare_technologies(
                capacity_mw=capacity,
                annual_irradiance=irradiance,
                discount_rate=discount_rate,
                lifetime=lifetime,
            )

            # Resultados
            st.markdown("### 📊 Resultados")

            fig = px.bar(
                comparison,
                x="technology_name",
                y="lcoe_usd_per_kwh",
                color="lcoe_usd_per_kwh",
                color_continuous_scale="RdYlGn_r",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabela detalhada
            st.markdown("### 📋 Comparação Detalhada")

            display_cols = [
                "technology_name",
                "capex_per_kw",
                "annual_generation_mwh",
                "lcoe_usd_per_mwh",
                "lcoe_usd_per_kwh",
            ]

            st.dataframe(
                comparison[display_cols].rename(
                    columns={
                        "technology_name": "Tecnologia",
                        "capex_per_kw": "CAPEX (USD/kW)",
                        "annual_generation_mwh": "Geração Anual (MWh)",
                        "lcoe_usd_per_mwh": "LCOE (USD/MWh)",
                        "lcoe_usd_per_kwh": "LCOE (USD/kWh)",
                    }
                ),
                use_container_width=True,
            )


# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown(
    """
<div style='text-align: center; color: #888; font-size: 0.9em; margin-top: 3rem;'>
    <p>GEESP-Angola Dashboard | Desenvolvido para MIT Climate Portal 2026</p>
    <p>Autores: Rocélio Da Silva, Alexandre Dos Santos, Delfina Mpanka (ISPTEC)</p>
</div>
""",
    unsafe_allow_html=True,
)
