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





