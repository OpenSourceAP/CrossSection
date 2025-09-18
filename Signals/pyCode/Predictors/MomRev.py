# ABOUTME: Calculates momentum and long-term reversal signal following Chan and Ko 2006 Table 5
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomRev.py
# Run from pyCode/ directory: python3 Predictors/MomRev.py
# Inputs: pyData/Intermediate/SignalMasterTable.parquet
# Outputs: pyData/Predictors/MomRev.csv

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import stata_multi_lag
from utils.save_standardized import save_predictor

print("=" * 80)
print("🏗️  MomRev.py")
print("Creating momentum and long-term reversal signal based on 6m and 36m momentum")
print("=" * 80)

# DATA LOAD
print("📊 Loading SignalMasterTable data...")
# Load return data for momentum calculations
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")[
    ["permno", "time_avail_m", "ret"]
].copy()
print(f"Loaded: {len(df):,} observations")

# Sort data for proper lag operations
df = df.sort_values(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
print("🧮 Computing 6m and 36m momentum signals...")
# Replace missing returns with 0 for momentum calculations
df.loc[df["ret"].isna(), "ret"] = 0

# Create lag variables using stata_multi_lag for calendar validation
# Mom6m uses lags 1-5
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", [1, 2, 3, 4, 5])

# Compounds monthly returns over months t-5 to t-1 to create 6-month momentum
df["Mom6m"] = (
    (1 + df["ret_lag1"])
    * (1 + df["ret_lag2"])
    * (1 + df["ret_lag3"])
    * (1 + df["ret_lag4"])
    * (1 + df["ret_lag5"])
) - 1

# Mom36m uses lags 13-36 (skips recent 12 months)
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", list(range(13, 37)))

# Compounds monthly returns over months t-36 to t-13 to create long-term momentum
mom36m_product = 1
for i in range(13, 37):
    mom36m_product *= 1 + df[f"ret_lag{i}"]
df["Mom36m"] = mom36m_product - 1


# Handle infinite values before quintile calculation
df["Mom6m_clean"] = df["Mom6m"].replace([np.inf, -np.inf], np.nan)
df["Mom36m_clean"] = df["Mom36m"].replace([np.inf, -np.inf], np.nan)

# Ranks stocks into quintiles (1-5) within each month based on 6-month momentum
# old code: df['tempMom6'] = fastxtile(df, 'Mom6m_clean', by='time_avail_m', n=5)
df["tempMom6"] = df.groupby("time_avail_m")["Mom6m"].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop") + 1
)


# Ranks stocks into quintiles (1-5) within each month based on 36-month momentum
# old code: df['tempMom36'] = fastxtile(df, 'Mom36m_clean', by='time_avail_m', n=5)
df["tempMom36"] = df.groupby("time_avail_m")["Mom36m"].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop") + 1
)


# Goes long (MomRev = 1) stocks in top quintile for 6m momentum AND bottom quintile for 36m momentum
# Goes short (MomRev = 0) stocks in bottom quintile for 6m momentum AND top quintile for 36m momentum
df["MomRev"] = np.nan
df.loc[(df["tempMom6"] == 5) & (df["tempMom36"] == 1), "MomRev"] = 1
df.loc[(df["tempMom6"] == 1) & (df["tempMom36"] == 5), "MomRev"] = 0


# label var MomRev "Momentum and LT Reversal"
# (Labels are comments in Python)

# SAVE
print("💾 Saving MomRev predictor...")
save_predictor(df, "MomRev")
print("✅ MomRev.csv saved successfully")

print("=" * 80)
print("✅ MomRev.py Complete")
print("Momentum and long-term reversal signal generated successfully")
print("=" * 80)
