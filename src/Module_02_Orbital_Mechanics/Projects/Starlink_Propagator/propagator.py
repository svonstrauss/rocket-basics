"""
Starlink Orbit Propagator
Module 2: Orbital Mechanics and Mission Design

Propagates satellite orbits with J2 perturbation physics.
Visualizes constellation coverage with real Starlink parameters.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
from dataclasses import dataclass

# --- Constants (WGS84 / EGM96) ---
G = 6.67430e-11
M_EARTH = 5.972e24
R_EARTH = 6378137.0
J2 = 1.08263e-3
MU = G * M_EARTH
OMEGA_EARTH = 7.2921159e-5

# Global constellation data from multiple space agencies
CONSTELLATION_DATABASE = {
    'starlink': {
        'name': 'Starlink', 'operator': 'SpaceX', 'country': 'USA',
        'alt_km': 550, 'inc_deg': 53.0, 'total_sats': 5000, 'status': 'Operational',
        'purpose': 'Broadband Internet', 'mass_kg': 260,
    },
    'oneweb': {
        'name': 'OneWeb', 'operator': 'OneWeb', 'country': 'UK',
        'alt_km': 1200, 'inc_deg': 87.9, 'total_sats': 648, 'status': 'Operational',
        'purpose': 'Broadband Internet', 'mass_kg': 150,
    },
    'gps': {
        'name': 'GPS', 'operator': 'US Space Force', 'country': 'USA',
        'alt_km': 20200, 'inc_deg': 55.0, 'total_sats': 31, 'status': 'Operational',
        'purpose': 'Navigation', 'mass_kg': 2000,
    },
    'glonass': {
        'name': 'GLONASS', 'operator': 'Roscosmos', 'country': 'Russia',
        'alt_km': 19130, 'inc_deg': 64.8, 'total_sats': 24, 'status': 'Operational',
        'purpose': 'Navigation', 'mass_kg': 1415,
    },
    'galileo': {
        'name': 'Galileo', 'operator': 'ESA/EU', 'country': 'Europe',
        'alt_km': 23222, 'inc_deg': 56.0, 'total_sats': 30, 'status': 'Operational',
        'purpose': 'Navigation', 'mass_kg': 700,
    },
    'beidou': {
        'name': 'BeiDou', 'operator': 'CNSA', 'country': 'China',
        'alt_km': 21528, 'inc_deg': 55.0, 'total_sats': 35, 'status': 'Operational',
        'purpose': 'Navigation', 'mass_kg': 800,
    },
    'iridium': {
        'name': 'Iridium NEXT', 'operator': 'Iridium', 'country': 'USA',
        'alt_km': 780, 'inc_deg': 86.4, 'total_sats': 66, 'status': 'Operational',
        'purpose': 'Satellite Phone', 'mass_kg': 860,
    },
    'iss': {
        'name': 'ISS', 'operator': 'NASA/Roscosmos/ESA/JAXA/CSA', 'country': 'International',
        'alt_km': 420, 'inc_deg': 51.6, 'total_sats': 1, 'status': 'Operational',
        'purpose': 'Space Station', 'mass_kg': 420000,
    },
    'hubble': {
        'name': 'Hubble', 'operator': 'NASA/ESA', 'country': 'USA/Europe',
        'alt_km': 547, 'inc_deg': 28.5, 'total_sats': 1, 'status': 'Operational',
        'purpose': 'Space Telescope', 'mass_kg': 11110,
    },
    'terra': {
        'name': 'Terra', 'operator': 'NASA', 'country': 'USA',
        'alt_km': 705, 'inc_deg': 98.2, 'total_sats': 1, 'status': 'Operational',
        'purpose': 'Earth Science', 'mass_kg': 5190,
    },
    'landsat9': {
        'name': 'Landsat 9', 'operator': 'NASA/USGS', 'country': 'USA',
        'alt_km': 705, 'inc_deg': 98.2, 'total_sats': 1, 'status': 'Operational',
        'purpose': 'Earth Imaging', 'mass_kg': 2711,
    },
    'sentinel': {
        'name': 'Sentinel-2', 'operator': 'ESA', 'country': 'Europe',
        'alt_km': 786, 'inc_deg': 98.6, 'total_sats': 2, 'status': 'Operational',
        'purpose': 'Earth Observation', 'mass_kg': 1140,
    },
    'qzss': {
        'name': 'QZSS', 'operator': 'JAXA', 'country': 'Japan',
        'alt_km': 32000, 'inc_deg': 43.0, 'total_sats': 4, 'status': 'Operational',
        'purpose': 'Regional Navigation', 'mass_kg': 4000,
    },
}


def style_axis_scifi(ax, title="", xlabel="", ylabel="", is_3d=False):
    """Apply dark theme styling for orbital visualization."""
    ax.set_facecolor('#060d18')
    
    if title:
        if is_3d:
            ax.set_title(title, color='#00d4ff', fontsize=12, fontweight='bold',
                        pad=8, fontfamily='monospace')
        else:
            ax.set_title(title, color='#00d4ff', fontsize=12, fontweight='bold',
                        pad=10, loc='left', fontfamily='monospace')
            ax.add_line(Line2D([0, 0.35], [1.02, 1.02], color='#00d4ff', alpha=0.8,
                               lw=2, transform=ax.transAxes, clip_on=False))
    
    ax.set_xlabel(xlabel, color='#00d4ff', fontsize=11, fontfamily='monospace', fontweight='bold')
    ax.set_ylabel(ylabel, color='#00d4ff', fontsize=11, fontfamily='monospace', fontweight='bold')
    ax.tick_params(colors='#4db8d4', labelsize=9)
    
    if is_3d:
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.yaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.zaxis._axinfo["grid"]['color'] = (0, 0.8, 1, 0.15)
        ax.zaxis.label.set_color('#00d4ff')
    else:
        for spine in ax.spines.values():
            spine.set_color('#0e4d64')
            spine.set_linewidth(2)
        ax.grid(True, color='#0a2a3a', alpha=0.5, linestyle='-', linewidth=0.5)


@dataclass
class Satellite:
    name: str
    a: float
    e: float
    i: float
    raan: float
    arg_p: float
    nu: float
    color: str = '#00d4ff'


class Propagator:
    """J2 perturbation propagator."""
    
    @staticmethod
    def j2_rates(a: float, e: float, i: float) -> tuple:
        """Secular J2 perturbation rates (rad/s)."""
        p = a * (1 - e**2)
        n = np.sqrt(MU / a**3)
        raan_dot = -1.5 * n * J2 * (R_EARTH / p)**2 * np.cos(i)
        arg_p_dot = 0.75 * n * J2 * (R_EARTH / p)**2 * (4 - 5 * np.sin(i)**2)
        return raan_dot, arg_p_dot

    @staticmethod
    def coe_to_rv(a, e, i, raan, arg_p, nu):
        """COEs to ECI position vector."""
        r_mag = a * (1 - e**2) / (1 + e * np.cos(nu))
        r_pqw = np.array([r_mag * np.cos(nu), r_mag * np.sin(nu), 0])
        
        cO, sO = np.cos(raan), np.sin(raan)
        ci, si = np.cos(i), np.sin(i)
        cw, sw = np.cos(arg_p), np.sin(arg_p)
        
        R = np.array([
            [cO*cw - sO*ci*sw, -cO*sw - sO*ci*cw,  sO*si],
            [sO*cw + cO*ci*sw, -sO*sw + cO*ci*cw, -cO*si],
            [si*sw,             si*cw,             ci]
        ])
        return R @ r_pqw
    
    @staticmethod
    def eci_to_lla(r_eci, time):
        """ECI to Lat/Lon/Alt."""
        x, y, z = r_eci
        r_mag = np.linalg.norm(r_eci)
        lat = np.arcsin(z / r_mag)
        lon_eci = np.arctan2(y, x)
        gmst = OMEGA_EARTH * time
        lon = np.arctan2(np.sin(lon_eci - gmst), np.cos(lon_eci - gmst))
        alt = r_mag - R_EARTH
        return np.degrees(lat), np.degrees(lon), alt


class ConstellationSimulator:
    """Simulates and stores constellation state."""
    
    def __init__(self, satellites: list):
        self.satellites = satellites
        self.history = {sat.name: {'x': [], 'y': [], 'z': [], 'lat': [], 'lon': [], 'v': []} 
                       for sat in satellites}
        self.dt = 10.0
        
    def simulate(self, duration: float, dt: float):
        self.dt = dt
        steps = int(duration / dt)
        
        for step in range(steps):
            time = step * dt
            
            for sat in self.satellites:
                raan_dot, arg_p_dot = Propagator.j2_rates(sat.a, sat.e, sat.i)
                current_raan = sat.raan + raan_dot * time
                current_arg_p = sat.arg_p + arg_p_dot * time
                n = np.sqrt(MU / sat.a**3)
                current_nu = sat.nu + n * time
                
                r_eci = Propagator.coe_to_rv(sat.a, sat.e, sat.i, current_raan, current_arg_p, current_nu)
                
                self.history[sat.name]['x'].append(r_eci[0] / 1000.0)
                self.history[sat.name]['y'].append(r_eci[1] / 1000.0)
                self.history[sat.name]['z'].append(r_eci[2] / 1000.0)
                
                lat, lon, _ = Propagator.eci_to_lla(r_eci, time)
                self.history[sat.name]['lat'].append(lat)
                self.history[sat.name]['lon'].append(lon)
                
                # Velocity magnitude (vis-viva)
                r = np.linalg.norm(r_eci)
                v = np.sqrt(MU * (2/r - 1/sat.a)) / 1000  # km/s
                self.history[sat.name]['v'].append(v)


class ConstellationDashboard:
    """Interactive satellite constellation visualization dashboard."""
    
    def __init__(self, sim: ConstellationSimulator):
        self.sim = sim
        self.current_view = 0
        self.views = [
            ("3D VIEW", self._draw_3d),
            ("GROUND TRACK", self._draw_ground_track),
            ("COVERAGE", self._draw_coverage),
            ("GLOBAL SATS", self._draw_stats),
        ]
        
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050a12')
        
        self.fig_texts = []
        self.button_axes = []
        self.anim = None
        
        self._setup_navigation()
        self._draw_current_view()
    
    def _setup_navigation(self):
        num_buttons = len(self.views)
        btn_w, btn_h = 0.14, 0.04
        spacing = 0.015
        total_w = num_buttons * btn_w + (num_buttons - 1) * spacing
        start_x = (1 - total_w) / 2
        
        self.buttons = []
        for i, (name, _) in enumerate(self.views):
            ax_btn = self.fig.add_axes([start_x + i * (btn_w + spacing), 0.02, btn_w, btn_h])
            self.button_axes.append(ax_btn)
            btn = Button(ax_btn, name, color='#0a1628', hovercolor='#1e3a5f')
            btn.label.set_color('#00d4ff')
            btn.label.set_fontsize(9)
            btn.label.set_fontweight('bold')
            btn.on_clicked(lambda event, idx=i: self._switch_view(idx))
            self.buttons.append(btn)
            for spine in ax_btn.spines.values():
                spine.set_color('#00d4ff')
                spine.set_linewidth(1.5)
    
    def _switch_view(self, idx):
        self.current_view = idx
        self._draw_current_view()
    
    def _clear_view(self):
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None
        for ax in [a for a in self.fig.axes if a not in self.button_axes]:
            ax.remove()
        for txt in self.fig_texts:
            try:
                txt.remove()
            except:
                pass
        self.fig_texts.clear()
    
    def _draw_current_view(self):
        self._clear_view()
        for i, btn in enumerate(self.buttons):
            if i == self.current_view:
                btn.ax.set_facecolor('#1e5f74')
                for spine in btn.ax.spines.values():
                    spine.set_color('#00ff9f')
            else:
                btn.ax.set_facecolor('#0a1628')
                for spine in btn.ax.spines.values():
                    spine.set_color('#00d4ff')
        _, draw_func = self.views[self.current_view]
        draw_func()
        self.fig.canvas.draw_idle()
    
    def _add_title(self, main, sub=""):
        t1 = self.fig.text(0.5, 0.96, f"◢ {main} ◣", fontsize=18, fontweight='bold',
                          color='#00d4ff', ha='center', fontfamily='monospace')
        self.fig_texts.append(t1)
        if sub:
            t2 = self.fig.text(0.5, 0.92, sub, fontsize=11, color='#7fdbff', ha='center',
                              alpha=0.8, fontfamily='monospace')
            self.fig_texts.append(t2)
    
    def _draw_3d(self):
        """3D constellation view."""
        self._add_title("SATELLITE CONSTELLATION", "LEO/MEO Orbit Propagation with J2 Perturbations")
        
        ax = self.fig.add_axes([0.05, 0.12, 0.6, 0.78], projection='3d')
        style_axis_scifi(ax, "", "X [km]", "Y [km]", is_3d=True)
        ax.set_zlabel("Z [km]", color='#00d4ff', fontsize=10, fontfamily='monospace')
        
        # Earth sphere
        u = np.linspace(0, 2*np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        r_km = R_EARTH / 1000
        x_e = r_km * np.outer(np.cos(u), np.sin(v))
        y_e = r_km * np.outer(np.sin(u), np.sin(v))
        z_e = r_km * np.outer(np.ones(len(u)), np.cos(v))
        ax.plot_surface(x_e, y_e, z_e, color='#1a4a6e', alpha=0.6, rstride=3, cstride=3)
        
        # Satellite trails and markers
        lines, markers = [], []
        for sat in self.sim.satellites:
            line, = ax.plot([], [], [], color=sat.color, lw=1.5, alpha=0.6)
            marker, = ax.plot([], [], [], 'o', color='white', markeredgecolor=sat.color, markersize=5)
            lines.append(line)
            markers.append(marker)
        
        limit = r_km + 1500
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        ax.view_init(elev=25, azim=45)
        
        # Telemetry panel
        ax_info = self.fig.add_axes([0.68, 0.12, 0.28, 0.78])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.96, "◢ CONSTELLATION DATA ◣", transform=ax_info.transAxes,
                    fontsize=11, fontweight='bold', color='#00d4ff', ha='center',
                    fontfamily='monospace')
        
        time_txt = ax_info.text(0.5, 0.88, "T+ 00:00:00", transform=ax_info.transAxes,
                               fontsize=14, color='#ffd700', ha='center', fontweight='bold',
                               fontfamily='monospace')
        
        # Static constellation info
        sat = self.sim.satellites[0]
        alt_km = (sat.a - R_EARTH) / 1000
        period_min = 2 * np.pi * np.sqrt(sat.a**3 / MU) / 60
        v_orbital = np.sqrt(MU / sat.a) / 1000
        
        info = [
            ("► SATELLITES", f"{len(self.sim.satellites)}", "#00d4ff"),
            ("► ALTITUDE", f"{alt_km:.0f} km", "#ff6b35"),
            ("► INCLINATION", f"{np.degrees(sat.i):.1f}°", "#00ff9f"),
            ("► PERIOD", f"{period_min:.1f} min", "#ffd700"),
            ("► VELOCITY", f"{v_orbital:.2f} km/s", "#ffffff"),
        ]
        
        for i, (label, val, col) in enumerate(info):
            y = 0.76 - i * 0.10
            ax_info.text(0.08, y, label, transform=ax_info.transAxes, fontsize=9,
                        color=col, fontfamily='monospace', fontweight='bold')
            ax_info.text(0.55, y, val, transform=ax_info.transAxes, fontsize=11,
                        color='#ffffff', fontfamily='monospace')
        
        # J2 effect info
        ax_info.text(0.5, 0.28, "◢ J2 PERTURBATION ◣", transform=ax_info.transAxes,
                    fontsize=9, fontweight='bold', color='#ff6b35', ha='center',
                    fontfamily='monospace')
        
        raan_dot, _ = Propagator.j2_rates(sat.a, sat.e, sat.i)
        raan_deg_day = np.degrees(raan_dot) * 86400
        
        ax_info.text(0.08, 0.20, "► RAAN DRIFT", transform=ax_info.transAxes, fontsize=9,
                    color='#00d4ff', fontfamily='monospace', fontweight='bold')
        ax_info.text(0.55, 0.20, f"{raan_deg_day:.2f}°/day", transform=ax_info.transAxes,
                    fontsize=10, color='#ffffff', fontfamily='monospace')
        
        ax_info.text(0.08, 0.12, "► PRECESSION", transform=ax_info.transAxes, fontsize=9,
                    color='#00d4ff', fontfamily='monospace', fontweight='bold')
        ax_info.text(0.55, 0.12, "Westward", transform=ax_info.transAxes,
                    fontsize=10, color='#ff6b35', fontfamily='monospace')
        
        def update(frame):
            idx = (frame * 5) % len(self.sim.history[self.sim.satellites[0].name]['x'])
            
            sim_time = idx * self.sim.dt
            h = int(sim_time // 3600)
            m = int((sim_time % 3600) // 60)
            s = int(sim_time % 60)
            time_txt.set_text(f"T+ {h:02d}:{m:02d}:{s:02d}")
            
            for i, sat in enumerate(self.sim.satellites):
                hist = self.sim.history[sat.name]
                trail_len = 200
                start = max(0, idx - trail_len)
                
                lines[i].set_data(hist['x'][start:idx], hist['y'][start:idx])
                lines[i].set_3d_properties(hist['z'][start:idx])
                
                markers[i].set_data([hist['x'][idx]], [hist['y'][idx]])
                markers[i].set_3d_properties([hist['z'][idx]])
            
            return lines + markers + [time_txt]
        
        frames = len(self.sim.history[self.sim.satellites[0].name]['x']) // 5
        self.anim = animation.FuncAnimation(self.fig, update, frames=frames,
                                           interval=30, blit=False)
    
    def _draw_ground_track(self):
        """Ground track projection."""
        self._add_title("GROUND TRACK PROJECTION", "Satellite Footprints on Earth Surface")
        
        ax = self.fig.add_axes([0.06, 0.12, 0.6, 0.78])
        style_axis_scifi(ax, "GROUND TRACK", "Longitude [°]", "Latitude [°]")
        
        # Grid
        for lat in range(-90, 91, 30):
            ax.axhline(lat, color='#0a2a3a', alpha=0.5, ls='--', lw=0.5)
        for lon in range(-180, 181, 60):
            ax.axvline(lon, color='#0a2a3a', alpha=0.5, ls='--', lw=0.5)
        
        ax.axhline(0, color='#ff6b35', alpha=0.3, lw=1)  # Equator
        
        # Plot all tracks
        for sat in self.sim.satellites:
            hist = self.sim.history[sat.name]
            lats = np.array(hist['lat'])
            lons = np.array(hist['lon'])
            
            # Break at discontinuities
            lon_diff = np.abs(np.diff(lons))
            breaks = np.where(lon_diff > 180)[0] + 1
            
            for seg_lat, seg_lon in zip(np.split(lats, breaks), np.split(lons, breaks)):
                if len(seg_lat) > 1:
                    ax.plot(seg_lon, seg_lat, color=sat.color, alpha=0.4, lw=1)
        
        # Current positions
        markers = []
        for sat in self.sim.satellites:
            marker, = ax.plot([], [], 'o', color=sat.color, markersize=8,
                             markeredgecolor='white', markeredgewidth=1)
            markers.append(marker)
        
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        
        # Info panel
        ax_info = self.fig.add_axes([0.70, 0.12, 0.26, 0.78])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.96, "◢ TRACKING ◣", transform=ax_info.transAxes,
                    fontsize=11, fontweight='bold', color='#00d4ff', ha='center',
                    fontfamily='monospace')
        
        time_txt = ax_info.text(0.5, 0.88, "T+ 00:00", transform=ax_info.transAxes,
                               fontsize=13, color='#ffd700', ha='center', fontweight='bold',
                               fontfamily='monospace')
        
        # Live telemetry for first sat
        labels = ["SAT-0-0 LAT", "SAT-0-0 LON", "COVERAGE", "ORBITS COMPLETE"]
        colors = ["#00d4ff", "#ff6b35", "#00ff9f", "#ffd700"]
        value_txts = []
        
        for i, (label, col) in enumerate(zip(labels, colors)):
            y = 0.76 - i * 0.12
            ax_info.text(0.08, y, f"► {label}", transform=ax_info.transAxes, fontsize=9,
                        color=col, fontfamily='monospace', fontweight='bold')
            txt = ax_info.text(0.08, y - 0.05, "---", transform=ax_info.transAxes,
                              fontsize=11, color='#ffffff', fontfamily='monospace')
            value_txts.append(txt)
        
        def update(frame):
            idx = (frame * 5) % len(self.sim.history[self.sim.satellites[0].name]['lat'])
            
            sim_time = idx * self.sim.dt
            m = int(sim_time // 60)
            s = int(sim_time % 60)
            time_txt.set_text(f"T+ {m:02d}:{s:02d}")
            
            for i, sat in enumerate(self.sim.satellites):
                hist = self.sim.history[sat.name]
                markers[i].set_data([hist['lon'][idx]], [hist['lat'][idx]])
            
            # Update telemetry
            hist0 = self.sim.history[self.sim.satellites[0].name]
            value_txts[0].set_text(f"{hist0['lat'][idx]:.2f}°")
            value_txts[1].set_text(f"{hist0['lon'][idx]:.2f}°")
            
            # Coverage estimate (simplified)
            coverage_pct = min(100, (len(self.sim.satellites) * 0.5) + (idx * 0.001))
            value_txts[2].set_text(f"~{coverage_pct:.0f}%")
            
            # Orbits complete
            sat = self.sim.satellites[0]
            period = 2 * np.pi * np.sqrt(sat.a**3 / MU)
            orbits = sim_time / period
            value_txts[3].set_text(f"{orbits:.2f}")
            
            return markers + [time_txt] + value_txts
        
        frames = len(self.sim.history[self.sim.satellites[0].name]['lat']) // 5
        self.anim = animation.FuncAnimation(self.fig, update, frames=frames,
                                           interval=50, blit=True)
    
    def _draw_coverage(self):
        """Coverage analysis view."""
        self._add_title("COVERAGE ANALYSIS", "Global Internet Service Footprint")
        
        ax = self.fig.add_axes([0.08, 0.15, 0.55, 0.72])
        style_axis_scifi(ax, "COVERAGE MAP", "Longitude [°]", "Latitude [°]")
        
        # Create coverage heatmap (simplified)
        lat_bins = np.linspace(-90, 90, 37)
        lon_bins = np.linspace(-180, 180, 73)
        coverage = np.zeros((len(lat_bins)-1, len(lon_bins)-1))
        
        # Count satellite passes in each bin
        for sat in self.sim.satellites:
            hist = self.sim.history[sat.name]
            for lat, lon in zip(hist['lat'], hist['lon']):
                lat_idx = np.searchsorted(lat_bins, lat) - 1
                lon_idx = np.searchsorted(lon_bins, lon) - 1
                if 0 <= lat_idx < len(lat_bins)-1 and 0 <= lon_idx < len(lon_bins)-1:
                    coverage[lat_idx, lon_idx] += 1
        
        # Normalize
        coverage = coverage / coverage.max() * 100
        
        im = ax.imshow(coverage, extent=[-180, 180, -90, 90], origin='lower',
                      cmap='viridis', alpha=0.8, aspect='auto')
        
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('Coverage Density [%]', color='#00d4ff', fontsize=10, fontfamily='monospace')
        cbar.ax.tick_params(colors='#4db8d4')
        
        # Info panel
        ax_info = self.fig.add_axes([0.68, 0.15, 0.28, 0.72])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00ff9f', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.95, "◢ SERVICE STATS ◣", transform=ax_info.transAxes,
                    fontsize=11, fontweight='bold', color='#00ff9f', ha='center',
                    fontfamily='monospace')
        
        stats = [
            ("GLOBAL COVERAGE", "~95%", "#00ff9f"),
            ("LATENCY", "20-40 ms", "#00d4ff"),
            ("DOWNLOAD", "50-200 Mbps", "#ff6b35"),
            ("UPLOAD", "10-20 Mbps", "#ffd700"),
            ("ACTIVE SATS", "~5,000+", "#ffffff"),
            ("COUNTRIES", "60+", "#ff6b35"),
        ]
        
        for i, (label, val, col) in enumerate(stats):
            y = 0.82 - i * 0.11
            ax_info.text(0.08, y, f"► {label}", transform=ax_info.transAxes, fontsize=9,
                        color=col, fontfamily='monospace', fontweight='bold')
            ax_info.text(0.08, y - 0.045, val, transform=ax_info.transAxes, fontsize=12,
                        color='#ffffff', fontfamily='monospace')
    
    def _draw_stats(self):
        """Global constellation statistics view."""
        self._add_title("GLOBAL SATELLITE CONSTELLATIONS", "NASA • ESA • Roscosmos • JAXA • SpaceX • More")
        
        # Left panel - Navigation constellations
        ax1 = self.fig.add_axes([0.04, 0.15, 0.44, 0.72])
        style_axis_scifi(ax1, "NAVIGATION SYSTEMS", "", "")
        ax1.axis('off')
        
        panel1 = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                                facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                                transform=ax1.transAxes)
        ax1.add_patch(panel1)
        
        ax1.text(0.5, 0.97, "◢ GNSS CONSTELLATIONS ◣", transform=ax1.transAxes,
                fontsize=13, fontweight='bold', color='#00d4ff', ha='center',
                fontfamily='monospace')
        
        nav_systems = ['gps', 'glonass', 'galileo', 'beidou', 'qzss']
        colors = ['#00d4ff', '#ff6b35', '#00ff9f', '#ffd700', '#ff69b4']
        
        for i, key in enumerate(nav_systems):
            c = CONSTELLATION_DATABASE[key]
            col = colors[i]
            y = 0.88 - i * 0.17
            
            ax1.text(0.06, y, f"► {c['name']}", transform=ax1.transAxes,
                    fontsize=13, color=col, fontfamily='monospace', fontweight='bold')
            ax1.text(0.45, y, f"({c['country']})", transform=ax1.transAxes,
                    fontsize=11, color='#7fdbff', fontfamily='monospace')
            
            info = f"Alt: {c['alt_km']:,} km | Inc: {c['inc_deg']}° | Sats: {c['total_sats']}"
            ax1.text(0.08, y - 0.055, info, transform=ax1.transAxes, fontsize=11,
                    color='#ffffff', fontfamily='monospace')
            ax1.text(0.08, y - 0.10, f"Operator: {c['operator']}", transform=ax1.transAxes,
                    fontsize=10, color='#aaaaaa', fontfamily='monospace')
        
        # Right panel - Communication & Science
        ax2 = self.fig.add_axes([0.52, 0.15, 0.44, 0.72])
        style_axis_scifi(ax2, "COMM & SCIENCE", "", "")
        ax2.axis('off')
        
        panel2 = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                                facecolor='#0a1420', edgecolor='#ff6b35', linewidth=2,
                                transform=ax2.transAxes)
        ax2.add_patch(panel2)
        
        # Internet constellations
        ax2.text(0.5, 0.97, "◢ INTERNET MEGA-CONSTELLATIONS ◣", transform=ax2.transAxes,
                fontsize=12, fontweight='bold', color='#ff6b35', ha='center',
                fontfamily='monospace')
        
        internet_sys = ['starlink', 'oneweb', 'iridium']
        for i, key in enumerate(internet_sys):
            c = CONSTELLATION_DATABASE[key]
            y = 0.88 - i * 0.12
            ax2.text(0.06, y, f"► {c['name']}", transform=ax2.transAxes,
                    fontsize=12, color='#00d4ff', fontfamily='monospace', fontweight='bold')
            ax2.text(0.40, y, f"{c['alt_km']} km | {c['total_sats']:,} sats", transform=ax2.transAxes,
                    fontsize=11, color='#ffffff', fontfamily='monospace')
        
        # Divider
        ax2.add_line(Line2D([0.05, 0.95], [0.50, 0.50], color='#ff6b35', alpha=0.3, lw=1,
                           transform=ax2.transAxes))
        
        # Science satellites
        ax2.text(0.5, 0.46, "◢ SCIENCE & OBSERVATION ◣", transform=ax2.transAxes,
                fontsize=12, fontweight='bold', color='#00ff9f', ha='center',
                fontfamily='monospace')
        
        science_sys = ['iss', 'hubble', 'terra', 'landsat9', 'sentinel']
        for i, key in enumerate(science_sys):
            c = CONSTELLATION_DATABASE[key]
            y = 0.38 - i * 0.075
            ax2.text(0.06, y, f"► {c['name']}", transform=ax2.transAxes,
                    fontsize=11, color='#00ff9f', fontfamily='monospace', fontweight='bold')
            ax2.text(0.32, y, f"{c['alt_km']} km | {c['operator']}", transform=ax2.transAxes,
                    fontsize=10, color='#ffffff', fontfamily='monospace')
            ax2.text(0.78, y, c['purpose'], transform=ax2.transAxes,
                    fontsize=9, color='#aaaaaa', fontfamily='monospace')
    
    def show(self):
        plt.show()


def run_demo():
    print("=" * 60)
    print("SATELLITE CONSTELLATION PROPAGATOR")
    print("Module 2: Orbital Mechanics")
    print("Featuring: GPS • GLONASS • Galileo • Starlink • More")
    print("=" * 60)
    
    # Create a mixed constellation demo (LEO like Starlink/OneWeb)
    altitude = 550000
    a = R_EARTH + altitude
    inc = np.radians(53.0)
    
    sats = []
    colors = ['#00d4ff', '#ff6b35', '#00ff9f']
    
    for plane in range(3):
        raan = np.radians(plane * 40)
        for sat_num in range(6):
            nu = np.radians(sat_num * 60)
            sats.append(Satellite(
                name=f"Sat-{plane}-{sat_num}",
                a=a, e=0.0, i=inc, raan=raan, arg_p=0.0, nu=nu,
                color=colors[plane]
            ))
    
    print(f"Simulating {len(sats)} satellites...")
    sim = ConstellationSimulator(sats)
    sim.simulate(duration=2*3600, dt=10.0)
    
    print("Launching dashboard...")
    print("-" * 60)
    
    dashboard = ConstellationDashboard(sim)
    dashboard.show()


if __name__ == "__main__":
    run_demo()
