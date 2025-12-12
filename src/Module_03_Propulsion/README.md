# Module 3: Space Systems & Propulsion Engineering

**Duration:** 8 Weeks  
**Goal:** Understand rocket propulsion, trade-off analysis, and constellation design.

## 🎓 Learning Path

Start with the interactive notebooks in the `Learn/` folder:

| Notebook | Topics Covered | Time |
|----------|---------------|------|
| `01_Rocket_Engines.ipynb` | Engine types, Isp, Thrust-to-weight | 1-2 hours |

## 🚀 Projects

### 1. [Propellant Explorer](Projects/Propellant_Explorer/README.md) ⭐ NEW
**Interactive web dashboard for learning rocket propellants!**

Features:
- Compare fuel efficiency (Isp) across propellant types
- See why hydrogen needs huge tanks (density trade-offs)
- Design rockets and check if they reach orbit
- Balance chemical reactions (stoichiometry)

```bash
cd Projects/Propellant_Explorer
pip install -r requirements.txt
streamlit run app.py
```

### 2. [Starship Trade Simulator](Projects/Starship_Trade_Simulator/README.md)
Analyze payload vs. delta-V trade-offs:
- Multi-stage rocket analysis
- Reusability impact on payload
- Compare vehicles from NASA, SpaceX, ESA, CNSA

```bash
cd Projects/Starship_Trade_Simulator
python trade_simulator.py
```

### 3. [Constellation Designer](Projects/Constellation_Designer/README.md)
Design and visualize satellite constellations:
- Walker Delta patterns
- Coverage analysis
- Real constellation data (GPS, Starlink, etc.)

```bash
cd Projects/Constellation_Designer
python designer.py
```

## 📚 Key Concepts

### Propulsion Fundamentals
- **Thrust**: Force from exhaust momentum (F = ṁ × vₑ)
- **Specific Impulse (Isp)**: Fuel efficiency measure (seconds)
- **Mass ratio**: Initial vs final mass

### The "Big Three" Metrics

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| **Isp** | Fuel efficiency | Higher = more Δv per kg fuel |
| **Density** | Tank size needed | Denser = smaller tanks |
| **Thrust-to-Weight** | Liftoff capability | Must be >1 to leave ground |

### Key Equations

**Thrust:**
$$F = \dot{m} \cdot v_e$$

**Specific Impulse:**
$$I_{sp} = \frac{v_e}{g_0}$$

**Tsiolkovsky Rocket Equation:**
$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_f}\right)$$

## 🧪 Propellant Comparison

| Propellant | Isp (vac) | Density | Trade-off |
|------------|-----------|---------|-----------|
| **Hydrolox** (LH2/LOX) | 450s | 0.07 g/cm³ | Best efficiency, huge tanks |
| **Methalox** (CH4/LOX) | 380s | 0.42 g/cm³ | Balanced, great for reuse |
| **RP-1/LOX** | 350s | 0.81 g/cm³ | Dense, but leaves soot |
| **Solid** (HTPB) | 280s | 1.80 g/cm³ | Simple, can't throttle |

## 🔥 Engine Data

| Engine | Company | Propellant | Isp (vac) |
|--------|---------|------------|-----------|
| Merlin 1D | SpaceX | RP-1/LOX | 311s |
| Raptor 2 | SpaceX | CH4/LOX | 380s |
| RS-25 | Aerojet | LH2/LOX | 452s |
| BE-4 | Blue Origin | CH4/LOX | 341s |

## 🛠️ Setup

```bash
# For all projects
pip install numpy matplotlib scipy

# For Propellant Explorer web app
pip install streamlit plotly pandas
```

---

*"Failure is an option here. If things are not failing, you are not innovating enough."* — Elon Musk
