import csv


def save_telemetry_csv(telemetry_log, mission_profile):
    """
    Save telemetry records to a CSV file.
    """

    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    telemetry_filename = f"telemetry_{mission_slug}.csv"

    with open(telemetry_filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames = [
    "mission_name",
    "time_s",
    "mode",
    "battery_percent",
    "temperature_c",
    "signal_strength_percent",
    "fault",
    "payload_power",
    "cooling_system",
    "antenna_mode"
]
        )

        writer.writeheader()
        writer.writerows(telemetry_log)