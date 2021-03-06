* --------------
// DATA LOAD
use permno time_avail_m ticker using "$pathDataIntermediate/SignalMasterTable", clear
* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve

keep if mi(ticker)

save "$pathtemp/temp", replace
restore
drop if mi(ticker)
merge m:1 ticker time_avail_m using "$pathDataIntermediate/OptionMetrics", keep(master match) nogenerate
append using "$pathtemp/temp"
// SIGNAL CONSTRUCTION
* Construction is done in R1_OptionMetrics.R
label var skew1 "Smirk skewness"
// SAVE
do "$pathCode/savepredictor" skew1