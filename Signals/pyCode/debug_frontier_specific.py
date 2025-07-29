# Debug specific Frontier issue - focus on permno 49315, 1973-06
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load data  
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Check all data for this problematic permno
problem_permno = 49315
problem_date = pd.to_datetime('1973-06-01')

all_permno_data = df[df['permno'] == problem_permno].copy()
print(f"All data for permno {problem_permno}:")
print(f"Total observations: {len(all_permno_data)}")
print(f"Date range: {all_permno_data['time_avail_m'].min()} to {all_permno_data['time_avail_m'].max()}")
print("Sample data:")
print(all_permno_data[['permno', 'time_avail_m', 'mve_c', 'ceq', 'at', 'sicCRSP']].head(10))

# Also check broader date range for context
date_range_start = pd.to_datetime('1965-01-01') 
date_range_end = pd.to_datetime('1975-12-31')

df_broader = df[(df['permno'] == problem_permno) & 
                (df['time_avail_m'] >= date_range_start) & 
                (df['time_avail_m'] <= date_range_end)].copy()

print(f"\nPermno {problem_permno} data from 1965-1975:")
print(f"Observations in decade: {len(df_broader)}")
if len(df_broader) > 0:
    print("All observations in range:")
    print(df_broader[['time_avail_m', 'mve_c', 'ceq', 'at']].to_string())

# Create time_avail using Stata format
stata_base = pd.to_datetime('1960-01-01')
df['time_avail'] = ((df['time_avail_m'].dt.year - stata_base.year) * 12 + 
                    (df['time_avail_m'].dt.month - stata_base.month))

# Create variables
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
        return 1  
    elif 1000 <= sic <= 1099:
        return 2  
    elif 1200 <= sic <= 1399:
        return 3  
    elif 1400 <= sic <= 1499:
        return 4  
    elif 1500 <= sic <= 1999:
        return 5  
    elif 2000 <= sic <= 2099:
        return 6  
    else:
        return 48  # Simplified for debug

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)
df = df.dropna(subset=['tempFF48'])

reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

# Now analyze the specific regression for June 1973
current_date = problem_date
current_time_avail = ((current_date.year - stata_base.year) * 12 + 
                     (current_date.month - stata_base.month))

date_60_months_back = current_date - pd.DateOffset(months=60)

print(f"\nAnalyzing regression for {current_date.strftime('%Y-%m')}:")
print(f"current_time_avail = {current_time_avail}")
date_60_months_back = current_date - pd.DateOffset(months=60)
print(f"60 months back (date) = {date_60_months_back.strftime('%Y-%m')}")
months_back_60 = current_time_avail - 60
print(f"60 months back (time_avail) = {months_back_60}")

# Get training data using calendar-based logic (like Stata `t' - 60)
months_back_60 = current_time_avail - 60
train_data = df[(df['time_avail'] <= current_time_avail) & 
               (df['time_avail'] > months_back_60)].copy()

print(f"Training data size: {len(train_data)} observations")
print(f"Training date range: {train_data['time_avail_m'].min()} to {train_data['time_avail_m'].max()}")

# Check if our problem permno is in training data
problem_in_training = train_data[train_data['permno'] == problem_permno]
print(f"Permno {problem_permno} in training data: {len(problem_in_training)} observations")

if len(problem_in_training) > 0:
    print("Sample training data for problem permno:")
    print(problem_in_training[['time_avail_m', 'YtempBM'] + reg_vars].head())
    
# Check if there's data to predict for current period
current_data = df[df['time_avail_m'] == current_date].copy()
problem_current = current_data[current_data['permno'] == problem_permno]
print(f"\nCurrent period data for permno {problem_permno}: {len(problem_current)} observations")

if len(problem_current) > 0:
    print("Values for prediction:")
    print(problem_current[['YtempBM'] + reg_vars + ['sicCRSP', 'tempFF48']])