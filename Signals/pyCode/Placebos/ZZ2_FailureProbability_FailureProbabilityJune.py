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
from utils.save_standardized import save_placebo
from utils.stata_replication import stata_multi_lag

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

# Merge with quarterly Compustat (Stata: keep(match) = inner join)
print("Loading m_QCompustat...")
qcomp = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet")
qcomp = qcomp.select(['gvkey', 'time_avail_m', 'atq', 'ceqq', 'ltq', 'cheq', 'ibq'])
qcomp = qcomp.with_columns(pl.col('gvkey').cast(pl.Float64))  # Match gvkey type
df = df.join(qcomp, on=['gvkey', 'time_avail_m'], how='inner')

# Merge with annual Compustat (Stata: keep(match) = inner join)  
print("Loading m_aCompustat...")
acomp = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")
acomp = acomp.select(['gvkey', 'time_avail_m', 'txditc', 'seq', 'ceq', 'at', 'lt', 'pstk', 'pstkrv', 'pstkl', 'txdb'])
acomp = acomp.with_columns(pl.col('gvkey').cast(pl.Float64))  # Match gvkey type
df = df.join(acomp, on=['gvkey', 'time_avail_m'], how='inner')

print(f"After merges: {len(df)} rows")

# SIGNAL CONSTRUCTION
print("Computing failure probability components...")

# SIGMA CALCULATION (matching Stata's approach)
print("Computing SIGMA from daily returns...")

# Load daily CRSP data
daily_crsp = pl.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_crsp = daily_crsp.select(['permno', 'time_d', 'ret'])
daily_crsp = daily_crsp.filter(pl.col('time_d') >= pd.to_datetime('1960-12-31'))

# Sort for rolling calculations
daily_crsp = daily_crsp.sort(['permno', 'time_d'])

# Create time sequence for asrol equivalent (rolling window based on trading days)
daily_crsp = daily_crsp.with_columns([
    pl.int_range(pl.len()).over('permno').alias('time_temp')
])

# Compute 3-month rolling standard deviation (60 business days, min 10 observations)
daily_crsp = daily_crsp.with_columns([
    pl.col('ret').rolling_std(60, min_periods=10).over('permno').alias('SIGMA')
])

# Drop missing SIGMA
daily_crsp = daily_crsp.filter(pl.col('SIGMA').is_not_null())

# Create monthly time_avail_m
daily_crsp = daily_crsp.with_columns([
    pl.col('time_d').dt.truncate('1mo').alias('time_avail_m')
])

# Keep last observation per permno-month (equivalent to gcollapse lastnm)
sigma_df = daily_crsp.sort(['permno', 'time_avail_m', 'time_d']).group_by(['permno', 'time_avail_m']).tail(1)
sigma_df = sigma_df.select(['permno', 'time_avail_m', 'SIGMA'])

print(f"Generated SIGMA for {len(sigma_df)} permno-months")

# Merge SIGMA back to main dataframe (Stata: keep(master match) = left join but keep both)
print("Merging SIGMA with main data...")
df = df.join(sigma_df, on=['permno', 'time_avail_m'], how='left')

# Sort main dataframe for subsequent calculations
df = df.sort(['permno', 'time_avail_m'])

# Market value
df = df.with_columns([
    (pl.col('shrout') * pl.col('prc').abs()).alias('tempMV')
])

# RSIZE - relative size 
print("Computing relative size...")
df = df.with_columns(pl.col('tempMV').alias('tempMV2'))
df = df.with_columns([
    pl.col('tempMV2').rank(method='ordinal', descending=True).over('time_avail_m').alias('tempRK')
])
df = df.with_columns([
    pl.when(pl.col('tempRK') <= 500).then(pl.col('tempMV2')).otherwise(None).alias('tempMV2')
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

# Apply basic winsorization (5/95 percentiles) across all temp* columns (matching Stata winsor2)
print("Applying winsorization...")
winsor_vars = [col for col in df.columns if col.startswith('temp')]
quantile_exprs = []
for var in winsor_vars:
    quantile_exprs.append(pl.col(var).quantile(0.05).alias(f'{var}_q05'))
    quantile_exprs.append(pl.col(var).quantile(0.95).alias(f'{var}_q95'))

quantile_bounds = df.select(quantile_exprs).to_dicts()[0]

df = df.with_columns([
    pl.col(var).clip(quantile_bounds[f'{var}_q05'], quantile_bounds[f'{var}_q95']).alias(var)
    for var in winsor_vars
])

# Create exponentially weighted averages (simplified)
print("Computing exponentially weighted averages...")
rho = 2**(-1/3)

# Create lags for NIMTA and EXRET using stata_multi_lag
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'tempNIMTA', list(range(1, 13)), prefix='l')
df = stata_multi_lag(df, 'permno', 'time_avail_m', 'tempEXRET', list(range(1, 13)), prefix='l')

# Compute weighted averages (matching Stata exactly)
df = df.with_columns([
    # NIMTAAVG - 4-quarter weighted average (Stata lines 58)
    ((1 - rho**3) / (1 - rho**12) * (
        pl.col('tempNIMTA') + rho**3 * pl.col('l3_tempNIMTA') + 
        rho**6 * pl.col('l6_tempNIMTA') + rho**9 * pl.col('l9_tempNIMTA')
    )).alias('tempNIMTAAVG'),
    
    # EXRETAVG - full 12-month weighted average (Stata lines 59-61)
    ((1 - rho) / (1 - rho**12) * (
        pl.col('tempEXRET') + 
        rho**1 * pl.col('l1_tempEXRET') + rho**2 * pl.col('l2_tempEXRET') +
        rho**3 * pl.col('l3_tempEXRET') + rho**4 * pl.col('l4_tempEXRET') + 
        rho**5 * pl.col('l5_tempEXRET') + rho**6 * pl.col('l6_tempEXRET') +
        rho**7 * pl.col('l7_tempEXRET') + rho**8 * pl.col('l8_tempEXRET') +
        rho**9 * pl.col('l9_tempEXRET') + rho**10 * pl.col('l10_tempEXRET') + 
        rho**11 * pl.col('l11_tempEXRET')
    )).alias('tempEXRETAVG')
])

# Book equity calculation
print("Computing book equity...")
df = df.with_columns([
    pl.col('txditc').fill_null(0).alias('txditc')
])

df = df.with_columns([
    pl.when(pl.col('pstk').is_not_null()).then(pl.col('pstk'))
    .when(pl.col('pstkrv').is_not_null()).then(pl.col('pstkrv'))
    .when(pl.col('pstkl').is_not_null()).then(pl.col('pstkl'))
    .otherwise(None).alias('tempPS')
])

df = df.with_columns([
    pl.col('seq').alias('tempSE')
])

df = df.with_columns([
    pl.col('tempSE').fill_null(pl.col('ceq') + pl.col('tempPS')).alias('tempSE')
])

df = df.with_columns([
    pl.col('tempSE').fill_null(pl.col('at') - pl.col('lt')).alias('tempSE')
])

df = df.with_columns([
    (pl.col('tempSE') + pl.col('txditc') - pl.col('tempPS') + pl.col('txdb')).alias('tempBE')
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
