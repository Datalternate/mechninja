import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs
from utils.ecu_reader import read_ecu_info
import pandas as pd  # For simple charts (install if needed: pip install pandas)

# Set wide layout for hub-style dashboard
st.set_page_config(page_title="Mec Ninja Scan Hub", layout="wide", page_icon="🔧")

# Custom CSS for creative, mechanic-themed UI: Spanner icons, gradients, animations, and workshop feel
st.markdown("""
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: #ecf0f1; background-image: radial-gradient(circle, #34495e 1px, transparent 1px); background-size: 20px 20px; }
.logo { text-align: center; padding: 1.5em; background: linear-gradient(45deg, #e74c3c, #f39c12); color: white; border-radius: 20px; margin-bottom: 1em; box-shadow: 0 6px 12px rgba(0,0,0,0.3); font-size: 2.5em; animation: pulse 2s infinite; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
.stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; padding: 1.5em 0; background: rgba(52, 73, 94, 0.8); border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); backdrop-filter: blur(10px); }
.stTabs [data-baseweb="tab"] { height: 70px; white-space: pre-wrap; background-color: rgba(255, 255, 255, 0.1); border-radius: 12px; gap: 8px; padding: 20px; font-weight: bold; transition: all 0.4s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.2); border: 1px solid rgba(255, 255, 255, 0.2); }
.stTabs [data-baseweb="tab"]:hover { transform: translateY(-5px) rotate(1deg); box-shadow: 0 6px 12px rgba(0,0,0,0.4); background: rgba(255, 255, 255, 0.2); }
.stTabs [aria-selected="true"] { background: linear-gradient(45deg, #e74c3c, #f39c12) !important; color: white !important; box-shadow: 0 6px 12px rgba(231, 76, 60, 0.5); animation: glow 1.5s infinite alternate; }
@keyframes glow { from { box-shadow: 0 6px 12px rgba(231, 76, 60, 0.5); } to { box-shadow: 0 6px 20px rgba(231, 76, 60, 0.8); } }
.stButton>button { border-radius: 10px; background: linear-gradient(45deg, #e74c3c, #f39c12); color: white; font-weight: bold; border: none; padding: 0.7em 1.2em; transition: all 0.3s ease; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.stButton>button:hover { transform: scale(1.1) rotate(-2deg); background: linear-gradient(45deg, #c0392b, #e67e22); box-shadow: 0 6px 12px rgba(0,0,0,0.4); }
.stMetric { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 1.5em; box-shadow: 0 4px 8px rgba(0,0,0,0.2); text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); position: relative; overflow: hidden; }
.stMetric::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #e74c3c, #f39c12); }
.card { background: rgba(255, 255, 255, 0.1); padding: 2em; border-radius: 15px; box-shadow: 0 6px 12px rgba(0,0,0,0.2); margin: 1.5em 0; border: 1px solid rgba(255, 255, 255, 0.2); transition: transform 0.3s ease; }
.card:hover { transform: translateY(-5px); }
.hero { text-align: center; padding: 2.5em; background: linear-gradient(135deg, #e74c3c, #f39c12); color: white; border-radius: 20px; margin-bottom: 2em; box-shadow: 0 8px 16px rgba(0,0,0,0.3); }
.footer { text-align: center; padding: 1.5em; background: rgba(44, 62, 80, 0.9); color: #ecf0f1; border-radius: 15px; margin-top: 3em; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.sidebar { background: rgba(52, 73, 94, 0.8); padding: 1.5em; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.gauge { position: relative; width: 100px; height: 100px; margin: 0 auto; background: conic-gradient(#e74c3c 0deg, #f39c12 180deg, #34495e 360deg); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Creative logo with spanner theme at the top
st.markdown("""
<div class="logo">
    🔧 <strong>Mec Ninja Scan Hub</strong> 🔧
</div>
""", unsafe_allow_html=True)

# Sidebar for hub controls (model selection, demo toggle) with gear icon
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.header("⚙️ Mec Ninja Hub")
    vehicle_model = st.selectbox("Select Vehicle Model", ["sample_model", "Toyota Camry", "Ford F-150"], index=0)
    demo_mode = st.checkbox("🧪 Demo Mode", value=True)
    if demo_mode:
        st.success("✅ Demo mode active. 🔧 Ready to wrench!")
    else:
        st.info("🔗 Connect OBD-II for live scans. ⚙️ Gear up!")
    st.markdown("**About**: Your digital mechanic's toolbox. 🛠️")
    st.markdown('</div>', unsafe_allow_html=True)

# Main hub with creative, mechanic-themed tabs
tab1, tab2, tab3 = st.tabs(["🏠 Garage Home", "🔍 Live Scan Bay", "⚠️ Diagnostics Pit"])

with tab1:
    # Hero and features (hub welcome page) with spanner flair
    st.markdown("""
    <div class="hero">
        <h1>🔧 Mec Ninja Scan Hub</h1>
        <p style='font-size: 1.2em;'>Plug-and-scan diagnostics for real-world mechanics. 🛠️</p>
        <h2>Your Digital Toolbox</h2>
        <p>Scan, diagnose, and fix vehicles with ease — no guesswork, just data. ⚙️</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in a grid with hover animations
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔍 Live Scan Bay</h3>
        <p>Real-time RPM, speed, and throttle data. 🛠️</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
        <h3>🚨 Fault Codes Pit</h3>
        <p>Instant detection with wrench-ready descriptions. ⚙️</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card">
        <h3>🧠 Spec Match Garage</h3>
        <p>Compare to expected specs for quick diagnosis. 🔧</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    # Live Scan tab (dashboard-style with metrics, gauges, and charts)
    st.header("🔍 Live Scan Bay")
    if demo_mode:
        if st.button("Run Demo Scan 🛠️"):
            sample_data = {
                "RPM": 950,
                "SPEED": 0,
                "THROTTLE_POS": 1.2
            }
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RPM", f"{sample_data['RPM']} rpm", delta="Idle")
                st.markdown('<div class="gauge">RPM<br>950</div>', unsafe_allow_html=True)
            with col2:
                st.metric("Speed", f"{sample_data['SPEED']} km/h", delta="Stationary")
                st.markdown('<div class="gauge">Speed<br>0</div>', unsafe_allow_html=True)
            with col3:
                st.metric("Throttle", f"{sample_data['THROTTLE_POS']} %", delta="Low")
                st.markdown('<div class="gauge">Throttle<br>1.2%</div>', unsafe_allow_html=True)
            
            # Simple chart for visualization
            df = pd.DataFrame(sample_data, index=[0])
            st.bar_chart(df.T)
    else:
        import obd
        connection = obd.OBD()
        if connection.is_connected():
            st.success("✅ Connected to car. ⚙️ Engine humming!")
            if st.button("Run Live Scan 🛠️"):
                commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
                live_data = {}
                for cmd in commands:
                    response = connection.query(cmd)
                    live_data[cmd.name] = float(str(response.value).split()[0]) if response.value else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RPM", f"{live_data.get('RPM', 0)} rpm")
                    st.markdown(f'<div class="gauge">RPM<br>{live_data.get("RPM", 0)}</div>', unsafe_allow_html=True)
                with col2:
                    st.metric("Speed", f"{live_data.get('SPEED', 0)} km/h")
                    st.markdown(f'<div class="gauge">Speed<br>{live_data.get("SPEED", 0)}</div>', unsafe_allow_html=True)
                with col3:
                    st.metric("Throttle", f"{live_data.get('THROTTLE_POS', 0)} %")
                    st.markdown(f'<div class="gauge">Throttle<br>{live_data.get("THROTTLE_POS", 0)}%</div>', unsafe_allow_html=True)
                
                # Chart for live data
                df = pd.DataFrame(live_data, index=[0])
                st.line_chart(df.T)
        else:
            st.error("❌ No OBD connection. 🔧 Check your tools!")

with tab3:
    # Diagnostics tab (faults, spec match, ECU) with pit theme
    st.header("⚠️ Diagnostics Pit")
    if demo_mode:
        if st.button("Run Demo Diagnostics 🛠️"):
            sample_data = {"RPM": "950 rpm", "SPEED": "0 km/h", "THROTTLE_POS": "1.2 %"}
            
            st.subheader("🧠 Spec Match Garage")
            match_specs(vehicle_model, sample_data)
            
            st.subheader("🧠 ECU Info Bay")
            ecu_info = read_ecu_info(demo=True)
            st.json(ecu_info)
            
            st.subheader("🚨 Fault Codes Pit")
            demo_faults = [
                ("P0301", "Cylinder 1 Misfire Detected"),
                ("P0174", "System Too Lean (Bank 2)"),
                ("P0455", "Evaporative Emission System Leak Detected (gross leak)")
            ]
            for code, desc in demo_faults:
                st.error(f"🚨 {code}: {desc} ⚙️")
    else:
        import obd
        connection = obd.OBD()
        if connection.is_connected() and st.button("Run Live Diagnostics 🔧"):
            commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
            live_data = {}
            for cmd in commands:
                response = connection.query(cmd)
                live_data[cmd.name] = str(response.value)
            
            st.subheader("🧠 Spec Match Garage")
            match_specs(vehicle_model, live_data)
            
            st.subheader("🧠 ECU Info Bay")
            ecu_info = read_ecu_info(connection)
            st.json(ecu_info)
            
            st.subheader("🚨 Fault Codes Pit")
            fault_codes = get_fault_codes(connection)
            for code, desc in fault_codes:
                st.error(f"🚨 {code}: {desc} ⚙️")
        else:
            st.info("Connect OBD-II to run diagnostics. 🛠️ Gear up!")

# Footer with mechanic flair
st.markdown("""
<div class="footer">
    <hr>
    <p>Built for Pan-African mechanics • <a href='https://github.com/your-repo' target='_blank' style='color: #f39c12;'>GitHub</a> 🔧</p>
</div>
""", unsafe_allow_html=True)
