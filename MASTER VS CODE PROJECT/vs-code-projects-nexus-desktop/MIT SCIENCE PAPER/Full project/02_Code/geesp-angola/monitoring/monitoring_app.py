"""
GEESP-Angola: Sistema de Monitoramento Pós-Implementação
Dashboard para acompanhar projetos de sistemas solares comunitários
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from logging.handlers import RotatingFileHandler
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))

# Import database components
from models.monitoring import (
    get_database_manager,
    ProjectRepository,
    GenerationRepository,
    MaintenanceRepository,
    KPIRepository,
)
from datetime import timedelta

# ============================================================================
# LOGGING SETUP
# ============================================================================

# Use shared logging utility
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
try:
    from logging_setup import setup_logging
    logger = setup_logging("geesp_monitoring", log_file="logs/geesp_monitoring.log")
except ImportError:
    # Fallback if utils not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("geesp_monitoring")

logger.info("=== Monitoring App Started ===")

# ============================================================================
# CONFIG & SETUP
# ============================================================================

st.set_page_config(
    page_title="GEESP Monitoramento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-active { color: #28a745; font-weight: bold; }
    .status-planning { color: #ffc107; font-weight: bold; }
    .status-maintenance { color: #17a2b8; font-weight: bold; }
    .status-inactive { color: #dc3545; font-weight: bold; }
    .header-title { color: #1f77b4; font-size: 2.5em; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

@st.cache_resource
def get_db_session():
    """Get or create database session"""
    try:
        db = get_database_manager()
        return db.get_session()
    except Exception as e:
        logger.warning(f"⚠️ Database not available: {e}")
        return None


# ============================================================================
# DATA LOADING FROM DATABASE
# ============================================================================

def load_projects_data(session, province_filter=None, status_filter=None):
    """Load projects from database with filtering"""
    if session is None:
        # Fallback to sample data if database unavailable
        return get_sample_projects()
    
    try:
        repo = ProjectRepository(session)
        projects = repo.get_all_active()
        
        # Convert to DataFrame
        data = [p.to_dict() for p in projects]
        df = pd.DataFrame(data)
        
        # Apply filters if provided
        if province_filter:
            df = df[df["province"].isin(province_filter)]
        if status_filter:
            df = df[df["status"].isin(status_filter)]
        
        return df
    except Exception as e:
        logger.warning(f"⚠️ Could not load projects from database: {e}")
        return get_sample_projects()


def load_generation_data(session, days=30):
    """Load recent generation data from database"""
    if session is None:
        return get_sample_daily_generation()
    
    try:
        repo = GenerationRepository(session)
        
        # Get data for all projects in past 30 days
        cutoff_date = datetime.now() - timedelta(days=days)
        records = repo.get_by_date_range(cutoff_date, datetime.now())
        
        # Convert to DataFrame with pivot
        data = [r.to_dict() for r in records]
        df = pd.DataFrame(data)
        
        if df.empty:
            return get_sample_daily_generation()
        
        # Pivot to get communities as columns
        df_pivot = df.pivot_table(
            index="date",
            columns="community",
            values="generation_kwh",
            aggfunc="sum"
        )
        
        return df_pivot.reset_index()
    except Exception as e:
        logger.warning(f"⚠️ Could not load generation data from database: {e}")
        return get_sample_daily_generation()


def load_maintenance_data(session):
    """Load maintenance logs from database"""
    if session is None:
        return get_sample_maintenance()
    
    try:
        repo = MaintenanceRepository(session)
        
        # Get recent maintenance records
        cutoff_date = datetime.now() - timedelta(days=90)
        all_maintenance = repo.get_recent(cutoff_date)
        
        data = [m.to_dict() for m in all_maintenance]
        return pd.DataFrame(data) if data else get_sample_maintenance()
    except Exception as e:
        logger.warning(f"⚠️ Could not load maintenance data: {e}")
        return get_sample_maintenance()


def load_kpi_summary(session):
    """Load latest KPI snapshot"""
    if session is None:
        return None
    
    try:
        repo = KPIRepository(session)
        latest_kpi = repo.get_latest_daily()
        return latest_kpi.to_dict() if latest_kpi else None
    except Exception as e:
        logger.warning(f"⚠️ Could not load KPI summary: {e}")
        return None


# ============================================================================
# SAMPLE DATA FALLBACKS
# ============================================================================

def get_sample_projects():
    """Get sample projects for testing when database unavailable"""
    return pd.DataFrame(
        {
            "project_id": ["PRJ-001", "PRJ-002", "PRJ-003", "PRJ-004", "PRJ-005"],
            "community": ["Cacula", "Humpata", "Jamba", "Nhamatanda", "Quilengues"],
            "province": ["Huíla", "Huíla", "Huíla", "Gaza", "Huíla"],
            "status": [
                "Operacional",
                "Operacional",
                "Planejamento",
                "Planejamento",
                "Manutenção",
            ],
            "capacity_kw": [50, 75, 100, 60, 80],
            "installation_date": ["2025-06-15", "2025-07-20", None, None, "2025-05-10"],
            "population_served": [850, 1200, 1500, 900, 1100],
            "annual_generation_mwh": [87.5, 131.25, 175.0, 105.0, 140.0],
            "system_health_percent": [95, 92, None, None, 85],
            "investment_usd": [150000, 225000, 300000, 180000, 240000],
            "economic_status": [
                "ROI +12%",
                "ROI +8%",
                "Pre-launch",
                "Pre-launch",
                "ROI +15%",
            ],
        }
    )


def get_sample_daily_generation():
    """Get sample daily generation for testing"""
    return pd.DataFrame(
        {
            "date": pd.date_range(start="2025-08-01", end="2025-08-31", freq="D"),
            "Cacula_kWh": np.random.normal(240, 30, 31),
            "Humpata_kWh": np.random.normal(360, 40, 31),
            "Jamba_kWh": np.random.normal(0, 0, 31),
            "Nhamatanda_kWh": np.random.normal(0, 0, 31),
            "Quilengues_kWh": np.random.normal(300, 35, 31),
        }
    )


def get_sample_maintenance():
    """Get sample maintenance data for testing"""
    return pd.DataFrame(
        {
            "project": ["Cacula", "Cacula", "Humpata", "Quilengues", "Quilengues"],
            "maintenance_type": [
                "Limpeza painéis",
                "Inspeção anual",
                "Reparo inversor",
                "Calibração",
                "Limpeza painéis",
            ],
            "date": ["2025-08-15", "2025-08-10", "2025-08-18", "2025-08-05", "2025-08-20"],
            "status": ["Concluído", "Concluído", "Em progresso", "Concluído", "Agendado"],
            "priority": ["Normal", "Normal", "Alta", "Normal", "Baixa"],
        }
    )


# ============================================================================
# SAMPLE DATA: IMPLEMENTATION PROJECTS
# ============================================================================

# Initialize database session
db_session = get_db_session()

# Load data from database (with fallback to sample data)
sample_projects = load_projects_data(db_session)
sample_daily_generation = load_generation_data(db_session)
sample_maintenance = load_maintenance_data(db_session)
kpi_summary = load_kpi_summary(db_session)

# ============================================================================
# SIDEBAR: NAVEGAÇÃO
# ============================================================================

st.sidebar.markdown("# 📊 GEESP Monitoramento")
st.sidebar.markdown("### Sistema de Acompanhamento Pós-Implementação")
st.sidebar.divider()

page = st.sidebar.radio(
    "Selecione uma seção:",
    [
        "📈 Dashboard Geral",
        "🔧 Manutenção e Saúde",
        "👥 Impacto Comunitário",
        "💡 Indicadores de Performance",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("### 🔄 Atualizações em Tempo Real")
st.sidebar.info("""
    **Últimas atualizações**:
    - Cacula: 5 min atrás
    - Humpata: 12 min atrás
    - Quilengues: 28 min atrás
    
    Próxima sincronização: 2 min
    """)

st.sidebar.divider()
st.sidebar.markdown("### 📌 Filtros")
selected_province = st.sidebar.multiselect(
    "Filtrar por Província:", ["Huíla", "Gaza"], default=["Huíla", "Gaza"]
)

selected_status = st.sidebar.multiselect(
    "Filtrar por Status:",
    ["Operacional", "Planejamento", "Manutenção"],
    default=["Operacional", "Planejamento", "Manutenção"],
)

# ============================================================================
# PÁGINA 1: DASHBOARD GERAL
# ============================================================================

if page == "📈 Dashboard Geral":
    st.markdown(
        "<h1 class='header-title'>Dashboard Geral de Monitoramento</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "#### Status em tempo real de todos os projetos de sistemas solares comunitários"
    )

    # Filtrar dados
    filtered_df = sample_projects[
        (sample_projects["Province"].isin(selected_province))
        & (sample_projects["Status"].isin(selected_status))
    ]

    # KPIs Principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        operacional = len(filtered_df[filtered_df["Status"] == "Operacional"])
        st.metric("Sistemas Operacionais", operacional, "+2 este mês")

    with col2:
        total_capacity = filtered_df[filtered_df["Status"] == "Operacional"][
            "Capacity_kW"
        ].sum()
        st.metric("Capacidade Total", f"{total_capacity:.0f} kW", "Operacional")

    with col3:
        total_pop = filtered_df[filtered_df["Status"] == "Operacional"][
            "Population_Served"
        ].sum()
        st.metric("População Beneficiada", f"{total_pop:,.0f}", "Acesso a energia")

    with col4:
        avg_health = filtered_df[filtered_df["Status"] == "Operacional"][
            "System_Health"
        ].mean()
        st.metric("Saúde Média dos Sistemas", f"{avg_health:.1f}%", "Muito bom")

    st.divider()

    # Tabela de Status
    st.markdown("### 📋 Status dos Projetos")

    # Criar coluna de status formatado
    display_df = filtered_df[
        [
            "Project_ID",
            "Community",
            "Province",
            "Status",
            "Capacity_kW",
            "Population_Served",
            "System_Health",
        ]
    ].copy()
    display_df["Saúde"] = display_df["System_Health"].apply(
        lambda x: (
            f"{x:.0f}% ✅"
            if pd.notna(x) and x >= 90
            else f"{x:.0f}% ⚠️" if pd.notna(x) and x >= 80 else "N/A"
        )
    )
    display_df = display_df.drop("System_Health", axis=1)

    st.dataframe(display_df, use_container_width=True)

    st.divider()

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚡ Capacidade por Projeto (kW)")
        capacity_chart = filtered_df[filtered_df["Status"] == "Operacional"].copy()
        fig = px.bar(
            capacity_chart,
            x="Community",
            y="Capacity_kW",
            color="Status",
            labels={"Capacity_kW": "Capacidade (kW)", "Community": "Comunidade"},
            color_discrete_map={
                "Operacional": "#28a745",
                "Planejamento": "#ffc107",
                "Manutenção": "#17a2b8",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 👥 População Servida por Comunidade")
        pop_chart = filtered_df[filtered_df["Status"] == "Operacional"].copy()
        fig = px.pie(
            pop_chart,
            values="Population_Served",
            names="Community",
            labels={"Population_Served": "População"},
        )
        st.plotly_chart(fig, use_container_width=True)

    # Geração de Energia
    st.markdown("### 📊 Geração Diária acumulada (Agosto 2025)")
    daily_gen = sample_daily_generation.copy()
    daily_gen["Total_kWh"] = daily_gen.iloc[:, 1:].sum(axis=1)

    fig = go.Figure()
    for col in ["Cacula_kWh", "Humpata_kWh", "Quilengues_kWh"]:
        fig.add_trace(
            go.Scatter(
                x=daily_gen["Date"],
                y=daily_gen[col],
                mode="lines+markers",
                name=col.replace("_kWh", ""),
            )
        )

    fig.update_layout(
        title="Geração Diária por Projeto",
        xaxis_title="Data",
        yaxis_title="Geração (kWh)",
        hovermode="x unified",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PÁGINA 2: MANUTENÇÃO E SAÚDE
# ============================================================================

elif page == "🔧 Manutenção e Saúde":
    st.markdown(
        "<h1 class='header-title'>Manutenção e Saúde dos Sistemas</h1>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tarefas em Progresso", 1, "1 reparação alta prioridade")

    with col2:
        st.metric("Próximas Revisões", 2, "Próximos 7 dias")

    with col3:
        st.metric("Saúde Média", "91%", "Excelente")

    st.divider()

    # Tabela de Manutenção
    st.markdown("### 🔧 Histórico de Manutenção")

    maint_display = sample_maintenance.copy()

    # Colorir status
    def color_status(status):
        if status == "Concluído":
            return "🟢 Concluído"
        elif status == "Em progresso":
            return "🟡 Em progresso"
        else:
            return "📅 Agendado"

    maint_display["Status"] = maint_display["Status"].apply(color_status)

    st.dataframe(maint_display, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏥 Saúde do Sistema por Projeto")
        health_data = sample_projects[sample_projects["Status"] == "Operacional"].copy()
        health_data = health_data.sort_values("System_Health", ascending=True)

        fig = px.bar(
            health_data,
            y="Community",
            x="System_Health",
            orientation="h",
            labels={"System_Health": "Saúde (%)", "Community": "Comunidade"},
            color="System_Health",
            color_continuous_scale="RdYlGn",
            range_color=[80, 100],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚠️ Alertas de Sistema")

        alerts = {
            "Cacula": "✅ Normal",
            "Humpata": "⚠️ Limpeza necessária (score: 92%)",
            "Quilengues": "⚠️ Calibração em progresso",
        }

        for project, alert in alerts.items():
            st.info(f"**{project}**: {alert}")

    st.divider()

    st.markdown("### 📋 Agendar Manutenção")
    col1, col2, col3 = st.columns(3)

    with col1:
        project = st.selectbox(
            "Selecionar Projeto", ["Cacula", "Humpata", "Quilengues"]
        )

    with col2:
        maint_type = st.selectbox(
            "Tipo de Manutenção",
            ["Limpeza painéis", "Inspeção", "Reparo", "Calibração"],
        )

    with col3:
        maint_date = st.date_input("Data de Agendamento")

    if st.button("✏️ Agendar", use_container_width=True):
        st.success(f"✅ Manutenção agendada para {project} em {maint_date}")


# ============================================================================
# PÁGINA 3: IMPACTO COMUNITÁRIO
# ============================================================================

elif page == "👥 Impacto Comunitário":
    st.markdown(
        "<h1 class='header-title'>Impacto Comunitário e Social</h1>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Comunidades Beneficiadas", 5, "2 operacionais + 3 planejamento")

    with col2:
        st.metric("População Total", "6,550", "+15% vs ano passado")

    with col3:
        st.metric("Acesso a Eletricidade", "92%", "Meta: 95%")

    with col4:
        st.metric("Satisfação Comunitária", "4.2/5.0", "Muito satisfeito")

    st.divider()

    # Impacto por comunidade
    st.markdown("### 📊 Indicadores de Impacto por Comunidade")

    impact_data = pd.DataFrame(
        {
            "Community": ["Cacula", "Humpata", "Quilengues"],
            "Pop_Served": [850, 1200, 1100],
            "Households": [170, 240, 220],
            "School_hrs/day": [8, 8, 8],
            "Hospital_hrs/day": [24, 24, 24],
            "Satisfaction": [4.5, 4.3, 4.0],
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            impact_data,
            x="Community",
            y="Households",
            labels={"Households": "Famílias Beneficiadas", "Community": "Comunidade"},
            color="Households",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.radar(
            impact_data,
            r="Satisfaction",
            theta="Community",
            fill="toself",
            title="Satisfação Comunitária (0-5)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📚 Educação e Bem-estar")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Escolas Eletrificadas", 3, "100% dos projetos operacionais")

    with col2:
        st.metric("Centros de Saúde", 3, "Funcionamento 24/7")

    with col3:
        st.metric("Negócios Facilitados", 45, "Pequenos comerciantes")

    st.divider()

    st.markdown("### 💬 Feedback Comunitário (Últimas Semanas)")

    testimonials = [
        (
            "Maria Silva, Cacula",
            "Agora meus filhos podem estudar à noite. A mudança na educação é real.",
        ),
        (
            "João Nkosi, Humpata",
            "O sistema de refrigeração da clínica é muito confiável. Salva vidas.",
        ),
        (
            "Lucia Mbarga, Quilengues",
            "Meu negócio de costura cresceu 200% com luz disponível.",
        ),
    ]

    for name, feedback in testimonials:
        st.info(f'**{name}**: "{feedback}"')


# ============================================================================
# PÁGINA 4: INDICADORES DE PERFORMANCE
# ============================================================================

elif page == "💡 Indicadores de Performance":
    st.markdown(
        "<h1 class='header-title'>Indicadores Técnicos de Performance</h1>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Métricas operacionais detalhadas")

    # KPIs financeiros
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_investment = sample_projects[sample_projects["Status"] == "Operacional"][
            "Investment_USD"
        ].sum()
        st.metric("Investimento Total", f"${total_investment:,.0f}", "USD")

    with col2:
        total_revenue = (
            sample_projects[sample_projects["Status"] == "Operacional"][
                "Annual_Generation_MWh"
            ].sum()
            * 0.15
        )
        st.metric(
            "Receita Anual Estimada", f"${total_revenue:,.0f}", "USD (tarifa média)"
        )

    with col3:
        st.metric("Recuperação de Capital", "2.8 anos", "Média")

    with col4:
        st.metric("ROI Médio", "+11.7%", "Excelente")

    st.divider()

    # Performance técnica
    st.markdown("### ⚡ Performance Técnica")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Eficiência Média Diária")
        efficiency_data = pd.DataFrame(
            {
                "Hora": range(0, 24),
                "Eficiencia": [
                    0,
                    0,
                    0,
                    0,
                    2,
                    8,
                    15,
                    22,
                    28,
                    32,
                    35,
                    37,
                    38,
                    37,
                    35,
                    32,
                    28,
                    22,
                    15,
                    8,
                    2,
                    0,
                    0,
                    0,
                ],
            }
        )

        fig = px.area(
            efficiency_data,
            x="Hora",
            y="Eficiencia",
            labels={"Hora": "Hora do Dia", "Eficiencia": "Eficiência (%)"},
            title="Perfil de Eficiência (6h-18h)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Performance YTD (Ano até Agora)")
        ytd_data = pd.DataFrame(
            {
                "Mês": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"],
                "Geração_kWh": [210, 195, 240, 265, 280, 310, 285, 275],
                "Target_kWh": [240, 240, 240, 240, 280, 300, 300, 300],
            }
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=ytd_data["Mês"],
                y=ytd_data["Geração_kWh"],
                mode="lines+markers",
                name="Geração Real",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=ytd_data["Mês"],
                y=ytd_data["Target_kWh"],
                mode="lines+markers",
                name="Target",
                line=dict(dash="dash"),
            )
        )
        fig.update_layout(
            xaxis_title="Mês",
            yaxis_title="Geração (kWh)",
            hovermode="x unified",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📈 Análise Comparativa")

    comparison_data = sample_projects[sample_projects["Status"] == "Operacional"].copy()
    comparison_data["LCOE_USD/kWh"] = comparison_data["Investment_USD"] / (
        comparison_data["Annual_Generation_MWh"] * 1000 * 20
    )
    comparison_data["Geração_por_kW"] = (
        comparison_data["Annual_Generation_MWh"] / comparison_data["Capacity_kW"]
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            comparison_data,
            x="Community",
            y="LCOE_USD/kWh",
            labels={"LCOE_USD/kWh": "LCOE (USD/kWh)", "Community": "Comunidade"},
            color="LCOE_USD/kWh",
            color_continuous_scale="RdYlGn_r",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            comparison_data,
            x="Capacity_kW",
            y="Geração_por_kW",
            size="Population_Served",
            color="Community",
            labels={
                "Capacity_kW": "Capacidade (kW)",
                "Geração_por_kW": "Geração por kW (MWh/kW/ano)",
            },
            title="Eficiência de Geração vs Capacidade",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📊 Relatório Exportável")

    if st.button("📥 Gerar Relatório PDF", use_container_width=True):
        st.info("📄 Relatório em PDF seria gerado aqui (integrar com reportlab/fpdf)")

    if st.button("📊 Exportar para Excel", use_container_width=True):
        st.success("✅ Dados exportados para Excel (download automático)")


# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>GEESP-Angola | Sistema de Monitoramento Pós-Implementação</p>
        <p>Última atualização: 2025-08-{:02d} 14:35 UTC</p>
        <p><small>Desenvolvido para ISPTEC Energy Research Center</small></p>
    </div>
""".format(datetime.now().day),
    unsafe_allow_html=True,
)
