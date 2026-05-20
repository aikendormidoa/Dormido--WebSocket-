"""
Smart Agriculture IoT WebSocket Server
Part A: WebSocket Server component
Part B: Handles connection, data transmission, model analysis
Part D: Event-driven, persistent connections — no polling needed
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime
from .model import classify_plant_health

# Part D: Secure Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s — %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('iot_security.log'),
    ]
)
logger = logging.getLogger(__name__)

# Track all connected dashboard clients
connected_clients = set()


async def handle_sensor(websocket, path):
    """
    Part B Step 2-5:
    - Accepts WebSocket connection from sensor or dashboard
    - Processes incoming sensor data
    - Runs model inference
    - Broadcasts result to all dashboard clients
    """
    client_ip = websocket.remote_address[0]
    logger.info(f"New connection from {client_ip} on path '{path}'")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            try:
                # Part B Step 3: Receive raw sensor data (JSON)
                data = json.loads(message)
                logger.info(f"Received sensor data: {data}")

                temperature = data.get("temperature", 0)
                humidity = data.get("humidity", 0)
                crop_status_raw = data.get("crop_health_index", 0)

                # Part C Step 1-2: Run model inference on incoming data
                health_status = classify_plant_health(temperature, humidity, crop_status_raw)

                # Build enriched payload with timestamp + prediction
                payload = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "temperature": temperature,
                    "humidity": humidity,
                    "crop_health_index": crop_status_raw,
                    "health_status": health_status["label"],        # Healthy / Warning / Critical
                    "health_color": health_status["color"],         # green / yellow / red
                    "alert": health_status["alert"],                # alert message if abnormal
                    "recommendation": health_status["recommendation"],
                }

                # Part C Step 3: Log alert if abnormal
                if health_status["label"] in ["Warning", "Critical"]:
                    logger.warning(
                        f"ABNORMAL DATA DETECTED — Status: {health_status['label']} | "
                        f"Temp: {temperature}°C | Humidity: {humidity}% | IP: {client_ip}"
                    )

                # Part B Step 5: Broadcast to ALL connected dashboard clients
                if connected_clients:
                    message_out = json.dumps(payload)
                    await asyncio.gather(
                        *[client.send(message_out) for client in connected_clients],
                        return_exceptions=True
                    )
                    logger.info(f"Broadcasted to {len(connected_clients)} client(s)")

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from {client_ip}")
                await websocket.send(json.dumps({"error": "Invalid JSON format"}))

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed: {client_ip}")
    finally:
        connected_clients.discard(websocket)
        logger.info(f"Client removed. Active connections: {len(connected_clients)}")


async def main():
    logger.info("Starting Smart Agriculture IoT WebSocket Server on ws://localhost:8765")
    async with websockets.serve(handle_sensor, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
