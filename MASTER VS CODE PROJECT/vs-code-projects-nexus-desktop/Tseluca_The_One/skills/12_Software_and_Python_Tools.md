# Software Tools You Must Know — Angola Petroleum Engineering
## The Complete Practical Guide: What Runs the Industry, What You Can Learn Free

> No one teaches you this at university. This file tells you exactly which software runs Angola's oil sector, what it does, how you learn it (free or cheap), and what to say in interviews. Knowing even ONE tool deeply is a hiring advantage because most fresh graduates know none.

---

## The Software Landscape by Discipline

### Quick Reference Map

```
DRILLING                     PRODUCTION                  RESERVOIR
───────────────              ──────────────              ─────────────
WellPlan (Landmark/Halliburton) → T&D, casing    Prosper (Petex) → IPR, nodal    Eclipse (SLB) → dynamic sim
COMPASS (Landmark) → directional planning        GAP (Petex) → network optimize   CMG IMEX/GEM → dynamic sim
EDR / DROPS (Halliburton) → real-time monitoring PIPESIM (SLB) → pipeline flow    Petrel (SLB) → static model
Petrel WellDesign (SLB) → wellbore planning      OLGA (SLB) → transient multiphase Techlog (SLB) → petrophysics
iHandS / WellPlan (NOV) → hole cleaning          PI System (OSIsoft) → historian  DecisionSpace (Halliburton) → petrophysics

COMPLETIONS                  HSE                         DIGITAL/DATA
──────────────────           ─────────────               ─────────────
Perform (Baker Hughes) → well performance      Bowtie XP → bow-tie analysis     Python + pandas + numpy
WellFlo → IPR, nodal, GL    SAFETI (DNV) → consequence   Matplotlib/Plotly → visualization
Fracpro / FracPT → frac design  PHA-Pro (Dyadem) → HAZOP   Jupyter Notebooks → analysis
WELLCAT (Landmark) → casing design  Isograph (FaultTree+) → QRA  Excel VBA → automated reports
```

---

## Tool Deep Dives: Prosper (Most Important Production Tool)

### What It Is
Prosper (from Petroleum Experts Ltd, Edinburgh) is the industry-standard **nodal analysis** software. It models:
- The **IPR** (Inflow Performance Relationship) — how the reservoir delivers fluid to the wellbore
- The **VLP** (Vertical Lift Performance) — how fluid travels from wellbore to surface
- **Artificial lift** (gas lift, ESP, rod pump)
- The **operating point** (where IPR and VLP intersect = your actual production rate)

Every production engineer in Angola uses Prosper. TotalEnergies, Azule, Eni, Chevron, Sonangol all have Prosper licenses. If you say "I know Prosper" in an interview, you will immediately differentiate yourself.

### Free Learning Path

**Option 1 — Petroleum Experts provides student licenses:**
Go to: petex.com → Education → Student License
You need to apply through your university (ISPTEC). If ISPTEC has an academic agreement, you get a free license. If not, ask your professor to contact Petex directly.

**Option 2 — Learn through tutorial videos:**
Search YouTube: "Prosper petroleum tutorial" — there are multi-hour walkthroughs.

**Option 3 — Learn the concepts, use the formulas manually:**
Before you get the software, master the underlying math:

```python
# IPR (Darcy radial flow) in Python — practice this
import numpy as np
import matplotlib.pyplot as plt

# Well parameters (Block 17 example)
Pr = 4100  # psi, reservoir pressure
PI = 6.5   # STB/day/psi, productivity index (from well test)

# Generate IPR curve
Pwf = np.linspace(0, Pr, 100)  # range of bottomhole flowing pressures
q_oil = PI * (Pr - Pwf)         # Darcy linear IPR

# VLP (simplified linear, or import from Prosper)
# VLP: FBHP = A + B*q (simplified)
A = 1200  # psi (minimum BHP for the tubing string at zero rate)
B = 0.32  # psi/(STB/day) (slope)
FBHP_VLP = A + B * q_oil

# Operating point: where IPR = VLP
# Set equal: Pr - q/PI = A + B*q → solve for q
q_op = (Pr - A) / (1/PI + B)
P_op = A + B * q_op

plt.figure(figsize=(10, 6))
plt.plot(q_oil, Pwf, 'b-', linewidth=2, label='IPR (Darcy)')
plt.plot(q_oil, FBHP_VLP, 'r-', linewidth=2, label='VLP')
plt.axvline(x=q_op, color='green', linestyle='--', label=f'Operating point: {q_op:.0f} STB/day')
plt.axhline(y=P_op, color='green', linestyle='--')
plt.xlabel('Oil rate (STB/day)')
plt.ylabel('Bottomhole Flowing Pressure (psi)')
plt.title('Nodal Analysis — Block 17 Example')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('nodal_analysis.png', dpi=150)
plt.show()
print(f"Operating rate: {q_op:.0f} STB/day")
print(f"Operating FBHP: {P_op:.0f} psi")
```

Run this in a Jupyter notebook. Save the plot. Add it to your CV portfolio on GitHub.

---

## Petrel — The Platform That Runs Everything

### What It Is
Petrel (SLB, formerly Schlumberger) is the **dominant integrated reservoir characterization and modelling platform** in Angola's oil sector. It does:
- **Seismic interpretation** — picking horizons, fault interpretation
- **Well correlation** — matching formations across multiple wells
- **Petrophysical analysis** — calculating porosity, Sw, NTG from logs (via Techlog plugin)
- **Structural modelling** — building the 3D geometry of the reservoir
- **Property modelling** — populating the grid with porosity, permeability, Sw
- **Volume calculation** — STOIIP from the static model
- **Export to Eclipse** — sending the model to dynamic simulation

**In Angola:** Every single TotalEnergies, Azule, Eni, Chevron, and Sonangol subsurface team uses Petrel. The reservoir engineers, geologists, and geophysicists who work on Block 17 and Block 32 spend their workday in Petrel.

### Free Learning
- **Petrel learning edition:** SLB provides a limited free version. Access via: slb.com/products → Software → Petrel → Student Resources
- **E-learning:** SLB Eureka training portal (ask your company/university for access)
- **YouTube:** "Petrel tutorial beginners" — multiple 30-60 min walkthroughs

### What You Do in Petrel (Angola Reservoir Context)

**Step 1: Import well data**
```
File → Import → Well Data → LAS file (from wireline logs)
→ Select wells: GD-1, GD-2, GD-3 (Block 32 exploration wells)
→ Set datum: KB elevation
→ Assign curves: GR, RHOB, NPHI, Rt, Caliper
```

**Step 2: Correlate wells**
Create a well section panel. Pick the **Malembo Formation** top in each well. The top is where GR drops from >80 to <30 API. In GD-1 it's at 3,468m, in GD-2 at 3,412m, in GD-3 at 3,489m. The formation is shallower in GD-2 — the reservoir is dipping.

**Step 3: Build the structural model**
- Horizon: Top Malembo Sand (picked across wells + interpolated from seismic)
- Fault model: 2 faults identified on seismic, verified by pressure compartmentalization in MDT data
- Grid: 100m × 100m × 1m cells (3D grid)

**Step 4: Property modelling**
For each cell: assign porosity (from the well log at that location, interpolated by kriging between wells), Sw (from Archie's equation using Rt and φ), NTG (1 if Vsh<0.30 and φ>0.10, else 0).

**Step 5: STOIIP calculation**

$$STOIIP = \frac{7758 \times A \times h \times NTG \times \phi \times (1-S_w)}{B_{oi}}$$

In Petrel this is calculated automatically: Right-click → Volumetrics → Calculate HC volumes. You get P10, P50, P90.

---

## Eclipse — Dynamic Reservoir Simulation

### What It Is
Eclipse (SLB) is the **dominant reservoir simulator** used for Angola deepwater field development planning. It simulates fluid flow through the porous rock over time, predicting:
- How much oil you can produce from a field over its life
- How water injection supports pressure and sweeps oil toward producers
- What happens at different development scenarios (fewer wells? more water injection?)

**In Angola:** TotalEnergies used Eclipse extensively for Block 17 (Dalia, Pazflor, CLOV). Azule uses it for Block 15. It is the standard.

### Free Learning
- **CMG (Computer Modelling Group)** has excellent free student licenses and tutorials: cmgroup.com → Student → Academic
- **Eclipse** is expensive (no free student version for full use), but the DATA file format is open and well-documented. You can write and understand Eclipse input files without the software.

### The Eclipse DATA File — Know This Format

```eclipse
-- Block 32 Example Model (simplified)
-- Comments start with double dash

RUNSPEC
-- Run specification
TITLE
Block32_GD1_Development_Model

DIMENS
-- Grid dimensions: 20x15x8 cells (x, y, z)
20 15 8 /

OIL
WATER
GAS
DISGAS  -- Gas dissolved in oil (solution GOR)
VAPOIL  -- No; comment this out for this black oil model

GRID
-- Grid block dimensions
DX
-- 20x15 values all = 100m (100m x 100m cells)
300*100 /

DZ
-- Thickness by layer
300*3 /  -- Layer 1: 3m thick
300*5 /  -- Layer 2: 5m thick
... (8 layers total)

PORO
-- Porosity for each cell (300 values per layer, 8 layers = 2400 values)
-- From Petrel export
0.28 0.26 0.27 ...

PERMX
-- Permeability in X direction (mD)
-- From Petrel export
450 420 380 ...

SCHEDULE
-- Production schedule
WELSPECS
-- Well name, group, I, J location in grid, datum, fluid
'PROD-1' 'PROD' 10 8 1*  OIL /
'PROD-2' 'PROD' 12 5 1*  OIL /
/

COMPDAT
-- Connection data (well perforations)
-- Well name, I, J, K1, K2, OPEN/SHUT, Sat tab, Trans factor, diameter
'PROD-1' 10 8 3 6 OPEN 1* 1* 0.21 /  -- Perforated in layers 3-6
/

WCONPROD
-- Production constraints
-- Well name, OPEN/SHUT, ORAT, WRAT, GRAT, LRAT, BHP
'PROD-1' OPEN ORAT 5000 1* 1* 1* 200 /  -- Target 5000 STB/day, min BHP 200 bar
/

TSTEP
-- Time steps (days)
30 30 60 60 365 365 365 /

END
```

Study this structure. When you interview for reservoir engineering, mentioning "I've read Eclipse DATA file syntax and understand the GRID, PROPS, SOLUTION, and SCHEDULE sections" is exceptional for a graduate.

---

## Python for Petroleum Engineering — Build Your Portfolio NOW

### Why Python is Your Hidden Weapon

Angola has ~150+ petroleum engineers working for major companies. How many of them can write Python for production data analysis? Fewer than 10. If you can:
- Write a script to process a CSV of daily production rates and fit a decline curve
- Build a Prosper-like IPR/VLP intersection solver in Python
- Create automated plots from PI Historian data

You are immediately valuable to any technical team. Production decline analysis that takes a PE 2 hours in Excel takes 5 seconds in Python — and you can run it for all 30 wells simultaneously.

### Install Your Environment

```bash
# Windows: Install Miniconda
# https://docs.conda.io/en/latest/miniconda.html

# Create a petroleum engineering environment
conda create -n peteng python=3.11
conda activate peteng
conda install numpy pandas matplotlib scipy jupyter
pip install pyXLL  # Excel integration (optional)

# Verify
python -c "import numpy; print('Ready!')"
```

### Project 1: Decline Curve Analysis (Arps)

```python
# decline_curve.py
# Fit Arps exponential decline to Angola well production data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ─── Simulated production data: Block 17 Well G-01 ─────────────────
# In real life this comes from PI Historian or the daily production report
months = np.arange(0, 36, 1)  # 36 months of production
qi = 6200  # initial rate STB/day
Di = 0.06  # annual decline rate (6%/year = 0.5%/month)
q_observed = qi * np.exp(-Di/12 * months) + np.random.normal(0, 150, len(months))
q_observed = np.maximum(q_observed, 0)  # can't be negative

# ─── Create a DataFrame ────────────────────────────────────────────
df = pd.DataFrame({'month': months, 'rate': q_observed})

# ─── Fit exponential decline (Arps b=0) ───────────────────────────
def exponential_decline(t, qi, Di_monthly):
    return qi * np.exp(-Di_monthly * t)

# Fit using scipy curve_fit
popt, pcov = curve_fit(exponential_decline, months, q_observed, p0=[6000, 0.005])
qi_fit, Di_fit_monthly = popt
Di_fit_annual = Di_fit_monthly * 12

print(f"Fitted Initial Rate (qi): {qi_fit:.0f} STB/day")
print(f"Fitted Decline Rate (Di): {Di_fit_annual*100:.1f}%/year")

# ─── Forecast to 60 months ────────────────────────────────────────
months_forecast = np.arange(0, 72, 1)
q_forecast = exponential_decline(months_forecast, qi_fit, Di_fit_monthly)

# ─── Economic limit calculation ───────────────────────────────────
q_economic_limit = 500  # STB/day (below this: abandon)
t_abandon = -np.log(q_economic_limit / qi_fit) / Di_fit_monthly
print(f"Economic limit reached at month: {t_abandon:.1f} ({t_abandon/12:.1f} years)")

# ─── Cumulative Production (EUR) ──────────────────────────────────
# Integrate: EUR = qi/Di * (1 - exp(-Di*t_abandon))
EUR = (qi_fit / Di_fit_monthly) * (1 - np.exp(-Di_fit_monthly * t_abandon))
EUR_MMbbls = EUR / 1e6 * 30  # convert to million barrels (30 days/month)
print(f"EUR (Estimated Ultimate Recovery): {EUR_MMbbls:.2f} MMbbl")

# ─── Plot ─────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Linear scale
ax1.scatter(months, q_observed, color='steelblue', alpha=0.6, label='Historical data', zorder=3)
ax1.plot(months_forecast, q_forecast, 'r-', linewidth=2, label=f'Forecast (Di={Di_fit_annual*100:.1f}%/yr)')
ax1.axhline(y=q_economic_limit, color='gray', linestyle='--', label='Economic limit (500 bbl/d)')
ax1.axvline(x=t_abandon, color='darkred', linestyle=':', alpha=0.7, label=f'Abandonment: month {t_abandon:.0f}')
ax1.set_xlabel('Month')
ax1.set_ylabel('Oil Rate (STB/day)')
ax1.set_title('Block 17 Well G-01 — Decline Curve Analysis')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Semi-log scale
ax2.semilogy(months, q_observed, 'o', color='steelblue', alpha=0.6, label='Historical data', zorder=3)
ax2.semilogy(months_forecast, q_forecast, 'r-', linewidth=2, label='Exponential fit')
ax2.axhline(y=q_economic_limit, color='gray', linestyle='--')
ax2.set_xlabel('Month')
ax2.set_ylabel('Oil Rate (STB/day, log scale)')
ax2.set_title('Semi-Log: Confirms Exponential Decline')
ax2.legend()
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('G01_decline_curve.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Save this, run it, put the output plot on your GitHub portfolio page.** When a production engineer sees this in your portfolio, they will hire you.

---

### Project 2: Mud Weight Window Calculator

```python
# mud_window.py
# Calculate pore pressure, fracture gradient and mud weight window with depth
# Angola deepwater well (Block 32 example)

import numpy as np
import matplotlib.pyplot as plt

# ─── Depth vector ──────────────────────────────────────────────────
tvd = np.linspace(0, 5000, 500)  # TVD in meters

# ─── Water depth: 1,850m (Block 32) ────────────────────────────────
water_depth = 1850
seawater_density = 1.025  # SG

# ─── Pore pressure ─────────────────────────────────────────────────
# Hydrostatic gradient from surface (seawater + formation water)
# Simplified: normally pressured = 0.433 psi/ft = 0.098 bar/m * SG
def pore_pressure_SG(tvd, water_depth):
    """Return pore pressure gradient as SG equivalent at each depth"""
    # Normal hydrostatic throughout (simplified)
    # More complex: use seismic velocity or Eaton's method in practice
    pp = np.where(tvd <= water_depth,
                  seawater_density,  # In water column
                  1.03 + 0.02 * np.maximum(0, (tvd - water_depth - 2000) / 1000))  # Overpressure below 2000m sub-seabed
    return pp

# ─── Fracture gradient ─────────────────────────────────────────────
def fracture_gradient_SG(tvd, water_depth):
    """Simplified fracture gradient — typically 80-90% between PP and OB"""
    overburden = np.where(tvd <= water_depth, seawater_density, 1.9)  # Overburden SG
    pp = pore_pressure_SG(tvd, water_depth)
    # Hubbert-Willis approximation: FG ≈ (OB + 2*PP) / 3
    fg = (overburden + 2 * pp) / 3
    return np.minimum(fg, overburden * 0.88)  # cap at 88% of overburden

# ─── Calculate windows ─────────────────────────────────────────────
pp = pore_pressure_SG(tvd, water_depth)
fg = fracture_gradient_SG(tvd, water_depth)
mw_actual = pp + 0.06  # Mud weight = pore pressure + 0.06 SG overbalance
ecd = mw_actual + 0.05  # ECD = mud weight + circulating friction (simplified)

# ─── Plot ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 12))

ax.plot(pp, tvd, 'b-', linewidth=2, label='Pore Pressure (SG)')
ax.plot(fg, tvd, 'r-', linewidth=2, label='Fracture Gradient (SG)')
ax.plot(mw_actual, tvd, 'g--', linewidth=2, label='Mud Weight Plan (SG)')
ax.plot(ecd, tvd, 'g:', linewidth=1.5, label='ECD (SG)')
ax.fill_betweenx(tvd, pp, fg, alpha=0.1, color='green', label='Safe drilling window')
ax.axhline(y=water_depth, color='cyan', linestyle='-', linewidth=1, alpha=0.7, label=f'Mudline ({water_depth}m)')

ax.invert_yaxis()  # Depth increases downward
ax.set_xlabel('Equivalent Density (SG)')
ax.set_ylabel('TVD (m)')
ax.set_title('Mud Weight Window — Block 32 Deepwater Well')
ax.legend(loc='lower left')
ax.grid(True, alpha=0.3)
ax.set_xlim([0.8, 2.5])

plt.tight_layout()
plt.savefig('mud_weight_window.png', dpi=150)
plt.show()
```

---

### Project 3: Gas Lift Optimization (The One That Impresses Most)

```python
# gas_lift_optimization.py
# Allocate available GL gas to maximize FPSO oil production
# Using equal incremental principle (Economic Optimization)

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# ─── Performance curves for 5 wells (GL injection rate → oil rate) ─
# In real practice these come from Prosper models for each well
well_data = {
    'G-01': ([0, 1, 2, 3, 4, 5, 6, 7, 8], [2800, 4100, 5200, 6000, 6600, 6900, 7100, 7200, 7250]),
    'G-02': ([0, 1, 2, 3, 4, 5, 6, 7, 8], [3200, 4600, 5600, 6200, 6650, 6900, 7000, 7050, 7080]),
    'G-03': ([0, 1, 2, 3, 4, 5, 6, 7, 8], [1500, 2800, 3900, 4700, 5300, 5700, 5950, 6050, 6100]),
    'G-04': ([0, 1, 2, 3, 4, 5, 6, 7, 8], [2200, 3300, 4100, 4750, 5200, 5500, 5650, 5720, 5750]),
    'G-05': ([0, 1, 2, 3, 4, 5, 6, 7, 8], [4000, 5500, 6500, 7100, 7500, 7700, 7800, 7850, 7870]),
}

# Interpolate performance curves
curves = {}
for well, (gl, rate) in well_data.items():
    curves[well] = interp1d(gl, rate, kind='cubic', fill_value='extrapolate')

# ─── Available gas ──────────────────────────────────────────────────
G_total = 20.0  # MMscfd total available

# ─── Optimization: equal incremental returns ───────────────────────
# We use a discrete search: try all combinations at 0.5 MMscfd steps
# (In practice: gradient method or LP solver)

step = 0.5
G_options = np.arange(0, 8 + step, step)
n_wells = len(well_data)
wells = list(well_data.keys())

# Calculate incremental oil for each additional 0.5 MMscfd per well
# Then fill the "best increment" first (greedy algorithm)
allocation = {w: 0.0 for w in wells}
G_used = 0.0

for iteration in range(int(G_total / step)):
    best_well = None
    best_incr = -1e9
    for well in wells:
        current_rate = curves[well](allocation[well])
        new_rate = curves[well](allocation[well] + step)
        incremental = new_rate - current_rate
        if incremental > best_incr:
            best_incr = incremental
            best_well = well
    allocation[best_well] += step
    G_used += step

# ─── Results ───────────────────────────────────────────────────────
print("=" * 50)
print("Optimal Gas Lift Allocation")
print("=" * 50)
total_oil = 0
for well in wells:
    rate = curves[well](allocation[well])
    total_oil += rate
    print(f"{well}: GL = {allocation[well]:.1f} MMscfd → Oil = {rate:.0f} STB/day")

print(f"\nTotal GL used: {sum(allocation.values()):.1f} / {G_total:.1f} MMscfd")
print(f"Total Oil Production: {total_oil:,.0f} STB/day")

# Compare to equal distribution baseline
equal_alloc = G_total / n_wells
total_equal = sum(curves[w](equal_alloc) for w in wells)
print(f"\nEqual distribution baseline: {total_equal:,.0f} STB/day")
print(f"Optimization gain: {total_oil - total_equal:,.0f} STB/day (+{(total_oil/total_equal-1)*100:.1f}%)")
```

---

## What to Put on Your CV — Software Section

**Before you have the software but have done the exercises:**
> "Petroleum engineering software: Prosper (self-study, IPR/VLP modelling concepts), Eclipse (DATA file syntax and simulation workflow), Python (Arps decline curve fitting, gas lift optimization, mud weight window analysis). Working toward formal proficiency via student license applications."

**After you get free student licenses:**
> "Prosper (student license: nodal analysis, gas lift valve design, ESP sizing), Petrel (student license: well correlation, property modelling, STOIIP calculation), Python (pandas, numpy, scipy: production data analysis, decline curve fitting), Microsoft Excel (advanced: automated production reports, Solver optimization)."

---

## Practical Exercises — Do These This Week

### Exercise 1: Download and Install
1. Download Python (via Miniconda)
2. Install: `pip install numpy pandas matplotlib scipy jupyter`
3. Run the decline curve code above
4. Modify qi to 8000 STB/day and Di to 8%/year
5. What is the new EUR?

### Exercise 2: IPR Nodal Analysis
1. Run the IPR Python code from Project 1 (modify the constants)
2. Try three gas lift scenarios: no GL (A=2800), moderate GL (A=1600), heavy GL (A=1200)
3. What is the production rate difference between scenarios?
4. Plot all three on one graph

### Exercise 3: Mud Window
1. Run the mud weight window code
2. Change water depth to 800m (shallow water Block 0 scenario) and replot
3. How does the safe drilling window change with shallow vs deepwater?

### Exercise 4: Find and Review Real Software
1. Go to petex.com → Request student license for Prosper/GAP/MBAL
2. Go to cmgroup.com → Academic → Request CMG student license (full Eclipse-class simulator, free)
3. Watch one tutorial video (30 minutes) and write 5 things you learned

---

## The "Portfolio Proof" Principle

**Every software skill needs a proof artifact.** When you apply to SLB or TotalEnergies, you need to be able to show work — not just claim it. Here's what to build:

1. **GitHub repository** called `petroleum-engineering-scripts`
2. Upload your:
   - Decline curve analysis script + plot output
   - IPR/VLP nodal analysis + plot
   - Mud weight window calculator
   - Gas lift optimization (if you get there)
3. **README.md** for the repo: "Python tools for petroleum engineering analysis. Applications to Angola deepwater well performance."

Put the GitHub link on your CV. Any technical interviewer who clicks it will immediately know you are serious.

---

*Related: [05_Reservoir_Engineering_Tutorial.md](05_Reservoir_Engineering_Tutorial.md) | [09_Production_Engineering_Tutorial.md](09_Production_Engineering_Tutorial.md) | [discipline/05_Digital_PE_Data_Science.md](../discipline/05_Digital_PE_Data_Science.md)*  
*Free student software directory: [Learning Resources — Software](../../../docs/learning-resources.md#software--free-student-access)*
