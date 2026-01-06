import streamlit as st

st.set_page_config(
    page_title="About | NCR Ride Analytics",
    layout="wide"
)

st.title("Title: Uber Data Analytics Pipeline using Linux")
st.write("### Name: Michael Fernandes")
st.write("### UID: 2509006")
st.write("### Roll No. 06")
st.write("### Linux and Cloud Computing Project CIA-1")

st.divider()
st.title("📘 About This Project")

st.markdown("""
This project demonstrates a **complete real-world data analytics workflow** using Linux Commands, starting from
raw data ingestion to an interactive analytics dashboard.

The goal was to create Pipelines using shell commands for cleaning data,analyzing and storing results in sqlite database and deploying results in streamlit..
""")

st.image(
    "images/pipeline.jpg",
    use_container_width=True
)

st.divider()

# --------------------------------
# STAGE 1
# --------------------------------
st.header("📥 Stage 1 — Dataset Acquisition")

st.markdown("""
- Dataset downloaded from **Kaggle**: "https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard"
- Domain: **Ride bookings & mobility analytics**
- Raw CSV contained:
  - Missing values
  - Inconsistent formats
  - Noise & invalid records

This stage mimics how raw data is typically received in real-world pipelines.
""")

# --------------------------------
# STAGE 2
# --------------------------------
st.header("🧹 Stage 2 — Data Cleaning ")

st.image(
    "images/clean.png",
    use_container_width=True
)

st.markdown("""
The dataset was cleaned using a **custom Bash script**:

**`dataclean.sh`**
- Removed invalid rows
- Standardized date & time formats
- Handled missing values
- Ensured numeric column consistency
- Produced a clean, analytics-ready CSV

""")

if "show_clean_code" not in st.session_state:
    st.session_state.show_clean_code = False

if st.button("Show / Hide cleaning.sh"):
    st.session_state.show_clean_code = not st.session_state.show_clean_code
    
if st.session_state.show_clean_code:
    st.code(
        """#!/bin/bash

# ============================================
# CONFIG
# ============================================
INPUT="ncr_ride_bookings_dirty.csv"
OUTPUT="ncr_ride_bookings_clean.csv"
TMP="__tmp_clean.csv"

set -e

# ============================================
# UTILS
# ============================================
log() {
  echo "[INFO] $1"
}

# ============================================
# 1. REMOVE LEADING / TRAILING WHITESPACE
# ============================================
trim_whitespace() {
  log "Trimming whitespaces"
  sed 's/^[ \\t]*//;s/[ \\t]*$//' "$INPUT" > "$TMP"
}

# ============================================
# 2. NORMALIZE NULL VALUES
# ============================================
normalize_nulls() {
  log "Normalizing NULL values"
  sed -i '
    s/, *,/,/g;
    s/,,/,NULL,/g;
    s/^,/NULL,/g;
    s/,$/,NULL/g;
    s/\\bNaN\\b/NULL/g;
    s/\\bnan\\b/NULL/g;
  ' "$TMP"
}

# ============================================
# 3. REMOVE DUPLICATES
# ============================================
remove_duplicates() {
  log "Removing duplicate rows"
  awk '!seen[$0]++' "$TMP" > "$TMP.dup"
  mv "$TMP.dup" "$TMP"
}

# ============================================
# 4. FIX NEGATIVE NUMERIC VALUES
# ============================================
fix_negatives() {
  log "Fixing negative numeric values"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^-[0-9]+(\\.[0-9]+)?$/) {
        $i = abs($i)
      }
    }
    print
  }
  function abs(x){return x<0?-x:x}
  ' OFS=',' "$TMP" > "$TMP.neg"
  mv "$TMP.neg" "$TMP"
}

# ============================================
# 5. CAP EXTREME OUTLIERS
# ============================================
cap_outliers() {
  log "Capping extreme outliers"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^[0-9]+(\\.[0-9]+)?$/ && $i > 1000000) {
        $i = 1000000
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.out"
  mv "$TMP.out" "$TMP"
}

# ============================================
# 6. STANDARDIZE TEXT
# ============================================
standardize_text() {
  log "Standardizing text columns"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /[A-Za-z]/) {
        gsub(/^[ \\t]+|[ \\t]+$/, "", $i)
        $i = tolower($i)
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.txt"
  mv "$TMP.txt" "$TMP"
}

# ============================================
# 7. FINAL SANITY CLEAN
# ============================================
final_sanity() {
  log "Final sanity cleanup"
  sed -i 's/NULL,NULL/NULL/g' "$TMP"
}

# ============================================
# PIPELINE
# ============================================
log "Starting cleaning pipeline"

trim_whitespace
normalize_nulls
remove_duplicates
fix_negatives
cap_outliers
standardize_text
final_sanity

mv "$TMP" "$OUTPUT"

log "Cleaning complete → $OUTPUT"
""",
        language="bash"
    )


# --------------------------------
# STAGE 3
# --------------------------------
st.header("📊 Stage 3 — Analytics via Shell Scripting")

st.image(
    "images/analyze.png",
    use_container_width=True
)
st.markdown("""
Exploratory analytics were performed using **pure Bash + AWK**:

**`analytics.sh`**
- Booking status distribution
- Vehicle demand
- Location popularity
- Revenue metrics
- Cancellation analysis

This stage shows:
- Strong command-line analytics skills
- Ability to work in constrained environments
- Efficient processing of large CSV files
""")

if "show_ana_code" not in st.session_state:
    st.session_state.show_ana_code = False

if st.button("Show / Hide analytics.sh"):
    st.session_state.show_ana_code = not st.session_state.show_ana_code
    
if st.session_state.show_ana_code:
    st.code(
        """

#!/bin/bash

FILE="ncr_ride_bookings_clean.csv"


# Remove header
DATA=$(tail -n +2 "$FILE")


# 1️⃣ Total number of bookings
echo "1. Total bookings:"
echo "$DATA" | wc -l
echo "--------------------------------------------------"

# 2️⃣ Completed vs Cancelled vs Incomplete rides
echo "2. Ride status distribution:"
echo "$DATA" | awk -F',' '{print $4}' | sort | uniq -c | sort -nr
echo "--------------------------------------------------"

# 3️⃣ Total revenue from completed rides
echo "3. Total booking value (Completed rides):"
echo "$DATA" | awk -F',' '$4=="Completed"{sum+=$17} END{printf "%.2f\n", sum}'
echo "--------------------------------------------------"

# 4️⃣ Average booking value
echo "4. Average booking value:"
echo "$DATA" | awk -F',' '{sum+=$17; c++} END{printf "%.2f\n", sum/c}'
echo "--------------------------------------------------"

# 5️⃣ Top 5 pickup locations
echo "5. Top 5 pickup locations:"
echo "$DATA" | awk -F',' '{print $7}' | sort | uniq -c | sort -nr | head -5
echo "--------------------------------------------------"

# 6️⃣ Top 5 drop locations
echo "6. Top 5 drop locations:"
echo "$DATA" | awk -F',' '{print $8}' | sort | uniq -c | sort -nr | head -5
echo "--------------------------------------------------"

# 7️⃣ Vehicle type demand
echo "7. Rides by vehicle type:"
echo "$DATA" | awk -F',' '{print $6}' | sort | uniq -c | sort -nr
echo "--------------------------------------------------"

# 8️⃣ Cancellation analysis (Customer vs Driver)
echo "8. Total cancellations:"
echo "Cancelled by Customer:"
echo "$DATA" | awk -F',' '$11>0{sum+=$11} END{print sum}'
echo "Cancelled by Driver:"
echo "$DATA" | awk -F',' '$13>0{sum+=$13} END{print sum}'
echo "--------------------------------------------------"

# 9️⃣ Average ride distance & ratings
echo "9. Ride quality metrics:"
echo "Average Ride Distance (km):"
echo "$DATA" | awk -F',' '{sum+=$18; c++} END{printf "%.2f\n", sum/c}'
echo "Average Driver Rating:"
echo "$DATA" | awk -F',' '$19!=""{sum+=$19; c++} END{printf "%.2f\n", sum/c}'
echo "--------------------------------------------------"

# 🔟 Payment method usage
echo "10. Payment method distribution:"
echo "$DATA" | awk -F',' '{print $21}' | sort | uniq -c | sort -nr

""",
        language="bash"
    )

st.image(
    "images/analytics_1.png",
    use_container_width=True
)
st.image(
    "images/analytics2.png",
    use_container_width=True
)
# --------------------------------
# STAGE 4
# --------------------------------
st.header("🗄️ Stage 4 — Storing Results in SQLite")

st.markdown("""
The computed analytics were persisted using:

**`analytics_to_sql.sh`**
- Created a SQLite database
- Designed normalized tables
- Inserted pre-aggregated metrics
- Enabled fast downstream access

""")

if "show_ats_code" not in st.session_state:
    st.session_state.show_ats_code = False

if st.button("Show / Hide uber_analytics_sqlite.sh"):
    st.session_state.show_ats_code = not st.session_state.show_ats_code
    
if st.session_state.show_ats_code:
    st.code(
        """#!/bin/bash

FILE="ncr_ride_bookings_clean.csv"
DB="ncr_ride_analytics.db"

echo "================ BASIC RIDE ANALYTICS ================"

DATA=$(tail -n +2 "$FILE")

# -------------------------------
# Initialize SQLite DB
# -------------------------------
sqlite3 "$DB" <<EOF
DROP TABLE IF EXISTS summary_metrics;
DROP TABLE IF EXISTS ride_status_distribution;
DROP TABLE IF EXISTS top_pickup_locations;
DROP TABLE IF EXISTS top_drop_locations;
DROP TABLE IF EXISTS vehicle_demand;
DROP TABLE IF EXISTS cancellations;
DROP TABLE IF EXISTS payment_methods;

CREATE TABLE summary_metrics (
    metric TEXT,
    value REAL
);

CREATE TABLE ride_status_distribution (
    status TEXT,
    count INTEGER
);

CREATE TABLE top_pickup_locations (
    location TEXT,
    count INTEGER
);

CREATE TABLE top_drop_locations (
    location TEXT,
    count INTEGER
);

CREATE TABLE vehicle_demand (
    vehicle_type TEXT,
    count INTEGER
);

CREATE TABLE cancellations (
    type TEXT,
    total INTEGER
);

CREATE TABLE payment_methods (
    method TEXT,
    count INTEGER
);
EOF


TOTAL_BOOKINGS=$(echo "$DATA" | wc -l)
sqlite3 "$DB" "INSERT INTO summary_metrics VALUES ('Total Bookings', $TOTAL_BOOKINGS);"


echo "$DATA" | awk -F',' '{print $4}' | sort | uniq -c |
while read count status; do
    sqlite3 "$DB" "INSERT INTO ride_status_distribution VALUES ('$status', $count);"
done


TOTAL_REVENUE=$(echo "$DATA" | awk -F',' '$4=="Completed"{sum+=$17} END{print sum}')
sqlite3 "$DB" "INSERT INTO summary_metrics VALUES ('Total Revenue (Completed)', $TOTAL_REVENUE);"


AVG_BOOKING=$(echo "$DATA" | awk -F',' '{sum+=$17;c++} END{print sum/c}')
sqlite3 "$DB" "INSERT INTO summary_metrics VALUES ('Average Booking Value', $AVG_BOOKING);"


echo "$DATA" | awk -F',' '{print $7}' | sort | uniq -c | sort -nr | head -5 |
while read count loc; do
    sqlite3 "$DB" "INSERT INTO top_pickup_locations VALUES ('$loc', $count);"
done


echo "$DATA" | awk -F',' '{print $8}' | sort | uniq -c | sort -nr | head -5 |
while read count loc; do
    sqlite3 "$DB" "INSERT INTO top_drop_locations VALUES ('$loc', $count);"
done


echo "$DATA" | awk -F',' '{print $6}' | sort | uniq -c | sort -nr |
while read count vehicle; do
    sqlite3 "$DB" "INSERT INTO vehicle_demand VALUES ('$vehicle', $count);"
done


CUST_CANCEL=$(echo "$DATA" | awk -F',' '$11>0{sum+=$11} END{print sum}')
DRIVER_CANCEL=$(echo "$DATA" | awk -F',' '$13>0{sum+=$13} END{print sum}')

sqlite3 "$DB" "INSERT INTO cancellations VALUES ('Customer', $CUST_CANCEL);"
sqlite3 "$DB" "INSERT INTO cancellations VALUES ('Driver', $DRIVER_CANCEL);"


AVG_DISTANCE=$(echo "$DATA" | awk -F',' '{sum+=$18;c++} END{print sum/c}')
AVG_DRIVER_RATING=$(echo "$DATA" | awk -F',' '$19!=""{sum+=$19;c++} END{print sum/c}')

sqlite3 "$DB" "INSERT INTO summary_metrics VALUES ('Average Ride Distance', $AVG_DISTANCE);"
sqlite3 "$DB" "INSERT INTO summary_metrics VALUES ('Average Driver Rating', $AVG_DRIVER_RATING);"


echo "$DATA" | awk -F',' '{print $21}' | sort | uniq -c | sort -nr |
while read count method; do
    sqlite3 "$DB" "INSERT INTO payment_methods VALUES ('$method', $count);"
done

echo "===================================================="
echo "✅ Analytics successfully stored in SQLite database:"
echo "   → $DB"


""",
        language="bash"
    )
st.image(
    "images/sqlite.png",
    use_container_width=True
)

# --------------------------------
# STAGE 5
# --------------------------------
st.header("📈 Stage 5 — Interactive Dashboard (Streamlit)")

st.markdown("""
Finally, the analytics were deployed using **Streamlit**:

- SQL-backed KPIs (fast & stable)
- CSV-backed deep analytics (time trends, correlations)
- Interactive filters
- Visual storytelling with Plotly
- Clean, modular dashboard structure

""")

st.divider()


if st.session_state.show_clean_code:
    st.code(
        """#!/bin/bash

# ============================================
# CONFIG
# ============================================
INPUT="ncr_ride_bookings_dirty.csv"
OUTPUT="ncr_ride_bookings_clean.csv"
TMP="__tmp_clean.csv"

set -e

# ============================================
# UTILS
# ============================================
log() {
  echo "[INFO] $1"
}

# ============================================
# 1. REMOVE LEADING / TRAILING WHITESPACE
# ============================================
trim_whitespace() {
  log "Trimming whitespaces"
  sed 's/^[ \\t]*//;s/[ \\t]*$//' "$INPUT" > "$TMP"
}

# ============================================
# 2. NORMALIZE NULL VALUES
# ============================================
normalize_nulls() {
  log "Normalizing NULL values"
  sed -i '
    s/, *,/,/g;
    s/,,/,NULL,/g;
    s/^,/NULL,/g;
    s/,$/,NULL/g;
    s/\\bNaN\\b/NULL/g;
    s/\\bnan\\b/NULL/g;
  ' "$TMP"
}

# ============================================
# 3. REMOVE DUPLICATES
# ============================================
remove_duplicates() {
  log "Removing duplicate rows"
  awk '!seen[$0]++' "$TMP" > "$TMP.dup"
  mv "$TMP.dup" "$TMP"
}

# ============================================
# 4. FIX NEGATIVE NUMERIC VALUES
# ============================================
fix_negatives() {
  log "Fixing negative numeric values"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^-[0-9]+(\\.[0-9]+)?$/) {
        $i = abs($i)
      }
    }
    print
  }
  function abs(x){return x<0?-x:x}
  ' OFS=',' "$TMP" > "$TMP.neg"
  mv "$TMP.neg" "$TMP"
}

# ============================================
# 5. CAP EXTREME OUTLIERS
# ============================================
cap_outliers() {
  log "Capping extreme outliers"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^[0-9]+(\\.[0-9]+)?$/ && $i > 1000000) {
        $i = 1000000
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.out"
  mv "$TMP.out" "$TMP"
}

# ============================================
# 6. STANDARDIZE TEXT
# ============================================
standardize_text() {
  log "Standardizing text columns"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /[A-Za-z]/) {
        gsub(/^[ \\t]+|[ \\t]+$/, "", $i)
        $i = tolower($i)
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.txt"
  mv "$TMP.txt" "$TMP"
}

# ============================================
# 7. FINAL SANITY CLEAN
# ============================================
final_sanity() {
  log "Final sanity cleanup"
  sed -i 's/NULL,NULL/NULL/g' "$TMP"
}

# ============================================
# PIPELINE
# ============================================
log "Starting cleaning pipeline"

trim_whitespace
normalize_nulls
remove_duplicates
fix_negatives
cap_outliers
standardize_text
final_sanity

mv "$TMP" "$OUTPUT"

log "Cleaning complete → $OUTPUT"
""",
        language="bash"
    )

































