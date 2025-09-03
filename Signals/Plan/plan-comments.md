# Plan for comments lit references

Update the comments in ONE script as follows:

1. Get the predictor names from the script
    - Most predictors are just what comes before the .py
    - In some cases you need to remove ZZ1_, ZZ2_, and there are multiple predictors in some files
2. Check it the script already has an ABOUTME: top line that states the Author, Year, and Table
    - If it does, mark the script with ✅ and stop.
3. Get context by running `cd pyCode && python3 utils/fetch-doc.py [predictorname]`
    - This will give an overview of what the predictor does    
4. Update the top comments to provide the LongDescription, AuthorYear and Table being replicated 
    - The table appears in the format "Key Table      : [table number] [table panel]"

When complete, mark the predictor below by ✅.

If no script is specified, work on the first incomplete script.

Work on only one script.

## Example:

```python
# ABOUTME: Advertising Expense following Chan, Lakonishok and Sougiannis 2001, Table 7, first year
# ABOUTME: calculates advertising expense predictor scaled by market value of equity
"""
Usage:
    python3 Predictors/AdExp.py

Inputs:
    - m_aCompustat.parquet: Monthly Compustat data with columns [permno, time_avail_m, xad]
    - SignalMasterTable.parquet: Monthly master table with mve_c

Outputs:
    - AdExp.csv: CSV file with columns [permno, yyyymm, AdExp]
    - AdExp = xad/mve_c, set to missing if xad <= 0 (following Table VII)
"""
```

# Progress tracking 

- Accruals.py ✅ 
- AccrualsBM.py ✅ 
- AdExp.py ✅ 
- AgeIPO.py ✅ 
- AM.py ✅ 
- AnalystRevision.py ✅
- AssetGrowth.py ✅
- Beta.py ✅
- BetaLiquidityPS.py ✅
- BetaTailRisk.py ✅
- BidAskSpread.py ✅
- BM.py ✅
- BMdec.py ✅
- BookLeverage.py ✅
- BrandInvest.py ✅
- Cash.py ✅
- CashProd.py ✅
- CBOperProf.py ✅
- CF.py ✅
- cfp.py ✅
- ChangeInRecommendation.py ✅
- ChAssetTurnover.py ✅
- ChEQ.py ✅
- ChForecastAccrual.py ✅
- ChInv.py ✅
- ChInvIA.py ✅
- ChNAnalyst.py ✅
- ChNNCOA.py ✅
- ChNWC.py ✅
- ChTax.py ✅
- CitationsRD.py ✅
- CompEquIss.py ✅
- CompositeDebtIssuance.py ✅
- ConsRecomm.py ✅
- ConvDebt.py ✅
- CoskewACX.py ✅
- Coskewness.py ✅
- CPVolSpread.py ✅
- CredRatDG.py ✅
- CustomerMomentum.py ✅
- dCPVolSpread.py ✅
- DebtIssuance.py ✅
- DelBreadth.py ✅
- DelCOA.py ✅
- DelCOL.py ✅
- DelDRC.py ✅
- DelEqu.py ✅
- DelFINL.py ✅
- DelLTI.py ✅
- DelNetFin.py ✅
- DivInit.py ✅
- DivOmit.py ✅
- DivSeason.py ✅
- DivYieldST.py ✅
- dNoa.py ✅
- DolVol.py ✅
- DownRecomm.py ✅
- dVolCall.py ✅
- dVolPut.py ✅
- EarningsConsistency.py ✅
- EarningsForecastDisparity.py ✅
- EarningsStreak.py ✅
- EarningsSurprise.py ✅
- EarnSupBig.py ✅
- EntMult.py ✅
- EP.py ✅
- EquityDuration.py ✅
- ExchSwitch.py ✅
- ExclExp.py ✅
- FEPS.py ✅
- fgr5yrLag.py ✅
- FirmAge.py ✅
- FirmAgeMom.py ✅
- ForecastDispersion.py ✅
- Frontier.py ✅
- Governance.py ✅
- GP.py ✅
- GrAdExp.py ✅
- GrLTNOA.py ✅
- GrSaleToGrInv.py ✅
- GrSaleToGrOverhead.py ✅
- Herf.py ✅
- HerfAsset.py ✅
- HerfBE.py ✅
- High52.py ✅
- hire.py ✅
- Illiquidity.py ✅
- IndIPO.py ✅
- IndMom.py ✅
- IndRetBig.py ✅
- IntMom.py ✅
- Investment.py ✅
- InvestPPEInv.py ✅
- InvGrowth.py ✅
- IO-ShortInterest.py ✅
- iomom-cust.py ✅
- iomom-supp.py ✅
- Leverage.py ✅
- LRreversal.py ✅
- MaxRet.py ✅
- MeanRankRevGrowth.py ✅
- Mom12m.py ✅
- Mom12mOffSeason.py ✅
- Mom6m.py ✅
- Mom6mJunk.py ✅
- MomOffSeason.py ✅
- MomOffSeason06YrPlus.py ✅
- MomOffSeason11YrPlus.py ✅
- MomOffSeason16YrPlus.py ✅
- MomRev.py ✅
- MomSeason.py ✅
- MomSeason06YrPlus.py ✅
- MomSeason11YrPlus.py ✅
- MomSeason16YrPlus.py ✅
- MomSeasonShort.py ✅
- MomVol.py ✅
- MRreversal.py ✅
- MS.py ✅
- NetDebtFinance.py ✅
- NetDebtPrice.py ✅
- NetEquityFinance.py ✅
- NetPayoutYield.py ✅
- NOA.py ✅
- NumEarnIncrease.py ✅
- OperProf.py ✅
- OperProfRD.py ✅
- OPLeverage.py ✅
- OrderBacklog.py ✅
- OrderBacklogChg.py ✅
- OScore.py ✅
- PatentsRD.py ✅
- PayoutYield.py ✅
- PctAcc.py ✅
- PctTotAcc.py ✅
- Price.py ✅
- ProbInformedTrading.py ✅
- PS.py ✅
- RD.py ✅
- RDAbility.py ✅
- RDcap.py ✅
- RDIPO.py ✅
- RDS.py ✅
- realestate.py ✅
- Recomm-ShortInterest.py ✅ (file is actually Recomm_ShortInterest.py)
- retConglomerate.py ✅
- ReturnSkew.py ✅
- REV6.py ✅
- RevenueSurprise.py ✅
- roaq.py ✅
- RoE.py ✅
- sfe.py ✅
- ShareIss1Y.py ✅
- ShareIss5Y.py ✅
- ShareRepurchase.py ✅
- ShareVol.py ✅
- ShortInterest.py ✅
- sinAlgo.py ✅
- Size.py ✅
- skew1.py ✅
- SmileSlope.py ✅
- SP.py ✅
- Spinoff.py ✅
- std-turn.py ✅
- STreversal.py ✅
- SurpriseRD.py ✅
- tang.py ✅
- Tax.py ✅
- TotalAccruals.py ✅
- TrendFactor.py ✅
- UpRecomm.py ✅
- VarCF.py ✅
- VolMkt.py ✅
- VolSD.py ✅
- VolumeTrend.py ✅
- XFIN.py ✅
- ZZ0-RealizedVol-IdioVol3F-ReturnSkew3F.py ✅
- ZZ1-Activism1-Activism2.py ✅
- ZZ1-AnalystValue-AOP-PredictedFE-IntrinsicValue.py ✅
- ZZ1-EBM-BPEBM.py ✅
- ZZ1-FR-FRbook.py ✅
- ZZ1-grcapx-grcapx1y-grcapx3y.py ✅
- ZZ1-IntanBM-IntanSP-IntanCFP-IntanEP.py ✅
- ZZ1-OptionVolume1-OptionVolume2.py ✅
- ZZ1-OrgCap-OrgCapNoAdj.py ✅
- ZZ1-ResidualMomentum6m-ResidualMomentum.py ✅
- ZZ1-RIO-MB-RIO-Disp-RIO-Turnover-RIO-Volatility.py ✅
- ZZ1-RIVolSpread.py ✅
- ZZ1-zerotrade-zerotradeAlt1-zerotradeAlt12.py ✅
- ZZ2-AbnormalAccruals-AbnormalAccrualsPercent.py ✅
- ZZ2-AnnouncementReturn.py ✅
- ZZ2-BetaFP.py ✅
- ZZ2-betaVIX.py ✅
- ZZ2-IdioVolAHT.py ✅
- ZZ2-PriceDelaySlope-PriceDelayRsq-PriceDelayTstat.py ✅