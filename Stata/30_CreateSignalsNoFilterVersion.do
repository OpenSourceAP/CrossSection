timer clear
timer on 1


********************
** Create factors **
********************
/* This file creates all factors used in the paper (unless they had to be
   created earlier (e.g. monthly measures from daily stock file)) from 
   the merged dataset
   
   Takes about 3-4 hours
   
   OUTPUT: 
    AnomaliesAll.dta 
	SignalFirmMonth.csv
    SignalFirmMonthMetaData.csv   
*/

u "$pathProject/DataClean/m_MergedData", clear
xtset permno time_avail_m
gen sicCS   = sic
replace sic = sicCRSP

* Converting units
replace shrout = shrout/1000
replace vol =  vol/10^4

* common variables
gen mve_c 	= (shrout * abs(prc)) // Common shares outstanding * Price
gen ret2 = ret
replace ret2 = 0 if ret2 ==.

*-------------------------------------------------------------------------------
// 10 Book-to-market
gen BM 		=	log(ceq/mve_c)
label var BM "Book-to-market"

// 66 Profit Margin
gen PM = ni/revt
label var PM "Profit Margin"

// 52 Six month momentum 
gen Mom6m = ( (1+l.ret2)*(1+l2.ret2)*(1+l3.ret2)*(1+l4.ret2)*(1+l5.ret2)) - 1
label var Mom6m "Six month momentum"

*-------------------------------------------------------------------------------

// 1 52-week high
gen temp = max(l1.maxpr, l2.maxpr, l3.maxpr, l4.maxpr, l5.maxpr, l6.maxpr, ///
	l7.maxpr, l8.maxpr, l9.maxpr, l10.maxpr, l11.maxpr, l12.maxpr)
gen High52 = (abs(prc)/cfacshr)/temp	
drop temp*
label var High52 "52-week High"


// 2 Accruals
gen tempTXP = txp
replace tempTXP = 0 if mi(txp)

gen Accruals = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
	(dlc - l12.dlc) - (tempTXP - l12.tempTXP) )) / ( (at + l12.at)/2)
label var Accruals "Accruals"
drop temp*

// 49 Book-to-market and accruals
gen tempacc = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
	(dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)

egen tempqBM = fastxtile(BM), by(time_avail_m) n(5)
egen tempqAcc = fastxtile(tempacc), by(time_avail_m) n(5)

gen AccrualsBM = 1 if tempqBM == 5 & tempqAcc == 1
replace AccrualsBM = 0 if tempqBM == 1 & tempqAcc == 5
replace AccrualsBM = . if ceq <0

drop temp*
label var AccrualsBM "Accruals and BM"



// 3 Advertising expense
gen AdExp 	= xad/mve_c
replace AdExp = . if xad <= 0 // Following Table VII
label var AdExp "Advertising Expenses"

// 4 Illiquidity
gen Illiquidity = (ill + l.ill + l2.ill + l3.ill + l4.ill + l5.ill + ///
	l6.ill + l7.ill + l8.ill + l9.ill + l10.ill + l11.ill)/12
label var Illiquidity "Illiquidity"

// 6 Asset Growth
gen AssetGrowth = (at - l12.at)/l12.at 
label var AssetGrowth "Asset Growth"

// 7 Asset Turnover
gen temp = (rect + invt + aco + ppent + intan - ap - lco - lo) 
gen AssetTurnover = sale/((temp + l12.temp)/2)
drop temp
replace AssetTurnover = . if AssetTurnover < 0
label var AssetTurnover "Asset Turnover"

// 8 Beta
label var Beta "CAPM Beta"

// 9 Bid-ask spread
gen BidAskSpread = hlspread // MP divides by price but hlspread already divides by price (in both Corwin's xlsx and sas code)
label var BidAskSpread "Bid-ask spread"

// 11 Cash-flow to market	
gen CF 		= (ib + dp)/mve_c
label var CF "Cash-flow to market"

// 12 Cash-flow variance
* works better without MP's screens (original lacks screens)
* 2018 04 AC
gen tempCF = (ib + dp)/mve_c
asrol tempCF, gen(sigma) stat(sd) window(time_avail_m 60) min(24) by(permno)
gen VarCF = sigma^2
drop sigma
label var VarCF "Cash-flow variance"
cap drop temp*

// 13 Change in Asset Turnover
gen ChAssetTurnover = AssetTurnover - l12.AssetTurnover
label var ChAssetTurnover "Change in Asset Turnover"

// 413 Change in Forecast and Accrual
gen tempAccruals = ( (act - l12.act) - (che - l12.che) - ( (lct - l12.lct) - ///
	(dlc - l12.dlc) - (txp - l12.txp) )) / ( (at + l12.at)/2)
egen tempsort = fastxtile(tempAccruals), by(time_avail_m) n(2)
gen ChForecastAccrual = 1 if meanest > l.meanest & !mi(meanest) & !mi(l.meanest)
replace ChForecastAccrual = 0 if meanest < l.meanest & !mi(meanest) & !mi(l.meanest)
replace ChForecastAccrual = . if tempsort == 1
drop temp*
label var ChForecastAccrual "Change in Forecast and Accrual"


// 14 Change in Profit Margin
gen ChPM = PM - l12.PM
label var ChPM "Change in Profit Margin"

// 15 Change in recommendation
label var ChangeInRecommendation "Change in recommendation"

// 16 Coskewness
label var Coskewness "Coskewness"

// 17 Credit Rating Downgrade 
gen CredRatDG = 0
replace CredRatDG = 1 if (credrat_dwn == 1 | l.credrat_dwn == 1 | l2.credrat_dwn == 1 | l3.credrat_dwn == 1 | l4.credrat_dwn == 1 | l5.credrat_dwn == 1  ) 
// we lack data before 1985 and after 2015.  Not sure why.  
// Should probably do this by counting credrat_dwn obs but I don't know how to in stata -- AC
*replace CredRatDG = . if year < 1985 | year > 2015 
replace CredRatDG = . if year < 1979 | year > 2016  // No data before or after that
label var CredRatDG "Credit Rating Downgrade"


// 18 Debt Issuance
gen DebtIssuance = (dltis > 0 & dltis !=.)
replace DebtIssuance = . if shrcd > 11 | mi(BM)
label var DebtIssuance "Debt Issuance"

// 19 Dividend Initiation
gen temp = divamt
replace temp = 0 if divamt ==.
gen PayedDividend = temp > 0

* Make columns with dividends over last 24 months
foreach n of numlist 1(1)25 {
	gen Divtemp`n' = l`n'.temp
	replace Divtemp`n' = 0 if mi(Divtemp`n')
}
egen tempNo = rowtotal(Divtemp*)
gen NoDiv24 = (tempNo == 0)

gen tempDivInit = (NoDiv24 == 1 & PayedDividend == 1)

gen DivInit = (tempDivInit == 1 | l.tempDivInit == 1 | l2.tempDivInit == 1 ///
	| l3.tempDivInit == 1 | l4.tempDivInit == 1 | l5.tempDivInit == 1 ///
	| l6.tempDivInit == 1 | l7.tempDivInit == 1 | l8.tempDivInit == 1 ///
	| l9.tempDivInit == 1 | l10.tempDivInit == 1 | l11.tempDivInit == 1)

replace DivInit = . if shrcd > 11 
drop temp* Divtemp* PayedDividend NoDiv24
label var DivInit "Dividend Initiation"

// 20 Dividend Omission
gen temp = divamt
replace temp = 0 if divamt ==.

gen tempND = ( temp ==0 & l.temp ==0 & l2.temp ==0)
gen temp3  = (l3.temp >0 & l6.temp>0 & l9.temp >0 & l12.temp > 0 & l15.temp > 0 & l18.temp >0)
gen tempOmit = (tempND == 1 & temp3 == 1)

gen DivOmit = (tempOmit == 1 | l1.tempOmit == 1 | l2.tempOmit == 1 | l3.tempOmit ==1 ///
	| l4.tempOmit == 1 | l5.tempOmit == 1 | l6.tempOmit == 1 | l7.tempOmit == 1 ///
	| l8.tempOmit == 1 | l9.tempOmit == 1 | l10.tempOmit ==1 | l11.tempOmit == 1)
	
cap drop temp*
label var DivOmit "Dividend Omission"

// 21 Dividend Yield (Current)
gen temp = divamt
replace temp = 0 if divamt ==.
gen tempdy = 4*max(temp, l1.temp, l2.temp)/abs(prc)

gen tempdypos = tempdy 
replace tempdypos = . if (temp <=0 & l1.temp<=0 & l2.temp<=0) | ///
	(l3.temp <=0 & l4.temp <= 0 & l5.temp <=0) | ///
	(l6.temp<=0 & l7.temp<=0 & l8.temp<=0) | ///
	(l9.temp<=0 & l10.temp<=0 & l11.temp <=0)	
	
egen tempdyposq = fastxtile(tempdypos), by(time_avail_m) n(4)	
gen DivYield = 1 if tempdyposq >= 3 
replace DivYield = 0 if tempdy == 0 // see table 1B
egen tempsize = fastxtile(mve_c), by(time_avail_m) n(4)	
replace DivYield = . if tempsize >= 3	// see table 1B

cap drop temp*
label var DivYield "Dividend Yield (Current)"

// 22 Dividends
gen DivInd = ( (l11.ret > l11.retx) | (l2.ret > l2.retx) )
*replace DivInd = . if abs(prc) < 5
label var DivInd "Dividend Indicator"

// 23 Down Forecast
gen DownForecast = (meanest < l.meanest)
replace DownForecast = . if mi(meanest) | mi(l.meanest)
label var DownForecast "Down Forecast EPS"

// 24 Earnings-to-Price ratio
* original paper uses Dec 31 obs for ib and mve_c, while our 
* mve_c gets updated monthly.  Thus, I lag mve_c 6 months
* to try to get at the spirit of the original paper.  
* this lag helps a lot, as it seems to remove momentum effects.	
* excluding EP < 0 and using the original sample (not MP's) helps too
* 2018 04 AC
gen tempib = ib
gen tempp = l6.mve_c
gen EP 		= tempib/tempp
replace EP  = . if EP < 0
label var EP "Earnings-to-price ratio"
cap drop temp*


// 25 Earnings consistency
cap drop temp*
gen temp = (epspx - l12.epspx)/(.5*(abs(l12.epspx) + abs(l24.epspx)))
foreach n of numlist 12(12)48 {
	gen temp`n' = l`n'.temp
	}
egen EarningsConsistency = rowmean(temp*)

replace EarningsConsistency = . if abs(epspx/l12.epspx) > 6 | ///
	(temp > 0 & l12.temp < 0 & !mi(temp)) | (temp < 0 & l12.temp > 0 & !mi(temp))

cap drop temp*
label var EarningsConsistency "Earnings Consistency"

// 26 Earnings Surprise
gen GrTemp = (epspxq - l12.epspxq)
foreach n of numlist 3(3)24 {
	gen temp`n' = l`n'.GrTemp
	}
egen Drift = rowmean(temp*)

gen EarningsSurprise = epspxq - l12.epspxq - Drift
cap drop temp*
foreach n of numlist 3(3)24 {
	gen temp`n' = l`n'.EarningsSurprise
	}
egen SD = rowsd(temp*)

replace EarningsSurprise = EarningsSurprise/SD
drop SD Drift temp* GrTemp
label var EarningsSurprise "Earnings Surprise"


// 27 Enterprise component of BM
gen temp = che - dltt - dlc - dc - dvpa+ tstkp
gen EBM = (ceq + temp)/(mve_c + temp)
drop temp
label var EBM "Enterprise component of BM"

// 28 Enterprise Multiple
gen EntMult = (mve_c + dltt + dlc + dc - che)/oibdp
replace EntMult = . if ceq < 0 | oibdp < 0  // This screen come from Loughran and Wellman's paper, MP don't mention them.
label var EntMult "Enterprise Multiple"

// 29 Exchange Switch
gen ExchSwitch = ( ( exchcd == 1 & (l1.exchcd == 2 | l2.exchcd == 2 | l3.exchcd == 2 | ///
	l4.exchcd == 2 | l5.exchcd == 2 | l6.exchcd == 2 | l7.exchcd == 2 | ///
	l8.exchcd == 2 | l9.exchcd == 2 | l10.exchcd == 2 | l11.exchcd == 2 | l12.exchcd == 2 | ///
	l1.exchcd == 3 | l2.exchcd == 3 | l3.exchcd == 3 | ///
	l4.exchcd == 3 | l5.exchcd == 3 | l6.exchcd == 3 | l7.exchcd == 3 | ///
	l8.exchcd == 3 | l9.exchcd == 3 | l10.exchcd == 3 | l11.exchcd == 3 | l12.exchcd == 3)) | ///
	( exchcd == 2 & (l1.exchcd == 3 | l2.exchcd == 3 | l3.exchcd == 3 | ///
	l4.exchcd == 3 | l5.exchcd == 3 | l6.exchcd == 3 | l7.exchcd == 3 | ///
	l8.exchcd == 3 | l9.exchcd == 3 | l10.exchcd == 3 | l11.exchcd == 3 | l12.exchcd == 3) ))
label var ExchSwitch "Exchange Switch"

// 30 Firm Age
* original paper uses NYSE archives for 459 securities in 1926
bys permno (time_avail_m): gen FirmAge = _n
* remove stuff we started with (don't have age for)
gen tempcrsptime = time_avail_m - mofd(mdy(7,1,1926)) + 1
replace FirmAge = . if tempcrsptime == FirmAge
replace FirmAge = . if exchcd != 1 
label var FirmAge "Firm Age"	

// 31 Firm Age - Momentum
bys permno (time_avail_m): gen tempage = _n
gen FirmAgeMom = ( (1+l.ret2)*(1+l2.ret2)*(1+l3.ret2)*(1+l4.ret2)*(1+l5.ret2) ) - 1
replace FirmAgeMom = . if abs(prc) < 5 | tempage < 12
egen temp = fastxtile(tempage), by(time_avail_m) n(5)  // Find bottom age quintile
replace FirmAgeMom =. if temp > 1 & temp !=.
drop temp
label var FirmAgeMom "Firm Age - Momentum"


// 431 Forecast dispersion
gen ForecastDispersion = stdev_est/abs(meanest)
label var ForecastDispersion "EPS Forecast Dispersion"

// 32 Governance Index
label var G_Binary "Governance Index"

// 33 Gross Profitability
gen GP 	=   (sale-cogs)/at		
label var GP "Gross profitability"

// 34 Change in inventory
gen ChInv 	=	(invt-l12.invt)/((at+l12.at)/2)
label var ChInv "Change in inventory"

// 35 Growth in long term net operating assets
gen GrLTNOA = 	(rect+invt+ppent+aco+intan+ao-ap-lco-lo)/at -(l12.rect+l12.invt+ ///
	l12.ppent+l12.aco+l12.intan+l12.ao-l12.ap-l12.lco-l12.lo)/l12.at ///
	- ( rect-l12.rect+invt-l12.invt + aco-l12.aco-(ap-l12.ap+lco-l12.lco) -dp )/((at+l12.at)/2)
label var GrLTNOA "Growth in long term net operating assets"

// 36 Piotroski (2000) F-score
* aka pscore
* somewhat fixed by Andrew 2018 04
* used ebit insetad of sales - cogs
* used shrout - l12.shrout instead of the compustat sale of common stock variable
* used oancf when needed
* remove if any variable is missing following original paper
replace fopt = oancf if fopt == .
gen p1 = 0
replace p1 = 1 if ib > 0
gen p2 = 0
replace p2 = 1 if fopt > 0
gen p3 = 0
replace p3 = 1 	if (ib/at - l12.ib/l12.at)>0
gen p4 = 0
replace p4 =1 if fopt > ib
gen p5 = 0
replace p5 = 1 if dltt/at - l12.dltt/l12.at < 0
gen p6 = 0
replace p6 = 1 if act/lct - l12.act/l12.lct > 0
gen p7 = 0
gen tempebit = ib + txt + xint
replace p7 = 1 if tempebit/sale - tempebit/l12.sale > 0
gen p8 = 0
replace p8 = 1 if sale/at - l12.sale/l12.at>0
gen p9 = 0
replace p9 = 1 if shrout <= l12.shrout

gen PS = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
drop p1 p2 p3 p4 p5 p6 p7 p8 p9
replace PS = . if fopt == . | ib == . | at == . | dltt == . | sale == . | act == . ///
	| tempebit == . | shrout == .
drop tempebit

egen temp = fastxtile(BM), by(time_avail_m) n(5)  // Find highest BM quintile
replace PS =. if temp != 5

drop temp
label var PS "Piotroski F-score"

// 37 Mohanram G-score
* aka Mscore
* Limit sample to firms in the lowest BM quintile
egen temp = fastxtile(BM), by(time_avail_m) n(5) 
preserve
	drop if temp == 1
	save temp, replace
restore
keep if temp == 1

xtset permno time_avail_m
gen roa = 	ni/((at+l12.at)/2)
gen cfroa = oancf/((at+l12.at)/2)
replace cfroa = (ib+dp)/((at+l12.at)/2) if oancf ==.
gen xrdint = 	xrd/((at+l12.at)/2)
gen capxint = 	capx/((at+l12.at)/2)
gen xadint = 	xad/((at+l12.at)/2)

foreach v of varlist roa cfroa xrdint capxint xadint {

	egen md_`v' = median(`v'), by(sic2D time_avail_m)
	
}

gen m1 = 0
replace m1 = 1 if roa > md_roa

gen m2 = 0
replace m2 = 1 if cfroa > md_cfroa

gen m3 = 0 
replace m3 = 1 if oancf > ni

gen m4 = 0
replace m4 = 1 if xrdint > md_xrdint

gen m5 = 0
replace m5 = 1 if capxint > md_capxint

gen m6 = 0
replace m6 = 1 if xadint > md_xadint

bys permno: asrol ni, gen(niVol) stat(sd) window(time_avail_m 36) min(24)
bys permno: asrol revt, gen(revVol) stat(sd) window(time_avail_m 36) min(24)

foreach v of varlist niVol revVol {

	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}		

gen m7 = 0
replace m7 = 1 if niVol < md_niVol

gen m8 = 0
replace m8 = 1 if revVol < md_revVol

/*
gen MS = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8
*/
gen tempMS = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8
gen MS = 1 if tempMS >= 6 & tempMS <= 8
replace MS =  0 if tempMS <= 1
drop m1 m2 m3 m4 m5 m6 m7 m8 temp niVol revVol roa cfroa xrdint capxint xadint md_* tempMS
label var MS "Mohanram G-score"

append using temp
drop temp

// 38 Industry concentration (Herfindahl)
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works

egen indsale    = total(sale), by(sic3D time_avail_m)
gen temp  	= (sale/indsale)^2
egen tempHerf 	= total(temp), by(sic3D time_avail_m)
bys permno: asrol tempHerf, gen(Herf) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average
replace Herf = . if shrcd > 11

* Missing if regulated industry (Barclay and Smith 1995 definition)
replace Herf = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace Herf = . if tempSIC == "4512" & year <=1978 
replace Herf = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace Herf = . if substr(tempSIC, 1,2) == "49"
drop temp*
label var Herf "Industry concentration"

// 339 Idiosyncratic Risk
rename idiovol IdioRisk
label var IdioRisk "Idiosyncratic Risk"

// 339c Idiosyncratic Risk
label var IdioVolCAPM "Idiosyncratic Risk (CAPM)"

// 339ff Idiosyncratic Risk
label var IdioVol3F "Idiosyncratic Risk (3 factor)"

// 339qfac Idiosyncratic Risk
label var IdioVolQF "Idiosyncratic Risk (qfactor)"

// 339aht Idiosyncratic Risk (Ali, Hwang, and Trombley)
label var IdioVolAHT "Idiosyncratic Risk (AHT)"

// 724 Systematic volatility
label var betaVIX "Systematic volatility"

// 40 Industry momentum
xtset permno time_avail_m
gen tempMom6m = ( (1+l.ret2)*(1+l2.ret2)*(1+l3.ret2)*(1+l4.ret2)*(1+l5.ret2)) - 1
egen IndMom = wtmean(tempMom6m), by(sic2D time_avail_m) weight(mve_c)
label var IndMom "Industry momentum"
drop temp*


// 41 IPO
* 2018 04 AC: fixed this to match Ritter's results
* previously was going short recent IPOs and going long
* all firms that had IPOs a long time ago ignoring missing ipo dates
* That somehow leads to a negative return in ritter's sample.
* but has ridiculously large SE of 0.52
* Ritter actually goes short recent IPOs and long matched firms 
* which should include firms missing IPO dates.  Removing the first 2
* months is also consistent with the main table
gen IndIPO = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate >= 3)
replace IndIPO = 0 if IPOdate == .

label var IndIPO "IPO 3 months to 3 years ago"

// 43 IPO and Age
gen tempipo = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate >= 3)
replace tempipo = . if IPOdate == .
gen AgeIPO = year(dofm(time_avail_m)) - FoundingYear
replace AgeIPO = . if tempipo == 0 // only sort recent IPO firms
egen tempTotal = total(tempipo), by(time_avail_m)  // Number of IPO = 1 firms per month
replace AgeIPO = . if tempTotal < 20*5
drop temp*
label var AgeIPO "IPO and Age"


// 42 Investment
gen Investment = capx/revt 
bys permno: asrol Investment, gen(tempMean) window(time_avail_m 36) min(24) stat(mean)
replace Investment = Investment/tempMean
replace Investment = . if revt<10  // Replace with missing if revenue less than 10 million (units are millions)
drop temp*
label var Investment "Investment"


// 44 IPOs without R&D
gen tempipo = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate > 6)
replace tempipo  = 0 if IPOdate == .
gen RDIPO = 0
replace RDIPO = 1 if tempipo  == 1 & xrd == 0
drop tempipo
label var RDIPO "IPO without R&D"


// 45 Intermediate momentum
gen IntMom = ( (1+l7.ret2)*(1+l8.ret2)*(1+l9.ret2)*(1+l10.ret2)*(1+l11.ret2)*(1+l12.ret2) ) - 1
label var IntMom "Intermediate Momentum"

// 46 Market leverage
* 2018 04 previously called LTlev and defined using dltt
gen Leverage = lt/mve_c
label var Leverage "Market leverage"

// 47 Leverage component of BM
gen BP = (ceq + tstkp - dvpa)/mve_c
gen BPEBM = BP - EBM
label var BPEBM "Leverage component of BM"

// 48 Long-run reversal
gen Mom36m = (   (1+l13.ret2)*(1+l14.ret2)*(1+l15.ret2)*(1+l16.ret2)*(1+l17.ret2)*(1+l18.ret2)   * ///
	(1+l19.ret2)*(1+l20.ret2)*(1+l21.ret2)*(1+l22.ret2)*(1+l23.ret2)*(1+l24.ret2)* ///
	(1+l25.ret2)*(1+l26.ret2)*(1+l27.ret2)*(1+l28.ret2)*(1+l29.ret2)*(1+l30.ret2)     * ///
	(1+l31.ret2)*(1+l32.ret2)*(1+l33.ret2)*(1+l34.ret2)*(1+l35.ret2)*(1+l36.ret2)  ) - 1
label var Mom36m "LT reversal"


// 50 Max return
gen MaxRet = maxret
label var MaxRet "Maximum return over month"

// 53 Momentum and Reversal
egen tempMom6 = fastxtile(Mom6m), by(time_avail_m) n(5)
egen tempMom36 = fastxtile(Mom36m), by(time_avail_m) n(5)

gen MomRev = 1 if tempMom6 == 5 & tempMom36 == 1
replace MomRev = 0 if tempMom6 == 1 & tempMom36 == 5
drop temp*
label var MomRev "Momentum and LT Reversal"

// 454 Momentum and Rating
* credrat is from 1_prepareratings.do
gen Mom6mJunk = Mom6m if credrat <= 14
label var Mom6mJunk "Junk stock momentum"

// 354 Momentum-Reversal
gen Mom18m13m = ( (1+l13.ret2)*(1+l14.ret2)*(1+l15.ret2)*(1+l16.ret2)*(1+l17.ret2)*(1+l18.ret2) ) - 1
replace Mom18m13m  = -1*Mom18m13m 
label var Mom18m13m "Momentum-Reversal"

// 55 Momentum-Volume
replace vol = . if vol <0
bys permno: asrol vol, gen(temp) window(time_avail_m 6) min(5) stat(mean)
egen tempVol = fastxtile(temp), by(time_avail_m) n(5)

gen MomVol = Mom6m if tempVol == 5
sort permno time_avail_m
by permno: replace MomVol = . if _n < 24
drop temp*
label var MomVol "Momentum-Volume"

// 56 Net Operating Assets
gen OA = at - che
gen OL = at - dltt - mib - dc - ceq
gen NOA = (OA - OL)/l12.at
label var NOA "Net Operating Assets"

// 57 Change in Net Working Capital
gen temp = ( (act - che) - (lct - dlc) )/at
gen ChNWC = temp - l12.temp
drop temp*
label var ChNWC "Change in Net Working Capital"

// 58 Change in Net Noncurrent Operating Assets
gen temp = ( (at - act - ivao)  - (lt - dlc - dltt) )/at
gen ChNNCOA = temp - l12.temp
drop temp*
label var ChNNCOA "Change in Net Noncurrent Operating Assets"

// 59 Operating Leverage
* aka OperLeverage
gen tempxsga		= 0
replace tempxsga 	= xsga if xsga !=.
gen OPLeverage = (tempxsga + cogs)/at
label var OPLeverage "Operating Leverage"
drop temp*

// 60 Organizational Capital

/*
* Tom: See http://www.kellogg.northwestern.edu/faculty/papanikolaou/htm/org_cap.pdf
* equations 38 and 39 
gen avgat = (at+l12.at)/2
gen orgcap_1 =  (xsga/cpi)/(.1+.15) if FirmAge <= 12
replace orgcap_1 = l12.orgcap_1*(1-.15) + xsga/cpi if FirmAge > 12
gen OrgCap = orgcap_1/avgat
replace OrgCap = . if FirmAge <= 12
drop avgat orgcap_1
label var OrgCap "Organizational capital"
*/

* MP version
bys permno (time_avail_m): gen tempAge = _n
gen OrgCap = 4*xsga if tempAge <= 12
replace OrgCap = .85*l12.OrgCap + xsga if tempAge > 12
replace OrgCap = OrgCap/at
label var OrgCap "Organizational capital"
cap drop temp*

// 61 O-Score		
* fixed fopt 2017 04 Andrew
* fopt = funds from operations, total, not available after 1993
* fopt contains a Not Available data code for a company reporting a Statement of Cash Flows (Format Code = 7). 
* oancf = Operating Activities - Net Cash Flow, only available after 1992
* price screen seems to help a lot
replace fopt = oancf if fopt == .
gen OScore = -1.32 - .407*log(at/gnpdefl) + 6.03*(lt/at) - 1.43*( (act - lct)/at) + ///
	.076*(lct/act) - 1.72*(lt>at) - 2.37*(ib/at) - 1.83*(fopt/lt) + .285*(ib + l12.ib <0) - ///
	.521*( (ib - l12.ib)/(abs(ib) + abs(l12.ib)) )
destring sic, replace
replace OScore = . if (sic > 3999 & sic < 5000) | sic > 5999  | abs(prc) < 5 	

* returns on non-monotonic (see Panel A of original), so we want to exclude
* the lowest quintile of OScores
egen tempsort = fastxtile(OScore), by(time_avail_m) n(5)	
replace OScore = . if tempsort == 1	

label var OScore "O-Score"	

// 62 Pension Funding Status
gen FVPA = pbnaa if year >=1980 & year <=1986
replace FVPA = pplao + pplau if year >=1987 & year <= 1997
replace FVPA = pplao if year >= 1998

gen PBO = pbnvv if year >= 1980 & year <=1986
replace PBO = pbpro + pbpru if year >= 1987 & year <=1997
replace PBO = pbpro if year >=1998

gen FR = (FVPA - PBO)/mve_c
replace FR = . if shrcd > 11
label var FR "Pension Funding Status"

// 62n Pension Funding Status (scaled by book assets)
gen FRbook = (FVPA - PBO)/at
replace FRbook = . if shrcd > 11
label var FRbook "Pension Funding Status (scaled by book assets)"

// 63 Percent Operating Accruals
gen PctAcc 		= (ib-oancf)/abs(ib) 		
replace PctAcc 	= (ib - oancf)/.01 if ib == 0
replace PctAcc 	= ( (act-l12.act) - (che-l12.che) - (  (lct-l12.lct)- ///
	(dlc-l12.dlc)-(txp-l12.txp)-dp ) )/abs(ib) if oancf ==.
replace PctAcc 	= (   (act-l12.act) - (che-l12.che) - (  (lct-l12.lct)- ///
	(dlc-l12.dlc)-(txp-l12.txp)-dp ) )/.01 if oancf == . & ib ==0
label var PctAcc "Percent Operating Accruals"

// 64 Percent Total Accruals
gen PctTotAcc = ( ni - (prstkcc - sstk + dvt + oancf + fincf + ivncf) )/abs(ni)
label var PctTotAcc "Percent Total Accruals"

// 65 Price
gen Price = log(abs(prc))
label var Price "Price"

// 67 Profitability
gen Profitability = (cshprq*epspxq)/at
label var Profitability "Profitability"

// 69 R&D to market cap
gen RD 	=   xrd/mve_c					
label var RD "R&D-to-market cap"

// 70 Return on Equity
gen RoE = ni/ceq 

// 71 Revenue surprise
gen revps = revtq/cshprq

gen GrTemp = (revps - l12.revps)
foreach n of numlist 3(3)24 {
	gen temp`n' = l`n'.GrTemp
	}
egen Drift = rowmean(temp*)

gen RevenueSurprise = revps - l12.revps - Drift
cap drop temp*
foreach n of numlist 3(3)24 {
	gen temp`n' = l`n'.RevenueSurprise
	}
egen SD = rowsd(temp*)

replace RevenueSurprise = RevenueSurprise/SD
drop SD Drift temp* GrTemp
label var RevenueSurprise "Revenue Surprise"

// 72 Sales growth (average rank)
* aka salesgr
gen temp = log(revt) - log(l12.revt)
gsort time_avail_m -temp
by time_avail_m: gen tempRank = _n if temp !=.
xtset permno time_avail_m
 
gen MeanRankRevGrowth = (5*l12.tempRank + 4* l24.tempRank + 3*l36.tempRank + ///
	2*l48.tempRank  + l60.tempRank)/15
drop temp*
label var MeanRankRevGrowth "Average Revenue Growth"

// 73 Sales-to-price ratio
gen SP 		=   sale/mve_c
label var SP "Sales-to-price ratio"

// 74 Seasonality (2-5)
cap drop temp*
foreach n of numlist 11(12)60 {
	gen temp`n' = l`n'.ret2
}
*egen MomSeas = rowmean(temp*) // Quick way to take mean only over non-missing values
egen retTemp1 = rowtotal(temp*), missing  // Quick way to take mean only over non-missing values
egen retTemp2 = rownonmiss(temp*)

gen MomSeas = retTemp1/retTemp2
label var MomSeas "Return Seasonality"

// 74a Non-Seasonal returns 2-5
* We compute this with a trick: Use asrol to compute rolling sum and non-missing obs
* in specified window, then subtract seasonal part of returns from above and adjust denominator accordingly

gen retLagTemp = ret2
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  // 59 because current obs is also part of calculations (predictions for t+1)

gen MomSeasAlt2to5n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt2to5n "Non-seasonal return (years 2-5)"

drop *Temp* temp* 

// 74_1a Seasonality (1 year)
gen MomSeasAlt1a = l11.ret2
label var MomSeasAlt1a "Return Seasonality (1 year)"

// 74_1n Non-Seasonal return 1
asrol ret2, by(permno) window(time_avail_m 10) stat(mean) minimum(6) gen(MomSeasAlt1n) xf(focal)  // xf(focal) excludes STR, the most recent return
label var MomSeasAlt1n "Non-seasonal return (year 1)"

// 74_6to10 Seasonality (6-10)
cap drop temp*
foreach n of numlist 71(12)120 {
	gen temp`n' = l`n'.ret2
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen MomSeasAlt6to10a = retTemp1/retTemp2
label var MomSeasAlt6to10a "Return Seasonality (6-10)"

// 74_6to10n Non-Seasonal returns 6-10
gen retLagTemp = l60.ret2
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  

gen MomSeasAlt6to10n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt6to10n "Non-seasonal return (years 6-10)"

drop *Temp* temp* 

// 74_11to15 Seasonality (11-15)
cap drop temp*
foreach n of numlist 131(12)180 {
	gen temp`n' = l`n'.ret2
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen MomSeasAlt11to15a = retTemp1/retTemp2
label var MomSeasAlt11to15a "Return Seasonality (11-15)"

// 74_11to15n Non-Seasonal returns 11-15
gen retLagTemp = l120.ret2
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  

gen MomSeasAlt11to15n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt11to15n "Non-seasonal return (years 11-15)"

drop *Temp* temp* 


// 74_16to20 Seasonality (16-20)
cap drop temp*
foreach n of numlist 191(12)240 {
	gen temp`n' = l`n'.ret2
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen MomSeasAlt16to20a = retTemp1/retTemp2
label var MomSeasAlt16to20a "Return Seasonality (16-20)"

// 74_16to20n Non-Seasonal returns 16-20
gen retLagTemp = l180.ret2
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  

gen MomSeasAlt16to20n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt16to20n "Non-seasonal return (years 16-20)"

drop *Temp* temp* 

// 75 Share issuance (1 year)
gen temp = shrout/cfacshr
gen ShareIss1Y = (l6.temp - l18.temp)/l18.temp
drop temp*
label var ShareIss1Y "Share Issuance (1 year)"

// 76 Share issuance (5 year)
gen temp = shrout/cfacshr
gen ShareIss5Y = (temp - l60.temp)/l60.temp
drop temp*
label var ShareIss5Y "Share Issuance (5 year)"

// 77 Share repurchases
gen ShareRepurchase = (prstkc > 0 & !mi(prstkc))
replace ShareRepurchase = . if mi(prstkc)
label var ShareRepurchase "Share Repurchase"

// 78 Share Volume
gen ShareVol = (vol + l1.vol + l2.vol)/(3*shrout) // vol is in 100's, shrout is in 1000's
* original uses regressions, and ShareVol is right skewed
* so we remove the "uninformative" left mass
egen tempsort = fastxtile(ShareVol), by(time_avail_m) n(2)
replace ShareVol = . if tempsort == 1
drop temp*	
label var ShareVol "Share Volume"	

// 79 Short interest
gen ShortInterest = shortint/shrout
label var ShortInterest "Short interest"

// 80 ST reversal
gen Mom1m = ret2
label var Mom1m "Short-term reversal"

// 81 Size [Market cap (monthly)]
gen Size = log(abs(prc)*shrout)
label var Size "Size"

// 82 Spinoffs
bys permno (time_avail_m): gen FirmAgeNoScreen = _n
gen Spinoff = 1 if SpinoffCo == 1 & FirmAgeNoScreen <= 12
replace Spinoff = 0 if Spinoff ==.
label var Spinoff "Spinoff"

// 83 Sustainable Growth
gen ChEQ = ceq/l12.ceq if ceq >0 & l12.ceq >0
label var ChEQ "Sustainable Growth"

// 84 Taxes
* Define highest tax rate by year
gen tr = .48
replace tr = .46 if year >= 1979 & year <= 1986
replace tr = .4 if year ==1987
replace tr = .34 if year >= 1988 & year <=1992
replace tr = .35 if year >=1993

gen Tax 		= ((txfo+txfed)/tr)/ib
replace Tax 	= ((txt-txdi)/tr)/ib if txfo ==. | txfed ==.
replace Tax 	= 1 if (txfo + txfed > 0 | txt > txdi) & ib <=0
label var Tax "Taxable income to income"

// 85 Net external financing
gen XFIN = (sstk - dv - prstkc + dltis - dltr)/at
label var XFIN "Net External Financing"

// 86 Unexpected R&D
gen SurpriseRD = 1 if xrd/revt > 0 & xrd/at > 0 & xrd/l12.xrd > 1.05 & ///
	(xrd/at)/(l12.xrd/l12.at) > 1.05 & xrd !=. & l12.xrd !=.
replace SurpriseRD = 0 if SurpriseRD==. & (xrd !=. & l12.xrd !=.)
label var SurpriseRD "Unexpected R&D increase"

// 87 Up Forecast
gen UpForecast = (meanest > l.meanest)
replace UpForecast = . if mi(meanest) | mi(l.meanest)
label var UpForecast "Up Forecast EPS"

// 88 Volume to Market Cap
gen temp = vol*abs(prc)
bys permno: asrol temp, gen(tempMean) stat(mean) window(time_avail_m 12) min(10)
gen VolMkt = tempMean/mve_c
drop temp*
label var VolMkt "Volume to market equity"

// 89 Volume Trend
*rolling_betaNew2 vol time_avail_m, long(60) short(30)  // Get coefficient
asreg vol time_av, window(time_av 60) min(30) by(permno)
rename _b_time betaVolTrend
drop _*

*rolling_sigma vol, long(60) short(30)  // Get rolling average of volume
bys permno: asrol vol, gen(meanX) stat(mean) window(time_avail_m 60) min(30)  

gen VolumeTrend = betaVolTrend/meanX
drop betaVolTrend meanX
winsor2 VolumeTrend, cut(1 99) replace trim  // TZ ADD ON SINCE SOME VALUES LOOKED OUT OF LINE (e^14)
label var VolumeTrend "Volume Trend"

// 90 Volume variance
bys permno: asrol vol, gen(VolSD) stat(sd) window(time_avail_m 36) min(24)
label var VolSD "Volume variance"

// 91 Altman Z-Score
* 2018 04 AC fixed to account for nonmontonicity and exchange code
gen ZScore = 1.2*(act - lct)/at + 1.4*(re/at) + 3.3*(ni + xint + txt)/at + ///
	.6*(mve_c/lt) + revt/at
replace ZScore = . if (sic >3999 & sic < 4999) | sic > 5999
* returns on non-monotonic (see Panel A of original), so we want to exclude
* the lowest quintile of ZScores
egen tempsort = fastxtile(ZScore), by(time_avail_m) n(5)	
replace ZScore = . if tempsort == 1	
label var ZScore "Altman Z-Score"
drop tempsort

// 92 Industry-adjusted investment growth
replace capx = ppent - l12.ppent if capx ==.
gen pchcapx  	= (capx- .5*(l12.capx + l24.capx))/(.5*(l12.capx + l24.capx)) 
replace pchcapx = (capx-l12.capx)/l12.capx if mi(pchcapx)
egen temp = mean(pchcapx), by(sic2D time_avail_m)
gen ChInvIA = pchcapx - temp
drop temp

label var ChInvIA "Change in capital inv (ind adj)"

// 93 Sales growth over inventory growth
gen GrSaleToGrInv =	((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) ///
	-((invt- (.5*(l12.invt + l24.invt)))/(.5*(l12.invt + l24.invt)))
replace GrSaleToGrInv =  ((sale-l12.sale)/l12.sale)-((invt-l12.invt)/l12.invt) if mi(GrSaleToGrInv)
label var GrSaleToGrInv "Sales growth over inventory growth"

// 94 Sales growth over overhead growth (xsga = selling, general and administrative expenses)
** Timing: Takes about 30 minutes to get here
gen GrSaleToGrOverhead = ///
	( (sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)) ) ///
	-( (xsga- (.5*(l12.xsga+l24.xsga))) /(.5*(l12.xsga+l24.xsga)) ) 
replace GrSaleToGrOverhead = ///
	( (sale-l12.sale)/l12.sale )-( (xsga-l12.xsga) /l12.xsga ) if mi(GrSaleToGrOverhead)
* returns only only monotonic in 1st - 4th quintiles
* could be consistent with original's rank regressions
egen tempsort = fastxtile(GrSaleToGrOverhead), by(time_avail_m) n(5)
replace GrSaleToGrOverhead = . if tempsort == 5
drop tempsort
label var GrSaleToGrOverhead "Sales growth over overhead growth"

// ============== ADD NONMP SIGNALS ===============================//

// 301 Beta Squared
gen BetaSquared = Beta^2
label var BetaSquared "Beta squared"

// 302 Cash to assets
gen Cash = cheq/atq
label var Cash "Cash to assets"

// 303 Cash flow to debt
gen cashdebt 	= (ib+dp)/((lt+l12.lt)/2)  // Cash flow to debt
label var cashdebt "Cash flow to debt"

// 304 Cash productivity
gen CashProd = (mve_c - at)/che
label var CashProd "Cash productivity"

// 305 Cash flow to price 
gen accrual_level = (act-l12.act - (che-l12.che)) - ( (lct-l12.lct)- ///
                (dlc-l12.dlc)-(txp-l12.txp)-dp )  
gen cfp =(ib - accrual_level )/ mve_c       
replace cfp = oancf/mve_c if oancf !=.
label var cfp "Cash flow to price"

// 306 Change in number of analysts
gen ChNAnalyst = 1 if numest < l3.numest & !mi(l3.numest)
replace ChNAnalyst = 0 if numest >= l3.numest & !mi(numest)
replace ChNAnalyst = . if time_avail_m >= ym(1987,7) & time_avail_m <= ym(1987,9) 
label var ChNAnalyst "Decline in Analyst Coverage"

// 307 Change in taxes
gen ChTax = (txtq - l12.txtq)/l12.at
label var ChTax "Change in taxes"

// 308 Convertible debt
gen ConvDebt 	= 0
replace ConvDebt = 1 	if (dc !=. & dc !=0) | (cshrc !=. & cshrc !=0)
label var ConvDebt "Convertible debt indicator"

// 309 Depreciation to PPE
gen depr 	=	dp/ppent 
label var depr "Depreciation to PPE"

// 310 Past trading volume Fixed Andrew 2018 01
gen DolVol = log(l2.vol*abs(l2.prc))
label var DolVol "Past trading volume"

// 311 Change in Capex over two years
replace capx = ppent - l12.ppent if capx ==. & FirmAge >=24
gen grcapx 	= 	(capx-l24.capx)/l24.capx 
label var grcapx "Change in capex (two years)" 

// 312 Employee growth rate
gen hire = (emp-l12.emp)/(.5*(emp + l12.emp))
replace hire = 0 if emp ==. | l12.emp ==.
replace hire = . if year < 1965
label var hire "Employee growth"


// 314 Twelve month momentum
gen Mom12m = ( (1+l.ret2)*(1+l2.ret2)*(1+l3.ret2)*(1+l4.ret2)*(1+l5.ret2)*(1+l6.ret2)*(1+l7.ret2)*(1+ ///
 l8.ret2)*(1+l9.ret2)*(1+l10.ret2)*(1+l11.ret2) ) - 1
label var Mom12m "Twelve month momentum"

// 315 Number of analysts
gen nanalyst = numest
replace nanalyst = 0 if yofd(dofm(time_avail_m)) >=1989 & mi(nanalyst)
label var nanalyst "Number of analysts"

// 316 Operating profitability
*gen OperProf = (revt - cogs - xsga - xint)/ceq

// dirty simulation of NYSE size breakpoints:
// Fama and French use NYSE market cap median to form size groups,
// independently sort on OperProf, and then equally weight the two
// size groups with high OperProf in the long portfolio 
// (see RFS paper footnote to Table 1)
// This effectively overweights large cap stocks.  We can do
// that by simply excluding small cap here.
// Hou Xue Zhang do something similar
	      * more complicated denominator (ceq-pstk+min(txdi,0)) does not help
	      * removing xsga helps a _lot_, and is pretty much the Novy Marx signal
gen tempprof = (revt - cogs - xsga - xint)/(ceq)
egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3)
replace tempprof = . if tempsizeq == 1
gen OperProf = tempprof
cap drop temp*
label var OperProf "Operating Profitability"


// 317 Current ratio
gen act2 = act
replace act2 	= 	che + rect + invt if act2 ==.
replace lct 	= 	ap if lct ==.
gen currat 		= 	act2/lct  
label var currat "Current ratio"

// 318 Change in current ratio
gen pchcurrat 		= 	((act/lct)-(l12.act/l12.lct))/(l12.act/l12.lct)
replace pchcurrat 	= 	0 if pchcurrat ==.
label var pchcurrat "Change in current ratio"

// 319 CAPEX and inventory
gen invest 		= ((ppegt-l12.ppegt) + (invt-l12.invt))/l12.at
replace invest 	= ((ppent-l12.ppent) +  (invt-l12.invt))/ l12.at if ppegt ==.
label var invest "Capex and inventory"

// 320 Sales growth over receivables growth
gen GrSaleToGrReceivables =	((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) ///
	-((rect- (.5*(l12.rect + l24.rect)))/(.5*(l12.rect + l24.rect)))
replace GrSaleToGrReceivables =  ((sale-l12.sale)/l12.sale)-((rect-l12.rect)/l12.rect) if mi(GrSaleToGrReceivables)
label var GrSaleToGrReceivables "Sales growth over receivables growth"

// 321 Margin growth over sales growth
gen pchgm_pchsale 	= 	(((sale-cogs)-(l12.sale-l12.cogs))/(l12.sale-l12.cogs))-((sale-l12.sale)/l12.sale)
label var pchgm_pchsale "Margin growth over sales growth"

// 322 Change in depreciation to gross PPE
gen pchdepr = 	((dp/ppent)-(l12.dp/l12.ppent))/(l12.dp/l12.ppent)
label var pchdepr "Change in depreciation to gross PPE"

// 323 Quick ratio
gen quick = (act - invt)/lct
label var quick "Quick ratio"

// 324 Real estate holdings
cap drop temp*
gen temp 		= (fatb+fatl)/ppegt  
replace temp 	= (fatb + fatl)/ppent if ppegt ==.
replace temp 	= 0 if temp ==.

egen tempMean = mean(temp), by(sic2D time_avail_m)
gen realestate = temp - tempMean
label var realestate "Real estate holdings"

// 325 Return on assets
gen roaq = ibq/l3.atq
label var roaq "Return on Assets"

// 326 Change in quick ratio
gen pchquick = 	( (act-invt)/lct - (l12.act-l12.invt)/l12.lct ) /  ((l12.act-l12.invt)/l12.lct)
replace pchquick = 0 if pchquick ==. & l12.pchquick ==.
label var pchquick "Change in quick ratio"

// 327 RoA volatility
bys permno: asrol roaq, gen(roavol) stat(sd) window(time_avail_m 48) min(24) 
label var roavol "RoA volatility"

// 328 Return on invested capital
gen roic = (ebit - nopi)/(ceq + lt - che)
label var roic "Return on invested capital"

// 329 Sales to cash ratio
gen salecash 	= sale/che 
label var salecash "Sales to cash"

// 330 Sales to receivables 
gen salerec 	= sale/rect
label var salerec "Sales to receivables"

// 331 Sales to inventory
gen saleinv 	= sale/invt
label var saleinv "Sales to inventory"

// 332 Secured debt over liabilities
gen secured 	= dm/(dltt+dlc)
replace secured = 0 if dltt ==. | dltt ==0 | dlc == .
label var secured "Secured debt over liabilities"

// 333 Secured debt indicator
gen securedind 		= 0
replace securedind 	= 1 	if dm !=. & dm !=0
label var securedind "Secured debt indicator"

// 334 Annual sales growth
gen sgr 	= 	(sale/l12.sale)-1
label var sgr "Annual sales growth"

// 335 Sin stock Original paper
replace sinOrig = . if sinOrig == 0
replace sinOrig = 0 if ///
	(sic >= 2000 & sic <= 2046) | (sic >= 2050 & sic <= 2063) | ///
	(sic >= 2070 & sic <= 2079) | (sic >= 2090 & sic <= 2092) | ///
	(sic >= 2095 & sic <= 2099) | (sic >= 2064 & sic <= 2068) | ///
	(sic >= 2086 & sic <= 2087) | (sic >=  920 & sic <=  999) | ///
	(sic >= 3650 & sic <= 3652) | sic == 3732 | ///
	(sic >= 3931 & sic <= 3932) | (sic >= 3940 & sic <= 3949) | ///
	(sic >= 7800 & sic <= 7833) | (sic >= 7840 & sic <= 7841) | ///
	(sic >= 7900 & sic <= 7911) | (sic >= 7920 & sic <= 7933) | ///
	(sic >= 7940 & sic <= 7949) | sic == 7980 | ///
	(sic >= 7990 & sic <= 7999) & sinOrig !=1

replace sinOrig = . if shrcd > 11
label var sinOrig "Sin Stock (original)"

// 336 Sin Stock Algorithm
replace sinAlgo = . if sinAlgo == 0
replace sinAlgo = 0 if ///
	(sic >= 2000 & sic <= 2046) | (sic >= 2050 & sic <= 2063) | ///
	(sic >= 2070 & sic <= 2079) | (sic >= 2090 & sic <= 2092) | ///
	(sic >= 2095 & sic <= 2099) | (sic >= 2064 & sic <= 2068) | ///
	(sic >= 2086 & sic <= 2087) | (sic >=  920 & sic <=  999) | ///
	(sic >= 3650 & sic <= 3652) | sic == 3732 | ///
	(sic >= 3931 & sic <= 3932) | (sic >= 3940 & sic <= 3949) | ///
	(sic >= 7800 & sic <= 7833) | (sic >= 7840 & sic <= 7841) | ///
	(sic >= 7900 & sic <= 7911) | (sic >= 7920 & sic <= 7933) | ///
	(sic >= 7940 & sic <= 7949) | sic == 7980 | ///
	(sic >= 7990 & sic <= 7999) & sinAlgo !=1
replace sinAlgo = . if shrcd > 11
label var sinAlgo "Sin Stock (algorithm)"

// 337 Change in sales to inventory
gen pchsaleinv 	= ( (sale/invt)-(l12.sale/l12.invt) ) / (l12.sale/l12.invt)
label var pchsaleinv "Change in sales to inventory"

// 39 Std of daily turnover
gen tempturn = vol/shrout
bys permno: asrol tempturn, gen(std_turn) stat(sd) window(time_avail_m 36) min(24)
egen tempqsize = fastxtile(mve_c), by(time_avail_m) n(5) 
replace std_turn = . if tempqsize >= 4 // OP Tab3B: tiny 10 bps spread in size quints 4 and 5
drop temp*
label var std_turn "Turnover volatility"

// 40n1 Number of days with 0 trades (1 month version)
gen zerotradeAlt1 = l.zerotrade
label var zerotradeAlt1 "Days with zero trades (1 month version)"

// 40 Number of days with 0 trades (6 month version)
cap drop temp*
gen temp = (zerotrade + l.zerotrade + l2.zerotrade + l3.zerotrade + ///
	l4.zerotrade + l5.zerotrade)/6
replace zerotrade = temp
drop temp
label var zerotrade "Days with zero trades (6 month version)"

// 40n12 Number of days with 0 trades (12 month version)
gen zerotradeAlt12 = (zerotradeAlt1 + l.zerotradeAlt1 + l2.zerotradeAlt1 + l3.zerotradeAlt1 + ///
	l4.zerotradeAlt1 + l5.zerotradeAlt1 + l6.zerotradeAlt1 + l7.zerotradeAlt1 + l8.zerotradeAlt1 + ///
	l9.zerotradeAlt1 + l10.zerotradeAlt1 + l11.zerotradeAlt1)/12
label var zerotradeAlt12 "Days with zero trades (12 month version)"




// 341 Kaplan-Zingales Index    CASHFLOW = ibq + dpq,
gen tempTX = txdi
replace tempTX = 0 if mi(tempTX)
gen temp = divamt
replace temp = 0 if divamt ==.

gen KZ = -1.002* (ib + dp)/at + .283*(at + mve_c - ceq - tempTX)/at + 3.319*(dlc + dltt)/(dlc + dltt + ceq) ///
 - 39.368*(temp/at) - 1.315*(che/at)
cap drop temp*
label var KZ "Kaplan-Zingales index"

// 342 Earnings forecast
gen sfe =  meanest/abs(prc)
replace sfe = . if abs(prc) < 1
label var sfe "Earnings Forecast"

// 343 Long-term EPS forecast
gen fgr5yrLag = l12.fgr5yr
replace fgr5yrLag = . if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == .
label var fgr5yrLag "Long-term EPS forecast"

// 343d Long-term EPS forecast (December version)
cap drop temp*
gen tempEPS = fgr5yr if month(dofm(time_avail_m)) == 12
gen tempYear = yofd(dofm(time_avail_m))
egen tempDecEPS = min(tempEPS), by(permno tempYear)

gen fgr5yrLagJune = l12.tempDecEPS if month(dofm(time_avail_m)) > = 6
replace fgr5yrLagJune = l17.tempDecEPS if month(dofm(time_avail_m)) < 6

replace fgr5yrLagJune = . if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == .
label var fgr5yrLagJune "Long-term EPS forecast (December version)"

// 344 Consensus recommendation
gen ConsRecomm = 1 if MeanRecomm >3 & MeanRecomm < .
replace ConsRecomm = 0 if MeanRecomm <= 1.5
label var ConsRecomm "Consensus Recommendation"

// 345 Tangibility
// ac: probably don't need the tempAnomalies stuff anymore
drop tickerIBES sic2D conm tic cnum cusip cik lpermco cpi
save tempAnomalies, replace // Memory problems with preserve/restore

*preserve
	drop if sicCS < 2000 | sicCS > 3999  // Manufacturing firms only
	egen tempFC = fastxtile(at), n(10) by(time_avail_m)
	gen FC = 1 if tempFC <=3  // Lower three deciles are defined as financiall constrained
	replace FC = 0 if tempFC >=8 & !mi(tempFC)
	save temp, replace
*restore
u tempAnomalies, clear
merge 1:1 permno time_avail_m using temp, keepusing(FC) nogenerate

gen tang = 	(che + .715*rect + .547*invt + .535*ppegt)/at 
label var tang "Tangibility"

// 346 Breadth in ownership
*gen DelBreadth = numinstown - l3.numinstown
gen DelBreadth = dbreadth
save tempAnomalies, replace // Memory problems with preserve/restore

*preserve
	keep if exchcd == 1
	bys time_avail_m: egen temp = pctile(mve_c), p(20)
	keep time_avail_m temp
	duplicates drop
	save temp, replace
*restore
u tempAnomalies, clear
merge m:1 time_avail_m using temp, nogenerate
replace DelBreadth = . if mve_c < temp
drop temp
label var DelBreadth "Institutional Ownership"

// Residual Institutional Ownership interacted with various other anomalies
gen temp = instown_perc/100  // Check units here!
replace temp = 0 if mi(temp)
replace temp = .9999 if temp > .9999
replace temp = .0001 if temp < .0001

gen RIO = log(temp/(1-temp)) + 23.66 - 2.89*log(mve_c) + .08*(log(mve_c))^2

** Several strategies based on RIO
* these are independent double sorts
egen tempRIO = fastxtile(RIO), n(5) by(time_avail_m)
gen Turnover = vol/shrout

foreach v of varlist BM ForecastDispersion IdioRisk Turnover {
	egen temp`v'  = fastxtile(`v'), n(2) by(time_avail_m)
}

gen RIO_BM = 1 if tempRIO == 5 & tempBM == 1
replace RIO_BM = 0 if tempRIO == 1 & tempBM == 1

gen RIO_Disp = 1 if tempRIO == 5 & tempForecastDispersion == 2
replace RIO_Disp = 0 if tempRIO == 1 & tempForecastDispersion == 2

gen RIO_Turnover = 1 if tempRIO == 5 & tempTurnover == 2
replace RIO_Turnover = 0 if tempRIO == 1 & tempTurnover == 2

// note that idiorisk is has a flipped sign
gen RIO_IdioRisk = 1 if tempRIO == 5 & tempIdioRisk == 1
replace RIO_IdioRisk = 0 if tempRIO == 1 & tempIdioRisk == 1

drop temp* RIO
// 347 RIO and BM
label var RIO_BM "Inst Own and BM"
// 348 RIO and Analyst dispersion
label var RIO_Disp "Inst Own and Forecast Dispersion"
// 349 RIO and Turnover
label var RIO_Turnover "Inst Own and Turnover"
// 350 RIO and Idio Vol
label var RIO_IdioRisk "Inst Own and Idio Vol"


// 351 Shareholder activism proxy 1
gen tempBLOCK = maxinstown_perc if maxinstown_perc > 5
replace tempBLOCK = 0 if tempBLOCK == .
egen tempBLOCKQuant = fastxtile(tempBLOCK), n(4) by(time_avail_m)

gen tempEXT = 24 - G
replace tempEXT = . if G == . 
replace tempEXT = . if tempBLOCKQuant <= 3
replace tempEXT = . if !mi(shrcls) // Exclude dual class shares

gen Activism1 = tempEXT
label var Activism1 "Shareholder activism I: External Gov among Large Blockheld"

drop temp*

// 352 Shareholder activism proxy 2
gen tempBLOCK = maxinstown_perc if maxinstown_perc > 5
replace tempBLOCK = 0 if tempBLOCK == .

replace tempBLOCK = . if G == .
replace tempBLOCK = . if !mi(shrcls) // Exclude dual class shares

replace tempBLOCK = . if 24 - G < 19

gen Activism2 = tempBLOCK
label var Activism2 "Shareholder activism II: Blockholdings among High Ext Gov"

drop temp*


// 353 R&D Ability
xtset permno time_avail_m
gen tempRD = xrd/sale
replace tempRD = . if xrd <= 0
egen tempRDQuant = fastxtile(tempRD), n(3) by(time_avail_m)
gen RDAbility = Ability
replace RDAbility = . if tempRDQuant != 3
replace RDAbility = . if xrd <=0
cap drop temp*
label var RDAbility "R&D ability"


// 354 Real dirty surplus
gen temprecta = recta
replace temprecta = 0 if recta == .
gen DS = (msa - l12.msa) + (temprecta - l12.temprecta) + .65*(min(pcupsu - paddml,0) ///
                - min(l12.pcupsu - l12.paddml,0))
gen RDS = (ceq - l12.ceq) - DS - (ni - dvp) + divamt - prcc_f*(csho - l12.csho)
drop temprecta DS
label var RDS "Real dirty surplus"

// 355 Price delay
gen temp = l.PriceDelay  // Hou and Moskowitz skip one month
drop PriceDelay
rename temp PriceDelay
label var PriceDelay "Price delay"

// 355D1 Price delay (R2 based)
gen temp = l.PriceDelayRsq  // Hou and Moskowitz skip one month
drop PriceDelayRsq
rename temp PriceDelayRsq
label var PriceDelayRsq "Price delay (R2 based)"

// 355D3 Price delay (SE adjusted)
gen temp = l.PriceDelayAdj  // Hou and Moskowitz skip one month
drop PriceDelayAdj
rename temp PriceDelayAdj

gstats winsor PriceDelayAdj, by(time_avail_m) trim cuts(10 90) replace  // Trim very aggressively because coefficient/se not very well-behaved

label var PriceDelayAdj "Price delay (SE adjusted)"

// 356 Consistent earnings increase (quarterly version)
gen temp = ibq - l12.ibq
gen EarnIncrease = 1 if temp > 0 & l3.temp > 0 & l6.temp > 0 & l9.temp > 0 & l12.temp > 0 ///
               & !mi(temp) & !mi(l3.temp) & !mi(l6.temp) & !mi(l9.temp) & !mi(l12.temp)
replace EarnIncrease = 0 if mi(EarnIncrease) & !mi(temp) & !mi(l3.temp) ///
               & !mi(l6.temp) & !mi(l9.temp) & !mi(l12.temp)
drop temp
label var EarnIncrease "Consistent Earnings Increase (quarterly)"

// 357-358 Consistent positive/negative returns
gen ConsPosRet = 1 if (ret > 0 & l.ret > 0 & l2.ret > 0 & l3.ret > 0 & l4.ret > 0 ///
	& l5.ret > 0 & !mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret))
replace ConsPosRet = 0 if (!mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret)) ///
	& mi(ConsPosRet)
gen ConsNegRet = 1 if (ret < 0 & l.ret < 0 & l2.ret < 0 & l3.ret < 0 & l4.ret < 0 ///
	& l5.ret2 < 0)
replace ConsNegRet = 0 if (!mi(ret) & !mi(l.ret) & !mi(l2.ret) & !mi(l3.ret) & !mi(l4.ret) & !mi(l5.ret)) ///
	& mi(ConsNegRet)

label var ConsPosRet "Consistently positive return"
label var ConsNegRet "Consistently negative return"

// 359 Positive vs negative consistent returns
gen PosNegCons = 1 if ConsPosRet == 1
replace PosNegCons = 0 if ConsNegRet == 1
label var PosNegCons "Pos vs negative consistent return"

// 360 Excluded expenses
gen ExclExp = int0a - epspiq
winsor2 ExclExp, replace cut(1 99) trim
label var ExclExp "Excluded Expenses"

// 361 Deferred revenue
cap drop DelDRC
gen DelDRC = (drc - l12.drc)/(.5*(at + l12.at))
replace DelDRC = . if ceq <=0 | (drc == 0 & DelDRC == 0) | sale < 5 | (sic >=6000 & sic < 7000)  // (drc == 0 & DelDRC == 0) sets almost all to missing
												 // fn 8 says that it removes only a few??? http://pbfea2005.rutgers.edu/20thFEA/AccountingPapers/Session3/Prakash%20and%20Sinha.pdf

label var DelDRC "Deferred Revenue"

// 262 Accrual quality
gen AccrualQuality = l12.AQ  // Construction uses one year ahead operating cash flow so need to lag
label var AccrualQuality "Accrual Quality"

// 262q Accrual quality
gen AccrualQualityJune = AccrualQuality if month(dofm(time_avail_m)) == 6
bys permno (time_avail_m): replace AccrualQualityJune = AccrualQualityJune[_n-1] if mi(AccrualQualityJune)
label var AccrualQualityJune "Accrual Quality (June version)"


// 263 Accounting component of price delay
* timing: this is slow! 

gen tempSI = spi/(.5*(at + l12.at))
gen tempSurprise = meanest - EPSactualIBES
foreach n of numlist 12(12)48 {
	gen tempSurprise`n' = l`n'.tempSurprise
}
egen tempSD = rowsd(tempSurprise*)
egen tempN  = rowmiss(tempSurprise*)
replace tempSD = . if tempN > 2
gen tempES = abs(tempSurprise)/tempSD

gen DelayAcct = .
levelsof time_avail_m
foreach t of numlist `r(levels)' {
	cap drop tempU
	cap reg PriceDelay AccrualQuality tempSI tempES if time_avail_m == `t'
	cap predict tempU
	cap replace DelayAcct = tempU if e(sample)
}
cap drop temp*
label var DelayAcct "Accounting part price delay"

// 264 Non-accounting component of price delay
gen DelayNonAcct = PriceDelay - DelayAcct
label var DelayNonAcct "Non-Accounting part price delay"

// 365 Efficiency frontier
cap drop temp*
gen YtempBM = log(mve_c)
gen tempBook = log(ceq)
gen tempLTDebt = dltt/at
gen tempCapx = capx/sale
gen tempRD   = xrd/sale
gen tempAdv  = xad/sale
gen tempPPE = ppent/at
gen tempEBIT = ebitda/at
ffind sic, newvar(tempFF48) type(48)

gen logmefit_NS = .
levelsof time_avail_m
foreach t of numlist `r(levels)' {
	cap drop tempY
	cap reg YtempBM temp* i.tempFF48 if time_avail <= `t' & time_avail_m > `t' - 60
	cap predict tempY
	cap replace logmefit_NS = tempY if time_avail_m == `t'
}

cap drop temp*
gen Frontier = YtempBM - logmefit_NS
replace Frontier = -1*Frontier
label var Frontier "Efficient Frontier index"

// 366 Consistent earnings increase (continuous version)
gen chearn = ibq - l12.ibq

gen nincr = 0
replace nincr = 1 if chearn > 0 & l3.chearn <=0
replace nincr = 2 if chearn > 0 & l3.chearn >0 & l6.chearn <=0
replace nincr = 3 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn <=0
replace nincr = 4 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn <=0
replace nincr = 5 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn <=0
replace nincr = 6 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn <=0
replace nincr = 7 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn <=0
replace nincr = 8 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn >0 & l24.chearn <=0
drop chearn
rename nincr NumEarnIncrease
label var NumEarnIncrease "Number of consecutive earnings increases"


// 367 Institutional Ownership for stocks with high short interest
gen tempshortratio = shortint/shrout
replace tempshortratio = 0 if tempshortratio == .
sort time_avail_m
by time_avail_m: egen temps99 = pctile(shortint/shrout), p(99)

gen     temp = instown_perc
replace temp = 0 if mi(temp)
replace temp = . if tempshortratio < temps99

gen IO_ShortInterest = temp

cap drop temp*
label var IO_ShortInterest "Inst Onwership for high short interest"



// Intangible return (4 versions) 
gen tempAccBM = BM
gen tempAccSP = sale/mve_c
gen tempAccCFP = (ib + dp)/mve_c
gen tempAccEP = ni/mve_c

// Cumulative return (based on return adjusted for splits and dividends)
xtset permno time_avail_m
bys permno: gen tempCumRet = exp(sum(log(1+ ret2)))  
gen tempRet60 = (tempCumRet - l60.tempCumRet)/l60.tempCumRet
winsor2 tempRet60, replace cut(1 99) trim

foreach v of varlist tempAcc* {  // Loop over four measures

	gen `v'Ret = `v' - l60.`v' + tempRet60
	gen tempU_`v' = .
	
	levelsof time_avail_m  // Loop over cross-sectional regressions
	foreach t of numlist `r(levels)' {

		cap reg tempRet60 l60.`v' `v'Ret if time_avail_m == `t'
		cap predict tempResid, resid
		cap replace tempU_`v' = tempResid if time_avail_m == `t'
		cap drop tempResid
	}
}

// 368
rename tempU_tempAccBM IntanBM
label var IntanBM "Intangible return (BM)"

// 369
rename tempU_tempAccSP IntanSP
label var IntanSP "Intangible return (SP)"

// 370
rename tempU_tempAccCFP IntanCFP
label var IntanCFP "Intangible return (CFP)"

// 371
rename tempU_tempAccEP IntanEP
label var IntanEP "Intangible return (EP)"

cap drop temp*

// 372 Net equity finance
gen NetEquityFinance = (sstk - prstkc)/(.5*(at + l12.at))
replace NetEquityFinance = . if abs(NetEquityFinance) > 1
label var NetEquityFinance "Net Equity Finance"

// 373 Net debt finance
replace dlcch = 0 if mi(dlcch)
gen NetDebtFinance = (dltis - dltr - dlcch)/(.5*(at + l12.at))
replace NetDebtFinance = . if abs(NetDebtFinance) > 1
label var NetDebtFinance "NetDebtFinance"

// 374 Growth in advertising expenses
gen GrAdExp = log(xad) - log(l12.xad)
egen tempSize = fastxtile(mve_c), n(10) by(time_avail)
replace GrAdExp = . if xad < .1 | tempSize == 1
drop tempSize
label var GrAdExp "Growth in advertising expenses"

// 375 Gross Margin growth over sales growth
gen tempGM = sale-cogs
gen GrGMToGrSales =	((tempGM- (.5*(l12.tempGM + l24.tempGM)))/(.5*(l12.tempGM + l24.tempGM))) ///
	- ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)))
replace GrGMToGrSales =  ((tempGM-l12.tempGM)/l12.tempGM)- ((sale-l12.sale)/l12.sale) if mi(GrGMToGrSales)
drop tempGM
label var GrGMToGrSales "Gross Margin growth over sales growth"

// 376 Total assets to market 
gen AM = at/mve_c
label var AM "Total assets to market"

// 377 Change in current operating assets
gen tempAvAT = .5*(at + l12.at)
gen DelCOA = (act - che) - (l12.act - l12.che)
replace DelCOA = DelCOA/tempAvAT
label var DelCOA "Change in current operating assets"

// 378 Change in current operating liabilities
gen DelCOL = (lct - dlc) - (l12.lct - l12.dlc)
replace DelCOL = DelCOL/tempAvAT
label var DelCOL "Change in current operating liabilities"

// 379 Change in Long-term investment
gen DelLTI = ivao - l12.ivao
replace DelLTI = DelLTI/tempAvAT
label var DelLTI "Change in long-term investment"

// 380 Change in Financial Liabilities
gen tempPSTK = pstk
replace tempPSTK = 0 if mi(pstk)

gen DelFINL = (dltt + dlc + tempPSTK) - (l12.dltt + l12.dlc + l12.tempPSTK)
replace DelFINL = DelFINL/tempAvAT
label var DelFINL "Change in financial liabilities"
drop tempPSTK

// 381 Change in Equity
gen DelEqu = (ceq - l12.ceq)
replace DelEqu = DelEqu/tempAvAT
label var DelEqu "Change in common equity"

// 382 Payout yield
gen PayoutYield = (dvc + prstkc + max(pstkrv,0))/l6.mve_c
replace PayoutYield = . if PayoutYield <= 0
label var PayoutYield "Payout Yield"


// 383 Net Payout yield
gen NetPayoutYield = (dvc + prstkc - sstk)/mve_c
label var NetPayoutYield "Net Payout Yield"

// 384 Order backlog
gen OrderBacklog = ob/(.5*(at + l12.at))
replace OrderBacklog = . if ob == 0
label var OrderBacklog "Order Backlog"

// 385 Net debt to price
gen NetDebtPrice = ((dltt + dlc + pstk + dvpa - tstkp) - che)/mve_c
replace NetDebtPrice = . if sic >= 6000 & sic <= 6999
replace NetDebtPrice = . if mi(at) | mi(ib) | mi(csho) | mi(ceq) | mi(prcc_f)
* keep constant B/M, as i nTable 4
egen tempsort = fastxtile(BM), by(time_avail_m) n(5)
replace NetDebtPrice = . if tempsort <= 2
label var NetDebtPrice "Net debt to price ratio"
drop temp*

// 386 Abnormal Accruals
label var AbnormalAccruals "Abnormal Accruals"

// 386n Abnormal Accruals Percent
gen AbnormalAccrualsPercent = AbnormalAccruals*l12.at/abs(ni)
label var AbnormalAccrualsPercent "Abnormal Accruals (Percent)"


// 387 Analyst revisions
gen tempRev = (meanest - l.meanest)/abs(l.prc)
gen REV6 = tempRev + l.tempRev + l2.tempRev + l3.tempRev + l4.tempRev + l5.tempRev + l6.tempRev
label var REV6 "Earnings forecast revision"

// 388 R&D to sales
gen rd_sale =   l12.xrd/l12.sale  // Returns seem to be strongest in ht second year after portfolio formation (table IV of Chan et al paper)
replace rd_sale = . if rd_sale == 0
label var rd_sale "R&D-to-sales ratio"

// 389 Failure probability
cap drop temp*
gen tempMV = shrout*abs(prc)
gen tempTA = atq + .1*(tempMV - ceqq)
gen tempMV2 = tempMV
bys time_avail_m (tempMV2): gen tempRK = _N- _n + 1
replace tempMV2 = . if tempRK > 500 
egen tempTotMV = total(tempMV2), by(time_avail_m)  
gen tempRSIZE = log(tempMV/tempTotMV)
gen tempEXRET = log(1+ret) - log(1+mktrf)
gen tempNIMTA = ibq/(tempMV + ltq)
gen tempTLMTA = ltq/(tempMV + ltq)
gen tempCASHMTA = cheq/(tempMV + ltq)
winsor2 temp*, replace cut(5 95)

xtset permno time_avail_m
local rho = 2^(-1/3)
gen tempNIMTAAVG =( (1 - `rho'^3)/(1-`rho'^12))*(tempNIMTA + `rho'^3*l3.tempNIMTA + `rho'^6*l6.tempNIMTA + `rho'^9*l9.tempNIMTA)
gen tempEXRETAVG =( (1 - `rho')/(1-`rho'^12))*(tempEXRET + `rho'^1*l1.tempEXRET + `rho'^2*l2.tempEXRET + `rho'^3*l3.tempEXRET + ///
	`rho'^4*l4.tempEXRET + `rho'^5*l5.tempEXRET + `rho'^6*l6.tempEXRET + ///
	`rho'^7*l7.tempEXRET + `rho'^8*l8.tempEXRET + `rho'^9*l9.tempEXRET + `rho'^10*l10.tempEXRET + `rho'^11*l11.tempEXRET)
	
gen tempMB = tempMV/ceqq
gen tempPRICE = log(min(abs(prc), 15))

gen FailureProbability = -9.16 -.058*tempPRICE + .075*tempMB - 2.13*tempCASHMTA ///
	-.045*tempRSIZE + 100*1.41*IdioRisk - 7.13*tempEXRETAVG + 1.42*tempTLMTA - 20.26*tempNIMTAAVG  

cap drop temp*
label var FailureProbability "Failure Probability"

// 389f Failure probability (June version)
gen FailureProbabilityJune = FailureProbability if month(dofm(time_avail_m)) == 6
bys permno (time_avail_m): replace FailureProbabilityJune = FailureProbabilityJune[_n-1] if mi(FailureProbabilityJune)
label var FailureProbabilityJune "Failure Probability (June version)"

// 390 Composite debt issuance
gen tempBD = dltt + dlc
gen CompositeDebtIssuance = log(tempBD/l60.tempBD)
label var CompositeDebtIssuance "Composite Debt Issuance"

// 391 Capital turnover
gen CapTurnover = l12.sale/l24.at
label var CapTurnover "Capital turnover"

// 393 Conglomerate returns
label var retConglomerate "Conglomerate return"

// 394 Earnings Announcement returns
label var AnnouncementReturn "Earnings announcement return"

// 398 Tail risk beta
asreg ret tailex, window(time_avail_m 120) min(72) by(permno)
rename _b_tailex BetaTailRisk
drop _*
replace BetaTailRisk = . if shrcd > 11
label var BetaTailRisk "Tail risk beta"

// Industry lead lag returns/earnings surprises
ffind sic, newvar(tempFF48) type(48)
bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
save tempAnomalies, replace // intermediate save

	keep if tempRK >=.7 & !mi(tempRK)
	fcollapse (mean) ret EarningsSurprise, by(tempFF48 time_avail_m)
	rename ret IndRetBig
	rename EarningsSurprise EarnSupBig
	save temp,replace

use tempAnomalies, clear

merge m:1 tempFF48 time_avail_m using temp, nogenerate
replace IndRetBig = . if tempRK >= .7
replace EarnSupBig = . if tempRK >= .7
drop temp*
// 399
label var IndRetBig "Industry return big companies"
// 400
label var EarnSupBig "Industry Earnings surprise big companies"
 
// 401 Composite equity issuance
bys permno (time_avail): gen tempIdx = 1 if _n == 1
bys permno (time_avail): replace tempIdx = (1 + ret)*l.tempIdx if _n > 1
gen tempBH = (tempIdx - l60.tempIdx)/l60.tempIdx

gen CompEquIss = log(mve_c/l60.mve_c) - tempBH
cap drop temp*
label var CompEquIss "Composite Equity Issuance"

// 402 Jump Size
* Slope is created in 1b_DownloadOptionsAndProcess.R
gen SmileSlope = slope
label var SmileSlope "Average Jump Size"

// 403 Skewness of smirk
* see 1b_DownloadOptionsAndProcess
label var skew1 "Smirk skewness"

// 404-405 Option volume
*optVolume is from 1b_DownloadOptionsAndProcess
gen OptionVolume1 = optvolume/vol
replace OptionVolume1 = . if abs(prc) < 1 | shrcd > 11 | mi(l1.optvolume) | mi(l1.vol)
label var OptionVolume1 "Option Volume"

foreach n of numlist 1/6 {
	gen tempVol`n' = l`n'.OptionVolume1
	}
egen tempMean = rowmean(tempVol*)
gen OptionVolume2 = OptionVolume1/tempMean
label var OptionVolume2 "Option Volume (abnormal)"


*-----------------------------------------------------------------------------

// 200 Laborforce efficiency
gen temp = sale/emp
gen LaborforceEfficiency = (temp - l12.temp)/l12.temp
label var LaborforceEfficiency "Laborforce efficiency"
drop temp

// 201 Change in Noncurrent Operating Assets
gen temp = at - act - ivao
replace temp = at - act if mi(ivao)
gen ChNCOA = (temp - l12.temp)/l12.at
drop temp*
label var ChNCOA "Change in Noncurrent Operating Assets"


// 202 Change in Noncurrent Operating Liabilities
gen temp = lt - dlc - dltt
replace temp = lt - dlc if mi(dltt)
gen ChNCOL = (temp - l12.temp)/l12.at
drop temp*
label var ChNCOL "Change in Noncurrent Operating Liabilities"

// 203 Asset liquidity (book assets)
gen AssetLiquidityBook = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/l.at
label var AssetLiquidityBook "Asset liquidity (scaled by book value of assets)"

// 204 Asset liquidity (market assets)
gen AssetLiquidityMarket = (che + .75*(act - che) + .5*(at - act - gdwl - intan))/(l.at + l.prcc_f*l.csho - l.ceq)
label var AssetLiquidityMarket "Asset liquidity (scaled by market value of assets)"

// 205 Whited-Wu index (annual)
tostring sic, gen(tempSIC)
gen tempSIC3 = substr(tempSIC, 1, 3)
egen tempIndSales = total(sale), by(tempSIC3 time_avail_m)

* Divide CF and growth rates by 4 to approximate quarterly rates
gen WW = -.091* (ib+dp)/(4*at) -.062*(dvpsx_c>0 & !mi(dvpsx_c)) + .021*dltt/at ///
         -.044*log(at) + .102*(tempIndSales/l12.tempIndSales - 1)/4 - .035*(sale/l.sale - 1)/4
label var WW "Whited-Wu index (annual)"
drop temp*

// 206 Change in Capex over one year
replace capx = ppent - l12.ppent if capx ==. & FirmAge >=24
gen grcapx1y   = 	(l12.capx-l24.capx)/l24.capx 
label var grcapx1y "Change in capex (one year)" 

// 207 R&D capital to assets
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)

gen RDcap = (tempXRD + .8*l12.tempXRD + .6*l24.tempXRD + .4*l36.tempXRD + .2*l48.tempXRD)/at
replace RDcap = . if year < 1980

egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3) // OP: only works in small firms
replace RDcap = . if tempsizeq >= 2

label var RDcap "R&D capital to assets (for constrained only)"

// 208 Return Skewness
label var ReturnSkew "Return Skewness"

// 209 Return Skewness
label var ReturnSkewCAPM "Skewness of daily idiosyncratic returns (CAPM)"

// 210 Return Skewness
label var ReturnSkew3F "Skewness of daily idiosyncratic returns (3F model)"

// 210a Return Skewness
label var ReturnSkewQF "Skewness of daily idiosyncratic returns (Q factor model)"

// 211 Liquidity beta (return-return)
label var betaRR "Liquidity beta (return-return)"

// 212 Liquidity beta (ill-ill)
label var betaCC "Liquidity beta (ill-ill)"

// 213 Liquidity beta (return-ill)
label var betaRC "Liquidity beta (return-ill)"

// 214 Liquidity beta (return-return)
label var betaCR "Liquidity beta (ill-return)"

// 215 Liquidity beta (Net)
label var betaRR "Liquidity beta (Net)"

//216 Downside beta
label var DownsideBeta "Downside beta"

// 217 Brand capital 
label var BrandCapital "Brand capital to assets"

// 1217 Brand investment
gen BrandInvest = xad/l12.BrandCapital
label var BrandInvest "Brand investment rate"

// 218 6-moth residual momentum
label var ResidualMomentum6m "6 month residual momentum"

// 219 12-moth residual momentum
label var ResidualMomentum11m "11 month residual momentum"

// 220 Equity Duration
label var EquityDuration "Equity Duration"

// 221 Frazzini-Pedersen beta
label var BetaFP "Frazzini-Pedersen beta"

// 222 Dimson beta
label var BetaDimson "Dimson beta"

// 223 Pastor-Stambaugh liquidity beta
label var BetaLiquidityPS "Pastor-Stambaugh liquidity beta"

// 224 Long vs short-term earnings expectations
gen tempShort = 100* (meanest - fy0a)/abs(fy0a)
gen EarningsForecastDisparity = fgr5yr - tempShort
label var EarningsForecastDisparity "Long vs short-term earnings expectations"

// 227 Change in short-term investments
gen tempAvAT = .5*(at + l12.at)
gen DelSTI = ivst - l12.ivst
replace DelSTI = DelSTI/tempAvAT
label var DelSTI "Change in short-term investment"

// 228 Change in net financial assets
gen tempPSTK = pstk
replace tempPSTK = 0 if mi(pstk)

gen temp = (ivst + ivao) - (dltt + dlc + tempPSTK)  // Financial assets minus liabilities
gen DelNetFin = temp - l12.temp
replace DelNetFin = DelNetFin/tempAvAT
label var DelNetFin "Change in net financial assets"
drop temp*

// 230 Probability of Informed Trading
rename pin ProbInformedTrading
label var ProbInformedTrading "Probability of Informed Trading"
egen tempsize = fastxtile(mve_c), by(time_avail_m) n(2)
replace ProbInformedTrading = . if tempsize == 2
drop tempsize

// 231 Book leverage (annual)
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen BookLeverage = at/(tempSE + txditc - tempPS)
label var BookLeverage "Book leverage (annual)"
drop temp*

// 233 Earnings persistence
label var EarningsPersistence "Earnings Persistence"

// 234 Earnings predictability
label var EarningsPredictability "Earnings Predictability"

// 235 Earnings smoothness
label var EarningsSmoothness "Earnings smoothness"

// 236 Effective tax rate
replace am = 0 if mi(am)
gen tempTaxOverEBT = txt/(pi + am)
gen tempEarn = epspx/ajex
gen ETR = ( tempTaxOverEBT - 1/3*(l12.tempTaxOverEBT + l24.tempTaxOverEBT + l36.tempTaxOverEBT))*((tempEarn - l12.tempEarn)/l.prcc_f)
label var ETR "Effective Tax Rate"

// 237 Analyst value
gen FROE = (meanest*shrout)/ceq
replace FROE = . if abs(FROE) > 1  // Frankel and Lee, page 291

gen tempBM = ceq/mve_c
gen tempBMAve = (tempBM + l12.tempBM)/2
bys permno: replace tempBMAve = tempBM if _n <= 12

gen AnalystValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*tempBMAve
replace AnalystValue = . if ceq < 0 | abs(prc) < 1 | abs(ib/ceq) > 1 // Frankel and Lee, page 291
drop temp* FROE
label var AnalystValue "Analyst Value"

// 238 Intrinsic value
gen FROE = ib/ceq
replace FROE = . if abs(FROE) > 1  // Frankel and Lee, page 291
 
gen tempBM = ceq/mve_c
xtset permno time_avail_m // Andrew 2018 01
gen tempBMAve = (tempBM + l12.tempBM)/2
bys permno: replace tempBMAve = tempBM if _n <= 12
 
gen IntrinsicValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*tempBMAve
replace IntrinsicValue = . if ceq < 0 | abs(prc) < 1  // Frankel and Lee, page 291
drop temp* FROE
label var IntrinsicValue "Intrinsic Value"

// 239 Analyst Optimism
gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)
label var AOP "Analyst Optimism"

// 240 Predicted earnings forecast error
save tempAnomalies, replace // intermediate save
xtset permno time_avail_m
bys time_avail_m: relrank sale, gen(tempRKSale) ref(sale)
by time_avail_m: relrank BM, gen(tempRKBM) ref(BM)
by time_avail_m: relrank AOP, gen(tempRKAOP) ref(AOP)
 
gen FROE = (meanest*shrout)/ceq
by time_avail_m: relrank FROE, gen(tempRKFROE) ref(FROE)
 
gen tempError = ib/ceq - FROE
 
gen PredictedFE = .

xtset permno time_avail_m
gen tempLag36RKSale = l36.tempRKSale
gen tempLag36RKBM   = l36.tempRKBM
gen tempLag36RKAOP  = l36.tempRKAOP
gen tempLag36RKFROE  = l36.tempRKFROE

levelsof time_avail_m 
foreach t of numlist `r(levels)' {
    
    cap drop tempY
    cap reg tempError tempLag36RKSale tempLag36RKBM tempLag36RKAOP tempLag36RKFROE if time_avail_m == `t'
    cap predict tempY if time_avail_m == `t'
    cap replace PredictedFE = tempY if time_avail_m == `t'
}
drop temp*
label var PredictedFE "Predicted Forecast Error"

// 241 Value relevance of earnings
label var EarningsValueRelevance "Value relevance of earnings"

// 242 Earnings conservatism
label var EarningsConservatism "Earnings conservatism"

// 243 Earnings timeliness
label var EarningsTimeliness "Earnings timeliness"

// 244 Patents to RD
// ac: modified to be closer to the "size-adjustment" done in Table 6.  Also patched up a few other things.
gen tempXRD = xrd
replace tempXRD = 0 if mi(xrd)
gen tempnpat = l12.npat
replace tempnpat = 0 if mi(tempnpat)

gen tempPatentsRD = tempnpat/(l24.tempXRD + .8*l36.tempXRD + .6*l48.tempXRD + .4*l60.tempXRD + .2*l72.tempXRD)
gen PatentsRD = tempPatentsRD  // Takes into account that data have end-of-year timing
replace PatentsRD = . if mi(l24.xrd) | time_avail_m < ym(1982,1)  // Takes into account that xrd data standardized after 1975

egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(2) // imitating size adjutment: ideally this uses nyse breakpoints
replace PatentsRD = . if tempsizeq == 2

label var PatentsRD "Patents to RD capital"
drop temp*

// 245 Citations to RD
// ac: modified to be closer to the "size-adjustment" done in Table 6.  Also patched up a few other things.
gen tempXRD = xrd
replace tempXRD = 0 if mi(xrd)

gen tempncit = l12.ncitscale  // account for patent data being end of year
replace tempncit = 0 if tempncit == .
gen CitationsRD  = (tempncit + l12.tempncit + l24.tempncit + l36.tempncit + ///
                  l48.tempncit) / (l36.tempXRD + l48.tempXRD + l60.tempXRD + l72.tempXRD + l84.tempXRD)
replace CitationsRD = . if time_avail_m < ym(1982,1)  // Takes into account that xrd data standardized after 1975

egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(2) // imitating size adjutment: ideally this uses nyse breakpoints
replace CitationsRD = . if tempsizeq == 2

label var CitationsRD "Citations to RD expenses"

drop temp*
		  
// 246 Broker-Dealer Leverage Beta
label var BetaBDLeverage "Broker-Dealer Leverage Beta"

// 247 Customer momentum
rename custmom CustomerMomentum
label var CustomerMomentum "Customer momentum"

// 566 Return on net Operating Assets
gen tempOA = at - che - ivao
replace tempOA = at - che if mi(ivao)

foreach v of varlist dlc dltt mib pstk {
gen temp`v' = `v'
replace temp`v' = 0 if mi(`v')
}
gen tempOL = at - tempdlc - tempdltt - tempmib - temppstk - ceq
gen RetNOA = l12.oiadp/(l24.tempOA - l24.tempOL)
cap drop temp*
label var RetNOA "Return on Net Operating Assets"

// 601 Change in return on assets
gen tempRoa = ibq/atq
gen ChangeRoA = tempRoa - l12.tempRoa
cap drop temp*
label var ChangeRoA "Change in return on assets"

// 602 Change in return on equity
gen tempRoe = ibq/ceqq
gen ChangeRoE = tempRoe - l12.tempRoe
cap drop temp*
label var ChangeRoE "Change in return on equity"

// 603 Total accruals
foreach v of varlist ivao ivst dltt dlc pstk sstk prstkc dv {
	gen temp`v' = `v'
	replace temp`v' = 0 if mi(temp`v')
}

gen tempWc = (act - che) - (lct - tempdlc)
gen tempNc = (at - act - tempivao) - (lt - tempdlc - tempdltt)
gen tempFi = (tempivst + tempivao) - (tempdltt + tempdlc + temppstk)

gen TotalAccruals = (tempWc - l12.tempWc) + (tempNc - l12.tempNc) + (tempFi - l12.tempFi) if year <= 1989  // HXZ use 1988 here but that leads to break in data availability (perhaps because of lagged availability?)
replace TotalAccruals = ni - (oancf + ivncf + fincf) + (sstk - prstkc - dv) if year >1989

replace TotalAccruals = TotalAccruals/l12.at
cap drop temp*
label var TotalAccruals "Total Accruals"

// 604 Bid-ask spread (TAQ data)
rename tcost BidAskTAQ
label var BidAskTAQ "Bid-ask spread (TAQ data)"

// 605 IO customer momentum
gen temp = 1 if iomom_cust >= 10
replace temp = 0 if iomom_cust <= 1
replace temp = . if iomom_cust == .
replace iomom_cust = temp
label var iomom_cust "IO customer momentum"
drop temp


// 606 IO supplier momentum
gen temp = 1 if iomom_supp >= 10
replace temp = 0 if iomom_supp <= 1
replace temp = . if iomom_supp == .		
replace iomom_supp = temp
label var iomom_supp "IO supplier momentum"
drop temp	
	


// 555 Operating profits to lagged assets
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)

gen OperProfRD = (revt - cogs - xsga + tempXRD)/l12.at
label var OperProfRD "Operating profits to lagged assets"
drop temp*

// 555n Operating profits to assets
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)

gen OperProfRDNoLag = (revt - cogs - xsga + tempXRD)/at
label var OperProfRDNoLag "Operating profits to assets"
drop temp*

// 429 Inventory growth
gen InvGrowth = l12.invt/l24.invt - 1
label var InvGrowth "Inventory Growth"

// 316n Operating profits to lagged equity
gen tempprof = (revt - cogs - xsga - xint)/l12.ceq
egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3)
replace tempprof = . if tempsizeq == 1

gen OperProfLag = tempprof
cap drop temp*
label var OperProfLag "Operating Profits to lagged equity"


// 801 Industry-adjusted organizational capital
winsor2 OrgCap, suffix("temp") cuts(1 99) by(time_avail_m)
ffind sic, newvar(tempFF17) type(17)

egen tempMean = mean(OrgCaptemp), by(tempFF17 time_avail_m)
egen tempSD   = sd(OrgCaptemp), by(tempFF17 time_avail_m)

gen OrgCapAdj = (OrgCaptemp - tempMean)/tempSD
label var OrgCapAdj "Industry-adjusted organizational capital"

drop temp* OrgCaptemp

// 33n Gross Profitability (lagged assets)
gen GPlag 	=   (sale-cogs)/l12.at		
label var GPlag "Gross profitability (lagged assets)"

// 831 LT Forecast dispersion
gen ForecastDispersionLT = stdev5yr if numest5yr > 1 & !mi(numest5yr)
label var ForecastDispersionLT "LT EPS Forecast Dispersion"

// 56n Change in Net Operating Assets
gen tempOA = at - che
foreach v of varlist dltt dlc mib pstk {
    gen temp`v' = `v'
    replace temp`v' = 0 if mi(temp`v')
}

gen tempOL = at - tempdltt - tempmib - tempdlc - temppstk - ceq
gen tempNOA = tempOA - tempOL

gen dNoa = (tempNOA - l12.tempNOA)/l12.at
label var dNoa "Change in Net Operating Assets"
drop temp*

// 38a Industry concentration (Herfindahl, asset based)
cap drop sic3D
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works

egen indasset    = total(at), by(sic3D time_avail_m)
gen temp  	= (at/indasset)^2
egen tempHerf 	= total(temp), by(sic3D time_avail_m)
bys permno: asrol tempHerf, gen(HerfAsset) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average
replace HerfAsset = . if shrcd > 11

* Missing if regulated industry (Barclay and Smith 1995 definition)
replace HerfAsset = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace HerfAsset = . if tempSIC == "4512" & year <=1978 
replace HerfAsset = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace HerfAsset = . if substr(tempSIC, 1,2) == "49"
drop temp* indasset
label var HerfAsset "Industry concentration (asset based)"

// 38b Industry concentration (Herfindahl, equity based)
cap drop sic3D
tostring sicCRSP, gen(tempSIC)
gen sic3D = substr(tempSIC,1, 4) // for some reason sic3 isn't working anymore, but sic4 works

* Compute book equity
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen tempBE = tempSE + txditc - tempPS

egen indequity    = total(tempBE), by(sic3D time_avail_m)
gen temp  	= (tempBE/indequity)^2
egen tempHerf 	= total(temp), by(sic3D time_avail_m)
bys permno: asrol tempHerf, gen(HerfBE) stat(mean) window(time_avail_m 36) min(12)  // Take 3 year moving average
replace HerfBE = . if shrcd > 11

* Missing if regulated industry (Barclay and Smith 1995 definition)
replace HerfBE = . if (tempSIC == "4011" | tempSIC == "4210" | tempSIC == "4213" ) &  year <=1980 
replace HerfBE = . if tempSIC == "4512" & year <=1978 
replace HerfBE = . if (tempSIC == "4812" | tempSIC == " 4813") &  year <= 1982
replace HerfBE = . if substr(tempSIC, 1,2) == "49"
drop temp* indequity
label var HerfAsset "Industry concentration (book equity based)"

// 899 PPE and inventory changes to assets
gen tempPPE = ppegt - l12.ppegt
gen tempInv = invt  - l12.invt 

gen InvestPPEInv = (tempPPE + tempInv)/l12.at
label var InvestPPEInv "PPE and inventory changes to assets"
drop temp*

// 898 BM with December market equity
cap drop temp*
gen tempME = abs(prc)*shrout if month(dofm(time_avail_m)) == 12
gen tempYear = yofd(dofm(time_avail_m))
egen tempDecME = min(tempME), by(permno tempYear)

* Compute book equity
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen tempBE = tempSE + txditc - tempPS

gen BMdec = tempBE/l12.tempDecME if month(dofm(time_avail_m)) > = 6
replace BMdec = tempBE/l17.tempDecME if month(dofm(time_avail_m)) < 6

label var BMdec "Book-to-market (December market equity)"
drop temp*

// 406 Cash-based operating profitability
* this should be last to avoid conflicts - Andrew 2018 04 
foreach v of varlist revt cogs xsga xrd rect invt xpp drc drlt ap xacc {
	replace `v' = 0 if mi(`v')
}

gen CBOperProf = (revt - cogs - (xsga - xrd)) - ///
	(rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + ///
	(drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
replace CBOperProf = CBOperProf/l12.at

replace CBOperProf = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(at) | (sic >= 6000 & sic < 7000)
label var CBOperProf "Cash-based Operating Profitability"

// 406a Cash-based operating profitability
gen CBOperProfNoLag = (revt - cogs - (xsga - xrd)) - ///
	(rect - l12.rect) - (invt - l12.invt) - (xpp - l12.xpp) + ///
	(drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
replace CBOperProfNoLag = CBOperProfNoLag/at

replace CBOperProfNoLag = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(at) | (sic >= 6000 & sic < 7000)
label var CBOperProfNoLag "Cash-based Operating Profitability (no lag)"

*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* Quarterly version of (some) annual signals

// 225 Asset liquidity (book assets)
replace gdwlq = 0 if mi(gdwlq)
replace intanq = 0 if mi(intanq)
gen AssetLiquidityBookQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/l.atq
label var AssetLiquidityBookQuart "Quarterly Asset liquidity (scaled by book value of assets)"

// 226 Asset liquidity (market assets)
gen AssetLiquidityMarketQuart = (cheq + .75*(actq - cheq) + .5*(atq - actq - gdwlq - intanq))/(l.atq + l.prccq*l.cshoq - l.ceqq)
label var AssetLiquidityMarketQuart "Quarterly asset liquidity (scaled by market value of assets)"


// 10q Book-to-market (quarterly)
gen BMq 		=	log(ceqq/mve_c)
label var BMq "Book-to-market quarterly"

// 232 Book leverage (quarterly)
replace txditcq = 0 if mi(txditcq)
gen tempSE = seqq
replace tempSE = ceqq + pstkq if mi(tempSE)
replace tempSE = atq - ltq if mi(tempSE)

gen BookLeverageQuarterly = atq/(tempSE + txditcq - pstkq)
label var BookLeverageQuarterly "Book leverage (quarterly)"
drop temp*

// 11q Cash-flow to market (quarterly)
gen CFq 		= (ibq + dpq)/mve_c
label var CFq "Cash-flow to market (quarterly)"


// 24q Earnings-to-Price ratio (quarterly)
gen EPq 		= ibq/l6.mve_c
replace EPq  = . if EPq < 0
label var EPq "Earnings-to-price ratio (quarterly)"
cap drop temp*

// 46q Market leverage (quarterly)
gen Leverage_q = ltq/mve_c
label var Leverage_q "Market leverage (quarterly)"

// 376q Total assets to market (quarterly)
gen AMq = atq/mve_c
label var AMq "Total assets to market (quarterly)"

// 7q Asset Turnover (quarterly)
gen temp = (rectq + invtq + acoq + ppentq + intanq - apq - lcoq - loq) 
gen AssetTurnover_q = saleq/((temp + l12.temp)/2)
drop temp
replace AssetTurnover_q = . if AssetTurnover_q < 0
label var AssetTurnover_q "Asset Turnover (quarterly)"

// 6q Asset Growth (quarterly)
gen AssetGrowth_q = (atq - l12.atq)/l12.atq 
label var AssetGrowth_q "Asset Growth (quarterly)"

// 341q Kaplan-Zingales Index (quarterly)
gen tempTX = txdiq
replace tempTX = 0 if mi(tempTX)
gen temp = divamt
replace temp = 0 if divamt ==.

gen KZ_q = -1.002* (ibq + dpq)/atq + .283*(atq + mve_c - ceqq - tempTX)/atq + 3.319*(dlcq + dlttq)/(dlcq + dlttq + ceqq) ///
 - 39.368*(temp/atq) - 1.315*(cheq/atq)
cap drop temp*
label var KZ_q "Kaplan-Zingales index (quarterly)"

// 385q Net debt to price (quarterly)
gen NetDebtPrice_q = ((dlttq + dlcq + pstkq) - cheq)/mve_c
replace NetDebtPrice_q = . if sic >= 6000 & sic <= 6999
replace NetDebtPrice_q = . if mi(atq) | mi(ibq) | mi(csho) | mi(ceqq) | mi(prcc_f)
* keep constant B/M, as in Table 4
egen tempsort = fastxtile(BM), by(time_avail_m) n(5)
replace NetDebtPrice_q = . if tempsort <= 2
label var NetDebtPrice_q "Net debt to price ratio (quarterly)"
drop temp*

// 382q Payout yield (quarterly)
gen tempDiv = dvpsxq*cshoq*ajexq 
gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq) // See 1_PrepareQuarterlyCS for treatment of year-to-date variables
gen PayoutYield_q = tempTotalPayout/l6.mve_c
replace PayoutYield_q = . if PayoutYield_q <= 0
cap drop temp*
label var PayoutYield_q "Payout Yield (quarterly)"

// 383q Net Payout yield (quarterly)
gen tempDiv = dvpsxq*cshoq*ajexq 
gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq) // See 1_PrepareQuarterlyCS for treatment of year-to-date variables

gen NetPayoutYield_q = (tempTotalPayout - sstkyq - (pstkq - l3.pstkq))/mve_c
cap drop temp*
label var NetPayoutYield_q "Net Payout Yield (quarterly)"

// 21q Dividend Yield (quarterly)
gen temp = divamt
replace temp = 0 if divamt ==.
gen DivYield_q = (temp + l1.temp + l2.temp)/abs(prc)
	
egen tempsize = fastxtile(mve_c), by(time_avail_m) n(4)	
replace DivYield_q = . if tempsize >= 3	// see table 1B

cap drop temp*
label var DivYield_q "Dividend Yield (quarterly)"

// 305q Cash flow to price (quarterly) 
gen tempaccrual_level = (actq-l12.actq - (cheq-l12.cheq)) - ( (lctq-l12.lctq)- ///
                (dlcq-l12.dlcq)-(txpq-l12.txpq)-dpq )  
gen cfpq =(ibq - tempaccrual_level )/ mve_c       
replace cfpq = oancfyq/mve_c if oancfyq !=.
label var cfpq "Cash flow to price (quarterly)"


// 27q Enterprise component of BM (quarterly)
gen temp = cheq - dlttq - dlcq - pstkq
gen EBM_q = (ceqq + temp)/(mve_c + temp)
drop temp
label var EBM_q "Enterprise component of BM (quarterly)"

// 28q Enterprise Multiple
gen EntMult_q = (mve_c + dlttq + dlcq + pstkq - cheq)/oibdpq
replace EntMult_q = . if ceqq < 0 | oibdpq < 0  // This screen come from Loughran and Wellman's paper, MP don't mention them.
label var EntMult_q "Enterprise Multiple (quarterly)"

// 59q Operating Leverage (quarterly)
gen tempxsga		= 0
replace tempxsga 	= xsgaq if xsgaq !=.
gen OPLeverage_q = (tempxsga + cogsq)/atq
label var OPLeverage_q "Operating Leverage (quarterly)"
drop temp*

// 69q R&D to market cap (quarterly)
gen RD_q 	=   xrdq/mve_c					
label var RD_q "R&D-to-market cap (quarterly)"

// 388q R&D to sales (quarterly)
gen rd_sale_q =  l12.xrdq/l12.saleq  
replace rd_sale_q = . if rd_sale_q == 0
label var rd_sale_q "R&D-to-sales ratio (quarterly)"

// 334q Quarterly sales growth
gen sgr_q 	= 	(saleq/l12.saleq)-1
label var sgr_q "Quarterly sales growth"

// 73q Sales-to-price ratio (quarterly)
gen SP_q 		=   saleq/mve_c
label var SP_q "Sales-to-price ratio (quarterly)"

// 345q Tangibility (quarterly)
/*
save tempAnomalies, replace // Memory problems with preserve/restore

	drop if sicCS < 2000 | sicCS > 3999  // Manufacturing firms only
	egen tempFC = fastxtile(at), n(10) by(time_avail_m)
	gen FC = 1 if tempFC <=3  // Lower three deciles are defined as financially constrained
	replace FC = 0 if tempFC >=8 & !mi(tempFC)
	save temp, replace

u tempAnomalies, clear
merge 1:1 permno time_avail_m using temp, keepusing(FC) nogenerate
*/

gen tang_q = 	(cheq + .715*rectq + .547*invtq + .535*ppegtq)/at 
label var tang_q "Tangibility (quarterly)"

// 84q Taxes
gen Tax_q = piq/niq if piq >0 & niq >0
label var Tax_q "Taxable income to income"

// 229 Quarter Whited-Wu index
tostring sic, gen(tempSIC)
gen tempSIC3 = substr(tempSIC, 1, 3)
egen tempIndSales = total(saleq), by(tempSIC3 time_avail_m)

gen WW_Q = -.091* (ibq+dpq)/atq -.062*(dvpsxq>0 & !mi(dvpsxq)) + .021*dlttq/atq ///
         -.044*log(atq) + .102*(tempIndSales/l3.tempIndSales - 1) - .035*(saleq/l.saleq - 1)
label var WW_Q "Whited-Wu index (quarterly)"
drop temp*

// 91q Altman Z-Score (quarterly)
gen ZScore_q = 1.2*(actq - lctq)/atq + 1.4*(req/atq) + 3.3*(niq + xintq + txtq)/at + ///
	.6*(mve_c/ltq) + revtq/atq
replace ZScore_q = . if (sic >3999 & sic < 4999) | sic > 5999
* returns are non-monotonic (see Panel A of original), so we want to exclude
* the lowest quintile of ZScores
egen tempsort = fastxtile(ZScore_q), by(time_avail_m) n(5)	
replace ZScore_q = . if tempsort == 1	
label var ZScore_q "Altman Z-Score (quarterly)"
drop tempsort

// 66q Profit Margin (quarterly)
gen PM_q = niq/revtq
label var PM_q "Profit Margin (quarterly)"

// 566q Return on net Operating Assets (quarterly)
gen tempOA = atq - cheq - ivaoq
replace tempOA = atq - cheq if mi(ivaoq)

foreach v of varlist dlcq dlttq mibq pstkq {
gen temp`v' = `v'
replace temp`v' = 0 if mi(`v')
}
gen tempOL = atq - tempdlcq - tempdlttq - tempmibq - temppstkq - ceqq
gen RetNOA_q = oiadpq/(l3.tempOA - l3.tempOL)
cap drop temp*
label var RetNOA_q "Return on Net Operating Assets (quarterly)"

// 36q Piotroski F-score (quarterly)
replace foptyq = oancfyq if foptyq == .
gen p1 = 0
replace p1 = 1 if ibq > 0 | !mi(ibq)
gen p2 = 0
replace p2 = 1 if (oancfyq > 0  & !mi(oancfyq)) | (mi(oancfyq) & !mi(foptyq) & foptyq > 0)
gen p3 = 0
replace p3 = 1 	if (ibq/atq - l12.ibq/l12.atq)>0
gen p4 = 0
replace p4 = 1 if oancfyq > ibq
gen p5 = 0
replace p5 = 1 if dlttq/atq - l12.dlttq/l12.atq < 0
gen p6 = 0
replace p6 = 1 if actq/lctq - l12.actq/l12.lctq > 0
gen p7 = 0
gen tempebit = ibq + txtq + xintq
replace p7 = 1 if tempebit/saleq - tempebit/l12.saleq > 0
gen p8 = 0
replace p8 = 1 if saleq/atq - l12.saleq/l12.atq>0
gen p9 = 0
replace p9 = 1 if shrout <= l12.shrout  // this can be the same as in annual version
  
gen PS_q = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
drop p1 p2 p3 p4 p5 p6 p7 p8 p9
replace PS_q = . if foptyq == . | ibq == . | atq == . | dlttq == . | saleq == . | actq == . ///
	| tempebit == . | shrout == .
drop tempebit

egen temp = fastxtile(BM), by(time_avail_m) n(5)  // Find highest BM quintile
replace PS_q =. if temp != 5

drop temp
label var PS_q "Piotroski F-score (quarterly)"

// 61q O-Score (quarterly)		
replace foptyq = oancfyq if foptyq == .
gen OScore_q = -1.32 - .407*log(atq/gnpdefl) + 6.03*(ltq/atq) - 1.43*( (actq - lctq)/atq) + ///
	.076*(lctq/actq) - 1.72*(ltq>atq) - 2.37*(ibq/atq) - 1.83*(foptyq/ltq) + .285*(ibq + l12.ibq <0) - ///
	.521*( (ibq - l12.ibq)/(abs(ibq) + abs(l12.ibq)) )
destring sic, replace
replace OScore_q = . if (sic > 3999 & sic < 5000) | sic > 5999  | abs(prc) < 5 	

* exclude the lowest quintile of OScores
egen tempsort = fastxtile(OScore_q), by(time_avail_m) n(5)	
replace OScore_q = . if tempsort == 1	

label var OScore_q "O-Score (quarterly)"	

// 311a Change in Capex over three years
replace capx = ppent - l12.ppent if capx ==. & FirmAge >=24
gen grcapx3y 	= 	(capx-l36.capx)/l36.capx 
label var grcapx3y "Change in capex (three years)" 

// 316q Quarterly operating profits to laggedd equity
foreach v of varlist cogsq xsgaq xintq {
    gen temp_`v' = `v'
    replace temp_`v' = 0 if mi(`v')
}

gen OperProfLag_q = revtq - temp_cogsq - temp_xsgaq - temp_xintq
replace OperProfLag_q = . if mi(cogsq) & mi(xsgaq) & mi(xintq)

* Shareholder equity
gen tempSE = seqq
replace tempSE = ceqq + pstkq if mi(tempSE)
replace tempSE = atq - ltq if mi(tempSE)

* Final signal
replace OperProfLag_q = OperProfLag_q/(tempSE + txditcq - pstkq)
replace OperProfLag_q = OperProfLag_q/(tempSE - pstkq) if mi(txditcq)

label var OperProfLag_q "Quarterly operating profits to lagged equity"
drop temp*

// 391q Capital turnover (quarterly)
gen CapTurnover_q = saleq/l3.atq
label var CapTurnover "Capital turnover (quarterly)"

// 33q Gross Profitability (quarterly)
gen GPlag_q 	=   (revtq - cogsq)/l3.atq		
label var GPlag_q "Gross profitability (quarterly)"

// 406q Cash-based operating profitability (quarterly)
* this should be last to avoid conflicts - Andrew 2018 04 
foreach v of varlist revtq cogsq xsgaq xrdq rectq invtq drcq drltq apq xaccq {
	replace `v' = 0 if mi(`v')
}

gen CBOperProf_q = (revt - cogs - (xsga - xrd)) - ///
	(rect - l12.rect) - (invt - l12.invt) + ///
	(drc + drlt - l12.drc - l12.drlt) + (ap - l12.ap) + (xacc - l12.xacc)
replace CBOperProf_q = CBOperProf_q/l3.atq

replace CBOperProf_q = . if shrcd > 11 | mi(mve_c) | mi(BM) | mi(atq) | (sic >= 6000 & sic < 7000)
label var CBOperProf_q "Cash-based Operating Profitability (quarterly)"

// 555q Operating profits to lagged assets
gen tempXRD = xrdq
replace tempXRD = 0 if mi(tempXRD)

gen OperProfRD_q = (revtq - cogsq - xsgaq + tempXRD)/l3.atq
label var OperProfRD_q "Operating profits to lagged assets (quarterly)"
drop temp*


*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* NYSE indicator
gen NYSE = exchcd == 1

* ------- Future buy and hold returns ---------------------------------------
gen bh1m  = f.ret

* XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
* X Some clean-up now and we're almost done
* XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


* Would be better to do anomaly selection programmatically using SignalDocumentation.xlsx
* but can't figure out how this works with Stata
#delimit ;

keep gvkey permno time_avail_m bh1m mve_c prc NYSE exchcd ret

High52
Accruals
AdExp
Illiquidity
AssetGrowth
AssetGrowth_q
AssetTurnover
AssetTurnover_q
Beta
BidAskSpread
BM
BMq
CF
CFq
VarCF
ChAssetTurnover
ChPM
ChangeInRecommendation
Coskewness
CredRatDG
DebtIssuance
DivInit
DivOmit
DivYield
DivYield_q
DivInd
DownForecast
EP
EarningsConsistency
EarningsSurprise
EBM
EntMult
EBM_q
EntMult_q
ExchSwitch
FirmAge
FirmAgeMom
G_Binary
GP
ChInv
GrLTNOA
PS
MS
Herf
std_turn
zerotrade
IndMom
IndIPO
Investment
AgeIPO
RDIPO
IntMom
Leverage
BPEBM
Mom36m
AccrualsBM
MaxRet
Mom6m
MomRev
MomVol
NOA
ChNWC
ChNNCOA
OPLeverage
OPLeverage_q
OrgCap
OScore
FR
PctAcc
PctTotAcc
Price
PM
Profitability
RD
RD_q
RoE
RevenueSurprise
MeanRankRevGrowth
SP
SP_q
MomSeas
ShareIss1Y
ShareIss5Y
ShareRepurchase
ShareVol
ShortInterest
Mom1m
Size
Spinoff
ChEQ
Tax
XFIN
SurpriseRD
UpForecast
VolMkt
VolumeTrend
VolSD
ZScore
ChInvIA
GrSaleToGrInv
GrSaleToGrOverhead
BetaTailRisk
ReturnSkew
ReturnSkewCAPM
ReturnSkew3F
betaRR
betaCC
betaRC
betaCR
betaNet
DownsideBeta
BrandCapital
ResidualMomentum6m
ResidualMomentum11m
EquityDuration
BetaFP
BetaDimson
BetaLiquidityPS
EarningsPredictability
EarningsSmoothness
EarningsValueRelevance
EarningsTimeliness
EarningsConservatism
PatentsRD
CitationsRD
BetaBDLeverage
CustomerMomentum
AccrualQuality
DelayAcct
DelayNonAcct
BetaSquared
Cash
cashdebt
CashProd
cfp
cfpq
ChNAnalyst
ChTax
ConvDebt
depr
DolVol
grcapx
hire
Mom12m
nanalyst
OperProf
currat
pchcurrat
invest
GrSaleToGrReceivables
pchgm_pchsale
pchdepr
quick
realestate
roaq
pchquick
roavol
roic
salecash
salerec
saleinv
secured
securedind
sgr
sinOrig
sinAlgo
pchsaleinv
IdioRisk
KZ
KZ_q
sfe
fgr5yrLag
ConsRecomm
tang
DelBreadth
RIO_BM
RIO_Disp
RIO_Turnover
RIO_IdioRisk
Activism1
Activism2
RDAbility
Mom18m13m
RDS
PriceDelay
EarnIncrease
ConsPosRet
ConsNegRet
PosNegCons
ExclExp
DelDRC
Frontier
NumEarnIncrease
IO_ShortInterest
IntanBM
IntanSP
IntanCFP
IntanEP
NetEquityFinance
NetDebtFinance
GrAdExp
GrGMToGrSales
AM
AMq
DelCOA
DelCOL
DelLTI
DelFINL
DelEqu
PayoutYield
PayoutYield_q
NetPayoutYield
NetPayoutYield_q
OrderBacklog
NetDebtPrice
NetDebtPrice_q
AbnormalAccruals
REV6
rd_sale
FailureProbability
CompositeDebtIssuance
CapTurnover
retConglomerate
AnnouncementReturn
BetaTailRisk
IndRetBig
EarnSupBig
CompEquIss
SmileSlope
skew1
OptionVolume1
OptionVolume2
CBOperProf
CBOperProf_q
ChForecastAccrual
ForecastDispersion
Mom6mJunk
LaborforceEfficiency
ChNCOA
ChNCOL
AssetLiquidityBook
AssetLiquidityMarket
WW
grcapx1y
RDcap
BrandInvest
EarningsForecastDisparity
AssetLiquidityBookQuart
AssetLiquidityMarketQuart
DelSTI
DelNetFin
WW_Q
ProbInformedTrading
BookLeverage
BookLeverageQuarterly
EarningsPersistence
ETR
AnalystValue
IntrinsicValue
AOP
PredictedFE
Leverage_q
rd_sale_q
sgr_q
tang_q
Tax_q
ZScore_q
PM_q
RetNOA
RetNOA_q
ChangeRoA
ChangeRoE
PS_q
OScore_q
TotalAccruals
BidAskTAQ
ReturnSkewQF
IdioVolCAPM
IdioVol3F
IdioVolQF
IdioVolAHT
betaVIX
iomom_cust
iomom_supp
EPq
grcapx3y
CBOperProfNoLag
OperProfRD
OperProfRD_q
OperProfRDNoLag
InvGrowth
OrgCapAdj
OperProfLag
OperProfLag_q
FRbook
AbnormalAccrualsPercent
CapTurnover_q
MomSeasAlt1a
MomSeasAlt1n
MomSeasAlt2to5n
MomSeasAlt6to10a
MomSeasAlt6to10n
MomSeasAlt11to15a
MomSeasAlt11to15n
MomSeasAlt16to20a
MomSeasAlt16to20n
GPlag
GPlag_q
ForecastDispersionLT
dNoa
HerfAsset
HerfBE
zerotradeAlt1
zerotradeAlt12
InvestPPEInv
BMdec
PriceDelayRsq
PriceDelayAdj
fgr5yrLagJune
FailureProbabilityJune
AccrualQualityJune
;

#delimit cr

compress  
save "$pathProject/DataClean/AnomaliesAll", replace

* Save as CSV 

// Metadata
preserve
	keep gvkey permno time_avail_m ret mve_c prc NYSE exchcd
	order gvkey permno time_avail_m ret mve_c prc NYSE exchcd
	export delimited using "$pathProject/DataClean/SignalFirmMonthMetaData.csv", replace 
restore

// Signals
drop gvkey ret mve_c prc NYSE exchcd bh1m
order permno time_avail_m 
export delimited using "$pathProject/DataClean/SignalFirmMonth.csv", replace 

*******************************************************************************

erase tempAnomalies.dta
erase temp.dta

timer off 1
timer list 1
