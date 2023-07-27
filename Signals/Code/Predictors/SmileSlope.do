* Signal is actually contructed in PrepScripts/OptionMetricsProcessing.R
* --------------
// DATA LOAD
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTableOC", clear
* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve

keep if mi(secid)

save "$pathtemp/temp", replace
restore
drop if mi(secid)
merge m:1 secid time_avail_m using "$pathDataIntermediate/OptionMetrics", keep(master match) nogenerate
append using "$pathtemp/temp"

// SIGNAL CONSTRUCTION
* Construction is done in PrepScripts/R1_OptionMetrics.R
rename slope SmileSlope 
label var SmileSlope "Average Jump Size"

// SAVE
do "$pathCode/savepredictor" SmileSlope
