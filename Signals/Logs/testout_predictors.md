# Predictor Validation Results

**Generated**: 2025-08-12 22:40:24

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 0.001
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| PatentsRD                 | ✅         | ✅       | ❌ (21.05%)  | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |

**Overall**: 0/1 available predictors passed validation
**Python CSVs**: 1/1 predictors have Python implementation

## Detailed Results

### PatentsRD

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 141420 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PatentsRD']

**Observations**:
- Stata:  671,832
- Python: 571,284
- Common: 530,412

**Precision1**: 0.023% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e-03)

**Missing Observations Sample**:
```
 index  permno  yyyymm  PatentsRD
     0   10006  198306          1
     1   10006  198307          1
     2   10006  198308          1
     3   10006  198309          1
     4   10006  198310          1
     5   10006  198311          1
     6   10006  198312          1
     7   10006  198401          1
     8   10006  198402          1
     9   10006  198403          1
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/530412 (0.023%)
- Stata standard deviation: 1.50e-02

---

