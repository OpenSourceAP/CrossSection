# ABOUTME: Operating leverage following Novy-Marx 2011, Table 3b
# ABOUTME: Sum of administrative expenses and cost of goods sold, scaled by total assets

"""
OPLeverage.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/OPLeverage.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, xsga, cogs, at]

Outputs:
    - OPLeverage.csv: CSV file with columns [permno, yyyymm, OPLeverage]
"""

import polars as pl
from pathlib import Path
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.save_standardized import save_predictor

# DATA LOAD
print("Loading m_aCompustat data...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")

# Select only the columns we need
df = df.select(["gvkey", "permno", "time_avail_m", "xsga", "cogs", "at"])

print(f"Loaded {len(df)} observations")

# SIGNAL CONSTRUCTION
# Remove duplicate permno-time_avail_m observations
df = df.group_by(["permno", "time_avail_m"]).first()
print(f"After removing duplicates: {len(df)} observations")

# Set missing SGA expenses to zero
df = df.with_columns(
    [
        pl.when(pl.col("xsga").is_null())
        .then(0)
        .otherwise(pl.col("xsga"))
        .alias("tempxsga")
    ]
)

# Calculate operating leverage: (SGA + COGS) / Total Assets
df = df.with_columns(
    [((pl.col("tempxsga") + pl.col("cogs")) / pl.col("at")).alias("OPLeverage")]
)

print(
    f"Calculated OPLeverage for {df.filter(pl.col('OPLeverage').is_not_null()).count()} observations"
)

# SAVE
save_predictor(df, "OPLeverage")

print("OPLeverage predictor completed successfully")
