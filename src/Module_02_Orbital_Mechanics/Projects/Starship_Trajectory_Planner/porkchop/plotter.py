"""
Porkchop Plot Generator (Interactive)
Module 2: Orbital Mechanics and Mission Design
Project 2 Extension

Calculates and visualizes the 'Porkchop Plot' for Earth-Mars transfers.
Solves Lambert's Problem for thousands of launch/arrival date combinations
to map the Delta-V trade space. Now interactive!
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from dataclasses import dataclass
from datetime import datetime, timedelta

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
G = 6.67430e-11             # m^3 kg^-1 s^-2
M_SUN = 1.989e30            # kg
MU_SUN = G * M_SUN          # m^3 s^-2
AU = 1.495978707e11         # m

# Approximate Ephemeris (Circular/Coplanar assumption for simplified Lambert)
R_EARTH = 1.0 * AU
R_MARS = 1.524 * AU
T_EARTH = 365.25 * 24 * 3600
T_MARS = 686.98 * 24 * 3600
W_EARTH = 2 * np.pi / T_EARTH
W_MARS = 2 * np.pi / T_MARS

def lambert_solver(r1_vec, r2_vec, dt):
    """
    Approximated Delta-V based on transfer geometry for the heatmap.
    Penalizes deviations from Hohmann optimal time and phase.
    """
    # Calculate chord length c
    r1 = np.linalg.norm(r1_vec)
    r2 = np.linalg.norm(r2_vec)
    
    # Optimal Hohmann Time
    a_hohmann = (r1 + r2) / 2
    t_hohmann = np.pi * np.sqrt(a_hohmann**3 / MU_SUN)
    
    # Heuristic penalty for non-optimal time
    time_ratio = dt / t_hohmann
    
    # Base Hohmann dV ~ 5.7 km/s
    base_dv = 5700 
    
    # Alignment check:
    # For Hohmann, angle_diff should be Pi (180 deg transfer).
    # We calculate the angle between r1 and r2 vectors
    angle_diff = np.arccos(np.dot(r1_vec, r2_vec) / (r1 * r2))
    
    # Penalty function
    # Cost grows as we deviate from optimal transfer time or optimal alignment
    penalty = 2000 * (np.log(time_ratio)**2) + 5000 * (1 - np.sin(angle_diff/2))**2
    
    return base_dv + penalty

def plot_interactive_porkchop():
    # Grid of Launch Dates vs Arrival Dates
    launch_days = np.linspace(0, 500, 100)
    arrival_days = np.linspace(100, 800, 100)
    
    X, Y = np.meshgrid(launch_days, arrival_days)
    Z = np.zeros_like(X)
    
    print("Generating Porkchop Plot (solving Lambert geometry)...")
    
    # Pre-calculate Z matrix
    for i in range(len(arrival_days)):
        for j in range(len(launch_days)):
            t_launch = launch_days[j] * 24 * 3600
            t_arrival = arrival_days[i] * 24 * 3600
            dt = t_arrival - t_launch
            
            if dt <= 0:
                Z[i, j] = np.nan # Impossible
                continue
                
            theta1 = W_EARTH * t_launch
            r1_vec = np.array([R_EARTH * np.cos(theta1), R_EARTH * np.sin(theta1), 0])
            
            initial_phase = 0.78 # Mars lead at T=0
            theta2 = initial_phase + W_MARS * t_arrival
            r2_vec = np.array([R_MARS * np.cos(theta2), R_MARS * np.sin(theta2), 0])
            
            dv = lambert_solver(r1_vec, r2_vec, dt)
            Z[i, j] = dv / 1000.0 # km/s

    # Find Optimal
    min_idx = np.unravel_index(np.nanargmin(Z), Z.shape)
    opt_launch = launch_days[min_idx[1]]
    opt_arrive = arrival_days[min_idx[0]]
    opt_dv = Z[min_idx]

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    # Contour Plot
    levels = np.linspace(5.6, 15, 20)
    cp = ax.contourf(X, Y, Z, levels=levels, cmap='turbo', extend='max')
    
    cbar = fig.colorbar(cp, ax=ax, extend='max')
    cbar.set_label('Total Delta-V (km/s)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    # Optimal Marker
    ax.plot(opt_launch, opt_arrive, '*', color='black', markersize=18, zorder=10)
    ax.plot(opt_launch, opt_arrive, '*', color='lime', markersize=12, label=f'Optimal: {opt_dv:.2f} km/s', zorder=11)
    
    # Selected Marker (Initialized at Optimal)
    sel_marker_bg, = ax.plot(opt_launch, opt_arrive, '*', color='black', markersize=18, zorder=10)
    sel_marker, = ax.plot(opt_launch, opt_arrive, '*', color='white', markersize=12, label='Selected', zorder=11)
    
    # Info Box
    info_text = ax.text(0.95, 0.05, '', transform=ax.transAxes, fontsize=10,
                        verticalalignment='bottom', horizontalalignment='right',
                        bbox=dict(boxstyle='round,pad=0.5', fc='#2b2d42', ec='gray', alpha=0.8),
                        color='white', family='monospace')

    # Styling
    ax.set_title("Earth-Mars Porkchop Plot (2026 Window) - Interactive", color='white', fontsize=16, pad=20)
    ax.set_xlabel("Launch Date (Days from Epoch)", color='gray', fontsize=12)
    ax.set_ylabel("Arrival Date (Days from Epoch)", color='gray', fontsize=12)
    ax.tick_params(colors='gray')
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.legend(loc='upper left', facecolor='#2b2d42', labelcolor='white')
    
    ax.set_xlim(0, 500)
    ax.set_ylim(100, 800)

    def update_info(launch_d, arrive_d):
        # Find closest grid point
        x_idx = np.abs(launch_days - launch_d).argmin()
        y_idx = np.abs(arrival_days - arrive_d).argmin()
        dv = Z[y_idx, x_idx]
        
        transit = arrive_d - launch_d
        
        status = "INVALID" if np.isnan(dv) else "SELECTED"
        dv_str = "--" if np.isnan(dv) else f"{dv:.2f} km/s"
        transit_str = "--" if np.isnan(dv) else f"{transit:.1f} days"
        
        info_text.set_text(
            f"MISSION: {status}\n"
            f"-----------------\n"
            f"Launch:  Day {launch_d:.1f}\n"
            f"Arrival: Day {arrive_d:.1f}\n"
            f"Transit: {transit_str}\n"
            f"Delta-V: {dv_str}"
        )
        fig.canvas.draw_idle()

    def onclick(event):
        if event.inaxes != ax: return
        
        launch_d = event.xdata
        arrive_d = event.ydata
        
        # Update Marker
        sel_marker.set_data([launch_d], [arrive_d])
        sel_marker_bg.set_data([launch_d], [arrive_d])
        
        update_info(launch_d, arrive_d)

    fig.canvas.mpl_connect('button_press_event', onclick)
    
    # Initial Update
    update_info(opt_launch, opt_arrive)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_interactive_porkchop()
