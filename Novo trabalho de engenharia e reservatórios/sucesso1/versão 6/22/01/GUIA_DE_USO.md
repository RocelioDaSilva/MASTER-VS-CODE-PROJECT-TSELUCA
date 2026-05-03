# GUIA DE USO - PetroChamp v6.1

## 🚀 Iniciando a Aplicação

```bash
python v6.py
```

---

## 📊 Principais Funcionalidades

### 1. **Importação de Dados** (Aba: Dados)
- **CSV**: Arquivo com colunas nomeadas
- **Excel**: Planilhas com parâmetros
- **Manual**: Entrada direta de valores

**Parâmetros aceitos:**
- API (°API)
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
- Dip (graus)

### 2. **Triagem EOR** (Aba: Triagem)
- Selecione os métodos para análise
- Clique em "Executar Triagem"
- Visualize pontuações de suitability

**15 Métodos Disponíveis:**
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
11. VAPEX
12. Injeção de Água Inteligente
13. Injeção de Espuma
14. Aquecimento Elétrico
15. Injeção Microbiana

### 3. **Análise de Suitability** (Aba: Suitability)
- **Spider Chart**: Comparação visual de top 3 métodos
- **Matriz**: Adequabilidade de parâmetros vs métodos
- **Comparativo**: 4 visualizações simultâneas
- **Dashboard**: Análise completa com semáforo

**Cores de Status:**
- 🟢 **ALTA** (≥80%): Fortemente recomendado
- 🟡 **MÉDIA** (60-79%): Potencial com ressalvas
- 🔴 **BAIXA** (<60%): Não recomendado

### 4. **Justificações Detalhadas** (Aba: Resultados → Justificações)
- Explicações textuais para cada método
- Análise de pontos fortes e fracos
- Recomendações específicas
- Estimativas de custo

**Exemplo de Justificativa:**
```
🟢 ALTA SUITABILITY - Este método é altamente recomendado porque 
seu reservatório tem características ideais para injeção de vapor:
• Óleo pesado (API < 22°)
• Alta viscosidade (>100 cP)
• Profundidade adequada (150-1500m)
→ Recomendação: Proceder com estudo de viabilidade
```

### 5. **Análise Econômica** (Aba: Análise Econômica)

**Parâmetros Configuráveis:**
- Preço do Óleo (US$/bbl)
- Taxa de Desconto (%)
- Impostos (%)
- Vida do Projeto (anos)
- Taxa de Declínio (%/ano)
- Custo CAPEX (US$)
- OPEX (% receita)

**Resultados Calculados:**
- NPV (Valor Presente Líquido)
- IRR (Taxa Interna de Retorno)
- Payback Period
- Fluxo de Caixa Anual

### 6. **Visualizações de Resultados** (Aba: Resultados)
- **Tabela**: Resumo de scores por método
- **Gráficos**: Visualizações econômicas
- **Justificações**: Análise textual detalhada

---

## 💡 Dicas de Uso

### Para Melhores Resultados:

1. **Dados Completos**
   - Preencha o máximo de parâmetros possível
   - Use dados medidos em laboratório
   - Valide dados antes de importar

2. **Interpretação de Suitability**
   - Score ≥80%: Investimento viável
   - Score 60-79%: Requer análise adicional
   - Score <60%: Considere alternativas

3. **Análise Econômica**
   - Use preços históricos ou projetados
   - Ajuste taxa de desconto para seu risco
   - Considere custos operacionais reais

4. **Exportação**
   - Salve resultados em Excel para apresentações
   - Use relatórios de justificações para documentação
   - Guarde gráficos para análises futuras

---

## 🔍 Validação de Dados

O sistema valida automaticamente:
- ✅ Intervalos razoáveis de valores
- ✅ Ausência de dados obrigatórios
- ✅ Consistência de unidades
- ✅ Valores negativos inválidos

**Exemplo de Erro:**
```
VALIDAÇÃO FALHOU:
- Viscosidade: 150000.0 fora do intervalo [0.1, 100000]
- Temperatura: 300 acima do máximo (250)
```

---

## 📈 Interpretando Gráficos

### Spider Chart (Radar)
- Quanto maior a área, melhor o score
- Comparação visual entre top 3 métodos
- Útil para decisões rápidas

### Matriz de Adequabilidade
- ✓ = Parâmetro atende critério
- ✗ = Parâmetro não atende
- \- = Dado não disponível

### Gráfico Comparativo
- Painel 1: Barras coloridas por status
- Painel 2: Distribuição em pizza
- Painel 3: Curva de acumulação
- Painel 4: Heatmap de scores

### Gráficos Econômicos
- NPV vs Taxa de Desconto
- Fluxo de Caixa Acumulado
- Análise de Sensibilidade
- Payback vs Produção

---

## 🛠️ Troubleshooting

### Problema: "Erro ao criar gráfico"
- **Solução**: Verifique se matplotlib está instalado
- `pip install matplotlib`

### Problema: "IRR não calculado"
- **Solução**: Sistema usará método alternativo
- Não afeta qualidade de resultados

### Problema: "Dados inválidos"
- **Solução**: Revise valores em intervalos válidos
- Veja aba "Dados" para revisar entrada

### Problema: "Aplicação lenta"
- **Solução**: Reduza número de métodos selecionados
- Cache está habilitado automaticamente

---

## 📊 Formatos de Importação

### CSV
```
API,Viscosidade,Profundidade,Temperatura
32,5,1200,60
28,8,1500,65
```

### Excel
- Primeira linha com nomes de parâmetros
- Uma linha por reservatório
- Formatos suportados: .xls, .xlsx

### Manual
- Preencha campos individuais
- Deixe em branco se não houver dados
- Clique "Adicionar Reservatório"

---

## 🎯 Workflow Recomendado

1. **Preparar Dados**
   - Colete parâmetros do reservatório
   - Organize em formato CSV/Excel

2. **Importar Dados**
   - Use aba "Dados"
   - Valide visualização na tabela

3. **Executar Triagem**
   - Aba "Triagem"
   - Clique "Executar Triagem"

4. **Analisar Suitability**
   - Veja gráficos de suitability
   - Interprete scores

5. **Avaliar Economicamente**
   - Configure parâmetros econômicos
   - Calcule NPV e IRR

6. **Revisar Justificações**
   - Leia análises detalhadas
   - Tome decisões informadas

7. **Exportar Resultados**
   - Salve em Excel
   - Documente relatórios

---

## 📞 Contato e Suporte

- **Versão**: 6.1
- **Última Atualização**: 22/01/2026
- **Autor**: PetroChamp Development Team

---

## ✅ Checklist de Uso

- [ ] Dados do reservatório preparados
- [ ] Parâmetros dentro de intervalos válidos
- [ ] Métodos EOR selecionados
- [ ] Triagem executada
- [ ] Gráficos visualizados
- [ ] Suitability analisada
- [ ] Parâmetros econômicos configurados
- [ ] Análise econômica realizada
- [ ] Justificações revisadas
- [ ] Resultados exportados

---

**Divirta-se analisando seus projetos EOR! 🎉**
