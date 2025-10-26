def read_ecu_info(connection=None, demo=False):
    if demo:
        return {
            "ECU Name": "Bosch ME7.5",
            "Firmware Version": "1.9.3",
            "Calibration ID": "CAL12345678",
            "VIN": "KNDJT2A56D1234567"
        }

    import obd
    ecu_data = {}

    try:
        ecu_data["ECU Name"] = str(connection.query(obd.commands.ELM_VERSION).value)
        ecu_data["Firmware Version"] = str(connection.query(obd.commands.ELM_ID).value)
        ecu_data["Calibration ID"] = str(connection.query(obd.commands.CALID).value)
        ecu_data["VIN"] = str(connection.query(obd.commands.VIN).value)
    except Exception as e:
        ecu_data["Error"] = f"ECU read failed: {e}"

    return ecu_data
