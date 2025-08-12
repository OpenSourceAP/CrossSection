# Mom6mJunk Superset Test Fix: tsfill + Forward Fill Logic

**Date**: 2025-08-08  
**Predictor**: Mom6mJunk  
**Issue**: 32.49% superset test failure (Python missing 127,269 Stata observations)  
**Result**: Fixed to 18.09% failure (14.4 percentage point improvement, recovered 56,409 observations)

## Problem Analysis

### Root Cause
The Python translation was **missing Stata's `tsfill` + forward fill logic**, which is critical for handling gaps in credit rating data.

**Stata Code (Lines 54-59)**:
```stata
xtset permno time_avail_m
tsfill
sort permno time_avail_m
foreach v of varlist credratciq {
    replace `v' = `v'[_n-1] if permno == permno[_n-1] & mi(`v') 
}
```

**Key Insight**: `tsfill` creates a complete balanced panel first, then forward fills ratings within permno groups.

### Specific Example: permno=10026, yyyymm=198907

**Data Gap in SP Ratings**:
- June 1989 (198906): credrat = 9
- **MISSING**: July-October 1989 (198907-198910)  
- November 1989 (198911): credrat = 0

**Stata Behavior**:
1. `tsfill` creates records for missing months (198907-198910)
2. Forward fill propagates June rating (credrat=9) to July-October
3. July 1989 gets credrat=9, qualifying as junk stock (9 ≤ 14)
4. Momentum calculated: Mom6mJunk = 0.279570

**Original Python Behavior**:
- No missing records created
- No rating available for July 1989
- Mom6mJunk = NaN (filtered out)

## Solution Implementation

### Fix 1: Forward fill credratciq only (PARTIAL)
```python
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()
```
**Result**: Minimal improvement (+417 observations)

### Fix 2: Forward fill BOTH credrat and credratciq (SUCCESSFUL)  
```python
# Forward fill BOTH SP ratings (credrat) and CIQ ratings (credratciq) within permno groups
# This replicates the effect of Stata's tsfill creating missing periods + forward fill
df['credrat'] = df.groupby('permno')['credrat'].ffill()
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()
```
**Result**: Major improvement (+56,409 observations, 14.4 percentage point reduction)

## Key Lessons

### 1. tsfill is Critical for Panel Data
- **Stata's `tsfill`** creates complete balanced panels before processing
- **Python equivalent** requires careful forward filling of ALL rating variables
- **Gap filling** is essential when rating data has missing periods

### 2. Forward Fill Order Matters
- Must forward fill **BEFORE** coalescing credit ratings
- Must fill **ALL** rating sources (both SP and CIQ), not just one
- **Timing**: Fill gaps → Coalesce → Apply business logic

### 3. Missing vs Missing Data Types
- **Actual missing data**: Ratings never existed for that time period
- **Gap data**: Ratings exist before/after but missing in specific months
- **Stata tsfill handles both**, Python must replicate this explicitly

### 4. Business Logic Understanding
- **Junk stocks defined as**: credrat ≤ 14 and credrat > 0  
- **Forward filled ratings** allow classification of stocks during rating gaps
- **Rating persistence** assumption: ratings remain valid until updated

## Validation Results

**Before Fix**:
- Python: 264,547 observations
- Superset failure: 32.49% (127,269 missing)
- Target obs (10026/198907): Missing

**After Fix**:
- Python: 328,709 observations  
- Superset failure: 18.09% (70,860 missing)
- Target obs (10026/198907): Present (0.27957) ✅

## Remaining Issues

**18.09% superset failure remains** - likely due to:
1. Different date ranges in rating data sources
2. Missing gvkey mappings for some permnos  
3. Other data availability differences

**Next Steps**: Focus on remaining 70,860 missing observations to further improve superset test.

## Code Pattern for Future Use

```python
# CRITICAL: Implement Stata's tsfill + forward fill logic
# Sort first
df = df.sort_values(['permno', 'time_avail_m'])

# Forward fill ALL rating variables within permno groups
df['credrat'] = df.groupby('permno')['credrat'].ffill()
df['credratciq'] = df.groupby('permno')['credratciq'].ffill()

# Then coalesce
df.loc[df['credrat'].isna(), 'credrat'] = df.loc[df['credrat'].isna(), 'credratciq']
```

This pattern should be applied to any predictor using credit ratings or other panel data with potential gaps.