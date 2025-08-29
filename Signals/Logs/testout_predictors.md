# Predictor Validation Results

**Generated**: 2025-08-28 19:06:24

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

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| RDAbility*                | ✅         | ✅ (0.02%) | ✅ (+4.4%)   | ❌ (4.3%)     | ❌ (2.2E+00)             | ❌ (-0.64)  |

**Overall**: 1/1 available predictors passed validation
  - Natural passes: 0
  - Overridden passes: 1
**Python CSVs**: 1/1 predictors have Python implementation
\* = Manual override applied (see Predictors/overrides.yaml for details)

## Detailed Results

### RDAbility

**Status**: ✅ PASSED (with override)

**Override Applied**:
- Reviewed on: 2025-08-28
- Reviewed by: ac
- Details: Given the complicated nature of this predictor (many regressions with many missing values), the 4.3% Precision1 failure rate is amazing. I think we actually improved the replication a bit, since the long-short t-stat is higher by a bit.

**Test Results**:
- Test 1 - Superset check: ✅ PASSED
- Test 2 - NumRows check: ✅ PASSED (Python has +4.43% rows vs Stata)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED
- Test 5 - T-stat check: NA

**Observations**:
- Stata:  173,266
- Python: 180,944
- Common: 173,240

**Precision1**: 4.336% obs with std_diff >= 1.00e-02 (tolerance: < 1%)

**Precision2**: 100th percentile diff = 2.17e+00 (tolerance: < 1.00e-01)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    173240.0000 |    173240.0000 |    173240.0000 |    173240.0000 |
| mean       |         0.4685 |         0.4644 |        -0.0040 |      -7.50e-04 |
| std        |         5.3534 |         5.2908 |         0.7769 |         0.1451 |
| min        |      -170.7315 |      -170.7315 |       -25.1031 |        -4.6892 |
| 25%        |        -0.2961 |        -0.2951 |      -1.56e-07 |      -2.91e-08 |
| 50%        |         0.4038 |         0.4001 |       5.57e-10 |       1.04e-10 |
| 75%        |         1.3891 |         1.3673 |       1.58e-07 |       2.94e-08 |
| max        |        83.8592 |        83.8592 |        35.2219 |         6.5793 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0064 + 0.9778 * stata
- **R-squared**: 0.9789
- **N observations**: 173,240

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0064 |       0.0019 |      3.4395 |     0.001 |
| Slope       |       0.9778 |     3.45e-04 |   2837.9578 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 7512/173240 (4.336%)
- Stata standard deviation: 5.35e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   14033  202608  0.379405  0.192091  0.187314
1   14033  202607  0.379405  0.192091  0.187314
2   14033  202606  0.379405  0.192091  0.187314
3   14033  202605  0.379405  0.192091  0.187314
4   14245  202605  0.943359  0.997209 -0.053850
5   14432  202605  0.304188  0.448311 -0.144123
6   14668  202605  0.619375  0.359465  0.259910
7   15059  202605  0.805267 -4.663055  5.468322
8   16533  202605 -0.130891 -0.232203  0.101312
9   82670  202605  0.300767  0.394679 -0.093913
```

**Largest Differences**:
```
   permno  yyyymm     python      stata       diff
0   79283  200206 -24.396323 -59.618244  35.221921
1   79283  200207 -24.396323 -59.618244  35.221921
2   79283  200208 -24.396323 -59.618244  35.221921
3   79283  200209 -24.396323 -59.618244  35.221921
4   79283  200210 -24.396323 -59.618244  35.221921
5   79283  200211 -24.396323 -59.618244  35.221921
6   79283  200212 -24.396323 -59.618244  35.221921
7   79283  200301 -24.396323 -59.618244  35.221921
8   79283  200302 -24.396323 -59.618244  35.221921
9   79283  200303 -24.396323 -59.618244  35.221921
```

**Largest Differences Before 1950**:
```
No data before 1950
```

---

