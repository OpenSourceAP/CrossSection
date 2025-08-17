# MS Time-Based Rolling Window Fix - Major Breakthrough

**Date**: 2025-08-17  
**Task**: Fix MS precision failures through time-based rolling windows  
**Result**: 40.6% improvement in precision, dramatic bias reduction

## Problem Identified

MS had 32.967% precision failures due to **position-based vs time-based rolling window** differences:

- **Stata**: `asrol window(time_avail_m 12) min(12)` uses calendar-based 12-month windows
- **Python**: `rolling(12, min_periods=12)` uses consecutive observation windows
- **Impact**: With irregular monthly data, this created huge systematic differences

## Root Cause Analysis

Using permno 11170 in 1995m6 as test case:
- **Stata's 12-month window**: Found only 11 observations (missing 1994-10-01), returned missing values ✅
- **Python's 12-obs window**: Found 12 consecutive observations spanning different time range, calculated values ❌

Same issue affected 48-month volatility rolling windows.

## Fixes Implemented

### 1. Quarterly Aggregation (12-month windows)
```python
# OLD: Position-based
pl.col("niq").rolling_mean(window_size=12, min_samples=12).over("permno")

# NEW: Time-based 
group['niqsum'] = group['niq'].rolling('366D', min_periods=12).mean() * 4
```

### 2. Volatility Measures (48-month windows)  
```python
# OLD: Position-based
pl.col("roaq").rolling_std(window_size=48, min_samples=18).over("permno")

# NEW: Time-based
group['niVol'] = group['roaq'].rolling('1470D', min_periods=18).std()
```

## Results - Dramatic Improvements

### Precision Failures
- **Before**: 32.967% → **After**: 19.575%
- **Improvement**: **40.6% reduction** in failing observations

### Systematic Bias (Slope)
- **Before**: python = 0.8246 + **0.7565** * stata
- **After**: python = 0.2175 + **0.9252** * stata  
- **Improvement**: **+22.4%** closer to perfect 1.0 correlation

### Model Fit (R-squared)
- **Before**: 0.5782 → **After**: 0.8765
- **Improvement**: **+51.6%** better explained variance

### Checkpoint Alignment
- **CHECKPOINT 2**: ROA/CFROA now correctly missing for early periods ✅
- **CHECKPOINT 3**: Volatility measures show appropriate missing patterns ✅  
- **CHECKPOINT 5**: Final MS scores much closer to Stata values ✅

## Technical Implementation

Used pandas time-based rolling with careful window sizing:
- **12 months**: 366 days (accounts for leap years)
- **48 months**: 1470 days (4 years + buffer)
- **min_periods**: Exactly matches Stata's min() requirements

Converting to/from pandas for time-based calculations, then back to polars for compatibility.

## Remaining Issues

Still 19.575% precision failures, likely due to:
1. Industry median calculation differences
2. Missing data handling edge cases  
3. Timing logic nuances (seasonal adjustment)
4. Potential data preprocessing differences

Some extreme cases still show ±5 differences (permno 49016, 76023), suggesting fundamental logic differences in specific scenarios.

## Key Learnings

1. **Position vs Time-Based Rolling**: Critical difference for irregular time series
2. **Stata's asrol behavior**: Requires exact calendar-based windows, not just observation counts
3. **Missing data propagation**: Time-based windows naturally handle data gaps correctly
4. **Debugging approach**: Focus on specific failing observations to understand root causes

## Next Steps

For further precision improvements:
1. Investigate industry median calculation differences
2. Check timing logic (seasonal adjustment) implementation  
3. Analyze extreme failing cases (±5 differences)
4. Verify data preprocessing alignment with Stata

This fix represents a major breakthrough in Stata-Python translation accuracy for financial time series with irregular data patterns.