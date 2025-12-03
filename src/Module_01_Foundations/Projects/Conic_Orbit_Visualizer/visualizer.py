"""
Conic Orbit Visualizer
Module 1: Foundations in Math, Physics, and Computation

Interactive visualization of orbital trajectories using Keplerian mechanics.
Includes real mission data from NASA, ESA, and SpaceX programs.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
from dataclasses import dataclass
import os

# --- Physical Constants (NASA values) ---
G = 6.67430e-11  # Gravitational Constant (m^3 kg^-1 s^-2)
C = 299792458    # Speed of light (m/s)

@dataclass
class Body:
    name: str
    mass: float
    radius: float
    mu: float  # Standard gravitational parameter (GM)
    color: str
    
EARTH = Body("Earth", 5.972e24, 6371000, 3.986004418e14, '#4a90e2')
MOON = Body("Moon", 7.342e22, 1737400, 4.9048695e12, '#888888')

# --- Real Mission Data from Global Space Agencies ---
MISSION_DATA = {
    'leo': {
        'name': 'LOW EARTH ORBIT',
        'subtitle': 'ISS • Hubble • Tiangong • Earth Observation',
        'missions': [
            'ISS (NASA/Roscosmos): 420 km, 51.6°',
            'Tiangong (CNSA): 380 km, 41.5°',
            'Hubble (NASA/ESA): 547 km, 28.5°',
            'Landsat 9 (NASA): 705 km, 98.2°',
            'Sentinel-2 (ESA): 786 km, 98.6°',
        ],
        'facts': [
            'ISS has been continuously crewed since Nov 2000',
            'China\'s Tiangong is the 2nd operational space station',
            'Sun-synchronous orbits enable consistent lighting',
        ],
        'delta_v_from_surface': 9.4,
    },
    'gto': {
        'name': 'GEOSYNC TRANSFER ORBIT',
        'subtitle': 'GPS • GLONASS • Galileo • BeiDou • QZSS',
        'missions': [
            'GPS (US Space Force): 20,200 km MEO',
            'GLONASS (Roscosmos): 19,130 km MEO',
            'Galileo (ESA): 23,222 km MEO',
            'BeiDou (CNSA): 21,528 km MEO',
            'QZSS (JAXA): 32,000 km quasi-zenith',
        ],
        'facts': [
            '4 GNSS systems provide global coverage',
            'GPS accuracy: 30 cm with dual-frequency',
            'Galileo is the most accurate GNSS system',
        ],
        'delta_v_to_geo': 1.5,
    },
    'escape': {
        'name': 'ESCAPE TRAJECTORY',
        'subtitle': 'Voyager • New Horizons • Pioneer • Hayabusa',
        'missions': [
            'Voyager 1 (NASA): 24 billion km from Earth',
            'Voyager 2 (NASA): Only probe to visit Uranus/Neptune',
            'New Horizons (NASA): First Pluto flyby 2015',
            'Hayabusa2 (JAXA): Asteroid sample return',
            'Chang\'e 5 (CNSA): Lunar sample return 2020',
        ],
        'facts': [
            'Voyager 1 entered interstellar space in 2012',
            'Pioneer 10 was first to cross asteroid belt',
            'Parker Solar Probe: fastest human-made object',
        ],
        'earth_escape_v': 11.186,
    },
    'lunar': {
        'name': 'LOW LUNAR ORBIT',
        'subtitle': 'Apollo • Artemis • Chang\'e • Chandrayaan',
        'missions': [
            'Apollo 11-17 (NASA): First humans on Moon',
            'Artemis (NASA): Return humans 2025+',
            'Chang\'e 4 (CNSA): First far-side landing',
            'Chandrayaan-3 (ISRO): South pole landing 2023',
            'SLIM (JAXA): Precision landing 2024',
        ],
        'facts': [
            'Only 12 humans have walked on the Moon',
            'India became 4th nation to soft-land 2023',
            'Japan became 5th nation to soft-land 2024',
        ],
        'transit_time_days': 3,
    },
}


def style_axis_scifi(ax, title="", xlabel="", ylabel=""):
    """Apply dark theme styling for aerospace visualization."""
    ax.set_facecolor('#060d18')
    
    if title:
        ax.set_title(title, color='#00d4ff', fontsize=13, fontweight='bold',
                    pad=12, loc='left', fontfamily='monospace')
        line = Line2D([0, 0.4], [1.02, 1.02], color='#00d4ff', alpha=0.8,
                     lw=2, transform=ax.transAxes, clip_on=False)
        ax.add_line(line)
    
    ax.set_xlabel(xlabel, color='#00d4ff', fontsize=11, labelpad=10,
                 fontfamily='monospace', fontweight='bold')
    ax.set_ylabel(ylabel, color='#00d4ff', fontsize=11, labelpad=10,
                 fontfamily='monospace', fontweight='bold')
    
    ax.tick_params(colors='#4db8d4', labelsize=9, length=5, width=1.5)
    
    for spine in ax.spines.values():
        spine.set_color('#0e4d64')
        spine.set_linewidth(2)
    
    corners = [
        ([0, 0.05], [1, 1]), ([0, 0], [1, 0.95]),
        ([0.95, 1], [1, 1]), ([1, 1], [1, 0.95]),
        ([0, 0.05], [0, 0]), ([0, 0], [0, 0.05]),
        ([0.95, 1], [0, 0]), ([1, 1], [0, 0.05]),
    ]
    for x_coords, y_coords in corners:
        corner = Line2D(x_coords, y_coords, color='#00d4ff', alpha=0.7,
                       lw=2, transform=ax.transAxes, clip_on=False)
        ax.add_line(corner)
    
    ax.grid(True, color='#0a2a3a', alpha=0.5, linestyle='-', linewidth=0.5)


@dataclass
class Orbit:
    semi_major_axis: float
    eccentricity: float
    central_body: Body = None
    
    def __post_init__(self):
        if self.central_body is None:
            self.central_body = EARTH
    
    @property
    def orbit_type(self) -> str:
        if np.isclose(self.eccentricity, 0.0): return "Circular"
        elif 0.0 < self.eccentricity < 1.0: return "Elliptical"
        elif np.isclose(self.eccentricity, 1.0): return "Parabolic"
        else: return "Hyperbolic"
    
    @property
    def period(self) -> float:
        """Orbital period in seconds."""
        if self.eccentricity >= 1.0:
            return float('inf')
        return 2 * np.pi * np.sqrt(self.semi_major_axis**3 / self.central_body.mu)
    
    @property
    def periapsis(self) -> float:
        """Periapsis distance in meters."""
        return self.semi_major_axis * (1 - self.eccentricity)
    
    @property
    def apoapsis(self) -> float:
        """Apoapsis distance in meters (inf for hyperbolic)."""
        if self.eccentricity >= 1.0:
            return float('inf')
        return self.semi_major_axis * (1 + self.eccentricity)
    
    def velocity_at_r(self, r: float) -> float:
        """Vis-viva equation: velocity at distance r."""
        if self.eccentricity >= 1.0:
            # Hyperbolic: use negative a
            return np.sqrt(self.central_body.mu * (2/r + 1/abs(self.semi_major_axis)))
        return np.sqrt(self.central_body.mu * (2/r - 1/self.semi_major_axis))
    
    @property
    def v_infinity(self) -> float:
        """Hyperbolic excess velocity (only for e > 1)."""
        if self.eccentricity <= 1.0:
            return 0.0
        return np.sqrt(-self.central_body.mu / self.semi_major_axis)


class OrbitDashboard:
    """Interactive dashboard for orbit visualization with real mission data."""
    
    def __init__(self):
        self.current_view = 0
        self.views = [
            ("LEO", self._draw_leo),
            ("GTO", self._draw_gto),
            ("ESCAPE", self._draw_escape),
            ("LUNAR", self._draw_lunar),
        ]
        
        self._precompute_orbits()
        
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050a12')
        
        self.fig_texts = []
        self.button_axes = []
        self.anim = None
        
        self._setup_navigation()
        self._draw_current_view()
    
    def _precompute_orbits(self):
        """Compute all orbit trajectories with real parameters."""
        self.orbits = {}
        
        # LEO - ISS parameters (420 km altitude)
        alt_iss = 420000  # 420 km
        a_leo = EARTH.radius + alt_iss
        self.orbits['leo'] = self._compute_orbit(Orbit(a_leo, 0.0005, EARTH))  # Slight eccentricity
        
        # GTO - Typical SpaceX GTO (185 km x 35,786 km)
        r_p = EARTH.radius + 185000
        r_a = EARTH.radius + 35786000  # GEO altitude
        a_gto = (r_p + r_a) / 2
        e_gto = (r_a - r_p) / (r_a + r_p)
        self.orbits['gto'] = self._compute_orbit(Orbit(a_gto, e_gto, EARTH))
        
        # Hyperbolic escape (Mars mission departure, C3 ~10 km²/s²)
        # V∞ ≈ 3.2 km/s for Mars transfer
        v_inf = 3200  # m/s
        r_p_esc = EARTH.radius + 200000  # 200 km departure
        # a = -μ/v∞² and e = 1 + r_p*v∞²/μ
        a_esc = -EARTH.mu / v_inf**2
        e_esc = 1 + r_p_esc * v_inf**2 / EARTH.mu
        self.orbits['escape'] = self._compute_orbit(Orbit(a_esc, e_esc, EARTH))
        
        # Low Lunar Orbit (100 km altitude)
        alt_llo = 100000
        a_llo = MOON.radius + alt_llo
        self.orbits['lunar'] = self._compute_orbit(Orbit(a_llo, 0.0, MOON))
    
    def _compute_orbit(self, orbit: Orbit):
        """Calculate orbit trajectory."""
        if orbit.eccentricity >= 1.0:
            # Hyperbolic - limit to physical branch
            e = orbit.eccentricity
            limit = np.arccos(-1.0 / e) - 0.15
            theta = np.linspace(-limit, limit, 600)
        else:
            theta = np.linspace(0, 2*np.pi, 600)
        
        # Orbit equation: r = a(1-e²)/(1 + e·cos(θ))
        p = orbit.semi_major_axis * (1 - orbit.eccentricity**2)
        r = p / (1 + orbit.eccentricity * np.cos(theta))
        
        x = r * np.cos(theta) / 1000  # km
        y = r * np.sin(theta) / 1000
        r_km = r / 1000
        
        # Velocity at each point (vis-viva)
        if orbit.eccentricity >= 1.0:
            v = np.sqrt(orbit.central_body.mu * (2/r + 1/abs(orbit.semi_major_axis))) / 1000
        else:
            v = np.sqrt(orbit.central_body.mu * (2/r - 1/orbit.semi_major_axis)) / 1000
        
        mask = r > 0
        
        return {
            'orbit': orbit,
            'x': x[mask], 'y': y[mask], 'r_km': r_km[mask],
            'v_km_s': v[mask], 'theta': theta[mask],
            'body_radius_km': orbit.central_body.radius / 1000
        }
    
    def _setup_navigation(self):
        """Create navigation buttons."""
        num_buttons = len(self.views)
        button_width = 0.15
        button_height = 0.04
        spacing = 0.02
        total_width = num_buttons * button_width + (num_buttons - 1) * spacing
        start_x = (1 - total_width) / 2
        
        self.buttons = []
        for i, (name, _) in enumerate(self.views):
            ax_btn = self.fig.add_axes([start_x + i * (button_width + spacing),
                                        0.02, button_width, button_height])
            self.button_axes.append(ax_btn)
            btn = Button(ax_btn, name, color='#0a1628', hovercolor='#1e3a5f')
            btn.label.set_color('#00d4ff')
            btn.label.set_fontsize(10)
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
        
        axes_to_remove = [ax for ax in self.fig.axes if ax not in self.button_axes]
        for ax in axes_to_remove:
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
    
    def _add_title(self, main_title, subtitle=""):
        t1 = self.fig.text(0.5, 0.96, f"◢ {main_title} ◣",
                         fontsize=18, fontweight='bold', color='#00d4ff', ha='center',
                         fontfamily='monospace')
        self.fig_texts.append(t1)
        if subtitle:
            t2 = self.fig.text(0.5, 0.92, subtitle,
                              fontsize=11, color='#7fdbff', ha='center', alpha=0.8,
                              fontfamily='monospace')
            self.fig_texts.append(t2)
    
    def _draw_orbit_with_telemetry(self, key, mission_key):
        """Generic orbit drawing with rich telemetry."""
        data = self.orbits[key]
        orbit = data['orbit']
        mission = MISSION_DATA[mission_key]
        
        # Main orbit plot
        ax = self.fig.add_axes([0.06, 0.15, 0.48, 0.72])
        style_axis_scifi(ax, "TRAJECTORY", "X [km]", "Y [km]")
        
        # Central body
        body_circle = Circle((0, 0), data['body_radius_km'], 
                            color=orbit.central_body.color, alpha=0.8, zorder=2)
        ax.add_patch(body_circle)
        
        # Atmosphere glow
        if orbit.central_body.name == "Earth":
            atmo = Circle((0, 0), data['body_radius_km'] * 1.025,
                         color='#00d4ff', alpha=0.15, zorder=1)
            ax.add_patch(atmo)
        
        # Orbit trajectory with glow
        ax.plot(data['x'], data['y'], color='#00d4ff', lw=6, alpha=0.15, zorder=3)
        ax.plot(data['x'], data['y'], color='#00d4ff', lw=2, alpha=0.9, zorder=4)
        
        # Spacecraft marker
        spacecraft, = ax.plot([], [], marker='^', color='#00ff9f', markersize=14, zorder=5)
        
        # Set limits
        if orbit.eccentricity > 1:
            periapsis_dist = np.min(data['r_km'])
            limit = periapsis_dist * 4
        else:
            limit = np.max(np.abs(data['r_km'])) * 1.15
        
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        
        # Info panel
        ax_info = self.fig.add_axes([0.58, 0.15, 0.38, 0.72])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                               boxstyle="round,pad=0.02,rounding_size=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff',
                               linewidth=2, alpha=0.95, transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        # Live telemetry header
        ax_info.text(0.5, 0.96, "◢ LIVE TELEMETRY ◣", transform=ax_info.transAxes,
                    fontsize=12, fontweight='bold', color='#00d4ff', ha='center',
                    fontfamily='monospace')
        
        # Dynamic telemetry values
        time_txt = ax_info.text(0.5, 0.89, "T+ 0:00", transform=ax_info.transAxes,
                               fontsize=14, color='#ffd700', ha='center', fontweight='bold',
                               fontfamily='monospace')
        
        telem_labels = ["ALTITUDE", "VELOCITY", "TRUE ANOMALY", "RANGE RATE"]
        telem_colors = ["#00d4ff", "#ff6b35", "#00ff9f", "#ffd700"]
        telem_txts = []
        
        for i, (label, col) in enumerate(zip(telem_labels, telem_colors)):
            y = 0.80 - i * 0.10
            ax_info.text(0.08, y, f"► {label}", transform=ax_info.transAxes, fontsize=9,
                        color=col, fontfamily='monospace', fontweight='bold')
            txt = ax_info.text(0.55, y, "---", transform=ax_info.transAxes, fontsize=11,
                              color='#ffffff', fontfamily='monospace')
            telem_txts.append(txt)
        
        # Divider
        div = Line2D([0.05, 0.95], [0.42, 0.42], color='#00d4ff', alpha=0.3, lw=1,
                    transform=ax_info.transAxes)
        ax_info.add_line(div)
        
        # Mission info section
        ax_info.text(0.5, 0.38, "◢ MISSION DATA ◣", transform=ax_info.transAxes,
                    fontsize=10, fontweight='bold', color='#ff6b35', ha='center',
                    fontfamily='monospace')
        
        # Real mission examples
        for i, mission_txt in enumerate(mission['missions'][:3]):
            y = 0.32 - i * 0.06
            ax_info.text(0.08, y, f"• {mission_txt}", transform=ax_info.transAxes,
                        fontsize=8, color='#aaaaaa', fontfamily='monospace')
        
        # Fun facts
        ax_info.text(0.5, 0.12, "◢ DID YOU KNOW? ◣", transform=ax_info.transAxes,
                    fontsize=9, fontweight='bold', color='#00ff9f', ha='center',
                    fontfamily='monospace')
        
        fact = mission['facts'][0]
        ax_info.text(0.5, 0.06, fact, transform=ax_info.transAxes,
                    fontsize=8, color='#7fdbff', ha='center', fontfamily='monospace',
                    wrap=True)
        
        self._add_title(mission['name'], mission['subtitle'])
        
        # Animation with live telemetry
        def update(frame):
            if len(data['x']) == 0:
                return [spacecraft, time_txt] + telem_txts
            
            idx = frame % len(data['x'])
            spacecraft.set_data([data['x'][idx]], [data['y'][idx]])
            
            # Calculate orbital time
            if orbit.eccentricity < 1.0:
                period_min = orbit.period / 60
                elapsed = (idx / len(data['x'])) * period_min
                mins = int(elapsed)
                secs = int((elapsed - mins) * 60)
                time_txt.set_text(f"T+ {mins}:{secs:02d}")
            else:
                time_txt.set_text(f"FRAME {idx}")
            
            # Update telemetry
            alt = data['r_km'][idx] - data['body_radius_km']
            vel = data['v_km_s'][idx]
            theta_deg = np.degrees(data['theta'][idx]) % 360
            
            # Range rate (radial velocity component)
            if idx > 0:
                dr = data['r_km'][idx] - data['r_km'][idx-1]
                range_rate = dr * 100  # Approximate
            else:
                range_rate = 0
            
            telem_txts[0].set_text(f"{alt:.1f} km")
            telem_txts[1].set_text(f"{vel:.3f} km/s")
            telem_txts[2].set_text(f"{theta_deg:.1f}°")
            telem_txts[3].set_text(f"{range_rate:+.2f} km/s")
            
            return [spacecraft, time_txt] + telem_txts
        
        self.anim = animation.FuncAnimation(self.fig, update, frames=len(data['x']),
                                           interval=30, blit=True)
    
    def _draw_leo(self):
        self._draw_orbit_with_telemetry('leo', 'leo')
    
    def _draw_gto(self):
        self._draw_orbit_with_telemetry('gto', 'gto')
    
    def _draw_escape(self):
        self._draw_orbit_with_telemetry('escape', 'escape')
    
    def _draw_lunar(self):
        self._draw_orbit_with_telemetry('lunar', 'lunar')
    
    def show(self):
        plt.show()


def run_demo():
    print("=" * 60)
    print("CONIC ORBIT VISUALIZER")
    print("Module 1: Foundations")
    print("=" * 60)
    print("\nOrbital mechanics with real NASA/SpaceX mission data")
    print("Use buttons to switch between orbit types.")
    print("-" * 60)
    
    dashboard = OrbitDashboard()
    dashboard.show()


if __name__ == "__main__":
    run_demo()
