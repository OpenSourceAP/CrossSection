* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1"
keep if fpedats != . & fpedats > statpers + 30 // keep only forecasts past June
save "$pathtemp/temp", replace

// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(stdev meanest)

// SIGNAL CONSTRUCTION
gen ForecastDispersion = stdev/abs(meanest)
label var ForecastDispersion "EPS Forecast Dispersion"

// SAVE
do "$pathCode/savepredictor" ForecastDispersion
