# CÃ¡lculo III

**Ano:** 2Âº | **Semestre:** 2Âº | **Sector:** Upstream, Midstream

---

## What You Learned

Sequences and series, Fourier series, ordinary differential equations (first-order, second-order, linear, separable), Laplace transforms, and applications of ODEs to physical systems. You learned to model dynamic systems mathematically.

## Where This Subject Is Used in Industry

- **Pressure Transient Analysis:** When a well is shut in for a buildup test, the pressure at the wellbore changes over time according to a partial differential equation (the diffusivity equation). The analytical solution involves exponential integrals and Bessel functions â€” which arise from solving differential equations. Interpreting a welltest is interpreting the solution of a PDE.
- **Decline Curve Analysis:** Arps' exponential decline equation $q = q_i e^{-Dt}$ is the solution to a first-order ODE: $\frac{dq}{dt} = -Dq$. The hyperbolic decline equation is a more general ODE solution.
- **ESP Motor Control:** Electrical Submersible Pumps use Variable Speed Drives (VSD) whose control theory is based on differential equations â€” the response of motor speed and torque to electrical input.
- **Pipeline Transient Flow:** Water hammer and pressure surges in pipelines are modeled by the wave equation â€” a second-order PDE. The method of characteristics used to solve it numerically was built on ODE theory.
- **Heat Transfer:** Cooling of a pipeline on the seabed (critical for [flow assurance](../../../docs/skills/10-flow-assurance.md)) follows Newton's law of cooling â€” a first-order ODE: $\frac{dT}{dt} = -hA(T - T_{seabed})$.

## Angola-Specific Context

Pressure transient analysis is performed on Angola wells to determine reservoir permeability and skin â€” the parameters that determine how much a well can produce. Every new well drilled on Block 17 or 32 undergoes a well test. The interpretation is done using software (Saphir, PanSystem) that solves differential equations â€” but the engineer must understand the physics behind the math to validate the software output.

## ðŸ” Your Reflection Task

*"If I observed that an Angola well's production rate followed $q(t) = 5000 \cdot e^{-0.02t}$ (bbl/day), what ODE does this solve, and what physical process leads to this exponential behavior?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
