"""
EXEMPLO COMPLETO: MÓDULO DE SCREENING AVANÇADO COM VALIDAÇÃO TÉCNICA
=====================================================================

Demonstra como usar o novo módulo de screening avançado, validação de
consistência de dados, critérios offshore/Angola e cálculo de eficiência.

Este arquivo implementa:
1. Perguntas de screening técnico (Tabela 4 do artigo)
2. Validação de consistência de dados
3. Análise offshore para campos de Angola
4. Cálculo de número capilar e eficiência
5. Análise integrada de viabilidade
"""

import sys
import numpy as np
from typing import Dict, List, Tuple

# Importar classes do v7
sys.path.insert(0, '.')

try:
    from v7 import (
        AdvancedScreeningQuestions,
        OffshoreSpecificCriteria,
        EfficiencyCalculator,
        DataValidator,
        TechnicalRedFlags,
        EORScreeningEngine
    )
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de executar este script no diretório de v7.py")
    sys.exit(1)


# ============================================================================
# DADOS DE CAMPOS DE EXEMPLO - ANGOLA
# ============================================================================

CAMPO_BLOCO15_ONSHORE = {
    "nome": "Campo Onshore - Bloco 15 (Maduro)",
    "bloco": "Bloco 15",
    "tipo_campo": "Onshore/Transição",
    "profundidade_agua": 50,  # m subsea (muito raso)
    "profundidade": 1200,     # m estrutural
    "API": 18.5,              # Óleo pesado
    "Viscosidade": 850,       # cP muito alto
    "Porosidade": 22,         # %
    "Permeabilidade": 180,    # mD
    "Saturação de Óleo": 62,  # %
    "Saturação de Água": 35,  # %
    "Espessura": 45,          # m
    "Temperatura": 55,        # °C
    "Pressão": 350,           # psi
    "Salinidade": 85000,      # ppm
    "TAN": 0.85,              # mg KOH/g
    "pH": 7.2,                # -
}

CAMPO_BLOCO17_OFFSHORE = {
    "nome": "Campo Offshore Profundo - Bloco 17",
    "bloco": "Bloco 17",
    "tipo_campo": "Offshore Profundo",
    "profundidade_agua": 800,  # m subsea
    "profundidade": 2800,      # m estrutural
    "API": 32.5,               # Óleo leve
    "Viscosidade": 8.5,        # cP baixa
    "Porosidade": 18,          # %
    "Permeabilidade": 250,     # mD
    "Saturação de Óleo": 55,   # %
    "Saturação de Água": 43,   # %
    "Espessura": 38,           # m
    "Temperatura": 95,         # °C
    "Pressão": 1250,           # psi
    "Salinidade": 35000,       # ppm (água do mar)
    "TAN": 0.15,               # mg KOH/g
    "pH": 7.8,                 # -
}

CAMPO_BLOCO18_ULTRAPROFUNDO = {
    "nome": "Campo Ultraprofundo - Bloco 18",
    "bloco": "Bloco 18",
    "tipo_campo": "Offshore Ultraprofundo",
    "profundidade_agua": 1200,  # m subsea
    "profundidade": 3500,       # m estrutural
    "API": 24.0,                # Óleo médio-pesado
    "Viscosidade": 120,         # cP
    "Porosidade": 20,           # %
    "Permeabilidade": 150,      # mD
    "Saturação de Óleo": 58,    # %
    "Saturação de Água": 38,    # %
    "Espessura": 35,            # m
    "Temperatura": 115,         # °C
    "Pressão": 1800,            # psi
    "Salinidade": 40000,        # ppm
    "TAN": 0.45,                # mg KOH/g
    "pH": 7.5,                  # -
}


# ============================================================================
# FUNÇÕES DE ANÁLISE
# ============================================================================

def print_header(titulo: str, sublevel: int = 0):
    """Imprime cabeçalho formatado."""
    if sublevel == 0:
        print("\n" + "=" * 80)
        print(f"  {titulo}".upper())
        print("=" * 80)
    elif sublevel == 1:
        print("\n" + "-" * 80)
        print(f"  {titulo}")
        print("-" * 80)
    else:
        print(f"\n  ► {titulo}")


def analyze_screening_questions(method_name: str):
    """Analisa perguntas de screening para um método específico."""
    print_header(f"Perguntas de Screening - {method_name}", 1)
    
    questions = AdvancedScreeningQuestions.get_questions_by_method(method_name)
    category = AdvancedScreeningQuestions.get_category(method_name)
    
    print(f"Categoria: {category}")
    print(f"Número de perguntas críticas: {len(questions)}\n")
    
    for i, question in enumerate(questions, 1):
        print(f"  {i}. {question}")


def analyze_data_consistency(campo: Dict, campo_nome: str):
    """Valida consistência de dados do campo."""
    print_header(f"Validação de Consistência - {campo_nome}", 1)
    
    valid, messages = DataValidator.validate_consistency(campo)
    
    if valid:
        print("  ✓ Dados geometricamente consistentes (sem erros críticos)")
    else:
        print("  ✗ Erros detectados:")
        for msg in messages[:3]:  # Mostrar apenas 3 primeiros
            print(f"    - {msg}")
    
    if messages:
        print(f"\n  Aviso/Sugestões ({len(messages)} total):")
        for msg in messages[3:]:
            if "Aviso" in msg or "Verificar" in msg:
                print(f"    ⚠ {msg[:75]}...")


def analyze_offshore_feasibility(campo: Dict, campo_nome: str):
    """Analisa viabilidade em ambiente offshore."""
    print_header(f"Análise Offshore - {campo_nome}", 1)
    
    depth_subsea = campo.get("profundidade_agua", 0)
    depth_structural = campo.get("profundidade", 0)
    
    # Classificação
    classification = OffshoreSpecificCriteria.get_water_depth_classification(depth_subsea)
    cost_multiplier = OffshoreSpecificCriteria.get_cost_multiplier(depth_subsea)
    
    print(f"Profundidade de lâmina d'água: {depth_subsea} m")
    print(f"Classificação (SPE IADC): {classification}")
    print(f"Multiplicador de custo operacional: {cost_multiplier}x\n")
    
    # Verificar blocos de Angola
    bloco = campo.get("bloco", "")
    if bloco in OffshoreSpecificCriteria.ANGOLA_BLOCKS:
        bloco_info = OffshoreSpecificCriteria.ANGOLA_BLOCKS[bloco]
        print(f"Informações do Bloco {bloco}:")
        print(f"  - Tipo: {bloco_info['tipo']}")
        print(f"  - Status: {bloco_info['status']}")
        print(f"  - Operador: {bloco_info['operador']}\n")
    
    # Avaliar métodos por viabilidade offshore
    print("Viabilidade de métodos por profundidade:\n")
    
    test_methods = [
        "Injeção de Vapor",
        "Injeção de CO2 Miscível",
        "Injeção de Polímeros",
        "EOR Térmico para Águas Profundas"
    ]
    
    for method in test_methods:
        viable, reason = OffshoreSpecificCriteria.validate_offshore_feasibility(
            method, depth_subsea, depth_structural
        )
        status = "✓ Viável" if viable else "✗ Inviável"
        print(f"  {status:12} | {method:35} | {reason[:50]}...")


def analyze_capillary_number(campo: Dict, campo_nome: str):
    """Calcula e interpreta número capilar."""
    print_header(f"Análise de Número Capilar - {campo_nome}", 1)
    
    # Parâmetros para cálculo
    velocity = 1.0  # ft/dia (típico)
    viscosity = campo.get("Viscosidade", 100)  # cP
    ift_oil_water = 25  # dinas/cm (típico óleo-água)
    contact_angle = 30  # graus (parcialmente molhável)
    
    # Calcular número capilar
    nc = EfficiencyCalculator.calculate_capillary_number(
        velocity, viscosity, ift_oil_water, contact_angle
    )
    
    # Interpretar
    interpretation = EfficiencyCalculator.interpret_capillary_number(nc)
    
    print(f"Parâmetros de entrada:")
    print(f"  - Velocidade: {velocity} ft/dia")
    print(f"  - Viscosidade do óleo: {viscosity} cP")
    print(f"  - Tensão interfacial: {ift_oil_water} dinas/cm")
    print(f"  - Ângulo de contato: {contact_angle}°\n")
    
    print(f"Resultado:")
    print(f"  Número Capilar (Nc): {nc:.2e}")
    print(f"  Log₁₀(Nc): {interpretation['log_nc']:.2f}")
    print(f"  Nível: {interpretation['level']}")
    print(f"  Descrição: {interpretation['description']}")
    print(f"  Potencial de recuperação: {interpretation['recovery_potential']}\n")


def analyze_recovery_efficiency(campo: Dict, campo_nome: str):
    """Calcula eficiência de recuperação."""
    print_header(f"Análise de Eficiência de Recuperação - {campo_nome}", 1)
    
    # Parâmetros típicos
    velocity = 1.5  # ft/dia
    viscosity = campo.get("Viscosidade", 100)  # cP
    ift = 20  # dinas/cm
    contact_angle = 25  # graus
    
    # Eficiência microscópica
    psd = EfficiencyCalculator.calculate_microscopic_displacement_efficiency(
        ift, contact_angle, viscosity, viscosity * 0.5, velocity
    )
    
    # Eficiência macroscópica
    mobility_ratio = 1.2
    aspect_ratio = 3.0
    heterogeneity = 0.85
    
    se = EfficiencyCalculator.calculate_sweep_efficiency(
        mobility_ratio, aspect_ratio, heterogeneity
    )
    
    # Fator de recuperação
    rf_result = EfficiencyCalculator.calculate_recovery_factor(
        psd, se, drainage=0.95, time_factor=0.9
    )
    
    print("Componentes de Eficiência (Equação 1: RF = PSD × SE × D × T):\n")
    print(f"  PSD (Deslocamento Microscópico):  {psd*100:6.1f}%")
    print(f"  SE (Varredura Macroscópica):      {se*100:6.1f}%")
    print(f"  D (Drenagem):                     {rf_result['D']*100:6.1f}%")
    print(f"  T (Fator Temporal):               {rf_result['T']:6.2f}x\n")
    
    print(f"  ════════════════════════════════")
    print(f"  RF TOTAL (Fator de Recuperação):  {rf_result['RF_percentage']:6.1f}%")
    print(f"  ════════════════════════════════\n")
    
    # Interpretação
    if rf_result['RF_percentage'] > 30:
        quality = "EXCELENTE"
    elif rf_result['RF_percentage'] > 20:
        quality = "BOM"
    elif rf_result['RF_percentage'] > 10:
        quality = "MODERADO"
    else:
        quality = "BAIXO"
    
    print(f"  Qualidade de recuperação: {quality}")


def analyze_red_flags(campo: Dict, campo_nome: str):
    """Verifica red flags técnicas para o campo."""
    print_header(f"Análise de Red Flags Técnicas - {campo_nome}", 1)
    
    # Usar EORScreeningEngine para gerar scores
    try:
        engine = EORScreeningEngine()
        
        # Verificar inviabilidades
        all_flags = TechnicalRedFlags.check_all_methods_inviability(campo, engine.methods)
        
        viable_count = 0
        inviable_methods = []
        
        for method, flags in all_flags.items():
            if flags:  # Se há flags
                inviable_methods.append((method, len(flags)))
            else:
                viable_count += 1
        
        total_methods = len(engine.methods)
        inviable_count = len(inviable_methods)
        
        print(f"Resultado da Validação Técnica:\n")
        print(f"  Métodos viáveis:   {viable_count:2d}/{total_methods}")
        print(f"  Métodos inviáveis: {inviable_count:2d}/{total_methods}\n")
        
        if inviable_methods:
            print("  Métodos com inviabilidades detectadas:\n")
            for method, num_flags in sorted(inviable_methods, key=lambda x: x[1], reverse=True):
                print(f"    ✗ {method:40} ({num_flags} red flags)")
        
        # Gerar relatório
        report = TechnicalRedFlags.get_inviability_report(campo, engine.methods)
        
        print(f"\n  {report[:200]}...")
        
    except Exception as e:
        print(f"  Erro ao analisar red flags: {e}")


def analyze_integrated_assessment(campo: Dict, campo_nome: str):
    """Análise integrada completa do campo."""
    print_header(f"Avaliação Integrada - {campo_nome}", 0)
    
    print(f"\n📍 LOCALIZAÇÃO E CARACTERÍSTICAS")
    print(f"  Campo: {campo.get('nome', campo_nome)}")
    print(f"  Bloco: {campo.get('bloco', 'N/A')}")
    print(f"  Tipo: {campo.get('tipo_campo', 'N/A')}")
    
    print(f"\n⛰️  PARÂMETROS ESTRUTURAIS")
    print(f"  Profundidade subsea: {campo.get('profundidade_agua', 0)} m")
    print(f"  Profundidade estrutural: {campo.get('profundidade', 0)} m")
    print(f"  Espessura da camada: {campo.get('Espessura', 0)} m")
    
    print(f"\n🛢️  PROPRIEDADES DO ÓLEO")
    print(f"  API: {campo.get('API', 0):.1f}°")
    print(f"  Viscosidade: {campo.get('Viscosidade', 0):.1f} cP")
    print(f"  TAN: {campo.get('TAN', 0):.2f} mg KOH/g")
    
    print(f"\n🪨 PROPRIEDADES DA ROCHA")
    print(f"  Porosidade: {campo.get('Porosidade', 0):.1f}%")
    print(f"  Permeabilidade: {campo.get('Permeabilidade', 0):.1f} mD")
    print(f"  Saturação de óleo: {campo.get('Saturação de Óleo', 0):.1f}%")
    
    # Validar consistência
    valid, messages = DataValidator.validate_consistency(campo)
    consistency_status = "✓ Consistente" if valid else f"⚠ {len(messages)} aviso(s)"
    print(f"  Status de consistência: {consistency_status}")
    
    # Eficiência
    try:
        psd = 0.7
        se = 0.75
        rf = EfficiencyCalculator.calculate_recovery_factor(psd, se, 0.95, 0.9)
        print(f"\n📊 ESTIMATIVA DE RECUPERAÇÃO")
        print(f"  Fator de recuperação (RF): {rf['RF_percentage']:.1f}%")
    except:
        pass


# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal de execução."""
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  MÓDULO DE SCREENING AVANÇADO PARA EOR - EXEMPLO COMPLETO".center(78) + "█")
    print("█" + "  Validação Técnica, Critérios Offshore e Análise de Eficiência".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    campos = [
        (CAMPO_BLOCO15_ONSHORE, "CAMPO BLOCO 15 (Onshore Maduro)"),
        (CAMPO_BLOCO17_OFFSHORE, "CAMPO BLOCO 17 (Offshore Profundo)"),
        (CAMPO_BLOCO18_ULTRAPROFUNDO, "CAMPO BLOCO 18 (Offshore Ultraprofundo)")
    ]
    
    for campo, nome in campos:
        # Análise integrada
        analyze_integrated_assessment(campo, nome)
        
        # Validação de consistência
        analyze_data_consistency(campo, nome)
        
        # Análise offshore
        analyze_offshore_feasibility(campo, nome)
        
        # Eficiência
        analyze_capillary_number(campo, nome)
        analyze_recovery_efficiency(campo, nome)
        
        # Red flags
        analyze_red_flags(campo, nome)
        
        # Exemplo de perguntas para melhor método
        print_header("Exemplo: Perguntas de Screening para Melhor Método", 1)
        analyze_screening_questions("Injeção de CO2 Miscível")
    
    # Resumo comparativo
    print_header("RESUMO COMPARATIVO DOS CAMPOS", 0)
    print("\n📊 MATRIZ DE CARACTERÍSTICAS\n")
    
    print(f"{'Campo':<35} {'Profundidade':<12} {'API':<8} {'Viscosidade':<12} {'Tipo':<20}")
    print("-" * 90)
    
    for campo, nome in campos:
        campo_name = campo.get('nome', nome)[:33]
        depth = f"{campo.get('profundidade_agua', 0)}m subsea"
        api = f"{campo.get('API', 0):.1f}°"
        visc = f"{campo.get('Viscosidade', 0):.0f} cP"
        tipo = campo.get('tipo_campo', 'N/A')
        
        print(f"{campo_name:<35} {depth:<12} {api:<8} {visc:<12} {tipo:<20}")
    
    print("\n" + "█" * 80)
    print("█" + "  ANÁLISE CONCLUÍDA COM SUCESSO".center(78) + "█")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
