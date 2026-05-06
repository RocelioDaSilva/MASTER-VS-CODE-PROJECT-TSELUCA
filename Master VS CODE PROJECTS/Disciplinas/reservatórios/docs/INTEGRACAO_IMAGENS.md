# Integração de Imagens na Apresentação

## Status: ✅ COMPLETO

Todas as imagens do diretório `histo/figuras/` foram integradas na apresentação PPTX: `Historia_Eng_Reservatorios_ISPTEC.pptx`

---

## Imagens por Slide

### 🏛️ Slide 1 – Capa
- **logo isptec.png** — Logo institucional (canto superior direito)

### 📋 Slide 2 – Sumário
- **transferir.jpg** — Imagem técnica decorativa (canto inferior direito)

### 📖 Slide 3 – Introdução
- **afloramento natural de betume fonte-.jpg** — Contexto histórico (coluna direita)

### 🎯 Slide 4 – Objetivos
- **angola_relief_map.png** — Mapa de Angola contextual (coluna direita)

### ⚖️ Slide 5 – Justificativa
- **balakhani_1904.png** — Histórico de campo (decorativo, canto inferior)

### 🌊 Slide 6 – As Quatro Eras
- **afloramento natural de betume fonte-.jpg** — Era 1: Empírica
- **drake_well.jpg** — Era 2: Fundamentação
- **cdc_7600_1969.jpg** — Era 3: Consolidação
- **701px-Conducting-a-reservoir-simulation-study-an-overview_fig3.png** — Era 4: Digital

### 🏆 Slide 7 – Marcos Teóricos (Grid 3×2)
- **Henry_Darcy.jpg** — Henry Darcy (1856)
- **Modified schematic diagram of Darcy's experimental apparatus.png** — Aparato experimental
- **eniac_1946.jpg** — ENIAC (1946)
- **cdc_7600_1969.jpg** — CDC 7600 (1969)
- **Portrait of Morris Muska.png** — Morris Muskat
- **Classic_shot_of_the_ENIAC_(full_resolution).jpg** — ENIAC – Visão completa

### 🔬 Slide 8 – Era Digital
- **701px-Conducting-a-reservoir-simulation-study-an-overview_fig3.png** — Simulação numérica
- **Enhanced-oil-recovery.png** — Métodos EOR
- **angola_relief_map.png** — Contexto de Angola

### 🎓 Slide 9 – Conclusão
- **The first oil well-.jpg** — Primeiro poço (decorativo, canto inferior)

### 📚 Slide 10 – Referências
- **balakhani_1904.png** — Ref. 1856 (Darcy)
- **cdc_7600_1969.jpg** — Ref. 1936 (Schilthuis)
- **The first oil well-.jpg** — Ref. 1951 (Horner)
- **eniac_1946.jpg** — Ref. 1978 (Dake)
- **service-pnp-cph-3a10000-3a14000-3a14100-3a14109r.jpg** — Ref. 2010 (Ahmed)

---

## Inventário Completo

| # | Arquivo | Slide | Contexto | Status |
|---|---------|-------|---------|--------|
| 1 | afloramento natural de betume fonte-.jpg | 3, 6 | Histórico; Era 1 | ✅ |
| 2 | angola_relief_map.png | 4, 8 | Contexto Angola; Bloco Digital | ✅ |
| 3 | balakhani_1904.png | 5, 10 | Decorativo; Referência | ✅ |
| 4 | cdc_7600_1969.jpg | 6, 7, 10 | Era 3; Marcos; Referência | ✅ |
| 5 | Classic_shot_of_the_ENIAC_(full_resolution).jpg | 7 | Marcos Teóricos | ✅ |
| 6 | 701px-Conducting-a-reservoir-simulation-study-an-overview_fig3.png | 6, 8 | Era 4; Simulação | ✅ |
| 7 | drake_well.jpg | 6 | Era 2: Fundamentação | ✅ |
| 8 | Enhanced-oil-recovery.png | 8 | EOR – Métodos | ✅ |
| 9 | eniac_1946.jpg | 7, 10 | Marcos; Referência | ✅ |
| 10 | Henry_Darcy.jpg | 7 | Marcos Teóricos | ✅ |
| 11 | logo isptec.png | 1 | Capa – Logo institucional | ✅ |
| 12 | Modified schematic diagram of Darcy's experimental apparatus.png | 7 | Marcos Teóricos | ✅ |
| 13 | Portrait of Morris Muska.png | 7 | Marcos Teóricos | ✅ |
| 14 | The first oil well-.jpg | 9, 10 | Conclusão; Referência | ✅ |
| 15 | service-pnp-cph-3a10000-3a14000-3a14100-3a14109r.jpg | 10 | Referência (2010) | ✅ |
| 16 | transferir.jpg | 2 | Sumário – Decorativo | ✅ |
| — | README_IMAGENS.txt | — | Metadados (não integrado) | — |

---

## Resumo

- **Total de imagens principais**: 16
- **Imagens integradas**: 16 ✅
- **Taxa de integração**: 100%
- **Referências únicas em slides**: Cada imagem aparece de 1 a 3 vezes (dependendo do contexto)
- **Compatibilidade**: Todos os caminhos relativos validados; fallback para placeholders configurado

---

## Notas Técnicas

- **Padrão de caminho**: `os.path.join(FIGURAS_PATH, "nome-arquivo")`
- **FIGURAS_PATH**: `histo/figuras/` (configurado no inicio do script)
- **Tratamento de erros**: Função `_img()` gerencia paths ausentes com stylized placeholder
- **Resoluções ajustadas**: Imagens redimensionadas para layouts específicos de slide (sem distorção de aspecto)
- **Integração**: Realizada sem substituição ou remoção de conteúdo existente

---

**Apresentação finalizada**: `Historia_Eng_Reservatorios_ISPTEC.pptx`
**Data de geração**: 2026-04-09
