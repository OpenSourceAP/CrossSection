* --------------
// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(stdev_est meanest)
// SIGNAL CONSTRUCTION
gen ForecastDispersion = stdev_est/abs(meanest)
label var ForecastDispersion "EPS Forecast Dispersion"
// SAVE
do "$pathCode/savepredictor" ForecastDispersion