* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "0" 
save "$pathtemp/temp", replace

// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(stdev numest)

// SIGNAL CONSTRUCTION
gen ForecastDispersionLT = stdev if numest > 1 & !mi(numest)
label var ForecastDispersionLT "LT EPS Forecast Dispersion"

// SAVE
do "$pathCode/saveplacebo" ForecastDispersionLT
