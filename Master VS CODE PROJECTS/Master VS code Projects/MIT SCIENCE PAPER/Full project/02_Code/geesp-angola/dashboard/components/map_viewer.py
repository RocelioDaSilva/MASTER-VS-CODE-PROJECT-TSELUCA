"""
Map Viewer Component
Reusable Folium map with layers and styling
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, List
from pathlib import Path


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
