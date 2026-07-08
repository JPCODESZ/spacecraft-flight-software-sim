def read_sensors(time_s):
    """
    Simulate spacecraft sensor readings at a given mission time.
    """

    battery_percent = 100 - 0.4 * time_s
    temperature_c = 22 + 0.8 * time_s
    signal_strength_percent = 100 - 0.6 * time_s

    sensors = {
        "battery_percent": battery_percent,
        "temperature_c": temperature_c,
        "signal_strength_percent": signal_strength_percent
    }

    return sensors