# Guia de Complementação do TCC
## "A História da Engenharia de Reservatórios de Petróleo: Da Teoria Empírica à Era Digital"

**Autor**: Rocélio Da Silva  
**Instituição**: ISPTEC (Instituto Superior Politécnico de Tecnologias e Ciências)  
**Status**: ✅ Compilado com sucesso | 35 páginas | PDF gerado  
**Data**: 2026

---

## 📊 Status do Documento

| Elemento | Status | Observações |
|----------|--------|-------------|
| **Estrutura ABNT** | ✅ Completo | Capa, resumo, sumário, introdução, desenvolvimento, conclusão, referências |
| **Formatação LaTeX** | ✅ Validado | Compilação bem-sucedida, margens e espaçamento corretos |
| **Referências Bibliográficas** | ✅ Processadas | BibTeX implementado com 19 fontes |
| **Figuras TikZ** | ✅ 10 diagramas | Armadilhas, PVT, malha simulação, timeline, etc. |
| **Imagens Históricas** | ⏳ 7 placeholders | Requerem substituição para versão final |
| **Tabelas** | ✅ Completas | Marcos históricos, símbolos, abreviaturas |

---

## 🖼️ Imagens Faltantes (Placeholders \fbox{})

### 1. **Betume Mesopotâmico**
- **Linha**: ~450
- **Descrição**: Uso de betume natural na Mesopotâmia (c. 3000 a.C.)
- **Sugestão de Fonte**: Wikimedia Commons - "Bitumen use in ancient Mesopotamia" (domínio público)
- **Alternativa**: MDPI Open Access ou Museum images (domínio público anterior a 1928)
- **Procedimento**: 
  ```bash
  \includegraphics[width=0.72\textwidth]{figuras/betume_mesopotamia.jpg}
  ```

### 2. **Poço Drake (1859)**
- **Linha**: ~510
- **Descrição**: Poço de Edwin Drake em Titusville, Pensilvânia
- **Sugestão de Fonte**: Wikimedia Commons - "Drake Well Titusville 1859" (domínio público, pré-1928)
- **Procedimento**:
  ```bash
  \includegraphics[width=0.65\textwidth]{figuras/poco_drake_1859.jpg}
  ```

### 3. **Campo Petrolífero Histórico**
- **Linha**: ~570
- **Descrição**: Torre de perfuração (derrick) do final do século XIX (Baku/Pensilvânia)
- **Sugestão de Fonte**: Wikimedia Commons - "Baku oil fields 1890" ou "Oil Creek" (domínio público)
- **Procedimento**:
  ```bash
  \includegraphics[width=0.80\textwidth]{figuras/campo_historico_1890.jpg}
  ```

### 4. **Retrato Henry Darcy**
- **Linha**: ~580
- **Descrição**: Engenheiro hidráulico francês (1803–1858)
- **Sugestão de Fonte**: Wikimedia Commons - "Henri Darcy portrait" (domínio público)
- **Procedimento**:
  ```bash
  \includegraphics[width=0.40\textwidth]{figuras/henry_darcy_retrato.jpg}
  ```

### 5. **Microscopia de Rocha**
- **Linha**: ~870
- **Descrição**: MEV de arenito/carbonato mostrando estrutura de poros
- **Sugestão de Fonte**: MDPI Open Access, Journal of Petroleum Science & Engineering (licença aberta)
- **Alternativa**: Imagens educacionais de universidades (com permissão)
- **Procedimento**:
  ```bash
  \includegraphics[width=0.70\textwidth]{figuras/microscopio_rocha.jpg}
  ```

### 6. **Interface de Simulador Numérico**
- **Linha**: ~1050
- **Descrição**: Software de simulação de reservatórios (Eclipse, CMG IMEX ou Petrel)
- **Sugestão de Fonte**: 
  - Material educacional do fabricante (SLB/Schlumberger, CMG, Rock Flow Dynamics) - **verificar licença**
  - Screenshots de tutoriais públicos em YouTube
- **Alternativa**: Captura de tela de simulador acadêmico
- **Procedimento**:
  ```bash
  \includegraphics[width=0.80\textwidth]{figuras/simulador_reservatorio.png}
  ```

### 7. **Inteligência Artificial em Reservatórios**
- **Linha**: ~1260
- **Descrição**: Representação de ML/IA aplicada em engenharia de petróleo
- **Sugestão de Fonte**: 
  - Unsplash/Pexels - "Machine learning", "Neural network", "Data visualization" (licença gratuita)
  - Wikimedia: "Artificial neural network" (domínio público/CC)
- **Procedimento**:
  ```bash
  \includegraphics[width=0.78\textwidth]{figuras/ia_reservatorio.png}
  ```

---

## 📁 Estrutura de Diretórios Recomendada

```
histo/
├── historiadeengres.tex          ✓ Arquivo principal
├── referencias.bib               ✓ Referências bibliográficas
├── historiadeengres.pdf          ✓ PDF compilado
├── figuras/                       (criar diretório)
│   ├── betume_mesopotamia.jpg
│   ├── poco_drake_1859.jpg
│   ├── campo_historico_1890.jpg
│   ├── henry_darcy_retrato.jpg
│   ├── microscopio_rocha.jpg
│   ├── simulador_reservatorio.png
│   └── ia_reservatorio.png
└── GUIA_COMPLEMENTACAO.md         ✓ Este arquivo
```

---

## 🔧 Instruções para Substituição de Imagens

### Procedimento Geral:

1. **Criar diretório `figuras/`**:
   ```bash
   mkdir figuras
   ```

2. **Baixar/salvar as imagens** neste diretório

3. **Editar o arquivo `.tex`** para substituir `\fbox{}` por `\includegraphics`:
   
   Antes:
   ```latex
   \fbox{\parbox{0.72\textwidth}{\centering Fotografia...}}
   ```
   
   Depois:
   ```latex
   \includegraphics[width=0.72\textwidth]{figuras/betume_mesopotamia.jpg}
   ```

4. **Recompilar o PDF**:
   ```bash
   pdflatex -interaction=batchmode historiadeengres.tex
   bibtex historiadeengres.aux
   pdflatex -interaction=batchmode historiadeengres.tex
   ```

---

## ✅ Checklist de Finalização

- [ ] Substituir 7 imagens faltantes (ou validar uso de placeholders TikZ)
- [ ] Verificar se todas as datas/nomes están corretos (apresentação, banca)
- [ ] Validar todas as citações bibliográficas
- [ ] Revisar ortografia e gramática
- [ ] Imprimir prova (verificar qualidade de página)
- [ ] Salvar PDF em versão de arquivo final: `historiadeengres_FINAL_2026.pdf`
- [ ] Preparar versão para submissão digital na plataforma ISPTEC

---

## 📞 Fontes de Imagens Recomendadas

| Fonte | Tipo | Licença | URL |
|-------|------|---------|-----|
| **Wikimedia Commons** | Histórico, domínio público | CC0, PD | https://commons.wikimedia.org |
| **MDPI Open Access** | Microscopia, pesquisa | CC, Open Access | https://www.mdpi.com |
| **Unsplash** | Moderno, conceitual | CC0 | https://unsplash.com |
| **Pexels** | Moderno, conceitual | CC0 | https://www.pexels.com |
| **Internet Archive** | Histórico | Variável | https://archive.org |
| **SPE (Society of Petroleum Engineers)** | Técnico, educacional | Verificar | https://www.spe.org |

---

## 📝 Notas Importantes

1. **Diretos Autorais**: Todas as imagens utilizadas devem ter licença compatível com publicação acadêmica
2. **Créditos**: Incluir fonte/autoria em cada figura (já está estruturado no template)
3. **Resolução**: Mínimo 300 DPI para impressão
4. **Formato**: Preferir JPG para fotos, PNG para diagramas
5. **Tamanho**: Procurar manter < 500 KB por imagem para não inflacionar o PDF

---

## 🏆 Principais Pontos Fortes do TCC

- ✅ **Estrutura Narrativa Excelente**: Progressão lógica das 4 eras
- ✅ **Fundamentação Sólida**: 19 referências bibliográficas de qualidade
- ✅ **Rigor Académico**: Citações inline, tabelas, figuras com legendas
- ✅ **Contexto Angolano**: Conexão com ISPTEC e realidade nacional
- ✅ **Diagramas Técnicos**: 10 figuras TikZ bem elaboradas
- ✅ **Bilíngue**: Resumos em português e inglês

---

## 📌 Recomendações Adicionais

1. **Para Apresentação Oral**: Preparar slides resumindo os 4 marcos paradigmáticos
2. **Para Defesa**: Estar pronto para diskussões sobre IA/ML e CCS em Angola
3. **Para Publicação**: Considerar converter capítulos para artigos em periódicos especializados
4. **Para Continuidade**: Possível linha de pesquisa em "Reservatórios Angolanos Pré-sal"

---

**Documento compilado com sucesso em 2026**  
**PDF Final: historiadeengres.pdf (35 páginas, 0.56 MB)**
