# ABOUTME: Short-term reversal predictor - current month return
# ABOUTME: Usage: python3 STreversal.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# Data load
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")

# Select required columns
df = signal_master.select(["permno", "time_avail_m", "ret"])

# Signal construction
df = df.with_columns([
    # Fill missing returns with 0 and use as STreversal
    pl.col("ret").fill_null(0).alias("STreversal")
])

# Select final data
result = df.select(["permno", "time_avail_m", "STreversal"])

# Save predictor
save_predictor(result, "STreversal")