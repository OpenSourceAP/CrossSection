# Debug the remaining 27 missing Frontier observations
import pandas as pd
import numpy as np

print("Analyzing the remaining 27 missing observations...")

# Load test results to get the exact missing observations
missing_obs = [
    (10516, 196212), (10516, 196301), (10516, 196302), (10516, 196303),
    (16280, 196302), (16280, 196303), (17670, 196303),
    (19430, 196212), (19430, 196301), (19430, 196302)
]

# Load our source data
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Convert to yyyymm
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

# Create time_avail using Stata format
stata_base = pd.to_datetime('1960-01-01')
df['time_avail'] = ((df['time_avail_m'].dt.year - stata_base.year) * 12 + 
                    (df['time_avail_m'].dt.month - stata_base.month))

# Create variables like Frontier.py
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

# FF48 classification
def get_ff48(sic):
    if pd.isna(sic):
        return np.nan
    sic = int(sic)
    if 100 <= sic <= 999:
        return 1  # Agriculture
    elif 1000 <= sic <= 1099:
        return 2  # Mining
    elif 1200 <= sic <= 1399:
        return 3  # Coal
    elif 1400 <= sic <= 1499:
        return 4  # Oil
    elif 1500 <= sic <= 1999:
        return 5  # Construction
    elif 2000 <= sic <= 2099:
        return 6  # Food
    elif 2100 <= sic <= 2199:
        return 7  # Soda
    elif 2200 <= sic <= 2269 or 2270 <= sic <= 2299:
        return 8  # Textiles
    elif 2300 <= sic <= 2399:
        return 9  # Apparel
    elif 2400 <= sic <= 2499:
        return 10  # Wood
    elif 2500 <= sic <= 2549 or 2590 <= sic <= 2599:
        return 11  # Furniture
    elif 2600 <= sic <= 2699:
        return 12  # Paper
    elif 2700 <= sic <= 2749 or 2770 <= sic <= 2799:
        return 13  # Printing
    elif 2800 <= sic <= 2829 or 2840 <= sic <= 2899:
        return 14  # Chemicals
    elif 2830 <= sic <= 2839:
        return 15  # Drugs
    elif 2900 <= sic <= 2999:
        return 16  # Petroleum
    elif 3000 <= sic <= 3099:
        return 17  # Rubber
    elif 3100 <= sic <= 3199:
        return 18  # Leather
    elif 3200 <= sic <= 3299:
        return 19  # Stone
    elif 3300 <= sic <= 3399:
        return 20  # Steel
    elif 3400 <= sic <= 3499:
        return 21  # Fabricated Metal
    elif 3500 <= sic <= 3569 or 3580 <= sic <= 3599:
        return 22  # Machinery
    elif 3570 <= sic <= 3579:
        return 23  # Computers
    elif 3600 <= sic <= 3699:
        return 24  # Electronic Equipment
    elif 3700 <= sic <= 3799:
        return 25  # Transportation
    elif 3800 <= sic <= 3829 or 3860 <= sic <= 3899:
        return 26  # Instruments
    elif 3830 <= sic <= 3859:
        return 27  # Photo
    elif 3900 <= sic <= 3999:
        return 28  # Other Manufacturing
    elif 4000 <= sic <= 4099:
        return 29  # Railroad
    elif 4100 <= sic <= 4199:
        return 30  # Shipping
    elif 4200 <= sic <= 4299:
        return 31  # Transportation
    elif 4400 <= sic <= 4499:
        return 32  # Water
    elif 4500 <= sic <= 4599:
        return 33  # Aircraft
    elif 4600 <= sic <= 4699:
        return 34  # Communication
    elif 4700 <= sic <= 4799:
        return 35  # Communication
    elif 4800 <= sic <= 4899:
        return 36  # Communication  
    elif 4900 <= sic <= 4999:
        return 37  # Utilities
    elif 5000 <= sic <= 5099:
        return 38  # Wholesale
    elif 5100 <= sic <= 5199:
        return 39  # Wholesale
    elif 5200 <= sic <= 5999:
        return 40  # Retail
    elif 6000 <= sic <= 6099:
        return 41  # Banks
    elif 6100 <= sic <= 6199:
        return 42  # Insurance
    elif 6200 <= sic <= 6299:
        return 43  # Real Estate
    elif 6300 <= sic <= 6399:
        return 44  # Insurance
    elif 6400 <= sic <= 6499:
        return 45  # Insurance
    elif 6500 <= sic <= 6599:
        return 46  # Real Estate
    elif 6700 <= sic <= 6799:
        return 47  # Finance
    elif 7000 <= sic <= 8999:
        return 48  # Other
    else:
        return 48  # Other

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)

reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

print("\nAnalyzing each missing observation:")
print("=" * 80)

for permno, yyyymm in missing_obs:
    print(f"\nPermno {permno}, yyyymm {yyyymm}:")
    
    # Convert yyyymm back to date
    year = yyyymm // 100
    month = yyyymm % 100
    current_date = pd.to_datetime(f'{year}-{month:02d}-01')
    
    # Check if observation exists in source data
    exists_in_source = ((df['permno'] == permno) & (df['yyyymm'] == yyyymm)).any()
    
    if not exists_in_source:
        print(f"  ❌ NOT IN SOURCE DATA")
        continue
    
    print(f"  ✅ EXISTS IN SOURCE DATA")
    
    # Get the observation
    obs = df[(df['permno'] == permno) & (df['yyyymm'] == yyyymm)].iloc[0]
    
    # Check each filter condition
    print(f"  ceq: {obs['ceq']:.3f} (>0: {obs['ceq'] > 0 if not pd.isna(obs['ceq']) else False})")
    print(f"  tempFF48: {obs['tempFF48']} (not NaN: {not pd.isna(obs['tempFF48'])})")
    print(f"  YtempBM: {obs['YtempBM']:.3f} (not NaN: {not pd.isna(obs['YtempBM'])})")
    
    # Check regression variables
    reg_var_status = {}
    has_missing_reg_vars = False
    for var in reg_vars:
        is_valid = not pd.isna(obs[var])
        reg_var_status[var] = is_valid
        if not is_valid:
            has_missing_reg_vars = True
    
    print(f"  Regression vars valid: {not has_missing_reg_vars}")
    if has_missing_reg_vars:
        missing_vars = [var for var, valid in reg_var_status.items() if not valid]
        print(f"    Missing: {missing_vars}")
    
    # Check training data availability
    current_time_avail = ((current_date.year - stata_base.year) * 12 + 
                         (current_date.month - stata_base.month))
    months_back_60 = current_time_avail - 60
    
    train_data = df[(df['time_avail'] <= current_time_avail) & 
                   (df['time_avail'] > months_back_60)].copy()
    
    train_data_clean = train_data.dropna(subset=['YtempBM'] + reg_vars + ['tempFF48'])
    
    print(f"  Training data: {len(train_data_clean)} observations (min 50 required)")
    
    if len(train_data_clean) < 50:
        print(f"  ❌ INSUFFICIENT TRAINING DATA")
        continue
    
    # Check if current observation passes all filters
    passes_ceq = not pd.isna(obs['ceq']) and obs['ceq'] > 0
    passes_ff48 = not pd.isna(obs['tempFF48'])
    passes_ytempbm = not pd.isna(obs['YtempBM'])
    passes_reg_vars = not has_missing_reg_vars
    
    all_filters_pass = passes_ceq and passes_ff48 and passes_ytempbm and passes_reg_vars
    
    if all_filters_pass:
        print(f"  ✅ ALL FILTERS PASS - SHOULD HAVE PREDICTION")
        print(f"     This suggests a bug in the regression logic!")
    else:
        print(f"  ❌ FAILS SOME FILTER")
        print(f"     ceq: {passes_ceq}, ff48: {passes_ff48}, ytempbm: {passes_ytempbm}, reg_vars: {passes_reg_vars}")