# Conic Orbit Visualizer

**Module:** 1 (Foundations)
**Project:** 2
**Language:** Python 3.x

## Project Overview
This tool visualizes the fundamental shapes of orbital mechanics: **Conic Sections**. By manipulating Keplerian elements (specifically eccentricity and semi-major axis), we can generate and classify:
*   **Circular Orbits ($e=0$):** Like the ISS or Starlink.
*   **Elliptical Orbits ($0 < e < 1$):** Like GTO (Geostationary Transfer Orbit).
*   **Parabolic/Hyperbolic Orbits ($e \ge 1$):** Escape trajectories for interplanetary missions to Mars.

The tool calculates the radius $r$ and velocity $v$ at every point along the path using polar coordinates and the Vis-Viva equation.

## SpaceX Tie-In
Visualizing orbits is the first step in mission design.
*   **Starlink:** Relies on precise circular orbits at specific altitudes.
*   **Starship Mars Missions:** Requires a high-energy **Hyperbolic Injection** burn to escape Earth's gravity well.
*   **Falcon 9 GTO:** The second stage executes a burn to put a satellite into a highly elliptical "Transfer Orbit" ($e \approx 0.73$) before it circularizes at GEO.

## Installation & Usage

1.  **Prerequisites:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Visualizer:**
    ```bash
    python visualizer.py
    ```

3.  **Output:**
    The script runs a demo sequence, displaying interactive polar plots for:
    1.  **LEO (Low Earth Orbit)** - Circular.
    2.  **GTO (Geostationary Transfer Orbit)** - Highly Elliptical.
    3.  **Escape Trajectory** - Hyperbolic.

## Technical Features
*   **Polar Plotting:** Uses `matplotlib`'s polar projection for accurate orbital representation.
*   **Anomaly Calculation:** Handles the "True Anomaly" $\theta$ range to correctly render open orbits (hyperbolas) without asymptotic errors.
*   **Velocity Estimation:** Computes orbital speed at any point using the energy-conservation principle (Vis-Viva).

See `EXPLANATION.md` for the math behind the curves.
