# Plan for removing comments referring to Stata code

Update the comments in ONE script as follows:

1. Get the predictor names from the script
    - Most predictors are just what comes before the .py
    - In some cases you need to remove ZZ1_, ZZ2_, and there are multiple predictors in some files
2. Remove all references to Stata code. 
    - For example, remove
        ```
        # gen AccrualsBM = 1 if tempqBM == 5 & tempqAcc == 1
        # replace AccrualsBM = 0 if tempqBM == 1 & tempqAcc == 5
        # replace AccrualsBM = . if ceq <0
        ```
    - Also remove:
        ```
        # Following exact Stata logic: ONLY tempqBM==1 AND tempqAcc==5  
        ```

3. Replace with natural language the computational mechanics in the code

When complete, mark the predictor below by ✅.

If no predictor is specified, work on the first incomplete predictor.

Work on only one predictor at a time.

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
- BookLeverage.py
- BrandInvest.py
- Cash.py
- CashProd.py
- CBOperProf.py
- CF.py
- cfp.py
- ChangeInRecommendation.py
- ChAssetTurnover.py
- ChEQ.py
- ChForecastAccrual.py
- ChInv.py
- ChInvIA.py
- ChNAnalyst.py
- ChNNCOA.py
- ChNWC.py
- ChTax.py
- CitationsRD.py
- CompEquIss.py
- CompositeDebtIssuance.py
- ConsRecomm.py
- ConvDebt.py
- CoskewACX.py
- Coskewness.py
- CPVolSpread.py
- CredRatDG.py
- CustomerMomentum.py
- dCPVolSpread.py
- DebtIssuance.py
- DelBreadth.py
- DelCOA.py
- DelCOL.py
- DelDRC.py
- DelEqu.py
- DelFINL.py
- DelLTI.py
- DelNetFin.py
- DivInit.py
- DivOmit.py
- DivSeason.py
- DivYieldST.py
- dNoa.py
- DolVol.py
- DownRecomm.py
- dVolCall.py
- dVolPut.py
- EarningsConsistency.py
- EarningsForecastDisparity.py
- EarningsStreak.py
- EarningsSurprise.py
- EarnSupBig.py
- EntMult.py
- EP.py
- EquityDuration.py
- ExchSwitch.py
- ExclExp.py
- FEPS.py
- fgr5yrLag.py
- FirmAge.py
- FirmAgeMom.py
- ForecastDispersion.py
- Frontier.py
- Governance.py
- GP.py
- GrAdExp.py
- GrLTNOA.py
- GrSaleToGrInv.py
- GrSaleToGrOverhead.py
- Herf.py
- HerfAsset.py
- HerfBE.py
- High52.py
- hire.py
- Illiquidity.py
- IndIPO.py
- IndMom.py
- IndRetBig.py
- IntMom.py
- Investment.py
- InvestPPEInv.py
- InvGrowth.py
- IO-ShortInterest.py
- iomom-cust.py
- iomom-supp.py
- Leverage.py
- LRreversal.py
- MaxRet.py
- MeanRankRevGrowth.py
- Mom12m.py
- Mom12mOffSeason.py
- Mom6m.py
- Mom6mJunk.py
- MomOffSeason.py
- MomOffSeason06YrPlus.py
- MomOffSeason11YrPlus.py
- MomOffSeason16YrPlus.py
- MomRev.py
- MomSeason.py
- MomSeason06YrPlus.py
- MomSeason11YrPlus.py
- MomSeason16YrPlus.py
- MomSeasonShort.py
- MomVol.py
- MRreversal.py
- MS.py
- NetDebtFinance.py
- NetDebtPrice.py
- NetEquityFinance.py
- NetPayoutYield.py
- NOA.py
- NumEarnIncrease.py
- OperProf.py
- OperProfRD.py
- OPLeverage.py
- OrderBacklog.py
- OrderBacklogChg.py
- OScore.py
- PatentsRD.py
- PayoutYield.py
- PctAcc.py
- PctTotAcc.py
- Price.py
- ProbInformedTrading.py
- PS.py
- RD.py
- RDAbility.py
- RDcap.py
- RDIPO.py
- RDS.py
- realestate.py
- Recomm-ShortInterest.py
- retConglomerate.py
- ReturnSkew.py
- REV6.py
- RevenueSurprise.py
- roaq.py
- RoE.py
- sfe.py
- ShareIss1Y.py
- ShareIss5Y.py
- ShareRepurchase.py
- ShareVol.py
- ShortInterest.py
- sinAlgo.py
- Size.py
- skew1.py
- SmileSlope.py
- SP.py
- Spinoff.py
- std-turn.py
- STreversal.py
- SurpriseRD.py
- tang.py
- Tax.py
- TotalAccruals.py
- TrendFactor.py
- UpRecomm.py
- VarCF.py
- VolMkt.py
- VolSD.py
- VolumeTrend.py
- XFIN.py
- ZZ0-RealizedVol-IdioVol3F-ReturnSkew3F.py
- ZZ1-Activism1-Activism2.py
- ZZ1-AnalystValue-AOP-PredictedFE-IntrinsicValue.py
- ZZ1-EBM-BPEBM.py
- ZZ1-FR-FRbook.py
- ZZ1-grcapx-grcapx1y-grcapx3y.py
- ZZ1-IntanBM-IntanSP-IntanCFP-IntanEP.py
- ZZ1-OptionVolume1-OptionVolume2.py
- ZZ1-OrgCap-OrgCapNoAdj.py
- ZZ1-ResidualMomentum6m-ResidualMomentum.py
- ZZ1-RIO-MB-RIO-Disp-RIO-Turnover-RIO-Volatility.py
- ZZ1-RIVolSpread.py
- ZZ1-zerotrade-zerotradeAlt1-zerotradeAlt12.py
- ZZ2-AbnormalAccruals-AbnormalAccrualsPercent.py
- ZZ2-AnnouncementReturn.py
- ZZ2-BetaFP.py
- ZZ2-betaVIX.py
- ZZ2-IdioVolAHT.py
- ZZ2-PriceDelaySlope-PriceDelayRsq-PriceDelayTstat.py