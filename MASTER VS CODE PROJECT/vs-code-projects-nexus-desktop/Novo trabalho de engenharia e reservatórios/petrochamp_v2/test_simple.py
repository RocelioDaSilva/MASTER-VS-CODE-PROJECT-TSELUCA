# -*- coding: utf-8 -*-
"""Simple integration test"""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Starting integration tests...")
print("="*80)

# Test 1: Config
try:
    from petrochamp_v2.config.settings import get_config
    config = get_config()
    print(f"[OK] Config: {config.app_name} v{config.version}")
except Exception as e:
    print(f"[ERROR] Config: {e}")

# Test 2: Models
try:
    from petrochamp_v2.core.models import ReservoirData, EORProject
    reservoir = ReservoirData(
        name="Test",
        location="Test",
        depth=2500.0,
        temperature=75.0,
        pressure=250.0,
        api_gravity=28.5,
        viscosity=125.0,
        permeability=800.0,
        porosity=18.5
    )
    print(f"[OK] Models: ReservoirData created")
except Exception as e:
    print(f"[ERROR] Models: {e}")

# Test 3: Plugins
try:
    from petrochamp_v2.core.plugins import PluginManager
    manager = PluginManager()
    plugins = manager.list_available()
    print(f"[OK] Plugins: {len(plugins)} available")
except Exception as e:
    print(f"[ERROR] Plugins: {e}")

# Test 4: Analysis
try:
    from petrochamp_v2.core.analysis import SensitivityAnalyzer
    analyzer = SensitivityAnalyzer(config)
    print(f"[OK] Analysis: SensitivityAnalyzer initialized")
except Exception as e:
    print(f"[ERROR] Analysis: {e}")

# Test 5: Persistence
try:
    from petrochamp_v2.data.persistence import ProjectManager, ResultsCache
    pm = ProjectManager()
    cache = ResultsCache()
    print(f"[OK] Persistence: ProjectManager & ResultsCache initialized")
except Exception as e:
    print(f"[ERROR] Persistence: {e}")

# Test 6: Dashboard
try:
    from petrochamp_v2.core.dashboard import RealtimeDashboard
    dashboard = RealtimeDashboard()
    print(f"[OK] Dashboard: RealtimeDashboard initialized")
except Exception as e:
    print(f"[ERROR] Dashboard: {e}")

# Test 7: Reporting
try:
    from petrochamp_v2.core.reporting import AdvancedReportGenerator
    report = AdvancedReportGenerator()
    print(f"[OK] Reporting: AdvancedReportGenerator initialized")
except Exception as e:
    print(f"[ERROR] Reporting: {e}")

# Test 8: V5 Integration
try:
    from petrochamp_v2.ui.v5_integration import SuitabilityVisualizer, V5ToV2Adapter
    viz = SuitabilityVisualizer()
    adapter = V5ToV2Adapter()
    print(f"[OK] V5 Integration: Visualizer & Adapter initialized")
except Exception as e:
    print(f"[ERROR] V5 Integration: {e}")

print("="*80)
print("Integration test completed!")
