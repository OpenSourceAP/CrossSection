# ABOUTME: Change in Asset Turnover following Soliman 2008, Table 7, Model 1 DeltaATO
# ABOUTME: calculates annual change in asset turnover predictor (sales growth economic category)

"""
ChAssetTurnover.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChAssetTurnover.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (columns: gvkey, permno, time_avail_m, rect, invt, aco, ppent, intan, ap, lco, lo, sale)

Outputs:
    - ../pyData/Predictors/ChAssetTurnover.csv (columns: permno, yyyymm, ChAssetTurnover)
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag
import numpy as np
from pathlib import Path

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "gvkey",
        "permno",
        "time_avail_m",
        "rect",
        "invt",
        "aco",
        "ppent",
        "intan",
        "ap",
        "lco",
        "lo",
        "sale",
    ],
)

# SIGNAL CONSTRUCTION
# Remove duplicate permno-month observations, keeping first occurrence
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first").copy()

# Sort by permno and time for panel data operations
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Forward-fill missing ppent values within each permno group
df["ppent"] = df.groupby("permno")["ppent"].ffill()

# Calculate total assets: current assets + fixed assets - current liabilities - other liabilities
df["temp"] = (
    df["rect"]
    + df["invt"]
    + df["aco"]
    + df["ppent"]
    + df["intan"]
    - df["ap"]
    - df["lco"]
    - df["lo"]
)

# Calculate asset turnover as sales divided by average total assets over 12 months
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "temp", [12])
df = df.rename(columns={'temp_lag12': 'temp_l12'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

df["AssetTurnover"] = df["sale"] / ((df["temp"] + df["temp_l12"]) / 2)

# Remove temporary variables
df = df.drop(columns=["temp", "temp_l12"])

# Set negative asset turnover values to missing
df.loc[df["AssetTurnover"] < 0, "AssetTurnover"] = np.nan

# Calculate change in asset turnover as current minus 12-month lagged value
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "AssetTurnover", [12])
df = df.rename(columns={'AssetTurnover_lag12': 'AssetTurnover_l12'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

df["ChAssetTurnover"] = df["AssetTurnover"] - df["AssetTurnover_l12"]

# Keep only needed columns and non-missing values
result = df[["permno", "time_avail_m", "ChAssetTurnover"]].copy()
result = result.dropna(subset=["ChAssetTurnover"]).copy()

# Convert time_avail_m to yyyymm
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Prepare final output
final_result = result[["permno", "yyyymm", "ChAssetTurnover"]].copy()

# SAVE
Path("../pyData/Predictors").mkdir(parents=True, exist_ok=True)
final_result.to_csv("../pyData/Predictors/ChAssetTurnover.csv", index=False)

print(f"ChAssetTurnover predictor saved: {len(final_result)} observations")
