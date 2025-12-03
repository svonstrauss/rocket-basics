# Technical Explanation: Conic Sections & Orbital Mechanics

## 1. The Polar Equation of an Orbit
While Cartesian coordinates ($x, y$) are useful for position, orbits are most naturally described in **Polar Coordinates** ($r, \theta$). The shape of an orbit around a massive body (like Earth) is a conic section defined by:

$$ r(\theta) = \frac{a(1-e^2)}{1 + e \cos \theta} $$

Where:
*   **$r$**: Radial distance from the focus (Earth's center).
*   **$\theta$**: True Anomaly (the angle from periapsis, the closest point).
*   **$a$**: Semi-major axis (defines the "size" or energy of the orbit).
*   **$e$**: Eccentricity (defines the "shape").

### Eccentricity Classes
*   **$e = 0$**: Circle. The denominator becomes constant ($1$), so radius $r$ is constant.
*   **$0 < e < 1$**: Ellipse. The radius oscillates between a minimum (periapsis) and maximum (apoapsis).
*   **$e = 1$**: Parabola. The orbit is "open" and never returns.
*   **$e > 1$**: Hyperbola. An escape trajectory with excess velocity.

## 2. Orbital Velocity (Vis-Viva Equation)
To calculate how fast the spacecraft is moving at any point $r$, we use the **Vis-Viva Equation**, which is derived from the conservation of specific orbital energy:

$$ v^2 = \mu \left( \frac{2}{r} - \frac{1}{a} \right) $$

Where:
*   **$\mu$**: Standard Gravitational Parameter ($G \cdot M_{earth}$).
*   **$r$**: Current distance from center.
*   **$a$**: Semi-major axis.

### Key Insights from Vis-Viva:
1.  **Highest Velocity:** Occurs when $r$ is smallest (Periapsis). This is why rocket burns are most efficient here (Oberth Effect).
2.  **Lowest Velocity:** Occurs when $r$ is largest (Apoapsis).
3.  **Escape Velocity:** For a parabolic orbit ($e=1$), $a \to \infty$, so the term $1/a \to 0$. The equation simplifies to $v_{esc} = \sqrt{2\mu/r}$.

## 3. Code Implementation Logic
The `calculate_radius` function in `visualizer.py` directly implements the polar equation.
*   **Challenge:** For Hyperbolic orbits ($e > 1$), the denominator ($1 + e \cos \theta$) can become zero. This corresponds to the asymptotes of the hyperbola.
*   **Solution:** In the code, we limit the plotting range of $\theta$ to be within the valid physical region of the orbit, avoiding the mathematical singularities.

