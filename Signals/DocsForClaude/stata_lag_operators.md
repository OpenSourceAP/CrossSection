# Stata Lag Operators (`l.`, `l12.`) Translation to Python

## Overview

Stata's lag operators (`l.`, `l12.`, etc.) create lagged versions of variables for time series and panel data analysis. They're crucial for finance applications where you need past values for predictions and calculations.

## Stata Syntax and Usage

### Basic Syntax
```stata
l.variable      [1-period lag]
l12.variable    [12-period lag]  
L.variable      [equivalent to l.]
L12.variable    [equivalent to l12.]
```

### Prerequisites
```stata
xtset panelvar timevar    [for panel data]
tsset timevar             [for time series data]
```

### Common Patterns from Our Codebase

**Example 1: Simple lag calculation (Mom12m.do)**
```stata
gen Mom12m = ((1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)) - 1
```

**Example 2: 12-month lag (Accruals.do)**
```stata
gen Accruals = ((act - l12.act) - (che - l12.che) - ((lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP)) - dp) / ((at + l12.at)/2)
```

**Example 3: Conditional with lag comparison (BM.do)**
```stata
gen me_datadate = l6.mve_c 
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
```

**Example 4: Missing value forward fill pattern**
```stata
bys permno (time_avail_m): replace me_datadate = me_datadate[_n-1] if me_datadate == .
```

## Python Translation Patterns

### Method 1: Simple Lag with .shift()
```python
# Stata: l.variable
df['lag1_variable'] = df.groupby('panel_id')['variable'].shift(1)

# Stata: l12.variable  
df['lag12_variable'] = df.groupby('panel_id')['variable'].shift(12)
```

### Method 2: Time-based Lag (More Accurate)
```python
# Sort data first
df = df.sort_values(['panel_id', 'time_var'])

# Create time-based lag using merge
df['time_lag12'] = df['time_var'] - pd.DateOffset(months=12)
lag_data = df[['panel_id', 'time_var', 'variable']].copy()
lag_data.columns = ['panel_id', 'time_lag12', 'lag12_variable']
df = df.merge(lag_data, on=['panel_id', 'time_lag12'], how='left')
```

### Method 3: Multiple Lags at Once
```python
# Create multiple lags efficiently
lag_periods = [1, 2, 3, 6, 12]
for lag in lag_periods:
    df[f'lag{lag}_variable'] = df.groupby('panel_id')['variable'].shift(lag)
```

## Complete Translation Examples

### Example 1: Momentum Calculation
**Stata:**
```stata
xtset permno time_avail_m
gen Mom12m = ((1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)*(1+l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret)) - 1
```

**Python:**
```python
# Sort data
df = df.sort_values(['permno', 'time_avail_m'])

# Create lags
for i in range(1, 12):
    df[f'lag{i}_ret'] = df.groupby('permno')['ret'].shift(i)

# Calculate momentum
momentum_product = 1
for i in range(1, 12):
    momentum_product *= (1 + df[f'lag{i}_ret'])
df['Mom12m'] = momentum_product - 1

# Cleanup temporary variables
df = df.drop([f'lag{i}_ret' for i in range(1, 12)], axis=1)
```

### Example 2: Accruals with 12-Month Lags
**Stata:**
```stata
xtset permno time_avail_m
gen Accruals = ((act - l12.act) - (che - l12.che) - ((lct - l12.lct) - (dlc - l12.dlc) - (tempTXP - l12.tempTXP)) - dp) / ((at + l12.at)/2)
```

**Python:**
```python
# Sort data
df = df.sort_values(['permno', 'time_avail_m'])

# Create 12-month lags for all variables
lag_vars = ['act', 'che', 'lct', 'dlc', 'tempTXP', 'at']
for var in lag_vars:
    df[f'l12_{var}'] = df.groupby('permno')[var].shift(12)

# Calculate Accruals
df['Accruals'] = (
    ((df['act'] - df['l12_act']) - (df['che'] - df['l12_che']) - 
     ((df['lct'] - df['l12_lct']) - (df['dlc'] - df['l12_dlc']) - 
      (df['tempTXP'] - df['l12_tempTXP'])) - df['dp']) / 
    ((df['at'] + df['l12_at']) / 2)
)
```

### Example 3: Time-based Lag with Validation
**Stata:**
```stata
xtset permno time_avail_m  
gen me_datadate = l6.mve_c 
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
```

**Python:**
```python
# Sort data
df = df.sort_values(['permno', 'time_avail_m'])

# Method 1: Simple 6-period shift
df['l6_mve_c'] = df.groupby('permno')['mve_c'].shift(6)
df['l6_time_avail_m'] = df.groupby('permno')['time_avail_m'].shift(6)

# Initial assignment
df['me_datadate'] = df['l6_mve_c']

# Validation: Set to NaN if time periods don't match expected lag
df['l6_time_avail_m_period'] = pd.to_datetime(df['l6_time_avail_m']).dt.to_period('M')
df['datadate_period'] = pd.to_datetime(df['datadate']).dt.to_period('M')
df.loc[df['l6_time_avail_m_period'] != df['datadate_period'], 'me_datadate'] = np.nan
```

## Time-based vs Position-based Lags

### Position-based Lag (Pandas default)
```python
# Simple position-based lag (assumes regular time intervals)
df['lag1_var'] = df.groupby('panel_id')['variable'].shift(1)
```

### Time-based Lag (More Accurate)
```python
# Time-based lag accounting for irregular intervals
def create_time_lag(df, group_col, time_col, value_col, lag_periods):
    """Create time-based lag accounting for irregular intervals"""
    df = df.sort_values([group_col, time_col])
    
    # Convert to period for arithmetic
    df['time_period'] = pd.to_datetime(df[time_col]).dt.to_period('M')
    df['lag_time_period'] = df['time_period'] - lag_periods
    
    # Self-merge to get lagged values
    lag_df = df[[group_col, 'time_period', value_col]].copy()
    lag_df.columns = [group_col, 'lag_time_period', f'lag{lag_periods}_{value_col}']
    
    result = df.merge(lag_df, on=[group_col, 'lag_time_period'], how='left')
    return result.drop(['time_period', 'lag_time_period'], axis=1)

# Usage
df = create_time_lag(df, 'permno', 'time_avail_m', 'mve_c', 6)
```

## Advanced Lag Patterns

### Forward Fill Missing Lags
```python
# Stata: bys permno (time_avail_m): replace var = var[_n-1] if mi(var)
df = df.sort_values(['permno', 'time_avail_m'])
df['variable'] = df.groupby('permno')['variable'].ffill()
```

### Conditional Lag Operations
```python
# Only create lag if certain conditions are met
df['conditional_lag'] = np.where(
    df['condition'],
    df.groupby('permno')['variable'].shift(1),
    np.nan
)
```

### Multiple Panel Variables
```python
# For nested panel structure (e.g., firm-year within industry)
df['lag_var'] = df.groupby(['industry', 'firm'])['variable'].shift(1)
```

## Performance Optimization

### Efficient Multiple Lag Creation
```python
# ✅ EFFICIENT: Create all lags at once
def create_lags(group, variable, max_lag):
    result = pd.DataFrame(index=group.index)
    for lag in range(1, max_lag + 1):
        result[f'lag{lag}_{variable}'] = group[variable].shift(lag)
    return result

# Apply to each group
lag_df = df.groupby('permno').apply(
    lambda x: create_lags(x, 'ret', 12)
).reset_index(level=0, drop=True)
df = pd.concat([df, lag_df], axis=1)
```

### Memory-efficient Lag Operations
```python
# For very large datasets, create lags one at a time
for lag in range(1, 13):
    df[f'lag{lag}_ret'] = df.groupby('permno')['ret'].shift(lag)
    # Use immediately and drop if not needed permanently
    # df = df.drop(f'lag{lag}_ret', axis=1)
```

## Validation Checklist

After translating lag operators:
1. ✅ Check that lag periods match Stata exactly
2. ✅ Verify handling of missing values in lag calculations
3. ✅ Confirm group structure preserves panel integrity  
4. ✅ Test edge cases (beginning of panels, irregular time gaps)
5. ✅ Validate that time-based lags account for period arithmetic

## Common Mistakes

### ❌ WRONG: Not sorting before creating lags
```python
df['lag_var'] = df.groupby('panel')['var'].shift(1)  # Order may be wrong!
```

### ❌ WRONG: Using global shift instead of group-wise
```python
df['lag_var'] = df['var'].shift(1)  # Mixes different panels!
```

### ❌ WRONG: Not handling irregular time intervals
```python
df['lag12_var'] = df.groupby('panel')['var'].shift(12)  # May not be 12 months!
```

### ✅ CORRECT: Proper panel lag creation
```python
df = df.sort_values(['panel_id', 'time_var'])
df['lag_var'] = df.groupby('panel_id')['var'].shift(1)
```

### ✅ CORRECT: Time-based lag for irregular intervals
```python
# Use time-based merge approach for precise time lags
df['time_lag'] = pd.to_datetime(df['time_var']) - pd.DateOffset(months=12)
lag_data = df[['panel_id', 'time_var', 'var']].rename(
    columns={'time_var': 'time_lag', 'var': 'lag12_var'}
)
df = df.merge(lag_data, on=['panel_id', 'time_lag'], how='left')
```