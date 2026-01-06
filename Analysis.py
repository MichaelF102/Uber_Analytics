import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --------------------------------
# CONFIG
# --------------------------------
st.set_page_config(
    page_title="Uber Ride Analytics Dashboard",
    layout="wide"
)

DB_PATH = "ncr_ride_analytics.db"

# --------------------------------
# COLOR PALETTES
# --------------------------------
STATUS_COLORS = {
    "Completed": "#2ECC71",
    "Cancelled": "#E74C3C",
    "Incomplete": "#F1C40F"
}

VEHICLE_COLORS = px.colors.qualitative.Set2
PAYMENT_COLORS = px.colors.qualitative.Pastel
TIME_SERIES_COLOR = "#3498DB"
HEATMAP_SCALE = "YlOrRd"

# --------------------------------
# DB HELPERS
# --------------------------------
def load_df(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --------------------------------
# LOAD RAW CSV
# --------------------------------
@st.cache_data
def load_csv():
    df = pd.read_csv("ncr_ride_bookings_clean.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour
    return df

raw_df = load_csv()

# --------------------------------
# LOAD FILTER DIMENSIONS
# --------------------------------
ride_status_list = load_df("SELECT DISTINCT status FROM ride_status_distribution")["status"].tolist()
vehicle_list = load_df("SELECT DISTINCT vehicle_type FROM vehicle_demand")["vehicle_type"].tolist()
pickup_list = load_df("SELECT DISTINCT location FROM top_pickup_locations")["location"].tolist()
drop_list = load_df("SELECT DISTINCT location FROM top_drop_locations")["location"].tolist()
payment_list = load_df("SELECT DISTINCT method FROM payment_methods")["method"].tolist()

# --------------------------------
# SIDEBAR FILTERS
# --------------------------------
st.sidebar.header("🎛 Filters")

selected_status = st.sidebar.multiselect("Ride Status", ride_status_list, ride_status_list)
selected_vehicle = st.sidebar.multiselect("Vehicle Type", vehicle_list, vehicle_list)
selected_pickup = st.sidebar.multiselect("Pickup Location", pickup_list, pickup_list)
selected_drop = st.sidebar.multiselect("Drop Location", drop_list, drop_list)
selected_payment = st.sidebar.multiselect("Payment Method", payment_list, payment_list)

def sql_in(values):
    return "(" + ",".join(f"'{v}'" for v in values) + ")"

# --------------------------------
# LOAD SQL DATA
# --------------------------------
summary = load_df("SELECT * FROM summary_metrics")
ride_status = load_df(f"SELECT * FROM ride_status_distribution WHERE status IN {sql_in(selected_status)}")
vehicles = load_df(f"SELECT * FROM vehicle_demand WHERE vehicle_type IN {sql_in(selected_vehicle)}")
pickup = load_df(f"SELECT * FROM top_pickup_locations WHERE location IN {sql_in(selected_pickup)}")
drop = load_df(f"SELECT * FROM top_drop_locations WHERE location IN {sql_in(selected_drop)}")
payment = load_df(f"SELECT * FROM payment_methods WHERE method IN {sql_in(selected_payment)}")
cancel = load_df("SELECT * FROM cancellations")

# --------------------------------
# HEADER
# --------------------------------
st.title("🚕 Uber Ride Analytics Dashboard")

# --------------------------------
# KPI METRICS
# --------------------------------
st.subheader("📌 Key Metrics")
cols = st.columns(len(summary))
for col, row in zip(cols, summary.itertuples()):
    col.metric(row.metric, f"{row.value:,.2f}")

# --------------------------------
# RIDE DISTRIBUTION
# --------------------------------
st.subheader("📊 Ride Distribution")

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        ride_status,
        x="status",
        y="count",
        color="status",
        color_discrete_map=STATUS_COLORS,
        title="Ride Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        vehicles,
        x="vehicle_type",
        y="count",
        color="vehicle_type",
        color_discrete_sequence=VEHICLE_COLORS,
        title="Vehicle Type Demand"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# TOP LOCATIONS
# --------------------------------
st.subheader("📍 Top Locations")

c3, c4 = st.columns(2)

with c3:
    fig = px.bar(
        pickup,
        x="count",
        y="location",
        orientation="h",
        color="count",
        color_continuous_scale="Blues",
        title="Top Pickup Locations"
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.bar(
        drop,
        x="count",
        y="location",
        orientation="h",
        color="count",
        color_continuous_scale="Greens",
        title="Top Drop Locations"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# BOOKING OVERVIEW
# --------------------------------
st.header("📘 Booking Overview")

c5, c6 = st.columns(2)

with c5:
    fig = px.pie(
        raw_df,
        names="Booking Status",
        hole=0.4,
        color="Booking Status",
        color_discrete_map=STATUS_COLORS,
        title="Booking Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    fig = px.histogram(
        raw_df,
        x="Booking Status",
        color="Booking Status",
        color_discrete_map=STATUS_COLORS,
        title="Completed vs Cancelled vs Incomplete"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# CANCELLATIONS & PAYMENTS
# --------------------------------
st.subheader("❌ Cancellations & 💳 Payments")

c7, c8 = st.columns(2)

with c7:
    fig = px.pie(
        cancel,
        names="type",
        values="total",
        color_discrete_sequence=["#E74C3C", "#F39C12"],
        title="Cancellation Breakdown"
    )
    st.plotly_chart(fig, use_container_width=True)

with c8:
    fig = px.bar(
        payment,
        x="method",
        y="count",
        color="method",
        color_discrete_sequence=PAYMENT_COLORS,
        title="Payment Method Usage"
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# TIME & DEMAND
# --------------------------------
st.header("⏱️ Time & Demand Patterns")

daily = raw_df.groupby("Date").size().reset_index(name="Rides")
fig = px.line(daily, x="Date", y="Rides", markers=True,
              color_discrete_sequence=[TIME_SERIES_COLOR],
              title="Total Rides Over Time")
st.plotly_chart(fig, use_container_width=True)

dow = raw_df.groupby("DayOfWeek").size().reset_index(name="Rides")
fig = px.bar(dow, x="DayOfWeek", y="Rides",
             color="Rides", color_continuous_scale="Viridis",
             title="Rides by Day of Week")
st.plotly_chart(fig, use_container_width=True)

hourly = raw_df.groupby("Hour").size().reset_index(name="Rides")
fig = px.area(hourly, x="Hour", y="Rides",
              color_discrete_sequence=["#9B59B6"],
              title="Rides by Hour of Day")
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# VEHICLE PERFORMANCE
# --------------------------------
st.header("🚗 Vehicle Type Performance")

fig = px.bar(
    raw_df.groupby("Vehicle Type").size().reset_index(name="Bookings"),
    x="Vehicle Type",
    y="Bookings",
    color="Vehicle Type",
    color_discrete_sequence=VEHICLE_COLORS,
    title="Bookings by Vehicle Type"
)
st.plotly_chart(fig, use_container_width=True)

fig = px.box(
    raw_df,
    x="Vehicle Type",
    y="Booking Value",
    color="Vehicle Type",
    color_discrete_sequence=VEHICLE_COLORS,
    title="Booking Value by Vehicle Type"
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# LOCATION HEATMAP
# --------------------------------
st.header("📍 Location Intelligence")

heat = raw_df.groupby(["Pickup Location", "Drop Location"]).size().reset_index(name="Trips")
heat = heat.sort_values("Trips", ascending=False).head(50)

fig = px.density_heatmap(
    heat,
    x="Pickup Location",
    y="Drop Location",
    z="Trips",
    color_continuous_scale=HEATMAP_SCALE,
    title="Pickup vs Drop Location Heatmap"
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# RATINGS & QUALITY
# --------------------------------
st.header("⭐ Service Quality")

fig = px.histogram(raw_df, x="Driver Ratings", nbins=20,
                   color_discrete_sequence=["#1ABC9C"],
                   title="Driver Rating Distribution")
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(raw_df, x="Customer Rating", nbins=20,
                   color_discrete_sequence=["#F39C12"],
                   title="Customer Rating Distribution")
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# RAW TABLES
# --------------------------------
with st.expander("📂 View SQL Tables"):
    st.dataframe(ride_status)
    st.dataframe(vehicles)
    st.dataframe(pickup)
    st.dataframe(drop)
    st.dataframe(payment)
    
st.header("📄 Full Uber Ride Dataset")

st.dataframe(
    raw_df,
    use_container_width=True,
    height=600
)






