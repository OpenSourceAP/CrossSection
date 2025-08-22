# Placebo Validation Results

**Generated**: 2025-08-22 10:39:31

**Configuration**:
- TOL_SUPERSET: 0.0%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| pchquick                  | ✅         | ✅       | ❌ (9.39%)   | ✅ (8.80%)    | ❌ (99th diff NAN)       |
| rd_sale_q                 | ✅         | ✅       | ❌ (0.24%)   | ✅ (0.17%)    | ✅ (99th diff 9.3E-05)   |
| AssetGrowth_q             | ✅         | ✅       | ❌ (0.16%)   | ✅ (1.32%)    | ✅ (99th diff 1.7E-02)   |
| sgr_q                     | ✅         | ✅       | ❌ (0.12%)   | ✅ (0.09%)    | ✅ (99th diff 5.3E-04)   |
| cfpq                      | ✅         | ✅       | ❌ (0.09%)   | ✅ (0.42%)    | ✅ (99th diff 5.8E-08)   |
| EPq                       | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.74%)    | ✅ (99th diff 2.9E-03)   |
| tang_q                    | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| EBM_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-08)   |
| AMq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |
| BMq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| CFq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-08)   |
| AssetTurnover             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-09)   |
| pchdepr                   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| depr                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.7E-09)   |
| roic                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-23)   |
| salerec                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-08)   |
| secured                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.4E-08)   |
| securedind                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| sgr                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| salecash                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.5E-09)   |
| quick                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| rd_sale                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-09)   |
| cashdebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| saleinv                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| AbnormalAccrualsPercent   | ❌         | NA      | NA          | NA           | NA                      |
| AccrualQuality            | ❌         | NA      | NA          | NA           | NA                      |
| AccrualQualityJune        | ❌         | NA      | NA          | NA           | NA                      |
| AssetLiquidityBook        | ❌         | NA      | NA          | NA           | NA                      |
| AssetLiquidityBookQuart   | ❌         | NA      | NA          | NA           | NA                      |
| AssetLiquidityMarket      | ❌         | NA      | NA          | NA           | NA                      |
| AssetLiquidityMarketQuart | ❌         | NA      | NA          | NA           | NA                      |
| AssetTurnover_q           | ❌         | NA      | NA          | NA           | NA                      |
| BetaBDLeverage            | ❌         | NA      | NA          | NA           | NA                      |
| BetaDimson                | ❌         | NA      | NA          | NA           | NA                      |
| BetaSquared               | ❌         | NA      | NA          | NA           | NA                      |
| BidAskTAQ                 | ❌         | NA      | NA          | NA           | NA                      |
| BookLeverageQuarterly     | ❌         | NA      | NA          | NA           | NA                      |
| BrandCapital              | ❌         | NA      | NA          | NA           | NA                      |
| CBOperProfLagAT           | ❌         | NA      | NA          | NA           | NA                      |
| CBOperProfLagAT_q         | ❌         | NA      | NA          | NA           | NA                      |
| CapTurnover               | ❌         | NA      | NA          | NA           | NA                      |
| CapTurnover_q             | ❌         | NA      | NA          | NA           | NA                      |
| ChNCOA                    | ❌         | NA      | NA          | NA           | NA                      |
| ChNCOL                    | ❌         | NA      | NA          | NA           | NA                      |
| ChPM                      | ❌         | NA      | NA          | NA           | NA                      |
| ChangeRoA                 | ❌         | NA      | NA          | NA           | NA                      |
| ChangeRoE                 | ❌         | NA      | NA          | NA           | NA                      |
| DelSTI                    | ❌         | NA      | NA          | NA           | NA                      |
| DelayAcct                 | ❌         | NA      | NA          | NA           | NA                      |
| DelayNonAcct              | ❌         | NA      | NA          | NA           | NA                      |
| DivYield                  | ❌         | NA      | NA          | NA           | NA                      |
| DivYieldAnn               | ❌         | NA      | NA          | NA           | NA                      |
| DownsideBeta              | ❌         | NA      | NA          | NA           | NA                      |
| ETR                       | ❌         | NA      | NA          | NA           | NA                      |
| EarningsConservatism      | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPersistence       | ❌         | NA      | NA          | NA           | NA                      |
| EarningsPredictability    | ❌         | NA      | NA          | NA           | NA                      |
| EarningsSmoothness        | ❌         | NA      | NA          | NA           | NA                      |
| EarningsTimeliness        | ❌         | NA      | NA          | NA           | NA                      |
| EarningsValueRelevance    | ❌         | NA      | NA          | NA           | NA                      |
| EntMult_q                 | ❌         | NA      | NA          | NA           | NA                      |
| FRbook                    | ❌         | NA      | NA          | NA           | NA                      |
| FailureProbability        | ❌         | NA      | NA          | NA           | NA                      |
| FailureProbabilityJune    | ❌         | NA      | NA          | NA           | NA                      |
| ForecastDispersionLT      | ❌         | NA      | NA          | NA           | NA                      |
| GPlag                     | ❌         | NA      | NA          | NA           | NA                      |
| GPlag_q                   | ❌         | NA      | NA          | NA           | NA                      |
| GrGMToGrSales             | ❌         | NA      | NA          | NA           | NA                      |
| GrSaleToGrReceivables     | ❌         | NA      | NA          | NA           | NA                      |
| IdioVolCAPM               | ❌         | NA      | NA          | NA           | NA                      |
| IdioVolQF                 | ❌         | NA      | NA          | NA           | NA                      |
| IntrinsicValue            | ❌         | NA      | NA          | NA           | NA                      |
| KZ                        | ❌         | NA      | NA          | NA           | NA                      |
| KZ_q                      | ❌         | NA      | NA          | NA           | NA                      |
| LaborforceEfficiency      | ❌         | NA      | NA          | NA           | NA                      |
| Leverage_q                | ❌         | NA      | NA          | NA           | NA                      |
| NetDebtPrice_q            | ❌         | NA      | NA          | NA           | NA                      |
| NetPayoutYield_q          | ❌         | NA      | NA          | NA           | NA                      |
| OPLeverage_q              | ❌         | NA      | NA          | NA           | NA                      |
| OScore_q                  | ❌         | NA      | NA          | NA           | NA                      |
| OperProfLag               | ❌         | NA      | NA          | NA           | NA                      |
| OperProfLag_q             | ❌         | NA      | NA          | NA           | NA                      |
| OperProfRDLagAT           | ❌         | NA      | NA          | NA           | NA                      |
| OperProfRDLagAT_q         | ❌         | NA      | NA          | NA           | NA                      |
| OrgCapNoAdj               | ❌         | NA      | NA          | NA           | NA                      |
| PM                        | ❌         | NA      | NA          | NA           | NA                      |
| PM_q                      | ❌         | NA      | NA          | NA           | NA                      |
| PS_q                      | ❌         | NA      | NA          | NA           | NA                      |
| PayoutYield_q             | ❌         | NA      | NA          | NA           | NA                      |
| RD_q                      | ❌         | NA      | NA          | NA           | NA                      |
| ResidualMomentum6m        | ❌         | NA      | NA          | NA           | NA                      |
| RetNOA                    | ❌         | NA      | NA          | NA           | NA                      |
| RetNOA_q                  | ❌         | NA      | NA          | NA           | NA                      |
| ReturnSkewCAPM            | ❌         | NA      | NA          | NA           | NA                      |
| ReturnSkewQF              | ❌         | NA      | NA          | NA           | NA                      |
| SP_q                      | ❌         | NA      | NA          | NA           | NA                      |
| Tax_q                     | ❌         | NA      | NA          | NA           | NA                      |
| WW                        | ❌         | NA      | NA          | NA           | NA                      |
| WW_Q                      | ❌         | NA      | NA          | NA           | NA                      |
| ZScore                    | ❌         | NA      | NA          | NA           | NA                      |
| ZScore_q                  | ❌         | NA      | NA          | NA           | NA                      |
| betaCC                    | ❌         | NA      | NA          | NA           | NA                      |
| betaCR                    | ❌         | NA      | NA          | NA           | NA                      |
| betaNet                   | ❌         | NA      | NA          | NA           | NA                      |
| betaRC                    | ❌         | NA      | NA          | NA           | NA                      |
| betaRR                    | ❌         | NA      | NA          | NA           | NA                      |
| currat                    | ❌         | NA      | NA          | NA           | NA                      |
| fgr5yrNoLag               | ❌         | NA      | NA          | NA           | NA                      |
| grcapx1y                  | ❌         | NA      | NA          | NA           | NA                      |
| nanalyst                  | ❌         | NA      | NA          | NA           | NA                      |
| pchcurrat                 | ❌         | NA      | NA          | NA           | NA                      |
| pchgm_pchsale             | ❌         | NA      | NA          | NA           | NA                      |
| pchsaleinv                | ❌         | NA      | NA          | NA           | NA                      |
| roavol                    | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 10/24 available placebos passed validation
**Python CSVs**: 24/114 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 43 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,584,345
- Common: 2,584,335

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.91e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |      -1.42e-05 |      -6.09e-07 |
| std        |        23.2697 |        23.2697 |         0.0149 |       6.42e-04 |
| min        |       -33.6391 |       -33.6391 |       -14.6042 |        -0.6276 |
| 25%        |         0.6615 |         0.6615 |      -2.52e-08 |      -1.08e-09 |
| 50%        |         1.4017 |         1.4017 |       9.83e-12 |       4.22e-13 |
| 75%        |         3.2088 |         3.2088 |       2.53e-08 |       1.09e-09 |
| max        |     11549.4230 |     11549.4229 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,335

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.30e-05 |     9.41e-06 |     -1.3758 |     0.169 |
| Slope       |       1.0000 |     3.99e-07 |    2.50e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      AMq
     0   10515  199604 1.248122
     1   10515  199605 3.213409
     2   10515  199606 2.957797
     3   11545  199706 0.413572
     4   11545  199707 0.356745
     5   11545  199708 0.320093
     6   12750  198212 0.281005
     7   12750  198301 0.291609
     8   12750  198302 0.268788
     9   12837  198004 2.109993
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2584335 (0.000%)
- Stata standard deviation: 2.33e+01

---

### AssetGrowth_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 3619 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth_q']

**Observations**:
- Stata:  2,303,961
- Python: 2,324,239
- Common: 2,300,342

**Precision1**: 1.320% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.67e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |         0.1631 |            inf |            inf |            inf |
| std        |         3.5137 |            N/A |            N/A |            N/A |
| min        |        -1.0268 |        -1.0268 |      -616.8746 |      -175.5651 |
| 25%        |        -0.0281 |        -0.0281 |      -2.08e-09 |      -5.93e-10 |
| 50%        |         0.0624 |         0.0627 |      -4.46e-13 |      -1.27e-13 |
| 75%        |         0.1821 |         0.1829 |       2.08e-09 |       5.93e-10 |
| max        |      2788.4187 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + -inf * stata
- **R-squared**: nan
- **N observations**: 2,300,342

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetGrowth_q
     0   10011  199008       0.069888
     1   10027  198809       0.183796
     2   10031  198506       0.007827
     3   10031  198704       0.042602
     4   10042  198806       1.038125
     5   10051  198803      -0.296038
     6   10063  198806       0.146139
     7   10076  198806       0.096943
     8   10082  198506       0.210135
     9   10092  198806       0.081955
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30368/2300342 (1.320%)
- Stata standard deviation: 3.51e+00

---

### AssetTurnover

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover']

**Observations**:
- Stata:  2,796,921
- Python: 2,811,446
- Common: 2,796,897

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.94e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2786 |       1.87e-04 |       7.15e-07 |
| std        |       261.1058 |       261.1093 |         0.0658 |       2.52e-04 |
| min        |         0.0000 |        -0.0000 |        -1.8130 |        -0.0069 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,897

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.15e-04 |     3.93e-05 |      2.9340 |     0.003 |
| Slope       |       1.0000 |     1.50e-07 |    6.65e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetTurnover
     0   12373  202406       0.145598
     1   12373  202407       0.145598
     2   12373  202408       0.145598
     3   12373  202409       0.145598
     4   12373  202410       0.145598
     5   12373  202411       0.145598
     6   12373  202412       0.145598
     7   12373  202501       0.145598
     8   12373  202502       0.145598
     9   12373  202503       0.145598
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2796897 (0.001%)
- Stata standard deviation: 2.61e+02

---

### BMq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 41 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BMq']

**Observations**:
- Stata:  2,568,885
- Python: 2,652,980
- Common: 2,568,844

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |        -0.5919 |        -0.5919 |      -1.41e-06 |      -1.47e-06 |
| std        |         0.9608 |         0.9608 |         0.0014 |         0.0015 |
| min        |       -13.7467 |       -13.7467 |        -0.8206 |        -0.8540 |
| 25%        |        -1.1088 |        -1.1088 |      -1.09e-08 |      -1.13e-08 |
| 50%        |        -0.5062 |        -0.5062 |      -3.86e-12 |      -4.01e-12 |
| 75%        |         0.0109 |         0.0109 |       1.09e-08 |       1.13e-08 |
| max        |         6.6128 |         6.6128 |         0.7888 |         0.8210 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,568,844

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.90e-06 |     1.05e-06 |     -1.8021 |     0.072 |
| Slope       |       1.0000 |     9.34e-07 |    1.07e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm       BMq
     0   10515  199604  0.039689
     1   10515  199605  0.985382
     2   10515  199606  0.902494
     3   11545  199706 -0.990834
     4   11545  199707 -1.138644
     5   11545  199708 -1.247053
     6   12750  198212 -1.871727
     7   12750  198301 -1.834686
     8   12750  198302 -1.916179
     9   12837  198004  0.137666
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 41/2568844 (0.002%)
- Stata standard deviation: 9.61e-01

---

### CFq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 31 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CFq']

**Observations**:
- Stata:  2,797,878
- Python: 2,797,875
- Common: 2,797,847

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |      -2.99e-06 |      -2.55e-06 |
| std        |         1.1714 |         1.1714 |         0.0034 |         0.0029 |
| min        |      -917.6409 |      -917.6409 |        -2.7228 |        -2.3243 |
| 25%        |         0.0039 |         0.0039 |      -5.35e-10 |      -4.57e-10 |
| 50%        |         0.0195 |         0.0195 |      -1.43e-13 |      -1.22e-13 |
| 75%        |         0.0369 |         0.0369 |       5.33e-10 |       4.55e-10 |
| max        |       163.1038 |       163.1038 |         1.5098 |         1.2889 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,797,847

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.03e-06 |     2.05e-06 |     -1.4788 |     0.139 |
| Slope       |       1.0000 |     1.75e-06 | 570954.6173 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      CFq
     0   11545  199706 0.013777
     1   11545  199707 0.011884
     2   11545  199708 0.010663
     3   12837  198004 0.027496
     4   12837  198005 0.016803
     5   16965  201812 0.096766
     6   16965  201901 0.083703
     7   16965  201902 0.078968
     8   21346  197001 0.026762
     9   21346  197002 0.025521
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 200/2797847 (0.007%)
- Stata standard deviation: 1.17e+00

---

### EBM_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 54 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EBM_q']

**Observations**:
- Stata:  2,497,505
- Python: 2,497,500
- Common: 2,497,451

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.5320 |         0.5302 |        -0.0018 |      -8.56e-06 |
| std        |       210.6166 |       207.7943 |         4.0061 |         0.0190 |
| min        |   -135089.5600 |   -134017.4161 |     -6189.2265 |       -29.3862 |
| 25%        |         0.1800 |         0.1800 |      -1.36e-08 |      -6.44e-11 |
| 50%        |         0.5004 |         0.5004 |      -1.65e-11 |      -7.81e-14 |
| 75%        |         0.9606 |         0.9606 |       1.35e-08 |       6.43e-11 |
| max        |    215285.7300 |    209096.5035 |      1072.1439 |         5.0905 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0054 + 0.9865 * stata
- **R-squared**: 0.9998
- **N observations**: 2,497,451

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0054 |       0.0018 |      3.0083 |     0.003 |
| Slope       |       0.9865 |     8.48e-06 | 116274.9025 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    EBM_q
     0   10515  199604 1.030155
     1   10515  199605 1.891978
     2   10515  199606 1.808921
     3   11545  199706 0.477123
     4   11545  199707 0.421310
     5   11545  199708 0.383889
     6   12750  198212 0.099635
     7   12750  198301 0.103646
     8   12750  198302 0.095039
     9   12837  198004 1.263025
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 44/2497451 (0.002%)
- Stata standard deviation: 2.11e+02

---

### EPq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 101 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EPq']

**Observations**:
- Stata:  1,893,938
- Python: 1,908,337
- Common: 1,893,837

**Precision1**: 0.740% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.92e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.89e+06 |       1.89e+06 |       1.89e+06 |       1.89e+06 |
| mean       |         0.0273 |         0.0273 |       7.01e-06 |       7.00e-05 |
| std        |         0.1001 |         0.1021 |         0.0209 |         0.2086 |
| min        |         0.0000 |         0.0000 |       -14.6293 |      -146.1051 |
| 25%        |         0.0107 |         0.0107 |      -3.65e-10 |      -3.64e-09 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0297 |         0.0297 |       3.65e-10 |       3.65e-09 |
| max        |        35.0386 |        35.0386 |        19.1968 |       191.7226 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9986 * stata
- **R-squared**: 0.9582
- **N observations**: 1,893,837

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.62e-05 |     1.57e-05 |      2.9362 |     0.003 |
| Slope       |       0.9986 |     1.52e-04 |   6588.8327 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      EPq
     0   10198  198709 0.005705
     1   10515  199604 0.005181
     2   10515  199605 0.005181
     3   10515  199606 0.005181
     4   11321  199406 0.041526
     5   11545  199706 0.014092
     6   11545  199707 0.014227
     7   11545  199708 0.014227
     8   11651  198902 0.000409
     9   11843  198803 0.040014
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 14015/1893837 (0.740%)
- Stata standard deviation: 1.00e-01

---

### cashdebt

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cashdebt']

**Observations**:
- Stata:  3,267,782
- Python: 3,284,937
- Common: 3,267,782

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.21e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.27e+06 |       3.27e+06 |       3.27e+06 |       3.27e+06 |
| mean       |         0.3051 |         0.3051 |      -1.49e-06 |      -3.25e-08 |
| std        |        45.8671 |        45.8671 |       7.58e-04 |       1.65e-05 |
| min        |    -10248.0000 |    -10248.0000 |        -0.3728 |        -0.0081 |
| 25%        |         0.0096 |         0.0096 |      -3.26e-09 |      -7.11e-11 |
| 50%        |         0.1142 |         0.1142 |         0.0000 |         0.0000 |
| 75%        |         0.2625 |         0.2625 |       3.26e-09 |       7.11e-11 |
| max        |     13971.0000 |     13971.0000 |         0.0877 |         0.0019 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,267,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.49e-06 |     4.19e-07 |     -3.5652 |     0.000 |
| Slope       |       1.0000 |     9.14e-09 |    1.09e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3267782 (0.000%)
- Stata standard deviation: 4.59e+01

---

### cfpq

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1941 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,255,041
- Common: 2,250,681

**Precision1**: 0.422% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.76e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       4.88e-04 |       5.27e-04 |       3.90e-05 |       5.69e-05 |
| std        |         0.6863 |         0.6875 |         0.0526 |         0.0766 |
| min        |      -278.1893 |      -278.1893 |       -32.1553 |       -46.8523 |
| 25%        |        -0.0227 |        -0.0228 |      -2.93e-10 |      -4.27e-10 |
| 50%        |         0.0111 |         0.0111 |      -1.23e-13 |      -1.79e-13 |
| 75%        |         0.0389 |         0.0389 |       2.91e-10 |       4.25e-10 |
| max        |       250.7536 |       250.7536 |        26.9720 |        39.2998 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9987 * stata
- **R-squared**: 0.9942
- **N observations**: 2,250,681

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.96e-05 |     3.50e-05 |      1.1311 |     0.258 |
| Slope       |       0.9987 |     5.11e-05 |  19558.0887 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      cfpq
     0   10027  198809 -0.176309
     1   10031  198506  0.040552
     2   10031  198704  0.050945
     3   10051  198803  0.014210
     4   10063  198806 -0.051760
     5   10076  198806 -0.159924
     6   10082  198506 -0.038278
     7   10092  198806 -0.015793
     8   10136  198804 -0.184637
     9   10136  198810 -0.367341
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 9502/2250681 (0.422%)
- Stata standard deviation: 6.86e-01

---

### depr

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['depr']

**Observations**:
- Stata:  3,462,713
- Python: 3,547,200
- Common: 3,462,689

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -5.28e-06 |      -5.91e-07 |
| std        |         8.9356 |         8.9356 |         0.0028 |       3.14e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.1795 |         0.0201 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,689

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.26e-06 |     1.51e-06 |     -3.4855 |     0.000 |
| Slope       |       1.0000 |     1.69e-07 |    5.93e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     depr
     0   12373  202406 0.029963
     1   12373  202407 0.029963
     2   12373  202408 0.029963
     3   12373  202409 0.029963
     4   12373  202410 0.029963
     5   12373  202411 0.029963
     6   12373  202412 0.029963
     7   12373  202501 0.029963
     8   12373  202502 0.029963
     9   12373  202503 0.029963
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/3462689 (0.001%)
- Stata standard deviation: 8.94e+00

---

### pchdepr

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 24 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchdepr']

**Observations**:
- Stata:  3,050,498
- Python: 3,235,524
- Common: 3,050,474

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         0.4972 |         0.4971 |      -8.88e-05 |      -2.30e-06 |
| std        |        38.5914 |        38.5913 |         0.0375 |       9.70e-04 |
| min        |       -75.5903 |       -75.5903 |       -18.3420 |        -0.4753 |
| 25%        |        -0.0906 |        -0.0906 |      -2.22e-09 |      -5.74e-11 |
| 50%        |         0.0251 |         0.0251 |         0.0000 |         0.0000 |
| 75%        |         0.1646 |         0.1646 |       2.22e-09 |       5.76e-11 |
| max        |     15513.7030 |     15513.7034 |         1.3903 |         0.0360 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,050,474

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.83e-05 |     2.14e-05 |     -4.1186 |     0.000 |
| Slope       |       1.0000 |     5.56e-07 |    1.80e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchdepr
     0   12373  202406 0.091209
     1   12373  202407 0.091209
     2   12373  202408 0.091209
     3   12373  202409 0.091209
     4   12373  202410 0.091209
     5   12373  202411 0.091209
     6   12373  202412 0.091209
     7   12373  202501 0.091209
     8   12373  202502 0.091209
     9   12373  202503 0.091209
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 48/3050474 (0.002%)
- Stata standard deviation: 3.86e+01

---

### pchquick

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 313488 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['pchquick']

**Observations**:
- Stata:  3,339,639
- Python: 3,311,547
- Common: 3,026,151

**Precision1**: 8.797% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = nan (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.03e+06 |       2.77e+06 |       2.77e+06 |       2.77e+06 |
| mean       |         0.3284 |            N/A |            N/A |            N/A |
| std        |        45.1046 |            N/A |            N/A |            N/A |
| min        |      -111.5194 |           -inf |           -inf |           -inf |
| 25%        |        -0.1881 |        -0.2127 |      -3.51e-09 |      -7.79e-11 |
| 50%        |         0.0000 |        -0.0225 |       2.22e-16 |       4.92e-18 |
| 75%        |         0.1533 |         0.1836 |       3.56e-09 |       7.88e-11 |
| max        |     19726.1780 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,768,475

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchquick
     0   10000  198704       0.0
     1   10000  198705       0.0
     2   10000  198706       0.0
     3   10000  198707       0.0
     4   10000  198708       0.0
     5   10000  198709       0.0
     6   10000  198710       0.0
     7   10000  198711       0.0
     8   10000  198712       0.0
     9   10000  198801       0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 266221/3026151 (8.797%)
- Stata standard deviation: 4.51e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   12385  202608     NaN    0.0   NaN
1   19655  202608     NaN    0.0   NaN
2   21259  202608     NaN    0.0   NaN
3   81073  202608     NaN    0.0   NaN
4   86349  202608     NaN    0.0   NaN
5   90729  202608     NaN    0.0   NaN
6   91582  202608     NaN    0.0   NaN
7   12385  202607     NaN    0.0   NaN
8   19655  202607     NaN    0.0   NaN
9   21259  202607     NaN    0.0   NaN
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10002  199606     NaN    0.0   NaN
1   10002  199607     NaN    0.0   NaN
2   10002  199608     NaN    0.0   NaN
3   10002  199609     NaN    0.0   NaN
4   10002  199610     NaN    0.0   NaN
5   10002  199611     NaN    0.0   NaN
6   10002  199612     NaN    0.0   NaN
7   10002  199701     NaN    0.0   NaN
8   10002  199702     NaN    0.0   NaN
9   10002  199703     NaN    0.0   NaN
```

---

### quick

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['quick']

**Observations**:
- Stata:  3,065,278
- Python: 3,625,095
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         2.7309 |         2.7309 |      -2.05e-06 |      -3.62e-08 |
| std        |        56.6440 |        56.6440 |       9.36e-04 |       1.65e-05 |
| min        |       -41.2750 |       -41.2750 |        -0.4710 |        -0.0083 |
| 25%        |         0.8507 |         0.8507 |      -2.56e-08 |      -4.52e-10 |
| 50%        |         1.3264 |         1.3264 |         0.0000 |         0.0000 |
| 75%        |         2.2630 |         2.2630 |       2.57e-08 |       4.54e-10 |
| max        |     25204.0000 |     25204.0000 |       1.67e-04 |       2.94e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.05e-06 |     5.35e-07 |     -3.8297 |     0.000 |
| Slope       |       1.0000 |     9.44e-09 |    1.06e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3065278 (0.000%)
- Stata standard deviation: 5.66e+01

---

### rd_sale

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale']

**Observations**:
- Stata:  1,207,848
- Python: 1,254,467
- Common: 1,207,848

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.06e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         5.1262 |         5.1262 |      -5.92e-09 |      -3.17e-11 |
| std        |       186.9904 |       186.9904 |       5.03e-06 |       2.69e-08 |
| min        |     -1037.3235 |     -1037.3235 |        -0.0013 |      -7.13e-06 |
| 25%        |         0.0151 |         0.0151 |      -8.68e-10 |      -4.64e-12 |
| 50%        |         0.0509 |         0.0509 |      -5.55e-17 |      -2.97e-19 |
| 75%        |         0.1546 |         0.1546 |       8.73e-10 |       4.67e-12 |
| max        |     42070.6680 |     42070.6667 |       7.27e-04 |       3.89e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,207,848

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.41e-08 |     3.94e-09 |     16.2719 |     0.000 |
| Slope       |       1.0000 |     2.11e-11 |    4.75e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1207848 (0.000%)
- Stata standard deviation: 1.87e+02

---

### rd_sale_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1362 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale_q']

**Observations**:
- Stata:  566,115
- Python: 604,987
- Common: 564,753

**Precision1**: 0.167% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.27e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    564753.0000 |    564748.0000 |    564748.0000 |    564748.0000 |
| mean       |         7.6820 |            inf |            inf |            inf |
| std        |       183.4064 |            N/A |            N/A |            N/A |
| min        |     -3937.0000 |     -3937.0000 |     -1397.9160 |        -7.6220 |
| 25%        |         0.0468 |         0.0468 |      -2.11e-09 |      -1.15e-11 |
| 50%        |         0.1118 |         0.1118 |      -2.78e-17 |      -1.51e-19 |
| 75%        |         0.2509 |         0.2509 |       2.00e-09 |       1.09e-11 |
| max        |     31684.3340 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 564,748

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm  rd_sale_q
     0   10019  199909   0.604538
     1   10019  199910   0.604538
     2   10019  199911   0.604538
     3   10160  199208   0.223301
     4   10216  199712   0.002466
     5   10342  199006   0.027609
     6   10354  199006   0.003271
     7   10406  199306   0.013386
     8   10406  199406   0.006334
     9   10419  199103   0.013106
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 942/564753 (0.167%)
- Stata standard deviation: 1.83e+02

---

### roic

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roic']

**Observations**:
- Stata:  3,409,380
- Python: 3,410,772
- Common: 3,409,380

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.38e-23 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.41e+06 |       3.41e+06 |       3.41e+06 |       3.41e+06 |
| mean       |       1.87e+13 |            inf |            inf |            inf |
| std        |       5.82e+15 |            N/A |            N/A |            N/A |
| min        |      -3.62e+17 |      -3.91e+16 |      -3.40e+16 |        -5.8459 |
| 25%        |        -0.0121 |        -0.0121 |      -1.87e-09 |      -3.22e-25 |
| 50%        |         0.0586 |         0.0586 |         0.0000 |         0.0000 |
| 75%        |         0.1262 |         0.1262 |       1.86e-09 |       3.20e-25 |
| max        |       1.79e+18 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 3,409,380

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 492/3409380 (0.014%)
- Stata standard deviation: 5.82e+15

---

### salecash

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['salecash']

**Observations**:
- Stata:  3,583,392
- Python: 3,616,983
- Common: 3,583,392

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.55e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.58e+06 |       3.58e+06 |       3.58e+06 |       3.58e+06 |
| mean       |       107.6003 |       107.6001 |      -1.50e-04 |      -5.72e-08 |
| std        |      2627.3839 |      2627.3839 |         0.0798 |       3.04e-05 |
| min        |     -1591.6364 |     -1591.6364 |       -43.5883 |        -0.0166 |
| 25%        |         2.2471 |         2.2471 |      -1.37e-07 |      -5.21e-11 |
| 50%        |         8.4673 |         8.4673 |         0.0000 |         0.0000 |
| 75%        |        30.7168 |        30.7168 |       1.35e-07 |       5.12e-11 |
| max        |    519704.0000 |    519704.0000 |         0.1507 |       5.74e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,583,392

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.50e-04 |     4.22e-05 |     -3.5625 |     0.000 |
| Slope       |       1.0000 |     1.60e-08 |    6.23e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/3583392 (0.000%)
- Stata standard deviation: 2.63e+03

---

### saleinv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['saleinv']

**Observations**:
- Stata:  2,730,607
- Python: 3,616,983
- Common: 2,730,607

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.12e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |        61.9969 |        61.9969 |       1.38e-07 |       3.95e-11 |
| std        |      3492.9321 |      3492.9321 |       1.12e-04 |       3.22e-08 |
| min        |    -14573.0000 |    -14573.0000 |        -0.0233 |      -6.68e-06 |
| 25%        |         4.6053 |         4.6053 |      -1.57e-07 |      -4.49e-11 |
| 50%        |         7.6793 |         7.6793 |         0.0000 |         0.0000 |
| 75%        |        17.8215 |        17.8215 |       1.55e-07 |       4.45e-11 |
| max        |       1.05e+06 |       1.05e+06 |         0.0387 |       1.11e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,730,607

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.03e-07 |     6.74e-08 |      5.9744 |     0.000 |
| Slope       |       1.0000 |     1.93e-11 |    5.18e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2730607 (0.000%)
- Stata standard deviation: 3.49e+03

---

### salerec

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['salerec']

**Observations**:
- Stata:  3,451,784
- Python: 3,616,983
- Common: 3,451,784

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.11e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.45e+06 |       3.45e+06 |       3.45e+06 |       3.45e+06 |
| mean       |        16.3739 |        16.3744 |       5.33e-04 |       2.54e-06 |
| std        |       209.4212 |       209.4212 |         0.0834 |       3.98e-04 |
| min        |    -21796.0000 |    -21796.0000 |        -0.6092 |        -0.0029 |
| 25%        |         3.6746 |         3.6749 |      -1.08e-07 |      -5.16e-10 |
| 50%        |         5.9289 |         5.9293 |         0.0000 |         0.0000 |
| 75%        |         9.1589 |         9.1598 |       1.08e-07 |       5.14e-10 |
| max        |     47246.0000 |     47246.0000 |        17.2986 |         0.0826 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,451,784

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.36e-04 |     4.50e-05 |     11.8914 |     0.000 |
| Slope       |       1.0000 |     2.14e-07 |    4.66e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 168/3451784 (0.005%)
- Stata standard deviation: 2.09e+02

---

### secured

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['secured']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.1995 |         0.1995 |       3.89e-06 |       1.13e-05 |
| std        |         0.3454 |         0.3454 |         0.0015 |         0.0042 |
| min        |      -7.96e-05 |      -7.96e-05 |        -0.1626 |        -0.4709 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.3028 |         0.3028 |         0.0000 |         0.0000 |
| max        |        48.7452 |        48.7452 |         0.7243 |         2.0969 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.20e-06 |     8.80e-07 |      5.9060 |     0.000 |
| Slope       |       1.0000 |     2.21e-06 | 453400.1353 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 156/3624363 (0.004%)
- Stata standard deviation: 3.45e-01

---

### securedind

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['securedind']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.4092 |         0.4092 |       2.65e-05 |       5.39e-05 |
| std        |         0.4917 |         0.4917 |         0.0063 |         0.0128 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0338 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0338 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.60e-05 |     4.31e-06 |     13.0100 |     0.000 |
| Slope       |       0.9999 |     6.73e-06 | 148495.0598 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3624363 (0.004%)
- Stata standard deviation: 4.92e-01

---

### sgr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr']

**Observations**:
- Stata:  3,231,761
- Python: 3,303,855
- Common: 3,231,761

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.88e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |         0.7025 |         0.7025 |       3.84e-08 |       8.18e-10 |
| std        |        46.9281 |        46.9281 |         0.0026 |       5.61e-05 |
| min        |      -237.0000 |      -237.0000 |        -1.0899 |        -0.0232 |
| 25%        |        -0.0210 |        -0.0210 |      -2.50e-09 |      -5.32e-11 |
| 50%        |         0.0863 |         0.0863 |         0.0000 |         0.0000 |
| 75%        |         0.2252 |         0.2252 |       2.53e-09 |       5.39e-11 |
| max        |     12739.0000 |     12739.0000 |         0.7897 |         0.0168 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,231,761

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.48e-08 |     1.46e-06 |      0.0238 |     0.981 |
| Slope       |       1.0000 |     3.12e-08 |    3.21e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3231761 (0.001%)
- Stata standard deviation: 4.69e+01

---

### sgr_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2977 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,525,939
- Common: 2,454,724

**Precision1**: 0.086% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.26e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.45e+06 |       2.45e+06 |       2.45e+06 |       2.45e+06 |
| mean       |         1.0553 |            N/A |            N/A |            N/A |
| std        |       286.5321 |            N/A |            N/A |            N/A |
| min        |     -3092.0000 |           -inf |           -inf |           -inf |
| 25%        |        -0.0373 |        -0.0374 |      -2.64e-09 |      -9.22e-12 |
| 50%        |         0.0794 |         0.0797 |         0.0000 |         0.0000 |
| 75%        |         0.2228 |         0.2240 |       2.66e-09 |       9.29e-12 |
| max        |    251440.0000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,454,682

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm     sgr_q
     0   10011  199008  0.126970
     1   10027  198809 -0.021801
     2   10031  198506  1.197602
     3   10051  198803 -0.050746
     4   10063  198806  1.493302
     5   10076  198806 -0.497865
     6   10082  198506  0.402820
     7   10084  198803 -0.074579
     8   10092  198806  0.887324
     9   10093  198806 -0.263912
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2115/2454724 (0.086%)
- Stata standard deviation: 2.87e+02

---

### tang_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 84 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['tang_q']

**Observations**:
- Stata:  1,675,098
- Python: 1,675,074
- Common: 1,675,014

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.54e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6565 |      -1.92e-06 |      -5.58e-06 |
| std        |         0.3446 |         0.3446 |       6.89e-04 |         0.0020 |
| min        |        -0.4077 |        -0.4077 |        -0.4243 |        -1.2314 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.83e-11 |       8.21e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       158.7656 |         0.0988 |         0.2866 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,675,014

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.52e-06 |     1.15e-06 |     -2.2008 |     0.028 |
| Slope       |       1.0000 |     1.54e-06 | 647478.5288 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   tang_q
     0   11545  199706 0.812887
     1   11545  199707 0.812887
     2   11545  199708 0.812887
     3   12373  202306 0.611982
     4   12373  202307 0.611982
     5   12373  202308 0.611982
     6   12373  202309 0.610183
     7   12373  202310 0.610183
     8   12373  202311 0.610183
     9   12373  202312 0.620340
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1675014 (0.005%)
- Stata standard deviation: 3.45e-01

---

### AbnormalAccrualsPercent

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AbnormalAccrualsPercent.csv

---

### AccrualQuality

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AccrualQuality.csv

---

### AccrualQualityJune

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AccrualQualityJune.csv

---

### AssetLiquidityBook

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AssetLiquidityBook.csv

---

### AssetLiquidityBookQuart

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AssetLiquidityBookQuart.csv

---

### AssetLiquidityMarket

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AssetLiquidityMarket.csv

---

### AssetLiquidityMarketQuart

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AssetLiquidityMarketQuart.csv

---

### AssetTurnover_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AssetTurnover_q.csv

---

### BetaBDLeverage

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaBDLeverage.csv

---

### BetaDimson

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaDimson.csv

---

### BetaSquared

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BetaSquared.csv

---

### BidAskTAQ

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BidAskTAQ.csv

---

### BookLeverageQuarterly

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BookLeverageQuarterly.csv

---

### BrandCapital

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/BrandCapital.csv

---

### CBOperProfLagAT

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/CBOperProfLagAT.csv

---

### CBOperProfLagAT_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/CBOperProfLagAT_q.csv

---

### CapTurnover

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/CapTurnover.csv

---

### CapTurnover_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/CapTurnover_q.csv

---

### ChNCOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChNCOA.csv

---

### ChNCOL

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChNCOL.csv

---

### ChPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChPM.csv

---

### ChangeRoA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChangeRoA.csv

---

### ChangeRoE

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ChangeRoE.csv

---

### DelSTI

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DelSTI.csv

---

### DelayAcct

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DelayAcct.csv

---

### DelayNonAcct

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DelayNonAcct.csv

---

### DivYield

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DivYield.csv

---

### DivYieldAnn

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DivYieldAnn.csv

---

### DownsideBeta

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/DownsideBeta.csv

---

### ETR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ETR.csv

---

### EarningsConservatism

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsConservatism.csv

---

### EarningsPersistence

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsPersistence.csv

---

### EarningsPredictability

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsPredictability.csv

---

### EarningsSmoothness

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsSmoothness.csv

---

### EarningsTimeliness

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsTimeliness.csv

---

### EarningsValueRelevance

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EarningsValueRelevance.csv

---

### EntMult_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/EntMult_q.csv

---

### FRbook

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FRbook.csv

---

### FailureProbability

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FailureProbability.csv

---

### FailureProbabilityJune

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FailureProbabilityJune.csv

---

### ForecastDispersionLT

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ForecastDispersionLT.csv

---

### GPlag

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GPlag.csv

---

### GPlag_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GPlag_q.csv

---

### GrGMToGrSales

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GrGMToGrSales.csv

---

### GrSaleToGrReceivables

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/GrSaleToGrReceivables.csv

---

### IdioVolCAPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IdioVolCAPM.csv

---

### IdioVolQF

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IdioVolQF.csv

---

### IntrinsicValue

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IntrinsicValue.csv

---

### KZ

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/KZ.csv

---

### KZ_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/KZ_q.csv

---

### LaborforceEfficiency

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/LaborforceEfficiency.csv

---

### Leverage_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/Leverage_q.csv

---

### NetDebtPrice_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/NetDebtPrice_q.csv

---

### NetPayoutYield_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/NetPayoutYield_q.csv

---

### OPLeverage_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OPLeverage_q.csv

---

### OScore_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OScore_q.csv

---

### OperProfLag

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfLag.csv

---

### OperProfLag_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfLag_q.csv

---

### OperProfRDLagAT

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfRDLagAT.csv

---

### OperProfRDLagAT_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OperProfRDLagAT_q.csv

---

### OrgCapNoAdj

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OrgCapNoAdj.csv

---

### PM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PM.csv

---

### PM_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PM_q.csv

---

### PS_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PS_q.csv

---

### PayoutYield_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/PayoutYield_q.csv

---

### RD_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/RD_q.csv

---

### ResidualMomentum6m

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ResidualMomentum6m.csv

---

### RetNOA

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/RetNOA.csv

---

### RetNOA_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/RetNOA_q.csv

---

### ReturnSkewCAPM

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ReturnSkewCAPM.csv

---

### ReturnSkewQF

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ReturnSkewQF.csv

---

### SP_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/SP_q.csv

---

### Tax_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/Tax_q.csv

---

### WW

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/WW.csv

---

### WW_Q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/WW_Q.csv

---

### ZScore

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ZScore.csv

---

### ZScore_q

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ZScore_q.csv

---

### betaCC

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaCC.csv

---

### betaCR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaCR.csv

---

### betaNet

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaNet.csv

---

### betaRC

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaRC.csv

---

### betaRR

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/betaRR.csv

---

### currat

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/currat.csv

---

### fgr5yrNoLag

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/fgr5yrNoLag.csv

---

### grcapx1y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/grcapx1y.csv

---

### nanalyst

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/nanalyst.csv

---

### pchcurrat

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchcurrat.csv

---

### pchgm_pchsale

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchgm_pchsale.csv

---

### pchsaleinv

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/pchsaleinv.csv

---

### roavol

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/roavol.csv

---

