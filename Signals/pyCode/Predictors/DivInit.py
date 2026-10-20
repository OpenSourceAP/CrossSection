#%% debug
import os
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

# ABOUTME: Dividend initiation following Michaely, Thaler and Womack 1995, Table 3 init
# ABOUTME: Identifies firms that paid dividends after 24 months of no dividends, held for 6 months

"""
DivInit.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/DivInit.py

Inputs:
    - CRSPdistributions.parquet: CRSP distributions data with columns [permno, exdt, cd2, divamt]
    - SignalMasterTable.parquet: Signal master table with columns [permno, time_avail_m, exchcd, shrcd]

Outputs:
    - DivInit.csv: CSV file with columns [permno, yyyymm, DivInit]
"""

import pandas as pd
import numpy as np
import sys
import os
import sys

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.asrol import asrol
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

print("=" * 80)
print("🏗️  DivInit.py")
print("Creating dividend initiation predictor")
print("=" * 80)

# PREP DISTRIBUTIONS DATA
print("📊 Loading distributions data...")
dist_df = pd.read_parquet("../pyData/Intermediate/CRSPdistributions.parquet")
print(f"Loaded distributions: {len(dist_df):,} observations")

# Cash dividends only (cd2 == 2 | cd2 == 3)
dist_df = dist_df[(dist_df["cd2"] == 2) | (dist_df["cd2"] == 3)]

# Collapse by exdt: this date tends to come first
dist_df["time_avail_m"] = pd.to_datetime(
    dist_df["exdt"].dt.to_period("M").dt.start_time
)
dist_df = dist_df.dropna(subset=["time_avail_m", "divamt"])

# Sum dividends by permno and time_avail_m
tempdivamt = dist_df.groupby(["permno", "time_avail_m"])["divamt"].sum().reset_index()

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "exchcd", "shrcd"]].copy()

# Merge with dividend amounts
df = df.merge(tempdivamt, on=["permno", "time_avail_m"], how="left")

# SIGNAL CONSTRUCTION
print("🧮 Computing dividend initiation signal...")
# Replace missing dividend amounts with 0
df["divamt"] = df["divamt"].fillna(0)

# Rolling 24-month sum of dividends using asrol
df["_observed_rolling"] = True
df = asrol(
    df, "permno", "time_avail_m", "1mo", 24, "divamt", "sum", "divamt_sum", min_samples=1
)
df = df.loc[df["_observed_rolling"].eq(True)].drop(columns="_observed_rolling")

# Sort by permno and time_avail_m for lag calculation
df = df.sort_values(["permno", "time_avail_m"])

# Create dividend initiation indicator
# Flag firms paying dividends after 24 months of no dividends
# for some reason, asrol(stat="sum") can return 1e-17 instead of 0. This seems to be due to how polars handles rolling_sum. So I'm patching with this 1e-10 cutoff
# Fill calendar gaps for lags, then restore the observed rows.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "time_avail_m", "divamt_sum", [1])
df = df.rename(columns={"divamt_sum_lag1": "divsum_lag1"})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")
df["divinit_firstmonth"] = ((df["divamt"] > 0) & (df["divsum_lag1"] < 1e-10)).astype(int)

# Signal is valid for 6 months
df["_observed_rolling"] = True
df = asrol(
    df, "permno", "time_avail_m", "1mo", 6, "divinit_firstmonth", 
    "max", "DivInit", min_samples=1
)
df = df.loc[df["_observed_rolling"].eq(True)].drop(columns="_observed_rolling")

# save
print("💾 Saving DivInit predictor...")
save_predictor(df, "DivInit")
print("✅ DivInit.csv saved successfully")

#%% debug

small = df.query("permno == 10372 & time_avail_m <= '1936-12-31'")