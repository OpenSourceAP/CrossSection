# ABOUTME: Medium-run reversal following De Bondt and Thaler 1985, Fig2 two-year line
# ABOUTME: calculates stock return between months t-18 and t-13
"""
Usage:
    python3 Predictors/MRreversal.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with ret column

Outputs:
    - MRreversal.csv: CSV file with columns [permno, yyyymm, MRreversal]
    - MRreversal = geometric return over months t-18 to t-13 (medium-run reversal)
"""

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret"]].copy()

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Track originally missing returns
df["ret_orig_missing"] = df["ret"].isna()

# Replace missing returns with 0
df["ret"] = df["ret"].fillna(0).infer_objects(copy=False)


# Calculate lags for months 13-18 using calendar-based approach (matching Stata's l13.ret etc.)
# Use merge operations to efficiently create calendar-based lags
for lag in [13, 14, 15, 16, 17, 18]:
    # Create a copy for the lag data with shifted dates
    lag_df = df[["permno", "time_avail_m", "ret", "ret_orig_missing"]].copy()
    lag_df["time_avail_m"] = lag_df["time_avail_m"] + pd.DateOffset(months=lag)
    lag_df = lag_df.rename(
        columns={
            "ret": f"ret_lag{lag}",
            "ret_orig_missing": f"ret_lag{lag}_orig_missing",
        }
    )

    # Merge to get the lagged values
    df = df.merge(
        lag_df[
            ["permno", "time_avail_m", f"ret_lag{lag}", f"ret_lag{lag}_orig_missing"]
        ],
        on=["permno", "time_avail_m"],
        how="left",
    )

    # Fill missing lags with 0 (consistent with Stata behavior for missing)
    df[f"ret_lag{lag}"] = df[f"ret_lag{lag}"].fillna(0).infer_objects(copy=False)
    df[f"ret_lag{lag}_orig_missing"] = (
        df[f"ret_lag{lag}_orig_missing"].fillna(True).infer_objects(copy=False)
    )

# Calculate momentum-reversal (geometric return over months 13-18)
df["MRreversal"] = (
    (1 + df["ret_lag13"])
    * (1 + df["ret_lag14"])
    * (1 + df["ret_lag15"])
    * (1 + df["ret_lag16"])
    * (1 + df["ret_lag17"])
    * (1 + df["ret_lag18"])
) - 1

# Filter out observations where all lag values were originally missing
# This prevents spurious calculations with all-zero filled values
all_lags_missing = (
    df["ret_lag13_orig_missing"]
    & df["ret_lag14_orig_missing"]
    & df["ret_lag15_orig_missing"]
    & df["ret_lag16_orig_missing"]
    & df["ret_lag17_orig_missing"]
    & df["ret_lag18_orig_missing"]
)

# Set MRreversal to missing for problematic cases
df.loc[all_lags_missing, "MRreversal"] = np.nan


# Keep only necessary columns for output
df_final = df[["permno", "time_avail_m", "MRreversal"]].copy()
df_final = df_final.dropna(subset=["MRreversal"])

# Convert time_avail_m to yyyymm format like other predictors
df_final["yyyymm"] = (
    df_final["time_avail_m"].dt.year * 100 + df_final["time_avail_m"].dt.month
)

# Convert to integers for consistency with other predictors
df_final["permno"] = df_final["permno"].astype("int64")
df_final["yyyymm"] = df_final["yyyymm"].astype("int64")

# Keep only required columns and set index
df_final = df_final[["permno", "yyyymm", "MRreversal"]].copy()
df_final = df_final.set_index(["permno", "yyyymm"])


# SAVE
df_final.to_csv("../pyData/Predictors/MRreversal.csv")

print("MRreversal predictor saved successfully")
