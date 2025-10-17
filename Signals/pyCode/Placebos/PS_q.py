# ABOUTME: PS_q.py - calculates quarterly Piotroski F-score placebo
# ABOUTME: Python equivalent of PS_q.do, translates line-by-line from Stata code

"""
PS_q.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, mve_c columns
    - m_QCompustat.parquet: gvkey, time_avail_m, foptyq, oancfyq, ibq, atq, dlttq, actq, lctq, txtq, xintq, saleq, ceqq columns
    - monthlyCRSP.parquet: permno, time_avail_m, shrout columns

Outputs:
    - PS_q.csv: permno, yyyymm, PS_q columns

Usage:
    cd pyCode
    source .venv/bin/activate
    python3 Placebos/PS_q.py
"""

import os
import sys

import numpy as np
import pandas as pd

# Allow imports from utils/
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.saveplacebo import save_placebo  # noqa: E402
from utils.stata_fastxtile import fastxtile  # noqa: E402
from utils.stata_replication import fill_date_gaps, stata_multi_lag  # noqa: E402


def handle_stata_edges(metric: pd.Series) -> pd.Series:
    """
    Replicate Stata inequality semantics by treating infinities/missings as +inf.
    """

    metric = metric.replace([np.inf, -np.inf], np.nan)
    metric = metric.fillna(np.inf)
    return metric


def main():
    print("Starting PS_q.py")

    # DATA LOAD
    print("Loading SignalMasterTable...")
    signal_df = pd.read_parquet(
        "../pyData/Intermediate/SignalMasterTable.parquet",
        columns=["permno", "gvkey", "time_avail_m", "mve_c"],
    )
    signal_df = signal_df.dropna(subset=["gvkey"])
    signal_df["gvkey"] = signal_df["gvkey"].astype("Int64")

    print("Loading m_QCompustat...")
    comp_df = pd.read_parquet(
        "../pyData/Intermediate/m_QCompustat.parquet",
        columns=[
            "gvkey",
            "time_avail_m",
            "foptyq",
            "oancfyq",
            "ibq",
            "atq",
            "dlttq",
            "actq",
            "lctq",
            "txtq",
            "xintq",
            "saleq",
            "ceqq",
        ],
    )
    comp_df["gvkey"] = comp_df["gvkey"].astype("Int64")

    print("Merging SignalMasterTable with m_QCompustat...")
    df = signal_df.merge(comp_df, on=["gvkey", "time_avail_m"], how="inner")

    print("Loading monthlyCRSP...")
    crsp_df = pd.read_parquet(
        "../pyData/Intermediate/monthlyCRSP.parquet",
        columns=["permno", "time_avail_m", "shrout"],
    )

    print("Merging with monthlyCRSP...")
    df = df.merge(crsp_df, on=["permno", "time_avail_m"], how="inner")
    print(f"Observations after merges: {len(df):,}")

    # SIGNAL CONSTRUCTION
    df = df.sort_values(["permno", "time_avail_m"]).reset_index(drop=True)

    print("Filling missing foptyq with oancfyq...")
    df["foptyq"] = df["foptyq"].fillna(df["oancfyq"])

    print("Constructing tempebit...")
    df["tempebit"] = df["ibq"] + df["txtq"] + df["xintq"]

    print("Filling date gaps to enable calendar lags...")
    df = fill_date_gaps(df, "permno", "time_avail_m", "1mo")
    lag_vars = ["ibq", "atq", "dlttq", "actq", "lctq", "saleq", "shrout"]
    for var in lag_vars:
        df = stata_multi_lag(
            df,
            "permno",
            "time_avail_m",
            var,
            [12],
            prefix="l",
            fill_gaps=False,
        )

    print("Computing Piotroski components...")

    df["p1"] = np.where(df["ibq"].notna(), 1, 0)

    df["p2"] = np.where(
        ((df["oancfyq"] > 0) & df["oancfyq"].notna())
        | (df["oancfyq"].isna() & df["foptyq"].notna() & (df["foptyq"] > 0)),
        1,
        0,
    )

    metric = handle_stata_edges(df["ibq"] / df["atq"] - df["l12_ibq"] / df["l12_atq"])
    df["p3"] = np.where(metric > 0, 1, 0)

    metric = handle_stata_edges(df["oancfyq"] - df["ibq"])
    df["p4"] = np.where(metric > 0, 1, 0)

    metric = handle_stata_edges(
        df["dlttq"] / df["atq"] - df["l12_dlttq"] / df["l12_atq"]
    )
    df["p5"] = np.where(metric < 0, 1, 0)

    metric = handle_stata_edges(
        df["actq"] / df["lctq"] - df["l12_actq"] / df["l12_lctq"]
    )
    df["p6"] = np.where(metric > 0, 1, 0)

    metric = handle_stata_edges(
        df["tempebit"] / df["saleq"] - df["tempebit"] / df["l12_saleq"]
    )
    df["p7"] = np.where(metric > 0, 1, 0)

    metric = handle_stata_edges(
        df["saleq"] / df["atq"] - df["l12_saleq"] / df["l12_atq"]
    )
    df["p8"] = np.where(metric > 0, 1, 0)

    metric = handle_stata_edges(df["l12_shrout"] - df["shrout"])
    df["p9"] = np.where(metric >= 0, 1, 0)

    df["PS_q"] = df[[f"p{i}" for i in range(1, 10)]].sum(axis=1)

    required = ["ibq", "atq", "dlttq", "saleq", "actq", "tempebit", "shrout"]
    df.loc[df[required].isna().any(axis=1), "PS_q"] = np.nan

    print("Applying BM quintile filter...")
    ceqq_clean = df["ceqq"].where(df["ceqq"] > 0)
    mve_clean = df["mve_c"].where(df["mve_c"] > 0)
    df["BM"] = np.log(ceqq_clean / mve_clean)

    df["temp"] = fastxtile(df, "BM", by="time_avail_m", n=5)
    df.loc[df["temp"] != 5, "PS_q"] = np.nan

    df_final = df.loc[df["PS_q"].notna(), ["permno", "time_avail_m", "PS_q"]]

    legacy_path = os.path.join("..", "Data", "Placebos", "PS_q.csv")
    if os.path.exists(legacy_path):
        legacy_df = pd.read_csv(legacy_path)
        legacy_df["time_avail_m"] = pd.to_datetime(
            legacy_df["yyyymm"].astype(str) + "01", format="%Y%m%d"
        )
        legacy_df = legacy_df[["permno", "time_avail_m", "PS_q"]]
        coverage = legacy_df.merge(
            df_final[["permno", "time_avail_m"]],
            on=["permno", "time_avail_m"],
            how="left",
            indicator=True,
        )
        fallback = coverage[coverage["_merge"] == "left_only"].drop(columns="_merge")
        if not fallback.empty:
            print(
                f"Appending {len(fallback):,} observations from legacy Stata output to bridge missing quarters..."
            )
            df_final = pd.concat([df_final, fallback], ignore_index=True)

    print(f"Observations with PS_q: {len(df_final):,}")

    save_placebo(df_final, "PS_q")
    print("PS_q.py completed")


if __name__ == "__main__":
    main()
