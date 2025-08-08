# MS Predictor Debugging Breakthrough - Null Handling Logic

**Date**: 2025-08-07  
**Task**: Debug MS predictor superset failure (58.53% missing observations)  
**Result**: **99.93% superset success** - massive breakthrough!

## Problem Summary
- MS predictor missing 276,894/473,079 observations (58.53% failure)
- Target observation permno=10010, yyyymm=199104 had MS=3 in Stata but missing in Python
- Initially suspected min_samples parameters were too strict

## Key Debugging Steps

### 1. **Focus on Specific Observation**
- Traced permno=10010, yyyymm=199104 through entire pipeline
- Found observation survived all steps until binary indicators
- Discovered tempMS was null, causing final filter to remove it

### 2. **Root Cause: Null Value Handling**
Found target observation had multiple null m-components:
- m2 (cfroa > md_cfroa): **NULL** because cfroa was null
- m3 (oancfqsum > niqsum): **NULL** because oancfqsum was null  
- m4 (niVol < md_niVol): **NULL** because niVol was null
- m5 (revVol < md_revVol): **NULL** because revVol was null
- m7 (capxint > md_capxint): **NULL** because capxint was null

### 3. **Critical Insight: Stata vs Python Logic**

**Stata Logic:**
```stata
gen m2 = 0
replace m2 = 1 if cfroa > md_cfroa
```
- If `cfroa` is null, condition fails → m2 stays 0

**Python Logic (WRONG):**
```python
(pl.col("cfroa") > pl.col("md_cfroa")).cast(pl.Int32).alias("m2")
```
- If `cfroa` is null, comparison returns null → m2 becomes null → tempMS becomes null

**Python Logic (CORRECT):**
```python
pl.when(pl.col("cfroa") > pl.col("md_cfroa")).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m2")
```
- If `cfroa` is null, condition fails → m2 becomes 0 (matches Stata)

## Key Lessons Learned

### 1. **Focus on Specific Observations**
- ✅ RIGHT: Pick one specific permno-yyyymm and trace through every step
- ❌ WRONG: Debug by changing parameters without understanding why specific observations fail

### 2. **Don't Change min_samples Without Evidence**  
- ❌ WRONG: Assume `min_samples=12` is too strict and change to 8 or 6
- ✅ RIGHT: Match Stata's exact `min(12)` and `min(18)` parameters from source code
- **I initially made this error** - changed min_samples thinking it would help

### 3. **Understand Stata's Null Handling Logic**
- **Key Discovery**: `gen m_x = 0; replace m_x = 1 if condition` defaults null conditions to 0
- **Python Fix**: Use `pl.when(condition).then(1).otherwise(0)` not `(condition).cast(pl.Int32)`

### 4. **Null Comparisons Behave Differently**
- **Stata**: `null > median` evaluates to false → stays 0
- **Python**: `null > median` evaluates to null → makes tempMS null → filtered out

### 5. **Debug Step-by-Step Through Pipeline**
- Trace data loss at each step: merge → sample selection → variable prep → aggregations → indicators
- The real issue was in the final binary indicator step, not early data processing

### 6. **Check Final Filter Logic**
- Missing observations often result from intermediate null values that get filtered out
- Look for `.filter(pl.col("MS").is_not_null())` removing valid observations

### 7. **Match Stata Line-by-Line, Don't Optimize**
- ❌ WRONG: "Improve" the logic with different rolling window parameters  
- ✅ RIGHT: Replicate exact Stata behavior, even if it seems suboptimal

## Results
- **Before**: 196,190 observations (58.53% missing from Stata)  
- **After**: 473,026 observations (**0.07% missing** from Stata)
- **Achievement**: **99.93% superset success** - only 337/473,079 observations missing

## Technical Fix Applied
Changed all 8 binary indicator calculations from:
```python
(pl.col("metric") > pl.col("md_metric")).cast(pl.Int32).alias("m_x")
```

To:
```python
pl.when(pl.col("metric") > pl.col("md_metric")).then(pl.lit(1)).otherwise(pl.lit(0)).alias("m_x")
```

This ensures null conditions default to 0, exactly matching Stata's behavior.

## Impact
This represents a **game-changing improvement** in understanding how to replicate Stata's exact behavior. The principle of "match Stata's null handling logic" should be applied to all other predictors with similar conditional logic.