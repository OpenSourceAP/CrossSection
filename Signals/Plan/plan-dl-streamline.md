# Plan for streamlining DataDownloads/*.py

Some files are excessively long and complicated.

## Task for a given script

1. Think about how to reduce the number of lines of code
2. Implement the changes
3. Test the script
    - Run `utils/sum_dl.py [script_name]` to get new summary statistics
    - Compare the new summary statistics with `Logs/from-0908/sumout_dl_[script_name].md`
4. If the new summary statistics are different, try to fix it.
5. Report the results below.
    - mark with ✅ if the script is simplified and the summary statistics are IDENTICAL to the original
    - If the summary statistics are NOT IDENTICAL, mark with 🤔 and describe the differences
    - **IMPORTANT**: DO NOT mark with ✅ if the summary statistics are NOT IDENTICAL

If no script is specified, work on the first TBC script.

## Progress Tracking

1. A_CCMLinkingTable.py: ✅ COMPLETED
   - 91 lines → 67 lines (26% reduction)
   - Summary statistics IDENTICAL to original
2. B_CompustatAnnual.py: ✅ COMPLETED
   - 149 lines → 108 lines (28% reduction)
   - Summary statistics IDENTICAL to original 
3. C_CompustatQuarterly.py: ✅ COMPLETED
   - 181 lines → 130 lines (28% reduction)
   - Summary statistics IDENTICAL to original 
4. D_CompustatPensions.py: TBC
   - 93 lines 
5. E_CompustatBusinessSegments.py: SKIP
   - 83 lines
   - Slow, will need custom streamlining
6. F_CompustatCustomerSegments.py: TBC
   - 74 lines
7. G_CompustatShortInterest.py: TBC
   - 215 lines 
8. H_CRSPDistributions.py: TBC
   - 106 lines
9. I2_CRSPmonthlyraw.py: TBC
   - 97 lines
10. I_CRSPmonthly.py: TBC
    - 143 lines
11. J_CRSPdaily.py: TBC
    - 133 lines
12. K_CRSPAcquisitions.py: TBC
    - 99 lines
13. L2_IBES_EPS_Adj.py: TBC
    - 81 lines
14. L_IBES_EPS_Unadj.py: TBC
    - 93 lines
15. M_IBES_Recommendations.py: TBC
    - 95 lines
16. N_IBES_UnadjustedActuals.py
    - 133 lines
17. O_Daily_Fama-French.py: TBC
    - 63 lines
18. P_Monthly_Fama-French.py: TBC
    - 58 lines
19. Q_MarketReturns.py: TBC
    - 63 lines
20. R_MonthlyLiquidityFactor.py: TBC
    - 63 lines
21. S_QFactorModel.py: TBC
    - 116 lines
22. T_VIX.py: TBC
    - 193 lines
23. U_GNPDeflator.py: TBC
    - 193 lines
24. V_TBill3M.py: TBC
    - 115 lines
25. W_BrokerDealerLeverage.py: TBC
    - 178 lines
26. X2_CIQCreditRatings.py: SKIP
    - 233 lines
    - Slow, will need custom streamlining
27. X_SPCreditRatings.py: TBC
    - 109 lines
28. ZA_IPODates.py: TBC
    - 150 lines
29. ZB_PIN.py: SKIP
    - 208 lines
    - Requires unzipping, will need custom streamlining
30. ZC_GovernanceIndex.py: TBC
    - 175 lines
31. ZD_CorwinSchultz.py: TBC
    - 80 lines
32. ZE_13F.py: SKIP
    - 125 lines
    - Slow, will need custom streamlining
33. ZF_CRSPIBESLink.py: TBC
    - 82 lines
34. ZG_BidaskTAQ.py: TBC
    - 78 lines
35. ZH2_OptionMetricsCRSPLink.py: TBC
    - 93 lines
36. ZH_OptionMetricsCleaning.py SKIP
    - Needs custom streamlining. Likely will delete the whole thing and move the logic downstream.
37. ZI_PatentCitations.py: SKIP
    - 258 lines
    - Requires unzipping many files, will need custom streamlining
38. ZJ_InputOutputMomentum.py: SKIP
    - 258 lines
    - This interacts with B_CompustatAnnual.py and I_CRSPmonthly.py
    - We ultimately want to move this to `pyCode/Predictors/`