import csv


def save_telemetry_csv(telemetry_log, mission_profile):
    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    filename = f"telemetry_{mission_slug}.csv"

    fieldnames = [
        "mission_name",
        "time_s",
        "mode",
        "battery_percent",
        "temperature_c",
        "signal_strength_percent",
        "data_storage_mb",
        "fault",
        "payload_power",
        "cooling_system",
        "antenna_mode"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(telemetry_log)