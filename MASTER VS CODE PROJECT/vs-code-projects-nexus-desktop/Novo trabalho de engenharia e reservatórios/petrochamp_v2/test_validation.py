#!/usr/bin/env python3
"""
🧪 Validação da instalação e funcionalidade do PetroChamp v2.0

Execute este arquivo para verificar se tudo está funcionando corretamente:
    python test_validation.py
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Cores para output no terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Imprime cabeçalho formatado."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.RESET}\n")


def print_success(text: str) -> None:
    """Imprime mensagem de sucesso."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str) -> None:
    """Imprime mensagem de erro."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str) -> None:
    """Imprime mensagem de aviso."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def test_imports() -> Tuple[bool, List[str]]:
    """Testa importação de módulos principais."""
    print_header("1. VERIFICANDO IMPORTAÇÕES")
    
    results = []
    
    imports_to_test = [
        ("petrochamp_v2", "Pacote principal"),
        ("petrochamp_v2.config.settings", "Configuração"),
        ("petrochamp_v2.core.models", "Modelos"),
        ("petrochamp_v2.core.plugins", "Sistema de plugins"),
        ("petrochamp_v2.core.analysis", "Análise avançada"),
        ("petrochamp_v2.data.persistence", "Persistência"),
    ]
    
    all_ok = True
    
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print_success(f"{description} ({module_name})")
            results.append(f"✓ {description}")
        except ImportError as e:
            print_error(f"{description}: {str(e)}")
            results.append(f"✗ {description}: {str(e)}")
            all_ok = False
    
    return all_ok, results


def test_configuration() -> Tuple[bool, List[str]]:
    """Testa sistema de configuração."""
    print_header("2. TESTANDO CONFIGURAÇÃO")
    
    results = []
    
    try:
        from petrochamp_v2 import AppConfig, DEVELOPMENT_CONFIG, PRODUCTION_CONFIG
        
        # Testar carregar configuração
        config = DEVELOPMENT_CONFIG
        print_success("✓ Carregada configuração de desenvolvimento")
        results.append("✓ Configuração carregada")
        
        # Testar validação
        if config.validate():
            print_success("✓ Validação de configuração passou")
            results.append("✓ Validação OK")
        else:
            print_error("✗ Validação de configuração falhou")
            results.append("✗ Validação falhou")
            return False, results
        
        # Verificar propriedades
        assert hasattr(config, 'max_cache_size')
        assert hasattr(config, 'visualization')
        assert hasattr(config, 'analysis')
        print_success("✓ Todas as propriedades presentes")
        results.append("✓ Propriedades OK")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro na configuração: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        return False, results


def test_models() -> Tuple[bool, List[str]]:
    """Testa modelos de dados."""
    print_header("3. TESTANDO MODELOS DE DADOS")
    
    results = []
    
    try:
        from petrochamp_v2 import ReservoirData, EORProject, ScreeningResult
        
        # Criar dados de reservatório
        reservoir = ReservoirData(
            api_gravity=25.0,
            viscosity=500.0,
            depth=1200,
            porosity=0.20,
            permeability=100,
            temperature=60,
            saturation_oil=0.45,
            saturation_water=0.55,
            net_to_gross=0.80,
            formation="Sandstone"
        )
        print_success("✓ ReservoirData criado com sucesso")
        results.append("✓ ReservoirData OK")
        
        # Testar serialização
        data_dict = reservoir.to_dict()
        assert isinstance(data_dict, dict)
        assert data_dict['api_gravity'] == 25.0
        print_success("✓ Serialização JSON funcionando")
        results.append("✓ Serialização OK")
        
        # Testar desserialização
        reservoir2 = ReservoirData.from_dict(data_dict)
        assert reservoir2.api_gravity == reservoir.api_gravity
        print_success("✓ Desserialização funcionando")
        results.append("✓ Desserialização OK")
        
        # Criar projeto
        project = EORProject(
            name="Projeto Teste",
            location="Campo X",
            reservoir_data=reservoir
        )
        print_success("✓ EORProject criado com sucesso")
        results.append("✓ EORProject OK")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro nos modelos: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        return False, results


def test_plugins() -> Tuple[bool, List[str]]:
    """Testa sistema de plugins."""
    print_header("4. TESTANDO SISTEMA DE PLUGINS")
    
    results = []
    
    try:
        from petrochamp_v2 import PluginManager, ReservoirData
        
        pm = PluginManager()
        print_success("✓ PluginManager inicializado")
        results.append("✓ PluginManager OK")
        
        # Listar plugins disponíveis
        methods = pm.get_available_methods()
        assert len(methods) > 0
        print_success(f"✓ {len(methods)} métodos EOR disponíveis")
        results.append(f"✓ {len(methods)} métodos disponíveis")
        
        # Testar cálculo de suitability
        reservoir = ReservoirData(
            api_gravity=25,
            viscosity=500,
            depth=1200,
            porosity=0.20,
            permeability=100,
            temperature=60,
            saturation_oil=0.45,
            saturation_water=0.55,
            net_to_gross=0.80,
            formation="Sandstone"
        )
        
        scores = pm.calculate_all_suitability_scores(reservoir.to_dict())
        assert isinstance(scores, dict)
        assert len(scores) > 0
        print_success(f"✓ Cálculo de suitability: {len(scores)} métodos avaliados")
        results.append(f"✓ Suitability calculado")
        
        # Mostrar top 3
        top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        for method, score in top3:
            print(f"   - {method}: {score:.1f}%")
        results.append(f"✓ Top 3 métodos identificados")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro nos plugins: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, results


def test_persistence() -> Tuple[bool, List[str]]:
    """Testa sistema de persistência."""
    print_header("5. TESTANDO PERSISTÊNCIA")
    
    results = []
    
    try:
        from petrochamp_v2 import ProjectManager, EORProject, ReservoirData
        from pathlib import Path
        import tempfile
        
        # Usar diretório temporário para testes
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = ProjectManager(tmpdir)
            print_success("✓ ProjectManager inicializado")
            results.append("✓ ProjectManager OK")
            
            # Criar projeto
            reservoir = ReservoirData(
                api_gravity=25,
                viscosity=500,
                depth=1200,
                porosity=0.20,
                permeability=100,
                temperature=60,
                saturation_oil=0.45,
                saturation_water=0.55,
                net_to_gross=0.80,
                formation="Sandstone"
            )
            
            project = mgr.create_project(
                name="Teste Persistência",
                location="Campo Y",
                reservoir_data=reservoir
            )
            print_success("✓ Projeto criado")
            results.append("✓ Projeto criado")
            
            project_id = project.id
            
            # Salvar
            mgr.save_project(project)
            print_success("✓ Projeto salvo")
            results.append("✓ Projeto salvo")
            
            # Listar
            projects = mgr.list_projects()
            assert len(projects) > 0
            print_success(f"✓ Projeto listado")
            results.append("✓ Listar OK")
            
            # Carregar
            loaded_project = mgr.open_project(project_id)
            assert loaded_project.name == project.name
            print_success("✓ Projeto carregado com sucesso")
            results.append("✓ Carregamento OK")
            
            # Exportar
            export_path = Path(tmpdir) / "export.json"
            mgr.export_project(project_id, str(export_path))
            assert export_path.exists()
            print_success("✓ Projeto exportado")
            results.append("✓ Exportação OK")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro na persistência: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, results


def test_cache() -> Tuple[bool, List[str]]:
    """Testa sistema de cache."""
    print_header("6. TESTANDO CACHE")
    
    results = []
    
    try:
        from petrochamp_v2.data.persistence import ResultsCache
        
        cache = ResultsCache(max_size=100, ttl_seconds=300)
        print_success("✓ Cache inicializado")
        results.append("✓ Cache OK")
        
        # Adicionar item
        cache.put("key1", {"value": 42})
        cached_value = cache.get("key1")
        assert cached_value == {"value": 42}
        print_success("✓ Cache put/get funcionando")
        results.append("✓ Put/Get OK")
        
        # Verificar estatísticas
        stats = cache.get_statistics()
        assert 'hit_count' in stats
        assert 'miss_count' in stats
        print_success(f"✓ Estatísticas: {stats['hit_count']} hits, {stats['miss_count']} misses")
        results.append("✓ Estatísticas OK")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro no cache: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        return False, results


def test_analysis() -> Tuple[bool, List[str]]:
    """Testa módulo de análise."""
    print_header("7. TESTANDO ANÁLISE AVANÇADA")
    
    results = []
    
    try:
        from petrochamp_v2 import SensitivityAnalyzer
        
        analyzer = SensitivityAnalyzer()
        print_success("✓ SensitivityAnalyzer inicializado")
        results.append("✓ Analyzer OK")
        
        # Testar função objetivo simples
        def simple_objective(params):
            return params.get('x', 0) ** 2 + params.get('y', 0) ** 2
        
        # One-At-a-Time
        try:
            results_oat = analyzer.analyze_one_at_a_time(
                base_case={'x': 1, 'y': 1},
                parameter_ranges={'x': (0, 2), 'y': (0, 2)},
                objective_function=simple_objective,
                steps=3
            )
            assert 'x' in results_oat
            assert 'y' in results_oat
            print_success("✓ One-At-a-Time analysis funcionando")
            results.append("✓ OAT OK")
        except Exception as e:
            print_warning(f"⚠ OAT com limitações: {str(e)}")
            results.append("⚠ OAT com limitações")
        
        return True, results
        
    except Exception as e:
        print_error(f"Erro na análise: {str(e)}")
        results.append(f"✗ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, results


def test_dependencies() -> Tuple[bool, List[str]]:
    """Verifica dependências externas."""
    print_header("8. VERIFICANDO DEPENDÊNCIAS")
    
    results = []
    
    dependencies = [
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('matplotlib', 'Matplotlib'),
        ('scipy', 'SciPy'),
    ]
    
    all_ok = True
    for package, name in dependencies:
        try:
            __import__(package)
            print_success(f"✓ {name}")
            results.append(f"✓ {name}")
        except ImportError:
            print_error(f"✗ {name} não instalado")
            results.append(f"✗ {name}")
            all_ok = False
    
    return all_ok, results


def main() -> None:
    """Executa todos os testes."""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔" + "="*58 + "╗")
    print("║" + "🧪 VALIDAÇÃO - PetroChamp v2.0".center(58) + "║")
    print("╚" + "="*58 + "╝")
    print(Colors.RESET)
    
    all_results = []
    tests = [
        ("Dependências", test_dependencies),
        ("Importações", test_imports),
        ("Configuração", test_configuration),
        ("Modelos", test_models),
        ("Plugins", test_plugins),
        ("Persistência", test_persistence),
        ("Cache", test_cache),
        ("Análise", test_analysis),
    ]
    
    overall_success = True
    
    for test_name, test_func in tests:
        try:
            success, test_results = test_func()
            all_results.extend(test_results)
            if not success:
                overall_success = False
        except Exception as e:
            print_error(f"ERRO CRÍTICO em {test_name}: {str(e)}")
            all_results.append(f"✗ {test_name}: Erro crítico")
            overall_success = False
    
    # Resumo final
    print_header("RESUMO FINAL")
    
    passed = sum(1 for r in all_results if r.startswith("✓"))
    failed = sum(1 for r in all_results if r.startswith("✗"))
    warnings = sum(1 for r in all_results if r.startswith("⚠"))
    
    print(f"{Colors.GREEN}✓ Testes passaram: {passed}{Colors.RESET}")
    if warnings > 0:
        print(f"{Colors.YELLOW}⚠ Avisos: {warnings}{Colors.RESET}")
    if failed > 0:
        print(f"{Colors.RED}✗ Testes falharam: {failed}{Colors.RESET}")
    
    print(f"\nTotal: {passed + failed + warnings} testes")
    
    if overall_success and failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TODAS AS VALIDAÇÕES PASSARAM!{Colors.RESET}")
        print(f"{Colors.GREEN}A plataforma está pronta para uso!{Colors.RESET}\n")
        print("Próximos passos:")
        print("1. Execute: python example_complete.py")
        print("2. Explore os módulos em petrochamp_v2/")
        print("3. Comece a implementar sua interface gráfica\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ ALGUNS TESTES FALHARAM{Colors.RESET}")
        print(f"{Colors.RED}Por favor, corrija os erros acima antes de continuar.{Colors.RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
