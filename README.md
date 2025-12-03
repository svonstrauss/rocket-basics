# 🚀 Rocket Basics: Learn Space Engineering Through Code

A hands-on educational repository for learning aerospace engineering, orbital mechanics, and rocket science through executable Python simulations. Built from first principles with real physics.

**Perfect for:** Students, developers curious about aerospace, or anyone who's ever wondered "how does a rocket actually get to orbit?"

---

## 🎓 What You'll Learn

| Concept | Where It's Taught | Real-World Application |
|---------|-------------------|------------------------|
| **Orbital Mechanics** | Module 1 & 2 | How satellites stay in orbit |
| **Rocket Equation** | Module 3 | Why rockets need so much fuel |
| **Delta-V Budgets** | Module 2 & 3 | Planning missions to Mars |
| **G-Forces & Safety** | Module 4 | Keeping astronauts safe |
| **Numerical Integration** | Module 1 | Simulating trajectories accurately |
| **Perturbation Theory** | Module 2 | Why satellite orbits drift |

---

## 📚 Course Modules

| Module | Focus | Key Concepts |
|--------|-------|--------------|
| **[Module 1](src/Module_01_Foundations/README.md)** | Foundations | Newton's Laws, RK4 Integration, Kepler's Equations |
| **[Module 2](src/Module_02_Orbital_Mechanics/README.md)** | Orbital Mechanics | J2 Perturbations, Hohmann Transfers, Lambert's Problem |
| **[Module 3](src/Module_03_Propulsion/README.md)** | Propulsion & Systems | Tsiolkovsky Equation, Mass Ratios, Staging |
| **[Module 4](src/Module_04_Human_Factors/README.md)** | Human Factors | G-Force Limits, Vibration Analysis, Space Policy |
| **Module 5** | Astrophysics & ML | *Coming Soon* |
| **Module 6** | Capstone Mission | *Coming Soon* |

---

## 🔬 Featured Simulations

### 1. Rocket Ascent Simulator
**Learn:** How rockets fight gravity and drag to reach orbit

```bash
cd src/Module_01_Foundations/Projects/Rocket_Ascent_Simulator
pip install -r requirements.txt
python simulation.py
```

**Physics Concepts:**
- Newton's 2nd Law: F = ma for multi-body forces
- Atmospheric drag: D = ½ρv²CdA
- Runge-Kutta 4 integration for accurate trajectories
- Thrust-to-weight ratio and gravity turn maneuvers

---

### 2. Conic Orbit Visualizer
**Learn:** The mathematics of orbital paths (circles, ellipses, parabolas, hyperbolas)

```bash
cd src/Module_01_Foundations/Projects/Conic_Orbit_Visualizer
pip install -r requirements.txt
python visualizer.py
```

**Physics Concepts:**
- Vis-viva equation: v² = μ(2/r - 1/a)
- Orbital period: T = 2π√(a³/μ)
- Eccentricity and orbit shape
- Real missions: ISS, GPS, Voyager, Artemis

---

### 3. Satellite Constellation Propagator
**Learn:** How GPS, Starlink, and other constellations work

```bash
cd src/Module_02_Orbital_Mechanics/Projects/Starlink_Propagator
pip install -r requirements.txt
python propagator.py
```

**Physics Concepts:**
- J2 perturbation from Earth's oblate shape
- Nodal regression: why orbits precess
- Walker Delta constellation patterns
- Ground track coverage analysis

**Real Systems Compared:** GPS (USA), GLONASS (Russia), Galileo (EU), BeiDou (China), Starlink, OneWeb

---

### 4. Interplanetary Trajectory Planner
**Learn:** How to plan a mission to Mars

```bash
cd src/Module_02_Orbital_Mechanics/Projects/Starship_Trajectory_Planner
pip install -r requirements.txt
python mission_planner.py        # Animated Hohmann transfer
python porkchop/plotter.py       # Launch window analysis
```

**Physics Concepts:**
- Hohmann transfer orbits
- Synodic period and phase angles
- Delta-V budgets for interplanetary missions
- Porkchop plots for launch window optimization

---

### 5. Launch Vehicle Trade Simulator
**Learn:** Why rocket design involves difficult trade-offs

```bash
cd src/Module_03_Propulsion/Projects/Starship_Trade_Simulator
pip install -r requirements.txt
python trade_simulator.py
```

**Physics Concepts:**
- Tsiolkovsky rocket equation: Δv = Isp·g₀·ln(m₀/m_f)
- Mass ratio and staging
- Reusability vs. payload capacity trade-offs

**Vehicles Compared:** Starship (SpaceX), SLS (NASA), Ariane 6 (ESA), Long March 5 (CNSA), H3 (JAXA)

---

### 6. Crew Safety Simulator
**Learn:** How engineers keep astronauts safe during launch and reentry

```bash
cd src/Module_04_Human_Factors/Projects/Crew_Safety_Simulator
pip install -r requirements.txt
python simulator.py
```

**Physics Concepts:**
- Damped harmonic oscillators (crew seat modeling)
- Human G-force tolerance limits (NASA standards)
- Vibration frequency analysis
- Comparative vehicle profiles

**Vehicles Analyzed:** Crew Dragon, Soyuz, Apollo, Space Shuttle, New Shepard, Shenzhou

---

## 🛠️ Tech Stack

- **Python 3.10+** with NumPy, Matplotlib, SciPy
- **C++/OpenGL** for advanced 3D visualization (optional)

---

## 📁 Repository Structure

```
rocket-basics/
├── src/
│   ├── Module_01_Foundations/      # Newton's laws, numerical methods
│   ├── Module_02_Orbital_Mechanics/ # Kepler, perturbations, transfers
│   ├── Module_03_Propulsion/       # Rocket equation, staging
│   ├── Module_04_Human_Factors/    # Safety, policy
│   └── shared/                     # OpenGL Earth viewer (advanced)
└── README.md
```

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/svonstrauss/rocket-basics.git
cd rocket-basics

# Run your first simulation
cd src/Module_01_Foundations/Projects/Conic_Orbit_Visualizer
pip install -r requirements.txt
python visualizer.py
```

---

## 📖 Educational Resources

Each project includes:
- **README.md** - Overview and usage instructions
- **EXPLANATION.md** - Detailed physics and math derivations
- **Commented code** - Learn by reading the implementation

---

## 🤝 Contributing

Found a bug? Want to add a new simulation? PRs are welcome!

---

## 📜 License

MIT License - Use freely for learning and teaching.

---

*"The rocket worked perfectly, except for landing on the wrong planet." — Wernher von Braun*

*Built with physics, math, and a passion for making space accessible to everyone.*
