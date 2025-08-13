# Stata Inequality Fix for MS.py - Success!

**Date**: 2025-08-13  
**Issue**: MS.py had incorrect missing value handling in binary indicator comparisons  
**Solution**: Created new utils/stata_ineq.py and integrated into MS.py  

## Problem

MS.py was using standard Python inequality operators which treat missing values differently than Stata:
- Python: `missing > value` → False
- Stata: `missing > value` → True (missing treated as positive infinity)

This caused systematic undercounting in the 8 binary Mohanram G-score components (m1-m8).

## Solution

### Created `utils/stata_ineq.py`
New utility file with 4 functions:
- `stata_greater_than(left, right)` - Polars version for `>`
- `stata_less_than(left, right)` - Polars version for `<`  
- `stata_greater_than_numpy(left, right)` - NumPy version for pandas
- `stata_less_than_numpy(left, right)` - NumPy version for pandas

These implement Stata's exact missing value logic:
- `missing > finite = True`
- `finite > missing = False`
- `missing > missing = False`
- Similar rules for `<`

### Updated MS.py
Replaced all 8 binary indicator comparisons:
```python
# OLD (incorrect)
pl.when(pl.col("roa") > pl.col("md_roa")).then(pl.lit(1)).otherwise(pl.lit(0))

# NEW (Stata-compatible)  
pl.when(stata_greater_than(pl.col("roa"), pl.col("md_roa"))).then(pl.lit(1)).otherwise(pl.lit(0))
```

Applied to all indicators:
- m1, m2, m3, m6, m7, m8: use `stata_greater_than()`
- m4, m5: use `stata_less_than()`

## Results

**Major improvement**: Bad observations reduced from 63.4% to 33.0% (nearly 50% reduction!)

This confirms missing value handling was a significant systematic issue. Still 33% bad observations remaining suggests other differences beyond missing values.

## Key Learnings

1. **Missing value traps are real** - DocsForClaude/traps.md warnings were spot-on
2. **Systematic issues compound** - Small logic differences create large-scale problems  
3. **Utils/ pattern works well** - Reusable Stata compatibility functions are valuable
4. **Test early and often** - The 50% improvement validates the fix approach

## Next Steps

The utils/stata_ineq.py functions can now be reused across other predictors that have similar missing value inequality issues. Still need to investigate remaining 33% differences in MS.py.