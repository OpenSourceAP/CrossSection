# ABOUTME: Net debt to price following Penman, Richardson and Tuna 2007, Table 4A
# ABOUTME: Net debt (debt + preferred stock - cash) divided by market value, excluding financial firms and low BM firms

"""
NetDebtPrice predictor calculation

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    python3 Predictors/NetDebtPrice.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (permno, time_avail_m, at, dltt, dlc, pstk, dvpa, tstkp, che, sic, ib, csho, ceq, prcc_f)
    - ../pyData/Intermediate/SignalMasterTable.parquet (permno, time_avail_m, mve_c)

Outputs:
    - ../pyData/Predictors/NetDebtPrice.csv (permno, yyyymm, NetDebtPrice)
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.stata_fastxtile import fastxtile_by_group

# DATA LOAD
# Load m_aCompustat data
compustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "permno",
        "time_avail_m",
        "at",
        "dltt",
        "dlc",
        "pstk",
        "dvpa",
        "tstkp",
        "che",
        "sic",
        "ib",
        "csho",
        "ceq",
        "prcc_f",
    ],
)

# Remove duplicates by permno time_avail_m (keep first)
compustat_df = compustat_df.drop_duplicates(
    subset=["permno", "time_avail_m"], keep="first"
)

# Merge with SignalMasterTable
signal_df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_c"],
)
df = compustat_df.merge(signal_df, on=["permno", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
# Convert sic to numeric
df["sic"] = pd.to_numeric(df["sic"], errors="coerce")

# Calculate net debt to price ratio
df["NetDebtPrice"] = (
    (df["dltt"] + df["dlc"] + df["pstk"] + df["dvpa"] - df["tstkp"]) - df["che"]
) / df["mve_c"]

# Exclude financial firms (SIC 6000-6999)
df.loc[(df["sic"] >= 6000) & (df["sic"] <= 6999), "NetDebtPrice"] = np.nan

# Set to missing if key variables are missing
df.loc[
    (df["at"].isna())
    | (df["ib"].isna())
    | (df["csho"].isna())
    | (df["ceq"].isna())
    | (df["prcc_f"].isna()),
    "NetDebtPrice",
] = np.nan

# Keep constant B/M - exclude bottom 2 BM quintiles
with np.errstate(divide="ignore", invalid="ignore"):
    df["BM"] = np.log(df["ceq"] / df["mve_c"])
# Handle infinite values in BM
df["BM_clean"] = df["BM"].replace([np.inf, -np.inf], np.nan)
# Use Stata-equivalent fastxtile for BM quintiles
df["tempsort"] = fastxtile_by_group(df, "BM_clean", "time_avail_m", n=5)
# Exclude bottom 2 quintiles (keep only quintiles 3, 4, 5)
df.loc[df["tempsort"] <= 2, "NetDebtPrice"] = np.nan

# Drop missing values
df = df.dropna(subset=["NetDebtPrice"])

# Convert time_avail_m to yyyymm
df["yyyymm"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month

# Keep required columns and order
df = df[["permno", "yyyymm", "NetDebtPrice"]].copy()

# SAVE
df.to_csv("../pyData/Predictors/NetDebtPrice.csv", index=False)
print(f"NetDebtPrice: Saved {len(df):,} observations")
