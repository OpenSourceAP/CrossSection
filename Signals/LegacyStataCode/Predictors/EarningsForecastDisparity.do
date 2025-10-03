* --------------

// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
keep if fpedats != . & fpedats > statpers + 30 
save "$pathtemp/tempIBESshort", replace

use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "0" 
rename meanest fgr5yr
save "$pathtemp/tempIBESlong", replace


// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempIBESshort", keep(master match) nogenerate keepusing(meanest)
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempIBESlong", keep(master match) nogenerate keepusing(fgr5yr)
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_UnadjustedActuals", keep(master match) nogenerate keepusing(fy0a)

// SIGNAL CONSTRUCTION
gen tempShort = 100* (meanest - fy0a)/abs(fy0a)
gen EarningsForecastDisparity = fgr5yr - tempShort
label var EarningsForecastDisparity "Long vs short-term earnings expectations"

// SAVE
do "$pathCode/savepredictor" EarningsForecastDisparity
