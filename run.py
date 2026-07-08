from sensors import read_sensors
from flight_logic import check_faults, choose_mode
from telemetry import save_telemetry_csv
from plotting import plot_telemetry
from commands import generate_commands
from event_log import detect_events, save_event_log
from mission_profiles import (
    get_mission_profile,
    LOW_EARTH_ORBIT,
    GEOSTATIONARY_ORBIT,
    LUNAR_TRANSFER,
    DEEP_SPACE_CRUISE
)


SELECTED_MISSION = LUNAR_TRANSFER


def print_status(time_s, mode, sensors, fault):
    print(
        f"Time: {time_s:03d}s"
        f" | Mode: {mode}"
        f" | Battery: {sensors['battery_percent']:.1f}%"
        f" | Temperature: {sensors['temperature_c']:.1f}C"
        f" | Signal: {sensors['signal_strength_percent']:.1f}%"
        f" | Fault: {fault}"
    )


def print_commands(commands):
    print(
        f"Commands:"
        f" Payload={commands['payload_power']}"
        f" | Cooling={commands['cooling_system']}"
        f" | Antenna={commands['antenna_mode']}"
    )


def should_print_status(time_s, new_events):
    if time_s % 10 == 0:
        return True

    if len(new_events) > 0:
        return True

    return False


def create_telemetry_record(time_s, mission_profile, mode, sensors, fault, commands):
    telemetry_record = {
        "mission_name": mission_profile["name"],
        "time_s": time_s,
        "mode": mode,
        "battery_percent": sensors["battery_percent"],
        "temperature_c": sensors["temperature_c"],
        "signal_strength_percent": sensors["signal_strength_percent"],
        "fault": fault,
        "payload_power": commands["payload_power"],
        "cooling_system": commands["cooling_system"],
        "antenna_mode": commands["antenna_mode"]
    }
    return telemetry_record


def run_mission():
    print("Starting flight software simulation.")
    print("-" * 90)

    mission_profile = get_mission_profile(SELECTED_MISSION)

    print("Selected mission:", mission_profile["name"])
    print("-" * 90)

    telemetry_log = []
    mission_events = []
    previous_mode = None
    previous_fault = None

    for time_s in range(0, mission_profile["duration_s"]):
        sensors = read_sensors(time_s, mission_profile)
        fault = check_faults(sensors)
        mode = choose_mode(time_s, fault, sensors)
        commands = generate_commands(mode)

        new_events = detect_events(
            time_s,
            previous_mode,
            mode,
            previous_fault,
            fault
        )

        mission_events.extend(new_events)

        previous_mode = mode
        previous_fault = fault

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

    print("-" * 90)

    print("Mission events:")
    for event in mission_events:
        print(event)

    save_event_log(mission_events,mission_profile)
    save_telemetry_csv(telemetry_log, mission_profile)
    plot_telemetry(telemetry_log, mission_profile)

    print("Telemetry records saved:", len(telemetry_log))
    print("Saved mission_events.txt")
    print("Saved telemetry.csv")
    print("Saved telemetry_plot.png")
    print("Mission complete.")


if __name__ == "__main__":
    run_mission()