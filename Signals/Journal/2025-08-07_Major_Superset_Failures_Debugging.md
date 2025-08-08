# Major Superset Failures Debugging - August 7, 2025

## Summary
Fixed 6 predictors with superset failures >25%, recovering millions of missing observations.

## Key Lessons Learned

### 1. Monthly Expansion Logic (AbnormalAccruals: 91.72% → 0.65%)
- **Problem**: `row_id % 12` operated on global index, not per-record expansion
- **Fix**: Explicit loop to create 12 copies of each annual record with correct month offsets
- **Lesson**: Index-based operations can be deceptive - verify the actual grouping logic

### 2. Missing Data Handling in Screens (AnalystValue: 51.46% → 0.22%)  
- **Problem**: `abs(FROE1) <= 1` failed when FROE1 is NULL; Stata treats NULL comparisons differently
- **Fix**: Added `| pl.col("FROE1").is_null()` to allow NULL values through screens
- **Secondary**: Fixed ceq_ave calculation when l12_ceq is NULL by falling back to current ceq
- **Lesson**: Stata's missing value logic ≠ Python's - NULL handling requires explicit conditions

### 3. Calendar vs Position-based Lags (MomVol: 100.00% → 0.003%)
- **Problem**: Using `shift()` instead of proper sorted calendar-based lags like Stata's `l.ret`
- **Fix**: Ensured sorting before lag operations and used proper window functions
- **Lesson**: Stata's lag operators are calendar-aware, not just position-based

### 4. Merge Strategy Impact (AOP, AnnouncementReturn)
- **Problem**: Using `how="inner"` eliminated observations that should be kept
- **Fix**: Changed to `how="left"` and handled missing link dates properly  
- **Lesson**: Merge strategies have massive impact on observation counts - verify join logic carefully