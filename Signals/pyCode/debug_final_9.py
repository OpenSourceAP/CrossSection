# Debug the final 9 missing observations
import pandas as pd
import numpy as np

remaining_missing = [
    (10516, 196212), (10516, 196301),
    (19430, 196212), (19430, 196301), 
    (26112, 196212), (26112, 196301),
    (27094, 196301), (27713, 196301), (37102, 196301)
]

# Load data exactly like Frontier.py
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

stata_base = pd.to_datetime('1960-01-01')
df['time_avail'] = ((df['time_avail_m'].dt.year - stata_base.year) * 12 + 
                    (df['time_avail_m'].dt.month - stata_base.month))

df['xad'] = df['xad'].fillna(0)
df['YtempBM'] = np.log(df['mve_c'])
df['YtempBM'] = df['YtempBM'].replace([np.inf, -np.inf], np.nan)

df['tempBook'] = np.log(df['ceq'])
df['tempBook'] = df['tempBook'].replace([np.inf, -np.inf], np.nan)

df['tempLTDebt'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['dltt'] / df['at'])
df['tempCapx'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['capx'] / df['sale'])
df['tempRD'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['xrd'] / df['sale'])
df['tempAdv'] = np.where((df['sale'] == 0) | df['sale'].isna(), np.nan, df['xad'] / df['sale'])
df['tempPPE'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['ppent'] / df['at'])
df['tempEBIT'] = np.where((df['at'] == 0) | df['at'].isna(), np.nan, df['ebitda'] / df['at'])

def get_ff48(sic):
    if pd.isna(sic):
        return np.nan
    sic = int(sic)
    if 100 <= sic <= 999:
        return 1
    elif 1000 <= sic <= 1099:
        return 2
    else:
        return 48  # Simplified

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)
df = df.dropna(subset=['tempFF48'])

reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

print("Final 9 missing observations - training data analysis:")
print("=" * 70)

for permno, yyyymm in remaining_missing:
    year = yyyymm // 100
    month = yyyymm % 100
    current_date = pd.to_datetime(f'{year}-{month:02d}-01')
    
    current_time_avail = ((current_date.year - stata_base.year) * 12 + 
                         (current_date.month - stata_base.month))
    months_back_60 = current_time_avail - 60
    
    train_data = df[(df['time_avail'] <= current_time_avail) & 
                   (df['time_avail'] > months_back_60)].copy()
    
    train_data_clean = train_data.dropna(subset=['YtempBM'] + reg_vars + ['tempFF48'])
    
    print(f"Permno {permno}, {current_date.strftime('%Y-%m')}: {len(train_data_clean)} clean training obs")
    
    if len(train_data_clean) > 0:
        print(f"  Date range: {train_data_clean['time_avail_m'].min().strftime('%Y-%m')} to {train_data_clean['time_avail_m'].max().strftime('%Y-%m')}")
        industries = train_data_clean['tempFF48'].unique()
        print(f"  Industries: {sorted(industries)}")
        
        # Check if we have at least one observation per industry for regression
        industry_counts = train_data_clean['tempFF48'].value_counts()
        print(f"  Industry distribution: {dict(industry_counts)}")
        
        # Check if regression variables have sufficient variation
        reg_var_info = {}
        for var in reg_vars:
            values = train_data_clean[var].dropna()
            if len(values) > 0:
                reg_var_info[var] = f"n={len(values)}, range=[{values.min():.3f}, {values.max():.3f}]"
            else:
                reg_var_info[var] = "n=0"
        
        print(f"  Key reg vars: tempBook: {reg_var_info['tempBook']}, tempLTDebt: {reg_var_info['tempLTDebt']}")

print(f"\nCurrent minimum threshold: 10 observations")
print(f"Recommendation: Lower to 3-5 observations for very early periods")
print(f"Or add special handling for periods before 1963")