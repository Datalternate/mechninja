import obd
from utils.matcher import match_specs
from utils.fault_codes import get_fault_codes

connection = obd.OBD()
commands = [obd.commands.RPM, obd.commands.SPEED, obd.commands.THROTTLE_POS]
live_data = {}

for cmd in commands:
    response = connection.query(cmd)
    live_data[cmd.name] = str(response.value)

match_specs("sample_model", live_data)
get_fault_codes(connection)
