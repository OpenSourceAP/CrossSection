# ABOUTME: Change in Net Working Capital following Soliman 2008, Table 7 Model 2 DeltaWC
# ABOUTME: calculates twelve-month change in net working capital scaled by total assets

"""
ChNWC.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ChNWC.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, act, che, lct, dlc, at]

Outputs:
    - ../pyData/Predictors/ChNWC.csv: CSV file with columns [permno, yyyymm, ChNWC]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

print("Starting ChNWC predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "act", "che", "lct", "dlc", "at"],
)
print(f"Loaded {len(df):,} Compustat observations")

# SIGNAL CONSTRUCTION
print("Constructing ChNWC signal...")

# compute NWC
df["nwc_numerator"] = (df["act"] - df["che"]) - (df["lct"] - df["dlc"])
df.loc[df["at"] <= 0, "at"] = np.nan
df["NWC"] = df["nwc_numerator"] / df["at"]

# take first differences
# Create 12-month lag of working capital ratio
df = stata_multi_lag(df, "permno", "time_avail_m", "NWC", [12], prefix='l')
df["ChNWC"] = df["NWC"] - df["l12_NWC"]

print(f"Generated ChNWC values for {df['ChNWC'].notna().sum():,} observations")

# SAVE
print("Saving predictor...")
save_predictor(df, "ChNWC")

print("ChNWC predictor completed successfully!")
