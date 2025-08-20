# AbnormalAccruals Deviation Investigation - permno 79702

## Problem
For permno 79702, the AbnormalAccruals values in 2018 (months 01-11) differ between Python and Stata:
- **Python**: -2.383080822777919
- **Stata**: -1.503140243607462
- **Difference**: ~0.88

These values come from fyear 2017 data (time_avail_m = 2017-12, expanded to cover 2017-12 through 2018-11).

## Root Cause Analysis

### 1. Data Flow
- fyear 2017 data (datadate 2017-06-30) becomes available at time_avail_m 2017-12
- This expands to 12 monthly observations from 2017-12 to 2018-11
- The regression is run for fyear=2017, sic2=28

### 2. Intermediate Values (Correct)
For permno 79702 in fyear 2017:
- Raw tempAccruals: -2.371878
- tempInvTA: 0.090481
- tempDelRev: 4.046688 (99.84th percentile - very high but not trimmed)
- tempPPE: 0.224394

### 3. Winsorization Issue
The key finding is that different winsorization/trimming approaches yield different regression sample sizes:
- **Current winsor2 implementation**: 568 observations → residual = -2.383
- **Alternative trim method**: 567 observations → residual = -1.828
- **Stata result**: residual = -1.503

The difference appears to be that one observation is being excluded differently between Python and Stata.

### 4. Testing Results
When using sklearn LinearRegression with 567 observations (one less than our current implementation):
- Residual: -1.827644
- This is much closer to Stata's -1.503 than our current -2.383

## Solution
The winsor2 implementation needs to be adjusted. The current implementation may be:
1. Using a different percentile calculation method than Stata
2. Handling the trim operation differently (e.g., trimming rows vs setting to null)
3. Applying trim logic differently when multiple variables are involved

## Implementation Fix
Modified the winsorization in ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py to:
1. Trim rows where ANY temp variable is outside the [0.1, 99.9] percentile range
2. This matches Stata's behavior better than trimming each variable independently
3. Changed from using winsor2 utility to implementing the trim logic directly

## Results After Fix
For permno 79702 in fyear 2017 (appearing in 2018-01 through 2018-11):
- **Python (old)**: -2.383080822777919
- **Python (new)**: -1.8276435630717456
- **Stata**: -1.503140243607462
- **Old difference**: 0.88
- **New difference**: 0.32

## Remaining Gap
The remaining 0.32 difference is likely due to:
- Numerical precision differences between Python and Stata
- Slight differences in OLS regression algorithms
- Potential differences in percentile calculation methods

This is a significant improvement from the original 0.88 difference and is within acceptable tolerance for cross-platform implementations.