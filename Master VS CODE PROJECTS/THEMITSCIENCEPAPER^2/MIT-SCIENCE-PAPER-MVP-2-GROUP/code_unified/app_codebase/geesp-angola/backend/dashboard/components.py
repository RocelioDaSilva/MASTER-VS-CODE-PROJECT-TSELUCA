"""
GEESP-Angola Dashboard Components
Consolidated UI components for metrics, maps, weights, and data tables
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from typing import List, Dict, Optional, Tuple, Iterable
from pathlib import Path


# ============================================================================
# METRIC CARD COMPONENTS
# ============================================================================

def render_card(title: str, value, delta: str = "") -> dict:
    """
    Return a simple serializable representation of a metric card.
    
    Designed so pages can call this and render with Streamlit when available.
    Can be used for non-UI code paths that need to work without Streamlit.
    
    Args:
        title: Card title
        value: Card value (numeric or string)
        delta: Optional delta value or change indicator
    
    Returns:
        Dictionary with keys: 'title', 'value', 'delta'
    
    Example:
        card = render_card("Solar Capacity", "250 kW", "+15%")
    """
    return {"title": title, "value": value, "delta": delta}


def MetricsCard(metrics: List[Dict[str, str]]):
    """
    Display multiple metric cards in a row using Streamlit.
    
    **Interactive Streamlit component** for displaying KPIs
    
    Args:
        metrics: List of dicts with keys 'label', 'value', 'delta' (optional)
    
    Example:
        MetricsCard([
            {"label": "Critérios", "value": "5"},
            {"label": "Zonas", "value": "3"},
            {"label": "Mudança", "value": "+2"},
        ])
    """
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            label = metric.get("label", "")
            value = metric.get("value", "N/A")
            delta = metric.get("delta", None)
            
            st.metric(label=label, value=value, delta=delta)


# ============================================================================
# MAP VIEWER COMPONENT
# ============================================================================

def create_map(lat: float = -18.0, lon: float = 14.75, zoom_start: int = 8, 
               markers: Iterable[Dict] = None) -> folium.Map:
    """
    Create a simple Folium map centered at (lat, lon). Optionally add markers.
    
    **Simple function for quick map creation** (alternative to MapViewer class)
    
    Args:
        lat: Latitude for map center (default: Angola center -18.0)
        lon: Longitude for map center (default: Angola center 14.75)
        zoom_start: Initial zoom level (default: 8)
        markers: Iterable of dicts with keys: 'name', 'lat', 'lon', optional 'color'
    
    Returns:
        folium.Map object for embedding via streamlit_folium
    
    Example:
        m = create_map(markers=[
            {'name': 'Luanda', 'lat': -8.8, 'lon': 13.2, 'color': 'red'},
            {'name': 'Site 1', 'lat': -18.0, 'lon': 14.75, 'color': 'blue'}
        ])
    """
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start, tiles="OpenStreetMap")
    if markers:
        for mk in markers:
            name = mk.get("name", "marker")
            coords = [float(mk.get("lat", lat)), float(mk.get("lon", lon))]
            color = mk.get("color", "blue")
            folium.Marker(location=coords, popup=name, tooltip=name, 
                         icon=folium.Icon(color=color)).add_to(m)
    return m


class MapViewer:
    """Manages Folium map creation and rendering"""

    def __init__(self, 
                 center: Tuple[float, float] = (-18.0, 14.75),
                 zoom: int = 8,
                 style: str = "OpenStreetMap"):
        self.center = center
        self.zoom = zoom
        self.style = style
        self.map = None
        self._init_map()

    def _init_map(self):
        """Initialize base map"""
        self.map = folium.Map(
            location=self.center,
            zoom_start=self.zoom,
            tiles=self.style,
        )

    def add_markers(self, 
                    communities_df: pd.DataFrame,
                    priority_names: Optional[List[str]] = None):
        """
        Add community markers to map
        
        Args:
            communities_df: DataFrame with latitude, longitude, name, population_est
            priority_names: List of community names to highlight
        """
        if priority_names is None:
            priority_names = []
        
        for idx, row in communities_df.iterrows():
            name = row.get("name", f"Comunidade {idx}")
            coords = [float(row.get("latitude", 0)), float(row.get("longitude", 0))]
            pop = int(row.get("population_est", 0))
            
            if name in priority_names:
                color = "orange"
                icon = "info-sign"
                prefix = "🔴 "
            else:
                color = "blue"
                icon = "circle"
                prefix = "⚪ "
            
            folium.Marker(
                location=coords,
                popup=f"{name}<br>Pop: {pop:,}",
                tooltip=f"{prefix}{name}",
                icon=folium.Icon(color=color, icon=icon),
            ).add_to(self.map)

    def add_zones_layer(self, 
                        zones_geojson: Optional[str] = None):
        """Add zone boundaries from GeoJSON"""
        if zones_geojson:
            try:
                folium.GeoJson(zones_geojson).add_to(self.map)
            except Exception as e:
                st.warning(f"⚠️ Não foi possível carregar zonas: {e}")

    def render(self, height: int = 500, width: int = 700):
        """Render map in Streamlit"""
        return st_folium(self.map, width=width, height=height)


# ============================================================================
# WEIGHT SLIDERS COMPONENT
# ============================================================================

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


# ============================================================================
# ZONE TABLE COMPONENT
# ============================================================================

class ZoneTable:
    """Manages zone data table display"""

    def __init__(self, zones_data: dict):
        """
        Initialize with zones data
        
        Args:
            zones_data: Dict or DataFrame with zone information
        """
        if isinstance(zones_data, dict):
            self.df = pd.DataFrame(zones_data)
        else:
            self.df = zones_data

    def render(self, title: str = "🎯 Zonas Prioritárias"):
        """Render zone table"""
        st.markdown(f"## {title}")
        st.dataframe(self.df, use_container_width=True, hide_index=True)

    def get_sorted(self, by_column: str, ascending: bool = False) -> pd.DataFrame:
        """Get sorted zones"""
        return self.df.sort_values(by=by_column, ascending=ascending)

    def export_csv(self) -> str:
        """Export to CSV string"""
        return self.df.to_csv(index=False)

    def export_json(self) -> str:
        """Export to JSON string"""
        return self.df.to_json(orient='records', indent=2)


# ============================================================================
# PUBLIC API EXPORTS
# ============================================================================

__all__ = [
    # Metric card functions
    "render_card",
    "MetricsCard",
    
    # Map utilities
    "create_map",
    "MapViewer",
    
    # Weight management
    "WeightSliders",
    
    # Zone management
    "ZoneTable",
]
