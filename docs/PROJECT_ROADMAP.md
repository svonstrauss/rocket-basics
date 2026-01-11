# Rocket Basics — Project Roadmap

**Goal:** Teach rocket science and space engineering through **executable notebooks** and **interactive simulations** (high school → college friendly).

**Guiding principles:**
- Clarity first: every page answers “what is this and what can I do next?” quickly
- Multi‑agency: examples should include NASA / ESA / Roscosmos / JAXA / CNSA / ISRO (not only SpaceX)
- Run anywhere: local runs + Binder/Colab links + hosted Streamlit where relevant

---

## What exists today (current state)

- **Modules 1–4** are implemented with learning notebooks and projects:
  - Module 1: Foundations (`src/Module_01_Foundations/`)
  - Module 2: Orbital Mechanics (`src/Module_02_Orbital_Mechanics/`)
  - Module 3: Propulsion & Systems (`src/Module_03_Propulsion/`)
  - Module 4: Human Factors & Policy (`src/Module_04_Human_Factors/`)
- **Project website (GitHub Pages)** via Quarto:
  - `index.qmd` (home + notebook links + Binder/Colab)
  - `simulations.qmd` (preview images + “run locally” commands + browser links where supported)
- **Interactive app**:
  - Propellant Explorer (Streamlit): `src/Module_03_Propulsion/Projects/Propellant_Explorer/app.py`

---

## Near‑term roadmap (make it polished + reliable)

### 1) Make the GitHub Pages build 100% reliable
- Ensure the **Quarto render** job succeeds on GitHub Actions
- Keep notebooks fast to execute (target: quick “time to read” + reasonable CI runtime)

### 2) Improve learner navigation
- One clear “start here” path (Module 1 → Module 2 → …)
- No dead ends (every module has a README + at least one notebook)
- Keep wording consistent across modules and the website

### 3) Add design tokens (docs + reuse)
- Define a small token set (color palette, spacing, typography) in JSON
- Keep the website and dashboards aligned with those tokens

---

## Module structure (now + planned)

### Module 1 — Foundations
- **Learn notebooks**: Newton’s Laws, rocket equation basics, orbital basics
- **Projects**: Rocket Ascent Simulator, Conic Orbit Visualizer

### Module 2 — Orbital Mechanics
- **Learn notebooks**: Hohmann transfers + launch windows
- **Projects**: Constellation Propagator (multi‑constellation), Mars Mission Simulator

### Module 3 — Propulsion & Systems
- **Learn notebooks**: engines, propellant trade‑offs + chemistry intuition
- **Projects**: Propellant Explorer (Streamlit), Trade Simulator, Constellation Designer

### Module 4 — Human Factors & Policy
- **Learn notebooks**: g‑loads + vibration, policy buckets + toy risk model
- **Projects**: Crew Safety Simulator, Space Policy Risk Calculator

### Module 5 — Astrophysics & Machine Learning (planned)
- Space weather + remote sensing + anomaly detection using public datasets (NASA/NOAA/ESA/etc.)
- Proposed projects:
  - Orbital anomaly detector (telemetry‑style features)
  - Solar flare / space weather predictor (forecasting + uncertainty)

### Module 6 — Capstone (planned)
- A single integrated mission that ties together:
  - trajectory + delta‑V budget
  - propulsion sizing + staging assumptions
  - human factors constraints
  - policy / compliance constraints

