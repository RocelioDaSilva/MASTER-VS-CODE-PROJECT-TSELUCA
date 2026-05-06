# Revisão para a prova — Gabarito e Rubricas

Este ficheiro reúne as 4 questões propostas para a prova, as respostas‑gabarito e as rubricas de correção.

---

## Questão 1 — Verdadeiro ou Falso (Capítulo 1)

Enunciado (10 itens, 1 pt cada):
1) A armadilha geológica impede a migração de hidrocarbonetos e permite sua acumulação.
2) Rocha geradora é caracterizada por baixa matéria orgânica.
3) Rocha selante tem alta permeabilidade e facilita o fluxo de fluidos.
4) Migração de hidrocarbonetos ocorre preferencialmente por meios porosos e fraturados.
5) Sincronismo (coincidência temporal de processos) é irrelevante para a formação de um sistema petrolífero.
6) Catagênese refere‑se ao craqueamento térmico do querogênio em hidrocarbonetos.
7) O sistema de produção inclui instalações de coleta, elevação e separação até a superfície.
8) Em um gas‑cap drive, o gás livre contribui para manter a pressão do reservatório.
9) Porosidade e permeabilidade são a mesma propriedade física.
10) O fator de volume de formação `B_o` relaciona volumes em reservatório ao volume na superfície.

### Gabarito Q1
1) V
2) F
3) F
4) V
5) F
6) V
7) V
8) V
9) F
10) V

### Rubrica Q1 (10 pts)
- 1 ponto por resposta correta.
- Se for solicitada justificativa: aceitar 1–2 frases; atribuir 0.5 pt para justificativa parcial.

---

## Questão 2 — Dissertação (Capítulo 4)

Enunciado:
Redija uma dissertação (≈ 400–600 palavras) que responda e discuta:
- Descreva o método volumétrico para estimativa de OOIP/OGIP e os principais parâmetros envolvidos (`A`, `h`, `\phi`, `S_w`, `B_o`, `B_g`).
- Explique as principais fontes de incerteza (cut‑offs, N/G, heterogeneidade, PVT) e como afetam a estimativa.
- Proponha um fluxo de trabalho prático para integrar mapas de net, dados de core, logs e PVT para obter uma estimativa com P10/P50/P90 (mencione Monte Carlo).
- Conclua com recomendações para comunicar risco e medidas para reduzir incerteza (QA/QC, aquisição de dados adicionais, sensibilidade).

### Rubrica Q2 (30 pts)
- Método volumétrico e parâmetros (12 pts): fórmula prática (ex.: $$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$), explicação de cada termo, menção a unidades campo vs SI. (12 pts)
- Fontes de incerteza (8 pts): identificação e explicação do impacto de cut‑offs, N/G, heterogeneidade, erros PVT. (8 pts)
- Fluxo de trabalho prático (6 pts): integração cores/logs/PVT, construção de mapas, cálculo setorial, sensibilidade e Monte Carlo para P10/P50/P90. (6 pts)
- Comunicação de risco e recomendações (4 pts): QA/QC, aquisição adicional, apresentação de Pxx e mitigação. (4 pts)

Critérios de avaliação:
- Conteúdo técnico: 60% dos pontos.
- Metodologia/prática: 20%.
- Comunicação/clareza e recomendações: 20%.

---

## Questão 3 — Cálculo / Prático (Capítulo 2 — PVT)

Enunciado:
Um ensaio PVT fornece os seguintes resultados para 1 STB de óleo amostrado: volume no estado de reservatório $V_{res}=1.20\,$bbl; volume correspondente à superfície $V_{surf}=1.00\,$STB; gás libertado no ensaio $R_s=400\,$scf/STB.

a) Calcule o fator de volume de formação `B_o` (bbl/STB) usando $B_o=V_{res}/V_{surf}$.

b) Expresse `R_s` em m³/m³ usando $1\,\text{scf}=0.0283168\,\text{m}^3$ e $1\,\text{STB}=0.1589873\,\text{m}^3$.

c) Interprete fisicamente um $B_o>1$ e discuta brevemente como $R_s$ influencia o comportamento de produção.

### Gabarito Q3 (30 pts — 10/10/10)
(a) $$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ (10 pts)

(b) Conversão: $$R_s\,\text{(m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3.$$ (10 pts)

(c) Interpretação: (10 pts)
- $B_o>1$ indica que 1 STB à superfície corresponde a mais de 1 bbl nas condições de reservatório (efeito de compressibilidade e/ou gás dissolvido); volumes no reservatório são maiores que o volume final surfacel.
- $R_s$ alto implica presença significativa de gás dissolvido; durante declínio de pressão, se atingir o ponto de bolha, o gás é liberado, alterando mobilidade do fluido, afetando recuperação e mecanismo de produção. Pontos por clareza e ligação a efeitos operacionais.

---

## Questão 4 — Cálculo / Prático (Capítulo 3 — Rocha)

Enunciado:
a) Porosidade por método de massa: uma amostra tem massa seca $m_{dry}=250\,$g e massa saturada $m_{sat}=290\,$g; densidade do fluido $\rho_f=0.90\,$g/cm³; volume total da amostra $V_t=320\,$cm³. Calcule a porosidade $\phi$ (use $V_p=(m_{sat}-m_{dry})/\rho_f$ e $\phi=V_p/V_t$).

b) Permeabilidade (Darcy): num ensaio de bancada obteve‑se vazão volumétrica $q=1.0\times10^{-6}\,\text{m}^3/s$, área da amostra $A=10\,\text{cm}^2=1.0\times10^{-3}\,\text{m}^2$, comprimento $L=5\,\text{cm}=0.05\,\text{m}$, viscosidade $\mu=1.0\,\text{cP}=0.001\,\text{Pa·s}$ e queda de pressão $\Delta p=10{,}000\,$Pa. Calcule `k` em m² e converta para Darcy (1 D = 9.869233×10⁻¹³ m²) usando a relação:
$$k=\dfrac{q\,\mu\,L}{A\,\Delta p}$$

### Gabarito Q4 (30 pts — 15/15)
(a) Porosidade (15 pts):
- $$V_p=\dfrac{m_{sat}-m_{dry}}{\rho_f}=\dfrac{290-250}{0.90}=\dfrac{40}{0.90}=44.444\;\text{cm}^3.$$ 
- $$\phi=\dfrac{V_p}{V_t}=\dfrac{44.444}{320}\approx0.1389\approx13.9\%. $$
(atribuir parcial se passos corretos; tolerância ±0.2–0.5% absoluta)

(b) Permeabilidade (15 pts):
- Aplicando Darcy:
  $$k=\dfrac{1\times10^{-6}\times0.001\times0.05}{1\times10^{-3}\times10{,}000}=5\times10^{-12}\;\text{m}^2.$$ 
- Converter para Darcy:
  $$k_{D}=\dfrac{5\times10^{-12}}{9.869233\times10^{-13}}\approx5.07\;\text{D}=5\,070\;\text{mD}.$$ 
(Aceitar pequenas variações por arredondamento; exigir todas as conversões)

---

## Pontuação total sugerida
- Q1: 10 pts
- Q2: 30 pts
- Q3: 30 pts
- Q4: 30 pts

Total: 100 pts.

## Observações finais sobre correção
- Para cálculos, exigir passos e unidades; penalizar falta de conversões ou unidades incoerentes.
- Para dissertação, pontuar conteúdo técnico, metodologia e clareza.
- Para todos os itens, aceitar pequenas variações numéricas quando justificadas por arredondamento.

---

*Arquivo gerado automaticamente pelo assistente.*
