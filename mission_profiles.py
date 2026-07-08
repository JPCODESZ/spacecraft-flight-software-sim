LOW_EARTH_ORBIT = "LOW_EARTH_ORBIT"
GEOSTATIONARY_ORBIT = "GEOSTATIONARY_ORBIT"
LUNAR_TRANSFER = "LUNAR_TRANSFER"
DEEP_SPACE_CRUISE = "DEEP_SPACE_CRUISE"


MISSION_PROFILES = {
    LOW_EARTH_ORBIT: {
        "name": "Low Earth Orbit",
        "duration_s": 121,
        "battery_drain_rate": 0.4,
        "temperature_rise_rate": 0.8,
        "signal_loss_rate": 0.6
    },

        GEOSTATIONARY_ORBIT: {
        "name": "Geostationary Orbit",
        "duration_s": 121,
        "battery_drain_rate": 0.3,
        "temperature_rise_rate": 0.5,
        "signal_loss_rate": 0.2
    },

       LUNAR_TRANSFER: {
        "name": "Lunar Transfer",
        "duration_s": 121,
        "battery_drain_rate": 0.5,
        "temperature_rise_rate": 0.6,
        "signal_loss_rate": 0.9
    },

    DEEP_SPACE_CRUISE: {
        "name": "Deep Space Cruise",
        "duration_s": 121,
        "battery_drain_rate": 0.6,
        "temperature_rise_rate": 0.4,
        "signal_loss_rate": 1.1
    }
}


def get_mission_profile(mission_type):
    """
    Return the settings for the selected mission type.
    """

    return MISSION_PROFILES[mission_type]