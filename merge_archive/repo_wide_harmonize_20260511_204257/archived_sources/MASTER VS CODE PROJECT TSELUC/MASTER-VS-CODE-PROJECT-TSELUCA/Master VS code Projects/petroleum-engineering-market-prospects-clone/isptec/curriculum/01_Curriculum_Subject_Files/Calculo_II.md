# CÃ¡lculo II

**Ano:** 2Âº | **Semestre:** 1Âº | **Sector:** Upstream, Midstream

---

## What You Learned

Multivariable calculus: partial derivatives, multiple integrals (double, triple), vector calculus (gradient, divergence, curl), line integrals, surface integrals, and theorems of Green, Gauss, and Stokes. You extended single-variable calculus to functions of two and three variables.

## Where This Subject Is Used in Industry

- **Reservoir Volume Calculations (STOIIP):** Stock Tank Oil Initially In Place is calculated as a volume integral over the reservoir: $\text{STOIIP} = \int \int \int \frac{\phi \cdot (1 - S_w)}{B_o} \, dV$. The reservoir has variable porosity, saturation, and thickness â€” this is a triple integral over irregular geometry.
- **Fluid Flow Equations:** The diffusivity equation (governing pressure propagation in a reservoir) is a partial differential equation: $\frac{\partial^2 P}{\partial r^2} + \frac{1}{r}\frac{\partial P}{\partial r} = \frac{\phi \mu c_t}{k} \frac{\partial P}{\partial t}$. Understanding partial derivatives is essential.
- **Gradient:** The pressure gradient $\nabla P$ determines the direction and magnitude of fluid flow. Fluids flow from high to low pressure â€” the gradient tells you the direction.
- **Pipeline Heat Loss:** Heat transfer along a pipeline is modeled with surface integrals and partial differential equations (temperature as a function of position and time).

## Angola-Specific Context

Reservoir engineers at [TotalEnergies](../../../data/company-directory/totalenergies.md) and Eni in Luanda calculate STOIIP for Angola's turbidite reservoirs every day. The geological model provides a 3D grid of porosity and saturation values. The volume integral is computed numerically by the software â€” but the engineer must understand what the software is doing physically. That understanding comes from this course.

## ðŸ” Your Reflection Task

*"If a reservoir engineer tells me that the STOIIP for a Block 17 reservoir is 500 MMbbl, how was that number calculated? What physical quantities were integrated over what domain?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
