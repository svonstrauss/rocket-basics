# Module 1: Foundations in Math, Physics, and Computation

**Duration:** 8 Weeks  
**Goal:** Build the core math and physics foundation for rocket science through hands-on learning.

## 🎓 Learning Path

Start with the interactive notebooks in the `Learn/` folder:

| Notebook | Topics Covered | Time |
|----------|---------------|------|
| `01_Introduction_to_Rocket_Science.ipynb` | Newton's Laws, Rocket Equation, Gravity | 1-2 hours |
| `02_Orbital_Mechanics_Basics.ipynb` | Orbits, Orbital Velocity, LEO/GEO | 1-2 hours |

## 🚀 Projects

After completing the learning notebooks, explore the interactive simulators:

### 1. [Rocket Ascent Simulator](Projects/Rocket_Ascent_Simulator/README.md)
A 3D rocket launch simulation with:
- Realistic physics (thrust, drag, gravity)
- RK4 numerical integration
- Visual trajectory analysis

```bash
cd Projects/Rocket_Ascent_Simulator
python simulation.py
```

### 2. [Conic Orbit Visualizer](Projects/Conic_Orbit_Visualizer/README.md)
Interactive orbital trajectory visualization:
- Different orbit types (circular, elliptical, hyperbolic)
- Real mission data from NASA, ESA, CNSA, ISRO
- Delta-V calculations

```bash
cd Projects/Conic_Orbit_Visualizer
python visualizer.py
```

## 📚 Key Concepts Covered

### Physics
- Newton's Laws of Motion
- Gravitational Force
- Conservation of Momentum
- Orbital Mechanics basics

### Mathematics
- Parametric equations
- Polar coordinates
- Differential equations
- Numerical methods (Euler, RK4)

### Equations You'll Master

**Rocket Equation:**
$$\Delta v = v_e \cdot \ln\left(\frac{m_0}{m_f}\right)$$

**Orbital Velocity:**
$$v = \sqrt{\frac{\mu}{r}}$$

**Gravitational Acceleration:**
$$g = \frac{GM}{r^2}$$

## 🛠️ Setup

```bash
pip install numpy matplotlib scipy
```

## 📖 External Resources

- [NASA Glenn Research Center](https://www.grc.nasa.gov/www/k-12/rocket/rktprs.html) - Rocket physics tutorials
- [Kerbal Space Program](https://www.kerbalspaceprogram.com/) - Learn orbital mechanics through play
- [3Blue1Brown](https://www.youtube.com/c/3blue1brown) - Beautiful math visualizations

---

*"The rocket equation is like a cruel equation. It's not your friend."* — Elon Musk
