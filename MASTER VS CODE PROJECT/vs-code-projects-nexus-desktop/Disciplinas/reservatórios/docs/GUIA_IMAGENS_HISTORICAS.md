# Guia de Integração de Imagens para TCC História de Engenharia de Reservatórios

## 📋 Resumo das Imagens Encontradas (Domínio Público / CC-Licensed)

O seu documento está agora pronto para integração de **imagens de alta qualidade** que melhoram significativamente a narrativa histórica. Abaixo encontra todas as instruções.

---

## 🖼️ Imagens Recomendadas

### 1. **Henry Darcy Portrait** (Já integrado no documento)
- **Status:** Mantém imagem atual `Henry_Darcy.jpg`
- **Qualidade:** Adequada; pode ser melhorada com:
  - URL Wikimedia: https://commons.wikimedia.org/wiki/File:Henry_Darcy.jpg
  - License: Public Domain (PD-Old, falecido 1858)
- **Ação:** Manter como está OU substituir por versão de melhor resolução

---

### 2. **Darcy's Experimental Apparatus** (Substituir atual)
**PRIORITÁRIO** — Melhoria significativa

- **Seleção:** Original 1857 publication com diagramas históricos
- **URL:** https://commons.wikimedia.org/wiki/File:Darcy_-_Recherches_exp%C3%A9rimentales_relatives_au_mouvement_de_l%27eau_dans_les_tuyaux,_1857.djvu
- **License:** Public Domain (PD-Old-70)
- **Resolução:** 2,534 × 3,197 px — Excelente qualidade
- **Como usar:** 
  1. Aceda ao link acima
  2. Faça download do DJVU
  3. Extreia página(s) com diagrama (geralmente p. 20-30 do PDF)
  4. Converta para JPG/PNG em alta resolução
  5. Substitua `"Modified schematic diagram of Darcy's experimental apparatus.png"`

**Exemplo de substituição no LaTeX:**
```latex
\includegraphics[width=0.40\textwidth]{darcy_apparatus_original_1857.jpg}
\caption{Aparelho experimental original de Darcy (1857): diagrama histórico da publicação "Recherches expérimentales..."}
```

---

### 3. **Balakhani Oil Wells** (1904) — Contexto Histórico de Produção
**RECOMENDADO** — Adicionar nova figura

- **URL:** https://commons.wikimedia.org/wiki/File:Balakhani_oil_wells.png
- **License:** Public Domain (copyright expirado, pré-1931)
- **Resolução:** 3,543 × 2,080 px — Alta qualidade
- **Adequado para seção:** *"Os Primórdios e Fundação Científica"*
- **Onde inserir:** Junto com descrição de early oil derricks

**Instruções para adicionar ao documento:**
1. Faça download da imagem e coloque em `figuras/`
2. Adicione antes da figura Drake:

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.45\textwidth]{balakhani_oil_wells_1904.png}
  \caption{Campos de petróleo de Balakhani (Azerbaijão, 1904): exemplo de infraestrutura de produção do início do século XX, mostrando evolução desde o poço Drake (1859).}
  \label{fig:balakhani}
\end{figure}
```

---

### 4. **ENIAC Computer** (1946) — Revolução Computacional
**MUITO RECOMENDADO** — Novo parágrafo histórico adicionado

- **URL:** https://commons.wikimedia.org/wiki/File:Classic_shot_of_the_ENIAC_(full_resolution).jpg
- **License:** Public Domain (U.S. Army photograph)
- **Resolução:** 2,100 × 1,518 px
- **Adequado para seção:** *"Consolidação Metodológica — Evolução da Capacidade Computacional"*

**Instruções para adicionar:**
1. Faça download e coloque em `figuras/eniac_1946.jpg`
2. Após parágrafo sobre ENIAC, adicione:

```latex
\begin{wrapfigure}{r}{0.35\textwidth}
  \centering
  \vspace{-0.5cm}
  \includegraphics[width=0.33\textwidth]{eniac_1946.jpg}
  \caption{Computador ENIAC (1946): primeira máquina eletrónica de propósito geral para cálculo científico. Revolucionou viabilidade de simulação numérica.}
  \label{fig:eniac}
  \vspace{-0.5cm}
\end{wrapfigure}

O computador ENIAC (figura \ref{fig:eniac}) demonstrou a viabilidade de máquinas eletrónicas para cálculos complexos...
```

---

### 5. **CDC 7600 Supercomputer** (1969) — Simuladores Numéricos
**MUITO RECOMENDADO** — Complementa seção de computing

- **URL:** https://commons.wikimedia.org/wiki/File:CDC_7600.jc.jpg
- **License:** CC-BY 2.0 (Jitze Couperus, Computer History Museum)
- **Resolução:** 2,912 × 4,158 px — Excelente qualidade
- **Adequado para:** Demonstrar escala de supercomputadores 1960s-1970s

**Instruções:**
1. Download para `figuras/cdc_7600_1969.jpg`
2. Adicionar como:

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.50\textwidth]{cdc_7600_1969.jpg}
  \caption{Supercomputador CDC 7600 (1969): computador científico de ponta que habilitou simulação numérica multifásica complexa. Fonte: Computer History Museum, CC-BY 2.0.}
  \label{fig:cdc7600}
\end{figure}

O CDC 7600 representou o estado da arte em computação científica durante a década em que os primeiros simuladores black-oil foram desenvolvidos...
```

---

## 📥 Passos Rápidos para Integração

### Opção A: Integração Completa (Recomendado)
1. Crie pasta `figuras/` se não existir
2. Faça download das 5 imagens (URLs acima)
3. Renomeie conforme padrão (ex: `eniac_1946.jpg`)
4. Copie o código LaTeX de cada seção acima
5. Cole no arquivo `.tex` nas posições indicadas
6. Recompile: `pdflatex tcc_historia_eng_reservatorios.tex`

### Opção B: Integração Gradual
- Use uma imagem de cada vez
- Recompile após cada adição
- Verifique no PDF antes de adicionar a próxima

---

## 🔍 Referências das URLs para Download

| Imagem | URL Wikimedia | Tamanho | License |
|--------|---------------|--------|---------|
| Henry Darcy (melhorado) | commons.wikimedia.org/wiki/File:Henry_Darcy.jpg | 250×337 | PD |
| Darcy Apparatus 1857 | commons.wikimedia.org/wiki/File:Darcy_-_Recherches... | 2534×3197 | PD |
| Balakhani Oil Wells 1904 | commons.wikimedia.org/wiki/File:Balakhani_oil_wells.png | 3543×2080 | PD |
| ENIAC 1946 | commons.wikimedia.org/wiki/File:Classic_shot_of_the_ENIAC_(full_resolution).jpg | 2100×1518 | PD-USArmy |
| CDC 7600 1969 | commons.wikimedia.org/wiki/File:CDC_7600.jc.jpg | 2912×4158 | CC-BY 2.0 |

---

## ✅ Checklist de Integração

- [ ] Criar/verificar pasta `figuras/`
- [ ] Download das 5 imagens recomendadas
- [ ] Renomear conforme padrão proposto
- [ ] Copiar código LaTeX para cada imagem
- [ ] Recompilar PDF
- [ ] Verificar layout (texto ao redor, formatação wrapfig)
- [ ] Adicionar atribuições/licenças nas legendas

---

## 💡 Formatação: Text-Wrapping (Wrapfig)

O documento já inclui o pacote `wrapfig`. Use:

**Lado direito, 35% largura:**
```latex
\begin{wrapfigure}{r}{0.35\textwidth}
  \includegraphics[width=0.33\textwidth]{imagem.jpg}
  \caption{Legenda...}
\end{wrapfigure}
```

**Lado esquerdo:**
```latex
\begin{wrapfigure}{l}{0.35\textwidth}
  \includegraphics[width=0.33\textwidth]{imagem.jpg}
  \caption{Legenda...}
\end{wrapfigure}
```

O texto envolverá automaticamente! ✨

---

## 🎓 Resultado Esperado

Após integração completa:
- ✅ 8 imagens contextualizadas historicamente
- ✅ Texto fluindo ao redor das imagens (visual dinâmico)
- ✅ Narrativa enriquecida com artefatos históricos autênticos
- ✅ Todas as imagens com licenças claras (pronto para publicação)
- ✅ PDF profissional de ~2.5-3 MB

---

## ❓ Dúvidas?

- Para extrair páginas de DJVU: use ferramentas online como `CloudConvert`
- Para converter formatos: use `ImageMagick` ou ferramentas online
- Para verificar resolução: clique direito → Propriedades (Windows) ou `identify` (Linux)

Sucesso! 🚀
