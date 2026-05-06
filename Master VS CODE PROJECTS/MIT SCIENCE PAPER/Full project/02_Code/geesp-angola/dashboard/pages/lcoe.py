def render():
    import streamlit as st
    import plotly.express as px
    from pathlib import Path

    st.markdown("# 💰 Calculadora de LCOE")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ⚙️ Parâmetros")

        capacity = st.number_input("Capacidade (MW):", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
        irradiance = st.number_input("Irradiância Anual (kWh/m²/ano):", min_value=1000, max_value=3000, value=2226, step=50)
        discount_rate = st.slider("Taxa de Desconto (%):", min_value=1, max_value=15, value=8)
        lifetime = st.slider("Vida Útil (anos):", min_value=10, max_value=40, value=25)
        technology = st.selectbox("Tecnologia:", ["PV Fixo + Baterias", "PV com Rastreador", "Híbrido Solar+Diesel"]) 

    with col2:
        if st.button("Calcular LCOE", use_container_width=True, type="primary"):
            try:
                try:
                    from scripts.lcoe_calculator import LCOECalculator
                except Exception:
                    from lcoe_calculator import LCOECalculator

                calculator = LCOECalculator(location="Angola")
                comparison = calculator.compare_technologies(capacity_mw=capacity, annual_irradiance=irradiance, discount_rate=discount_rate, lifetime=lifetime)

                st.markdown("### 📊 Resultados")
                fig = px.bar(comparison, x="technology_name", y="lcoe_usd_per_kwh", color="lcoe_usd_per_kwh", color_continuous_scale="RdYlGn_r")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📋 Comparação Detalhada")
                display_cols = ["technology_name","capex_per_kw","annual_generation_mwh","lcoe_usd_per_mwh","lcoe_usd_per_kwh"]
                st.dataframe(comparison[display_cols].rename(columns={"technology_name": "Tecnologia","capex_per_kw": "CAPEX (USD/kW)","annual_generation_mwh": "Geração Anual (MWh)","lcoe_usd_per_mwh": "LCOE (USD/MWh)","lcoe_usd_per_kwh": "LCOE (USD/kWh)"}), use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao calcular LCOE: {e}")
