# Crew Safety Simulator

**Module:** 4 (Human Factors & Safety)  
**Concepts:** Damped Oscillations, G-Force Limits, Vibration Analysis

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Mass-Spring-Damper** | How crew seats absorb shock |
| **Damping Ratio** | Critically damped vs. underdamped response |
| **G-Force Limits** | NASA standards for human tolerance |
| **Frequency Response** | How vibrations affect crew |
| **ODE Solving** | Using scipy.integrate.odeint |

## Project Overview

A physics-based simulation modeling G-forces and vibrations experienced by astronauts during launch and landing. Uses damped oscillation mechanics to analyze how seat/harness systems protect crew.

## Historical G-Force Limits by Vehicle

| Vehicle | Agency | Launch | Reentry | Era |
|---------|--------|--------|---------|-----|
| **Mercury** | NASA | 8.0g | 11.0g | 1961-1963 |
| **Gemini** | NASA | 7.0g | 8.0g | 1965-1966 |
| **Apollo** | NASA | 4.0g | 6.5g | 1968-1972 |
| **Space Shuttle** | NASA | 3.0g | 1.5g | 1981-2011 |
| **Soyuz** | Roscosmos | 4.2g | 4.5g* | 1967-present |
| **Shenzhou** | CNSA | 4.0g | 4.5g | 2003-present |
| **Crew Dragon** | SpaceX | 4.0g | 4.5g | 2020-present |
| **New Shepard** | Blue Origin | 3.0g | 5.0g | 2021-present |

*Soyuz ballistic reentry: up to 8-9g (TMA-11 incident, 2008)

## Installation & Usage

```bash
pip install -r requirements.txt
python simulator.py
```

## Interactive Dashboard

Navigate between different analyses:
- **OVERVIEW:** Multi-vehicle launch/reentry comparison
- **CREW DRAGON:** SpaceX vehicle detailed analysis
- **SOYUZ:** Roscosmos vehicle with ballistic mode
- **APOLLO:** NASA lunar return high-speed reentry
- **STARSHIP:** SpaceX next-gen vehicle profile
- **NEW SHEPARD:** Blue Origin suborbital
- **SHENZHOU:** CNSA crewed spacecraft

## The Physics

### Mass-Spring-Damper Model

The crew seat is modeled as a single-degree-of-freedom system:

```
    Spacecraft Structure
           │
           │ F(t) = m × a_spacecraft
           ▼
    ┌──────────────┐
    │   Spring (k) │
    │   Damper (c) │
    └──────┬───────┘
           │
    ┌──────▼───────┐
    │  Astronaut   │
    │   Mass (m)   │
    └──────────────┘
```

### Equation of Motion

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

Where:
- x = relative displacement from equilibrium
- m = mass of astronaut + seat (~80 kg)
- c = damping coefficient (shock absorbers)
- k = spring constant (seat cushion stiffness)
- F(t) = external force from spacecraft acceleration

### Damping Ratio

$$\zeta = \frac{c}{2\sqrt{km}}$$

| ζ Value | Response Type | Behavior |
|---------|---------------|----------|
| ζ < 1 | Underdamped | Oscillates before settling |
| ζ = 1 | Critically damped | Fastest settling, no overshoot |
| ζ > 1 | Overdamped | Slow return to equilibrium |

### Natural Frequency

$$f_n = \frac{1}{2\pi}\sqrt{\frac{k}{m}}$$

Lower frequency = softer ride but more displacement.

## Key Parameters

| Parameter | Symbol | Typical Range | Effect |
|-----------|--------|---------------|--------|
| Damping Ratio | ζ | 0.3 - 1.5 | Controls oscillation |
| Natural Frequency | fₙ | 2-10 Hz | Seat stiffness |
| Peak Reduction | - | 10-40% | G-force attenuation |

## NASA Safety Standards (NASA-STD-3001)

| Condition | Limit | Duration |
|-----------|-------|----------|
| Sustained acceleration | < 4g | > 10 seconds |
| Peak acceleration | < 8g | < 1 second |
| Vibration (< 20 Hz) | < 0.5g RMS | Continuous |

## References

- NASA-STD-3001: Human Systems Integration Requirements
- NASA SP-2010-3407: Human Integration Design Handbook
- "Spacecraft Structures" by J.R. Wertz
- ESA ECSS-E-HB-32-25A: Mechanical Design Handbook

See `EXPLANATION.md` for complete derivations.
