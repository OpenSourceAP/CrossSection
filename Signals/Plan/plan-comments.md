# Plan for comments

We're done matching the Stata results. So let's remove the comments referring to the Stata code and replace them with comments that:
1. Describe the computational mechanics. 
2. Provide the LongDescription, AuthorYear and Table being replicated at the very top (ABOUTME: ...)

To get info for 2, run `cd pyCode && python3 utils/fetch-doc.py [signalname]`

# Progress tracking

If the subsection is marked with ✅, all predictors in the subsection are complete.

## momentum ✅

- FirmAgeMom
- High52
- IndMom
- IntMom
- Mom12m
- Mom6m
- Mom6mJunk
- MomRev
- MomVol
- ResidualMomentum
- TrendFactor

## R&D ✅

- AdExp
- OrgCap
- RD
- RDIPO
- SurpriseRD

## accruals ✅

- AbnormalAccruals
- Accruals
- OrderBacklogChg
- PctAcc
- PctTotAcc

## asset composition

- Cash
- NOA
- RDcap
- realestate
- tang

## cash flow risk

- VarCF

## composite accounting

- ExclExp
- FR
- MS
- PS
- RDS

## default risk

- OScore

## earnings event

- AnnouncementReturn
- ChNAnalyst

## earnings forecast

- AnalystRevision
- ChForecastAccrual
- DownRecomm
- EarningsForecastDisparity
- PredictedFE
- REV6
- UpRecomm
- fgr5yrLag

## earnings growth

- EarningsConsistency
- EarningsStreak
- EarningsSurprise
- NumEarnIncrease

## external financing

- CompEquIss
- CompositeDebtIssuance
- ConvDebt
- DebtIssuance
- DelCOL
- DelFINL
- IndIPO
- NetDebtFinance
- NetEquityFinance
- ShareIss1Y
- ShareIss5Y
- XFIN

## info proxy

- FirmAge

## informed trading

- dCPVolSpread
- dVolCall
- dVolPut

## investment

- AssetGrowth
- ChEQ
- DelEqu
- DelLTI
- GrLTNOA
- InvestPPEInv
- Investment
- dNoa

## investment alt

- BrandInvest
- ChInv
- ChNNCOA
- ChNWC
- DelCOA
- DelDRC
- DelNetFin
- GrAdExp
- TotalAccruals
- hire

## investment growth

- ChInvIA
- grcapx
- grcapx3y

## lead lag

- CustomerMomentum
- EarnSupBig
- IndRetBig
- PriceDelayRsq
- PriceDelaySlope
- PriceDelayTstat
- iomom_cust
- iomom_supp
- retConglomerate

## leverage

- BPEBM
- BookLeverage
- Leverage
- NetDebtPrice

## liquidity

- BetaLiquidityPS
- BidAskSpread
- Illiquidity
- ProbInformedTrading
- VolSD
- std_turn
- zerotrade12M
- zerotrade1M
- zerotrade6M

## long term reversal

- IntanBM
- IntanCFP
- IntanEP
- IntanSP
- LRreversal
- MRreversal

## optionrisk

- CPVolSpread
- RIVolSpread
- SmileSlope
- skew1

## other

- AOP
- Activism1
- AgeIPO
- BetaFP
- ChTax
- CredRatDG
- ExchSwitch
- Governance
- Herf
- HerfAsset
- HerfBE
- Mom12mOffSeason
- MomOffSeason
- MomOffSeason06YrPlus
- MomOffSeason11YrPlus
- MomOffSeason16YrPlus
- MomSeason
- MomSeason06YrPlus
- MomSeason11YrPlus
- MomSeason16YrPlus
- MomSeasonShort
- OPLeverage
- Price
- RDAbility
- Spinoff
- Tax
- sinAlgo

## ownership

- Activism2
- DelBreadth
- IO_ShortInterest

## payout indicator

- DivInit
- DivOmit
- DivSeason
- ShareRepurchase

## profitability

- CBOperProf
- FEPS
- GP
- InvGrowth
- OperProf
- OperProfRD
- RoE
- roaq

## profitability alt

- CashProd
- CitationsRD
- PatentsRD

## recommendation

- ChangeInRecommendation
- ConsRecomm
- Recomm_ShortInterest

## risk

- Beta
- BetaTailRisk
- CoskewACX
- Coskewness
- ReturnSkew
- ReturnSkew3F

## sales growth

- ChAssetTurnover
- GrSaleToGrInv
- GrSaleToGrOverhead
- MeanRankRevGrowth
- OrderBacklog
- RevenueSurprise

## short sale constraints

- RIO_Disp
- RIO_MB
- RIO_Turnover
- RIO_Volatility
- ShortInterest

## short-term reversal

- STreversal

## size

- Size

## valuation

- AM
- AccrualsBM
- AnalystValue
- BM
- BMdec
- CF
- DivYieldST
- EBM
- EP
- EntMult
- EquityDuration
- Frontier
- NetPayoutYield
- PayoutYield
- SP
- cfp
- sfe

## volatility

- ForecastDispersion
- IdioVol3F
- IdioVolAHT
- MaxRet
- RealizedVol
- betaVIX

## volume

- DolVol
- OptionVolume1
- OptionVolume2
- ShareVol
- VolMkt
- VolumeTrend
```

Do you also want me to collapse this further into just **categories with predictor counts** (e.g. `## R&D (5 predictors)`), or keep the flat list of predictor names like above?
