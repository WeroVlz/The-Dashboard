import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_production_data(days):
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    production_times = np.random.uniform(1, 5, days)
    restocking_times = np.random.uniform(0.5, 2, days)
    fixing_times = np.random.uniform(2, 4, days)
    data = {
        "Date": dates,
        "Production Time": production_times,
        "Restocking Time": restocking_times,
        "Fixing Time": fixing_times,
    }
    return pd.DataFrame(data)

data = generate_production_data(365)

st.title("Factory Simulation Dashboard")

st.sidebar.title("Dashboard Selection")
page = st.sidebar.selectbox("Select a Dashboard", [
    "Factory Summary",
    "Production Time Analysis",
    "Restocking Time Analysis",
    "Fixing Time Analysis",
    "Product Information",
    "Factory Logs",
])

timeframe_options = {
    "Week": 7,
    "Month": 30,
    "6 Months": 183,
    "Year": 365,
}

timeframe_choice = st.sidebar.selectbox("Select a Timeframe", list(timeframe_options.keys()))
timeframe_days = timeframe_options[timeframe_choice]

# Filtra datos x timeframe
filtered_data = data[data["Date"] >= datetime.now() - timedelta(days=timeframe_days)]