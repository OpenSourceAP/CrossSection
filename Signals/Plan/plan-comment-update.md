# Plan for updating comments

Update the comments in ONE DataDownloads script as follows:

1. Delete all comments, including shebangs
2. Create a top comment with the two ABOUTME: lines and the standard """[input][output][how to run]""" comment
    - Example: 
    ```
    # ABOUTME: Downloads and processes Compustat short interest data, combining legacy and new sources
    # ABOUTME: Joins with CCMLinkingTable to add permno and aggregates to monthly permno-level data
    """
    Inputs:
    - comp.sec_shortint_legacy (1973-2024)
    - comp.sec_shortint (2006+)
    - ../pyData/Intermediate/CCMLinkingTable.parquet

    Outputs:
    - ../pyData/Intermediate/monthlyShortInterest.parquet

    How to run: python3 G_CompustatShortInterest.py
    """
3. Add comments that describe clearly what each block of code does

When complete, mark the script below by ✅.

If no script is specified, work on the first TBC script.

# Progress tracking 

- A_CCMLinkingTable.py ✅
- B_CompustatAnnual.py: TBC
- C_CompustatQuarterly.py: TBC
- D_CompustatPensions.py: TBC
- E_CompustatBusinessSegments.py: TBC
- F_CompustatCustomerSegments.py: TBC
- G_CompustatShortInterest.py ✅
- H_CRSPDistributions.py: TBC
- I_CRSPmonthly.py: TBC
- I2_CRSPmonthlyraw.py: TBC
- J_CRSPdaily.py: TBC
- K_CRSPAcquisitions.py: TBC
- L_IBES_EPS_Unadj.py: TBC
- L2_IBES_EPS_Adj.py: TBC
- M_IBES_Recommendations.py: TBC
- N_IBES_UnadjustedActuals.py: TBC
- O_Daily_Fama-French.py: TBC
- P_Monthly_Fama-French.py: TBC
- Q_MarketReturns.py: TBC
- R_MonthlyLiquidityFactor.py: TBC
- S_QFactorModel.py: TBC
- T_VIX.py: TBC
- U_GNPDeflator.py: TBC
- V_TBill3M.py: TBC
- W_BrokerDealerLeverage.py: TBC
- X_SPCreditRatings.py: TBC
- X2_CIQCreditRatings.py: TBC
- ZA_IPODates.py: TBC
- ZB_PIN.py: TBC
- ZC_GovernanceIndex.py: TBC
- ZD_CorwinSchultz.py: TBC
- ZE_13F.py: TBC
- ZF_CRSPIBESLink.py: TBC
- ZG_BidaskTAQ.py: TBC
- ZH_OptionMetricsCleaning.py: TBC
- ZH2_OptionMetricsCRSPLink.py: TBC
- ZI_PatentCitations.py: TBC
- ZJ_InputOutputMomentum.py: TBC
- ZK_CustomerMomentum.py: TBC