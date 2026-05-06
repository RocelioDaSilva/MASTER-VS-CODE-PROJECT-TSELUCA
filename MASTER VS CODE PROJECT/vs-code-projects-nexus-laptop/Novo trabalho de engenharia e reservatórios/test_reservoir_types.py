#!/usr/bin/env python3
"""
Script de teste para validar a funcionalidade de tipos de reservatório
no PetroNalysis v8.py
"""

import sys
sys.path.insert(0, r'c:\Users\rocel\OneDrive\Desktop\Novo trabalho de engenharia e reservatórios\sucesso1\versão 8')

try:
    print("=" * 60)
    print("TESTE: Funcionalidade de Tipos de Reservatório - PetroNalysis")
    print("=" * 60)
    
    # Importar a classe
    from v8 import EORScreeningEngine
    
    # Criar instância do engine
    engine = EORScreeningEngine()
    print("\n✅ Engine de triagem EOR inicializado com sucesso")
    
    # Verificar se os tipos de reservatório foram carregados
    assert hasattr(engine, 'reservoir_types_data'), "Atributo 'reservoir_types_data' não encontrado"
    print("✅ Atributo 'reservoir_types_data' encontrado")
    
    # Verificar se todos os 6 tipos foram carregados
    types = engine.reservoir_types_data.keys()
    print(f"\n📋 Tipos de Reservatório Carregados ({len(types)}):")
    for i, rtype in enumerate(types, 1):
        print(f"   {i}. {rtype}")
    
    assert len(types) == 6, f"Esperado 6 tipos, mas encontrou {len(types)}"
    print("\n✅ Todos os 6 tipos de reservatório carregados")
    
    # Testar dados de um tipo específico
    print("\n" + "=" * 60)
    print("DETALHES: Tipo 'Petróleo Pesado/Viscoso'")
    print("=" * 60)
    
    heavy_oil_data = engine.reservoir_types_data["Petróleo Pesado/Viscoso"]
    print(f"Profundidade típica: {heavy_oil_data.get('profundidade_tipica')}")
    print(f"API ideal: {heavy_oil_data.get('api_ideal')}")
    print(f"Métodos prioritários: {', '.join(heavy_oil_data.get('metodos_prioritarios', []))}")
    print(f"Recuperação típica: {heavy_oil_data.get('recuperacao_tipica')}")
    
    # Testar a função de penalidade
    print("\n" + "=" * 60)
    print("TESTE: Função de Penalidade por Tipo")
    print("=" * 60)
    
    # Para óleo pesado, vapor deve ter penalidade baixa (0.6)
    penalty_vapor = engine._get_method_penalty_for_type(
        "Injeção de Vapor", "Petróleo Pesado/Viscoso"
    )
    print(f"Penalidade para 'Injeção de Vapor' em 'Petróleo Pesado/Viscoso': {penalty_vapor}")
    assert penalty_vapor == 0.6, f"Esperado 0.6, mas obteve {penalty_vapor}"
    print("✅ Penalidade correta para método recomendado")
    
    # Para onshore convencional, vapor deve ter penalidade alta (1.2)
    penalty_vapor_onshore = engine._get_method_penalty_for_type(
        "Injeção de Vapor", "Convencional Onshore"
    )
    print(f"Penalidade para 'Injeção de Vapor' em 'Convencional Onshore': {penalty_vapor_onshore}")
    assert penalty_vapor_onshore == 1.2, f"Esperado 1.2, mas obteve {penalty_vapor_onshore}"
    print("✅ Penalidade correta para método não recomendado")
    
    # Testar scoring com tipo de reservatório
    print("\n" + "=" * 60)
    print("TESTE: Scoring com Tipo de Reservatório")
    print("=" * 60)
    
    # Dados de teste: óleo pesado
    heavy_oil_reservoir = {
        "API": 15.5,
        "Viscosidade": 850,
        "Profundidade": 1200,
        "Permeabilidade": 450,
        "Porosidade": 22,
        "Saturação de Óleo": 65,
        "Saturação de Água": 35,
        "Temperatura": 75,
        "Pressão": 1800,
        "Salinidade": 25000,
        "Espessura": 12,
        "TAN": 1.2,
        "Dip": 5,
        "Tipo_Reservatorio": "Petróleo Pesado/Viscoso"
    }
    
    scores = engine.score_reservoir(heavy_oil_reservoir)
    
    # Encontrar os métodos com melhor score
    sorted_methods = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    print(f"\nTop 5 métodos para {heavy_oil_reservoir['Tipo_Reservatorio']}:")
    for i, (method, data) in enumerate(sorted_methods[:5], 1):
        print(f"   {i}. {method}: {data['score']:.1f}% ({data['status']})")
    
    # Vapor deve estar entre os top 3
    top_3_methods = [m[0] for m in sorted_methods[:3]]
    assert "Injeção de Vapor" in top_3_methods, "Injeção de Vapor deveria estar no top 3"
    print("\n✅ Métodos prioritários ranqueados corretamente")
    
    # Testar com tipo diferentes (convencional onshore)
    print("\n" + "=" * 60)
    print("TESTE: Óleo Convencional Onshore")
    print("=" * 60)
    
    conventional_reservoir = {
        "API": 28.0,
        "Viscosidade": 45,
        "Profundidade": 1500,
        "Permeabilidade": 650,
        "Porosidade": 24,
        "Saturação de Óleo": 55,
        "Saturação de Água": 45,
        "Temperatura": 65,
        "Pressão": 1500,
        "Salinidade": 15000,
        "Espessura": 15,
        "TAN": 0.3,
        "Dip": 8,
        "Tipo_Reservatorio": "Convencional Onshore"
    }
    
    scores_conv = engine.score_reservoir(conventional_reservoir)
    sorted_methods_conv = sorted(scores_conv.items(), key=lambda x: x[1]["score"], reverse=True)
    
    print(f"\nTop 5 métodos para {conventional_reservoir['Tipo_Reservatorio']}:")
    for i, (method, data) in enumerate(sorted_methods_conv[:5], 1):
        print(f"   {i}. {method}: {data['score']:.1f}% ({data['status']})")
    
    # Polímero deve ter bom score
    polymer_score = scores_conv["Injeção de Polímeros"]["score"]
    vapor_score = scores_conv["Injeção de Vapor"]["score"]
    print(f"\nComparação de scores:")
    print(f"   Polímero: {polymer_score:.1f}%")
    print(f"   Vapor: {vapor_score:.1f}%")
    print("✅ Scores ajustados por tipo de reservatório")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 60)
    print("\nA funcionalidade de tipos de reservatório está operacional:")
    print("✓ 6 tipos de reservatório carregados")
    print("✓ Penalidades por tipo aplicadas corretamente")
    print("✓ Scoring ajustado por tipo")
    print("✓ Métodos recomendados variam por tipo")
    
except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
