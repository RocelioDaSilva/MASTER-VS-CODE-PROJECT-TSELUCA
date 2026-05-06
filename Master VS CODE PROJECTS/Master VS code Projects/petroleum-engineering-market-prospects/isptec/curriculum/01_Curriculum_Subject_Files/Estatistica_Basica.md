# EstatÃ­stica BÃ¡sica

**Ano:** 2Âº | **Semestre:** 2Âº | **Sector:** Upstream (Reservoir, Exploration)

---

## What You Learned

Descriptive statistics (mean, median, mode, variance, standard deviation), probability distributions (normal, log-normal, uniform), hypothesis testing, confidence intervals, regression analysis, and basic sampling theory.

## Where This Subject Is Used in Industry

- **Reserves Estimation:** Petroleum reserves are never known with certainty. The SPE PRMS reserves classification is inherently probabilistic: Proved (P90 â€” 90% chance of exceeding), Probable (P50), and Possible (P10). Building these probability distributions requires statistics.
- **Monte Carlo Simulation:** To estimate STOIIP, engineers assign probability distributions to porosity, net-to-gross ratio, area, thickness, saturation, and Bo â€” then run thousands of random combinations. The result is a probability distribution of STOIIP. This is Monte Carlo simulation â€” built entirely on statistics.
- **Log-Normal Distribution:** Most petroleum parameters (porosity, permeability, reserves, field sizes) follow a log-normal distribution, not a normal one. Understanding this distribution from this course is essential.
- **Production Data Analysis:** Identifying trends, outliers, and anomalies in production data (is this well really declining, or is it just noise?) requires statistical reasoning.
- **Quality Control:** [Drilling fluids](../../../docs/skills/03-drilling-fluids.md) testing, cement testing, and pressure testing all use statistical process control (mean Â± 2Ïƒ limits) to determine if a measurement is within specification.

## Angola-Specific Context

When [TotalEnergies](../../../data/company-directory/totalenergies.md) reports reserves to the French stock exchange for Block 17, they use probabilistic reserves estimates built from statistical analysis. The difference between P10 and P90 for a single reservoir can be hundreds of millions of barrels â€” and hundreds of millions of dollars in company valuation. Understanding the statistics behind these numbers is non-optional for a reservoir engineer.

## ðŸ” Your Reflection Task

*"If I ran a Monte Carlo simulation with 10,000 iterations for the STOIIP of a Block 32 reservoir, and the P10 was 800 MMbbl and the P90 was 200 MMbbl, what does this range tell me about the uncertainty, and how would it affect the decision to build a $3 billion [FPSO](../../../docs/glossary.md)?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
