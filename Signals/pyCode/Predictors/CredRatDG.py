# %%

# ABOUTME: Credit Rating Downgrade following Dichev and Piotroski 2001, Table 4, Downgrade BHAR 3-month
# ABOUTME: calculates credit rating downgrade signal - 1 if downgrade in past 6 months

"""
Usage:
    python3 Predictors/CredRatDG.py

Inputs:
    - m_SP_creditratings.parquet: S&P credit ratings data with columns [gvkey, time_avail_m, credrat]
    - m_CIQ_creditratings.parquet: CIQ credit ratings data with columns [gvkey, ratingdate, source, anydowngrade]
    - SignalMasterTable.parquet: Monthly master table with columns [gvkey, permno, time_avail_m]

Outputs:
    - CredRatDG.csv: CSV file with columns [permno, yyyymm, CredRatDG]
    - CredRatDG = 1 if credit rating downgrade occurred in past 6 months, else 0
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

# %%

print("Starting CredRatDG predictor...")

# Process Compustat SP ratings data
print("Loading m_SP_creditratings data...")
comp_df = pd.read_parquet(
    "../pyData/Intermediate/m_SP_creditratings.parquet",
    columns=["gvkey", "time_avail_m", "credrat"],
)

# enforce standard formats (ideally, we should be more systematic about this)
comp_df["gvkey"] = comp_df["gvkey"].astype(np.int64)
comp_df["time_avail_m"] = comp_df["time_avail_m"].dt.to_period("M")

# define downgrade_sp: downgrade_sp = 1 if credrat - l.credrat < 0
comp_df = comp_df.sort_values(["gvkey", "time_avail_m"])
comp_df["l_credrat"] = comp_df.groupby("gvkey")["credrat"].shift(1)
comp_df["downgrade_sp"] = np.where(
    comp_df["credrat"] - comp_df["l_credrat"] < 0, 1, np.nan
)

# clean up, keeping only if we have a downgrade
comp_df.query("downgrade_sp == 1", inplace=True)
comp_df = comp_df[["gvkey", "time_avail_m", "downgrade_sp"]]

# note: SP credit ratings are already deduplicated

print(f"Generated dataset of {comp_df['downgrade_sp'].notna().sum():,} SP downgrades")

# %%

# Process CIQ SP ratings data
print("Loading m_CIQ_creditratings data...")
ciq_df = pd.read_parquet(
    "../pyData/Intermediate/m_CIQ_creditratings.parquet",
    columns=["gvkey", "ratingdate", "source", "anydowngrade"],
)
ciq_df["gvkey"] = ciq_df["gvkey"].astype(np.int64)
ciq_df["ratingdate"] = pd.to_datetime(ciq_df["ratingdate"]).dt.to_period("M")
ciq_df.rename(
    columns={"ratingdate": "time_avail_m", "anydowngrade": "downgrade_ciq"},
    inplace=True,
)

# keep only downgrades
ciq_df.query("downgrade_ciq == 1", inplace=True)

# deduplicate: assign downgrade if any source has a downgrade in the month
ciq_df = (
    ciq_df.groupby(["gvkey", "time_avail_m"])
    .agg({"downgrade_ciq": "max"})
    .reset_index()
)

# %%

# Load SignalMasterTable
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["gvkey", "permno", "time_avail_m"],
).dropna(subset=["gvkey"])

signal_master["gvkey"] = signal_master["gvkey"].astype(np.int64)
signal_master["time_avail_m"] = signal_master["time_avail_m"].dt.to_period("M")

print(f"Loaded {len(signal_master):,} SignalMasterTable observations")

# create df: merging signal_master with comp_df and ciq_df
print("Merging data...")
df = pd.merge(signal_master, comp_df, on=["gvkey", "time_avail_m"], how="left")
df = pd.merge(df, ciq_df, on=["gvkey", "time_avail_m"], how="left")

# define dg_cur: use SP downgrade if available, otherwise use CIQ downgrade
# if no data, assume no downgrade
df["dg_cur"] = df["downgrade_sp"].fillna(df["downgrade_ciq"])
df["dg_cur"] = df["dg_cur"].fillna(0)

print(f"After merging: {len(df):,} observations")

# %%

# SIGNAL CONSTRUCTION
print("Constructing CredRatDG signal...")

# define CredRatDG: 1 if any downgrade in current or previous 6 months
df.sort_values(["permno", "time_avail_m"], inplace=True)
df.set_index(["permno", "time_avail_m"], inplace=True)
df["CredRatDG"] = (
    df.groupby("permno")["dg_cur"]
    .rolling(6, min_periods=1)
    .max()
    .reset_index(level=0, drop=True)
)
df.reset_index(inplace=True)

# SAVE
print("Saving predictor...")

# convert time_avail_m to datetime for comptability with `savepredictor`
# tbc: we should really standardize the date formats better and from the DataDownloads
df["time_avail_m"] = df["time_avail_m"].dt.to_timestamp()

save_predictor(df, "CredRatDG")

print("CredRatDG predictor completed successfully!")
