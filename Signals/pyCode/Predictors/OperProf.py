# ABOUTME: Operating profitability following Fama and French 2006, Table 3 Y_t/B_t
# ABOUTME: calculates operating profits scaled by book equity, excluding smallest size tercile

"""
OperProf.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/OperProf.py

Inputs:
    - SignalMasterTable.parquet: Monthly master table with mve_c (size filtering)
    - m_aCompustat.parquet: Monthly Compustat data with revt, cogs, xsga, xint, ceq

Outputs:
    - OperProf.csv: CSV file with columns [permno, yyyymm, OperProf]
"""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, ".")
from utils.save_standardized import save_predictor

# Notes:
# Excludes smallest size tercile to simulate NYSE size breakpoints
# This approach follows Fama-French methodology which overweights large cap stocks
# Operating profitability = (revenue - cogs - sga - interest) / equity
# Removing SGA expenses significantly improves signal strength (similar to Novy-Marx)

# DATA LOAD
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m", "mve_c"],
)

# Merge with Compustat data
compustat = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["gvkey", "time_avail_m", "revt", "cogs", "xsga", "xint", "ceq"],
)

df = pd.merge(df, compustat, on=["gvkey", "time_avail_m"], how="inner")

# SIGNAL CONSTRUCTION
with np.errstate(over="ignore", invalid="ignore"):
    df["tempprof"] = (df["revt"] - df["cogs"] - df["xsga"] - df["xint"]) / df["ceq"]


# Create size terciles by time_avail_m and exclude smallest tercile
df["tempsizeq"] = df.groupby("time_avail_m")["mve_c"].transform(
    lambda x: pd.qcut(x, q=3, labels=False, duplicates="drop") + 1
)

# Set tempprof to missing for smallest size tercile
df.loc[df["tempsizeq"] == 1, "tempprof"] = pd.NA

# Assign to OperProf
df["OperProf"] = df["tempprof"]


# SAVE
save_predictor(df, "OperProf")
print(f"OperProf: Saved {len(df):,} observations")
