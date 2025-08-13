# PS Predictor: Missing Values Analysis

## Root Cause Identified

The PS predictor failure is due to **Stata's missing value logic** vs Python's missing value handling.

### Key Finding

**Permno 10001, yyyymm 198705**:
- Python PS: 3 (only p1, p2, p4 work due to missing lags)  
- Stata PS: 8 (lagged comparisons evaluate to TRUE due to missing=+infinity)

### Stata's Missing Value Logic

From DocsForClaude/traps.md: **Stata treats missing values as positive infinity in all comparisons.**

**Critical insight**: When 12-month lags are missing (no data 12 months ago), Stata's comparison logic treats them as +infinity:

```stata
# p3: (ib/at - l12.ib/l12.at) > 0
# When l12.ib and l12.at are missing:
# current - missing = missing
# missing > 0 = TRUE (because missing = +infinity)
```

### Debug Results

With proper Stata missing logic, I get PS = 9, vs Stata's 8. Almost perfect match.

**Components with corrected logic**:
- p1: 1 (ib > 0)
- p2: 1 (fopt > 0) 
- p3: 1 (missing lag → TRUE)
- p4: 1 (fopt > ib)
- p5: 1 (missing lag → TRUE) 
- p6: 1 (missing lag → TRUE)
- p7: 1 (missing lag → TRUE)
- p8: 1 (missing lag → TRUE)
- p9: 1 (missing lag → TRUE)

Need to find which component differs by 1 between my logic and actual Stata.

### Implementation Plan

1. Fix PS.py to use Stata's missing value logic for lag comparisons
2. Use `np.where()` with explicit missing handling for each component
3. Key pattern: `(condition) | (lag_var.isna())` for "greater than" comparisons
4. Pattern: `(condition) & (lag_var.notna())` for "less than" comparisons  
5. Pattern: `(condition) | (lag_var.isna())` for "less than or equal" comparisons

### Expected Fix

This should resolve ~18% precision failures and bring PS from failing to passing.