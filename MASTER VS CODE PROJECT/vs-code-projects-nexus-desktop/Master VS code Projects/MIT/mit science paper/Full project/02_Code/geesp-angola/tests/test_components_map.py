import pytest

pytest.importorskip("folium")

from dashboard.components.map_renderer import create_map


def test_create_map_basic():
    m = create_map(-18.0, 14.75, zoom_start=6)
    import folium

    assert isinstance(m, folium.Map)


def test_create_map_with_markers():
    markers = [{"name": "A", "lat": -18.0, "lon": 14.75, "color": "orange"}, {"name": "B", "lat": -17.5, "lon": 15.0}]
    m = create_map(markers=markers)
    children = list(m._children.values())
    marker_count = sum(1 for c in children if c.__class__.__name__ in ("Marker", "CircleMarker"))
    assert marker_count >= 2
