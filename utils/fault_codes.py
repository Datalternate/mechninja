def get_fault_codes(connection=None, demo=True):
    if demo:
        codes = [
            ("P0300", "Random/Multiple Cylinder Misfire Detected"),
            ("P0420", "Catalyst System Efficiency Below Threshold"),
            ("P0171", "System Too Lean (Bank 1)")
        ]
    else:
        import obd
        dtc_response = connection.query(obd.commands.GET_DTC)
        codes = dtc_response.value

    if not codes:
        print("✅ No fault codes detected.")
        return

    print("🚨 Fault Codes Found:")
    for code, desc in codes:
        print(f"{code}: {desc}")
