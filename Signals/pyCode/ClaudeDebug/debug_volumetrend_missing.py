import pandas as pd
import numpy as np

print("=== Debugging VolumeTrend missing observations ===")

# Focus on permno 10001 which shows missing observations in 1988
target_permno = 10001

# Load the data
df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')
df = df[['permno', 'time_avail_m', 'vol']].copy()

# Focus on the target permno
permno_data = df[df['permno'] == target_permno].copy()
permno_data = permno_data.sort_values('time_avail_m')

print(f"Data for permno {target_permno}:")
print(f"Total observations: {len(permno_data)}")
print(f"Date range: {permno_data['time_avail_m'].min()} to {permno_data['time_avail_m'].max()}")

# Check early data around 1988
early_data = permno_data[permno_data['time_avail_m'] < pd.Timestamp('1990-01-01')]
print(f"\nEarly data (before 1990): {len(early_data)} observations")
if len(early_data) > 0:
    print(early_data[['time_avail_m', 'vol']].head(20).to_string(index=False))

# Check what happens with the rolling window logic
print(f"\n=== Analyzing rolling window requirements ===")

# The missing observations start around 198806 (1988-06)
# For a 60-month window to start producing results in 1988-06,
# we need data going back to 1983-06 (5 years * 12 months = 60 months)

target_date = pd.Timestamp('1988-06-01')
window_start = target_date - pd.DateOffset(months=59)  # 60 months including current

print(f"For results in {target_date.strftime('%Y-%m')}:")
print(f"Need data starting from: {window_start.strftime('%Y-%m')}")

# Check if we have data in that range
data_in_window = permno_data[(permno_data['time_avail_m'] >= window_start) & 
                            (permno_data['time_avail_m'] <= target_date)]
print(f"Available data in window: {len(data_in_window)} observations")

if len(data_in_window) >= 30:
    print(f"✅ Should produce VolumeTrend result (>= 30 min observations)")
else:
    print(f"❌ Should NOT produce result (< 30 min observations)")

# Check what Stata actually produces
stata_df = pd.read_csv('../Data/Predictors/VolumeTrend.csv')
stata_10001 = stata_df[(stata_df['permno'] == target_permno) & 
                       (stata_df['yyyymm'] >= 198806) & 
                       (stata_df['yyyymm'] <= 198812)]

print(f"\nStata results for permno {target_permno} in 1988-06 to 1988-12:")
print(f"Count: {len(stata_10001)}")
if len(stata_10001) > 0:
    print(stata_10001.to_string(index=False))

# Check Python results for the same period
python_df = pd.read_csv('../pyData/Predictors/VolumeTrend.csv')
python_10001 = python_df[(python_df['permno'] == target_permno) & 
                         (python_df['yyyymm'] >= 198806) & 
                         (python_df['yyyymm'] <= 198812)]

print(f"\nPython results for permno {target_permno} in 1988-06 to 1988-12:")
print(f"Count: {len(python_10001)}")
if len(python_10001) > 0:
    print(python_10001.to_string(index=False))

print(f"\n=== Key issue identification ===")
if len(stata_10001) > 0 and len(python_10001) == 0:
    print("❌ Stata produces results but Python doesn't")
    print("This suggests Python's window logic is too restrictive")
elif len(stata_10001) == 0 and len(python_10001) > 0:
    print("❌ Python produces results but Stata doesn't")
    print("This suggests Python's window logic is too lenient")
else:
    print("✅ Both produce same result count")

# Check the actual data availability for the first few years
print(f"\n=== Early data availability check ===")
earliest_data = permno_data.head(80)  # First ~7 years of data
print(f"First 80 observations:")
for i, (_, row) in enumerate(earliest_data.iterrows()):
    # For each observation, check how many previous observations are available
    prev_count = i  # Number of previous observations
    months_back = (row['time_avail_m'] - earliest_data.iloc[0]['time_avail_m']).days / 30.44
    
    if i >= 30 and i < 35:  # Show a few examples around the minimum threshold
        print(f"  {row['time_avail_m'].strftime('%Y-%m')}: {prev_count:2d} prev obs, {months_back:5.1f} months back")
        
        # Check if this should produce a result
        if prev_count >= 29:  # Need at least 30 total (including current)
            print(f"    -> Should produce result ({prev_count + 1} >= 30 min)")
        else:
            print(f"    -> Should NOT produce result ({prev_count + 1} < 30 min)")