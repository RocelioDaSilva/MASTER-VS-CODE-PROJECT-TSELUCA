# CÃ¡lculo IV

**Ano:** 3Âº | **Semestre:** 2Âº | **Sector:** Upstream

---

## What You Learned

Partial differential equations (PDEs): classification (elliptic, parabolic, hyperbolic), separation of variables, Fourier transforms, boundary value problems, and applications to heat conduction, wave propagation, and diffusion.

## Where This Subject Is Used in Industry

- **Reservoir Flow Equations:** The diffusivity equation â€” the fundamental PDE governing pressure and fluid flow in reservoirs â€” is a parabolic PDE. All of well test analysis and reservoir simulation is solving this equation with different boundary conditions.
- **Heat Equation (Pipeline Cooling):** The temperature profile along a subsea flowline as hot oil cools toward seabed temperature is governed by the heat equation â€” a parabolic PDE. [Flow assurance](../../../docs/skills/10-flow-assurance.md) engineers solve this to determine insulation requirements.
- **Seismic Wave Propagation:** The wave equation (hyperbolic PDE) governs seismic wave propagation. Solving it numerically (reverse-time migration, full waveform inversion) is how modern seismic images are created.
- **Wellbore Stability:** Stress distribution around a wellbore is governed by Kirsch's equations â€” solutions to an elliptic PDE (Laplace equation in polar coordinates).

## Angola-Specific Context

Every piece of petroleum engineering software you will use (Eclipse, CMG, OLGA, PIPESIM, Saphir) is solving PDEs numerically. The engineer who understands the underlying PDE â€” its type, boundary conditions, and solution behavior â€” can troubleshoot model problems that a button-pusher cannot. This separates senior engineers from junior ones.

## ðŸ” Your Reflection Task

*"The diffusivity equation in radial coordinates is: $\frac{\partial^2 P}{\partial r^2} + \frac{1}{r}\frac{\partial P}{\partial r} = \frac{\phi \mu c_t}{k} \frac{\partial P}{\partial t}$. Can I identify this as a parabolic PDE, explain what each term represents physically, and describe how the solution behaves at early and late times?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
