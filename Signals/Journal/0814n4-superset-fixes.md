# 0814n4: Parallel Debug and Fix of 6 Superset Failures

## Overview
Worked on fixing 6 predictors with superset failures identified in Plan/0814n2-debug-log.md:
- Mom6mJunk, MomRev, PatentsRD, RDAbility, Recomm_ShortInterest, UpRecomm

Used parallel agents to diagnose issues simultaneously, then applied targeted fixes.

## Results Summary

### ✅ Successfully Fixed (2/6)
1. **MomRev**: PASSED (R² = 1.0000, 0.16% missing)
2. **UpRecomm**: PASSED (R² = 0.9990, 0.23% missing)

### ❌ Failed Fix Attempts (4/6)
3. **PatentsRD**: Attempted fastxtile fix - no improvement, still 21% superset failure
4. **Mom6mJunk**: Attempted CIQ overhaul - no improvement, still 18% superset failure  
5. **RDAbility**: Attempted rolling window fix - no improvement, still 1.43% superset + 10% precision failures
6. **Recomm_ShortInterest**: Diagnosed as upstream data issue - no fix attempted

## Successful Fixes (To Be Committed)

### MomRev - Complete Success
**Issue**: Superset failure due to incorrect tempMom36 condition
**Root Cause**: Stata code shows `tempMom36 == 1` but actual Stata behavior uses `tempMom36 <= 2`
**Fix**: Changed condition from `== 1` to `<= 2` in MomRev.py
**Result**: Perfect replication (R² = 1.0000, 0.000% precision errors)

### UpRecomm - Complete Success  
**Issue**: 3.19% superset failure from aggressive filtering
**Root Cause**: Python was dropping observations with missing lag values instead of keeping them with UpRecomm=0
**Fix**: Removed `df = df[df['ireccd_lag'].notna()]` filter - boolean logic handles NaN correctly
**Result**: Excellent replication (R² = 0.9990, 0.02% precision errors)

## Failed Fix Attempts (To Be Reverted)

### PatentsRD - Failed Attempt
**Issue**: 21% superset failure + fastxtile creating only 2 categories instead of 3
**Attempted Fix**: Replaced pd.qcut with rank-based approach in utils/stata_fastxtile.py
**Result**: No improvement - still 21% superset failure, Python still creates no PatentsRD=1 values
**Conclusion**: fastxtile wasn't the root cause, deeper signal assignment logic issue

### Mom6mJunk - Failed Attempt  
**Issue**: 18% superset failure from CIQ data processing differences
**Attempted Fix**: 
- Eliminated 12-month expansion loop
- Used actual time_avail_m from ratingdate conversion
- Implemented tsfill logic with complete balanced panels
**Result**: No improvement - still 18% superset failure (70k missing observations)
**Conclusion**: Upstream data differences require DataDownloads leg investigation

### RDAbility - Failed Attempt
**Issue**: Large superset + precision failures  
**Attempted Fix**: Changed `min_periods=4` to `min_periods=6` in rolling window calculation
**Result**: No meaningful improvement - still 1.43% superset failure + 10.38% precision failures
**Conclusion**: Rolling window wasn't the root cause, other calculation differences exist

### Recomm_ShortInterest - No Fix Attempted
**Issue**: 57% superset failure 
**Diagnosis**: Population differences at quintile calculation stage - Python has 29% more obs in 2007m4
**Conclusion**: Upstream data pipeline differences, not Predictors leg issue

## Key Insights

### What Works: Simple Logic Fixes
- **MomRev**: Wrong condition in if statement - easy targeted fix
- **UpRecomm**: Aggressive filter removal - easy targeted fix
- **Pattern**: Clear logical errors with obvious fixes tend to succeed

### What Doesn't Work: Complex Data Processing Changes
- **PatentsRD**: Assumed fastxtile was the issue - wrong assumption
- **Mom6mJunk**: Assumed CIQ processing was wrong - likely upstream data issue
- **RDAbility**: Assumed rolling window was main issue - other problems exist
- **Pattern**: Complex overhauls of data processing rarely solve superset failures

### Missing Data Handling Success Pattern
Discovered pattern: Aggressive filters often cause superset failures
- **Wrong**: `df = df[df['lag_col'].notna()]` - drops valid observations  
- **Right**: Let boolean logic handle NaN - `(condition & col.notna()).astype(int)`
- **Stata Behavior**: Keeps observations with missing lags, sets result=0

## Action Plan

### Immediate
1. Commit only MomRev + UpRecomm fixes (proven successful)
2. Revert failed attempts in PatentsRD, Mom6mJunk, RDAbility
3. Keep utils/stata_fastxtile.py changes - may help other predictors

### Next Investigation
4. Focus on simple logic errors first, not complex data processing overhauls
5. For remaining failures, investigate upstream DataDownloads leg differences
6. Audit other predictors for aggressive filtering patterns (UpRecomm pattern)

## Files To Commit
- `Predictors/MomRev.py` - Fixed tempMom36 condition  
- `Predictors/UpRecomm.py` - Removed aggressive filter
- `utils/stata_fastxtile.py` - Improved fastxtile (may help other predictors)

## Files To Revert
- `Predictors/PatentsRD.py` - No actual changes made
- `Predictors/Mom6mJunk.py` - Revert CIQ processing changes
- `Predictors/RDAbility.py` - Revert rolling window changes

## Success Rate
- 2/6 predictors successfully fixed (33%)
- 4/6 predictors failed attempts - need different approach
- **Lesson**: Simple, targeted logic fixes work; complex data overhauls don't