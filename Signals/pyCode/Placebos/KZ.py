# ABOUTME: KZ.py - calculates Kaplan-Zingales financial constraints index placebo
# ABOUTME: Python equivalent of KZ.do, translates line-by-line from Stata code

"""
KZ.py

Inputs:
    - m_aCompustat.parquet: permno, time_avail_m, ib, dp, ppent, at, ceq, txdb, dlc, dltt, seq, dvc, dvp, che columns
    - SignalMasterTable.parquet: permno, time_avail_m, mve_c columns

Outputs:
    - KZ.csv: permno, yyyymm, KZ columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/KZ.py
"""

import pandas as pd
import polars as pl
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting KZ.py")

# DATA LOAD
# use "$pathDataIntermediate/m_aCompustat", clear
print("Loading m_aCompustat...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")

print(f"After loading m_aCompustat: {len(df)} rows")

# bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
print("Removing duplicates...")
df = df.unique(subset=['permno', 'time_avail_m'], maintain_order=True)

print(f"After removing duplicates: {len(df)} rows")

# merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c)
print("Loading SignalMasterTable...")
signal = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
signal = signal.select(['permno', 'time_avail_m', 'mve_c'])

print("Merging with SignalMasterTable...")
df = df.join(signal, on=['permno', 'time_avail_m'], how='inner')

print(f"After merge with SignalMasterTable: {len(df)} rows")

# SIGNAL CONSTRUCTION
# KZ = -1.002* (ib + dp)/ppent + .283*(at + mve_c - ceq - txdb)/at + 3.139*(dlc + dltt)/(dlc + dltt + seq) - 39.368*((dvc+dvp)/ppent) - 1.315*(che/ppent)
print("Computing KZ index...")

# Build the KZ formula step by step
df = df.with_columns([
    # Term 1: -1.002 * (ib + dp)/ppent
    (-1.002 * (pl.col('ib') + pl.col('dp')) / pl.col('ppent')).alias('term1'),
    
    # Term 2: 0.283 * (at + mve_c - ceq - txdb)/at
    (0.283 * (pl.col('at') + pl.col('mve_c') - pl.col('ceq') - pl.col('txdb')) / pl.col('at')).alias('term2'),
    
    # Term 3: 3.139 * (dlc + dltt)/(dlc + dltt + seq)
    (3.139 * (pl.col('dlc') + pl.col('dltt')) / (pl.col('dlc') + pl.col('dltt') + pl.col('seq'))).alias('term3'),
    
    # Term 4: -39.368 * ((dvc + dvp)/ppent)
    (-39.368 * (pl.col('dvc') + pl.col('dvp')) / pl.col('ppent')).alias('term4'),
    
    # Term 5: -1.315 * (che/ppent)
    (-1.315 * pl.col('che') / pl.col('ppent')).alias('term5')
])

# Sum all terms to get KZ
df = df.with_columns([
    (pl.col('term1') + pl.col('term2') + pl.col('term3') + pl.col('term4') + pl.col('term5')).alias('KZ')
])

print(f"Generated KZ for {len(df)} observations")

# Keep only required columns for output
df_final = df.select(['permno', 'time_avail_m', 'KZ'])

# SAVE
# do "$pathCode/saveplacebo" KZ
save_placebo(df_final, 'KZ')

print("KZ.py completed")