"""
Conic Orbit Visualizer
Module 1: Foundations in Math, Physics, and Computation
Project 2

A tool to calculate, classify, and visualize orbital trajectories using Keplerian elements.
Features:
- Realistic Body visualization (Earth/Moon).
- Polar physics, Cartesian plotting for easier asset management.
- Animated spacecraft trajectory.
- High-contrast dark theme for clarity.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import os

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
G = 6.67430e-11       # Gravitational Constant (m^3 kg^-1 s^-2)

@dataclass
class Body:
    name: str
    mass: float       # kg
    radius: float     # m
    texture_path: str
    color: str

# Define Celestial Bodies
EARTH = Body(
    name="Earth",
    mass=5.972e24,
    radius=6371000,
    texture_path="earth_texture.jpg",
    color='dodgerblue'
)

MOON = Body(
    name="Moon",
    mass=7.34767309e22,
    radius=1737100,
    texture_path="moon_texture.jpg",
    color='gray'
)

# --- Helper to resolve texture paths ---
def get_texture_path(filename: str) -> str:
    """Resolves texture path checking CWD and script directory."""
    if os.path.exists(filename):
        return filename
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    if os.path.exists(full_path):
        return full_path
    return filename # Return original if not found

@dataclass
class Orbit:
    """Represents a Keplerian orbit."""
    semi_major_axis: float  # a (meters). Note: For Hyperbola (e > 1), this is expected to be NEGATIVE.
    eccentricity: float     # e (dimensionless)
    central_body: Body      # Using default_factory isn't straightforward with clean dataclass syntax here without field()

    def __init__(self, semi_major_axis: float, eccentricity: float, central_body: Body = EARTH):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.central_body = central_body
    
    @property
    def orbit_type(self) -> str:
        if np.isclose(self.eccentricity, 0.0): return "Circular"
        elif 0.0 < self.eccentricity < 1.0: return "Elliptical"
        elif np.isclose(self.eccentricity, 1.0): return "Parabolic"
        else: return "Hyperbolic"
        
    @property
    def mu(self) -> float:
        return G * self.central_body.mass

class OrbitVisualizer:
    """Handles physics generation and plotting."""

    def calculate_physics(self, orbit: Orbit, points: int = 500) -> tuple:
        """
        Calculates r, theta, x, y, v arrays for the orbit.
        """
        # 1. Generate Theta Range
        if orbit.eccentricity >= 1.0:
            # Hyperbola: Limit angles to avoid asymptotes
            limit = np.arccos(-1.0 / orbit.eccentricity) - 0.2
            theta = np.linspace(-limit, limit, points)
        else:
            # Circle/Ellipse: Full revolution
            theta = np.linspace(0, 2*np.pi, points)

        # 2. Calculate Radius (Polar Equation)
        # r = a(1-e^2) / (1 + e cos theta)
        # Note: If orbit is hyperbolic (e > 1), standard physics says a < 0.
        # If a < 0, then numerator = (-a)(1 - e^2) where (1-e^2) is neg, so result is neg * neg = pos.
        # If user passed positive 'a' for hyperbola, numerator is neg, resulting in negative radius (the "other branch").
        # We will trust standard conventions here. If user passes wrong sign, we visualize what math gives (loop).
        
        numerator = orbit.semi_major_axis * (1 - orbit.eccentricity**2)
        denominator = 1 + orbit.eccentricity * np.cos(theta)
        r = numerator / denominator
        
        # 3. Velocity (Vis-Viva)
        # v = sqrt(mu * (2/r - 1/a))
        
        # Handle potential negative values in sqrt for hyperbolas near infinity due to float precision
        term = 2/r - 1/orbit.semi_major_axis
        term[term < 0] = 0 # Clamp small negative errors
        v = np.sqrt(orbit.mu * term)

        # 4. Convert to Cartesian for Plotting
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y, r, v

    def animate_orbit(self, orbit: Orbit, title_suffix: str = ""):
        """
        Creates an animated plot of the orbit using Cartesian coordinates.
        """
        x, y, r, v = self.calculate_physics(orbit)
        
        # Convert to km
        x_km = x / 1000.0
        y_km = y / 1000.0
        r_km = r / 1000.0
        R_BODY_KM = orbit.central_body.radius / 1000.0

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # --- 1. Setup Central Body Asset ---
        tex_path = get_texture_path(orbit.central_body.texture_path)
        loaded_texture = False
        
        if os.path.exists(tex_path):
            try:
                img = plt.imread(tex_path)
                extent = [-R_BODY_KM, R_BODY_KM, -R_BODY_KM, R_BODY_KM]
                ax.imshow(img, extent=extent, zorder=1)
                loaded_texture = True
            except Exception as e:
                print(f"Could not load texture {tex_path}: {e}")

        if not loaded_texture:
            # Fallback circle
            body_circle = plt.Circle((0, 0), R_BODY_KM, color=orbit.central_body.color, alpha=0.6, zorder=1)
            ax.add_patch(body_circle)

        # Add atmosphere glow for Earth only
        if orbit.central_body.name == "Earth":
             atmosphere = plt.Circle((0, 0), R_BODY_KM * 1.05, color='cyan', alpha=0.2, zorder=2)
             ax.add_patch(atmosphere)

        # --- 2. Plot Trajectory Line ---
        # Use valid points only to avoid weird lines connecting across infinity if nans exist
        mask = r > 0 # Ensure we only plot positive radii physical branch
        x_plot = x_km[mask]
        y_plot = y_km[mask]
        
        line, = ax.plot(x_plot, y_plot, color='cyan', lw=2, alpha=0.8, zorder=3, label='Trajectory')

        # --- 3. Spacecraft Marker ---
        spacecraft, = ax.plot([], [], marker='^', color='white', markersize=10, zorder=5, label='Spacecraft')

        # --- 4. Styling ---
        # Better auto-scaling for hyperbolas
        if orbit.eccentricity > 1:
             # For hyperbola, zoom in to seeing the Periapsis + some margin
             periapsis_dist_km = np.min(r_km[mask])
             limit = periapsis_dist_km * 3.0 
             ax.set_xlim(-limit, limit)
             ax.set_ylim(-limit, limit)
        else:
             max_dist = np.max(np.abs(r_km)) * 1.1
             ax.set_xlim(-max_dist, max_dist)
             ax.set_ylim(-max_dist, max_dist)
             
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Distance (km)")
        
        # Title & Stats
        periapsis_alt = (np.min(r_km[mask]) - R_BODY_KM)
        title_text = f"{orbit.central_body.name} Orbit: {orbit.orbit_type} {title_suffix}\nPeriapsis: {periapsis_alt:.1f} km | Eccentricity: {orbit.eccentricity}"
        ax.set_title(title_text, color='white', fontsize=12, pad=20)

        # --- 5. Animation Function ---
        def update(frame):
            if len(x_plot) == 0: return spacecraft,
            idx = frame % len(x_plot)
            spacecraft.set_data([x_plot[idx]], [y_plot[idx]])
            return spacecraft,

        anim = animation.FuncAnimation(fig, update, frames=len(x_plot), interval=20, blit=True)
        
        plt.legend(loc='upper right')
        print(f"Displaying animated plot for {orbit.orbit_type} around {orbit.central_body.name}...")
        plt.show()

def run_demo():
    visualizer = OrbitVisualizer()
    
    # 1. LEO (Earth)
    a_leo = EARTH.radius + 400000
    print("Visualizing LEO (Earth)...")
    visualizer.animate_orbit(Orbit(a_leo, 0.0, EARTH), "(LEO)")

    # 2. GTO (Earth)
    r_p = EARTH.radius + 200000
    r_a = EARTH.radius + 35786000
    a_gto = (r_p + r_a) / 2
    e_gto = (r_a - r_p) / (r_a + r_p)
    print("Visualizing GTO (Earth)...")
    visualizer.animate_orbit(Orbit(a_gto, e_gto, EARTH), "(GTO)")

    # 3. Hyperbolic Escape (Earth)
    # To get a valid physical hyperbola with Periapsis = 400km (Earth departure burn):
    # r_p = a(1-e). Since e=1.5 > 1, (1-e) = -0.5.
    # We need r_p = R_EARTH + 400000 (approx 6771km).
    # 6771000 = a * (-0.5)  =>  a = 6771000 / -0.5 = -13542000 meters.
    # So we pass a NEGATIVE semi-major axis.
    r_p_desired = EARTH.radius + 400000
    e_esc = 1.5
    a_esc = r_p_desired / (1 - e_esc) # Will be negative
    
    print(f"Visualizing Escape (Hyperbolic)... a={a_esc/1000:.1f} km")
    visualizer.animate_orbit(Orbit(a_esc, e_esc, EARTH), "(Interplanetary)")

    # 4. Low Lunar Orbit (Moon)
    a_llo = MOON.radius + 100000
    print("Visualizing Low Lunar Orbit (Moon)...")
    visualizer.animate_orbit(Orbit(a_llo, 0.0, MOON), "(LLO)")

if __name__ == "__main__":
    run_demo()
