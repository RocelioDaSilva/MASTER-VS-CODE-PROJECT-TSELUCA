# Resumo por CapÃ­tulo â€” Engenharia de ReservatÃ³rios I (VERSÃƒO ULTRAâ€‘DETALHADA)

Este ficheiro contÃ©m uma compilaÃ§Ã£o exaustiva de fÃ³rmulas, definiÃ§Ãµes, derivacÌ§oÌƒes e exemplos numeÌricos para os capÃ­tulos 1â€“5. Use como referÃªncia tÃ©cnica aprofundada durante a preparaÃ§Ã£o.

Ãndice
- CapÃ­tulo 1 â€” Sistema petrolÃ­fero e conceitos fundamentais
- CapÃ­tulo 2 â€” Propriedades dos fluidos (PVT): equaÃ§Ãµes, correlaÃ§Ãµes e cÃ¡lculos
- CapÃ­tulo 3 â€” Propriedades de rochas: porosidade, permeabilidade, capilaridade, testes
- CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico (OOIP / OGIP): fÃ³rmulas de campo e SI, sensibilidade, Monte Carlo
- CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM): formulaÃ§Ã£o, linearizaÃ§Ã£o, p/z e exemplos
- Anexos: constantes, fatores de conversÃ£o, valores tÃ­picos, checklist de passos prÃ¡ticos

---

**ObservaÃ§Ã£o sobre unidades**
- Indique sempre o sistema: CAMPO (acres, ft, bbl, scf, psi) ou SI (m, mÂ³, Pa). Mantenha consistÃªncia.
- Fatores de conversÃ£o essenciais estÃ£o no Anexo.

---

## CapÃ­tulo 1 â€” Sistema petrolÃ­fero e conceitos fundamentais

1. DefiniÃ§Ãµes essenciais
- Sistema petrolÃ­fero: rocha geradora + rocha selante + armadilha + migraÃ§Ã£o + sincronismo. 
- Sistema de produÃ§Ã£o: conjunto de poÃ§os, tubulaÃ§Ãµes, elevaÃ§Ã£o artificial, separadores, tratamento e escoamento.

2. RelaÃ§Ãµes e equaÃ§Ãµes Ãºteis
- EquilÃ­brio hidrostÃ¡tico (coluna vertical):
$$p(Z)=p_{ref}+\int_{Z_{ref}}^{Z}\rho(z') g\,dz'\approx p_{ref}+\rho g (Z_{ref}-Z)$$
(usar densidade local em cada camada quando heterogÃªnea)

- Soma das saturaÃ§Ãµes (para mistura trifÃ¡sica):
$$S_w+S_o+S_g=1$$

3. Notas interpretativas
- IdentificaÃ§Ã£o do tipo de reservatÃ³rio (oilâ€‘drive, gasâ€‘cap, waterâ€‘drive, solution gas drive) depende de presenÃ§a de gas cap, aquÃ­fero e relaÃ§Ã£o GOR/Rs.

---

## CapÃ­tulo 2 â€” Propriedades dos fluidos (PVT)

2.1. Grandezas fundamentais
- EquaÃ§Ã£o dos gases (mol):
$$pV=nRT$$
- Fator de compressibilidade (Z):
$$Z=\dfrac{pV}{nRT}$$

2.2. Fatores de volume e razÃµes
- Fator de volume de formaÃ§Ã£o do Ã³leo (Ã³leo: reservatÃ³rio â†’ superfÃ­cie):
$$B_o=\dfrac{V_{res\_oil}}{V_{surf\_oil}}\quad(\text{m}^3/\text{m}^3\;\text{ou bbl/STB})$$
- RelaÃ§Ã£o densidade â†” B_o: massa invariÃ¡vel entre estados
$$\rho_{res} = \dfrac{m}{V_{res}},\qquad \rho_{surf}=\dfrac{m}{V_{surf}}\Rightarrow B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{\rho_{surf}}{\rho_{res}}$$

- RazÃ£o gÃ¡s/Ã³leo dissolvido:
$$R_s=\dfrac{\text{vol. gÃ¡s liberado (condiÃ§Ãµes padrÃ£o)}}{\text{vol. Ã³leo (superfÃ­cie)}}\quad(\text{scf/STB ou m}^3/\text{m}^3)$$

2.3. Compressibilidade de fluidos
- Compressibilidade do Ã³leo (adimensional, psiâ»1 ou Paâ»1):
$$c_o = -\dfrac{1}{V_o}\dfrac{\mathrm{d}V_o}{\mathrm{d}p}=\dfrac{\mathrm{d}(\ln V_o)}{\mathrm{d}p}$$
- Compressibilidade do gÃ¡s (aprox.):
$$c_g \approx \dfrac{1}{p}\left(1-\dfrac{\partial\ln Z}{\partial\ln p}\right)$$
(obter Z(p,T) de charts ou EoS)

2.4. EquaÃ§Ãµes de estado cÃºbicas (uso em PVT)
- DefiniÃ§Ãµes gerais (PR e SRK usadas com frequÃªncia):
  - Definir constantes crÃ­ticas de cada componente: $T_c, p_c, \omega$ (fator acÃªntrico).

- Pengâ€‘Robinson (PR):
  - ParÃ¢metros puros:
  $$a = 0.45724\dfrac{R^2 T_c^2}{p_c},\qquad b = 0.07780\dfrac{R T_c}{p_c}$$
  - Fator de temperatura:
  $$\alpha(T)=\left[1+\kappa (1-\sqrt{T_r})\right]^2,\quad T_r=\dfrac{T}{T_c}$$
  com
  $$\kappa = 0.37464 + 1.54226\omega - 0.26992\omega^2.$$
  - EoS:
  $$p=\dfrac{RT}{V-b}-\dfrac{a\alpha(T)}{V(V+b)+b(V-b)}$$

- Soaveâ€‘Redlichâ€‘Kwong (SRK):
  - ParÃ¢metros:
  $$a = 0.42748\dfrac{R^2T_c^2}{p_c},\qquad b=0.08664\dfrac{RT_c}{p_c}$$
  - EoS (forma):
  $$p=\dfrac{RT}{V-b}-\dfrac{a\alpha(T)}{V(V+b)}$$
  - Kappa (SRK): parÃ¢metro dependente de $\omega$ (ver formulaÃ§Ã£o SRK).

- Mistura (regra de mistura van der Waals tipo):
  $$a_{mix}=\sum_i\sum_j x_i x_j \sqrt{a_i a_j}(1-k_{ij}),\qquad b_{mix}=\sum_i x_i b_i$$
  onde $k_{ij}$ sÃ£o parÃ¢metros de interaÃ§Ã£o binÃ¡ria.

- ReduÃ§Ã£o a polinomial em Z (cÃºbica): em geral obtemâ€‘se um polinÃ³mio cÃºbico em $Z$ (derivado do EoS multiplicado por $V$ e normalizado) do tipo:
  $$Z^3 + c_2 Z^2 + c_1 Z + c_0 = 0$$
  com coeficientes que dependem de $A$ e $B$:
  $$A=\dfrac{a p}{(R T)^2},\qquad B=\dfrac{b p}{R T}$$
  e um polinÃ³mio padrÃ£o (usado tanto para PR como SRK apÃ³s definiÃ§Ã£o apropriada de $A,B$):
  $$Z^3-(1-B)Z^2+(A-3B^2-2B)Z-(AB-B^2-B^3)=0$$
  (resolver numericamente para raÃ­zes reais; raÃ­zes correspondem a fases gasosa/lÃ­quida onde aplicÃ¡vel).

2.5. CÃ¡lculo de fatores de volume com Z
- FormaÃ§Ã£o volume factor do gÃ¡s (por molar/molar base):
  $$B_g = \dfrac{Z R T}{p}\cdot\dfrac{V_{ref\_units}}{n_{ref}}$$
  (usar forma prÃ¡tica/constantes de conversÃ£o ao trabalhar em scf/ftÂ³ ou SI).

2.6. CorrelacÌ§oÌƒes empÃ­ricas e conversÃµes Ãºteis
- ConversÃµes:
  $$1\,\text{scf}=0.0283168\,\text{m}^3,\quad1\,\text{STB}=0.1589873\,\text{m}^3$$
- API gravity (relativa Ã  Ã¡gua a 60Â°F):
  $$API=\dfrac{141.5}{SG_{60Â°F}} -131.5,\quad SG=\dfrac{\rho_{oil}}{\rho_{water}}$$

2.7. Exemplo prÃ¡tico PVT (completo)
- Dados: $V_{res}=1.20\,$bbl; $V_{surf}=1.00\,$STB; $R_s=400\,$scf/STB.
  1) $B_o=1.20/1.00=1.20\,$bbl/STB.
  2) $R_s(\text{SI})=400\times0.0283168/0.1589873\approx71.3\,\text{m}^3/\text{m}^3$.
  3) Densidade de reservatÃ³rio: $\rho_{res}=\rho_{surf}/B_o$.

---

## CapÃ­tulo 3 â€” Propriedades das rochas (detalhado)

3.1. Porosidade (definiÃ§Ãµes e mÃ©todos)
- Porosidade total: $\phi=V_p/V_t$.
- MÃ©todos mediÃ§Ã£o: gravimÃ©tricos (pesagem seca/saturada), porosimetria de mercÃºrio, NMR, microâ€‘CT.
- Porosidade efetiva (conectada) e irreducÃ­vel (connate water) â€” distinguir para flow modelling.

3.2. Densidade de rocha saturada (mixing law)
$$\rho_b = (1-\phi)\rho_s + \phi (S_w \rho_w + S_o \rho_o + S_g \rho_g)$$
onde $\rho_s$ densidade da matriz.

3.3. Permeabilidade e Lei de Darcy
- Forma integral (unidimensional):
$$q = -\dfrac{k A}{\mu}\dfrac{\Delta p}{L}$$
- Para fluxo radial permanente para poÃ§o produtor (campo/ft):
$$q=\dfrac{2\pi k h (p_e-p_{wf})}{\mu \ln(r_e/r_w)}$$
(usar conversÃµes quando q em STB/d, Âµ em cP, k em mD â€” ver fÃ³rmulas de campo no anexo)

3.4. EquaÃ§Ã£o de difusividade (transiente, ligeiramente compressÃ­vel)
- Forma geral:
$$\dfrac{\partial p}{\partial t}=\dfrac{k}{\mu S} \nabla^2 p$$
onde $S$ (coeficiente de armazenamento) geralmente
$$S=\phi c_f + (1-\phi)c_s$$
com $c_f$ compressibilidade do fluido e $c_s$ compressibilidade da matriz sÃ³lida.

3.5. SoluÃ§Ã£o transiente radial (analÃ­tica aproximada â€” semilog)
- Para regime semilog (pseudosteady), pressÃ£o medida no poÃ§o varia com tempo t:
$$p(r_w,t)=p_i - \dfrac{q B \mu}{4\pi k h}\left[\ln\left(\dfrac{4 k t}{\phi \mu c_t r_w^2}\right)-0.80907\right]$$
- Em baseâ€‘10 logs (anÃ¡lise semilog): a declividade $m$ (psi por ciclo log10) Ã©
$$m=\dfrac{2.303\,q B \mu}{4\pi k h} = \dfrac{0.183 q B \mu}{k h}$$
  e, isolando $k$ (unidades de campo com $q$ em STB/d, $\mu$ cP, $h$ ft, $m$ psi/log10):
$$k(\text{mD}) = \dfrac{162.6\,q\,B\,\mu}{h\,m}$$
(162.6 Ã© constante empÃ­rica para conversÃµes entre unidades; verificar convenÃ§Ãµes de unidades)

3.6. FunÃ§Ã£o de Leverett e pressÃ£o capilar
- TensÃ£o interfacial e rÃ¡dio capilar simplificado (tubo):
$$P_c=\dfrac{2\sigma \cos\theta}{r}$$
- FunÃ§Ã£o J de Leverett:
$$J(S_w)=\dfrac{P_c(S_w)\sqrt{k/\phi}}{\sigma\cos\theta}$$
(usar J(S) para escalonar curvas Pc entre rochas com diferentes k e Ï†)

3.7. Permeabilidade relativa & modelos
- Modelo de Corey (exemplo):
$$S_{we}=\dfrac{S_w-S_{wr}}{1-S_{or}-S_{wr}}$$
$$k_{rw}=k_{rw0} S_{we}^{n_w},\quad k_{ro}=k_{ro0}(1-S_{we})^{n_o}$$
- ParÃ¢metros tÃ­picos: $n_w, n_o$ entre 2â€“4 dependendo de rocha/molhabilidade.

3.8. Resistividade e Archie
- EquaÃ§Ã£o de Archie:
$$R_t = a R_w \phi^{-m} S_w^{-n}$$
- ParÃ¢metros empÃ­ricos: $a\approx1$, $m\approx1.8-2.2$, $n\approx2$ (variam com litologia)

---

## CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico (OOIP / OGIP) â€” detalhe completo

4.1. FÃ³rmula fundamental (reservoir â†’ superfÃ­cie)
- Volume de fluido em reservatÃ³rio (mÂ³):
$$V_{fluid,res}=V_r\,\phi\,(1-S_w)$$
- Volume de superfÃ­cie:
$$N_{surface}=\dfrac{V_{fluid,res}}{B}\quad(\text{B = fator de volume de formaÃ§Ã£o})$$

4.2. FÃ³rmulas prÃ¡ticas de campo
- OOIP (barris stockâ€‘tank):
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$
  - DerivaÃ§Ã£o do factor 7758:
    - 1 acre = 43,560 ftÂ²; 1 ftÂ³ = 0.178107... bbl? (usar conversÃµes exatas). A relaÃ§Ã£o completa Ã©: 43560 ftÂ² Ã— 1 ft = 43560 ftÂ³ por acreÂ·ft; 1 bbl = 5.614583 ftÂ³; 43560/5.614583 â‰ˆ 7758 bbl/acreÂ·ft.

- OGIP (scf):
$$OGIP=\dfrac{43560\,A\,h\,\phi\,(1-S_w)}{B_g}$$
(43560 = ftÂ³/acre coeficient)

4.3. Sensibilidade analÃ­tica (derivadas parciais)
- Sensibilidade de OOIP a Ï†:
$$\dfrac{\partial OOIP}{\partial\phi}=\dfrac{7758 A h (1-S_w)}{B_o}$$
- Sensibilidade fraccional relativa: usar variÃ¡veis aleatÃ³rias e Monte Carlo para propagar incertezas.

4.4. Monte Carlo (passos prÃ¡ticos)
1. Definir distribuiÃ§Ãµes para cada variÃ¡vel incerta (A,h,Ï†,S_w,B_o): triangular, normal truncada ou lognormal conforme justificativa.
2. Amostrar N vezes (p.ex. 10kâ€‘100k iteraÃ§Ãµes para robustez) e calcular OOIP para cada amostra.
3. Ordenar resultados e extrair percentis P10/P50/P90.
4. Reportar mÃ©dia, mediana (P50), intervalo de confianÃ§a e curvas CDF/PDF.

4.5. Estimativa setorial
- Dividir reservatÃ³rio em setores i com A_i,h_i,Ï†_i,S_{w,i} e somar:
$$OOIP_{total}=\sum_i \dfrac{7758 A_i h_i \phi_i (1-S_{w,i})}{B_{o,i}}$$

---

## CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM) â€” completo

5.1. Conceito (conservaÃ§Ã£o de massa)
- A EBM parte do princÃ­pio: estoque inicial = estoque atual + produÃ§Ã£o acumulada - injeÃ§Ãµes + influxo. Convertendo volumes e considerando compressibilidade resulta em equaÃ§Ãµes relacionando variaÃ§Ã£o de pressÃ£o com quantidades produzidas/injetadas.

5.2. Forma linearizada (Havlena & Odeh, 1963)
- ExpressÃ£o usada em anÃ¡lise prÃ¡tica:
$$F = N E_o + m E_g + (1+m) E_{f,w} + W_e$$
onde:
- $F$ termo conhecido (construÃ­do a partir de produÃ§Ã£o/injeÃ§Ã£o e PVT);
- $N$ estoque original de Ã³leo (OOIP);
- $m$ razÃ£o gasâ€‘cap/Ã³leo (adimensional);
- $E_o,E_g,E_{f,w}$ termos calculÃ¡veis a partir de PVT/pressÃ£o;
- $W_e$ termo de influxo do aquÃ­fero.

5.3. DefiniÃ§Ãµes prÃ¡ticas (forma operacional)
- Termos (formas comumente usadas em regressÃ£o):
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
$$E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$$
$$E_{f,w}=B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$$
- Lado conhecido $F$ (exemplo):
$$F = N_p B_o + G_p - R_s B_g + W_p B_w - W_{inj} B_w - G_{inj} B_{g,inj}$$
(ajustar sinais e convenÃ§Ãµes conforme o conjunto de dados â€” ver notas do curso)

5.4. Procedimento prÃ¡tico
1. Organizar sÃ©rie temporal: p(t), N_p(t), G_p(t), volumes injetados W_{inj},G_{inj}.
2. Calcular $B_o(p),B_g(p),R_s(p)$ a partir de PVT ou correlaÃ§Ãµes.
3. Calcular colunas $E_o,E_g,E_{f,w}$ para cada instante.
4. Calcular $F$ para cada instante.
5. Executar regressÃ£o linear mÃºltipla: ajustar $F$ por combinaÃ§Ã£o linear dos termos para obter $N$ e $m$ (coeficientes de regressÃ£o) e estimar $W_e$.

5.5. MÃ©todo p/z (para gÃ¡s)
- Plot de $p/z$ vs $G_p$: em reservatÃ³rios gasâ€‘dominados volumÃ©tricos sem influxo, a extrapolaÃ§Ã£o linear pode fornecer OGIP. InterpretaÃ§Ã£o: declive e intercepto do plot relacionam OGIP e condiÃ§Ãµes iniciais; trate com cuidado correÃ§Ãµes de temperatura e compressibilidade.

5.6. Exemplo simplificado (numÃ©rico)
- Construir tabela com p, N_p, G_p, B_o(p),B_g(p),R_s(p), calcular $E$'s e ajustar. (ver tarefas do capÃ­tulo 5 para exemplo completo do curso).

---

## Anexos â€” constantes, fatores de conversÃ£o e valores tÃ­picos

Constantes importantes:
- $R_{universal}=8.314462618\;\text{J/(molÂ·K)}$ (usar unidades coerentes)
- $g=9.80665\;\text{m/s}^2$

ConversÃµes Ãºteis:
- $1\,\text{acre}=43560\,\text{ft}^2$
- $1\,\text{acreÂ·ft}=43560\,\text{ft}^3$
- $1\,\text{bbl}=0.1589873\,\text{m}^3$
- $1\,\text{scf}=0.0283168\,\text{m}^3$
- $1\,\text{D}=9.869233\times10^{-13}\,\text{m}^2$
- $1\,\text{psi}=6894.757\,\text{Pa}$

Valores tÃ­picos (ordem de grandeza)
- Porosidade: 5%â€“30% para rochas reservatÃ³rio; mÃ©dias Ãºteis 10%â€“25%.
- Permeabilidade: mDâ€“D (argiloso <1 mD, arenito bom 100â€“1000 mD, carbonatos variam muito).
- Exponentes de Archie: $m\approx1.8-2.2$, $n\approx2$.

Checklist prÃ¡tico para cada capÃ­tulo (sintÃ©tico)
- Cap.1: listar elementos do sistema petrolÃ­fero; identificar tipo de armadilha e presenÃ§a de gasâ€‘cap/aqÃ¼Ã­fero.
- Cap.2: ter curvas B_o(p), R_s(p), Âµ_o(p) e tabela PVT; conhecer EoS e quando aplicÃ¡â€‘las.
- Cap.3: consolidar porosidade/permeabilidade por core e logs; obter curvas Pc(S) e kr(S).
- Cap.4: montar planilha volumÃ©trica setorial; rodar sensibilidade e Monte Carlo.
- Cap.5: organizar sÃ©ries de produÃ§Ã£o; calcular colunas E; aplicar regressÃ£o e interpretar resultados.

---

FIM â€” ficheiro gerado como versÃ£o ULTRAâ€‘DETALHADA. Se desejar, posso:
- (A) sobrepor `resumo_capitulos.md` com esta versÃ£o;
- (B) gerar PDF/LaTeX desta versÃ£o; ou
- (C) extrair cartÃµes Anki (Q/A) automaticamente a partir das definiÃ§Ãµes e fÃ³rmulas.

## ExercÃ­cios resolvidos (seleÃ§Ã£o representativa)

Esta secÃ§Ã£o apresenta soluÃ§Ãµes passoâ€‘aâ€‘passo para exercÃ­cios-chave dos capÃ­tulos 1â€“5. Use estes exemplos como modelo para resolver problemas semelhantes.

### CapÃ­tulo 1 â€” Verdadeiro/Falso (respostas e justificativas breves)
1) V â€” Armadilha geolÃ³gica (structural/estratigrÃ¡fica) impede migraÃ§Ã£o e acumula hidrocarbonetos.
2) F â€” Rocha geradora Ã© rica em matÃ©ria orgÃ¢nica (nÃ£o baixa).
3) F â€” Rocha selante tem **baixa** permeabilidade e impede fluxo.
4) V â€” MigraÃ§Ã£o ocorre por meios porosos e fraturados, favorÃ¡vel a caminhos permeÃ¡veis.
5) F â€” Sincronismo Ã© relevante: geraÃ§Ã£o, migraÃ§Ã£o e armadilhamento devem coincidir temporalmente.
6) V â€” CatagÃªnese = craqueamento tÃ©rmico do querogÃ©nio em hidrocarbonetos.
7) V â€” Sistema de produÃ§Ã£o inclui coleta, elevaÃ§Ã£o e separaÃ§Ã£o atÃ© a superfÃ­cie.
8) V â€” Em gasâ€‘cap drive o gÃ¡s livre expande e ajuda a manter pressÃ£o.
9) F â€” Porosidade e permeabilidade sÃ£o propriedades distintas (volume de poros vs facilidade de fluxo).
10) V â€” $B_o$ relaciona volumes em reservatÃ³rio e superfÃ­cie (reservoir â†’ surface).

### CapÃ­tulo 2 â€” PVT: exemplo resolvido (cÃ¡lculo de $B_o$ e conversÃ£o de $R_s$)
Enunciado: Num ensaio PVT por 1 STB de Ã³leo obteveâ€‘se $V_{res}=1.20\,$bbl e $V_{surf}=1.00\,$STB; gÃ¡s libertado $R_s=400\,$scf/STB.

a) CÃ¡lculo de $B_o$:
$$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ 

b) ConversÃ£o de $R_s$ para mÂ³/mÂ³:
1 scf = 0.0283168 mÂ³; 1 STB = 0.1589873 mÂ³.
$$R_s(\text{m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx\dfrac{11.32672}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3.$$ 

c) InterpretaÃ§Ã£o breve: $B_o>1$ indica que o volume no reservatÃ³rio Ã© maior que o volume final de superfÃ­cie por unidade (efeitos de compressibilidade e gÃ¡s dissolvido). $R_s$ alto implica presenÃ§a significativa de gÃ¡s dissolvido â€” ao atingir o ponto de bolha o gÃ¡s libertaâ€‘se, alterando mobilidade.

### CapÃ­tulo 3 â€” Rochas: exercÃ­cios resolvidos (porosidade por massa e mÃ©todo de ArquÃ­medes)

**Exemplo (ExercÃ­cio 1)** â€” Dados: $m_{sat}=130\,$g; $m_{dry}=105\,$g; $\rho_o=0.84\,$g/cm^3; $V_t=180\,$cm^3.

1) Volume de fluido nos poros:
$$V_f=\dfrac{m_{sat}-m_{dry}}{\rho_o}=\dfrac{130-105}{0.84}=\dfrac{25}{0.84}\approx29.7619\;\text{cm}^3.$$ 

2) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{29.7619}{180}\approx0.16534\approx16.53\%.$$ 

**Exemplo (ExercÃ­cio 5 â€” mÃ©todo de ArquÃ­medes)** â€” Dados: $m_{dry}=330\,$g; $m_{sat}=360\,$g; $m_{ap\_agua}=225\,$g; $\rho_{agua}=1\,$g/cm^3.

1) Volume total da amostra via empuxo (diferenÃ§a entre peso em ar e peso aparente em Ã¡gua):
$$V_t=\dfrac{m_{sat}-m_{ap\_agua}}{\rho_{agua}}=\dfrac{360-225}{1}=135\;\text{cm}^3.$$ 

2) Volume poroso (volume de fluido nos poros):
$$V_p=m_{sat}-m_{dry}=360-330=30\;\text{cm}^3.$$ 

3) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{30}{135}\approx0.22222\approx22.22\%. $$

ObservaÃ§Ã£o: nos relatÃ³rios, apresente as unidades, arredondamento e possÃ­veis fontes de erro experimental.

### CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico: exemplo resolvido (OOIP)

Dados (exercÃ­cio 4.8): $A=200\,$acres; $h_{net}=30\,$ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

FÃ³rmula prÃ¡tica:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}.$$ 

Substituindo os valores e calculando passo a passo:
\begin{align*}
7758\times200&=1\,551\,600\\
1\,551\,600\times30&=46\,548\,000\\
46\,548\,000\times0.18&=8\,378\,640\\
8\,378\,640\times0.75&=6\,283\,980\\
OOIP&=\dfrac{6\,283\,980}{1.2}\approx5\,236\,650\;\text{STB}.
\end{align*}

InterpretaÃ§Ã£o: aproximadamente 5.24Ã—10^6 STB originalmente em lugar.

### CapÃ­tulo 5 â€” EBM: exemplo prÃ¡tico (cÃ¡lculo de $E_o$ e montagem de colunas)

Dados ilustrativos (simplificados): $B_{o,i}=1.10$, $B_o=1.15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0.005$ (unidades consistentes com a formulaÃ§Ã£o do curso).

CÃ¡lculo do termo $E_o$ (Havlena & Odeh):
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
Substituindo:
$$E_o = 1.15 - 1.10 + (200-180)\times0.005 = 0.05 + 20\times0.005 = 0.05 + 0.10 = 0.15.$$ 

Notas prÃ¡ticas para montar a tabela de anÃ¡lise EBM:
- Para cada instante (data) calcule: $p$, $N_p$, $G_p$, $B_o(p)$, $B_g(p)$, $R_s(p)$.
- Calcule colunas $E_o,E_g,E_{f,w}$ por fÃ³rmulas definidas; calcule $F$ (lado conhecido) usando volumes produzidos/injetados convertidos para unidades compatÃ­veis;
- Execute regressÃ£o linear mÃºltipla de $F$ versus colunas $E_o,E_g,E_{f,w}$ para obter estimativas de $N$ (coeficiente associado a $E_o$) e $m$ (coeficiente associado a $E_g$).

Exemplo de output parcial (apenas ilustrativo):
| t | p (psi) | N_p (STB) | G_p (scf) | B_o | B_g | R_s | E_o | E_g | E_{f,w} | F |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| t_1 | 3000 | 100000 | 50000 | 1.10 | 0.0050 | 200 | 0.00 | 0.00 | 0.00 | F_1 |
| t_2 | 2900 | 120000 | 60000 | 1.12 | 0.0051 | 195 | 0.02 | 0.01 | 0.002 | F_2 |

Onde $F_i$ Ã© montado conforme convensÃ£o adotada no curso; preste atenÃ§Ã£o Ã s unidades (STB vs scf) e Ã s conversÃµes necessÃ¡rias.

---

Se desejar, posso expandir esta secÃ§Ã£o com soluÃ§Ãµes de todos os exercÃ­cios presentes em `exercÃ­cios_transcription.md` (isto exigirÃ¡ mais tempo e poderei criar um ficheiro separado `exercicios_resolvidos.md`).

Arquivo criado automaticamente pelo assistente.

# Resumo por CapÃ­tulo â€” Engenharia de ReservatÃ³rios I (VersÃ£o EXTREMAMENTE Detalhada)

Este documento contÃ©m um resumo aprofundado dos capÃ­tulos 1â€“5, com fÃ³rmulas, definiÃ§Ãµes, unidades, notas de interpretaÃ§Ã£o e exemplos numÃ©ricos passoâ€‘aâ€‘passo. Use como referÃªncia de estudo e para gerar fichas de revisÃ£o.

Ãndice
- CapÃ­tulo 1 â€” Conceitos e sistema petrolÃ­fero
- CapÃ­tulo 2 â€” Propriedades dos fluidos (PVT): teorias, fÃ³rmulas e correlaÃ§Ãµes
- CapÃ­tulo 3 â€” Propriedades das rochas: porosidade, permeabilidade, capilaridade e equaÃ§Ãµes aplicadas
- CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico (OOIP / OGIP): fÃ³rmulas de campo e SI, sensibilidade e Monte Carlo
- CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM): formulaÃ§Ã£o, linearizaÃ§Ã£o e exemplos
- Anexos: constantes, fatores de conversÃ£o, lista de fÃ³rmulas essenciais

---

**Nota de unidades:** Sempre indique o sistema: UNIDADES DE CAMPO (acres, ft, bbl, scf) ou SI (m, mÂ³, Pa). Muitos fatores prÃ¡ticos (ex.: 7758) convertem acresÂ·ft â†’ bbl.

---

## CapÃ­tulo 1 â€” Conceitos e sistema petrolÃ­fero

1.1 Principais definiÃ§Ãµes
- Sistema petrolÃ­fero: conjunto de elementos necessÃ¡rios para geraÃ§Ã£o, migraÃ§Ã£o, armadilhamento e acumulaÃ§Ã£o de hidrocarbonetos.
- Sistema de produÃ§Ã£o: instalaÃ§Ãµes e equipamentos para recuperaÃ§Ã£o, elevaÃ§Ã£o e tratamento dos fluidos do reservatÃ³rio atÃ© a superfÃ­cie.

1.2 EquaÃ§Ãµes e relaÃ§Ãµes fundamentais (Ãºteis para este capÃ­tulo)
- EquilÃ­brio hidrostÃ¡tico (coluna incompressÃ­vel ideal):
$$p(z)=p_{ref}+\rho g (Z_{ref}-Z)$$
onde $p$ em Pa (ou psi), $\rho$ densidade (kg/mÂ³), $g$ = 9.80665 m/sÂ², $Z$ profundidade.
- Soma de saturaÃ§Ãµes (misto trifÃ¡sico):
$$S_w + S_o + S_g = 1$$
onde cada $S_\bullet$ Ã© fraÃ§Ã£o volumÃ©trica adimensional.

1.3 Conceitos qualitativos importantes
- Armadilha (structural/estratigrÃ¡fica/fraturada), rocha geradora/selante, migraÃ§Ã£o; sincronismo e janela tÃ©rmica (catagÃªnese) â€” sem equaÃ§Ãµes mas essenciais para interpretaÃ§Ã£o geolÃ³gica.

---

## CapÃ­tulo 2 â€” Propriedades dos fluidos (PVT)

2.1 VariÃ¡veis termodinÃ¢micas fundamentais
- EquaÃ§Ã£o dos gases ideais (mol):
$$pV=nRT$$
onde $p$ (Pa), $V$ (mÂ³), $n$ (mol), $R$ (8.314462618 J/(molÂ·K)), $T$ (K).
- Fator de compressibilidade (Z):
$$Z=\dfrac{pV}{nRT}=\dfrac{p\,\overline{v}}{RT}$$
Z corrige o comportamento real do gÃ¡s.

2.2 DefiniÃ§Ãµes PVT essenciais
- Fator de volume de formaÃ§Ã£o do Ã³leo ($B_o$):
$$B_o=\dfrac{V_{res\_oil}}{V_{surf\_oil}}\quad(\text{unidades: m}^3/\text{m}^3\;\text{ou bbl/STB})$$
- Fator de volume do gÃ¡s ($B_g$): volume de gÃ¡s no reservatÃ³rio por unidade de gÃ¡s padrÃ£o (ftÂ³/SCF ou mÂ³/SmÂ³):
$$B_g=\dfrac{V_{res\_gas}}{V_{std\_gas}}$$
- RazÃ£o gÃ¡s/Ã³leo dissolvido ($R_s$): normalmente em scf/STB (campo) ou mÂ³/mÂ³ (SI):
$$R_s=\dfrac{\text{volume de gÃ¡s dissolvido no Ã³leo (std)}}{\text{volume de Ã³leo (superfÃ­cie)}}$$

2.3 Compressibilidades e variaÃ§Ãµes com pressÃ£o
- Compressibilidade do Ã³leo (bo):
$$c_o = -\dfrac{1}{V_o}\dfrac{\mathrm{d}V_o}{\mathrm{d}p} = \dfrac{\mathrm{d}(\ln V_o)}{\mathrm{d}p}$$
- Compressibilidade do gÃ¡s (aproximaÃ§Ã£o):
$$c_g \approx \dfrac{1}{p} \left(1 - \dfrac{\mathrm{d}\ln Z}{\mathrm{d}\ln p}\right)$$
Usar tabelas/curvas Z para cÃ¡lculo prÃ¡tico.

2.4 CorrelaÃ§Ãµes e estimativas empÃ­ricas (nomes e uso)
- CorrelaÃ§Ãµes de $B_o$, $\mu_o$, $R_s$ (Standing, Vazquezâ€‘Beggs, Beggs & Robinson para viscosidade). Estas fornecem estimativas quando nÃ£o existem ensaios PVT.

2.5 ConversÃµes Ãºteis (campo â†” SI)
- $1\,\text{scf}=0.0283168\,\text{m}^3$;
- $1\,\text{STB}=0.1589873\,\text{m}^3$;
- $1\,\text{bbl}=0.1589873\,\text{m}^3$.

2.6 Exemplo prÃ¡tico (passo a passo)
- Dados: $V_{res}=1.20\,$bbl, $V_{surf}=1.00\,$STB, $R_s=400\,$scf/STB.
- $B_o = 1.20/1.00 = 1.20\,$bbl/STB.
- $R_s$ em SI:
$$R_s(\text{m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3$$

---

## CapÃ­tulo 3 â€” Propriedades das rochas

3.1 Porosidade e volumes
- Porosidade total:
$$\phi=\dfrac{V_p}{V_t}$$
onde $V_p$ Ã© o volume de poros e $V_t$ o volume total.
- Porosidade a partir de massa (mÃ©todo gravimÃ©trico):
$$V_p=\dfrac{m_{sat}-m_{dry}}{\rho_f},\qquad \phi=\dfrac{V_p}{V_t}$$

3.2 Densidades e densidade aparente (logs)
- Massa especÃ­fica/aparente: para rocha saturada
$$\rho_b=(1-\phi)\rho_{s}+\phi(S_w\rho_w+S_o\rho_o+S_g\rho_g)$$
onde $\rho_s$ Ã© a densidade da matriz.

3.3 Permeabilidade (Lei de Darcy)
- Forma diferencial (unidimensional):
$$q=-\dfrac{kA}{\mu}\dfrac{\mathrm{d}p}{\mathrm{d}x}$$
onde $q$ Ã© vazÃ£o volumÃ©trica (mÂ³/s), $k$ permeabilidade (mÂ²), $A$ Ã¡rea (mÂ²), $\mu$ viscosidade (PaÂ·s).
- Fluxo radial estacionÃ¡rio (poÃ§o produtor, conduto linearizado):
$$q=\dfrac{2\pi k h (p_e-p_{wf})}{\mu\ln\left(\dfrac{r_e}{r_w}\right)}$$
onde $h$ Ã© espessura produtiva, $r_e$ raio de drenagem, $r_w$ raio do poÃ§o.

3.4 Difusividade (equaÃ§Ã£o do fluxo transiente)
- Para fluido ligeiramente compressÃ­vel:
$$\dfrac{\partial p}{\partial t}=\dfrac{k}{\phi\mu c_t}\nabla^2 p$$
onde $c_t$ Ã© compressibilidade total (soma das compressibilidades relevantes).

3.5 Capilaridade e funÃ§Ã£o de Leverett
- PressÃ£o capilar (tubo capilar simplificado):
$$P_c = \dfrac{2\sigma\cos\theta}{r}$$
- FunÃ§Ã£o de Leverett:
$$J(S_w)=\dfrac{P_c(S_w)\sqrt{k/\phi}}{\sigma\cos\theta}$$

3.6 SaturaÃ§Ãµes e permeabilidades relativas
- $S_w+S_o+S_g=1$;
- Permeabilidade relativa: $k_{r\alpha}=f(S_\alpha)$ (curvas experimentais).

3.7 Resistividade e saturaÃ§Ã£o â€” EquaÃ§Ã£o de Archie
- Forma usual (zona limpa, rocha nÃ£o condutiva):
$$R_t = a\,R_w\,\phi^{-m}\,S_w^{-n}$$
ou invertendo para saturaÃ§Ã£o:
$$S_w = \left(\dfrac{a\,R_w}{R_t\,\phi^{m}}\right)^{1/n}$$
com parÃ¢metros empÃ­ricos $a,m,n$.

3.8 Exemplos resolvidos (porosidade por massa; ArquÃ­medes)
- Ver exemplos do capÃ­tulo 3 (por ex., $\phi\approx16{,}5\%$ e $22{,}2\%$ em exercÃ­cios prÃ¡ticos â€” seguir passos mostrados).

---

## CapÃ­tulo 4 â€” IntegraÃ§Ã£o de Dados e CÃ¡lculo VolumÃ©trico

4.1 Forma geral (reservoir and surface)
- Volume de fluido em reservatÃ³rio (mÂ³):
$$V_{fluid,res}=V_r\,\phi\,(1-S_w)$$
- ConversÃ£o para superfÃ­cie usando fator de volume $B$ (mÂ³/mÂ³):
$$N_{surface}=\dfrac{V_{fluid,res}}{B}$$

4.2 FÃ³rmulas prÃ¡ticas (unidades de campo)
- OOIP (STB):
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$
onde $A$ em acres, $h$ em ft, $\phi$ fraÃ§Ã£o, $B_o$ em bbl/STB.\
DerivaÃ§Ã£o rÃ¡pida do fator 7758:
1 acre = 43560 ft^2; 1 acreÂ·ft = 43560 ft^3; 1 bbl = 5.614583 ft^3 â†’ 43560/5.614583 \approx 7758 bbl/acreÂ·ft.

- OGIP (SCF):
$$OGIP=\dfrac{43560\,A\,h\,\phi\,(1-S_w)}{B_g}$$
onde $B_g$ Ã© o fator volume do gÃ¡s (ft^3/SCF).

4.3 Estimativa de reservas recuperÃ¡veis
- Reservas volumÃ©tricas (por fator de recuperaÃ§Ã£o $F_R$):
$$N_R = OOIP\times F_R$$
ou pontualmente (contando saturaÃ§Ãµes residuais):
$$N_R = V_r\,\phi\,(1-S_{w,i})\left(\dfrac{S_{o,i}}{B_{o,i}} - \dfrac{S_{o,r}}{B_{o,r}}\right)$$

4.4 AnÃ¡lise de sensibilidade e incerteza
- Derivada parcial (sensibilidade de OOIP a $\phi$):
$$\dfrac{\partial OOIP}{\partial\phi}=\dfrac{7758\,A\,h\,(1-S_w)}{B_o}$$
- Monte Carlo: descreva distribuiÃ§Ãµes para $A,h,\phi,S_w,B_o$ (p.ex. triangular, normal truncada, lognormal), gere N amostras e calcule percentis P10/P50/P90 da distribuiÃ§Ã£o resultante de OOIP.

4.5 Boas prÃ¡ticas de integraÃ§Ã£o
- QA/QC em dados de core, logs e PVT; uso de mapas de net pay e cutâ€‘offs; segmentaÃ§Ã£o setorial (zonas) â€” calcular OOIP por setor e somar.

---

## CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM)

5.1 Conceito geral
- A EBM relaciona as quantidades produzidas/injetadas com a variaÃ§Ã£o de estoque no reservatÃ³rio; Ã© uma equaÃ§Ã£o de conservaÃ§Ã£o de massa para os poros.

5.2 Forma linearizada (Havlena & Odeh)
- VariÃ¡vel conhecida (lado esquerdo), $F$, Ã© construÃ­da a partir de dados de produÃ§Ã£o e injeÃ§Ã£o convertidos para volumes de superfÃ­cie. A forma linearizada usada comumente Ã©:
$$F = N\,E_o + m\,E_g + (1+m)\,E_{f,w} + W_e$$
onde:
- $E_o = B_o - B_{o,i} + (R_{s,i}-R_s)\,B_g$;
- $E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$;
- $E_{f,w} = B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$;
- $N$ Ã© OOIP (a estimar), $m$ razÃ£o gasâ€‘cap/Ã³leo (a estimar), $W_e$ contribuiÃ§Ã£o lÃ­quida do aquÃ­fero.

5.3 ConstruÃ§Ã£o prÃ¡tica de $F$ (exemplo simplificado)
- Exemplo (formas ilustrativas): calcular $F$ acumulado por intervalo como combinaÃ§Ã£o de termos de produÃ§Ã£o $N_p B_o$, $G_p$ e correÃ§Ãµes por $R_s$, volumes injetados, etc. (ver exercÃ­cios e ficheiro cap5 para forma usada no curso).

5.4 EstimaÃ§Ã£o por regressÃ£o
- Monte as colunas $F, E_o, E_g, E_{f,w}$ para vÃ¡rios instantes. Execute regressÃ£o linear mÃºltipla:
$$F = \beta_1 E_o + \beta_2 E_g + \beta_3 E_{f,w} + \varepsilon$$
onde idealmente $\beta_1=N$, $\beta_2=m$, $\beta_3=(1+m)$ e $\varepsilon$ residuais (ou ajustar conforme convenÃ§Ã£o usada).

5.5 Notas sobre gÃ¡s e p/z
- Para reservatÃ³rios gasâ€‘dominados, a anÃ¡lise p/z (plot de $p/z$ vs $G_p$) permite estimar OGIP por extrapolaÃ§Ã£o; p/z Ã© inversamente proporcional ao volume remanescente quando as condiÃ§Ãµes sÃ£o adequadas. (ImplementaÃ§Ã£o numÃ©rica e tratamentos de retroinjeÃ§Ã£o exigem cuidados de unidades e correÃ§Ãµes).

---

## Anexos â€” FÃ³rmulas essenciais e constantes

Constantes e conversÃµes rÃ¡pidas
- $1\,\text{acre}=43560\,\text{ft}^2$.
- $1\,\text{acreÂ·ft}=43560\,\text{ft}^3\approx7758\,\text{bbl}$.
- $1\,\text{bbl}=0.1589873\,\text{m}^3$.
- $1\,\text{scf}=0.0283168\,\text{m}^3$.
- $1\,\text{D}=9.869233\times10^{-13}\,\text{m}^2$.
- $1\,\text{psi}=6894.757\,\text{Pa}$.

Lista condensada de fÃ³rmulas (referÃªncia rÃ¡pida)
- SomatÃ³rio das saturaÃ§Ãµes: $S_w+S_o+S_g=1$.
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

## SugestÃµes de estudo e uso deste ficheiro
- Transforme cada subseÃ§Ã£o num cartÃ£o de revisÃ£o (Anki) â€” fÃ³rmulas, definiÃ§Ãµes e exemplos numÃ©ricos.
- Implemente as fÃ³rmulas essenciais numa planilha (OOIP/OGIP/Monte Carlo) para treino prÃ¡tico.
- Para a prova: foque em interpretar o significado fÃ­sico das fÃ³rmulas (o que altera OOIP, por que $B_o$ varia com pressÃ£o, como $R_s$ altera mobilidade, etc.).

---

Arquivo gerado automaticamente pelo assistente â€” versÃ£o detalhada criada a pedido do utilizador.
# Banco de questÃµes â€” Matriz completa (CapÃ­tulos 1â€“5 + exercÃ­cios)

Este ficheiro reÃºne todas as perguntas, exercÃ­cios e tarefas extraÃ­dos dos materiais em `Estudar/matÃ©ria` (capÃ­tulos 1â€“5, ficheiro de exercÃ­cios e resumos). Use este banco para construir provas, listas de treino ou fichas de estudo.

---

## CapÃ­tulo 1 â€” Sistema petrolÃ­fero e conceitos fundamentais
(QuestÃµes extraÃ­das de `cap1_transcription.md`)

ConsolidaÃ§Ã£o â€” ExercÃ­cios / QuestÃµes:
1. O Ã³leo produzido em reservatÃ³rios leves caracterizaâ€‘se por: (escolhas Aâ€“E). TransformÃ¡vel em V/F.
2. O gÃ¡s produzido em reservatÃ³rios influencia a recuperaÃ§Ã£o de Ã³leo porque: (escolhas Aâ€“E).
3. ReservatÃ³rios com mecanismo de water drive caracterizamâ€‘se por: (escolhas Aâ€“E).
4. A viscosidade do Ã³leo impacta diretamente: (escolhas Aâ€“E).
5. Um mecanismo de produÃ§Ã£o por expansÃ£o de gÃ¡s livre (gasâ€‘cap drive): (escolhas Aâ€“E).
6. O condensado produzido em reservatÃ³rios ocorre quando: (escolhas Aâ€“E).
7. CaracterÃ­sticas do solution gas drive â€” identificar a opÃ§Ã£o que NÃƒO define o mecanismo.
8. Em um reservatÃ³rio com influxo de Ã¡gua, a produÃ§Ã£o Ã© sustentada porque: (escolhas Aâ€“E).
9. A produÃ§Ã£o em reservatÃ³rio undersaturated depende principalmente de: (escolhas Aâ€“E).
10. O que caracteriza um reservatÃ³rio com gasâ€‘cap drive? (escolhas Aâ€“E).

Tarefas transformÃ¡veis em perguntas:
- Explique a diferenÃ§a entre Sistema de ProduÃ§Ã£o, Sistema PetrolÃ­fero e cadeia produtiva.
- Desenhe o envelope de fases e identifique ponto de bolha e orvalho.
- Complete: HIDROCARBONETOS + NÃƒO HIDROCARBONETOS = _____________.
- QuestÃµes de definiÃ§Ã£o: porosidade (\phi), saturaÃ§Ãµes (S_w, S_o), B_o, R_s, etc.

---

## CapÃ­tulo 2 â€” Propriedades dos fluidos (PVT)
(QuestÃµes extraÃ­das de `cap2_transcription.md`)

ConsolidaÃ§Ã£o / Perguntas:
- O que Ã© $B_o$ e por que Ã© importante para volumes produzidos? (curta resposta)
- Como $R_s$ varia com pressÃ£o e o que significa o ponto de bolha?
- Como a viscosidade do Ã³leo influencia a mobilidade e o fator de recuperaÃ§Ã£o?
- Quando tratar o gÃ¡s como ideal e quando usar correÃ§Ãµes (Zâ€‘factor)?

Tarefas / Problemas numÃ©ricos:
1. Calcule $B_o$ e $R_s$ para ensaio PVT simplificado: $V_{res}=1.20$ bbl; $V_{surf}=1.00$ STB; $R_s=400$ scf/STB. (a) $B_o$ em bbl/STB; (b) converta $R_s$ para m^3/m^3).
2. Desenhar envelope de fases para mistura Ã³leoâ€‘gÃ¡s e identificar ponto de bolha/orvalho.
3. Dado uma tabela PVT simplificada, calcular curvas $B_o(p)$, $R_s(p)$ e discutir implicaÃ§Ãµes.
4. Aplicar correlaÃ§Ã£o (Standing, Vazquezâ€‘Beggs) para estimar $B_o$ quando nÃ£o hÃ¡ dados experimentais.
5. Tarefas propostas (cap2): calcular $B_o$ e $R_s$ em casos hipotÃ©ticos; comparar equaÃ§Ãµes de estado cÃºbicas.

---

## CapÃ­tulo 3 â€” Propriedades das rochas
(QuestÃµes extraÃ­das de `cap3_transcription.md`)

ExercÃ­cios e problemas:
1. Amostra saturada com Ã³leo: $m_{sat}=130$ g; $m_{dry}=105$ g; $\rho_o=0.84$ g/cm^3; $V_t=180$ cm^3. (a) Determine porosidade; (b) passos e unidades.
2. Determinar porosidade idealizada em figuras (a), (b), (c) â€” transformar em enunciados com figuras ou descriÃ§Ãµes.
3. CÃ¢mara de pressÃ£o: $V_1=100$ cc; $V_2=100$ cc; $p_1=15$ psi; $p_2=60$ psi; $p_f=39$ psi. Determinar volume do grÃ£o da amostra.
4. Calcule porosidade mÃ©dia para amostras com porosidades: 10, 12, 11, 13, 14, 10, 17%.
5. MÃ©todo de ArquÃ­medes: peso seco = 330 g; peso saturado = 360 g; peso aparente em Ã¡gua = 225 g; densidade da Ã¡gua = 1 g/cm^3. Determine a porosidade (passos).
6. QuestÃµes qualitativas: porosidade total vs efectiva; efeitos da compactaÃ§Ã£o; processos diagenÃ©ticos; molhabilidade e capilaridade.
7. Problemas adicionais: estimativa de compressibilidade de poros e aplicaÃ§Ã£o da funÃ§Ã£o de Leverett.

---

## CapÃ­tulo 4 â€” IntegraÃ§Ã£o de dados e cÃ¡lculo volumÃ©trico
(QuestÃµes extraÃ­das de `cap4_transcription.md`)

ExercÃ­cios / ConsolidaÃ§Ã£o:
1. Dado: A = 200 acres; $h_{net}=30$ ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2$. Calcule OOIP (fÃ³rmula prÃ¡tica).
2. FaÃ§a anÃ¡lise de sensibilidade variando $\phi$ entre 0.15â€“0.22 e interprete impacto no OOIP.
3. Explique como Netâ€‘toâ€‘Gross e cutâ€‘offs alteram a estimativa volumÃ©trica.

Tarefas/RedaÃ§Ã£o (temas para dissertaÃ§Ã£o):
- Incertezas no mÃ©todo volumÃ©trico: fontes, quantificaÃ§Ã£o e mitigaÃ§Ã£o (P10/P50/P90, Monte Carlo).
- IntegraÃ§Ã£o de dados petrofÃ­sicos e geolÃ³gicos para estimativa de OOIP.
- Plano de QA/QC para dados petrofÃ­sicos antes do cÃ¡lculo volumÃ©trico.

---

## CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM)
(QuestÃµes extraÃ­das de `cap5_transcription.md`)

ExercÃ­cios / ConsolidaÃ§Ã£o:
1. Explique a lÃ³gica da linearizaÃ§Ã£o de Havlena & Odeh.
2. Descreva os passos para construir o termo $F$ e os termos $E_o, E_g, E_{f,w}$ a partir de dados de produÃ§Ã£o e PVT.
3. Discuta como incluir influxo de aquÃ­fero e injeÃ§Ã£o de Ã¡gua na formulaÃ§Ã£o da EBM.

Tarefas prÃ¡ticas:
1. Aplicar a linearizaÃ§Ã£o Havlena & Odeh a dados hipotÃ©ticos (fornecer dados se desejar).
2. AnÃ¡lise de sensibilidade para $B_o, \phi, S_{w,i}$ e impacto nas reservas.
3. RelatÃ³rio comparando EBM e mÃ©todo volumÃ©trico para mesmo caso.

---

## Banco de questÃµes extra (do ficheiro `exercÃ­cios_transcription.md`)
- O documento de exercÃ­cios contÃ©m conjuntos de problemas organizados por capÃ­tulo; incluir como itens a lista de problemas por capÃ­tulo (Partes I e II).  
- Exemplos gerais: problemas de conversÃ£o de unidades, problemas PVT, problemas de porosidade/permeabilidade, questÃµes de material balance e anÃ¡lise de declÃ­nio.

---

## Uso
- Para gerar uma prova com a estrutura pedida (1 V/F â€” cap.1; 1 RedaÃ§Ã£o â€” cap.4; 1 cÃ¡lculo â€” cap.2; 1 cÃ¡lculo â€” cap.3) escolha, por capitulo, 1â€“3 enunciados deste ficheiro e monte o documento final.  
- Posso gerar automaticamente:  
  - (A) Prova em LaTeX/PDF com 4 perguntas aleatÃ³rias da matriz,  
  - (B) PDF imprimÃ­vel com todo o banco de questÃµes,  
  - (C) Conjunto de afirmaÃ§Ãµes V/F pronto para correÃ§Ã£o automÃ¡tica (Cap.1).  

Diga qual das opÃ§Ãµes prefere que eu execute a seguir.
# Banco de questÃµes â€” Prova (CapÃ­tulos 1â€“4)

Este ficheiro agrupa todas as perguntas extraÃ­das dos CapÃ­tulos 1 a 4 que podem ser usadas na prova com a estrutura requerida:
1) Verdadeiro/Falso â€” CapÃ­tulo 1
2) DissertaÃ§Ã£o (RedaÃ§Ã£o) â€” CapÃ­tulo 4
3) CÃ¡lculo/prÃ¡tico â€” CapÃ­tulo 2
4) CÃ¡lculo/prÃ¡tico â€” CapÃ­tulo 3

---

## 1) Verdadeiro/Falso â€” CapÃ­tulo 1
(Use estas questÃµes para construir afirmaÃ§Ãµes V/F ou convertÃªâ€‘las para enunciados curtos)

ConsolidaÃ§Ã£o â€” QuestÃµes (originais):
1. O Ã³leo produzido em reservatÃ³rios leves caracterizaâ€‘se por: A) Alta viscosidade e baixa mobilidade; B) Baixa densidade e alta mobilidade; C) FormaÃ§Ã£o de gÃ¡s livre em excesso; D) SaturaÃ§Ã£o irreductÃ­vel de Ã¡gua igual a zero; E) Exclusivamente lÃ­quido sem variaÃ§Ã£o de densidade.
2. O gÃ¡s produzido em reservatÃ³rios influencia a recuperaÃ§Ã£o de Ã³leo porque: A) Reduz a pressÃ£o do reservatÃ³rio e facilita o fluxo de Ã³leo; B) Aumenta a densidade do Ã³leo; C) Impede totalmente a produÃ§Ã£o de Ã¡gua; D) Ã‰ irrelevante para a eficiÃªncia de produÃ§Ã£o; E) A saturaÃ§Ã£o de Ã³leo se torna irrelevante.
3. ReservatÃ³rios com mecanismo de water drive caracterizamâ€‘se por: A) ManutenÃ§Ã£o da pressÃ£o por influxo de Ã¡gua do aquÃ­fero; B) ElevaÃ§Ã£o artificial de Ã³leo via bombeio mecÃ¢nico; C) ExpansÃ£o de gÃ¡s dissolvido no Ã³leo; D) ProduÃ§Ã£o exclusivamente de gÃ¡s condensado; E) InexistÃªncia de Ã³leo saturado.
4. A viscosidade do Ã³leo impacta diretamente: A) A taxa de fluxo pelo reservatÃ³rio; B) A pressÃ£o do aquÃ­fero; C) A densidade da Ã¡gua; D) A compressibilidade da rocha; E) A saturaÃ§Ã£o irreductÃ­vel de gÃ¡s.
5. Um mecanismo de produÃ§Ã£o por expansÃ£o de gÃ¡s livre (gasâ€‘cap drive): A) MantÃ©m pressÃ£o por expansÃ£o de gÃ¡s acima do Ã³leo; B) Depende exclusivamente de Ã¡gua injetada; C) Gera aumento da viscosidade do Ã³leo; D) Reduz a saturaÃ§Ã£o irreductÃ­vel de Ã¡gua; E) Impede o fluxo de Ã³leo.
6. O condensado produzido em reservatÃ³rios ocorre quando: A) O lÃ­quido condensado se separa do gÃ¡s Ã  medida que a pressÃ£o diminui; B) Ã“leo leve Ã© produzido sem formaÃ§Ã£o de gÃ¡s; C) A Ã¡gua do reservatÃ³rio se transforma em gÃ¡s; D) A pressÃ£o estÃ¡ acima da pressÃ£o de saturaÃ§Ã£o do gÃ¡s; E) NÃ£o hÃ¡ variaÃ§Ã£o de densidade com a pressÃ£o.
7. Qual das seguintes caracterÃ­sticas NÃƒO define o mecanismo solution gas drive? A) ExpansÃ£o do gÃ¡s dissolvido no Ã³leo; B) ReduÃ§Ã£o gradual da pressÃ£o do reservatÃ³rio; C) FormaÃ§Ã£o de gÃ¡s livre a partir do Ã³leo; D) DependÃªncia da pressÃ£o inicial para mobilidade; E) ProduÃ§Ã£o contÃ­nua de Ã³leo.
8. Em um reservatÃ³rio com influxo de Ã¡gua (water influx), a produÃ§Ã£o de Ã³leo Ã© sustentada porque: A) A Ã¡gua do aquÃ­fero desloca o Ã³leo em direÃ§Ã£o aos poÃ§os; B) A expansÃ£o do gÃ¡s acima do Ã³leo aumenta a viscosidade; C) PoÃ§os artificiais elevam a pressÃ£o; D) O Ã³leo condensado impede a produÃ§Ã£o de Ã¡gua; E) A saturaÃ§Ã£o irreductÃ­vel de Ã³leo Ã© zero.
9. A produÃ§Ã£o de Ã³leo em um reservatÃ³rio undersaturated depende principalmente de: A) PressÃ£o inicial do reservatÃ³rio e mobilidade do Ã³leo; B) ExpansÃ£o do gÃ¡s acima do Ã³leo; C) InjeÃ§Ã£o de Ã¡gua ou gÃ¡s; D) FormaÃ§Ã£o de condensado; E) ElevaÃ§Ã£o artificial exclusivamente.
10. O que caracteriza um reservatÃ³rio com gasâ€‘cap drive? A) GÃ¡s livre no topo do reservatÃ³rio que ajuda a manter a pressÃ£o; B) Ãgua injetada artificialmente para suporte de pressÃ£o; C) Ã“leo pesado nÃ£o fluido; D) ProduÃ§Ã£o apenas de condensado lÃ­quido; E) ReservatÃ³rio totalmente saturado sem gÃ¡s.

Tarefas e afirmaÃ§Ãµes adicionais (Ãºteis para V/F):
- Explique a diferenÃ§a entre Sistema de ProduÃ§Ã£o, Sistema PetrolÃ­fero e cadeia produtiva.
- Investigue teorias sobre a origem dos hidrocarbonetos e indique a mais aceita.
- Defina a Ã¡rea de atuaÃ§Ã£o do Engenheiro de ReservatÃ³rios.
- Complete: HIDROCARBONETOS + NÃƒO HIDROCARBONETOS = _____________.
- Fundamente respostas corretas/incorrectas dos exercÃ­cios de consolidaÃ§Ã£o (pode virar afirmaÃ§Ãµes de correÃ§Ã£o).
- Perguntas sobre sÃ­mbolos e definiÃ§Ãµes: definiÃ§Ã£o de \(\phi\), S_w, B_o, R_s, etc (transformÃ¡veis em V/F).

---

## 2) DissertaÃ§Ã£o (RedaÃ§Ã£o) â€” CapÃ­tulo 4
(Temas e enunciados extraÃ­dos de Cap.4 â€” escolha 1 como tema de redaÃ§Ã£o tÃ©cnica)

Temas / Enunciados possÃ­veis:
- Incertezas no mÃ©todo volumÃ©trico: fontes, quantificaÃ§Ã£o e mitigaÃ§Ã£o. (IntroduÃ§Ã£o, Desenvolvimento, ConclusÃ£o; discuta P10/P50/P90 e Monte Carlo â€” mÃ¡x. 1 pÃ¡gina.)
- IntegraÃ§Ã£o de dados petrofÃ­sicos e geolÃ³gicos para estimativa de OOIP: estratÃ©gias e principais fontes de erro.
- O papel do Netâ€‘toâ€‘Gross e dos cutâ€‘offs na estimativa volumÃ©trica: impactos e critÃ©rios de seleÃ§Ã£o.
- ComparaÃ§Ã£o entre mÃ©todos volumÃ©trico e material balance para estimativa de reservas: vantagens, limitaÃ§Ãµes e requisitos de dados.
- Plano de QA/QC para dados petrofÃ­sicos (logs, cores, PVT) antes do cÃ¡lculo volumÃ©trico.

Tarefas mais longas (podem virar redaÃ§Ã£o):
- Elaborar um relatÃ³rio curto sobre fontes de incerteza em um caso hipotÃ©tico e propor medidas para reduÃ§Ã£o de risco.
- Descrever uma metodologia prÃ¡tica para quantificar incertezas (ex.: anÃ¡lise de sensibilidade + Monte Carlo) aplicÃ¡vel a um campo hipotÃ©tico.

---

## 3) CÃ¡lculo/prÃ¡tico â€” CapÃ­tulo 2 (PVT / Propriedades dos fluidos)
(Lista de problemas/casos extraÃ­dos de Cap.2 â€” utilizÃ¡veis como enunciados prÃ¡ticos)

Perguntas e exemplos:
- O que Ã© \(B_o\) e por que Ã© importante para o cÃ¡lculo de volumes produzidos? (curta resposta)  
- Como \(R_s\) varia com a pressÃ£o e o que significa atingir o ponto de bolha?  
- Como a viscosidade do Ã³leo influencia a mobilidade e o fator de recuperaÃ§Ã£o?  
- Quando o gÃ¡s pode ser tratado como ideal e quando usar correÃ§Ãµes (Zâ€‘factor)?

Problemas numÃ©ricos / enunciados prÃ¡ticos:
1. Calcule \(B_o\) e \(R_s\) para um ensaio PVT simplificado (caso modelo):  
   - Dados de exemplo jÃ¡ disponÃ­veis: \(V_{res}=1{.}20\) bbl; \(V_{surf}=1{.}00\) STB; \(R_s=400\) scf/STB.  
   - (a) Calcule \(B_o\) em bbl/STB; (b) converta \(R_s\) para m^3/m^3 (use 1 scf = 0.0283168 m^3; 1 STB = 0.1589873 m^3).
2. Tarefa: desenhar envelope de fases para uma mistura Ã³leoâ€‘gÃ¡s e identificar ponto de bolha e ponto de orvalho (pode ser prova prÃ¡tica/descritiva).
3. Problema aplicado: dada uma tabela PVT simplificada, calcule curvas \(B_o(p)\), \(R_s(p)\) e discuta implicaÃ§Ãµes para produÃ§Ã£o.
4. ExercÃ­cio de correlaÃ§Ãµes: aplicar uma correlaÃ§Ã£o (Standing, Vazquezâ€‘Beggs) para estimar \(B_o\) quando dados experimentais nÃ£o estÃ£o disponÃ­veis.

---

## 4) CÃ¡lculo/prÃ¡tico â€” CapÃ­tulo 3 (Propriedades de rochas)
(ExercÃ­cios extraÃ­dos do Cap.3 â€” prontos para uso como enunciados de cÃ¡lculo)

Lista de problemas numÃ©ricos:
1. Amostra saturada: massa saturada \(m_{sat}=130\) g; massa seca \(m_{dry}=105\) g; densidade do Ã³leo \(\rho_{oil}=0{.}84\) g/cm^3; volume total \(V_{tot}=180\) cm^3.  
   - (a) Calcule o volume de fluido nos poros \(V_f\) e a porosidade \(\phi\) (%).  
   - (b) Mostre passos e unidades (3 algarismos significativos).
2. Calcular porosidade idealizada em figuras (desenho/esboÃ§o) â€” transformar em questÃ£o prÃ¡tica fornecendo figuras ou descriÃ§Ãµes geomÃ©tricas.
3. Problema de cÃ¢mara de pressÃ£o: Dados \(V_1=100\) cc, \(V_2=100\) cc, \(p_1=15\) psi, \(p_2=60\) psi; apÃ³s abertura, \(p_f=39\) psi. Determinar o volume do grÃ£o da amostra do testemunho.
4. Calcule a porosidade mÃ©dia de amostras com porosidades: 10, 12, 11, 13, 14, 10, 17%.
5. MÃ©todo de ArquÃ­medes: peso seco = 330 g; peso saturado = 360 g; peso aparente em Ã¡gua = 225 g; densidade da Ã¡gua = 1 g/cm^3. Determine porosidade (passos no enunciado).
6. QuestÃµes qualitativas transformÃ¡veis em cÃ¡lculo: definir porosidade total x efetiva; discutir efeitos da compactaÃ§Ã£o; analisar processos diagenÃ©ticos (curta resposta/explicaÃ§Ã£o).

---

### ObservaÃ§Ãµes finais
- O ficheiro acima contÃ©m todas as perguntas/enunciados extraÃ­dos dos capÃ­tulos 1â€“4 disponÃ­veis no diretÃ³rio `Estudar/matÃ©ria`.  
- Posso agora:  
  - (A) Gerar automaticamente um PDF de prova com UMA pergunta por tipo (V/F â€” selecione N afirmaÃ§Ãµes; RedaÃ§Ã£o â€” escolha tema; 2 problemas de cÃ¡lculo),  
  - (B) Gerar um ficheiro PDF com um banco de questÃµes imprimÃ­vel (todas as questÃµes listadas),  
  - (C) Converter as questÃµes V/F de Cap.1 em afirmaÃ§Ãµes curtas prontas para correÃ§Ã£o automÃ¡tica.

Indique qual opÃ§Ã£o prefere (A, B ou C) ou se quer outra montagem do exame.
Perguntas V/F â€” CapÃ­tulo 1

Resumo rÃ¡pido:
Quantidade de questÃµes: 12
Todas as respostas devem ser justificadas.
O CapÃ­tulo 1 apresenta sistemas de produÃ§Ã£o, elementos do sistema petrolÃ­fero (armadilha, rocha geradora, rocha selante), mecanismos de produÃ§Ã£o (water drive, gas-cap, solution gas), e definiÃ§Ãµes bÃ¡sicas como porosidade, permeabilidade e fatores de volume (B_o, R_s).

InstruÃ§Ãµes: Para cada afirmaÃ§Ã£o, marque V (verdadeiro) ou F (falso) e justifique em atÃ© duas linhas.

1. Em reservatÃ³rios leves, a viscosidade do Ã³leo costuma ser menor que em Ã³leos pesados. (V/F)
2. A presenÃ§a de gÃ¡s dissolvido no Ã³leo sempre aumenta a mobilidade do fluido. (V/F)
3. Um mecanismo de water drive mantÃ©m a pressÃ£o do reservatÃ³rio por influxo de Ã¡gua do aquÃ­fero. (V/F)
4. Gasâ€‘cap drive depende da expansÃ£o de gÃ¡s livre acima do Ã³leo para suporte de pressÃ£o. (V/F)
5. O fator de volume de formaÃ§Ã£o $B_o$ relaciona volumes no reservatÃ³rio e na superfÃ­cie. (V/F)
6. A porosidade Ã© a fraÃ§Ã£o volumÃ©trica de vazios no volume total da rocha. (V/F)
7. A permeabilidade Ã© geralmente expressa em Darcy ou mÂ². (V/F)
8. A armadilha geolÃ³gica impede a migraÃ§Ã£o de hidrocarbonetos e permite sua acumulaÃ§Ã£o. (V/F)
9. A saturaÃ§Ã£o irreductÃ­vel de Ã¡gua (Swi) costuma ser zero em todos os reservatÃ³rios. (V/F)
10. A expansÃ£o do gÃ¡s dissolvido no Ã³leo Ã© caracterÃ­stica do mecanismo solution gas drive. (V/F)
11. A gravidade API aumenta quando a densidade especÃ­fica do Ã³leo aumenta. (V/F)
12. Para cÃ¡lculos volumÃ©tricos em unidades de campo, usaâ€‘se o fator 7758 na fÃ³rmula prÃ¡tica de OOIP. (V/F)
# CapÃ­tulo 1 â€” AfirmaÃ§Ãµes V/F (prontas)

Marque V ou F e justifique brevemente.

1. ReservatÃ³rios leves produzem Ã³leo com baixa densidade e alta mobilidade. (V/F)

2. A presenÃ§a de gÃ¡s dissolvido no Ã³leo reduz a viscosidade e aumenta a mobilidade. (V/F)

3. Um water drive mantÃ©m a pressÃ£o do reservatÃ³rio por influxo de Ã¡gua do aquÃ­fero. (V/F)

4. A expansÃ£o do gÃ¡s dissolvido no Ã³leo contribui para a manutenÃ§Ã£o da pressÃ£o no solution gas drive. (V/F)

5. A existÃªncia de um gas cap (camada de gÃ¡s livre) ajuda a manter a pressÃ£o por expansÃ£o do gÃ¡s. (V/F)

6. O ponto de bolha indica a pressÃ£o em que comeÃ§a a aparecer gÃ¡s livre no Ã³leo. (V/F)

7. Netâ€‘toâ€‘Gross nÃ£o afeta a estimativa de OOIP quando a porosidade Ã© conhecida. (V/F)

8. A saturaÃ§Ã£o irreductÃ­vel de Ã¡gua (Swi) reduz o volume de Ã³leo disponÃ­vel. (V/F)

9. A viscosidade do Ã³leo nÃ£o influencia a mobilidade do fluido. (V/F)

10. As fÃ³rmulas prÃ¡ticas de OOIP devem ser aplicadas somente apÃ³s verificar unidades e fatores de conversÃ£o. (V/F)


Justifique cada resposta em uma ou duas linhas abaixo da afirmaÃ§Ã£o.
Perguntas de CÃ¡lculo / PrÃ¡tico â€” CapÃ­tulo 2 (Fluidos e PVT)

Resumo rÃ¡pido:
Quantidade de questÃµes: 10
Todas as respostas devem ser justificadas; mostre cÃ¡lculos quando aplicÃ¡vel.
CapÃ­tulo 2 trata de propriedades dos fluidos (B_o, R_s, viscosidade, Zâ€‘factor), amostragem PVT e uso de equaÃ§Ãµes de estado. As perguntas abaixo focam cÃ¡lculos prÃ¡ticos e conversÃµes comuns em PVT.

1) Ensaio PVT: $V_{res}=1.20$ bbl; $V_{surf}=1.00$ STB; $R_s=400$ scf/STB.
   a) Calcule o fator de volume de formaÃ§Ã£o do Ã³leo $B_o$ (bbl/STB). 
   b) Converta $R_s$ para m^3/m^3 (use 1 scf = 0.0283168 m^3; 1 STB = 0.1589873 m^3).

2) Use a fÃ³rmula prÃ¡tica para OOIP:
   $$OOIP = \frac{7758\,A\,h\,\phi\,(1-S_{wi})}{B_o}$$
   Calcule OOIP para: A = 150 acres; h = 25 ft; Ï† = 0.16; S_wi = 0.20; B_o = 1.10.

3) Convert units: converta 500 scf para m^3 e 2 STB para m^3.

4) Densidade â†’ API: dado Ï_oil = 800 kg/m^3. Calcule o grau API (use Ï_sp = Ï_oil/1000).

5) Problema prÃ¡tico PVT: se um ensaio mostra V_res = 2.40 bbl e V_surf = 2.00 STB, determine B_o.

6) InterpretaÃ§Ã£o/curvas: dado um conjunto simplificado de valores de B_o(p) e R_s(p), descreva qualitativamente o que indica uma queda acentuada de B_o com a pressÃ£o.

7) AplicaÃ§Ã£o de correlaÃ§Ãµes: explique (breve) quando usar uma equaÃ§Ã£o cÃºbica (Pengâ€‘Robinson) em vez de tratar o gÃ¡s como ideal.

8) ConversÃ£o e fator de formaÃ§Ã£o: calcule OGIP (scf) para A = 100 acres, h = 20 ft, Ï† = 0.12, S_wi = 0.25 e B_g = 0.005 m^3/Sm^3 (adapte unidades conforme necessÃ¡rio).

9) Projeto rÃ¡pido: descreva os passos e fÃ³rmulas para calcular B_o a partir de um ensaio CCE (constant composition expansion) com dados simplificados.

10) Erro e unidades: identifique a fonte de erro se alguÃ©m aplicar 7758 com A em m^2 (breve explicaÃ§Ã£o e correÃ§Ã£o).
Perguntas de CÃ¡lculo / PrÃ¡tico â€” CapÃ­tulo 3 (Rochas: porosidade, permeabilidade, compressibilidade)

Resumo rÃ¡pido:
Quantidade de questÃµes: 10
Todas as respostas devem ser justificadas; mostre cÃ¡lculos quando aplicÃ¡vel.
CapÃ­tulo 3 cobre mÃ©todos de mediÃ§Ã£o de porosidade, cÃ¡lculo a partir de massas e volumes, compressibilidade de poros, funÃ§Ã£o de Leverett e tÃ©cnicas de laboratÃ³rio (ArquÃ­medes, porosimetria).

1) Amostra: massa saturada m_sat = 130 g; massa seca m_dry = 105 g; Ï_o = 0.84 g/cm^3; volume total V_t = 180 cm^3.
   a) Calcule o volume de fluido nos poros V_f.
   b) Calcule a porosidade Ï† (em %).

2) MÃ©todo de ArquÃ­medes: m_dry = 330 g; m_sat = 360 g; peso aparente em Ã¡gua m_ap = 225 g; Ï_Ã¡gua = 1 g/cm^3.
   Calcule: V_t, V_p e Ï†.

3) CÃ¢maras conectadas: V1 = 100 cc; V2 = 100 cc; p1 = 15.0 psi; p2 = 60.0 psi; ao abrir a vÃ¡lvula a pressÃ£o final Ã© p_f = 39.0 psi. Determine o volume do grÃ£o (volume sÃ³lido) da amostra do testemunho (sugestÃ£o: usar conservaÃ§Ã£o de massa de ar/gÃ¡s e Boyle ideal para volumes livres).

4) Dados de porosidade: 10, 12, 11, 13, 14, 10, 17 (%). Calcule a porosidade mÃ©dia e o desvio padrÃ£o (passo a passo).

5) Compressibilidade: um volume poroso V_p = 100 cm^3 diminui 0.2 cm^3 quando a pressÃ£o aumenta Î”p = 100 psi. Calcule a compressibilidade efetiva C_f.

6) Permeabilidade relativa: descreva (breve) como a permeabilidade relativa varia com saturaÃ§Ã£o e como isso afeta produÃ§Ã£o.

7) FunÃ§Ã£o de Leverett: escreva a expressÃ£o de J(S_w) e explique como usar J para correlacionar curvas de P_c entre duas amostras de rocha com k e Ï† diferentes (pequena aplicaÃ§Ã£o numÃ©rica opcional).

8) Planejamento experimental: esboce os passos para medir porosidade por pesagem em laboratÃ³rio, indicando fontes potenciais de erro.

9) Dado um testemunho com V_t = 200 cm^3 e V_p = 40 cm^3, calcule Ï† e interprete se a rocha Ã© bem porosa (critÃ©rio: Ï† > 0.1).

10) Breve problema de molhabilidade: dada cosÎ¸ = (Ïƒ_so - Ïƒ_sw)/Ïƒ_wo e valores numÃ©ricos, calcule Î¸ e interprete o comportamento molhante.
QuestÃµes de DissertaÃ§Ã£o / RedaÃ§Ã£o â€” CapÃ­tulo 4 (IntegraÃ§Ã£o de Dados e CÃ¡lculo VolumÃ©trico)

Resumo rÃ¡pido:
Quantidade de questÃµes: 8
Todas as respostas devem ser justificadas (argumente suas escolhas).
CapÃ­tulo 4 discute o mÃ©todo volumÃ©trico, integraÃ§Ã£o de dados petrofÃ­sicos/geolÃ³gicos, anÃ¡lise de incerteza e uso de Monte Carlo para produzir P10/P50/P90. As propostas abaixo sÃ£o temas para redaÃ§Ã£o/dissertaÃ§Ã£o.

1) Discuta as principais fontes de incerteza em uma estimativa volumÃ©trica de OOIP (A, h_net, Ï†, S_wi, B_o). Proponha estratÃ©gias prÃ¡ticas para reduzir cada fonte de incerteza.

2) Descreva um fluxo de trabalho (passo a passo) para aplicar Monte Carlo a um cÃ¡lculo de OOIP; inclua escolha de distribuiÃ§Ãµes, nÃºmero de iteraÃ§Ãµes e como reportar P10/P50/P90.

3) Compare metodicamente o mÃ©todo volumÃ©trico e o mÃ©todo de balanÃ§o de material (material balance) para estimativa de reservas: vantagens, limitaÃ§Ãµes, dados necessÃ¡rios e casos de uso apropriados.

4) Explique como construir mapas de Netâ€‘toâ€‘Gross e A_eff; discuta como escolhas de cutâ€‘off de porosidade/permeabilidade afetam a estimativa de reservas.

5) Discuta a sensibilidade do OOIP a variaÃ§Ãµes em Ï† versus variaÃ§Ãµes em B_o. Use notaÃ§Ã£o matemÃ¡tica/um exemplo numÃ©rico curto para ilustrar.

6) Proponha um plano de QA/QC para dados petrofÃ­sicos usados em cÃ¡lculos volumÃ©tricos (logs, cores, testes PVT). Quais checagens consideraria obrigatÃ³rias?

7) Redija um pequeno relatÃ³rio (1â€“2 pÃ¡ginas) sobre como comunicar risco (P10/P50/P90) para gestores nÃ£oâ€‘tÃ©cnicos, incluindo recomendaÃ§Ãµes visuais e texto.

8) Estudo de caso proposto: descreva as etapas para integrar mapas de espessura, logs e PVT para estimar OGIP/OOIP setorialmente em um campo heterogÃªneo; inclua mÃ©todos de propagaÃ§Ã£o de erro.
# Compressibilidade (fator) Z â€” Cheatsheet extremo

Objetivo: referÃªncia completa e passoâ€‘aâ€‘passo para entender, calcular e aplicar o fator de compressibilidade $Z$ (gÃ¡s real), com mÃ©todos prÃ¡ticos (Standingâ€“Katz, EoS), derivadas Ãºteis e um exemplo numÃ©rico com cÃ³digo Python.

---

**Resumo rÃ¡pido**
- **DefiniÃ§Ã£o:** $Z = \dfrac{p V_m}{R T}$, mede o desvio do gÃ¡s em relaÃ§Ã£o ao gÃ¡s ideal ($Z=1$ ideal).
- **Usos:** converter entre densidade e pressÃ£o/temperatura reais; calcular o fator de volume $B_g$; avaliar compressibilidade isotÃ©rmica do gÃ¡s; PVT e balanÃ§o de massas.

---

**1) FormulaÃ§Ã£o e relaÃ§Ãµes bÃ¡sicas**

- Molar volume: $V_m = \dfrac{Z R T}{p}$.  
- Densidade (massa): $\rho = \dfrac{M p}{Z R T}$, onde $M$ Ã© massa molar (kgÂ·mol^{-1}).
- Fator de volume do gÃ¡s (molar): $B_{m} = V_m = \dfrac{Z R T}{p}$. (Em reservatÃ³rios usaâ€‘se versÃµes por massa/por scf â€” adaptar unidades.)

**2) RelaÃ§Ã£o com compressibilidade isotÃ©rmica do gÃ¡s $c_g$**

Partindo de $V_m = Z R T / p$ e definindo $c_g = -\dfrac{1}{V_m} \left( \dfrac{\partial V_m}{\partial p} \right)_T$ obtÃ©mâ€‘se:

$$
c_g \,=\, \frac{1}{p} \, - \, \frac{1}{Z} \left(\frac{\partial Z}{\partial p}\right)_T \,=\, \frac{1}{p} \, - \, \frac{\partial \ln Z}{\partial p} .
$$

InterpretaÃ§Ã£o prÃ¡tica: para gÃ¡s quase ideal $\partial Z/\partial p \approx 0$ e $c_g\approx 1/p$. O termo com $\partial Z/\partial p$ corrige o comportamento real; portanto Ã© importante para pressÃµes altas / nÃ£oâ€‘ideais.

**3) MÃ©todos para obter $Z$ (ordem de complexidade e precisÃ£o)**

- Leitura direta no grÃ¡fico Standingâ€“Katz (rÃ¡pido; precisa dos pseudoâ€‘crÃ­ticos do gÃ¡s).  
- CorrelaÃ§Ãµes empÃ­ricas e semiâ€‘empÃ­ricas (ex.: Dranchukâ€“Abouâ€‘Kassem) â€” boas para implementaÃ§Ã£o numÃ©rica.  
- EquaÃ§Ãµes de estado cÃºbicas (Pengâ€“Robinson, Soaveâ€“Redlichâ€“Kwong) â€” recomendadas quando se tem composiÃ§Ã£o e se precisa de consistÃªncia em fase lÃ­quida/vapor; permitem calcular Z e derivadas termodinÃ¢micas.

**4) PseudocrÃ­ticos e preparaÃ§Ã£o (howâ€‘to)**

Para usar chart ou correlaÃ§Ãµes reduzidas, calcule $T_{pc}$ e $P_{pc}$ da mistura. Duas rotas:

- Regra de Kay (mistura):  
  - para cada componente i obtenha $T_{c,i}$ e $P_{c,i}$ (temperaturas Kelvin, pressÃ£o em Pa).  
  - calcule $T_{pc} = \sum_i y_i \, T_{c,i}$ e $P_{pc} = \sum_i y_i \, P_{c,i}$ (mole fractions $y_i$).  
  - entÃ£o $T_r = T / T_{pc}$ e $P_r = p / P_{pc}$.  

- CorreÃ§Ãµes para gÃ¡s Ã¡cido / CO2/H2S (Wichertâ€“Aziz): existem procedimentos para reduzir $T_{pc}$ e $P_{pc}$ quando fraÃ§Ãµes significativas de CO2/H2S estiverem presentes â€” aplicar se $\mathrm{CO_2}+\mathrm{H_2S}$ > ~2â€“5\% mole.

Com $T_r$ e $P_r$ vocÃª lÃª $Z$ no grÃ¡fico de Standingâ€“Katz (curvas $Z$ vs $P_r$ para cada $T_r$). Para automaÃ§Ã£o prefira correlaÃ§Ãµes numÃ©ricas (Dranchukâ€“Abouâ€‘Kassem) ou uma EoS.

**5) MÃ©todo robusto: Pengâ€“Robinson (PR) â€” passo a passo (PadrÃ£o industrial)**

ParÃ¢metros do PR (unidades SI):

$$
a = 0.45724 \frac{R^2 T_c^2}{P_c},\qquad b = 0.07780 \frac{R T_c}{P_c}
$$

onde $R=8.314462618$ JÂ·mol^{-1}Â·K^{-1}, $T_c$ (K), $P_c$ (Pa). O fator $\alpha$ descreve dependÃªncia com $T$:

$$
\kappa = 0.37464 + 1.54226\,\omega - 0.26992\,\omega^2,\qquad
\alpha(T) = \left(1 + \kappa \left(1-\sqrt{\dfrac{T}{T_c}}\right)\right)^2
$$

Defina entÃ£o:

$$
A = \dfrac{a\,\alpha(T)\,p}{R^2 T^2},\qquad B = \dfrac{b p}{R T}.
$$

O polinÃ´mio cÃºbico em $Z$ (forma padrÃ£o PR):

$$
Z^3 - (1 - B) Z^2 + (A - 3B^2 - 2B) Z - (A B - B^2 - B^3) = 0.
$$

SoluÃ§Ã£o: encontre as raÃ­zes reais; para fase gasosa escolha a maior raiz real (maior $Z$).

**6) Exemplo numÃ©rico completo (CH4 puro)**

Dados (SI):
- $T = 350\ \mathrm{K}$ (exemplo)
- $p = 5\ \mathrm{MPa} = 5\times10^6\ \mathrm{Pa}$
- Metano: $T_c = 190.564\ \mathrm{K}$, $P_c = 4.5992\times10^6\ \mathrm{Pa}$, $\omega\approx0.011$.

1) Calcule $a,b$:

$$
a \approx 0.45724\dfrac{R^2 T_c^2}{P_c} \approx 0.2498\quad(\mathrm{SI})
$$
$$
b \approx 0.07780\dfrac{R T_c}{P_c} \approx 2.68\times10^{-5}\ \mathrm{m^3\,mol^{-1}}
$$

2) $\kappa\approx 0.3916$, $\alpha\approx 0.7396$ (usar fÃ³rmula acima).

3) $A\approx 0.1089$, $B\approx 0.0460$ (ver cÃ¡lculos no script abaixo).

4) Monta o cÃºbico e resolve: obtÃ©m $Z\approx 0.948$ (raiz gasosa principal).

InterpretaÃ§Ã£o: $Z<1$ porÃ©m prÃ³ximo de 1 â€” desvio moderado para estas condiÃ§Ãµes.

**7) Compressibilidade isotÃ©rmica calculada numericamente (exemplo)**

Procedimento prÃ¡tico (numÃ©rico):
1. Calcule $Z(p)$ com o mÃ©todo EoS (PR) no ponto $p$ (aqui 5 MPa).
2. Calcule $Z(p+\Delta p)$ com $\,\Delta p$ pequeno (ex.: $10^4$â€“$10^5\ \mathrm{Pa}$).  
3. Estime $\partial Z/\partial p \approx (Z(p+\Delta p)-Z(p))/\Delta p$.  
4. Use $c_g = 1/p - (1/Z) (\partial Z/\partial p)$.

Usando o exemplo numÃ©rico (valores aproximados do passo anterior e $\Delta p=10^5\ \mathrm{Pa}$) obtemos $c_g\approx 2.19\times10^{-7}\ \mathrm{Pa^{-1}}$ que corresponde a $0.219\ \mathrm{MPa^{-1}}$ ou aproximadamente $1.51\times10^{-3}\ \mathrm{psi^{-1}}$ (conversÃµes mostradas no script).

**8) CÃ³digo Python (PR EoS) â€” cÃ¡lculo de Z e compressibilidade por diferenÃ§a finita**

Instalar dependÃªncia mÃ­nima: `pip install numpy`

```python
import numpy as np

R = 8.314462618

def Z_PR(p, T, Tc, Pc, omega):
    # p in Pa, T in K, Tc in K, Pc in Pa
    a = 0.45724 * R**2 * Tc**2 / Pc
    b = 0.07780 * R * Tc / Pc
    kappa = 0.37464 + 1.54226*omega - 0.26992*omega**2
    alpha = (1 + kappa*(1 - np.sqrt(T/Tc)))**2
    A = a * alpha * p / (R**2 * T**2)
    B = b * p / (R * T)
    # Coeffs cubic: Z^3 - (1-B) Z^2 + (A - 3B^2 - 2B) Z - (A B - B^2 - B^3) = 0
    coeffs = [1.0, -(1 - B), (A - 3*B*B - 2*B), -(A*B - B*B - B*B*B)]
    roots = np.roots(coeffs)
    real_roots = np.real(roots[np.isclose(roots.imag, 0, atol=1e-8)])
    if len(real_roots) == 0:
        raise RuntimeError('No real root found for Z')
    # gas root = largest real root
    Z = np.max(real_roots)
    return float(Z)

def gas_compressibility(p, T, Tc, Pc, omega, dp=1e5):
    Z1 = Z_PR(p, T, Tc, Pc, omega)
    Z2 = Z_PR(p + dp, T, Tc, Pc, omega)
    dZdp = (Z2 - Z1) / dp
    c_g = 1.0/p - (1.0/Z1)*dZdp
    return Z1, dZdp, c_g

if __name__ == '__main__':
    # Example: methane at p=5 MPa, T=350 K
    Tc = 190.564
    Pc = 4.5992e6
    omega = 0.011
    p = 5e6
    T = 350.0
    Z, dZdp, cg = gas_compressibility(p, T, Tc, Pc, omega, dp=1e5)
    print('Z =', Z)
    print('dZ/dp =', dZdp, 'Pa^-1')
    print('c_g =', cg, 'Pa^-1 (', cg*1e6, 'MPa^-1 )')
```

SaÃ­da esperada aproximada (exemplo que usamos manualmente): `Z â‰ˆ 0.948`, `c_g â‰ˆ 2.19e-7 Pa^-1`.

**9) RecomendaÃ§Ãµes prÃ¡ticas e atenÃ§Ã£o a unidades**

- Sempre usar unidades consistentes (SI: Pa, K, J/(molÂ·K)). Para conversÃµes (psi, Â°R) ajuste constantes do gÃ¡s.  
- Para misturas use regras de mistura apropriadas (EoS: combinaÃ§Ãµes de `a_{ij}`/fatores de interaÃ§Ã£o). Se nÃ£o conhecer os coeficientes binÃ¡rios use $k_{ij}=0$ como primeira aproximaÃ§Ã£o (pode introduzir erro).  
- Para trabalho de campo rÃ¡pido: calculadoras com Standingâ€“Katz (chart) ou correlaÃ§Ã£o DAK. Para simulaÃ§Ã£o/reconhecimento e prognÃ³stico, prefira EoS com mistura.

**10) ReferÃªncias rÃ¡pidas**

- Standing, M. B., Katz, D. L. â€” grÃ¡fico Standingâ€“Katz para $Z$ (uso clÃ¡ssico).  
- Dranchuk, P. M. & Abouâ€‘Kassem, J. H. (1975) â€” correlaÃ§Ã£o numÃ©rica para $Z$ (boa para automaÃ§Ã£o).  
- Peng, D.-Y. & Robinson, D. B. (1976) â€” Pengâ€“Robinson EoS (cÃºbica), uso industrial.  
- Wichert, D. & Aziz, K. (1972) â€” correÃ§Ã£o pseudoâ€‘crÃ­tica para CO2/H2S (gases Ã¡cidos).

---

Se quiser, eu:
- gero uma versÃ£o com figuras (Standingâ€“Katz) e tabela de propriedades crÃ­ticas;  
- adiciono uma implementaÃ§Ã£o DAK (Dranchukâ€“Abouâ€‘Kassem) completa em Python;  
- aplico o cÃ¡lculo a uma mistura real (envie composiÃ§Ã£o molar) e salvo o resultado.
# DissertaÃ§Ã£o â€” CapÃ­tulo 4

**Tema:** Incertezas no mÃ©todo volumÃ©trico: fontes, quantificaÃ§Ã£o e mitigaÃ§Ã£o

**IntroduÃ§Ã£o.**
O mÃ©todo volumÃ©trico Ã© a base inicial para estimativas de volumes originalmente em lugar (OOIP/OGIP) e, por isso, a compreensÃ£o e a gestÃ£o das suas incertezas sÃ£o essenciais para decisÃµes de exploraÃ§Ã£o e desenvolvimento. A incerteza deriva de variabilidade geolÃ³gica, limitaÃ§Ãµes de mediÃ§Ã£o e escolhas metodolÃ³gicas; a prÃ¡tica robusta combina QA/QC de dados, anÃ¡lise determinÃ­stica e probabilÃ­stica para produzir estimativas utilizÃ¡veis em engenharia.

**Desenvolvimento.**
As fontes principais de incerteza incluem: (i) geometria do reservatÃ³rio (Ã¡rea $A$, espessura neta $h$ e Netâ€‘toâ€‘Gross), (ii) propriedades petrofÃ­sicas ($\phi$, $S_w$) e (iii) parÃ¢metros PVT ($B_o$, $R_s$, $B_g$). Uma forma prÃ¡tica de ver o problema Ã© pela fÃ³rmula clÃ¡ssica:

$$
OOIP = \frac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}
$$

Pequenas variaÃ§Ãµes relativas em $A$, $h$ ou $\phi$ propagamâ€‘se linearmente para o $OOIP$, enquanto erros em $B_o$ tÃªm efeito inverso. AlÃ©m disso, a heterogeneidade lateral/vertical e escolhas de cutâ€‘off para definir pay podem introduzir viÃ©s sistemÃ¡tico.

Para quantificar incertezas recomendaâ€‘se um fluxo em dois nÃ­veis: (1) anÃ¡lises de sensibilidade univariada para identificar parÃ¢metros crÃ­ticos; (2) simulaÃ§Ãµes probabilÃ­sticas (Monte Carlo ou Latin Hypercube) para gerar distribuiÃ§Ãµes de saÃ­da (P10/P50/P90). Complementos Ãºteis incluem anÃ¡lise de cenÃ¡rio (melhor/pior caso) e bootstrap sobre amostras de core/log para estimar erro amostral.

Medidas de mitigaÃ§Ã£o prÃ¡ticas: fortalecer o QA/QC (calibraÃ§Ã£o coreâ†”logâ†”PVT), aumentar amostragem representativa nas zonas mais incertas, usar correlaÃ§Ã£o estatÃ­stica entre variÃ¡veis (p.ex. $\phi$ vs N/G) e aplicar modelagem geoestatÃ­stica para propagar variabilidade espacial. IntegraÃ§Ã£o com mÃ©todos independentes (material balance, ajuste de produÃ§Ã£o e declÃ­nio) permite validar e restringir estimativas volumÃ©tricas.

**ConclusÃ£o.**
Gerenciar incertezas no mÃ©todo volumÃ©trico exige uma abordagem integrada: identificar parÃ¢metros sensÃ­veis, quantificÃ¡â€‘los com simulaÃ§Ã£o probabilÃ­stica e reduzir incerteza com QA/QC, amostragens adicionais e integraÃ§Ã£o de mÃ©todos. Ao combinar anÃ¡lises determinÃ­sticas (sensibilidade) e probabilÃ­sticas (Monte Carlo) com validaÃ§Ã£o operacional (material balance), obtÃ©mâ€‘se estimativas mais robustas e decisÃµes de desenvolvimento menos arriscadas.
# RevisÃ£o para a prova â€” Gabarito e Rubricas

Este ficheiro reÃºne as 4 questÃµes propostas para a prova, as respostasâ€‘gabarito e as rubricas de correÃ§Ã£o.

---

## QuestÃ£o 1 â€” Verdadeiro ou Falso (CapÃ­tulo 1)

Enunciado (10 itens, 1 pt cada):
1) A armadilha geolÃ³gica impede a migraÃ§Ã£o de hidrocarbonetos e permite sua acumulaÃ§Ã£o.
2) Rocha geradora Ã© caracterizada por baixa matÃ©ria orgÃ¢nica.
3) Rocha selante tem alta permeabilidade e facilita o fluxo de fluidos.
4) MigraÃ§Ã£o de hidrocarbonetos ocorre preferencialmente por meios porosos e fraturados.
5) Sincronismo (coincidÃªncia temporal de processos) Ã© irrelevante para a formaÃ§Ã£o de um sistema petrolÃ­fero.
6) CatagÃªnese refereâ€‘se ao craqueamento tÃ©rmico do querogÃªnio em hidrocarbonetos.
7) O sistema de produÃ§Ã£o inclui instalaÃ§Ãµes de coleta, elevaÃ§Ã£o e separaÃ§Ã£o atÃ© a superfÃ­cie.
8) Em um gasâ€‘cap drive, o gÃ¡s livre contribui para manter a pressÃ£o do reservatÃ³rio.
9) Porosidade e permeabilidade sÃ£o a mesma propriedade fÃ­sica.
10) O fator de volume de formaÃ§Ã£o `B_o` relaciona volumes em reservatÃ³rio ao volume na superfÃ­cie.

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
- Se for solicitada justificativa: aceitar 1â€“2 frases; atribuir 0.5 pt para justificativa parcial.

---

## QuestÃ£o 2 â€” DissertaÃ§Ã£o (CapÃ­tulo 4)

Enunciado:
Redija uma dissertaÃ§Ã£o (â‰ˆ 400â€“600 palavras) que responda e discuta:
- Descreva o mÃ©todo volumÃ©trico para estimativa de OOIP/OGIP e os principais parÃ¢metros envolvidos (`A`, `h`, `\phi`, `S_w`, `B_o`, `B_g`).
- Explique as principais fontes de incerteza (cutâ€‘offs, N/G, heterogeneidade, PVT) e como afetam a estimativa.
- Proponha um fluxo de trabalho prÃ¡tico para integrar mapas de net, dados de core, logs e PVT para obter uma estimativa com P10/P50/P90 (mencione Monte Carlo).
- Conclua com recomendaÃ§Ãµes para comunicar risco e medidas para reduzir incerteza (QA/QC, aquisiÃ§Ã£o de dados adicionais, sensibilidade).

### Rubrica Q2 (30 pts)
- MÃ©todo volumÃ©trico e parÃ¢metros (12 pts): fÃ³rmula prÃ¡tica (ex.: $$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}$$), explicaÃ§Ã£o de cada termo, menÃ§Ã£o a unidades campo vs SI. (12 pts)
- Fontes de incerteza (8 pts): identificaÃ§Ã£o e explicaÃ§Ã£o do impacto de cutâ€‘offs, N/G, heterogeneidade, erros PVT. (8 pts)
- Fluxo de trabalho prÃ¡tico (6 pts): integraÃ§Ã£o cores/logs/PVT, construÃ§Ã£o de mapas, cÃ¡lculo setorial, sensibilidade e Monte Carlo para P10/P50/P90. (6 pts)
- ComunicaÃ§Ã£o de risco e recomendaÃ§Ãµes (4 pts): QA/QC, aquisiÃ§Ã£o adicional, apresentaÃ§Ã£o de Pxx e mitigaÃ§Ã£o. (4 pts)

CritÃ©rios de avaliaÃ§Ã£o:
- ConteÃºdo tÃ©cnico: 60% dos pontos.
- Metodologia/prÃ¡tica: 20%.
- ComunicaÃ§Ã£o/clareza e recomendaÃ§Ãµes: 20%.

---

## QuestÃ£o 3 â€” CÃ¡lculo / PrÃ¡tico (CapÃ­tulo 2 â€” PVT)

Enunciado:
Um ensaio PVT fornece os seguintes resultados para 1 STB de Ã³leo amostrado: volume no estado de reservatÃ³rio $V_{res}=1.20\,$bbl; volume correspondente Ã  superfÃ­cie $V_{surf}=1.00\,$STB; gÃ¡s libertado no ensaio $R_s=400\,$scf/STB.

a) Calcule o fator de volume de formaÃ§Ã£o `B_o` (bbl/STB) usando $B_o=V_{res}/V_{surf}$.

b) Expresse `R_s` em mÂ³/mÂ³ usando $1\,\text{scf}=0.0283168\,\text{m}^3$ e $1\,\text{STB}=0.1589873\,\text{m}^3$.

c) Interprete fisicamente um $B_o>1$ e discuta brevemente como $R_s$ influencia o comportamento de produÃ§Ã£o.

### Gabarito Q3 (30 pts â€” 10/10/10)
(a) $$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ (10 pts)

(b) ConversÃ£o: $$R_s\,\text{(m}^3/\text{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\text{m}^3/\text{m}^3.$$ (10 pts)

(c) InterpretaÃ§Ã£o: (10 pts)
- $B_o>1$ indica que 1 STB Ã  superfÃ­cie corresponde a mais de 1 bbl nas condiÃ§Ãµes de reservatÃ³rio (efeito de compressibilidade e/ou gÃ¡s dissolvido); volumes no reservatÃ³rio sÃ£o maiores que o volume final surfacel.
- $R_s$ alto implica presenÃ§a significativa de gÃ¡s dissolvido; durante declÃ­nio de pressÃ£o, se atingir o ponto de bolha, o gÃ¡s Ã© liberado, alterando mobilidade do fluido, afetando recuperaÃ§Ã£o e mecanismo de produÃ§Ã£o. Pontos por clareza e ligaÃ§Ã£o a efeitos operacionais.

---

## QuestÃ£o 4 â€” CÃ¡lculo / PrÃ¡tico (CapÃ­tulo 3 â€” Rocha)

Enunciado:
a) Porosidade por mÃ©todo de massa: uma amostra tem massa seca $m_{dry}=250\,$g e massa saturada $m_{sat}=290\,$g; densidade do fluido $\rho_f=0.90\,$g/cmÂ³; volume total da amostra $V_t=320\,$cmÂ³. Calcule a porosidade $\phi$ (use $V_p=(m_{sat}-m_{dry})/\rho_f$ e $\phi=V_p/V_t$).

b) Permeabilidade (Darcy): num ensaio de bancada obteveâ€‘se vazÃ£o volumÃ©trica $q=1.0\times10^{-6}\,\text{m}^3/s$, Ã¡rea da amostra $A=10\,\text{cm}^2=1.0\times10^{-3}\,\text{m}^2$, comprimento $L=5\,\text{cm}=0.05\,\text{m}$, viscosidade $\mu=1.0\,\text{cP}=0.001\,\text{PaÂ·s}$ e queda de pressÃ£o $\Delta p=10{,}000\,$Pa. Calcule `k` em mÂ² e converta para Darcy (1 D = 9.869233Ã—10â»Â¹Â³ mÂ²) usando a relaÃ§Ã£o:
$$k=\dfrac{q\,\mu\,L}{A\,\Delta p}$$

### Gabarito Q4 (30 pts â€” 15/15)
(a) Porosidade (15 pts):
- $$V_p=\dfrac{m_{sat}-m_{dry}}{\rho_f}=\dfrac{290-250}{0.90}=\dfrac{40}{0.90}=44.444\;\text{cm}^3.$$ 
- $$\phi=\dfrac{V_p}{V_t}=\dfrac{44.444}{320}\approx0.1389\approx13.9\%. $$
(atribuir parcial se passos corretos; tolerÃ¢ncia Â±0.2â€“0.5% absoluta)

(b) Permeabilidade (15 pts):
- Aplicando Darcy:
  $$k=\dfrac{1\times10^{-6}\times0.001\times0.05}{1\times10^{-3}\times10{,}000}=5\times10^{-12}\;\text{m}^2.$$ 
- Converter para Darcy:
  $$k_{D}=\dfrac{5\times10^{-12}}{9.869233\times10^{-13}}\approx5.07\;\text{D}=5\,070\;\text{mD}.$$ 
(Aceitar pequenas variaÃ§Ãµes por arredondamento; exigir todas as conversÃµes)

---

## PontuaÃ§Ã£o total sugerida
- Q1: 10 pts
- Q2: 30 pts
- Q3: 30 pts
- Q4: 30 pts

Total: 100 pts.

## ObservaÃ§Ãµes finais sobre correÃ§Ã£o
- Para cÃ¡lculos, exigir passos e unidades; penalizar falta de conversÃµes ou unidades incoerentes.
- Para dissertaÃ§Ã£o, pontuar conteÃºdo tÃ©cnico, metodologia e clareza.
- Para todos os itens, aceitar pequenas variaÃ§Ãµes numÃ©ricas quando justificadas por arredondamento.

---

*Arquivo gerado automaticamente pelo assistente.*
# ExercÃ­cios Resolvidos â€” Engenharia de ReservatÃ³rios I

CompilaÃ§Ã£o de soluÃ§Ãµes passoâ€‘aâ€‘passo extraÃ­das dos ficheiros em `Estudar/matÃ©ria` (cap1â€“cap5). Use como referÃªncia rÃ¡pida para estudo; ver ficheiros de origem para enunciados completos.

---

## CapÃ­tulo 1 â€” Exemplo rÃ¡pido (OOIP)
Dados: Ãrea = 100 acres; $h=20\,$ft; $\phi=0.15$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

FÃ³rmula prÃ¡tica:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_{wi})}{B_o}$$

CÃ¡lculo passo a passo:
\begin{align*}
7758\times100&=775\,800\\
775\,800\times20&=15\,516\,000\\
15\,516\,000\times0.15&=2\,327\,400\\
2\,327\,400\times0.75&=1\,745\,550\\
OOIP&=\dfrac{1\,745\,550}{1.2}\approx1\,454\,625\;\text{STB}
\end{align*}

Resultado: â‰ˆ1.455Ã—10^6 STB.

---

## CapÃ­tulo 2 â€” PVT: cÃ¡lculo de $B_o$ e conversÃ£o de $R_s$
Enunciado (exemplo): 1 STB amostrado dÃ¡ $V_{res}=1.20\,$bbl, $V_{surf}=1.00\,$STB; $R_s=400\,$scf/STB.

1) $B_o$:
$$B_o=\dfrac{V_{res}}{V_{surf}}=\dfrac{1.20}{1.00}=1.20\;\text{bbl/STB}.$$ 

2) ConversÃ£o de $R_s$ para m^3/m^3 (opcional):
1 scf = 0.0283168 m^3; 1 STB = 0.1589873 m^3.
$$R_s(\mathrm{m}^3/\mathrm{m}^3)=\dfrac{400\times0.0283168}{0.1589873}\approx71.3\;\mathrm{m}^3/\mathrm{m}^3.$$ 

InterpretaÃ§Ã£o: $B_o>1$ indica expansÃ£o/volume maior em reservatÃ³rio por unidade de superfÃ­cie; $R_s$ alto = muito gÃ¡s dissolvido.

---

## CapÃ­tulo 3 â€” Rochas: porosidade (massa e ArquÃ­medes)

### Exemplo 1 (ExercÃ­cio 1)
Dados: $m_{sat}=130\,$g; $m_{dry}=105\,$g; $\rho_o=0.84\,$g/cm^3; $V_t=180\,$cm^3.

1) Volume de fluido nos poros:
$$V_f=\dfrac{m_{sat}-m_{dry}}{\rho_o}=\dfrac{130-105}{0.84}=\dfrac{25}{0.84}\approx29.7619\;\text{cm}^3.$$ 

2) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{29.7619}{180}\approx0.16534\approx16.53\%.$$ 

### Exemplo 2 (mÃ©todo de ArquÃ­medes â€” ExercÃ­cio 5)
Dados: $m_{dry}=330\,$g; $m_{sat}=360\,$g; $m_{ap\_agua}=225\,$g; $\rho_{agua}=1\,$g/cm^3.

1) Volume total via empuxo:
$$V_t=\dfrac{m_{sat}-m_{ap\_agua}}{\rho_{agua}}=\dfrac{360-225}{1}=135\;\text{cm}^3.$$ 

2) Volume poroso:
$$V_p=m_{sat}-m_{dry}=360-330=30\;\text{cm}^3.$$ 

3) Porosidade:
$$\phi=\dfrac{V_p}{V_t}=\dfrac{30}{135}\approx0.22222\approx22.22\%.$$

ObservaÃ§Ã£o: indicar unidades e arredondamentos no relatÃ³rio final.

---

## CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico (ExercÃ­cio 4.8 â€” OOIP)
Dados: $A=200\,$acres; $h_{net}=30\,$ft; $\phi=0.18$; $S_{wi}=0.25$; $B_o=1.2\,$bbl/STB.

FÃ³rmula:
$$OOIP=\dfrac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}.$$ 

CÃ¡lculo:
\begin{align*}
7758\times200&=1\,551\,600\\
1\,551\,600\times30&=46\,548\,000\\
46\,548\,000\times0.18&=8\,378\,640\\
8\,378\,640\times0.75&=6\,283\,980\\
OOIP&=\dfrac{6\,283\,980}{1.2}\approx5\,236\,650\;\text{STB}.
\end{align*}

Resultado: â‰ˆ5.24Ã—10^6 STB.

---

## CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (Havlena & Odeh)

### Exemplo (cÃ¡lculo do termo $E_o$)
Dados ilustrativos: $B_{o,i}=1.10$, $B_o=1.15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0.005$.

FÃ³rmula:
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$

CÃ¡lculo:
$$E_o = 1.15 - 1.10 + (200-180)\times0.005 = 0.05 + 20\times0.005 = 0.05 + 0.10 = 0.15.$$ 

Uso: repita para cada data (pressÃ£o) e monte a regressÃ£o linear $F= N E_o + m E_g + (1+m)E_{f,w} + W_e$ para estimar $N$ e $m$.

---

## ObservaÃ§Ãµes finais
- Este ficheiro agrupa exemplos resolvidos presentes nas notas (cap1â€“cap5). Para exercÃ­cios completos e figuras, consulte os ficheiros originais em `Estudar/matÃ©ria`.
- Se quiser, posso:
  - adicionar soluÃ§Ãµes passoâ€‘aâ€‘passo para TODOS os exercÃ­cios listados nos capÃ­tulos (criando uma secÃ§Ã£o por nÃºmero de exercÃ­cio), ou
  - gerar um PDF/LaTeX com este compÃªndio.

---

*Ficheiro gerado automaticamente pelo assistente.*

---

## SoluÃ§Ãµes adicionais completas â€” CapÃ­tulos 1â€“5

A seguir estÃ£o as soluÃ§Ãµes passoâ€‘aâ€‘passo para as perguntas listadas nas secÃ§Ãµes de consolidaÃ§Ã£o e tarefas dos CapÃ­tulos 1 a 5. Para problemas descritivos forneÃ§o uma respostaâ€‘modelo; para exercÃ­cios numÃ©ricos apresento cÃ¡lculos explÃ­citos e resultados.

### CapÃ­tulo 1 â€” Respostas e justificaÃ§Ãµes (ConsolidaÃ§Ã£o)
1) **B** â€” Baixa densidade e alta mobilidade.
  - JustificaÃ§Ã£o: Ã³leo leve tem menor densidade e viscosidade, o que aumenta a mobilidade relativa e facilita o escoamento.

2) **A** â€” Reduz a pressÃ£o do reservatÃ³rio e facilita o fluxo de Ã³leo.
  - JustificaÃ§Ã£o: a presenÃ§a de gÃ¡s (dissolvido ou livre) altera o comportamento volumÃ©trico e pode gerar mecanismos de drive (solution gas, gasâ€‘cap) que afetam a pressÃ£o e a mobilidade do Ã³leo.

3) **A** â€” ManutenÃ§Ã£o da pressÃ£o por influxo de Ã¡gua do aquÃ­fero.
  - JustificaÃ§Ã£o: water drive Ã© caracterizado pelo suporte de pressÃ£o fornecido pelo aquÃ­fero que desloca Ã³leo para os poÃ§os.

4) **A** â€” A taxa de fluxo pelo reservatÃ³rio.
  - JustificaÃ§Ã£o: a mobilidade Ã© proporcional a $1/\mu$; aumentos de viscosidade reduzem caudal para a mesma diferenÃ§a de pressÃ£o.

5) **A** â€” MantÃ©m pressÃ£o por expansÃ£o de gÃ¡s acima do Ã³leo.
  - JustificaÃ§Ã£o: gasâ€‘cap drive usa a expansÃ£o do gÃ¡s livre para suportar pressÃ£o de reservatÃ³rio.

6) **A** â€” O condensado separaâ€‘se do gÃ¡s Ã  medida que a pressÃ£o diminui.
  - JustificaÃ§Ã£o: condensado aparece quando a condiÃ§Ã£o de orvalho Ã© atingida e parte do gÃ¡s condensa em fase lÃ­quida.

7) **E** â€” (nÃ£o define).  
  - ExplicaÃ§Ã£o: as caracterÃ­sticas Aâ€“D sÃ£o diretamente associadas ao solutionâ€‘gas drive; a expressÃ£o "produÃ§Ã£o contÃ­nua de Ã³leo" nÃ£o Ã© uma definiÃ§Ã£o intrÃ­nseca do mecanismo (a produÃ§Ã£o pode declinar com a queda de pressÃ£o), portanto Ã© a alternativa que NÃƒO define o mecanismo.

8) **A** â€” A Ã¡gua do aquÃ­fero desloca o Ã³leo em direÃ§Ã£o aos poÃ§os.

9) **A** â€” PressÃ£o inicial do reservatÃ³rio e mobilidade do Ã³leo.
  - JustificaÃ§Ã£o: em reservatÃ³rios undersaturated a produÃ§Ã£o depende da pressÃ£o acima do ponto de bolha e da mobilidade do Ã³leo.

10) **A** â€” GÃ¡s livre no topo do reservatÃ³rio que ajuda a manter a pressÃ£o.

---

### CapÃ­tulo 2 â€” Propriedades dos fluidos (respostasâ€‘modelo)
- O que Ã© $B_o$ e por que Ã© importante:
  - $B_o$ Ã© o fator de volume de formaÃ§Ã£o do Ã³leo: $B_o=V_{res}/V_{surf}$. Ã‰ usado para converter volumes no reservatÃ³rio para volumes de superfÃ­cie (STB) e Ã© essencial em balanÃ§os de massa e estimativas de reservas.

- Como $R_s$ varia com pressÃ£o e significado do ponto de bolha:
  - Geralmente $R_s$ diminui com a reduÃ§Ã£o de pressÃ£o; ao atingir o ponto de bolha surge gÃ¡s livre e $R_s$ passa a ser o valor mÃ¡ximo de gÃ¡s dissolvido na condiÃ§Ã£o dada.

- Efeito da viscosidade do Ã³leo na mobilidade:
  - Mobilidade dinÃ¢mica $\\lambda = k/\\mu$; viscosidade maior reduz mobilidade e diminui vazÃµes para um mesmo gradiente de pressÃ£o.

- Quando tratar o gÃ¡s como ideal vs real:
  - Use o modelo ideal quando as condiÃ§Ãµes estiverem longe do crÃ­tico (pressÃµes relativamente baixas e temperaturas altas); para pressÃµes elevadas/temperaturas baixas use fator $Z$ (grÃ¡ficos de Standing & Katz) ou equaÃ§Ãµes de estado cÃºbicas (Pengâ€‘Robinson, SRK).

---

### CapÃ­tulo 3 â€” Rochas (soluÃ§Ãµes numÃ©ricas e procedimentos)

1) (jÃ¡ incluÃ­do) â€” Porosidade por pesagem: exemplo resolvido no ficheiro acima (Exemplo 1).

2) (figuras) â€” Porosidade idealizada: desenhe o volume total $V_t$, identifique $V_p$ (vazios) e calcule $\phi=V_p/V_t$. Em figuras, calcule Ã¡reas/volumes preferenciais e aplique fÃ³rmula.

3) **ExercÃ­cio (vÃ¡lvula e pressÃµes)** â€” Dados: $V_1=100\,$cc; $V_2=100\,$cc; $p_1=15\,$psi; $p_2=60\,$psi; $p_f=39\,$psi. Calcular volume do grÃ£o $V_g$.

DerivaÃ§Ã£o (conservaÃ§Ã£o do nÃºmero de moles a temperatura constante â€” Lei de Boyle):
$$p_1(V_1-V_g)+p_2V_2=p_f\,(V_1-V_g+V_2).$$
Resolvendo para $V_g$:
$$V_g=\dfrac{p_f(V_1+V_2)-p_1V_1-p_2V_2}{p_f-p_1}.$$ 
Substituindo valores:
$$V_g=\dfrac{39(100+100)-15\times100-60\times100}{39-15}=\dfrac{7800-1500-6000}{24}=\dfrac{300}{24}=12{,}5\;\text{cm}^3.$$

Resposta: $V_g=12{,}5\,$cc.

4) **Porosidade mÃ©dia (ExercÃ­cio 4)** â€” dados: 10, 12, 11, 13, 14, 10, 17 (%).
  - Soma = 77; mÃ©dia = $77/7 = 11.0\%$.

5) (jÃ¡ incluÃ­do) â€” MÃ©todo de ArquÃ­medes: exemplo resolvido no ficheiro (Exemplo 2).

6) **Compressibilidade de poros (exemplo)** â€” Dados: $V_p=18\,$cm^3$; \Delta V_p=0{,}15\,$cm^3 para $\Delta p=900\,$psi.
$$C_f=\dfrac{\Delta V_p/V_p}{\Delta p}=\dfrac{0{,}15/18}{900}\approx9{,}26\times10^{-6}\;\text{psi}^{-1}.$$ 

---

### CapÃ­tulo 4 â€” CÃ¡lculo volumÃ©trico (sensibilidade e procedimentos)

**ExercÃ­cio 4.8 (jÃ¡ incluÃ­do)** â€” OOIP calculado: aproximadamente $5{,}236{,}650\,$STB para $A=200\,$acres, $h=30\,$ft, $\phi=0.18$, $S_{wi}=0.25$, $B_o=1.2$.

**AnÃ¡lise de sensibilidade (variaÃ§Ã£o de $\phi$ de 0{,}15 a 0{,}22)** â€” usando a mesma fÃ³rmula prÃ¡tica:
- Para $\phi=0{,}15$:
$$OOIP\approx4{,}363{,}875\;\text{STB}.$$ 
- Para $\phi=0{,}22$:
$$OOIP\approx6{,}400{,}350\;\text{STB}.$$ 

InterpretaÃ§Ã£o: OOIP cresce aproximadamente linearmente com $\phi$ (mesmo A,h,Swi e Bo), mostrando elevada sensibilidade Ã  porosidade; variaÃ§Ã£o relativa de $\phi$ traduzâ€‘se diretamente numa variaÃ§Ã£o proporcional do OOIP.

**Procedimento Monte Carlo (resumo prÃ¡tico):**
 - Escolher distribuiÃ§Ãµes (ex.: normal/triangular) para $\phi$, $S_w$, $B_o$, $h$.
 - Gerar N iteraÃ§Ãµes (p.ex. 1.000â€“10.000), calcular OOIP por iteraÃ§Ã£o e recolher estatÃ­sticas P10/P50/P90.
 - Reportar mÃ©dia, desvios e percentis; preparar grÃ¡ficos de dispersÃ£o e histogramas.

---

### CapÃ­tulo 5 â€” EquaÃ§Ã£o de BalanÃ§o de Materiais (EBM) â€” passos e exemplo

**Passos para aplicar a linearizaÃ§Ã£o (Havlena & Odeh):**
1. Reunir por data: $p$, $N_p$, $G_p$, $W_p$ (produÃ§Ãµes), $B_o(p)$, $B_g(p)$, $R_s(p)$ a partir de PVT.
2. Calcular colunas por data: $E_o,E_g,E_{f,w}$ usando as fÃ³rmulas:
$$E_o = B_o - B_{o,i} + (R_{s,i}-R_s)B_g$$
$$E_g = B_{o,i}\left(\dfrac{B_g}{B_{g,i}} - 1\right)$$
$$E_{f,w} = B_{o,i}\left(S_{w,i}c_w + \dfrac{c_f}{1-S_{w,i}}\Delta p\right)$$
3. Montar $F$ (lado conhecido) por data (converter unidades):
$$F = N_p B_o + G_p - R_s B_g + W_p B_w - W_{inj} B_w - G_{inj} B_{g,inj}.$$ 
4. Fazer regressÃ£o linear mÃºltipla: $F = N E_o + m E_g + (1+m) E_{f,w} + W_e$ para estimar $N$ (estoque original) e $m$ (razÃ£o gasâ€‘cap/Ã³leo). Use regressÃ£o com todas as linhas de dados (mÃ­nimo 3â€“4 pontos; quanto mais, melhor).

**Exemplo (termo $E_o$ jÃ¡ calculado no ficheiro):**
 - Valores ilustrativos: $B_{o,i}=1{,}10$, $B_o=1{,}15$, $R_{s,i}=200\,$scf/STB, $R_s=180\,$scf/STB, $B_g=0{,}005$.
 - CalculÃ¡mos:
$$E_o=1{,}15-1{,}10+(200-180)\times0{,}005=0{,}15.$$ 

Para obter $N$ proceda assim (resumo): construa a tabela com colunas $F,E_o,E_g,E_{f,w}$ e execute uma regressÃ£o linear mÃºltipla (p.ex. em Excel: AnÃ¡lise de RegressÃ£o â†’ regressÃ£o mÃºltipla; em Python: numpy.linalg.lstsq ou statsmodels.OLS). O coeficiente associado a $E_o$ serÃ¡ a estimativa de $N$ (ou, dependendo da forma, a sua relaÃ§Ã£o direta â€” ver convenÃ§Ã£o de montagem das colunas).

---

Se desejar, posso agora:
- (A) inserir soluÃ§Ãµes detalhadas (passoâ€‘aâ€‘passo) para cada exercÃ­cio numerado nos ficheiros originais (por exemplo, 1â€“N de `exercÃ­cios_transcription.md`), incluindo os cÃ¡lculos intermÃ©dios e tabelas; ou
- (B) gerar um PDF/LaTeX do compÃªndio completo `exercicios_resolvidos.md` com formataÃ§Ã£o acadÃ©mica.

Ficarei aguardando a sua preferÃªncia para a etapa seguinte.
# CÃ¡lculo prÃ¡tico â€” CapÃ­tulo 3 (Propriedades das rochas)

**Enunciado**

Uma amostra de testemunho saturada com Ã³leo apresenta:
- massa saturada: m_sat = 130 g
- massa seca: m_dry = 105 g
- densidade do Ã³leo: Ï_o = 0.84 g/cmÂ³
- volume total da amostra: V_tot = 180 cmÂ³

Calcule:
(a) o volume de fluido nos poros V_f;  
(b) a porosidade Ï† (em %).  
Mostre todos os passos e apresente os resultados com 3 algarismos significativos.

---

**SoluÃ§Ã£o (passo a passo)**

1) Volume de fluido nos poros (V_f)

Usaâ€‘se a relaÃ§Ã£o entre massa de fluido e densidade:

\[ V_f = \frac{m_{sat} - m_{dry}}{\rho_o} \]

Substituindo os valores:

\[ V_f = \frac{130\ \text{g} - 105\ \text{g}}{0.84\ \text{g/cm}^3} = \frac{25}{0.84} \approx 29.7619\ \text{cm}^3 \]

Arredondando para 3 algarismos significativos: V_f â‰ˆ 29.8 cmÂ³.

2) Porosidade (Ï†)

Por definiÃ§Ã£o: \( \phi = \dfrac{V_p}{V_t} = \dfrac{V_f}{V_{tot}} \).

Substituindo:

\[ \phi = \dfrac{29.7619}{180} \approx 0.1653439 \approx 0.165 \]

Convertendo para percentagem e arredondando a 3 algarismos significativos: Ï† â‰ˆ 16.5 %.

---

**Resultados finais**

- Volume de fluido nos poros: V_f â‰ˆ 29.8 cmÂ³
- Porosidade: Ï† â‰ˆ 16.5 %

**ObservaÃ§Ãµes**
- Unidades usadas: g, cmÂ³, g/cmÂ³. Para SI, converta massa (kg) e volume (mÂ³) consistentemente.  
- MÃ©todo alternativo (mÃ©todo de ArquÃ­medes) e outros exemplos estÃ£o disponÃ­veis em `exercicios_resolvidos.md` e no material do Cap.3.
