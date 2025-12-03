# Orbital Visualization Platform - Earth Viewer

A high-fidelity OpenGL Earth renderer with satellite trajectory visualization. This viewer integrates with the Python orbital mechanics simulations in this repository, providing GPU-accelerated rendering with realistic lighting effects.

## Features

- **NASA Blue Marble Textures:** Day-side Earth with the iconic Blue Marble imagery
- **City Lights at Night:** Black Marble texture shows city lights on the dark side
- **Animated Cloud Layer:** Drifting clouds with Perlin noise distortion
- **Day/Night Cycle:** Smooth terminator with Lambert shading
- **Satellite Trajectories:** Load and visualize orbital paths from simulation data
- **Interactive Camera:** Trackball rotation, zoom, and pan controls

## Screenshots

*The viewer displays Earth with realistic lighting and satellite constellation overlays.*

## Requirements

- Windows 10/11 (macOS/Linux with minor CMake adjustments)
- Visual Studio 2022 Build Tools (or VS 2022)
- CMake 3.10+
- GPU with OpenGL 3.2+ support

## Build Instructions

### Windows (PowerShell)

```powershell
# From repository root
cd src/shared/EarthViewer

# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release -j 4
```

### Run

```powershell
# Run the viewer
build/Release/earth.exe
```

## Controls

| Key/Action | Function |
|------------|----------|
| **Mouse Drag** | Rotate view |
| **Shift + Drag** | Zoom in/out |
| **Alt + Drag** | Pan camera |
| **SPACE** | Pause/Resume animation |
| **W** | Toggle wireframe mode |
| **S** | Toggle satellite visibility |
| **T** | Toggle trajectory trails |
| **UP/DOWN** | Adjust playback speed |
| **R** | Reset animation to frame 0 |
| **ESC** | Quit |

## Integration with Python Simulations

The viewer loads trajectory data from `data/trajectories.csv`. To export data from the Python simulations:

### From Starlink Propagator

```bash
cd src/Module_02_Orbital_Mechanics/Projects/Starlink_Propagator
python propagator.py --export --no-plot
```

### From Constellation Designer

```python
from src.shared.trajectory_exporter import export_from_constellation_designer

designer = ConstellationDesigner()
# ... add shells ...
export_from_constellation_designer(designer)
```

### Manual Export

```python
from src.shared.trajectory_exporter import export_trajectories

trajectories = {
    "Satellite-1": {
        'x': [...],  # List of X positions (km)
        'y': [...],  # List of Y positions (km)
        'z': [...]   # List of Z positions (km)
    }
}

export_trajectories(trajectories, "path/to/output.csv")
```

## Data Format

The trajectory CSV format is:

```csv
name,x,y,z,r,g,b
Sat-0-0,1.086234,0.000000,0.000000,0.000,1.000,1.000
Sat-0-0,1.086123,0.012345,0.008765,0.000,1.000,1.000
...
```

Where:
- `name`: Satellite identifier
- `x,y,z`: Position in normalized Earth radii (Earth radius = 1.0)
- `r,g,b`: Color values (0.0 - 1.0)

## Architecture

```
EarthViewer/
├── source/
│   ├── earth.cpp          # Main application
│   └── common/            # Math utilities, mesh generation
├── shaders/
│   ├── vshader.glsl       # Vertex shader
│   └── fshader.glsl       # Fragment shader (day/night/clouds)
├── images/
│   ├── world.200405.3.png # NASA Blue Marble (day)
│   ├── BlackMarble.png    # NASA Black Marble (night lights)
│   ├── cloud_combined.png # Cloud layer
│   └── perlin_noise.png   # Noise for cloud drift
├── data/
│   └── trajectories.csv   # Satellite position data
└── glfw-3.2/              # Windowing library
```

## Day/Night Shading

The fragment shader computes realistic lighting:

```glsl
// Lambert diffuse for day side
float lambert = max(dot(N, L), 0.0);

// Day texture weighted by illumination
vec3 dayColor = textureEarth.rgb * lambert;

// Night lights fade in smoothly on dark side
float nightIntensity = pow(1.0 - lambert, 3.0);
vec3 nightColor = textureNight.rgb * nightIntensity;

// Combine with clouds
vec3 finalColor = clamp(dayColor + nightColor + clouds, 0.0, 1.0);
```

## Credits

- Blue Marble and Black Marble imagery © NASA
- GLFW for windowing and input
- GLAD for OpenGL loading
- lodepng for PNG decoding

## Troubleshooting

**Window closes immediately:**
- Run from terminal to see error messages
- Verify GPU supports OpenGL 3.2+

**Black screen:**
- Press W to toggle wireframe (confirms geometry is rendering)
- Check that texture files exist in `images/`

**No satellites visible:**
- Press S to toggle satellite visibility
- Verify `data/trajectories.csv` exists and has valid data
- Run a Python simulation with `--export` flag first

