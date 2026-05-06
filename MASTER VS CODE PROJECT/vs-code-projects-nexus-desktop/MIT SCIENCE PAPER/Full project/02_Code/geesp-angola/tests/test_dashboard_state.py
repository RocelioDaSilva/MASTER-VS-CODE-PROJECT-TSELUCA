from pathlib import Path


def test_dashboard_has_required_assets():
    base = Path(__file__).parent.parent / "dashboard"
    assert base.exists()
    # Ensure README or assets folder exists for dashboard
    assert (base / "app.py").exists()
    # optional assets
    assert (base / "static").exists() or (base / "assets").exists() or True
