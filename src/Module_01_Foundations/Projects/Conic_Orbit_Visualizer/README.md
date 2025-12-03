# Conic Orbit Visualizer

**Module:** 1 (Foundations)  
**Concepts:** Kepler's Laws, Vis-Viva Equation, Conic Sections

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Conic Sections** | Why orbits are ellipses, parabolas, or hyperbolas |
| **Eccentricity** | How orbit shape is determined |
| **Vis-Viva Equation** | Calculating velocity at any orbital position |
| **Orbital Energy** | Bound vs. unbound trajectories |
| **True Anomaly** | Spacecraft position along the orbit |

## Project Overview

This tool visualizes the fundamental shapes of orbital mechanics:

| Orbit Type | Eccentricity | Examples |
|------------|--------------|----------|
| **Circular** | e = 0 | ISS, Starlink, GPS |
| **Elliptical** | 0 < e < 1 | GTO, Molniya, Hubble |
| **Parabolic** | e = 1 | Minimum escape energy |
| **Hyperbolic** | e > 1 | Voyager, New Horizons |

## Real-World Applications

| Agency | Mission | Orbit Type |
|--------|---------|------------|
| **NASA** | ISS | Circular LEO (e ≈ 0.0001) |
| **NASA** | Voyager 1 & 2 | Hyperbolic escape |
| **ESA** | Gaia | Elliptical at L2 |
| **ISRO** | Chandrayaan | Lunar transfer |
| **CNSA** | Tiangong | Circular LEO |
| **SpaceX** | Starlink | Circular 550 km |

## Installation & Usage

```bash
pip install -r requirements.txt
python visualizer.py
```

## Interactive Dashboard

Navigate between different orbit demonstrations:
1. **LEO** - Circular orbit (e.g., ISS, Starlink)
2. **GTO** - Geostationary transfer (elliptical)
3. **ESCAPE** - Hyperbolic trajectory
4. **LUNAR** - Earth-Moon transfer

## The Math

### Polar Equation of a Conic
$$r(\theta) = \frac{a(1-e^2)}{1 + e\cos\theta}$$

### Vis-Viva Equation
$$v^2 = \mu\left(\frac{2}{r} - \frac{1}{a}\right)$$

Where:
- μ = GM (gravitational parameter)
- a = semi-major axis
- r = current radius
- e = eccentricity

### Orbital Period (Elliptical)
$$T = 2\pi\sqrt{\frac{a^3}{\mu}}$$

See `EXPLANATION.md` for complete derivations.
