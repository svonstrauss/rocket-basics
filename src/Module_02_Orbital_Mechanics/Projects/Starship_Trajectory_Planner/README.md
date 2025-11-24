# Project 2: Starship Trajectory Planner

**Module:** 2 (Orbital Mechanics)
**Project:** 2
**Language:** Python 3.x

## Project Overview
This tool calculates and visualizes the **Hohmann Transfer Orbit** required to send a spacecraft (Starship) from Earth to Mars. It solves the "Interplanetary Transfer" problem to determine:
1.  **Launch Windows:** The precise relative angle (Phase Angle) Earth and Mars must be in.
2.  **Delta-V Budget:** The exact velocity change ($\Delta v$) needed for Trans-Mars Injection (TMI) and Mars Orbit Insertion (MOI).
3.  **Time of Flight:** How long the journey takes (typically ~7-9 months).

## SpaceX Tie-In
*   **Mars Colonization:** This is the fundamental math behind Elon Musk's vision. Starship launches are timed to align with the 26-month Hohmann transfer window.
*   **Fuel Tanker Logistics:** Knowing the Delta-V allows engineers to calculate how many on-orbit refuelings are needed in LEO before the ship can depart.

## Features
- [x] **Hohmann Math Engine:** Calculates semi-major axis, eccentricity, and velocities for the transfer ellipse.
- [x] **Phase Angle Calculator:** Determines the "Lead Angle" Mars must have at launch.
- [x] **Heliocentric Animation:** A top-down 2D solar system view showing Earth, Mars, and Starship moving in sync to prove the rendezvous logic.

## Usage
1.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the planner:
    ```bash
    python mission_planner.py
    ```

## The Math (Hohmann Transfer)
The most energy-efficient transfer between two concentric circular orbits.

1.  **Transfer Semi-Major Axis ($a_{tx}$):**
    $$ a_{tx} = \frac{r_{earth} + r_{mars}}{2} $$

2.  **Departure Velocity ($\Delta v_1$):**
    $$ \Delta v_1 = \sqrt{\frac{\mu}{r_{earth}} \left(\frac{2 r_{mars}}{r_{earth} + r_{mars}}\right)} - \sqrt{\frac{\mu}{r_{earth}}} $$

3.  **Phase Angle ($\phi$):**
    $$ \phi = \pi - \omega_{mars} \cdot T_{transfer} $$
    Mars must be ahead of Earth by this angle at launch so it arrives at the meeting point exactly when the ship does.

