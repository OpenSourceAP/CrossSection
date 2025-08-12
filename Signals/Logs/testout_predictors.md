# Predictor Validation Results

**Generated**: 2025-08-12 12:52:31

**Configuration**:
- PTH_PERCENTILE: 1.0
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 0.1%
- TOL_DIFF_2: 1e-06
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Coskewness                | ✅         | ✅       | ✅           | ✅ (0.00%)    | ❌ (100th diff 4.5E-03)  |

**Overall**: 0/1 available predictors passed validation
**Python CSVs**: 1/1 predictors have Python implementation

## Detailed Results

### Coskewness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['Coskewness']

**Observations**:
- Stata:  4,609,158
- Python: 4,609,158
- Common: 4,609,158

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 0.1%)

**Precision2**: 100th percentile diff = 4.52e-03 (tolerance: < 1.00e-06)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4/4609158 (0.000%)
- Stata standard deviation: 3.83e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16558  201802 -0.219565 -0.223494  0.003929
1   16534  201801  1.158808  1.163328 -0.004520
2   16558  201801 -1.492818 -1.497080  0.004262
3   16566  201801  1.000350  1.004411 -0.004061
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   16534  201801  1.158808  1.163328 -0.004520
1   16558  201801 -1.492818 -1.497080  0.004262
2   16566  201801  1.000350  1.004411 -0.004061
3   16558  201802 -0.219565 -0.223494  0.003929
```

---

