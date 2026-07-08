import matplotlib.pyplot as plt


def plot_telemetry(telemetry_log, mission_profile):
    """
    Create a plot of spacecraft telemetry over time.
    """

    times = []
    batteries = []
    temperatures = []
    signal_strengths = []

    for record in telemetry_log:
        times.append(record["time_s"])
        batteries.append(record["battery_percent"])
        temperatures.append(record["temperature_c"])
        signal_strengths.append(record["signal_strength_percent"])

    plt.figure(figsize=(10, 5))

    plt.plot(times, batteries, label="Battery Percent")
    plt.plot(times, temperatures, label="Temperature C")
    plt.plot(times, signal_strengths, label="Signal Strength Percent")

    plt.axhline(80, linestyle="--", label="Temperature Fault Limit")
    plt.axhline(60, linestyle="--", label="Signal Fault Limit")

    plt.xlabel("Time (seconds)")
    plt.ylabel("Sensor Value")
    plt.title(f"Spacecraft Telemetry — {mission_profile['name']}")
    plt.legend()
    plt.grid(True)

    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    plot_filename = f"telemetry_plot_{mission_slug}.png"
    plt.savefig(plot_filename)
    plt.close()