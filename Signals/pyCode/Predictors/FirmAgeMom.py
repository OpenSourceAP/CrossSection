# ABOUTME: Firm Age-Momentum following Zhang 2006, Table 4, middle U5
# ABOUTME: calculates 6-month momentum for bottom quintile (youngest 20%) firms by age

# Inputs: SignalMasterTable.parquet
# Output: ../pyData/Predictors/FirmAgeMom.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

# DATA LOAD
df = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df[["permno", "time_avail_m", "ret", "prc"]].copy()

# SIGNAL CONSTRUCTION

# Replace missing returns with 0 for momentum calculations
df["ret"] = df["ret"].fillna(0)

# Generate firm age as months since first appearance in dataset
df = df.sort_values(["permno", "time_avail_m"])
df["age"] = df.groupby("permno").cumcount() + 1

# Filter: exclude stocks with price < $5 or less than 12 months of history
# Missing prices are retained (treated as passing price filter)
# TBC: consider moving price filter to the portfolio stage (caution: Zhang 2006 starts Section II by saying he excludes a bunch of stocks including price < $5)
price_condition = (df["prc"].abs() >= 5) | df["prc"].isna()
df = df[price_condition & (df["age"] >= 12)].copy()

# Calculate 6-month momentum (months t-5 to t-1) for youngest firms only
# Create lagged returns using calendar-based lags
df = stata_multi_lag(df, "permno", "time_avail_m", "ret", [1, 2, 3, 4, 5], prefix="l")

# Calculate FirmAgeMom
df["FirmAgeMom"] = (
    (1 + df["l1_ret"])
    * (1 + df["l2_ret"])
    * (1 + df["l3_ret"])
    * (1 + df["l4_ret"])
    * (1 + df["l5_ret"])
) - 1

# Identify bottom quintile (youngest 20%) of firms by age each month
df["age_quintile"] = df.groupby("time_avail_m")["age"].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates="drop") + 1
)

# Restrict signal to youngest quintile only - set others to missing
df.loc[(df["age_quintile"] > 1) | df["age_quintile"].isna(), "FirmAgeMom"] = np.nan

# SAVE
save_predictor(df, "FirmAgeMom")

print("FirmAgeMom predictor completed")
