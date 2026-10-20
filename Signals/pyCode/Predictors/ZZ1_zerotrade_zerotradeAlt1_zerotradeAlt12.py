# ABOUTME: Liquidity measures (LM1, LM6, LM12) following Liu 2006, Journal of Financial Economics 82, 631-671
# ABOUTME: Calculates turnover-adjusted number of zero daily trading volumes over 1M, 6M, and 12M periods

"""
ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12.py

Inputs:
    - dailyCRSP.parquet: Daily CRSP data with columns [permno, time_d, vol, shrout]

Outputs:
    - zerotrade1M.csv: CSV file with columns [permno, yyyymm, zerotrade1M]
    - zerotrade6M.csv: CSV file with columns [permno, yyyymm, zerotrade6M]
    - zerotrade12M.csv: CSV file with columns [permno, yyyymm, zerotrade12M]
"""

import pandas as pd
import numpy as np
import warnings
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.stata_replication import fill_date_gaps, stata_multi_lag

warnings.filterwarnings("ignore")

print("Starting ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12.py...")

# DATA LOAD
print("Loading data...")
df = pd.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")

# SIGNAL CONSTRUCTION
df["time_avail_m"] = df["time_d"].dt.year * 100 + df["time_d"].dt.month

df["countzero"] = np.where(df["vol"] == 0, 1, 0)
df["turn"] = (
    df["vol"] / df["shrout"]
)  # daily turnover is the ratio of the number of shares traded on a day to the number of shares outstanding at the end of the day (Liu (2006, p. 635))

df["days"] = 0  # help variable because of some weirdness of collapse

# gcollapse (sum) countzero turn (count) ndays = days, by(permno time_avail_m)
collapsed = (
    df.groupby(["permno", "time_avail_m"])
    .agg({"countzero": "sum", "turn": "sum", "days": "count"})
    .reset_index()
)
collapsed = collapsed.rename(columns={"days": "ndays"})

# xtset permno time_avail_m
collapsed = collapsed.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

# Use a date-valued grid while retaining the original YYYYMM output column.
collapsed["_calendar_m"] = pd.to_datetime(collapsed["time_avail_m"].astype(str), format="%Y%m")
collapsed["_observed"] = True
collapsed = fill_date_gaps(collapsed, "permno", "_calendar_m")
for var in ("turn", "countzero", "ndays"):
    collapsed = stata_multi_lag(collapsed, "permno", "_calendar_m", var, list(range(1, 12)), fill_gaps=False)

# 40n1 Number of days with 0 trades (1 month version)
collapsed["temp_zerotrade"] = (
    collapsed["countzero"] + ((1 / collapsed["turn"]) / 480000)
) * (21 / collapsed["ndays"])
collapsed = stata_multi_lag(collapsed, "permno", "_calendar_m", "temp_zerotrade", [1], fill_gaps=False)
collapsed["zerotrade1M"] = collapsed["temp_zerotrade_lag1"]

# 40 Number of days with 0 trades (6 month version)
collapsed["Turn6"] = (
    collapsed["turn"]
    + collapsed["turn_lag1"]
    + collapsed["turn_lag2"]
    + collapsed["turn_lag3"]
    + collapsed["turn_lag4"]
    + collapsed["turn_lag5"]
)
collapsed["countzero6"] = (
    collapsed["countzero"]
    + collapsed["countzero_lag1"]
    + collapsed["countzero_lag2"]
    + collapsed["countzero_lag3"]
    + collapsed["countzero_lag4"]
    + collapsed["countzero_lag5"]
)
collapsed["ndays6"] = (
    collapsed["ndays"]
    + collapsed["ndays_lag1"]
    + collapsed["ndays_lag2"]
    + collapsed["ndays_lag3"]
    + collapsed["ndays_lag4"]
    + collapsed["ndays_lag5"]
)

collapsed["temp_zerotrade6"] = (
    collapsed["countzero6"] + ((1 / collapsed["Turn6"]) / 11000)
) * (
    21 * 6 / collapsed["ndays6"]
)  # I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635))

collapsed = stata_multi_lag(collapsed, "permno", "_calendar_m", "temp_zerotrade6", [1], fill_gaps=False)
collapsed["zerotrade6M"] = collapsed["temp_zerotrade6_lag1"]

# 40n12 Number of days with 0 trades (12 month version)
collapsed["Turn12"] = (
    collapsed["turn"]
    + collapsed["turn_lag1"]
    + collapsed["turn_lag2"]
    + collapsed["turn_lag3"]
    + collapsed["turn_lag4"]
    + collapsed["turn_lag5"]
    + collapsed["turn_lag6"]
    + collapsed["turn_lag7"]
    + collapsed["turn_lag8"]
    + collapsed["turn_lag9"]
    + collapsed["turn_lag10"]
    + collapsed["turn_lag11"]
)
collapsed["countzero12"] = (
    collapsed["countzero"]
    + collapsed["countzero_lag1"]
    + collapsed["countzero_lag2"]
    + collapsed["countzero_lag3"]
    + collapsed["countzero_lag4"]
    + collapsed["countzero_lag5"]
    + collapsed["countzero_lag6"]
    + collapsed["countzero_lag7"]
    + collapsed["countzero_lag8"]
    + collapsed["countzero_lag9"]
    + collapsed["countzero_lag10"]
    + collapsed["countzero_lag11"]
)
collapsed["ndays12"] = (
    collapsed["ndays"]
    + collapsed["ndays_lag1"]
    + collapsed["ndays_lag2"]
    + collapsed["ndays_lag3"]
    + collapsed["ndays_lag4"]
    + collapsed["ndays_lag5"]
    + collapsed["ndays_lag6"]
    + collapsed["ndays_lag7"]
    + collapsed["ndays_lag8"]
    + collapsed["ndays_lag9"]
    + collapsed["ndays_lag10"]
    + collapsed["ndays_lag11"]
)

collapsed["temp_zerotrade12"] = (
    collapsed["countzero12"] + ((1 / collapsed["Turn12"]) / 11000)
) * (
    21 * 12 / collapsed["ndays12"]
)  # I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635))

collapsed = stata_multi_lag(collapsed, "permno", "_calendar_m", "temp_zerotrade12", [1], fill_gaps=False)
collapsed["zerotrade12M"] = collapsed["temp_zerotrade12_lag1"]

# Remove inserted months before saving any of the three signals.
collapsed = collapsed.loc[collapsed["_observed"].eq(True)].drop(columns=["_observed", "_calendar_m"]).copy()
collapsed["time_avail_m"] = collapsed["time_avail_m"].astype(int)

# SAVE
# Save zerotrade1M
zerotrade1M = collapsed[["permno", "time_avail_m", "zerotrade1M"]].dropna()
zerotrade1M["yyyymm"] = zerotrade1M["time_avail_m"]
zerotrade1M = zerotrade1M[["permno", "yyyymm", "zerotrade1M"]]
zerotrade1M.to_csv("../pyData/Predictors/zerotrade1M.csv", index=False)

# Save zerotrade6M
zerotrade6M = collapsed[["permno", "time_avail_m", "zerotrade6M"]].dropna()
zerotrade6M["yyyymm"] = zerotrade6M["time_avail_m"]
zerotrade6M = zerotrade6M[["permno", "yyyymm", "zerotrade6M"]]
zerotrade6M.to_csv("../pyData/Predictors/zerotrade6M.csv", index=False)

# Save zerotrade12M
zerotrade12M = collapsed[["permno", "time_avail_m", "zerotrade12M"]].dropna()
zerotrade12M["yyyymm"] = zerotrade12M["time_avail_m"]
zerotrade12M = zerotrade12M[["permno", "yyyymm", "zerotrade12M"]]
zerotrade12M.to_csv("../pyData/Predictors/zerotrade12M.csv", index=False)
