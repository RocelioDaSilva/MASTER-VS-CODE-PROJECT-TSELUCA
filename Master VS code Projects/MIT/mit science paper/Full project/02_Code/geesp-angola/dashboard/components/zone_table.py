"""
Zone Table Component
Display and format zone comparison tables
"""

import streamlit as st
import pandas as pd


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
