import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs
from utils.ecu_reader import read_ecu_info
from utils.ai_advisor import get_recommendations  # ✅ NEW

st.set_page_config(page_title="Mec Ninja", layout="centered")
st.title("🧰 Mec Ninja — Car Diagnostic Web App")

demo_mode = st.checkbox("Run in Demo Mode", value=True)

if demo_mode:
    st.success("✅ Demo mode is ON. No car connection needed.")
    if st.button("Run Demo Scan"):
        # Simulated live data for demo
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

        st.subheader("🧠 AI Recommendations")  # ✅ NEW
        recommendations = get_recommendations(ecu_info, demo_faults)
        st.markdown(recommendations)

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

        st.subheader("🧠 AI Recommendations")  # ✅ NEW
        recommendations = get_recommendations(ecu_info, fault_codes)
        st.markdown(recommendations)
