# Module 4: Human Factors, Regulations, and Space Policy

**Duration:** 6 Weeks  
**Goal:** Understand the human and regulatory dimensions of spaceflight that complement pure engineering.

## 🚀 Projects

1. **[Crew Safety Simulator](Projects/Crew_Safety_Simulator/README.md):** Models G-forces and vibrations on astronauts during launch and landing using damped oscillation physics.
2. **[Space Policy Risk Calculator](Projects/Space_Policy_Calculator/README.md):** A framework to assess regulatory compliance and mission risk for space operations.

## Core Concepts

### Human Factors in Spaceflight

Astronauts face extreme physical stresses that must be carefully managed:

| Stress Type | Typical Limit | Example Context |
|-------------|---------------|-----------------|
| Sustained G-force | < 4g | Typical crewed ascent + capsule reentry (Crew Dragon, Soyuz, Shenzhou) |
| Peak G-force (short) | < 8g | Abort / contingency scenarios (launch escape, rapid off‑nominal decel) |
| Vibration | ~0.5g @ < 20 Hz | Engine + structural vibration during ascent (multi‑engine liquid stages, solids) |
| Impact | < 15g spike | Landing shock (parachute touchdown, splashdown, propulsive landing) |

### Damped Oscillation Model

A crew seat can be modeled as a mass-spring-damper system:

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

Where:
- $m$ = Mass of astronaut + seat
- $c$ = Damping coefficient (shock absorbers)
- $k$ = Spring constant (seat cushion/harness)
- $F(t)$ = External force (rocket acceleration × mass)

The **damping ratio** $\zeta = \frac{c}{2\sqrt{km}}$ determines response:
- $\zeta < 1$: Underdamped (oscillates)
- $\zeta = 1$: Critically damped (fastest settling)
- $\zeta > 1$: Overdamped (slow return)

### Space Policy Framework

Space operations are governed by multiple regulatory bodies:

| Agency | Jurisdiction | Key Requirements |
|--------|--------------|------------------|
| **FAA** | US Launch/Reentry | Launch license, safety analysis |
| **FCC** | US Communications | Spectrum allocation, interference |
| **NOAA** | US Earth Imaging | Remote sensing license |
| **ITU** | International | Orbital slot coordination |
| **UNOOSA** | International | Space debris guidelines |

### Orbital Debris Mitigation

The **25-Year Rule**: Satellites should deorbit within 25 years of mission end.

$$\text{Orbital Lifetime} \approx \frac{H}{C_D \cdot A/m \cdot \rho}$$

Higher orbits → longer lifetime → greater debris risk.

## Tools & Libraries
- `numpy` - Numerical computation
- `scipy` - ODE solvers
- `matplotlib` - Visualization

## References
- NASA-STD-3001: Human Systems Integration Requirements
- UN Guidelines for Space Debris Mitigation
- FAA 14 CFR Part 450: Launch and Reentry Licensing
- SpaceX Starlink FCC Filings

