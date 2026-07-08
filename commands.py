from flight_logic import IDLE, CRUISE, WARMING, COMMS_RECOVERY, SAFE


def generate_commands(mode):
    """
    Generate spacecraft subsystem commands based on the current mode.
    """

    if mode == IDLE:
        commands = {
            "payload_power": "OFF",
            "cooling_system": "LOW",
            "antenna_mode": "STANDBY"
        }

    elif mode == CRUISE:
        commands = {
            "payload_power": "ON",
            "cooling_system": "NORMAL",
            "antenna_mode": "TRACKING"
        }

    elif mode == WARMING:
        commands = {
            "payload_power": "ON",
            "cooling_system": "HIGH",
            "antenna_mode": "TRACKING"
        }

    elif mode == COMMS_RECOVERY:
        commands = {
            "payload_power": "OFF",
            "cooling_system": "NORMAL",
            "antenna_mode": "SIGNAL_SEARCH"
        }

    elif mode == SAFE:
        commands = {
            "payload_power": "OFF",
            "cooling_system": "MAX",
            "antenna_mode": "EMERGENCY_BEACON"
        }

    else:
        commands = {
            "payload_power": "OFF",
            "cooling_system": "LOW",
            "antenna_mode": "UNKNOWN"
        }

    return commands