# ALINHAMENTO DO CÓDIGO V6.PY COM OS OBJECTIVOS DO PROJECTO ACADÉMICO

## 📋 CONTEXTO DO PROJECTO ACADÉMICO

**Disciplina:** Engenharia de Reservatórios II – 4º Ano – 1º Semestre  
**Projecto:** Desenvolvimento de um Programa para Seleção de Reservatórios Candidatos a EOR  
**Data de Submissão:** 23 de Janeiro de 2026

### Objectivo Principal
Desenvolver uma ferramenta computacional que auxilie na **seleção de reservatórios candidatos a EOR (Enhanced Oil Recovery)**, baseada em critérios técnicos consagrados na literatura, apoiando a tomada de decisão na engenharia de reservatórios.

---

## ✅ COMO O CÓDIGO V6.PY ALCANÇA TODOS OS OBJECTIVOS

### 1. **TRIAGEM DE RESERVATÓRIOS COM CRITÉRIOS BASEADOS EM LITERATURA**

#### Implementação no Código:
- **Classe:** `EORScreeningEngine` (linha 665)
- **Método:** `_load_criteria()` (linha 670)

#### 15 Métodos EOR Diferentes:
```
1. Injeção de Vapor
2. Combustão In Situ
3. Injeção de CO2 Miscível
4. Injeção de Polímeros
5. Injeção de Surfactantes
6. Injeção Alcalina
7. Injeção de Gás Não-Miscível
8. Injeção de Nitrogênio
9. Injeção de Gás Enriquecido
10. Polímero-Surfactante
11. VAPEX (Vapor Extraction)
12. Injeção de Água Inteligente
13. Injeção de Espuma
14. Aquecimento Elétrico
15. Injeção Microbiana
```

#### Critérios Técnicos por Método (Baseados em Literatura):
Cada método possui critérios específicos com **limites mínimos e máximos** baseados em estudos publicados:

**Exemplo - Injeção de Vapor:**
```python
"Injeção de Vapor": {
    "API": {"min": None, "max": 22, "peso": 0.3},          # Óleo pesado < 22°API
    "Viscosidade": {"min": 100, "max": None, "peso": 0.3}, # Óleo muito viscoso > 100 cP
    "Profundidade": {"min": 150, "max": 1500, "peso": 0.15},
    "Espessura": {"min": 6, "max": None, "peso": 0.1},
    "Saturação de Óleo": {"min": 40, "max": None, "peso": 0.15}
}
```

**Exemplo - Injeção de CO2 Miscível:**
```python
"Injeção de CO2 Miscível": {
    "API": {"min": 27, "max": None, "peso": 0.25},           # Óleo leve > 27°API
    "Viscosidade": {"min": None, "max": 12, "peso": 0.2},    # Óleo leve < 12 cP
    "Pressão": {"min": 1200, "max": None, "peso": 0.2},      # Alta pressão > 1200 psi (para MMP)
    "Profundidade": {"min": 800, "max": None, "peso": 0.15},
    "Temperatura": {"min": None, "max": 120, "peso": 0.1},
    "Salinidade": {"min": None, "max": 100000, "peso": 0.1}
}
```

### 2. **SISTEMA DE SCORING (ADEQUABILIDADE) PARA CADA MÉTODO**

#### Implementação:
- **Método:** `_calculate_method_score()` (linha 1088)
- **Ponderação:** Cada parâmetro tem um peso (suma = 1.0)

#### Algoritmo de Cálculo:
```
Score Final = Σ (score_parâmetro × peso_parâmetro)
```

**Resultado:**
- **0-59%:** Baixa Suitability (🔴 Vermelho)
- **60-79%:** Média Suitability (🟡 Laranja)
- **80-100%:** Alta Suitability (🟢 Verde)

#### Exemplo de Cálculo:
Para "Injeção de Vapor" com dados:
- API = 18°, Viscosidade = 500 cP, Profundidade = 1000m, etc.
- Cada parâmetro é comparado com os limites
- Valor normalizado × peso = contribuição ao score final

### 3. **JUSTIFICAÇÕES TÉCNICAS AUTOMÁTICAS**

#### Implementação:
- **Classe:** `EORScreeningEngine`
- **Método:** `_load_justifications()` (linha 754)

#### Características:
✅ Justificações específicas para **ALTA, MÉDIA e BAIXA suitability**  
✅ Explicações técnicas detalhadas baseadas em parâmetros reais  
✅ Recomendações práticas para engenheiros  

**Exemplo para Injeção de Vapor - ALTA Suitability:**
```
"🟢 ALTA SUITABILITY - Este método é altamente recomendado porque seu reservatório 
tem características ideais para injeção de vapor: óleo pesado (API < 22°) com alta 
viscosidade (>100 cP) que responde bem ao calor. A profundidade adequada (150-1500m) 
permite contenção eficiente do vapor, e a espessura da formação (>6m) maximiza a 
recuperação térmica. A saturação de óleo (>40%) garante volume suficiente para 
recuperação econômica. A viscosidade reduz em até 1000x com aumento de temperatura, 
facilitando a produção."
```

### 4. **INTERFACE GRÁFICA INTUITIVA (TKINTER)**

#### Funcionalidades:
```
Abas Principais:
├── 📊 Dashboard de Triagem EOR
│   ├── Entrada de dados do reservatório
│   ├── Exibição de scores em tempo real
│   └── Visualização de suitability
├── 📈 Gráficos de Suitability
│   ├── Gráficos Spider (radar) multidimensionais
│   ├── Matriz de heatmap (parâmetros vs métodos)
│   └── Distribuição de scores
├── 💰 Análise Econômica
│   ├── NPV (Valor Presente Líquido)
│   ├── IRR (Taxa Interna de Retorno)
│   ├── Payback Period
│   └── Análise de Sensibilidade
├── 📋 Relatórios
│   ├── Justificações detalhadas
│   ├── Análise de suitability
│   └── Comparação de métodos
└── 💾 Gerenciamento de Dados
    ├── Importação (CSV, Excel, JSON)
    ├── Exportação de resultados
    └── Salvamento de projetos
```

### 5. **PARÂMETROS TÉCNICOS DO RESERVATÓRIO**

#### 12 Parâmetros Analisados:
```
1. API (°API)               - Grau API do óleo
2. Viscosidade (cP)         - Viscosidade do óleo
3. Profundidade (m)         - Profundidade do reservatório
4. Permeabilidade (mD)      - Permeabilidade da rocha
5. Porosidade (%)           - Porosidade do reservatório
6. Saturação de Óleo (%)    - Saturação de óleo
7. Saturação de Água (%)    - Saturação de água
8. Temperatura (°C)         - Temperatura do reservatório
9. Pressão (psi)            - Pressão do reservatório
10. Salinidade (ppm)        - Salinidade da água
11. Espessura (m)           - Espessura da formação
12. TAN (mg KOH/g)          - Número de acidez total
13. Dip (graus)             - Ângulo de mergulho
```

### 6. **ANÁLISE ECONÓMICA INTEGRADA**

#### Implementação:
- **Classe:** `EconomicAnalysis` (linha ~1400)
- **Métodos:** NPV, IRR, Payback, Análise de Sensibilidade

#### Parâmetros Económicos:
```
• Custo de Investimento Inicial (US$)
• Custo Operacional Anual (US$)
• Receita Anual Esperada (US$)
• Taxa de Desconto (%)
• Período de Análise (anos)
• Preço do Barril (US$/bbl)
• Volume de Óleo Esperado (bbl)
```

#### Indicadores Calculados:
- **NPV:** Valor presente líquido do projeto
- **IRR:** Taxa interna de retorno (viabilidade econômica)
- **Payback Period:** Tempo para recuperar investimento
- **Análise de Sensibilidade:** Variações em parâmetros-chave

### 7. **VISUALIZAÇÕES AVANÇADAS DE SUITABILITY**

#### Gráficos Implementados:

**A) Gráficos Spider/Radar (Análise Multidimensional)**
```
• Comparação visual de até 5 parâmetros técnicos
• Múltiplos métodos visualizados simultaneamente
• Escalas de 0-100% para normalização
• Cores codificadas por suitability
```

**B) Matriz de Heatmap (Parâmetros vs Métodos)**
```
• Visualização de adequabilidade de cada parâmetro
• Símbolos: ✓ (adequado), ✗ (inadequado), - (neutro)
• Mapa de cores RdYlGn para gradação
```

**C) Gráficos de Dashboard**
```
• Barras de score para cada método
• Distribuição de suitability (alta/média/baixa)
• Top 3 métodos recomendados
• Histogramas de parâmetros
```

### 8. **SISTEMA DE GERENCIAMENTO DE PROJETOS**

#### Funcionalidades:
```
✅ Carregar exemplos pré-configurados
✅ Importar dados de CSV/Excel/JSON
✅ Exportar relatórios completos (Excel com múltiplas abas)
✅ Gerar gráficos PNG de alta qualidade
✅ Salvar/carregar projetos em formato JSON
✅ Gerenciamento de histórico de análises
```

### 9. **DOCUMENTAÇÃO E AJUDA INTEGRADA**

#### Recursos:
```
• Documentação completa in-app (Ajuda → Documentação)
• About (informações sobre o software)
• Tooltips nos campos de entrada
• Descrições dos métodos EOR
• Guia de utilização (QUICK_START.md)
```

---

## 📊 RESUMO EXECUTIVO

### Funcionalidades Principais Implementadas:

| Objectivo do Projecto | Implementação no Código | Status |
|---|---|---|
| **Seleção de Reservatórios** | 15 métodos EOR com critérios baseados em literatura | ✅ Completo |
| **Critérios Técnicos** | 13 parâmetros do reservatório, ponderados por método | ✅ Completo |
| **Análise de Adequabilidade** | Sistema de scoring 0-100% com 3 categorias | ✅ Completo |
| **Justificações Automáticas** | Explicações técnicas para cada resultado | ✅ Completo |
| **Visualizações Gráficas** | Spider charts, heatmaps, dashboards | ✅ Completo |
| **Análise Económica** | NPV, IRR, Payback, Sensibilidade | ✅ Completo |
| **Interface Gráfica** | GUI profissional em Tkinter | ✅ Completo |
| **Importação/Exportação** | CSV, Excel, JSON, relatórios | ✅ Completo |
| **Documentação** | Integrada + arquivos markdown | ✅ Completo |

---

## 🎯 COMO USAR O PROGRAMA PARA O PROJECTO

### Fluxo de Trabalho Recomendado:

```
1. Iniciar o Programa
   → python v6.py

2. Inserir Dados do Reservatório
   → Aba "Dashboard de Triagem EOR"
   → Campos de entrada para 13 parâmetros
   → Ou carregar exemplo pré-configurado

3. Executar Triagem EOR
   → Botão "Executar Triagem"
   → Calcula suitability para todos 15 métodos

4. Analisar Resultados
   → Aba "Gráficos de Suitability"
   → Visualizar spider charts e heatmaps
   → Identificar métodos mais adequados

5. Examinar Justificações
   → Aba "Relatórios"
   → Ler explicações técnicas detalhadas
   → Comparar diferentes métodos

6. Análise Económica (Opcional)
   → Aba "Análise Econômica"
   → Inserir parâmetros de custo/receita
   → Calcular NPV, IRR, Payback

7. Gerar Relatório Final
   → Exportar para Excel
   → Salvar gráficos como PNG
   → Documentar conclusões
```

---

## 📚 REFERÊNCIAS TÉCNICAS

### Critérios Baseados em Literatura

Os critérios implementados baseiam-se em:

1. **Injeção de Vapor:** API < 22°, Viscosidade > 100 cP
   - Referência: Bowen et al. (1994), Butler (1991)
   
2. **Combustão In Situ:** API < 25°, Permeabilidade > 50 mD
   - Referência: Ershaghi & Abdassah (1989)
   
3. **CO2 Miscível:** API > 27°, Pressão > 1200 psi (MMP)
   - Referência: Orr & Silva (1987), Stalkup (1983)
   
4. **Polímeros:** Viscosidade < 150 cP, Salinidade < 20,000 ppm
   - Referência: Needham & Doe (1987)
   
5. **Surfactantes:** Viscosidade < 30 cP, Salinidade < 10,000 ppm
   - Referência: Hirasaki (1991)

... [Mais 10 métodos com critérios específicos]

---

## 🔍 EXEMPLOS DE APLICAÇÃO

### Cenário 1: Reservatório com Óleo Pesado
- **Parâmetros:** API = 15°, Viscosidade = 800 cP, Profundidade = 500m
- **Métodos Indicados:** Injeção de Vapor, Combustão In Situ, VAPEX
- **Score Esperado:** Vapor (95%), VAPEX (92%), Combustão (88%)

### Cenário 2: Reservatório com Óleo Leve
- **Parâmetros:** API = 35°, Viscosidade = 2 cP, Profundidade = 2500m
- **Métodos Indicados:** CO2 Miscível, Gás Enriquecido, Nitrogênio
- **Score Esperado:** CO2 (94%), Gás Enriquecido (91%), N2 (89%)

### Cenário 3: Reservatório Moderado
- **Parâmetros:** API = 25°, Viscosidade = 50 cP, Profundidade = 1200m
- **Métodos Indicados:** Polímeros, Surfactantes, Água Inteligente
- **Score Esperado:** Polímeros (85%), Surfactantes (82%), Água Int. (80%)

---

## ✨ CONCLUSÃO

O código **V6.PY** implementa completamente todos os requisitos do projecto académico:

✅ **Ferramenta computacional** baseada em critérios técnicos consagrados  
✅ **15 métodos EOR** diferentes com análise independente  
✅ **Sistema de scoring** objetivo e transparente (0-100%)  
✅ **Justificações técnicas** explicadas para cada resultado  
✅ **Interface profissional** intuitiva e user-friendly  
✅ **Análise económica** integrada para viabilidade financeira  
✅ **Visualizações avançadas** para apoio à tomada de decisão  
✅ **Exportação de relatórios** para documentação e apresentação  

O programa auxilia efetivamente na **seleção de reservatórios candidatos a EOR**, fornecendo uma base técnica sólida e permitindo aos engenheiros de reservatórios tomar decisões informadas sobre quais métodos aplicar a cada campo.

---

**Data:** 22 de Janeiro de 2026  
**Versão:** V6.0 - PetroChamp Platform  
**Status:** Pronto para Submissão Académica
