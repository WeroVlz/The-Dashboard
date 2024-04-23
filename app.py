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

# Title
st.title("Factory Simulation Dashboard")

st.sidebar.title("Dashboard Selection")
page = st.sidebar.selectbox(
    "Select a Dashboard", 
    ["Product Information",
     "Factory Summary", 
     "Production Time Analysis", 
     "Restocking Time Analysis", 
     "Fixing Time Analysis", 
     "Production Stage Analysis"
     ]
)

# Timeframes
timeframe_options = {
    "Week": 7,
    "Month": 30,
    "6 Months": 183,
    "Year": 365,
}

timeframe_choice = st.sidebar.selectbox("Select a Timeframe", list(timeframe_options.keys()))
timeframe_days = timeframe_options[timeframe_choice]
filtered_data = data[data["Date"] >= datetime.now() - timedelta(days=timeframe_days)]

# Factory Summary Dashboard Page
if page == "Factory Summary":
    st.header("Factory Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Production Records", f"{len(filtered_data)}")
        st.metric("Total Production Time (avg)", f"{filtered_data['Production Time'].mean():.2f} hours")
        st.metric("Total Restocking Time (avg)", f"{filtered_data['Restocking Time'].mean():.2f} hours")
        st.metric("Total Fixing Time (avg)", f"{filtered_data['Fixing Time'].mean():.2f} hours")

    with col2:
        image_url = "https://economictimes.indiatimes.com/thumb/msid-102897652,width-1200,height-900,resizemode-4,imgsize-2145478/ev-manufacturers-have-been-at-the-forefront-of-ev-technology-innovation-that-appeal-to-the-preferences-of-tech-savvy-chinese-consumers-who-like-having-more-intelligent-features-in-cars-.jpg?from=mdr"
        st.image(image_url, use_column_width=True)
        image_url = "https://static.wixstatic.com/media/961f25_a6381e36b4d74c19a7afadf9e35c89a4~mv2.jpg/v1/fill/w_980,h_654,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/961f25_a6381e36b4d74c19a7afadf9e35c89a4~mv2.jpg"
        st.image(image_url, use_column_width=True)

# Production Time Analysis Dashboard Page
elif page == "Production Time Analysis":
    st.header("Production Time Analysis")
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=filtered_data["Date"], y=filtered_data["Production Time"], color='skyblue')
    plt.title("Production Time Trend")
    plt.xlabel("Date")
    plt.ylabel("Production Time (hours)")
    st.pyplot(plt)

# Restocking Time Analysis Dashboard Page
elif page == "Restocking Time Analysis":
    st.header("Restocking Time Analysis")
    plt.figure(figsize=(8, 6))
    sns.histplot(filtered_data["Restocking Time"], kde=True, color='orange', bins=10)
    plt.title("Restocking Time Distribution")
    plt.xlabel("Restocking Time (hours)")
    plt.ylabel("Frequency")
    st.pyplot(plt)

# Fixing Time Analysis Dashboard Page
if page == "Fixing Time Analysis":
    st.header("Fixing Time Analysis")
    fig = px.histogram(
        filtered_data,
        x="Fixing Time",
        nbins=10,
        title="Fixing Time Histogram",
        color_discrete_sequence=['#1f77b4'],
        labels={"Fixing Time": "Fixing Time (hours)"},
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title="Fixing Time (hours)",
        yaxis_title="Frequency",
        bargap=0.1,
        title_font_size=20,
        title_x=0.5,
    )
    st.plotly_chart(fig)

# Production Stage Analysis Dashboard Page
elif page == "Production Stage Analysis":
    st.header("Production Stage Analysis")
    fig = px.pie(filtered_data, names="Production Stage", title="Production Stages Distribution")
    st.plotly_chart(fig)