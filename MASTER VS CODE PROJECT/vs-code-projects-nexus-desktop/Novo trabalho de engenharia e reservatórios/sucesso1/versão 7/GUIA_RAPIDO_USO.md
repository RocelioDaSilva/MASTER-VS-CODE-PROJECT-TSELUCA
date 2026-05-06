# Guia Rápido de Uso - PetroChamp v7.4

## Iniciar a Aplicação

```bash
cd "c:\Users\rocel\OneDrive\Desktop\Novo trabalho de engenharia e reservatórios\sucesso1\versão 7"
python v7.py
```

## Interface Principal

### Dashboard (Aba 1)
- Visão geral da plataforma
- Cards informativos sobre funcionalidades
- Botões de ação rápida:
  - **Importar Dados CSV**: Carregar dados de arquivo
  - **Executar Análise Completa**: Rodar triagem + economia
  - **Gerar Dashboard Suitability**: Visualizar gráficos

### Dados (Aba 2)
Entrada manual de parâmetros do reservatório:
- API (°)
- Viscosidade (cP)
- Profundidade (m)
- Permeabilidade (mD)
- Porosidade (%)
- Saturação de Óleo (%)
- Saturação de Água (%)
- Temperatura (°C)
- Pressão (psi)
- Salinidade (ppm)
- Espessura (m)
- TAN (mg KOH/g)
- pH
- Mergulho/Dip (°)

### Triagem (Aba 3)
1. Clique "Executar Screening"
2. Veja scores de 20 métodos EOR
3. Identifique top 3 recomendados
4. Analise pontos positivos/negativos

### Economia (Aba 4)
1. Insira taxa de óleo (USD/bbl)
2. Configure parâmetros econômicos
3. Clique "Executar Análise Econômica"
4. Visualize NPV, IRR, Payback

### Resultados (Aba 5)
- Tabela com scores de todos os métodos
- Gráficos comparativos automáticos
- Opções de exportação

### Suitability (Aba 6)
- Visualizações avançadas de suitability
- Matriz de adequabilidade
- Comparações entre métodos
- Gráficos spider para análise detalhada

### Screening Avançado (Aba 7) - FASE 1B
4 subabas:
1. **Perguntas Técnicas**: Responda perguntas específicas por método
2. **Validação de Dados**: Verifique consistência dos parâmetros
3. **Offshore & Angola**: Análise específica para campos submarinos
4. **Eficiência**: Calcule PSD, SE, RF dos métodos

### Fuzzy Selector (Aba 8) - FASE 2
1. Selecione um campo Angola na lista dropdown
2. Clique "Executar Fuzzy Selector"
3. Veja Top 5 métodos com scores de confiança
4. Exporte resultado se necessário

**Campos Angola disponíveis:**
- Bloco 15 (Offshore Raso, 400m)
- Bloco 17 (Offshore Intermediário, 800m)
- Bloco 18 (Offshore Profundo, 1200m)
- Bloco 31 (Offshore Raso, 300m)
- Cabinda (Onshore/Transição, 100m)

### Monte Carlo (Aba 9) - FASE 3
1. Selecione campo Angola
2. Configure:
   - Número de iterações (5k-50k)
   - Método EOR desejado
3. Clique "Executar Monte Carlo"
4. Visualize P10/P50/P90 para:
   - RF (Fator de Recuperação)
   - NPV (Valor Presente Líquido)
   - IRR (Taxa Interna de Retorno)
   - CAPEX (Investimento Capital)

## Menu Arquivo

### Novo Projeto (Ctrl+N)
- Limpa todos os dados
- Inicia análise nova

### Abrir Projeto (Ctrl+O)
- Carrega projeto salvo anteriormente (formato JSON)
- Restaura todos os dados e resultados

### Salvar Projeto (Ctrl+S)
- Salva dados atuais, resultados e gráficos
- Arquivo: `petrochamp_project_[data].json`

### Importar Dados
- **CSV**: `parâmetro,valor`
- **Excel**: Folha com colunas
- **Exemplo CSV:**
  ```
  API,32
  Viscosidade,15.5
  Profundidade,1200
  ...
  ```

### Exportar Relatório
- Gera documento completo com:
  - Dados de entrada
  - Scores de todos os métodos
  - Justificações detalhadas
  - Gráficos (PNG embarcado)
  - Análise econômica

## Menu Análise

- **Executar Triagem**: Inicia screening de 20 métodos
- **Análise Econômica**: Calcula NPV/IRR/Payback
- **Gerar Justificações**: Cria relatório de texto detalhado
- **Gerar Gráficos Suitability**: Cria visualizações de adequabilidade

## Menu Visualização

- **Gráfico de Pontuação**: Barras coloridas por método
- **Gráficos Econômicos**: NPV, cashflow, payback
- **Dashboard Suitability**: 4 visualizações combinadas

## Atalhos de Teclado

| Atalho | Função |
|--------|--------|
| Ctrl+N | Novo Projeto |
| Ctrl+O | Abrir Projeto |
| Ctrl+S | Salvar Projeto |

## Fluxo Típico de Uso

### Análise Rápida (5 minutos)
1. Acesse "Dashboard"
2. Clique "Importar Dados CSV"
3. Clique "Executar Análise Completa"
4. Visualize resultados em "Resultados"

### Análise Completa (30 minutos)
1. Insira dados em "Dados"
2. Execute "Screening" (Aba 3)
3. Analise "Suitability" (Aba 6)
4. Execute "Economia" (Aba 4)
5. Estude "Screening Avançado" (Aba 7)
6. Para Angola: Use "Fuzzy Selector" (Aba 8)
7. Para risco: Use "Monte Carlo" (Aba 9)

### Comparação Angola (15 minutos)
1. Acesse "Fuzzy Selector" (Aba 8)
2. Selecione Bloco 15, 17, 18, 31 ou Cabinda
3. Clique "Executar" para cada bloco
4. Compare scores e métodos recomendados
5. Use "Monte Carlo" para validação econômica

## Interpretação de Resultados

### Cores de Status
- 🟢 **Verde (Alta Suitability ≥80%)**: Fortemente recomendado
- 🟡 **Amarelo (Média 60-79%)**: Potencial com ressalvas
- 🔴 **Vermelho (Baixa <60%)**: Não recomendado

### Campos de Resultado

**Score**: 0-100%
- Calculado pela ponderação de critérios do método
- Baseado em literatura e experiência de campo

**Status**: RECOMENDADO | POTENCIAL | NÃO RECOMENDADO

**Pontos Positivos**: Parâmetros que favorecem o método

**Pontos Negativos**: Limitações técnicas encontradas

**Red Flags**: Inviabilidades técnicas críticas

## Tratamento de Erros

### Mensagem: "Dados inválidos"
→ Verifique:
- Todos os campos preenchidos?
- Valores dentro dos intervalos válidos? (ver aba Dados)
- Consistência entre parâmetros (ex: API vs Viscosidade)

### Mensagem: "Erro ao calcular IRR"
→ Possível causa: Fluxo de caixa constantemente negativo
→ Solução: Ajuste parâmetros econômicos (preço do óleo, CAPEX)

### Interface congelada
→ Aguarde processamento (análise de 20 métodos ≈ 2-3 segundos)
→ Não há progresso após 10s? Feche e reinicie: `python v7.py`

## Exportação de Dados

Todos os resultados podem ser exportados como:
- **Texto (.txt)**: Relatórios em formato legível
- **Excel (.xlsx)**: Tabelas com múltiplas abas
- **Imagem (.png)**: Gráficos individuais
- **Projeto (.json)**: Todos os dados para reabrir depois

## Configuração de Parâmetros Econômicos

Valores padrão (editáveis):
- Preço do óleo: USD 60/bbl (2024)
- CAPEX multiplicador: 5000 USD/bbl/dia
- OPEX: 30% da receita
- Taxa de desconto: 10%
- Alíquota de imposto: 25%
- Vida do projeto: 15 anos
- Tempo de construção: 2 anos
- Taxa de declínio: 15%/ano

## Validação Angola Específica

Para campos Angola (Blocos 15-31, Cabinda):
1. Acesse "Screening Avançado" → "Offshore & Angola"
2. Selecione bloco na lista
3. Sistema valida:
   - Profundidade subsea
   - Viabilidade térmica em deepwater
   - Multiplicadores de custo
   - Infraestrutura disponível

## Salvando Projetos

Formato: JSON (portável)
```
{
  "reservoir_data": {...},
  "screening_results": {...},
  "economic_results": {...},
  "timestamp": "2025-01-23 14:30:00"
}
```

Reabrir qualquer hora com Ctrl+O

---

**Suporte**: Consulte documentação completa em Menu → Ajuda → Documentação  
**Versão**: PetroChamp v7.4  
**Status**: Pronto para uso em produção
