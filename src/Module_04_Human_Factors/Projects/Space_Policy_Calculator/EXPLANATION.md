# Space Policy Risk Calculator - Technical Explanation

## Why Policy Matters for Engineers

Engineering doesn't happen in isolation. Every SpaceX mission must satisfy:

1. **FAA**: Launch license, range safety, environmental review
2. **FCC**: Spectrum license for communications
3. **NASA**: If using government facilities or carrying NASA crew
4. **International**: ITU coordination, Outer Space Treaty obligations
5. **Self-imposed**: SpaceX's own safety standards

Ignoring these leads to delays (Boca Chica environmental review took years) or denial (various companies have failed to get licenses).

---

## Risk Assessment Framework

### Methodology

I use a **semi-quantitative risk scoring** approach:

1. **Identify** risk factors relevant to space missions
2. **Score** each factor 0-100 based on mission parameters
3. **Weight** factors by severity level
4. **Aggregate** into overall risk score
5. **Classify** into risk levels (Low/Medium/High/Critical)

This mirrors approaches used in:
- NASA Mission Risk Assessment
- FAA Safety Analysis
- Insurance underwriting for space missions

### Scoring Logic

Each risk factor is scored based on objective criteria:

```python
# Example: Debris Risk Scoring
if has_propulsion:
    score = 10  # Can actively deorbit
elif estimated_lifetime <= 25:
    score = 30  # Natural decay compliant
elif altitude > 800:
    score = 80  # Long-lived debris
else:
    score = 60  # Non-compliant but lower orbit
```

### Weighting

Higher severity factors contribute more to the overall score:

| Level | Weight | Rationale |
|-------|--------|-----------|
| LOW | 1.0x | Minor compliance issues |
| MEDIUM | 1.5x | Requires attention |
| HIGH | 2.0x | Could block mission |
| CRITICAL | 3.0x | Showstopper |

---

## Risk Categories Deep Dive

### 1. Orbital Debris

**The Problem**: Space is getting crowded. There are ~36,000 tracked objects, millions untracked. Collisions create more debris (Kessler Syndrome).

**Key Regulations**:
- **UN Guidelines (2007)**: 25-year post-mission disposal
- **FCC Rules (2022)**: Now requires 5-year disposal for new US satellites
- **NASA Standard 8719.14**: US government missions

**Assessment Logic**:
```
Estimated Lifetime = f(altitude, ballistic coefficient)
- < 400 km: ~1 year
- 550 km (Starlink): ~5 years
- 800 km: ~25-100 years
- 1000+ km: Centuries
```

If `has_propulsion` AND `altitude < 2000 km`: satellite can actively deorbit → LOW risk

### 2. Collision Risk

**The Problem**: More satellites = more conjunction events. ISS performs ~3 avoidance maneuvers per year.

**Key Actors**:
- **18th Space Control Squadron**: Tracks objects, issues collision warnings
- **Space Fence**: New radar, tracks smaller objects
- **Commercial SSA**: LeoLabs, ExoAnalytic provide additional data

**Assessment Logic**:
```
if maneuverable AND trackable:
    Can coordinate avoidance → LOW risk
elif trackable only:
    Others must maneuver for you → MEDIUM-HIGH risk
else:
    Invisible hazard → CRITICAL risk
```

### 3. Spectrum Allocation

**The Problem**: RF spectrum is finite. Satellite communications compete with:
- Other satellites
- Terrestrial systems
- Astronomy (radio telescopes)

**Key Regulations**:
- **FCC Part 25**: US satellite licensing
- **ITU Radio Regulations**: International coordination
- **EPFD limits**: Protect GEO from LEO interference

**Assessment Logic**:
```
if licensed:
    Coordinated with regulators → LOW risk
if mega_constellation (>1000 sats):
    Extra scrutiny, astronomy concerns → Elevated risk
if unlicensed:
    Potential enforcement action → HIGH risk
```

### 4. Human Safety

**The Problem**: Space is dangerous. Crew and public must be protected.

**Key Regulations**:
- **FAA 14 CFR Part 460**: Informed consent, crew qualifications
- **NASA-STD-3001**: Human systems integration
- **Range Safety**: Flight termination requirements

**Assessment Logic**:
```
if crewed:
    Baseline risk (life support, abort) → MEDIUM
if uncontrolled_reentry:
    Debris survival, random impact → HIGH risk
if overflight_population:
    Launch trajectory risk → Elevated
```

### 5. Environmental

**The Problem**: Launch sites impact local environment—noise, wildlife, emissions.

**Key Regulations**:
- **NEPA**: Environmental Impact Statement required
- **Endangered Species Act**: If protected species present
- **Coastal Zone Management Act**: Coastal areas

**SpaceX Example**: Boca Chica Starship launches required:
- Environmental Assessment → Programmatic Environmental Assessment
- Wildlife monitoring (shorebirds, sea turtles)
- Launch windows to avoid nesting seasons
- Noise mitigation

### 6. Planetary Protection

**The Problem**: Don't contaminate other worlds with Earth life (forward) or contaminate Earth with extraterrestrial material (backward).

**COSPAR Categories**:
| Category | Target | Requirements |
|----------|--------|--------------|
| I | Sun, Mercury | None |
| II | Moon, Venus | Documentation only |
| III | Mars (flyby/orbiter) | Contamination assessment |
| IV | Mars (lander) | Bioburden limits, sterilization |
| V | Sample return | Containment, quarantine |

**Assessment Logic**:
```
if destination in [Mars, Europa, Enceladus, Titan]:
    Astrobiological interest → HIGH requirements
else:
    Standard cleanliness → LOW risk
```

---

## Code Architecture

```
calculator.py
├── RiskLevel (Enum)
│   └── LOW, MEDIUM, HIGH, CRITICAL with colors
│
├── RiskFactor (dataclass)
│   └── name, category, level, score, description, mitigation, regulation
│
├── MissionProfile (dataclass)
│   └── All mission parameters (altitude, propulsion, crewed, etc.)
│
├── RiskAssessment (dataclass)
│   ├── factors: List[RiskFactor]
│   ├── overall_score, overall_level
│   └── add_factor(), _recalculate_overall()
│
├── SpacePolicyCalculator (class)
│   ├── assess_mission() - Main entry point
│   ├── _assess_debris_risk()
│   ├── _assess_collision_risk()
│   ├── _assess_spectrum_risk()
│   ├── _assess_human_safety()
│   ├── _assess_environmental()
│   ├── _assess_planetary_protection()
│   ├── generate_report() - Text output
│   └── plot_results() - Visual dashboard
│
└── run_demo() - Example scenarios
```

---

## Validation

### Starlink Sanity Check

Real Starlink parameters:
- 550 km altitude ✓
- Krypton ion propulsion ✓
- Ku/Ka licensed spectrum ✓
- FCC-coordinated ✓

Calculator output: **LOW-MEDIUM risk** (elevated for constellation size)

This matches reality: Starlink is operational with some ongoing spectrum coordination issues.

### Worst-Case Sanity Check

Hypothetical "bad" mission:
- 850 km, no propulsion
- Untrackable
- Unlicensed spectrum
- 200 satellites

Calculator output: **CRITICAL risk**

This matches reality: Such a mission would likely be denied licensing.

---

## Limitations and Future Work

### Current Simplifications

1. **Qualitative**: Real assessments use Monte Carlo collision probability
2. **Static**: Doesn't account for changing regulations
3. **US-centric**: Focuses on FAA/FCC, not ESA/JAXA/etc.
4. **Generic**: Doesn't include mission-specific factors

### Potential Extensions

1. **Collision Probability**: Implement NASA DAS-style calculation
2. **Timeline Risk**: Model regulatory timeline (how long to get licensed)
3. **Cost Impact**: Estimate compliance costs ($$$)
4. **Multi-jurisdiction**: Add ESA, JAXA, CNSA regulations
5. **ML Enhancement**: Train on historical mission outcomes

---

## SpaceX Relevance

This project demonstrates:

1. **Regulatory Awareness**: Understanding that engineering exists within constraints
2. **Systems Thinking**: Holistic view of mission success factors
3. **Risk Quantification**: Turning qualitative concerns into actionable scores
4. **Policy Translation**: Bridging technical and regulatory domains

SpaceX roles in Launch Operations, Mission Assurance, and Regulatory Affairs all require this perspective. The company's success comes partly from navigating (and sometimes pushing back on) regulatory requirements efficiently.

