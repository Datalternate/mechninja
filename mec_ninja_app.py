import streamlit as st
from utils.fault_codes import get_fault_codes
from utils.matcher import match_specs

st.set_page_config(page_title="Mec Ninja", layout="centered")
st.title("🧰 Mec Ninja — Car Diagnostic Web App")

demo_mode = st.checkbox("Run in Demo Mode", value=True)

if demo_mode:
    st.success("Demo mode is ON. No car connection needed.")
    if st.button("Run Demo Scan"):
        sample_data = {
            "RPM": "700 rpm",
            "SPEED": "0 km/h",
            "THROTTLE_POS": "0.0 %"
        }
        st.subheader("📊 Live Data")
        st.json(sample_data)

        st.subheader("🧠 Spec Match")
        match_specs("sample_model", sample_data)

        st.subheader("🚨 Fault Codes")
        get_fault_codes(demo=True)
else:
    import obd
    connection = obd.OBD()
    st.success("Connected to car.")
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

        st.subheader("🚨 Fault Codes")
        get_fault_codes(connection)
