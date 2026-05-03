"""
Page: Data Exploration (📊 Exploração de Dados)
Raster data upload and analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render():
    """Render data exploration page"""
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
            st.markdown("### 📊 Distribuição")

            # Distribution plot
            fig = go.Figure()
            fig.add_trace(go.Box(y=[5.5, 5.8, 6.0, 6.2, 6.4], name="Irradiação"))
            fig.add_trace(go.Box(y=[10, 30, 45, 60, 95], name="Demanda"))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Carregue um arquivo para começar a análise exploratória.")
        with col2:
            st.markdown("### Distribuição")

            fig = go.Figure()
            fig.add_trace(go.Box(y=[5.5, 5.8, 6.0, 6.2, 6.4], name="Irradiação"))
            fig.add_trace(go.Box(y=[10, 30, 45, 60, 95], name="Demanda"))
            st.plotly_chart(fig, use_container_width=True)
