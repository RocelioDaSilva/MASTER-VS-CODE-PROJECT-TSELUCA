"""
Page: Home (🏠 Início)
Project overview and introduction
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "components"))
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from metrics_card import MetricsCard
from map_viewer import MapViewer


def render():
    """Render home page"""
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
    communities_path = Path(__file__).parent.parent.parent / "data" / "processed" / "communities_45.csv"
    
    try:
        communities_df = pd.read_csv(communities_path)
        comm_names = ["Visão Geral"] + communities_df["name"].tolist()
        selected_comm = st.selectbox("Selecionar Comunidade:", comm_names, index=0)
        
        if selected_comm != "Visão Geral":
            comm_row = communities_df[communities_df["name"] == selected_comm].iloc[0]
            map_center = (float(comm_row["latitude"]), float(comm_row["longitude"]))
            map_zoom = 12
            pop = int(comm_row["population_est"])
            st.info(f"📍 {selected_comm} | Pop. {pop:,}")
        else:
            map_center = (-18.0, 14.75)
            map_zoom = 8
        
        # Render map
        mapper = MapViewer(center=map_center, zoom=map_zoom)
        priority_zones = ["Cacula", "Humpata", "Quilengues"]
        mapper.add_markers(communities_df, priority_zones)
        mapper.render()
except FileNotFoundError:
        st.warning("⚠️ Arquivo de comunidades não encontrado. Exibindo mapa padrão.")
        mapper = MapViewer()
        mapper.render()
