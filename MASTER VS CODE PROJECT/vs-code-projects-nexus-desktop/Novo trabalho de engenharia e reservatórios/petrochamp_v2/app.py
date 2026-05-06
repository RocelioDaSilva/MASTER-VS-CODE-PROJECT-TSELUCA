"""
🚀 PetroChamp v5.0 / v2.0 - Aplicação Principal Integrada

Combina o melhor do código legado com a nova arquitetura modular.
"""

import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
from pathlib import Path

# Adicionar path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from petrochamp_v2.config.settings import (
    get_config, AppConfig, PRODUCTION_CONFIG
)
from petrochamp_v2.core.models import (
    ReservoirData, EORProject, EORMethodType
)
from petrochamp_v2.core.plugins import PluginManager
from petrochamp_v2.core.analysis import SensitivityAnalyzer, HybridEOROptimizer
from petrochamp_v2.data.persistence import ProjectManager, ResultsCache
from petrochamp_v2.core.dashboard import RealtimeDashboard
from petrochamp_v2.core.reporting import AdvancedReportGenerator, ReportMetadata
from petrochamp_v2.ui.v5_integration import (
    SuitabilityVisualizer, V5ToV2Adapter, PetroChampV5GUI,
    SuitabilityLevel, ColorScheme
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PetroChampApplication:
    """Aplicação integrada PetroChamp v5.0/v2.0"""
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.config = get_config()
        self.plugin_manager = PluginManager()
        self.project_manager = ProjectManager()
        self.cache = ResultsCache()
        self.analyzer = SensitivityAnalyzer(self.config)
        self.optimizer = HybridEOROptimizer(self.config)
        self.dashboard = RealtimeDashboard()
        self.adapter = V5ToV2Adapter()
        
        logger.info("✅ Aplicação PetroChamp inicializada")
        self._print_welcome()
    
    def _print_welcome(self):
        """Imprime mensagem de boas-vindas."""
        print("\n" + "="*80)
        print("🌟 PETROCHAMP v5.0 / v2.0 - SISTEMA INTEGRADO DE TRIAGEM EOR 🌟")
        print("="*80)
        print("\n📊 Módulos Carregados:")
        print("  ✓ Configuração centralizada")
        print("  ✓ Plugin Manager (EOR Methods)")
        print("  ✓ Project Manager (Persistência)")
        print("  ✓ SensitivityAnalyzer (OAT, Tornado, MC)")
        print("  ✓ HybridEOROptimizer")
        print("  ✓ RealtimeDashboard")
        print("  ✓ AdvancedReportGenerator")
        print("  ✓ V5ToV2Adapter (Compatibilidade)")
        print("\n")
    
    def demo_workflow(self):
        """Demonstra um workflow completo."""
        print("📌 INICIANDO WORKFLOW DE DEMONSTRAÇÃO\n")
        
        # 1. Criar projeto
        print("1️⃣  Criando projeto EOR...")
        reservoir_data = ReservoirData(
            name="Reservatório Teste",
            location="Bacia de Santos",
            depth=2500.0,
            temperature=75.0,
            pressure=250.0,
            api_gravity=28.5,
            viscosity=125.0,
            permeability=800.0,
            porosity=18.5
        )
        
        project = EORProject(
            name="Avaliação de Métodos EOR",
            reservoir=reservoir_data,
            selected_methods=[EORMethodType.STEAM_INJECTION, EORMethodType.CO2_MISCIBLE]
        )
        
        print(f"   ✓ Projeto criado: {project.name}")
        print(f"   ✓ Reservoir: {reservoir_data.name}")
        print(f"   ✓ Métodos: {len(project.selected_methods)}\n")
        
        # 2. Análise de sensibilidade
        print("2️⃣  Executando análise de sensibilidade (One-at-a-Time)...")
        try:
            oat_result, oat_fig = self.analyzer.analyze_one_at_a_time(
                reservoir_data, ['temperature', 'viscosity']
            )
            print(f"   ✓ Análise OAT completada")
            print(f"   ✓ Parâmetros testados: {len(oat_result)}\n")
        except Exception as e:
            print(f"   ⚠️  OAT: {e}\n")
        
        # 3. Análise Tornado
        print("3️⃣  Executando análise Tornado...")
        try:
            tornado_result, tornado_fig = self.analyzer.tornado_analysis(
                reservoir_data,
                parameter_ranges={'temperature': (50, 100), 'viscosity': (50, 200)}
            )
            print(f"   ✓ Análise Tornado completada")
            print(f"   ✓ Parâmetros: {len(tornado_result)}\n")
        except Exception as e:
            print(f"   ⚠️  Tornado: {e}\n")
        
        # 4. Análise Monte Carlo
        print("4️⃣  Executando simulação Monte Carlo (5000 iterações)...")
        try:
            mc_result, mc_fig = self.analyzer.monte_carlo_simulation(
                reservoir_data,
                parameter_distributions={
                    'temperature': ('normal', 75, 10),
                    'pressure': ('uniform', 200, 300)
                },
                iterations=5000
            )
            print(f"   ✓ Simulação MC completada")
            print(f"   ✓ P10: {mc_result['P10']:.2f}%")
            print(f"   ✓ P50: {mc_result['P50']:.2f}%")
            print(f"   ✓ P90: {mc_result['P90']:.2f}%\n")
        except Exception as e:
            print(f"   ⚠️  MC: {e}\n")
        
        # 5. Otimização híbrida
        print("5️⃣  Executando otimização híbrida...")
        try:
            optimal, score_dict = self.optimizer.find_optimal_combination(
                reservoir_data,
                project.selected_methods
            )
            print(f"   ✓ Combinação ótima encontrada")
            print(f"   ✓ Score de sinergia: {score_dict.get('synergy_score', 0):.2f}\n")
        except Exception as e:
            print(f"   ⚠️  Híbrida: {e}\n")
        
        # 6. Gerar relatório
        print("6️⃣  Gerando relatório multi-formato...")
        try:
            report = AdvancedReportGenerator(
                metadata=ReportMetadata(
                    title="Relatório de Triagem EOR",
                    author="PetroChamp v2.0",
                    version="5.0"
                )
            )
            
            report.add_section("Resumo Executivo")
            report.add_text("Análise completa de métodos EOR para reservatório teste.")
            
            report.add_section("Dados do Reservatório")
            report.add_table(
                data={
                    'Parâmetro': ['Nome', 'Localização', 'Profundidade', 'Temperatura'],
                    'Valor': [
                        reservoir_data.name,
                        reservoir_data.location,
                        f"{reservoir_data.depth} m",
                        f"{reservoir_data.temperature} °C"
                    ]
                },
                title="Características do Reservatório"
            )
            
            print("   ✓ Relatório estruturado")
            print("   ✓ Formatos: HTML, JSON, Markdown, Excel, PDF")
            print(f"   ✓ Seções: {len(report._sections)}\n")
        
        except Exception as e:
            print(f"   ⚠️  Relatório: {e}\n")
        
        # 7. Dashboard em tempo real
        print("7️⃣  Ativando dashboard em tempo real...")
        try:
            self.dashboard.start()
            self.dashboard.add_alert("INFO", "Sistema", "Análise iniciada")
            stats = self.dashboard.get_statistics_summary()
            print(f"   ✓ Dashboard ativado")
            print(f"   ✓ Métricas coletadas: {len(stats)}\n")
            self.dashboard.stop()
        except Exception as e:
            print(f"   ⚠️  Dashboard: {e}\n")
        
        print("✅ WORKFLOW DE DEMONSTRAÇÃO CONCLUÍDO\n")
        print("="*80 + "\n")
    
    def run_gui(self):
        """Executa interface gráfica."""
        gui = PetroChampV5GUI()
        gui.run()


def main():
    """Função principal."""
    try:
        app = PetroChampApplication()
        
        # Menu de opções
        print("📋 OPÇÕES DISPONÍVEIS:")
        print("  1. Demo Workflow (Não-interativo)")
        print("  2. Interface Gráfica")
        print("  3. Sair")
        print()
        
        choice = input("Escolha uma opção (1-3): ").strip()
        
        if choice == "1":
            app.demo_workflow()
        elif choice == "2":
            print("Iniciando interface gráfica...")
            app.run_gui()
        elif choice == "3":
            print("Saindo...")
        else:
            print("Opção inválida!")
    
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
