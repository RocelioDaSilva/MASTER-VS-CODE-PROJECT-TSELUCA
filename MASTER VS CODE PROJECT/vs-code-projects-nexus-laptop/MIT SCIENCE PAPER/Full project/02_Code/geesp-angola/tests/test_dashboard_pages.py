import importlib


def test_pages_export_render():
    modules = [
        "dashboard.pages.home",
        "dashboard.pages.data_explore",
        "dashboard.pages.mcda",
        "dashboard.pages.results",
        "dashboard.pages.lcoe",
    ]
    for mod in modules:
        m = importlib.import_module(mod)
        assert hasattr(m, "render") and callable(m.render)
