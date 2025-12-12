"""
Propellant Explorer - Physics Engine Module
============================================
This module implements the Tsiolkovsky Rocket Equation.

Educational Focus:
- The "tyranny" of the rocket equation
- Why rockets are mostly fuel
- Trade-offs between efficiency and thrust

Author: Rocket Basics Project
"""

import math


class RocketPhysics:
    """
    Implements the Tsiolkovsky Rocket Equation and mission analysis.
    
    The Rocket Equation:
    --------------------
    Δv = Isp × g₀ × ln(m_initial / m_final)
    
    Where:
    - Δv = Change in velocity (what you need to reach your destination)
    - Isp = Specific Impulse (fuel efficiency, measured in seconds)
    - g₀ = Standard gravity (9.81 m/s²)
    - ln = Natural logarithm
    - m_initial = Total mass (rocket + fuel)
    - m_final = Dry mass (rocket without fuel)
    
    The logarithm is the "tyranny" - it means doubling fuel does NOT
    double your speed. You get diminishing returns because you have to
    carry that extra fuel before you burn it!
    """
    
    def __init__(self):
        # The Fuel Database (Real-world approximate values)
        # Isp (Specific Impulse) is measured in seconds
        # Higher Isp = More efficiency (like MPG for cars)
        self.fuels = {
            "Hydrolox (Hydrogen)": {
                "isp_sl": 366,      # Sea level Isp
                "isp_vac": 450,     # Vacuum Isp
                "density": 0.071,   # g/cm³ (VERY low - fluffy!)
                "color": "#1f77b4",
                "desc": "Highest efficiency, but requires huge tanks due to low density.",
                "used_by": "Space Shuttle, SLS, Delta IV"
            },
            "Methalox (Methane)": {
                "isp_sl": 330,
                "isp_vac": 380,
                "density": 0.42,    # g/cm³
                "color": "#9467bd",
                "desc": "Balanced efficiency and density. Clean burning for reuse.",
                "used_by": "Starship, New Glenn, Vulcan"
            },
            "RP-1 (Kerosene)": {
                "isp_sl": 282,
                "isp_vac": 350,
                "density": 0.81,    # g/cm³ (Dense!)
                "color": "#d62728",
                "desc": "High density = small tanks. Lower efficiency, leaves soot.",
                "used_by": "Falcon 9, Saturn V (Stage 1), Atlas V"
            },
            "Solid (HTPB)": {
                "isp_sl": 242,
                "isp_vac": 280,
                "density": 1.8,     # g/cm³ (Very dense)
                "color": "#ff7f0e",
                "desc": "Simple and reliable. Cannot throttle or shut down once lit!",
                "used_by": "Space Shuttle SRBs, Ariane 5 boosters"
            }
        }

        # Mission Database (Delta-v requirements in m/s)
        # These include margins for gravity loss and air resistance
        self.missions = {
            "Suborbital Hop": {
                "delta_v": 2000,
                "description": "Just touching space and coming back down",
                "example": "Blue Origin New Shepard, SpaceShipTwo"
            },
            "Low Earth Orbit (LEO)": {
                "delta_v": 9400,
                "description": "Where the ISS lives (~400 km altitude)",
                "example": "Falcon 9, Soyuz, Atlas V"
            },
            "Geostationary Transfer (GTO)": {
                "delta_v": 11800,
                "description": "Path to communication satellite orbit",
                "example": "Ariane 5, Falcon Heavy"
            },
            "Lunar Transfer": {
                "delta_v": 12500,
                "description": "Trans-Lunar Injection to reach the Moon",
                "example": "Apollo, Artemis"
            },
            "Mars Transfer": {
                "delta_v": 16000,
                "description": "Trans-Mars Injection (one way!)",
                "example": "Perseverance, Curiosity, Starship"
            }
        }
        
        # Standard gravity
        self.g0 = 9.80665

    def get_fuel_options(self):
        """Returns list of available fuels."""
        return list(self.fuels.keys())
    
    def get_fuel_info(self, fuel_name):
        """Returns detailed info about a fuel type."""
        return self.fuels.get(fuel_name, {})
    
    def get_mission_options(self):
        """Returns list of available missions."""
        return list(self.missions.keys())

    def calculate_delta_v(self, fuel_name, dry_mass_kg, fuel_mass_kg, use_vacuum_isp=True):
        """
        Applies the Tsiolkovsky Rocket Equation.
        
        Parameters:
        -----------
        fuel_name : str
            Name of the propellant
        dry_mass_kg : float
            Mass of rocket without fuel (structure + payload)
        fuel_mass_kg : float
            Mass of propellant
        use_vacuum_isp : bool
            Use vacuum Isp (True) or sea-level Isp (False)
            
        Returns:
        --------
        float : Delta-v in m/s
        """
        # Get efficiency of selected fuel
        fuel = self.fuels[fuel_name]
        isp = fuel["isp_vac"] if use_vacuum_isp else fuel["isp_sl"]
        
        # Calculate masses
        total_mass = dry_mass_kg + fuel_mass_kg
        
        # Safety check: Avoid division by zero or negative
        if dry_mass_kg <= 0:
            return 0
        if fuel_mass_kg <= 0:
            return 0

        # THE ROCKET EQUATION
        # math.log() is the Natural Logarithm (ln)
        mass_ratio = total_mass / dry_mass_kg
        delta_v = isp * self.g0 * math.log(mass_ratio)
        
        return round(delta_v, 2)
    
    def calculate_mass_ratio(self, dry_mass_kg, fuel_mass_kg):
        """Calculate the mass ratio (initial/final mass)."""
        if dry_mass_kg <= 0:
            return 0
        return (dry_mass_kg + fuel_mass_kg) / dry_mass_kg
    
    def calculate_fuel_fraction(self, dry_mass_kg, fuel_mass_kg):
        """Calculate what percentage of the rocket is fuel."""
        total = dry_mass_kg + fuel_mass_kg
        if total <= 0:
            return 0
        return (fuel_mass_kg / total) * 100

    def check_mission_status(self, delta_v):
        """
        Returns the highest mission tier the rocket can achieve.
        
        Parameters:
        -----------
        delta_v : float
            Calculated delta-v in m/s
            
        Returns:
        --------
        dict with achieved missions and status message
        """
        achieved = []
        for mission, info in self.missions.items():
            if delta_v >= info["delta_v"]:
                achieved.append(mission)
        
        if not achieved:
            return {
                "status": "Grounded",
                "message": "❌ Not enough delta-v to reach space!",
                "achieved": [],
                "next_target": "Suborbital Hop",
                "delta_v_needed": self.missions["Suborbital Hop"]["delta_v"] - delta_v
            }
        
        # Find the next unachieved mission
        all_missions = list(self.missions.keys())
        highest_achieved = achieved[-1]
        highest_idx = all_missions.index(highest_achieved)
        
        if highest_idx < len(all_missions) - 1:
            next_target = all_missions[highest_idx + 1]
            delta_v_needed = self.missions[next_target]["delta_v"] - delta_v
        else:
            next_target = None
            delta_v_needed = 0
        
        return {
            "status": "Success",
            "message": f"✅ Capable of: {highest_achieved}",
            "achieved": achieved,
            "next_target": next_target,
            "delta_v_needed": delta_v_needed
        }
    
    def required_fuel_for_mission(self, mission_name, fuel_name, dry_mass_kg):
        """
        Calculate how much fuel is needed to achieve a specific mission.
        
        Uses the inverted rocket equation:
        m_fuel = m_dry × (e^(Δv/(Isp×g₀)) - 1)
        """
        if mission_name not in self.missions:
            return None
        if fuel_name not in self.fuels:
            return None
            
        delta_v = self.missions[mission_name]["delta_v"]
        isp = self.fuels[fuel_name]["isp_vac"]
        
        # Inverted rocket equation
        exponent = delta_v / (isp * self.g0)
        mass_ratio = math.exp(exponent)
        fuel_mass = dry_mass_kg * (mass_ratio - 1)
        
        return round(fuel_mass, 2)


# --- Quick Test to verify it works in the terminal ---
if __name__ == "__main__":
    engine = RocketPhysics()
    
    print("=" * 70)
    print("ROCKET PHYSICS ENGINE - Test Suite")
    print("=" * 70)
    
    # Test parameters: 5,000 kg dry mass, 100,000 kg fuel
    dry_mass = 5000
    fuel_mass = 100000
    
    print(f"\nTest Rocket: {dry_mass:,} kg dry mass + {fuel_mass:,} kg fuel")
    print(f"Mass Ratio: {engine.calculate_mass_ratio(dry_mass, fuel_mass):.2f}")
    print(f"Fuel Fraction: {engine.calculate_fuel_fraction(dry_mass, fuel_mass):.1f}%")
    
    print("\n" + "-" * 70)
    print("DELTA-V BY PROPELLANT TYPE:")
    print("-" * 70)
    
    for fuel in engine.get_fuel_options():
        dv = engine.calculate_delta_v(fuel, dry_mass, fuel_mass)
        status = engine.check_mission_status(dv)
        fuel_info = engine.get_fuel_info(fuel)
        
        print(f"\n{fuel}")
        print(f"  Isp (vacuum): {fuel_info['isp_vac']} s")
        print(f"  Delta-v: {dv:,.0f} m/s")
        print(f"  {status['message']}")
    
    print("\n" + "=" * 70)
    print("FUEL REQUIRED FOR LEO (with Methalox):")
    print("=" * 70)
    
    for dry in [1000, 5000, 10000, 50000]:
        fuel_needed = engine.required_fuel_for_mission("Low Earth Orbit (LEO)", 
                                                        "Methalox (Methane)", dry)
        ratio = fuel_needed / dry if dry > 0 else 0
        print(f"  {dry:,} kg structure → {fuel_needed:,.0f} kg fuel needed ({ratio:.1f}x dry mass)")

