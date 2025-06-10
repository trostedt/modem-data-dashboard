import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Simulate data
np.random.seed(1)
time = pd.date_range(start="2025-06-01", periods=100, freq="H")
operators = ['Telia FI', 'elisa', 'unknown']
bearers = ['GSM', 'LTE', 'UNKNOWN']

data = pd.DataFrame({
    "Time": time,
    "Signal Level (1-5)": np.clip(np.round(3 + np.random.normal(0, 0.5, 100).cumsum() / 50), 1, 5),
    "Link Quality (%)": np.clip(70 + np.random.normal(0, 5, 100), 0, 100),
    "Signal Strength (dBm)": -75 + np.random.normal(0, 2, 100),
    "Latency (ms)": 20 + np.random.normal(0, 2, 100).cumsum(),
    "Modem Connected": np.random.choice([0, 1], size=100, p=[0.05, 0.95]),
    "Operator": np.random.choice(operators, size=100, p=[0.6, 0.3, 0.1]),
    "Bearer": np.random.choice(bearers, size=100, p=[0.2, 0.7, 0.1])
})

st.set_page_config(page_title="Modem Data Dashboard", layout="wide")
st.title("📶 Modem Data Quality Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
selected_operator = st.sidebar.multiselect("Operator", options=operators, default=operators)
selected_bearer = st.sidebar.multiselect("Bearer", options=bearers, default=bearers)

# Filter data
filtered_data = data[(data["Operator"].isin(selected_operator)) & (data["Bearer"].isin(selected_bearer))]

# Main charts for numeric metrics
metrics = [
    "Signal Level (1-5)",
    "Link Quality (%)",
    "Signal Strength (dBm)",
    "Latency (ms)"
]

for metric in metrics:
    fig = px.line(
        filtered_data,
        x="Time",
        y=metric,
        hover_data=["Operator", "Bearer", "Modem Connected"],
        title=metric
    )
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# Modem Connected status as a step plot
st.subheader("Modem Connection Status")
fig_conn = px.line(
    filtered_data,
    x="Time",
    y="Modem Connected",
    title="Modem Connected (0 = No, 1 = Yes)",
    line_shape='hv'
)
fig_conn.update_layout(
    height=200,
    margin=dict(l=10, r=10, t=30, b=10),
    yaxis=dict(
        tickvals=[0, 1],
        ticktext=["Disconnected", "Connected"]
    )
)
st.plotly_chart(fig_conn, use_container_width=True)

# Operator and Bearer timelines
st.subheader("Operator and Bearer Changes")
fig_cat = go.Figure()
fig_cat.add_trace(
    go.Scatter(
        x=filtered_data["Time"],
        y=filtered_data["Operator"],
        mode="lines+markers",
        name="Operator"
    )
)
fig_cat.add_trace(
    go.Scatter(
        x=filtered_data["Time"],
        y=filtered_data["Bearer"],
        mode="lines+markers",
        name="Bearer"
    )
)
fig_cat.update_layout(
    height=300,
    margin=dict(l=10, r=10, t=30, b=10),
    yaxis_title="Category"
)
st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")
st.caption("Interactive modem data dashboard using Streamlit + Plotly")