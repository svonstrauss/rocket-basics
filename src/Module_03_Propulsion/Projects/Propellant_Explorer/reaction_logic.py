"""
Propellant Explorer - Reaction Balancer Module
================================================
This module handles the chemistry of rocket propellants.

Educational Focus:
- Chemical stoichiometry (balancing equations)
- Fuel-rich vs fuel-lean combustion
- Real-world engine design constraints

Author: Rocket Basics Project
"""


class RocketReaction:
    """
    Handles chemical reaction balancing for rocket propellants.
    
    This class teaches students about stoichiometry - the math of 
    chemical reactions. In rocket engines, the fuel-to-oxidizer ratio
    is CRITICAL:
    
    - Too much fuel (fuel-rich): Cooler burn, wasted fuel, soot/coking
    - Too much oxidizer (fuel-lean): DANGER! Extreme heat melts engine
    - Perfect balance: Maximum energy, clean exhaust, happy engineers
    """
    
    def __init__(self):
        # The "Answer Key" for perfect stoichiometry
        # Format: {Fuel_Name: {'fuel': coefficient, 'oxidizer': coefficient}}
        self.correct_ratios = {
            "Hydrolox (Hydrogen)": {'fuel': 2, 'oxidizer': 1},   # 2H2 + O2 -> 2H2O
            "Methalox (Methane)":  {'fuel': 1, 'oxidizer': 2},   # CH4 + 2O2 -> CO2 + 2H2O
            "RP-1 (Kerosene)":     {'fuel': 1, 'oxidizer': 18.5} # Approx: C12H26 + 18.5 O2
        }
        
        # Chemical formulas for display
        self.formulas = {
            "Hydrolox (Hydrogen)": "2H₂ + O₂ → 2H₂O",
            "Methalox (Methane)":  "CH₄ + 2O₂ → CO₂ + 2H₂O",
            "RP-1 (Kerosene)":     "C₁₂H₂₆ + 18.5O₂ → 12CO₂ + 13H₂O"
        }
        
        # Educational descriptions
        self.descriptions = {
            "Hydrolox (Hydrogen)": 
                "Liquid Hydrogen + Liquid Oxygen. Used by Space Shuttle Main Engines, "
                "SLS, and Delta IV. Highest efficiency (Isp ~450s) but very low density - "
                "requires HUGE tanks (that's why the Space Shuttle's orange tank was so big!).",
            
            "Methalox (Methane)":  
                "Liquid Methane + Liquid Oxygen. The 'Goldilocks' propellant used by "
                "SpaceX Starship and Blue Origin's New Glenn. Good efficiency (~380s), "
                "reasonable density, and burns cleanly - perfect for reusable engines.",
            
            "RP-1 (Kerosene)":     
                "Refined Kerosene + Liquid Oxygen. Used by Falcon 9, Saturn V first stage, "
                "and Atlas V. High density = smaller tanks, but lower efficiency (~350s) "
                "and leaves carbon deposits (coking) that complicate reuse."
        }

    def get_fuel_options(self):
        """Returns list of available fuels for the dropdown."""
        return list(self.correct_ratios.keys())

    def get_formula(self, fuel_name):
        """Returns the display string for the chemical equation."""
        return self.formulas.get(fuel_name, "Unknown Fuel")
    
    def get_description(self, fuel_name):
        """Returns educational description of the propellant."""
        return self.descriptions.get(fuel_name, "No description available.")

    def check_balance(self, fuel_name, user_fuel_coeff, user_ox_coeff):
        """
        Compares user inputs against the answer key.
        
        Parameters:
        -----------
        fuel_name : str
            Name of the propellant combination
        user_fuel_coeff : float
            User's guess for fuel coefficient
        user_ox_coeff : float
            User's guess for oxidizer coefficient
            
        Returns:
        --------
        dict with 'status', 'color', and 'message' keys
        """
        if user_fuel_coeff <= 0:
            return {
                "status": "Error",
                "color": "gray",
                "message": "⚠️ Fuel coefficient must be greater than zero!"
            }
            
        target = self.correct_ratios[fuel_name]
        
        # Calculate the user's ratio vs the perfect ratio
        # We use ratios because 2:4 is the same chemically as 1:2
        user_ratio = user_ox_coeff / user_fuel_coeff
        target_ratio = target['oxidizer'] / target['fuel']
        
        # Tolerance for floating point math (especially for RP-1)
        tolerance = 0.1 

        if abs(user_ratio - target_ratio) < tolerance:
            return {
                "status": "Perfect",
                "color": "green",
                "message": "✅ Perfect Balance! Maximum energy release. "
                          "The exhaust is clean and velocity is maximized."
            }
        
        elif user_ratio < target_ratio:
            return {
                "status": "Fuel Rich",
                "color": "orange",
                "message": "⚠️ Fuel Rich (Too much Fuel). Not enough Oxygen to burn "
                          "everything. You are leaving energy on the table and likely "
                          "creating soot (carbon) in the exhaust. Real engines sometimes "
                          "run slightly fuel-rich to keep temperatures down!"
            }
            
        else:  # user_ratio > target_ratio
            return {
                "status": "Fuel Lean",
                "color": "red",
                "message": "🔥 Fuel Lean (Too much Oxygen). DANGEROUS! This burns "
                          "extremely hot and oxygen-rich gas can melt the metal of "
                          "your engine components. Never run an engine fuel-lean!"
            }


# --- Quick Test to verify it works in the terminal ---
if __name__ == "__main__":
    solver = RocketReaction()
    
    print("=" * 60)
    print("PROPELLANT REACTION BALANCER - Test Suite")
    print("=" * 60)
    
    # Test all fuels
    for fuel in solver.get_fuel_options():
        print(f"\n{fuel}")
        print(f"Formula: {solver.get_formula(fuel)}")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("Balance Tests:")
    print("=" * 60)
    
    # Test Case: User guesses 1 Methane and 1 Oxygen (Wrong - fuel rich)
    print("\nTest 1: 1:1 Methane (should be fuel rich)")
    result = solver.check_balance("Methalox (Methane)", 1, 1)
    print(f"  Status: {result['status']}")
    print(f"  {result['message']}")
    
    # Test Case: User guesses 1 Methane and 2 Oxygen (Correct)
    print("\nTest 2: 1:2 Methane (should be perfect)")
    result = solver.check_balance("Methalox (Methane)", 1, 2)
    print(f"  Status: {result['status']}")
    print(f"  {result['message']}")
    
    # Test Case: Too much oxygen
    print("\nTest 3: 1:4 Methane (should be fuel lean)")
    result = solver.check_balance("Methalox (Methane)", 1, 4)
    print(f"  Status: {result['status']}")
    print(f"  {result['message']}")

