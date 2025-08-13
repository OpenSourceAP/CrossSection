# PatentsRD Superset Failure Diagnosis

**Date**: 2025-01-13  
**Issue**: PatentsRD failing superset test - Python missing 23.11% (155,256) observations vs Stata

## Diagnostic Process

### Test Results
- **Stata**: 671,832 observations (530,748 zeros + 141,084 ones)
- **Python**: 571,284 observations (ALL zeros, NO ones!)
- **Missing**: 100,548 observations (14.97%)
- **Superset failure**: 23.11% > 1.0% threshold

### Root Cause Identified

**The Critical Issue**: PatentsRD tertile sorting completely fails
1. **PatentsRD tertile sorting**: `maincat 3 (high): 0` - NO observations get classified as "high" PatentsRD
2. **Signal assignment logic**:
   - `PatentsRD = 1` → small companies with high PatentsRD (`sizecat==1 & maincat==3`)
   - `PatentsRD = 0` → small companies with low PatentsRD (`sizecat==1 & maincat==1`)
   - Since NO observations get `maincat==3`, NO observations get `PatentsRD=1`
3. **Missing observations**: These are the observations that should get `PatentsRD=1` but get `NaN` and are dropped

### Detailed Findings

**June Processing Results**:
- Total June observations after filtering: 154,868
- Valid `tempPatentsRD` ratios: 77,248
- Invalid `tempPatentsRD` (NaN): 77,620

**Sorting Results**:
- `maincat 1` (low): 60,058 observations
- `maincat 2` (mid): 17,190 observations  
- `maincat 3` (high): **0 observations** ← THE PROBLEM
- `maincat NaN`: 77,620 observations

**Signal Assignment**:
- Small & High PatentsRD (should get 1): **0** ← Should be ~141K based on Stata
- Small & Low PatentsRD (should get 0): 47,607
- Everything else gets NaN and is dropped

### Technical Analysis

**Issue Location**: Lines 104-127 in `PatentsRD.py` - the PatentsRD tertile sorting
```python
# PatentsRD categories (3 groups)
patents_cuts = []
for time_month, group in df.groupby('time_avail_m'):
    valid_group = group.dropna(subset=['tempPatentsRD'])
    
    if len(valid_group) > 0:
        try:
            valid_group['maincat'] = fastxtile(valid_group['tempPatentsRD'], n=3)
            # Problem: fastxtile not correctly creating tertiles
```

**Suspected Cause**: 
- `fastxtile` function not working correctly for `tempPatentsRD` values
- All values being assigned to lower tertiles (1 and 2), none to tertile 3
- This could be due to:
  - Extreme distribution of `tempPatentsRD` values (all zeros?)
  - `fastxtile` implementation issue
  - Data preprocessing affecting the distribution

### Focus Areas for Fix

1. **Investigate `tempPatentsRD` distribution**: Are all values zero or very similar?
2. **Debug `fastxtile` behavior**: Is it correctly creating 3 equal-sized groups?
3. **Compare with Stata sorting**: How does Stata's `xtile` handle this distribution?

### Missing Observations Traced

The 100,548 missing observations are specifically the companies that:
- Are small (`sizecat == 1`) 
- Have high PatentsRD efficiency (`tempPatentsRD` in top tertile)
- Should get `PatentsRD = 1`
- Are currently getting `maincat = NaN` or wrong `maincat`, leading to `PatentsRD = NaN`
- Get dropped by the final `dropna()` step

## Next Steps

**Immediate**: Debug the tertile sorting logic in PatentsRD.py lines 104-127
**Focus**: Why are NO observations getting `maincat == 3` when ~141K should based on Stata output

**Key insight**: This is NOT a data availability issue - it's a sorting/classification logic error in the Python translation.