"""
run_server.py — Start the IoT WebSocket Server
Usage: python run_server.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from iot_server.server import main
import asyncio

if __name__ == "__main__":
    print("=" * 55)
    print("  Smart Agriculture IoT WebSocket Server")
    print("=" * 55)
    print("  Server  : ws://localhost:8765")
    print("  Dashboard: open templates/dashboard.html in browser")
    print("  Logs    : iot_security.log")
    print("=" * 55)
    print("\n[SERVER] Starting... Press Ctrl+C to stop.\n")
    asyncio.run(main())
