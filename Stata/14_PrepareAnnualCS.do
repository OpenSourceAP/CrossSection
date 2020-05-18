** Pre-processing the annual Compustat dataset
timer clear
timer on 1

import delimited "$pathProject/DataRaw/CompustatAnnual.csv", clear

** Preliminaries
gen time_d = date(datadate, "YMD")
format time_d %td

* Require some reasonable amount of information
drop if at ==. | prcc_c ==. | ni ==.

* 6 digit CUSIP
gen cnum = substr(cusip,1,6)

* ----------------------------------------------------------------------------
* Replace missing values if reasonable
* ----------------------------------------------------------------------

gen dr = . // Deferred revenue
replace dr = drc + drlt if drc !=. & drlt !=.    // drc  = deferred revenue current 
replace dr = drc 		if drc !=. & drlt ==.  // drlt = deferred revenue long-term
replace dr = drlt 		if drc ==. & drlt !=.

// dcpstk = convertible debt and preferred stock, pstk = preferred stock, dcvt = convertible debt
gen dc 		= dcpstk - pstk if dcpstk > pstk & pstk !=. & dcpstk !=. & dcvt ==. // convertible debt
replace dc	= dcpstk 		if pstk ==. & dcpstk !=. & dcvt ==.
replace dc 	= dcvt 			if dc ==.

// xint = interest and related expense - Total
gen xint0 		= 0
replace xint0 	= xint if xint !=.
// xsga = Selling, general and administrative expenses
gen xsga0		= 0
replace xsga0 	= xsga if xsga !=.

// For these variables, missing is assumed to be 0
foreach v of varlist nopi dvt ob dm dc aco ap intan ao lco lo rect ///
				invt drc spi gdwl fatl fatb che dp act lct tstk dvpa scstkc sstk mib ///
				ivao prstkc prstkcc txditc ivst {
				
	replace `v' = 0 if `v' ==.
	
}

// Add identifiers for merging
joinby gvkey using "$pathProject/DataClean/CCMLinkingTable", update

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= time_d  & time_d <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp

*------------------------------------------------------------------------------
// Compute Ability measure of Cohen, Dieter and Malloy (2013)
gen tempXRD = xrd
replace tempXRD = . if tempXRD <0
gen tempSale = sale
replace tempSale = . if tempSale < 0

xtset gvkey fyear
gen tempY = log(tempSale/l.tempSale)
gen tempX = log(1 + tempXRD/tempSale)

gen tempNonZero = .           // paper requires that "half of R&D observations"
                              // are non-zero". 
gen tempXLag = .
foreach n of numlist 1/5 {
	replace tempXLag = l`n'.tempX

    asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)
	rename _b_tempXLag gammaAbility`n'
	drop _*
	
	replace tempNonZero = tempXLag >0 & !mi(tempXLag) 
    asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)
	replace gammaAbility`n' = . if tempMean < .5 & !mi(tempMean)
	drop tempMean
}

drop temp*

egen Ability = rowmean(gammaAbil*)


*------------------------------------------------------------------------------
// Compute Accrual Quality (AQ) for Francis et al (2005) and  Callen, Khan and Lu (2011)
gen tempAccruals = ( (act - l.act) - (che - l.che) - ( (lct - l.lct) - ///
	(dlc - l.dlc)  ) - dp) / ( (at + l.at)/2)
gen tempCAcc = tempAccruals + dp/( (at + l.at)/2)	
gen tempRev = sale/( (at + l.at)/2)
gen tempDelRev = tempRev - l.tempRev
gen tempPPE = ppegt/( (at + l.at)/2)
gen tempCFO = ib/( (at + l.at)/2) - tempAccruals

* Run regressions for each year and industry
ffind sic, newvar(FF48) type(48)
gen tempResid = .
levelsof fyear
foreach y of numlist `r(levels)' {
	foreach ind of numlist 1/48 {
		cap drop tempU
		cap reg tempCAcc l(-1/1).tempCFO tempDelRev tempPPE if fyear == `y' & FF48 == `ind'
		cap predict tempU if e(sample), resid
		cap replace tempResid = tempU if e(sample)
	}
}
bys fyear FF48: replace tempResid = . if _N < 20  // At least 20 observations per year and industry required

* Rolling standard deviation
xtset gvkey fyear
foreach n of numlist 1/4 {
	gen tempResid`n' = l`n'.tempResid
}

egen AQ = rowsd(tempResid*)
egen tempN = rowmiss(tempResid*)	
replace AQ = . if tempN > 1
mdesc AQ
cap drop temp* FF48

*------------------------------------------------------------------------------
// Francis, Schipper et al measures that are based on 15-month returns

* Compute 15 month return (with 12 month past returns and 3 months future return)
* This will be matched to end of fiscal year, and then lagged to make sure
* data are actually available

preserve

	import delimited "$pathProject/DataRaw/mCRSP.csv", clear

	*create monthly date
	gen time_d = date(date,"YMD")
	format time_d %td
	gen time_m = mofd(time_d)
	format time_m %tm
	drop time_d

	* Incorporate delisting return
	replace dlret = -.35 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
		& (exchcd == 1 | exchcd == 2)

	replace dlret = -.55 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
		& exchcd == 3  // GHZ cite Johnson and Zhao (2007), Shumway and Warther (1999)

	replace dlret = -1 if dlret < -1 & dlret !=.

	replace dlret = 0 if dlret ==.

	replace ret = ret + dlret

	replace ret = dlret if ret ==. & dlret !=0

	bysort permno time_m: keep if _n == 1   // This should not delete observations
	xtset permno time_m

	replace ret = 0 if mi(ret)
	gen tempMom15m = ( (1+f2.ret)*(1+f.ret)*(1+ret)*(1+l.ret)*(1+l2.ret)* ///
					(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)* ///
					(1+ l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret) ) - 1

	gen tempmktcap = abs(prc)*shrout

	keep permno time_m temp*
	rename permno lpermno
	save temp, replace
restore

* Monthly date to match to monthly return database
gen time_m = mofd(time_d)
format time_m %tm

merge 1:1 lpermno time_m using temp, keep(master match) nogenerate
xtset gvkey fyear

gen tempEarn  = ib/tempmktcap
gen tempDEarn = (ib - l.ib)/tempmktcap

* Regression for value relevance of earnings
asreg tempMom15m tempEarn tempDEarn, window(fyear 10) min(10) by(gvkey)
rename _R2 EarningsValueRelevance
drop _*

* Regression for earnings timeliness and earnings conservatism
gen tempNeg = (tempMom15m < 0)
replace tempNeg = . if mi(tempMom15m)
gen tempInter = tempNeg*tempMom15m

asreg tempEarn tempNeg tempMom15m tempInter,  window(fyear 10) min(10) by(gvkey)
rename _R2 EarningsTimeliness

gen EarningsConservatism = (_b_tempMom15m + _b_tempInter)/_b_tempMom15m
drop _* temp*


*------------------------------------------------------------------------------
// Compute abnormal accruals for Xie (2001)
gen tempCFO = oancf
replace tempCFO = fopt - (act - l.act) + (che - l.che) + (lct - l.lct) - (dlc - l.dlc) if mi(tempCFO)
gen tempAccruals = (ib - tempCFO) / ((at + l.at)/2)
gen tempInvTA = 1/((at + l.at)/2)
gen tempDelRev = (sale - l.sale)/( (at + l.at)/2)
gen tempPPE = ppegt/( (at + l.at)/2)

* Run regressions for each year and industry
ffind sic, newvar(FF48) type(48)  // Xie uses 2 digit sic industry instead
gen tempResid = .
levelsof fyear
foreach y of numlist `r(levels)' {
	foreach ind of numlist 1/48 {
		cap drop tempU
		cap reg tempAccruals tempInvTA tempDelRev tempPPE if fyear == `y' & FF48 == `ind'
		cap predict tempU if e(sample), resid
		cap replace tempResid = tempU if e(sample)
	}
}
rename tempResid AbnormalAccruals
cap drop temp* FF48


*-------------------------------------------------------------------------------
* Compute brand capital to assets
gen byte OK = !missing(xad)
bys gvkey OK (fyear): gen BrandCapital = xad/(.5 + .1) if OK==1 & _n==1
bys gvkey OK (fyear): gen tempYear = fyear if OK==1 & _n==1
egen FirstNMyear = min(tempYear), by(gvkey)

gen tempxad = xad
replace tempxad = 0 if mi(xad)  

replace BrandCapital = 0 if mi(BrandCapital)
xtset gvkey fyear
by gvkey: replace BrandCapital = (1-.5)*l.BrandCapital + tempxad if _n > 1
replace BrandCapital = . if mi(FirstNMyear) | fyear < FirstNMyear
replace BrandCapital = . if mi(xad) 

replace BrandCapital = BrandCapital/at

drop OK temp* FirstNM

* For future use
replace xad = 0 if mi(xad) // We use xad = 0 if missing from now on throughout



*-------------------------------------------------------------------------------
* Equity duration

gen tempRoE = ib/l.ceq
gen temp_g_eq = sale/l.sale - 1
gen tempCD = l.ceq*(tempRoE - temp_g_eq)

gen tempRoE1 = .57*tempRoE + .12/(1-.57)
gen temp_g_eq1 = .24*temp_g_eq + .06/(1-.24)
gen tempCD1 = l.ceq*(tempRoE1 - temp_g_eq1)

foreach t of numlist 2/9{
local j = `t'-1
gen tempRoE`t' = .57*tempRoE`j' + .12/(1-.57)
gen temp_g_eq`t' = .24*temp_g_eq`j' + .06/(1-.24)
gen tempCD`t' = l.ceq*(tempRoE`j' - temp_g_eq`j')

}

gen tempSum1 = tempCD/(1+.12) + 2*tempCD1/(1+.12)^2 + 3*tempCD2/(1+.12)^3 ///
    + 4*tempCD3/(1+.12)^4 + 5*tempCD4/(1+.12)^5 + 6*tempCD5/(1+.12)^6 ///
	+ 7*tempCD6/(1+.12)^7 + 8*tempCD7/(1+.12)^8 + 9*tempCD8/(1+.12)^9 ///
	+ 10*tempCD9/(1+.12)^10
	

gen tempSum2 = tempCD/(1+.12) + tempCD1/(1+.12)^2 + tempCD2/(1+.12)^3 ///
    + tempCD3/(1+.12)^4 + tempCD4/(1+.12)^5 + tempCD5/(1+.12)^6 ///
	+ tempCD6/(1+.12)^7 + tempCD7/(1+.12)^8 + tempCD8/(1+.12)^9 ///
	+ tempCD9/(1+.12)^10

gen tempME = prcc_f*csho

gen tempED = tempSum1/tempME + (10 + (1+.12)/.12)*(1-tempSum2/tempME)
gen EquityDuration = l.tempED

* Exclusions
egen tempBE = min(ceq), by(gvkey)
replace EquityDuration = . if tempBE < 0

drop temp*

*-------------------------------------------------------------------------------
* Earnings persistence and earnings predictability
gen temp = epspx/ajex
gen tempLag = l.temp
asreg temp tempLag, window(fyear 10) min(10) by(gvkey) fitted rmse
rename _b_tempLag EarningsPersistence
gen EarningsPredictability = _rmse^2
drop _* temp*

*-------------------------------------------------------------------------------
* Earnings smoothness
gen tempEarnings = ib/l.at
gen tempCF       = (ib - ( (act - l.act) - (lct - l.lct) - (che - l.che) + (dlc - l.dlc) - dp))/l.at

asrol temp*, window(fyear 10) min(10) by(gvkey) stat(sd)

gen EarningsSmoothness = sd10_tempEarnings/sd10_tempCF
drop temp*

*-------------------------------------------------------------------------------
// Expand the dataset to monthly and assume a five month lag for availabilty of annual CS
gen temp = 12
expand temp
drop temp

bysort gvkey time_m: gen time_avail_m = time_m + 5 + _n /* Note: This is formatted in CURRENT TIME: that is
							  being in this month, this is the info that is available 
							  if we assume a five month lag */

format time_avail_m %tm
drop time_m
sort gvkey time_avail_m time_d
bysort gvkey time_avail_m: keep if _n == _N  // This affects .14% of observations that had changes of fiscal year ends. In that case, we keep the more recent info

* Housekeeping
drop timeLinkStart_d timeLinkEnd_d linkprim liid linktype ///
  time_d datadate fyear gammaAbility*
compress

save "$pathProject/DataClean/m_aCompustat", replace

*------------	
timer off 1
timer list 1
