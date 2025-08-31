# Stata `egen` Command Translation to Python

## Overview

The `egen` command (extended generate) in Stata creates variables using specialized functions that go beyond basic `gen` capabilities. It's particularly useful for statistical operations, group-wise calculations, and complex data transformations.

## Stata Syntax and Usage

### Basic Syntax
```stata
egen newvar = function(arguments) [if] [in] [, by(groupvars)]
```

### Common Functions
- **Statistical**: `mean()`, `median()`, `min()`, `max()`, `sd()`, `count()`
- **Row operations**: `rowmean()`, `rowmax()`, `rowmin()`, `rowsd()`
- **Grouping**: `group()`, `rank()`, `pctile()`, `xtile()`
- **String**: `concat()`, `ends()`, `length()`

### Common Patterns from Our Codebase

**Example 1: Group statistics**
```stata
egen industry_mean = mean(variable), by(industry time_avail_m)
```

**Example 2: Rankings and percentiles**
```stata
egen rank_var = rank(variable), by(time_avail_m)
egen pctile_var = pctile(variable), p(75) by(time_avail_m)
```

**Example 3: Row operations**
```stata
egen row_average = rowmean(var1 var2 var3 var4)
egen row_count = rownonmiss(var1 var2 var3 var4)
```

**Example 4: Group identifiers**
```stata
egen group_id = group(firm_id industry_code)
```

## Python Translation Patterns

### Method 1: Group Statistics with .transform()
```python
# Stata: egen group_mean = mean(var), by(group)
df['group_mean'] = df.groupby('group')['var'].transform('mean')
```

### Method 2: Row Operations with Pandas
```python
# Stata: egen row_mean = rowmean(var1 var2 var3)
df['row_mean'] = df[['var1', 'var2', 'var3']].mean(axis=1)
```

### Method 3: Ranking and Percentiles
```python
# Stata: egen rank_var = rank(var), by(group)
df['rank_var'] = df.groupby('group')['var'].rank()
```

### Method 4: Statistical Functions
```python
# Stata: egen var_sd = sd(var), by(group)
df['var_sd'] = df.groupby('group')['var'].transform('std')
```

## Complete Translation Examples

### Example 1: Group Statistics
**Stata:**
```stata
egen industry_mean = mean(roa), by(industry time_avail_m)
egen industry_median = median(roa), by(industry time_avail_m)
egen industry_count = count(roa), by(industry time_avail_m)
```

**Python:**
```python
# Create multiple group statistics
group_stats = df.groupby(['industry', 'time_avail_m'])['roa'].agg([
    ('industry_mean', 'mean'),
    ('industry_median', 'median'),
    ('industry_count', 'count')
]).reset_index()

# Merge back to original data
df = df.merge(group_stats, on=['industry', 'time_avail_m'], how='left')
```

### Example 2: Row Operations
**Stata:**
```stata
egen row_mean = rowmean(q1_earnings q2_earnings q3_earnings q4_earnings)
egen row_max = rowmax(q1_earnings q2_earnings q3_earnings q4_earnings)
egen row_nonmiss = rownonmiss(q1_earnings q2_earnings q3_earnings q4_earnings)
```

**Python:**
```python
quarterly_vars = ['q1_earnings', 'q2_earnings', 'q3_earnings', 'q4_earnings']

# Row mean
df['row_mean'] = df[quarterly_vars].mean(axis=1)

# Row max
df['row_max'] = df[quarterly_vars].max(axis=1)

# Row non-missing count
df['row_nonmiss'] = df[quarterly_vars].notna().sum(axis=1)
```

### Example 3: Ranking and Percentiles
**Stata:**
```stata
egen size_rank = rank(market_cap), by(time_avail_m)
egen size_pctile = pctile(market_cap), p(90) by(time_avail_m)
```

**Python:**
```python
# Ranking within groups
df['size_rank'] = df.groupby('time_avail_m')['market_cap'].rank()

# Percentiles within groups
df['size_pctile'] = df.groupby('time_avail_m')['market_cap'].transform(
    lambda x: x.quantile(0.90)
)
```

### Example 4: Group Identifiers
**Stata:**
```stata
egen group_id = group(firm_id industry_code year)
```

**Python:**
```python
# Create group identifiers
df['group_id'] = df.groupby(['firm_id', 'industry_code', 'year']).ngroup() + 1
```

## Function-Specific Translations

### Statistical Functions
| Stata Function | Python Equivalent | Notes |
|----------------|------------------|-------|
| `mean()` | `.transform('mean')` | Group mean |
| `median()` | `.transform('median')` | Group median |
| `min()` | `.transform('min')` | Group minimum |
| `max()` | `.transform('max')` | Group maximum |
| `sd()` | `.transform('std')` | Group standard deviation |
| `count()` | `.transform('count')` | Group count |

### Row Functions
| Stata Function | Python Equivalent | Notes |
|----------------|------------------|-------|
| `rowmean()` | `.mean(axis=1)` | Row mean |
| `rowmax()` | `.max(axis=1)` | Row maximum |
| `rowmin()` | `.min(axis=1)` | Row minimum |
| `rowsd()` | `.std(axis=1)` | Row standard deviation |
| `rownonmiss()` | `.notna().sum(axis=1)` | Count non-missing |

### Ranking Functions
| Stata Function | Python Equivalent | Notes |
|----------------|------------------|-------|
| `rank()` | `.rank()` | Ranking |
| `pctile()` | `.quantile()` | Percentiles |
| `xtile()` | `pd.qcut()` | Quantile categories |

## Advanced Pattern Translations

### Multiple Group Statistics
```python
# Stata: Multiple egen statements with same grouping
# egen mean_var = mean(var), by(group)
# egen sd_var = sd(var), by(group)
# egen count_var = count(var), by(group)

# Python: Efficient batch processing
group_stats = df.groupby('group')['var'].agg([
    'mean', 'std', 'count', 'median', 'min', 'max'
]).add_prefix('group_')

df = df.merge(group_stats, left_on='group', right_index=True, how='left')
```

### Conditional Group Operations
```python
# Stata: egen mean_var = mean(var) if condition, by(group)
df['mean_var'] = df[df['condition']].groupby('group')['var'].transform('mean')
```

### Custom Functions with Apply
```python
# For complex operations not covered by standard functions
def custom_group_function(group):
    # Custom logic here
    return group['var'].some_custom_operation()

df['custom_var'] = df.groupby('group').apply(custom_group_function).reset_index(level=0, drop=True)
```

## Performance Considerations

### Efficient Group Operations
```python
# ✅ EFFICIENT: Use transform for single statistics
df['group_mean'] = df.groupby('group')['var'].transform('mean')

# ✅ EFFICIENT: Use agg for multiple statistics
stats = df.groupby('group')['var'].agg(['mean', 'std', 'count'])

# ❌ LESS EFFICIENT: Multiple separate operations
df['group_mean'] = df.groupby('group')['var'].transform('mean')
df['group_std'] = df.groupby('group')['var'].transform('std')
df['group_count'] = df.groupby('group')['var'].transform('count')
```

### Memory Optimization
```python
# For large datasets, consider chunking
def process_groups_in_chunks(df, group_col, var_col, chunk_size=1000):
    unique_groups = df[group_col].unique()
    results = []
    
    for i in range(0, len(unique_groups), chunk_size):
        chunk_groups = unique_groups[i:i+chunk_size]
        chunk_df = df[df[group_col].isin(chunk_groups)]
        chunk_result = chunk_df.groupby(group_col)[var_col].transform('mean')
        results.append(chunk_result)
    
    return pd.concat(results)
```

## String Function Translations

### String Concatenation
```python
# Stata: egen concat_var = concat(var1 var2 var3)
df['concat_var'] = df[['var1', 'var2', 'var3']].astype(str).agg(''.join, axis=1)

# With separator
df['concat_var'] = df[['var1', 'var2', 'var3']].astype(str).agg('_'.join, axis=1)
```

### String Operations
```python
# Stata: egen str_length = length(string_var)
df['str_length'] = df['string_var'].str.len()

# Stata: egen first_word = word(string_var, 1)
df['first_word'] = df['string_var'].str.split().str[0]
```

## Validation Checklist

After translating `egen` commands:
1. ✅ Verify group-wise operations produce correct results
2. ✅ Check that row operations handle missing values appropriately
3. ✅ Confirm statistical functions match Stata calculations
4. ✅ Test edge cases (empty groups, all missing values)
5. ✅ Validate performance with large datasets

## Common Mistakes

### ❌ WRONG: Using apply() when transform() is sufficient
```python
df['group_mean'] = df.groupby('group').apply(lambda x: x['var'].mean())
```

### ❌ WRONG: Not handling missing values in row operations
```python
df['row_mean'] = df[['var1', 'var2', 'var3']].mean(axis=1)  # May not handle NaN like Stata
```

### ❌ WRONG: Inefficient multiple group operations
```python
df['mean1'] = df.groupby('group')['var1'].transform('mean')
df['mean2'] = df.groupby('group')['var2'].transform('mean')  # Separate operations
```

### ✅ CORRECT: Proper transform usage
```python
df['group_mean'] = df.groupby('group')['var'].transform('mean')
```

### ✅ CORRECT: Handle missing values explicitly
```python
df['row_mean'] = df[['var1', 'var2', 'var3']].mean(axis=1, skipna=True)
```

### ✅ CORRECT: Efficient batch operations
```python
group_stats = df.groupby('group')[['var1', 'var2']].agg('mean').add_prefix('mean_')
df = df.merge(group_stats, left_on='group', right_index=True, how='left')
```