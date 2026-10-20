# ABOUTME: Payout yield using individual-quarter Compustat flows.
"""PayoutYield_q.py

Run from Signals/pyCode:
    /opt/venv/projects/openap/bin/python3 Placebos/PayoutYield_q.py
Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet:
      permno, gvkey, time_avail_m, mve_permco
    - ../pyData/Intermediate/m_QCompustat.parquet:
      gvkey, time_avail_m, dvpsxq, cshoq, ajexq, prstkcyq, pstkq
Output: ../pyData/Placebos/PayoutYield_q.csv (permno, yyyymm, PayoutYield_q).
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.saveplacebo import save_placebo
from utils.stata_replication import fill_date_gaps, stata_multi_lag

# Use matched accounting rows without additional flow or market-cap imputation.
df = pd.read_parquet(
    "../pyData/Intermediate/SignalMasterTable.parquet",
    columns=["permno", "gvkey", "time_avail_m", "mve_permco"],
)
df = df.loc[df["gvkey"].notna()].copy()
qcomp = pd.read_parquet(
    "../pyData/Intermediate/m_QCompustat.parquet",
    columns=["gvkey", "time_avail_m", "dvpsxq", "cshoq", "ajexq", "prstkcyq", "pstkq"],
)
df["gvkey"] = df["gvkey"].astype(int)
qcomp["gvkey"] = qcomp["gvkey"].astype(int)
df = df.merge(qcomp, on=["gvkey", "time_avail_m"], how="inner", validate="many_to_one")

# Fill the monthly calendar once for calendar lags; remove inserted months.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
for column, months in [("pstkq", 3), ("mve_permco", 6)]:
    df = stata_multi_lag(
        df, "permno", "time_avail_m", column, [months],
        prefix="l", fill_gaps=False,
    )
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Zero dividends need no share inputs. All other missing flow inputs propagate.
df["tempDiv"] = (df["dvpsxq"] * df["cshoq"] * df["ajexq"]).mask(df["dvpsxq"].eq(0), 0)
df["preferred_reduction"] = (df["l3_pstkq"] - df["pstkq"]).clip(lower=0).fillna(0)
# prstkcyq is already an individual-quarter flow from the downloader.
df["gross_payout"] = df["tempDiv"] + df["prstkcyq"] + df["preferred_reduction"]
df["PayoutYield_q"] = df["gross_payout"] / df["l6_mve_permco"]

# Require observed, finite, positive market cap and finite positive gross yield.
df = df.loc[
    np.isfinite(df["l6_mve_permco"]) & (df["l6_mve_permco"] > 0)
    & np.isfinite(df["PayoutYield_q"]) & (df["PayoutYield_q"] > 0)
]
result = save_placebo(df[["permno", "time_avail_m", "PayoutYield_q"]], "PayoutYield_q")
