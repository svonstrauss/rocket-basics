# 3D Rocket Ascent Simulator

**Module:** 1 (Foundations)  
**Concepts:** Newton's Laws, Numerical Integration, Atmospheric Physics

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Newton's 2nd Law** | How F=ma governs rocket acceleration |
| **Drag Equation** | Why rockets experience Max Q |
| **Gravity Variation** | g decreases with altitude (1/r²) |
| **Mass Depletion** | Why rockets accelerate faster as fuel burns |
| **RK4 Integration** | Industry-standard numerical method for trajectories |

## Project Overview

This physics-based simulation models a multi-stage rocket ascent, accounting for:

- **Variable Gravity:** g decreases with altitude (inverse-square law)
- **Atmospheric Drag:** Air density decreases exponentially
- **Mass Depletion:** Rocket accelerates as fuel burns (F=ma)
- **Thrust Vectoring:** Gravity turn maneuver for orbit insertion

## Real-World Applications

| Agency | Vehicle | Similar Physics |
|--------|---------|-----------------|
| **SpaceX** | Falcon 9 | Max Q throttling, booster recovery |
| **NASA** | SLS | Gravity turn to orbit, staging events |
| **ESA** | Ariane 6 | Atmospheric drag modeling |
| **JAXA** | H3 | Trajectory optimization |

## Installation & Usage

```bash
pip install -r requirements.txt
python simulation.py
```

## Interactive Dashboard

The simulator provides an interactive dashboard with:
- **Overview:** Key flight metrics at a glance
- **Altitude:** Height vs time with apogee marker
- **Velocity:** Speed profile including Max Q
- **Max Q:** Dynamic pressure analysis
- **3D Path:** Spatial trajectory visualization

## The Physics

### Equations of Motion

The rocket experiences three main forces:

1. **Thrust:** \( F_{thrust} = \dot{m} \cdot v_{exhaust} \)
2. **Gravity:** \( F_g = \frac{G M m}{r^2} \)
3. **Drag:** \( F_d = \frac{1}{2} \rho v^2 C_d A \)

### RK4 Integration

Runge-Kutta 4 provides 4th-order accuracy by sampling slopes at:
- Beginning of timestep (k1)
- Midpoint using k1 (k2)
- Midpoint using k2 (k3)
- End using k3 (k4)

Final estimate: weighted average with 1/6, 2/6, 2/6, 1/6 weights.

## State Vector

The simulation tracks 7 variables:
```
[Position_X, Position_Y, Position_Z, Velocity_X, Velocity_Y, Velocity_Z, Mass]
```

See `EXPLANATION.md` for detailed physics derivations.
