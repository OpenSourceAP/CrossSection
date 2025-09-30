# ABOUTME: Order backlog following Rajgopal, Shevlin, Venkatachalam 2003, Table 3A gamma1
# ABOUTME: calculates order backlog predictor scaled by average total assets

"""
OrderBacklog.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/OrderBacklog.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, ob, at]

Outputs:
    - OrderBacklog.csv: CSV file with columns [permno, yyyymm, OrderBacklog]
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
df = df[["gvkey", "permno", "time_avail_m", "ob", "at"]].copy()

# SIGNAL CONSTRUCTION
# Remove duplicates (deletes a few observations)
df = df.drop_duplicates(["permno", "time_avail_m"])

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Create 12-month lag of at
df["at_lag12"] = df.groupby("permno")["at"].shift(12)

# Calculate OrderBacklog = ob / (0.5 * (at + l12.at))
df["OrderBacklog"] = df["ob"] / (0.5 * (df["at"] + df["at_lag12"]))

# Replace with missing if ob == 0
df.loc[df["ob"] == 0, "OrderBacklog"] = np.nan

# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "OrderBacklog"]].copy()
df_final = df_final.dropna(subset=["OrderBacklog"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "OrderBacklog"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])

# SAVE
df_final.to_csv("../pyData/Predictors/OrderBacklog.csv")

print("OrderBacklog predictor saved successfully")
