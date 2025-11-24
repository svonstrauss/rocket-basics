# Project 1: Starlink Orbit Propagator

**Module:** 2 (Orbital Mechanics)
**Project:** 1
**Language:** Python 3.x

## Project Overview
This tool simulates the motion of a satellite constellation (modeled after Starlink) in Low Earth Orbit (LEO). Unlike the simple Keplerian visualizer in Module 1, this propagator incorporates **J2 Perturbations**.

**What is J2?**
Earth is not a perfect sphere; it bulges at the equator. This non-spherical mass distribution creates a torque on satellite orbits, causing them to shift over time. This effect is called **Nodal Regression**.

## SpaceX Tie-In
*   **Constellation Management:** SpaceX relies on J2 precession to deploy Starlink satellites. They launch a batch into a single plane, and because satellites at different altitudes precess at different rates, they can use this drift to drift satellites into different orbital planes without using massive amounts of fuel.
*   **Sun-Synchronous Orbits:** The J2 effect is specifically exploited to keep certain satellites (like Transporter rideshare missions) always synchronized with the sun.

## Features
- [x] **J2 Propagator:** Calculates secular rates of change for RAAN ($\Omega$) and Argument of Perigee ($\omega$).
- [x] **COE to ECI Conversion:** Converts Classical Orbital Elements to Earth-Centered Inertial Cartesian coordinates ($x, y, z$).
- [x] **3D Constellation Viz:** Animates multiple orbital planes simultaneously using `matplotlib` 3D.
- [x] **High-Fidelity Graphics:** Features realistic Earth texture mapping, atmospheric glow, tech-grid overlays, and a heads-up display (HUD) for simulation time and telemetry.

## Usage
1.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the propagator:
    ```bash
    python propagator.py
    ```

## The Math (J2 Perturbation)
The rate of change of the Right Ascension of the Ascending Node (RAAN) is given by:

$$ \dot{\Omega} = -1.5 n J_2 \left(\frac{R_E}{p}\right)^2 \cos i $$

Where:
*   $n$: Mean motion
*   $J_2$: Second zonal harmonic ($1.0826 \times 10^{-3}$)
*   $p$: Semi-latus rectum
*   $i$: Inclination

Notice that for Starlink ($i=53^\circ$), the cosine term is positive, so $\dot{\Omega}$ is negative. The node drifts westward!

