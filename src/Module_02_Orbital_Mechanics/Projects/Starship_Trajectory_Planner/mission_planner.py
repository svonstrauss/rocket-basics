"""
Starship Trajectory Planner
Module 2: Orbital Mechanics and Mission Design
Project 2

Calculates Hohmann Transfer orbits for Earth-Mars missions.
Visualizes the transfer window, phase angles, and Delta-V requirements.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants (SI Units) ---
G = 6.67430e-11             # m^3 kg^-1 s^-2
M_SUN = 1.989e30            # kg
MU_SUN = G * M_SUN          # m^3 s^-2

# Planet Data (Approximate Mean Values)
# Distance (Semi-major axis in m)
R_EARTH = 1.496e11  # 1 AU
R_MARS = 2.279e11   # 1.52 AU

# Period (s)
T_EARTH = 365.25 * 24 * 3600
T_MARS = 687.0 * 24 * 3600

# Mean Motion (rad/s)
W_EARTH = 2 * np.pi / T_EARTH
W_MARS = 2 * np.pi / T_MARS

@dataclass
class MissionProfile:
    """Holds the calculated parameters for the transfer."""
    departure_name: str
    arrival_name: str
    r1: float
    r2: float
    
    @property
    def transfer_a(self) -> float:
        """Semi-major axis of transfer ellipse."""
        return (self.r1 + self.r2) / 2
    
    @property
    def transfer_time(self) -> float:
        """Time of flight (half period of transfer orbit)."""
        return np.pi * np.sqrt(self.transfer_a**3 / MU_SUN)
    
    @property
    def delta_v1(self) -> float:
        """Burn 1: Departure injection velocity (relative to planet 1 velocity)."""
        v1 = np.sqrt(MU_SUN / self.r1) # Velocity of Planet 1
        v_peri = np.sqrt(MU_SUN * (2/self.r1 - 1/self.transfer_a)) # Velocity at Perihelion of Transfer
        return abs(v_peri - v1)
    
    @property
    def delta_v2(self) -> float:
        """Burn 2: Arrival capture velocity (relative to planet 2 velocity)."""
        v2 = np.sqrt(MU_SUN / self.r2) # Velocity of Planet 2
        v_aphe = np.sqrt(MU_SUN * (2/self.r2 - 1/self.transfer_a)) # Velocity at Aphelion of Transfer
        return abs(v2 - v_aphe)
    
    @property
    def total_delta_v(self) -> float:
        return self.delta_v1 + self.delta_v2
    
    @property
    def phase_angle(self) -> float:
        """Required phase angle (angle Arrival is ahead of Departure) at launch."""
        # Angle covered by Arrival Planet during Transfer Time
        angle_covered = W_MARS * self.transfer_time
        # Arrival needs to be at pi (180 deg) when craft arrives.
        # So at launch, it must be pi - angle_covered.
        return np.pi - angle_covered

class TrajectoryVisualizer:
    def __init__(self, profile: MissionProfile):
        self.profile = profile
        
    def animate_transfer(self):
        """Creates an animation of the Earth-Mars transfer."""
        
        # Time setup
        t_total = self.profile.transfer_time
        # Simulate a bit before launch and a bit after arrival
        t_sim = np.linspace(-0.1 * t_total, t_total * 1.1, 400)
        
        # --- Calculate Positions ---
        
        # 1. Earth Position (Circular approx)
        # Start Earth at angle 0 for simplicity
        theta_earth = W_EARTH * t_sim
        x_earth = self.profile.r1 * np.cos(theta_earth)
        y_earth = self.profile.r1 * np.sin(theta_earth)
        
        # 2. Mars Position (Circular approx)
        # Mars starts at the Phase Angle relative to Earth
        phi = self.profile.phase_angle
        theta_mars = phi + W_MARS * t_sim
        x_mars = self.profile.r2 * np.cos(theta_mars)
        y_mars = self.profile.r2 * np.sin(theta_mars)
        
        # 3. Starship Transfer Orbit
        # Only active during 0 < t < t_total
        # Polar equation of ellipse: r = a(1-e^2) / (1+e cos theta)
        # Here theta corresponds to True Anomaly nu.
        # We need nu as a function of time (Kepler's Equation).
        # For visualization, let's map time directly to angle on the transfer arc for smoothness
        # Transfer arc goes from 0 to pi.
        
        x_ship = []
        y_ship = []
        
        # Transfer Orbit Params
        a_t = self.profile.transfer_a
        # Eccentricity of transfer: ra = a(1+e), rp = a(1-e) -> e = (ra-rp)/(ra+rp)
        e_t = (self.profile.r2 - self.profile.r1) / (self.profile.r2 + self.profile.r1)
        
        for t in t_sim:
            if t < 0:
                # On Earth
                idx = np.searchsorted(t_sim, t)
                x_ship.append(x_earth[min(idx, len(x_earth)-1)])
                y_ship.append(y_earth[min(idx, len(y_earth)-1)])
            elif t > t_total:
                # On Mars
                idx = np.searchsorted(t_sim, t)
                x_ship.append(x_mars[min(idx, len(x_mars)-1)])
                y_ship.append(y_mars[min(idx, len(y_mars)-1)])
            else:
                # In Transit
                # Mean Anomaly M = n * t
                n_t = np.sqrt(MU_SUN / a_t**3)
                M = n_t * t
                
                # Solve Kepler Eq: M = E - e sin E
                # Approx for small e or use Newton
                E = M # First guess
                for _ in range(5):
                    E = M + e_t * np.sin(E)
                
                # True Anomaly nu
                # tan(nu/2) = sqrt((1+e)/(1-e)) * tan(E/2)
                term = np.sqrt((1+e_t)/(1-e_t)) * np.tan(E/2)
                nu = 2 * np.arctan(term)
                
                # Polar to Cartesian
                r = a_t * (1 - e_t**2) / (1 + e_t * np.cos(nu))
                
                # Rotate to match launch point (Earth at angle 0)
                # The perihelion of transfer orbit aligns with Earth at launch
                x = r * np.cos(nu)
                y = r * np.sin(nu)
                x_ship.append(x)
                y_ship.append(y)

        # --- Plotting ---
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # Background color
        fig.patch.set_facecolor('#0b0b10')
        ax.set_facecolor('#0b0b10')
        
        # Set Sun (Glowing effect)
        # Draw multiple circles for glow
        for radius, alpha in [(0.05*self.profile.r1, 0.3), (0.03*self.profile.r1, 0.5), (0.015*self.profile.r1, 1.0)]:
            sun_glow = plt.Circle((0, 0), radius, color='#ffd700', alpha=alpha, zorder=5)
            ax.add_patch(sun_glow)
        
        # Static Orbit Rings (Background)
        theta_ring = np.linspace(0, 2*np.pi, 300)
        
        # Earth Orbit Ring
        ax.plot(self.profile.r1 * np.cos(theta_ring), self.profile.r1 * np.sin(theta_ring), 
                ls='-', color='#4a90e2', alpha=0.2, lw=1)
        
        # Mars Orbit Ring
        ax.plot(self.profile.r2 * np.cos(theta_ring), self.profile.r2 * np.sin(theta_ring), 
                ls='-', color='#ff6b6b', alpha=0.2, lw=1)
        
        # Grid - Radial and Circular
        # Circular faint grids
        for r_frac in [0.5, 1.25, 1.75]:
            r_grid = self.profile.r1 * r_frac
            ax.plot(r_grid * np.cos(theta_ring), r_grid * np.sin(theta_ring), 
                    ls=':', color='gray', alpha=0.05, lw=0.5)
        
        # Radial lines
        for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
            ax.plot([0, 2*self.profile.r2 * np.cos(angle)], [0, 2*self.profile.r2 * np.sin(angle)], 
                    ls=':', color='gray', alpha=0.05, lw=0.5)

        # Initialize Elements
        earth_dot, = ax.plot([], [], 'o', color='#4a90e2', markersize=10, markeredgecolor='white', markeredgewidth=1, label='Earth', zorder=10)
        mars_dot, = ax.plot([], [], 'o', color='#ff6b6b', markersize=8, markeredgecolor='white', markeredgewidth=1, label='Mars', zorder=10)
        ship_dot, = ax.plot([], [], '^', color='white', markersize=8, label='Starship', zorder=15)
        ship_trail, = ax.plot([], [], '-', color='#00ffff', alpha=0.6, lw=1.5, zorder=12) # Cyan trail
        
        # Styling
        max_r = self.profile.r2 * 1.2
        ax.set_xlim(-max_r, max_r)
        ax.set_ylim(-max_r, max_r)
        ax.set_aspect('equal')
        ax.axis('off') # Clean look
        
        # Text Info Panel (Top Left)
        info_text = (f"MISSION PROFILE: {self.profile.departure_name.upper()} -> {self.profile.arrival_name.upper()}\n"
                     f"--------------------------------\n"
                     f"Strategy:      Hohmann Transfer\n"
                     f"Total Delta-V: {self.profile.total_delta_v/1000:.2f} km/s\n"
                     f"Transit Time:  {self.profile.transfer_time/(24*3600):.1f} days\n"
                     f"Phase Angle:   {np.degrees(self.profile.phase_angle):.1f}°")
        
        ax.text(0.02, 0.95, info_text, transform=ax.transAxes, color='#00ff00', 
                family='monospace', fontsize=10, verticalalignment='top',
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='#00ff00', boxstyle='round,pad=0.5'))
        
        # Dynamic Status (Bottom Right)
        status_text = ax.text(0.95, 0.05, "", transform=ax.transAxes, color='white', 
                              family='monospace', fontsize=10, ha='right')
        
        def update(frame):
            # Calculate current time in days
            current_time_days = t_sim[frame] / (24*3600)
            status_str = f"T: {current_time_days:.1f} Days"
            
            if t_sim[frame] < 0:
                status_str += " [PRE-LAUNCH]"
            elif t_sim[frame] > t_total:
                status_str += " [ARRIVAL]"
            else:
                status_str += " [TRANSIT]"
                
            status_text.set_text(status_str)

            # Earth
            earth_dot.set_data([x_earth[frame]], [y_earth[frame]])
            
            # Mars
            mars_dot.set_data([x_mars[frame]], [y_mars[frame]])
            
            # Ship
            ship_dot.set_data([x_ship[frame]], [y_ship[frame]])
            ship_trail.set_data(x_ship[:frame], y_ship[:frame])
            
            return earth_dot, mars_dot, ship_dot, ship_trail, status_text

        anim = animation.FuncAnimation(fig, update, frames=len(t_sim), interval=30, blit=True)
        
        # Legend with custom location
        plt.legend(loc='lower left', facecolor='black', edgecolor='gray', labelcolor='white', framealpha=0.8)
        plt.title("Interplanetary Trajectory Planner", color='white', fontsize=16, pad=20)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Plan Mission: Earth to Mars
    mission = MissionProfile(
        departure_name="Earth",
        arrival_name="Mars",
        r1=R_EARTH,
        r2=R_MARS
    )
    
    print(f"--- {mission.departure_name} to {mission.arrival_name} Mission Plan ---")
    print(f"Delta-V 1 (Injection): {mission.delta_v1:.2f} m/s")
    print(f"Delta-V 2 (Capture):   {mission.delta_v2:.2f} m/s")
    print(f"Total Delta-V:         {mission.total_delta_v:.2f} m/s")
    print(f"Transit Time:          {mission.transfer_time / (24*3600):.2f} days")
    print(f"Required Phase Angle:  {np.degrees(mission.phase_angle):.2f} degrees")
    
    viz = TrajectoryVisualizer(mission)
    viz.animate_transfer()

