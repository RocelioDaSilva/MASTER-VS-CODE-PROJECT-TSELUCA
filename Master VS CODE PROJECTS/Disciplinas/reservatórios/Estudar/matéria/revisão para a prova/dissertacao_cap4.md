# Dissertação — Capítulo 4

**Tema:** Incertezas no método volumétrico: fontes, quantificação e mitigação

**Introdução.**
O método volumétrico é a base inicial para estimativas de volumes originalmente em lugar (OOIP/OGIP) e, por isso, a compreensão e a gestão das suas incertezas são essenciais para decisões de exploração e desenvolvimento. A incerteza deriva de variabilidade geológica, limitações de medição e escolhas metodológicas; a prática robusta combina QA/QC de dados, análise determinística e probabilística para produzir estimativas utilizáveis em engenharia.

**Desenvolvimento.**
As fontes principais de incerteza incluem: (i) geometria do reservatório (área $A$, espessura neta $h$ e Net‑to‑Gross), (ii) propriedades petrofísicas ($\phi$, $S_w$) e (iii) parâmetros PVT ($B_o$, $R_s$, $B_g$). Uma forma prática de ver o problema é pela fórmula clássica:

$$
OOIP = \frac{7758\,A\,h\,\phi\,(1-S_w)}{B_o}
$$

Pequenas variações relativas em $A$, $h$ ou $\phi$ propagam‑se linearmente para o $OOIP$, enquanto erros em $B_o$ têm efeito inverso. Além disso, a heterogeneidade lateral/vertical e escolhas de cut‑off para definir pay podem introduzir viés sistemático.

Para quantificar incertezas recomenda‑se um fluxo em dois níveis: (1) análises de sensibilidade univariada para identificar parâmetros críticos; (2) simulações probabilísticas (Monte Carlo ou Latin Hypercube) para gerar distribuições de saída (P10/P50/P90). Complementos úteis incluem análise de cenário (melhor/pior caso) e bootstrap sobre amostras de core/log para estimar erro amostral.

Medidas de mitigação práticas: fortalecer o QA/QC (calibração core↔log↔PVT), aumentar amostragem representativa nas zonas mais incertas, usar correlação estatística entre variáveis (p.ex. $\phi$ vs N/G) e aplicar modelagem geoestatística para propagar variabilidade espacial. Integração com métodos independentes (material balance, ajuste de produção e declínio) permite validar e restringir estimativas volumétricas.

**Conclusão.**
Gerenciar incertezas no método volumétrico exige uma abordagem integrada: identificar parâmetros sensíveis, quantificá‑los com simulação probabilística e reduzir incerteza com QA/QC, amostragens adicionais e integração de métodos. Ao combinar análises determinísticas (sensibilidade) e probabilísticas (Monte Carlo) com validação operacional (material balance), obtém‑se estimativas mais robustas e decisões de desenvolvimento menos arriscadas.