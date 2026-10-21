# ABOUTME: Earnings Surprise following Foster, Olsen and Shevlin 1984 AR, Table 4, Days +1 to +60
# ABOUTME: Calculates standardized unexpected earnings scaled by standard deviation

"""
EarningsSurprise.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/EarningsSurprise.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, gvkey, time_avail_m]
    - m_QCompustat.parquet: Quarterly Compustat data with columns [gvkey, time_avail_m, epspxq]

Outputs:
    - EarningsSurprise.csv: CSV file with columns [permno, yyyymm, EarningsSurprise]
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import stata_multi_lag
import numpy as np

# DATA LOAD
# Load SignalMasterTable with specific columns
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m"],
)

# Filter to observations with valid gvkey identifiers
df = df.dropna(subset=["gvkey"])

# Merge with quarterly Compustat data to get earnings per share
qcompustat = pd.read_parquet(
    "../pyData/Intermediate/m_QCompustat.parquet",
    columns=["gvkey", "time_avail_m", "epspxq"],
)

df = df.merge(qcompustat, on=["gvkey", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Sort data by company and time for time series operations
df = df.sort_values(["permno", "time_avail_m"])

# Calculate quarterly earnings growth over 12-month period
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "epspxq", [12])
df = df.rename(columns={'epspxq_lag12': 'epspxq_l12'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

df["GrTemp"] = df["epspxq"] - df["epspxq_l12"]

# Create lagged earnings growth values at 3-month intervals for drift calculation
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "GrTemp", [3, 6, 9, 12, 15, 18, 21, 24])
df = df.rename(columns={'GrTemp_lag3': 'grtemp_lag3', 'GrTemp_lag6': 'grtemp_lag6', 'GrTemp_lag9': 'grtemp_lag9', 'GrTemp_lag12': 'grtemp_lag12', 'GrTemp_lag15': 'grtemp_lag15', 'GrTemp_lag18': 'grtemp_lag18', 'GrTemp_lag21': 'grtemp_lag21', 'GrTemp_lag24': 'grtemp_lag24'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate average earnings growth over past 8 quarters (drift component)
grtemp_lag_cols = [f"grtemp_lag{n}" for n in range(3, 25, 3)]
df["Drift"] = df[grtemp_lag_cols].mean(axis=1)

# Calculate earnings surprise as growth minus historical drift
df["EarningsSurprise"] = df["epspxq"] - df["epspxq_l12"] - df["Drift"]

# Drop grtemp lag columns
df = df.drop(columns=grtemp_lag_cols)

# Create lagged earnings surprise values for volatility calculation
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "EarningsSurprise", [3, 6, 9, 12, 15, 18, 21, 24])
df = df.rename(columns={'EarningsSurprise_lag3': 'es_lag3', 'EarningsSurprise_lag6': 'es_lag6', 'EarningsSurprise_lag9': 'es_lag9', 'EarningsSurprise_lag12': 'es_lag12', 'EarningsSurprise_lag15': 'es_lag15', 'EarningsSurprise_lag18': 'es_lag18', 'EarningsSurprise_lag21': 'es_lag21', 'EarningsSurprise_lag24': 'es_lag24'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate standard deviation of historical earnings surprises
es_lag_cols = [f"es_lag{n}" for n in range(3, 25, 3)]
df["SD"] = df[es_lag_cols].std(axis=1, ddof=1)

# Standardize earnings surprise by dividing by historical volatility
df["EarningsSurprise"] = df["EarningsSurprise"] / df["SD"]
# Replace infinite values with missing when standard deviation is zero
df["EarningsSurprise"] = df["EarningsSurprise"].replace([np.inf, -np.inf], np.nan)

# Keep only observations with valid standardized earnings surprise
df = df.dropna(subset=["EarningsSurprise"])
# Remove observations with missing or near-zero standard deviation
df = df.dropna(subset=["SD"])
df = df[df["SD"] > 1e-10]

# Keep only required columns for final output
result = df[["permno", "time_avail_m", "EarningsSurprise"]].copy()

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)

# Final output format
result = result[["permno", "yyyymm", "EarningsSurprise"]]

# Convert permno and yyyymm to int
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

# SAVE
result.to_csv("../pyData/Predictors/EarningsSurprise.csv", index=False)

print(f"EarningsSurprise predictor created with {len(result)} observations")
