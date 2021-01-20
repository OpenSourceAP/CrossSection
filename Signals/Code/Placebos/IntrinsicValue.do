* IntrinsicValue
* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" & month(statpers) == 5
keep if fpedats != . & fpedats > statpers + 30 // keep only forecasts past June
replace time_avail_m = time_avail_m + 1 // OP is conservative, this matches with Compustat following FF

save "$pathtemp/temp", replace

// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib sale datadate)
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(match) nogenerate keepusing(meanest) 

* common screens and variables
sort permno time_avail_m
xtset permno time_avail_m

gen mve_c = (shrout * abs(prc))
gen FROE = (meanest*shrout)/ceq
gen FROEi = ib/ceq

gen ceq_ave = (ceq + l12.ceq)/2
bys permno (time_avail_m): replace ceq_ave = ceq if _n <= 1

drop if ceq < 0 | ceq == . // Frankel and Lee, page 291
drop if abs(FROEi) > 1 | abs(FROE) > 1 // Frankel and Lee, page 291
keep if month(datadate) >= 6


// SIGNAL CONSTRUCTION (annual)
gen AnalystValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*ceq_ave/mve_c
gen IntrinsicValue = (1 + (FROEi - .1)/1.1 + (FROEi - .1)/(.1*1.1))*ceq_ave/mve_c
gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)

label var IntrinsicValue "Intrinsic Value"

// SAVE
do "$pathCode/saveplacebo" IntrinsicValue
