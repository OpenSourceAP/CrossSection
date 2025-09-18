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
df = pd.merge(signal_master, compustat, on=["permno", "time_avail_m"], how="inner")
df = pd.merge(df, gnpdefl, on="time_avail_m", how="inner")


# Convert sic to numeric
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Filter conditions: December fiscal year end and SIC industry restrictions
df["month_datadate"] = df["datadate"].dt.month
df = df[
    (df["month_datadate"] == 12)
    & ((df["sic"] < 6000) | (df["sic"] >= 7000))
    & df["sic"].notna()
].copy()

print(f"After filtering: {len(df):,} observations")


# SIGNAL CONSTRUCTION
# Sort by permno and time
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Create age variable for each firm
df["tempAge"] = df.groupby("permno").cumcount() + 1

# Replace missing SG&A with 0
df["xsga"] = df["xsga"].fillna(0)

# Deflate SG&A by GNP deflator
df["xsga"] = df["xsga"] / df["gnpdefl"]


# Initialize organizational capital for firms with <= 12 periods of data
df["OrgCapNoAdj"] = np.where(df["tempAge"] <= 12, 4 * df["xsga"], np.nan)

# For firms with > 12 periods: use depreciation formula with 12-month calendar lag
# Apply iteratively since later values depend on earlier calculations

# Sort by permno and time to ensure proper order
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Create a mapping of time_avail_m for efficient lookup
time_to_index = {}
for idx, row in df.iterrows():
    key = (row["permno"], row["time_avail_m"])
    time_to_index[key] = idx

# Apply the recursive formula iteratively
print("Applying recursive organizational capital formula...")
for idx, row in df.iterrows():
    if row["tempAge"] > 12:
        # Look for the value 12 months ago
        lag_date = row["time_avail_m"] - pd.DateOffset(months=12)
        lag_key = (row["permno"], lag_date)

        if lag_key in time_to_index:
            lag_idx = time_to_index[lag_key]
            lag_value = df.at[lag_idx, "OrgCapNoAdj"]

            if pd.notna(lag_value):
                new_value = 0.85 * lag_value + row["xsga"]
                df.at[idx, "OrgCapNoAdj"] = new_value

# Create lag column for display purposes
df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)
df["l12_OrgCapNoAdj"] = df.groupby("permno")["OrgCapNoAdj"].shift(12)

# Scale by total assets
df["OrgCapNoAdj"] = df["OrgCapNoAdj"] / df["at"]

# Handle infinite values from division by zero
df.loc[np.isinf(df["OrgCapNoAdj"]), "OrgCapNoAdj"] = np.nan

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
df["tempFF17"] = sicff(df["sicCRSP"], industry=17)

# Drop observations with missing industry classification
df = df.dropna(subset=["tempFF17"]).copy()

# Exclude SIC 9999 companies (unclassified)
df = df[df["sicCRSP"] != 9999].copy()


print(f"After FF17 classification: {len(df):,} observations")

# Calculate industry means and standard deviations by FF17 industry and time
temp_stats = (
    df.groupby(["tempFF17", "time_avail_m"])["OrgCapNoAdjtemp"]
    .agg(["mean", "std"])
    .reset_index()
)
temp_stats.columns = ["tempFF17", "time_avail_m", "tempMean", "tempSD"]

df = pd.merge(df, temp_stats, on=["tempFF17", "time_avail_m"], how="left")


# Create industry-adjusted organizational capital
df["OrgCap"] = (df["OrgCapNoAdjtemp"] - df["tempMean"]) / df["tempSD"]

# Handle cases where tempSD is 0 or NaN
df.loc[df["tempSD"] == 0, "OrgCap"] = np.nan
df.loc[df["tempSD"].isna(), "OrgCap"] = np.nan


print(f"Final OrgCap values: {df['OrgCap'].notna().sum():,} non-missing")


# SAVE

# Save OrgCap predictor
df_orgcap = df[["permno", "time_avail_m", "OrgCap"]].dropna(subset=["OrgCap"]).copy()
save_predictor(df_orgcap, "OrgCap")

# Save OrgCapNoAdj placebo
df_orgcapnoadj = (
    df[["permno", "time_avail_m", "OrgCapNoAdj"]].dropna(subset=["OrgCapNoAdj"]).copy()
)
save_placebo(df_orgcapnoadj, "OrgCapNoAdj")

print("OrgCap and OrgCapNoAdj calculation completed successfully!")
