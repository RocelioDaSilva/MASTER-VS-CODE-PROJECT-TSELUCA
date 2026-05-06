"""
✅ Teste de Integração V5 → V2

Valida que todos os componentes estão funcionando corretamente.
"""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

import logging
logging.basicConfig(level=logging.INFO)


def test_imports():
    """Testa se todos os imports funcionam."""
    print("\n🔍 TESTANDO IMPORTS...")
    print("-" * 80)
    
    tests_passed = 0
    tests_failed = 0
    
    imports_to_test = [
        ("Config", "petrochamp_v2.config.settings", ["get_config", "AppConfig"]),
        ("Models", "petrochamp_v2.core.models", ["ReservoirData", "EORProject"]),
        ("Plugins", "petrochamp_v2.core.plugins", ["PluginManager"]),
        ("Analysis", "petrochamp_v2.core.analysis", ["SensitivityAnalyzer"]),
        ("Persistence", "petrochamp_v2.data.persistence", ["ProjectManager"]),
        ("Dashboard", "petrochamp_v2.core.dashboard", ["RealtimeDashboard"]),
        ("Reporting", "petrochamp_v2.core.reporting", ["AdvancedReportGenerator"]),
        ("V5 Integration", "petrochamp_v2.ui.v5_integration", ["SuitabilityVisualizer"]),
    ]
    
    for name, module, items in imports_to_test:
        try:
            mod = __import__(module, fromlist=items)
            for item in items:
                getattr(mod, item)
            print(f"  ✅ {name:20} - OK")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ {name:20} - FAILED: {e}")
            tests_failed += 1
    
    print("-" * 80)
    print(f"Imports: {tests_passed} OK, {tests_failed} FAILED\n")
    
    return tests_failed == 0


def test_config():
    """Testa configurações."""
    print("🔧 TESTANDO CONFIGURAÇÕES...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.config.settings import get_config, AppConfig
        
        config = get_config()
        print(f"  ✅ Config carregada")
        print(f"     - App name: {config.app_name}")
        print(f"     - Version: {config.version}")
        print(f"     - Debug: {config.debug_mode}")
        print(f"     - Performance level: {config.performance.optimization_level}")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_models():
    """Testa modelos de dados."""
    print("📊 TESTANDO MODELOS DE DADOS...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.core.models import ReservoirData, EORProject, EORMethodType
        
        # Criar reservatório
        reservoir = ReservoirData(
            name="Teste",
            location="Santos",
            depth=2500.0,
            temperature=75.0,
            pressure=250.0,
            api_gravity=28.5,
            viscosity=125.0,
            permeability=800.0,
            porosity=18.5
        )
        print(f"  ✅ ReservoirData criado")
        print(f"     - Nome: {reservoir.name}")
        print(f"     - Profundidade: {reservoir.depth}m")
        
        # Criar projeto
        project = EORProject(
            name="Teste",
            reservoir=reservoir,
            selected_methods=[EORMethodType.STEAM_INJECTION]
        )
        print(f"  ✅ EORProject criado")
        print(f"     - Métodos: {len(project.selected_methods)}")
        
        # Testar serialização
        json_data = reservoir.to_json()
        print(f"  ✅ Serialização JSON: {len(json_data)} bytes")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_plugins():
    """Testa sistema de plugins."""
    print("🔌 TESTANDO SISTEMA DE PLUGINS...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.core.plugins import PluginManager
        
        manager = PluginManager()
        print(f"  ✅ PluginManager criado")
        
        plugins = manager.list_available()
        print(f"  ✅ {len(plugins)} plugins disponíveis")
        
        for plugin in plugins:
            print(f"     - {plugin}")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_analysis():
    """Testa análise."""
    print("📈 TESTANDO ANÁLISE...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.config.settings import get_config
        from petrochamp_v2.core.models import ReservoirData
        from petrochamp_v2.core.analysis import SensitivityAnalyzer
        
        config = get_config()
        analyzer = SensitivityAnalyzer(config)
        
        reservoir = ReservoirData(
            name="Teste",
            location="Santos",
            depth=2500.0,
            temperature=75.0,
            pressure=250.0,
            api_gravity=28.5,
            viscosity=125.0,
            permeability=800.0,
            porosity=18.5
        )
        
        print(f"  ✅ SensitivityAnalyzer criado")
        
        # OAT Analysis
        result_oat, fig_oat = analyzer.analyze_one_at_a_time(
            reservoir, ['temperature', 'viscosity']
        )
        print(f"  ✅ OAT analysis: {len(result_oat)} parâmetros")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_persistence():
    """Testa persistência."""
    print("💾 TESTANDO PERSISTÊNCIA...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.data.persistence import ProjectManager, ResultsCache
        
        manager = ProjectManager()
        print(f"  ✅ ProjectManager criado")
        
        cache = ResultsCache(max_size=100, ttl=3600)
        print(f"  ✅ ResultsCache criado")
        print(f"     - Max size: {cache.max_size}")
        print(f"     - TTL: {cache.ttl}s")
        
        # Testar cache
        cache.put("test_key", {"value": 123})
        result = cache.get("test_key")
        print(f"  ✅ Cache put/get: {result}")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_dashboard():
    """Testa dashboard."""
    print("📊 TESTANDO DASHBOARD...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.core.dashboard import RealtimeDashboard
        import time
        
        dashboard = RealtimeDashboard()
        print(f"  ✅ RealtimeDashboard criado")
        
        dashboard.start()
        print(f"  ✅ Dashboard iniciado")
        
        dashboard.add_alert("INFO", "Test", "Teste de alerta")
        print(f"  ✅ Alerta adicionado")
        
        time.sleep(0.5)
        
        stats = dashboard.get_statistics_summary()
        print(f"  ✅ Estatísticas obtidas: {len(stats)} métricas")
        
        dashboard.stop()
        print(f"  ✅ Dashboard parado")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_reporting():
    """Testa relatórios."""
    print("📄 TESTANDO RELATÓRIOS...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.core.reporting import AdvancedReportGenerator, ReportMetadata
        
        report = AdvancedReportGenerator(
            metadata=ReportMetadata(
                title="Teste",
                author="Test",
                version="1.0"
            )
        )
        print(f"  ✅ AdvancedReportGenerator criado")
        
        report.add_section("Test Section")
        report.add_text("Test content")
        print(f"  ✅ Seção adicionada: {len(report._sections)} seções")
        
        html = report.to_html()
        print(f"  ✅ HTML gerado: {len(html)} bytes")
        
        json_data = report.to_json()
        print(f"  ✅ JSON gerado: {len(json_data)} bytes")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def test_v5_integration():
    """Testa integração com v5."""
    print("🔗 TESTANDO INTEGRAÇÃO V5...")
    print("-" * 80)
    
    try:
        from petrochamp_v2.ui.v5_integration import (
            SuitabilityVisualizer, V5ToV2Adapter, get_suitability_level
        )
        
        visualizer = SuitabilityVisualizer()
        print(f"  ✅ SuitabilityVisualizer criado")
        
        adapter = V5ToV2Adapter()
        print(f"  ✅ V5ToV2Adapter criado")
        
        # Test suitability levels
        scores = {'Método A': 85.0, 'Método B': 70.0, 'Método C': 50.0}
        converted = adapter.convert_scores_format(scores)
        print(f"  ✅ Scores convertidos: {len(converted)} métodos")
        
        # Test report
        report = adapter.generate_summary_report(scores)
        print(f"  ✅ Relatório gerado: {len(report)} bytes")
        
        # Test dataframe
        df = adapter.export_to_dataframe(scores)
        print(f"  ✅ DataFrame criado: {len(df)} linhas")
        
        print("-" * 80)
        return True
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        print("-" * 80)
        return False


def main():
    """Executa todos os testes."""
    print("\n" + "="*80)
    print("✅ SUITE DE TESTES - PETROCHAMP V5/V2 INTEGRAÇÃO")
    print("="*80)
    
    results = []
    
    # Executar testes
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Models", test_models()))
    results.append(("Plugins", test_plugins()))
    results.append(("Analysis", test_analysis()))
    results.append(("Persistence", test_persistence()))
    results.append(("Dashboard", test_dashboard()))
    results.append(("Reporting", test_reporting()))
    results.append(("V5 Integration", test_v5_integration()))
    
    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:25} {status}")
    
    print("-" * 80)
    print(f"Total: {passed} PASS, {failed} FAIL out of {len(results)}")
    print("="*80 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
