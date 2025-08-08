# Test different ranking methods to match Stata's fastxtile behavior

import pandas as pd
import numpy as np

print("=== Testing Stata-like Ranking Methods ===")

focus_date = pd.to_datetime("2004-08-01")
focus_permno = 80432

# Load processed data
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'ret']].copy()
df = df.sort_values(['permno', 'time_avail_m'])
df.loc[df['ret'].isna(), 'ret'] = 0

# Process to get Mom36m
for i in range(1, 6):
    df[f'l{i}_ret'] = df.groupby('permno')['ret'].shift(i)
for i in range(13, 37):
    df[f'l{i}_ret'] = df.groupby('permno')['ret'].shift(i)

df['Mom6m'] = ((1 + df['l1_ret']) * (1 + df['l2_ret']) * (1 + df['l3_ret']) * 
               (1 + df['l4_ret']) * (1 + df['l5_ret'])) - 1

mom36m_product = 1
for i in range(13, 37):
    mom36m_product *= (1 + df[f'l{i}_ret'])
df['Mom36m'] = mom36m_product - 1

time_cohort = df[df['time_avail_m'] == focus_date].copy()
time_cohort = time_cohort[(time_cohort['Mom6m'].notna()) & (time_cohort['Mom36m'].notna())]

focus_mom36m = time_cohort[time_cohort['permno'] == focus_permno]['Mom36m'].iloc[0]
print(f"Focus Mom36m: {focus_mom36m:.8f}")

# Test different pandas ranking methods
ranking_methods = ['average', 'min', 'max', 'first', 'dense']

print(f"\n=== Testing Pandas Ranking Methods ===")

for method in ranking_methods:
    # Calculate percentile rank
    pct_rank = time_cohort['Mom36m'].rank(pct=True, method=method)
    focus_pct_rank = pct_rank[time_cohort['permno'] == focus_permno].iloc[0]
    
    # Convert to quintile (1-based)
    quintile = np.floor(focus_pct_rank * 5) + 1
    # Handle exact 100th percentile edge case
    if quintile > 5:
        quintile = 5
        
    print(f"Method '{method}': pct_rank={focus_pct_rank:.4f} → quintile={int(quintile)}")

# Test manual quintile assignment based on ranks
print(f"\n=== Manual Quintile Assignment Tests ===")

n_obs = len(time_cohort)

# Method A: Based on position in sorted array (0-indexed)
sorted_positions = time_cohort['Mom36m'].rank(method='first') - 1  # 0-indexed positions
focus_position = sorted_positions[time_cohort['permno'] == focus_permno].iloc[0]
manual_quintile_a = int(focus_position // (n_obs / 5)) + 1
if manual_quintile_a > 5:
    manual_quintile_a = 5
    
print(f"Method A (position-based): position={int(focus_position)}/{n_obs} → quintile={manual_quintile_a}")

# Method B: Based on <=20%, <=40%, etc. thresholds
mom36m_values = time_cohort['Mom36m']
p20 = np.percentile(mom36m_values, 20)
p40 = np.percentile(mom36m_values, 40)  
p60 = np.percentile(mom36m_values, 60)
p80 = np.percentile(mom36m_values, 80)

print(f"Percentile thresholds: 20%={p20:.6f}, 40%={p40:.6f}, 60%={p60:.6f}, 80%={p80:.6f}")

if focus_mom36m <= p20:
    manual_quintile_b = 1
elif focus_mom36m <= p40:
    manual_quintile_b = 2
elif focus_mom36m <= p60:
    manual_quintile_b = 3
elif focus_mom36m <= p80:
    manual_quintile_b = 4
else:
    manual_quintile_b = 5
    
print(f"Method B (percentile thresholds): {focus_mom36m:.6f} vs {p20:.6f} → quintile={manual_quintile_b}")

# Method C: Stata-like based on rank <= 20% of n
# This might be how Stata actually does it
ranks_min = time_cohort['Mom36m'].rank(method='min')
focus_rank_min = ranks_min[time_cohort['permno'] == focus_permno].iloc[0]

# Calculate thresholds based on ranks
rank_20pct = n_obs * 0.2
rank_40pct = n_obs * 0.4
rank_60pct = n_obs * 0.6
rank_80pct = n_obs * 0.8

print(f"Rank thresholds: 20%={rank_20pct:.1f}, 40%={rank_40pct:.1f}, 60%={rank_60pct:.1f}, 80%={rank_80pct:.1f}")

if focus_rank_min <= rank_20pct:
    manual_quintile_c = 1
elif focus_rank_min <= rank_40pct:
    manual_quintile_c = 2
elif focus_rank_min <= rank_60pct:
    manual_quintile_c = 3
elif focus_rank_min <= rank_80pct:
    manual_quintile_c = 4
else:
    manual_quintile_c = 5
    
print(f"Method C (rank thresholds): rank={focus_rank_min:.1f} vs {rank_20pct:.1f} → quintile={manual_quintile_c}")

# Method D: Test with different numpy percentile methods
print(f"\n=== Testing Numpy Percentile Methods ===")

for interpolation in ['linear', 'lower', 'higher', 'midpoint', 'nearest']:
    try:
        p20_interp = np.percentile(mom36m_values, 20, method=interpolation)
        quintile_d = 1 if focus_mom36m <= p20_interp else 2  # Just test first boundary
        print(f"numpy method '{interpolation}': 20th percentile={p20_interp:.8f}, focus→quintile={quintile_d}")
    except Exception as e:
        print(f"numpy method '{interpolation}': failed ({e})")

print(f"\n=== Results Summary ===")
print(f"Current Python (pd.qcut): quintile 2")
print(f"Stata expects: quintile 1")
print(f"")
print(f"Alternative methods that produce quintile 1:")

methods_results = [
    ('pd.rank average', np.floor(time_cohort['Mom36m'].rank(pct=True, method='average')[time_cohort['permno'] == focus_permno].iloc[0] * 5) + 1),
    ('pd.rank min', np.floor(time_cohort['Mom36m'].rank(pct=True, method='min')[time_cohort['permno'] == focus_permno].iloc[0] * 5) + 1),
    ('pd.rank max', np.floor(time_cohort['Mom36m'].rank(pct=True, method='max')[time_cohort['permno'] == focus_permno].iloc[0] * 5) + 1),
    ('pd.rank first', np.floor(time_cohort['Mom36m'].rank(pct=True, method='first')[time_cohort['permno'] == focus_permno].iloc[0] * 5) + 1),
    ('manual rank-based', manual_quintile_c)
]

for method_name, quintile in methods_results:
    if quintile == 1:
        print(f"  ✅ {method_name}: {int(quintile)}")
    else:
        print(f"  ❌ {method_name}: {int(quintile)}")

print(f"\nThis suggests Stata uses a rank-based method with min() tie handling")
print(f"where observations with rank ≤ 20% of n are assigned to quintile 1.")