# 3D Rocket Ascent Simulator

**Module:** 1 (Foundations)
**Project:** 1
**Language:** Python 3.x

## Project Overview
This project is a physics-based simulation of a multi-stage rocket ascent (modeled on a Falcon 9-class vehicle). It integrates the equations of motion in 3D space, accounting for:
*   **Variable Gravity:** $g$ decreases with altitude ($1/r^2$).
*   **Atmospheric Drag:** Air density decreases exponentially with altitude.
*   **Mass Depletion:** Rocket gets lighter as fuel is burned, increasing acceleration ($F=ma$).
*   **Thrust Vectoring:** Simple "Gravity Turn" logic to simulate orbit insertion.

## SpaceX Tie-In
At SpaceX, accurate trajectory simulation is critical for:
*   **Mission Planning:** Calculating exact fuel requirements for Starlink launches.
*   **GNC (Guidance, Navigation, Control):** Real-time onboard computers solve similar equations to steer the rocket.
*   **Max Q Analysis:** Predicting the point of maximum dynamic pressure to throttle engines and prevent structural failure.

## Installation & Usage

1.  **Prerequisites:**
    Ensure you have Python installed (Anaconda recommended).
    Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Simulation:**
    ```bash
    python simulation.py
    ```

3.  **Output:**
    The script will print flight events (Launch, Impact/Orbit, Max Alt) to the console and open a dashboard of plots:
    *   Altitude vs. Time
    *   Velocity vs. Time
    *   Dynamic Pressure (Q) vs. Time
    *   3D Trajectory visualization

## How It Works
The simulation uses **Runge-Kutta 4 (RK4)** numerical integration. This provides much higher accuracy than standard Euler integration by sampling the slope at 4 points within each time step. 

The State Vector tracks 7 variables:
`[Position_X, Position_Y, Position_Z, Velocity_X, Velocity_Y, Velocity_Z, Mass]`

See `EXPLANATION.md` for the deep dive into the math and physics.
