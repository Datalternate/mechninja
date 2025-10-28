import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs
from utils.ecu_reader import read_ecu_info
import pandas as pd  # For simple dataframes/charts if needed

# Set wide layout for dashboard feel
st.set_page_config(page_title="Mec Ninja Scan Hub", layout="wide", page_icon="🧰")

# Custom CSS for hub-like styling: Dashboard theme, cards, metrics
st.markdown("""
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; }
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #e9ecef; border-radius: 4px 4px 0 0; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
.stTabs [aria-selected="true"] { background-color: #d62828 !important; color: white !important; }
.stButton>button { border-radius: 8px; background: linear-gradient(45deg, #d62828, #f77f00); color: white; font-weight: bold; border: none; padding: 0.5em 1em; transition: transform 0.2s; }
.stButton>button:hover { transform: scale(1.05); background: linear-gradient(45deg, #b22222, #e66a00); }
.stMetric { background: white; border-radius: 10px; padding: 1em; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
.card { background: white; padding: 1.5em; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 1em 0; }
.hero { text-align: center; padding: 2em; background: linear-gradient(135deg, #d62828, #f77f00); color: white; border-radius: 15px; margin-bottom: 2em; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.footer { text-align: center; padding: 1em; background: #343a40; color: white; border-radius: 10px; margin-top: 3em; }
.sidebar { background: #f1f3f4; padding: 1em; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Sidebar for hub settings (like a control panel)
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.header("🧰 Mec Ninja Hub")
    vehicle_model = st.selectbox("Select Vehicle Model", ["sample_model", "Toyota Camry", "Ford F-150"], index=0)
    demo_mode = st.checkbox("🧪 Demo Mode", value=True)
    if demo_mode:
        st.success("✅ Demo mode active.")
    else:
        st.info("🔗 Connect OBD-II for live scans.")
    st.markdown("**About**: Your diagnostic toolbox.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main hub with tabs for organization
tab1, tab2, tab3 = st.tabs(["🏠 Home", "🔍 Live Scan", "🚨 Diagnostics"])

with tab1:
    # Hero and features (hub welcome page)
    st.markdown("""
    <div class="hero">
        <h1>🧰 Mec Ninja Scan Hub</h1>
        <p style='font-size: 1.2em;'>Plug-and-scan diagnostics for real-world mechanics.</p>
        <h2>Your Digital Toolbox</h2>
        <p>Scan, diagnose, and fix vehicles with ease — no guesswork, just data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in a grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔍 Live Scan</h3>
        <p>Real-time RPM, speed, and throttle data.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
        <h3>🚨 Fault Codes</h3>
        <p>Instant detection with descriptions.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
        <h3>🧠 Spec Match</h3>
        <p>Compare to expected specs.</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    # Live Scan tab (dashboard-style with metrics)
    st.header("🔍 Live Scan Dashboard")
    if demo_mode:
        if st.button("Run Demo Scan"):
            sample_data = {
                "RPM": 950,
                "SPEED": 0,
                "THROTTLE_POS": 1.2
            }
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RPM", f"{sample_data['RPM']} rpm", delta="Idle")
            with col2:
                st.metric("Speed", f"{sample_data['SPEED']} km/h", delta="Stationary")
            with col3:
                st.metric("Throttle", f"{sample_data['THROTTLE_POS']} %", delta="Low")
            
            # Simple chart for visualization
            df = pd.DataFrame(sample_data, index=[0])
            st.bar_chart(df.T)
    else:
        import obd
        connection = obd.OBD()
        if connection.is_connected():
            st.success("✅ Connected to car.")
            if st.button("Run Live Scan"):
                commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
                live_data = {}
                for cmd in commands:
                    response = connection.query(cmd)
                    live_data[cmd.name] = float(str(response.value).split()[0]) if response.value else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RPM", f"{live_data.get('RPM', 0)} rpm")
                with col2:
                    st.metric("Speed", f"{live_data.get('SPEED', 0)} km/h")
                with col3:
                    st.metric("Throttle", f"{live_data.get('THROTTLE_POS', 0)} %")
                
                # Chart for live data
                df = pd.DataFrame(live_data, index=[0])
                st.line_chart(df.T)
        else:
            st.error("❌ No OBD connection.")

with tab3:
    # Diagnostics tab (faults, spec match, ECU)
    st.header("🚨 Diagnostics Hub")
    if demo_mode:
        if st.button("Run Demo Diagnostics"):
            sample_data = {"RPM": "950 rpm", "SPEED": "0 km/h", "THROTTLE_POS": "1.2 %"}
            
            st.subheader("🧠 Spec Match")
            match_specs(vehicle_model, sample_data)
            
            st.subheader("🧠 ECU Info")
            ecu_info = read_ecu_info(demo=True)
            st.json(ecu_info)
            
            st.subheader("🚨 Fault Codes")
            demo_faults = [
                ("P0301", "Cylinder 1 Misfire Detected"),
                ("P0174", "System Too Lean (Bank 2)"),
                ("P0455", "Evaporative Emission System Leak Detected (gross leak)")
            ]
            for code, desc in demo_faults:
                st.error(f"🚨 {code}: {desc}")
    else:
        import obd
        connection = obd.OBD()
        if connection.is_connected() and st.button("Run Live Diagnostics"):
            commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
            live_data = {}
            for cmd in commands:
                response = connection.query(cmd)
                live_data[cmd.name] = str(response.value)
            
            st.subheader("🧠 Spec Match")
            match_specs(vehicle_model, live_data)
            
            st.subheader("🧠 ECU Info")
            ecu_info = read_ecu_info(connection)
            st.json(ecu_info)
            
            st.subheader("🚨 Fault Codes")
            fault_codes = get_fault_codes(connection)
            for code, desc in fault_codes:
                st.error(f"🚨 {code}: {desc}")
        else:
            st.info("Connect OBD-II to run diagnostics.")

# Footer
st.markdown("""
<div class="footer">
    <hr>
    <p>Built for Pan-African mechanics • <a href='https://github.com/your-repo' target='_blank' style='color: #f77f00;'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
