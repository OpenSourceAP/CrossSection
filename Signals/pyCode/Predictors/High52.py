# ABOUTME: Calculates 52-week high ratio following George and Hwang 2004 Table 1
# ABOUTME: Run from pyCode/ directory: python3 Predictors/High52.py

# Inputs:
#   - ../pyData/Intermediate/dailyCRSP.parquet
# Outputs:
#   - ../pyData/Predictors/High52.csv

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

# Use absolute price without split adjustment (following original methodology)
df["prcadj"] = df["prc"].abs()

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

# Find maximum price over previous 12 months

# Create 12-month lags of maxpr
for i in range(1, 13):
    df[f"l{i}_maxpr"] = df.groupby("permno")["maxpr"].shift(i)

# Calculate maximum across all 12 lags
lag_columns = [f"l{i}_maxpr" for i in range(1, 13)]
df["temp"] = df[lag_columns].max(axis=1)

# Calculate ratio: current price / 52-week high
df["High52"] = df["prcadj"] / df["temp"]

print(f"High52 calculated for {df['High52'].notna().sum()} observations")

# SAVE
save_predictor(df, "High52")
print("High52.csv saved successfully")
