# Exercícios Resolvidos — Engenharia de Reservatórios I

Compilação de soluções passo‑a‑passo extraídas dos ficheiros em `Estudar/matéria` (cap1–cap5). Use como referência rápida para estudo; ver ficheiros de origem para enunciados completos.

---

## Capítulo 1 — Exemplo rápido (OOIP)
Dados: Área = 100 acres; $h=20\,$ft; $\phi=0.15$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

Fórmula prática:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_{wi})}{B_o}$$

Cálculo passo a passo:
\begin{align*}
7758\times100&=775\,800\\
775\,800\times20&=15\,516\,000\\
15\,516\,000\times0.15&=2\,327\,400\\
2\,327\,400\times0.75&=1\,745\,550\\
OOIP&=\dfrac{1\,745\,550}{1.2}\approx1\,454\,625\;\text{STB}
\end{align*}

Resultado: ≈1.455×10^6 STB.

---

## Capítulo 2 — PVT: cálculo de $B_o$ e conversão de $R_s$
Enunciado (exemplo): 1 STB amostrado dá $V_{res}=1.20\,$bbl, $V_{surf}=1.00\,$STB; $R_s=400\,$scf/STB.

1) $B_o$:
$$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ 

2) Conversão de $R_s$ para m^3/m^3 (opcional):
1 scf = 0.0283168 m^3; 1 STB = 0.1589873 m^3.
$$R_s(\mathrm{m}^3/\mathrm{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\mathrm{m}^3/\mathrm{m}^3.$$ 

Interpretação: $B_o>1$ indica expansão/volume maior em reservatório por unidade de superfície; $R_s$ alto = muito gás dissolvido.

---

## Capítulo 3 — Rochas: porosidade (massa e Arquímedes)

### Exemplo 1 (Exercício 1)
Dados: $m_{sat}=130\,$g; $m_{dry}=105\,$g; $\rho_o=0.84\,$g/cm^3; $V_t=180\,$cm^3.

1) Volume de fluido nos poros:
$$V_f=\dfrac{m_{sat}-m_{dry}}{\rho_o}=\dfrac{130-105}{0.84}=\dfrac{25}{0.84}\approx29.7619\;\text{cm}^3.$$ 

2) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{29.7619}{180}\approx0.16534\approx16.53\%.$$ 

### Exemplo 2 (método de Arquímedes — Exercício 5)
Dados: $m_{dry}=330\,$g; $m_{sat}=360\,$g; $m_{ap\_agua}=225\,$g; $\rho_{agua}=1\,$g/cm^3.

1) Volume total via empuxo:
$$V_t=\dfrac{m_{sat}-m_{ap\_agua}}{\rho_{agua}}=\dfrac{360-225}{1}=135\;\text{cm}^3.$$ 

2) Volume poroso:
$$V_p=m_{sat}-m_{dry}=360-330=30\;\text{cm}^3.$$ 

3) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{30}{135}\approx0.22222\approx22.22\%.$$

Observação: indicar unidades e arredondamentos no relatório final.

---

## Capítulo 4 — Cálculo volumétrico (Exercício 4.8 — OOIP)
Dados: $A=200\,$acres; $h_{net}=30\,$ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

Fórmula:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}.$$ 

Cálculo:
\begin{align*}
7758\times200&=1\,551\,600\\
1\,551\,600\times30&=46\,548\,000\\
46\,548\,000\times0.18&=8\,378\,640\\
8\,378\,640\times0.75&=6\,283\,980\\
OOIP&=\dfrac{6\,283\,980}{1.2}\approx5\,236\,650\;\text{STB}.
\end{align*}

Resultado: ≈5.24×10^6 STB.

---

## Capítulo 5 — Equação de Balanço de Materiais (Havlena & Odeh)

### Exemplo (cálculo do termo $E_o$)
Dados ilustrativos: $B_{o,i}=1.10$, $B_o=1.15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0.005$.

Fórmula:
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$

Cálculo:
$$E_o = 1.15 - 1.10 + (200-180)\times0.005 = 0.05 + 20\times0.005 = 0.05 + 0.10 = 0.15.$$ 

Uso: repita para cada data (pressão) e monte a regressão linear $F= N E_o + m E_g + (1+m)E_{f,w} + W_e$ para estimar $N$ e $m$.

---

## Observações finais
- Este ficheiro agrupa exemplos resolvidos presentes nas notas (cap1–cap5). Para exercícios completos e figuras, consulte os ficheiros originais em `Estudar/matéria`.
- Se quiser, posso:
  - adicionar soluções passo‑a‑passo para TODOS os exercícios listados nos capítulos (criando uma secção por número de exercício), ou
  - gerar um PDF/LaTeX com este compêndio.

---

*Ficheiro gerado automaticamente pelo assistente.*

---

## Soluções adicionais completas — Capítulos 1–5

A seguir estão as soluções passo‑a‑passo para as perguntas listadas nas secções de consolidação e tarefas dos Capítulos 1 a 5. Para problemas descritivos forneço uma resposta‑modelo; para exercícios numéricos apresento cálculos explícitos e resultados.

### Capítulo 1 — Respostas e justificações (Consolidação)
1) **B** — Baixa densidade e alta mobilidade.
  - Justificação: óleo leve tem menor densidade e viscosidade, o que aumenta a mobilidade relativa e facilita o escoamento.

2) **A** — Reduz a pressão do reservatório e facilita o fluxo de óleo.
  - Justificação: a presença de gás (dissolvido ou livre) altera o comportamento volumétrico e pode gerar mecanismos de drive (solution gas, gas‑cap) que afetam a pressão e a mobilidade do óleo.

3) **A** — Manutenção da pressão por influxo de água do aquífero.
  - Justificação: water drive é caracterizado pelo suporte de pressão fornecido pelo aquífero que desloca óleo para os poços.

4) **A** — A taxa de fluxo pelo reservatório.
  - Justificação: a mobilidade é proporcional a $1/\mu$; aumentos de viscosidade reduzem caudal para a mesma diferença de pressão.

5) **A** — Mantém pressão por expansão de gás acima do óleo.
  - Justificação: gas‑cap drive usa a expansão do gás livre para suportar pressão de reservatório.

6) **A** — O condensado separa‑se do gás à medida que a pressão diminui.
  - Justificação: condensado aparece quando a condição de orvalho é atingida e parte do gás condensa em fase líquida.

7) **E** — (não define).  
  - Explicação: as características A–D são diretamente associadas ao solution‑gas drive; a expressão "produção contínua de óleo" não é uma definição intrínseca do mecanismo (a produção pode declinar com a queda de pressão), portanto é a alternativa que NÃO define o mecanismo.

8) **A** — A água do aquífero desloca o óleo em direção aos poços.

9) **A** — Pressão inicial do reservatório e mobilidade do óleo.
  - Justificação: em reservatórios undersaturated a produção depende da pressão acima do ponto de bolha e da mobilidade do óleo.

10) **A** — Gás livre no topo do reservatório que ajuda a manter a pressão.

---

### Capítulo 2 — Propriedades dos fluidos (respostas‑modelo)
- O que é $B_o$ e por que é importante:
  - $B_o$ é o fator de volume de formação do óleo: $B_o=V_{res}/V_{surf}$. É usado para converter volumes no reservatório para volumes de superfície (STB) e é essencial em balanços de massa e estimativas de reservas.

- Como $R_s$ varia com pressão e significado do ponto de bolha:
  - Geralmente $R_s$ diminui com a redução de pressão; ao atingir o ponto de bolha surge gás livre e $R_s$ passa a ser o valor máximo de gás dissolvido na condição dada.

- Efeito da viscosidade do óleo na mobilidade:
  - Mobilidade dinâmica $\\lambda = k/\\mu$; viscosidade maior reduz mobilidade e diminui vazões para um mesmo gradiente de pressão.

- Quando tratar o gás como ideal vs real:
  - Use o modelo ideal quando as condições estiverem longe do crítico (pressões relativamente baixas e temperaturas altas); para pressões elevadas/temperaturas baixas use fator $Z$ (gráficos de Standing & Katz) ou equações de estado cúbicas (Peng‑Robinson, SRK).

---

### Capítulo 3 — Rochas (soluções numéricas e procedimentos)

1) (já incluído) — Porosidade por pesagem: exemplo resolvido no ficheiro acima (Exemplo 1).

2) (figuras) — Porosidade idealizada: desenhe o volume total $V_t$, identifique $V_p$ (vazios) e calcule $\phi=V_p/V_t$. Em figuras, calcule áreas/volumes preferenciais e aplique fórmula.

3) **Exercício (válvula e pressões)** — Dados: $V_1=100\,$cc; $V_2=100\,$cc; $p_1=15\,$psi; $p_2=60\,$psi; $p_f=39\,$psi. Calcular volume do grão $V_g$.

Derivação (conservação do número de moles a temperatura constante — Lei de Boyle):
$$p_1(V_1-V_g)+p_2V_2=p_f\,(V_1-V_g+V_2).$$
Resolvendo para $V_g$:
$$V_g=\dfrac{p_f(V_1+V_2)-p_1V_1-p_2V_2}{p_f-p_1}.$$ 
Substituindo valores:
$$V_g=\dfrac{39(100+100)-15\times100-60\times100}{39-15}=\dfrac{7800-1500-6000}{24}=\dfrac{300}{24}=12{,}5\;\text{cm}^3.$$

Resposta: $V_g=12{,}5\,$cc.

4) **Porosidade média (Exercício 4)** — dados: 10, 12, 11, 13, 14, 10, 17 (%).
  - Soma = 77; média = $77/7 = 11.0\%$.

5) (já incluído) — Método de Arquímedes: exemplo resolvido no ficheiro (Exemplo 2).

6) **Compressibilidade de poros (exemplo)** — Dados: $V_p=18\,$cm^3$; \Delta V_p=0{,}15\,$cm^3 para $\Delta p=900\,$psi.
$$C_f=\dfrac{\Delta V_p/V_p}{\Delta p}=\dfrac{0{,}15/18}{900}\approx9{,}26\times10^{-6}\;\text{psi}^{-1}.$$ 

---

### Capítulo 4 — Cálculo volumétrico (sensibilidade e procedimentos)

**Exercício 4.8 (já incluído)** — OOIP calculado: aproximadamente $5{,}236{,}650\,$STB para $A=200\,$acres, $h=30\,$ft, $\phi=0.18$, $S_{wi}=0.25$, $B_o=1.2$.

**Análise de sensibilidade (variação de $\phi$ de 0{,}15 a 0{,}22)** — usando a mesma fórmula prática:
- Para $\phi=0{,}15$:
$$OOIP\approx4{,}363{,}875\;\text{STB}.$$ 
- Para $\phi=0{,}22$:
$$OOIP\approx6{,}400{,}350\;\text{STB}.$$ 

Interpretação: OOIP cresce aproximadamente linearmente com $\phi$ (mesmo A,h,Swi e Bo), mostrando elevada sensibilidade à porosidade; variação relativa de $\phi$ traduz‑se diretamente numa variação proporcional do OOIP.

**Procedimento Monte Carlo (resumo prático):**
 - Escolher distribuições (ex.: normal/triangular) para $\phi$, $S_w$, $B_o$, $h$.
 - Gerar N iterações (p.ex. 1.000–10.000), calcular OOIP por iteração e recolher estatísticas P10/P50/P90.
 - Reportar média, desvios e percentis; preparar gráficos de dispersão e histogramas.

---

### Capítulo 5 — Equação de Balanço de Materiais (EBM) — passos e exemplo

**Passos para aplicar a linearização (Havlena & Odeh):**
1. Reunir por data: $p$, $N_p$, $G_p$, $W_p$ (produções), $B_o(p)$, $B_g(p)$, $R_s(p)$ a partir de PVT.
2. Calcular colunas por data: $E_o,E_g,E_{f,w}$ usando as fórmulas:
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
$$E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$$
$$E_{f,w} = B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$$
3. Montar $F$ (lado conhecido) por data (converter unidades):
$$F = N_p B_o + G_p - R_s B_g + W_p B_w - W_{inj} B_w - G_{inj} B_{g,inj}.$$ 
4. Fazer regressão linear múltipla: $F = N E_o + m E_g + (1+m) E_{f,w} + W_e$ para estimar $N$ (estoque original) e $m$ (razão gas‑cap/óleo). Use regressão com todas as linhas de dados (mínimo 3–4 pontos; quanto mais, melhor).

**Exemplo (termo $E_o$ já calculado no ficheiro):**
 - Valores ilustrativos: $B_{o,i}=1{,}10$, $B_o=1{,}15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0{,}005$.
 - Calculámos:
$$E_o=1{,}15-1{,}10+(200-180)\times0{,}005=0{,}15.$$ 

Para obter $N$ proceda assim (resumo): construa a tabela com colunas $F,E_o,E_g,E_{f,w}$ e execute uma regressão linear múltipla (p.ex. em Excel: Análise de Regressão → regressão múltipla; em Python: numpy.linalg.lstsq ou statsmodels.OLS). O coeficiente associado a $E_o$ será a estimativa de $N$ (ou, dependendo da forma, a sua relação direta — ver convenção de montagem das colunas).

---

Se desejar, posso agora:
- (A) inserir soluções detalhadas (passo‑a‑passo) para cada exercício numerado nos ficheiros originais (por exemplo, 1–N de `exercícios_transcription.md`), incluindo os cálculos intermédios e tabelas; ou
- (B) gerar um PDF/LaTeX do compêndio completo `exercicios_resolvidos.md` com formatação académica.

Ficarei aguardando a sua preferência para a etapa seguinte.
