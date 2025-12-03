# Module 3: Space Systems & Propulsion Engineering

**Duration:** 8 Weeks  
**Goal:** Understand rocket propulsion fundamentals and apply systems engineering principles to vehicle design.

## Projects

1. **[Starship Trade Simulator](Projects/Starship_Trade_Simulator/README.md):** Interactive tool analyzing payload vs. delta-v trade-offs for reusable rockets.
2. **[Constellation Designer](Projects/Constellation_Designer/README.md):** Design and visualize satellite constellations with coverage analysis.

## Core Concepts

### The Rocket Equation (Tsiolkovsky)
The fundamental equation governing all rocket propulsion:

$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_f}\right)$$

Where:
- $\Delta v$ = Change in velocity (m/s)
- $I_{sp}$ = Specific impulse (s) - engine efficiency metric
- $g_0$ = Standard gravity (9.80665 m/s²)
- $m_0$ = Initial mass (wet)
- $m_f$ = Final mass (dry + payload)

### Mass Ratio
The ratio $\frac{m_0}{m_f}$ is called the **mass ratio**. Higher is better, but structural limits cap it around 10-20 for most rockets.

### Staging
Why stage? Each stage can be optimized for its flight regime:
- **Stage 1:** High thrust, sea-level optimized nozzles
- **Stage 2:** High Isp, vacuum-optimized nozzles

Staging also discards dead weight (empty tanks, engines) to improve mass ratio for subsequent burns.

### Reusability Trade-offs
Reusable rockets must carry:
- Landing legs and grid fins
- Extra propellant for landing burns
- Thermal protection for re-entry

This increases dry mass, reducing payload capacity. The trade-off: lower cost per launch vs. lower payload per launch.

### Constellation Design (Walker Delta)
Satellite constellations are described by the notation $i:t/p/f$:
- $i$ = Inclination
- $t$ = Total satellites
- $p$ = Number of orbital planes
- $f$ = Phasing factor

## Weekly Schedule

### Week 1-2: Propulsion Fundamentals
- Thrust equation derivation
- Specific impulse and efficiency
- Nozzle design basics

### Week 3-4: Rocket Equation Applications
- Single-stage vs. multi-stage analysis
- Mass budgets and margins
- Reusability penalties

### Week 5-6: Systems Engineering
- Trade study methodology
- Requirements flow-down
- Design margins and factors of safety

### Week 7-8: Constellation Design
- Walker patterns
- Coverage analysis
- Link budgets (intro)

## Tools & Libraries
- `numpy` - Numerical computation
- `matplotlib` - Visualization and interactive widgets
- `scipy` - Optimization

## References
- Sutton, G. "Rocket Propulsion Elements"
- Wertz, J. "Space Mission Analysis and Design" (SMAD)
- Humble, R. "Space Propulsion Analysis and Design"

