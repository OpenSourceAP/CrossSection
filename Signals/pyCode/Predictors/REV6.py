# ABOUTME: REV6 following Chan, Jegadeesh and Lakonishok 1996 JF Table 7
# ABOUTME: calculates 6-month sum of monthly changes in mean earnings estimates scaled by prior month stock price

"""
REV6.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/REV6.py

Inputs:
    - IBES_EPS_Unadj.parquet: IBES earnings forecast data with columns [tickerIBES, time_avail_m, fpi, fpedats, statpers, meanest]
    - SignalMasterTable.parquet: Master security data with columns [permno, tickerIBES, time_avail_m, prc]

Outputs:
    - REV6.csv: CSV file with columns [permno, yyyymm, REV6]
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

print("Loading and processing REV6...")

# Prepare IBES earnings forecast data
ibes_df = pd.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")
ibes_df = ibes_df[ibes_df["fpi"] == "1"].copy()

# Create validity flag for forecasts beyond 30 days from statement period
ibes_df["tmp"] = np.where(
    (ibes_df["fpedats"].notna())
    & (ibes_df["fpedats"] > ibes_df["statpers"] + pd.Timedelta(days=30)),
    1,
    np.nan,
)

# Fill forward estimates when forecast periods match but validity flag missing
ibes_df = ibes_df.sort_values(["tickerIBES", "time_avail_m"])

# Stata explicitly uses [_n-1] here: retain observation-order forecast imputation.
# Create lagged values for conditional fill-forward logic
ibes_df["meanest_lag1"] = ibes_df.groupby("tickerIBES")["meanest"].shift(1)
ibes_df["fpedats_lag1"] = ibes_df.groupby("tickerIBES")["fpedats"].shift(1)

# Apply fill-forward when validity missing but forecast periods match
fill_condition = (
    pd.isna(ibes_df["tmp"])
    & (ibes_df["fpedats"] == ibes_df["fpedats_lag1"])
    & ibes_df["meanest_lag1"].notna()
)

# Execute conditional estimate replacement
ibes_df.loc[fill_condition, "meanest"] = ibes_df.loc[fill_condition, "meanest_lag1"]

# Remove intermediate calculation columns
ibes_df = ibes_df.drop(["meanest_lag1", "fpedats_lag1"], axis=1)
ibes_df = ibes_df.drop("tmp", axis=1)  # drop tmp

# Note: Missing data handled through conditional fill-forward only

# Load master security table with prices
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "tickerIBES", "time_avail_m", "prc"]].copy()

# Add earnings forecast data to master table
df = df.merge(
    ibes_df[["tickerIBES", "time_avail_m", "meanest"]],
    on=["tickerIBES", "time_avail_m"],
    how="left",
)

# Sort data by firm and time for panel calculations
df = df.sort_values(["permno", "time_avail_m"])

# Keep the complete monthly grid through both calendar-lag stages.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
for var in ("meanest", "prc"):
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [1], fill_gaps=False)

# Compute price-scaled forecast change
df["tempRev"] = (df["meanest"] - df["meanest_lag1"]) / np.abs(df["prc_lag1"])

df = stata_multi_lag(df, "permno", "time_avail_m", "tempRev", list(range(1, 7)), fill_gaps=False)
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()
# Require every monthly revision, including the current month.
rev6_cols = ["tempRev"] + [f"tempRev_lag{lag}" for lag in range(1, 7)]
df["REV6"] = df[rev6_cols].sum(axis=1, skipna=False)

# Format output variables
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month
df["permno"] = df["permno"].astype("int64")
df["yyyymm"] = df["yyyymm"].astype("int64")

df_final = df[["permno", "yyyymm", "REV6"]].copy()
df_final = df_final.dropna(subset=["REV6"])
df_final = df_final.set_index(["permno", "yyyymm"])

# Save predictor to CSV
df_final.to_csv("../pyData/Predictors/REV6.csv")
print("REV6 predictor saved successfully")
