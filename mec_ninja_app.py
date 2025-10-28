import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs
from utils.ecu_reader import read_ecu_info

st.set_page_config(page_title="Mec Ninja", layout="centered")

# 🔧 Branding Header
st.markdown("""
<h1 style='text-align: center; color: #d62828; font-size: 3em;'>🧰 Mec Ninja</h1>
<p style='text-align: center; font-size: 1.2em; color: #6c757d;'>
Plug-and-scan diagnostics for real-world mechanics.
</p>
""", unsafe_allow_html=True)

# 🛠️ Hero Section
st.markdown("""
<div style='text-align: center; margin-top: 2em;'>
    <h2 style='color: #343a40;'>Your Digital Toolbox</h2>
    <p style='font-size: 1.1em; color: #495057;'>
        Scan, diagnose, and fix vehicles with ease — no guesswork, just data.
    </p>
</div>
""", unsafe_allow_html=True)

# ⚙️ Feature Grid
st.markdown("""
<div style="display: flex; justify-content: space-around; margin-top: 3em;">
  <div style="width: 30%; text-align: center;">
    <h3>🔍 Live Scan</h3>
    <p>Read RPM, speed, throttle and more in real time.</p>
  </div>
  <div style="width: 30%; text-align: center;">
    <h3>🚨 Fault Codes</h3>
    <p>Instant fault detection with code descriptions.</p>
  </div>
  <div style="width: 30%; text-align: center;">
    <h3>🧠 Spec Match</h3>
    <p>Compare live data to expected specs for quick diagnosis.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# 🧪 Demo Mode Toggle
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

# 🔗 Footer
st.markdown("""
<hr>
<p style='text-align: center; font-size: 0.9em; color: #6c757d;'>
Built for Pan-African mechanics • <a href='https://github.com/your-repo' target='_blank'>GitHub</a>
</p>
""", unsafe_allow_html=True)
