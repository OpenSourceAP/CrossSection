# Stata `fastxtile` Command Translation to Python

## Overview

`fastxtile` is a high-performance replacement for Stata's built-in `xtile` command, used to create quantile categories (deciles, quintiles, etc.) from continuous variables. It's critical for portfolio formation and ranking operations in finance.

## Stata Syntax and Usage

### Basic Syntax
```stata
egen newvar = fastxtile(varname), n(#) [by(groupvars)]
```

### Common Patterns from Our Codebase

**Example 1: Simple deciles (tang.do:8)**
```stata
egen tempFC = fastxtile(at), n(10) by(time_avail_m)
```
Creates 10 quantiles of `at` within each `time_avail_m` group.

**Example 2: Creating financial constraint categories**
```stata
gen FC = 1 if tempFC <=3  // Lower three deciles
replace FC = 0 if tempFC >=8 & !mi(tempFC)  // Upper three deciles
```

## Python Translation Patterns

### Method 1: pandas.qcut() - Equal Frequency Quantiles
```python
# Stata: egen decile = fastxtile(variable), n(10)
df['decile'] = pd.qcut(df['variable'], q=10, labels=False) + 1
```

### Method 2: pandas.qcut() with Groups - Most Common Pattern
```python
# Stata: egen decile = fastxtile(variable), n(10) by(group)
df['decile'] = df.groupby('group')['variable'].transform(
    lambda x: pd.qcut(x, q=10, labels=False, duplicates='drop') + 1
)
```

### Method 3: pandas.rank() with Percentiles
```python
# More flexible approach for custom breakpoints
df['percentile_rank'] = df.groupby('group')['variable'].rank(pct=True)
df['decile'] = pd.cut(df['percentile_rank'], 
                     bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                     labels=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

## Complete Translation Example

### Stata Code (tang.do):
```stata
use permno time_avail_m che rect invt ppegt at sic using "data.dta", clear
destring sic, replace
drop if sic < 2000 | sic > 3999
egen tempFC = fastxtile(at), n(10) by(time_avail_m)
gen FC = 1 if tempFC <=3
replace FC = 0 if tempFC >=8 & !mi(tempFC)
```

### Python Translation:
```python
# Load data
df = pd.read_parquet('data.parquet')[['permno', 'time_avail_m', 'che', 'rect', 'invt', 'ppegt', 'at', 'sic']]

# Convert and filter
df['sic'] = pd.to_numeric(df['sic'], errors='coerce')
df = df[(df['sic'] >= 2000) & (df['sic'] <= 3999)]

# Create deciles by time period
df['tempFC'] = df.groupby('time_avail_m')['at'].transform(
    lambda x: pd.qcut(x, q=10, labels=False, duplicates='drop') + 1
)

# Create binary financial constraint variable
df['FC'] = np.nan
df.loc[df['tempFC'] <= 3, 'FC'] = 1
df.loc[(df['tempFC'] >= 8) & df['tempFC'].notna(), 'FC'] = 0
```

## Critical Translation Issues

### 1. **Missing Values Handling**
- **Stata**: `fastxtile` excludes missing values automatically
- **Python**: Use `duplicates='drop'` in `pd.qcut()` to handle ties and missing values

### 2. **Group-wise Operations**
- **Stata**: `by(groupvar)` creates quantiles within each group
- **Python**: **MUST** use `.groupby().transform()` to replicate exact behavior

### 3. **1-based vs 0-based Indexing**
- **Stata**: Returns quantiles 1, 2, 3, ..., n
- **Python**: `pd.qcut()` returns 0, 1, 2, ..., n-1, so add +1

### 4. **Handling Ties and Duplicates**
- **Stata**: Automatically resolves ties consistently
- **Python**: Use `duplicates='drop'` or `duplicates='raise'` to control behavior

### 5. **Infinite Values Handling** ⚠️ **CRITICAL**
- **Stata**: Automatically excludes extreme values (±inf) from quantile calculations
- **Python**: `pd.qcut()` fails silently with infinite values, producing NaN quantiles
- **Solution**: **ALWAYS** replace infinite values with NaN before quantile calculation

**Example of the infinite value issue:**
```python
# ❌ WRONG: -inf values break pd.qcut
df['BM'] = np.log(df['ceq'] / df['mve_c'])  # Can produce -inf
df['BM_quintile'] = pd.qcut(df['BM'], q=5, labels=False) + 1  # Fails with -inf

# ✅ CORRECT: Handle infinite values first
df['BM'] = np.log(df['ceq'] / df['mve_c'])
df['BM_clean'] = df['BM'].replace([np.inf, -np.inf], np.nan)
df['BM_quintile'] = pd.qcut(df['BM_clean'], q=5, labels=False, duplicates='drop') + 1
```

**Root cause discovered in AccrualsBM predictor (2025-07-16):**
- Financial ratios like `log(ceq/mve_c)` produce -inf when ceq/mve_c ≤ 0
- pd.qcut cannot handle -inf values and silently produces NaN quantiles
- This caused 9,605 missing observations until fixed with proper infinite value handling

## Validation Checklist

After translating `fastxtile`:
1. ✅ Check quantile counts match expected (e.g., 10 for deciles)
2. ✅ Verify within-group quantiles when using `by()` option
3. ✅ Ensure missing values are handled consistently
4. ✅ Confirm 1-based indexing (quantiles start at 1, not 0)
5. ✅ Test with edge cases (all equal values, many missing values)
6. ✅ **Check for infinite values** in input data (especially log-transformed ratios)
7. ✅ **Verify no NaN quantiles** caused by infinite input values

## Common Mistakes

### ❌ WRONG: Ignoring group structure
```python
df['decile'] = pd.qcut(df['variable'], q=10, labels=False) + 1  # Global quantiles
```

### ❌ WRONG: Forgetting +1 for 1-based indexing
```python
df['decile'] = pd.qcut(df['variable'], q=10, labels=False)  # Returns 0-9 instead of 1-10
```

### ❌ WRONG: Not handling infinite values
```python
df['BM'] = np.log(df['ceq'] / df['mve_c'])  # Can produce -inf
df['BM_quintile'] = pd.qcut(df['BM'], q=5, labels=False) + 1  # Fails silently with -inf
```

### ✅ CORRECT: Complete robust implementation
```python
def fastxtile(series, n_quantiles=5):
    """
    Robust fastxtile implementation with infinite value handling
    """
    try:
        # Handle infinite values first
        series_clean = series.replace([np.inf, -np.inf], np.nan)
        
        # Use pd.qcut with proper parameters
        return pd.qcut(series_clean, q=n_quantiles, labels=False, duplicates='drop') + 1
    except Exception:
        # Fallback for edge cases
        return pd.Series(np.nan, index=series.index)

# Usage with groups
df['decile'] = df.groupby('time_period')['variable'].transform(
    lambda x: fastxtile(x, 10)
)
```

## Performance Notes

- For large datasets, consider using `numpy.percentile()` for custom implementations
- `pd.qcut()` is generally fast but can be memory-intensive with many groups
- The `duplicates='drop'` option prevents errors when all values in a group are identical