# FinalCCNProject — MQTT Network Simulation (AnyLogic) + Animated Dashboard

A Computer Networks final project built in **AnyLogic 8.9.x** to simulate an **MQTT traffic pipeline** (arrival table → network latency → buffering → cloud sink), with a companion **animated dashboard** that visualizes the dataset and “packet flow” in a presentation-ready way.

## What’s inside

- **AnyLogic model**: `FinalCCNProject.alp`
- **Model database (HSQL)**: `database/` (contains the `MQTT_READY` table)
- **Animated dashboard (web)**: `dashboard/` (Canvas network animation + charts)
- **Data extraction tool**: `tools/extract_mqtt_ready.py` (exports `MQTT_READY` from `db.script` → JSON/CSV for the dashboard)

## Quick start

### 1) Open & run the AnyLogic model

1. Install **AnyLogic 8.9+**.
2. Open the project file: `FinalCCNProject.alp`
3. Run the **Simulation** experiment.

### 2) Generate dashboard data

From the repository root:

- `python tools/extract_mqtt_ready.py`

Windows (no Python required):

- `powershell -ExecutionPolicy Bypass -File tools/extract_mqtt_ready.ps1`

This reads `database/db.script` and writes:

- `dashboard/data/mqtt_ready.json`
- `dashboard/data/mqtt_ready.csv`

### 3) Launch the animated dashboard

Zero-setup (recommended for demos):

- Open `dashboard/index.html` directly.

If you prefer to serve it locally (e.g., for browser caching/devtools):

- `python -m http.server 8000`

Then open:

- `http://localhost:8000/dashboard/`

## Model overview

### Flow (Process Modeling)

```mermaid
flowchart LR
  A[Source\n(Database Arrival Table)] --> B[Delay\nNetwork Latency]
  B --> C[Queue\nMQTT Buffer]
  C --> D[Sink\nCloud Received]
```

### Entities / agents

- `MQTTPacket`: carries `packet_size`, `inter_arrival`, `flow_duration`
- `NetworkMetrics`: records and summarizes latency statistics

## Dashboard overview

The dashboard is designed for demos/presentations:

- **Canvas animation**: packets travel Sensor → Gateway → Cloud with smooth motion and glow
- **Charts**: latency time-series, histogram, and size-vs-latency scatter
- **Animated counters**: totals and key KPIs count up on load

## Notes for portability

- The AnyLogic model was cleaned to remove hard-coded local file paths (like `C:/Users/.../Downloads/...`).
- The project data is taken from the included `database/db.script`, so the project stays self-contained.

## Recommended demo script (for presentation)

1. Run the AnyLogic simulation and explain the flow blocks.
2. Show that the dataset comes from the built-in HSQL database table.
3. Open the dashboard and explain:
   - live-feel packet animation
   - real dataset charts
   - KPI counters (avg/min/max/std-dev latency)

## Tech

- AnyLogic 8.9.x (Process Modeling Library)
- HSQLDB (AnyLogic internal database)
- Dashboard: HTML/CSS/JS + Chart.js (CDN)

---

If you want, tell me what your teacher expects (network topology view vs. charts), and I can tune the dashboard visuals and terminology to match your report.
