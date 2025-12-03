"""
Constellation Designer
Module 3: Space Systems & Propulsion Engineering

Design and visualize satellite constellations for global coverage.
Includes real Walker Delta notation and coverage analysis with sensor cones.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from dataclasses import dataclass
from typing import List

R_EARTH = 6371.0  # km

# Comprehensive constellation data from global space agencies
CONSTELLATION_DATA = {
    # USA
    'gps': {'name': 'GPS', 'operator': 'US Space Force', 'country': 'USA',
            'altitude': 20200, 'inclination': 55, 'planes': 6, 'sats_per_plane': 4,
            'purpose': 'Navigation', 'first_launch': 1978},
    'starlink': {'name': 'Starlink', 'operator': 'SpaceX', 'country': 'USA',
                 'altitude': 550, 'inclination': 53, 'planes': 72, 'sats_per_plane': 22,
                 'purpose': 'Internet', 'first_launch': 2019},
    'iridium': {'name': 'Iridium NEXT', 'operator': 'Iridium', 'country': 'USA',
                'altitude': 780, 'inclination': 86.4, 'planes': 6, 'sats_per_plane': 11,
                'purpose': 'Satellite Phone', 'first_launch': 2017},
    # Russia
    'glonass': {'name': 'GLONASS', 'operator': 'Roscosmos', 'country': 'Russia',
                'altitude': 19130, 'inclination': 64.8, 'planes': 3, 'sats_per_plane': 8,
                'purpose': 'Navigation', 'first_launch': 1982},
    # Europe
    'galileo': {'name': 'Galileo', 'operator': 'ESA/EU', 'country': 'Europe',
                'altitude': 23222, 'inclination': 56, 'planes': 3, 'sats_per_plane': 10,
                'purpose': 'Navigation', 'first_launch': 2011},
    'oneweb': {'name': 'OneWeb', 'operator': 'OneWeb', 'country': 'UK',
               'altitude': 1200, 'inclination': 87.9, 'planes': 18, 'sats_per_plane': 36,
               'purpose': 'Internet', 'first_launch': 2019},
    # China
    'beidou': {'name': 'BeiDou-3', 'operator': 'CNSA', 'country': 'China',
               'altitude': 21528, 'inclination': 55, 'planes': 3, 'sats_per_plane': 8,
               'purpose': 'Navigation', 'first_launch': 2000},
    # Japan
    'qzss': {'name': 'QZSS (Michibiki)', 'operator': 'JAXA', 'country': 'Japan',
             'altitude': 32000, 'inclination': 43, 'planes': 1, 'sats_per_plane': 4,
             'purpose': 'Regional Nav', 'first_launch': 2010},
    # India
    'irnss': {'name': 'NavIC (IRNSS)', 'operator': 'ISRO', 'country': 'India',
              'altitude': 36000, 'inclination': 29, 'planes': 1, 'sats_per_plane': 7,
              'purpose': 'Regional Nav', 'first_launch': 2013},
}


def style_axis_scifi(ax, is_3d=False):
    """Apply dark theme styling for constellation visualization."""
    ax.set_facecolor('#060d18')
    
    if is_3d:
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.yaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.zaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.axis('off')


def create_cone(radius, height, resolution=20):
    """Create cone coordinates for sensor visualization."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    r = np.linspace(0, radius, resolution)
    theta_grid, r_grid = np.meshgrid(theta, r)
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    z = -r_grid * (height / radius)
    return x, y, z


@dataclass
class OrbitalShell:
    """Defines a shell of satellites."""
    name: str
    altitude: float
    inclination: float
    planes: int
    sats_per_plane: int
    color: str
    fov_deg: float = 45.0  # Sensor field of view


class ConstellationDesigner:
    """Interactive constellation visualization tool."""
    
    def __init__(self):
        self.shells: List[OrbitalShell] = []
        self.current_view = 0
        
    def add_shell(self, shell: OrbitalShell):
        self.shells.append(shell)
        
    def _generate_data(self, n_frames: int = 200):
        """Generate constellation position data."""
        data = {}
        
        for shell in self.shells:
            shell_data = {'orbits': [], 'sats': []}
            r = R_EARTH + shell.altitude
            inc_rad = np.deg2rad(shell.inclination)
            
            for p in range(shell.planes):
                raan = (2 * np.pi / shell.planes) * p
                
                # Orbit path
                theta = np.linspace(0, 2 * np.pi, 100)
                x_orb = r * np.cos(theta)
                y_orb = r * np.sin(theta)
                
                y_inc = y_orb * np.cos(inc_rad)
                z_inc = y_orb * np.sin(inc_rad)
                
                x_final = x_orb * np.cos(raan) - y_inc * np.sin(raan)
                y_final = x_orb * np.sin(raan) + y_inc * np.cos(raan)
                z_final = z_inc
                
                shell_data['orbits'].append((x_final, y_final, z_final))
                
                # Satellite positions
                sat_sep = 2 * np.pi / shell.sats_per_plane
                phase_offset = (2 * np.pi / shell.planes) * p * 0.5
                t_sim = np.linspace(0, 2 * np.pi, n_frames)
                
                plane_x, plane_y, plane_z = [], [], []
                
                for s in range(shell.sats_per_plane):
                    M = t_sim + (s * sat_sep) + phase_offset
                    xs = r * np.cos(M)
                    ys = r * np.sin(M)
                    
                    ys_inc = ys * np.cos(inc_rad)
                    zs_inc = ys * np.sin(inc_rad)
                    
                    xs_f = xs * np.cos(raan) - ys_inc * np.sin(raan)
                    ys_f = xs * np.sin(raan) + ys_inc * np.cos(raan)
                    zs_f = zs_inc
                    
                    plane_x.append(xs_f)
                    plane_y.append(ys_f)
                    plane_z.append(zs_f)
                
                shell_data['sats'].append((plane_x, plane_y, plane_z))
            
            data[shell.name] = shell_data
        
        return data
    
    def animate(self):
        """Create the visualization dashboard."""
        n_frames = 200
        self.data = self._generate_data(n_frames)
        
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050a12')
        
        # Title
        self.fig.text(0.5, 0.97, "◢ CONSTELLATION DESIGNER ◣",
                     fontsize=20, fontweight='bold', color='#00d4ff', ha='center',
                     fontfamily='monospace')
        self.fig.text(0.5, 0.935, "GPS • Galileo • GLONASS • Starlink Architecture Analysis",
                     fontsize=11, color='#7fdbff', ha='center', fontfamily='monospace')
        
        # 3D plot
        self.ax_3d = self.fig.add_axes([0.02, 0.10, 0.62, 0.80], projection='3d')
        style_axis_scifi(self.ax_3d, is_3d=True)
        
        # Earth
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x_e = R_EARTH * np.outer(np.cos(u), np.sin(v))
        y_e = R_EARTH * np.outer(np.sin(u), np.sin(v))
        z_e = R_EARTH * np.outer(np.ones(len(u)), np.cos(v))
        
        self.ax_3d.plot_surface(x_e, y_e, z_e, color='#1a4a6e', alpha=0.5, rstride=3, cstride=3)
        self.ax_3d.plot_wireframe(x_e, y_e, z_e, color='#00d4ff', alpha=0.2, rstride=8, cstride=8, lw=0.5)
        
        # Initialize plots
        self.scatter_proxies = {}
        self.orbit_lines = []
        
        for shell in self.shells:
            sd = self.data[shell.name]
            
            for ox, oy, oz in sd['orbits']:
                line, = self.ax_3d.plot(ox, oy, oz, color=shell.color, ls='-', lw=0.8, alpha=0.4)
                self.orbit_lines.append(line)
            
            scat = self.ax_3d.scatter([], [], [], color=shell.color, s=40,
                                      edgecolor='white', alpha=0.9, label=shell.name)
            self.scatter_proxies[shell.name] = scat
        
        # Sensor cone
        self.cone_plot = [None]
        first_shell = self.shells[0]
        cone_radius = first_shell.altitude * np.tan(np.deg2rad(first_shell.fov_deg))
        cone_height = first_shell.altitude
        self.cone_x, self.cone_y, self.cone_z = create_cone(cone_radius, cone_height)
        self.cone_flat = np.vstack([self.cone_x.ravel(), self.cone_y.ravel(), self.cone_z.ravel()])
        
        limit = R_EARTH + max(s.altitude for s in self.shells) + 500
        self.ax_3d.set_xlim(-limit, limit)
        self.ax_3d.set_ylim(-limit, limit)
        self.ax_3d.set_zlim(-limit, limit)
        self.ax_3d.view_init(elev=20, azim=45)
        
        # Info panel
        self.ax_info = self.fig.add_axes([0.66, 0.10, 0.32, 0.80])
        self.ax_info.set_facecolor('#050a12')
        self.ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=self.ax_info.transAxes)
        self.ax_info.add_patch(panel)
        
        self.ax_info.text(0.5, 0.97, "◢ CONSTELLATION DATA ◣", transform=self.ax_info.transAxes,
                         fontsize=12, fontweight='bold', color='#00d4ff', ha='center',
                         fontfamily='monospace')
        
        # Time display
        self.time_txt = self.ax_info.text(0.5, 0.91, "T+ 00h 00m", transform=self.ax_info.transAxes,
                                         fontsize=14, color='#ffd700', ha='center', fontweight='bold',
                                         fontfamily='monospace')
        
        # Shell info
        y_pos = 0.84
        colors = ['#00d4ff', '#ff6b35', '#00ff9f', '#ffd700']
        
        for i, shell in enumerate(self.shells):
            col = colors[i % len(colors)]
            self.ax_info.text(0.08, y_pos, f"► {shell.name.upper()}", transform=self.ax_info.transAxes,
                             fontsize=10, color=col, fontfamily='monospace', fontweight='bold')
            
            total_sats = shell.planes * shell.sats_per_plane
            walker = f"{shell.inclination}°: {total_sats}/{shell.planes}/1"
            
            info = f"Alt: {shell.altitude} km | Inc: {shell.inclination}°\n"
            info += f"Planes: {shell.planes} | Sats/Plane: {shell.sats_per_plane}\n"
            info += f"Walker: {walker} | FOV: {shell.fov_deg}°"
            
            self.ax_info.text(0.10, y_pos - 0.06, info, transform=self.ax_info.transAxes,
                             fontsize=8, color='#ffffff', fontfamily='monospace')
            y_pos -= 0.18
        
        # Total stats
        div = Line2D([0.05, 0.95], [0.32, 0.32], color='#00d4ff', alpha=0.3, lw=1,
                    transform=self.ax_info.transAxes)
        self.ax_info.add_line(div)
        
        self.ax_info.text(0.5, 0.28, "◢ SYSTEM TOTALS ◣", transform=self.ax_info.transAxes,
                         fontsize=10, fontweight='bold', color='#ff6b35', ha='center',
                         fontfamily='monospace')
        
        total_sats = sum(s.planes * s.sats_per_plane for s in self.shells)
        total_planes = sum(s.planes for s in self.shells)
        
        stats = [
            ("TOTAL SATELLITES", f"{total_sats}", "#00d4ff"),
            ("ORBITAL PLANES", f"{total_planes}", "#ff6b35"),
            ("SHELLS", f"{len(self.shells)}", "#00ff9f"),
        ]
        
        for i, (label, val, col) in enumerate(stats):
            y = 0.22 - i * 0.06
            self.ax_info.text(0.08, y, f"► {label}", transform=self.ax_info.transAxes,
                             fontsize=9, color=col, fontfamily='monospace')
            self.ax_info.text(0.65, y, val, transform=self.ax_info.transAxes,
                             fontsize=10, color='#ffffff', fontfamily='monospace')
        
        # Global constellations comparison
        div2 = Line2D([0.05, 0.95], [0.15, 0.15], color='#00ff9f', alpha=0.3, lw=1,
                     transform=self.ax_info.transAxes)
        self.ax_info.add_line(div2)
        
        self.ax_info.text(0.5, 0.11, "◢ REAL WORLD SYSTEMS ◣", transform=self.ax_info.transAxes,
                         fontsize=9, fontweight='bold', color='#00ff9f', ha='center',
                         fontfamily='monospace')
        
        self.ax_info.text(0.5, 0.04, "GPS(USA) • GLONASS(RUS) • Galileo(EU) • BeiDou(CHN)",
                         transform=self.ax_info.transAxes, fontsize=7, color='#7fdbff',
                         ha='center', fontfamily='monospace')
        
        def update(frame):
            total_min = frame * 2
            hours = total_min // 60
            mins = total_min % 60
            self.time_txt.set_text(f"T+ {hours:02d}h {mins:02d}m")
            
            artists = [self.time_txt]
            first_sat_pos = None
            
            for i, shell in enumerate(self.shells):
                sd = self.data[shell.name]
                scat = self.scatter_proxies[shell.name]
                
                all_x, all_y, all_z = [], [], []
                
                for p_idx, (px, py, pz) in enumerate(sd['sats']):
                    for s_idx in range(len(px)):
                        x = px[s_idx][frame]
                        y = py[s_idx][frame]
                        z = pz[s_idx][frame]
                        all_x.append(x)
                        all_y.append(y)
                        all_z.append(z)
                        
                        if i == 0 and p_idx == 0 and s_idx == 0:
                            first_sat_pos = np.array([x, y, z])
                
                scat._offsets3d = (all_x, all_y, all_z)
                artists.append(scat)
            
            # Update cone
            if self.cone_plot[0]:
                self.cone_plot[0].remove()
            
            if first_sat_pos is not None:
                sat_mag = np.linalg.norm(first_sat_pos)
                down_vec = -first_sat_pos / sat_mag
                up_vec = np.array([0, 0, 1])
                
                rot_axis = np.cross(up_vec, down_vec)
                rot_mag = np.linalg.norm(rot_axis)
                
                if rot_mag > 1e-6:
                    rot_axis /= rot_mag
                    angle = np.arccos(np.clip(np.dot(up_vec, down_vec), -1, 1))
                    K = np.array([[0, -rot_axis[2], rot_axis[1]],
                                  [rot_axis[2], 0, -rot_axis[0]],
                                  [-rot_axis[1], rot_axis[0], 0]])
                    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
                    rotated = R @ self.cone_flat
                else:
                    rotated = self.cone_flat
                
                X = rotated[0].reshape(self.cone_x.shape) + first_sat_pos[0]
                Y = rotated[1].reshape(self.cone_y.shape) + first_sat_pos[1]
                Z = rotated[2].reshape(self.cone_z.shape) + first_sat_pos[2]
                
                self.cone_plot[0] = self.ax_3d.plot_surface(X, Y, Z, color='#ffd700', alpha=0.25)
                artists.append(self.cone_plot[0])
            
            return artists
        
        self.anim = FuncAnimation(self.fig, update, frames=n_frames, interval=50, blit=False)
        plt.show()


def run_demo():
    print("=" * 60)
    print("CONSTELLATION DESIGNER")
    print("Module 3: Space Systems Engineering")
    print("Based on: GPS • Galileo • GLONASS • Starlink • Iridium")
    print("=" * 60)
    print("\nDesigning multi-shell satellite constellation...")
    print("-" * 60)
    
    designer = ConstellationDesigner()
    
    # LEO Communications (like Starlink/OneWeb/Iridium)
    designer.add_shell(OrbitalShell(
        name="LEO Comms",
        altitude=550,
        inclination=53,
        planes=12,
        sats_per_plane=5,
        color='#00d4ff',
        fov_deg=45
    ))
    
    # Polar Earth Observation (like Landsat/Sentinel)
    designer.add_shell(OrbitalShell(
        name="Polar EO",
        altitude=700,
        inclination=98,
        planes=4,
        sats_per_plane=6,
        color='#ff6b35',
        fov_deg=40
    ))
    
    # MEO Navigation (like GPS/Galileo/GLONASS)
    designer.add_shell(OrbitalShell(
        name="MEO Nav",
        altitude=20200,
        inclination=55,
        planes=6,
        sats_per_plane=4,
        color='#00ff9f',
        fov_deg=25
    ))
    
    designer.animate()


if __name__ == "__main__":
    run_demo()
