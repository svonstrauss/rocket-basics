"""
Trajectory Exporter
Shared utility for exporting simulation data to the OpenGL Earth Viewer.

This module provides functions to convert simulation output from any of our
orbital mechanics projects into the CSV format expected by the EarthViewer.
"""

import os
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Earth radius in meters (WGS84)
R_EARTH = 6378137.0

@dataclass
class TrajectoryPoint:
    """A single point in a trajectory."""
    name: str
    x: float  # Normalized to Earth radii
    y: float
    z: float
    r: float  # Color (0-1)
    g: float
    b: float

def normalize_position(x_m: float, y_m: float, z_m: float) -> Tuple[float, float, float]:
    """
    Converts position from meters to normalized Earth radii.
    The OpenGL viewer expects positions where Earth radius = 1.0.
    """
    return (x_m / R_EARTH, y_m / R_EARTH, z_m / R_EARTH)

def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Converts hex color string to RGB floats (0-1)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def export_trajectories(
    trajectories: Dict[str, Dict],
    output_path: str,
    colors: Dict[str, str] = None
) -> str:
    """
    Exports trajectory data to CSV format for the OpenGL Earth Viewer.
    
    Parameters
    ----------
    trajectories : dict
        Dictionary mapping satellite names to their position history.
        Each value should be a dict with 'x', 'y', 'z' lists (in meters).
    output_path : str
        Path to write the CSV file.
    colors : dict, optional
        Dictionary mapping satellite names to hex color strings.
        
    Returns
    -------
    str
        Path to the exported file.
    """
    # Default colors if not provided
    default_colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00', '#ff6b6b', '#4ecdc4']
    
    with open(output_path, 'w') as f:
        # Write header
        f.write("name,x,y,z,r,g,b\n")
        
        for i, (name, data) in enumerate(trajectories.items()):
            # Get color
            if colors and name in colors:
                r, g, b = hex_to_rgb(colors[name])
            else:
                r, g, b = hex_to_rgb(default_colors[i % len(default_colors)])
            
            # Write each position
            x_list = data['x']
            y_list = data['y']
            z_list = data['z']
            
            for x_m, y_m, z_m in zip(x_list, y_list, z_list):
                # Convert from meters to normalized Earth radii
                x, y, z = normalize_position(x_m * 1000, y_m * 1000, z_m * 1000)  # km to m
                f.write(f"{name},{x:.6f},{y:.6f},{z:.6f},{r:.3f},{g:.3f},{b:.3f}\n")
    
    print(f"Exported {len(trajectories)} trajectories to {output_path}")
    return output_path

def get_viewer_data_path() -> str:
    """Returns the path to the EarthViewer data directory."""
    # Navigate from this file to the EarthViewer data folder
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_dir, "EarthViewer", "data", "trajectories.csv")

# ============================================================================
# Integration with specific simulations
# ============================================================================

def export_from_starlink_propagator(viz, output_path: str = None) -> str:
    """
    Exports trajectory data from a ConstellationVisualizer instance.
    
    Parameters
    ----------
    viz : ConstellationVisualizer
        The visualizer instance after running simulate().
    output_path : str, optional
        Output path. Defaults to EarthViewer data directory.
        
    Returns
    -------
    str
        Path to exported file.
    """
    if output_path is None:
        output_path = get_viewer_data_path()
    
    # Build color map from satellite objects
    colors = {}
    for sat in viz.satellites:
        colors[sat.name] = sat.color
    
    return export_trajectories(viz.history, output_path, colors)

def export_from_constellation_designer(designer, output_path: str = None) -> str:
    """
    Exports trajectory data from a ConstellationDesigner instance.
    
    Parameters
    ----------
    designer : ConstellationDesigner
        The designer instance after generating constellation data.
    output_path : str, optional
        Output path. Defaults to EarthViewer data directory.
        
    Returns
    -------
    str
        Path to exported file.
    """
    if output_path is None:
        output_path = get_viewer_data_path()
    
    # Generate data if not already done
    data = designer.generate_constellation_data(n_frames=200)
    
    trajectories = {}
    colors = {}
    
    for shell in designer.shells:
        shell_d = data[shell.name]
        
        for p_idx, (px, py, pz) in enumerate(shell_d['sats']):
            for s_idx in range(len(px)):
                sat_name = f"{shell.name}_P{p_idx}_S{s_idx}"
                
                # Convert from km to the format expected (which will be normalized)
                trajectories[sat_name] = {
                    'x': [px[s_idx][f] / 1000 for f in range(len(px[s_idx]))],  # km
                    'y': [py[s_idx][f] / 1000 for f in range(len(py[s_idx]))],
                    'z': [pz[s_idx][f] / 1000 for f in range(len(pz[s_idx]))]
                }
                colors[sat_name] = shell.color
    
    return export_trajectories(trajectories, output_path, colors)

# ============================================================================
# Demo / Test
# ============================================================================

if __name__ == "__main__":
    print("Trajectory Exporter - Demo")
    print("=" * 40)
    
    # Create sample trajectory data
    t = np.linspace(0, 2 * np.pi, 100)
    
    # Sample orbit at 550 km altitude
    altitude = 550  # km
    r = R_EARTH / 1000 + altitude  # km
    
    demo_trajectories = {
        "Demo-Sat-1": {
            'x': list(r * np.cos(t)),
            'y': list(r * np.sin(t)),
            'z': list(np.zeros_like(t))
        },
        "Demo-Sat-2": {
            'x': list(r * np.cos(t + np.pi/2)),
            'y': list(r * np.sin(t + np.pi/2) * np.cos(np.radians(53))),
            'z': list(r * np.sin(t + np.pi/2) * np.sin(np.radians(53)))
        }
    }
    
    output = export_trajectories(
        demo_trajectories,
        get_viewer_data_path(),
        colors={"Demo-Sat-1": "#00ffff", "Demo-Sat-2": "#ff00ff"}
    )
    
    print(f"Demo data exported to: {output}")
    print("\nTo view, build and run the EarthViewer:")
    print("  cd src/shared/EarthViewer")
    print("  cmake -B build -DCMAKE_BUILD_TYPE=Release")
    print("  cmake --build build --config Release")
    print("  build/Release/earth.exe")

