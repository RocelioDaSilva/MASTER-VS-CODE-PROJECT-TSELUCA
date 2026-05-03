# CÃ¡lculo I

**Ano:** 1Âº | **Semestre:** 1Âº | **Sector:** All (Upstream, Midstream, Downstream)

---

## What You Learned

Limits, derivatives, integrals of single-variable functions, the fundamental theorem of calculus, applications of derivatives (optimization, rates of change), and basic integration techniques. You learned to quantify how things change.

## Where This Subject Is Used in Industry

- **Flow Rate Calculations:** Flow rate is the derivative of cumulative production with respect to time: $q = \frac{dN_p}{dt}$. Decline curve analysis â€” the most common reservoir engineering tool â€” uses exponential and hyperbolic functions you learned here.
- **Hydrostatic Pressure:** Pressure at depth = integral of fluid density over the depth interval: $P = \int_0^h \rho g \, dz$. This is used every day in drilling (mud weight selection) and [well control](../../../docs/skills/01-well-control.md).
- **Darcy's Law (Radial Flow):** The radial inflow equation involves logarithmic functions: $q = \frac{2\pi k h \Delta P}{\mu \ln(r_e/r_w)}$. Understanding the logarithm and its derivative is essential.
- **Optimization:** Drilling engineers optimize Rate of Penetration (ROP) by adjusting Weight on Bit (WOB) and RPM â€” this is a multivariable optimization problem that starts with single-variable calculus concepts.
- **Pipeline Flow:** Pressure drop along a pipeline is calculated using integrals over the pipe length, accounting for elevation changes and friction.

## Angola-Specific Context

Every quantitative calculation in petroleum engineering â€” whether you are computing the volume of oil in a reservoir, the pressure at the bottom of a 2,000m deep well, or the economic value of a production stream â€” begins with calculus. No employer will ask you to "do calculus" explicitly, but every formula you will use daily was derived from it.

## ðŸ” Your Reflection Task

*"If I know the production rate of an Angola well declines exponentially as $q(t) = q_i \cdot e^{-Dt}$, how would I use integration to calculate the total oil produced between month 0 and month 24?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
