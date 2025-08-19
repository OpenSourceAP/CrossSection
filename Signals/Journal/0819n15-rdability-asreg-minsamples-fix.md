# 0819n15 - RDAbility asreg min_samples Fix

## Problem Identified
RDAbility.py was producing incorrect values because the `asreg` function wasn't properly enforcing the `min_samples` parameter.

### Key Finding
For permno 86597 at fyear 1995:
- **Lag 4**: Only 4 valid observations (< 6 required)
  - Stata: Returns missing/null
  - Python (before fix): Returned -569.39 (extreme value due to ill-conditioned matrix)
- **Lag 5**: Only 3 valid observations (< 6 required)  
  - Stata: Returns missing/null
  - Python (before fix): Returned 125.82 (extreme value)

This caused RDAbility to be calculated as:
- Stata: 8.653519 (average of only gammaAbility1=9.71 and gammaAbility2=7.60)
- Python: -184.03 (included the extreme values from lag 4 and 5)

## Root Cause
The polars-ols library's `rolling_ols` function doesn't properly respect the `min_periods` parameter when there are fewer valid (non-null) observations than required. It still attempts regression on insufficient data, leading to numerical instability.

## Solution Applied
Added manual validation count in RDAbility.py:

```python
# Count valid observations in each 8-year rolling window
df = df.with_columns([
    (pl.col("tempY").is_not_null() & pl.col("tempXLag").is_not_null())
    .cast(pl.Int32)
    .rolling_sum(window_size=8, min_samples=1)
    .over("gvkey")
    .alias("_valid_count")
])

# Only keep coefficients when valid_count >= 6
df = df.with_columns(
    pl.when(pl.col("_valid_count") >= 6)
    .then(result["b_tempXLag"])
    .otherwise(None)
    .alias(f"gammaAbility{n}")
)
```

## Result
After the fix, for permno 86597 at fyear 1995:
- gammaAbility1: 9.70539 ✓ (matches Stata)
- gammaAbility2: 7.601648 ✓ (matches Stata)
- gammaAbility3: null ✓ (matches Stata)
- gammaAbility4: null ✓ (now correct, was -569.39)
- gammaAbility5: null ✓ (now correct, was 125.82)
- RDAbility: 8.653519 ✓ (exactly matches Stata)

## Remaining Issues
The test still shows 4.3% of observations with differences. Further investigation may be needed for:
1. Observations with infinite values (e.g., permno 14033 fyear 2024 has inf values)
2. Edge cases in the rolling window calculation
3. Potential differences in how Stata and Python handle the `rowmean` calculation

## Lessons Learned
1. Always verify that statistical libraries properly enforce minimum sample requirements
2. Numerical instability can produce plausible-looking but completely wrong results
3. When translating from Stata, pay special attention to how missing values and edge cases are handled
4. Manual validation of constraints may be necessary when library functions don't behave as expected