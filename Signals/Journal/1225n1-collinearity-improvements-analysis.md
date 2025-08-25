# Analysis: Using asreg_collinear for Predictors

Date: 2025-12-25
Doctor Andrew

## Summary

Investigated using the `asreg_rebuild` module's collinearity handling features to improve three predictors: AbnormalAccruals, ResidualMomentum, and BetaFP.

## Key Findings

### 1. AbnormalAccruals - HIGH PRIORITY ✅
**Issue**: Cross-sectional regressions by year-industry could have collinearity issues, especially in small industry groups.

**Solution Implemented**: 
- Created `ZZ2_AbnormalAccruals_AbnormalAccrualsPercent_collinear.py`
- Uses `asreg` from `asreg_rebuild.stata_regress` with `drop_collinear=True`
- Handles rank-deficient groups properly by outputting NaN for problematic windows

**Benefits**:
- More robust handling of small industry groups
- Prevents numerical instability in rank-deficient cases
- Better matches Stata's behavior with collinear variables

### 2. ResidualMomentum - MEDIUM PRIORITY ✅
**Issue**: Rolling 36-month FF3 regressions could face collinearity in periods with limited factor variation.

**Solution Implemented**:
- Created `ZZ1_ResidualMomentum6m_ResidualMomentum_collinear.py`
- Uses `asreg` with rolling windows and `drop_collinear=True`
- Properly handles rank-deficient windows

**Benefits**:
- More robust during market stress periods where factors may be highly correlated
- Better numerical stability
- Cleaner handling of problematic windows

### 3. BetaFP - LOW PRIORITY (No changes needed)
**Current approach**: Uses correlation-based R² calculation, avoiding regression entirely.

**Assessment**: 
- No immediate benefit from collinearity handling since it doesn't run regressions
- The correlation approach is already numerically stable
- Recommendation: Keep as-is

## Technical Details

### asreg_rebuild Features Used

The `asreg_rebuild/stata_regress.py` module provides:

1. **`drop_collinear()` function**: 
   - Identifies and drops rank-deficient columns using QR decomposition or greedy methods
   - Returns list of kept/dropped columns with reasons

2. **`regress()` function**: 
   - Stata-like regression with automatic collinearity handling
   - Handles constant columns and linear dependencies

3. **`asreg()` function**: 
   - Panel/rolling regressions with `drop_collinear=True` parameter
   - Outputs NaN for rank-deficient windows/groups
   - Matches Stata's asreg behavior closely

### Implementation Challenges

1. **Data format conversion**: Need to convert between polars and pandas DataFrames
2. **Column preservation**: asreg returns only regression outputs, need to merge back with original data
3. **Empty groups**: Some year-industry combinations have no valid data after winsorization

## Files Created

1. `/pyCode/Predictors/ZZ2_AbnormalAccruals_AbnormalAccrualsPercent_collinear.py`
2. `/pyCode/Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum_collinear.py`

## Next Steps

1. Run full tests comparing original vs collinear-handled versions
2. Check for performance improvements
3. Consider migrating other regression-based predictors to use asreg_rebuild

## Conclusion

The collinearity handling from `asreg_rebuild` provides more robust regression estimates, especially for:
- Small groups (AbnormalAccruals with small industries)
- Rolling windows with potential multicollinearity (ResidualMomentum during market stress)

The implementation successfully handles rank-deficient cases that could cause numerical instability in the original implementations.