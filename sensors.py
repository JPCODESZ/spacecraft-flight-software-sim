def read_sensors(time_s, mission_profile):
    """
    Simulate spacecraft sensor readings at a given mission time.

    The mission_profile controls how fast battery, temperature,
    and signal strength change during the mission.
    """

    battery_percent = 100 - mission_profile["battery_drain_rate"] * time_s
    temperature_c = 22 + mission_profile["temperature_rise_rate"] * time_s
    signal_strength_percent = 100 - mission_profile["signal_loss_rate"] * time_s

    sensors = {
        "battery_percent": battery_percent,
        "temperature_c": temperature_c,
        "signal_strength_percent": signal_strength_percent
    }

    return sensors