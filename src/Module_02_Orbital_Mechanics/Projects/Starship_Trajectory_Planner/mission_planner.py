"""
Mars Mission Simulator
Module 2: Orbital Mechanics and Mission Design

A comprehensive educational tool for understanding Earth-to-Mars missions.
Covers all mission phases with detailed explanations and real physics.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle, FancyArrowPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from dataclasses import dataclass
from typing import Dict, List, Tuple

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

G = 6.67430e-11                  # Gravitational constant (m³/kg/s²)
M_SUN = 1.989e30                 # Sun mass (kg)
M_MARS = 6.39e23                 # Mars mass (kg)
MU_SUN = G * M_SUN               # Sun gravitational parameter
MU_MARS = G * M_MARS             # Mars gravitational parameter

AU = 1.495978707e11              # Astronomical Unit (m)
R_EARTH_ORBIT = 1.0 * AU         # Earth orbital radius
R_MARS_ORBIT = 1.524 * AU        # Mars orbital radius
R_MARS = 3.3895e6                # Mars radius (m)

MARS_ATMO_HEIGHT = 125e3         # Mars atmosphere interface (m)
MARS_RHO_0 = 0.020               # Mars surface density (kg/m³)
MARS_SCALE_HEIGHT = 11100        # Mars atmospheric scale height (m)

T_EARTH = 365.25 * 24 * 3600     # Earth orbital period (s)
T_MARS = 686.98 * 24 * 3600      # Mars orbital period (s)
W_EARTH = 2 * np.pi / T_EARTH    # Earth angular velocity
W_MARS = 2 * np.pi / T_MARS      # Mars angular velocity

# =============================================================================
# MISSION DATABASE
# =============================================================================

MARS_MISSIONS = {
    'Perseverance': {'agency': 'NASA', 'year': 2020, 'type': 'Rover', 'mass': 1025, 
                     'transit': 203, 'color': '#00d4ff', 'success': True},
    'Curiosity': {'agency': 'NASA', 'year': 2011, 'type': 'Rover', 'mass': 899, 
                  'transit': 254, 'color': '#ffa500', 'success': True},
    'InSight': {'agency': 'NASA', 'year': 2018, 'type': 'Lander', 'mass': 358, 
                'transit': 205, 'color': '#9b59b6', 'success': True},
    'Tianwen-1': {'agency': 'CNSA', 'year': 2020, 'type': 'Orbiter+Rover', 'mass': 5000, 
                  'transit': 295, 'color': '#e74c3c', 'success': True},
    'Mars Express': {'agency': 'ESA', 'year': 2003, 'type': 'Orbiter', 'mass': 1120, 
                     'transit': 206, 'color': '#2ecc71', 'success': True},
    'Mangalyaan': {'agency': 'ISRO', 'year': 2013, 'type': 'Orbiter', 'mass': 1337, 
                   'transit': 300, 'color': '#f39c12', 'success': True},
    'Hope': {'agency': 'UAE', 'year': 2020, 'type': 'Orbiter', 'mass': 1350, 
             'transit': 201, 'color': '#e91e63', 'success': True},
}

# =============================================================================
# PHYSICS CALCULATIONS
# =============================================================================

@dataclass
class HohmannTransfer:
    """Hohmann transfer orbit between two circular orbits."""
    r1: float  # Inner orbit radius
    r2: float  # Outer orbit radius
    mu: float  # Central body gravitational parameter
    
    @property
    def semi_major_axis(self) -> float:
        return (self.r1 + self.r2) / 2
    
    @property
    def eccentricity(self) -> float:
        return (self.r2 - self.r1) / (self.r2 + self.r1)
    
    @property
    def transfer_time(self) -> float:
        return np.pi * np.sqrt(self.semi_major_axis**3 / self.mu)
    
    @property
    def delta_v_departure(self) -> float:
        v_circular = np.sqrt(self.mu / self.r1)
        v_transfer = np.sqrt(self.mu * (2/self.r1 - 1/self.semi_major_axis))
        return abs(v_transfer - v_circular)
    
    @property
    def delta_v_arrival(self) -> float:
        v_circular = np.sqrt(self.mu / self.r2)
        v_transfer = np.sqrt(self.mu * (2/self.r2 - 1/self.semi_major_axis))
        return abs(v_circular - v_transfer)
    
    @property
    def total_delta_v(self) -> float:
        return self.delta_v_departure + self.delta_v_arrival
    
    @property
    def phase_angle(self) -> float:
        return np.pi - W_MARS * self.transfer_time


def compute_trajectory(transfer: HohmannTransfer, n_points: int = 400) -> Dict:
    """Compute transfer trajectory positions and velocities."""
    t_total = transfer.transfer_time
    t = np.linspace(0, t_total, n_points)
    
    # Earth orbit
    theta_earth = W_EARTH * t
    earth_x = np.cos(theta_earth)
    earth_y = np.sin(theta_earth)
    
    # Mars orbit (starts at phase angle)
    phase = transfer.phase_angle
    theta_mars = phase + W_MARS * t
    mars_x = 1.524 * np.cos(theta_mars)
    mars_y = 1.524 * np.sin(theta_mars)
    
    # Spacecraft on transfer ellipse
    a = transfer.semi_major_axis
    e = transfer.eccentricity
    n = np.sqrt(transfer.mu / a**3)
    
    ship_x, ship_y, ship_v, ship_r = [], [], [], []
    
    for ti in t:
        M = n * ti
        E = M
        for _ in range(15):
            E = M + e * np.sin(E)
        
        nu = 2 * np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
        r = a * (1 - e**2) / (1 + e * np.cos(nu))
        
        ship_x.append(r * np.cos(nu) / AU)
        ship_y.append(r * np.sin(nu) / AU)
        ship_r.append(r / AU)
        ship_v.append(np.sqrt(transfer.mu * (2/r - 1/a)) / 1000)
    
    return {
        'time': t, 'days': t / 86400,
        'earth_x': earth_x, 'earth_y': earth_y,
        'mars_x': mars_x, 'mars_y': mars_y,
        'ship_x': np.array(ship_x), 'ship_y': np.array(ship_y),
        'ship_v': np.array(ship_v), 'ship_r': np.array(ship_r)
    }


def simulate_edl(v0: float = 5500, angle: float = -12, mass: float = 1000,
                 cd: float = 1.5, area: float = 15) -> Dict:
    """Simulate Mars Entry, Descent, and Landing."""
    h, v, gamma = MARS_ATMO_HEIGHT, v0, np.radians(angle)
    dt = 0.1
    
    data = {'time': [0], 'alt': [h/1000], 'vel': [v], 'g_load': [0], 
            'heat': [0], 'mach': [0], 'dyn_press': [0]}
    t = 0
    
    while h > 0 and v > 50 and t < 500:
        rho = MARS_RHO_0 * np.exp(-h / MARS_SCALE_HEIGHT)
        g = MU_MARS / (R_MARS + h)**2
        q = 0.5 * rho * v**2
        drag = q * cd * area / mass
        
        # Heat flux (Sutton-Graves)
        heat = 1.83e-4 * np.sqrt(rho) * v**3 / 1e6
        
        # Mars speed of sound ~240 m/s
        mach = v / 240
        
        dv = -drag - g * np.sin(gamma)
        dgamma = (v/(R_MARS+h) - g/v) * np.cos(gamma)
        dh = v * np.sin(gamma)
        
        h += dh * dt
        v += dv * dt
        gamma += dgamma * dt
        t += dt
        
        if t > data['time'][-1] + 0.3:
            data['time'].append(t)
            data['alt'].append(max(0, h/1000))
            data['vel'].append(v)
            data['g_load'].append(abs(dv) / 9.81)
            data['heat'].append(heat)
            data['mach'].append(mach)
            data['dyn_press'].append(q / 1000)  # kPa
    
    return {k: np.array(v) for k, v in data.items()}


def compute_porkchop() -> Dict:
    """Compute porkchop plot data."""
    launch = np.linspace(0, 400, 50)
    arrival = np.linspace(180, 550, 50)
    X, Y = np.meshgrid(launch, arrival)
    Z = np.full_like(X, np.nan)
    
    for i, arr in enumerate(arrival):
        for j, lnch in enumerate(launch):
            dt = (arr - lnch) * 86400
            if dt < 120 * 86400:
                continue
            
            # Simplified Lambert approximation
            t_hohmann = np.pi * np.sqrt(((R_EARTH_ORBIT + R_MARS_ORBIT)/2)**3 / MU_SUN)
            ratio = dt / t_hohmann
            
            base = 5.6
            penalty = 1200 * (np.log(max(ratio, 0.4))**2)
            Z[i, j] = base + penalty / 1000
    
    return {'X': X, 'Y': Y, 'Z': Z, 'launch': launch, 'arrival': arrival}


# =============================================================================
# STYLING
# =============================================================================

def style_axis(ax, title="", xlabel="", ylabel="", fontsize=11):
    """Apply educational dark theme."""
    ax.set_facecolor('#080812')
    ax.tick_params(colors='#8888aa', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#303050')
    ax.grid(True, alpha=0.15, color='#4444aa', linestyle='-', linewidth=0.5)
    
    if title:
        ax.set_title(title, color='#00d4ff', fontsize=fontsize, fontweight='bold', pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, color='#aaaacc', fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color='#aaaacc', fontsize=10)


def draw_info_box(ax, x, y, text, width=0.3, color='#00ff88'):
    """Draw an info box with educational content."""
    box = FancyBboxPatch((x, y), width, 0.15, boxstyle="round,pad=0.02",
                         facecolor='#0a0a18', edgecolor=color, linewidth=1.5,
                         transform=ax.transAxes, zorder=100)
    ax.add_patch(box)
    ax.text(x + width/2, y + 0.075, text, transform=ax.transAxes,
            color=color, fontsize=9, ha='center', va='center', fontfamily='monospace')


# =============================================================================
# MAIN SIMULATOR CLASS
# =============================================================================

class MarsMissionSimulator:
    """Educational Mars Mission Simulator with detailed explanations."""
    
    def __init__(self):
        self.view = 0
        self.views = ['OVERVIEW', 'TRANSIT', 'EDL', 'MISSIONS', 'WINDOWS']
        self.anim = None
        self.transit_anim = None
        
        print("=" * 50)
        print("  MARS MISSION SIMULATOR")
        print("  Educational Edition")
        print("=" * 50)
        print("\nComputing mission data...")
        
        # Pre-compute
        self.transfer = HohmannTransfer(R_EARTH_ORBIT, R_MARS_ORBIT, MU_SUN)
        self.traj = compute_trajectory(self.transfer)
        self.edl = simulate_edl()
        self.porkchop = compute_porkchop()
        
        print("Ready!\n")
        
        # Setup
        self.fig = plt.figure(figsize=(17, 10))
        self.fig.patch.set_facecolor('#04040a')
        self._setup_nav()
        self._draw()
    
    def _setup_nav(self):
        """Setup navigation."""
        colors = ['#0a4060', '#0a6040', '#600a40', '#606000', '#400a60']
        self.btn_axes = []
        self.buttons = []
        
        for i, name in enumerate(self.views):
            ax = self.fig.add_axes([0.06 + i*0.175, 0.012, 0.16, 0.045])
            btn = Button(ax, name, color=colors[i], hovercolor='#00aaff')
            btn.label.set_color('white')
            btn.label.set_fontsize(11)
            btn.label.set_fontweight('bold')
            btn.on_clicked(lambda e, idx=i: self._switch(idx))
            self.btn_axes.append(ax)
            self.buttons.append(btn)
    
    def _switch(self, idx):
        """Switch view."""
        if self.anim:
            self.anim.event_source.stop()
            self.anim = None
        if self.transit_anim:
            self.transit_anim.event_source.stop()
            self.transit_anim = None
        
        self.view = idx
        self._clear()
        self._draw()
        self.fig.canvas.draw_idle()
    
    def _clear(self):
        """Clear axes."""
        for ax in self.fig.axes[:]:
            if ax not in self.btn_axes:
                ax.remove()
    
    def _draw(self):
        """Draw current view."""
        [self._draw_overview, self._draw_transit, self._draw_edl,
         self._draw_missions, self._draw_windows][self.view]()
    
    # =========================================================================
    # VIEW 1: OVERVIEW (Animated orbital transfer)
    # =========================================================================
    
    def _draw_overview(self):
        """Animated orbital transfer visualization."""
        ax = self.fig.add_axes([0.02, 0.08, 0.58, 0.88])
        ax.set_facecolor('#04040a')
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Orbit paths
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), color='#2255aa', alpha=0.5, lw=2,
                label='Earth Orbit (1 AU)')
        ax.plot(1.524*np.cos(theta), 1.524*np.sin(theta), color='#aa3333', alpha=0.5, lw=2,
                label='Mars Orbit (1.52 AU)')
        
        # Transfer ellipse
        a = self.transfer.semi_major_axis / AU
        e = self.transfer.eccentricity
        b = a * np.sqrt(1 - e**2)
        c = a * e
        t_e = np.linspace(0, np.pi, 100)
        ax.plot(a*np.cos(t_e) - c, b*np.sin(t_e), '--', color='#00ffaa', alpha=0.7, lw=2,
                label='Transfer Orbit')
        
        # Sun
        for r, alpha in [(0.12, 0.15), (0.08, 0.3), (0.05, 0.6), (0.03, 1.0)]:
            ax.add_patch(Circle((0, 0), r, color='#ffdd00', alpha=alpha, zorder=5))
        ax.text(0, -0.2, 'SUN', color='#ffdd00', fontsize=10, ha='center', fontweight='bold')
        
        # Animated elements
        self.earth_dot, = ax.plot([], [], 'o', color='#4488ff', ms=16, mec='white', mew=2, zorder=10)
        self.mars_dot, = ax.plot([], [], 'o', color='#ff6644', ms=14, mec='white', mew=2, zorder=10)
        self.ship_dot, = ax.plot([], [], '^', color='#00ffff', ms=12, mec='white', mew=1.5, zorder=15)
        self.ship_trail, = ax.plot([], [], '-', color='#00ffff', alpha=0.7, lw=2.5, zorder=8)
        
        self.earth_lbl = ax.text(0, 0, '', color='#4488ff', fontsize=11, ha='center', fontweight='bold')
        self.mars_lbl = ax.text(0, 0, '', color='#ff6644', fontsize=11, ha='center', fontweight='bold')
        
        ax.set_xlim(-2.1, 2.1)
        ax.set_ylim(-1.0, 2.0)
        ax.legend(loc='lower left', facecolor='#0a0a18', edgecolor='#333366',
                  labelcolor='white', fontsize=10)
        
        # Status panel
        self.status = ax.text(0.02, 0.98, '', transform=ax.transAxes, color='#00ff88',
                              fontsize=12, fontfamily='monospace', va='top',
                              bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a18',
                                        edgecolor='#00ff88', alpha=0.95))
        
        # Info panel
        self._draw_overview_info()
        
        # Start animation
        self.anim = animation.FuncAnimation(
            self.fig, self._update_overview, frames=len(self.traj['time']),
            interval=30, blit=False, repeat=True
        )
    
    def _draw_overview_info(self):
        """Draw educational info panel for overview."""
        ax = self.fig.add_axes([0.62, 0.08, 0.36, 0.88])
        ax.set_facecolor('#080812')
        ax.axis('off')
        
        days = self.transfer.transfer_time / 86400
        dv1 = self.transfer.delta_v_departure / 1000
        dv2 = self.transfer.delta_v_arrival / 1000
        phase = np.degrees(self.transfer.phase_angle)
        
        info = f"""
┌─────────────────────────────────────┐
│     HOHMANN TRANSFER EXPLAINED      │
└─────────────────────────────────────┘

WHAT IS A HOHMANN TRANSFER?
───────────────────────────────────────
A Hohmann transfer is the most fuel-
efficient way to travel between two
circular orbits. It uses an elliptical
path that touches both orbits.

THE TWO BURNS
───────────────────────────────────────
① TMI (Trans-Mars Injection)
   At Earth, we accelerate to enter
   the transfer ellipse.
   ΔV = {dv1:.2f} km/s

② MOI (Mars Orbit Insertion)
   At Mars, we slow down to match
   Mars' orbital velocity.
   ΔV = {dv2:.2f} km/s

   TOTAL ΔV = {dv1+dv2:.2f} km/s

TIMING IS EVERYTHING
───────────────────────────────────────
Phase Angle: {phase:.1f}°

Mars must be {phase:.1f}° ahead of Earth
when we launch. Why? Because Mars
moves slower than Earth - we need
Mars to "catch up" to where our
spacecraft will arrive!

MISSION DURATION
───────────────────────────────────────
Transit Time: {days:.0f} days (~{days/30:.1f} months)

This is roughly half the period of
the transfer ellipse.

WHY NOT FLY STRAIGHT?
───────────────────────────────────────
Space travel isn't about distance -
it's about ENERGY. A "straight line"
would require enormous fuel to fight
the Sun's gravity the whole way!
"""
        ax.text(0.02, 0.99, info, transform=ax.transAxes, color='#00ff88',
                fontsize=10.5, fontfamily='monospace', va='top')
    
    def _update_overview(self, frame):
        """Update orbital animation."""
        ex, ey = self.traj['earth_x'][frame], self.traj['earth_y'][frame]
        mx, my = self.traj['mars_x'][frame], self.traj['mars_y'][frame]
        sx, sy = self.traj['ship_x'][frame], self.traj['ship_y'][frame]
        
        self.earth_dot.set_data([ex], [ey])
        self.mars_dot.set_data([mx], [my])
        self.ship_dot.set_data([sx], [sy])
        
        trail_start = max(0, frame - 80)
        self.ship_trail.set_data(self.traj['ship_x'][trail_start:frame+1],
                                  self.traj['ship_y'][trail_start:frame+1])
        
        self.earth_lbl.set_position((ex, ey - 0.15))
        self.earth_lbl.set_text('EARTH')
        self.mars_lbl.set_position((mx, my + 0.18))
        self.mars_lbl.set_text('MARS')
        
        day = self.traj['days'][frame]
        vel = self.traj['ship_v'][frame]
        dist = self.traj['ship_r'][frame]
        progress = frame / len(self.traj['time']) * 100
        total = self.traj['days'][-1]
        
        phase = "DEPARTURE" if progress < 5 else "ARRIVAL" if progress > 95 else "CRUISE"
        
        self.status.set_text(f"""╔═══════════════════════════╗
║  MISSION DAY {day:>5.0f} / {total:.0f}  ║
╠═══════════════════════════╣
║  Progress:  {progress:>5.1f}%        ║
║  Velocity:  {vel:>5.1f} km/s     ║
║  Distance:  {dist:>5.2f} AU       ║
║  Phase:     {phase:<12}  ║
╚═══════════════════════════╝""")
        
        return self.earth_dot, self.mars_dot, self.ship_dot
    
    # =========================================================================
    # VIEW 2: TRANSIT (Animated graphs with explanations)
    # =========================================================================
    
    def _draw_transit(self):
        """Animated transit analysis with educational content."""
        # Velocity plot
        ax1 = self.fig.add_axes([0.06, 0.56, 0.45, 0.36])
        style_axis(ax1, 'SPACECRAFT VELOCITY DURING TRANSIT', 'Mission Day', 'Velocity (km/s)')
        
        days = self.traj['days']
        vel = self.traj['ship_v']
        
        ax1.fill_between(days, 20, vel, alpha=0.25, color='#00ffff')
        ax1.plot(days, vel, color='#00ffff', lw=2.5, label='Spacecraft')
        
        v_earth = np.sqrt(MU_SUN / R_EARTH_ORBIT) / 1000
        v_mars = np.sqrt(MU_SUN / R_MARS_ORBIT) / 1000
        ax1.axhline(v_earth, color='#4488ff', ls='--', lw=2, label=f'Earth: {v_earth:.1f} km/s')
        ax1.axhline(v_mars, color='#ff6644', ls='--', lw=2, label=f'Mars: {v_mars:.1f} km/s')
        
        ax1.legend(loc='upper right', facecolor='#0a0a18', edgecolor='#333366',
                   labelcolor='white', fontsize=9)
        ax1.set_xlim(0, days[-1])
        ax1.set_ylim(20, 35)
        
        # Animated marker
        self.vel_marker, = ax1.plot([], [], 'o', color='#ffffff', ms=12, mec='#00ffff', mew=2, zorder=20)
        self.vel_text = ax1.text(0, 0, '', color='white', fontsize=10, fontweight='bold')
        
        # Distance plot
        ax2 = self.fig.add_axes([0.06, 0.12, 0.45, 0.36])
        style_axis(ax2, 'DISTANCE FROM THE SUN', 'Mission Day', 'Distance (AU)')
        
        dist = self.traj['ship_r']
        ax2.fill_between(days, 0.9, dist, alpha=0.25, color='#ffaa00')
        ax2.plot(days, dist, color='#ffaa00', lw=2.5, label='Spacecraft')
        ax2.axhline(1.0, color='#4488ff', ls='--', lw=2, label='Earth orbit (1 AU)')
        ax2.axhline(1.524, color='#ff6644', ls='--', lw=2, label='Mars orbit (1.52 AU)')
        
        ax2.legend(loc='lower right', facecolor='#0a0a18', edgecolor='#333366',
                   labelcolor='white', fontsize=9)
        ax2.set_xlim(0, days[-1])
        ax2.set_ylim(0.9, 1.65)
        
        # Animated marker
        self.dist_marker, = ax2.plot([], [], 'o', color='#ffffff', ms=12, mec='#ffaa00', mew=2, zorder=20)
        self.dist_text = ax2.text(0, 0, '', color='white', fontsize=10, fontweight='bold')
        
        # Educational info panel
        ax3 = self.fig.add_axes([0.54, 0.08, 0.44, 0.88])
        ax3.set_facecolor('#080812')
        ax3.axis('off')
        
        info = f"""
┌─────────────────────────────────────────┐
│    UNDERSTANDING THE TRANSIT PHASE      │
└─────────────────────────────────────────┘

WHY DOES VELOCITY CHANGE?
───────────────────────────────────────────
The spacecraft is in FREE FALL around the
Sun the entire time - no engines firing!

• NEAR EARTH (1 AU): Moving fast because
  we're deep in the Sun's gravity well.
  Speed ≈ 32.7 km/s at departure

• NEAR MARS (1.52 AU): Moving slower
  because we've climbed "uphill" against
  the Sun's gravity.
  Speed ≈ 21.5 km/s at arrival

This is the VIS-VIVA EQUATION in action:
  v² = μ(2/r - 1/a)

WHERE DOES THE ENERGY GO?
───────────────────────────────────────────
As we move away from the Sun:
  • Kinetic energy (speed) DECREASES
  • Potential energy (height) INCREASES
  • Total energy stays CONSTANT

It's like rolling a ball up a hill - it
slows down as it gains height!

WHAT HAPPENS DURING THE 259-DAY CRUISE?
───────────────────────────────────────────
Day 1-7:    Post-TMI checkout
Day 7-30:   Trajectory corrections (TCMs)
Day 30-230: Deep space cruise
            • Minimal activity
            • Instrument calibration
            • Science observations
Day 230+:   Mars approach
            • Final targeting
            • Prepare for EDL

COMMUNICATION
───────────────────────────────────────────
Signal delay: 4 min (closest) to 24 min
The spacecraft must operate AUTONOMOUSLY
during critical events like landing!
"""
        ax3.text(0.02, 0.99, info, transform=ax3.transAxes, color='#00ff88',
                 fontsize=10.5, fontfamily='monospace', va='top')
        
        # Store axes for animation
        self.transit_ax1 = ax1
        self.transit_ax2 = ax2
        
        # Start animation
        self.transit_anim = animation.FuncAnimation(
            self.fig, self._update_transit, frames=len(days),
            interval=40, blit=False, repeat=True
        )
    
    def _update_transit(self, frame):
        """Update transit animation."""
        day = self.traj['days'][frame]
        vel = self.traj['ship_v'][frame]
        dist = self.traj['ship_r'][frame]
        
        self.vel_marker.set_data([day], [vel])
        self.vel_text.set_position((day + 5, vel + 0.5))
        self.vel_text.set_text(f'{vel:.1f} km/s')
        
        self.dist_marker.set_data([day], [dist])
        self.dist_text.set_position((day + 5, dist + 0.03))
        self.dist_text.set_text(f'{dist:.2f} AU')
        
        return self.vel_marker, self.dist_marker
    
    # =========================================================================
    # VIEW 3: EDL (Entry, Descent, Landing with full explanations)
    # =========================================================================
    
    def _draw_edl(self):
        """EDL simulation with comprehensive educational legends."""
        t = self.edl['time']
        peak_g = max(self.edl['g_load'])
        peak_h = max(self.edl['heat'])
        
        # ALTITUDE
        ax1 = self.fig.add_axes([0.05, 0.55, 0.28, 0.34])
        style_axis(ax1, 'ALTITUDE', 'Time (s)', 'Altitude (km)', fontsize=11)
        ax1.fill_between(t, 0, self.edl['alt'], alpha=0.3, color='#ff6644')
        ax1.plot(t, self.edl['alt'], color='#ff6644', lw=2.5)
        ax1.set_xlim(0, t[-1])
        ax1.set_ylim(0, 130)
        ax1.axhline(125, color='#ffff00', ls=':', alpha=0.7)
        ax1.axhline(10, color='#00ff00', ls=':', alpha=0.7)
        
        # VELOCITY
        ax2 = self.fig.add_axes([0.36, 0.55, 0.28, 0.34])
        style_axis(ax2, 'VELOCITY', 'Time (s)', 'Velocity (m/s)', fontsize=11)
        ax2.fill_between(t, 0, self.edl['vel'], alpha=0.3, color='#00ffff')
        ax2.plot(t, self.edl['vel'], color='#00ffff', lw=2.5)
        ax2.set_xlim(0, t[-1])
        
        # G-FORCE
        ax3 = self.fig.add_axes([0.05, 0.12, 0.28, 0.34])
        style_axis(ax3, 'G-FORCE', 'Time (s)', "G's", fontsize=11)
        ax3.fill_between(t, 0, self.edl['g_load'], alpha=0.3, color='#ffaa00')
        ax3.plot(t, self.edl['g_load'], color='#ffaa00', lw=2.5)
        peak_t_g = t[np.argmax(self.edl['g_load'])]
        ax3.plot(peak_t_g, peak_g, 'o', color='#ff0000', ms=8, zorder=10)
        ax3.text(peak_t_g + 15, peak_g - 0.8, f'Peak: {peak_g:.1f}g', 
                 color='#ff4444', fontsize=9, fontweight='bold')
        ax3.axhline(3, color='#00ff00', ls=':', alpha=0.5)
        ax3.set_xlim(0, t[-1])
        
        # HEAT FLUX
        ax4 = self.fig.add_axes([0.36, 0.12, 0.28, 0.34])
        style_axis(ax4, 'HEAT FLUX', 'Time (s)', 'MW/m²', fontsize=11)
        ax4.fill_between(t, 0, self.edl['heat'], alpha=0.3, color='#ff44aa')
        ax4.plot(t, self.edl['heat'], color='#ff44aa', lw=2.5)
        peak_t_h = t[np.argmax(self.edl['heat'])]
        ax4.plot(peak_t_h, peak_h, 'o', color='#ff0000', ms=8, zorder=10)
        ax4.text(peak_t_h + 15, peak_h - 0.03, f'Peak: {peak_h:.2f}', 
                 color='#ff4444', fontsize=9, fontweight='bold')
        ax4.set_xlim(0, t[-1])
        
        # EXPLANATION PANEL
        ax5 = self.fig.add_axes([0.67, 0.08, 0.31, 0.86])
        ax5.set_facecolor('#080812')
        ax5.axis('off')
        
        info = f"""EDL: "7 MINUTES OF TERROR"
================================

WHAT THE GRAPHS SHOW:

ALTITUDE (Top Left)
  Height above Mars surface
  Entry: 125 km (yellow line)
  Parachute: 10 km (green line)

VELOCITY (Top Right)  
  Entry speed: 5,500 m/s
  (That's 12,000 mph!)
  Must slow to ~0 for landing

G-FORCE (Bottom Left)
  Deceleration in Earth g's
  Peak: {peak_g:.1f}g (spacecraft
  feels {peak_g:.1f}x its weight!)
  Green line = human limit (~3g)

HEAT FLUX (Bottom Right)
  Heat hitting the shield
  Peak: {peak_h:.2f} MW/m²
  Like {int(peak_h*100)} ovens per m²!

--------------------------------
WHY IS THIS SO HARD?

* Mars air is 100x thinner than
  Earth's = less braking power
* But still causes extreme heat
* Only ~50% of Mars landings
  have succeeded!

THE EDL SEQUENCE:
1. Atmosphere entry (5+ km/s)
2. Peak heating & G-force
3. Supersonic parachute deploy
4. Heat shield jettison
5. Radar locks onto ground
6. Retrorockets fire
7. Touchdown!

Total time: ~7 minutes
No human control possible
(signal delay: 4-24 min)"""
        ax5.text(0.02, 0.98, info, transform=ax5.transAxes, color='#00ff88',
                 fontsize=9.5, fontfamily='monospace', va='top')
    
    # =========================================================================
    # VIEW 4: MISSIONS (Scatter plot comparison)
    # =========================================================================
    
    def _draw_missions(self):
        """Mission comparison scatter plot."""
        ax = self.fig.add_axes([0.06, 0.10, 0.52, 0.82])
        style_axis(ax, 'MARS MISSION COMPARISON', 'Transit Time (days)', 'Spacecraft Mass (kg)')
        
        for name, data in MARS_MISSIONS.items():
            ax.scatter(data['transit'], data['mass'], s=200, c=data['color'], 
                       alpha=0.85, edgecolors='white', linewidth=1.5, zorder=10,
                       label=f"{name} ({data['agency']})")
        
        ax.set_yscale('log')
        ax.set_xlim(150, 350)
        ax.set_ylim(100, 200000)
        
        ax.legend(loc='upper right', facecolor='#0a0a18', edgecolor='#333366', 
                  labelcolor='white', fontsize=8, framealpha=0.95)
        
        # Info panel - COMPACT to avoid overflow
        ax2 = self.fig.add_axes([0.60, 0.10, 0.38, 0.82])
        ax2.set_facecolor('#080812')
        ax2.axis('off')
        
        info = """HISTORICAL MISSIONS
==============================

SPACE AGENCIES

NASA (USA)
  Most Mars missions
  Rovers: Curiosity, Perseverance

CNSA (China)
  Tianwen-1 (2020)
  First: orbit + land + rove

ESA (Europe)
  Mars Express (2003)
  ExoMars program

ISRO (India)
  Mangalyaan (2013)
  First attempt success!

UAE
  Hope orbiter (2020)
  Weather observation

==============================
MISSION TYPES

FLYBY
  Quick pass, limited data

ORBITER
  Long-term observation
  Global mapping

LANDER
  Surface science
  Seismic, weather

ROVER
  Mobile exploration
  Rock analysis

==============================
FUTURE

SpaceX Starship
  Target: Late 2020s
  First crewed mission
  100+ metric tons"""
        ax2.text(0.02, 0.98, info, transform=ax2.transAxes, color='#00ff88',
                 fontsize=9, fontfamily='monospace', va='top')
    
    # =========================================================================
    # VIEW 5: WINDOWS (Simplified porkchop with visual explanation)
    # =========================================================================
    
    def _draw_windows(self):
        """Launch windows with beginner-friendly explanation."""
        # Main plot
        ax = self.fig.add_axes([0.05, 0.10, 0.45, 0.82])
        style_axis(ax, 'LAUNCH WINDOWS TO MARS', 
                   'Launch (days from Jan 1)', 'Arrival (days from Jan 1)')
        
        levels = np.linspace(5.5, 9, 8)
        cp = ax.contourf(self.porkchop['X'], self.porkchop['Y'], 
                         self.porkchop['Z'], levels=levels, cmap='RdYlGn_r', extend='max')
        
        cbar = self.fig.colorbar(cp, ax=ax, shrink=0.7, pad=0.02)
        cbar.set_label('Fuel (km/s)', color='white', fontsize=9)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        # Find optimal
        min_idx = np.unravel_index(np.nanargmin(self.porkchop['Z']), self.porkchop['Z'].shape)
        opt_launch = self.porkchop['launch'][min_idx[1]]
        opt_arrive = self.porkchop['arrival'][min_idx[0]]
        opt_dv = self.porkchop['Z'][min_idx]
        transit = opt_arrive - opt_launch
        
        ax.plot(opt_launch, opt_arrive, '*', color='#00ff00', ms=20,
                mec='white', mew=2, zorder=20)
        ax.text(opt_launch + 20, opt_arrive, 'BEST', color='#00ff00', 
                fontsize=10, fontweight='bold')
        
        # Visual explanation - orbital diagram
        ax2 = self.fig.add_axes([0.52, 0.50, 0.46, 0.44])
        ax2.set_facecolor('#080812')
        ax2.axis('off')
        ax2.set_xlim(-1.6, 1.6)
        ax2.set_ylim(-1.2, 1.2)
        ax2.set_aspect('equal')
        
        theta = np.linspace(0, 2*np.pi, 100)
        ax2.plot(0.5*np.cos(theta), 0.5*np.sin(theta), '-', color='#4488ff', lw=2, alpha=0.5)
        ax2.plot(1.0*np.cos(theta), 1.0*np.sin(theta), '-', color='#ff6644', lw=2, alpha=0.5)
        
        ax2.add_patch(Circle((0, 0), 0.12, color='#ffdd00', zorder=10))
        ax2.add_patch(Circle((0.5, 0), 0.06, color='#4488ff', zorder=10))
        ax2.add_patch(Circle((0.7, 0.7), 0.07, color='#ff6644', zorder=10))
        
        ax2.annotate('', xy=(0.6, 0.6), xytext=(0.5, 0.08),
                     arrowprops=dict(arrowstyle='->', color='#00ff00', lw=2.5))
        
        ax2.text(0.5, -0.18, 'Earth', color='#4488ff', fontsize=9, ha='center')
        ax2.text(0.7, 0.88, 'Mars', color='#ff6644', fontsize=9, ha='center')
        ax2.text(0, -1.0, 'Correct alignment = efficient path', 
                 color='#00ff00', fontsize=9, ha='center', fontweight='bold')
        
        # Explanation panel - COMPACT
        ax3 = self.fig.add_axes([0.52, 0.10, 0.46, 0.38])
        ax3.set_facecolor('#080812')
        ax3.axis('off')
        
        info = f"""HOW TO READ THIS CHART
================================
X-axis = Launch date
Y-axis = Arrival date
Color  = Fuel required

GREEN = Efficient | RED = Costly

OPTIMAL WINDOW
================================
Launch: Day {opt_launch:.0f}  |  Arrive: Day {opt_arrive:.0f}
Transit: {transit:.0f} days  |  Fuel: {opt_dv:.1f} km/s

WHY LIMITED DATES?
================================
Earth & Mars orbit at different
speeds. Efficient transfers only
work when planets align properly.

Windows open every ~26 MONTHS.
Miss one? Wait 2+ years!"""
        ax3.text(0.02, 0.95, info, transform=ax3.transAxes, color='#00ff88',
                 fontsize=9.5, fontfamily='monospace', va='top')
    
    def show(self):
        plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    sim = MarsMissionSimulator()
    sim.show()


if __name__ == "__main__":
    main()
