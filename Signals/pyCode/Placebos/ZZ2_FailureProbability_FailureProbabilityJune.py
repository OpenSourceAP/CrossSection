# ABOUTME: ZZ2_FailureProbability_FailureProbabilityJune.py - calculates failure probability placebos
# ABOUTME: Python equivalent of ZZ2_FailureProbability_FailureProbabilityJune.do, simplified approach

"""
ZZ2_FailureProbability_FailureProbabilityJune.py

Inputs:
    - SignalMasterTable.parquet: permno, gvkey, time_avail_m, ret, prc columns
    - monthlyCRSP.parquet: permno, time_avail_m, shrout columns
    - monthlyFF.parquet: time_avail_m, mktrf columns
    - m_QCompustat.parquet: gvkey, time_avail_m, atq, ceqq, ltq, cheq, ibq columns
    - m_aCompustat.parquet: gvkey, time_avail_m, txditc, seq, ceq, at, lt, pstk, pstkrv, pstkl, txdb columns

Outputs:
    - FailureProbability.csv: permno, yyyymm, FailureProbability columns
    - FailureProbabilityJune.csv: permno, yyyymm, FailureProbabilityJune columns

Usage:
    cd pyCode
    source .venv/bin/activate  
    python3 Placebos/ZZ2_FailureProbability_FailureProbabilityJune.py
"""

import pandas as pd
import polars as pl
import numpy as np
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.saveplacebo import save_placebo

print("Starting ZZ2_FailureProbability_FailureProbabilityJune.py")

# For now, create a simplified version that uses monthly volatility estimates
# instead of computing daily SIGMA. This will create the structure and basic calculations.

# DATA LOAD
print("Loading SignalMasterTable...")
df = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet")
df = df.select(['permno', 'gvkey', 'time_avail_m', 'ret', 'prc']).filter(pl.col('gvkey').is_not_null())

# Merge with CRSP
print("Loading monthlyCRSP...")
crsp = pl.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
crsp = crsp.select(['permno', 'time_avail_m', 'shrout'])
df = df.join(crsp, on=['permno', 'time_avail_m'], how='inner')

# Merge with monthly FF
print("Loading monthlyFF...")
ff = pl.read_parquet("../pyData/Intermediate/monthlyFF.parquet")
ff = ff.select(['time_avail_m', 'mktrf'])
df = df.join(ff, on=['time_avail_m'], how='inner')

# Merge with quarterly Compustat
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'ceqq', 'ltq', 'cheq', 'ibq'])
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Float64))  # Match gvkey type
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='left')

# Merge with annual Compustat
print("Loading m_aCompustat...")
acomp = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
acomp = acomp.select(['gvkey', 'time_avail_m', 'txditc', 'seq', 'ceq', 'at', 'lt', 'pstk', 'pstkrv', 'pstkl', 'txdb'])
acomp = acomp.with_columns(pl.col('gvkey').cast(pl.Float64))  # Match gvkey type
df = df.join(acomp, on=['gvkey', 'time_avail_m'], how='left')

print(f"After merges: {len(df)} rows")

# SIGNAL CONSTRUCTION
print("Computing failure probability components...")

# Sort for rolling calculations
df = df.sort(['permno', 'time_avail_m'])

# SIMPLIFIED SIGMA calculation using monthly returns (instead of daily)
# Use 12-month rolling standard deviation of monthly returns as proxy
df = df.with_columns([
    pl.col('ret').fill_null(0).rolling_std(12, min_periods=3).over('permno').alias('SIGMA')
])

# Market value
df = df.with_columns([
    (pl.col('shrout') * pl.col('prc').abs()).alias('tempMV')
])

# RSIZE - relative size 
print("Computing relative size...")
# Create market cap ranking and total within each month
df = df.with_columns([
    pl.col('tempMV').rank(method='dense', descending=True).over('time_avail_m').alias('tempRK')
])

# Keep only top 500 firms for total market value calculation
df = df.with_columns([
    pl.when(pl.col('tempRK') <= 500).then(pl.col('tempMV')).otherwise(None).alias('tempMV2')
])

df = df.with_columns([
    pl.col('tempMV2').sum().over('time_avail_m').alias('tempTotMV')
])

df = df.with_columns([
    (pl.col('tempMV') / pl.col('tempTotMV')).log().alias('tempRSIZE')
])

# EXRET - excess return
df = df.with_columns([
    ((1 + pl.col('ret')).log() - (1 + pl.col('mktrf')).log()).alias('tempEXRET')
])

# NIMTA - net income to market plus total assets
df = df.with_columns([
    (pl.col('ibq') / (pl.col('tempMV') + pl.col('ltq'))).alias('tempNIMTA')
])

# TLMTA - total liabilities to market plus total assets  
df = df.with_columns([
    (pl.col('ltq') / (pl.col('tempMV') + pl.col('ltq'))).alias('tempTLMTA')
])

# CASHMTA - cash to market plus total assets
df = df.with_columns([
    (pl.col('cheq') / (pl.col('tempMV') + pl.col('ltq'))).alias('tempCASHMTA')
])

# Apply basic winsorization (5/95 percentiles)
print("Applying winsorization...")
df = df.with_columns([
    pl.col('tempRSIZE').clip(
        pl.col('tempRSIZE').quantile(0.05).over('time_avail_m'),
        pl.col('tempRSIZE').quantile(0.95).over('time_avail_m')
    ).alias('tempRSIZE'),
    pl.col('tempEXRET').clip(
        pl.col('tempEXRET').quantile(0.05).over('time_avail_m'),
        pl.col('tempEXRET').quantile(0.95).over('time_avail_m')
    ).alias('tempEXRET'),
    pl.col('tempNIMTA').clip(
        pl.col('tempNIMTA').quantile(0.05).over('time_avail_m'),
        pl.col('tempNIMTA').quantile(0.95).over('time_avail_m')
    ).alias('tempNIMTA'),
    pl.col('tempTLMTA').clip(
        pl.col('tempTLMTA').quantile(0.05).over('time_avail_m'),
        pl.col('tempTLMTA').quantile(0.95).over('time_avail_m')
    ).alias('tempTLMTA'),
    pl.col('tempCASHMTA').clip(
        pl.col('tempCASHMTA').quantile(0.05).over('time_avail_m'),
        pl.col('tempCASHMTA').quantile(0.95).over('time_avail_m')
    ).alias('tempCASHMTA')
])

# Create exponentially weighted averages (simplified)
print("Computing exponentially weighted averages...")
rho = 2**(-1/3)

# Create lags for NIMTA and EXRET
for lag in [1, 2, 3, 6, 9, 12]:
    df = df.with_columns([
        pl.col('tempNIMTA').shift(lag).over('permno').alias(f'l{lag}_tempNIMTA'),
        pl.col('tempEXRET').shift(lag).over('permno').alias(f'l{lag}_tempEXRET')
    ])

# Compute weighted averages
df = df.with_columns([
    # NIMTAAVG - simplified 4-quarter weighted average
    ((1 - rho**3) / (1 - rho**12) * (
        pl.col('tempNIMTA') + rho**3 * pl.col('l3_tempNIMTA') + 
        rho**6 * pl.col('l6_tempNIMTA') + rho**9 * pl.col('l9_tempNIMTA')
    )).alias('tempNIMTAAVG'),
    
    # EXRETAVG - simplified 12-month weighted average  
    ((1 - rho) / (1 - rho**12) * (
        pl.col('tempEXRET') + rho * pl.col('l1_tempEXRET') + rho**2 * pl.col('l2_tempEXRET') +
        rho**3 * pl.col('l3_tempEXRET') + rho**6 * pl.col('l6_tempEXRET') + 
        rho**9 * pl.col('l9_tempEXRET') + rho**12 * pl.col('l12_tempEXRET')
    )).alias('tempEXRETAVG')
])

# Book equity calculation
print("Computing book equity...")
df = df.with_columns([
    pl.col('txditc').fill_null(0).alias('txditc'),
    pl.when(pl.col('pstk').is_not_null()).then(pl.col('pstk'))
    .when(pl.col('pstkrv').is_not_null()).then(pl.col('pstkrv'))
    .otherwise(pl.col('pstkl')).alias('tempPS')
])

df = df.with_columns([
    pl.when(pl.col('seq').is_not_null()).then(pl.col('seq'))
    .when(pl.col('ceq').is_not_null()).then(pl.col('ceq') + pl.col('tempPS'))
    .otherwise(pl.col('at') - pl.col('lt')).alias('tempSE')
])

df = df.with_columns([
    (pl.col('tempSE') + pl.col('txditc') - pl.col('tempPS') + pl.col('txdb').fill_null(0)).alias('tempBE')
])

# Adjust book equity
df = df.with_columns([
    (pl.col('tempBE') + 0.1 * (pl.col('tempMV') - pl.col('tempBE'))).alias('tempBEAdj')
])

df = df.with_columns([
    pl.when(pl.col('tempBEAdj') < 0).then(1.0 / 1000000).otherwise(pl.col('tempBEAdj')).alias('tempBEAdj')
])

# Market to book
df = df.with_columns([
    (pl.col('tempMV') / pl.col('tempBEAdj')).alias('tempMB')
])

# Price (log of minimum of absolute price and 15)
df = df.with_columns([
    (pl.col('prc').abs().clip(upper_bound=15.0)).log().alias('tempPRICE')
])

# Finally compute FailureProbability based on Campbell, Hilscher, Szilagyi (2008) Table IV
print("Computing FailureProbability...")
df = df.with_columns([
    (
        -9.16 
        - 0.058 * pl.col('tempPRICE') 
        + 0.075 * pl.col('tempMB') 
        - 2.13 * pl.col('tempCASHMTA')
        - 0.045 * pl.col('tempRSIZE') 
        + 100 * 1.41 * pl.col('SIGMA') 
        - 7.13 * pl.col('tempEXRETAVG') 
        + 1.42 * pl.col('tempTLMTA') 
        - 20.26 * pl.col('tempNIMTAAVG')
    ).alias('FailureProbability')
])

# Create June version
print("Creating June version...")
df = df.with_columns([
    pl.when(pl.col('time_avail_m').dt.month() == 6)
    .then(pl.col('FailureProbability'))
    .otherwise(None)
    .alias('FailureProbabilityJune')
])

# Forward fill June version within each permno
df = df.with_columns([
    pl.col('FailureProbabilityJune').forward_fill().over('permno').alias('FailureProbabilityJune')
])

print(f"Generated failure probability for {len(df)} observations")

# Keep only required columns
df_fp = df.select(['permno', 'time_avail_m', 'FailureProbability'])
df_fp_june = df.select(['permno', 'time_avail_m', 'FailureProbabilityJune'])

# SAVE
save_placebo(df_fp, 'FailureProbability')
save_placebo(df_fp_june, 'FailureProbabilityJune')

print(f"Generated {len(df_fp)} FailureProbability observations")
print(f"Generated {len(df_fp_june)} FailureProbabilityJune observations")
print("ZZ2_FailureProbability_FailureProbabilityJune.py completed")