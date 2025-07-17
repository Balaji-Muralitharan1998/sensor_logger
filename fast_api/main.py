
from fastapi import FastAPI,Request
import csv
import os
from contextlib import asynccontextmanager
import sqlite3


sensor_log : list[dict] = []

db_file = "sensor_data.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting...")
    await on_startup()
    yield
    print("Server is shutting down...")


async def on_startup ():

    if os.path.exists(db_file):
        os.remove(db_file)
        print("Old database file deleted")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            pressure REAL,
            vibration REAL,
            device_id TEXT
        )
    ''')
    conn.commit()
    conn.close()


app = FastAPI(lifespan=lifespan)

@app.post("/sensor-data")
async def receive_sensor_data (request:Request):
    data = await request.json()
    sensor_log.append(data)
    print("Received:" , data)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (timestamp, temperature, pressure, vibration, device_id)
        VALUES (?, ?, ?, ?, ?)
    ''',(data["timestamp"],
        data["temperature"],
        data["pressure"],
        data["vibration"],
        data["device_id"],
        )
    )
    conn.commit()
    conn.close()
    return {"status": "ok" , "totalrecords" : len(sensor_log)}

@app.get("/sensor-data")
async def get_sensor_data():
    return {"sensor_readings": sensor_log}

