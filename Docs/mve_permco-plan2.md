# Plan for updating signals to use mve_permco

2025-10-17 Andrew Chen

## Problem Summary

Issue #167 describes a problem where the current code fails to aggregate market equity across multiple stock identifiers (permnos) within the same company (permco). While multi-permno companies represent only ~1% of securities, they account for ~4% of total market capitalization.

We fixed this issue in commit 68d6ce5. However, in the previous fix (commit 68d6ce5), we did not carefully track deviations of the output from the legacy Stata code. We rolled back and ensured we knew when the Stata replication was complete (see https://github.com/OpenSourceAP/CrossSection/issues/174) and then started to address the current Github issues that. The goal here is just to re-apply and check again, being more aware of how we are deviating from Stata. 


## Files That Need To Be Changed

### Step 0: Remove mve_c references from specific files (5 files) ✅

These files should have references to `mve_c` removed FIRST, before any other changes:

1. **Signals/pyCode/Predictors/Governance.py** - Remove `mve_c` references ✅
2. **Signals/pyCode/Predictors/RevenueSurprise.py** - Remove `mve_c` references ✅
3. **Signals/pyCode/Predictors/ZZ1_Activism1_Activism2.py** - Remove `mve_c` references ✅
4. **Signals/pyCode/Predictors/sfe.py** - Remove `mve_c` references ✅
5. **Signals/pyCode/Predictors/roaq.py** - Remove `mve_c` references ✅

### Core Data Processing and Testing (3 files) ✅

6. **Signals/pyCode/DataDownloads/CRSPMonthly.py** ✅
   - Add calculation of `mve_permco` after line 105 (after creating `mve_c`)
   - Aggregate `mve_c` by `permco` and `time_avail_m` to create `mve_permco`
   - Keep `permco` in the dataset (currently dropped at line 108)
   - Merge `mve_permco` back to main dataset

7. **Signals/pyCode/SignalMasterTable.py**
   - Update line 26 to include `mve_permco` in the columns list
   - Update line 127 to include `mve_permco` in the reordered columns (it's already there but commented as "commonly used crsp variables")

8. Test by updating BM.py to use mve_permco ✅
   - Hand check result

### Predictors: Accounting Scaling Only (20 files)

These use mve_permco only for rescaling Compustat Fund A accounting numbers. Replace `mve_c` with `mve_permco`:

8. AccrualsBM.py ✅
9. AdExp.py ✅
10. AM.py ✅
11. CashProd.py ✅
12. CF.py ✅
13. cfp.py ✅
14. DebtIssuance.py ✅
15. EntMult.py ✅
16. EP.py ✅
17. Frontier.py ✅
18. Leverage.py ✅
19. NetPayoutYield.py ✅
20. PayoutYield.py ✅
21. RD.py ✅
22. SP.py ✅
23. VarCF.py ✅
24. ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py ✅
25. ZZ1_EBM_BPEBM.py ✅
26. ZZ1_FR_FRbook.py ✅
27. ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py ✅

### Predictors: Other Uses (10 files)

These use may use mve_permco for filtering other non-scaling purposes. Use `mve_permco` *only* for scaling. Use `mve_c` for other purposes.

28. CBOperProf.py ✅
   - use `mve_permco` for constructing B/M
   - use `mve_c` for filtering for non-missing market equity
29. GrAdExp.py
   - use `mve_c` for monthly size deciles and culling smallest bucket
   - (no scaling use)
30. MS.py
   - use `mve_permco` for computing log B/M (ceq / mve_permco)
   - use `mve_c` for identifying lowest quintile eligible for Mohanram score
31. NetDebtPrice.py
   - use `mve_permco` for scaling net debt (net debt / mve_permco)
   - use `mve_c` for log B/M filter that removes bottom two quintiles
32. OperProf.py
   - use `mve_c` for size-tercile assignment (smallest firms drop out)
   - (profitability ratio itself uses assets, not market equity)
33. OperProfRD.py
   - use `mve_c` as screen to exclude rows missing market equity
   - (ratio is over assets, not market equity)
34. PS.py
   - use `mve_permco` for computing log B/M (ceq / mve_permco)
   - use `mve_c` for highest BM quintile filter
35. RDcap.py
   - use `mve_c` for monthly size tertiles (small-firm restriction)
   - (R&D capital is scaled by assets, not market equity)
37. ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py
   - use `mve_permco` for market-to-book ratio (mve_permco in numerator)
   - use `mve_c` for NYSE/AMEX size breakpoints, logistic RIO transformation, and dropping rows lacking market equity 

### Accounting-Based Placebos 

These use accounting ratios and fundamental data. Replace `mve_c` with `mve_permco`:

1. AMq.py ✅
2. AssetLiquidityMarketQuart.py ✅
3. AssetTurnover_q.py ✅
4. BMq.py ✅
5. BookLeverageQuarterly.py ✅
6. CBOperProfLagAT.py ✅
7. CBOperProfLagAT_q.py ✅
8. CFq.py ✅
9. ChangeRoA.py ✅
10. ChangeRoE.py ✅
11. EBM_q.py ✅
12. EPq.py ✅
13. EntMult_q.py ✅
14. GPlag_q.py ✅
15. KZ.py ✅
16. KZ_q.py ✅
17. Leverage_q.py ✅
18. NetDebtPrice_q.py ✅
19. NetPayoutYield_q.py ✅
20. OPLeverage_q.py ✅
21. OperProfLag.py ✅
22. PS_q.py ✅
23. PayoutYield_q.py ✅
24. RD_q.py ✅
25. RetNOA_q.py ✅
26. SP_q.py ✅
27. Tax_q.py ✅
28. Tax_q_test.py ✅
29. ZScore.py ✅
30. ZScore_q.py ✅
31. cfpq.py ✅
32. sgr_q.py ✅
33. tang_q.py ✅

## Files To Keep As-Is

**Purely Market Price Predictors (5 files)**
These operate at the stock (permno) level and should continue using `mve_c`:
- IndMom.py
- IndRetBig.py
- Size.py
- VolMkt.py
- TrendFactor.py

**Scripts That Filter on mve_c (8 files)**
These use size filters/rankings. For now, keep using `mve_c`:
- ChNAnalyst.py
- CitationsRD.py
- DelBreadth.py
- EarnSupBig.py
- PatentsRD.py
- ProbInformedTrading.py
- std_turn.py
- DivYield.py
- DivYieldAnn.py

**Other**
- CompEquIss.py - measures equity issuance by comparing buy-hold returns with change in market value. Keep using `mve_c`.
- ZZ1_iomom_cust__iomom_supp.R - Uses `mve_c` to compute value-weighted returns. Keep using `mve_c`.



