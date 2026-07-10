def read_sensors(spacecraft_state):
    """
    Read the current spacecraft state as sensor data.
    """

    return {
        "battery_percent": spacecraft_state["battery_percent"],
        "temperature_c": spacecraft_state["temperature_c"],
        "signal_strength_percent": spacecraft_state["signal_strength_percent"],
        "data_storage_mb": spacecraft_state["data_storage_mb"]
    }