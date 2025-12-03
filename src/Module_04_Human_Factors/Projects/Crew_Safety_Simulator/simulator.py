"""
Crew Safety Simulator
Module 4: Human Factors, Regulations, and Space Policy
Project 1

Simulates the G-forces and vibrations experienced by astronauts during
launch and landing. Models the crew seat as a mass-spring-damper system
to analyze how different damping configurations affect crew safety.

The key insight: a well-designed seat/harness system acts as a mechanical
low-pass filter, attenuating high-frequency vibrations and smoothing
acceleration spikes to keep crew within safe limits.

Includes realistic profiles from:
- SpaceX Starship / Crew Dragon
- NASA Space Shuttle (historical)
- Russian Soyuz
- Apollo (historical)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Callable, Tuple, List, Dict
import matplotlib.animation as animation

# --- Configuration ---
plt.style.use('dark_background')

# --- Constants ---
G0 = 9.80665  # Standard gravity (m/s^2)

# Human tolerance limits from various sources
# NASA-STD-3001 Vol. 1, Russian GOST standards
NASA_SUSTAINED_G_LIMIT = 4.0   # g's for sustained acceleration (> 10s)
NASA_PEAK_G_LIMIT = 8.0        # g's for short duration spikes (< 1s)
NASA_VIBRATION_LIMIT = 0.5     # g's RMS for comfort
SOYUZ_ABORT_G_LIMIT = 21.0     # g's (Soyuz abort tower - brief)
APOLLO_REENTRY_TYPICAL = 6.5   # g's (Apollo reentry - sustained)

# Historical G-force records (for reference in documentation)
VEHICLE_DATA = {
    'SpaceX Crew Dragon': {
        'launch_max_g': 4.0,      # Nominal launch
        'abort_max_g': 6.0,       # In-flight abort
        'reentry_max_g': 4.5,     # Nominal reentry
        'agency': 'SpaceX',
        'first_crewed': 2020,
        'notes': 'Propulsive abort, parachute landing'
    },
    'SpaceX Starship': {
        'launch_max_g': 3.0,      # Target for crew variant
        'landing_max_g': 4.0,     # Propulsive landing flip
        'reentry_max_g': 2.0,     # Belly-flop controlled
        'agency': 'SpaceX',
        'first_crewed': 2026,     # Projected
        'notes': 'Fully reusable, propulsive landing'
    },
    'NASA Space Shuttle': {
        'launch_max_g': 3.0,      # SRB burnout
        'reentry_max_g': 1.5,     # Glide reentry
        'abort_max_g': 3.0,       # RTLS abort
        'agency': 'NASA',
        'first_crewed': 1981,
        'notes': 'Winged orbiter, runway landing'
    },
    'Russian Soyuz': {
        'launch_max_g': 4.2,      # Stage separation peaks
        'reentry_max_g': 4.5,     # Nominal guided descent
        'ballistic_max_g': 8.0,   # Ballistic reentry (off-nominal)
        'abort_max_g': 21.0,      # Launch abort tower (brief)
        'agency': 'Roscosmos',
        'first_crewed': 1967,
        'notes': 'Most flown crewed vehicle, parachute + retrorocket landing'
    },
    'Apollo Command Module': {
        'launch_max_g': 4.0,      # Saturn V launch
        'reentry_max_g': 6.5,     # Lunar return (faster)
        'abort_max_g': 15.0,      # Launch escape system
        'agency': 'NASA',
        'first_crewed': 1968,
        'notes': 'Lunar missions, ocean splashdown'
    },
    'Chinese Shenzhou': {
        'launch_max_g': 4.0,      # Similar to Soyuz
        'reentry_max_g': 4.5,     # Guided descent
        'agency': 'CNSA',
        'first_crewed': 2003,
        'notes': 'Based on Soyuz design, parachute landing'
    },
    'Blue Origin New Shepard': {
        'launch_max_g': 3.0,      # Suborbital
        'reentry_max_g': 5.0,     # Capsule reentry
        'agency': 'Blue Origin',
        'first_crewed': 2021,
        'notes': 'Suborbital tourism, parachute landing'
    }
}


@dataclass
class SeatParameters:
    """
    Physical parameters for the crew seat system.
    
    The seat is modeled as a spring-damper connecting the astronaut
    to the spacecraft structure. When the spacecraft accelerates,
    the seat filters that motion before it reaches the crew.
    """
    mass: float = 80.0          # kg (astronaut + seat mass)
    spring_k: float = 50000.0   # N/m (seat cushion stiffness)
    damping_c: float = 2000.0   # N·s/m (shock absorber damping)
    name: str = "Standard"
    
    @property
    def natural_frequency(self) -> float:
        """Natural frequency in Hz."""
        return np.sqrt(self.spring_k / self.mass) / (2 * np.pi)
    
    @property
    def damping_ratio(self) -> float:
        """Damping ratio (zeta). < 1 = underdamped, = 1 = critical, > 1 = overdamped."""
        return self.damping_c / (2 * np.sqrt(self.spring_k * self.mass))
    
    @property
    def damping_type(self) -> str:
        zeta = self.damping_ratio
        if zeta < 0.9:
            return "Underdamped"
        elif zeta > 1.1:
            return "Overdamped"
        else:
            return "Critically Damped"


def create_launch_profile(duration: float = 180.0, dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a realistic Starship-like launch acceleration profile.
    
    The profile includes:
    - Initial ramp-up (ignition to max thrust)
    - Throttle-down for Max-Q (aerodynamic pressure)
    - Throttle-up after Max-Q
    - MECO (Main Engine Cutoff) with rapid decrease
    - Stage separation transient
    - Second stage ignition and sustained burn
    
    Returns:
        time: Array of time points (s)
        accel: Array of accelerations (m/s^2)
    """
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 5:
            # Ignition ramp-up: 0 to 1.2g over 5 seconds
            accel[i] = 1.2 * G0 * (time / 5)
        elif time < 60:
            # Max-Q throttle profile: varies between 1.0g and 1.5g
            # Simulates throttle-down around t=40s (Max-Q)
            base = 1.2 * G0
            maxq_factor = 1 - 0.3 * np.exp(-((time - 40) ** 2) / 200)
            accel[i] = base * maxq_factor
        elif time < 150:
            # Post Max-Q: increasing acceleration as fuel depletes
            # Goes from 1.2g to about 3g (mass decreases, thrust constant)
            progress = (time - 60) / 90
            accel[i] = (1.2 + 1.8 * progress) * G0
        elif time < 155:
            # MECO: rapid throttle-down
            progress = (time - 150) / 5
            accel[i] = 3.0 * G0 * (1 - progress) + 0.0 * progress
        elif time < 160:
            # Coast/separation: near zero g with small transients
            accel[i] = 0.1 * G0 * np.sin(2 * np.pi * 2 * (time - 155))
        else:
            # Second stage: steady ~1.5g
            accel[i] = 1.5 * G0
    
    # Add realistic high-frequency vibration (engine rumble)
    # Raptor engines produce vibration in the 10-50 Hz range
    vibration = 0.15 * G0 * np.sin(2 * np.pi * 25 * t)  # 25 Hz component
    vibration += 0.08 * G0 * np.sin(2 * np.pi * 12 * t)  # 12 Hz component
    
    # Vibration is present only during powered flight
    vibration_mask = (t < 155) | (t > 160)
    accel += vibration * vibration_mask
    
    return t, accel


def create_landing_profile(duration: float = 30.0, dt: float = 0.001) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a Starship propulsive landing acceleration profile.
    
    The profile simulates:
    - Belly-flop descent (low g, aerodynamic)
    - Flip maneuver (transient)
    - Landing burn (high g spike)
    - Touchdown (impact transient)
    
    This is the most demanding phase for crew comfort.
    """
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 15:
            # Belly-flop descent: ~0.3g drag deceleration
            accel[i] = 0.3 * G0
        elif time < 18:
            # Flip maneuver: rotation causes lateral g's, approximated
            progress = (time - 15) / 3
            accel[i] = 0.3 * G0 + 2.0 * G0 * np.sin(np.pi * progress)
        elif time < 25:
            # Landing burn: 3-4g deceleration
            progress = (time - 18) / 7
            # Starts high, decreases as velocity drops
            accel[i] = (4.0 - 1.5 * progress) * G0
        elif time < 25.5:
            # Touchdown spike: brief high-g impact
            accel[i] = 6.0 * G0 * np.exp(-20 * (time - 25))
        else:
            # Landed: 1g (Earth gravity)
            accel[i] = 1.0 * G0
    
    return t, accel


# =============================================================================
# VEHICLE-SPECIFIC ACCELERATION PROFILES
# =============================================================================

def create_soyuz_launch_profile(dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a Russian Soyuz rocket launch acceleration profile.
    
    Soyuz is a 3-stage rocket with characteristic G-profile:
    - Stage 1+2 parallel burn (strap-ons + core)
    - Strap-on separation at ~118s with brief G spike
    - Core stage continues, G builds as fuel depletes
    - Stage 2 separation
    - Stage 3 (Block I) ignition for orbital insertion
    
    Data based on: Soyuz MS crew missions, Roscosmos flight data
    Peak G during launch: ~4.2g at stage separation
    """
    duration = 540.0  # ~9 minutes to orbit
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 3:
            # Ignition sequence
            accel[i] = 1.3 * G0 * (time / 3)
        elif time < 118:
            # Stage 1+2 parallel burn (4 strap-ons + core)
            # G increases as fuel depletes: 1.3g → 3.8g
            progress = (time - 3) / 115
            accel[i] = (1.3 + 2.5 * progress) * G0
        elif time < 120:
            # Strap-on separation transient (4 boosters separate)
            # Brief spike then drop as thrust decreases
            sep_progress = (time - 118) / 2
            accel[i] = 3.8 * G0 * (1 - 0.5 * sep_progress)
        elif time < 287:
            # Core stage alone - continues to build G
            # 1.9g → 4.2g (peak of Soyuz launch)
            progress = (time - 120) / 167
            accel[i] = (1.9 + 2.3 * progress) * G0
        elif time < 290:
            # Stage 2 separation
            sep_progress = (time - 287) / 3
            accel[i] = 4.2 * G0 * (1 - sep_progress)
        elif time < 295:
            # Brief coast
            accel[i] = 0.05 * G0
        elif time < 530:
            # Stage 3 (Block I) - lower G, vacuum optimized
            progress = (time - 295) / 235
            accel[i] = (0.8 + 1.5 * progress) * G0
        else:
            # SECO - orbital insertion
            accel[i] = 0.0
    
    # Soyuz has significant vibration from RD-107/108 engines
    vibration = 0.12 * G0 * np.sin(2 * np.pi * 18 * t)
    vibration += 0.06 * G0 * np.sin(2 * np.pi * 35 * t)
    powered_mask = t < 530
    accel += vibration * powered_mask
    
    return t, accel


def create_soyuz_reentry_profile(ballistic: bool = False, dt: float = 0.001) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a Soyuz capsule reentry and landing profile.
    
    Two modes:
    - Guided descent (nominal): Peak ~4.5g, gentle
    - Ballistic descent (off-nominal): Peak ~8g, steeper
    
    The 2008 Soyuz TMA-11 ballistic reentry reached ~8g.
    Normal parachute deployment at ~10km, retrorockets at ~1m.
    """
    duration = 420.0 if not ballistic else 350.0  # ~7 min nominal, ~6 min ballistic
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    if ballistic:
        # Ballistic (steep) reentry - higher G, shorter duration
        for i, time in enumerate(t):
            if time < 60:
                # Initial reentry interface
                progress = time / 60
                accel[i] = progress * 2.0 * G0
            elif time < 180:
                # Peak heating/deceleration zone - 8g peak
                progress = (time - 60) / 120
                # Bell curve with peak at middle
                accel[i] = (2.0 + 6.0 * np.sin(np.pi * progress)) * G0
            elif time < 280:
                # Drogue chute deployment - oscillations
                accel[i] = 3.0 * G0 * np.exp(-0.02 * (time - 180))
            elif time < 340:
                # Main chute descent
                accel[i] = 1.0 * G0
            elif time < 345:
                # Retrorocket firing just before touchdown
                accel[i] = 4.0 * G0
            else:
                # Landed
                accel[i] = 1.0 * G0
    else:
        # Guided (nominal) reentry - lower G, more comfortable
        for i, time in enumerate(t):
            if time < 90:
                # Gradual reentry with lift vector control
                progress = time / 90
                accel[i] = progress * 1.5 * G0
            elif time < 240:
                # Peak deceleration zone - 4.5g peak
                progress = (time - 90) / 150
                accel[i] = (1.5 + 3.0 * np.sin(np.pi * progress)) * G0
            elif time < 320:
                # Drogue chute
                accel[i] = 2.5 * G0 * np.exp(-0.015 * (time - 240))
            elif time < 410:
                # Main chute descent
                accel[i] = 1.0 * G0
            elif time < 415:
                # Retrorockets (soft landing system)
                accel[i] = 3.5 * G0
            else:
                # Landed
                accel[i] = 1.0 * G0
    
    return t, accel


def create_shuttle_launch_profile(dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a NASA Space Shuttle launch acceleration profile.
    
    The Shuttle had a unique profile:
    - SRB + SSME ignition at T-0
    - Roll program at T+7s
    - Throttle-down for Max-Q (~T+52s)
    - SRB separation at ~T+126s (brief dip then recovery)
    - SSME throttle-up as fuel depletes
    - Peak ~3g before MECO
    - MECO at ~T+510s
    
    Data based on: NASA STS mission data
    """
    duration = 520.0  # ~8.5 minutes to MECO
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 7:
            # Ignition and liftoff
            accel[i] = 1.5 * G0 * (time / 7)
        elif time < 52:
            # Ascent to Max-Q - throttle down to limit q
            progress = (time - 7) / 45
            # Throttle bucket: down then up
            throttle_factor = 1.0 - 0.3 * np.sin(np.pi * progress)
            accel[i] = 1.5 * G0 * throttle_factor
        elif time < 126:
            # Post Max-Q, SRBs still burning
            # G increases: 1.5g → 2.5g
            progress = (time - 52) / 74
            accel[i] = (1.5 + 1.0 * progress) * G0
        elif time < 130:
            # SRB separation - thrust dip
            accel[i] = 1.0 * G0
        elif time < 510:
            # Main engine only - G builds as fuel depletes
            # 1.0g → 3.0g (shuttle throttled to limit at 3g)
            progress = (time - 130) / 380
            accel[i] = (1.0 + 2.0 * progress) * G0
            # Shuttle throttled down near end to limit to 3g
            if accel[i] > 3.0 * G0:
                accel[i] = 3.0 * G0
        else:
            # MECO
            accel[i] = 0.0
    
    # Shuttle had lower vibration than most rockets due to liquid engines
    vibration = 0.08 * G0 * np.sin(2 * np.pi * 20 * t)
    # SRBs added more vibration
    srb_mask = t < 126
    srb_vibration = 0.15 * G0 * np.sin(2 * np.pi * 15 * t) * srb_mask
    
    powered_mask = t < 510
    accel += (vibration + srb_vibration) * powered_mask
    
    return t, accel


def create_apollo_reentry_profile(dt: float = 0.001) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates an Apollo Command Module lunar return reentry profile.
    
    Apollo reentry was challenging due to high velocity (~11 km/s vs ~7.8 km/s for LEO).
    The CM used skip reentry and lift vector control to manage G-loads.
    
    Typical profile:
    - Initial entry interface at 122 km
    - First deceleration pulse (can skip out)
    - Second deceleration (most severe)
    - Peak ~6.5g (Apollo 11 saw 6.56g)
    - Drogue chutes at ~7 km
    - Main chutes at ~3 km
    - Splashdown
    
    Data based on: Apollo mission reports, NASA technical notes
    """
    duration = 900.0  # ~15 minutes from entry interface to splashdown
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 60:
            # Initial entry - gradual heating
            progress = time / 60
            accel[i] = progress * 1.5 * G0
        elif time < 180:
            # First deceleration pulse
            progress = (time - 60) / 120
            accel[i] = (1.5 + 3.0 * np.sin(np.pi * progress)) * G0
        elif time < 240:
            # Possible skip phase (reduced G)
            accel[i] = 1.0 * G0
        elif time < 420:
            # Second deceleration - most severe, peak 6.5g
            progress = (time - 240) / 180
            # Gaussian-like peak
            peak_factor = np.exp(-((progress - 0.4) ** 2) / 0.05)
            accel[i] = (1.5 + 5.0 * peak_factor) * G0
        elif time < 600:
            # High atmosphere - decreasing G
            progress = (time - 420) / 180
            accel[i] = (2.5 - 1.5 * progress) * G0
        elif time < 700:
            # Drogue chute deployment - oscillations
            accel[i] = 2.0 * G0 + 0.5 * G0 * np.sin(2 * np.pi * 0.5 * (time - 600))
        elif time < 880:
            # Main chute descent
            accel[i] = 1.0 * G0
        elif time < 890:
            # Splashdown impact
            impact_t = time - 880
            accel[i] = 1.0 * G0 + 8.0 * G0 * np.exp(-impact_t / 0.5)
        else:
            # Floating
            accel[i] = 1.0 * G0
    
    return t, accel


def create_crew_dragon_launch_profile(dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a SpaceX Crew Dragon / Falcon 9 launch profile.
    
    Falcon 9 with Crew Dragon has a human-rated profile:
    - 9 Merlin engines at liftoff
    - Max-Q throttle-down
    - MECO and stage separation at ~T+150s
    - Second stage Mvac ignition
    - Peak ~4g before SECO
    
    Data based on: SpaceX crew mission telemetry, NASA Commercial Crew data
    """
    duration = 570.0  # ~9.5 minutes to orbit insertion
    t = np.arange(0, duration, dt)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 5:
            # Ignition and liftoff
            accel[i] = 1.2 * G0 * (time / 5)
        elif time < 60:
            # Ascent through Max-Q with throttle management
            progress = (time - 5) / 55
            # Throttle bucket around Max-Q
            maxq_factor = 1.0 - 0.25 * np.exp(-((time - 40) ** 2) / 100)
            accel[i] = 1.2 * G0 * (1 + 0.8 * progress) * maxq_factor
        elif time < 150:
            # Stage 1 burn continues - G builds
            progress = (time - 60) / 90
            accel[i] = (1.6 + 2.0 * progress) * G0
        elif time < 155:
            # MECO and stage separation
            accel[i] = 0.5 * G0 * (1 - (time - 150) / 5)
        elif time < 160:
            # Brief coast
            accel[i] = 0.0
        elif time < 500:
            # Stage 2 burn - lower thrust, G builds as fuel depletes
            progress = (time - 160) / 340
            accel[i] = (0.8 + 3.2 * progress) * G0
            # Throttle down to limit crew G to 4.0
            if accel[i] > 4.0 * G0:
                accel[i] = 4.0 * G0
        else:
            # SECO - orbital insertion
            accel[i] = 0.0
    
    # Merlin engines are relatively smooth
    vibration = 0.1 * G0 * np.sin(2 * np.pi * 22 * t)
    powered_mask = (t < 150) | ((t > 160) & (t < 500))
    accel += vibration * powered_mask
    
    return t, accel


def create_new_shepard_launch_profile() -> Tuple[np.ndarray, np.ndarray]:
    """
    Blue Origin New Shepard suborbital flight profile.
    ~11 minutes total, reaches ~100km altitude.
    Notable for relatively gentle 3g max during ascent.
    """
    t = np.linspace(0, 660, 6600)  # 11 minutes
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 10:
            # Engine ignition ramp
            accel[i] = (time / 10) * 2.0 * G0
        elif time < 140:
            # Main burn - BE-3 engine, max ~3g
            progress = (time - 10) / 130
            accel[i] = (2.0 + 1.0 * progress) * G0
        elif time < 150:
            # MECO coast
            accel[i] = 0.0
        elif time < 240:
            # Microgravity phase (above Karman line)
            accel[i] = 0.0
        elif time < 400:
            # Reentry - capsule experiences up to 5g
            progress = (time - 240) / 160
            peak = np.exp(-((progress - 0.5) ** 2) / 0.05)
            accel[i] = 5.0 * G0 * peak + 1.0 * G0
        elif time < 600:
            # Parachute descent - ~1.5g
            accel[i] = 1.5 * G0
        else:
            # Touchdown
            accel[i] = 1.0 * G0
    
    return t, accel


def create_shenzhou_launch_profile() -> Tuple[np.ndarray, np.ndarray]:
    """
    Chinese Shenzhou spacecraft on Long March 2F.
    Similar profile to Soyuz - reaches ~4g at staging.
    """
    t = np.linspace(0, 600, 6000)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 10:
            # Liftoff
            accel[i] = (time / 10) * 1.5 * G0
        elif time < 120:
            # Stage 1 - 4 boosters + core
            progress = (time - 10) / 110
            accel[i] = (1.5 + 2.5 * progress) * G0
        elif time < 140:
            # Booster separation, brief dip
            accel[i] = 0.8 * G0
        elif time < 280:
            # Stage 2
            progress = (time - 140) / 140
            accel[i] = (1.2 + 2.8 * progress) * G0
        elif time < 300:
            # Staging
            accel[i] = 0.5 * G0
        elif time < 550:
            # Stage 3 - upper stage to orbit
            progress = (time - 300) / 250
            accel[i] = (0.8 + 2.5 * progress) * G0
        else:
            accel[i] = 0.0
    
    # Slight vibration from solid boosters
    booster_mask = (t > 10) & (t < 120)
    vibration = 0.15 * G0 * np.sin(2 * np.pi * 25 * t)
    accel += vibration * booster_mask
    
    return t, accel


def create_shenzhou_reentry_profile() -> Tuple[np.ndarray, np.ndarray]:
    """
    Shenzhou capsule reentry - similar to Soyuz guided descent.
    ~4.5g typical peak.
    """
    t = np.linspace(0, 500, 5000)
    accel = np.zeros_like(t)
    
    for i, time in enumerate(t):
        if time < 50:
            # Deorbit burn (retrograde)
            accel[i] = 0.5 * G0
        elif time < 100:
            # Atmospheric interface
            progress = (time - 50) / 50
            accel[i] = progress * 1.5 * G0
        elif time < 200:
            # Peak heating / deceleration
            progress = (time - 100) / 100
            peak = np.exp(-((progress - 0.5) ** 2) / 0.08)
            accel[i] = 4.5 * G0 * peak + 1.0 * G0
        elif time < 350:
            # Drogue phase
            accel[i] = 2.0 * G0 * (1 - (time - 200) / 150)
        elif time < 480:
            # Main chute
            accel[i] = 1.5 * G0
        else:
            # Soft landing rockets
            accel[i] = 2.5 * G0
    
    return t, accel


def get_vehicle_profile(vehicle: str, phase: str = 'launch', **kwargs) -> Tuple[np.ndarray, np.ndarray, str]:
    """
    Returns the appropriate acceleration profile for a given vehicle and phase.
    
    Parameters:
        vehicle: One of 'starship', 'soyuz', 'shuttle', 'apollo', 'crew_dragon'
        phase: 'launch', 'reentry', or 'landing'
        **kwargs: Additional options (e.g., 'ballistic' for Soyuz reentry)
    
    Returns:
        (time, accel, description)
    """
    vehicle = vehicle.lower().replace(' ', '_')
    
    profiles = {
        ('starship', 'launch'): (create_launch_profile, "SpaceX Starship Launch"),
        ('starship', 'landing'): (create_landing_profile, "SpaceX Starship Landing"),
        ('soyuz', 'launch'): (create_soyuz_launch_profile, "Soyuz MS Launch"),
        ('soyuz', 'reentry'): (create_soyuz_reentry_profile, "Soyuz Capsule Reentry"),
        ('shuttle', 'launch'): (create_shuttle_launch_profile, "Space Shuttle Launch"),
        ('apollo', 'reentry'): (create_apollo_reentry_profile, "Apollo CM Lunar Return"),
        ('crew_dragon', 'launch'): (create_crew_dragon_launch_profile, "Crew Dragon Launch"),
        ('new_shepard', 'launch'): (create_new_shepard_launch_profile, "Blue Origin New Shepard"),
        ('shenzhou', 'launch'): (create_shenzhou_launch_profile, "CNSA Shenzhou Launch"),
        ('shenzhou', 'reentry'): (create_shenzhou_reentry_profile, "CNSA Shenzhou Reentry"),
    }
    
    key = (vehicle, phase)
    if key not in profiles:
        raise ValueError(f"Unknown profile: {vehicle} {phase}. Available: {list(profiles.keys())}")
    
    func, desc = profiles[key]
    
    # Handle special kwargs
    if vehicle == 'soyuz' and phase == 'reentry':
        ballistic = kwargs.get('ballistic', False)
        t, a = func(ballistic=ballistic)
        if ballistic:
            desc += " (Ballistic)"
    else:
        t, a = func()
    
    return t, a, desc


class CrewSafetySimulator:
    """
    Simulates the dynamic response of a crew member in their seat
    when subjected to spacecraft accelerations.
    
    The model treats the astronaut+seat as a single-DOF mass-spring-damper
    system. The "displacement" x represents how much the astronaut moves
    relative to the spacecraft structure (compression of seat cushion).
    
    The acceleration felt by the astronaut is the spacecraft acceleration
    minus the relative acceleration (x''). A well-tuned seat system
    reduces peak accelerations experienced by the crew.
    """
    
    def __init__(self, seat: SeatParameters):
        self.seat = seat
        self.results = None
        
    def _equations_of_motion(self, state: np.ndarray, t: float, 
                              accel_func: Callable) -> np.ndarray:
        """
        Defines the ODE for the mass-spring-damper system.
        
        State: [x, x_dot] where x is relative displacement from equilibrium
        
        Equation: m*x'' + c*x' + k*x = m*a_spacecraft(t)
        
        Rearranged: x'' = a_spacecraft(t) - (c/m)*x' - (k/m)*x
        """
        x, x_dot = state
        
        # External acceleration (spacecraft)
        a_ext = accel_func(t)
        
        # Equation of motion
        x_ddot = a_ext - (self.seat.damping_c / self.seat.mass) * x_dot \
                       - (self.seat.spring_k / self.seat.mass) * x
        
        return np.array([x_dot, x_ddot])
    
    def simulate(self, time: np.ndarray, accel: np.ndarray) -> dict:
        """
        Runs the simulation for a given acceleration profile.
        
        Parameters:
            time: Array of time points
            accel: Array of spacecraft accelerations (m/s^2)
        
        Returns:
            Dictionary with simulation results
        """
        # Create interpolation function for acceleration
        from scipy.interpolate import interp1d
        accel_func = interp1d(time, accel, kind='linear', 
                              bounds_error=False, fill_value=accel[-1])
        
        # Initial conditions: at rest, no displacement
        state0 = np.array([0.0, 0.0])
        
        # Solve ODE
        solution = odeint(self._equations_of_motion, state0, time,
                         args=(accel_func,))
        
        x = solution[:, 0]           # Relative displacement (m)
        x_dot = solution[:, 1]       # Relative velocity (m/s)
        
        # Calculate accelerations
        # The astronaut feels: spacecraft accel - relative accel of mass
        # Relative accel can be found from the equation of motion
        x_ddot = np.gradient(x_dot, time)  # Numerical differentiation
        
        # Acceleration experienced by crew (in g's)
        crew_accel = (accel - x_ddot) / G0
        spacecraft_accel = accel / G0
        
        # Store results
        self.results = {
            'time': time,
            'spacecraft_accel_g': spacecraft_accel,
            'crew_accel_g': crew_accel,
            'displacement_cm': x * 100,  # Convert to cm
            'velocity': x_dot,
            'peak_spacecraft_g': np.max(np.abs(spacecraft_accel)),
            'peak_crew_g': np.max(np.abs(crew_accel)),
            'rms_spacecraft_g': np.sqrt(np.mean(spacecraft_accel**2)),
            'rms_crew_g': np.sqrt(np.mean(crew_accel**2)),
            'max_displacement_cm': np.max(np.abs(x)) * 100,
            'seat_params': self.seat
        }
        
        return self.results
    
    def assess_safety(self) -> dict:
        """
        Evaluates the simulation results against NASA safety limits.
        """
        if self.results is None:
            raise ValueError("Must run simulation first")
        
        r = self.results
        
        assessment = {
            'sustained_g_ok': r['rms_crew_g'] < NASA_SUSTAINED_G_LIMIT,
            'peak_g_ok': r['peak_crew_g'] < NASA_PEAK_G_LIMIT,
            'vibration_ok': True,  # Would need frequency analysis for proper check
            'overall_safe': True,
            'reduction_percent': (1 - r['peak_crew_g'] / r['peak_spacecraft_g']) * 100
        }
        
        assessment['overall_safe'] = assessment['sustained_g_ok'] and assessment['peak_g_ok']
        
        return assessment
    
    def plot_results(self, title: str = "Crew Safety Analysis"):
        """Creates a comprehensive visualization of the simulation results."""
        if self.results is None:
            raise ValueError("Must run simulation first")
        
        from matplotlib.patches import FancyBboxPatch
        
        r = self.results
        assessment = self.assess_safety()
        
        fig = plt.figure(figsize=(16, 11))
        fig.patch.set_facecolor('#050a12')
        
        # Color palette for visualization
        cyan = '#00d4ff'
        teal = '#00ff9f'
        orange = '#ff6b35'
        gold = '#ffd700'
        red = '#ff3366'
        soft_white = '#b0d4e8'
        
        # 1. Acceleration Comparison
        ax1 = fig.add_subplot(2, 2, 1)
        style_axis_dark(ax1, "G-FORCE PROFILE", "Time [seconds]", "Acceleration [g]")
        
        # Glow effect for lines
        ax1.plot(r['time'], r['spacecraft_accel_g'], color=orange, lw=6, alpha=0.15, zorder=2)
        ax1.plot(r['time'], r['spacecraft_accel_g'], color=orange, alpha=0.7, 
                 lw=2, label='VEHICLE', zorder=3)
        
        ax1.plot(r['time'], r['crew_accel_g'], color=cyan, lw=6, alpha=0.15, zorder=2)
        ax1.plot(r['time'], r['crew_accel_g'], color=cyan, lw=2.5, 
                 label='CREW [FILTERED]', zorder=3)
        
        ax1.axhline(NASA_SUSTAINED_G_LIMIT, color=gold, ls='--', lw=2,
                   alpha=0.8, label=f'SUSTAINED [{NASA_SUSTAINED_G_LIMIT}g]')
        ax1.axhline(NASA_PEAK_G_LIMIT, color=red, ls='--', lw=2,
                   alpha=0.8, label=f'PEAK [{NASA_PEAK_G_LIMIT}g]')
        
        leg1 = ax1.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                         labelcolor=soft_white, fontsize=9, framealpha=0.9)
        leg1.get_frame().set_linewidth(1.5)
        
        # 2. Seat Displacement
        ax2 = fig.add_subplot(2, 2, 2)
        style_axis_dark(ax2, "SEAT DISPLACEMENT", "Time [seconds]", "Displacement [cm]")
        
        ax2.fill_between(r['time'], 0, r['displacement_cm'], color=teal, alpha=0.3, zorder=2)
        ax2.plot(r['time'], r['displacement_cm'], color=teal, lw=6, alpha=0.15, zorder=2)
        ax2.plot(r['time'], r['displacement_cm'], color=teal, lw=2.5, zorder=3)
        ax2.axhline(0, color='white', alpha=0.3, lw=1)
        
        # 3. G-Force Reduction
        ax3 = fig.add_subplot(2, 2, 3)
        style_axis_dark(ax3, "ATTENUATION ANALYSIS", "Time [seconds]", "G Reduction")
        
        reduction = r['spacecraft_accel_g'] - r['crew_accel_g']
        ax3.fill_between(r['time'], 0, reduction, where=reduction > 0,
                        color=teal, alpha=0.4, label='ABSORPTION', zorder=2)
        ax3.fill_between(r['time'], 0, reduction, where=reduction < 0,
                        color=red, alpha=0.4, label='AMPLIFICATION', zorder=2)
        ax3.plot(r['time'], reduction, color='white', lw=1.5, alpha=0.6, zorder=3)
        ax3.axhline(0, color='white', alpha=0.5, lw=1)
        
        leg3 = ax3.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                         labelcolor=soft_white, fontsize=9, framealpha=0.9)
        leg3.get_frame().set_linewidth(1.5)
        
        # 4. Summary Panel
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.set_facecolor('#050a12')
        ax4.axis('off')
        
        # Info panel
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                               boxstyle="round,pad=0.02,rounding_size=0.02",
                               facecolor='#0a1628', edgecolor=cyan,
                               linewidth=2, alpha=0.9,
                               transform=ax4.transAxes, zorder=1)
        ax4.add_patch(panel)
        
        seat = r['seat_params']
        status_color = teal if assessment['overall_safe'] else red
        status_text = "◆ NOMINAL ◆" if assessment['overall_safe'] else "◆ WARNING ◆"
        
        # Header
        from matplotlib.lines import Line2D
        ax4.text(0.5, 0.95, "◢ SYSTEM STATUS ◣", transform=ax4.transAxes,
                fontsize=14, fontweight='bold', color=cyan, ha='center', va='top')
        header_line = Line2D([0.1, 0.9], [0.89, 0.89], color=cyan, alpha=0.5, 
                            lw=1, transform=ax4.transAxes)
        ax4.add_line(header_line)
        
        # Configuration section
        ax4.text(0.08, 0.83, "SEAT CONFIGURATION", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=gold)
        config_text = (
            f"► Mass:           {seat.mass:.0f} kg\n"
            f"► Spring (k):     {seat.spring_k:.0f} N/m\n"
            f"► Damping (c):    {seat.damping_c:.0f} N·s/m\n"
            f"► Natural Freq:   {seat.natural_frequency:.2f} Hz\n"
            f"► Damping Ratio:  {seat.damping_ratio:.2f} ({seat.damping_type})"
        )
        ax4.text(0.10, 0.77, config_text, transform=ax4.transAxes,
                fontsize=10, color=soft_white, va='top', family='monospace')
        
        # Results section
        ax4.text(0.08, 0.48, "ANALYSIS RESULTS", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=orange)
        results_text = (
            f"► Peak Vehicle G:   {r['peak_spacecraft_g']:.2f} g\n"
            f"► Peak Crew G:      {r['peak_crew_g']:.2f} g\n"
            f"► G Reduction:      {assessment['reduction_percent']:.1f}%\n"
            f"► Max Displacement: {r['max_displacement_cm']:.2f} cm"
        )
        ax4.text(0.10, 0.42, results_text, transform=ax4.transAxes,
                fontsize=10, color=soft_white, va='top', family='monospace')
        
        # Safety assessment
        ax4.text(0.08, 0.20, "SAFETY ASSESSMENT", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=teal)
        sustained_icon = "●" if assessment['sustained_g_ok'] else "○"
        peak_icon = "●" if assessment['peak_g_ok'] else "○"
        sustained_color = teal if assessment['sustained_g_ok'] else red
        peak_color = teal if assessment['peak_g_ok'] else red
        
        ax4.text(0.10, 0.14, f"{sustained_icon} Sustained G (<{NASA_SUSTAINED_G_LIMIT}g)", 
                transform=ax4.transAxes, fontsize=10, color=sustained_color, va='top')
        ax4.text(0.10, 0.09, f"{peak_icon} Peak G (<{NASA_PEAK_G_LIMIT}g)",
                transform=ax4.transAxes, fontsize=10, color=peak_color, va='top')
        
        # Overall status
        ax4.text(0.5, 0.03, status_text, transform=ax4.transAxes,
                fontsize=14, fontweight='bold', color=status_color, ha='center')
        
        # Main title
        fig.text(0.5, 0.97, "◢ CREW SAFETY ANALYSIS ◣",
                fontsize=20, fontweight='bold', color=cyan, ha='center', va='top')
        fig.text(0.5, 0.935, title,
                fontsize=12, color=soft_white, ha='center', va='top', alpha=0.8)
        
        plt.tight_layout(rect=[0, 0, 1, 0.92])
        plt.show()
        
        return fig


def compare_seat_configurations(time: np.ndarray, accel: np.ndarray,
                                 seats: List[SeatParameters]):
    """
    Compares multiple seat configurations on the same acceleration profile.
    Interactive trade study visualization for engineering analysis.
    """
    from matplotlib.patches import FancyBboxPatch
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.patch.set_facecolor('#050a12')
    
    # Color palette for multiple configurations
    colors = ['#00d4ff', '#00ff9f', '#ffd700', '#ff6b35']
    soft_white = '#b0d4e8'
    
    results = []
    for i, seat in enumerate(seats):
        sim = CrewSafetySimulator(seat)
        r = sim.simulate(time, accel)
        results.append(r)
    
    # Plot 1: Crew acceleration comparison
    ax1 = axes[0, 0]
    style_axis_dark(ax1, "CREW G-FORCE COMPARISON", "Time [seconds]", "Acceleration [g]")
    
    ax1.plot(time, accel / G0, color='white', alpha=0.2, lw=1, label='VEHICLE')
    for i, r in enumerate(results):
        ax1.plot(r['time'], r['crew_accel_g'], color=colors[i], lw=6, alpha=0.15)
        ax1.plot(r['time'], r['crew_accel_g'], color=colors[i], lw=2.5, 
                label=f"{seats[i].name.upper()}")
    ax1.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=2, alpha=0.8)
    
    leg1 = ax1.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor=soft_white, fontsize=9, framealpha=0.9)
    leg1.get_frame().set_linewidth(1.5)
    
    # Plot 2: Displacement comparison
    ax2 = axes[0, 1]
    style_axis_dark(ax2, "DISPLACEMENT ANALYSIS", "Time [seconds]", "Displacement [cm]")
    
    for i, r in enumerate(results):
        ax2.plot(r['time'], r['displacement_cm'], color=colors[i], lw=6, alpha=0.15)
        ax2.plot(r['time'], r['displacement_cm'], color=colors[i], lw=2.5,
                label=f"{seats[i].name.upper()}")
    
    leg2 = ax2.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor=soft_white, fontsize=9, framealpha=0.9)
    leg2.get_frame().set_linewidth(1.5)
    
    # Plot 3: Bar chart of peak G
    ax3 = axes[1, 0]
    style_axis_dark(ax3, "PEAK G-FORCE RANKING", "", "Peak Acceleration [g]")
    
    names = [s.name.upper() for s in seats]
    peak_gs = [r['peak_crew_g'] for r in results]
    
    bars = ax3.bar(names, peak_gs, color=colors[:len(seats)], 
                  edgecolor='white', linewidth=2, alpha=0.85)
    
    # Add value labels
    for bar, val, color in zip(bars, peak_gs, colors):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                f'{val:.2f}g', ha='center', va='bottom', color=color,
                fontsize=10, fontweight='bold')
    
    ax3.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=2, alpha=0.8,
               label=f'LIMIT [{NASA_PEAK_G_LIMIT}g]')
    ax3.tick_params(axis='x', colors=soft_white)
    
    leg3 = ax3.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor=soft_white, fontsize=9, framealpha=0.9)
    leg3.get_frame().set_linewidth(1.5)
    
    # Plot 4: Summary table
    ax4 = axes[1, 1]
    ax4.set_facecolor('#050a12')
    ax4.axis('off')
    
    # Holographic panel
    panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                           boxstyle="round,pad=0.02,rounding_size=0.02",
                           facecolor='#0a1628', edgecolor='#00d4ff',
                           linewidth=2, alpha=0.9,
                           transform=ax4.transAxes, zorder=1)
    ax4.add_patch(panel)
    
    # Header
    from matplotlib.lines import Line2D
    ax4.text(0.5, 0.95, "◢ CONFIGURATION ANALYSIS ◣", transform=ax4.transAxes,
            fontsize=13, fontweight='bold', color='#00d4ff', ha='center', va='top')
    header_line = Line2D([0.1, 0.9], [0.89, 0.89], color='#00d4ff', alpha=0.5, 
                        lw=1, transform=ax4.transAxes)
    ax4.add_line(header_line)
    
    # Create custom table display
    y_pos = 0.82
    headers = ['CONFIG', 'ζ', 'PEAK G', 'DISP', 'REDUCTION', 'STATUS']
    x_positions = [0.08, 0.30, 0.45, 0.60, 0.75, 0.90]
    
    for x, header in zip(x_positions, headers):
        ax4.text(x, y_pos, header, transform=ax4.transAxes,
                fontsize=9, fontweight='bold', color='#ffd700', ha='left')
    
    table_line = Line2D([0.05, 0.95], [0.78, 0.78], color='#ffd700', alpha=0.3, 
                       lw=1, transform=ax4.transAxes)
    ax4.add_line(table_line)
    
    for i, (seat, r) in enumerate(zip(seats, results)):
        y = y_pos - 0.12 - i * 0.15
        reduction = (1 - r['peak_crew_g'] / r['peak_spacecraft_g']) * 100
        safe = r['peak_crew_g'] < NASA_PEAK_G_LIMIT
        status_text = "● PASS" if safe else "○ FAIL"
        status_color = '#00ff9f' if safe else '#ff3366'
        
        row_data = [
            seat.name,
            f"{seat.damping_ratio:.2f}",
            f"{r['peak_crew_g']:.2f}g",
            f"{r['max_displacement_cm']:.1f}cm",
            f"{reduction:.1f}%",
            status_text
        ]
        
        for x, val in zip(x_positions[:-1], row_data[:-1]):
            ax4.text(x, y, val, transform=ax4.transAxes,
                    fontsize=10, color=colors[i], ha='left')
        ax4.text(x_positions[-1], y, status_text, transform=ax4.transAxes,
                fontsize=10, color=status_color, ha='left')
    
    # Best configuration indicator
    best_idx = np.argmin(peak_gs)
    ax4.text(0.5, 0.08, f"◆ OPTIMAL: {seats[best_idx].name.upper()} ◆",
            transform=ax4.transAxes, fontsize=12, fontweight='bold',
            color='#00ff9f', ha='center')
    
    # Main title
    fig.text(0.5, 0.97, "◢ SEAT CONFIGURATION TRADE STUDY ◣",
            fontsize=20, fontweight='bold', color='#00d4ff', ha='center', va='top')
    
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()
    
    return results


def create_dark_background(ax, color='#060d18'):
    """Creates a styled dark background for technical plots."""
    ax.set_facecolor(color)
    
    # Add faint horizontal scan lines effect
    for i in range(0, 100, 4):
        ax.axhspan(i/100, (i+1)/100, alpha=0.015, color='#00d4ff',
                  transform=ax.transAxes, zorder=0)


def style_axis_dark(ax, title="", xlabel="", ylabel=""):
    """Applies dark theme styling for aerospace engineering plots."""
    from matplotlib.lines import Line2D
    from matplotlib.patches import FancyBboxPatch
    
    # Dark background for readability
    create_dark_background(ax)
    
    # Title with accent line
    if title:
        ax.set_title(title, color='#00d4ff', fontsize=12, fontweight='bold',
                    pad=12, loc='left', fontfamily='monospace')
        # Accent underline
        line = Line2D([0, 0.35], [1.02, 1.02], color='#00d4ff', alpha=0.8,
                     lw=2, transform=ax.transAxes, clip_on=False)
        ax.add_line(line)
        # Subtle glow
        line_glow = Line2D([0, 0.35], [1.02, 1.02], color='#00d4ff', alpha=0.2,
                          lw=6, transform=ax.transAxes, clip_on=False)
        ax.add_line(line_glow)
    
    # Labels - LARGER and HIGH CONTRAST (bright cyan)
    ax.set_xlabel(xlabel, color='#00d4ff', fontsize=11, labelpad=10, 
                 fontfamily='monospace', fontweight='bold')
    ax.set_ylabel(ylabel, color='#00d4ff', fontsize=11, labelpad=10, 
                 fontfamily='monospace', fontweight='bold')
    
    # Ticks - brighter for visibility
    ax.tick_params(colors='#4db8d4', labelsize=9, length=5, width=1.5)
    
    # Border styling - glowing effect
    for spine in ax.spines.values():
        spine.set_color('#0e4d64')
        spine.set_linewidth(2)
    
    # Add corner accents
    corners = [
        ([0, 0.05], [1, 1]),      # top-left horizontal
        ([0, 0], [1, 0.95]),      # top-left vertical
        ([0.95, 1], [1, 1]),      # top-right horizontal
        ([1, 1], [1, 0.95]),      # top-right vertical
        ([0, 0.05], [0, 0]),      # bottom-left horizontal
        ([0, 0], [0, 0.05]),      # bottom-left vertical
        ([0.95, 1], [0, 0]),      # bottom-right horizontal
        ([1, 1], [0, 0.05]),      # bottom-right vertical
    ]
    for x_coords, y_coords in corners:
        corner = Line2D(x_coords, y_coords, color='#00d4ff', alpha=0.7,
                       lw=2, transform=ax.transAxes, clip_on=False, solid_capstyle='round')
        ax.add_line(corner)
    
    # Grid - subtle pattern
    ax.grid(True, color='#0a2a3a', alpha=0.5, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)


def compare_vehicles(seat: SeatParameters = None):
    """
    Compares G-force profiles across different historical and modern spacecraft.
    
    Features a dark theme with high-contrast colors for clear
    visualization of safety-critical data.
    """
    if seat is None:
        seat = SeatParameters(mass=80, spring_k=50000, damping_c=2500, name="Standard")
    
    # Create figure with dark space background
    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor('#050a12')
    
    # Add subtle gradient effect via multiple rectangles
    from matplotlib.patches import Rectangle, FancyBboxPatch
    
    # Main background gradient simulation
    for i in range(20):
        alpha = 0.02 * (1 - i/20)
        rect = Rectangle((0, i/20), 1, 0.05, transform=fig.transFigure,
                         facecolor='#0a1e3c', alpha=alpha, zorder=0)
        fig.patches.append(rect)
    
    # Color palette for different vehicles
    colors_launch = {
        'starship': '#00d4ff',      # Cyan (Paragon)
        'crew_dragon': '#00ff9f',   # Teal
        'shuttle': '#ffd700',       # Gold
        'soyuz': '#ff6b35',         # Orange (Renegade)
    }
    
    colors_reentry = {
        'soyuz_guided': '#ff6b35',
        'soyuz_ballistic': '#ff3366',
        'apollo': '#ffd700',
        'starship': '#00d4ff',
    }
    
    # === PLOT 1: Launch Profiles ===
    ax1 = fig.add_subplot(2, 2, 1)
    style_axis_dark(ax1, "LAUNCH ACCELERATION PROFILES", "Mission Time [seconds]", "Acceleration [g]")
    
    vehicles = [
        ('starship', 'launch', {}, 'STARSHIP', colors_launch['starship']),
        ('crew_dragon', 'launch', {}, 'CREW DRAGON', colors_launch['crew_dragon']),
        ('shuttle', 'launch', {}, 'SPACE SHUTTLE', colors_launch['shuttle']),
        ('soyuz', 'launch', {}, 'SOYUZ', colors_launch['soyuz']),
    ]
    
    for vehicle, phase, kwargs, label, color in vehicles:
        t, a, _ = get_vehicle_profile(vehicle, phase, **kwargs)
        # Main line
        ax1.plot(t, a / G0, color=color, lw=2.5, alpha=0.9, label=label, zorder=3)
        # Glow effect
        ax1.plot(t, a / G0, color=color, lw=6, alpha=0.15, zorder=2)
    
    # Safety limit line with glow
    ax1.axhline(NASA_SUSTAINED_G_LIMIT, color='#ff3366', ls='--', lw=2, alpha=0.8, 
               label=f'SAFETY LIMIT [{NASA_SUSTAINED_G_LIMIT}g]', zorder=4)
    ax1.axhline(NASA_SUSTAINED_G_LIMIT, color='#ff3366', ls='--', lw=6, alpha=0.2, zorder=3)
    
    ax1.set_xlim(0, 600)
    ax1.set_ylim(0, 5)
    
    # Custom legend
    leg1 = ax1.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor='#b0d4e8', fontsize=9, framealpha=0.9)
    leg1.get_frame().set_linewidth(1.5)
    
    # === PLOT 2: Reentry Profiles ===
    ax2 = fig.add_subplot(2, 2, 2)
    style_axis_dark(ax2, "REENTRY/LANDING PROFILES", "Mission Time [seconds]", "Acceleration [g]")
    
    reentry_vehicles = [
        ('soyuz', 'reentry', {'ballistic': False}, 'SOYUZ [GUIDED]', colors_reentry['soyuz_guided']),
        ('soyuz', 'reentry', {'ballistic': True}, 'SOYUZ [BALLISTIC]', colors_reentry['soyuz_ballistic']),
        ('apollo', 'reentry', {}, 'APOLLO CM', colors_reentry['apollo']),
        ('starship', 'landing', {}, 'STARSHIP', colors_reentry['starship']),
    ]
    
    for vehicle, phase, kwargs, label, color in reentry_vehicles:
        t, a, _ = get_vehicle_profile(vehicle, phase, **kwargs)
        ax2.plot(t, a / G0, color=color, lw=2.5, alpha=0.9, label=label, zorder=3)
        ax2.plot(t, a / G0, color=color, lw=6, alpha=0.15, zorder=2)
    
    ax2.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=2, alpha=0.8,
               label=f'PEAK LIMIT [{NASA_PEAK_G_LIMIT}g]', zorder=4)
    ax2.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=6, alpha=0.2, zorder=3)
    
    ax2.set_ylim(0, 10)
    
    leg2 = ax2.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor='#b0d4e8', fontsize=9, framealpha=0.9)
    leg2.get_frame().set_linewidth(1.5)
    
    # === PLOT 3: Vehicle Comparison Bars ===
    ax3 = fig.add_subplot(2, 2, 3)
    style_axis_dark(ax3, "VEHICLE G-FORCE COMPARISON", "", "Peak Acceleration [g]")
    
    vehicle_names = ['CREW\nDRAGON', 'STARSHIP', 'SPACE\nSHUTTLE', 'SOYUZ', 'APOLLO', 'SHENZHOU']
    launch_gs = [4.0, 3.0, 3.0, 4.2, 4.0, 4.0]
    reentry_gs = [4.5, 4.0, 1.5, 4.5, 6.5, 4.5]
    
    x = np.arange(len(vehicle_names))
    width = 0.35
    
    # Bars with glow effect
    bars1 = ax3.bar(x - width/2, launch_gs, width, label='LAUNCH', 
                   color='#00d4ff', edgecolor='#00ffff', linewidth=2, alpha=0.85, zorder=3)
    bars2 = ax3.bar(x + width/2, reentry_gs, width, label='REENTRY',
                   color='#ff6b35', edgecolor='#ff8c5a', linewidth=2, alpha=0.85, zorder=3)
    
    # Add value labels on bars
    for bar, val in zip(bars1, launch_gs):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                f'{val}g', ha='center', va='bottom', color='#00d4ff', 
                fontsize=8, fontweight='bold')
    for bar, val in zip(bars2, reentry_gs):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                f'{val}g', ha='center', va='bottom', color='#ff6b35',
                fontsize=8, fontweight='bold')
    
    # Limit lines
    ax3.axhline(NASA_SUSTAINED_G_LIMIT, color='#ffd700', ls='--', lw=2, alpha=0.7,
               label=f'SUSTAINED LIMIT')
    ax3.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=2, alpha=0.7,
               label=f'PEAK LIMIT')
    
    ax3.set_xticks(x)
    ax3.set_xticklabels(vehicle_names, color='#b0d4e8', fontsize=9)
    ax3.set_ylim(0, 9)
    
    leg3 = ax3.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1e5f74',
                     labelcolor='#b0d4e8', fontsize=9, ncol=2, framealpha=0.9)
    leg3.get_frame().set_linewidth(1.5)
    
    # === PLOT 4: Info Panel ===
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor('#050a12')
    ax4.axis('off')
    
    # Create info panel border
    panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, 
                           boxstyle="round,pad=0.02,rounding_size=0.02",
                           facecolor='#0a1628', edgecolor='#00d4ff',
                           linewidth=2, alpha=0.8,
                           transform=ax4.transAxes, zorder=1)
    ax4.add_patch(panel)
    
    # Inner glow
    panel_inner = FancyBboxPatch((0.03, 0.03), 0.94, 0.94,
                                 boxstyle="round,pad=0.02,rounding_size=0.02",
                                 facecolor='none', edgecolor='#00d4ff',
                                 linewidth=0.5, alpha=0.3,
                                 transform=ax4.transAxes, zorder=2)
    ax4.add_patch(panel_inner)
    
    # Header
    ax4.text(0.5, 0.95, "◆ HISTORICAL G-FORCE DATABASE ◆", transform=ax4.transAxes,
            fontsize=14, fontweight='bold', color='#00d4ff', ha='center', va='top',
            zorder=3)
    
    # Decorative line under header (using Line2D)
    from matplotlib.lines import Line2D
    header_line = Line2D([0.1, 0.9], [0.90, 0.90], color='#00d4ff', alpha=0.5, 
                        lw=1, transform=ax4.transAxes)
    ax4.add_line(header_line)
    
    # Content sections
    sections = [
        ("EXTREME G-FORCE RECORDS", 0.85, '#ff6b35', [
            "► Col. John Stapp (1954): 46.2g — Rocket sled test",
            "► Soyuz TMA-11 (2008): 8.2g — Ballistic reentry",
            "► Apollo 16 (1972): 7.19g — Fastest lunar return"
        ]),
        ("DESIGN PARAMETERS BY ERA", 0.62, '#ffd700', [
            "► Mercury/Gemini: 8g reentry tolerance",
            "► Apollo Program: 4g launch / 6.5g return",
            "► Space Shuttle: 3g limit for crew comfort",
            "► Modern Era: 4-4.5g typical operations"
        ]),
        ("ENGINEERING PHILOSOPHY", 0.37, '#00ff9f', [
            "► NASA: < 4g sustained for nominal missions",
            "► Roscosmos: Higher G accepted in contingency",
            "► SpaceX: < 3g target for passenger comfort"
        ])
    ]
    
    for title, y_pos, color, items in sections:
        ax4.text(0.08, y_pos, title, transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=color, va='top', zorder=3)
        section_line = Line2D([0.08, 0.55], [y_pos - 0.02, y_pos - 0.02], 
                             color=color, alpha=0.3, lw=1, transform=ax4.transAxes)
        ax4.add_line(section_line)
        
        for i, item in enumerate(items):
            ax4.text(0.10, y_pos - 0.06 - i*0.05, item, transform=ax4.transAxes,
                    fontsize=9, color='#b0d4e8', va='top', zorder=3)
    
    # Status indicator
    ax4.text(0.5, 0.08, "● SYSTEMS NOMINAL", transform=ax4.transAxes,
            fontsize=10, color='#00ff9f', ha='center', fontweight='bold', zorder=3)
    
    # === Main Title ===
    fig.text(0.5, 0.97, "◢ CREW SAFETY ANALYSIS SYSTEM ◣", 
            fontsize=22, fontweight='bold', color='#00d4ff', ha='center',
            va='top')
    fig.text(0.5, 0.935, "NASA  ·  ROSCOSMOS  ·  SPACEX  ·  CNSA",
            fontsize=12, color='#7fdbff', ha='center', va='top', alpha=0.8)
    
    # Decorative corner elements
    fig.text(0.02, 0.97, "◄", fontsize=16, color='#00d4ff', alpha=0.6)
    fig.text(0.98, 0.97, "►", fontsize=16, color='#00d4ff', alpha=0.6, ha='right')
    
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.show()


class InteractiveDashboard:
    """
    Interactive single-window dashboard for crew safety analysis.
    Navigate between views using buttons - no need to close windows.
    """
    
    def __init__(self):
        self.seat = SeatParameters(mass=80, spring_k=50000, damping_c=2500, name="Standard")
        self.current_view = 0
        self.views = [
            ("OVERVIEW", self._draw_overview),
            ("DRAGON", self._draw_crew_dragon),
            ("STARSHIP", self._draw_starship),
            ("SOYUZ", self._draw_soyuz),
            ("APOLLO", self._draw_apollo),
            ("SHEPARD", self._draw_new_shepard),
            ("SHENZHOU", self._draw_shenzhou),
        ]
        
        # Pre-compute all simulation data for fast switching
        self._precompute_data()
        
        # Create figure
        self.fig = plt.figure(figsize=(18, 11))
        self.fig.patch.set_facecolor('#050a12')
        
        # Track figure text elements for cleanup
        self.fig_texts = []
        
        # Store button axes references
        self.button_axes = []
        
        # Setup navigation
        self._setup_navigation()
        
        # Draw initial view
        self._draw_current_view()
    
    def _precompute_data(self):
        """
        Run all physics simulations at startup for instant view switching.
        
        This runs the FULL simulation (ODE solving, mass-spring-damper dynamics)
        for each vehicle profile once. The physics are real - we're just caching
        the results so you don't have to wait when switching between tabs.
        """
        self.cached_data = {}
        
        # Overview data - launch profiles
        self.cached_data['launch_profiles'] = []
        launch_vehicles = [('starship', 'launch'), ('crew_dragon', 'launch'), 
                          ('shuttle', 'launch'), ('soyuz', 'launch'),
                          ('new_shepard', 'launch'), ('shenzhou', 'launch')]
        for vehicle, phase in launch_vehicles:
            t, a, _ = get_vehicle_profile(vehicle, phase)
            self.cached_data['launch_profiles'].append((t, a / G0))
        
        # Overview data - reentry profiles
        self.cached_data['reentry_profiles'] = []
        for vehicle, phase, kwargs in [('soyuz', 'reentry', {'ballistic': False}),
                                        ('soyuz', 'reentry', {'ballistic': True}),
                                        ('apollo', 'reentry', {}),
                                        ('shenzhou', 'reentry', {}),
                                        ('starship', 'landing', {})]:
            t, a, _ = get_vehicle_profile(vehicle, phase, **kwargs)
            self.cached_data['reentry_profiles'].append((t, a / G0))
        
        # Individual vehicle simulations for detailed views
        vehicles = [
            ('crew_dragon', 'launch', {}),
            ('starship', 'launch', {}),
            ('soyuz', 'reentry', {'ballistic': True}),
            ('apollo', 'reentry', {}),
            ('new_shepard', 'launch', {}),
            ('shenzhou', 'launch', {}),
        ]
        
        for vehicle, phase, kwargs in vehicles:
            key = f"{vehicle}_{phase}"
            t, a, desc = get_vehicle_profile(vehicle, phase, **kwargs)
            sim = CrewSafetySimulator(self.seat)
            r = sim.simulate(t, a)
            assessment = sim.assess_safety()
            self.cached_data[key] = {'t': t, 'a': a, 'r': r, 'assessment': assessment, 'desc': desc}
        
    def _setup_navigation(self):
        """Creates navigation buttons at the bottom of the window."""
        from matplotlib.widgets import Button
        
        button_color = '#0a1628'
        hover_color = '#1e3a5f'
        text_color = '#00d4ff'
        
        num_buttons = len(self.views)
        button_width = 0.12
        button_height = 0.035
        spacing = 0.008
        total_width = num_buttons * button_width + (num_buttons - 1) * spacing
        start_x = (1 - total_width) / 2
        
        self.buttons = []
        for i, (name, _) in enumerate(self.views):
            ax_btn = self.fig.add_axes([start_x + i * (button_width + spacing), 
                                        0.02, button_width, button_height])
            self.button_axes.append(ax_btn)
            btn = Button(ax_btn, name, color=button_color, hovercolor=hover_color)
            btn.label.set_color(text_color)
            btn.label.set_fontsize(8)
            btn.label.set_fontweight('bold')
            btn.on_clicked(lambda event, idx=i: self._switch_view(idx))
            self.buttons.append(btn)
            
            for spine in ax_btn.spines.values():
                spine.set_color('#00d4ff')
                spine.set_linewidth(1.5)
    
    def _switch_view(self, idx):
        """Switch to a different view."""
        self.current_view = idx
        self._draw_current_view()
        
    def _clear_view(self):
        """Efficiently clear current view elements."""
        # Remove all axes except button axes
        axes_to_remove = [ax for ax in self.fig.axes if ax not in self.button_axes]
        for ax in axes_to_remove:
            ax.remove()
        
        # Remove all figure-level text elements
        for txt in self.fig_texts:
            try:
                txt.remove()
            except:
                pass
        self.fig_texts.clear()
        
    def _draw_current_view(self):
        """Clear and redraw the current view."""
        self._clear_view()
        
        # Highlight current button
        for i, btn in enumerate(self.buttons):
            if i == self.current_view:
                btn.ax.set_facecolor('#1e5f74')
                for spine in btn.ax.spines.values():
                    spine.set_color('#00ff9f')
            else:
                btn.ax.set_facecolor('#0a1628')
                for spine in btn.ax.spines.values():
                    spine.set_color('#00d4ff')
        
        # Draw the selected view
        _, draw_func = self.views[self.current_view]
        draw_func()
        
        self.fig.canvas.draw_idle()
    
    def _add_title(self, main_title, subtitle=""):
        """Add main title with proper tracking for cleanup."""
        t1 = self.fig.text(0.5, 0.96, f"◢ {main_title} ◣",
                         fontsize=20, fontweight='bold', color='#00d4ff', ha='center')
        self.fig_texts.append(t1)
        if subtitle:
            t2 = self.fig.text(0.5, 0.92, subtitle,
                              fontsize=11, color='#7fdbff', ha='center', alpha=0.8)
            self.fig_texts.append(t2)
    
    def _draw_overview(self):
        """Multi-vehicle comparison overview with enhanced visuals."""
        from matplotlib.patches import FancyBboxPatch
        from matplotlib.lines import Line2D
        
        colors_launch = ['#00d4ff', '#00ff9f', '#ffd700', '#ff6b35', '#9b59b6', '#e74c3c']
        labels_launch = ['STARSHIP', 'DRAGON', 'SHUTTLE', 'SOYUZ', 'SHEPARD', 'SHENZHOU']
        colors_reentry = ['#ff6b35', '#ff3366', '#ffd700', '#e74c3c', '#00d4ff']
        labels_reentry = ['SOYUZ', 'SOYUZ [BALL]', 'APOLLO', 'SHENZHOU', 'STARSHIP']
        
        # === PLOT 1: Launch Profiles ===
        ax1 = self.fig.add_axes([0.05, 0.52, 0.42, 0.36])
        style_axis_dark(ax1, "LAUNCH PROFILES", "Time [s]", "Accel [g]")
        
        for i, (t, a_g) in enumerate(self.cached_data['launch_profiles']):
            # Glow effect
            ax1.plot(t, a_g, color=colors_launch[i], lw=5, alpha=0.1)
            ax1.plot(t, a_g, color=colors_launch[i], lw=2, alpha=0.9, label=labels_launch[i])
        
        ax1.axhline(NASA_SUSTAINED_G_LIMIT, color='#ff3366', ls='--', lw=1.5, alpha=0.6)
        ax1.set_xlim(0, 600)
        ax1.set_ylim(0, 5)
        ax1.legend(loc='upper right', facecolor='#0a1420', edgecolor='#1a4a5e',
                  labelcolor='#b0d4e8', fontsize=6, framealpha=0.95)
        
        # === PLOT 2: Reentry Profiles ===
        ax2 = self.fig.add_axes([0.53, 0.52, 0.42, 0.36])
        style_axis_dark(ax2, "REENTRY/LANDING", "Time [s]", "Accel [g]")
        
        for i, (t, a_g) in enumerate(self.cached_data['reentry_profiles']):
            ax2.plot(t, a_g, color=colors_reentry[i], lw=5, alpha=0.1)
            ax2.plot(t, a_g, color=colors_reentry[i], lw=2, alpha=0.9, label=labels_reentry[i])
        
        ax2.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=1.5, alpha=0.6)
        ax2.set_ylim(0, 10)
        ax2.legend(loc='upper right', facecolor='#0a1420', edgecolor='#1a4a5e',
                  labelcolor='#b0d4e8', fontsize=6, framealpha=0.95)
        
        # === PLOT 3: Bar Chart (Enhanced) ===
        ax3 = self.fig.add_axes([0.05, 0.10, 0.42, 0.35])
        style_axis_dark(ax3, "PEAK G COMPARISON", "", "Peak [g]")
        
        vehicle_names = ['DRAGON', 'SHIP', 'SHUTTLE', 'SOYUZ', 'APOLLO', 'SHEPARD', 'SHENZHOU']
        launch_gs = [4.0, 3.0, 3.0, 4.2, 4.0, 3.0, 4.0]
        reentry_gs = [4.5, 4.0, 1.5, 4.5, 6.5, 5.0, 4.5]
        
        x = np.arange(len(vehicle_names))
        width = 0.38
        
        # Bars with gradient effect (multiple overlapping bars with decreasing alpha)
        for offset in [0.15, 0.1, 0.05, 0]:
            alpha = 0.2 + offset * 3
            ax3.bar(x - width/2, [g - offset for g in launch_gs], width, 
                   color='#00d4ff', alpha=alpha * 0.3, edgecolor='none')
            ax3.bar(x + width/2, [g - offset for g in reentry_gs], width,
                   color='#ff6b35', alpha=alpha * 0.3, edgecolor='none')
        
        ax3.bar(x - width/2, launch_gs, width, label='LAUNCH', 
               color='#00d4ff', edgecolor='#00ffff', linewidth=1, alpha=0.85)
        ax3.bar(x + width/2, reentry_gs, width, label='REENTRY',
               color='#ff6b35', edgecolor='#ff8855', linewidth=1, alpha=0.85)
        
        ax3.axhline(NASA_SUSTAINED_G_LIMIT, color='#ffd700', ls='--', lw=1.5, alpha=0.5)
        ax3.axhline(NASA_PEAK_G_LIMIT, color='#ff3366', ls='--', lw=1.5, alpha=0.5)
        ax3.set_xticks(x)
        ax3.set_xticklabels(vehicle_names, color='#b0d4e8', fontsize=6, rotation=45,
                           fontfamily='monospace')
        ax3.set_ylim(0, 8)
        ax3.legend(loc='upper right', facecolor='#0a1420', edgecolor='#1a4a5e',
                  labelcolor='#b0d4e8', fontsize=6, framealpha=0.95)
        
        # === PLOT 4: Info Panel (Enhanced) ===
        ax4 = self.fig.add_axes([0.53, 0.10, 0.42, 0.35])
        ax4.set_facecolor('#050a10')
        ax4.axis('off')
        
        # Glow effect
        panel_glow = FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                                    boxstyle="round,pad=0.02,rounding_size=0.03",
                                    facecolor='none', edgecolor='#00d4ff',
                                    linewidth=4, alpha=0.15,
                                    transform=ax4.transAxes)
        ax4.add_patch(panel_glow)
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                               boxstyle="round,pad=0.02,rounding_size=0.02",
                               facecolor='#0a1420', edgecolor='#00d4ff',
                               linewidth=2, alpha=0.95,
                               transform=ax4.transAxes)
        ax4.add_patch(panel)
        
        # Inner accent
        inner = FancyBboxPatch((0.04, 0.04), 0.92, 0.92,
                               boxstyle="round,pad=0.01,rounding_size=0.01",
                               facecolor='none', edgecolor='#00d4ff',
                               linewidth=0.5, alpha=0.3,
                               transform=ax4.transAxes)
        ax4.add_patch(inner)
        
        ax4.text(0.5, 0.94, "◆ G-FORCE DATABASE ◆", transform=ax4.transAxes,
                fontsize=10, fontweight='bold', color='#00d4ff', ha='center', va='top',
                fontfamily='monospace')
        
        # Divider
        divider = Line2D([0.1, 0.9], [0.88, 0.88], color='#00d4ff', alpha=0.4, lw=1,
                        transform=ax4.transAxes)
        ax4.add_line(divider)
        
        info_sections = [
            ("► RECORDS", 0.80, '#ff6b35', [
                "Stapp: 46.2g (sled)", "Soyuz TMA-11: 8.2g"
            ]),
            ("► BY ERA", 0.55, '#ffd700', [
                "Apollo: 4g / 6.5g", "Shuttle: 3g limit"
            ]),
            ("► DESIGN", 0.30, '#00ff9f', [
                "NASA: <4g nominal", "SpaceX: <3g comfort"
            ])
        ]
        
        for title, y_pos, color, items in info_sections:
            ax4.text(0.08, y_pos, title, transform=ax4.transAxes,
                    fontsize=8, fontweight='bold', color=color, va='top',
                    fontfamily='monospace')
            for i, item in enumerate(items):
                ax4.text(0.12, y_pos - 0.08 - i*0.08, item, transform=ax4.transAxes,
                        fontsize=7, color='#b0d4e8', va='top', fontfamily='monospace')
        
        # Status indicator with glow
        ax4.text(0.5, 0.08, "● SYSTEMS NOMINAL", transform=ax4.transAxes,
                fontsize=9, color='#00ff9f', ha='center', fontweight='bold',
                fontfamily='monospace')
        
        self._add_title("CREW SAFETY ANALYSIS SYSTEM", "NASA · ROSCOSMOS · SPACEX · CNSA · BLUE ORIGIN")
    
    def _draw_vehicle_analysis(self, cache_key: str, title: str, subtitle: str):
        """Draw detailed vehicle analysis with enhanced visuals."""
        from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
        from matplotlib.lines import Line2D
        
        data = self.cached_data[cache_key]
        r = data['r']
        assessment = data['assessment']
        
        # Color palette
        cyan = '#00d4ff'
        teal = '#00ff9f'
        orange = '#ff6b35'
        gold = '#ffd700'
        red = '#ff3366'
        purple = '#9b59b6'
        soft_white = '#b0d4e8'
        dark_bg = '#060d18'
        
        # === PLOT 1: G-Force Profile ===
        ax1 = self.fig.add_axes([0.05, 0.50, 0.42, 0.36])
        style_axis_dark(ax1, "G-FORCE PROFILE", "Time [s]", "Accel [g]")
        
        # Glow effect for main line
        ax1.plot(r['time'], r['crew_accel_g'], color=cyan, lw=8, alpha=0.1)
        ax1.plot(r['time'], r['crew_accel_g'], color=cyan, lw=4, alpha=0.2)
        ax1.plot(r['time'], r['crew_accel_g'], color=cyan, lw=2, label='CREW')
        
        ax1.plot(r['time'], r['spacecraft_accel_g'], color=orange, lw=4, alpha=0.15)
        ax1.plot(r['time'], r['spacecraft_accel_g'], color=orange, alpha=0.8, lw=1.5, label='VEHICLE')
        
        # Limit lines with glow
        ax1.axhline(NASA_SUSTAINED_G_LIMIT, color=gold, ls='--', lw=1.5, alpha=0.6, label=f'LIMIT [{NASA_SUSTAINED_G_LIMIT}g]')
        ax1.axhline(NASA_PEAK_G_LIMIT, color=red, ls='--', lw=1.5, alpha=0.6, label=f'PEAK [{NASA_PEAK_G_LIMIT}g]')
        
        ax1.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1a4a5e',
                  labelcolor=soft_white, fontsize=7, framealpha=0.9)
        
        # === PLOT 2: Seat Displacement ===
        ax2 = self.fig.add_axes([0.53, 0.50, 0.42, 0.36])
        style_axis_dark(ax2, "DISPLACEMENT", "Time [s]", "Disp [cm]")
        
        # Gradient fill effect
        ax2.fill_between(r['time'], 0, r['displacement_cm'], color=teal, alpha=0.15)
        ax2.fill_between(r['time'], 0, r['displacement_cm'] * 0.7, color=teal, alpha=0.15)
        ax2.fill_between(r['time'], 0, r['displacement_cm'] * 0.4, color=teal, alpha=0.15)
        ax2.plot(r['time'], r['displacement_cm'], color=teal, lw=6, alpha=0.15)
        ax2.plot(r['time'], r['displacement_cm'], color=teal, lw=2)
        
        # === PLOT 3: Attenuation Analysis ===
        ax3 = self.fig.add_axes([0.05, 0.08, 0.42, 0.36])
        style_axis_dark(ax3, "ATTENUATION", "Time [s]", "G Reduction")
        
        reduction = r['spacecraft_accel_g'] - r['crew_accel_g']
        ax3.fill_between(r['time'], 0, reduction, where=reduction > 0,
                        color=teal, alpha=0.5, label='ABSORB')
        ax3.fill_between(r['time'], 0, reduction, where=reduction < 0,
                        color=red, alpha=0.5, label='AMPLIFY')
        ax3.plot(r['time'], reduction, color='white', lw=1.5, alpha=0.7)
        ax3.axhline(0, color='white', alpha=0.4, lw=1)
        ax3.legend(loc='upper right', facecolor='#0a1628', edgecolor='#1a4a5e',
                  labelcolor=soft_white, fontsize=7, framealpha=0.9)
        
        # === PLOT 4: Status Panel (Enhanced) ===
        ax4 = self.fig.add_axes([0.53, 0.08, 0.42, 0.36])
        ax4.set_facecolor(dark_bg)
        ax4.axis('off')
        
        # Outer panel with glow
        panel_glow = FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                                    boxstyle="round,pad=0.02,rounding_size=0.03",
                                    facecolor='none', edgecolor=cyan,
                                    linewidth=4, alpha=0.15,
                                    transform=ax4.transAxes)
        ax4.add_patch(panel_glow)
        
        panel = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                               boxstyle="round,pad=0.02,rounding_size=0.02",
                               facecolor='#0a1420', edgecolor=cyan,
                               linewidth=2, alpha=0.95,
                               transform=ax4.transAxes)
        ax4.add_patch(panel)
        
        # Inner accent line
        inner = FancyBboxPatch((0.04, 0.04), 0.92, 0.92,
                               boxstyle="round,pad=0.01,rounding_size=0.01",
                               facecolor='none', edgecolor=cyan,
                               linewidth=0.5, alpha=0.3,
                               transform=ax4.transAxes)
        ax4.add_patch(inner)
        
        status_color = teal if assessment['overall_safe'] else red
        status_text = "NOMINAL" if assessment['overall_safe'] else "WARNING"
        
        # Header
        ax4.text(0.30, 0.94, "◢ STATUS ◣", transform=ax4.transAxes,
                fontsize=13, fontweight='bold', color=cyan, ha='center', va='top',
                fontfamily='monospace')
        
        # Divider line
        divider = Line2D([0.05, 0.55], [0.88, 0.88], color=cyan, alpha=0.5, lw=1.5,
                        transform=ax4.transAxes)
        ax4.add_line(divider)
        
        # Config section - LARGER & BRIGHTER
        ax4.text(0.05, 0.82, "► SEAT CONFIG", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=gold, fontfamily='monospace')
        config = f"Mass: {self.seat.mass:.0f}kg | k: {self.seat.spring_k:.0f}N/m | ζ: {self.seat.damping_ratio:.2f}"
        ax4.text(0.07, 0.73, config, transform=ax4.transAxes, fontsize=9, color='#ffffff',
                fontfamily='monospace')
        
        # Results section - LARGER & HIGH CONTRAST
        ax4.text(0.05, 0.63, "► RESULTS", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=orange, fontfamily='monospace')
        
        results = [
            (f"Vehicle G:", f"{r['peak_spacecraft_g']:.2f}"),
            (f"Crew G:", f"{r['peak_crew_g']:.2f}"),
            (f"Reduction:", f"{assessment['reduction_percent']:.1f}%"),
            (f"Disp:", f"{r['max_displacement_cm']:.2f} cm"),
        ]
        for i, (label, value) in enumerate(results):
            y = 0.54 - i * 0.09
            ax4.text(0.07, y, label, transform=ax4.transAxes, fontsize=10, color=cyan,
                    fontfamily='monospace')
            ax4.text(0.32, y, value, transform=ax4.transAxes, fontsize=10, color='#ffffff',
                    fontweight='bold', fontfamily='monospace')
        
        # Safety indicators - LARGER
        ax4.text(0.05, 0.16, "► SAFETY", transform=ax4.transAxes,
                fontsize=11, fontweight='bold', color=teal, fontfamily='monospace')
        
        sus_color = teal if assessment['sustained_g_ok'] else red
        peak_color = teal if assessment['peak_g_ok'] else red
        ax4.text(0.07, 0.07, "●", transform=ax4.transAxes, fontsize=14, color=sus_color)
        ax4.text(0.12, 0.07, "Sustained", transform=ax4.transAxes, fontsize=10, color='#ffffff',
                fontfamily='monospace')
        ax4.text(0.32, 0.07, "●", transform=ax4.transAxes, fontsize=14, color=peak_color)
        ax4.text(0.37, 0.07, "Peak", transform=ax4.transAxes, fontsize=10, color='#ffffff',
                fontfamily='monospace')
        
        # Status indicator on right side
        status_bg = FancyBboxPatch((0.62, 0.10), 0.32, 0.75,
                                   boxstyle="round,pad=0.02,rounding_size=0.02",
                                   facecolor=status_color, edgecolor=status_color,
                                   linewidth=1.5, alpha=0.12,
                                   transform=ax4.transAxes)
        ax4.add_patch(status_bg)
        
        # Vertical accent bar
        accent_bar = FancyBboxPatch((0.62, 0.10), 0.025, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.01",
                                    facecolor=status_color, edgecolor='none',
                                    alpha=0.9, transform=ax4.transAxes)
        ax4.add_patch(accent_bar)
        
        # Status icon
        icon = "◆" if assessment['overall_safe'] else "⚠"
        ax4.text(0.78, 0.72, icon, transform=ax4.transAxes,
                fontsize=18, color=status_color, ha='center', va='center')
        
        # Status text - reasonable size
        ax4.text(0.78, 0.45, status_text, transform=ax4.transAxes,
                fontsize=14, fontweight='bold', color=status_color, ha='center',
                rotation=90, fontfamily='monospace')
        
        # Sub-label
        sub_label = "ALL CLEAR" if assessment['overall_safe'] else "REVIEW"
        ax4.text(0.78, 0.15, sub_label, transform=ax4.transAxes,
                fontsize=9, color=status_color, ha='center', fontweight='bold',
                fontfamily='monospace')
        
        self._add_title(title, subtitle)
    
    def _draw_crew_dragon(self):
        self._draw_vehicle_analysis('crew_dragon_launch', 
                                    "CREW DRAGON",
                                    "SpaceX Falcon 9 - Nominal Launch")
    
    def _draw_starship(self):
        self._draw_vehicle_analysis('starship_launch',
                                    "STARSHIP",
                                    "Super Heavy / Starship - Orbital")
    
    def _draw_soyuz(self):
        self._draw_vehicle_analysis('soyuz_reentry',
                                    "SOYUZ BALLISTIC",
                                    "TMA-11 (2008) - Emergency")
    
    def _draw_apollo(self):
        self._draw_vehicle_analysis('apollo_reentry',
                                    "APOLLO LUNAR",
                                    "Command Module - Trans-Earth")
    
    def _draw_new_shepard(self):
        self._draw_vehicle_analysis('new_shepard_launch',
                                    "NEW SHEPARD",
                                    "Blue Origin - Suborbital Flight")
    
    def _draw_shenzhou(self):
        self._draw_vehicle_analysis('shenzhou_launch',
                                    "SHENZHOU",
                                    "CNSA Long March 2F - Orbital")
    
    def show(self):
        """Display the dashboard."""
        plt.show()


def run_demo():
    """Launch the interactive crew safety dashboard."""
    print("=" * 70)
    print("CREW SAFETY SIMULATOR")
    print("Module 4: Human Factors, Regulations, and Space Policy")
    print("=" * 70)
    print("\nLaunching interactive dashboard...")
    print("Use the buttons at the bottom to switch between views.")
    print("-" * 70)
    
    dashboard = InteractiveDashboard()
    dashboard.show()


if __name__ == "__main__":
    run_demo()

