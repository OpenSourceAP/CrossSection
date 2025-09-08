# Predictor Validation Results

**Generated**: 2025-09-08 13:00:15

**Configuration**:
- TOL_SUPERSET: 1.0%
- TOL_NUMROWS: 5.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 1%
- EXTREME_Q: 0.999
- TOL_DIFF_2: 0.1
- TOL_TSTAT: 0.2
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2    | T-stat     |
|---------------------------|------------|------------|---------------|--------------|---------------|------------|
| CustomerMomentum          | ✅         | ✅ (0.05%) | ✅ (-0.0%)   | ✅ (0.6%)     | ❌ (7.1E-01)   | SKIP       |

**Overall**: 0/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 0
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### CustomerMomentum

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has -0.04% rows vs Stata)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA (Skipped - use --tstat to enable)

**Observations**:
- Stata:  356,600
- Python: 356,474
- Common: 356,426

**Precision1**: 0.633% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 7.11e-01 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    356426.0000 |    356426.0000 |    356426.0000 |    356426.0000 |
| mean       |         0.0114 |         0.0114 |       5.77e-05 |       5.18e-04 |
| std        |         0.1115 |         0.1116 |         0.0065 |         0.0584 |
| min        |        -0.9813 |        -0.9813 |        -0.4973 |        -4.4621 |
| 25%        |        -0.0407 |        -0.0407 |      -2.00e-10 |      -1.79e-09 |
| 50%        |         0.0102 |         0.0102 |         0.0000 |         0.0000 |
| 75%        |         0.0606 |         0.0606 |       1.00e-10 |       8.97e-10 |
| max        |         8.1384 |         8.1384 |         0.8190 |         7.3487 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9993 * stata
- **R-squared**: 0.9966
- **N observations**: 356,426

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.61e-05 |     1.10e-05 |      6.0295 |     0.000 |
| Slope       |       0.9993 |     9.78e-05 |  10218.5321 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2256/356426 (0.633%)
- Stata standard deviation: 1.11e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   85265  202411  0.062140  0.038684  0.023456
1   87299  202411  0.045972  0.041455  0.004517
2   85265  202410  0.011421  0.017658 -0.006237
3   87299  202410 -0.021951 -0.017611 -0.004340
4   85265  202409  0.014368  0.015946 -0.001578
5   85265  202408 -0.048965 -0.060372  0.011407
6   87299  202408  0.002821 -0.004346  0.007167
7   85265  202407  0.027211  0.051186 -0.023974
8   87299  202407  0.036055  0.041312 -0.005257
9   85265  202406 -0.015085 -0.051199  0.036114
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   86313  202007  0.809589 -0.009438  0.819028
1   86313  202004  0.865116  0.208269  0.656847
2   90508  201304  0.688312  0.067991  0.620321
3   13887  202007  0.559422  0.013403  0.546019
4   68187  202007  0.590193  0.044175  0.546019
5   90508  201210  0.457268 -0.084444  0.541712
6   86013  200804  0.613770  0.101695  0.512075
7   22089  202208  0.018277  0.515593 -0.497316
8   86313  202208 -0.101489  0.395827 -0.497316
9   22128  202208 -0.090914  0.406401 -0.497316
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

