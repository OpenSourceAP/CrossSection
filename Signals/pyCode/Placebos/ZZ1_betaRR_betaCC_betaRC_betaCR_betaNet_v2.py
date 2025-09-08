#!/usr/bin/env python3
# ABOUTME: Liquidity betas following Acharya and Pedersen (2005) exact Stata replication
# ABOUTME: Fixed implementation matching Stata preserve/restore logic and data filtering

import pandas as pd
import numpy as np
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_placebo
from utils.asrol import asrol
from utils.stata_regress import asreg

print("=== Beta Placebo v3: Fixed Stata Replication ===")

# Step 1: Daily illiquidity computation (exact Stata replication)
print("Step 1: Computing daily illiquidity from dailyCRSP...")
daily_crsp = pd.read_parquet("../pyData/Intermediate/dailyCRSP.parquet")
daily_crsp['time_avail_m'] = daily_crsp['time_d'].dt.to_period('M').dt.start_time
daily_crsp['ill'] = (daily_crsp['ret'].abs() / (daily_crsp['prc'].abs() * daily_crsp['vol'])) * 1_000_000

# Handle inf/nan values in illiquidity before collapsing
daily_crsp['ill'] = daily_crsp['ill'].replace([np.inf, -np.inf], np.nan)

# Monthly collapse (mean) by permno time_avail_m
temp_ill = daily_crsp.groupby(['permno', 'time_avail_m'])['ill'].mean().reset_index()

# Convert to standard numpy dtypes to avoid nullable dtype issues
temp_ill['ill'] = temp_ill['ill'].astype(float)

print(f"Monthly illiquidity collapsed: {len(temp_ill):,} observations")

# Step 2: Load monthly data (exact Stata order)
print("Step 2: Loading monthly CRSP and Market data...")
monthly_crsp = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet")
df = monthly_crsp[['permno', 'time_avail_m', 'ret', 'prc', 'exchcd', 'shrout']].copy()

# Merge illiquidity (keep master match)
df = df.merge(temp_ill, on=['permno', 'time_avail_m'], how='left')

# Merge market data (keep match only)
monthly_market = pd.read_parquet("../pyData/Intermediate/monthlyMarket.parquet")
market = monthly_market[['time_avail_m', 'vwretd', 'usdval']].copy()
df = df.merge(market, on='time_avail_m', how='inner')

print(f"After merges: {len(df):,} observations")

# Step 3: Market cap indexing relative to July 1962 (exact Stata logic)
print("Step 3: Market cap indexing...")
july_1962_data = df[(df['time_avail_m'].dt.year == 1962) & (df['time_avail_m'].dt.month == 7)]
if len(july_1962_data) > 0:
    july_1962_market = july_1962_data['usdval'].mean()
else:
    # Fallback if July 1962 not available
    july_1962_market = df['usdval'].dropna().iloc[0] if len(df) > 0 else 1.0

df['MarketCapitalization'] = df['usdval'] / july_1962_market
print(f"Market cap base (July 1962): {july_1962_market}")

# Set panel structure (sorting equivalent to xtset)
df = df.sort_values(['permno', 'time_avail_m'])

# Individual stock liquidity cost (exact Stata formula)
# Note: Stata uses min(.25 + .3*ill*MarketCapitalization, 30) but this is a typo
# The correct formula from AP2005 is min(ill, (30-.25)/(.3*MarketCapitalization))  
df['c_i'] = np.minimum(0.25 + 0.3 * df['ill'] * df['MarketCapitalization'], 30.0)

# Step 4: Market illiquidity innovation (preserve/restore logic)
print("Step 4: Computing market illiquidity innovation...")

# PRESERVE equivalent - create filtered subset for market calculations
market_subset = df[
    (df['prc'].abs() > 5) & 
    (df['prc'].abs() < 1000) &
    ((df['exchcd'] == 1) | (df['exchcd'] == 2))
].copy()

# Market calculations on filtered subset
market_subset['mktcap'] = market_subset['shrout'] * market_subset['prc'].abs()
market_subset['temp2'] = np.minimum(
    market_subset['ill'], 
    (30.0 - 0.25) / (0.3 * market_subset['MarketCapitalization'])
)

# Convert to standard dtypes to avoid nullable dtype issues
market_subset['temp2'] = market_subset['temp2'].astype(float)
market_subset['mktcap'] = market_subset['mktcap'].astype(float)

# Remove observations with missing illiquidity or infinite values
market_subset = market_subset.dropna(subset=['temp2', 'ill', 'MarketCapitalization'])
market_subset = market_subset[np.isfinite(market_subset['temp2'])]

print(f"Market subset after cleaning: {len(market_subset):,} observations")

# Market aggregations (weighted averages by market cap)
market_agg = market_subset.groupby('time_avail_m').apply(
    lambda x: pd.Series({
        'MarketIlliquidity': (x['temp2'] * x['mktcap']).sum() / x['mktcap'].sum(),
        'rM': (x['vwretd'] * x['mktcap']).sum() / x['mktcap'].sum(),  
        'MarketCapitalization': (x['MarketCapitalization'] * x['mktcap']).sum() / x['mktcap'].sum()
    }),
    include_groups=False
).reset_index()

print(f"Market aggregations: {len(market_agg):,} periods")

# Sort by time for lag operations
market_agg = market_agg.sort_values('time_avail_m')

# Create lagged variables for market model
market_agg['MarketCapitalization_lag1'] = market_agg['MarketCapitalization'].shift(1)
market_agg['temp'] = 0.25 + market_agg['MarketIlliquidity'] * market_agg['MarketCapitalization_lag1']
market_agg['templ1'] = 0.25 + market_agg['MarketIlliquidity'].shift(1) * market_agg['MarketCapitalization_lag1']
market_agg['templ2'] = 0.25 + market_agg['MarketIlliquidity'].shift(2) * market_agg['MarketCapitalization_lag1']

# Market illiquidity innovation regression
print("Running market illiquidity innovation regression...")
market_clean = market_agg.dropna(subset=['temp', 'templ1', 'templ2']).copy()

if len(market_clean) > 60:
    illiq_reg = asreg(
        market_clean,
        y="temp",
        X=["templ1", "templ2"],
        time="time_avail_m",
        window=60,
        min_obs=48,
        add_constant=True
    )
    
    # Merge coefficients back to market data
    market_agg = market_agg.merge(
        illiq_reg[['_b_cons', '_b_templ1', '_b_templ2']],
        left_index=True, right_index=True, how='left'
    )
    
    # Calculate market illiquidity innovation (eps_c_M)
    market_agg['eps_c_M'] = market_agg['temp'] - (
        market_agg['_b_cons'] + 
        market_agg['_b_templ1'] * market_agg['templ1'] + 
        market_agg['_b_templ2'] * market_agg['templ2']
    )
    
    print(f"Market illiquidity innovations computed: {market_agg['eps_c_M'].count()} observations")
else:
    print("Insufficient data for market illiquidity regression")
    market_agg['eps_c_M'] = np.nan
    market_agg[['_b_cons', '_b_templ1', '_b_templ2']] = np.nan

# Market return innovation regression
print("Running market return innovation regression...")
market_agg['rM_lag1'] = market_agg['rM'].shift(1)
market_agg['rM_lag2'] = market_agg['rM'].shift(2)

market_ret_clean = market_agg.dropna(subset=['rM', 'rM_lag1', 'rM_lag2']).copy()

if len(market_ret_clean) > 60:
    ret_reg = asreg(
        market_ret_clean,
        y="rM",
        X=["rM_lag1", "rM_lag2"],
        time="time_avail_m",
        window=60,
        min_obs=48,
        add_constant=True
    )
    
    # Merge return regression coefficients
    market_agg = market_agg.merge(
        ret_reg[['_b_cons', '_b_rM_lag1', '_b_rM_lag2']],
        left_index=True, right_index=True, how='left',
        suffixes=('', '_ret')
    )
    
    # Calculate market return innovation (eps_r_M)
    market_agg['eps_r_M'] = market_agg['rM'] - (
        market_agg['_b_cons_ret'] + 
        market_agg['_b_rM_lag1'] * market_agg['rM_lag1'] + 
        market_agg['_b_rM_lag2'] * market_agg['rM_lag2']
    )
    
    print(f"Market return innovations computed: {market_agg['eps_r_M'].count()} observations")
else:
    print("Insufficient data for market return regression") 
    market_agg['eps_r_M'] = np.nan

# Keep essential columns for merging back
market_results = market_agg[['time_avail_m', 'eps_c_M', 'eps_r_M', '_b_cons', '_b_templ1', '_b_templ2']].copy()

# RESTORE equivalent - merge market results back to main dataset
print("Step 5: Merging market innovations back to main dataset...")
df = df.merge(market_results, on='time_avail_m', how='left')

# Step 6: Stock-level illiquidity innovation 
print("Step 6: Computing stock-level illiquidity innovations...")

# Individual stock illiquidity measure (matching Stata exactly)
df['tempIll'] = np.minimum(
    df['ill'], 
    (30.0 - 0.25) / (0.3 * df['MarketCapitalization'])
)

# Create lagged market cap by stock
df['MarketCapitalization_lag1'] = df.groupby('permno')['MarketCapitalization'].shift(1)

# Stock illiquidity terms using market coefficients  
df['temp_stock'] = 0.25 + df['tempIll'] * df['MarketCapitalization_lag1']
df['templ1_stock'] = 0.25 + df.groupby('permno')['tempIll'].shift(1) * df['MarketCapitalization_lag1']
df['templ2_stock'] = 0.25 + df.groupby('permno')['tempIll'].shift(2) * df['MarketCapitalization_lag1']

# Stock illiquidity innovation using market model coefficients
df['eps_c_i'] = df['temp_stock'] - (
    df['_b_cons'] + 
    df['_b_templ1'] * df['templ1_stock'] + 
    df['_b_templ2'] * df['templ2_stock']
)

# Step 7: Rolling statistics for beta computation
print("Step 7: Computing rolling statistics...")

# Filter to valid observations for rolling calculations
df_work = df.dropna(subset=['ret', 'eps_r_M', 'eps_c_i', 'eps_c_M']).copy()

if len(df_work) > 0:
    print(f"Valid observations for rolling calculations: {len(df_work):,}")
    
    # Rolling means (60-month windows, minimum 24 observations)
    print("Computing rolling means...")
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'ret', 'mean', 'mean60_ret', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'eps_r_M', 'mean', 'mean60_eps_r_M', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'eps_c_i', 'mean', 'mean60_eps_c_i', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'eps_c_M', 'mean', 'mean60_eps_c_M', min_samples=24)
    
    # Variance of difference (eps_r_M - eps_c_M)
    df_work['tempEpsDiff'] = df_work['eps_r_M'] - df_work['eps_c_M']
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'tempEpsDiff', 'std', 'sd60_tempEpsDiff', min_samples=24)
    df_work['sd60_tempEpsDiff'] = df_work['sd60_tempEpsDiff'] ** 2
    
    # Covariance components
    print("Computing covariance components...")
    df_work['tempRR'] = (df_work['ret'] - df_work['mean60_ret']) * (df_work['eps_r_M'] - df_work['mean60_eps_r_M'])
    df_work['tempCC'] = (df_work['eps_c_i'] - df_work['mean60_eps_c_i']) * (df_work['eps_c_M'] - df_work['mean60_eps_c_M'])
    df_work['tempRC'] = (df_work['ret'] - df_work['mean60_ret']) * (df_work['eps_c_M'] - df_work['mean60_eps_c_M'])
    df_work['tempCR'] = (df_work['eps_c_i'] - df_work['mean60_eps_c_i']) * (df_work['eps_r_M'] - df_work['mean60_eps_r_M'])
    
    # Rolling covariances (means of cross-products)
    print("Computing rolling covariances...")
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'tempRR', 'mean', 'mean60_tempRR', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'tempCC', 'mean', 'mean60_tempCC', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'tempRC', 'mean', 'mean60_tempRC', min_samples=24)
    df_work = asrol(df_work, 'permno', 'time_avail_m', '1mo', 60, 'tempCR', 'mean', 'mean60_tempCR', min_samples=24)
    
    # Step 8: Compute final betas
    print("Step 8: Computing final betas...")
    df_work['betaRR'] = df_work['mean60_tempRR'] / df_work['sd60_tempEpsDiff']
    df_work['betaCC'] = df_work['mean60_tempCC'] / df_work['sd60_tempEpsDiff']
    df_work['betaRC'] = df_work['mean60_tempRC'] / df_work['sd60_tempEpsDiff']
    df_work['betaCR'] = df_work['mean60_tempCR'] / df_work['sd60_tempEpsDiff']
    df_work['betaNet'] = df_work['betaRR'] + df_work['betaCC'] - df_work['betaRC'] - df_work['betaCR']
    
    # Apply price filter (exact Stata condition)
    print("Applying price filter...")
    for beta_name in ['betaRR', 'betaCC', 'betaRC', 'betaCR', 'betaNet']:
        df_work.loc[df_work['prc'].abs() > 1000, beta_name] = np.nan
    
    print(f"Final dataset: {len(df_work):,} observations")
    
    # Step 9: Save results (matching standardized format)
    print("Step 9: Saving results...")
    for beta_name in ['betaRR', 'betaCC', 'betaRC', 'betaCR', 'betaNet']:
        # Filter to non-missing observations
        beta_subset = df_work.dropna(subset=[beta_name])[['permno', 'time_avail_m', beta_name]].copy()
        
        if len(beta_subset) > 0:
            # Convert to yyyymm format for consistency
            beta_subset['yyyymm'] = beta_subset['time_avail_m'].dt.year * 100 + beta_subset['time_avail_m'].dt.month
            final_subset = beta_subset[['permno', 'yyyymm', beta_name]].copy()
            
            # Save using pandas to_csv for exact format control
            output_path = f"../pyData/Placebos/{beta_name}.csv"
            final_subset.to_csv(output_path, index=False)
            print(f"✅ Saved {len(final_subset):,} {beta_name} observations to {beta_name}.csv")
        else:
            # Save empty file with correct structure
            empty_df = pd.DataFrame({'permno': [], 'yyyymm': [], beta_name: []})
            output_path = f"../pyData/Placebos/{beta_name}.csv"
            empty_df.to_csv(output_path, index=False)
            print(f"❌ Saved 0 {beta_name} observations to {beta_name}.csv")

else:
    print("❌ No valid data after filtering - saving empty files")
    for beta_name in ['betaRR', 'betaCC', 'betaRC', 'betaCR', 'betaNet']:
        empty_df = pd.DataFrame({'permno': [], 'yyyymm': [], beta_name: []})
        output_path = f"../pyData/Placebos/{beta_name}.csv"
        empty_df.to_csv(output_path, index=False)
        print(f"❌ Saved 0 {beta_name} observations to {beta_name}.csv")

print("✅ Beta Placebo v3 completed")