import csv


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
                "signal_strength_percent",
                "fault",
                "payload_power",
                "cooling_system",
                "antenna_mode"
            ]
        )

        writer.writeheader()
        writer.writerows(telemetry_log)