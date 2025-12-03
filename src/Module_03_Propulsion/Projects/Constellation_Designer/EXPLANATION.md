# Constellation Designer: Technical Explanation

## Overview

This document explains the physics and mathematics behind the Constellation Designer tool. We cover Walker constellation patterns, orbital mechanics for multi-plane systems, and the geometry of sensor coverage analysis.

---

## 1. Walker Constellation Patterns

### The Walker Delta Notation

Satellite constellations are commonly described using **Walker Delta** notation:

$$i : t/p/f$$

Where:
- $i$ = Orbital inclination (degrees)
- $t$ = Total number of satellites
- $p$ = Number of equally-spaced orbital planes
- $f$ = Phasing factor (0 to p-1)

### Plane Distribution

For $p$ planes, the Right Ascension of Ascending Node (RAAN) for each plane is:

$$\Omega_k = \frac{2\pi k}{p}, \quad k = 0, 1, ..., p-1$$

### Satellite Distribution Within Planes

Each plane contains $s = t/p$ satellites. The true anomaly spacing is:

$$\Delta\nu = \frac{2\pi}{s}$$

### Phase Factor

The phasing factor $f$ controls the relative positioning of satellites in adjacent planes. A satellite in plane $k$ has an additional phase offset:

$$\phi_k = \frac{2\pi f k}{t}$$

This creates a "mesh" pattern that optimizes coverage overlap.

---

## 2. Coordinate Transformations

### Orbital Plane to ECI

To plot satellites in 3D, we transform from the orbital plane (2D) to Earth-Centered Inertial (ECI) coordinates.

**Step 1: Position in Orbital Plane**

For a circular orbit at radius $r$ and true anomaly $\nu$:

$$\vec{r}_{orbital} = r \begin{pmatrix} \cos\nu \\ \sin\nu \\ 0 \end{pmatrix}$$

**Step 2: Rotation by Inclination**

Rotate around the line of nodes (X-axis) by inclination $i$:

$$R_i = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos i & -\sin i \\ 0 & \sin i & \cos i \end{pmatrix}$$

**Step 3: Rotation by RAAN**

Rotate around the Z-axis by RAAN $\Omega$:

$$R_\Omega = \begin{pmatrix} \cos\Omega & -\sin\Omega & 0 \\ \sin\Omega & \cos\Omega & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Combined Transformation:**

$$\vec{r}_{ECI} = R_\Omega \cdot R_i \cdot \vec{r}_{orbital}$$

---

## 3. Sensor Cone Geometry

### Field of View (FOV)

A satellite's sensor has a half-angle $\theta_{FOV}$ defining its cone of visibility. The "footprint" on Earth depends on:
- Satellite altitude $h$
- Minimum elevation angle $\epsilon$ required by ground terminals
- Earth radius $R_E$

### Central Angle Calculation

The central angle (from Earth's center) subtended by the coverage circle is:

$$\theta_{central} = \arccos\left(\frac{R_E \cos\epsilon}{R_E + h}\right) - \epsilon$$

For a nadir-pointing sensor with half-angle $\theta_{FOV}$:

$$\theta_{central} = \arcsin\left(\frac{(R_E + h) \sin\theta_{FOV}}{R_E}\right) - \theta_{FOV}$$

### Footprint Radius

The ground footprint radius (arc length on Earth's surface) is:

$$r_{footprint} = R_E \cdot \theta_{central}$$

---

## 4. Cone Visualization

### Creating the Cone Mesh

We generate a cone pointing along the negative Z-axis (toward Earth's center when satellite is at +Z):

```python
def create_cone(radius, height, resolution=20):
    theta = np.linspace(0, 2*np.pi, resolution)
    r = np.linspace(0, radius, resolution)
    theta_grid, r_grid = np.meshgrid(theta, r)
    
    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)
    z = -r_grid * (height / radius)  # Cone points "down"
    
    return x, y, z
```

### Rotating the Cone to Point at Earth

The cone must always point toward Earth's center. Given satellite position $\vec{p}$:

1. **Down vector:** $\hat{d} = -\vec{p} / |\vec{p}|$
2. **Default up:** $\hat{u} = (0, 0, 1)$
3. **Rotation axis:** $\hat{k} = \hat{u} \times \hat{d}$
4. **Rotation angle:** $\theta = \arccos(\hat{u} \cdot \hat{d})$

Using Rodrigues' rotation formula:

$$R = I + \sin\theta \cdot K + (1 - \cos\theta) \cdot K^2$$

Where $K$ is the skew-symmetric matrix of $\hat{k}$:

$$K = \begin{pmatrix} 0 & -k_z & k_y \\ k_z & 0 & -k_x \\ -k_y & k_x & 0 \end{pmatrix}$$

---

## 5. Coverage Analysis

### Single Satellite Coverage

A single satellite covers a circular region on Earth's surface. The coverage area is:

$$A_{single} = 2\pi R_E^2 (1 - \cos\theta_{central})$$

### Constellation Coverage

For a full constellation, we must account for:
1. **Overlap regions** where multiple satellites see the same area
2. **Gap regions** where no satellite has coverage
3. **Latitude variation** (polar regions may have different coverage than equatorial)

### Coverage Metric

A common metric is the **percentage of Earth's surface** with at least one satellite in view:

$$\text{Coverage} = \frac{\text{Area with } \geq 1 \text{ satellite}}{\text{Total Earth Surface}} \times 100\%$$

---

## 6. Implementation Notes

### Animation Frame Update

Each animation frame:
1. Advances satellite true anomalies based on orbital period
2. Recalculates ECI positions for all satellites
3. Updates the sensor cone rotation for the tracked satellite
4. Redraws the scatter plot and cone surface

### Performance Considerations

- Cone mesh resolution is kept low (20 points) for smooth animation
- Only one satellite's cone is rendered to reduce computational load
- Satellite positions are pre-computed for all frames before animation starts

---

## References

1. Walker, J.G. "Satellite Constellations," Journal of the British Interplanetary Society, 1984
2. Wertz, J.R. and Larson, W.J. "Space Mission Analysis and Design" (SMAD), 3rd Edition
3. Vallado, D.A. "Fundamentals of Astrodynamics and Applications," 4th Edition
