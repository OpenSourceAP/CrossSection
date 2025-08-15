# FastXtile Edge Cases in PatentsRD - 0815n1

## Context
Working on PatentsRD superset failure debugging. Fixed main CEQ filter issue (missing value handling) but still have 13.72% observations missing vs Stata. Root cause identified as fastxtile behavior differences.

## The Problem
Stata's `egen maincat = fastxtile(tempPatentsRD), by(time_avail_m) n(3)` vs our Python fastxtile produce different results in later years.

### Expected vs Actual MainCat Distribution

**Early years (1977-2007) - Works correctly:**
- MainCat 1: ~630-1100 obs (low tercile)
- MainCat 2: ~80-380 obs (middle tercile) 
- MainCat 3: ~440-700 obs (high tercile)

**Later years (2008+) - Edge cases:**
- **200806**: MainCat 2: 1665, MainCat 3: 1 (missing category 1!)
- **200906**: MainCat 1: 1564 only (missing categories 2,3!)
- **201006**: MainCat 1: 1561 only (missing categories 2,3!)
- **201106**: MainCat 2: 1501, MainCat 3: 2 (missing category 1!)

## Impact
- Total observations after filters: 154,893 (matches Stata perfectly)
- Observations with valid PatentsRD signal: 48,572 (Python) vs ~56,000 expected (Stata)
- Missing ~89k observations = 13% superset failure

## Root Cause Analysis

### Stata FastXtile Behavior
Stata's `fastxtile` apparently has special handling for:
1. **Sparse data**: When there are limited unique values
2. **Extreme distributions**: When data is heavily skewed
3. **Missing value treatment**: How it handles NaN in the ranking

### Python FastXtile Behavior
Our current implementation:
1. Drops missing tempPatentsRD observations first
2. Ranks only valid observations 
3. Forces exactly 3 groups even when inappropriate
4. Merges categories back to full dataset

## Hypothesis
Stata's fastxtile may:
1. **Include missing values** in the ranking process differently
2. **Adjust group boundaries** when data is sparse
3. **Use different tie-breaking** for identical values
4. **Handle edge cases** where perfect terciles aren't possible

## Evidence from Debug Output
- **Size categories work fine**: 119,882 small vs 35,011 big (reasonable split)
- **MainCat assignment fails**: Creates incomplete 3-way splits in recent years
- **PatentsRD assignment**: Only assigns to (sizecat=1, maincat=1) and (sizecat=1, maincat=3)
- **Missing assignments**: sizecat=1,maincat=2 and all sizecat=2 get PatentsRD=NaN

## Next Steps
1. **Investigate Stata fastxtile source code** or documentation for edge case handling
2. **Modify Python fastxtile** to match Stata's behavior exactly
3. **Alternative**: Use quantile-based approach that guarantees 3 groups
4. **Test fix** with validation script

## Pattern Recognition
This is similar to other Stata translation traps:
- **Inequality operators**: Missing value handling differences  
- **Lag operators**: Position vs time-based differences
- **Fastxtile**: Ranking and grouping edge cases

## Status
- ✅ CEQ filter fixed (missing value handling)
- ❌ FastXtile edge cases remain (13% observations missing)
- Need to debug fastxtile behavior for sparse/skewed data