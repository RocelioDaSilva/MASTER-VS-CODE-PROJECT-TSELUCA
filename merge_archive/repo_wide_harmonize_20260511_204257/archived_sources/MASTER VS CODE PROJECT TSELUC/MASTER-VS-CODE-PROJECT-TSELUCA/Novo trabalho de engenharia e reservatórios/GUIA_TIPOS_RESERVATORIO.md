# Guia Rápido: Seleção de Tipo de Reservatório - PetroNalysis v8

## 🚀 Como Usar a Nova Funcionalidade

### 1️⃣ Abra o PetroNalysis
```
Rode: python sucesso1/versão 8/v8.py
```

### 2️⃣ Acesse a Aba "Dados"
- Você verá uma nova seção no topo: **"Tipo de Reservatório"**

### 3️⃣ Selecione o Tipo de Seu Reservatório
Clique no dropdown e escolha uma das 6 opções:

| Opção | Melhor Para |
|-------|-----------|
| **Convencional Onshore** | Campos em terra com óleo leve/médio |
| **Petróleo Pesado/Viscoso** | Óleo com API < 20, viscosidade > 100 cP |
| **Profundo/Ultra-profundo** | Campos > 2500m de profundidade |
| **Offshore Intermediário** | Campos no mar com profundidade 1500-3000m |
| **Carbonatado** | Reservatórios em calcário/dolomita |
| **Teor Argila Elevado** | Formações com >10% de argila misturada |

### 4️⃣ Revise as Informações
Uma caixa de informações aparece automaticamente mostrando:
- Profundidade típica
- API ideal
- Métodos prioritários
- Recuperação esperada
- Descrição das características

### 5️⃣ Adicione Dados do Seu Reservatório

**Opção A - Manual:**
- Preencha os campos de entrada (API, Viscosidade, etc.)
- Clique "Adicionar Reservatório"
- O tipo selecionado é registrado automaticamente

**Opção B - Importar:**
- Clique "Importar CSV" ou "Importar Excel"
- Se o arquivo não tiver coluna "Tipo_Reservatorio", será atribuído "Convencional Onshore" como padrão

**Opção C - Exemplo:**
- Clique "Carregar Exemplo" para ver dados de teste
- Tipo é ajustado para "Petróleo Pesado/Viscoso" (exemplo é óleo pesado)

### 6️⃣ Execute a Triagem EOR
- Vá para a aba "Triagem"
- Clique "Executar Triagem"
- Os scores serão **ajustados especificamente para o tipo** do seu reservatório

### 7️⃣ Analise os Resultados

A visualização mostra scores onde:
- ✅ Métodos com **alta penalidade** (scores altos) = Recomendados para seu tipo
- ⚠️ Métodos com **penalidade** (scores baixos) = Menos adequados para seu tipo
- 💡 Notas explicativas indicam se há ajuste por tipo

### 8️⃣ Salve o Projeto
- Menu "Arquivo" → "Salvar Projeto"
- O tipo é preservado no arquivo JSON

---

## 📊 Exemplos de Resultados

### Cenário 1: Óleo Pesado (API 15.5, Viscosidade 850 cP)
```
Tipo Selecionado: Petróleo Pesado/Viscoso

Top 3 Métodos Recomendados:
1. Injeção de Vapor: 100.0% ✅
2. Injeção Cíclica de Vapor (CSS): 100.0% ✅
3. WAG: 80.0% ⚠️

Nota: Métodos térmicos recebem boost significativo
porque são ideais para viscosidades altas
```

### Cenário 2: Óleo Convencional (API 28, Viscosidade 45 cP)
```
Tipo Selecionado: Convencional Onshore

Top 3 Métodos Recomendados:
1. Injeção de Polímeros: ~75.0% ✅
2. Injeção Alcalina: ~68.0% ✅
3. Surfactante: ~60.0% ⚠️

Nota: Métodos químicos recebem boost
porque funcionam bem com óleos convencionais
```

### Cenário 3: Óleo Profundo (API 35, Profundidade 4000m)
```
Tipo Selecionado: Profundo/Ultra-profundo

Top 3 Métodos Recomendados:
1. CO2 Miscível: ~82.0% ✅
2. Nitrogênio Miscível: ~75.0% ✅
3. Gás Hidrocarboneto: ~70.0% ✅

Nota: Métodos miscíveis recebem boost
porque a alta pressão favorece miscibilidade
```

---

## 🎯 Dicas Práticas

### ✅ Faça Isso
- ✓ Compare resultados alterando o tipo → entenda impacto do tipo
- ✓ Use o tipo que melhor descreve seu reservatório
- ✓ Revise a caixa de informações para confirmar match
- ✓ Salve projetos com tipo específico para rastrear análises

### ❌ Evite Fazer Isso
- ✗ Deixar tipo padrão se seu reservatório é diferente
- ✗ Ignorar a caixa de informações
- ✗ Importar dados sem verificar se tipo foi atribuído

---

## 📁 Formato de Dados

### Se Importar CSV/Excel
Para melhor resultado, inclua coluna `Tipo_Reservatorio`:

```csv
ID,API,Viscosidade,Profundidade,Tipo_Reservatorio
1,15.5,850,1200,Petróleo Pesado/Viscoso
2,28.0,45,1500,Convencional Onshore
```

Se não incluir, será atribuído "Convencional Onshore" automaticamente.

---

## 🔧 Troubleshooting

### Problema: "A caixa de informações não atualiza"
**Solução:** Espere um segundo após mudar o tipo, ou clique em outro campo

### Problema: "Tipo não aparece na coluna de dados"
**Solução:** Se o tipo for muito longo, truncamento é esperado. Clique "Visualizar Detalhes" para ver completo

### Problema: "Tipo sempre aparece como 'Convencional Onshore' na importação"
**Solução:** Adicione coluna `Tipo_Reservatorio` ao seu arquivo CSV/Excel

---

## 📞 Suporte

Para dúvidas ou sugestões sobre a funcionalidade de tipos:
- Revise o documento: `IMPLEMENTACAO_TIPOS_RESERVATORIO.md`
- Consulte as penalidades em: `v8.py` linha ~925
- Veja os tipos em: `v8.py` método `_load_reservoir_types()`

---

**Última Atualização:** 23 de Janeiro de 2026
**Versão:** PetroNalysis v8 com Tipos de Reservatório
**Status:** ✅ Operacional
