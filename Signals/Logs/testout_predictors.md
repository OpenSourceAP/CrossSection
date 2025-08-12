# Predictor Validation Results

**Generated**: 2025-08-12 16:05:35

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
| AbnormalAccruals          | ✅         | ✅       | ✅ (0.68%)   | ❌ (27.95%)   | ❌ (99th diff 5.2E-02)   |

**Overall**: 0/1 available predictors passed validation
**Python CSVs**: 1/1 predictors have Python implementation

## Detailed Results

### AbnormalAccruals

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AbnormalAccruals']

**Observations**:
- Stata:  2,570,664
- Python: 2,567,830
- Common: 2,553,227

**Precision1**: 27.951% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.22e-02 (tolerance: < 1.00e-03)

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 713656/2553227 (27.951%)
- Stata standard deviation: 1.61e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   29946  202609  0.108293  0.092957  0.015336
1   12366  202608  0.139485  0.146414 -0.006929
2   13142  202608 -0.125493 -0.145704  0.020211
3   14033  202608  1.382135  1.391868 -0.009733
4   15623  202608 -0.091212 -0.093782  0.002570
5   16632  202608 -0.026517 -0.029087  0.002570
6   19655  202608 -0.036532 -0.038729  0.002197
7   22092  202608  0.014588  0.016372 -0.001784
8   23681  202608 -0.003675 -0.001505 -0.002170
9   24252  202608  0.088683  0.090385 -0.001702
```

**Largest Differences**:
```
   permno  yyyymm    python    stata      diff
0   79702  201712 -2.383081 -1.50314 -0.879941
1   79702  201801 -2.383081 -1.50314 -0.879941
2   79702  201802 -2.383081 -1.50314 -0.879941
3   79702  201803 -2.383081 -1.50314 -0.879941
4   79702  201804 -2.383081 -1.50314 -0.879941
5   79702  201805 -2.383081 -1.50314 -0.879941
6   79702  201806 -2.383081 -1.50314 -0.879941
7   79702  201807 -2.383081 -1.50314 -0.879941
8   79702  201808 -2.383081 -1.50314 -0.879941
9   79702  201809 -2.383081 -1.50314 -0.879941
```

---

