
import time
import json
import random
import requests
from datetime import datetime
import os


print("🚀 Simulator script has started.")
PAUSE_FLAG = "/data/PAUSE"
STOP_FLAG = "/data/STOP"


SENSOR_IDS = ["sensor_001" , "sensor_002" , "sensor_003"]

def generate_sensor_data(device_id):
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(20.0, 100.0), 2),
        "pressure": round(random.uniform(900.0, 1100.0), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "device_id": device_id
    }

API_URL = "http://backend:8000/sensor-data"  # Update to your FastAPI endpoint


while True:
    print("🔁 Simulator loop running...")
    if os.path.isfile(STOP_FLAG):
        print("🛑 STOP signal received. Exiting simulator.")
        break
    
    if os.path.isfile(PAUSE_FLAG):
        print("⏸️  PAUSE signal received. Sleeping until resumed...")
        while os.path.exists(PAUSE_FLAG):
            time.sleep(2)
        print("▶️  Resume signal received. Continuing data transmission.")

    for sensor_id in SENSOR_IDS:
        
        data = generate_sensor_data(sensor_id)
        print("Sending:", json.dumps(data))
        
        try:
            response = requests.post(API_URL, json=data)
            print("Server response:", response.status_code)
        except Exception as e:
            print("Error sending data:", e)

    time.sleep(1)
