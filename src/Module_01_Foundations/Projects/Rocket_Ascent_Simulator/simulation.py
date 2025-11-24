"""
Rocket Ascent Simulator
Module 1: Foundations in Math, Physics, and Computation
Project 1

A 3D simulation of a rocket ascent considering thrust, gravity, variable atmospheric drag,
and mass depletion. Implements RK4 numerical integration for high precision.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass

# --- Constants ---
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_EARTH = 5.972e24  # Mass of Earth (kg)
R_EARTH = 6371000  # Radius of Earth (m)
SEA_LEVEL_DENSITY = 1.225  # kg/m^3
SCALE_HEIGHT = 8500  # m (approx scale height for Earth atmosphere)

@dataclass
class RocketParams:
    """Physical parameters defining the rocket vehicle (based roughly on a Falcon 9 / Starship hybrid for demo)."""
    wet_mass: float = 500000.0    # kg (Launch mass)
    dry_mass: float = 25000.0     # kg (Empty mass)
    thrust: float = 7600000.0     # N (Mean thrust, e.g., Merlin/Raptor cluster)
    isp: float = 300.0            # s (Specific Impulse)
    drag_coeff: float = 0.75      # Dimensionless (Cd)
    area: float = 10.0            # m^2 (Cross-sectional area)
    burn_time: float = 160.0      # s (Time until engine cutoff)

class Environment:
    """Handles environmental physics like gravity and atmosphere."""
    
    @staticmethod
    def get_gravity_acceleration(position: np.ndarray) -> np.ndarray:
        """
        Calculates gravitational acceleration vector at a given 3D position.
        Formula: g = -(GM / r^3) * r_vec
        """
        r_mag = np.linalg.norm(position)
        if r_mag == 0:
            return np.zeros(3)
        
        # F_g = G * M * m / r^2, so a_g = G * M / r^2
        # Vector direction is -r_hat.
        magnitude = (G * M_EARTH) / (r_mag**2)
        direction = -position / r_mag
        return direction * magnitude

    @staticmethod
    def get_air_density(altitude: float) -> float:
        """
        Calculates air density using the barometric formula approximation.
        rho = rho_0 * exp(-h / H)
        """
        if altitude < 0:
            return SEA_LEVEL_DENSITY
        return SEA_LEVEL_DENSITY * np.exp(-altitude / SCALE_HEIGHT)

class RocketSimulator:
    """
    Simulates the rocket's flight using Runge-Kutta 4 (RK4) integration.
    State Vector: [x, y, z, vx, vy, vz, mass]
    """
    
    def __init__(self, rocket: RocketParams):
        self.rocket = rocket
        self.history: Dict[str, List[float]] = {
            'time': [], 'x': [], 'y': [], 'z': [],
            'vx': [], 'vy': [], 'vz': [],
            'altitude': [], 'mass': [], 'dynamic_pressure': []
        }

    def _derivatives(self, t: float, state: np.ndarray) -> np.ndarray:
        """
        Computes the derivative of the state vector (dy/dt) for RK4.
        State: [rx, ry, rz, vx, vy, vz, m]
        Derivative: [vx, vy, vz, ax, ay, az, dm/dt]
        """
        # Unpack state
        r = state[:3]  # Position vector relative to Earth center
        v = state[3:6] # Velocity vector
        m = state[6]   # Current mass

        # 1. Altitude calculations
        r_mag = np.linalg.norm(r)
        altitude = r_mag - R_EARTH
        
        # 2. Environmental Forces
        # Gravity
        a_gravity = Environment.get_gravity_acceleration(r)
        
        # Atmosphere
        rho = Environment.get_air_density(altitude)
        v_mag = np.linalg.norm(v)
        v_hat = v / v_mag if v_mag > 0 else np.zeros(3)
        
        # Drag Force: F_d = 0.5 * rho * v^2 * Cd * A
        # Direction is opposite to velocity (-v_hat)
        f_drag_mag = 0.5 * rho * (v_mag**2) * self.rocket.drag_coeff * self.rocket.area
        f_drag = -f_drag_mag * v_hat
        a_drag = f_drag / m

        # 3. Thrust Force
        # Simple model: Constant thrust aligned with velocity vector (gravity turn assumption)
        # In a real GNC system, we would control pitch/yaw.
        # Here, we assume the rocket tilts slightly East initially then follows velocity vector.
        
        a_thrust = np.zeros(3)
        dm_dt = 0.0
        
        if t < self.rocket.burn_time and m > self.rocket.dry_mass:
            # Thrust direction logic:
            # If velocity is near zero (launchpad), thrust Up (radially out) + slight nudge East (for gravity turn)
            if v_mag < 10.0:
                radial_out = r / r_mag
                # Nudge East: Cross radial with North pole (0,0,1) gives East-ish? 
                # Simplified: Just add a small x-component if launching from "North Pole" equivalent or just hardcode a tilt
                # Let's assume launch from (R_earth, 0, 0). Radial is (1,0,0). Up is +X.
                # We want to tilt towards +Y (East).
                tilt = np.array([0, 0.1, 0]) 
                thrust_dir = radial_out + tilt
                thrust_dir = thrust_dir / np.linalg.norm(thrust_dir)
            else:
                # Gravity Turn: Thrust follows velocity vector
                thrust_dir = v_hat
            
            f_thrust = self.rocket.thrust * thrust_dir
            a_thrust = f_thrust / m
            
            # Mass flow rate: dm/dt = -F / (Isp * g0)
            # g0 is standard gravity (9.80665) for Isp calculation, distinct from local gravity
            g0 = 9.80665
            dm_dt = -self.rocket.thrust / (self.rocket.isp * g0)

        # Total Acceleration
        a_total = a_gravity + a_drag + a_thrust

        return np.concatenate([v, a_total, [dm_dt]])

    def step_rk4(self, t: float, state: np.ndarray, dt: float) -> np.ndarray:
        """ Performs one RK4 integration step. """
        k1 = self._derivatives(t, state)
        k2 = self._derivatives(t + 0.5*dt, state + 0.5*dt*k1)
        k3 = self._derivatives(t + 0.5*dt, state + 0.5*dt*k2)
        k4 = self._derivatives(t + dt, state + dt*k3)
        
        return state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

    def run(self, duration: float = 300.0, dt: float = 0.1):
        """ Runs the simulation loop. """
        # Initial Conditions
        # Start at Earth's surface on the X-axis (Equator-ish)
        # Velocity includes Earth's rotation if we want to be precise, but starting 0 for simplicity relative to surface
        start_pos = np.array([R_EARTH, 0, 0], dtype=float)
        start_vel = np.array([0, 0, 0], dtype=float) 
        start_mass = self.rocket.wet_mass
        
        state = np.concatenate([start_pos, start_vel, [start_mass]])
        t = 0.0
        
        print(f"Starting simulation: Wet Mass={start_mass}kg, Burn Time={self.rocket.burn_time}s")
        
        while t < duration:
            # Record History
            r = state[:3]
            v = state[3:6]
            alt = np.linalg.norm(r) - R_EARTH
            
            # Crash detection
            if alt < -1.0:
                print(f"Impact at t={t:.2f}s")
                break
                
            self.history['time'].append(t)
            self.history['x'].append(r[0])
            self.history['y'].append(r[1])
            self.history['z'].append(r[2])
            self.history['vx'].append(v[0])
            self.history['vy'].append(v[1])
            self.history['vz'].append(v[2])
            self.history['altitude'].append(alt)
            self.history['mass'].append(state[6])
            
            # Dynamic Pressure (q) for analysis
            rho = Environment.get_air_density(alt)
            v_mag = np.linalg.norm(v)
            q = 0.5 * rho * v_mag**2
            self.history['dynamic_pressure'].append(q)

            # Integration Step
            state = self.step_rk4(t, state, dt)
            t += dt

        print(f"Simulation Complete. Max Alt: {max(self.history['altitude'])/1000:.2f} km")

    def plot_results(self):
        """ Generates engineering plots using Matplotlib. """
        time = self.history['time']
        alt_km = np.array(self.history['altitude']) / 1000.0
        vel_mag = np.sqrt(np.array(self.history['vx'])**2 + np.array(self.history['vy'])**2 + np.array(self.history['vz'])**2)
        q_kpa = np.array(self.history['dynamic_pressure']) / 1000.0

        fig = plt.figure(figsize=(14, 8))
        
        # 1. Altitude vs Time
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(time, alt_km, 'b', label='Altitude')
        ax1.set_title("Altitude vs Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Altitude (km)")
        ax1.grid(True)

        # 2. Velocity vs Time
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(time, vel_mag, 'r', label='Velocity')
        ax2.set_title("Velocity vs Time")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Velocity (m/s)")
        ax2.grid(True)

        # 3. Dynamic Pressure (Max Q check)
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(time, q_kpa, 'g', label='Q')
        ax3.set_title("Dynamic Pressure (Q)")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Q (kPa)")
        ax3.grid(True)
        
        # 4. 3D Trajectory
        ax4 = fig.add_subplot(2, 2, 4, projection='3d')
        # Shift coordinates to be relative to launch site for better visibility
        x_rel = np.array(self.history['x']) - R_EARTH
        y_rel = np.array(self.history['y'])
        z_rel = np.array(self.history['z'])
        
        ax4.plot(x_rel, y_rel, z_rel, label='Trajectory')
        ax4.set_title("3D Ascent Trajectory (Relative to Center)")
        ax4.set_xlabel("X (Radial)")
        ax4.set_ylabel("Y (East)")
        ax4.set_zlabel("Z (North)")
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Create vehicle
    # Example: Roughly Falcon 9 First Stage parameters
    vehicle = RocketParams(
        wet_mass=549054,
        dry_mass=22200,
        thrust=7607000,
        isp=282,     # Sea level Isp roughly
        burn_time=162
    )
    
    sim = RocketSimulator(vehicle)
    sim.run(duration=200.0, dt=0.1)
    sim.plot_results()

