Validating 108 placebos: ['AMq', 'AccrualQuality', 'AccrualQualityJune', 'AssetGrowth_q', 'AssetLiquidityBook', 'AssetLiquidityBookQuart', 'AssetLiquidityMarket', 'AssetLiquidityMarketQuart', 'AssetTurnover', 'AssetTurnover_q', 'BMq', 'BetaBDLeverage', 'BetaDimson', 'BetaSquared', 'BidAskTAQ', 'BookLeverageQuarterly', 'BrandCapital', 'CBOperProfLagAT', 'CBOperProfLagAT_q', 'CFq', 'CapTurnover', 'CapTurnover_q', 'ChNCOA', 'ChNCOL', 'ChPM', 'ChangeRoA', 'ChangeRoE', 'DelSTI', 'DelayAcct', 'DelayNonAcct', 'DivYield', 'DivYieldAnn', 'DownsideBeta', 'EBM_q', 'EPq', 'ETR', 'EarningsConservatism', 'EarningsPersistence', 'EarningsPredictability', 'EarningsSmoothness', 'EarningsTimeliness', 'EarningsValueRelevance', 'EntMult_q', 'FailureProbability', 'FailureProbabilityJune', 'ForecastDispersionLT', 'GPlag', 'GPlag_q', 'GrGMToGrSales', 'GrSaleToGrReceivables', 'IdioVolCAPM', 'IdioVolQF', 'KZ', 'KZ_q', 'LaborforceEfficiency', 'Leverage_q', 'NetDebtPrice_q', 'NetPayoutYield_q', 'OPLeverage_q', 'OScore_q', 'OperProfLag', 'OperProfLag_q', 'OperProfRDLagAT', 'OperProfRDLagAT_q', 'PM', 'PM_q', 'PS_q', 'PayoutYield_q', 'RD_q', 'RetNOA', 'RetNOA_q', 'ReturnSkewCAPM', 'ReturnSkewQF', 'SP_q', 'Tax_q', 'WW', 'WW_Q', 'ZScore', 'ZScore_q', 'betaCC', 'betaCR', 'betaNet', 'betaRC', 'betaRR', 'cashdebt', 'cfpq', 'currat', 'depr', 'fgr5yrNoLag', 'nanalyst', 'pchcurrat', 'pchdepr', 'pchgm_pchsale', 'pchquick', 'pchsaleinv', 'quick', 'rd_sale', 'rd_sale_q', 'roavol', 'roic', 'salecash', 'saleinv', 'salerec', 'secured', 'securedind', 'sgr', 'sgr_q', 'tang_q']
Including 6 missing Python CSVs in summary: ['AbnormalAccrualsPercent', 'FRbook', 'IntrinsicValue', 'OrgCapNoAdj', 'ResidualMomentum6m', 'grcapx1y']

=== Validating AMq ===
  Loaded Stata: 2584378 rows, Python: 2809455 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.92e-08 < 1.00e+00)
  ✅ AMq PASSED

=== Validating AccrualQuality ===
  Loaded Stata: 1740065 rows, Python: 1789393 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 148568 observations, 8.54% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (90.694% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 1.67e+00 >= 1.00e+00)
  ❌ AccrualQuality FAILED
    Bad observations: 1443393/1591497 (90.694%)

=== Validating AccrualQualityJune ===
  Loaded Stata: 1784388 rows, Python: 1815384 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 147179 observations, 8.25% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (89.541% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 1.75e+00 >= 1.00e+00)
  ❌ AccrualQualityJune FAILED
    Bad observations: 1465979/1637209 (89.541%)

=== Validating AssetGrowth_q ===
  Loaded Stata: 2303961 rows, Python: 2303943 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 49 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.89e-08 < 1.00e+00)
  ❌ AssetGrowth_q FAILED
    Bad observations: 36/2303912 (0.002%)

=== Validating AssetLiquidityBook ===
  Loaded Stata: 3595932 rows, Python: 3598966 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.48e-08 < 1.00e+00)
  ✅ AssetLiquidityBook PASSED

=== Validating AssetLiquidityBookQuart ===
  Loaded Stata: 2538807 rows, Python: 2553360 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 44 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.44e-08 < 1.00e+00)
  ❌ AssetLiquidityBookQuart FAILED
    Bad observations: 67/2538763 (0.003%)

=== Validating AssetLiquidityMarket ===
  Loaded Stata: 3476318 rows, Python: 3477044 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.65e-07 < 1.00e+00)
  ✅ AssetLiquidityMarket PASSED

=== Validating AssetLiquidityMarketQuart ===
  Loaded Stata: 2503163 rows, Python: 2503127 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 50 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.49e-07 < 1.00e+00)
  ❌ AssetLiquidityMarketQuart FAILED
    Bad observations: 84/2503113 (0.003%)

=== Validating AssetTurnover ===
  Loaded Stata: 2796921 rows, Python: 2816617 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.94e-09 < 1.00e+00)
  ✅ AssetTurnover PASSED
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)

=== Validating AssetTurnover_q ===
  Loaded Stata: 1963604 rows, Python: 2183915 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 39 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.48e-09 < 1.00e+00)
  ❌ AssetTurnover_q FAILED
    Bad observations: 42/1963565 (0.002%)

=== Validating BMq ===
  Loaded Stata: 2568885 rows, Python: 2717113 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.24e-07 < 1.00e+00)
  ✅ BMq PASSED

=== Validating BetaBDLeverage ===
  Loaded Stata: 2116539 rows, Python: 2130495 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (2.206% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.31e-01 < 1.00e+00)
  ✅ BetaBDLeverage PASSED

=== Validating BetaDimson ===
  Loaded Stata: 5002680 rows, Python: 5083747 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.40e-07 < 1.00e+00)
  ✅ BetaDimson PASSED

=== Validating BetaSquared ===
  Loaded Stata: 4285574 rows, Python: 4353773 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.04e-08 < 1.00e+00)
  ✅ BetaSquared PASSED

=== Validating BidAskTAQ ===
  Loaded Stata: 3262927 rows, Python: 3262927 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.96e-08 < 1.00e+00)
  ✅ BidAskTAQ PASSED

=== Validating BookLeverageQuarterly ===
  Loaded Stata: 2572594 rows, Python: 2670966 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.13e-13 < 1.00e+00)
  ✅ BookLeverageQuarterly PASSED

=== Validating BrandCapital ===
  Loaded Stata: 1231460 rows, Python: 1280000 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (5.877% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.25e-02 < 1.00e+00)
  ✅ BrandCapital PASSED

=== Validating CBOperProfLagAT ===
  Loaded Stata: 2103518 rows, Python: 2171034 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.60e-08 < 1.00e+00)
  ✅ CBOperProfLagAT PASSED

=== Validating CBOperProfLagAT_q ===
  Loaded Stata: 1911489 rows, Python: 2183952 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ❌ Test 3 - Precision1 check: FAILED (26.663% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 2.54e+00 >= 1.00e+00)
  ❌ CBOperProfLagAT_q FAILED
    Bad observations: 509657/1911489 (26.663%)

=== Validating CFq ===
  Loaded Stata: 2797878 rows, Python: 3041630 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.008% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.51e-08 < 1.00e+00)
  ✅ CFq PASSED

=== Validating CapTurnover ===
  Loaded Stata: 2985685 rows, Python: 2986378 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.50e-08 < 1.00e+00)
  ✅ CapTurnover PASSED

=== Validating CapTurnover_q ===
  Loaded Stata: 2486325 rows, Python: 2486315 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 48 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.01e-08 < 1.00e+00)
  ❌ CapTurnover_q FAILED
    Bad observations: 93/2486277 (0.004%)

=== Validating ChNCOA ===
  Loaded Stata: 3295125 rows, Python: 3295872 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.48e-08 < 1.00e+00)
  ✅ ChNCOA PASSED

=== Validating ChNCOL ===
  Loaded Stata: 3249290 rows, Python: 3250061 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.79e-08 < 1.00e+00)
  ✅ ChNCOL PASSED

=== Validating ChPM ===
  Loaded Stata: 3222277 rows, Python: 3288060 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.23e-09 < 1.00e+00)
  ✅ ChPM PASSED

=== Validating ChangeRoA ===
  Loaded Stata: 2296769 rows, Python: 2526837 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.010% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.61e-08 < 1.00e+00)
  ✅ ChangeRoA PASSED

=== Validating ChangeRoE ===
  Loaded Stata: 2360217 rows, Python: 2535908 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.18e-09 < 1.00e+00)
  ✅ ChangeRoE PASSED

=== Validating DelSTI ===
  Loaded Stata: 3295155 rows, Python: 3295872 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.04e-07 < 1.00e+00)
  ✅ DelSTI PASSED

=== Validating DelayAcct ===
  Loaded Stata: 674090 rows, Python: 722651 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 4549 observations, 0.67% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (89.589% obs with std_diff >= 1.00e-02 >= 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.12e-01 < 1.00e+00)
  ❌ DelayAcct FAILED
    Bad observations: 599832/669541 (89.589%)

=== Validating DelayNonAcct ===
  Loaded Stata: 674090 rows, Python: 722651 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 4549 observations, 0.67% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (78.142% obs with std_diff >= 1.00e-02 >= 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.86e-01 < 1.00e+00)
  ❌ DelayNonAcct FAILED
    Bad observations: 523193/669541 (78.142%)

=== Validating DivYield ===
  Loaded Stata: 421384 rows, Python: 2014931 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.007% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.24e-08 < 1.00e+00)
  ✅ DivYield PASSED

=== Validating DivYieldAnn ===
  Loaded Stata: 3878713 rows, Python: 3883930 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.032% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.07e-08 < 1.00e+00)
  ✅ DivYieldAnn PASSED

=== Validating DownsideBeta ===
  Loaded Stata: 4848559 rows, Python: 5072307 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 6 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
   index  permno  yyyymm  DownsideBeta
     0   11746  192608      0.712000
     1   12909  192608      0.917963
     2   13127  192608      0.547239
     3   13629  192612      0.354627
     4   13960  192608     -1.756058
     5   18593  192608      0.171028
  ✅ Test 3 - Precision1 check: PASSED (0.349% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.20e-13 < 1.00e+00)
  ❌ DownsideBeta FAILED
    Bad observations: 16923/4848553 (0.349%)

=== Validating EBM_q ===
  Loaded Stata: 2497505 rows, Python: 2497500 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 54 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.39e-08 < 1.00e+00)
  ❌ EBM_q FAILED
    Bad observations: 44/2497451 (0.002%)

=== Validating EPq ===
  Loaded Stata: 1893938 rows, Python: 1893940 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 36 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.62e-08 < 1.00e+00)
  ❌ EPq FAILED
    Bad observations: 82/1893902 (0.004%)

=== Validating ETR ===
  Loaded Stata: 2657230 rows, Python: 2658445 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.20e-12 < 1.00e+00)
  ✅ ETR PASSED

=== Validating EarningsConservatism ===
  Loaded Stata: 1467671 rows, Python: 1503418 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 36945 observations, 2.52% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (3.563% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.39e-02 < 1.00e+00)
  ❌ EarningsConservatism FAILED
    Bad observations: 50971/1430726 (3.563%)

=== Validating EarningsPersistence ===
  Loaded Stata: 1495672 rows, Python: 1553579 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.12e-07 < 1.00e+00)
  ✅ EarningsPersistence PASSED

=== Validating EarningsPredictability ===
  Loaded Stata: 1495672 rows, Python: 1553579 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.057% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.62e-10 < 1.00e+00)
  ✅ EarningsPredictability PASSED

=== Validating EarningsSmoothness ===
  Loaded Stata: 1482823 rows, Python: 1538785 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.005% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.06e-07 < 1.00e+00)
  ✅ EarningsSmoothness PASSED

=== Validating EarningsTimeliness ===
  Loaded Stata: 1467923 rows, Python: 1503418 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 36945 observations, 2.52% > 0.0% threshold)
  Sample of missing observations:
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.76e-07 < 1.00e+00)
  ❌ EarningsTimeliness FAILED
    Bad observations: 15/1430978 (0.001%)

=== Validating EarningsValueRelevance ===
  Loaded Stata: 1427774 rows, Python: 1503418 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.44e-07 < 1.00e+00)
  ✅ EarningsValueRelevance PASSED

=== Validating EntMult_q ===
  Loaded Stata: 1689737 rows, Python: 1691109 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 94 observations, 0.01% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.67e-09 < 1.00e+00)
  ❌ EntMult_q FAILED
    Bad observations: 19/1689643 (0.001%)

=== Validating FailureProbability ===
  Loaded Stata: 1958798 rows, Python: 2420937 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.105% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.07e-08 < 1.00e+00)
  ✅ FailureProbability PASSED

=== Validating FailureProbabilityJune ===
  Loaded Stata: 2090935 rows, Python: 2558215 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.206% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.70e-07 < 1.00e+00)
  ✅ FailureProbabilityJune PASSED

=== Validating ForecastDispersionLT ===
  Loaded Stata: 828578 rows, Python: 828784 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 1774 observations, 0.21% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.087% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.49e-07 < 1.00e+00)
  ❌ ForecastDispersionLT FAILED
    Bad observations: 717/826804 (0.087%)

=== Validating GPlag ===
  Loaded Stata: 3281500 rows, Python: 3297874 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.006% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.55e-08 < 1.00e+00)
  ✅ GPlag PASSED

=== Validating GPlag_q ===
  Loaded Stata: 2216580 rows, Python: 2482774 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.012% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.78e-08 < 1.00e+00)
  ✅ GPlag_q PASSED

=== Validating GrGMToGrSales ===
  Loaded Stata: 3229675 rows, Python: 3279256 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.11e-09 < 1.00e+00)
  ✅ GrGMToGrSales PASSED

=== Validating GrSaleToGrReceivables ===
  Loaded Stata: 3134552 rows, Python: 3303855 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.012% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.03e-10 < 1.00e+00)
  ✅ GrSaleToGrReceivables PASSED

=== Validating IdioVolCAPM ===
  Loaded Stata: 5026821 rows, Python: 4998007 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 28814 observations, 0.57% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (2.348% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.16e-02 < 1.00e+00)
  ❌ IdioVolCAPM FAILED
    Bad observations: 117869/5019669 (2.348%)

=== Validating IdioVolQF ===
  Loaded Stata: 3986461 rows, Python: 3955898 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 30563 observations, 0.77% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.10e-08 < 1.00e+00)
  ❌ IdioVolQF FAILED
    Bad observations: 0/3955898 (0.000%)

=== Validating KZ ===
  Loaded Stata: 2630499 rows, Python: 2663058 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.04e-09 < 1.00e+00)
  ✅ KZ PASSED

=== Validating KZ_q ===
  Loaded Stata: 1936942 rows, Python: 1953037 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 255 observations, 0.01% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.12e-09 < 1.00e+00)
  ❌ KZ_q FAILED
    Bad observations: 20/1936687 (0.001%)

=== Validating LaborforceEfficiency ===
  Loaded Stata: 2974260 rows, Python: 3073530 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.28e-09 < 1.00e+00)
  ✅ LaborforceEfficiency PASSED

=== Validating Leverage_q ===
  Loaded Stata: 2571833 rows, Python: 2571800 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 67 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.47e-08 < 1.00e+00)
  ❌ Leverage_q FAILED
    Bad observations: 3/2571766 (0.000%)

=== Validating NetDebtPrice_q ===
  Loaded Stata: 1178409 rows, Python: 1219765 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 40 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.85e-08 < 1.00e+00)
  ❌ NetDebtPrice_q FAILED
    Bad observations: 6/1178369 (0.001%)

=== Validating NetPayoutYield_q ===
  Loaded Stata: 2520037 rows, Python: 2622217 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.016% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.53e-08 < 1.00e+00)
  ✅ NetPayoutYield_q PASSED

=== Validating OPLeverage_q ===
  Loaded Stata: 2546734 rows, Python: 2546725 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 65 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.009% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.72e-08 < 1.00e+00)
  ❌ OPLeverage_q FAILED
    Bad observations: 235/2546669 (0.009%)

=== Validating OScore_q ===
  Loaded Stata: 877922 rows, Python: 2823459 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 0.00e+00 < 1.00e+00)
  ✅ OScore_q PASSED

=== Validating OperProfLag ===
  Loaded Stata: 1292263 rows, Python: 1809262 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.44e-08 < 1.00e+00)
  ✅ OperProfLag PASSED

=== Validating OperProfLag_q ===
  Loaded Stata: 2395707 rows, Python: 2579758 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.15e-05 < 1.00e+00)
  ✅ OperProfLag_q PASSED

=== Validating OperProfRDLagAT ===
  Loaded Stata: 2742767 rows, Python: 2948224 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (4.539% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.20e-02 < 1.00e+00)
  ✅ OperProfRDLagAT PASSED

=== Validating OperProfRDLagAT_q ===
  Loaded Stata: 1800025 rows, Python: 1799984 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 114 observations, 0.01% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.013% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.55e-08 < 1.00e+00)
  ❌ OperProfRDLagAT_q FAILED
    Bad observations: 235/1799911 (0.013%)

=== Validating PM ===
  Loaded Stata: 3547773 rows, Python: 3616815 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.31e-09 < 1.00e+00)
  ✅ PM PASSED

=== Validating PM_q ===
  Loaded Stata: 2492083 rows, Python: 2823459 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.86e-09 < 1.00e+00)
  ✅ PM_q PASSED

=== Validating PS_q ===
  Loaded Stata: 310650 rows, Python: 371767 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 17 observations, 0.01% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (53.350% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 3.16e+00 >= 1.00e+00)
  ❌ PS_q FAILED
    Bad observations: 165723/310633 (53.350%)

=== Validating PayoutYield_q ===
  Loaded Stata: 1310000 rows, Python: 2891504 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.015% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.46e-08 < 1.00e+00)
  ✅ PayoutYield_q PASSED

=== Validating RD_q ===
  Loaded Stata: 833583 rows, Python: 3038208 rows
  ✅ Test 1 - Column names: PASSED
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1698: RuntimeWarning: invalid value encountered in subtract
  return self.model.wendog - self.model.predict(
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/numpy/_core/_methods.py:52: RuntimeWarning: invalid value encountered in reduce
  return umr_sum(a, axis, dtype, out, keepdims, initial, where)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1698: RuntimeWarning: invalid value encountered in subtract
  return self.model.wendog - self.model.predict(
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.007% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 5.19e-08 < 1.00e+00)
  ✅ RD_q PASSED

=== Validating RetNOA ===
  Loaded Stata: 2892942 rows, Python: 3012996 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.40e-19 < 1.00e+00)
  ✅ RetNOA PASSED

=== Validating RetNOA_q ===
  Loaded Stata: 2413581 rows, Python: 3041661 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.86e-11 < 1.00e+00)
  ✅ RetNOA_q PASSED

=== Validating ReturnSkewCAPM ===
  Loaded Stata: 4997359 rows, Python: 4959575 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 37784 observations, 0.76% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (2.908% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.78e-01 < 1.00e+00)
  ❌ ReturnSkewCAPM FAILED
    Bad observations: 144854/4980640 (2.908%)

=== Validating ReturnSkewQF ===
  Loaded Stata: 3985016 rows, Python: 3955898 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 30525 observations, 0.77% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.899% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.93e-07 < 1.00e+00)
  ❌ ReturnSkewQF FAILED
    Bad observations: 35562/3954491 (0.899%)

=== Validating SP_q ===
  Loaded Stata: 2790383 rows, Python: 2790383 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 31 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.005% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.95e-08 < 1.00e+00)
  ❌ SP_q FAILED
    Bad observations: 127/2790352 (0.005%)

=== Validating Tax_q ===
  Loaded Stata: 1906647 rows, Python: 1906650 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 52 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.61e-09 < 1.00e+00)
  ❌ Tax_q FAILED
    Bad observations: 40/1906595 (0.002%)

=== Validating WW ===
  Loaded Stata: 2702805 rows, Python: 3297568 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.49e-10 < 1.00e+00)
  ✅ WW PASSED

=== Validating WW_Q ===
  Loaded Stata: 2406602 rows, Python: 2493801 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 44 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.62e-07 < 1.00e+00)
  ❌ WW_Q FAILED
    Bad observations: 33/2406558 (0.001%)

=== Validating ZScore ===
  Loaded Stata: 1669459 rows, Python: 1669861 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.31e-08 < 1.00e+00)
  ✅ ZScore PASSED

=== Validating ZScore_q ===
  Loaded Stata: 1214174 rows, Python: 1490451 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.003% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 7.18e-08 < 1.00e+00)
  ✅ ZScore_q PASSED

=== Validating betaCC ===
  Loaded Stata: 3459006 rows, Python: 2486601 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 994210 observations, 28.74% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (75.643% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 1.46e+01 >= 1.00e+00)
  ❌ betaCC FAILED
    Bad observations: 1864457/2464796 (75.643%)

=== Validating betaCR ===
  Loaded Stata: 3459006 rows, Python: 2486601 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 994210 observations, 28.74% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (62.088% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 3.52e+00 >= 1.00e+00)
  ❌ betaCR FAILED
    Bad observations: 1530352/2464796 (62.088%)

=== Validating betaNet ===
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/pandas/core/nanops.py:1016: RuntimeWarning: invalid value encountered in subtract
  sqr = _ensure_numeric((avg - values) ** 2)
/Users/idrees/Desktop/CrossSection/Signals/pyCode/.venv/lib/python3.11/site-packages/statsmodels/regression/linear_model.py:1733: RuntimeWarning: invalid value encountered in subtract
  return np.sum(weights * (model.endog - mean)**2)
  Loaded Stata: 3420591 rows, Python: 2486247 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 955888 observations, 27.95% > 0.0% threshold)
  Sample of missing observations:
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
  ❌ Test 3 - Precision1 check: FAILED (80.912% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 8.03e+00 >= 1.00e+00)
  ❌ betaNet FAILED
    Bad observations: 1994231/2464703 (80.912%)

=== Validating betaRC ===
  Loaded Stata: 3421560 rows, Python: 3461692 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ❌ Test 3 - Precision1 check: FAILED (98.930% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 3.93e+00 >= 1.00e+00)
  ❌ betaRC FAILED
    Bad observations: 3384947/3421560 (98.930%)

=== Validating betaRR ===
  Loaded Stata: 3421560 rows, Python: 3461692 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ❌ Test 3 - Precision1 check: FAILED (98.404% obs with std_diff >= 1.00e-02 >= 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = 2.92e+00 >= 1.00e+00)
  ❌ betaRR FAILED
    Bad observations: 3366957/3421560 (98.404%)

=== Validating cashdebt ===
  Loaded Stata: 3267782 rows, Python: 3284937 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.21e-09 < 1.00e+00)
  ✅ cashdebt PASSED

=== Validating cfpq ===
  Loaded Stata: 2252622 rows, Python: 2703309 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ❌ Test 3 - Precision1 check: FAILED (11.982% obs with std_diff >= 1.00e-02 >= 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.81e-01 < 1.00e+00)
  ❌ cfpq FAILED
    Bad observations: 269905/2252622 (11.982%)

=== Validating currat ===
  Loaded Stata: 3065278 rows, Python: 3069214 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.40e-08 < 1.00e+00)
  ✅ currat PASSED

=== Validating depr ===
  Loaded Stata: 3462713 rows, Python: 3523904 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.68e-09 < 1.00e+00)
  ✅ depr PASSED

=== Validating fgr5yrNoLag ===
  Loaded Stata: 996237 rows, Python: 996104 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 2116 observations, 0.21% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.075% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.43e-07 < 1.00e+00)
  ❌ fgr5yrNoLag FAILED
    Bad observations: 750/994121 (0.075%)

=== Validating nanalyst ===
  Loaded Stata: 2700302 rows, Python: 4047630 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.259% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 0.00e+00 < 1.00e+00)
  ✅ nanalyst PASSED

=== Validating pchcurrat ===
  Loaded Stata: 3624363 rows, Python: 3625095 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (1.042% obs with std_diff >= 1.00e-02 < 10%)
  ❌ Test 4 - Precision2 check: FAILED (99th percentile diff = inf >= 1.00e+00)
  ❌ pchcurrat FAILED
    Bad observations: 37772/3624363 (1.042%)

=== Validating pchdepr ===
  Loaded Stata: 3050498 rows, Python: 3268732 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.002% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.31e-09 < 1.00e+00)
  ✅ pchdepr PASSED

=== Validating pchgm_pchsale ===
  Loaded Stata: 3222544 rows, Python: 3279256 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.59e-09 < 1.00e+00)
  ✅ pchgm_pchsale PASSED

=== Validating pchquick ===
  Loaded Stata: 3339639 rows, Python: 3655797 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.96e-09 < 1.00e+00)
  ✅ pchquick PASSED

=== Validating pchsaleinv ===
  Loaded Stata: 2465425 rows, Python: 3303855 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.66e-09 < 1.00e+00)
  ✅ pchsaleinv PASSED

=== Validating quick ===
  Loaded Stata: 3065278 rows, Python: 3625095 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.06e-08 < 1.00e+00)
  ✅ quick PASSED

=== Validating rd_sale ===
  Loaded Stata: 1207848 rows, Python: 1254467 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 4.06e-09 < 1.00e+00)
  ✅ rd_sale PASSED

=== Validating rd_sale_q ===
  Loaded Stata: 566115 rows, Python: 1051434 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.67e-09 < 1.00e+00)
  ✅ rd_sale_q PASSED

=== Validating roavol ===
  Loaded Stata: 2039901 rows, Python: 2159781 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (2.934% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.44e-02 < 1.00e+00)
  ✅ roavol PASSED

=== Validating roic ===
  Loaded Stata: 3409380 rows, Python: 3410772 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.014% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.38e-23 < 1.00e+00)
  ✅ roic PASSED

=== Validating salecash ===
  Loaded Stata: 3583392 rows, Python: 3616983 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 6.55e-09 < 1.00e+00)
  ✅ salecash PASSED

=== Validating saleinv ===
  Loaded Stata: 2730607 rows, Python: 3616983 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.000% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.12e-09 < 1.00e+00)
  ✅ saleinv PASSED

=== Validating salerec ===
  Loaded Stata: 3451784 rows, Python: 3616983 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.005% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 2.11e-08 < 1.00e+00)
  ✅ salerec PASSED

=== Validating secured ===
  Loaded Stata: 3624363 rows, Python: 3625095 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 8.39e-08 < 1.00e+00)
  ✅ secured PASSED

=== Validating securedind ===
  Loaded Stata: 3624363 rows, Python: 3625095 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.004% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 0.00e+00 < 1.00e+00)
  ✅ securedind PASSED

=== Validating sgr ===
  Loaded Stata: 3231761 rows, Python: 3232394 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.88e-09 < 1.00e+00)
  ✅ sgr PASSED

=== Validating sgr_q ===
  Loaded Stata: 2457701 rows, Python: 2457695 rows
  ✅ Test 1 - Column names: PASSED
  ❌ Test 2 - Superset check: FAILED (Missing 45 observations, 0.00% > 0.0% threshold)
  Sample of missing observations:
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
  ✅ Test 3 - Precision1 check: PASSED (0.001% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 3.03e-10 < 1.00e+00)
  ❌ sgr_q FAILED
    Bad observations: 30/2457656 (0.001%)

=== Validating tang_q ===
  Loaded Stata: 1675098 rows, Python: 2823459 rows
  ✅ Test 1 - Column names: PASSED
  ✅ Test 2 - Superset check: PASSED (Missing 0.00% <= 0.0% threshold)
  ✅ Test 3 - Precision1 check: PASSED (0.010% obs with std_diff >= 1.00e-02 < 10%)
  ✅ Test 4 - Precision2 check: PASSED (99th percentile diff = 1.54e-07 < 1.00e+00)
  ✅ tang_q PASSED

=== AbnormalAccrualsPercent ===
  ❌ Python CSV missing: ../pyData/Placebos/AbnormalAccrualsPercent.csv

=== FRbook ===
  ❌ Python CSV missing: ../pyData/Placebos/FRbook.csv

=== IntrinsicValue ===
  ❌ Python CSV missing: ../pyData/Placebos/IntrinsicValue.csv

=== OrgCapNoAdj ===
  ❌ Python CSV missing: ../pyData/Placebos/OrgCapNoAdj.csv

=== ResidualMomentum6m ===
  ❌ Python CSV missing: ../pyData/Placebos/ResidualMomentum6m.csv

=== grcapx1y ===
  ❌ Python CSV missing: ../pyData/Placebos/grcapx1y.csv

Detailed results written to: ../Logs/testout_placebos.md

=== SUMMARY ===
Available placebos tested: 108
Missing Python CSVs included: 6
Python-only CSVs included: 0
Passed validation: 69
Failed validation: 39
❌ SOME TESTS FAILED
