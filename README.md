# 🚕 Uber Ride Analytics — End-to-End Data Engineering Project

An end-to-end **data engineering and analytics pipeline** that transforms raw CSV data into structured insights using **Bash, SQLite, and Streamlit**.

This project intentionally mirrors **real-world data workflows** — messy data ingestion, command-line processing, analytics persistence, and interactive visualization — without relying on heavy frameworks.

---

## 📌 Project Overview

### Pipeline Flow

Raw CSV (Kaggle)
↓
Bash Data Cleaning
↓
Shell-Based Analytics
↓
SQLite Storage
↓
Streamlit Dashboard

yaml
Copy code

- **Domain:** Ride bookings & mobility analytics  
- **Dataset Source:** Kaggle (Uber Ride Analytics)

---

## 📥 Stage 1 — Dataset Acquisition

- Dataset downloaded from Kaggle
- Raw CSV contained:
  - Missing values
  - Inconsistent date & time formats
  - Noise and invalid records
- Represents how data is typically received in real-world pipelines

---

## 🧹 Stage 2 — Data Cleaning (Bash)

**Script:** `dataclean.sh`

### Cleaning Operations
- Removed invalid and duplicate rows
- Trimmed leading and trailing whitespace
- Normalized NULL values
- Fixed negative numeric values
- Capped extreme outliers
- Standardized categorical text
- Final sanity cleanup

### Why Bash?
- Fast streaming processing
- Works in constrained environments
- Scales to large CSV files
- Fully reproducible and automatable

---

## 📊 Stage 3 — Exploratory Analytics (Shell)

**Script:** `analytics.sh`  
**Tools:** Bash + AWK

### Analytics Generated
- Booking status distribution
- Vehicle demand patterns
- Pickup and drop location popularity
- Revenue metrics
- Cancellation analysis

This stage demonstrates that **meaningful analytics can be performed without Python or Pandas**.

---

## 🗄️ Stage 4 — Persisting Analytics (SQLite)

**Script:** `analytics_to_sql.sh`

### Features
- SQLite database creation
- Normalized analytics tables
- Pre-aggregated metrics
- Fast downstream query access

### Why SQLite?
- Lightweight and portable
- Zero configuration
- Ideal for analytics dashboards
- Production-friendly for read-heavy workloads

---

## 📈 Stage 5 — Interactive Dashboard (Streamlit)

**Framework:** Streamlit  
**Visualizations:** Plotly  
**Backend:** SQLite + CSV

### Dashboard Features
- SQL-backed KPIs for fast performance
- CSV-backed deep analytics (time trends and correlations)
- Interactive filters
- Modular and maintainable code structure
- Optional code visibility toggle for data cleaning logic

---

## 🗂️ Project Structure

.
├── data/
│ ├── ncr_ride_bookings_dirty.csv
│ └── ncr_ride_bookings_clean.csv
│
├── scripts/
│ ├── dataclean.sh
│ ├── analytics.sh
│ └── analytics_to_sql.sh
│
├── dashboard/
│ ├── app.py
│ └── assets/
│
├── analytics.db
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Setup & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/uber-ride-analytics.git
cd uber-ride-analytics
2️⃣ Run Data Cleaning
bash
Copy code
bash scripts/dataclean.sh
3️⃣ Run Analytics
bash
Copy code
bash scripts/analytics.sh
4️⃣ Store Results in SQLite
bash
Copy code
bash scripts/analytics_to_sql.sh
5️⃣ Launch the Dashboard
bash
Copy code
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

