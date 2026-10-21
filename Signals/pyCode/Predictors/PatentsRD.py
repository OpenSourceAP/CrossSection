# ABOUTME: Patents to RD expenses following Hirschleifer, Hsu and Li 2013, Table 9A EMI1
# ABOUTME: Calculates patent efficiency scaled by R&D capital with double-sorted portfolio approach

"""
PatentsRD.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/PatentsRD.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, gvkey, time_avail_m, mve_c, sicCRSP, exchcd]
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, xrd, sich, datadate, ceq]
    - PatentDataProcessed.parquet: Patent data with columns [gvkey, year, npat]

Outputs:
    - PatentsRD.csv: CSV file with columns [permno, yyyymm, PatentsRD]
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_multi_lag

# DATA LOAD
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master[
    ["permno", "gvkey", "time_avail_m", "mve_c", "sicCRSP", "exchcd"]
].copy()

# Convert datetime time_avail_m to YYYYMM integer format
df["time_avail_m"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month
df["year"] = df["time_avail_m"] // 100

# Merge with Compustat
compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
# Convert compustat time_avail_m to YYYYMM format
compustat["time_avail_m"] = (
    compustat["time_avail_m"].dt.year * 100 + compustat["time_avail_m"].dt.month
)
df = df.merge(
    compustat[["permno", "time_avail_m", "xrd", "sich", "datadate", "ceq"]],
    on=["permno", "time_avail_m"],
    how="left",
)
df = df.dropna(subset=["gvkey"])

# Patent citation dataset - compustat is already lagged, need to lag patent data to match
patents = pd.read_parquet("../pyData/Intermediate/PatentDataProcessed.parquet")
df = df.merge(patents[["gvkey", "year", "npat"]], on=["gvkey", "year"], how="left")

# Convert the established YYYYMM key only for calendar lagging.
df["_calendar_m"] = pd.to_datetime(df["time_avail_m"].astype(str), format="%Y%m")
df["_observed"] = True
df = stata_multi_lag(df, "permno", "_calendar_m", "npat", [6])
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()
# The source replaces missing patent counts after the lag, only on observed rows.
df["npat"] = df["npat_lag6"].fillna(0)
df = df.drop(columns="npat_lag6")

# SIGNAL CONSTRUCTION - form portfolios only in June
df = df[df["time_avail_m"] % 100 == 6]  # month == 6
df = df[
    df["time_avail_m"] >= 197501
]  # Takes into account xrd data standardized after 1975

# Efficiency in year t is patents in year t scaled by R&D capital (sum of depreciated past R&D)
# Portfolios are computed from July of year t to June of year t+1
# Replace missing R&D with 0
df["xrd"] = df["xrd"].fillna(0)

# June-only observations use annual calendar endpoints, including across missing years.
df["_observed"] = True
df = stata_multi_lag(df, "permno", "_calendar_m", "xrd", [2, 3, 4, 5, 6], freq="Y")
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed").copy()
df["time_avail_m"] = df["time_avail_m"].astype(int)
comp1_lag = df["xrd_lag2"]
comp2_lag = 0.8 * df["xrd_lag3"]
comp3_lag = 0.6 * df["xrd_lag4"]
comp4_lag = 0.4 * df["xrd_lag5"]
comp5_lag = 0.2 * df["xrd_lag6"]

df["comp1"] = np.where(comp1_lag.notna(), comp1_lag, 0.0)
df["comp2"] = np.where(comp2_lag.notna(), comp2_lag, 0.0)
df["comp3"] = np.where(comp3_lag.notna(), comp3_lag, 0.0)
df["comp4"] = np.where(comp4_lag.notna(), comp4_lag, 0.0)
df["comp5"] = np.where(comp5_lag.notna(), comp5_lag, 0.0)

df["RDcap"] = df["comp1"] + df["comp2"] + df["comp3"] + df["comp4"] + df["comp5"]
df["tempPatentsRD"] = np.where(df["RDcap"] > 0, df["npat"] / df["RDcap"], np.nan)

# Patent efficiency ratio: number of patents divided by R&D capital

df = df.drop(columns="_calendar_m")

# Filter
df = df.sort_values(["gvkey", "time_avail_m"])
df = (
    df.groupby("gvkey")
    .apply(lambda x: x.iloc[2:] if len(x) > 2 else x.iloc[0:0])
    .reset_index(drop=True)
)

df = df[~((df["sicCRSP"] >= 6000) & (df["sicCRSP"] <= 6999))]

df = df[~(df["ceq"] < 0)]

# Double independent sort
# Size categories
df = df.sort_values("time_avail_m")
size_cuts = []
for time_month, group in df.groupby("time_avail_m"):
    nyse_group = group[group["exchcd"] == 1]
    if len(nyse_group) > 0:
        median_mve = nyse_group["mve_c"].median()
        group["sizecat"] = np.where(group["mve_c"] <= median_mve, 1, 2)
    else:
        group["sizecat"] = 1
    size_cuts.append(group)
df = pd.concat(size_cuts, ignore_index=True)

# PatentsRD categories (3 groups)
patents_cuts = []
for time_month, group in df.groupby("time_avail_m"):
    # Keep all observations, sort only those with valid tempPatentsRD
    valid_group = group.dropna(subset=["tempPatentsRD"])

    if len(valid_group) > 0:
        try:
            # Use fastxtile to match Stata behavior
            valid_group = valid_group.copy()  # Make explicit copy to avoid warning
            valid_group.loc[:, "maincat"] = fastxtile(valid_group["tempPatentsRD"], n=3)
            valid_group.loc[:, "maincat"] = valid_group["maincat"].astype(int)

            # Merge categories back to all observations
            group = group.merge(
                valid_group[["permno", "time_avail_m", "maincat"]],
                on=["permno", "time_avail_m"],
                how="left",
            )
        except ValueError:
            # Handle case where all values are the same
            group["maincat"] = np.nan
    else:
        # No valid observations this month
        group["maincat"] = np.nan

    patents_cuts.append(group)
df = pd.concat(patents_cuts, ignore_index=True)


# Create PatentsRD signal (binary: 1 for small/high, 0 for small/low)
df["PatentsRD"] = np.nan
df.loc[(df["sizecat"] == 1) & (df["maincat"] == 3), "PatentsRD"] = 1
df.loc[(df["sizecat"] == 1) & (df["maincat"] == 1), "PatentsRD"] = 0


# Expand back to monthly
def add_months_to_yyyymm(yyyymm, months_to_add):
    """Add months to YYYYMM format, handling year rollover properly"""
    year = yyyymm // 100
    month = yyyymm % 100

    # Add months
    total_months = month + months_to_add

    # Handle year rollover
    while total_months > 12:
        year += 1
        total_months -= 12

    return year * 100 + total_months


monthly_data = []
for _, row in df.iterrows():
    for i in range(12):
        new_row = row.copy()
        new_row["time_avail_m"] = add_months_to_yyyymm(row["time_avail_m"], i)
        monthly_data.append(new_row)

df_monthly = pd.DataFrame(monthly_data)

# SAVE
output = df_monthly[["permno", "time_avail_m", "PatentsRD"]].dropna()
output = output.astype({"permno": int, "time_avail_m": int})
output = output.rename(columns={"time_avail_m": "yyyymm"})
output = output.set_index(["permno", "yyyymm"]).sort_index()
output.to_csv("../pyData/Predictors/PatentsRD.csv")

print("PatentsRD predictor saved successfully")
