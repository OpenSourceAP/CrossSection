# Mom*.py Scripts stata_lag Improvement Plan

## Overview
Systematic improvement of all 15 Mom*.py scripts to use `stata_lag` from `utils/stata_replication.py` for consistent, calendar-validated lag operations.

## Current Status
All 15 Mom*.py scripts are **PASSING tests** (per Logs/testout_predictors 0824.md):
- Mom12m, Mom12mOffSeason, Mom6m, Mom6mJunk (override), MomOffSeason
- MomOffSeason06YrPlus, MomOffSeason11YrPlus, MomOffSeason16YrPlus
- MomRev, MomSeason, MomSeason06YrPlus, MomSeason11YrPlus, MomSeason16YrPlus
- MomSeasonShort, MomVol

## Phase 1: Priority Scripts (5 scripts)

### 1. Mom12m.py
- **Current**: Uses basic `df.groupby('permno')['ret'].shift(i)` for 11 lags
- **Improvement**: Replace with `stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [1,2,3,4,5,6,7,8,9,10,11])`
- **Benefit**: Calendar validation prevents invalid lags

### 2. MomRev.py  
- **Current**: Uses basic `shift()` for 29 different lags (1-5, 13-36)
- **Improvement**: Two `stata_multi_lag()` calls: `[1,2,3,4,5]` and `[13,14,15,...,36]`
- **Benefit**: Replaces 29 manual shift operations with 2 validated calls

### 3. MomVol.py
- **Current**: Complex manual calendar-based approach (lines 49-58, ~20 lines)
- **Improvement**: Replace with `stata_multi_lag(df_pd, 'permno', 'time_avail_m', 'ret', [1,2,3,4,5])`
- **Benefit**: Reduces complexity from 20+ lines to 2 lines

### 4. MomSeason.py
- **Current**: Manual calendar lookups for lags 23,35,47,59 (~30 lines, lines 26-47)
- **Improvement**: Replace with `stata_multi_lag(df, 'permno', 'time_avail_m', 'ret', [23,35,47,59])`
- **Benefit**: Dramatic code simplification

### 5. Mom12mOffSeason.py
- **Status**: Need to examine current implementation
- **Expected**: Similar issues to Mom12m.py
- **Improvement**: Apply same stata_multi_lag approach

## Phase 2: Remaining Scripts (10 scripts)

### Scripts to examine and improve:
- Mom6m.py (already uses stata_multi_lag - ✅ GOOD)
- Mom6mJunk.py
- MomOffSeason.py
- MomOffSeason06YrPlus.py, MomOffSeason11YrPlus.py, MomOffSeason16YrPlus.py
- MomSeason06YrPlus.py, MomSeason11YrPlus.py, MomSeason16YrPlus.py
- MomSeasonShort.py

### Common Improvement Patterns:
1. **Basic shift() replacement**: For scripts using `df.groupby().shift()`
2. **Manual calendar logic**: For scripts with complex date-based lookups
3. **Polars/pandas hybrid**: Some scripts mix both - standardize approach

## Testing Strategy
After each script improvement:
```bash
cd pyCode/
python3 utils/test_predictors.py --predictors [ScriptName]
```

**Success Criteria:**
- Maintain PASSING test status
- All 4 tests (Columns, Superset, Precision1, Precision2) should pass
- Accept minor precision differences as improvement benefit

## Implementation Timeline

### Week 1: Phase 1 (5 priority scripts)
- Day 1-2: Mom12m.py and MomRev.py
- Day 3-4: MomVol.py and MomSeason.py  
- Day 5: Mom12mOffSeason.py

### Week 2: Phase 2 (remaining 10 scripts)
- Systematic examination and improvement
- Group similar scripts for batch improvements
- Final validation testing

## Benefits
1. **Consistency**: All Mom scripts use same lag approach
2. **Maintainability**: Centralized lag logic in utils
3. **Robustness**: Calendar validation prevents invalid lags
4. **Code Quality**: Dramatic reduction in code complexity
5. **Future-proofing**: Easy to modify lag logic across all scripts

## Risks & Mitigation
- **Risk**: Minor numerical differences due to improved lag validation  
- **Mitigation**: Accept passing tests even with small precision changes
- **Risk**: Breaking currently working scripts
- **Mitigation**: Test each script individually before proceeding