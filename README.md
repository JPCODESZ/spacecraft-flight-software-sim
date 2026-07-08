# Mini Flight Software Simulator

A beginner aerospace software project that simulates a simple spacecraft flight software loop.

## Project Goal

This project simulates how spacecraft software can:

1. Read sensor data
2. Detect faults
3. Switch spacecraft modes
4. Save telemetry
5. Generate a telemetry plot

## Spacecraft Modes

The simulator uses three spacecraft modes:

- `IDLE` — startup mode during the first few seconds
- `CRUISE` — normal operating mode
- `SAFE` — protective mode when a fault is detected

## Simulated Sensors

The simulator tracks:

- Battery percentage
- Temperature in Celsius

Battery decreases over time, while temperature increases over time.

## Fault Detection

The software detects two possible faults:

- `LOW_BATTERY` if battery drops below 20%
- `HIGH_TEMPERATURE` if temperature rises above 80°C

If a fault occurs, the spacecraft enters `SAFE` mode.

## Outputs

Running the program creates:

- `telemetry.csv` — mission telemetry data
- `telemetry_plot.png` — plot of battery and temperature over time

## How to Run

Install dependencies:

```bash
python -m pip install matplotlib