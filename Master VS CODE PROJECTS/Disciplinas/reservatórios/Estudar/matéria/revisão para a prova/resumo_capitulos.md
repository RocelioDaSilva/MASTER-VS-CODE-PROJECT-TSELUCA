
# Resumo por Capítulo — Engenharia de Reservatórios I (Versão EXTREMAMENTE Detalhada)

Este documento contém um resumo aprofundado dos capítulos 1–5, com fórmulas, definições, unidades, notas de interpretação e exemplos numéricos passo‑a‑passo. Use como referência de estudo e para gerar fichas de revisão.

Índice
- Capítulo 1 — Conceitos e sistema petrolífero
- Capítulo 2 — Propriedades dos fluidos (PVT): teorias, fórmulas e correlações
- Capítulo 3 — Propriedades das rochas: porosidade, permeabilidade, capilaridade e equações aplicadas
- Capítulo 4 — Cálculo volumétrico (OOIP / OGIP): fórmulas de campo e SI, sensibilidade e Monte Carlo
- Capítulo 5 — Equação de Balanço de Materiais (EBM): formulação, linearização e exemplos
- Anexos: constantes, fatores de conversão, lista de fórmulas essenciais

---

**Nota de unidades:** Sempre indique o sistema: UNIDADES DE CAMPO (acres, ft, bbl, scf) ou SI (m, m³, Pa). Muitos fatores práticos (ex.: 7758) convertem acres·ft → bbl.

---

## Capítulo 1 — Conceitos e sistema petrolífero

1.1 Principais definições
- Sistema petrolífero: conjunto de elementos necessários para geração, migração, armadilhamento e acumulação de hidrocarbonetos.
- Sistema de produção: instalações e equipamentos para recuperação, elevação e tratamento dos fluidos do reservatório até a superfície.

1.2 Equações e relações fundamentais (úteis para este capítulo)
- Equilíbrio hidrostático (coluna incompressível ideal):
$$p(z)=p_{ref}+\rho g (Z_{ref}-Z)$$
onde $p$ em Pa (ou psi), $\rho$ densidade (kg/m³), $g$ = 9.80665 m/s², $Z$ profundidade.
- Soma de saturações (misto trifásico):
$$S_w + S_o + S_g = 1$$
onde cada $S_\bullet$ é fração volumétrica adimensional.

1.3 Conceitos qualitativos importantes
- Armadilha (structural/estratigráfica/fraturada), rocha geradora/selante, migração; sincronismo e janela térmica (catagênese) — sem equações mas essenciais para interpretação geológica.

---

## Capítulo 2 — Propriedades dos fluidos (PVT)

2.1 Variáveis termodinâmicas fundamentais
- Equação dos gases ideais (mol):
$$pV=nRT$$
onde $p$ (Pa), $V$ (m³), $n$ (mol), $R$ (8.314462618 J/(mol·K)), $T$ (K).
- Fator de compressibilidade (Z):
$$Z=\dfrac{pV}{nRT}=\dfrac{p\,\overline{v}}{RT}$$
Z corrige o comportamento real do gás.

2.2 Definições PVT essenciais
- Fator de volume de formação do óleo ($B_o$):
$$B_o=\dfrac{V_{res\_oil}}{V_{surf\_oil}}\quad(\text{unidades: m}^3/\text{m}^3\;\text{ou bbl/STB})$$
- Fator de volume do gás ($B_g$): volume de gás no reservatório por unidade de gás padrão (ft³/SCF ou m³/Sm³):
$$B_g=\dfrac{V_{res\_gas}}{V_{std\_gas}}$$
- Razão gás/óleo dissolvido ($R_s$): normalmente em scf/STB (campo) ou m³/m³ (SI):
$$R_s=\dfrac{\text{volume de gás dissolvido no óleo (std)}}{\text{volume de óleo (superfície)}}$$

2.3 Compressibilidades e variações com pressão
- Compressibilidade do óleo (bo):
$$c_o = -\dfrac{1}{V_o}\dfrac{\mathrm{d}V_o}{\mathrm{d}p} = \dfrac{\mathrm{d}(\ln V_o)}{\mathrm{d}p}$$
- Compressibilidade do gás (aproximação):
$$c_g \approx \dfrac{1}{p} \left(1 - \dfrac{\mathrm{d}\ln Z}{\mathrm{d}\ln p}\right)$$
Usar tabelas/curvas Z para cálculo prático.

2.4 Correlações e estimativas empíricas (nomes e uso)
- Correlações de $B_o$, $\mu_o$, $R_s$ (Standing, Vazquez‑Beggs, Beggs & Robinson para viscosidade). Estas fornecem estimativas quando não existem ensaios PVT.

2.5 Conversões úteis (campo ↔ SI)
- $1\,\text{scf}=0.0283168\,\text{m}^3$;
- $1\,\text{STB}=0.1589873\,\text{m}^3$;
- $1\,\text{bbl}=0.1589873\,\text{m}^3$.

2.6 Exemplo prático (passo a passo)
- Dados: $V_{res}=1.20\,$bbl, $V_{surf}=1.00\,$STB, $R_s=400\,$scf/STB.
- $B_o = 1.20/1.00 = 1.20\,$bbl/STB.
- $R_s$ em SI:
$$R_s(\text{m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3$$

---

## Capítulo 3 — Propriedades das rochas

3.1 Porosidade e volumes
- Porosidade total:
$$\phi=\dfrac{V_p}{V_t}$$
onde $V_p$ é o volume de poros e $V_t$ o volume total.
- Porosidade a partir de massa (método gravimétrico):
$$V_p=\dfrac{m_{sat}-m_{dry}}{\rho_f},\qquad \phi=\dfrac{V_p}{V_t}$$

3.2 Densidades e densidade aparente (logs)
- Massa específica/aparente: para rocha saturada
$$\rho_b=(1-\phi)\rho_{s}+\phi(S_w\rho_w+S_o\rho_o+S_g\rho_g)$$
onde $\rho_s$ é a densidade da matriz.

3.3 Permeabilidade (Lei de Darcy)
- Forma diferencial (unidimensional):
$$q=-\dfrac{kA}{\mu}\dfrac{\mathrm{d}p}{\mathrm{d}x}$$
onde $q$ é vazão volumétrica (m³/s), $k$ permeabilidade (m²), $A$ área (m²), $\mu$ viscosidade (Pa·s).
- Fluxo radial estacionário (poço produtor, conduto linearizado):
$$q=\dfrac{2\pi k h (p_e-p_{wf})}{\mu\ln\left(\dfrac{r_e}{r_w}\right)}$$
onde $h$ é espessura produtiva, $r_e$ raio de drenagem, $r_w$ raio do poço.

3.4 Difusividade (equação do fluxo transiente)
- Para fluido ligeiramente compressível:
$$\dfrac{\partial p}{\partial t}=\dfrac{k}{\phi\mu c_t}\nabla^2 p$$
onde $c_t$ é compressibilidade total (soma das compressibilidades relevantes).

3.5 Capilaridade e função de Leverett
- Pressão capilar (tubo capilar simplificado):
$$P_c = \dfrac{2\sigma\cos\theta}{r}$$
- Função de Leverett:
$$J(S_w)=\dfrac{P_c(S_w)\sqrt{k/\phi}}{\sigma\cos\theta}$$

3.6 Saturações e permeabilidades relativas
- $S_w+S_o+S_g=1$;
- Permeabilidade relativa: $k_{r\alpha}=f(S_\alpha)$ (curvas experimentais).

3.7 Resistividade e saturação — Equação de Archie
- Forma usual (zona limpa, rocha não condutiva):
$$R_t = a\,R_w\,\phi^{-m}\,S_w^{-n}$$
ou invertendo para saturação:
$$S_w = \left(\dfrac{a\,R_w}{R_t\,\phi^{m}}\right)^{1/n}$$
com parâmetros empíricos $a,m,n$.

3.8 Exemplos resolvidos (porosidade por massa; Arquímedes)
- Ver exemplos do capítulo 3 (por ex., $\phi\approx16{,}5\%$ e $22{,}2\%$ em exercícios práticos — seguir passos mostrados).

---

## Capítulo 4 — Integração de Dados e Cálculo Volumétrico

4.1 Forma geral (reservoir and surface)
- Volume de fluido em reservatório (m³):
$$V_{fluid,res}=V_r\,\phi\,(1-S_w)$$
- Conversão para superfície usando fator de volume $B$ (m³/m³):
$$N_{surface}=\dfrac{V_{fluid,res}}{B}$$

4.2 Fórmulas práticas (unidades de campo)
- OOIP (STB):
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$
onde $A$ em acres, $h$ em ft, $\phi$ fração, $B_o$ em bbl/STB.\
Derivação rápida do fator 7758:
1 acre = 43560 ft^2; 1 acre·ft = 43560 ft^3; 1 bbl = 5.614583 ft^3 → 43560/5.614583 \approx 7758 bbl/acre·ft.

- OGIP (SCF):
$$OGIP=\dfrac{43560\,A\,h\,\phi\,(1-S_w)}{B_g}$$
onde $B_g$ é o fator volume do gás (ft^3/SCF).

4.3 Estimativa de reservas recuperáveis
- Reservas volumétricas (por fator de recuperação $F_R$):
$$N_R = OOIP\times F_R$$
ou pontualmente (contando saturações residuais):
$$N_R = V_r\,\phi\,(1-S_{w,i})\left(\dfrac{S_{o,i}}{B_{o,i}} - \dfrac{S_{o,r}}{B_{o,r}}\right)$$

4.4 Análise de sensibilidade e incerteza
- Derivada parcial (sensibilidade de OOIP a $\phi$):
$$\dfrac{\partial OOIP}{\partial\phi}=\dfrac{7758\,A\,h\,(1-S_w)}{B_o}$$
- Monte Carlo: descreva distribuições para $A,h,\phi,S_w,B_o$ (p.ex. triangular, normal truncada, lognormal), gere N amostras e calcule percentis P10/P50/P90 da distribuição resultante de OOIP.

4.5 Boas práticas de integração
- QA/QC em dados de core, logs e PVT; uso de mapas de net pay e cut‑offs; segmentação setorial (zonas) — calcular OOIP por setor e somar.

---

## Capítulo 5 — Equação de Balanço de Materiais (EBM)

5.1 Conceito geral
- A EBM relaciona as quantidades produzidas/injetadas com a variação de estoque no reservatório; é uma equação de conservação de massa para os poros.

5.2 Forma linearizada (Havlena & Odeh)
- Variável conhecida (lado esquerdo), $F$, é construída a partir de dados de produção e injeção convertidos para volumes de superfície. A forma linearizada usada comumente é:
$$F = N\,E_o + m\,E_g + (1+m)\,E_{f,w} + W_e$$
onde:
- $E_o = B_o - B_{o,i} + (R_{s,i}-R_s)\,B_g$;
- $E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$;
- $E_{f,w} = B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$;
- $N$ é OOIP (a estimar), $m$ razão gas‑cap/óleo (a estimar), $W_e$ contribuição líquida do aquífero.

5.3 Construção prática de $F$ (exemplo simplificado)
- Exemplo (formas ilustrativas): calcular $F$ acumulado por intervalo como combinação de termos de produção $N_p B_o$, $G_p$ e correções por $R_s$, volumes injetados, etc. (ver exercícios e ficheiro cap5 para forma usada no curso).

5.4 Estimação por regressão
- Monte as colunas $F, E_o, E_g, E_{f,w}$ para vários instantes. Execute regressão linear múltipla:
$$F = \beta_1 E_o + \beta_2 E_g + \beta_3 E_{f,w} + \varepsilon$$
onde idealmente $\beta_1=N$, $\beta_2=m$, $\beta_3=(1+m)$ e $\varepsilon$ residuais (ou ajustar conforme convenção usada).

5.5 Notas sobre gás e p/z
- Para reservatórios gas‑dominados, a análise p/z (plot de $p/z$ vs $G_p$) permite estimar OGIP por extrapolação; p/z é inversamente proporcional ao volume remanescente quando as condições são adequadas. (Implementação numérica e tratamentos de retroinjeção exigem cuidados de unidades e correções).

---

## Anexos — Fórmulas essenciais e constantes

Constantes e conversões rápidas
- $1\,\text{acre}=43560\,\text{ft}^2$.
- $1\,\text{acre·ft}=43560\,\text{ft}^3\approx7758\,\text{bbl}$.
- $1\,\text{bbl}=0.1589873\,\text{m}^3$.
- $1\,\text{scf}=0.0283168\,\text{m}^3$.
- $1\,\text{D}=9.869233\times10^{-13}\,\text{m}^2$.
- $1\,\text{psi}=6894.757\,\text{Pa}$.

Lista condensada de fórmulas (referência rápida)
- Somatório das saturações: $S_w+S_o+S_g=1$.
- API gravity: $API=\dfrac{141.5}{SG}-131.5$.
- Darcy (unidimensional): $q=-\dfrac{kA}{\mu}\dfrac{\mathrm{d}p}{\mathrm{d}x}$.
- Radial steady flow to well: $q=\dfrac{2\pi k h (p_e-p_{wf})}{\mu\ln(r_e/r_w)}$.
- OOIP (campo): $OOIP=\dfrac{7758Ah\phi(1-S_w)}{B_o}$.
- OGIP (campo): $OGIP=\dfrac{43560Ah\phi(1-S_w)}{B_g}$.
- Porosidade: $\phi=V_p/V_t$.
- Compressibilidade: $c= -\dfrac{1}{V}\dfrac{\mathrm{d}V}{\mathrm{d}p}$.
- Archie: $R_t=aR_w\phi^{-m}S_w^{-n}$.
- Capilaridade (tubo): $P_c=\dfrac{2\sigma\cos\theta}{r}$.
- Leverett: $J(S_w)=\dfrac{P_c(S_w)\sqrt{k/\phi}}{\sigma\cos\theta}$.

---

## Sugestões de estudo e uso deste ficheiro
- Transforme cada subseção num cartão de revisão (Anki) — fórmulas, definições e exemplos numéricos.
- Implemente as fórmulas essenciais numa planilha (OOIP/OGIP/Monte Carlo) para treino prático.
- Para a prova: foque em interpretar o significado físico das fórmulas (o que altera OOIP, por que $B_o$ varia com pressão, como $R_s$ altera mobilidade, etc.).

---

Arquivo gerado automaticamente pelo assistente — versão detalhada criada a pedido do utilizador.