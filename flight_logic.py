IDLE = "IDLE"
CRUISE = "CRUISE"
WARMING = "WARMING"
COMMS_RECOVERY = "COMMS_RECOVERY"
SAFE = "SAFE"


def check_faults(sensors):
    """
    Check sensor data for unsafe spacecraft conditions.
    """

    if sensors["battery_percent"] < 20:
        return "LOW_BATTERY"

    if sensors["temperature_c"] > 80:
        return "HIGH_TEMPERATURE"

    if sensors["signal_strength_percent"] < 60:
        return "LOW_SIGNAL"

    return None


def choose_mode(time_s, fault, sensors):
    """
    Choose the spacecraft mode based on time, fault status, and sensor data.
    """

    if fault == "LOW_BATTERY":
        return SAFE

    if fault == "HIGH_TEMPERATURE":
        return SAFE

    if fault == "LOW_SIGNAL":
        return COMMS_RECOVERY

    if time_s < 5:
        return IDLE

    if sensors["temperature_c"] > 65:
        return WARMING

    return CRUISE