def render():
    import streamlit as st
    import pandas as pd
    import plotly.express as px

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
            "Aptidão Média Zona A": [0.81, 0.82, 0.83, 0.84, 0.85],
            "Robustez": ["Robusta"] * 5,
        }

        fig = px.line(pd.DataFrame(sensitivity_data), x="Variação", y="Aptidão Média Zona A", title="Sensibilidade: Variação de Peso ±20%")
        st.plotly_chart(fig, use_container_width=True)
