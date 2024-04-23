import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
import plotly.express as px

from FactorySimulation import Factory

# Car assembly factory
class Debug(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4

class WrkStationStatus(Enum):
    START = 1
    IDLE = 2
    PRODUCING = 3
    RESTOCK = 4
    DOWN = 5
    STOP = 6

class ProductStatus(Enum):
    ORDERED = 1
    PRODUCING = 2
    DONE = 3
    FAIL = 4
    ABORT = 5
    INCOMPLETE = 6

class FactoryStatus(Enum):
    OPEN = 1
    CLOSED = 2
    SHUTDOWN = 3

# Custom exception classes
class Product:
    def __init__(self, id, env):
        self._status = ProductStatus.ORDERED
        self._id = id
        self._env = env
        self._currentStation = -1
        self._wrkStat = [False] * 6  # WRK_STATIONS = 6
        self._wrkStatTime = [0] * 6
        self._startClock = 0
        self._endClock = 0
        self._status = ProductStatus.ORDERED

    def is_done(self):
        return all(self._wrkStat)

# Generate production data
def generate_production_data(days):
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    production_times = np.random.uniform(1, 5, days)
    restocking_times = np.random.uniform(0.5, 2, days)
    fixing_times = np.random.uniform(2, 4, days)
    stages = ['Assembly', 'Painting', 'Quality Control', 'Packaging', 'Shipping']
    production_stages = np.random.choice(stages, days, p=[0.3, 0.2, 0.3, 0.1, 0.1])
    
    data = {
        "Date": dates,
        "Production Time": production_times,
        "Restocking Time": restocking_times,
        "Fixing Time": fixing_times,
        "Production Stage": production_stages,
    }
    
    return pd.DataFrame(data)

# Generate data for a year
data = generate_production_data(365)

# Factory Summary
st.title("Factory Simulation Dashboard")

st.sidebar.title("Dashboard Selection")
page = st.sidebar.selectbox(
    "Select a Dashboard", 
    ["Factory Summary", 
     "Production Time Analysis", 
     "Restocking Time Analysis", 
     "Fixing Time Analysis", 
     "Production Stage Analysis",
     "Product Information"]
)

# Select a timeframe
timeframe_options = {
    "Week": 7,
    "Month": 30,
    "6 Months": 183,
    "Year": 365,
}

timeframe_choice = st.sidebar.selectbox("Select a Timeframe", list(timeframe_options.keys()))
timeframe_days = timeframe_options[timeframe_choice]

# Filter data based on the selected timeframe
filtered_data = data[data["Date"] >= datetime.now() - timedelta(days=timeframe_days)]

# Factory Summary Dashboard
if page == "Factory Summary":
    st.header("Factory Summary")
    # Use st.metric for big numbers
    st.metric("Total Production Records", f"{len(filtered_data)}")
    st.metric("Total Production Time (avg)", f"{filtered_data['Production Time'].mean():.2f} hours")
    st.metric("Total Restocking Time (avg)", f"{filtered_data['Restocking Time'].mean():.2f} hours")
    st.metric("Total Fixing Time (avg)", f"{filtered_data['Fixing Time'].mean():.2f} hours")

# Production Time Analysis Dashboard
elif page == "Production Time Analysis":
    st.header("Production Time Analysis")
    # Change to a line chart for smoother trend visualization
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=filtered_data["Date"], y=filtered_data["Production Time"], color='skyblue')
    plt.title("Production Time Trend")
    plt.xlabel("Date")
    plt.ylabel("Production Time (hours)")
    st.pyplot(plt)