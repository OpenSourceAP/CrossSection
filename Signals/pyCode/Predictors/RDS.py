# ABOUTME: Real Dirty Surplus following Landsman et al. 2011, Table 4
# ABOUTME: calculates real dirty surplus as change in book equity minus dirty surplus minus earnings plus dividends

"""
RDS.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/RDS.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, gvkey, time_avail_m, recta, ceq, ni, dvp, dvc, prcc_f, csho, msa]
    - CompustatPensions.parquet: Pension data with columns [gvkey, year, pcupsu, paddml]

Outputs:
    - RDS.csv: CSV file with columns [permno, yyyymm, RDS]
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# DATA LOAD
# Load m_aCompustat data
compustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "permno",
        "gvkey",
        "time_avail_m",
        "recta",
        "ceq",
        "ni",
        "dvp",
        "dvc",
        "prcc_f",
        "csho",
        "msa",
    ],
)

# Create year variable for pension data merge
compustat_df["year"] = compustat_df["time_avail_m"].dt.year

# Merge with CompustatPensions
pensions_df = pd.read_parquet(
    "../pyData/Intermediate/CompustatPensions.parquet",
    columns=["gvkey", "year", "pcupsu", "paddml"],
)
df = compustat_df.merge(pensions_df, on=["gvkey", "year"], how="left")

# SIGNAL CONSTRUCTION
# Sort data for lag operations
df = df.sort_values(["permno", "time_avail_m"])

# Track which values were originally missing to handle edge cases
df["recta_orig_missing"] = df["recta"].isna()
df["msa_orig_missing"] = df["msa"].isna()

# Replace missing recta and msa with 0
df["recta"] = df["recta"].fillna(0)
df["msa"] = df["msa"].fillna(0)

# Fill once after current-value imputation; absent calendar endpoints stay missing.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
lag_vars = ["msa", "recta", "pcupsu", "paddml", "ceq", "csho",
            "recta_orig_missing", "msa_orig_missing"]
for var in lag_vars:
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [12], prefix="l", fill_gaps=False)
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()


# Calculate dirty surplus (DS)
# min(pcupsu - paddml, 0) - min(l12.pcupsu - l12.paddml, 0)
# Handle missing pension data by treating as 0 in the min() function
def min_pension(pcupsu, paddml):
    if pd.isna(pcupsu) or pd.isna(paddml):
        return 0  # Treat missing pension data as 0 in min() function
    return min(pcupsu - paddml, 0)


pension_current = df.apply(
    lambda row: min_pension(row["pcupsu"], row["paddml"]), axis=1
)
pension_lag = df.apply(
    lambda row: min_pension(row["l12_pcupsu"], row["l12_paddml"]), axis=1
)

# Note: msa and recta are already filled with 0 above for current values
# But we should NOT fill lag values - let NaN propagate naturally
df["DS"] = (
    (df["msa"] - df["l12_msa"])
    + (df["recta"] - df["l12_recta"])
    + 0.65 * (pension_current - pension_lag)
)

# Calculate RDS
df["RDS"] = (
    (df["ceq"] - df["l12_ceq"])
    - df["DS"]
    - (df["ni"] - df["dvp"])
    + df["dvc"]
    - df["prcc_f"] * (df["csho"] - df["l12_csho"])
)

# Filter out observations where both current and lagged msa/recta were originally missing
# This prevents meaningless 0-0=0 calculations
both_missing_mask = (
    df["recta_orig_missing"]
    & df["l12_recta_orig_missing"].fillna(True).infer_objects(copy=False)
) & (
    df["msa_orig_missing"]
    & df["l12_msa_orig_missing"].fillna(True).infer_objects(copy=False)
)

# Set RDS to missing for these problematic cases
df.loc[both_missing_mask, "RDS"] = np.nan

# Drop missing values
df = df.dropna(subset=["RDS"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "RDS"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/RDS.csv", index=False)
print(f"RDS: Saved {len(df):,} observations")
