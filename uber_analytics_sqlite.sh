#!/bin/bash

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

