# Failed Attempt: Using asrol_pedantic to Fix MS Predictor

**Date**: 2025-08-16  
**Task**: Fix MS predictor precision failures using asrol_pedantic  
**Result**: FAILED - Made precision worse  

## What We Tried

### Hypothesis
The MS predictor had 32.97% precision failures because Polars' `rolling_std()` uses observation-based windows while Stata's `asrol` uses calendar-time based windows. We theorized that `asrol_pedantic.py` would provide exact Stata compatibility.

### Changes Made

1. **Replaced rolling_std with asrol_pedantic** (lines 217-220 in MS.py)
   - Changed from `pl.col("roaq").rolling_std(window_size=48, min_samples=18)` 
   - To `asrol_pedantic()` with exact Stata `asrol` options

2. **Fixed filtering order** (moved lines 108-130 to after line 250)
   - Previously: Filter to BM quintile 1 → Calculate rolling volatilities (missing history)
   - Now: Calculate rolling volatilities on full dataset → Then filter

### Results

**Before**: 32.97% precision failures  
**After**: 40.96% precision failures  

**Made it WORSE by 8 percentage points.**

## What Actually Happened

### Positive Changes
- Volatility calculations now work (no more NaN values)
- permno 11170 CHECKPOINT 3 shows real values:
  - niVol: 0.008759, 0.007396, etc. (was NaN)
  - revVol: 0.229176, 0.243333, etc. (was NaN)

### The Problem
- The volatility values we calculate are systematically different from Stata
- New worst case: permno 10812 (5-point differences)
- asrol_pedantic apparently doesn't match Stata's asrol as closely as claimed

## Why It Failed

### Root Cause Analysis
1. **asrol_pedantic ≠ asrol.ado**: Despite claims of exact compatibility, there are still differences in:
   - Missing value handling in rolling windows
   - Standard deviation calculation edge cases
   - Treatment of irregular quarterly data

2. **Implementation Complexity**: The filtering order fix was correct but revealed that the underlying volatility calculations have deeper issues

3. **Performance Cost**: Now takes much longer to run (processes 2.3M observations for volatility vs 500K before)

## Lessons Learned

1. **"Exact replication" tools often aren't exact** - asrol_pedantic still has differences from Stata
2. **Fixing architecture doesn't guarantee better results** - The filtering order was wrong, but fixing it revealed worse underlying issues
3. **Incremental changes can make things worse** - Sometimes the original approach was closer to correct

## Status
- MS predictor precision: **WORSE** (40.96% vs 32.97% failures)
- Should revert these changes and try different approach
- asrol_pedantic is not the solution for this problem

## Files Modified
- `pyCode/Predictors/MS.py` - Added asrol_pedantic imports and calls, moved filtering logic
- Failed completely - recommend reverting

## Next Steps
- Revert to previous approach
- Consider that the original rolling_std might have been closer to correct
- Focus on other aspects of the MS calculation (quarterly aggregation logic, industry medians, etc.)