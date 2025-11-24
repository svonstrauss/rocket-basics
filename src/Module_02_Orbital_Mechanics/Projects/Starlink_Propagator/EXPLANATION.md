# Technical Explanation: J2 Perturbations & Constellation Design

## 1. The Problem with "Perfect" Spheres
In introductory physics (and our Module 1 project), we assumed Earth was a point mass or a perfect sphere. In this model, an orbit stays fixed in inertial space forever. The "Orbital Plane" never moves.

In reality, Earth spins, and centrifugal force causes it to bulge at the equator. The diameter at the equator is ~43km larger than at the poles.

## 2. The J2 Effect
This bulge acts like a "belt" of extra mass. For a satellite in an inclined orbit (like Starlink at $53^\circ$), this belt exerts a gravitational torque.

A torque applied to a spinning gyroscope (the orbit) causes **Precession**.

### Nodal Regression ($\dot{\Omega}$)
The orbit's crossing point at the equator (the Ascending Node) drifts over time.
*   **Prograde Orbits ($i < 90^\circ$):** Node drifts West (negative).
*   **Retrograde Orbits ($i > 90^\circ$):** Node drifts East (positive).
*   **Polar Orbits ($i = 90^\circ$):** No drift ($\cos 90 = 0$).

### Apsidal Rotation ($\dot{\omega}$)
The ellipse itself rotates within the plane. The point of perigee moves.
*   At $i \approx 63.4^\circ$ (The "Critical Inclination"), this rotation stops. This is used for Molniya orbits.

## 3. Application: Starlink Deployment
SpaceX launches ~60 satellites at a time. They are released into a "Parking Orbit" (lower altitude).
1.  **Injection:** Satellites released at 300km.
2.  **Drift:** Because gravity is stronger lower down, they move faster (higher $n$). The J2 effect is stronger ($\propto 1/a^{3.5}$).
3.  **Plane Change:** SpaceX waits for the J2 effect to naturally drift the group's RAAN to the desired target plane.
4.  **Raise:** They thrust up to the operational altitude (550km), "locking in" the plane.

This allows one launch to fill multiple planes over time!

## 4. Code Implementation
In `propagator.py`, we use a simplified "Secular Perturbation" model.
We do not numerically integrate force vectors (like in Module 1's ascent sim) because J2 is a small, constant effect over millions of orbits. Instead, we analytically update the orbital elements:

```python
# Linear approximation suitable for short durations
current_raan = initial_raan + raan_dot * time
```
This is much faster computationally, allowing us to simulate hundreds of satellites easily.

