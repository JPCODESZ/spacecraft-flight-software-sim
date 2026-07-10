from sensors import read_sensors
from flight_logic import check_faults, choose_mode
from telemetry import save_telemetry_csv
from plotting import plot_telemetry
from commands import generate_commands
from event_log import detect_events, save_event_log
from orbit import calculate_mission_orbit
from spacecraft_state import (
    initialize_spacecraft_state,
    update_spacecraft_state
)
from mission_profiles import (
    get_mission_profile,
    LOW_EARTH_ORBIT,
    GEOSTATIONARY_ORBIT,
    LUNAR_TRANSFER,
    DEEP_SPACE_CRUISE
)


SELECTED_MISSION = LOW_EARTH_ORBIT


def get_mission_slug(mission_profile):
    return mission_profile["name"].lower().replace(" ", "_")


def print_status(time_s, mode, sensors, fault):
    print(
        f"Time: {time_s:03d}s"
        f" | Mode: {mode}"
        f" | Battery: {sensors['battery_percent']:.1f}%"
        f" | Temperature: {sensors['temperature_c']:.1f}C"
        f" | Signal: {sensors['signal_strength_percent']:.1f}%"
        f" | Data: {sensors['data_storage_mb']:.1f} MB"
        f" | Fault: {fault}"
    )


def print_commands(commands):
    print(
        "Commands:"
        f" Payload={commands['payload_power']}"
        f" | Cooling={commands['cooling_system']}"
        f" | Antenna={commands['antenna_mode']}"
    )


def print_trajectory_summary(orbit_data):
    print("Trajectory summary:")
    print(f"Trajectory type: {orbit_data['trajectory_type']}")

    if orbit_data["trajectory_type"] == "circular_orbit":
        print(f"Altitude: {orbit_data['altitude_km']:.1f} km")
        print(
            f"Orbital radius: "
            f"{orbit_data['orbital_radius_km']:.1f} km"
        )
        print(
            f"Orbital velocity: "
            f"{orbit_data['orbital_velocity_km_s']:.2f} km/s"
        )
        print(
            f"Orbital period: "
            f"{orbit_data['orbital_period_min']:.2f} minutes"
        )

    elif orbit_data["trajectory_type"] == "transfer":
        print(
            f"Target distance: "
            f"{orbit_data['target_distance_km']:.1f} km"
        )
        print(
            f"Estimated cruise velocity: "
            f"{orbit_data['estimated_cruise_velocity_km_s']:.2f} km/s"
        )
        print(
            f"Estimated travel time: "
            f"{orbit_data['estimated_travel_time_days']:.2f} days"
        )
        print(f"Model note: {orbit_data['model_note']}")

    print("-" * 90)


def should_print_status(time_s, new_events):
    return time_s % 10 == 0 or len(new_events) > 0


def create_telemetry_record(
    time_s,
    mission_profile,
    mode,
    sensors,
    fault,
    commands
):
    return {
        "mission_name": mission_profile["name"],
        "time_s": time_s,
        "mode": mode,
        "battery_percent": sensors["battery_percent"],
        "temperature_c": sensors["temperature_c"],
        "signal_strength_percent": sensors[
            "signal_strength_percent"
        ],
        "data_storage_mb": sensors["data_storage_mb"],
        "fault": fault,
        "payload_power": commands["payload_power"],
        "cooling_system": commands["cooling_system"],
        "antenna_mode": commands["antenna_mode"]
    }


def run_mission():
    print("Starting flight software simulation.")
    print("-" * 90)

    mission_profile = get_mission_profile(SELECTED_MISSION)
    trajectory_data = calculate_mission_orbit(mission_profile)
    mission_slug = get_mission_slug(mission_profile)

    print(f"Selected mission: {mission_profile['name']}")
    print_trajectory_summary(trajectory_data)

    spacecraft_state = initialize_spacecraft_state()

    telemetry_log = []
    mission_events = []

    previous_mode = None
    previous_fault = None

    for time_s in range(mission_profile["duration_s"]):
        sensors = read_sensors(spacecraft_state)

        fault = check_faults(sensors)
        mode = choose_mode(
    time_s,
    fault,
    sensors,
    previous_mode
)
        commands = generate_commands(mode)

        new_events = detect_events(
            time_s,
            previous_mode,
            mode,
            previous_fault,
            fault
        )

        mission_events.extend(new_events)

        telemetry_record = create_telemetry_record(
            time_s,
            mission_profile,
            mode,
            sensors,
            fault,
            commands
        )

        telemetry_log.append(telemetry_record)

        if should_print_status(time_s, new_events):
            print_status(time_s, mode, sensors, fault)
            print_commands(commands)

        spacecraft_state = update_spacecraft_state(
            spacecraft_state,
            mission_profile,
            commands
        )

        previous_mode = mode
        previous_fault = fault

    print("-" * 90)
    print("Mission events:")

    for event in mission_events:
        print(event)

    save_event_log(mission_events, mission_profile)
    save_telemetry_csv(telemetry_log, mission_profile)
    plot_telemetry(telemetry_log, mission_profile)

    print("-" * 90)
    print(f"Telemetry records saved: {len(telemetry_log)}")
    print(f"Saved mission_events_{mission_slug}.txt")
    print(f"Saved telemetry_{mission_slug}.csv")
    print(f"Saved telemetry_plot_{mission_slug}.png")
    print("Mission complete.")


if __name__ == "__main__":
    run_mission()