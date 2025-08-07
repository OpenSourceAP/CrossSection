# Stata `collapse` Command Translation to Python

## Overview

The `collapse` command in Stata aggregates datasets by computing summary statistics within groups. It reduces the number of observations while preserving essential information in summarized form.

## Stata Syntax and Usage

### Basic Syntax
```stata
collapse (stat) varlist [if] [in], by(groupvars) [options]
```

### Available Statistics
- `mean`: Mean (default if no stat specified)
- `sum`: Sum
- `median`: Median
- `min`: Minimum
- `max`: Maximum
- `count`: Count of non-missing observations
- `sd`: Standard deviation
- `p25`, `p50`, `p75`: Percentiles

### Common Patterns

**Example 1: Simple mean by group**
```stata
collapse (mean) sales revenue, by(year)
```

**Example 2: Multiple statistics**
```stata
collapse (mean) avg_sales=sales (sum) total_revenue=revenue (count) n_obs=sales, by(region year)
```

**Example 3: Percentiles**
```stata
collapse (p25) p25_return=returns (p50) median_return=returns (p75) p75_return=returns, by(industry)
```

**Example 4: Financial data aggregation**
```stata
collapse (mean) avg_return=returns (sd) vol_return=returns (count) n_firms=returns, by(year industry)
```

## Python Translation Patterns

### Method 1: Simple Aggregation with .groupby()
```python
# Stata: collapse (mean) var, by(group)
df_collapsed = df.groupby('group')['var'].mean().reset_index()
```

### Method 2: Multiple Statistics with .agg()
```python
# Stata: collapse (mean) var1 (sum) var2, by(group)
df_collapsed = df.groupby('group').agg({
    'var1': 'mean',
    'var2': 'sum'
}).reset_index()
```

### Method 3: Named Aggregations
```python
# Stata: collapse (mean) avg_sales=sales (count) n_obs=sales, by(group)
df_collapsed = df.groupby('group').agg(
    avg_sales=('sales', 'mean'),
    n_obs=('sales', 'count')
).reset_index()
```

### Method 4: Multiple Groups and Statistics
```python
# Stata: collapse (mean) var1 (sum) var2, by(group1 group2)
df_collapsed = df.groupby(['group1', 'group2']).agg({
    'var1': 'mean',
    'var2': 'sum'
}).reset_index()
```

## Complete Translation Examples

### Example 1: Simple Mean by Group
**Stata:**
```stata
collapse (mean) sales revenue, by(year)
```

**Python:**
```python
# Method 1: Multiple columns with same statistic
df_collapsed = df.groupby('year')[['sales', 'revenue']].mean().reset_index()

# Method 2: Using agg for clarity
df_collapsed = df.groupby('year').agg({
    'sales': 'mean',
    'revenue': 'mean'
}).reset_index()
```

### Example 2: Multiple Statistics with Custom Names
**Stata:**
```stata
collapse (mean) avg_sales=sales (sum) total_revenue=revenue (count) n_obs=sales, by(region year)
```

**Python:**
```python
# Using named aggregations (pandas >= 0.25)
df_collapsed = df.groupby(['region', 'year']).agg(
    avg_sales=('sales', 'mean'),
    total_revenue=('revenue', 'sum'),
    n_obs=('sales', 'count')
).reset_index()

# Alternative for older pandas versions
df_collapsed = df.groupby(['region', 'year']).agg({
    'sales': 'mean',
    'revenue': 'sum',
    'sales_count': 'count'
}).reset_index()
df_collapsed.columns = ['region', 'year', 'avg_sales', 'total_revenue', 'n_obs']
```

### Example 3: Percentiles and Quantiles
**Stata:**
```stata
collapse (p25) p25_return=returns (p50) median_return=returns (p75) p75_return=returns, by(industry)
```

**Python:**
```python
# Method 1: Using quantile function
df_collapsed = df.groupby('industry').agg(
    p25_return=('returns', lambda x: x.quantile(0.25)),
    median_return=('returns', 'median'),
    p75_return=('returns', lambda x: x.quantile(0.75))
).reset_index()

# Method 2: Using multiple quantiles at once
percentiles = df.groupby('industry')['returns'].quantile([0.25, 0.5, 0.75]).unstack()
percentiles.columns = ['p25_return', 'median_return', 'p75_return']
df_collapsed = percentiles.reset_index()
```

### Example 4: Financial Data Aggregation
**Stata:**
```stata
collapse (mean) avg_return=returns (sd) vol_return=returns (count) n_firms=returns, by(year industry)
```

**Python:**
```python
# Comprehensive financial aggregation
df_collapsed = df.groupby(['year', 'industry']).agg(
    avg_return=('returns', 'mean'),
    vol_return=('returns', 'std'),
    n_firms=('returns', 'count'),
    min_return=('returns', 'min'),
    max_return=('returns', 'max')
).reset_index()
```

## Advanced Aggregation Patterns

### Custom Aggregation Functions
```python
# Stata: collapse (mean) var if condition, by(group)
def conditional_mean(series, condition_series):
    """Calculate mean only where condition is true"""
    return series[condition_series].mean()

df_collapsed = df.groupby('group').apply(
    lambda x: conditional_mean(x['var'], x['condition'])
).reset_index(name='conditional_mean')
```

### Complex Statistical Functions
```python
# Advanced statistics not directly available in Stata collapse
def advanced_stats(group):
    """Calculate advanced statistics"""
    return pd.Series({
        'mean': group['var'].mean(),
        'std': group['var'].std(),
        'skew': group['var'].skew(),
        'kurtosis': group['var'].kurtosis(),
        'iqr': group['var'].quantile(0.75) - group['var'].quantile(0.25)
    })

df_collapsed = df.groupby('group').apply(advanced_stats).reset_index()
```

### Weighted Aggregations
```python
# Stata doesn't have direct weighted collapse, but Python can handle it
def weighted_mean(values, weights):
    """Calculate weighted mean"""
    return (values * weights).sum() / weights.sum()

df_collapsed = df.groupby('group').apply(
    lambda x: weighted_mean(x['var'], x['weight'])
).reset_index(name='weighted_mean')
```

## Handling Missing Values

### Casewise Deletion (cw option equivalent)
```python
# Stata: collapse (mean) var1 var2, by(group) cw
# Remove rows with missing values in key variables before aggregation
df_clean = df.dropna(subset=['var1', 'var2'])
df_collapsed = df_clean.groupby('group')[['var1', 'var2']].mean().reset_index()
```

### Missing Value Handling in Aggregation
```python
# Different approaches to handle missing values
df_collapsed = df.groupby('group').agg({
    'var1': 'mean',           # Ignores NaN (pandas default)
    'var2': lambda x: x.mean(skipna=False),  # Returns NaN if any NaN
    'var3': 'count'           # Count non-missing values
}).reset_index()
```

## Performance Optimization

### Efficient Multiple Aggregations
```python
# ✅ EFFICIENT: Single groupby with multiple functions
df_collapsed = df.groupby('group').agg({
    'var1': ['mean', 'std', 'count'],
    'var2': ['sum', 'min', 'max']
}).reset_index()

# Flatten column names
df_collapsed.columns = ['group', 'var1_mean', 'var1_std', 'var1_count', 
                       'var2_sum', 'var2_min', 'var2_max']
```

### Large Dataset Aggregation
```python
# For very large datasets, consider chunking
def chunked_collapse(df, group_cols, agg_dict, chunk_size=10000):
    """Aggregate large dataset in chunks"""
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk_agg = chunk.groupby(group_cols).agg(agg_dict)
        chunks.append(chunk_agg)
    
    # Combine and re-aggregate
    combined = pd.concat(chunks).reset_index()
    final_agg = combined.groupby(group_cols).agg(agg_dict).reset_index()
    return final_agg
```

## Comprehensive Collapse Function

```python
def stata_collapse(df, stats_dict, by_vars, if_condition=None, cw=False):
    """
    Replicate Stata collapse functionality
    
    Parameters:
    - df: DataFrame
    - stats_dict: Dictionary with {new_var: (old_var, stat)} format
    - by_vars: List of grouping variables
    - if_condition: Boolean series for filtering
    - cw: Whether to use casewise deletion
    
    Example:
    stata_collapse(df, {
        'avg_sales': ('sales', 'mean'),
        'total_revenue': ('revenue', 'sum'),
        'n_obs': ('sales', 'count')
    }, ['year', 'region'])
    """
    # Apply if condition
    if if_condition is not None:
        df = df[if_condition]
    
    # Apply casewise deletion if requested
    if cw:
        vars_to_check = list(set([var for var, stat in stats_dict.values()]))
        df = df.dropna(subset=vars_to_check)
    
    # Build aggregation dictionary
    agg_dict = {}
    for new_var, (old_var, stat) in stats_dict.items():
        if old_var not in agg_dict:
            agg_dict[old_var] = []
        agg_dict[old_var].append(stat)
    
    # Perform aggregation
    result = df.groupby(by_vars).agg(agg_dict).reset_index()
    
    # Flatten column names and rename
    if len(result.columns.levels) > 1:  # MultiIndex columns
        new_columns = by_vars.copy()
        for old_var in agg_dict.keys():
            for stat in agg_dict[old_var]:
                # Find corresponding new variable name
                new_var = next(k for k, v in stats_dict.items() if v == (old_var, stat))
                new_columns.append(new_var)
        result.columns = new_columns
    else:
        # Simple case - rename columns
        column_mapping = {by_vars[i]: by_vars[i] for i in range(len(by_vars))}
        for new_var, (old_var, stat) in stats_dict.items():
            column_mapping[old_var] = new_var
        result = result.rename(columns=column_mapping)
    
    return result

# Usage examples
df_collapsed = stata_collapse(df, {
    'avg_sales': ('sales', 'mean'),
    'total_revenue': ('revenue', 'sum'),
    'n_firms': ('firm_id', 'count')
}, ['year', 'industry'])
```

## Validation Checklist

After translating `collapse` commands:
1. ✅ Check that group variables are preserved correctly
2. ✅ Verify statistics calculations match Stata exactly
3. ✅ Confirm missing value handling behaves as expected
4. ✅ Test with edge cases (empty groups, all missing values)
5. ✅ Validate column names and data types

## Common Mistakes

### ❌ WRONG: Forgetting to reset index
```python
df_collapsed = df.groupby('group')['var'].mean()  # MultiIndex result
```

### ❌ WRONG: Incorrect column naming after aggregation
```python
df_collapsed = df.groupby('group').agg({'var': ['mean', 'sum']})  # MultiIndex columns
```

### ❌ WRONG: Not handling missing values consistently
```python
# May not match Stata's missing value handling
df_collapsed = df.groupby('group')['var'].mean()
```

### ✅ CORRECT: Proper aggregation with clear naming
```python
df_collapsed = df.groupby('group').agg(
    avg_var=('var', 'mean'),
    sum_var=('var', 'sum')
).reset_index()
```

### ✅ CORRECT: Handling missing values explicitly
```python
# Explicit missing value handling
df_collapsed = df.groupby('group')['var'].agg(['mean', 'count']).reset_index()
df_collapsed.columns = ['group', 'avg_var', 'n_obs']
```