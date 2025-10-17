# ABOUTME: Pension Funding Status following Franzoni and Marin 2006, Table 3B
# ABOUTME: Computes funding status metrics using pension plan asset/obligation data from Compustat

"""
ZZ1_FR_FRbook.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ZZ1_FR_FRbook.py

Inputs:
    - SignalMasterTable.parquet: Master table with columns [permno, gvkey, time_avail_m, shrcd, mve_permco]
    - CompustatPensions.parquet: Pension data with columns [gvkey, year, pbnaa, pplao, pplau, pbnvv, pbpro, pbpru]
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, time_avail_m, at]

Outputs:
    - FR.csv: CSV file with columns [permno, yyyymm, FR]
    - FRbook.csv: CSV file with columns [permno, yyyymm, FRbook] (saved to Placebos folder)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
signal_master = pd.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = signal_master[["permno", "gvkey", "time_avail_m", "shrcd", "mve_permco"]].copy()
df = df.dropna(subset=["gvkey"])

# Convert datetime time_avail_m to YYYYMM integer format
df["time_avail_m"] = df["time_avail_m"].dt.year * 100 + df["time_avail_m"].dt.month
df["year"] = df["time_avail_m"] // 100

# Merge with pension data
pensions = pd.read_parquet("../pyData/Intermediate/CompustatPensions.parquet")
df = df.merge(pensions, on=["gvkey", "year"], how="inner")

# Merge with Compustat for book assets
compustat = pd.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
# Convert compustat time_avail_m to YYYYMM format
compustat["time_avail_m"] = (
    compustat["time_avail_m"].dt.year * 100 + compustat["time_avail_m"].dt.month
)
df = df.merge(
    compustat[["gvkey", "time_avail_m", "at"]], on=["gvkey", "time_avail_m"], how="left"
)

# SIGNAL CONSTRUCTION
# Fair Value of Plan Assets
df["FVPA"] = np.where(
    (df["year"] >= 1980) & (df["year"] <= 1986),
    df["pbnaa"],
    np.where(
        (df["year"] >= 1987) & (df["year"] <= 1997),
        df["pplao"] + df["pplau"],
        np.where(df["year"] >= 1998, df["pplao"], np.nan),
    ),
)

# Projected Benefit Obligation
df["PBO"] = np.where(
    (df["year"] >= 1980) & (df["year"] <= 1986),
    df["pbnvv"],
    np.where(
        (df["year"] >= 1987) & (df["year"] <= 1997),
        df["pbpro"] + df["pbpru"],
        np.where(df["year"] >= 1998, df["pbpro"], np.nan),
    ),
)

# Funding Ratio scaled by market value
df["FR"] = (df["FVPA"] - df["PBO"]) / df["mve_permco"]
df.loc[df["shrcd"] > 11, "FR"] = np.nan

# Funding Ratio scaled by book assets
df["FRbook"] = (df["FVPA"] - df["PBO"]) / df["at"]
df.loc[df["shrcd"] > 11, "FRbook"] = np.nan

# SAVE FR
fr_output = df[["permno", "time_avail_m", "FR"]].dropna()
fr_output = fr_output.astype({"permno": int, "time_avail_m": int})
fr_output = fr_output.rename(columns={"time_avail_m": "yyyymm"})
fr_output = fr_output.set_index(["permno", "yyyymm"]).sort_index()
fr_output.to_csv("../pyData/Predictors/FR.csv")

# SAVE FRbook (as placebo in original)
frbook_output = df[["permno", "time_avail_m", "FRbook"]].dropna()
frbook_output = frbook_output.astype({"permno": int, "time_avail_m": int})
frbook_output = frbook_output.rename(columns={"time_avail_m": "yyyymm"})
frbook_output = frbook_output.set_index(["permno", "yyyymm"]).sort_index()
frbook_output.to_csv("../pyData/Placebos/FRbook.csv")

print("FR (Predictor) and FRbook (Placobo) saved successfully")
