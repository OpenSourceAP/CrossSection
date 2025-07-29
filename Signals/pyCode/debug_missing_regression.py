# Debug why specific observations aren't getting regression predictions
import pandas as pd
import numpy as np

# Load and prepare data exactly like Frontier.py
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Create time_avail 
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

# FF48 classification (simplified)
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
    else:
        return 48  # Simplified for debug

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)
df = df.dropna(subset=['tempFF48'])

reg_vars = ['tempBook', 'tempLTDebt', 'tempCapx', 'tempRD', 'tempAdv', 'tempPPE', 'tempEBIT']

# Check why permno 10006, Oct 1963 doesn't get a prediction
problem_permno = 10006
problem_date = pd.to_datetime('1963-10-01')

print(f"Debugging permno {problem_permno}, {problem_date.strftime('%Y-%m')}:")

# Convert to time_avail
current_time_avail = ((problem_date.year - stata_base.year) * 12 + 
                     (problem_date.month - stata_base.month))
print(f"current_time_avail = {current_time_avail}")

# Check if current observation exists and has valid data
current_data = df[df['time_avail_m'] == problem_date].copy()
problem_current = current_data[current_data['permno'] == problem_permno]

print(f"Current period data for permno {problem_permno}: {len(problem_current)} observations")
if len(problem_current) > 0:
    print("Current observation exists")
    print(f"YtempBM: {problem_current['YtempBM'].iloc[0]}")
    print(f"Regression vars: {problem_current[reg_vars].iloc[0].to_dict()}")
    has_missing_reg_vars = problem_current[reg_vars].isna().any(axis=1).iloc[0]
    print(f"Has missing regression vars: {has_missing_reg_vars}")
else:
    print("Current observation MISSING")

# Check training data
months_back_60 = current_time_avail - 60
print(f"Training window: time_avail > {months_back_60} AND time_avail <= {current_time_avail}")

train_data = df[(df['time_avail'] <= current_time_avail) & 
               (df['time_avail'] > months_back_60)].copy()

print(f"Total training data size: {len(train_data)} observations")

# Check if training data is sufficient
train_data_clean = train_data.dropna(subset=['YtempBM'] + reg_vars)
print(f"Training data after dropping NaN: {len(train_data_clean)} observations")

if len(train_data_clean) < 30:
    print("ISSUE: Insufficient training data (< 30 observations)")
elif len(train_data_clean) < 50:
    print("ISSUE: Training data below minimum threshold (< 50 observations)")
else:
    print("Training data size looks sufficient")
    
    # Check industry dummies
    industry_dummies = pd.get_dummies(train_data_clean['tempFF48'], prefix='ff48')
    print(f"Industry dummies: {len(industry_dummies.columns)} industries")
    
    # Check if current observation can be predicted
    if len(problem_current) > 0 and not has_missing_reg_vars:
        current_industry = pd.get_dummies(problem_current['tempFF48'], prefix='ff48')
        print(f"Current observation industry: {problem_current['tempFF48'].iloc[0]}")
        
        # Check if all required dummy columns exist
        missing_dummies = []
        for col in industry_dummies.columns:
            if col not in current_industry.columns:
                missing_dummies.append(col)
        
        if missing_dummies:
            print(f"Missing industry dummies for prediction: {len(missing_dummies)}")
        else:
            print("All industry dummies available for prediction")

# Check what date range training data spans for this specific problem
if len(train_data) > 0:
    print(f"Training data date range: {train_data['time_avail_m'].min()} to {train_data['time_avail_m'].max()}")
    
    # Check for early period data availability
    early_cutoff = pd.to_datetime('1965-01-01')
    if problem_date < early_cutoff:
        print(f"EARLY PERIOD ISSUE: Problem date {problem_date.strftime('%Y-%m')} is before {early_cutoff.strftime('%Y-%m')}")
        print("This might be filtered out by the min_history_date logic")