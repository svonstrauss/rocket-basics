# Week 1: Parametric Equations & Conic Sections

**Goal:** Gain comfort with parametric and polar representations of curves to model orbits.

## Daily Tasks

### Day 1: Intro to Parametric Equations
*   **Reading:** Briggs Calculus Ch. 11.1 (Parametric Equations).
*   **Concept:** Representing curves as $x(t), y(t)$ (like a rocket's path over time).
*   **Coding:** Create `conic_visualizer.py`. Implement a basic parametric plotter for a circle ($x = r\cos t$, $y = r\sin t$).

### Day 2: Polar Coordinates & Orbits
*   **Reading:** Briggs Ch. 11.2 (Polar Coordinates).
*   **Concept:** Describing curves as $r(\theta)$ (crucial for orbits).
*   **Coding:** Extend `conic_visualizer.py` to handle polar input.
    *   Input: Eccentricity ($e$) and Semi-major axis ($a$).
    *   Equation: $r(\theta) = \frac{a(1-e^2)}{1+e\cos\theta}$.
    *   Test: Ellipse ($0 < e < 1$), Parabola ($e=1$), Hyperbola ($e>1$).

### Day 3: Calculus in Polar Coordinates
*   **Reading:** Briggs Ch. 11.3 (Calculus in Polar).
*   **Concept:** Rates of change ($\frac{dr}{d\theta}$), velocity components.
*   **Coding:** Add velocity calculation to `conic_visualizer.py`.
    *   Compute orbital speed estimates at various points.

### Day 4: Conic Sections as Orbits
*   **Reading:** Briggs Ch. 11.4 (Conic Sections).
*   **Concept:** Relating math shapes to physical orbits (Circle=LEO, Hyperbola=Escape).
*   **Coding:** Refine visualizer to classify orbit types based on user input.

### Day 5-7: Review & Extensions
*   **Review:** Solve practice problems from Briggs.
*   **SpaceX Tie-in:** How does Starship's trajectory change from ascent (parametric) to orbit (polar/conic)?

