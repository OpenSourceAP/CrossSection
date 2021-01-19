* --------------
// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(meanest)
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPSLongRun", keep(master match) nogenerate keepusing(fgr5yr)
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_UnadjustedActuals", keep(master match) nogenerate keepusing(fy0a)
// SIGNAL CONSTRUCTION
gen tempShort = 100* (meanest - fy0a)/abs(fy0a)
gen EarningsForecastDisparity = fgr5yr - tempShort
label var EarningsForecastDisparity "Long vs short-term earnings expectations"
// SAVE
do "$pathCode/savepredictor" EarningsForecastDisparity