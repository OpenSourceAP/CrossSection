# ABOUTME: Turnover volatility predictor using 36-month rolling standard deviation of turnover
# ABOUTME: Usage: python3 std_turn.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile

# Data load
monthly_crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = monthly_crsp.select(["permno", "time_avail_m", "vol", "shrout", "prc"])

# Sort by permno and time to ensure proper rolling window calculation
df = df.sort(["permno", "time_avail_m"])

# Signal construction
df = df.with_columns([
    # Generate turnover
    (pl.col("vol") / pl.col("shrout")).alias("tempturn"),
    # Market value
    (pl.col("shrout") * pl.col("prc").abs()).alias("mve_c")
])

# Rolling standard deviation of turnover using 36-month window, min 24 observations
df = df.with_columns(
    pl.col("tempturn")
    .rolling_std(window_size=36, min_samples=24)
    .over("permno")
    .alias("std_turn")
)

# Size quintiles by time_avail_m using fastxtile helper
# Convert to pandas for fastxtile, then back to polars
df_pandas = df.to_pandas()
df_pandas['tempqsize'] = fastxtile(df_pandas, 'mve_c', by='time_avail_m', n=5)
df = pl.from_pandas(df_pandas)

# Set to null for size quintiles 4 and 5 (tiny spread per OP Tab3B)
df = df.with_columns(
    pl.when(pl.col("tempqsize") >= 4)
    .then(None)
    .otherwise(pl.col("std_turn"))
    .alias("std_turn")
)

# Select final data
result = df.select(["permno", "time_avail_m", "std_turn"])

# Save predictor
save_predictor(result, "std_turn")