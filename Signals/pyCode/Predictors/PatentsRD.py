# ABOUTME: Translates PatentsRD.do - calculates patent efficiency scaled by R&D capital 
# ABOUTME: Implements double-sorted portfolio approach linking patent counts to accumulated R&D capital

# Run: python3 Predictors/PatentsRD.py
# Inputs: SignalMasterTable.parquet, m_aCompustat.parquet, PatentDataProcessed.parquet
# Outputs: pyData/Predictors/PatentsRD.csv

import pandas as pd
import numpy as np
from pathlib import Path

# DATA LOAD
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = signal_master[['permno', 'gvkey', 'time_avail_m', 'mve_c', 'sicCRSP', 'exchcd']].copy()

# Convert datetime time_avail_m to YYYYMM integer format
df['time_avail_m'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month
df['year'] = df['time_avail_m'] // 100

# Merge with Compustat
compustat = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
# Convert compustat time_avail_m to YYYYMM format
compustat['time_avail_m'] = compustat['time_avail_m'].dt.year * 100 + compustat['time_avail_m'].dt.month
df = df.merge(compustat[['permno', 'time_avail_m', 'xrd', 'sich', 'datadate', 'ceq']], 
              on=['permno', 'time_avail_m'], how='left')
df = df.dropna(subset=['gvkey'])

# Patent citation dataset - compustat is already lagged, need to lag patent data to match
patents = pd.read_parquet('../pyData/Intermediate/PatentDataProcessed.parquet')
df = df.merge(patents[['gvkey', 'year', 'npat']], on=['gvkey', 'year'], how='left')

# Set up time series structure
df = df.sort_values(['permno', 'time_avail_m'])
df = df.set_index(['permno', 'time_avail_m'])

# Lag patent data by 6 months (l6.npat)
df['temp'] = df.groupby('permno')['npat'].shift(6)
df['temp'] = df['temp'].fillna(0)
df['npat'] = df['temp']
df = df.drop('temp', axis=1)

# Reset index for further processing
df = df.reset_index()

# SIGNAL CONSTRUCTION - form portfolios only in June
df = df[df['time_avail_m'] % 100 == 6]  # month == 6
df = df[df['time_avail_m'] >= 197501]  # Takes into account xrd data standardized after 1975

# Replace missing R&D with 0
df['xrd'] = df['xrd'].fillna(0)

# Components of R&D capital
df = df.sort_values(['permno', 'time_avail_m'])
df = df.set_index(['permno', 'time_avail_m'])

df['comp1'] = 0
df['comp2'] = 0  
df['comp3'] = 0
df['comp4'] = 0
df['comp5'] = 0

# Create lagged R&D components (June-only data: shift by years, not months)
grouped = df.groupby('permno')['xrd']
comp1_lag = grouped.shift(2)  # 2 years back (was shift(24) - WRONG!)
comp2_lag = 0.8 * grouped.shift(3)  # 3 years back (was shift(36) - WRONG!)
comp3_lag = 0.6 * grouped.shift(4)  # 4 years back (was shift(48) - WRONG!)
comp4_lag = 0.4 * grouped.shift(5)  # 5 years back (was shift(60) - WRONG!)
comp5_lag = 0.2 * grouped.shift(6)  # 6 years back (was shift(72) - WRONG!)

df['comp1'] = np.where(comp1_lag.notna(), comp1_lag, 0.0)
df['comp2'] = np.where(comp2_lag.notna(), comp2_lag, 0.0)
df['comp3'] = np.where(comp3_lag.notna(), comp3_lag, 0.0)  
df['comp4'] = np.where(comp4_lag.notna(), comp4_lag, 0.0)
df['comp5'] = np.where(comp5_lag.notna(), comp5_lag, 0.0)

df['RDcap'] = df['comp1'] + df['comp2'] + df['comp3'] + df['comp4'] + df['comp5']
df['tempPatentsRD'] = np.where(df['RDcap'] > 0, df['npat'] / df['RDcap'], np.nan)

df = df.reset_index()

# Filter
df = df.sort_values(['gvkey', 'time_avail_m'])
df = df.groupby('gvkey').apply(lambda x: x.iloc[2:] if len(x) > 2 else x.iloc[0:0]).reset_index(drop=True)
df = df[~((df['sicCRSP'] >= 6000) & (df['sicCRSP'] <= 6999))]
df = df[df['ceq'] >= 0]

# Double independent sort
# Size categories
df = df.sort_values('time_avail_m')
size_cuts = []
for time_month, group in df.groupby('time_avail_m'):
    nyse_group = group[group['exchcd'] == 1]
    if len(nyse_group) > 0:
        median_mve = nyse_group['mve_c'].median()
        group['sizecat'] = np.where(group['mve_c'] <= median_mve, 1, 2)
    else:
        group['sizecat'] = 1
    size_cuts.append(group)
df = pd.concat(size_cuts, ignore_index=True)

# PatentsRD categories (3 groups)
patents_cuts = []
for time_month, group in df.groupby('time_avail_m'):
    # Keep all observations, sort only those with valid tempPatentsRD
    valid_group = group.dropna(subset=['tempPatentsRD'])
    
    if len(valid_group) > 0:
        try:
            # Use rank method to handle duplicate values at quantile boundaries
            valid_group['maincat'] = pd.qcut(valid_group['tempPatentsRD'].rank(method='first'), 
                                           q=3, labels=[1, 2, 3])
            valid_group['maincat'] = valid_group['maincat'].astype(int)
            
            # Merge categories back to all observations
            group = group.merge(valid_group[['permno', 'time_avail_m', 'maincat']], 
                              on=['permno', 'time_avail_m'], how='left')
        except ValueError:
            # Handle case where all values are the same
            group['maincat'] = np.nan
    else:
        # No valid observations this month
        group['maincat'] = np.nan
        
    patents_cuts.append(group)
df = pd.concat(patents_cuts, ignore_index=True)

# Create PatentsRD signal (binary: 1 for small/high, 0 for small/low)
df['PatentsRD'] = np.nan
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 3), 'PatentsRD'] = 1
df.loc[(df['sizecat'] == 1) & (df['maincat'] == 1), 'PatentsRD'] = 0

# Expand back to monthly
def add_months_to_yyyymm(yyyymm, months_to_add):
    """Add months to YYYYMM format, handling year rollover properly"""
    year = yyyymm // 100
    month = yyyymm % 100
    
    # Add months
    total_months = month + months_to_add
    
    # Handle year rollover
    while total_months > 12:
        year += 1
        total_months -= 12
    
    return year * 100 + total_months

monthly_data = []
for _, row in df.iterrows():
    for i in range(12):
        new_row = row.copy()
        new_row['time_avail_m'] = add_months_to_yyyymm(row['time_avail_m'], i)
        monthly_data.append(new_row)

df_monthly = pd.DataFrame(monthly_data)

# SAVE
output = df_monthly[['permno', 'time_avail_m', 'PatentsRD']].dropna()
output = output.astype({'permno': int, 'time_avail_m': int})
output = output.rename(columns={'time_avail_m': 'yyyymm'})
output = output.set_index(['permno', 'yyyymm']).sort_index()
output.to_csv('../pyData/Predictors/PatentsRD.csv')

print("PatentsRD predictor saved successfully")