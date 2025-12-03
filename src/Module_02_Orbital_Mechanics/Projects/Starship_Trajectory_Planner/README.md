# Interplanetary Trajectory Planner

**Module:** 2 (Orbital Mechanics)  
**Concepts:** Hohmann Transfers, Phase Angles, Lambert's Problem

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Hohmann Transfer** | Most fuel-efficient path between orbits |
| **Phase Angle** | When to launch for planetary rendezvous |
| **Delta-V Budget** | Total velocity change required |
| **Porkchop Plots** | Visualizing launch window trade-offs |
| **Synodic Period** | How often launch windows occur |

## Project Overview

This tool calculates and visualizes interplanetary transfer orbits:

1. **Launch Windows:** Optimal Earth-Mars alignment
2. **Delta-V Budget:** Velocity changes for departure and arrival
3. **Time of Flight:** Transfer duration (~7-9 months for Mars)

## Historical Mars Missions

| Mission | Agency | Year | Transfer Type |
|---------|--------|------|---------------|
| **Mariner 4** | NASA | 1964 | Flyby |
| **Viking 1** | NASA | 1975 | Orbit + Land |
| **Mars Pathfinder** | NASA | 1996 | Direct entry |
| **Mars Express** | ESA | 2003 | Orbit |
| **Curiosity** | NASA | 2011 | Direct entry |
| **Tianwen-1** | CNSA | 2020 | Orbit + Land |
| **Perseverance** | NASA | 2020 | Direct entry |
| **Hope** | UAE | 2020 | Orbit |

## Installation & Usage

```bash
pip install -r requirements.txt

# Animated transfer visualization
python mission_planner.py

# Interactive launch window analysis
python porkchop/plotter.py
```

## The Physics

### Hohmann Transfer Geometry

The most energy-efficient two-body transfer:

1. **Burn 1:** At Earth, tangential burn to raise aphelion to Mars orbit
2. **Coast:** Follow elliptical transfer path for ~259 days
3. **Burn 2:** At Mars, tangential burn to match circular orbit

### Key Equations

**Transfer Semi-Major Axis:**
$$a_{transfer} = \frac{r_{Earth} + r_{Mars}}{2}$$

**Departure Delta-V:**
$$\Delta v_1 = \sqrt{\frac{\mu_{Sun}}{r_E}}\left(\sqrt{\frac{2r_M}{r_E + r_M}} - 1\right)$$

**Phase Angle:**
$$\phi = 180° - \omega_{Mars} \cdot t_{transfer}$$

Mars must lead Earth by this angle at departure.

### Typical Values (Earth to Mars)

| Parameter | Value |
|-----------|-------|
| Transfer time | 259 days |
| Phase angle | ~44° |
| Departure ΔV | 2.94 km/s |
| Arrival ΔV | 2.65 km/s |
| Total ΔV | 5.59 km/s |
| Window interval | 26 months |

## Porkchop Plots

Click on the contour plot to explore different launch dates. The plot shows:
- **X-axis:** Departure date
- **Y-axis:** Arrival date
- **Color:** Total Delta-V required

Lower values (darker) = more efficient trajectories.

See `EXPLANATION.md` for complete derivations.
