# ABOUTME: Cash-based operating profitability following Ball et al. 2016 JFE, Table 4A Cash-based 10-1
# ABOUTME: calculates operating profitability with working capital and R&D adjustments

"""
CBOperProf.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/CBOperProf.py

Inputs:
    - SignalMasterTable.parquet: Master signal data with columns [permno, gvkey, time_avail_m, exchcd, sicCRSP, shrcd, mve_permco, mve_c]
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, revt, cogs, xsga, xrd, rect, invt, xpp, drc, drlt, ap, xacc, at, ceq]

Outputs:
    - CBOperProf.csv: CSV file with columns [permno, yyyymm, CBOperProf]
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor
from utils.stata_replication import stata_multi_lag, fill_date_gaps

print("Starting CBOperProf predictor...")

# DATA LOAD
print("Loading SignalMasterTable...")
signal_master = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m", "exchcd", "sicCRSP", "shrcd", "mve_permco", "mve_c"],
)

print(f"Loaded SignalMasterTable: {len(signal_master):,} observations")

print("Loading m_aCompustat...")
compustat_df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=[
        "permno",
        "time_avail_m",
        "revt",
        "cogs",
        "xsga",
        "xrd",
        "rect",
        "invt",
        "xpp",
        "drc",
        "drlt",
        "ap",
        "xacc",
        "at",
        "ceq",
    ],
)

print(f"Loaded m_aCompustat: {len(compustat_df):,} observations")

# Merge SignalMasterTable with m_aCompustat
print("Merging SignalMasterTable with m_aCompustat...")
df = pd.merge(signal_master, compustat_df, on=["permno", "time_avail_m"], how="left")

print(f"After merge: {len(df):,} observations")

# SIGNAL CONSTRUCTION
print("Constructing CBOperProf signal...")

# Replace missing values with 0 for the specified variables
# (equivalent to foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc { replace `v' = 0 if mi(`v') })
zero_fill_vars = [
    "revt",
    "cogs",
    "xsga",
    "xrd",
    "rect",
    "invt",
    "xpp",
    "drc",
    "drlt",
    "ap",
    "xacc",
]
for var in zero_fill_vars:
    df[var] = df[var].fillna(0)

# Sort by permno and time_avail_m for lag calculations
df = df.sort_values(["permno", "time_avail_m"])

lag_vars = ["rect", "invt", "xpp", "drc", "drlt", "ap", "xacc"]
# Preserve observed rows while filling the monthly grid for calendar lags.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m")
lag_vars = ['rect', 'invt', 'xpp', 'drc', 'drlt', 'ap', 'xacc']
for var in lag_vars:
    df = stata_multi_lag(df, "permno", "time_avail_m", var, [12], fill_gaps=False)
df = df.rename(columns={f"{var}_lag12": f"l12_{var}" for var in lag_vars})
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# some confusion about lagging assets or not
# OP 2016 JFE seems to lag assets, but 2015 JFE does not
# Yet no lag implies results much closer to OP
# Calculate CBOperProf following the complex formula
# CBOperProf = (revt - cogs - (xsga - xrd)) -
#              (rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) +
#              (drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)

df["CBOperProf"] = (
    (df["revt"] - df["cogs"] - (df["xsga"] - df["xrd"]))
    - (df["rect"] - df["l12_rect"])
    - (df["invt"] - df["l12_invt"])
    - (df["xpp"] - df["l12_xpp"])
    + (df["drc"] + df["drlt"] - df["l12_drc"] - df["l12_drlt"])
    + (df["ap"] - df["l12_ap"])
    + (df["xacc"] - df["l12_xacc"])
)

# Scale by total assets (equivalent to replace CBOperProf = CBOperProf/at)
df["CBOperProf"] = df["CBOperProf"] / df["at"]

# Calculate BM for filtering (equivalent to gen BM = log(ceq/mve_permco))
df["BM"] = np.log(df["ceq"] / df["mve_permco"])

# Apply exclusion criteria
# replace CBOperProf = . if shrcd > 11 | mi(mve_permco) | mi(BM) | mi(at) | (sicCRSP >= 6000 & sicCRSP < 7000)
exclusion_mask = (
    (df["shrcd"] > 11)
    | df["mve_c"].isna()
    | df["BM"].isna()
    | df["at"].isna()
    | ((df["sicCRSP"] >= 6000) & (df["sicCRSP"] < 7000))
)

df.loc[exclusion_mask, "CBOperProf"] = np.nan

print(
    f"Generated CBOperProf values for {df['CBOperProf'].notna().sum():,} observations"
)
print(f"Excluded {exclusion_mask.sum():,} observations due to filtering criteria")

# Clean up temporary columns
lag_cols_to_drop = [f"l12_{var}" for var in lag_vars]
df = df.drop(columns=lag_cols_to_drop + ["BM"])

# SAVE
print("Saving predictor...")
save_predictor(df, "CBOperProf")

print("CBOperProf predictor completed successfully!")
