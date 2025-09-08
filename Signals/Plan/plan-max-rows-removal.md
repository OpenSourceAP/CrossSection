# Plan to remove MAX_ROWS_DL from fast download scripts

In many of the `pyCode/DataDownloads/*.py` scripts, we have code like
```
# Add row limit for debugging if configured
if MAX_ROWS_DL > 0:
    QUERY += f" LIMIT {MAX_ROWS_DL}"
    print(f"DEBUG MODE: Limiting to {MAX_ROWS_DL} rows", flush=True)
```

This is not needed for many scripts that are fast to download.

# Task

For a given script, 
1. Remove the MAX_ROWS_DL code. 
2. Run the script to make sure it works.
3. Update the progress tracking below.
    - Mark with ✅ if the MAX_ROWS_DL code is removed and the script works.

# Progress tracking

The following scripts are fast:

- V_TBill3M.py
- U_GNPDeflator.py
- W_BrokerDealerLeverage.py
- T_VIX.py
- S_QFactorModel.py
- R_MonthlyLiquidityFactor.py
- Q_MarketReturns.py
- P_Monthly_Fama-French.py
- O_Daily_Fama-French.py
- ZA_IPODates.py
- A_CCMLinkingTable.py
- ZH2_OptionMetricsCRSPLink.py
- D_CompustatPensions.py
- ZG_BidaskTAQ.py
- ZF_CRSPIBESLink.py
- ZD_CorwinSchultz.py
- K_CRSPAcquisitions.py
- ZH_OptionMetricsCleaning.py
- ZC_GovernanceIndex.py
- M_IBES_Recommendations.py
- X_SPCreditRatings.py
- F_CompustatCustomerSegments.py
- H_CRSPDistributions.py
- ZK_CustomerMomentum.py
- E_CompustatBusinessSegments.py
- ZE_13F.py