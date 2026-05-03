# Resumo por Capítulo — Engenharia de Reservatórios I (VERSÃO ULTRA‑DETALHADA)

Este ficheiro contém uma compilação exaustiva de fórmulas, definições, derivações e exemplos numéricos para os capítulos 1–5. Use como referência técnica aprofundada durante a preparação.

Índice
- Capítulo 1 — Sistema petrolífero e conceitos fundamentais
- Capítulo 2 — Propriedades dos fluidos (PVT): equações, correlações e cálculos
- Capítulo 3 — Propriedades de rochas: porosidade, permeabilidade, capilaridade, testes
- Capítulo 4 — Cálculo volumétrico (OOIP / OGIP): fórmulas de campo e SI, sensibilidade, Monte Carlo
- Capítulo 5 — Equação de Balanço de Materiais (EBM): formulação, linearização, p/z e exemplos
- Anexos: constantes, fatores de conversão, valores típicos, checklist de passos práticos

---

**Observação sobre unidades**
- Indique sempre o sistema: CAMPO (acres, ft, bbl, scf, psi) ou SI (m, m³, Pa). Mantenha consistência.
- Fatores de conversão essenciais estão no Anexo.

---

## Capítulo 1 — Sistema petrolífero e conceitos fundamentais

1. Definições essenciais
- Sistema petrolífero: rocha geradora + rocha selante + armadilha + migração + sincronismo. 
- Sistema de produção: conjunto de poços, tubulações, elevação artificial, separadores, tratamento e escoamento.

2. Relações e equações úteis
- Equilíbrio hidrostático (coluna vertical):
$$p(Z)=p_{ref}+\int_{Z_{ref}}^{Z}\rho(z') g\,dz'\approx p_{ref}+\rho g (Z_{ref}-Z)$$
(usar densidade local em cada camada quando heterogênea)

- Soma das saturações (para mistura trifásica):
$$S_w+S_o+S_g=1$$

3. Notas interpretativas
- Identificação do tipo de reservatório (oil‑drive, gas‑cap, water‑drive, solution gas drive) depende de presença de gas cap, aquífero e relação GOR/Rs.

---

## Capítulo 2 — Propriedades dos fluidos (PVT)

2.1. Grandezas fundamentais
- Equação dos gases (mol):
$$pV=nRT$$
- Fator de compressibilidade (Z):
$$Z=\dfrac{pV}{nRT}$$

2.2. Fatores de volume e razões
- Fator de volume de formação do óleo (óleo: reservatório → superfície):
$$B_o=\dfrac{V_{res\_oil}}{V_{surf\_oil}}\quad(\text{m}^3/\text{m}^3\;\text{ou bbl/STB})$$
- Relação densidade ↔ B_o: massa invariável entre estados
$$\rho_{res} = \dfrac{m}{V_{res}},\qquad \rho_{surf}=\dfrac{m}{V_{surf}}\Rightarrow B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{\rho_{surf}}{\rho_{res}}$$

- Razão gás/óleo dissolvido:
$$R_s=\dfrac{\text{vol. gás liberado (condições padrão)}}{\text{vol. óleo (superfície)}}\quad(\text{scf/STB ou m}^3/\text{m}^3)$$

2.3. Compressibilidade de fluidos
- Compressibilidade do óleo (adimensional, psi⁻1 ou Pa⁻1):
$$c_o = -\dfrac{1}{V_o}\dfrac{\mathrm{d}V_o}{\mathrm{d}p}=\dfrac{\mathrm{d}(\ln V_o)}{\mathrm{d}p}$$
- Compressibilidade do gás (aprox.):
$$c_g \approx \dfrac{1}{p}\left(1-\dfrac{\partial\ln Z}{\partial\ln p}\right)$$
(obter Z(p,T) de charts ou EoS)

2.4. Equações de estado cúbicas (uso em PVT)
- Definições gerais (PR e SRK usadas com frequência):
  - Definir constantes críticas de cada componente: $T_c, p_c, \omega$ (fator acêntrico).

- Peng‑Robinson (PR):
  - Parâmetros puros:
  $$a = 0.45724\dfrac{R^2 T_c^2}{p_c},\qquad b = 0.07780\dfrac{R T_c}{p_c}$$
  - Fator de temperatura:
  $$\alpha(T)=\left[1+\kappa (1-\sqrt{T_r})\right]^2,\quad T_r=\dfrac{T}{T_c}$$
  com
  $$\kappa = 0.37464 + 1.54226\omega - 0.26992\omega^2.$$
  - EoS:
  $$p=\dfrac{RT}{V-b}-\dfrac{a\alpha(T)}{V(V+b)+b(V-b)}$$

- Soave‑Redlich‑Kwong (SRK):
  - Parâmetros:
  $$a = 0.42748\dfrac{R^2T_c^2}{p_c},\qquad b=0.08664\dfrac{RT_c}{p_c}$$
  - EoS (forma):
  $$p=\dfrac{RT}{V-b}-\dfrac{a\alpha(T)}{V(V+b)}$$
  - Kappa (SRK): parâmetro dependente de $\omega$ (ver formulação SRK).

- Mistura (regra de mistura van der Waals tipo):
  $$a_{mix}=\sum_i\sum_j x_i x_j \sqrt{a_i a_j}(1-k_{ij}),\qquad b_{mix}=\sum_i x_i b_i$$
  onde $k_{ij}$ são parâmetros de interação binária.

- Redução a polinomial em Z (cúbica): em geral obtem‑se um polinómio cúbico em $Z$ (derivado do EoS multiplicado por $V$ e normalizado) do tipo:
  $$Z^3 + c_2 Z^2 + c_1 Z + c_0 = 0$$
  com coeficientes que dependem de $A$ e $B$:
  $$A=\dfrac{a p}{(R T)^2},\qquad B=\dfrac{b p}{R T}$$
  e um polinómio padrão (usado tanto para PR como SRK após definição apropriada de $A,B$):
  $$Z^3-(1-B)Z^2+(A-3B^2-2B)Z-(AB-B^2-B^3)=0$$
  (resolver numericamente para raízes reais; raízes correspondem a fases gasosa/líquida onde aplicável).

2.5. Cálculo de fatores de volume com Z
- Formação volume factor do gás (por molar/molar base):
  $$B_g = \dfrac{Z R T}{p}\cdot\dfrac{V_{ref\_units}}{n_{ref}}$$
  (usar forma prática/constantes de conversão ao trabalhar em scf/ft³ ou SI).

2.6. Correlações empíricas e conversões úteis
- Conversões:
  $$1\,\text{scf}=0.0283168\,\text{m}^3,\quad1\,\text{STB}=0.1589873\,\text{m}^3$$
- API gravity (relativa à água a 60°F):
  $$API=\dfrac{141.5}{SG_{60°F}} -131.5,\quad SG=\dfrac{\rho_{oil}}{\rho_{water}}$$

2.7. Exemplo prático PVT (completo)
- Dados: $V_{res}=1.20\,$bbl; $V_{surf}=1.00\,$STB; $R_s=400\,$scf/STB.
  1) $B_o=1.20/1.00=1.20\,$bbl/STB.
  2) $R_s(\text{SI})=400\times0.0283168/0.1589873\approx71.3\,\text{m}^3/\text{m}^3$.
  3) Densidade de reservatório: $\rho_{res}=\rho_{surf}/B_o$.

---

## Capítulo 3 — Propriedades das rochas (detalhado)

3.1. Porosidade (definições e métodos)
- Porosidade total: $\phi=V_p/V_t$.
- Métodos medição: gravimétricos (pesagem seca/saturada), porosimetria de mercúrio, NMR, micro‑CT.
- Porosidade efetiva (conectada) e irreducível (connate water) — distinguir para flow modelling.

3.2. Densidade de rocha saturada (mixing law)
$$\rho_b = (1-\phi)\rho_s + \phi (S_w \rho_w + S_o \rho_o + S_g \rho_g)$$
onde $\rho_s$ densidade da matriz.

3.3. Permeabilidade e Lei de Darcy
- Forma integral (unidimensional):
$$q = -\dfrac{k A}{\mu}\dfrac{\Delta p}{L}$$
- Para fluxo radial permanente para poço produtor (campo/ft):
$$q=\dfrac{2\pi k h (p_e-p_{wf})}{\mu \ln(r_e/r_w)}$$
(usar conversões quando q em STB/d, µ em cP, k em mD — ver fórmulas de campo no anexo)

3.4. Equação de difusividade (transiente, ligeiramente compressível)
- Forma geral:
$$\dfrac{\partial p}{\partial t}=\dfrac{k}{\mu S} \nabla^2 p$$
onde $S$ (coeficiente de armazenamento) geralmente
$$S=\phi c_f + (1-\phi)c_s$$
com $c_f$ compressibilidade do fluido e $c_s$ compressibilidade da matriz sólida.

3.5. Solução transiente radial (analítica aproximada — semilog)
- Para regime semilog (pseudosteady), pressão medida no poço varia com tempo t:
$$p(r_w,t)=p_i - \dfrac{q B \mu}{4\pi k h}\left[\ln\left(\dfrac{4 k t}{\phi \mu c_t r_w^2}\right)-0.80907\right]$$
- Em base‑10 logs (análise semilog): a declividade $m$ (psi por ciclo log10) é
$$m=\dfrac{2.303\,q B \mu}{4\pi k h} = \dfrac{0.183 q B \mu}{k h}$$
  e, isolando $k$ (unidades de campo com $q$ em STB/d, $\mu$ cP, $h$ ft, $m$ psi/log10):
$$k(\text{mD}) = \dfrac{162.6\,q\,B\,\mu}{h\,m}$$
(162.6 é constante empírica para conversões entre unidades; verificar convenções de unidades)

3.6. Função de Leverett e pressão capilar
- Tensão interfacial e rádio capilar simplificado (tubo):
$$P_c=\dfrac{2\sigma \cos\theta}{r}$$
- Função J de Leverett:
$$J(S_w)=\dfrac{P_c(S_w)\sqrt{k/\phi}}{\sigma\cos\theta}$$
(usar J(S) para escalonar curvas Pc entre rochas com diferentes k e φ)

3.7. Permeabilidade relativa & modelos
- Modelo de Corey (exemplo):
$$S_{we}=\dfrac{S_w-S_{wr}}{1-S_{or}-S_{wr}}$$
$$k_{rw}=k_{rw0} S_{we}^{n_w},\quad k_{ro}=k_{ro0}(1-S_{we})^{n_o}$$
- Parâmetros típicos: $n_w, n_o$ entre 2–4 dependendo de rocha/molhabilidade.

3.8. Resistividade e Archie
- Equação de Archie:
$$R_t = a R_w \phi^{-m} S_w^{-n}$$
- Parâmetros empíricos: $a\approx1$, $m\approx1.8-2.2$, $n\approx2$ (variam com litologia)

---

## Capítulo 4 — Cálculo volumétrico (OOIP / OGIP) — detalhe completo

4.1. Fórmula fundamental (reservoir → superfície)
- Volume de fluido em reservatório (m³):
$$V_{fluid,res}=V_r\,\phi\,(1-S_w)$$
- Volume de superfície:
$$N_{surface}=\dfrac{V_{fluid,res}}{B}\quad(\text{B = fator de volume de formação})$$

4.2. Fórmulas práticas de campo
- OOIP (barris stock‑tank):
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$
  - Derivação do factor 7758:
    - 1 acre = 43,560 ft²; 1 ft³ = 0.178107... bbl? (usar conversões exatas). A relação completa é: 43560 ft² × 1 ft = 43560 ft³ por acre·ft; 1 bbl = 5.614583 ft³; 43560/5.614583 ≈ 7758 bbl/acre·ft.

- OGIP (scf):
$$OGIP=\dfrac{43560\,A\,h\,\phi\,(1-S_w)}{B_g}$$
(43560 = ft³/acre coeficient)

4.3. Sensibilidade analítica (derivadas parciais)
- Sensibilidade de OOIP a φ:
$$\dfrac{\partial OOIP}{\partial\phi}=\dfrac{7758 A h (1-S_w)}{B_o}$$
- Sensibilidade fraccional relativa: usar variáveis aleatórias e Monte Carlo para propagar incertezas.

4.4. Monte Carlo (passos práticos)
1. Definir distribuições para cada variável incerta (A,h,φ,S_w,B_o): triangular, normal truncada ou lognormal conforme justificativa.
2. Amostrar N vezes (p.ex. 10k‑100k iterações para robustez) e calcular OOIP para cada amostra.
3. Ordenar resultados e extrair percentis P10/P50/P90.
4. Reportar média, mediana (P50), intervalo de confiança e curvas CDF/PDF.

4.5. Estimativa setorial
- Dividir reservatório em setores i com A_i,h_i,φ_i,S_{w,i} e somar:
$$OOIP_{total}=\sum_i \dfrac{7758 A_i h_i \phi_i (1-S_{w,i})}{B_{o,i}}$$

---

## Capítulo 5 — Equação de Balanço de Materiais (EBM) — completo

5.1. Conceito (conservação de massa)
- A EBM parte do princípio: estoque inicial = estoque atual + produção acumulada - injeções + influxo. Convertendo volumes e considerando compressibilidade resulta em equações relacionando variação de pressão com quantidades produzidas/injetadas.

5.2. Forma linearizada (Havlena & Odeh, 1963)
- Expressão usada em análise prática:
$$F = N E_o + m E_g + (1+m) E_{f,w} + W_e$$
onde:
- $F$ termo conhecido (construído a partir de produção/injeção e PVT);
- $N$ estoque original de óleo (OOIP);
- $m$ razão gas‑cap/óleo (adimensional);
- $E_o,E_g,E_{f,w}$ termos calculáveis a partir de PVT/pressão;
- $W_e$ termo de influxo do aquífero.

5.3. Definições práticas (forma operacional)
- Termos (formas comumente usadas em regressão):
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
$$E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$$
$$E_{f,w}=B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$$
- Lado conhecido $F$ (exemplo):
$$F = N_p B_o + G_p - R_s B_g + W_p B_w - W_{inj} B_w - G_{inj} B_{g,inj}$$
(ajustar sinais e convenções conforme o conjunto de dados — ver notas do curso)

5.4. Procedimento prático
1. Organizar série temporal: p(t), N_p(t), G_p(t), volumes injetados W_{inj},G_{inj}.
2. Calcular $B_o(p),B_g(p),R_s(p)$ a partir de PVT ou correlações.
3. Calcular colunas $E_o,E_g,E_{f,w}$ para cada instante.
4. Calcular $F$ para cada instante.
5. Executar regressão linear múltipla: ajustar $F$ por combinação linear dos termos para obter $N$ e $m$ (coeficientes de regressão) e estimar $W_e$.

5.5. Método p/z (para gás)
- Plot de $p/z$ vs $G_p$: em reservatórios gas‑dominados volumétricos sem influxo, a extrapolação linear pode fornecer OGIP. Interpretação: declive e intercepto do plot relacionam OGIP e condições iniciais; trate com cuidado correções de temperatura e compressibilidade.

5.6. Exemplo simplificado (numérico)
- Construir tabela com p, N_p, G_p, B_o(p),B_g(p),R_s(p), calcular $E$'s e ajustar. (ver tarefas do capítulo 5 para exemplo completo do curso).

---

## Anexos — constantes, fatores de conversão e valores típicos

Constantes importantes:
- $R_{universal}=8.314462618\;\text{J/(mol·K)}$ (usar unidades coerentes)
- $g=9.80665\;\text{m/s}^2$

Conversões úteis:
- $1\,\text{acre}=43560\,\text{ft}^2$
- $1\,\text{acre·ft}=43560\,\text{ft}^3$
- $1\,\text{bbl}=0.1589873\,\text{m}^3$
- $1\,\text{scf}=0.0283168\,\text{m}^3$
- $1\,\text{D}=9.869233\times10^{-13}\,\text{m}^2$
- $1\,\text{psi}=6894.757\,\text{Pa}$

Valores típicos (ordem de grandeza)
- Porosidade: 5%–30% para rochas reservatório; médias úteis 10%–25%.
- Permeabilidade: mD–D (argiloso <1 mD, arenito bom 100–1000 mD, carbonatos variam muito).
- Exponentes de Archie: $m\approx1.8-2.2$, $n\approx2$.

Checklist prático para cada capítulo (sintético)
- Cap.1: listar elementos do sistema petrolífero; identificar tipo de armadilha e presença de gas‑cap/aqüífero.
- Cap.2: ter curvas B_o(p), R_s(p), µ_o(p) e tabela PVT; conhecer EoS e quando aplicá‑las.
- Cap.3: consolidar porosidade/permeabilidade por core e logs; obter curvas Pc(S) e kr(S).
- Cap.4: montar planilha volumétrica setorial; rodar sensibilidade e Monte Carlo.
- Cap.5: organizar séries de produção; calcular colunas E; aplicar regressão e interpretar resultados.

---

FIM — ficheiro gerado como versão ULTRA‑DETALHADA. Se desejar, posso:
- (A) sobrepor `resumo_capitulos.md` com esta versão;
- (B) gerar PDF/LaTeX desta versão; ou
- (C) extrair cartões Anki (Q/A) automaticamente a partir das definições e fórmulas.

## Exercícios resolvidos (seleção representativa)

Esta secção apresenta soluções passo‑a‑passo para exercícios-chave dos capítulos 1–5. Use estes exemplos como modelo para resolver problemas semelhantes.

### Capítulo 1 — Verdadeiro/Falso (respostas e justificativas breves)
1) V — Armadilha geológica (structural/estratigráfica) impede migração e acumula hidrocarbonetos.
2) F — Rocha geradora é rica em matéria orgânica (não baixa).
3) F — Rocha selante tem **baixa** permeabilidade e impede fluxo.
4) V — Migração ocorre por meios porosos e fraturados, favorável a caminhos permeáveis.
5) F — Sincronismo é relevante: geração, migração e armadilhamento devem coincidir temporalmente.
6) V — Catagênese = craqueamento térmico do querogénio em hidrocarbonetos.
7) V — Sistema de produção inclui coleta, elevação e separação até a superfície.
8) V — Em gas‑cap drive o gás livre expande e ajuda a manter pressão.
9) F — Porosidade e permeabilidade são propriedades distintas (volume de poros vs facilidade de fluxo).
10) V — $B_o$ relaciona volumes em reservatório e superfície (reservoir → surface).

### Capítulo 2 — PVT: exemplo resolvido (cálculo de $B_o$ e conversão de $R_s$)
Enunciado: Num ensaio PVT por 1 STB de óleo obteve‑se $V_{res}=1.20\,$bbl e $V_{surf}=1.00\,$STB; gás libertado $R_s=400\,$scf/STB.

a) Cálculo de $B_o$:
$$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ 

b) Conversão de $R_s$ para m³/m³:
1 scf = 0.0283168 m³; 1 STB = 0.1589873 m³.
$$R_s(\text{m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx\dfrac{11.32672}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3.$$ 

c) Interpretação breve: $B_o>1$ indica que o volume no reservatório é maior que o volume final de superfície por unidade (efeitos de compressibilidade e gás dissolvido). $R_s$ alto implica presença significativa de gás dissolvido — ao atingir o ponto de bolha o gás liberta‑se, alterando mobilidade.

### Capítulo 3 — Rochas: exercícios resolvidos (porosidade por massa e método de Arquímedes)

**Exemplo (Exercício 1)** — Dados: $m_{sat}=130\,$g; $m_{dry}=105\,$g; $\rho_o=0.84\,$g/cm^3; $V_t=180\,$cm^3.

1) Volume de fluido nos poros:
$$V_f=\dfrac{m_{sat}-m_{dry}}{\rho_o}=\dfrac{130-105}{0.84}=\dfrac{25}{0.84}\approx29.7619\;\text{cm}^3.$$ 

2) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{29.7619}{180}\approx0.16534\approx16.53\%.$$ 

**Exemplo (Exercício 5 — método de Arquímedes)** — Dados: $m_{dry}=330\,$g; $m_{sat}=360\,$g; $m_{ap\_agua}=225\,$g; $\rho_{agua}=1\,$g/cm^3.

1) Volume total da amostra via empuxo (diferença entre peso em ar e peso aparente em água):
$$V_t=\dfrac{m_{sat}-m_{ap\_agua}}{\rho_{agua}}=\dfrac{360-225}{1}=135\;\text{cm}^3.$$ 

2) Volume poroso (volume de fluido nos poros):
$$V_p=m_{sat}-m_{dry}=360-330=30\;\text{cm}^3.$$ 

3) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{30}{135}\approx0.22222\approx22.22\%. $$

Observação: nos relatórios, apresente as unidades, arredondamento e possíveis fontes de erro experimental.

### Capítulo 4 — Cálculo volumétrico: exemplo resolvido (OOIP)

Dados (exercício 4.8): $A=200\,$acres; $h_{net}=30\,$ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

Fórmula prática:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}.$$ 

Substituindo os valores e calculando passo a passo:
\begin{align*}
7758\times200&=1\,551\,600\\
1\,551\,600\times30&=46\,548\,000\\
46\,548\,000\times0.18&=8\,378\,640\\
8\,378\,640\times0.75&=6\,283\,980\\
OOIP&=\dfrac{6\,283\,980}{1.2}\approx5\,236\,650\;\text{STB}.
\end{align*}

Interpretação: aproximadamente 5.24×10^6 STB originalmente em lugar.

### Capítulo 5 — EBM: exemplo prático (cálculo de $E_o$ e montagem de colunas)

Dados ilustrativos (simplificados): $B_{o,i}=1.10$, $B_o=1.15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0.005$ (unidades consistentes com a formulação do curso).

Cálculo do termo $E_o$ (Havlena & Odeh):
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
Substituindo:
$$E_o = 1.15 - 1.10 + (200-180)\times0.005 = 0.05 + 20\times0.005 = 0.05 + 0.10 = 0.15.$$ 

Notas práticas para montar a tabela de análise EBM:
- Para cada instante (data) calcule: $p$, $N_p$, $G_p$, $B_o(p)$, $B_g(p)$, $R_s(p)$.
- Calcule colunas $E_o,E_g,E_{f,w}$ por fórmulas definidas; calcule $F$ (lado conhecido) usando volumes produzidos/injetados convertidos para unidades compatíveis;
- Execute regressão linear múltipla de $F$ versus colunas $E_o,E_g,E_{f,w}$ para obter estimativas de $N$ (coeficiente associado a $E_o$) e $m$ (coeficiente associado a $E_g$).

Exemplo de output parcial (apenas ilustrativo):
| t | p (psi) | N_p (STB) | G_p (scf) | B_o | B_g | R_s | E_o | E_g | E_{f,w} | F |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t_1 | 3000 | 100000 | 50000 | 1.10 | 0.0050 | 200 | 0.00 | 0.00 | 0.00 | F_1 |
| t_2 | 2900 | 120000 | 60000 | 1.12 | 0.0051 | 195 | 0.02 | 0.01 | 0.002 | F_2 |

Onde $F_i$ é montado conforme convensão adotada no curso; preste atenção às unidades (STB vs scf) e às conversões necessárias.

---

Se desejar, posso expandir esta secção com soluções de todos os exercícios presentes em `exercícios_transcription.md` (isto exigirá mais tempo e poderei criar um ficheiro separado `exercicios_resolvidos.md`).

Arquivo criado automaticamente pelo assistente.