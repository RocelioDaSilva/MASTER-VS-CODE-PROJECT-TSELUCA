"""
GEESP-Angola: Dashboard Interativo (Refactored - Modular)
Interface Streamlit para visualização e análise de dados MCDA-SIG
"""

import streamlit as st
import sys
import logging
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent / "utils"))
sys.path.insert(0, str(Path(__file__).parent / "pages"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# ============================================================================
# LOGGING SETUP
# ============================================================================

try:
    from logging_setup import setup_logging
    logger = setup_logging("geesp_dashboard", log_file="logs/geesp_dashboard.log")
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("geesp_dashboard")

# Import utilities
from session_state import SessionState
from page_router import PageRouter

# Import pages
import home
import data_explore
import mcda
import results
import lcoe

# ============================================================================
# CONFIG & SETUP
# ============================================================================

st.set_page_config(
    page_title="GEESP-Angola Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
SessionState.init()

# Custom theme
st.markdown(
    """
    <style>
    .main { background-color: #f5f5f5; }
    .header-title { color: #1f77b4; font-size: 2.5em; font-weight: bold; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px;
                   box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("# 🗺️ GEESP-Angola")
st.sidebar.markdown("### Geospatial Energy for Equity and Solar Planning")
st.sidebar.divider()

pages_list = [
    ("🏠 Início", home.render),
    ("📊 Exploração de Dados", data_explore.render),
    ("🎯 Análise MCDA", mcda.render),
    ("📈 Resultados", results.render),
    ("💰 Calculadora LCOE", lcoe.render),
]

page_names = [name for name, _ in pages_list]
selected_page = st.sidebar.radio("Selecione uma página:", page_names)

logger.info(f"User navigated to: {selected_page}")

st.sidebar.divider()
st.sidebar.markdown("### ℹ️ Sobre")
st.sidebar.info("""
    Dashboard para identificação otimizada de locais para sistemas solares
    comunitários em Angola.
    
    **Dados**: NASA POWER, Sentinel-2, VIIRS, SRTM
    
    **Métodos**: AHP, Weighted Overlay, Análise de Sensibilidade
""")

# ============================================================================
# PAGE RENDERING
# ============================================================================

# Create router and register pages
router = PageRouter()
for name, render_func in pages_list:
    router.register(name, render_func)

# Render current page
router.render(selected_page)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown(
    """
<div style='text-align: center; color: #888; font-size: 0.9em; margin-top: 3rem;'>
    <p>GEESP-Angola Dashboard | Desenvolvido para MIT Climate Portal 2026</p>
    <p>Autores: Rocélio Da Silva, Alexandre Dos Santos, Delfina Mpanka (ISPTEC)</p>
    <p style='font-size: 0.8em; margin-top: 1rem;'>Architecture: Modular 6-page design | Test coverage: In progress</p>
</div>
""",
    unsafe_allow_html=True,
)
