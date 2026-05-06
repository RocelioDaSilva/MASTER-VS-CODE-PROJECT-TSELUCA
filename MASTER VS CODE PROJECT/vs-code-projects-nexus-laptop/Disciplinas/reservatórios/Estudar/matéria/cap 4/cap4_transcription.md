


1



ENGENHARIA DE RESERVATÓRIOS I
3º ANO – 2º SEMESTRE
2025 - 2026
1
Docente: Prof. Dr. Geraldo A. R. Ramos
1Engenharia de Reservatórios I
Geraldo Ramos, BSc, MSc, PhD
Capítulo 4 - Integração de dados e Cálculo Volumétrico de Hidrocarbonetos
 # ENGENHARIA DE RESERVATÓRIOS I
 **3º Ano – 2º Semestre — 2025–2026**

 **Docente:** Prof. Dr. Geraldo A. R. Ramos

 ---

 ## Capítulo 4 — Integração de dados e Cálculo Volumétrico de Hidrocarbonetos

 ### Sumário
 - 4.1 Objectivo Geral e Objectivos Específicos
 - 4.2 Prefixos
 - 4.3 Introdução
 - 4.4 Definições
 - 4.5 Métodos de cálculo de volumes originalmente existentes
 - 4.6 Método volumétrico (parâmetros e fórmulas)
 - 4.7 Integração de dados e incertezas
 - 4.8 Consolidação da aula (exercícios)
 - 4.9 Tarefas
 - Bibliografia

 ---

 ## 4.1 Objetivo geral
Aplicar integração de dados geológicos, petrofísicos e de engenharia para estimar volumes originais de hidrocarbonetos (OOIP / OGIP) e volumes recuperáveis, considerando incertezas e apresentando resultados úteis para tomada de decisão.

### Objetivos específicos
 - Definir conceitos fundamentais relacionados a volumes em reservatórios.
 - Explicar métodos de cálculo (volumétrico, material balance, decline, probabilístico).
 - Descrever parâmetros essenciais do método volumétrico e suas fontes de incerteza.
 - Demonstrar integração de dados (mapas de espessura, Net‑to‑Gross, phi, Sw, Bo, Bg).

 ## 4.2 Prefixos e unidades (resumo)
| Prefixo | Símbolo | Fator |
|---|---:|---:|
| Kilo | k | 10^3 |
| Mega | M | 10^6 |
| Giga | G | 10^9 |
| Milli | m | 10^-3 |
| Micro | µ | 10^-6 |

> Nota: escolha unidades consistentes (SI ou campo — acres/ft/bbl). Ao usar fórmulas práticas, aplique os fatores de conversão corretos.

 ## 4.3 Introdução
O método volumétrico estima o volume de fluido originalmente existente no reservatório a partir de propriedades petrofísicas e geométricas: área, espessura neta, porosidade, saturação, e fatores de volume de formação. É a primeira estimativa após descoberta e serve de base para cálculos de reservas.

 ## 4.4 Definições essenciais
 - $V_r$: volume de rocha do reservatório (m³ ou ft³);
 - $\phi$: porosidade (fração);
 - $S_w$: saturação de água (fração); $S_o=1-S_w$ saturação de óleo;
 - $B_o, B_g$: fatores de volume de formação (reservatório → superfície);
 - $N$: número de barris padrão (STB) ou volume de gás em condições padrão.

 ## 4.5 Métodos de cálculo de volumes originalmente existentes
 - Método volumétrico (petrofísico/geométrico).
 - Material balance (balanço de material) — requer dados de produção e pressão.
 - Métodos empíricos e baseados em declínio — para reservas quando há produção.
 - Abordagens probabilísticas (Monte Carlo) — para quantificar incerteza.

 ## 4.6 Método volumétrico
 ### 4.6.1 Forma geral (reservoir conditions)
O volume de hidrocarboneto no reservatório (volume de fluido em reservatório):
$$
V_{fluid,res} = V_r\,\phi\,(1-S_w)
$$

Para converter para unidades de superfície usa‑se o fator de volume de formação $B$:
$$
N_{surface} = \frac{V_{fluid,res}}{B}
$$

### 4.6.2 Fórmulas práticas (exemplos)
- OOIP (stock tank barrels, usando unidades campo):
$$
OOIP = \frac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}
$$
onde $A$ em acres, $h$ em ft, $\phi$ fração, $B_o$ em bbl/STB.

- OGIP (scf ou Sm^3 dependendo da convenção):
$$
OGIP = \frac{43560\,A\,h\,\phi\,(1-S_w)}{B_g}
$$

> Observação: ao usar SI, converta $A$ (m²), $h$ (m) e fatores de conversão adequados.

### 4.6.3 Estimativa de volume recuperável (reservas)
Reservas (recuperáveis) podem ser expressas como função das condições iniciais e finais:

Para gás (exemplo conceitual):
$$
N_R = V_r\,\phi\,(1-S_{w_i})\left(\frac{1}{B_{g_i}} - \frac{1}{B_{g_a}}\right)
$$

Para óleo (contando saturações iniciais e residuais):
$$
N_R = V_r\,\phi\,(1-S_{w_i})\left(\frac{S_{o_i}}{B_{o_i}} - \frac{S_{o_r}}{B_{o_r}}\right)
$$

Onde índices $i$ e $a$ referem‑se às condições iniciais e de abandono; $S_{o_r}$ e $B_{o_r}$ são saturação de óleo residual e fator de volume no estado residual.

### 4.6.4 Reserva por fator de recuperação
Reservas também podem ser estimadas por:
$$
N_R = N \times F_R
$$
onde $N$ é o volume originalmente em lugar e $F_R$ o fator de recuperação (fração).

 ## 4.7 Integração de dados e incertezas
Passos práticos:
 - QA/QC das fontes: mapas de batimetria, logs, cores, testes de poço, análises PVT.
 - Construir mapas de Net‑to‑Gross, porosidade média, Sw média por setor.
 - Calcular sensibilidade dos parâmetros-chave (A, h, φ, Sw, Bo) — análise P10/P50/P90.
 - Usar Monte Carlo para propagar incertezas e gerar distribuições de OOIP/OGIP e reservas.

Principais fontes de incerteza: interpretação de limites (cut‑offs), heterogeneidade vertical e lateral, erros de core/log, variabilidade PVT.

 ## 4.8 Consolidação da aula — Exercícios
1) Dado: Área = 200 acres; h_net = 30 ft; φ = 0.18; Swi = 0.25; Bo = 1.2 bbl/STB. Calcule OOIP (use fórmula prática).
2) Faça uma análise de sensibilidade variando φ entre 0.15–0.22 e interprete o impacto no OOIP.
3) Explique como Net‑to‑Gross e cut‑offs alteram a estimativa volumétrica.

 ## 4.9 Tarefas
1) Reunir os dados petrofísicos e montar uma planilha de cálculo volumétrico para um caso hipotético.
2) Rodar uma simulação Monte Carlo simples (50–100 iterações) variando φ, Sw e Bo e apresentar P10/P50/P90.
3) Elaborar um pequeno relatório discutindo fontes de incerteza e medidas para redução de risco.

 ## Bibliografia
1. DAKE, L. P. Engenharia de Reservatórios: fundamentos. Elsevier, 2014.
2. MCCAIN, W. D. The Properties of Petroleum Fluids. PennWell, 1990.
3. ROSA, A. J.; CARVALHO, R. D. S.; XAVIER, J. A. D. Engenharia de Reservatórios de Petróleo. Interciência, 2006.

---

## Definições importantes
- **Net‑to‑Gross (N/G):** fração da coluna que é considerada 'net pay' (contribui para produção).
- **Cut‑off:** valor mínimo de porosidade/permeabilidade/saturação usado para definir zonas produtivas.
- **Fator de recuperação (F_R):** fração do volume originalmente em lugar que se espera recuperar.
- **Área efetiva (A_eff):** área do reservatório considerada produtiva após aplicar cut‑offs e mapas de net.

## Exemplo prático — cálculo de OOIP (exercício 4.8)
Dados: Área $A=200\,$acres; $h_{net}=30\,$ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

Usando a fórmula prática:
$$
OOIP = \frac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}
$$
Substituindo os valores:
$$
OOIP = \frac{7758 \times 200 \times 30 \times 0.18 \times (1-0.25)}{1.2}
$$
Calculando passo a passo:
$$
7758\times200 = 1\,551\,600\\
1\,551\,600\times30 = 46\,548\,000\\
46\,548\,000\times0.18 = 8\,378\,640\\
8\,378\,640\times0.75 = 6\,283\,980\\
	ext{OOIP} = \dfrac{6\,283\,980}{1.2} \approx 5\,236\,650\;\text{STB}
$$
Interpretação: aproximadamente $5.24\times10^6$ STB (5,24 milhões de barris originalmente em lugar).

## Observações sobre unidades
- Fórmulas práticas usam unidades de campo (acres, ft, bbl). Para SI, converta área e espessura e aplique os fatores apropriados.
- Sempre verifique se $B_o$ e $B_g$ estão no mesmo sistema de unidades antes de dividir.

## Glossário de símbolos (cap.4)
- `A` — área (acres ou m²).
- `h` — espessura neta (ft ou m).
- `\phi` — porosidade (fração).
- `S_w` — saturação de água (fração); `S_o = 1-S_w`.
- `B_o`, `B_g` — fatores de volume de formação do óleo e do gás.
- `N`, `OGIP` — volumes originalmente em lugar (STB para óleo; scf ou Sm³ para gás).
- `F_R` — fator de recuperação (fração).

## Dicas rápidas de estudo
- Monte uma planilha com a fórmula prática e permita variação de parâmetros (sensibilidade).
- Construa mapas de A_eff e h_net para setores diferentes e compare OOIP setorial.
- Use Monte Carlo para obter P10/P50/P90 e comunicar risco na estimativa.

---

Muito obrigado(a)!
