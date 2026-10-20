# ABOUTME: Intermediate momentum following Novy-Marx 2012 Table 2
# ABOUTME: Stock returns between months t-12 and t-6 (intermediate horizon)

"""
IntMom.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/IntMom.py

Inputs:
    - SignalMasterTable.parquet: Signal master table with columns [permno, time_avail_m, ret]

Outputs:
    - IntMom.csv: CSV file with columns [permno, yyyymm, IntMom]
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")[
    ["permno", "time_avail_m", "ret"]
]

# SIGNAL CONSTRUCTION
# Replace missing returns with 0 for momentum calculations
df.loc[df["ret"].isna(), "ret"] = 0

# Convert time_avail_m to datetime for time-based lag calculations
df["time_avail_m"] = pd.to_datetime(df["time_avail_m"])

# Sort data for proper processing
df = df.sort_values(["permno", "time_avail_m"])

# Create time-based lags for months t-7 to t-12 (intermediate momentum period)

# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", [7, 8, 9, 10, 11, 12])
df = df.rename(columns={'ret_lag7': 'l7_ret', 'ret_lag8': 'l8_ret', 'ret_lag9': 'l9_ret', 'ret_lag10': 'l10_ret', 'ret_lag11': 'l11_ret', 'ret_lag12': 'l12_ret'})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Missing lagged values result in missing IntMom (consistent with methodology)

# Calculate intermediate momentum by compounding returns over months t-12 to t-6
df["IntMom"] = (
    (1 + df["l7_ret"])
    * (1 + df["l8_ret"])
    * (1 + df["l9_ret"])
    * (1 + df["l10_ret"])
    * (1 + df["l11_ret"])
    * (1 + df["l12_ret"])
) - 1

# Clean up temporary lagged variables
df = df.drop([f"l{lag}_ret" for lag in range(7, 13)], axis=1)

# SAVE
save_predictor(df, "IntMom")

print(f"Saved {len(df)} observations to IntMom.csv")
