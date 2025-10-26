import json
import streamlit as st

def match_specs(model, live_data):
    try:
        with open(f"specs/{model}.json") as f:
            expected = json.load(f)
    except FileNotFoundError:
        st.warning(f"Spec file for {model} not found.")
        return

    for key, value in live_data.items():
        if key in expected and value != expected[key]:
            st.error(f"{key} mismatch: got {value}, expected {expected[key]}")
        else:
            st.success(f"{key} OK: {value}")
