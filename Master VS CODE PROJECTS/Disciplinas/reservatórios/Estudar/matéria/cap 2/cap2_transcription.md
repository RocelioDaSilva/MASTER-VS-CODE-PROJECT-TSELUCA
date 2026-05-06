

# ENGENHARIA DE RESERVATÓRIOS I
**3º Ano – 2º Semestre — 2025–2026**

**Docente:** Prof. Dr. Geraldo A. R. Ramos

---

## Sumário
- 2.1 Introdução
- 2.2 Misturas e soluções
- 2.3 Propriedades básicas dos fluidos
	- 2.3.1 Propriedades de óleo
	- 2.3.2 Propriedades dos gases
	- 2.3.3 Propriedades de misturas de hidrocarbonetos
- 2.4 Consolidação da aula
- 2.5 Tarefas
- Bibliografia

---

## Objetivo geral
Analisar as propriedades dos fluidos de reservatório por meio da caracterização de misturas e soluções, aplicação de equações de estado, interpretação de dados PVT e utilização de correlações empíricas, visando prever o comportamento dos fluidos e apoiar a tomada de decisão na engenharia de reservatórios.

### Objetivos específicos
- Identificar os tipos de misturas e soluções presentes nos fluidos.
- Descrever propriedades físicas e termodinâmicas relevantes (densidade, viscosidade, compressibilidade, fator de volume, etc.).
- Aplicar equações de estado e correlações empíricas para estimativas de propriedades.
- Calcular o fator volume de formação (B_o), a razão de solubilidade (R_s) e interpretar resultados PVT.
- Avaliar a influência da viscosidade e do grau API no escoamento.

## 2.1 Introdução
Um fluido é uma substância que se deforma continuamente (escoa) sob ação de uma força tangencial. Para o engenheiro de reservatórios, conhecer as propriedades físico‑químicas e o comportamento de fase é essencial para estimar volumes in situ, planejar produção e definir estratégias de recuperação.

### Amostragem e análises
- Amostragem em superfície (separadores e frascos de amostra).
- Amostragem em fundo de poço (downhole sampling).
- Amostragem em teste de formação (formation testing).

Análises normalmente realizadas:
- Determinação da composição (frações de hidrocarbonetos C1–Cn).
- Análises PVT: ensaios CCE (constant composition expansion), DL (differential liberation), flash, etc.
- Determinação de propriedades tecnológicas: $B_o$, $R_s$, viscosidade, densidade, Z‑factor.
- Testes de compatibilidade de fluidos e análise de contaminantes.

## 2.2 Misturas e soluções
- Mistura: combinação física de componentes (gás + óleo + água) onde as fases podem coexistir.
- Solução: situação em que um componente está dissolvido (ex.: gás dissolvido no óleo). A razão gás/óleo dissolvido é expressa por $R_s$ (m³ de gás por m³ de óleo, ou SCCM/Sm³ conforme unidade).
- Pontos relevantes: ponto de bolha (bubble point) e ponto de orvalho (dew point) que definem o início da formação de uma fase livre.

## 2.3 Propriedades básicas dos fluidos

### 2.3.1 Propriedades de óleo
- Densidade e gravidade API: $API = \frac{141.5}{\rho_{sp}} - 131.5$ (forma prática para converter densidade específica em grau API).
- Viscosidade: afeta diretamente a mobilidade e a taxa de fluxo através do meio poroso.
- Fator volume de formação ($B_o$): relação entre volume no reservatório e volume à superfície; importante para conversão de volumes de reservatório para superficie.
- Compressibilidade de óleo: influencia o declínio de pressão e estimativas volumétricas.

### 2.3.2 Propriedades dos gases
- Gases ideais obedecem à equação de estado $pV = nRT$ em condições de baixa pressão e alta temperatura.
- Leis fundamentais: Boyle ( $V\propto 1/p$ ), Charles ( $V\propto T$ ), Avogadro.
- Lei de Dalton (pressões parciais): a pressão total de uma mistura é a soma das pressões parciais.
- Gases reais: desvio do comportamento ideal é quantificado pelo fator de compressibilidade $Z$ (tabelas/curvas de correção). Equações de estado cúbicas (Peng‑Robinson, Soave‑Redlich‑Kwong) são usadas em PVT.

### 2.3.3 Propriedades de misturas de hidrocarbonetos
- Comportamento de fases (monofásico vs bifásico) dependente de pressão e temperatura.
- Razão gás‑óleo ($R_s$) e fator de formação $B_o$ em sistemas bifásicos.
- Uso de análises PVT (flash/diferencial) para determinar curvas de $B_o(p)$, $R_s(p)$, viscosidade vs pressão e temperatura.

## 2.4 Consolidação da aula
Exemplos de perguntas para revisão:
- O que é $B_o$ e por que é importante para o cálculo de volumes produzidos?
- Como o $R_s$ varia com a pressão e o que significa atingir o ponto de bolha?
- Como a viscosidade do óleo influencia a mobilidade e o fator de recuperação?
- Quando o gás pode ser tratado como ideal e quando deve‑se usar correções (Z‑factor)?

## 2.5 Tarefas
1. Desenhar o envelope de fases para uma mistura óleo‑gás e identificar ponto de bolha e ponto de orvalho.
2. Calcular $B_o$ e $R_s$ em um caso hipotético a partir de dados PVT simplificados (fornecerei os dados se desejar).
3. Fazer um resumo comparativo: gases ideais vs gases reais e apresentar quando usar equações de estado cúbicas.
4. Ler um ensaio PVT (CCE + DL) e resumir os principais resultados e curvas obtidas.

## Bibliografia
1. MCCAIN, W. D. The Properties of Petroleum Fluids. 2nd ed. Tulsa: PennWell Books, 1990.
2. DAKE, L. P. Engenharia de Reservatórios: fundamentos. Elsevier, 2014.
3. AHMED, T. Reservoir Engineering Handbook. 3rd ed. Elsevier, 2010.
4. ROSA, A. J.; CARVALHO, R. D. S.; XAVIER, J. A. D. Engenharia de Reservatórios de Petróleo. Interciência, 2006.

---

## Definições importantes
- **Fator de volume de formação ($B_o$):** razão entre o volume de óleo em condições de reservatório e o volume correspondente à superfície (bbl/STB ou m^3/m^3). Fórmula: $B_o = V_{res}/V_{surf}$.
- **Razão de solubilidade ($R_s$):** quantidade de gás dissolvido por unidade de óleo (scf/STB ou m^3/m^3). No ponto de bolha, $R_s$ corresponde ao máximo gás dissolvido antes do aparecimento de gás livre.
- **Fator de compressibilidade do gás ($Z$):** correção adimensional que quantifica o desvio do comportamento ideal do gás: $Z = pV/(nRT)$.
- **Ponto de bolha / ponto de orvalho:** pressão (a uma dada temperatura) em que surge a primeira bolha de gás no líquido ou a primeira gota de líquido no gás.

## Exemplo prático — cálculo de $B_o$ e $R_s$
Considere um ensaio PVT simplificado com resultados experimentais por 1 STB amostrado:
- Volume de óleo medido em condições de reservatório: $V_{res} = 1.20\;\text{bbl}$;
- Volume correspondente à superfície: $V_{surf} = 1.00\;\text{STB}$;
- Gás libertado no ensaio: $R_s = 400\;\text{scf/STB}$.

Cálculo de $B_o$:
$$
B_o = \frac{V_{res}}{V_{surf}} = \frac{1.20\;\text{bbl}}{1.00\;\text{STB}} = 1.20\;\text{bbl/STB}
$$
Interpretação: 1 STB de óleo de superfície corresponde a 1.20 bbl no reservatório.

Conversão de $R_s$ para unidades SI (opcional):
1 scf = 0.0283168 m^3; 1 STB = 0.1589873 m^3.
$$
R_s\,\text{(m}^3/\text{m}^3) = \frac{400\times0.0283168}{0.1589873} \approx 71.3\;\text{m}^3/\text{m}^3
$$

Observação: prefira as unidades pedidas no enunciado (scf/STB é muito comum). Converta unidades apenas quando necessário e mantenha consistência.

## Notas práticas e correlações
- Quando não existirem dados experimentais, use correlações empíricas (p.ex. Standing, Vazquez‑Beggs) ou equações de estado cúbicas (Peng‑Robinson, SRK) para estimar $B_o$, $R_s$ e viscosidade.
- Para gás, determine $Z(p,T)$ via charts ou equações para calcular volumes em condições padrão e avaliar expansibilidade.

## Glossário de símbolos (cap.2)
- $B_o$: fator de volume de formação do óleo (bbl/STB ou m^3/m^3).
- $R_s$: razão gás/óleo dissolvido (scf/STB ou m^3/m^3).
- $Z$: fator de compressibilidade do gás (adimensional).
- $\rho$: densidade (kg/m^3).
- $\mu$: viscosidade (cP).

## Dicas rápidas de estudo
- Verifique sempre as unidades antes de aplicar fórmulas; a maioria dos erros vem de conversões incorretas.
- Plote curvas PVT simplificadas ($B_o(p)$, $R_s(p)$, $\mu(p)$) para compreender tendências com pressão.
- Use exemplos numéricos pequenos (1 STB) para fixar interpretação física dos parâmetros.
- Ao estudar equações de estado, foque primeiro no conceito físico (equilíbrio de fases) antes da implementação numérica.

---

Muito obrigado(a)!

