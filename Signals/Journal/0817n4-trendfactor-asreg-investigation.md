# TrendFactor: asreg Implementation Investigation - August 17

## Summary
Executed Plan/miniplan-logdebug.md for TrendFactor debugging. Identified that Python's asreg produces different regression coefficients than Stata's asreg, causing 4-6x higher final TrendFactor values. Attempted fix did not improve precision (97.137% failure rate unchanged).

## Key Findings

### 1. Perfect Match on Data Normalization
- ✅ Moving average calculation (A_3, A_5, etc.) matches Stata exactly
- ✅ Price normalization (A_L/P) matches Stata perfectly  
- ✅ Input data for regression (ret, fRet) matches Stata exactly

### 2. Regression Coefficient Differences
**Python vs Stata checkpoint 4 (_b_A_* values):**
- 91040 2018m1: Python _b_A_3=0.61176 vs Stata _b_A_3=0.72920163
- 91040 2018m2: Python _b_A_3=-0.622152 vs Stata _b_A_3=-0.61578691
- Similar differences across all coefficients

### 3. Expected Beta (EBeta) Sign Issues  
**Python vs Stata checkpoint 5 (EBeta values):**
- 89901 2020m9: Python EBeta_3=0.026007 vs Stata EBeta_3=-0.02052406 ❌ **Different signs!**
- 89901 2020m9: Python EBeta_5=-0.054907 vs Stata EBeta_5=0.02860362 ❌ **Different signs!**

### 4. Final TrendFactor Magnitude Differences
**Python vs Stata final values:**
- 91040 2018m1: Python=2.339864 vs Stata=0.5671266 (4.1x higher)
- 89901 2020m9: Python=2.889721 vs Stata=0.4848789 (6.0x higher)

## Root Cause Analysis

The issue occurs in the cross-sectional regression step:
- `bys time_avail_m: asreg fRet A_*` (Stata)
- `asreg(df, y="fRet", X=feature_cols, by=["time_avail_m"], mode="group")` (Python)

**Hypothesis:** Python's asreg helper function implementation differs from Stata's asreg in:
1. Sample handling/filtering
2. Regression algorithm 
3. Missing value treatment
4. Numerical precision

## Attempted Fix
Changed `min_samples=12` to `min_samples=1` in asreg call to allow all samples like Stata.

**Result:** No improvement. Precision failure rate remains exactly 97.137%.

## Next Steps Needed

1. **Deep dive into asreg helper function** - Compare Python implementation with Stata asreg documentation
2. **Test with minimal dataset** - Create controlled test with known regression inputs/outputs  
3. **Check 12-month rolling average** - Investigate if EBeta calculation differs from Stata's `asrol _b_A_L', window(time_avail_m -13 -1) stat(mean)`
4. **Sample size investigation** - Check if cross-sectional regressions use different numbers of observations

## Technical Details
- Python checkpoints match Stata perfectly through checkpoint 3 (pre-regression)
- Divergence begins at checkpoint 4 (regression coefficients)
- Issue persists through checkpoint 5 (EBeta) and checkpoint 6 (final TrendFactor)
- No improvement despite allowing smaller regression samples (min_samples=1)

## Status: ATTEMPTED - Deeper Investigation Required
The min_samples fix was insufficient. The core issue is in the asreg implementation differences between Python and Stata. This requires more sophisticated debugging of the regression methodology itself.