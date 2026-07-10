import matplotlib.pyplot as plt


def plot_telemetry(telemetry_log, mission_profile):
    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    filename = f"telemetry_plot_{mission_slug}.png"

    times = [record["time_s"] for record in telemetry_log]
    batteries = [record["battery_percent"] for record in telemetry_log]
    temperatures = [record["temperature_c"] for record in telemetry_log]
    signals = [record["signal_strength_percent"] for record in telemetry_log]
    data_storage = [record["data_storage_mb"] for record in telemetry_log]

    plt.figure(figsize=(11, 6))

    plt.plot(times, batteries, label="Battery (%)")
    plt.plot(times, temperatures, label="Temperature (C)")
    plt.plot(times, signals, label="Signal (%)")
    plt.plot(times, data_storage, label="Data Storage (MB)")

    plt.axhline(
        y=80,
        linestyle="--",
        label="High Temperature Limit"
    )

    plt.axhline(
        y=60,
        linestyle="--",
        label="Low Signal Limit"
    )

    plt.axhline(
        y=90,
        linestyle="--",
        label="Data Storage Limit"
    )

    plt.xlabel("Mission Time (seconds)")
    plt.ylabel("Telemetry Value")
    plt.title(f"Spacecraft Telemetry — {mission_profile['name']}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()