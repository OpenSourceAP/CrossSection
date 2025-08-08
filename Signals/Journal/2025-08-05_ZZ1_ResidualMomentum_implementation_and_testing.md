# ZZ1_ResidualMomentum Implementation and Testing

**Date**: 2025-08-05  
**Task**: Replicate `Code/Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum.do` in Python

## Implementation Summary

Successfully created Python translation of ZZ1_ResidualMomentum6m_ResidualMomentum.do with the following components:

### Files Created
1. **`pyCode/utils/saveplacebo.py`** - Utility for saving placebo signals (similar to savepredictor.py but outputs to Placebos/)
2. **`pyCode/Predictors/ZZ1_ResidualMomentum6m_ResidualMomentum.py`** - Main script implementing the Stata logic

### Data Processing Pipeline
1. Load monthly CRSP and FF data (5.15M observations)
2. Calculate excess returns: `retrf = ret - rf`
3. Create sequential time index (`time_temp`) for rolling operations
4. Perform rolling 36-month FF3 regressions by permno using numpy/pandas
5. Calculate lagged residuals (`temp = l1._residuals`)
6. Compute rolling 6-month and 11-month statistics (mean, std)
7. Generate momentum signals as mean/std ratios

### Outputs Generated
- **ResidualMomentum6m.csv** (111MB, 3.5M observations) → `pyData/Placebos/`
- **ResidualMomentum.csv** (107MB, 3.4M observations) → `pyData/Predictors/`

## Testing Results

Ran `python3 utils/test_predictors.py --predictors ResidualMomentum` with the following results:

### Test Results Summary
- ✅ **Test 1 - Column names**: PASSED
- ❌ **Test 2 - Superset check**: FAILED (Python missing 83,157 Stata observations = 2.4%)
- ❌ **Test 3 - Precision check**: FAILED (100th percentile diff = 4.39e-02 >= 1.00e-06)

### Detailed Issues

#### Issue 1: Missing Observations (83,157)
- Python: 3,375,265 observations
- Stata: 3,458,422 observations  
- Missing observations appear to be from early dates (e.g., permno 10012 from 199003 onwards)
- **Hypothesis**: Rolling window implementation starts later than Stata's version

#### Issue 2: High Precision Differences
- 14.2% of observations (478,734/3,375,265) exceed tolerance
- Maximum difference: 4.39e-02 vs tolerance of 1.00e-06
- **Hypothesis**: Systematic differences in rolling regression or momentum calculations

## Technical Implementation Notes

### Rolling Regression Approach
Used custom numpy-based rolling regression function instead of statsmodels for performance:
```python
def compute_rolling_residuals(group):
    # 36-month rolling window with numpy lstsq
    # Vectorized approach for better performance
```

### Key Challenges
1. **Panel data operations**: Converting polars → pandas for rolling operations
2. **Memory efficiency**: Processing 38,835 permnos with custom groupby functions
3. **Stata equivalence**: Matching exact behavior of `asreg` and `asrol` commands

## Next Steps Required

### Debugging Strategy
1. **Investigate missing observations**:
   - Compare date ranges and permno coverage between Stata/Python
   - Check if 36-month window requirement is implemented consistently
   - Verify sequential time index (`time_temp`) creation

2. **Debug precision differences**:
   - Focus on specific permno-yyyymm observation that fails
   - Step through rolling regression calculation manually
   - Compare FF3 residuals calculation vs Stata
   - Verify lagged residuals and rolling statistics logic

3. **Bisection debugging approach**:
   - Isolate which step introduces the largest differences
   - Test intermediate outputs (residuals, rolling means, rolling stds)
   - Compare with small sample of observations

### Lessons Learned
- High error rates (14.2%) indicate systematic rather than numerical precision issues
- Rolling panel operations require careful attention to window definitions and edge cases
- Early implementation testing reveals structural issues before optimization

## Status
- ❌ **Implementation**: Complete but failing validation
- ❌ **Testing**: 0/1 predictors passed validation  
- 🔄 **Next**: Debug missing observations and precision differences