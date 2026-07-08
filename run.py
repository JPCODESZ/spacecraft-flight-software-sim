import csv
import matplotlib.pyplot as plt

"""
Mini Flight Software V1

Goal:
Simulate a simple spacecraft flight software loop.

The software:
1. Reads simulated spacecraft sensor data.
2. Checks for faults.
3. Chooses the correct spacecraft mode.
4. Saves mission telemetry to a CSV file.
5. Creates a telemetry plot.
"""

IDLE = "IDLE"
CRUISE = "CRUISE"
SAFE = "SAFE"


def read_sensors(time_s):
    """
    Simulate spacecraft sensor readings at a given mission time.
    """

    battery_percent = 100 - 0.4 * time_s
    temperature_c = 22 + 0.8 * time_s

    sensors = {
        "battery_percent": battery_percent,
        "temperature_c": temperature_c
    }

    return sensors


def check_faults(sensors):
    """
    Check sensor data for unsafe spacecraft conditions.
    """

    if sensors["battery_percent"] < 20:
        return "LOW_BATTERY"

    if sensors["temperature_c"] > 80:
        return "HIGH_TEMPERATURE"

    return None


def choose_mode(time_s, fault):
    """
    Choose the spacecraft mode based on time and fault status.
    """

    if fault is not None:
        return SAFE

    if time_s < 5:
        return IDLE

    return CRUISE


def print_status(time_s, mode, sensors, fault):
    """
    Print one line of spacecraft status.
    """

    print(
        f"Time: {time_s:03d}s"
        f" | Mode: {mode}"
        f" | Battery: {sensors['battery_percent']:.1f}%"
        f" | Temperature: {sensors['temperature_c']:.1f}C"
        f" | Fault: {fault}"
    )


def save_telemetry_csv(telemetry_log):
    """
    Save telemetry records to a CSV file.
    """

    with open("telemetry.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "time_s",
                "mode",
                "battery_percent",
                "temperature_c",
                "fault"
            ]
        )

        writer.writeheader()
        writer.writerows(telemetry_log)


def plot_telemetry(telemetry_log):
    """
    Create a plot of battery and temperature over time.
    """

    times = []
    batteries = []
    temperatures = []

    for record in telemetry_log:
        times.append(record["time_s"])
        batteries.append(record["battery_percent"])
        temperatures.append(record["temperature_c"])

    plt.figure(figsize=(10, 5))

    plt.plot(times, batteries, label="Battery Percent")
    plt.plot(times, temperatures, label="Temperature C")
    plt.axhline(80, linestyle="--", label="Temperature Fault Limit")

    plt.xlabel("Time (seconds)")
    plt.ylabel("Sensor Value")
    plt.title("Spacecraft Telemetry Over Time")
    plt.legend()
    plt.grid(True)

    plt.savefig("telemetry_plot.png")
    plt.close()


def run_mission():
    """
    Run the full spacecraft flight software simulation.
    """

    print("Starting flight software simulation.")
    print("-" * 70)

    telemetry_log = []

    for time_s in range(0, 121):
        sensors = read_sensors(time_s)
        fault = check_faults(sensors)
        mode = choose_mode(time_s, fault)

        telemetry_record = {
            "time_s": time_s,
            "mode": mode,
            "battery_percent": sensors["battery_percent"],
            "temperature_c": sensors["temperature_c"],
            "fault": fault
        }

        telemetry_log.append(telemetry_record)

        print_status(time_s, mode, sensors, fault)

    print("-" * 70)

    save_telemetry_csv(telemetry_log)
    plot_telemetry(telemetry_log)

    print("Telemetry records saved:", len(telemetry_log))
    print("Saved telemetry.csv")
    print("Saved telemetry_plot.png")
    print("Mission complete.")


if __name__ == "__main__":
    run_mission()