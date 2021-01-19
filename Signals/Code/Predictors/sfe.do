* --------------
// DATA LOAD
use permno time_avail_m tickerIBES prc using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(stdev_est meanest)
// SIGNAL CONSTRUCTION
gen sfe =  meanest/abs(prc)
replace sfe = . if abs(prc) < 1
label var sfe "Earnings Forecast"
// SAVE
do "$pathCode/savepredictor" sfe