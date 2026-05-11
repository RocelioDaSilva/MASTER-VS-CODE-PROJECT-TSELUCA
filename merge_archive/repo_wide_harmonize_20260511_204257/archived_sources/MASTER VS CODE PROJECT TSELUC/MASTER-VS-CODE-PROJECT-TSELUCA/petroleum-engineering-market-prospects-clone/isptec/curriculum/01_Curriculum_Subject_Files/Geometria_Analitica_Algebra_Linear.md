# Geometria AnalÃ­tica e Ãlgebra Linear

**Ano:** 1Âº | **Semestre:** 2Âº | **Sector:** Upstream (Drilling, Reservoir)

---

## What You Learned

Vectors, matrices, linear systems, eigenvalues/eigenvectors, coordinate transformations (rotation, translation), conic sections, planes and lines in 3D space. You learned to solve systems of linear equations and represent geometric objects algebraically.

## Where This Subject Is Used in Industry

- **[Directional Drilling](../../../docs/skills/05-directional-drilling.md) / Well Trajectory:** The 3D path of a well through the earth is described using vectors. Inclination, azimuth, measured depth, and true vertical depth are connected by coordinate transformations. The **minimum curvature method** â€” the standard survey calculation used on every drilling rig â€” is a vector calculation that converts downhole survey data (inclination + azimuth at each station) into 3D coordinates (North, East, TVD). This is algebra linear applied directly.
- **Reservoir Simulation:** Reservoir simulators (Eclipse, CMG) solve massive systems of linear equations (Ax = b) at every timestep. The grid has thousands of cells; each cell has pressure, saturation, and composition unknowns. Solving this requires matrix operations â€” Gaussian elimination, LU decomposition, iterative solvers.
- **Geostatistics / Kriging:** Kriging (used to map reservoir properties between wells) involves solving systems of linear equations where the matrix represents spatial correlation.
- **Seismic Processing:** Coordinate transformations between surface, depth, and time domains use rotation matrices and linear algebra.
- **Structural Analysis:** Stress tensors in rock mechanics are 3Ã—3 matrices. Principal stresses (the most important parameters for wellbore stability) are eigenvalues of the stress tensor.

## Angola-Specific Context

Angola's deepwater wells routinely have complex 3D trajectories â€” S-shaped wells, horizontal wells, and multilateral wells. On Block 17, some wells deviate 3â€“4 km horizontally from the subsea wellhead to reach the target reservoir. Every meter of that trajectory was calculated using the vector and matrix math from this course.

## ðŸ” Your Reflection Task

*"If I were an [MWD](../../../docs/glossary.md) Engineer and received a survey reading of inclination = 45Â° and azimuth = 220Â° at measured depth 3,500m, how would I use vector decomposition (from this course) to calculate the North, East, and TVD coordinates of that survey station?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
