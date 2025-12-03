# Technical Explanation: Interplanetary Mission Design

## 1. The Hohmann Transfer
A Hohmann Transfer is an elliptical orbit tangent to both the departure orbit (Earth) and the arrival orbit (Mars).
*   **Perihelion:** Occurs at Earth's distance ($1 \text{ AU}$).
*   **Aphelion:** Occurs at Mars's distance ($1.52 \text{ AU}$).

### Why is it efficient?
It uses the sun's gravity to do most of the work. We only burn engines twice:
1.  **Trans-Mars Injection (TMI):** Adds energy to raise the Aphelion to Mars's orbit.
2.  **Mars Orbit Insertion (MOI):** Matches speed with Mars to be captured (otherwise we'd just fly past and fall back to the sun).

## 2. The Launch Window (Phase Angle)
You can't just launch anytime. Since the spacecraft takes ~259 days to travel, Mars moves during that time.
*   Mars moves slower than Earth (Kepler's 3rd Law).
*   We must "lead" the target.
*   **Calculation:** We calculate how far Mars moves in 259 days ($\theta_{mars}$). The transfer orbit covers exactly $180^\circ$ ($\pi$ radians). The difference determines where Mars must be at $T=0$.
*   For Earth-Mars, this angle is roughly **44 degrees ahead** of Earth. This alignment happens every ~26 months.

## 3. Kepler's Equation in Code
To animate the spacecraft correctly along the ellipse, we can't just increment the angle linearly (that would violate conservation of angular momentum/Kepler's 2nd Law).
In `mission_planner.py`, we solve **Kepler's Equation** iteratively:

$$ M = E - e \sin E $$

Where:
*   $M$: Mean Anomaly (Linear time-based angle).
*   $E$: Eccentric Angle (Geometric angle).
*   $e$: Eccentricity.

We calculate $M$ from time $t$, solve for $E$ using a Newton-Raphson loop (or simple iteration), and then convert $E$ to the True Anomaly $\nu$ to get the actual $(x,y)$ coordinates. This makes the spacecraft speed up near the Sun (Earth) and slow down near Mars, just like real physics.

