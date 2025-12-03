"""
Rocket Ascent Simulator
Module 1: Foundations in Math, Physics, and Computation

3D rocket ascent simulation with RK4 numerical integration.
Models thrust, gravity, atmospheric drag, and mass depletion.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from dataclasses import dataclass
from typing import Dict, List

# --- Constants ---
G = 6.67430e-11
M_EARTH = 5.972e24
R_EARTH = 6371000
SEA_LEVEL_DENSITY = 1.225
SCALE_HEIGHT = 8500


def style_axis_scifi(ax, title="", xlabel="", ylabel="", is_3d=False):
    """Apply dark theme styling for technical visualization."""
    ax.set_facecolor('#060d18')
    
    if title:
        if is_3d:
            ax.set_title(title, color='#00d4ff', fontsize=12, fontweight='bold',
                        pad=8, fontfamily='monospace')
        else:
            ax.set_title(title, color='#00d4ff', fontsize=12, fontweight='bold',
                        pad=10, loc='left', fontfamily='monospace')
            line = Line2D([0, 0.35], [1.02, 1.02], color='#00d4ff', alpha=0.8,
                         lw=2, transform=ax.transAxes, clip_on=False)
            ax.add_line(line)
    
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
        
        corners = [
            ([0, 0.04], [1, 1]), ([0, 0], [1, 0.96]),
            ([0.96, 1], [1, 1]), ([1, 1], [1, 0.96]),
            ([0, 0.04], [0, 0]), ([0, 0], [0, 0.04]),
            ([0.96, 1], [0, 0]), ([1, 1], [0, 0.04]),
        ]
        for x_c, y_c in corners:
            ax.add_line(Line2D(x_c, y_c, color='#00d4ff', alpha=0.6, lw=1.5,
                              transform=ax.transAxes, clip_on=False))


@dataclass
class RocketParams:
    """Falcon 9-like rocket parameters."""
    wet_mass: float = 549054.0    # kg
    dry_mass: float = 22200.0     # kg
    thrust: float = 7607000.0     # N (sea level)
    isp: float = 282.0            # s
    drag_coeff: float = 0.3       # Cd
    area: float = 10.5            # m^2
    burn_time: float = 162.0      # s


class RocketSimulator:
    """Simulates rocket flight using RK4 integration."""
    
    def __init__(self, rocket: RocketParams):
        self.rocket = rocket
        self.history: Dict[str, List[float]] = {
            'time': [], 'x': [], 'y': [], 'z': [],
            'vx': [], 'vy': [], 'vz': [],
            'altitude': [], 'mass': [], 'dynamic_pressure': [],
            'acceleration': []
        }

    def _get_gravity(self, r: np.ndarray) -> np.ndarray:
        """Gravitational acceleration toward Earth center."""
        r_mag = np.linalg.norm(r)
        if r_mag == 0:
            return np.zeros(3)
        return -(G * M_EARTH / r_mag**2) * (r / r_mag)

    def _get_density(self, altitude: float) -> float:
        """Atmospheric density using exponential model."""
        if altitude < 0:
            return SEA_LEVEL_DENSITY
        return SEA_LEVEL_DENSITY * np.exp(-altitude / SCALE_HEIGHT)

    def _derivatives(self, t: float, state: np.ndarray) -> np.ndarray:
        """Compute state derivatives for RK4."""
        r = state[:3]
        v = state[3:6]
        m = state[6]
        
        r_mag = np.linalg.norm(r)
        v_mag = np.linalg.norm(v)
        altitude = r_mag - R_EARTH
        
        # Gravity - always present
        a_gravity = self._get_gravity(r)
        
        # Drag - opposes velocity
        rho = self._get_density(altitude)
        if v_mag > 0:
            v_hat = v / v_mag
            drag_force = 0.5 * rho * v_mag**2 * self.rocket.drag_coeff * self.rocket.area
            a_drag = -(drag_force / m) * v_hat
        else:
            a_drag = np.zeros(3)
        
        # Thrust
        a_thrust = np.zeros(3)
        dm_dt = 0.0
        
        if t < self.rocket.burn_time and m > self.rocket.dry_mass:
            # Initial vertical ascent, then gravity turn
            r_hat = r / r_mag
            
            if v_mag < 50:
                # Vertical launch phase
                thrust_dir = r_hat
            else:
                # Gravity turn - thrust along velocity with slight pitch program
                # Blend between radial and velocity direction
                pitch_angle = min(t / 60.0, 1.0) * 0.3  # Gradually pitch over
                thrust_dir = (1 - pitch_angle) * r_hat + pitch_angle * (v / v_mag)
                thrust_dir = thrust_dir / np.linalg.norm(thrust_dir)
            
            a_thrust = (self.rocket.thrust / m) * thrust_dir
            
            # Mass flow rate: mdot = T / (Isp * g0)
            g0 = 9.80665
            dm_dt = -self.rocket.thrust / (self.rocket.isp * g0)
        
        a_total = a_gravity + a_drag + a_thrust
        return np.concatenate([v, a_total, [dm_dt]])

    def _rk4_step(self, t: float, state: np.ndarray, dt: float) -> np.ndarray:
        """Single RK4 integration step."""
        k1 = self._derivatives(t, state)
        k2 = self._derivatives(t + 0.5*dt, state + 0.5*dt*k1)
        k3 = self._derivatives(t + 0.5*dt, state + 0.5*dt*k2)
        k4 = self._derivatives(t + dt, state + dt*k3)
        return state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

    def run(self, duration: float = 500.0, dt: float = 0.5):
        """Run the simulation."""
        # Start on Earth's surface (x-axis, equator)
        state = np.array([R_EARTH, 0, 0, 0, 0, 0, self.rocket.wet_mass], dtype=float)
        t = 0.0
        
        print(f"Simulating Falcon 9 ascent...")
        print(f"  Wet Mass: {self.rocket.wet_mass/1000:.0f} tonnes")
        print(f"  Thrust: {self.rocket.thrust/1e6:.1f} MN")
        print(f"  T/W Ratio: {self.rocket.thrust/(self.rocket.wet_mass*9.81):.2f}")
        
        while t <= duration:
            r = state[:3]
            v = state[3:6]
            m = state[6]
            
            r_mag = np.linalg.norm(r)
            v_mag = np.linalg.norm(v)
            alt = r_mag - R_EARTH
            
            # Stop if crashed
            if alt < -100:
                print(f"  Impact at T+{t:.1f}s")
                break
            
            # Record state
            self.history['time'].append(t)
            self.history['x'].append(r[0])
            self.history['y'].append(r[1])
            self.history['z'].append(r[2])
            self.history['vx'].append(v[0])
            self.history['vy'].append(v[1])
            self.history['vz'].append(v[2])
            self.history['altitude'].append(alt)
            self.history['mass'].append(m)
            
            # Dynamic pressure
            rho = self._get_density(alt)
            q = 0.5 * rho * v_mag**2
            self.history['dynamic_pressure'].append(q)
            
            # Acceleration magnitude
            derivs = self._derivatives(t, state)
            a_mag = np.linalg.norm(derivs[3:6])
            self.history['acceleration'].append(a_mag / 9.81)  # in G's
            
            state = self._rk4_step(t, state, dt)
            t += dt
        
        max_alt = max(self.history['altitude']) / 1000
        max_vel = max(np.sqrt(np.array(self.history['vx'])**2 + 
                              np.array(self.history['vy'])**2 + 
                              np.array(self.history['vz'])**2))
        print(f"  Max Altitude: {max_alt:.1f} km")
        print(f"  Max Velocity: {max_vel:.0f} m/s ({max_vel/1000:.1f} km/s)")


class AscentDashboard:
    """Interactive dashboard with live telemetry."""
    
    def __init__(self, simulator: RocketSimulator):
        self.sim = simulator
        self.current_view = 0
        self.views = [
            ("OVERVIEW", self._draw_overview),
            ("ALTITUDE", self._draw_altitude),
            ("VELOCITY", self._draw_velocity),
            ("MAX Q", self._draw_maxq),
            ("3D PATH", self._draw_3d),
        ]
        
        self._process_data()
        
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050a12')
        
        self.fig_texts = []
        self.button_axes = []
        self.anim = None
        
        self._setup_navigation()
        self._draw_current_view()
    
    def _process_data(self):
        """Convert history to numpy arrays."""
        self.time = np.array(self.sim.history['time'])
        self.alt_km = np.array(self.sim.history['altitude']) / 1000.0
        self.vel_mag = np.sqrt(np.array(self.sim.history['vx'])**2 + 
                               np.array(self.sim.history['vy'])**2 + 
                               np.array(self.sim.history['vz'])**2)
        self.q_kpa = np.array(self.sim.history['dynamic_pressure']) / 1000.0
        self.mass = np.array(self.sim.history['mass']) / 1000  # tonnes
        self.accel_g = np.array(self.sim.history['acceleration'])
        
        # 3D trajectory in km
        x = np.array(self.sim.history['x'])
        y = np.array(self.sim.history['y'])
        z = np.array(self.sim.history['z'])
        
        # Convert to local coordinates (relative to launch site)
        # Launch site is at [R_EARTH, 0, 0]
        self.traj_up = (np.sqrt(x**2 + y**2 + z**2) - R_EARTH) / 1000  # altitude
        self.traj_east = np.arctan2(y, x) * R_EARTH / 1000  # downrange
        self.traj_north = z / 1000
    
    def _setup_navigation(self):
        """Create navigation buttons."""
        num_buttons = len(self.views)
        btn_w, btn_h = 0.12, 0.04
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
    
    def _draw_overview(self):
        """4-panel overview."""
        self._add_title("ROCKET ASCENT SIMULATION", "Falcon 9 First Stage Profile")
        
        ax1 = self.fig.add_axes([0.06, 0.52, 0.42, 0.35])
        ax2 = self.fig.add_axes([0.54, 0.52, 0.42, 0.35])
        ax3 = self.fig.add_axes([0.06, 0.12, 0.42, 0.35])
        ax4 = self.fig.add_axes([0.54, 0.12, 0.42, 0.35])
        
        style_axis_scifi(ax1, "ALTITUDE", "Time [s]", "Alt [km]")
        ax1.plot(self.time, self.alt_km, color='#00d4ff', lw=2)
        ax1.fill_between(self.time, 0, self.alt_km, color='#00d4ff', alpha=0.15)
        
        style_axis_scifi(ax2, "VELOCITY", "Time [s]", "Vel [m/s]")
        ax2.plot(self.time, self.vel_mag, color='#ff6b35', lw=2)
        ax2.fill_between(self.time, 0, self.vel_mag, color='#ff6b35', alpha=0.15)
        
        style_axis_scifi(ax3, "DYNAMIC PRESSURE", "Time [s]", "Q [kPa]")
        ax3.plot(self.time, self.q_kpa, color='#ffd700', lw=2)
        ax3.fill_between(self.time, 0, self.q_kpa, color='#ffd700', alpha=0.15)
        max_q_idx = np.argmax(self.q_kpa)
        ax3.axvline(x=self.time[max_q_idx], color='#ff3366', ls='--', lw=1.5)
        ax3.scatter([self.time[max_q_idx]], [self.q_kpa[max_q_idx]], color='#ff3366', s=80, zorder=5)
        
        style_axis_scifi(ax4, "ACCELERATION", "Time [s]", "Accel [G]")
        ax4.plot(self.time, self.accel_g, color='#00ff9f', lw=2)
        ax4.fill_between(self.time, 0, self.accel_g, color='#00ff9f', alpha=0.15)
        ax4.axhline(y=3.0, color='#ff3366', ls=':', lw=1, alpha=0.7)
        ax4.text(self.time[-1]*0.7, 3.2, '3G LIMIT', color='#ff3366', fontsize=8, fontfamily='monospace')
    
    def _draw_altitude(self):
        """Altitude view with live telemetry."""
        self._add_title("ALTITUDE PROFILE", "Vehicle Altitude During Ascent")
        
        ax = self.fig.add_axes([0.08, 0.15, 0.55, 0.72])
        style_axis_scifi(ax, "ALTITUDE vs TIME", "Time [s]", "Altitude [km]")
        ax.plot(self.time, self.alt_km, color='#00d4ff', lw=3, alpha=0.3)
        ax.plot(self.time, self.alt_km, color='#00d4ff', lw=1.5)
        ax.fill_between(self.time, 0, self.alt_km, color='#00d4ff', alpha=0.1)
        
        # Reference lines
        ax.axhline(y=100, color='#ff6b35', ls='--', lw=1, alpha=0.5)
        ax.text(10, 105, 'KARMAN LINE (100km)', color='#ff6b35', fontsize=8, fontfamily='monospace')
        
        marker, = ax.plot([], [], 'o', color='#00ff9f', markersize=14, zorder=5)
        
        # Info panel
        ax_info = self.fig.add_axes([0.68, 0.15, 0.28, 0.72])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.95, "◢ LIVE TELEMETRY ◣", transform=ax_info.transAxes, fontsize=12,
                    fontweight='bold', color='#00d4ff', ha='center', fontfamily='monospace')
        
        # Create text elements for live update
        time_txt = ax_info.text(0.5, 0.82, "T+ 0.0s", transform=ax_info.transAxes, fontsize=16,
                               color='#ffd700', ha='center', fontweight='bold', fontfamily='monospace')
        
        labels = ["ALTITUDE", "VELOCITY", "ACCELERATION", "MASS"]
        colors = ["#00d4ff", "#ff6b35", "#00ff9f", "#ffffff"]
        value_txts = []
        
        for i, (label, col) in enumerate(zip(labels, colors)):
            y = 0.68 - i * 0.15
            ax_info.text(0.1, y, f"► {label}", transform=ax_info.transAxes, fontsize=10,
                        color=col, fontfamily='monospace', fontweight='bold')
            txt = ax_info.text(0.1, y - 0.06, "0", transform=ax_info.transAxes, fontsize=14,
                              color='#ffffff', fontfamily='monospace')
            value_txts.append(txt)
        
        # Engine status
        engine_txt = ax_info.text(0.5, 0.12, "● ENGINE: NOMINAL", transform=ax_info.transAxes,
                                 fontsize=11, color='#00ff9f', ha='center', fontfamily='monospace',
                                 fontweight='bold')
        
        def update(frame):
            idx = (frame * 2) % len(self.time)
            marker.set_data([self.time[idx]], [self.alt_km[idx]])
            
            time_txt.set_text(f"T+ {self.time[idx]:.1f}s")
            value_txts[0].set_text(f"{self.alt_km[idx]:.1f} km")
            value_txts[1].set_text(f"{self.vel_mag[idx]:.0f} m/s")
            value_txts[2].set_text(f"{self.accel_g[idx]:.2f} G")
            value_txts[3].set_text(f"{self.mass[idx]:.0f} tonnes")
            
            if self.time[idx] < self.sim.rocket.burn_time:
                engine_txt.set_text("● ENGINE: NOMINAL")
                engine_txt.set_color('#00ff9f')
            else:
                engine_txt.set_text("● ENGINE: CUTOFF")
                engine_txt.set_color('#ff6b6b')
            
            return [marker, time_txt] + value_txts + [engine_txt]
        
        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.time)//2,
                                           interval=50, blit=True)
    
    def _draw_velocity(self):
        """Velocity view with telemetry."""
        self._add_title("VELOCITY PROFILE", "Vehicle Speed During Ascent")
        
        ax = self.fig.add_axes([0.08, 0.15, 0.55, 0.72])
        style_axis_scifi(ax, "VELOCITY vs TIME", "Time [s]", "Velocity [m/s]")
        ax.plot(self.time, self.vel_mag, color='#ff6b35', lw=3, alpha=0.3)
        ax.plot(self.time, self.vel_mag, color='#ff6b35', lw=1.5)
        ax.fill_between(self.time, 0, self.vel_mag, color='#ff6b35', alpha=0.1)
        
        # MECO marker
        meco_idx = np.searchsorted(self.time, self.sim.rocket.burn_time)
        if meco_idx < len(self.time):
            ax.axvline(x=self.sim.rocket.burn_time, color='#ff3366', ls='--', lw=2)
            ax.text(self.sim.rocket.burn_time + 5, max(self.vel_mag)*0.5, 'MECO',
                   color='#ff3366', fontsize=11, fontfamily='monospace', fontweight='bold')
        
        marker, = ax.plot([], [], 'o', color='#00ff9f', markersize=14, zorder=5)
        
        ax_info = self.fig.add_axes([0.68, 0.15, 0.28, 0.72])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#ff6b35', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.95, "◢ LIVE TELEMETRY ◣", transform=ax_info.transAxes, fontsize=12,
                    fontweight='bold', color='#ff6b35', ha='center', fontfamily='monospace')
        
        time_txt = ax_info.text(0.5, 0.82, "T+ 0.0s", transform=ax_info.transAxes, fontsize=16,
                               color='#ffd700', ha='center', fontweight='bold', fontfamily='monospace')
        
        labels = ["VELOCITY", "MACH NUMBER", "ALTITUDE", "DOWNRANGE"]
        colors = ["#ff6b35", "#00d4ff", "#00ff9f", "#ffffff"]
        value_txts = []
        
        for i, (label, col) in enumerate(zip(labels, colors)):
            y = 0.68 - i * 0.15
            ax_info.text(0.1, y, f"► {label}", transform=ax_info.transAxes, fontsize=10,
                        color=col, fontfamily='monospace', fontweight='bold')
            txt = ax_info.text(0.1, y - 0.06, "0", transform=ax_info.transAxes, fontsize=14,
                              color='#ffffff', fontfamily='monospace')
            value_txts.append(txt)
        
        def update(frame):
            idx = (frame * 2) % len(self.time)
            marker.set_data([self.time[idx]], [self.vel_mag[idx]])
            
            time_txt.set_text(f"T+ {self.time[idx]:.1f}s")
            value_txts[0].set_text(f"{self.vel_mag[idx]:.0f} m/s")
            value_txts[1].set_text(f"Mach {self.vel_mag[idx]/343:.1f}")
            value_txts[2].set_text(f"{self.alt_km[idx]:.1f} km")
            value_txts[3].set_text(f"{self.traj_east[idx]:.1f} km")
            
            return [marker, time_txt] + value_txts
        
        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.time)//2,
                                           interval=50, blit=True)
    
    def _draw_maxq(self):
        """Max-Q analysis view."""
        self._add_title("DYNAMIC PRESSURE", "Max-Q Analysis")
        
        ax = self.fig.add_axes([0.08, 0.15, 0.55, 0.72])
        style_axis_scifi(ax, "DYNAMIC PRESSURE vs TIME", "Time [s]", "Q [kPa]")
        ax.plot(self.time, self.q_kpa, color='#ffd700', lw=3, alpha=0.3)
        ax.plot(self.time, self.q_kpa, color='#ffd700', lw=1.5)
        ax.fill_between(self.time, 0, self.q_kpa, color='#ffd700', alpha=0.1)
        
        max_q_idx = np.argmax(self.q_kpa)
        ax.axvline(x=self.time[max_q_idx], color='#ff3366', ls='--', lw=2)
        ax.scatter([self.time[max_q_idx]], [self.q_kpa[max_q_idx]], color='#ff3366',
                  s=200, zorder=5, marker='*')
        
        ax_info = self.fig.add_axes([0.68, 0.15, 0.28, 0.72])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#ffd700', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.95, "◢ MAX Q DATA ◣", transform=ax_info.transAxes, fontsize=12,
                    fontweight='bold', color='#ffd700', ha='center', fontfamily='monospace')
        
        stats = [
            ("PEAK PRESSURE", f"{self.q_kpa[max_q_idx]:.1f} kPa", "#ff3366"),
            ("TIME @ MAX Q", f"T+ {self.time[max_q_idx]:.1f}s", "#ffd700"),
            ("ALTITUDE @ MAX Q", f"{self.alt_km[max_q_idx]:.1f} km", "#00d4ff"),
            ("VELOCITY @ MAX Q", f"{self.vel_mag[max_q_idx]:.0f} m/s", "#ff6b35"),
            ("MACH @ MAX Q", f"Mach {self.vel_mag[max_q_idx]/343:.1f}", "#00ff9f"),
        ]
        
        for i, (label, val, col) in enumerate(stats):
            y = 0.80 - i * 0.14
            ax_info.text(0.1, y, f"► {label}", transform=ax_info.transAxes, fontsize=10,
                        color=col, fontfamily='monospace', fontweight='bold')
            ax_info.text(0.1, y - 0.055, val, transform=ax_info.transAxes, fontsize=13,
                        color='#ffffff', fontfamily='monospace')
    
    def _draw_3d(self):
        """3D trajectory with live telemetry."""
        self._add_title("3D TRAJECTORY", "Ascent Path Visualization")
        
        ax = self.fig.add_axes([0.05, 0.12, 0.55, 0.78], projection='3d')
        style_axis_scifi(ax, "", "Downrange [km]", "Altitude [km]", is_3d=True)
        ax.set_zlabel("Cross-track [km]", color='#00d4ff', fontsize=10, fontfamily='monospace')
        
        # Plot trajectory
        ax.plot(self.traj_east, self.traj_up, self.traj_north, color='#00d4ff', lw=3, alpha=0.3)
        ax.plot(self.traj_east, self.traj_up, self.traj_north, color='#00d4ff', lw=1.5)
        
        # Launch and end markers
        ax.scatter([self.traj_east[0]], [self.traj_up[0]], [self.traj_north[0]], 
                  color='#00ff9f', s=100, marker='o', label='LAUNCH')
        ax.scatter([self.traj_east[-1]], [self.traj_up[-1]], [self.traj_north[-1]], 
                  color='#ff3366', s=100, marker='^', label='MECO')
        
        rocket, = ax.plot([], [], [], 'o', color='#ffffff', markersize=12)
        trail, = ax.plot([], [], [], color='#00ff9f', lw=2, alpha=0.7)
        
        ax.set_xlim(min(self.traj_east)-10, max(self.traj_east)+10)
        ax.set_ylim(0, max(self.traj_up)*1.1)
        ax.set_zlim(min(self.traj_north)-5, max(self.traj_north)+5)
        
        ax.legend(loc='upper left', facecolor='#0a1420', labelcolor='white', fontsize=9)
        ax.view_init(elev=15, azim=-60)
        
        # Telemetry panel
        ax_info = self.fig.add_axes([0.63, 0.12, 0.34, 0.78])
        ax_info.set_facecolor('#050a12')
        ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=ax_info.transAxes)
        ax_info.add_patch(panel)
        
        ax_info.text(0.5, 0.96, "◢ FLIGHT TELEMETRY ◣", transform=ax_info.transAxes, fontsize=12,
                    fontweight='bold', color='#00d4ff', ha='center', fontfamily='monospace')
        
        time_txt = ax_info.text(0.5, 0.88, "T+ 0.0s", transform=ax_info.transAxes, fontsize=18,
                               color='#ffd700', ha='center', fontweight='bold', fontfamily='monospace')
        
        labels = ["ALTITUDE", "VELOCITY", "DOWNRANGE", "ACCELERATION", "MASS"]
        colors = ["#00d4ff", "#ff6b35", "#00ff9f", "#ffd700", "#ffffff"]
        value_txts = []
        
        for i, (label, col) in enumerate(zip(labels, colors)):
            y = 0.76 - i * 0.12
            ax_info.text(0.08, y, f"► {label}", transform=ax_info.transAxes, fontsize=10,
                        color=col, fontfamily='monospace', fontweight='bold')
            txt = ax_info.text(0.55, y, "0", transform=ax_info.transAxes, fontsize=12,
                              color='#ffffff', fontfamily='monospace', ha='left')
            value_txts.append(txt)
        
        engine_txt = ax_info.text(0.5, 0.12, "● ENGINE: NOMINAL", transform=ax_info.transAxes,
                                 fontsize=12, color='#00ff9f', ha='center', fontfamily='monospace',
                                 fontweight='bold')
        
        phase_txt = ax_info.text(0.5, 0.05, "VERTICAL ASCENT", transform=ax_info.transAxes,
                                fontsize=10, color='#7fdbff', ha='center', fontfamily='monospace')
        
        def update(frame):
            idx = (frame * 2) % len(self.time)
            
            rocket.set_data([self.traj_east[idx]], [self.traj_up[idx]])
            rocket.set_3d_properties([self.traj_north[idx]])
            
            trail.set_data(self.traj_east[:idx+1], self.traj_up[:idx+1])
            trail.set_3d_properties(self.traj_north[:idx+1])
            
            time_txt.set_text(f"T+ {self.time[idx]:.1f}s")
            value_txts[0].set_text(f"{self.alt_km[idx]:.1f} km")
            value_txts[1].set_text(f"{self.vel_mag[idx]:.0f} m/s")
            value_txts[2].set_text(f"{self.traj_east[idx]:.1f} km")
            value_txts[3].set_text(f"{self.accel_g[idx]:.2f} G")
            value_txts[4].set_text(f"{self.mass[idx]:.0f} t")
            
            t = self.time[idx]
            if t < self.sim.rocket.burn_time:
                engine_txt.set_text("● ENGINE: NOMINAL")
                engine_txt.set_color('#00ff9f')
                if t < 10:
                    phase_txt.set_text("VERTICAL ASCENT")
                elif t < 60:
                    phase_txt.set_text("GRAVITY TURN")
                else:
                    phase_txt.set_text("POWERED FLIGHT")
            else:
                engine_txt.set_text("● ENGINE: CUTOFF")
                engine_txt.set_color('#ff6b6b')
                phase_txt.set_text("COAST PHASE")
            
            return [rocket, trail, time_txt, engine_txt, phase_txt] + value_txts
        
        self.anim = animation.FuncAnimation(self.fig, update, frames=len(self.time)//2,
                                           interval=50, blit=False)
    
    def show(self):
        plt.show()


def run_demo():
    print("=" * 60)
    print("ROCKET ASCENT SIMULATOR")
    print("Module 1: Foundations")
    print("=" * 60)
    
    vehicle = RocketParams()
    sim = RocketSimulator(vehicle)
    sim.run(duration=500.0, dt=0.5)
    
    print("\nLaunching interactive dashboard...")
    print("Use buttons to switch between views.")
    print("-" * 60)
    
    dashboard = AscentDashboard(sim)
    dashboard.show()


if __name__ == "__main__":
    run_demo()
