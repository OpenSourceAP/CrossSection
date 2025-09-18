# ABOUTME: Change in Net Operating Assets following Hirshleifer, Hou, Teoh, Zhang 2004, Table 7B
# ABOUTME: calculates 12-month growth in Net Operating Assets scaled by lagged total assets

"""
dNoa Predictor - Change in Net Operating Assets

This predictor calculates the change in net operating assets scaled by lagged assets:
dNoa = (tempNOA - l12.tempNOA)/l12.at

Where:
- tempOA = at - che (Operating Assets = Total Assets - Cash)
- tempOL = at - tempdltt - tempmib - tempdlc - temppstk - ceq (Operating Liabilities)
- tempNOA = tempOA - tempOL (Net Operating Assets)

Inputs:
- m_aCompustat.parquet (permno, time_avail_m, at, che, dltt, dlc, mib, pstk, ceq)

Outputs:
- dNoa.csv (permno, yyyymm, dNoa)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

print("Starting dNoa predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "permno",
        "time_avail_m",
        "at",
        "che",
        "dltt",
        "dlc",
        "mib",
        "pstk",
        "ceq",
    ],
)

print(f"Loaded {len(df):,} m_aCompustat observations")

# Remove duplicates by keeping first observation per permno-month
print("Deduplicating by permno time_avail_m...")
df = df.sort_values(["permno", "time_avail_m"])
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing dNoa signal...")

# Sort data for panel operations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate operating assets (total assets minus cash)
df["tempOA"] = df["at"] - df["che"]

# Create temporary variables for debt and preferred stock components, filling missing values with zero
for var in ["dltt", "dlc", "mib", "pstk"]:
    df[f"temp{var}"] = df[var].fillna(0)

# Calculate operating liabilities
df["tempOL"] = (
    df["at"]
    - df["tempdltt"]
    - df["tempmib"]
    - df["tempdlc"]
    - df["temppstk"]
    - df["ceq"]
)

# Calculate net operating assets
df["tempNOA"] = df["tempOA"] - df["tempOL"]

# Calculate change in net operating assets scaled by lagged assets
# Create 12-month lags using time-based approach
df["time_lag12"] = pd.to_datetime(df["time_avail_m"]) - pd.DateOffset(months=12)

# Create lag data for merging
lag_data = df[["permno", "time_avail_m", "tempNOA", "at"]].copy()
lag_data["time_avail_m"] = pd.to_datetime(lag_data["time_avail_m"])
lag_data.columns = ["permno", "time_lag12", "tempNOA_lag12", "at_lag12"]

# Convert time_lag12 to datetime for consistent merging
df["time_lag12"] = pd.to_datetime(df["time_lag12"])

# Merge to get lagged values
df = df.merge(lag_data, on=["permno", "time_lag12"], how="left")

# Calculate dNoa with proper missing value handling
df["dNoa"] = np.where(
    (df["tempNOA_lag12"].isna()) | (df["at_lag12"].isna()) | (df["at_lag12"] == 0),
    np.nan,
    (df["tempNOA"] - df["tempNOA_lag12"]) / df["at_lag12"],
)

# Keep only observations with valid dNoa
df = df.dropna(subset=["dNoa"])
print(f"Generated dNoa values for {len(df):,} observations")

# Clean up extra columns for save
df = df[["permno", "time_avail_m", "dNoa"]].copy()

# SAVE
print("Saving predictor...")
save_predictor(df, "dNoa")

print("dNoa predictor completed successfully!")
