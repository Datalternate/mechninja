import obd

def get_fault_codes(connection):
    dtc_response = connection.query(obd.commands.GET_DTC)
    codes = dtc_response.value

    if not codes:
        print("✅ No fault codes detected.")
        return

    print("🚨 Fault Codes Found:")
    for code, desc in codes:
        print(f"{code}: {desc}")
