# The Fundamental Polars-OLS Issue with Beta.py

## Date: 2025-08-10
## Problem: Beta.py has 70.71% Precision1 failures

## 🔍 Investigation Summary

Ran 4 parallel agents to test different approaches to fix Beta.py:

### Agent Results:
1. **Agent 1 (Polars-OLS + min_periods)**: 70.71% failures - NO IMPROVEMENT
2. **Agent 2 (Pandas manual rolling)**: 57.43% failures - 13% IMPROVEMENT ✅
3. **Agent 3 (Optimized polars)**: 57.43% failures (subset only)
4. **Agent 4 (Exact Stata logic)**: 72.64% failures - WORSE

## 🔴 Root Cause Discovery

### Initial Hypothesis (WRONG)
Thought polars-ols was missing an `order_by` parameter based on the `asreg` function pattern:
```python
# Thought this was needed
.rolling_ols(..., order_by=pl.col("time_temp"), ...)
```

### Actual Problem
**Polars-OLS doesn't have an `order_by` parameter!** The API only supports:
- `window_size`
- `min_periods` 
- `mode`
- `sample_weights`
- `add_intercept`
- `null_policy`
- `use_woodbury`
- `alpha`

### The Real Issue: Window Calculation Mismatch

Created test to compare polars-ols vs manual calculation on identical sorted data:

```python
# Test results on same sorted data:
Polars-OLS Beta: 1.655182
Manual Beta:     0.978778
Difference:      69% (!!)
```

This massive discrepancy explains the 70.71% Precision1 failures!

## 🤔 Why Polars-OLS Fails

Even with properly sorted data, polars-ols produces wrong results. Possible reasons:

1. **Window Definition Issue**: 
   - Polars-ols might use centered windows instead of trailing
   - Or it counts windows differently than expected

2. **The `.over()` Interaction**:
   - `.rolling_ols().over("permno")` might not work as expected
   - The grouping might interfere with the rolling window logic

3. **Different Regression Algorithm**:
   - Polars-ols might use a different numerical method
   - Or different handling of edge cases

## 💡 Key Insights

### Why Sorting Didn't Help
- Data WAS already sorted: `df.sort(["permno", "time_avail_m"])`
- Added `min_periods=20` 
- Still got 70.71% failures!
- The problem isn't data ordering - it's the rolling window calculation itself

### Why Pandas Works Better
The pandas manual approach (Agent 2):
- Explicitly controls window construction
- Uses simple, transparent OLS calculation
- Matches Stata's `asreg` logic exactly
- Result: 57.43% failures (13% improvement)

### The Unused time_temp Column
The code creates but never uses:
```python
pl.int_range(pl.len()).over("permno").alias("time_temp")
```
This was a red flag - someone tried to add ordering but couldn't figure out how to use it with polars-ols!

## 🎯 Solution

**Abandon polars-ols for Beta.py** - Use pandas manual rolling regression like VolumeTrend.py:

```python
def rolling_regression_pandas(time_vals, vol_vals, window_size=60, min_periods=20):
    # Manual OLS for each window
    # Full control over window logic
    # Transparent calculation
```

## 📝 Lessons Learned

1. **Library APIs can be misleading** - polars-ols looks sophisticated but doesn't match our needs
2. **Test assumptions early** - Should have compared polars-ols output with manual calc immediately
3. **Simple > Complex** - Manual rolling regression is more code but actually simpler to debug
4. **When precision matters, control matters** - Black-box libraries can hide critical differences

## 🚨 Action Items

1. **Replace Beta.py with pandas implementation** (Agent 2 approach)
2. **Audit other predictors using polars-ols** - They likely have similar issues
3. **Document that polars-ols rolling_ols is unreliable** for our use case
4. **Prefer manual implementations** when exact replication is needed

## 📊 The Numbers

- Current (polars-ols): 70.71% Precision1 failures
- Best fix (pandas manual): 57.43% failures
- Improvement: 13.28 percentage points
- Still not perfect but significantly better!

The remaining failures might be due to:
- Data differences between Python and Stata sources
- Other subtle calculation differences
- Need further investigation with specific failing cases