# Constellation Designer

**Module:** 3 (Space Systems & Propulsion)  
**Concepts:** Walker Patterns, Coverage Analysis, FOV Geometry

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Walker Delta** | Standard notation for constellation design |
| **Orbital Shells** | Why constellations use multiple altitudes |
| **Coverage Geometry** | Calculating ground footprints |
| **Phasing** | Optimizing satellite spacing |
| **Link Budget Basics** | Why altitude matters for signal strength |

## Project Overview

Design and visualize satellite constellations like GPS, Starlink, or Galileo. This tool simulates multiple "Orbital Shells" at different altitudes and inclinations to analyze global coverage.

**Key Feature:** Animated 3D visualization with sensor cone coverage.

## Global Navigation & Communication Constellations

| System | Operator | Satellites | Altitude | Inclination | Purpose |
|--------|----------|------------|----------|-------------|---------|
| **GPS** | US Space Force | 31 | 20,200 km | 55° | Navigation |
| **GLONASS** | Roscosmos | 24 | 19,100 km | 64.8° | Navigation |
| **Galileo** | ESA | 30 | 23,222 km | 56° | Navigation |
| **BeiDou** | CNSA | 35 | 21,528 km | 55° | Navigation |
| **QZSS** | JAXA | 4 | 32,000-40,000 km | 41° | Regional Nav |
| **Starlink** | SpaceX | 6,000+ | 540-570 km | 53-98° | Internet |
| **OneWeb** | OneWeb | 648 | 1,200 km | 87.9° | Internet |
| **Iridium NEXT** | Iridium | 66 | 780 km | 86.4° | Voice/Data |
| **O3b mPOWER** | SES | 11+ | 8,062 km | 0° | Internet |

## Installation & Usage

```bash
pip install -r requirements.txt
python designer.py
```

## Design Parameters

Configure your constellation with:
- **Altitude:** Orbital height (affects coverage area and latency)
- **Inclination:** Orbital tilt (determines latitude coverage)
- **Planes:** Number of orbital planes
- **Sats/Plane:** Satellites per plane
- **FOV:** Sensor field of view (degrees)

## The Physics

### Walker Delta Notation

Constellations are described as **i: t/p/f**:
- **i** = Inclination (degrees)
- **t** = Total satellites
- **p** = Number of planes
- **f** = Phasing factor (0 to p-1)

Example: GPS is approximately **55°: 24/6/1**

### Coverage Geometry

The ground footprint depends on altitude (h) and minimum elevation angle (ε):

$$\theta_{half-angle} = \arccos\left(\frac{R_E \cos(\epsilon)}{R_E + h}\right) - \epsilon$$

Higher altitude = larger footprint, but worse latency.

### Altitude Trade-offs

| Altitude | Footprint | Latency | Sats for Global |
|----------|-----------|---------|-----------------|
| 550 km (LEO) | ~2,500 km | 4 ms | ~1,600 |
| 1,200 km (LEO) | ~4,500 km | 8 ms | ~400 |
| 8,000 km (MEO) | ~12,000 km | 53 ms | ~20 |
| 20,200 km (MEO) | ~18,000 km | 135 ms | ~24 |
| 35,786 km (GEO) | ~17,000 km | 240 ms | 3 |

### Coverage Percentage

For a Walker constellation, continuous coverage requires:
$$n_{min} = \frac{4\pi R_E^2}{\pi r_{footprint}^2} \times \text{overlap factor}$$

See `EXPLANATION.md` for complete derivations.
