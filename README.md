🚕 Uber Ride Analytics — End-to-End Data Pipeline Using Linux Project

An end-to-end data analytics pipeline that demonstrates how raw CSV data can be transformed into clean, structured insights using Bash, SQLite, and Streamlit — without relying on heavy frameworks.

This project mirrors real-world data engineering workflows: messy data, command-line processing, analytics persistence, and interactive dashboards.

📌 Project Overview

Pipeline Flow

Raw CSV (Kaggle)
   ↓
Bash Data Cleaning
   ↓
Shell-Based Analytics
   ↓
SQLite Storage
   ↓
Streamlit Dashboard


Domain: Ride bookings & mobility analytics
Dataset Source: Kaggle (Uber Ride Analytics)

📥 Stage 1 — Dataset Acquisition

Dataset downloaded from Kaggle

Raw CSV contained:

Missing values

Inconsistent formats

Noise & invalid records

Mimics how data is typically received in real-world pipelines

🧹 Stage 2 — Data Cleaning (Bash)

Script: dataclean.sh

Cleaning Operations

Removed invalid & duplicate rows

Trimmed whitespace

Normalized NULL values

Fixed negative numeric values

Capped extreme outliers

Standardized categorical text

Final sanity cleanup

Why Bash?

Fast streaming processing

Works in constrained environments

Scales to large CSV files

Reproducible & automatable

📊 Stage 3 — Exploratory Analytics (Shell)

Script: analytics.sh
Tools: Bash + AWK

Analytics Generated

Booking status distribution

Vehicle demand patterns

Pickup & drop location popularity

Revenue metrics

Cancellation analysis

Demonstrates that meaningful analytics can be performed without Python or Pandas.

🗄️ Stage 4 — Analytics Storage (SQLite)

Script: analytics_to_sql.sh

Features

SQLite database creation

Normalized analytics tables

Pre-aggregated metrics

Fast downstream access

Why SQLite?

Lightweight & portable

Zero configuration

Ideal for analytics dashboards

Production-friendly for read-heavy workloads

📈 Stage 5 — Interactive Dashboard (Streamlit)

Framework: Streamlit
Visuals: Plotly
Backend: SQLite + CSV

Dashboard Capabilities

SQL-backed KPIs (fast & stable)

CSV-backed deep analytics

Interactive filters

Time trends & correlations

Clean, modular architecture

Optional code visibility toggle for data cleaning logic

🗂️ Project Structure
.
├── data/
│   ├── ncr_ride_bookings_dirty.csv
│   └── ncr_ride_bookings_clean.csv
│
├── scripts/
│   ├── dataclean.sh
│   ├── analytics.sh
│   └── analytics_to_sql.sh
│
├── dashboard/
│   ├── app.py
│   └── assets/
│
├── analytics.db
├── requirements.txt
└── README.md

⚙️ Setup & Usage
1️⃣ Clone Repository
git clone https://github.com/yourusername/uber-ride-analytics.git
cd uber-ride-analytics

2️⃣ Run Data Cleaning
bash scripts/dataclean.sh

3️⃣ Run Analytics
bash scripts/analytics.sh

4️⃣ Store Results in SQLite
bash scripts/analytics_to_sql.sh

5️⃣ Launch Dashboard
pip install -r requirements.txt
streamlit run dashboard/app.py

📦 Requirements

See requirements.txt

Core dependencies:

Streamlit

Pandas

Plotly

SQLite

Pillow
