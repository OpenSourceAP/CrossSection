# ABOUTME: Decline in Analyst Coverage following Scherbina 2008, Table 2 alphas return diff
# ABOUTME: calculates binary predictor for decrease in analyst coverage relative to three months ago

"""
ChNAnalyst.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/ChNAnalyst.py

Inputs:
    - ../pyData/Intermediate/IBES_EPS_Unadj.parquet
    - ../pyData/Intermediate/SignalMasterTable.parquet

Outputs:
    - ../pyData/Predictors/ChNAnalyst.csv (columns: permno, yyyymm, ChNAnalyst)
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

# Load IBES earnings per share data
ibes_df = pd.read_parquet("../pyData/Intermediate/IBES_EPS_Unadj.parquet")

# Filter to annual forecasts only
ibes_df = ibes_df[ibes_df["fpi"] == "1"].copy()

# Create indicator for valid forecasts (end date exists and is at least 30 days after statement period)
ibes_df["tmp"] = np.where(
    ibes_df["fpedats"].notna()
    & (ibes_df["fpedats"] > ibes_df["statpers"] + pd.Timedelta(days=30)),
    1,
    np.nan,
)

# For invalid forecasts with same end date as previous record, use previous mean estimate
ibes_df = ibes_df.sort_values(["tickerIBES", "time_avail_m"])
ibes_df["meanest_lag1"] = ibes_df.groupby("tickerIBES")["meanest"].shift(1)
ibes_df["fpedats_lag1"] = ibes_df.groupby("tickerIBES")["fpedats"].shift(1)

mask_replace = ibes_df["tmp"].isna() & (ibes_df["fpedats"] == ibes_df["fpedats_lag1"])
ibes_df.loc[mask_replace, "meanest"] = ibes_df.loc[mask_replace, "meanest_lag1"]

# Clean up temporary variables
ibes_df = ibes_df.drop(columns=["tmp", "meanest_lag1", "fpedats_lag1"])

# Keep only required analyst coverage variables
temp_ibes = ibes_df[
    ["tickerIBES", "time_avail_m", "numest", "statpers", "fpedats"]
].copy()

# Load master table with stock identifiers and market values
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "tickerIBES", "mve_c"],
)

# Merge in analyst coverage data by ticker and month
df = pd.merge(df, temp_ibes, on=["tickerIBES", "time_avail_m"], how="left")

# Sort data for time series operations
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Calculate 3-month lagged analyst coverage using stata_multi_lag
df = stata_multi_lag(df, "permno", "time_avail_m", "numest", [3])
df = df.rename(columns={"numest_lag3": "numest_l3"})
df["ChNAnalyst"] = np.nan

# Set indicator to 1 if current analyst count is less than 3 months ago
mask_decline = (df["numest"] < df["numest_l3"]) & df["numest_l3"].notna()
df.loc[mask_decline, "ChNAnalyst"] = 1

# Set indicator to 0 if current analyst count is greater than or equal to 3 months ago
mask_no_decline = (df["numest"] >= df["numest_l3"]) & df["numest"].notna()
df.loc[mask_no_decline, "ChNAnalyst"] = 0

# Exclude data from July-September 1987 due to data quality issues (OP tab 2)
mask_1987 = (df["time_avail_m"] >= pd.Timestamp("1987-07-01")) & (
    df["time_avail_m"] <= pd.Timestamp("1987-09-01")
)
df.loc[mask_1987, "ChNAnalyst"] = np.nan

# Only works in small firms (OP tab 2)
# this is the correct way to do it
df["tempqsize"] = df.groupby("time_avail_m")["mve_c"].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop") + 1
)

# this way replicates `ChNAnalyst.do`
# df['tempqsize'] = (
#     df['mve_c'].transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1)
# )

# Keep only smallest two quintiles (small firms)
df = df[df["tempqsize"] <= 2].copy()

# Keep only needed columns and save
result = df[["permno", "time_avail_m", "ChNAnalyst"]].copy()
save_predictor(result, "ChNAnalyst")
