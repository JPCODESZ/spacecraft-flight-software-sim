import math


EARTH_RADIUS_KM = 6371.0
EARTH_MU_KM3_S2 = 398600.4418


def calculate_circular_orbit(altitude_km):
    orbital_radius_km = EARTH_RADIUS_KM + altitude_km

    orbital_velocity_km_s = math.sqrt(
        EARTH_MU_KM3_S2 / orbital_radius_km
    )

    orbital_period_s = 2 * math.pi * math.sqrt(
        orbital_radius_km**3 / EARTH_MU_KM3_S2
    )

    return {
        "trajectory_type": "circular_orbit",
        "altitude_km": altitude_km,
        "orbital_radius_km": orbital_radius_km,
        "orbital_velocity_km_s": orbital_velocity_km_s,
        "orbital_period_s": orbital_period_s,
        "orbital_period_min": orbital_period_s / 60,
        "orbital_period_hr": orbital_period_s / 3600,
        "model_note": "Circular Earth orbit model"
    }


def calculate_transfer_trajectory(target_distance_km):
    starting_radius_km = EARTH_RADIUS_KM + 400
    target_radius_km = EARTH_RADIUS_KM + target_distance_km
    average_radius_km = (starting_radius_km + target_radius_km) / 2

    estimated_cruise_velocity_km_s = math.sqrt(
        EARTH_MU_KM3_S2 / average_radius_km
    )

    estimated_travel_time_s = (
        target_distance_km / estimated_cruise_velocity_km_s
    )

    return {
        "trajectory_type": "transfer",
        "target_distance_km": target_distance_km,
        "starting_radius_km": starting_radius_km,
        "target_radius_km": target_radius_km,
        "average_radius_km": average_radius_km,
        "estimated_cruise_velocity_km_s": estimated_cruise_velocity_km_s,
        "estimated_travel_time_s": estimated_travel_time_s,
        "estimated_travel_time_hr": estimated_travel_time_s / 3600,
        "estimated_travel_time_days": estimated_travel_time_s / 86400,
        "model_note": (
            "Simplified transfer estimate, not full orbital propagation"
        )
    }


def calculate_mission_orbit(mission_profile):
    trajectory_type = mission_profile["trajectory_type"]

    if trajectory_type == "circular_orbit":
        return calculate_circular_orbit(
            mission_profile["altitude_km"]
        )

    if trajectory_type == "transfer":
        return calculate_transfer_trajectory(
            mission_profile["altitude_km"]
        )

    raise ValueError(
        f"Unknown trajectory type: {trajectory_type}"
    )