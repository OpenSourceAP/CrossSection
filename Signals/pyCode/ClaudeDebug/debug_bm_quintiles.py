import pandas as pd
import numpy as np

# Load data to understand BM quintile boundaries
signal_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                           columns=['permno', 'time_avail_m', 'mve_c'])
compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                               columns=['permno', 'time_avail_m', 'ceq'])

# Focus on Sept 2024
target_date = pd.to_datetime('2024-09-01')
merged = compustat_df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')
sept_merged = merged[merged['time_avail_m'] == target_date].copy()

# Calculate BM
sept_merged['BM'] = np.log(sept_merged['ceq'] / sept_merged['mve_c'])
sept_merged['BM_clean'] = sept_merged['BM'].replace([np.inf, -np.inf], np.nan)
sept_merged = sept_merged.dropna(subset=['BM_clean'])

print(f'September 2024 BM statistics:')
print(f'Total observations: {len(sept_merged)}')
print(f'BM_clean stats: min={sept_merged["BM_clean"].min():.6f}, max={sept_merged["BM_clean"].max():.6f}')

# Calculate quintiles manually
quintiles = sept_merged['BM_clean'].quantile([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
print('\nQuintile boundaries:')
for i, (q, val) in enumerate(quintiles.items()):
    print(f'  {q*100:.0f}%: {val:.6f}')
    
# Check where our target would fall
target_bm = 0.144817  # From earlier analysis
print(f'\nTarget BM: {target_bm:.6f}')
print('Target falls between:')
for i in range(len(quintiles)-1):
    if quintiles.iloc[i] <= target_bm <= quintiles.iloc[i+1]:
        print(f'  Quintile {i+1}: [{quintiles.iloc[i]:.6f}, {quintiles.iloc[i+1]:.6f}]') 
        
# Count how many observations are in quintile 5
quint5_threshold = quintiles.iloc[4]  # 80th percentile
quint5_count = (sept_merged['BM_clean'] >= quint5_threshold).sum()
print(f'\nQuintile 5 threshold: {quint5_threshold:.6f}')
print(f'Observations in quintile 5: {quint5_count}')
comparison = 'above' if target_bm >= quint5_threshold else 'below'
print(f'Our target BM ({target_bm:.6f}) is {comparison} this threshold')

# Show the exact qcut assignment
sept_merged['temp_quintile'] = pd.qcut(sept_merged['BM_clean'], q=5, labels=False, duplicates='drop') + 1
target_quintile_check = sept_merged[sept_merged['permno'] == 23033]
if len(target_quintile_check) > 0:
    print(f'\nActual quintile assignment for permno 23033: {target_quintile_check.iloc[0]["temp_quintile"]}')
else:
    print('\nNo data found for permno 23033 in September 2024')

# Check very close to quintile boundaries
print(f'\nAnalyzing observations near quintile 4-5 boundary:')
boundary_45 = quintiles.iloc[4]  # 80th percentile
near_boundary = sept_merged[abs(sept_merged['BM_clean'] - boundary_45) < 0.01].copy()
near_boundary = near_boundary.sort_values('BM_clean')
print(f'Observations within 0.01 of quintile 4-5 boundary ({boundary_45:.6f}):')
for _, row in near_boundary.head(10).iterrows():
    print(f'  permno {row["permno"]}: BM={row["BM_clean"]:.6f}, quintile={row["temp_quintile"]}')