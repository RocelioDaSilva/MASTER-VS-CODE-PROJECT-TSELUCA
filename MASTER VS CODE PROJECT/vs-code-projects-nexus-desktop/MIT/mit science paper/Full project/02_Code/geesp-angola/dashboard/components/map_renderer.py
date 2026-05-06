from typing import Iterable, Dict
import folium


def create_map(lat: float = -18.0, lon: float = 14.75, zoom_start: int = 8, markers: Iterable[Dict] = None) -> folium.Map:
    """Create a Folium map centered at (lat, lon). Optionally add markers.

    markers: iterable of dicts with keys: 'name', 'lat', 'lon', optional 'color'
    Returns the folium.Map object so it can be embedded via streamlit_folium in pages.
    """
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start, tiles="OpenStreetMap")
    if markers:
        for mk in markers:
            name = mk.get("name", "marker")
            coords = [float(mk.get("lat", lat)), float(mk.get("lon", lon))]
            color = mk.get("color", "blue")
            folium.Marker(location=coords, popup=name, tooltip=name, icon=folium.Icon(color=color)).add_to(m)
    return m
