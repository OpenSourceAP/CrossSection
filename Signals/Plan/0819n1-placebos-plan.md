# Placebos Translation Plan

## Mission

Translate every Stata `.do` file in `Code/Placebos/` to Python scripts in `pyCode/Placebos/`, ensure outputs match Stata results, and integrate into the project’s run + test pipelines.

Do NOT make any changes to code which generates intermediate data files or predictors. 

## Action Items

1. **Inventory**

   * List all `.do` files in `Code/Placebos/`.
   * Create a mapping table (`Journal/placebos_map.json`) of Stata → Python scripts.

2. **Translation**

   * Port logic line-by-line from each `.do`.
   * Use Python equivalents for Stata lags/leads, merges, and by-group ops.
   * Save outputs to `../pyData/Placebos/`.
   * Check @DocsForClaude/  and if there exists a utils python veresion of stata functions that we have use that version of the stata function. 

3. **Validation**

   * Use `utils/test_placebos.py` to compare Python outputs with Stata outputs (schema, rows, values).
   * Mark status: `todo → first-pass → green`.
   * Acceptable tolerance for missing observations (subset test) is 0 missing observations.

4. **Debugging**

   * When mismatches appear, isolate by permno/date.
   * Trace ops, fix logic, and re-run validation.

5. **Sign-off**

   * Lock final schemas & filenames.
   * Update docs with lessons/traps.
   * All statuses `green`.

## Tracker

| Stata `.do` | Python script | Status     |
| ----------- | ------------- | ---------- |
| AMq | AMq.py | green |
| AssetGrowth_q | AssetGrowth_q.py | green |
| AssetLiquidityBook | AssetLiquidityBook.py | todo |
| AssetLiquidityBookQuart | AssetLiquidityBookQuart.py | todo |
| AssetLiquidityMarket | AssetLiquidityMarket.py | todo |
| AssetLiquidityMarketQuart | AssetLiquidityMarketQuart.py | todo |
| AssetTurnover | AssetTurnover.py | green |
| AssetTurnover_q | AssetTurnover_q.py | todo |
| BMq | BMq.py | green |
| BetaBDLeverage | BetaBDLeverage.py | todo |
| BetaSquared | BetaSquared.py | todo |
| BidAskTAQ | BidAskTAQ.py | todo |
| BookLeverageQuarterly | BookLeverageQuarterly.py | todo |
| BrandCapital | BrandCapital.py | todo |
| CBOperProfLagAT | CBOperProfLagAT.py | todo |
| CBOperProfLagAT_q | CBOperProfLagAT_q.py | todo |
| CFq | CFq.py | green |
| CapTurnover | CapTurnover.py | todo |
| CapTurnover_q | CapTurnover_q.py | todo |
| ChNCOA | ChNCOA.py | todo |
| ChNCOL | ChNCOL.py | todo |
| ChangeRoA | ChangeRoA.py | todo |
| ChangeRoE | ChangeRoE.py | todo |
| DelSTI | DelSTI.py | todo |
| DivYield | DivYield.py | todo |
| DivYieldAnn | DivYieldAnn.py | todo |
| EBM_q | EBM_q.py | todo |
| EPq | EPq.py | green |
| ETR | ETR.py | todo |
| EarningsSmoothness | EarningsSmoothness.py | todo |
| EntMult_q | EntMult_q.py | todo |
| ForecastDispersionLT | ForecastDispersionLT.py | todo |
| GPlag | GPlag.py | todo |
| GPlag_q | GPlag_q.py | todo |
| GrGMToGrSales | GrGMToGrSales.py | todo |
| GrSaleToGrReceivables | GrSaleToGrReceivables.py | todo |
| KZ | KZ.py | todo |
| KZ_q | KZ_q.py | todo |
| LaborforceEfficiency | LaborforceEfficiency.py | todo |
| Leverage_q | Leverage_q.py | todo |
| NetDebtPrice_q | NetDebtPrice_q.py | todo |
| NetPayoutYield_q | NetPayoutYield_q.py | todo |
| OPLeverage_q | OPLeverage_q.py | todo |
| OScore_q | OScore_q.py | todo |
| OperProfLag | OperProfLag.py | todo |
| OperProfLag_q | OperProfLag_q.py | todo |
| OperProfRDLagAT | OperProfRDLagAT.py | todo |
| OperProfRDLagAT_q | OperProfRDLagAT_q.py | todo |
| PM_q | PM_q.py | todo |
| PS_q | PS_q.py | todo |
| PayoutYield_q | PayoutYield_q.py | todo |
| RD_q | RD_q.py | todo |
| RetNOA | RetNOA.py | todo |
| RetNOA_q | RetNOA_q.py | todo |
| SP_q | SP_q.py | todo |
| Tax_q | Tax_q.py | todo |
| WW | WW.py | todo |
| WW_Q | WW_Q.py | todo |
| ZScore | ZScore.py | todo |
| ZScore_q | ZScore_q.py | todo |
| ZZ1_EarningsPersistence_EarningsPredictability | ZZ1_EarningsPersistence_EarningsPredictability.py | todo |
| ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism | ZZ1_EarningsValueRelevance_EarningsTimeliness_EarningsConservatism.py | todo |
| ZZ1_PM_ChPM | ZZ1_PM_ChPM.py | todo |
| ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet | ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py | todo |
| ZZ1_currat_pchcurrat | ZZ1_currat_pchcurrat.py | todo |
| ZZ2_AccrualQuality_AccrualQualityJune | ZZ2_AccrualQuality_AccrualQualityJune.py | todo |
| ZZ2_BetaDimson | ZZ2_BetaDimson.py | todo |
| ZZ2_DownsideBeta | ZZ2_DownsideBeta.py | todo |
| ZZ2_FailureProbability_FailureProbabilityJune | ZZ2_FailureProbability_FailureProbabilityJune.py | todo |
| ZZ2_IdioVolCAPM_ReturnSkewCAPM | ZZ2_IdioVolCAPM_ReturnSkewCAPM.py | todo |
| ZZ2_IdioVolQF_ReturnSkewQF | ZZ2_IdioVolQF_ReturnSkewQF.py | todo |
| ZZ3_DelayAcct_DelayNonAcct | ZZ3_DelayAcct_DelayNonAcct.py | todo |
| cashdebt | cashdebt.py | green |
| cfpq | cfpq.py | todo |
| depr | depr.py | todo |
| fgr5yrNoLag | fgr5yrNoLag.py | todo |
| nanalyst | nanalyst.py | todo |
| pchdepr | pchdepr.py | todo |
| pchgm_pchsale | pchgm_pchsale.py | todo |
| pchquick | pchquick.py | todo |
| pchsaleinv | pchsaleinv.py | todo |
| quick | quick.py | green |
| rd_sale | rd_sale.py | todo |
| rd_sale_q | rd_sale_q.py | todo |
| roavol | roavol.py | todo |
| roic | roic.py | green |
| salecash | salecash.py | todo |
| saleinv | saleinv.py | todo |
| salerec | salerec.py | todo |
| secured | secured.py | todo |
| securedind | securedind.py | todo |
| sgr | sgr.py | todo |
| sgr_q | sgr_q.py | todo |
| tang_q | tang_q.py | green |

## Progress Summary

**Status as of completion:**
- **Total scripts**: 89
- **Completed and passing validation**: 10 (green status)
- **Remaining to implement**: 79 (todo status)
- **Success rate**: 100% of implemented scripts pass validation

**Completed scripts (all validation green ✅):**
1. AMq.py - Total assets to market cap (quarterly)
2. AssetGrowth_q.py - Asset Growth (quarterly) 
3. AssetTurnover.py - Asset Turnover
4. BMq.py - Book-to-market (quarterly)
5. CFq.py - Cash-flow to market (quarterly)
6. EPq.py - Earnings-to-price ratio (quarterly)
7. cashdebt.py - Cash flow to debt
8. quick.py - Quick ratio
9. roic.py - Return on invested capital
10. tang_q.py - Tangibility (quarterly)

## Next Steps

### Systematic Implementation Strategy

**Priority 1: Simple Arithmetic Operations** (estimated 30 scripts)
- Scripts with basic formulas like divisions, multiplications, additions
- No complex lag operations or merges
- Examples: cfpq, depr, salecash, saleinv, salerec

**Priority 2: Single Lag Operations** (estimated 25 scripts)
- Scripts using l12.variable or similar simple lags
- Examples: AssetTurnover_q, pchdepr, pchquick, pchsaleinv

**Priority 3: Complex Multi-step Calculations** (estimated 20 scripts)
- Scripts with multiple merges, complex transformations
- Examples: DivYield, EarningsSmoothness, ForecastDispersionLT

**Priority 4: Multi-variable Complex Operations** (estimated 4 scripts)
- The ZZ* scripts with multiple outputs per file
- Require careful analysis of Stata code structure

### Implementation Pattern
Each script follows this pattern:
1. Load required parquet files
2. Apply filters/joins as needed
3. Implement signal calculation line-by-line from Stata
4. Save using save_placebo() utility
5. Run validation test

### Testing Strategy
- Run `python3 utils/test_placebos.py` after each batch
- All scripts must achieve validation green status
- Focus on superset check (Python ⊇ Stata observations)
- Precision requirements typically pass when logic is correct

