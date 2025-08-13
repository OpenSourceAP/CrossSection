# Precision Failure Pattern Analysis

## Context
Studying "ATTEMPTED" and "Skip for now" scripts (PS, MS, OrgCap) to understand common precision failures. All three scripts show significant Precision1 failures despite attempted fixes.

## Key Discovery: All Three Are Actually FAILING

**Tolerance Analysis:**
- `TOL_OBS_1 = 10%` (acceptable threshold)
- **OrgCap**: 14.23% > 10% → **FAILED** (not "major improvement")
- **PS**: 17.93% > 10% → **FAILED** 
- **MS**: 63.45% > 10% → **FAILED**

The plan's "improvements" are misleading - they're all still broken, just by different degrees.

## Common Functions and Patterns

### Shared Utilities:
1. **`fastxtile()`** - All three use for BM quintile calculations
2. **`save_predictor()`** - Standardized output saving
3. **Stata-compatible inequality operators** - Custom missing value handling

### Shared Logic Patterns:
1. **BM quintile sample selection**:
   - PS: highest quintile (`temp != 5`)
   - MS: lowest quintile (`BM_quintile == 1`) 
   - OrgCap: uses FF17 industry adjustment (similar grouping concept)

2. **Missing value handling**:
   - PS: `condition | lag_missing` pattern
   - MS: `stata_greater_than()`, `stata_less_than()` functions
   - OrgCap: simpler but still has recursive dependencies

3. **Complex data processing pipelines**:
   - 3-4 dataset merges each
   - Multiple transformation steps (logs, ratios, standardizations)
   - Time series operations with potential alignment issues
   - Industry/cross-sectional calculations with grouping

## Root Cause Hypothesis: Accumulated Precision Drift

### Not Just Missing Values - Architectural Problem

The **15-65% precision failures** suggest **systematic drift** rather than isolated bugs. Each script follows this error-prone pattern:

1. **Multiple data merges** → alignment precision loss
2. **BM calculations**: `log(ceq/mve_c)` → infinities/precision issues  
3. **Custom missing value functions** → subtle differences from Stata
4. **Time series operations** → calendar vs positional lag differences
5. **Grouping operations** → `fastxtile()`, industry medians compound errors

**Each step introduces small floating-point precision differences that compound through the pipeline.**

### Specific Vulnerabilities:

1. **`fastxtile()` complexity**: Multiple fallback mechanisms and tie-breaking methods that may not match Stata exactly
2. **BM quintile boundaries**: Small differences in quintile cutoffs cascade through entire sample selection
3. **Custom Stata compatibility functions**: `stata_greater_than()`, missing lag logic introduce systematic biases
4. **Industry grouping**: FF17, SIC2D median calculations accumulate group-wise errors
5. **Time series alignment**: Calendar-based vs position-based lags create observation mismatches

## Evidence Supporting This Theory:

1. **All three scripts still fail** despite extensive missing value fixes
2. **Precision failures are percentage-based** (14-65%), not isolated observations
3. **Complex scripts fail worse** (MS: 63% vs PS: 18% vs OrgCap: 14%)
4. **Early pipeline errors compound**: BM quintile selection affects everything downstream

## Implications:

This isn't just a "missing value" problem - it's **architectural precision decay**. The translation philosophy of line-by-line replication may be fundamentally flawed when **floating-point precision accumulates** through complex multi-step calculations.

**Need to focus on:**
1. **End-to-end numerical precision** rather than individual function accuracy
2. **Simplified processing pipelines** to reduce accumulation points
3. **Direct comparison at intermediate steps** to isolate where drift begins
4. **Alternative approaches** that minimize transformation chain length

## Next Steps:

1. **Bisection debugging**: Find exact step where precision diverges in one specific observation
2. **Intermediate validation**: Compare Python vs Stata at each major processing step
3. **Pipeline simplification**: Reduce transformation steps where possible
4. **Numerical stability review**: Focus on critical calculations like BM, quintiles, industry adjustments

Date: 2025-08-13