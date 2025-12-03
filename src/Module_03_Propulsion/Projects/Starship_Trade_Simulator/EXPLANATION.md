# Starship Trade Simulator: Technical Explanation

## Overview

This document explains the physics and systems engineering principles behind the Starship Trade Simulator. We cover the Tsiolkovsky rocket equation, staging analysis, and the trade-offs inherent in reusable rocket design.

---

## 1. The Tsiolkovsky Rocket Equation

### Derivation

The rocket equation relates velocity change to mass ratio. Starting from Newton's second law and conservation of momentum:

$$F = ma = m\frac{dv}{dt}$$

For a rocket expelling mass at exhaust velocity $v_e$:

$$m\frac{dv}{dt} = -v_e \frac{dm}{dt}$$

Separating variables and integrating:

$$\int_0^{\Delta v} dv = -v_e \int_{m_0}^{m_f} \frac{dm}{m}$$

$$\Delta v = v_e \ln\left(\frac{m_0}{m_f}\right)$$

### Specific Impulse Form

Using specific impulse $I_{sp}$ (thrust per unit weight flow rate):

$$v_e = I_{sp} \cdot g_0$$

Where $g_0 = 9.80665$ m/s² is standard gravity. The equation becomes:

$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_f}\right)$$

---

## 2. Mass Definitions

### Mass Breakdown

- **Wet Mass ($m_0$):** Total mass at ignition (structure + propellant + payload)
- **Dry Mass ($m_{dry}$):** Structure mass without propellant
- **Propellant Mass ($m_p$):** Fuel + oxidizer
- **Payload Mass ($m_{payload}$):** Useful cargo delivered to orbit
- **Final Mass ($m_f$):** $m_{dry} + m_{payload}$

### Mass Ratio

$$MR = \frac{m_0}{m_f} = \frac{m_{dry} + m_p + m_{payload}}{m_{dry} + m_{payload}}$$

Higher mass ratio = more delta-v. Structural limits typically cap MR at 10-20.

---

## 3. Staging Analysis

### Why Stage?

A single-stage rocket must carry empty tanks and engines through the entire flight. Staging allows:
1. Discarding dead weight (empty tanks, first-stage engines)
2. Optimizing each stage for its flight regime (sea-level vs. vacuum)
3. Achieving higher total mass ratios

### Two-Stage Delta-V

For a two-stage vehicle:

$$\Delta v_{total} = \Delta v_1 + \Delta v_2$$

Where each stage follows the rocket equation independently.

**Stage 1 (Booster):**
$$\Delta v_1 = I_{sp,1} \cdot g_0 \cdot \ln\left(\frac{m_{wet,1}}{m_{dry,1} + m_{wet,2} + m_{payload}}\right)$$

**Stage 2 (Ship):**
$$\Delta v_2 = I_{sp,2} \cdot g_0 \cdot \ln\left(\frac{m_{wet,2} + m_{payload}}{m_{dry,2} + m_{payload}}\right)$$

---

## 4. Reusability Trade-Offs

### The Reusability Penalty

Reusable rockets must carry additional hardware:
- Landing legs
- Grid fins (aerodynamic control)
- Extra propellant for landing burns
- Thermal protection (if re-entering)

This increases dry mass, reducing the mass ratio.

### Three Operating Modes

**1. Expendable Mode**
- Minimum dry mass (no landing hardware)
- Maximum payload capacity
- Highest cost per flight

**2. Booster Reuse Mode**
- Booster returns to launch site or drone ship
- Upper stage is expended
- Moderate payload reduction
- Significant cost savings

**3. Fully Reusable Mode**
- Both stages return and land
- Maximum dry mass penalty
- Lowest payload capacity
- Lowest cost per kg to orbit (if flight rate is high)

### Quantifying the Penalty

If landing hardware adds $\Delta m_{dry}$ to the dry mass:

$$\Delta v_{reusable} = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_{dry} + \Delta m_{dry} + m_{payload}}\right)$$

The payload reduction for the same delta-v target can be calculated by solving:

$$m_{payload,reusable} = m_{payload,expendable} - \Delta m_{dry} \cdot \frac{m_0}{m_f}$$

---

## 5. Trade Study Methodology

### Parametric Analysis

The simulator varies input parameters to map the trade space:

1. **Payload mass** (independent variable, x-axis)
2. **Delta-v capability** (dependent variable, y-axis)
3. **Operating mode** (separate curves)

### Key Insights

The curves reveal:
- **Crossover points:** Where one mode becomes preferable
- **Payload limits:** Maximum payload for each mode to reach a given delta-v
- **Sensitivity:** How changes in Isp or dry mass affect capability

---

## 6. Interactive Controls

### Slider Parameters

**Ship Propellant (tonnes):**
- Range: 1000 - 1500 tonnes
- Effect: More propellant increases mass ratio (more delta-v)

**Ship Dry Mass (tonnes):**
- Range: 80 - 150 tonnes
- Effect: Lower dry mass improves mass ratio

**Ship Isp (seconds):**
- Range: 350 - 390 s
- Effect: Higher Isp directly increases delta-v (linear relationship)

### Real-Time Update

When a slider moves:
1. Recalculate all three curves with new parameters
2. Update plot data without redrawing axes
3. Call `fig.canvas.draw_idle()` for efficient rendering

---

## 7. Reference Delta-V Targets

### LEO (Low Earth Orbit)
- **Target:** ~9,400 m/s
- Includes gravity losses (~1,500 m/s) and drag losses (~100 m/s)

### TLI (Trans-Lunar Injection)
- **Target:** ~12,800 m/s
- LEO + ~3,100 m/s for lunar transfer

### Mars Transfer
- **Target:** ~15,000+ m/s
- Requires orbital refueling for Starship architecture

---

## 8. Assumptions and Simplifications

1. **Constant Isp:** Real engines vary with altitude (sea-level vs. vacuum)
2. **Instantaneous burns:** Gravity losses not explicitly modeled
3. **Circular staging:** Booster/Ship separation at a fixed point
4. **No propellant reserves:** Real vehicles keep reserves for contingencies

---

## References

1. Sutton, G.P. and Biblarz, O. "Rocket Propulsion Elements," 9th Edition
2. Humble, R.W. et al. "Space Propulsion Analysis and Design"
3. SpaceX Starship User's Guide (public version)
