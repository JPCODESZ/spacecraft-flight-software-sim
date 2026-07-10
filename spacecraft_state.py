def clamp(value, minimum, maximum):
    """Keep a value inside a specified range."""

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


def initialize_spacecraft_state():
    """Create the spacecraft's starting condition."""

    return {
        "battery_percent": 100.0,
        "temperature_c": 22.0,
        "signal_strength_percent": 100.0,
        "data_storage_mb": 0.0
    }


def calculate_battery_drain(mission_profile, commands):
    """Calculate battery use during one simulation step."""

    battery_drain = mission_profile["battery_drain_rate"]

    if commands["payload_power"] == "ON":
        battery_drain += 0.25

    if commands["cooling_system"] == "LOW":
        battery_drain += 0.03
    elif commands["cooling_system"] == "NORMAL":
        battery_drain += 0.07
    elif commands["cooling_system"] == "MAX":
        battery_drain += 0.18

    if commands["antenna_mode"] == "TRACKING":
        battery_drain += 0.08
    elif commands["antenna_mode"] == "SIGNAL_SEARCH":
        battery_drain += 0.12
    elif commands["antenna_mode"] == "EMERGENCY_BEACON":
        battery_drain += 0.20

    return battery_drain


def calculate_temperature_change(mission_profile, commands):
    """Calculate temperature change during one simulation step."""

    temperature_change = mission_profile["temperature_rise_rate"]

    if commands["payload_power"] == "ON":
        temperature_change += 0.25

    if commands["cooling_system"] == "LOW":
        temperature_change -= 0.05
    elif commands["cooling_system"] == "NORMAL":
        temperature_change -= 0.25
    elif commands["cooling_system"] == "MAX":
        temperature_change -= 0.75

    return temperature_change


def calculate_signal_change(mission_profile, commands):
    """Calculate communication signal change."""

    signal_loss = mission_profile["signal_loss_rate"]

    if commands["antenna_mode"] == "TRACKING":
        signal_loss *= 0.80
    elif commands["antenna_mode"] == "SIGNAL_SEARCH":
        signal_loss *= 0.50
    elif commands["antenna_mode"] == "EMERGENCY_BEACON":
        signal_loss *= 0.35

    return -signal_loss


def calculate_data_change(commands):
    """Calculate stored science-data change."""

    data_change_mb = 0.0

    if commands["payload_power"] == "ON":
        data_change_mb += 2.5

    if commands["antenna_mode"] == "TRACKING":
        data_change_mb -= 1.0
    elif commands["antenna_mode"] == "SIGNAL_SEARCH":
        data_change_mb -= 0.2
    elif commands["antenna_mode"] == "EMERGENCY_BEACON":
        data_change_mb -= 0.1

    return data_change_mb


def update_spacecraft_state(spacecraft_state, mission_profile, commands):
    """Apply commands and produce the spacecraft state for the next second."""

    battery_drain = calculate_battery_drain(mission_profile, commands)
    temperature_change = calculate_temperature_change(
        mission_profile,
        commands
    )
    signal_change = calculate_signal_change(mission_profile, commands)
    data_change = calculate_data_change(commands)

    return {
        "battery_percent": clamp(
            spacecraft_state["battery_percent"] - battery_drain,
            0.0,
            100.0
        ),
        "temperature_c": clamp(
            spacecraft_state["temperature_c"] + temperature_change,
            -100.0,
            150.0
        ),
        "signal_strength_percent": clamp(
            spacecraft_state["signal_strength_percent"] + signal_change,
            0.0,
            100.0
        ),
        "data_storage_mb": clamp(
            spacecraft_state["data_storage_mb"] + data_change,
            0.0,
            10000.0
        )
    }