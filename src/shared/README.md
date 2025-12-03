# Shared Visualization Platform

This directory contains the unified visualization infrastructure for all orbital mechanics simulations in this repository. It bridges the Python physics simulations with a high-fidelity OpenGL renderer.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Python Simulations                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │    Starlink     │  │  Constellation  │  │   Trajectory    │     │
│  │   Propagator    │  │    Designer     │  │    Planner      │     │
│  │   (J2 Physics)  │  │ (Walker Patterns)│  │  (Hohmann/Lambert)│   │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘     │
│           │                    │                    │               │
│           └────────────────────┼────────────────────┘               │
│                                │                                    │
│                    ┌───────────▼───────────┐                       │
│                    │  trajectory_exporter  │                       │
│                    │    (Python Module)    │                       │
│                    └───────────┬───────────┘                       │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                                 │  CSV Data File
                                 │  (trajectories.csv)
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                      OpenGL Earth Viewer                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    C++ / OpenGL 3.2                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │   │
│  │  │   Earth     │  │  Satellite  │  │  Trackball  │         │   │
│  │  │  Renderer   │  │  Renderer   │  │   Camera    │         │   │
│  │  │ (Day/Night) │  │  (Trails)   │  │ (Controls)  │         │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Features:                                                          │
│  • NASA Blue Marble / Black Marble textures                        │
│  • Animated cloud layer with Perlin noise drift                    │
│  • Lambert shading for realistic day/night terminator              │
│  • GPU-accelerated satellite trajectory rendering                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### `trajectory_exporter.py`
Python module that converts simulation output to the CSV format expected by the viewer.

```python
from trajectory_exporter import export_trajectories

trajectories = {
    "Satellite-1": {'x': [...], 'y': [...], 'z': [...]}
}
export_trajectories(trajectories, "output.csv")
```

### `run_visualization.py`
Unified launcher script for the entire visualization pipeline.

```bash
# Generate demo data and launch viewer
python run_visualization.py --demo --view

# Run Starlink simulation, export data, launch viewer
python run_visualization.py --sim starlink --export --view

# Just launch viewer with existing data
python run_visualization.py --view
```

### `EarthViewer/`
The OpenGL Earth rendering application. See [EarthViewer/README.md](EarthViewer/README.md) for build instructions.

## Quick Start

### 1. Generate Demo Data
```bash
cd src/shared
python run_visualization.py --demo
```

### 2. Build the Viewer (Windows)
```powershell
cd src/shared/EarthViewer
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

### 3. Launch
```bash
cd src/shared
python run_visualization.py --view
```

## Data Flow

1. **Simulation** (Python): Computes orbital mechanics (J2, Hohmann, etc.)
2. **Export** (Python): Converts positions from meters/km to normalized Earth radii
3. **Load** (C++): Parses CSV into satellite trajectory structures
4. **Render** (OpenGL): Draws Earth with textures + satellite points/trails

## Why This Architecture?

| Approach | Pros | Cons |
|----------|------|------|
| **Python Only (Matplotlib)** | Simple, cross-platform | Slow, limited visual quality |
| **OpenGL Only** | Fast, beautiful | Physics in C++ is tedious |
| **Hybrid (This)** | Best of both worlds | Two codebases to maintain |

The hybrid approach lets us:
- Use Python's scientific ecosystem for physics (NumPy, SciPy)
- Use OpenGL for GPU-accelerated, publication-quality rendering
- Demonstrate proficiency in both languages (portfolio value!)

## Extending the System

### Adding a New Simulation

1. Create your Python simulation with position history output
2. Add an export function:

```python
def export_to_viewer(sim_data, output_path=None):
    from src.shared.trajectory_exporter import export_trajectories, get_viewer_data_path
    
    if output_path is None:
        output_path = get_viewer_data_path()
    
    export_trajectories(sim_data.history, output_path)
```

3. Register in `run_visualization.py`:

```python
SIMS["my_sim"] = os.path.join(REPO_ROOT, "src", "Module_XX", "my_sim.py")
```

### Modifying the Viewer

The key files to edit:
- `EarthViewer/source/earth.cpp` - Main application logic
- `EarthViewer/shaders/fshader.glsl` - Fragment shader (lighting, textures)
- `EarthViewer/shaders/vshader.glsl` - Vertex shader (transformations)

## Performance Notes

- The viewer targets 60 FPS with thousands of trajectory points
- Satellite trails are rendered as GL_LINE_STRIP for efficiency
- Earth texture resolution can be adjusted in the PNG files
- Sphere mesh resolution is set to 64 segments (adjustable in `init()`)

