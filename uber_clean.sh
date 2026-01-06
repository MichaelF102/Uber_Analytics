#!/bin/bash

#
INPUT="ncr_ride_bookings_dirty.csv"
OUTPUT="ncr_ride_bookings_clean.csv"
TMP="__tmp_clean.csv"

set -e

log() {
  echo "[INFO] $1"
}


# 1. REMOVE LEADING / TRAILING WHITESPACE

trim_whitespace() {
  log "Trimming whitespaces"
  sed 's/^[ \t]*//;s/[ \t]*$//' "$INPUT" > "$TMP"
}


# 2. NORMALIZE NULL VALUES

normalize_nulls() {
  log "Normalizing NULL values"
  sed -i '
    s/, *,/,/g;
    s/,,/,NULL,/g;
    s/^,/NULL,/g;
    s/,$/,NULL/g;
    s/\bNaN\b/NULL/g;
    s/\bnan\b/NULL/g;
  ' "$TMP"
}


# 3. REMOVE DUPLICATES (EXACT ROW MATCH)

remove_duplicates() {
  log "Removing duplicate rows"
  awk '!seen[$0]++' "$TMP" > "$TMP.dup"
  mv "$TMP.dup" "$TMP"
}


# 4. FIX NEGATIVE NUMERIC VALUES

fix_negatives() {
  log "Fixing negative numeric values"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^-[0-9]+(\.[0-9]+)?$/) {
        $i = abs($i)
      }
    }
    print
  }
  function abs(x){return x<0?-x:x}
  ' OFS=',' "$TMP" > "$TMP.neg"
  mv "$TMP.neg" "$TMP"
}


cap_outliers() {
  log "Capping extreme outliers"

  awk -F',' '
  NR==1 {
    print
    next
  }
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /^[0-9]+(\.[0-9]+)?$/ && $i > 1000000) {
        $i = 1000000
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.out"
  mv "$TMP.out" "$TMP"
}


standardize_text() {
  log "Standardizing text columns (lowercase)"
  awk -F',' '
  NR==1 {print; next}
  {
    for (i=1; i<=NF; i++) {
      if ($i ~ /[A-Za-z]/) {
        gsub(/^[ \t]+|[ \t]+$/, "", $i)
        $i = tolower($i)
      }
    }
    print
  }
  ' OFS=',' "$TMP" > "$TMP.txt"
  mv "$TMP.txt" "$TMP"
}


final_sanity() {
  log "Final sanity cleanup"
  sed -i 's/NULL,NULL/NULL/g' "$TMP"
}


# PIPELINE

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


