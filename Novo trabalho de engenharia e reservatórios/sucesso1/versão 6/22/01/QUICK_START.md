# QUICK START - PetroChamp v6.0

## ⚡ Em 5 Minutos

### 1️⃣ Execute a Triagem
```
Aba "Triagem" → Preencha parâmetros → Clique "Executar Triagem"
```

### 2️⃣ Explore a Matriz
```
Aba "Suitability" → Aba "Matriz"
├─ Clique "Todos" (seleciona 15 métodos)
├─ Clique "Gerar Matriz"
├─ Selecione um método no dropdown
└─ Veja características na caixa azul
```

### 3️⃣ Veja Gráficos
```
Aba "Resultados" → Aba "Gráficos"
├─ Selecione tipo no combobox
├─ Clique "Gerar Gráfico"
└─ Exporte em PNG/PDF/SVG
```

---

## 🎯 Por Tarefa

### Quero comparar 3 métodos
```
1. Aba Suitability → Aba Matriz
2. Desmarque tudo clicando "Nenhum"
3. Marque apenas 3 métodos
4. Aba Comparativo
5. Escolha tipo "Radar"
6. Clique "Métodos Selecionados"
```

### Quero ver todos em um gráfico
```
1. Aba Resultados → Aba Gráficos
2. Selecione "Dashboard Completo"
3. Clique "Gerar Gráfico"
```

### Quero exportar em alta qualidade
```
1. Gere um gráfico
2. Clique "Exportar Gráfico"
3. Escolha tipo (PNG = pequeno, PDF = melhor)
4. Salve no local desejado
```

### Quero ver características de um método
```
1. Aba Suitability → Aba Matriz
2. Clique "Gerar Matriz"
3. Selecione método no dropdown
4. Leia a caixa azul abaixo
```

---

## 📊 Tipo de Gráfico Recomendado Por Caso

| Situação | Gráfico | Onde |
|----------|---------|------|
| Ver todos os métodos | Barras | Resultados |
| Comparar 2-3 métodos | Radar | Comparativo |
| Ver distribuição | Pizza | Resultados |
| Análise completa | Dashboard | Resultados |
| Tendência | Linha | Resultados |
| Quartis | Box Plot | Resultados |
| Outliers | Dispersão | Resultados |

---

## 🎨 Cores no Sistema

```
Verde    #27ae60  →  Alta Suitability (≥80%)
Laranja  #f39c12  →  Média Suitability (60-79%)
Vermelho #e74c3c  →  Baixa Suitability (<60%)
Azul     #d6eaf8  →  Características importantes
```

---

## ❓ Problemas Comuns

### "Execute a triagem primeiro"
→ Vá para aba "Triagem", preencha e clique "Executar Triagem"

### Gráfico não aparece
→ Clique "Limpar" e tente novamente

### Texto truncado
→ Use zoom na toolbar matplotlib (botão com lupa +)

### Muitos métodos em Radar
→ Selecione menos métodos ou use "Barras"

---

## 🎬 Fluxo Ideal

```
START
  ↓
Triagem (2 min) ────────────────────┐
  ↓                                   ↓
Suitability → Matriz (5 min) ──→ Comparativo (3 min)
  ↓                                   ↓
Resultados → Gráficos (2 min) ──→ Exportar (1 min)
  ↓
END ✅
```

**Tempo Total: 13 minutos**

---

## 📱 Interface em 30 segundos

### Aba Suitability

```
┌─ Suitability ──────────────────────────┐
│                                         │
│  ┌─ Matriz ──────────────────────────┐ │
│  │ [Todos] [Nenhum] [Gerar Matriz]  │ │
│  │ Checkboxes dos 15 métodos        │ │
│  │ Matriz com 14 parâmetros         │ │
│  │ Caixa azul com características   │ │
│  └─────────────────────────────────┘ │
│                                         │
│  ┌─ Visão Geral ─────────────────────┐ │
│  │ [Gerar Gráficos] [Spider] [Dash] │ │
│  │ Exibe múltiplos gráficos          │ │
│  └─────────────────────────────────┘ │
│                                         │
│  ┌─ Gráficos Individuais ────────────┐ │
│  │ Método: [Dropdown] Tipo: [Combo] │ │
│  │ [Gerar] Exibe 1 gráfico           │ │
│  └─────────────────────────────────┘ │
│                                         │
│  ┌─ Comparativo ─────────────────────┐ │
│  │ Tipo: [Combo ▼] (5 opções)       │ │
│  │ Checkboxes dos 15 métodos        │ │
│  │ [Todos] [Selecionados]           │ │
│  │ Exibe gráfico de comparação      │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Aba Resultados

```
┌─ Resultados ───────────────────────────┐
│                                         │
│  ┌─ Gráficos ────────────────────────┐ │
│  │ Tipo: [Combobox com 8 opções ▼]  │ │
│  │ [Gerar] [Exportar] [Limpar]       │ │
│  │                                    │ │
│  │ ┌─ Gráfico Dinâmico ───────────┐ │ │
│  │ │ Renderiza em tamanho completo│ │ │
│  │ │ Com toolbar (zoom, pan, save)│ │ │
│  │ └──────────────────────────────┘ │ │
│  └─────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────┘
```

---

## 🔑 Atalhos de Teclado

| Ação | Onde |
|------|------|
| Tab | Navegar entre elementos |
| Enter | Ativar botão |
| Space | Marcar/desmarcar checkbox |
| Ctrl+A | Selecionar tudo (em combobox) |

---

## 📞 Ajuda Rápida

| Pergunta | Resposta |
|----------|----------|
| Como comparar métodos? | [GUIA_USO_V6.md#aba-suitability---comparativo](GUIA_USO_V6.md) |
| Como exportar? | [GUIA_USO_V6.md#aba-resultados---gráficos](GUIA_USO_V6.md) |
| Qual gráfico usar? | [GUIA_USO_V6.md#dicas--troubleshooting](GUIA_USO_V6.md) |
| Como testo? | [CHECKLIST_TECNICO.md](CHECKLIST_TECNICO.md) |

---

## ⏱️ Tempos Típicos

| Tarefa | Tempo |
|--------|-------|
| Executar triagem | 2-3 min |
| Gerar matriz | 30 seg |
| Comparar métodos | 2-3 min |
| Gerar gráfico | 1-2 seg |
| Exportar | 10-20 seg |
| **Total** | **~10 min** |

---

## 🎉 Recursos Disponíveis

✅ 21 tipos de gráficos  
✅ 15 métodos EOR  
✅ 4 sub-abas especializadas  
✅ Seleção dinâmica de métodos  
✅ Exportação em 3 formatos  
✅ Dashboard com KPIs  
✅ Características com pesos  

---

## 🚀 Próximo Passo

**Leia [GUIA_USO_V6.md](GUIA_USO_V6.md) para tutorial completo**

---

**Versão**: 6.0 | **Status**: ✅ Pronto  
**Tempo para começar**: 5 minutos | **Tempo para dominar**: 30 minutos

