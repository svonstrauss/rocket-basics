from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path("assets") / "simulations"


def _base_style():
    plt.rcParams.update(
        {
            "figure.facecolor": "#0b0f14",
            "axes.facecolor": "#0b0f14",
            "savefig.facecolor": "#0b0f14",
            "text.color": "#EAF2FF",
            "axes.labelcolor": "#EAF2FF",
            "axes.edgecolor": "#2A3340",
            "xtick.color": "#A8B3C7",
            "ytick.color": "#A8B3C7",
            "grid.color": "#2A3340",
            "grid.alpha": 0.35,
            "axes.grid": True,
            "font.size": 12,
            "axes.titleweight": "bold",
        }
    )


def _finish(fig: plt.Figure, title: str, subtitle: str, out_path: Path):
    fig.suptitle(title, x=0.03, y=0.98, ha="left", va="top", fontsize=18, color="#00D4FF")
    fig.text(0.03, 0.93, subtitle, ha="left", va="top", fontsize=12, color="#A8B3C7")
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def thumb_rocket_ascent(out_path: Path):
    t = np.linspace(0, 180, 240)
    altitude_km = 120 * (1 - np.exp(-t / 55)) ** 1.35
    v_ms = np.gradient(altitude_km * 1000, t)

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(t, altitude_km, color="#00D4FF", lw=2.8)
    ax.fill_between(t, altitude_km, 0, color="#00D4FF", alpha=0.10)
    ax2 = ax.twinx()
    ax2.plot(t, v_ms / 1000, color="#FCA311", lw=2.0, alpha=0.9)
    ax2.set_ylabel("Velocity (km/s)")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("Altitude & Velocity (sample profile)")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 140)
    ax2.set_ylim(0, max(1.0, float(np.max(v_ms / 1000)) * 1.15))
    ax.grid(True)

    _finish(fig, "Rocket Ascent Simulator", "Thrust, drag, gravity turn, and live telemetry", out_path)


def thumb_conic_orbits(out_path: Path):
    theta = np.linspace(0, 2 * np.pi, 720)

    # Ellipse in polar form: r = p / (1 + e cos θ)
    p = 1.0
    e1 = 0.25
    e2 = 0.7
    r1 = p / (1 + e1 * np.cos(theta))
    r2 = p / (1 + e2 * np.cos(theta))

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(r1 * np.cos(theta), r1 * np.sin(theta), color="#00D4FF", lw=2.6, label=f"e={e1:.2f}")
    ax.plot(r2 * np.cos(theta), r2 * np.sin(theta), color="#FF4D6D", lw=2.2, label=f"e={e2:.2f}")
    ax.scatter([0], [0], s=180, color="#EAF2FF", edgecolor="#0b0f14", zorder=5, label="Primary body")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (normalized)")
    ax.set_ylabel("y (normalized)")
    ax.set_title("Conic sections as orbital paths")
    ax.legend(loc="upper right", frameon=True, facecolor="#0b0f14", edgecolor="#2A3340")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.6, 1.6)

    _finish(fig, "Conic Orbit Visualizer", "Circular, elliptical, parabolic, and hyperbolic trajectories", out_path)


def thumb_constellation_propagator(out_path: Path):
    # Simple ground-track like curves (lat vs lon)
    lon = np.linspace(-180, 180, 720)
    lat1 = 45 * np.sin(np.deg2rad(lon * 1.2))
    lat2 = 60 * np.sin(np.deg2rad(lon * 1.8 + 25))

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(lon, lat1, color="#00D4FF", lw=2.4, label="Plane A (sample)")
    ax.plot(lon, lat2, color="#FCA311", lw=2.0, alpha=0.95, label="Plane B (sample)")
    ax.axhline(0, color="#2A3340", lw=1)
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_title("Ground tracks & coverage (illustrative)")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.legend(loc="lower left", frameon=True, facecolor="#0b0f14", edgecolor="#2A3340")

    _finish(fig, "Satellite Constellation Propagator", "Orbit propagation, ground tracks, and coverage stats", out_path)


def thumb_mars_mission(out_path: Path):
    theta = np.linspace(0, 2 * np.pi, 720)

    # Two circular orbits + a transfer ellipse
    r_earth = 1.0
    r_mars = 1.524
    a = (r_earth + r_mars) / 2
    e = (r_mars - r_earth) / (r_mars + r_earth)
    r_tr = a * (1 - e**2) / (1 + e * np.cos(theta))

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(r_earth * np.cos(theta), r_earth * np.sin(theta), color="#4ECDC4", lw=2.2, label="Earth orbit")
    ax.plot(r_mars * np.cos(theta), r_mars * np.sin(theta), color="#FF4D6D", lw=2.2, label="Mars orbit")
    ax.plot(r_tr * np.cos(theta), r_tr * np.sin(theta), color="#00D4FF", lw=2.8, label="Transfer (Hohmann)")
    ax.scatter([0], [0], s=220, color="#FFD166", edgecolor="#0b0f14", zorder=5, label="Sun")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    ax.set_title("Transfer geometry (illustrative)")
    ax.legend(loc="upper right", frameon=True, facecolor="#0b0f14", edgecolor="#2A3340")
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)

    _finish(fig, "Mars Mission Simulator", "Transfer windows, transit, and EDL walkthrough", out_path)


def thumb_trade_simulator(out_path: Path):
    payload = np.array([150, 120, 95, 70])
    dv = np.array([9.4, 11.8, 12.5, 16.0])
    labels = ["LEO", "GTO", "Moon", "Mars"]

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.bar(labels, payload, color="#00D4FF", alpha=0.85, edgecolor="#2A3340")
    ax.plot(labels, payload, color="#EAF2FF", lw=1.4, alpha=0.6)
    ax.set_ylabel("Payload (t) (illustrative)")
    ax.set_xlabel("Mission target")
    ax.set_title("Payload vs mission energy (illustrative)")
    for i, (p, d) in enumerate(zip(payload, dv)):
        ax.text(i, p + 4, f"Δv≈{d:.1f} km/s", ha="center", va="bottom", fontsize=10, color="#A8B3C7")
    ax.set_ylim(0, 175)

    _finish(fig, "Launch Vehicle Trade Simulator", "Mass ratio, Isp, payload, and mission targets", out_path)


def thumb_constellation_designer(out_path: Path):
    rng = np.random.default_rng(7)
    n = 220
    x = rng.normal(0, 1.0, n)
    y = rng.normal(0, 0.65, n)
    z = rng.normal(0, 0.4, n)

    fig = plt.figure(figsize=(12, 6.75))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, s=14, c="#00D4FF", alpha=0.9)
    ax.scatter([0], [0], [0], s=260, c="#EAF2FF", edgecolors="#0b0f14")
    ax.set_title("Multi-shell geometry (illustrative)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_box_aspect((1.4, 1.0, 0.6))
    ax.grid(True)

    _finish(fig, "Constellation Designer", "Walker patterns, coverage cones, and shell comparisons", out_path)


def thumb_crew_safety(out_path: Path):
    t = np.linspace(0, 180, 600)
    g = 1.0 + 2.8 * (1 - np.exp(-t / 50))
    vib = 0.35 * np.sin(2 * np.pi * 6.5 * t / 60) * np.exp(-t / 120)
    g_total = g + vib

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(t, g_total, color="#00D4FF", lw=2.6, label="Total g-load (sample)")
    ax.fill_between(t, g_total, 0, color="#00D4FF", alpha=0.10)
    ax.axhline(4.0, color="#FCA311", lw=2.0, alpha=0.85, linestyle="--", label="Crew comfort guideline (~4g)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Acceleration (g)")
    ax.set_title("G-load & vibration response (illustrative)")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 6.5)
    ax.legend(loc="upper left", frameon=True, facecolor="#0b0f14", edgecolor="#2A3340")

    _finish(fig, "Crew Safety Simulator", "G-forces, vibration, damping, and comfort limits", out_path)


def thumb_policy_calculator(out_path: Path):
    # Simple radar-like visualization (illustrative)
    labels = ["Debris", "Licensing", "Spectrum", "Safety", "Planetary\nProtection"]
    vals = np.array([0.68, 0.55, 0.42, 0.62, 0.38])
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.concatenate([angles, angles[:1]])
    vals = np.concatenate([vals, vals[:1]])

    fig = plt.figure(figsize=(12, 6.75))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, vals, color="#00D4FF", lw=2.6)
    ax.fill(angles, vals, color="#00D4FF", alpha=0.12)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 1)
    ax.set_title("Risk / compliance dimensions (illustrative)", pad=14)

    _finish(fig, "Space Policy Risk Calculator", "Regulatory, debris, and mission-risk scoring framework", out_path)


def thumb_propellant_explorer(out_path: Path):
    fuels = ["Hydrolox", "Methalox", "RP-1", "Solid"]
    isp = [450, 380, 350, 280]
    dens = [0.07, 0.42, 0.81, 1.80]

    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(dens, isp, marker="o", ms=8, lw=2.4, color="#00D4FF")
    for x, y, label in zip(dens, isp, fuels):
        ax.text(x + 0.03, y + 6, label, fontsize=11, color="#EAF2FF")
    ax.set_xlabel("Density (g/cm³)")
    ax.set_ylabel("Specific impulse (s) (vac)")
    ax.set_title("Efficiency vs tank sizing (illustrative)")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(240, 480)

    _finish(fig, "Propellant Explorer (Web App)", "Compare fuels, balance reactions, and compute Δv with sliders", out_path)


def main():
    _base_style()

    thumbs = {
        "rocket_ascent.png": thumb_rocket_ascent,
        "conic_orbits.png": thumb_conic_orbits,
        "constellation_propagator.png": thumb_constellation_propagator,
        "mars_mission.png": thumb_mars_mission,
        "trade_simulator.png": thumb_trade_simulator,
        "constellation_designer.png": thumb_constellation_designer,
        "crew_safety.png": thumb_crew_safety,
        "policy_calculator.png": thumb_policy_calculator,
        "propellant_explorer.png": thumb_propellant_explorer,
    }

    for filename, fn in thumbs.items():
        fn(OUT_DIR / filename)

    print(f"Generated {len(thumbs)} thumbnails in {OUT_DIR.as_posix()}/")


if __name__ == "__main__":
    main()


