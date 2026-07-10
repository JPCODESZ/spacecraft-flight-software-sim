def detect_events(
    time_s,
    previous_mode,
    current_mode,
    previous_fault,
    current_fault
):
    events = []

    if previous_mode is not None and previous_mode != current_mode:
        events.append(
            f"{time_s:03d}s MODE_CHANGE: "
            f"{previous_mode} -> {current_mode}"
        )

    if previous_fault != current_fault:
        if current_fault is not None:
            events.append(
                f"{time_s:03d}s FAULT: {current_fault}"
            )

        elif previous_fault is not None:
            events.append(
                f"{time_s:03d}s FAULT_CLEARED: {previous_fault}"
            )

    return events


def save_event_log(mission_events, mission_profile):
    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    filename = f"mission_events_{mission_slug}.txt"

    with open(filename, "w") as file:
        file.write(f"Mission: {mission_profile['name']}\n")
        file.write("-" * 40 + "\n")

        for event in mission_events:
            file.write(event + "\n")