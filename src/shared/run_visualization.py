#!/usr/bin/env python3
"""
Orbital Visualization Platform - Launcher Script

This script provides a unified interface to:
1. Run orbital mechanics simulations (Python)
2. Export trajectory data
3. Launch the OpenGL Earth Viewer

Usage:
    python run_visualization.py --sim starlink --export --view
    python run_visualization.py --sim constellation --export
    python run_visualization.py --view  # Just launch viewer with existing data
"""

import argparse
import subprocess
import sys
import os

# Get paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
VIEWER_DIR = os.path.join(SCRIPT_DIR, "EarthViewer")
VIEWER_EXE = os.path.join(VIEWER_DIR, "build", "Release", "earth.exe")

# Simulation paths
SIMS = {
    "starlink": os.path.join(REPO_ROOT, "src", "Module_02_Orbital_Mechanics", 
                             "Projects", "Starlink_Propagator", "propagator.py"),
    "constellation": os.path.join(REPO_ROOT, "src", "Module_03_Propulsion",
                                  "Projects", "Constellation_Designer", "designer.py"),
    "trajectory": os.path.join(REPO_ROOT, "src", "Module_02_Orbital_Mechanics",
                               "Projects", "Starship_Trajectory_Planner", "mission_planner.py"),
}

def build_viewer():
    """Build the OpenGL Earth Viewer if not already built."""
    if os.path.exists(VIEWER_EXE):
        print("Viewer already built.")
        return True
    
    print("Building OpenGL Earth Viewer...")
    print("=" * 50)
    
    # Configure
    result = subprocess.run(
        ["cmake", "-B", "build", "-DCMAKE_BUILD_TYPE=Release"],
        cwd=VIEWER_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("CMake configuration failed:")
        print(result.stderr)
        return False
    
    # Build
    result = subprocess.run(
        ["cmake", "--build", "build", "--config", "Release", "-j", "4"],
        cwd=VIEWER_DIR,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Build failed:")
        print(result.stderr)
        return False
    
    print("Build successful!")
    return True

def run_simulation(sim_name: str, export: bool = False, show_plot: bool = True):
    """Run a Python orbital mechanics simulation."""
    if sim_name not in SIMS:
        print(f"Unknown simulation: {sim_name}")
        print(f"Available: {', '.join(SIMS.keys())}")
        return False
    
    sim_path = SIMS[sim_name]
    
    if not os.path.exists(sim_path):
        print(f"Simulation file not found: {sim_path}")
        return False
    
    print(f"Running {sim_name} simulation...")
    print("=" * 50)
    
    args = [sys.executable, sim_path]
    
    if export:
        args.append("--export")
    
    if not show_plot:
        args.append("--no-plot")
    
    result = subprocess.run(args)
    return result.returncode == 0

def launch_viewer():
    """Launch the OpenGL Earth Viewer."""
    if not os.path.exists(VIEWER_EXE):
        print("Viewer not built. Building now...")
        if not build_viewer():
            return False
    
    print("Launching Earth Viewer...")
    print("=" * 50)
    
    subprocess.Popen([VIEWER_EXE], cwd=VIEWER_DIR)
    return True

def generate_demo_data():
    """Generate demo trajectory data for testing the viewer."""
    print("Generating demo trajectory data...")
    
    from trajectory_exporter import export_trajectories, get_viewer_data_path
    import numpy as np
    
    R_EARTH_KM = 6378.137
    
    # Create a sample Starlink-like constellation
    trajectories = {}
    colors = {}
    
    n_frames = 200
    t = np.linspace(0, 2 * np.pi, n_frames)
    
    # 3 planes, 6 sats each
    # Professional aerospace colors: soft white, gold, and coral
    # These provide good visibility against both day and night Earth
    plane_colors = ['#e8e8e8', '#f4a460', '#87ceeb']  # Off-white, Sandy brown, Sky blue
    
    for plane in range(3):
        raan = np.radians(plane * 40)
        inc = np.radians(53)
        altitude = 550  # km
        r = R_EARTH_KM + altitude
        
        for sat in range(6):
            phase = np.radians(sat * 60)
            name = f"Demo-P{plane}-S{sat}"
            
            # Orbital motion
            theta = t + phase
            
            # Position in orbital plane
            x_orb = r * np.cos(theta)
            y_orb = r * np.sin(theta)
            
            # Rotate by inclination
            y_inc = y_orb * np.cos(inc)
            z_inc = y_orb * np.sin(inc)
            
            # Rotate by RAAN
            x_final = x_orb * np.cos(raan) - y_inc * np.sin(raan)
            y_final = x_orb * np.sin(raan) + y_inc * np.cos(raan)
            z_final = z_inc
            
            trajectories[name] = {
                'x': list(x_final),
                'y': list(y_final),
                'z': list(z_final)
            }
            colors[name] = plane_colors[plane]
    
    output_path = get_viewer_data_path()
    export_trajectories(trajectories, output_path, colors)
    print(f"Demo data exported to: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Orbital Visualization Platform Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --demo --view           Generate demo data and launch viewer
  %(prog)s --sim starlink --export Export Starlink simulation data
  %(prog)s --view                  Launch viewer with existing data
  %(prog)s --build                 Build the OpenGL viewer
        """
    )
    
    parser.add_argument('--sim', choices=list(SIMS.keys()),
                        help='Run a specific simulation')
    parser.add_argument('--export', action='store_true',
                        help='Export trajectory data for the viewer')
    parser.add_argument('--no-plot', action='store_true',
                        help='Skip matplotlib visualization')
    parser.add_argument('--view', action='store_true',
                        help='Launch the OpenGL Earth Viewer')
    parser.add_argument('--build', action='store_true',
                        help='Build the OpenGL viewer')
    parser.add_argument('--demo', action='store_true',
                        help='Generate demo trajectory data')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Build viewer if requested
    if args.build:
        build_viewer()
    
    # Generate demo data if requested
    if args.demo:
        generate_demo_data()
    
    # Run simulation if specified
    if args.sim:
        run_simulation(args.sim, args.export, not args.no_plot)
    
    # Launch viewer if requested
    if args.view:
        launch_viewer()

if __name__ == "__main__":
    main()

