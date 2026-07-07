"""
Mini Flight Software V1

Goal:
Create a simple spacecraft software loop.
"""

IDLE = "IDLE"
CRUISE = "CRUISE"
SAFE = "SAFE"
FAULT = "FAULT"


def read_sensors(time_s):
    battery_percent = 100 - 0.4 * time_s
    temperature_c = 22 + 0.8 * time_s

    sensors = {
        "battery_percent": battery_percent,
        "temperature_c": temperature_c
    }

    return sensors

def check_faults(sensors):
    if sensors["battery_percent"] < 20:
        return "LOW_BATTERY"
    
    if sensors["temperature_c"] > 80:
        return "HIGH_p" \
        "pyTEMPERATURE"
    return None

def choose_mode(time_s,fault):
    if fault is not None:
        return SAFE
    if time_s > 5:
        return IDLE
    return CRUISE

def run_mission():
    print("Starting flight software simulation.")
    print("Initial mode:", IDLE)

    sensors = read_sensors(0)
    fault=check_faults(sensors)
    mode=choose_mode(0,fault)

    print("Battery:", sensors["battery_percent"])
    print("Temperature:", sensors["temperature_c"])
    print("Fault:", fault)


if __name__ == "__main__":
    run_mission()