"""
Propellant Explorer - Interactive Dashboard
============================================
A Streamlit web application for learning about rocket propellants.

Run with: streamlit run app.py

Author: Rocket Basics Project
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math

# Import our custom modules
from reaction_logic import RocketReaction
from physics_logic import RocketPhysics

# Initialize the engines
reaction_engine = RocketReaction()
physics_engine = RocketPhysics()

# Page configuration
st.set_page_config(
    page_title="Propellant Explorer",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .success-text { color: #00ff00; }
    .warning-text { color: #ffaa00; }
    .danger-text { color: #ff4444; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 Propellant Explorer")
st.markdown("*Learn how different rocket fuels affect mission capability*")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Efficiency Showdown", 
    "⚖️ Tank Size Reality", 
    "🎮 Mission Calculator",
    "⚗️ Chemistry Balancer"
])

# ========================================
# TAB 1: Efficiency Showdown
# ========================================
with tab1:
    st.header("The Efficiency Showdown")
    st.markdown("""
    **Specific Impulse (Isp)** is the "miles per gallon" of rockets. 
    Higher is better! But there's a catch...
    """)
    
    # Create comparison data
    fuel_data = []
    for name, info in physics_engine.fuels.items():
        fuel_data.append({
            "Propellant": name.split(" (")[0],
            "Sea Level Isp": info["isp_sl"],
            "Vacuum Isp": info["isp_vac"],
            "Density": info["density"],
            "Used By": info["used_by"]
        })
    
    df = pd.DataFrame(fuel_data)
    
    # Bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Sea Level',
        x=df['Propellant'],
        y=df['Sea Level Isp'],
        marker_color='#ff6b6b'
    ))
    fig.add_trace(go.Bar(
        name='Vacuum',
        x=df['Propellant'],
        y=df['Vacuum Isp'],
        marker_color='#4ecdc4'
    ))
    
    fig.update_layout(
        title="Specific Impulse Comparison",
        xaxis_title="Propellant Type",
        yaxis_title="Specific Impulse (seconds)",
        barmode='group',
        template='plotly_dark',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Educational note
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **💡 Why two values?**
        
        - **Sea Level**: Engine fighting against air pressure
        - **Vacuum**: Engine in space (more efficient!)
        
        Rocket nozzles are designed to work best at one altitude.
        """)
    
    with col2:
        st.info("""
        **💡 The Trade-off**
        
        Hydrogen has the BEST efficiency... but look at the density tab!
        It's so "fluffy" that you need enormous tanks to carry enough.
        """)

# ========================================
# TAB 2: Tank Size Reality Check
# ========================================
with tab2:
    st.header("The Tank Size Reality Check")
    st.markdown("""
    Students often think "Hydrogen is best!" until they see tank sizes...
    """)
    
    # Create bubble chart data
    bubble_data = []
    for name, info in physics_engine.fuels.items():
        bubble_data.append({
            "Propellant": name.split(" (")[0],
            "Efficiency (Isp)": info["isp_vac"],
            "Density": info["density"],
            "Tank Volume": 1 / info["density"],  # Relative tank size
            "Color": info["color"]
        })
    
    bubble_df = pd.DataFrame(bubble_data)
    
    fig2 = px.scatter(
        bubble_df,
        x="Efficiency (Isp)",
        y="Density",
        size="Tank Volume",
        color="Propellant",
        hover_data=["Tank Volume"],
        size_max=60,
        template='plotly_dark',
        title="Efficiency vs Density (bubble size = relative tank volume)"
    )
    
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Tank comparison
    st.subheader("For the same amount of energy:")
    
    cols = st.columns(4)
    base_volume = 1.0 / 0.81  # RP-1 as baseline
    
    for i, (name, info) in enumerate(physics_engine.fuels.items()):
        relative_volume = (1 / info["density"]) / base_volume
        short_name = name.split(" (")[0]
        
        with cols[i]:
            st.metric(
                label=short_name,
                value=f"{relative_volume:.1f}x",
                delta=f"Isp: {info['isp_vac']}s"
            )
    
    st.warning("""
    **The Goldilocks Problem:** Hydrogen tanks need to be ~10x larger than Kerosene tanks!
    That's why the Space Shuttle's orange tank was so massive. Methane is the "just right" choice.
    """)

# ========================================
# TAB 3: Mission Calculator
# ========================================
with tab3:
    st.header("🎮 Design Your Rocket!")
    st.markdown("Can you reach orbit? Mars? Adjust the sliders and find out!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Rocket Parameters")
        
        fuel_choice = st.selectbox(
            "Select Propellant",
            physics_engine.get_fuel_options(),
            index=1  # Default to Methalox
        )
        
        payload_mass = st.slider(
            "Payload Mass (kg)",
            min_value=100,
            max_value=50000,
            value=5000,
            step=100,
            help="Satellite, crew capsule, or cargo"
        )
        
        structure_mass = st.slider(
            "Structure Mass (kg)",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000,
            help="Rocket body, engines, tanks (empty)"
        )
        
        fuel_mass = st.slider(
            "Fuel Mass (kg)",
            min_value=10000,
            max_value=500000,
            value=100000,
            step=10000,
            help="Propellant loaded in tanks"
        )
        
        dry_mass = payload_mass + structure_mass
    
    with col2:
        # Calculate results
        delta_v = physics_engine.calculate_delta_v(fuel_choice, dry_mass, fuel_mass)
        mass_ratio = physics_engine.calculate_mass_ratio(dry_mass, fuel_mass)
        fuel_fraction = physics_engine.calculate_fuel_fraction(dry_mass, fuel_mass)
        mission_status = physics_engine.check_mission_status(delta_v)
        
        # Display metrics
        st.subheader("Results")
        
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.metric("Delta-V", f"{delta_v:,.0f} m/s")
        with metric_cols[1]:
            st.metric("Mass Ratio", f"{mass_ratio:.2f}")
        with metric_cols[2]:
            st.metric("Fuel Fraction", f"{fuel_fraction:.1f}%")
        
        # Mission gauge
        st.subheader("Mission Capability")
        
        # Create gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=delta_v,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Delta-V (m/s)"},
            delta={'reference': 9400, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [0, 20000], 'tickwidth': 1},
                'bar': {'color': "#00d4ff"},
                'steps': [
                    {'range': [0, 2000], 'color': '#333333'},
                    {'range': [2000, 9400], 'color': '#4a4a00'},
                    {'range': [9400, 12500], 'color': '#004a00'},
                    {'range': [12500, 16000], 'color': '#004a4a'},
                    {'range': [16000, 20000], 'color': '#4a004a'},
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': delta_v
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=300,
            template='plotly_dark',
            annotations=[
                dict(x=0.1, y=0.35, text="Suborbital", showarrow=False),
                dict(x=0.35, y=0.35, text="LEO", showarrow=False),
                dict(x=0.6, y=0.35, text="Moon", showarrow=False),
                dict(x=0.85, y=0.35, text="Mars", showarrow=False),
            ]
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Mission status
        if delta_v >= 16000:
            st.success("🔴 MARS CAPABLE! You can reach the Red Planet!")
        elif delta_v >= 12500:
            st.success("🌙 LUNAR CAPABLE! Next stop: the Moon!")
        elif delta_v >= 9400:
            st.success("🛰️ LEO CAPABLE! You can reach orbit!")
        elif delta_v >= 2000:
            st.warning("🚀 SUBORBITAL: You'll touch space but come back down.")
        else:
            st.error("❌ GROUNDED: Not enough delta-v to reach space.")

# ========================================
# TAB 4: Chemistry Balancer
# ========================================
with tab4:
    st.header("⚗️ Balance the Reaction")
    st.markdown("""
    Rocket engines need the **perfect mix** of fuel and oxidizer. 
    Too much fuel? Wasted energy. Too much oxygen? ENGINE MELTS! 🔥
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Select Propellant")
        
        chem_fuel = st.selectbox(
            "Propellant Type",
            reaction_engine.get_fuel_options(),
            key="chem_fuel"
        )
        
        st.markdown(f"**Reaction:** `{reaction_engine.get_formula(chem_fuel)}`")
        st.markdown(f"*{reaction_engine.get_description(chem_fuel)}*")
        
        st.subheader("Your Guess")
        
        user_fuel = st.number_input(
            "Fuel Coefficient",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.5,
            help="How many molecules of fuel?"
        )
        
        user_ox = st.number_input(
            "Oxidizer (O₂) Coefficient",
            min_value=0.1,
            max_value=20.0,
            value=1.0,
            step=0.5,
            help="How many molecules of oxygen?"
        )
        
        check_button = st.button("Check Balance!", type="primary")
    
    with col2:
        st.subheader("Result")
        
        if check_button:
            result = reaction_engine.check_balance(chem_fuel, user_fuel, user_ox)
            
            if result["status"] == "Perfect":
                st.success(result["message"])
                st.balloons()
            elif result["status"] == "Fuel Rich":
                st.warning(result["message"])
            else:
                st.error(result["message"])
            
            # Visual feedback
            fig_balance = go.Figure(go.Indicator(
                mode="gauge",
                value=user_ox / user_fuel if user_fuel > 0 else 0,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "O₂/Fuel Ratio"},
                gauge={
                    'axis': {'range': [0, 5]},
                    'bar': {'color': result["color"]},
                    'steps': [
                        {'range': [0, 1.5], 'color': 'orange'},
                        {'range': [1.5, 2.5], 'color': 'green'},
                        {'range': [2.5, 5], 'color': 'red'},
                    ]
                }
            ))
            fig_balance.update_layout(height=250, template='plotly_dark')
            st.plotly_chart(fig_balance, use_container_width=True)
        else:
            st.info("👆 Enter your coefficients and click 'Check Balance!'")
            st.markdown("""
            **Hints:**
            - Hydrogen: Simple! H₂ + O₂ → H₂O
            - Methane: CH₄ needs more oxygen because it has carbon
            - Kerosene: Complex hydrocarbon, needs LOTS of oxygen
            """)

# Footer
st.markdown("---")
st.markdown("""
*Part of the [Rocket Basics](https://github.com/yourusername/rocket-basics) educational project.*

**Learn more:**
- [NASA Glenn Research Center](https://www.grc.nasa.gov/www/k-12/rocket/)
- [SpaceX](https://www.spacex.com)
""")

