IDLE = "IDLE"
CRUISE = "CRUISE"
COMMS_RECOVERY = "COMMS_RECOVERY"
DOWNLINK = "DOWNLINK"
SAFE = "SAFE"


def check_faults(sensors):
    if sensors["battery_percent"] < 20:
        return "LOW_BATTERY"

    if sensors["temperature_c"] > 80:
        return "HIGH_TEMPERATURE"

    if sensors["signal_strength_percent"] < 60:
        return "LOW_SIGNAL"

    if sensors["data_storage_mb"] > 90:
        return "DATA_STORAGE_HIGH"

    return None


def choose_mode(time_s, fault, sensors, previous_mode):
    # Critical faults always override other modes.
    if fault in ("LOW_BATTERY", "HIGH_TEMPERATURE"):
        return SAFE

    if fault == "LOW_SIGNAL":
        return COMMS_RECOVERY

    # Once downlink begins, remain there until storage falls below 30 MB.
    if previous_mode == DOWNLINK:
        if sensors["data_storage_mb"] > 30:
            return DOWNLINK

    # Start downlink when storage exceeds 90 MB.
    if sensors["data_storage_mb"] > 90:
        return DOWNLINK

    if time_s < 5:
        return IDLE

    return CRUISE