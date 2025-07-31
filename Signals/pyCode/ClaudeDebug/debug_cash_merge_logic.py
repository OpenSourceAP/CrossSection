import pandas as pd
import numpy as np

print("=== Examining the merge logic difference ===")

# Stata does:
# merge 1:1 gvkey time_avail_m using "$pathtemp/tempCash", keepusing(atq cheq rdq) nogenerate keep(match)

# Python does:
# pd.merge(signal_master, expanded_df, on=['gvkey', 'time_avail_m'], how='inner')

# The key difference might be in what gets merged vs what's available

test_permno = 10517
test_gvkey = 1076.0
target_time = pd.Timestamp('1984-10-01')

print(f"Debugging merge for permno {test_permno}, gvkey {test_gvkey}, time {target_time}")

# Load SignalMasterTable entries for this permno around Oct 1984
signal_master = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
                               columns=['permno', 'gvkey', 'time_avail_m'])

target_entries = signal_master[
    (signal_master['permno'] == test_permno) & 
    (signal_master['time_avail_m'] >= '1984-08-01') & 
    (signal_master['time_avail_m'] <= '1984-12-01')
]

print(f"\nSignalMasterTable entries for permno {test_permno} around Oct 1984:")
if len(target_entries) > 0:
    print(target_entries[['permno', 'gvkey', 'time_avail_m']].to_string(index=False))
else:
    print("No entries found")

# Now let's see what quarterly data is available for merge
qcompustat_df = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet',
                               columns=['gvkey', 'rdq', 'cheq', 'atq'])

# Process quarterly data exactly as in Cash.py
gvkey_data = qcompustat_df[qcompustat_df['gvkey'] == test_gvkey].copy()
gvkey_data = gvkey_data.dropna(subset=['gvkey', 'atq'])
gvkey_data = gvkey_data.sort_values(['gvkey', 'rdq'])
gvkey_data = gvkey_data.drop_duplicates(['gvkey', 'rdq'], keep='first')
gvkey_data['time_avail_m'] = pd.to_datetime(gvkey_data['rdq']).dt.to_period('M').dt.to_timestamp()

# Expand
expanded_dfs = []
for month_offset in range(3):
    df_copy = gvkey_data.copy()
    df_copy['time_avail_m'] = df_copy['time_avail_m'] + pd.DateOffset(months=month_offset)
    expanded_dfs.append(df_copy)

expanded_df = pd.concat(expanded_dfs, ignore_index=True)

# Final dedup
expanded_df = expanded_df.sort_values(['gvkey', 'time_avail_m', 'rdq'], ascending=[True, True, False])
expanded_df = expanded_df.drop_duplicates(['gvkey', 'time_avail_m'], keep='first')

quarterly_entries = expanded_df[
    (expanded_df['gvkey'] == test_gvkey) & 
    (expanded_df['time_avail_m'] >= '1984-08-01') & 
    (expanded_df['time_avail_m'] <= '1984-12-01')
]

print(f"\nQuarterly data available for merge (gvkey {test_gvkey}):")
if len(quarterly_entries) > 0:
    print(quarterly_entries[['gvkey', 'time_avail_m', 'rdq', 'cheq', 'atq']].to_string(index=False))
else:
    print("No quarterly data available")

# Check what the merge produces
print(f"\n=== Merge result ===")
merge_result = pd.merge(
    target_entries, 
    quarterly_entries[['gvkey', 'time_avail_m', 'rdq', 'cheq', 'atq']], 
    on=['gvkey', 'time_avail_m'], 
    how='inner'
)

print(f"Merge result for this permno:")
if len(merge_result) > 0:
    print(merge_result[['permno', 'gvkey', 'time_avail_m', 'rdq', 'cheq', 'atq']].to_string(index=False))
    
    # Check if Oct 1984 is in the merge
    oct_result = merge_result[merge_result['time_avail_m'] == target_time]
    if len(oct_result) > 0:
        print(f"\n✅ Oct 1984 found in merge!")
    else:
        print(f"\n❌ Oct 1984 NOT in merge result")
else:
    print("No merge results")

print(f"\n=== Key insight ===")
print("The issue is that quarterly expansion doesn't cover Oct 1984")
print("SignalMasterTable wants Oct 1984, but no quarterly data expands to that month")
print("Stata somehow bridges this gap - maybe through a different mechanism")

# Let me check if there's a different pattern - maybe Stata allows gaps and uses most recent quarterly data?
print(f"\n=== Testing 'most recent quarter' hypothesis ===")
print("Maybe Stata uses the most recent quarterly data for months not covered by expansion?")

# Find the most recent quarterly data before Oct 1984
all_quarterly_before_oct = expanded_df[
    (expanded_df['gvkey'] == test_gvkey) & 
    (expanded_df['time_avail_m'] <= target_time)
].sort_values('time_avail_m')

if len(all_quarterly_before_oct) > 0:
    most_recent = all_quarterly_before_oct.iloc[-1]
    print(f"Most recent quarterly data before/at Oct 1984:")
    print(f"  time_avail_m: {most_recent['time_avail_m']}")
    print(f"  rdq: {most_recent['rdq']}")
    print(f"  Cash: {most_recent['cheq']/most_recent['atq']:.6f}")
    
    if abs(most_recent['cheq']/most_recent['atq'] - 0.010443) < 0.000001:
        print(f"  ✅ This would match Stata's value!")
        print(f"  💡 Hypothesis: Stata forward-fills across gaps in quarterly coverage")