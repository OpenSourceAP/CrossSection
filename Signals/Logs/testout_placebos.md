# Placebo Validation Results

**Generated**: 2025-09-07 22:14:54

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
| betaCC                    | ✅         | ✅       | ❌ (28.95%)  | ❌ (61.57%)   | ❌ (99th diff 4.0E+00)   |
| betaCR                    | ✅         | ✅       | ❌ (28.95%)  | ❌ (56.47%)   | ❌ (99th diff 2.8E+00)   |
| betaRC                    | ✅         | ✅       | ❌ (28.17%)  | ❌ (96.95%)   | ❌ (99th diff 2.9E+00)   |
| betaRR                    | ✅         | ✅       | ❌ (28.17%)  | ❌ (92.29%)   | ❌ (99th diff 2.3E+00)   |
| betaNet                   | ✅         | ✅       | ❌ (28.15%)  | ❌ (63.11%)   | ❌ (99th diff 3.0E+00)   |
| AccrualQuality            | ✅         | ✅       | ❌ (8.54%)   | ❌ (90.69%)   | ❌ (99th diff 1.7E+00)   |
| AccrualQualityJune        | ✅         | ✅       | ❌ (8.25%)   | ❌ (89.54%)   | ❌ (99th diff 1.7E+00)   |
| EarningsConservatism      | ✅         | ✅       | ❌ (2.52%)   | ✅ (3.56%)    | ✅ (99th diff 6.4E-02)   |
| EarningsTimeliness        | ✅         | ✅       | ❌ (2.52%)   | ✅ (0.00%)    | ✅ (99th diff 4.8E-07)   |
| IdioVolQF                 | ✅         | ✅       | ❌ (0.77%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-08)   |
| ReturnSkewQF              | ✅         | ✅       | ❌ (0.77%)   | ✅ (0.90%)    | ✅ (99th diff 3.9E-07)   |
| ReturnSkewCAPM            | ✅         | ✅       | ❌ (0.76%)   | ✅ (2.91%)    | ✅ (99th diff 2.8E-01)   |
| DelayAcct                 | ✅         | ✅       | ❌ (0.67%)   | ❌ (89.59%)   | ✅ (99th diff 6.1E-01)   |
| DelayNonAcct              | ✅         | ✅       | ❌ (0.67%)   | ❌ (78.14%)   | ✅ (99th diff 2.9E-01)   |
| IdioVolCAPM               | ✅         | ✅       | ❌ (0.57%)   | ✅ (2.35%)    | ✅ (99th diff 7.2E-02)   |
| ForecastDispersionLT      | ✅         | ✅       | ❌ (0.21%)   | ✅ (0.09%)    | ✅ (99th diff 1.5E-07)   |
| fgr5yrNoLag               | ✅         | ✅       | ❌ (0.21%)   | ✅ (0.08%)    | ✅ (99th diff 1.4E-07)   |
| KZ_q                      | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| OperProfRDLagAT_q         | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.01%)    | ✅ (99th diff 6.6E-08)   |
| EntMult_q                 | ✅         | ✅       | ❌ (0.01%)   | ✅ (0.00%)    | ✅ (99th diff 4.7E-09)   |
| PS_q                      | ✅         | ✅       | ❌ (0.01%)   | ❌ (53.35%)   | ❌ (99th diff 3.2E+00)   |
| NetDebtPrice_q            | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.8E-08)   |
| Tax_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.6E-09)   |
| Leverage_q                | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-08)   |
| OPLeverage_q              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 7.7E-08)   |
| EBM_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.4E-08)   |
| AssetGrowth_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-08)   |
| AssetLiquidityMarketQuart | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.5E-07)   |
| AssetTurnover_q           | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.5E-09)   |
| CapTurnover_q             | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.0E-08)   |
| EPq                       | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.6E-08)   |
| sgr_q                     | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.0E-10)   |
| WW_Q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.6E-07)   |
| AssetLiquidityBookQuart   | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.4E-08)   |
| SP_q                      | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.0E-08)   |
| DownsideBeta              | ✅         | ✅       | ❌ (0.00%)   | ✅ (0.35%)    | ✅ (99th diff 1.2E-13)   |
| CBOperProfLagAT_q         | ✅         | ✅       | ✅ (0.00%)   | ❌ (26.66%)   | ❌ (99th diff 2.5E+00)   |
| cfpq                      | ✅         | ✅       | ✅ (0.00%)   | ❌ (11.98%)   | ✅ (99th diff 8.8E-01)   |
| BrandCapital              | ✅         | ✅       | ✅ (0.00%)   | ✅ (5.88%)    | ✅ (99th diff 8.2E-02)   |
| OperProfRDLagAT           | ✅         | ✅       | ✅ (0.00%)   | ✅ (4.54%)    | ✅ (99th diff 8.2E-02)   |
| roavol                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.93%)    | ✅ (99th diff 3.4E-02)   |
| BetaBDLeverage            | ✅         | ✅       | ✅ (0.00%)   | ✅ (2.21%)    | ✅ (99th diff 2.3E-01)   |
| pchcurrat                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (1.04%)    | ❌ (99th diff INF)       |
| nanalyst                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.26%)    | ✅ (99th diff 0.0E+00)   |
| FailureProbabilityJune    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.21%)    | ✅ (99th diff 1.7E-07)   |
| FailureProbability        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.11%)    | ✅ (99th diff 6.1E-08)   |
| EarningsPredictability    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.06%)    | ✅ (99th diff 5.6E-10)   |
| DivYieldAnn               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.03%)    | ✅ (99th diff 2.1E-08)   |
| NetPayoutYield_q          | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.5E-08)   |
| PayoutYield_q             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.02%)    | ✅ (99th diff 3.5E-08)   |
| roic                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 3.4E-23)   |
| GPlag_q                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.8E-08)   |
| GrSaleToGrReceivables     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 8.0E-10)   |
| ChangeRoA                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 6.6E-08)   |
| tang_q                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-07)   |
| CFq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.5E-08)   |
| DivYield                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 1.2E-08)   |
| RD_q                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.2E-08)   |
| GPlag                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.01%)    | ✅ (99th diff 5.6E-08)   |
| EarningsSmoothness        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-07)   |
| salerec                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-08)   |
| secured                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.4E-08)   |
| securedind                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| CBOperProfLagAT           | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.6E-08)   |
| ChNCOL                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.8E-08)   |
| DelSTI                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-07)   |
| ZScore_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.2E-08)   |
| BMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.2E-07)   |
| ChNCOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| pchdepr                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| ChangeRoE                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| GrGMToGrSales             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-09)   |
| OperProfLag               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-08)   |
| AssetLiquidityMarket      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-07)   |
| PM_q                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.9E-09)   |
| AssetLiquidityBook        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| ETR                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.2E-12)   |
| OperProfLag_q             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-05)   |
| RetNOA_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-11)   |
| WW                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.5E-10)   |
| depr                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.7E-09)   |
| AssetTurnover             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-09)   |
| RetNOA                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-19)   |
| pchgm_pchsale             | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.6E-09)   |
| sgr                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.9E-09)   |
| BookLeverageQuarterly     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-13)   |
| rd_sale_q                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.7E-09)   |
| AMq                       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.9E-08)   |
| LaborforceEfficiency      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.3E-09)   |
| CapTurnover               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.5E-08)   |
| salecash                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 6.5E-09)   |
| EarningsValueRelevance    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.4E-07)   |
| EarningsPersistence       | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.1E-07)   |
| BetaDimson                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-07)   |
| ZScore                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.3E-08)   |
| BidAskTAQ                 | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 8.0E-08)   |
| BetaSquared               | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 7.0E-08)   |
| currat                    | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.4E-08)   |
| quick                     | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.1E-08)   |
| ChPM                      | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 5.2E-09)   |
| rd_sale                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 4.1E-09)   |
| cashdebt                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.2E-09)   |
| saleinv                   | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 3.1E-09)   |
| PM                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.3E-09)   |
| KZ                        | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-09)   |
| pchquick                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 2.0E-09)   |
| pchsaleinv                | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 1.7E-09)   |
| OScore_q                  | ✅         | ✅       | ✅ (0.00%)   | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| AbnormalAccrualsPercent   | ❌         | NA      | NA          | NA           | NA                      |
| FRbook                    | ❌         | NA      | NA          | NA           | NA                      |
| IntrinsicValue            | ❌         | NA      | NA          | NA           | NA                      |
| OrgCapNoAdj               | ❌         | NA      | NA          | NA           | NA                      |
| ResidualMomentum6m        | ❌         | NA      | NA          | NA           | NA                      |
| grcapx1y                  | ❌         | NA      | NA          | NA           | NA                      |

**Overall**: 69/108 available placebos passed validation
**Python CSVs**: 108/114 placebos have Python implementation

## Detailed Results

### AMq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AMq']

**Observations**:
- Stata:  2,584,378
- Python: 2,809,455
- Common: 2,584,378

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.92e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |      -1.45e-05 |      -6.23e-07 |
| std        |        23.2695 |        23.2695 |         0.0149 |       6.42e-04 |
| min        |       -33.6391 |       -33.6391 |       -14.6042 |        -0.6276 |
| 25%        |         0.6615 |         0.6615 |      -2.52e-08 |      -1.08e-09 |
| 50%        |         1.4017 |         1.4017 |       9.63e-12 |       4.14e-13 |
| 75%        |         3.2088 |         3.2087 |       2.53e-08 |       1.09e-09 |
| max        |     11549.4230 |     11549.4229 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,378

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.33e-05 |     9.42e-06 |     -1.4108 |     0.158 |
| Slope       |       1.0000 |     4.00e-07 |    2.50e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 13/2584378 (0.001%)
- Stata standard deviation: 2.33e+01

---

### AccrualQuality

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 148568 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AccrualQuality']

**Observations**:
- Stata:  1,740,065
- Python: 1,789,393
- Common: 1,591,497

**Precision1**: 90.694% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.67e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.59e+06 |       1.59e+06 |       1.59e+06 |       1.59e+06 |
| mean       |         0.0448 |         0.0453 |       4.90e-04 |         0.0102 |
| std        |         0.0482 |         0.0484 |         0.0205 |         0.4248 |
| min        |       4.17e-04 |       4.58e-04 |        -1.2534 |       -25.9799 |
| 25%        |         0.0175 |         0.0179 |        -0.0043 |        -0.0891 |
| 50%        |         0.0309 |         0.0314 |       4.52e-05 |       9.37e-04 |
| 75%        |         0.0547 |         0.0555 |         0.0048 |         0.0993 |
| max        |         1.6265 |         1.6229 |         1.3339 |        27.6494 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0044 + 0.9123 * stata
- **R-squared**: 0.8281
- **N observations**: 1,591,497

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0044 |     2.17e-05 |    203.8558 |     0.000 |
| Slope       |       0.9123 |     3.29e-04 |   2769.0427 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQuality
     0   10001  200712        0.028371
     1   10001  200801        0.028371
     2   10001  200802        0.028371
     3   10001  200803        0.028371
     4   10001  200804        0.028371
     5   10001  200805        0.028371
     6   10001  201706        0.007970
     7   10001  201707        0.007970
     8   10001  201708        0.007970
     9   10001  201709        0.007970
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1443393/1591497 (90.694%)
- Stata standard deviation: 4.82e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   17144  202510  0.004839  0.007341 -0.002503
1   54114  202510  0.028960  0.028468  0.000493
2   57665  202510  0.022367  0.026395 -0.004027
3   61621  202510  0.019028  0.021003 -0.001974
4   83601  202510  0.051109  0.049397  0.001713
5   10501  202509  0.023631  0.024701 -0.001070
6   17144  202509  0.004839  0.007341 -0.002503
7   42585  202509  0.021855  0.019674  0.002181
8   47571  202509  0.087518  0.086237  0.001280
9   48347  202509  0.011106  0.016769 -0.005663
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79703  200406  1.405788  0.071864  1.333923
1   79703  200407  1.405788  0.071864  1.333923
2   79703  200408  1.405788  0.071864  1.333923
3   79703  200409  1.405788  0.071864  1.333923
4   79703  200410  1.405788  0.071864  1.333923
5   79703  200411  1.405788  0.071864  1.333923
6   79703  200412  1.405788  0.071864  1.333923
7   79703  200501  1.405788  0.071864  1.333923
8   79703  200502  1.405788  0.071864  1.333923
9   79703  200503  1.405788  0.071864  1.333923
```

---

### AccrualQualityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 147179 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['AccrualQualityJune']

**Observations**:
- Stata:  1,784,388
- Python: 1,815,384
- Common: 1,637,209

**Precision1**: 89.541% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.75e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.64e+06 |       1.64e+06 |       1.64e+06 |       1.64e+06 |
| mean       |         0.0455 |         0.0461 |       6.43e-04 |         0.0130 |
| std        |         0.0495 |         0.0501 |         0.0220 |         0.4434 |
| min        |       4.17e-04 |       4.58e-04 |        -1.2534 |       -25.3054 |
| 25%        |         0.0175 |         0.0179 |        -0.0041 |        -0.0835 |
| 50%        |         0.0311 |         0.0316 |       1.04e-05 |       2.09e-04 |
| 75%        |         0.0555 |         0.0563 |         0.0047 |         0.0945 |
| max        |         1.6265 |         1.6229 |         1.3339 |        26.9316 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9127 * stata
- **R-squared**: 0.8151
- **N observations**: 1,637,209

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     2.28e-05 |    201.9393 |     0.000 |
| Slope       |       0.9127 |     3.40e-04 |   2686.1392 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AccrualQualityJune
     0   10001  200712            0.028488
     1   10001  200801            0.028488
     2   10001  200802            0.028488
     3   10001  200803            0.028488
     4   10001  200804            0.028488
     5   10001  200805            0.028488
     6   10001  201706            0.007970
     7   10001  201707            0.007970
     8   10001  201708            0.007970
     9   10001  201709            0.007970
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1465979/1637209 (89.541%)
- Stata standard deviation: 4.95e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   17144  202510  0.004839  0.007341 -0.002503
1   57665  202510  0.022367  0.026395 -0.004027
2   61621  202510  0.019028  0.021003 -0.001974
3   83601  202510  0.051109  0.049397  0.001713
4   10501  202509  0.023631  0.024701 -0.001070
5   17144  202509  0.004839  0.007341 -0.002503
6   42585  202509  0.021855  0.019674  0.002181
7   47571  202509  0.087518  0.086237  0.001280
8   48347  202509  0.011106  0.016769 -0.005663
9   57665  202509  0.022367  0.026395 -0.004027
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   79703  200406  1.405788  0.071864  1.333923
1   79703  200407  1.405788  0.071864  1.333923
2   79703  200408  1.405788  0.071864  1.333923
3   79703  200409  1.405788  0.071864  1.333923
4   79703  200410  1.405788  0.071864  1.333923
5   79703  200411  1.405788  0.071864  1.333923
6   79703  200412  1.405788  0.071864  1.333923
7   79703  200501  1.405788  0.071864  1.333923
8   79703  200502  1.405788  0.071864  1.333923
9   79703  200503  1.405788  0.071864  1.333923
```

---

### AssetGrowth_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 49 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth_q']

**Observations**:
- Stata:  2,303,961
- Python: 2,303,943
- Common: 2,303,912

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |         0.1633 |         0.1633 |       2.84e-07 |       8.09e-08 |
| std        |         3.5114 |         3.5114 |         0.0207 |         0.0059 |
| min        |        -1.0268 |        -1.0268 |       -12.3040 |        -3.5040 |
| 25%        |        -0.0283 |        -0.0283 |      -2.02e-09 |      -5.74e-10 |
| 50%        |         0.0624 |         0.0624 |      -8.09e-13 |      -2.30e-13 |
| 75%        |         0.1821 |         0.1821 |       2.01e-09 |       5.72e-10 |
| max        |      2788.4187 |      2788.4186 |        13.1749 |         3.7521 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,303,912

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.92e-06 |     1.37e-05 |      0.2141 |     0.830 |
| Slope       |       1.0000 |     3.88e-06 | 257423.5890 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetGrowth_q
     0   10515  199604       0.039085
     1   10515  199605       0.039085
     2   10515  199606       0.039085
     3   10515  199704      -0.161325
     4   10515  199705      -0.161325
     5   10515  199706      -0.161325
     6   11545  199706       1.051804
     7   11545  199707       1.051804
     8   11545  199708       1.051804
     9   11545  199806       0.729125
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2303912 (0.002%)
- Stata standard deviation: 3.51e+00

---

### AssetLiquidityBook

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBook']

**Observations**:
- Stata:  3,595,932
- Python: 3,598,966
- Common: 3,595,932

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.48e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |         0.5929 |         0.5929 |      -5.19e-07 |      -1.35e-06 |
| std        |         0.3840 |         0.3840 |       3.14e-04 |       8.19e-04 |
| min        |       -11.5597 |       -11.5597 |        -0.1662 |        -0.4329 |
| 25%        |         0.5072 |         0.5072 |      -1.24e-08 |      -3.22e-08 |
| 50%        |         0.5933 |         0.5933 |         0.0000 |         0.0000 |
| 75%        |         0.6967 |         0.6967 |       1.23e-08 |       3.20e-08 |
| max        |       491.6170 |       491.6170 |         0.0941 |         0.2450 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,595,932

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.59e-07 |     3.05e-07 |     -2.4882 |     0.013 |
| Slope       |       1.0000 |     4.32e-07 |    2.32e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49/3595932 (0.001%)
- Stata standard deviation: 3.84e-01

---

### AssetLiquidityBookQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 44 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBookQuart']

**Observations**:
- Stata:  2,538,807
- Python: 2,553,360
- Common: 2,538,763

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.44e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.54e+06 |       2.54e+06 |       2.54e+06 |       2.54e+06 |
| mean       |         0.6036 |         0.6036 |       1.86e-06 |       1.38e-06 |
| std        |         1.3441 |         1.3441 |         0.0041 |         0.0030 |
| min        |       -10.8152 |       -10.8152 |        -0.9876 |        -0.7348 |
| 25%        |         0.5155 |         0.5155 |      -1.26e-08 |      -9.35e-09 |
| 50%        |         0.6075 |         0.6075 |         0.0000 |         0.0000 |
| 75%        |         0.7025 |         0.7025 |       1.25e-08 |       9.32e-09 |
| max        |      2003.3081 |      2003.3081 |         6.1525 |         4.5775 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,538,763

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.15e-06 |     2.79e-06 |      0.7683 |     0.442 |
| Slope       |       1.0000 |     1.90e-06 | 527351.3128 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityBookQuart
     0   10515  199604                 0.816307
     1   10515  199605                 0.781849
     2   10515  199606                 0.781849
     3   11545  199706                 0.818928
     4   11545  199707                 0.777539
     5   11545  199708                 0.777539
     6   12750  198212                 0.666923
     7   12750  198301                 0.695176
     8   12750  198302                 0.695176
     9   12750  198303                 0.943752
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 67/2538763 (0.003%)
- Stata standard deviation: 1.34e+00

---

### AssetLiquidityMarket

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarket']

**Observations**:
- Stata:  3,476,318
- Python: 3,477,044
- Common: 3,476,318

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.65e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.48e+06 |       3.48e+06 |       3.48e+06 |       3.48e+06 |
| mean       |         0.4488 |         0.4488 |      -4.78e-07 |      -1.71e-06 |
| std        |         0.2802 |         0.2802 |       1.49e-04 |       5.31e-04 |
| min        |        -7.2979 |        -7.2979 |        -0.0545 |        -0.1943 |
| 25%        |         0.2655 |         0.2655 |      -7.62e-09 |      -2.72e-08 |
| 50%        |         0.4442 |         0.4442 |       1.39e-17 |       4.95e-17 |
| 75%        |         0.5694 |         0.5694 |       7.63e-09 |       2.72e-08 |
| max        |        48.9168 |        48.9168 |         0.0013 |         0.0045 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,476,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.68e-07 |     1.51e-07 |     -3.1075 |     0.002 |
| Slope       |       1.0000 |     2.85e-07 |    3.51e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 49/3476318 (0.001%)
- Stata standard deviation: 2.80e-01

---

### AssetLiquidityMarketQuart

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 50 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarketQuart']

**Observations**:
- Stata:  2,503,163
- Python: 2,503,127
- Common: 2,503,113

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.4482 |         0.4482 |       1.58e-06 |       5.68e-06 |
| std        |         0.2781 |         0.2781 |         0.0036 |         0.0131 |
| min        |        -6.3541 |        -6.3541 |        -1.3938 |        -5.0125 |
| 25%        |         0.2725 |         0.2725 |      -7.72e-09 |      -2.78e-08 |
| 50%        |         0.4522 |         0.4522 |       6.28e-12 |       2.26e-11 |
| 75%        |         0.5664 |         0.5664 |       7.73e-09 |       2.78e-08 |
| max        |       137.3564 |       137.3564 |         5.3448 |        19.2216 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 2,503,113

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.24e-06 |     4.37e-06 |      1.4266 |     0.154 |
| Slope       |       1.0000 |     8.29e-06 | 120625.5350 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetLiquidityMarketQuart
     0   10515  199604                   0.819677
     1   10515  199605                   0.833838
     2   10515  199606                   0.833838
     3   11545  199706                   0.363298
     4   11545  199707                   0.407572
     5   11545  199708                   0.407572
     6   12750  198212                   0.349204
     7   12750  198301                   0.398642
     8   12750  198302                   0.398642
     9   12750  198303                   0.541186
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/2503113 (0.003%)
- Stata standard deviation: 2.78e-01

---

### AssetTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover']

**Observations**:
- Stata:  2,796,921
- Python: 2,816,617
- Common: 2,796,921

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.94e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2785 |       1.87e-04 |       7.15e-07 |
| std        |       261.1047 |       261.1082 |         0.0658 |       2.52e-04 |
| min        |         0.0000 |        -0.0000 |        -1.8130 |        -0.0069 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,921

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.15e-04 |     3.93e-05 |      2.9331 |     0.003 |
| Slope       |       1.0000 |     1.50e-07 |    6.65e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2796921 (0.001%)
- Stata standard deviation: 2.61e+02

---

### AssetTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 39 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover_q']

**Observations**:
- Stata:  1,963,604
- Python: 2,183,915
- Common: 1,963,565

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.48e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |         1.3790 |         1.3790 |       1.59e-05 |       2.89e-07 |
| std        |        55.1416 |        55.1406 |         0.0136 |       2.46e-04 |
| min        |         0.0000 |        -0.0000 |        -3.2387 |        -0.0587 |
| 25%        |         0.2551 |         0.2551 |      -1.00e-08 |      -1.81e-10 |
| 50%        |         0.5119 |         0.5119 |         0.0000 |         0.0000 |
| 75%        |         0.8749 |         0.8749 |       1.00e-08 |       1.82e-10 |
| max        |     27068.2270 |     27068.2000 |         7.8176 |         0.1418 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,963,565

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.24e-05 |     9.65e-06 |      4.3902 |     0.000 |
| Slope       |       1.0000 |     1.75e-07 |    5.72e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AssetTurnover_q
     0   11545  199706         0.546037
     1   11545  199707         0.546037
     2   11545  199708         0.546037
     3   12373  202406         0.021631
     4   12373  202407         0.021631
     5   12373  202408         0.021631
     6   12373  202409         0.038419
     7   12373  202410         0.038419
     8   12373  202411         0.038419
     9   12373  202412         0.047890
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 42/1963565 (0.002%)
- Stata standard deviation: 5.51e+01

---

### BMq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BMq']

**Observations**:
- Stata:  2,568,885
- Python: 2,717,113
- Common: 2,568,885

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |        -0.5919 |        -0.5919 |      -1.30e-06 |      -1.36e-06 |
| std        |         0.9608 |         0.9608 |         0.0015 |         0.0015 |
| min        |       -13.7467 |       -13.7467 |        -0.8206 |        -0.8540 |
| 25%        |        -1.1088 |        -1.1088 |      -1.09e-08 |      -1.13e-08 |
| 50%        |        -0.5062 |        -0.5062 |      -3.87e-12 |      -4.02e-12 |
| 75%        |         0.0109 |         0.0109 |       1.09e-08 |       1.13e-08 |
| max        |         6.6128 |         6.6128 |         0.7888 |         0.8210 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,568,885

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.73e-06 |     1.08e-06 |     -1.6040 |     0.109 |
| Slope       |       1.0000 |     9.58e-07 |    1.04e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 76/2568885 (0.003%)
- Stata standard deviation: 9.61e-01

---

### BetaBDLeverage

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaBDLeverage']

**Observations**:
- Stata:  2,116,539
- Python: 2,130,495
- Common: 2,116,539

**Precision1**: 2.206% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.12e+06 |       2.12e+06 |       2.12e+06 |       2.12e+06 |
| mean       |         0.2175 |         0.2194 |         0.0019 |         0.0019 |
| std        |         0.9765 |         0.9681 |         0.1224 |         0.1254 |
| min        |       -29.5917 |       -29.5915 |        -5.8416 |        -5.9822 |
| 25%        |        -0.1353 |        -0.1334 |      -5.38e-06 |      -5.51e-06 |
| 50%        |         0.2846 |         0.2856 |       4.28e-05 |       4.38e-05 |
| 75%        |         0.6641 |         0.6649 |       7.60e-05 |       7.78e-05 |
| max        |        25.2977 |        25.2978 |        16.0268 |        16.4126 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0054 + 0.9836 * stata
- **R-squared**: 0.9843
- **N observations**: 2,116,539

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0054 |     8.55e-05 |     63.7187 |     0.000 |
| Slope       |       0.9836 |     8.54e-05 |  11514.0790 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 46683/2116539 (2.206%)
- Stata standard deviation: 9.76e-01

---

### BetaDimson

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaDimson']

**Observations**:
- Stata:  5,002,680
- Python: 5,083,747
- Common: 5,002,680

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.00e+06 |       5.00e+06 |       5.00e+06 |       5.00e+06 |
| mean       |         0.7973 |         0.7973 |       3.67e-10 |       1.53e-10 |
| std        |         2.3944 |         2.3944 |       9.55e-08 |       3.99e-08 |
| min        |      -286.1514 |      -286.1514 |      -9.68e-06 |      -4.04e-06 |
| 25%        |        -0.0184 |        -0.0184 |      -2.59e-08 |      -1.08e-08 |
| 50%        |         0.6958 |         0.6958 |      -6.02e-16 |      -2.51e-16 |
| 75%        |         1.5830 |         1.5830 |       2.62e-08 |       1.09e-08 |
| max        |       301.7971 |       301.7971 |       1.43e-05 |       5.96e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 5,002,680

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.63e-10 |     4.50e-11 |    -19.1997 |     0.000 |
| Slope       |       1.0000 |     1.78e-11 |    5.61e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/5002680 (0.000%)
- Stata standard deviation: 2.39e+00

---

### BetaSquared

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BetaSquared']

**Observations**:
- Stata:  4,285,574
- Python: 4,353,773
- Common: 4,285,574

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.04e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.29e+06 |       4.29e+06 |       4.29e+06 |       4.29e+06 |
| mean       |         1.5351 |         1.5351 |       7.77e-09 |       1.17e-09 |
| std        |         6.6568 |         6.6568 |       4.67e-07 |       7.02e-08 |
| min        |       5.10e-13 |       5.13e-13 |      -4.38e-05 |      -6.58e-06 |
| 25%        |         0.2920 |         0.2920 |      -1.62e-08 |      -2.43e-09 |
| 50%        |         0.8168 |         0.8168 |       4.33e-10 |       6.51e-11 |
| 75%        |         1.7846 |         1.7846 |       2.33e-08 |       3.50e-09 |
| max        |      2770.3259 |      2770.3261 |       3.03e-04 |       4.55e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,285,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -6.95e-08 |     1.61e-10 |   -430.8821 |     0.000 |
| Slope       |       1.0000 |     2.36e-11 |    4.24e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/4285574 (0.000%)
- Stata standard deviation: 6.66e+00

---

### BidAskTAQ

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BidAskTAQ']

**Observations**:
- Stata:  3,262,927
- Python: 3,262,927
- Common: 3,262,927

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.96e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |         1.5559 |         1.5559 |      -7.71e-12 |      -3.07e-12 |
| std        |         2.5110 |         2.5110 |       4.90e-08 |       1.95e-08 |
| min        |         0.0000 |         0.0000 |      -2.00e-06 |      -7.96e-07 |
| 25%        |         0.1774 |         0.1774 |         0.0000 |         0.0000 |
| 50%        |         0.6136 |         0.6136 |         0.0000 |         0.0000 |
| 75%        |         1.8032 |         1.8032 |         0.0000 |         0.0000 |
| max        |        39.9582 |        39.9582 |       2.00e-06 |       7.96e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,262,927

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.86e-12 |     3.19e-11 |     -0.0584 |     0.953 |
| Slope       |       1.0000 |     1.08e-11 |    9.26e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3262927 (0.000%)
- Stata standard deviation: 2.51e+00

---

### BookLeverageQuarterly

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BookLeverageQuarterly']

**Observations**:
- Stata:  2,572,594
- Python: 2,670,966
- Common: 2,572,594

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.13e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |       945.9140 |            inf |            inf |            inf |
| std        |       3.67e+06 |            N/A |            N/A |            N/A |
| min        |      -1.62e+09 |    -34413.0000 |       -96.2367 |      -2.62e-05 |
| 25%        |         1.4348 |         1.4348 |      -6.20e-08 |      -1.69e-14 |
| 50%        |         2.0340 |         2.0340 |      -2.22e-16 |      -6.04e-23 |
| 75%        |         3.3458 |         3.3458 |       6.19e-08 |       1.68e-14 |
| max        |       2.85e+09 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 2,572,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18/2572594 (0.001%)
- Stata standard deviation: 3.67e+06

---

### BrandCapital

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['BrandCapital']

**Observations**:
- Stata:  1,231,460
- Python: 1,280,000
- Common: 1,231,460

**Precision1**: 5.877% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.25e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.23e+06 |       1.23e+06 |       1.23e+06 |       1.23e+06 |
| mean       |         0.0642 |         0.0656 |         0.0014 |         0.0040 |
| std        |         0.3504 |         0.3545 |         0.0239 |         0.0683 |
| min        |        -0.0066 |        -0.0066 |        -0.0211 |        -0.0603 |
| 25%        |         0.0043 |         0.0045 |      -1.01e-10 |      -2.88e-10 |
| 50%        |         0.0228 |         0.0238 |       2.62e-10 |       7.47e-10 |
| 75%        |         0.0651 |         0.0669 |       1.75e-07 |       5.00e-07 |
| max        |        86.0362 |        86.0362 |         6.8422 |        19.5254 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0094 * stata
- **R-squared**: 0.9955
- **N observations**: 1,231,460

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.07e-04 |     2.17e-05 |     37.1912 |     0.000 |
| Slope       |       1.0094 |     6.09e-05 |  16562.8102 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72379/1231460 (5.877%)
- Stata standard deviation: 3.50e-01

---

### CBOperProfLagAT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CBOperProfLagAT']

**Observations**:
- Stata:  2,103,518
- Python: 2,171,034
- Common: 2,103,518

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.60e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1168 |         0.1168 |       4.30e-09 |       8.53e-09 |
| std        |         0.5041 |         0.5041 |       2.96e-04 |       5.88e-04 |
| min        |      -162.6901 |      -162.6901 |        -0.2216 |        -0.4396 |
| 25%        |         0.0533 |         0.0533 |      -3.47e-09 |      -6.89e-09 |
| 50%        |         0.1320 |         0.1320 |       4.66e-12 |       9.24e-12 |
| 75%        |         0.2129 |         0.2129 |       3.50e-09 |       6.94e-09 |
| max        |        26.7835 |        26.7835 |         0.0372 |         0.0738 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,103,518

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.13e-07 |     2.10e-07 |      1.0172 |     0.309 |
| Slope       |       1.0000 |     4.05e-07 |    2.47e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 82/2103518 (0.004%)
- Stata standard deviation: 5.04e-01

---

### CBOperProfLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['CBOperProfLagAT_q']

**Observations**:
- Stata:  1,911,489
- Python: 2,183,952
- Common: 1,911,489

**Precision1**: 26.663% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.54e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         0.0219 |         0.0116 |        -0.0103 |        -0.0585 |
| std        |         0.1758 |         0.2600 |         0.2070 |         1.1774 |
| min        |       -89.0698 |       -89.0698 |       -38.9822 |      -221.7759 |
| 25%        |        -0.0051 |        -0.0079 |      -1.17e-09 |      -6.67e-09 |
| 50%        |         0.0278 |         0.0285 |       1.14e-10 |       6.51e-10 |
| 75%        |         0.0571 |         0.0598 |       2.68e-09 |       1.53e-08 |
| max        |        22.7565 |        23.8488 |        23.8496 |       135.6844 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0081 + 0.9012 * stata
- **R-squared**: 0.3711
- **N observations**: 1,911,489

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0081 |     1.50e-04 |    -54.0166 |     0.000 |
| Slope       |       0.9012 |     8.49e-04 |   1061.9617 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 509657/1911489 (26.663%)
- Stata standard deviation: 1.76e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10333  202412 -0.138080 -0.068818 -0.069262
1   10382  202412  0.042999  0.023126  0.019874
2   10516  202412  0.023663  0.018805  0.004858
3   10517  202412 -0.097929  0.305647 -0.403575
4   11144  202412  0.066241  0.050950  0.015291
5   11654  202412 -0.018806 -0.030510  0.011704
6   11731  202412  0.049574  0.026383  0.023191
7   11850  202412  0.045113  0.043205  0.001908
8   12009  202412  0.019519  0.017253  0.002266
9   12017  202412 -0.085506 -0.091540  0.006035
```

**Largest Differences**:
```
   permno  yyyymm     python         stata       diff
0   85002  200003 -38.982167  4.432618e-17 -38.982167
1   85002  200004 -38.982167  4.432618e-17 -38.982167
2   85002  200005 -38.982167  4.432618e-17 -38.982167
3   25778  198212 -32.869907 -1.559557e-01 -32.713951
4   25778  198301 -32.869907 -1.559557e-01 -32.713951
5   25778  198302 -32.869907 -1.559557e-01 -32.713951
6   79906  199412 -31.007524 -1.504778e-03 -31.006019
7   79906  199501 -31.007524 -1.504778e-03 -31.006019
8   79906  199502 -31.007524 -1.504778e-03 -31.006019
9   79906  199409 -26.832238 -2.543420e-02 -26.806804
```

---

### CFq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CFq']

**Observations**:
- Stata:  2,797,878
- Python: 3,041,630
- Common: 2,797,878

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.51e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |      -4.71e-06 |      -4.02e-06 |
| std        |         1.1714 |         1.1714 |         0.0037 |         0.0031 |
| min        |      -917.6409 |      -917.6409 |        -2.7228 |        -2.3243 |
| 25%        |         0.0039 |         0.0039 |      -5.35e-10 |      -4.57e-10 |
| 50%        |         0.0195 |         0.0195 |      -1.45e-13 |      -1.24e-13 |
| 75%        |         0.0369 |         0.0369 |       5.33e-10 |       4.55e-10 |
| max        |       163.1038 |       163.1038 |         1.5098 |         1.2889 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,797,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.74e-06 |     2.18e-06 |     -2.1696 |     0.030 |
| Slope       |       1.0000 |     1.86e-06 | 536734.4442 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 222/2797878 (0.008%)
- Stata standard deviation: 1.17e+00

---

### CapTurnover

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover']

**Observations**:
- Stata:  2,985,685
- Python: 2,986,378
- Common: 2,985,685

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.99e+06 |       2.99e+06 |       2.99e+06 |       2.99e+06 |
| mean       |         1.1455 |         1.1455 |      -1.85e-07 |      -1.04e-07 |
| std        |         1.7917 |         1.7917 |       7.20e-05 |       4.02e-05 |
| min        |        -1.8804 |        -1.8804 |        -0.0353 |        -0.0197 |
| 25%        |         0.3456 |         0.3456 |      -1.39e-08 |      -7.78e-09 |
| 50%        |         0.9236 |         0.9236 |         0.0000 |         0.0000 |
| 75%        |         1.5797 |         1.5797 |       1.43e-08 |       7.97e-09 |
| max        |       392.8943 |       392.8943 |       5.00e-06 |       2.79e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,985,685

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.44e-07 |     4.95e-08 |     -4.9341 |     0.000 |
| Slope       |       1.0000 |     2.33e-08 |    4.30e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2985685 (0.000%)
- Stata standard deviation: 1.79e+00

---

### CapTurnover_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 48 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover_q']

**Observations**:
- Stata:  2,486,325
- Python: 2,486,315
- Common: 2,486,277

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |         0.2638 |         0.2638 |       8.96e-07 |       2.86e-07 |
| std        |         3.1372 |         3.1372 |         0.0033 |         0.0011 |
| min        |        -0.9789 |        -0.9789 |        -1.4640 |        -0.4666 |
| 25%        |         0.0801 |         0.0801 |      -3.40e-09 |      -1.08e-09 |
| 50%        |         0.2127 |         0.2127 |         0.0000 |         0.0000 |
| 75%        |         0.3650 |         0.3650 |       3.40e-09 |       1.08e-09 |
| max        |      2816.9070 |      2816.9070 |         1.5684 |         0.4999 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,486,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.01e-06 |     2.11e-06 |      0.4784 |     0.632 |
| Slope       |       1.0000 |     6.70e-07 |    1.49e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  CapTurnover_q
     0   10515  199607       0.068358
     1   10515  199608       0.068358
     2   10515  199609       0.068358
     3   11545  199706       0.209439
     4   11545  199707       0.209439
     5   11545  199708       0.209439
     6   12750  198303       0.359559
     7   12750  198304       0.359559
     8   12750  198305       0.359559
     9   12837  198004       0.328576
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 93/2486277 (0.004%)
- Stata standard deviation: 3.14e+00

---

### ChNCOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNCOA']

**Observations**:
- Stata:  3,295,125
- Python: 3,295,872
- Common: 3,295,125

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.48e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0889 |         0.0889 |      -2.75e-06 |      -3.06e-06 |
| std        |         0.8966 |         0.8966 |         0.0015 |         0.0016 |
| min        |        -1.4114 |        -1.4114 |        -0.7511 |        -0.8377 |
| 25%        |        -0.0138 |        -0.0138 |      -9.90e-09 |      -1.10e-08 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0917 |         0.0917 |       9.89e-09 |       1.10e-08 |
| max        |       192.5833 |       192.5833 |         0.1241 |         0.1384 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,125

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.76e-06 |     8.11e-07 |     -3.4040 |     0.001 |
| Slope       |       1.0000 |     9.00e-07 |    1.11e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/3295125 (0.003%)
- Stata standard deviation: 8.97e-01

---

### ChNCOL

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChNCOL']

**Observations**:
- Stata:  3,249,290
- Python: 3,250,061
- Common: 3,249,290

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.79e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |         0.0487 |         0.0487 |      -1.48e-07 |      -1.52e-07 |
| std        |         0.9693 |         0.9693 |       1.85e-04 |       1.91e-04 |
| min        |       -23.0669 |       -23.0669 |        -0.0482 |        -0.0497 |
| 25%        |        -0.0092 |        -0.0092 |      -5.62e-09 |      -5.80e-09 |
| 50%        |         0.0187 |         0.0187 |         0.0000 |         0.0000 |
| 75%        |         0.0626 |         0.0626 |       5.61e-09 |       5.79e-09 |
| max        |       381.2545 |       381.2545 |         0.0528 |         0.0545 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,249,290

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.46e-07 |     1.03e-07 |     -1.4209 |     0.155 |
| Slope       |       1.0000 |     1.06e-07 |    9.42e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/3249290 (0.004%)
- Stata standard deviation: 9.69e-01

---

### ChPM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChPM']

**Observations**:
- Stata:  3,222,277
- Python: 3,288,060
- Common: 3,222,277

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.23e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.3833 |        -0.3833 |      -4.11e-08 |      -2.71e-10 |
| std        |       151.4586 |       151.4586 |       7.13e-04 |       4.71e-06 |
| min        |    -30903.6450 |    -30903.6451 |        -0.2284 |        -0.0015 |
| 25%        |        -0.0312 |        -0.0312 |      -2.22e-09 |      -1.47e-11 |
| 50%        |      -1.17e-04 |      -1.17e-04 |       6.86e-12 |       4.53e-14 |
| 75%        |         0.0251 |         0.0251 |       2.23e-09 |       1.48e-11 |
| max        |     24410.3810 |     24410.3806 |         0.2069 |         0.0014 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.21e-08 |     3.97e-07 |     -0.1059 |     0.916 |
| Slope       |       1.0000 |     2.62e-09 |    3.81e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3222277 (0.000%)
- Stata standard deviation: 1.51e+02

---

### ChangeRoA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoA']

**Observations**:
- Stata:  2,296,769
- Python: 2,526,837
- Common: 2,296,769

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.61e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |        -0.0019 |        -0.0019 |       3.63e-08 |       1.55e-07 |
| std        |         0.2344 |         0.2344 |         0.0021 |         0.0090 |
| min        |       -55.1174 |       -55.1174 |        -0.8505 |        -3.6276 |
| 25%        |        -0.0078 |        -0.0078 |      -4.27e-10 |      -1.82e-09 |
| 50%        |      -7.35e-05 |      -7.35e-05 |      -3.63e-13 |      -1.55e-12 |
| 75%        |         0.0058 |         0.0058 |       4.28e-10 |       1.83e-09 |
| max        |       136.3447 |       136.3447 |         0.8505 |         3.6276 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 2,296,769

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.43e-08 |     1.40e-06 |     -0.0531 |     0.958 |
| Slope       |       0.9999 |     5.97e-06 | 167454.4596 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 234/2296769 (0.010%)
- Stata standard deviation: 2.34e-01

---

### ChangeRoE

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ChangeRoE']

**Observations**:
- Stata:  2,360,217
- Python: 2,535,908
- Common: 2,360,217

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.18e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.36e+06 |       2.36e+06 |       2.36e+06 |       2.36e+06 |
| mean       |      -8.46e-04 |      -8.50e-04 |      -4.31e-06 |      -1.39e-07 |
| std        |        31.1263 |        31.1265 |         0.0990 |         0.0032 |
| min        |    -14927.4960 |    -14927.4966 |       -61.0000 |        -1.9598 |
| 25%        |        -0.0196 |        -0.0196 |      -1.10e-09 |      -3.53e-11 |
| 50%        |      -6.95e-04 |      -6.95e-04 |      -1.29e-12 |      -4.14e-14 |
| 75%        |         0.0130 |         0.0130 |       1.09e-09 |       3.49e-11 |
| max        |     14925.0560 |     14925.0557 |        61.0000 |         1.9598 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,360,217

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.31e-06 |     6.44e-05 |     -0.0669 |     0.947 |
| Slope       |       1.0000 |     2.07e-06 | 483063.0535 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 46/2360217 (0.002%)
- Stata standard deviation: 3.11e+01

---

### DelSTI

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelSTI']

**Observations**:
- Stata:  3,295,155
- Python: 3,295,872
- Common: 3,295,155

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.04e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0019 |         0.0019 |      -7.19e-07 |      -7.20e-06 |
| std        |         0.0999 |         0.0999 |       4.37e-04 |         0.0044 |
| min        |        -1.8790 |        -1.8790 |        -0.2141 |        -2.1431 |
| 25%        |      -6.70e-06 |      -6.63e-06 |      -1.32e-12 |      -1.32e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |       2.58e-04 |       2.58e-04 |       1.33e-12 |       1.34e-11 |
| max        |         1.8457 |         1.8457 |         0.0581 |         0.5818 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -7.46e-07 |     2.41e-07 |     -3.0985 |     0.002 |
| Slope       |       1.0000 |     2.41e-06 | 414759.9752 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 108/3295155 (0.003%)
- Stata standard deviation: 9.99e-02

---

### DelayAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4549 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayAcct']

**Observations**:
- Stata:  674,090
- Python: 722,651
- Common: 669,541

**Precision1**: 89.589% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.12e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    669541.0000 |    669541.0000 |    669541.0000 |    669541.0000 |
| mean       |         0.1916 |         0.1941 |         0.0025 |         0.0265 |
| std        |         0.0957 |         0.0967 |         0.0156 |         0.1626 |
| min        |        -0.4104 |        -0.3694 |        -0.6092 |        -6.3656 |
| 25%        |         0.1119 |         0.1132 |        -0.0028 |        -0.0297 |
| 50%        |         0.1732 |         0.1768 |         0.0020 |         0.0213 |
| 75%        |         0.2700 |         0.2733 |         0.0076 |         0.0798 |
| max        |         1.3192 |         1.4377 |         0.6684 |         6.9841 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0030 + 0.9977 * stata
- **R-squared**: 0.9741
- **N observations**: 669,541

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0030 |     4.25e-05 |     70.0089 |     0.000 |
| Slope       |       0.9977 |     1.99e-04 |   5022.0174 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayAcct
     0   10114  200306   0.405294
     1   10114  200307   0.400538
     2   10119  199706   0.367174
     3   10119  199707   0.350161
     4   10119  199708   0.354161
     5   10119  199709   0.358161
     6   10119  199710   0.354708
     7   10119  199711   0.349145
     8   10119  199802   0.348034
     9   10119  199803   0.358375
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 599832/669541 (89.589%)
- Stata standard deviation: 9.57e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202407  0.151546  0.155085 -0.003539
1   10028  202407  0.235169  0.220374  0.014795
2   10032  202407  0.140464  0.142951 -0.002487
3   10138  202407  0.165682  0.161488  0.004194
4   10158  202407  0.157643  0.158672 -0.001030
5   10200  202407  0.146554  0.144167  0.002387
6   10220  202407  0.170142  0.171523 -0.001381
7   10257  202407  0.222061  0.231531 -0.009470
8   10318  202407  0.142052  0.138319  0.003733
9   10382  202407  0.173514  0.184804 -0.011290
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90285  201804  0.923722  0.255317  0.668405
1   90285  201805  0.875788  0.242163  0.633625
2   87084  201508  0.341064  0.950278 -0.609214
3   87084  201507  0.311339  0.916879 -0.605540
4   90285  201711  0.779553  0.177341  0.602212
5   90285  201708  0.787031  0.190940  0.596091
6   87084  201510  0.208410  0.801547 -0.593137
7   87084  201511  0.227464  0.815343 -0.587879
8   90285  201710  0.754215  0.169134  0.585081
9   90285  201709  0.743042  0.168518  0.574524
```

---

### DelayNonAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4549 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayNonAcct']

**Observations**:
- Stata:  674,090
- Python: 722,651
- Common: 669,541

**Precision1**: 78.142% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.86e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    669541.0000 |    669541.0000 |    669541.0000 |    669541.0000 |
| mean       |      -3.56e-04 |        -0.0029 |        -0.0025 |        -0.0124 |
| std        |         0.2048 |         0.2048 |         0.0156 |         0.0761 |
| min        |        -0.7815 |        -0.8640 |        -0.6684 |        -3.2631 |
| 25%        |        -0.1141 |        -0.1162 |        -0.0076 |        -0.0373 |
| 50%        |        -0.0509 |        -0.0527 |        -0.0020 |        -0.0099 |
| 75%        |         0.0450 |         0.0424 |         0.0028 |         0.0139 |
| max        |         0.9457 |         0.9705 |         0.6092 |         2.9741 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0025 + 0.9970 * stata
- **R-squared**: 0.9942
- **N observations**: 669,541

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0025 |     1.90e-05 |   -133.4392 |     0.000 |
| Slope       |       0.9970 |     9.29e-05 |  10732.3937 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayNonAcct
     0   10114  200306     -0.267660
     1   10114  200307     -0.114482
     2   10119  199706     -0.277600
     3   10119  199707      0.003510
     4   10119  199708     -0.000490
     5   10119  199709     -0.004490
     6   10119  199710     -0.001037
     7   10119  199711      0.004526
     8   10119  199802      0.005637
     9   10119  199803     -0.004704
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 523193/669541 (78.142%)
- Stata standard deviation: 2.05e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202407  0.336787  0.333248  0.003539
1   10028  202407 -0.184858 -0.170063 -0.014795
2   10032  202407 -0.083146 -0.085633  0.002487
3   10138  202407 -0.148736 -0.144541 -0.004194
4   10200  202407 -0.118465 -0.116077 -0.002387
5   10257  202407  0.222719  0.213249  0.009470
6   10318  202407 -0.119658 -0.115925 -0.003733
7   10382  202407 -0.022283 -0.033574  0.011290
8   10397  202407 -0.125235 -0.128800  0.003565
9   10516  202407  0.216990  0.219996 -0.003006
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   90285  201804 -0.758650 -0.090245 -0.668405
1   90285  201805 -0.710716 -0.077091 -0.633625
2   87084  201508 -0.172254 -0.781468  0.609214
3   87084  201507 -0.142529 -0.748070  0.605540
4   90285  201711 -0.614482 -0.012269 -0.602212
5   90285  201708 -0.621960 -0.025869 -0.596091
6   87084  201510 -0.039601 -0.632738  0.593137
7   87084  201511 -0.058654 -0.646533  0.587879
8   90285  201710 -0.589144 -0.004063 -0.585081
9   90285  201709 -0.577971 -0.003446 -0.574524
```

---

### DivYield

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYield']

**Observations**:
- Stata:  421,384
- Python: 2,014,931
- Common: 421,384

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    421384.0000 |    421384.0000 |    421384.0000 |    421384.0000 |
| mean       |         0.0490 |         0.0490 |      -1.45e-05 |      -2.53e-05 |
| std        |         0.5731 |         0.5718 |         0.0043 |         0.0074 |
| min        |         0.0000 |         0.0000 |        -1.7481 |        -3.0501 |
| 25%        |         0.0201 |         0.0201 |      -1.02e-09 |      -1.77e-09 |
| 50%        |         0.0356 |         0.0356 |      -2.02e-11 |      -3.53e-11 |
| 75%        |         0.0554 |         0.0554 |       4.69e-10 |       8.19e-10 |
| max        |       154.9091 |       154.9091 |         0.0335 |         0.0584 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9976 * stata
- **R-squared**: 1.0000
- **N observations**: 421,384

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.05e-04 |     6.22e-06 |     16.7946 |     0.000 |
| Slope       |       0.9976 |     1.08e-05 |  92188.7514 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/421384 (0.007%)
- Stata standard deviation: 5.73e-01

---

### DivYieldAnn

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DivYieldAnn']

**Observations**:
- Stata:  3,878,713
- Python: 3,883,930
- Common: 3,878,713

**Precision1**: 0.032% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.07e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.88e+06 |       3.88e+06 |       3.88e+06 |       3.88e+06 |
| mean       |         0.0239 |         0.0239 |       2.17e-05 |       1.05e-04 |
| std        |         0.2072 |         0.2075 |         0.0092 |         0.0443 |
| min        |        -0.5405 |        -0.5405 |        -1.5984 |        -7.7145 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0299 |         0.0299 |         0.0000 |         0.0000 |
| max        |        83.2000 |        83.2000 |         6.1759 |        29.8080 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0004 * stata
- **R-squared**: 0.9980
- **N observations**: 3,878,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.26e-05 |     4.69e-06 |      2.6782 |     0.007 |
| Slope       |       1.0004 |     2.25e-05 |  44469.1835 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1247/3878713 (0.032%)
- Stata standard deviation: 2.07e-01

---

### DownsideBeta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownsideBeta']

**Observations**:
- Stata:  4,848,559
- Python: 5,072,307
- Common: 4,848,553

**Precision1**: 0.349% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.20e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.85e+06 |       4.85e+06 |       4.85e+06 |       4.85e+06 |
| mean       |         0.8537 |         0.8539 |       2.51e-04 |       3.49e-04 |
| std        |         0.7191 |         0.7203 |         0.0454 |         0.0632 |
| min        |       -43.6149 |       -43.6149 |       -17.8849 |       -24.8725 |
| 25%        |         0.4076 |         0.4076 |      -2.44e-15 |      -3.40e-15 |
| 50%        |         0.8185 |         0.8188 |       2.22e-16 |       3.09e-16 |
| 75%        |         1.2309 |         1.2312 |       4.00e-15 |       5.56e-15 |
| max        |        16.0159 |        22.7108 |        22.2480 |        30.9402 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9998 * stata
- **R-squared**: 0.9960
- **N observations**: 4,848,553

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.28e-04 |     3.20e-05 |     13.3559 |     0.000 |
| Slope       |       0.9998 |     2.87e-05 |  34841.2739 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DownsideBeta
     0   11746  192608      0.712000
     1   12909  192608      0.917963
     2   13127  192608      0.547239
     3   13629  192612      0.354627
     4   13960  192608     -1.756058
     5   18593  192608      0.171028
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16923/4848553 (0.349%)
- Stata standard deviation: 7.19e-01

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
- Test 2 - Superset check: ❌ FAILED (Python missing 36 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EPq']

**Observations**:
- Stata:  1,893,938
- Python: 1,893,940
- Common: 1,893,902

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.62e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.89e+06 |       1.89e+06 |       1.89e+06 |       1.89e+06 |
| mean       |         0.0273 |         0.0273 |       1.70e-07 |       1.70e-06 |
| std        |         0.1001 |         0.1001 |       2.62e-04 |         0.0026 |
| min        |         0.0000 |         0.0000 |        -0.0547 |        -0.5459 |
| 25%        |         0.0107 |         0.0107 |      -3.58e-10 |      -3.57e-09 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0297 |         0.0297 |       3.59e-10 |       3.58e-09 |
| max        |        35.0386 |        35.0386 |         0.2346 |         2.3427 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,893,902

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.81e-07 |     1.97e-07 |      0.9165 |     0.359 |
| Slope       |       1.0000 |     1.90e-06 | 526487.0811 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      EPq
     0   10515  199604 0.005181
     1   10515  199605 0.005181
     2   10515  199606 0.005181
     3   11545  199706 0.014092
     4   11545  199707 0.014227
     5   11545  199708 0.014227
     6   11843  198803 0.040014
     7   11843  198804 0.081029
     8   11843  198805 0.055882
     9   12837  198004 0.033490
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 82/1893902 (0.004%)
- Stata standard deviation: 1.00e-01

---

### ETR

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ETR']

**Observations**:
- Stata:  2,657,230
- Python: 2,658,445
- Common: 2,657,230

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.20e-12 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.66e+06 |       2.66e+06 |       2.66e+06 |       2.66e+06 |
| mean       |       200.8662 |       199.7921 |        -1.0740 |      -1.11e-05 |
| std        |     96619.4326 |     96620.8610 |       523.6358 |         0.0054 |
| min        |      -2.82e+07 |      -2.82e+07 |   -256264.7862 |        -2.6523 |
| 25%        |      -6.25e-04 |      -6.25e-04 |      -1.44e-10 |      -1.49e-15 |
| 50%        |         0.0000 |         0.0000 |        -0.0000 |        -0.0000 |
| 75%        |         0.0010 |         0.0010 |       1.45e-10 |       1.50e-15 |
| max        |       3.75e+07 |       3.75e+07 |      8898.4587 |         0.0921 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -1.0741 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,657,230

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -1.0741 |       0.3212 |     -3.3436 |     0.001 |
| Slope       |       1.0000 |     3.32e-06 | 300780.4586 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2657230 (0.001%)
- Stata standard deviation: 9.66e+04

---

### EarningsConservatism

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36945 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsConservatism']

**Observations**:
- Stata:  1,467,671
- Python: 1,503,418
- Common: 1,430,726

**Precision1**: 3.563% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.39e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |       -58.8950 |         0.2690 |        59.1640 |         0.0030 |
| std        |     19715.2905 |        36.3067 |     19714.2874 |         0.9999 |
| min        |      -6.48e+06 |      -100.0000 |   -872029.2500 |       -44.2311 |
| 25%        |        -5.1398 |        -5.1886 |      -1.17e-06 |      -5.91e-11 |
| 50%        |         0.9102 |         0.6719 |         0.0000 |         0.0000 |
| 75%        |         5.4525 |         5.5536 |       9.13e-07 |       4.63e-11 |
| max        |    872129.2500 |       100.0000 |       6.48e+06 |       328.6320 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.2721 + 0.0001 * stata
- **R-squared**: 0.0008
- **N observations**: 1,430,726

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.2721 |       0.0303 |      8.9674 |     0.000 |
| Slope       |     5.26e-05 |     1.54e-06 |     34.1609 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarningsConservatism
     0   10002  200306             -1.976701
     1   10002  200307             -1.976701
     2   10002  200308             -1.976701
     3   10002  200309             -1.976701
     4   10002  200310             -1.976701
     5   10002  200311             -1.976701
     6   10002  200312             -1.976701
     7   10002  200401             -1.976701
     8   10002  200402             -1.976701
     9   10002  200403             -1.976701
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 50971/1430726 (3.563%)
- Stata standard deviation: 1.97e+04

---

### EarningsPersistence

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsPersistence']

**Observations**:
- Stata:  1,495,672
- Python: 1,553,579
- Common: 1,495,672

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.12e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |         0.4579 |         0.4579 |       5.41e-07 |       9.03e-07 |
| std        |         0.5997 |         0.5997 |       3.63e-04 |       6.06e-04 |
| min        |      -119.0719 |      -119.0719 |      -3.47e-06 |      -5.78e-06 |
| 25%        |         0.1421 |         0.1421 |      -1.11e-08 |      -1.85e-08 |
| 50%        |         0.4517 |         0.4517 |      -5.03e-12 |      -8.39e-12 |
| 75%        |         0.7670 |         0.7670 |       1.08e-08 |       1.80e-08 |
| max        |        14.3520 |        14.3520 |         0.2564 |         0.4276 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.27e-07 |     3.74e-07 |      1.9440 |     0.052 |
| Slope       |       1.0000 |     4.95e-07 |    2.02e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/1495672 (0.000%)
- Stata standard deviation: 6.00e-01

---

### EarningsPredictability

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsPredictability']

**Observations**:
- Stata:  1,495,672
- Python: 1,553,579
- Common: 1,495,672

**Precision1**: 0.057% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.62e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |       2.99e+11 |       2.39e+11 |      -5.99e+10 |        -0.0015 |
| std        |       4.05e+13 |       3.24e+13 |       8.10e+12 |         0.2000 |
| min        |         0.0000 |         0.0000 |      -2.45e+15 |       -60.5280 |
| 25%        |         0.0446 |         0.0357 |        -0.3582 |      -8.84e-15 |
| 50%        |         0.2784 |         0.2227 |        -0.0557 |      -1.37e-15 |
| 75%        |         1.7905 |         1.4323 |        -0.0089 |      -2.20e-16 |
| max        |       1.23e+16 |       9.81e+15 |       3.60e+09 |       8.88e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 29563.6909 + 0.8000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   29563.6909 |    8385.2264 |      3.5257 |     0.000 |
| Slope       |       0.8000 |     2.07e-10 |    3.87e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 849/1495672 (0.057%)
- Stata standard deviation: 4.05e+13

---

### EarningsSmoothness

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsSmoothness']

**Observations**:
- Stata:  1,482,823
- Python: 1,538,785
- Common: 1,482,823

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.06e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.48e+06 |       1.48e+06 |       1.48e+06 |       1.48e+06 |
| mean       |         0.6548 |         0.6548 |       2.11e-07 |       5.30e-07 |
| std        |         0.3971 |         0.3971 |       2.96e-04 |       7.45e-04 |
| min        |         0.0036 |         0.0036 |        -0.0287 |        -0.0722 |
| 25%        |         0.3480 |         0.3480 |      -1.50e-08 |      -3.78e-08 |
| 50%        |         0.6297 |         0.6297 |       1.52e-11 |       3.82e-11 |
| 75%        |         0.9233 |         0.9233 |       1.51e-08 |       3.79e-08 |
| max        |         8.3146 |         8.3146 |         0.3090 |         0.7781 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,482,823

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.16e-07 |     4.69e-07 |      0.8875 |     0.375 |
| Slope       |       1.0000 |     6.12e-07 |    1.63e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 73/1482823 (0.005%)
- Stata standard deviation: 3.97e-01

---

### EarningsTimeliness

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36945 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsTimeliness']

**Observations**:
- Stata:  1,467,923
- Python: 1,503,418
- Common: 1,430,978

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.76e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         0.3952 |         0.3952 |       4.16e-06 |       1.69e-05 |
| std        |         0.2458 |         0.2458 |         0.0013 |         0.0053 |
| min        |       6.46e-10 |       6.48e-10 |      -1.35e-06 |      -5.48e-06 |
| 25%        |         0.1933 |         0.1933 |      -1.34e-08 |      -5.46e-08 |
| 50%        |         0.3608 |         0.3608 |      -6.61e-11 |      -2.69e-10 |
| 75%        |         0.5729 |         0.5729 |       1.33e-08 |       5.40e-08 |
| max        |         1.0000 |         1.0000 |         0.4256 |         1.7318 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,430,978

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.83e-06 |     2.06e-06 |      3.3242 |     0.001 |
| Slope       |       1.0000 |     4.42e-06 | 226426.0250 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EarningsTimeliness
     0   10002  200306            0.382373
     1   10002  200307            0.382373
     2   10002  200308            0.382373
     3   10002  200309            0.382373
     4   10002  200310            0.382373
     5   10002  200311            0.382373
     6   10002  200312            0.382373
     7   10002  200401            0.382373
     8   10002  200402            0.382373
     9   10002  200403            0.382373
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 15/1430978 (0.001%)
- Stata standard deviation: 2.46e-01

---

### EarningsValueRelevance

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsValueRelevance']

**Observations**:
- Stata:  1,427,774
- Python: 1,503,418
- Common: 1,427,774

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.44e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         0.3224 |         0.3224 |       1.41e-07 |       6.61e-07 |
| std        |         0.2136 |         0.2136 |       9.73e-05 |       4.55e-04 |
| min        |       5.13e-06 |       5.13e-06 |      -3.86e-07 |      -1.81e-06 |
| 25%        |         0.1458 |         0.1458 |      -9.53e-09 |      -4.46e-08 |
| 50%        |         0.2926 |         0.2926 |       3.59e-11 |       1.68e-10 |
| 75%        |         0.4707 |         0.4707 |       9.68e-09 |       4.53e-08 |
| max        |         0.9929 |         0.9929 |         0.0671 |         0.3142 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,427,774

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.14e-07 |     1.47e-07 |      2.1285 |     0.033 |
| Slope       |       1.0000 |     3.81e-07 |    2.62e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/1427774 (0.000%)
- Stata standard deviation: 2.14e-01

---

### EntMult_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 94 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EntMult_q']

**Observations**:
- Stata:  1,689,737
- Python: 1,691,109
- Common: 1,689,643

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.69e+06 |       1.69e+06 |       1.69e+06 |       1.69e+06 |
| mean       |        87.9017 |        87.9020 |       3.15e-04 |       1.01e-07 |
| std        |      3126.4162 |      3126.4162 |         0.7816 |       2.50e-04 |
| min        |    -43431.7380 |    -43431.7397 |      -269.0794 |        -0.0861 |
| 25%        |        20.2672 |        20.2673 |      -6.42e-07 |      -2.05e-10 |
| 50%        |        32.0420 |        32.0420 |      -1.58e-09 |      -5.05e-13 |
| 75%        |        51.5114 |        51.5114 |       6.38e-07 |       2.04e-10 |
| max        |       1.43e+06 |       1.43e+06 |       523.7859 |         0.1675 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,689,643

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.18e-04 |     6.02e-04 |      0.5283 |     0.597 |
| Slope       |       1.0000 |     1.92e-07 |    5.20e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  EntMult_q
     0   11545  199706  47.009804
     1   11545  199707  56.398899
     2   11545  199708  64.223152
     3   12373  202403  52.285816
     4   12373  202404  49.820324
     5   12373  202405  50.198395
     6   12750  198212 143.219590
     7   12750  198301 138.307430
     8   12750  198302 149.359800
     9   16564  199506  26.425295
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19/1689643 (0.001%)
- Stata standard deviation: 3.13e+03

---

### FailureProbability

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbability']

**Observations**:
- Stata:  1,958,798
- Python: 2,420,937
- Common: 1,958,798

**Precision1**: 0.105% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.07e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |       1.08e+06 |       1.09e+06 |     12405.6305 |       5.80e-04 |
| std        |       2.14e+07 |       4.97e+07 |       4.46e+07 |         2.0884 |
| min        |       -10.0057 |       -10.4365 |      -6.77e+08 |       -31.6501 |
| 25%        |        -5.9270 |        -5.9199 |        -0.0106 |      -4.97e-10 |
| 50%        |        -4.5351 |        -4.5382 |       3.85e-05 |       1.80e-12 |
| 75%        |        -2.0932 |        -2.1069 |         0.0198 |       9.28e-10 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       459.8211 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -7605.8682 + 1.0185 * stata
- **R-squared**: 0.1922
- **N observations**: 1,958,798

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   -7605.8682 |   31940.5746 |     -0.2381 |     0.812 |
| Slope       |       1.0185 |       0.0015 |    682.6224 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2063/1958798 (0.105%)
- Stata standard deviation: 2.14e+07

---

### FailureProbabilityJune

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FailureProbabilityJune']

**Observations**:
- Stata:  2,090,935
- Python: 2,558,215
- Common: 2,090,935

**Precision1**: 0.206% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.70e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.09e+06 |       2.09e+06 |       2.09e+06 |       2.09e+06 |
| mean       |       1.03e+06 |       1.07e+06 |     38140.0656 |         0.0018 |
| std        |       2.07e+07 |       4.99e+07 |       4.52e+07 |         2.1840 |
| min        |        -9.7055 |        -9.7215 |      -6.77e+08 |       -32.6947 |
| 25%        |        -5.9385 |        -5.9354 |        -0.0147 |      -7.09e-10 |
| 50%        |        -4.5879 |        -4.5868 |       3.93e-05 |       1.90e-12 |
| 75%        |        -2.2171 |        -2.2137 |         0.0190 |       9.17e-10 |
| max        |       6.77e+08 |       1.05e+10 |       9.83e+09 |       474.9975 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 16500.0612 + 1.0209 * stata
- **R-squared**: 0.1793
- **N observations**: 2,090,935

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |   16500.0612 |   31295.8407 |      0.5272 |     0.598 |
| Slope       |       1.0209 |       0.0015 |    675.9851 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 4317/2090935 (0.206%)
- Stata standard deviation: 2.07e+07

---

### ForecastDispersionLT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1774 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ForecastDispersionLT']

**Observations**:
- Stata:  828,578
- Python: 828,784
- Common: 826,804

**Precision1**: 0.087% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    826804.0000 |    826804.0000 |    826804.0000 |    826804.0000 |
| mean       |         4.5453 |         4.5451 |      -1.46e-04 |      -2.17e-05 |
| std        |         6.7281 |         6.7286 |         0.1312 |         0.0195 |
| min        |         0.0000 |         0.0000 |       -18.1600 |        -2.6991 |
| 25%        |         1.7100 |         1.7100 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         5.2000 |         5.2000 |       2.00e-08 |       2.97e-09 |
| max        |       623.7400 |       623.7400 |        41.1800 |         6.1206 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0004 + 0.9999 * stata
- **R-squared**: 0.9996
- **N observations**: 826,804

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.70e-04 |     1.74e-04 |      2.1263 |     0.033 |
| Slope       |       0.9999 |     2.14e-05 |  46632.5512 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ForecastDispersionLT
     0   11406  199609                  1.41
     1   11406  199610                  1.41
     2   12473  201012                  5.13
     3   12473  201101                  6.10
     4   12473  201710                  6.83
     5   12473  201711                  4.03
     6   12473  201712                  4.03
     7   12473  201801                  6.77
     8   12473  201802                  7.78
     9   12473  201803                  7.75
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 717/826804 (0.087%)
- Stata standard deviation: 6.73e+00

---

### GPlag

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag']

**Observations**:
- Stata:  3,281,500
- Python: 3,297,874
- Common: 3,281,500

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.55e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.28e+06 |       3.28e+06 |       3.28e+06 |       3.28e+06 |
| mean       |         0.3420 |         0.3420 |      -2.68e-07 |      -2.36e-07 |
| std        |         1.1339 |         1.1339 |         0.0020 |         0.0018 |
| min        |       -28.7301 |       -28.7301 |        -0.2811 |        -0.2479 |
| 25%        |         0.0981 |         0.0981 |      -4.83e-09 |      -4.26e-09 |
| 50%        |         0.2774 |         0.2774 |         0.0000 |         0.0000 |
| 75%        |         0.4978 |         0.4978 |       4.90e-09 |       4.32e-09 |
| max        |       282.3216 |       282.3216 |         0.8837 |         0.7794 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,281,500

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.14e-06 |     1.17e-06 |      1.8357 |     0.066 |
| Slope       |       1.0000 |     9.85e-07 |    1.02e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/3281500 (0.006%)
- Stata standard deviation: 1.13e+00

---

### GPlag_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GPlag_q']

**Observations**:
- Stata:  2,216,580
- Python: 2,482,774
- Common: 2,216,580

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.78e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.22e+06 |       2.22e+06 |       2.22e+06 |       2.22e+06 |
| mean       |         0.0808 |         0.0808 |       9.25e-07 |       1.30e-06 |
| std        |         0.7089 |         0.7089 |         0.0021 |         0.0029 |
| min        |        -9.0482 |        -9.0482 |        -0.5642 |        -0.7959 |
| 25%        |         0.0314 |         0.0314 |      -1.36e-09 |      -1.92e-09 |
| 50%        |         0.0731 |         0.0731 |         0.0000 |         0.0000 |
| 75%        |         0.1240 |         0.1240 |       1.36e-09 |       1.92e-09 |
| max        |       598.7442 |       598.7442 |         1.0085 |         1.4226 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,216,580

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.13e-06 |     1.40e-06 |      0.8087 |     0.419 |
| Slope       |       1.0000 |     1.96e-06 | 511432.2657 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 267/2216580 (0.012%)
- Stata standard deviation: 7.09e-01

---

### GrGMToGrSales

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrGMToGrSales']

**Observations**:
- Stata:  3,229,675
- Python: 3,279,256
- Common: 3,229,675

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.11e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |        -1.0320 |            inf |            inf |            inf |
| std        |       213.3399 |            N/A |            N/A |            N/A |
| min        |    -90231.3050 |    -89952.2742 |        -1.3321 |        -0.0062 |
| 25%        |        -0.0941 |        -0.0941 |      -2.50e-08 |      -1.17e-10 |
| 50%        |        -0.0024 |        -0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0784 |         0.0784 |       2.49e-08 |       1.17e-10 |
| max        |      7383.3198 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + nan * stata
- **R-squared**: nan
- **N observations**: 3,229,675

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/3229675 (0.002%)
- Stata standard deviation: 2.13e+02

---

### GrSaleToGrReceivables

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['GrSaleToGrReceivables']

**Observations**:
- Stata:  3,134,552
- Python: 3,303,855
- Common: 3,134,552

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.03e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.13e+06 |       3.13e+06 |       3.13e+06 |       3.13e+06 |
| mean       |        -0.7276 |        -0.7208 |         0.0068 |       2.50e-05 |
| std        |       272.2844 |       272.2685 |         2.4935 |         0.0092 |
| min        |    -93814.8910 |    -93814.8917 |      -122.8291 |        -0.4511 |
| 25%        |        -0.1435 |        -0.1435 |      -2.75e-09 |      -1.01e-11 |
| 50%        |         0.0056 |         0.0057 |       1.92e-12 |       7.06e-15 |
| 75%        |         0.1566 |         0.1568 |       2.77e-09 |       1.02e-11 |
| max        |     51770.8950 |     51770.8949 |      1176.6455 |         4.3214 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0067 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 3,134,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0067 |       0.0014 |      4.7865 |     0.000 |
| Slope       |       0.9999 |     5.17e-06 | 193323.0863 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 364/3134552 (0.012%)
- Stata standard deviation: 2.72e+02

---

### IdioVolCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 28814 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolCAPM']

**Observations**:
- Stata:  5,026,821
- Python: 4,998,007
- Common: 4,998,007

**Precision1**: 2.348% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.16e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.02e+06 |       5.02e+06 |       5.02e+06 |       5.02e+06 |
| mean       |         0.0273 |         0.0273 |      -3.09e-05 |        -0.0010 |
| std        |         0.0305 |         0.0305 |         0.0027 |         0.0874 |
| min        |         0.0000 |         0.0000 |        -2.7238 |       -89.2702 |
| 25%        |         0.0113 |         0.0112 |      -2.60e-17 |      -8.53e-16 |
| 50%        |         0.0195 |         0.0195 |         0.0000 |         0.0000 |
| 75%        |         0.0337 |         0.0337 |       2.78e-17 |       9.10e-16 |
| max        |         8.4129 |         8.4129 |         1.0441 |        34.2197 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9961 * stata
- **R-squared**: 0.9924
- **N observations**: 5,019,669

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.53e-05 |     1.59e-06 |     47.2005 |     0.000 |
| Slope       |       0.9961 |     3.90e-05 |  25566.6347 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolCAPM
     0   10000  198706 0.000000e+00
     1   10001  201708 8.975916e-04
     2   10004  198601 0.000000e+00
     3   10005  199107 4.418356e-02
     4   10007  198902 7.370520e-02
     5   10009  200011 3.122368e-04
     6   10011  199802 1.508194e-02
     7   10012  198601 4.278900e-02
     8   10012  198710 1.201176e-01
     9   10012  200508 4.906539e-18
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 117869/5019669 (2.348%)
- Stata standard deviation: 3.05e-02

---

### IdioVolQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30563 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolQF']

**Observations**:
- Stata:  3,986,461
- Python: 3,955,898
- Common: 3,955,898

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.10e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.96e+06 |       3.96e+06 |       3.96e+06 |       3.96e+06 |
| mean       |         0.0255 |         0.0255 |      -6.90e-13 |      -2.53e-11 |
| std        |         0.0273 |         0.0273 |       3.02e-10 |       1.11e-08 |
| min        |         0.0000 |         0.0000 |      -3.93e-08 |      -1.44e-06 |
| 25%        |         0.0106 |         0.0106 |      -7.35e-11 |      -2.70e-09 |
| 50%        |         0.0185 |         0.0185 |      -3.08e-20 |      -1.13e-18 |
| 75%        |         0.0316 |         0.0316 |       7.29e-11 |       2.68e-09 |
| max        |         3.4183 |         3.4183 |       9.48e-08 |       3.48e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,955,898

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.09e-12 |     2.08e-13 |    -10.0808 |     0.000 |
| Slope       |       1.0000 |     5.56e-12 |    1.80e+11 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    IdioVolQF
     0   10000  198706 5.849607e-19
     1   10002  201302 6.958739e-03
     2   10003  198601 1.861721e-02
     3   10003  199512 1.487973e-02
     4   10005  198601 4.759861e-02
     5   10005  199107 4.180065e-02
     6   10007  198601 2.829195e-02
     7   10007  199010 2.182299e-01
     8   10008  198601 1.745024e-02
     9   10009  198601 1.959985e-02
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3955898 (0.000%)
- Stata standard deviation: 2.73e-02

---

### KZ

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ']

**Observations**:
- Stata:  2,630,499
- Python: 2,663,058
- Common: 2,630,499

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.04e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.63e+06 |       2.63e+06 |       2.63e+06 |       2.63e+06 |
| mean       |       -34.2550 |       -34.2550 |      -4.84e-05 |      -1.55e-08 |
| std        |      3118.1767 |      3118.1767 |         0.0315 |       1.01e-05 |
| min        |      -1.23e+06 |      -1.23e+06 |       -19.2429 |        -0.0062 |
| 25%        |        -5.2581 |        -5.2582 |      -4.09e-08 |      -1.31e-11 |
| 50%        |        -0.6982 |        -0.6982 |       1.24e-11 |       3.97e-15 |
| 75%        |         1.0179 |         1.0179 |       4.08e-08 |       1.31e-11 |
| max        |    205925.8400 |    205925.8463 |         3.3978 |         0.0011 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,630,499

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.84e-05 |     1.94e-05 |     -2.4895 |     0.013 |
| Slope       |       1.0000 |     6.23e-09 |    1.60e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2630499 (0.000%)
- Stata standard deviation: 3.12e+03

---

### KZ_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 255 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ_q']

**Observations**:
- Stata:  1,936,942
- Python: 1,953,037
- Common: 1,936,687

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.12e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.94e+06 |       1.94e+06 |       1.94e+06 |       1.94e+06 |
| mean       |       -26.0737 |       -26.0742 |      -5.17e-04 |      -2.91e-07 |
| std        |      1776.1958 |      1776.1958 |         0.3830 |       2.16e-04 |
| min        |      -1.23e+06 |      -1.23e+06 |      -256.0814 |        -0.1442 |
| 25%        |        -4.8604 |        -4.8607 |      -3.96e-08 |      -2.23e-11 |
| 50%        |        -0.2486 |        -0.2486 |      -5.06e-12 |      -2.85e-15 |
| 75%        |         1.2951 |         1.2951 |       3.94e-08 |       2.22e-11 |
| max        |     26732.3870 |     26732.3858 |       130.4051 |         0.0734 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0005 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,936,687

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.18e-04 |     2.75e-04 |     -1.8810 |     0.060 |
| Slope       |       1.0000 |     1.55e-07 |    6.45e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm      KZ_q
     0   10515  199604 -4.790903
     1   10515  199605 -4.929575
     2   10515  199606 -4.921965
     3   10986  199008  8.309092
     4   10994  199204  5.937374
     5   10994  199205  6.358468
     6   11212  199008 -1.955831
     7   11545  199612 -1.467011
     8   11545  199701 -1.472400
     9   11545  199702 -1.472400
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 20/1936687 (0.001%)
- Stata standard deviation: 1.78e+03

---

### LaborforceEfficiency

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['LaborforceEfficiency']

**Observations**:
- Stata:  2,974,260
- Python: 3,073,530
- Common: 2,974,260

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.28e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.97e+06 |       2.97e+06 |       2.97e+06 |       2.97e+06 |
| mean       |         0.5044 |         0.5043 |      -3.97e-05 |      -1.08e-06 |
| std        |        36.7045 |        36.7045 |         0.0199 |       5.43e-04 |
| min        |      -247.4286 |      -247.4286 |        -9.9206 |        -0.2703 |
| 25%        |        -0.0439 |        -0.0439 |      -2.62e-08 |      -7.15e-10 |
| 50%        |         0.0510 |         0.0510 |         0.0000 |         0.0000 |
| 75%        |         0.1598 |         0.1598 |       2.63e-08 |       7.16e-10 |
| max        |     11615.4880 |     11615.4889 |         0.1038 |         0.0028 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,974,260

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.95e-05 |     1.16e-05 |     -3.4220 |     0.001 |
| Slope       |       1.0000 |     3.15e-07 |    3.18e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2974260 (0.000%)
- Stata standard deviation: 3.67e+01

---

### Leverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 67 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Leverage_q']

**Observations**:
- Stata:  2,571,833
- Python: 2,571,800
- Common: 2,571,766

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.47e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |         2.8298 |         2.8298 |       1.84e-06 |       9.83e-08 |
| std        |        18.6726 |        18.6726 |         0.0018 |       9.66e-05 |
| min        |       -11.0632 |       -11.0632 |        -0.1521 |        -0.0081 |
| 25%        |         0.2307 |         0.2307 |      -1.17e-08 |      -6.26e-10 |
| 50%        |         0.6768 |         0.6768 |      -2.03e-12 |      -1.09e-13 |
| 75%        |         2.0022 |         2.0022 |       1.16e-08 |       6.22e-10 |
| max        |      8843.3477 |      8843.3475 |         2.0802 |         0.1114 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,571,766

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.86e-06 |     1.14e-06 |      1.6312 |     0.103 |
| Slope       |       1.0000 |     6.02e-08 |    1.66e+07 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  Leverage_q
     0   10515  199604    0.207634
     1   10515  199605    0.534574
     2   10515  199606    0.492051
     3   11545  199706    0.042305
     4   11545  199707    0.036492
     5   11545  199708    0.032743
     6   12750  198212    0.127148
     7   12750  198301    0.131946
     8   12750  198302    0.121620
     9   12837  198004    0.933059
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/2571766 (0.000%)
- Stata standard deviation: 1.87e+01

---

### NetDebtPrice_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 40 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtPrice_q']

**Observations**:
- Stata:  1,178,409
- Python: 1,219,765
- Common: 1,178,369

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.85e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.18e+06 |       1.18e+06 |       1.18e+06 |       1.18e+06 |
| mean       |         1.0138 |         1.0138 |       1.65e-06 |       2.40e-07 |
| std        |         6.8787 |         6.8787 |         0.0013 |       1.87e-04 |
| min        |      -142.3929 |      -142.3929 |        -0.0512 |        -0.0074 |
| 25%        |        -0.0768 |        -0.0768 |      -8.22e-09 |      -1.20e-09 |
| 50%        |         0.2984 |         0.2984 |       1.28e-12 |       1.86e-13 |
| 75%        |         0.9501 |         0.9501 |       8.29e-09 |       1.20e-09 |
| max        |      2492.7185 |      2492.7185 |         1.3700 |         0.1992 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,178,369

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.66e-06 |     1.20e-06 |      1.3845 |     0.166 |
| Slope       |       1.0000 |     1.72e-07 |    5.80e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  NetDebtPrice_q
     0   10515  199604       -0.342635
     1   10515  199605       -0.882147
     2   10515  199606       -0.811976
     3   12837  198004        0.438865
     4   23033  202412       -0.213396
     5   23792  202412        0.499986
     6   23863  202412       -0.402767
     7   25786  198806       -1.045119
     8   25786  198807       -1.081157
     9   25786  198808       -1.119770
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6/1178369 (0.001%)
- Stata standard deviation: 6.88e+00

---

### NetPayoutYield_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetPayoutYield_q']

**Observations**:
- Stata:  2,520,037
- Python: 2,622,217
- Common: 2,520,037

**Precision1**: 0.016% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.53e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.52e+06 |       2.52e+06 |       2.52e+06 |       2.52e+06 |
| mean       |         0.0042 |         0.0042 |       1.30e-06 |       4.29e-06 |
| std        |         0.3030 |         0.3030 |         0.0019 |         0.0062 |
| min        |      -193.6226 |      -193.6226 |        -0.9269 |        -3.0591 |
| 25%        |      -1.53e-04 |      -1.53e-04 |      -5.93e-11 |      -1.96e-10 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0100 |         0.0100 |       5.96e-11 |       1.97e-10 |
| max        |       195.8306 |       195.8306 |         0.8013 |         2.6445 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,520,037

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.36e-06 |     1.18e-06 |      1.1551 |     0.248 |
| Slope       |       1.0000 |     3.89e-06 | 257308.7854 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 401/2520037 (0.016%)
- Stata standard deviation: 3.03e-01

---

### OPLeverage_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 65 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OPLeverage_q']

**Observations**:
- Stata:  2,546,734
- Python: 2,546,725
- Common: 2,546,669

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.72e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.2547 |         0.2547 |       6.51e-06 |       1.35e-05 |
| std        |         0.4836 |         0.4836 |         0.0049 |         0.0101 |
| min        |        -1.4798 |        -1.4798 |        -1.3312 |        -2.7526 |
| 25%        |         0.0824 |         0.0824 |      -3.41e-09 |      -7.06e-09 |
| 50%        |         0.1983 |         0.1983 |      -1.96e-12 |      -4.06e-12 |
| 75%        |         0.3378 |         0.3378 |       3.40e-09 |       7.03e-09 |
| max        |       280.5029 |       280.5029 |         3.8251 |         7.9096 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,546,669

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.93e-06 |     3.46e-06 |      2.8667 |     0.004 |
| Slope       |       1.0000 |     6.34e-06 | 157786.5763 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OPLeverage_q
     0   10515  199604      0.205151
     1   10515  199605      0.205151
     2   10515  199606      0.205151
     3   11545  199706      0.157832
     4   11545  199707      0.157832
     5   11545  199708      0.157832
     6   12750  198212      0.294411
     7   12750  198301      0.294411
     8   12750  198302      0.294411
     9   12837  198004      0.584828
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 235/2546669 (0.009%)
- Stata standard deviation: 4.84e-01

---

### OScore_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore_q']

**Observations**:
- Stata:  877,922
- Python: 2,823,459
- Common: 877,922

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    877922.0000 |    872102.0000 |    872102.0000 |    872102.0000 |
| mean       |         0.1247 |         0.1194 |         0.0000 |         0.0000 |
| std        |         0.3304 |         0.3243 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 872,102

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.19e-14 |     2.64e-16 |   -310.4659 |     0.000 |
| Slope       |       1.0000 |     7.63e-16 |    1.31e+15 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/877922 (0.000%)
- Stata standard deviation: 3.30e-01

---

### OperProfLag

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag']

**Observations**:
- Stata:  1,292,263
- Python: 1,809,262
- Common: 1,292,263

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.44e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.29e+06 |       1.29e+06 |       1.29e+06 |       1.29e+06 |
| mean       |         0.2732 |         0.2732 |      -2.20e-07 |      -3.15e-08 |
| std        |         6.9919 |         6.9919 |       4.82e-04 |       6.89e-05 |
| min        |     -1594.7000 |     -1594.7000 |        -0.1205 |        -0.0172 |
| 25%        |         0.1432 |         0.1432 |      -5.76e-09 |      -8.24e-10 |
| 50%        |         0.2805 |         0.2805 |       2.22e-16 |       3.18e-17 |
| 75%        |         0.4266 |         0.4266 |       5.79e-09 |       8.28e-10 |
| max        |      1096.4845 |      1096.4845 |         0.0741 |         0.0106 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,292,263

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.14e-07 |     4.24e-07 |     -0.5056 |     0.613 |
| Slope       |       1.0000 |     6.06e-08 |    1.65e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/1292263 (0.002%)
- Stata standard deviation: 6.99e+00

---

### OperProfLag_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfLag_q']

**Observations**:
- Stata:  2,395,707
- Python: 2,579,758
- Common: 2,395,707

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.15e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |       -70.1478 |            N/A |            N/A |            N/A |
| std        |    252624.5138 |            N/A |            N/A |            N/A |
| min        |      -3.48e+08 |           -inf |           -inf |           -inf |
| 25%        |        -0.0048 |        -0.0274 |      -2.69e-08 |      -1.07e-13 |
| 50%        |         0.0444 |         0.0372 |      -2.28e-09 |      -9.04e-15 |
| 75%        |         0.0849 |         0.0767 |       4.61e-09 |       1.82e-14 |
| max        |       9.52e+07 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,395,707

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/2395707 (0.001%)
- Stata standard deviation: 2.53e+05

---

### OperProfRDLagAT

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT']

**Observations**:
- Stata:  2,742,767
- Python: 2,948,224
- Common: 2,742,767

**Precision1**: 4.539% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.20e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.74e+06 |       2.74e+06 |       2.74e+06 |       2.74e+06 |
| mean       |         0.1294 |         0.1345 |         0.0051 |         0.0043 |
| std        |         1.1878 |         1.1902 |         0.0735 |         0.0619 |
| min        |      -200.7273 |      -200.7273 |        -1.0772 |        -0.9068 |
| 25%        |         0.0319 |         0.0327 |      -2.15e-09 |      -1.81e-09 |
| 50%        |         0.1281 |         0.1303 |       3.09e-10 |       2.60e-10 |
| 75%        |         0.2154 |         0.2197 |       4.69e-09 |       3.95e-09 |
| max        |       226.5365 |       226.5365 |         6.8470 |         5.7642 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0051 + 1.0001 * stata
- **R-squared**: 0.9962
- **N observations**: 2,742,767

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0051 |     4.47e-05 |    114.0592 |     0.000 |
| Slope       |       1.0001 |     3.74e-05 |  26760.4335 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 124482/2742767 (4.539%)
- Stata standard deviation: 1.19e+00

---

### OperProfRDLagAT_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 114 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT_q']

**Observations**:
- Stata:  1,800,025
- Python: 1,799,984
- Common: 1,799,911

**Precision1**: 0.013% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.55e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.80e+06 |       1.80e+06 |       1.80e+06 |       1.80e+06 |
| mean       |         0.0249 |         0.0249 |       3.77e-07 |       2.86e-06 |
| std        |         0.1317 |         0.1317 |         0.0013 |         0.0101 |
| min        |       -10.0000 |       -10.0000 |        -0.4027 |        -3.0571 |
| 25%        |         0.0110 |         0.0110 |      -7.24e-10 |      -5.50e-09 |
| 50%        |         0.0317 |         0.0317 |         0.0000 |         0.0000 |
| 75%        |         0.0522 |         0.0522 |       7.22e-10 |       5.48e-09 |
| max        |        54.3953 |        54.3953 |         0.6825 |         5.1816 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 1,799,911

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.99e-06 |     1.01e-06 |      2.9597 |     0.003 |
| Slope       |       0.9999 |     7.54e-06 | 132622.0694 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OperProfRDLagAT_q
     0   10515  199607           0.007740
     1   10515  199608           0.007740
     2   10515  199609           0.007740
     3   10517  202006           0.168328
     4   10517  202007           0.168328
     5   10517  202008           0.168328
     6   10517  202009           0.160288
     7   10517  202010           0.160288
     8   10517  202011           0.160288
     9   10517  202012           0.194064
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 235/1799911 (0.013%)
- Stata standard deviation: 1.32e-01

---

### PM

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM']

**Observations**:
- Stata:  3,547,773
- Python: 3,616,815
- Common: 3,547,773

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.55e+06 |       3.55e+06 |       3.55e+06 |       3.55e+06 |
| mean       |        -4.0283 |        -4.0283 |      -1.02e-06 |      -4.83e-09 |
| std        |       211.9918 |       211.9919 |       4.41e-04 |       2.08e-06 |
| min        |    -84221.6640 |    -84221.6667 |        -0.1893 |      -8.93e-04 |
| 25%        |        -0.0177 |        -0.0177 |      -1.41e-09 |      -6.64e-12 |
| 50%        |         0.0398 |         0.0398 |         0.0000 |         0.0000 |
| 75%        |         0.0957 |         0.0957 |       1.42e-09 |       6.69e-12 |
| max        |     10418.0800 |     10418.0800 |         0.0391 |       1.85e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,547,773

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.60e-07 |     2.34e-07 |     -4.1007 |     0.000 |
| Slope       |       1.0000 |     1.10e-09 |    9.05e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3547773 (0.000%)
- Stata standard deviation: 2.12e+02

---

### PM_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PM_q']

**Observations**:
- Stata:  2,492,083
- Python: 2,823,459
- Common: 2,492,083

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.86e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -3.9606 |        -3.9377 |         0.0229 |       1.34e-04 |
| std        |       171.1246 |       174.3678 |        33.4642 |         0.1956 |
| min        |    -64982.0000 |    -64982.0000 |     -9330.2298 |       -54.5230 |
| 25%        |        -0.0250 |        -0.0250 |      -1.28e-09 |      -7.50e-12 |
| 50%        |         0.0340 |         0.0340 |         0.0000 |         0.0000 |
| 75%        |         0.0816 |         0.0816 |       1.28e-09 |       7.46e-12 |
| max        |     18403.0000 |     28930.0000 |     28930.3781 |       169.0603 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0230 + 1.0000 * stata
- **R-squared**: 0.9632
- **N observations**: 2,492,083

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0230 |       0.0212 |      1.0826 |     0.279 |
| Slope       |       1.0000 |     1.24e-04 |   8072.6926 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 34/2492083 (0.001%)
- Stata standard deviation: 1.71e+02

---

### PS_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 17 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['PS_q']

**Observations**:
- Stata:  310,650
- Python: 371,767
- Common: 310,633

**Precision1**: 53.350% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.16e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    310633.0000 |    310633.0000 |    310633.0000 |    310633.0000 |
| mean       |         5.2218 |         4.7231 |        -0.4987 |        -0.3154 |
| std        |         1.5810 |         1.7963 |         1.5059 |         0.9525 |
| min        |         1.0000 |         1.0000 |        -6.0000 |        -3.7950 |
| 25%        |         4.0000 |         3.0000 |        -1.0000 |        -0.6325 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         2.0000 |         1.2650 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1.1103 + 0.6919 * stata
- **R-squared**: 0.3708
- **N observations**: 310,633

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       1.1103 |       0.0088 |    125.8503 |     0.000 |
| Slope       |       0.6919 |       0.0016 |    427.8576 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  PS_q
     0   10515  199604   5.0
     1   10515  199605   6.0
     2   10515  199606   6.0
     3   16965  201812   6.0
     4   16965  201901   6.0
     5   16965  201902   6.0
     6   20637  202407   6.0
     7   66617  201309   2.0
     8   76200  199308   5.0
     9   81124  202406   5.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 165723/310633 (53.350%)
- Stata standard deviation: 1.58e+00

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   11174  202412     2.0    3.0  -1.0
1   11593  202412     8.0    7.0   1.0
2   11701  202412     5.0    6.0  -1.0
3   11775  202412     6.0    7.0  -1.0
4   11790  202412     4.0    5.0  -1.0
5   12880  202412     5.0    6.0  -1.0
6   13116  202412     6.0    5.0   1.0
7   13124  202412     6.0    5.0   1.0
8   13337  202412     4.0    5.0  -1.0
9   13583  202412     3.0    8.0  -5.0
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10005  198706     1.0    7.0  -6.0
1   10005  198707     1.0    7.0  -6.0
2   10005  198708     1.0    7.0  -6.0
3   10005  198709     1.0    7.0  -6.0
4   10005  198710     1.0    7.0  -6.0
5   10005  198711     1.0    7.0  -6.0
6   10005  198712     2.0    8.0  -6.0
7   10005  198801     2.0    8.0  -6.0
8   10005  198802     2.0    8.0  -6.0
9   10005  198803     1.0    7.0  -6.0
```

---

### PayoutYield_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PayoutYield_q']

**Observations**:
- Stata:  1,310,000
- Python: 2,891,504
- Common: 1,310,000

**Precision1**: 0.015% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.46e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.31e+06 |       1.31e+06 |       1.31e+06 |       1.31e+06 |
| mean       |         0.0309 |         0.0309 |       1.97e-06 |       5.73e-06 |
| std        |         0.3442 |         0.3442 |       8.28e-04 |         0.0024 |
| min        |       1.15e-17 |      -9.53e-04 |        -0.2764 |        -0.8031 |
| 25%        |         0.0045 |         0.0045 |      -2.39e-10 |      -6.95e-10 |
| 50%        |         0.0106 |         0.0106 |      -1.32e-14 |      -3.83e-14 |
| 75%        |         0.0230 |         0.0230 |       2.40e-10 |       6.97e-10 |
| max        |       217.7060 |       217.7060 |         0.3121 |         0.9067 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,310,000

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.00e-06 |     7.27e-07 |      2.7569 |     0.006 |
| Slope       |       1.0000 |     2.10e-06 | 475597.0553 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 201/1310000 (0.015%)
- Stata standard deviation: 3.44e-01

---

### RD_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RD_q']

**Observations**:
- Stata:  833,583
- Python: 3,038,208
- Common: 833,583

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.19e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    833583.0000 |    833583.0000 |    833583.0000 |    833583.0000 |
| mean       |         0.0298 |         0.0298 |      -1.39e-06 |      -8.40e-06 |
| std        |         0.1656 |         0.1656 |       4.91e-04 |         0.0030 |
| min        |        -1.5270 |        -1.5270 |        -0.2737 |        -1.6526 |
| 25%        |         0.0024 |         0.0024 |      -1.71e-10 |      -1.03e-09 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0278 |         0.0278 |       1.71e-10 |       1.03e-09 |
| max        |        98.7289 |        98.7289 |         0.0221 |         0.1332 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 833,583

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.12e-06 |     5.46e-07 |     -2.0562 |     0.040 |
| Slope       |       1.0000 |     3.25e-06 | 307992.3745 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 59/833583 (0.007%)
- Stata standard deviation: 1.66e-01

---

### RetNOA

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA']

**Observations**:
- Stata:  2,892,942
- Python: 3,012,996
- Common: 2,892,942

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-19 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.89e+06 |       2.89e+06 |       2.89e+06 |       2.89e+06 |
| mean       |       2.31e+11 |            inf |            inf |            inf |
| std        |       1.27e+14 |            N/A |            N/A |            N/A |
| min        |      -5.90e+15 |      -5.90e+15 |      -1.75e+09 |      -1.37e-05 |
| 25%        |        -0.0320 |        -0.0320 |      -6.74e-09 |      -5.29e-23 |
| 50%        |         0.1203 |         0.1203 |      -1.19e-12 |      -9.33e-27 |
| 75%        |         0.2648 |         0.2648 |       6.73e-09 |       5.28e-23 |
| max        |       6.23e+16 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,892,942

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2892942 (0.001%)
- Stata standard deviation: 1.27e+14

---

### RetNOA_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['RetNOA_q']

**Observations**:
- Stata:  2,413,581
- Python: 3,041,661
- Common: 2,413,581

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.86e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |       -46.8886 |            N/A |            N/A |            N/A |
| std        |     46097.2088 |            N/A |            N/A |            N/A |
| min        |      -4.12e+07 |           -inf |           -inf |           -inf |
| 25%        |      -9.84e-04 |      -9.84e-04 |      -1.55e-09 |      -3.37e-14 |
| 50%        |         0.0288 |         0.0288 |      -4.62e-13 |      -1.00e-17 |
| 75%        |         0.0609 |         0.0609 |       1.54e-09 |       3.34e-14 |
| max        |       3.43e+06 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = nan + nan * stata
- **R-squared**: nan
- **N observations**: 2,413,581

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 29/2413581 (0.001%)
- Stata standard deviation: 4.61e+04

---

### ReturnSkewCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 37784 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkewCAPM']

**Observations**:
- Stata:  4,997,359
- Python: 4,959,575
- Common: 4,959,575

**Precision1**: 2.908% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.78e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.98e+06 |       4.98e+06 |       4.98e+06 |       4.98e+06 |
| mean       |         0.1853 |         0.1837 |        -0.0016 |        -0.0017 |
| std        |         0.9495 |         0.9474 |         0.1062 |         0.1118 |
| min        |        -4.9022 |        -4.9022 |        -7.8738 |        -8.2924 |
| 25%        |        -0.2796 |        -0.2808 |      -2.22e-16 |      -2.34e-16 |
| 50%        |         0.1560 |         0.1550 |         0.0000 |         0.0000 |
| 75%        |         0.6331 |         0.6315 |       2.22e-16 |       2.34e-16 |
| max        |         4.8256 |         4.8256 |         6.6541 |         7.0078 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9915 * stata
- **R-squared**: 0.9875
- **N observations**: 4,980,640

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.21e-05 |     4.83e-05 |     -0.6650 |     0.506 |
| Slope       |       0.9915 |     5.00e-05 |  19847.5088 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewCAPM
     0   10001  201708        0.532855
     1   10002  198706       -0.117148
     2   10002  199001        4.320210
     3   10002  199103       -2.666667
     4   10002  199107        0.132583
     5   10002  199111       -2.666667
     6   10005  198704        4.248529
     7   10005  198803       -2.931764
     8   10005  198806       -0.131841
     9   10005  198808        4.477215
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144854/4980640 (2.908%)
- Stata standard deviation: 9.50e-01

---

### ReturnSkewQF

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 30525 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkewQF']

**Observations**:
- Stata:  3,985,016
- Python: 3,955,898
- Common: 3,954,491

**Precision1**: 0.899% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.93e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.95e+06 |       3.94e+06 |       3.94e+06 |       3.94e+06 |
| mean       |         0.1399 |         0.1395 |      -7.25e-04 |      -8.77e-04 |
| std        |         0.8265 |         0.8309 |         0.1081 |         0.1308 |
| min        |        -4.4416 |        -4.4416 |        -6.3554 |        -7.6892 |
| 25%        |        -0.2864 |        -0.2874 |      -2.15e-08 |      -2.60e-08 |
| 50%        |         0.1203 |         0.1201 |       2.43e-10 |       2.95e-10 |
| 75%        |         0.5534 |         0.5540 |       2.19e-08 |       2.66e-08 |
| max        |         4.4416 |         4.4772 |         6.0899 |         7.3679 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 0.9960 * stata
- **R-squared**: 0.9831
- **N observations**: 3,941,791

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.65e-04 |     5.52e-05 |     -2.9956 |     0.003 |
| Slope       |       0.9960 |     6.58e-05 |  15135.9904 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewQF
     0   10000  198706      0.499660
     1   10002  201302      0.345465
     2   10003  198601      0.164571
     3   10003  199512      0.168800
     4   10005  198601     -1.189934
     5   10005  199107      1.837418
     6   10007  198601     -0.753537
     7   10007  199010     -1.225254
     8   10008  198601      0.281495
     9   10009  198601      0.921937
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 35562/3954491 (0.899%)
- Stata standard deviation: 8.27e-01

---

### SP_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 31 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SP_q']

**Observations**:
- Stata:  2,790,383
- Python: 2,790,383
- Common: 2,790,352

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.95e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.79e+06 |       2.79e+06 |       2.79e+06 |       2.79e+06 |
| mean       |         0.6076 |         0.6076 |      -7.85e-06 |      -4.34e-06 |
| std        |         1.8101 |         1.8101 |         0.0073 |         0.0040 |
| min        |       -31.7352 |       -31.7352 |        -4.6447 |        -2.5660 |
| 25%        |         0.1051 |         0.1051 |      -4.68e-09 |      -2.59e-09 |
| 50%        |         0.2523 |         0.2523 |         0.0000 |         0.0000 |
| 75%        |         0.5972 |         0.5972 |       4.67e-09 |       2.58e-09 |
| max        |       537.3825 |       537.3825 |         3.2442 |         1.7923 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,790,352

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.60e-06 |     4.61e-06 |     -0.3480 |     0.728 |
| Slope       |       1.0000 |     2.41e-06 | 414132.4540 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm     SP_q
     0   11545  199706 0.082241
     1   11545  199707 0.070940
     2   11545  199708 0.063652
     3   12837  198004 0.717490
     4   12837  198005 0.438482
     5   21346  197001 4.004309
     6   21346  197002 3.818679
     7   21346  197003 4.271263
     8   23792  202412 6.755312
     9   23863  202412 0.866520
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 127/2790352 (0.005%)
- Stata standard deviation: 1.81e+00

---

### Tax_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 52 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax_q']

**Observations**:
- Stata:  1,906,647
- Python: 1,906,650
- Common: 1,906,595

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.61e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         1.7501 |         1.7501 |       1.28e-05 |       7.96e-07 |
| std        |        16.1404 |        16.1405 |         0.0100 |       6.20e-04 |
| min        |       2.00e-06 |       2.00e-06 |        -0.8325 |        -0.0516 |
| 25%        |         1.2937 |         1.2936 |      -3.00e-08 |      -1.86e-09 |
| 50%        |         1.5463 |         1.5463 |         0.0000 |         0.0000 |
| 75%        |         1.7239 |         1.7239 |       3.03e-08 |       1.87e-09 |
| max        |     10630.3370 |     10630.3365 |         7.0000 |         0.4337 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,906,595

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.44e-06 |     7.29e-06 |      1.1579 |     0.247 |
| Slope       |       1.0000 |     4.49e-07 |    2.23e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    Tax_q
     0   10515  199604 1.604096
     1   10515  199605 1.604096
     2   10515  199606 1.604096
     3   11545  199706 1.449165
     4   11545  199707 1.449165
     5   11545  199708 1.449165
     6   11843  198803 0.940294
     7   11843  198804 0.940294
     8   11843  198805 0.940294
     9   12837  198004 1.881661
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40/1906595 (0.002%)
- Stata standard deviation: 1.61e+01

---

### WW

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW']

**Observations**:
- Stata:  2,702,805
- Python: 3,297,568
- Common: 2,702,805

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.49e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |        -0.1112 |        -0.1111 |       1.12e-05 |       2.04e-07 |
| std        |        54.8159 |        54.8159 |         0.0052 |       9.44e-05 |
| min        |      -111.6833 |      -111.6833 |        -2.7503 |        -0.0502 |
| 25%        |        -0.3470 |        -0.3470 |      -5.04e-09 |      -9.19e-11 |
| 50%        |        -0.2572 |        -0.2571 |       6.03e-12 |       1.10e-13 |
| 75%        |        -0.1745 |        -0.1745 |       5.04e-09 |       9.19e-11 |
| max        |     76241.1800 |     76241.1777 |         3.7323 |         0.0681 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,702,805

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.12e-05 |     3.15e-06 |      3.5521 |     0.000 |
| Slope       |       1.0000 |     5.74e-08 |    1.74e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 29/2702805 (0.001%)
- Stata standard deviation: 5.48e+01

---

### WW_Q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 44 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW_Q']

**Observations**:
- Stata:  2,406,602
- Python: 2,493,801
- Common: 2,406,558

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.62e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |        -0.0942 |           -inf |           -inf |           -inf |
| std        |        80.9101 |            N/A |            N/A |            N/A |
| min        |     -1099.2520 |           -inf |           -inf |           -inf |
| 25%        |        -0.3578 |        -0.3578 |      -6.01e-09 |      -7.42e-11 |
| 50%        |        -0.2663 |        -0.2663 |      -3.11e-12 |      -3.84e-14 |
| 75%        |        -0.1791 |        -0.1791 |       6.00e-09 |       7.41e-11 |
| max        |     75674.3520 |     75674.3568 |        15.5945 |         0.1927 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -inf + inf * stata
- **R-squared**: nan
- **N observations**: 2,406,551

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Missing Observations Sample**:
```
 index  permno  yyyymm      WW_Q
     0   10515  199604 -0.192867
     1   10515  199605 -0.198629
     2   10515  199606 -0.190664
     3   10535  198805  0.097225
     4   11545  199706 -0.169969
     5   11545  199707 -0.161824
     6   11545  199708 -0.155090
     7   12750  198212 -0.038403
     8   12750  198301 -0.042673
     9   12750  198302 -0.043110
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33/2406558 (0.001%)
- Stata standard deviation: 8.09e+01

---

### ZScore

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ZScore']

**Observations**:
- Stata:  1,669,459
- Python: 1,669,861
- Common: 1,669,459

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.31e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.67e+06 |       1.67e+06 |       1.67e+06 |       1.67e+06 |
| mean       |         5.9418 |         5.9418 |       1.93e-07 |       5.67e-09 |
| std        |        33.9664 |        33.9665 |       2.23e-06 |       6.56e-08 |
| min        |      -353.7195 |      -353.7195 |      -1.69e-04 |      -4.96e-06 |
| 25%        |         2.1706 |         2.1706 |      -1.81e-08 |      -5.34e-10 |
| 50%        |         3.4987 |         3.4987 |       5.01e-08 |       1.47e-09 |
| 75%        |         5.4589 |         5.4589 |       1.57e-07 |       4.63e-09 |
| max        |      8802.6084 |      8802.6093 |       8.92e-04 |       2.63e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,669,459

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.75e-08 |     1.38e-09 |    -34.3687 |     0.000 |
| Slope       |       1.0000 |     4.00e-11 |    2.50e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1669459 (0.000%)
- Stata standard deviation: 3.40e+01

---

### ZScore_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ZScore_q']

**Observations**:
- Stata:  1,214,174
- Python: 1,490,451
- Common: 1,214,174

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.18e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         4.2873 |         4.2873 |      -1.95e-06 |      -5.68e-08 |
| std        |        34.3037 |        34.3037 |         0.0081 |       2.36e-04 |
| min        |     -9318.5010 |     -9318.5014 |        -3.3394 |        -0.0973 |
| 25%        |         1.1057 |         1.1057 |      -2.51e-09 |      -7.32e-11 |
| 50%        |         1.9844 |         1.9844 |       3.75e-08 |       1.09e-09 |
| 75%        |         3.4886 |         3.4886 |       1.19e-07 |       3.47e-09 |
| max        |      9482.0879 |      9482.0889 |         2.9884 |         0.0871 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,214,174

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.07e-06 |     7.40e-06 |     -0.2799 |     0.780 |
| Slope       |       1.0000 |     2.14e-07 |    4.67e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 38/1214174 (0.003%)
- Stata standard deviation: 3.43e+01

---

### betaCC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1001412 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCC']

**Observations**:
- Stata:  3,459,006
- Python: 2,477,076
- Common: 2,457,594

**Precision1**: 61.569% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.99e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         6.4107 |         4.6771 |        -1.7336 |        -0.1016 |
| std        |        17.0566 |        15.9427 |        14.5064 |         0.8505 |
| min        |      -204.1360 |      -238.8489 |      -334.1474 |       -19.5905 |
| 25%        |         0.0451 |         0.0150 |        -0.8806 |        -0.0516 |
| 50%        |         0.4967 |         0.2618 |        -0.0424 |        -0.0025 |
| 75%        |         4.3344 |         2.8014 |         0.1097 |         0.0064 |
| max        |       375.9494 |       416.0598 |       322.3343 |        18.8979 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.9899 + 0.5752 * stata
- **R-squared**: 0.3787
- **N observations**: 2,457,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.9899 |       0.0086 |    115.5953 |     0.000 |
| Slope       |       0.5752 |     4.70e-04 |   1223.7935 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaCC
     0   10001  198912 96.556709
     1   10001  199001 78.446892
     2   10001  199002 81.491409
     3   10001  199003 77.058983
     4   10001  199004 69.123657
     5   10001  199005 65.499115
     6   10001  199006 62.682751
     7   10001  199007 54.436337
     8   10001  199008 59.355011
     9   10001  199009 56.830456
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1513127/2457594 (61.569%)
- Stata standard deviation: 1.71e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata       diff
0   10028  202412  62.922378  21.920418  41.001960
1   10044  202412  26.092065  23.439190   2.652875
2   10113  202412  16.103179  18.293459  -2.190280
3   10158  202412   1.969406   0.455747   1.513659
4   10207  202412   6.617960   4.409046   2.208914
5   10253  202412  55.701422  22.687012  33.014410
6   10257  202412  50.506467  15.757562  34.748905
7   10258  202412   4.722760   1.725508   2.997252
8   10333  202412   4.705993   3.627675   1.078318
9   10355  202412   6.555554   2.654729   3.900824
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   12353  201411 -238.848949   95.298477 -334.147426
1   77488  201710  138.534961 -183.799300  322.334261
2   93134  201402  416.059848  100.153070  315.906778
3   77488  201709  144.540290 -170.686610  315.226900
4   93134  201403  399.211885   96.516716  302.695169
5   12878  201507   73.338846  375.949400 -302.610554
6   77488  201708  146.038909 -154.166600  300.205509
7   93134  201404  391.599070   95.253258  296.345812
8   77488  201707  135.931150 -156.940780  292.871930
9   91636  199511 -134.736190  157.277800 -292.013990
```

---

### betaCR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 1001412 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaCR']

**Observations**:
- Stata:  3,459,006
- Python: 2,477,076
- Common: 2,457,594

**Precision1**: 56.468% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.83e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |        -7.4593 |        -5.7299 |         1.7295 |         0.0638 |
| std        |        27.1048 |        24.4228 |        16.4230 |         0.6059 |
| min        |      -453.6021 |      -448.1695 |      -301.2645 |       -11.1148 |
| 25%        |        -3.7425 |        -2.9250 |        -0.2614 |        -0.0096 |
| 50%        |        -0.3487 |        -0.2659 |         0.0045 |       1.64e-04 |
| 75%        |        -0.0127 |        -0.0113 |         0.6986 |         0.0258 |
| max        |       469.9789 |       457.2326 |       398.0246 |        14.6847 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.3414 + 0.7224 * stata
- **R-squared**: 0.6427
- **N observations**: 2,457,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.3414 |       0.0097 |    -35.3465 |     0.000 |
| Slope       |       0.7224 |     3.44e-04 |   2102.7263 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaCR
     0   10001  198912 -4.462341
     1   10001  199001  7.927080
     2   10001  199002 10.556782
     3   10001  199003 10.227539
     4   10001  199004 17.441637
     5   10001  199005 14.496083
     6   10001  199006  7.174622
     7   10001  199007  8.668968
     8   10001  199008 -8.670435
     9   10001  199009 -8.461947
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1387753/2457594 (56.468%)
- Stata standard deviation: 2.71e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata       diff
0   10028  202412  34.869606  15.126258  19.743348
1   10044  202412 -42.042942 -51.162571   9.119629
2   10113  202412 -29.251628 -33.305286   4.053658
3   10207  202412  -2.183358  -4.013835   1.830477
4   10253  202412 -36.802231 -14.677695 -22.124536
5   10257  202412 -25.185999 -31.312153   6.126154
6   10308  202412  -0.007633  -0.377225   0.369592
7   10333  202412   0.657261  -0.421896   1.079157
8   10355  202412  -8.440257  -9.463994   1.023737
9   10463  202412 -45.948254 -48.889687   2.941433
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   88725  200710   -1.063757 -399.088320  398.024563
1   83882  200710    8.820300 -383.429570  392.249870
2   84030  200710   -4.658101 -396.349550  391.691449
3   91636  199602  433.056602   46.790867  386.265735
4   84030  200709   -4.749141 -390.758730  386.009589
5   91636  199604  423.630484   39.016193  384.614291
6   85776  200706  199.616307 -183.112790  382.729097
7   83882  200712    8.277843 -370.866670  379.144513
8   84030  200712  -13.092411 -387.985050  374.892639
9   91636  199603  411.904078   39.658962  372.245116
```

---

### betaNet

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 962997 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaNet']

**Observations**:
- Stata:  3,420,591
- Python: 2,477,076
- Common: 2,457,594

**Precision1**: 63.110% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.97e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |        14.5811 |        11.1329 |        -3.4482 |        -0.0907 |
| std        |        38.0337 |        35.2954 |        23.9648 |         0.6301 |
| min        |      -527.2736 |      -609.2294 |      -676.3739 |       -17.7835 |
| 25%        |         0.7139 |         0.5970 |        -1.6110 |        -0.0424 |
| 50%        |         1.8144 |         1.4633 |        -0.0593 |        -0.0016 |
| 75%        |         9.5909 |         6.7991 |         0.3672 |         0.0097 |
| max        |       587.6557 |       656.8489 |       389.1643 |        10.2321 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.4583 + 0.7321 * stata
- **R-squared**: 0.6223
- **N observations**: 2,457,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.4583 |       0.0148 |     30.9259 |     0.000 |
| Slope       |       0.7321 |     3.64e-04 |   2012.4101 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaNet
     0   10001  198912 101.080060
     1   10001  199001  70.609283
     2   10001  199002  71.023659
     3   10001  199003  66.917381
     4   10001  199004  51.771923
     5   10001  199005  51.066372
     6   10001  199006  55.570599
     7   10001  199007  45.826405
     8   10001  199008  68.131134
     9   10001  199009  65.379723
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1550991/2457594 (63.110%)
- Stata standard deviation: 3.80e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm     python      stata       diff
0   10028  202412  28.627420   7.307667  21.319752
1   10044  202412  68.833331  75.308937  -6.475606
2   10113  202412  46.200880  52.441204  -6.240324
3   10158  202412   4.858252   3.256010   1.602242
4   10207  202412   9.630439   9.244012   0.386427
5   10253  202412  93.725203  38.610798  55.114405
6   10257  202412  76.658143  47.998154  28.659989
7   10258  202412  28.609746  25.298738   3.311008
8   10308  202412   0.725786   1.229633  -0.503846
9   10355  202412  15.728702  12.896639   2.832063
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   91636  199602 -609.229395   67.144463 -676.373858
1   91636  199603 -556.757065   68.578629 -625.335694
2   91636  199604 -553.921115   60.991245 -614.912360
3   91636  199511 -478.126123  104.688450 -582.814573
4   84030  200710    8.627707  587.655700 -579.027993
5   11554  199311 -537.828689   32.305172 -570.133861
6   84030  200709    9.044902  575.808840 -566.763938
7   11554  199312 -533.394205   33.141479 -566.535684
8   91636  199512 -478.126123   87.731339 -565.857462
9   91636  199601 -484.487667   65.834572 -550.322239
```

---

### betaRC

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 963966 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRC']

**Observations**:
- Stata:  3,421,560
- Python: 2,477,076
- Common: 2,457,594

**Precision1**: 96.955% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.85e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |        -0.1536 |        -0.1416 |         0.0120 |         0.0591 |
| std        |         0.2029 |         0.1917 |         0.1510 |         0.7443 |
| min        |        -7.6796 |        -5.6080 |        -6.0458 |       -29.7915 |
| 25%        |        -0.2469 |        -0.2265 |        -0.0378 |        -0.1864 |
| 50%        |        -0.1368 |        -0.1220 |         0.0086 |         0.0425 |
| 75%        |        -0.0422 |        -0.0388 |         0.0580 |         0.2860 |
| max        |         6.1166 |         7.6160 |         7.3917 |        36.4234 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0388 + 0.6690 * stata
- **R-squared**: 0.5018
- **N observations**: 2,457,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0388 |     1.08e-04 |   -358.9357 |     0.000 |
| Slope       |       0.6690 |     4.25e-04 |   1573.2852 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    betaRC
     0   10001  198912 -0.037640
     1   10001  199001 -0.049183
     2   10001  199002 -0.051516
     3   10001  199003 -0.049271
     4   10001  199004 -0.050521
     5   10001  199005 -0.039892
     6   10001  199006 -0.039184
     7   10001  199007 -0.036623
     8   10001  199008 -0.052458
     9   10001  199009 -0.042971
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2382760/2457594 (96.955%)
- Stata standard deviation: 2.03e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412 -0.001367 -0.024906  0.023539
1   10028  202412 -0.252961 -0.200618 -0.052343
2   10032  202412 -0.050648 -0.044258 -0.006391
3   10044  202412  0.042708  0.018604  0.024103
4   10065  202412 -0.083899 -0.104633  0.020734
5   10104  202412 -0.115178 -0.129191  0.014013
6   10107  202412 -0.104849 -0.124065  0.019216
7   10113  202412 -0.120979 -0.132289  0.011311
8   10138  202412 -0.124288 -0.152853  0.028564
9   10145  202412 -0.067405 -0.092242  0.024837
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   58748  199608 -0.287963 -7.679625  7.391662
1   58748  199610 -0.267892 -7.226124  6.958231
2   58748  199612 -0.289788 -7.140743  6.850955
3   58748  199609 -0.325816 -7.164882  6.839066
4   58748  199611 -0.224826 -6.840232  6.615406
5   89741  201701  0.070833  6.116641 -6.045808
6   89741  201702  0.060265  6.075231 -6.014966
7   76472  199711  7.615999  1.775495  5.840504
8   89741  201610  0.070833  5.835716 -5.764883
9   76472  199712  7.596357  1.838067  5.758290
```

---

### betaRR

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 963966 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['betaRR']

**Observations**:
- Stata:  3,421,560
- Python: 2,477,076
- Common: 2,457,594

**Precision1**: 92.290% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.26e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         0.5575 |         0.5843 |         0.0268 |         0.0576 |
| std        |         0.4654 |         0.4562 |         0.2913 |         0.6260 |
| min        |        -7.2013 |        -5.6563 |        -4.4093 |        -9.4752 |
| 25%        |         0.2700 |         0.3010 |        -0.0333 |        -0.0716 |
| 50%        |         0.4708 |         0.5180 |         0.0262 |         0.0562 |
| 75%        |         0.7484 |         0.7799 |         0.1567 |         0.3367 |
| max        |         8.3078 |         9.3451 |         7.5127 |        16.1440 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.1469 + 0.7846 * stata
- **R-squared**: 0.6405
- **N observations**: 2,457,594

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.1469 |     2.72e-04 |    539.5964 |     0.000 |
| Slope       |       0.7846 |     3.75e-04 |   2092.5870 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm   betaRR
     0   10001  198912 0.023374
     1   10001  199001 0.040286
     2   10001  199002 0.037514
     3   10001  199003 0.036667
     4   10001  199004 0.039381
     5   10001  199005 0.023447
     6   10001  199006 0.023286
     7   10001  199007 0.022415
     8   10001  199008 0.053231
     9   10001  199009 0.044351
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2268102/2457594 (92.290%)
- Stata standard deviation: 4.65e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10026  202412  0.475199  0.465418  0.009781
1   10028  202412  0.321687  0.312890  0.008797
2   10032  202412  0.636000  0.622909  0.013091
3   10044  202412  0.741033  0.725779  0.015253
4   10065  202412  0.687285  0.673138  0.014147
5   10104  202412  0.671942  0.658111  0.013831
6   10107  202412  0.592979  0.580773  0.012206
7   10113  202412  0.725095  0.710170  0.014925
8   10138  202412  1.034256  1.012967  0.021289
9   10145  202412  0.699170  0.684779  0.014392
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   58748  199608  2.186324 -5.326391  7.512715
1   58748  199609  2.227492 -5.109660  7.337151
2   58748  199610  2.114096 -5.179592  7.293688
3   58748  199612  1.979756 -5.240927  7.220682
4   58748  199611  1.865837 -5.151053  7.016890
5   82162  200607  7.799125  2.406791  5.392334
6   13030  201705 -1.917474 -7.201326  5.283852
7   82162  200608  7.582370  2.505906  5.076464
8   13030  201706 -2.018299 -7.075431  5.057133
9   13030  201703 -1.984233 -7.027189  5.042956
```

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
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,703,309
- Common: 2,252,622

**Precision1**: 11.982% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.81e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.37e-04 |         0.0061 |         0.0058 |         0.0081 |
| std        |         0.7177 |         0.8125 |         0.6324 |         0.8812 |
| min        |      -306.2332 |      -278.1893 |      -161.2249 |      -224.6477 |
| 25%        |        -0.0228 |        -0.0169 |      -2.74e-10 |      -3.82e-10 |
| 50%        |         0.0110 |         0.0132 |       6.38e-12 |       8.89e-12 |
| 75%        |         0.0389 |         0.0423 |       3.47e-10 |       4.83e-10 |
| max        |       250.7536 |       250.7536 |       307.0868 |       427.8889 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0059 + 0.7525 * stata
- **R-squared**: 0.4419
- **N observations**: 2,252,622

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0059 |     4.04e-04 |     14.5732 |     0.000 |
| Slope       |       0.7525 |     5.64e-04 |   1335.4072 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 269905/2252622 (11.982%)
- Stata standard deviation: 7.18e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   15268  202412 -0.611130 -1.136608  0.525478
1   17330  202412 -0.271085 -0.231680 -0.039405
2   18302  202412 -0.031779  0.599014 -0.630793
3   18464  202412  0.236709 -0.015777  0.252486
4   19487  202412 -0.321679 -0.423716  0.102037
5   20801  202412 -0.375193  1.748981 -2.124173
6   22894  202412 -0.030379 -0.019062 -0.011316
7   23193  202412 -0.098279 -4.034034  3.935756
8   80276  202412  0.000368  0.304700 -0.304332
9   81861  202412  0.054212  0.245272 -0.191060
```

**Largest Differences**:
```
   permno  yyyymm      python       stata        diff
0   19314  202311    0.853598 -306.233250  307.086848
1   63079  198711   -0.132030 -169.426270  169.294240
2   50518  197409 -161.705505   -0.480574 -161.224932
3   28310  197505  109.189842  -16.858906  126.048748
4   50518  197507 -122.357903   -0.110357 -122.247545
5   50518  197509 -122.357903   -0.110357 -122.247545
6   28310  197503  105.488495  -16.287418  121.775913
7   28310  197504  105.488495  -16.287418  121.775913
8   28310  197605  125.327965    6.254519  119.073446
9   28310  197703  109.315552   -9.288592  118.604144
```

---

### currat

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['currat']

**Observations**:
- Stata:  3,065,278
- Python: 3,069,214
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         3.3803 |         3.3803 |      -1.95e-06 |      -3.44e-08 |
| std        |        56.6989 |        56.6989 |       9.85e-04 |       1.74e-05 |
| min        |         0.0000 |         0.0000 |        -0.4978 |        -0.0088 |
| 25%        |         1.2859 |         1.2859 |      -5.02e-08 |      -8.85e-10 |
| 50%        |         2.0125 |         2.0125 |         0.0000 |         0.0000 |
| 75%        |         3.1813 |         3.1813 |       5.05e-08 |       8.91e-10 |
| max        |     25204.0000 |     25204.0000 |       1.67e-04 |       2.94e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.95e-06 |     5.64e-07 |     -3.4584 |     0.001 |
| Slope       |       1.0000 |     9.92e-09 |    1.01e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3065278 (0.000%)
- Stata standard deviation: 5.67e+01

---

### depr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['depr']

**Observations**:
- Stata:  3,462,713
- Python: 3,523,904
- Common: 3,462,713

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.68e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -5.48e-06 |      -6.13e-07 |
| std        |         8.9356 |         8.9356 |         0.0028 |       3.14e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.1795 |         0.0201 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.45e-06 |     1.51e-06 |     -3.6120 |     0.000 |
| Slope       |       1.0000 |     1.69e-07 |    5.93e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/3462713 (0.001%)
- Stata standard deviation: 8.94e+00

---

### fgr5yrNoLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 2116 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['fgr5yrNoLag']

**Observations**:
- Stata:  996,237
- Python: 996,104
- Common: 994,121

**Precision1**: 0.075% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.43e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    994121.0000 |    994121.0000 |    994121.0000 |    994121.0000 |
| mean       |        16.8659 |        16.8658 |      -3.91e-05 |      -2.79e-06 |
| std        |        14.0128 |        14.0129 |         0.3335 |         0.0238 |
| min        |      -899.2000 |      -899.2000 |       -62.1000 |        -4.4317 |
| 25%        |        10.5000 |        10.5000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        20.0000 |        20.0000 |         0.0000 |         0.0000 |
| max        |      2097.8000 |      2097.8000 |        90.3000 |         6.4441 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0046 + 0.9997 * stata
- **R-squared**: 0.9994
- **N observations**: 994,121

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0046 |     5.23e-04 |      8.7028 |     0.000 |
| Slope       |       0.9997 |     2.39e-05 |  41888.2260 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  fgr5yrNoLag
     0   11406  199204         20.0
     1   11406  199205         15.0
     2   11406  199206         15.0
     3   11406  199207         15.0
     4   11406  199208         15.0
     5   11406  199209         15.0
     6   11406  199210         15.0
     7   11406  199211         15.0
     8   11406  199212         15.0
     9   11406  199301         15.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 750/994121 (0.075%)
- Stata standard deviation: 1.40e+01

---

### nanalyst

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['nanalyst']

**Observations**:
- Stata:  2,700,302
- Python: 4,047,630
- Common: 2,700,302

**Precision1**: 0.259% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |         5.1509 |         5.1529 |         0.0022 |       3.29e-04 |
| std        |         6.7163 |         6.7171 |         0.5838 |         0.0869 |
| min        |         0.0000 |         0.0000 |       -29.0000 |        -4.3178 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| max        |        62.0000 |        62.0000 |        35.0000 |         5.2112 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0212 + 0.9963 * stata
- **R-squared**: 0.9925
- **N observations**: 2,699,586

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0212 |     4.47e-04 |     47.3288 |     0.000 |
| Slope       |       0.9963 |     5.29e-05 |  18848.5715 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 6994/2700302 (0.259%)
- Stata standard deviation: 6.72e+00

---

### pchcurrat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ❌ FAILED

**Columns**: ['pchcurrat']

**Observations**:
- Stata:  3,624,363
- Python: 3,625,095
- Common: 3,624,363

**Precision1**: 1.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = inf (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.59e+06 |       3.59e+06 |       3.59e+06 |
| mean       |         0.1878 |            inf |            inf |            inf |
| std        |        20.4050 |            N/A |            N/A |            N/A |
| min        |        -1.0000 |        -1.0000 |        -0.1094 |        -0.0054 |
| 25%        |        -0.1194 |        -0.1217 |      -2.16e-08 |      -1.06e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0786 |         0.0814 |       2.16e-08 |       1.06e-09 |
| max        |      8289.6123 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = inf + -inf * stata
- **R-squared**: nan
- **N observations**: 3,588,349

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |          nan |          nan |         nan |       nan |
| Slope       |          nan |          nan |         nan |       nan |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 37772/3624363 (1.042%)
- Stata standard deviation: 2.04e+01

**Most Recent Bad Observations**:
```
   permno  yyyymm  python  stata  diff
0   15735  202605     NaN    0.0   NaN
1   62391  202605     NaN    0.0   NaN
2   62922  202605     NaN    0.0   NaN
3   75069  202605     NaN    0.0   NaN
4   77895  202605     NaN    0.0   NaN
5   15735  202604     NaN    0.0   NaN
6   62391  202604     NaN    0.0   NaN
7   62922  202604     NaN    0.0   NaN
8   75069  202604     NaN    0.0   NaN
9   77895  202604     NaN    0.0   NaN
```

**Largest Differences**:
```
   permno  yyyymm  python  stata  diff
0   10055  198910     NaN    0.0   NaN
1   10055  198911     NaN    0.0   NaN
2   10055  198912     NaN    0.0   NaN
3   10055  199001     NaN    0.0   NaN
4   10055  199002     NaN    0.0   NaN
5   10055  199003     NaN    0.0   NaN
6   10055  199004     NaN    0.0   NaN
7   10055  199005     NaN    0.0   NaN
8   10055  199006     NaN    0.0   NaN
9   10055  199007     NaN    0.0   NaN
```

---

### pchdepr

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchdepr']

**Observations**:
- Stata:  3,050,498
- Python: 3,268,732
- Common: 3,050,498

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.31e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         0.4972 |         0.4971 |      -9.31e-05 |      -2.41e-06 |
| std        |        38.5912 |        38.5913 |         0.0375 |       9.72e-04 |
| min        |       -75.5903 |       -75.5903 |       -18.3420 |        -0.4753 |
| 25%        |        -0.0906 |        -0.0906 |      -2.22e-09 |      -5.74e-11 |
| 50%        |         0.0251 |         0.0251 |         0.0000 |         0.0000 |
| 75%        |         0.1646 |         0.1646 |       2.22e-09 |       5.76e-11 |
| max        |     15513.7030 |     15513.7034 |         1.3903 |         0.0360 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,050,486

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.26e-05 |     2.15e-05 |     -4.3116 |     0.000 |
| Slope       |       1.0000 |     5.57e-07 |    1.80e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3050498 (0.002%)
- Stata standard deviation: 3.86e+01

---

### pchgm_pchsale

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchgm_pchsale']

**Observations**:
- Stata:  3,222,544
- Python: 3,279,256
- Common: 3,222,544

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.59e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.7243 |        -0.7243 |       9.70e-06 |       1.23e-07 |
| std        |        78.7275 |        78.7275 |         0.0038 |       4.82e-05 |
| min        |    -27624.8850 |    -27624.8841 |        -0.4564 |        -0.0058 |
| 25%        |        -0.0812 |        -0.0812 |      -1.27e-09 |      -1.62e-11 |
| 50%        |        -0.0029 |        -0.0029 |         0.0000 |         0.0000 |
| 75%        |         0.0636 |         0.0636 |       1.29e-09 |       1.63e-11 |
| max        |      5139.5205 |      5139.5206 |         1.4141 |         0.0180 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.69e-06 |     2.12e-06 |      4.5821 |     0.000 |
| Slope       |       1.0000 |     2.69e-08 |    3.72e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3222544 (0.001%)
- Stata standard deviation: 7.87e+01

---

### pchquick

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchquick']

**Observations**:
- Stata:  3,339,639
- Python: 3,655,797
- Common: 3,339,639

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.96e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.34e+06 |       3.34e+06 |       3.34e+06 |       3.34e+06 |
| mean       |         0.2975 |         0.2975 |      -2.53e-07 |      -5.89e-09 |
| std        |        42.9356 |        42.9356 |       2.60e-04 |       6.05e-06 |
| min        |      -111.5194 |      -111.5194 |        -0.1096 |        -0.0026 |
| 25%        |        -0.1626 |        -0.1626 |      -2.27e-09 |      -5.28e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.1243 |         0.1243 |       2.28e-09 |       5.31e-11 |
| max        |     19726.1780 |     19726.1780 |         0.0773 |         0.0018 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,339,639

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.54e-07 |     1.42e-07 |     -1.7849 |     0.074 |
| Slope       |       1.0000 |     3.31e-09 |    3.02e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3339639 (0.000%)
- Stata standard deviation: 4.29e+01

---

### pchsaleinv

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchsaleinv']

**Observations**:
- Stata:  2,465,425
- Python: 3,303,855
- Common: 2,465,425

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.66e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.47e+06 |       2.47e+06 |       2.47e+06 |       2.47e+06 |
| mean       |         0.7658 |         0.7658 |       9.89e-08 |       1.35e-09 |
| std        |        73.4020 |        73.4020 |       4.81e-05 |       6.55e-07 |
| min        |     -3126.2041 |     -3126.2041 |      -6.97e-04 |      -9.50e-06 |
| 25%        |        -0.1224 |        -0.1224 |      -2.63e-09 |      -3.59e-11 |
| 50%        |         0.0114 |         0.0114 |       1.70e-12 |       2.31e-14 |
| 75%        |         0.1759 |         0.1759 |       2.67e-09 |       3.63e-11 |
| max        |     28764.0310 |     28764.0303 |         0.0218 |       2.97e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,465,425

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.17e-07 |     3.06e-08 |      3.8251 |     0.000 |
| Slope       |       1.0000 |     4.17e-10 |    2.40e+09 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2465425 (0.000%)
- Stata standard deviation: 7.34e+01

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

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['rd_sale_q']

**Observations**:
- Stata:  566,115
- Python: 1,051,434
- Common: 566,115

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    566115.0000 |    566115.0000 |    566115.0000 |    566115.0000 |
| mean       |         7.6746 |         7.6747 |       1.34e-04 |       7.34e-07 |
| std        |       183.2067 |       183.2067 |         0.1055 |       5.76e-04 |
| min        |     -3937.0000 |     -3937.0000 |       -29.0278 |        -0.1584 |
| 25%        |         0.0468 |         0.0468 |      -2.04e-09 |      -1.11e-11 |
| 50%        |         0.1117 |         0.1117 |      -2.22e-16 |      -1.21e-18 |
| 75%        |         0.2509 |         0.2509 |       1.93e-09 |       1.05e-11 |
| max        |     31684.3340 |     31684.3333 |        52.2216 |         0.2850 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 566,115

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.34e-04 |     1.40e-04 |      0.9547 |     0.340 |
| Slope       |       1.0000 |     7.65e-07 |    1.31e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 3/566115 (0.001%)
- Stata standard deviation: 1.83e+02

---

### roavol

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['roavol']

**Observations**:
- Stata:  2,039,901
- Python: 2,159,781
- Common: 2,039,901

**Precision1**: 2.934% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.44e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.04e+06 |       2.04e+06 |       2.04e+06 |       2.04e+06 |
| mean       |         0.0305 |         0.0313 |       8.61e-04 |         0.0056 |
| std        |         0.1527 |         0.1740 |         0.0827 |         0.5419 |
| min        |       3.49e-05 |       3.49e-05 |        -0.4214 |        -2.7599 |
| 25%        |         0.0056 |         0.0056 |      -2.12e-10 |      -1.39e-09 |
| 50%        |         0.0124 |         0.0125 |      -8.09e-12 |      -5.30e-11 |
| 75%        |         0.0295 |         0.0296 |       1.24e-10 |       8.14e-10 |
| max        |        49.8304 |        49.8304 |        24.9505 |       163.4275 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0027 * stata
- **R-squared**: 0.7739
- **N observations**: 2,039,784

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.80e-04 |     5.91e-05 |     13.1978 |     0.000 |
| Slope       |       1.0027 |     3.80e-04 |   2642.1174 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 59848/2039901 (2.934%)
- Stata standard deviation: 1.53e-01

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
- Python: 3,232,394
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
- Test 2 - Superset check: ❌ FAILED (Python missing 45 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,457,695
- Common: 2,457,656

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.03e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         1.0672 |         1.0670 |      -1.23e-04 |      -4.30e-07 |
| std        |       286.5304 |       286.5304 |         0.1413 |       4.93e-04 |
| min        |     -3092.0000 |     -3092.0000 |      -146.0200 |        -0.5096 |
| 25%        |        -0.0374 |        -0.0374 |      -2.58e-09 |      -8.99e-12 |
| 50%        |         0.0794 |         0.0794 |         0.0000 |         0.0000 |
| 75%        |         0.2229 |         0.2229 |       2.55e-09 |       8.91e-12 |
| max        |    251440.0000 |    251440.0000 |        15.0962 |         0.0527 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,457,656

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.23e-04 |     9.02e-05 |     -1.3635 |     0.173 |
| Slope       |       1.0000 |     3.15e-07 |    3.18e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm    sgr_q
     0   11545  199706 0.241882
     1   11545  199707 0.241882
     2   11545  199708 0.241882
     3   11545  199806 1.767560
     4   11545  199807 1.767560
     5   11545  199808 1.767560
     6   12837  198004 0.209407
     7   12837  198005 0.209407
     8   21346  197001 0.152858
     9   21346  197002 0.152858
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/2457656 (0.001%)
- Stata standard deviation: 2.87e+02

---

### tang_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['tang_q']

**Observations**:
- Stata:  1,675,098
- Python: 2,823,459
- Common: 1,675,098

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.54e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6576 |         0.0010 |         0.0030 |
| std        |         0.3446 |         0.7647 |         0.6824 |         1.9803 |
| min        |        -0.4077 |        -0.4077 |        -0.9878 |        -2.8666 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.80e-11 |       8.13e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       738.0701 |       737.1991 |      2139.2976 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 1.0013 * stata
- **R-squared**: 0.2036
- **N observations**: 1,675,098

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.84e-04 |       0.0011 |      0.1625 |     0.871 |
| Slope       |       1.0013 |       0.0015 |    654.4138 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 168/1675098 (0.010%)
- Stata standard deviation: 3.45e-01

---

### AbnormalAccrualsPercent

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/AbnormalAccrualsPercent.csv

---

### FRbook

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/FRbook.csv

---

### IntrinsicValue

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/IntrinsicValue.csv

---

### OrgCapNoAdj

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/OrgCapNoAdj.csv

---

### ResidualMomentum6m

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/ResidualMomentum6m.csv

---

### grcapx1y

**Status**: ❌ MISSING PYTHON CSV

**Error**: Python CSV file not found: ../pyData/Placebos/grcapx1y.csv

---

