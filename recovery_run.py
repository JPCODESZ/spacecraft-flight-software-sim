import csv
import math
from pathlib import Path


# -----------------------------
# Mission and mode definitions
# -----------------------------
IDLE = "IDLE"
CRUISE = "CRUISE"
DOWNLINK = "DOWNLINK"
COMMS_RECOVERY = "COMMS_RECOVERY"
SAFE = "SAFE"

LOW_EARTH_ORBIT = "Low Earth Orbit"
GEOSTATIONARY_ORBIT = "Geostationary Orbit"
LUNAR_TRANSFER = "Lunar Transfer"
DEEP_SPACE_CRUISE = "Deep Space Cruise"

SELECTED_MISSION = LOW_EARTH_ORBIT

EARTH_RADIUS_KM = 6371.0
EARTH_MU_KM3_S2 = 398600.4418

MISSION_PROFILES = {
    LOW_EARTH_ORBIT: {
        "name": LOW_EARTH_ORBIT,
        "duration_s": 121,
        "trajectory_type": "circular_orbit",
        "altitude_km": 400.0,
        "battery_drain_rate": 0.18,
        "temperature_rise_rate": 0.10,
        "signal_loss_rate": 0.08,
    },
    GEOSTATIONARY_ORBIT: {
        "name": GEOSTATIONARY_ORBIT,
        "duration_s": 121,
        "trajectory_type": "circular_orbit",
        "altitude_km": 35786.0,
        "battery_drain_rate": 0.22,
        "temperature_rise_rate": 0.08,
        "signal_loss_rate": 0.12,
    },
    LUNAR_TRANSFER: {
        "name": LUNAR_TRANSFER,
        "duration_s": 121,
        "trajectory_type": "transfer",
        "altitude_km": 384400.0,
        "battery_drain_rate": 0.28,
        "temperature_rise_rate": 0.12,
        "signal_loss_rate": 0.35,
    },
    DEEP_SPACE_CRUISE: {
        "name": DEEP_SPACE_CRUISE,
        "duration_s": 121,
        "trajectory_type": "transfer",
        "altitude_km": 1000000.0,
        "battery_drain_rate": 0.32,
        "temperature_rise_rate": 0.06,
        "signal_loss_rate": 0.55,
    },
}


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def mission_slug(mission_profile):
    return mission_profile["name"].lower().replace(" ", "_")


# -----------------------------
# Trajectory models
# -----------------------------
def calculate_circular_orbit(altitude_km):
    radius_km = EARTH_RADIUS_KM + altitude_km
    velocity_km_s = math.sqrt(EARTH_MU_KM3_S2 / radius_km)
    period_s = 2.0 * math.pi * math.sqrt(radius_km**3 / EARTH_MU_KM3_S2)

    return {
        "trajectory_type": "circular_orbit",
        "altitude_km": altitude_km,
        "orbital_radius_km": radius_km,
        "orbital_velocity_km_s": velocity_km_s,
        "orbital_period_min": period_s / 60.0,
    }


def calculate_transfer_trajectory(target_distance_km):
    start_radius_km = EARTH_RADIUS_KM + 400.0
    target_radius_km = EARTH_RADIUS_KM + target_distance_km
    semi_major_axis_km = (start_radius_km + target_radius_km) / 2.0

    transfer_period_s = 2.0 * math.pi * math.sqrt(
        semi_major_axis_km**3 / EARTH_MU_KM3_S2
    )
    transfer_time_s = transfer_period_s / 2.0

    return {
        "trajectory_type": "transfer",
        "target_distance_km": target_distance_km,
        "semi_major_axis_km": semi_major_axis_km,
        "estimated_transfer_time_days": transfer_time_s / 86400.0,
        "model_note": "Simplified two-body Hohmann-style transfer estimate",
    }


def calculate_trajectory(mission_profile):
    if mission_profile["trajectory_type"] == "circular_orbit":
        return calculate_circular_orbit(mission_profile["altitude_km"])

    if mission_profile["trajectory_type"] == "transfer":
        return calculate_transfer_trajectory(mission_profile["altitude_km"])

    raise ValueError(
        f"Unknown trajectory type: {mission_profile['trajectory_type']}"
    )


# -----------------------------
# Spacecraft state and sensors
# -----------------------------
def initialize_spacecraft_state():
    return {
        "battery_percent": 100.0,
        "temperature_c": 22.0,
        "signal_strength_percent": 100.0,
        "data_storage_mb": 0.0,
    }


def read_sensors(spacecraft_state):
    return dict(spacecraft_state)


def check_faults(sensors):
    if sensors["battery_percent"] < 20.0:
        return "LOW_BATTERY"

    if sensors["temperature_c"] > 80.0:
        return "HIGH_TEMPERATURE"

    if sensors["signal_strength_percent"] < 25.0:
        return "LOW_SIGNAL"

    if sensors["data_storage_mb"] >= 90.0:
        return "DATA_STORAGE_HIGH"

    return None


def choose_mode(time_s, sensors, current_mode, fault):
    if fault in {"LOW_BATTERY", "HIGH_TEMPERATURE"}:
        return SAFE

    if fault == "LOW_SIGNAL":
        return COMMS_RECOVERY

    # Hysteresis: once downlink starts, continue until storage is mostly cleared.
    if current_mode == DOWNLINK and sensors["data_storage_mb"] > 30.0:
        return DOWNLINK

    if fault == "DATA_STORAGE_HIGH":
        return DOWNLINK

    if time_s < 5:
        return IDLE

    return CRUISE


def generate_commands(mode):
    command_table = {
        IDLE: {
            "payload_power": "OFF",
            "cooling_system": "LOW",
            "antenna_mode": "STANDBY",
        },
        CRUISE: {
            "payload_power": "ON",
            "cooling_system": "NORMAL",
            "antenna_mode": "TRACKING",
        },
        DOWNLINK: {
            "payload_power": "OFF",
            "cooling_system": "NORMAL",
            "antenna_mode": "DOWNLINK",
        },
        COMMS_RECOVERY: {
            "payload_power": "OFF",
            "cooling_system": "NORMAL",
            "antenna_mode": "SIGNAL_SEARCH",
        },
        SAFE: {
            "payload_power": "OFF",
            "cooling_system": "MAX",
            "antenna_mode": "EMERGENCY_BEACON",
        },
    }

    return command_table[mode]


def update_spacecraft_state(state, mission_profile, commands):
    battery_drain = mission_profile["battery_drain_rate"]
    temperature_change = mission_profile["temperature_rise_rate"]
    signal_change = -mission_profile["signal_loss_rate"]
    data_change = 0.0

    if commands["payload_power"] == "ON":
        battery_drain += 0.20
        temperature_change += 0.20
        data_change += 2.5

    cooling_effects = {
        "LOW": (-0.03, 0.02),
        "NORMAL": (-0.18, 0.05),
        "MAX": (-0.80, 0.18),
    }
    cooling_temperature, cooling_power = cooling_effects[
        commands["cooling_system"]
    ]
    temperature_change += cooling_temperature
    battery_drain += cooling_power

    antenna_mode = commands["antenna_mode"]

    if antenna_mode == "TRACKING":
        battery_drain += 0.05
        signal_change *= 0.60
        data_change -= 0.70
    elif antenna_mode == "DOWNLINK":
        battery_drain += 0.12
        signal_change *= 0.45
        data_change -= 4.0
    elif antenna_mode == "SIGNAL_SEARCH":
        battery_drain += 0.15
        signal_change = 0.80
        data_change -= 0.10
    elif antenna_mode == "EMERGENCY_BEACON":
        battery_drain += 0.18
        signal_change = 0.25

    return {
        "battery_percent": clamp(
            state["battery_percent"] - battery_drain,
            0.0,
            100.0,
        ),
        "temperature_c": clamp(
            state["temperature_c"] + temperature_change,
            -100.0,
            150.0,
        ),
        "signal_strength_percent": clamp(
            state["signal_strength_percent"] + signal_change,
            0.0,
            100.0,
        ),
        "data_storage_mb": clamp(
            state["data_storage_mb"] + data_change,
            0.0,
            10000.0,
        ),
    }


# -----------------------------
# Events, telemetry, and plots
# -----------------------------
def detect_events(time_s, previous_mode, mode, previous_fault, fault):
    events = []

    if previous_mode is not None and mode != previous_mode:
        events.append(
            f"{time_s:03d}s MODE_CHANGE: {previous_mode} -> {mode}"
        )

    if fault is not None and fault != previous_fault:
        events.append(f"{time_s:03d}s FAULT: {fault}")

    if previous_fault is not None and fault is None:
        events.append(f"{time_s:03d}s FAULT_CLEARED: {previous_fault}")

    return events


def make_telemetry_record(time_s, mission_profile, mode, sensors, fault, commands):
    return {
        "mission_name": mission_profile["name"],
        "time_s": time_s,
        "mode": mode,
        "battery_percent": round(sensors["battery_percent"], 3),
        "temperature_c": round(sensors["temperature_c"], 3),
        "signal_strength_percent": round(
            sensors["signal_strength_percent"], 3
        ),
        "data_storage_mb": round(sensors["data_storage_mb"], 3),
        "fault": fault,
        "payload_power": commands["payload_power"],
        "cooling_system": commands["cooling_system"],
        "antenna_mode": commands["antenna_mode"],
    }


def save_outputs(telemetry_log, mission_events, mission_profile):
    slug = mission_slug(mission_profile)
    csv_path = Path(f"recovery_telemetry_{slug}.csv")
    event_path = Path(f"recovery_events_{slug}.txt")
    plot_path = Path(f"recovery_plot_{slug}.png")

    fieldnames = list(telemetry_log[0].keys())
    with csv_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(telemetry_log)

    with event_path.open("w") as file:
        file.write(f"Mission: {mission_profile['name']}\n")
        file.write("-" * 60 + "\n")
        for event in mission_events:
            file.write(event + "\n")

    try:
        import matplotlib.pyplot as plt

        times = [record["time_s"] for record in telemetry_log]
        batteries = [record["battery_percent"] for record in telemetry_log]
        temperatures = [record["temperature_c"] for record in telemetry_log]
        signals = [record["signal_strength_percent"] for record in telemetry_log]
        storage = [record["data_storage_mb"] for record in telemetry_log]

        plt.figure(figsize=(11, 6))
        plt.plot(times, batteries, label="Battery (%)")
        plt.plot(times, temperatures, label="Temperature (C)")
        plt.plot(times, signals, label="Signal (%)")
        plt.plot(times, storage, label="Data storage (MB)")
        plt.xlabel("Mission time (s)")
        plt.ylabel("Value")
        plt.title(f"Stateful Spacecraft Simulation — {mission_profile['name']}")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
    except ImportError:
        plot_path = None
        print("Plot skipped: matplotlib is not installed.")

    return csv_path, event_path, plot_path


# -----------------------------
# Console reporting
# -----------------------------
def print_trajectory_summary(trajectory):
    print("Trajectory summary:")
    print(f"Trajectory type: {trajectory['trajectory_type']}")

    if trajectory["trajectory_type"] == "circular_orbit":
        print(f"Altitude: {trajectory['altitude_km']:.1f} km")
        print(f"Orbital radius: {trajectory['orbital_radius_km']:.1f} km")
        print(
            f"Orbital velocity: "
            f"{trajectory['orbital_velocity_km_s']:.2f} km/s"
        )
        print(
            f"Orbital period: "
            f"{trajectory['orbital_period_min']:.2f} minutes"
        )
    else:
        print(f"Target distance: {trajectory['target_distance_km']:.1f} km")
        print(
            f"Estimated transfer time: "
            f"{trajectory['estimated_transfer_time_days']:.2f} days"
        )
        print(f"Model note: {trajectory['model_note']}")

    print("-" * 100)


def print_status(time_s, mode, sensors, fault, commands):
    print(
        f"Time: {time_s:03d}s"
        f" | Mode: {mode}"
        f" | Battery: {sensors['battery_percent']:.1f}%"
        f" | Temp: {sensors['temperature_c']:.1f}C"
        f" | Signal: {sensors['signal_strength_percent']:.1f}%"
        f" | Data: {sensors['data_storage_mb']:.1f} MB"
        f" | Fault: {fault}"
    )
    print(
        "Commands:"
        f" Payload={commands['payload_power']}"
        f" | Cooling={commands['cooling_system']}"
        f" | Antenna={commands['antenna_mode']}"
    )


# -----------------------------
# Main mission loop
# -----------------------------
def run_mission():
    mission_profile = MISSION_PROFILES[SELECTED_MISSION]
    trajectory = calculate_trajectory(mission_profile)

    print("Starting stateful flight software simulation.")
    print("=" * 100)
    print(f"Selected mission: {mission_profile['name']}")
    print_trajectory_summary(trajectory)

    state = initialize_spacecraft_state()
    current_mode = IDLE
    previous_mode = None
    previous_fault = None
    telemetry_log = []
    mission_events = []

    for time_s in range(mission_profile["duration_s"]):
        sensors = read_sensors(state)
        fault = check_faults(sensors)
        mode = choose_mode(time_s, sensors, current_mode, fault)
        commands = generate_commands(mode)

        new_events = detect_events(
            time_s,
            previous_mode,
            mode,
            previous_fault,
            fault,
        )
        mission_events.extend(new_events)

        telemetry_log.append(
            make_telemetry_record(
                time_s,
                mission_profile,
                mode,
                sensors,
                fault,
                commands,
            )
        )

        if time_s % 10 == 0 or new_events:
            print_status(time_s, mode, sensors, fault, commands)

        previous_mode = mode
        previous_fault = fault
        current_mode = mode
        state = update_spacecraft_state(state, mission_profile, commands)

    print("-" * 100)
    print("Mission events:")
    for event in mission_events:
        print(event)

    csv_path, event_path, plot_path = save_outputs(
        telemetry_log,
        mission_events,
        mission_profile,
    )

    print("-" * 100)
    print(f"Telemetry records saved: {len(telemetry_log)}")
    print(f"Saved {csv_path}")
    print(f"Saved {event_path}")
    if plot_path is not None:
        print(f"Saved {plot_path}")
    print("Mission complete.")


if __name__ == "__main__":
    run_mission()
