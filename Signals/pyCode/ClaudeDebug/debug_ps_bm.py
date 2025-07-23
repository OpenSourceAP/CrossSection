import pandas as pd
import numpy as np

# Full PS calculation up to BM quintile restriction
compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet', 
                               columns=['permno', 'time_avail_m', 'fopt', 'oancf', 'ib', 'at', 'dltt', 'act', 'lct', 'txt', 'xint', 'sale', 'ceq'])
signal_df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet', 
                           columns=['permno', 'time_avail_m', 'mve_c'])
crsp_df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', 
                         columns=['permno', 'time_avail_m', 'shrout'])

df = compustat_df.merge(signal_df, on=['permno', 'time_avail_m'], how='inner')
df = df.merge(crsp_df, on=['permno', 'time_avail_m'], how='inner')
df = df.sort_values(['permno', 'time_avail_m'])
df['fopt'] = df['fopt'].fillna(df['oancf'])

# Create lags and calculate PS (abbreviated for brevity)
df['time_lag12'] = df['time_avail_m'] - pd.DateOffset(months=12)
lag_vars = ['ib', 'at', 'dltt', 'act', 'lct', 'sale', 'shrout']
for var in lag_vars:
    lag_data = df[['permno', 'time_avail_m', var]].copy()
    lag_data.columns = ['permno', 'time_lag12', f'l12_{var}']
    df = df.merge(lag_data, on=['permno', 'time_lag12'], how='left')
df = df.drop('time_lag12', axis=1)

# Calculate PS components (abbreviated)
df['p1'] = (df['ib'] > 0).astype(int)
df['p2'] = (df['fopt'] > 0).astype(int)
df['p3'] = ((df['ib']/df['at'] - df['l12_ib']/df['l12_at']) > 0).astype(int)
df['p4'] = (df['fopt'] > df['ib']).astype(int)
df['p5'] = ((df['dltt']/df['at'] - df['l12_dltt']/df['l12_at']) < 0).astype(int)
df['p6'] = ((df['act']/df['lct'] - df['l12_act']/df['l12_lct']) > 0).astype(int)
df['tempebit'] = df['ib'] + df['txt'] + df['xint']
df['p7'] = ((df['tempebit']/df['sale'] - df['tempebit']/df['l12_sale']) > 0).astype(int)
df['p8'] = ((df['sale']/df['at'] - df['l12_sale']/df['l12_at']) > 0).astype(int)
df['p9'] = (df['shrout'] <= df['l12_shrout']).astype(int)
df['PS'] = df['p1'] + df['p2'] + df['p3'] + df['p4'] + df['p5'] + df['p6'] + df['p7'] + df['p8'] + df['p9']

# Apply missing value filter
df.loc[(df['fopt'].isna()) | (df['ib'].isna()) | (df['at'].isna()) | (df['dltt'].isna()) | 
       (df['sale'].isna()) | (df['act'].isna()) | (df['tempebit'].isna()) | (df['shrout'].isna()), 'PS'] = np.nan

target_dates = pd.to_datetime(['2024-09-01', '2024-10-01', '2024-11-01'])
target_permno = 23033

print('Checking BM quintile restriction (following PS.py exactly):')
print('='*60)

# Calculate BM exactly as in PS.py (lines 108-115)
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['BM_clean'] = df['BM'].replace([np.inf, -np.inf], np.nan)

# Apply quintile transformation exactly as in PS.py
df['temp'] = df.groupby('time_avail_m')['BM_clean'].transform(
    lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1
)

for date in target_dates:
    date_str = date.strftime('%Y-%m-%d')
    print(f'\n{date_str}:')
    
    # Get target observation
    target_obs = df[(df['permno'] == target_permno) & (df['time_avail_m'] == date)]
    if len(target_obs) == 0:
        print('  No observation found!')
        continue
        
    target_obs = target_obs.iloc[0]
    
    # Show BM values
    ceq = target_obs['ceq']
    mve_c = target_obs['mve_c']
    bm = target_obs['BM']
    bm_clean = target_obs['BM_clean']
    temp_quintile = target_obs['temp']
    
    print(f'  ceq: {ceq:.3f}')
    print(f'  mve_c: {mve_c:.6f}')
    print(f'  BM = ln(ceq/mve_c) = {bm:.6f}')
    print(f'  BM_clean: {bm_clean:.6f}')
    print(f'  Quintile (temp): {temp_quintile}')
    
    # Check the filter condition
    if pd.isna(temp_quintile):
        print('  ✗ Missing quintile - EXCLUDED')
    elif temp_quintile != 5:
        print(f'  ✗ Not in highest quintile (need 5, got {temp_quintile}) - EXCLUDED')
    else:
        print('  ✓ In highest BM quintile (5) - INCLUDED')
        
    # Show some quintile stats for this month
    month_data = df[df['time_avail_m'] == date]
    month_quintiles = month_data['temp'].value_counts().sort_index()
    print(f'  Month quintile distribution: {dict(month_quintiles)}')

print('\nFinal check - applying line 115 filter:')
# Apply the filter as in PS.py line 115
df.loc[df['temp'] != 5, 'PS'] = np.nan

for date in target_dates:
    date_str = date.strftime('%Y-%m-%d')
    target_obs = df[(df['permno'] == target_permno) & (df['time_avail_m'] == date)]
    if len(target_obs) > 0:
        ps_value = target_obs.iloc[0]['PS']
        print(f'{date_str}: PS after BM filter = {ps_value}')