* --------------
// DATA LOAD
use permno time_avail_m tickerIBES mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPSLongRun", keep(master match) nogenerate keepusing(stdev5yr numest5yr)

* approximate S&P 500 only
gsort time_avail_m -mve_c
bys time_avail_m: gen sizerank = _n
drop if sizerank > 500

// SIGNAL CONSTRUCTION
gen ForecastDispersionLT = stdev5yr if numest5yr > 1 & !mi(numest5yr)
label var ForecastDispersionLT "LT EPS Forecast Dispersion"

// SAVE
do "$pathCode/saveplacebo" ForecastDispersionLT
