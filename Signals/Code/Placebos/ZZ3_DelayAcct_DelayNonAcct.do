* --------------
* NOTE: RUN LAST SINCE NEEDS PRICEDELAY AND ACCRUALQUALITY AND BOTH ARE SLOW

* --------------
* prep: PriceDelay
* Need to run PriceDelay_PriceDelayRsq_PriceDelayAdj.do first!

import delimited "$pathDataPredictors/PriceDelayRsq.csv", clear varnames(1)
tostring yyyymm, replace
gen y = substr(yyyymm, 1,4)
gen m = substr(yyyymm, 5,2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm
drop y m yyyymm
rename pricedelay PriceDelay
save "$pathtemp/tempPriceDelay", replace

* --------------
* prep: AccrualQuality
* Need to run Placebo/ZZ2_AccrualQuality_AccrualQualityJune.do first!

import delimited "$pathDataPlacebos/AccrualQuality.csv", clear varnames(1)
tostring yyyymm, replace
gen y = substr(yyyymm, 1,4)
gen m = substr(yyyymm, 5,2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm
drop y m yyyymm
rename accrualquality AccrualQuality
save "$pathtemp/tempAccrualQuality", replace

* --------------
// Prep IBES data
use tickerIBES fy0a fy0edats using "$pathDataIntermediate/IBES_UnadjustedActuals", replace
bys tickerIBES fy0edats: keep if _n == 1 
save "$pathtemp/tempIBESactual", replace

use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
keep if fpedats != . & fpedats > statpers + 30 
keep tickerIBES time_avail_m meanest fpedats
rename fpedats fy0edats
merge m:1 tickerIBES fy0edats using "$pathtemp/tempIBESactual", keep(master match) nogenerate keepusing(fy0a)

save "$pathtemp/tempIBES", replace

* --------------
* finally make this placebo
// DATA LOAD
use permno tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(at spi ib) 
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempIBES", keep(master match) nogenerate keepusing(meanest fy0edats fy0a)
merge 1:1 permno time_avail_m using "$pathtemp/tempPriceDelay", keep(master match) nogenerate keepusing(PriceDelay)
merge 1:1 permno time_avail_m using "$pathtemp/tempAccrualQuality", keep(master match) nogenerate keepusing(AccrualQuality)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempSI = spi/(.5*(at + l12.at))

gen tempSurprise = meanest - fy0a
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
gen DelayNonAcct = PriceDelay - DelayAcct
label var DelayNonAcct "Non-Accounting part price delay"

// SAVE
do "$pathCode/saveplacebo" DelayAcct
do "$pathCode/saveplacebo" DelayNonAcct
