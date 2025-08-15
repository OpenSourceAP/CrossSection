# Asrol Consecutive Periods Problem - Critical Issue for Stata Translation

**Date**: 2025-08-15  
**Context**: Debugging Herf predictor precision failures  
**Status**: Root cause identified, requires architectural fix

## Problem Summary

The `asrol` function in `utils/data_utils.py` does not replicate Stata's `asrol` behavior correctly. This causes **systematic precision failures** in predictors that use rolling calculations with data gaps.

**Key Issue**: Stata's `asrol` only uses consecutive periods for rolling calculations, while Python's pandas `.rolling()` uses all available observations within the window, allowing gaps.

## Specific Example: Permno 64785 in Herf Predictor

### The Data Gap
- **1995-05-01**: Last observation in first consecutive period (SIC 3560)
- **[12-year gap with no data]**
- **2007-08-01**: First observation in second consecutive period (SIC 6719)

### Rolling 36-Month Average for 2009-02-01
- **Python pandas result**: 2.60 (uses last 36 available observations across gap)
- **Stata asrol result**: 4.80 (uses only 19 consecutive months from 2007-08 to 2009-02)
- **Difference**: 2.20 (exactly matches precision test failures)

### Test Results Impact
- **Herf Precision1**: ✅ 0.787% (under 1% threshold)
- **Herf Precision2**: ❌ 99.9th percentile diff = 5.06e-01 (above 0.1 threshold)
- **Affected observations**: 24,846 out of 3,158,336 (0.787%)

## Technical Details

### Current Implementation (utils/data_utils.py)
```python
# INCORRECT: Allows data gaps
df[new_col_name] = df.groupby(group_col)[value_col].rolling(
    window=window, min_periods=min_periods
).mean().reset_index(level=0, drop=True)
```

### Stata's Behavior
```stata
bys permno: asrol tempHerf, gen(Herf) stat(mean) window(time_avail_m 36) min(12)
```
- Only calculates rolling statistics within consecutive time periods
- If there's a gap > 1 month, starts a new rolling calculation from the beginning of the next consecutive period
- Never combines observations across time gaps

### Required Fix Pattern
```python
# CORRECT: Must identify consecutive periods first
def stata_asrol(df, group_col, time_col, value_col, window, stat, min_periods):
    result = []
    for group in df.groupby(group_col):
        # 1. Identify consecutive periods (gaps > 35 days = break)
        # 2. Apply rolling calculation only within each consecutive period
        # 3. Reset rolling window at each break
    return result
```

## Debug Scripts Created

### Key Files for Understanding the Issue
1. **`Debug/debug_herf_permno64785.py`**: Traces the problematic observation
2. **`Debug/debug_asrol_gap_issue.py`**: Demonstrates the consecutive periods problem
3. **`Debug/test_negative_sales_fix.py`**: Rules out negative sales as the cause

### Verification Commands
```bash
# Run the gap analysis
python3 Debug/debug_asrol_gap_issue.py

# Shows:
# - Pandas (gaps allowed): 2.598
# - Strict consecutive: 4.801  ← Matches Stata!
# - Stata expected: ~4.8
```

## Impact Assessment

### Affected Predictors
This issue affects **any predictor using asrol with data gaps**, including:
- **Herf**: Uses 36-month rolling average (confirmed affected)
- **Mom12m**: Uses 12-month momentum calculations
- **Any rolling statistics on irregular time series**

### Performance vs Accuracy Trade-off
- **Current pandas approach**: Fast but incorrect for gap-heavy data
- **Required Stata approach**: Slower but mathematically correct

## Implementation Strategy

### Phase 1: Targeted Fix (Immediate)
1. Create `stata_asrol` function that handles consecutive periods correctly
2. Use only for predictors with known gap issues (Herf, etc.)
3. Keep current `asrol` for predictors without gap issues

### Phase 2: Full Migration (Future)
1. Replace all `asrol` calls with `stata_asrol`
2. Performance optimization with vectorized operations
3. Comprehensive testing across all predictors

## Code Architecture Requirements

### Function Signature
```python
def stata_asrol(df, group_col, time_col, value_col, window, stat='mean', min_periods=1):
    """
    Stata-compatible asrol that respects consecutive periods
    
    Key difference: Only calculates rolling statistics within consecutive
    time periods, never across data gaps.
    """
```

### Algorithm Steps
1. **Group by entity** (e.g., permno)
2. **Sort by time** within each group
3. **Identify breaks** where `time_diff > 35 days`
4. **Create period IDs** for each consecutive segment
5. **Apply rolling calculation** within each period separately
6. **Handle min_periods** requirement per Stata behavior

### Performance Considerations
- Use vectorized operations where possible
- Consider caching for repeated calculations
- Profile against large datasets (>4M observations)

## Testing Requirements

### Validation Cases
1. **Regular monthly data**: Should match current asrol
2. **Data with gaps**: Should match Stata asrol exactly
3. **Mixed scenarios**: Some entities with gaps, others without
4. **Edge cases**: Very short consecutive periods, all-gap data

### Test Data
- **Permno 64785**: Known case with 12-year gap
- **Permno 11406**: Regular case from Stata log (should be ~0.29)
- **Synthetic data**: Controlled gap patterns

## Priority and Timeline

### Priority: HIGH
- Affects multiple predictors
- Causes systematic precision failures
- Architectural issue requiring careful implementation

### Estimated Effort
- **Research and design**: 4-6 hours
- **Implementation**: 8-12 hours  
- **Testing and validation**: 6-8 hours
- **Total**: 18-26 hours

## Related Issues

### Fixed During Investigation
1. **String comparison**: Added space in `" 4813"` for regulated industries
2. **Negative sales**: Confirmed Stata includes them (was not the issue)
3. **SIC code conversion**: Working correctly

### Still Outstanding
1. **Asrol consecutive periods**: This critical architectural issue
2. **Performance optimization**: After correctness is achieved

## Next Steps

1. **Immediate**: Document this issue (✅ DONE)
2. **Short-term**: Implement `stata_asrol` function 
3. **Medium-term**: Migrate Herf and other gap-affected predictors
4. **Long-term**: Full asrol replacement across all predictors

## References

- **Stata asrol documentation**: Rolling statistics with time gaps
- **Pandas rolling documentation**: Default gap-inclusive behavior
- **Test results**: `Logs/testout_predictors.md` for Herf precision failures
- **Debug outputs**: All debug scripts in `Debug/debug_*asrol*.py`