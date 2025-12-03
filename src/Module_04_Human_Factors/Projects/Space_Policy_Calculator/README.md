# Space Policy Risk Calculator

**Module:** 4 (Human Factors & Regulations)  
**Concepts:** Space Law, Risk Assessment, Regulatory Compliance

## 🎓 What You'll Learn

| Concept | Application |
|---------|-------------|
| **Orbital Debris Rules** | UN 25-year guideline |
| **Spectrum Licensing** | FCC and ITU coordination |
| **Launch Licensing** | FAA Part 450 requirements |
| **Collision Avoidance** | Space situational awareness |
| **Planetary Protection** | COSPAR contamination rules |

## Project Overview

A regulatory compliance and risk assessment framework for space missions. Evaluates missions against six key policy areas with quantitative scoring.

## Global Space Regulatory Bodies

| Agency | Country/Region | Jurisdiction |
|--------|----------------|--------------|
| **FAA** | USA | Launch/reentry licensing |
| **FCC** | USA | Communications spectrum |
| **NOAA** | USA | Earth observation |
| **NASA** | USA | Planetary protection (US) |
| **ESA** | Europe | Debris mitigation |
| **JAXA** | Japan | Space activities law |
| **CNSA** | China | National space law |
| **ISRO** | India | Space licensing |
| **Roscosmos** | Russia | Launch coordination |
| **ITU** | International | Spectrum allocation |
| **UNOOSA** | International | Space treaties |
| **COSPAR** | International | Planetary protection |

## Installation & Usage

```bash
pip install -r requirements.txt
python calculator.py
```

## Risk Categories

### 1. Orbital Debris (UN Guidelines)
- **25-Year Rule:** Satellites must deorbit within 25 years
- **Propulsion:** Active vs. passive deorbit capability
- **Altitude:** Higher orbits = longer lifetime = more risk
- **Reference:** UN Space Debris Mitigation Guidelines (2007)

### 2. Collision Risk (SSA)
- **Maneuverability:** Collision avoidance capability
- **Trackability:** Can ground radar monitor it?
- **Regime:** LEO congestion vs. MEO/GEO spacing
- **Reference:** USSPACECOM conjunction assessments

### 3. Spectrum Allocation (FCC/ITU)
- **Licensing:** National and international coordination
- **Interference:** Potential to disrupt other systems
- **Astronomy:** Impact on radio astronomy
- **Reference:** ITU Radio Regulations, FCC Part 25

### 4. Human Safety (FAA Part 460)
- **Crew Safety:** Abort systems, life support
- **Public Safety:** Launch/reentry trajectories
- **Flight Termination:** Emergency destruct systems
- **Reference:** 14 CFR Parts 450, 460

### 5. Environmental (NEPA)
- **Launch Site:** Environmental impact assessment
- **Wildlife:** Protected species considerations
- **Propellant:** Toxicity and emissions
- **Reference:** National Environmental Policy Act

### 6. Planetary Protection (COSPAR)
- **Destination:** Category I-V classification
- **Bioburden:** Sterilization requirements
- **Sample Return:** Earth protection protocols
- **Reference:** COSPAR Planetary Protection Policy

## Demo Scenarios

The calculator includes three example missions:

1. **LEO Communication Constellation**
   - Low debris risk (has propulsion)
   - Medium spectrum risk (mega-constellation)
   - Low collision risk (maneuverable)

2. **Crewed Mars Mission**
   - High human safety requirements
   - High planetary protection (Mars special region)
   - Complex environmental review

3. **Uncontrolled CubeSat**
   - High debris risk (no propulsion)
   - High collision risk (non-maneuverable)
   - Regulatory compliance challenges

## Risk Scoring

| Score | Level | Action Required |
|-------|-------|-----------------|
| 0-25 | LOW | Standard compliance |
| 25-50 | MEDIUM | Enhanced documentation |
| 50-75 | HIGH | Mitigation required |
| 75-100 | CRITICAL | Major redesign needed |

## Key Space Treaties

| Treaty | Year | Key Provisions |
|--------|------|----------------|
| Outer Space Treaty | 1967 | Non-appropriation, peaceful use |
| Rescue Agreement | 1968 | Astronaut assistance |
| Liability Convention | 1972 | Damage responsibility |
| Registration Convention | 1975 | Object tracking |
| Moon Agreement | 1979 | Resource exploitation |

## Limitations

This is a simplified educational tool. Real regulatory assessments involve:
- Detailed mission-specific analysis
- Legal review and agency coordination
- Years of documentation
- Quantitative collision probability (NASA DAS, ESA DRAMA)

## References

- FAA Office of Commercial Space Transportation
- NASA Orbital Debris Program Office
- ESA Space Debris Office
- COSPAR Planetary Protection Policy
- UN Committee on Peaceful Uses of Outer Space

See `EXPLANATION.md` for complete policy explanations.
