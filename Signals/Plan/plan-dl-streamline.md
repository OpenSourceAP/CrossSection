# Plan for streamlining Predictors/*.py

Some files are excessively long and complicated.

## Task for a given script

1. Extract the dataset outputs from the script
2. Run `utils/test_dl.py --datasets [dataset_names] --skipcheck --outputname testout_dl_cur` to get the current test results
3. Implement the changes
4. Run the script
5. Run `utils/test_dl.py --datasets [dataset_names] --skipcheck --outputname testout_dl_new` to get the new test results
6. If the test results are different, think about how to fix it.
7. Report the results below.
    - mark with ✅ if the script is simplified and the test results are at least as good as the original

## Progress Tracking

- ✅ ZH2_OptionMetricsCleaning.py - Simplified from 140 to 57 lines (59% reduction). Removed unused function, eliminated redundant logic, consolidated file operations. All tests pass with identical results.

## DataDownloads Scripts Analysis

### Scripts by Size (lines of code)
1. **ZK_CustomerMomentum.py** - 348 lines ⚠️ HIGH PRIORITY
2. **ZI_PatentCitations.py** - 258 lines ⚠️ HIGH PRIORITY  
3. **C_CompustatQuarterly.py** - 258 lines ⚠️ HIGH PRIORITY
4. **X2_CIQCreditRatings.py** - 233 lines ⚠️ HIGH PRIORITY
5. **B_CompustatAnnual.py** - 232 lines ⚠️ HIGH PRIORITY
6. **G_CompustatShortInterest.py** - 215 lines ⚠️ HIGH PRIORITY
7. **ZB_PIN.py** - 208 lines
8. **U_GNPDeflator.py** - 193 lines
9. **T_VIX.py** - 193 lines
10. **W_BrokerDealerLeverage.py** - 178 lines
11. **ZC_GovernanceIndex.py** - 175 lines
12. **ZA_IPODates.py** - 150 lines
13. **I_CRSPmonthly.py** - 143 lines
14. **ZJ_InputOutputMomentum.py** - 135 lines
15. **N_IBES_UnadjustedActuals.py** - 133 lines
16. **J_CRSPdaily.py** - 133 lines
17. **ZE_13F.py** - 125 lines
18. **S_QFactorModel.py** - 116 lines
19. **V_TBill3M.py** - 115 lines
20. **X_SPCreditRatings.py** - 109 lines
21. **H_CRSPDistributions.py** - 106 lines
22. **K_CRSPAcquisitions.py** - 99 lines
23. **I2_CRSPmonthlyraw.py** - 97 lines
24. **D_CompustatPensions.py** - 97 lines
25. **M_IBES_Recommendations.py** - 95 lines
26. **ZH2_OptionMetricsCRSPLink.py** - 93 lines
27. **L_IBES_EPS_Unadj.py** - 93 lines
28. **A_CCMLinkingTable.py** - 91 lines
29. **E_CompustatBusinessSegments.py** - 83 lines
30. **ZF_CRSPIBESLink.py** - 82 lines
31. **L2_IBES_EPS_Adj.py** - 81 lines
32. **ZD_CorwinSchultz.py** - 80 lines
33. **ZG_BidaskTAQ.py** - 78 lines
34. **F_CompustatCustomerSegments.py** - 74 lines
35. **R_MonthlyLiquidityFactor.py** - 63 lines
36. **Q_MarketReturns.py** - 63 lines
37. **O_Daily_Fama-French.py** - 63 lines
38. **P_Monthly_Fama-French.py** - 58 lines
39. **ZH_OptionMetricsCleaning.py** - 57 lines ✅ COMPLETED

### Streamlining Priority List
**Top Priority (200+ lines, good candidates):**
- ZK_CustomerMomentum.py (348 lines) - Single function, likely has redundant code
- ZI_PatentCitations.py (258 lines) - Only 2 functions, potential for consolidation
- C_CompustatQuarterly.py (258 lines) - No functions, all inline code
- X2_CIQCreditRatings.py (233 lines) - Single function structure
- B_CompustatAnnual.py (232 lines) - No functions, all inline code  
- G_CompustatShortInterest.py (215 lines) - Likely has repetitive patterns

**Medium Priority (150-200 lines):**
- ZB_PIN.py, U_GNPDeflator.py, T_VIX.py, W_BrokerDealerLeverage.py, ZC_GovernanceIndex.py

**Low Priority (<150 lines):**
- Already reasonably concise, but can review if time permits