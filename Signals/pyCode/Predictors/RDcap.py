# ABOUTME: Translates RDcap.do to create R&D capital to assets predictor for small firms
# ABOUTME: Run from pyCode/ directory: python3 Predictors/RDcap.py

# Run from pyCode/ directory
# Inputs: m_aCompustat.parquet, SignalMasterTable.parquet
# Output: ../pyData/Predictors/RDcap.csv

import pandas as pd
import numpy as np

# DATA LOAD
df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
df = df[['permno', 'time_avail_m', 'at', 'xrd']].copy()

# Drop duplicates
df = df.drop_duplicates(subset=['permno', 'time_avail_m'])

# Merge with SignalMasterTable (keep master match like Stata)
smt = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df.merge(smt[['permno', 'time_avail_m', 'mve_c']], on=['permno', 'time_avail_m'], how='left')

# Sort for lag operations
df = df.sort_values(['permno', 'time_avail_m'])

# SIGNAL CONSTRUCTION
# Extract year for filtering
df['year'] = df['time_avail_m'].dt.year

# Handle missing xrd values
df['tempXRD'] = df['xrd'].fillna(0)

# Calculate calendar-based lags of tempXRD (matching Stata's l12., l24., etc.)
df_tempxrd = df[['permno', 'time_avail_m', 'tempXRD']].copy()

# Calculate lag times
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
df['time_lag24'] = df['time_avail_m'] - pd.DateOffset(months=24)
df['time_lag36'] = df['time_avail_m'] - pd.DateOffset(months=36)
df['time_lag48'] = df['time_avail_m'] - pd.DateOffset(months=48)

# Merge to get lagged values
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag12', 'tempXRD': 'tempXRD_lag12'}),
              on=['permno', 'time_lag12'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag24', 'tempXRD': 'tempXRD_lag24'}),
              on=['permno', 'time_lag24'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag36', 'tempXRD': 'tempXRD_lag36'}),
              on=['permno', 'time_lag36'], how='left')
df = df.merge(df_tempxrd.rename(columns={'time_avail_m': 'time_lag48', 'tempXRD': 'tempXRD_lag48'}),
              on=['permno', 'time_lag48'], how='left')

# Clean up temporary columns
df = df.drop(['time_lag12', 'time_lag24', 'time_lag36', 'time_lag48'], axis=1)

# Fill missing lagged values with 0 (like Stata arithmetic)
df['tempXRD_lag12'] = df['tempXRD_lag12'].fillna(0)
df['tempXRD_lag24'] = df['tempXRD_lag24'].fillna(0)
df['tempXRD_lag36'] = df['tempXRD_lag36'].fillna(0)
df['tempXRD_lag48'] = df['tempXRD_lag48'].fillna(0)

# Calculate R&D capital (weighted sum of current and lagged R&D)
df['RDcap'] = (df['tempXRD'] + 
               0.8 * df['tempXRD_lag12'] + 
               0.6 * df['tempXRD_lag24'] + 
               0.4 * df['tempXRD_lag36'] + 
               0.2 * df['tempXRD_lag48']) / df['at']

# Exclude observations before 1980
df.loc[df['year'] < 1980, 'RDcap'] = np.nan

# Create size tertiles using fastxtile-compatible method (position-based with ties to lower)
def fastxtile_tertiles(x):
    """Replicate Stata's fastxtile behavior exactly - position-based with ties to lower tertile"""
    try:
        if len(x.dropna()) < 3:
            return pd.Series(np.nan, index=x.index)
        
        valid_x = x.dropna()
        if len(valid_x) == 0:
            return pd.Series(np.nan, index=x.index)
        
        # Sort values and get their positions
        sorted_values = valid_x.sort_values()
        n_obs = len(sorted_values)
        
        # Calculate position-based cutoffs (use ceiling to include boundary cases in lower tertile)
        # This matches Stata's fastxtile behavior where boundary cases go to lower tertile
        tertile_1_cutoff_pos = int(np.ceil(n_obs * 1/3)) - 1  # Last position in first tertile (0-indexed)
        tertile_2_cutoff_pos = int(np.ceil(n_obs * 2/3)) - 1  # Last position in second tertile (0-indexed)
        
        # Get the actual values at these positions
        if tertile_1_cutoff_pos < n_obs:
            p33_value = sorted_values.iloc[tertile_1_cutoff_pos]
        else:
            p33_value = sorted_values.iloc[-1]
            
        if tertile_2_cutoff_pos < n_obs:
            p67_value = sorted_values.iloc[tertile_2_cutoff_pos]  
        else:
            p67_value = sorted_values.iloc[-1]
        
        # Assign tertiles - values <= boundary go to lower tertile
        # But we need to handle the next value after boundary too (Stata includes ties)
        result = pd.Series(np.nan, index=x.index)
        
        # Find values that are exactly equal to the next value after boundary
        next_val_after_p33 = None
        next_val_after_p67 = None
        
        if tertile_1_cutoff_pos + 1 < n_obs:
            next_val_after_p33 = sorted_values.iloc[tertile_1_cutoff_pos + 1]
        
        if tertile_2_cutoff_pos + 1 < n_obs:
            next_val_after_p67 = sorted_values.iloc[tertile_2_cutoff_pos + 1]
        
        # Include ties with the boundary value in the lower tertile
        p33_tie_cutoff = next_val_after_p33 if next_val_after_p33 is not None else p33_value
        p67_tie_cutoff = next_val_after_p67 if next_val_after_p67 is not None else p67_value
        
        result.loc[x <= p33_tie_cutoff] = 1  # <= to include ties in lower tertile
        result.loc[(x > p33_tie_cutoff) & (x <= p67_tie_cutoff)] = 2  
        result.loc[x > p67_tie_cutoff] = 3
        
        return result
    except:
        return pd.Series(np.nan, index=x.index)

df['tempsizeq'] = df.groupby('time_avail_m')['mve_c'].transform(fastxtile_tertiles)
df.loc[df['tempsizeq'] >= 2, 'RDcap'] = np.nan

# Keep only necessary columns for output
df_final = df[['permno', 'time_avail_m', 'RDcap']].copy()
df_final = df_final.dropna(subset=['RDcap'])

# Convert time_avail_m to yyyymm format like other predictors
df_final['yyyymm'] = df_final['time_avail_m'].dt.year * 100 + df_final['time_avail_m'].dt.month

# Convert to integers for consistency with other predictors
df_final['permno'] = df_final['permno'].astype('int64')
df_final['yyyymm'] = df_final['yyyymm'].astype('int64')

# Keep only required columns and set index
df_final = df_final[['permno', 'yyyymm', 'RDcap']].copy()
df_final = df_final.set_index(['permno', 'yyyymm'])

# SAVE
df_final.to_csv('../pyData/Predictors/RDcap.csv')

print("RDcap predictor saved successfully")