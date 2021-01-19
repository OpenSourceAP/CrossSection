* --------------
// DATA LOAD
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPSLongRun", keep(master match) nogenerate keepusing(stdev5yr numest5yr)
// SIGNAL CONSTRUCTION
gen ForecastDispersionLT = stdev5yr if numest5yr > 1 & !mi(numest5yr)
label var ForecastDispersionLT "LT EPS Forecast Dispersion"
// SAVE
do "$pathCode/saveplacebo" ForecastDispersionLT