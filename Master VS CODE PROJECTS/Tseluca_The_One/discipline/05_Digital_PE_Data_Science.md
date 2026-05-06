# Digital Petroleum Engineering and Data Science
## The Fastest-Growing Skill Set in the Industry

---

## Why This Section Exists in a Petroleum Engineering Guide

Five years ago, knowing Python was optional for a petroleum engineer. Today, it is quickly becoming a baseline expectation — the same way knowing Excel was mandatory in 2010.

The oil industry generates enormous volumes of data: pressure gauges transmitting every second, production rates logged every minute, seismic surveys covering entire blocks, well logs measured every 0.15m. The engineers who can work with this data systematically — not just look at it in spreadsheets — are becoming the most valuable technical people in the industry.

This is not about replacing engineers with algorithms. It is about amplifying what good engineers can do.

---

## The Digital Petroleum Engineering Stack

### Layer 1: Data Collection (Sensors and Instrumentation)

**What generates data in upstream petroleum:**
- **Downhole gauges:** Temperature and pressure gauges installed in producing wells, transmitting data every 1–60 seconds via fibre optic or electrical cable to surface
- **FPSO process sensors:** Flow meters, pressure transmitters, temperature sensors across the entire FPSO process — thousands of data points, logged every 1–10 seconds
- **Production logging tools (PLT):** Wireline-deployed sensors that profile inflow contribution from each zone while the well is producing
- **MWD/LWD:** Real-time downhole data during drilling (gamma ray, resistivity, weight on bit, RPM, temperature)
- **ROV inspection cameras:** Video and sonar data from subsea inspections
- **Seismic 4D:** Time-lapse seismic surveys that reveal how the reservoir changes over time

**The volume:** A single producing FPSO may generate 50–100 GB of time-series data per day. A full seismic survey for one Angola block generates 10–50 TB.

### Layer 2: Data Storage and Historians

**SCADA and historians:**
- SCADA (Supervisory Control and Data Acquisition): the real-time monitoring and control system on the FPSO
- PI Historian (OSIsoft/AVEVA): the standard data historian in upstream petroleum. Stores time-series SCADA data with high efficiency. All major Angola operators use PI.
- Data lakes: increasingly used to store structured and unstructured data (sensor data, documents, images)

**What you need to know:** PI Historian is the gateway to all FPSO production data. Learn to query PI data using PI DataLink (Excel add-in) and PI Web API (REST-based access for Python). This is the first practical digital skill that gets you hired.

### Layer 3: Data Processing and Engineering Analysis

This is where Python comes in.

**Python for petroleum engineers — the essential toolkit:**

```python
# The core petroleum engineering Python stack
import pandas as pd          # Data manipulation (production tables, well data)
import numpy as np           # Numerical calculations (Darcy, Vogel, Arps equations)
import matplotlib.pyplot as plt  # Plotting (production profiles, IPR curves)
import scipy.optimize as opt  # Curve fitting (Arps decline fitting)
import scipy.stats as stats   # Statistical analysis (P10/P50/P90)
```

**What you can build with these five libraries:**

1. **Automated decline curve analysis:**
```python
def arps_exponential(t, qi, di):
    """Exponential decline: q(t) = qi * exp(-di * t)"""
    return qi * np.exp(-di * t)

# Fit the curve to actual production data
from scipy.optimize import curve_fit
popt, pcov = curve_fit(arps_exponential, time_data, rate_data)
qi_fitted, di_fitted = popt

# Forecast
time_forecast = np.arange(0, 20, 1/12)  # 20 years monthly
rate_forecast = arps_exponential(time_forecast, qi_fitted, di_fitted)
cumulative_forecast = np.cumsum(rate_forecast / 12)  # Approximate cumulative
```

2. **Well performance dashboard:**
```python
# Load PI historian data (or CSV export)
df = pd.read_csv('well_A15_production.csv', parse_dates=['datetime'])
df['PI'] = df['liquid_rate'] / (df['reservoir_pressure'] - df['FBHP'])
df['PI_rolling'] = df['PI'].rolling(7).mean()

# Flag wells with PI decline
threshold = 0.85  # 15% decline from 30-day baseline
baseline_PI = df.PI_rolling.head(30).mean()
flagged = df[df['PI_rolling'] < baseline_PI * threshold]
```

3. **Gas lift optimisation:**
```python
# Given 15 wells and 10 MMscf/day total gas availability
# Maximise total production
from scipy.optimize import minimize

def neg_total_production(gas_allocation, well_models):
    """Negative total production (we minimise the negative = maximise production)"""
    total = 0
    for i, model in enumerate(well_models):
        total += model.calculate_production(gas_allocation[i])
    return -total

constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - total_gas_available}
bounds = [(0, max_per_well)] * n_wells
result = minimize(neg_total_production, x0=initial_allocation,
                  method='SLSQP', constraints=constraints, bounds=bounds)
```

---

### Layer 4: Machine Learning in Petroleum Engineering

Machine learning is not magic. In petroleum engineering, it is a statistical tool for finding patterns in data. Here are the applications that are actually used in Angola operations today:

#### A. Production Anomaly Detection

**Problem:** With 20 wells producing on an FPSO, finding early signs of equipment failure in 100,000+ daily readings is humanly impossible to do manually.

**ML solution:** Train an anomaly detection model on historical "normal" production data. When current data deviates significantly from the model's expectation, flag it for engineer review.

**Algorithm used:** Isolation Forest, LSTM (Long Short-Term Memory), or simple z-score deviation detection.

**Angola application:** TotalEnergies Exploration & Production uses production anomaly detection on their Angola assets. One system detects ESP motor temperature anomalies 3–7 days before the actual failure — allowing planned replacement rather than emergency workover.

#### B. Well Test Interpretation (Automated PTA)

**Problem:** Pressure transient analysis (PTA) involves manually fitting type curves to pressure buildup data — a skill requiring years of experience.

**ML solution:** Train a neural network on thousands of synthetic PTA datasets (with known k, h, skin). The network learns to estimate k, h, and skin from the pressure transient data directly.

**Status:** Several service companies (SLB, Halliburton) have internal tools. Research-stage for most operators.

#### C. Seismic Interpretation and Facies Classification

**Problem:** Manually interpreting seismic attributes to classify reservoir facies (channels, lobes, mudstone barriers) takes weeks for experienced geophysicists.

**ML solution:** Supervised classification using convolutional neural networks (CNNs) trained on labelled seismic data. The network learns what different facies look like in seismic attributes.

**Angola application:** TotalEnergies has used ML seismic interpretation on Block 17 and Block 32 datasets. Results validated against well data.

#### D. Drilling Optimization (ROP Prediction)

**Problem:** Optimal drilling parameters (WOB, RPM, flow rate) that maximise ROP change with formation type. Manual adjustment is slow and relies on experience.

**ML solution:** Regression models trained on past well data predict optimal drilling parameters for the current formation (identified by gamma ray, resistivity from MWD).

**Current use:** SLB's PERFORM suite and Halliburton's iCruise have embedded ML models for real-time drilling optimisation. SLB has used this on Angola deepwater wells.

---

### Layer 5: Digital Twins

A digital twin is a real-time, continuously updated computational model of a physical asset.

**FPSO digital twin:**
- A real-time simulation of the FPSO process (separators, compressors, water treatment)
- Fed with live SCADA data from the FPSO
- Predicts: how will the FPSO behave if I close this valve? If I increase gas compression to 110%?
- Used for: process optimisation, operator training, maintenance planning

**Angola context:** SBM Offshore (FPSO operator for several Angola FPSOs) has implemented digital twins for their FPSO fleet, including Angola assets. They use it for remote operations support from their Rotterdam and Monaco offices.

**Well digital twin:**
- Real-time well model (Prosper equivalent) fed with live downhole gauge data
- Alerts when actual production deviates from model prediction
- Enables remote production engineers to monitor Angola wells from Luanda office

---

## Python Skills Roadmap for Petroleum Engineers

This is a structured learning path from zero to productive in 6 months.

### Month 1–2: Foundations
```
Goal: Understand Python basics and data manipulation

Topics:
- Python syntax, data types, functions, loops
- pandas DataFrames (read CSV, filter, aggregate, plot)
- numpy arrays and basic math
- matplotlib plotting

Practice project: Load Angola production data CSV, calculate monthly averages,
plot production rate vs time for each well.
```

### Month 3–4: Petroleum Engineering Applications
```
Goal: Implement PE equations in Python

Topics:
- Arps decline curve fitting (scipy.optimize.curve_fit)
- IPR/VLP calculation and plotting
- Material balance calculation
- Volumetric STOIIP calculation
- Monte Carlo simulation (numpy.random)

Practice project: Build an Arps decline analyser:
input = production history CSV
output = qi, Di, b fitted; 10-year production forecast; EUR at P10/P50/P90
```

### Month 5–6: Data Integration and Automation
```
Goal: Automate reporting and integrate with industry data systems

Topics:
- PI Web API access (HTTP requests, JSON parsing)
- Automated PDF/Excel report generation (openpyxl, reportlab)
- Dashboard creation (Plotly Dash or Streamlit)
- Basic machine learning (scikit-learn: regression, anomaly detection)

Practice project: Build a well surveillance dashboard:
- Reads daily production data from CSV (or PI API)
- Calculates PI and flags declining wells
- Generates weekly PDF report automatically
```

### Key Resources (All Free)
- **Python basics:** Python.org official tutorial, Real Python (realpython.com)
- **Pandas/numpy:** pandas documentation, "Python for Data Analysis" (Wes McKinney — check ISPTEC library)
- **Petroleum-specific:** Yohanes Nuwara's `petrodc` and `well-profile` Python packages (GitHub, open source)
- **SPE resources:** SPE has Python workshops at every Annual Technical Conference (free for student members)
- **Course:** Coursera "Applied Data Science with Python" (University of Michigan) — $50/month, worth every kwanza

---

## The Digital PE Career Path in Angola

### Current Landscape (2026)
Every major Angola operator has or is building a digital/data team:
- **TotalEnergies Angola:** Digital POAP team (Production Optimisation and Asset Performance) — uses Python, PI, and ML tools
- **Azule Energy:** Implementing integrated digital operations platform post-merger
- **Eni Angola:** Connected operations centre in Rome with Angola real-time data feeds
- **Sonangol EP:** Sonangol Digital — building data engineering capability
- **SLB:** Angola Petrotechnical Center in Luanda uses Delfi cloud platform

### Entry Roles for Digital PE
- **Production Data Analyst:** Extract and analyse production data, automate reports. Requires Excel + Python + PI access.
- **Digital Asset Performance Engineer:** Run and maintain integrated production models, production digital twins. Requires Prosper + GAP + Python.
- **Reservoir Data Analyst:** Run simulation cases, manage model databases, analyse 4D seismic results. Requires Eclipse/CMG + Python + GIS basics.
- **Drilling Data Engineer:** Real-time drilling parameter analysis, ROP optimisation support. Requires MWD data processing, Python.

### Career Positioning
Being a petroleum engineer with strong data skills places you in the most in-demand category in 2026. Companies are struggling to find engineers who understand petroleum physics AND can code. You do not need to be a software engineer. You need to be a petroleum engineer who uses Python fluently.

---

## What to Build Before Your First Interview

Create a GitHub portfolio with 2–3 projects. Example projects that impress petroleum engineering hiring managers:

**Project 1: Decline Curve Analyser**
- Input: CSV of well production history
- Output: Fitted Arps parameters, production forecast, EUR
- Extra: Interactive plot with Plotly

**Project 2: Angola Field Production Dashboard**
- Use public Sonangol or Angola EITI data (open data)
- Build a Streamlit dashboard showing Angola block production by operator
- Include forecast using fitted decline curves

**Project 3: Well Performance Surveillance Tool**
- Calculate PI trends for multiple wells
- Flag declining wells with automated alerts
- Generate weekly HTML report

These projects demonstrate that you can do real work, not just answer textbook questions. Post them to GitHub and include the link on your CV.

---

## Interview Questions for Digital PE Roles

1. What Python libraries do you use for petroleum engineering data analysis? Give a specific example of something you have built.
2. What is a PI historian and how would you access data from it using Python?
3. Explain Arps decline curve fitting. Which Python function would you use to fit the parameters?
4. What is a digital twin in the context of an FPSO? What data feeds it and what questions can it answer?
5. Describe a production anomaly detection system. What data would it use and what algorithm would you recommend?
6. What is the difference between supervised and unsupervised machine learning? Give a petroleum engineering example of each.
7. How would you optimise gas lift allocation across 15 wells using Python?
8. What is the risk of using ML models in production-critical decisions? How would you mitigate it?
9. What open-source tools exist for petroleum data analysis?
10. How does 4D seismic work and what ML methods are used to interpret it?

---

*Next: [06_Integrated_Subsurface_Discipline.md](06_Integrated_Subsurface_Discipline.md) — how reservoir engineering, geology, and petrophysics work together as an integrated subsurface team.*  
*Courses, books, software: [Learning Resources](../../../docs/learning-resources.md)*
