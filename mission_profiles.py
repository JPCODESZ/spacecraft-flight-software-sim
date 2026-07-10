LOW_EARTH_ORBIT = "Low Earth Orbit"
GEOSTATIONARY_ORBIT = "Geostationary Orbit"
LUNAR_TRANSFER = "Lunar Transfer"
DEEP_SPACE_CRUISE = "Deep Space Cruise"


MISSION_PROFILES = {
    LOW_EARTH_ORBIT: {
        "name": LOW_EARTH_ORBIT,
        "duration_s": 121,
        "battery_drain_rate": 0.40,
        "temperature_rise_rate": 0.80,
        "signal_loss_rate": 0.60,
        "altitude_km": 400,
        "trajectory_type": "circular_orbit"
    },

    GEOSTATIONARY_ORBIT: {
        "name": GEOSTATIONARY_ORBIT,
        "duration_s": 121,
        "battery_drain_rate": 0.30,
        "temperature_rise_rate": 0.50,
        "signal_loss_rate": 0.20,
        "altitude_km": 35786,
        "trajectory_type": "circular_orbit"
    },

    LUNAR_TRANSFER: {
        "name": LUNAR_TRANSFER,
        "duration_s": 121,
        "battery_drain_rate": 0.50,
        "temperature_rise_rate": 0.60,
        "signal_loss_rate": 0.90,
        "altitude_km": 384400,
        "trajectory_type": "transfer"
    },

    DEEP_SPACE_CRUISE: {
        "name": DEEP_SPACE_CRUISE,
        "duration_s": 121,
        "battery_drain_rate": 0.60,
        "temperature_rise_rate": 0.40,
        "signal_loss_rate": 1.10,
        "altitude_km": 1000000,
        "trajectory_type": "transfer"
    }
}


def get_mission_profile(mission_type):
    return MISSION_PROFILES[mission_type]