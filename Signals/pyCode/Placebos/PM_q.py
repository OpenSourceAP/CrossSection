"""
PM_q.py

Inputs:
    - Signals/pyData/Intermediate/SignalMasterTable.parquet
    - Signals/pyData/Intermediate/m_QCompustat.parquet

Outputs:
    - Signals/pyData/Placebos/PM_q.csv

How to run:
    source ~/venvloc/openalpha/bin/activate
    python Placebos/PM_q.py
"""

from pathlib import Path
import sys

import polars as pl

ROOT_DIR = Path(__file__).resolve().parents[1]
PYDATA_INTERMEDIATE = ROOT_DIR / "pyData" / "Intermediate"

sys.path.append(str(ROOT_DIR))
from utils.saveplacebo import save_placebo


def main() -> None:
    """Replicate the Stata PM_q placebo: profit margin equals niq / revtq."""
    print("Starting PM_q.py")

    print("Loading SignalMasterTable...")
    signal_master = (
        pl.read_parquet(PYDATA_INTERMEDIATE / "SignalMasterTable.parquet")
        .select(["permno", "gvkey", "time_avail_m"])
        .filter(pl.col("gvkey").is_not_null())
        .with_columns(pl.col("gvkey").cast(pl.Int64))
    )

    print("Loading m_QCompustat...")
    qcomp = (
        pl.read_parquet(PYDATA_INTERMEDIATE / "m_QCompustat.parquet")
        .select(["gvkey", "time_avail_m", "niq", "revtq"])
        .with_columns(pl.col("gvkey").cast(pl.Int64))
    )

    print("Merging SignalMasterTable with m_QCompustat...")
    merged = signal_master.join(qcomp, on=["gvkey", "time_avail_m"], how="left")

    print("Computing PM_q...")
    merged = merged.with_columns(
        pl.when(pl.col("revtq").is_null() | (pl.col("revtq") == 0))
        .then(None)
        .otherwise(pl.col("niq") / pl.col("revtq"))
        .alias("PM_q")
    )

    df_final = merged.select(["permno", "time_avail_m", "PM_q"])

    print("Saving PM_q placebo...")
    save_placebo(df_final, "PM_q")

    print("PM_q.py completed")


if __name__ == "__main__":
    main()
