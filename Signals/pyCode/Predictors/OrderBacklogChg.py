# ABOUTME: Change in Order Backlog predictor from Baik and Ahn 2007, Table 2 High-Low
# ABOUTME: Calculates change in normalized order backlog (order backlog divided by average total assets)

"""
OrderBacklogChg.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/OrderBacklogChg.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ob, at]

Outputs:
    - OrderBacklogChg.csv: CSV file with columns [permno, yyyymm, OrderBacklogChg]
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[["gvkey", "permno", "time_avail_m", "ob", "at"]].copy()

# SIGNAL CONSTRUCTION
df = df.drop_duplicates(subset=["permno", "time_avail_m"])
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lag of assets
# Keep the full monthly grid until all calendar lags are calculated.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
df = stata_multi_lag(df, "permno", "time_avail_m", "at", [12], fill_gaps=False)

# Calculate OrderBacklog
df["OrderBacklog"] = df["ob"] / (0.5 * (df["at"] + df["at_lag12"]))
df.loc[df["ob"] == 0, "OrderBacklog"] = np.nan

# Calculate 12-month lag of OrderBacklog
df = stata_multi_lag(df, "permno", "time_avail_m", "OrderBacklog", [12], fill_gaps=False)
# Preserve the source observation set before subsequent calculations.
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()

# Calculate OrderBacklogChg
df["OrderBacklogChg"] = df["OrderBacklog"] - df["OrderBacklog_lag12"]

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "OrderBacklogChg"]].copy()
df_final = df_final.dropna(subset=["OrderBacklogChg"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "OrderBacklogChg"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/OrderBacklogChg.csv")

print("OrderBacklogChg predictor saved successfully")
