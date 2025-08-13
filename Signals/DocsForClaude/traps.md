# Stata to Python Translation Traps

## Overview

These are the most dangerous "traps" when translating Stata code to Python - subtle behavioral differences that can cause data loss, incorrect calculations, or unexpected filtering without obvious error messages. Each trap represents a fundamental difference in how Stata and Python handle core operations.

**Why these are "traps":** They work silently in ways you don't expect, often producing plausible-looking results that are actually wrong. Unlike syntax errors that fail immediately, these bugs can persist undetected through entire analysis pipelines.

---

## Trap #1: Stata's Inequality Operators with Missing Values

### The Surprising Truth

**Stata treats missing values as positive infinity in all comparisons.** This violates the IEEE 754 standard and is opposite to most programming languages.

**Stata's missing value ordering:**
```
numbers < . < .a < .b < .c < ... < .z
```

This means:
- `.` (standard missing) = positive infinity
- `.a, .b, .c, ..., .z` (extended missing) = even larger infinities

### The Shocking Examples

**Example 1: Accidental data loss**
```stata
* Stata code
drop if price > 1000
```
This drops ALL observations where `price` is missing, even though you only wanted to drop expensive items!

**Example 2: Unexpected filtering**
```stata
* Stata code  
keep if revenue > 50000
```
This keeps ALL missing revenue observations, treating them as if they had infinite revenue.

**Example 3: Boolean variable creation**
```stata
* Stata code
gen high_sales = (sales > 100000)
```
Creates `high_sales = 1` for ALL missing sales values!

### Why Stata Does This

From Stata's FAQ: *"Once this fact is absorbed, everything is consistent, drop and keep statements work as one would expect, and the logical comparisons make sense."*

Stata chose deterministic two-valued logic (true/false) over three-valued logic (true/false/missing) for simplicity, even though it violates IEEE 754 standards.

### Safe Translation Patterns

**❌ DANGEROUS Python Translation (mimics Stata's unexpected behavior):**
```python
# This accidentally keeps missing values
df = df[df['price'] > 1000]  # Missing values become False, opposite of Stata!
```

**✅ CORRECT Python Translation (explicit missing handling):**
Use the `stata_ineq` module to translate Stata's inequality operators to Python.
```python
from utils.stata_ineq import stata_ineq_pd, stata_ineq_pl

# For pandas Series
result = stata_ineq_pd(pd_series, ">", value)

# For polars expressions
df.with_columns([
    stata_ineq_pl(pl.col("x"), ">", pl.col("y")).alias("x_gt_y")
])
```

### Stata's Safe Practices (for reference)

Experienced Stata users write defensive code:
```stata
* Safe Stata patterns
drop if price > 1000 & price < .        // Explicitly exclude missing
keep if revenue > 50000 & !mi(revenue)  // Use !mi() function
gen high_sales = (sales > 100000) if !mi(sales)  // Conditional assignment
```

---

## Trap #2: Missing Value Propagation and Handling

### The Core Differences

| Aspect | Stata | Python (pandas) |
|--------|-------|-----------------|
| Missing representation | `.`, `.a`-`.z` | `np.nan`, `pd.NA` |
| Arithmetic with missing | Often missing result | Propagates `NaN` |
| Comparisons with missing | Missing = positive infinity | `NaN` comparisons = `False` |
| Boolean context | Can be true/false | `NaN` is falsy |

### Dangerous Examples

**Example 1: Conditional replacement**
```stata
* Stata code
replace sales = 0 if mi(sales)
```

```python
# ❌ WRONG: Condition never matches
df.loc[df['sales'] == np.nan, 'sales'] = 0  # NaN != NaN!

# ✅ CORRECT: Use proper missing check
df.loc[df['sales'].isna(), 'sales'] = 0
# OR: df['sales'] = df['sales'].fillna(0)
```

**Example 2: Forward fill patterns**
```stata
* Stata code  
bys permno (time): replace var = var[_n-1] if mi(var)
```

```python
# ✅ CORRECT: Pandas handles this naturally
df['var'] = df.groupby('permno')['var'].ffill()

# ✅ ALTERNATIVE: More explicit control
mask = df['var'].isna()
df.loc[mask, 'var'] = df.groupby('permno')['var'].ffill()[mask]
```

**Example 3: Multiple variable missing logic**
```stata
* Stata code: Drop if ANY variable is missing
drop if mi(var1) | mi(var2) | mi(var3)
```

```python
# ✅ CORRECT: Multiple approaches
# Method 1: Using all()
df = df[df[['var1', 'var2', 'var3']].notna().all(axis=1)]

# Method 2: Using dropna()
df = df.dropna(subset=['var1', 'var2', 'var3'])

# Method 3: Explicit condition
condition = df['var1'].notna() & df['var2'].notna() & df['var3'].notna()
df = df[condition]
```

### Key Missing Value Functions

| Stata Function | Python Equivalent | Notes |
|----------------|------------------|-------|
| `mi(var)` | `df['var'].isna()` | Check if missing |
| `!mi(var)` | `df['var'].notna()` | Check if not missing |
| `mi(v1,v2,v3)` | `df[['v1','v2','v3']].isna().any(axis=1)` | Any variable missing |
| `replace var = .` | `df.loc[condition, 'var'] = np.nan` | Set to missing |

### Validation Patterns

```python
# Check for unexpected missing propagation
original_count = len(df)
df_processed = df[condition]
missing_count = original_count - len(df_processed)
print(f"Dropped {missing_count} observations")

# Validate missing handling matches Stata
stata_missing_logic = df['var'].isna() | (df['var'] > threshold)  # Stata-like
python_missing_logic = (df['var'] > threshold) & df['var'].notna()  # Safe Python
```

---

## Trap #3: Lag Operators - Position vs Time Based

### The Hidden Assumption

**Stata's lag operators are time-aware and calendar-based.**  
**Pandas `.shift()` is position-based and assumes regular intervals.**

This difference causes major issues with irregular time series data.

### When Position-Based Lags Break

**Example: Irregular monthly data**
```
permno  time_avail_m    ret
123     2020-01        0.05
123     2020-03        0.02  # Missing February!  
123     2020-04       -0.01
```

```stata
* Stata code: l.ret gets January's return for March row
gen lag1_ret = l.ret
```

```python
# ❌ WRONG: Gets February's return (which doesn't exist)
df['lag1_ret'] = df.groupby('permno')['ret'].shift(1)

# ✅ CORRECT: Time-based lag
df['time_lag1'] = pd.to_datetime(df['time_avail_m']) - pd.DateOffset(months=1)
lag_data = df[['permno', 'time_avail_m', 'ret']].copy()
lag_data.columns = ['permno', 'time_lag1', 'lag1_ret']
df = df.merge(lag_data, on=['permno', 'time_lag1'], how='left')
```

### Critical Example: 6-Month Market Equity Lag

This pattern from BM.do illustrates the time-based validation requirement:

```stata
* Stata code
xtset permno time_avail_m
gen me_datadate = l6.mve_c 
replace me_datadate = . if l6.time_avail_m != mofd(datadate)
```

The validation `l6.time_avail_m != mofd(datadate)` ensures the lag is exactly 6 calendar months, not 6 positions.

```python
# ✅ CORRECT: Replicating Stata's time-based validation
df = df.sort_values(['permno', 'time_avail_m'])

# Position-based lag (insufficient)
df['l6_mve_c'] = df.groupby('permno')['mve_c'].shift(6)
df['l6_time_avail_m'] = df.groupby('permno')['time_avail_m'].shift(6)

# Apply Stata's validation
df['me_datadate'] = df['l6_mve_c']
df['l6_time_period'] = pd.to_datetime(df['l6_time_avail_m']).dt.to_period('M')
df['datadate_period'] = pd.to_datetime(df['datadate']).dt.to_period('M')
condition = df['l6_time_period'] != df['datadate_period']
df.loc[condition, 'me_datadate'] = np.nan
```

### Advanced Lag Patterns

**12-month momentum calculation (Mom12m.do):**
```stata
* Stata code: Each lag is exactly 1 calendar month back
gen Mom12m = ((1+l.ret)*(1+l2.ret)*...*(1+l11.ret)) - 1
```

```python
# ✅ CORRECT: Time-based lags for irregular data
def create_time_lag(df, lag_months):
    df_lag = df.copy()
    df_lag['time_avail_m'] = (
        pd.to_datetime(df_lag['time_avail_m']) + 
        pd.DateOffset(months=lag_months)
    )
    return df_lag[['permno', 'time_avail_m', 'ret']].rename(
        columns={'ret': f'lag{lag_months}_ret'}
    )

# Create all lags and merge
for lag in range(1, 12):
    lag_df = create_time_lag(df, lag)
    df = df.merge(lag_df, on=['permno', 'time_avail_m'], how='left')

# Calculate momentum
momentum_vars = [f'lag{i}_ret' for i in range(1, 12)]
df['Mom12m'] = df[momentum_vars].apply(
    lambda row: np.prod([1 + x for x in row if pd.notna(x)]) - 1, axis=1
)
```

### Position vs Time-Based Lag Summary

| Scenario | Position-Based Lag | Time-Based Lag | When to Use |
|----------|-------------------|----------------|-------------|
| Regular monthly data | ✅ Works | ✅ Works | Either (position faster) |
| Irregular monthly data | ❌ Wrong results | ✅ Correct | Always use time-based |
| Daily data with gaps | ❌ Wrong results | ✅ Correct | Always use time-based |
| Quarterly data | ❌ Risky | ✅ Safer | Prefer time-based |

---

## Quick Reference Table

| Trap | Stata Behavior | Python Default | Correct Python Pattern |
|------|---------------|----------------|------------------------|
| `x > 1000` with missing x | `TRUE` | `FALSE` | `(x > 1000) & x.notna()` |
| `mi(x)` | Check missing | No equivalent | `x.isna()` |
| `l.ret` | Calendar-based lag | Position-based | Time-based merge |
| `drop if x > y` | Drops missing x | Keeps missing x | Explicit missing handling |
| Boolean with missing | Can be true | Always false | `np.where()` with explicit logic |

---

## Validation Checklist

After every Stata-to-Python translation:

### 1. Missing Value Validation
- [ ] Check observation counts match between Stata and Python outputs  
- [ ] Verify missing values aren't accidentally dropped in comparisons
- [ ] Test edge cases with all-missing and no-missing data
- [ ] Validate boolean variable creation with missing inputs

### 2. Inequality Validation  
- [ ] Ensure filtering logic explicitly handles missing values
- [ ] Test comparison operators with mixed missing/non-missing data
- [ ] Verify conditional assignments match Stata's missing-as-infinity logic

### 3. Lag Operator Validation
- [ ] Compare lag results on irregular time series data
- [ ] Verify time-based vs position-based lag differences  
- [ ] Test panel data with different observation frequencies
- [ ] Validate group-wise operations preserve time relationships

### 4. Integration Testing
- [ ] Run full pipeline on subset with known missing patterns
- [ ] Compare final output shapes and summary statistics
- [ ] Test extreme cases (all missing, no missing, mixed patterns)

---

## Related Documentation

- `stata_mi.md` - Comprehensive missing value function translations
- `stata_lag_operators.md` - Detailed lag operator patterns and examples  
- `debugging-philosophy.md` - General debugging strategies for translation issues

---

## Performance Notes

**Missing value operations:**
- Use vectorized `.isna()` operations rather than element-wise checks
- `fillna()` is more efficient than conditional assignment for simple replacements

**Lag operations:**  
- Position-based lags are much faster than time-based merges
- Use position-based when data is guaranteed regular
- Consider caching time-based lag results for repeated operations

**Memory considerations:**
- Time-based lags require temporary DataFrames for merging
- Clean up intermediate lag variables when not needed permanently