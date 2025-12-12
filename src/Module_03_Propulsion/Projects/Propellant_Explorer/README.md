# 🚀 Propellant Explorer

An interactive dashboard for learning about rocket propellants, chemical reactions, and the Tsiolkovsky Rocket Equation.

## 🎯 Learning Objectives

By using this tool, students will understand:

1. **Specific Impulse (Isp)** - The "fuel efficiency" of rockets
2. **Density Trade-offs** - Why hydrogen needs huge tanks
3. **The Rocket Equation** - Why rockets are 90% fuel
4. **Stoichiometry** - Balancing combustion reactions

## 🏃 Quick Start

### Option 1: Interactive Web App (Recommended)

```bash
# Install dependencies
pip install streamlit plotly pandas numpy

# Run the app
cd src/Module_03_Propulsion/Projects/Propellant_Explorer
streamlit run app.py
```

Then open http://localhost:8501 in your browser!

### Option 2: Command Line Testing

```bash
# Test the physics engine
python physics_logic.py

# Test the reaction balancer
python reaction_logic.py
```

## 📊 The Four Views

### View 1: Efficiency Showdown
Compare specific impulse across propellant types. Learn why we use kerosene to get off the ground but hydrogen for deep space.

### View 2: Tank Size Reality Check
See the density trade-off - hydrogen is efficient but needs 10x larger tanks than kerosene!

### View 3: Mission Calculator
Design your own rocket! Adjust:
- Payload mass (satellite, crew, cargo)
- Structure mass (engines, tanks, body)
- Fuel mass
- Propellant type

See if you can reach orbit, the Moon, or Mars!

### View 4: Chemistry Balancer
Balance combustion reactions. Learn what happens with:
- **Perfect balance**: Maximum energy
- **Fuel rich**: Wasted fuel, soot
- **Fuel lean**: ENGINE MELTS! 🔥

## 🔬 The Math

### Tsiolkovsky Rocket Equation

$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_{initial}}{m_{final}}\right)$$

| Variable | Meaning |
|----------|---------|
| Δv | Change in velocity (m/s) |
| Isp | Specific Impulse (seconds) |
| g₀ | 9.81 m/s² |
| m_initial | Rocket + Fuel mass |
| m_final | Rocket mass (empty) |

### Mission Requirements

| Destination | Delta-V Required |
|-------------|------------------|
| Suborbital | ~2,000 m/s |
| Low Earth Orbit | ~9,400 m/s |
| Moon | ~12,500 m/s |
| Mars | ~16,000 m/s |

## 🧪 Propellant Data

| Propellant | Isp (vacuum) | Density | Used By |
|------------|--------------|---------|---------|
| Hydrolox (LH2/LOX) | 450s | 0.07 g/cm³ | SLS, Space Shuttle |
| Methalox (CH4/LOX) | 380s | 0.42 g/cm³ | Starship, New Glenn |
| RP-1/LOX | 350s | 0.81 g/cm³ | Falcon 9, Saturn V |
| Solid (HTPB) | 280s | 1.80 g/cm³ | SRBs |

## 📁 File Structure

```
Propellant_Explorer/
├── app.py              # Streamlit web interface
├── physics_logic.py    # Rocket equation calculations
├── reaction_logic.py   # Chemistry balancer
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎓 Teaching Tips

### For High School (AP Physics/Chemistry)
- Start with the Chemistry Balancer to connect to chemistry class
- Use Mission Calculator to show real-world applications
- Discuss why SpaceX chose methane for Starship

### For College Freshmen
- Derive the rocket equation from conservation of momentum
- Analyze the logarithm's "tyranny" - diminishing returns
- Compare staging strategies for different missions

## 🔗 Real-World Connections

- **SpaceX Falcon 9**: Uses RP-1/LOX for high thrust
- **SpaceX Starship**: Uses Methalox for reusability
- **NASA SLS**: Uses Hydrolox for efficiency
- **Space Shuttle**: Used both (SRBs + SSMEs)

## 📚 Further Reading

- [NASA Rocket Propulsion](https://www.grc.nasa.gov/www/k-12/rocket/rockth.html)
- [Everyday Astronaut: Rocket Fuel](https://everydayastronaut.com/rocket-fuel/)
- [SpaceX Raptor Engine](https://www.spacex.com/vehicles/starship/)

---

*Part of the Rocket Basics educational project*

