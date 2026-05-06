# Guia de Uso - PetroChamp v6.0

## Índice
1. [Visão Geral](#visão-geral)
2. [Aba Suitability - Matriz](#aba-suitability---matriz)
3. [Aba Suitability - Visão Geral](#aba-suitability---visão-geral)
4. [Aba Suitability - Gráficos Individuais](#aba-suitability---gráficos-individuais)
5. [Aba Suitability - Comparativo](#aba-suitability---comparativo)
6. [Aba Resultados - Gráficos](#aba-resultados---gráficos)
7. [Dicas & Troubleshooting](#dicas--troubleshooting)

---

## Visão Geral

O **PetroChamp v6.0** agora possui uma interface completamente reorganizada com 4 sub-abas dedicadas na seção de Suitability e 8 tipos dinâmicos de gráficos nos Resultados.

### Fluxo Básico
```
1. Execute Triagem → 2. Explore Suitability → 3. Analise Resultados
```

---

## Aba Suitability - Matriz

**Localização**: Abas Principais → Suitability → Matriz

### Objetivo
Visualizar a **matriz de critérios** dos métodos EOR com seleção flexível.

### Funcionalidade

#### 1. Seleção de Métodos (Checkboxes)
- **Listar**: Scroll na seção de checkboxes
- **Selecionar**: Marque os métodos que deseja avaliar
- **Atalhos**:
  - **"Todos"** - Seleciona os 15 métodos
  - **"Nenhum"** - Deseleciona todos

#### 2. Gerar Matriz
- Clique **"Gerar Matriz"**
- A matriz será exibida com apenas os métodos selecionados

#### 3. Leitura da Matriz
| Elemento | Significado |
|----------|------------|
| **Cor Verde** | Parâmetro favorável (≥80%) |
| **Cor Laranja** | Parâmetro médio (60-79%) |
| **Cor Vermelha** | Parâmetro desfavorável (<60%) |
| **Bordas Azuis** | Parâmetro crítico para o método |

#### 4. Características do Método
- Selecione um método no **dropdown** abaixo da matriz
- A **caixa azul** mostrará:
  - Critérios principais
  - Pesos de cada fator
  - Estimativa de tendência

### Exemplo de Uso
```
1. Clique "Todos" para ver todos os 15 métodos
2. Desmarque métodos que não deseja avaliar
3. Clique "Gerar Matriz"
4. Selecione um método no dropdown
5. Leia os critérios na caixa azul
```

---

## Aba Suitability - Visão Geral

**Localização**: Abas Principais → Suitability → Visão Geral

### Objetivo
Visualizar **estatísticas gerais** de todos os métodos.

### Botões Disponíveis

#### 1. "Gerar Gráficos"
Exibe 4 gráficos simultâneos:
- Barras (scores de todos)
- Pizza (distribuição por categoria)
- Linha (tendência ordenada)
- Área (visualização em coluna)

#### 2. "Spider Chart"
Exibe radar chart com todos os métodos.
- Útil para visualizar padrões radiais
- Até 8 métodos por clareza

#### 3. "Dashboard Suitability"
Exibe dashboard com:
- Resumo em texto (monospace)
- KPIs principais
- Top 10 métodos
- Distribuição por categoria
- Histograma de scores
- Tendência geral

### Como Usar
```
1. Vá para "Visão Geral"
2. Clique em um dos botões
3. Aguarde renderização
4. Use zoom/pan da toolbar para explorar
5. Clique novamente para voltar ao conjunto anterior
```

---

## Aba Suitability - Gráficos Individuais

**Localização**: Abas Principais → Suitability → Gráficos Individuais

### Objetivo
Analisar um **método específico** com visualizações diferentes.

### Controles

#### 1. Seletor de Método
- Dropdown com todos os 15 métodos
- Selecione o método desejado

#### 2. Seletor de Tipo
Escolha entre 5 tipos de gráfico:

| Tipo | Descrição |
|------|-----------|
| **Barras** | Mostra scores dos parâmetros |
| **Pizza** | Distribuição de peso dos fatores |
| **Radar** | Visualização em polígono |
| **Box Plot** | Quartis e distribuição |
| **Dispersão** | Scatter com anotações |

#### 3. Gerar Gráfico
- Clique **"Gerar"**
- O gráfico será exibido no espaço dedicado

### Fluxo Típico
```
1. Selecione um método (ex: Steam Flooding)
2. Escolha um tipo (ex: Radar)
3. Clique "Gerar"
4. Analise o resultado
5. Mude o tipo e clique "Gerar" novamente
```

---

## Aba Suitability - Comparativo

**Localização**: Abas Principais → Suitability → Comparativo

### Objetivo
**Comparar múltiplos métodos** lado a lado com diferentes visualizações.

### Controles

#### 1. Seletor de Tipo de Gráfico
Combobox com 5 opções:

| Tipo | Número de Métodos | Melhor Para |
|------|------------------|-----------|
| **Radar** | Até 5 | Comparação simultânea |
| **Barras** | Ilimitado | Ranking visual |
| **Box Plot** | Ilimitado | Distribuição |
| **Dispersão** | Ilimitado | Scatter analysis |
| **Dashboard** | 8+ | Resumo completo |

#### 2. Seleção de Métodos
- **Checkboxes**: Marque os métodos
- **Botão "Todos os Métodos"**: Seleciona todos os 15
- **Botão "Métodos Selecionados"**: Gera com apenas marcados

#### 3. Gerar Comparativo
- Clique o botão desejado
- O gráfico renderiza com a seleção

### Exemplo de Uso

**Cenário 1: Comparação Rápida**
```
1. Selecione tipo "Radar"
2. Clique "Todos os Métodos"
3. Veja os 15 métodos em uma visualização
```

**Cenário 2: Análise Detalhada**
```
1. Desmarque tudo clicando "Nenhum" (na Matriz)
2. Marque apenas Steam Flooding, Surfactant, ASP
3. Selecione tipo "Dashboard"
4. Clique "Métodos Selecionados"
5. Veja análise detalhada dos 3 selecionados
```

**Cenário 3: Ranking**
```
1. Selecione tipo "Barras"
2. Clique "Todos os Métodos"
3. Veja ordenação horizontal de todos
```

---

## Aba Resultados - Gráficos

**Localização**: Abas Principais → Resultados → Gráficos

### Objetivo
Gerar gráficos personalizados e **exportar resultados**.

### Controles

#### 1. Seletor de Tipo
Combobox com **8 tipos**:

| # | Tipo | Características |
|---|------|-----------------|
| 1 | **Barras** | Horizontal com scores e referências |
| 2 | **Pizza** | Distribuição por categoria (Alta/Média/Baixa) |
| 3 | **Linha** | Tendência com preenchimento azul |
| 4 | **Área** | Colunas com cores por status |
| 5 | **Radar** | Projeção polar (até 8 métodos) |
| 6 | **Box Plot** | Quartis agrupados por categoria |
| 7 | **Dispersão** | Scatter com anotações de valores |
| 8 | **Dashboard Completo** | KPIs + 4 gráficos em gridspec |

#### 2. Botões de Ação

**"Gerar Gráfico"**
- Cria o gráfico selecionado
- Renderiza em alta qualidade
- Exibe com toolbar matplotlib (zoom, pan, etc)

**"Exportar Gráfico"**
- Abre dialog para salvar
- Suporta: PNG, PDF, SVG
- Resolução: 300 DPI
- Confirma localização do arquivo

**"Limpar"**
- Remove gráfico atual
- Limpa frame de display

### Fluxo Completo

```
1. Execute triagem na aba "Triagem"
2. Vá para "Resultados" → "Gráficos"
3. Selecione um tipo no combobox
4. Clique "Gerar Gráfico"
5. Explore com zoom/pan/toolbar
6. Satisfeito? Clique "Exportar Gráfico"
7. Escolha formato (PNG/PDF/SVG)
8. Salve em local desejado
```

### Dashboard Completo - Detalhes

O Dashboard oferece uma visão completa:

**Quadrante 1 (Topo - KPIs)**
```
RESUMO DE SUITABILITY - EOR SCREENING
═════════════════════════════════════════════════════════════════
Total de Métodos: 15 │ Média: 62.3% │ Máx: 92.5% │ Mín: 31.2%
Suitabilidade Alta (≥80%): 5 │ Média (60-79%): 6 │ Baixa (<60%): 4
═════════════════════════════════════════════════════════════════
```

**Quadrante 2 (Esquerda - Top 10 em Barras)**
- Ranking dos 10 métodos melhores

**Quadrante 3 (Direita - Pizza)**
- Distribuição percentual por categoria

**Quadrante 4 (Esquerda Inferior - Histograma)**
- Distribuição de frequência dos scores

**Quadrante 5 (Direita Inferior - Linha)**
- Tendência de scores ordenados

---

## Dicas & Troubleshooting

### ✅ Dicas de Uso

#### Para Matriz
- Use "Todos" depois "Nenhum" para limpar
- Combobox atualiza instantaneamente
- Bordas azuis indicam parâmetros críticos

#### Para Comparativo
- **Radar**: Máximo 5 métodos para clareza
- **Dashboard**: Melhor com 4-8 métodos
- **Barras**: Funciona bem com todos os 15

#### Para Resultados
- **Pizza**: Melhor para propósito geral
- **Dashboard**: Quando precisa de resumo completo
- **Radar**: Quando quer visualizar padrões
- **Dispersão**: Quando quer ver outliers

#### Para Exportação
- **PNG**: Melhor para apresentações (tamanho pequeno)
- **PDF**: Melhor para relatórios (vetor escalável)
- **SVG**: Melhor para edição posterior (formato aberto)

### ❌ Troubleshooting

#### Problema: "Execute a triagem primeiro"
**Solução**: 
- Vá para aba "Triagem"
- Preencha parâmetros do reservatório
- Clique "Executar Triagem"

#### Problema: Gráfico não aparece
**Solução**:
- Clique "Limpar" para resetar
- Selecione outro tipo
- Clique "Gerar Gráfico" novamente

#### Problema: Texto truncado em gráfico
**Solução**:
- Use zoom da toolbar matplotlib
- Ou exporte e abra em visualizador

#### Problema: Exportação não funciona
**Solução**:
- Certifique-se de ter gerado um gráfico
- Verifique permissões da pasta
- Tente PNG primeiro (mais compatível)

#### Problema: Muitos métodos no Radar
**Solução**:
- Selecione menos métodos na Matriz
- O sistema limita automaticamente a 8
- Use "Barras" ou "Dashboard" para todos

### ⚡ Atalhos Rápidos

| Ação | Localização | Resultado |
|------|------------|-----------|
| Ver todos os métodos | Matriz → "Todos" | Matriz completa com 15 métodos |
| Comparar 3 melhores | Comparativo → Radar | Visualização clara de top 3 |
| Exportar resumo | Resultados → Dashboard | PDF com 5 quadrantes de análise |
| Análise individual | Gráficos Individuais → Radar | Visualização polar de 1 método |

---

## Checklist de Exploração

### Primeira Execução
- [ ] Executei a triagem
- [ ] Vi a Matriz de todos os 15 métodos
- [ ] Selecionei um método e visualizei características
- [ ] Gerou 4 gráficos na "Visão Geral"
- [ ] Comparei 2-3 métodos no Comparativo
- [ ] Selecionei tipo "Dashboard Completo"
- [ ] Gerou gráfico na aba Resultados
- [ ] Exportei um gráfico em PNG

### Exploração Avançada
- [ ] Usei "Nenhum" e selecionei manualmente
- [ ] Testei todos os 5 tipos de Comparativo
- [ ] Testei todos os 8 tipos de Resultados
- [ ] Exportei em PDF e SVG
- [ ] Explorei zoom/pan na toolbar
- [ ] Comparei Radar vs Dashboard para mesmo método
- [ ] Usei "Spider Chart" na Visão Geral

---

## Recursos Disponíveis

### Total de Gráficos Suportados
- ✅ 5 tipos em Gráficos Individuais
- ✅ 5 tipos em Comparativo
- ✅ 8 tipos em Resultados
- ✅ 3 tipos na Visão Geral
- **Total: 21 visualizações diferentes**

### Métodos EOR Disponíveis
- ✅ 15 métodos completos
- ✅ Cada um com 14 parâmetros
- ✅ Análise econômica integrada

### Formatos de Exportação
- ✅ PNG (raster, pequeno, compatível)
- ✅ PDF (vetor, escalável, profissional)
- ✅ SVG (vetor, editável, aberto)

---

## Contato & Suporte

Para dúvidas ou sugestões sobre o PetroChamp v6.0, consulte:
- Documentação: [CAPACIDADES_COMPLETAS_V6.md](../CAPACIDADES_COMPLETAS_V6.md)
- Implementação: [RESUMO_IMPLEMENTACOES_V6.md](./RESUMO_IMPLEMENTACOES_V6.md)
- Melhorias: [MELHORIAS_ABA_RESULTADOS.md](./MELHORIAS_ABA_RESULTADOS.md)

---

**Versão**: 6.0  
**Último Update**: 2024  
**Status**: ✅ Completo e Testado

