# Module 2: Orbital Mechanics and Mission Design

**Duration:** 8 Weeks  
**Goal:** Master the physics of orbital motion and apply it to real mission planning scenarios.

## Projects

1. **[Starlink Orbit Propagator](Projects/Starlink_Propagator/README.md):** Simulates satellite constellation dynamics with J2 perturbation effects.
2. **[Starship Trajectory Planner](Projects/Starship_Trajectory_Planner/README.md):** Plans interplanetary Hohmann transfers and visualizes launch windows via Porkchop Plots.

## Core Concepts

### Keplerian Orbital Elements
Every orbit can be uniquely described by six parameters:
- **a** (Semi-major axis): Size of the orbit
- **e** (Eccentricity): Shape (0 = circle, 0-1 = ellipse, 1 = parabola, >1 = hyperbola)
- **i** (Inclination): Tilt relative to equatorial plane
- **Ω** (RAAN): Where the orbit crosses the equator going north
- **ω** (Argument of Periapsis): Where periapsis is within the orbital plane
- **ν** (True Anomaly): Current position along the orbit

### J2 Perturbations
Earth isn't a perfect sphere—it bulges at the equator. This causes:
- **Nodal Regression:** RAAN drifts over time (used by sun-synchronous satellites)
- **Apsidal Rotation:** Argument of periapsis rotates

### Hohmann Transfers
The most fuel-efficient way to move between two circular orbits:
1. Burn at periapsis to raise apoapsis to target orbit
2. Coast along transfer ellipse
3. Burn at apoapsis to circularize

$$\Delta v_{total} = \Delta v_1 + \Delta v_2$$

### Lambert's Problem
Given two position vectors and a time of flight, find the orbit connecting them. This is the foundation of trajectory optimization and Porkchop Plot generation.

## Weekly Schedule

### Week 1-2: Two-Body Problem
- Kepler's Laws derivation
- Orbital elements and conversions
- Vis-viva equation

### Week 3-4: Orbital Maneuvers
- Hohmann transfers
- Bi-elliptic transfers
- Plane changes

### Week 5-6: Perturbations
- J2 effects on LEO satellites
- Atmospheric drag
- Third-body perturbations

### Week 7-8: Mission Design
- Lambert's Problem
- Porkchop Plots
- Launch window analysis

## Tools & Libraries
- `numpy` - Numerical computation
- `matplotlib` - Visualization and animation
- `scipy` - ODE solvers and optimization
- `skyfield` - Ephemeris data (optional)

## References
- Vallado, D. "Fundamentals of Astrodynamics and Applications"
- Curtis, H. "Orbital Mechanics for Engineering Students"
- NASA JPL Horizons (ephemeris data)

