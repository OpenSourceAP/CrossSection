* --------------
* Xing, Zhang, Zhao 2010 JFQA
// DATA LOAD
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTable", clear


preserve

keep if mi(secid)

save "$pathtemp/temp", replace
restore
drop if mi(secid)
merge m:1 secid time_avail_m using "$pathDataIntermediate/OptionMetricsXZZ", keep(master match) nogenerate
append using "$pathtemp/temp"
// SIGNAL CONSTRUCTION
* Construction is done in R1_OptionMetrics.R
label var skew1 "Smirk skewness"
// SAVE
do "$pathCode/savepredictor" skew1
