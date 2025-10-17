# Plan for updating signals to use mve_permco

2025-10-17 Andrew Chen

## Problem Summary

Issue #167 describes a problem where the current code fails to aggregate market equity across multiple stock identifiers (permnos) within the same company (permco). While multi-permno companies represent only ~1% of securities, they account for ~4% of total market capitalization.

We fixed this issue in commit 68d6ce5. However, in the previous fix (commit 68d6ce5), we did not carefully track deviations of the output from the legacy Stata code. We rolled back and ensured we knew when the Stata replication was complete (see https://github.com/OpenSourceAP/CrossSection/issues/174) and then started to address the current Github issues that. The goal here is just to re-apply and check again, being more aware of how we are deviating from Stata. 

## Current State

Looking at the current code:
- `Signals/pyCode/DataDownloads/CRSPMonthly.py` only creates `mve_c` (no `mve_permco`)
- `Signals/pyCode/SignalMasterTable.py` only loads `mve_c` (no `mve_permco`)
- All predictors use `mve_c`

The old code from commit 68d6ce5:
- `I_CRSPmonthly.py` created both `mve_c` and `mve_permco`
- `SignalMasterTable.py` loaded both variables
- Accounting-based predictors were updated to use `mve_permco`

## Files That Need To Be Changed

### Step 0: Remove mve_c references from specific files (5 files) ✅

These files should have references to `mve_c` removed FIRST, before any other changes:

1. **Signals/pyCode/Predictors/Governance.py** - Remove `mve_c` references ✅
2. **Signals/pyCode/Predictors/RevenueSurprise.py** - Remove `mve_c` references ✅
3. **Signals/pyCode/Predictors/ZZ1_Activism1_Activism2.py** - Remove `mve_c` references ✅
4. **Signals/pyCode/Predictors/sfe.py** - Remove `mve_c` references ✅

### Core Data Processing and Testing (3 files) ✅

6. **Signals/pyCode/DataDownloads/CRSPMonthly.py**
   - Add calculation of `mve_permco` after line 105 (after creating `mve_c`)
   - Aggregate `mve_c` by `permco` and `time_avail_m` to create `mve_permco`
   - Keep `permco` in the dataset (currently dropped at line 108)
   - Merge `mve_permco` back to main dataset

7. **Signals/pyCode/SignalMasterTable.py**
   - Update line 26 to include `mve_permco` in the columns list
   - Update line 127 to include `mve_permco` in the reordered columns (it's already there but commented as "commonly used crsp variables")

8. Test by updating BM.py to use mve_permco
   - Hand check result


### Accounting-Based Predictors (31 files)

These use accounting ratios and fundamental data. Replace `mve_c` with `mve_permco`:

8. AccrualsBM.py ✅
9. AdExp.py ✅
10. AM.py ✅
12. CashProd.py ✅
13. CBOperProf.py ✅
14. CF.py ✅
15. cfp.py ✅
16. DebtIssuance.py ✅
17. EntMult.py ✅
18. EP.py ✅
19. GrAdExp.py ✅
20. Leverage.py ✅
21. MS.py ✅
22. NetDebtPrice.py ✅
23. NetPayoutYield.py ✅
24. OperProf.py ✅
25. OperProfRD.py ✅
26. PayoutYield.py ✅
27. PS.py ✅
28. RD.py ✅
29. RDcap.py ✅
30. roaq.py ✅
31. SP.py ✅
32. VarCF.py ✅
33. ZZ1_EBM_BPEBM.py ✅
34. ZZ1_FR_FRbook.py ✅
35. ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py ✅
36. ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py ✅
37. ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py ✅
38. Frontier.py ✅

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
- ZZ1_iomom_cust__iomom_supp.R - Uses `mve_c` to compute value-weighted returns. Unclear what is ideal so we keep it as is to match OP.



