"""
Part B Step 1: Sensor Data Generation Simulator
Simulates an IoT drone/sensor sending data every 2 seconds via WebSocket.
Run this in a separate terminal AFTER starting the server.

Usage: python sensor_simulator/simulator.py
"""

import asyncio
import websockets
import json
import random
import time

WEBSOCKET_SERVER = "ws://localhost:8765"


def generate_sensor_reading(scenario="normal"):
    """
    Simulates IoT sensor readings.
    Scenarios: normal | drought | heatwave | disease
    """
    if scenario == "normal":
        return {
            "sensor_id": "DRONE-AG-001",
            "location": "Field Zone A",
            "temperature": round(random.uniform(22, 28), 2),
            "humidity": round(random.uniform(55, 75), 2),
            "crop_health_index": round(random.uniform(70, 95), 2),
        }
    elif scenario == "drought":
        return {
            "sensor_id": "DRONE-AG-001",
            "location": "Field Zone B",
            "temperature": round(random.uniform(33, 38), 2),
            "humidity": round(random.uniform(15, 30), 2),
            "crop_health_index": round(random.uniform(35, 55), 2),
        }
    elif scenario == "heatwave":
        return {
            "sensor_id": "DRONE-AG-001",
            "location": "Field Zone C",
            "temperature": round(random.uniform(41, 47), 2),
            "humidity": round(random.uniform(20, 40), 2),
            "crop_health_index": round(random.uniform(20, 40), 2),
        }
    elif scenario == "disease":
        return {
            "sensor_id": "DRONE-AG-001",
            "location": "Field Zone D",
            "temperature": round(random.uniform(24, 29), 2),
            "humidity": round(random.uniform(60, 70), 2),
            "crop_health_index": round(random.uniform(10, 28), 2),
        }


async def simulate_sensor(scenario="normal", readings=10):
    """
    Part B Step 2: Establish WebSocket connection then send data.
    """
    print(f"\n[SENSOR] Connecting to WebSocket server at {WEBSOCKET_SERVER}...")
    try:
        async with websockets.connect(WEBSOCKET_SERVER) as ws:
            print(f"[SENSOR] Connected! Sending {readings} readings (scenario: {scenario})\n")
            for i in range(readings):
                data = generate_sensor_reading(scenario)
                await ws.send(json.dumps(data))
                print(f"[SENSOR] Sent reading #{i+1}: {data}")
                await asyncio.sleep(2)  # Send every 2 seconds
            print("\n[SENSOR] All readings sent. Closing connection.")
    except ConnectionRefusedError:
        print("[ERROR] Could not connect. Make sure the server is running first!")
        print("  Run: python run_server.py")


if __name__ == "__main__":
    import sys
    scenario = sys.argv[1] if len(sys.argv) > 1 else "normal"
    readings = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print("=" * 55)
    print("  Smart Agriculture IoT Sensor Simulator")
    print("=" * 55)
    print(f"  Scenario : {scenario}")
    print(f"  Readings : {readings}")
    print(f"  Interval : 2 seconds")
    print("=" * 55)

    asyncio.run(simulate_sensor(scenario, readings))
