def generate_commands(mode):
    if mode == "IDLE":
        return {
            "payload_power": "OFF",
            "cooling_system": "LOW",
            "antenna_mode": "STANDBY"
        }

    if mode == "CRUISE":
        return {
            "payload_power": "ON",
            "cooling_system": "NORMAL",
            "antenna_mode": "TRACKING"
        }

    if mode == "DOWNLINK":
        return {
            "payload_power": "OFF",
            "cooling_system": "NORMAL",
            "antenna_mode": "TRACKING"
        }

    if mode == "COMMS_RECOVERY":
        return {
            "payload_power": "OFF",
            "cooling_system": "NORMAL",
            "antenna_mode": "SIGNAL_SEARCH"
        }

    if mode == "SAFE":
        return {
            "payload_power": "OFF",
            "cooling_system": "MAX",
            "antenna_mode": "EMERGENCY_BEACON"
        }

    return {
        "payload_power": "OFF",
        "cooling_system": "LOW",
        "antenna_mode": "STANDBY"
    }