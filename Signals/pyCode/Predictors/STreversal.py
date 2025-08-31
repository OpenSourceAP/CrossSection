# ABOUTME: Short-term reversal following Jegadeesh 1990, Table 2, Jan-Dec
# ABOUTME: calculates stock return over the previous month (1-month momentum/reversal)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting STreversal.py...")

# Data load
print("Loading SignalMasterTable...")
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")

# Select required columns
df = signal_master.select(["permno", "time_avail_m", "ret"])
print(f"Loaded data: {df.shape[0]} rows")

# Signal construction
print("Calculating STreversal...")
df = df.with_columns([
    # Fill missing returns with 0 and use as STreversal
    pl.col("ret").fill_null(0).alias("STreversal")
])

# Select final data
result = df.select(["permno", "time_avail_m", "STreversal"])
print(f"Calculated STreversal for {result.shape[0]} observations")

# Save predictor
save_predictor(result, "STreversal")
print("STreversal.py completed successfully")