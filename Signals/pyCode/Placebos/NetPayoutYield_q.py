# ABOUTME: Net payout yield using individual-quarter Compustat flows.
"""NetPayoutYield_q.py

Run from Signals/pyCode:
    /opt/venv/projects/openap/bin/python3 Placebos/NetPayoutYield_q.py
Inputs:
    - ../pyData/Intermediate/SignalMasterTable.parquet:
      permno, gvkey, time_avail_m, mve_permco
    - ../pyData/Intermediate/m_QCompustat.parquet:
      gvkey, time_avail_m, dvpsxq, cshoq, ajexq, prstkcyq, pstkq, sstkyq
Output: ../pyData/Placebos/NetPayoutYield_q.csv (permno, yyyymm, NetPayoutYield_q).
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
    columns=["gvkey", "time_avail_m", "dvpsxq", "cshoq", "ajexq", "prstkcyq", "pstkq", "sstkyq"],
)
df["gvkey"] = df["gvkey"].astype(int)
qcomp["gvkey"] = qcomp["gvkey"].astype(int)
df = df.merge(qcomp, on=["gvkey", "time_avail_m"], how="inner", validate="many_to_one")

# Fill the monthly calendar once for calendar lags; remove inserted months.
df["_observed"] = True
df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
for column, months in [("pstkq", 3)]:
    df = stata_multi_lag(
        df, "permno", "time_avail_m", column, [months],
        prefix="l", fill_gaps=False,
    )
df = df.loc[df["_observed"].eq(True)].drop(columns="_observed")

# Zero dividends need no share inputs. All other missing flow inputs propagate.
df["tempDiv"] = (df["dvpsxq"] * df["cshoq"] * df["ajexq"]).mask(df["dvpsxq"].eq(0), 0)
df["preferred_reduction"] = (df["l3_pstkq"] - df["pstkq"]).clip(lower=0).fillna(0)
# prstkcyq and sstkyq are already individual-quarter flows from the downloader.
df["gross_payout"] = df["tempDiv"] + df["prstkcyq"] + df["preferred_reduction"]
df["preferred_increase"] = (df["pstkq"] - df["l3_pstkq"]).clip(lower=0).fillna(0)
df["equity_issuance"] = df["sstkyq"] - df["preferred_increase"]
df["NetPayoutYield_q"] = (df["gross_payout"] - df["equity_issuance"]) / df["mve_permco"]

# Require observed, finite, positive market cap and finite nonzero net yield.
df = df.loc[
    np.isfinite(df["mve_permco"]) & (df["mve_permco"] > 0)
    & np.isfinite(df["NetPayoutYield_q"]) & (df["NetPayoutYield_q"] != 0)
]
result = save_placebo(df[["permno", "time_avail_m", "NetPayoutYield_q"]], "NetPayoutYield_q")
