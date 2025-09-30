# Plan for comments lit references

Update the comments in ONE script as follows:

1. If the top comment does not match the example, replace it with a comment follows the example:

Example:
```python
# ABOUTME: Accruals following Sloan 1996, Table 6, year t+1
# ABOUTME: calculates working capital accruals predictor scaled by average total assets

"""
Accruals.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/
    python3 Predictors/Accruals.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [gvkey, permno, time_avail_m, txp, act, che, lct, dlc, at, dp]

Outputs:
    - Accruals.csv: CSV file with columns [permno, yyyymm, Accruals]
"""
```

2. Remove unneeded whitespace from the top comment.
3. Mark the script with ✅.

If no script is specified, work on the first script without ✅.


# Progress tracking 

Accruals.py ✅
AccrualsBM.py ✅
AdExp.py ✅
AgeIPO.py ✅ 
AM.py ✅ 
AnalystRevision.py ✅ 
AssetGrowth.py ✅ 
Beta.py ✅ 
BetaLiquidityPS.py ✅ 
BetaTailRisk.py ✅ 
BidAskSpread.py ✅
BM.py ✅ 
BMdec.py ✅ 
BookLeverage.py ✅ 
BrandInvest.py ✅ 
Cash.py ✅ 
CashProd.py ✅ 
CBOperProf.py ✅
CF.py ✅ 
cfp.py ✅ 
ChangeInRecommendation.py ✅ 
ChAssetTurnover.py ✅ 
ChEQ.py ✅ 
ChForecastAccrual.py ✅ 
ChInv.py ✅ 
ChInvIA.py ✅ 
ChNAnalyst.py ✅ 
ChNNCOA.py ✅ 
ChNWC.py ✅
ChTax.py ✅
CitationsRD.py ✅ 
CompEquIss.py ✅ 
CompositeDebtIssuance.py ✅ 
ConsRecomm.py ✅ 
ConvDebt.py ✅ 
CoskewACX.py ✅ 
Coskewness.py ✅ 
CPVolSpread.py ✅
CredRatDG.py ✅ 
CustomerMomentum.py ✅ 
dCPVolSpread.py ✅
DebtIssuance.py ✅
DelBreadth.py ✅ 
DelCOA.py ✅ 
DelCOL.py ✅ 
DelDRC.py ✅ 
DelEqu.py ✅ 
DelFINL.py ✅ 
DelLTI.py ✅ 
DelNetFin.py ✅ 
DivInit.py ✅ 
DivOmit.py ✅ 
DivSeason.py ✅ 
DivYieldST.py ✅ 
dNoa.py ✅ 
DolVol.py ✅ 
DownRecomm.py ✅ 
dVolCall.py ✅
dVolPut.py ✅
EarningsConsistency.py ✅ 
EarningsForecastDisparity.py ✅ 
EarningsStreak.py ✅ 
EarningsSurprise.py ✅ 
EarnSupBig.py ✅ 
EntMult.py ✅ 
EP.py ✅
EquityDuration.py ✅
ExchSwitch.py ✅
ExclExp.py ✅ 
FEPS.py ✅ 
fgr5yrLag.py ✅
FirmAge.py ✅
FirmAgeMom.py ✅
ForecastDispersion.py ✅
Frontier.py ✅
Governance.py ✅
GP.py ✅
GrAdExp.py ✅
GrLTNOA.py ✅
GrSaleToGrInv.py ✅
GrSaleToGrOverhead.py ✅
Herf.py ✅
HerfAsset.py ✅
HerfBE.py ✅
High52.py ✅
hire.py ✅
Illiquidity.py ✅
IndIPO.py ✅
IndMom.py ✅
IndRetBig.py ✅
IntMom.py ✅
Investment.py ✅
InvestPPEInv.py ✅
InvGrowth.py ✅
IO_ShortInterest.py ✅
Leverage.py ✅
LRreversal.py ✅
MaxRet.py ✅
MeanRankRevGrowth.py ✅
Mom12m.py ✅
Mom12mOffSeason.py ✅
Mom6m.py ✅
Mom6mJunk.py ✅
MomOffSeason.py ✅
MomOffSeason06YrPlus.py ✅
MomOffSeason11YrPlus.py ✅
MomOffSeason16YrPlus.py ✅
MomRev.py ✅
MomSeason.py ✅
MomSeason06YrPlus.py ✅
MomSeason11YrPlus.py ✅
MomSeason16YrPlus.py ✅
MomSeasonShort.py ✅
MomVol.py ✅
MRreversal.py ✅
MS.py ✅
NetDebtFinance.py ✅
NetDebtPrice.py ✅
NetEquityFinance.py ✅
NetPayoutYield.py ✅
NOA.py ✅
NumEarnIncrease.py ✅
OperProf.py ✅
OperProfRD.py ✅
OPLeverage.py ✅
OrderBacklog.py ✅
OrderBacklogChg.py ✅
OScore.py ✅
PatentsRD.py ✅
PayoutYield.py ✅
PctAcc.py ✅
PctTotAcc.py ✅
Price.py ✅
ProbInformedTrading.py ✅
PS.py ✅
RD.py ✅
RDAbility.py ✅
RDcap.py ✅
RDIPO.py ✅
RDS.py ✅
realestate.py ✅
Recomm_ShortInterest.py ✅
retConglomerate.py ✅
ReturnSkew.py ✅
REV6.py ✅
RevenueSurprise.py ✅
roaq.py ✅
RoE.py ✅
sfe.py ✅
ShareIss1Y.py ✅
ShareIss5Y.py ✅
ShareRepurchase.py ✅
ShareVol.py ✅
ShortInterest.py ✅
sinAlgo.py ✅
Size.py ✅
skew1.py ✅
SmileSlope.py ✅
SP.py ✅
Spinoff.py ✅
std_turn.py ✅
STreversal.py ✅
SurpriseRD.py ✅
tang.py ✅
Tax.py ✅
TotalAccruals.py ✅
TrendFactor.py ✅
UpRecomm.py ✅
VarCF.py ✅
VolMkt.py ✅
VolSD.py ✅
VolumeTrend.py ✅
XFIN.py ✅
ZZ0_RealizedVol_IdioVol3F_ReturnSkew3F.py ✅
ZZ1_Activism1_Activism2.py ✅
ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py ✅
ZZ1_EBM_BPEBM.py ✅
ZZ1_FR_FRbook.py ✅
ZZ1_grcapx_grcapx1y_grcapx3y.py ✅
ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py ✅
ZZ1_iomom_cust__iomom_supp.py ✅
ZZ1_OptionVolume1_OptionVolume2.py ✅
ZZ1_OrgCap_OrgCapNoAdj.py ✅
ZZ1_ResidualMomentum6m_ResidualMomentum.py ✅
ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py ✅
ZZ1_RIVolSpread.py ✅
ZZ1_zerotrade_zerotradeAlt1_zerotradeAlt12.py ✅
ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py ✅
ZZ2_AnnouncementReturn.py ✅
ZZ2_BetaFP.py ✅
ZZ2_betaVIX.py ✅
ZZ2_IdioVolAHT.py ✅
ZZ2_PriceDelaySlope_PriceDelayRsq_PriceDelayTstat.py ✅