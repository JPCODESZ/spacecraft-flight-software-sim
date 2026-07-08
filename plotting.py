import matplotlib.pyplot as plt


def plot_telemetry(telemetry_log):
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
    plt.title("Spacecraft Telemetry Over Time")
    plt.legend()
    plt.grid(True)

    plt.savefig("telemetry_plot.png")
    plt.close()