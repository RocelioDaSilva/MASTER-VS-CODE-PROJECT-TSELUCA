"""
Weight Sliders Component
Interactive weight configuration for MCDA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict


class WeightSliders:
    """Manages MCDA weight configuration via sliders"""

    def __init__(self, 
                 criteria: list,
                 defaults: Dict[str, float],
                 location: str = "sidebar"):
        self.criteria = criteria
        self.defaults = defaults
        self.location = location
        self.weights = {}

    def render(self) -> Dict[str, float]:
        """
        Render sliders and return normalized weights
        
        Returns:
            Dictionary of criterion -> normalized weight
        """
        container = st.sidebar if self.location == "sidebar" else st
        
        with container:
            st.markdown("## ⚙️ Configurar Pesos")
            
            for criterion in self.criteria:
                default_val = self.defaults.get(criterion, 20)
                self.weights[criterion] = st.slider(
                    f"{criterion}",
                    0, 100, default_val,
                    help="Ajuste o peso relativo deste critério"
                )
        
        # Normalize to sum to 100%
        total = sum(self.weights.values())
        weights_normalized = {k: v / total * 100 for k, v in self.weights.items()}
        
        return weights_normalized

    def get_weights(self) -> Dict[str, float]:
        """Get current weights"""
        return self.weights

    def display_distribution(self):
        """Display weight distribution chart"""
        if not self.weights:
            st.warning("⚠️ Configure pesos primeiro.")
            return
        
        total = sum(self.weights.values())
        weights_normalized = {k: v / total * 100 for k, v in self.weights.items()}
        
        df = pd.DataFrame({
            "Critério": list(weights_normalized.keys()),
            "Peso (%)": list(weights_normalized.values()),
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df,
                x="Critério",
                y="Peso (%)",
                color="Peso (%)",
                color_continuous_scale="Blues",
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df, use_container_width=True)
