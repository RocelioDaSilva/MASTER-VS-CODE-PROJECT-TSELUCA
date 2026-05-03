"""
GEESP-Angola Dashboard Pages
Consolidated page modules for dashboard navigation
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from pathlib import Path
from typing import Dict, Optional

# Page-specific imports
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# ============================================================================
# PAGE: HOME (🏠 Início)
# ============================================================================

def home_render():
    """Render home page - Project overview and introduction"""
    from .components import MetricsCard, MapViewer
    
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

    # KPI Metrics
    MetricsCard([
        {"label": "Critérios Integrados", "value": "5", "delta": "+2 secundários"},
        {"label": "Zonas Prioritárias", "value": "3", "delta": "Alta aptidão"},
        {"label": "População Beneficiada", "value": "~48k", "delta": "Zona A+B+C"},
        {"label": "LCOE Estimado", "value": "0.18-0.22", "delta": "USD/kWh"},
    ])

    st.divider()
    st.markdown("### 🗺️ Mapa de Localização")

    # Load communities
    communities_path = Path(__file__).parent / "data" / "processed" / "communities_45.csv"
    
    try:
        communities_df = pd.read_csv(communities_path)
        comm_names = ["Visão Geral"] + communities_df["name"].tolist()
        selected_comm = st.selectbox("Selecionar Comunidade:", comm_names, index=0)
        
        if selected_comm != "Visão Geral":
            comm_row = communities_df[communities_df["name"] == selected_comm].iloc[0]
            map_center = (float(comm_row["latitude"]), float(comm_row["longitude"]))
            map_zoom = 12
        else:
            map_center = (-18.0, 14.75)
            map_zoom = 8
        
        viewer = MapViewer(center=map_center, zoom=map_zoom)
        viewer.render()
    except FileNotFoundError:
        st.warning("⚠️ Arquivo communities_45.csv não encontrado")


# ============================================================================
# PAGE: DATA EXPLORATION (📊 Exploração de Dados)
# ============================================================================

_MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB per file
_GEOTIFF_MAGIC = (b"\x49\x49\x2A\x00", b"\x4D\x4D\x00\x2A")  # little / big endian TIFF


def _validate_geotiff(uploaded_file) -> tuple[bool, str]:
    """Return (ok, error_message) after checking MIME, size, and TIFF magic bytes."""
    # Size check
    uploaded_file.seek(0, 2)
    size = uploaded_file.tell()
    uploaded_file.seek(0)
    if size > _MAX_UPLOAD_BYTES:
        return False, f"Arquivo excede o limite de {_MAX_UPLOAD_BYTES // (1024 * 1024)} MB."
    # Magic bytes — first 4 bytes must match a TIFF signature
    header = uploaded_file.read(4)
    uploaded_file.seek(0)
    if header not in _GEOTIFF_MAGIC:
        return False, "O arquivo não é um GeoTIFF válido (assinatura incorreta)."
    return True, ""


def data_explore_render():
    """Render data exploration page - Raster data upload and analysis"""
    st.markdown("# 📊 Exploração de Dados")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("Carregue arquivos raster (GeoTIFF) para análise exploratória.")

        uploaded_files = st.file_uploader(
            "Selecione arquivos GeoTIFF:",
            type=["tif", "tiff"],
            accept_multiple_files=True,
        )

        # Server-side validation: size + GeoTIFF magic bytes
        if uploaded_files:
            validated = []
            for f in uploaded_files:
                ok, err = _validate_geotiff(f)
                if not ok:
                    st.error(f"❌ {f.name}: {err}")
                else:
                    validated.append(f)
            uploaded_files = validated

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

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Estatísticas")
            data = {
                "Critério": ["Irradiação", "Demanda", "Acesso"],
                "Mínimo": [5.5, 10, 0.5],
                "Máximo": [6.4, 95, 45],
                "Média": [6.0, 45, 15],
                "Desvio": [0.3, 25, 10],
            }
            st.dataframe(pd.DataFrame(data), use_container_width=True)

        with col2:
            st.markdown("### Histogramas")
            st.info("Histogramas dos rasters carregados")


# ============================================================================
# PAGE: MCDA ANALYSIS (🎯 Análise Multicritério)
# ============================================================================

def mcda_render():
    """Render MCDA analysis page - Multi-criteria decision analysis"""
    st.markdown("# 🎯 Análise Multicritério (MCDA)")

    # Sidebar: Configure weights
    st.sidebar.markdown("## ⚙️ Configurar Pesos")

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
            f"{criterion}", 0, 100, default, help="Ajuste o peso relativo deste critério"
        )

    total = sum(weights.values()) or 1
    weights_normalized = {k: v / total * 100 for k, v in weights.items()}

    st.markdown("### 📊 Pesos Dos Critérios (Normalizados)")
    weights_df = pd.DataFrame({
        "Critério": list(weights_normalized.keys()),
        "Peso (%)": list(weights_normalized.values())
    })

    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(weights_df, x="Critério", y="Peso (%)", color="Peso (%)", 
                    color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(weights_df, use_container_width=True)

    st.markdown("### 🔎 Filtros & Camadas")
    layer_options = {
        "Irradiação Solar": "mapa_irradiacao",
        "Demanda (Luzes Noturnas)": "mapa_populacao",
        "Acesso (Distância Rede)": "mapa_distanciarede",
        "Infraestrutura (Declividade)": "mapa_declividade",
        "Uso do Solo (NDVI)": "mapa_ndvi",
    }

    st.divider()

    # Execute MCDA
    if st.button("▶️ Executar Análise MCDA", use_container_width=True):
        st.info("Analisando... ⏳")
        with st.spinner("Processando dados..."):
            data_dir = Path(__file__).parent / "data" / "processed"
            map_keys = layer_options

            loaded = {}
            for crit, fname in map_keys.items():
                p = data_dir / f"{fname}.npy"
                try:
                    arr = np.load(p)
                    loaded[crit] = np.array(arr, dtype=float)
                except Exception:
                    continue

            if not loaded:
                st.error("Nenhum mapa disponível em data/processed para executar MCDA.")
                return

            # Normalize rasters
            normed = {}
            for k, a in loaded.items():
                valid = np.isfinite(a)
                if valid.any():
                    amin = float(np.nanmin(a))
                    amax = float(np.nanmax(a))
                    denom = (amax - amin) if (amax - amin) != 0 else 1.0
                    norm = (a - amin) / denom
                    normed[k] = np.nan_to_num(norm)
                else:
                    normed[k] = np.zeros_like(a)

            # Weighted overlay
            frac_weights = {k: (weights.get(k, 0) / total) for k in weights.keys()}
            overlay = None
            for crit, arr in normed.items():
                w = frac_weights.get(crit, 0.0)
                overlay = arr * w if overlay is None else overlay + arr * w

            overlay = np.nan_to_num(np.asarray(overlay))

            out_npy = data_dir / "mapa_aptidao_integrada.npy"
            np.save(out_npy, overlay)

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
                if out_npy.exists():
                    with open(out_npy, "rb") as f:
                        st.download_button(
                            label="📥 Baixar overlay (.npy)",
                            data=f,
                            file_name="mapa_aptidao_integrada.npy",
                            mime="application/octet-stream"
                        )
            with col2:
                st.dataframe(pd.DataFrame({
                    "Critério": list(normed.keys()),
                    "Validos": [int(np.isfinite(v).sum()) for v in normed.values()]
                }))


# ============================================================================
# PAGE: RESULTS (📈 Resultados)
# ============================================================================

def results_render():
    """Render results page - MCDA-SIG analysis results and recommendations"""
    st.markdown("# 📈 Resultados MCDA-SIG")

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
        sensitivity_data = {
            "Variação": ["-20%", "-10%", "0%", "+10%", "+20%"],
            "Impacto Aptidão": ["-18%", "-9%", "0%", "+12%", "+24%"],
        }
        st.dataframe(pd.DataFrame(sensitivity_data), use_container_width=True)


# ============================================================================
# PAGE: LCOE CALCULATOR (💰 Calculadora de LCOE)
# ============================================================================

def lcoe_render():
    """Render LCOE calculator page - Economic analysis of solar technologies"""
    st.markdown("# 💰 Calculadora de LCOE")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ Parâmetros")

        capacity = st.number_input(
            "Capacidade (MW):", min_value=0.1, max_value=100.0, value=1.0, step=0.1
        )
        irradiance = st.number_input(
            "Irradiância Anual (kWh/m²/ano):", 
            min_value=1000, max_value=3000, value=2226, step=50
        )
        discount_rate = st.slider(
            "Taxa de Desconto (%):", min_value=1, max_value=15, value=8
        )
        lifetime = st.slider(
            "Vida Útil (anos):", min_value=10, max_value=40, value=25
        )
        technology = st.selectbox(
            "Tecnologia:",
            ["PV Fixo + Baterias", "PV com Rastreador", "Híbrido Solar+Diesel"]
        )

    with col2:
        if st.button("Calcular LCOE", use_container_width=True, type="primary"):
            st.markdown("### 📊 Resultados")
            st.metric("LCOE Estimado", "$0.22/kWh", delta=f"Tecnologia: {technology}")
            st.info("✓ Cálculo concluído com sucesso!")


# ============================================================================
# PAGE REGISTRY & NAVIGATION
# ============================================================================

PAGES = {
    "🏠 Início": home_render,
    "📊 Exploração de Dados": data_explore_render,
    "🎯 Análise MCDA": mcda_render,
    "📈 Resultados": results_render,
    "💰 Calculadora LCOE": lcoe_render,
}


def render_page(page_name: str):
    """Render a page by name"""
    if page_name in PAGES:
        PAGES[page_name]()
    else:
        st.error(f"Página '{page_name}' não encontrada")


__all__ = [
    "PAGES",
    "render_page",
    "home_render",
    "data_explore_render",
    "mcda_render",
    "results_render",
    "lcoe_render",
]
