# Petroleum Economics
## The Financial Discipline That Decides Which Projects Get Built

---

## Why Petroleum Engineers Must Understand Economics

Every technical decision you make has an economic consequence. Drilling an extra infill well costs $80M. Choosing water injection over pressure depletion adds $200M in injection facility costs but recovers 15% more oil. Installing a fourth gas compressor train increases plateau duration by 18 months.

Which of these is the right decision? You cannot answer that question with engineering alone. You need economics.

The petroleum economist does not replace the engineer. The petroleum economist IS the engineer who learns to think in money. Understanding economics makes you 10 times more powerful as a reservoir engineer, drilling engineer, or production engineer — because you can defend your technical recommendations in financial terms.

---

## Time Value of Money: The Foundation

The most important economic concept is that **$1 today is worth more than $1 in 5 years**.

Why? Because $1 today can be invested and earn a return. If your investment earns 10%/year:
- $1 today → $1.10 in Year 1 → $1.21 in Year 2 → $1.61 in Year 5

**Discount rate:** The rate used to convert future cash flows to present value. In upstream petroleum, typical discount rates are 8–15%, reflecting the risk of the investment.

**Present Value (PV) of a future cash flow:**

$$PV = \frac{CF_t}{(1 + r)^t}$$

Where:
- $CF_t$ = cash flow in year $t$
- $r$ = discount rate (e.g., 0.10 for 10%)
- $t$ = year number

**Net Present Value (NPV):** The sum of all discounted cash flows over the project life.

$$NPV = \sum_{t=0}^{T} \frac{CF_t}{(1+r)^t}$$

If NPV > 0: the project creates value at that discount rate → invest.
If NPV < 0: the project destroys value at that discount rate → do not invest.

**Worked Example:**
A small Angola satellite development:
- Year 0 (construction): -$800M (CAPEX)
- Years 1–5 (plateau): +$300M/year (net revenue)
- Years 6–10 (decline): +$150M/year average
- Discount rate: 10%

$$NPV = -800 + \frac{300}{1.1^1} + \frac{300}{1.1^2} + \frac{300}{1.1^3} + \frac{300}{1.1^4} + \frac{300}{1.1^5} + \frac{150}{1.1^6} + ... + \frac{150}{1.1^{10}}$$

$$NPV \approx -800 + 272.7 + 247.9 + 225.4 + 204.9 + 186.3 + 84.7 + 77.0 + 70.0 + 63.6 + 57.8$$

$$NPV \approx +\$689M$$

This project is economically attractive at a 10% discount rate.

---

## Key Economic Metrics

### Internal Rate of Return (IRR)
The IRR is the discount rate at which NPV = 0. It is the project's own implied return rate.

$$NPV = 0 = \sum_{t=0}^{T} \frac{CF_t}{(1+IRR)^t}$$

IRR is found by trial and error (or Excel's IRR function). A project is attractive if IRR > required return (hurdle rate).

**Angola deepwater context:** Major operators (TotalEnergies, Azule, Eni) typically require IRR > 15–20% for a greenfield deepwater development at the time of FID. This is because deepwater projects carry significant technical and commercial risk.

### Payback Period
The time until cumulative cash flows recover the initial CAPEX investment.

Simple payback (no discounting): divide CAPEX by annual net revenue.
Discounted payback: more conservative — uses PV of cash flows.

**Example:** $800M CAPEX at $300M/year revenue → simple payback ≈ 2.7 years.

### Breakeven Oil Price
The oil price at which NPV = 0. Below this price, the project loses money.

For Angola deepwater, typical breakeven oil prices range:
- New-build FPSO development: $45–70/bbl (Brent equivalent) depending on scale and CAPEX
- Tieback development: $25–40/bbl (much lower CAPEX)
- Mature field with paid-off FPSO: $15–25/bbl (OPEX-only basis)

---

## Angola's Production Sharing Agreement (PSA) Structure

Angola uses Production Sharing Agreements (PSAs) as the legal framework for oil development. This is fundamentally different from royalty-tax systems used in some other countries. You must understand this.

### How a PSA Works

Under an Angola PSA (Contrato de Partilha de Produção):

**Step 1: Cost Recovery Oil (Petróleo de Custo)**
The operator recovers its costs (CAPEX + OPEX) from production first. There is a cap — typically 50% of gross production in any year can be used for cost recovery.

$$\text{Cost Recovery Production} = \frac{\text{Allowable Costs}}{\text{Oil Price}} \leq \text{Cost Recovery Cap}$$

**Step 2: Profit Oil Split (Petróleo de Lucro)**
After cost recovery, the remaining production (profit oil) is split between:
- The operator consortium (IOCs + Sonangol in the consortium)
- ANPG/Sonangol (representing the Angolan state)

The split ratio depends on the PSA contract terms and often on an R-Factor (the ratio of cumulative revenue to cumulative costs — as the project becomes more profitable, the state's share increases).

**Typical Angola PSA splits (indicative):**
- Early production (R-Factor < 1): Operator 70% / State 30%
- Mid-life (R-Factor 1–2): Operator 50% / State 50%
- Mature (R-Factor > 2): Operator 30% / State 70%

**Step 3: Royalty**
Angola also charges royalties (2–10% of gross production) depending on the block and production depth/type.

**Step 4: Corporate Income Tax**
After profit oil allocation, the operator pays corporate income tax on their profit oil share.

### Simplified Angola PSA Cash Flow Model

```
GROSS PRODUCTION REVENUE (Qprod × Poil)
         │
         ▼
─── Less: Royalty (e.g., 5% of gross) ──────────────────→ Government
         │
         ▼
AVAILABLE FOR COST RECOVERY
         │
         ├── Cost Recovery Oil ──────────────────────────→ Operator (cost recovery)
         │   (capped at 50% of available production)
         │
         ▼
PROFIT OIL
         │
         ├── State Share (30–70%) ──────────────────────→ ANPG/Sonangol
         │
         └── Operator Share (30–70%)
                   │
                   ▼
         Less: Corporate Income Tax (35%)
                   │
                   ▼
         NET CASH FLOW TO OPERATOR
```

**Why this matters for petroleum engineers:** When you advocate for an infill well ($80M cost), you are not spending $80M of your company's money in isolation. Under cost recovery, that $80M is recovered from the oil first. The net cost to the operator after cost recovery may be only $24M (if the operator's profit oil share is 30%). This changes the economics — making infill wells more attractive than a simple CAPEX analysis suggests.

---

## CAPEX and OPEX Estimation

### Capital Expenditure (CAPEX)
One-time costs to build the project.

**Typical CAPEX breakdown for an Angola FPSO development:**

| Category | % of Total CAPEX | Example Item |
|----------|-----------------|--------------|
| FPSO (hull + mooring + topsides) | 30–45% | FPSO Kaombo Norte ≈ $4B |
| Subsea (trees, manifolds, flowlines, umbilicals) | 25–35% | 16 trees × $10M each + SURF |
| Drilling (wells) | 20–30% | 8 producers × $80M + 7 injectors × $70M |
| Project management, contingency | 5–10% | PMC fees, 10–15% contingency |

**CAPEX accuracy by project phase:**
- Concept selection: ±50% (order of magnitude estimate)
- Pre-FEED: ±30%
- FEED: ±15%
- Detailed engineering: ±5%

### Operating Expenditure (OPEX)
Annual costs to operate the field.

**OPEX components:**
- FPSO lease/operating cost (if FPSO is leased): $100–200M/year for large FPSO
- Drilling of in-fill wells (during operations): $60–100M each
- Subsea maintenance and IMR (ROV, inspection): $20–50M/year
- Chemical injection: $10–20M/year
- Logistical support (supply vessels, helicopters): $30–60M/year
- Personnel costs: $50–100M/year

**OPEX per barrel ($/boe):** The key operational metric.
- World-class Angola FPSO: $15–25/bbl OPEX
- Average Angola deepwater: $20–35/bbl OPEX
- Cabinda (Block 0) shallow water: $10–20/bbl OPEX (lower because FPSO is paid off)

---

## Sensitivity Analysis and Monte Carlo Simulation

Economic models are not point estimates — they are ranges. The key inputs (oil price, production rate, CAPEX) are all uncertain. Sensitivity analysis quantifies this.

### One-Way Sensitivity (Tornado Chart)
Vary one input at a time while holding all others constant. The inputs that cause the largest NPV swings are the most important risks.

```
NPV Base Case: $689M

Oil Price ±20%:         ──────────────|────────────── ($320M to $1,060M)
CAPEX ±20%:             ─────────|──────────          ($530M to $850M)
Production Rate ±20%:   ──────|──────────             ($480M to $900M)
Discount Rate 8-15%:    ─────|──────                  ($550M to $780M)
Operating Cost ±20%:    ───|────                      ($620M to $760M)
```

→ Oil price and CAPEX are the biggest risks. Focus your mitigation effort there.

### Monte Carlo Simulation
Instead of varying one input at a time, sample all inputs simultaneously from probability distributions. Run 10,000 iterations. The result is a probability distribution of NPV.

**Input distributions (example):**
- Oil price: triangular distribution (min $50/bbl, mode $75/bbl, max $110/bbl)
- Recovery factor: triangular (min 25%, mode 35%, max 45%)
- CAPEX: triangular (base $800M ×1.0, most likely $800M, worst case $800M ×1.25)
- OPEX: normal (mean $25/bbl, std dev $5/bbl)

**Output:** P10 NPV = $200M, P50 NPV = $650M, P90 NPV = $1,200M

This tells management: there is a 50% chance this project exceeds $650M NPV and a 10% chance it exceeds $1,200M NPV.

**Software for Monte Carlo in petroleum:** @Risk (Excel add-in), Crystal Ball (Excel add-in), Python (scipy/numpy), or dedicated petroleum software like Merak PEEP.

---

## Economic Limit

Every field has an economic limit — the point where revenue no longer exceeds operating costs.

$$Q_{economic} = \frac{OPEX_{monthly}}{(P_{oil} - \text{transportation} - \text{royalty}) \times 30}$$

Where $Q_{economic}$ is the minimum production rate to remain economic.

**Example:**
- Monthly OPEX for a well: $500,000/month
- Oil price: $75/bbl
- Transportation + royalty: $10/bbl
- Net price: $65/bbl

$$Q_{economic} = \frac{500,000}{65 \times 30} = \frac{500,000}{1,950} \approx 256 \text{ bbl/day}$$

When a well falls below 256 bbl/day, it becomes uneconomic and should be shut in (unless it is a water injector providing reservoir pressure support for nearby producers, in which case the economic analysis is different).

---

## Real-World Economic Decisions That PE Engineers Make

These are the decisions where economic thinking directly intersects with technical work:

### Infill Drilling Decision
"Should we drill one more production well at $80M cost?"

Framework:
1. Reservoir engineer: estimate incremental production from the infill well (Δ cumulative recovery)
2. Convert to revenue: Δ cumulative bbl × (oil price - transportation)
3. Apply PSA cost recovery: net CAPEX to operator is lower than $80M
4. Calculate incremental NPV: is it positive at 10% discount rate?
5. Decision: drill if incremental NPV > 0

### Water Injection Timing
"Should we start water injection in Year 1 (costs $150M for injection wells + injection facility) or wait until Year 3 when pressure starts declining?"

Framework:
1. Reservoir engineer: model recovery factor with early injection vs late injection
2. Facilities engineer: estimate injection facility CAPEX for each case
3. Economist: NPV comparison of early vs late injection (earlier investment costs more in NPV terms but recovers more oil)
4. Decision: depends on the oil price and the recovery factor differential

### EOR (Enhanced Oil Recovery) Decision
"Should we invest $400M in a water alternating gas (WAG) injection scheme on a mature field?"

This is a full FDP in miniature. Requires all the same economic analysis as a new development.

---

## Engenharia Económica: What ISPTEC Teaches vs What Industry Needs

Your Engenharia Económica subject at ISPTEC covers:
- Time value of money ✓
- NPV, IRR, Payback ✓
- Basic project evaluation ✓

What industry additionally requires:
- PSA economics model (not taught at ISPTEC — learn it here)
- Monte Carlo simulation with petroleum-specific input distributions
- Real options analysis (the option to delay, expand, or abandon)
- Fiscal regime comparison (PSA vs royalty-tax)
- SEC/SPE reserves classification linked to economic limit

**Self-study gap:** Read "Fundamentals of Oil and Gas Accounting" by Charlotte Wright and Rebecca Gallun. Free chapters are available via the SPE Digital Library.

---

## The Number Every Angolan PE Graduate Should Know

**Angola deepwater breakeven oil price: approximately $45–70/bbl for new greenfield development.**

At $75/bbl Brent (close to current 2026 market), Angola deepwater projects are marginal to economic depending on CAPEX. This is why:
- Operators are focusing on tiebacks to existing FPSOs (lower CAPEX, lower breakeven)
- Sonangol and ANPG are offering fiscal incentives for new deepwater development
- CAPEX reduction is a strategic priority for every Angola operator

When you enter the industry, you will be working in this economic environment. Know the numbers.

---

## Interview Questions for Economics-Flavoured Roles

1. What is NPV and how does it differ from simple payback period?
2. Explain how Angola's PSA structure works. What is cost oil and profit oil?
3. What is the economic limit of a well and how do you calculate it?
4. An infill well costs $80M and will recover an incremental 3 MMbbl at $65/bbl net. Is it economic? Show your calculation.
5. What is Monte Carlo simulation and why do we use it for petroleum economics?
6. What is the breakeven oil price for a typical Angola deepwater development?
7. Explain the R-Factor in an Angola PSA. Why does it matter?
8. What discount rate would you use for an Angola deepwater project and why?
9. What is the difference between CAPEX and OPEX, and how do they affect the economics differently?
10. Why does early water injection improve the NPV even though it requires upfront CAPEX?

---

*Next: [04_Production_Technology_Discipline.md](04_Production_Technology_Discipline.md) — artificial lift selection, flow assurance, and production optimisation.*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
