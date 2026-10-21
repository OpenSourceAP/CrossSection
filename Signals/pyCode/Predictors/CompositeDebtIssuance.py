# ABOUTME: Composite debt issuance following Lyandres, Sun and Zhang 2008, Table 5B
# ABOUTME: calculates log of total debt minus log of total debt 5 years ago

"""
CompositeDebtIssuance.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/CompositeDebtIssuance.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, dltt, dlc]

Outputs:
    - CompositeDebtIssuance.csv: CSV file with columns [permno, yyyymm, CompositeDebtIssuance]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag

print("Starting CompositeDebtIssuance predictor...")

# DATA LOAD
print("Loading m_aCompustat data...")
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "dltt", "dlc"],
)

print(f"Loaded {len(df):,} Compustat observations")

# SIGNAL CONSTRUCTION
print("Constructing CompositeDebtIssuance signal...")

# Deduplicate by permno time_avail_m
df = df.drop_duplicates(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(df):,} observations")

# Sort by permno and time_avail_m
df = df.sort_values(["permno", "time_avail_m"])

# Calculate total debt
df["tempBD"] = df["dltt"] + df["dlc"]

# Create 60-month lag using calendar-based calculation
print("Calculating 60-month calendar-based lag...")

# Fill the monthly calendar before lagging; missing target months and debt
# values stay missing. Remove inserted months to preserve the observed panel.
df["_observed"] = True
df = stata_multi_lag(
    df, "permno", "time_avail_m", "tempBD", [60], prefix="l"
)
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Calculate composite debt issuance as log growth in total debt over 60 months
# Stata's log(x/0) and log(0) are missing; numpy returns +/-inf. Match Stata so that
# firms with zero total debt now or 60 months ago are dropped rather than kept as inf.
with np.errstate(divide="ignore", invalid="ignore"):
    df["CompositeDebtIssuance"] = np.log(df["tempBD"] / df["l60_tempBD"])
df["CompositeDebtIssuance"] = df["CompositeDebtIssuance"].replace([np.inf, -np.inf], np.nan)

print(
    f"Generated CompositeDebtIssuance values for {df['CompositeDebtIssuance'].notna().sum():,} observations"
)

# Clean up temporary columns
df = df.drop(columns=["tempBD", "l60_tempBD"])

# SAVE
print("Saving predictor...")
save_predictor(df, "CompositeDebtIssuance")

print("CompositeDebtIssuance predictor completed successfully!")
