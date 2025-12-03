# Satellite Constellation Propagator

**Module:** 2 (Orbital Mechanics)  
**Concepts:** J2 Perturbations, Nodal Regression, Orbital Elements

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **J2 Perturbation** | Why satellite orbits drift over time |
| **Nodal Regression** | RAAN drift from Earth's equatorial bulge |
| **Orbital Elements** | The 6 parameters that define any orbit |
| **Ground Tracks** | How satellites trace paths over Earth |
| **Walker Constellations** | How to design global coverage systems |

## Project Overview

This propagator simulates satellite constellation dynamics, accounting for **J2 perturbations** from Earth's oblate shape. Unlike ideal Keplerian orbits, real satellites experience:

- **Nodal Regression:** RAAN drifts westward (for most orbits)
- **Apsidal Rotation:** Argument of periapsis rotates
- **Secular Drift:** Accumulates over days/weeks

## Global Constellation Systems

| System | Agency/Company | Satellites | Altitude | Inclination |
|--------|----------------|------------|----------|-------------|
| **GPS** | US Space Force | 31 | 20,200 km | 55° |
| **GLONASS** | Roscosmos | 24 | 19,100 km | 64.8° |
| **Galileo** | ESA | 30 | 23,222 km | 56° |
| **BeiDou** | CNSA | 35 | 21,528 km | 55° |
| **Starlink** | SpaceX | 6,000+ | 550 km | 53° |
| **OneWeb** | OneWeb | 648 | 1,200 km | 87.9° |
| **Iridium** | Iridium | 66 | 780 km | 86.4° |

## Installation & Usage

```bash
pip install -r requirements.txt
python propagator.py
```

## Interactive Dashboard

- **3D VIEW:** Animated constellation with Earth
- **GROUND TRACK:** Satellite paths over world map
- **COVERAGE:** Ground coverage analysis
- **GLOBAL SATS:** Statistics and system comparison

## The Physics

### J2 Perturbation

Earth bulges at the equator by ~21 km. This extra mass creates a torque on inclined orbits:

$$\dot{\Omega} = -\frac{3}{2} n J_2 \left(\frac{R_E}{p}\right)^2 \cos i$$

Where:
- n = mean motion (rad/s)
- J₂ = 1.0826 × 10⁻³ (Earth's oblateness)
- Rₑ = Earth radius (6,378 km)
- p = semi-latus rectum
- i = inclination

### Sun-Synchronous Orbits

By choosing the right inclination (~98°), RAAN can drift exactly 360°/year, keeping the orbital plane fixed relative to the Sun. Used by:
- Landsat (NASA)
- Sentinel (ESA)
- WorldView (Maxar)

### Classical Orbital Elements (COEs)

| Element | Symbol | Meaning |
|---------|--------|---------|
| Semi-major axis | a | Orbit size |
| Eccentricity | e | Orbit shape |
| Inclination | i | Orbit tilt |
| RAAN | Ω | Node location |
| Arg. of Periapsis | ω | Periapsis location |
| True Anomaly | ν | Current position |

See `EXPLANATION.md` for complete derivations.
