* --------------
// DATA LOAD
use permno tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(meanest)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen UpForecast = (meanest > l.meanest)
replace UpForecast = . if mi(meanest) | mi(l.meanest)
label var UpForecast "Up Forecast EPS"
// SAVE
do "$pathCode/savepredictor" UpForecast