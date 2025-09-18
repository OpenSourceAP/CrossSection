# ABOUTME: Calculates R&D capital-to-assets following Li 2011 Table 7 (small firms only)
# ABOUTME: Run from pyCode/ directory: python3 Predictors/RDcap.py

# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/RDcap.csv

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.save_standardized import save_predictor

# DATA LOAD
df = pd.read_parquet(
    "../pyData/Intermediate/m_aCompustat.parquet",
    columns=["permno", "time_avail_m", "at", "xrd"],
)

# Drop duplicates
df = df.drop_duplicates(subset=["permno", "time_avail_m"])

# Merge with SignalMasterTable (keep master match like Stata)
smt = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "time_avail_m", "mve_c"],
)
df = df.merge(
    smt[["permno", "time_avail_m", "mve_c"]], on=["permno", "time_avail_m"], how="left"
)

# SIGNAL CONSTRUCTION

# Fill date gaps before processing R&D data
df = fill_date_gaps(df)

# Assume missing xrd values are 0
df["tempXRD"] = df["xrd"].fillna(0)

# Calculate calendar-based lags of tempXRD using stata_multi_lag
df = stata_multi_lag(df, "permno", "time_avail_m", "tempXRD", [12, 24, 36, 48])

# Calculate R&D capital (weighted sum of current and lagged R&D)
df["RDcap"] = (
    df["tempXRD"]
    + 0.8 * df["tempXRD_lag12"]
    + 0.6 * df["tempXRD_lag24"]
    + 0.4 * df["tempXRD_lag36"]
    + 0.2 * df["tempXRD_lag48"]
) / df["at"]

# Exclude observations before 1980
df.loc[df["time_avail_m"].dt.year < 1980, "RDcap"] = np.nan

# Create size tertiles - RDcap only works in small firms
df["tempsizeq"] = df.groupby("time_avail_m")["mve_c"].transform(
    lambda x: pd.qcut(x, q=3, labels=False, duplicates="drop") + 1
)
df.loc[df["tempsizeq"] >= 2, "RDcap"] = np.nan
df.loc[df["tempsizeq"].isna(), "RDcap"] = np.nan

# SAVE
save_predictor(df, "RDcap")

print("RDcap predictor saved successfully")
