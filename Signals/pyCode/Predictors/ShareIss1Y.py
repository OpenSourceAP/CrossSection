# ABOUTME: Share issuance (1 year) following Pontiff and Woodgate 2008, Table 3A ISSUE
# ABOUTME: calculates growth in number of shares between t-18 and t-6 months

"""
Usage:
    python3 Predictors/ShareIss1Y.py

Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet: Monthly master table
    - ../pyData/Intermediate/monthlyCRSP.parquet: Monthly CRSP data with shrout, cfacshr

Outputs:
    - ../pyData/Predictors/ShareIss1Y.csv: CSV file with columns [permno, yyyymm, ShareIss1Y]
    - ShareIss1Y = (shares_t-6 - shares_t-18) / shares_t-18, where shares = shrout * cfacshr
"""

# Note: We tried constructing the share adjustment from facshr as described in Pontiff and Woodgate (2008). Results are almost identical. So we stick with the simpler implementation
# by using cfacshr directly.
# Note that the signal does not suffer from look-ahead bias despite using cfacshr,
# see https://github.com/OpenSourceAP/CrossSection/issues/152#issue-2462197349

import pandas as pd
import numpy as np

print("Starting ShareIss1Y calculation...")

# DATA LOAD
# Load signal master table
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m"],
)

# Merge with monthly CRSP data
monthly_crsp = pd.read_parquet(
    "../pyData/Intermediate/monthlyCRSP.parquet",
    columns=["permno", "time_avail_m", "shrout", "cfacshr"],
)
df = pd.merge(
    signal_master,
    monthly_crsp,
    on=["permno", "time_avail_m"],
    how="inner",
    validate="1:1",
)

print(f"After merge: {len(df)} observations")

# SIGNAL CONSTRUCTION
# Calculate adjusted shares outstanding
df["temp"] = df["shrout"] * df["cfacshr"]

# Sort for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Get historical values from 6 and 18 months ago
df["time_lag6"] = df["time_avail_m"] - pd.DateOffset(months=6)
df["time_lag18"] = df["time_avail_m"] - pd.DateOffset(months=18)

# Create lag data for merging
lag6_data = df[["permno", "time_avail_m", "temp"]].copy()
lag6_data.columns = ["permno", "time_lag6", "l6_temp"]

lag18_data = df[["permno", "time_avail_m", "temp"]].copy()
lag18_data.columns = ["permno", "time_lag18", "l18_temp"]

# Merge to get lagged values
df = df.merge(lag6_data, on=["permno", "time_lag6"], how="left")
df = df.merge(lag18_data, on=["permno", "time_lag18"], how="left")

# Calculate 1-year share issuance as percentage change in shares
df["ShareIss1Y"] = (df["l6_temp"] - df["l18_temp"]) / df["l18_temp"]

print(f"ShareIss1Y calculated for {df['ShareIss1Y'].notna().sum()} observations")

# SAVE
# Save predictor output
result = df[["permno", "time_avail_m", "ShareIss1Y"]].copy()
result = result.dropna(subset=["ShareIss1Y"])

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)
result = result[["permno", "yyyymm", "ShareIss1Y"]].copy()

# Convert to integers where appropriate
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv("../pyData/Predictors/ShareIss1Y.csv", index=False)
print("ShareIss1Y.csv saved successfully")
