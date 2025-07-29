# Check if missing Frontier observations exist in our Python data
import pandas as pd

# Load Python and Stata data
python_data = pd.read_csv('../pyData/Predictors/Frontier.csv')
python_data['permno'] = python_data['permno']
python_data['yyyymm'] = python_data['yyyymm']

# Read the missing observations from test output
missing_obs = [
    (10006, 196310),
    (10006, 196311), 
    (10006, 196312),
    (10006, 196401),
    (10006, 196402),
    (10006, 196403),
    (10006, 196404),
    (10006, 196405),
    (10006, 196406),
    (10006, 196407)
]

print("Checking if missing observations exist in source data...")

# Load our source data before final filtering
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'mve_c', 'sicCRSP']].copy()

comp = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet')
comp = comp[['permno', 'time_avail_m', 'at', 'ceq', 'dltt', 'capx', 'sale', 'xrd', 'xad', 'ppent', 'ebitda']].copy()
df = df.merge(comp, on=['permno', 'time_avail_m'], how='inner')

# Convert to yyyymm format for checking
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

for permno, yyyymm in missing_obs:
    # Check if exists in source data
    exists_in_source = ((df['permno'] == permno) & (df['yyyymm'] == yyyymm)).any()
    
    # Check if exists in final output
    exists_in_output = ((python_data['permno'] == permno) & (python_data['yyyymm'] == yyyymm)).any()
    
    print(f"permno {permno}, yyyymm {yyyymm}: source={exists_in_source}, output={exists_in_output}")
    
    if exists_in_source:
        # Show the data
        source_row = df[(df['permno'] == permno) & (df['yyyymm'] == yyyymm)]
        print(f"  Source data: ceq={source_row['ceq'].iloc[0]:.3f}, mve_c={source_row['mve_c'].iloc[0]:.3f}")
        
        # Check if ceq filter would remove it
        ceq_val = source_row['ceq'].iloc[0]
        if pd.isna(ceq_val) or ceq_val <= 0:
            print(f"  FILTERED OUT: ceq={ceq_val} fails ceq filter")
    else:
        print(f"  NOT IN SOURCE DATA")

# Summary check for permno 10006 in early 1960s
print(f"\nPermno 10006 data availability:")
permno_10006 = df[df['permno'] == 10006].copy()
print(f"Total observations: {len(permno_10006)}")
print(f"Date range: {permno_10006['time_avail_m'].min()} to {permno_10006['time_avail_m'].max()}")

early_1960s = permno_10006[permno_10006['yyyymm'] < 196500]
print(f"Pre-1965 observations: {len(early_1960s)}")
if len(early_1960s) > 0:
    print("Sample pre-1965 data:")
    print(early_1960s[['yyyymm', 'ceq', 'mve_c']].head())