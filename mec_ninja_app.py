import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs
from utils.ecu_reader import read_ecu_info

# Set wide layout for better space usage and responsiveness
st.set_page_config(page_title="Mec Ninja", layout="wide", page_icon="🧰")

# Custom CSS for global styling: Colors, fonts, spacing, and effects
st.markdown("""
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; }
.stButton>button { border-radius: 8px; background: linear-gradient(45deg, #d62828, #f77f00); color: white; font-weight: bold; border: none; padding: 0.5em 1em; transition: transform 0.2s; }
.stButton>button:hover { transform: scale(1.05); background: linear-gradient(45deg, #b22222, #e66a00); }
.stCheckbox>label { font-weight: bold; color: #495057; }
.stJson { background: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 1em; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.stExpander { border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.hero { text-align: center; padding: 2em; background: linear-gradient(135deg, #d62828, #f77f00); color: white; border-radius: 15px; margin-bottom: 2em; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
.feature-grid { display: flex; justify-content: space-around; gap: 1em; margin: 2em 0; }
.feature-card { background: white; padding: 1.5em; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; flex: 1; transition: box-shadow 0.3s; }
.feature-card:hover { box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
.footer { text-align: center; padding: 1em; background: #343a40; color: white; border-radius: 10px; margin-top: 3em; }
h1, h2, h3 { margin-bottom: 0.5em; }
p { line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# Main container for structured layout
with st.container():
    # 🔧 Branding Header with enhanced hero section
    st.markdown("""
    <div class="hero">
        <h1>🧰 Mec Ninja</h1>
        <p style='font-size: 1.2em;'>Plug-and-scan diagnostics for real-world mechanics.</p>
        <h2>Your Digital Toolbox</h2>
        <p>Scan, diagnose, and fix vehicles with ease — no guesswork, just data.</p>
    </div>
    """, unsafe_allow_html=True)

    # ⚙️ Feature Grid (Responsive cards)
    st.markdown("### Key Features")
    st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <h3>🔍 Live Scan</h3>
        <p>Read RPM, speed, throttle and more in real time.</p>
      </div>
      <div class="feature-card">
        <h3>🚨 Fault Codes</h3>
        <p>Instant fault detection with code descriptions.</p>
      </div>
      <div class="feature-card">
        <h3>🧠 Spec Match</h3>
        <p>Compare live data to expected specs for quick diagnosis.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# 🧪 Demo Mode Toggle (Kept as-is, with slight styling)
demo_mode = st.checkbox("🧪 Run in Demo Mode", value=True)

if demo_mode:
    st.success("✅ Demo mode is ON. No car connection needed.")
    if st.button("Run Demo Scan"):
        sample_data = {
            "RPM": "950 rpm",
            "SPEED": "0 km/h",
            "THROTTLE_POS": "1.2 %"
        }

        st.subheader("📊 Live Data")
        st.json(sample_data)

        st.subheader("🧠 Spec Match")
        match_specs("sample_model", sample_data)

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
            st.error(f"{code}: {desc}")

else:
    import obd
    connection = obd.OBD()
    st.success("✅ Connected to car.")
    if st.button("Run Live Scan"):
        commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
        live_data = {}

        for cmd in commands:
            response = connection.query(cmd)
            live_data[cmd.name] = str(response.value)

        st.subheader("📊 Live Data")
        st.json(live_data)

        st.subheader("🧠 Spec Match")
        match_specs("sample_model", live_data)

        st.subheader("🧠 ECU Info")
        ecu_info = read_ecu_info(connection)
        st.json(ecu_info)

        st.subheader("🚨 Fault Codes")
        fault_codes = get_fault_codes(connection)
        for code, desc in fault_codes:
            st.error(f"{code}: {desc}")

# 🔗 Footer (Enhanced with styling)
st.markdown("""
<div class="footer">
    <hr>
    <p>Built for Pan-African mechanics • <a href='https://github.com/your-repo' target='_blank' style='color: #f77f00;'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
