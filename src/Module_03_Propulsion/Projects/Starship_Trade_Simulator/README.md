# Launch Vehicle Trade Simulator

**Module:** 3 (Propulsion & Systems Engineering)  
**Concepts:** Rocket Equation, Mass Ratios, Staging, Reusability

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Tsiolkovsky Equation** | Fundamental relationship between mass and velocity |
| **Mass Ratio** | Why rockets are mostly propellant |
| **Specific Impulse** | Engine efficiency metric |
| **Staging** | Why we throw away parts of the rocket |
| **Reusability Trade-offs** | What you sacrifice for landing legs |

## Project Overview

This tool simulates the **Systems Engineering** trade-offs inherent in rocket design. It uses the **Tsiolkovsky Rocket Equation** to analyze how different variables affect vehicle capability.

**Key Question:** "How much payload do you lose by landing the booster?"

## Global Launch Vehicles Compared

| Vehicle | Agency | LEO Payload | Isp (vac) | Reusable |
|---------|--------|-------------|-----------|----------|
| **Starship** | SpaceX | 150 t | 380 s | Full |
| **SLS Block 1** | NASA | 95 t | 366 s | No |
| **Falcon Heavy** | SpaceX | 64 t | 348 s | Partial |
| **Long March 5** | CNSA | 25 t | 430 s | No |
| **Ariane 6** | ESA | 22 t | 431 s | No |
| **H3** | JAXA | 6.5 t | 425 s | No |
| **Proton-M** | Roscosmos | 23 t | 326 s | No |
| **PSLV** | ISRO | 3.8 t | 316 s | No |

## Installation & Usage

```bash
pip install -r requirements.txt
python trade_simulator.py
```

## Interactive Features

- **Sliders:** Adjust propellant mass, dry mass, and Isp in real-time
- **Trade Curves:** See payload vs. delta-V for different reuse scenarios
- **Vehicle Comparison:** Side-by-side LEO capacity from world's rockets
- **Mission Targets:** Reference lines for LEO, GTO, TLI, Mars

## The Physics

### Tsiolkovsky Rocket Equation

The fundamental equation governing all chemical propulsion:

$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_f}\right)$$

Where:
- Δv = velocity change (m/s)
- Isp = specific impulse (seconds)
- g₀ = 9.80665 m/s²
- m₀ = initial mass (wet)
- m_f = final mass (dry + payload)

### Mass Ratio

$$R = \frac{m_0}{m_f} = \frac{m_{dry} + m_{prop} + m_{payload}}{m_{dry} + m_{payload}}$$

Higher is better. Structural limits cap R around 10-20.

### Reusability Penalty

Reusable vehicles carry extra mass:
- Landing legs and grid fins (~2% of stage mass)
- Landing propellant (~10-15% of original load)
- Thermal protection for re-entry
- Heavier structures for multiple flights

This increases m_dry, reducing the logarithm term and therefore Δv.

### Typical Delta-V Requirements

| Destination | From LEO | Total from Ground |
|-------------|----------|-------------------|
| LEO (400 km) | — | 9.4 km/s |
| GTO | 2.5 km/s | 11.9 km/s |
| Lunar orbit | 3.9 km/s | 13.3 km/s |
| Mars (C3=0) | 3.6 km/s | 13.0 km/s |

See `EXPLANATION.md` for complete derivations.
