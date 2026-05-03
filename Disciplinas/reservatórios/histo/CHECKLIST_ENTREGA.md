# Checklist Final de Entrega do TCC
## "A História da Engenharia de Reservatórios de Petróleo"

**Instituição**: ISPTEC (Instituto Superior Politécnico de Tecnologias e Ciências)  
**Autor**: Rocélio Da Silva  
**Orientador**: Prof. Geraldo André Raposo Ramos  
**Disciplina**: Engenharia de Reservatórios  
**Modo**: Trabalho de Avaliação Contínua  
**Data de Conclusão**: 2026

---

## ✅ CONFORMIDADE COM NORMAS TCC

### Estrutura Conforme ABNT NBR 14724:2011

- [x] **Elementos Pré-Textuais**
  - [x] Capa (com todos os dados necessários)
  - [x] Folha de Rosto (com verso contendo ficha catalográfica)
  - [x] Ficha Catalográfica
  - [x] Folha de Aprovação (com espaços para data e assinatura)
  - [x] Resumo em português (máx. 500 palavras)
  - [x] Resumo em inglês (Abstract)
  - [x] Listas (figuras, tabelas, abreviaturas, símbolos)
  - [x] Sumário (com numeração correta)

- [x] **Elementos Textuais**
  - [x] Introdução (objetivos, justificativa, metodologia)
  - [x] Desenvolvimento (capítulo principal com 4 seções)
  - [x] Conclusão (síntese e recomendações)

- [x] **Elementos Pós-Textuais**
  - [x] Referências Bibliográficas (formato ABNT)
  - [ ] Apêndices (se necessário)
  - [ ] Anexos (se necessário)

### Formatação Técnica

- [x] Fonte: Times New Roman 12pt
- [x] Espaçamento: 1.5 entre linhas
- [x] Margens: Esq 3cm, Dir 2cm, Sup 3cm, Inf 2cm (ISPTEC)
- [x] Parágrafos: Primeira linha com 1.25cm de indentação
- [x] Alinhamento: Justificado
- [x] Numeração: Capítulos em algarismos arábicos
- [x] Citações: ABNT autor-ano com abntex2cite

### Conteúdo Técnico

- [x] Resumo estruturado (problema, metodologia, resultados, conclusão)
- [x] Introdução com contexto, problema, objetivos e metodologia
- [x] Desenvolvimento coerente em 4 macroseções temáticas
- [x] Conclusão com síntese e recomendações futuras
- [x] Referências bibliográficas de qualidade (internacionais e lusófonas)

---

## 📚 VALIDAÇÃO DE CONTEÚDO ACADÉMICO

### Qualidade das Referências

| Aspecto | Avaliação | Detalhe |
|---------|-----------|--------|
| **Quantidade** | ✅ Excelente | 19 fontes (adequado para TCC) |
| **Relevância** | ✅ Alta | Clássicos e contemporâneos |
| **Diversidade** | ✅ Boa | Inglês, português, técnico |
| **Atualidade** | ✅ Bom | 2006-2020 + clássicos de 1856-1979 |
| **Autoria Lusófona** | ✅ Presente | Ramos (2016, 2020), Rosa et al. (2006) |

### Estrutura Argumentativa

- [x] Narrativa histórica clara (4 eras paradigmáticas)
- [x] Conexão entre marcos teóricos e aplicação prática
- [x] Contextualização angolana (alinhada com ISPTEC)
- [x] Visão multidisciplinar (física, matemática, computação, economia)
- [x] Perspectiva crítica (evita obsolescência do conhecimento)

### Originalidade e Escopo

- [x] Trabalho de pesquisa bibliográfica (não plágio)
- [x] Síntese original de conhecimento histórico
- [x] Análise crítica da evolução disciplinar
- [x] Contribuição ao contexto angolano/africano
- [x] Relevância para formação de engenheiros nacionais

---

## 🖥️ VALIDAÇÃO TÉCNICA LaTeX

### Compilação

- [x] **PDFLaTeX**: Compila sem erros críticos
- [x] **BibTeX**: Processa 19 referências sem falhas
- [x] **Múltiplos Passes**: Referências cruzadas resolvidas
- [x] **Output PDF**: 35 páginas, 0.56 MB

### Elementos Gráficos

- [x] 10 figuras TikZ integradas sem erros
- [x] Legendas para todas as figuras
- [x] Fontes adequadas (Fonte: ... em cada figura)
- [x] Referências cruzadas funcionam (Fig.~\ref{})
- [x] 1 tabela de marcos históricos (longtable)

### Integridade de Documento

- [x] Índice/Sumário gerado automaticamente
- [x] Links internos funcionando
- [x] Hiperlinks com cores pretas (conforme ABNT)
- [x] Páginas numeradas corretamente
- [x] Cabeçalhos e rodapés apropriados

---

## 📋 ITENS PENDENTES (Versão Final)

### Críticos (Obrigatório antes de entrega)

- [ ] **Folha de Aprovação**: Preencher data de apresentação
- [ ] **Folha de Aprovação**: Obter assinatura do orientador
- [ ] **Folha de Aprovação**: Obter assinatura de examinadores (se aplicável)
- [ ] **Imagens Placeholder**: Substituir 7 figuras \fbox{} por imagens reais
  - [ ] Betume mesopotâmico
  - [ ] Poço Drake
  - [ ] Campo histórico
  - [ ] Retrato Darcy
  - [ ] Microscopia de rocha
  - [ ] Interface simulador
  - [ ] IA/Machine Learning

### Importante (Recomendado)

- [ ] Revisar ortografia com ferramenta (Hunspell/Aspell)
- [ ] Validar todas as citações são atualizadas no texto
- [ ] Confirmar que nenhuma figura saiu do eixo de página
- [ ] Testar impressão em papel A4 (visualizar em 100%)
- [ ] Validar que QR-codes ou links (se houver) funcionam

### Complementar (Opcional)

- [ ] Adicionar dedicatória (página anterior ao resumo)
- [ ] Adicionar agradecimentos (após dedicatória)
- [ ] Criar versão em HTML para arquivos digitais
- [ ] Preparar versão compactada para e-mail (< 5 MB)

---

## 📤 PROCEDIMENTO DE FINALIZAÇÃO

### Passo 1: Prepare as Imagens
```bash
# Criar diretório para imagens
mkdir figuras

# Salvar as 7 imagens correspondentes em formato JPG/PNG
# Manter resolução mínima 300 DPI para impressão
```

### Passo 2: Atualize o Documento
```latex
% Substituir cada \fbox{\parbox...} por:
\includegraphics[width=0.72\textwidth]{figuras/nome_imagem.jpg}
```

### Passo 3: Recompile o PDF Final
```bash
cd histo/
pdflatex -interaction=batchmode historiadeengres.tex
bibtex historiadeengres.aux
pdflatex -interaction=batchmode historiadeengres.tex
pdflatex -interaction=batchmode historiadeengres.tex
```

### Passo 4: Valide o Resultado
```bash
# Verificar número de páginas (deve ser 35+)
pdfinfo historiadeengres.pdf

# Verificar tamanho (tipicamente 0.5-2 MB)
ls -lh historiadeengres.pdf
```

### Passo 5: Prepare para Entrega
```bash
# Criar cópias nomeadas por versão
cp historiadeengres.pdf historiadeengres_FINAL_2026.pdf
cp historiadeengres.pdf "Rocélio_TCC_Engenharia_Reservatórios.pdf"

# Compactar para submissão digital (se necessário)
zip -r TCC_Rocélio_2026.zip historiadeengres_FINAL_2026.pdf GUIA_COMPLEMENTACAO.md
```

---

## 🎓 INFORMAÇÕES DE ENTREGA

### Formato de Arquivo

- **Formato Principal**: PDF (historiadeengres.pdf)
- **Formato Alternativo**: PDF com nome descritivo para arquivo
- **Suporte**: Arquivo LaTeX (.tex) + Referências (.bib) + Figuras (pasta)

### Entrega Digital

- Plataforma: [Especificar plataforma ISPTEC]
- Formato: PDF único ou ZIP com suplementares
- Limite de Arquivo: [Verificar com coordenação]
- Data Limite: [Confirmar com professor orientador]

### Entrega Física (se requerido)

- [ ] Impressão em papel A4 branco, 75 g/m²
- [ ] Encadernação: Espiral, grampo ou cola (conforme orientação)
- [ ] Número de Cópias: 1 (validar com ISPTEC)
- [ ] Acondicionamento: Envelope A4 com dados de identificação

---

## 📞 CONTATO PARA ESCLARECIMENTOS

- **Orientador**: Prof. Geraldo André Raposo Ramos
- **Coordenação do Curso**: Departamento de Geociências - ISPTEC
- **Referências ABNT**: http://www.abntex.net.br/

---

## 📌 RESUMO TÉCNICO DO DOCUMENTO

| Metadado | Valor |
|----------|-------|
| **Título** | A história da Engenharia de Reservatórios de Petróleo: Da Teoria Empírica à Era Digital |
| **Autor** | Rocélio Da Silva |
| **Orientador** | Prof. Geraldo André Raposo Ramos |
| **Instituição** | ISPTEC - Luanda, Angola |
| **Tipo** | Trabalho de Avaliação Contínua |
| **Páginas** | 35 |
| **Figuras** | 10 (TikZ) + 7 (placeholders) = 17 total |
| **Tabelas** | 2 (símbolos + marcos históricos) |
| **Referências** | 19 |
| **Palavras-chave** | 8 |
| **Idiomas** | Português + Inglês (resumo) |
| **Tamanho PDF** | ~0.56 MB |
| **Status** | ✅ Pronto para revisão final |

---

**Documento gerado: 2026**  
**Próxima etapa: Revisão orientador → Correções → Entrega final**
