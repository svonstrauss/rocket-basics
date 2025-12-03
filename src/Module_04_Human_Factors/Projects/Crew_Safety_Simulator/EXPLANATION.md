# Crew Safety Simulator - Technical Explanation

## Physics Background

### The Human Body Under Acceleration

Humans can tolerate significant G-forces, but limits depend on:

1. **Direction**: Gx (chest-to-back) is most tolerable, Gz (head-to-foot) causes blood pooling
2. **Duration**: Brief spikes (< 1s) up to 15g survivable, sustained > 4g causes issues
3. **Rate of Onset**: Gradual increase allows physiological adaptation

NASA and SpaceX design to these approximate limits:

| Condition | Limit | Duration |
|-----------|-------|----------|
| Nominal Launch | 3-4g | Minutes |
| Abort | 6-8g | Seconds |
| Landing | 4-6g | Seconds |
| Impact Spike | 10-15g | < 100ms |

### Vibration Concerns

The human body has resonant frequencies:
- **Whole body**: 4-8 Hz
- **Head/neck**: 20-30 Hz
- **Eyeballs**: 30-80 Hz

Rocket engines produce vibration across these bands. If vibration matches body resonance, it's amplified internally—causing discomfort, impaired vision, or injury.

---

## Mathematical Model

### Mass-Spring-Damper System

We model the astronaut-seat system as a **second-order linear ODE**:

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

Where `F(t) = m × a_spacecraft(t)` is the "base excitation" from the rocket.

### Standard Form

Dividing by mass:

$$\ddot{x} + 2\zeta\omega_n\dot{x} + \omega_n^2 x = a_{spacecraft}(t)$$

Where:
- $\omega_n = \sqrt{k/m}$ is the **natural frequency** (rad/s)
- $\zeta = \frac{c}{2\sqrt{km}}$ is the **damping ratio**

### Damping Ratio Interpretation

| ζ Value | Behavior | Pros | Cons |
|---------|----------|------|------|
| < 1 | Underdamped | Good high-freq filtering | Oscillates, overshoot |
| = 1 | Critically damped | Fastest settling | May be too stiff |
| > 1 | Overdamped | No oscillation | Slow response, poor filtering |

For crew comfort, ζ ≈ 0.5-0.8 is often optimal—good filtering with minimal oscillation.

---

## Transfer Function Analysis

In the frequency domain, the system acts as a **low-pass filter**:

$$H(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

The **magnitude response**:

$$|H(j\omega)| = \frac{1}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}$$

Where $r = \omega/\omega_n$ is the frequency ratio.

### Filtering Behavior

- **Low frequencies** (r << 1): Passed through (~1x gain)
- **At resonance** (r ≈ 1): Amplified if ζ < 0.707
- **High frequencies** (r >> 1): Attenuated (the filtering we want)

This is why the seat parameters matter: we want the natural frequency low enough that engine vibration (10-50 Hz) is in the "high frequency" regime and gets filtered.

---

## Implementation Details

### ODE Solver

I use `scipy.integrate.odeint` which implements the LSODA algorithm:
- Adaptive step size for stiff problems
- Handles the rapid changes during landing spikes well

### Acceleration Calculation

The crew experiences the **inertial acceleration**:

$$a_{crew} = a_{spacecraft} - \ddot{x}_{relative}$$

Where $\ddot{x}_{relative}$ is the acceleration of the mass relative to the spacecraft (found by differentiating the ODE solution).

When the seat compresses (positive $\ddot{x}$), it "absorbs" some of the spacecraft acceleration, reducing what the crew feels.

---

## Code Architecture

```
simulator.py
├── SeatParameters (dataclass)
│   ├── mass, spring_k, damping_c
│   └── Properties: natural_frequency, damping_ratio
│
├── create_launch_profile() → (time, accel)
├── create_landing_profile() → (time, accel)
│
├── CrewSafetySimulator (class)
│   ├── _equations_of_motion() - ODE definition
│   ├── simulate() - Runs odeint, stores results
│   ├── assess_safety() - Checks NASA limits
│   └── plot_results() - Visualization
│
├── compare_seat_configurations() - Trade study
└── run_demo() - Main entry point
```

---

## Validation

### Sanity Checks

1. **No damping (c=0)**: System should oscillate at natural frequency indefinitely
2. **Critical damping**: Should return to equilibrium fastest without overshoot
3. **DC response**: Constant acceleration should produce constant displacement x = F/k

### Physical Reasonableness

For typical parameters (m=80kg, k=50000 N/m, c=2500 N·s/m):
- Natural frequency: ~4 Hz (reasonable for a seat)
- Damping ratio: ~0.6 (moderately underdamped)
- At 3g constant acceleration: displacement ≈ 5 cm (realistic cushion compression)

---

## Limitations and Future Work

### Current Simplifications

1. **1-DOF model**: Real seats have multiple degrees of freedom (vertical, lateral, rotational)
2. **Linear springs**: Real cushions are nonlinear (stiffen under compression)
3. **No hysteresis**: Real dampers have velocity-dependent behavior
4. **Point mass**: Doesn't model human body dynamics (organs, spine)

### Potential Extensions

1. **Multi-DOF model**: Add lateral and rotational motion
2. **Frequency analysis**: FFT of input/output to visualize filtering
3. **Nonlinear springs**: Use piecewise or polynomial force models
4. **Monte Carlo**: Vary parameters to assess sensitivity

---

## SpaceX Relevance

SpaceX performs similar analyses for Crew Dragon and Starship:

1. **Crew Dragon seats** underwent extensive drop testing to validate shock absorption
2. **Starship landing** poses unique challenges—the flip maneuver and propulsive landing create complex acceleration profiles
3. **Raptor engine vibration** (33 engines!) must be damped to prevent crew discomfort

This simulator demonstrates understanding of:
- Dynamic systems modeling
- Human factors engineering
- Trade study methodology
- Numerical simulation

All skills directly applicable to SpaceX crew systems engineering roles.

