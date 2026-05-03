"""
Metrics Card Component
Reusable KPI cards display
"""

import streamlit as st
from typing import List, Dict


def MetricsCard(metrics: List[Dict[str, str]]):
    """
    Display multiple metric cards in a row
    
    Args:
        metrics: List of dicts with keys 'label', 'value', 'delta' (optional)
    
    Example:
        MetricsCard([
            {"label": "Critérios", "value": "5"},
            {"label": "Zonas", "value": "3"},
        ])
    """
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            label = metric.get("label", "")
            value = metric.get("value", "N/A")
            delta = metric.get("delta", None)
            
            st.metric(label=label, value=value, delta=delta)
