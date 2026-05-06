


1



ENGENHARIA DE RESERVATÓRIOS I
3º ANO – 2º SEMESTRE
2025 - 2026
1
Docente: Prof. Dr. Geraldo A. R. Ramos
1Engenharia de Reservatórios I
Geraldo Ramos, BSc, MSc, PhD
Capítulo 5 – Equação de Balanço de Materiais
▪ 5.1. Objectivo Geral e Objectivos Específicos
▪ 5.2. Introdução à Equação de Balanço de Materiais
▪ 5.3. Equação de balanço de materiais Generalizada;
▪ 5.4. Equação de Balanço de Materiais em reservatórios de óleo;
▪ 5.5. Equação de Balanço de Materiais em reservatórios de gás;
▪ 5.6. Técnicas de análise das Equações de Balanço de Materiais
▪ 5.7. Vantagens e desvantagens das equações de balanço de materiais;
▪ .5.8. Consolidação da Aula
▪ 5.9. Tarefas
 # ENGENHARIA DE RESERVATÓRIOS I
 **3º Ano – 2º Semestre — 2025–2026**

 **Docente:** Prof. Dr. Geraldo A. R. Ramos

 ---

 ## Capítulo 5 — Equação de Balanço de Materiais

### Sumário
- 5.1 Objetivo geral e objetivos específicos
- 5.2 Introdução à EBM
- 5.3 Equação de Balanço de Materiais (forma geral)
- 5.4 EBM para reservatórios de óleo (linearização)
- 5.5 EBM para reservatórios de gás
- 5.6 Técnicas de análise (gráficos e métodos)
- 5.7 Vantagens e limitações
- 5.8 Consolidação da aula (exercícios)
- 5.9 Tarefas
- Bibliografia

---

## 5.1 Objetivo geral
Aplicar a equação de balanço de materiais (EBM) para quantificar volumes em reservatórios de óleo e gás, integrando dados de produção, PVT e propriedades do reservatório, e avaliando a incerteza das estimativas.

### Objetivos específicos
- Explicar os fundamentos e hipóteses da EBM.
- Interpretar os termos da EBM generalizada.
- Aplicar a linearização (Havlena & Odeh) para estimar volumes e parâmetros desconhecidos.
- Comparar técnicas de análise e discutir vantagens/limitações.

## 5.2 Introdução
A EBM baseia‑se no balanço de massa dos fluidos presentes nos poros do reservatório. Em termos práticos, relaciona o fluido produzido e injetado com a variação do estoque no reservatório, permitindo estimar o volume originalmente em lugar (N) ou parâmetros como o fator de recuperação.

A técnica situa‑se entre a estimativa volumétrica e a simulação: usa dados de produção (e PVT) para inferir o estoque sem exigir dimensões detalhadas do reservatório.

## 5.3 Equação de Balanço de Materiais — forma geral
Em termos gerais, a EBM pode ser escrita como uma relação entre os termos de produção/injeção/influxo e as variações volumétricas e compressibilidades. Uma forma útil para análise prática é escrever a equação como:

$$
F = N E_o + m E_g + (1+m) E_{f,w} + W_e
$$

onde os termos são definidos abaixo (Havlena & Odeh, 1963) e $F$ representa o lado conhecido (produções e injecções).

## 5.4 EBM para reservatórios de óleo — linearização (Havlena & Odeh)
Para facilitar a estimação dos parâmetros desconhecidos, a EBM é linearizada agrupando termos de variação de volume, compressibilidade e contribuição do gas‑cap. As definições práticas são:

$$E_o = B_o - B_{o,i} + (R_{s,i} - R_s)\,B_g$$

$$E_g = B_{o,i}\left(\frac{B_g}{B_{g,i}} - 1\right)$$

$$E_{f,w} = B_{o,i}\left(S_{w,i}c_w + \frac{c_f}{1-S_{w,i}}\Delta p\right)$$

e o termo conhecido (lado esquerdo) é, por exemplo:

$$F = N_p B_o + G_p - R_s B_g + W_p B_w - W_{inj} B_w - G_{inj} B_{g,inj}$$

Assim, a equação linear para regressão fica:

$$F = N E_o + m E_g + (1+m) E_{f,w} + W_e$$

onde $N$ (estoque original), $m$ (razão do gas‑cap/óleo) e outros parâmetros podem ser estimados por ajuste linear de $F$ versus os termos $E_o, E_g, E_{f,w}$.

## 5.5 EBM para reservatórios de gás
Para reservatórios dominados por gás a formulação é adaptada; utiliza‑se o fator de volume do gás $B_g$ e considera‑se o comportamento PVT do gás. Técnicas similares de linearização e plotagem (ex.: material balance gas plots) são usadas para estimar OGIP e responder por influxos.

## 5.6 Técnicas de análise
- Plotagens clássicas de material balance (ex.: $F$ vs $E_o$, $F$ vs combinação linear) para estimar $N$ e $m$.
- Uso de regressão linear múltipla (Havlena & Odeh) para separar contribuições de compressibilidade e gas‑cap.
- Análise de sensibilidade e propagação de incerteza (p.ex. Monte Carlo) para obter P10/P50/P90.

## 5.7 Vantagens e limitações
- Vantagens: não requer geometria detalhada; integra dados de produção; fornece estimativas robustas quando dados de produção e PVT são confiáveis.
- Limitações: sensível a erros de PVT, incertezas em volumes injetados, e viés por heterogeneidade ou comunicação entre zonas; exige QA/QC rigoroso dos dados.

## 5.8 Consolidação da aula — Exercícios
1) Explique a lógica da linearização de Havlena & Odeh.
2) Dado um conjunto de dados de produção e PVT, descreva os passos para construir o termo $F$ e os termos $E_o,E_g,E_{f,w}$.
3) Discuta como incluir influxo de aquífero e injeção de água na formulação.

## 5.9 Tarefas
1) Aplicar a linearização Havlena & Odeh a um conjunto de dados hipotético (fornecerei os dados se desejar).
2) Fazer uma análise de sensibilidade para $B_o$, $\phi$ e $S_{w,i}$ e discutir o impacto nas reservas estimadas.
3) Preparar um pequeno relatório comparando EBM e método volumétrico para um mesmo caso.

## Bibliografia
1. DAKE, L. P. Engenharia de Reservatórios: fundamentos. Elsevier, 2014.
2. HAVLENA, V. & ODEH, A. (1963). The Material Balance as a Reservoir Management Tool. SPE.
3. AHMED, T. Reservoir Engineering Handbook. Elsevier, 2010.

---

## Definições importantes
- **Termo $F$ (lado conhecido):** representa as quantidades medidas de produção/injeção devidamente convertidas para volumes de superfície usados na EBM.
- **$N$ (estoque original):** volume originalmente em lugar de óleo (STB) ou gás (scf/Sm3).
- **$m$ (razão gas‑cap/óleo):** relação entre volumes de gás livre no gas‑cap e volume de óleo no reservatório.
- **$E_o, E_g, E_{f,w}$:** termos de variação volumétrica do óleo, do gás e do fluido de formação/água respectivamente (definidos na linearização Havlena & Odeh).

## Exemplo prático — aplicação simplificada da linearização Havlena & Odeh
Considere um caso hipotético com os seguintes dados simplificados por período acumulado (valores ilustrativos):
- Produção acumulada de óleo $N_p = 100{,}000\,$STB;
- Produção acumulada de gás $G_p = 50{,}000\,$scf (convertido para as mesmas unidades apropriadas);
- $B_{o,i}=1.1$, $B_o$ atual = 1.15; $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB; $B_g=0.005$ respec.

Calcule um termo $E_o$ simplificado:
$$
E_o = B_o - B_{o,i} + (R_{s,i} - R_s)B_g
$$
Substituindo valores (exemplo):
$$
E_o = 1.15 - 1.10 + (200-180)\times0.005 = 0.05 + 20\times0.005 = 0.05 + 0.10 = 0.15
$$
Se repetirmos esse cálculo para várias datas e obtivermos $F$ correspondente, um ajuste linear de $F$ versus $E_o$ (junto com $E_g$ e $E_{f,w}$) permite estimar $N$ (coeficiente angular/intercepto dependendo da formulação).

## Observações práticas
- Garantir que todos os volumes e fatores $B$ estejam convertidos para o mesmo sistema de unidades antes de montar $F$.
- Corrigir por volumes injetados ($W_{inj},G_{inj}$) e por perdas/erros de medição.
- Em presença de aquífero, incluir o termo $W_e$ de forma explícita e considerar modelos simplificados de influxo para estimativa.

## Glossário de símbolos (cap.5)
- `F` — termo conhecido (volume produzido/injetado convertido para superfície).
- `N` — estoque original de óleo (STB).
- `m` — razão gas‑cap/óleo (adimensional).
- `E_o, E_g, E_{f,w}` — termos de variação na linearização da EBM.
- `B_o, B_g` — fatores de volume de formação do óleo e do gás.
- `N_p, G_p` — produção acumulada de óleo e gás.
- `W_e` — contribuição do influxo de água (aquífero).

## Dicas rápidas de estudo
- Organize os dados de produção e PVT em uma planilha com colunas para $N_p,G_p,B_o,B_g,R_s$ e calcule $F,E_o,E_g,E_{f,w}$ periodicamente.
- Plote pares $(F,E_o)$ e $(F,E_g)$ para observar linearidade e influências dominantes.
- Teste sensibilidade a erros de PVT (p.ex. variação de $B_o$) para entender impacto nas estimativas de $N$.

---

Muito obrigado(a)!
