#!/usr/bin/env python3
"""
🎯 Exemplo Completo com Dashboard e Relatórios - PetroChamp v2.0

Demonstra uso de Dashboard em tempo real e geração de relatórios avançados.
"""

from petrochamp_v2 import (
    PluginManager,
    ProjectManager,
    ReservoirData,
    SensitivityAnalyzer,
    HybridEOROptimizer,
    IntelligentRecommender,
    RealtimeDashboard,
    AdvancedReportGenerator,
    ReportMetadata,
)
import pandas as pd
import numpy as np
from pathlib import Path
import time


def demo_dashboard():
    """Demonstra dashboard em tempo real."""
    print("\n" + "="*80)
    print("📊 DEMO 1: DASHBOARD EM TEMPO REAL")
    print("="*80)
    
    # Inicializar dashboard
    dashboard = RealtimeDashboard(update_interval=1)
    
    # Callback para atualizar quando há mudanças
    def on_update(metrics):
        print(f"\n📈 Atualização do Dashboard:")
        print(f"   • Projetos: {metrics.total_projects}")
        print(f"   • Análises: {metrics.total_analyses}")
        print(f"   • Score Médio: {metrics.avg_suitability_score:.1f}%")
        print(f"   • Taxa de Cache: {metrics.cache_hit_rate*100:.1f}%")
        print(f"   • Sucesso: {metrics.success_rate*100:.1f}%")
    
    # Adicionar callback
    dashboard.add_callback(on_update)
    
    # Iniciar dashboard
    dashboard.start()
    print("\n✅ Dashboard iniciado (rodando por 5 segundos)...")
    
    # Simular alertas
    dashboard.add_alert(
        level="INFO",
        title="Projeto Criado",
        message="Novo projeto adicionado ao sistema",
        data={'project_id': 'proj_001', 'name': 'Projeto EOR X'}
    )
    
    dashboard.add_alert(
        level="WARNING",
        title="Cache em Limite",
        message="Uso de cache atingiu 80%",
        data={'cache_usage': 0.80}
    )
    
    # Aguardar
    time.sleep(5)
    
    # Parar dashboard
    dashboard.stop()
    print("\n✅ Dashboard parado")
    
    # Exibir estatísticas
    stats = dashboard.get_statistics_summary()
    print(f"\n📊 Sumário Final:")
    print(f"   • Timestamp: {stats.get('timestamp', 'N/A')}")
    print(f"   • Projetos Totais: {stats.get('total_projects', 0)}")
    print(f"   • Score Médio: {stats.get('avg_suitability_score', 0):.1f}%")
    print(f"   • Taxa de Sucesso: {stats.get('success_rate', 0):.1f}%")
    print(f"   • Alertas: {stats.get('num_alerts', 0)}")
    
    # Gerar figura de overview
    print("\n📈 Gerando gráficos de dashboard...")
    fig = dashboard.create_overview_figure()
    fig.savefig('reports/dashboard_overview.png', dpi=100, bbox_inches='tight')
    print("✅ Gráfico salvo: reports/dashboard_overview.png")
    
    return dashboard


def demo_reporting():
    """Demonstra geração de relatórios avançados."""
    print("\n" + "="*80)
    print("📄 DEMO 2: GERAÇÃO DE RELATÓRIOS AVANÇADOS")
    print("="*80)
    
    # Criar gerador de relatórios
    metadata = ReportMetadata(
        title="Relatório de Triagem EOR - PetroChamp v2.0",
        author="Sistema PetroChamp",
        description="Análise completa de métodos EOR para campo de petróleo",
        confidential=False
    )
    
    report = AdvancedReportGenerator(metadata)
    
    # Adicionar seções
    print("\n📝 Adicionando seções ao relatório...")
    
    # 1. Introdução
    report.add_text(
        "Introdução",
        """
        Este relatório apresenta uma análise completa de métodos de recuperação
        secundária e terciária (EOR) para o campo de petróleo.
        
        A análise utiliza critérios técnicos, econômicos, operacionais e ambientais
        para classificar os métodos mais adequados para as condições específicas do reservatório.
        """
    )
    
    # 2. Dados do Reservatório
    reservoir_data = {
        'API Gravity': 28.5,
        'Viscosidade (cp)': 450,
        'Profundidade (m)': 1250,
        'Porosidade (%)': 22,
        'Permeabilidade (mD)': 120,
        'Temperatura (°C)': 58,
        'Saturação de Óleo (%)': 55,
    }
    report.add_metrics(
        "Dados do Reservatório",
        reservoir_data
    )
    
    # 3. Tabela de Métodos EOR
    eor_methods = pd.DataFrame({
        'Método EOR': ['Injeção de Vapor', 'CO2 Miscível', 'Gás Não-Miscível', 'Polímeros'],
        'Score Técnico': [85, 78, 72, 68],
        'Viabilidade Econômica': [72, 85, 78, 65],
        'Score Geral': [82, 79, 73, 66],
        'Recomendação': ['✅ Altamente Recomendado', '✅ Recomendado', '⚠️ Possível', '❌ Não Recomendado'],
    })
    report.add_table(
        "Análise Comparativa de Métodos EOR",
        eor_methods
    )
    
    # 4. Análise Técnica
    report.add_text(
        "Análise Técnica",
        """
        **Método Recomendado: Injeção de Vapor**
        
        Justificativa técnica:
        • API entre 10-30°: ✅ Ótimo (API = 28.5)
        • Viscosidade 100-1000 cp: ✅ Excelente (Visc = 450 cp)
        • Profundidade <2000m: ✅ Adequado (Prof = 1250m)
        • Formação terrígena: ✅ Aplicável
        
        **Benefícios Esperados:**
        • Aumento de recuperação: 20-35% do OOIP
        • Fator de recuperação final: 0.60-0.65
        • Payback period: 8-10 anos
        """
    )
    
    # 5. Análise Econômica
    economic_data = {
        'CAPEX (MM$/ano)': 2.5,
        'OPEX (MM$/ano)': 0.8,
        'NPV (MM$)': 45.2,
        'IRR (%)': 22.5,
        'Payback (anos)': 9.2,
    }
    report.add_metrics(
        "Análise Econômica",
        economic_data
    )
    
    # 6. Recomendações
    report.add_text(
        "Recomendações",
        """
        1. **Curto Prazo (0-12 meses):**
           - Conduzir estudo de injeção de vapor
           - Avaliar disponibilidade de energia
           - Fazer análise de sensibilidade econômica
        
        2. **Médio Prazo (1-2 anos):**
           - Projeto piloto de injeção de vapor
           - Monitoramento de produção
           - Análise de sinergias com outros métodos
        
        3. **Longo Prazo (2+ anos):**
           - Implementação em full field
           - Otimização operacional
           - Expansão para outros campos
        """
    )
    
    # Criar diretório para relatórios
    Path("reports").mkdir(exist_ok=True)
    
    # Exportar em diferentes formatos
    print("\n💾 Exportando relatórios...")
    
    # HTML
    report.save("reports/relatorio_eor.html", format="html")
    print("✅ HTML: reports/relatorio_eor.html")
    
    # JSON
    report.save("reports/relatorio_eor.json", format="json")
    print("✅ JSON: reports/relatorio_eor.json")
    
    # Markdown
    report.save("reports/relatorio_eor.md", format="markdown")
    print("✅ Markdown: reports/relatorio_eor.md")
    
    # Excel
    try:
        report.save("reports/relatorio_eor.xlsx", format="excel")
        print("✅ Excel: reports/relatorio_eor.xlsx")
    except ImportError:
        print("⚠️ Excel: módulo openpyxl não instalado")
    
    # PDF
    try:
        report.save("reports/relatorio_eor.pdf", format="pdf")
        print("✅ PDF: reports/relatorio_eor.pdf")
    except ImportError:
        print("⚠️ PDF: módulo reportlab não instalado")
    
    return report


def demo_full_workflow():
    """Demonstra workflow completo com dashboard e relatórios."""
    print("\n" + "="*80)
    print("🎯 DEMO 3: WORKFLOW COMPLETO")
    print("="*80)
    
    # Inicializar componentes
    pm = PluginManager()
    project_mgr = ProjectManager()
    dashboard = RealtimeDashboard()
    dashboard.start()
    
    print("\n✅ Componentes inicializados")
    
    # Criar projeto
    print("\n📝 Criando projeto...")
    reservoir = ReservoirData(
        api_gravity=28.5,
        viscosity=450,
        depth=1250,
        porosity=0.22,
        permeability=120,
        temperature=58,
        saturation_oil=0.55,
        saturation_water=0.45,
        net_to_gross=0.85,
        formation="Arenito"
    )
    
    project = project_mgr.create_project(
        name="Campo EOR X",
        location="Bacia de Santos",
        reservoir_data=reservoir
    )
    project_mgr.save_project(project)
    print(f"✅ Projeto criado: {project.id}")
    
    # Triagem de métodos
    print("\n🔍 Realizando triagem de métodos...")
    scores = pm.calculate_all_suitability_scores(reservoir.to_dict())
    top_methods = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for method, score in top_methods:
        print(f"   • {method}: {score:.1f}%")
    
    # Adicionar alerta
    dashboard.add_alert(
        "INFO",
        "Triagem Concluída",
        f"Top método: {top_methods[0][0]} com score {top_methods[0][1]:.1f}%"
    )
    
    # Análise de sensibilidade
    print("\n📊 Executando análise de sensibilidade...")
    analyzer = SensitivityAnalyzer()
    
    def objective_func(params):
        return params.get('api', 25) * 2 + params.get('depth', 1000) * 0.01
    
    try:
        oat = analyzer.analyze_one_at_a_time(
            base_case={'api': 28.5, 'depth': 1250},
            parameter_ranges={'api': (20, 35), 'depth': (1000, 1500)},
            objective_function=objective_func,
            steps=5
        )
        print("✅ Análise OAT concluída")
    except Exception as e:
        print(f"⚠️ Análise OAT: {str(e)[:50]}...")
    
    # Gerar relatório final
    print("\n📄 Gerando relatório final...")
    report = AdvancedReportGenerator(
        ReportMetadata(
            title="Relatório Final - Workflow Completo",
            description="Resultado do workflow de triagem e análise EOR"
        )
    )
    
    report.add_metrics("Top 5 Métodos", dict(top_methods[:5]))
    report.add_metrics("Dados do Reservatório", {
        'API Gravity': reservoir.api_gravity,
        'Viscosidade (cp)': reservoir.viscosity,
        'Profundidade (m)': reservoir.depth,
        'Porosidade (%)': f"{reservoir.porosity*100:.1f}",
    })
    
    Path("reports").mkdir(exist_ok=True)
    report.save("reports/workflow_final.html", format="html")
    print("✅ Relatório: reports/workflow_final.html")
    
    # Parar dashboard
    dashboard.stop()
    print("\n✅ Workflow concluído")


def main():
    """Executa todas as demonstrações."""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + "🎯 EXEMPLOS COMPLETOS - Dashboard e Relatórios".center(78) + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Demo 1: Dashboard
        demo_dashboard()
        
        # Demo 2: Relatórios
        demo_reporting()
        
        # Demo 3: Workflow Completo
        demo_full_workflow()
        
        print("\n" + "="*80)
        print("✅ TODAS AS DEMONSTRAÇÕES CONCLUÍDAS COM SUCESSO!")
        print("="*80)
        print("\n📁 Arquivos gerados em: ./reports/")
        print("\n✨ Próximos passos:")
        print("   1. Explore os relatórios em ./reports/")
        print("   2. Customize o ReportGenerator conforme necessário")
        print("   3. Integre o Dashboard em sua aplicação")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
