# ABOUTME: Calculates 52-week high ratio following George and Hwang 2004 Table 1
# ABOUTME: calculates split-adjusted month-end price divided by its maximum over the 12 months ending in the current month

"""
High52.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/High52.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, prc, cfacpr]

Outputs:
    - High52.csv: CSV file with columns [permno, yyyymm, High52]
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting High52 calculation...")

# DATA LOAD
daily_crsp = pd.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
df = daily_crsp.copy()
print(f"Loaded dailyCRSP data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Convert daily dates to monthly periods for aggregation
df["time_avail_m"] = df["time_d"].dt.to_period("M").dt.start_time

# Split-adjust prices with cfacpr. cfacpr is normalised to 1 at the vintage date of
# the CRSP file, so a single adjusted price depends on the vintage (see issue #95).
# High52 is a ratio of two adjusted prices of the same stock, so the vintage factor
# cancels: (P_t/cfacpr_t) / (P_s/cfacpr_s) only involves cfacpr_s/cfacpr_t, the
# cumulative split factor between s and t, which is known at t. There is no
# look-ahead bias. Without the adjustment, reverse splits can produce weird ratios
# (see issue #205).
df["prcadj"] = df["prc"].abs() / df["cfacpr"].where(df["cfacpr"] != 0)

# Aggregate daily data to monthly: max price and end-of-month price
df_collapsed = (
    df.groupby(["permno", "time_avail_m"])
    .agg(
        maxpr=("prcadj", "max"),
        prcadj=("prcadj", "last"),  # lastnm means last non-missing
    )
    .reset_index()
)

print(f"After collapse by permno and time_avail_m: {len(df_collapsed)} observations")

# Sort for time series operations
df = df_collapsed.sort_values(["permno", "time_avail_m"])

# Find the 52-week high: maximum price over the 12-month period ending on the last
# day of the current month (George and Hwang 2004, Section I.A). Including the
# current month bounds the ratio at 1.

# Create lags 0 to 11 of maxpr (lag 0 is the current month)
for i in range(0, 12):
    df[f"l{i}_maxpr"] = df.groupby("permno")["maxpr"].shift(i)

# Calculate maximum across the 12 months
lag_columns = [f"l{i}_maxpr" for i in range(0, 12)]
df["temp"] = df[lag_columns].max(axis=1)

# Calculate ratio: current price / 52-week high
df["High52"] = df["prcadj"] / df["temp"]

print(f"High52 calculated for {df['High52'].notna().sum()} observations")

# SAVE
save_predictor(df, "High52")
print("High52.csv saved successfully")
