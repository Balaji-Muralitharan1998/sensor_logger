import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh
import sqlite3


DB_FILE = "/data/sensor_data.db"
pause_flag = "/data/PAUSE"
stop_flag = "/data/STOP"

if "simulator_status" not in st.session_state:
    st.session_state.simulator_status = "running"

st.set_page_config(page_title="Sensor Dashboard" , layout="wide")

st.title("Real-time Sensor Dashboard")

st_autorefresh(interval=1000, key="sensor_data_dashboard")



with st.sidebar:

    st.markdown("<h3 style='text-align: center;'>💬 Simulator Control Panel</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
                background-color: lightblue;
                width: 130px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start"):
        if os.path.exists(stop_flag):
            os.remove(stop_flag)
        st.error("Simulation Stopped")
        st.session_state.simulator_status = "stopped"

    if st.button("⏸️ Pause"):
        with open(pause_flag, "w") as f:
            f.write("pause")
        st.info("Pausing Simulation....")
        st.session_state.simulator_status = "paused"
        

    if st.button("▶️ Resume"):
        if os.path.exists(pause_flag):
            os.remove(pause_flag)
        if os.path.exists(stop_flag):
            os.remove(stop_flag)
        st.success("Resuming Simulation...")
        st.session_state.simulator_status = "running"

    if st.button("🛑 Stop"):
        with open(stop_flag, "w") as f:
            f.write("stop")
        st.error("Simulation Stopped")
        st.session_state.simulator_status = "stopped"
    
with st.spinner("Loading Database....."):
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM sensor_data",conn)
        conn.close()
    except Exception as e:
        st.error(f"Database read error: {e}")
        st.stop()

if df.empty:
    st.warning("No sensor data found.")
    st.stop()

st.info(f"Simulator is {st.session_state.simulator_status}")

st.subheader("Latest Sensor Readings")

st.dataframe(df.tail(10), use_container_width=True)

device_ids = df["device_id"].unique().tolist()
selected_device = st.selectbox("Select Device ID", sorted(device_ids))
filtered = df[df["device_id"] == selected_device]

col1, col2 = st.columns(2)

with col1:
    st.line_chart(filtered.set_index("timestamp")[["temperature"]],x_label="Timestamp" , y_label= "Temperature (°C)")
with col2:
    st.line_chart(filtered.set_index("timestamp")[["pressure"]],x_label="Timestamp" , y_label= "Pressure (hPa)")
