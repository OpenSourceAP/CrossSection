# 0815n1: Quantile Interpolation Method Fix for BetaTailRisk

## Problem Summary
BetaTailRisk was failing precision tests with 4.15% of observations having differences >= 0.01. The largest errors (~0.15-0.20) were concentrated around permno 78050 during Nov 1998 - Aug 1999.

## Root Cause: Quantile Interpolation Method Mismatch

### What is Quantile Interpolation?

When calculating quantiles (like the 5th percentile), the exact position often falls between two data points. For example, if you have 100 observations, the 5th percentile is at position 5.0 - which corresponds to a specific data point. But with 175,277 observations (like Nov 1998), the 5th percentile is at position 8,763.85 - which falls between the 8,763rd and 8,764th values.

Different interpolation methods handle this fractional position differently:

1. **"nearest"** (Python default): Takes the closest data point
2. **"lower"**: Always takes the lower value (8,763rd in this case)  
3. **"higher"**: Always takes the higher value (8,764th in this case)
4. **"linear"**: Linearly interpolates between the two values
5. **"midpoint"**: Takes the average of the two boundary values

### The Specific Issue

For Nov 1998 with 175,277 observations:
- Position 8,763: -0.071310
- Position 8,764: -0.071240

**Stata uses "lower" method**: -0.071310
**Python default "nearest"**: -0.071240 (closer to fractional position 8,763.85)

This small difference (0.00007) gets amplified through the entire calculation pipeline:
1. Different 5th percentile thresholds
2. Different sets of "tail" observations included
3. Different log(ret/retp5) calculations  
4. Different monthly averages
5. Different rolling regression inputs
6. Final BetaTailRisk values differ by ~0.15-0.20

## Functions Involved

### Stata Functions
- `egen retp5 = pctile(ret), p(5) by(time_avail_m)` - Uses "lower" interpolation by default
- Stata's quantile functions consistently use this method across versions

### Python Functions  
- **Before**: `pl.col("ret").quantile(0.05)` - Uses "nearest" (default)
- **After**: `pl.col("ret").quantile(0.05, interpolation="lower")` - Matches Stata

### Other Affected Functions
This issue could affect any script that uses:
- `quantile()` in polars
- `percentile()` in numpy  
- `quantile()` in pandas
- Any percentile-based calculations (p10, p25, p50, p75, p90, etc.)

## The Fix

**File**: `pyCode/Predictors/BetaTailRisk.py`
**Line**: 70-72

```python
# OLD (incorrect)
monthly_p5 = daily_crsp.group_by("time_avail_m").agg([
    pl.col("ret").quantile(0.05).alias("retp5")
])

# NEW (correct)  
monthly_p5 = daily_crsp.group_by("time_avail_m").agg([
    pl.col("ret").quantile(0.05, interpolation="lower").alias("retp5")
])
```

## Validation Results

**Before Fix**:
- ❌ Precision1: 4.149% failures (95,107/2,292,350 observations)
- ❌ Largest differences: ~0.20 for permno 78050

**After Fix**:
- ✅ Precision1: 0.013% failures (307/2,292,350 observations)  
- ✅ Largest differences: ~0.006
- ✅ **ALL TESTS PASSED**

## Broader Implications

### For Other Predictors
This discovery suggests we should audit other predictors that use quantiles:
- Any `pctile` operations in Stata
- Winsorizing operations (`winsor2`)
- Ranking operations that use percentiles
- Industry breakpoints based on quantiles

### Standard Practice Going Forward
For all future translations:
1. **Always specify `interpolation="lower"`** for quantile calculations
2. **Test quantile methods** during checkpoint validation
3. **Document quantile method** in script comments
4. **Add this to the translation checklist**

### Common Quantile Operations to Watch
```python
# Percentiles
df.quantile(0.05, interpolation="lower")  # 5th percentile
df.quantile(0.95, interpolation="lower")  # 95th percentile

# Winsorizing (trimming extremes)
p01 = df.quantile(0.01, interpolation="lower")
p99 = df.quantile(0.99, interpolation="lower")

# Industry breakpoints
breakpoints = df.quantile([0.3, 0.7], interpolation="lower")
```

## Debugging Process That Led to Discovery

1. **Checkpoint comparison**: Noticed small differences in 5th percentile values
2. **Focused investigation**: Created Debug/test_quantile_method.py
3. **Method testing**: Tested all 5 interpolation methods
4. **Exact match**: "lower" method matched Stata perfectly
5. **Systematic validation**: Confirmed across all target months

## Key Lesson

**Small methodological differences can cascade into large errors.** A 0.00007 difference in a 5th percentile calculation led to 4% precision failures. This emphasizes the importance of:
- Understanding the exact behavior of statistical functions
- Not assuming defaults are consistent across software
- Using checkpoint-based debugging to isolate issues
- Testing edge cases during translation

## Files Modified
- `pyCode/Predictors/BetaTailRisk.py` - Fixed quantile interpolation method
- `pyCode/Debug/test_quantile_method.py` - Debugging script (created)  
- `pyCode/Debug/debug_betatailrisk_78050.py` - Investigation script (created)

## Documentation Updated
This discovery should be added to:
- `DocsForClaude/traps.md` - New trap about quantile interpolation
- Translation guidelines - Standard practice for quantile methods
- Debugging checklist - Include quantile method verification