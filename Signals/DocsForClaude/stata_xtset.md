# Stata xtset and Lag Operators in Pandas

## Stata Behavior

### xtset Command
```stata
xtset permno time_avail_m
```
- Declares data as panel data with `permno` as panel identifier and `time_avail_m` as time variable
- Enables time-series operators to work within each panel
- Requires both variables to be numeric integers

### Lag Operators (L6)
```stata
gen me_datadate = l6.mve_c
```
- `l6.` looks for the **exact** period that is 6 units back in time
- **No gap filling**: If period t-6 doesn't exist, returns missing (.)
- **Does NOT** use nearest available data (e.g., t-7 if t-6 is missing)

## Example of Missing Data Behavior

```
time_avail_m:  100  101  102  104  105  106  107
               (missing period 103)

For period 107:
- l6. looks for 101 (107-6) ✓ EXISTS → returns value
  
For period 106:  
- l6. looks for 100 (106-6) ✓ EXISTS → returns value

For period 105:
- l6. looks for 99 (105-6) ✗ MISSING → returns NaN

For period 104:
- l6. looks for 98 (104-6) ✗ MISSING → returns NaN
```

## Pandas Equivalent

### Setup Panel Data
```python
# Equivalent to xtset permno time_avail_m
df = df.set_index(['permno', 'time_avail_m']).sort_index()
# OR
df = df.sort_values(['permno', 'time_avail_m'])
```

### Lag Operations with Exact Period Matching

#### Method 1: Using groupby + shift (Approximate)
```python
# WARNING: This doesn't handle gaps correctly
df['me_datadate'] = df.groupby('permno')['mve_c'].shift(6)
```

#### Method 2: Exact Stata Replication (Recommended)
```python
def stata_lag(df, var, lag_periods, panel_var='permno', time_var='time_avail_m'):
    """
    Replicate Stata's exact lag behavior with gap handling
    """
    result = pd.Series(index=df.index, dtype=float)
    
    for panel_id in df[panel_var].unique():
        panel_data = df[df[panel_var] == panel_id].copy()
        
        for idx, row in panel_data.iterrows():
            current_time = row[time_var]
            target_time = current_time - lag_periods
            
            # Look for exact time match
            target_row = panel_data[panel_data[time_var] == target_time]
            
            if len(target_row) == 1:
                result.loc[idx] = target_row[var].iloc[0]
            else:
                result.loc[idx] = np.nan
    
    return result

# Usage
df['me_datadate'] = stata_lag(df, 'mve_c', 6)
```

#### Method 3: Using merge (Most Efficient)
```python
# Create lagged time variable
df['time_lag6'] = df['time_avail_m'] - 6

# Self-merge to get lagged values
lagged = df[['permno', 'time_avail_m', 'mve_c']].copy()
lagged.columns = ['permno', 'time_lag6', 'me_datadate']

df = df.merge(lagged, on=['permno', 'time_lag6'], how='left')
df = df.drop('time_lag6', axis=1)
```

## Complete Stata Code Translation

```stata
xtset permno time_avail_m
gen me_datadate = l6.mve_c 
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
bys permno (time_avail_m): replace me_datadate = me_datadate[_n-1] if me_datadate == .
```

```python
# Step 1: Setup (equivalent to xtset)
df = df.sort_values(['permno', 'time_avail_m'])

# Step 2: Create lag (equivalent to gen me_datadate = l6.mve_c)
df['time_lag6'] = df['time_avail_m'] - 6
lagged = df[['permno', 'time_avail_m', 'mve_c']].copy()
lagged.columns = ['permno', 'time_lag6', 'me_datadate']
df = df.merge(lagged, on=['permno', 'time_lag6'], how='left')

# Also get lagged time for validation
lagged_time = df[['permno', 'time_avail_m']].copy()
lagged_time.columns = ['permno', 'time_lag6']
lagged_time['l6_time_avail_m'] = lagged_time['time_lag6']
df = df.merge(lagged_time, on=['permno', 'time_lag6'], how='left')

# Step 3: Validation (equivalent to replace me_datadate = . if l6.time_avail_m != mofd(datadate))
# Assuming datadate is already in monthly format
df.loc[df['l6_time_avail_m'] != df['datadate_monthly'], 'me_datadate'] = np.nan

# Step 4: Forward fill (equivalent to bys permno (time_avail_m): replace me_datadate = me_datadate[_n-1])
df['me_datadate'] = df.groupby('permno')['me_datadate'].fillna(method='ffill')

# Cleanup
df = df.drop(['time_lag6', 'l6_time_avail_m'], axis=1)
```

## Key Differences to Remember

1. **Stata lag operators require exact period matches** - pandas `shift()` doesn't
2. **Missing periods break the lag chain** - use merge-based approach for exact replication
3. **Forward fill in Stata respects group boundaries** - use `groupby().fillna(method='ffill')`
4. **Stata missing comparisons have special behavior** - be explicit with `pd.isna()` checks