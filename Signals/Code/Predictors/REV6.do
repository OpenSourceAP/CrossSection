* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
keep if fpedats != . & fpedats > statpers + 30 
save "$pathtemp/temp", replace

// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(meanest)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempRev = (meanest - l.meanest)/abs(l.prc)
gen REV6 = tempRev + l.tempRev + l2.tempRev + l3.tempRev + l4.tempRev + l5.tempRev + l6.tempRev
label var REV6 "Earnings forecast revision"

// SAVE
do "$pathCode/savepredictor" REV6

