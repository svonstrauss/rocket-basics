"""
Starship Subsystem Trade Simulator
Module 3: Space Systems & Propulsion Engineering
Project 1

A systems engineering tool to analyze trade-offs between mass, propulsion, and payload.
Solves the Rocket Equation for multi-stage vehicles and optimizes for cost/performance.
Features an INTERACTIVE trade space visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from dataclasses import dataclass
from typing import List, Dict

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
G0 = 9.80665  # Standard Gravity (m/s^2)

def plot_interactive_trade_space():
    """
    Generates an INTERACTIVE "Payload vs. Delta-V" plot with sliders
    to change rocket parameters in real-time.
    """
    
    # --- 1. Initial Mass Definitions ---
    # Starship (Upper Stage)
    initial_prop_ship = 1200_000    # kg
    initial_dry_ship = 112_000      # kg
    initial_isp = 380               # s (Raptor Vac)
    
    # Booster (Super Heavy)
    # Assumed fairly constant for this upper stage trade study
    prop_booster = 3400_000  # kg
    dry_booster = 230_000    # kg
    isp_booster = 350        # s (Raptor SL avg)
    
    # Payload range (0 to 200 tonnes)
    payload_mass = np.linspace(1_000, 200_000, 100) # kg

    # --- 2. Rocket Equation Function ---
    def calculate_delta_v(isp, m_prop, m_dry, m_payload):
        """Calculates delta-v given masses using Tsiolkovsky."""
        m_initial = m_prop + m_dry + m_payload
        m_final = m_dry + m_payload
        dv = isp * G0 * np.log(m_initial / m_final)
        return dv # Return in m/s

    # --- 3. Setup the Plot ---
    fig, ax = plt.subplots(figsize=(12, 9)) # Make room for sliders
    fig.patch.set_facecolor('#1e1e2f')
    ax.set_facecolor('#1e1e2f')
    
    # Adjust main plot position to leave room for sliders at the bottom
    plt.subplots_adjust(left=0.1, bottom=0.35)

    # --- 4. Initial Plot ---
    # We will plot three lines and save references to update later
    line_fr, = ax.plot([], [], color='#50e3c2', linewidth=3, label='Fully Reusable')
    line_br, = ax.plot([], [], color='#f5e653', linewidth=3, label='Booster Reuse')
    line_ex, = ax.plot([], [], color='#e63946', linewidth=3, label='Expendable')

    # Add DV Target Lines
    ax.axhline(9400, color='#00b4d8', linestyle='--', label='LEO Orbit')
    ax.axhline(12800, color='#9b5de5', linestyle='--', label='Trans-Lunar (TLI)')

    # --- 5. Update Function ---
    def update_plot(val):
        """This function is called when a slider is moved."""
        # Get current slider values
        isp = slider_isp.val
        prop_ship = slider_prop.val * 1000
        dry_ship = slider_dry.val * 1000
        
        # Recalculate all 3 curves with Staging logic
        
        # Profile 1 (Green): Fully Reusable
        # Penalties: Booster lands (high dry/reserve), Ship lands (high dry/reserve)
        # Stage 1
        # Payload for S1 = Ship Wet + Actual Payload
        pl_1_fr = prop_ship + dry_ship + payload_mass
        # Booster reserve/legs penalty handled by effective dry/mass ratios or explicit penalty
        # Here we replicate the approximated profile logic from the inspiration code
        dv_s1_fr = calculate_delta_v(isp_booster, prop_booster, dry_booster * 1.2, pl_1_fr)
        # Stage 2
        dv_s2_fr = calculate_delta_v(isp, prop_ship, dry_ship, payload_mass)
        dv_total_fr = (dv_s1_fr + dv_s2_fr) * 0.90 # 10% losses
        
        # Profile 2 (Yellow): Booster Reuse
        # Penalties: Booster lands, Ship expended (lower effective dry mass)
        # Ship dry mass reduced (no heat shield/flaps/legs)
        dry_ship_exp = dry_ship * 0.7 
        pl_1_br = prop_ship + dry_ship_exp + payload_mass
        dv_s1_br = calculate_delta_v(isp_booster, prop_booster, dry_booster, pl_1_br)
        dv_s2_br = calculate_delta_v(isp, prop_ship, dry_ship_exp, payload_mass)
        dv_total_br = (dv_s1_br + dv_s2_br) * 0.92 # slightly less loss

        # Profile 3 (Red): Expendable
        # Penalties: None. Lowest dry masses.
        dry_booster_exp = dry_booster * 0.6
        dry_ship_max_exp = dry_ship * 0.6
        pl_1_ex = prop_ship + dry_ship_max_exp + payload_mass
        dv_s1_ex = calculate_delta_v(isp_booster, prop_booster, dry_booster_exp, pl_1_ex)
        dv_s2_ex = calculate_delta_v(isp, prop_ship, dry_ship_max_exp, payload_mass)
        dv_total_ex = (dv_s1_ex + dv_s2_ex) * 0.94 # least loss
        
        # Update the plot data
        payload_tonnes = payload_mass / 1000
        line_fr.set_data(payload_tonnes, dv_total_fr)
        line_br.set_data(payload_tonnes, dv_total_br)
        line_ex.set_data(payload_tonnes, dv_total_ex)
        
        # Redraw the figure
        fig.canvas.draw_idle()

    # --- 6. Stylize the Main Plot ---
    ax.set_title("Starship Architecture: Payload vs. Delta-V Trade Space", color='white', fontsize=16)
    ax.set_xlabel("Payload Mass (tonnes)", color='gray', fontsize=12)
    ax.set_ylabel("Total Delta-V (m/s)", color='gray', fontsize=12)
    ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.1)
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    for spine in ax.spines.values():
        spine.set_edgecolor('gray')
    
    # Set reasonable fixed limits to see the curves move
    ax.set_ylim(7500, 13500)
    ax.set_xlim(0, 200)
    
    ax.legend(facecolor='#2b2d42', labelcolor='white', loc='upper right')

    # --- 7. Create Sliders ---
    # Propellant Slider
    ax_prop = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor='#2b2d42')
    slider_prop = Slider(
        ax=ax_prop,
        label='Ship Prop (t) ',
        valmin=1000,
        valmax=1500,
        valinit=initial_prop_ship / 1000,
        color='#50e3c2'
    )
    slider_prop.label.set_color('white')
    slider_prop.valtext.set_color('white')

    # Dry Mass Slider
    ax_dry = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor='#2b2d42')
    slider_dry = Slider(
        ax=ax_dry,
        label='Ship Dry (t)  ',
        valmin=80,
        valmax=150,
        valinit=initial_dry_ship / 1000,
        color='#f5e653'
    )
    slider_dry.label.set_color('white')
    slider_dry.valtext.set_color('white')

    # Isp Slider
    ax_isp = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor='#2b2d42')
    slider_isp = Slider(
        ax=ax_isp,
        label='Ship Isp (s)  ',
        valmin=350,
        valmax=390,
        valinit=initial_isp,
        color='#e63946'
    )
    slider_isp.label.set_color('white')
    slider_isp.valtext.set_color('white')
    
    # --- 8. Connect Sliders to Update Function ---
    slider_prop.on_changed(update_plot)
    slider_dry.on_changed(update_plot)
    slider_isp.on_changed(update_plot)
    
    # Call it once to draw the initial plot
    update_plot(None)

    plt.show()

if __name__ == "__main__":
    plot_interactive_trade_space()
