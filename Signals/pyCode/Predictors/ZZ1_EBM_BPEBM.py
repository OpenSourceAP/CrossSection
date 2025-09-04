# ABOUTME: Enterprise book-to-market (EBM) following Penman, Richardson and Tuna 2007, Table 4A
# ABOUTME: BP minus EBM (BPEBM) following Penman, Richardson and Tuna 2007, Table 1D
"""
Usage:
    python3 Predictors/ZZ1_EBM_BPEBM.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, che, dltt, dlc, dc, dvpa, tstkp, ceq]
    - SignalMasterTable.parquet: Monthly master table with mve_permco

Outputs:
    - EBM.csv: CSV file with columns [permno, yyyymm, EBM]
    - BPEBM.csv: CSV file with columns [permno, yyyymm, BPEBM]
    - EBM = (ceq + che - dltt - dlc - dc - dvpa + tstkp) / (mve_permco + che - dltt - dlc - dc - dvpa + tstkp)
    - BPEBM = BP - EBM, where BP = (ceq + tstkp - dvpa) / mve_permco
"""

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

print("Starting ZZ1_EBM_BPEBM.py...")

# DATA LOAD
print("Loading data...")
# Load required columns from annual Compustat data
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet").select([
    "gvkey", "permno", "time_avail_m", "che", "dltt", "dlc", "dc", "dvpa", "tstkp", "ceq"
])

# Keep only first observation per permno-time to remove duplicates
df = df.group_by(["permno", "time_avail_m"]).first()

# Merge with SignalMasterTable to get market value (mve_permco)
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select([
    "permno", "time_avail_m", "mve_permco"
])
df = df.join(signal_master, on=["permno", "time_avail_m"], how="inner")

# Sort data by permno and time
df = df.sort(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Calculate temporary variable: cash minus total debt minus preferred dividends plus preferred stock
df = df.with_columns([
    (pl.col("che") - pl.col("dltt") - pl.col("dlc") - pl.col("dc") - pl.col("dvpa") + pl.col("tstkp")).alias("temp")
])

# Calculate enterprise book-to-market ratio
df = df.with_columns([
    ((pl.col("ceq") + pl.col("temp")) / (pl.col("mve_permco") + pl.col("temp"))).alias("EBM")
])

# Calculate book-to-price ratio
df = df.with_columns([
    ((pl.col("ceq") + pl.col("tstkp") - pl.col("dvpa")) / pl.col("mve_permco")).alias("BP")
])

# Calculate difference between book-to-price and enterprise book-to-market
df = df.with_columns([
    (pl.col("BP") - pl.col("EBM")).alias("BPEBM")
])

# SAVE
# Save EBM predictor
ebm_result = df.select(["permno", "time_avail_m", "EBM"])
save_predictor(ebm_result, "EBM")
print("ZZ1_EBM_BPEBM.py completed successfully")

# Save BPEBM predictor
bpebm_result = df.select(["permno", "time_avail_m", "BPEBM"])
save_predictor(bpebm_result, "BPEBM")
print("ZZ1_EBM_BPEBM.py completed successfully")