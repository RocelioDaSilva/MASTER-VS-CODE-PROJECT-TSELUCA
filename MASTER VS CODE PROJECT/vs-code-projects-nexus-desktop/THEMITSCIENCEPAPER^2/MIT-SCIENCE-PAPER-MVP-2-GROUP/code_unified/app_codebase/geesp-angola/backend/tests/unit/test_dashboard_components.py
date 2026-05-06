from pathlib import Path


def test_dashboard_file_contains_title_and_pages():
    p = Path(__file__).parent.parent / "dashboard" / "app.py"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "GEESP-Angola" in text
    # Check page option strings exist
    assert "Início" in text or "Inicio" in text
    assert "Análise MCDA" in text or "MCDA" in text
