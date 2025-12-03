"""
Space Policy Risk Calculator
Module 4: Human Factors, Regulations, and Space Policy
Project 2

A framework to assess regulatory compliance and mission risk for space operations.
Evaluates missions against key policy areas: orbital debris, collision risk,
spectrum allocation, human safety, environmental impact, and planetary protection.

This tool demonstrates understanding of the regulatory landscape that SpaceX
navigates for every launch—from FAA licensing to FCC spectrum coordination
to international space debris guidelines.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json

# --- Configuration ---
plt.style.use('dark_background')


class RiskLevel(Enum):
    """Risk severity levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    
    @property
    def color(self) -> str:
        colors = {
            RiskLevel.LOW: '#50e3c2',
            RiskLevel.MEDIUM: '#f5e653',
            RiskLevel.HIGH: '#ff9f43',
            RiskLevel.CRITICAL: '#e63946'
        }
        return colors[self]
    
    @property
    def label(self) -> str:
        return self.name


@dataclass
class RiskFactor:
    """Represents a single risk factor in the assessment."""
    name: str
    category: str
    level: RiskLevel
    score: float  # 0-100
    description: str
    mitigation: str = ""
    regulation: str = ""


@dataclass
class MissionProfile:
    """
    Defines the parameters of a space mission for risk assessment.
    
    All the information needed to evaluate regulatory compliance
    and operational risks.
    """
    name: str
    
    # Orbital Parameters
    altitude_km: float              # Mean orbital altitude
    inclination_deg: float          # Orbital inclination
    is_geostationary: bool = False  # Special case for GEO
    
    # Spacecraft Capabilities
    has_propulsion: bool = True     # Can maneuver/deorbit
    has_tracking: bool = True       # Can be tracked from ground
    mass_kg: float = 500.0          # Spacecraft mass
    cross_section_m2: float = 5.0   # Radar cross-section
    
    # Mission Type
    is_crewed: bool = False         # Human spaceflight
    is_interplanetary: bool = False # Beyond Earth orbit
    destination: str = "LEO"        # Target orbit/body
    
    # Communications
    uses_spectrum: bool = True      # RF communications
    frequency_band: str = "Ku"      # Frequency band (S, Ku, Ka, etc.)
    is_spectrum_licensed: bool = True
    
    # Constellation
    is_constellation: bool = False  # Part of multi-satellite system
    constellation_size: int = 1     # Number of satellites
    
    # Reentry
    has_controlled_reentry: bool = True  # Can target reentry location
    reentry_over_ocean: bool = True      # Targets unpopulated area
    
    # Launch Site
    launch_site: str = "Cape Canaveral"
    overflight_population: bool = False  # Flight path over populated areas


@dataclass
class RiskAssessment:
    """Complete risk assessment for a mission."""
    mission: MissionProfile
    factors: List[RiskFactor] = field(default_factory=list)
    overall_score: float = 0.0
    overall_level: RiskLevel = RiskLevel.LOW
    timestamp: str = ""
    
    def add_factor(self, factor: RiskFactor):
        self.factors.append(factor)
        self._recalculate_overall()
    
    def _recalculate_overall(self):
        if not self.factors:
            return
        
        # Weighted average with emphasis on critical factors
        weights = {
            RiskLevel.LOW: 1.0,
            RiskLevel.MEDIUM: 1.5,
            RiskLevel.HIGH: 2.0,
            RiskLevel.CRITICAL: 3.0
        }
        
        total_weight = sum(weights[f.level] for f in self.factors)
        self.overall_score = sum(f.score * weights[f.level] for f in self.factors) / total_weight
        
        # Determine overall level
        if self.overall_score < 25:
            self.overall_level = RiskLevel.LOW
        elif self.overall_score < 50:
            self.overall_level = RiskLevel.MEDIUM
        elif self.overall_score < 75:
            self.overall_level = RiskLevel.HIGH
        else:
            self.overall_level = RiskLevel.CRITICAL


class SpacePolicyCalculator:
    """
    Evaluates space missions against regulatory and safety requirements.
    
    Categories assessed:
    1. Orbital Debris - UN Guidelines, 25-year rule
    2. Collision Risk - Conjunction assessment, maneuverability
    3. Spectrum/Frequency - FCC/ITU coordination
    4. Human Safety - Crew and public safety
    5. Environmental - Launch site impact, reentry
    6. Planetary Protection - Contamination prevention
    """
    
    # Regulatory thresholds
    DEORBIT_RULE_YEARS = 25  # UN guideline for LEO debris
    LEO_ALTITUDE_LIMIT = 2000  # km, above which debris persists longer
    GEO_ALTITUDE = 35786  # km
    
    def __init__(self):
        self.assessment: Optional[RiskAssessment] = None
    
    def assess_mission(self, mission: MissionProfile) -> RiskAssessment:
        """
        Performs a complete risk assessment on the mission.
        """
        from datetime import datetime
        
        self.assessment = RiskAssessment(
            mission=mission,
            timestamp=datetime.now().isoformat()
        )
        
        # Run all assessment categories
        self._assess_debris_risk(mission)
        self._assess_collision_risk(mission)
        self._assess_spectrum_risk(mission)
        self._assess_human_safety(mission)
        self._assess_environmental(mission)
        self._assess_planetary_protection(mission)
        
        return self.assessment
    
    def _assess_debris_risk(self, m: MissionProfile):
        """
        Evaluates orbital debris compliance.
        
        Key regulations:
        - UN Space Debris Mitigation Guidelines
        - US Government Orbital Debris Mitigation Standard Practices
        - FCC 25-year deorbit rule for licensed satellites
        """
        # Estimate orbital lifetime based on altitude
        # Simplified model: lifetime increases exponentially with altitude
        if m.altitude_km < 400:
            estimated_lifetime = 1  # years
        elif m.altitude_km < 600:
            estimated_lifetime = 5
        elif m.altitude_km < 800:
            estimated_lifetime = 25
        elif m.altitude_km < 1000:
            estimated_lifetime = 100
        else:
            estimated_lifetime = 500  # Very long-lived
        
        # If no propulsion, can't actively deorbit
        can_deorbit = m.has_propulsion and m.altitude_km < self.LEO_ALTITUDE_LIMIT
        
        # Calculate risk score
        if can_deorbit:
            score = 10  # Low risk if can maneuver
            level = RiskLevel.LOW
            description = f"Satellite has propulsion for controlled deorbit."
        elif estimated_lifetime <= self.DEORBIT_RULE_YEARS:
            score = 30
            level = RiskLevel.MEDIUM
            description = f"Natural decay within {estimated_lifetime:.0f} years (< 25 year rule)."
        elif m.altitude_km > 800:
            score = 80
            level = RiskLevel.CRITICAL
            description = f"High altitude ({m.altitude_km} km) with {estimated_lifetime:.0f}+ year lifetime."
        else:
            score = 60
            level = RiskLevel.HIGH
            description = f"No propulsion, {estimated_lifetime:.0f} year estimated lifetime."
        
        # Constellation multiplier
        if m.is_constellation and m.constellation_size > 100:
            score = min(100, score * 1.5)
            description += f" Large constellation ({m.constellation_size} sats) increases cumulative risk."
        
        self.assessment.add_factor(RiskFactor(
            name="Orbital Debris Compliance",
            category="Debris",
            level=level,
            score=score,
            description=description,
            mitigation="Ensure propulsion for EOL deorbit or design for natural decay < 25 years.",
            regulation="UN Space Debris Mitigation Guidelines, FCC 47 CFR 25.114"
        ))
    
    def _assess_collision_risk(self, m: MissionProfile):
        """
        Evaluates collision avoidance capabilities.
        
        Key factors:
        - Maneuverability (can avoid tracked debris)
        - Trackability (can be monitored by Space Surveillance Network)
        - Altitude regime (congested vs sparse)
        """
        # LEO is crowded, especially 400-600 km (ISS, Starlink, etc.)
        crowded_regime = 350 < m.altitude_km < 650
        
        if m.has_propulsion and m.has_tracking:
            score = 15 if not crowded_regime else 25
            level = RiskLevel.LOW
            description = "Maneuverable and trackable. Can perform collision avoidance."
        elif m.has_tracking and not m.has_propulsion:
            score = 50 if not crowded_regime else 65
            level = RiskLevel.HIGH if crowded_regime else RiskLevel.MEDIUM
            description = "Trackable but non-maneuverable. Collision avoidance limited."
        elif m.has_propulsion and not m.has_tracking:
            score = 55
            level = RiskLevel.HIGH
            description = "Maneuverable but difficult to track. Coordination challenges."
        else:
            score = 85
            level = RiskLevel.CRITICAL
            description = "Non-maneuverable and difficult to track. High collision risk."
        
        # GEO is critical infrastructure
        if m.is_geostationary:
            score = min(100, score + 20)
            description += " GEO is a limited resource—collisions have outsized impact."
        
        self.assessment.add_factor(RiskFactor(
            name="Collision Risk",
            category="Collision",
            level=level,
            score=score,
            description=description,
            mitigation="Include propulsion system and ensure radar reflectivity > 10 cm².",
            regulation="18th Space Control Squadron Conjunction Assessments"
        ))
    
    def _assess_spectrum_risk(self, m: MissionProfile):
        """
        Evaluates RF spectrum compliance.
        
        Key factors:
        - Licensed vs unlicensed spectrum use
        - Potential for interference with other systems
        - ITU coordination status
        """
        if not m.uses_spectrum:
            self.assessment.add_factor(RiskFactor(
                name="Spectrum Allocation",
                category="Spectrum",
                level=RiskLevel.LOW,
                score=5,
                description="No RF communications. Spectrum regulations not applicable.",
                regulation="N/A"
            ))
            return
        
        if m.is_spectrum_licensed:
            score = 15
            level = RiskLevel.LOW
            description = f"Licensed {m.frequency_band}-band spectrum. FCC/ITU coordinated."
        else:
            score = 70
            level = RiskLevel.HIGH
            description = f"Unlicensed {m.frequency_band}-band use. Potential interference issues."
        
        # Large constellations face additional scrutiny
        if m.is_constellation and m.constellation_size > 1000:
            score = min(100, score + 25)
            description += f" Mega-constellation ({m.constellation_size} sats) requires extensive coordination."
            level = RiskLevel.HIGH if score > 50 else level
        
        self.assessment.add_factor(RiskFactor(
            name="Spectrum Allocation",
            category="Spectrum",
            level=level,
            score=score,
            description=description,
            mitigation="Obtain FCC license, coordinate with ITU, implement interference mitigation.",
            regulation="FCC Part 25, ITU Radio Regulations"
        ))
    
    def _assess_human_safety(self, m: MissionProfile):
        """
        Evaluates human safety risks.
        
        Key factors:
        - Crew safety (if crewed)
        - Public safety during launch
        - Reentry hazards
        """
        factors_assessed = []
        
        # Crew safety
        if m.is_crewed:
            score = 40  # Baseline risk for any crewed mission
            level = RiskLevel.MEDIUM
            description = "Crewed mission. Requires crew safety systems and abort capability."
            
            factors_assessed.append(RiskFactor(
                name="Crew Safety",
                category="Human Safety",
                level=level,
                score=score,
                description=description,
                mitigation="Implement launch abort system, life support redundancy, crew escape systems.",
                regulation="NASA-STD-3001, FAA 14 CFR Part 460"
            ))
        
        # Public safety (launch/reentry)
        reentry_score = 20  # Base
        
        if not m.has_controlled_reentry:
            reentry_score += 40
            reentry_desc = "Uncontrolled reentry. Impact location unpredictable."
            reentry_level = RiskLevel.HIGH
        elif not m.reentry_over_ocean:
            reentry_score += 25
            reentry_desc = "Controlled reentry but not targeting ocean. Some public risk."
            reentry_level = RiskLevel.MEDIUM
        else:
            reentry_desc = "Controlled reentry targeting ocean. Minimal public risk."
            reentry_level = RiskLevel.LOW
        
        # Overflight
        if m.overflight_population:
            reentry_score += 20
            reentry_desc += " Launch trajectory overflies populated areas."
        
        factors_assessed.append(RiskFactor(
            name="Public Safety (Reentry/Launch)",
            category="Human Safety",
            level=reentry_level,
            score=reentry_score,
            description=reentry_desc,
            mitigation="Target reentry over unpopulated areas, flight termination system for launch.",
            regulation="FAA 14 CFR Part 450, Range Safety Requirements"
        ))
        
        for f in factors_assessed:
            self.assessment.add_factor(f)
    
    def _assess_environmental(self, m: MissionProfile):
        """
        Evaluates environmental impact.
        
        Key factors:
        - Launch site environmental assessment
        - Propellant toxicity
        - Wildlife/habitat impact
        """
        # This is simplified—real assessments are extensive (see SpaceX Boca Chica delays)
        
        if m.launch_site in ["Cape Canaveral", "Vandenberg"]:
            score = 20
            level = RiskLevel.LOW
            description = f"Established launch site ({m.launch_site}). Environmental baseline known."
        elif m.launch_site == "Boca Chica":
            score = 45
            level = RiskLevel.MEDIUM
            description = "Boca Chica near wildlife refuge. Enhanced environmental review required."
        else:
            score = 50
            level = RiskLevel.MEDIUM
            description = f"Launch site ({m.launch_site}) environmental status unknown."
        
        self.assessment.add_factor(RiskFactor(
            name="Environmental Impact",
            category="Environmental",
            level=level,
            score=score,
            description=description,
            mitigation="Complete Environmental Impact Statement, implement wildlife mitigation.",
            regulation="National Environmental Policy Act (NEPA), FAA Environmental Review"
        ))
    
    def _assess_planetary_protection(self, m: MissionProfile):
        """
        Evaluates planetary protection requirements.
        
        Key factors:
        - Destination body (Mars, Europa, etc.)
        - Mission type (flyby, orbiter, lander)
        - Biological contamination risk
        """
        if not m.is_interplanetary:
            # Not applicable for Earth orbit missions
            return
        
        # COSPAR planetary protection categories
        protected_bodies = ["Mars", "Europa", "Enceladus", "Titan"]
        
        if m.destination in protected_bodies:
            score = 60
            level = RiskLevel.HIGH
            description = f"Destination ({m.destination}) is a body of astrobiological interest."
            mitigation = "Spacecraft sterilization, bioburden reduction per COSPAR Category III/IV."
        else:
            score = 25
            level = RiskLevel.LOW
            description = f"Destination ({m.destination}) has minimal planetary protection concerns."
            mitigation = "Standard cleanliness protocols."
        
        self.assessment.add_factor(RiskFactor(
            name="Planetary Protection",
            category="Planetary Protection",
            level=level,
            score=score,
            description=description,
            mitigation=mitigation,
            regulation="COSPAR Planetary Protection Policy, NASA NPR 8020.12"
        ))
    
    def generate_report(self) -> str:
        """Generates a text report of the assessment."""
        if self.assessment is None:
            return "No assessment performed."
        
        a = self.assessment
        m = a.mission
        
        lines = [
            "═" * 70,
            "SPACE MISSION REGULATORY RISK ASSESSMENT",
            "═" * 70,
            "",
            f"Mission:    {m.name}",
            f"Timestamp:  {a.timestamp}",
            "",
            "─" * 70,
            "MISSION PARAMETERS",
            "─" * 70,
            f"  Altitude:          {m.altitude_km} km",
            f"  Inclination:       {m.inclination_deg}°",
            f"  Destination:       {m.destination}",
            f"  Propulsion:        {'Yes' if m.has_propulsion else 'No'}",
            f"  Trackable:         {'Yes' if m.has_tracking else 'No'}",
            f"  Crewed:            {'Yes' if m.is_crewed else 'No'}",
            f"  Constellation:     {'Yes' if m.is_constellation else 'No'}",
            f"  Spectrum:          {m.frequency_band + '-band' if m.uses_spectrum else 'None'}",
            "",
            "─" * 70,
            "RISK FACTORS",
            "─" * 70,
        ]
        
        for f in a.factors:
            lines.extend([
                "",
                f"[{f.level.label}] {f.name}",
                f"  Category:    {f.category}",
                f"  Score:       {f.score:.0f}/100",
                f"  Description: {f.description}",
                f"  Mitigation:  {f.mitigation}",
                f"  Regulation:  {f.regulation}",
            ])
        
        lines.extend([
            "",
            "─" * 70,
            "OVERALL ASSESSMENT",
            "─" * 70,
            f"  Overall Score: {a.overall_score:.1f}/100",
            f"  Risk Level:    {a.overall_level.label}",
            "",
            "═" * 70,
        ])
        
        return "\n".join(lines)
    
    def plot_results(self):
        """Creates a visual summary of the risk assessment."""
        if self.assessment is None:
            print("No assessment to plot.")
            return
        
        a = self.assessment
        
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#0b0b10')
        
        # 1. Risk Breakdown by Category (Radar Chart)
        ax1 = fig.add_subplot(2, 2, 1, projection='polar')
        ax1.set_facecolor('#0b0b10')
        
        categories = list(set(f.category for f in a.factors))
        values = []
        for cat in categories:
            cat_factors = [f for f in a.factors if f.category == cat]
            avg_score = np.mean([f.score for f in cat_factors])
            values.append(avg_score)
        
        # Close the radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values_plot = values + [values[0]]
        angles_plot = angles + [angles[0]]
        
        ax1.plot(angles_plot, values_plot, 'o-', linewidth=2, color='#00ffff')
        ax1.fill(angles_plot, values_plot, alpha=0.25, color='#00ffff')
        ax1.set_xticks(angles)
        ax1.set_xticklabels(categories, color='white', size=9)
        ax1.set_ylim(0, 100)
        ax1.set_title("Risk by Category", color='white', pad=20)
        ax1.tick_params(colors='gray')
        ax1.grid(color='gray', alpha=0.3)
        
        # 2. Individual Factor Scores (Horizontal Bar)
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.set_facecolor('#0b0b10')
        
        factor_names = [f.name[:25] + "..." if len(f.name) > 25 else f.name for f in a.factors]
        factor_scores = [f.score for f in a.factors]
        factor_colors = [f.level.color for f in a.factors]
        
        y_pos = np.arange(len(factor_names))
        bars = ax2.barh(y_pos, factor_scores, color=factor_colors, edgecolor='white', alpha=0.8)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(factor_names, color='white', size=9)
        ax2.set_xlabel("Risk Score", color='gray')
        ax2.set_xlim(0, 100)
        ax2.set_title("Individual Risk Factors", color='white')
        ax2.tick_params(colors='gray')
        ax2.grid(axis='x', alpha=0.2)
        
        # Add threshold lines
        ax2.axvline(25, color='#50e3c2', ls='--', alpha=0.5, label='Low')
        ax2.axvline(50, color='#f5e653', ls='--', alpha=0.5, label='Medium')
        ax2.axvline(75, color='#e63946', ls='--', alpha=0.5, label='High')
        
        # 3. Risk Level Distribution (Pie)
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.set_facecolor('#0b0b10')
        
        level_counts = {}
        for level in RiskLevel:
            count = len([f for f in a.factors if f.level == level])
            if count > 0:
                level_counts[level.label] = count
        
        if level_counts:
            colors = [RiskLevel[name].color for name in level_counts.keys()]
            wedges, texts, autotexts = ax3.pie(
                level_counts.values(), 
                labels=level_counts.keys(),
                colors=colors,
                autopct='%1.0f%%',
                startangle=90,
                textprops={'color': 'white'}
            )
            ax3.set_title("Risk Level Distribution", color='white')
        
        # 4. Summary Panel
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.set_facecolor('#0b0b10')
        ax4.axis('off')
        
        m = a.mission
        status_color = a.overall_level.color
        
        summary = (
            f"MISSION: {m.name}\n"
            f"══════════════════════════════════════\n\n"
            f"Orbit:           {m.altitude_km} km × {m.inclination_deg}°\n"
            f"Destination:     {m.destination}\n"
            f"Type:            {'Crewed' if m.is_crewed else 'Uncrewed'}\n"
            f"Constellation:   {'Yes (' + str(m.constellation_size) + ' sats)' if m.is_constellation else 'No'}\n\n"
            f"══════════════════════════════════════\n\n"
            f"Factors Assessed:  {len(a.factors)}\n"
            f"Overall Score:     {a.overall_score:.1f}/100\n"
        )
        
        ax4.text(0.05, 0.95, summary, transform=ax4.transAxes,
                fontsize=11, family='monospace', color='white',
                verticalalignment='top')
        
        ax4.text(0.05, 0.25, f"RISK LEVEL: {a.overall_level.label}", 
                transform=ax4.transAxes, fontsize=18, family='monospace',
                color=status_color, weight='bold')
        
        # Recommendation
        if a.overall_level == RiskLevel.LOW:
            rec = "Mission likely compliant. Proceed with standard licensing."
        elif a.overall_level == RiskLevel.MEDIUM:
            rec = "Some risks identified. Address mitigations before proceeding."
        elif a.overall_level == RiskLevel.HIGH:
            rec = "Significant risks. Requires design changes or waivers."
        else:
            rec = "Critical risks. Mission design requires major revision."
        
        ax4.text(0.05, 0.10, f"Recommendation:\n{rec}", transform=ax4.transAxes,
                fontsize=9, family='monospace', color='gray',
                verticalalignment='top')
        
        plt.suptitle("SPACE MISSION REGULATORY RISK ASSESSMENT", 
                    color='white', fontsize=16, y=0.98)
        plt.tight_layout()
        plt.show()


def run_demo():
    """Demonstrates the Space Policy Calculator with example missions."""
    
    print("=" * 70)
    print("SPACE POLICY RISK CALCULATOR")
    print("Module 4: Human Factors, Regulations, and Space Policy")
    print("=" * 70)
    
    calc = SpacePolicyCalculator()
    
    # --- Scenario 1: Starlink Mission ---
    print("\n[Scenario 1] Starlink Deployment Mission")
    print("-" * 50)
    
    starlink = MissionProfile(
        name="Starlink v2 Mini Deployment",
        altitude_km=550,
        inclination_deg=53,
        has_propulsion=True,
        has_tracking=True,
        mass_kg=800,
        is_constellation=True,
        constellation_size=4500,
        uses_spectrum=True,
        frequency_band="Ku/Ka",
        is_spectrum_licensed=True,
        has_controlled_reentry=True,
        reentry_over_ocean=True,
        launch_site="Cape Canaveral"
    )
    
    assessment = calc.assess_mission(starlink)
    print(calc.generate_report())
    calc.plot_results()
    
    # --- Scenario 2: Crewed Starship to Mars ---
    print("\n[Scenario 2] Crewed Starship Mars Mission")
    print("-" * 50)
    
    mars_mission = MissionProfile(
        name="Starship Mars Crew Transfer",
        altitude_km=250,  # Parking orbit before TMI
        inclination_deg=28.5,
        has_propulsion=True,
        has_tracking=True,
        mass_kg=150000,
        is_crewed=True,
        is_interplanetary=True,
        destination="Mars",
        uses_spectrum=True,
        frequency_band="X/Ka",
        is_spectrum_licensed=True,
        has_controlled_reentry=True,
        reentry_over_ocean=True,
        launch_site="Boca Chica"
    )
    
    assessment = calc.assess_mission(mars_mission)
    print(calc.generate_report())
    calc.plot_results()
    
    # --- Scenario 3: Worst Case (Debris-generating) ---
    print("\n[Scenario 3] High-Risk CubeSat Cluster (Problematic)")
    print("-" * 50)
    
    bad_mission = MissionProfile(
        name="Budget CubeSat Dump",
        altitude_km=850,  # High enough to last decades
        inclination_deg=98,
        has_propulsion=False,  # No deorbit capability
        has_tracking=False,    # Too small to track
        mass_kg=50,
        is_constellation=True,
        constellation_size=200,
        uses_spectrum=True,
        frequency_band="UHF",
        is_spectrum_licensed=False,  # Amateur frequencies, not coordinated
        has_controlled_reentry=False,
        reentry_over_ocean=False,
        launch_site="Unknown"
    )
    
    assessment = calc.assess_mission(bad_mission)
    print(calc.generate_report())
    calc.plot_results()
    
    print("\nAssessment complete!")


if __name__ == "__main__":
    run_demo()

