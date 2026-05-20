# Smart Agriculture IoT WebSocket System
### Activity: Designing a Real-Time IoT Monitoring System Using WebSocket

---

## Project Structure

```
iot_websocket_system/
├── run_server.py                  ← Start WebSocket server here
├── requirements.txt
├── README.md
├── iot_security.log               ← Auto-generated security log
├── iot_server/
│   ├── server.py                  ← Part A/B: WebSocket server
│   └── model.py                   ← Part C: Plant health AI model
├── sensor_simulator/
│   └── simulator.py               ← Part B Step 1: Sensor simulator
└── templates/
    └── dashboard.html             ← Part B Step 5: Live web dashboard
```

---

## Quick Start (3 Terminals)

### Terminal 1 — Install & Start Server
```bash
pip install -r requirements.txt
python run_server.py
```

### Terminal 2 — Open Dashboard
Just open `templates/dashboard.html` in your browser (double-click or drag to browser).

### Terminal 3 — Run Sensor Simulator
```bash
# Normal scenario (healthy crops)
python sensor_simulator/simulator.py normal 15

# Drought scenario (Warning status)
python sensor_simulator/simulator.py drought 10

# Heatwave scenario (Critical status)
python sensor_simulator/simulator.py heatwave 10

# Disease scenario (Critical crop health)
python sensor_simulator/simulator.py disease 10
```

---

## System Architecture (Part A)

```
[IoT Sensor / Drone]
        |
        | WebSocket (ws://localhost:8765)
        ↓
[WebSocket Server — server.py]
        |
        ├─→ [AI Model — model.py]
        |       Classifies: Healthy / Warning / Critical
        |
        | WebSocket broadcast
        ↓
[Web Dashboard — dashboard.html]
        Real-time charts, status, alerts
```

---

## Data Flow (Part B)

1. **Sensor generates** temperature, humidity, crop_health_index readings
2. **WebSocket connection** established between sensor and server (persistent)
3. **Data transmitted** as JSON every 2 seconds
4. **Model inference** runs on server — classifies plant health
5. **Dashboard updated** in real time via WebSocket broadcast

---

## Model Classification (Part C)

| Status   | Temperature | Humidity | Crop Index | Color  |
|----------|-------------|----------|------------|--------|
| Healthy  | 15–35°C     | 40–85%   | 60–100     | 🟢 Green |
| Warning  | 10–15 or 35–40°C | 20–40% | 30–60 | 🟡 Yellow |
| Critical | <10 or >40°C | <20 or >95% | <30  | 🔴 Red   |

---

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Smart Agriculture IoT WebSocket System"
git remote add origin https://github.com/YOUR_USERNAME/iot-websocket-system.git
git branch -M main
git push -u origin main
```
