# ABOUTME: OperProfLag_q.py - calculates quarterly operating profits to lagged equity placebo
# ABOUTME: Python equivalent of OperProfLag_q.do, translated directly from Stata logic

"""
Inputs:
    - Signals/pyData/Intermediate/SignalMasterTable.parquet providing permno, gvkey, time_avail_m
    - Signals/pyData/Intermediate/m_QCompustat.parquet providing cogsq, xsgaq, xintq, revtq, seqq, ceqq, pstkq, atq, ltq, txditcq
Outputs:
    - Signals/pyData/Placebos/OperProfLag_q.csv with permno, yyyymm, OperProfLag_q
How to run:
    source ~/venvloc/openalpha/bin/activate
    cd Signals/pyCode
    python Placebos/OperProfLag_q.py
Example:
    python Placebos/OperProfLag_q.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import polars as pl

# Add parent directory to path to import utils
BASE_DIR = Path(__file__).resolve().parent
PYCODE_DIR = BASE_DIR.parent
SIGNALS_ROOT = PYCODE_DIR.parent
DATA_INTERMEDIATE = SIGNALS_ROOT / "pyData" / "Intermediate"
sys.path.append(str(PYCODE_DIR))

from utils.saveplacebo import save_placebo


def main() -> None:
    print("Starting OperProfLag_q.py")

    signal_master_path = DATA_INTERMEDIATE / "SignalMasterTable.parquet"
    qcomp_path = DATA_INTERMEDIATE / "m_QCompustat.parquet"

    print(f"Loading {signal_master_path.name}...")
    signal_master = (
        pl.read_parquet(signal_master_path)
        .select(["permno", "gvkey", "time_avail_m"])
        .filter(pl.col("gvkey").is_not_null())
        .with_columns(pl.col("gvkey").cast(pl.Int64, strict=False))
    )
    print(f"Signal master after gvkey filter: {signal_master.height} rows")

    print(f"Loading {qcomp_path.name}...")
    qcomp = (
        pl.read_parquet(qcomp_path)
        .select(
            [
                "gvkey",
                "time_avail_m",
                "cogsq",
                "xsgaq",
                "xintq",
                "revtq",
                "seqq",
                "ceqq",
                "pstkq",
                "atq",
                "ltq",
                "txditcq",
            ]
        )
        .with_columns(pl.col("gvkey").cast(pl.Int64, strict=False))
    )

    print("Performing 1:1 merge on gvkey and time_avail_m...")
    df = signal_master.join(qcomp, on=["gvkey", "time_avail_m"], how="inner")
    print(f"Rows after merge: {df.height}")

    df = df.with_columns(pl.col("txditcq").alias("txditcq_original"))
    df = df.with_columns(
        pl.when(pl.col("txditcq").is_null()).then(0).otherwise(pl.col("txditcq")).alias("txditcq")
    )
    df = df.with_columns(
        pl.when(pl.col("pstkq").is_null()).then(0).otherwise(pl.col("pstkq")).alias("pstkq_filled")
    )

    expense_cols = ["cogsq", "xsgaq", "xintq"]
    df = df.with_columns(
        [
            pl.when(pl.col(col).is_null()).then(0).otherwise(pl.col(col)).alias(f"temp_{col}")
            for col in expense_cols
        ]
    )

    df = df.with_columns(
        (
            pl.col("revtq")
            - pl.col("temp_cogsq")
            - pl.col("temp_xsgaq")
            - pl.col("temp_xintq")
        ).alias("OperProfLag_q")
    )

    df = df.with_columns(
        pl.when(
            pl.col("cogsq").is_null()
            & pl.col("xsgaq").is_null()
            & pl.col("xintq").is_null()
        )
        .then(pl.lit(None))
        .otherwise(pl.col("OperProfLag_q"))
        .alias("OperProfLag_q")
    )

    df = df.with_columns(pl.col("seqq").alias("tempSE"))
    df = df.with_columns(
        pl.when(pl.col("tempSE").is_null())
        .then(pl.col("ceqq") + pl.col("pstkq_filled"))
        .otherwise(pl.col("tempSE"))
        .alias("tempSE")
    )
    df = df.with_columns(
        pl.when(pl.col("tempSE").is_null())
        .then(pl.col("atq") - pl.col("ltq"))
        .otherwise(pl.col("tempSE"))
        .alias("tempSE")
    )

    df = df.with_columns(
        (pl.col("tempSE") + pl.col("txditcq") - pl.col("pstkq_filled")).alias("denom_operprof")
    )
    df = df.with_columns(
        pl.when(
            pl.col("denom_operprof").is_null() | (pl.col("denom_operprof") == 0)
        )
        .then(pl.lit(None))
        .otherwise(pl.col("OperProfLag_q") / pl.col("denom_operprof"))
        .alias("OperProfLag_q")
    )

    df = df.with_columns(
        (pl.col("tempSE") - pl.col("pstkq_filled")).alias("denom_txdit_missing")
    )
    df = df.with_columns(
        pl.when(pl.col("txditcq_original").is_null())
        .then(
            pl.when(
                pl.col("denom_txdit_missing").is_null()
                | (pl.col("denom_txdit_missing") == 0)
            )
            .then(pl.lit(None))
            .otherwise(pl.col("OperProfLag_q") / pl.col("denom_txdit_missing"))
        )
        .otherwise(pl.col("OperProfLag_q"))
        .alias("OperProfLag_q")
    )

    columns_to_drop = [
        *(f"temp_{col}" for col in expense_cols),
        "tempSE",
        "denom_operprof",
        "denom_txdit_missing",
        "txditcq_original",
        "pstkq_filled",
    ]
    df = df.drop([col for col in columns_to_drop if col in df.columns])

    df_final = df.select(["permno", "time_avail_m", "OperProfLag_q"])

    save_placebo(df_final, "OperProfLag_q")

    print("OperProfLag_q.py completed")


if __name__ == "__main__":
    main()
