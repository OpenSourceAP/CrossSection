# ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F Debug Analysis - Residual Sign Issue Discovery

**Date**: 2025-08-17  
**Script**: ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py  
**Issue**: ReturnSkew3F precision failure 2.676% → 2.575%

## Executive Summary

Discovered the root cause of ReturnSkew3F precision failures: **systematic sign differences in FF3 regression residuals** for degenerate cases where all daily returns are identical within a month.

## Key Breakthrough

### Original Problem
- ReturnSkew3F had 2.676% precision failure rate  
- Largest differences showed exact opposites: Python = -4.364358, Stata = +4.364358
- 128 different permnos in yyyymm=198212 ALL had identical pattern

### Root Cause Discovery
1. **Degenerate input data**: For permno 49382 in 198212, ALL 22 daily returns were identical: `-0.00031`
2. **Regression becomes numerically unstable**: When all inputs are identical, FF3 regression has infinite solutions
3. **Sign ambiguity**: Python's asreg (SVD method) vs Stata's asreg produce residuals with opposite signs
4. **Systematic impact**: Affects all 128 permnos in that month with identical returns

### Specific Analysis
**Permno 49382, yyyymm=198212:**
- All 22 returns: `-0.00031` (identical)
- Python residuals: 21 values ≈ `1.084e-19`, 1 value ≈ `5.421e-20`
- Standardized residuals: 21 values = `+0.218`, 1 value = `-4.583`
- **Python skewness**: -4.364358
- **Stata skewness**: +4.364358
- **Negating Python residuals produces exact Stata match**: +4.364358

## Fixes Applied

### 1. Removed Incorrect Post-Processing (COMPLETED)
**Problem**: Python code had unauthorized post-processing step replacing extreme values
```python
# REMOVED: This was not in Stata code
pl.when((pl.col("ReturnSkew3F").abs() > 4.0) | pl.col("ReturnSkew3F").is_null())
.then(0.1790421686972114)  # Hardcoded replacement
```

**Fix**: Replaced with comment: `# NO POST-PROCESSING: Stata code does not modify ReturnSkew3F values`

**Result**: Precision improved from 2.676% to 2.575% failure rate

### 2. Core Issue Identified (NEEDS DEEPER INVESTIGATION)
**Problem**: Systematic residual sign differences in degenerate regression cases  
**Root cause**: asreg numerical implementation differences (Python SVD vs Stata's method)  
**Impact**: When all returns identical → regression numerically unstable → sign ambiguity

## Test Results

### Before Fix
- Precision1: 2.676% failure  
- Precision2: 99.900th percentile diff = 4.54e+00

### After Fix  
- Precision1: 2.575% failure (3.8% improvement)
- Precision2: 99.900th percentile diff = 1.40e+00 (69% improvement)

## Technical Insights

### When Skewness Calculation Breaks Down
1. **Normal case**: Diverse residuals → well-defined skewness
2. **Degenerate case**: All residuals ≈ 0 → numerically unstable skewness
3. **Current case**: Tiny residual differences → skewness dominated by numerical artifacts

### Numerical Behavior
- 21 observations: standardized = +0.218 → cube = +0.0104
- 1 observation: standardized = -4.583 → cube = **-96.234** (dominates!)
- Final skewness = mean of cubes = -4.364

## Status and Next Steps

### Achieved
✅ Identified exact root cause: residual sign differences in degenerate cases  
✅ Removed incorrect post-processing masking the issue  
✅ Improved precision by 3.8% (2.676% → 2.575%)  
✅ Created comprehensive debugging framework for similar issues

### Remaining Work
🔧 **Core numerical issue**: Requires investigation of asreg vs Stata's regression implementation  
🔧 **Sign convention**: Need to understand which method is "correct" or implement sign standardization  
🔧 **Edge case handling**: Consider special handling for degenerate regression cases (all inputs identical)

### Recommendation
This is a complex numerical analysis issue requiring comparison of regression implementations. The 3.8% improvement shows we're on the right track, but the remaining 2.575% failure rate suggests this is a systematic difference that affects multiple months/permnos with degenerate data patterns.

## Debug Files Created
- `Debug/find_exact_case.py`: Identifies specific problematic permnos
- `Debug/analyze_permno_49382.py`: Deep dive into residual calculations  
- `Debug/exact_residuals_49382.py`: Exact numerical analysis
- `Debug/test_zero_variance_skew.py`: Skewness edge case testing
- `Debug/test_skew_198212.py`: Month-specific analysis