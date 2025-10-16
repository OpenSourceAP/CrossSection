# Placebo Validation Results

**Generated**: 2025-10-16 18:30:14

**Configuration**:
- TOL_SUPERSET: 0.1%
- TOL_DIFF_1: 0.01
- TOL_OBS_1: 10%
- EXTREME_Q: 0.99
- TOL_DIFF_2: 1.0
- INDEX_COLS: ['permno', 'yyyymm']

## Summary

| Placebo                   | Superset  | Precision1   | R-squared | Precision2              |
|---------------------------|-----------|--------------|-----------|-------------------------|
| ETR                       | ✅ (0.00%)   | ✅ (0.03%)    | 0.6701    | ✅ (99th diff 1.2E-11)   |
| EarningsPredictability    | ✅ (0.00%)   | ✅ (0.01%)    | 0.7744    | ✅ (99th diff 2.5E-16)   |
| pchsaleinv                | ✅ (0.00%)   | ✅ (0.00%)    | 0.9197    | ✅ (99th diff 1.7E-09)   |
| nanalyst                  | ✅ (0.00%)   | ✅ (1.25%)    | 0.9734    | ✅ (99th diff 3.0E-01)   |
| roic                      | ✅ (0.00%)   | ✅ (0.01%)    | 0.9735    | ✅ (99th diff 3.6E-23)   |
| cfpq                      | ✅ (0.00%)   | ✅ (0.43%)    | 0.9739    | ✅ (99th diff 1.0E-07)   |
| ReturnSkewQF              | ❌ (0.77%)   | ✅ (0.89%)    | 0.9799    | ✅ (99th diff 3.2E-07)   |
| BetaBDLeverage            | ✅ (0.00%)   | ✅ (2.21%)    | 0.9843    | ✅ (99th diff 2.3E-01)   |
| RetNOA_q                  | ✅ (0.00%)   | ✅ (0.00%)    | 0.9913    | ✅ (99th diff 4.3E-11)   |
| AccrualQuality            | ✅ (0.01%)   | ❌ (10.68%)   | 0.9943    | ✅ (99th diff 1.2E-01)   |
| ReturnSkewCAPM            | ❌ (0.75%)   | ✅ (0.81%)    | 0.9945    | ✅ (99th diff 9.0E-03)   |
| DownsideBeta              | ✅ (0.00%)   | ❌ (19.35%)   | 0.9946    | ✅ (99th diff 1.7E-01)   |
| AccrualQualityJune        | ✅ (0.01%)   | ❌ (10.49%)   | 0.9947    | ✅ (99th diff 1.2E-01)   |
| DelayAcct                 | ❌ (0.90%)   | ❌ (66.04%)   | 0.9949    | ✅ (99th diff 2.7E-01)   |
| BrandCapital              | ✅ (0.00%)   | ✅ (5.88%)    | 0.9955    | ✅ (99th diff 8.2E-02)   |
| IntrinsicValue            | ❌ (0.71%)   | ✅ (2.12%)    | 0.9972    | ✅ (99th diff 6.3E-02)   |
| DivYieldAnn               | ✅ (0.00%)   | ✅ (0.05%)    | 0.9976    | ✅ (99th diff 2.1E-08)   |
| DivYield                  | ✅ (0.00%)   | ✅ (0.01%)    | 0.9978    | ✅ (99th diff 1.2E-08)   |
| PM_q                      | ✅ (0.00%)   | ✅ (0.00%)    | 0.9985    | ✅ (99th diff 3.0E-09)   |
| AbnormalAccrualsPercent   | ❌ (1.39%)   | ✅ (1.13%)    | 0.9986    | ✅ (99th diff 1.1E-02)   |
| DelayNonAcct              | ❌ (0.90%)   | ❌ (43.60%)   | 0.9989    | ✅ (99th diff 1.3E-01)   |
| ForecastDispersionLT      | ❌ (0.92%)   | ✅ (0.08%)    | 0.9989    | ✅ (99th diff 1.5E-07)   |
| OperProfLag_q             | ✅ (0.00%)   | ✅ (0.01%)    | 0.9991    | ✅ (99th diff 1.8E-08)   |
| tang_q                    | ✅ (0.00%)   | ✅ (0.01%)    | 0.9994    | ✅ (99th diff 1.6E-07)   |
| OperProfRDLagAT_q         | ✅ (0.01%)   | ✅ (0.05%)    | 0.9994    | ✅ (99th diff 6.8E-08)   |
| CBOperProfLagAT_q         | ✅ (0.00%)   | ✅ (0.05%)    | 0.9996    | ✅ (99th diff 8.8E-08)   |
| securedind                | ✅ (0.00%)   | ✅ (0.01%)    | 0.9997    | ✅ (99th diff 0.0E+00)   |
| PS_q                      | ✅ (0.00%)   | ✅ (0.04%)    | 0.9998    | ✅ (99th diff 0.0E+00)   |
| OperProfRDLagAT           | ✅ (0.00%)   | ✅ (1.12%)    | 0.9998    | ✅ (99th diff 1.2E-02)   |
| RD_q                      | ✅ (0.00%)   | ✅ (0.02%)    | 0.9998    | ✅ (99th diff 6.8E-08)   |
| OPLeverage_q              | ✅ (0.00%)   | ✅ (0.03%)    | 0.9998    | ✅ (99th diff 8.1E-08)   |
| fgr5yrNoLag               | ❌ (0.49%)   | ✅ (0.08%)    | 0.9999    | ✅ (99th diff 1.4E-07)   |
| roavol                    | ✅ (0.00%)   | ✅ (0.04%)    | 0.9999    | ✅ (99th diff 3.6E-08)   |
| ChangeRoA                 | ✅ (0.00%)   | ✅ (0.02%)    | 0.9999    | ✅ (99th diff 6.7E-08)   |
| GrSaleToGrReceivables     | ✅ (0.00%)   | ✅ (0.01%)    | 0.9999    | ✅ (99th diff 8.3E-10)   |
| GPlag_q                   | ✅ (0.00%)   | ✅ (0.04%)    | 0.9999    | ✅ (99th diff 1.8E-08)   |
| RetNOA                    | ✅ (0.00%)   | ✅ (0.00%)    | 0.9999    | ✅ (99th diff 1.5E-19)   |
| EBM_q                     | ✅ (0.00%)   | ✅ (0.00%)    | 0.9999    | ✅ (99th diff 4.9E-08)   |
| NetPayoutYield_q          | ✅ (0.00%)   | ✅ (0.04%)    | 0.9999    | ✅ (99th diff 4.9E-08)   |
| CFq                       | ✅ (0.00%)   | ✅ (0.02%)    | 1.0000    | ✅ (99th diff 2.1E-08)   |
| secured                   | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 8.4E-08)   |
| GPlag                     | ✅ (0.00%)   | ✅ (0.02%)    | 1.0000    | ✅ (99th diff 5.7E-08)   |
| Tax_q                     | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 8.6E-09)   |
| BetaDimson                | ✅ (0.00%)   | ✅ (2.94%)    | 1.0000    | ✅ (99th diff 1.9E-02)   |
| AssetLiquidityMarketQuart | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.5E-07)   |
| CapTurnover_q             | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.0E-08)   |
| EarningsPersistence       | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 2.1E-07)   |
| DelSTI                    | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 2.0E-07)   |
| SP_q                      | ✅ (0.00%)   | ✅ (0.02%)    | 1.0000    | ✅ (99th diff 1.1E-07)   |
| betaRC                    | ✅ (0.00%)   | ✅ (2.45%)    | 1.0000    | ✅ (99th diff 1.6E-02)   |
| AssetGrowth_q             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.9E-08)   |
| betaCC                    | ✅ (0.00%)   | ✅ (1.85%)    | 1.0000    | ✅ (99th diff 1.5E-02)   |
| EntMult_q                 | ✅ (0.01%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 6.4E-09)   |
| EPq                       | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 6.2E-08)   |
| ChangeRoE                 | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.3E-09)   |
| OrgCapNoAdj               | ❌ (2.05%)   | ✅ (0.02%)    | 1.0000    | ✅ (99th diff 3.0E-05)   |
| BMq                       | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.3E-07)   |
| PayoutYield_q             | ✅ (0.00%)   | ✅ (0.06%)    | 1.0000    | ✅ (99th diff 4.4E-08)   |
| ResidualMomentum6m        | ✅ (0.00%)   | ✅ (0.93%)    | 1.0000    | ✅ (99th diff 9.6E-03)   |
| salerec                   | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 2.1E-08)   |
| AssetLiquidityBookQuart   | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.4E-08)   |
| grcapx1y                  | ❌ (1.09%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.8E-09)   |
| betaNet                   | ✅ (0.00%)   | ✅ (0.72%)    | 1.0000    | ✅ (99th diff 8.4E-03)   |
| saleinv                   | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.1E-09)   |
| ChNCOA                    | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 8.5E-08)   |
| betaRR                    | ✅ (0.00%)   | ✅ (0.47%)    | 1.0000    | ✅ (99th diff 7.3E-03)   |
| GrGMToGrSales             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.3E-09)   |
| ChNCOL                    | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 5.8E-08)   |
| betaCR                    | ✅ (0.00%)   | ✅ (0.15%)    | 1.0000    | ✅ (99th diff 5.6E-03)   |
| pchdepr                   | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.3E-09)   |
| AssetLiquidityBook        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 8.5E-08)   |
| EarningsSmoothness        | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 3.1E-07)   |
| EarningsConservatism      | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.4E-07)   |
| CBOperProfLagAT           | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 6.6E-08)   |
| AssetLiquidityMarket      | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 1.7E-07)   |
| sgr_q                     | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.1E-10)   |
| LaborforceEfficiency      | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.3E-09)   |
| rd_sale_q                 | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 6.7E-09)   |
| pchgm_pchsale             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.8E-09)   |
| BookLeverageQuarterly     | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.1E-13)   |
| EarningsValueRelevance    | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.4E-07)   |
| depr                      | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 8.8E-09)   |
| KZ_q                      | ✅ (0.01%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.4E-09)   |
| NetDebtPrice_q            | ✅ (0.01%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 6.4E-08)   |
| ZScore_q                  | ✅ (0.00%)   | ✅ (0.01%)    | 1.0000    | ✅ (99th diff 5.0E-08)   |
| AssetTurnover             | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.0E-09)   |
| IdioVolCAPM               | ❌ (0.77%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.0E-03)   |
| WW_Q                      | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.5E-06)   |
| AssetTurnover_q           | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.7E-09)   |
| OperProfLag               | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.5E-08)   |
| sgr                       | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.9E-09)   |
| AMq                       | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.1E-08)   |
| CapTurnover               | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 8.5E-08)   |
| EarningsTimeliness        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.8E-07)   |
| Leverage_q                | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.7E-08)   |
| WW                        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.2E-10)   |
| BetaSquared               | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.2E-04)   |
| ChPM                      | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.3E-09)   |
| ZScore                    | ✅ (0.08%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.6E-08)   |
| salecash                  | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 6.6E-09)   |
| PM                        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.4E-09)   |
| cashdebt                  | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.2E-09)   |
| currat                    | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.4E-08)   |
| quick                     | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.1E-08)   |
| KZ                        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.1E-09)   |
| pchcurrat                 | ❌ (0.99%)   | ✅ (0.05%)    | 1.0000    | ✅ (99th diff 9.7E-09)   |
| FailureProbabilityJune    | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 5.2E-09)   |
| FailureProbability        | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.7E-09)   |
| pchquick                  | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.0E-09)   |
| rd_sale                   | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 4.1E-09)   |
| FRbook                    | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 2.1E-07)   |
| BidAskTAQ                 | ✅ (0.00%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 1.6E-07)   |
| IdioVolQF                 | ❌ (0.77%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 3.4E-08)   |
| OScore_q                  | ❌ (0.66%)   | ✅ (0.00%)    | 1.0000    | ✅ (99th diff 0.0E+00)   |

**Overall**: 97/114 available placebos passed validation
**Python CSVs**: 114/114 placebos have Python implementation

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
- Python: 2,671,099
- Common: 2,584,377

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.15e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.58e+06 |       2.58e+06 |       2.58e+06 |       2.58e+06 |
| mean       |         3.7379 |         3.7379 |       3.16e-06 |       1.36e-07 |
| std        |        23.2695 |        23.2695 |         0.0035 |       1.50e-04 |
| min        |       -33.6391 |       -33.6391 |        -0.6348 |        -0.0273 |
| 25%        |         0.6615 |         0.6615 |      -3.34e-08 |      -1.44e-09 |
| 50%        |         1.4017 |         1.4017 |         0.0000 |         0.0000 |
| 75%        |         3.2088 |         3.2088 |       3.35e-08 |       1.44e-09 |
| max        |     11549.4230 |     11549.4231 |         3.4533 |         0.1484 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,584,377

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.19e-06 |     2.19e-06 |      1.4540 |     0.146 |
| Slope       |       1.0000 |     9.30e-08 |    1.08e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 23/2584377 (0.001%)
- Stata standard deviation: 2.33e+01

---

### AbnormalAccrualsPercent

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 35302 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AbnormalAccrualsPercent']

**Observations**:
- Stata:  2,535,621
- Python: 2,629,976
- Common: 2,500,319

**Precision1**: 1.131% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.13e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         1.0534 |         1.0446 |        -0.0087 |      -1.06e-04 |
| std        |        82.5140 |        82.3362 |         3.0917 |         0.0375 |
| min        |     -5995.7578 |     -5995.7576 |      -879.1455 |       -10.6545 |
| 25%        |        -0.4816 |        -0.4808 |      -4.53e-07 |      -5.49e-09 |
| 50%        |         0.0802 |         0.0808 |      -4.27e-09 |      -5.17e-11 |
| 75%        |         0.7854 |         0.7847 |       1.34e-07 |       1.63e-09 |
| max        |     22304.4650 |     22304.4471 |       369.1171 |         4.4734 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0057 + 0.9971 * stata
- **R-squared**: 0.9986
- **N observations**: 2,500,319

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0057 |       0.0019 |     -2.9392 |     0.003 |
| Slope       |       0.9971 |     2.36e-05 |  42203.8502 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  AbnormalAccrualsPercent
     0   10006  197206                 1.094513
     1   10006  197207                 1.094513
     2   10006  197208                 1.094513
     3   10006  197209                 1.094513
     4   10006  197210                 1.094513
     5   10006  197211                 1.094513
     6   10006  197212                 1.094513
     7   10006  197301                 1.094513
     8   10006  197302                 1.094513
     9   10006  197303                 1.094513
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 28285/2500319 (1.131%)
- Stata standard deviation: 8.25e+01

---

### AccrualQuality

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AccrualQuality']

**Observations**:
- Stata:  1,740,065
- Python: 1,740,989
- Common: 1,739,921

**Precision1**: 10.677% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.21e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.74e+06 |       1.74e+06 |       1.74e+06 |       1.74e+06 |
| mean       |         0.0460 |         0.0460 |       4.54e-06 |       9.17e-05 |
| std        |         0.0495 |         0.0495 |         0.0037 |         0.0758 |
| min        |       4.17e-04 |       4.17e-04 |        -0.3495 |        -7.0598 |
| 25%        |         0.0179 |         0.0179 |      -2.74e-09 |      -5.54e-08 |
| 50%        |         0.0316 |         0.0316 |       3.68e-12 |       7.43e-11 |
| 75%        |         0.0563 |         0.0563 |       2.70e-09 |       5.45e-08 |
| max        |         1.6265 |         1.6264 |         0.4169 |         8.4227 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9966 * stata
- **R-squared**: 0.9943
- **N observations**: 1,739,921

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.63e-04 |     3.88e-06 |     42.0804 |     0.000 |
| Slope       |       0.9966 |     5.74e-05 |  17371.1717 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 185763/1739921 (10.677%)
- Stata standard deviation: 4.95e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.017073  0.018274 -0.001202
1   10104  202609  0.017073  0.018274 -0.001202
2   18136  202609  0.032174  0.032920 -0.000746
3   21742  202609  0.031449  0.033581 -0.002131
4   42585  202609  0.021529  0.041185 -0.019655
5   60097  202609  0.021091  0.019858  0.001233
6   10104  202608  0.017073  0.018274 -0.001202
7   12082  202608  0.086911  0.085591  0.001320
8   12783  202608  0.029369  0.031918 -0.002550
9   13142  202608  0.017982  0.017444  0.000538
```

**Largest Differences**:
```
   permno  yyyymm   python     stata      diff
0   85705  200609  0.45688  0.039956  0.416924
1   85705  200610  0.45688  0.039956  0.416924
2   85705  200611  0.45688  0.039956  0.416924
3   85705  200612  0.45688  0.039956  0.416924
4   85705  200701  0.45688  0.039956  0.416924
5   85705  200702  0.45688  0.039956  0.416924
6   85705  200703  0.45688  0.039956  0.416924
7   85705  200704  0.45688  0.039956  0.416924
8   85705  200705  0.45688  0.039956  0.416924
9   85705  200706  0.45688  0.039956  0.416924
```

---

### AccrualQualityJune

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AccrualQualityJune']

**Observations**:
- Stata:  1,784,388
- Python: 1,785,269
- Common: 1,784,228

**Precision1**: 10.490% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.18e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.78e+06 |       1.78e+06 |       1.78e+06 |       1.78e+06 |
| mean       |         0.0465 |         0.0465 |       1.75e-06 |       3.46e-05 |
| std        |         0.0506 |         0.0506 |         0.0037 |         0.0729 |
| min        |       4.17e-04 |       4.17e-04 |        -0.3495 |        -6.8997 |
| 25%        |         0.0179 |         0.0179 |      -2.78e-09 |      -5.49e-08 |
| 50%        |         0.0318 |         0.0318 |       1.41e-13 |       2.79e-12 |
| 75%        |         0.0569 |         0.0569 |       2.70e-09 |       5.32e-08 |
| max        |         1.6265 |         1.6264 |         0.4169 |         8.2317 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0002 + 0.9967 * stata
- **R-squared**: 0.9947
- **N observations**: 1,784,228

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.55e-04 |     3.75e-06 |     41.3539 |     0.000 |
| Slope       |       0.9967 |     5.45e-05 |  18274.3742 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 187160/1784228 (10.490%)
- Stata standard deviation: 5.06e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10104  202610  0.017073  0.018274 -0.001202
1   10104  202609  0.017073  0.018274 -0.001202
2   18136  202609  0.032174  0.032920 -0.000746
3   21742  202609  0.031449  0.033581 -0.002131
4   42585  202609  0.021529  0.041185 -0.019655
5   60097  202609  0.021091  0.019858  0.001233
6   10104  202608  0.017073  0.018274 -0.001202
7   12082  202608  0.086911  0.085591  0.001320
8   12783  202608  0.029369  0.031918 -0.002550
9   13142  202608  0.017982  0.017444  0.000538
```

**Largest Differences**:
```
   permno  yyyymm   python     stata      diff
0   85705  200706  0.45688  0.039956  0.416924
1   85705  200707  0.45688  0.039956  0.416924
2   85705  200708  0.45688  0.039956  0.416924
3   85705  200709  0.45688  0.039956  0.416924
4   85705  200710  0.45688  0.039956  0.416924
5   85705  200711  0.45688  0.039956  0.416924
6   85705  200712  0.45688  0.039956  0.416924
7   85705  200801  0.45688  0.039956  0.416924
8   85705  200802  0.45688  0.039956  0.416924
9   85705  200803  0.45688  0.039956  0.416924
```

---

### AssetGrowth_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetGrowth_q']

**Observations**:
- Stata:  2,303,961
- Python: 2,303,973
- Common: 2,303,898

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |         0.1633 |         0.1633 |      -1.26e-05 |      -3.58e-06 |
| std        |         3.5114 |         3.5114 |         0.0144 |         0.0041 |
| min        |        -1.0268 |        -1.0268 |       -12.1084 |        -3.4483 |
| 25%        |        -0.0283 |        -0.0283 |      -2.02e-09 |      -5.74e-10 |
| 50%        |         0.0624 |         0.0624 |      -8.11e-13 |      -2.31e-13 |
| 75%        |         0.1821 |         0.1821 |       2.01e-09 |       5.72e-10 |
| max        |      2788.4187 |      2788.4186 |         3.0812 |         0.8775 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,303,898

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.85e-06 |     9.53e-06 |     -1.0337 |     0.301 |
| Slope       |       1.0000 |     2.71e-06 | 368841.8003 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 45/2303898 (0.002%)
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
- Python: 3,600,509
- Common: 3,595,932

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.49e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |         0.5929 |         0.5929 |      -8.44e-07 |      -2.20e-06 |
| std        |         0.3840 |         0.3840 |       3.41e-04 |       8.87e-04 |
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
| Intercept   |    -9.38e-07 |     3.30e-07 |     -2.8411 |     0.004 |
| Slope       |       1.0000 |     4.68e-07 |    2.14e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 158/3595932 (0.004%)
- Stata standard deviation: 3.84e-01

---

### AssetLiquidityBookQuart

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityBookQuart']

**Observations**:
- Stata:  2,538,807
- Python: 2,553,361
- Common: 2,538,755

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.44e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.54e+06 |       2.54e+06 |       2.54e+06 |       2.54e+06 |
| mean       |         0.6036 |         0.6036 |      -1.92e-06 |      -1.43e-06 |
| std        |         1.3441 |         1.3441 |         0.0035 |         0.0026 |
| min        |       -10.8152 |       -10.8152 |        -4.2936 |        -3.1944 |
| 25%        |         0.5155 |         0.5155 |      -1.26e-08 |      -9.35e-09 |
| 50%        |         0.6075 |         0.6075 |         0.0000 |         0.0000 |
| 75%        |         0.7025 |         0.7025 |       1.25e-08 |       9.33e-09 |
| max        |      2003.3081 |      2003.3081 |         3.0063 |         2.2367 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,538,755

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.62e-07 |     2.37e-06 |      0.2789 |     0.780 |
| Slope       |       1.0000 |     1.61e-06 | 620452.6112 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 74/2538755 (0.003%)
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
- Python: 3,478,723
- Common: 3,476,318

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.68e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.48e+06 |       3.48e+06 |       3.48e+06 |       3.48e+06 |
| mean       |         0.4488 |         0.4488 |      -4.60e-07 |      -1.64e-06 |
| std        |         0.2802 |         0.2802 |       2.06e-04 |       7.35e-04 |
| min        |        -7.2979 |        -7.2979 |        -0.0545 |        -0.1943 |
| 25%        |         0.2655 |         0.2655 |      -7.62e-09 |      -2.72e-08 |
| 50%        |         0.4442 |         0.4442 |       1.05e-13 |       3.76e-13 |
| 75%        |         0.5694 |         0.5694 |       7.64e-09 |       2.73e-08 |
| max        |        48.9168 |        48.9168 |         0.0444 |         0.1583 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,476,318

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.89e-07 |     2.09e-07 |     -2.3445 |     0.019 |
| Slope       |       1.0000 |     3.94e-07 |    2.54e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 225/3476318 (0.006%)
- Stata standard deviation: 2.80e-01

---

### AssetLiquidityMarketQuart

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetLiquidityMarketQuart']

**Observations**:
- Stata:  2,503,163
- Python: 2,503,160
- Common: 2,503,106

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.50e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.4482 |         0.4482 |      -1.50e-06 |      -5.40e-06 |
| std        |         0.2781 |         0.2781 |         0.0014 |         0.0050 |
| min        |        -6.3541 |        -6.3541 |        -1.3938 |        -5.0125 |
| 25%        |         0.2725 |         0.2725 |      -7.72e-09 |      -2.78e-08 |
| 50%        |         0.4522 |         0.4522 |       6.19e-12 |       2.23e-11 |
| 75%        |         0.5664 |         0.5664 |       7.73e-09 |       2.78e-08 |
| max        |       137.3564 |       137.3564 |         1.3203 |         4.7483 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,503,106

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.41e-06 |     1.66e-06 |      2.6510 |     0.008 |
| Slope       |       1.0000 |     3.15e-06 | 317358.4604 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 141/2503106 (0.006%)
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
- Python: 2,813,605
- Common: 2,796,921

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.00e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |         5.2784 |         5.2785 |       1.08e-04 |       4.15e-07 |
| std        |       261.1047 |       261.1082 |         0.0761 |       2.92e-04 |
| min        |         0.0000 |        -0.0000 |       -18.4493 |        -0.0707 |
| 25%        |         0.9854 |         0.9854 |      -3.85e-08 |      -1.47e-10 |
| 50%        |         1.8726 |         1.8726 |         0.0000 |         0.0000 |
| 75%        |         3.0805 |         3.0805 |       3.86e-08 |       1.48e-10 |
| max        |    108845.1100 |    108847.6000 |        27.7236 |         0.1062 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,796,921

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.73e-05 |     4.55e-05 |      0.8195 |     0.412 |
| Slope       |       1.0000 |     1.74e-07 |    5.74e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2796921 (0.001%)
- Stata standard deviation: 2.61e+02

---

### AssetTurnover_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['AssetTurnover_q']

**Observations**:
- Stata:  1,963,604
- Python: 2,183,943
- Common: 1,963,555

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.70e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |         1.3789 |         1.3789 |       6.27e-06 |       1.14e-07 |
| std        |        55.1418 |        55.1407 |         0.0116 |       2.11e-04 |
| min        |         0.0000 |        -0.0000 |        -1.4730 |        -0.0267 |
| 25%        |         0.2551 |         0.2550 |      -1.00e-08 |      -1.82e-10 |
| 50%        |         0.5119 |         0.5119 |         0.0000 |         0.0000 |
| 75%        |         0.8749 |         0.8749 |       1.00e-08 |       1.82e-10 |
| max        |     27068.2270 |     27068.2000 |         4.9335 |         0.0895 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,963,555

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.27e-05 |     8.26e-06 |      3.9555 |     0.000 |
| Slope       |       1.0000 |     1.50e-07 |    6.68e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 70/1963555 (0.004%)
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
- Python: 2,631,795
- Common: 2,568,881

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.35e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |        -0.5919 |        -0.5919 |       1.39e-06 |       1.45e-06 |
| std        |         0.9608 |         0.9608 |         0.0029 |         0.0030 |
| min        |       -13.7467 |       -13.7467 |        -0.8206 |        -0.8540 |
| 25%        |        -1.1088 |        -1.1088 |      -2.50e-08 |      -2.61e-08 |
| 50%        |        -0.5062 |        -0.5062 |      -1.46e-11 |      -1.52e-11 |
| 75%        |         0.0109 |         0.0109 |       2.51e-08 |       2.61e-08 |
| max        |         6.6128 |         6.6128 |         2.3152 |         2.4096 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,568,881

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.44e-06 |     2.14e-06 |     -1.6076 |     0.108 |
| Slope       |       1.0000 |     1.90e-06 | 527504.6768 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 79/2568881 (0.003%)
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
| 25%        |        -0.1353 |        -0.1334 |      -5.37e-06 |      -5.50e-06 |
| 50%        |         0.2846 |         0.2856 |       4.28e-05 |       4.38e-05 |
| 75%        |         0.6641 |         0.6649 |       7.60e-05 |       7.78e-05 |
| max        |        25.2977 |        25.2978 |        16.0268 |        16.4126 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0054 + 0.9836 * stata
- **R-squared**: 0.9843
- **N observations**: 2,116,539

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0054 |     8.55e-05 |     63.7188 |     0.000 |
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

**Precision1**: 2.944% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.90e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       5.00e+06 |       5.00e+06 |       5.00e+06 |       5.00e+06 |
| mean       |         0.7973 |         0.7978 |       4.79e-04 |       2.00e-04 |
| std        |         2.3944 |         2.3967 |         0.0133 |         0.0056 |
| min        |      -286.1514 |      -285.0655 |        -3.0642 |        -1.2797 |
| 25%        |        -0.0184 |        -0.0184 |      -4.30e-04 |      -1.79e-04 |
| 50%        |         0.6958 |         0.6962 |       1.02e-08 |       4.25e-09 |
| 75%        |         1.5830 |         1.5838 |         0.0013 |       5.26e-04 |
| max        |       301.7971 |       302.8436 |         1.6407 |         0.6852 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0003 + 1.0009 * stata
- **R-squared**: 1.0000
- **N observations**: 5,002,680

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.63e-04 |     6.19e-06 |    -42.4922 |     0.000 |
| Slope       |       1.0009 |     2.45e-06 | 408024.9645 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 147265/5002680 (2.944%)
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

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.16e-04 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.29e+06 |       4.29e+06 |       4.29e+06 |       4.29e+06 |
| mean       |         1.5351 |         1.5351 |      -4.90e-06 |      -7.36e-07 |
| std        |         6.6568 |         6.6566 |       5.54e-04 |       8.33e-05 |
| min        |       5.10e-13 |       5.13e-13 |        -0.3036 |        -0.0456 |
| 25%        |         0.2920 |         0.2920 |      -2.20e-08 |      -3.31e-09 |
| 50%        |         0.8168 |         0.8168 |       5.22e-10 |       7.84e-11 |
| 75%        |         1.7846 |         1.7846 |       3.14e-08 |       4.71e-09 |
| max        |      2770.3259 |      2770.1126 |         0.1280 |         0.0192 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,285,574

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.16e-05 |     2.56e-07 |    162.4728 |     0.000 |
| Slope       |       1.0000 |     3.75e-08 |    2.67e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40/4285574 (0.001%)
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

**Precision2**: 99th percentile diff = 1.59e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.26e+06 |       3.26e+06 |       3.26e+06 |       3.26e+06 |
| mean       |         1.5559 |         1.5559 |       1.00e-10 |       3.99e-11 |
| std        |         2.5110 |         2.5110 |       8.73e-08 |       3.48e-08 |
| min        |         0.0000 |         0.0000 |      -2.27e-06 |      -9.05e-07 |
| 25%        |         0.1774 |         0.1774 |      -1.00e-08 |      -3.98e-09 |
| 50%        |         0.6136 |         0.6136 |         0.0000 |         0.0000 |
| 75%        |         1.8032 |         1.8032 |       1.00e-08 |       3.98e-09 |
| max        |        39.9582 |        39.9582 |       2.22e-06 |       8.83e-07 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,262,927

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.95e-10 |     5.69e-11 |     -8.7096 |     0.000 |
| Slope       |       1.0000 |     1.93e-11 |    5.19e+10 |     0.000 |

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
- Python: 2,670,968
- Common: 2,572,593

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.13e-13 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |       945.9143 |            inf |            inf |            inf |
| std        |       3.67e+06 |            N/A |            N/A |            N/A |
| min        |      -1.62e+09 |    -34413.0000 |       -96.2367 |      -2.62e-05 |
| 25%        |         1.4348 |         1.4348 |      -6.20e-08 |      -1.69e-14 |
| 50%        |         2.0340 |         2.0341 |      -2.22e-16 |      -6.04e-23 |
| 75%        |         3.3458 |         3.3458 |       6.19e-08 |       1.68e-14 |
| max        |       2.85e+09 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,572,575

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.06e-05 |     7.18e-05 |      0.4259 |     0.670 |
| Slope       |       1.0000 |     3.03e-07 |    3.30e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18/2572593 (0.001%)
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
- Python: 1,280,696
- Common: 1,231,412

**Precision1**: 5.878% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.25e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.23e+06 |       1.23e+06 |       1.23e+06 |       1.23e+06 |
| mean       |         0.0642 |         0.0656 |         0.0014 |         0.0040 |
| std        |         0.3504 |         0.3545 |         0.0239 |         0.0683 |
| min        |        -0.0066 |        -0.0066 |        -0.0211 |        -0.0603 |
| 25%        |         0.0043 |         0.0045 |      -1.01e-10 |      -2.88e-10 |
| 50%        |         0.0228 |         0.0238 |       2.62e-10 |       7.46e-10 |
| 75%        |         0.0651 |         0.0669 |       1.75e-07 |       4.99e-07 |
| max        |        86.0362 |        86.0362 |         6.8422 |        19.5251 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 1.0094 * stata
- **R-squared**: 0.9955
- **N observations**: 1,231,412

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.07e-04 |     2.17e-05 |     37.1894 |     0.000 |
| Slope       |       1.0094 |     6.09e-05 |  16562.4815 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72379/1231412 (5.878%)
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

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.65e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.10e+06 |       2.10e+06 |       2.10e+06 |       2.10e+06 |
| mean       |         0.1168 |         0.1168 |      -6.16e-08 |      -1.22e-07 |
| std        |         0.5041 |         0.5040 |       3.91e-04 |       7.76e-04 |
| min        |      -162.6901 |      -162.6901 |        -0.2216 |        -0.4396 |
| 25%        |         0.0533 |         0.0533 |      -3.47e-09 |      -6.89e-09 |
| 50%        |         0.1320 |         0.1320 |       4.61e-12 |       9.15e-12 |
| 75%        |         0.2129 |         0.2129 |       3.50e-09 |       6.94e-09 |
| max        |        26.7835 |        26.7835 |         0.1114 |         0.2211 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,103,518

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.12e-07 |     2.77e-07 |      0.7676 |     0.443 |
| Slope       |       1.0000 |     5.35e-07 |    1.87e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 186/2103518 (0.009%)
- Stata standard deviation: 5.04e-01

---

### CBOperProfLagAT_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CBOperProfLagAT_q']

**Observations**:
- Stata:  1,911,489
- Python: 1,978,675
- Common: 1,911,448

**Precision1**: 0.053% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.79e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         0.0219 |         0.0219 |       6.74e-06 |       3.84e-05 |
| std        |         0.1758 |         0.1758 |         0.0035 |         0.0199 |
| min        |       -89.0698 |       -89.0698 |        -0.6121 |        -3.4823 |
| 25%        |        -0.0051 |        -0.0051 |      -9.07e-10 |      -5.16e-09 |
| 50%        |         0.0278 |         0.0278 |         0.0000 |         0.0000 |
| 75%        |         0.0571 |         0.0571 |       9.11e-10 |       5.18e-09 |
| max        |        22.7565 |        22.7565 |         1.8353 |        10.4414 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9996
- **N observations**: 1,911,448

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.04e-05 |     2.55e-06 |      4.0793 |     0.000 |
| Slope       |       0.9998 |     1.44e-05 |  69343.8157 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1006/1911448 (0.053%)
- Stata standard deviation: 1.76e-01

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
- Python: 3,041,093
- Common: 2,797,878

**Precision1**: 0.020% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.80e+06 |       2.80e+06 |       2.80e+06 |       2.80e+06 |
| mean       |        -0.0128 |        -0.0128 |       1.39e-05 |       1.18e-05 |
| std        |         1.1714 |         1.1714 |         0.0080 |         0.0069 |
| min        |      -917.6409 |      -917.6410 |        -1.6696 |        -1.4252 |
| 25%        |         0.0039 |         0.0039 |      -6.64e-10 |      -5.67e-10 |
| 50%        |         0.0195 |         0.0195 |      -4.51e-14 |      -3.85e-14 |
| 75%        |         0.0369 |         0.0369 |       6.62e-10 |       5.65e-10 |
| max        |       163.1038 |       163.1038 |         8.6011 |         7.3423 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,797,878

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.33e-05 |     4.80e-06 |      2.7786 |     0.005 |
| Slope       |       1.0000 |     4.10e-06 | 244098.1884 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 572/2797878 (0.020%)
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
- Python: 2,987,368
- Common: 2,985,685

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.51e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.99e+06 |       2.99e+06 |       2.99e+06 |       2.99e+06 |
| mean       |         1.1455 |         1.1455 |       3.07e-07 |       1.71e-07 |
| std        |         1.7917 |         1.7917 |       2.21e-04 |       1.23e-04 |
| min        |        -1.8804 |        -1.8804 |        -0.0353 |        -0.0197 |
| 25%        |         0.3456 |         0.3456 |      -1.39e-08 |      -7.78e-09 |
| 50%        |         0.9236 |         0.9236 |         0.0000 |         0.0000 |
| 75%        |         1.5797 |         1.5797 |       1.43e-08 |       7.98e-09 |
| max        |       392.8943 |       392.8943 |         0.0736 |         0.0411 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,985,685

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.43e-07 |     1.52e-07 |      2.9220 |     0.003 |
| Slope       |       1.0000 |     7.14e-08 |    1.40e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 36/2985685 (0.001%)
- Stata standard deviation: 1.79e+00

---

### CapTurnover_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['CapTurnover_q']

**Observations**:
- Stata:  2,486,325
- Python: 2,486,376
- Common: 2,486,271

**Precision1**: 0.013% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |         0.2638 |         0.2638 |      -1.75e-06 |      -5.59e-07 |
| std        |         3.1372 |         3.1372 |         0.0138 |         0.0044 |
| min        |        -0.9789 |        -0.9789 |        -8.8194 |        -2.8112 |
| 25%        |         0.0801 |         0.0801 |      -3.40e-09 |      -1.08e-09 |
| 50%        |         0.2127 |         0.2127 |         0.0000 |         0.0000 |
| 75%        |         0.3650 |         0.3650 |       3.40e-09 |       1.08e-09 |
| max        |      2816.9070 |      2816.9070 |         6.0506 |         1.9286 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,486,271

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.87e-07 |     8.77e-06 |      0.1011 |     0.919 |
| Slope       |       1.0000 |     2.79e-06 | 358808.8077 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 325/2486271 (0.013%)
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
- Python: 3,297,096
- Common: 3,295,125

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.50e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0889 |         0.0889 |      -2.05e-06 |      -2.29e-06 |
| std        |         0.8966 |         0.8966 |         0.0016 |         0.0018 |
| min        |        -1.4114 |        -1.4114 |        -0.7511 |        -0.8377 |
| 25%        |        -0.0138 |        -0.0138 |      -9.90e-09 |      -1.10e-08 |
| 50%        |         0.0232 |         0.0232 |         0.0000 |         0.0000 |
| 75%        |         0.0917 |         0.0917 |       9.89e-09 |       1.10e-08 |
| max        |       192.5833 |       192.5833 |         0.3378 |         0.3768 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,125

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.03e-06 |     8.99e-07 |     -2.2611 |     0.024 |
| Slope       |       1.0000 |     9.97e-07 |    1.00e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 228/3295125 (0.007%)
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
- Python: 3,251,345
- Common: 3,249,290

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.80e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.25e+06 |       3.25e+06 |       3.25e+06 |       3.25e+06 |
| mean       |         0.0487 |         0.0487 |      -2.83e-06 |      -2.92e-06 |
| std        |         0.9693 |         0.9693 |         0.0013 |         0.0013 |
| min        |       -23.0669 |       -23.0669 |        -0.6600 |        -0.6808 |
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
| Intercept   |    -2.16e-06 |     7.15e-07 |     -3.0266 |     0.002 |
| Slope       |       1.0000 |     7.36e-07 |    1.36e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 192/3249290 (0.006%)
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
- Python: 3,250,343
- Common: 3,222,277

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.32e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.3833 |        -0.3833 |       3.53e-06 |       2.33e-08 |
| std        |       151.4586 |       151.4586 |         0.0089 |       5.87e-05 |
| min        |    -30903.6450 |    -30903.6451 |        -3.1309 |        -0.0207 |
| 25%        |        -0.0312 |        -0.0312 |      -2.22e-09 |      -1.47e-11 |
| 50%        |      -1.17e-04 |      -1.17e-04 |       6.89e-12 |       4.55e-14 |
| 75%        |         0.0251 |         0.0251 |       2.23e-09 |       1.48e-11 |
| max        |     24410.3810 |     24410.3806 |         3.2878 |         0.0217 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,277

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.53e-06 |     4.95e-06 |      0.7126 |     0.476 |
| Slope       |       1.0000 |     3.27e-08 |    3.06e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/3222277 (0.001%)
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
- Python: 2,389,987
- Common: 2,296,768

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.72e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.30e+06 |       2.30e+06 |       2.30e+06 |       2.30e+06 |
| mean       |        -0.0019 |        -0.0019 |       2.10e-06 |       8.97e-06 |
| std        |         0.2344 |         0.2344 |         0.0024 |         0.0102 |
| min        |       -55.1174 |       -55.1174 |        -0.8505 |        -3.6276 |
| 25%        |        -0.0078 |        -0.0078 |      -4.27e-10 |      -1.82e-09 |
| 50%        |      -7.35e-05 |      -7.34e-05 |      -3.68e-13 |      -1.57e-12 |
| 75%        |         0.0058 |         0.0058 |       4.28e-10 |       1.83e-09 |
| max        |       136.3447 |       136.3447 |         1.3543 |         5.7764 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 2,296,768

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.95e-06 |     1.57e-06 |      1.2417 |     0.214 |
| Slope       |       0.9999 |     6.70e-06 | 149137.2741 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 567/2296768 (0.025%)
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
- Python: 2,435,546
- Common: 2,360,216

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.26e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.36e+06 |       2.36e+06 |       2.36e+06 |       2.36e+06 |
| mean       |      -8.46e-04 |      -8.49e-04 |      -3.65e-06 |      -1.17e-07 |
| std        |        31.1263 |        31.1265 |         0.0976 |         0.0031 |
| min        |    -14927.4960 |    -14927.4966 |       -61.0000 |        -1.9598 |
| 25%        |        -0.0196 |        -0.0196 |      -1.10e-09 |      -3.53e-11 |
| 50%        |      -6.95e-04 |      -6.94e-04 |      -1.27e-12 |      -4.09e-14 |
| 75%        |         0.0130 |         0.0130 |       1.09e-09 |       3.50e-11 |
| max        |     14925.0560 |     14925.0557 |        61.0000 |         1.9598 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,360,216

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.65e-06 |     6.35e-05 |     -0.0575 |     0.954 |
| Slope       |       1.0000 |     2.04e-06 | 489862.3152 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 91/2360216 (0.004%)
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
- Python: 3,297,096
- Common: 3,295,155

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.05e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.30e+06 |       3.30e+06 |       3.30e+06 |       3.30e+06 |
| mean       |         0.0019 |         0.0019 |      -2.37e-07 |      -2.37e-06 |
| std        |         0.0999 |         0.0999 |       4.29e-04 |         0.0043 |
| min        |        -1.8790 |        -1.8790 |        -0.2141 |        -2.1431 |
| 25%        |      -6.70e-06 |      -6.63e-06 |      -1.32e-12 |      -1.32e-11 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |       2.58e-04 |       2.59e-04 |       1.35e-12 |       1.35e-11 |
| max        |         1.8457 |         1.8457 |         0.0605 |         0.6054 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,295,155

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.68e-07 |     2.36e-07 |     -1.1333 |     0.257 |
| Slope       |       1.0000 |     2.37e-06 | 422581.7802 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 264/3295155 (0.008%)
- Stata standard deviation: 9.99e-02

---

### DelayAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6092 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayAcct']

**Observations**:
- Stata:  674,090
- Python: 675,349
- Common: 667,998

**Precision1**: 66.043% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.70e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    667998.0000 |    667998.0000 |    667998.0000 |    667998.0000 |
| mean       |         0.1913 |         0.1907 |      -6.03e-04 |        -0.0063 |
| std        |         0.0959 |         0.0956 |         0.0069 |         0.0716 |
| min        |        -0.4104 |        -0.4166 |        -0.5505 |        -5.7425 |
| 25%        |         0.1117 |         0.1109 |        -0.0021 |        -0.0224 |
| 50%        |         0.1722 |         0.1728 |      -4.52e-04 |        -0.0047 |
| 75%        |         0.2702 |         0.2699 |         0.0010 |         0.0108 |
| max        |         1.3192 |         1.3166 |         0.5717 |         5.9638 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0005 + 0.9943 * stata
- **R-squared**: 0.9949
- **N observations**: 667,998

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.95e-04 |     1.87e-05 |     26.4813 |     0.000 |
| Slope       |       0.9943 |     8.73e-05 |  11384.2081 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayAcct
     0   10001  199311   0.336795
     1   10012  200208   0.207148
     2   10012  200209   0.217094
     3   10016  199805   0.390521
     4   10062  199311   0.366439
     5   10116  201508   0.121925
     6   10137  199709   0.275193
     7   10235  200001   0.262848
     8   10239  199506   0.308485
     9   10239  199507   0.357610
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 441164/667998 (66.043%)
- Stata standard deviation: 9.59e-02

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202407  0.224656  0.220374  0.004282
1   10032  202407  0.145375  0.142951  0.002424
2   10138  202407  0.157249  0.161488 -0.004239
3   10200  202407  0.140958  0.144167 -0.003209
4   10220  202407  0.173979  0.171523  0.002456
5   10258  202407  0.147825  0.151306 -0.003481
6   10318  202407  0.134704  0.138319 -0.003615
7   10382  202407  0.181288  0.184804 -0.003515
8   10421  202407  0.155363  0.157009 -0.001645
9   10517  202407  0.320318  0.321542 -0.001225
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   85705  200706  0.740964  0.169225  0.571738
1   21872  199004  0.288854  0.839375 -0.550521
2   85705  200705  0.687626  0.160952  0.526674
3   85705  200611  0.628556  0.144539  0.484017
4   85705  200609  0.641397  0.157428  0.483969
5   85705  200610  0.613998  0.150461  0.463537
6   85705  200607  0.589950  0.153971  0.435978
7   85705  200608  0.588336  0.154959  0.433378
8   85705  200707  0.569168  0.141587  0.427581
9   85705  200801  0.533253  0.110461  0.422793
```

---

### DelayNonAcct

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 6092 Stata observations)
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DelayNonAcct']

**Observations**:
- Stata:  674,090
- Python: 675,349
- Common: 667,998

**Precision1**: 43.598% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.27e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    667998.0000 |    667998.0000 |    667998.0000 |    667998.0000 |
| mean       |      -5.68e-04 |       3.06e-05 |       5.99e-04 |         0.0029 |
| std        |         0.2046 |         0.2045 |         0.0069 |         0.0339 |
| min        |        -0.8858 |        -0.9530 |        -0.5718 |        -2.7950 |
| 25%        |        -0.1140 |        -0.1133 |        -0.0011 |        -0.0053 |
| 50%        |        -0.0509 |        -0.0505 |       4.47e-04 |         0.0022 |
| 75%        |         0.0445 |         0.0451 |         0.0022 |         0.0106 |
| max        |         0.9457 |         0.9458 |         0.5509 |         2.6928 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9993 * stata
- **R-squared**: 0.9989
- **N observations**: 667,998

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.99e-04 |     8.48e-06 |     70.5676 |     0.000 |
| Slope       |       0.9993 |     4.15e-05 |  24099.1435 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  DelayNonAcct
     0   10001  199311      0.661581
     1   10012  200208     -0.166785
     2   10012  200209     -0.176730
     3   10016  199805      0.158209
     4   10062  199311      0.215670
     5   10116  201508      0.689750
     6   10137  199709     -0.227305
     7   10235  200001     -0.125564
     8   10239  199506      0.357900
     9   10239  199507      0.570551
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 291234/667998 (43.598%)
- Stata standard deviation: 2.05e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   10028  202407 -0.174312 -0.170063 -0.004249
1   10032  202407 -0.088146 -0.085633 -0.002513
2   10138  202407 -0.140349 -0.144541  0.004193
3   10200  202407 -0.112977 -0.116077  0.003100
4   10258  202407  0.054295  0.051251  0.003043
5   10318  202407 -0.112310 -0.115925  0.003615
6   10382  202407 -0.029959 -0.033574  0.003614
7   10421  202407 -0.055077 -0.057301  0.002224
8   10547  202407 -0.285096 -0.276424 -0.008673
9   10606  202407 -0.099612 -0.102583  0.002972
```

**Largest Differences**:
```
   permno  yyyymm    python     stata      diff
0   85705  200706  0.218257  0.790008 -0.571751
1   21872  199004  0.544062 -0.006797  0.550858
2   85705  200705  0.271594  0.798281 -0.526687
3   85705  200611  0.330665  0.814694 -0.484030
4   85705  200609  0.317823  0.801805 -0.483981
5   85705  200610  0.345222  0.808772 -0.463549
6   85705  200607  0.369271  0.805262 -0.435991
7   85705  200608  0.370884  0.804274 -0.433390
8   85705  200707  0.153286  0.582479 -0.429193
9   85705  200801  0.189201  0.613606 -0.424405
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
- Python: 2,014,930
- Common: 421,383

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.24e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    421383.0000 |    421383.0000 |    421383.0000 |    421383.0000 |
| mean       |         0.0490 |         0.0490 |       4.91e-05 |       8.57e-05 |
| std        |         0.5731 |         0.5726 |         0.0269 |         0.0469 |
| min        |         0.0000 |         0.0000 |        -1.7481 |        -3.0501 |
| 25%        |         0.0201 |         0.0201 |      -1.01e-09 |      -1.77e-09 |
| 50%        |         0.0356 |         0.0356 |      -1.99e-11 |      -3.48e-11 |
| 75%        |         0.0554 |         0.0554 |       4.69e-10 |       8.19e-10 |
| max        |       154.9091 |       154.9091 |        13.8577 |        24.1787 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9979 * stata
- **R-squared**: 0.9978
- **N observations**: 421,383

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.50e-04 |     4.15e-05 |      3.6065 |     0.000 |
| Slope       |       0.9979 |     7.22e-05 |  13830.8506 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30/421383 (0.007%)
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

**Precision1**: 0.053% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.12e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.88e+06 |       3.88e+06 |       3.88e+06 |       3.88e+06 |
| mean       |         0.0239 |         0.0239 |       3.73e-05 |       1.80e-04 |
| std        |         0.2072 |         0.2076 |         0.0101 |         0.0488 |
| min        |        -0.5405 |        -0.5405 |        -1.5984 |        -7.7145 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0299 |         0.0299 |         0.0000 |         0.0000 |
| max        |        83.2000 |        83.2000 |         6.1759 |        29.8080 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0008 * stata
- **R-squared**: 0.9976
- **N observations**: 3,878,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.90e-05 |     5.17e-06 |      3.6702 |     0.000 |
| Slope       |       1.0008 |     2.48e-05 |  40370.3962 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 2060/3878713 (0.053%)
- Stata standard deviation: 2.07e-01

---

### DownsideBeta

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ❌ FAILED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['DownsideBeta']

**Observations**:
- Stata:  4,848,559
- Python: 5,072,351
- Common: 4,848,552

**Precision1**: 19.351% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.74e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.85e+06 |       4.85e+06 |       4.85e+06 |       4.85e+06 |
| mean       |         0.8537 |         0.8543 |       6.00e-04 |       8.34e-04 |
| std        |         0.7191 |         0.7201 |         0.0530 |         0.0737 |
| min        |       -43.6149 |       -43.6034 |       -17.8849 |       -24.8725 |
| 25%        |         0.4076 |         0.4080 |      -6.43e-04 |      -8.95e-04 |
| 50%        |         0.8185 |         0.8190 |       9.52e-05 |       1.32e-04 |
| 75%        |         1.2309 |         1.2316 |         0.0012 |         0.0016 |
| max        |        16.0159 |        22.7108 |        22.2480 |        30.9402 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0017 + 0.9988 * stata
- **R-squared**: 0.9946
- **N observations**: 4,848,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0017 |     3.73e-05 |     44.3783 |     0.000 |
| Slope       |       0.9988 |     3.35e-05 |  29855.7059 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 938264/4848552 (19.351%)
- Stata standard deviation: 7.19e-01

**Most Recent Bad Observations**:
```
   permno  yyyymm    python     stata      diff
0   16680  202412 -0.288771 -0.279329 -0.009443
1   19014  202412  1.500611  1.490741  0.009870
2   19066  202412  2.207404  2.217591 -0.010187
3   19146  202412  0.962848  0.955032  0.007816
4   19147  202412  3.032554  3.016006  0.016548
5   20292  202412  1.655575  1.647555  0.008019
6   20334  202412  1.157843  1.165704 -0.007861
7   20638  202412 -0.351702 -0.362992  0.011289
8   21114  202412  9.236139  9.247963 -0.011824
9   21539  202412  1.794273  1.785916  0.008357
```

**Largest Differences**:
```
   permno  yyyymm     python     stata       diff
0   11818  192608  19.061026 -3.186927  22.247954
1   11412  192608  22.710776  3.952252  18.758523
2   10815  192608  15.747186 -2.698489  18.445674
3   10583  192608 -15.932580  1.952304 -17.884885
4   11383  192609 -15.923443 -2.731694 -13.191749
5   14648  192608  15.302066  2.676733  12.625333
6   11818  192609   8.157301 -1.672886   9.830186
7   12714  192609   8.802288 -0.983153   9.785441
8   10655  192608  -8.780685  0.721612  -9.502297
9   10655  192612  -8.503854  0.846114  -9.349969
```

---

### EBM_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EBM_q']

**Observations**:
- Stata:  2,497,505
- Python: 2,497,530
- Common: 2,497,418

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.89e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.50e+06 |       2.50e+06 |       2.50e+06 |       2.50e+06 |
| mean       |         0.5320 |         0.5337 |         0.0016 |       7.70e-06 |
| std        |       210.6180 |       212.5570 |         2.5521 |         0.0121 |
| min        |   -135089.5600 |   -136046.0000 |      -956.4400 |        -4.5411 |
| 25%        |         0.1800 |         0.1800 |      -1.71e-08 |      -8.14e-11 |
| 50%        |         0.5004 |         0.5004 |      -1.04e-11 |      -4.93e-14 |
| 75%        |         0.9606 |         0.9606 |       1.71e-08 |       8.14e-11 |
| max        |    215285.7300 |    219000.0000 |      3714.2700 |        17.6351 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0033 + 1.0092 * stata
- **R-squared**: 0.9999
- **N observations**: 2,497,418

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0033 |       0.0011 |     -3.0906 |     0.002 |
| Slope       |       1.0092 |     5.01e-06 | 201493.0408 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 63/2497418 (0.003%)
- Stata standard deviation: 2.11e+02

---

### EPq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EPq']

**Observations**:
- Stata:  1,893,938
- Python: 1,893,957
- Common: 1,893,883

**Precision1**: 0.009% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.17e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.89e+06 |       1.89e+06 |       1.89e+06 |       1.89e+06 |
| mean       |         0.0273 |         0.0273 |       2.94e-07 |       2.93e-06 |
| std        |         0.1001 |         0.1001 |       3.17e-04 |         0.0032 |
| min        |         0.0000 |         0.0000 |        -0.0547 |        -0.5459 |
| 25%        |         0.0107 |         0.0107 |      -4.38e-10 |      -4.38e-09 |
| 50%        |         0.0180 |         0.0180 |         0.0000 |         0.0000 |
| 75%        |         0.0297 |         0.0297 |       4.39e-10 |       4.39e-09 |
| max        |        35.0386 |        35.0386 |         0.2346 |         2.3426 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,893,883

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.23e-07 |     2.39e-07 |      1.7715 |     0.076 |
| Slope       |       1.0000 |     2.30e-06 | 434679.1936 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 179/1893883 (0.009%)
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
- Python: 2,659,321
- Common: 2,657,230

**Precision1**: 0.026% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.17e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.66e+06 |       2.66e+06 |       2.66e+06 |       2.66e+06 |
| mean       |       200.8662 |       310.3177 |       109.4515 |         0.0011 |
| std        |     96619.4326 |    148863.3909 |     89150.5529 |         0.9227 |
| min        |      -2.82e+07 |      -7.90e+07 |      -7.13e+07 |      -738.0394 |
| 25%        |      -6.25e-04 |      -6.26e-04 |      -1.44e-10 |      -1.49e-15 |
| 50%        |         0.0000 |         0.0000 |        -0.0000 |        -0.0000 |
| 75%        |         0.0010 |         0.0010 |       1.45e-10 |       1.50e-15 |
| max        |       3.75e+07 |       5.07e+07 |       3.69e+07 |       381.9033 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 56.9809 + 1.2612 * stata
- **R-squared**: 0.6701
- **N observations**: 2,657,230

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      56.9809 |      52.4529 |      1.0863 |     0.277 |
| Slope       |       1.2612 |     5.43e-04 |   2323.2053 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 689/2657230 (0.026%)
- Stata standard deviation: 9.66e+04

---

### EarningsConservatism

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsConservatism']

**Observations**:
- Stata:  1,467,671
- Python: 1,495,202
- Common: 1,467,671

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.45e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.47e+06 |       1.47e+06 |       1.47e+06 |       1.47e+06 |
| mean       |       -60.3159 |       -60.3726 |        -0.0567 |      -2.91e-06 |
| std        |     19491.2782 |     19490.5670 |        15.2672 |       7.83e-04 |
| min        |      -6.48e+06 |      -6.48e+06 |     -4582.1725 |        -0.2351 |
| 25%        |        -5.1421 |        -5.1259 |      -6.14e-07 |      -3.15e-11 |
| 50%        |         0.9096 |         0.9198 |         0.0000 |         0.0000 |
| 75%        |         5.4537 |         5.4463 |       6.39e-07 |       3.28e-11 |
| max        |    872129.2500 |    872120.6238 |       243.2624 |         0.0125 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0589 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,467,671

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0589 |       0.0126 |     -4.6773 |     0.000 |
| Slope       |       1.0000 |     6.46e-07 |    1.55e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 84/1467671 (0.006%)
- Stata standard deviation: 1.95e+04

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
- Python: 1,501,717
- Common: 1,495,672

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.13e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |         0.4579 |         0.4579 |      -1.18e-05 |      -1.96e-05 |
| std        |         0.5997 |         0.5997 |         0.0026 |         0.0044 |
| min        |      -119.0719 |      -119.0719 |        -0.7309 |        -1.2188 |
| 25%        |         0.1421 |         0.1421 |      -1.11e-08 |      -1.85e-08 |
| 50%        |         0.4517 |         0.4517 |      -5.28e-12 |      -8.80e-12 |
| 75%        |         0.7670 |         0.7670 |       1.08e-08 |       1.80e-08 |
| max        |        14.3520 |        14.3520 |         0.2564 |         0.4276 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.30e-05 |     2.70e-06 |     -4.8194 |     0.000 |
| Slope       |       1.0000 |     3.58e-06 | 279444.5075 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 99/1495672 (0.007%)
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
- Python: 1,501,717
- Common: 1,495,672

**Precision1**: 0.008% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.50e-16 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.50e+06 |       1.50e+06 |       1.50e+06 |       1.50e+06 |
| mean       |       2.99e+11 |       1.58e+12 |       1.28e+12 |         0.0317 |
| std        |       4.05e+13 |       4.68e+14 |       4.32e+14 |        10.6721 |
| min        |         0.0000 |         0.0000 |      -2.58e+13 |        -0.6367 |
| 25%        |         0.0446 |         0.0445 |      -1.03e-08 |      -2.53e-22 |
| 50%        |         0.2784 |         0.2789 |       6.50e-13 |       1.60e-26 |
| 75%        |         1.7905 |         1.7993 |       1.03e-08 |       2.55e-22 |
| max        |       1.23e+16 |       1.65e+17 |       1.53e+17 |      3766.1862 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -1455853807476.9307 + 10.1566 * stata
- **R-squared**: 0.7744
- **N observations**: 1,495,672

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.46e+12 |     1.82e+11 |     -8.0166 |     0.000 |
| Slope       |      10.1566 |       0.0045 |   2265.9476 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 120/1495672 (0.008%)
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
- Python: 1,539,289
- Common: 1,482,823

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.07e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.48e+06 |       1.48e+06 |       1.48e+06 |       1.48e+06 |
| mean       |         0.6548 |         0.6548 |       8.18e-07 |       2.06e-06 |
| std        |         0.3971 |         0.3971 |       3.30e-04 |       8.31e-04 |
| min        |         0.0036 |         0.0036 |        -0.0287 |        -0.0722 |
| 25%        |         0.3480 |         0.3480 |      -1.50e-08 |      -3.78e-08 |
| 50%        |         0.6297 |         0.6297 |       1.72e-11 |       4.33e-11 |
| 75%        |         0.9233 |         0.9233 |       1.51e-08 |       3.79e-08 |
| max        |         8.3146 |         8.3146 |         0.3090 |         0.7781 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,482,823

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.11e-06 |     5.23e-07 |      2.1196 |     0.034 |
| Slope       |       1.0000 |     6.82e-07 |    1.47e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 145/1482823 (0.010%)
- Stata standard deviation: 3.97e-01

---

### EarningsTimeliness

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EarningsTimeliness']

**Observations**:
- Stata:  1,467,923
- Python: 1,495,202
- Common: 1,467,923

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.75e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.47e+06 |       1.47e+06 |       1.47e+06 |       1.47e+06 |
| mean       |         0.3946 |         0.3946 |      -8.22e-08 |      -3.35e-07 |
| std        |         0.2455 |         0.2455 |       2.88e-05 |       1.17e-04 |
| min        |       6.46e-10 |       6.48e-10 |        -0.0101 |        -0.0410 |
| 25%        |         0.1930 |         0.1930 |      -1.34e-08 |      -5.47e-08 |
| 50%        |         0.3602 |         0.3602 |      -6.32e-11 |      -2.58e-10 |
| 75%        |         0.5716 |         0.5716 |       1.33e-08 |       5.40e-08 |
| max        |         1.0000 |         1.0000 |       5.69e-07 |       2.32e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,467,923

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.51e-08 |     4.49e-08 |     -1.0046 |     0.315 |
| Slope       |       1.0000 |     9.67e-08 |    1.03e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/1467923 (0.001%)
- Stata standard deviation: 2.45e-01

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
- Python: 1,457,273
- Common: 1,427,774

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.44e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.43e+06 |       1.43e+06 |       1.43e+06 |       1.43e+06 |
| mean       |         0.3224 |         0.3224 |       2.76e-07 |       1.29e-06 |
| std        |         0.2136 |         0.2136 |       9.51e-05 |       4.45e-04 |
| min        |       5.13e-06 |       5.13e-06 |      -3.86e-07 |      -1.81e-06 |
| 25%        |         0.1458 |         0.1458 |      -9.53e-09 |      -4.46e-08 |
| 50%        |         0.2926 |         0.2926 |       3.59e-11 |       1.68e-10 |
| 75%        |         0.4707 |         0.4707 |       9.68e-09 |       4.53e-08 |
| max        |         0.9929 |         0.9929 |         0.0328 |         0.1535 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,427,774

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.26e-07 |     1.44e-07 |      4.3457 |     0.000 |
| Slope       |       1.0000 |     3.72e-07 |    2.68e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/1427774 (0.001%)
- Stata standard deviation: 2.14e-01

---

### EntMult_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['EntMult_q']

**Observations**:
- Stata:  1,689,737
- Python: 1,691,201
- Common: 1,689,593

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.40e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.69e+06 |       1.69e+06 |       1.69e+06 |       1.69e+06 |
| mean       |        87.8823 |        87.8677 |        -0.0145 |      -4.64e-06 |
| std        |      3126.4388 |      3126.4204 |        10.4454 |         0.0033 |
| min        |    -43431.7380 |    -43431.7391 |     -7731.1405 |        -2.4728 |
| 25%        |        20.2672 |        20.2677 |      -7.63e-07 |      -2.44e-10 |
| 50%        |        32.0420 |        32.0420 |      -2.84e-14 |      -9.09e-18 |
| 75%        |        51.5093 |        51.5100 |       7.53e-07 |       2.41e-10 |
| max        |       1.43e+06 |       1.43e+06 |       642.1284 |         0.2054 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0135 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,689,593

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0135 |       0.0080 |     -1.6810 |     0.093 |
| Slope       |       1.0000 |     2.57e-06 | 389055.8599 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 103/1689593 (0.006%)
- Stata standard deviation: 3.13e+03

---

### FRbook

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['FRbook']

**Observations**:
- Stata:  684,322
- Python: 684,322
- Common: 684,322

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    684322.0000 |    684322.0000 |    684322.0000 |    684322.0000 |
| mean       |        -0.0069 |        -0.0069 |      -1.55e-11 |      -1.29e-10 |
| std        |         0.1200 |         0.1200 |       1.52e-08 |       1.27e-07 |
| min        |       -39.0165 |       -39.0165 |      -5.02e-06 |      -4.18e-05 |
| 25%        |        -0.0158 |        -0.0158 |      -8.08e-10 |      -6.74e-09 |
| 50%        |        -0.0012 |        -0.0012 |         0.0000 |         0.0000 |
| 75%        |         0.0043 |         0.0043 |       8.16e-10 |       6.80e-09 |
| max        |         1.8105 |         1.8105 |       4.58e-07 |       3.82e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 684,322

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.65e-10 |     1.14e-11 |     58.1352 |     0.000 |
| Slope       |       1.0000 |     9.52e-11 |    1.05e+10 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/684322 (0.000%)
- Stata standard deviation: 1.20e-01

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
- Python: 1,958,928
- Common: 1,958,739

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.65e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.96e+06 |       1.96e+06 |       1.96e+06 |       1.96e+06 |
| mean       |       1.08e+06 |       1.08e+06 |       -12.3425 |      -5.77e-07 |
| std        |       2.14e+07 |       2.14e+07 |       456.4276 |       2.13e-05 |
| min        |       -10.0057 |       -10.0054 |    -16928.8988 |      -7.92e-04 |
| 25%        |        -5.9270 |        -5.9270 |      -5.15e-07 |      -2.41e-14 |
| 50%        |        -4.5351 |        -4.5350 |       1.55e-05 |       7.25e-13 |
| 75%        |        -2.0932 |        -2.0932 |       6.71e-05 |       3.14e-12 |
| max        |       6.77e+08 |       6.77e+08 |        61.2658 |       2.87e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 7.3465 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,958,739

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       7.3465 |       0.1697 |     43.3021 |     0.000 |
| Slope       |       1.0000 |     7.93e-09 |    1.26e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/1958739 (0.000%)
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
- Python: 2,148,742
- Common: 2,090,910

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.23e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.09e+06 |       2.09e+06 |       2.09e+06 |       2.09e+06 |
| mean       |       1.03e+06 |       1.03e+06 |       -11.1262 |      -5.38e-07 |
| std        |       2.07e+07 |       2.07e+07 |       433.4000 |       2.09e-05 |
| min        |        -9.7055 |        -9.7053 |    -16928.8351 |      -8.18e-04 |
| 25%        |        -5.9385 |        -5.9387 |      -2.33e-07 |      -1.13e-14 |
| 50%        |        -4.5879 |        -4.5880 |       1.91e-05 |       9.21e-13 |
| 75%        |        -2.2171 |        -2.2171 |       6.50e-05 |       3.14e-12 |
| max        |       6.77e+08 |       6.77e+08 |        51.7171 |       2.50e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 7.0251 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,090,910

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       7.0251 |       0.1638 |     42.8971 |     0.000 |
| Slope       |       1.0000 |     7.90e-09 |    1.27e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2090910 (0.000%)
- Stata standard deviation: 2.07e+07

---

### ForecastDispersionLT

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 7604 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ForecastDispersionLT']

**Observations**:
- Stata:  828,578
- Python: 828,777
- Common: 820,974

**Precision1**: 0.085% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.49e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    820974.0000 |    820974.0000 |    820974.0000 |    820974.0000 |
| mean       |         4.5450 |         4.5450 |       5.39e-05 |       8.01e-06 |
| std        |         6.7258 |         6.7265 |         0.2252 |         0.0335 |
| min        |         0.0000 |         0.0000 |      -115.8600 |       -17.2262 |
| 25%        |         1.7200 |         1.7200 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         5.2000 |         5.2000 |       2.00e-08 |       2.97e-09 |
| max        |       623.7400 |       623.7400 |       115.8600 |        17.2262 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0021 + 0.9995 * stata
- **R-squared**: 0.9989
- **N observations**: 820,974

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0021 |     3.00e-04 |      7.0081 |     0.000 |
| Slope       |       0.9995 |     3.69e-05 |  27054.3472 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ForecastDispersionLT
     0   10016  199805                  6.03
     1   10104  202412                  1.77
     2   10107  202412                  2.21
     3   10122  199711                  0.00
     4   10137  199709                  1.57
     5   10138  200012                  3.17
     6   10145  198403                  3.20
     7   10145  198404                  3.20
     8   10145  198405                  3.00
     9   10145  198406                  2.80
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 694/820974 (0.085%)
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
- Python: 3,299,098
- Common: 3,281,500

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.67e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.28e+06 |       3.28e+06 |       3.28e+06 |       3.28e+06 |
| mean       |         0.3420 |         0.3420 |      -6.35e-06 |      -5.60e-06 |
| std        |         1.1339 |         1.1339 |         0.0065 |         0.0057 |
| min        |       -28.7301 |       -28.7301 |        -2.7728 |        -2.4454 |
| 25%        |         0.0981 |         0.0981 |      -4.84e-09 |      -4.27e-09 |
| 50%        |         0.2774 |         0.2774 |         0.0000 |         0.0000 |
| 75%        |         0.4978 |         0.4978 |       4.90e-09 |       4.32e-09 |
| max        |       282.3216 |       282.3216 |         1.0171 |         0.8970 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,281,500

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.54e-07 |     3.74e-06 |     -0.2546 |     0.799 |
| Slope       |       1.0000 |     3.16e-06 | 316240.8335 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 720/3281500 (0.022%)
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
- Python: 2,339,969
- Common: 2,216,579

**Precision1**: 0.037% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.83e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.22e+06 |       2.22e+06 |       2.22e+06 |       2.22e+06 |
| mean       |         0.0808 |         0.0808 |       5.41e-06 |       7.63e-06 |
| std        |         0.7089 |         0.7089 |         0.0065 |         0.0091 |
| min        |        -9.0482 |        -9.0482 |        -3.0442 |        -4.2943 |
| 25%        |         0.0314 |         0.0314 |      -1.36e-09 |      -1.92e-09 |
| 50%        |         0.0731 |         0.0731 |         0.0000 |         0.0000 |
| 75%        |         0.1240 |         0.1240 |       1.36e-09 |       1.92e-09 |
| max        |       598.7442 |       598.7442 |         3.2404 |         4.5711 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,216,579

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.51e-06 |     4.37e-06 |      1.7189 |     0.086 |
| Slope       |       1.0000 |     6.12e-06 | 163304.8505 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 825/2216579 (0.037%)
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
- Python: 3,231,484
- Common: 3,229,675

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.25e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |        -1.0320 |        -1.0308 |         0.0012 |       5.77e-06 |
| std        |       213.3399 |       212.9016 |         0.5417 |         0.0025 |
| min        |    -90231.3050 |    -89952.2742 |        -4.6620 |        -0.0219 |
| 25%        |        -0.0941 |        -0.0941 |      -2.50e-08 |      -1.17e-10 |
| 50%        |        -0.0024 |        -0.0024 |         0.0000 |         0.0000 |
| 75%        |         0.0784 |         0.0784 |       2.49e-08 |       1.17e-10 |
| max        |      7383.3198 |      7383.3528 |       279.0308 |         1.3079 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0009 + 0.9979 * stata
- **R-squared**: 1.0000
- **N observations**: 3,229,675

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.90e-04 |     1.77e-04 |     -5.0293 |     0.000 |
| Slope       |       0.9979 |     8.30e-07 |    1.20e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/3229675 (0.002%)
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
- Python: 3,172,225
- Common: 3,134,552

**Precision1**: 0.012% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.31e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.13e+06 |       3.13e+06 |       3.13e+06 |       3.13e+06 |
| mean       |        -0.7276 |        -0.7208 |         0.0068 |       2.50e-05 |
| std        |       272.2844 |       272.2685 |         2.4935 |         0.0092 |
| min        |    -93814.8910 |    -93814.8917 |      -122.8291 |        -0.4511 |
| 25%        |        -0.1435 |        -0.1436 |      -2.75e-09 |      -1.01e-11 |
| 50%        |         0.0056 |         0.0057 |       1.88e-12 |       6.92e-15 |
| 75%        |         0.1566 |         0.1568 |       2.77e-09 |       1.02e-11 |
| max        |     51770.8950 |     51770.8949 |      1176.6455 |         4.3214 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0067 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 3,134,552

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0067 |       0.0014 |      4.7854 |     0.000 |
| Slope       |       0.9999 |     5.17e-06 | 193322.5259 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 364/3134552 (0.012%)
- Stata standard deviation: 2.72e+02

---

### IdioVolCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 38931 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IdioVolCAPM']

**Observations**:
- Stata:  5,026,821
- Python: 4,987,890
- Common: 4,987,890

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.03e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.99e+06 |       4.99e+06 |       4.99e+06 |       4.99e+06 |
| mean       |         0.0273 |         0.0273 |      -1.47e-08 |      -4.86e-07 |
| std        |         0.0304 |         0.0304 |       8.55e-06 |       2.81e-04 |
| min        |         0.0000 |         0.0000 |        -0.0021 |        -0.0708 |
| 25%        |         0.0113 |         0.0113 |      -7.46e-07 |      -2.46e-05 |
| 50%        |         0.0195 |         0.0195 |      -3.47e-18 |      -1.14e-16 |
| 75%        |         0.0337 |         0.0337 |       4.90e-07 |       1.61e-05 |
| max        |         8.4129 |         8.4129 |         0.0020 |         0.0650 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 4,987,890

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.50e-09 |     5.14e-09 |     -0.4856 |     0.627 |
| Slope       |       1.0000 |     1.26e-07 |    7.93e+06 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IdioVolCAPM
     0   10000  198706     0.000000
     1   10001  201708     0.000898
     2   10002  201302     0.008657
     3   10003  198601     0.021412
     4   10003  199512     0.020168
     5   10004  198601     0.000000
     6   10005  198601     0.051636
     7   10005  199107     0.044184
     8   10007  198601     0.037836
     9   10007  199010     0.251540
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 152/4987890 (0.003%)
- Stata standard deviation: 3.04e-02

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

**Precision2**: 99th percentile diff = 3.43e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.96e+06 |       3.96e+06 |       3.96e+06 |       3.96e+06 |
| mean       |         0.0255 |         0.0255 |       2.86e-13 |       1.05e-11 |
| std        |         0.0273 |         0.0273 |       2.52e-10 |       9.25e-09 |
| min        |         0.0000 |         0.0000 |      -2.33e-08 |      -8.56e-07 |
| 25%        |         0.0106 |         0.0106 |      -6.46e-11 |      -2.37e-09 |
| 50%        |         0.0185 |         0.0185 |      -2.21e-20 |      -8.12e-19 |
| 75%        |         0.0316 |         0.0316 |       6.49e-11 |       2.38e-09 |
| max        |         3.4183 |         3.4183 |       6.27e-08 |       2.30e-06 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,955,898

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.50e-12 |     1.74e-13 |    -20.1372 |     0.000 |
| Slope       |       1.0000 |     4.65e-12 |    2.15e+11 |     0.000 |

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

### IntrinsicValue

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 8808 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['IntrinsicValue']

**Observations**:
- Stata:  1,244,664
- Python: 1,301,064
- Common: 1,235,856

**Precision1**: 2.117% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.29e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.24e+06 |       1.24e+06 |       1.24e+06 |       1.24e+06 |
| mean       |         0.4657 |         0.4687 |         0.0031 |         0.0024 |
| std        |         1.2614 |         1.2678 |         0.0671 |         0.0532 |
| min        |       -51.3084 |       -51.3084 |        -2.7533 |        -2.1827 |
| 25%        |         0.0526 |         0.0527 |      -3.20e-08 |      -2.54e-08 |
| 50%        |         0.4591 |         0.4607 |      -4.83e-09 |      -3.83e-09 |
| 75%        |         0.7858 |         0.7888 |       1.58e-08 |       1.25e-08 |
| max        |        47.5224 |        47.5224 |         9.8992 |         7.8476 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0014 + 1.0036 * stata
- **R-squared**: 0.9972
- **N observations**: 1,235,856

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0014 |     6.42e-05 |     21.7505 |     0.000 |
| Slope       |       1.0036 |     4.77e-05 |  21022.2773 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  IntrinsicValue
     0   10145  197606         0.94617
     1   10145  197607         0.94617
     2   10145  197608         0.94617
     3   10145  197609         0.94617
     4   10145  197610         0.94617
     5   10145  197611         0.94617
     6   10145  197612         0.94617
     7   10145  197701         0.94617
     8   10145  197702         0.94617
     9   10145  197703         0.94617
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 26160/1235856 (2.117%)
- Stata standard deviation: 1.26e+00

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
- Python: 2,663,113
- Common: 2,630,499

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.06e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.63e+06 |       2.63e+06 |       2.63e+06 |       2.63e+06 |
| mean       |       -34.2550 |       -34.2551 |      -8.85e-05 |      -2.84e-08 |
| std        |      3118.1767 |      3118.1767 |         0.0395 |       1.27e-05 |
| min        |      -1.23e+06 |      -1.23e+06 |       -19.2429 |        -0.0062 |
| 25%        |        -5.2581 |        -5.2582 |      -4.30e-08 |      -1.38e-11 |
| 50%        |        -0.6982 |        -0.6982 |       2.30e-11 |       7.37e-15 |
| 75%        |         1.0179 |         1.0179 |       4.29e-08 |       1.37e-11 |
| max        |    205925.8400 |    205925.8463 |         3.3978 |         0.0011 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,630,499

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.84e-05 |     2.43e-05 |     -3.6340 |     0.000 |
| Slope       |       1.0000 |     7.80e-09 |    1.28e+08 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/2630499 (0.000%)
- Stata standard deviation: 3.12e+03

---

### KZ_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['KZ_q']

**Observations**:
- Stata:  1,936,942
- Python: 1,940,675
- Common: 1,936,689

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.36e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.94e+06 |       1.94e+06 |       1.94e+06 |       1.94e+06 |
| mean       |       -26.0747 |       -26.0759 |        -0.0012 |      -6.55e-07 |
| std        |      1776.1956 |      1776.1955 |         0.6689 |       3.77e-04 |
| min        |      -1.23e+06 |      -1.23e+06 |      -794.1236 |        -0.4471 |
| 25%        |        -4.8607 |        -4.8610 |      -4.19e-08 |      -2.36e-11 |
| 50%        |        -0.2486 |        -0.2486 |      -2.66e-11 |      -1.50e-14 |
| 75%        |         1.2951 |         1.2951 |       4.17e-08 |       2.35e-11 |
| max        |     26732.3870 |     26732.3858 |        15.1278 |         0.0085 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0012 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,936,689

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0012 |     4.81e-04 |     -2.4264 |     0.015 |
| Slope       |       1.0000 |     2.71e-07 |    3.70e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 19/1936689 (0.001%)
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
- Python: 2,990,300
- Common: 2,974,260

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.32e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.97e+06 |       2.97e+06 |       2.97e+06 |       2.97e+06 |
| mean       |         0.5044 |         0.5043 |      -3.75e-05 |      -1.02e-06 |
| std        |        36.7045 |        36.7045 |         0.0230 |       6.26e-04 |
| min        |      -247.4286 |      -247.4286 |        -9.9206 |        -0.2703 |
| 25%        |        -0.0439 |        -0.0440 |      -2.63e-08 |      -7.15e-10 |
| 50%        |         0.0510 |         0.0510 |         0.0000 |         0.0000 |
| 75%        |         0.1598 |         0.1598 |       2.63e-08 |       7.16e-10 |
| max        |     11615.4880 |     11615.4889 |         3.4648 |         0.0944 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,974,260

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.73e-05 |     1.33e-05 |     -2.8038 |     0.005 |
| Slope       |       1.0000 |     3.63e-07 |    2.76e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/2974260 (0.002%)
- Stata standard deviation: 3.67e+01

---

### Leverage_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Leverage_q']

**Observations**:
- Stata:  2,571,833
- Python: 2,571,841
- Common: 2,571,764

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.75e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.57e+06 |       2.57e+06 |       2.57e+06 |       2.57e+06 |
| mean       |         2.8298 |         2.8298 |       2.20e-06 |       1.18e-07 |
| std        |        18.6726 |        18.6726 |         0.0019 |       1.02e-04 |
| min        |       -11.0632 |       -11.0632 |        -0.2401 |        -0.0129 |
| 25%        |         0.2307 |         0.2307 |      -1.51e-08 |      -8.07e-10 |
| 50%        |         0.6768 |         0.6768 |         0.0000 |         0.0000 |
| 75%        |         2.0022 |         2.0022 |       1.50e-08 |       8.06e-10 |
| max        |      8843.3477 |      8843.3470 |         2.0802 |         0.1114 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,571,764

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.23e-06 |     1.20e-06 |      1.8573 |     0.063 |
| Slope       |       1.0000 |     6.35e-08 |    1.57e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 10/2571764 (0.000%)
- Stata standard deviation: 1.87e+01

---

### NetDebtPrice_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['NetDebtPrice_q']

**Observations**:
- Stata:  1,178,409
- Python: 1,220,286
- Common: 1,178,315

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.18e+06 |       1.18e+06 |       1.18e+06 |       1.18e+06 |
| mean       |         1.0139 |         1.0139 |       5.91e-06 |       8.59e-07 |
| std        |         6.8788 |         6.8788 |         0.0025 |       3.67e-04 |
| min        |      -142.3929 |      -142.3930 |        -0.0512 |        -0.0074 |
| 25%        |        -0.0768 |        -0.0768 |      -1.03e-08 |      -1.50e-09 |
| 50%        |         0.2984 |         0.2984 |      -1.10e-12 |      -1.59e-13 |
| 75%        |         0.9501 |         0.9501 |       1.03e-08 |       1.50e-09 |
| max        |      2492.7185 |      2492.7184 |         1.7826 |         0.2591 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,178,315

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.02e-06 |     2.35e-06 |      1.7118 |     0.087 |
| Slope       |       1.0000 |     3.38e-07 |    2.96e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 18/1178315 (0.002%)
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
- Python: 2,622,226
- Common: 2,520,036

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.91e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.52e+06 |       2.52e+06 |       2.52e+06 |       2.52e+06 |
| mean       |         0.0042 |         0.0042 |       5.19e-06 |       1.71e-05 |
| std        |         0.3030 |         0.3030 |         0.0022 |         0.0072 |
| min        |      -193.6226 |      -193.6226 |        -0.7671 |        -2.5316 |
| 25%        |      -1.53e-04 |      -1.53e-04 |      -7.90e-11 |      -2.61e-10 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0100 |         0.0100 |       8.07e-11 |       2.66e-10 |
| max        |       195.8306 |       195.8306 |         1.2332 |         4.0699 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,520,036

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     5.22e-06 |     1.38e-06 |      3.7921 |     0.000 |
| Slope       |       1.0000 |     4.54e-06 | 220049.6422 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1051/2520036 (0.042%)
- Stata standard deviation: 3.03e-01

---

### OPLeverage_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OPLeverage_q']

**Observations**:
- Stata:  2,546,734
- Python: 2,546,783
- Common: 2,546,640

**Precision1**: 0.034% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.08e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.55e+06 |       2.55e+06 |       2.55e+06 |       2.55e+06 |
| mean       |         0.2547 |         0.2547 |       4.07e-06 |       8.41e-06 |
| std        |         0.4836 |         0.4836 |         0.0064 |         0.0132 |
| min        |        -1.4798 |        -1.4798 |        -1.0265 |        -2.1227 |
| 25%        |         0.0824 |         0.0824 |      -3.42e-09 |      -7.07e-09 |
| 50%        |         0.1983 |         0.1983 |      -2.08e-12 |      -4.30e-12 |
| 75%        |         0.3378 |         0.3378 |       3.40e-09 |       7.04e-09 |
| max        |       280.5029 |       280.5029 |         3.8251 |         7.9099 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9998
- **N observations**: 2,546,640

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.00e-06 |     4.51e-06 |      0.4430 |     0.658 |
| Slope       |       1.0000 |     8.26e-06 | 121111.5726 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 862/2546640 (0.034%)
- Stata standard deviation: 4.84e-01

---

### OScore_q

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 5821 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OScore_q']

**Observations**:
- Stata:  877,922
- Python: 1,177,523
- Common: 872,101

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    872101.0000 |    872101.0000 |    872101.0000 |    872101.0000 |
| mean       |         0.1194 |         0.1194 |         0.0000 |         0.0000 |
| std        |         0.3243 |         0.3243 |         0.0000 |         0.0000 |
| min        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 872,101

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.44e-13 |     4.11e-16 |   -350.6194 |     0.000 |
| Slope       |       1.0000 |     1.19e-15 |    8.40e+14 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OScore_q
     0   10010  199501       1.0
     1   10012  199002       1.0
     2   10012  199207       1.0
     3   10012  199302       1.0
     4   10012  199303       1.0
     5   10015  198511       1.0
     6   10025  199601       1.0
     7   10025  199607       1.0
     8   10025  199608       1.0
     9   10028  199902       1.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/872101 (0.000%)
- Stata standard deviation: 3.24e-01

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
- Python: 1,826,388
- Common: 1,292,263

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.47e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.29e+06 |       1.29e+06 |       1.29e+06 |       1.29e+06 |
| mean       |         0.2732 |         0.2732 |      -1.02e-07 |      -1.45e-08 |
| std        |         6.9919 |         6.9919 |         0.0013 |       1.86e-04 |
| min        |     -1594.7000 |     -1594.7000 |        -0.3447 |        -0.0493 |
| 25%        |         0.1432 |         0.1432 |      -5.76e-09 |      -8.24e-10 |
| 50%        |         0.2805 |         0.2805 |       4.44e-16 |       6.35e-17 |
| 75%        |         0.4266 |         0.4266 |       5.79e-09 |       8.28e-10 |
| max        |      1096.4845 |      1096.4845 |         0.3904 |         0.0558 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,292,263

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.25e-08 |     1.15e-06 |     -0.0197 |     0.984 |
| Slope       |       1.0000 |     1.64e-07 |    6.11e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 60/1292263 (0.005%)
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
- Python: 2,407,559
- Common: 2,395,616

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.76e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |        -0.0081 |        -0.0074 |       6.60e-04 |       4.63e-05 |
| std        |        14.2568 |        14.2516 |         0.4277 |         0.0300 |
| min        |     -5783.8232 |     -5784.0000 |        -3.1995 |        -0.2244 |
| 25%        |        -0.0048 |        -0.0048 |      -6.84e-09 |      -4.80e-10 |
| 50%        |         0.0444 |         0.0444 |         0.0000 |         0.0000 |
| 75%        |         0.0849 |         0.0849 |       6.86e-09 |       4.81e-10 |
| max        |      8526.0000 |      8526.0000 |       340.7708 |        23.9023 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9992 * stata
- **R-squared**: 0.9991
- **N observations**: 2,395,616

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.53e-04 |     2.76e-04 |      2.3650 |     0.018 |
| Slope       |       0.9992 |     1.94e-05 |  51566.6837 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 173/2395616 (0.007%)
- Stata standard deviation: 1.43e+01

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
- Python: 2,855,231
- Common: 2,742,767

**Precision1**: 1.122% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.19e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.74e+06 |       2.74e+06 |       2.74e+06 |       2.74e+06 |
| mean       |         0.1294 |         0.1302 |       8.35e-04 |       7.03e-04 |
| std        |         1.1878 |         1.1878 |         0.0179 |         0.0151 |
| min        |      -200.7273 |      -200.7273 |        -1.6015 |        -1.3483 |
| 25%        |         0.0319 |         0.0323 |      -2.45e-09 |      -2.07e-09 |
| 50%        |         0.1281 |         0.1287 |       1.23e-10 |       1.03e-10 |
| 75%        |         0.2154 |         0.2162 |       3.48e-09 |       2.93e-09 |
| max        |       226.5365 |       226.5365 |         2.9988 |         2.5246 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0009 + 0.9999 * stata
- **R-squared**: 0.9998
- **N observations**: 2,742,767

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.51e-04 |     1.09e-05 |     78.1040 |     0.000 |
| Slope       |       0.9999 |     9.12e-06 | 109686.6719 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 30773/2742767 (1.122%)
- Stata standard deviation: 1.19e+00

---

### OperProfRDLagAT_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OperProfRDLagAT_q']

**Observations**:
- Stata:  1,800,025
- Python: 1,800,098
- Common: 1,799,857

**Precision1**: 0.051% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.79e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.80e+06 |       1.80e+06 |       1.80e+06 |       1.80e+06 |
| mean       |         0.0249 |         0.0249 |       4.74e-06 |       3.60e-05 |
| std        |         0.1317 |         0.1317 |         0.0031 |         0.0235 |
| min        |       -10.0000 |       -10.0000 |        -0.6451 |        -4.8975 |
| 25%        |         0.0110 |         0.0110 |      -7.25e-10 |      -5.50e-09 |
| 50%        |         0.0317 |         0.0317 |         0.0000 |         0.0000 |
| 75%        |         0.0522 |         0.0522 |       7.23e-10 |       5.49e-09 |
| max        |        54.3953 |        54.3953 |         1.8353 |        13.9346 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 0.9998 * stata
- **R-squared**: 0.9994
- **N observations**: 1,799,857

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.08e-05 |     2.35e-06 |      4.6091 |     0.000 |
| Slope       |       0.9998 |     1.75e-05 |  56976.7916 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 925/1799857 (0.051%)
- Stata standard deviation: 1.32e-01

---

### OrgCapNoAdj

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 25478 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['OrgCapNoAdj']

**Observations**:
- Stata:  1,243,418
- Python: 1,249,255
- Common: 1,217,940

**Precision1**: 0.022% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.02e-05 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.22e+06 |       1.22e+06 |       1.22e+06 |       1.22e+06 |
| mean       |         2.6133 |         2.6132 |      -7.88e-05 |      -8.68e-06 |
| std        |         9.0762 |         9.0761 |         0.0277 |         0.0030 |
| min        |        -5.4577 |        -5.4577 |       -17.0922 |        -1.8832 |
| 25%        |         0.7044 |         0.7043 |      -7.19e-08 |      -7.93e-09 |
| 50%        |         1.6586 |         1.6587 |      -1.31e-09 |      -1.44e-10 |
| 75%        |         3.3211 |         3.3211 |       5.06e-08 |       5.58e-09 |
| max        |      3861.9792 |      3861.9793 |         5.7057 |         0.6286 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,217,940

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -2.95e-05 |     2.61e-05 |     -1.1300 |     0.258 |
| Slope       |       1.0000 |     2.76e-06 | 361865.7815 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  OrgCapNoAdj
     0   10286  198806     1.863002
     1   10286  198807     1.844594
     2   10286  198808     1.844594
     3   10286  198809     1.844594
     4   10286  198810     1.822256
     5   10286  198811     1.822256
     6   10286  198812     1.822256
     7   10286  198901     1.805611
     8   10286  198902     1.805611
     9   10286  198903     1.805611
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 270/1217940 (0.022%)
- Stata standard deviation: 9.08e+00

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
- Python: 3,618,543
- Common: 3,547,773

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.35e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.55e+06 |       3.55e+06 |       3.55e+06 |       3.55e+06 |
| mean       |        -4.0283 |        -4.0283 |       1.20e-05 |       5.66e-08 |
| std        |       211.9918 |       211.9919 |         0.0059 |       2.79e-05 |
| min        |    -84221.6640 |    -84221.6667 |        -0.1893 |      -8.93e-04 |
| 25%        |        -0.0177 |        -0.0177 |      -1.41e-09 |      -6.64e-12 |
| 50%        |         0.0398 |         0.0398 |         0.0000 |         0.0000 |
| 75%        |         0.0957 |         0.0957 |       1.42e-09 |       6.69e-12 |
| max        |     10418.0800 |     10418.0800 |         3.1361 |         0.0148 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,547,773

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.21e-05 |     3.14e-06 |      3.8447 |     0.000 |
| Slope       |       1.0000 |     1.48e-08 |    6.75e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/3547773 (0.000%)
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
- Python: 2,492,118
- Common: 2,491,991

**Precision1**: 0.003% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.03e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.49e+06 |       2.49e+06 |       2.49e+06 |       2.49e+06 |
| mean       |        -3.9606 |        -3.9563 |         0.0042 |       2.48e-05 |
| std        |       171.1276 |       171.0159 |         6.6231 |         0.0387 |
| min        |    -64982.0000 |    -64982.0000 |     -1325.2500 |        -7.7442 |
| 25%        |        -0.0250 |        -0.0250 |      -1.28e-09 |      -7.51e-12 |
| 50%        |         0.0340 |         0.0340 |         0.0000 |         0.0000 |
| 75%        |         0.0816 |         0.0816 |       1.28e-09 |       7.46e-12 |
| max        |     18403.0000 |     18403.0000 |      5840.5208 |        34.1296 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0013 + 0.9986 * stata
- **R-squared**: 0.9985
- **N observations**: 2,491,991

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0013 |       0.0042 |     -0.3126 |     0.755 |
| Slope       |       0.9986 |     2.45e-05 |  40757.4861 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 63/2491991 (0.003%)
- Stata standard deviation: 1.71e+02

---

### PS_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['PS_q']

**Observations**:
- Stata:  310,650
- Python: 371,823
- Common: 310,650

**Precision1**: 0.042% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    310650.0000 |    310650.0000 |    310650.0000 |    310650.0000 |
| mean       |         5.2218 |         5.2216 |      -1.58e-04 |      -9.98e-05 |
| std        |         1.5810 |         1.5809 |         0.0243 |         0.0154 |
| min        |         1.0000 |         1.0000 |        -2.0000 |        -1.2650 |
| 25%        |         4.0000 |         4.0000 |         0.0000 |         0.0000 |
| 50%        |         5.0000 |         5.0000 |         0.0000 |         0.0000 |
| 75%        |         6.0000 |         6.0000 |         0.0000 |         0.0000 |
| max        |         9.0000 |         9.0000 |         2.0000 |         1.2650 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0007 + 0.9998 * stata
- **R-squared**: 0.9998
- **N observations**: 310,650

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.84e-04 |     1.50e-04 |      4.5504 |     0.000 |
| Slope       |       0.9998 |     2.75e-05 |  36303.0650 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 129/310650 (0.042%)
- Stata standard deviation: 1.58e+00

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
- Python: 2,903,425
- Common: 1,310,000

**Precision1**: 0.064% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.41e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.31e+06 |       1.31e+06 |       1.31e+06 |       1.31e+06 |
| mean       |         0.0309 |         0.0309 |       9.93e-06 |       2.89e-05 |
| std        |         0.3442 |         0.3442 |       9.33e-04 |         0.0027 |
| min        |       1.15e-17 |        -0.0152 |        -0.1056 |        -0.3067 |
| 25%        |         0.0045 |         0.0045 |      -2.96e-10 |      -8.60e-10 |
| 50%        |         0.0106 |         0.0106 |      -2.09e-13 |      -6.07e-13 |
| 75%        |         0.0230 |         0.0231 |       2.97e-10 |       8.63e-10 |
| max        |       217.7060 |       217.7060 |         0.3391 |         0.9851 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,310,000

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.86e-06 |     8.19e-07 |     12.0474 |     0.000 |
| Slope       |       1.0000 |     2.37e-06 | 422102.7711 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 839/1310000 (0.064%)
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
- Python: 3,038,238
- Common: 833,583

**Precision1**: 0.025% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.85e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    833583.0000 |    833583.0000 |    833583.0000 |    833583.0000 |
| mean       |         0.0298 |         0.0298 |      -7.54e-06 |      -4.55e-05 |
| std        |         0.1656 |         0.1656 |         0.0022 |         0.0133 |
| min        |        -1.5270 |        -1.5270 |        -1.2894 |        -7.7861 |
| 25%        |         0.0024 |         0.0024 |      -2.18e-10 |      -1.32e-09 |
| 50%        |         0.0105 |         0.0105 |         0.0000 |         0.0000 |
| 75%        |         0.0278 |         0.0278 |       2.15e-10 |       1.30e-09 |
| max        |        98.7289 |        98.7289 |         0.2419 |         1.4604 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 0.9998 * stata
- **R-squared**: 0.9998
- **N observations**: 833,583

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.04e-06 |     2.45e-06 |     -0.4244 |     0.671 |
| Slope       |       0.9998 |     1.46e-05 |  68560.8697 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 206/833583 (0.025%)
- Stata standard deviation: 1.66e-01

---

### ResidualMomentum6m

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ResidualMomentum6m']

**Observations**:
- Stata:  3,601,405
- Python: 3,601,799
- Common: 3,601,405

**Precision1**: 0.926% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.58e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.60e+06 |       3.60e+06 |       3.60e+06 |       3.60e+06 |
| mean       |        -0.0597 |        -0.0597 |       5.99e-05 |       1.17e-04 |
| std        |         0.5125 |         0.5125 |         0.0014 |         0.0027 |
| min        |       -12.3925 |       -12.3887 |        -0.2201 |        -0.4294 |
| 25%        |        -0.3366 |        -0.3366 |      -3.16e-08 |      -6.17e-08 |
| 50%        |        -0.0296 |        -0.0296 |      -2.64e-09 |      -5.14e-09 |
| 75%        |         0.2494 |         0.2495 |       1.76e-08 |       3.43e-08 |
| max        |        35.4630 |        35.4663 |         0.2783 |         0.5429 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,601,405

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.02e-05 |     7.28e-07 |     82.7564 |     0.000 |
| Slope       |       1.0000 |     1.41e-06 | 708806.2205 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33366/3601405 (0.926%)
- Stata standard deviation: 5.13e-01

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
- Python: 3,014,016
- Common: 2,892,942

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.48e-19 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.89e+06 |       2.89e+06 |       2.89e+06 |       2.89e+06 |
| mean       |       2.31e+11 |            inf |            inf |            inf |
| std        |       1.27e+14 |            N/A |            N/A |            N/A |
| min        |      -5.90e+15 |      -5.90e+15 |      -1.75e+09 |      -1.37e-05 |
| 25%        |        -0.0320 |        -0.0320 |      -6.74e-09 |      -5.29e-23 |
| 50%        |         0.1203 |         0.1203 |      -1.33e-12 |      -1.04e-26 |
| 75%        |         0.2648 |         0.2648 |       6.73e-09 |       5.29e-23 |
| max        |       6.23e+16 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 2179695700.9759 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,892,930

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.18e+09 |     6.29e+08 |      3.4641 |     0.001 |
| Slope       |       1.0000 |     4.94e-06 | 202432.8852 |     0.000 |

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
- Python: 2,692,958
- Common: 2,413,578

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.34e-11 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |       -46.8887 |            N/A |            N/A |            N/A |
| std        |     46097.2375 |            N/A |            N/A |            N/A |
| min        |      -4.12e+07 |           -inf |           -inf |           -inf |
| 25%        |      -9.84e-04 |      -9.81e-04 |      -1.55e-09 |      -3.37e-14 |
| 50%        |         0.0288 |         0.0288 |      -4.06e-13 |      -8.81e-18 |
| 75%        |         0.0609 |         0.0609 |       1.54e-09 |       3.34e-14 |
| max        |       3.43e+06 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 1401890785.8418 + -266360970.0095 * stata
- **R-squared**: 0.9913
- **N observations**: 2,413,559

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.40e+09 |     7.40e+08 |      1.8942 |     0.058 |
| Slope       |    -2.66e+08 |   16055.3403 | -16590.1791 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 25/2413578 (0.001%)
- Stata standard deviation: 4.61e+04

---

### ReturnSkewCAPM

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 37254 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['ReturnSkewCAPM']

**Observations**:
- Stata:  4,997,359
- Python: 4,988,237
- Common: 4,960,105

**Precision1**: 0.808% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.97e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       4.96e+06 |       4.95e+06 |       4.95e+06 |       4.95e+06 |
| mean       |         0.1846 |         0.1846 |      -2.52e-04 |      -2.64e-04 |
| std        |         0.9536 |         0.9517 |         0.0706 |         0.0740 |
| min        |        -4.9022 |        -4.9022 |        -8.0139 |        -8.4041 |
| 25%        |        -0.2801 |        -0.2799 |      -2.62e-04 |      -2.75e-04 |
| 50%        |         0.1553 |         0.1556 |         0.0000 |         0.0000 |
| 75%        |         0.6325 |         0.6326 |       2.33e-04 |       2.44e-04 |
| max        |         4.8256 |         4.8258 |         7.7611 |         8.1391 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9982 * stata
- **R-squared**: 0.9945
- **N observations**: 4,953,435

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     7.84e-05 |     3.23e-05 |      2.4269 |     0.015 |
| Slope       |       0.9982 |     3.33e-05 |  29948.1483 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  ReturnSkewCAPM
     0   10001  201708        0.532855
     1   10002  201302        0.980123
     2   10003  198601        0.194168
     3   10003  199512        0.707874
     4   10005  198601       -1.702117
     5   10005  199107        2.265614
     6   10007  198601       -0.336022
     7   10007  199010       -1.647068
     8   10008  198601        0.808999
     9   10009  198601        1.587751
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 40095/4960105 (0.808%)
- Stata standard deviation: 9.54e-01

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

**Precision1**: 0.892% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.16e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.95e+06 |       3.94e+06 |       3.94e+06 |       3.94e+06 |
| mean       |         0.1399 |         0.1401 |      -2.54e-04 |      -3.07e-04 |
| std        |         0.8265 |         0.8321 |         0.1179 |         0.1426 |
| min        |        -4.4416 |        -4.4416 |        -6.1208 |        -7.4054 |
| 25%        |        -0.2864 |        -0.2870 |      -1.92e-08 |      -2.33e-08 |
| 50%        |         0.1203 |         0.1203 |       1.76e-10 |       2.13e-10 |
| 75%        |         0.5534 |         0.5541 |       1.97e-08 |       2.38e-08 |
| max        |         4.4416 |         4.4772 |         6.0899 |         7.3679 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0003 + 0.9962 * stata
- **R-squared**: 0.9799
- **N observations**: 3,943,726

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     2.81e-04 |     6.02e-05 |      4.6702 |     0.000 |
| Slope       |       0.9962 |     7.18e-05 |  13883.1483 |     0.000 |

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
- Num observations with std_diff >= TOL_DIFF_1: 35283/3954491 (0.892%)
- Stata standard deviation: 8.27e-01

---

### SP_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['SP_q']

**Observations**:
- Stata:  2,790,383
- Python: 2,790,452
- Common: 2,790,334

**Precision1**: 0.017% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.09e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.79e+06 |       2.79e+06 |       2.79e+06 |       2.79e+06 |
| mean       |         0.6076 |         0.6076 |      -2.39e-05 |      -1.32e-05 |
| std        |         1.8101 |         1.8101 |         0.0077 |         0.0043 |
| min        |       -31.7352 |       -31.7352 |        -4.6447 |        -2.5660 |
| 25%        |         0.1051 |         0.1051 |      -5.82e-09 |      -3.22e-09 |
| 50%        |         0.2523 |         0.2523 |         0.0000 |         0.0000 |
| 75%        |         0.5972 |         0.5972 |       5.80e-09 |       3.20e-09 |
| max        |       537.3825 |       537.3825 |         2.4458 |         1.3512 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,790,334

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.51e-05 |     4.86e-06 |     -3.1082 |     0.002 |
| Slope       |       1.0000 |     2.55e-06 | 392629.7881 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 479/2790334 (0.017%)
- Stata standard deviation: 1.81e+00

---

### Tax_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['Tax_q']

**Observations**:
- Stata:  1,906,647
- Python: 1,906,682
- Common: 1,906,581

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.65e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.91e+06 |       1.91e+06 |       1.91e+06 |       1.91e+06 |
| mean       |         1.7501 |         1.7502 |       1.10e-04 |       6.78e-06 |
| std        |        16.1405 |        16.1418 |         0.0886 |         0.0055 |
| min        |       2.00e-06 |       2.00e-06 |       -11.3264 |        -0.7017 |
| 25%        |         1.2937 |         1.2936 |      -3.00e-08 |      -1.86e-09 |
| 50%        |         1.5463 |         1.5463 |         0.0000 |         0.0000 |
| 75%        |         1.7239 |         1.7239 |       3.03e-08 |       1.87e-09 |
| max        |     10630.3370 |     10630.3365 |        69.8003 |         4.3245 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0001 * stata
- **R-squared**: 1.0000
- **N observations**: 1,906,581

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.34e-06 |     6.45e-05 |     -0.1447 |     0.885 |
| Slope       |       1.0001 |     3.98e-06 | 251546.0040 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 101/1906581 (0.005%)
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
- Python: 3,247,820
- Common: 2,702,805

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.20e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.70e+06 |       2.70e+06 |       2.70e+06 |
| mean       |        -0.1112 |        -0.1111 |       1.11e-05 |       2.02e-07 |
| std        |        54.8159 |        54.8159 |         0.0052 |       9.44e-05 |
| min        |      -111.6833 |      -111.6833 |        -2.7503 |        -0.0502 |
| 25%        |        -0.3470 |        -0.3470 |      -5.02e-09 |      -9.17e-11 |
| 50%        |        -0.2572 |        -0.2571 |       2.66e-11 |       4.85e-13 |
| 75%        |        -0.1745 |        -0.1745 |       5.09e-09 |       9.29e-11 |
| max        |     76241.1800 |     76241.1777 |         3.7323 |         0.0681 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,702,805

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.11e-05 |     3.15e-06 |      3.5220 |     0.000 |
| Slope       |       1.0000 |     5.74e-08 |    1.74e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 29/2702805 (0.001%)
- Stata standard deviation: 5.48e+01

---

### WW_Q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['WW_Q']

**Observations**:
- Stata:  2,406,602
- Python: 2,440,908
- Common: 2,406,519

**Precision1**: 0.002% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.51e-06 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.41e+06 |       2.41e+06 |       2.41e+06 |       2.41e+06 |
| mean       |        -0.0942 |           -inf |           -inf |           -inf |
| std        |        80.9107 |            N/A |            N/A |            N/A |
| min        |     -1099.2520 |           -inf |           -inf |           -inf |
| 25%        |        -0.3578 |        -0.3578 |      -6.09e-09 |      -7.52e-11 |
| 50%        |        -0.2663 |        -0.2663 |      -4.39e-11 |      -5.42e-13 |
| 75%        |        -0.1791 |        -0.1791 |       5.97e-09 |       7.38e-11 |
| max        |     75674.3520 |     75674.3568 |        15.5945 |         0.1927 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,406,509

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.56e-05 |     1.34e-05 |      2.6509 |     0.008 |
| Slope       |       1.0000 |     1.66e-07 |    6.02e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 38/2406519 (0.002%)
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
- Python: 1,669,132
- Common: 1,668,108

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.63e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.67e+06 |       1.67e+06 |       1.67e+06 |       1.67e+06 |
| mean       |         5.9429 |         5.9429 |       7.95e-07 |       2.34e-08 |
| std        |        33.9604 |        33.9604 |         0.0011 |       3.27e-05 |
| min        |      -353.7195 |      -353.7195 |        -0.1188 |        -0.0035 |
| 25%        |         2.1718 |         2.1718 |      -7.65e-08 |      -2.25e-09 |
| 50%        |         3.4992 |         3.4992 |       2.97e-11 |       8.75e-13 |
| 75%        |         5.4589 |         5.4589 |       7.67e-08 |       2.26e-09 |
| max        |      8802.6084 |      8802.6085 |         1.3375 |         0.0394 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,668,108

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     9.25e-07 |     8.72e-07 |      1.0601 |     0.289 |
| Slope       |       1.0000 |     2.53e-08 |    3.95e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1/1668108 (0.000%)
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
- Python: 1,490,445
- Common: 1,214,174

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.01e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         4.2873 |         4.2873 |      -5.23e-06 |      -1.52e-07 |
| std        |        34.3037 |        34.3037 |         0.0108 |       3.15e-04 |
| min        |     -9318.5010 |     -9318.5014 |        -3.3394 |        -0.0973 |
| 25%        |         1.1057 |         1.1057 |      -4.80e-08 |      -1.40e-09 |
| 50%        |         1.9844 |         1.9844 |       3.66e-11 |       1.07e-12 |
| 75%        |         3.4886 |         3.4886 |       4.82e-08 |       1.40e-09 |
| max        |      9482.0879 |      9482.0882 |         2.9884 |         0.0871 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,214,174

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -5.32e-06 |     9.87e-06 |     -0.5390 |     0.590 |
| Slope       |       1.0000 |     2.85e-07 |    3.50e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 72/1214174 (0.006%)
- Stata standard deviation: 3.43e+01

---

### betaCC

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaCC']

**Observations**:
- Stata:  3,459,006
- Python: 3,544,098
- Common: 3,459,006

**Precision1**: 1.852% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.48e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |        10.0114 |        10.0121 |       7.07e-04 |       3.17e-05 |
| std        |        22.2834 |        22.2860 |         0.0854 |         0.0038 |
| min        |      -349.5267 |      -349.8631 |        -5.1346 |        -0.2304 |
| 25%        |         0.0634 |         0.0634 |        -0.0031 |      -1.40e-04 |
| 50%        |         1.1260 |         1.1257 |       8.63e-06 |       3.87e-07 |
| 75%        |        15.1275 |        15.1291 |         0.0028 |       1.25e-04 |
| max        |       389.6191 |       389.5582 |         4.6776 |         0.2099 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0004 + 1.0001 * stata
- **R-squared**: 1.0000
- **N observations**: 3,459,006

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.93e-04 |     5.03e-05 |     -7.8066 |     0.000 |
| Slope       |       1.0001 |     2.06e-06 | 485659.3371 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 64065/3459006 (1.852%)
- Stata standard deviation: 2.23e+01

---

### betaCR

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaCR']

**Observations**:
- Stata:  3,459,006
- Python: 3,543,453
- Common: 3,459,006

**Precision1**: 0.152% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 5.65e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |        -8.6710 |        -8.6767 |        -0.0057 |      -1.90e-04 |
| std        |        30.1087 |        30.1169 |         0.0358 |         0.0012 |
| min        |      -453.6021 |      -453.6194 |        -1.9380 |        -0.0644 |
| 25%        |        -7.9603 |        -7.9666 |        -0.0027 |      -9.09e-05 |
| 50%        |        -0.6032 |        -0.6036 |      -8.86e-05 |      -2.94e-06 |
| 75%        |        -0.0065 |        -0.0065 |       4.05e-04 |       1.34e-05 |
| max        |       498.2335 |       498.0308 |         1.7332 |         0.0576 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0034 + 1.0003 * stata
- **R-squared**: 1.0000
- **N observations**: 3,459,006

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0034 |     1.95e-05 |   -172.1096 |     0.000 |
| Slope       |       1.0003 |     6.22e-07 |    1.61e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 5257/3459006 (0.152%)
- Stata standard deviation: 3.01e+01

---

### betaNet

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaNet']

**Observations**:
- Stata:  3,420,591
- Python: 3,460,090
- Common: 3,420,591

**Precision1**: 0.717% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.37e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |        19.0357 |        19.0422 |         0.0065 |       1.48e-04 |
| std        |        43.5530 |        43.5614 |         0.0952 |         0.0022 |
| min        |      -566.6315 |      -566.6579 |        -5.4861 |        -0.1260 |
| 25%        |         0.7646 |         0.7649 |        -0.0022 |      -5.13e-05 |
| 50%        |         2.8178 |         2.8187 |       2.41e-04 |       5.52e-06 |
| 75%        |        23.5852 |        23.5843 |         0.0057 |       1.30e-04 |
| max        |       620.3024 |       623.0691 |         6.0689 |         0.1393 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0028 + 1.0002 * stata
- **R-squared**: 1.0000
- **N observations**: 3,420,591

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0028 |     5.60e-05 |     50.6543 |     0.000 |
| Slope       |       1.0002 |     1.18e-06 | 849254.4350 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24541/3420591 (0.717%)
- Stata standard deviation: 4.36e+01

---

### betaRC

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaRC']

**Observations**:
- Stata:  3,421,560
- Python: 3,461,692
- Common: 3,421,560

**Precision1**: 2.452% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.61e-02 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |        -0.1585 |        -0.1584 |       5.20e-05 |       2.50e-04 |
| std        |         0.2080 |         0.2080 |       8.67e-04 |         0.0042 |
| min        |        -8.9074 |        -8.8976 |        -0.0440 |        -0.2114 |
| 25%        |        -0.2516 |        -0.2516 |      -1.11e-04 |      -5.32e-04 |
| 50%        |        -0.1403 |        -0.1402 |       1.58e-05 |       7.61e-05 |
| 75%        |        -0.0465 |        -0.0464 |       1.74e-04 |       8.37e-04 |
| max        |         6.1166 |         6.1123 |         0.0656 |         0.3156 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,421,560

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.93e-05 |     5.89e-07 |     83.6612 |     0.000 |
| Slope       |       1.0000 |     2.25e-06 | 443907.5384 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 83897/3421560 (2.452%)
- Stata standard deviation: 2.08e-01

---

### betaRR

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['betaRR']

**Observations**:
- Stata:  3,421,560
- Python: 3,461,064
- Common: 3,421,560

**Precision1**: 0.473% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 7.33e-03 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.42e+06 |       3.42e+06 |       3.42e+06 |       3.42e+06 |
| mean       |         0.4870 |         0.4872 |       2.55e-04 |       5.81e-04 |
| std        |         0.4391 |         0.4393 |       7.33e-04 |         0.0017 |
| min        |        -9.0881 |        -9.0880 |        -0.0159 |        -0.0363 |
| 25%        |         0.2195 |         0.2196 |      -6.03e-06 |      -1.37e-05 |
| 50%        |         0.4000 |         0.4002 |       4.35e-05 |       9.91e-05 |
| 75%        |         0.6594 |         0.6597 |       2.15e-04 |       4.89e-04 |
| max        |        14.4013 |        14.4004 |         0.0395 |         0.0901 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0004 * stata
- **R-squared**: 1.0000
- **N observations**: 3,421,560

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.41e-05 |     5.72e-07 |     77.0843 |     0.000 |
| Slope       |       1.0004 |     8.72e-07 |    1.15e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 16185/3421560 (0.473%)
- Stata standard deviation: 4.39e-01

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
- Python: 3,286,185
- Common: 3,267,782

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.24e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.27e+06 |       3.27e+06 |       3.27e+06 |       3.27e+06 |
| mean       |         0.3051 |         0.3051 |       8.64e-07 |       1.88e-08 |
| std        |        45.8671 |        45.8671 |         0.0011 |       2.45e-05 |
| min        |    -10248.0000 |    -10248.0000 |        -0.3728 |        -0.0081 |
| 25%        |         0.0096 |         0.0096 |      -3.26e-09 |      -7.11e-11 |
| 50%        |         0.1142 |         0.1142 |         0.0000 |         0.0000 |
| 75%        |         0.2625 |         0.2625 |       3.26e-09 |       7.11e-11 |
| max        |     13971.0000 |     13971.0000 |         0.2960 |         0.0065 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,267,782

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.61e-07 |     6.21e-07 |      1.3871 |     0.165 |
| Slope       |       1.0000 |     1.35e-08 |    7.39e+07 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 0/3267782 (0.000%)
- Stata standard deviation: 4.59e+01

---

### cfpq

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['cfpq']

**Observations**:
- Stata:  2,252,622
- Python: 2,430,653
- Common: 2,252,621

**Precision1**: 0.432% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.01e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.25e+06 |       2.25e+06 |       2.25e+06 |       2.25e+06 |
| mean       |       2.37e-04 |       8.75e-04 |       6.38e-04 |       8.89e-04 |
| std        |         0.7177 |         0.7129 |         0.1161 |         0.1618 |
| min        |      -306.2332 |      -306.2333 |       -20.5189 |       -28.5906 |
| 25%        |        -0.0228 |        -0.0225 |      -9.36e-10 |      -1.30e-09 |
| 50%        |         0.0110 |         0.0111 |       4.86e-13 |       6.78e-13 |
| 75%        |         0.0389 |         0.0389 |       9.50e-10 |       1.32e-09 |
| max        |       250.7536 |       250.7536 |        66.0967 |        92.0978 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0006 + 0.9803 * stata
- **R-squared**: 0.9739
- **N observations**: 2,252,621

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     6.43e-04 |     7.68e-05 |      8.3732 |     0.000 |
| Slope       |       0.9803 |     1.07e-04 |   9163.8064 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 9737/2252621 (0.432%)
- Stata standard deviation: 7.18e-01

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
- Python: 3,070,726
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.40e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         3.3803 |         3.3803 |      -1.59e-06 |      -2.81e-08 |
| std        |        56.6989 |        56.6989 |       9.92e-04 |       1.75e-05 |
| min        |         0.0000 |         0.0000 |        -0.4978 |        -0.0088 |
| 25%        |         1.2859 |         1.2859 |      -5.02e-08 |      -8.85e-10 |
| 50%        |         2.0125 |         2.0125 |         0.0000 |         0.0000 |
| 75%        |         3.1813 |         3.1813 |       5.05e-08 |       8.91e-10 |
| max        |     25204.0000 |     25204.0000 |         0.0579 |         0.0010 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.59e-06 |     5.68e-07 |     -2.8076 |     0.005 |
| Slope       |       1.0000 |     1.00e-08 |    1.00e+08 |     0.000 |

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
- Python: 3,526,532
- Common: 3,462,713

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.77e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.46e+06 |       3.46e+06 |       3.46e+06 |       3.46e+06 |
| mean       |         0.4261 |         0.4261 |      -1.05e-05 |      -1.17e-06 |
| std        |         8.9356 |         8.9356 |         0.0037 |       4.12e-04 |
| min        |        -2.3523 |        -2.3523 |        -1.4752 |        -0.1651 |
| 25%        |         0.0910 |         0.0910 |      -3.06e-09 |      -3.43e-10 |
| 50%        |         0.1480 |         0.1480 |         0.0000 |         0.0000 |
| 75%        |         0.2717 |         0.2717 |       2.97e-09 |       3.32e-10 |
| max        |      2457.7500 |      2457.7500 |         0.2782 |         0.0311 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,462,713

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.04e-05 |     1.98e-06 |     -5.2527 |     0.000 |
| Slope       |       1.0000 |     2.22e-07 |    4.51e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 132/3462713 (0.004%)
- Stata standard deviation: 8.94e+00

---

### fgr5yrNoLag

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 4917 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['fgr5yrNoLag']

**Observations**:
- Stata:  996,237
- Python: 998,737
- Common: 991,320

**Precision1**: 0.077% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.43e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    991320.0000 |    991320.0000 |    991320.0000 |    991320.0000 |
| mean       |        16.8629 |        16.8626 |      -3.11e-04 |      -2.22e-05 |
| std        |        14.0065 |        14.0065 |         0.1603 |         0.0114 |
| min        |      -899.2000 |      -899.2000 |       -87.7100 |        -6.2621 |
| 25%        |        10.5000 |        10.5000 |         0.0000 |         0.0000 |
| 50%        |        15.0000 |        15.0000 |         0.0000 |         0.0000 |
| 75%        |        20.0000 |        20.0000 |         0.0000 |         0.0000 |
| max        |      2097.8000 |      2097.8000 |        28.2200 |         2.0148 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0008 + 0.9999 * stata
- **R-squared**: 0.9999
- **N observations**: 991,320

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.33e-04 |     2.52e-04 |      3.3074 |     0.001 |
| Slope       |       0.9999 |     1.15e-05 |  87005.4295 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  fgr5yrNoLag
     0   10012  200108        30.00
     1   10012  200109        30.00
     2   10104  202412        12.01
     3   10107  202412        13.95
     4   10137  199709         3.64
     5   10138  200012        15.36
     6   10138  202412         8.10
     7   10145  198403        10.30
     8   10145  198404        10.30
     9   10145  198405        10.00
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 768/991320 (0.077%)
- Stata standard deviation: 1.40e+01

---

### grcapx1y

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 26438 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['grcapx1y']

**Observations**:
- Stata:  2,427,138
- Python: 2,440,811
- Common: 2,400,700

**Precision1**: 0.010% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.40e+06 |       2.40e+06 |       2.40e+06 |       2.40e+06 |
| mean       |         1.7653 |            inf |            inf |            inf |
| std        |       183.8807 |            N/A |            N/A |            N/A |
| min        |     -4687.0000 |     -4687.0000 |      -405.1343 |        -2.2032 |
| 25%        |        -0.2932 |        -0.2932 |      -6.90e-09 |      -3.75e-11 |
| 50%        |         0.0705 |         0.0705 |         0.0000 |         0.0000 |
| 75%        |         0.5721 |         0.5721 |       6.90e-09 |       3.75e-11 |
| max        |     91212.0000 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,400,680

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.07e-04 |     2.70e-04 |      0.3975 |     0.691 |
| Slope       |       1.0000 |     1.47e-06 | 681954.5600 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  grcapx1y
     0   10001  200812  0.047433
     1   10001  200901  0.047433
     2   10001  200902  0.047433
     3   10001  200903  0.047433
     4   10001  200904  0.047433
     5   10001  200905  0.047433
     6   10002  199706 19.634615
     7   10002  199707 19.634615
     8   10002  199708 19.634615
     9   10002  199709 19.634615
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 244/2400700 (0.010%)
- Stata standard deviation: 1.84e+02

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

**Precision1**: 1.246% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.98e-01 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.70e+06 |       2.69e+06 |       2.69e+06 |       2.69e+06 |
| mean       |         5.1509 |         5.1533 |         0.0042 |       6.29e-04 |
| std        |         6.7163 |         6.7181 |         1.0988 |         0.1636 |
| min        |         0.0000 |         0.0000 |       -62.0000 |        -9.2312 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         3.0000 |         3.0000 |         0.0000 |         0.0000 |
| 75%        |         7.0000 |         7.0000 |         0.0000 |         0.0000 |
| max        |        62.0000 |        59.0000 |        35.0000 |         5.2112 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0734 + 0.9866 * stata
- **R-squared**: 0.9734
- **N observations**: 2,689,688

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0734 |     8.41e-04 |     87.2427 |     0.000 |
| Slope       |       0.9866 |     9.94e-05 |   9926.3522 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 33637/2700302 (1.246%)
- Stata standard deviation: 6.72e+00

---

### pchcurrat

**Status**: ❌ FAILED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ❌ FAILED (Python missing 36014 Stata observations)
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['pchcurrat']

**Observations**:
- Stata:  3,624,363
- Python: 3,590,809
- Common: 3,588,349

**Precision1**: 0.049% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 9.73e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.59e+06 |       3.59e+06 |       3.59e+06 |       3.59e+06 |
| mean       |         0.1897 |            inf |            inf |            inf |
| std        |        20.5071 |            N/A |            N/A |            N/A |
| min        |        -1.0000 |        -1.0000 |        -0.1094 |        -0.0053 |
| 25%        |        -0.1217 |        -0.1217 |      -2.16e-08 |      -1.05e-09 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.0809 |         0.0814 |       2.16e-08 |       1.05e-09 |
| max        |      8289.6123 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,586,591

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     1.46e-07 |     1.37e-07 |      1.0666 |     0.286 |
| Slope       |       1.0000 |     6.68e-09 |    1.50e+08 |     0.000 |

**Missing Observations Sample**:
```
 index  permno  yyyymm  pchcurrat
     0   10055  198910        0.0
     1   10055  198911        0.0
     2   10055  198912        0.0
     3   10055  199001        0.0
     4   10055  199002        0.0
     5   10055  199003        0.0
     6   10055  199004        0.0
     7   10055  199005        0.0
     8   10055  199006        0.0
     9   10055  199007        0.0
```

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 1758/3588349 (0.049%)
- Stata standard deviation: 2.05e+01

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
- Python: 3,270,004
- Common: 3,050,498

**Precision1**: 0.005% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.34e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.05e+06 |       3.05e+06 |       3.05e+06 |       3.05e+06 |
| mean       |         0.4972 |         0.4971 |      -9.16e-05 |      -2.37e-06 |
| std        |        38.5912 |        38.5913 |         0.0378 |       9.78e-04 |
| min        |       -75.5903 |       -75.5903 |       -18.3420 |        -0.4753 |
| 25%        |        -0.0906 |        -0.0906 |      -2.22e-09 |      -5.75e-11 |
| 50%        |         0.0251 |         0.0251 |         0.0000 |         0.0000 |
| 75%        |         0.1646 |         0.1646 |       2.22e-09 |       5.76e-11 |
| max        |     15513.7030 |     15513.7034 |         1.3903 |         0.0360 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0001 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,050,486

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.11e-05 |     2.16e-05 |     -4.2145 |     0.000 |
| Slope       |       1.0000 |     5.60e-07 |    1.79e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3050498 (0.005%)
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
- Python: 3,232,774
- Common: 3,222,544

**Precision1**: 0.004% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.76e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.22e+06 |       3.22e+06 |       3.22e+06 |       3.22e+06 |
| mean       |        -0.7243 |        -0.7244 |      -4.55e-05 |      -5.78e-07 |
| std        |        78.7275 |        78.7275 |         0.0451 |       5.73e-04 |
| min        |    -27624.8850 |    -27624.8841 |       -13.5667 |        -0.1723 |
| 25%        |        -0.0812 |        -0.0812 |      -1.28e-09 |      -1.62e-11 |
| 50%        |        -0.0029 |        -0.0029 |         0.0000 |         0.0000 |
| 75%        |         0.0636 |         0.0636 |       1.29e-09 |       1.63e-11 |
| max        |      5139.5205 |      5139.5206 |         7.1747 |         0.0911 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,222,544

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -4.56e-05 |     2.51e-05 |     -1.8137 |     0.070 |
| Slope       |       1.0000 |     3.19e-07 |    3.13e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 144/3222544 (0.004%)
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
- Python: 3,657,525
- Common: 3,339,639

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.96e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.34e+06 |       3.34e+06 |       3.34e+06 |       3.34e+06 |
| mean       |         0.2975 |         0.2975 |      -1.56e-08 |      -3.63e-10 |
| std        |        42.9356 |        42.9356 |       2.76e-04 |       6.42e-06 |
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
| Intercept   |    -1.62e-08 |     1.51e-07 |     -0.1077 |     0.914 |
| Slope       |       1.0000 |     3.51e-09 |    2.85e+08 |     0.000 |

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
- Python: 2,466,706
- Common: 2,465,425

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.47e+06 |       2.47e+06 |       2.47e+06 |       2.47e+06 |
| mean       |         0.7658 |         0.7199 |        -0.0459 |      -6.25e-04 |
| std        |        73.4020 |        70.3930 |        20.8029 |         0.2834 |
| min        |     -3126.2041 |     -3126.2041 |     -9429.3242 |      -128.4613 |
| 25%        |        -0.1224 |        -0.1224 |      -2.63e-09 |      -3.59e-11 |
| 50%        |         0.0114 |         0.0114 |       1.63e-12 |       2.23e-14 |
| 75%        |         0.1759 |         0.1759 |       2.67e-09 |       3.63e-11 |
| max        |     28764.0310 |     28764.0303 |         0.0597 |       8.13e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0156 + 0.9197 * stata
- **R-squared**: 0.9197
- **N observations**: 2,465,425

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0156 |       0.0127 |      1.2284 |     0.219 |
| Slope       |       0.9197 |     1.73e-04 |   5313.0942 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 12/2465425 (0.000%)
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
- Python: 3,359,810
- Common: 3,065,278

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.06e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.07e+06 |       3.07e+06 |       3.07e+06 |       3.07e+06 |
| mean       |         2.7309 |         2.7309 |      -1.82e-06 |      -3.21e-08 |
| std        |        56.6440 |        56.6440 |       9.57e-04 |       1.69e-05 |
| min        |       -41.2750 |       -41.2750 |        -0.4710 |        -0.0083 |
| 25%        |         0.8507 |         0.8507 |      -2.56e-08 |      -4.52e-10 |
| 50%        |         1.3264 |         1.3264 |         0.0000 |         0.0000 |
| 75%        |         2.2630 |         2.2630 |       2.57e-08 |       4.54e-10 |
| max        |     25204.0000 |     25204.0000 |         0.0579 |         0.0010 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,065,278

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.82e-06 |     5.47e-07 |     -3.3277 |     0.001 |
| Slope       |       1.0000 |     9.65e-09 |    1.04e+08 |     0.000 |

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
- Python: 1,253,272
- Common: 1,207,848

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 4.09e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.21e+06 |       1.21e+06 |       1.21e+06 |       1.21e+06 |
| mean       |         5.1262 |         5.1262 |      -9.27e-07 |      -4.96e-09 |
| std        |       186.9904 |       186.9904 |       4.62e-04 |       2.47e-06 |
| min        |     -1037.3235 |     -1037.3235 |        -0.1280 |      -6.85e-04 |
| 25%        |         0.0151 |         0.0151 |      -8.68e-10 |      -4.64e-12 |
| 50%        |         0.0509 |         0.0509 |      -2.78e-17 |      -1.48e-19 |
| 75%        |         0.1546 |         0.1546 |       8.73e-10 |       4.67e-12 |
| max        |     42070.6680 |     42070.6667 |         0.0533 |       2.85e-04 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 1,207,848

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -8.57e-07 |     4.21e-07 |     -2.0368 |     0.042 |
| Slope       |       1.0000 |     2.25e-09 |    4.45e+08 |     0.000 |

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
- Python: 783,507
- Common: 566,115

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.67e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |    566115.0000 |    566115.0000 |    566115.0000 |    566115.0000 |
| mean       |         7.6746 |         7.6747 |       1.35e-04 |       7.37e-07 |
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
| Intercept   |     1.34e-04 |     1.40e-04 |      0.9582 |     0.338 |
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
- Python: 2,069,582
- Common: 2,039,879

**Precision1**: 0.045% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.55e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.04e+06 |       2.04e+06 |       2.04e+06 |       2.04e+06 |
| mean       |         0.0305 |         0.0305 |       4.17e-06 |       2.73e-05 |
| std        |         0.1527 |         0.1527 |         0.0016 |         0.0105 |
| min        |       3.49e-05 |       3.49e-05 |        -0.0591 |        -0.3872 |
| 25%        |         0.0056 |         0.0056 |      -1.35e-10 |      -8.83e-10 |
| 50%        |         0.0124 |         0.0124 |       2.32e-13 |       1.52e-12 |
| 75%        |         0.0295 |         0.0295 |       1.35e-10 |       8.85e-10 |
| max        |        49.8304 |        49.8304 |         0.5649 |         3.6999 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9999
- **N observations**: 2,039,771

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     3.47e-06 |     1.14e-06 |      3.0326 |     0.002 |
| Slope       |       1.0000 |     7.35e-06 | 136062.0037 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 908/2039879 (0.045%)
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
- Python: 3,412,476
- Common: 3,409,380

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.65e-23 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.41e+06 |       3.41e+06 |       3.41e+06 |       3.41e+06 |
| mean       |       1.87e+13 |            inf |            inf |            inf |
| std        |       5.82e+15 |            N/A |            N/A |            N/A |
| min        |      -3.62e+17 |      -3.91e+16 |      -3.40e+16 |        -5.8459 |
| 25%        |        -0.0121 |        -0.0121 |      -1.88e-09 |      -3.23e-25 |
| 50%        |         0.0586 |         0.0586 |         0.0000 |         0.0000 |
| 75%        |         0.1262 |         0.1262 |       1.86e-09 |       3.20e-25 |
| max        |       1.79e+18 |            inf |            inf |            inf |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -33727704718.7420 + 0.6169 * stata
- **R-squared**: 0.9735
- **N observations**: 3,409,056

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -3.37e+10 |     1.71e+10 |     -1.9675 |     0.049 |
| Slope       |       0.6169 |     5.51e-05 |  11186.9942 |     0.000 |

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
- Python: 3,617,586
- Common: 3,583,392

**Precision1**: 0.000% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 6.63e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.58e+06 |       3.58e+06 |       3.58e+06 |       3.58e+06 |
| mean       |       107.6003 |       107.6001 |      -1.90e-04 |      -7.24e-08 |
| std        |      2627.3839 |      2627.3839 |         0.0830 |       3.16e-05 |
| min        |     -1591.6364 |     -1591.6364 |       -43.5883 |        -0.0166 |
| 25%        |         2.2471 |         2.2470 |      -1.37e-07 |      -5.21e-11 |
| 50%        |         8.4673 |         8.4670 |         0.0000 |         0.0000 |
| 75%        |        30.7168 |        30.7168 |       1.35e-07 |       5.12e-11 |
| max        |    519704.0000 |    519704.0000 |         4.4842 |         0.0017 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,583,392

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.90e-04 |     4.39e-05 |     -4.3319 |     0.000 |
| Slope       |       1.0000 |     1.67e-08 |    5.99e+07 |     0.000 |

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
- Python: 3,554,041
- Common: 2,730,607

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.13e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.73e+06 |       2.73e+06 |       2.73e+06 |       2.73e+06 |
| mean       |        61.9969 |        61.9749 |        -0.0220 |      -6.30e-06 |
| std        |      3492.9321 |      3492.9205 |         7.5822 |         0.0022 |
| min        |    -14573.0000 |    -14573.0000 |     -3081.3552 |        -0.8822 |
| 25%        |         4.6053 |         4.6053 |      -1.57e-07 |      -4.49e-11 |
| 50%        |         7.6793 |         7.6787 |         0.0000 |         0.0000 |
| 75%        |        17.8215 |        17.8207 |       1.55e-07 |       4.45e-11 |
| max        |       1.05e+06 |       1.05e+06 |         0.0919 |       2.63e-05 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0217 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,730,607

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |      -0.0217 |       0.0046 |     -4.7193 |     0.000 |
| Slope       |       1.0000 |     1.31e-06 | 761240.4084 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 24/2730607 (0.001%)
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
- Python: 3,578,887
- Common: 3,451,784

**Precision1**: 0.007% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 2.14e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.45e+06 |       3.45e+06 |       3.45e+06 |       3.45e+06 |
| mean       |        16.3739 |        16.3749 |       9.99e-04 |       4.77e-06 |
| std        |       209.4212 |       209.4212 |         0.5576 |         0.0027 |
| min        |    -21796.0000 |    -21796.0000 |      -121.3652 |        -0.5795 |
| 25%        |         3.6746 |         3.6748 |      -1.08e-07 |      -5.16e-10 |
| 50%        |         5.9289 |         5.9292 |         0.0000 |         0.0000 |
| 75%        |         9.1589 |         9.1597 |       1.08e-07 |       5.14e-10 |
| max        |     47246.0000 |     47246.0000 |       269.4239 |         1.2865 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0011 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,451,784

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |       0.0011 |     3.01e-04 |      3.4999 |     0.000 |
| Slope       |       1.0000 |     1.43e-06 | 697746.4741 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 240/3451784 (0.007%)
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
- Python: 3,626,823
- Common: 3,624,363

**Precision1**: 0.011% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 8.39e-08 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.1995 |         0.1995 |       2.43e-06 |       7.03e-06 |
| std        |         0.3454 |         0.3454 |         0.0020 |         0.0059 |
| min        |      -7.96e-05 |      -7.96e-05 |        -0.3067 |        -0.8880 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         0.3028 |         0.3029 |         0.0000 |         0.0000 |
| max        |        48.7452 |        48.7452 |         0.7243 |         2.0969 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.23e-06 |     1.23e-06 |      6.7050 |     0.000 |
| Slope       |       1.0000 |     3.08e-06 | 325036.5301 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 384/3624363 (0.011%)
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
- Python: 3,626,823
- Common: 3,624,363

**Precision1**: 0.006% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 0.00e+00 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.62e+06 |       3.62e+06 |       3.62e+06 |       3.62e+06 |
| mean       |         0.4092 |         0.4092 |       4.30e-05 |       8.75e-05 |
| std        |         0.4917 |         0.4917 |         0.0079 |         0.0161 |
| min        |         0.0000 |         0.0000 |        -1.0000 |        -2.0338 |
| 25%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 50%        |         0.0000 |         0.0000 |         0.0000 |         0.0000 |
| 75%        |         1.0000 |         1.0000 |         0.0000 |         0.0000 |
| max        |         1.0000 |         1.0000 |         1.0000 |         2.0338 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0001 + 0.9999 * stata
- **R-squared**: 0.9997
- **N observations**: 3,624,363

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     8.97e-05 |     5.42e-06 |     16.5431 |     0.000 |
| Slope       |       0.9999 |     8.47e-06 | 118008.7505 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 228/3624363 (0.006%)
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
- Python: 3,233,546
- Common: 3,231,761

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.89e-09 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       3.23e+06 |       3.23e+06 |       3.23e+06 |       3.23e+06 |
| mean       |         0.7025 |         0.7024 |      -9.67e-06 |      -2.06e-07 |
| std        |        46.9281 |        46.9281 |         0.0086 |       1.84e-04 |
| min        |      -237.0000 |      -237.0000 |        -4.0617 |        -0.0866 |
| 25%        |        -0.0210 |        -0.0210 |      -2.50e-09 |      -5.32e-11 |
| 50%        |         0.0863 |         0.0863 |         0.0000 |         0.0000 |
| 75%        |         0.2252 |         0.2252 |       2.53e-09 |       5.39e-11 |
| max        |     12739.0000 |     12739.0000 |         1.2280 |         0.0262 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0000 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 3,231,761

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -9.65e-06 |     4.79e-06 |     -2.0144 |     0.044 |
| Slope       |       1.0000 |     1.02e-07 |    9.79e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 48/3231761 (0.001%)
- Stata standard deviation: 4.69e+01

---

### sgr_q

**Status**: ✅ PASSED

**Test Results**:
- Test 1 - Column names: ✅ PASSED
- Test 2 - Superset check: ✅ PASSED
- Test 3 - Precision1 check: ✅ PASSED
- Test 4 - Precision2 check: ✅ PASSED

**Columns**: ['sgr_q']

**Observations**:
- Stata:  2,457,701
- Python: 2,457,721
- Common: 2,457,635

**Precision1**: 0.001% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 3.07e-10 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       2.46e+06 |       2.46e+06 |       2.46e+06 |       2.46e+06 |
| mean       |         1.0672 |         1.0670 |      -1.91e-04 |      -6.66e-07 |
| std        |       286.5317 |       286.5317 |         0.2023 |       7.06e-04 |
| min        |     -3092.0000 |     -3092.0000 |      -146.0200 |        -0.5096 |
| 25%        |        -0.0374 |        -0.0374 |      -2.58e-09 |      -9.00e-12 |
| 50%        |         0.0794 |         0.0794 |         0.0000 |         0.0000 |
| 75%        |         0.2229 |         0.2229 |       2.55e-09 |       8.91e-12 |
| max        |    251440.0000 |    251440.0000 |       187.2391 |         0.6535 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = -0.0002 + 1.0000 * stata
- **R-squared**: 1.0000
- **N observations**: 2,457,635

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |    -1.91e-04 |     1.29e-04 |     -1.4774 |     0.140 |
| Slope       |       1.0000 |     4.50e-07 |    2.22e+06 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 25/2457635 (0.001%)
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
- Python: 2,417,352
- Common: 1,675,094

**Precision1**: 0.014% obs with std_diff >= 1.00e-02 (tolerance: < 10%)

**Precision2**: 99th percentile diff = 1.55e-07 (tolerance: < 1.00e+00)

**Summary Statistics** (Common Observations):

| Statistic  |          Stata |         Python |     Difference | Std Difference |
|------------|----------------|----------------|----------------|----------------|
| count      |       1.68e+06 |       1.68e+06 |       1.68e+06 |       1.68e+06 |
| mean       |         0.6565 |         0.6565 |      -3.03e-06 |      -8.78e-06 |
| std        |         0.3446 |         0.3447 |         0.0086 |         0.0251 |
| min        |        -0.4077 |        -0.4077 |        -0.9940 |        -2.8845 |
| 25%        |         0.5451 |         0.5451 |      -1.26e-08 |      -3.66e-08 |
| 50%        |         0.6594 |         0.6594 |       2.83e-11 |       8.21e-11 |
| 75%        |         0.7667 |         0.7667 |       1.27e-08 |       3.68e-08 |
| max        |       158.7655 |       158.7656 |         6.1017 |        17.7068 |

**Regression Analysis** (Python ~ Stata):

- **Model**: python = 0.0000 + 1.0000 * stata
- **R-squared**: 0.9994
- **N observations**: 1,675,094

| Coefficient |     Estimate |    Std Error | t-statistic |   p-value |
|-------------|--------------|--------------|-------------|----------|
| Intercept   |     4.51e-06 |     1.44e-05 |      0.3138 |     0.754 |
| Slope       |       1.0000 |     1.94e-05 |  51614.4811 |     0.000 |

**Feedback**:
- Num observations with std_diff >= TOL_DIFF_1: 237/1675094 (0.014%)
- Stata standard deviation: 3.45e-01

---

