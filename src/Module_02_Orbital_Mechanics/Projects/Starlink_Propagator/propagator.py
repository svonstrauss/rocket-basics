"""
Starlink Orbit Propagator
Module 2: Orbital Mechanics and Mission Design
Project 1

A tool to propagate satellite orbits using J2 perturbation physics (Earth oblateness).
Visualizes the constellation coverage and orbital planes with high-fidelity graphics.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import os

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
G = 6.67430e-11           # Gravitational Constant
M_EARTH = 5.972e24        # Mass of Earth (kg)
R_EARTH = 6378137.0       # Radius of Earth (Equatorial) (m) - WGS84
J2 = 1.08263e-3           # Earth's J2 Coefficient (Oblateness)
MU = G * M_EARTH          # Standard Gravitational Parameter

# Texture Path
TEXTURE_PATH = "earth_texture.jpg"

@dataclass
class Satellite:
    name: str
    # Classical Orbital Elements (COEs)
    a: float        # Semi-major axis (m)
    e: float        # Eccentricity
    i: float        # Inclination (rad)
    raan: float     # Right Ascension of Ascending Node (rad)
    arg_p: float    # Argument of Perigee (rad)
    nu: float       # True Anomaly (rad) - Current position
    
    color: str = 'white'

class Propagator:
    """
    Propagates orbits considering J2 perturbations.
    J2 effect causes RAAN precession (nodal regression) and Argument of Perigee rotation.
    """
    
    @staticmethod
    def j2_rates(a: float, e: float, i: float) -> tuple:
        """
        Calculates secular J2 perturbation rates (rad/s).
        Returns: (raan_dot, arg_p_dot)
        """
        p = a * (1 - e**2) # Semi-latus rectum
        n = np.sqrt(MU / a**3) # Mean motion
        
        # Nodal Regression (RAAN dot)
        raan_dot = -1.5 * n * J2 * (R_EARTH / p)**2 * np.cos(i)
        
        # Apsidal Rotation (Arg Perigee dot)
        arg_p_dot = 0.75 * n * J2 * (R_EARTH / p)**2 * (4 - 5 * np.sin(i)**2)
        
        return raan_dot, arg_p_dot

    @staticmethod
    def coe_to_rv(a, e, i, raan, arg_p, nu):
        """
        Converts Classical Orbital Elements to State Vector (Position, Velocity) in ECI frame.
        """
        # 1. Position in Perifocal Frame (PQW)
        r_mag = a * (1 - e**2) / (1 + e * np.cos(nu))
        
        r_pqw = np.array([
            r_mag * np.cos(nu),
            r_mag * np.sin(nu),
            0
        ])
        
        # 2. Rotation Matrix (Perifocal -> ECI)
        cO, sO = np.cos(raan), np.sin(raan)
        ci, si = np.cos(i), np.sin(i)
        cw, sw = np.cos(arg_p), np.sin(arg_p)
        
        R = np.array([
            [cO*cw - sO*ci*sw, -cO*sw - sO*ci*cw,  sO*si],
            [sO*cw + cO*ci*sw, -sO*sw + cO*ci*cw, -cO*si],
            [si*sw,             si*cw,             ci]
        ])
        
        r_eci = R @ r_pqw
        return r_eci

class ConstellationVisualizer:
    def __init__(self, satellites: list[Satellite]):
        self.satellites = satellites
        self.history = {sat.name: {'x': [], 'y': [], 'z': []} for sat in satellites}
        self.dt = 10.0 # Default, updated in simulate
        
    def simulate(self, duration: float, dt: float):
        """Run the simulation loop."""
        self.dt = dt
        steps = int(duration / dt)
        print(f"Simulating {len(self.satellites)} satellites for {duration/3600:.1f} hours...")
        
        for step in range(steps):
            time = step * dt
            
            for sat in self.satellites:
                # 1. Calculate Perturbation Rates
                raan_dot, arg_p_dot = Propagator.j2_rates(sat.a, sat.e, sat.i)
                
                # 2. Update Orbital Elements
                current_raan = sat.raan + raan_dot * time
                current_arg_p = sat.arg_p + arg_p_dot * time
                
                # Update True Anomaly (Mean Motion approximation)
                n = np.sqrt(MU / sat.a**3)
                current_nu = sat.nu + n * time
                
                # 3. Convert to Cartesian ECI
                r_eci = Propagator.coe_to_rv(sat.a, sat.e, sat.i, current_raan, current_arg_p, current_nu)
                
                # Store
                self.history[sat.name]['x'].append(r_eci[0] / 1000.0) # km
                self.history[sat.name]['y'].append(r_eci[1] / 1000.0)
                self.history[sat.name]['z'].append(r_eci[2] / 1000.0)

    def animate(self):
        """Create 3D Animation."""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Background color
        fig.patch.set_facecolor('#0b0b10')
        ax.set_facecolor('#0b0b10')
        
        # --- Draw Earth with Texture ---
        # Create sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x_earth = (R_EARTH/1000) * np.outer(np.cos(u), np.sin(v))
        y_earth = (R_EARTH/1000) * np.outer(np.sin(u), np.sin(v))
        z_earth = (R_EARTH/1000) * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Try to load texture
        texture_loaded = False
        if os.path.exists(TEXTURE_PATH):
            try:
                img = plt.imread(TEXTURE_PATH)
                # Map the image to the sphere surface
                # This is computationally expensive but looks great
                from matplotlib import cm
                
                # Normalize u,v to 0..1 for image sampling
                # u is 0..2pi, v is 0..pi
                # We need to flip/rotate to align correctly with ECI typically
                # Simple mapping:
                color_map = img / 255.0
                
                # Create a mapping function
                # We need to sample the image at coordinates corresponding to the meshgrid
                # Image dimensions
                H, W, _ = color_map.shape
                
                # Map u,v indices to image pixels
                # u corresponds to longitude (width), v to latitude (height)
                # u goes 0->2pi (0->W), v goes 0->pi (0->H)
                
                # We need arrays of pixel indices
                x_idx = np.array((u / (2*np.pi)) * (W-1), dtype=int)
                y_idx = np.array((v / np.pi) * (H-1), dtype=int)
                
                # We need to broadcast these to the meshgrid shape
                # outer product logic was used for x,y,z
                # x_idx varies along axis 0 of meshgrid? No, np.outer(cos(u), sin(v))
                # Result shape is (len(u), len(v)) = (100, 100)
                # Row index corresponds to u, Column index to v
                
                # Construct facecolors array
                facecolors = np.zeros((len(u), len(v), 3))
                for i in range(len(u)):
                    for j in range(len(v)):
                        # Simple mapping
                        # v[j] is latitude (0 is North Pole, pi is South) -> Image row 0 is Top
                        # u[i] is longitude -> Image col
                        r = min(y_idx[j], H-1)
                        c = min(x_idx[i], W-1)
                        # We might need to flip u to match rotation direction
                        facecolors[i, j] = color_map[r, -c] 
                
                ax.plot_surface(x_earth, y_earth, z_earth, facecolors=facecolors, rstride=2, cstride=2, shade=False)
                texture_loaded = True
                print("Texture loaded successfully.")
            except Exception as e:
                print(f"Texture loading failed: {e}")
        
        if not texture_loaded:
            # Fallback to stylized wireframe Earth
            ax.plot_surface(x_earth, y_earth, z_earth, color='#1f77b4', alpha=0.2, rstride=5, cstride=5)
            ax.plot_wireframe(x_earth, y_earth, z_earth, color='#4a90e2', alpha=0.3, rstride=10, cstride=10)

        # --- Plot Orbits ---
        lines = []
        markers = []
        
        for sat in self.satellites:
            # Brighter lines, better alpha
            line, = ax.plot([], [], [], color=sat.color, lw=2, alpha=0.7)
            # White marker with colored edge
            marker, = ax.plot([], [], [], marker='o', color='white', markeredgecolor=sat.color, markersize=5)
            lines.append(line)
            markers.append(marker)
            
        # --- Styling ---
        limit = (R_EARTH/1000) + 1500 # Tight zoom on LEO
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        # Hide panes
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # Dim grid
        ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.15)
        ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.15)
        ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.15)
        
        # Styled Axis Labels
        ax.set_xlabel("X (km)", color='gray')
        ax.set_ylabel("Y (km)", color='gray')
        ax.set_zlabel("Z (km)", color='gray')
        ax.tick_params(axis='x', colors='gray', labelsize=8)
        ax.tick_params(axis='y', colors='gray', labelsize=8)
        ax.tick_params(axis='z', colors='gray', labelsize=8)
        
        # HUD Text overlay
        # We use text2D to place text in screen coordinates (fixed position)
        time_text = ax.text2D(0.05, 0.95, "T+ 00h 00m", transform=ax.transAxes, color='white', fontsize=12, family='monospace')
        
        # Constellation Stats
        stats_text = (f"Constellation: Starlink (Shell 1)\n"
                      f"Satellites: {len(self.satellites)}\n"
                      f"Altitude: {(self.satellites[0].a - R_EARTH)/1000:.0f} km\n"
                      f"Inclination: {np.degrees(self.satellites[0].i):.1f}°")
        ax.text2D(0.05, 0.85, stats_text, transform=ax.transAxes, color='cyan', fontsize=9, family='monospace')

        # Equatorial Plane visual helper (faint ring)
        theta_ring = np.linspace(0, 2*np.pi, 100)
        r_ring = (R_EARTH/1000) + 2000
        x_ring = r_ring * np.cos(theta_ring)
        y_ring = r_ring * np.sin(theta_ring)
        z_ring = np.zeros_like(x_ring)
        ax.plot(x_ring, y_ring, z_ring, color='white', alpha=0.1, linestyle='--', lw=0.5)

        ax.set_title("Starlink LEO Constellation\nJ2 Nodal Regression", color='white', pad=10)
        
        # Set viewing angle
        ax.view_init(elev=30, azim=45)

        def update(frame):
            idx = frame * 10  # Speed up
            if idx >= len(self.history[self.satellites[0].name]['x']):
                idx = len(self.history[self.satellites[0].name]['x']) - 1
            
            # Update HUD Time
            # Use stored dt for accurate time calculation
            sim_time_s = idx * self.dt
            hours = int(sim_time_s // 3600)
            mins = int((sim_time_s % 3600) // 60)
            time_text.set_text(f"T+ {hours:02d}h {mins:02d}m")

            for i, sat in enumerate(self.satellites):
                hist = self.history[sat.name]
                
                # Longer trail for better visual of the orbital ring
                trail_len = 300 
                start = max(0, idx - trail_len)
                
                lines[i].set_data(hist['x'][start:idx], hist['y'][start:idx])
                lines[i].set_3d_properties(hist['z'][start:idx])
                
                markers[i].set_data([hist['x'][idx]], [hist['y'][idx]])
                markers[i].set_3d_properties([hist['z'][idx]])
                
            return lines + markers

        # Reduced frames for performance
        frames = len(self.history[self.satellites[0].name]['x']) // 10
        anim = animation.FuncAnimation(fig, update, frames=frames, interval=30, blit=False)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Starlink Parameters
    altitude = 550000 # m
    a_starlink = R_EARTH + altitude
    inc_starlink = np.radians(53.0)
    
    sats = []
    
    # 3 orbital planes
    for plane_num in range(3):
        # 30 degree RAAN separation for visual clarity
        raan = np.radians(plane_num * 30) 
        # High contrast colors
        color = ['#00ffff', '#ff00ff', '#ffff00'][plane_num]
        
        # 6 sats per plane to fill the ring better visually
        for sat_num in range(6):
            nu = np.radians(sat_num * 60) 
            
            sats.append(Satellite(
                name=f"Sat-{plane_num}-{sat_num}",
                a=a_starlink,
                e=0.0, 
                i=inc_starlink,
                raan=raan,
                arg_p=0.0,
                nu=nu,
                color=color
            ))
            
    viz = ConstellationVisualizer(sats)
    viz.simulate(duration=3*3600, dt=10.0) 
    viz.animate()
