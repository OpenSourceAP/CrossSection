# ABOUTME: Net debt financing following Bradshaw, Richardson, Sloan 2006, Table 3
# ABOUTME: calculates net debt financing activity scaled by average total assets

"""
NetDebtFinance.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/NetDebtFinance.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, dlcch, dltis, dltr, at]

Outputs:
    - NetDebtFinance.csv: CSV file with columns [permno, yyyymm, NetDebtFinance]
"""

import pandas as pd
import numpy as np

print("Starting NetDebtFinance calculation...")

# DATA LOAD
# use gvkey permno time_avail_m dlcch dltis dltr at using "$pathDataIntermediate/m_aCompustat", clear
m_aCompustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "permno", "time_avail_m", "dlcch", "dltis", "dltr", "at"],
)
df = m_aCompustat.copy()
print(f"Loaded m_aCompustat data: {len(df)} observations")

# SIGNAL CONSTRUCTION
# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.drop_duplicates(subset=["permno", "time_avail_m"], keep="first")
print(f"After deduplicating by permno time_avail_m: {len(df)} observations")

# xtset permno time_avail_m
df = df.sort_values(["permno", "time_avail_m"])

# Update 0 if mi(dlcch)
df["dlcch"] = df["dlcch"].fillna(0)

# Generate (dltis - dltr + dlcch)/(.5*(at + l12.at))
# Create 12-month lag of at
df["l12_at"] = df.groupby("permno")["at"].shift(12)

# Calculate NetDebtFinance
df["NetDebtFinance"] = (df["dltis"] - df["dltr"] + df["dlcch"]) / (
    0.5 * (df["at"] + df["l12_at"])
)

# Update . if abs(NetDebtFinance) > 1
df.loc[df["NetDebtFinance"].abs() > 1, "NetDebtFinance"] = np.nan

print(
    f"NetDebtFinance calculated for {df['NetDebtFinance'].notna().sum()} observations"
)

# SAVE
# do "$pathCode/savepredictor" NetDebtFinance
result = df[["permno", "time_avail_m", "NetDebtFinance"]].copy()
result = result.dropna(subset=["NetDebtFinance"])

# Convert time_avail_m to yyyymm format
result["yyyymm"] = (
    result["time_avail_m"].dt.year * 100 + result["time_avail_m"].dt.month
)
result = result[["permno", "yyyymm", "NetDebtFinance"]].copy()

# Convert to integers where appropriate
result["permno"] = result["permno"].astype(int)
result["yyyymm"] = result["yyyymm"].astype(int)

print(f"Final output: {len(result)} observations")
result.to_csv("../pyData/Predictors/NetDebtFinance.csv", index=False)
print("NetDebtFinance.csv saved successfully")
