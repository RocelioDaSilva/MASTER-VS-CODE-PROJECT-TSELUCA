# Compressibilidade (fator) Z — Cheatsheet extremo

Objetivo: referência completa e passo‑a‑passo para entender, calcular e aplicar o fator de compressibilidade $Z$ (gás real), com métodos práticos (Standing–Katz, EoS), derivadas úteis e um exemplo numérico com código Python.

---

**Resumo rápido**
- **Definição:** $Z = \dfrac{p V_m}{R T}$, mede o desvio do gás em relação ao gás ideal ($Z=1$ ideal).
- **Usos:** converter entre densidade e pressão/temperatura reais; calcular o fator de volume $B_g$; avaliar compressibilidade isotérmica do gás; PVT e balanço de massas.

---

**1) Formulação e relações básicas**

- Molar volume: $V_m = \dfrac{Z R T}{p}$.  
- Densidade (massa): $\rho = \dfrac{M p}{Z R T}$, onde $M$ é massa molar (kg·mol^{-1}).
- Fator de volume do gás (molar): $B_{m} = V_m = \dfrac{Z R T}{p}$. (Em reservatórios usa‑se versões por massa/por scf — adaptar unidades.)

**2) Relação com compressibilidade isotérmica do gás $c_g$**

Partindo de $V_m = Z R T / p$ e definindo $c_g = -\dfrac{1}{V_m} \left( \dfrac{\partial V_m}{\partial p} \right)_T$ obtém‑se:

$$
c_g \,=\, \frac{1}{p} \, - \, \frac{1}{Z} \left(\frac{\partial Z}{\partial p}\right)_T \,=\, \frac{1}{p} \, - \, \frac{\partial \ln Z}{\partial p} .
$$

Interpretação prática: para gás quase ideal $\partial Z/\partial p \approx 0$ e $c_g\approx 1/p$. O termo com $\partial Z/\partial p$ corrige o comportamento real; portanto é importante para pressões altas / não‑ideais.

**3) Métodos para obter $Z$ (ordem de complexidade e precisão)**

- Leitura direta no gráfico Standing–Katz (rápido; precisa dos pseudo‑críticos do gás).  
- Correlações empíricas e semi‑empíricas (ex.: Dranchuk–Abou‑Kassem) — boas para implementação numérica.  
- Equações de estado cúbicas (Peng–Robinson, Soave–Redlich–Kwong) — recomendadas quando se tem composição e se precisa de consistência em fase líquida/vapor; permitem calcular Z e derivadas termodinâmicas.

**4) Pseudocríticos e preparação (how‑to)**

Para usar chart ou correlações reduzidas, calcule $T_{pc}$ e $P_{pc}$ da mistura. Duas rotas:

- Regra de Kay (mistura):  
  - para cada componente i obtenha $T_{c,i}$ e $P_{c,i}$ (temperaturas Kelvin, pressão em Pa).  
  - calcule $T_{pc} = \sum_i y_i \, T_{c,i}$ e $P_{pc} = \sum_i y_i \, P_{c,i}$ (mole fractions $y_i$).  
  - então $T_r = T / T_{pc}$ e $P_r = p / P_{pc}$.  

- Correções para gás ácido / CO2/H2S (Wichert–Aziz): existem procedimentos para reduzir $T_{pc}$ e $P_{pc}$ quando frações significativas de CO2/H2S estiverem presentes — aplicar se $\mathrm{CO_2}+\mathrm{H_2S}$ > ~2–5\% mole.

Com $T_r$ e $P_r$ você lê $Z$ no gráfico de Standing–Katz (curvas $Z$ vs $P_r$ para cada $T_r$). Para automação prefira correlações numéricas (Dranchuk–Abou‑Kassem) ou uma EoS.

**5) Método robusto: Peng–Robinson (PR) — passo a passo (Padrão industrial)**

Parâmetros do PR (unidades SI):

$$
a = 0.45724 \frac{R^2 T_c^2}{P_c},\qquad b = 0.07780 \frac{R T_c}{P_c}
$$

onde $R=8.314462618$ J·mol^{-1}·K^{-1}, $T_c$ (K), $P_c$ (Pa). O fator $\alpha$ descreve dependência com $T$:

$$
\kappa = 0.37464 + 1.54226\,\omega - 0.26992\,\omega^2,\qquad
\alpha(T) = \left(1 + \kappa \left(1-\sqrt{\dfrac{T}{T_c}}\right)\right)^2
$$

Defina então:

$$
A = \dfrac{a\,\alpha(T)\,p}{R^2 T^2},\qquad B = \dfrac{b p}{R T}.
$$

O polinômio cúbico em $Z$ (forma padrão PR):

$$
Z^3 - (1 - B) Z^2 + (A - 3B^2 - 2B) Z - (A B - B^2 - B^3) = 0.
$$

Solução: encontre as raízes reais; para fase gasosa escolha a maior raiz real (maior $Z$).

**6) Exemplo numérico completo (CH4 puro)**

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

2) $\kappa\approx 0.3916$, $\alpha\approx 0.7396$ (usar fórmula acima).

3) $A\approx 0.1089$, $B\approx 0.0460$ (ver cálculos no script abaixo).

4) Monta o cúbico e resolve: obtém $Z\approx 0.948$ (raiz gasosa principal).

Interpretação: $Z<1$ porém próximo de 1 — desvio moderado para estas condições.

**7) Compressibilidade isotérmica calculada numericamente (exemplo)**

Procedimento prático (numérico):
1. Calcule $Z(p)$ com o método EoS (PR) no ponto $p$ (aqui 5 MPa).
2. Calcule $Z(p+\Delta p)$ com $\,\Delta p$ pequeno (ex.: $10^4$–$10^5\ \mathrm{Pa}$).  
3. Estime $\partial Z/\partial p \approx (Z(p+\Delta p)-Z(p))/\Delta p$.  
4. Use $c_g = 1/p - (1/Z) (\partial Z/\partial p)$.

Usando o exemplo numérico (valores aproximados do passo anterior e $\Delta p=10^5\ \mathrm{Pa}$) obtemos $c_g\approx 2.19\times10^{-7}\ \mathrm{Pa^{-1}}$ que corresponde a $0.219\ \mathrm{MPa^{-1}}$ ou aproximadamente $1.51\times10^{-3}\ \mathrm{psi^{-1}}$ (conversões mostradas no script).

**8) Código Python (PR EoS) — cálculo de Z e compressibilidade por diferença finita**

Instalar dependência mínima: `pip install numpy`

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

Saída esperada aproximada (exemplo que usamos manualmente): `Z ≈ 0.948`, `c_g ≈ 2.19e-7 Pa^-1`.

**9) Recomendações práticas e atenção a unidades**

- Sempre usar unidades consistentes (SI: Pa, K, J/(mol·K)). Para conversões (psi, °R) ajuste constantes do gás.  
- Para misturas use regras de mistura apropriadas (EoS: combinações de `a_{ij}`/fatores de interação). Se não conhecer os coeficientes binários use $k_{ij}=0$ como primeira aproximação (pode introduzir erro).  
- Para trabalho de campo rápido: calculadoras com Standing–Katz (chart) ou correlação DAK. Para simulação/reconhecimento e prognóstico, prefira EoS com mistura.

**10) Referências rápidas**

- Standing, M. B., Katz, D. L. — gráfico Standing–Katz para $Z$ (uso clássico).  
- Dranchuk, P. M. & Abou‑Kassem, J. H. (1975) — correlação numérica para $Z$ (boa para automação).  
- Peng, D.-Y. & Robinson, D. B. (1976) — Peng–Robinson EoS (cúbica), uso industrial.  
- Wichert, D. & Aziz, K. (1972) — correção pseudo‑crítica para CO2/H2S (gases ácidos).

---

Se quiser, eu:
- gero uma versão com figuras (Standing–Katz) e tabela de propriedades críticas;  
- adiciono uma implementação DAK (Dranchuk–Abou‑Kassem) completa em Python;  
- aplico o cálculo a uma mistura real (envie composição molar) e salvo o resultado.
