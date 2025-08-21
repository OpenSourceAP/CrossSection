# REV6 Extra Observations Analysis

## Problem
REV6.py creates 4,003,555 observations while Stata only creates 1,762,090 - more than double.

## Root Cause
The Python code has an incorrect fallback condition (lines 70-75 in REV6.py) that sets `tempRev = 0` when both `meanest` and `meanest_lag1` are missing but price data exists.

```python
# Lines 70-75 in REV6.py (INCORRECT)
both_meanest_missing = df['meanest'].isna() & df['meanest_lag1'].isna()
has_price_data = df['prc_lag1'].notna()
fallback_condition = both_meanest_missing & has_price_data

df.loc[fallback_condition, 'tempRev'] = 0.0
```

## Why This Is Wrong
1. In Stata, when `meanest` and `l.meanest` are both missing, the calculation `(meanest - l.meanest)/abs(l.prc)` produces a missing value (NaN), not 0.
2. This fallback creates ~2 million extra observations where all REV6 values equal 0.
3. These observations shouldn't exist because REV6 should be NaN when the underlying components are missing.

## Evidence
- Without fallback: 2,006,319 observations (closer to Stata's 1,762,090)
- With fallback: 4,003,555 observations 
- Extra observations: 1,997,236 (all have REV6 = 0)
- Python-only observations: 2,241,465 total, with 2,067,625 having REV6 = 0

## Additional Issues Found
Even without the fallback, Python still has ~244K more observations than Stata (2,006,319 vs 1,762,090). This suggests:
1. There may be upstream data differences in IBES processing
2. Or Stata's `savepredictor` macro may have additional filtering

## Fix Required
Remove lines 70-75 from REV6.py. The calculation should naturally produce NaN when meanest values are missing, matching Stata's behavior.