# ABOUTME: Organizational capital following Eisfeldt and Papanikolaou 2013, Table 4A.1
# ABOUTME: Calculates OrgCap (industry-adjusted) and OrgCapNoAdj (raw) based on SG&A with depreciation

"""
ZZ1_OrgCap_OrgCapNoAdj.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ZZ1_OrgCap_OrgCapNoAdj.py

Inputs:
    - SignalMasterTable.parquet: Permno, time_avail_m, sicCRSP, shrcd, exchcd
    - m_aCompustat.parquet: Permno, time_avail_m, xsga, at, datadate, sic
    - GNPdefl.parquet: Time_avail_m, gnpdefl

Outputs:
    - OrgCap.csv: CSV file with columns [permno, yyyymm, OrgCap]
    - OrgCapNoAdj.csv: CSV file with columns [permno, yyyymm, OrgCapNoAdj]
"""

import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor, save_placebo
from utils.sicff import sicff
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# DATA LOAD
print("Loading data files...")
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "sicCRSP", "shrcd", "exchcd"],
)

compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "time_avail_m", "xsga", "at", "datadate", "sic"],
)

gnpdefl = pd.read_parquet(
    "../pyData/Intermediate/GNPdefl.parquet", columns=["time_avail_m", "gnpdefl"]
)

# Merge datasets
df = pd.merge(signal_master, compustat, on=["permno", "time_avail_m"], how="left")
df = pd.merge(df, gnpdefl, on="time_avail_m", how="inner")

# Convert sic to numeric
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Keep December fiscal year end only, and then fill the date gaps
df = df[df["datadate"].dt.month == 12]

# Fill NA for sicCRSP with last non-missing value by permno
# This was not in Stata, but it makes sense.
df['sic'] = df.groupby('permno')['sic'].ffill()
df['sicCRSP'] = df.groupby('permno')['sicCRSP'].ffill()

# Create variables
df["age"] = df.groupby("permno").cumcount() + 1
df["xsga"] = df["xsga"].fillna(0)
df["xsga"] = df["xsga"] / df["gnpdefl"]

# Define the orgcap recursive function
def build_orgcap(group, a=0.85):
    xsga = group['xsga'].to_numpy(dtype=float)
    n = xsga.size
    y = np.full(n, np.nan)

    period = 12

    # initialization: first period obs per permno -> 4 * xsga
    k = min(period, n)
    y[:k] = 4.0 * xsga[:k]

    # recursive step: y[t] = a * y[t-period] + xsga[t]
    for i in range(period, n):
            y[i] = a * y[i-period] + xsga[i]

    group['OrgCapNoAdj'] = y
    return group


# Apply the orgcap recursive function
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
df = df.groupby('permno', group_keys=False)[
    ['permno', 'time_avail_m', 'xsga', 'at', 'sicCRSP']
].apply(build_orgcap)

# Scale by total assets
df.loc[df["at"] == 0, "at"] = np.nan
df["OrgCapNoAdj"] = df["OrgCapNoAdj"] / df["at"]

# Set zero values to missing
df.loc[df["OrgCapNoAdj"] == 0, "OrgCapNoAdj"] = np.nan

print(
    f"After OrgCapNoAdj calculation: {df['OrgCapNoAdj'].notna().sum():,} non-missing values"
)

# INDUSTRY ADJUSTMENT
# Winsorize by time_avail_m at 1% and 99%
def winsorize_by_time(group):
    """Winsorize a column within each time group"""
    if group.isna().all() or len(group.dropna()) <= 1:
        return group

    # Only consider non-missing values for quantile calculation
    non_missing = group.dropna()

    # Calculate percentiles for winsorization bounds
    lower_bound = np.percentile(non_missing, 1, method="lower")
    upper_bound = np.percentile(non_missing, 99, method="higher")

    # Apply winsorization to all values (including missing)
    return group.clip(lower=lower_bound, upper=upper_bound)


df["OrgCapNoAdjtemp"] = df.groupby("time_avail_m")["OrgCapNoAdj"].transform(
    winsorize_by_time
)

# Create Fama-French 17 industry classification from sicCRSP
df["FF17ind"] = sicff(df["sicCRSP"], industry=17)
df = df.dropna(subset=["FF17ind"])
df = df[df["sicCRSP"] != 9999] # exclude unclassified companies

print(f"After FF17 classification: {len(df):,} observations")

# Calculate industry means and standard deviations by FF17 industry and time
industry_stats = (
    df.groupby(["FF17ind", "time_avail_m"])["OrgCapNoAdjtemp"]
    .agg(["mean", "std"])
    .reset_index()
)
df = pd.merge(df, industry_stats, on=["FF17ind", "time_avail_m"], how="left")

# Create industry-adjusted organizational capital
df.loc[df["std"].isna(), "OrgCap"] = np.nan
df["OrgCap"] = (df["OrgCapNoAdjtemp"] - df["mean"]) / df["std"]

# filter out financial firms
df = df[((df["sicCRSP"] < 6000) | (df["sicCRSP"] >= 7000)) & df["sicCRSP"].notna()]

print(f"Final OrgCap values: {df['OrgCap'].notna().sum():,} non-missing")

# SAVE
save_predictor(df, "OrgCap")
save_placebo(df, "OrgCapNoAdj")

print("OrgCap and OrgCapNoAdj calculation completed successfully!")