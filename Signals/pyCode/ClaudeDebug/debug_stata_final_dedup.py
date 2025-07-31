import pandas as pd
import numpy as np

print("=== Debugging Stata's final deduplication logic ===")

# The Stata logic after expansion is:
# gsort gvkey time_avail_m -rdq
# quietly by gvkey time_avail_m:  gen dup = cond(_N==1,0,_n)
# keep if dup == 0

test_gvkey = 1076.0

# Simulate the full process
qcompustat_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet',
                               columns=['gvkey', 'rdq', 'cheq', 'atq'])

# Step 1: Initial filtering and dedup
gvkey_data = qcompustat_df[qcompustat_df['gvkey'] == test_gvkey].copy()
gvkey_data = gvkey_data.dropna(subset=['gvkey', 'atq'])
gvkey_data = gvkey_data.sort_values(['gvkey', 'rdq'])
gvkey_data = gvkey_data.drop_duplicates(['gvkey', 'rdq'], keep='first')

print(f"After initial dedup: {len(gvkey_data)} quarters")

# Step 2: Add time_avail_m and expand
gvkey_data['time_avail_m'] = pd.to_datetime(gvkey_data['rdq']).dt.to_period('M').dt.to_timestamp()

# Expand to monthly
expanded_dfs = []
for month_offset in range(3):
    df_copy = gvkey_data.copy()
    df_copy['time_avail_m'] = df_copy['time_avail_m'] + pd.DateOffset(months=month_offset)
    expanded_dfs.append(df_copy)

expanded_df = pd.concat(expanded_dfs, ignore_index=True)
print(f"After expansion: {len(expanded_df)} monthly observations")

# Step 3: Focus on Oct 1984 and surrounding months
focus_months = expanded_df[
    (expanded_df['time_avail_m'] >= '1984-08-01') & 
    (expanded_df['time_avail_m'] <= '1984-12-01')
].copy()

print(f"\nExpanded data for Aug-Dec 1984:")
focus_months = focus_months.sort_values(['time_avail_m', 'rdq'])
for _, row in focus_months.iterrows():
    time_avail = row['time_avail_m']
    rdq = row['rdq']
    cheq = row['cheq']
    atq = row['atq']
    cash = cheq / atq if atq != 0 else np.nan
    print(f"  {time_avail}: rdq={rdq}, Cash={cash:.6f}")

# Step 4: Apply Stata's final deduplication
# gsort gvkey time_avail_m -rdq (sort by gvkey, time_avail_m, rdq descending)
# keep if dup == 0 (keep first occurrence, which is newest rdq)

print(f"\n=== Stata's final deduplication ===")
print("Sort by (gvkey, time_avail_m, -rdq) and keep first (newest rdq):")

final_dedup = focus_months.sort_values(['gvkey', 'time_avail_m', 'rdq'], ascending=[True, True, False])
final_dedup = final_dedup.drop_duplicates(['gvkey', 'time_avail_m'], keep='first')

print(f"After final dedup:")
for _, row in final_dedup.iterrows():
    time_avail = row['time_avail_m']
    rdq = row['rdq']
    cheq = row['cheq']
    atq = row['atq']
    cash = cheq / atq if atq != 0 else np.nan
    print(f"  {time_avail}: rdq={rdq}, Cash={cash:.6f}")

# Check if Oct 1984 is covered now
oct_1984 = pd.Timestamp('1984-10-01')
oct_data = final_dedup[final_dedup['time_avail_m'] == oct_1984]

print(f"\nOct 1984 data after final dedup:")
if len(oct_data) > 0:
    row = oct_data.iloc[0]
    print(f"  ✅ Found: rdq={row['rdq']}, Cash={row['cheq']/row['atq']:.6f}")
    if abs(row['cheq']/row['atq'] - 0.010443) < 0.000001:
        print(f"  ✅ Matches Stata value!")
else:
    print(f"  ❌ Still no Oct 1984 data")

print(f"\n=== Python's current deduplication ===")
print("Python currently does:")
python_dedup = focus_months.sort_values(['gvkey', 'time_avail_m', 'rdq'], ascending=[True, True, False])
python_dedup = python_dedup.drop_duplicates(['gvkey', 'time_avail_m'], keep='first')

print("Result is the same as Stata's approach")

print(f"\n=== The real issue ===")
print("Both approaches produce the same result - no data for Oct 1984")
print("This suggests either:")
print("1. Stata has different source data")
print("2. Stata has a different expansion mechanism")
print("3. There's a forward-fill or carryover mechanism we're missing")

# Check if Stata does forward filling after dedup
print(f"\n=== Testing forward fill hypothesis ===")
print("Maybe Stata forward-fills quarterly data across gaps?")

# Sort by time and forward fill
all_gvkey_data = expanded_df[expanded_df['gvkey'] == test_gvkey].copy()
all_gvkey_data = all_gvkey_data.sort_values(['gvkey', 'time_avail_m', 'rdq'], ascending=[True, True, False])
all_gvkey_data = all_gvkey_data.drop_duplicates(['gvkey', 'time_avail_m'], keep='first')

# Sort by time and forward fill missing months
all_gvkey_data = all_gvkey_data.sort_values('time_avail_m')
all_gvkey_data['cheq_ffill'] = all_gvkey_data['cheq'].ffill()
all_gvkey_data['atq_ffill'] = all_gvkey_data['atq'].ffill()

oct_data_ffill = all_gvkey_data[all_gvkey_data['time_avail_m'] == oct_1984]
if len(oct_data_ffill) > 0:
    print("Forward fill doesn't help - Oct 1984 still not in the data")
else:
    print("Oct 1984 would need to be added to the time series first")