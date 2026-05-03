# CÃ¡lculo NumÃ©rico

**Ano:** 3Âº | **Semestre:** 1Âº | **Sector:** Upstream (Reservoir Simulation)

---

## What You Learned

Numerical methods for solving equations: root finding (bisection, Newton-Raphson), interpolation (Lagrange, splines), numerical integration (trapezoidal, Simpson's), numerical differentiation, linear system solvers (Gaussian elimination, LU decomposition, iterative methods), and numerical solutions to ordinary differential equations (Euler, Runge-Kutta).

## Where This Subject Is Used in Industry

- **Reservoir Simulation:** Every reservoir simulator (Eclipse, CMG, tNavigator) solves the reservoir flow equations numerically. The reservoir is divided into grid cells, and at each timestep, the simulator solves a massive system of nonlinear equations using Newton-Raphson iteration with linear solvers (IMPES or fully implicit). This is numerical methods at industrial scale.
- **Pressure Transient Analysis:** The analytical solutions for well test interpretation use series expansions and special functions. Numerical methods are used when the analytical solution is too complex (e.g., multilayer, composite, or fractured reservoirs).
- **Nodal Analysis:** Finding the operating point of a well (intersection of IPR and VLP curves) is a root-finding problem â€” solved by bisection or Newton-Raphson.
- **Pipeline Simulation:** OLGA (transient multiphase flow simulator) solves the conservation equations (mass, momentum, energy) using finite difference methods â€” numerical calculus applied to pipes.
- **History Matching:** Adjusting reservoir model parameters to match observed production data is a nonlinear optimization problem solved numerically.

## Angola-Specific Context

Reservoir simulation is one of the most computationally intensive activities in petroleum engineering. [TotalEnergies](../../../data/company-directory/totalenergies.md) runs full-field simulations of Block 17 reservoirs with millions of grid cells â€” each timestep involves solving millions of equations. The engineer who understands what the simulator is doing numerically (not just pushing buttons) can diagnose convergence problems, select appropriate timestep sizes, and validate results. That engineer is the one who gets promoted.

## ðŸ” Your Reflection Task

*"If a reservoir simulator fails to converge at a particular timestep, what numerical concept from this course would help me diagnose whether the problem is the linear solver, the Newton-Raphson iteration, or the grid resolution?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
