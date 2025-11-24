"""
Constellation Designer
Module 3: Space Systems & Propulsion Engineering
Project 2

A tool to design and visualize satellite constellations (like Starlink or GPS)
for global coverage analysis. Features a high-fidelity animated 3D globe with sensor cones.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import List

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
R_EARTH = 6371.0  # km

def create_cone(radius, height, resolution=20):
    """Helper function to create cone coordinates."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    r = np.linspace(0, radius, resolution)
    theta_grid, r_grid = np.meshgrid(theta, r)
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    z = -r_grid * (height / radius) # Cone points "down"
    return x, y, z

@dataclass
class OrbitalShell:
    """Defines a shell of satellites at a specific altitude and inclination."""
    name: str
    altitude: float     # km
    inclination: float  # degrees
    planes: int         # Number of orbital planes
    sats_per_plane: int # Satellites per plane
    color: str          # Plot color
    marker: str = 'o'   # Plot marker style

class ConstellationDesigner:
    def __init__(self):
        self.shells: List[OrbitalShell] = []
        
    def add_shell(self, shell: OrbitalShell):
        self.shells.append(shell)
        
    def generate_constellation_data(self, n_frames: int = 200) -> dict:
        """
        Generates position data for all satellites across all frames.
        Returns a dictionary structure for plotting.
        """
        data = {}
        
        for shell in self.shells:
            shell_data = {
                'orbits': [], # Static orbit lines (x, y, z)
                'sats': []    # Animated sat positions (frame -> x, y, z)
            }
            
            r = R_EARTH + shell.altitude
            inc_rad = np.deg2rad(shell.inclination)
            
            # Generate Planes
            for p in range(shell.planes):
                raan = (2 * np.pi / shell.planes) * p
                
                # --- 1. Static Orbit Path ---
                theta_orbit = np.linspace(0, 2 * np.pi, 100)
                # Orbital plane coordinates
                x_orb = r * np.cos(theta_orbit)
                y_orb = r * np.sin(theta_orbit)
                z_orb = np.zeros_like(x_orb)
                
                # Rotate by Inclination (around X-axis)
                y_inc = y_orb * np.cos(inc_rad)
                z_inc = y_orb * np.sin(inc_rad)
                
                # Rotate by RAAN (around Z-axis)
                x_final = x_orb * np.cos(raan) - y_inc * np.sin(raan)
                y_final = x_orb * np.sin(raan) + y_inc * np.cos(raan)
                z_final = z_inc
                
                shell_data['orbits'].append((x_final, y_final, z_final))
                
                # --- 2. Animated Satellite Positions ---
                sat_phase_sep = 2 * np.pi / shell.sats_per_plane
                plane_phase_offset = (2 * np.pi / shell.planes) * p * 0.5 
                
                t_sim = np.linspace(0, 2*np.pi, n_frames) 
                
                plane_sats_x = []
                plane_sats_y = []
                plane_sats_z = []
                
                for s in range(shell.sats_per_plane):
                    M = t_sim + (s * sat_phase_sep) + plane_phase_offset
                    xs = r * np.cos(M)
                    ys = r * np.sin(M)
                    
                    ys_inc = ys * np.cos(inc_rad)
                    zs_inc = ys * np.sin(inc_rad)
                    
                    xs_final = xs * np.cos(raan) - ys_inc * np.sin(raan)
                    ys_final = xs * np.sin(raan) + ys_inc * np.cos(raan)
                    zs_final = zs_inc
                    
                    plane_sats_x.append(xs_final)
                    plane_sats_y.append(ys_final)
                    plane_sats_z.append(zs_final)
                
                shell_data['sats'].append((plane_sats_x, plane_sats_y, plane_sats_z))
            
            data[shell.name] = shell_data
            
        return data

    def animate(self):
        """Generates the high-fidelity 3D animation with sensor cones."""
        n_frames = 200
        data = self.generate_constellation_data(n_frames)
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set background color (Dark Teal/Space)
        fig.patch.set_facecolor('#1a2e2a')
        ax.set_facecolor('#1a2e2a')
        
        # --- Plot Earth (Wireframe Style) ---
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 60)
        x_earth = R_EARTH * np.outer(np.cos(u), np.sin(v))
        y_earth = R_EARTH * np.outer(np.sin(u), np.sin(v))
        z_earth = R_EARTH * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_earth, y_earth, z_earth, color='#50e3c2', rstride=3, cstride=3, alpha=0.1, shade=False)
        ax.plot_wireframe(x_earth, y_earth, z_earth, color='#50e3c2', rstride=6, cstride=6, alpha=0.3, linewidth=0.5)
        
        # --- Initialize Plots ---
        scatter_proxies = {} 
        cone_plot = [None] # Mutable container for the cone surface
        
        for shell in self.shells:
            shell_d = data[shell.name]
            # Plot Static Orbits
            for (ox, oy, oz) in shell_d['orbits']:
                ax.plot(ox, oy, oz, color=shell.color, linestyle='-', linewidth=0.8, alpha=0.4)
            # Create scatters
            scat = ax.scatter([], [], [], color=shell.color, marker=shell.marker, s=30, edgecolor='white', alpha=0.9, label=shell.name)
            scatter_proxies[shell.name] = scat

        # --- Precompute Cone Geometry ---
        # We'll attach a cone to the first satellite of the first shell
        first_shell = self.shells[0]
        cone_radius = 2000 # km
        cone_height = first_shell.altitude 
        cone_x_base, cone_y_base, cone_z_base = create_cone(cone_radius, cone_height)
        cone_flat = np.vstack([cone_x_base.ravel(), cone_y_base.ravel(), cone_z_base.ravel()])

        # --- Styling ---
        limit = R_EARTH + 3000
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.1)
        ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.1)
        ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.1)
        ax.axis('off') 
        
        # Overlay Text
        ax.text2D(0.05, 0.95, "CONSTELLATION DESIGNER", transform=ax.transAxes, color='white', fontsize=16, weight='bold')
        
        stats_text = ""
        for s in self.shells:
            stats_text += f"{s.name}: {s.planes}x{s.sats_per_plane} Sats @ {s.altitude}km, {s.inclination}°\n"
        
        ax.text2D(0.05, 0.82, stats_text, transform=ax.transAxes, color='#50e3c2', fontsize=10, va='top', family='monospace',
                  bbox=dict(boxstyle='round,pad=0.3', fc='#1a2e2a', ec='gray', alpha=0.5))
        
        time_text = ax.text2D(0.05, 0.05, "", transform=ax.transAxes, color='white', fontsize=12)
        
        # --- Update Function ---
        def update(frame):
            total_minutes = frame * 2
            hours = total_minutes // 60
            minutes = total_minutes % 60
            time_text.set_text(f"Simulation Step: {frame} (T+ {hours:02d}h {minutes:02d}m)")
            
            artists = [time_text]
            
            # Update Satellites
            first_sat_pos = None # For cone attachment
            
            for i, shell in enumerate(self.shells):
                shell_d = data[shell.name]
                scat = scatter_proxies[shell.name]
                
                all_x, all_y, all_z = [], [], []
                
                for p_idx in range(len(shell_d['sats'])):
                    px, py, pz = shell_d['sats'][p_idx]
                    for s_idx in range(len(px)):
                        x_pos = px[s_idx][frame]
                        y_pos = py[s_idx][frame]
                        z_pos = pz[s_idx][frame]
                        all_x.append(x_pos)
                        all_y.append(y_pos)
                        all_z.append(z_pos)
                        
                        # Capture first sat of first shell for cone
                        if i == 0 and p_idx == 0 and s_idx == 0:
                            first_sat_pos = np.array([x_pos, y_pos, z_pos])
                
                scat._offsets3d = (all_x, all_y, all_z)
                artists.append(scat)
            
            # Update Cone
            if cone_plot[0]:
                cone_plot[0].remove()
                
            if first_sat_pos is not None:
                # Rotate cone to point to Earth center
                sat_mag = np.linalg.norm(first_sat_pos)
                down_vec = -first_sat_pos / sat_mag
                up_vec = np.array([0, 0, 1])
                
                rot_axis = np.cross(up_vec, down_vec)
                rot_axis_mag = np.linalg.norm(rot_axis)
                
                if rot_axis_mag > 1e-6:
                    rot_axis /= rot_axis_mag
                    angle = np.arccos(np.dot(up_vec, down_vec))
                    K = np.array([[0, -rot_axis[2], rot_axis[1]],
                                  [rot_axis[2], 0, -rot_axis[0]],
                                  [-rot_axis[1], rot_axis[0], 0]])
                    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
                    rotated_cone = R @ cone_flat
                else:
                    # Aligned (rarely happens exactly)
                    rotated_cone = cone_flat if np.dot(up_vec, down_vec) > 0 else -cone_flat # Approx
                
                X_cone = rotated_cone[0].reshape(cone_x_base.shape) + first_sat_pos[0]
                Y_cone = rotated_cone[1].reshape(cone_y_base.shape) + first_sat_pos[1]
                Z_cone = rotated_cone[2].reshape(cone_z_base.shape) + first_sat_pos[2]
                
                cone_plot[0] = ax.plot_surface(X_cone, Y_cone, Z_cone, color='#f5e653', alpha=0.2)
                artists.append(cone_plot[0])
                
            return artists

        anim = FuncAnimation(fig, update, frames=n_frames, interval=50, blit=False)
        ax.view_init(elev=25, azim=45)
        plt.legend(loc='upper right', facecolor='#1a2e2a', edgecolor='gray', labelcolor='white')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    designer = ConstellationDesigner()
    
    # 1. Starlink-like Shell
    designer.add_shell(OrbitalShell(
        name="Internet (V1)",
        altitude=550,
        inclination=53,
        planes=12,
        sats_per_plane=5,
        color='#f5e653',
        marker='o'
    ))
    
    # 2. Polar Shell
    designer.add_shell(OrbitalShell(
        name="Polar Obs",
        altitude=700,
        inclination=90,
        planes=4,
        sats_per_plane=8,
        color='#f565c1',
        marker='^'
    ))
    
    # 3. Equatorial Ring
    designer.add_shell(OrbitalShell(
        name="Equatorial",
        altitude=1200,
        inclination=0,
        planes=1,
        sats_per_plane=10,
        color='#50e3c2',
        marker='s'
    ))
    
    designer.animate()
