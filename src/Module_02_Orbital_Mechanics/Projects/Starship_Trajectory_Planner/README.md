# Mars Mission Simulator

**Module:** 2 (Orbital Mechanics)  
**Concepts:** Hohmann Transfers, Lambert's Problem, Atmospheric Entry Dynamics

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Hohmann Transfer** | Most fuel-efficient path between planetary orbits |
| **Phase Angle** | When to launch for planetary rendezvous |
| **Delta-V Budget** | Total velocity change required for mission |
| **Porkchop Plots** | Visualizing launch window trade-offs |
| **Entry Dynamics** | Atmospheric deceleration, heat flux, G-loads |
| **Kepler's Equation** | Solving spacecraft position over time |

## Project Overview

This interactive dashboard simulates a complete Earth-to-Mars mission:

1. **Mission Overview** - Visualize the Hohmann transfer orbit
2. **Transit Analysis** - Velocity and distance profiles during cruise
3. **Entry, Descent, Landing** - Atmospheric entry simulation with physics
4. **Historical Missions** - Compare NASA, ESA, CNSA, ISRO, UAE missions
5. **Launch Windows** - Interactive porkchop plot analysis

## Historical Mars Missions Included

| Mission | Agency | Year | Type | Status |
|---------|--------|------|------|--------|
| **Perseverance** | NASA | 2020 | Rover | Active |
| **Curiosity** | NASA | 2011 | Rover | Active |
| **InSight** | NASA | 2018 | Lander | Completed |
| **Tianwen-1** | CNSA | 2020 | Orbiter+Rover | Active |
| **Mars Express** | ESA | 2003 | Orbiter | Active |
| **ExoMars TGO** | ESA/Roscosmos | 2016 | Orbiter | Active |
| **Mangalyaan** | ISRO | 2013 | Orbiter | Completed |
| **Hope** | UAE | 2020 | Orbiter | Active |

## Installation & Usage

```bash
pip install -r requirements.txt

# Launch the interactive dashboard
python mission_planner.py

# Porkchop plot tool (standalone)
python porkchop/plotter.py
```

## The Physics

### Hohmann Transfer

The most energy-efficient two-impulse transfer between circular orbits:

**Transfer Semi-Major Axis:**
$$a_{transfer} = \frac{r_{Earth} + r_{Mars}}{2} = \frac{1.0 + 1.524}{2} \text{ AU} = 1.262 \text{ AU}$$

**Transfer Time (half orbital period):**
$$T_{transfer} = \pi \sqrt{\frac{a^3}{\mu_{Sun}}} \approx 259 \text{ days}$$

**Departure Delta-V (Trans-Mars Injection):**
$$\Delta v_1 = \sqrt{\frac{\mu}{r_E}}\left(\sqrt{\frac{2r_M}{r_E + r_M}} - 1\right) \approx 2.94 \text{ km/s}$$

**Arrival Delta-V (Mars Orbit Insertion):**
$$\Delta v_2 = \sqrt{\frac{\mu}{r_M}}\left(1 - \sqrt{\frac{2r_E}{r_E + r_M}}\right) \approx 2.65 \text{ km/s}$$

### Phase Angle

Mars must lead Earth by the correct angle at departure:

$$\phi = 180° - \omega_{Mars} \cdot T_{transfer} \approx 44°$$

Where $\omega_{Mars}$ is Mars' angular velocity around the Sun.

### Atmospheric Entry

The simulator models Mars entry using:

**Exponential Atmosphere:**
$$\rho(h) = \rho_0 \cdot e^{-h/H}$$

Where:
- $\rho_0 = 0.020$ kg/m³ (Mars surface density)
- $H = 11,100$ m (scale height)

**Aerodynamic Deceleration:**
$$a_{drag} = \frac{1}{2} \cdot \rho \cdot v^2 \cdot C_D \cdot A / m$$

**Convective Heat Flux (Sutton-Graves):**
$$\dot{q} = k \sqrt{\frac{\rho}{r_n}} \cdot v^3$$

### Typical Values (Earth to Mars)

| Parameter | Value |
|-----------|-------|
| Transfer time | ~259 days |
| Phase angle | ~44° |
| Total Δv | ~5.6 km/s |
| Entry velocity | 5.5-6.0 km/s |
| Peak deceleration | 10-15 G |
| Peak heating | ~100 W/cm² |

## Understanding Porkchop Plots

The porkchop plot shows delta-V required for different launch/arrival combinations:

- **X-axis:** Launch date (days from epoch)
- **Y-axis:** Arrival date (days from epoch)  
- **Color:** Total delta-V (darker = more efficient)

The characteristic "porkchop" shape emerges because:
- Too-fast transits require extra energy (upper-left region)
- Too-slow transits miss optimal geometry (lower-right region)
- The minimum (sweet spot) approximates a Hohmann transfer

## References

- Vallado, D. "Fundamentals of Astrodynamics and Applications"
- NASA Mars Exploration Program: https://mars.nasa.gov
- ESA Mars Missions: https://www.esa.int/Science_Exploration/Space_Science/Mars_Express
- ISRO Mars Orbiter Mission: https://www.isro.gov.in/MarsOrbiterMissionSpacecraft
