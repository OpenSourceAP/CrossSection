# %%
# debug
import os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

# # goal is to fix:
# **Largest Differences**:
# ```
#    permno  yyyymm  python  stata  diff
# 0   49016  199201       1      6    -5
# 1   49016  199202       1      6    -5
# 2   49016  199204       1      6    -5
# 3   76023  199906       6      1     5
# 4   76023  199907       6      1     5
# 5   76023  199908       6      1     5
# 6   76023  199909       6      1     5
# 7   76023  199910       6      1     5
# 8   76023  199911       6      1     5
# 9   76023  199912       6      1     5
# ```

pl.Config.set_tbl_cols(1000)
pl.Config.set_tbl_rows(24)

from polars import col as cc

debug_datemax = pl.date(2000, 1, 1) # for speed

import polars as pl

def diff_with_nulls(a: str | pl.Expr, b: str | pl.Expr, *, inf: float = float("inf")) -> pl.Expr:
    """
    Compute a - b with custom null rules:
      • +inf if exactly one of (a, b) is null
      • 0.0  if both are null
      • a - b otherwise
    Returns a Polars expression.
    """
    a_expr = pl.col(a) if isinstance(a, str) else a
    b_expr = pl.col(b) if isinstance(b, str) else b

    a_null = a_expr.is_null()
    b_null = b_expr.is_null()

    return (
        pl.when(a_null & b_null).then(pl.lit(0.0))
        .when(a_null | b_null).then(pl.lit(inf))
        .otherwise(a_expr - b_expr)
    )


# %%

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
    "permno", "time_avail_m", "mve_c", "sicCRSP"
])
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
    .join(smt, on=["permno", "time_avail_m"], how="inner")
    .join(qcompustat, on=["gvkey", "time_avail_m"], how="left")
    .sort(["permno", "time_avail_m"])
)
print(f"After merging: {len(df):,} observations")

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
df_pd['BM_clean'] = df_pd['BM'].replace([np.inf, -np.inf], np.nan)

# Use enhanced fastxtile for quintile assignment
df_pd['BM_quintile'] = fastxtile(df_pd, 'BM_clean', by='time_avail_m', n=5)

# Convert back to polars and filter for lowest quintile
df = pl.from_pandas(df_pd).filter(
    pl.col("BM_quintile") == 1  # Keep only lowest BM quintile (growth firms)
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

print("📈 Computing quarterly aggregations...")

# Aggregate quarterly data using time-based rolling to match Stata's asrol behavior
# Stata's asrol window(time_avail_m 12) min(12) requires exactly 12 observations
# spanning 12 calendar months, not just 12 consecutive data points


# === old code ===

# # Convert to pandas for time-based rolling calculations
# df_pd = df.to_pandas()
# df_pd = df_pd.set_index('time_avail_m').sort_index()

# # Use pandas' built-in rolling with time window to match Stata's asrol behavior
# # This is much faster than the custom loop approach
# print("  Calculating time-based rolling means (matching Stata's asrol)...")

# # Group by permno for rolling calculations
# def apply_stata_rolling(group):
#     """Apply Stata-like rolling aggregation to a permno group"""
#     # Ensure data is sorted by time
#     group = group.sort_index()
    
#     # Use exact 12-month window to match Stata's asrol window(time_avail_m 12) min(12)
#     # 365D can be slightly off due to leap years, use 366D to be safe
#     group['niqsum'] = group['niq'].rolling('366D', min_periods=12).mean() * 4
#     group['xrdqsum'] = group['xrdq'].rolling('366D', min_periods=12).mean() * 4
#     group['oancfqsum'] = group['oancfq'].rolling('366D', min_periods=12).mean() * 4
#     group['capxqsum'] = group['capxq'].rolling('366D', min_periods=12).mean() * 4
    
#     return group

# # Apply rolling calculations by permno
# df_pd = df_pd.groupby('permno', group_keys=False).apply(apply_stata_rolling)

# === new code ===

def asrol_polars_rolling(
    df: pl.DataFrame, 
    group_col: str, 
    date_col: str, 
    value_col: str, 
    stat: str = 'mean',
    window: str = '12mo', 
    min_obs: int = 1,
    ) -> pl.DataFrame:
    """
    hand built polars asrol that 
      - constructs windows based a date duration
      - replaces with na if there are not enough observations in the window
    input: polars dataframe
    output: polars dataframe with a new column
    """

    # grab the stat function
    stat_dict = {'mean': pl.mean, 'std': pl.std, 'min': pl.min, 'max': pl.max}
    stat_fun = stat_dict[stat]

    df_addition =  df.sort(
        pl.col([group_col, date_col])
        ).with_columns(
            pl.col([group_col, date_col]).set_sorted()
        ).rolling(index_column=date_col, period=window, group_by=group_col).agg(
            [
                pl.last(value_col).alias(f'{value_col}_last'),
                stat_fun(value_col).alias(f'{value_col}_{stat}'),
                pl.count(value_col).alias(f'{value_col}_obs')
            ]
        ).with_columns(
            pl.when(cc(f'{value_col}_obs') >= min_obs).then(cc(f'{value_col}_{stat}'))
            .otherwise(pl.lit(None))
            .alias(f'{value_col}_{stat}')
        )

    return df.join(
        df_addition.select([group_col, date_col, f'{value_col}_{stat}']),
        on=[group_col, date_col],
        how='left',
        coalesce=True
    )

    

dateref = pl.date(1999,6,1)
permnolist = [76023, 38295]


df = asrol_polars_rolling(df, 'permno', 'time_avail_m', 'niq', 'mean', '12mo', 12)\
    .rename({'niq_mean':'niqsum'})

#%% ddd

# temp_check2.dta passed!

#%%


df = asrol_polars_rolling(df, 'permno', 'time_avail_m', 'xrdq', 'mean', '12mo', 12)\
    .rename({'xrdq_mean':'xrdqsum'})
df = asrol_polars_rolling(df, 'permno', 'time_avail_m', 'oancfq', 'mean', '12mo', 12)\
    .rename({'oancfq_mean':'oancfqsum'})
df = asrol_polars_rolling(df, 'permno', 'time_avail_m', 'capxq', 'mean', '12mo', 12)\
    .rename({'capxq_mean':'capxqsum'})

#%% ddd

# temp_check3.dta passed!

#%% ddd

# temp_check3.dta placeholder

print('compare with stata')

col_to_check = ['permno','gvkey','time_avail_m','oancfqsum']
id_cols = ['permno','gvkey','time_avail_m']

stata = pd.read_stata('../Human/temp_check3.dta')
stata = pl.from_pandas(stata).with_columns(
    cc('time_avail_m').cast(pl.Date)
).select(col_to_check)

stata_long = stata.unpivot(
    index = id_cols,
    variable_name = 'name',
    value_name = 'stata'
)

# make df that matches stata_long
df_long = df.with_columns(
    pl.col('time_avail_m').cast(pl.Date)
).select(col_to_check).unpivot(
    index = id_cols,
    variable_name = 'name',
    value_name = 'python'
)

# merge
both = stata_long.join(
    df_long, on = ['permno','gvkey','time_avail_m','name'], how = 'full', coalesce = True
).with_columns(
    pl.when(cc('stata').is_null() & cc('python').is_null()).then(0)
    .when(cc('stata').is_not_null() & cc('python').is_not_null()).then(cc('stata') - cc('python'))
    .otherwise(pl.lit(float('inf')))
    .alias('diff')
).sort(
    cc('diff').abs(), descending=True
)

print(f'rows where diff is inf, out of {len(both)}')
print(
    both.filter(
        cc('diff').is_infinite()
    ).sort(
        cc('diff').abs(), descending=True
    )
)

#%% ddd

print('focus on selected obs')

permno = 10011
dateref = pl.date(1994,4,1)

print(
    df.filter(
        cc('permno') == permno, cc('time_avail_m') <= dateref, cc('time_avail_m') >= dateref - pl.duration(days=365*1)
    ).sort('time_avail_m').select(
        ['permno','gvkey','time_avail_m','oancfq','oancfqsum']
    )
)
#%%


# Handle special case for early years (endnote 3): Use fopt - wcapch for oancfqsum before 1988
df = df.with_columns(
    pl.when(pl.col("datadate").dt.year() <= 1988)
    .then(pl.col("fopt") - pl.col("wcapch"))
    .otherwise(pl.col("oancfqsum"))
    .alias("oancfqsum")
)

print("💰 Constructing the 8 Mohanram G-score components...")

# Calculate denominators for profitability ratios
df = df.with_columns([
    # Average total assets for current and lagged quarters
    ((pl.col("atq") + pl.col("atq").shift(3).over("permno")) / 2).alias("atdenom"),
    # Lagged quarterly assets for intensity ratios  
    pl.col("atq").shift(3).over("permno").alias("atdenom2")
])

# Calculate the 8 component ratios step by step to avoid window expression issues
print("  Computing profitability ratios...")
df = df.with_columns([
    # Profitability measures
    (pl.col("niqsum") / pl.col("atdenom")).alias("roa"),
    (pl.col("oancfqsum") / pl.col("atdenom")).alias("cfroa"),
    
    # Investment intensity measures
    (pl.col("xrdqsum") / pl.col("atdenom2")).alias("xrdint"),
    (pl.col("capxqsum") / pl.col("atdenom2")).alias("capxint"),
    (pl.col("xad") / pl.col("atdenom2")).alias("xadint")
])

print("  Computing volatility measures...")
# Calculate quarterly ratios first, then time-based rolling volatility
df = df.with_columns([
    (pl.col("niq") / pl.col("atq")).alias("roaq"),
    (pl.col("saleq") / pl.col("saleq").shift(3).over("permno")).alias("sg")
])

# Convert to pandas for time-based volatility calculations (48-month rolling)
print("    Calculating time-based 48-month rolling volatility...")
df_pd_vol = df.to_pandas().set_index('time_avail_m').sort_index()

def apply_stata_volatility_rolling(group):
    """Apply Stata-like 48-month rolling volatility calculations"""
    group = group.sort_index()
    
    # Use 48-month (4 years) time window with min_periods=18 to match Stata's asrol
    # 48 months ≈ 1460 days, use 1470D to be safe with leap years
    group['niVol'] = group['roaq'].rolling('1470D', min_periods=18).std()
    group['revVol'] = group['sg'].rolling('1470D', min_periods=18).std()
    
    return group

# Apply volatility rolling calculations by permno
df_pd_vol = df_pd_vol.groupby('permno', group_keys=False).apply(apply_stata_volatility_rolling)

# Convert back to polars
df = pl.from_pandas(df_pd_vol.reset_index())

print("🏭 Computing industry medians...")

# Calculate industry medians for all ratios by sic2D-time_avail_m
median_cols = ["roa", "cfroa", "niVol", "revVol", "xrdint", "capxint", "xadint"]
for col in median_cols:
    df = df.with_columns(
        pl.col(col).median().over(["sic2D", "time_avail_m"]).alias(f"md_{col}")
    )


print("🎯 Creating binary indicators...")

# Create the 8 binary Mohanram G-score components
# Following Stata logic: gen m_x = 0, replace m_x = 1 if condition
# Using Stata-compatible inequality operators that treat missing as positive infinity
df = df.with_columns([
    # M1: ROA > industry median (missing ROA treated as infinity)
    pl.when(stata_ineq_pl(pl.col("roa"), ">", pl.col("md_roa"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m1"),
    # M2: CF-ROA > industry median (missing CFROA treated as infinity)
    pl.when(stata_ineq_pl(pl.col("cfroa"), ">", pl.col("md_cfroa"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m2"),
    # M3: Operating cash flow > net income (missing treated as infinity)
    pl.when(stata_ineq_pl(pl.col("oancfqsum"), ">", pl.col("niqsum"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m3"),
    # M4: Earnings volatility < industry median (missing volatility treated as infinity)
    pl.when(stata_ineq_pl(pl.col("niVol"), "<", pl.col("md_niVol"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m4"),
    # M5: Revenue volatility < industry median (missing volatility treated as infinity)
    pl.when(stata_ineq_pl(pl.col("revVol"), "<", pl.col("md_revVol"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m5"),
    # M6: R&D intensity > industry median (missing R&D treated as infinity)
    pl.when(stata_ineq_pl(pl.col("xrdint"), ">", pl.col("md_xrdint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m6"),
    # M7: Capex intensity > industry median (missing capex treated as infinity)
    pl.when(stata_ineq_pl(pl.col("capxint"), ">", pl.col("md_capxint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m7"),
    # M8: Advertising intensity > industry median (missing advertising treated as infinity)
    pl.when(stata_ineq_pl(pl.col("xadint"), ">", pl.col("md_xadint"))).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m8")
])


# Sum the 8 components to get tempMS
df = df.with_columns(
    (pl.col("m1") + pl.col("m2") + pl.col("m3") + pl.col("m4") + 
     pl.col("m5") + pl.col("m6") + pl.col("m7") + pl.col("m8")).alias("tempMS")
)

# %%

# ================================================================
# DEBUG CHECKPOINT 7
# ================================================================

print('debug temp_check7.dta')

# load temp_check7.dta
stata = pd.read_stata('../Human/temp_check7.dta')
stata = pl.from_pandas(stata).with_columns(
    cc('time_avail_m').cast(pl.Date)
)

# %%

print('check on permno 76023 in 1999-06')

print('python')
print(
df.filter(
        (pl.col('permno') == 76023), 
        pl.col('time_avail_m') == pl.date(1999,6,1)
    ).sort('time_avail_m').select(
        ['permno','time_avail_m','m1','m2','m3','m4','m5','m6','m7','m8','tempMS']
    )
)
print('stata')
print(
stata.filter(
    cc('permno') == 76023,
    cc('time_avail_m') == pl.date(1999,6,1)
).sort('time_avail_m').select(
    ['permno','time_avail_m','m1','m2','m3','m4','m5','m6','m7','m8','tempMS']
)
)

print('python m1 through m3 = 1, but stata has all zeros')

# %%

print('m1 to m3 are about roa, cfroa, and oancfqsum, where oancfqsum comes from oancfq')

print('python')
print(
    df.filter(
        cc('permno') == 76023, cc('time_avail_m') <= pl.date(1999,6,1), cc('time_avail_m') >= pl.date(1999,1,1)
    ).sort('time_avail_m').select(
        ['permno','gvkey','time_avail_m','roa','cfroa','oancfqsum','oancfq']
    )
)

print('stata')
print(
    stata.filter(
        cc('permno') == 76023, cc('time_avail_m') <= pl.date(1999,6,1), cc('time_avail_m') >= pl.date(1999,1,1)
    ).sort('time_avail_m').select(
        ['permno','gvkey','time_avail_m','roa','cfroa','oancfqsum','oancfq']
    )
)

print('roa and cfroa are missing in stata but not in python')
print('roa and cfroa come from niqsum and oancfqsum, whcich in turn come from asrol on niq and oancfq')

# %%

print('checking on niq and oancfq for permno == 76023')

print('python')
print(
    df.filter(
        cc('permno') == 76023, cc('time_avail_m') <= pl.date(1999,6,1), cc('time_avail_m') >= pl.date(1998,6,1)
    ).sort('time_avail_m').select(
        ['permno','gvkey','time_avail_m','niq','oancfq']
    )
)

print('stata')
print(
    stata.filter(
        cc('permno') == 76023, cc('time_avail_m') <= pl.date(1999,6,1), cc('time_avail_m') >= pl.date(1998,6,1)
    ).sort('time_avail_m').select(
        ['permno','gvkey','time_avail_m','niq','oancfq']
    )
)

print('XXX: for this particular difference, we have a solution')
print('the problem here is that the stata asrol requires all 12 months to be present ')
print('when bys permno: asrol niq, gen(niqsum) stat(mean) window(time_avail_m 12) min(12)')
print('but the python code lacks this requirement.')


# %%

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
