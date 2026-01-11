# Rocket Basics — Implementation Plan

**Purpose:** Keep the repository coherent as it grows. This is an internal plan to prevent “we forgot a whole feature” moments.

**North star:** Teach rocket science and space engineering through **executable notebooks** and **interactive simulations** (high school → college friendly).

## Principles (non‑negotiables)

- **Clarity first**: every page answers “What is this and what can I do next?” in <3 seconds.
- **Multi‑agency**: examples should include NASA / ESA / Roscosmos / JAXA / CNSA / ISRO where relevant (not only SpaceX).
- **Run anywhere**: local runs + Binder/Colab for notebooks + hosted Streamlit where it makes sense.
- **Accessible by default**: readable text sizes, strong contrast, keyboard focus visible.
- **Consistent patterns**: repeated UI patterns across visualizers (colors, info panels, telemetry layout).

---

## Current state (what exists today)

- **Modules 1–4**: learning notebooks + simulations are implemented.
- **Module 5**: first learning notebook exists (`src/Module_05_Astrophysics_ML/Learn/01_Space_Data_Basics.ipynb`).
- **Module 6**: first capstone planning notebook exists (`src/Module_06_Capstone/Learn/01_Capstone_Planning.ipynb`).
- **Website (GitHub Pages)**: Quarto site renders notebooks and links to simulations.
- **Binder/Colab links**: available from `index.qmd`.
- **Streamlit app**: Propellant Explorer exists (deploy separately).

---

## Repo structure (keep it consistent)

- `src/Module_01_Foundations/`
- `src/Module_02_Orbital_Mechanics/`
- `src/Module_03_Propulsion/`
- `src/Module_04_Human_Factors/`
- `src/Module_05_Astrophysics_ML/`
- `src/Module_06_Capstone/`

Each module should have:

- `README.md` (what it is + next step)
- `Learn/` (notebooks; short and runnable end‑to‑end)
- `Projects/` (where applicable; runnable locally with a clear README)

---

## Workstreams (what we build next)

### 1) Learning notebooks (curriculum)

**Goal:** Every module has at least 1–3 notebooks that teach core concepts with clear visuals and exercises.

- **Module 5 (Astrophysics & ML)**
  - Add `02_Anomaly_Detection_Basics.ipynb` (from thresholds → z‑scores → simple models)
  - Add `03_Forecasting_Basics.ipynb` (baselines + uncertainty; keep it simple and teachable)

- **Module 6 (Capstone)**
  - Add a capstone “template” notebook: requirements → budgets → assumptions → outputs
  - Add `Projects/Capstone_Mission/` skeleton (README + minimal runnable script)

**Notebook quality bar**

- Runs in <60–90 minutes for a learner
- No network dependency required to execute (use toy data unless optional downloads)
- Uses plain language (grade 8-ish) and explains *why* each step exists

---

### 2) Simulations (visualizers)

**Goal:** Keep simulations consistent, readable, and educational.

Baseline checklist for each simulation:

- **UI readability**: no tiny fonts; no clipped text; legends not stacked; layouts don’t overlap.
- **Telemetry**: show the core “what’s happening” numbers (units included).
- **Animation**: if the concept is dynamic, the plot should move (within reason).
- **Educational framing**: short on-screen “what to notice” + a clear next action.

---

### 3) Website (GitHub Pages)

**Goal:** Site is a clean portal: learn (notebooks) → run (simulations/apps) → contribute.

Immediate improvements:

- Add a dedicated “Modules” page (optional) that explains progression and links to notebooks/projects.
- Keep `simulations.qmd` updated with new projects and “run locally” commands.
- Add a small design token file (see next section) and keep site styling aligned.

---

### 4) Design tokens (shared styling)

**Goal:** Make the dashboards and website feel like one product.

Add a small JSON token set (colors, spacing, typography) and reference it from:
- `website.css`
- Matplotlib/Plotly styling helpers in simulations

Proposed file:
- `docs/design_tokens.json`

---

## Definition of “done” for Modules 5–6 (minimum viable)

- Module 5:
  - 3 notebooks rendered on the website
  - at least 1 small, runnable project skeleton (even if toy‑data first)

- Module 6:
  - capstone planning notebook + capstone project template exists
  - clear “how to extend this” guidance (no dead ends)

---

## Quick maintenance checklist (do this when adding anything)

- Update module `README.md` and `Learn/README.md` if you add a notebook.
- Add the notebook to `_quarto.yml` render list + navbar (if it should be visible on the site).
- Add Binder/Colab links in `index.qmd` for new notebooks.
- Keep examples multi‑agency when possible.

