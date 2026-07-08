def detect_events(time_s, previous_mode, current_mode, previous_fault, current_fault):
    """
    Detect important mission events.
    """

    events = []

    if previous_mode is not None and current_mode != previous_mode:
        events.append(
            f"{time_s:03d}s MODE_CHANGE: {previous_mode} -> {current_mode}"
        )

    if current_fault is not None and current_fault != previous_fault:
        events.append(
            f"{time_s:03d}s FAULT: {current_fault}"
        )

    return events


def save_event_log(mission_events, mission_profile):
    mission_slug = mission_profile["name"].lower().replace(" ", "_")
    event_filename = f"mission_events_{mission_slug}.txt"

    with open(event_filename, "w") as file:
        file.write(f"Mission: {mission_profile['name']}\n")
        file.write("-" * 40 + "\n")

        for event in mission_events:
            file.write(event + "\n")