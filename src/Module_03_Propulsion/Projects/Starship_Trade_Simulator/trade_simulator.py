"""
Starship Trade Simulator
Module 3: Space Systems & Propulsion Engineering

Interactive trade-space analysis for the Starship launch system.
Models payload vs delta-V performance for different reuse configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from dataclasses import dataclass

G0 = 9.80665  # Standard gravity (m/s²)

# Launch vehicle data from multiple agencies
VEHICLE_DATA = {
    'starship': {
        'name': 'Starship/Super Heavy', 'operator': 'SpaceX', 'country': 'USA',
        'propellant_kg': 4600000, 'thrust_kn': 7590 + 1380, 'isp_vac': 380,
        'payload_leo_kg': 150000, 'status': 'Development',
    },
    'sls': {
        'name': 'SLS Block 1', 'operator': 'NASA', 'country': 'USA',
        'propellant_kg': 2600000, 'thrust_kn': 8800, 'isp_vac': 366,
        'payload_leo_kg': 95000, 'status': 'Operational',
    },
    'falcon_heavy': {
        'name': 'Falcon Heavy', 'operator': 'SpaceX', 'country': 'USA',
        'propellant_kg': 1400000, 'thrust_kn': 5000, 'isp_vac': 348,
        'payload_leo_kg': 63800, 'status': 'Operational',
    },
    'ariane6': {
        'name': 'Ariane 6', 'operator': 'ESA/Arianespace', 'country': 'Europe',
        'propellant_kg': 800000, 'thrust_kn': 1500, 'isp_vac': 431,
        'payload_leo_kg': 21650, 'status': 'Operational',
    },
    'long_march_5': {
        'name': 'Long March 5', 'operator': 'CNSA', 'country': 'China',
        'propellant_kg': 850000, 'thrust_kn': 1078, 'isp_vac': 430,
        'payload_leo_kg': 25000, 'status': 'Operational',
    },
    'h3': {
        'name': 'H3', 'operator': 'JAXA', 'country': 'Japan',
        'propellant_kg': 450000, 'thrust_kn': 2940, 'isp_vac': 425,
        'payload_leo_kg': 6500, 'status': 'Operational',
    },
}

# Starship specifics for trade study
STARSHIP_DATA = {
    'booster': {
        'name': 'Super Heavy', 'propellant_kg': 3400000, 'dry_mass_kg': 200000,
        'engines': 33, 'engine_type': 'Raptor 2', 'thrust_kn': 230 * 33,
        'isp_sl': 327, 'isp_vac': 350,
    },
    'ship': {
        'name': 'Starship', 'propellant_kg': 1200000, 'dry_mass_kg': 100000,
        'engines': 6, 'engine_type': 'Raptor Vacuum', 'thrust_kn': 230 * 6,
        'isp_vac': 380,
    },
    'targets': {
        'leo': {'name': 'LEO (400 km)', 'dv': 9400, 'color': '#00d4ff'},
        'gto': {'name': 'GTO', 'dv': 11000, 'color': '#ff6b35'},
        'tli': {'name': 'Trans-Lunar', 'dv': 12800, 'color': '#00ff9f'},
        'mars': {'name': 'Mars Direct', 'dv': 15000, 'color': '#ff3366'},
    }
}


def style_axis_scifi(ax, title="", xlabel="", ylabel=""):
    """Apply dark theme styling for engineering plots."""
    ax.set_facecolor('#060d18')
    
    if title:
        ax.set_title(title, color='#00d4ff', fontsize=13, fontweight='bold',
                    pad=12, loc='left', fontfamily='monospace')
        ax.add_line(Line2D([0, 0.4], [1.02, 1.02], color='#00d4ff', alpha=0.8,
                          lw=2, transform=ax.transAxes, clip_on=False))
    
    ax.set_xlabel(xlabel, color='#00d4ff', fontsize=11, fontfamily='monospace', fontweight='bold')
    ax.set_ylabel(ylabel, color='#00d4ff', fontsize=11, fontfamily='monospace', fontweight='bold')
    ax.tick_params(colors='#4db8d4', labelsize=9)
    
    for spine in ax.spines.values():
        spine.set_color('#0e4d64')
        spine.set_linewidth(2)
    
    ax.grid(True, color='#0a2a3a', alpha=0.5, linestyle='-', linewidth=0.5)
    
    # Corner accents
    corners = [
        ([0, 0.04], [1, 1]), ([0, 0], [1, 0.96]),
        ([0.96, 1], [1, 1]), ([1, 1], [1, 0.96]),
        ([0, 0.04], [0, 0]), ([0, 0], [0, 0.04]),
        ([0.96, 1], [0, 0]), ([1, 1], [0, 0.04]),
    ]
    for x_c, y_c in corners:
        ax.add_line(Line2D(x_c, y_c, color='#00d4ff', alpha=0.6, lw=1.5,
                          transform=ax.transAxes, clip_on=False))


class TradeSimulator:
    """Interactive Starship trade-space analyzer."""
    
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.patch.set_facecolor('#050a12')
        
        # Initial parameters
        self.prop_ship = 1200  # tonnes
        self.dry_ship = 100   # tonnes
        self.isp_ship = 380   # seconds
        
        # Booster parameters (fixed)
        self.prop_booster = 3400  # tonnes
        self.dry_booster = 200   # tonnes
        self.isp_booster = 350   # seconds
        
        self.payload_range = np.linspace(1, 250, 200)  # tonnes
        
        self._setup_ui()
        self._update_plot(None)
    
    def _setup_ui(self):
        """Create the UI layout."""
        # Title
        self.fig.text(0.5, 0.97, "◢ LAUNCH VEHICLE TRADE SIMULATOR ◣",
                     fontsize=20, fontweight='bold', color='#00d4ff', ha='center',
                     fontfamily='monospace')
        self.fig.text(0.5, 0.935, "Starship • SLS • Falcon Heavy • Ariane 6 • Long March 5",
                     fontsize=11, color='#7fdbff', ha='center', fontfamily='monospace')
        
        # Main plot
        self.ax_main = self.fig.add_axes([0.08, 0.35, 0.55, 0.52])
        style_axis_scifi(self.ax_main, "TRADE SPACE", "Payload Mass [tonnes]", "Total ΔV [m/s]")
        
        # Create plot lines
        self.line_reuse, = self.ax_main.plot([], [], color='#00ff9f', lw=3, label='Fully Reusable')
        self.line_partial, = self.ax_main.plot([], [], color='#ffd700', lw=3, label='Booster Reuse')
        self.line_expend, = self.ax_main.plot([], [], color='#ff3366', lw=3, label='Expendable')
        
        # Glow effects
        self.line_reuse_glow, = self.ax_main.plot([], [], color='#00ff9f', lw=8, alpha=0.2)
        self.line_partial_glow, = self.ax_main.plot([], [], color='#ffd700', lw=8, alpha=0.2)
        self.line_expend_glow, = self.ax_main.plot([], [], color='#ff3366', lw=8, alpha=0.2)
        
        # Target lines
        for key, target in STARSHIP_DATA['targets'].items():
            self.ax_main.axhline(target['dv'], color=target['color'], ls='--', lw=1.5, alpha=0.7)
            self.ax_main.text(240, target['dv'] + 100, target['name'], color=target['color'],
                             fontsize=9, fontfamily='monospace', ha='right')
        
        self.ax_main.set_xlim(0, 250)
        self.ax_main.set_ylim(7000, 16000)
        self.ax_main.legend(loc='upper right', facecolor='#0a1420', labelcolor='white',
                           edgecolor='#00d4ff', fontsize=9)
        
        # Info panel
        self.ax_info = self.fig.add_axes([0.68, 0.35, 0.28, 0.52])
        self.ax_info.set_facecolor('#050a12')
        self.ax_info.axis('off')
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff', linewidth=2,
                               transform=self.ax_info.transAxes)
        self.ax_info.add_patch(panel)
        
        self.ax_info.text(0.5, 0.97, "◢ VEHICLE COMPARISON ◣", transform=self.ax_info.transAxes,
                         fontsize=11, fontweight='bold', color='#00d4ff', ha='center',
                         fontfamily='monospace')
        
        # Global launch vehicles comparison
        self.ax_info.text(0.08, 0.90, "► LEO PAYLOAD CAPACITY", transform=self.ax_info.transAxes,
                         fontsize=10, color='#ff6b35', fontfamily='monospace', fontweight='bold')
        
        vehicles = [
            ('Starship', 'SpaceX', 150, '#00d4ff'),
            ('SLS Block 1', 'NASA', 95, '#ff6b35'),
            ('Falcon Heavy', 'SpaceX', 64, '#00ff9f'),
            ('Long March 5', 'CNSA', 25, '#ffd700'),
            ('Ariane 6', 'ESA', 22, '#ff69b4'),
            ('H3', 'JAXA', 6.5, '#ffffff'),
        ]
        
        for i, (name, agency, payload, col) in enumerate(vehicles):
            y = 0.82 - i * 0.075
            self.ax_info.text(0.08, y, f"• {name}", transform=self.ax_info.transAxes,
                             fontsize=9, color=col, fontfamily='monospace')
            self.ax_info.text(0.55, y, f"{payload} t", transform=self.ax_info.transAxes,
                             fontsize=9, color='#ffffff', fontfamily='monospace')
            self.ax_info.text(0.75, y, f"({agency})", transform=self.ax_info.transAxes,
                             fontsize=7, color='#888888', fontfamily='monospace')
        
        # Divider
        self.ax_info.add_line(Line2D([0.05, 0.95], [0.35, 0.35], color='#00d4ff', alpha=0.3, lw=1,
                                    transform=self.ax_info.transAxes))
        
        # Dynamic payload capacity text
        self.payload_txt = self.ax_info.text(0.5, 0.28, "", transform=self.ax_info.transAxes,
                                            fontsize=9, color='#ffd700', ha='center',
                                            fontfamily='monospace', fontweight='bold')
        
        # Mission capability text
        self.ax_info.text(0.08, 0.18, "► TRADE STUDY RESULTS", transform=self.ax_info.transAxes,
                         fontsize=9, color='#00ff9f', fontfamily='monospace', fontweight='bold')
        self.cap_txt = self.ax_info.text(0.10, 0.03, "", transform=self.ax_info.transAxes,
                                        fontsize=8, color='#ffffff', fontfamily='monospace')
        
        # Sliders
        slider_color = '#0a2a3a'
        
        ax_prop = self.fig.add_axes([0.12, 0.22, 0.50, 0.025], facecolor=slider_color)
        self.slider_prop = Slider(ax_prop, 'Ship Propellant [t]', 1000, 1500,
                                 valinit=self.prop_ship, color='#00d4ff')
        self.slider_prop.label.set_color('#00d4ff')
        self.slider_prop.label.set_fontsize(10)
        self.slider_prop.valtext.set_color('#ffffff')
        
        ax_dry = self.fig.add_axes([0.12, 0.16, 0.50, 0.025], facecolor=slider_color)
        self.slider_dry = Slider(ax_dry, 'Ship Dry Mass [t]', 80, 150,
                                valinit=self.dry_ship, color='#ff6b35')
        self.slider_dry.label.set_color('#ff6b35')
        self.slider_dry.label.set_fontsize(10)
        self.slider_dry.valtext.set_color('#ffffff')
        
        ax_isp = self.fig.add_axes([0.12, 0.10, 0.50, 0.025], facecolor=slider_color)
        self.slider_isp = Slider(ax_isp, 'Ship Isp [s]', 350, 400,
                                valinit=self.isp_ship, color='#00ff9f')
        self.slider_isp.label.set_color('#00ff9f')
        self.slider_isp.label.set_fontsize(10)
        self.slider_isp.valtext.set_color('#ffffff')
        
        # Connect sliders
        self.slider_prop.on_changed(self._update_plot)
        self.slider_dry.on_changed(self._update_plot)
        self.slider_isp.on_changed(self._update_plot)
        
        # Reset button
        ax_reset = self.fig.add_axes([0.68, 0.10, 0.12, 0.04])
        self.btn_reset = Button(ax_reset, 'RESET', color='#0a1628', hovercolor='#1e3a5f')
        self.btn_reset.label.set_color('#00d4ff')
        self.btn_reset.label.set_fontsize(10)
        self.btn_reset.label.set_fontweight('bold')
        for spine in ax_reset.spines.values():
            spine.set_color('#00d4ff')
        self.btn_reset.on_clicked(self._reset)
    
    def _calc_delta_v(self, isp, m_prop, m_dry, m_payload):
        """Tsiolkovsky rocket equation."""
        m_initial = m_prop + m_dry + m_payload
        m_final = m_dry + m_payload
        return isp * G0 * np.log(m_initial / m_final)
    
    def _update_plot(self, val):
        """Update plot with current slider values."""
        prop_ship = self.slider_prop.val * 1000  # kg
        dry_ship = self.slider_dry.val * 1000    # kg
        isp_ship = self.slider_isp.val
        
        prop_booster = self.prop_booster * 1000  # kg
        dry_booster = self.dry_booster * 1000    # kg
        
        payload_kg = self.payload_range * 1000
        
        # Fully Reusable (both stages land)
        # Landing penalties: higher dry mass, reserve propellant
        dry_booster_reuse = dry_booster * 1.15
        dry_ship_reuse = dry_ship * 1.0
        ship_wet = prop_ship + dry_ship_reuse + payload_kg
        
        dv1_reuse = self._calc_delta_v(self.isp_booster, prop_booster, dry_booster_reuse, ship_wet)
        dv2_reuse = self._calc_delta_v(isp_ship, prop_ship, dry_ship_reuse, payload_kg)
        dv_reuse = (dv1_reuse + dv2_reuse) * 0.92  # Gravity/drag losses
        
        # Partial Reuse (booster lands, ship expended)
        dry_ship_exp = dry_ship * 0.75  # No heat shield, landing legs
        ship_wet_partial = prop_ship + dry_ship_exp + payload_kg
        
        dv1_partial = self._calc_delta_v(self.isp_booster, prop_booster, dry_booster_reuse, ship_wet_partial)
        dv2_partial = self._calc_delta_v(isp_ship, prop_ship, dry_ship_exp, payload_kg)
        dv_partial = (dv1_partial + dv2_partial) * 0.93
        
        # Fully Expendable
        dry_booster_exp = dry_booster * 0.65
        dry_ship_full_exp = dry_ship * 0.65
        ship_wet_exp = prop_ship + dry_ship_full_exp + payload_kg
        
        dv1_exp = self._calc_delta_v(self.isp_booster, prop_booster, dry_booster_exp, ship_wet_exp)
        dv2_exp = self._calc_delta_v(isp_ship, prop_ship, dry_ship_full_exp, payload_kg)
        dv_exp = (dv1_exp + dv2_exp) * 0.94
        
        # Update lines
        self.line_reuse.set_data(self.payload_range, dv_reuse)
        self.line_partial.set_data(self.payload_range, dv_partial)
        self.line_expend.set_data(self.payload_range, dv_exp)
        
        self.line_reuse_glow.set_data(self.payload_range, dv_reuse)
        self.line_partial_glow.set_data(self.payload_range, dv_partial)
        self.line_expend_glow.set_data(self.payload_range, dv_exp)
        
        # Calculate payload capacities at different DV targets
        leo_dv = 9400
        tli_dv = 12800
        
        # Find payload at LEO (interpolate)
        idx_leo_reuse = np.searchsorted(dv_reuse[::-1], leo_dv)
        idx_leo_exp = np.searchsorted(dv_exp[::-1], leo_dv)
        
        pl_leo_reuse = self.payload_range[::-1][idx_leo_reuse] if idx_leo_reuse < len(self.payload_range) else 0
        pl_leo_exp = self.payload_range[::-1][idx_leo_exp] if idx_leo_exp < len(self.payload_range) else 0
        
        # Update payload text
        self.payload_txt.set_text(f"LEO PAYLOAD CAPACITY\n"
                                  f"Reusable: ~{pl_leo_reuse:.0f} t\n"
                                  f"Expendable: ~{pl_leo_exp:.0f} t")
        
        # Capability assessment
        mass_ratio = (prop_ship + dry_ship) / dry_ship
        cap_text = f"Ship Mass Ratio: {mass_ratio:.2f}\n"
        cap_text += f"Ship ΔV (alone): {isp_ship * G0 * np.log(mass_ratio)/1000:.1f} km/s\n"
        cap_text += f"TWR (ship): ~{(STARSHIP_DATA['ship']['thrust_kn']*1000)/(dry_ship*9.81):.1f}"
        self.cap_txt.set_text(cap_text)
        
        self.fig.canvas.draw_idle()
    
    def _reset(self, event):
        """Reset sliders to default."""
        self.slider_prop.set_val(1200)
        self.slider_dry.set_val(100)
        self.slider_isp.set_val(380)
    
    def show(self):
        plt.show()


def run_demo():
    print("=" * 60)
    print("ROCKET TRADE SIMULATOR")
    print("Module 3: Propulsion Engineering")
    print("Comparing: Starship • SLS • Falcon Heavy • Ariane 6 • Long March 5")
    print("=" * 60)
    print("\nInteractive trade-space analysis")
    print("Use sliders to modify vehicle parameters")
    print("-" * 60)
    
    sim = TradeSimulator()
    sim.show()


if __name__ == "__main__":
    run_demo()
