# 0821n1-trendfactor-multicollinearity.md

## Issue
TrendFactor.py returns NaN/0.0 for regression coefficients and EBeta values, while Stata returns proper values.

## Root Cause Discovery
After extensive debugging, found TWO issues:

### Issue 1: Window Size for Rolling Average
- **Stata**: Uses `window(time_avail_m -13 -1)` = 13-month window
- **Python**: Was using 12-month window with `rolling_mean(window_size=12)`
- **Fix**: Changed to `rolling_mean(window_size=13)`

### Issue 2: Severe Multicollinearity
- The 11 moving average features (A_3, A_5, ..., A_1000) are HIGHLY correlated
- Condition number of X matrix: **7.01e+17** (extremely high!)
- Correlations between adjacent features: 0.8-0.93
- This causes the regression matrix to be nearly singular
- polars-ols returns null when it can't solve the regression due to numerical instability

## Why Stata Works But Python Doesn't
Stata's `asreg` likely uses:
1. Different numerical solver that's more tolerant of multicollinearity
2. Possible regularization or pseudo-inverse approach
3. Different handling of near-singular matrices

## Evidence
```python
# Condition number check for Feb 1928 data
X_with_intercept = np.column_stack([np.ones(506), X_data])  # 506 rows, 12 cols (11 features + intercept)
condition_number = np.linalg.cond(X_with_intercept)
# Result: 7.01e+17 (anything > 1e10 is problematic)

# Feature correlations
A_3 vs A_5: 0.9285
A_5 vs A_10: 0.9223
A_10 vs A_20: 0.8905
```

## Potential Solutions

### Option 1: Use Ridge Regression
Add small regularization to handle multicollinearity:
```python
# Instead of standard OLS, use ridge regression with small lambda
# This would require custom implementation since polars-ols doesn't support it
```

### Option 2: Use SVD-based Solver
Use numpy's lstsq which uses SVD and can handle singular matrices:
```python
from scipy.linalg import lstsq
coeffs, residuals, rank, s = lstsq(X, y, cond=None, lapack_driver='gelsd')
```

### Option 3: Match Stata's Exact Method
Research what numerical method Stata's asreg uses and replicate it exactly.

## Immediate Workaround
For now, could:
1. Use fewer lag lengths (e.g., only 3, 5, 10, 20, 50)
2. Implement custom regression with SVD solver
3. Add regularization parameter

## Testing Notes
- With 3 features (A_3, A_5, A_10): Works fine, gets coefficients
- With 11 features: Returns null due to multicollinearity
- Manual scipy.linalg.lstsq with 3 features matches Stata exactly

## Specific Stata Lines That Are Hard to Replicate

### Line 85: `bys time_avail_m: asreg fRet A_*`
This is the critical regression line that fails in Python due to multicollinearity.
- Stata's `asreg` somehow handles 11 highly correlated features (A_3 through A_1000)
- Python's polars-ols returns null due to near-singular matrix (condition number: 7e17)
- The regression works in Stata despite correlations of 0.8-0.93 between adjacent features

### Line 95: `asrol _b_A_`L', window(time_avail_m -13 -1) stat(mean) gen(EBeta_`L')`
Rolling average calculation that depends on the regression coefficients from line 85.
- Since Python gets null coefficients, this also produces null EBeta values
- The window specification `-13 -1` means 13 months (not 12 as initially assumed)

### Lines 110-118: TrendFactor calculation
```stata
gen TrendFactor = EBeta_3    * A_3 +   ///
                  EBeta_5    * A_5 +   ///
                  EBeta_10   * A_10 +  ///
                  EBeta_20   * A_20 +  ///
                  EBeta_50   * A_50 +  ///
                  EBeta_100  * A_100 + ///
                  EBeta_200  * A_200 + ///
                  EBeta_400  * A_400 + ///
                  EBeta_600  * A_600 + ///
                  EBeta_800  * A_800 + ///
                  EBeta_1000 * A_1000
```
This calculation produces 0.0 in Python because all EBeta values are null.

## Problem Dates and Permnos

### Dates Where Regression Fails
**All dates from 1926-2028 fail** due to multicollinearity, except:
- ✅ **1929-01-01**: Works (condition number: 7.32e+02)

**Problem dates with extreme condition numbers:**
- 1926-01-01: 7.85e+97
- 1926-06-01: 1.77e+65  
- 1927-01-01: 8.88e+49
- 1927-06-01: 1.05e+34
- 1928-01-01: 1.96e+18
- **1928-02-01: 5.57e+17** (our key test date)
- 1928-06-01: 2.36e+18

### Specific Problem Permnos for 1928-02-01
**All three test permnos have complete valid data but still get TrendFactor = 0.0:**

| Permno | Stata Expected | Python Actual | fRet | A_3 | A_5 | A_10 |
|--------|---------------|---------------|------|-----|-----|------|
| 25486  | 0.58562       | 0.0          | ✓    | ✓   | ✓   | ✓    |
| 15683  | 0.6249967     | 0.0          | ✓    | ✓   | ✓   | ✓    |
| 14787  | 0.5195121     | 0.0          | ✓    | ✓   | ✓   | ✓    |

**Data values for 1928-02-01:**
- Permno 14787: fRet=0.078838, A_3=0.997234, A_5=0.995021, A_10=0.992531
- Permno 15683: fRet=0.410714, A_3=1.011905, A_5=1.033929, A_10=1.021429  
- Permno 25486: fRet=-0.104, A_3=1.005333, A_5=1.0144, A_10=1.0208

### Scale of the Problem
From Python TrendFactor output (176,499 total rows):
- **15,856 rows (9.0%) have TrendFactor = 0.0** (due to null EBeta values)
- 160,643 rows (91.0%) have non-zero values
- This suggests the multicollinearity issue affects early periods most severely

## Suggested Solution: SVD-Based Custom Regression

Since we cannot access Mata source code (only compiled .mlib files), implement a **custom regression function** that mimics Stata's robust numerical behavior:

```python
def stata_like_regression(X, y):
    """
    Robust regression that handles multicollinearity like Stata's asreg
    Uses SVD-based solver similar to what Stata's Mata functions likely use
    """
    import numpy as np
    from scipy.linalg import lstsq
    
    # Add intercept if needed
    X_with_intercept = np.column_stack([np.ones(len(X)), X])
    
    # Use SVD-based solver with permissive conditioning
    coeffs, residuals, rank, s = lstsq(
        X_with_intercept, y, 
        cond=None,  # No condition number cutoff
        lapack_driver='gelsd'  # SVD-based, most robust
    )
    
    return coeffs
```

**Key advantages:**
- Uses SVD decomposition (most numerically stable)
- No condition number cutoff (handles near-singular matrices)
- `gelsd` driver is designed for ill-conditioned problems
- Should replicate Stata's tolerance for multicollinearity

This replaces the failing polars-ols regression in the critical line 85 of TrendFactor.py.

## Next Steps
1. Confirm with user if we should implement custom regression solver
2. Or reduce number of lag features to avoid multicollinearity
3. Or investigate Stata's exact numerical method