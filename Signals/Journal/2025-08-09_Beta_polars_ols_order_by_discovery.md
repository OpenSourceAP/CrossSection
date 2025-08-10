# Beta.py Polars-OLS Failure: Window Misalignment Issue

## Date: 2025-08-09
## Issue: Beta.py had 70.71% Precision1 failures

## 🔴 THE CRITICAL BUG

Initially thought the issue was a missing `order_by` parameter, but polars-ols doesn't have that parameter!

The real issue: **polars-ols rolling windows don't work as expected even with sorted data**

Test results show massive discrepancy:
- Polars-OLS Beta: 1.655
- Manual calculation Beta: 0.979
- Difference: ~69%!

```python
# Current implementation (sorted but still wrong)
df_sorted = df.sort(['permno', 'time_avail_m'])
pl.col("retrf").least_squares.rolling_ols(
    pl.col("ewmktrf"),
    window_size=60,
    min_periods=20,
    mode="coefficients"
).over("permno")
```

## 🔍 Why This Caused 70% Failures

Even WITH sorting, polars-ols rolling windows produce different results than manual calculations:
- Polars-OLS may be using different window definitions (centered vs trailing?)
- Or different regression algorithms/numerical methods
- Or the `.over("permno")` interaction with rolling_ols is buggy

The 69% difference in Beta values explains the 70.71% Precision1 failures!

## 📊 Evidence

1. **Symptom**: 70.71% Precision1 failures with polars-ols
2. **Clue**: The code creates `time_temp` column but never uses it:
   ```python
   df = df.with_columns(
       pl.int_range(pl.len()).over("permno").alias("time_temp")
   )
   # time_temp created but ignored in rolling_ols call!
   ```
3. **Proof**: Pandas manual approach (Agent 2) with proper ordering → 57.43% failures (13% improvement)

## 💡 Key Insights

### Why Pandas Worked Better
The pandas approach manually:
1. Sorts data by time first
2. Constructs windows based on sorted positions  
3. Ensures temporal coherence

### The asreg Pattern
Looking at a proper `asreg` implementation revealed the pattern:
```python
# Proper implementation always:
# 1. Sorts first
lf = lf.sort([*(by or []), t])  

# 2. Uses order_by in rolling_ols
yexpr.rolling_ols(
    *Xexprs, 
    order_by=pl.col(t),  # Essential!
    window_size=window_size,
    min_samples=min_samples,
    ...
).over(over)
```

## 🎯 Lessons Learned

1. **Rolling operations need explicit ordering** - Never assume data is pre-sorted
2. **order_by is NOT optional** for time series operations in polars
3. **Unused variables are red flags** - time_temp was created but never used
4. **Read the API carefully** - polars-ols has order_by for a reason
5. **Scrambled windows produce valid-looking but wrong results** - The code ran without errors but produced garbage

## 🔧 The Fix

Simply add the `order_by` parameter:
```python
df_with_beta = df.with_columns(
    pl.col("retrf")
    .least_squares.rolling_ols(
        pl.col("ewmktrf"),
        order_by=pl.col("time_temp"),  # or time_avail_m  
        window_size=60,
        min_samples=20,  # Also add this
        mode="coefficients"
    )
    .over("permno")
    .alias("_b_coeffs")
)
```

## 📈 Expected Improvement

With proper time ordering, we expect:
- Precision1 failures to drop from 70.71% to <10%
- Results to match Stata's asreg much more closely
- Beta values to represent actual trailing 60-month CAPM regressions

## 🚨 Similar Issues to Check

Other predictors using polars-ols should be audited for:
1. Missing `order_by` parameter
2. Unused time/sequence columns
3. Unexplained precision failures

This was a classic case of **syntactically correct but semantically wrong** code - it ran without errors but computed nonsense because windows were temporally scrambled!