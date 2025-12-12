# Module 2: Orbital Mechanics and Mission Design

**Duration:** 8 Weeks  
**Goal:** Master orbital mechanics for satellite operations and interplanetary mission planning.

## 🎓 Learning Path

Start with the interactive notebooks in the `Learn/` folder:

| Notebook | Topics Covered | Time |
|----------|---------------|------|
| `01_Interplanetary_Travel.ipynb` | Hohmann transfers, Delta-V, Launch windows | 1-2 hours |

## 🚀 Projects

### 1. [Starlink Orbit Propagator](Projects/Starlink_Propagator/README.md)
Propagate satellite orbits with real physics:
- J2 perturbation effects
- Ground track visualization
- Multi-constellation support (GPS, GLONASS, Galileo, etc.)

```bash
cd Projects/Starlink_Propagator
python propagator.py
```

### 2. [Mars Mission Simulator](Projects/Starship_Trajectory_Planner/README.md)
Complete Earth-to-Mars mission simulation:
- Animated Hohmann transfer
- Entry, Descent, Landing (EDL) simulation
- Porkchop plot analysis
- Historical mission data

```bash
cd Projects/Starship_Trajectory_Planner
python mission_planner.py
```

## 📚 Key Concepts

### Orbital Elements
- Semi-major axis (a) - orbit size
- Eccentricity (e) - orbit shape
- Inclination (i) - orbit tilt

### Key Equations

**Vis-Viva Equation:**
$$v = \sqrt{\mu\left(\frac{2}{r} - \frac{1}{a}\right)}$$

**Hohmann Transfer Time:**
$$T = \pi\sqrt{\frac{a^3}{\mu}}$$

**Orbital Period:**
$$T = 2\pi\sqrt{\frac{a^3}{\mu}}$$

## 🌍 Real Mission Data Included

| Mission | Agency | Type |
|---------|--------|------|
| Starlink | SpaceX | LEO Internet |
| GPS | US Space Force | Navigation |
| Galileo | ESA | Navigation |
| BeiDou | CNSA | Navigation |
| Perseverance | NASA | Mars Rover |
| Tianwen-1 | CNSA | Mars Orbiter+Rover |

## 🛠️ Setup

```bash
pip install numpy matplotlib scipy
```

---

*"The universe is a pretty big place. If it's just us, seems like an awful waste of space."* — Carl Sagan
