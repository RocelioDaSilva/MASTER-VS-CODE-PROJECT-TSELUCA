#!/usr/bin/env python3
"""
Exemplo Completo de Uso - PetroChamp Advanced v2.0

Demonstra todos os recursos principais da plataforma
"""

import sys
import json
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_config, DEVELOPMENT_CONFIG, load_config
from core.models import EORProject, ReservoirData, ScreeningResult, EconomicAnalysis
from core.plugins import PluginManager
from data.persistence import ProjectManager, ResultsCache
from core.analysis import SensitivityAnalyzer, HybridEOROptimizer, IntelligentRecommender
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def example_1_configuration():
    """Exemplo 1: Configuração da Aplicação"""
    print_header("EXEMPLO 1: Configuração Centralizada")
    
    # Usando configuração padrão
    config = get_config()
    print(f"✓ Configuração padrão carregada")
    print(f"  - Max cache size: {config.performance.max_cache_size}")
    print(f"  - Workers paralelos: {config.performance.max_workers}")
    print(f"  - Passos de sensibilidade: {config.analysis.sensitivity_steps}")
    
    # Usando configuração de desenvolvimento
    config_dev = DEVELOPMENT_CONFIG
    print(f"\n✓ Configuração DEVELOPMENT:")
    print(f"  - Debug mode: {config_dev.debug_mode}")
    print(f"  - Log level: {config_dev.log_level}")
    
    # Salvar configuração
    config_dev.save("config_exemplo.json")
    print(f"\n✓ Configuração salva em: config_exemplo.json")
    
    return config_dev


def example_2_project_management(config):
    """Exemplo 2: Gerenciamento de Projetos"""
    print_header("EXEMPLO 2: Gerenciamento de Projetos")
    
    # Inicializar project manager
    project_mgr = ProjectManager(storage_path="./projects_exemplo")
    logger.info("ProjectManager inicializado")
    
    # Criar projeto
    project = project_mgr.create_project(
        name="Projeto Piloto - Gás da Amazônia",
        description="Avaliação de métodos EOR para reservatório de gás condensado"
    )
    print(f"✓ Projeto criado:")
    print(f"  - ID: {project.id}")
    print(f"  - Nome: {project.name}")
    print(f"  - Data: {project.created_at}")
    
    # Adicionar dados do reservatório
    project.reservoir_data = ReservoirData(
        api_gravity=22,
        viscosity=450,
        depth=1250,
        thickness=28,
        permeability=120,
        porosity=23,
        temperature=68,
        pressure=280,
        salinity=55000,
        oil_saturation=65,
        field_name="Campo Imortal"
    )
    print(f"\n✓ Dados do reservatório adicionados:")
    print(f"  - API: {project.reservoir_data.api_gravity}°")
    print(f"  - Viscosidade: {project.reservoir_data.viscosity} cP")
    print(f"  - Profundidade: {project.reservoir_data.depth} m")
    
    # Salvar projeto
    saved = project_mgr.save_project(project, auto_backup=True)
    print(f"\n✓ Projeto salvo: {saved}")
    
    # Listar projetos
    projects = project_mgr.list_projects()
    print(f"\n✓ Projetos no sistema: {len(projects)}")
    for p in projects:
        print(f"  - {p['name']} (ID: {p['id'][:8]}...)")
    
    # Estatísticas
    stats = project_mgr.get_statistics()
    print(f"\n✓ Estatísticas:")
    print(f"  - Total de projetos: {stats.total_projects}")
    print(f"  - Projetos com resultados: {stats.projects_with_results}")
    
    return project_mgr, project


def example_3_screening(plugin_mgr, project):
    """Exemplo 3: Triagem com Sistema de Plugins"""
    print_header("EXEMPLO 3: Sistema de Plugins EOR - Triagem")
    
    # Listar métodos disponíveis
    available_methods = plugin_mgr.get_available_methods()
    print(f"✓ Métodos EOR disponíveis ({len(available_methods)}):")
    for method in available_methods:
        print(f"  - {method}")
    
    # Calcular suitability para todos os métodos
    print(f"\n✓ Calculando suitability para {len(available_methods)} métodos...")
    reservoir_dict = project.reservoir_data.to_dict()
    scores = plugin_mgr.calculate_all_suitability_scores(reservoir_dict)
    
    # Top 5 métodos
    print(f"\n✓ Top 5 Métodos (Ranking de Suitability):")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (method, score) in enumerate(sorted_scores[:5], 1):
        plugin = plugin_mgr.get_plugin(method)
        
        # Determinar status
        if score >= 80:
            status = "🟢 ALTA"
        elif score >= 60:
            status = "🟡 MÉDIA"
        else:
            status = "🔴 BAIXA"
        
        print(f"\n  {rank}. {method} - {score:.1f}% {status}")
        
        # Justificativa
        justification = plugin.get_justification(score, reservoir_dict)
        print(f"     {justificação[:100]}...")
        
        # Parâmetros críticos
        critical = plugin.get_critical_parameters(reservoir_dict)
        print(f"     Parâmetros críticos: {', '.join(critical)}")
        
        # Estimativa de recuperação
        recovery = plugin.estimate_recovery_factor(reservoir_dict, {})
        print(f"     Fator de recuperação estimado: {recovery*100:.1f}%")
    
    # Salvar resultados de triagem
    for rank, (method, score) in enumerate(sorted_scores, 1):
        result = ScreeningResult(
            method_name=method,
            suitability_score=score,
            rank=rank,
            status="ALTA" if score >= 80 else "MEDIA" if score >= 60 else "BAIXA",
            confidence=min(0.95, score/100)
        )
        project.screening_results.append(result)
    
    logger.info(f"Adicionados {len(project.screening_results)} resultados de triagem")
    
    return scores


def example_4_economic_analysis(plugin_mgr, project):
    """Exemplo 4: Análise Econômica"""
    print_header("EXEMPLO 4: Análise Econômica")
    
    # Obter melhor método
    best_method = project.get_best_method()
    print(f"✓ Melhor método: {best_method.method_name} ({best_method.suitability_score:.1f}%)")
    
    # Obter parâmetros econômicos do plugin
    plugin = plugin_mgr.get_plugin(best_method.method_name)
    econ_params = plugin.get_economic_parameters()
    
    # Criar análise econômica
    econ = EconomicAnalysis(
        method=best_method.method_name,
        capex=econ_params.get('capex_per_well', 2.5) * 10 * 1e6,  # 10 poços
        opex_annual=econ_params.get('opex_annual', 0.5) * 1e6,
        drilling_wells=10,
        production_rate_bbl_day=econ_params.get('production_rate_bbl_day', 200),
        oil_price=75.0,
        discount_rate=0.10,
        project_life=20
    )
    
    # Calcular NPV simplificado (sem descontos por simplicidade)
    total_production = econ.production_rate_bbl_day * 365 * econ.project_life / 1000  # MMbbl
    revenue = total_production * econ.oil_price
    costs = econ.capex + (econ.opex_annual * econ.project_life)
    econ.npv = (revenue - costs) / 1e6  # Converter para milhões
    econ.irr = 0.15  # Simplificado
    econ.recovery_factor = total_production / 100  # Simplificado
    
    project.economic_analyses.append(econ)
    
    print(f"\n✓ Análise Econômica:")
    print(f"  - Método: {econ.method}")
    print(f"  - CAPEX: ${econ.capex/1e6:.1f}M")
    print(f"  - OPEX anual: ${econ.opex_annual/1e6:.1f}M")
    print(f"  - Produção: {econ.production_rate_bbl_day:.0f} bbl/dia")
    print(f"  - NPV (20 anos): ${econ.npv:.1f}M")
    print(f"  - IRR: {econ.irr*100:.1f}%")
    print(f"  - Recuperação total: {total_production:.0f} MMbbl")


def example_5_sensitivity_analysis():
    """Exemplo 5: Análise de Sensibilidade"""
    print_header("EXEMPLO 5: Análise de Sensibilidade")
    
    analyzer = SensitivityAnalyzer()
    print(f"✓ Analisador de sensibilidade inicializado")
    
    # Função objetivo simplificada
    def npv_function(params):
        api = params.get('api_gravity', 25)
        visc = params.get('viscosity', 500)
        return (api * 2 - visc / 100) * 1e6
    
    # Análise One-At-a-Time
    print(f"\n✓ Realizando análise One-At-a-Time...")
    base_case = {
        'api_gravity': 25,
        'viscosity': 500,
        'depth': 1200
    }
    
    ranges = {
        'api_gravity': (10, 40),
        'viscosity': (100, 2000),
        'depth': (500, 2000)
    }
    
    oat_results = analyzer.analyze_one_at_a_time(
        base_case=base_case,
        parameter_ranges=ranges,
        objective_function=npv_function,
        steps=10
    )
    
    print(f"\n✓ Resultados OAT (Top 3):")
    for idx, row in oat_results.head(3).iterrows():
        print(f"  {row['parameter']}: sensibilidade={row['sensitivity']:.3f}")
    
    # Monte Carlo
    print(f"\n✓ Executando simulação Monte Carlo (100 iterações)...")
    distributions = {
        'api_gravity': {'type': 'normal', 'mean': 25, 'std': 3},
        'viscosity': {'type': 'lognormal', 'mean': 500, 'std': 100},
        'depth': {'type': 'uniform', 'min': 800, 'max': 1600}
    }
    
    mc_results = analyzer.monte_carlo_simulation(
        base_case=base_case,
        parameter_distributions=distributions,
        objective_function=npv_function,
        n_iterations=100
    )
    
    print(f"\n✓ Resultados Monte Carlo:")
    print(f"  - Média: ${mc_results['mean']/1e6:.1f}M")
    print(f"  - Std Dev: ${mc_results['std']/1e6:.1f}M")
    print(f"  - P10: ${mc_results['p10']/1e6:.1f}M")
    print(f"  - P50 (Mediana): ${mc_results['p50']/1e6:.1f}M")
    print(f"  - P90: ${mc_results['p90']/1e6:.1f}M")


def example_6_cache_performance():
    """Exemplo 6: Sistema de Cache"""
    print_header("EXEMPLO 6: Cache para Performance")
    
    cache = ResultsCache(max_size=100, ttl_seconds=3600)
    print(f"✓ Cache inicializado (max_size=100, ttl=3600s)")
    
    # Função custosa
    def expensive_calculation(n):
        return sum(i**2 for i in range(n)) / n
    
    # Primeira chamada (miss)
    print(f"\n✓ Primeira chamada...")
    result1 = cache.get('calc_1000', expensive_calculation, 1000)
    print(f"  Resultado: {result1:.0f}")
    
    # Segunda chamada (hit)
    print(f"\n✓ Segunda chamada (mesmo parâmetro)...")
    result2 = cache.get('calc_1000', expensive_calculation, 1000)
    print(f"  Resultado: {result2:.0f} (do cache)")
    
    # Terceira chamada (miss)
    print(f"\n✓ Terceira chamada (parâmetro diferente)...")
    result3 = cache.get('calc_2000', expensive_calculation, 2000)
    print(f"  Resultado: {result3:.0f}")
    
    # Estatísticas
    stats = cache.get_statistics()
    print(f"\n✓ Estatísticas do Cache:")
    print(f"  - Hits: {stats['hits']}")
    print(f"  - Misses: {stats['misses']}")
    print(f"  - Taxa de acerto: {stats['hit_rate']:.1f}%")
    print(f"  - Itens em cache: {stats['size']}/{stats['max_size']}")
    print(f"  - Uso: {stats['usage_percent']:.1f}%")


def example_7_intelligent_recommendations(plugin_mgr, project_mgr, project):
    """Exemplo 7: Recomendações Inteligentes"""
    print_header("EXEMPLO 7: Recomendações Inteligentes com IA")
    
    recommender = IntelligentRecommender(plugin_mgr, project_mgr)
    
    print(f"✓ Analisando {len(project_mgr.projects)} projetos no histórico...")
    
    recommendations = recommender.recommend(
        current_reservoir=project.reservoir_data.to_dict(),
        similarity_threshold=0.5
    )
    
    if not recommendations:
        print(f"\n✓ Nenhuma recomendação baseada em histórico (primeiros projetos)")
    else:
        print(f"\n✓ Top 3 Recomendações (baseadas em casos similares):")
        for idx, rec in enumerate(recommendations[:3], 1):
            print(f"\n  {idx}. {rec['method']}")
            print(f"     - Confiança: {rec['confidence']*100:.0f}%")
            print(f"     - Taxa de sucesso: {rec['success_rate']*100:.0f}%")
            print(f"     - Casos similares: {rec['similar_cases_count']}")


def example_8_export_import(project_mgr, project):
    """Exemplo 8: Exportação e Importação"""
    print_header("EXEMPLO 8: Exportação e Importação de Projetos")
    
    # Exportar para JSON
    export_path_json = "projeto_exportado.json"
    success = project_mgr.export_project(
        project.id,
        export_path_json,
        include_results=True
    )
    print(f"✓ Exportado para JSON: {success}")
    print(f"  Arquivo: {export_path_json}")
    
    # Verificar arquivo
    if Path(export_path_json).exists():
        size = Path(export_path_json).stat().st_size
        print(f"  Tamanho: {size/1024:.1f} KB")
    
    # Exportar para Pickle
    export_path_pkl = "projeto_exportado.pkl"
    success = project_mgr.export_project(
        project.id,
        export_path_pkl,
        include_results=True
    )
    print(f"\n✓ Exportado para PKL: {success}")
    print(f"  Arquivo: {export_path_pkl}")


def main():
    """Função principal"""
    print("\n")
    print("█"*70)
    print("█  PetroChamp Advanced v2.0 - Exemplo Completo de Funcionalidades  █")
    print("█"*70)
    
    try:
        # Exemplo 1: Configuração
        config = example_1_configuration()
        
        # Exemplo 2: Gerenciamento de Projetos
        project_mgr, project = example_2_project_management(config)
        
        # Exemplo 3: Sistema de Plugins
        plugin_mgr = PluginManager()
        scores = example_3_screening(plugin_mgr, project)
        
        # Exemplo 4: Análise Econômica
        example_4_economic_analysis(plugin_mgr, project)
        
        # Salvar projeto
        project_mgr.save_project(project)
        
        # Exemplo 5: Sensibilidade
        example_5_sensitivity_analysis()
        
        # Exemplo 6: Cache
        example_6_cache_performance()
        
        # Exemplo 7: Recomendações
        example_7_intelligent_recommendations(plugin_mgr, project_mgr, project)
        
        # Exemplo 8: Exportação
        example_8_export_import(project_mgr, project)
        
        # Resumo final
        print_header("✅ CONCLUSÃO")
        print(f"Todos os exemplos foram executados com sucesso!")
        print(f"\nRecursos demonstrados:")
        print(f"  ✓ Configuração centralizada")
        print(f"  ✓ Gerenciamento de projetos com persistência")
        print(f"  ✓ Sistema de plugins extensível")
        print(f"  ✓ Análise avançada (OAT, Monte Carlo)")
        print(f"  ✓ Cache inteligente")
        print(f"  ✓ Recomendações baseadas em IA")
        print(f"  ✓ Exportação/importação de projetos")
        print(f"\nPróximas etapas:")
        print(f"  1. Implementar interface gráfica")
        print(f"  2. Adicionar mais plugins EOR")
        print(f"  3. Integrar com bancos de dados")
        print(f"  4. Criar API REST")
        print(f"\n")
        
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
