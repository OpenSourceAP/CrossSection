#%%

# debug
import os
from polars import col

from statsmodels.datasets.danish_data.data import variable_names
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')

# ABOUTME: MS.py - generates Mohanram G-score predictor using 8 financial metrics
# ABOUTME: Python translation of MS.do with industry median comparisons and quarterly aggregation

"""
MS.py

Generates Mohanram G-score predictor from financial statement data:
- MS: Binary score (1-8) based on 8 financial strength indicators
- Sample: Lowest BM quintile only, minimum 3 firms per SIC2D-time
- Indicators: ROA, CF-ROA, cash flow quality, earnings volatility, revenue volatility, R&D intensity, capex intensity, advertising intensity
- All comparisons vs industry medians by (sic2D, time_avail_m)

Usage:
    cd pyCode/
    source .venv/bin/activate  
    python3 Predictors/MS.py

Inputs:
    - ../pyData/Intermediate/m_aCompustat.parquet (accounting data)
    - ../pyData/Intermediate/SignalMasterTable.parquet (mve_c, sicCRSP)
    - ../pyData/Intermediate/m_QCompustat.parquet (quarterly data)

Outputs:
    - ../pyData/Predictors/MS.csv

Requirements:
    - Lowest BM quintile sample selection
    - Industry median normalization for all 8 scores
    - Quarterly data aggregation using 12-month rolling means
    - Complex timing logic with seasonal adjustments
"""

import polars as pl
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.savepredictor import save_predictor
from utils.stata_fastxtile import fastxtile
from utils.stata_replication import stata_ineq_pl
from utils.stata_asreg_asrol import asrol_fast

print("=" * 80)
print("🏗️  MS.py")
print("Generating Mohanram G-score predictor")
print("=" * 80)

# DATA LOAD
print("📊 Loading Compustat and SignalMasterTable data...")

# Load annual Compustat data
print("Loading m_aCompustat.parquet...")
compustat = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet").select([
    "permno", "gvkey", "time_avail_m", "datadate", "at", "ceq", "ni", "oancf", 
    "fopt", "wcapch", "ib", "dp", "xrd", "capx", "xad", "revt"
])
print(f"Loaded m_aCompustat: {len(compustat):,} observations")

# Deduplicate by permno-time_avail_m (following Stata logic)
compustat = compustat.unique(["permno", "time_avail_m"], keep="first")
print(f"After deduplication: {len(compustat):,} observations")

# Load SignalMasterTable for market value and SIC codes
print("Loading SignalMasterTable.parquet...")
smt = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select([
    "permno", "gvkey", "time_avail_m", "mve_c", "sicCRSP"
]).with_columns(
    pl.col('gvkey').cast(pl.Int32)
)
print(f"Loaded SignalMasterTable: {len(smt):,} observations")

# Load quarterly Compustat data
print("Loading m_QCompustat.parquet...")
qcompustat = pl.read_parquet("../pyData/Intermediate/m_QCompustat.parquet").select([
    "gvkey", "time_avail_m", "niq", "atq", "saleq", "oancfy", "capxy", "xrdq", 
    "fyearq", "fqtr", "datafqtr", "datadateq"
])
print(f"Loaded m_QCompustat: {len(qcompustat):,} observations")

# MERGE DATA
print("🔗 Merging datasets...")
df = (compustat
    .join(smt, on=["permno", "gvkey", "time_avail_m"], how="inner")
    .join(qcompustat, on=["gvkey", "time_avail_m"], how="left")
    .sort(["permno", "time_avail_m"])
)
print(f"After merging: {len(df):,} observations")

#%%

# debug

debug_datemax = pl.date(1970, 1, 1) # for speed

# load temp_check*.dta
stata = pd.read_stata('../Human/temp_check0.dta')
stata = pl.from_pandas(stata).with_columns(
    col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(stata.columns, stata.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32, pl.Int16)]
cols = [c for c in cols if c not in ['permno','gvkey']]

stata = stata.select(['permno','gvkey','time_avail_m'] + cols)

stata_long = stata.unpivot(
    index = ['permno','gvkey','time_avail_m'],
    variable_name = 'name',
    value_name = 'stata'
)  

# make df that matches stata_long
df_long = df.with_columns(
    pl.col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(df_long.columns, df_long.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32, pl.Int16)]
cols = [c for c in cols if c not in ['permno','gvkey']]

df_long = df_long.select(['permno','gvkey','time_avail_m'] + cols)

df_long = df_long.unpivot(
    index = ['permno','gvkey','time_avail_m'],
    variable_name = 'name',
    value_name = 'python'
).with_columns(
    pl.col('python').cast(pl.Float64)
)

# merge
both = stata_long.join(
    df_long, on = ['permno','gvkey','time_avail_m','name'], how = 'full', coalesce = True
)

both = (
    both.with_columns(
        pl.when(col('stata').is_null() & col('python').is_null())
        .then(0)
        .when(col('stata').is_not_null() & col('python').is_not_null())
        .then(col('stata') - col('python'))
        .otherwise(pl.lit(float("inf")))
        .alias("diff")
    )
    .sort(col("diff").abs(), descending=True)
)

print('rows where abs(diff) > tiny')
print(
    both.filter(
        col('diff').abs() > 1e-6
    ).sort(
        col('diff').abs(), descending=True
    )
)

#%%
print('why is stata missing niq for permno 32508 gvkey 5337 in 1968?')

# read Data/Intermediate/m_qCompustat.dta
stataraw = pd.read_stata('../Data/Intermediate/m_qCompustat.dta', columns=['gvkey','time_avail_m','niq'])

print('Data/Intermediate/m_qCompustat.dta')
print(
    pl.from_pandas(stataraw).filter(
        col('gvkey') == 5337, col('time_avail_m') >= pl.date(1968, 1, 1), col('time_avail_m') < pl.date(1969, 1, 1) 
    ).sort(col('time_avail_m'))
)

#%%

pythonraw = pl.read_parquet('../pyData/Intermediate/m_QCompustat.parquet', columns=['gvkey','time_avail_m','niq'])
print('pyData/Intermediate/m_QCompustat.parquet')
print(
    pythonraw.filter(
        col('gvkey') == 5337, col('time_avail_m') >= pl.date(1968, 1, 1), col('time_avail_m') < pl.date(1969, 1, 1) 
    ).sort(col('time_avail_m'))
)

print('the difference seems ok. just 96 rows of expanded data (more like 20 obs )')
print('looks like the python data is more updated.')



#%%

# SAMPLE SELECTION
print("🎯 Applying sample selection criteria...")

# Limit sample to firms in the lowest BM quintile (p 8 of original paper)
df = df.with_columns([
    (pl.col("ceq") / pl.col("mve_c")).log().alias("BM")
]).filter(
    pl.col("ceq") > 0  # Positive book equity
)

# Calculate BM quintiles using enhanced fastxtile (pandas-based for accuracy)
# Convert to pandas temporarily for quintile calculation
print("Calculating BM quintiles with enhanced fastxtile...")
df_pd = df.to_pandas()

# Clean infinite BM values explicitly (following successful PS pattern)
df_pd['BM'] = df_pd['BM'].replace([np.inf, -np.inf], np.nan)

# Use enhanced fastxtile for quintile assignment
df_pd['BM_quintile'] = fastxtile(df_pd, 'BM', by='time_avail_m', n=5)

# Convert back to polars and filter for lowest quintile
df = pl.from_pandas(df_pd).filter(
    pl.col("BM_quintile") == 1  # Keep only lowest BM quintile (growth firms)
).drop(
    'BM_quintile'
)



print(f"After BM quintile filter: {len(df):,} observations")

# Keep if at least 3 firms in sic2D-time_avail_m combination
df = df.with_columns(
    pl.col("sicCRSP").cast(pl.Utf8).str.slice(0, 2).alias("sic2D")
).with_columns(
    pl.len().over(["sic2D", "time_avail_m"]).alias("sic2D_count")
).filter(
    pl.col("sic2D_count") >= 3
)

print(f"After SIC2D minimum filter: {len(df):,} observations")

# PREP VARIABLES
print("🧮 Preparing financial variables...")

# Handle missing values for optional items (following Stata logic)
df = df.with_columns([
    pl.col("xad").fill_null(0.0),
    pl.col("xrdq").fill_null(0.0)
])

# Create quarterly capx and oancf from annual data based on fiscal quarter
# This follows the "locating oancfq" logic from WRDS
df = df.with_columns([
    # capxq: If Q1, use capxy directly. If Q>1, use capxy - lag3(capxy)
    pl.when(pl.col("fqtr") == 1)
    .then(pl.col("capxy"))
    .when((pl.col("fqtr") > 1) & pl.col("fqtr").is_not_null())
    .then(pl.col("capxy") - pl.col("capxy").shift(3).over("permno"))
    .otherwise(pl.lit(None))
    .alias("capxq"),
    
    # oancfq: Same logic as capxq
    pl.when(pl.col("fqtr") == 1)
    .then(pl.col("oancfy"))
    .when((pl.col("fqtr") > 1) & pl.col("fqtr").is_not_null())
    .then(pl.col("oancfy") - pl.col("oancfy").shift(3).over("permno"))
    .otherwise(pl.lit(None))
    .alias("oancfq")
])

#%%

# debug 
print('debug temp_check1.dta')

debug_datemax = pl.date(1976, 1, 1) # for speed

# load temp_check1.dta
stata = pd.read_stata('../Human/temp_check1.dta')
stata = pl.from_pandas(stata).with_columns(
    col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(stata.columns, stata.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c != "permno"]

stata = stata.select(['permno','time_avail_m'] + cols)

stata_long = stata.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'stata'
)  

# make df that matches stata_long
df_long = df.with_columns(
    pl.col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(df_long.columns, df_long.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c != "permno"]

df_long = df_long.select(['permno','time_avail_m'] + cols)

df_long = df_long.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'python'
).with_columns(
    pl.col('python').cast(pl.Float64)
)

both = stata_long.join(
    df_long, on = ['permno','time_avail_m','name'], how = 'full', coalesce = True
).filter(
    col('time_avail_m') < pl.date(1990, 1, 1)
)

both = (
    both.with_columns(
        pl.when(col('stata').is_null() & col('python').is_null())
        .then(0)
        .when(col('stata').is_not_null() & col('python').is_not_null())
        .then(col('stata') - col('python'))
        .otherwise(pl.lit(float("inf")))
        .alias("diff")
    )
    .sort(col("diff").abs(), descending=True)
)

print('rows where abs(diff) > tiny')
print(
    both.filter(
        col('diff').abs() > 1e-6
    ).sort(
        col('diff').abs(), descending=True
    )
)

print('differences are tiny, seems like tiny data updates')

#%%

# debug: create MWE

df.write_parquet('../Human/mwe_input.parquet')


#%%

print("📈 Computing quarterly aggregations...")

# Aggregate quarterly data using time-based rolling to match Stata's asrol behavior
# Stata's asrol window(time_avail_m 12) min(12) requires exactly 12 observations 
# spanning 12 calendar months, not just 12 consecutive data points

print("  Calculating time-based rolling means (matching Stata's asrol)...")

# Use fast asrol_fast function to compute 12-month rolling means
df = asrol_fast(df, 'permno', 'time_avail_m', 'niq', 12, "monthly", 'mean', 'niqsum', 12)


#%%

# debug temp_check2.dta
print('debug temp_check2.dta')

debug_datemax = pl.date(1976, 1, 1) # for speed

# load temp_check2.dta
stata = pd.read_stata('../Human/temp_check2.dta')
stata = pl.from_pandas(stata).with_columns(
    col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(stata.columns, stata.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c != "permno"]

stata = stata.select(['permno','time_avail_m'] + cols)

stata_long = stata.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'stata'
)  


# make df that matches stata_long
df_long = df.with_columns(
    pl.col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(df_long.columns, df_long.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c != "permno"]

df_long = df_long.select(['permno','time_avail_m'] + cols)

df_long = df_long.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'python'
).with_columns(
    pl.col('python').cast(pl.Float64)
)

both = stata_long.join(
    df_long, on = ['permno','time_avail_m','name'], how = 'full', coalesce = True
).filter(
    col('time_avail_m') < pl.date(1990, 1, 1)
)

both = (
    both.with_columns(
        pl.when(col('stata').is_null() & col('python').is_null())
        .then(0)
        .when(col('stata').is_not_null() & col('python').is_not_null())
        .then(col('stata') - col('python'))
        .otherwise(pl.lit(float("inf")))
        .alias("diff")
    )
    .sort(col("diff").abs(), descending=True)
)

print('rows where abs(diff) > tiny')
print(
    both.filter(
        col('diff').abs() > 1e-6
    ).sort(
        col('diff').abs(), descending=True
    )
)




#%%


df = asrol_fast(df, 'permno', 'time_avail_m', 'xrdq', 12, "monthly", 'mean', 'xrdqsum', 12)  
df = asrol_fast(df, 'permno', 'time_avail_m', 'oancfq', 12, "monthly", 'mean', 'oancfqsum', 12)
df = asrol_fast(df, 'permno', 'time_avail_m', 'capxq', 12, "monthly", 'mean', 'capxqsum', 12)



#%%

# debug temp_check3.dta
print('debug temp_check3.dta')

debug_datemax = pl.date(1976, 1, 1) # for speed

# load temp_check3.dta
stata = pd.read_stata('../Human/temp_check3.dta')
stata = pl.from_pandas(stata).with_columns(
    col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(stata.columns, stata.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c not in ['permno','gvkey','time_avail_m']]

stata = stata.select(['permno','gvkey','time_avail_m'] + cols)

stata_long = stata.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'stata'
)  

# make df that matches stata_long
df_long = df.with_columns(
    pl.col('time_avail_m').cast(pl.Date)
).filter(
    col('time_avail_m') < debug_datemax
)
cols = [c for c, dtype in zip(df_long.columns, df_long.dtypes) if dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
cols = [c for c in cols if c not in ['permno','gvkey','time_avail_m']]

df_long = df_long.select(['permno','gvkey','time_avail_m'] + cols)

df_long = df_long.unpivot(
    index = ['permno','time_avail_m'],
    variable_name = 'name',
    value_name = 'python'
).with_columns(
    pl.col('python').cast(pl.Float64)
)

both = stata_long.join(
    df_long, on = ['permno','time_avail_m','name'], how = 'full', coalesce = True
).filter(
    col('time_avail_m') < pl.date(1990, 1, 1)
)

both = (
    both.with_columns(
        pl.when(col('stata').is_null() & col('python').is_null())
        .then(0)
        .when(col('stata').is_not_null() & col('python').is_not_null())
        .then(col('stata') - col('python'))
        .otherwise(pl.lit(float("inf")))
        .alias("diff")
    )
    .sort(col("diff").abs(), descending=True)
)

print('rows where abs(diff) > tiny')
print(
    both.filter(
        col('diff').abs() > 1e-6
    ).sort(
        col('diff').abs(), descending=True
    )
)

print('very few differences')

#%%

print('double checking the asrol outputs')

print(
    both.filter(
        col('name').is_in(['niqsum','xrdqsum','oancfqsum','capxqsum'])
    ).sort(
        col('diff').abs(), descending=True
    ).filter(
        col('diff').abs() > 1e-6
    )
)

print('looks good')

#%%

# Annualize the quarterly means by multiplying by 4
df = df.with_columns([
    (pl.col("niqsum") * 4).alias("niqsum"),
    (pl.col("xrdqsum") * 4).alias("xrdqsum"), 
    (pl.col("oancfqsum") * 4).alias("oancfqsum"),
    (pl.col("capxqsum") * 4).alias("capxqsum")
])

# Handle special case for early years (endnote 3): Use fopt - wcapch for oancfqsum before 1988
df = df.with_columns(
    pl.when(pl.col("datadate").dt.year() <= 1988)
    .then(pl.col("fopt") - pl.col("wcapch"))
    .otherwise(pl.col("oancfqsum"))
    .alias("oancfqsum")
)

#%%

# SIGNAL CONSTRUCTION
print("💰 Constructing the 8 Mohanram G-score components...")

# ================================================================
# PROFITABILITY AND CASH FLOW SIGNALS (following MS.do lines 54-68)
# ================================================================
print("  Phase 1: Profitability and cash flow signals...")

# Calculate atdenom for profitability ratios (MS.do line 56)
df = df.with_columns(
    ((pl.col("atq") + pl.col("atq").shift(3).over("permno")) / 2).alias("atdenom")
)

# Calculate profitability ratios (MS.do lines 58-59)
df = df.with_columns([
    (pl.col("niqsum") / pl.col("atdenom")).alias("roa"),
    (pl.col("oancfqsum") / pl.col("atdenom")).alias("cfroa")
])

# Calculate industry medians for profitability ratios (MS.do lines 60-62)
for col in ["roa", "cfroa"]:
    df = df.with_columns(
        pl.col(col).median().over(["sic2D", "time_avail_m"]).alias(f"md_{col}")
    )

# Create profitability binary indicators m1, m2, m3 (MS.do lines 63-68)
df = df.with_columns([
    # M1: ROA > industry median
    pl.when(stata_ineq_pl(pl.col("roa"), ">", pl.col("md_roa"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m1"),
    # M2: CF-ROA > industry median  
    pl.when(stata_ineq_pl(pl.col("cfroa"), ">", pl.col("md_cfroa"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m2"),
    # M3: Operating cash flow > net income
    pl.when(stata_ineq_pl(pl.col("oancfqsum"), ">", pl.col("niqsum"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m3")
])

# ================================================================  
# "NAIVE EXTRAPOLATION" SIGNALS (following MS.do lines 70-83)
# ================================================================
print("  Phase 2: Naive extrapolation (volatility) signals...")

# Calculate quarterly ratios (MS.do lines 72-73)
df = df.with_columns([
    (pl.col("niq") / pl.col("atq")).alias("roaq"),
    (pl.col("saleq") / pl.col("saleq").shift(3).over("permno")).alias("sg")
])

# Calculate 48-month rolling volatility (MS.do lines 74-75)
df = asrol_fast(df, 'permno', 'time_avail_m', 'roaq', 48, "monthly", 'std', 'niVol', 18)
df = asrol_fast(df, 'permno', 'time_avail_m', 'sg', 48, "monthly", 'std', 'revVol', 18)

# Calculate industry medians for volatility measures (MS.do lines 77-79)
for col in ["niVol", "revVol"]:
    df = df.with_columns(
        pl.col(col).median().over(["sic2D", "time_avail_m"]).alias(f"md_{col}")
    )

# Create volatility binary indicators m4, m5 (MS.do lines 80-83)
df = df.with_columns([
    # M4: Earnings volatility < industry median
    pl.when(stata_ineq_pl(pl.col("niVol"), "<", pl.col("md_niVol"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m4"),
    # M5: Revenue volatility < industry median
    pl.when(stata_ineq_pl(pl.col("revVol"), "<", pl.col("md_revVol"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m5")
])

# ================================================================
# "CONSERVATISM" SIGNALS (following MS.do lines 85-99) 
# ================================================================
print("  Phase 3: Conservatism (investment intensity) signals...")

# Calculate atdenom2 for intensity ratios (MS.do line 87)
df = df.with_columns(
    pl.col("atq").shift(3).over("permno").alias("atdenom2")
)

# Calculate investment intensity ratios (MS.do lines 88-90)
df = df.with_columns([
    (pl.col("xrdqsum") / pl.col("atdenom2")).alias("xrdint"),
    (pl.col("capxqsum") / pl.col("atdenom2")).alias("capxint"),
    (pl.col("xad") / pl.col("atdenom2")).alias("xadint")
])

# Calculate industry medians for intensity measures (MS.do lines 91-93)
for col in ["xrdint", "capxint", "xadint"]:
    df = df.with_columns(
        pl.col(col).median().over(["sic2D", "time_avail_m"]).alias(f"md_{col}")
    )

# Create intensity binary indicators m6, m7, m8 (MS.do lines 94-99)
df = df.with_columns([
    # M6: R&D intensity > industry median
    pl.when(stata_ineq_pl(pl.col("xrdint"), ">", pl.col("md_xrdint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m6"),
    # M7: Capex intensity > industry median
    pl.when(stata_ineq_pl(pl.col("capxint"), ">", pl.col("md_capxint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m7"),
    # M8: Advertising intensity > industry median  
    pl.when(stata_ineq_pl(pl.col("xadint"), ">", pl.col("md_xadint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m8")
])

# ================================================================
# FINAL MOHANRAM G-SCORE (following MS.do lines 101-113)
# ================================================================
print("  Phase 4: Final G-score calculation...")

# Sum the 8 components to get tempMS (MS.do line 101)
df = df.with_columns(
    (pl.col("m1") + pl.col("m2") + pl.col("m3") + pl.col("m4") + 
     pl.col("m5") + pl.col("m6") + pl.col("m7") + pl.col("m8")).alias("tempMS")
)

print("📅 Applying timing logic...")

# Fix tempMS at most recent data release for entire year
# Complex timing logic: only keep if month matches (datadate + 6 months) mod 12
df = df.with_columns([
    # Calculate expected release month
    ((pl.col("datadate").dt.month() + 6) % 12).alias("expected_month"),
    # Current month
    pl.col("time_avail_m").dt.month().alias("current_month")
]).with_columns([
    # Set tempMS to null if not in expected release month
    pl.when(pl.col("current_month") != pl.col("expected_month"))
    .then(pl.lit(None))
    .otherwise(pl.col("tempMS"))
    .alias("tempMS")
])

# Forward fill tempMS within permno groups
df = df.with_columns(
    pl.col("tempMS").forward_fill().over("permno").alias("tempMS")
)

# Create final MS score - fix missing upper bound condition
df_final = df.with_columns([
    pl.when((pl.col("tempMS") >= 6) & (pl.col("tempMS") <= 8))
    .then(pl.lit(6))
    .when(pl.col("tempMS") <= 1) 
    .then(pl.lit(1))
    .otherwise(pl.col("tempMS"))
    .alias("MS")
])


df_final = df_final.select(["permno", "time_avail_m", "MS"]).filter(
    pl.col("MS").is_not_null()
)

print(f"Generated MS values: {len(df_final):,} observations")
print(f"MS summary stats:")
print(f"  Mean: {df_final['MS'].mean():.4f}")
print(f"  Std: {df_final['MS'].std():.4f}")
print(f"  Min: {df_final['MS'].min()}")  
print(f"  Max: {df_final['MS'].max()}")

# SAVE
print("💾 Saving MS predictor...")
save_predictor(df_final, "MS")
print("✅ MS.csv saved successfully")