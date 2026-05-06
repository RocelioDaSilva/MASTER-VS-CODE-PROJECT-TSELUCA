#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE USO - SISTEMA DE RED FLAGS TÉCNICAS
================================================

Demonstra como utilizar o novo sistema TechnicalRedFlags para detecção
automática de inviabilidades técnicas em projetos EOR baseados em dados
de campos angolanos.

Autor: PetroChamp v7.0
Data: Janeiro 2026
"""

from typing import Dict, Any, List

# ============================================================================
# DADOS DE EXEMPLO - CAMPOS HIPOTÉTICOS
# ============================================================================

# Campo 1: Bloco 15 Angola (Onshore, API pesado)
CAMPO_BLOCO15 = {
    "nome": "Campo Onshore Bloco 15",
    "tipo": "onshore",
    "API": 18.5,
    "Viscosidade": 850,  # cP
    "Profundidade": 1200,  # m
    "Permeabilidade": 180,  # mD
    "Porosidade": 24,  # %
    "Saturação de Óleo": 62,  # %
    "Saturação de Água": 38,  # %
    "Temperatura": 65,  # °C
    "Pressão": 1500,  # psi
    "Salinidade": 85000,  # ppm
    "Espessura": 22,  # m
    "TAN": 0.45,  # mg KOH/g
    "pH": 7.2,
    "Dip": 12  # °
}

# Campo 2: Bloco 17 Angola (Deepwater, API leve)
CAMPO_BLOCO17 = {
    "nome": "Campo Deepwater Bloco 17",
    "tipo": "offshore-profundo",
    "profundidade_agua": 1800,  # m
    "API": 32.5,
    "Viscosidade": 8.5,  # cP
    "Profundidade": 2800,  # m (subsea)
    "Permeabilidade": 520,  # mD
    "Porosidade": 26,  # %
    "Saturação de Óleo": 68,  # %
    "Saturação de Água": 32,  # %
    "Temperatura": 92,  # °C
    "Pressão": 2850,  # psi
    "Salinidade": 35000,  # ppm (água do mar)
    "Espessura": 35,  # m
    "TAN": 0.15,  # mg KOH/g
    "pH": 7.8,
    "Dip": 8  # °
}

# Campo 3: Campo Problemático (múltiplas red flags)
CAMPO_PROBLEMATICO = {
    "nome": "Campo com Limitações Técnicas",
    "tipo": "onshore-profundo",
    "API": 12,  # Óleo muito pesado
    "Viscosidade": 3500,  # cP - Viscosidade extremamente alta
    "Profundidade": 4200,  # m - MUITO PROFUNDO
    "Permeabilidade": 2.5,  # mD - MUITO BAIXO
    "Porosidade": 18,  # %
    "Saturação de Óleo": 45,  # %
    "Saturação de Água": 55,  # %
    "Temperatura": 145,  # °C - ALTA
    "Pressão": 3800,  # psi
    "Salinidade": 250000,  # ppm - MUITO ALTA
    "Espessura": 3,  # m - MUITO FINO
    "TAN": 0.08,  # mg KOH/g - BAIXO
    "pH": 4.2,  # ÁCIDO
    "Dip": 3  # ° - QUASE HORIZONTAL
}

# Campo 4: Campo com Potencial (LoSal)
CAMPO_LOSAL = {
    "nome": "Campo Candidato para LoSal",
    "tipo": "onshore-maduro",
    "API": 28,
    "Viscosidade": 18,  # cP
    "Profundidade": 1500,  # m
    "Permeabilidade": 450,  # mD
    "Porosidade": 25,  # %
    "Saturação de Óleo": 52,  # %
    "Saturação de Água": 48,  # %
    "Temperatura": 75,  # °C
    "Pressão": 1850,  # psi
    "Salinidade": 145000,  # ppm - ALTA (LoSal ideal)
    "Espessura": 18,  # m
    "TAN": 0.35,  # mg KOH/g
    "pH": 7.5,
    "Dip": 15  # °
}

# ============================================================================
# DEMONSTRAÇÃO: ANÁLISE DE CAMPO
# ============================================================================

def analyze_field_for_eor(campo: Dict[str, Any], metodos: List[str]):
    """Analisa um campo para todos os métodos EOR e reporta inviabilidades.
    
    Args:
        campo: Dicionário com parâmetros do reservatório
        metodos: Lista de métodos EOR a avaliar
    """
    from v7 import TechnicalRedFlags
    
    print(f"\n{'=' * 80}")
    print(f"📍 ANÁLISE EOR: {campo.get('nome', 'Campo sem nome')}")
    print(f"{'=' * 80}\n")
    
    print(f"📊 CARACTERÍSTICAS DO CAMPO:")
    print(f"  • API: {campo.get('API', 'N/A')}°")
    print(f"  • Viscosidade: {campo.get('Viscosidade', 'N/A')} cP")
    print(f"  • Profundidade: {campo.get('Profundidade', 'N/A')} m")
    print(f"  • Temperatura: {campo.get('Temperatura', 'N/A')}°C")
    print(f"  • Salinidade: {campo.get('Salinidade', 'N/A')} ppm")
    print(f"  • Espessura: {campo.get('Espessura', 'N/A')} m\n")
    
    # Verificar inviabilidades para cada método
    inviabilities_by_method = {}
    viable_count = 0
    problematic_count = 0
    
    for metodo in metodos:
        red_flags = TechnicalRedFlags.check_reservoir_inviability(
            campo, metodo
        )
        
        if red_flags:
            inviabilities_by_method[metodo] = red_flags
            problematic_count += 1
        else:
            viable_count += 1
    
    # Relatório de viabilidade
    print(f"🔍 RESULTADO DA VALIDAÇÃO TÉCNICA:")
    print(f"  ✅ Métodos viáveis: {viable_count}/{len(metodos)}")
    print(f"  ❌ Métodos com inviabilidades: {problematic_count}/{len(metodos)}\n")
    
    if not inviabilities_by_method:
        print("✅ NÃO HÁ INVIABILIDADES TÉCNICAS DETECTADAS")
        print("Recomendação: Campo adequado para múltiplos métodos EOR\n")
        return
    
    # Detalhe das inviabilidades
    print("⚠️ INVIABILIDADES TÉCNICAS DETECTADAS:\n")
    
    for metodo, flags in inviabilities_by_method.items():
        print(f"  ❌ {metodo}")
        for flag in flags:
            print(f"     • {flag['mensagem']}")
            print(f"       Parâmetro: {flag['parâmetro']}")
            print(f"       Valor atual: {flag['valor']:.2f} | Limite: {flag['limite']:.2f}")
            print()
    
    # Recomendações baseadas em padrões
    print("\n💡 RECOMENDAÇÕES:")
    analyze_recommendations(campo, metodos)


def analyze_recommendations(campo: Dict[str, Any], metodos: List[str]):
    """Gera recomendações EOR baseadas no perfil do campo.
    
    Args:
        campo: Dados do campo
        metodos: Lista de métodos disponíveis
    """
    from v7 import TechnicalRedFlags
    
    api = campo.get('API', 0)
    viscosidade = campo.get('Viscosidade', 0)
    profundidade = campo.get('Profundidade', 0)
    salinidade = campo.get('Salinidade', 0)
    temperatura = campo.get('Temperatura', 0)
    
    recommendations = []
    
    # Análise de padrões
    if api < 20 and viscosidade > 100:
        recommendations.append(
            "🔴 Óleo muito pesado e viscoso - Foco em métodos térmicos"
        )
        if profundidade < 2000:
            recommendations.append(
                "  → Considere CSS (Injeção Cíclica de Vapor) para campos maduros"
            )
        if profundidade > 2000 and temperatura < 100:
            recommendations.append(
                "  → EOR Térmico para Águas Profundas pode ser viável"
            )
    
    elif api > 27 and viscosidade < 20:
        recommendations.append(
            "🟢 Óleo leve e de baixa viscosidade - Adequado para injeção de gás"
        )
        if profundidade > 800 and profundidade < 3500:
            recommendations.append(
                "  → WAG (Injeção Gás com Alternância de Água) recomendado"
            )
    
    if salinidade > 30000 and salinidade < 150000:
        recommendations.append(
            "🟠 Salinidade elevada - LoSal (Baixa Salinidade) pode ser viável"
        )
        if temperatura < 100:
            recommendations.append(
                "  → Análise de compatibilidade com água fresca recomendada"
            )
    
    if salinidade > 80000:
        recommendations.append(
            "🔴 Salinidade muito elevada - Nanotecnologia pode ser alternativa"
        )
        if temperatura < 120:
            recommendations.append(
                "  → Considere nanopartículas tolerantes a sal"
            )
    
    if profundidade > 1000 and profundidade < 3500 and api > 20:
        recommendations.append(
            "💎 Profundidade moderada com óleo leve - Aplicável a WAG offshore"
        )
    
    if not recommendations:
        recommendations.append(
            "⚠️ Perfil do campo desafiador - Recomenda-se análise técnica detalhada"
        )
    
    for rec in recommendations:
        print(f"  {rec}")


def compare_fields(*campos_list):
    """Compara múltiplos campos em uma análise comparativa.
    
    Args:
        campos_list: Múltiplos dicionários de campos
    """
    from v7 import EORScreeningEngine
    
    print("\n" + "=" * 80)
    print("📊 ANÁLISE COMPARATIVA DE CAMPOS")
    print("=" * 80 + "\n")
    
    screening = EORScreeningEngine()
    
    for campo in campos_list:
        print(f"\n{campo.get('nome', 'Campo sem nome')}:")
        print("-" * 60)
        
        scores = screening.score_reservoir(campo)
        
        # Top 3 métodos
        top_3 = sorted(
            scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )[:3]
        
        for i, (metodo, data) in enumerate(top_3, 1):
            status_icon = "🟢" if data['score'] >= 80 else "🟡" if data['score'] >= 60 else "🔴"
            print(f"  {i}. {status_icon} {metodo}: {data['score']:.1f}%")


# ============================================================================
# EXECUÇÃO DOS EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    # Importar TechnicalRedFlags (demonstração)
    try:
        from v7 import EORScreeningEngine
        
        # Listar todos os métodos disponíveis
        screening = EORScreeningEngine()
        TODOS_METODOS = screening.methods
        
        print("\n" + "🎯 PETROCHAMP v7.0 - DEMONSTRAÇÃO DE RED FLAGS" + "\n")
        print(f"Métodos EOR disponíveis ({len(TODOS_METODOS)}):")
        for i, metodo in enumerate(TODOS_METODOS, 1):
            print(f"  {i:2d}. {metodo}")
        
        # ANÁLISE 1: Campo Bloco 15 (Bom candidato para CSS)
        analyze_field_for_eor(CAMPO_BLOCO15, TODOS_METODOS)
        
        # ANÁLISE 2: Campo Bloco 17 (Bom candidato para WAG)
        analyze_field_for_eor(CAMPO_BLOCO17, TODOS_METODOS)
        
        # ANÁLISE 3: Campo Problemático
        analyze_field_for_eor(CAMPO_PROBLEMATICO, TODOS_METODOS)
        
        # ANÁLISE 4: Campo para LoSal
        analyze_field_for_eor(CAMPO_LOSAL, TODOS_METODOS)
        
        # ANÁLISE COMPARATIVA
        compare_fields(CAMPO_BLOCO15, CAMPO_BLOCO17, CAMPO_LOSAL)
        
    except ImportError:
        print("❌ Erro: Não foi possível importar v7.py")
        print("Verifique se o arquivo está no mesmo diretório.")
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
